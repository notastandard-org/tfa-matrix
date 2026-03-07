#!/usr/bin/env node
/**
 * One-time extraction: pull all structured data from existing HTML pages
 * into a single canonical site-data.json.
 *
 * After running this, site-data.json is the single source of truth.
 * All future content changes go into site-data.json.
 * Then run build-site.js to regenerate everything.
 */

import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

// ── Helpers ──

function extractBetween(html, startPattern, endPattern) {
  const startIdx = html.indexOf(startPattern);
  if (startIdx === -1) return '';
  const searchFrom = startIdx + startPattern.length;
  const endIdx = html.indexOf(endPattern, searchFrom);
  if (endIdx === -1) return '';
  return html.substring(searchFrom, endIdx).trim();
}

function stripHtml(text) {
  return text.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#9888;/g, '')
    .replace(/&mdash;/g, '—').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
}

function extractListItems(html, listClass) {
  const listMatch = html.match(new RegExp(`<ul class="${listClass}">(.*?)</ul>`, 's'));
  if (!listMatch) return [];
  const items = [];
  const liRegex = /<li>(.*?)<\/li>/gs;
  let m;
  while ((m = liRegex.exec(listMatch[1])) !== null) {
    const li = m[1];
    const strong = li.match(/<strong>(.*?)<\/strong>/s);
    const paragraphs = [...li.matchAll(/<p(?:\s+class="([^"]*)")?>(.*?)<\/p>/gs)];
    const item = {};
    if (strong) item.signal = stripHtml(strong[1]);
    if (listClass === 'action-list' && strong) {
      item.action = item.signal;
      delete item.signal;
    }
    for (const p of paragraphs) {
      const cls = p[1] || '';
      const text = stripHtml(p[2]);
      if (cls === 'safety-note') item.safety_note = text;
      else if (!item.detail) item.detail = text;
    }
    if (item.signal || item.action) items.push(item);
  }
  return items;
}

function extractMitigations(html) {
  const mitigations = [];
  // Find mitigations table
  const mitSection = html.match(/id\s*=\s*"?mitigations"?[^>]*>Mitigations<\/h2>(.*?)(?:<h2|<div class="technical-disclaimer")/s);
  if (!mitSection) return mitigations;
  const rows = [...mitSection[1].matchAll(/<tr>\s*<td><strong>(.*?)<\/strong><\/td>\s*<td><strong>(.*?)<\/strong><br>(.*?)<\/td>\s*<\/tr>/gs)];
  for (const row of rows) {
    mitigations.push({
      id: stripHtml(row[1]),
      name: stripHtml(row[2]),
      description: stripHtml(row[3])
    });
  }
  return mitigations;
}

function extractDetections(html) {
  const detections = [];
  const detSection = html.match(/id="detections"[^>]*>Detection Indicators<\/h2>(.*?)(?:<div class="technical-disclaimer")/s);
  if (!detSection) return detections;
  const rows = [...detSection[1].matchAll(/<tr>\s*<td><strong>(.*?)<\/strong><\/td>\s*<td><strong>(.*?)<\/strong><br>(.*?)<\/td>\s*<\/tr>/gs)];
  for (const row of rows) {
    detections.push({
      id: stripHtml(row[1]),
      name: stripHtml(row[2]),
      description: stripHtml(row[3])
    });
  }
  return detections;
}

// ── Extract Techniques ──

console.log('Extracting technique data...');
const techniques = [];
const techDir = join(ROOT, 'techniques');

for (const dir of readdirSync(techDir).sort()) {
  if (!dir.startsWith('SAFE-T-')) continue;
  const htmlPath = join(techDir, dir, 'index.html');
  if (!existsSync(htmlPath)) continue;

  const html = readFileSync(htmlPath, 'utf8');

  // Skip redirects
  if (html.includes('meta http-equiv="refresh"')) continue;

  // Technical name
  const nameMatch = html.match(/<div class="view-technical"[^>]*>\s*<h1[^>]*>\s*(.*?)\s*<\/h1>/s);
  const name = nameMatch ? stripHtml(nameMatch[1]) : dir;

  // Description
  const descMatch = html.match(/<div class="description-body">\s*<p>(.*?)<\/p>/s);
  const description = descMatch ? stripHtml(descMatch[1]) : '';

  // Tactic link
  const tacticMatch = html.match(/href="\/tactics\/(SAFE-TA-\d+)"/);
  const tactic = tacticMatch ? tacticMatch[1] : '';

  // Public content
  const publicTitleMatch = html.match(/<div class="view-public">.*?<h1>(.*?)<\/h1>/s);
  const publicTitle = publicTitleMatch ? stripHtml(publicTitleMatch[1]) : '';

  const publicSummaryMatch = html.match(/<p class="public-summary">(.*?)<\/p>/s);
  const publicSummary = publicSummaryMatch ? stripHtml(publicSummaryMatch[1]) : '';

  const warningMatch = html.match(/<div class="safety-warning">.*?<\/span>\s*(.*?)\s*<\/div>/s);
  const safetyWarning = warningMatch ? stripHtml(warningMatch[1]) : null;

  const notices = extractListItems(html, 'notice-list');
  const actions = extractListItems(html, 'action-list');
  const mitigations = extractMitigations(html);
  const detections = extractDetections(html);

  // Check for sub-techniques
  const subTechLinks = [...html.matchAll(/href="\/techniques\/(SAFE-T-\d+)\/(\d+)\/">(SAFE-T-\d+\.\d+): ([^<]+)<\/a>/g)];
  const subTechIds = subTechLinks.map(m => m[3]);

  // Extract sub-technique pages
  const subTechniques = [];
  for (const subDir of readdirSync(join(techDir, dir)).filter(d => /^\d+$/.test(d)).sort()) {
    const subPath = join(techDir, dir, subDir, 'index.html');
    if (!existsSync(subPath)) continue;
    const subHtml = readFileSync(subPath, 'utf8');
    if (subHtml.includes('meta http-equiv="refresh"')) continue;

    const subId = `${dir}.${subDir}`;
    const subNameMatch = subHtml.match(/<div class="view-technical"[^>]*>\s*<h1[^>]*>\s*(.*?)\s*<\/h1>/s);
    const subName = subNameMatch ? stripHtml(subNameMatch[1]) : subId;
    const subDescMatch = subHtml.match(/<div class="description-body">\s*<p>(.*?)<\/p>/s);
    const subDesc = subDescMatch ? stripHtml(subDescMatch[1]) : '';

    const subPubTitleMatch = subHtml.match(/<div class="view-public">.*?<h1>(.*?)<\/h1>/s);
    const subPubSummaryMatch = subHtml.match(/<p class="public-summary">(.*?)<\/p>/s);
    const subWarningMatch = subHtml.match(/<div class="safety-warning">.*?<\/span>\s*(.*?)\s*<\/div>/s);

    subTechniques.push({
      safe_id: subId,
      name: subName,
      description: subDesc,
      public_title: subPubTitleMatch ? stripHtml(subPubTitleMatch[1]) : '',
      public_summary: subPubSummaryMatch ? stripHtml(subPubSummaryMatch[1]) : '',
      safety_warning: subWarningMatch ? stripHtml(subWarningMatch[1]) : null,
      notices: extractListItems(subHtml, 'notice-list'),
      actions: extractListItems(subHtml, 'action-list'),
    });
  }

  const tech = {
    safe_id: dir,
    name,
    description,
    tactic,
    public_title: publicTitle,
    public_summary: publicSummary,
    safety_warning: safetyWarning,
    notices,
    actions,
    mitigations,
    detections,
  };

  if (subTechniques.length > 0) tech.sub_techniques = subTechniques;

  techniques.push(tech);
  const mitCount = mitigations.length;
  const detCount = detections.length;
  const subCount = subTechniques.length;
  console.log(`  ${dir}: ${name} (${mitCount}m ${detCount}d ${subCount}s)`);
}

console.log(`\nTotal techniques: ${techniques.length}`);

// ── Extract Tactics ──

console.log('\nExtracting tactic data...');
const tactics = [];
const tacticDir = join(ROOT, 'tactics');

for (const dir of readdirSync(tacticDir).sort()) {
  if (!dir.startsWith('SAFE-TA-')) continue;
  const htmlPath = join(tacticDir, dir, 'index.html');
  if (!existsSync(htmlPath)) continue;

  const html = readFileSync(htmlPath, 'utf8');
  if (html.includes('meta http-equiv="refresh"')) continue;

  // Technical name
  const nameMatch = html.match(/<div class="view-technical"[^>]*>\s*<h1>\s*(.*?)\s*<\/h1>/s);
  const name = nameMatch ? stripHtml(nameMatch[1]) : dir;

  // Description
  const descMatch = html.match(/<div class="description-body">\s*<p>(.*?)<\/p>/s);
  const description = descMatch ? stripHtml(descMatch[1]) : '';

  // Public content
  const publicNameMatch = html.match(/<div class="view-public">.*?<h1>(.*?)<\/h1>/s);
  const publicName = publicNameMatch ? stripHtml(publicNameMatch[1]) : '';

  const publicIntroMatch = html.match(/<p class="public-summary">(.*?)<\/p>/s);
  const publicIntro = publicIntroMatch ? stripHtml(publicIntroMatch[1]) : '';

  const warningMatch = html.match(/<div class="safety-warning">.*?<\/span>\s*(.*?)\s*<\/div>/s);
  const publicSafety = warningMatch ? stripHtml(warningMatch[1]) : null;

  // Technique list
  const techLinks = [...html.matchAll(/href="\/techniques\/(SAFE-T-\d+)"/g)];
  const tacticTechniques = [...new Set(techLinks.map(m => m[1]))];

  tactics.push({
    safe_id: dir,
    name,
    description,
    public_name: publicName,
    public_intro: publicIntro,
    public_safety: publicSafety,
    techniques: tacticTechniques,
  });

  console.log(`  ${dir}: ${name} (${tacticTechniques.length} techniques)`);
}

console.log(`\nTotal tactics: ${tactics.length}`);

// ── Build site-data.json ──

const siteData = {
  _meta: {
    generated: new Date().toISOString().split('T')[0],
    description: "Canonical data source for the TFA Matrix site. Edit this file, then run build-site.js to regenerate all HTML.",
    technique_count: techniques.length,
    tactic_count: tactics.length,
    sub_technique_count: techniques.reduce((sum, t) => sum + (t.sub_techniques || []).length, 0),
  },
  tactics,
  techniques,
};

const outputPath = join(ROOT, 'site-data.json');
writeFileSync(outputPath, JSON.stringify(siteData, null, 2));

console.log(`\nWritten: ${outputPath}`);
console.log(`  Tactics: ${tactics.length}`);
console.log(`  Techniques: ${techniques.length}`);
console.log(`  Sub-techniques: ${siteData._meta.sub_technique_count}`);
