# Safety — scoped report (round 13, w1)

Full findings, anchors and source opens are in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/Safety.md`.
Gate anchors are at snapshot tag `3D69` of `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`.

- **F1 MEDIUM, remediated in-wave.** The GlobalCapture seat left two copies of the unfiltered `wayland-info` dump in `/tmp`:
  `/tmp/wayland-info.raw` and an undocumented `.2.raw`, 68256 B each, mode 0644. Shape-only counts: 651 detail lines, including
  make/model, description and device-path lines. I messaged the owner, who deleted both files. `ls /tmp/wayland-info*` now
  reports "No such file". `globals.json` is clean: only the keys `interface`/`version`, all 72 names valid, and `set_sha256`
  replays.
- **F2–F6 LOW/INFO (wayland-info 1.3.0, commit `d01edd68`).**
  - F2: the tool binds 10 interfaces however `-i` is set; the filter only gates printing (`wayland-info.c:3163`). Binding the
    lease device brings a non-master DRM fd. The probe is a read-only observational client, not a "pure read".
  - F3: rc 0 does not prove the enumeration is complete, because the `wl_display_roundtrip` return value is ignored
    (`:3258`, `:3267`). Admit a capture only when rc is 0, stderr is empty and `wl_compositor` is present.
  - F4: a compositor string containing a newline could forge a header line. The parser should fail closed.
  - F5: the capture records no check that the `hyprctl` instance and `WAYLAND_DISPLAY` are the same compositor.
  - F6: the safety of the projection depends on the tool version. 1.3.0 binds no toplevel or title globals; pin it and
    re-review on upgrade.
- **F7 LOW.** `LocalSurface.md` describes file contents and sizes, which is beyond "names + source declarations". It also says
  "verified by measure.py", which nobody ran, and it overstates the baseline source-substitution false-green: `include_graph`
  already FAILed on it.
- **F8 LOW, pre-existing.** `boundary_hash` (`:222-229`) hashes 142 files across all of `~/.config`. An unrelated writer during
  the run gives a false DIVERGED blamed on the gate. Scoping the hash to the declared planes is an L1 decision and moves the PIN.
- **F9 and F10, fixed in-flight by GateImplement after my message.**
  - F9: the `&`/patsub bug is fixed (`x="$ROOT${t#\~}"`, `:2367-2370`).
  - F10: local census names now print through `%q` (`:2416`, `:2422`). Source-line text in the `include_graph`/`sources_resolve`
    details is still raw, but the snapshot fails closed on a forged row.
- **F11–F13 LOW.**
  - F11: 8 stale `/tmp/w5-mado-m52-selftest.*` dirs. There is no trap, and the recut path bypasses the guarded cleanup.
  - F12: fixed in-flight by GateImplement. The scenario-F cleanup is now prefix-guarded (`:1018-1020` @ `57C6`). `PIN_MADO`
    is untouched, so the re-cut is still owed.
  - F13: `--snapshot` has a TOCTOU gap, then writes with a symlink-following `>`. Fix: `set -C`.
- **F14/F15 INFO, positive.**
  - N1–N4 fixture writes stay inside `$T/census`, and `$A` carries only relative symlinks.
  - Each `cp -a "$OMR"` copy re-points the absolute symlink before any write.
  - `measure.py` uses an auto-cleaned TemporaryDirectory.
  - `MistakeFix.py` writes nothing.

No raw session data was captured by this seat. I installed nothing and ran no tests, builds or gate runs.
