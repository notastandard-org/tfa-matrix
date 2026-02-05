#!/usr/bin/env python3
"""
TFA Matrix STIX Integration: Mitigations & Detections

Reads the existing tfa-attack.json STIX bundle and adds:
  - course-of-action objects for each mitigation
  - x-tfa-detection objects for each detection indicator
  - 'mitigates' relationships (course-of-action -> technique)
  - 'detects' relationships (x-tfa-detection -> technique)

Also generates master_mitigations_detections.csv.

Usage:
    python3 integrate_stix_mitigations.py

Input:  tfa-matrix/stix/tfa-attack.json
Output: tfa-matrix/stix/tfa-attack.json (updated in place)
        master_mitigations_detections.csv
"""

import json
import csv
import uuid
import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
STIX_INPUT = "tfa-matrix/stix/tfa-attack.json"
STIX_OUTPUT = "tfa-matrix/stix/tfa-attack.json"
CSV_OUTPUT = "master_mitigations_detections.csv"

# Constants matching existing bundle
CREATED_DATE = "2026-02-04T00:00:00.000Z"
MODIFIED_DATE = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
IDENTITY_REF = "identity--f1b2c3d4-e5f6-7890-abcd-ef1234567890"
MARKING_REF = "marking-definition--a1b2c3d4-1234-5678-9abc-def012345678"
EXTENSION_ID = "extension-definition--acf2f380-0000-4000-8000-000000000001"
SPEC_VERSION = "2.1"

# Source name for external references
SOURCE_NAME = "not-a-standard-tfa"
BASE_URL = "https://notastandard.ai/tfa-matrix"


def deterministic_uuid(seed: str) -> str:
    """Generate deterministic UUID from seed for reproducibility."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"tfa-matrix.org.{seed}"))


def build_technique_stix_map(bundle: dict) -> dict:
    """Map technique external IDs (TFA-T-XXXX) to their STIX IDs."""
    mapping = {}
    for obj in bundle["objects"]:
        if obj["type"] == "attack-pattern":
            ext_refs = obj.get("external_references", [])
            if ext_refs:
                ext_id = ext_refs[0].get("external_id", "")
                if ext_id.startswith("TFA-T-"):
                    mapping[ext_id] = obj["id"]
    return mapping


def create_course_of_action(mit_id: str, name: str, description: str) -> dict:
    """Create a STIX 2.1 course-of-action object for a mitigation."""
    return {
        "type": "course-of-action",
        "spec_version": SPEC_VERSION,
        "id": f"course-of-action--{deterministic_uuid(mit_id)}",
        "created_by_ref": IDENTITY_REF,
        "created": CREATED_DATE,
        "modified": MODIFIED_DATE,
        "name": name,
        "description": description,
        "external_references": [
            {
                "source_name": SOURCE_NAME,
                "external_id": mit_id,
                "url": f"{BASE_URL}/mitigations/{mit_id}"
            }
        ],
        "object_marking_refs": [MARKING_REF],
        "extensions": {
            EXTENSION_ID: {
                "extension_type": "property-extension",
                "x_tfa_mitigation_id": mit_id,
                "x_tfa_version": "1.0"
            }
        }
    }


def create_detection(det_id: str, name: str, description: str) -> dict:
    """Create a STIX 2.1 indicator object for a detection signal.
    
    Uses the 'indicator' type as these represent observable behavioral
    signals that indicate a technique is being employed.
    """
    return {
        "type": "indicator",
        "spec_version": SPEC_VERSION,
        "id": f"indicator--{deterministic_uuid(det_id)}",
        "created_by_ref": IDENTITY_REF,
        "created": CREATED_DATE,
        "modified": MODIFIED_DATE,
        "name": name,
        "description": description,
        "indicator_types": ["anomalous-activity"],
        "pattern": f"[x-tfa-behavioral:description = '{det_id}']",
        "pattern_type": "stix",
        "valid_from": CREATED_DATE,
        "external_references": [
            {
                "source_name": SOURCE_NAME,
                "external_id": det_id,
                "url": f"{BASE_URL}/detections/{det_id}"
            }
        ],
        "object_marking_refs": [MARKING_REF],
        "extensions": {
            EXTENSION_ID: {
                "extension_type": "property-extension",
                "x_tfa_detection_id": det_id,
                "x_tfa_signal_type": "behavioral",
                "x_tfa_version": "1.0"
            }
        }
    }


def create_relationship(source_ref: str, rel_type: str, target_ref: str,
                        description: str, seed: str) -> dict:
    """Create a STIX 2.1 relationship object."""
    return {
        "type": "relationship",
        "spec_version": SPEC_VERSION,
        "id": f"relationship--{deterministic_uuid(seed)}",
        "created_by_ref": IDENTITY_REF,
        "created": CREATED_DATE,
        "modified": MODIFIED_DATE,
        "relationship_type": rel_type,
        "description": description,
        "source_ref": source_ref,
        "target_ref": target_ref,
        "object_marking_refs": [MARKING_REF]
    }


def main():
    # Import technique data
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from technique_data import TECHNIQUE_DATA

    # Load existing STIX bundle
    if not os.path.exists(STIX_INPUT):
        print(f"ERROR: {STIX_INPUT} not found")
        sys.exit(1)

    with open(STIX_INPUT, 'r') as f:
        bundle = json.load(f)

    print(f"Loaded STIX bundle: {len(bundle['objects'])} existing objects")

    # Build technique ID -> STIX ID map
    tech_map = build_technique_stix_map(bundle)
    print(f"Found {len(tech_map)} techniques in bundle")

    # Remove any existing mitigations/detections (for idempotency)
    original_count = len(bundle["objects"])
    bundle["objects"] = [
        obj for obj in bundle["objects"]
        if obj["type"] not in ("course-of-action", "indicator")
        and not (obj["type"] == "relationship" 
                 and obj.get("relationship_type") in ("mitigates", "detects"))
    ]
    removed = original_count - len(bundle["objects"])
    if removed:
        print(f"Removed {removed} existing mitigation/detection objects (idempotent)")

    # Track new objects
    new_coas = []
    new_indicators = []
    new_relationships = []
    csv_rows = []
    missing_techniques = []

    for tech_id in sorted(TECHNIQUE_DATA.keys()):
        data = TECHNIQUE_DATA[tech_id]

        # Look up the technique's STIX ID
        technique_stix_id = tech_map.get(tech_id)
        if not technique_stix_id:
            missing_techniques.append(tech_id)
            continue

        # --- Mitigations ---
        for mit_id, mit_name, mit_desc in data["mitigations"]:
            # STIX course-of-action
            coa = create_course_of_action(mit_id, mit_name, mit_desc)
            new_coas.append(coa)

            # Relationship: course-of-action --mitigates--> technique
            rel = create_relationship(
                source_ref=coa["id"],
                rel_type="mitigates",
                target_ref=technique_stix_id,
                description=f"{mit_name} mitigates {tech_id}",
                seed=f"{mit_id}-mitigates-{tech_id}"
            )
            new_relationships.append(rel)

            # CSV row
            csv_rows.append({
                "technique_id": tech_id,
                "type": "mitigation",
                "item_id": mit_id,
                "item_name": mit_name,
                "item_description": mit_desc,
            })

        # --- Detections ---
        for det_id, det_name, det_desc in data["detections"]:
            # STIX indicator
            indicator = create_detection(det_id, det_name, det_desc)
            new_indicators.append(indicator)

            # Relationship: indicator --indicates--> technique
            rel = create_relationship(
                source_ref=indicator["id"],
                rel_type="indicates",
                target_ref=technique_stix_id,
                description=f"{det_name} indicates {tech_id}",
                seed=f"{det_id}-indicates-{tech_id}"
            )
            new_relationships.append(rel)

            # CSV row
            csv_rows.append({
                "technique_id": tech_id,
                "type": "detection",
                "item_id": det_id,
                "item_name": det_name,
                "item_description": det_desc,
            })

    # Append new objects to bundle
    bundle["objects"].extend(new_coas)
    bundle["objects"].extend(new_indicators)
    bundle["objects"].extend(new_relationships)

    # Write updated STIX bundle
    with open(STIX_OUTPUT, 'w') as f:
        json.dump(bundle, f, indent=2)

    # Write CSV
    fieldnames = ["technique_id", "type", "item_id", "item_name", "item_description"]
    with open(CSV_OUTPUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    # --- Report ---
    from collections import Counter
    type_counts = Counter(obj["type"] for obj in bundle["objects"])

    print(f"\n{'='*60}")
    print(f"STIX INTEGRATION COMPLETE")
    print(f"{'='*60}")
    print(f"\nUpdated: {STIX_OUTPUT}")
    print(f"  Total objects: {len(bundle['objects'])}")
    for obj_type, count in sorted(type_counts.items()):
        print(f"    {obj_type}: {count}")

    print(f"\nNew objects added:")
    print(f"  course-of-action (mitigations): {len(new_coas)}")
    print(f"  indicator (detections):         {len(new_indicators)}")
    print(f"  relationships:                  {len(new_relationships)}")
    
    rel_types = Counter(r["relationship_type"] for r in bundle["objects"] if r["type"] == "relationship")
    print(f"\nRelationship breakdown:")
    for rt, c in sorted(rel_types.items()):
        print(f"    {rt}: {c}")

    print(f"\nCSV: {CSV_OUTPUT}")
    mit_csv = sum(1 for r in csv_rows if r["type"] == "mitigation")
    det_csv = sum(1 for r in csv_rows if r["type"] == "detection")
    print(f"  {mit_csv} mitigations + {det_csv} detections = {len(csv_rows)} rows")

    if missing_techniques:
        print(f"\n⚠ Techniques in data but not in STIX bundle: {missing_techniques}")

    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
