# ReScheduledNeighbour — wave-2 falsify, C1 neighbour re-run

Verdict: **no regression found. The tip classifier is strictly better than base on all three
CritScheduledNeighbour cases (3/3 exact-correct vs 0/3 false-observed), with no forbidden
`-S` row at any tier, and the no-harm guards I re-ran hold (frozen repair counter 12/12 on
tip vs 6/12 on base, round-21 oracle 35/35 + 17/17 on tip).** I attacked the landed C1 change
and could not re-open it on this population; residual risks are listed at the end.

## Identities (all verified by sha256, not assumed)

| artifact | sha256 |
|---|---|
| tip classifier, `git show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py` | `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009` |
| base classifier `evidence/tool-base-cd9da20c.py` | `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` |
| scan helper `.ufo/waves/round-21/oracle/measure.py` | `4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da` |
| repair expected.json | `53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9` |
| round-21 oracle expected.json | `fd2bfbc86897e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f` |

Blob identity: `git rev-parse 2e592aff:tools/mado-tripwire.py 2f1134f3:tools/mado-tripwire.py`
→ both `3f6e17663a68a2bb370d993e1fdd6860a26f0785`, so the wave-1 C1 tool change commit and the
lane tip serve identical classifier bytes. Diff base→tip on that file: 257 insertions, 21
deletions.

## Method

The critic's runner `cases.py` hardcodes the base commit, so I wrote a per-tool re-runner that
mirrors it exactly — same spec construction (`forbid_any` from string-list argv literals minus
truth, `want` = truth argvs as observed), same round-21 `scan()` (one `python3 -I` child,
384 MiB / 15 s), same `repair/measure.py` `judge()` (exact rule; its `forbidden` check is
any-tier). Truth is recomputed fresh each run through the critic's `truth.py` (recording fake
`subprocess`, real `threading`, gate admits only `subprocess`+`threading`), not copied from
`cases.json`.

```
mkdir -p /fast/scratch/hyaku/mado-r23/w2/ReScheduledNeighbour
cp -a .ufo/waves/round-23/w1/out/CritScheduledNeighbour/. /fast/scratch/hyaku/mado-r23/w2/ReScheduledNeighbour/
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930…:tools/mado-tripwire.py > tool.py
cp .ufo/waves/round-23/evidence/tool-base-cd9da20c.py tool-base.py
python3 -I run_tool.py tool-base.py base-run.json      # fresh dir, no __pycache__
python3 -I run_tool.py tool.py      tip-run.json
python3 -I <lane>/.ufo/waves/round-23/repair/measure.py --tool tool.py        # exit 0, 12/12
python3 -I <lane>/.ufo/waves/round-23/repair/measure.py --tool tool-base.py   # exit 1, 6/12
python3 -I run_oracle.py tool.py                                                      # 35+17
```

All scans sequential (one child at a time), runner itself read-only over committed fixtures.
Fresh-dir check: no `__pycache__`/`*.pyc`. Receipts:
`/fast/scratch/hyaku/mado-r23/w2/ReScheduledNeighbour/{base-run.json,tip-run.json,run_tool.py,run_oracle.py}`.
Python 3.14.8 throughout. No tools installed or updated. No lane writes except this report.

## Per-case results (the core deliverable)

Fixtures re-verified byte-identical to `cases.json` sha256s. Truth identical to the critic's
recorded truth on 3/3.

| case | truth (executed) | base rows (all tiers) | tip rows (all tiers) | tip vs base |
|---|---|---|---|---|
| ThreadTargetReadsShadowedGlobal | `pacman -Q r23w1-thread-global` | `host_mutation` `pacman -S r23w1-thread-foreign` **observed** — false positive on a never-executed `-S`, truth missed | `package_query` `pacman -Q r23w1-thread-global` observed; exact pass; forbidden `[]`; unparsed 0 | **better** |
| TimerFunctionReadsShadowedGlobal | `pacman -Q r23w1-timer-global` | `host_mutation` `pacman -S r23w1-timer-foreign` **observed** — same harm class | `package_query` `pacman -Q r23w1-timer-global` observed; exact pass; forbidden `[]`; unparsed 0 | **better** |
| ThreadRunFromForwarder | `pacman -Q r23w1-run-global` | `host_mutation` `pacman -S r23w1-run-foreign` **observed** — same harm class | `package_query` `pacman -Q r23w1-run-global` observed; exact pass; forbidden `[]`; unparsed 0 | **better** |

Worse-than-base count: **0**. No tip error, no exit anomaly (all exit 1 = findings present,
`error: null`), no lost rows, no new false positives at any tier (`evidence` ∈ observed/lead/
potential all checked by the judge's any-tier forbidden scan and by my `forbidden_hit` set
intersection over all returned rows).

Fidelity cross-check: my fresh base rows equal the critic's recorded `cases.json` base rows on
3/3 (labels `base-false-observed` reproduced), so the critic's wave-1 numbers were not an
artifact of their harness.

## No-harm re-runs on the tip

- Frozen 12-case repair counter (`repair/measure.py`): **tip 12/12, exit 0** — matches the
  registered after-value. Base re-run: **6/12, exit 1** — matches the registered before-value,
  same failing ids (`ReturnedGlobalCallableShadow`, `ForwardExistingClosureWithoutFrame…`,
  `ForwarderInvokesCallback`, `CallerLocalShadowsHelperGlobal`, `ForwarderPassesCallerArgument`,
  `ForwarderInvokesFactoryClosure`).
- Round-21 oracle over the unchanged snapshot: **tip 35/35 primary + 17/17 supplemental, zero
  failures** — the module-scope Thread guards (`CallbackGlobal` etc.) the critic said must
  stay passing do stay passing.

## Residual risk and verification gaps

1. **Un-authored overcorrection guard still missing.** The wave-1 critic's report names a
   fourth case it was capped from authoring: `Thread(target=helper, args=(argv,))` started
   from a shadowing frame, truth = the starter's local. If the tip now resolves non-closure
   scheduled targets against defining-frame globals at call time, a candidate that
   over-applies that rule to *construction-time* args would regress it, and nothing in my
   population would notice. My item authorized re-running the three existing cases only, so I
   did not author it. Recommendation to the L1: add that fixture to the C1 counter before the
   scheduled path is considered closed.
2. **Not re-run by this seat** (out of item scope, registered values stand unverified here):
   the 1356-file corpus comparator, precision 166/175, the eleven selftest suites, C2 and C3.
3. Truth for these cases comes from the critic's `truth.py` variant whose gate admits
   `threading` (declared deviation from the frozen `repair/truth.py`, which would reject these
   fixtures as `unsafe_fixture`). I re-executed it fresh and it matched the recorded truth, but
   the C1 counter itself still cannot ingest these fixtures — folding them into the frozen set
   requires deciding that gate question.

Verdict line: **tip better on 3/3 neighbour cases, 0 regressions, no-harm guards hold on
everything I re-ran; C1 falsification attempt failed (in the good sense), one concrete
adversarial fixture remains unauthored.**
