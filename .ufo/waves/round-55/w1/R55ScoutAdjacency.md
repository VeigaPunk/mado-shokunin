# R55ScoutAdjacency: report (round 55, mado, wave w1)

Seat: read-only adjacency scan. Deliverable: `.ufo/waves/round-55/w1/R55ScoutAdjacency/adjacency.md` (full tables). Receipts: `.ufo/waves/round-55/w1/R55ScoutAdjacency/receipts/`.

## What I did

1. Read the frozen contract (`.ufo/waves/round-55/claims-frozen.md`) for scope. I did not edit it, and I did not read the sealed hold-out fixtures.
2. Ran per-term `grep -rIl` sweeps over the 20 sibling `*-shokunin` repos (mado skipped) and `/home/vgpnk/Projects/kimi-shokunin`, excluding `.git`, `node_modules` and `target`. Terms: `repeat_rate`, `repeat_delay`, `numlock_by_default`, `repeat_info`, `xkb_options`, `wl_keyboard`, `numlock`, `kb_options|kb_layout|kb_variant`, `hyprctl`, and the phrases "repeat rate" / "repeat delay" / "key repeat".
3. Read the mado knowledge notes that mention the terms, and the matching lines in sibling notes, to confirm what each claims.
4. Copied receipts into the deliverable directory. Scratch lived at `/fast/scratch/hyaku/mado-r55/R55ScoutAdjacency/` and is removed before yield.

Nothing was written to any sibling repo, the fleet root, `~/.config`, or the lane's tracked files. No `hyprctl` call was run. No git or jj command was run.

## Decisive outputs

```
TERM=repeat_rate    files=0
TERM=repeat_delay   files=0
TERM=numlock_by_default files=0
TERM=repeat_info    files=0
TERM=xkb_options    files=0
TERM=wl_keyboard    files=1   -> tsukuroi-shokunin/.ufo/waves/round-15/build/ConnectMadoBoundary.md:33
TERM=numlock        files=3   -> tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/{host,stable,official}-extra-pkglist.txt  ("numlockx 1.2-6")
numlock -i          files=5   (above 3 + kotoba omp-live strings "NumLock" key table + tabi Chromium modifier mask, unrelated)
kb_options/kb_layout/kb_variant (text) files=2 -> tsukuroi-shokunin/.ufo/waves/round-50/w1/R50RevScopeSiblings/tip.mado.md:103, R50ScoutLiveTip/mado-PROVINCE-at-tip.txt
hyprctl getoption|devices (*.md)   1 file, 2 lines -> tip.mado.md:106, :114
"repeat rate|repeat delay|key repeat" (-i) 41 lines: none about keyboard repeat settings (JSON duplicate-key helpers; "does not test OS key repeat" scope exclusions)
```

The unfiltered `kb_options` sweep timed out at 300 s. I reran it text-type-filtered, and it completed.

## Findings

- **No sibling holds keyboard repeat rate, repeat delay, numlock_by_default, `wl_keyboard.repeat_info` or XKB option content.** The C1 entry's territory is uncontested in the siblings.
- **tsukuroi (layer 4)** names `wl_keyboard.enter` in its event chain (ConnectMadoBoundary.md:33). The C1 entry should stop at compositor emission of `wl_keyboard.repeat_info` and defer client consumption to tsukuroi.
- **tsukuroi R50 copies of mado text** (tip.mado.md:103-114) restate mado's round-46 ownership of the `kb_*` plane. They are not tsukuroi evidence and should not be cited for C1.
- **`numlockx` is installed** per the tsukuroi R24 host package census (host-extra-pkglist.txt:7708; stable and official :7713). Nothing in the text files searched wires it. If an autostart runs it, the live numLock state is not the `numlock_by_default` option alone. The entry must say so.
- **Mado's own notes already hold the values** 40 / 250 / 1 for `input:repeat_rate`, `input:repeat_delay` and `input:numlock_by_default`: hyprctl-verification-layer.md:132-134, config-health-report-r3.md:546-548 and :829-831, config-option-table-r39.md:70, and tools/mado-options.py:1584. C2's new tool would duplicate that table unless it reuses or cites it.
- **Mado's round-46 note marks the per-device repeat/numlock settings UNK** (hyprland-input-devices-r46.md:70). It also warns that the devices dump's `numLock` is lock state, not the option (r46:34). This is the seam C1 moves, and the two must stay separate.
- **Mado's knowledge notes do not cite `repeat_info`, `wl_keyboard`, or `numlock` as sourced keyboard-repeat claims.** The only mado hits for `repeat_rate`/`repeat_delay`/`numlock_by_default` are the value tables, the r46 UNK line, the r39 operator-table line, the README open-items row, and the option/counter tools and fixtures listed in adjacency.md §3.
- `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` and `tools/mado-kbdopts.py` do not exist at base, as the contract says.

## Defects and ambiguities

- **Premise confirmed, not a defect.** The frozen C1 text says `grep -lE 'repeat_info|m_repeatRate' corpus/knowledge/*.md` returns 0 files at base. I ran it: 0 files. The sibling sweep agrees that no sibling holds `repeat_info`. The mado notes do cite `wl_keyboard` focus lines (input-debugging-boundaries-r15.md:35, :55; hyprland-focus-grab-r41.md:35), which is not the repeat path.
- **Ambiguity:** the frozen C1 wording "applied per device too" (r46:70) is the mado note's claim. It is not something this seat verified against the Hyprland source.
- **Hyprctl text hits (36 files) were not classified.** They are logs and evidence dumps. I did not confirm that none is an input-config claim beyond the two named tip.mado.md lines.

## Not verified

- Autostart wiring of `numlockx`: `~/.config/hypr` files other than `input.conf` are outside the allowed reads, so I did not check them.
- Live host values: no `hyprctl` call by this seat. The 40 / 250 / 1 values are cited from mado notes only.
- Literal-grep limits: zero counts mean no textual match. Other phrasings were covered only by the `-i` and phrase sweeps.

## Tooling

No tools were installed or updated. The pacman guard applies, and nothing was needed.

## Cleanup

Scratch dir `/fast/scratch/hyaku/mado-r55/R55ScoutAdjacency/` removed before yield (see final bash call).
