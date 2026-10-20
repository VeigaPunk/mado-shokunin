# SentinelGatePath — holds (with one out-of-scope prepend, one detection gap, and one host-pause incident caused by this seat)

Surface: PATH hygiene of `tools/mado-verify.sh --selftest` at 01b80946d92b26370d3012a7da655d00dd135154.
The bytes are identical: `sha256sum` of `git show 01b8094:tools/mado-verify.sh` equals the worktree file,
`1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af`, 4097 lines. HEAD = 01b80946….

## Verdict per claim

| Claim | Result | Evidence |
|---|---|---|
| Every WL* scenario runs its stubs under a replaced PATH | **holds** | `:1261`, `:1275`, `:1285` set `PATH="$WLB"` or `PATH="$WLB2"` in-process, then restore `PATH="$wl_path"` (`:1236`). |
| Every OM* scenario (OM1–OM16, including OM10A/B and OM11–OM16) runs under a replaced PATH | **holds** | 17 `env PATH="$OMB"` / `"$OMB2"` prefixes at `:736 765 787 799 816 827 834 844 858 878 891 908 937 948 960 973 991`. None prepends. |
| No real walker, systemctl, hyprctl or git is exec'd by `--selftest` | **holds (observed)** | Traced run below: zero execve of `/usr/bin/walker`, `/usr/bin/systemctl`, `/usr/bin/hyprctl`, `/usr/bin/git`, or the real `omarchy`. Tripwire log is empty. |
| "PATH is REPLACED, never prepended" (`:1231-1234`) | **holds as scoped (WL)**. The file as a whole has **one prepend** (F-1). | `:1337` |

## Attack 1 — static census of every PATH prefix (committed bytes)

`grep -nE 'PATH=|\$PATH' /tmp/sgp-verify.sh` (the git-show copy):

- Replaced, 24 sites: the 17 OM sites above, C `:1197` `PATH="$SANDBOX"`, E `:1220` `PATH="$SANDBOX_NPY"`, F `:1303` `PATH="$SANDBOX_NOSHA"`, S6 `:1701` `PATH="$SANDBOX"`, and WL `:1261/:1275/:1285`.
- **Prepended, 1 site:** scenario I, `:1337`: `out=$(env PATH="$MID:$PATH" "$BASH_BIN" "$0" --root "$A" --no-live 2>&1)`.
- Host-PATH children with no prefix at all: T1–T9 (`:1018-1137`), A/B (`:1146`, `:1178`), H (`:1317`), N1–N16 (`:1358-1627`), S1/S2/S7 (`:1646`, `:1662`, `:1710`), and the D, R12, R13, S3–S10 usage, help and diff calls. Every one of them either carries `--no-live` or runs a mode with no planes (`--help`, `--snapshot-diff`, refused usage, or `--regression` with `MADO_VERIFY_HARNESS=$T/no-harness`). `grep` of `"$BASH_BIN" "$0"` lines with no PATH or mode guard returned only the OM continuation lines, whose `env PATH=` sits on the line before.
- Why those children stay off the host: `LIVE_REQ="${MADO_VERIFY_LIVE:-auto}"` (`:107`). `--no-live` sets it to `no` *after* the env read (`:4029`). `auto` only goes live when `ROOT = HOME` (`:4047`), and every fixture root is under `/tmp/w5-mado-m52-*`. An inherited `MADO_VERIFY_LIVE=yes` in the caller's env cannot flip them live.
- The git probe in the omarchy plane sits inside the live arm (`:3686-3690`; comment at `:3685`: "a file-plane run spawns no git").
- `live_plane` returns before `walker_live_rows` when hyprctl is absent or unreachable (`:3317-3329`, `return` at `:3328`). So the OM and C/S6 live runs, whose PATHs have no hyprctl, never reach the walker or systemctl calls (`:3556`).

## Attack 2 — run `--selftest` under `strace -f -e trace=execve`, with tripwires

strace 7.2 is at `/usr/bin/strace` (already installed). Caller env had `HYPRLAND_INSTANCE_SIGNATURE` and `WAYLAND_DISPLAY` set, so a leak would have reached the real compositor. To make a leak observable without executing host surfaces, the run went inside a private user+mount namespace: `unshare --map-root-user --mount --propagation private /tmp/sgp/inns.sh`, with a nested `unshare --user --map-user=1000 --map-group=1000`, so the payload runs as uid/gid 1000. That namespace bind-mounts a logging stub (`/tmp/sgp/tripwire.sh`, sha256 `7eb7f4ef…`; it appends argv to `/tmp/sgp/tripwire.log` and exits 127) over 16 paths: `/usr/bin/{hyprctl,walker,systemctl,waybar,busctl,elephant,notify-send,journalctl,loginctl,uwsm,makoctl,swayosd-client,pacman,sudo}`, `~/.local/share/omarchy/bin/omarchy` and `~/.local/bin/jj`. Before running anything it checks each mount with `cmp` and refuses the payload on any failure (`inns.sh` sha256 `59b23493…`). Real `/usr/bin/git` was left in place but traced.

```
unshare --map-root-user --mount --propagation private /tmp/sgp/inns.sh \
  strace -f -qq -s 300 -e trace=execve -e signal=none -o /tmp/sgp/strace-main.log \
  /bin/bash /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh --selftest
rc=0   2026-10-20T18:05:54Z → 18:06:31Z
MADO_SELFTEST: 443/443 assertions passed
strace-main.log 13240 lines, 11492 execve, sha256 05c5764b…  ; tripwire.log 0 lines
```

Every execve target that hit a watched name, outer suite (`wSceGn`) plus nested scenario-F suite (`1zonho`):

```
 69/55 …/omarchy/bin/git            5/4  …/omarchy/bin-no-omarchy/git
 45/30 …/omarchy/bin/omarchy
  2/2  …/walker/bin/walker          4/4  …/walker/bin/systemctl     2/2 …/walker/bin-no-walker/systemctl
```

`grep -oE 'execve\("(/usr/bin|/home/vgpnk/…)/(walker|systemctl|hyprctl|git|omarchy|waybar|busctl|elephant|jj|pacman|sudo|…)"'` for host paths returned **nothing**. Every non-/tmp execve target is coreutils, python3, bash or env (full list: awk bash cat chmod cp cut date dirname env find grep head ln mkdir mktemp python3 readlink rm sed sha256sum sort tr wc xargs tail). The only host-PATH walk is `xargs sha256sum` from the `find | xargs sha256sum` fixture hashes (`:1145/:1147/:1645`). It probes each host PATH dir for `sha256sum` four times.

**Detection-power controls.** These are mutated copies under `/tmp/sgp/m*/`, run with `--selftest` only, under the same tripwire+strace harness, with `MADO_SELFTEST_NESTED=1`:

| Mutant | Host surface reached (tripwire log) | Selftest result |
|---|---|---|
| mA: WL3 `PATH="$WLB2:$wl_path"` (`:1285`) | `/usr/bin/walker --version` | FAILED 439/441: R10 + **WL3 "the FAIL names the missing binary"** |
| mB: OM4 `env PATH="$OMB2:$PATH"` (`:799`) | real `omarchy version`, `omarchy theme current`, `omarchy commands --json --all`, `/usr/bin/hyprctl version` | FAILED 440/441: **only R10** |
| mC: OM1 `env PATH="$OMB:$PATH"` (`:736`) | `/usr/bin/hyprctl version` | FAILED 440/441: **only R10** |

So the harness detects leaks. It also shows the gap in F-2.

## Findings

**F-1 (info/low) — scenario I prepends the host PATH.** `:1337` `env PATH="$MID:$PATH" … --no-live`.
- **Exploit path:** none at this tip. Two independent guards keep LIVE=0: `--no-live`, and a non-home `--root "$A"`. The stub dir holds only `sha256sum`, and the trace shows no host-surface exec.
- **Impact:** latent. If a future file-plane row spawns walker, git, omarchy or systemctl, the run falls through to the host binary.
- **Smallest remediation:** build `$MID` from the same coreutils symlink loop as `$SANDBOX` (`:1193-1196`) plus the counting `sha256sum`, then use `env PATH="$MID"`. `REAL_SHA` is already absolute (`:1326`).

**F-2 (medium, latent) — no assertion pins hermeticity. A PATH-prepend regression in an OM scenario reaches the host and passes every behavioural assertion.**
- **Evidence:** in mB and mC above, the only red was R10, the derived-target sha pin (`R10: derived target equals the recorded gate revision`). R10 trips on *any* edit to the gate and is re-recorded whenever the gate changes legitimately, so it does not guard PATH.
- **Real-host case [INFERENCE]:** without tripwires, `hyprctl version` would succeed with `HYPRLAND_INSTANCE_SIGNATURE` set, and the whole live plane would run against the operator's session. That covers hyprctl getoption/binds/monitors/layers, `waybar --version`, `pgrep`, `busctl --user`, `walker --version`, `systemctl --user is-active` and `omarchy theme current`. The OM1 rows would still come from the stubs earlier in PATH. This was not executed, by design.
- **Contrast:** WL3 does catch its own prepend, because the absent-binary arm asserts `not on PATH`.
- **Smallest remediation:** add one assertion per stub sandbox that the stub dirs contain no `hyprctl` and that the OM1 output carries `live.plane UNKNOWN "hyprctl not on PATH"`. That pins the absent-hyprctl arm the way WL3 pins absent-walker. Alternatively, make R-scenarios grep the gate for `PATH="[^"]*:\$PATH"` and refuse.

**F-3 (info) — `$OMB` has no `timeout`** (symlink loop at `:728-731`, unlike `$WLB` `:1252`). `tmo` therefore runs the OM stubs with no 5 s bound. This is not a host-reach issue, only robustness.

## Incident — this seat executed the real `/usr/bin/hyprctl` once (host-pause breach)

- **What happened:** the first tripwire attempt used `unshare --user --map-current-user --mount`. util-linux `mount` refused ("must be superuser to use mount") for all 16 paths. The script's `[ -e ] && mount && echo` chain does not trip `set -e`, so the smoke command `/usr/bin/hyprctl probe` ran against the real binary. Output was `unknown request`, rc=0, shortly before 2026-10-20T18:05Z.
- **Impact [INFERENCE]:** an unrecognised request to the compositor socket. It is not a read verb or a dispatch, and no state changed. It is still a forbidden hyprctl invocation under the host pause, and it is reported as such.
- **Fix applied before any further run:** `inns.sh` now exits 99 or 98 unless every bind mount succeeds and `cmp` confirms the tripwire bytes. Every later run printed `armed …` for all 16 paths. The selftest run and the three mutant runs logged their only hyprctl contact to the tripwire.

## Limits
- The runs went inside a user namespace, so `/usr/bin` files appeared owned by the overflow uid. The fixtures live under `/tmp` and were owned by the mapped uid 1000, and the suite passed 443/443, as the lane reports.
- [UNK] Untested: environment-borne bypasses other than PATH, such as exported `BASH_FUNC_hyprctl%%` functions or `BASH_ENV` in the caller's env. `command -v` would honour an exported function.
- Tripwires covered the 16 listed paths. Other host binaries were only traced, not intercepted; the trace shows nothing outside coreutils, python3, bash and env.
- The mutant controls ran with `MADO_SELFTEST_NESTED=1`, which skips scenario F, and from a `/tmp` path, which is why R10 fired.
- No fetches. Scratch: `/tmp/sgp/*` and `/tmp/sgp-verify.sh`. The `--selftest` fixtures it created are under `/tmp/w5-mado-m52-selftest.*`.

## Installs
none (strace 7.2 and util-linux unshare were already present; pacman paused).
