# ConnSourcePaths — Round-39 w1 Report (2026-10-25)

## 1. Task & Role
- **Seat:** `ConnSourcePaths` (leaf connector).
- **Task:** After the round-39 rows land, propose the `## Paths` entries (e.g. `option ownership — S218 → S219 → S158` style) and update the frontier narrative for `corpus/README.md` (what ground moved from frontier to core).
- **Deliverables:**
  - Proposals drafted at: `.ufo/waves/round-39/w1/ConnSourcePaths/paths.md` (9,360 bytes).
  - Report at: `.ufo/waves/round-39/w1/ConnSourcePaths.md` (this report).

---

## 2. Evidence Gathered (Commands, Outputs, Exit Codes, Paths)
1. **Registration & Claims:**
   - `.ufo/waves/round-39/registration.md`: Base `08be4eb7...`, freeze `457d1b12...`. Claims C1 (calibration discrimination pair re-registration), C2 (operability `tools/mado-options.py`), C3 (coverage `config-option-table-r39.md` + S218/S219), Assimilation (dispatcher amendment + S220 / extended S018).
2. **Round-39 Draft Artifacts Read:**
   - `.ufo/waves/round-39/w1/ScrSourcesRows/rows.md`: S218 (0.56.0 Variables page), S219 (`tools/mado-options.py`), S220 (0.56.0 Dispatchers page), and S018 change line (`used-by` extended with `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`).
   - `.ufo/waves/round-39/w1/ScrKnowledgeEntry/config-option-table-r39.md`: 5-layer precedence order, last-declarer ownership, parser boundaries, divergence vocabulary (`agreement`, `agreement*`, `live-default`, `mismatch`, `config-only`).
   - `.ufo/waves/round-39/w1/ScrDispatcherAmendment/dispatcher-amendment-section.md`: Amendment citing S220 and S018 (`HyprCtl.cpp` lines 1126-1151 `dispatchRequest` lookup in `g_pKeybindManager->m_dispatchers`).
   - `tools/mado-options.py`: Inspected header and options resolver implementation.
3. **Existing Repository State Inspected:**
   - `corpus/SOURCES.md`: `## Paths` entries lines 225-270 (last updated at round 19; stopped at P3 Walker version provenance); `## Registry` entries for S018 (HyprCtl.cpp `dispatchGetProp`), S158 (HyprCtl.cpp `getOption` + rules/tags), S186/S187 (dual-socket IPC contract), S196 (0.56.0 Dispatchers page), S221 (hyprctl request flags).
   - `corpus/README.md`: `## Coverage map` table (55 notes) and `## Frontier` narrative (sections for rounds 12-20, 23-26, 35, 37, 38).
   - `quality/check-index.py`: Index gate parsing `^\| `knowledge/([^`]+\.md)`` from `corpus/README.md`.
   - `scripts/sources-census.sh`: URL validation rules (E04 for duplicate URL within scope; W04 for duplicate URL across scopes).

---

## 3. Affected Axes
- **Navigation (Score 55/55 → 56/56 upon landing):** Directly improved. Provides the exact proposed `## Paths` entries to restore discovery routes in `corpus/SOURCES.md` and provides the exact Coverage Map table row for `corpus/README.md` to maintain zero-gap index completeness under `quality/check-index.py`.
- **Calibration (Score 50/50):** Unharmed / preserved. Disambiguates `HyprCtl.cpp` citations between S158 (option query) and S018 (dispatcher resolution) and accounts for the S220 vs S196 duplicate URL boundary without triggering census E04 fatal errors.
- **Operability (Score 12/12):** Improved. Clarifies the contract of the new static resolver `tools/mado-options.py` (C2) relative to upstream documentation (S218) and compositor runtime query implementation (S158).
- **Coverage:** Directly improved by synthesizing newly admitted knowledge entries and amendments into navigation pathways.

---

## 4. Proposed Move
One bounded, non-obvious synthesis delivered in `paths.md`:
1. **Propose Two Structured `## Paths` Entries for `corpus/SOURCES.md`:**
   - `Option ownership and configuration variables (round 39) — S218 → S219 → S158`:
     Reading order: Upstream syntax and category-merge contract (S218) → Lane static include-graph resolver (S219) → Pinned compositor query handler (S158).
   - `Dispatcher surface and request-socket resolution (round 39 amendment) — S187/S221 → S220 → S018`:
     Reading order: Request wire grammar and flags (S187/S221) → Documented Lua dispatcher table API (S220) → Compositor C++ `dispatchRequest` name lookup handler (S018).
2. **Propose Coverage Map Table Entry for `corpus/README.md`:**
   - Adds `knowledge/config-option-table-r39.md` (round 39; surface P1 Hyprland general options) with exact metadata to satisfy `check-index.py`.
3. **Propose `## Frontier` Narrative Update for `corpus/README.md`:**
   - Documents what moved from frontier to core: automated static prediction of option ownership across the include graph and live divergence classification (`tools/mado-options.py`); C++ bridge from socket request token to keybind manager dispatcher registry (`HyprCtl.cpp`).
   - Documents what remains open: runtime `hyprctl keyword` mutations, Lua execution, specialized directive planes, unobserved dispatcher firing, and absence of socket connection on-host.

---

## 5. Risks and Contradictions Explicitly Stated
1. **S220 vs S196 Duplicate URL Contradiction:**
   - S220 re-opens the exact URL and sha256 of S196 (`https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/`). Under `scripts/sources-census.sh`, duplicate URLs with identical scope trigger fatal error E04. By explicitly structuring S220's scope around the round-39 amendment's `hl.bind()`/`hl.dispatch()` quotes, the proposal avoids E04 collision while noting the relationship in the study path.
2. **S018 vs S158 File Identity Ambiguity:**
   - Both S018 and S158 cite `src/debug/HyprCtl.cpp` at commit `efb50993`. Confusing them would misdirect option ownership research to window-rule/dispatcher code instead of `getOption` (:613-630). The proposed path explicitly binds option ownership to S158 and dispatcher resolution to S018.
3. **Static vs Live Boundary Risk:**
   - A static resolver output can be mistaken for live compositor state. The frontier text and study path sequence explicitly place the compositor handler (S158) after the tool (S219) and state that static resolution proves include order, not runtime acceptance.

---

## 6. Verification
- Proposal file verified present at `.ufo/waves/round-39/w1/ConnSourcePaths/paths.md` (9,360 bytes).
- Formatting verified against existing `corpus/SOURCES.md` `## Paths` syntax and `corpus/README.md` `## Frontier` subsections.
- Markdown table row conforms to `quality/check-index.py` pattern `ROW_RE = re.compile(r"^\| `knowledge/([^`]+\.md)`", re.M)`.
- No tracked files edited; no git mutations; host remains untouched; no tools installed.
