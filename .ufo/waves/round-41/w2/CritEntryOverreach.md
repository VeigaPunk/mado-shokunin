# CritEntryOverreach — report (round 41, w2)

Status: complete. Seat directory: `.ufo/waves/round-41/w2/CritEntryOverreach/` (full evidence in `overreach.md`).
Target: `corpus/knowledge/hyprland-focus-grab-r41.md` at DATA `07f2641696b5ac73de1404ea737a9f27e9819aa1` (worktree has no diff for the entry or `corpus/SOURCES.md`).
Axis attacked: statements that are stronger than the weakest reading of their receipts. All findings below are DATA defects (entry text, fixed before the round lands); two also expose C2 predicate gaps. No lane file was edited.

## Verdict

The quotes are faithful except one (F3), but **seven statements outrun them**, and the two most serious are on the host census: the latest journal session is **not** a whole advertisement (F1), and the first session is from a **different boot** (F6). Two request counts are also wrong (F2).

## Findings (entry line at the data commit → one-line repair)

| # | Sev | Entry line | What is stronger than the quote | Smallest safe repair | Class |
|---|---|---|---|---|---|
| F1 | HIGH | L67 INF "Only the second session is a whole advertisement ... 63 distinct names" | Portal PID 1952 is alive since 13:36:24; the live unit journal is byte-identical to the receipt 7h23m later (`diff` → IDENTICAL); the latest session has no `wl_output` and no `zwp_linux_dmabuf_v1` advert although the same portal logged both on the previous boot (:8-9,26,...) and its own `onGlobal` binds them (`xdph-PortalManager.cpp:113-117,122-129`); `card1-DP-1` is connected. The log ends mid-enumeration → 63 is a lower bound. | Rewrite L67 as a lower bound; keep census L63 byte-identical (clause h pins it). | DATA + predicate gap (`journal_counts` has no completeness test) |
| F2 | HIGH | L115 "two interfaces, five requests, one event" | XML has six `<request>` elements (`grep -c` → 6); §1 and the table list six. S283 row says "four requests" — a third count. | L115 → six; row S283 → "six requests (two manager, four grab)". | DATA |
| F3 | HIGH | L49 quote "if (anyCommitted) start(); else finish(true);" | The quote is a substring of the real block and drops `if (surfacesChanged)`, which the next clause ("only a change of the set") silently relies on. | Quote `if (surfacesChanged) { if (anyCommitted) start(); else finish(true); }`. | DATA + predicate gap (clause d checks only Gate quotes, by substring) |
| F4 | MED | L49 "a commit promotes additions into the seat grab" | False for `commit(true)` from `eraseSurface` (`if (!removeOnly)` at :123-129). | "a normal commit promotes; the destroy-path commit(true) only erases removals." | DATA |
| F5 | MED | L73 "the running unit [is] the same upstream release" | The S037 receipt's own note says pkgrel 2 covers v1.4.1 only if packaging left the source untouched, "which this receipt does not establish". The receipt proves installed 1.4.1-2 and (`/proc/1952/exe` + package `files:9` + unit `ExecStart`) the running binary, not source identity. | Split into "installed 1.4.1-2 + running binary is that package's file; packaging effect on source not established." | DATA |
| F6 | MED | L67 "its 15 adverts are a lower bound" | `-- Boot` at :78 is a boot transition (`--list-boots`: boot -1 ends 13:35:34, boot 0 starts 13:36:22), so session 1 is the previous boot's portal — not a lower bound for this registry. | "a slice of the previous boot's session; not comparable with the current registry." | DATA |
| F7 | MED | L55 INF "enforced at the seat, not at the rule layer" | The receipt installs a `CSeatGrab` and reads no rule; the seat's filtering is L57's own UNK; `rawSurfaceFocus` constraints are not in the receipt. | "installed as the seat's grab; this file reads no rule; `CSeatGrab` filtering unread (UNK)." | DATA |
| F8 | MED | L37 "the client controls only membership" | The client also controls commit timing (which starts/ends the grab) and the grab's lifetime. | "no request names a focus target; the client controls the set, the commit timing, and the grab's lifetime." | DATA |
| F9 | LOW-MED | L71 / L120 "the portal does not use it" | Evidence is one file (`PortalManager.cpp`) + the journal; L135 already scopes it to that file. | "`PortalManager.cpp` logs it and has no branch for it"; L120 question → "Does `PortalManager.cpp` bind it?" | DATA |
| F10 | LOW-MED | L51 "treats ... as a bug rather than a state" | The code logs `LOGM(Log::ERR, ...)` and returns; no clear, no client error. | "logs an ERR assertion and returns." | DATA |
| F11 | LOW-MED | L43 "when the seat grab is cancelled" | Callback registration is in the receipt (:22); the trigger lives in `CSeatGrab`, which is only forward-declared (`hpp:12`). | "registers a callback that calls finish(true); CSeatGrab unread." | DATA |
| F12 | LOW | L53 "a failed allocation" | Receipt shows only `!good()` → `noMemory()`; cause not shown. | "a grab whose new resource is not good() gets noMemory() and is dropped." | DATA |
| F13 | LOW | L35 "the keyboard goes to one surface ..." | XML conditions enter on "if a whitelisted surface is not already entered". | Add the condition. | DATA |
| F14 | LOW | L19 "the client's own surfaces" | "own" is an object-model inference inside an OBS paragraph. | Label INF or drop "own". | DATA |
| F15 | LOW | L105 "shows why a client cannot get a grab through rules" | Issue 565 shows a rule/focus disagreement, not client grab acquisition. | "shows the rule layer deciding focus over a window; no receipt shows a rule granting a grab." | DATA |
| F16 | LOW | L125 wayland-protocols row | README:11 says "**Some** of the protocols here also do not belong in w-p" — not this one. | Cite the repo location (S283 URL), not the README's "some". | DATA |
| F17 | LOW | L122 "What must a client do ..." | One client's practice, not a protocol requirement. | "What does this client do ...". | DATA |
| F18 | LOW | L6 "binds ten of them" vs S286 row "nine" | Nine direct `wl_registry_bind` calls; the tenth branch hands name/version to `CToplevelManager` (bind not in receipt); row's branch list omits `foreign_toplevel`. | "nine direct binds plus the foreign-toplevel branch via `CToplevelManager`." | DATA |
| F19 | LOW | L31 `cleared` row | Implementation also sends `cleared` when a client commit empties the set (`commit` → `finish(true)`). | Note the extra path in §2 (table row may stay XML-scoped). | DATA |
| F20 | LOW | L109 "The lane holds no focus-rule knowledge" | Supported only by one grep + three named files; other rule entries unscanned. | Scope to the three files and the grep. | DATA |

## UNKs (second question)

- `Hyprland-FocusGrab.hpp` answers **none**: it forward-declares `class CSeatGrab;` (:12) and holds only `m_surfaces`/`m_grab`/`m_grabActive` (:50-54).
- §1 (criteria), §2 (seat routing), §3 (who binds), §5 (0.56.2 #565) stay UNK.
- **§4 UNK second half is answerable from the fetched receipts** (L93): S283 sends `cleared` only for an *active* grab; `startTransaction()` suspends `sync()` so the event loop can dispatch between `add_surface` and `commit`; quickshell's handler sets `active=false` without clearing `pendingAdditions`; `CFocusGrab::finish` clears `m_surfaces` (dropping the pending addition); the deferred commit then starts nothing while the client sets `active=true`. So yes, observable, and client/server `active` can diverge. Repair: answer as INF with the chain, or narrow to "whether the race occurs in practice".
- Predicate gap: no C2 clause tests whether a UNK is already answered by the cited receipts.

## Checked, no defect found

Census 2/78/63/1 (own parser = counter's); latest session has 63 distinct names with no duplicate; `focus` occurs once in the journal; `grep -in focus` over `PortalManager.cpp` exits 1; `onGlobal` :85-261 with ten branches in the listed order and no focus-grab branch; S037 installed `1.4.1-2`; `hyprctl version` matches L77; S287 quotes + CLOSED/COMPLETED + 2022-08-23 + "fixed in b09f157"; S288 quotes; S285 quotes and "sync is the only place that commits" (`this->commit()` only at :75); base-revision lane grep exits 1; every Gate receipt sha256 matches its file (S283 `0bc60c14…`, S284 `53b762f7…`, S285 `6f7cecf1…`, S286 `15c3e39c…`, S287 `148a9053…`, S288 `3c700763…`, S289 `bf8fa91a…`, S037 `4294737a…`).

## Method / safety

Read-only git (`show`, `grep`, `diff`), read-only `journalctl --user -u xdg-desktop-portal-hyprland` (plain, `--list-boots`) and `-u wayland-wm@hyprland.desktop.service -b 0`, `systemctl --user show/cat/is-active`, `readlink /proc/1952/exe`, sysfs DRM status, package-DB `files` read. No pacman, no compositor socket, no Wayland client, no input, no lane edits, no campaign tool in the staged package. No tool installed. Scratch `/tmp/live-journal.txt` removed after the diff.

Full evidence, commands and outputs: `.ufo/waves/round-41/w2/CritEntryOverreach/overreach.md`.

Report: .ufo/waves/round-41/w2/CritEntryOverreach.md
