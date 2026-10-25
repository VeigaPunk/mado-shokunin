# PROVINCE.md rows / paragraph for "advertised Wayland globals and focus-grab clients" (round 41, w1)

Seat: ScrSkillProvince. Draft only — PROVINCE.md is frozen for this seat; the L1 integrates.
Line numbers are at HEAD `cd950ec781149040cc73d71cd67c2b67452e7724` (read-only `git rev-parse
HEAD`); PROVINCE.md is 95 lines.

## Provenance of the grounding anchors

| Anchor | Where | Checked by |
|---|---|---|
| portal logs one line per advertised global | `.ufo/waves/round-41/fetch/xdph-PortalManager.cpp:85` (`void CPortalManager::onGlobal(uint32_t name, const char* interface, uint32_t version) {`), log statement at `:88`: `Debug::log(LOG, " \| Got interface: {} (ver {})", INTERFACE, version);` | `read …:78-95` |
| own-work advertisement on this host | `.ufo/waves/round-41/fetch/xdph-journal.txt:117` — `2026-10-25T13:36:24-03:00 plazir27 xdg-desktop-portal-hyprland[1952]: [LOG]  \| Got interface: hyprland_focus_grab_manager_v1 (ver 1)` (journal sha256 `bf8fa91a…`, 153 lines) | `grep -n 'focus_grab'`, `sha256sum` (this seat) |
| Hyprland's own protocol list | `.ufo/waves/round-41/fetch/protocols-README.md:17` — `` `hyprland_focus_grab` -> for grabbing input focus, primarily for complex context menus. `` | `awk NR==17` |
| compositor-side implementation | `.ufo/waves/round-41/fetch/Hyprland-FocusGrab.hpp:59` — `class CFocusGrabProtocol : public IWaylandProtocol {` | `awk NR==59` |
| protocol wire surface | `.ufo/waves/round-41/fetch/focus-grab-v1.xml:39` (`hyprland_focus_grab_manager_v1`, version 1), `:60` (`hyprland_focus_grab_v1`), `:121` (`<event name="cleared">`) | `grep -n '<interface\|<event name'` |
| a real client's lifecycle | `.ufo/waves/round-41/fetch/quickshell-grab.cpp:78` — `// the protocol will always send cleared() when the grab is deactivated,` and `:98` `void FocusGrab::hyprland_focus_grab_v1_cleared() {` | `awk NR>=76&&NR<=80`, `grep -n` |
| rule-level counterpart (already owned) | `corpus/knowledge/keybind-rule-semantics.md:225` (`no_initial_focus`), `:229` (`no_focus`), `:232` (`stay_focused`) | `awk` |
| the exclusion rule this row must obey | `PROVINCE.md:73-76` (localized-documentation channel is out) and `PRED-C2-r41-v1` clause i (a cited location must not contain `amgsk.dev`, `zhihu`, `/zh`, `/ja`) | `read quality/counters/c2-r41-focus-entry.py:1-80` |

Every one of these is a read-only byte/source read; no socket was connected, no client started,
no journal verb beyond the allowed `journalctl --user -u <unit> --no-pager -o short-iso` form.

## Anchor C — tool-inventory row

- File: `PROVINCE.md`
- The inventory table starts at line **22** (`| Tool | Reads | Writes | Owner and adjacent lanes |`),
  separator line **23**, rows lines **24-30** (last row: `tools/mado-anims.py`, line 30), blank
  line 31, then the `**Round-23 wave-2 correction …**` paragraph at line 32.
- Insert the new row **immediately after line 30**; it becomes line 31 and shifts the rest by +1.

Row text (one line, verbatim):

```
| `tools/mado-globals.py` | the bytes of a caller-supplied journal file (`--journal-file`, read whole with an 8 MiB cap; a missing or unreadable path is a setup error) or, under `--live`, the stdout of exactly one program (`journalctl`, or `--journalctl PROG`, resolved to an absolute regular file that is not group- or other-writable) run with exactly `--user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, stdin `/dev/null`, an environment limited to `PATH`, `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS`, `LC_ALL`; no compositor socket, no Wayland client, no network, no config tree | nothing — stdout only (`MADO_GLOBALS_SESSION:`, `MADO_GLOBAL:`, `MADO_GLOBALS_DIFF:`, `MADO_GLOBALS:` lines); `--selftest` writes only inside a private temporary directory it removes | mado, round 41 (census of the globals the compositor advertised to its desktop portal, as that portal logged them; one host, one journal — the portal's registry view, not another client's, and not a client's behaviour) |
```

Note for the L1: this row is written to the table's four-column shape, but see the finding below —
three tracked tools are missing from that table, so the row may instead belong in a new
`## Round-41 addendum` (Anchor D) if the table is not repaired this round.

## Anchor D — scope-check paragraph (new append-only section)

- File: `PROVINCE.md`, append at end of file: after line **95** (`half).`), which closes
  `## Round-38 addendum — request-socket knowledge ground (append-only)` (section opens line 84).
- Precedent for this shape: `git log --oneline -4 -- PROVINCE.md` → `6068feb round-38: PROVINCE
  addendum naming the request-socket knowledge ground (ConnOverlap) — append-only, read-only
  bound kept explicit`. Appending a section leaves every existing line number intact.

Text to append (verbatim, after one blank line):

```markdown
## Round-41 addendum — advertised Wayland globals and focus-grab clients (append-only)

The protocol surface this round adds is the set of globals the compositor *advertises*, not the
capabilities they carry. It is witnessed two ways, both read-only: by the portal's own journal
(`CPortalManager::onGlobal` logs one line per global, `xdph-PortalManager.cpp:85-88`; the host
journal holds one advert of `hyprland_focus_grab_manager_v1 (ver 1)` at `xdph-journal.txt:117`),
and by Hyprland's own protocol sources read at pinned revisions (the `hyprland_focus_grab`
listing at `protocols-README.md:17`, the compositor-side `class CFocusGrabProtocol : public
IWaylandProtocol` at `Hyprland-FocusGrab.hpp:59`, the wire surface at `focus-grab-v1.xml:39,60,121`).

**In province.** (1) The advertised set as the portal logged it — the read surface of
`tools/mado-globals.py`, whose class table (`focus-grab`, `input-synthesis`, `input-capture`,
`session-lock`, `idle`, `clipboard`, `capture`, `toplevel-control`, `output-control`, `sandbox`,
`other`) names surfaces, never behaviour. (2) Hyprland's own protocol definitions and the
compositor-side implementation, as documentation/source-read knowledge at a pinned revision —
the same footing the Round-38 addendum gives the socket vocabulary. (3) The rule-level
counterpart is already owned, not new: focus rules (`no_initial_focus`,
`keybind-rule-semantics.md:225`; `no_focus`, `:229`; `stay_focused`, `:232`) are declared in
`~/.config/hypr/` under lines 6-12 above.

**Adjacency — report, never absorb.** (a) A client application's use of a global is evidence of
the protocol's shape, not an owned surface: the grab lifecycle in
`quickshell-grab.cpp:78,98` (`cleared()` on deactivation) is read from a client codebase the
lane does not own, and the client's own behaviour stays `[UNK]`. (b) Security literature and
upstream bug-tracker material about focus stealing (e.g. the issue titled "New windows in
inactive workspaces stealing focus", `issue-565.html`) may name a surface or a lead; it never
grounds a host claim, which still needs a journal line or a source byte. (c) The *exercise* of a
privileged capability — input synthesis, input capture, a grab actually taken — is outside the
province; only its advertisement is inside, which is why the census reports `class=` and nothing
about what any client did.

**Out of province.** The localized-documentation channel, by the rule stated at lines 73-76: no
Japanese- or Chinese-channel material, URL, snapshot or revision-bookkeeping claim enters an
entry or this file (the staged `focus-control-surfaces-r28` section 3 is excluded on that rule,
and `PRED-C2-r41-v1` clause i forbids such a location in any cited source row).

No new write surface: the census opens no socket and starts no client, the journal is read only
through `journalctl --user -u <unit> --no-pager -o short-iso`, and the protocol sources are
bytes in `.ufo/waves/round-41/fetch/`.
```

## Scope check, condensed (what the L1 can diff against the paragraph)

| Question | Answer | Anchor |
|---|---|---|
| Is "the compositor advertises global X" in province? | yes, as the portal's logged registry view | `xdph-PortalManager.cpp:85-88`, `xdph-journal.txt:117` |
| Is Hyprland's own protocol definition in province? | yes, documentation/source-read at a pinned revision, read-only | `protocols-README.md:17`, `Hyprland-FocusGrab.hpp:59`, `focus-grab-v1.xml:39` |
| Is a client's grab lifecycle in province? | adjacency only — evidence of shape, `[UNK]` for the client's behaviour | `quickshell-grab.cpp:78,98` |
| Is security literature in province? | adjacency only — a lead, never a ground | `issue-565.html` title |
| Are focus *rules* new surface? | no — already owned by the config plane | `keybind-rule-semantics.md:225,229,232`; PROVINCE.md:6-12 |
| Is localized-channel material in province? | no | PROVINCE.md:73-76; `PRED-C2-r41-v1` clause i |
| Does this widen a write surface? | no — read-only journal and source bytes | tool contract, Anchor C |

## Finding (report-only, for the L1)

`PROVINCE.md:32` says the inventory "covers every tracked file under `tools/`", but the table
(lines 24-30) lists **7** rows while `git ls-tree --name-only HEAD tools/` returns **10**:
`tools/mado-eventq.py`, `tools/mado-options.py` and `tools/mado-wsrules.py` are tracked and
unlisted. So the table is stale as of those rounds and the round-23 correction's "every tracked
file" clause is falsified at HEAD. I did not repair it (frozen file, and the repair is not my
seat's task); if the L1 appends `tools/mado-globals.py` as row 8 of a 7-row table, the staleness
should be disclosed in the same commit or the row moved into the Round-41 addendum instead.

Checks I did **not** run (so they are not claimed): the C2 counter was not executed against any
draft (the entry it scores does not exist at HEAD — `ls corpus/knowledge/hyprland-focus-grab-r41.md`
→ absent), and no counter or control was re-run this seat.
