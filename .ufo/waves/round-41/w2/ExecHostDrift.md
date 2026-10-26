# ExecHostDrift — w2 report (round 41, mado)

**Attack target:** the entry's host claims are a dated measurement — has the host moved?
**Verdict: no defect found.** All dated host claims in `corpus/knowledge/hyprland-focus-grab-r41.md` (DATA commit 07f2641696) were re-measured today, 2026-10-25, and remain true. No drift detected on any read-only axis.

**What was run (reproduction):**
1. `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` (fresh capture, saved to `w2/ExecHostDrift/xdph-journal-now.txt`) → **byte-identical** to the fetch receipt `fetch/xdph-journal.txt` (153 lines / 19130 bytes; sha256 `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7` on both). No new sessions/adverts/restarts in ~7 h.
2. Delivered tool on both journals (`python3 -I tool-datacommit.py --journal-file <each>`; data-commit extraction sha256 `286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`, byte-identical to working tree and v2 reference) → identical output on both, exit 0, `verdict=OK`, `sessions=2 latest_pid=1952 interfaces=63 expected_missing=- ignored=0`; `--expect hyprland_focus_grab_manager_v1 --expect hyprland_input_capture_manager_v1` → OK.
3. `hyprctl version` → `Hyprland 0.56.2 … at commit efb50993780079460b0cbed1363e2166a2de1d9f` — verbatim match with the entry's dated read.
4. `pgrep -af xdg-desktop-portal-hyprland` → `1952 /usr/lib/xdg-desktop-portal-hyprland`; `systemctl --user status` → active since Sun 2026-10-25 13:36:24, Main PID 1952 (same process as journal session 2). `journalctl --list-boots` → boots 0a3785aa… / 7ab69ee…, unchanged.
5. Package record `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc` sha256 `7bf2f8beeadf189be54460a72700f81722d9be78884a0a8ee56a46a70c9445a5` — identical to the S037 receipt; version still 1.4.1-2.
6. Internal counts reproduced on the fresh capture: `Got interface:` = 78 (15+63), `focus` (case-insensitive) = 1, only on the advert line — matching entry lines 63 and 71.

**Statement-by-statement:** entry lines 9, 10, 11, 61, 63, 65, 71, 73, 77, 79 all still true (table in `w2/ExecHostDrift/drift.md`). The entry itself flags the version read as a dated measurement (line 77); §7's "one host, one day, two portal sessions — re-run the census, never reuse the counts" caveat still holds.

**Files changed (only my seat):** `.ufo/waves/round-41/w2/ExecHostDrift/drift.md` (findings), plus scratch copies in the same seat dir (`tool-datacommit.py`, `xdph-journal-now.txt`, `entry-datacommit.md`, `lesson-datacommit.md`, `readme-datacommit.md`). No fetch/ files touched; no tracked lane files edited; no git mutations; no tools installed; no package transactions.

**Checkpoints for main agent:** none required for my seat (no defect); the C1/C2 counters can run as-is — host-side inputs are unchanged.
