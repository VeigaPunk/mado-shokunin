# Why the first journal session lists only 8 interfaces

Seat: `ExecJournalHistory` (w1, round 41). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Subject: session 1 of `xdg-desktop-portal-hyprland` (pid 1918) in
`.ufo/waves/round-41/fetch/xdph-journal.txt` (sha256 `bf8fa91a…00aaf7`, 153 lines; verified byte-identical
to the live journal for both blocks by `diff` — see §7).

## 0. Verdict

**Neither of the three offered causes is the operative one.** Session 1 is not a registry that lost its tail
to rotation, and it is not a portal that restarted early or bound a smaller registry. It is a **fragment of a
block-buffered stdout stream**:

1. xdph logs to stdout (`_TRANSPORT=stdout`), which is a pipe, so libc block-buffers it; journald therefore
   receives the process's log in **~4 KiB flushes** and **stamps each entry with the flush instant**, not the
   instant the process produced it.
2. Session 1's surviving 73 entries were all ingested at **2026-10-25T13:16:45.875** in three reads
   (2034 + 2049 + 42 B), 39 h 02 m after the portal started. They contain startup-phase content.
3. The **first** flush of that same stream (which held the registry-census head) had been ingested at unit
   start, 2026-10-23T22:14:10, and is **outside journal retention** — the user journal retains nothing older
   than 2026-10-24T20:57:12 (22 h 43 m of the unit's 39 h 21 m life is gone). The only recorded removal is an
   explicit `journalctl --vacuum-size=50M` at **13:10:39**, six minutes before the surviving flush.
4. Consequently the 8 names are **disjoint** from session 2's 63 (`comm -23` = all 8): they are the
   *complementary* second slice of the same advertisement set, not a subset of the 63. Same binaries on both
   boots (Hyprland 0.56.2-4 installed 2026-10-20, xdph 1.4.1-2 installed 2026-10-11), so the set is the same
   ~71 globals on both boots; each session's log exposes about half of it.

A reader must treat **both** sessions as partial views. Session 2's 63 is *also* incomplete (§5).

## 1. What the two records actually contain (measured, not read off the file by eye)

`journalctl --user -u xdg-desktop-portal-hyprland -b -1|0 --no-pager -o json` → per-entry
`__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `MESSAGE`:

| session | boot | pid | app entries | adverts | distinct | ingest clusters (rt / mono / entries / bytes) |
|---|---|---|---|---|---|---|
| 1 | `0a3785aa…95a7` | 1918 | 74 | 15 | 8 | `…875228`/140577868785/39/2034 · `…876044`/140577869602/33/2049 · `…876211`/140577869768/1/42 · `…128363286`/141700356843/1/30 (truncated) |
| 2 | `7ab69ee4…d119b` | 1952 | 73 | 63 | 63 | `…126352`/17675971/37/2044 · `…126792`/17676411/36/1994 |

Session 1: 15 adverts = 9 init-phase adverts (`ext_foreign_toplevel_image_capture_source_manager_v1`,
`ext_image_copy_capture_manager_v1`, `wp_color_manager_v1`, `wp_drm_lease_device_v1` ×2,
`wp_linux_drm_syncobj_manager_v1`, `wl_drm`, `zwp_linux_dmabuf_v1`, `wl_output`) + **6 further `wl_output`
adverts** interleaved with `[core] dmabufFeedbackMainDevice` (13×) and `Found output name DP-1|FALLBACK` (6×).
So even inside the slice, "15 adverts" is not 15 globals.

Session 1's whole retained stream is **4125 bytes** of complete lines; session 2's is **4038 bytes**.
4125 + 4038 = 8163 B ≈ 2 × 4096. `[INFERENCE]` one ~4 KiB stdio block per flush, ~8 KiB for the startup
stream, i.e. session 1's missing flush #1 ≈ session 2's visible flush #1 (63 names / 4038 B).

## 2. The mechanism, step by step, with the evidence for each step

**(a) The portal logs to stdout; nothing in the unit overrides it.**
`systemctl --user cat xdg-desktop-portal-hyprland` shows `Type=dbus`, `ExecStart=/usr/lib/xdg-desktop-portal-hyprland`,
`Restart=on-failure`, and **no `StandardOutput=`** → journal default. The journal entries confirm the transport:
`_TRANSPORT=stdout`, `_STREAM_ID=2abb905525ef4734bf2fc022ac1338ce`, `_COMM=xdg-desktop-por`.

**(b) journald cannot delay: it stamps on receipt.** All 73 of session 1's 13:16:45 entries carry three
monotonic stamps inside **683 µs** (`140577868785` → `140577869768`), and those stamps correspond to
**39.05 h of boot uptime** — the app had been up 39 h. The bytes therefore reached journald in one burst.

**(c) The burst's content is startup-phase output, not 13:16:45 output.** Inside the burst, before any request
traffic, sit `[toplevel] Activated, bound to 55cc6bdd08d0, toplevels: 0`, `[screencopy] Registered for
toplevel export`, `[screenshot] init successful`. These are emitted from `CPortalManager::init()` before
`startEventLoop()` (`xdph-PortalManager.cpp:267-335`), i.e. at process start. The 13:16:45 request traffic
(OnePassword, then three VoiceStudio global-shortcut sessions) appears *later in the same flush*, after
`screenshot] init successful` — the ordering proves the startup lines were produced at startup and merely
*delivered* with the 13:16:45 traffic.

**(d) The slice begins mid-stream.** xdph's startup always emits, in order, `Initializing xdph...`,
`XDG_CURRENT_DESKTOP set to Hyprland`, `Gathering exported interfaces` before the first advert
(`xdph-PortalManager.cpp:291,309`; all three format strings are in the installed binary —
`strings /usr/lib/xdg-desktop-portal-hyprland` lines 2148, 2166, 2331). Counts in the live journal:

| line | boot −1 | boot 0 |
|---|---|---|
| `Initializing xdph` | **0** | 1 |
| `XDG_CURRENT_DESKTOP set to Hyprland` | **0** | 1 |
| `Gathering exported interfaces` | **0** | 1 |

So session 1's record does **not** start at the beginning of the dump: the head was flushed earlier and is gone.

**(e) The slice ends mid-word.** The last pid-1918 entry is 30 bytes, `[LOG] [core] dmabufFeedbackMa` — a line
cut inside the word `dmabufFeedbackMainDevice`, written at 13:35:28 as the unit was stopped. The stream's own
tail was never delivered.

**(f) The head is outside retention, and the removal is dated.** `journalctl --list-boots` (system *and*
`--user` agree) gives boot −1 `FIRST ENTRY Sat 2026-10-24 20:57:12`. The unit's own start time is derivable
from systemd's accounting line at 13:35:28 — `Consumed 43.752s CPU time over 1d 15h 21min 17.607s wall clock time` → start `2026-10-23T22:14:10.393`. Gap = **22 h 43 m 01.6 s** of the unit's stream outside retention.
The audit trail holds exactly one removal:

```
2026-10-25T13:10:39-03:00 plazir27 sudo[3394677]: vgpnk : PWD=/home/vgpnk ; USER=root ; COMMAND=/usr/bin/journalctl --vacuum-size=50M
```

6 m 06 s before the surviving flush. `[INFERENCE]` this vacuum (or earlier automatic size-based vacuuming:
`SystemMaxUse=256M`, `RuntimeMaxUse=64M` in `/etc/systemd/journald.conf.d/size.conf`, usage now 37 M) removed
flush #1. Either way the head is gone; the surviving slice cannot be a prefix.

**(g) Rate limiting is excluded.** `/etc/systemd/journald.conf` has `#RateLimitIntervalSec=30s` /
`#RateLimitBurst=10000` commented out (defaults, far above 73 lines). No suppression message mentions the unit:
`journalctl --user -b -1 | grep -iE 'suppress|rate.?limit|dropped'` yields 27 hits, **0** of which concern the
portal (all are `hermes[…]: … 429 Rate limit reached`, an unrelated HTTP client).

## 3. Why it is not the other two hypotheses

**Not "rotation truncated a complete census."** A rotation-truncated record loses its *tail* and still starts
with `Initializing xdph…`. Session 1 starts mid-dump (§2d) and ends mid-word (§2e) — head lost to retention,
tail lost to the buffered writer. It is a **slice**, not a truncated whole.

**Not "a partial registry / portal restarted early."** One process, one invocation, no second dump:
`_PID=1918` for all 74 app entries, `_SYSTEMD_INVOCATION_ID=bc8d69b032e14cb88937a64b0ee7b5a0` is the **only**
invocation id in boot −1, and systemd accounts a single continuous run of 39 h 21 m. `onGlobal`
(`xdph-PortalManager.cpp:85-88`) logs every registry global exactly once per registry event, so a restart would
show a second `Gathering exported interfaces` + a second full dump; there is none.

**Not "the portal really bound a smaller registry."** The 8 names are not a subset of session 2's 63:

```
comm -23 <session-1 names> <session-2 names>   →  all 8
```

Every one of `ext_foreign_toplevel_image_capture_source_manager_v1`, `ext_image_copy_capture_manager_v1`,
`wl_drm`, `wl_output`, `wp_color_manager_v1`, `wp_drm_lease_device_v1`, `wp_linux_drm_syncobj_manager_v1`,
`zwp_linux_dmabuf_v1` is **absent** from the 63. Both boots ran the same binaries (`pacman -Qi`: hyprland
`0.56.2-4`, install date 2026-10-20 09:16:38; xdg-desktop-portal-hyprland `1.4.1-2`, 2026-10-11 16:14:39 —
both *before* boot −1). The two visible sets are complementary halves of one ~71-global advertisement:
63 flushed at start in session 2, 8 flushed late in session 1.

## 4. What a reader of the census must NOT conclude from session 1

1. **Must not** conclude the compositor advertised only 8 globals at boot −1, or that the portal bound a
   partial/smaller registry. The portal bound the full registry; the log exposes one flush of it.
2. **Must not** conclude the registry "grew from 8 to 63" across the reboot, nor infer a Hyprland upgrade: the
   binaries are identical (§3) and the two numbers are slices, not snapshots.
3. **Must not** use session 1 for any **negative existence** claim. In particular
   `hyprland_focus_grab_manager_v1` has 0 hits in boot −1 — that is an artifact of the missing flush, **not**
   evidence that focus-grab was unadvertised before the reboot. C2's advertisement fact rests on session 2 only
   and must not be contrasted with session 1.
4. **Must not** read session 1's timestamps as event times. All 13:16:45 values are *flush* times; the content
   spans 2026-10-23T22:14 → 2026-10-25T13:16:45.
5. **Must not** treat session 1 as a prefix of session 2's list, or compare orderings: the slice starts
   mid-stream, so ordering and completeness carry no information.
6. **Must not** equate `adverts` with globals. Session 1 has 15 adverts for 8 names (7 × `wl_output`, 2 ×
   `wp_drm_lease_device_v1`); `onGlobalRemoved()` (`xdph-PortalManager.cpp:263-265`) contains **no** log call,
   so output add/remove cycles are invisible and repeated names cannot be counted as simultaneous outputs
   (`Found output name` shows only `DP-1` and the synthetic `FALLBACK`).
7. **Must not** run `--diff` between session 1 and session 2 as a registry delta. The frozen counter models a
   session as "or its PID differs from the open session's PID" (`quality/counters/c1-r41-globals.py:33-35`) and
   emits `MADO_GLOBALS_DIFF: from=<k-1> to=<k> added=<csv|-> removed=<csv|->` (line 43). On this journal that yields
   `added=<63 names> removed=<8 names>` — a pure flush-boundary artifact, not a protocol change.

## 5. Session 2 is incomplete too (this is the same defect, not a different one)

Session 2's 63 names contain **no `wl_output` and no `zwp_linux_dmabuf_v1`**, yet:

- boot 0's compositor has a live output — `/run/user/1000/hypr/efb5099…/hyprland.log`:
  `drm: Connecting connector DP-1, CRTC ID 205` / `drm: Description LG Electronics LG ULTRAWIDE …` — so
  `wl_output` must be advertised;
- `zwp_linux_dmabuf_v1` was advertised and bound on boot −1 (`Got interface: zwp_linux_dmabuf_v1 (ver 5)` +
  13 × `dmabufFeedbackMainDevice`), and `onGlobal` binds it for the dmabuf-feedback path
  (`xdph-PortalManager.cpp:123-129`) under the same binary.

Session 2's stream stops exactly at a flush boundary: 4038 B of complete lines, last entry
`Got interface: ext_output_image_capture_source_manager_v1 (ver 1)`, and **nothing has been added since
13:36:24** (still 75 lines at 19:59, 6 h 23 m later) — the remaining ~2-4 KiB is sitting in the process's
stdio buffer, exactly as session 1's second slice sat for 39 h.

**Falsifiable prediction:** the next time the portal writes enough to fill that buffer (any portal request
burst), boot 0's journal will gain the missing DRM/capture globals (`wl_output`, `zwp_linux_dmabuf_v1`,
`wp_drm_lease_device_v1`, `wl_drm`, …) under a single new timestamp. If instead nothing appears after a busy
portal day, the buffering model is wrong and must be replaced.

**Operational consequence for C1:** `--expect NAME` and the "latest session only" per-name table read the
buffered remainder as absence. `--expect zwp_linux_dmabuf_v1` (or `--expect wl_output`) against this journal
will report `MISSING_EXPECTED` while the compositor does advertise it. That is a tool-vs-journal limitation, not
a compositor fact; a census that needs an authoritative set must force a flush (or read the compositor's
registry), not trust one session.

## 6. Answers to the specific probes the ticket named

One advert line per registry event is guaranteed by the code: `onGlobal` calls
`Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version)` before any bind
(`xdph-PortalManager.cpp:88`), and the installed binary carries that format string exactly once
(`strings /usr/lib/xdg-desktop-portal-hyprland` line 2148).

| probe | result |
|---|---|
| `journalctl --list-boots` | 2 boots: −1 `0a3785aa…95a7` 2026-10-24 20:57:12 → 2026-10-25 13:35:39; 0 `7ab69ee4…d119b` from 13:36:19 |
| `journalctl --user --disk-usage` | `37M` (limit 256 M → not currently size-pressured) |
| `journalctl --user -u … -b -1 \| wc -l` | **77** (74 app + 3 systemd) — the whole boot −1 record for this unit |
| retention config | `/etc/systemd/journald.conf` all defaults; drop-in `size.conf`: `SystemMaxUse=256M`, `RuntimeMaxUse=64M`; no `RateLimit*` set |
| unit start lines / status | unit started 2026-10-23T22:14:10.393 (derived from the `Consumed … 1d 15h 21min 17.607s` line); stopped 13:35:28; single invocation `bc8d69b0…`; no `StandardOutput=` in the unit |
| xdph advert code | `onGlobal` logs every global then binds it (quoted above, `:85-88`); one registry (`:299-301`), three roundtrips (`:311,314,335`); `onGlobalRemoved` silent, `:263-265` |

## 7. Reproduction (read-only; nothing was mutated)

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/fetch
sha256sum xdph-journal.txt                      # bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7
journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o short-iso | wc -l    # 77
journalctl --user -u xdg-desktop-portal-hyprland -b 0  --no-pager -o short-iso | wc -l    # 75
diff <(awk 'NR<=77' xdph-journal.txt) <(journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o short-iso)  # identical
diff <(awk 'NR>78'  xdph-journal.txt) <(journalctl --user -u xdg-desktop-portal-hyprland -b 0  --no-pager -o short-iso)  # identical
journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o json | python3 -c '<per-entry MESSAGE byte sums per __REALTIME_TIMESTAMP>'   # §1 table
journalctl --user --list-boots --no-pager        # boot -1 FIRST ENTRY 2026-10-24 20:57:12
journalctl --no-pager -o short-iso | grep -i 'vacuum-size'   # 2026-10-25T13:10:39 sudo … --vacuum-size=50M
```

Every number in this file comes from one of those commands; the only items marked `[INFERENCE]` are the
~4 KiB stdio-block attribution, the assignment of the missing head to the 13:10:39 vacuum (vs earlier automatic
vacuuming), and the hotplug reading of the 6 post-init `wl_output` adverts.
