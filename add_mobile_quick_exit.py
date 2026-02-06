#!/usr/bin/env python3
"""
Add mobile quick exit bar after </nav> in all HTML files.
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent

QUICK_EXIT_BAR = '''
    <div class="quick-exit-bar">
        <a href="https://doodles.google" id="quick-exit-mobile" title="Press Escape to quickly leave this site">⚡ Quick Exit</a>
    </div>
'''


def add_quick_exit_bar(filepath):
    """Add quick exit bar after </nav> if not already present."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has quick-exit-bar
    if 'quick-exit-bar' in content:
        return False

    # Skip if no </nav> tag
    if '</nav>' not in content:
        return False

    # Insert after </nav>
    content = content.replace('</nav>\n', '</nav>' + QUICK_EXIT_BAR)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    print("Adding mobile quick exit bar to all HTML files...\n")
    updated = 0

    for html_file in BASE_DIR.rglob('*.html'):
        # Skip node_modules, etc.
        if 'node_modules' in str(html_file):
            continue
        if add_quick_exit_bar(html_file):
            print(f"  Updated: {html_file.relative_to(BASE_DIR)}")
            updated += 1

    print(f"\nDone! Updated {updated} files.")


if __name__ == '__main__':
    main()
