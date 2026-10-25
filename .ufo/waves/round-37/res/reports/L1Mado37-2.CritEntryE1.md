# CritEntryE1 — residual falsify of `corpus/knowledge/event-delivery-limits-r26.md` at 3f424257a1ea69cd2655770259ba00b423293f4f

Seat: L1Mado37-2.CritEntryE1 (critic, read-only). Target: the landed corpus entry
`mado-shokunin/corpus/knowledge/event-delivery-limits-r26.md` (HEAD = 3f424257a1ea69cd2655770259ba00b423293f4f, verified by `git rev-parse HEAD`).
Ground truth: `.ufo/waves/round-37/fetch/{S189,S201,S212}.bin` (sha256 computed here:
S189 `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`,
S201 `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e`,
S212 `1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9` — same hexes
recorded in `corpus/lessons/round-37.md` `## Gate`, line 18; `RevCollisions.md`; scratch only
under `/dev/shm/mado37-L1Mado37-2.CritEntryE1/`). No tool installed. No socket, no hyprctl
mutation, no lane write; the only file created is this report.

## Method
Sentence-by-sentence check of every numbered claim in the entry against the actual bytes,
line by line of the three bins. Each `:N` cite was resolved on the bin itself (not assumed).
The entry is 85 lines; every factual sentence was mapped to at least one byte pointer.

## Sentence verdicts

### Header (lines 3–12)
| Entry cite | Claim | Verdict | Basis |
|---|---|---|---|
| :3 | S189 = Hyprland v0.56.2 `src/managers/EventManager.cpp` @ `efb50993…`; S201 = Waybar 0.15.0 `src/modules/hyprland/backend.cpp`; S212 = Waybar 0.15.0 `src/modules/hyprland/workspaces.cpp` | PASS | Bin identities confirmed by wave-1 re-fetch + `cmp` (ScoutS189 §0, ScoutWaybarDrop §0, RevCollisions); host `hyprctl version` = v0.56.2 @ efb50993 (ScoutS189). |
| :10-11 | Receipts S189/S201/S212, digests in round-37 lesson `## Gate` | PASS | `corpus/lessons/round-37.md:18` `## Gate` contains `eea605df` (×2) and `1e19d926`; full hex matches my `sha256sum` above. |
| :9, :11-12 | Read-only process claims; host runs same compositor commit and Waybar 0.15.0-3 | PASS | Corroborated by ScoutS189/ScoutWaybarDrop (read-only seats, `pacman -Q`). |

### §1 S189 (lines 16–42)
| Entry cite | Claim | Verdict | Basis |
|---|---|---|---|
| :16-19 | `socket(AF_UNIX, SOCK_STREAM\|SOCK_CLOEXEC\|SOCK_NONBLOCK, 0)` at :14; `listen(…,10)` at :35; `accept4(…, SOCK_CLOEXEC\|SOCK_NONBLOCK)` at :73; compositor never reads from a client | PASS | S189:14, :35, :73 verbatim (quotes below). No `read`/`recv` anywhere in the 192-line file; accepted fds registered with wl mask 0 (:88) — no READABLE interest. |
| :21-22 | Per-client queue; cap counts events not bytes, at :169 `const size_t MAX_QUEUED_EVENTS = 64;` | PASS | S189:169 verbatim; `it->events.size()` (:172) vs 64. |
| :24-28 | Cap checked only on post (:172-177); ≥64 queued → log `Socket2 fd {} overflowed event queue, removing` (:175), remove (:176), new event not queued; else append+flush (:180-182); arm WRITABLE when queue was empty before (:187-188) | PASS | S189:172 `QUEUESIZE = it->events.size()`, :174 `>= MAX_QUEUED_EVENTS`, :175 log, :176 `removeClientByFD`, :180 `push_back`, :182 `flushClient`, :187-188 `!it->events.empty() && QUEUESIZE == 0` → `wl_event_source_fd_update(…WL_EVENT_WRITABLE)`. Removal precedes push, so the triggering event is not queued (correct). |
| :30-33 | `flushClient` (:133-161): writeOffset resume (:136-144); EAGAIN/EWOULDBLOCK keeps queued (:149-150); EINTR retries (:152-153); zero-byte write or other error logs `Socket2 fd {} failed writing event: {}` (:155), client removed | PASS | S189:133-161 verbatim; :149 `return true` without erasing; :152-153 `continue`; :155 `"write returned 0"`/strerror branch, :156 `return false` → caller removes (:108-109/:182-183). |
| :35-37 | Shutdown → dropped with WARN (:164-166); data cut to 1024 bytes before framing; framed line = `EVENT>>` + ≤1024 bytes + `\n` (:128) | PASS | S189:164-166 `m_isShuttingDown` → WARN + `return`; :128 `std::format("{}>>{}\n", event.event, data.substr(0, 1024))`. |
| :39-42 (**INF**) | Removal needs send buffer full first (until then every write succeeds and nothing queues), then 64 more posted events; slow client tolerated long; stopped client removed after buffer+64 events; buffer size not measured | PASS (INF, correctly labeled) | Derives from :149-150/:139-147 (queue grows only when `write` cannot complete) + :174-177 (removal at 64 queued). The count is precise: the post that leaves the first event queued is followed by exactly 64 further posts; removal occurs at the post that finds 64 queued (65th total). "Its buffer + 64 events" = 64 events queued at removal. Buffer size honestly flagged unmeasured. No OBS mislabel. |

### §2 S201/S212 (lines 46–64)
| Entry cite | Claim | Verdict | Basis |
|---|---|---|---|
| :46-48 | workspaces registers twelve events unconditionally (:804-815, starting `m_ipc.registerForIPC("workspacev2", this);`); two more only under config (`windowtitlev2` :821, `activewindowv2` :827) | PASS | S212:804-815 = exactly 12 registerForIPC calls, no guard; :817-822 `windowRewriteConfigUsesTitle() || m_taskbarWithTitle` gates `windowtitlev2`; :823-828 `m_updateActiveWindow` gates `activewindowv2`. |
| :50-54 | fgets into `std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes` (:115-117); comment wrong vs S189 :128; fgets returns ≤1023 chars; long event → truncated head + tail parsed as separate message | PASS | S201:115 (two spaces before `//` — byte-exact), :117 `fgets(buffer.data(), buffer.size(), file)`. S189:128 max line = name+2+1024+1 > 1023 (data-capped line is always >1023). fgets stores ≤1023 chars + NUL; no newline in the first chunk ⇒ one line arrives as ≥2 `fgets` calls, each parsed by :124-129 (head parsed with truncated payload; tail parsed as its own message). Replica-confirmed in ScoutWaybarDrop Q2. |
| :56-58 | Connects once (:105); on `fgets` null sleeps 1 ms and loops (:119-122) — no reconnect, no log, no exit; sleeps 1 ms after every event (:136) | PASS | S201:105 single `connect`; :119-122 `if (receivedCharPtr == nullptr) { sleep(1ms); continue; }`; no `feof`/`ferror`, no retry, no break; loop exits only on `running_` (set false in `~IPC` only); :136 unconditional `sleep_for(1ms)`. |
| :60-64 (**INF**) | After compositor removal the bar keeps running with no feed, no error; only restart reconnects; module handlers run on listener thread (backend.cpp:129,143-147); a slow handler — not a slow custom-module producer (own thread) — can stop reading | PASS (INF, correctly labeled) | S201:129 `parseIPC` inline in `socketListener`; :143-147 `handler->onEvent(ev)` on that thread under `callbackMutex_`. Custom-module producer runs on its own worker thread (`continuousWorker`, custom.cpp:69/73/81) per wave-1 ScoutWaybarDrop Q3-Q4; that report also verified the EOF poll-loop replica. Both directions grounded in wave-1 bytes. |

### §3 and Assimilation (lines 66–85)
| Entry cite | Claim | Verdict | Basis |
|---|---|---|---|
| :66-68 | UNK: bytes absorbed before queueing; SIGPIPE handling; `removeClientByFD` close mechanics (hyprutils outside these bytes) | PASS | All three are genuinely outside S189/S201/S212 (fd close = hyprutils RAII, SIGPIPE = process-level, byte budget = unmeasured) — correctly left UNK, not asserted. |
| :72-73 | On this host compositor log lines (both markers) are not written at all → see `event-queue-observability-r37.md` | PASS | `debug:disable_logs`=1 on host (ScoutS189 §0) ⇒ `CLogger::log` early-returns before rolling feed (S214:15-16, :48); live log grep `Socket2` = 0 (ScoutS189 §7). |
| :77-84 | Assimilation: kept/corrected/dropped items | PASS | Each "corrected" claim matches the byte findings (source-id remap per renumber-map; 1023-char read vs 1024-byte data cut; send-buffer-first; log suppression; custom-module trigger dropped). |

## Findings

- **F1 (severity: none)** — No INF stated as OBS. Every `**OBS**` block resolves to verbatim bytes (or, for the fgets-split and never-read claims, to deterministic stdio/wl semantics corroborated by the wave-1 replica). Every runtime extrapolation is explicitly `**INF**` or `**UNK**` with honest hedging (buffer size unmeasured; SIGPIPE outside bytes).
- **F2 (severity: none)** — No line-number misses. All 21 cited ranges (`S189:14,35,73,128,133-161,136-144,149-150,152-153,155,164-166,169,172-177,175,176,180-182,187-188`; `S201:105,115-117,119-122,129,136,143-147`; `S212:804-815,821,827`) resolve exactly on the bins.
- **F3 (severity: LOW, informational)** — Removal-timing INF (lines 39-42): wording "then 64 more posted events" is precise only if read as *64 further posts after the first event is left queued*; the removal itself happens at the post that finds 64 queued (the 65th after the buffer first fills). The sentence "removed after its buffer plus 64 events" matches the 64-queued-at-removal reading, so no factual error; the smallest tightening is: "…then 64 events queue; the post that finds 64 queued removes the client." Optional, non-blocking.
- **F4 (severity: LOW, informational)** — 1023-character-split OBS (line 54) rests on stdio `fgets` semantics plus `:128` framing (it is the only OBS that is a *consequence* rather than a literal byte). It is replica-confirmed (ScoutWaybarDrop Q2, lines 4-5) and matches `fgets` contract; no correction needed, but the entry could label it "OBS (derived, replica-verified)" for strictness.
- **F5 (severity: none)** — The four named overreach candidates all hold: removal-timing INF (supported, F3 nuance only), 1023-character split (supported), never-reconnect claim (supported: single `connect`, null-branch sleeps forever, exit only at teardown), handler-thread claim (supported: `parseIPC`/`onEvent` on listener thread; custom-module producer on its own thread).

## Verdict
Every sentence passes against S189/S201/S212 bytes. No FAIL items. Two LOW/informational wording notes (F3, F4) with optional smallest corrections; nothing that requires an edit of the landed entry.

## Commands / pointers
- `git rev-parse HEAD` → 3f424257a1ea69cd2655770259ba00b423293f4f
- `sha256sum fetch/S189.bin fetch/S201.bin fetch/S212.bin` → hexes above (= lesson `## Gate` + RevCollisions)
- Bin lines quoted in verdicts: `S189.bin:14,35,73,128,133-161,172-177,187-188`; `S201.bin:115,117,119-122,129,143-147`; `S212.bin:804-815,821,827`
- Supporting wave-1 reports: `w1/reports/ScoutS189.md`, `w1/reports/ScoutWaybarDrop.md`, `w1/reports/RevCollisions.md`, `w1/reports/ScribeLessonGate.md`
