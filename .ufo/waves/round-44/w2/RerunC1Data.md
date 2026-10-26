# RerunC1Data — C1 counting command re-run at the data commit

Seat: `RerunC1Data` (w2, round 44, hyaku run 9). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Data commit under test: `e46789213830597348fe96a351ae004d10587385` (base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`).
Predicate: `PRED-C1-r44-v2` (`registration-v2.md:28`, counting command).

**Verdict: the C1 after-data line REPRODUCES. No falsification, no open predicate defect found on this re-run.**

All evidence below is in `.ufo/waves/round-44/w2/RerunC1Data/evidence/` (digests: `evidence/SHA256SUMS.txt`).
Scratch used: `/fast/scratch/hyaku/mado-r44/RerunC1Data` (deleted at seat close); every cited file is in the seat dir.

## 1. `c1-r44-geometry-states-v2.py` at the data commit — 4 runs, all TARGET_MET

Command (exactly as registered, `--work` set to the seat scratch, `cd` into the lane):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo . \
  --rev e46789213830597348fe96a351ae004d10587385 --work /fast/scratch/hyaku/mado-r44/RerunC1Data [--nonce N]
```

| run | nonce | final line | exit | receipt |
|---|---|---|---|---|
| 1 (fresh) | `2f4219ca4f9637e7` | `fixtures=26/26 tool=present verdict=TARGET_MET` | 0 | `evidence/run1.txt`, `run1.rc` |
| 2 (fresh) | `fd87ebd5dd7c8c93` | `fixtures=26/26 tool=present verdict=TARGET_MET` | 0 | `evidence/run2.txt`, `run2.rc` |
| 3 (fresh) | `7083b1c0e0706d38` | `fixtures=26/26 tool=present verdict=TARGET_MET` | 0 | `evidence/run3.txt`, `run3.rc` |
| 4 (fixed) | `0000000000000001` | `fixtures=26/26 tool=present verdict=TARGET_MET` | 0 | `evidence/run4-fixednonce.txt`, `run4-fixednonce.rc` |

Final line, run 4 (`evidence/run4-fixednonce.txt:53`, verbatim):

```
PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=0000000000000001
```

Clause line in all four runs (`evidence/run{1,2,3,4-fixednonce}.txt:52`):

```
PRED-C1-r44-v2 clauses=a:1 b:1 b4:1 b5:1 e:1 g:1 r:1
```

Clause `r` (the round-43 no-harm side, embedded) in all four runs:

```
PRED-C1-r44-v2 clause=r rc=0 PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=...
```

## 2. Comparison with `receipts/c1-after-data.txt` (the claimed after state)

Normalising only the printed nonce (`s/nonce=[0-9a-f]+/nonce=X/`), each of my four outputs is **byte-identical**
to the claimed receipt apart from one trailing line the receipt carries and my runs record separately:

```
$ diff <(sed -E 's/nonce=[0-9a-f]+/nonce=X/g' .ufo/waves/round-44/receipts/c1-after-data.txt) \
       <(sed -E 's/nonce=[0-9a-f]+/nonce=X/g' evidence/run4-fixednonce.txt)
54d53
< exit=0
```

i.e. the receipt is my 53 lines plus a final `exit=0`; my runs' exit code is 0 and is recorded in `run*.rc`.
Every per-clause line (`b` 94/94, `b4` 16 sites killed 16, `b5` 86/94 with `failed=1`, `e` five fixtures with
`same=1`, the 26 `fixture=` lines) and the clause summary are identical, not merely equal in verdict.
Claimed line for comparison — `receipts/c1-after-data.txt:53`:

```
PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=65b72cf3b24db2b4
```

Corroboration: the tool at the data commit is the registered reference byte for byte —

```
$ git show e46789213830597348fe96a351ae004d10587385:tools/mado-geometry.py | sha256sum
1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4  -
$ sha256sum .ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt
1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4  .ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt
```

## 3. Superseded v1 counter (`c1-r44-geometry-states.py`) at the data commit — MISSED, and for exactly one reason

Two runs, both `TARGET_MISSED`, exit 1:

| run | nonce | final line | exit |
|---|---|---|---|
| fresh | `9eb7724c69b9decb` | `fixtures=18/26 … verdict=TARGET_MISSED` | 1 (`evidence/v1-run.txt:47`, `v1-run.rc`) |
| fixed | `0000000000000001` | `fixtures=17/26 … verdict=TARGET_MISSED` | 1 (`evidence/v1-run-fixednonce.txt:47`) |

Both clause lines: `PRED-C1-r44 clauses=a:1 b:1 b4:1 g:1 r:1` (v1 has no `b5`/`e`).

Failing fixtures, fixed nonce (`evidence/v1-run-fixednonce.txt`), every one `rc=5 want=0`:

```
fixture=sgen4  fixture=sgen9  fixture=sgen10  fixture=fs0  fixture=fsagree0
fixture=max0   fixture=maxfloat0  fixture=fsstdin0  fixture=fsdup0 (case 0)
```

**Are the failing fixtures exactly the NOT_COMPARED cases?** Yes, checked two ways.

(a) Every failure is an rc-only divergence: all nine report `why: rc=5 want=0`, none reports a
`stdout line`/`stdout differs` divergence — so nothing except the added verdict rule differs.

(b) A read-only probe (`evidence/probe-v1-fixtures.py`) re-ran v1's own 26 fixtures (38 case invocations,
`many()` fixtures expand) through the landed tool at the data rev and logged, per case, the tool's rc and last
line and v1's modelled line (`evidence/probe-fixed.txt`). Result of
`failing iff tool verdict == NOT_COMPARED` over all 38 cases (`evidence/assert-noncomp.txt`):

```
cases=38 mismatches=0 (failing iff NOT_COMPARED)
not_compared_cases=9
```

For each failing case the tool line and v1's modelled line are token-for-token identical except the verdict
word, e.g. `fs0`/`fsagree0`:

```
tool: … matched=1 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 maximized=0 fullscreen=1 verdict=NOT_COMPARED
want: … matched=1 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 maximized=0 fullscreen=1 verdict=OK
```

and the same single-token diff (`verdict=NOT_COMPARED` vs `verdict=OK`, rc 5 vs 0) for `sgen4`, `sgen9`
(`tiled=1 fullscreen=1`), `sgen10` (`tiled=1 maximized=1`), `max0`/`maxfloat0` (`maximized=1`), `fsstdin0`
(`maximized=1 fullscreen=1`) and `fsdup0` case 0 (`fullscreen=1`; case 1, duplicate `fullscreen` key with the
last value 0, still passes). Every failing dump has `agree=0` and `maximized + fullscreen > 0` — the
`NOT_COMPARED` condition as written at `tools/mado-geometry.py:73`:

> NOT_COMPARED (exit 5, agree=0 and maximized + fullscreen > 0)

This is exactly what v1's own docstring promised and no longer holds — `quality/counters/c1-r44-geometry-states.py:24-25`:

> MAXIMIZED clients count as matched and never as differ, so the top verdict rules (NO_SIZE_RULES,
> DIFFER, NO_MATCHING_CLIENT, OK and their exit codes) are unchanged.

The tool kept the client-line and summary model; it changed the *top verdict rules*, which v1 froze as
unchanged. So v1's MISSED is a model-version mismatch, not a defect in the landed tool.

**Precision note (not a defect).** The v1 fixture count is nonce-dependent: `18/26` at
`9eb7724c69b9decb` (failing `sgen1`, `sgen7`, …) versus `17/26` at `0000000000000001` (failing `sgen4`,
`sgen9`, `sgen10`, …). Only the `sgen` membership moves, because the seed draws the `fullscreen` value per
client; the invariant that holds at every nonce is *failing set == NOT_COMPARED set*. Any statement of the
form "v1 gives 18/26 at the data commit" is therefore nonce-specific and should carry its nonce.

## 4. Round-43 counter (`c1-r42-geometry.py`) — no-harm side, standalone

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
  python3 -I quality/counters/c1-r42-geometry.py --repo . --rev e46789213830597348fe96a351ae004d10587385
PRED-C1-r42 clauses=a:1 b:1 b2:1 b3:1 g:1
PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=bcb498706f6abee4
```

(`evidence/r42-run.txt:49`; the process exit status is recorded separately in `evidence/r42-run.rc` as `EXIT=0`.) Its 37 fixtures compare rc and stdout byte-exactly and carry no
`fullscreen` field, so this is the "round-43 output byte-identical otherwise" side of the claim: the landed
tool still reproduces the round-43 contract on every round-42 lattice fixture.

## 5. The tip half of the claim (extra, cheap, same command)

`registration-v2.md:31` targets `fixtures=26/26 … exit 0, at the data commit and at the tip`. The seat's target was
the data commit; the tip is one `--rev` away, so it is measured too. Both runs `TARGET_MET`, exit 0:

| run | rev | nonce | final line | exit |
|---|---|---|---|---|
| tip (fresh) | `290cddea92a18e2202456db89cb2bb60d9aaacff` | `642b047336fd210b` | `fixtures=26/26 … verdict=TARGET_MET` | 0 (`evidence/tip-run.txt`, `tip-run.rc`) |
| tip (fixed) | `290cddea92a18e2202456db89cb2bb60d9aaacff` | `0000000000000001` | `fixtures=26/26 … verdict=TARGET_MET` | 0 (`evidence/tip-fixed.txt`, `tip-fixed.rc`) |

`tools/mado-geometry.py` is unchanged between the data commit and the tip
(`sha256 1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4` at both), so the tip run differs from the
data run only in the revision-addressed reads the counter performs (`clause=r` still 37/37 `rc=0`).

## 6. What this re-run does and does not establish

Establishes (measured, at `e4678921` for the v1/v2 comparison and at `290cddea` for the tip run):
- `PRED-C1-r44-v2` scores `fixtures=26/26 verdict=TARGET_MET` exit 0, deterministically across three fresh
  nonces and one fixed nonce; clause `e` (sandbox vs plain, five fixtures, `same=1` every run) and clause `b5`
  (state-blind copy 86/94, `failed=1`) hold in each run.
- The published after-data receipt is a faithful transcript of that counter at that commit (53 lines, up to
  nonce), the landed tool equals the registered v2 reference (sha256 `1da3dda…`), and the round-43 counter is
  undisturbed (37/37, exit 0).
- The superseded v1 counter's MISSED is attributable, fixture by fixture, to the single added `NOT_COMPARED`
  verdict; no other divergence exists at the data commit.

Does not establish (out of this seat's scope, declared residuals unchanged from `registration-v2.md`):
- the live maximized/fullscreen geometry of any host window, the C2 lane, or the tool's truth beyond the
  counter's model — a tool holding a model of the contract
  is an implementation. Whether `NOT_COMPARED` is the *right* operability verdict is the registry's judgement,
  not a number this seat measures.

## 7. Tooling and host state

No tool installed, no package transaction, no compositor call beyond `hyprctl version`-class reads (none were
needed), no host-service or config mutation. Interpreter: `Python 3.14.8`. Only reads against the lane
(`git show`, `git rev-parse`, `git log`); no git/jj write anywhere; scratch
`/fast/scratch/hyaku/mado-r44/RerunC1Data` removed at seat close after the receipts above were copied into this
seat directory.

## 8. Evidence inventory (in `evidence/`)

`run1.txt` `run2.txt` `run3.txt` `run4-fixednonce.txt` (+ `.rc`), `tip-run.txt` `tip-fixed.txt` (+ `.rc`),
`v1-run.txt` `v1-run-fixednonce.txt` (+ `.rc`), `r42-run.txt` (+ `.rc`), `probe-v1-fixtures.py`, `probe-fixed.txt`, `assert-noncomp.txt`, `quote-check.sh`,
`quote-check.txt`, `SHA256SUMS.txt` (sha256 of the other 22 files).

## 9. Self-check of this report

`evidence/quote-check.sh` re-greps every quotation and every locator in this report against its source and every
count quoted above, and recomputes each `grep -n` line number rather than trusting the typed value
(`evidence/quote-check.txt`, 38 checks):

```
QUOTE-CHECK: PASS (all locators and counts reproduced)
```

