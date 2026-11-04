# R73ExecBattery — harm-watch battery, mado round 73 wave 1

Seat: executor (leaf). Assignment: prove the round harmed no measured surface at the instrument
commit `1459cca11fb5d3956a6e9a128217852dd0c28cb9` by running the six declared battery legs from
`/home/vgpnk/Projects/shokunin/mado-shokunin`, recording each command's own rc, and writing the
receipt `harm-watch-r73.txt` beside this report. No other move was assigned; none was taken.

## Axes (godspeed)

1. **Evidence fidelity** — every leg's rc taken from the command itself, never inferred from
   output text; a setup error is not a pass.
2. **Coverage** — all six legs run to completion, plus one out-of-band confirmation leg (5b)
   only where the frozen battery leg hit the wave's own in-flight state.
3. **No-harm of the probe itself** — read-only posture end to end; writes confined to this seat
   directory and scratch.

## Result table (receipt: harm-watch-r73.txt in this directory)

| leg | command | rc | last line (abridged where noted) |
|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` — matches the declared expectation exactly |
| 2 | `python3 -I quality/check-index.py --repo . --rev 1459cca1…` | 0 | `MADO_INDEX: … indexed=87/87 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| 3 | `python3 -I quality/check-tool-ledger.py --repo . --rev 1459cca1…` | 0 | `LEDGER: population=127 ledger_rows=127 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=…` |
| 4 | `python3 -I quality/check-axis-scores.py --repo . --rev 1459cca1…` | 0 | `MADO_AXIS: checked=3 mismatched=0 rev=…` |
| 5 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | **1** | `mado	E11	S449 missing used-by corpus/knowledge/guard-carrier-global-environ-r73.md` |
| 6 | `git rev-parse <5 paths>@1459cca1 <5 paths>@d3f6c9f5` | 0 | 10 blob ids printed; all five pairs identical |
| 5b | same argv as leg 5, out-of-band confirmation after the wave landed its knowledge entry | 0 | `mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` |

Leg 4 argv note: the given flag set was accepted unchanged (rc=0, no usage error), so there is
no alternate argv to report. Full leg-4 output: three `MADO_AXIS_ROW` lines — navigation 87/87,
calibration 86/86, operability 12/12, all `verdict=MATCH` — then the `MADO_AXIS` total line.

Leg 6 blob pairs (identical within every pair):
`c1-r72-landing-controls.py` 484c5d7e…; `c2-r71-shapes.py` 6b9c3019…; `c2-r70-carriers.py`
9afbbeed…; `tools/mado-verify.sh` 9113c7c0…; `quality/landing-counters.sh` 40db7db8….

## The one rc!=0 leg, fully diagnosed

- `sources-census.sh` exit contract (script header): 0 = clean or warnings; 1 = E/overdue
  findings; W-codes never change status. Leg 5 printed 45 lines: 41x W04 (duplicate-url across
  scopes), 1x W01 (S277 tierC note), 3x E11. Exit 1 comes from the three E11 findings only.
- The three E11 rows (S447 CPython `simple_stmts.rst`, S448 `os.rst`, S449 `subprocess.rst`) are
  this round's own uncommitted sources-plan rows at `corpus/SOURCES.md:397-399`. `git show
  HEAD:corpus/SOURCES.md` (HEAD = 1459cca1, dumped and searched) contains none of them — the
  pre-round registry has no E-class finding.
- E11 = "used-by path missing on disk": the rows point at
  `corpus/knowledge/guard-carrier-global-environ-r73.md`, which did not exist at run time. The
  claims declaration makes "the registry census must exit 0 **at round end**" and assigns the
  entry to seat R73ScribeEntryC2 (w1-dispatch.json); the 3x byte-identical fetch receipts for
  all three documents were present under `.ufo/waves/round-73/fetch/` at probe time.
- Between leg 5 and leg 5b the entry landed on disk (untracked, visible in `git status
  --porcelain`); leg 5b then exited 0 with `mado ok` and only the non-fatal warnings. The
  surface is healed pending the L1's round-end integration/commit of the working-tree files.

## Verdict

**No measured surface was harmed.** Selftest 460/460; index 87/87 clean; ledger TARGET_MET with
uncovered=0; axis table 3/3 MATCH at published values; every frozen counter/harness blob pair
byte-identical between instrument commit and base. The single failing leg is the round's own
declared in-flight sources-plan work, not damage to a held surface, and it validates clean once
the declared C2 knowledge entry is on disk (leg 5b, rc=0).

## Bounds, tooling, cleanup

- Writes: this directory only (`R73ExecBattery.md`, `harm-watch-r73.txt`). Scratch
  `/fast/scratch/hyaku/mado-r73/R73ExecBattery/` held the command captures, was cited in full in
  the receipt, and was deleted afterwards.
- Git usage strictly read-only (`rev-parse`, `show`, `status`); no git/jj write commands; no
  subagent dispatch; no background jobs; no message to `agent://all`.
- Tooling: no install or upgrade was needed; pacman untouched. No host probing, no writes to
  `~/.config`, `~/.local/bin`, `.ufo/state/`, or any committed lane file.

## Risks / blockers

- None for this seat. For the L1: leg 5 stays rc=1 until the round-73 working-tree files
  (notably `corpus/SOURCES.md` rows S447-S449 with the now-present knowledge entry) are
  integrated and committed at round end — that is the declared round-end obligation, re-check
  the census after integration.
