#!/usr/bin/env python3
"""
Inject mobile quick exit bar into all TFA Matrix HTML pages.

This adds a sticky quick exit bar that appears on mobile only,
positioned below the header navigation.

Usage:
    python3 inject_quick_exit_bar.py
"""

import os
import re

# The HTML to inject — goes right after </nav> closing tag
QUICK_EXIT_BAR_HTML = '''
                <!-- Mobile Quick Exit Bar - visible on mobile only -->
                <div class="quick-exit-bar">
                    <a href="https://doodles.google" id="quick-exit-mobile" title="Press Escape to quickly leave this site">⚡ Quick Exit</a>
                </div>'''

# Pattern to find the </nav> closing tag (after the header nav)
# We want to insert after </nav> but still within <header>
NAV_CLOSE_PATTERN = r'(</nav>\s*\n)(\s*</header>)'

def inject_quick_exit_bar(html_content):
    """Inject the quick exit bar HTML after </nav> tag."""
    
    # Check if already injected
    if 'quick-exit-bar' in html_content:
        return html_content, False
    
    # Find and replace
    replacement = r'\1' + QUICK_EXIT_BAR_HTML + r'\n\2'
    new_content, count = re.subn(NAV_CLOSE_PATTERN, replacement, html_content)
    
    return new_content, count > 0


def process_directory(base_dir):
    """Process all HTML files in directory tree."""
    modified_count = 0
    skipped_count = 0
    error_count = 0
    
    for root, dirs, files in os.walk(base_dir):
        # Skip node_modules, .git, etc.
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '__pycache__']
        
        for filename in files:
            if not filename.endswith('.html'):
                continue
            
            filepath = os.path.join(root, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content, was_modified = inject_quick_exit_bar(content)
                
                if was_modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✓ Modified: {filepath}")
                    modified_count += 1
                else:
                    skipped_count += 1
                    
            except Exception as e:
                print(f"✗ Error processing {filepath}: {e}")
                error_count += 1
    
    return modified_count, skipped_count, error_count


def main():
    import sys
    
    # Default to current directory's tfa-matrix folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if not base_dir.endswith('tfa-matrix'):
        base_dir = os.path.join(base_dir, 'tfa-matrix')
    
    # Allow override via command line
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    
    print(f"Injecting mobile quick exit bar into HTML files...")
    print(f"Base directory: {base_dir}\n")
    
    modified, skipped, errors = process_directory(base_dir)
    
    print(f"\n{'='*50}")
    print(f"Results:")
    print(f"  Modified: {modified} files")
    print(f"  Skipped (already had bar or no nav): {skipped} files")
    print(f"  Errors: {errors} files")
    
    if modified > 0:
        print(f"\n✓ Done! The mobile quick exit bar has been added.")
        print(f"  CSS is already in theme/style-user.css")
        print(f"  Test by viewing the site at mobile viewport width.")


if __name__ == "__main__":
    main()
