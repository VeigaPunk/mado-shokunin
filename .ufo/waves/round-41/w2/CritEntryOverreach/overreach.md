# CritEntryOverreach — where the landed entry says more than its quotes say

Seat: CritEntryOverreach, round 41 wave w2, 2026-10-25.
Target: `corpus/knowledge/hyprland-focus-grab-r41.md` at DATA `07f2641696b5ac73de1404ea737a9f27e9819aa1`
(read with `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641...:<path>`; the worktree has no diff for the entry or `corpus/SOURCES.md`).
Receipts: `.ufo/waves/round-41/fetch/`. Axis: every OBS/INF line must be no stronger than the weakest reading of its receipt.

Verdict: the entry's *quotes* are faithful except one, but **seven statements outrun them**, two of them on the
census that the whole host-advertisement claim rests on. All are DATA defects (fixed in the entry before the round
lands); two also expose predicate gaps (the C2 counter cannot see them).

## Findings, strongest first

### F1 (HIGH, DATA) — "Only the second session is a whole advertisement" is false
Attacks: entry L67 `**INF** Only the second session is a whole advertisement ... 63 distinct names ... which is the only session that can be compared with the compositor's registry as a whole`.
Weakest reading the receipt supports: *the second session starts at a session boundary; its saved log ends mid-enumeration, so 63 is a lower bound.*

Evidence (all run this seat, read-only):
1. The portal is alive: `systemctl --user show -p MainPID,ActiveEnterTimestamp,ExecMainStartTimestamp xdg-desktop-portal-hyprland` → `MainPID=1952`, `ActiveEnterTimestamp=Sun 2026-10-25 13:36:24 -03`; `readlink /proc/1952/exe` → `/usr/lib/xdg-desktop-portal-hyprland`.
2. The live journal is byte-identical to the receipt 7h23m later: `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso > /tmp/live-journal.txt; diff /tmp/live-journal.txt .ufo/waves/round-41/fetch/xdph-journal.txt` → `IDENTICAL` (19130 B each); last line is the 63rd advert at `13:36:24`.
3. The latest session's advert list contains **no `wl_output` and no `zwp_linux_dmabuf_v1`**, while the same portal logged both on the previous boot (`xdph-journal.txt:8-9,26,29,35,38,70,73`) and its own `onGlobal` binds and annotates them (`xdph-PortalManager.cpp:113-117`, `:122-129`; s1 logs `Found output name` at `:42,72` and `[core] dmabufFeedbackMainDevice` at `:69`).
4. The host has a connected output: `for f in /sys/class/drm/*/status; do ...; done` → `card1-DP-1: connected`. Hyprland advertises `wl_output` per output — proven by the previous boot's own log on this host.
5. `journalctl --user -u xdg-desktop-portal-hyprland --list-boots` → boot 0 first entry `13:36:22`, last `20:59:30`; the unit's own journal has no line after `13:36:24`.

So a complete enumeration on a running Hyprland session with a connected output would have logged `wl_output`; the saved log stops before it. The 63 adverts are a prefix, not a whole advertisement.
Impacted: §3 INF, the "registry as a whole" comparison, §7's census discipline.
Smallest safe correction: rewrite L67 to say the latest session *starts* at a session boundary but its log ends mid-enumeration (no `wl_output`/`zwp_linux_dmabuf_v1` line although the same portal logged both on the previous boot and PID 1952 is still alive), so 63 is a lower bound too; keep the census line L63 byte-identical (C2 clause h pins it).
Predicate gap: `journal_counts()` (`quality/counters/c2-r41-focus-entry-v2.py:209`) counts adverts in the latest session but has no completeness check (no mandatory-global set, no "log ends at a session end" test), so a truncated enumeration passes.

### F2 (HIGH, DATA) — "five requests" is not a count of the XML
Attacks: entry L115 `S283: two interfaces, five requests, one event (§1)`.
The XML has **six** `<request>` elements: `create_grab` (:44), manager `destroy` (:52), `add_surface` (:79), `remove_surface` (:91), `commit` (:105), grab `destroy` (:115). The entry's own §1 (L21) and table (L25-L30) list all six.
Also the S283 registry row's cell 4 says "The two interfaces, four requests and one event" — a third, different count for the same file.
Evidence: `grep -c '<request' .ufo/waves/round-41/fetch/focus-grab-v1.xml` → `6`.
Smallest safe correction: L115 → "two interfaces, six requests, one event"; S283 row → "six requests (two on the manager, four on the grab)".
Predicate gap: no clause counts XML members.

### F3 (HIGH, DATA) — the `commit` quote drops the guard that the next clause depends on
Attacks: entry L49 `"if (anyCommitted) start(); else finish(true);" - ... only a change of the set triggers start or finish`.
Actual code (`Hyprland-FocusGrab.cpp:137-142`):
```
    if (surfacesChanged) {
        if (anyCommitted)
            start();
        else
            finish(true);
    }
```
The quoted string occurs in the whitespace-collapsed receipt only as a *substring* of the guarded block. As presented, a commit that changes nothing but has a committed surface would call `start()`; the entry's own "only a change of the set" clause silently relies on the dropped `if (surfacesChanged)`.
Smallest safe correction: quote the collapsed block `if (surfacesChanged) { if (anyCommitted) start(); else finish(true); }` (that string is verbatim after whitespace collapse).
Predicate gap: clause d checks only the per-id Gate quote (S284's is `m_grab->m_keyboard = true;`) and matches it as a substring, so an inline quote that drops an enclosing condition passes.

### F4 (MEDIUM, DATA) — "a commit promotes additions into the seat grab" is false for the destroy-path commit
Attacks: entry L49 second clause, read together with L49's `eraseSurface` sentence.
`commit(bool removeOnly)` skips promotion for `removeOnly` (`Hyprland-FocusGrab.cpp:123-129`: `if (!removeOnly) { ... }`); `eraseSurface` calls `commit(true)` (:89-92), so pending additions are left pending, not promoted. The sentence is true only for `commit(false)`.
Smallest safe correction: "a normal commit promotes additions; the destroy-path `commit(true)` erases removals only and leaves pending additions pending."

### F5 (MEDIUM, DATA) — S037: the receipt contradicts "the same upstream release"
Attacks: entry L73 `the portal that wrote this journal is upstream v1.4.1 at pkgrel 2, so the v1.4.1 pin ... and the running unit are the same upstream release`.
The S037 receipt's own reading note says: "a claim pinned to v1.4.1 covers 1.4.1-2 only as far as the packaging leaves the source untouched, which this receipt does not establish" (`.ufo/waves/round-41/fetch/xdph-installed-version.txt`, tail).
What the receipt does establish: installed package version `1.4.1-2`; and separately the running binary is the installed package's file — `readlink /proc/1952/exe` → `/usr/lib/xdg-desktop-portal-hyprland`, `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/files:9` lists `usr/lib/xdg-desktop-portal-hyprland`, and the unit's `ExecStart` names the same path (`systemctl --user cat xdg-desktop-portal-hyprland`). Source identity (pkgrel 2 = unmodified v1.4.1) is not established.
Smallest safe correction: split the sentence — "the installed package is 1.4.1-2 and PID 1952 executes the binary that package owns; whether pkgrel 2 modified the v1.4.1 source is not established by this receipt."

### F6 (MEDIUM, DATA) — the first session's 15 adverts are not a lower bound for this registry
Attacks: entry L67 `its 15 adverts are a lower bound`.
The `-- Boot 7ab69ee4149c4811a3faf6c08c9d119b --` marker at `xdph-journal.txt:78` is a boot transition: `journalctl --user -u xdg-desktop-portal-hyprland --list-boots` shows boot -1 last entry `2026-10-25 13:35:34` and boot 0 first `13:36:22`. The first session is the previous boot's portal (pid 1918), so its adverts are a slice of a *different compositor instance*, not a lower bound for the current registry. The entry notes the marker but draws no consequence.
Smallest safe correction: "the first session is the previous boot's portal (the :78 marker is a boot transition), so its slice cannot be compared with the current registry at all."

### F7 (MEDIUM, DATA) — "enforced at the seat" is the entry's own UNK
Attacks: entry L55 `**INF** The whitelist is enforced at the seat, not at the rule layer`.
The receipt shows `setGrab(m_grab)`/`setGrab(nullptr)` and no rule read in the file; the seat's own filtering is L57's UNK ("the seat's own code was not read this round"). `refocusKeyboard` goes through `Desktop::focusState()->rawSurfaceFocus` (:108), a focus-state call whose constraints are not in the receipt. "Not at the rule layer" is a negative about the whole compositor derived from one file.
Smallest safe correction: "the grab is installed as the seat's grab and this file reads no window or workspace rule; how `CSeatGrab` filters events is unread (§2 UNK)." Drop "enforced"/"not at the rule layer" or label them INF with the scope.

### F8 (MEDIUM, DATA) — "the client controls only membership"
Attacks: entry L37.
The client also controls *when* it commits (a commit is what starts/ends the grab, S283 `commit` text) and *when* it destroys the grab (S283 grab `destroy`: "remove the grab if active"). "Only membership" excludes both.
Smallest safe correction: "no request names a focus target; the client controls the surface set, the commit timing, and the grab's lifetime."

### F9 (LOW-MED, DATA) — "the portal does not use it" is one file
Attacks: entry L71 last sentence and the L120 row `Does the portal use it? ... OBS`.
The evidence is `grep -in focus` over `xdph-PortalManager.cpp` (exit 1) and the journal; the other portal sources were not read. L135 already scopes this to "v1.4.1's `PortalManager.cpp` and this journal", so L71/L120 should match.
Smallest safe correction: "`PortalManager.cpp` logs the global and has no branch for it"; L120 → "Does `PortalManager.cpp` bind it?".

### F10 (LOW-MED, DATA) — "treats ... as a bug rather than a state"
Attacks: entry L51.
The branch is `LOGM(Log::ERR, "CFocusGrab::refocusKeyboard called with no committed surfaces. This should never happen.")` followed by function return (`Hyprland-FocusGrab.cpp:109-110`): no clear, no client error, no abort. "Treats as a bug" is a gloss on a log line, not a behaviour.
Smallest safe correction: "logs an ERR assertion and returns without touching focus or signalling the client."

### F11 (LOW-MED, DATA) — the callback's trigger is not in the receipt
Attacks: entry L43 `makes the grab finish itself ... when the seat grab is cancelled`.
The receipt shows the registration `m_grab->setCallback([this]() { finish(true); })` (:22) and nothing about `CSeatGrab`; the header only forward-declares `class CSeatGrab;` (`Hyprland-FocusGrab.hpp:12`). When the callback fires is the unread side.
Smallest safe correction: "registers a callback that calls `finish(true)`; what invokes it lives in `CSeatGrab`, not in this receipt."

### F12 (LOW, DATA) — "failed allocation" is inferred from the error name
Attacks: entry L53.
The receipt shows `if UNLIKELY (!RESOURCE->good()) { pMgr->noMemory(); m_grabs.pop_back(); }` (:169-172); `good()` is `m_resource->resource()` (:35-37). The cause of a not-good resource is not in the receipt.
Smallest safe correction: "a grab whose new resource is not good() gets `noMemory()` and is dropped from `m_grabs`."

### F13 (LOW, DATA) — the `wl_keyboard::enter` sentence drops its condition
Attacks: entry L35 `the keyboard goes to one surface the compositor picks from the set`.
The XML conditions the pick: "a compositor-picked surface in the whitelist will receive a wl_keyboard::enter event **if a whitelisted surface is not already entered**" (`focus-grab-v1.xml:69-70`).
Smallest safe correction: add the condition.

### F14 (LOW, DATA) — "the client's own surfaces" is an object-model inference inside an OBS
Attacks: entry L19 `so the surface is a *limiter over the client's own surfaces*`.
The XML says "a specific set of surfaces"; "own" follows from Wayland's object model (a client can only name objects it created), not from the quoted text. The paragraph is labelled OBS.
Smallest safe correction: label the inference INF or drop "own".

### F15 (LOW, DATA) — issue 565 does not show why a client cannot get a grab through rules
Attacks: entry L105 `it shows why a client cannot get a grab through rules`.
Issue 565 shows a workspace `silent` rule and a focus disagreement (verified: rule, Expected, Actual, log line, CLOSED/COMPLETED, created 2022-08-23, "fixed in b09f157"). It says nothing about a client obtaining a grab.
Smallest safe correction: "it shows the rule layer deciding focus over a window; no receipt shows a rule that grants a client a surface grab."

### F16 (LOW, DATA) — the wayland-protocols row rests on "some"
Attacks: entry L125 `Is the protocol part of wayland-protocols? | S288: Hyprland maintains its own set`.
README:11 says "**Some** of the protocols here also do not belong in w-p"; "some" does not name this protocol. The location (`hyprwm/hyprland-protocols`, S283's URL) is the evidence.
Smallest safe correction: cite the repository location, not the README's "some".

### F17 (LOW, DATA) — a "must" answered by one client's practice
Attacks: entry L122 `What must a client do between add_surface and commit? | S285: batch in pendingAdditions, then sync() commits`.
That is quickshell's practice, not a protocol requirement (the XML requires only a commit).
Smallest safe correction: "What does this client do between ...".

### F18 (LOW, DATA) — "binds ten of them" vs the row's "nine"
Attacks: entry L6 header and S286 row cell 4 ("which nine it binds").
`grep -c 'wl_registry_bind' xdph-PortalManager.cpp` → 9 direct binds; the tenth branch (`:249-254`) hands the global name/version to `CToplevelManager`, whose bind is not in the receipt. The row's parenthetical branch list omits `foreign_toplevel` although its own range `:247-259` covers it.
Smallest safe correction: "nine direct binds plus the foreign-toplevel branch via `CToplevelManager`" in both places.

### F19 (LOW, DATA) — the `cleared` table row is narrower than the implementation
Attacks: entry L31 `cleared | the compositor cancelled an active grab`.
In this implementation `commit` → `finish(true)` also sends `cleared` when a client commit empties the set (`Hyprland-FocusGrab.cpp:137-142`, `:68-69`), which is the path quickshell's §4 comment relies on.
Smallest safe correction: note the client-driven empty-commit path in §2 (the table row can stay XML-scoped).

### F20 (LOW, DATA) — "The lane holds no focus-rule knowledge"
Attacks: entry L109.
Verified evidence: `git grep -il -e focus_grab -e focus-grab -e 'focus grab' ab2bfaab -- corpus PROVINCE.md SKILL.md tools` exits 1; `window-rule-effects-getprop.md` and `workspace-rules-r27.md` have no `focus` line; `rule-attribution-r24.md:81` has `jetbrains-focus`. The general negative is supported only for those three files and that grep pattern; other rule entries were not scanned.
Smallest safe correction: scope the sentence to the three named files plus the grep.

## UNK answerability (the task's second question)

- `Hyprland-FocusGrab.hpp` answers **none** of the entry's UNKs: it forward-declares `class CSeatGrab;` (:12) with no members, and holds only `m_surfaces`, `m_grab`, `m_grabActive` (:50-54). No routing, no criteria, no client identity.
- §1 UNK (implementation-defined criteria): the XML says "implementation-defined" and names only the usual outside-input case and a competing grab; not answerable from the XML.
- §2 UNK (CSeatGrab routing): not answerable — the header has no `CSeatGrab` body.
- §3 UNK (who binds today): not answerable from the receipts; the journal logs adverts, not binds (this round forbids a live registry read).
- §5 UNK (0.56.2 still exhibits #565): not answerable; no focus transition was measured.
- **§4 UNK, second half is answerable from the fetched receipts** (L93: "whether a `cleared` arriving between `add_surface` and `commit` is observable to this client"). Derivation, not measurement:
  1. S283's `cleared` is sent when an *active* grab is cancelled; a grab with a pending addition is still active (`focus-grab-v1.xml:121-126`).
  2. `startTransaction()` suspends `sync()` (`quickshell-grab.cpp:71-72,91-96`), so `add_surface` can be sent and the commit deferred while the client's event loop runs — the cleared can be dispatched in that window.
  3. The cleared handler sets `active = false` and emits, and does **not** clear `pendingAdditions` (`quickshell-grab.cpp:98-101`).
  4. `CFocusGrab::finish` clears `m_surfaces` (`Hyprland-FocusGrab.cpp:65-66`), dropping the server-side pending addition; the deferred commit then finds nothing to start, while the client's `sync()` still sees a non-empty `pendingAdditions` and sets `active = true` (`quickshell-grab.cpp:74-87`).
  So: yes, observable, and the client's `active` can diverge from the server. The first half of the UNK (one Qt transaction = one frame) stays unmeasured.
  Smallest safe correction: answer the second half as an INF with this chain (or narrow the UNK to "whether the race occurs in practice").
- Predicate note: no C2 clause tests whether a UNK is already answered by the cited receipts.

## Checked with no defect found

- §1 quotes against `focus-grab-v1.xml`: interface description (:33-37), manager two requests (:44-57), grab four requests + `cleared` (:79-126), commit transition (:109-111), routing/trigger (:66-76) — all verbatim modulo line joins; duplicate-addition and destroy-as-remove semantics match `addSurface`/`eraseSurface`.
- §2 quotes against `Hyprland-FocusGrab.cpp`: constructor keyboard+pointer (:20-21), callback (:22), `start` (:47-56), `finish` + destructor + `m_seatGrab` guard (:58-71, :31-33), three-valued state (`Hyprland-FocusGrab.hpp:20-24`), `eraseSurface` (:89-92), `onCreateGrab` (:165-173).
- §3 census arithmetic: 2 sessions, 78 adverts, 63 distinct names in the latest session, no duplicate name in it, 1 focus-grab advert (own parser and the counter's `journal_counts` agree); `focus` occurs once in the journal (case-insensitive); `grep -in focus xdph-PortalManager.cpp` exits 1; `onGlobal` spans :85-261 with ten `INTERFACE ==` branches in the listed order and no focus-grab branch.
- S037 installed version `1.4.1-2`; running binary is the installed package's file (`/proc/1952/exe`, package `files:9`, unit `ExecStart`).
- `hyprctl version` prints `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f` — matches L77.
- S287 quotes, CLOSED/COMPLETED, created 2022-08-23T14:03:55Z, "fixed in b09f157"; S288 quotes at README:8-9,17; S285 quotes and "sync is the only place that commits" (`this->commit()` only at `quickshell-grab.cpp:75`).
- Every Gate receipt sha256 matches its file: S283 `0bc60c14…`, S284 `53b762f7…`, S285 `6f7cecf1…`, S286 `15c3e39c…`, S287 `148a9053…`, S288 `3c700763…`, S289 `bf8fa91a…`, S037 `4294737a…`.
- The base-revision lane grep claim at L109 (exit 1) is true.

## Reproduction

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git show 07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/knowledge/hyprland-focus-grab-r41.md | cat -n
journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso > /tmp/live-journal.txt
diff /tmp/live-journal.txt .ufo/waves/round-41/fetch/xdph-journal.txt     # IDENTICAL
systemctl --user show -p MainPID,ActiveEnterTimestamp xdg-desktop-portal-hyprland
readlink /proc/1952/exe; grep -n 'usr/lib/xdg-desktop-portal-hyprland$' /var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/files
journalctl --user -u xdg-desktop-portal-hyprland --list-boots --no-pager
for f in /sys/class/drm/*/status; do printf '%s: ' "$f"; cat "$f"; done
grep -c '<request' .ufo/waves/round-41/fetch/focus-grab-v1.xml          # 6
grep -n 'wl_registry_bind' .ufo/waves/round-41/fetch/xdph-PortalManager.cpp   # 9 direct
grep -n 'commit(true)\|if (surfacesChanged)' .ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp
```

No tool was installed; no campaign tool was run; no lane file was edited; no Wayland client or compositor socket was opened; the only journal verbs were the read-only forms above.
