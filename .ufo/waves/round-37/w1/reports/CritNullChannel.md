# CritNullChannel — critic report, mado round 37 wave 1

Seat: `L1Mado37-2.CritNullChannel` (critic, leaf). Target: the round's central inference, as stated in S213.receipt.txt § reading:
"With debug:disable_logs = 1 the core logger returns before writing (S214 Logger.cpp:15-16, :48) … A zero marker count in either channel therefore cannot distinguish 'never overflowed' from 'not logged'."

**Bottom line: the conclusion holds and is stronger than the receipt argues, but three of its supporting sentences overreach or cite the wrong line, and there is a second, independent null mechanism (file buffering) that the round has not recorded.** Every defect is fixable; none forces the judge to reject anything.

## Sources opened (all read-only)

| Source | sha256 (prefix) | Note |
|---|---|---|
| fetch/S214.bin (Logger.cpp) | d04e3a2fe5c73ad8 | identical to upstream v0.56.2 `src/debug/log/Logger.cpp` (full sha match) |
| fetch/S189.bin (EventManager.cpp) | eea605dfe5ce09e1 | identical to upstream v0.56.2 `src/managers/EventManager.cpp` (full sha match) |
| fetch/S213.receipt.txt | 1c1b0ce149ecd7b1 | |
| fetch/S201.bin (Waybar backend.cpp) | 799bf02f6d18ae04 | |
| `/usr/include/hyprland/src/debug/log/Logger.hpp` (pkg hyprland 0.56.2-4) | aeb07ba1ba1fd5cf | `cmp` against upstream v0.56.2 header: identical (`HDR_IDENTICAL`) |
| `/usr/include/hyprutils/cli/Logger.hpp` (pkg hyprutils 0.14.2-1) | — | installed header |
| scratch: hyprutils v0.14.2 `src/cli/Logger.cpp` | 91dec1f3efae49bb | curl from raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2 |
| scratch: Hyprland v0.56.2 tarball (`Compositor.cpp` 74833ecbf0e2b6f8, `config/legacy/ConfigManager.cpp` 9db68cf44048d865, `config/values/ConfigValues.cpp` a76f05079454e1f6) | — | codeload.github.com/hyprwm/Hyprland/tar.gz/refs/tags/v0.56.2 |

Scratch lives only under `/dev/shm/mado37-CritNullChannel/`. No tools were installed or upgraded. No socket connects, apart from the hyprctl read verbs `getoption`, `rollinglog` and `plugin list`.

## Verdicts per sub-claim

### SC1. "With disable_logs = 1 the core logger writes nothing." Verdict: OVERREACHES as worded; HOLDS for every moment after `initCallbacks`.

- `Logger.hpp:42`: `bool m_logsEnabled = true;`. The gate starts open. It closes only when `recheckCfg` runs (`Logger.cpp:48` `m_logsEnabled = !*PDISABLELOGS;`). That is reached from `initCallbacks` (`Logger.cpp:36-38`), which `Compositor.cpp:298` calls *after* `initIS` (`:229`, which opens the file and enables stdout, `Logger.cpp:29-32`) and after `initManagers(STAGE_PRIORITY)` (`:296`).
- Host evidence that the core logger did write: the session log has 21 core lines, numbered 1-21 (re-derived below), even though `disable_logs` = 1.
- Citation defect: the socket2 markers are formatted calls, `Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", …)` (`EventManager.cpp:175`, and `:155` for "failed writing event"). They resolve to the **template overload in `Logger.hpp:22-33`**, whose first gate is `Logger.hpp:23-24` `if (!m_logsEnabled) return;`, before any formatting. `Logger.cpp:15-16` is only the second, redundant gate (reached via `Logger.hpp:32`). The decisive lines are `Logger.hpp:23` and `Logger.hpp:42` together with `Logger.cpp:48`. S214 alone does not contain them.
- Default value: `ConfigValues.cpp:629` `MS<Bool>("debug:disable_logs", "disable logging to a file", true)`. Live getoption agrees, and `"set": false` means the value comes from that default, not from user config (output under "Commands and quoted output" below).

### SC2. "Does m_logsEnabled start true before config load, so early markers could be logged?" Verdict: the window exists, but it cannot carry a marker, so the claim HOLDS.

- The window is real: `m_logsEnabled = true` from construction until `Compositor.cpp:298`, and the EventManager is created inside it (`Compositor.cpp:678` `g_pEventManager = makeUnique<CEventManager>();` under `STAGE_PRIORITY`; host log line 17 is "Creating the EventManager!").
- A marker needs a client in `m_clients` with 64 queued events (`EventManager.cpp:169-175`). Clients are accepted only by `onClientEvent`, registered on the wl event loop (`EventManager.cpp:40`). That loop is first run by `wl_display_run` (`EventLoopManager.cpp:137`) via `startCompositor()` (`main.cpp:298`), which comes after `initServer` returns (`main.cpp:287`). A grep for `wl_display_run|wl_event_loop_dispatch` in `Compositor.cpp` and `main.cpp` finds no dispatch inside `initServer`. So no client can exist while the gate is open. [INFERENCE, limited to that grep: no other code dispatches the wl loop during `initServer`.]

### SC3. "Could the hyprutils CLI logger (m_logger) be written by another path that bypasses CLogger::log?" Verdict: YES, a bypass exists, but it cannot carry the markers, so the claim HOLDS. The round should name the bypass.

- Bypass: `Compositor.cpp:304-307` builds a `Hyprutils::CLI::CLoggerConnection` on `Log::logger->hu()` (`Logger.cpp:57-59` returns the raw `m_logger`), named "aquamarine", and hands it to aquamarine (`aquamarine/backend/Backend.hpp:74` `logConnection`). `CLoggerConnection::log` checks only `m_logger->m_shouldLogAtAll` (hyprutils `Logger.cpp:183`), which is `m_fileEnabled || m_stdoutEnabled` (`:153`). It never consults `Log::CLogger::m_logsEnabled`. `setOutputFile` in `initIS` set `m_fileEnabled = true` (`:63`), and `recheckCfg` never clears it (`Logger.cpp:47-50` touch only stdout, time and color).
- Other bypass users: a grep for `hu\(\)|CLoggerConnection` over v0.56.2 `src` (excluding headers) finds only `Logger.cpp:57` (definition), `Compositor.cpp:304` (aquamarine), and `CrashReporter.cpp:250` (which *reads* `rolling()`). `hyprctl plugin list` returns `no plugins loaded`, so no plugin uses it either.
- The markers go through `Log::logger->log` (`EventManager.cpp:155`, `:175`), not through `hu()` or a connection, so they stay gated.

### SC4. "Is the 21-core-line observation consistent with a logger that was enabled but quiet?" Verdict: NO. The "enabled but quiet" reading is refuted. The receipt's conclusion holds, but its stated reason is weak.

- The receipt argues from position ("last core line 21, three lines after the second config load"). That does not exclude a logger that is enabled but has nothing to say. What does exclude it: `Compositor.cpp:344-356` writes core lines unconditionally after the aquamarine backend starts, which is after `:298`. Those are "Instance Signature: {}", "Hyprland PID: {}", "===== SYSTEM INFO: =====", and "Running on DRMFD: {}". Each output also logs "New aquamarine output with name {}" (`:459`). Host counts: all five are **0**. Meanwhile "Creating the" (`STAGE_PRIORITY`, before `:298`) appears **13** times. Lines 20-21 ("Creating the PointerManager!", "Creating the AsyncResourceGatherer!") are the last `STAGE_PRIORITY` lines before `initCallbacks`. This sequence is exactly a gate closing at `Compositor.cpp:298`.
- Trap for the corpus writer: line 13 of the session log ("!!!!HEY YOU … further logs to stdout / logfile are disabled by default …") is unconditional (`legacy/ConfigManager.cpp:632-637`, guarded only by `!m_onlyConfigVerification`), so it does **not** prove the setting's value. Line 19 ("Disabling stdout logs … Further logs will be written to <instance>/hyprland.log", `legacy/ConfigManager.cpp:1047-1051`) states the opposite of what happens to core lines when `disable_logs` = 1. Neither line may be cited as evidence about the setting.

### SC5. "Is '27,280 aquamarine lines' evidence the file channel is live for aquamarine only?" Verdict: OVERREACHES twice.

- (a) "Only aquamarine": the lines prove the **hyprutils file sink is open** (`m_fileEnabled`). It accepts any writer that reaches `CLoggerImpl::log`, and the core logger is blocked upstream by `Log::CLogger`'s gate. The sink is not aquamarine-only by design. Aquamarine is the only writer *observed*, because it is the only gate bypass in v0.56.2 (SC3). The correct wording is "sink open; core path gated off; aquamarine is the only bypass writer".
- (b) "Live": **the file is block-buffered and lags memory.** hyprutils `Logger.cpp:146` writes `m_logOfs << logPrefix << logMsg << "\n";`, with no flush or `endl` anywhere in the file. On the host:
  - The log does not end with a newline (`tail -c 1` = `N`, `ends_with_newline False`). The file stops mid-record.
  - `hyprctl rollinglog` (the in-memory copy of the same stream, `Logger.cpp:148-149`) holds 26 lines, all `DEBUG from aquamarine ]`. Of the 25 complete ones, only the first 7 match the file's tail; **18 lines (about 2660 bytes) are in memory but not on disk.**
  - The file's mtime is 04:24:03 and the check ran at 09:15:21, so the on-disk file had lagged the process for about 4 h 51 m.
  - Consequence: even with `disable_logs` = 0, a zero marker count in `hyprland.log` cannot cover the most recent buffered kilobytes. This is a second, independent reason the file is not an absence channel. The round has not recorded it.

### SC6. Journal side of "either channel". Verdict: HOLDS, but the receipt's journal query has the wrong scope.

- `Logger.cpp:47` `setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT)` resolves to `!1 && 0`, which is false. After `initCallbacks` nothing reaches stdout, so the unit journal is null for core and aquamarine lines alike. This matches the receipt's probe (`in_log=7 in_unit_journal=0`).
- Scope defect: S213's `journalctl --user -u wayland-wm@hyprland.desktop.service` has no `-b`/`_PID` filter. Re-run: all = 717 lines, `-b 0` = 351, `_PID=1619` = 51. Lines by date: 701 on 2026-10-23 and 6 on 2026-10-24. Four boots are listed. "Using config": all = 4, `-b 0` = 2. "Creating the": all = 26, `-b 0` = 13. The receipt's `unit_journal_using_config_lines: 4` therefore spans **two Hyprland starts** and is not comparable with the log's 2 config loads. The journal also contains a stack-trace block from an earlier instance (lines starting with `#0` … `#5`, `ELF` and `Stack`; counts only). The zero is still a null, but over several instances.

## Additional finding: both ends of the event socket are silent

- Client side: Waybar 0.15.0 `socketListener` (S201.bin:117-122): `fgets` returns `nullptr` → `sleep_for(1ms); continue;`. Waybar logs nothing when Hyprland removes it (EOF), so its own log cannot substitute for the marker either.
- A non-null, read-only, connect-free channel exists: `ss -xpH` (kernel unix_diag census). Host now: 2 socket2 connections, both `ESTAB`. One peer is `waybar` (pid 935660, started Sun Oct 25 02:06:20, parent systemd), the other `socat` (pid 2293, started Fri Oct 23 22:14:11). Hyprland pid 1619 started Fri Oct 23 22:14:09. Client-end `recvq=0 sendq=0` for both. A removed client disappears from this census. Client-end Recv-Q growth is the stall precursor before Hyprland's 64-event cap (`EventManager.cpp:169`). [INFERENCE: that unix_diag Recv-Q on a stream socket reports unread bytes; the kernel source was not opened.]
- Counterexample to any "no overflow this session" reading: Waybar's current connection dates from 02:06 on 10-25, about 28 h into the Hyprland session. Something ended the earlier Waybar process. Its cause cannot be attributed from any channel examined here, which is the round's point.

## Commands and quoted output (load-bearing only)

```
$ hyprctl -j getoption debug:disable_logs / debug:enable_stdout_logs / debug:disable_time
{"option": "debug:disable_logs", "int": 1, "set": false }
{"option": "debug:enable_stdout_logs", "int": 0, "set": false }
{"option": "debug:disable_time", "int": 1, "set": false }

$ (session log, instance efb50993…_1792804449_426444678 == $HYPRLAND_INSTANCE_SIGNATURE; Hyprland pid 1619 holds 1 fd on it)
size=4259033 mtime=2026-10-25 04:24:03.444802113 -0300     (date: 2026-10-25T09:15:21-03:00)
27331
--- origin histogram
     21 DEBUG ]
  27280 DEBUG from aquamarine ]
     31 ERR from aquamarine ]
--- core line numbers
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
--- first aquamarine line
22
Instance Signature=0  Hyprland PID=0  SYSTEM INFO=0  Running on DRMFD=0  New aquamarine output=0
Creating the=13  overflowed event queue=0  failed writing event=0  Socket2=0

$ hyprctl rollinglog > rolling.txt   →   26 4042 rolling.txt ; 26 DEBUG from aquamarine ]
file_lines 27332 rolling_lines_used 25
file_tail_equals_rolling_tail False
overlap_file_suffix_vs_rolling_prefix 7 rolling_lines_not_in_file_tail 18
pending_bytes_est 2660
$ tail -c 1 hyprland.log | od -c   →   0000000   N        ends_with_newline False

$ journalctl --user -u wayland-wm@hyprland.desktop.service …
all: 717   boot0: 351   pid1619: 51
Using config all=4 b0=2 ; Creating the all=26 b0=13 ; overflowed event queue all=0 b0=0 ; failed writing event all=0 b0=0 ; Socket2 fd all=0 b0=0

$ hyprctl plugin list   →   no plugins loaded

$ ss -xpH (socket2 rows; peer → owner)
.socket2.sock 181151236 * 181143087   → peer 181143087 -> users:(("waybar"
.socket2.sock 10029 * 40790           → peer 40790 -> users:(("socat"
peer_endpoint 181143087 state=ESTAB recvq=0 sendq=0
peer_endpoint 40790 state=ESTAB recvq=0 sendq=0
```

The 21 core lines were read with `/home/...` paths redacted. They match the source templates named above. No journal line and no window title is reproduced here.

## Impacted axes

- **Coverage (C1)**: `event-queue-observability-r37.md` must not present the log or the journal as an absence channel. It should cite `Logger.hpp:23`/`:42`, `Compositor.cpp:298`/`:304`, and hyprutils `Logger.cpp:146`/`:183`. The cited lines `Logger.cpp:15-16`/`:48` are necessary but not sufficient. It must not quote session-log lines 13 or 19 as evidence about the setting.
- **Operability (C2)**: `mado-eventq.py`'s live-receipt replay must report the log count as *unobservable* (not 0) when `disable_logs` = 1. When it is 0, it must still flag buffered lag: the file ends without a newline, or the rollinglog tail is not in the file. It must scope the journal to `-b 0` or `_PID=<hyprland>`. If a live channel is wanted, the `ss -x` census is read-only and connect-free.

## Smallest safe correction

Replace the S213 § reading sentence (in the next receipt or errata; S213 itself is frozen data) with:

> With debug:disable_logs = 1 (default, ConfigValues.cpp:629), `Log::CLogger` drops every core line after `initCallbacks` (Compositor.cpp:298 → Logger.cpp:48; gate Logger.hpp:23-24 for the formatted overload used at EventManager.cpp:155/:175). Core lines before that point (m_logsEnabled defaults true, Logger.hpp:42) cannot include a socket2 marker, because no client is accepted before `wl_display_run`. Aquamarine lines reach the same file through a `CLoggerConnection` (Compositor.cpp:304; hyprutils Logger.cpp:183) that bypasses the gate. The file is block-buffered (hyprutils Logger.cpp:146), so even an enabled log lags the process. The unit journal gets nothing after the gate closes (Logger.cpp:47) and must be scoped to one boot or PID.

Fixable defects, not judge-rejecting tradeoffs: the citation gap (SC1), the weak positional argument (SC4), the "aquamarine only / live" wording (SC5), and the journal scope (SC6).
