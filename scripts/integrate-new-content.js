#!/usr/bin/env node
/**
 * Integrate new techniques, sub-techniques, and tactics into the live site.
 *
 * Reads CC-NEW-TTP-CONTENT.json and CC-NEW-SUBTECHNIQUE-CONTENT.json,
 * creates HTML pages matching the existing site structure.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const ttpData = JSON.parse(readFileSync(join(ROOT, 'CC-NEW-TTP-CONTENT.json'), 'utf8'));
const subData = JSON.parse(readFileSync(join(ROOT, 'CC-NEW-SUBTECHNIQUE-CONTENT.json'), 'utf8'));

// Read an existing page as template reference for header/footer
const templatePage = readFileSync(join(ROOT, 'techniques', 'SAFE-T-0072', 'index.html'), 'utf8');

// Extract header (everything up to and including breadcrumb opening)
const headerEnd = templatePage.indexOf('<ol class="breadcrumb">');
const HEADER = templatePage.substring(0, headerEnd);

// Extract footer (from search overlay to end)
const footerStart = templatePage.indexOf('            <!--stop-indexing-for-search-->');
const FOOTER = templatePage.substring(footerStart);

// Tactic shortname -> existing tactic mapping (for linking)
const TACTIC_MAP = {
  'surveillance-tracking': { id: 'SAFE-TA-0001', name: 'Surveillance & Tracking' },
  'access-credential-control': { id: 'SAFE-TA-0002', name: 'Access & Credential Control' },
  'harassment-intimidation': { id: 'SAFE-TA-0003', name: 'Harassment & Intimidation' },
  'isolation-control': { id: 'SAFE-TA-0004', name: 'Isolation & Control' },
  'information-manipulation': { id: 'SAFE-TA-0005', name: 'Information Manipulation' },
  'image-based-abuse': { id: 'SAFE-TA-0006', name: 'Image-Based Abuse' },
  'resource-financial-control': { id: 'SAFE-TA-0007', name: 'Resource & Financial Control' },
  'grooming-targeted-recruitment': { id: 'SAFE-TA-0008', name: 'Grooming & Targeted Recruitment' },
  'discovery-preparation': { id: 'SAFE-TA-0009', name: 'Discovery & Preparation' },
};

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function generateNoticesHtml(notices) {
  if (!notices || notices.length === 0) return '';
  const items = notices.map(n => `                                        <li>
                                            <strong>${escapeHtml(n.signal)}</strong>
                                            <p>${escapeHtml(n.detail)}</p>
                                        </li>`).join('\n');
  return `<h2>What You Might Notice</h2>
                                    <ul class="notice-list">
${items}
                                    </ul>`;
}

function generateActionsHtml(actions) {
  if (!actions || actions.length === 0) return '';
  const items = actions.map(a => {
    const safetyNote = a.safety_note ? `\n                                            <p class="safety-note">${escapeHtml(a.safety_note)}</p>` : '';
    return `                                        <li>
                                            <strong>${escapeHtml(a.action)}</strong>
                                            <p>${escapeHtml(a.detail)}</p>${safetyNote}
                                        </li>`;
  }).join('\n');
  return `<h2>What You Can Do</h2>
                                    <ul class="action-list">
${items}
                                    </ul>`;
}

function generateTechniquePage(tech, isSubTechnique = false) {
  const safeId = tech.safe_id;
  const name = tech.name;
  const description = tech.description;
  const publicTitle = tech.x_safe_public_title;
  const publicSummary = tech.x_safe_public_summary;
  const safetyWarning = tech.x_safe_public_safety_warning;
  const notices = tech.x_safe_public_notices || [];
  const actions = tech.x_safe_public_actions || [];
  const tacticShortname = tech.tactic || (tech.parent ? null : null);
  const tactic = tacticShortname ? TACTIC_MAP[tacticShortname] : null;
  const subTechniques = tech.sub_techniques || [];

  // Build title
  const pageTitle = `${escapeHtml(name)}, Technique ${safeId} | SAFE TFA Matrix`;

  // Safety warning HTML
  const safetyWarningHtml = safetyWarning ? `<div class="safety-warning">
                                        <span class="safety-warning-icon">&#9888;</span>
                                        ${escapeHtml(safetyWarning)}
                                    </div>` : '';

  // Sub-techniques display
  const subTechDisplay = subTechniques.length > 0
    ? subTechniques.map(s => `<a href="/techniques/${s.safe_id.replace('.', '/')}/">${s.safe_id}: ${escapeHtml(s.name)}</a>`).join('<br>')
    : 'No sub-techniques';

  // Parent link for sub-techniques
  const parentId = tech.parent || null;
  const breadcrumbTech = isSubTechnique
    ? `<li class="breadcrumb-item"><a href="/techniques/${parentId}/">${parentId}</a></li>
        <li class="breadcrumb-item">${escapeHtml(name)}</li>`
    : `<li class="breadcrumb-item">${escapeHtml(name)}</li>`;

  // Tactic link
  const tacticHtml = tactic
    ? `<a href="/tactics/${tactic.id}">${escapeHtml(tactic.name)}</a>`
    : parentId ? '(see parent technique)' : 'N/A';

  // Fix header title
  let header = HEADER.replace(
    /<title>[^<]*<\/title>/,
    `<title>${pageTitle}</title>`
  );

  // Make Techniques nav active
  header = header.replace(
    'href="/techniques/tfa/"  class="nav-link"',
    'href="/techniques/tfa/"  class="nav-link"'
  );

  return `${header}<ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="/techniques/">Techniques</a></li>
        ${breadcrumbTech}
    </ol>
    <div class="view-toggle-container" role="group" aria-label="Content view selection">
                        <button class="view-toggle-btn" data-view="technical" aria-pressed="false">Technical View</button>
                        <button class="view-toggle-btn active" data-view="public" aria-pressed="true">Public View</button>
                    </div>
    <div class="tab-pane fade show active" id="v-" role="tabpanel" aria-labelledby="v--tab"></div>
    <div class="row">
        <div class="col-xl-12">
            <div class="jumbotron jumbotron-fluid">
                <div class="container-fluid">
                    <div class="view-public">
                                    <div class="helpline-banner">
                                        <strong>Need support?</strong>
                                        <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> |
                                        Emergency: <a href="tel:000">000</a>
                                    </div>
                                    ${safetyWarningHtml}
                                    <h1>${escapeHtml(publicTitle)}</h1>
                                    <p class="public-summary">${escapeHtml(publicSummary)}</p>
                                    ${generateNoticesHtml(notices)}
                                    ${generateActionsHtml(actions)}
                                <div class="public-disclaimer">
                                        <p><strong>Important:</strong> This resource provides general information, not personal advice. Every situation is different. The actions suggested here may not be safe in your specific circumstances &mdash; particularly if the person causing harm could notice changes to your devices or accounts. <strong>Always consider your physical safety first.</strong></p>
                                        <p>If you need personalised support, contact <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> or your local specialist domestic violence service. If you are in immediate danger, call <a href="tel:000">000</a>.</p>
                                        <p>This framework is under active development. <a href="/about/limitations/">View full limitations &amp; methodology</a>.</p>
                                    </div>
                                </div>
                            <div class="view-technical" style="display: none;">
                            <h1 id="">
                        ${escapeHtml(name)}
                    </h1>

                        <div class="row">
                            <div class="col-md-8">

                                    <div class="description-body">
                                                <p>${escapeHtml(description)}</p>

                                    </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card">
                                    <div class="card-body">
                                            <div class="row card-data" id="card-id">
                                                <div class="col-md-1 px-0 text-center"></div>
                                                <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">ID:&nbsp;</span>${safeId}
                                                </div>
                                            </div>
                                        <!--stop-indexing-for-search-->
                                        <div class="row card-data">
                                            <div class="col-md-1 px-0 text-center"></div>
                                            <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">Sub-techniques:&nbsp;</span>
                                                        ${subTechDisplay}
                                            </div>
                                        </div>
                                        <!--start-indexing-for-search-->
                                            <div id="card-tactics" class="row card-data">
                                                <div class="col-md-1 px-0 text-center">
                                                    <span data-toggle="tooltip" data-placement="left" title="" data-test-ignore="true" data-original-title="The tactic objectives that the (sub-)technique can be used to accomplish">&#9432;</span>
                                                </div>
                                                <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">Tactic:</span>
                                                        ${tacticHtml}                                                </div>
                                            </div>
                                            <div class="row card-data">
                                                <div class="col-md-1 px-0 text-center"></div>
                                                <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">Created:&nbsp;</span>07 March 2026
                                                </div>
                                            </div>
                                            <div class="row card-data">
                                                <div class="col-md-1 px-0 text-center"></div>
                                                <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">Last Modified:&nbsp;</span>07 March 2026
                                                </div>
                                            </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                            <h2 class="pt-3" id ="mitigations">Mitigations</h2>
                            <p>Mitigations for this technique are under development.</p>
<div class="technical-disclaimer">
                                <p>The TFA Matrix is a research framework under active development. Technique classifications, detection methods, and mitigations reflect current understanding and are subject to revision. This framework does not constitute forensic methodology, legal evidence standards, or clinical diagnostic criteria. Practitioners should apply professional judgement appropriate to their discipline and jurisdiction.</p>
                                <p><a href="/about/limitations/">Full limitations, methodology &amp; responsible use statement</a>.</p>
                            </div>
                            </div><!-- end view-technical --></div>
            </div>
        </div>
    </div>

        </div>
    </div>

${FOOTER}`;
}

function generateTacticPage(tactic, techniques) {
  const safeId = tactic.safe_id;
  const name = tactic.name;
  const description = tactic.description;
  const publicName = tactic.x_safe_public_name;
  const publicIntro = tactic.x_safe_public_intro;
  const publicSafety = tactic.x_safe_public_safety;

  const pageTitle = `${escapeHtml(name)} | SAFE TFA Matrix`;

  // Safety warning for public view
  const safetyHtml = publicSafety ? `<div class="safety-warning">
                                        <span class="safety-warning-icon">&#9888;</span>
                                        ${escapeHtml(publicSafety)}
                                    </div>` : '';

  // Build technique rows
  const sortedTechs = techniques.sort((a, b) => a.name.localeCompare(b.name));
  const techRows = sortedTechs.map(t => `                <tr class="technique">
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

  let header = HEADER.replace(
    /<title>[^<]*<\/title>/,
    `<title>${pageTitle}</title>`
  );

  return `${header}<ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="/tactics/">Tactics</a></li>
        <li class="breadcrumb-item">${escapeHtml(name)}</li>
    </ol>
    <div class="view-toggle-container" role="group" aria-label="Content view selection">
                        <button class="view-toggle-btn" data-view="technical" aria-pressed="false">Technical View</button>
                        <button class="view-toggle-btn active" data-view="public" aria-pressed="true">Public View</button>
                    </div>
    <div class="tab-pane fade show active" id="v-" role="tabpanel" aria-labelledby="v--tab"></div>
    <div class="row">
        <div class="col-xl-12">
            <div class="jumbotron jumbotron-fluid">
                <div class="container-fluid">
                    <div class="view-public">
                                    <div class="helpline-banner">
                                        <strong>Need support?</strong>
                                        <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> |
                                        Emergency: <a href="tel:000">000</a>
                                    </div>
                                    ${safetyHtml}
                                    <h1>${escapeHtml(publicName)}</h1>
                                    <p class="public-summary">${escapeHtml(publicIntro)}</p>
                                <div class="public-disclaimer">
                                        <p><strong>Important:</strong> This resource provides general information, not personal advice. Every situation is different. The actions suggested here may not be safe in your specific circumstances &mdash; particularly if the person causing harm could notice changes to your devices or accounts. <strong>Always consider your physical safety first.</strong></p>
                                        <p>If you need personalised support, contact <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> or your local specialist domestic violence service. If you are in immediate danger, call <a href="tel:000">000</a>.</p>
                                        <p>This framework is under active development. <a href="/about/limitations/">View full limitations &amp; methodology</a>.</p>
                                    </div>
                                </div>
                            <div class="view-technical" style="display: none;">
                            <h1>
                        ${escapeHtml(name)}
                    </h1>

                        <div class="row">
                            <div class="col-md-8">
                                <div class="description-body">
                                            <p>${escapeHtml(description)}</p>

                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card">
                                    <div class="card-body">
                                        <div class="card-data"><span class="h5 card-title">ID:</span> ${safeId}</div>
                                            <div class="card-data"><span class="h5 card-title">Created:&nbsp;</span>07 March 2026</div>
                                            <div class="card-data"><span class="h5 card-title">Last Modified:&nbsp;</span>07 March 2026</div>

                                    </div>
                                </div>
                            </div>
                        </div>
                        <h2 class="pt-3" id ="techniques">Techniques</h2><h6 class="table-object-count">Techniques: ${sortedTechs.length}</h6>
<div class="technical-disclaimer">
                                <p>The TFA Matrix is a research framework under active development. Technique classifications, detection methods, and mitigations reflect current understanding and are subject to revision. This framework does not constitute forensic methodology, legal evidence standards, or clinical diagnostic criteria. Practitioners should apply professional judgement appropriate to their discipline and jurisdiction.</p>
                                <p><a href="/about/limitations/">Full limitations, methodology &amp; responsible use statement</a>.</p>
                            </div>
                            </div><!-- end view-technical --><table class="table-techniques">
        <thead>
            <tr>
                <td colspan="2" style="min-width: 120px;">ID</td>
                <td>Name</td>
                <td>Description</td>
            </tr>
        </thead>
        <tbody>
${techRows}
        </tbody>
    </table>

                </div>
            </div>
        </div>
    </div>

        </div>
    </div>

${FOOTER}`;
}

// ── CREATE TECHNIQUE PAGES ──

console.log('=== Integrating New Content ===\n');

let techCount = 0;
let subCount = 0;

// New parent techniques from TTP file
for (const tech of ttpData.new_techniques) {
  const dirPath = join(ROOT, 'techniques', tech.safe_id);
  mkdirSync(dirPath, { recursive: true });
  writeFileSync(join(dirPath, 'index.html'), generateTechniquePage(tech));
  techCount++;
  console.log(`  Created technique: ${tech.safe_id} - ${tech.name}`);

  // Sub-techniques embedded in parent
  if (tech.sub_techniques) {
    for (const sub of tech.sub_techniques) {
      // Sub-technique dir: SAFE-T-0146/001/
      const parts = sub.safe_id.split('.');
      const subDirPath = join(ROOT, 'techniques', parts[0], parts[1]);
      mkdirSync(subDirPath, { recursive: true });
      // Add parent's tactic to sub
      const subWithTactic = { ...sub, tactic: tech.tactic, parent: parts[0] };
      writeFileSync(join(subDirPath, 'index.html'), generateTechniquePage(subWithTactic, true));
      subCount++;
      console.log(`    Created sub-technique: ${sub.safe_id} - ${sub.name}`);
    }
  }
}

// Sub-techniques for existing parents from subtechnique file
for (const sub of subData.sub_techniques) {
  const parts = sub.safe_id.split('.');
  const subDirPath = join(ROOT, 'techniques', parts[0], parts[1]);
  mkdirSync(subDirPath, { recursive: true });
  const subWithParent = { ...sub, parent: parts[0] };
  writeFileSync(join(subDirPath, 'index.html'), generateTechniquePage(subWithParent, true));
  subCount++;
  console.log(`  Created sub-technique: ${sub.safe_id} - ${sub.name}`);
}

console.log(`\nTechniques created: ${techCount}`);
console.log(`Sub-techniques created: ${subCount}`);

// ── CREATE TACTIC PAGES ──

let tacticCount = 0;

for (const tactic of ttpData.new_tactics) {
  // Find techniques belonging to this tactic
  const tacticTechs = ttpData.new_techniques.filter(
    t => t.tactic === tactic.x_mitre_shortname
  );

  const dirPath = join(ROOT, 'tactics', tactic.safe_id);
  mkdirSync(dirPath, { recursive: true });
  writeFileSync(join(dirPath, 'index.html'), generateTacticPage(tactic, tacticTechs));
  tacticCount++;
  console.log(`  Created tactic: ${tactic.safe_id} - ${tactic.name} (${tacticTechs.length} techniques)`);
}

console.log(`\nTactics created: ${tacticCount}`);

// ── UPDATE EXISTING PARENT PAGES with sub-technique links ──

// For sub-techniques added to existing parents, update the parent's "No sub-techniques" text
const existingParentSubs = {};
for (const sub of subData.sub_techniques) {
  const parentId = sub.parent;
  if (!existingParentSubs[parentId]) existingParentSubs[parentId] = [];
  existingParentSubs[parentId].push(sub);
}

let parentUpdates = 0;
for (const [parentId, subs] of Object.entries(existingParentSubs)) {
  const parentPage = join(ROOT, 'techniques', parentId, 'index.html');
  if (!existsSync(parentPage)) {
    console.log(`  SKIP parent update: ${parentId} not found`);
    continue;
  }

  let html = readFileSync(parentPage, 'utf8');

  // Replace "No sub-techniques" with links
  const subLinks = subs.map(s => {
    const parts = s.safe_id.split('.');
    return `<a href="/techniques/${parts[0]}/${parts[1]}/">${s.safe_id}: ${escapeHtml(s.name)}</a>`;
  }).join('<br>\n                                                        ');

  if (html.includes('No sub-techniques')) {
    html = html.replace('No sub-techniques', subLinks);
    writeFileSync(parentPage, html);
    parentUpdates++;
    console.log(`  Updated parent ${parentId} with ${subs.length} sub-technique links`);
  }
}

console.log(`\nParent pages updated: ${parentUpdates}`);

// ── SUMMARY ──

console.log('\n=== Integration Complete ===');
console.log(`  New parent techniques: ${techCount}`);
console.log(`  New sub-techniques: ${subCount}`);
console.log(`  New tactics: ${tacticCount}`);
console.log(`  Existing parents updated: ${parentUpdates}`);
console.log(`  Total new pages: ${techCount + subCount + tacticCount}`);
