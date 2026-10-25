# Review report — L1Mado37-2.RevAfterC1 (residual falsify, C1)

Rev under test: `3f424257a1ea69cd2655770259ba00b423293f4f` = HEAD; worktree copies of
`corpus/lessons/round-37.md`, `corpus/knowledge/event-delivery-limits-r26.md`,
`corpus/knowledge/event-queue-observability-r37.md` are byte-identical to the rev
(sha256 match per file, quoted below).

## 1. Counter re-run (exact command and output)

Command (run as assigned):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r37-event-ground.py --repo . --rev 3f424257a1ea69cd2655770259ba00b423293f4f
```

Output (verbatim):

```
PRED-C1-r37-v2 entry=corpus/knowledge/event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 ids=S189,S201,S212 ok=1
PRED-C1-r37-v2 entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 ids=S189,S213,S214,S215,S216,S217 ok=1
PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET rev=3f424257a1ea69cd2655770259ba00b423293f4f base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
```

Verdict: PASS (counter output as declared by registration; exit 0).

## 2. GATE lines — digest binding (round-37.md lines 28–36)

Declared sha256 vs on-disk receipt and vs re-fetched URL (`fetch/` = `.ufo/waves/round-37/fetch/`):

| GATE | declared | on-disk | re-fetch URL | re-fetch |
|---|---|---|---|---|
| S189 (×2) | eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d | match | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp` | match |
| S201 | 799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e | match | `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp` | match |
| S212 | 1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9 | match | `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp` | match |
| S213 | 1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58 | match | host receipt, re-derived (§3) | — |
| S214 | d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868 | match | `.../hyprwm/Hyprland/efb5099.../src/debug/log/Logger.cpp` | match |
| S215 | a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754 | match | `.../src/config/values/ConfigValues.cpp` | match |
| S216 | 74833ecbf0e2b6f8ad84345ac0716a3295a0e347420a188be0ab4f6a684af7c0 | match | `.../src/Compositor.cpp` | match |
| S217 | aeb07ba1ba1fd5cfdb75aaf7434910c887096c24952f1a6788f71a4d7dbe78fe | match | `.../src/debug/log/Logger.hpp` | match |

All seven raw URLs re-fetched (curl -fsSL, pinned commits) byte-match the declared digests;
sha256 quoted in the shell run above.

GATE quotes present at located lines: S189 `const size_t MAX_QUEUED_EVENTS = 64;` @169 and
`Socket2 fd {} overflowed event queue, removing` @175; S201 buffer+comment @115; S212
`m_ipc.registerForIPC("workspacev2", this);` @804; S213 receipt `debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}` @receipt:28; S214 `m_logsEnabled = !*PDISABLELOGS;` @48; S215 `MS<Bool>("debug:disable_logs", "disable logging to a file", true),` @629; S216 `conn->setName("aquamarine");` @306; S217 `if (!m_logsEnabled)` @23.

## 3. GATE S213 — host receipt re-derived (read-only verbs)

- `hyprctl getoption debug:disable_logs -j` → `{"option": "debug:disable_logs", "int": 1, "set": false }`; `debug:enable_stdout_logs` → `int 0` — match receipt lines 28–29.
- Session log `/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/hyprland.log`: exists; `stat` bytes=4259033, mtime=2026-10-25 04:24:03.444802113 -0300 — exact match. `wc -l`=27331, marker counts 0/0/0, probe `drm: getCurrentCRTC: No CRTC 0`=7, core-logger (`^[A-Z]+ \]`) lines=21 with last at line 21, `Using config:` at lines 12 and 18 — all as receipt.
- `journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat`: 717 lines; marker counts 0/0/0; probe=0; only 4 `ERR` substring hits are `QT_STYLE_OVERRIDE` env notes (no ERR-class log lines); 4 `Using config:` lines.

Verdict: PASS.

## 4. OBS verdicts

### event-delivery-limits-r26.md (`corpus/knowledge/event-delivery-limits-r26.md`)

| OBS | cited bytes / lines | verdict |
|---|---|---|
| §1 S189: `socket(AF_UNIX, SOCK_STREAM \| SOCK_CLOEXEC \| SOCK_NONBLOCK, 0)` @14, `listen(…,10)` @35, `accept4(…, SOCK_CLOEXEC \| SOCK_NONBLOCK)` @73; compositor never reads from a client | S189.bin:14/35/73; `flushClient` writes only — no client read in cited bytes | holds |
| §1 S189: cap is a count of events, not bytes, @169 | S189.bin:169 exact | holds |
| §1 S189: cap checked only on post, `:172-177`; overflow log @175, remove @176; else append+flush `:180-182`, writable armed when was empty `:187-188` | S189.bin:172-177 (`QUEUESIZE >= MAX_QUEUED_EVENTS`, log 175, `removeClientByFD` 176, continue 177); 180 push_back, 181 flushClient, 187-188 `QUEUESIZE == 0` arm | holds |
| §1 S189: `flushClient` `:133-161`, partial resume via `writeOffset` `:136-144`; EAGAIN/EWOULDBLOCK leave queued `:149-150`; EINTR retries `:152-153`; zero-byte/other error logs `Socket2 fd {} failed writing event: {}` @155 and client removed | S189.bin:133-161; 136-144; 149-150; 152-153; 155 (`Log::logger->log(Log::ERR, "Socket2 fd {} failed writing event: {}", …)`, `return false`) | holds |
| §1 S189: shutdown drop logs WARN instead of delivering `:164-166`; event cut to 1024 bytes before framing, `EVENT>>`+≤1024+`\n` @128 | S189.bin:164-166 (`Suppressed (shutting down)` WARN, return); 128 `std::format("{}>>{}\n", event.event, data.substr(0, 1024))` | holds |

### event-queue-observability-r37.md (`corpus/knowledge/event-queue-observability-r37.md`)

| OBS | cited bytes / lines | verdict |
|---|---|---|
| §1 S189: both removal paths log through core logger — overflow `:175`, fail-write `:155` | S189.bin:175/155 (both `Log::logger->log(Log::ERR, …)`) | holds |
| §2 S215: `debug:disable_logs` default true @629; `enable_stdout_logs` default false @632 | S215.bin:629 `MS<Bool>("debug:disable_logs", "disable logging to a file", true),`; 632 `…("debug:enable_stdout_logs", "enables logging to stdout", false),` | holds |
| §2 S217: markers are formatted calls → template overload gate `if (!m_logsEnabled)` / `return;` `Logger.hpp:22-24` before formatting; flag `bool m_logsEnabled = true;` @42 | S217.bin:22-24 (overload opens 22, if 23, return 24, format 29-30 after gate); 42 | holds |
| §2 S214: `m_logsEnabled = !*PDISABLELOGS;` @48; string overload re-checks `:15-16` before rolling feed `:21-22` and write @24; stdout only when on+`enable_stdout_logs` @47 | S214.bin:48; 15-16 (`if (!m_logsEnabled)`/`return;`); 21-22 (`SRollingLogFollow::get().addLog(str)`); 24 `m_logger.log(level, str);`; 47 `m_logger.setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT);` | holds |
| §2 S216: switch applied in `Log::logger->initCallbacks();` @298 after first init stage; aquamarine handed raw hyprutils logger `conn->setName("aquamarine");` `:304-307` | S216.bin:298; 304-307 (`conn = makeShared<…CLoggerConnection>(Log::logger->hu());`, setLogLevel, setName 306, `options.logConnection = std::move(conn);` 307) | holds |
| §2 S213: on this host both options at defaults | re-derived (`hyprctl getoption`, §3): int 1 / int 0, `set:false` | holds |
| §3 S213: session log 27,331 lines holds 21 core-logger lines, last @21, three lines after second config load (line 18); every later line aquamarine (27,280 DEBUG, 31 ERR); zero lines match either marker | re-derived: `wc -l`=27331 (27332 physical; final line unterminated); core lines=21, last @21; `Using config:` @12/18; histogram 27280 DEBUG + 31 ERR aquamarine + 21 DEBUG core = 27332 (all lines classed); markers 0/0/0 | holds |
| §3 S213: unit journal 717 lines over four service runs, no ERR-class line; probe string 7× in log, 0× in journal; zero marker lines | re-derived: 717 lines; no ERR-class log line (4 `ERR` substrings are `QT_STYLE_OVERRIDE` env notes); probe 7 → 0; markers 0/0/0 | holds |

No OBS line found to be wrong-seated or overreaching. All line numbers cited in OBS bodies
were re-checked against the receipt bytes.

## 5. Findings (by severity)

- **Low — narrative imprecision in an INF (not an OBS)**: `event-queue-observability-r37.md`
  §3 INF says the core logger "never writes to the journal", but the unit journal actually
  contains 42 core-logger `DEBUG ]` lines (e.g. `Creating the ConfigManager!`, `Using config:`,
  the "HEY YOU" disable notice), all from unit startup before logging is disabled. The OBS
  lines themselves do not claim this, and the inference that matters (markers cannot appear,
  because they are runtime events and `m_logsEnabled=false` gates the logger in both channels)
  is unaffected. Suggest rewording the INF to "the core logger writes no post-startup line to
  the journal".
- **Nit — line-count semantics**: `wc -l` reports 27,331 for the session log while there are
  27,332 physical lines (final line has no trailing newline). The receipt and the OBS figures
  match `wc -l` semantics; histogram classes sum to 27,332. No effect on the claim.
- **Nit — "four service runs"** is not directly countable from the journal; the re-derived
  journal shows 4 `Using config:` lines (two start sequences × two config loads). Not OBS-critical.

## 6. Residual risk / gaps

- Re-fetch was done against the pinned commits named in the lesson table; GitHub raw URLs at a
  pinned SHA are immutable, so the digest binding is sound. The host receipt S213 was re-derived
  only read-only (getoption, file stat/counts, journalctl); the exact `journalctl` command
  output was not byte-compared to the receipt's memory of it (receipt stores counts only).
- The "never reads from a client" OBS and the §5 route inference rest on the absence of any
  client-read call in the cited `EventManager.cpp` bytes; no other event-path source beyond
  S189 was re-fetched (none is cited by an OBS).

## 7. Commands used

Counter re-run, `sha256sum` on `fetch/*`, `curl -fsSL` re-fetch ×7 + sha256, `hyprctl
getoption debug:disable_logs -j` / `debug:enable_stdout_logs -j`, `stat`/`wc -l`/`grep -c`
on the session log, `journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q
-o cat` + counts, `grep -nF`/`awk` line-number checks on every receipt, `git show
3f424257a1ea69cd2655770259ba00b423293f4f:<file> | sha256sum` for the three corpus files
(all match worktree). No installs; no repo state touched.
