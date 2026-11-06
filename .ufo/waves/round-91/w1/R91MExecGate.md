# R91MExecGate — C2 seat-report retention: independent expectation labels

Round 91, wave `w1`, seat R91MExecGate (leaf executor; C2 label seat). Lane:
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision
`cc0381db585cc44c3dfc13ced807409c32c45bb0` (master). Read-only git only; no mutating git/jj
command was run.

Writes (only):
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-91/controls/seat-reports-labels-r91.json`
  (sha256 `c1c660d59bd9a6d855ea51c504b49ee3f5b7d90975f361dfd46035a5c5e347f1`, 46 rounds, 18 fixtures)
- this report.

Independence: `build/check-seat-reports.c2.py` was **not opened and not executed**;
`controls/gen-c2-set-r91.py` was not opened; no C2 counter run, no candidate `--selftest`, no oracle
run. Read for lane conventions only: fleet `PROTOCOL.md` §Gate standard (`0 = clean`, `1 = failed`,
other codes declared; `2` used as setup/could-not-evaluate by the base-revision gate below) and the
docstring of `quality/check-receipt-presence.py` at `cc0381db` (a different, already-landed tool).
No DRAFT or measured counter value is claimed anywhere in this report.

## 1. Scope and method

Scope per the declaration/item: every `.ufo/waves/round-*/<wave>-dispatch.json` at the base revision.
For each such dispatch, `taskCall.tasks`; per task the **last** rendered trailer
`Report: write your scoped findings to <path>`; only if no rendered trailer exists, the **last**
plain trailer `Report: <path>` whose payload is path-shaped (no whitespace); no trailer at all =
untrailed. Path status, in order: unsafe (absolute, `..` component, or a non-regular target) →
missing (no tree entry) → empty (zero-byte blob) → present (regular blob, size > 0).

Commands (all at `cc0381db`, all exit 0 unless stated):

| # | command | result |
|---|---|---|
| 1 | `git -C <lane> cat-file -t cc0381db…` | `commit` |
| 2 | `git -C <lane> rev-parse --show-toplevel` | lane path |
| 3 | `git -C <lane> ls-tree -r --name-only cc0381db -- .ufo/waves` | 75 `dispatch.json` files; 61 match the in-scope glob |
| 4 | `git -C <lane> cat-file -p cc0381db:<dispatch>` ×61 | all parse as JSON; `taskCall.tasks` present in all |
| 5 | `git -C <lane> ls-tree -r -l cc0381db -- .ufo` | mode/type/size for every report path |
| 6 | `python3 extract.py extracted.json` (scratch) | `dispatches=61 rounds=46 errors=0 tasks=1732` |
| 7 | classification script over (4)+(5) | `present=1599 missing=133 empty=0 symlink=0` |
| 8 | `git cat-file -s/-t cc0381db:<path>` on a fixed sample of 16 seats | 8 present → rc 0, blob, sizes 579–19920; 8 missing → rc 128 |
| 9 | totals arithmetic assertion | rc 0 |
| 10 | fixture trailer self-check (18 fixtures) | rc 0 |

No host mutation: no `gio`, no `xdg-*`, no application launch, no service action, no pacman
transaction, no sudo. No tool was installed or upgraded.

## 2. Result at the base revision

`rounds=46 waves=61 seats=1732 trailered=1732 present=1599 missing=133 empty=0 unsafe=0 untrailed=0`

This equals the declaration's draft `--all` line
(`rounds=46 waves=61 seats=1732 trailered=1732 present=1599 missing=133`) exactly; the 61-dispatch /
46-round set is the only reading of the glob that reproduces it (see §5).

**Coverage gap in the live set:** all 133 live findings are SR01 (missing). There is **no live
SR02 (empty), SR03 (unsafe) or SR04 (untrailed) case anywhere at base** — those three classes are
exercised only by the fixtures in §6 (and by whatever the candidate's own selftest adds). The
`--all` measurement at `cc0381db` therefore cannot distinguish a gate that implements empty/unsafe/
untrailed correctly from one that does not, beyond the fixtures.

Rounds with findings (25 of 46; the other 21 rounds are clean):
37, 38, 43, 44, 45, 46, 47, 50, 51, 53, 67, 68, 69, 70, 82, 84, 85, 86, 87, 88, 89 have zero
missing/empty/unsafe/untrailed.

| round | waves | seats | present | missing |
|---|---|---|---|---|
| 39 | w1 | 64 | 60 | 4 |
| 40 | w1 | 64 | 63 | 1 |
| 41 | w1,w2 | 68 | 67 | 1 |
| 42 | w1 | 36 | 0 | 36 |
| 48 | a4r1,w1,w2 | 97 | 92 | 5 |
| 49 | w1 | 45 | 43 | 2 |
| 52 | w1,w2 | 100 | 98 | 2 |
| 54 | w1,w2 | 69 | 66 | 3 |
| 55 | w1,w2 | 77 | 75 | 2 |
| 56 | w1,w2,w3 | 142 | 134 | 8 |
| 65 | w1 | 12 | 9 | 3 |
| 66 | w1 | 12 | 11 | 1 |
| 71 | w1 | 13 | 2 | 11 |
| 72 | w1 | 13 | 4 | 9 |
| 73 | w1 | 13 | 4 | 9 |
| 74 | w1 | 13 | 0 | 13 |
| 75 | w1 | 13 | 10 | 3 |
| 76 | w1 | 13 | 12 | 1 |
| 77 | w1 | 12 | 9 | 3 |
| 78 | w1 | 13 | 11 | 2 |
| 79 | w1 | 14 | 13 | 1 |
| 80 | w1 | 14 | 11 | 3 |
| 81 | w1 | 14 | 9 | 5 |
| 83 | w1 | 10 | 7 | 3 |
| 90 | w1 | 13 | 11 | 2 |

The JSON carries the full per-round `missing`/`empty`/`unsafe`/`untrailed` triples
`[wave, seat, path]`, so a counter can compare lists, not just counts.

Round 90 (the M90-4 failure the claim is built on) — exactly two seats:
- `.ufo/waves/round-90/w1-dispatch.json:120` seat `R90MScoutSources` trailers
  `.ufo/waves/round-90/w1/R90MScoutSources.md` → no tree entry (SR01).
- `.ufo/waves/round-90/w1-dispatch.json:125` seat `R90MScoutCases` trailers
  `.ufo/waves/round-90/w1/R90MScoutCases.md` → no tree entry (SR01).
Round 89 in both waves (`w1`, `r1`) is clean; round 86/87/88 are clean.

## 3. Trailer grammar at base (what the gate will actually meet)

- 1724 tasks use the rendered trailer; 8 use only the plain trailer. The plain eight are the
  round-88/89 residual calls `r1`: `.ufo/waves/round-88/r1-dispatch.json:14,19,24,29` and
  `.ufo/waves/round-89/r1-dispatch.json:14,19,24,29` (`R88MResidCasesC1/C2/Critic/Mut`,
  `R89MResidC1/C2/Mut/Critic`). All eight report files are present and non-empty, so a gate that
  accepts only the rendered form would emit 8 false findings (or miss 8 reports) on a clean pair of
  rounds.
- In every one of the 1732 tasks the chosen trailer is the **final non-empty line of the task text**;
  no task has two differing rendered trailers; no task has a plain line after its rendered trailer.
  "Last line" and "last matching line" coincide at base, so the corpus cannot distinguish strict
  last-line parsing from last-match parsing.
- Three tasks carry a `Report:` line that is **prose, not a path**, *before* their rendered trailer:
  `.ufo/waves/round-45/w1-dispatch.json:413` (ScoutFrontier: "Report: the exact Frontier text the
  new entry moves …"), `.ufo/waves/round-68/w1-dispatch.json:129` (R68ExecHazard: "Report: draft
  sha256 and diff, the hazard pair …"), `.ufo/waves/round-88/w1-dispatch.json:169` (R88MMutTester:
  "Report: both tables and the survivor list."). A gate must not treat these as trailer paths (they
  are not path-shaped); at base the rendered-priority rule already excludes them. Fixture
  `fx15-prose-report-no-trailer` pins the prose-only case.
- All 1732 chosen paths are relative, under `.ufo/`, end in `.md`, and contain no whitespace, quote
  or glob character. At base: 0 absolute, 0 `..`, 0 symlinked targets, 0 zero-byte blobs.

## 4. Excluded dispatches (14 `dispatch.json` files)

Not in scope because they are not `<wave>-dispatch.json` directly under a round directory:

```
.ufo/waves/round-13/w1/dispatch.json   .ufo/waves/round-14/w1/dispatch.json
.ufo/waves/round-15/w1/dispatch.json   .ufo/waves/round-16/w1/dispatch.json
.ufo/waves/round-16/w2/dispatch.json   .ufo/waves/round-17/w1/dispatch.json
.ufo/waves/round-17/w2/dispatch.json   .ufo/waves/round-18/w1/dispatch.json
.ufo/waves/round-18/w2/dispatch.json   .ufo/waves/round-19/w1/dispatch.json
.ufo/waves/round-19/w2/dispatch.json   .ufo/waves/round-20/w1/dispatch.json
.ufo/waves/round-20/w2/dispatch.json   .ufo/waves/round-50/w1/ScrQualityR50/fixtures/w1-dispatch.json
```

The 13 legacy `round-13…20/wN/dispatch.json` files and the round-50 fixture-internal dispatch are
the only other `dispatch.json` shapes at base (75 total = 61 + 14). Including them would change the
seat/round totals; the declaration's draft totals equal the 61-file set, so the exclusion is the
intended scope. If the frozen gate is meant to cover them, its `--all` totals cannot match the
draft line.

## 5. Finding-id mapping (reconciliation required)

No `SR0x` id exists at base (`git grep` over `*.md`/`*.py` at `cc0381db` finds no such id; the only
hits for the pattern are prose "seat report"). This seat labels the ids from the declaration's case
order and the item's status list:

| id | class |
|---|---|
| SR01 | missing — trailer path has no tree entry / no file |
| SR02 | empty — zero-byte blob / file |
| SR03 | unsafe — absolute, `..` component, or non-regular target (symlink) |
| SR04 | untrailed — no rendered and no plain path trailer |

The L1 must reconcile this mapping with the candidate's numbering before freezing expectations; if
the candidate numbers differently, only the ids need re-mapping — the per-round seat/path lists and
the fixture expectations are independent of the numbering.

## 6. Fixtures (18, `--worktree`, plain directory as root/cwd, no VCS)

`expected_summary` counts are included in the JSON where defined (rc 0/1); they follow the counts
definition `seats / trailered / present / missing / empty / unsafe / untrailed`. Rounds 900–917
avoid collision with real rounds.

| id | argv (round) | rc | ids | conf. | case |
|---|---|---|---|---|---|
| fx01-present | 900 | 0 | — | firm | regular non-empty report |
| fx02-missing | 901 | 1 | SR01 | firm | trailer path absent |
| fx03-empty | 902 | 1 | SR02 | firm | zero-byte report |
| fx04-unsafe-absolute | 903 | 1 | SR03 | firm | trailer `/etc/hostname` (exists on host; must be rejected, never read) |
| fx05-unsafe-dotdot-escape | 904 | 1 | SR03 | firm | trailer `../outside.md` |
| fx05b-unsafe-dotdot-inner | 905 | 1 | SR03 | firm | `…/w1/../w1/SeatF.md` normalises to a present file; literal `..` still unsafe |
| fx06-untrailed | 906 | 1 | SR04 | firm | no `Report:` line |
| fx07-plain-trailer | 907 | 0 | — | firm | plain form accepted (round-88/89 `r1` shape) |
| fx08-rendered-wins-residual-plain | 908 | 0 | — | firm | plain line LAST but rendered trailer wins; plain target absent, not a finding |
| fx09-two-rendered-last-wins-clean | 909 | 0 | — | firm | first rendered absent, last present → clean |
| fx09b-two-rendered-last-wins-missing | 910 | 1 | SR01 | firm | last rendered absent; finding must name `Absent.md`, not fall back |
| fx10-dispatch-not-json | 911 | 2 | — | firm | unparsable dispatch = setup error, not zero seats |
| fx11-dispatch-no-taskcall | 912 | 2 | — | firm | valid JSON without `taskCall.tasks` = setup error |
| fx12-round-without-dispatch-explicit | 913 | 2 | — | advisory | explicit `--round` with no dispatch = setup error |
| fx12b-round-without-dispatch-all | all | 0 | — | advisory | `--all` skips a dispatch-less round directory (rounds 13–20 shape) |
| fx13-symlinked-report | 915 | 1 | SR03 | advisory | symlinked trailer target (target non-empty, inside root) |
| fx14-mixed-summary | 916 | 1 | SR01,SR02 | firm | 3 seats: summary counts + one finding per seat |
| fx15-prose-report-no-trailer | 917 | 1 | SR04 | advisory | `Report: <prose>` only → untrailed, not a bogus path |

Advisory rows are the three places where the declaration does not fully pin semantics (dispatch-less
round directory, symlink class, path-shape of a plain trailer); they are labelled with the reading
this seat argues for, with the reason in `expected_summary`/`reason` fields. A disagreement there
should be resolved in the freeze, not silently dropped (the fixture is still a falsifier for the
other reading).

## 7. Risks / limits

- The labels grade `cc0381db` only. Round 91 has no dispatch at that revision; this round's own
  `--worktree --round 91` run is the L1's records duty, not part of this label set.
- The live set exercises SR01 only (§2); SR02–SR04 rest on fixtures. A counter that scores only the
  `--all` counts would not falsify those classes.
- The id mapping is inferred (§5).
- `trailered` counts seats with any trailer line (rendered or plain), including an unsafe one; the
  base data has no unsafe seat, so the corpus does not pin that definition either.
- The three advisory fixtures encode one defensible reading each; the L1 should adjudicate them
  before the freeze rather than treat a mismatch as a silent label error.

## 8. Installs / scratch

No installs, no upgrades. Scratch
`/fast/scratch/hyaku/mado-r91/R91MExecGate` (clone-free: the extraction script ran read-only
against the lane) was removed at seat exit; the only retained output is the labels JSON above.
