#!/usr/bin/env python3
"""
Update mitigations and detections sections in technical view.
Replaces "COMING SOON" with actual content from technique_data.py.
"""

import re
from pathlib import Path
from technique_data import TECHNIQUE_DATA

BASE_DIR = Path(__file__).parent
OUTPUT_TECHNIQUES_DIR = BASE_DIR / "output" / "techniques"
TECHNIQUES_DIR = BASE_DIR / "techniques"


def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ''
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def generate_mitigations_html(technique_id):
    """Generate mitigations table HTML."""
    data = TECHNIQUE_DATA.get(technique_id, {})
    mitigations = data.get('mitigations', [])

    if not mitigations:
        return '<p>No mitigations documented for this technique.</p>'

    rows = []
    for mid, name, desc in mitigations:
        rows.append(f'''                                <tr>
                                    <td><strong>{escape_html(mid)}</strong></td>
                                    <td><strong>{escape_html(name)}</strong><br>{escape_html(desc)}</td>
                                </tr>''')

    return f'''<table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th style="width: 120px;">ID</th>
                                        <th>Mitigation</th>
                                    </tr>
                                </thead>
                                <tbody>
{chr(10).join(rows)}
                                </tbody>
                            </table>'''


def generate_detections_html(technique_id):
    """Generate detections table HTML."""
    data = TECHNIQUE_DATA.get(technique_id, {})
    detections = data.get('detections', [])

    if not detections:
        return ''

    rows = []
    for did, name, desc in detections:
        rows.append(f'''                                <tr>
                                    <td><strong>{escape_html(did)}</strong></td>
                                    <td><strong>{escape_html(name)}</strong><br>{escape_html(desc)}</td>
                                </tr>''')

    return f'''<h2 class="pt-3" id="detections">Detection Indicators</h2>
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th style="width: 120px;">ID</th>
                                        <th>Detection Indicator</th>
                                    </tr>
                                </thead>
                                <tbody>
{chr(10).join(rows)}
                                </tbody>
                            </table>'''


def update_technique_page(html_path, technique_id):
    """Update a technique page with actual mitigations/detections."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if already has table (already updated)
    if 'table-bordered' in html and 'TFA-M-' in html:
        print(f"  Skipping {technique_id} (already has mitigations)")
        return False

    # Find and replace COMING SOON in mitigations
    # Note: id ="mitigations" has a space before = in the actual HTML
    coming_soon_pattern = r'(<h2[^>]*id\s*=\s*["\']?mitigations["\']?[^>]*>Mitigations</h2>\s*)<p>\s*COMING SOON![^<]*<a[^>]*>[^<]*</a>[^<]*</p>'

    mitigations_html = generate_mitigations_html(technique_id)
    detections_html = generate_detections_html(technique_id)

    replacement = r'\1' + mitigations_html
    if detections_html:
        replacement += '\n' + detections_html

    new_html, count = re.subn(coming_soon_pattern, replacement, html, flags=re.IGNORECASE | re.DOTALL)

    if count == 0:
        # Try alternate pattern without "COMING SOON"
        alt_pattern = r'(<h2[^>]*id\s*=\s*["\']?mitigations["\']?[^>]*>Mitigations</h2>\s*<p>)[^<]*(</p>)'
        new_html, count = re.subn(alt_pattern, r'\1' + mitigations_html + r'\2', html, flags=re.IGNORECASE | re.DOTALL)

    if count == 0:
        print(f"  Warning: Could not find mitigations section in {technique_id}")
        return False

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"  Updated {technique_id}")
    return True


def main():
    print("Updating mitigations and detections...")
    updated = 0

    for tech_dir in [OUTPUT_TECHNIQUES_DIR, TECHNIQUES_DIR]:
        if not tech_dir.exists():
            continue
        print(f"\nProcessing {tech_dir}...")
        for subdir in sorted(tech_dir.iterdir()):
            if subdir.is_dir() and subdir.name.startswith('TFA-T-'):
                html_path = subdir / 'index.html'
                if html_path.exists():
                    if update_technique_page(html_path, subdir.name):
                        updated += 1

    print(f"\nDone! Updated {updated} pages.")


if __name__ == '__main__':
    main()
