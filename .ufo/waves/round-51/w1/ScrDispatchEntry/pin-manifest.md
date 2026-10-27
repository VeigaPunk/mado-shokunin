# Pin manifest for `hyprland-dispatcher-dispatch-r51.md`

Promotion target: `.ufo/waves/round-51/fetch/`. The bytes now sit in the fetch seat's draft
directory `.ufo/waves/round-51/w1/ExecFetchDispatch/fetch/` (19 pins, 3 revisions) and were
checked byte-for-byte by that seat; `Hyprland-SharedDefs.hpp` is also held in
`.ufo/waves/round-51/w1/ScrDispatchEntry/fetch/` as an independent fetch of the same bytes.

| pin | upstream file | revision | bytes | lines | sha256 | registry row |
|---|---|---|---|---|---|---|
| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | `efb50993` | 39334 | 975 | `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40` | S364 (and S352 held) |
| Hyprland-KeybindManager.hpp | src/managers/KeybindManager.hpp | `efb50993` | 7936 | 191 | `cee22c13d413ab389803e0eb87a6fcefadedea885cee4457b56ae351228dd1e0` | S364 |
| Hyprland-legacy-DispatcherTranslator.cpp | src/config/legacy/DispatcherTranslator.cpp | `efb50993` | 35997 | 868 | `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771` | S365 |
| Hyprland-legacy-DispatcherTranslator.hpp | src/config/legacy/DispatcherTranslator.hpp | `efb50993` | 567 | 22 | `438c1e662f5c9fa4d5821fbab251113c66562dd452d1844f965c294bb3444e87` | S365 |
| Hyprland-HyprCtl.cpp | src/debug/HyprCtl.cpp | `efb50993` | 97582 | 2346 | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` | S366 |
| Hyprland-ConfigActions.cpp | src/config/shared/actions/ConfigActions.cpp | `efb50993` | 71407 | 1772 | `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637` | S367 |
| Hyprland-ConfigActions.hpp | src/config/shared/actions/ConfigActions.hpp | `efb50993` | 6960 | 122 | `746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073` | S367 |
| Hyprland-legacy-ConfigManager.cpp | src/config/legacy/ConfigManager.cpp | `efb50993` | 90963 | 2184 | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | S368 (and S353 held) |
| Hyprland-SharedDefs.hpp | src/SharedDefs.hpp | `efb50993` | 1915 | 60 | `0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087` | S369 |
| Hyprland-ConfigManager.cpp | src/config/ConfigManager.cpp | `efb50993` | 2597 | 82 | `c10dc1ce6602a854121a79fb0192c9f43aa836a35f9acb98ff1789541b01f366` | none — Limits only |
| Hyprutils-VarList.hpp | include/hyprutils/string/VarList.hpp | `a21e87b8` (v0.14.2) | 1883 | 65 | `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43` | none — Limits only |
| Hyprutils-VarList.cpp | src/string/VarList.cpp | `a21e87b8` | 1189 | 38 | `b02df8d688519366e7f20de5c3c44d21c3832316e8262ced0d295e129b166a36` | none — Limits only |
| Hyprutils-VarList2.cpp | src/string/VarList2.cpp | `a21e87b8` | 5033 | 126 | `b8cacea741b2d6260ad6618be00e37bc01c4d092e655a7557f7cfbadb76cf26d` | none — Limits only |
| wiki-Using-hyprctl.md | content/Configuring/Using-hyprctl.md | `d5f07c60` | 7859 | 315 | `3489a75da5f0865d56deda13412c67af905d8507a4bc51367d96952e55ab3545` | none — Limits only |
| wiki-Dispatchers.md | content/Configuring/Dispatchers.md | `d5f07c60` | 13337 | 313 | `39d0747a34bf013d62f8d70d4e1259cf084510e38c17bb4dc1e3245095c1f494` | none — Limits only |

`Hyprland-docs-hyprctl.1.rst` (2623 B, `07cd73872e32ec59dcd1d51cc53e40a6318f25e577a63b6ce25f748f0e0ac166`)
is cited once in Limits for the documented argument-presence rule and has no row (rows seat §4.1).

## Cited lines per pin

- `Hyprland-KeybindManager.cpp` - 42, 112, 113, 131, 154, 386, 396, 599, 652, 775-778, 782,
  785, 793, 795, 799, 804, 810, 812, 814, 816-819, 820-823, 842, 845-851.
- `Hyprland-KeybindManager.hpp` - 25-26, 137 (and 163 for the pressed-special vector).
- `Hyprland-legacy-DispatcherTranslator.cpp` - 31-34, 48-51, 532-535, 676, 684, 773, 797-867.
- `Hyprland-legacy-DispatcherTranslator.hpp` - 19.
- `Hyprland-HyprCtl.cpp` - 1128, 1130-1141, 1143-1147, 1149, 1151, 1153-1157, 2036.
- `Hyprland-ConfigActions.cpp` - 1465, 1487, 1492, 1499-1500, 1603-1615, 1634, 1640, 1643,
  1664, 1666, 1674, 1681.
- `Hyprland-ConfigActions.hpp` - 114 (and 118 declared).
- `Hyprland-legacy-ConfigManager.cpp` - 1584, 1586, 1589, 1592, 1594, 1598, 1624-1631, 1633,
  1797-1798.
- `Hyprland-SharedDefs.hpp` - 53-55.
- `Hyprland-ConfigManager.cpp` - 40, 50 (Limits).
- `Hyprutils-VarList.cpp` - 20-21 (Limits).
- `Hyprutils-VarList2.cpp` - 21-102 (Limits).
- `wiki-Using-hyprctl.md` - 53-61 (Limits); `wiki-Dispatchers.md` - 83-84 (Limits).

## Notes

- Two pins are byte-identical to round-50 copies: `cmp` of `Hyprland-KeybindManager.cpp` and
  `Hyprland-legacy-ConfigManager.cpp` against `.ufo/waves/round-50/fetch/` reports no difference,
  and their sha256 match `.ufo/waves/round-50/fetch/SHA256SUMS`.
- The checksum manifest to build at promotion must not carry a self-row (M50-9/D4): digest the pins,
  not `SHA256SUMS` itself. The fetch seat's `fetch-manifest.json` already records
  `sums_self_row: none`.
