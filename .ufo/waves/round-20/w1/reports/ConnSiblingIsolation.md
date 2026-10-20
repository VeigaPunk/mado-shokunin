# ConnSiblingIsolation — an inner `|| exit` is not fail-closed once a wrapper can still reach the canary

Criterion 29 (C2) is red on the round-19 control flow even under `set -e`. Sibling lanes already contain the green token `mount || exit 97` on a branch that is not the one that runs the payload. Scoring the token, or scoring "canary absent" alone, greens those wrappers.

## Evidence

### The incident chain is non-final `&&`, then the payload

`mado-shokunin/.ufo/waves/round-19/w2/reports/SentinelGatePath.md:77` states the mechanism: the first `inns.sh` used `[ -e ] && mount && echo`, that chain does not trip `set -e`, and `/usr/bin/hyprctl probe` still ran. The heredoc is one JSONL record, not a lane file: `~/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR19/MadoR19.SentinelGatePath.jsonl:33` writes `set -e`, then `[ -e "$p" ] && mount --bind … && echo "armed $p"`, then `set +e` and `"$@"`. The later heredoc at `:36` is the repair (`mount || exit 99`), not the red shape. Pre-registration of the red shape: `mado-shokunin/SCORECARD.md:1266-1268`.

This seat did not re-run `unshare` or `mount`. `ScoutUnshareHost.md:32-47` (same wave) already reproduced mount rc 32 under `--map-current-user`, outer rc 0, canary present, including with `set -e`. Independent of mount, bash 5.3.20 reproduces the control flow with `false` standing in for a failed setup (`/tmp/conn-sib-iso`, canary writes only):

| case | script tail | result |
|---|---|---|
| L | `set -e; [ -e "$dir" ] && false && echo armed; echo PAYLOAD` | stdout `PAYLOAD`, exit 0 |
| C | `set -e; [ -e "$dir" ] && false; echo PAYLOAD` (`false` is the last `&&` element) | no PAYLOAD, exit 1 |
| G | `set -e; [ -e "$dir" ] && false && echo PAYLOAD; echo AFTER` | `PAYLOAD` skipped, `AFTER` printed, exit 0 |
| J/K | same chain as L, grafted `\|\| exit 99`, with and without `set -e` | no PAYLOAD, exit 99 |
| M | probe set to 0, else-branch `touch` canary | file created, exit 0 |

`set -e` aborts only when the failing command is the last element of the `&&` list (C). An `echo` after `mount` in that list is what keeps the mount failure from aborting (L). Putting the payload inside the list does not abort a later statement (G).

### Sibling wrappers that already contain `|| exit` and still run a body

- **Probe, then optional wrap.** `game-dev-2d-shokunin/reports/round-102/mutations/ver3_export_probe.py:422-425` sets `unshare` from `mount -t tmpfs … && test -w /tmp`. `run_shell` at `:110-114` uses `mount … || exit 97` only when that flag is true; the else is `["/usr/bin/sh", "-c", body]`. `mut08_filter_case_inversion.py:293-308` is the same split: probe `mount && echo UNSHARE_OK`, and on failure `godot_cmd` returns the bare argv. The spec states the policy: `reports/round-101/r101-E0-spec.md:105-106`, "Without unshare the arms still run".
- **Inner exit does not bind the parent.** `game-dev-2d-shokunin/reports/round-102/mutations/r102-crit1-attack.sh:16` is `set -u` only (no `set -e` in the file). `:119-124` is `unshare … "mount … || exit 97"` plus exports. `:125-131` (`stat`, then `run` of binaries) is outside that string, so an `unshare` failure does not stop them.
- **Skip returns 0, so the closed helper never runs.** `chousa-shokunin/tools/research-gate.sh:4653-4658` is actually closed when called: `mount … || exit 97`, then the fixture write `|| exit 98`, then `exec` of the gate. `tnscase` at `:4666-4671` does not call it when `NS_STATE != yes`; it increments `SKIPPED` and `return 0`. Setup failure and a green case are the same status.
- **The repaired doctrine for that skip.** Fleet `.ufo/reports/round-10/kagi.md:76-77`: `SKIP` was fail-open on infra failure and became `UNVERIFIED`, exit 1. Landed bytes: `kagi-shokunin/corpus/surface-census.sh:395-406` (`FAILED=1` unless the error matches `locked|busy`, which stays `SKIP` and does not set `FAILED`) and `:865-867` (nonzero `FAILED` prints `DRIFT` and `exit 1`). A zero-probe verbs summary is the same rule at `:874-881`.

`kotodama-shokunin/reports/round-37/calib/Ca08-verify.md:23-25` rejected a weaker isolator for the same reason a token check is weak: `GIT_CEILING_DIRECTORIES` still resolved the live checkout, so those runs were excluded. That report does not show `bwrap`'s failure branch.

Fleet `.ufo/reports/round-1*` has no second unshare harness. "namespace" hits there are round-numbering or souji census scope. `round-16/tameshi.md:111` names `bwrap` confinement as an open debt, not a landed abort. `chousa-shokunin/tools/research-gate.sh:1190-1193` and `corpus/knowledge/mount-alias-r14.md:52-53` are a different fail-open (unmeasurable `stat` accepts a source). They are not a payload harness.

PATH-prepend stubs (`mado-shokunin/tools/mado-verify.sh:1410`, souji `PATH="$MOCK:$PATH"` harnesses) fall through to a host binary when the stub dir lacks the name. That is adjacent and out of criterion 29's registered red. Folding it in would score a different defect than `SCORECARD.md:1266-1268`.

## Affected axes

- **C2 / criterion 29.** Improves if the checker is red when any wrapper path creates the canary or returns 0 on setup failure, and green only when setup failure exits nonzero before the canary. Harmed if "contains `|| exit`" or "`set -e`" or "canary file absent" is the oracle: the first matches ver3, r102-crit1, and `ns_run`; the second matches the incident script; the third matches `tnscase`'s skip.
- **C1.** No tripwire change. The canary stays a `/tmp` file, which is the payload the claim already bounds.

## Proposed move

Give criterion 29 three red fixtures and one green, all with `false` or a missing command in place of `mount` except where `ScoutUnshareHost.md` already measured real mount rc 32. Do not add a probe-fallback.

1. **Red, incident list.** `set -e`; `[ -e "$target" ] && false && echo armed`; then the canary. Want: canary present, exit 0. This is jsonl `:33`, not the repaired `:36`.
2. **Red, sibling else-branch.** A flag computed by a failing probe; the `|| exit 97` string exists only on the true branch; the false branch writes the canary (`ver3_export_probe.py:110-114`). Want: that shape is a failure of the harness under test. Textual presence of `|| exit` must not pass.
3. **Red, skip.** Setup helper returns 0 without writing the canary (`research-gate.sh:4668-4671`). Want: exit 0 with no canary is still red. kagi's `UNVERIFIED`/`exit 1` (`surface-census.sh:405-406`) is the status rule; do not copy kagi's `locked|busy` exception into a mount harness.
4. **Green.** One sequence, no else: failing setup `|| exit 125`, then the canary (`ScoutUnshareHost.md:49-68`, same shape as `research-gate.sh:4654` before `exec`). Want: canary absent, exit 125. Case J shows the `|| exit` may be grafted on the `&&` list; it does not need its own statement, and it does not need `set -e`.

## Risks

- Requiring the literal token `|| exit` false-reds case C, which already aborts (exit 1, no payload) because the failing command is the last `&&` element. Score status and the canary, not the spelling.
- `mount && exec` as the entire `-c` (mut08 `:307`, and `game-dev-3d-shokunin/reports/round-103/gate/sentinel.md:186`) skips that payload and returns the mount status when the list is the whole script. One following statement (case G) drops the status to 0 and runs. Do not treat `&& exec` as the template.
- The repaired inns loop still `exec`s when every path misses (`[ -e ] || continue`, jsonl `:36`). Case analogue: missing path, then payload, exit 0. A red fixture whose only fault is a missing target cannot separate the incident script from that repair. The discriminating fault is an existing target and a failing mount.
- Copying `ver3`'s probe into `isolation-check.sh` makes criterion 29 green on a host where the probe works and never executes red 2.
- Running chousa's `ns_run` or any sibling `unshare` against a host path reopens R19-V4. The fixtures above do not need that.

## Verification

Re-run the bash table (L, C, G, J/K, M) under `bash --version` 5.3.x with a `/tmp` canary. Diff the red script against jsonl `:33` only. Grep the checker for an else/fallback around the gate (red 2) and for a `return 0` / `SKIP` on setup failure (red 3). Do not invoke `hyprctl`, `mount` on `/usr`, or `research-gate.sh --selftest` as part of this check.

## Limits

Did not execute sibling harnesses (godot exports, chousa selftest, kagi census, kotodama `bwrap`). Did not recover `bwrap`'s failure branch. Fleet `round-1*` was searched for `unshare|bwrap|fail-open|namespace`, not read line by line. PATH-prepend stubs were not modeled. No live host-state recheck of the round-19 probe. `ScoutUnshareHost.md` mount results are that seat's runs; this seat's runs are the `false` canaries only.

## Installs

none
