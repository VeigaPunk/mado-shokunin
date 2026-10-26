# RerunControlsV2 — w2, round 44 (re-run of both v2 control receipts)

**Bottom line:** both frozen control receipts reproduce at the registered freeze, row for row. C1: 20 of 20 controls
still score TARGET_MISSED and the reference still scores TARGET_MET (`0 of 20`, PASS) — twice, at two independent
nonces. C2: the positive control is admitted and 10 of 10 do-nothing/forged variants are rejected (`wrong=0 of 11`,
PASS) — twice. Zero disallowed differences in 32 row comparisons against `receipts/ctl-c1-v2.txt` /
`receipts/ctl-c2-v2.txt`, and zero clause-vector flips across the 32 row comparisons between my own repeated runs. Only
the nonce- and timestamp-derived columns move. No OPEN predicate defect was produced by this seat; two LOW/INFO
provenance notes follow (F5, F6), neither of which changes a verdict.

Seat: leaf. No subagent, no background job beyond the harness's own completion of the two foreground runs, no write
outside `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w2/RerunControlsV2*` and my scratch dir.

## 1. Commands (verbatim, as assigned)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && TMPDIR=/fast/scratch/hyaku/mado-r44/RerunControlsV2 \
  python3 -I .ufo/waves/round-44/ctl/run-c1-controls-v2.py \
    --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev 03fa5c618b089064a657b3d79d3d4272ae4b6894 \
    --work /fast/scratch/hyaku/mado-r44/RerunControlsV2/c1
```
```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && TMPDIR=/fast/scratch/hyaku/mado-r44/RerunControlsV2/c2 \
  python3 -I .ufo/waves/round-44/ctl/run-c2-controls-v2.py \
    --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --freeze 03fa5c618b089064a657b3d79d3d4272ae4b6894 \
    --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f \
    --work /fast/scratch/hyaku/mado-r44/RerunControlsV2/c2
```

Each was then run a second time (same arguments, fresh `--work` `c1b` / `c2b`, fresh nonces) to measure run-to-run
variance. All four runs exited 0 with empty stderr; wall clock 240.02 s, 236.96 s (C1) and 22.08 s, 19.08 s (C2).

| run | receipt (in this seat dir) | sha256 | exit | last line |
|---|---|---|---|---|
| C1 #1 | `c1-rerun.txt` | `d5a3fc96608546b4ccb740e06ea377b552457dde45b4757ff57b8d2ddeef7f55` | 0 | `CTL_C1v2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 20; reference met: 1)` |
| C1 #2 | `c1-rerun2.txt` | `e6e7a7495ba10afeffa2f16b1b2e2d3958cfce3729e716ab3491aedf9903ed85` | 0 | same |
| C2 #1 | `c2-rerun.txt` | `11a84dbfe3ecea56d877d496d9d0ea5ba02745881a082398b4255472fba0d464` | 0 | `CTL_C2v2 VERDICT: PASS (wrong=0 of 11; positive admitted=1)` |
| C2 #2 | `c2-rerun2.txt` | `7f4e56da0fa144bf26826f5eb23693a0da7b97eb5076cdf6b72ebe23eb2a0605` | 0 | same |

Diff receipts, produced by `differ.py` (this seat; parses both receipt formats, compares roster, `want`, `got`,
`rc`, `ok`, the clause vector, the top verdict word and `admitted=x/1` field-by-field, and allows only `nonce`,
`rev` and the C1 `fixtures=k/26` share to differ):

| diff | receipt | exit |
|---|---|---|
| `receipts/ctl-c1-v2.txt` vs `c1-rerun.txt` | `c1-diff-vs-committed.txt` | 0 → `MATCH (no disallowed difference)` |
| `receipts/ctl-c2-v2.txt` vs `c2-rerun.txt` | `c2-diff-vs-committed.txt` | 0 → `MATCH (no disallowed difference)` |
| `c1-rerun.txt` vs `c1-rerun2.txt` | `c1-diff-run1-vs-run2.txt` | 0 → `MATCH` |
| `c2-rerun.txt` vs `c2-rerun2.txt` | `c2-diff-run1-vs-run2.txt` | 0 → `MATCH` |

## 2. C1 — every row identical, twice

Clause order in the receipts is `a b b4 b5 e g r`. Committed column is `receipts/ctl-c1-v2.txt`; run1/run2 are
mine at the registered freeze.

| control | committed clauses | run1 | run2 | verdict/rc, all three |
|---|---|---|---|---|
| REF | `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1` | same | same | met / 0 |
| BASE-tool | `a:1 b:0 b4:0 b5:0 e:1 g:1 r:1` | same | same | missed / 1 |
| ABSENT-62dd798 | `a:0 b:0 b4:0 b5:0 e:0 g:0 r:0` | same | same | missed / 1 |
| K01…K12, K14, K15, K16 (15 rows) | `a:1 b:0 b4:0 b5:0 e:1 g:1 r:0` | same | same | missed / 1 |
| X1-sandbox-gate | `a:1 b:1 b4:1 b5:1 e:0 g:1 r:1` | same | same | missed / 1 |
| X2-padded-selftest | `a:1 b:1 b4:1 b5:0 e:1 g:1 r:1` | same | same | missed / 1 |
| K13-no-new-selftest | `a:1 b:0 b4:0 b5:0 e:1 g:1 r:1` | same | same | missed / 1 |

The per-row `IDENTICAL` verdicts are in `c1-diff-vs-committed.txt` (21 rows, `RESULT: MATCH`). This reproduces the
landed claim verbatim: `controls 0 of 20 met` (`LOG.md:2502`) and the registration's control sentence
(`registration-v2.md:34-37`).

## 3. C1 — the `fixtures=k/26` share really is nonce-dependent (and nothing else is)

| control | committed | run1 | run2 |  | control | committed | run1 | run2 |
|---|---|---|---|---|---|---|---|---|
| REF | 26 | 26 | 26 |  | K09-states-differ | 17 | 16 | 19 |
| BASE-tool | 15 | 14 | 15 |  | K10-swapped-words | 13 | 15 | 11 |
| ABSENT | 0 | 0 | 0 |  | K11-old-summary | 12 | 14 | 13 |
| K01 | 17 | 18 | 19 |  | K12-field-order | 15 | 15 | 12 |
| K02 | 12 | 12 | 13 |  | K14 | 20 | 17 | 20 |
| K03 | 22 | 22 | 24 |  | K15 | 24 | 23 | 22 |
| K04 | 19 | 20 | 20 |  | K16 | 19 | 19 | 19 |
| K05 | 24 | 25 | 25 |  | X1 | 26 | 26 | 26 |
| K06 | 24 | 24 | 21 |  | X2 | 26 | 26 | 26 |
| K07 | 24 | 23 | 23 |  | K13 | 26 | 26 | 26 |
| K08 | 15 | 12 | 14 |  |  |  |  |  |

11 of 21 rows change share between the committed run and run1; 12 of 21 change between run1 and run2 (same `--rev`,
different nonce). In all 42 row comparisons the clause vector, `rc` and the top verdict word are unchanged, and
`REF` is 26/26 every time. This is exactly the declared behaviour — "the lattice share varies with the nonce, the
verdict does not" (`registration-v2.md:30`) — because the fixture lattice is seeded by both arguments:
`rng = old.rng_for(rev, nonce, "sgen", i)` (`quality/counters/c1-r44-geometry-states-v2.py:209`, `:243`) over
`def rng_for(rev, nonce, tag, i)` (`quality/counters/c1-r42-geometry.py:336`).

**Isolation claims also reproduce twice:** the registration says X1 is "caught by **e** only" and X2 "caught by
**b5** only" (`registration-v2.md:35-36`). In both of my runs X1 zeroes only `e` (all other clauses 1) and X2 zeroes
only `b5`; no other variant shares those vectors.

## 4. C2 — every row identical, twice

| control | committed clauses `a…j` | run1 | run2 | admitted | rc |
|---|---|---|---|---|---|
| P (positive) | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1` | same | same | 1/1 | 0 |
| C2-BASE | all `:0` | same | same | 0/1 | 1 |
| STAGED-COPY | `a:1 b:0 c:0 d:0 e:0 f:1 g:0 h:0 i:0 j:0` | same | same | 0/1 | 1 |
| R12-REPOINT | `a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 j:0` | same | same | 0/1 | 1 |
| MINIMAL-QUOTES | = R12-REPOINT | same | same | 0/1 | 1 |
| SHELL | = R12-REPOINT | same | same | 0/1 | 1 |
| HIDDEN-LINE | `… g:0 … j:1` (`g` only failure) | same | same | 0/1 | 1 |
| FORGED-PIN | `a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:0 i:0 j:1` | same | same | 0/1 | 1 |
| FALSE-URL | `… e:0, g:1 …` (`e` only failure) | same | same | 0/1 | 1 |
| PROSE-SIZE-REQUEST | `… h:0 …` (`h` only failure) | same | same | 0/1 | 1 |
| ANCHOR-PAST-EOF | `… e:0 …` (`e` only failure) | same | same | 0/1 | 1 |

`c2-diff-vs-committed.txt`: 11 rows, `RESULT: MATCH (no disallowed difference)`, trailer
`VERDICT: PASS (wrong=0 of 11; positive admitted=1)` in both, differing only in the `freeze=` label. This reproduces
`registration-v2.md:59-62` and `corpus/lessons/round-44.md:167` ("0 of 20 met … positive control P … 10 of 10").

## 5. Input identity (so the comparison is about the same predicate, not a re-edited one)

`input-identity.txt` (git `hash-object` of the working tree vs `rev-parse <rev>:<path>`, read-only):

- `quality/counters/c1-r44-geometry-states-v2.py` = `8e844b22…` = **freeze v2** blob; absent at the v1 freeze and
  at base.
- `quality/counters/c2-r44-gkeep-size-request-v2.py` = `d24abcf7…` = freeze v2; absent at v1/base.
- `quality/counters/c1-r42-geometry.py` (imported by the C1 counter) = `79657a45…` at work, v2 freeze and base.
- both runners (`a5090b2f…`, `517a742f…`) and the C1 reference (`d5f50df1…`) = freeze v2 blobs.
- `tools/mado-geometry.py` = `d5f35b66…` at **base, v1 freeze and v2 freeze** (the round-43 tool), and `d5f50df1…`
  in the working tree (the landed data tool, identical to the C1 reference). Only the `BASE-tool` row reads the tool
  at the supplied `--rev` (`ABSENT-62dd798` deliberately reads an earlier rev where the file is absent), so its bytes
  are the same whichever of the two freezes is passed; only the RNG seed moves.

No lane write occurred: `git status --porcelain` shows only the orchestrator's `w2.ready*` markers and the w2 seat
directories; `HEAD` is `290cddea92a18e2202456db89cb2bb60d9aaacff`.

## 6. Findings

**F1 — SUPPORTS C1's control claim (no defect).** `receipts/ctl-c1-v2.txt` reproduces at the registered freeze:
21/21 rows identical in `want/got/rc/ok/clauses/verdict` (the `fixtures=k/26` share moved on 11 rows — see §3),
trailer `0 of 20` met with the reference met, exit 0, twice.
What it attacks: any reading that the `0 of 20` was a single-run or nonce-dependent artifact.
Repro: §1–§2, `c1-diff-vs-committed.txt`.

**F2 — SUPPORTS C2's control claim (no defect).** `receipts/ctl-c2-v2.txt` reproduces: 11/11 rows identical
including `admitted=x/1` and the isolation pattern of each forgery (only `g`, only `e`, only `h`, `d/g/h/i` for the
forged pin), `PASS (wrong=0 of 11; positive admitted=1)`, exit 0, twice. Repro: §4.

**F3 — SUPPORTS the declared nonce residual, quantified.** 11/21 and 12/21 rows move their `fixtures=k/26` share
with no clause/verdict/rc flip in 42 comparisons (§3). The registration's residual — "the lattice share varies with
the nonce, the verdict does not" (`registration-v2.md:30`) — is measured, not assumed. Consequence for readers: a
future receipt whose `BASE-tool` line reads `11/26` (as in `receipts/c1-v2-before-base.txt`) rather than `14/26` is
not evidence of a change.

**F4 — SUPPORTS the two isolation claims.** X1 fails `e` only, X2 fails `b5` only, in all four of my runs
(`registration-v2.md:35-36`); the ported cheats stay caught by exactly the clause the registration nominates.

**F5 — LOW (evidence provenance; attacks the frozen C1 receipt, not a predicate).** `receipts/ctl-c1-v2.txt` labels
every row `rev=e2289516…`, a revision at which the v2 counter does not exist (`input-identity.txt`, row 1:
`freezeV1=e2289516 → ABSENT`), and the runner resolves the counter from the *working tree*, not from `--rev`
(`.ufo/waves/round-44/ctl/run-c1-controls-v2.py:48`; same shape at `run-c2-controls-v2.py:74`). So the printed
receipt cannot be rebuilt by checking out the rev it names, and it does not pin the predicate's bytes at all — a
reader must trust the tree of the moment. Nothing here is false (the rev argument is only an RNG seed plus the
`BASE-tool` read, and both freezes carry the same tool blob `d5f35b66`), and no re-registration is implied. Repair
is the L1's call; the minimal one is a provenance line on the two receipts —
`# counter=8e844b221a957173c3c557f371f7871b2a6e11cf ref=d5f50df12ab32abd172d17b039c93daec2a94ff7 runner=a5090b2f088f6f90ccedae81f946be80e0f38013 rev=03fa5c61…` —
or, cheaper, cite the freeze-labelled rerun this seat produced (`c1-rerun.txt` / `c2-rerun.txt`) alongside them.

**F6 — INFO (attacks the C2 receipt's `rev=` column as evidence).** The C2 runner commits each control in a
throwaway clone, so the printed commit ids are timestamp-dependent: same freeze, same inputs, two runs —
`P rev=cd1ff8bf…` then `0b7ca8f8…`, and the other nine forged rows likewise (P with them; `C2-BASE` is fixed at the
base commit `6a1a905…`). Those cells carry no evidence; the clause vector, `admitted` and the verdict word are the evidence, and
those were identical. Anyone comparing C2 receipts must normalise the `rev=` column or they will "find" drift that
does not exist. (Also: the committed `P rev=92d67315…` differs from mine because the freeze tree differs — expected,
not drift.)

## 7. Limits of this seat's result

- I probed two axes: receipt reproduction at the registered freeze, and invariance under a second nonce. I did not
  extend the variant set, mutate the counters, or attempt new forgeries — those are the w2 mutation/forgery seats'
  items (`R39W2C1Mutants`, `MutC2Corrections`, `SwarmCritic20`).
- Runs were CPU-quiet (no sibling work in my scratch); no deliberate load/flake probe was run, so the sandboxed
  fixture timeouts were not exercised near their limit.
- The C1 `fixtures=` share is a function of `(rev, nonce)`; my two runs sample two points of that space, not the
  whole of it.
- No OPEN predicate defect arose from these two runs; F5/F6 are documentation/provenance notes with recommended text
  and require no predicate change.

## 8. Hygiene

- Receipts in this seat directory, with hashes, in `RerunControlsV2/receipts.sha256`: the four control runs
  (`c1-rerun.txt`, `c1-rerun2.txt`, `c2-rerun.txt`, `c2-rerun2.txt`), their two 0-byte stderr captures
  (`c1-rerun.err`, `c2-rerun.err` — both runs printed nothing on stderr), the four diffs
  (`c1-diff-vs-committed.txt`, `c1-diff-run1-vs-run2.txt`, `c2-diff-vs-committed.txt`,
  `c2-diff-run1-vs-run2.txt`), `input-identity.txt`, the born-here `differ.py`, and `quote-check.txt`
  (`quote-check.py`: all 16 liftings re-grepped at their cited line ranges, whitespace-normalised across line breaks,
  `QUOTE-CHECK: PASS (16 cases, 0 failures)`).
- Scratch `/fast/scratch/hyaku/mado-r44/RerunControlsV2` (C1 tool copies, C2 clones, bootstrap) deleted at the end of
  this seat; every citable byte was copied into this seat directory first.
- No package manager run, no compositor call, no `git`/`jj` mutation, no write outside the seat dir.
- Tool record: no installs; `python3` (system, 3.x), `git` (system), `bwrap` (already present, used by the counters'
  sandbox) — all pre-existing.
