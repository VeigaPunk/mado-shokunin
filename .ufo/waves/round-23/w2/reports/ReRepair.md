# ReRepair — WAVE 2 falsification of C1 (repair-set operability) at lane tip 2f1134f3

Seat: MadoR23.ReRepair (leaf; no subagents used). Date: 2026-10-22.
Scope: re-run the landed C1 after-measurement from extracted committed bytes, re-open the
harness for counterexamples, verify per-case rows against `expected.json`.

## What I did (exact commands)

Fresh scratch dir, no `__pycache__`; tool extracted from the landed tip, not the working tree:

```
mkdir -p /fast/scratch/hyaku/mado-r23/w2/ReRepair
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show \
  2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py \
  > /fast/scratch/hyaku/mado-r23/w2/ReRepair/tool.py
sha256sum /fast/scratch/hyaku/mado-r23/w2/ReRepair/tool.py
# 41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009  tool.py

python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/measure.py \
  --tool /fast/scratch/hyaku/mado-r23/w2/ReRepair/tool.py     # exit 0
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/truth.py   # exit 0
```

Runs were sequential (one classifier child at a time), `python3 -I`, committed fixture data only.

## Headline results

- `measure.py`: `schema mado-r23-repair-measure-v1`, `passed: 12, total: 12`, **exit 0**.
  `tool_sha256 41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009` (matches
  registered `41489991...`); `helper_sha256 4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da`;
  `expected_sha256 53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9`.
- `truth.py`: `schema mado-r23-repair-truth-v1`, `passed: 12, total: 12`, **exit 0**, python 3.14.8.
- Every case: `passed: true`, `unparsed: 0`, `exit: 1` (allowed by the pass rule "exit 0 or 1"),
  `error: null`, and no `forbid_any` command appears in any row or executed set.

## Per-case rows vs expected.json

`want` columns read from `expected.json` (I re-fetched the full case table, not the elided read):
measure rows are the scanner's `(class, command, evidence)`; truth `executed` is the argv set
recorded by the fake `subprocess` module. `exact` requires the sorted row triple to equal `want`;
`present` requires `want_present` commands in rows with evidence `observed`/`lead`.

| # | Case | Kind | expected want | measure row | truth executed | Pass |
|---|------|------|---------------|-------------|----------------|------|
| 1 | ReturnedGlobalHelper | exact | (package_query, `pacman -Q r22-nhb-module`, observed) | identical | `pacman -Q r22-nhb-module` | ✓ |
| 2 | CallerArgumentBeforeClosureOverlay | exact | (package_query, `pacman -Q r22-callsite-argument`, observed) | identical | `pacman -Q r22-callsite-argument` | ✓ |
| 3 | ReturnedGlobalCallableShadow | exact | (package_query, `pacman -Q r22-global-callable`, observed) | identical | `pacman -Q r22-global-callable` | ✓ |
| 4 | ForwardExistingClosureWithoutFrameContamination | exact | (package_query, `pacman -Q r22-forward-global`, observed) | identical | `pacman -Q r22-forward-global` | ✓ |
| 5 | ForwarderInvokesCallback | exact | (package_query, `pacman -Q r23-forward-global`, observed) | identical | `pacman -Q r23-forward-global` | ✓ |
| 6 | CallerLocalShadowsHelperGlobal | exact | (package_query, `pacman -Q r23-local-global`, observed) | identical | `pacman -Q r23-local-global` | ✓ |
| 7 | NestedDefReadsDefiningFrame | exact | (package_query, `pacman -Q r23-nested-local`, observed) | identical | `pacman -Q r23-nested-local` | ✓ |
| 8 | LateGlobalRebinding | exact | (package_query, `pacman -Q r23-late-global`, observed) | identical | `pacman -Q r23-late-global` | ✓ |
| 9 | ForwarderPassesCallerArgument | exact | (package_query, `pacman -Q r23-forwarded-argument`, observed) | identical | `pacman -Q r23-forwarded-argument` | ✓ |
| 10 | ForwarderInvokesFactoryClosure | exact | (package_query, `pacman -Q r23-closure-captured`, observed) | identical | `pacman -Q r23-closure-captured` | ✓ |
| 11 | CallbackStoredInDict | present | want_present `pacman -S r23-hook-dict` | (host_mutation, `pacman -S r23-hook-dict`, lead) | `pacman -S r23-hook-dict` | ✓ |
| 12 | CallbackStoredOnAttribute | present | want_present `pacman -S r23-hook-attr` | (host_mutation, `pacman -S r23-hook-attr`, lead) | `pacman -S r23-hook-attr` | ✓ |

`forbid_any` (e.g. `pacman -S r22-nhb-factory-local`, `pacman -S r23-*-foreign`): absent from all
measured rows and all executed sets. H4's caller-frame leak case (`ForwarderInvokesCallback`)
yields exactly the global-lead row, no foreign argv — the overcorrection cases 6–8 and forwarder
cases 9–10 each produce exactly their one expected row, no extra findings.

## Provenance / anti-tamper probes (all passed)

- Blob identity: `git rev-parse 2e592aff` = `2e592aff01be2bdd3039f3a825864078cdff86b5`;
  `tools/mado-tripwire.py` blob id at that commit and at tip `2f1134f3` is the same
  `3f6e17663a68a2bb370d993e1fdd6860a26f0785` — C1 bytes unchanged between the C1 commit and the
  lane tip, and they extract to the registered sha256. (First probe of `2e592aff` used a guessed
  full sha and printed nothing; redone with `rev-parse` as shown.)
- Harness committed, not dirty: `git status --porcelain .ufo/waves/round-23/repair/` empty;
  working `measure.py`/`truth.py`/`expected.json` sha256s equal `git show 2f1134f3:...` bytes.
  Round-21 helper `.ufo/waves/round-21/oracle/measure.py` also working==committed and equals the
  `helper_sha256` printed by measure.py.
- `expected.json` sha256 = `53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9`
  (matches the frozen constant in both harness scripts; verified independently with sha256sum).
- Round-22 copies byte-exact: the four supplemental fixtures under
  `round-22/residual-truth/<Case>.jsonl` have sha256 identical to
  `round-23/repair/fixtures/<Case>.jsonl` (bba51318…, 79931530…, 6b3d8382…, d3d8222a…), matching
  the origin shas recorded in `expected.json`. (They live flat in `residual-truth/`, not under
  `fixtures/` — first provenance probe used the wrong layout and is corrected here.)
- 12 fixture files present; scripts' internal pre/post tamper checks did not trip (exit 0, not 2).

## Falsification attempts → no counterexample found

Tried to break the claim via: wrong-byte extraction (tool sha mismatch would have surfaced — it
didn't); modified/dirty harness or fixtures (none); helper swap (hash recorded and matched);
fixture provenance drift from round-22 (byte-exact); per-case row drift vs `expected.json`
(exact match on all 24 row triples / want sets); truth-vs-scanner disagreement (none: scanner
rows and truth-executed argv agree on all 12).

## Verdict

**PASS — confirmed.** C1 after-value 12/12 reproduced at the landed tip
`2f1134f38930fc8b067d2d7f5bba126338faabdd` from extracted committed bytes
(sha256 `41489991…`), truth oracle 12/12, per-case rows exactly as frozen in `expected.json`,
round-22 fixture copies byte-exact. Registered C1 value is honest; I found nothing to falsify.

## Residual risk / verification gaps

- I re-ran only the C1 repair counter and truth oracle. The C1 no-harm guards (round-22 primary
  57/57, round-21 oracle 35/35+17/17, precision 166/175 same passing set, eleven selftest suites
  247/247, 1356-file corpus comparator, resource caps) were not re-run in this seat; a passing
  repair set alone does not establish the full no-harm claim.
- Single host runtime (python 3.14.8), one pass per oracle; no variation in environment attempted.
- Harness scripts were read from the committed tree and hash-matched; I did not audit the
  round-21 `scan` helper's internals beyond its committed-clean hash.

No tools were installed or updated for this seat (nothing to record under the tooling directive).
No lane files were modified other than this report.
