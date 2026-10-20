# ReviewNavigation — U4 joins and same-count false positives (mado round 13, w1)

Seat: MadoR13.ReviewNavigation (reviewer, leaf). Date: 2026-10-20. Baseline revision: `7dcb785b7b943d03703181b218d7860a7b43007b`.
Scope: read coverage counter, indexes and registry; name the exact U4 joins and the same-count checks a final measurement must pass. Read-only. No edits to shared files, no builds, tests, lint, smoke runs, or `tools/mado-verify.sh` invocations. Tooling installed or updated: none. Source opens: none external (all evidence is repo-internal, cited by path:line).

Tags: [OBS] read or measured here; [INF] inference from [OBS]; [UNK] not settled by the repo.

## 1. Baseline census (OBS)

- Navigation counter fence (`SCORECARD.md:69-89`) at HEAD: `git show HEAD:SCORECARD.md` fence sha256 = `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`, matching `SCORECARD.md:236`. Notes at `7dcb785` = 26 (`git ls-files corpus/knowledge` = 26); README rows = 26; distinct rows = 26.
- Source-cited head-15 entries (`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/*.md`) = 4: `config-drift-r12.md` (no `covers:`), `hyprland-config-era-r12.md:6` `covers: U2`, `window-rule-effects-getprop.md:6` `covers: U1`, `xdg-portal-routing-r12.md:6` `covers: U3`. Raw `^covers:` lines in the whole corpus = 3, all within head-15, none outside.
- Registry `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`: 39 rows (IDs S001–S039, contiguous, no duplicates). Tier A=35, B=1 (S008), C=3 (S010, S011, S012).
- **Status histogram drift [OBS]:** current HEAD = `mined=27 queued=9 rejected=3`. The recorded round-12 census (`.ufo/evidence/round-12/after.txt:58`, at `6e3b75f`) = `mined=28 queued=9 rejected=2`. The change is the post-review in-place flip of S030 mined→rejected (`SOURCES.md:91`). Same total (39), different histogram: a count-only census cannot see this.
- Queued U4 candidates: S005 (wayland-protocols README, anchor `README.md §Protocol phases @ main 3dac056d`, `SOURCES.md:16`, used-by `—`), S006 (`SOURCES.md:17`), S007, S008 (B), S009, S010 (C, "never sole support", `SOURCES.md:21`). No row is `mined` for U4 today.
- Index: `corpus/README.md` rows 12–37 (one per note); `Frontier` lines 70–94 keep "protocol phase and advertised globals" open (`README.md:92-93`).

## 2. Current counter, read line by line (OBS)

Round-13 counter text, `SCORECARD.md:237` and `.ufo/evidence/round-12/after-measure.sh:23-25`:

| Step | Command (abridged) | What it actually measures |
|---|---|---|
| A (entries) | head-15 `^source:.*\bS[0-9]{3,}\b` per file | any S-token on the source line, mined or not |
| B (numerator) | `after-measure.sh:24` `grep -oE '^covers: U[1-7]'` on the files passing A, then `sort -u` | distinct covers tokens **with no mined check** |
| C (join) | `after-measure.sh:25` each registry row's used-by vs. each cited ID | prints violation lines only; prints nothing on success |
| D (raw) | `SCORECARD.md:237` `grep -cE '^covers: U[1-7]' corpus/knowledge/*.md` | line count over all notes; no source join |

Consequences (all demonstrated with stdin-only fixtures; no files written):
- **F1 — numerator not intersected with the mined join.** Fixture `source: S011` (rejected row) + `covers: U4` passes step B and yields `covers: U4`. The rubric (`SCORECARD.md:237`: "an item is covered when an admitted entry … cites a `mined` row") says it must not count. The round-12 reviewer requested exactly this intersection (`.ufo/evidence/round-12/l2-reviewer.md:66-70`); `after-measure.sh` implements it as a separate violation printout, not as the numerator. A U4 note citing only rejected or queued rows inflates 4/7 while step C prints a line that a headline reader can miss.
- **F2 — raw counter is vacuous.** Step D counts lines, not distinct items or joined notes (`l2-reviewer.md:66-68`: 3 lines, 2 distinct on the fixture). It must not be reported as the score.
- **F3 — token truncation.** `grep -oE '^covers: U[1-7]'` is unanchored at the right: `covers: U10` → `covers: U1` (demonstrated); `covers: U1, U4` → `covers: U1` with U4 hidden (demonstrated). A typo or multi-value line silently changes the distinct set.
- **F4 — source-less covers are excluded silently.** `source: none` + `covers: U4` is dropped by step A and not reported by step C (the loop over S-IDs is empty), but step D counts it. Steps B/C and D disagree and the final measurement has no line that says so (demonstrated).
- **F5 — used-by check is whole-file.** Step C uses `grep -qw "$i" "$p"` over the whole note (`after-measure.sh:25`). A note whose head-15 source line does not cite S005 but whose Rejected section mentions "S005" passes the used-by-cites test (demonstrated). Reciprocity must be checked against the head-15 source line.
- **F6 — substring path match.** `index($3,f)` (`after-measure.sh:25`) matches `corpus/knowledge/a.md` inside `old/corpus/knowledge/a.md` (demonstrated). Low likelihood; fix by exact comma-split equality.
- **F7 — contract census skips `—`.** `SOURCES-CONTRACT-v1.md:80` skips used-by `—`, so a row flipped to `mined` with used-by `—` passes the census and is caught only by step C. The contract's own census must not be the sole used-by gate.
- **F8 — tier is not checked.** Neither step A/B/C nor the contract census tests that a note's cited rows include an A-tier row for the claim scope. `SOURCES-CONTRACT-v1.md:26-30` says C is never sole support and `community` is never A (the latter is checked, line 78; the former is not). A U4 note sourced only from S010 (C) or S008 (B) would count.
- **F9 — numerator and denominator at different states.** `after-measure.sh` reads notes and registry from the working tree (`corpus/knowledge/*.md`, `/tmp/mado-r12-rows.tsv` from `$S`), but navigation reads the committed `REV` (`SCORECARD.md:70-89`, `git ls-tree`/`git show`). With a dirty tree the two numbers describe different states. The `after-measure.sh:8` header records the dirty count but does not fail on it.
- **F10 — same-count aggregation hides which file covers which item.** `sort -u` (`after-measure.sh:24`) prints only distinct tokens. Two notes both `covers: U4` yield one line. Print `file:covers` pairs instead.
- **F11 — navigation can be correct yet silent about the new note.** The counter is revision-bound. A note present only in the working tree is invisible to it (not in `ls-tree REV`); a README row added without its note is `dangling=1`, exit 1. So the navigation count is honest only for the cited REV; it says nothing about uncommitted notes.

## 3. Exact U4 joins the final measurement must pass (recommendation; [INF] unrun)

Planned identifiers, from the round-13 dispatch (`.ufo/waves/round-13/w1/spec.json` items ProtocolPhases, GlobalCapture, GlobalDocs): note `corpus/knowledge/wayland-protocol-boundaries-r13.md`; new registry rows S040 (GOVERNANCE), S041 (own-work globals capture, `globals.json`), S042 (supersedes S006, only with exact page revision), S043 (core registry spec, if needed). None exists yet at `7dcb785`.

- **J1 note exists at REV:** `git ls-tree --name-only REV corpus/knowledge/` contains the slug.
- **J2 header, head-15 only, exact:** `verified-at: 2026-10-20`, `recheck:` valid (date or `90d`/`180d`/`on-release`), a `source:` line listing ≥1 S-ID, and exactly one line `covers: U4` matched with `^covers: U[1-7]$` (anchored; no `, U5`, no suffix).
- **J3 each cited ID joins a registry row at REV:** `status == mined` (not `queued`/`rejected`), and the row's `used-by` split on commas and compared by exact equality to `corpus/knowledge/<slug>.md`.
- **J4 reciprocity against the head-15 source line:** every mined row whose used-by names the slug must be cited on that slug's head-15 `source:` line (not merely present in the body). Inverse: no note cites a row whose used-by omits it.
- **J5 tier support:** the note's cited rows include ≥1 tier-A row whose scope is the U4 claim; no U4 claim rests on C-tier (S010, S011, S012) and no claim rests on B-tier (S008) alone. Community is never A (existing census line 78 holds).
- **J6 registry set, not count:** the ID set of `corpus/SOURCES.md` at REV equals the expected set (S001–S039 plus the allocated new IDs, no reuse, no duplicates via `uniq -d`). Expected cardinality 39 + k. The round-12 histogram (28/2) must be re-recorded, not carried; the count alone cannot detect a same-count replacement.
- **J7 index:** exactly one README row `^| \`knowledge/<slug>.md\`` at REV (navigation counter reports `indexed=27/27 missing=0 dangling=0 duplicates=0`, exit 0, with the fence sha `8b59b503…` unchanged). Frontier lines 92-93 are edited only for the part the note closes; "unexercised behavior" stays open unless a row closes it.
- **J8 lesson log:** the status change S005 queued→mined and each new row is logged old→new in `corpus/lessons/round-13.md` (`SOURCES-CONTRACT-v1.md` rules 1–2). No such lesson file exists at `7dcb785` (`corpus/lessons/` ends at `round-12*.md`). This join is manual.
- **J9 anchor revision:** S005's anchor is `main 3dac056d (2026-01-16)`. The note's `verified-at` must not predate the row's `opened`, and the anchor SHA must be the one the note quotes. Not automated [UNK].

## 4. Same-count false-positive checks (each must FAIL on a bad fixture before the final number is accepted)

1. Rejected-only source + `covers: U4` → must not count (F1).
2. Queued-only source (S005 still queued) + `covers: U4` → must not count.
3. Two notes both `covers: U4`, one valid, one with a dangling S-ID → must print the violating file, and the headline must name the valid file only.
4. `covers: U10` and `covers: U1, U4` → must FAIL, not tokenize (F3).
5. `source: none` / missing `source:` + `covers: U4` → must appear as a violation, not be silently excluded (F4).
6. Body-only mention of S005 (not in head-15 source) → must not satisfy reciprocity (F5).
7. Mined row with used-by `—` → must FAIL in the join (F7).
8. Registry: one row replaced by another with the same ID count (39 → 39, statuses shift) → must FAIL the ID-set check (J6); the round-12 histogram drift (28/2 vs 27/3) must be reported as a change, not an inconsistency.
9. Dirty tree at final measurement (any uncommitted `corpus/` or `tools/` change) → must FAIL or be reported as a different state (F9).
10. `covers: U4` with S-ID cited only in a footnote-like body line beyond line 15 → must not count (positional check, already correct in step A; keep it).

Positive control to keep: the three existing U1–U3 notes must still produce exactly `covers: U1`, `covers: U2`, `covers: U3` with the new join (no regression of 3/7).

## 5. Recommended measurement shape (spec, not run)

One per-file predicate, run against a committed REV (or a clean worktree at that REV), printing `file<TAB>covers<TAB>joined(yes/no)` for every note and then:
- distinct joined U-items (must equal `U1 U2 U3 U4`, count 4 → 5.7143 on the C1 rubric `SCORECARD.md:334-338`);
- raw `grep -c '^covers: U[1-7]$'` across all notes, which must equal the joined-note count (any excess is F2/F4 and fails the census);
- violations, one line each, exit 1 if any;
- registry ID-set equality, status histogram, `used-by` existence, and navigation counter at the same REV.

## 6. Verification gaps and risks

- Per-file predicate above is a spec; it has not been implemented or run here (no-test rule). [UNK] until the main agent runs it once.
- Topical fit of the source to "protocol phase vs advertised globals vs unexercised behavior" is not machine-checkable; it needs a named non-author reviewer (AXES F7 class). A counter pass proves registry joins, not that the note separates the three claims.
- C2 operability (set-blind census) and C1 coverage share the same defect class (count-only equality); the registry check (J6) is an instance of the same fix and should be reported with it.
- Host-side globals (S041) support only the host-scoped claim; the advertisement ≠ bind/use distinction needs a core-registry A-tier row (S043) and cannot rest on S006 (queued) or S041 alone.
- Nothing here is a verdict. Findings are for the planner (L1).

## Findings, by severity

- **MAJOR** — F1 numerator not intersected with the mined join (`after-measure.sh:24`); fix in the final measurement before any 4/7 is recorded.
- **MAJOR** — F8 no tier check; C-tier sole support can satisfy the U4 count.
- **MAJOR** — F9 working-tree vs REV mixing in the same measurement.
- **MODERATE** — F2/F3/F4 raw counter, token truncation, silent source-less exclusion.
- **MODERATE** — F5/F6/F7 reciprocity and used-by edge cases.
- **MODERATE** — registry histogram drift 28/2 → 27/3 unrecorded in round-13 baseline; the ID-set check (J6) is needed.
- **MINOR** — F10 `sort -u` hides file identity; F11 navigation silent on uncommitted notes (true by design, record it).
