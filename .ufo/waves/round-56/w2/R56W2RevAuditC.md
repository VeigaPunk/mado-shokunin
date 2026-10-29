# R56W2RevAuditC — sentence-to-pin audit of the C1 entry, rows K13–K18

Seat: `R56W2RevAuditC` (leaf member: no subagents, no background jobs).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Target revision audited: **28fc86ac2359ec27406d8a2c63bef82ea6e947ed** (the integrated content revision; lane tip `9c3ca28a` adds only wave-1 evidence).
Entry: `corpus/knowledge/hyprland-config-autoreload-r56.md` (sha256 `ddbdb366c2419c18a2211e9da8d0ccaf964c68f77a526cd0723375713c8c189d`, byte-identical to the blob at the audited revision).
Contract read first, and never edited: `.ufo/waves/round-56/claims-frozen-v2.md`, `.ufo/waves/round-56/registration-v2.md`, `.ufo/waves/round-56/registration.md` (where v2 is silent), `.ufo/waves/round-56/registration-v2-errata.md`, `.ufo/waves/round-56/frozen-tables-v2.json` (sha256 `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2`).
Pins read: `.ufo/waves/round-56/fetch/` at the audited revision (`git show <rev>:<path>` only; the working tree copy of `fetch/` is byte-identical to the audited revision — `git diff --stat` empty).
Deliverables: this report plus `.ufo/waves/round-56/w2/R56W2RevAuditC/receipts/{01-baseline,02-false-propositions,03-pin-context,04-corrections-and-nulls}.txt`.
Scratch (removed before yield): `/fast/scratch/hyaku/mado-r56/R56W2RevAuditC/`.
Tooling: no tool was installed or upgraded (`python3 -I`, `git`, `grep`, `sed` from the base system only); `/home/vgpnk/.omp/agent/RULES.md` was read and no pacman/uv/npm transaction was needed or performed.

**The entry was not edited.** The working tree shows `corpus/SOURCES.md` and the entry as modified, but those are another seat's uncommitted work (new registry rows S392–S395 re-pointing the E-rows); I did not touch them. Everything below is scored at `28fc86ac` via `git show`, never the working tree.

---

## 1. What I attacked

The seat's attack: *the C1 counter proves quote identity and lexical grounding only, so an overreaching or false proposition passes.* Concretely I attacked, for rows K13–K18 of the entry:

1. **Sentence-to-pin fidelity** of each proposition cell against the pin line and the surrounding function (the task's SUPPORTED / OVERREACH / UNSUPPORTED verdict per row).
2. **The counter's sensitivity to those six rows**: can a false proposition in K13–K18 reach `TARGET_MET` and `controls=12/12 verdict=OK`? I built such a tree on a scratch copy and ran the real counter and the real harness on it.
3. **The entry prose that cites these rows or these lines** (Chain steps 4, 5, 7; the Limits sentences that cite `EventLoopManager.cpp:127`, `PropRefresher.cpp:148-149`, `legacy ConfigManager.cpp:1079-1080`): every sentence about pinned code must be true, and every inference must be labelled as inference.

---

## 2. Row-by-row verdict

Pins are the frozen files in `.ufo/waves/round-56/fetch/` at `28fc86ac`. "Pin lines" are line numbers in those files (1-based), as the rows cite them.

| row | verdict | pin lines | correction (one sentence) |
|---|---|---|---|
| **K13** | **SUPPORTED** | `Hyprland-EventLoopManager.cpp:128` (quote) and `:127` (the `FD` binding), `:30-33` (`m_wayland.loop = wlEventLoop`) | none |
| **K14** | **OVERREACH — the "forwards the readable event" clause is contradicted by the pin** | `Hyprland-EventLoopManager.cpp:70-73`, `Hyprland-ConfigWatcher.cpp:80-83` | "On this line the event-loop callback calls onInotifyEvent() on the watcher returned by Config::watcher(), passing none of its fd, mask or data arguments; the watcher then reads its own inotify descriptor." |
| **K15** | **SUPPORTED** | `Hyprland-PropRefresher.cpp:148-149`, `Hyprland-PropRefresher.hpp:18` | none |
| **K16** | **OVERREACH** (effect not shown by the quoted line nor by its surrounding function) | `Hyprland-PropRefresher.cpp:148-149`; the effect is at `Hyprland-ConfigWatcher.cpp:32-35` | "The guarded statement calls update() on the object returned by Config::watcher(); that function rebuilds the watch list (ConfigWatcher.cpp:32-35)." |
| **K17** | **SUPPORTED** | `Hyprland-legacy-ConfigManager.cpp:1077-1082`; `Hyprland-ConfigWatcher.cpp:76-78` | none |
| **K18** | **OVERREACH (minor)** — the logged text is rendered without its `{}` placeholder, so the proposition disagrees with its own quote cell | `Hyprland-legacy-ConfigManager.cpp:1080` | "The debug line logs the reload message for the modified config file and passes the event's file field as its argument." (must not restate the format string verbatim — see §5) |

### K13 — SUPPORTED
Pin line 128 is exactly:
`        m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);`
The proposition's three claims are each visible in the quoted line: an fd descriptor (`FD.get()`) is handed to `wl_event_loop_add_fd` on `m_wayland.loop` (the Wayland event loop, bound from `wl_event_loop* wlEventLoop` at line 32), with `WL_EVENT_READABLE`, and with `configWatcherWrite` as the callback. The proposition's word "the FD descriptor" is deliberately generic and does not claim the fd is the inotify one (which the pin does not show at line 128) — the *inotify* identity is carried by the Chain sentence that cites `127-128` and by `ConfigWatcher.cpp:28-30`. SUPPORTED.

### K14 — OVERREACH (one false clause)
Pin line 71 is `    Config::watcher()->onInotifyEvent();`, inside:
```
70  static int configWatcherWrite(int fd, uint32_t mask, void* data) {
71      Config::watcher()->onInotifyEvent();
72      return 0;
73  }
```
The proposition's second half ("calls onInotifyEvent on the watcher from Config::watcher()") is exactly the line. The first half — "forwards the readable event" — is **not shown and is contradicted**: the callback's `fd`, `mask` and `data` parameters are never used (line 70), `onInotifyEvent()` takes no argument, and the watcher reads its **own** descriptor rather than receiving an event:
```
80  void CConfigWatcher::onInotifyEvent() {
81      constexpr size_t  BUFFER_SIZE = sizeof(inotify_event) + NAME_MAX + 1;
82      alignas(inotify_event) std::array<char, BUFFER_SIZE> buffer = {};
83      const ssize_t    bytesRead = read(m_inotifyFd.get(), buffer.data(), buffer.size());
```
So no readable event is forwarded; the callback only *triggers* a drain of the watcher's own fd. (The fd happens to be the same one — `getInotifyFD()` returns `m_inotifyFd`, `ConfigWatcher.cpp:28-30` — but the event payload and the mask are not passed.) The row's bounded reading should say "triggers the watcher to process its pending inotify events", not "forwards the readable event".

### K15 — SUPPORTED
Pin line 148 `    if (m_propsTripped & REFRESH_CONFIG_WATCHER)` guarding line 149. The proposition claims only the *necessary* direction ("enters its branch only when the mask contains REFRESH_CONFIG_WATCHER"), which is exactly what a bitwise-AND guard on a flag shows. The reading "contains the flag" is exact because `REFRESH_CONFIG_WATCHER` is a single bit — `Hyprland-PropRefresher.hpp:18`: `REFRESH_CONFIG_WATCHER     = (1 << 8),` — which the entry itself carries as row E08 and cites in Chain step 7. `m_propsTripped` is `PropRefreshBits` (`uint16_t` underlying, hpp:9,24,36), so "bit mask" is fair. SUPPORTED.

### K16 — OVERREACH
Pin line 149 `        Config::watcher()->update();` shows the call and nothing else. "refreshing the watch list" is a statement about the *callee*, and the callee's body is in a different file: `Hyprland-ConfigWatcher.cpp:32-35` (`update()` → `setWatchList(...)`). The surrounding function of the quoted line (`CPropRefresher::refreshProp`, `PropRefresher.cpp:55-159`) does not establish it either. As written, the row reads as if line 149 itself says the watch list is rebuilt; that is an inference from another pin's function, stated flatly. The entry's Chain step 7 does label the rebuild an inference ("The watch list is therefore rebuilt after every `reload()` … (inference from these lines; no reload was observed)"), so the prose is better behaved than the row cell.

### K17 — SUPPORTED
Pin line 1079, inside `void CConfigManager::init() {` (line 1077):
```
1077 void CConfigManager::init() {
1079     Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {
1080         Log::logger->log(Log::DEBUG, "CConfigManager: file {} modified, reloading", e.file);
1081         reload();
1082     });
```
The function attribution ("the init function"), the mechanism ("registers a change callback with setOnChange on the config watcher" — `Config::watcher()` is the `CConfigWatcher`, and `setOnChange` stores the function in `m_watchCallback`, `ConfigWatcher.cpp:76-78`), and the argument type (`const CConfigWatcher::SConfigWatchEvent& e`) are all visible in the quoted line or its immediate enclosing function. SUPPORTED.

### K18 — OVERREACH (minor), with a trap for the fix
Pin line 1080 is `        Log::logger->log(Log::DEBUG, "CConfigManager: file {} modified, reloading", e.file);`. Two observations:
* The row's **quote cell** is the format string *including* its `{}` placeholder: `CConfigManager: file {} modified, reloading`. The **proposition** renders the logged text as "CConfigManager: file modified, reloading" — with the placeholder dropped. As a statement of the literal format string it is wrong; as a description of the message after substitution ("file <path> modified, reloading") it is loose but harmless. The row thus disagrees with its own quote cell.
* Any repair that restates the format string verbatim trips the counter's **echo leg** (registration-v2 E4: a frozen quote of ≥30 characters must not appear as a substring of the proposition). I verified this on a scratch copy: see §5, receipt `04-corrections-and-nulls.txt`.

---

## 3. The falsification: six false propositions reach `TARGET_MET` and `controls=12/12 verdict=OK`

This is the seat's central attack, run on a **copy** (the lane was never touched). Method: `git clone --shared` the lane into scratch, `git checkout 28fc86ac`, rewrite only the six proposition cells of K13–K18 into plainly false statements that keep lexical grounding (they reuse the quote's own identifiers and introduce no new numbers), one commit, then run the lane's real counter and the lane's real harness against that commit.

The six false propositions used (scratch commit `a8a7c35b838dd70b002c83ffe930dc2bfe449e11`):

| row | false proposition written into the scratch copy |
|---|---|
| K13 | "…registers the FD descriptor with the Wayland event loop as a **writable** source that calls configWatcherWrite and **immediately reloads the compositor**." (the pin says `WL_EVENT_READABLE`; no reload happens) |
| K14 | "…**forwards the readable event's file path** to the watcher by calling onInotifyEvent…" (the pin forwards nothing) |
| K15 | "…only when the m_propsTripped bit mask contains REFRESH_CONFIG_WATCHER **and REFRESH_GRADIENTS_GROUPBAR**." (the pin tests one flag) |
| K16 | "…calls update on the object returned by Config::watcher(), **sending a SIGHUP to the compositor process**." (the pin sends no signal) |
| K17 | "…registers a change callback with setOnChange on the config watcher, taking an SConfigWatchEvent argument **and clearing the watch list**." (the pin clears nothing) |
| K18 | "…logs the text CConfigManager: file modified, reloading and passes **the event's watch descriptor number** as its argument." (the pin passes a path) |

Commands and decisive output (full transcript: `receipts/02-false-propositions.txt`):

```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo <scratch>/clone --rev a8a7c35... --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=a8a7c35b838dd70b002c83ffe930dc2bfe449e11 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
exit=0

$ python3 -I quality/check-r56-controls.py --claim c1 --repo <scratch>/clone --rev a8a7c35... --work <scratch>
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK
exit=0
```

Compare the baseline on the unmutated lane at the audited revision (`receipts/01-baseline.txt`):
```
MADO_AUTORELOAD_ENTRY: rev=28fc86ac... rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK
```
The two lines are byte-identical apart from the revision. **Six false propositions are invisible to the frozen C1 predicate and to all twelve of its controls.** The `content=33/33` leg is satisfied because `tok` (one shared identifier), `num` (no foreign digit run) and `echo` (the quote is not echoed) are all lexical; the twelve controls are all mutations of *structure* (missing entry, placeholders, a foreign number, a cross-pin source, a scope swap, a dangling provenance id, a dropped row, an edited quote, a flipped pin byte, a missing registry row, a quote echo, a past-EOF anchor), none of which is a semantic falsehood inside a proposition.

**Scope of this finding.** It does **not** falsify `PRED-C1-r56-v2` as frozen: `registration.md` §C1 ("What the counter proves and does not") and `registration-v2.md` ("What v2 does not repair") both state that the counter proves quote identity, registry binding, scope and lexical grounding, and that entailment is carried by the wave-2 sentence-to-pin audit and the non-author closure, "reported not counted". My result confirms that declared limit with a worked instance rather than contradicting it. The consequence for the lane is narrow and concrete: **the entry's proposition cells are the only place where the K13–K18 content is checked, and three of the six need correction** — the counter and the harness will not catch it if the L1 does.

---

## 4. Prose audit of the sentences that cite these rows / these lines

All quoted from the entry at `28fc86ac`.

**Chain step 4** (entry line 23):
> "`CEventLoopManager::enterLoop` registers the inotify descriptor as a readable Wayland source (`Hyprland-EventLoopManager.cpp:127-128`; K13). The callback `configWatcherWrite` calls `onInotifyEvent` (lines 70-71; K14). `CConfigWatcher::onInotifyEvent` (`Hyprland-ConfigWatcher.cpp:80-111`) reads the events, finds each watch by `wd` (line 100), and calls the stored callback with that watch's `file` (lines 102-107; K12, E03). The event `name` field is never read, so the reported path is the watch's stored path, not the name the kernel reports."

Every clause is true of the pins, and the reasoning is not merely plausible — I checked each: `127` binds `FD = Config::watcher()->getInotifyFD()` and guards on `FD.isValid()`; `128` is the `wl_event_loop_add_fd` call with `WL_EVENT_READABLE`; `70-71` is the callback and its call; `80-111` is exactly the span of `CConfigWatcher::onInotifyEvent()`; `100` is the `find_if` on `e.wd == wd`; `102-107` is the `if (WD == m_watches.end()) … else m_watchCallback(SConfigWatchEvent{ .file = WD->file, })` pair; and the last sentence is confirmed by a null search — `grep -rn -- 'ev->name'` over all pins finds **no** match, while the loop uses only `ev->wd` and `ev->len` (the `name` bytes are never dereferenced), so the path handed to the callback is the watch's stored `file` (`ConfigWatcher.cpp:106`), not the kernel-reported name. Note this Chain sentence does **not** repeat K14's "forwards the readable event" wording — the prose is clean where the row cell is not.

**Chain step 5** (line 24): "`CConfigManager::init` installs the change callback (`Hyprland-legacy-ConfigManager.cpp:1079-1082`; K17). It logs (K18) and calls `reload()`." — true (1079-1082 is the whole `setOnChange` block; 1080 the log; 1081 the `reload()`).

**Chain step 7** (line 26): "The prop refresher calls `Config::watcher()->update()` only when the `REFRESH_CONFIG_WATCHER` bit is set (`Hyprland-PropRefresher.cpp:148-149`; K15, K16). `REFRESH_CONFIG_WATCHER` is bit 8 (`Hyprland-PropRefresher.hpp:18`; E08) and `REFRESH_ALL` is the maximum of the 16-bit underlying type (`Hyprland-PropRefresher.hpp:21`; E09), so it contains that bit (arithmetic on the two declarations); `scheduleRefresh` ORs its argument into `m_propsTripped` (`Hyprland-PropRefresher.cpp:31`) and queues the refresh with `doLater` (34). The watch list is therefore rebuilt after every `reload()` from the then-current `m_configPaths` (inference from these lines; no reload was observed)."

Checked line by line: `148-149` guard+call ✔; `hpp:18` `(1 << 8)` ✔ bit 8; `hpp:21` `std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max()` with the enum declared `: uint16_t` (`hpp:9`) ✔ "16-bit underlying type", so `REFRESH_ALL` = 0xFFFF contains bit 8 ✔ — and this arithmetic step is explicitly labelled "(arithmetic on the two declarations)" ✔; `PropRefresher.cpp:31` `m_propsTripped |= prop;` ✔; `:34` `g_pEventLoopManager->doLater(...)` ✔; the final sentence is labelled "(inference from these lines; no reload was observed)" ✔ and the inference is sound (`reload()` → `postConfigReload` → `scheduleRefresh(REFRESH_ALL)` → `m_propsTripped |= REFRESH_ALL` → the bit test at 148 → `update()` → `setWatchList(getConfigPaths())`, with `m_propsTripped` reset at `:156` after the test).

**Scope bullet** (line 14): "…and how an inotify event is routed to `CConfigManager::reload`." — true: event → `onInotifyEvent` → `m_watchCallback` → the lambda installed at 1079 → `reload()` at 1081.

**Limits, line 135**: "if `inotify_init1` fails, the constructor logs and returns (`Hyprland-ConfigWatcher.cpp:21-26`), and the event loop does not register a descriptor (`Hyprland-EventLoopManager.cpp:127`)." — true: `ConfigWatcher.cpp:21-26` is the constructor with the `inotify_init1` failure branch (log + return); `EventLoopManager.cpp:127` is the `FD.isValid()` guard, so line 128's registration is skipped. Both citations point at the right lines.

**Limits, line 136** (adjacent to my rows — it cites the callback path these rows sit on): "`onInotifyEvent` calls the callback once per event (lines 87-110)." — **not quite true**: for an event whose `wd` is not in `m_watches`, `ConfigWatcher.cpp:102-103` logs an error and the callback is *not* called. The accurate sentence is "calls the callback once per event whose watch descriptor is known (lines 87-110); an event for an unknown descriptor is logged and dropped." Severity: minor, but it is a statement of fact about pinned code that the pin contradicts. (The following sentence — "one save … could call `reload()` several times (inference; no save observed)" — is correctly labelled as inference.)

**Adjacent prose I checked opportunistically (outside my row set; not claimed as my scope):** Limits line 137 (inode-based watching, `man7-inotify.7.html:225-228` = "Inotify monitoring is inode-based…") ✔ with the editor-rename consequence correctly labelled "(inference from the man page; not observed)"; Limits line 138's keyword claims ✔ — `HyprCtl.cpp:1194-1208` contains no `Config::watcher()->update()` call (the only `update()` is at 1223-1224 under the `misc:disable_autoreload` test), and the `parseDynamic` → `handleSource` step is explicitly labelled as inference because `parseDynamic` is not in the pins; the host sentence on line 68 ("holds 18 `source =` lines … line 13 names the theme file") and Limits line 139 ("the live file's line 13 holds the same text") check out on this host: `grep -c '^source' ~/.config/hypr/hyprland.conf` → `18`, line 13 → `source = ~/.config/omarchy/current/theme/hyprland.conf`, matching `host-sources.txt:10`; `~/.local/share/omarchy/default/hypr/envs.conf` line 3 → `source = ~/.config/omarchy/current/theme/gum.env.conf`, and `host-watched-lstat.txt:8` lists that path as a regular file.

---

## 5. Counter-safe corrections (verified on a scratch copy)

Proposed replacements, checked against the real counter so the L1 can apply them without turning the predicate red (scratch commits `d9b0f120`, `640f1a0d`; transcript `receipts/04-corrections-and-nulls.txt`):

| row | proposed proposition | counter result |
|---|---|---|
| K14 | "On this line the event-loop callback calls onInotifyEvent() on the watcher returned by Config::watcher(), passing no event data." | included in the run below → `TARGET_MET` |
| K16 | "The guarded statement calls update() on the object returned by Config::watcher()." | included in the run below → `TARGET_MET` |
| K18 | "The debug line logs the reload message for the changed config file and passes e.file as its argument." | included in the run below → `TARGET_MET` |

```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo <scratch>/clone --rev 640f1a0d... --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=640f1a0d... rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
exit=0
```
**Trap found and reported:** a "more literal" K18 wording that restores the format string verbatim — "The debug line logs the format text CConfigManager: file {} modified, reloading and passes e.file as its argument." — makes the counter fail, because the frozen quote (40 characters) then appears inside the proposition and the `echo:` leg fires (registration-v2 E4):
```
MADO_AUTORELOAD_ENTRY: rev=d9b0f120... rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=32/33 new_rows=8/8 verdict=TARGET_MISSED missed=echo:K18
exit=1
```
So the K18 repair must paraphrase the message (as in the table) rather than quote it.

---

## 6. Defects, with severity

| id | row / place | defect | evidence | severity |
|---|---|---|---|---|
| **D1** | K14 proposition | asserts the event-loop callback "forwards the readable event"; the pin shows `fd`/`mask`/`data` are unused and `onInotifyEvent()` takes no argument and re-reads `m_inotifyFd` itself | `EventLoopManager.cpp:70-73`, `ConfigWatcher.cpp:80-83` | **weakens the claim** (the row is false as to mechanism; the frozen predicate is unaffected — it never claimed entailment) |
| **D2** | K16 proposition | "refreshing the watch list" is an effect of the *callee* (`ConfigWatcher.cpp:32-35`), not of the quoted line `PropRefresher.cpp:149` nor of its surrounding function; stated flatly | `PropRefresher.cpp:148-159`, `ConfigWatcher.cpp:32-35` | **weakens the claim** (mild; the Chain prose labels the same rebuild an inference, the row cell does not) |
| **D3** | K18 proposition | renders the logged text without the `{}` placeholder, so the proposition and its own quote cell disagree; a verbatim restatement of the format string breaks the `echo:` leg | `legacy ConfigManager.cpp:1080`; counter run `missed=echo:K18` | **weakens the claim** (mild) |
| **D4** | Limits line 136 | "calls the callback once per event" — for an unknown `wd` the callback is not called (`ConfigWatcher.cpp:102-103`) | `ConfigWatcher.cpp:102-103` | **weakens the claim** (mild, prose-level) |
| **D5** | the C1 counter + harness | six false K13–K18 propositions yield `TARGET_MET` and `controls=12/12 verdict=OK`; the predicate is blind to proposition truth | scratch commit `a8a7c35…`, receipts `02-false-propositions.txt` | **declared limit, not a new defect** — reported as the seat's attack landing; the entry's cells are the only remaining check |

No defect was found in K13, K15 or K17, and none in the Chain prose that cites them.

## 7. Null results (the commands that found nothing)

* `grep -rn -- 'ev->name' <pins>` → **no match**: the inotify event's `name` field is never dereferenced anywhere in the pins, so the Chain's "the event `name` field is never read" holds (the loop touches only `ev->wd` and `ev->len`).
* `grep -rn 'IN_Q_OVERFLOW' <pins>/Hyprland-ConfigWatcher.cpp` → **no match**: the watcher's event loop really has no queue-overflow branch, as Limits states.
* `grep -n 'depth\|visited\|maxDepth'` over `legacy ConfigManager.cpp:1802-1855` → **no match** (checked while validating the neighbouring row set; consistent with the entry's "no visited set and no depth limit" sentence).
* No `IN_Q_OVERFLOW`/`ev->name` occurrence anywhere in `Hyprland-EventLoopManager.cpp` either — the event-loop pin contributes nothing beyond the registration and the callback.

## 8. What I could not verify / did not run

* I did **not** verify the six propositions' truth against upstream Hyprland beyond the frozen pins; the pins are the contract's evidence base and I read only them (plus the lane's own registry/entry at `28fc86ac`). Every verdict above is "what the pin shows", which is exactly the question the seat poses.
* I did **not** re-derive Hyprland's runtime behaviour (no event was generated, no `hyprctl` state change, no config write). The reload-on-save question stays UNKNOWN, as the entry says.
* I did not attack C2 or C3 (other seats' items); I ran only the C1 counter and the C1 harness.
* The non-author closure (a second reader confirming entailment) was not run — that is the lane's stated next step, and my table is exactly the input it needs.
* The `w2` working-tree modifications to `corpus/SOURCES.md` and the entry (new rows S392–S395) are another seat's uncommitted work; I neither read them as evidence nor touched them, and my verdicts are pinned to `28fc86ac`.

## 9. Deliverables

* Report: `.ufo/waves/round-56/w2/R56W2RevAuditC.md` (this file)
* Receipts: `.ufo/waves/round-56/w2/R56W2RevAuditC/receipts/01-baseline.txt`, `02-false-propositions.txt`, `03-pin-context.txt`, `04-corrections-and-nulls.txt`

Report: `.ufo/waves/round-56/w2/R56W2RevAuditC.md`
