# TFA Site Fix — Claude Code Follow-Up Briefing

## The Problem

You updated the STIX bundle correctly (all SAFE IDs, MITRE compat, etc.) and created redirects at old TFA-T-XXXX URLs. But you replaced the original technique HTML pages with redirect stubs, and NEVER created actual pages at the new SAFE-T-XXXX URLs. Every technique page on the site now 404s.

## Why generate_public_pages.py Won't Help

That script INJECTS public content into EXISTING HTML pages that Pelican generated. It doesn't create pages from scratch. The original Pelican-generated HTML no longer exists — you overwrote it with redirects. Running generate_public_pages.py now would find nothing to inject into.

## What You Must Do

### Step 1: Git restore the original technique pages

The original HTML pages (with full dual-view public/technical content) exist in the git history. Restore them:

```bash
cd /Users/emilyholyoake/Desktop/SAFE/tfa-matrix

# Restore all technique pages from the commit BEFORE your migration
git log --oneline -5  # find the commit hash before your changes
git checkout <COMMIT_BEFORE_MIGRATION> -- techniques/
git checkout <COMMIT_BEFORE_MIGRATION> -- tactics/
git checkout <COMMIT_BEFORE_MIGRATION> -- matrices/
```

### Step 2: Create SAFE-T-XXXX directories and copy pages

For each technique, copy the restored HTML to the new SAFE ID directory:

```python
import json, shutil, os

# Load the ID map
with open('/Users/emilyholyoake/Desktop/SAFE/safe-platform/src/data/tfa-to-safe-id-map.json') as f:
    id_map = json.load(f)

base = '/Users/emilyholyoake/Desktop/SAFE/tfa-matrix/techniques'

for tfa_id, safe_id in id_map['techniques'].items():
    if '.' in tfa_id:  # skip sub-techniques for now
        continue
    src = os.path.join(base, tfa_id)
    dst = os.path.join(base, safe_id)
    if os.path.exists(src) and os.path.isdir(src):
        # Copy the full technique page to the new SAFE ID directory
        shutil.copytree(src, dst, dirs_exist_ok=True)
```

Do the same for tactics:
```python
tactics_base = '/Users/emilyholyoake/Desktop/SAFE/tfa-matrix/tactics'
for tfa_id, safe_id in id_map['tactics'].items():
    src = os.path.join(tactics_base, tfa_id)
    dst = os.path.join(tactics_base, safe_id)
    if os.path.exists(src) and os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
```

### Step 3: Update all IDs inside the copied HTML pages

Within each SAFE-T-XXXX/index.html, replace TFA IDs with SAFE IDs:

```python
import re

for tfa_id, safe_id in id_map['techniques'].items():
    if '.' in tfa_id:
        continue
    html_path = os.path.join(base, safe_id, 'index.html')
    if not os.path.exists(html_path):
        continue
    
    with open(html_path, 'r') as f:
        html = f.read()
    
    # Replace this technique's own ID everywhere
    html = html.replace(tfa_id, safe_id)
    
    # Replace all OTHER TFA IDs that appear (in links, references, etc.)
    for other_tfa, other_safe in id_map['techniques'].items():
        if '.' not in other_tfa:
            html = html.replace(other_tfa, other_safe)
    
    # Replace tactic IDs
    for tfa_ta, safe_ta in id_map['tactics'].items():
        html = html.replace(tfa_ta, safe_ta)
    
    # Replace mitigation IDs
    for tfa_m, safe_m in id_map['courses_of_action'].items():
        html = html.replace(tfa_m, safe_m)
    
    # Replace detection IDs
    for tfa_d, safe_d in id_map['detections'].items():
        html = html.replace(tfa_d, safe_d)
    
    # Replace extension property prefixes in any inline data
    html = html.replace('x_tfa_', 'x_safe_')
    
    # Fix page title to show SAFE ID
    html = html.replace(f'<title>{tfa_id}', f'<title>{safe_id}')
    
    with open(html_path, 'w') as f:
        f.write(html)
```

Do the same for tactic pages. Do the same for the matrix page.

### Step 4: Put redirects back at old TFA paths

The original TFA-T-XXXX directories now have the restored HTML (from step 1). Replace those with redirect stubs again:

```python
redirect_template = '''<!DOCTYPE html><html><head>
<meta http-equiv="refresh" content="0; url=/techniques/{safe_id}/">
<link rel="canonical" href="/techniques/{safe_id}/">
<title>Redirecting to {safe_id}</title>
</head><body>
<p>This technique has moved to <a href="/techniques/{safe_id}/">{safe_id}</a></p>
</body></html>'''

for tfa_id, safe_id in id_map['techniques'].items():
    if '.' in tfa_id:
        continue
    redirect_path = os.path.join(base, tfa_id, 'index.html')
    os.makedirs(os.path.dirname(redirect_path), exist_ok=True)
    with open(redirect_path, 'w') as f:
        f.write(redirect_template.format(safe_id=safe_id))
```

Same for tactics.

### Step 5: Update the matrix page

The matrix page at `/matrices/tfa/index.html` has:
- `data-public-title` attributes on technique cells
- `href="/techniques/TFA-T-XXXX"` links

All of these need updating to SAFE IDs. Apply the same find-and-replace as step 3.

### Step 6: Update generate_public_pages.py

This script will be needed for future updates. Change:

```python
# Old:
EXT_ID = "extension-definition--acf2f380-0000-4000-8000-000000000001"
# New:
EXT_ID = "extension-definition--acf2f380-0000-4000-8000-000000000002"

# Old: all references to x_tfa_
# New: all references to x_safe_

# Old: directory matching TFA-T-
# New: directory matching SAFE-T-

# Old: tactic matching TFA-TA-
# New: tactic matching SAFE-TA-
```

### Step 7: Update other injection scripts

Check and update these scripts for SAFE IDs:
- inject_disclaimers.py
- inject_quick_exit_bar.py
- add_mobile_quick_exit.py
- create_legal_pages.py
- integrate_stix_mitigations.py
- update_disclaimers.py
- update_mitigations.py
- technique_data.py

### Step 8: Verify

1. Visit /techniques/SAFE-T-0072/ — should show full technique page with public/technical views
2. Visit /techniques/TFA-T-1001/ — should redirect to SAFE-T-0072
3. Visit /tactics/SAFE-TA-0001/ — should show tactic page
4. Visit /matrices/tfa/ — matrix should render with correct links
5. View toggle should work (public/technical switch)
6. Safety banner, quick exit, helpline — all present
7. All 74 technique pages accessible at SAFE-T-XXXX URLs
8. All 74 old TFA-T-XXXX URLs redirect correctly

## Execution Order

1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

Do NOT skip step 1. Without restoring the originals from git, there is no HTML to work with.

## What NOT to Do

- Do NOT try to generate pages from scratch — the Pelican templates don't have the customisations
- Do NOT run the Pelican build — it would overwrite everything with stock MITRE templates
- Do NOT modify the STIX bundle — it's correct
- Do NOT touch the GitHub Actions workflow — it's disabled for a reason
