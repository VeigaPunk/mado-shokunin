# ScrLessonSkeleton — round-41 w1: lesson skeleton (final)

Deliverable: `.ufo/waves/round-41/w1/ScrLessonSkeleton/round-41.md` (207 lines) — the round-41 lesson draft for
`corpus/lessons/round-41.md`. Nothing tracked was edited; no git/jj mutation; no pacman; no compositor, socket or
Wayland-client contact; no journal verb beyond the read-only forms (none was needed — the own-work journal is the
committed receipt).

## What the draft contains

- **Round intent**: registration `.ufo/waves/round-41/registration.md`, freeze `60c39141…`, base `ab2bfaa…`; C1
  (`tools/mado-globals.py`, PRED-C1-r41-v1, target 24/24, base 0/24) and C2 (`corpus/knowledge/hyprland-focus-grab-r41.md`,
  PRED-C2-r41-v1 clauses a–i, target 1/1, base 0/1); host Hyprland 0.56.2 `efb5099…`, xdph v1.4.1 (held S037,
  `corpus/SOURCES.md:49`); **shape: two v1 waves** (`w1` = 34 seats at `cd950ec`, `w2` residual); axes operability +
  coverage with the base axis receipt quoted; the freeze/dispatch conflict stated verbatim (below).
- **`## Gate`**: seven column-0 `GATE S283…S289` lines carrying the digests recomputed from the committed fetch receipts and
  the quotes entry draft A uses, plus `ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md as
  corpus/knowledge/hyprland-focus-grab-r41.md` and two `REFUSE` lines (`privileged-client-surface-r29.md`; 
  `focus-control-surfaces-r28.md` §3 = the Japanese channel). The GATE-line *shape* is an HTML comment **outside** the
  section (placeholders are not landable text); no `<sha>` placeholder anywhere. Two **conditional** lines sit in a second
  comment above the section, in landable form: S037 (entry draft A cites the held row; needs
  `fetch/xdph-installed-version.txt` committed byte-identically first — 1442 B, sha256 `4294737a…`, verified against
  `w1/ScrEntryA/s037-installed-version.txt`) and S290 (only if the entry cites `input-capture-v1.xml`; draft A does not).
- **Assimilation ledger** (admit / refuse / not-adopted, with `PROVINCE.md:75` for the localization refusal) and the id map by
  document (S283 focus-grab-v1.xml, S284 FocusGrab.cpp, S285 quickshell grab.cpp, S286 xdph PortalManager.cpp, S287 issue #565,
  S288 hyprland-protocols README, S289 own-work journal; `Hyprland-FocusGrab.hpp` carries no id).
- **Round-40 closure items D1–D4** with the state measured this seat.
- **`## Mistakes` M41-1 … M41-8**, each with class / evidence pointer / captured-by / fix / whether a control shows the fix can
  fail.
- A `### QUALITY.md criteria` note (no criterion claimed; each candidate must cite an M41 id and a failing control), the
  `considerthese` pointer (owned by `ScrConsiderthese`), and the census/measurement section with the exact commands and base
  values.

## Checks run (commands and outputs)

| check | command | output |
|---|---|---|
| Gate lines verify against committed bytes | `python3 -I .ufo/waves/round-41/w1/ScrLessonSkeleton/quotes.py --repo . --rev 60c3914154333180450d5da27ba222d5763cc56a --lesson …/round-41.md` | `S283 … ok=1` … `S289 … ok=1` (bytes 5447/6242/2568/24182/475170/1903/19130; words 11/3/11/5/10/9/5; `in_norm=True` each), `admits=1 refuses=2`, `QUOTES: gates=7 bad=0`, rc 0 |
| entry-draft gate lines (A) | same norm/sha checks on `w1/ScrEntryA/gates.txt` | 8/8 `ok=1` (S283–S289 against committed receipts, S037 against the seat copy, 4–11 words each) |
| entry draft A binds its quotes (read-only) | per-id scan of `w1/ScrEntryA/hyprland-focus-grab-r41.md` for id + quote on one line | S283:19, S284:43, S285:83, S286:69, S287:99, S288:103, S289:61, S037:73; census line `journal sessions=2 adverts=78 interfaces=63 focus_grab=1` exactly once (line 63) |
| own-work census | the counter's own `journal_counts()` on `fetch/xdph-journal.txt` | `(2, 78, 63, 1)` |
| M41-1 single-edit equivalence | `python3 -I quality/counters/c1-r41-globals.py --repo . --rev 60c3914… --tool …/m09-<variant>.py` ×3 | `m09-a-line139.py` → `fixtures=24/24 … TARGET_MET` rc 0 (nonce `f274be9b2cebe486`); `m09-b-line227.py` → `24/24 … TARGET_MET` rc 0 (nonce `c9ea24a7e48b8c7b`); `m09-c-both.py` → `23/24 … TARGET_MISSED` rc 1 (nonce `fb1f5c8e72297d1e`) |
| base facts | `git ls-tree -r --name-only ab2bfaa corpus/knowledge/ \| grep -c '\.md$'`; `git show ab2bfaa:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`; `git ls-tree --name-only ab2bfaa tools/`; `git grep -lEi 'focus_grab\|focus-grab\|focus grab' ab2bfaa -- corpus PROVINCE.md SKILL.md tools` | 58 entries; 219 rows; 10 tools (no `mado-globals.py`); grep rc 1, no output |
| freeze tree | `git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/` | 21 paths; the nine `fetch/` receipts, both controls, the reference, the eight receipts, `registration.md` |
| leftovers | `GIT_OPTIONAL_LOCKS=0 git status --porcelain` | `?? .ufo/waves/round-41/assimilation/`, `?? …/w1.ready`, `?? …/w1.ready.dispatched`, `?? …/w1/` |
| round-40 tip axis receipt | `git ls-tree -r --name-only ab2bfaa quality/receipts/` | `axis-520c631d…txt` (round 36) and `red-axis-publication-stale-at-data-commit.txt` only |
| control distribution | `grep -o 'fixtures=[0-9]*/24' receipts/ctl-c1.txt \| sort \| uniq -c` | 10 mutants at 23/24, 9 at 22/24, 6 at 24/24 (1 reference + 1 selftest-echo + 4 cheats) |

`quotes.py` mirrors PRED-C2-r41-v1 clause d exactly: it imports the counter and uses its `GATE_RE`, `norm()`, `MIN_RECEIPT`,
`section()`, `ADMIT_RE`, `REFUSE_RE`, and rejects an indented `GATE S` line. It reads receipts with `git show` only.

## Findings (what each attacks or supports)

1. **M41-1, measured, attacks `registration.md:45`** ("43 single-defect mutants / single-edit cheats"): the reference dedupes
   twice (`c1/ctl-ref-tool.py.txt:139`, `:227`), so dropping either site alone leaves an equivalent mutant (24/24 MET, rc 0,
   two nonces); only the two-site edit is killed (23/24 MISSED, rc 1). Control row `ctl/run-c1-controls.py:44` already carries
   both edits. Fix shown able to fail: `receipts/ctl-c1.txt` M09 23/24.
2. **M41-2, attacks the fixture margin**: ten of the 43 mutants are killed by exactly one fixture (`receipts/ctl-c1.txt`: M09,
   M12, M19, M20, M21, M23, M24, M26, M27, M37 at 23/24). Declared limit, no fix.
3. **M41-3, recurrence of a routed defect**: the dispatch marker is untracked again for round 41, while round-40's marker is
   tracked (committed by `60c3914`). No instrument asserts the closure tree is clean.
4. **M41-4, routed defect 2 still open**: no `quality/receipts/axis-<40hex>.txt` for the round-40 tip; the conjunct that names
   the rule (`tip_axis_transcript`, `quality/check-evidence-pointers.py`) is round-36-scoped, and was proved able to miss
   (`.ufo/waves/round-36/w1/reports/ExecPtrFixtures.md:45`: `tip_axis_transcript=0 … TARGET_MISSED`).
5. **M41-5, the conflict below**, plus 34 < the registration's own band floor of 64.
6. **M41-6, new this round, attacks the C2 Gate contract**: clause d requires a receipt under `.ufo/waves/round-41/fetch/` for
   *every* cited id, but the frozen fetch set has no receipt for held row S037, which the entry prompts invite the drafts to
   cite ("Cite at least one held id if it fits (S037 xdph release)", `w1-spec.json`). The repair is one byte-identical copy of
   `w1/ScrEntryA/s037-installed-version.txt` (1442 B, sha256 `4294737a…`) into `fetch/` by the L1, then the S037 line in the
   comment above the Gate. Clause d is shown able to bite by `receipts/ctl-c2.txt` N03/N14 (`clause d:0`).
7. **M41-7, disclosure (M40-5 pattern)**: five falsifier seats are dispatched against v1 predicates; the registration's own
   residual clause allows a `registration-v2.md` before data. Not a gate.
8. **M41-8, watch (M40-6)**: `ConnCrossClaim` is dispatched again; its report is at the correct path (104 B) as of this read,
   so the defect has not recurred.

## Coordination with `ScrEntryA` (answered; no lane bytes written for it)

`ScrEntryA` asked this seat to (1) copy its `s037-installed-version.txt` into `.ufo/waves/round-41/fetch/` and (2) supply the
clause-i lines. Answer sent: (2) the three lines are in the draft and were quoted back verbatim, with the notes that
`ADMIT_RE` accepts one `.md` token per line (so an `assimilated-from:` naming r14 *and* r28 must stay prose), that the
registration refuses r28's *section 3* rather than the file, and that clause i also refuses any cited location containing
`amgsk.dev`; (1) **declined** — `fetch/` holds frozen receipts, this seat's write scope is its own directory, and the L1 is the
only integrator, so the tenth receipt is the L1's commit (M41-6 records the exact sha). The draft's Gate quotes were then
switched to draft A's exact strings (clause g binds Gate quote to entry line), re-verified against the receipts (`gates=7
bad=0`), and draft A's id/quote binding was checked read-only (see the table above). `ScrEntryA` then confirmed draft A is final
(`ids=8 quotes=30 failed=0`, `SIMULATED b/g/h -> OK`), so the draft records the landed Gate as exactly eight lines — the seven
committed ones plus S037 once its receipt is committed — and that S290 must not list the entry in `used-by`.

## Conflict, verbatim, for the canonical judge

`registration.md:4` (frozen at `60c3914`, unchanged in the worktree — `git diff 60c3914 -- …/registration.md` empty):

> Shape: one v2 wave `w1` of 64 seats (policy v2, band 64–128), no residual call, round total 64.

The dispatched wave (`cd950ec`, subject `round-41: wave w1 spec and dispatch (34 seats)`; `w1-spec.json` `items` length 34;
`w1.ready` `{"lane":"mado","round":41,"wave":"w1",…}`) and the assignment both state **34 seats, w1 of two v1 waves**. The
draft records the assignment's shape ("two v1 waves") and carries the registration line as a recorded conflict (M41-5); it
does not edit the registration.

## Touched surfaces

Written, all under the seat directory `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w1/ScrLessonSkeleton/`:

- `round-41.md` — the deliverable (draft lesson, 207 lines).
- `quotes.py` — the Gate verifier (re-runnable; imports the frozen counter, read-only).
- `m09-a-line139.py`, `m09-b-line227.py`, `m09-c-both.py` — three measurement fixtures (copies of `c1/ctl-ref-tool.py.txt`
  with one/two dedupe sites dropped); not deliverables, kept so the M41-1 claim is replayable.
- `m09-a-line139.out`, `m09-b-line227.out`, `m09-c-both.out`, `m09-rc.txt` — their full counter outputs and exit codes.
- `.ufo/waves/round-41/w1/ScrLessonSkeleton.md` — this report.

Not written: the entry, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/lessons/round-41.md`, `corpus/QUALITY.md`, `tools/`,
`.ufo/waves/round-41/fetch/`, the counters/controls/reference, the jj/git index, the shokuknow checkout.

## Out of scope (owned by other seats / the L1)

- The C2 entry text (`ScrEntryA/B/C`), the registry rows (`ScrRowsDraft`), the README index row, criteria 69+
  (`ScrQualityCriteria`), the considerthese proposal (`ScrConsiderthese`), SKILL/PROVINCE rows (`ScrSkillProvince`), the id
  guard (`ExecAssimIdGuard`).
- No end-to-end C2 counter run: the entry and rows are not landed, so `admitted` cannot be scored; only the Gate half (clause d)
  is verified here, by a mirror that imports the counter's own regexes and `norm()`.
- No commit, no push, no verification of the lane's gates (main agent's job). Tooling: nothing installed.

## For the L1 before landing the lesson

1. Commit `fetch/xdph-installed-version.txt` byte-identically (sha256 `4294737a…`, 1442 B) and promote the S037 line out of the
   comment: the final entry (draft A) cites eight ids, so the landed `## Gate` must hold exactly eight GATE lines. Do **not** add
   the S290 line, and S290's registry row must not list the C2 entry in `used-by` (draft A does not cite it) (M41-6).
2. The Gate quotes are draft A's OBS-line quotes; if the entry text changes, re-take them and re-run
   `quotes.py --rev <data commit>` (the invariant is Gate quote == entry line quote, clause g).
3. Fill the census section with the data-commit measurements; commit the tip axis transcript (M41-4) and the two dispatch
   markers (M41-3) in the closure commit.
