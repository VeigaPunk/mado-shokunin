# ScribeE1 — re-grounded draft of `event-delivery-limits-r26.md` (mado round 37, wave 1)

**Verdict: PASS (draft delivered).** The draft is at
`.ufo/waves/round-37/w1/scratch/ScribeE1/event-delivery-limits-r26.md` (76 lines, sha256
`c49795a1921214e7aaf5471705fac12d572b49dc48b6bdd677e5164e45e677ea`). It has 26 tagged lines:
20 **OBS**, 5 **INF** and 1 **UNK**. No product file was written.

## Behaviour

- The header has the required shape, and lines 1–6 are `source:` S189, `source:` S201,
  `source:` S212, `verified-at: 2026-10-25`, `recheck: 90d` and `ground:`.
- Every body line under §1–§3 starts with a tag. Every **OBS** line names an S-id with
  file:line anchors.
- Each S-id has at least one verbatim quote of 25 words or fewer:
  - **S189:169**: `const size_t MAX_QUEUED_EVENTS = 64;` (5 words)
  - **S189:175**: the overflow log line (9 words)
  - **S201:115**: the 1024-byte buffer line, with two spaces before `//` (11 words)
  - **S212:804**: `m_ipc.registerForIPC("workspacev2", this);` (2 words)
- The package's §2 UNK is replaced by one **UNK** line. That line points to
  `event-queue-observability-r37.md` and says nothing else about the host.
- The `## Assimilation` note covers the package's origin and sha256, how the ids were
  renumbered, and what was kept, corrected, dropped and added.

## Commands and output relied on

- `sha256sum fetch/S189.bin fetch/S201.bin fetch/S212.bin` gave:
  - `eea605df…540d`
  - `799bf02f…4f9e`
  - `1e19d926…97d7e9`

  The S212 digest matches the renumber map.
- `wc -l` gave 192, 246 and 1154 lines.
- `cat -n fetch/S189.bin` and `cat -n fetch/S201.bin` were read in full. In S212 I read
  `sed -n 18,47p`, `120,140p`, `320,360p`, `383,396p`, `429,445p` and `795,835p`.
- `grep -n registerForIPC fetch/S212.bin` gave 15 hits:
  - `:37` is `unregisterForIPC`.
  - `:804`–`:815` are 12 unconditional subscriptions.
  - `:821` (`windowtitlev2`) and `:827` (`activewindowv2`) sit inside `if` blocks at `:817`
    and `:823`.
- Quote check with `grep -nF` (line, word count):

  | quote | line | words |
  |---|---|---|
  | `const size_t MAX_QUEUED_EVENTS = 64;` | 169 | 5 |
  | overflow log | 175 | 9 |
  | `failed writing event` log | 155 | 18 |
  | shutdown WARN | 165 | 12 |
  | S201 buffer line | 115 | 11 |
  | `fgets` | 117 | 6 |
  | `workspacev2` | 804 | 2 |
  | `windowtitlev2` | 821 | 2 |
  | `activewindowv2` | 827 | 2 |

- Inline snippets were confirmed with `grep -nF`:
  - S189: `"Socket2 fd {} hung up"` :100, `SOCK_CLOEXEC | SOCK_NONBLOCK` :14,73, `.socket2.sock` :21.
  - S212: `windowRewriteConfigUsesTitle() || m_taskbarWithTitle` :817,
    `'update-active-window' is set` :825, `m_ipc(IPC::inst())` :21, the `m_mutex` lock :326.
  - S201: `static IPC ipc;` :73, `ipcThread_ = std::thread` :48, `callbackMutex_` :143,157,166.
- `grep -n connect fetch/S201.bin` found socket2 `connect` only at :105. The other hit,
  :206, is socket1 in `getSocket1Reply`.
- Socket1 calls inside `Workspaces::` functions were mapped with awk:
  - `onWorkspaceCreated` (from :383): :393–394
  - `onWorkspaceMoved` (from :429): :433 and :442
  - `onMonitorFocused` (from :468): :480
  - `onWindowTitleEvent` (from :556): :590
  - `doUpdate` (:126) locks `m_mutex` at :127.
- I simulated counter clauses b, f and g (logic copied from `c1-r37-event-ground.py:129-157`)
  against the draft. Output:
  `ids ['S189', 'S201', 'S212'] verified True recheck ['recheck: 90d']`, each candidate quote
  `in_receipt True in_body True`, OBS lines naming the id S189=12, S201=8 and S212=5, both
  tokens `True True`, `untagged body lines []`, `OBS without S-id []`.

  This is a local simulation of three clauses only. Clauses a, c, d and e depend on the commit,
  `SOURCES.md`, the lesson Gate and the README. They were not run.

## Sentence ledger (package → draft)

| # | package sentence (short) | decision | deciding line |
|---|---|---|---|
| 1 | Title "What happens to an event client that stops reading" | kept | — |
| 2 | "Round: corpus-expansion-2, round 2 … no socket was connected and no event was observed" | corrected: now names round 37 and the three receipts with digests | `sha256sum` above |
| 3 | `source: S214 — …workspaces.cpp — § event registrations` | corrected: S214 → S212 (anchor `Workspaces::registerIpc`); S189 and S201 added from the merge note | renumber-map.md table rows 1–3; S212:803 |
| 4 | `verified-at: 2026-10-23` | corrected to 2026-10-25 | re-read this round |
| 5 | `recheck: 90d — re-pull … (ran 2026-10-23)` | corrected to `90d` with nothing else on the line | prompt shape |
| 6 | `ground: F1 — … arc-synthesis §6 U1` | corrected: §6 has no "U1" label, and "F1" there is the r3 hypridle finding. Re-pointed to the §6 row "waybar module text" and the README Frontier bullet | `arc-synthesis.md:290-305` (row `\| waybar module text \|`; `F1` occurs only as "r3 F1"); `corpus/README.md:98-100` |
| 7 | Merge note about adding S187/S188 | folded into the `source:` lines (S189, S201) | renumber-map.md |
| 8 | "The lane's event socket hands each connected client its own queue" | corrected: it is the compositor's socket2, not "the lane's". Each `SClient` has its own `events` queue, and the formatted string is shared | S189:21, :89-93, :170, :180 |
| 9 | "the compositor writes to that client from its own event loop" | corrected: `postEvent` writes immediately. Leftovers are flushed on `WL_EVENT_WRITABLE` from the event-loop source | S189:180-188, :88, :105-109 |
| 10 | "The cap is explicit in the host's v0.56.2 event manager … `MAX_QUEUED_EVENTS = 64`" | kept (quote). "host's" was dropped: host facts belong to the observability entry, and v0.56.2 stays on the `source:` line per SOURCES row S189 | S189:169; `corpus/SOURCES.md:201` |
| 11 | "A client whose queue is at or over the cap is removed, not throttled" + log quote | kept and made exact: the check runs per posted event, before queueing, and the triggering event is not queued | S189:172-177 |
| 12 | "Partial writes are resumed … `writeOffset` … `EAGAIN`/`EWOULDBLOCK` … `EINTR` retries" | kept | S189:136-146, :149-150, :152-153 |
| 13 | "Any other write failure logs 'Socket2 fd {} failed writing event' and ends the client" | kept and widened: `write` returning 0 also counts, the full format string is given, and both removal sites are cited | S189:155-156, :108-109, :182-183 |
| 14 | "While the compositor is shutting down, events are dropped with a warning" | kept (WARN format quoted) | S189:164-166 |
| 15 | INF "compositor's answer to a stalled client is to drop it after 64 queued events" | kept and made exact: removal happens when the next event finds 64 queued, counted after the kernel buffer | S189:149-150, :172-177 |
| 16 | INF "A blocked custom-module producer can therefore cost the bar its whole compositor-event feed" | **dropped** (the trigger). None of the three files contains custom-module code. Replaced by the stall routes the bytes do show: handlers run synchronously on the single reader thread, `m_mutex` is shared with the UI thread's `doUpdate`, there are socket1 round trips inside handlers, and the reader sleeps 1 ms per line | S201:129, :136, :143-148; S212:126-127, :326, :393-394, :433, :442, :480, :590 |
| 17 | "— including the `hyprland/workspaces` element —" | kept: one `IPC` singleton serves every handler | S201:72-75; S212:21 |
| 18 | "with no error shown to the user, because the failure is logged compositor-side, not in the bar" | corrected to what the bytes show: the bar's EOF path logs nothing and never reconnects, and the only record in these bytes is the compositor ERR line. Whether that line reaches the host is left to the pointer | S201:105, :119-121; S189:175 |
| 19 | "together with the twelve event subscriptions in S214" | **corrected**: 12 unconditional + 2 conditional = 12 to 14 | S212:804-815, :817-821, :823-827 |
| 20 | OBS "the Waybar backend reads at most 1024 bytes per event" | corrected: the buffer is 1024 bytes and `fgets` returns at most 1023 per read. The 1023 is C library semantics, so it is tagged INF | S201:115, :117 |
| 21 | "matching the compositor's own 1024-character truncation of event data" | **corrected (contradicted)**: S189 caps the *data* at 1024, and the framed line adds the event name, `>>` and `\n`. The sizes do not match, so long lines split | S189:128; S201:115-117, :124-125, :142-147 |
| 22 | UNK "Whether the host's compositor ever reached that cap is unknown — no log was read" | replaced by the pointer to `event-queue-observability-r37.md`, with nothing else about the host | prompt |

Additions taken from the same bytes, labelled in `## Assimilation`:

- non-blocking accepted sockets (S189:73)
- removal on hang-up (S189:99-102)
- data cut to 1024 before framing (S189:128)
- an INF that removal closes the fd via `CFileDescriptor` ownership (S189:73, :90, :123); the
  destructor is not in these bytes
- one thread and no reconnect (S201:48, :105)
- silent null `fgets` (S201:119-122)

## Cross-checks against sibling reports (read, not re-run)

- **`w1/reports/ScoutWaybarDrop.md` Q4** marks the custom-module trigger "CONTRADICTED as a
  direct mechanism by these bytes; indirect routes UNDETERMINED". It marks the feed-loss and
  bar-side silence clauses "HOLDS".
  - This agrees with ledger rows 16–18.
  - Its custom.cpp evidence is outside S189/S201/S212, so the draft only drops the trigger and
    does not cite custom.cpp.
- **`w1/reports/ScoutS189.md` §2** says that removal comes "at the 65th post", after the kernel
  send buffer is full. This agrees with ledger rows 11 and 15.
  - Its host `wmem_default` figure is a host fact, so it was left out under the pointer-only
    rule.
  - Its "'Logged compositor-side' is **false on this host**" is consistent with the draft, which
    makes no host-logging claim.
- No conflict found.

## Coordination

- I messaged `L1Mado37-2.ScribeLessonGate` with the exact quotes the draft carries for S189,
  S201 and S212, so its `GATE` lines can match clause g.
- **It replied.** Its draft GATE quotes are:
  - S189: `const size_t MAX_QUEUED_EVENTS = 64;` and `Socket2 fd {} overflowed event queue, removing`
  - S201: the buffer line, with two spaces before `//`
  - S212: `m_ipc.registerForIPC("workspacev2", this);`
- `grep -cF` on the draft finds each of the four exactly once, so the two drafts agree. I sent
  that confirmation back.
- If a Gate quote changes later, the body must carry the new quote verbatim, or clause g fails
  for that id.

## Out of scope / for the L1

- Clause c needs the `used-by` cells of S189, S201 and S212 to list
  `corpus/knowledge/event-delivery-limits-r26.md`.
  - `w1/reports/ScribeRows.md:26-27` shows S189 and S201 extended.
  - I did not check the S212 row.
- Clause e needs the README Coverage map row (ScribeReadme).
- The draft must be copied to `LANE/corpus/knowledge/event-delivery-limits-r26.md` by the
  committing seat. I wrote nothing under `corpus/`.
- The counter itself was not run. It needs a commit.

## Touched surfaces

- Written:
  - `.ufo/waves/round-37/w1/scratch/ScribeE1/event-delivery-limits-r26.md`
  - this report
  - one peer message
- Read only: the package entry, renumber-map.md, registration.md, c1 counter, fetch receipts,
  `corpus/knowledge/{ipc-contract-r25,workspace-rules-r27,waybar-module-text-route-r25,arc-synthesis}.md`,
  `corpus/README.md`, `corpus/SOURCES.md` (rows S189, S201), sibling prompts and reports.
- No socket connection, no `hyprctl`, no git or jj command in LANE.
- Tools installed or updated: none.
