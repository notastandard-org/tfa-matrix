#!/usr/bin/env python3
"""
Extract public-layer content from TFA Matrix HTML pages and inject into STIX bundle.

Reads: techniques/TFA-T-XXXX/index.html (74 pages)
Updates: tfa-attack.json (STIX 2.1 bundle)

Adds these fields to each attack-pattern object:
  - x_public_title (string)
  - x_public_description (string)
  - x_recognition_signals (array of {title, explanation})
  - x_safety_actions (array of {title, explanation, safety_note?})
  - x_safety_warning (string, optional)

Run from repo root: python3 extract_public_to_stix.py
"""

import json
import os
import re
from html.parser import HTMLParser

# ─── Lightweight HTML content extractor (no external deps) ───

class PublicContentExtractor(HTMLParser):
    """Extract structured public content from a technique page's view-public div."""
    
    def __init__(self):
        super().__init__()
        self.in_view_public = False
        self.depth = 0
        
        # Tracking current element
        self.current_tag = None
        self.current_class = None
        self.tag_stack = []
        
        # Extracted content
        self.public_title = ""
        self.public_summary = ""
        self.safety_warning = ""
        self.notice_items = []
        self.action_items = []
        
        # State tracking
        self.in_notice_list = False
        self.in_action_list = False
        self.in_safety_warning = False
        self.in_h1 = False
        self.in_public_summary = False
        self.in_li = False
        self.in_strong = False
        self.in_p = False
        self.in_safety_note = False
        self.in_disclaimer = False
        
        # Current item being built
        self.current_item_title = ""
        self.current_item_explanation = ""
        self.current_item_safety_note = ""
        
        # Text accumulator
        self.text_buffer = ""
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '')
        
        if 'view-public' in classes:
            self.in_view_public = True
            return
        
        if not self.in_view_public:
            return
            
        if 'public-disclaimer' in classes:
            self.in_disclaimer = True
            return
        
        if self.in_disclaimer:
            return
        
        if 'safety-warning' in classes and tag == 'div':
            self.in_safety_warning = True
            self.text_buffer = ""
            return
        
        if tag == 'h1' and not self.public_title:
            self.in_h1 = True
            self.text_buffer = ""
            return
        
        if 'public-summary' in classes:
            self.in_public_summary = True
            self.text_buffer = ""
            return
        
        if 'notice-list' in classes:
            self.in_notice_list = True
            return
        
        if 'action-list' in classes:
            self.in_action_list = True
            return
        
        if tag == 'li' and (self.in_notice_list or self.in_action_list):
            self.in_li = True
            self.current_item_title = ""
            self.current_item_explanation = ""
            self.current_item_safety_note = ""
            return
        
        if tag == 'strong' and self.in_li:
            self.in_strong = True
            self.text_buffer = ""
            return
        
        if tag == 'p' and self.in_li:
            if 'safety-note' in classes:
                self.in_safety_note = True
            else:
                self.in_p = True
            self.text_buffer = ""
            return
    
    def handle_endtag(self, tag):
        if not self.in_view_public:
            return
        
        if tag == 'div' and self.in_safety_warning:
            self.safety_warning = self.text_buffer.strip()
            # Clean up the warning icon character
            self.safety_warning = re.sub(r'^[⚠\s]+', '', self.safety_warning).strip()
            self.in_safety_warning = False
            return
        
        if tag == 'div' and self.in_disclaimer:
            self.in_disclaimer = False
            return
        
        if tag == 'h1' and self.in_h1:
            self.public_title = self.text_buffer.strip()
            self.in_h1 = False
            return
        
        if tag == 'p' and self.in_public_summary:
            self.public_summary = self.text_buffer.strip()
            self.in_public_summary = False
            return
        
        if tag == 'ul':
            if self.in_notice_list:
                self.in_notice_list = False
            elif self.in_action_list:
                self.in_action_list = False
            return
        
        if tag == 'strong' and self.in_strong:
            self.current_item_title = self.text_buffer.strip()
            self.in_strong = False
            return
        
        if tag == 'p' and self.in_safety_note:
            self.current_item_safety_note = self.text_buffer.strip()
            self.in_safety_note = False
            return
        
        if tag == 'p' and self.in_p:
            # Append to explanation (some items have multiple <p> tags)
            if self.current_item_explanation:
                self.current_item_explanation += " " + self.text_buffer.strip()
            else:
                self.current_item_explanation = self.text_buffer.strip()
            self.in_p = False
            return
        
        if tag == 'li' and self.in_li:
            item = {
                "title": self.current_item_title,
                "explanation": self.current_item_explanation
            }
            if self.current_item_safety_note:
                item["safety_note"] = self.current_item_safety_note
            
            if self.in_notice_list:
                self.notice_items.append(item)
            elif self.in_action_list:
                self.action_items.append(item)
            self.in_li = False
            return
    
    def handle_data(self, data):
        if not self.in_view_public or self.in_disclaimer:
            return
        
        if self.in_h1 or self.in_public_summary or self.in_strong or self.in_p or self.in_safety_note or self.in_safety_warning:
            self.text_buffer += data
    
    def handle_entityref(self, name):
        char_map = {
            'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"',
            'apos': "'", 'mdash': '—', 'ndash': '–',
        }
        char = char_map.get(name, f'&{name};')
        if self.in_h1 or self.in_public_summary or self.in_strong or self.in_p or self.in_safety_note or self.in_safety_warning:
            self.text_buffer += char
    
    def handle_charref(self, name):
        try:
            if name.startswith('x'):
                char = chr(int(name[1:], 16))
            else:
                char = chr(int(name))
        except (ValueError, OverflowError):
            char = f'&#{name};'
        
        if self.in_h1 or self.in_public_summary or self.in_strong or self.in_p or self.in_safety_note or self.in_safety_warning:
            self.text_buffer += char
    
    def get_result(self):
        return {
            "x_public_title": self.public_title,
            "x_public_description": self.public_summary,
            "x_recognition_signals": self.notice_items,
            "x_safety_actions": self.action_items,
            "x_safety_warning": self.safety_warning
        }


def extract_technique_id(html_content):
    """Extract technique ID from the page HTML."""
    match = re.search(r'ID:&nbsp;</span>(TFA-T-\d+)', html_content)
    return match.group(1) if match else None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stix_path = os.path.join(script_dir, 'tfa-attack.json')
    techniques_dir = os.path.join(script_dir, 'techniques')
    
    # Load STIX bundle
    print(f"Loading STIX bundle from {stix_path}")
    with open(stix_path, 'r') as f:
        bundle = json.load(f)
    
    # Build index of attack-pattern objects by technique ID
    technique_index = {}
    for i, obj in enumerate(bundle['objects']):
        if obj.get('type') != 'attack-pattern':
            continue
        for ref in obj.get('external_references', []):
            if ref.get('source_name') == 'not-a-standard-tfa':
                technique_index[ref['external_id']] = i
    
    print(f"Found {len(technique_index)} attack-pattern objects in STIX bundle")
    
    # Process each technique directory
    extracted = 0
    errors = []
    
    for tech_dir in sorted(os.listdir(techniques_dir)):
        if not tech_dir.startswith('TFA-T-'):
            continue
        
        html_path = os.path.join(techniques_dir, tech_dir, 'index.html')
        if not os.path.exists(html_path):
            errors.append(f"  Missing: {html_path}")
            continue
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract technique ID from page
        tech_id = extract_technique_id(html_content)
        if not tech_id:
            # Fall back to directory name
            tech_id = tech_dir
        
        if tech_id not in technique_index:
            errors.append(f"  No STIX object for {tech_id}")
            continue
        
        # Parse public content
        parser = PublicContentExtractor()
        try:
            parser.feed(html_content)
        except Exception as e:
            errors.append(f"  Parse error for {tech_id}: {e}")
            continue
        
        result = parser.get_result()
        
        # Validate extraction
        if not result['x_public_title']:
            errors.append(f"  No public title found for {tech_id}")
            continue
        
        # Inject into STIX object
        obj_index = technique_index[tech_id]
        stix_obj = bundle['objects'][obj_index]
        
        stix_obj['x_public_title'] = result['x_public_title']
        stix_obj['x_public_description'] = result['x_public_description']
        stix_obj['x_recognition_signals'] = result['x_recognition_signals']
        stix_obj['x_safety_actions'] = result['x_safety_actions']
        if result['x_safety_warning']:
            stix_obj['x_safety_warning'] = result['x_safety_warning']
        
        extracted += 1
        signals_count = len(result['x_recognition_signals'])
        actions_count = len(result['x_safety_actions'])
        warning = "⚠" if result['x_safety_warning'] else " "
        print(f"  ✓ {tech_id}: \"{result['x_public_title']}\" — {signals_count} signals, {actions_count} actions {warning}")
    
    # Write updated bundle
    output_path = stix_path  # Overwrite in place
    backup_path = stix_path.replace('.json', '-pre-public.json')
    
    # Backup first
    print(f"\nBacking up original to {backup_path}")
    with open(stix_path, 'r') as f:
        with open(backup_path, 'w') as bf:
            bf.write(f.read())
    
    print(f"Writing updated STIX bundle to {output_path}")
    with open(output_path, 'w') as f:
        json.dump(bundle, f, indent=2)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*50}")
    print(f"Techniques processed: {extracted}/{len(technique_index)}")
    
    if errors:
        print(f"\nIssues ({len(errors)}):")
        for e in errors:
            print(e)
    
    # Quick stats
    total_signals = 0
    total_actions = 0
    total_warnings = 0
    for obj in bundle['objects']:
        if obj.get('type') == 'attack-pattern':
            total_signals += len(obj.get('x_recognition_signals', []))
            total_actions += len(obj.get('x_safety_actions', []))
            if obj.get('x_safety_warning'):
                total_warnings += 1
    
    print(f"\nSTIX bundle now contains:")
    print(f"  Public titles:        {extracted}")
    print(f"  Recognition signals:  {total_signals}")
    print(f"  Safety actions:       {total_actions}")
    print(f"  Safety warnings:      {total_warnings}")
    print(f"\nBackup saved to: {backup_path}")


if __name__ == '__main__':
    main()
