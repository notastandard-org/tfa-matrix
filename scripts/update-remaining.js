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

function transform(filePath) {
  if (!existsSync(filePath)) {
    console.log(`SKIP: ${filePath}`);
    return;
  }
  let html = readFileSync(filePath, 'utf8');
  const beforeCount = (html.match(/TFA-[TDMA]+-\d+/g) || []).length;
  if (beforeCount === 0) return;

  for (const [from, to] of pathReplacements) html = html.replaceAll(from, to);
  for (const [from, to] of replacements) html = html.replaceAll(from, to);

  writeFileSync(filePath, html);
  const residual = html.match(/TFA-[TDMA]+-\d+/g);
  console.log(`${filePath}: ${beforeCount} → ${residual ? residual.length : 0} TFA IDs`);
  if (residual) console.log(`  Residual: ${[...new Set(residual)].join(', ')}`);
}

// Live pages that need updating
transform(join(ROOT, 'index.html'));
transform(join(ROOT, 'tactics', 'tfa', 'index.html'));
transform(join(ROOT, 'techniques', 'tfa', 'index.html'));

console.log('Done.');
