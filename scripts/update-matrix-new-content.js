#!/usr/bin/env node
/**
 * Update the matrix page to add new tactic columns and new techniques
 * to existing tactic columns.
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const ttpData = JSON.parse(readFileSync(join(ROOT, 'CC-NEW-TTP-CONTENT.json'), 'utf8'));
const matrixPath = join(ROOT, 'matrices', 'tfa', 'index.html');
let html = readFileSync(matrixPath, 'utf8');

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function makeTechCell(safeId, publicTitle, techTitle) {
  const cellId = `technique-cell--new--${safeId}`;
  return `                        <!-- tour technique is scheduled task under privilege escalation -->

                            <tr class="technique-row" >
                                <td>

<div data-public-title="${escapeHtml(publicTitle)}" data-tech-title="${escapeHtml(techTitle)}" class="technique-cell "  id="${cellId}">
    <a href="/techniques/${safeId}" data-toggle="tooltip" data-placement="top" data-animation="false" data-container="#${cellId}" title="${safeId}">${escapeHtml(publicTitle)}</a>
</div>

                                </td>
                                <td class="subtechniques-td">
                                    <div class="subtechniques hidden subtechniques-container subtechniques--new--${safeId}">
                                    </div>
                                </td>
                            </tr>`;
}

// ── 1. Add new tactic columns to header ──

// Map tactic shortnames to existing tactic column IDs in the matrix
// The matrix currently has 7 columns. Need to add 2 more.
const TACTIC_SHORTNAME_TO_COLUMN = {
  'surveillance-tracking': 'SAFE-TA-0001',
  'access-credential-control': 'SAFE-TA-0002',
  'harassment-intimidation': 'SAFE-TA-0003',
  'information-manipulation': 'SAFE-TA-0004',
  'isolation-control': 'SAFE-TA-0005',
  'resource-financial-control': 'SAFE-TA-0006',
  'physical-enablement': 'SAFE-TA-0007',
};

// Add new tactic headers after Physical Enablement
const newTacticHeaders = ttpData.new_tactics.map(t =>
  `                <td class="tactic name"><a href="/tactics/${t.safe_id}" data-toggle="tooltip" data-placement="top" title="${t.safe_id}">${escapeHtml(t.name)}</a></td>`
).join('\n');

html = html.replace(
  `<td class="tactic name"><a href="/tactics/SAFE-TA-0007" data-toggle="tooltip" data-placement="top" title="SAFE-TA-0007">Physical Enablement</a></td>`,
  `<td class="tactic name"><a href="/tactics/SAFE-TA-0007" data-toggle="tooltip" data-placement="top" title="SAFE-TA-0007">Physical Enablement</a></td>\n${newTacticHeaders}`
);

// Add technique count cells for new tactics
const groomingTechs = ttpData.new_techniques.filter(t => t.tactic === 'grooming-targeted-recruitment');
const discoveryTechs = ttpData.new_techniques.filter(t => t.tactic === 'discovery-preparation');

const newTacticCounts = `                <td class="tactic count">
                    ${groomingTechs.length}&nbsp;techniques
                </td>
                <td class="tactic count">
                    ${discoveryTechs.length}&nbsp;techniques
                </td>`;

html = html.replace(
  `                <td class="tactic count">
                    10&nbsp;techniques
                </td>
        </tr>
    </thead>`,
  `                <td class="tactic count">
                    10&nbsp;techniques
                </td>
${newTacticCounts}
        </tr>
    </thead>`
);

// ── 2. Add new techniques to existing tactic columns ──

// Techniques that go into existing tactics:
// SAFE-T-0161 -> surveillance-tracking (column 1, after last tech before </table>)
// SAFE-T-0162 -> information-manipulation (column 4)
// SAFE-T-0163 -> harassment-intimidation (column 3)
// SAFE-T-0164 -> resource-financial-control (column 6)
// SAFE-T-0165 -> isolation-control (column 5)

const existingTacticTechs = ttpData.new_techniques.filter(t =>
  !['grooming-targeted-recruitment', 'discovery-preparation'].includes(t.tactic)
);

// For each technique that goes into an existing tactic, find the last technique
// in that column and insert after it
for (const tech of existingTacticTechs) {
  const tacticId = TACTIC_SHORTNAME_TO_COLUMN[tech.tactic];
  if (!tacticId) {
    console.log(`  WARNING: Unknown tactic shortname "${tech.tactic}" for ${tech.safe_id}`);
    continue;
  }

  const cell = makeTechCell(tech.safe_id, tech.x_safe_public_title, tech.name);

  // Find the tactic column by looking for its header link, then find the last
  // technique row in that column's table
  // Strategy: find the href to this tactic in the header, then count which column it is,
  // then find the Nth </table> in the tbody to insert before
  const tacticHeaderPattern = `href="/tactics/${tacticId}"`;
  const headerIdx = html.indexOf(tacticHeaderPattern);
  if (headerIdx === -1) {
    console.log(`  WARNING: Could not find tactic ${tacticId} in matrix`);
    continue;
  }

  // Count which column (0-indexed) by counting how many tactic name cells come before
  const beforeHeader = html.substring(0, headerIdx);
  const colIndex = (beforeHeader.match(/class="tactic name"/g) || []).length;

  // In the tbody, find the Nth+1 </table> (each column has its own techniques-table)
  const tbodyStart = html.indexOf('<tbody>');
  let searchFrom = tbodyStart;
  for (let i = 0; i <= colIndex; i++) {
    searchFrom = html.indexOf('<table class="techniques-table">', searchFrom) + 1;
  }
  // Now find the </table> for this column
  const tableEnd = html.indexOf('</table>', searchFrom);

  // Insert before the </table>
  html = html.substring(0, tableEnd) + cell + '\n                    ' + html.substring(tableEnd);

  console.log(`  Added ${tech.safe_id} to existing tactic column ${tacticId} (col ${colIndex})`);
}

// Update technique counts for modified columns
// SAFE-TA-0001: was 10, now 11
// SAFE-TA-0003: was 12, now 13
// SAFE-TA-0004: was 11, now 12
// SAFE-TA-0005: was 10, now 11
// SAFE-TA-0006: was 11, now 12

// We need to carefully update the count cells. They appear in order in the second <tr> of <thead>
// Let me just do string replacements on the counts, being specific about which to change

// These are the existing counts in order: 10, 10, 12, 11, 10, 11, 10
// Updated: 11, 10, 13, 12, 11, 12, 10
// I need to be careful since some counts repeat. Let me replace them in order.

// Actually let me just rebuild the count row properly
const updatedCounts = [11, 10, 13, 12, 11, 12, 10, groomingTechs.length, discoveryTechs.length];
const countCells = updatedCounts.map(c => `                <td class="tactic count">
                    ${c}&nbsp;techniques
                </td>`).join('\n');

// Replace the entire count row
const countRowStart = html.indexOf('<tr>', html.indexOf('<thead>') + 10);
const countRowContentStart = html.indexOf('<td class="tactic count">', countRowStart);
const countRowEnd = html.indexOf('</tr>', countRowContentStart);
html = html.substring(0, countRowContentStart) + countCells + '\n        ' + html.substring(countRowEnd);

// ── 3. Add new tactic columns to tbody ──

// Build technique cells for each new tactic
function buildTacticColumn(techniques) {
  const cells = techniques.map(t =>
    makeTechCell(t.safe_id, t.x_safe_public_title, t.name)
  ).join('\n');

  return `                <td class="tactic">
                    <table class="techniques-table">
${cells}
                    </table>
                </td>`;
}

const groomingColumn = buildTacticColumn(groomingTechs);
const discoveryColumn = buildTacticColumn(discoveryTechs);

// Insert before </tr>\n    </tbody>
html = html.replace(
  '        </tr>\n    </tbody>\n</table>',
  `${groomingColumn}\n${discoveryColumn}\n        </tr>\n    </tbody>\n</table>`
);

writeFileSync(matrixPath, html);

console.log('\n=== Matrix Updated ===');
console.log(`  New tactic columns: 2 (SAFE-TA-0008, SAFE-TA-0009)`);
console.log(`  Techniques added to existing columns: ${existingTacticTechs.length}`);
console.log(`  Grooming techniques in new column: ${groomingTechs.length}`);
console.log(`  Discovery techniques in new column: ${discoveryTechs.length}`);

// Verify
const finalHtml = readFileSync(matrixPath, 'utf8');
const safeTA8 = finalHtml.includes('SAFE-TA-0008');
const safeTA9 = finalHtml.includes('SAFE-TA-0009');
const safeT161 = finalHtml.includes('SAFE-T-0161');
const safeT165 = finalHtml.includes('SAFE-T-0165');
console.log(`\n  Verification:`);
console.log(`    SAFE-TA-0008 present: ${safeTA8}`);
console.log(`    SAFE-TA-0009 present: ${safeTA9}`);
console.log(`    SAFE-T-0161 present: ${safeT161}`);
console.log(`    SAFE-T-0165 present: ${safeT165}`);
