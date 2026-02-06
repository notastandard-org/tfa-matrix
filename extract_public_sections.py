#!/usr/bin/env python3
"""Extract view-public HTML sections from all technique pages into a single JSON file."""
import os, re, json, html as html_mod

TECHNIQUES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'techniques')
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public_extractions.json')

def clean(text):
    if not text: return text
    text = html_mod.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('\u26a0', '').strip()
    return re.sub(r'\s+', ' ', text)

def extract(html_content):
    result = {}
    id_m = re.search(r'<span class="h5 card-title">ID:&nbsp;</span>(TFA-T-\d+)', html_content)
    if not id_m: return None, None
    tid = id_m.group(1)
    
    pub_m = re.search(r'<div class="view-public">(.*?)<div class="public-disclaimer">', html_content, re.DOTALL)
    if not pub_m: return tid, None
    pub = pub_m.group(1)
    
    h1 = re.search(r'<h1>(.*?)</h1>', pub, re.DOTALL)
    if h1: result['x_public_title'] = clean(h1.group(1))
    
    summ = re.search(r'<p class="public-summary">(.*?)</p>', pub, re.DOTALL)
    if summ: result['x_public_description'] = clean(summ.group(1))
    
    warn = re.search(r'<div class="safety-warning">(.*?)</div>', pub, re.DOTALL)
    if warn:
        wt = clean(warn.group(1))
        if wt: result['x_safety_warning'] = wt
    
    signals = []
    nl = re.search(r'<ul class="notice-list">(.*?)</ul>', pub, re.DOTALL)
    if nl:
        for t, e in re.findall(r'<li>\s*<strong>(.*?)</strong>\s*<p>(.*?)</p>', nl.group(1), re.DOTALL):
            signals.append({'title': clean(t), 'explanation': clean(e)})
    if signals: result['x_recognition_signals'] = signals
    
    actions = []
    al = re.search(r'<ul class="action-list">(.*?)</ul>', pub, re.DOTALL)
    if al:
        for li in re.findall(r'<li>(.*?)</li>', al.group(1), re.DOTALL):
            tm = re.search(r'<strong>(.*?)</strong>', li, re.DOTALL)
            paras = re.findall(r'<p(?:\s+class="([^"]*)")?>(.*?)</p>', li, re.DOTALL)
            a = {}
            if tm: a['title'] = clean(tm.group(1))
            for cls, txt in paras:
                if cls == 'safety-note': a['safety_note'] = clean(txt)
                elif 'explanation' not in a: a['explanation'] = clean(txt)
            if a.get('title'): actions.append(a)
    if actions: result['x_safety_actions'] = actions
    
    return tid, result

results = {}
errors = []
for d in sorted(os.listdir(TECHNIQUES_DIR)):
    if not d.startswith('TFA-T-'): continue
    fp = os.path.join(TECHNIQUES_DIR, d, 'index.html')
    if not os.path.exists(fp):
        errors.append(d)
        continue
    try:
        with open(fp) as f: content = f.read()
        tid, data = extract(content)
        if tid and data:
            results[tid] = data
            s = len(data.get('x_recognition_signals', []))
            a = len(data.get('x_safety_actions', []))
            w = ' \u26a0' if 'x_safety_warning' in data else ''
            print(f"  \u2713 {tid}: {data.get('x_public_title','?')[:45]:45s} | {s}s {a}a{w}")
        else:
            errors.append(f"no-public:{d}")
    except Exception as e:
        errors.append(f"{d}:{e}")

with open(OUTPUT, 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"Extracted: {len(results)}/74 techniques -> {OUTPUT}")
if errors: 
    print(f"Errors: {errors}")
print(f"{'='*60}")
