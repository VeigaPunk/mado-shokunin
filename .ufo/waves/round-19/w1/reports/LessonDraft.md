# LessonDraft — four round-19 Mistakes rows drafted (M1–M4 from §6 R18-V1..V4); two design points for L1

Draft: `.ufo/waves/round-19/drafts/LessonDraft.md` (sha256 `87d8dff3b93d03866982253615e76774064b8e4fc42b27e1eb55aeec8a804351`, 4 rows, table shape of `corpus/lessons/round-18.md:14`). Only that file and this report were written. No lesson, QUALITY, SOURCES or SKILL file was edited.

## Findings

Each row follows the round-18 columns: id | class | evidence pointer | captured-by | fix (shown able to fail). Captured-by names the check or prose rule that existed and missed the defect.

- **M1 — reference-drift (R18-V1), criterion 27 + `anchor-durability.py` HTML-digest arm.**
  - Evidence: `corpus/SOURCES.md:106` (S094) anchor carries `50c1ac25…` and `9e1160a0…`, both tree-page HTML digests (grep: one hit each). Two closure fetches of the same tree URL gave `1a3ddca5…` then `4d001dc8…` (`corpus/lessons/round-18-verifier-spotcheck.md:105`), so neither anchor value reproduces. The raw `colors.toml` `dbdd13a6…` reproduces (`theme-route-r18.md:158-161`).
  - Captured-by: round-18 Gate prose (`corpus/lessons/round-18.md:33-36`). The row was admitted; the `fetch-verify.py` CONFLICT rule gated no criterion.
- **M2 — scope (R18-V4), criterion 27 UNPINNED_ALIAS arm.**
  - Evidence: `corpus/SOURCES.md:96` (S084) anchor is `docs.rs/xdg/latest/…`, saved-HTML sha `0291cfe6…`, tier A. The `XD` row at `corpus/knowledge/walker-route-r18.md:33` relies on it. The reopen GATE line (`round-18.md:64`) and spot-check item 4 (`round-18-verifier-spotcheck.md:120-121`) both advise the crate-tarball re-point; the row was not changed.
  - Captured-by: round-18 Gate prose (`round-18.md:34-36`).
- **M3 — landing (R18-V3), criterion 28 + `supersede-sweep.py`.**
  - Evidence: `.ufo/waves/round-19/evidence/fresh-pins-before.txt` (the `fresh-pins.py` baseline at 9c54c56): denominator 13, current 2, so 11 stale. The stale set is `SKILL.md`, `tools/mado-verify.sh`, and nine `corpus/knowledge/*.md` files. The two current files are `corpus/README.md` and `walker-route-r18.md`.
  - The SKILL erratum (`SKILL.md:1822-1827`) carries `2.17.2` on line 1825 with no `S###` token, so it fails the same rule. Host move: `/var/log/pacman.log:2929` (file bytes read with grep only).
  - The round-18 sweep grep (`round-18-verifier-spotcheck.md:119`) was limited to `corpus/`. It did not reach root `SKILL.md` or `tools/`; the baseline's 11 includes both.
  - Captured-by: round-18 ConnStalePinsSweep (`round-18.md:91`) listed the files; the fix stopped at SKILL and one note.
- **M4 — attribution (R18-V2), criterion 29 + round-19 receipt claims.**
  - Evidence: `corpus/QUALITY.md:144-154` (criterion 26) rests on `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt`. Its header has 0 `tool_sha256=` and 0 `measured_commit=` (grep = 0). The seat has `old gate bytes` `fba82a66…` (line 8) and `edited gate bytes` `2bdf5e8a…` (line 10), and the W3 report says the edited gate was uncommitted at run time (`w3/reports/W3CriticC1Final.md:96`, `:196-197`).
  - Under `receipt-check.py` on a lab claims file the receipt prints `MISSING_PROVENANCE` (`W3CriticC1Final.md:64`). The committed `.ufo/waves/round-18/receipt-claims.json` has no `gate-rc` entry.
  - Captured-by: none; criterion 24 (`corpus/QUALITY.md:131`) was not applied to criterion 26's own red.

## Design points for L1 (decide before landing; not decided in the draft)

1. S094 and S084 need a new registry status for superseded rows (`SOURCES.md` allows in-place status change, logged old→new). Status vocabulary today is `mined`, `queued`, `rejected`. The draft writes `superseded-by-S097` and `superseded-by-S098` as placeholders.
2. The UNPINNED_ALIAS arm needs a fixed alias list. The draft proposes `/latest/`, `/master/`, `/main/`, `/HEAD/`; the list must be pinned at pre-registration.

Reserved ids used: S097 (superseding S094 row, no HTML digests), S098 (xdg crate tarball `2fb4332…` replacing S084 as support). Neither id exists yet: `corpus/SOURCES.md` has no S096–S105 rows (grep empty). Scripts `anchor-durability.py`, `supersede-sweep.py` and any round-19 receipt claim do not exist yet (`ls` of `.ufo/waves/round-19/`); the draft cites them as planned paths only. No red or green result for any row was run by this seat.

## Evidence I checked (read-only)

- `corpus/lessons/round-18.md:14`, `:22`, `:33-36`, `:64`, `:74`, `:91`: table header, M7, Gate rules, S084 and S094 GATE lines, SKILL erratum line.
- `corpus/lessons/round-18-verifier-spotcheck.md:105`, `:117-121`: §4 HTML-digest row and §6 items 1–4.
- `corpus/SOURCES.md:96`, `:102`, `:106`: S084, S090, S094 rows; `grep -o` gives one hit each for `50c1ac25`, `9e1160a0`, `dbdd13a6`.
- `corpus/QUALITY.md:131`, `:144` (criteria 24, 26); file is 161 lines, last criterion ends near 154.
- `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` lines 1–10 (no provenance fields).
- `.ufo/waves/round-18/w3/reports/W3CriticC1Final.md:64`, `:85-87`, `:96`, `:196-197`.
- `.ufo/waves/round-18/receipt-claims.json`: 0 `gate-rc` matches.
- `.ufo/waves/round-19/evidence/fresh-pins-before.txt`: denominator 13 / current 2 and the per-file rows.
- `SKILL.md:23`, `:114`, `:1075`, `:1475-1476`, `:1822-1827`: `2.17.0` occurrences and the erratum.
- `/var/log/pacman.log:1943`, `:2929`: walker upgrade lines (grep only; no pacman, systemctl or other host command run).
- `corpus/knowledge/walker-route-r18.md:33`; `corpus/knowledge/theme-route-r18.md:158-161`.

## Limits

- Did not run `fetch-verify.py`, `receipt-check.py`, `fresh-pins.py`, `anchor-durability.py` or `supersede-sweep.py`. The 13/2 and 11-stale figures come from the pre-registration baseline file, not a fresh run.
- Did not re-fetch the S094 tree pages or the S084 docs.rs page. The two-fetch digests `1a3ddca5…`/`4d001dc8…` are as recorded by the closure spot-check, not re-observed.
- Did not verify the S084 GATE line's "no v3.0.0 tag exists" claim; the draft cites it only as the reopen seat's statement.
- Did not check whether the `XD`/`walker-route-r18.md` re-point or the crate tarball sha `2fb4332…` is correct; the draft takes it from the round-18 GATE line.
- Lessons are not committed to any lane file; the draft is a draft. Not checked: numbering collisions with other round-19 drafts (`drafts/` contained no other files at drafting time).
- Did not read the three tripwire drafts or the frozen F1/F2 items; out of this seat's assignment.
- Host: only read `/var/log/pacman.log` as bytes (grep). No pacman, sudo, systemctl or omarchy command. No git or jj command run.

## Installs

none
