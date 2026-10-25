# L1Mado37-2.CritRefusals — round-37 data commit `3f424257a1ea69cd2655770259ba00b423293f4f`: Assimilation attack

Role: UFO-FSD critic (leaf; read-only on lane files). Verdict per item with command pointers.
No tool installed (no need); scratch `/dev/shm/mado37-L1Mado37-2.CritRefusals/`.

## 0. Grounding of the reviewed text

- The lane is jj; the commit is `3f424257…` = `master` (`jj log --no-graph --limit 8`: `sotvlqzy … master 3f424257`). Working copy above it is clean: `jj --ignore-working-copy diff --stat` → `0 files changed`. So the lesson/registry/assimilation files in the tree ARE the committed data.
- `jj file show -r 3f424257… root:corpus/lessons/round-37.md` reproduces the working-tree lesson verbatim (its `## Gate`/`### Assimilation` table is the object of review).
- Path note: the assignment's `/home/vgpnk/Projects/shokunin/merge/mado/…` does not exist; the package root is `/home/vgpnk/Projects/shokuknow/merge/mado/` (the lesson itself writes `shokuknow`). Used the existing path.

## 1. r28/r29 refusals — does the reason hold on this host? **PASS**

Reason as written (lesson `### Assimilation` table + `## Mistakes` M37-2): r28/r29 read a *zero marker count* as "never overflowed", but the markers are core-logger lines and on this host `debug:disable_logs` is 1 (shipped default), so the core logger returns before formatting/writing → the log and the unit journal are null channels for the class; r28's own source instance no longer exists.

Evidence the reason holds, this host, now:

- Live option: `hyprctl getoption debug:disable_logs -j` → `{"option": "debug:disable_logs", "int": 1, "set": false }` (read verb; matches Gate S213 quote and `fetch/S213.receipt.txt:28`).
- Default in code: `fetch/S215.bin:629` → `MS<Bool>("debug:disable_logs", "disable logging to a file", true),`; `:632` → `debug:enable_stdout_logs` default `false`.
- Gate code: `fetch/S217.bin:22-24` → the formatted `log(...)` overload's first statement is `if (!m_logsEnabled) return;` **before** `std::format` (returns before formatting); `fetch/S214.bin:14-16` → non-formatted `CLogger::log` returns before rolling-log/file/stdout; `:47` → `m_logger.setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT);`; `:48` → `m_logsEnabled = !*PDISABLELOGS;`.
- Markers are core-logger calls: `fetch/S189.bin:175` (`Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", …)`) and `:155` (`"Socket2 fd {} failed writing event: {}"`).
- Re-measured live (2026-10-25, unchanged log): `/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/hyprland.log` (4,259,033 B) → `overflowed event queue` 0, `failed writing event` 0, `Socket2 fd` 0; core-logger lines (prefix `LEVEL ]`) = 21, last at line 21; probe `drm: getCurrentCRTC: No CRTC 0` = 7 in the log, 0 in the unit journal (`journalctl --user -u wayland-wm@hyprland.desktop.service -q -o cat`, 717 lines, markers 0/0/0). Numerical claims of `S213.receipt.txt` reproduce exactly.
- r28's source instance `…_1792772698_564628331` is gone: `/run/user/1000/hypr/` now holds only `efb50993…_1792804449_426444678` (also `hyprctl instances`; host `v0.56.2 efb50993…`).

No counterexample found: a zero on these channels is structurally uninformative, and the refusal targets exactly that inferential leap (r28/r29's own §2 caveats don't cure it). Flip conditions are coherent.

## 2. Admitted r26 is the package entry re-grounded **PASS**

Sources: package `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/event-delivery-limits-r26.md` (read-only) vs lane `corpus/knowledge/event-delivery-limits-r26.md` (committed).

- Origin declared: lane entry `## Assimilation` names the package path and states "every sentence was re-checked against the re-fetched bytes".
- Corrections claimed (five) match the diff: (1) source ids S187/S188/S214 → S189/S201/S212 by document; (2) "matching … 1024-character truncation" corrected (framed line exceeds 1024 B; `fgets` reads ≤1023 chars); (3) "dropped after 64 queued events" corrected (kernel send buffer fills first); (4) "failure is logged compositor-side" corrected (not on a default install); (5) trigger corrected (module handler on the listener thread, not a custom-module producer). Package's host-side `UNK` dropped, replaced by §3 pointer to `event-queue-observability-r37.md`.
- Every new anchor verified against `fetch/` bytes: S189 `:14` (AF_UNIX SOCK_STREAM|CLOEXEC|NONBLOCK), `:35` (`listen(…, 10)`), `:73` (`accept4` nonblock), `:128` (framing/1024 cut), `:133-161` (`flushClient`, `writeOffset` resume, EAGAIN/EWOULDBLOCK `:149-150`, EINTR `:152-153`, error log `:155`), `:163-167` (shutdown drop), `:169` cap, `:172-177` check/log/remove, `:187-188` write-interest arm; S212 `:804-815` (twelve unconditional registrations), `:821`/`:827` (conditional windowtitlev2/activewindowv2); S201 `:105` (connect once), `:115-117` (1024 array + `fgets`), `:119-122` (1 ms sleep loop), `:136` (sleep after event).
- Gate honesty: `sha256sum` of `S189.bin` = round-32 fetch `eea605df…`, `S201.bin` = round-34 fetch `799bf02f…` (byte-identical claims true).

This is a substantive re-grounding, not a relabel.

## 3. Ids re-pointed by document **PASS**

`assimilation/renumber-map.md` maps by URL/artefact, never arithmetic: staged `S214` (workspaces.cpp) → lane `S212` (new, sha `1e19d926…` = package anchor prefix); merge-note "wave-1 S187" (EventManager.cpp) → `S189` (held); "wave-1 S188" (backend.cpp) → `S201` (held); staged `S226`/`S242` (host log/journal) refused. Committed registry confirms: `S189` = EventManager.cpp `efb50993…` (sha prefix `eea605df…` — same document as package staged S206), `S201` = backend.cpp, `S212` = workspaces.cpp. The lane entry's `source:` line cites exactly these three.

## 4. Any staged row appended as-is? **PASS**

Parsed all 147 staged rows (`merge/mado/SOURCES.append.md`) vs the 207 registry rows at the commit (id + source from `| S### |` rows):

- Same-id identical content: **none** (`[]`).
- Id collisions at the commit: 15 (S203–S217); every pair differs in content; at base `b4e47e9` the registry has 201 rows and the intersection is exactly 9 (S203–S211), matching the lesson.
- URL overlaps all map to *different* registry ids: staged S203→reg S186, S204→S187, S205→S188, S206→S189, S207→S201, S208→S202, S213→S196, S214→S212, S276→S187 — i.e. staged rows are duplicates of already-held documents under older ids or the rewritten new row; no verbatim append.
- Guard proof reproduces: `reg-ids`/`staged-ids`/`collisions` fixtures show the 0–3-space pattern catches the indented `  | S002 |` scratch row (collision `S002`, n=1) while the column-zero pattern misses it (n=0) — the declared guard is live.

## 5. Lesson records ≥1 admit and ≥1 reject **PASS**

`round-37.md` `### Assimilation` table: `event-delivery-limits-r26.md` → **admit**; `event-queue-host-measurement-r28.md` and `event-queue-journal-measurement-r29.md` → **refuse** (with flip rows). Both sides present, with reasons.

## 6. Quarantine verdict for register row S189 **PASS**

- Register (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:141`): `mado | round1 | S189 | payload-absent | …EventManager.cpp | auto eventString = std::format(\"{}>>{}\\n\", …)`.
- Lesson & renumber-map verdict: **present** at `:128`; the register's escaped `\"`/`\\n` form is why its checker found nothing.
- Verified: `fetch/S189.bin:128` is verbatim `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` — the register's quote matches modulo JSON escaping. The other twelve slice rows name documents no admitted entry cites (S213/serialized receipt and renumber-map list them; none is cited by the admitted entries) — "unappended and unchecked" is consistent.

## Bottom line

No counterexample survived. All six items PASS. The r28/r29 refusals hold on this host *now* (live option 1, null channels re-measured, old instance gone); the r26 admission is a genuine re-grounding with all anchors traceable to fetched bytes; ids follow documents; no staged row was appended as-is; the lesson records both an admit and rejects; and the S189 quarantine verdict (present at `:128`, register escaped-form false negative) is confirmed.

Findings (severity: info): assignment path `…/shokunin/merge/mado/…` does not exist (actual: `…/shokuknow/merge/mado/`); r28's old-instance artefact is now unrecoverable, but the refusal does not rest on it.
