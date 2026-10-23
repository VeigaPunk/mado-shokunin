# IsolationProbe — host-safety re-check of the isolated Hyprland oracle (mado round 26, w1)

## What I did

Independently re-checked the round-26 host-safety method, not the registration's summary of it: read
`harness/pilot.py` and `harness/oracle.py` at the lane tip, ran `harness/pilot.py` under `timeout 120`
(verbatim, twice), and ran one frozen C1 counter (`c1/count.py 05319e0f --jobs 6`) while a host sampler read
state every 0.5 s for the whole counter window. The live compositor was queried with read verbs only
(`clients`, `monitors`, `version`, `instances`); the sampler and every process I started had
`WAYLAND_DISPLAY` and `HYPRLAND_INSTANCE_SIGNATURE` removed from the environment, and live reads selected the
instance with `hyprctl -i <signature>` under `env {PATH, XDG_RUNTIME_DIR=/run/user/1000}`. No lane source,
tool, counter or harness file was edited. No tool was installed or upgraded.

The question this answers: round 25's oracle ran nested Hyprlands on the live session (windows on the desktop,
~1330 SIGABRT `coredumpctl` records). Did the new method, on this host, at the measured concurrency, ever touch
the live session or leave a nested compositor that could?

## Method as read (line anchors, lane tip 05319e0f)

| fact | source |
|---|---|
| nested Hyprland = tinywl (wlroots headless) parent + Hyprland child, one bwrap sandbox | `harness/oracle.py:147-160` |
| `--unshare-all` (own net/pid/ipc/uts), `--clearenv` | `harness/oracle.py:147,154` |
| `--tmpfs /run` (no host runtime dir, D-Bus, logind socket) | `harness/oracle.py:152` |
| private XDG_RUNTIME_DIR `mkdtemp(prefix="m26o-", dir="/tmp")`, mode 0700 | `harness/oracle.py:144-145` |
| only `/dev/dri/renderD129` (amdgpu render node); no card node, no input | `harness/oracle.py:150`, `RENDER_NODE` |
| `prlimit --core=0 --as=8000000000` inside the sandbox | `harness/oracle.py:146` |
| `WLR_BACKENDS=headless`, `LIBSEAT_BACKEND=noop`, Hyprland sd/crash-reporter off | `harness/oracle.py:155-159` |
| coredump count = lines containing `/usr/bin/Hyprland` from `coredumpctl list` | `harness/oracle.py:60-62` |
| pilot's nested-pid scan matches *any* `/usr/bin/Hyprland` with `XDG_RUNTIME_DIR=/tmp/m26o-` (host-global) | `harness/pilot.py:25-37` |
| pilot's leftover check counts *every* `/tmp/m26o-*` dir (host-global); `ok` requires it empty | `harness/pilot.py:78-82` |

## Exact commands

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 120 \
  python3 .ufo/waves/round-26/harness/pilot.py 2>&1 | tee .ufo/waves/round-26/evidence/isolation-probe-pilot.txt

env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout -k 10 900 python3 -I \
  /fast/scratch/hyaku/mado-r26/isolation_probe.py 2>&1 | tee .ufo/waves/round-26/evidence/isolation-probe.txt
# inside that sampler, the assigned command, cwd = lane, no outer --as (oracle.py:146 sets its own):
#   timeout 900 python3 -I .ufo/waves/round-26/c1/count.py 05319e0f --jobs 6

env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 180 python3 -I \
  /fast/scratch/hyaku/mado-r26/pilot_audit.py 2>&1 | tee .ufo/waves/round-26/evidence/isolation-probe-pilot2.txt
# live reads (read verbs, never dispatch/keyword/reload):
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE XDG_RUNTIME_DIR=/run/user/1000 \
  timeout 10 hyprctl -i efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 clients -j
# ... monitors -j, version -j, instances -j similarly
timeout 120 coredumpctl list --no-pager --no-legend   # count lines containing /usr/bin/Hyprland
```

## Pilot receipts (verbatim)

Run 1 as assigned (`isolation-probe-pilot.txt`):

```
before: hyprland_coredumps=1335 live_instances=1
nested process (host view): {"card_nodes": [], "env": ["WAYLAND_DISPLAY=wayland-0", "XDG_RUNTIME_DIR=/tmp/m26o-rz622fq8"], "netns_same": false, "pid": "837883", "render_mounts": ["/dev/dri/renderD129"], "run_user": false}
oracle answered: binds=192 animation_nodes=35 beziers=6
after: hyprland_coredumps=1335 live_instances=1 delta_coredumps=0
leftover private runtime dirs: 6; nested processes alive: 0
PILOT NOT_OK
exit=1
```

Run 3 with the run-scoped audit (`isolation-probe-pilot2.txt`); run 2 was a first version of the audit script
that crashed on an ENOENT race over a transient `/tmp/m26o-*` entry (my script, not the harness) and was
discarded; its pilot half showed the same two failing clauses:

```
before: hyprland_coredumps=1335 live_instances=1
nested process (host view): {"card_nodes": [], "env": ["WAYLAND_DISPLAY=wayland-0", "XDG_RUNTIME_DIR=/tmp/m26o-b4wuhddc"], "netns_same": false, "pid": "1245394", "render_mounts": ["/dev/dri/renderD129"], "run_user": false}
oracle answered: binds=192 animation_nodes=35 beziers=6
after: hyprland_coredumps=1335 live_instances=1 delta_coredumps=0
leftover private runtime dirs: 4; nested processes alive: 0
PILOT NOT_OK
exit=1
--- audit (run-scoped) ---
pilot_rc=1 wall=4.84s
before m26o_dirs=4 nested_procs=[]
after  m26o_dirs=8 nested_procs=[1248550, 1248556, 1248564, 1248566]
pilot_own_xdg=["/tmp/m26o-b4wuhddc"] own_dirs_present_after=[]
dirs_present_before_and_after=4 (not pilot's, pre-existing) ["m26o-3mmzf4ft", "m26o-d4wi4n_z", "m26o-hez8e_lb", "m26o-w3i84tdo"]
new_dirs_still_present=4 empty_ones=[]
preexisting_empty_orphans=4 ["m26o-3mmzf4ft", "m26o-d4wi4n_z", "m26o-hez8e_lb", "m26o-w3i84tdo"]
```

The 4 dirs counted by the pilot were created 05:51:21–22 (before the pilot's own 4.84 s window), are empty,
mode 0700, and have no owning process; the pilot's own private dir was removed. `PILOT NOT_OK` therefore comes
only from `not leftovers` (`pilot.py:78,82`); every isolation clause of the same predicate
(`res is not None`, `c1 == c0`, `run_user` false, `card_nodes` empty, `netns_same` false) passed.

## Sampling result (81 samples, 0.5 s cycle, 45.4 s window, counter `--jobs 6`)

| invariant | measurement over the counter window |
|---|---|
| live clients (`hyprctl -i <sig> clients -j`) | **2 in 81/81** samples; address digest `5b3440a8a5a4` unchanged 81/81 |
| live monitors (`hyprctl -i <sig> monitors -j`) | **1 in 81/81** samples |
| live Hyprland process | pid **1614**, present in every sample and never classified nested |
| `/usr/bin/Hyprland` processes | 7–13 total; nested (`XDG_RUNTIME_DIR=/tmp/m26o-*`) **max 12** = oracle slot cap |
| nested instances observed | **288 distinct host pids**, 770 per-tick detail observations |
| nested `WAYLAND_DISPLAY` | `wayland-0` **770/770** (private tinywl display) |
| nested `XDG_RUNTIME_DIR` | `/tmp/m26o-*` **770/770** (never `/run/user/1000`) |
| nested `/proc/<pid>/root/run/user` | **absent 770/770** |
| nested `/dev/dri/card*` mount | **absent 770/770**; only `renderD129` |
| nested net namespace | `net:[4026533921]` vs host `net:[4026531833]` (unshared) |
| coredumpctl `/usr/bin/Hyprland` | **1335 → 1335, delta 0** (counter receipt prints the same) |
| live `hyprctl instances -j` | **1 → 1** (both pilots) |

Nested env of a sampled instance contained exactly `HOME PATH PWD SHLVL WAYLAND_DISPLAY XDG_RUNTIME_DIR
WLR_BACKENDS=headless WLR_HEADLESS_OUTPUTS=1 WLR_RENDERER=gles2 WLR_RENDER_DRM_DEVICE
HYPRLAND_NO_CRASHREPORTER HYPRLAND_NO_SD_NOTIFY HYPRLAND_NO_SD_VARS LIBSEAT_BACKEND=noop` — no `DISPLAY`, no
`DBUS_SESSION_BUS_ADDRESS`, no `HYPRLAND_INSTANCE_SIGNATURE`. Private runtime dir contents were `wayland-0` +
`wayland-0.lock` (tinywl) and, once Hyprland was up, `wayland-1` + `wayland-1.lock` (Hyprland's own socket).

Counter side observation (not an isolation result): `counter sha256:f98e264b…352cd`, `oracle.py
sha256:680798ed…e441` (pins match registration), seed `469d907e676d11c1`, `tool=MISSING_TOOL at 05319e0f`,
`cases_pass=0/41 TARGET_MISSED`, `exit=1`, `HOST_SAFETY … delta=0`.

## Findings

F1 — The live session was not touched. Clients and monitors were byte-identical in count and client-address
digest for the full window, including 12 concurrent nested instances; no window ever appeared. The round-25
failure mode (windows on the operator desktop) is not reproducible through `harness/oracle.py`.

F2 — Every nested compositor was headless and sandbox-private: private tinywl display, private runtime dir, no
host `/run`, no DRM card node, no input device, unshared network namespace, cleared environment, only the
amdgpu render node. 770/770 observations of 288 distinct pids agree.

F3 — No crash residue: coredumps stayed 1335 throughout the pilot runs and the counter run, and the counter's
own receipt reports delta 0. Nested Hyprlands exit via `dispatch exit` (clean) and the sandbox group is killed.

F4 — `pilot.py`'s `PILOT` predicate is host-global, not run-scoped, in two clauses: `leftovers` counts every
`/tmp/m26o-*` on the host (`pilot.py:78`) and `nested_pids()` matches any nested Hyprland on the host
(`pilot.py:25-37`). Under the registration's own 12-slot concurrency this makes `PILOT ISOLATED_OK`
unattainable while any other seat runs an oracle: run 1 counted 6 dirs at 05:51:2x, run 2 counted 15 with 6 peer
nests alive, run 3 counted the same 4 pre-existing empty dirs before and after a clean pilot. The token is a
false negative under load, not evidence of a breach.

F5 — The oracle leaks empty `/tmp/m26o-*` dirs when its caller dies while an oracle is in flight: the dir is
created at `oracle.py:144`, but removal happens only in the `finally` at `oracle.py:226`, after `Slot.__enter__`
(`oracle.py:161`) which waits unbounded for one of 12 locks. A counter killed while its threads wait for a slot
leaves a 0700 empty directory with no owner. I found 4 such orphans (05:51:21–22, before my first command's
output file at 05:51:27.8) that survived three pilot runs and several minutes of peers' churn (05:51–05:56). They hold no sockets, no
environment, no user data — `/tmp` inode hygiene and a contamination of the host-global pilot check, not a
live-session exposure. I did not delete them: they are not mine and an empty dir can be a pre-socket window of a
peer's in-flight oracle.

F6 — Attribution caveat: during my window other seats ran C1/C2 counters (`m26c1-*`, `m26c2-*` work dirs; up to
13 Hyprland processes, 12 nested = slot cap). The sampled nested pids are therefore host-wide, not only my
counter's; that strengthens F2 (peer instances are isolated too) but means the per-pid counts are not mine alone.

## Verdict

`ISOLATION ok — live_clients 2→2 (81/81, digest 5b3440a8a5a4 unchanged), live_monitors 1→1, live Hyprland pid 1614 untouched, 288 nested oracle pids all headless+private (WAYLAND_DISPLAY=wayland-0, XDG_RUNTIME_DIR=/tmp/m26o-*, /run/user absent 770/770, /dev/dri/card absent 770/770, netns unshared), coredumpctl /usr/bin/Hyprland 1335→1335 delta 0, live_instances 1→1; 4 empty pre-existing /tmp/m26o-* dirs are residue with no live-session contact; PILOT token NOT_OK is caused only by its host-global leftover/nested-pid clauses.`

## Risks

- If the L1 wants a literal `PILOT ISOLATED_OK` receipt, it cannot be obtained during fleet waves without an
  idle host; either run it on an idle host or rescope `pilot.py:78` and `pilot.py:25-37` to the pilot's own
  `xdg`/pid. That is a harness edit and belongs to the L1, not this seat.
- Empty `/tmp/m26o-*` dirs accumulate without bound when counters are killed mid-flight (4 observed; 19 empty
  at one audit point, some in-flight). Inode/mtime hygiene only; no sockets, no credentials, no host paths.
- The 12-slot lock caps concurrency but `Slot.__enter__` spins forever; a killed waiter leaks its dir (F5).
- My live reads used the `-i` flag with a clean env; no read used or inherited `WAYLAND_DISPLAY` /
  `HYPRLAND_INSTANCE_SIGNATURE`, and no process I started was given them.

## Blockers

None. The assigned pilot was run; its literal token is `NOT_OK` for the global-clause reason above, demonstrated
run-scoped, and every isolation clause of that same predicate passed.

## Evidence (this seat's outputs only)

| artifact | path | sha256 | lines |
|---|---|---|---|
| samples + appendix A/B/C (bounded 186 ≤ 2000) | `.ufo/waves/round-26/evidence/isolation-probe.txt` | `b4f9c9dfc8b25648c5d3bb61f3f700ea9e2dac0bc22bd1aaa23e7e36f72796e3` | 186 |
| pilot run 1 verbatim | `.ufo/waves/round-26/evidence/isolation-probe-pilot.txt` | `454b38410bef1faac66cbf7134478dfde8e0944d4ed271207c7d57b47b84c345` | 8 |
| audited pilot run 3 verbatim | `.ufo/waves/round-26/evidence/isolation-probe-pilot2.txt` | `87aa10ee555cf601ea976195ae4383066fe460a0c24be01066992bde1ee48dc8` | 16 |
| sampler (scratch) | `/fast/scratch/hyaku/mado-r26/isolation_probe.py` | `c977d7d3e13843cdc30c83e98f6ab76a423792ee63c955527c70214f8a2eef84` | — |
| pilot audit (scratch) | `/fast/scratch/hyaku/mado-r26/pilot_audit.py` | `e0a463c3eca2bbe4b79a4ff337ee932dca60862439094f90d4268922567bcf1a` | — |

No lane file other than this report and the evidence artifacts was written. No installs, no git/jj writes, no
harness/counter edits, no live-compositor write verbs.
