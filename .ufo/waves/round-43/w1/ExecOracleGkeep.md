# ExecOracleGkeep — oracle observation: the size Hyprland 0.56.2 reports for the gkeep window

Seat: executor, round 43 wave w1. Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Deliverable: one observation, from a Hyprland 0.56.2 nested in the round-27 bubblewrap oracle,
of a client with application id `org.omarchy.gkeep` under the host's three gkeep rules, read from
`hyprctl clients -j`. Everything below is in `.ufo/waves/round-43/w1/ExecOracleGkeep/`.

## 1. Result (the observation)

**`size` = [420, 500], `floating` = true**, for app_id `org.omarchy.gkeep` under
`fetch/host-gkeep.conf` (float on, center on, `size 420 500`), in a Hyprland v0.56.2
(commit `efb50993780079460b0cbed1363e2166a2de1d9f`, the host binary, read-only, run inside bwrap)
nested under a wlroots 0.20.2 tinywl inside the round-27 bubblewrap layout.

The registration's chain holds: the rule's size is what the compositor reports, not a value the
client asked for.

Evidence:
- the verbatim `clients -j` object: `20-observation.txt` §1 (`"size": [420, 500]`, `"floating": true`,
  `"mapped": true`, `"at": [270, 20]`, `"class": "org.omarchy.gkeep"`); raw arrays in
  `receipts/dump-headlesshost.json` and `receipts/receipt-headlesshost.json`.
- Hyprland's own map line (`receipt-headlesshost.json:sandbox_log_tail`, sandbox.log:1762):
  `Map request dispatched, monitor HEADLESS-2, window pos: [270.00000, 20.00000], window size: [420.00000, 500.00000]`.
  x=270=(960-420)/2, y=20=(540-500)/2 on the 1920x1080@scale-2 monitor: the `center on` rule too.
- what the compositor told the client (client stderr, `receipt-headlesshost.json:client_log`):
  `TOPLEVEL_CONFIGURE w=420 h=500`.
- repeatability: four independent sandboxes (fresh bwrap each time) all report `[420, 500]`
  (`10-cases.txt`; `20-observation.txt` §4).
- the field read is `w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)` — the animation goal, not
  a sampled current value: `25-size-provenance.txt` citing `fetch/Hyprland-HyprCtl.cpp:426-428`
  (the `-j` builder) and `:447-448` (the text builder). The fetched file verifies against
  `receipts/fetch-sha256.txt` (`sha256sum -c`: 10/10 OK).

## 2. Controls (same oracle, same client, one variable changed)

| case | change | `size` | `floating` | reading |
|---|---|---|---|---|
| `nofloat` | `float on` line removed (`rules-nofloat.conf`) | [918, 498] | false | TILED — the size rule is never read for a tiled window |
| `size300` | `size 300 300` (`rules-size300.conf`) | [300, 300] | true | AGREE — the reported size tracks the rule text |
| `nomatch` | same rules, app_id `org.omarchy.gkeep2` | [918, 498] | false | no rule matched → tiled |
| `floatonly` | `size` line removed | [200, 200] | true | the client's own 200x200 buffer — the rule is the origin of 420x500 |
| `minsize` | host rules + client `set_min_size(800,700)` | [420, 500] | true | the rule's size wins over the client's own request |

The client is `/gkeep-shm` (`gkeep-shm.c`): an xdg_toplevel with app_id and title, one 200x200 shm
buffer, no `set_min_size`/`set_max_size`/`set_fullscreen` unless `--min-size` is passed
(`gkeep-shm.c:152-164`).

## 3. Structural finding: the plain round-27 layout cannot map any window

This seat had to add one nested-instance step; without it the size is **unobservable**, and that is
itself a result.

1. In the oracle layout of `.ufo/waves/round-27/harness/oracle.py` (tinywl + nested Hyprland, no
   extra output), the nested Hyprland never keeps a monitor: `monitors -j` is `[]` for a 20 s watch
   (`40-monitor-requirement.txt`, mwatch timeline `[{"names": [], "t": 0.0}]`), and
   `[FallbackStateKeeper] Launch timeout of 2000ms exceeded, entering fallback state.` creates a
   `FALLBACK` output that is disconnected at once (`onDisconnect called for FALLBACK`,
   `Removed monitor FALLBACK!`, aquamarine's `Output WAYLAND-1: initialized` is never turned into a
   monitor).
2. A client mapped in that layout is created and classed
   (`Window 562b1fb8ae20 set class to org.omarchy.gkeep`) but never mapped:
   `mapWindow: no valid monitor/workspace, aborting map for 562b1fb8ae20` — `clients -j` stays `[]`.
3. Repair used for every reported case: `hyprctl -i <sig> output create headless HEADLESS-2` on the
   **nested** instance (1920x1080@60, scale 2) before mapping the client. After that the map
   succeeds. This is a verb on the sandboxed instance only; no host-session socket is touched.
4. A second repair was needed to make the client reach the nested compositor at all: Hyprland
   spawns children with the parent's `WAYLAND_DISPLAY`, i.e. tinywl's `wayland-0`, so the client
   must be started as `WAYLAND_DISPLAY=wayland-1` (the nested Hyprland's socket, visible in the
   private `XDG_RUNTIME_DIR`). Without it the child connects to tinywl and never appears in the
   nested `clients -j` (first attempt, `receipts/receipt-host.json`).

## 4. Comparison with the reference control tool (not the deliverable)

`30-reference-tool.txt`: `python3 -I round-42/c1/ctl-ref-tool.py.txt` selftest 73/73, then on this
seat's observed dumps — host rules `verdict=AGREE size=420x500 want=420x500 float_rule=on`;
`nofloat` `verdict=TILED`; `size300` `AGREE 300x300`; `nomatch` `NO_MATCHING_CLIENT` (exit 3);
`floatonly` `NO_SIZE_RULES` (exit 4); `minsize` `AGREE 420x500`. The tool's verdicts and the
compositor's behaviour agree on every case; nothing here contradicts PRED-C1-r42's contract.

## 5. Build (tinywl from wlroots 0.20.2)

`02-build.txt`: clone tag 0.20.2 at `d783533489e1f75d6886c2ab5c5960090ef268f8`, the round-26
`tinywl-global-versions.patch` applied (compositor 5→6, xdg_shell 3→6), meson 1.12.1 + ninja 1.13.2
+ gcc 16.2.1, 372/372 targets, rc 0. **New shas** (the round-27 pins differ by construction):

- `tinywl` `273151bd088a9389ce07a07afc84fb9c70fc59877005dc43cfcf14b5dfc64af0`
- `libwlroots-0.20.so` `e6dfde744d0727eec764d4d294421cc9704c37e2781214dd45734e63c034364e`

`round-27/harness/oracle.py` was not edited: it still pins `/fast/scratch/hyaku/mado-r26` paths and
the old shas, so `check_build()` would refuse this build. Its bwrap verb set and boot line are copied
verbatim into `oracle-gkeep.py` (plus `--ro-bind` of the client dir, `--tmpfs /dev/shm`, and the
nested `output create`/`dispatch exec` steps).

## 6. Deviations and risks

- Scratch path: the task named `D=/fast/scratch/hyaku/mado-r43-oracle`; the build was done at
  `/fast/scratch/hyaku/mado-r43/oracle` (same shape, one level inside the round-43 scratch root).
  Both are scratch and are deleted at seat end; the build is reproducible from `15-commands.txt`.
- `uv tool install meson` found a **dangling** pre-existing shim (`~/.local/bin/meson` →
  `~/.local/share/uv/tools/meson/bin/meson`, target gone); `uv tool install --force meson`
  (1.12.1) repaired it. Recorded in `01-meson.txt`, `02-build.txt`.
- Host coredumps: Hyprland entries 0 before and 0 after; the raw `coredumpctl list` line count moved
  27 → 26 because one old head entry expired from the journal. The newest entry (04:18:18) predates
  this seat's first run (04:21:28) and the six newest entries are byte-identical before/after —
  see `05-coredumps.txt`. The count is therefore *not* strictly equal; no entry was created by this
  seat, and `prlimit --core=0` plus `HYPRLAND_NO_CRASHREPORTER=1` made a dump impossible.
- The observation is of the **goal** size for a client on an aquamarine **headless** output created
  on the nested instance. The rule application path does not see the output type, and the three
  controls move the reported value exactly as the rules change, but a host-side confirmation is
  still absent (no gkeep window was open on the host — `fetch/host-clients-r43.json` has four tiled
  clients, none of them gkeep).
- The client's own resize behaviour after mapping was not probed beyond the initial configure
  (`TOPLEVEL_CONFIGURE w=0 h=0` second configure, and the tiled control's later 460x500); the
  reported `size` is `GEOMETRIC_GOAL`, so a user resize would be a later state, not this one.

## 7. Tooling used (recorded per operator directive 2026-10-19)

| tool | version | channel | reason |
|---|---|---|---|
| meson | 1.12.1 | `uv tool install --force meson` (existing shim was dangling) | configure/build wlroots 0.20.2 |
| ninja | 1.13.2 | host, already present | build driver |
| gcc | 16.2.1 | host, already present | tinywl + the shm client |
| wayland-scanner | 1.26.0 | host, already present | generate xdg-shell bindings for `gkeep-shm.c` |
| bubblewrap | 0.13.1 | host, already present | the oracle sandbox |

No pacman transaction was run; no host service, config or compositor was mutated.

## 8. Files

```
w1/ExecOracleGkeep/00-toolchain.txt      versions of everything the sandbox needs
w1/ExecOracleGkeep/01-meson.txt          uv meson install
w1/ExecOracleGkeep/02-build.txt          wlroots clone/patch/build, new shas, round-27 pin diff
w1/ExecOracleGkeep/05-coredumps.txt      host coredump before/after
w1/ExecOracleGkeep/10-cases.txt          one line per case: rules, error, size, floating, at, dumps
w1/ExecOracleGkeep/15-commands.txt       every command run (steps' rcs live in receipts/*.json)
w1/ExecOracleGkeep/20-observation.txt    the observation, map line, client configure, repeatability
w1/ExecOracleGkeep/25-size-provenance.txt  GEOMETRIC_GOAL citation from fetch/Hyprland-HyprCtl.cpp
w1/ExecOracleGkeep/30-reference-tool.txt reference tool on this seat's dumps (7 cases + selftest)
w1/ExecOracleGkeep/40-monitor-requirement.txt  the no-monitor negative, with log line numbers
w1/ExecOracleGkeep/gkeep-shm.c           the window under test (source)
w1/ExecOracleGkeep/oracle-gkeep.py       the adapted oracle runner (bwrap + tinywl + Hyprland)
w1/ExecOracleGkeep/build-tinywl-r43.sh   adapted round-26 build script (D repointed)
w1/ExecOracleGkeep/tinywl-global-versions.patch   byte copy of the round-26 patch
w1/ExecOracleGkeep/rules-{host,nofloat,size300,floatonly}.conf  the four rule variants
w1/ExecOracleGkeep/receipts/receipt-*.json   full per-case receipts (commands, rcs, clients, logs)
w1/ExecOracleGkeep/receipts/dump-*.json      clients/monitors/client-log per case
```

## 9. For the L1

- The observation supports the registration's C2 chain end to end and does not contradict C1's
  contract (`mado-geometry.py` would print `verdict=AGREE` on this dump).
- If a row is wanted, S300+ is free: *the round-27 oracle layout yields a monitor-less nested
  Hyprland (windows cannot map), so any `clients -j` observation needs an output created on the
  nested instance* — this is new, measured, and would otherwise be rediscovered by every later seat.
