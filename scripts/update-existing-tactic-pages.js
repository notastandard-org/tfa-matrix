#!/usr/bin/env node
/**
 * Add new techniques to existing tactic pages' technique tables,
 * and update technique counts.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const ttpData = JSON.parse(readFileSync(join(ROOT, 'CC-NEW-TTP-CONTENT.json'), 'utf8'));

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

const TACTIC_MAP = {
  'surveillance-tracking': 'SAFE-TA-0001',
  'harassment-intimidation': 'SAFE-TA-0003',
  'information-manipulation': 'SAFE-TA-0004',
  'isolation-control': 'SAFE-TA-0005',
  'resource-financial-control': 'SAFE-TA-0006',
};

// Group new techniques by existing tactic
const techsByTactic = {};
for (const tech of ttpData.new_techniques) {
  const tacticId = TACTIC_MAP[tech.tactic];
  if (!tacticId) continue; // New tactics handled separately
  if (!techsByTactic[tacticId]) techsByTactic[tacticId] = [];
  techsByTactic[tacticId].push(tech);
}

for (const [tacticId, techs] of Object.entries(techsByTactic)) {
  const pagePath = join(ROOT, 'tactics', tacticId, 'index.html');
  if (!existsSync(pagePath)) {
    console.log(`SKIP: ${pagePath} not found`);
    continue;
  }

  let html = readFileSync(pagePath, 'utf8');

  // Build new rows
  const newRows = techs.map(t => `                <tr class="technique">
                    <td colspan="2" style="white-space: nowrap;">
                        <a href="/techniques/${t.safe_id}"> ${t.safe_id} </a>
                    </td>
                    <td>
                        <a href="/techniques/${t.safe_id}"> ${escapeHtml(t.name)} </a>
                    </td>
                    <td>
                                ${escapeHtml(t.description).substring(0, 300)}${t.description.length > 300 ? '...' : ''}

                    </td>
                </tr>`).join('\n');

  // Insert before </tbody>
  html = html.replace('        </tbody>\n    </table>', newRows + '\n        </tbody>\n    </table>');

  // Update technique count
  const countMatch = html.match(/Techniques: (\d+)/);
  if (countMatch) {
    const oldCount = parseInt(countMatch[1]);
    const newCount = oldCount + techs.length;
    html = html.replace(`Techniques: ${oldCount}`, `Techniques: ${newCount}`);
  }

  writeFileSync(pagePath, html);
  console.log(`Updated ${tacticId}: added ${techs.length} techniques`);
}

console.log('\nDone.');
