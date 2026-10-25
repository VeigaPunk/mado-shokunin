# SKILL.md rows for `tools/mado-globals.py` (round 41, w1)

Seat: ScrSkillProvince. Draft only — SKILL.md is frozen for this seat; the L1 integrates.
Every line number below is at HEAD `cd950ec781149040cc73d71cd67c2b67452e7724` (read-only
`git rev-parse HEAD`).

## Provenance of the sample output (read this before the rows)

| Item | Value | How it was checked |
|---|---|---|
| Tool contract | docstring of `quality/counters/c1-r41-globals.py` (`PRED-C1-r41-v1`), lines 1-123 | `read quality/counters/c1-r41-globals.py:1-120` |
| Reference control (NOT the deliverable) | `.ufo/waves/round-41/c1/ctl-ref-tool.py.txt` | `.ufo/waves/round-41/receipts/ctl-c1.txt:1` — `control=P-reference expect=MET got=MET correct=1 \| PRED-C1-r41-v1: fixtures=24/24 tool=present verdict=TARGET_MET` |
| Journal the samples were taken from | `.ufo/waves/round-41/fetch/xdph-journal.txt`, 153 lines, sha256 `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7` | `sha256sum`, `wc -l` (run this seat, 2026-10-25) |
| My run receipt (no `--diff`) | `.ufo/waves/round-41/w1/ScrSkillProvince/ref-run-journal.txt`, sha256 `dda94374195a60f34cb37058750d4010efe3f130d2a6abe4111836e0a73f089c`, 66 lines, rc 0 | `sha256sum`, `wc -l` |
| My run receipt (`--diff`) | `.ufo/waves/round-41/w1/ScrSkillProvince/ref-run-diff.txt`, sha256 `3b3637a482efd330faf8f0c93193622fb57999345a855cee7f7417aca3b45dcf`, 67 lines, rc 0 | `sha256sum`, `wc -l` |
| `tools/mado-globals.py` today | absent at HEAD | `git cat-file -e HEAD:tools/mado-globals.py` → `fatal: path 'tools/mado-globals.py' does not exist in 'HEAD'` |

Why the reference's output is the right sample for the landed tool: `PRED-C1-r41-v1` scores
each of 24 fixtures by comparing **rc and stdout byte-exactly** with the judge's model, and the
reference passes 24/24 (`ctl-c1.txt:1`). The sample below is therefore the output the landed
`tools/mado-globals.py` must produce for this journal, not one tool's private formatting choice.
An unrun check has not passed: I did not run the (still absent) deliverable.

## Anchor A — probe-table row

- File: `SKILL.md`
- Section: `### Read-only probes (all executed 2026-10-14 unless cited)` — line **202**
- Table header `| Probe | Answers | Sample |` — line **204**; separator line **205**
- Last existing row: line **221** — `| \`grim -t ppm -\` (screenshot read to stdout) | ... |`
- Insert the new row **immediately after line 221**, i.e. before the blank line 222 and
  `### Mutating commands — operator only, mado never runs` (line 223). The new row lands on
  line 222 and shifts every later line by +1.

Row text (one line, verbatim):

```
| `python3 tools/mado-globals.py --journal-file <journal>` / `--live` | the Wayland globals the compositor advertised to its portal, as the user journal logged them: sessions, per-global version and count, a fixed class (`focus-grab`, `input-synthesis`, `input-capture`, `session-lock`, `idle`, `clipboard`, `capture`, `toplevel-control`, `output-control`, `sandbox`, `other`), `--diff` drift, `--expect NAME` presence | round-41, journal sha256 `bf8fa91a…`: 2 sessions (pid 1918 boot `-`, pid 1952 boot `7ab69ee4…`), 63 interfaces / 63 adverts in the latest; `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab`; final `MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- verdict=OK` |
```

Note on the section's parenthetical: the header says "all executed 2026-10-14 unless cited".
This row is cited (round-41, 2026-10-25) exactly as the `hyprctl layers` and `grim` rows are,
so no header edit is needed.

## Anchor B — decision-table row

- File: `SKILL.md`
- Section: `### Claim-first routing (what am I trying to settle?)` — line **142**
- Table header `| The claim you must settle | Route to | Run (read-only) | Tag |` — line **144**;
  separator line **145**
- Last existing row: line **156** — `| Bar runtime facts (running? mapped? tray? module text) | ... |`
- Insert the new row **immediately after line 156**, before the blank line 157 and
  `### Divergence vocabulary and severity taxonomy` (line 158). The new row lands on line 157.

Row text (one line, verbatim):

```
| Which Wayland globals the compositor advertises to its portal; is a named global among them | portal journal, not a socket — the portal's own registry view (`xdph-PortalManager.cpp:85` `CPortalManager::onGlobal`, log at `:88`) | `tools/mado-globals.py --live` — one program only, `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, exact argv, stdin `/dev/null`, env limited to `PATH`/`XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`/`LC_ALL`, a bounded timeout, 8 MiB cap — or `--journal-file P`; exit 0 `OK` · 1 `MISSING_EXPECTED` · 3 `NO_SESSIONS` · 2 `SETUP usage` / `unreadable` / `too_large` / `bad_expect` · 5 `SETUP journalctl_unusable` / `journalctl_failed` / `journalctl_too_large` | `[OBS]` for the advertised set as logged; what a client does with a global (grab, capture, synthesis) → `[UNK]` |
```

## Exit map (the row's `Run` cell, expanded)

| Exit | Verdict / setup reason | Trigger (from the `PRED-C1-r41-v1` docstring) |
|---|---|---|
| 0 | `verdict=OK` | ≥ 1 session parsed and every `--expect NAME` present in the latest session |
| 1 | `verdict=MISSING_EXPECTED` | an `--expect NAME` absent from the latest session (`expected_missing=<csv>`) |
| 2 | `MADO_GLOBALS: SETUP usage` | neither or both of `--journal-file`/`--live`; `--journalctl` without `--live`; abbreviated flag |
| 2 | `MADO_GLOBALS: SETUP unreadable` | journal path missing/unreadable |
| 2 | `MADO_GLOBALS: SETUP too_large` | journal file > 8 MiB (8388608 B) |
| 2 | `MADO_GLOBALS: SETUP bad_expect` | an `--expect` value not matching `[A-Za-z0-9_]{1,128}` |
| 3 | `verdict=NO_SESSIONS` | zero ADVERT lines parsed; wins over `MISSING_EXPECTED` |
| 5 | `MADO_GLOBALS: SETUP journalctl_unusable` | `journalctl` (or `--journalctl PROG`) not an absolute regular executable, or group/other-writable; the program is not run |
| 5 | `MADO_GLOBALS: SETUP journalctl_failed` | non-zero exit, spawn failure or timeout |
| 5 | `MADO_GLOBALS: SETUP journalctl_too_large` | > 8 MiB of stdout |

Setup failures print exactly one stdout line and nothing else; on exits 0/1/3 stderr is empty.

## Sample output — my run of the reference on the committed journal

Command (cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`), rc 0, stderr empty:

```
python3 .ufo/waves/round-41/c1/ctl-ref-tool.py.txt \
  --journal-file .ufo/waves/round-41/fetch/xdph-journal.txt
```

Verbatim lines from `.ufo/waves/round-41/w1/ScrSkillProvince/ref-run-journal.txt`
(66 lines total: 2 session lines + 63 `MADO_GLOBAL:` lines + 1 final line):

```
MADO_GLOBALS_SESSION: n=1 boot=- pid=1918 first=2026-10-25T13:16:45-03:00 last=2026-10-25T13:16:45-03:00 interfaces=8 adverts=15
MADO_GLOBALS_SESSION: n=2 boot=7ab69ee4149c4811a3faf6c08c9d119b pid=1952 first=2026-10-25T13:36:24-03:00 last=2026-10-25T13:36:24-03:00 interfaces=63 adverts=63
MADO_GLOBAL: name=ext_background_effect_manager_v1 ver=1 count=1 class=other
MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab
MADO_GLOBAL: name=wl_seat ver=9 count=1 class=other
MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- verdict=OK
```

(The three `MADO_GLOBAL:` lines shown are 1st, 9th and 20th of the 63 by bytewise name
order — a sample of the sorted block, not its whole body; all 63 lines are in the receipt.)

`--diff` (same journal), rc 0 — from `ref-run-diff.txt` (67 lines):

```
MADO_GLOBALS_DIFF: from=1 to=2 added=ext_background_effect_manager_v1,ext_data_control_manager_v1,<61 more names>,zxdg_output_manager_v1 removed=ext_foreign_toplevel_image_capture_source_manager_v1,ext_image_copy_capture_manager_v1,wl_drm,wl_output,wp_color_manager_v1,wp_drm_lease_device_v1,wp_linux_drm_syncobj_manager_v1,zwp_linux_dmabuf_v1 ver_changed=-
```

`<61 more names>` is my elision marker, not tool output: the real line carries all 63 added
names in bytewise order between `ext_data_control_manager_v1` and
`zxdg_output_manager_v1`. The `removed` and `ver_changed` fields above are the real bytes.

The diff line is 1902 bytes in the receipt; measured this seat: `added` 63 names (first
`ext_background_effect_manager_v1`, last `zxdg_output_manager_v1`), `removed` 8 names,
`ver_changed` `-`. The row/sample cells must not carry the whole line —
cite the receipt (`ref-run-diff.txt`, sha256 `3b3637a4…`).

`--expect` legs (same journal):

```
$ … --expect hyprland_focus_grab_manager_v1        # rc 0, final line ends: expected_missing=- verdict=OK
$ … --expect zwlr_screencopy_manager_v2            # rc 1, final line ends: expected_missing=zwlr_screencopy_manager_v2 verdict=MISSING_EXPECTED
```

The second name was chosen to be absent on purpose (the host advertises
`zwlr_screencopy_manager_v1 ver=3`, not `_v2`) so the exit-1 leg is shown on real bytes.

`--selftest` (reference): `MADO_GLOBALS_SELFTEST: 47/47 passed`, rc 0 — the contract floor is
`n >= 25` with `k == n` (clause b).

## What these rows deliberately do not claim

- The journal is the **portal's** registry view (`xdph-PortalManager.cpp:85-88`), not every
  client's. "The compositor advertises X" is `[OBS]` only in the sense "the portal was logged
  receiving X"; a second client's registry is not in this journal.
- Class is a fixed decision table over the name (`quality/counters/c1-r41-globals.py:48-58` in the
  contract docstring; the code table at `:142-165`),
  not a measurement of what the global does. `class=other` is the table's fallback, and 38 of
  the 63 latest-session names fall there.
- No compositor socket is opened, no Wayland client is started, no config byte is written: the
  tool fits SKILL.md's read-verb fence (lines 233-266) rather than extending it. `--live` runs
  exactly one program with a fixed argv, which is the one journal verb the host-safety rule
  allows (`journalctl --user -u <unit> --no-pager -o short-iso`).
- `tools/mado-globals.py` does not exist at HEAD (`git cat-file -e` above), so every sample
  line here is the reference's, not the deliverable's.
