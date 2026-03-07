import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const idMap = JSON.parse(readFileSync(
  join(ROOT, '..', 'safe-platform', 'src', 'data', 'tfa-to-safe-id-map.json'), 'utf8'
));

const replacements = [];
for (const [tfa, safe] of Object.entries(idMap.techniques)) {
  if (!tfa.includes('.')) replacements.push([tfa, safe]);
}
for (const [tfa, safe] of Object.entries(idMap.tactics)) replacements.push([tfa, safe]);
for (const [tfa, safe] of Object.entries(idMap.courses_of_action)) replacements.push([tfa, safe]);
for (const [tfa, safe] of Object.entries(idMap.detections)) replacements.push([tfa, safe]);
replacements.sort((a, b) => b[0].length - a[0].length);

const pathReplacements = [];
for (const [tfa, safe] of Object.entries(idMap.techniques)) {
  if (!tfa.includes('.')) pathReplacements.push([`/techniques/${tfa}`, `/techniques/${safe}`]);
}
for (const [tfa, safe] of Object.entries(idMap.tactics)) {
  pathReplacements.push([`/tactics/${tfa}`, `/tactics/${safe}`]);
}
pathReplacements.sort((a, b) => b[0].length - a[0].length);

// Process all matrix pages
const matrixFiles = [
  join(ROOT, 'matrices', 'tfa', 'index.html'),
  join(ROOT, 'matrices', 'index.html'),
];

for (const matrixPath of matrixFiles) {
  if (!existsSync(matrixPath)) {
    console.log(`SKIP: ${matrixPath} not found`);
    continue;
  }

  let html = readFileSync(matrixPath, 'utf8');
  const beforeCount = (html.match(/TFA-[TDMA]+-\d+/g) || []).length;

  for (const [from, to] of pathReplacements) html = html.replaceAll(from, to);
  for (const [from, to] of replacements) html = html.replaceAll(from, to);

  writeFileSync(matrixPath, html);

  const residual = html.match(/TFA-[TDMA]+-\d+/g);
  console.log(`${matrixPath}:`);
  console.log(`  TFA IDs before: ${beforeCount}`);
  console.log(`  Residual TFA IDs: ${residual ? [...new Set(residual)].join(', ') : 'NONE'}`);
  console.log(`  SAFE-T refs: ${(html.match(/SAFE-T-/g) || []).length}`);
  console.log(`  SAFE-TA refs: ${(html.match(/SAFE-TA-/g) || []).length}`);
}

// Also check the top-level techniques index and tactics index
const otherPages = [
  join(ROOT, 'techniques', 'index.html'),
  join(ROOT, 'tactics', 'index.html'),
];

for (const pagePath of otherPages) {
  if (!existsSync(pagePath)) {
    console.log(`SKIP: ${pagePath} not found`);
    continue;
  }

  let html = readFileSync(pagePath, 'utf8');
  const beforeCount = (html.match(/TFA-[TDMA]+-\d+/g) || []).length;

  if (beforeCount === 0) {
    console.log(`${pagePath}: no TFA IDs found, skipping`);
    continue;
  }

  for (const [from, to] of pathReplacements) html = html.replaceAll(from, to);
  for (const [from, to] of replacements) html = html.replaceAll(from, to);

  writeFileSync(pagePath, html);

  const residual = html.match(/TFA-[TDMA]+-\d+/g);
  console.log(`${pagePath}:`);
  console.log(`  TFA IDs before: ${beforeCount}`);
  console.log(`  Residual TFA IDs: ${residual ? [...new Set(residual)].join(', ') : 'NONE'}`);
}

// Check sidebar files
const sidebarFiles = [
  join(ROOT, 'techniques', 'sidebar-techniques', 'index.html'),
  join(ROOT, 'tactics', 'sidebar-tactics', 'index.html'),
  join(ROOT, 'matrices', 'sidebar-matrices', 'index.html'),
];

for (const sbPath of sidebarFiles) {
  if (!existsSync(sbPath)) continue;

  let html = readFileSync(sbPath, 'utf8');
  const beforeCount = (html.match(/TFA-[TDMA]+-\d+/g) || []).length;

  if (beforeCount === 0) continue;

  for (const [from, to] of pathReplacements) html = html.replaceAll(from, to);
  for (const [from, to] of replacements) html = html.replaceAll(from, to);

  writeFileSync(sbPath, html);

  const residual = html.match(/TFA-[TDMA]+-\d+/g);
  console.log(`${sbPath}:`);
  console.log(`  TFA IDs before: ${beforeCount}`);
  console.log(`  Residual: ${residual ? [...new Set(residual)].join(', ') : 'NONE'}`);
}

console.log('\nDone.');
