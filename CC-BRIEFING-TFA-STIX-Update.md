# TFA Matrix STIX Bundle Update — Claude Code Briefing

## Session Goal

Migrate the TFA STIX bundle from TFA IDs to SAFE IDs, apply all MITRE compatibility fixes, and bring the bundle in line with the SAFE STIX template v1.3.0. This is the foundational update — everything else builds on getting IDs right.

## Critical Context

### The Core Change
TFA is a *filtered view* of SAFE, not a separate framework. All IDs must be SAFE IDs. The TFA site (tfa.notastandard.org) continues to exist — it just displays SAFE objects filtered by `x_safe_vector == "tech_facilitated"`.

### ID Scheme
```
SAFE-T-XXXX       Techniques (attack-pattern)
SAFE-T-XXXX.XXX   Sub-techniques
SAFE-M-XXXX       Mitigations (course-of-action)
SAFE-D-XXXX       Detections/Indicators (indicator)
SAFE-TA-XXXX      Tactics — activity-type groupings displayed on the TFA website
SAFE-C-XXX        Coordinates — mode.mechanism.domain intersections (27 total)
```

### ID Mapping File
**`/Users/emilyholyoake/Desktop/SAFE/safe-platform/src/data/tfa-to-safe-id-map.json`**

This file contains the COMPLETE mapping: 74 parent techniques, 24 sub-techniques, 180 mitigations, 165 detections. Use this as the authoritative lookup. Example:
- TFA-T-1001 → SAFE-T-0072 (Stalkerware Installation)
- TFA-M-1001 → SAFE-M-0001 (Anti-Stalkerware Scanning)
- TFA-D-1001 → SAFE-D-0001 (Anomalous Battery Consumption)

### Tactic ID Mapping (NEW — not in the map file)
```
TFA-TA-0001 → SAFE-TA-0001  Surveillance & Tracking
TFA-TA-0002 → SAFE-TA-0002  Account & Access Compromise
TFA-TA-0003 → SAFE-TA-0003  Harassment & Intimidation
TFA-TA-0004 → SAFE-TA-0004  Information Manipulation
TFA-TA-0005 → SAFE-TA-0005  Isolation & Control
TFA-TA-0006 → SAFE-TA-0006  Resource & Financial Control
TFA-TA-0007 → SAFE-TA-0007  Physical Enablement
SAFE-TA-0008 (NEW, not yet in bundle) Grooming & Targeted Recruitment
SAFE-TA-0009 (NEW, not yet in bundle) Discovery & Preparation
```

### Repository Structure
- **`gh-pages` branch** is the LIVE SITE. All work happens here. Do not touch `main`.
- Canonical STIX bundle: `stix/tfa-attack.json` on gh-pages
- GitHub Actions workflow on `main` is DISABLED (workflow_dispatch only)

### Reference Files (read these first)
1. **ID Map** — `safe-platform/src/data/tfa-to-safe-id-map.json`
2. **SAFE STIX Template v1.2.2** — `safe-platform/src/data/stix-extensions/TEMPLATE-README.md`
3. **Coordinate Mapping Spreadsheet** — `tfa-matrix/TFA-to-SAFE-Coordinate-Mapping.xlsx`

### Architecture Decisions (DO NOT CHANGE)
- Triple kill chains: `safe-harm-taxonomy` + `tfa-matrix` + `safe-harm-lifecycle`
- gh-pages is canonical, main is reference only
- CC BY-SA 4.0 license stays
- `sectors: ["technology"]` not `["non-profit"]`
- Extension key: `extension-definition--acf2f380-0000-4000-8000-000000000002` (SAFE)
- TAXII is the ecosystem backbone — NAS Hub publishes collections, Client Hubs subscribe and publish back anonymised validation. The TAXII boundary IS the PII firewall. The TFA website is just another TAXII consumer. See template v1.3.0.

---

## Task 1: Migrate All IDs to SAFE (P0 — DO THIS FIRST)

### 1a. Extension Properties: x_tfa_* → x_safe_*

On ALL 74 attack-pattern objects, rename the extension properties inside the extensions block. The extension key itself changes from `extension-definition--acf2f380-0000-4000-8000-000000000001` (TFA) to `extension-definition--acf2f380-0000-4000-8000-000000000002` (SAFE).

```
x_tfa_technique_id  → x_safe_technique_id  (AND change value: TFA-T-1001 → SAFE-T-0072)
x_tfa_mode          → x_safe_mode
x_tfa_mechanism     → x_safe_mechanism
x_tfa_domain        → x_safe_domain
x_tfa_platforms     → x_safe_platforms
x_tfa_detection_difficulty → x_safe_detection_difficulty
x_tfa_evidence_types → x_safe_evidence_types
x_tfa_prevalence    → x_safe_prevalence
x_tfa_version       → x_safe_version
x_tfa_public_title  → x_safe_public_title
x_tfa_public_summary → x_safe_public_summary
x_tfa_public_safety_warning → x_safe_public_safety_warning
x_tfa_public_notices → x_safe_public_notices
x_tfa_public_actions → x_safe_public_actions
```

Add new fields (set to defaults):
```
x_safe_vector: "tech_facilitated"    (all TFA techniques are tech-facilitated)
x_safe_is_subtechnique: false        (all 74 are parent techniques)
x_safe_parent_technique_id: null
x_safe_sexual: false                 (review per technique later)
x_safe_status: "active"
x_safe_validation: null
x_safe_migrated_from: null           (these ARE the originals, not migrated)
x_safe_view_mode: "both"
x_safe_recognition_signals: []       (copy from x_safe_public_notices signals if populated)
x_safe_safety_guidance: null         (copy from x_safe_public_safety_warning if populated)
```

### 1b. External References: TFA IDs → SAFE IDs

On EVERY object that has `external_references`, change:
```json
// FROM:
{"source_name": "not-a-standard-tfa", "external_id": "TFA-T-1001", "url": "..."}

// TO:
{"source_name": "SAFE Framework", "external_id": "SAFE-T-0072", "url": "https://tfa.notastandard.org/techniques/SAFE-T-0072"}
```

Apply to all object types using the ID map:
- 74 techniques: TFA-T-XXXX → SAFE-T-XXXX
- 180 mitigations: TFA-M-XXXX → SAFE-M-XXXX
- 165 indicators: TFA-D-XXXX → SAFE-D-XXXX
- 7 tactics: TFA-TA-XXXX → SAFE-TA-XXXX

### 1c. Tactic Objects

On the 7 x-mitre-tactic objects, rename custom properties:
```
x_tfa_public_name    → x_safe_public_name
x_tfa_public_intro   → x_safe_public_intro
x_tfa_public_safety  → x_safe_public_safety
```

In the extensions block:
```
x_tfa_tactic_id → x_safe_tactic_id (AND change value: TFA-TA-0001 → SAFE-TA-0001)
x_tfa_version   → x_safe_version
```

The `x_mitre_shortname` values stay the same (surveillance-tracking, etc.) — these are the kill chain phase names and the TFA site reads them.

### 1d. Extension Definition Object

Replace the existing extension-definition:
- ID: `extension-definition--acf2f380-0000-4000-8000-000000000002`
- Name: "SAFE Framework Technique Extension"
- Update `extension_properties` to list all `x_safe_*` fields (see template v1.2.2)

Keep a backward-compat reference to the old TFA extension ID in external_references.

### 1e. Kill Chain Name

`kill_chain_name: "tfa-matrix"` STAYS. It names the activity-type tactic view, not the ID scheme. Do NOT rename.

### 1f. Website URLs

Technique page URLs change:
```
/techniques/TFA-T-1001/  →  /techniques/SAFE-T-0072/
/tactics/TFA-TA-0001/    →  /tactics/SAFE-TA-0001/
```

**Create redirect pages at ALL old URLs.** Every existing link must continue to work:

```html
<!-- /techniques/TFA-T-1001/index.html (redirect) -->
<html><head>
<meta http-equiv="refresh" content="0; url=/techniques/SAFE-T-0072/">
<link rel="canonical" href="/techniques/SAFE-T-0072/">
</head><body>
<p>This technique has moved to <a href="/techniques/SAFE-T-0072/">SAFE-T-0072</a></p>
</body></html>
```

### 1g. Indicator Patterns

Update IDs inside pattern strings:
```
[x-tfa-behavioral:description = 'TFA-D-1001']
→
[x-tfa-behavioral:description = 'SAFE-D-0001']
```

---

## Task 2: Apply Coordinate Changes (P0)

Six techniques need x_safe_mode/mechanism/domain updated:

| SAFE ID | Technique | Field | From | To |
|---------|-----------|-------|------|----|
| SAFE-T-0073 | Physical Tracker Planting | mechanism, domain | manipulation, psychological | manipulation, physical |
| SAFE-T-0110 | Sextortion | mode, domain | exploitation, environmental | exploitation, psychological |
| SAFE-T-0133 | Smart Home Resource Control | domain | physical | environmental |
| SAFE-T-0141 | IoT Device Weaponization | domain | psychological | environmental |
| SAFE-T-0121 | Communication Monitoring Disclosure | mechanism | force | isolation |
| SAFE-T-0088 | Backup/Cloud Access | domain | psychological | environmental |

---

## Task 3: MITRE Compatibility Fixes (P0)

Apply to ALL 74 attack-pattern objects (top-level):
```python
"x_mitre_is_subtechnique": False,
"x_mitre_platforms": [...],  # Copy from x_safe_platforms in extensions
"x_mitre_version": "1.0",
"x_mitre_domains": ["tfa-matrix"],
"x_mitre_deprecated": False,
"revoked": False,
```

Apply to ALL 7 x-mitre-tactic objects:
```python
"x_mitre_version": "1.0",
"x_mitre_domains": ["tfa-matrix"],
"x_mitre_deprecated": False,
```

Add TLP:CLEAR marking (ID: `marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487`).
Add to `object_marking_refs` on ALL objects alongside CC BY-SA 4.0.
Fix identity: `"sectors": ["technology"]`

---

## Task 4: Remove Redundant Relationships (P1)

Remove the 74 "uses" relationships (attack-pattern → x-mitre-tactic). Keep 180 "mitigates" + 165 "indicates".

---

## Task 5: Add x-mitre-collection Object (P1)

See template v1.2.2 for structure. Use "SAFE Framework" as source_name.

---

## What NOT To Do

- Do NOT add safe-harm-taxonomy or safe-harm-lifecycle kill chains (separate session)
- Do NOT add SAFE-TA-0008/0009 (content not ready)
- Do NOT add sub-techniques (content not ready)
- Do NOT touch `main` branch
- Do NOT delete old URL directories — create redirects
- Do NOT rename `kill_chain_name: "tfa-matrix"`

---

## Validation Checklist

1. Bundle is valid JSON
2. ZERO remaining `TFA-T-`, `TFA-M-`, `TFA-D-`, or `TFA-TA-` strings in any external_id
3. ZERO remaining `x_tfa_` property names anywhere
4. Extension key is `...000000000002` on all technique objects
5. All 74 techniques have SAFE-T-XXXX in x_safe_technique_id
6. All 180 mitigations have SAFE-M-XXXX in external_references
7. All 165 indicators have SAFE-D-XXXX in external_references
8. All 7 tactics have SAFE-TA-XXXX in x_safe_tactic_id
9. source_name is "SAFE Framework" on all external_references
10. Identity has `sectors: ["technology"]`
11. TLP:CLEAR marking exists, referenced on all objects
12. 74 "uses" relationships removed
13. 180 "mitigates" + 165 "indicates" relationships remain
14. x-mitre-collection exists
15. 6 coordinate changes applied
16. MITRE compat fields on all techniques and tactics
17. Redirect pages at all old TFA URLs
18. kill_chain_phases still reference tfa-matrix shortnames (unchanged)
19. x_safe_vector == "tech_facilitated" on all 74 techniques

## Testing

1. ATT&CK Navigator: load bundle, verify 7 columns + 74 techniques
2. TFA site: pages load at new SAFE-T-XXXX URLs
3. TFA site: old TFA-T-XXXX URLs redirect correctly
4. stix2 validation: `from stix2 import parse; parse(bundle, allow_custom=True)`
5. Grep: `grep -r "TFA-T-" stix/tfa-attack.json` returns ZERO results
6. Grep: `grep -r "x_tfa_" stix/tfa-attack.json` returns ZERO results
