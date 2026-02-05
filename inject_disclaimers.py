#!/usr/bin/env python3
"""
Inject disclaimers into existing technique and tactic pages.
Adds footer disclaimer to .view-public and .view-technical containers.
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_TECHNIQUES_DIR = BASE_DIR / "output" / "techniques"
OUTPUT_TACTICS_DIR = BASE_DIR / "output" / "tactics"
TECHNIQUES_DIR = BASE_DIR / "techniques"
TACTICS_DIR = BASE_DIR / "tactics"
OUTPUT_MATRIX_PATH = BASE_DIR / "output" / "matrices" / "tfa" / "index.html"
MATRIX_PATH = BASE_DIR / "matrices" / "tfa" / "index.html"

PUBLIC_DISCLAIMER = '''<div class="public-disclaimer">
                                        <p><strong>Important:</strong> This information is general in nature and does not constitute personal, legal, or clinical advice. Every situation is different. Actions that are safe for one person may not be safe for another — especially if the person causing harm may escalate when they notice changes. If you're unsure, speak with a specialist service before making changes to your devices or accounts.</p>
                                        <p><a href="/about/limitations/">Read our full disclaimer</a></p>
                                    </div>'''

TECHNICAL_DISCLAIMER = '''<div class="technical-disclaimer">
                                <p><strong>Framework Limitations:</strong> This framework is provided for informational purposes. It is not forensic methodology, legal advice, or clinical guidance. Detection indicators identify possible signs, not evidence. Mitigation descriptions are not step-by-step instructions. <a href="/about/limitations/">Full limitations and methodology</a>.</p>
                            </div>'''

MATRIX_DISCLAIMER = '''<div class="matrix-disclaimer view-public">
                            <p><strong>Important:</strong> This matrix shows patterns of technology-facilitated abuse. The information is general in nature and does not constitute personal advice. If you recognise something that's happening to you and want to take action, please contact a specialist service first — some responses may alert the person causing harm. <a href="/about/limitations/">Read our full disclaimer</a>. Need support? <a href="tel:1800737732">1800RESPECT (1800 737 732)</a></p>
                        </div>'''


def inject_public_disclaimer(html):
    """Inject public disclaimer before closing </div> of .view-public."""
    # Check if already has disclaimer
    if 'public-disclaimer' in html:
        return html, False

    # Find the closing </div> of .view-public - it's right before <div class="view-technical"
    pattern = r'(</ul>\s*)(</div>\s*<div class="view-technical")'

    replacement = r'\1' + PUBLIC_DISCLAIMER + r'\n                                \2'
    new_html, count = re.subn(pattern, replacement, html)

    if count == 0:
        # Try alternate pattern - look for end of action-list before view-technical
        pattern2 = r'(</div>)(\s*<div class="view-technical")'
        new_html, count = re.subn(pattern2, PUBLIC_DISCLAIMER + r'\n                            \1\2', html, count=1)

    return new_html, count > 0


def inject_technical_disclaimer(html):
    """Inject technical disclaimer before closing </div><!-- end view-technical -->."""
    # Check if already has disclaimer
    if 'technical-disclaimer' in html:
        return html, False

    # Find the closing marker for view-technical
    pattern = r'(\s*)(</div><!-- end view-technical -->)'

    replacement = r'\n' + TECHNICAL_DISCLAIMER + r'\n                            \2'
    new_html, count = re.subn(pattern, replacement, html, count=1)

    return new_html, count > 0


def process_technique_page(html_path):
    """Process a single technique page to add disclaimers."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if not processed with dual views
    if 'view-toggle-container' not in html:
        print(f"  Skipping {html_path.parent.name} (no dual views)")
        return False

    modified = False

    # Inject public disclaimer
    html, pub_changed = inject_public_disclaimer(html)
    if pub_changed:
        modified = True

    # Inject technical disclaimer
    html, tech_changed = inject_technical_disclaimer(html)
    if tech_changed:
        modified = True

    if modified:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Updated {html_path.parent.name}")
        return True
    else:
        print(f"  Skipping {html_path.parent.name} (already has disclaimers)")
        return False


def process_tactic_page(html_path):
    """Process a single tactic page to add disclaimers."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if not processed with dual views
    if 'view-toggle-container' not in html:
        print(f"  Skipping {html_path.parent.name} (no dual views)")
        return False

    # For tactics, the structure is simpler
    modified = False

    # Check for public disclaimer
    if 'public-disclaimer' not in html:
        # Find end of .view-public (before .view-technical)
        pattern = r'(</p>\s*)(</div>\s*<div class="view-technical")'
        replacement = r'\1' + PUBLIC_DISCLAIMER + r'\n                                \2'
        html, count = re.subn(pattern, replacement, html, count=1)
        if count > 0:
            modified = True

    # Check for technical disclaimer
    if 'technical-disclaimer' not in html:
        pattern = r'(\s*)(</div><!-- end view-technical -->)'
        replacement = r'\n' + TECHNICAL_DISCLAIMER + r'\n                            \2'
        html, count = re.subn(pattern, replacement, html, count=1)
        if count > 0:
            modified = True

    if modified:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Updated tactic {html_path.parent.name}")
        return True
    else:
        print(f"  Skipping tactic {html_path.parent.name} (already has disclaimers)")
        return False


def process_matrix_page(matrix_path):
    """Add matrix disclaimer to the matrix page."""
    if not matrix_path.exists():
        print(f"  Matrix not found: {matrix_path}")
        return False

    with open(matrix_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already has disclaimer
    if 'matrix-disclaimer' in html:
        print(f"  Skipping matrix (already has disclaimer)")
        return False

    # Find the toggle container and insert disclaimer after it
    pattern = r'(</div>\s*)(<!-- matrix container|<div class="row".*?overflow-x-auto)'

    def add_disclaimer(match):
        return match.group(1) + MATRIX_DISCLAIMER + '\n                    ' + match.group(2)

    new_html, count = re.subn(pattern, add_disclaimer, html, count=1)

    if count == 0:
        # Try alternate approach - after view-toggle-container
        toggle_end = html.find('</div>', html.find('view-toggle-container'))
        if toggle_end != -1:
            insert_pos = toggle_end + len('</div>')
            new_html = html[:insert_pos] + '\n' + MATRIX_DISCLAIMER + html[insert_pos:]
            count = 1

    if count > 0:
        with open(matrix_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"  Updated matrix: {matrix_path}")
        return True
    else:
        print(f"  Could not find insertion point in matrix")
        return False


def main():
    print("Injecting disclaimers into pages...\n")
    updated = 0

    # Process technique pages
    print("Processing technique pages in output/...")
    if OUTPUT_TECHNIQUES_DIR.exists():
        for tech_dir in sorted(OUTPUT_TECHNIQUES_DIR.iterdir()):
            if tech_dir.is_dir() and tech_dir.name.startswith('TFA-T-'):
                html_path = tech_dir / 'index.html'
                if html_path.exists():
                    if process_technique_page(html_path):
                        updated += 1

    print("\nProcessing technique pages in techniques/...")
    if TECHNIQUES_DIR.exists():
        for tech_dir in sorted(TECHNIQUES_DIR.iterdir()):
            if tech_dir.is_dir() and tech_dir.name.startswith('TFA-T-'):
                html_path = tech_dir / 'index.html'
                if html_path.exists():
                    if process_technique_page(html_path):
                        updated += 1

    # Process tactic pages
    print("\nProcessing tactic pages...")
    for tactics_dir in [OUTPUT_TACTICS_DIR, TACTICS_DIR]:
        if tactics_dir.exists():
            for tactic_dir in sorted(tactics_dir.iterdir()):
                if tactic_dir.is_dir() and tactic_dir.name.startswith('TFA-TA-'):
                    html_path = tactic_dir / 'index.html'
                    if html_path.exists():
                        if process_tactic_page(html_path):
                            updated += 1

    # Process matrix pages
    print("\nProcessing matrix pages...")
    for matrix_path in [OUTPUT_MATRIX_PATH, MATRIX_PATH]:
        if process_matrix_page(matrix_path):
            updated += 1

    print(f"\nDone! Updated {updated} pages.")


if __name__ == '__main__':
    main()
