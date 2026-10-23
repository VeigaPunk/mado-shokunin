# RcVerdictGateLiveFilePlane309 — C2 ledger attack on a3w1 seat CapVerdictGateLiveFilePlane309

Seat: `MadoR25A3.RcVerdictGateLiveFilePlane309` (reviewer, DATA+FALSIFY wave a3w2). Target:
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/a3w1/reports/CapVerdictGateLiveFilePlane309.md`
(C2 row re-run of `SCORECARD.md:309`, `verdict gate (live + file plane)`, measured base `41cc04c8`).

## What I re-derived

- Base blob `git -C <lane> show 41cc04c8:SCORECARD.md`: 1,618 lines,
  sha256:`6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08` — matches the report. Row 309 verbatim
  as quoted: `| verdict gate (live + file plane) | Read-only verdict over the declared config plane and live hyprctl
  surfaces, exit 0/1/2, boundary check | \`bash tools/mado-verify.sh\` → \`MADO_VERIFY: CLEAN (52 pass, 8 notes …)\`,
  \`.ufo/evidence/round-12/gate-live-after.txt\` | 5 (re-demonstrated 12) |`.
- Evidence pointer `.ufo/evidence/round-12/gate-live-after.txt` present at base, 66 lines; head is the raw gate banner
  (no measured-commit header — report's "round-12-era receipt shape" accurate); tail `pass=52 fail=0 unknown=0
  skip=0 note=8`, `CLEAN (52 pass, 8 notes)`, `exit=0`; `live.consumer.hypridle NOTE` (hypridle absent) at line 23 —
  the exact one-status delta the report's 52/8 → 53/7 reconciliation names.
- Own sandbox: `git clone -q <lane> /fast/scratch/hyaku/mado-r25a3/rc/CapVerdictGateLiveFilePlane309`,
  `checkout --detach 41cc04c8` → `rev-parse HEAD` = `41cc04c8d593837a0d5078bffaacdaa163d12897`. Gate bytes
  sha256:`050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1`, 4,194 L — matches report and the
  `SCORECARD.md:1221-1222` pin (`050efc72…`, 4,194 L, selftest 460/460).
- Demonstration command re-run exactly, GIT_* unset, `timeout 600 prlimit --as=4000000000 -- bash
  tools/mado-verify.sh` from the clone root: **exit 0, `MADO_VERIFY: CLEAN (53 pass, 7 notes; file + live planes
  verified read-only)`**, `counts: pass=53 fail=0 unknown=0 skip=0 note=7`. Diff of my 66-line output against the
  report's quoted 66-line block: exactly one line — `live.hypr.instances PASS 5 instances` vs their `4 instances`
  (fleet nested-instance count moved between runs; row still PASS, "targeting the session's own signature"). Every
  other field byte-identical, including `gate boundary.readonly PASS … ddb0780742f8…` — the same combined sha means
  the live `$HOME` config plane was identical across both runs, corroborating that their output is a real same-day
  live run, not a stale or copied block.
- Exit-map probes re-run independently: `--bogus` → usage text + `exit=2` (verbatim match);
  `--no-live --root $(mktemp -d)` → `counts: pass=1 fail=14 unknown=7 skip=12 note=6`,
  `DIVERGED … first fail: hypr.file.root`, `exit=1` — identical counts to the report's probe. Exit map 0/1/2
  independently confirmed.
- Superseding pointer `SCORECARD.md:1576` verified: round-24 `### Capability status` row `| verdict gate (live +
  file plane) | works | \`--no-live\` prints a \`MADO_VERIFY:\` verdict, exit 0 at \`8e5d9369\`; live layer not
  exercised |`, with the preamble (1568-1571) stating it supersedes implied `works` of earlier rows. The report's
  ledger line names exactly this row and correctly notes the live arm is what it re-demonstrated.
- Complementary cites spot-verified: line 30 round-11 live-DIVERGED caveat (waybar coredump, operator-owned,
  superseded); lines 122/287/400/533/653 are `--no-live`-only readings (narrower, not contradictions); line 954
  `JjAuditMado F10` — at base, `tools/mado-verify.sh:3406` is indeed the `live.plane UNKNOWN` row inside
  `live_plane()`, and the selftest OM9 scenario (`tools/mado-verify.sh:872-884`) guards "a FAILING git show reads
  UNKNOWN, never a local edit" — the stale-line-pointer / fixed-defect call is accurate.
- Missed-superseding sweep: greps for `verdict gate|mado-verify|MADO_VERIFY|live plane|live layer|DIVERGED|gate`
  across the whole base SCORECARD; after line 954 the only row naming this capability is 1576; all other late
  mentions are harm-watch/selftest/tripwire counts or other capabilities. No contradicting text missed.

## Findings

No defects. Row text, evidence pointer, revision, gate sha, command form, exit code, verdict line, boundary check,
and the superseding-pointer column all reproduce independently. The ledger line's only live-dependent field
(instance count) drifted 4→5 in my re-run — session state, not a defect, and the row itself still reads PASS.
`git status --porcelain` in the clone: 0 lines after all runs.

## Cleanup

Clone deleted (`rm -rf /fast/scratch/hyaku/mado-r25a3/rc/CapVerdictGateLiveFilePlane309`, verified absent);
`/tmp/rc309-*` scratch files removed; `mktemp` probe root removed. No lane writes besides this report; gate ran
read-only (its own boundary check PASSed in my run).

RECHECK CapVerdictGateLiveFilePlane309: agree — ledger line re-derives cleanly at 41cc04c8 (exit 0, CLEAN 53/7, boundary PASS, exit map 0/1/2 confirmed, superseding cite SCORECARD.md:1576 accurate); only transient drift is live Hyprland instance count 4→5.
