# ExecLiveHost — host receipt for C1 (`--live` against the running desktop)

Round 41 (hyaku run 7), wave w1, seat `ExecLiveHost`. Lane `mado-shokunin`, base `ab2bfaab661c846d1de9d58c01651cd156a13949`.
Assignment: the reference tool's `--live` against the running desktop. **Reported, not scored** (registration, Residuals: "The host
receipt (`--live` against the running desktop) is reported, not scored").

Deliverables: `w1/ExecLiveHost/live-census.txt` (439 lines, verbatim outputs + exit codes + hashes + class counts),
`w1/ExecLiveHost/raw/` (21 raw files), `w1/ExecLiveHost/mado-globals.py` (byte copy of the frozen reference),
`w1/ExecLiveHost/manifest.sha256`.

## 1. Setup (byte identity of the tool under test)

- `cp c1/ctl-ref-tool.py.txt w1/ExecLiveHost/mado-globals.py`; sha256 `61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0`
  for both files → the copy is byte-identical to the frozen reference (`c1/ctl-ref-tool.py.txt`).
- `python3 -VV` → `Python 3.14.8`; `hyprctl version` → `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`
  (matches the registration's host row).
- `/usr/bin/journalctl` is root-owned mode 0755, so `resolve_program` accepts it (it rejects group/other-writable).

## 2. Results — every requested run

| run | command | rc | sha256 of stdout |
|---|---|---|---|
| 1 | `python3 -I mado-globals.py --live --diff` | **0** | `3b3637a482efd330…` (67 lines, 7018 B) |
| 2 | same | **0** | `3b3637a482efd330…` (identical) |
| 3 | same | **0** | `3b3637a482efd330…` (identical) |
| 4 | `--live --expect hyprland_focus_grab_manager_v1 --expect zwlr_virtual_pointer_manager_v1 --expect no_such_global_v9` | **1** | `276ca46212d05096…` (66 lines, 5145 B) |
| 5 | same | **1** | `276ca46212d05096…` (identical) |
| 6 | same | **1** | `276ca46212d05096…` (identical) — **third verdict `MISSING_EXPECTED` rc 1, as required** |
| 7 | `--journal-file raw/fresh-journal.txt` | **0** | `dda94374195a60f…` |
| 8 | `--journal-file ../../fetch/xdph-journal.txt` | **0** | `dda94374195a60f…` (identical to 7) |
| 9 | `--journal-file ../../fetch/xdph-journal.txt --diff` | **0** | `3b3637a482efd330…` (identical to runs 1–3) |
| 10 | `env PATH=/nonexistent /usr/bin/python3 -I mado-globals.py --live` | **5** | `MADO_GLOBALS: SETUP journalctl_unusable` |
| 11 | `python3 -I mado-globals.py --live --journalctl /bin/true` | **3** | `…sessions=0 … verdict=NO_SESSIONS` |
| 12 | `python3 -I mado-globals.py --selftest` | **0** | `MADO_GLOBALS_SELFTEST: 47/47 passed` |

- **Stability:** three runs of each live command are byte-identical (same sha256, stderr 0 bytes in all six runs).
- **`--live` == `--journal-file`:** `diff raw/live-diff.1.out raw/jf-fetch-diff.out` → rc 0, 0 bytes of output.
- **Third verdict:** the final line of the expect runs is `… expected_missing=no_such_global_v9 verdict=MISSING_EXPECTED` — the two real
  globals (`hyprland_focus_grab_manager_v1` ver 1, `zwlr_virtual_pointer_manager_v1` ver 2) are present, only the fabricated name is missing.
- Run 12 (`--selftest`, 47/47) was not requested; run for completeness, matches the control receipt's claim.

## 3. Census content and class table counts

Two sessions, latest pid 1952, 63 interfaces, 63 adverts; final line
`MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- verdict=OK`.

Class table counts (recounted from the 63 `MADO_GLOBAL:` lines, sums to 63 and matches the tool's own string):
capture 2, clipboard 3, focus-grab 1, idle 2, input-capture 3, input-synthesis 3, other 38, output-control 4, sandbox 1,
session-lock 2, toplevel-control 4. `hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab` is in the latest session.

## 4. Drift since the fetch capture — none

- Fresh capture `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` (rc 0, 153 lines) is **byte-identical** to
  `fetch/xdph-journal.txt`: both sha256 `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7`.
- No new session, no new advert: the last line of both is the same advert at `2026-10-25T13:36:24-03:00` (pid 1952); the census ran at
  `2026-10-25T20:02-03:00`, i.e. ~6.4 h with no new advert (adverts are emitted by the startup gather, and `wl_output` was re-advertised
  six times by pid 1918 as outputs appeared — `raw/fresh-journal.txt:9,26,29,35,38,70,73`; neither trigger has recurred).
- Independent grep cross-check over the raw journal: `Got interface:` count = 78 = 15 (session 1) + 63 (session 2); distinct names over
  the whole journal = 71; `hyprland_focus_grab_manager_v1` occurrences = 1.
- The registration's provisional fact (2 sessions, 78 adverts, 63 distinct globals latest, one focus-grab advert ver 1 at 13:36:24 pid
  1952) is reproduced exactly by the live run.

## 5. Finding (supports C1, constrains how `--diff` may be read) — session 1 is a truncated view

The two sessions are **disjoint**: session 1 (pid 1918, 15 adverts / 8 distinct) contributes exactly the 8 names in `removed=`, and none
of them (`wl_output`, `wl_drm`, `zwp_linux_dmabuf_v1`, `wp_color_manager_v1`, `wp_drm_lease_device_v1`,
`wp_linux_drm_syncobj_manager_v1`, `ext_image_copy_capture_manager_v1`, `ext_foreign_toplevel_image_capture_source_manager_v1`)
appears anywhere in session 2; `ver_changed=-`.

Evidence that this is journal truncation, not compositor drift:
- Session 2 starts with the complete startup block — `raw/fresh-journal.txt:79` `Starting Portal service (Hyprland implementation)`,
  `:81` `Initializing xdph...`, `:83` `Gathering exported interfaces` — so its 63 globals are a full registry gather.
- Session 1 has no such block: its earliest retained line is `raw/fresh-journal.txt:1`, already an advert at `2026-10-25T13:16:45-03:00`;
  `grep -c 'Initializing xdph' raw/fresh-journal.txt` = 1 (pid 1952 only), and there is no `Starting Portal service (Hyprland
  implementation)` line for pid 1918.
- The boot −1 user journal as a whole is not truncated at that point: `journalctl --user -b -1 … | head -1` → `2026-10-24T20:57:12-03:00`
  (the boot's first entry), while this unit's boot −1 slice starts at 13:16:45 and holds 77 lines, 15 of them adverts
  (`journalctl --user -b -1 -u xdg-desktop-portal-hyprland … | wc -l` = 77). `grep -c Suppressed` over boot −1 = 0, so it is not
  journald rate limiting. What is missing is this unit's start block for that boot; the cause is undetermined by this seat.

Consequence for the lane: on this host, `MADO_GLOBALS_DIFF`'s `removed=` list must not be published as "the compositor stopped advertising
these"; only session 2 is a complete gather. The C2 datum (one advert of `hyprland_focus_grab_manager_v1`, ver 1) is in session 2 and is
unaffected. This is an observation about the host journal, not a defect in the reference tool, whose `--diff` contract is purely positional
(last two sessions).

## 6. Failure modes — as specified

- `PATH=/nonexistent` → `MADO_GLOBALS: SETUP journalctl_unusable`, **rc 5**, 0 bytes stderr. `journalctl` is resolved through `PATH`
  (`resolve_program`), so an unresolvable name is a setup failure, not a crash.
- `--journalctl /bin/true` → **rc 3**, `sessions=0 … verdict=NO_SESSIONS`. `/bin/true` is a regular root-owned 0755 binary, so
  `resolve_program` accepts it; it exits 0 with empty stdout → zero sessions. Empty journal is therefore distinguishable from a failure
  (3 vs 5).

## 7. Risks / notes for the L1

1. **"one allowlisted program" is a weak phrase for this code.** `--journalctl` accepts *any* executable regular file that is not
   group/other-writable (`resolve_program`), not a name allowlist. What is actually constrained is the argv: only the fixed
   `--user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` is ever passed (`JOURNALCTL_ARGS`), with `shell=False`, a 30 s timeout,
   an 8 MiB output cap and a 4-variable environment (`PATH`, `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS`, `LC_ALL`). If the claim text is
   tightened, say "one program, fixed argv, bounded output" rather than "allowlisted program".
2. **`--diff` on a rotated journal** can report `removed=` names that are artifacts of a truncated earlier session (finding 5). A reader of
   the tool's output on this host would otherwise conclude `wl_output`/`wl_drm` had disappeared.
3. **Live-path liveness:** the live path is only as fresh as the portal's last start; a host that has not restarted its portal since boot
   yields a stable but stale census. The live run here agrees with the committed capture because neither trigger has recurred
   (no portal restart, no new output) — an agreement that is evidence of stability, not of freshness.
4. Not exercised: a `--live` hang (the 30 s timeout) and a >8 MiB journal — neither is reachable without perturbing the host, and the
   registration already declares the hang as an uncovered residual.

## 8. Hygiene

Read-only throughout: the frozen reference and fetch receipt, the user journal of `xdg-desktop-portal-hyprland` (only `--list-boots`, `-b -1`
and the plain unit listing; no `--vacuum`/`--rotate`/`--flush`), and `hyprctl version`. No Wayland socket, no compositor or service mutation,
no input injection, no pacman, no git/jj write, no subagent dispatch. No tool installed (nothing was needed). Writes confined to
`w1/ExecLiveHost/` and this report.

## 9. Files

```
w1/ExecLiveHost/mado-globals.py          61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0
w1/ExecLiveHost/live-census.txt          b7587a0905e83be53ff14f3d4606125f22f16b1a11c0221cc524480a7684c482
w1/ExecLiveHost/raw/live-diff.1.out      3b3637a482efd330faf8f0c93193622fb57999345a855cee7f7417aca3b45dcf   (= .2.out = .3.out = jf-fetch-diff.out)
w1/ExecLiveHost/raw/live-expect.1.out    276ca46212d050963fe5bc410f8f75b89ddc8c6ec0a0594535a11527b828b626   (= .2.out = .3.out)
w1/ExecLiveHost/raw/jf-fresh.out         dda94374195a60f34cb37058750d4010efe3f130d2a6abe4111836e0a73f089c   (= jf-fetch.out)
w1/ExecLiveHost/raw/fresh-journal.txt    bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7   (= fetch/xdph-journal.txt)
w1/ExecLiveHost/manifest.sha256          (mado-globals.py + the 21 raw files)
w1/ExecLiveHost/receipt.sha256           b7587a0905e83be53ff14f3d4606125f22f16b1a11c0221cc524480a7684c482  (the receipt cannot contain its own hash)
w1/ExecLiveHost/raw/                     live-diff.{1,2,3}.out/.err, live-expect.{1,2,3}.out/.err,
                                         jf-fresh.out, jf-fetch.out, jf-fetch-diff.out,
                                         fresh-journal.txt (+.err), path-nonexistent.out/.err,
                                         journalctl-true.out/.err
```
