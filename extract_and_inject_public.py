#!/usr/bin/env python3
"""
Extract public content from TFA technique HTML pages and inject into STIX bundle.
Creates backup before modifying tfa-attack.json.

Usage: cd ~/Desktop/SAFE/tfa-matrix && python3 extract_and_inject_public.py
"""
import os, re, json, html as html_mod, shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TECHNIQUES_DIR = os.path.join(SCRIPT_DIR, 'techniques')
STIX_PATH = os.path.join(SCRIPT_DIR, 'tfa-attack.json')
BACKUP_PATH = os.path.join(SCRIPT_DIR, 'tfa-attack-pre-public.json')

def clean(text):
    """Clean HTML to plain text."""
    if not text: return text
    text = html_mod.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('\u26a0', '').strip()
    return re.sub(r'\s+', ' ', text)

def extract_public(html_content):
    """Extract public-facing content from technique HTML."""
    result = {}
    
    # Technique ID
    id_m = re.search(r'<span class="h5 card-title">ID:&nbsp;</span>(TFA-T-\d+)', html_content)
    if not id_m: return None, None
    tid = id_m.group(1)
    
    # View-public section (stop at disclaimer to avoid boilerplate)
    pub_m = re.search(r'<div class="view-public">(.*?)<div class="public-disclaimer">', html_content, re.DOTALL)
    if not pub_m: return tid, None
    pub = pub_m.group(1)
    
    # Public title
    h1 = re.search(r'<h1>(.*?)</h1>', pub, re.DOTALL)
    if h1: result['x_public_title'] = clean(h1.group(1))
    
    # Public description/summary
    summ = re.search(r'<p class="public-summary">(.*?)</p>', pub, re.DOTALL)
    if summ: result['x_public_description'] = clean(summ.group(1))
    
    # Safety warning (optional - not all techniques have one)
    warn = re.search(r'<div class="safety-warning">(.*?)</div>', pub, re.DOTALL)
    if warn:
        wt = clean(warn.group(1))
        if wt: result['x_safety_warning'] = wt
    
    # Recognition signals (notice-list)
    signals = []
    nl = re.search(r'<ul class="notice-list">(.*?)</ul>', pub, re.DOTALL)
    if nl:
        for t, e in re.findall(r'<li>\s*<strong>(.*?)</strong>\s*<p>(.*?)</p>', nl.group(1), re.DOTALL):
            signals.append({'title': clean(t), 'explanation': clean(e)})
    if signals: result['x_recognition_signals'] = signals
    
    # Safety actions (action-list)
    actions = []
    al = re.search(r'<ul class="action-list">(.*?)</ul>', pub, re.DOTALL)
    if al:
        for li_content in re.findall(r'<li>(.*?)</li>', al.group(1), re.DOTALL):
            tm = re.search(r'<strong>(.*?)</strong>', li_content, re.DOTALL)
            paras = re.findall(r'<p(?:\s+class="([^"]*)")?>(.*?)</p>', li_content, re.DOTALL)
            action = {}
            if tm: action['title'] = clean(tm.group(1))
            for cls, txt in paras:
                if cls == 'safety-note':
                    action['safety_note'] = clean(txt)
                elif 'explanation' not in action:
                    action['explanation'] = clean(txt)
            if action.get('title'): actions.append(action)
    if actions: result['x_safety_actions'] = actions
    
    return tid, result


# ── PHASE 1: Extract from HTML ──────────────────────────────────────
print("=" * 65)
print("TFA STIX Public Content Injection")
print("=" * 65)
print(f"\nSource:  {TECHNIQUES_DIR}")
print(f"Target:  {STIX_PATH}")
print(f"Backup:  {BACKUP_PATH}\n")

extractions = {}
errors = []

for dirname in sorted(os.listdir(TECHNIQUES_DIR)):
    if not dirname.startswith('TFA-T-'):
        continue
    filepath = os.path.join(TECHNIQUES_DIR, dirname, 'index.html')
    if not os.path.exists(filepath):
        errors.append(f"missing: {dirname}")
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tid, data = extract_public(content)
        if tid and data and data.get('x_public_title'):
            extractions[tid] = data
            s = len(data.get('x_recognition_signals', []))
            a = len(data.get('x_safety_actions', []))
            w = ' \u26a0' if 'x_safety_warning' in data else ''
            print(f"  \u2713 {tid}: {data['x_public_title'][:42]:42s} | {s}s {a}a{w}")
        else:
            errors.append(f"no-public-content: {dirname}")
    except Exception as e:
        errors.append(f"{dirname}: {e}")

print(f"\n  Extracted: {len(extractions)}/74 techniques")

if errors:
    print(f"\n  Errors ({len(errors)}):")
    for e in errors:
        print(f"    \u2717 {e}")

if len(extractions) < 70:
    print(f"\n  ABORT: Too few extractions ({len(extractions)}). Expected ~74.")
    exit(1)


# ── PHASE 2: Backup STIX bundle ─────────────────────────────────────
print(f"\n{'─' * 65}")
print("Creating backup...")
shutil.copy2(STIX_PATH, BACKUP_PATH)
print(f"  Backup: {BACKUP_PATH}")


# ── PHASE 3: Inject into STIX ───────────────────────────────────────
print(f"\n{'─' * 65}")
print("Injecting public content into STIX bundle...")

with open(STIX_PATH, 'r') as f:
    bundle = json.load(f)

injected = 0
not_found = []

for obj in bundle.get('objects', []):
    if obj.get('type') != 'attack-pattern':
        continue
    
    # Find technique ID
    ext_id = None
    for ref in obj.get('external_references', []):
        if ref.get('source_name') == 'not-a-standard-tfa' and ref.get('external_id', '').startswith('TFA-T-'):
            ext_id = ref['external_id']
            break
    
    if not ext_id:
        continue
    
    if ext_id not in extractions:
        not_found.append(ext_id)
        continue
    
    # Inject all public fields
    data = extractions[ext_id]
    for key, value in data.items():
        obj[key] = value
    
    injected += 1

# Write updated bundle
with open(STIX_PATH, 'w') as f:
    json.dump(bundle, f, indent=2, ensure_ascii=False)

print(f"\n  Injected: {injected}/74 attack-pattern objects")
if not_found:
    print(f"  Not matched: {not_found}")


# ── PHASE 4: Verify ─────────────────────────────────────────────────
print(f"\n{'─' * 65}")
print("Verification...")

with open(STIX_PATH, 'r') as f:
    verify = json.load(f)

has_public = 0
missing_public = []
for obj in verify.get('objects', []):
    if obj.get('type') != 'attack-pattern':
        continue
    if obj.get('x_public_title'):
        has_public += 1
    else:
        for ref in obj.get('external_references', []):
            if ref.get('external_id', '').startswith('TFA-T-'):
                missing_public.append(ref['external_id'])

print(f"  Techniques with public content: {has_public}/74")
if missing_public:
    print(f"  Missing public content: {missing_public}")

# Sample verification
sample = None
for obj in verify.get('objects', []):
    if obj.get('type') == 'attack-pattern' and obj.get('x_public_title'):
        sample = obj
        break

if sample:
    ext_id = None
    for ref in sample.get('external_references', []):
        if ref.get('external_id', '').startswith('TFA-T-'):
            ext_id = ref['external_id']
    print(f"\n  Sample ({ext_id}):")
    print(f"    Title:    {sample.get('x_public_title')}")
    print(f"    Summary:  {sample.get('x_public_description', '')[:80]}...")
    print(f"    Signals:  {len(sample.get('x_recognition_signals', []))}")
    print(f"    Actions:  {len(sample.get('x_safety_actions', []))}")
    print(f"    Warning:  {'Yes' if sample.get('x_safety_warning') else 'No'}")

print(f"\n{'=' * 65}")
print("DONE. Updated: tfa-attack.json")
print(f"{'=' * 65}")
