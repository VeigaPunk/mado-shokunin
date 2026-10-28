## Joining the declaration to the live read (the round-55 tool)

`tools/mado-kbdopts.py` (round 55, claim C2) models the config half of this chain for config text a caller supplies — device
value when the block set it, else the global option, else the table default (K16, K13-K15), integers as the hyprlang parser
reads them — and joins the result to the JSON that `hyprctl getoption <name> -j` prints. Receipt, read-only, 2026-10-28:
`.ufo/waves/round-55/receipts/live-kbdopts.txt`. For `~/.config/hypr/input.conf` (byte-equal to the committed pin, `cmp`) and
two keyboard names from `hyprctl devices -j` it prints `repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0`
for both and `AGREE` three times against the live read (the committed H04-H06 lines).

How to read that output without overclaiming:

- The host config holds no `device` block (`grep -rnE 'device\[|device \{|device\{' ~/.config/hypr` → no match, receipt
  `.ufo/waves/round-55/w1/R55ScoutHost/receipts-cmp-grep.txt`), so by K16 every keyboard resolves to the global value; the two
  per-keyboard lines are what the source implies for those names, not an observed per-keyboard value.
- `getoption` returns an option by name. [INFERENCE] It takes no device argument, so `AGREE` says the running compositor's
  global option equals the declared one; it cannot show a device override (the reply forms are held in
  `hyprctl-getoption-native-forms-r40.md`, not re-claimed here).
- The `numLock` field of `hyprctl devices -j` is lock state, not this option (`hyprland-input-devices-r46.md` step 5); the
  tool never compares them.
- `hyprland-input-devices-r46.md:70` lists these three options as applied per device and printed by no dump; K01-K03 and K08
  now show the per-device read at source level and that sentence stays as history. Nothing here makes the dump print them.
- The tool's `unsupported` count is its honesty valve: a value outside the modelled token set (`$` variables, `device[...]`
  bracket forms, hex or signed numbers, out-of-range values, `##`) is counted, not guessed. The numlock 0..1 range is the
  lane's modelling rule, not a source range (K15 declares a Bool without min or max).

## Adjacent ground (reported, not absorbed)

- The XKB compile of `kb_layout`/`kb_options` is `hyprland-input-devices-r46.md` and `xkb-keymap-compile-r48.md`; K09 only
  pins that numlock is set on the keymap state after that compile.
- What a client does with `repeat_info`, and any input-method (fcitx5) interaction, is outside the province; a sibling sweep
  (`.ufo/waves/round-55/w1/R55ScoutAdjacency.md`) found no sibling lane holding `repeat_rate`, `repeat_delay`,
  `numlock_by_default` or `repeat_info`.
- The host readback 40 / 250 / 1 was already held (`hyprctl-verification-layer.md:132-134`, `config-health-report-r3.md:546-548`);
  H01-H06 add the source chain around it, not a new host fact.
