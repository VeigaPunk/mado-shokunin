# R55 adjacency scan: keyboard repeat rate/delay, numlock, wl_keyboard, XKB options, Hyprland input settings

Seat: R55ScoutAdjacency (read-only, leaf member, no subagents). Lane: mado round 55, wave w1.
Scope: the 20 sibling `*-shokunin` repos under /home/vgpnk/Projects/shokunin (mado-shokunin skipped) and /home/vgpnk/Projects/kimi-shokunin (git HEAD e737d2e, 2026-10-19; a plugin/skills repo). Excluded dirs: `.git`, `node_modules`, `target`. Adjacency axis only: this file reports holdings and defers scope; it absorbs nothing.

Receipts (raw file lists, one per term): `receipts/files-<term>.txt`, `receipts/numlock-i-files.txt`, `receipts/repeat-phrase.txt`.

## 1. Term sweeps across siblings (case-sensitive unless noted)

| Term | Files | Hits |
|---|---|---|
| `repeat_rate` | 0 | none |
| `repeat_delay` | 0 | none |
| `numlock_by_default` | 0 | none |
| `repeat_info` | 0 | none |
| `xkb_options` / `XKB_OPTIONS` | 0 | none |
| `wl_keyboard` | 1 | tsukuroi-shokunin/.ufo/waves/round-15/build/ConnectMadoBoundary.md:33 |
| `numlock` (case-sensitive) | 3 | tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/{host,stable,official}-extra-pkglist.txt:7708, :7713, :7713 (`numlockx 1.2-6`, package census only) |
| `numlock` (`-i`) | 5 | the 3 above plus kotoba-shokunin/.ufo/round-44/evidence/omp-live-18.12.2-strings.txt (`NumLock` key-name table in a binary string dump) and tabi-shokunin/.ufo/waves/round-33/w1/ScribeSrcSession/web_view_impl.cc.dec:1473 (Chromium modifier mask, unrelated) |
| `kb_options` / `kb_layout` / `kb_variant` (text types) | 2 | tsukuroi-shokunin/.ufo/waves/round-50/w1/R50RevScopeSiblings/tip.mado.md:103 and tsukuroi-shokunin/.ufo/waves/round-50/w1/R50ScoutLiveTip/mado-PROVINCE-at-tip.txt |
| `hyprctl getoption` / `hyprctl devices` (`*.md`) | 1 file, 2 lines | tsukuroi-shokunin/.ufo/waves/round-50/w1/R50RevScopeSiblings/tip.mado.md:106, :114 |
| `hyprctl` (text types) | 36 | not classified; logs, receipts and evidence dumps, not input-config claims |
| `repeat rate` / `repeat delay` / `key repeat` (`-i`, md/txt/sh/py) | 41 lines | none about keyboard repeat settings; every hit is either a JSON duplicate-key helper in chousa-shokunin/.ufo/waves/round-33 or a scope exclusion ("does not test OS key repeat") in game-dev-2d-shokunin reports (e.g. reports/r42-focus-restore-scout.md:20, reports/r50-release-critic.md:17) |
| `input:` (text types) | 1350 files | noise (ffmpeg "Error opening input", audio corpora, kernel logs); discarded |

Command shape for every row: `grep -rIl --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target -e '<term>' <20 sibling repos> /home/vgpnk/Projects/kimi-shokunin`. The unfiltered `kb_options` sweep timed out at 300 s on the large trees; the text-type-filtered rerun completed (counts above).

Decisive outputs:
- `repeat_rate … files=0`, `repeat_delay … files=0`, `numlock_by_default … files=0`, `repeat_info … files=0`, `xkb_options … files=0`.
- `wl_keyboard … files=1`.
- `numlock … files=3`, all three `numlockx 1.2-6` package lines.

## 2. What each sibling already holds

- **tsukuroi-shokunin (layer-4 / event delivery).** ConnectMadoBoundary.md:33 places `wl_keyboard.enter` / `wl_pointer.enter` in the event-delivery chain and states that tsukuroi has no input-injection authority. It holds no repeat or numlock content. Consequence for the C1 entry: its path stops at compositor-side `wl_keyboard.repeat_info` emission. Client-side consumption (toolkit key repeat) belongs to tsukuroi's layer-4 claims.
- **tsukuroi-shokunin R50 scope review copies.** tip.mado.md:103-106 and :114 and mado-PROVINCE-at-tip.txt hold copies of mado's round-46 ownership text: mado owns the `input` block's `kb_*` keys and the `device` blocks, via `hyprctl devices -j`, and the keybind keymap is excluded. These are scope-review artifacts that restate mado's own text. They are not tsukuroi claims and must not be cited as evidence for C1.
- **tsukuroi-shokunin R24 host package census.** `numlockx 1.2-6` appears in the three extra-pkglist files. Presence on the host is observed. Wiring is not: no `numlockx` reference exists in any sibling, mado or kimi text file searched (`*.md *.sh *.py *.conf *.json *.toml`, excluding pkglists). Whether an autostart runs it was not checked (see §5).
- **kotoba, tabi, kimi, chousa, kaidoku, kagi, audio, game-dev, tameshi, mori, lore, kama, kake, etc.** No keyboard-repeat, numlock or XKB config holdings. Their hits are noise or unrelated (see table). tameshi's `Hyprland 0.56` markdown hit (round-27/w1/ScoutLegAnchors.md:83) is a mado-verify conf-SHA pin row, not an input setting.

## 3. Mado knowledge notes that mention the terms (mado-shokunin, excluding `.ufo/waves/`)

| Location | Claim |
|---|---|
| corpus/knowledge/hyprctl-verification-layer.md:132-134 | §3.2 input rows: `input:repeat_rate` = 40 (declared L-IN:14), `input:repeat_delay` = 250 (L-IN:15), `input:numlock_by_default` = true (L-IN:18). Live `int: 40`, `int: 250`, `int: 1`, all `set`, all `agreement`. |
| corpus/knowledge/config-health-report-r3.md:546-548 | Appendix A live re-measure: 40 / 250 / 1, `set`, `agreement`. |
| corpus/knowledge/config-health-report-r3.md:829-831 | Machine-readable expected-values block for the same three keys. |
| corpus/knowledge/hyprland-input-devices-r46.md:70 | Says `repeat_rate`, `repeat_delay`, `numlock_by_default` and other settings are "applied per device too but the dump prints none of them"; marks them UNK for the devices join. This is the UNK that the round-55 C1 entry claims to move. |
| corpus/knowledge/hyprland-input-devices-r46.md:34 | Says `numLock` in `hyprctl devices -j` is locked-modifier state, "not the `numlock_by_default` option". The C1 entry must keep these two apart. |
| corpus/knowledge/config-option-table-r39.md:70 | Says the operator's `input.conf` owns "repeat 40/250, numlock" among 7 keys. |
| corpus/README.md:122 | Round-46 row lists repeat_rate, repeat_delay, numlock_by_default as still open. |
| tools/mado-options.py:1345 (sample config string `repeat_rate = $r`), :1407, :1495, :1584, :1607 | Option table: expected `input:repeat_rate` = 40 int set, agreement check. |
| quality/counters/c3-r39-options.py:66 | Option list includes `repeat_rate`. |
| quality/counters/c1-r46-devices.py:193, c1-r46-devices-v3.py:256 | Field list naming `repeat_rate` among the devices-join fields. |
| quality/counters/c1-r46-fixtures-v2.json:5, :63, :1106, :1248 | Fixture configs with `repeat_rate = 40`. |

Neighbours: corpus/knowledge/xkb-keymap-compile-r48.md (kb_* compile; no repeat/numlock hits), hyprland-config-plane.md (no hits). input-debugging-boundaries-r15.md:35 and :55 and hyprland-focus-grab-r41.md:35 cite `wl_keyboard.enter` / keyboard focus only; none of the mado notes (`corpus/knowledge`, `corpus/README.md`) cites `repeat_info`, `wl_keyboard.repeat_info` or `m_repeatRate` (verified by grep: 2 files match the combined pattern, both via `wl_keyboard` focus lines).

Absent at base, as the frozen contract says: corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md and tools/mado-kbdopts.py.

## 4. Contested scope and deferrals for the C1/C2 entry

1. **C1 owns the per-keyboard path** config value → `applyConfigToKeyboard` → keyboard state → `wl_keyboard.repeat_info`, and numlock → keymap setup. This is the r46 line-70 UNK. Nothing in siblings contests it.
2. **Defer to r46** (hyprland-input-devices-r46.md) for `kb_*` per-device names and the `hyprctl devices -j` dump semantics. Do not re-derive the devices join already in `tools/mado-devices.py`.
3. **Defer to r48** (xkb-keymap-compile-r48.md) for the XKB compile of `kb_*` names. Only the numlock keymap-setup link is new.
4. **Duplication risk for C2.** `tools/mado-options.py` and the verification notes already hold the live values 40 / 250 / 1 and their expected forms. A new `mado-kbdopts.py` that joins `hyprctl getoption` should reuse or cite that table, not add a second one.
5. **Defer to tsukuroi** (ConnectMadoBoundary.md:33, layer-4) for client-side consumption of `wl_keyboard.repeat_info`. The entry stops at compositor emission.
6. **numlock contest.** `numlock_by_default` is the compositor's startup setting. If a host autostart runs `numlockx` (installed per the R24 census), the live numLock state is not the option's alone. The entry must say so and must not claim the observed numLock state is the option's effect.
7. **Language to keep distinct.** The `numLock` modifier state in the devices dump (r46:34) is not the `numlock_by_default` option.

## 5. Not verified

- No read of any `~/.config/hypr` file other than `input.conf`. Not checked: an `exec-once` / autostart `numlockx`, or any `source =` target. The allowed-read list did not include them.
- No `hyprctl` call run by this seat. The scout role is grep-only, so the host's live values are cited only from mado's own notes, not re-observed.
- Greps are literal text matches. A zero count means no textual match. Other phrasings (e.g. "NumLock" in prose, "keyboard delay") were covered only by the `-i` numlock and phrase sweeps above.
- Files under sibling `.ufo/waves` and evidence directories were included in the sweeps but not individually read beyond the listed hit lines.
