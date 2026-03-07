#!/usr/bin/env node
/**
 * TFA → SAFE ID Migration Script
 *
 * Step 2: Copy each TFA-T-XXXX dir to SAFE-T-YYYY (using ID map)
 * Step 3: Find-and-replace all TFA IDs with SAFE IDs inside copied HTML
 * Step 4: Replace original TFA-T-XXXX pages with redirect stubs
 *
 * Also handles tactics (TFA-TA → SAFE-TA)
 */

import { readFileSync, writeFileSync, mkdirSync, cpSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

// Load ID map
const idMap = JSON.parse(readFileSync(
  join(ROOT, '..', 'safe-platform', 'src', 'data', 'tfa-to-safe-id-map.json'), 'utf8'
));

// Build a single flat replacement map: TFA-ID → SAFE-ID
// Order matters: longer IDs first to avoid partial replacements
const replacements = [];

// Techniques (parent only — no sub-techniques in the HTML pages)
for (const [tfa, safe] of Object.entries(idMap.techniques)) {
  if (!tfa.includes('.')) { // Skip sub-techniques like TFA-T-1006.001
    replacements.push([tfa, safe]);
  }
}

// Tactics
for (const [tfa, safe] of Object.entries(idMap.tactics)) {
  replacements.push([tfa, safe]);
}

// Mitigations
for (const [tfa, safe] of Object.entries(idMap.courses_of_action)) {
  replacements.push([tfa, safe]);
}

// Detections
for (const [tfa, safe] of Object.entries(idMap.detections)) {
  replacements.push([tfa, safe]);
}

// Sort by length descending to avoid partial matches (TFA-T-1001 before TFA-T-100)
replacements.sort((a, b) => b[0].length - a[0].length);

// Also build URL path replacements for directory references
const pathReplacements = [];
for (const [tfa, safe] of Object.entries(idMap.techniques)) {
  if (!tfa.includes('.')) {
    pathReplacements.push([`/techniques/${tfa}`, `/techniques/${safe}`]);
  }
}
for (const [tfa, safe] of Object.entries(idMap.tactics)) {
  pathReplacements.push([`/tactics/${tfa}`, `/tactics/${safe}`]);
}
pathReplacements.sort((a, b) => b[0].length - a[0].length);

// Extension property prefix replacement
const extensionReplacements = [
  ['x_tfa_', 'x_safe_'],
  ['extension-definition--acf2f380-0000-4000-8000-000000000001', 'extension-definition--acf2f380-0000-4000-8000-000000000002'],
];

function applyReplacements(html) {
  let result = html;

  // Apply path replacements first (more specific — includes /techniques/ prefix)
  for (const [from, to] of pathReplacements) {
    result = result.replaceAll(from, to);
  }

  // Apply ID replacements
  for (const [from, to] of replacements) {
    result = result.replaceAll(from, to);
  }

  // Apply extension replacements
  for (const [from, to] of extensionReplacements) {
    result = result.replaceAll(from, to);
  }

  return result;
}

function createRedirect(oldId, newId, type) {
  const typePath = type === 'tactic' ? 'tactics' : 'techniques';
  return `<!DOCTYPE html><html><head>
<meta http-equiv="refresh" content="0; url=/${typePath}/${newId}/">
<link rel="canonical" href="/${typePath}/${newId}/">
<title>Redirecting to ${newId}</title>
</head><body>
<p>This ${type} has moved to <a href="/${typePath}/${newId}/">${newId}</a></p>
</body></html>`;
}

// ── Step 2 & 3: Copy technique dirs and replace IDs ──

console.log('=== TFA → SAFE HTML Migration ===\n');

let techCount = 0;
for (const [tfaId, safeId] of Object.entries(idMap.techniques)) {
  if (tfaId.includes('.')) continue; // Skip sub-techniques

  const srcDir = join(ROOT, 'techniques', tfaId);
  const destDir = join(ROOT, 'techniques', safeId);

  if (!existsSync(srcDir)) {
    console.log(`  SKIP: ${srcDir} not found`);
    continue;
  }

  // Copy directory
  mkdirSync(destDir, { recursive: true });

  // Read, transform, write
  const srcHtml = readFileSync(join(srcDir, 'index.html'), 'utf8');
  const transformedHtml = applyReplacements(srcHtml);
  writeFileSync(join(destDir, 'index.html'), transformedHtml);

  techCount++;
}
console.log(`Techniques: ${techCount} pages copied and transformed`);

// ── Step 2 & 3: Copy tactic dirs and replace IDs ──

let tacticCount = 0;
for (const [tfaId, safeId] of Object.entries(idMap.tactics)) {
  const srcDir = join(ROOT, 'tactics', tfaId);
  const destDir = join(ROOT, 'tactics', safeId);

  if (!existsSync(srcDir)) {
    console.log(`  SKIP: ${srcDir} not found`);
    continue;
  }

  mkdirSync(destDir, { recursive: true });

  const srcHtml = readFileSync(join(srcDir, 'index.html'), 'utf8');
  const transformedHtml = applyReplacements(srcHtml);
  writeFileSync(join(destDir, 'index.html'), transformedHtml);

  tacticCount++;
}
console.log(`Tactics: ${tacticCount} pages copied and transformed`);

// ── Step 4: Replace originals with redirect stubs ──

let redirectCount = 0;
for (const [tfaId, safeId] of Object.entries(idMap.techniques)) {
  if (tfaId.includes('.')) continue;

  const srcDir = join(ROOT, 'techniques', tfaId);
  if (!existsSync(srcDir)) continue;

  writeFileSync(join(srcDir, 'index.html'), createRedirect(tfaId, safeId, 'technique'));
  redirectCount++;
}

for (const [tfaId, safeId] of Object.entries(idMap.tactics)) {
  const srcDir = join(ROOT, 'tactics', tfaId);
  if (!existsSync(srcDir)) continue;

  writeFileSync(join(srcDir, 'index.html'), createRedirect(tfaId, safeId, 'tactic'));
  redirectCount++;
}
console.log(`Redirects: ${redirectCount} stub pages created`);

// ── Summary ──

console.log('\n=== Verification Checklist ===');
console.log(`  SAFE technique dirs created: ${techCount}`);
console.log(`  SAFE tactic dirs created: ${tacticCount}`);
console.log(`  Redirect stubs created: ${redirectCount}`);
console.log(`  ID replacements applied: ${replacements.length} unique IDs`);
console.log(`  Path replacements applied: ${pathReplacements.length} URL paths`);

// Quick sanity check on first technique
const sampleSafe = join(ROOT, 'techniques', 'SAFE-T-0072', 'index.html');
if (existsSync(sampleSafe)) {
  const content = readFileSync(sampleSafe, 'utf8');
  const hasTfaId = content.includes('TFA-T-');
  const hasSafeId = content.includes('SAFE-T-0072');
  console.log(`\n  Sanity check (SAFE-T-0072):`);
  console.log(`    Contains SAFE-T-0072: ${hasSafeId ? 'YES' : 'NO — PROBLEM'}`);
  console.log(`    Contains any TFA-T-: ${hasTfaId ? 'YES — PROBLEM (residual TFA IDs)' : 'NO — CLEAN'}`);

  // Check for residual TFA IDs
  if (hasTfaId) {
    const matches = content.match(/TFA-[TDMA]+-\d+/g);
    const unique = [...new Set(matches)];
    console.log(`    Residual TFA IDs found: ${unique.join(', ')}`);
  }
}

// Check a redirect stub
const sampleRedirect = join(ROOT, 'techniques', 'TFA-T-1001', 'index.html');
if (existsSync(sampleRedirect)) {
  const content = readFileSync(sampleRedirect, 'utf8');
  const isRedirect = content.includes('meta http-equiv="refresh"');
  const pointsToSafe = content.includes('SAFE-T-0072');
  console.log(`\n  Redirect check (TFA-T-1001):`);
  console.log(`    Is redirect: ${isRedirect ? 'YES' : 'NO — PROBLEM'}`);
  console.log(`    Points to SAFE-T-0072: ${pointsToSafe ? 'YES' : 'NO — PROBLEM'}`);
}

console.log('\nDone.');
