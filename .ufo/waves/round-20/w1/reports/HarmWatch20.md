# HarmWatch20-3 — PASS: receipt-backed baseline harm watch completed

## Implementation

Added `.ufo/waves/round-20/harm-watch.sh` (SHA-256 `694e1f1afd615e846f10ead79bf94ef675a54524eea2c157d32cb652ef35a9b8`). It accepts an absolute `ROOT` test checkout and absolute `OUTDIR`, defaults OUTDIR to `.ufo/waves/round-20/evidence/harm`, and writes per-command receipts with `measured_commit=REV` and a final `exit=N` line. Lane tools are run only after their worktree SHA-256 matches `git show REV:path`; pin failures are recorded and skipped. See script lines 5–10, 34–39, 124–180.

The navigation command now checks `SCORECARD.md` against REV and extracts/runs the counting block only from the verified `git show` bytes; it does not run a differing worktree block (lines 388–435). The regression helper is materialized under the runner's private `/tmp` scratch directory only after its digest matches the hash embedded in the pinned gate (lines 199–246, 254–280). Census validation is scoped to the clone's `corpus/SOURCES.md` and runs an exact copied parser whose bytes are pinned to its own fleet git blob (lines 439–478).

## Run and retained evidence

Clone identity was `e629f731172b8238caffe50f152217ce56535fb4` (`git -C /tmp/mado-r20-HarmWatch20-3 rev-parse HEAD`). The only run used the clone and `/tmp` output:

```text
ROOT=/tmp/mado-r20-HarmWatch20-3
OUTDIR=/tmp/mado-r20-HarmWatch20-3-harm-evidence
HARM_TIMEOUT=1800
bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/harm-watch.sh e629f731172b8238caffe50f152217ce56535fb4
HARM_WATCH: PASS
```

Summary: `/tmp/mado-r20-HarmWatch20-3-harm-evidence/harm-watch-summary.txt:25-35` records 20 commands, 19 exit-0 checks, zero failures/skips, and one expected round-18 frozen baseline. The 11 tripwire selftest suites passed (`:5-15`); there was no `.ufo/waves/round-20/tripwire` in this revision (`:16`). Round-18 frozen replay returned the expected `frozen_verdict_mismatch`, exit 1, recorded as baseline (`harm-tripwire-frozen-round-18.txt:1-5`); round-19 replay was `frozen_match`, exit 0 (`harm-tripwire-frozen-round-19.txt:1-4`). Round-20 frozen was absent (`summary.txt:19`).

Additional observed results:

- Gate selftest: `MADO_SELFTEST: 460/460 assertions passed`, exit 0 (`harm-gate-selftest.txt:1-3`). Gate regression: PASS, 10/10 killed, zero flips/inconclusive, control green and restore OK (`harm-gate-regression.txt:6-16`). The exact helper SHA recorded by the gate (`b56c6e57…fd22bcb`) was found in tameshi commit `44947154c23772f766f9f5439090fb5c7ad76e46` and copied to `/tmp`; the current helper worktree has a different digest, which the pin ledger records (`harm-watch-pins.txt:4`).
- Classifier selftest: 52/52, exit 0 (`harm-action-plan-selftest.txt:55-56`).
- Round-17 measure at the clone revision: exit 0, c1 `20/28`, score `7.1429`; c2 count 6, score `10.0` (`harm-measure-round-17.txt:1-13`).
- Round-19 recall counter: 6/6, score 10.0, exit 0 (`harm-tw-recall.txt:1-10`). `tw-precision.py` was absent at this pre-registration revision and was not run (`summary.txt:22`).
- Navigation: 34/34 indexed, no missing, dangling or duplicate notes; exit 0 (`harm-nav-fleet-round-1.txt:1-4`). The scorecard worktree and REV SHA matched at `0139a1a4…e62914`; the executed block SHA is `8b59b503…04a7b88`.
- Census: exit 0 on the clone registry; four W04 duplicate-URL warnings were emitted (`harm-census-validate.txt:1-8`). Its parser SHA is `3fb72615…d4a64e30`, pinned to fleet commit `b332af20722cb4adb02ca6c0ccbe6b1111bf2379`; the input measured was the clone file at REV, not the live fleet roster.
- Lane tool pin receipts show worktree==REV bytes for the gate, classifier, tripwire, round-17 measure, round-19 recall and SCORECARD (`harm-watch-pins.txt:2-3,5-21`). Census parser provenance is separately recorded on line 22.

## Round-19 harm-watch limits

- `measure-mutants.py --workdir` caller-directory deletion was already fixed in round 19; this runner does not exercise that tool (`corpus/lessons/round-19.md:110-111`).
- The `--out` guard still covers only the `--lane` worktree; not changed or exercised here (`:112`).
- **Fixed here:** the prior worktree `SCORECARD` block execution; the revised runner verifies full SCORECARD bytes at REV and runs the block extracted from the pinned REV copy (`harm-watch.sh:388-435`).
- `supersede-sweep.py` still reads its ledger from the worktree; not invoked or changed (`corpus/lessons/round-19.md:112-113`).
- `anchor-durability.py` still exits 1 for a malformed receipt line; not invoked or changed (`:114`).
- `frozen-repin.py` still writes its README receipt without `measured_commit`; not invoked or changed (`:115-116`). This runner's own frozen replay receipts do include `measured_commit=REV`, but that does not repair `frozen-repin.py`.
- The separately noted frozen pin-spelling/normpath limitation was not tested or changed (`SCORECARD.md:1213-1216`).

## Limits

The baseline commit predates the round-20 precision script, tripwire suite and frozen directory, so those optional checks were unavailable and are explicitly noted rather than inferred. The census check intentionally validates only the cloned lane registry, not a fleet-wide census. No live gate, host probe, build, lint or unrelated suite was run. The results do not claim post-integration verification.

## Installs

none
