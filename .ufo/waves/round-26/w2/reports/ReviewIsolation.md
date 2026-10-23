# ReviewIsolation — w2 host-safety re-check (mado round 26)

Re-ran `harness/pilot.py` once at lane tip `1b0b91e9`, re-checked every w1 IsolationProbe
(`w1/reports/IsolationProbe.md`) and SentinelHarness (`w1/reports/SentinelHarness.md`) finding, and
dynamically tested the K1LabelKeyed `/proc/1/environ` leak claim. All runs from cwd
`/home/vgpnk/Projects/shokunin/mado-shokunin` or scratch `/fast/scratch/hyaku/mado-r26/review-isolation/`;
every command I started ran with `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE` removed, under `timeout`
and `prlimit --as=4000000000:8000000000`. Live compositor contacted with read verbs only (`instances -j`).
No lane file edited except this report; no installs; no git/jj writes; no process left running.

## Exact commands

```sh
df -h /fast /tmp
timeout 60 coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland   # before + after
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 5 hyprctl instances -j     # before + after
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000:8000000000 \
  timeout 120 python3 .ufo/waves/round-26/harness/pilot.py                               # the assigned run, once
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE MADO_REVIEWISOLATION_CANARY=1 \
  prlimit --as=4000000000:8000000000 timeout 90 python3 <scratch>/probe_runner.py        # /proc/1/environ probe
prlimit --as=4000000000:8000000000 timeout 60 python3 <scratch>/probe_snapshot.py        # snapshot symlink probe
```

Probe scripts import the unmodified `harness/oracle.py` by path and call its `run_tool()` /
`snapshot()`; neither probe starts Hyprland (run_tool's bwrap contains no compositor).

## Pilot re-run receipt (verbatim, once)

```text
harness tinywl sha256:227a74af3455c4cd90ef0fc64edf3c927ddf7f0b9b4bf903bdc30b3aeea40cda libwlroots sha256:1f3d7036c91417c0b6efccf67ad0d368a30818df630f07bb92574a13527a7967 render_node=/dev/dri/renderD129
before: hyprland_coredumps=1335 live_instances=1
nested process (host view): {"card_nodes": [], "env": ["WAYLAND_DISPLAY=wayland-0", "XDG_RUNTIME_DIR=/tmp/m26o-af8a2g23"], "netns_same": false, "pid": "1885817", "render_mounts": ["/dev/dri/renderD129"], "run_user": false}
oracle answered: binds=192 animation_nodes=35 beziers=6
after: hyprland_coredumps=1335 live_instances=1 delta_coredumps=0
leftover private runtime dirs: 8; nested processes alive: 3
PILOT NOT_OK
exit=1
```

Host-side comparison around the run: `coredumpctl` `/usr/bin/Hyprland` lines **1335 → 1335**
(delta 0); `hyprctl instances -j` **1 → 1** (same instance `efb5099378007946…`). `PILOT NOT_OK` came
only from its host-global clauses: 8 `/tmp/m26o-*` dirs and 3 nested Hyprland processes were host-wide
fleet state (peers' counters), not the pilot's own run — the pilot's own dir `m26o-af8a2g23` was removed
and its nested pid 1885817 was gone when checked minutes later. This reproduces IsolationProbe's F1–F5.

## Findings (by severity)

| # | w1 finding | w2 verdict | evidence |
|---|---|---|---|
| S1 | MEDIUM — `run_tool` has no memory/output/core bound (`oracle.py:231-243`: `subprocess.run(capture_output=True)`, no prlimit; coredump check counts only `/usr/bin/Hyprland`, `oracle.py:60-62`) | **confirmed** (code + facts) | Line anchors re-verified verbatim at tip (sha256 `680798ed…`). Host facts re-observed: inherited `ulimit -c` = `unlimited`, `core_pattern` = `\|/usr/lib/systemd/systemd-coredump …`. A tool `os.abort()` would produce a host systemd-coredump invisible to the counter's check. Did not trigger an actual core (would be the defect itself, harmless but unnecessary). |
| S2 | MEDIUM — symlinked config roots/files copy unrelated readable data into the tool sandbox (`oracle.py:69-85`: `realpath` + `isfile`/`open`, no containment; mounted at `/snap/home` via `oracle.py:234`) | **confirmed** (dynamic) | `probe_snapshot.py` called unmodified `snapshot()` on a crafted tree: file symlink `.config/hypr/host.conf → /etc/hostname` was copied through (content `plazir27\n` — the real hostname), and directory-symlinked root `.local/state/omarchy/toggles/hypr → outside-dir` was copied through (`marker.txt` `MARKER_ESCAPED\n`). Both files outside the intended tree landed in the snapshot; the digest includes them. |
| S3 | MEDIUM — snapshot/case copies/`sandbox.log` have no aggregate disk bound (`oracle.py:69-88` per-file 1 MiB only; `oracle.py:162-163` uncapped log redirect) | **confirmed** (code) | No total byte/count cap anywhere in `snapshot()`; `sandbox.log` opened `wb` with compositor stdout+stderr piped to it, uncapped. Lines re-verified. Not exercised dynamically (deliberately would consume /fast). |
| S4 | LOW — interruption leaves `/fast` and `/tmp` artifacts (`mkdtemp` at `oracle.py:144` precedes the `try/finally` at `:167-228`; `Slot.__enter__` `oracle.py:110-121` waits unbounded in between) | **confirmed** (dynamic, persistent) | The exact 4 empty orphan dirs IsolationProbe named at 05:51Z — `/tmp/m26o-{3mmzf4ft,d4wi4n_z,hez8e_lb,w3i84tdo}` — still exist hours later, still empty, unowned. 13 `m26o-*` dirs total before my pilot (9 non-empty = live peer oracles), 7 after; the 4 orphans untouched by anyone. |
| S5 | LOW — `Slot.__enter__` opens `slot-N.lock` mode `"w"` (`oracle.py:114`): follows planted symlinks, truncates, locks the opened inode not the path | **confirmed** (code) | Line re-verified; slot dir is `drwxr-xr-x vgpnk:vgpnk`, so exploitation needs same-UID control. NOT exercised: the live slot dir is shared with running peer counters; probing the race there would risk truncating a peer's lock. Conditional same-UID finding stands. |
| S6 | LOW — pilot's `live_instances()` does a read-only `hyprctl instances -j` against the live compositor (`pilot.py:17-22`) | **confirmed** (code + my run) | My run's `live_instances=1` lines show the live read succeeds. Fixed `instances` argv, no dispatch/keyword/reload path exists in the file; allowed by the stated method. |
| K1LK | K1LabelKeyed: **`/proc/1/environ` of the tool sandbox's bwrap exposes the launching environment** | **confirmed** (dynamic, independently reproduced) | `probe_tool.py` inside `run_tool`'s sandbox read `/proc/1/environ`: **262 distinct keys** = the launcher's full environment, including my injected canary `MADO_REVIEWISOLATION_CANARY` (key present → proven launch-path leak), plus credential/socket names `OPENAI_CODEX_TOKEN`, `XAI_OAUTH_TOKEN`, `HL_INITIAL_WORKSPACE_TOKEN`, `SSH_AUTH_SOCK`, `SSH_ASKPASS`, `DBUS_SESSION_BUS_ADDRESS`, `DISPLAY` (names only reported; values unread/unprinted). `/proc/self/environ` was correctly cleared to 3 keys (`HOME PATH PWD`) — `--clearenv` (`oracle.py:235`) applies to the exec'd child (PID 2), while PID 1 is bwrap itself (`/proc/1/cmdline` = `bwrap --ro-bind /usr /usr --symlink …`), retaining the launcher env. `pid_count=2` → pid-ns isolation intact otherwise. Same structure in `oracle()`'s sandbox (`oracle.py:147,155` `--unshare-all … --clearenv` + `--proc`), so the nested compositor's sandbox exposes the launcher's env to in-sandbox processes identically. The tool's only output channel is captured stdout → tool env values *could* reach counter receipts. |
| F1 | IsolationProbe F1 — live session untouched | **confirmed** (my re-run) | Live instances 1→1, same signature; pilot's nested view shows `run_user:false`, `card_nodes:[]`, `netns_same:false`; peers' nested pids show only `XDG_RUNTIME_DIR=/tmp/m26o-*`, never `/run/user/1000`. |
| F2 | F2 — every nested compositor headless/sandbox-private | **confirmed** | Pilot's nested process (pid 1885817): `WAYLAND_DISPLAY=wayland-0`, `XDG_RUNTIME_DIR=/tmp/m26o-af8a2g23`, only `renderD129`, no `/run/user`, unshared netns. Consistent with w1's 770/770 sampling. |
| F3 | F3 — no crash residue | **confirmed** | 1335→1335 both pilot-internal and my own `coredumpctl` counts. |
| F4 | F4 — `PILOT` token host-global → false negative under fleet load | **confirmed** (reproduced) | `PILOT NOT_OK`, `exit=1` solely from `leftover private runtime dirs: 8; nested processes alive: 3` (`pilot.py:78-82`) while every isolation clause of the same predicate passed. |
| F5 | F5 — oracle leaks empty `/tmp/m26o-*` dirs when caller dies mid-flight | **confirmed** | Same 4 orphans persist; mechanism (`mkdtemp` `oracle.py:144` before slot-wait + `try`) re-verified at `:161-228`. |
| F6 | F6 — attribution caveat (nested pids are host-wide under concurrency) | **confirmed** | Peer nested processes alive during and after my pilot; my own pid gone. |

## Verdict

`HOST_SAFETY concern`

The primary invariant holds and is re-confirmed: **no live-session contact, no coredump growth (1335→1335),
no host runtime-dir or DRM-card exposure, private netns/env, clean process-group teardown** — the
`PILOT NOT_OK` token is the known host-global-clause false negative, not a breach. The concern rating is
for the **independently re-confirmed `/proc/1/environ` credential/environment leak into both sandboxes**
(K1LK): a tool under test can read the full launcher environment (session tokens, SSH/DBus sockets names)
through PID 1's environ despite `--clearenv`; remediation is a harness-side `--clearenv`-equivalent applied
to the bwrap process itself or a scrubbed launch env. Secondary, lower-severity confirmations: symlinked-root
snapshot escape (S2, dynamically reproduced), unbounded tool resources (S1), unbounded snapshot/log disk
(S3), and the accumulated `/tmp/m26o-*` orphans (S4/F5 — 4 still present, inode hygiene only).

## Residual risk and gaps

- All four "dynamic" findings that would cost host resources (S1 core/memory, S3 disk fill) or touch shared
  state (S5 slot race) were confirmed at code level only — exercising them is itself the harm.
- The `/proc/1/environ` leak was demonstrated via `run_tool`'s sandbox; the oracle sandbox shares the same
  `bwrap … --unshare-all --clearenv --proc /proc` shape (`oracle.py:146-160`) but I did not re-demonstrate
  inside the compositor sandbox — the mechanism is identical and independent of the process run.
- During my window other w2 seats ran counters; `/tmp/m26o-*` counts and the pilot's leftover count are
  host-wide values, not mine alone (strengthens isolation findings; attribution caveat stands).
- 4 pre-existing orphan dirs were left in place — not mine, and an empty dir can be a peer's pre-socket
  window.

## Evidence

| artifact | path | sha256 | lines |
|---|---|---|---|
| pilot re-run, verbatim | `/fast/scratch/hyaku/mado-r26/review-isolation/pilot-run-w2.txt` | `0654bcf9418cae0465249071604e1292f2cf62dfa336318691759d31b19cc30b` | 8 |
| tool-sandbox environ probe output | `/fast/scratch/hyaku/mado-r26/review-isolation/probe-environ.txt` | `97483cb07facb436fa2386cdcc4a080dac7d92a7dadcde3b2b001e93fb29142e` | — |
| snapshot symlink probe output | `/fast/scratch/hyaku/mado-r26/review-isolation/probe-snapshot.txt` | `26a09857dd362abde940400bb27b3ee448a0fd0232ff3e13b35eff10786d1103` | 4 |
| probe scripts | `/fast/scratch/hyaku/mado-r26/review-isolation/probe_{tool,runner,snapshot}.py` | — | — |

No installs or upgrades. `oracle.py` sha256 at review time `680798ed…e441` (matches registration pin);
`pilot.py` sha256 `e5f43100dce040d9a9842b031434c3a483781d4a9bb5dec8d3c5a8bf343a4b26`.
