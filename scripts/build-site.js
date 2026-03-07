#!/usr/bin/env node
/**
 * build-site.js — Generate the entire TFA Matrix site from site-data.json.
 *
 * Single source of truth: site-data.json
 * Generates:
 *   - techniques/{SAFE-T-XXXX}/index.html (all techniques)
 *   - techniques/{SAFE-T-XXXX}/{NNN}/index.html (sub-techniques)
 *   - tactics/{SAFE-TA-XXXX}/index.html (all tactics)
 *   - matrices/tfa/index.html (the matrix grid)
 *   - techniques/tfa/index.html (techniques listing)
 *   - tactics/tfa/index.html (tactics listing)
 *   - techniques/sidebar-techniques/index.html
 *   - tactics/sidebar-tactics/index.html
 *
 * Usage: node scripts/build-site.js
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const siteData = JSON.parse(readFileSync(join(ROOT, 'site-data.json'), 'utf8'));
const { tactics, techniques } = siteData;

// ── Build indices ──

const tacticById = {};
for (const t of tactics) tacticById[t.safe_id] = t;

const techByTactic = {};
for (const t of techniques) {
  if (!techByTactic[t.tactic]) techByTactic[t.tactic] = [];
  techByTactic[t.tactic].push(t);
}

// ── HTML Components ──

function escapeHtml(text) {
  if (!text) return '';
  return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function pageHeader(title, activeNav = '') {
  const navItems = [
    { href: '/matrices/tfa/', label: 'Matrix', key: 'matrix' },
    { href: '/tactics/tfa/', label: 'Tactics', key: 'tactics' },
    { href: '/techniques/tfa/', label: 'Techniques', key: 'techniques' },
    { href: '/about/', label: 'About', key: 'about' },
  ];
  const navHtml = navItems.map(n =>
    `                        <li class="nav-item">
                            <a href="${n.href}"  class="nav-link${n.key === activeNav ? ' active' : ''}" ><b>${n.label}</b></a>
                        </li>`
  ).join('\n');

  return `
<!DOCTYPE html>
<html lang='en'>

<head>

        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1,shrink-to-fit=no'>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link rel='shortcut icon' href='/theme/favicon.ico' type='image/x-icon'>
        <title>${escapeHtml(title)}</title>
        <!-- Bootstrap CSS -->
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap.min.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-tourist.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-select.min.css' />
        <!-- Fontawesome CSS -->
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/fontawesome.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/brands.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/solid.min.css"/>
            <link rel="stylesheet" href="/theme/style-user.css"/>


</head>

<body>

    <div class="safety-banner" id="browser-safety-banner">
        <div class="safety-banner-content">
            <strong>Is someone checking your browsing?</strong>
            This website will appear in your browser history. If you're concerned someone may be monitoring your internet use, consider using a trusted friend's device, a library computer, or your browser's private/incognito mode. You can press <strong>Quick Exit</strong> or hit <strong>Escape</strong> at any time to leave this site quickly.
            <a href="/about/online-safety/">Learn more about staying safe online</a>
        </div>
        <button class="safety-banner-close" id="close-safety-banner" aria-label="Dismiss safety notice">&times;</button>
    </div>


    <div class="container-fluid attack-website-wrapper d-flex flex-column h-100">
        <div class="row sticky-top flex-grow-0 flex-shrink-1">
            <header class="col px-0">
                    <nav class='navbar navbar-expand-lg navbar-dark position-static'>
        <a class='navbar-brand' href='/'><img src="/theme/images/safe_logo_header.png" class="attack-logo"></a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarCollapse'
                aria-controls='navbarCollapse' aria-expanded='false' aria-label='Toggle navigation'>
                <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarCollapse'>
            <ul class='nav nav-tabs ml-auto'>
${navHtml}
                        <li class="nav-item">
                            <button id="search-button" class="btn search-button">Search <div id="search-icon" class="icon-button search-icon"></div></button>
                        </li>


            </ul>
            <a href="https://doodles.google" id="quick-exit-btn" class="btn ml-3"
               style="background-color: #e65100; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px;"
               title="Press Escape to quickly leave this site">Quick Exit</a>
        </div>
    </nav>
    <div class="quick-exit-bar">
        <a href="https://doodles.google" id="quick-exit-mobile" title="Press Escape to quickly leave this site">&#9889; Quick Exit</a>
    </div>

            </header>
        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <div class="col px-0">
                <!-- !versions banner! -->
            </div>
        </div>
        <div class="row flex-grow-1 flex-shrink-0">
            <!--start-indexing-for-search-->



    <div class="sidebar nav sticky-top flex-column pr-0 pt-4 pb-3 pl-3" id="v-tab" role="tablist" aria-orientation="vertical">
        <div class="resizer" id="resizer"></div>
<!--stop-indexing-for-search-->
<div id="sidebars"></div>
<!--start-indexing-for-search-->
    </div>



    <div class="tab-content col-xl-9 pt-4" id="v-tabContent">
        <div class="tab-pane fade show active" id="v-attckmatrix" role="tabpanel" aria-labelledby="v-attckmatrix-tab">
    `;
}

function pageFooter() {
  return `
        </div>
    </div>

            <!--stop-indexing-for-search-->
            <div class="overlay search" id="search-overlay" style="display: none;">
    <div class="overlay-inner">
        <div class="search-header">
            <div class="search-input">
                <input type="text" id="search-input" placeholder="search">
            </div>
            <div class="search-icons">
                <div class="search-parsing-icon spinner-border" style="display: none" id="search-parsing-icon"></div>
                <div class="close-search-icon" id="close-search-icon">&times;</div>
            </div>
        </div>
        <div id="search-body" class="search-body">
            <div class="results" id="search-results"></div>
            <div id="load-more-results" class="load-more-results">
                <button class="btn btn-default" id="load-more-results-button">load more results</button>
            </div>
        </div>
    </div>
</div>

        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <footer class="col footer">
                <div class="container-fluid">
                    <div class="row row-footer">
                        <div class="col-2 col-sm-2 col-md-2">
                            <div class="footer-center-responsive my-auto">
                                <a href="https://notastandard.org" target="_blank" rel="noopener" aria-label="Not A Standard">
                                    <img src="/theme/images/safe_logo_footer.png" class="mitre-logo-wtrans">
                                </a>
                            </div>
                        </div>
                        <div class="col-2 col-sm-2 footer-responsive-break"></div>
                        <div class="footer-link-group">
                            <div class="row row-footer">
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="/about/" class="footer-link">About</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://notastandard.org" class="footer-link">About SAFE</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://form.jotform.com/260340396646056" class="footer-link" target="_blank">Submit a Pattern</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://github.com/notastandard-org/tfa-matrix" class="footer-link" target="_blank">Contribute</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://www.notastandard.org/contact-8" class="footer-link">Contact</a></u>
                                </div>
                            </div>
                            <div class="row row-footer footer-legal-row">
                                <div class="px-3 col-footer"><a href="/about/online-safety/" class="footer-link">Your Safety Online</a></div>
                                <div class="px-3 col-footer"><a href="/about/privacy/" class="footer-link">Privacy</a></div>
                                <div class="px-3 col-footer"><a href="/about/terms/" class="footer-link">Terms</a></div>
                                <div class="px-3 col-footer"><a href="/about/licensing/" class="footer-link">Licensing</a></div>
                            </div>
                            <div class="row">
                                <small class="px-3">&copy;&nbsp;2026, Not A Standard Pty Ltd. SAFE and TFA Matrix are trademarks of Not A Standard Pty Ltd.</small>
                            </div>
                        </div>
                        <div class="w-100 p-2 footer-responsive-break"></div>
                        <div class="col footer-float-right-responsive-centered">
                            <div><div><a href="https://tfa.notastandard.org" class="btn btn-primary w-100">tfa.notastandard.org</a></div></div>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    </div>

<!--stopindex-->

</div>
    <script src="/theme/scripts/jquery-3.5.1.min.js"></script>
    <script src="/theme/scripts/popper.min.js"></script>
    <script src="/theme/scripts/bootstrap-select.min.js"></script>
    <script src="/theme/scripts/bootstrap.bundle.min.js"></script>
    <script src="/theme/scripts/site.js"></script>
    <script src="/theme/scripts/settings.js"></script>
    <script src="/theme/scripts/search_bundle.js"></script>
    <script>
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') { window.location.href = 'https://doodles.google'; }
        });
    </script>
<script src="/theme/scripts/resizer.js"></script>
<script src="/theme/scripts/bootstrap-tourist.js"></script>
<script src="/theme/scripts/settings.js"></script>
<script src="/theme/scripts/sidebar-load-all.js"></script>
    <script src="/theme/scripts/view-toggle.js"></script>
    <script src="/theme/scripts/safety-banner.js"></script>
</body>
</html>`;
}

const PUBLIC_DISCLAIMER = `<div class="public-disclaimer">
                                        <p><strong>Important:</strong> This resource provides general information, not personal advice. Every situation is different. The actions suggested here may not be safe in your specific circumstances &mdash; particularly if the person causing harm could notice changes to your devices or accounts. <strong>Always consider your physical safety first.</strong></p>
                                        <p>If you need personalised support, contact <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> or your local specialist domestic violence service. If you are in immediate danger, call <a href="tel:000">000</a>.</p>
                                        <p>This framework is under active development. <a href="/about/limitations/">View full limitations &amp; methodology</a>.</p>
                                    </div>`;

const TECHNICAL_DISCLAIMER = `<div class="technical-disclaimer">
                                <p>The TFA Matrix is a research framework under active development. Technique classifications, detection methods, and mitigations reflect current understanding and are subject to revision. This framework does not constitute forensic methodology, legal evidence standards, or clinical diagnostic criteria. Practitioners should apply professional judgement appropriate to their discipline and jurisdiction.</p>
                                <p><a href="/about/limitations/">Full limitations, methodology &amp; responsible use statement</a>.</p>
                            </div>`;

function helplineBanner() {
  return `<div class="helpline-banner">
                                        <strong>Need support?</strong>
                                        <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> |
                                        Emergency: <a href="tel:000">000</a>
                                    </div>`;
}

function safetyWarningHtml(warning) {
  if (!warning) return '';
  return `<div class="safety-warning">
                                        <span class="safety-warning-icon">&#9888;</span>
                                        ${escapeHtml(warning)}
                                    </div>`;
}

function noticesHtml(notices) {
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

function actionsHtml(actions) {
  if (!actions || actions.length === 0) return '';
  const items = actions.map(a => {
    const sn = a.safety_note ? `\n                                            <p class="safety-note">${escapeHtml(a.safety_note)}</p>` : '';
    return `                                        <li>
                                            <strong>${escapeHtml(a.action)}</strong>
                                            <p>${escapeHtml(a.detail)}</p>${sn}
                                        </li>`;
  }).join('\n');
  return `<h2>What You Can Do</h2>
                                    <ul class="action-list">
${items}
                                    </ul>`;
}

function mitigationsTableHtml(mitigations) {
  if (!mitigations || mitigations.length === 0) return '<p>Mitigations for this technique are under development. If you have suggestions on how to improve this content, please <a href="https://form.jotform.com/260340396646056" target="_blank">submit a pattern</a>.</p>';
  const rows = mitigations.map(m => `                                <tr>
                                    <td><strong>${escapeHtml(m.id)}</strong></td>
                                    <td><strong>${escapeHtml(m.name)}</strong><br>${escapeHtml(m.description)}</td>
                                </tr>`).join('\n');
  return `<table class="table table-bordered">
                                <thead><tr><th style="width: 120px;">ID</th><th>Mitigation</th></tr></thead>
                                <tbody>
${rows}
                                </tbody>
                            </table>`;
}

function detectionsTableHtml(detections) {
  if (!detections || detections.length === 0) return '';
  const rows = detections.map(d => `                                <tr>
                                    <td><strong>${escapeHtml(d.id)}</strong></td>
                                    <td><strong>${escapeHtml(d.name)}</strong><br>${escapeHtml(d.description)}</td>
                                </tr>`).join('\n');
  return `<h2 class="pt-3" id="detections">Detection Indicators</h2>
                            <table class="table table-bordered">
                                <thead><tr><th style="width: 120px;">ID</th><th>Detection Indicator</th></tr></thead>
                                <tbody>
${rows}
                                </tbody>
                            </table>`;
}

// ── Generate Technique Pages ──

function buildTechniquePage(tech, isSubTechnique = false) {
  const parentId = isSubTechnique ? tech.safe_id.split('.')[0] : null;
  const tactic = tacticById[tech.tactic];
  const tacticLink = tactic ? `<a href="/tactics/${tactic.safe_id}">${escapeHtml(tactic.name)}</a>` : parentId ? '(see parent technique)' : '';

  const subTechDisplay = (tech.sub_techniques && tech.sub_techniques.length > 0)
    ? tech.sub_techniques.map(s => {
        const parts = s.safe_id.split('.');
        return `<a href="/techniques/${parts[0]}/${parts[1]}/">${s.safe_id}: ${escapeHtml(s.name)}</a>`;
      }).join('<br>')
    : 'No sub-techniques';

  const breadcrumb = isSubTechnique
    ? `<li class="breadcrumb-item"><a href="/techniques/${parentId}/">${parentId}</a></li>
        <li class="breadcrumb-item">${escapeHtml(tech.name)}</li>`
    : `<li class="breadcrumb-item">${escapeHtml(tech.name)}</li>`;

  const isTechnicalOnly = !tech.public_title && !tech.public_summary;

  const publicViewContent = isTechnicalOnly
    ? `${helplineBanner()}
                                    <h1>${escapeHtml(tech.name)}</h1>
                                    <p class="technical-only-notice">This technique is documented for researchers and practitioners. It describes how perpetrators discover or acquire abuse methods, and is not written as victim-facing guidance.</p>
                                    <p>Switch to <strong>Technical View</strong> above for the full description, mitigations, and detection indicators.</p>
                                ${PUBLIC_DISCLAIMER}`
    : `${helplineBanner()}
                                    ${safetyWarningHtml(tech.safety_warning)}
                                    <h1>${escapeHtml(tech.public_title || tech.name)}</h1>
                                    <p class="public-summary">${escapeHtml(tech.public_summary || '')}</p>
                                    ${noticesHtml(tech.notices)}
                                    ${actionsHtml(tech.actions)}
                                ${PUBLIC_DISCLAIMER}`;

  const title = `${escapeHtml(tech.name)}, Technique ${tech.safe_id} | SAFE TFA Matrix`;

  return `${pageHeader(title, 'techniques')}
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="/techniques/">Techniques</a></li>
        ${breadcrumb}
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
                                    ${publicViewContent}
                                </div>
                            <div class="view-technical" style="display: none;">
                            <h1 id="">
                        ${escapeHtml(tech.name)}
                    </h1>

                        <div class="row">
                            <div class="col-md-8">
                                    <div class="description-body">
                                                <p>${escapeHtml(tech.description)}</p>
                                    </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card">
                                    <div class="card-body">
                                            <div class="row card-data" id="card-id">
                                                <div class="col-md-1 px-0 text-center"></div>
                                                <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">ID:&nbsp;</span>${tech.safe_id}
                                                </div>
                                            </div>
                                        <div class="row card-data">
                                            <div class="col-md-1 px-0 text-center"></div>
                                            <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">Sub-techniques:&nbsp;</span>
                                                        ${subTechDisplay}
                                            </div>
                                        </div>
                                            <div id="card-tactics" class="row card-data">
                                                <div class="col-md-1 px-0 text-center"></div>
                                                <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">Tactic:</span>
                                                        ${tacticLink}                                                </div>
                                            </div>
                                            <div class="row card-data">
                                                <div class="col-md-1 px-0 text-center"></div>
                                                <div class="col-md-11 pl-0">
                                                    <span class="h5 card-title">Created:&nbsp;</span>04 February 2026
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
                            ${mitigationsTableHtml(tech.mitigations)}
${detectionsTableHtml(tech.detections)}
${TECHNICAL_DISCLAIMER}
                            </div><!-- end view-technical --></div>
            </div>
        </div>
    </div>
${pageFooter()}`;
}

// ── Generate Tactic Pages ──

function buildTacticPage(tactic) {
  const tacticTechs = (techByTactic[tactic.safe_id] || []).sort((a, b) => a.name.localeCompare(b.name));
  const techRows = tacticTechs.map(t => `                <tr class="technique">
                    <td colspan="2" style="white-space: nowrap;">
                        <a href="/techniques/${t.safe_id}"> ${t.safe_id} </a>
                    </td>
                    <td>
                        <a href="/techniques/${t.safe_id}"> ${escapeHtml(t.name)} </a>
                    </td>
                    <td>
                                ${escapeHtml(t.description).substring(0, 350)}${t.description.length > 350 ? '...' : ''}
                    </td>
                </tr>`).join('\n');

  const title = `${escapeHtml(tactic.name)} | SAFE TFA Matrix`;

  return `${pageHeader(title, 'tactics')}
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="/tactics/">Tactics</a></li>
        <li class="breadcrumb-item">${escapeHtml(tactic.name)}</li>
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
                                    ${helplineBanner()}
                                    ${safetyWarningHtml(tactic.public_safety)}
                                    <h1>${escapeHtml(tactic.public_name || tactic.name)}</h1>
                                    <p class="public-summary">${escapeHtml(tactic.public_intro || '')}</p>
                                ${PUBLIC_DISCLAIMER}
                                </div>
                            <div class="view-technical" style="display: none;">
                            <h1>
                        ${escapeHtml(tactic.name)}
                    </h1>

                        <div class="row">
                            <div class="col-md-8">
                                <div class="description-body">
                                            <p>${escapeHtml(tactic.description)}</p>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card">
                                    <div class="card-body">
                                        <div class="card-data"><span class="h5 card-title">ID:</span> ${tactic.safe_id}</div>
                                            <div class="card-data"><span class="h5 card-title">Created:&nbsp;</span>04 February 2026</div>
                                            <div class="card-data"><span class="h5 card-title">Last Modified:&nbsp;</span>07 March 2026</div>
                                    </div>
                                </div>
                            </div>
                        </div>
${TECHNICAL_DISCLAIMER}
                            </div><!-- end view-technical -->
                        <h2 class="pt-3" id ="techniques">Techniques</h2><h6 class="table-object-count">Techniques: ${tacticTechs.length}</h6>
                        <table class="table-techniques">
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
${pageFooter()}`;
}

// ── Shared Matrix Grid Components ──

function buildMatrixHeaders() {
  return tactics.map(t =>
    `                <td class="tactic name"><a href="/tactics/${t.safe_id}" data-toggle="tooltip" data-placement="top" title="${t.safe_id}">${escapeHtml(t.name)}</a></td>`
  ).join('\n');
}

function buildMatrixCounts() {
  return tactics.map(t => {
    const count = (techByTactic[t.safe_id] || []).length;
    return `                <td class="tactic count">\n                    ${count}&nbsp;techniques\n                </td>`;
  }).join('\n');
}

function buildMatrixColumns() {
  return tactics.map(t => {
    const techs = (techByTactic[t.safe_id] || []).sort((a, b) => a.name.localeCompare(b.name));
    const cells = techs.map(tech => {
      const cellId = `technique-cell--${t.safe_id}--${tech.safe_id}`;
      const hasSubs = tech.sub_techniques && tech.sub_techniques.length > 0;

      const subTechRows = hasSubs ? tech.sub_techniques.map(sub => {
        const subParts = sub.safe_id.split('.');
        const subCellId = `technique-cell--${t.safe_id}--${sub.safe_id.replace('.', '-')}`;
        return `
                                        <tr class="technique-row" >
                                            <td>
<div data-public-title="${escapeHtml(sub.public_title || sub.name)}" data-tech-title="${escapeHtml(sub.name)}" class="technique-cell subtechnique"  id="${subCellId}">
    <a href="/techniques/${subParts[0]}/${subParts[1]}/" data-toggle="tooltip" data-placement="top" data-animation="false" data-container="#${subCellId}" title="${sub.safe_id}">.${subParts[1]} ${escapeHtml(sub.name)}</a>
</div>
                                            </td>
                                        </tr>`;
      }).join('\n') : '';

      const subTechToggle = hasSubs
        ? `\n    <span onclick="toggleMatrixSubTechniques('${t.safe_id}', '${tech.safe_id}')" class="subtechniques-count">${tech.sub_techniques.length}</span>`
        : '';

      return `                        <!-- technique row -->
                            <tr class="technique-row" >
                                <td>
<div data-public-title="${escapeHtml(tech.public_title || tech.name)}" data-tech-title="${escapeHtml(tech.name)}" class="technique-cell ${hasSubs ? 'has-subtechniques' : ''}"  id="${cellId}">
    <a href="/techniques/${tech.safe_id}" data-toggle="tooltip" data-placement="top" data-animation="false" data-container="#${cellId}" title="${tech.safe_id}">${escapeHtml(tech.name)}</a>${subTechToggle}
</div>
                                </td>
                                <td class="subtechniques-td">
                                    <div class="subtechniques hidden subtechniques-container subtechniques--${t.safe_id}--${tech.safe_id}">
                                        <table class="sub-techniques-table">${subTechRows}
                                        </table>
                                    </div>
                                </td>
                            </tr>`;
    }).join('\n');

    return `                <td class="tactic">
                    <table class="techniques-table">
${cells}
                    </table>
                </td>`;
  }).join('\n');
}

// ── Generate Matrix Page ──

function buildMatrixPage() {
  const MATRIX_DISCLAIMER = `<div class="matrix-disclaimer view-public">
                            <p>This matrix shows known patterns of technology-facilitated abuse. It is not a complete list &mdash; new techniques emerge as technology changes. Click any technique for guidance on what to notice and what you can do.</p>
                            <p>Need support? <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> | Emergency: <a href="tel:000">000</a> | <a href="/about/limitations/">Limitations &amp; methodology</a></p>
                        </div>`;

  const tacticHeaders = buildMatrixHeaders();
  const tacticCounts = buildMatrixCounts();
  const tacticColumns = buildMatrixColumns();

  return `${pageHeader('TFA Matrix | SAFE TFA Matrix', 'matrix')}
    <div class="row">
        <div class="col-md-9">
            <ol class="breadcrumb mx-0 px-1">
                <li class="breadcrumb-item"><a href="/">Home</a></li>
                <li class="breadcrumb-item"><a href="/matrices/">Matrices</a></li>
                <li class="breadcrumb-item">TFA</li>
            </ol>
    <div class="view-toggle-container" role="group" aria-label="Content view selection">
                        <button class="view-toggle-btn" data-view="technical" aria-pressed="false">Technical View</button>
                        <button class="view-toggle-btn active" data-view="public" aria-pressed="true">Public View</button>
                    </div>
${MATRIX_DISCLAIMER}
        </div>
    </div>
    <div class="tab-pane fade show active" id="v-attckmatrix" role="tabpanel" aria-labelledby="v-attckmatrix-tab">

        <div class="matrix-container p-3">
                <div class="row">
                    <div class="col-md-9">
                        <h1>TFA Matrix</h1>
                        <p>Below are the tactics and techniques representing the SAFE TFA (Technology-Facilitated Abuse) Matrix. This matrix maps the tactics and techniques used in technology-facilitated interpersonal harm.</p>
                    </div>
                </div>
        </div>
            <div class="pb-3">
                <div id="tour-matrix-container">
            <div class="matrix-container p-3">
    <div class="scroll-indicator-group">
        <div class="scroll-indicator left">
            <div class="cover"></div>
        </div>
        <div class="overflow-x-auto matrix-scroll-box pb-3">
                <table class="matrix side">
    <thead>
        <tr>
${tacticHeaders}
        </tr>
        <tr>
${tacticCounts}
        </tr>
    </thead>
    <tbody>
        <tr>
${tacticColumns}
        </tr>
    </tbody>
</table>

        </div>
        <div class="scroll-indicator right">
            <div class="cover"></div>
        </div>
    </div>
</div>

</div>

            </div>
    </div>
${pageFooter()}`;
}

// ── Generate Home Page ──

function buildHomePage() {
  const totalTactics = tactics.length;
  const totalTechniques = techniques.length;

  const navHtml = [
    { href: '/matrices/tfa/', label: 'Matrix' },
    { href: '/tactics/tfa/', label: 'Tactics' },
    { href: '/techniques/tfa/', label: 'Techniques' },
    { href: '/about/', label: 'About' },
  ].map(n =>
    `                        <li class="nav-item">
                            <a href="${n.href}"  class="nav-link" ><b>${n.label}</b></a>
                        </li>`
  ).join('\n');

  // Reuse shared matrix grid components
  const tacticHeaders = buildMatrixHeaders();
  const tacticCounts = buildMatrixCounts();
  const tacticColumns = buildMatrixColumns();

  return `
<!DOCTYPE html>
<html lang='en'>

<head>

        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1,shrink-to-fit=no'>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link rel='shortcut icon' href='/theme/favicon.ico' type='image/x-icon'>
        <title>SAFE TFA Matrix</title>
        <!-- Bootstrap CSS -->
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap.min.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-tourist.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-select.min.css' />
        <!-- Fontawesome CSS -->
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/fontawesome.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/brands.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/solid.min.css"/>
            <link rel="stylesheet" href="/theme/style-user.css"/>

</head>

<body>

    <div class="safety-banner" id="browser-safety-banner">
        <div class="safety-banner-content">
            <strong>Is someone checking your browsing?</strong>
            This website will appear in your browser history. If you're concerned someone may be monitoring your internet use, consider using a trusted friend's device, a library computer, or your browser's private/incognito mode. You can press <strong>Quick Exit</strong> or hit <strong>Escape</strong> at any time to leave this site quickly.
            <a href="/about/online-safety/">Learn more about staying safe online</a>
        </div>
        <button class="safety-banner-close" id="close-safety-banner" aria-label="Dismiss safety notice">&times;</button>
    </div>


    <div class="container-fluid attack-website-wrapper d-flex flex-column h-100">
        <div class="row sticky-top flex-grow-0 flex-shrink-1">
            <header class="col px-0">
                    <nav class='navbar navbar-expand-lg navbar-dark position-static'>
        <a class='navbar-brand' href='/'><img src="/theme/images/safe_logo_header.png" class="attack-logo"></a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarCollapse'
                aria-controls='navbarCollapse' aria-expanded='false' aria-label='Toggle navigation'>
                <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarCollapse'>
            <ul class='nav nav-tabs ml-auto'>
${navHtml}
                        <li class="nav-item">
                            <button id="search-button" class="btn search-button">Search <div id="search-icon" class="icon-button search-icon"></div></button>
                        </li>


            </ul>
            <a href="https://doodles.google" id="quick-exit-btn" class="btn ml-3"
               style="background-color: #e65100; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px;"
               title="Press Escape to quickly leave this site">Quick Exit</a>
        </div>
    </nav>
    <div class="quick-exit-bar">
        <a href="https://doodles.google" id="quick-exit-mobile" title="Press Escape to quickly leave this site">&#9889; Quick Exit</a>
    </div>

            </header>
        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <div class="col px-0">
                <!-- !versions banner! -->
            </div>
        </div>
        <div class="row flex-grow-1 flex-shrink-0">
            <!--start-indexing-for-search-->

    <div id="attack-jumbotron" class="col jumbotron-fluid">
        <div class="container home-banner">
            <div class="row-main-page pt-5">
                    <p class="text-justify">
                        The <strong>TFA Matrix</strong> (Technology-Facilitated Abuse Matrix) is a knowledge base of tactics and techniques used in technology-facilitated interpersonal harm. It provides a structured framework for understanding, documenting, and addressing technology-enabled abuse.
                    </p>
                    <p class="text-justify pb-2">
                        The TFA Matrix is part of the <strong>SAFE Framework</strong> developed by Not A Standard to help researchers, practitioners, and technologists better understand and mitigate technology-facilitated abuse.
                    </p>
                    <div class="p-line">
                        <p class="py-3">
                            This matrix maps <strong>${totalTactics} tactics</strong> and <strong>${totalTechniques} techniques</strong> commonly observed in technology-facilitated abuse scenarios, providing a common language for describing these behaviors.
                        </p>
                    </div>
            </div>
        </div>
    </div>
    <div id="matrix-section" class="container-fluid bg-alternate pt-5 pb-3">
        <div id="matrix-header" class="container text-center">
            <h2>TFA Matrix &mdash; Technology-Facilitated Abuse</h2>
        </div>
        <div id="matrix-enterprise">
            <div id="tour-matrix-container">
            <div class="matrix-container p-3">
    <div class="scroll-indicator-group">
        <div class="scroll-indicator left">
            <div class="cover"></div>
        </div>
        <div class="overflow-x-auto matrix-scroll-box pb-3">
                <table class="matrix side">
    <thead>
        <tr>
${tacticHeaders}
        </tr>
        <tr>
${tacticCounts}
        </tr>
    </thead>
    <tbody>
        <tr>
${tacticColumns}
        </tr>
    </tbody>
</table>

        </div>
        <div class="scroll-indicator right">
            <div class="cover"></div>
        </div>
    </div>
</div>

</div>

        </div>
    </div>
            <!--stop-indexing-for-search-->
        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <footer class="col footer">
                <div class="container-fluid">
                    <div class="row row-footer">
                        <div class="col-2 col-sm-2 col-md-2">
                            <div class="footer-center-responsive my-auto">
                                <a href="https://notastandard.org" target="_blank" rel="noopener" aria-label="Not A Standard">
                                    <img src="/theme/images/safe_logo_footer.png" class="mitre-logo-wtrans">
                                </a>
                            </div>
                        </div>
                        <div class="col-2 col-sm-2 footer-responsive-break"></div>
                        <div class="footer-link-group">
                            <div class="row row-footer">
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="/about/" class="footer-link">About</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://notastandard.org" class="footer-link">About SAFE</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://form.jotform.com/260340396646056" class="footer-link" target="_blank">Submit a Pattern</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://github.com/notastandard-org/tfa-matrix" class="footer-link" target="_blank">Contribute</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://www.notastandard.org/contact-8" class="footer-link">Contact</a></u>
                                </div>
                            </div>
                            <div class="row row-footer footer-legal-row">
                                <div class="px-3 col-footer"><a href="/about/online-safety/" class="footer-link">Your Safety Online</a></div>
                                <div class="px-3 col-footer"><a href="/about/privacy/" class="footer-link">Privacy</a></div>
                                <div class="px-3 col-footer"><a href="/about/terms/" class="footer-link">Terms</a></div>
                                <div class="px-3 col-footer"><a href="/about/licensing/" class="footer-link">Licensing</a></div>
                            </div>
                            <div class="row">
                                <small class="px-3">&copy;&nbsp;2026, Not A Standard Pty Ltd. SAFE and TFA Matrix are trademarks of Not A Standard Pty Ltd.</small>
                            </div>
                        </div>
                        <div class="w-100 p-2 footer-responsive-break"></div>
                        <div class="col footer-float-right-responsive-centered">
                            <div><div><a href="https://tfa.notastandard.org" class="btn btn-primary w-100">tfa.notastandard.org</a></div></div>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    </div>

<!--stopindex-->

</div>
    <script src="/theme/scripts/jquery-3.5.1.min.js"></script>
    <script src="/theme/scripts/popper.min.js"></script>
    <script src="/theme/scripts/bootstrap-select.min.js"></script>
    <script src="/theme/scripts/bootstrap.bundle.min.js"></script>
    <script src="/theme/scripts/site.js"></script>
    <script src="/theme/scripts/settings.js"></script>
    <script src="/theme/scripts/search_bundle.js"></script>
    <script>
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') { window.location.href = 'https://doodles.google'; }
        });
    </script>
    <script src="/theme/scripts/matrix.js"></script>
    <script src="/theme/scripts/bootstrap-tourist.js"></script>
    <script src="/theme/scripts/settings.js"></script>
    <script src="/theme/scripts/tour/tour-introduction.js"></script>
    <script src="/theme/scripts/random_page.js"></script>
    <script src="/theme/scripts/safety-banner.js"></script>
</body>
</html>`;
}

// ── Generate Listing Pages ──

function buildTacticsListing() {
  const rows = tactics.map(t => `                                        <tr>
                                        <td style="white-space: nowrap;">
                                            <a href="/tactics/${t.safe_id}">${t.safe_id}</a>
                                        </td>
                                        <td>
                                            <a href="/tactics/${t.safe_id}">${escapeHtml(t.name)}</a>
                                        </td>
                                        <td>
                                                    ${escapeHtml(t.description)}
                                        </td>
                                        </tr>`).join('\n');

  return `${pageHeader('Tactics | SAFE TFA Matrix', 'tactics')}
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        <li class="breadcrumb-item"><a href="/tactics/">Tactics</a></li>
        <li class="breadcrumb-item">TFA</li>
    </ol>
    <div class="tab-pane fade show active" id="v-" role="tabpanel" aria-labelledby="v--tab"></div>
    <div class="row">
        <div class="col-xl-12">
            <div class="jumbotron jumbotron-fluid">
                <div class="container-fluid">
                                <h2>Tactics</h2>
                                <h6 class="table-object-count">Tactics: ${tactics.length}</h6>
                                <table class="table table-bordered table-alternate mt-2">
                                    <thead>
                                        <tr>
                                            <th scope="col" style="min-width: 120px;">ID</th>
                                            <th scope="col">Name</th>
                                            <th scope="col">Description</th>
                                        </tr>
                                    </thead>
                                    <tbody>
${rows}
                                    </tbody>
                                </table>
                </div>
            </div>
        </div>
    </div>
${pageFooter()}`;
}

function buildTechniquesListing() {
  const sorted = [...techniques].sort((a, b) => a.name.localeCompare(b.name));
  const totalWithSubs = techniques.length + techniques.reduce((sum, t) => sum + (t.sub_techniques || []).length, 0);
  const rows = sorted.map(t => {
    let row = `                <tr class="technique">
                    <td colspan="2" style="white-space: nowrap;">
                        <a href="/techniques/${t.safe_id}"> ${t.safe_id} </a>
                    </td>
                    <td>
                        <a href="/techniques/${t.safe_id}"> ${escapeHtml(t.name)} </a>
                    </td>
                    <td>
                                ${escapeHtml(t.description).substring(0, 350)}${t.description.length > 350 ? '...' : ''}
                    </td>
                </tr>`;
    if (t.sub_techniques) {
      for (const sub of t.sub_techniques) {
        const parts = sub.safe_id.split('.');
        row += `\n                <tr class="sub-technique">
                    <td style="white-space: nowrap; padding-left: 2em;">
                        <a href="/techniques/${parts[0]}/${parts[1]}/"> ${sub.safe_id} </a>
                    </td>
                    <td></td>
                    <td>
                        <a href="/techniques/${parts[0]}/${parts[1]}/"> ${escapeHtml(sub.name)} </a>
                    </td>
                    <td>
                                ${escapeHtml(sub.description).substring(0, 350)}${sub.description.length > 350 ? '...' : ''}
                    </td>
                </tr>`;
      }
    }
    return row;
  }).join('\n');

  return `${pageHeader('Techniques | SAFE TFA Matrix', 'techniques')}
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        <li class="breadcrumb-item"><a href="/techniques/">Techniques</a></li>
        <li class="breadcrumb-item">TFA</li>
    </ol>
    <div class="tab-pane fade show active" id="v-" role="tabpanel" aria-labelledby="v--tab"></div>
    <div class="row">
        <div class="col-xl-12">
            <div class="jumbotron jumbotron-fluid">
                <div class="container-fluid">
                            <h2>Techniques</h2>
                                        <h6>Techniques: ${techniques.length}, Sub-techniques: ${totalWithSubs - techniques.length}</h6>
    <table class="table-techniques">
        <thead>
            <tr>
                <td colspan="2" style="min-width: 120px;">ID</td>
                <td>Name</td>
                <td>Description</td>
            </tr>
        </thead>
        <tbody>
${rows}
        </tbody>
    </table>
                </div>
            </div>
        </div>
    </div>
${pageFooter()}`;
}

// ── Generate Sidebar Files ──

function buildTechniquesSidebar() {
  // Build tactic → techniques accordion matching original MITRE-style structure
  const tacticSections = tactics.map(tactic => {
    const techs = (techByTactic[tactic.safe_id] || []).sort((a, b) => a.name.localeCompare(b.name));
    const techItems = techs.map(t => {
      const hasSubs = t.sub_techniques && t.sub_techniques.length > 0;
      const subItems = hasSubs ? t.sub_techniques.map(sub => {
        const parts = sub.safe_id.split('.');
        return `        <div class="sidenav">
    <div class="sidenav-head  " id="tfa-${tactic.safe_id}-${t.safe_id}-${parts[1]}">
      <a href="/techniques/${parts[0]}/${parts[1]}/">
        .${parts[1]} ${escapeHtml(sub.name)}
      </a>
    </div>
</div>
`;
      }).join('\n') : '';

      if (hasSubs) {
        return `        <div class="sidenav">
  <div class="sidenav-head  " id="tfa-${tactic.safe_id}-${t.safe_id}">
      <a href="/techniques/${t.safe_id}/">
        ${escapeHtml(t.name)}
      </a>
    <div class="expand-button collapsed" id="tfa-${tactic.safe_id}-${t.safe_id}-header" data-toggle="collapse" data-target="#tfa-${tactic.safe_id}-${t.safe_id}-body" aria-expanded="false" aria-controls="#tfa-${tactic.safe_id}-${t.safe_id}-body"></div>
  </div>
  <div class="sidenav-body collapse" id="tfa-${tactic.safe_id}-${t.safe_id}-body" aria-labelledby="tfa-${tactic.safe_id}-${t.safe_id}-header">
${subItems}
  </div>
</div>
`;
      }
      return `        <div class="sidenav">
    <div class="sidenav-head  " id="tfa-${tactic.safe_id}-${t.safe_id}">
      <a href="/techniques/${t.safe_id}/">
        ${escapeHtml(t.name)}
      </a>
    </div>
</div>
`;
    }).join('\n');

    return `        <div class="sidenav">
  <div class="sidenav-head  " id="tfa-${tactic.safe_id}">
      <a href="/tactics/${tactic.safe_id}">
        ${escapeHtml(tactic.name)}
      </a>
    <div class="expand-button collapsed" id="tfa-${tactic.safe_id}-header" data-toggle="collapse" data-target="#tfa-${tactic.safe_id}-body" aria-expanded="false" aria-controls="#tfa-${tactic.safe_id}-body"></div>
  </div>
  <div class="sidenav-body collapse" id="tfa-${tactic.safe_id}-body" aria-labelledby="tfa-${tactic.safe_id}-header">
${techItems}
  </div>
</div>
`;
  }).join('\n');

  return `    <div id="v-tab" role="tablist" aria-orientation="vertical" class="h-100">
        <div class="sidenav-wrapper">
  <div class="heading" data-toggle="collapse" data-target="#sidebar-collapse" id="v-home-tab" aria-expanded="true" aria-controls="#sidebar-collapse" aria-selected="false">TECHNIQUES
    <i class="fa-solid fa-fw fa-chevron-down"></i>
    <i class="fa-solid fa-fw fa-chevron-up"></i>
  </div>
  <br class="br-mobile">
  <div class="sidenav-list collapse show" id="sidebar-collapse" aria-labelledby="v-home-tab">
<div class="sidenav">
  <div class="sidenav-head  " id="tfa">
      <a href="/techniques/tfa/">
        TFA
      </a>
    <div class="expand-button collapsed" id="tfa-header" data-toggle="collapse" data-target="#tfa-body" aria-expanded="false" aria-controls="#tfa-body"></div>
  </div>
  <div class="sidenav-body collapse" id="tfa-body" aria-labelledby="tfa-header">
${tacticSections}
  </div>
</div>

  </div>
</div>

    </div>
<!--SCRIPTS-->
<script src="/theme/scripts/navigation.js"></script>`;
}

function buildTacticsSidebar() {
  const tacticItems = tactics.map(t =>
    `        <div class="sidenav">
    <div class="sidenav-head  " id="tfa-${escapeHtml(t.name)}">
      <a href="/tactics/${t.safe_id}/">
        ${escapeHtml(t.name)}
      </a>
    </div>
</div>
`).join('\n');

  return `    <div id="v-tab" role="tablist" aria-orientation="vertical" class="h-100">
        <div class="sidenav-wrapper">
  <div class="heading" data-toggle="collapse" data-target="#sidebar-collapse" id="v-home-tab" aria-expanded="true" aria-controls="#sidebar-collapse" aria-selected="false">TACTICS
    <i class="fa-solid fa-fw fa-chevron-down"></i>
    <i class="fa-solid fa-fw fa-chevron-up"></i>
  </div>
  <br class="br-mobile">
  <div class="sidenav-list collapse show" id="sidebar-collapse" aria-labelledby="v-home-tab">
<div class="sidenav">
  <div class="sidenav-head  " id="tfa">
      <a href="/tactics/tfa/">
        TFA
      </a>
    <div class="expand-button collapsed" id="tfa-header" data-toggle="collapse" data-target="#tfa-body" aria-expanded="false" aria-controls="#tfa-body"></div>
  </div>
  <div class="sidenav-body collapse" id="tfa-body" aria-labelledby="tfa-header">
${tacticItems}
  </div>
</div>

  </div>
</div>

    </div>
<!--SCRIPTS-->
<script src="/theme/scripts/navigation.js"></script>`;
}

// ══════════════════════════════════════════════════════════
// BUILD
// ══════════════════════════════════════════════════════════

console.log('=== Building TFA Matrix Site ===\n');

let pageCount = 0;

// ── Technique pages ──
for (const tech of techniques) {
  const dir = join(ROOT, 'techniques', tech.safe_id);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, 'index.html'), buildTechniquePage(tech));
  pageCount++;

  // Sub-techniques
  if (tech.sub_techniques) {
    for (const sub of tech.sub_techniques) {
      const parts = sub.safe_id.split('.');
      const subDir = join(ROOT, 'techniques', parts[0], parts[1]);
      mkdirSync(subDir, { recursive: true });
      const subWithMeta = { ...sub, tactic: tech.tactic };
      writeFileSync(join(subDir, 'index.html'), buildTechniquePage(subWithMeta, true));
      pageCount++;
    }
  }
}
console.log(`  Technique pages: ${techniques.length} (+ ${siteData._meta.sub_technique_count} sub-techniques)`);

// ── Tactic pages ──
for (const tactic of tactics) {
  const dir = join(ROOT, 'tactics', tactic.safe_id);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, 'index.html'), buildTacticPage(tactic));
  pageCount++;
}
console.log(`  Tactic pages: ${tactics.length}`);

// ── Matrix page ──
writeFileSync(join(ROOT, 'matrices', 'tfa', 'index.html'), buildMatrixPage());
pageCount++;
console.log(`  Matrix page: matrices/tfa/`);

// ── Home page (welcome content + matrix) ──
writeFileSync(join(ROOT, 'index.html'), buildHomePage());
pageCount++;
console.log(`  Home page: index.html`);

// ── Listing pages ──
writeFileSync(join(ROOT, 'tactics', 'tfa', 'index.html'), buildTacticsListing());
writeFileSync(join(ROOT, 'techniques', 'tfa', 'index.html'), buildTechniquesListing());
pageCount += 2;
console.log(`  Listing pages: 2`);

// ── Sidebar files ──
const sidebarTechDir = join(ROOT, 'techniques', 'sidebar-techniques');
const sidebarTacDir = join(ROOT, 'tactics', 'sidebar-tactics');
if (existsSync(sidebarTechDir)) {
  writeFileSync(join(sidebarTechDir, 'index.html'), buildTechniquesSidebar());
  console.log(`  Sidebar (techniques): 1`);
  pageCount++;
}
if (existsSync(sidebarTacDir)) {
  writeFileSync(join(sidebarTacDir, 'index.html'), buildTacticsSidebar());
  console.log(`  Sidebar (tactics): 1`);
  pageCount++;
}

console.log(`\n=== Build Complete: ${pageCount} pages generated ===`);
console.log(`\n  Tactics: ${tactics.length}`);
console.log(`  Techniques: ${techniques.length}`);
console.log(`  Sub-techniques: ${siteData._meta.sub_technique_count}`);
console.log(`  Total pages: ${pageCount}`);
