# Session Log

Running log of substantive changes made during working sessions with Claude.
Newest sessions at the top. For the public-facing changelog see `data/changelog.json`.

---

## 2026-04-21 / 2026-04-22 — Site audit pass (Notion-tracked cleanup)

### Source
Work driven by the Notion database at
`https://www.notion.so/33e4b3bb9ab980eea4b3ce107a94dd44` (~28 rows).
Em confirmed the following out of scope for this pass: Licence section,
Limitations grammar pass, open questions (SAFE Tactic IDs, NAS view, metadata
improvements), Search (already working).

### Phase 1 — editorial fixes (9 tasks)

| # | Item | Status |
|---|------|--------|
| 1 | Verify `.ai` domain refs — grep found none, already done | ✓ no-op |
| 2 | Safety disclaimer reordered: "Always consider your physical safety first" now leads; second paragraph with underlined "The actions suggested here may not be safe in your specific circumstances" | ✓ |
| 3 | "Not an exhaustive list" caveat added to every "What You Can Do" section | ✓ |
| 4 | Spyware absence-of-evidence notice added to SAFE-T-0072 + sub-techniques (001–004) | ✓ |
| 5 | OASIS Open link in Attribution — already linked | ✓ no-op |
| 6 | `SAFE-T-0145` wrapped as hyperlink in SAFE-TA-0001, SAFE-T-0161, and techniques index | ✓ |
| 7 | Have I Been Pwned added to SAFE-T-0082 (public action + new COA `SAFE-M-0181 Credential Breach Monitoring`) | ✓ |
| 8 | Calendar sharing instructions on SAFE-T-0079 expanded from Google-only to cover Apple iCloud, Microsoft/Outlook, Samsung, Proton, Fastmail | ✓ |
| 9 | `sitemap.xml` at repo root (222 URLs, lastmod from file mtimes) | ✓ |

### Phase 3 — structural

| # | Item | Status |
|---|------|--------|
| 10 | Public view now shows the full metadata card (ID, sub-techniques, tactic, created, last-modified) on all 120 technique + tactic pages. Later repositioned to top-right with reduced padding via `theme/style-user.css` (`.public-meta-card` rules) to match technical view layout. Responsive: stacks below 768px. | ✓ |
| 11 | View-parity audit. 68/74 STIX-tracked techniques have full public↔technical parity. 6 have minor count imbalance (kept — stylistic, not gaps). **Finding:** 20 technique HTML pages (SAFE-T-0146 through 0165) have no STIX entry. Em accepted the drift to address in a future pass. Report: `reports/view-parity-audit.csv`. | ✓ |

### Phase 4 — new pages

All built from data sources + build scripts. Scripts live in `scripts/` (git-ignored per existing convention); re-run to regenerate pages.

| Page | Source | Build script | Notes |
|------|--------|--------------|-------|
| `/changelog/` | `data/changelog.json` | `scripts/build_changelog.py` | Data-driven. Linked from `about/limitations/` "Versioning & Currency". RSS discovery tag in `<head>`. |
| `/contributors/` | `data/contributors.json` | `scripts/build_contributors.py` | Framework lead + upstream seeded. Contributors / lived experience / practitioner review groups empty — Em to populate with consent. |
| `/documentation/` | inline in script | `scripts/build_documentation.py` | Narrative guidance on safely documenting TFA. Draft content — Em to review. |
| `/mitigations/` | `stix/tfa-attack.json` (course-of-action objects) | `scripts/build_mitigations_index.py` | MITRE-style index. 181 rows. |

### Phase 5 — RSS

- `/feed.xml` — RSS 2.0, built from same `data/changelog.json` via `scripts/build_feed.py`
- Changelog page has `<link rel="alternate" type="application/rss+xml">` + visible link
- Email signup (task #17) **deferred** per Em. RSS covers the gap; revisit if audience/stakeholder demand emerges. Buttondown was the recommended paid option; avoid Mailchimp/Substack given audience sensitivity.

### Public-facing polish (late in session)

- Metadata card on public view moved from bottom-of-page to top-right (floats alongside content, matching technical view). Inline styles initially applied to 120 files, then promoted to `theme/style-user.css` and stripped from HTML for maintainability.

### Files touched

**Content (source of truth):**
- `stix/tfa-attack.json` — SAFE-T-0072 notices, SAFE-T-0079 actions, SAFE-T-0082 actions + new COA + `mitigates` relationship

**HTML (generated output):**
- All 120 `techniques/SAFE-T-*/index.html` + `tactics/SAFE-TA-*/index.html`
- `techniques/tfa/index.html` — SAFE-T-0145 link
- `about/limitations/index.html` — changelog link added under Versioning & Currency

**Infrastructure:**
- `sitemap.xml` (new)
- `feed.xml` (new)
- `theme/style-user.css` — appended `.public-meta-card` rules (responsive)

**New pages:**
- `changelog/index.html`, `contributors/index.html`, `documentation/index.html`, `mitigations/index.html`

**New data sources:**
- `data/changelog.json`, `data/contributors.json`

**New scripts (git-ignored):**
- `scripts/build_changelog.py`, `build_contributors.py`, `build_documentation.py`, `build_mitigations_index.py`, `build_feed.py`

**New audit artefact:**
- `reports/view-parity-audit.csv`

### Decisions recorded

- **Skip-if-already-processed guard** in `generate_public_pages.py` means the generator won't re-emit existing pages. All Phase 1 HTML changes were therefore done via targeted find-and-replace rather than regeneration. If the generator is ever rerun from scratch, the `PUBLIC_DISCLAIMER` constant in that script was updated to match the new disclaimer text so output stays consistent.
- `SAFE-M-0181` allocated for Credential Breach Monitoring — based on highest SAFE-M ID currently in HTML (no central registry exists).
- Metadata card was cloned from each page's technical view rather than rebuilt from STIX, so per-technique fields (sub-techniques, created date, etc.) are preserved exactly as the technical view shows them.

### Deferred / backlog

- **#17** — Email signup for updates. Deferred. RSS covers for now.
- **#18** — Backport SAFE-T-0146–0165 into `stix/tfa-attack.json` as proper attack-pattern objects with `x_safe_*` extensions. Em to handle in next update.
- **General** — `scripts/` directory is git-ignored per existing `.gitignore` convention (matching the `generate_public_pages.py` pattern). New build scripts for changelog/contributors/documentation/mitigations/feed live locally only. Worth reconsidering if a collaborator joins or Em switches machines.
- **General** — No central registry for `SAFE-M-*` mitigation IDs; currently allocated by scanning HTML. Worth a separate tidy-up pass at some point.

### Not committed

Session ended with all changes unstaged per Em's instruction. Commit plan was a single logical commit covering Phase 1 edits, with later phases as separate commits if desired.
