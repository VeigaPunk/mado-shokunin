# RerunAllV3 — partly falsified: the named tripwire checks reproduce, but the live corpus-diff receipt counts do not

All commands below were run from the disposable clone at `a8960de655e6ea8c0a3bf74f5542041d9fe25b39`. Its `tools/mado-tripwire.py` SHA-256 is `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458`.

## Finding — P3: corpus-diff receipt counts depend on an unpinned live input

The raw comparisons still reproduce their finding deltas on the attempt-2 session itself, but the historical whole-corpus census numbers do not repeat against the current session corpus. The prior evidence is `.ufo/waves/round-20/a2/evidence/corpus-diff-28c6837-vs-a8960de.json` (SHA-256 `c5c8ebcffad7bdde0bab85827634666f0059ed1c9b271cd8ba8587a650bf389e`) and `.ufo/waves/round-20/a2/evidence/corpus-diff-9c54c56-vs-a8960de.json` (SHA-256 `b758abd3c29aec4259747974f11620fb1f4fdac6df78578dae2438e0192eaf2b`). The comparison program is `.ufo/waves/round-20/w2/CorpusDiffV2/corpus-diff-v2.py` (SHA-256 `f464e72f9615e75497528b671bbd420615e9e786fa4f3fc5d448e7eb830d050c`). The external transcript corpus is live and has no immutable fixture SHA / saved per-file input manifest; that missing identity is part of the finding.

Reproducing commands (run from clone root; `$SESSION_CORPUS` is the session corpus named by the recorded receipt; output is redirected to scratch):

```sh
python3 -I .ufo/waves/round-20/w2/CorpusDiffV2/corpus-diff-v2.py \
  --base 28c6837 --new a8960de --corpus "$SESSION_CORPUS" \
  --round20-dir "$SESSION_CORPUS/<MadoR20-session>" --out "$SCRATCH/corpus-diff-28.json"
# exit=0
python3 -I .ufo/waves/round-20/w2/CorpusDiffV2/corpus-diff-v2.py \
  --base 9c54c56 --new a8960de --corpus "$SESSION_CORPUS" \
  --round20-dir "$SESSION_CORPUS/<MadoR20-session>" --out "$SCRATCH/corpus-diff-9c54.json"
# exit=0
```

| Receipt comparison | Prior receipt values | Re-run values | Stable comparison portion | Revisions |
|---|---|---|---|---|
| `.ufo/waves/round-20/a2/evidence/corpus-diff-28c6837-vs-a8960de.json` | start 8,039; stable 7,913; excluded 195 | start 8,255; stable 8,092; excluded 253 | lost calls 4, lost findings 5, added findings 10, relabels 2 in both runs; R20 stayed 164/164 stable with 5 lost findings and 2 additions | `28c6837` → `a8960de` |
| `.ufo/waves/round-20/a2/evidence/corpus-diff-9c54c56-vs-a8960de.json` | start 8,039; stable 7,889; excluded 150; added findings 7,253 | start 8,417; stable 8,254; excluded 235; added findings 7,418 | zero lost calls/findings and 2 relabels in both runs; R20 stayed 164/164 stable with 325 additions | `9c54c56` → `a8960de` |

The current outputs themselves report 90/72 files added during scan and 163 files changed during scan, respectively. [INFERENCE] The changed census and the +165 whole-corpus additions on the pre-harm comparison reflect growth/drift in the live transcript input rather than changed tool bytes: both comparisons used the same recorded base/new tool hashes, while the input is not content-addressed. This does not change the listed precision or guard-suite results, but the historical full-corpus counts cannot be treated as repeatable without a frozen corpus manifest/snapshot.

## Stated vs reproduced

| Claim / input identity | Command (clone-root cwd) | Stated | Reproduced | Exit |
|---|---|---|---|---:|
| Precision, 175 scored cases; `.ufo/waves/round-20/precision/expected.json` SHA-256 `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f`; suite pin `f3da50488661509ce5d144c90f7780f8088e0903` | `python3 -I .ufo/waves/round-20/tw-precision.py a8960de` | 172/175; P 66/66, S 17/17, W 21/22, H 51/52, L 17/18 | 172/175; P 66/66, S 17/17, W 21/22, H 51/52, L 17/18; tool SHA-256 `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458` | 0 |
| Held-out precision, `.ufo/waves/round-20/precision-heldout/expected.json` SHA-256 `78b168b0db86502df23b6204a5a9a3e1f53189df5cf0257fef6c1d1214b3901a` | `python3 -I .ufo/waves/round-20/tw-precision.py a8960de --heldout` | 2/12 | 2/12 (H 2/3, S 0/3, W 0/6) | 0 |
| Frozen recall, `.ufo/waves/round-18/frozen/expected.json` SHA-256 `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`, pinned at `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` | `python3 -I .ufo/waves/round-19/tw-recall.py a8960de` | 6/6 | 6/6 | 0 |
| Recall evidence split, same frozen input | `python3 -I .ufo/waves/round-20/tw-recall-split.py a8960de` | 5 observed + 1 lead; 20 control lines, 0 findings | 5 observed + 1 lead; 20 control lines, 0 findings; 0 undetected lines | 0 |
| Attempt-2 guard fixtures, pinned at `6a7d9ca0d2124a4077074b800c94a9bc1184441c`; `.ufo/waves/round-20/a2/fixtures/manifest.json` SHA-256 `1c4305891b3133211f7127e3258f5d341e9105cec54481a7807af522189d7d31`; W2 manifests: `AdvRecallShapes/manifest.json` `710308a2c9c146631727e2e7d8a1b708f9f16fbde2181a3a802decdac1a40a9d`, `AdvDepth/manifest.json` `c556dccc545ec50f89353fa923a3d5edd202c36edb39ea3fcbb06ccb32ee391a`, `AdvVcsForms/fixtures/manifest.json` `fe4debcb577472e650f2bd23fa5e8de064f174ba23f00e50a994db4d187f439d` | `python3 -I .ufo/waves/round-20/a2/a2-guards.py 1f7f995 --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c` | Existing `guards-before-1f7f995.txt` receipt | recall_lost 0; crash_flip 0; pure_rows 23; vcs_fp 46; vcs_fn 0; a2_mismatch 4; dup_rows 0; no timeouts | 0 |
| Same guard fixture set | `python3 -I .ufo/waves/round-20/a2/a2-guards.py 28c6837 --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c` | recall_lost 52; crash_flip 13; pure_rows 24; vcs_fp 31; vcs_fn 0; a2_mismatch 6 | recall_lost 52; crash_flip 13; pure_rows 24; vcs_fp 31; vcs_fn 0; a2_mismatch 6; dup_rows 0; no timeouts | 0 |
| Same guard fixture set | `python3 -I .ufo/waves/round-20/a2/a2-guards.py 3610e3e --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c` | after: recall_lost 0; crash_flip 0; pure_rows 0; vcs_fp 20; vcs_fn 0; a2_mismatch 0 | recall_lost 0; crash_flip 0; pure_rows 0; vcs_fp 20; vcs_fn 0; a2_mismatch 0; dup_rows 0; no timeouts | 0 |
| Same guard fixture set | `python3 -I .ufo/waves/round-20/a2/a2-guards.py a8960de --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c` | after: recall_lost 0; crash_flip 0; pure_rows 0; vcs_fp 20; vcs_fn 0; a2_mismatch 0 | recall_lost 0; crash_flip 0; pure_rows 0; vcs_fp 20; vcs_fn 0; a2_mismatch 0; dup_rows 0; no timeouts | 0 |
| Harm watch at `a8960de`; committed tool identity `tools/mado-tripwire.py` SHA-256 above | `ROOT=<clone> OUTDIR=<absolute scratch>/harm bash .ufo/waves/round-20/harm-watch.sh a8960de` | PASS; 21 commands; 11 tripwire suites; gate selftest/regression; measure c1 22/30 | PASS; 21 commands (20 OK + 1 expected round-18 frozen baseline mismatch; 0 fail/skip), 11/11 tripwire selftests; gate selftest 0, regression 0; overall 0 | 0 |
| Round-17 c1, `.ufo/waves/round-17/measure.py` reads `corpus/QUALITY.md` SHA-256 `4da2cd62576ebea5a80028391e3a657ffa0505dd950f7ae563abb67cf47f4dd4` | `python3 -I .ufo/waves/round-17/measure.py a8960de` | 22/30 | 22/30 (score 7.3333) | 0 |
| Tally registry `.ufo/waves/round-20/tally-claims.json` SHA-256 `81eed3ebe33ec0bd2a7adbb5077c51a2624e00bccd945df83477f21674b3a48d` | `python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json --set all --rev a8960de --expect` | `EXPECT_SUMMARY: 9/9` | `EXPECT_SUMMARY: 9/9` (5 expected red mismatches + 4 green matches; 0 errors) | 0 |
| Census end / harm-watch validation, `corpus/SOURCES.md` SHA-256 `ff69dcc8c76f55eb1968092fa7486e53a1024c855e7249702880b2a100664b1e` | Included by the harm-watch command above (`sources-census.sh validate --file corpus/SOURCES.md`) | Four duplicate-URL warnings; final `ok`; exit 0 | Same four warnings (W04 S030, S042, S045, S097); final `ok` | 0 |

Guard populations were constant across runs: recall 81, crash 172, pure 24, VCS 74, and a2 9. The guard counter source in the receipts has SHA-256 `414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef`.

## Isolation harnesses

Each command was `bash .ufo/waves/round-20/isolation-check.sh <harness>` from the clone root. `exit` is the checker exit (not the subject harness exit). The checker uses only its generated `/tmp` targets and canary payload.

| Committed input path (SHA-256) | Stated | Reproduced | Checker exit |
|---|---|---|---:|
| `.ufo/waves/round-20/evidence/inns-r19-shape.sh` (`8bd507f0ea39d4d876359a0f5a1f798e810cda3c59293487af35d3a8df37ce9c`) | 5/6 FAIL_OPEN | 5/6 FAIL_OPEN; the unshare-refused mode is FAIL_CLOSED | 1 |
| `.ufo/waves/round-20/isolate.sh` (`89125ff7191f0d91799158c0e19695197784bda9e352c0fa0a59bbe0090b7f9a`) | 6/6 FAIL_CLOSED | 6/6 FAIL_CLOSED; positive control passed | 0 |
| `.ufo/waves/round-20/evidence/isolation-mutants/m1-nocmp.sh` (`2f2cc63bdb4903a42d99bf5685acc12e5b221158610217e42b0c1ee3d85df359`) | adversarial mutant exits 1 | FAIL_OPEN on mount-noop | 1 |
| `.ufo/waves/round-20/evidence/isolation-mutants/m3b-capprobe.sh` (`a6dde1c30355b29917091f0045b51befcefc7fc78d0903c098fc880ff9099727`) | adversarial mutant exits 1 | FAIL_OPEN on unshare-refused and mount-noop | 1 |
| `.ufo/waves/round-20/evidence/isolation-mutants/m4-skiptarget.sh` (`a9bfa1be563c76e74edffa480514e69f3ee85ead8415e54b865d02be10107940`) | adversarial mutant exits 1 | FAIL_OPEN on mount-noop and missing-target | 1 |
| `.ufo/waves/round-20/evidence/isolation-mutants/m6-besteffort.sh` (`ac11cc5adb1ece61eba4d45a8e2b65016576eb247957a846afe797b9118c6ed4`) | adversarial mutant exits 1 | FAIL_OPEN on mount-noop and partial-arm | 1 |
| `.ufo/waves/round-20/evidence/isolation-adversarial/fake-cmp.sh` (`63e22a710f888ef854b461019faae7b163a32546841450b9b1a0f11bac6926ff`) | adversarial harness exits 1 | FAIL_OPEN on mount-noop; injected cmp stub was observed | 1 |
| `.ufo/waves/round-20/evidence/isolation-adversarial/canary-deleter3.sh` (`87cb3526ae27fd4daaeeea9a2dbf2cb00a9f3891676823bf95cc74777f16e9b5`) | adversarial harness exits 1 | FAIL_OPEN (including witnessed execution and SKIP_AS_SUCCESS) | 1 |
| `.ufo/waves/round-20/evidence/isolation-adversarial/env-aware.sh` (`e3e32dca6992c1d8db4f7c07387dc955a988646a0d54a442977cf449df7154b8`) | adversarial harness exits 1 | FAIL_OPEN on mount failure, no-op, partial-arm, missing-target, and missing-stub | 1 |
| `.ufo/waves/round-20/evidence/isolation-adversarial/masked.sh` (`890df50ebbe2aebecbd47fee69967e1098667af3420300b571eea393b0863126`) | adversarial harness exits 1 | FAIL_OPEN on mount failure, no-op, partial-arm, missing-target, and missing-stub | 1 |

`isolation-check.sh` input SHA-256: `f7aa051faee522f3c4b61494a7a75078b469a1b0f1d0f7503caa3f89777736e1`. All 8 adversarial harnesses/mutants returned checker exit 1 as stated; both positive controls completed. The checker is scoped to fail-closed setup behavior, not sandboxing or containment.

## Limits

- The corpus-diff divergence is an input reproducibility issue: the external transcript corpus was live, no immutable snapshot manifest was available, and the two reruns began with different file counts. The exact historical count cannot be replayed from the committed lane alone. The manually annotated `.ufo/waves/round-20/a2/evidence/corpus-diff-28c6837-vs-a8960de-classified.txt` (SHA-256 `8d636a01cd163d77a29deaa98c9eaf60cb284e7aaaf5578abc36d6e500810e76`) has no standalone generator; the raw corpus-diff counter was rerun.
- The held-out result is only 2/12. That reproduces the stated score but does not establish broad out-of-suite generalization.
- The census helper is external to the lane: the old harm receipt records source commit `a51f7db4fb889a2f54399f6cde9a40d439959329`, while this rerun used the current helper commit `4a2bb5c3052e979d2203b31b2901da218419b6e9`. Both emitted the same four duplicate-URL warnings and `ok`; the helper provenance changed.
- Transcript JSONL was scanned as data and never executed. No host probe, compositor operation, or lane code edit was performed; the only lane write was this report.

## Installs

None.
