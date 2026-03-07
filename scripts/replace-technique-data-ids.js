import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const idMap = JSON.parse(readFileSync(
  join(ROOT, '..', 'safe-platform', 'src', 'data', 'tfa-to-safe-id-map.json'), 'utf8'
));

// Build replacement pairs: longest first
const replacements = [];
for (const [tfa, safe] of Object.entries(idMap.techniques)) {
  replacements.push([tfa, safe]);
}
for (const [tfa, safe] of Object.entries(idMap.tactics)) {
  replacements.push([tfa, safe]);
}
for (const [tfa, safe] of Object.entries(idMap.courses_of_action)) {
  replacements.push([tfa, safe]);
}
for (const [tfa, safe] of Object.entries(idMap.detections)) {
  replacements.push([tfa, safe]);
}
replacements.sort((a, b) => b[0].length - a[0].length);

const filePath = join(ROOT, 'technique_data.py');
let content = readFileSync(filePath, 'utf8');

const beforeCount = (content.match(/TFA-[TDMA]+-\d+/g) || []).length;

for (const [from, to] of replacements) {
  content = content.replaceAll(from, to);
}

writeFileSync(filePath, content);

const residual = content.match(/TFA-[TDMA]+-\d+/g);
console.log(`technique_data.py: ${beforeCount} TFA IDs replaced`);
if (residual) {
  console.log(`Residual TFA IDs: ${[...new Set(residual)].join(', ')}`);
} else {
  console.log('No residual TFA IDs - CLEAN');
}
