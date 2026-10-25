# ExecJournalHistory — DONE

Seat of round 41 / w1. Target: **why the first journal session lists only 8 interfaces.**
Deliverable: `.ufo/waves/round-41/w1/ExecJournalHistory/finding.md`
Quote gate: `.ufo/waves/round-41/w1/ExecJournalHistory/verify-quotes.sh` → **12 quotes, 0 failures**.

## Verdict

Session 1 (pid 1918) is **not** a registry that lost its tail to rotation, **not** a portal that restarted early
or bound a smaller registry. It is a **fragment of a block-buffered stdout stream**:

1. xdph logs to a pipe (`_TRANSPORT=stdout`, `_STREAM_ID=2abb905525ef4734bf2fc022ac1338ce`; unit has no
   `StandardOutput=`), so libc block-buffers it and journald receives **~4 KiB flushes**, stamped with the
   **flush** instant.
2. All 73 entries dated `13:16:45` were ingested in 683 µs (three reads: 2034 + 2049 + 42 B), 39 h 02 m after
   the portal started — and they contain *startup-phase* lines (`[toplevel] Activated`, `[screencopy] Registered
   for toplevel export`, `[screenshot] init successful`, all from `init()` before `startEventLoop()`).
3. That same stream's **first** flush (the registry-census head, ingested at unit start 2026-10-23T22:14:10) is
   outside journal retention: the user journal retains nothing older than **2026-10-24T20:57:12**, i.e.
   **22 h 43 m 01.6 s** of the unit's 39 h 21 m life is gone. The only recorded removal is an explicit
   `journalctl --vacuum-size=50M` at **2026-10-25T13:10:39** — six minutes before the surviving flush.
4. Hence the 8 names are **disjoint** from session 2's 63 (`comm -23` = all 8): they are the complementary
   second slice of one ~71-global advertisement, not a subset. Same binaries on both boots (hyprland `0.56.2-4`
   installed 2026-10-20; xdph `1.4.1-2` installed 2026-10-11), so no version drift is involved.

Session 2's 63 is **also incomplete** — it has no `wl_output` and no `zwp_linux_dmabuf_v1` although boot 0's
compositor has a live DP-1 (`hyprland.log`: `drm: Connecting connector DP-1, CRTC ID 205`) and boot −1 bound
`Got interface: zwp_linux_dmabuf_v1 (ver 5)`. Its stream stopped at a flush boundary at 13:36:24 and has not
grown since (still 75 lines at 19:59). **Falsifiable prediction:** the next ~4 KiB of portal output will add
those globals under one new timestamp.

## What a reader must NOT conclude from session 1

1. Not "the compositor advertised only 8 globals" / "the portal saw a smaller registry".
2. Not "the registry grew 8 → 63 across the reboot" (no upgrade; complementary slices).
3. **No negative existence claims.** `hyprland_focus_grab_manager_v1` has 0 hits in boot −1 — an artifact, not
   evidence that focus-grab was unadvertised before the reboot.
4. Not that session 1's timestamps are event times (all `13:16:45` are flush times; content spans
   10-23T22:14 → 10-25T13:16:45).
5. Not that session 1 is a prefix of session 2's list (it starts mid-stream; order/completeness carry nothing).
6. Not `adverts` = globals: 15 adverts / 8 names (7 × `wl_output`, 2 × `wp_drm_lease_device_v1`);
   `onGlobalRemoved` (`xdph-PortalManager.cpp:263-265`) logs nothing, so add/remove cycles are invisible.
7. Not a registry delta from `--diff`: the frozen counter models sessions by PID/boot
   (`c1-r41-globals.py:33-35`) and emits `MADO_GLOBALS_DIFF: from=<k-1> to=<k> added=<csv|-> removed=<csv|->`
   (line 43); on this journal that is `added=<63> removed=<8>` — a flush artifact.

## Impact on the two claims

- **C1 (operability):** supports the tool's premise (the journal does carry adverts) but **attacks** any reading
  of per-session `interfaces=`/`adverts=` as registry facts, and warns that `--expect wl_output` /
  `--expect zwp_linux_dmabuf_v1` on this journal can yield a **false `MISSING_EXPECTED`** from the buffered
  remainder. `--diff` between the two sessions is meaningless here.
- **C2 (coverage):** the one `hyprland_focus_grab_manager_v1` advert at 2026-10-25T13:36:24 pid 1952 stands and
  is the *only* admissible advertisement evidence; session 1 must not be cited for or against availability.

## Files written (all inside my seat; nothing else touched)

- `.ufo/waves/round-41/w1/ExecJournalHistory.md` (this report)
- `.ufo/waves/round-41/w1/ExecJournalHistory/finding.md`
- `.ufo/waves/round-41/w1/ExecJournalHistory/verify-quotes.sh`

## Retained evidence (exact commands)

```bash
journalctl --list-boots --no-pager                      # boot -1 FIRST ENTRY 2026-10-24 20:57:12
journalctl --user --list-boots --no-pager               # same boundary for the user journal
journalctl --user --disk-usage                          # 37M
journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o short-iso | wc -l   # 77
journalctl --user -u xdg-desktop-portal-hyprland -b 0  --no-pager -o short-iso | wc -l   # 75
journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o verbose | grep _SYSTEMD_INVOCATION_ID | sort -u
                                                        # one invocation bc8d69b0… (no restart)
journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o json   # per-entry byte sums per ingest instant
journalctl --no-pager -o short-iso | grep -i 'vacuum-size'   # 2026-10-25T13:10:39 … --vacuum-size=50M
systemctl --user status xdg-desktop-portal-hyprland --no-pager ; systemctl --user cat xdg-desktop-portal-hyprland
cat /etc/systemd/journald.conf.d/size.conf              # SystemMaxUse=256M RuntimeMaxUse=64M
pacman -Qi hyprland xdg-desktop-portal-hyprland         # query only; versions + install dates
hyprctl version                                         # 0.56.2 @ efb50993780079460b0cbed1363e2166a2de1d9f
strings -a /usr/lib/xdg-desktop-portal-hyprland         # 1× "| Got interface: {} (ver {})"
grep -icE 'suppress|rate.?limit|dropped'                # 27 hits, 0 concerning the portal (hermes 429s)
```

`sha256sum .ufo/waves/round-41/fetch/xdph-journal.txt` =
`bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7`; both blocks `diff`-identical to the live
journal.

## Tooling / safety

- No tools installed or updated (nothing needed). No `pacman` transaction; `pacman -Qi` is a read-only query.
- Journal verbs used: read-only `journalctl` (`--list-boots`, `--disk-usage`, `-u`, `-b`, `--file`, `-o …`) only.
  `hyprctl version` only (no compositor socket client, no input injection).
- No mutating git/jj, no writes outside `.ufo/waves/round-41/w1/ExecJournalHistory*`.

## Risks / caveats left for the L1

- `[INFERENCE]` items, each labelled in the finding: the ~4 KiB stdio-block attribution (measured sizes 4038 B /
  4125 B support it), the assignment of the missing head to the 13:10:39 vacuum (vs earlier automatic
  size-based vacuuming — the head is gone either way), and the hotplug reading of the 6 post-init `wl_output`
  adverts (boot −1's Hyprland output history is not recoverable).
- Checks the main agent can run: `bash .ufo/waves/round-41/w1/ExecJournalHistory/verify-quotes.sh` (green here),
  and — when the C1 counter seat is done — confirm whether its `--diff` output reproduces the predicted
  `added=<63> removed=<8>` artifact.
