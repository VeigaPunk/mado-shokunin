# AttackNav — round 16 README/knowledge navigation falsification

Seat: MadoR16.AttackNav (leaf, read-only). Scope: `corpus/README.md` expected/observed knowledge
filename sets, the new note `corpus/knowledge/waybar-observation-boundaries-r16.md`, and dropped-row
check. No gate, measure, verify, selftest, package, service, or producer execution. Only read-only
git (`show`, `diff`, `ls-tree`, `status`). No tools installed or updated.

## Verdict

No blocking defect in the navigation set. Expected (README) equals observed (disk). No old row dropped.
Three low-severity advisories (N1–N3) and one hygiene item for L1 (N2).

## Measured set comparison (C locale, sorted-unique)

| Set | HEAD | Working tree |
|---|---|---|
| README `knowledge/*.md` refs (table rows + prose links) | 29 | 30 |
| README table rows whose lead is a knowledge link | 29 | 30 |
| `corpus/knowledge/*.md` on disk | 29 tracked | 30 |

- Expected − observed (README refs not on disk): **[]**
- Observed − expected (disk not referenced by README): **[]**
- Duplicate row leads (`uniq -d`): **[]** in HEAD and working tree
- Dropped (in HEAD README, absent from working README): **[]**
- Added: `knowledge/waybar-observation-boundaries-r16.md` (one row, appended after the r15 row, line 41)
- Removed lines in `git diff HEAD` for `corpus/README.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`: **0 / 0 / 0**
- Every backticked `knowledge/` row lead is byte-identical to its HEAD row (none changed, none removed).
- Relative `](…)` links in README resolve (`../PROVINCE.md`, `../SHONEN.md`, `SOURCES.md`, all `knowledge/*.md`, `lessons/round-15.md`).
- Backticked repo paths in README resolve, including `.ufo/waves/round-16/evidence/source-bindings.json`.

## Uniqueness and provenance join

- Basename `waybar-observation-boundaries-r16.md` occurs once on the filesystem under the shokunin tree.
- `covers:` headers in the first 15 lines of `corpus/knowledge/*.md`: exactly 7 notes, one per U1–U7:
  `window-rule-effects-getprop` U1, `hyprland-config-era-r12` U2, `xdg-portal-routing-r12` U3,
  `wayland-protocol-boundaries-r13` U4, `output-colour-boundaries-r14` U5,
  `input-debugging-boundaries-r15` U6, `waybar-observation-boundaries-r16` U7.
  Each matches its README row's "covers Uk" text. No U7 claim from any other note.
- Provenance trio (`source:`, `verified-at:`, `recheck:`) present in the new note at lines 1–3, same shape as the r14/r15 notes.
- Reciprocal join: note line 1 cites S053 and S054; `corpus/SOURCES.md` rows S053/S054 name
  `corpus/knowledge/waybar-observation-boundaries-r16.md` as used-by; README row (line 41) cites S053/S054.
- Digests: `.ufo/waves/round-16/evidence/source-bindings.json` lists S053 `efb6a63a…d82` (6656 B) and
  S054 `2232f7f7…b291f` (8746 B). The same sha256 strings appear in the SOURCES.md rows. Textual match only;
  the raw bytes were NOT re-fetched or re-hashed by this seat.

## Advisories

**N1 (low, navigation) — Waybar route table has no U7 pointer.** README "Province routes" Waybar row
(line 58) links only `waybar-walker-plane` and `waybar-walker-semantics` §§2–5, §9. The new note is reached
from the Coverage map row (line 41), the Frontier bullet (lines 111–116), and the SOURCES rows, but not from
the surface route a navigator uses for Waybar. Counter-evidence: the r15 input note also has no route row
(no input route exists in that table), so this follows precedent. Suggested fix: add
`[documentary observation route](knowledge/waybar-observation-boundaries-r16.md)` to the Waybar row's
"Start here" cell, with "producer contract only; no module text" in the Limit cell. Owner: L1 (README).

**N2 (low, hygiene) — `tools/__pycache__/` is untracked and not ignored.** `git status` shows
`?? tools/__pycache__/`; `.gitignore` contains only `.ufo/interactive-sessions/`. The directory holds
`mado-action-plan.cpython-314.pyc`, mtime 2026-10-20 05:46:56 -0300, the same minute as
`tools/mado-action-plan.py` (05:46). Bytecode is written on import or `py_compile`, so something in the
lane imported or compiled the module this round. That is not proof of execution. Under the round's
"no execution" rule, the origin should be identified and the pyc removed before commit. Either way, add an
ignore or remove it. Not re-run by this seat.

**N3 (low, overlap) — new producer-contract text overlaps an existing Waybar note.**
`corpus/knowledge/waybar-walker-semantics.md` already tabulates `custom/*` producers (lines 119–149:
`exec`, `exec-if`, `signal`, json, `interval`) and cites the manual's JSON fields (line 161,
"`men 5 waybar-custom` documents JSON fields"). The new note's "Producer contract" section (lines 13–30)
restates the same manual areas from the tagged 0.15.0 source. The evidence class differs (tagged source
versus the host-pinned semantics), so this is not a duplicate-admission. Suggested: a one-line cross-link
from the new note's "Producer contract" to `waybar-walker-semantics.md` §3 with the statement that the
host-table rows are not re-verified here. Owner: L1.

## Checked and clean

- Note line 67 cites "QUALITY21". Resolves: `corpus/QUALITY.md` criterion 21 under "## Round 16", and the
  lesson uses the same numbering.
- Note header `covers: U7` and README row are consistent; no second U7 note.
- The note's "not built-in module" limit (lines 77–78) matches the README row's `[UNK]` wording.

## Verification gaps (not run by this seat)

- Raw S053/S054 bytes not fetched; SHA-256/byte counts are checked for text consistency only.
- Note body claims (`Custom::update` hide conditions, `label_.set_markup`, JSON first-line behaviour) are
  not checked against tagged source here; that is owned by the U7 source/code seats.
- No gate, `measure.py`, `mado-verify.sh`, or census was executed. Counts above are from set operations on
  files as they stand at the time of reading. L1 should re-derive the 30/30 figure once after integration.
