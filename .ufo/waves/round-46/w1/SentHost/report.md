# SentHost — host mutation audit, mado round-46 w1

Seat `SentHost` (sentinel). Assignment: item `SentHost` of `.ufo/waves/round-46/w1-spec.json` — "list every host
command a seat is told to run; flag any that could mutate the compositor, input devices or host packages …
and any instruction that contradicts the context's safety rules".
Full findings and evidence: `.ufo/waves/round-46/w1/SentHost.md`; evidence transcript:
`.ufo/waves/round-46/w1/SentHost/checks.txt` (locators `checks.txt:<line>` are computed from that file).

## Verdict

**No instruction in the wave asks for a mutating host action.** Across all 66 items, `hyprctl` followed by
`dispatch`, `keyword`, `reload`, `setprop`, `setcursor`, `switchxkblayout`, `output`, `notify`, `plugin` or
`--batch` never occurs in command position (`checks.txt:46`); `pacman`, `systemctl`, `journalctl`, `udevadm`,
`libinput` and `ss` occur 0 times as a command (`checks.txt:174-179`). The instruments the wave runs against the
host are file reads, five whitelisted compositor reads, a hermetic lane gate, and scratch-clone counters whose
tool runs are bubblewrapped against host *writes* (`checks.txt:111-119`) — reads are not fenced, which is H9.

The residual risk is in **instruction wording**, not in the intended actions: one sentence puts a host secret in
process argv, one asks a seat to commit hardware names, one names a gate whose default mode is outside the
wave's own read whitelist, six compile steps name no output directory while the seat cwd is the fleet root, the counter harness the wave runs does not fence live reads at all (H9), and a v2 re-registration is being
built untracked while eleven items still name the v1 counters and the v2 freeze document is absent (H10).

## Command inventory (host surface, grouped)

| Surface | Items | Verdict |
|---|---|---|
| `hyprctl devices -j` (5 items), `hyprctl monitors all -j` (3), `hyprctl getoption` (1) | ExecLiveHost, ExecW2Monitors, ExecSerialRule, ExecXkbCompile, CritPremise, RevPrivacyRound, ScrSerialCorrection, CritRegistration (implied counts) | allowed by `context:51`; the pinned `devicesRequest` is a formatting routine (`checks.txt:122`); the tools run on these dumps import no `subprocess`/`socket` (`checks.txt:158-160`) |
| `hyprctl clients` (1 item, as a fixture shape) | CritW2Gate | **not whitelisted**; H6 |
| host config-tree reads (`~/.config/hypr/*`, omarchy defaults, 18 `source =` lines) | ExecLiveHost, ExecW2Monitors, CritPremise, CritRegistration, ScoutOmarchyInput, ExecSerialRule | allowed (trees READ-ONLY, `context:53`); every named file exists (`checks.txt:124-129`) |
| host secret read (`serial` out of `monitors all -j`) + `git grep -F "$SERIAL"` | ExecSerialRule, ScrSerialCorrection | **H2** |
| lane gate `bash tools/mado-verify.sh --selftest` | ExecHarmBase | **hermetic as written** (rc 0, 460/460, zero files in redirected `HOME`/cwd, `checks.txt:54-57`); default live mode is out of whitelist → **H3** |
| read-only lane/fleet scripts (counters, `check-axis-scores.py`, `check-index.py`, `check-session-material.py`, `scripts/sources-census.sh validate`) | ExecHarmBase, ExecDataRehearsal, ExecSupersede, ExecSessionTriage, CritW2Gate | allowed: `sources-census.sh` "writes only stdout or `--out`" (`scripts/sources-census.sh:7`); counters' writes stay under `--work` (`checks.txt:117-119`) |
| host compiler + host library `g++ -std=c++23 -lhyprlang` | ExecHyprlangOracle, ExecHyprlangOracleB, ExecStofOracle, LabFloatFormat, LabDupNames, RevengerHyprlang | allowed (toolchain present, `checks.txt:103-109`); **H4** for the unnamed output dir |
| host library via ctypes (`libxkbcommon`) | ExecXkbCompile | allowed — in-process, no Wayland client, no write surface |
| network reads (upstream raw/API) | ScoutRecheck, ScoutFrontier, LabVirtualRules | allowed (no install required) |
| counter runs (bubblewrap per tool run) | 14 items name a counter command, 5 more run the same counters by description | allowed for writes (`--ro-bind / /`, tmpfs over repo/lane/parent, marker-dir bind only, `--unshare-pid --unshare-net`, `checks.txt:111-119`); **read-permeable, clause r unsound → H9** |
| file writes with no named target | ExecLiveHost (input.conf copy), 6 compile items, ExecW2Monitors (`git show` materialization) | **H4, H5** |

## Findings

| id | sev | instruction | exploit path | smallest remediation |
|---|---|---|---|---|
| H1 | Medium | ExecLiveHost: "device names are product names: keep them" | 10 keyboard + 4 pointer product names committed in a seat receipt; two already appear in `.ufo/waves/round-46/receipts/live-devices-host-l1.txt:5` and `:11` (FIDO CCID keyboard, launcher/audio device; locators computed, values not reproduced) | project the dump to counts and per-class verdicts, or make the instruction conditional on `RevPrivacyRound`'s ruling on whether product names are session material |
| H2 | Medium | ExecSerialRule and ScrSerialCorrection: `git grep -l/-c -F "$SERIAL"` | (a) the serial becomes an argv element of `git`; `/proc/<pid>/cmdline` is world-readable `0444` (`checks.txt:100-101`) — "Never echo the value" is satisfied while the value is still written, contradicting `context:54-55`; (b) an empty extraction makes `git grep -F ""` match every tracked file with rc 0 (`checks.txt:92-94`), turning the D2 count into false evidence | `[ -n "$SERIAL" ] && printf '%s\n' "$SERIAL" \| git -C <lane> grep -l -F -f - <rev>` — verified `-f -` works and empty stdin fails closed (`checks.txt:95-97`); same form for the optional `--serial-from-host` mode |
| H3 | Medium | ExecHarmBase: lane-relative gate paths plus `--selftest` | first commands fail from the fleet-root cwd (`checks.txt:170`); the recovery `cd <lane> && bash tools/mado-verify.sh` drops `--selftest` and runs `hyprctl -j instances/:3421`, `configerrors/:3443`, `-j binds/:3499`, `monitors/:3515`, `-j layers/:3595` with `ROOT=$HOME` (`tools/mado-verify.sh:109`) — four verbs outside `context:51-53` | absolute lane path + one sentence: the live mode is out of scope this round |
| H4 | Low-Medium | six `g++` items and ExecW2Monitors give no output dir | `g++` without `-o` writes `a.out` into `/home/vgpnk/Projects/shokunin` (seat cwd); only 6 of 66 items name `/fast/scratch` (`checks.txt:48-51`) | name the per-seat scratch path in those item texts |
| H5 | Low | ExecLiveHost: "a scratch copy of input.conf with `kb_layout = zz`" | one keystroke from writing `~/.config/hypr/input.conf.zz`, which `SKILL.md:314,322` classifies as mutating and `context:53` forbids | say "under `/fast/scratch/hyaku/mado-r46/<Seat>/`; never under `~/.config/hypr`" |
| H6 | Low | CritW2Gate: craft a "`hyprctl clients` plain text" fixture | a seat obtains the shape by running `clients` (not whitelisted; window titles), and `SKILL.md:326` licenses that verb, so the two documents disagree | add "synthesized by hand — never by running `hyprctl clients`" |
| H7 | Low | regime conflict between the context, `SKILL.md` and `PROVINCE.md` | the lane still declares a source-only scope that forbids live reads (`SKILL.md:40-42`, `:339`, `:613`) while nine prompts name a live read (`checks.txt:171`); `SKILL.md:326` and `PROVINCE.md:28` allow a wider read set than the context; `SKILL.md:350,365` mandates `/tmp/<lane>-*` where the operator directive mandates `/fast/scratch` | one line in the wave context naming which document governs for this round (L1) |
| H8 | Low | C1 counter accepts `--work` anywhere outside repo/lane/lane-parent | a mistyped `--work /home/vgpnk` creates and removes `c1r46-*` dirs under `$HOME` (`quality/counters/c1-r46-devices.py:241-243,424-429`); no item passes anything but `/fast/scratch` | none in the frozen data path; refuse `$HOME`/`/tmp` if the counter is ever re-cut |
| H10 | Medium | round-level provenance: untracked `c1-r46-devices-v2.py` (`19d00e66…`), `c1-r46-fixtures-v2.json` (`d31849db…`), `c2-…-v2.py` (`eb6db5c9…`), two `ctl/run-*-v2.py`, and `.ufo/waves/round-46/v2/`; `registration-v2.md` absent although the v2 docstring line 4 asserts it (`checks.txt:194-223`) | a seat scores the superseded v1 predicate as written, or cites a v2 number with no freeze, no controls and no registration behind it; 11 items name v1, 0 name v2 | before any v2 number is quoted: L1 writes `registration-v2.md` + v2 control receipt and issues a wave-level notice naming the v2 files and their sha256 pins; until then the v1 counters are the only citable ones |
| H9 | Medium | C1 harness: fake-bin `PATH` absent from the selftest run (`c1-r46-devices.py:375`), absolute `/usr/bin/hyprctl` unshadowed (`:252`), `hidden_paths` = repo/lane/parent only (`:241-243`) and env B hands out `XDG_RUNTIME_DIR=/run/user/<uid>` (`:269`) | a scored tool runs `/usr/bin/hyprctl` or connects to the live request socket and still prints `readonly=ok`; `SentTool-3` reports executed bypasses reaching TARGET_MET (their F1/F2), I verified the code shape (`checks.txt:181-191`) | ro-bind the four fake binaries over their `/usr/bin` names, give the selftest `env_a`'s PATH, add `~` and `/run/user/<uid>` to `hidden_paths()`; the untracked v2 candidate instead uses an allowlist root `/usr`+`/etc`, `--tmpfs /tmp`, fake bin on the selftest PATH and a pipe-based clause r — unproven until frozen |

Adjacent, outside the host surface: O1 the 48-vs-49 finding count drift between `registration.md` and
`ExecSessionTriage`; O2 `ExecDataRehearsal`'s "`tools/*.py --selftest`" produces three usage errors (three tools
take a directory argument); O3 `ExecHarmBase`'s lane-relative paths (the trigger half of H3).

## What I ran

Read-only: `hyprctl monitors all -j` once (serial **shape only**: 12 chars, mixed class, `checks.txt:132`), file
existence and counts on the config trees, greps over lane scripts and pins, `bash tools/mado-verify.sh --selftest`
with `HOME` and cwd redirected to scratch (`checks.txt:54-57`), and two behaviour probes in scratch (argv
readability with a dummy token; `git grep -f -` and the empty-pattern case). No compositor mutation, no package
action, no input injection, no Wayland client of my own, no write outside this seat dir and the Report file.

Residuals: the round prompt `.ufo/prompts/mado-round-46.md` was not audited (outside the lane, not named to this
seat); H1's policy call belongs to `RevPrivacyRound`; I did not inspect an audit daemon to confirm argv capture.
