# ExecErrataR1 — R1 (round-46 erratum draft) falsified by command

Seat `ExecErrataR1`, mado round 47 wave w2 (policy v1, falsify). Target:
`.ufo/waves/round-47/w1/ScrErrataR1/erratum.md` (= the R1 erratum on `corpus/knowledge/hyprland-input-devices-r46.md:57`).
Full per-sentence work, hashes and reproduce lines: `.ufo/waves/round-47/w2/ExecErrataR1/verdicts.md`.
Driver + receipt: `.ufo/waves/round-47/w2/ExecErrataR1/verify-r1.sh` →
`.ufo/waves/round-47/w2/ExecErrataR1/receipts/verify-r1.out` (`VERIFY-R1: 77/77 passed`, rc 0;
receipt `sha256 02e036e1c2ec61cddee391e4d97464679f9b7e22a734f7146bdf12fc410ef9ad`, driver
`sha256 27e42e6a9cdb170ad5242055399a730fc10afbd10bb3ace7c9ac3aed4dd2bf67`).

Quotes judged (both <= 25 words, locators computed):

- `hyprland-input-devices-r46.md:57` — one `input` block in `~/.config/hypr/input.conf`, no `device` block — 8 words,
  the clause the erratum corrects.
- `live-devices-host-r46.txt:5` — # chain: ~/.config/hypr/hyprland.conf sources the omarchy default input.conf before the user's input.conf — 12 words, the chain the erratum adopts.

Scope read: `mado-shokunin` lane only; lane not edited; host config and compositor read-only
(`hyprctl version`, `hyprctl -j getoption …`, `hyprctl devices -j`); scratch deleted; no GUI program, no package
transaction, no `~/.cache/xdg-terminal-exec` touch.

## Answer

The draft's facts re-derive exactly; its **framing is wrong twice** and one assertion lacks its witness.

| unit | verdict |
|---|---|
| producing tools (V9, V10) | **CONFIRMED** — `tools/mado-devices.py` = `3a803689…` in the worktree and at `git show` of `1001bda0`, `60edb66e`, `d7527d60`, `9bddd6ac`, `c24adef2`; `l1-draft/mado-devices.py` = `b229efd0…` (worktree = `git show 1001bda0:`); l1 receipt `d635baec…`, r46 receipt `0c749e1d…` (both worktree = committed). The w1 `verify.sh` hashed the worktree only; the `git show` column is the check it lacked, and it passes. |
| config count (V1a, V2–V5, V8) | **CONFIRMED, stronger** — r46 run passes 2 `--config` (`:6`, headers `:3-4`), l1 run 1 (`:4`, header `:3`); the depth-4 source closure of `~/.config/hypr/hyprland.conf` is **40 files, exactly 2 with an `input` block, 0 with a `device` block, `kb_layout` at exactly those two sites** (`us` at omarchy `:3`, `br` at user `:10`); sources at `hyprland.conf:11` and `:17`, both hashes as tabled. |
| draft→landed delta (V10) | **CONFIRMED** — 30 removed / 105 added / 9 hunks, 566 → 641 lines; the erratum's parenthetical is complete (a 768-byte display cut made it look truncated; the bytes read `30 removed, 105 added, 9 hunks`). |
| merge order (V6, V7) | **CONFIRMED by experiment** — two-config → `br`; reversed → `us`, `agree=0 differ=9 DIFFER`; omarchy only → `us`; `:418-419` and `:334` are the exact lines; `hyprctl -j getoption input:kb_layout` = `br` with `set: true`. |
| `:3` "the citation names the wrong receipt" | **WRONG as phrased** (F2) — the cited l1 receipt names its own producer and prints the numbers `:57` prints; the landed tool reproduces them line for line today. The class is producer identity (stale producer), and `corpus/lessons/round-46-verifier-spotcheck.md:52` already says "both receipts print the same summary line, so the sentence's content holds". |
| `:18` "the observation itself" [stands] | **WRONG at the tip** (F1) — same-day re-run gives `keyboards=9 … virtual=0`; both receipts record `keyboards=10 … virtual=1`, and the `hl-virtual-keyboard-fcitx5` line is absent. |
| `:14` "two `input` blocks reach the compositor" | **CONFIRMED, witness supplied** (F3) — `hyprctl -j getoption misc:key_press_enables_dpms` = `{"int": 1, "set": true}`; that key is set only by `~/.local/share/omarchy/default/hypr/input.conf:19` in the whole closure, so the compositor parses that file and its `input` block. |
| remaining units (V1c, V12–V15) | **CONFIRMED** — one citation site at `:57`; 14 device lines / 10 / 9 / 1 / 4 / `verdict=OK` in both receipts; landed = draft on identical argv; selftest line 1 vs 0 (the draft does implement `--selftest`, so the omission was the run's). |

## Holes to close before the data commit

1. **F1 (must fix)** — the erratum re-asserts a live observation that no longer reproduces on the same day. The
   entry is present tense under `verified-at: 2026-10-26` with `recheck: on-release`; the virtual keyboard is
   session-state-conditioned, so a release-triggered recheck would never fire on this drift. Land the live sentence
   as a dated, session-qualified observation instead of "the observation itself".
2. **F2 (wording)** — "the citation names the wrong receipt" overstates. Say: the entry cites a receipt produced by
   the pre-landing draft (`b229efd0…`, one `--config`), not by the landed tool (`3a803689…`, two configs); the
   content holds under either. Also worth one line in the errata ledger: QUALITY 24 as worded is satisfied by the l1
   receipt (its bytes do name a producer), which is why it missed this; criterion 79 is satisfied after the swap,
   since the r46 receipt is committed at `1001bda0`.
3. **F3 (evidence)** — add the `getoption misc:key_press_enables_dpms` read so "reach the compositor" is observed,
   not inferred from two file hashes.

## Reproduce

```
bash .ufo/waves/round-47/w2/ExecErrataR1/verify-r1.sh
git -C <lane> show 1001bda0:tools/mado-devices.py | sha256sum
hyprctl -j getoption misc:key_press_enables_dpms
hyprctl devices -j > $WORK/d.json && python3 -I tools/mado-devices.py --devices $WORK/d.json --config <user> --config <omarchy>
```

## Not done (out of this seat's scope)

No lane file edited, no commit, no counter scored, no claim judged. The dump, the closure list and the run outputs
stayed in scratch and are deleted; only `MADO_*` summary lines and the hashes appear in the receipt.
