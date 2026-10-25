# ScoutPkgRefuse — round 37 wave 1 scout report

Task: try to falsify the refusal of package r28 (session log) and r29 (unit journal) "never
overflowed" readings, by finding any host channel where a core-logger line appears after config
load despite `debug:disable_logs` = 1, and look for a record of that option's value in earlier
sessions.

**Bottom line: both refusals SURVIVE.** No channel on this host carries a core-logger line after
config load. One refinement for r29: the journal is gated twice, so the registration's flip
condition is too weak for that channel (finding F1). One trap: a startup line that looks like a
record of `disable_logs` is unconditional and proves nothing (finding F2).

All commands were read-only. Scratch: `/dev/shm/mado37-ScoutPkgRefuse/` (rolling-log capture,
journal dumps, shallow Hyprland source clone). I only report counts and digests. No line from a
journal or a window title is reproduced; any log wording below is paraphrased.

## Source binding (ties my source reads to the frozen receipts)

`git clone -q --depth 1 --branch v0.56.2 https://github.com/hyprwm/Hyprland.git hl` into
scratch → `git -C hl rev-parse HEAD` = `efb50993780079460b0cbed1363e2166a2de1d9f`, which equals the
running build (`hyprctl version`: "Hyprland 0.56.2 … at commit efb50993…"). Digests:

```
d04e3a2f…6b868  hl/src/debug/log/Logger.cpp        == fetch/S214.bin (d04e3a2f…6b868)
eea605df…9540d  hl/src/managers/EventManager.cpp   == fetch/S189.bin (eea605df…9540d)
a8ada2f9…3d583  hl/src/debug/crash/CrashReporter.cpp
9db68cf4…5b62b  hl/src/config/legacy/ConfigManager.cpp
a76f0507…97754  hl/src/config/values/ConfigValues.cpp
```

The last three files are not in any receipt yet. They support F1, F2 and the crash-report check.

## Per-channel verdicts

| # | Channel | Core lines after config load | Verdict |
|---|---|---|---|
| 1 | `hyprctl rollinglog` | 0 of 26 | refusal SURVIVED |
| 2 | Crash reports | none exist; would carry 0 anyway | SURVIVED |
| 3 | Coredumps | none | SURVIVED |
| 4 | uwsm unit stdout/stderr (journal) | 0 (both sessions) | SURVIVED, refined (F1) |
| 5 | Whole user and system journal, per boot | 0 markers | SURVIVED |
| 6 | Session log (positive check) | 0 | SURVIVED, strengthened |

### 1. Rolling log — SURVIVED
- `hyprctl rollinglog > rolling.txt` → rc=0, 26 lines, sha256 `1a0fac91…30ff90`.
- Line-origin counts: `26 DEBUG from aquamarine ]`, and **0** core lines (`LEVEL ]` with no "from").
  Marker counts: "overflowed event queue" 0, "failed writing event" 0, "Socket2 fd" 0.
- Why: the early return at `Logger.cpp:15-16` (`if (!m_logsEnabled) return;`) comes before the
  rolling-follow at `:21-22` and before `m_logger.log` at `:24`, which feeds the rolling buffer.
  Aquamarine lines bypass that return because aquamarine writes through its own
  `CLoggerConnection` on `Log::logger->hu()` (`Compositor.cpp:304-307`). That is why only
  aquamarine lines survive in the file, the rolling buffer and the journal.

### 2. Crash reports — SURVIVED
- `ls ~/.cache/hyprland` → "No such file or directory". `~/.local/share/hyprland` holds only
  `lastNag` and `lastVersion` (content `0.56.0`). There is no `~/.local/state/hyprland`.
  `XDG_CACHE_HOME=/home/vgpnk/.cache`.
- Strings in `/usr/bin/Hyprland` confirm the report path (`/.cache/hyprland`, `/hyprlandCrashReport`).
  `CrashReporter.cpp:66-72` and `:80-81` build it the same way.
- Even if a crash had happened, the report's "Log tail" is `Log::logger->rolling()`
  (`CrashReporter.cpp:248-250`). That is the same buffer as channel 1, gated by the same return.
  The crash reporter writes core text directly only for its header, the system info and the
  backtrace. So a crash report could never carry the socket2 markers on this host.
- In the user journal for boots -1 and 0, the crash-notice text ("Hyprland has crashed" or
  `hyprlandCrashReport`) appears **0** times.

### 3. Coredumps — SURVIVED
- `coredumpctl list hyprland --no-pager` → "No coredumps found."
- In `coredumpctl list` output, hypr appears 0 times. `journalctl -t systemd-coredump` mentions
  hyprland 0 times. `/var/lib/systemd/coredump` has 0 hypr entries.

### 4. uwsm unit stdout/stderr — SURVIVED, refined (finding F1)
- `systemctl --user cat wayland-wm@hyprland.desktop.service`: `Type=notify`; the drop-in
  `ExecStart=/usr/bin/uwsm aux exec -- %I /usr/bin/start-hyprland`. There is no
  `StandardOutput`/`StandardError` override, so output goes to the journal by default.
- `journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat` (all boots):
  717 lines, sha256 `43bf1f07…af63d4`, **42** core-shaped lines (all `DEBUG ]`).
  - Core lines sit at 41–61 and 401–421. Config loads ("Using config") are at 52, 58, 412 and 418.
    Each session's core output stops 3 lines after its second config load. This is the same
    pattern S213 found in the session log.
  - Marker counts: overflow 0, write_fail 0, "Socket2 fd" 0.
- Per boot (`-b N`):

  | Boot | Unit lines | Core lines | Config loads |
  |---|---|---|---|
  | -3 | 0 | 0 | 0 |
  | -2 | 6 | 0 | 0 |
  | -1 | 360 | 21 | 2 |
  | 0 | 351 | 21 | 2 |

- **F1: the journal is gated twice.** `Logger.cpp:47` reads
  `m_logger.setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT);`. The default for
  `debug:enable_stdout_logs` is false (`ConfigValues.cpp:632`), and live
  `hyprctl getoption debug:enable_stdout_logs -j` → `{"option":"debug:enable_stdout_logs","int":0,"set":false}`.
  `ConfigManager.cpp:1046-1050` prints the "Disabling stdout logs (debug.enable_stdout_logs = 0)"
  line, and I counted it in both sessions' unit journal.
  - So the r29 refusal holds even more strongly. However, the registration's flip at
    `registration.md:95` ("a host with `debug:disable_logs = 0` re-measured") is **not enough
    for the journal channel**. With `disable_logs = 0` and the default `enable_stdout_logs = 0`,
    the journal would still be blank for markers. The r29 flip needs `disable_logs = 0` **and**
    `enable_stdout_logs = 1`.
  - The r28 session-log flip as written is correct, because the file output is gated only by
    `m_logsEnabled` (`Logger.cpp:48`).

### 5. Whole user and system journal, per boot — SURVIVED
Command: `journalctl [--user] -b N --no-pager -q -o cat`.

| Boot | User journal lines | Core-shaped lines | Overflow | Write-fail | "Socket2" | `_COMM=Hyprland` lines |
|---|---|---|---|---|---|---|
| -3 | 0 | 0 | 0 | 0 | 0 | 0 |
| -2 | 22876 | 0 | 0 | 0 | 0 | 0 |
| -1 | 58644 | 21 | 0 | 0 | 0 | 51 |
| 0 | 87236 | 21 | 0 | 0 | 0 | 51 |

- System journal: `_COMM=Hyprland` gives 0/0/51/51 lines for boots -3/-2/-1/0, and markers are
  0 in every boot.
- `journalctl --user --disk-usage` → "Archived and active journals take up 198.1M".
- The boot -2 user count is large for a 41-second boot. I report it as observed and did not
  analyse it.

### 6. Session log, positive evidence — SURVIVED and strengthened
- Log: `/run/user/1000/hypr/efb50993…_1792804449_426444678/hyprland.log`, sha256 `b7cdca1f…e36c815`,
  27331 lines, 21 core lines, last core line at 21. The independent recount matches S213.
- `EventManager.cpp:85` logs `DEBUG "Socket2 accepted a new client at FD {}"` on every accept.
  Here `grep -cF 'Socket2 accepted a new client'` = **0** and `grep -cF 'Socket2'` = **0**.
- Meanwhile `ss -xpa | grep -cF '.socket2.sock'` = **3** rows. I read those as the listener plus
  server-side ends of live accepted subscribers [INFERENCE: I did not break the rows down;
  C2 seats hold the exact client set].
- So socket2 clients connected during this session and the log recorded none of the accepts.
  This is direct, in-log evidence that the core logger was off when socket2 activity happened,
  not just an argument from the option value.

## Was `debug:disable_logs` the same in earlier sessions? — no direct record; inferred yes

- **F2 (trap): the startup warning is not a record.** Both sessions' unit journal contains
  Hyprland's startup warning that further logs are disabled by default and pointing at
  `debug:disable_logs`. In the source it is emitted **unconditionally**: at
  `ConfigManager.cpp:632-637` the only guard is `if (!g_pCompositor->m_onlyConfigVerification)`.
  Its presence says nothing about the option's value. Do not cite it as evidence.
- **Boot -1 is the r28 session.** The boot -1 unit journal's "Disabling stdout logs … Further logs
  will be written to" line names instance `efb50993…_1792772698_564628331`. That is r28's source
  instance (`event-queue-host-measurement-r28.md:8`), and its log file is gone. Boot -1's journal
  output has the same shape as the current session (core output stops after config load). But
  the journal alone cannot tell `disable_logs = 1` apart from `enable_stdout_logs = 0` (F1).
- Indirect evidence (high confidence [INFERENCE]):
  - **Same package:** `/var/log/pacman.log` → hyprland `0.56.2-2 -> 0.56.2-4` upgraded
    2026-10-20T09:16:38. That is before boot -1 started (2026-10-23 13:24:36) and stayed through
    boot 0. Boot -3 (07:18–13:21 on 10-23) also ran v0.56.2 (pkgrel -4). The compiled default is
    `MS<Bool>("debug:disable_logs", "disable logging to a file", true)` (`ConfigValues.cpp:629`).
  - **Same config, and it never sets the option:** `hyprland.conf` and all 19 files it sources
    (including the omarchy defaults, theme and toggles) have 0 `disable_logs`,
    0 `enable_stdout_logs` and 0 `debug {` blocks. The `.bak.1792267376` copy has none either.
    The newest file mtime is 2026-10-17 17:05 (`gkeep.conf`), before every boot listed.
    The only file on the host naming the option is `/usr/share/hypr/stubs/hl.meta.lua`
    (a package type stub, sha256 `0c3f4c7e…ff851a`).
  - **No runtime toggle found:** live getoption reports `"set":false`, so the current value is the
    default and there is no runtime override in this session. `~/.bash_history` has 0
    `disable_logs` and 0 `hyprctl … keyword … debug` entries. `rg -l -F 'keyword debug:disable_logs'`
    over the fleet and `~/.omp` returned nothing.
  - Remaining gap: a runtime `hyprctl keyword debug:disable_logs 0` in boot -1 or -3 that left no
    history trace cannot be ruled out. No surviving channel records it.
- The package entries record nothing on this. `grep disable_logs|enable_stdout` in r28 and r29
  finds no match in either.

## Further finding (F3): r29's source window is gone

`event-queue-journal-measurement-r29.md:19` claims 1091 unit lines, read 2026-10-23. The unit
journal now holds 717 lines (boot -2: 6, boot -1: 360, boot 0: 351). Boot -3 keeps 0 user-journal
lines although `journalctl --list-boots` lists it, so earlier sessions' unit output has rotated
away. r29's measured window cannot be reproduced. This matches what `registration.md:94` says
about r28's vanished log. It is not a new refusal reason, only a note on reproducibility.

## Tooling

No install or upgrade, and no pacman transaction. I used `git clone` (network, read-only, public
upstream) into `/dev/shm` scratch. `hyprctl` was used only with `version`, `getoption` and
`rollinglog` (no `-f`). No socket connection, no dispatch, no keyword.

## Checks the main agent may rerun
- `hyprctl rollinglog | grep -cE '^(TRACE|DEBUG|LOG|INFO|WARN|ERR|CRIT) \]'` → expect 0.
- `journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat | grep -nE '^DEBUG \]' | cut -d: -f1`
  → expect blocks 41–61 and 401–421.
- To make F1 machine-checkable, the round could commit receipts for `Logger.cpp:47`,
  `ConfigValues.cpp:629,632` and `ConfigManager.cpp:632-637`.
