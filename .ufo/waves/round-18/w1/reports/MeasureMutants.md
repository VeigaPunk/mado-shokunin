# MeasureMutants — R17-V5 committed mutant receipts

Round 18, wave 1, seat `MadoR18.MeasureMutants`. Claim worked: C1 route
R17-V5 — the round-17 rubric-V tightenings were asserted but never shown
to bite. This report backs each tightening with a committed mutant in a
throwaway git repo built from `git archive d9a5a18`, plus a loose/tight
instrument comparison at that commit.

No lane git/jj write occurred. The lane was read only through
`git show`/`git archive`; every write landed in `/tmp`, plus the two
assigned lane files and this report. No package query, service,
compositor, input or screenshot operation ran.

## Verdict

All six tightenings bite. In every mutant the loose instrument
(`f52f43f`) credits at least one province entry that the tight instrument
(`d9a5a18`) does not, or the tight instrument refuses the measurement
outright. No tightening is recorded as a silent no-op.

| # | Tightening | Loose | Tight | Bites |
|---|---|---|---|---|
| M1 | exact `surface: P<n>` line | 4 / P1,P2,P4,P6 | 3 / P1,P2,P6 | **yes** |
| M2 | legacy credit pinned to three paths | 4 / P1,P2,P4,P6 | 4 / P1,P2,P4,P6 | **yes (entry-level)** |
| M3 | upstream https docs/spec/code row naming the surface | 5 / P1,P2,P3,P4,P6 | 4 / P1,P2,P4,P6 | **yes** |
| M4 | three-line section floor | 5 / P1,P2,P3,P4,P6 | 4 / P1,P2,P4,P6 | **yes** |
| M5 | registry-only parse | 5 / P1,P2,P3,P4,P6 | 4 / P1,P2,P4,P6 | **yes** |
| M6 | duplicate ids fail | 5 / P1,P2,P3,P4,P6 | exit 2, no c2 | **yes** |

M2's count cannot move: `LEGACY_MAP` maps only U1/U2→P1 and U7→P2, and
both provinces are already covered by the three pinned paths. The bite is
the covered-entry set: loose adds
`corpus/knowledge/input-debugging-boundaries-r15.md` to P1 via an
unpinned `covers: U1`; tight does not credit it.

## Instruments

| Role | Revision | sha256 | Staged path in the mutant repo |
|---|---|---|---|
| loose | `f52f43f8ea44f60b3c52e5cc5b2e5ab76d77be59` | `a280b3ab7c4dc21a25a954056f6a0c55187fd84dc06cfcddcb28e7f897d3508e` | `.ufo/waves/round-18/measure-loose.py` |
| tight | `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` | `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc` | `.ufo/waves/round-18/measure-tight.py` |

The sha256 of both revisions was verified with `git show <rev>:.ufo/waves/round-17/measure.py | sha256sum`
before the run, and again on the staged file before every invocation
(recorded per run in `mutant.<role>.instrument_sha256`). Use
`python3 -I` for every run.

**Adaptation recorded:** only file placement. Each instrument's bytes are
copied unmodified so that its own line
`REPO = Path(__file__).resolve().parents[3]` resolves to the throwaway
repo root. No instrument source byte, argument or environment variable was
changed.

**Extraction note:** the archive extraction skips symlink members whose
targets are absolute or escape the extraction root (the baseline tree
carries such fixtures under `.ufo/waves/round-17/tripwire/`). Neither
instrument reads those paths; every path either instrument reads
(`corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/`,
`tools/mado-tripwire.py`) is extracted verbatim.

## Method

Per mutant, independent of every other mutant:

1. `git -C <lane> archive d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` into
   a fresh `/tmp` directory; fresh `git init`; commit the baseline tree.
2. Run both instruments at the baseline commit and assert the baseline is
   identical for both: `c2.count == 4`, covered `P1,P2,P4,P6`, identical
   covered sets, empty `rejected`.
3. Apply exactly one mutant and commit it; assert the changed-file set
   equals the declared set.
4. Run both instruments at the mutant commit; compare `c2.count` and the
   per-province entry sets.

Harness: `.ufo/waves/round-18/measure-mutants.py`
(sha256 `075815bd5bbcf80fbf00a80ac9400ff9ec82082562a6691c1f5cc290da601d73`).
Evidence: `.ufo/waves/round-18/evidence/measure-mutants.json`
(schema `mado-measure-mutants-v1`, generated
`2026-10-20T15:50:02+00:00`). Retained repos:
`/tmp/mado-r18-mutants-run/M{1..6}/repo`.

## Receipts

Common baseline per repo: loose 4 / tight 4, covered `P1,P2,P4,P6`,
identical sets, empty `rejected`.

| # | Mutant change | Mutant commit | Diff sha256 | Loose c2 | Tight c2 | Tight response |
|---|---|---|---|---|---|---|
| M1 | `terminal-route-r17.md`: `surface: P4` → `surface: P4 terminal` (one line) | `4efe919d7f88b867ffa235a896fe9834af9b1e14` | `e9f712a5f88ca88f646eb961e96beb9ce847e542b0947dce994d433ae1af21b5` | 4, P1,P2,P4,P6 | 3, P1,P2,P6 | rejected: ``surface line must be exactly `surface: P<n>` `` |
| M2 | `input-debugging-boundaries-r15.md`: `covers: U6` → `covers: U6, U1` (one line) | `134c648cb35d57e986b34e7b8e7be338a6539cc6` | `cf76218f577ccf30a7ed40bd1e06e2e5ea1a642c0858ed01a26ba188cad19eb2` | 4, P1,P2,P4,P6 (P1 gains `input-debugging-boundaries-r15.md`) | 4, P1,P2,P4,P6 (P1 keeps only the pinned entries) | no rejection; the unpinned entry is simply not credited |
| M3 | new `p3-upstream-keyword-mutant.md` (`surface: P3`, all sections ≥3 lines) citing Hyprland docs row S016; S016 used-by gains the note | `39f98005fdfbcfcd4dc43668f406493c74d25200` | `6a0fcaf898cb083e2a0f78c7b227331afaa7e70782bb4d60b41994fbd019a3e9` | 5, P1,P2,P3,P4,P6 | 4, P1,P2,P4,P6 | rejected: `no cited mined tier-A row is an upstream https source of kind docs/spec/code naming the surface` |
| M4 | new `p3-section-floor-mutant.md` with a two-line `## Host declaration`, citing a valid walker row S900 | `5adb297833fe16ced1dc6861faf7c410a9fe2b52` | `1bf73ed9392de649ae9183a0c1354574d2eb83b6969b3b80f92c12ec218ba16c` | 5, P1,P2,P3,P4,P6 | 4, P1,P2,P4,P6 | rejected: `sections under content floor: ## Host declaration` |
| M5 | new `p3-registry-only-mutant.md` citing walker row S901 placed under `## Paths`, outside `## Registry` | `02be7a4c4820462dedd6599fe3485432cdede59c` | `700d022a9b18fb322d95ae2b3fb8e389723f80100859549c5b3cd195f2a299b2` | 5, P1,P2,P3,P4,P6 | 4, P1,P2,P4,P6 | rejected: ``no head `source:` S### token resolves to a mined tier-A SOURCES row naming this entry in used-by`` |
| M6 | new `p3-duplicate-id-mutant.md` plus a second `S016` row inside `## Registry` (walker docs row, used-by the note) | `19f4bc4cb17937bde463bb2b44bebdf6dfa49859` | `d62bfcd81afb60154e28c67e885ba3a0ffd51714d6b79d73154a6b9b5dd6e474` | 5, P1,P2,P3,P4,P6 (last copy wins) | exit 2, no c2 JSON | stderr `duplicate SOURCES id S016` |

Run-specific baseline commits (fresh repo per mutant, commit timestamps
differ): M1 `452e92e1321a…`, M2–M4 `2a5d21cdbced…`, M5–M6 `a8f378424ea7…`.
Full hashes are in the JSON.

M1's tight rejection is the exact-line rule: the note still carries all
four headings with content, `[UNK]`, the mined tier-A used-by join and a
single valid trigger token, and P4 is lost as soon as the surface line is
malformed; the later checks are not reached. The same isolation holds for
M3 (the floor, headings and `[UNK]` pass; only the surface-keyword check
fails), M4 (only the content floor fails), M5 (only the registry parse
hides the row) and M6 (the registry parse refuses before any note is
read).

## Reproduction

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-18/measure-mutants.py --keep \
  --workdir /tmp/mado-r18-mutants-run
```

Per mutant, the two instrument runs are equivalent to:

```sh
python3 -I /tmp/mado-r18-mutants-run/M1/repo/.ufo/waves/round-18/measure-loose.py <mutant_commit>
python3 -I /tmp/mado-r18-mutants-run/M1/repo/.ufo/waves/round-18/measure-tight.py <mutant_commit>
git -C /tmp/mado-r18-mutants-run/M1/repo diff HEAD^ HEAD
```

The harness exits 0 only when every mutant bites, every expected tight
response is the one observed, and no run has a `tight_only` entry
(i.e. the tight instrument never credits something the loose one misses).
This run: `mutants 6, bites 6, no_bite [], expectations_met 6,
expected_but_unmet [], unexpected_tight_only [], baselines_agree true`.

## Limits and risks

- The fixture rows `S900`, `S901` and the duplicate `S016` are synthetic
  and exist only inside the throwaway repos. They are not lane sources and
  carry no fetch receipt; they are scaffolding for an instrument test, not
  evidence about Walker.
- The mutant commit hashes identify this run only: each rerun creates new
  repos and new commit timestamps, so hashes will differ while the diffs
  and instrument digests stay the same.
- M2 is an entry-level bite, not a count-level one (see Verdict); a reader
  comparing only `c2.count` would see 4 vs 4 and must inspect the covered
  sets.
- M6's tight response is a process refusal (exit 2, no `c2`), which is the
  documented duplicate-id behaviour, not a measured count.
- Mutants exercise `c2` (rubric V) only; `c1` and `c3` are unaffected by
  these fixtures and are not re-measured here.
- The extraction filter drops unrelated absolute-target symlink fixtures
  (`.ufo/waves/round-17/tripwire/...`); neither instrument reads them, and
  the harness hashes the instrument bytes at every run, so instrument
  identity does not depend on the filtered tree.
- No host binary, service or package state was observed or changed; these
  receipts establish instrument strictness only, not coverage of P3/P5 on
  this host.
