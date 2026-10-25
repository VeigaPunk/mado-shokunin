# ScoutLogger — round 37 wave 1 report

Seat: L1Mado37-2.ScoutLogger (scout). Scratch: `/dev/shm/mado37-ScoutLogger/` (no lane writes besides this file).
Tools installed/updated: none. No pacman transaction (only `pacman -Q`, a read-only query). No socket connections; `hyprctl` read verbs only (`version`, `getoption`, `rollinglog`).
LSP: not used — sources are fetched upstream snapshots outside any project with a configured server; all symbol tracing below is literal `rg` over the full commit tarball (text evidence, not semantic proof). The relevant symbols (`hu()`, `CLoggerConnection`, `logConnection`, `m_logsEnabled`) have very few uses each, so grep coverage of the whole tree is complete for them.

## Sources opened (all at Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` = v0.56.2)

| artifact | sha256 | note |
|---|---|---|
| raw `src/debug/log/Logger.cpp` | `d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868` | `cmp` with S214.bin → `CMP_IDENTICAL` (same sha) |
| codeload tarball of the commit | `5b05ce7ba5296fa46e666852bf108ab5af121bf577f8043787e2d2c252d8f109` | tarball Logger.cpp `cmp` == raw (`tarball_logger_same`); tarball EventManager.cpp `cmp` == S189.bin (`EM_eq_S189`) |
| git tree API `?recursive=1` | — | `truncated False n 1181` |
| hyprutils tag `v0.14.2` tarball | `2061b7b08c8104fb02a609553b28f6c8580e5ec38633015845f1c4553980175b` | host lib version |
| aquamarine tag `v0.15.1` tarball | `2f9de98c0bd1b7b1b09c576e390a2fef436449762fb334163c414f0c300296f2` | host lib version |

Host binds to exactly these versions (`hyprctl version`):
`Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`,
`Hyprutils: built against 0.14.2, system has 0.14.2`, `Aquamarine: built against 0.15.1, system has 0.15.1`;
`pacman -Q` → `hyprland 0.56.2-4`, `hyprutils 0.14.2-1`, `aquamarine 0.15.1-1`.

## (1) Where `debug:disable_logs` is declared, and its default — FOUND

- Declared at `src/config/values/ConfigValues.cpp:629`:
  `MS<Bool>("debug:disable_logs", "disable logging to a file", true),` → **default = true (1)**.
  Siblings: `:630` `debug:disable_time` default `true`; `:632` `debug:enable_stdout_logs` default `false`; `:638` `debug:colored_stdout_logs` default `true`.
- Neither `src/config/legacy/DefaultConfig.hpp` nor `src/config/lua/DefaultConfig.hpp` mentions it (`rg -n disable_logs` over the whole tarball hits only Logger.cpp:42, ConfigValues.cpp:629, legacy/ConfigManager.cpp:635 and `hyprtester/test.lua:171` `disable_logs = false,`, i.e. the test harness turns it off).
- The legacy parser itself announces the default: `src/config/legacy/ConfigManager.cpp:633-636` logs at DEBUG `"!!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default. BEFORE SENDING THIS LOG, ENABLE THEM. Use debug:disable_logs = false ..."`.
- Consumer: `src/debug/log/Logger.cpp:42` reads it; `:47` `m_logger.setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT);` `:48` `m_logsEnabled = !*PDISABLELOGS;`.
- Host: `hyprctl getoption debug:disable_logs` → `int: 1` / `set: false`. **`set: false` means the host runs the shipped default; nobody set it.** (`debug:enable_stdout_logs` → `int: 0`, `set: false`.)

Verdict: PASS (line-cited). Correction to the framing "on this host disable_logs = 1": true, but it is the upstream default, not a host choice — so the observability blind spot applies to every stock v0.56.2 install, not just this host.

## (2) How aquamarine's lines reach hyprland.log — they BYPASS `m_logsEnabled` — FOUND

Chain, line-cited:
1. `src/Compositor.cpp:229` `Log::logger->initIS(m_instancePath);` → `Logger.cpp:29` `m_logger.setOutputFile(... "/hyprland.log")`, `:30` `setEnableRolling(true)`. In hyprutils `src/cli/Logger.cpp:63-64` this sets `m_fileEnabled = true` and recomputes `m_shouldLogAtAll`.
2. `src/Compositor.cpp:304-307`:
   `SP<Hyprutils::CLI::CLoggerConnection> conn = makeShared<Hyprutils::CLI::CLoggerConnection>(Log::logger->hu());` / `conn->setLogLevel(Log::DEBUG);` / `conn->setName("aquamarine");` / `options.logConnection = std::move(conn);`
   `Log::logger->hu()` (`Logger.cpp:57-59`) returns the raw `Hyprutils::CLI::CLogger m_logger` — it does **not** go through `Log::CLogger::log` (`Logger.cpp:14-16`), the only place `m_logsEnabled` is checked (plus the template overload `Logger.hpp:23-24`). This is the sole use of `hu()` / `CLoggerConnection` / `logConnection` in the tree (`rg` over `hl/src`: Logger.hpp:36, Logger.cpp:57, Compositor.cpp:304, :307).
3. aquamarine v0.15.1: `src/backend/Backend.cpp:68` `backend->logger->m_loggerConnection = options.logConnection;`; `src/backend/Logger.cpp:31-32` `m_loggerConnection->log(levelToHU(level), str);` (level map `:8-12`: ERROR→LOG_ERR, CRITICAL→LOG_CRIT …).
4. hyprutils v0.14.2 `src/cli/Logger.cpp:179-189` `CLoggerConnection::log`: gates only on `m_logger->m_shouldLogAtAll` (`:183`) and `level < m_logLevel` (`:186`), then `m_impl->log(level, msg, m_name)`.
   `m_shouldLogAtAll = m_fileEnabled || m_stdoutEnabled` (`:152-153`). `disable_logs=1` only turns stdout off (Hyprland `Logger.cpp:47`); **nothing ever turns file output off** (only `setOutputFile("")` does, `:38-41`, never called by Hyprland). So `m_shouldLogAtAll` stays true and aquamarine lines are written to the file (`:145-146`) and the rolling buffer (`:148-149`) with a `from aquamarine ` tag (`:128-131`).

Why the core cutoff falls at line 21: `m_logsEnabled` defaults to `true` (`Logger.hpp:42`) and is only re-read at `Log::logger->initCallbacks()` (`Compositor.cpp:298` → `Logger.cpp:36-38`), which runs after `initManagers(STAGE_PRIORITY)` (`Compositor.cpp:296`; the stage spans `:645-690`, config parsed at `:664-665`, last log `:688` "Creating the AsyncResourceGatherer!"). The aquamarine backend is created after that (`Compositor.cpp:321`; aquamarine `Backend.cpp:75` "Creating an Aquamarine backend!").

Host evidence (counts only; first ≤4 message words of Hyprland's own static strings for lines 12-22):
```
total_lines 27331
aq_lines 27311
non_aq_lines 21
last_non_aq_lineno 21
first_aq_lineno 22
HEYYOU_lineno 13
overflow_marker 0
aq_levels:   27280 DEBUG / 31 ERR
core_levels: 21 DEBUG
14: Creating the Error Overlay!   ... 21: Creating the AsyncResourceGatherer!
22: Creating an Aquamarine backend!
```
So the log the L1 called "21 core lines all precede line 22" is confirmed, and the file keeps growing (4,259,033 bytes) purely from aquamarine, including 31 aquamarine ERR lines.
`hyprctl rollinglog` → `rolling_bytes 4041 rolling_lines 26 rolling_aq 26`, zero non-aquamarine prefixed lines: the in-memory rolling buffer (hyprutils `ROLLING_LOG_SIZE = 4096`, `:157`) is likewise aquamarine-only.

Side fact: `hyprctl rollinglog -f` (follow) is fed only by `SRollingLogFollow::addLog`, called only from `Log::CLogger::log` after the `m_logsEnabled` gate (`Logger.cpp:21-22`); aquamarine lines never enter it. With `disable_logs=1`, follow mode carries nothing but its own `[LOG] Following log to socket ...` header (`RollingLogFollow.hpp:59`) — [INFERENCE] from source; not run (it would hold a socket open, and the bounds forbid me relying on it).

Verdict: PASS (line-cited, host-corroborated).

## (3) Are ERR/CRIT exempt from `m_logsEnabled` anywhere? — NO

- `Logger.cpp:14-16` and `Logger.hpp:23-24` return on `!m_logsEnabled` **before** any level test; the only level test after it is the TRACE filter (`:18-19`, `Logger.hpp:26-27`). No level is exempt.
- `rg -n 'm_logsEnabled'` over the tree: only `Logger.hpp:23`, `:42`, `Logger.cpp:15`, `:48`. No other gate or bypass for core code.
- Concretely dropped on this host: `EventManager.cpp:175` `Log::ERR, "Socket2 fd {} overflowed event queue, removing"`; `:155` `Log::ERR, "Socket2 fd {} failed writing event: ..."`; `:165` WARN shutdown suppression; `MiscFunctions.cpp:620` `Log::CRIT, "Critical error thrown: {}"`; `macros.hpp:48` ASSERTION FAILED CRIT; `macros.hpp:91` MEMORY CORRUPTED CRIT.
- The only ERR/CRIT lines that survive are aquamarine's (via path (2)) — host shows 31 aquamarine ERR, 0 core ERR.
- The crash report also gets no core context: `CrashReporter.cpp:250` appends `Log::logger->rolling()`, which with `disable_logs=1` holds only aquamarine lines.

Verdict: PASS (no exemption exists).

## Consequences for the observability entry (§2-§3, Unknowns)

- **§2 (channels):** `hyprland.log` and `hyprctl rollinglog` stay live under `disable_logs=1` but carry only `from aquamarine` lines after the init cutoff. A growing log or fresh rolling buffer therefore does **not** show core logging is on. `rollinglog -f` carries no core lines either. The overflow marker (EventManager.cpp:175, ERR) has no surviving channel.
- **§3 (reading a zero):** `overflow_marker 0` (and journal zero) cannot be evidence of "never overflowed" while `getoption debug:disable_logs` = `int: 1`. A valid null requires reading `disable_logs` = 0 for the whole window, plus checking that the core-line count grows after `initCallbacks`; one test is a line without `from aquamarine` after the first aquamarine line. Under the default, the overflow is silent apart from its side effect: `removeClientByFD` at `:176` closes the client fd, so the client sees EOF/disconnect. That is client-side evidence only.
- **Unknowns to keep:** (a) whether `disable_logs` was ever 0 earlier in this session (`getoption` gives the current value only; `set: false` suggests never, [INFERENCE]); (b) how `rollinglog -f` behaves live — inferred from source, not run; (c) the `getoption` → `int:` rendering of a Bool was observed, but I did not trace the Bool→INTEGER `CConfigValue` cast. Logger.cpp:42 reads it as `Config::INTEGER`, and the observed `int: 1` matches.

## Commands run (all from `/dev/shm/mado37-ScoutLogger`)
`curl -sSfL` of raw Logger.cpp, tree API, raw Logger.hpp/Compositor.cpp/ConfigValues.{cpp,hpp}/ConfigManager.cpp (root, legacy, lua)/main.cpp, codeload tarballs (Hyprland@commit, hyprutils@v0.14.2, aquamarine@v0.15.1); `cmp` ×3; `sha256sum`; `rg`/`sed`/`awk` reads; `pacman -Q hyprland hyprutils aquamarine`; `hyprctl version`; `hyprctl getoption debug:disable_logs`; `hyprctl getoption debug:enable_stdout_logs`; `hyprctl rollinglog` (piped to counts only); `rg -c`/`awk` counts on `$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/hyprland.log`; `env | rg -o '^(HYPRLAND_TRACE|AQ_TRACE)='` → `no_trace_env`.
