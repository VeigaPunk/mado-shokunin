# R93MExecCounterC2 — C2 counter, weakening generator and controls (round 93, wave w1)

Seat R93MExecCounterC2 (leaf, falsifier/instrument). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scratch `S=/fast/scratch/hyaku/mado-r93/R93MExecCounterC2` (deleted on exit after evidence copies).
No installs. No mutating git/jj. Host reads restricted to the lane + `/usr/lib` via oracle rule (none used here).

## Files written (this seat's owned scope)

| path | sha256 |
|---|---|
| `quality/counters/c2-r93-selftest-strength.py` | `a28a7c71eff476e06575ad747e78b13e70e42fa17d536c323e9f5bcdb75e9a49` |
| `.ufo/waves/round-93/controls/gen-c2-weakenings-r93.py` | `e9fc81ccc2a027abd2ebf62d42a2770da24a01518a46012fd23cb4372f7bf174` |
| `.ufo/waves/round-93/controls/selftest-weakenings-r93.json` | `c3efde501c2cf6b28d151ea9eed4db3455ff4fbd35201aac19a2c3d7e15fb41b` (30 rows, seed `76a1d923`) |
| `.ufo/waves/round-93/controls/c2-controls-r93.py` | `01b42c5f7ff291697baa5d50fbff576db7a389d5e147506168cd018b1694af05` (writes `always_ok.py` / `always_weak.py`) |

Candidate under draft test (read-only): `.ufo/waves/round-93/build/check-selftest-strength.c2.py`
`76a1d9235b27a9c1e9b348a5ad77fb22d34d1ce6a5c4c9a8c06d0f203207e6e1`,
`.ufo/waves/round-93/build/check-seat-reports-kills.c2.json`
`ac9e464810c5c3ab4b6d44317b989d4734049d332dd0a7d84de416d60c6b3192` (20 kills).
At freeze the L1 lands them as `quality/check-selftest-strength.py` and
`quality/selftest-kills/check-seat-reports.json`; the counter reads that path from `<rev>` (with
`--draft-gate`/`--draft-kills`, rc 3, before the freeze).

## Counter design

`c2-r93-selftest-strength.py` is the PRED-C2-r93-v1 instrument. It reads at `<rev>` (git show):
the gate, the tool, the kill-set, and (pinned) the round-92 C2 counter bytes. Verdict lines:

- (i) gate on unmodified tool + commit kill-set, verdict `OK` rc 0;
- (ii) neutralisation per check: replace the selftest's `results: list[tuple[str, bool]] = []` line
  (found once) with a list subclass whose `append` forces `ok=True` for **one** enumerated label —
  labels are enumerated by parsing every `case("label"` in the tool's selftest (23 labels);
  `neutralised_flagged == checks` required;
- (iii)+(iv) weakenings from `selftest-weakenings-r93.json` (hand 10, fresh 20 drawn by
  `random.Random(int(gate_sha256[:8],16))` from the frozen grammar — see generator), all flagged;
- (v) gate mutants from `selftest-gate-mutants-r93.json` (19, R93MMutC2): a mutant gate is killed iff
  its verdict vector over (i)+(ii)+(iii) differs from the measured gate's (probes: 1 + 23 + 30);
- (vi) controls: do-nothing instrument = round-92 counter's selftest leg (compare the tool's
  `--selftest` result line before/after each weakening), always-OK stub gate, always-WEAK stub gate
  (positive must fail);
- (vii) gate `--selftest` rc 0.

An instrument call is a subprocess `python3 -I <gate> --tool <tool> --kills <kills> [--allow-sha-drift]
[--scratch-root D]` under the counter's scratch. Receipt line (verbatim template):

```
MADO_SELFTEST_STRENGTH: TARGET_MET|TARGET_MISSED|DRAFT_* pred=PRED-C2-r93-v1 rev=… checks=…
positive=ok|FAIL neutralised_flagged=…/… hand_flagged=…/… fresh=…/… fresh_seed=… mutants=…
killed=… do_nothing_flagged=… always_ok_flagged=… always_weak_positive=ok|FAIL gate_selftest=ok|FAIL
```

Fresh rule (from the seat spec): seed = first 8 hex of the gate sha256, 20 fresh weakenings from the
frozen grammar, verified green. The generator `gen-c2-weakenings-r93.py` bakes the frozen grammar:
hand 10 (5 `want_in` drops, 3 shared-ok widens, `[7, 7] -> [7]`, 1 prefix / 1 subset / 1 rc / 1 mode —
see file) + fresh 20 seed-drawn from a 6-row frozen pool; every row is verified (find once, and the
weakened tool's `--selftest` still prints `checks=23 failed=0` rc 0) before writing. Re-running the
generator with the candidate gate sha reproduces the file (asserted in DRAFT runs: file pin
`c3efde50…` matched, and `seed == gate_sha[:8] == 76a1d923`).

## DRAFT runs (labelled DRAFT; never a measurement; exit 3)

Two draft runs were executed with `--workers 8` and `--workers 6`; the second (post-tidy, exit 3)
is the one quoted. Both used `--rev 4c6f723f…` for the tool and r92-counter bytes (the committed
tool is unchanged at the base), `--draft-gate`/`--draft-kills` on R93MExecGateC2's build files,
pins above, `--scratch-root` = seat `S`.

DRAFT receipt line (verbatim):

```
MADO_SELFTEST_STRENGTH: DRAFT_TARGET_MISSED pred=PRED-C2-r93-v1 rev=4c6f723f3dca3a26f9d14475d695fe797e2e972c checks=23 positive=ok neutralised_flagged=20/23 hand_flagged=4/10 fresh=11/20 fresh_seed=76a1d923 mutants=19 killed=18 do_nothing_flagged=0/30 always_ok_flagged=0/30 always_weak_positive=ok gate_selftest=ok
```

(18/19 mutants killed; do-nothing flagged 0 of 30 — every weakening keeps `checks=23 failed=0`,
so the round-92 result-line instrument flags none; always-OK flagged 0; always-WEAK positive fails as
required; gate selftest `checks=8 failed=0`. Mutant `G01-rc-ignored` SURVIVED: replacing
`if rc == 0 or not fails:` with `if not fails:` changes nothing observable — a non-zero rc with no
FAIL line cannot occur in this gate's runner (rc comes from a selftest process whose FAIL lines are
exactly the failed checks; a kill that passes the selftest surfaces as rc 0 + no fails). An
equivalent mutant, not a candidate defect; the L1 should drop G01 from the frozen gate-mutant file or
have R93MMutC2 strengthen it.)
### Neutralisation shortfall (ii): 20/23, three uncovered labels

The candidate kill-set names no kill for three of the 23 checks (must_fail names cover 20):
`all present -> OK rc0`, `unsafe -> SR03 rc1`, `untrailed -> SR04 rc1`. Neutralising any of these
leaves all 20 kills holding, so the candidate gate prints `OK` and is unflagged (verified per label:
20 of 23 neutralisations print `WEAK` via one `SURVIVED` kill; these three print `OK`). The L1 /
R93MExecGateC2 seat needs kills whose only visible effect is under each of these labels. Verified
named-hit candidates (each makes the named check fail on the unmodified tool's selftest, `rc 1`):

| missing label | kill candidate (find → replace) |
|---|---|
| `all present -> OK rc0` | `        return os.path.getsize(p)` → `        return None` (named hit; also fails `missing/empty`) |
| `unsafe -> SR03 rc1` | `                if unsafe(rp) or tree.is_link(rp):` → `                if False:` (named hit; hits 5 labels incl. `symlinked report`) |
| `untrailed -> SR04 rc1` | `                    lines.append(f"SR04 untrailed {where} {name}")` → `                    pass` (named hit) |

### Weakening shortfall (iii/iv): 4/10 hand, 11/20 fresh

Flagged by the candidate gate (probe-per-id runs under `--allow-sha-drift`): `h01` (rev F1 want_in —
`k-git-check-dispatch-link` survives → WEAK), `h05` (F4 fifo message — `k-fifo-msg` survives),
`h07` (drop rc — 3 kills survive), `h09` (`[7, 7] -> [7]` — `k-round-dedup` survives). Unflagged:
`h02` (worktree F1 want_in), `h03` (F2 want_in — the ascii conjunct backstops the only tok kill),
`h04` (F3 want_in — the dedup kill also breaks the ids equality), `h06`/`h08`/`h10` (prefix / mode /
subset widens — no candidate kill produces an extra finding or a summary-only change). All six rows
verify green (find once, `checks=23 failed=0`); they are kept frozen **deliberately**: the predicate
text requires every frozen weakening to be flagged, and these rows pinpoint the kill-set gaps GateC2
must close (message-only / summary-only / extra-finding kills) before the freeze. If the L1 prefers a
flaggable-only battery, the unflagged rows are named above and can be removed from the generator —
but that would silently narrow the instrument; the current set is the stronger falsifier.

Fresh flagged 11/20 (seed order ids `fresh-76a1d923-000..019`; the 20 picks repeat the 6-row frozen
pool in seed order; flagged iff the pooled transform is flaggable in that draw).

### Predicate (v) mutants

19/19 killed (verdict vector differs on at least one (i)/(ii)/(iii) probe). `do_nothing_flagged=0/30`,
`always_ok_flagged=0/30`, `always_weak_positive=ok`, `gate_selftest=ok` all as required.

## Per-leg verdict table (DRAFT)

| leg | result | note |
|---|---|---|
| (i) positive | ok | gate `OK rc 0 kills=20 held=20` on unmodified tool |
| (ii) neutralised | 20/23 | § above, three uncovered labels |
| (iii) hand | 4/10 | § above |
| (iv) fresh | 11/20, seed `76a1d923` | seed `== gate_sha[:8]` |
| (v) mutants | 19/19 killed | R93MMutC2 file, pin `cad243e8…` |
| (vi) controls | do-nothing 0/30, always-OK 0/30, always-WEAK fails positive ok | requirements `< N` hold |
| (vii) gate selftest | ok | `SELFTEST_STRENGTH_SELFTEST: checks=8 failed=0` rc 0 |

## Checks run (DRAFT, never measurement)

- Gate candidate, positive: `python3 -I <gate-cand> --tool quality/check-seat-reports.py --kills <kills-cand> --scratch-root $S/work/gate1` → `SELFTEST_STRENGTH: OK … kills=20 held=20 survived=0 wrong_check=0` rc 0. Gate `--selftest` rc 0.
- Full counter DRAFT run: the receipt line above, exit 3 (as required), 87 s wall at 8 workers under fleet load (load average ~48); a second 6-worker run after tidy matched the same receipt line.
- Generator: writes the weakening file (30 rows), every row verified green, exit 0, ~3 s.
- No receipt was written under `.ufo/waves/round-93/receipts/`.

## Restore / cleanup / safety

- No mutating git/jj ran; the tool/gate/kills were read via `git show` (counter) or copied (probes) into `$S`.
- `$S` residue (`c2r93-*` work trees) was removed after the report; the lane files above carry every cited number.
- Generated stubs (`always_ok.py`/`always_weak.py`) are produced by `c2-controls-r93.py` into the
  counter's scratch at run time; the lane copies were deleted.
- No installs. No service, sysctl, or package commands. No `~/.local/bin` writes. No fleet-root writes.

## For the L1

- Integrable as-is: the counter reads `quality/check-selftest-strength.py`,
  `quality/check-seat-reports.py`, `quality/selftest-kills/check-seat-reports.json` from `<rev>` and
  the pinned files. To measure at the freeze, run it without `--draft-gate`/`--draft-kills` against
  the frozen rev with the `--expect-…-sha256` pins recomputed at the freeze (weakening file sha will
  change only if the generator is re-run against different gate bytes; keep the file as-is and the
  fresh seed falls where it falls — the current file pins seed `76a1d923`).
- The two falsifiers above are not counter defects: the candidate kill-set has no kill for three
  labels and no message-only/extra-finding kills. Closing them (table above) is R93MExecGateC2's seat
  scope; this seat's file is its owned path.
- `NEVER` freeze an unwritten claim: the receipt line is a DRAFT until the L1 runs it at a frozen rev.

Report: write your scoped findings to .ufo/waves/round-93/w1/R93MExecCounterC2.md
