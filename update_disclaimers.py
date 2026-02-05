#!/usr/bin/env python3
"""
Update disclaimers to match the revised brief.
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Old disclaimer patterns
OLD_PUBLIC = r'<div class="public-disclaimer">.*?</div>'
OLD_TECHNICAL = r'<div class="technical-disclaimer">.*?</div>'
OLD_MATRIX = r'<div class="matrix-disclaimer view-public">.*?</div>'

# New disclaimers from the updated brief
NEW_PUBLIC = '''<div class="public-disclaimer">
                                        <p><strong>Important:</strong> This resource provides general information, not personal advice. Every situation is different. The actions suggested here may not be safe in your specific circumstances — particularly if the person causing harm could notice changes to your devices or accounts. <strong>Always consider your physical safety first.</strong></p>
                                        <p>If you need personalised support, contact <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> or your local specialist domestic violence service. If you are in immediate danger, call <a href="tel:000">000</a>.</p>
                                        <p>This framework is under active development. <a href="/about/limitations/">View full limitations &amp; methodology</a>.</p>
                                    </div>'''

NEW_TECHNICAL = '''<div class="technical-disclaimer">
                                <p>The TFA Matrix is a research framework under active development. Technique classifications, detection methods, and mitigations reflect current understanding and are subject to revision. This framework does not constitute forensic methodology, legal evidence standards, or clinical diagnostic criteria. Practitioners should apply professional judgement appropriate to their discipline and jurisdiction.</p>
                                <p><a href="/about/limitations/">Full limitations, methodology &amp; responsible use statement</a>.</p>
                            </div>'''

NEW_MATRIX = '''<div class="matrix-disclaimer view-public">
                            <p>This matrix shows known patterns of technology-facilitated abuse. It is not a complete list — new techniques emerge as technology changes. Click any technique for guidance on what to notice and what you can do.</p>
                            <p>Need support? <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> | Emergency: <a href="tel:000">000</a> | <a href="/about/limitations/">Limitations &amp; methodology</a></p>
                        </div>'''


def update_file(filepath):
    """Update disclaimers in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace public disclaimer
    content = re.sub(OLD_PUBLIC, NEW_PUBLIC, content, flags=re.DOTALL)

    # Replace technical disclaimer
    content = re.sub(OLD_TECHNICAL, NEW_TECHNICAL, content, flags=re.DOTALL)

    # Replace matrix disclaimer
    content = re.sub(OLD_MATRIX, NEW_MATRIX, content, flags=re.DOTALL)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("Updating disclaimers to match revised brief...\n")
    updated = 0

    # Find all HTML files
    for html_file in BASE_DIR.rglob("*.html"):
        if update_file(html_file):
            print(f"  Updated: {html_file.relative_to(BASE_DIR)}")
            updated += 1

    print(f"\nDone! Updated {updated} files.")


if __name__ == '__main__':
    main()
