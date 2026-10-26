# SKILL.md / PROVINCE.md insertion text — `tools/mado-globals.py` (round 41, w2)

Seat: ScrSkillFinal. Line numbers are at the DATA commit `07f2641` (`git show 07f2641:SKILL.md`,
2006 lines; `git show 07f2641:PROVINCE.md`, 95 lines). Every sample line is pasted from real runs
of the delivered tool (sha256 `286c051f…`, byte-identical to `ctl-ref-tool-v2.py.txt`) on
`.ufo/waves/round-41/fetch/xdph-journal.txt` (sha256 `bf8fa91a…`), run this seat 2026-10-25.

## Apply order (so anchors stay valid)
1. Probe-table row — after SKILL.md line **221** (lands on 222).
2. Subsection — after SKILL.md line **222** (immediately under the new probe row; `### Mutating
   commands` shifts from 223 to 224+).
3. Decision-table row — after SKILL.md line **156** (unchanged by 1–2).
4. PROVINCE.md inventory row — after line **30**.

## 1. SKILL.md probe-table row (insert after line 221)

```
| `python3 tools/mado-globals.py --journal-file <journal>` / `--live` | which Wayland globals the compositor advertised to its portal, as the portal's journal logged them: per-session `MADO_GLOBALS_SESSION:` lines, one sorted `MADO_GLOBAL: name= ver= count= class=` line per latest-session global, the `MADO_GLOBALS:` summary (interfaces, classes, `ignored=`, verdict); `--diff` drift between the last two sessions; `--expect NAME` presence | round-41, journal sha256 `bf8fa91a…`: 2 sessions (pid 1918 boot `-`, pid 1952 boot `7ab69ee4…`), 63 interfaces / 63 adverts in the latest; `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab`; final `MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK` |
```

## 2. SKILL.md subsection 'Advertised Wayland globals' (insert after line 222)

```
### Advertised Wayland globals

`python3 tools/mado-globals.py --journal-file <journal>` parses the portal unit's `short-iso` journal (`xdph-PortalManager.cpp:85-88` logs one line per advertised global) into sessions; `--live` runs
exactly one program, `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` (stdin `/dev/null`, env `PATH`/`XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`/`LC_ALL`, 30 s timeout,
8 MiB stdout cap; capture the journal by redirecting that same command to a file). Output: `MADO_GLOBALS_SESSION:` per session; one `MADO_GLOBAL: name= ver= count= class=` per latest-session global
(sorted by name); `MADO_GLOBALS_DIFF:` under `--diff`; a `MADO_GLOBALS:` summary with `ignored=` and verdict.

Exit map: 0 `OK` · 1 `MISSING_EXPECTED` (`--expect NAME` absent) · 2 `SETUP` (usage/unreadable/too_large/bad_expect) · 3 `NO_SESSIONS` · 4 `UNRECOGNIZED_FORMAT` · 5 live-journal failure
(journalctl_unusable/journalctl_failed/journalctl_too_large). UNRECOGNIZED_FORMAT = every `Got interface:`-bearing line failed the grammar (`sessions=0`, `ignored>0`) — another `journalctl -o` format, level
or spacing — never a silent NO_SESSIONS; partially foreign journals pass with `ignored=N`.

Class is a fixed table over names: focus-grab, input-synthesis, input-capture, session-lock, idle, clipboard, capture, toplevel-control, output-control, sandbox, else `other`. Advertising a global is not
proving a capability: the census reports `class=` only — no socket, no client, nothing exercised. Real runs on the round-41 journal (second sample: same run with `--expect zwlr_screencopy_manager_v2`, rc 1):

    $ python3 tools/mado-globals.py --journal-file .ufo/waves/round-41/fetch/xdph-journal.txt
    MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab
    MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK
    MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=zwlr_screencopy_manager_v2 ignored=0 verdict=MISSING_EXPECTED
```

## 3. SKILL.md decision-table row (insert after line 156)

```
| Which Wayland globals the compositor advertises to its portal; is a named global among them | portal journal, not a socket — the portal's own registry view (`xdph-PortalManager.cpp:85` `CPortalManager::onGlobal`, log at `:88`) | `tools/mado-globals.py --live` — one program only, `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, exact argv, stdin `/dev/null`, env limited to `PATH`/`XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`/`LC_ALL`, 30 s timeout, 8 MiB cap — or `--journal-file P`; exit map 0/1/2/3/4/5 in § "Advertised Wayland globals" | `[OBS]` for the advertised set as the portal logged it; what a client got is outside this read |
```

## 4. PROVINCE.md inventory row (insert after line 30)

```
| `tools/mado-globals.py` | the bytes of a caller-supplied journal file (`--journal-file`, read whole, 8 MiB cap; missing/unreadable path = setup error) or, under `--live`, the stdout of exactly one program (`journalctl`, or `--journalctl PROG` resolved to an absolute regular, non-group/other-writable file) run with exactly `--user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, stdin `/dev/null`, env `PATH`/`XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`/`LC_ALL`; no compositor socket, no Wayland client, no network, no config tree | nothing — stdout only (`MADO_GLOBALS_SESSION:`, `MADO_GLOBAL:`, `MADO_GLOBALS_DIFF:`, `MADO_GLOBALS:` lines); `--selftest` (63/63 passed this seat) writes only inside a private temporary directory it removes | mado, round 41 (read-only census of the advertised globals; class table is static — a name, not a capability proof; operator applies changes) |
```

## Provenance of every sample line (verbatim from real runs)
| Sample | Source run (this seat, cwd lane root) | Receipt |
|---|---|---|
| `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 …` | `python3 tools/mado-globals.py --journal-file .ufo/waves/round-41/fetch/xdph-journal.txt` | `/tmp/globals-run1.txt:11`, rc 0 |
| final `MADO_GLOBALS: … verdict=OK` | same | `/tmp/globals-run1.txt:66` |
| final `MADO_GLOBALS: … verdict=MISSING_EXPECTED` | same + `--expect zwlr_screencopy_manager_v2` | `/tmp/globals-expect2.txt`, rc 1 |
| selftest 63/63 | `python3 tools/mado-globals.py --selftest` | `/tmp/globals-selftest.txt`, rc 0 |
