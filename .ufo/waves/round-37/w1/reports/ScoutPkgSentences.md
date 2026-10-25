# ScoutPkgSentences — sentence-level audit of the three event-queue package entries, and their three SOURCES rows

Seat: L1Mado37-2.ScoutPkgSentences (scout, read-only). Date 2026-10-25.
Writes: this report only; scratch only under `/dev/shm/mado37-ScoutPkgSentences/` (census copy). No lane production file, no package file, no socket touched. No tool installed.

## Verdict summary

- **event-delivery-limits-r26.md**: the source-code half holds against S189/S212 bytes, with one exception. The "1024 bytes matches the compositor's 1024 truncation" sentence is **wrong**: `fgets` with a 1024 buffer reads ≤1023 chars, but the compositor's line is `event>>` + up to 1024 data chars + `\n`. Two §2 inferences fail on this host or cannot be checked. The causal mechanism ("blocked custom-module producer") has no support in the bytes. "Logged compositor-side" is **wrong** on this host, where `debug:disable_logs` = 1.
- **event-queue-host-measurement-r28.md**: the measurement **cannot be checked**, because the log file no longer exists (ENOENT). The conclusion ("never hit its cap") is **wrong as an inference**. The core logger is disabled, and the current session proves the log is blind to socket2: 2 live socket2 clients, 0 `Socket2` lines. "The markers are emitted only on failure" is **wrong** for the third marker: `Socket2 fd` also matches the normal DEBUG hang-up line (S189:100).
- **event-queue-journal-measurement-r29.md**: its counts **cannot be checked** (1091 lines then, 717 now; the flags were not recorded). Its zeros **hold** now. Its conclusion is **wrong**: the journal is a null channel because stdout is disabled (S214:47) and the probe string appears in the log but not the journal (S213).
- **Rows S214 / S226 / S242**: each has 11 cells, no `|` inside a cell, and a valid ISO `opened`. **None can be appended as-is**: all three fail fleet census **E09** (recheck cell). S214 also collides with the lane's round-37 S214 (Logger.cpp) and has a wrong anchor span. S226's artefact is gone. S242's anchor cannot be reproduced and its `teaches` cell is wrong.

## Commands run (all read-only)

```
cat -n fetch/S189.bin fetch/S201.bin fetch/S214.bin; sed -n '145,165p;795,825p' fetch/S212.bin   # plus sha256sum
cmp round-37/fetch/S189.bin round-32/fetch/S189.bin  -> S189-identical-r32
cmp round-37/fetch/S201.bin round-34/fetch/S201.bin  -> S201-identical-r34
sha256 prefixes: S189 eea605dfe5ce09e1, S201 799bf02f6d18ae04, S212 1e19d92638e7923f, S214 d04e3a2fe5c73ad8
hyprctl version            -> "Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean"
hyprctl -j getoption debug:disable_logs       -> {"option":"debug:disable_logs","int":1,"set":false}
hyprctl -j getoption debug:enable_stdout_logs -> {"option":"debug:enable_stdout_logs","int":0,"set":false}
rg -c 'disable_logs|enable_stdout_logs' ~/.config/hypr  -> no match, rc=1   (value is Hyprland's default, not user-set)
ls -1 /run/user/1000/hypr/  -> efb50993…_1792804449_426444678   (only the current instance)
stat …/efb50993…_1792772698_564628331/hyprland.log -> "No such file or directory (os error 2)"
ls -1A ~/.local/share/hyprland/ -> lastNag, lastVersion
uptime -s -> 2026-10-23 22:14:06 (local -0300);  date -u -d @1792772698 -> 2026-10-23T16:24:58Z; @1792804449 -> 2026-10-24T01:14:09Z
current log (…_1792804449_…/hyprland.log): bytes=4259033, 27331 lines;
  grep -cF: "overflowed event queue" 0, "failed writing event" 0, "Socket2 fd" 0, "Socket2" 0,
            "Socket2 accepted" 0, "hung up" 0, "Suppressed (shutting down)" 0; core-logger lines 21
ss -xpH | grep -F .socket2.sock  -> 2 ESTAB entries owned by "Hyprland", Send-Q 0 / Recv-Q 0;
  peers by inode -> waybar (181143087), socat (40790)       [not this seat's socat; no socket connected here]
journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat -> 717 lines, sha16 43bf1f07176502bf
journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager           -> 718 lines, sha16 4b89242bf4d87bb7
  unit counts: overflowed 0, failed writing 0, "Socket2 fd" 0, "Socket2" 0
  unit retained window (timestamps only): first 2026-10-23T12:39:20Z, last 2026-10-24T15:09:57Z, n=707
journalctl --user --no-pager -q -o cat -> 168754 lines; overflowed 0, failed writing 0, "Socket2 fd" 0, "Socket2" 0
registerForIPC in S212.bin: lines 804-821 -> 13; lines 804-815 -> 12; whole file -> 15
scripts/sources-census.sh validate --today 2026-10-25 <scratch copy of lane registry + the 3 rows>  (see Rows)
```

Privacy: counts and digests only; no journal line or window title reproduced.

## 1. event-delivery-limits-r26.md (package path `…/knowledge/corpus/knowledge/`)

| # | line | sentence (abridged) | verdict | deciding evidence |
|---|---|---|---|---|
| 1 | 4-5 | Substrates read-only; source files read; no socket connected, no event observed | unverifiable | Process claim; no byte records it |
| 2 | 7 | `source: S214 — …Waybar/0.15.0/src/modules/hyprland/workspaces.cpp — § event registrations — tag 0.15.0` | holds (document) / wrong (id under lane numbering) | S212.bin sha16 `1e19d92638e7923f` = row's prefix; renumber-map: package S214 → lane **S212**; lane S214 is now Logger.cpp |
| 3 | 9 | recheck 90d … "(ran 2026-10-23)" | unverifiable | Process claim |
| 4 | 12-17 | Merge note: add wave-1 rows S187 (event manager) and S188 (Waybar backend) | holds by map; referents absent in package | `grep -nE '^\| S18[78] ' SOURCES.append.md` → nothing; renumber-map maps them to lane S189/S201 (byte-identical, cmp above) |
| 5 | 20-21 | The event socket gives each connected client its own queue | holds | S189:172 `it->events.size()`, :180 `it->events.push_back(sharedEvent)`. Per-client queue; payload shared (:170 `makeShared`) |
| 6 | 21 | …and the compositor writes to that client from its own event loop | holds | S189:182 `flushClient` inside `postEvent`; :88 client fd on `m_wlEventLoop`; :105-109 WRITABLE path |
| 7 | 23-24 | The cap is explicit in the host's v0.56.2 event manager | holds | S189:169 `const size_t MAX_QUEUED_EVENTS = 64;`; `hyprctl version` → v0.56.2 commit efb50993…, same commit as the S189 URL |
| 8 | 26 | Quote `const size_t MAX_QUEUED_EVENTS = 64;` | holds (verbatim) | S189:169 |
| 9 | 28-29 | A client whose queue is at or over the cap is removed, not throttled | holds | S189:174-177 `if (QUEUESIZE >= MAX_QUEUED_EVENTS) { … it = removeClientByFD(…)` |
| 10 | 31 | Quote of the overflow log call | holds (verbatim) | S189:175 |
| 11 | 33-35 | Partial writes resume via `writeOffset`; EAGAIN/EWOULDBLOCK leaves the event queued; EINTR retries | holds | S189:136-146, :149-150, :152-153 |
| 12 | 35-36 | Any other write failure logs "Socket2 fd {} failed writing event" and ends the client | holds in code; the log half fails on this host | S189:155-156 then :108-109 / :182-183 remove. A zero-byte write also counts as failure (:155 "write returned 0"). The log call is a no-op here: S214:15-16 `if (!m_logsEnabled) return;` with disable_logs=1 |
| 13 | 38-39 | During shutdown, events are dropped with a warning instead of delivered | holds (warning also suppressed here) | S189:164-166 `m_isShuttingDown` → WARN "Suppressed (shutting down)…" + `return`; S214:15-16 |
| 14 | 43-44 | The compositor drops a stalled client after 64 queued events | holds with qualification | S189:174. The queue only grows when `write` returns EAGAIN (:149-150); events written successfully leave it (:144-146). So "stalled" means the kernel socket buffer is already full; 64 more events then cause removal on the 65th post |
| 15 | 44-46 | A blocked custom-module producer can therefore cost the bar its whole compositor-event feed | unverifiable / no support in bytes | S201:48 the event reader is a **dedicated thread** (`ipcThread_ = std::thread(…socketListener…)`). No receipt shows a custom-module path that blocks it. The only coupling in the bytes is `callbackMutex_` (S201:143) plus handler `onEvent`, which is not a custom-module path |
| 16 | 46 | …including the `hyprland/workspaces` element | holds (given removal) | S212:804-815 workspaces registers on the one `m_ipc` reader; host waybar config names `hyprland/workspaces` (rg count 10 across config files) |
| 17 | 46-47 | …with no error shown to the user | holds (bar side) | After removal the bar's `fgets` returns NULL and the loop sleeps 1 ms and continues forever: S201:117-122. No reconnect, no error log in these bytes. [INFERENCE] fd close on erase relies on Hyprutils `CFileDescriptor` RAII, not in the receipts |
| 18 | 47 | …because the failure is logged compositor-side, not in the bar | **wrong on this host** | S214:15-16 + :48 `m_logsEnabled = !*PDISABLELOGS`; getoption disable_logs int 1 → nothing is logged |
| 19 | 47-48 | Basis: queue cap, removal log, twelve subscriptions in S214 | holds (twelve unconditional) | S212:804-815 = 12 `registerForIPC`; two more are conditional (S212:821 `windowtitlev2`, :823ff `activewindowv2`); 15 call sites in the file |
| 20 | 50-51 | The Waybar backend reads at most 1024 bytes per event | **wrong** | S201:115-117 `std::array<char,1024>`, `fgets(buffer.data(), buffer.size(), file)` → at most **1023** chars per call. A longer line is split; the tail is parsed as a separate message (S201:124-129, :142) |
| 21 | 51-52 | …matching the compositor's own 1024-character truncation of event data | **wrong** | S189:128 truncates **data** to 1024, but the line is `event>>data\n` (`std::format("{}>>{}\n", …)`), up to len(event)+2+1024+1 bytes > 1023. The Waybar comment at S201:115 ("max 1024 bytes") is the source of the error |
| 22 | 54-55 | Whether the cap was ever reached is unknown; no log was read | holds (still unknown, now by construction) | S213 receipt + S214:15-16: the log channel cannot answer it while disable_logs=1 |

## 2. event-queue-host-measurement-r28.md

| # | line | sentence (abridged) | verdict | deciding evidence |
|---|---|---|---|---|
| 1 | 3-5 | Amends r26 §2, whose open item was whether the 64-event cap had been reached | holds | r26 lines 41-55: the UNK at :54 sits under §2 |
| 2 | 7 | `source: S226 — /run/user/1000/hypr/efb50993…_1792772698_564628331/hyprland.log` | unverifiable now / artefact gone | `stat` → ENOENT; `/run/user/1000/hypr/` holds only `…_1792804449_…`; that instance started 2026-10-24T01:14:09Z, after the 2026-10-23 22:14 local boot. [INFERENCE] tmpfs runtime dir cleared at reboot |
| 3 | 13-16 | Merge note: add "wave-2 row S187 (event manager)" | inconsistent | r26 :13 calls the same row **wave-1** S187; the package holds no S187 row (grep empty); lane equivalent is S189 |
| 4 | 20-22 | The log exists at `<HIS>/hyprland.log`: 942 548 B, 6 425 lines, mtime 2026-10-23T19:23 | unverifiable | File gone (ENOENT). Only plausibility: instance epoch 1792772698 = 2026-10-23T16:24:58Z precedes the stated mtime. The mtime carries no zone |
| 5 | 24-25 | Zero "overflowed event queue", "failed writing event" and "Socket2 fd" | unverifiable (that file); same zeros hold in the current log | Current log: 0 / 0 / 0, and also 0 for "Socket2" |
| 6 | 27-28 | Within this log window the compositor never hit its cap and no socket2 write failed | **wrong as inference** | getoption disable_logs int 1, `set:false`; no config line sets it (rg rc=1), so it is Hyprland's default here. S214:15-16 means the core logger writes nothing. Live falsifier: `ss` shows 2 established socket2 clients (waybar, socat) on Hyprland's side, yet the current log has **0** "Socket2 accepted" lines (S189:85 logs every accept). The log does not see socket2 at all. [INFERENCE] the same default applied on 2026-10-23 |
| 7 | 28-30 | The overflow path exists in the code but was not exercised on this host | exists = holds (S189:174-176); not exercised = **wrong as inference** | Same as row 6 |
| 8 | 34-35 | The markers are emitted only on failure; the overflow path logs "…overflowed event queue, removing" and removes the client | overflow clause holds; "only on failure" **wrong** for marker 3; all markers conditional on logging | S189:174-176 holds. But `Socket2 fd` also matches S189:100 DEBUG "Socket2 fd {} hung up" (a normal disconnect). All of them sit behind S214:15-16 |
| 9 | 37-38 | A zero is a negative observation about this window, not proof over history | first half **wrong** (not even a window observation); second half holds | S214:15-16; S213 "core_logger_lines … 21", last at line 21 |
| 10 | 38-39 | The log is per-session and rotates; basis: the instance-scoped runtime dir | per-session holds; "rotates" unverifiable | S214:29 `setOutputFile(std::string{IS} + … "/hyprland.log")`. S214:30 `setEnableRolling(true)` is the in-memory rolling buffer behind `hyprctl rollinglog` ([INFERENCE], Hyprutils not in receipts); no file rotation appears in the bytes. The current log has 27331 lines in one file |
| 11 | 41-43 | Earlier-session logs are not retained; only `lastNag` and `lastVersion` remain under `~/.local/share/hyprland/` | holds | `ls -1A ~/.local/share/hyprland/` → lastNag, lastVersion; `/run/user/1000/hypr/` → current instance only |

## 3. event-queue-journal-measurement-r29.md

| # | line | sentence (abridged) | verdict | deciding evidence |
|---|---|---|---|---|
| 1 | 3-5 | Amends r28, which measured only the current session's log file | holds | r28 source line :7 (single file) |
| 2 | 7 | `source: S242 — journalctl --user -u wayland-wm@hyprland.desktop.service` | holds (command exists, unit has output) | Ran it: 717 lines (`-q -o cat`) |
| 3 | 13-15 | Merge note: add the wave-3 log-file row beside this one | n/a (process) | — |
| 4 | 19-20 | Unit output holds 1091 lines (sha256 prefix `72b064bb2a4e5490`) | unverifiable / not reproducible | Now 717 lines `-q -o cat` (sha16 `43bf1f07176502bf`), 718 lines default (sha16 `4b89242bf4d87bb7`); S213 also 717. r29 did not record its flags. First retained unit entry is now 2026-10-23T12:39:20Z, so the retained window has moved since r29 |
| 5 | 20-21 | …with zero "overflowed event queue", "failed writing event" and "Socket2 fd" | holds (now) | Unit counts 0/0/0 (also 0 "Socket2") |
| 6 | 23-24 | A grep across the whole user journal returns zero of the first two markers | holds (now) | 168754 lines; 0 and 0 (also 0 "Socket2 fd", 0 "Socket2") |
| 7 | 26-27 | The 64-event queue never overflowed in retained history, and no socket2 write failed | **wrong as inference** | The journal is a null channel. S214:47 `setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT)` is false with disable_logs=1 and enable_stdout_logs=0 (getoption), and S214:15-16 returns first anyway. S213 probe: `"drm: getCurrentCRTC: No CRTC 0" in_log=7 in_unit_journal=0`. Stdout is on only before the config loads (S214:32 vs :47) |
| 8 | 27-29 | The journal spans sessions the per-session log does not | holds literally / adds no marker evidence | Unit's first entry 2026-10-23T12:39:20Z predates the current instance (2026-10-24T01:14:09Z). Spanning sessions does not help, because no core-logger line reaches the journal after config load (row 7) |
| 9 | 33-34 | The markers are emitted only on failure; the compositor logs the overflow and removes the client | as r28 #8 | S189:100 (DEBUG hang-up matches "Socket2 fd"); S189:174-176; S214:15-16 |
| 10 | 36-39 | The negative is bounded by retention; an unloaded host or rotated journal gives the same zero | holds but **omits the decisive confound** | With logging disabled (S214:15-16, :47), every host state gives zero, loaded or not |

## 4. The three package rows under the fleet schema

Schema: `CORPUS.md` § SOURCES.md (11 columns, "No `|` inside any cell", `opened` ISO date, `recheck` "ISO date or cadence (`90d`, `180d`, `on-release`)"). Validator: `scripts/sources-census.sh` E01 (NF≠13), E08 (opened), E09 (recheck must match `^[0-9]{4}-…$`, `^[0-9]+d$`, or symbolic `^[A-Za-z][A-Za-z0-9 _-]*$`, census line 582).

Method: a scratch copy of the lane registry with the three rows inserted after the last registry row, plus the lane's knowledge/lessons and the 4 package entries the rows' used-by names, at `/dev/shm/mado37-ScoutPkgSentences/scratch-shokunin`. Ran `scripts/sources-census.sh validate --today 2026-10-25`. The lane as-is gives W04 ×4 and `ok`. The rows' own findings:

```
scratch-shokunin	E09	S214 recheck=on-release — re-pull at tag `0.15.0` and compare sha256 (expect prefix `1e19d92638e7923f`) (ran 2026-10-23)
scratch-shokunin	E09	S226 recheck=on-log-rotation — re-read the log and re-count the three markers (ran 2026-10-23)
scratch-shokunin	E09	S242 recheck=on-log-rotation — re-read the unit's journal output and re-count the markers (ran 2026-10-23)
```

There was no E01 and no E08 for these rows. The other E11 lines in the scratch run name `tools/`, `SKILL.md` and `.ufo/` paths absent from the scratch copy; they are an artefact of the scratch, not of these rows.

| row | cells | `\|` in a cell | opened | recheck | other blockers | appendable as-is? |
|---|---|---|---|---|---|---|
| S214 (line 18) | 11 (12 raw pipes) | none | 2026-10-23 valid | **E09**: prose after `on-release` | (a) The id collides with the lane's round-37 **S214** = Logger.cpp (renumber-map); the document is lane S212. (b) Anchor `:804-821` "twelve event registrations" spans **13** `registerForIPC`; the twelve are :804-815. (c) used-by names `host-bar-and-idle-binding-r26.md`, which is not in the lane | **No** |
| S226 (line 30) | 11 | none | 2026-10-23 valid | **E09**: `on-log-rotation — …` (also no rotation exists; the log is per-instance) | (a) Artefact gone (ENOENT), so Rule 1 "write only after opening the source" cannot be met today. (b) The source cell starts `~//run/…` (malformed path). (c) The `teaches` cell asserts "never overflowed", which is wrong (§2 #6). (d) Tier A `own-work` claimed for a non-re-runnable read | **No** |
| S242 (line 46) | 11 | none | 2026-10-23 valid | **E09**: `on-log-rotation — …` | (a) Anchor "1091 lines, sha256 `72b064bb2a4e5490`" does not reproduce (717/718 now; flags unrecorded). (b) The `teaches` cell's conclusion is wrong: null channel (§3 #7). (c) Renumber-map already refuses it | **No** |

Under a symbolic-only rewrite (`on-release` / `on-session-change`), S214 would pass E09; it would still need the id moved to S212 and the anchor fixed to `:804-815`. S226 and S242 fail on content, not only form.

## Unknowns left open

- Whether `debug:disable_logs` was 1 on 2026-10-23, when r28/r29 measured. It is the default now and not set in `~/.config/hypr`; earlier state is [INFERENCE] only.
- Whether the bar's fd is closed on overflow removal. That depends on Hyprutils `CFileDescriptor` RAII, which is not in the receipts.
- `setEnableRolling` semantics. "In-memory rolling log" is [INFERENCE]; Hyprutils' CLI logger is not among the receipts.
- No receipt shows a mechanism by which a custom-module producer could block Waybar's IPC thread (r26 §2).
