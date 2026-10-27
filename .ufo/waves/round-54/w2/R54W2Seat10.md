# R54W2Seat10 — item 10: C1 absolute manifest paths

**Axis:** operability (C1 record-instrument claim). **Verdict:** the absolute-path trap is independently reproduced in an isolated clone. Any counter that opens SHA256SUMS paths literally instead of reading the scored Git blob can admit a forged pin. The actual pinned C1 counter was absent, so its behavior is **NOT RUN**; this establishes the failure mode, not that an unavailable implementation exhibited it.

## Frozen contract and pin evidence

- `claims-frozen.md:19-30` requires the counter at the scored revision to verify the four proposition quotes, their anchors, and that each pin's bytes hash to the round-52 recorded digest. The C1 `before` state at `claims-frozen.md:32-34` is counter absent.
- `registration.md:11-19` names the round-52 pins and frozen digests; `registration.md:21-34` gives the frozen propositions and exact spans: P19 `Hyprland-ConfigActions.cpp:1554-1558`, P20 `:1576`, P21 `Hyprland-legacy-DispatcherTranslator.cpp:619-622`, P22 `:573-574`. The attacked P19 span in the base blob is exactly:
  ```
  1554:     g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
  1555:
  1556:     if (S.m_passPressed == 1) {
  1557:         if (!isMouse)
  1558:             g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
  ```
- `registration.md:36-38` explicitly requires controls to be mutated copies of the scored tree and says the counter reads inputs from `--repo`/`--rev` Git objects. Its C1-CTL-3 hash tamper is at `registration.md:40-47`.
- Relevant w1 evidence: `w1/R54Seat03.md:167-190` documents the absolute-path trap and measures an admitted forged pin under path resolution (`P2 ... -> ADMIT`) versus tree-blob rejection; `w1/R54Seat01.md:205-236` describes the same pin-edit laundering case and the basename + frozen-digest mitigation.

## Isolated reproduction

Scratch was `/fast/scratch/hyaku/mado-r54/R54W2Seat10`; fixture `D=/fast/scratch/hyaku/mado-r54/R54W2Seat10/fixture-ckazc5gr`. I cloned the lane with shared objects, checked out frozen base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`, appended a comment to the fixture's P19 pin, and committed only inside D. Before the commit, `git -C D rev-parse --show-toplevel` printed exactly D. No lane/frozen file was changed.

Relevant exact commands and results (all Git commands were `git -C D ...`):

- `git -C D clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin .` → `Cloning into '.'... done.`; exit 0.
- `git -C D checkout --detach e25149fec8152a3aabd2b18a0ee8663b23cf65aa` → `HEAD is now at e25149fe round-53 verifier spot-check (integrator, hyaku): non-author admit/reject`; exit 0.
- `git -C D rev-parse --show-toplevel` → `/fast/scratch/hyaku/mado-r54/R54W2Seat10/fixture-ckazc5gr`; exit 0.
- `git -C D show e25149fec8152a3aabd2b18a0ee8663b23cf65aa:.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` → exit 0; SHA-256 of returned Git blob: `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`, matching the frozen P19 pin digest.
- Fixture-only mutation: appended `\n// scratch pin mutation for R54W2Seat10\n` to that pin; `git -C D add -- .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` → exit 0.
- Pre-commit `git -C D rev-parse --show-toplevel` again printed D; exit 0. Fixture-local identity was configured, then `git -C D commit -m 'fixture: mutate pinned blob'` → `[detached HEAD ef94a4d7] fixture: mutate pinned blob` / `1 file changed, 2 insertions(+)`; exit 0.
- `git -C D rev-parse HEAD` → `ef94a4d7fa292dd0377dd7299d30fe23fb29a8c1`; exit 0.
- `git -C D show ef94a4d7fa292dd0377dd7299d30fe23fb29a8c1:.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` → exit 0. SHA-256 of returned scored Git blob: `7bdae45af782b57b7d784ed25c4bb7edcf7634dc05c621a3e72ac6812625b507`, not the frozen digest.
- The manifest line in the cloned base was exactly `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`; the recorded path is absolute. Reading that recorded path yielded SHA-256 `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637` (the pristine lane file), while the scored commit's P19 pin blob hashes to `7bdae45a...`. Thus literal manifest-path resolution reads outside the scored clone and misses the mutation; `git show <scored-rev>:<pin>` detects it.

**Counter command:** frozen command is `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` (`claims-frozen.md:20`). Exact path read returned `Path '/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r54-errata-truth.py' not found`; **NOT RUN / absent**, no exit code. No other counter command was substituted. The `lsp` status lookup returned `Tool 'lsp' has no doc topics`; no LSP server was available.

## Finding and residual risk

**Confirmed failure mode (high impact if implemented):** a counter resolving the manifest's absolute filename literally can compare the pristine lane file to the recorded digest while the `--rev` Git blob is mutated, allowing pin-byte laundering and violating the scored-Git-object requirement. The required remedy follows the frozen contract: resolve the pin by basename within the scored revision, read its bytes from Git objects at `--rev`, and compare against the frozen round-52 digest (not merely the tree's self-reported manifest).

**Residual / verification gap:** the counter is absent, so whether the eventual implementation rejects this fixture cannot be determined here. No predicate or registration edit is proposed. No tests beyond this isolated Git-blob/path-resolution probe were run.

Scratch cleanup: `/fast/scratch/hyaku/mado-r54/R54W2Seat10` removed before yield; no scratch remains; ENOSPC was not observed.
