#!/usr/bin/env python3
"""
Generate dual-view technique and tactic pages for TFA Matrix.

This script reads the STIX bundle to generate HTML pages with both
Technical (ATT&CK-style) and Public (victim-friendly) views embedded.
Public view is shown by default - victims are the primary audience.
"""

import json
import os
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
STIX_PATH = BASE_DIR / "stix" / "tfa-attack.json"
OUTPUT_TECHNIQUES_DIR = BASE_DIR / "output" / "techniques"
OUTPUT_TACTICS_DIR = BASE_DIR / "output" / "tactics"
OUTPUT_MATRIX_PATH = BASE_DIR / "output" / "matrices" / "tfa" / "index.html"
TECHNIQUES_DIR = BASE_DIR / "techniques"
TACTICS_DIR = BASE_DIR / "tactics"
MATRIX_PATH = BASE_DIR / "matrices" / "tfa" / "index.html"

# Extension ID for TFA properties
EXT_ID = "extension-definition--acf2f380-0000-4000-8000-000000000001"


def load_stix_bundle():
    """Load and parse the STIX bundle."""
    with open(STIX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_techniques(stix_data):
    """Extract technique objects indexed by TFA ID."""
    techniques = {}
    for obj in stix_data.get('objects', []):
        if obj.get('type') == 'attack-pattern':
            ext = obj.get('extensions', {}).get(EXT_ID, {})
            tfa_id = ext.get('x_tfa_technique_id')
            if tfa_id:
                techniques[tfa_id] = {
                    'name': obj.get('name', ''),
                    'description': obj.get('description', ''),
                    'public_title': ext.get('x_tfa_public_title', ''),
                    'public_summary': ext.get('x_tfa_public_summary', ''),
                    'safety_warning': ext.get('x_tfa_public_safety_warning'),
                    'notices': ext.get('x_tfa_public_notices', []),
                    'actions': ext.get('x_tfa_public_actions', []),
                }
    return techniques


def get_tactics(stix_data):
    """Extract tactic objects indexed by TFA ID."""
    tactics = {}
    for obj in stix_data.get('objects', []):
        if obj.get('type') == 'x-mitre-tactic':
            ext = obj.get('extensions', {}).get(EXT_ID, {})
            tfa_id = ext.get('x_tfa_tactic_id')
            if tfa_id:
                tactics[tfa_id] = {
                    'name': obj.get('name', ''),
                    'description': obj.get('description', ''),
                    'public_name': ext.get('x_tfa_public_name', ''),
                    'public_intro': ext.get('x_tfa_public_intro', ''),
                    'public_safety': ext.get('x_tfa_public_safety', ''),
                }
    return tactics


def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ''
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def generate_helpline_banner():
    """Generate the helpline banner HTML."""
    return '''<div class="helpline-banner">
                                        <strong>Need support?</strong>
                                        <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> |
                                        Emergency: <a href="tel:000">000</a>
                                    </div>'''


def generate_safety_warning(warning_text):
    """Generate safety warning HTML if warning exists."""
    if not warning_text:
        return ''
    escaped = escape_html(warning_text)
    return f'''<div class="safety-warning">
                                        <span class="safety-warning-icon">&#9888;</span>
                                        {escaped}
                                    </div>'''


def generate_notices_html(notices):
    """Generate 'What You Might Notice' section."""
    if not notices:
        return ''

    items = []
    for notice in notices:
        signal = escape_html(notice.get('signal', ''))
        detail = escape_html(notice.get('detail', ''))
        items.append(f'''                                        <li>
                                            <strong>{signal}</strong>
                                            <p>{detail}</p>
                                        </li>''')

    return '''<h2>What You Might Notice</h2>
                                    <ul class="notice-list">
''' + '\n'.join(items) + '''
                                    </ul>'''


def generate_actions_html(actions):
    """Generate 'What You Can Do' section."""
    if not actions:
        return ''

    items = []
    for action in actions:
        action_text = escape_html(action.get('action', ''))
        detail = escape_html(action.get('detail', ''))
        safety_note = action.get('safety_note')

        safety_html = ''
        if safety_note:
            safety_escaped = escape_html(safety_note)
            safety_html = f'\n                                            <p class="safety-note">{safety_escaped}</p>'

        items.append(f'''                                        <li>
                                            <strong>{action_text}</strong>
                                            <p>{detail}</p>{safety_html}
                                        </li>''')

    return '''<h2>What You Can Do</h2>
                                    <ul class="action-list">
''' + '\n'.join(items) + '''
                                    </ul>'''


def generate_public_view(technique):
    """Generate complete public view HTML for a technique."""
    public_title = escape_html(technique.get('public_title', '') or technique.get('name', 'Unknown'))
    public_summary = escape_html(technique.get('public_summary', ''))

    return f'''<div class="view-public">
                                    {generate_helpline_banner()}
                                    {generate_safety_warning(technique.get('safety_warning'))}
                                    <h1>{public_title}</h1>
                                    <p class="public-summary">{public_summary}</p>
                                    {generate_notices_html(technique.get('notices', []))}
                                    {generate_actions_html(technique.get('actions', []))}
                                </div>'''


def generate_toggle_html():
    """Generate view toggle buttons."""
    return '''<div class="view-toggle-container" role="group" aria-label="Content view selection">
                        <button class="view-toggle-btn" data-view="technical" aria-pressed="false">Technical View</button>
                        <button class="view-toggle-btn active" data-view="public" aria-pressed="true">Public View</button>
                    </div>'''


def add_script_tag(html_content):
    """Add view-toggle.js script tag if not already present."""
    if 'view-toggle.js' in html_content:
        return html_content

    # Add before closing body tag
    script_tag = '    <script src="/theme/scripts/view-toggle.js"></script>\n'
    return html_content.replace('</body>', script_tag + '</body>')


def process_technique_page(html_path, technique_data):
    """Process a single technique page to add dual views."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already processed
    if 'view-toggle-container' in html:
        print(f"  Skipping {html_path.name} (already processed)")
        return False

    # Find the breadcrumb section and insert toggle after it
    breadcrumb_end = html.find('</ol>')
    if breadcrumb_end == -1:
        print(f"  Error: No breadcrumb found in {html_path}")
        return False

    # Find the next line after breadcrumb close
    insert_after_breadcrumb = html.find('\n', breadcrumb_end) + 1

    # Find jumbotron container-fluid to insert content
    jumbotron_container = html.find('<div class="container-fluid">', insert_after_breadcrumb)
    if jumbotron_container == -1:
        print(f"  Error: No jumbotron container in {html_path}")
        return False

    # Find h1 tag
    h1_start = html.find('<h1', jumbotron_container)
    if h1_start == -1:
        print(f"  Error: No h1 found in {html_path}")
        return False

    # Find the closing div of container-fluid (before the outer jumbotron closing)
    # We need to wrap from h1 to before the closing </div> of container-fluid
    # The structure is: container-fluid > h1, row, h2 mitigations > /div > /div jumbotron

    # Find mitigations section end
    mitigations_start = html.find('<h2', h1_start)
    if mitigations_start == -1:
        mitigations_start = len(html)

    # Find the paragraph after mitigations
    content_end = html.find('</div>\n            </div>\n        </div>', mitigations_start)
    if content_end == -1:
        content_end = html.find('</div>\n            </div>', mitigations_start)
    if content_end == -1:
        print(f"  Error: Could not find content end in {html_path}")
        return False

    # Build new HTML
    # 1. Everything up to after breadcrumb
    # 2. Toggle
    # 3. Everything from breadcrumb to h1
    # 4. Public view
    # 5. Technical view wrapper start
    # 6. Original content from h1 to content_end
    # 7. Technical view wrapper end
    # 8. Rest of HTML

    toggle_html = generate_toggle_html()
    public_view_html = generate_public_view(technique_data)

    new_html = (
        html[:insert_after_breadcrumb] +
        '    ' + toggle_html + '\n' +
        html[insert_after_breadcrumb:h1_start] +
        public_view_html + '\n' +
        '                            <div class="view-technical" style="display: none;">\n' +
        '                            ' + html[h1_start:content_end] +
        '\n                            </div><!-- end view-technical -->' +
        html[content_end:]
    )

    # Add script tag
    new_html = add_script_tag(new_html)

    # Save
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"  Updated {html_path.name}")
    return True


def process_tactic_page(html_path, tactic_data):
    """Process a single tactic page to add dual views."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already processed
    if 'view-toggle-container' in html:
        print(f"  Skipping {html_path.name} (already processed)")
        return False

    # Similar logic to technique pages but with tactic content
    public_name = escape_html(tactic_data.get('public_name', '') or tactic_data.get('name', ''))
    public_intro = escape_html(tactic_data.get('public_intro', ''))
    public_safety = tactic_data.get('public_safety', '')

    # Find breadcrumb
    breadcrumb_end = html.find('</ol>')
    if breadcrumb_end == -1:
        print(f"  Error: No breadcrumb found in {html_path}")
        return False

    insert_after_breadcrumb = html.find('\n', breadcrumb_end) + 1

    # Find h1
    h1_start = html.find('<h1', insert_after_breadcrumb)
    if h1_start == -1:
        print(f"  Error: No h1 found in {html_path}")
        return False

    # Find content end - look for techniques table or end of description
    table_start = html.find('<table', h1_start)
    if table_start == -1:
        table_start = html.find('</div>\n            </div>', h1_start)

    toggle_html = generate_toggle_html()

    public_view_html = f'''<div class="view-public">
                                    {generate_helpline_banner()}
                                    {generate_safety_warning(public_safety) if public_safety else ''}
                                    <h1>{public_name}</h1>
                                    <p class="public-summary">{public_intro}</p>
                                </div>'''

    new_html = (
        html[:insert_after_breadcrumb] +
        '    ' + toggle_html + '\n' +
        html[insert_after_breadcrumb:h1_start] +
        public_view_html + '\n' +
        '                            <div class="view-technical" style="display: none;">\n' +
        '                            ' + html[h1_start:table_start] +
        '\n                            </div><!-- end view-technical -->' +
        html[table_start:]
    )

    # Add script tag
    new_html = add_script_tag(new_html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"  Updated tactic {html_path.parent.name}")
    return True


def process_matrix_page(matrix_path, techniques):
    """Process matrix page to add public titles to technique cells."""
    if not matrix_path.exists():
        print(f"  Matrix page not found: {matrix_path}")
        return False

    with open(matrix_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already processed
    if 'view-toggle.js' in html:
        print(f"  Skipping matrix (already processed)")
        return False

    # Add toggle after breadcrumb
    breadcrumb_end = html.find('</ol>')
    if breadcrumb_end != -1:
        insert_pos = html.find('\n', breadcrumb_end) + 1
        toggle_html = generate_toggle_html()
        html = html[:insert_pos] + '    ' + toggle_html + '\n' + html[insert_pos:]

    # Find technique cells and add data attributes
    # Pattern: <a href="/techniques/TFA-T-XXXX" ...>Title</a> inside technique-cell div
    def replace_cell(match):
        full_div = match.group(1)
        href = match.group(2)
        attrs = match.group(3)
        title = match.group(4)

        # Extract technique ID
        id_match = re.search(r'TFA-T-\d+', href)
        if not id_match:
            return match.group(0)

        tfa_id = id_match.group(0)
        tech = techniques.get(tfa_id)
        if not tech or not tech.get('public_title'):
            return match.group(0)

        public_title = escape_html(tech['public_title'])
        tech_title = escape_html(tech['name'])

        # Add data attributes to the div
        new_div = full_div.replace(
            'class="technique-cell',
            f'data-public-title="{public_title}" data-tech-title="{tech_title}" class="technique-cell'
        )

        # Return with public title (shown by default)
        return f'{new_div}\n    <a href="{href}"{attrs}>{public_title}</a>'

    # Match: <div class="technique-cell ...">...<a href="/techniques/TFA-T-XXXX" ...>Title</a>
    cell_pattern = r'(<div class="technique-cell[^"]*"[^>]*>)\s*<a href="(/techniques/TFA-T-\d+)"([^>]*)>([^<]+)</a>'
    html = re.sub(cell_pattern, replace_cell, html, flags=re.DOTALL)

    # Add script tag
    html = add_script_tag(html)

    with open(matrix_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Updated matrix page: {matrix_path}")
    return True


def main():
    print("Loading STIX bundle...")
    stix_data = load_stix_bundle()

    techniques = get_techniques(stix_data)
    tactics = get_tactics(stix_data)

    print(f"Found {len(techniques)} techniques and {len(tactics)} tactics with public content")

    updated_count = 0

    # Process technique pages in output directory
    print("\nProcessing technique pages in output/...")
    if OUTPUT_TECHNIQUES_DIR.exists():
        for tech_dir in sorted(OUTPUT_TECHNIQUES_DIR.iterdir()):
            if tech_dir.is_dir() and tech_dir.name.startswith('TFA-T-'):
                html_path = tech_dir / 'index.html'
                if html_path.exists():
                    tfa_id = tech_dir.name
                    tech_data = techniques.get(tfa_id)
                    if tech_data:
                        if process_technique_page(html_path, tech_data):
                            updated_count += 1
                    else:
                        print(f"  Warning: No STIX data for {tfa_id}")

    # Process source technique pages
    print("\nProcessing technique pages in techniques/...")
    if TECHNIQUES_DIR.exists():
        for tech_dir in sorted(TECHNIQUES_DIR.iterdir()):
            if tech_dir.is_dir() and tech_dir.name.startswith('TFA-T-'):
                html_path = tech_dir / 'index.html'
                if html_path.exists():
                    tfa_id = tech_dir.name
                    tech_data = techniques.get(tfa_id)
                    if tech_data:
                        if process_technique_page(html_path, tech_data):
                            updated_count += 1

    # Process tactic pages
    print("\nProcessing tactic pages...")
    for tactics_dir in [OUTPUT_TACTICS_DIR, TACTICS_DIR]:
        if tactics_dir.exists():
            for tactic_dir in sorted(tactics_dir.iterdir()):
                if tactic_dir.is_dir() and tactic_dir.name.startswith('TFA-TA-'):
                    html_path = tactic_dir / 'index.html'
                    if html_path.exists():
                        tfa_id = tactic_dir.name
                        tactic_data = tactics.get(tfa_id)
                        if tactic_data:
                            if process_tactic_page(html_path, tactic_data):
                                updated_count += 1

    # Process matrix pages
    print("\nProcessing matrix pages...")
    for matrix_path in [OUTPUT_MATRIX_PATH, MATRIX_PATH]:
        if matrix_path.exists():
            if process_matrix_page(matrix_path, techniques):
                updated_count += 1

    print(f"\nDone! Updated {updated_count} pages.")


if __name__ == '__main__':
    main()
