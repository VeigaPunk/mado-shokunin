# R54W2Seat04 — C1 P20 interior-whitespace mutation

## Finding

No actionable defect found in the frozen requirement: P20 interior whitespace drift MUST be rejected. The w1 report records an exercised draft-counter case where changing an interior space in the P20 quote produced `quotes=3, anchors=3`, rejected; it also records that trailing spaces are intentionally tolerated while interior spaces are not. This is evidence about the w1 scratch draft, not the current landed counter.

## Frozen contract and pin evidence

`registration.md` lines 21–23 requires the P19–P22 entry rows to match the frozen table “byte-for-byte modulo trailing spaces” and says any drift is `TARGET_MISSED`. Lines 25–30 give P20’s exact quote as ``g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);`` at anchor `:1576`; lines 32–34 require it at exactly line 1576. Thus the requested mutation (e.g. replacing the interior `, ` with `,  `) is not a permissible trailing-space difference. It also ceases to match the source pin verbatim at that anchor. The actual pin line is `    g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);`; its recorded SHA-256 is `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`.

Relevant prior evidence: `w1/R54Seat04.md` lines 180–196, especially lines 192–195, lists shortened P20 quote, interior-space change, leading space, and trailing spaces, with the interior-space mutation rejected (`quotes=3, anchors=3`) and trailing spaces tolerated. W1 lines 21–23 describe its scratch-only counter draft, so those results do not establish behavior of a landed counter.

## W2 execution / limitation

Checked for the prescribed executable: `find /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters -maxdepth 1 -name '*r54*' -type f -printf '%f\\n' | wc -l` → `0` (exit 0). Therefore the pinned command `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` is **NOT RUN / absent**. No substitute evaluator or synthetic counter result is claimed. The assignment’s requested mutation test against the current counter cannot be completed until that counter exists. The exact required rejection follows from the frozen contract, but current implementation behavior remains unverified.

Pin check command/output:

```text
$ sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
 a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
exit=0

$ sed -n '1576p' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
    g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
exit=0
```

## Residual risk and verification gaps

Current landed-counter response to an interior P20 whitespace mutation is unverified because the counter is absent. W1’s independently reported draft test is consistent with the frozen contract but is not a rerun of a pinned current executable. No control counter was available.

## Trailer

Relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`:
- Report: `.ufo/waves/round-54/w2/R54W2Seat04.md`
- Scratch: `/fast/scratch/hyaku/mado-r54/R54W2Seat04` (removed before yield)
- Scratch remaining: none; ENOSPC: none.
