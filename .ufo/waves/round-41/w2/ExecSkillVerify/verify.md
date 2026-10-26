# ExecSkillVerify — attack on w1 SKILL.md/PROVINCE.md row drafts (round 41, w2)

Seat: ExecSkillVerify. Target: `ScrSkillProvince` drafts `skill-rows.md` / `province-row.md`.
Executed every command the drafts contain against the **delivered tool** (committed bytes at
`07f2641696b5ac73de1404ea737a9f27e9819aa1`, in my own clone `/tmp/tmp.w2VkXwZBny/lane`
checked out at that commit; clone made with `git clone` + detached `git checkout` — read-only on
the lane).

Deliverable identity: `tools/mado-globals.py` at 07f264 is byte-identical to the v2 reference
(`.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt`): main run `sha256sum` equal
(`392a621d…`), `--diff` run byte-identical, `--selftest` both print `MADO_GLOBALS_SELFTEST: 63/63 passed`.

## 1. Command execution and verdicts (skill-rows.md)

All commands run with cwd = clone root, journal =
`.ufo/waves/round-41/fetch/xdph-journal.txt` (committed; sha256 `bf8fa91a…`, 153 lines — matches
draft).

| Draft statement | Command run | Result | Verdict |
|---|---|---|---|
| Main run rc 0, stderr empty, 66 lines (2 session + 63 `MADO_GLOBAL:` + 1 final) | `python3 tools/mado-globals.py --journal-file .ufo/waves/round-41/fetch/xdph-journal.txt` | rc=0; stderr 0 B; 66 lines | **ok** |
| Session lines: n=1 boot=- pid=1918, n=2 boot=7ab69ee4… pid=1952, interfaces=63 adverts=63 | same run, lines 1-2 | byte-identical to draft quote | **ok** |
| 63 interfaces / 63 adverts in latest; class counts sum to 63 | same run | `interfaces=63 adverts=63`; class counts 2+3+1+2+3+3+38+4+1+2+4=63 | **ok** |
| `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab` | `awk '/^MADO_GLOBAL:/' | grep -n 'hyprland_focus_grab_manager_v1'` | present, 9th of 63 in bytewise-sorted block (`LC_ALL=C sort -c` clean) | **ok** |
| Final line ends `expected_missing=- verdict=OK` | same run, line 66 | tool prints `… expected_missing=- ignored=0 verdict=OK` — **extra `ignored=0`** | **wrong** (see §2) |
| `--diff` rc 0, 67 lines | `--diff` run | rc=0; 67 lines; stderr 0 B | **ok** |
| Diff line 1902 B; added 63 names (first `ext_background_effect_manager_v1`, last `zxdg_output_manager_v1`); removed 8 names; `ver_changed=-` | position of `MADO_GLOBALS_DIFF` line (66), `wc -c`, `tr ',' '\n' | wc -l`, field extracts | 1903 B incl. newline = 1902 content; added 63, first/last as claimed; removed exact 8-name list matches; `ver_changed=-` | **ok** |
| `--expect hyprland_focus_grab_manager_v1` → rc 0 | run with `--expect` | rc=0; final line `… expected_missing=- ignored=0 verdict=OK` | **ok** (suffix true; full line has `ignored=0`) |
| `--expect zwlr_screencopy_manager_v2` → rc 1, `expected_missing=zwlr_screencopy_manager_v2` | run with `--expect` | rc=1; final `… expected_missing=zwlr_screencopy_manager_v2 ignored=0 verdict=MISSING_EXPECTED` | **ok** (suffix true) |
| `--selftest` rc 0 (draft labels 47/47 as *reference* output) | `python3 tools/mado-globals.py --selftest` | rc=0; `MADO_GLOBALS_SELFTEST: 63/63 passed` (draft's 47/47 is correctly attributed to the v1 reference; the landed tool reports 63/63 — v2 reference identical) | **ok** (no row claims the 47/47 number) |
| Exit map: 0 OK / 1 MISSING_EXPECTED / 2 SETUP usage·unreadable·too_large·bad_expect / 3 NO_SESSIONS / 5 SETUP journalctl_unusable·journalctl_failed·journalctl_too_large | setup legs (see §3) | every leg matched | **ok** |

## 2. Defect found: `ignored=0` missing from quoted final lines

`diff /tmp/jn.out <(git show 07f2641:.ufo/waves/round-41/w1/ScrSkillProvince/ref-run-journal.txt)`
→ only line 66 differs: the **delivered tool** (and the v2 reference, byte-identical) prints

```
MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK
```

while the w1 ref receipt (and the row/sample quotes) omit `ignored=0`. Because the draft itself
states the sample is "the output the landed `tools/mado-globals.py` must produce", the row text
does not run as written. **Corrected exact insertion text** (replace the quoted final line in
skill-rows.md row A, sample section, and the two `--expect` excerpts):

```
MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK
$ … --expect hyprland_focus_grab_manager_v1        # rc 0, final line ends: expected_missing=- ignored=0 verdict=OK
$ … --expect zwlr_screencopy_manager_v2            # rc 1, final line ends: expected_missing=zwlr_screencopy_manager_v2 ignored=0 verdict=MISSING_EXPECTED
```

Corrected one-line row A (verbatim replacement for the current row):

```
| `python3 tools/mado-globals.py --journal-file <journal>` / `--live` | the Wayland globals the compositor advertised to its portal, as the user journal logged them: sessions, per-global version and count, a fixed class (`focus-grab`, `input-synthesis`, `input-capture`, `session-lock`, `idle`, `clipboard`, `capture`, `toplevel-control`, `output-control`, `sandbox`, `other`), `--diff` drift, `--expect NAME` presence | round-41, journal sha256 `bf8fa91a…`: 2 sessions (pid 1918 boot `-`, pid 1952 boot `7ab69ee4…`), 63 interfaces / 63 adverts in the latest; `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab`; final `MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK` |
```

The `--diff` row cells carry no final line, so they need no change. Row B (decision table) quotes
no byte output — only the exit map, all of which matches §3.

## 3. Setup legs (exit map) — all matched

| Leg | Command | rc | stdout (single line) |
|---|---|---|---|
| no args | `python3 tools/mado-globals.py` | 2 | `MADO_GLOBALS: SETUP usage` |
| both `--journal-file` and `--live` | `--journal-file x --live` | 2 | `SETUP usage` |
| `--journalctl` without `--live` | `--journalctl /bin/true` | 2 | `SETUP usage` |
| abbreviated flag | `--exp _x` | 2 | `SETUP usage` |
| bad `--expect` value | `--expect 'bad name!'` | 2 | `SETUP bad_expect` |
| missing journal path | `--journal-file /nonexistent/xyz` | 2 | `SETUP unreadable` |
| > 8 MiB | `truncate -s 8388609` | 2 | `SETUP too_large` |
| exactly 8 MiB (8388608 B) | `truncate -s 8388608` | 3 | sessions=0 NO_SESSIONS (cap accepted) |
| non-empty, no ADVERT lines | file with one junk line | 3 | `… sessions=0 … verdict=NO_SESSIONS` |
| 0-byte file | empty file | 2 | `SETUP unreadable` (nuance: 0-byte is treated as unreadable, not NO_SESSIONS; no row claims this case) |
| journalctl unusable | `--live --journalctl /nonexistent/xyz` | 5 | `SETUP journalctl_unusable` |
| journalctl failed | `--live --journalctl /bin/false` | 5 | `SETUP journalctl_failed` |
| valid-but-absent expect | `--expect ABC_123` | 1 | `… expected_missing=ABC_123 ignored=0 verdict=MISSING_EXPECTED` |

All setup failures: exactly one stdout line, stderr empty. `--live` end-to-end run: rc 0, same
final line as `--journal-file` (host journal), stderr empty — the only journal verb used is the
allowed `journalctl --user -u <unit> --no-pager -o short-iso` form.

Implementation facts claimed by the rows, confirmed by source read of `tools/mado-globals.py`:
`MAX_BYTES = 8 * 1024 * 1024` (line 36); env limited to `PATH`/`XDG_RUNTIME_DIR`/
`DBUS_SESSION_BUS_ADDRESS`/`LC_ALL` (lines 191-192); selftest inside `tempfile.TemporaryDirectory`
(line 354, auto-removed); class table keys exactly the eleven classes the rows name, fallback
`other` (lines 49-83).

## 4. Anchors — all verified at 07f264

`SKILL.md`: 142 = `### Claim-first routing (…)`; 144 = header `| The claim you must settle | Route to | Run (read-only) | Tag |`; 145 = separator; 156 = last row `| Bar runtime facts (…) |`; 157 = blank; 158 = `### Divergence vocabulary and severity taxonomy`; 202 = `### Read-only probes (all executed 2026-10-14 unless cited)`; 204 = header `| Probe | Answers | Sample |`; 205 = separator; 221 = last row `| \`grim -t ppm -\` (…) |`; 222 = blank; 223 = `### Mutating commands — operator only, mado never runs`. All match the draft's claimed line numbers exactly.

`PROVINCE.md` (95 lines total at 07f264): 22 = header `| Tool | Reads | Writes | Owner and adjacent lanes |`; 23 = separator; 24-30 = seven rows, last = `tools/mado-anims.py` (line 30); 31 = blank; 32 = `**Round-23 wave-2 correction (…)**: the inventory above covers every tracked file under tools/…`; 84 = `## Round-38 addendum — request-socket knowledge ground (append-only)`; 95 = `half).` — the file's **last** line, so "append after line 95" is a true end-of-file append.

The province-row finding (7 rows vs 10 tracked tools) is verified at w1 HEAD cd950ec:
`git ls-tree --name-only cd950ec tools/` returns exactly 10 (`mado-eventq.py`,
`mado-options.py`, `mado-wsrules.py` unlisted). At 07f264 tools/ has **11** entries (the 10 +
`mado-globals.py`), so the staleness persists and the table now omits four tracked tools; if the L1
inserts the globals row as row 8, the omission of eventq/options/wsrules should be disclosed in the
same commit or the row moved to the addendum (as the draft itself proposed).

## 5. Quote provenance — all verified by grep/awk on the receipts

- `xdph-PortalManager.cpp:85` = `void CPortalManager::onGlobal(uint32_t name, const char* interface, uint32_t version) {`; `:88` = `Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);` ✓
- `xdph-journal.txt:117` = `2026-10-25T13:36:24-03:00 plazir27 xdg-desktop-portal-hyprland[1952]: [LOG]  | Got interface: hyprland_focus_grab_manager_v1 (ver 1)` ✓
- `protocols-README.md:17` = `- `hyprland_focus_grab` -> for grabbing input focus, primarily for complex context menus.` ✓
- `Hyprland-FocusGrab.hpp:59` = `class CFocusGrabProtocol : public IWaylandProtocol {` ✓
- `focus-grab-v1.xml:39` (`hyprland_focus_grab_manager_v1`), `:60` (`hyprland_focus_grab_v1`), `:121` (`<event name="cleared">`) ✓
- `quickshell-grab.cpp:78` = `// the protocol will always send cleared() when the grab is deactivated,`; `:98` = `void FocusGrab::hyprland_focus_grab_v1_cleared() {` ✓
- `keybind-rule-semantics.md:225` contains `no_initial_focus`, `:229` contains `no_focus`, `:232` contains `stay_focused` ✓
- `issue-565.html` `<title>` = `New windows in inactive workspaces stealing focus · Issue #565 · hyprwm/Hyprland · GitHub` ✓
- `PROVINCE.md:73-76` localized-channel rule; `c2-r41-focus-entry-v2.py` clause i: `BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja", …)` (line 121) — equivalent to v1. Minor nit: the draft cites `PRED-C2-r41-v1`; the registered predicate at 07f264 is `PRED-C2-r41-v2` (both counter files exist; clause i unchanged). Not a functional defect.

## 6. Summary

- **Wrong (row text does not run as written):** row A final-line sample (and the sample-section
  and `--expect` excerpts) omit `ignored=0`; corrected text in §2.
- **ok:** all other row statements — exit map (every leg executed), session/global/diff samples,
  anchors (all line numbers exact at 07f264), quote provenance, tool-contract implementation facts.
- **unrun:** none — every command the drafts contain was executed (including `--live` and every
  setup leg). Tools installed: none (used existing python3 + git; no installs recorded).
