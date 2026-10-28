## Joining the declaration to the live read (the round-55 tool)

`tools/mado-kbdopts.py` (round 55, claim C2) models the config half of this chain for config text a caller supplies — device
value when the block set it, else the global option, else the table default (K16, K13-K15), integers as the hyprlang parser
reads them — and joins the result to the JSON that `hyprctl getoption <name> -j` prints. Receipt, read-only, 2026-10-28:
`.ufo/waves/round-55/receipts/live-kbdopts.txt`. For `~/.config/hypr/input.conf` (byte-equal to the committed pin, `cmp`) and
two keyboard names from `hyprctl devices -j` it prints `repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0`
for both and `AGREE` three times against the live read (the committed H04-H06 lines).

How to read that output without overclaiming:

- The host config holds no `device` block (`grep -rnE 'device\[|device \{|device\{' ~/.config/hypr` → no match, receipt
  `.ufo/waves/round-55/w1/R55ScoutHost/receipts-cmp-grep.txt`), so the K16 rule (read at source level) predicts the global
  value for every keyboard; the two per-keyboard lines are that prediction from the file bytes, [INFERENCE] about the running
  compositor, not an observed per-keyboard value. The tool is only given `input.conf`: a `source =` line is skipped without a
  count, so a value set in a file the caller did not pass is invisible to it.
- `getoption` returns an option by name. [INFERENCE] It takes no device argument, so `AGREE` says the running compositor's
  global option equals the declared one; it cannot show a device override (the reply forms are held in
  `hyprctl-getoption-native-forms-r40.md`, not re-claimed here).
- The `numLock` field of `hyprctl devices -j` is lock state, not this option (`hyprland-input-devices-r46.md` step 5); the
  tool never compares them.
- `hyprland-input-devices-r46.md:70` lists these three options as applied per device and not printed by the `hyprctl devices`
  dump (which prints lock state and libinput's default speed instead); K01-K03 and K08 now show the per-device read at source
  level and that sentence stays as history. The global `getoption -j` read does return all three (H04-H06); neither read
  prints a per-device value.
- The tool's `unsupported` count is its honesty valve, and it must be read FIRST: a value outside the modelled token set
  (`$` variables, `device[...]` bracket forms, hex or signed numbers, `##`) or outside the ranges it applies is counted and
  ignored, so the value it then prints is the default or an earlier line, NOT what Hyprland stores, and an `AGREE` against the
  live read is then unreliable (R55W2AuditF: `repeat_rate = 201` prints 25 and `AGREE` against a live 25). The ranges are the
  lane's modelling rule: K15 declares a Bool without min or max, and a wave-2 source review reports that the legacy `.conf`
  path does not enforce the table's min and max at all (R55W2RevToolSource), so for such a line Hyprland stores the written
  value and the tool does not. Known divergences from Hyprland's own parser are listed in the tool's docstring.

## Adjacent ground (reported, not absorbed)

- The XKB compile of `kb_layout`/`kb_options` is `hyprland-input-devices-r46.md` and `xkb-keymap-compile-r48.md`; K09 only
  pins that numlock is set on the keymap state after that compile.
- What a client does with `repeat_info`, and any input-method (fcitx5) interaction, is outside the province; a sibling sweep
  (`.ufo/waves/round-55/w1/R55ScoutAdjacency.md`) found no sibling lane holding `repeat_rate`, `repeat_delay`,
  `numlock_by_default` or `repeat_info`.
- The host readback 40 / 250 / 1 was already held (`hyprctl-verification-layer.md:132-134`, `config-health-report-r3.md:546-548`);
  H01-H06 add the source chain around it, not a new host fact.
