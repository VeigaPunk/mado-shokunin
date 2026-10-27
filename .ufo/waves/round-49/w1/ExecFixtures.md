# ExecFixtures — round 49 w1, C1 fixture set

Lane `mado-shokunin`, base `03e4ae76aff7a4be59cb69970dd553baa319695a`. Seat: `w1/ExecFixtures`.
Deliverable: `.ufo/waves/round-49/w1/ExecFixtures/fixtures.json` — **633** `(RMLVO, keysym)` cases in **17** classes, every
`expect` captured from **3 identical runs** of the pinned judge on keymaps compiled by the pinned compiler in a clean environment.
Nothing frozen, nothing committed; the L1 integrates.

## 1. What was built

| file | sha256 | bytes | role |
|---|---|---|---|
| `fixtures.json` | `80fd778adb5e72430158a51c29e713b6ffb203c75a7eda2cba57b1339d9a4547` | 303537 | the deliverable (`[{id,class,rmlvo{5},arg,expect{stdout,rc}}]`) |
| `build.py` | `2d3b53bb6d10a413c74f2214d9104c7853598bf2b13a03137abef68814d3765b` | 21171 | generator: compiles each RMLVO, runs the judge 3× per case, asserts class invariants |
| `verify.py` | `e2c22b7341f09919b78bd3413038277d77e4d47786223f8eb096280eec3bbe17` | 2844 | independent re-check: recompiles from the JSON's `rmlvo` only, re-runs the judge once per case |
| `receipt-build.log` | `6dadc077030e3a7afef4c86f75b8eb4272e60ceeaa6a5e4df384fee4842f7c42` | 5982 | judge/compiler digests, per-keymap sha256 + byte size + RMLVO, census line |
| `receipt-verify.txt` | `dea1f75b8043a2b687e1e29e98fdd85054fa7d3f5e55e9800c296bd543eb9754` | 349 | `TOTAL 633/633 keymaps=27 mismatches=0` |
| `receipt-census.txt` | `4576dd8d311d88c60b03113761c6f49c6691f6992d6b96ade7ef7335033215c6` | 4038 | class table, rc/row distribution, per-RMLVO fixture counts |
| `receipt-samples.txt` | `dd11bbda847eeaacde7858d4b50c11e476322091e68e5f8d296c75491378a41e` | 7650 | 20 verbatim `expect.stdout` bodies with their RMLVO |
| `receipt-bind-keys.txt` | `544b148852dd15a467163e4e780b1a60bbb251dca98e3faa6ce58d550ecd744f` | 1094 | the 58 keysym-bearing keys taken from `hyprctl binds -j` (shape-only for the 7 dropped forms) |
| `fixtures-counter.json` | `81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393` | 179660 | the same 633 pairs in the C1 counter's flat shape `{id,class,rmlvo,arg,rc,sha256}` |
| `export_counter.py` | `7c9e00fc291c706b7683e3be207072602239819325414ea40c33e48272930f14` | 1724 | derives the counter view from `fixtures.json` (stdout folded to a digest, nothing else changes) |

Instrument identity, re-measured this seat (not copied from the brief):

```
f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54  /usr/lib/xkbcommon/xkbcli-how-to-type
43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250  /usr/lib/xkbcommon/xkbcli-compile-keymap
13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3  /usr/include/xkbcommon/xkbcommon-keysyms.h
```

Host keymap (`--layout br --options compose:caps`) compiles to `efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81`,
73079 B — the same digest round 48 recorded. `xkbcli compile-keymap --help` and `how-to-type --help` were the only extra reads.

## 2. Method (what a counter has to reproduce)

For each case: compile the fixture's RMLVO with the pinned `xkbcli-compile-keymap` in `env -i PATH=/usr/bin HOME=<work>/w
XDG_CONFIG_HOME=<work>/w/cfg`, then run
`xkbcli-how-to-type --keymap=<file> --disable-compose --keysym <ARG>` in the same clean env; `expect = {stdout, rc}`.
`build.py` compiles 28 keymap ids — `host` and `case-host` share one RMLVO and one file, so the fixtures reference 27
distinct RMLVOs — runs each case **3×** and aborts on any difference (`triples_stable=633`, `judge_runs=1899`); it also aborts if a
compile returns non-zero or emits `XKB-595`/`Unrecognized` (a silently-ignored option would make the RMLVO a lie — checked:
`grep COMPILE_WARN receipt-build.log` is empty).

`verify.py` deliberately forgets the keymap files: it compiles from the `rmlvo` object in `fixtures.json` into a fresh work dir
and re-runs the judge once. Result `633/633`, 27 distinct keymaps, 0 mismatches. So the stored `expect` is a function of
`(rmlvo, arg)` alone — no path, env, or cache dependency.

Timing on this host: build (1899 judge runs + 28 compiles) 2.0 s; verify (633 runs + 27 compiles) 2.7 s wall including Python
startup. A counter can afford the full set per run.

**Schema split, on purpose.** The ticket fixes `expect = {stdout, rc}` for `fixtures.json`; the C1 counter seat
(`w1/ExecCounterC1/c1-r49-keysym.py`, `check_fixture`) accepts an installed file only with the flat keys
`{id, class, rmlvo, arg, rc, sha256}` and an exact key set. `fixtures-counter.json` is the derived view (same 633 pairs,
`sha256` over the same stdout bytes, ASCII-only so bytes == `stdout.encode()`), regenerable with `export_counter.py`.
Both files are in the seat dir; the L1 freezes whichever the counter needs and can pin either digest.

**Cross-seat agreement (independent).** The counter seat embedded eight of these pairs with its own recorded digests. Recomputed
from my `expect.stdout` they match exactly: `slash`/`0x2f`/`47` `3d895204…`, `Return` `9697ab0c…`, `dead_acute` `db686887…`,
`ISO_Level3_Shift` `b181628d…`, `XF86AudioMute` `a815c2db…`, `Escape` `d0cf7e53…` (all `br+compose:caps`, rc 0). Two seats
recorded the same bytes for the same inputs without coordinating.

The same `verify.py` was re-run from the **delivered** seat copy against the **delivered** `fixtures.json` in a fresh work dir
(`--work /fast/scratch/hyaku/mado-r49/ExecFixtures/final`) and printed the byte-identical result
(`TOTAL 633/633 keymaps=27 mismatches=0`, identical digest to `receipt-verify.txt`).

## 3. Class counts (633 total; `rows>=2` share = 180/633 = **0.284**)

| class | n | rc0 | rc2 | rows>=1 | rows>=2 | zero-row rc0 | what it attacks |
|---|---|---|---|---|---|---|---|
| HOST | 55 | 55 | 0 | 51 | 10 | 4 | host keymap `br + compose:caps` |
| MULTI | 58 | 58 | 0 | 52 | 27 | 6 | `br,us` / `us,ru` / `us,ru,de` / `us,ru,de,fr` / variants per layout |
| VARIANT | 81 | 81 | 0 | 73 | 14 | 8 | `br(nodeadkeys|abnt2|thinkpad|dvorak)`, `us(intl|dvorak|colemak|altgr-intl)`, `de(nodeadkeys)` |
| OPTIONS | 51 | 51 | 0 | 45 | 16 | 6 | `lv3:ralt_switch`, `grp:alt_shift_toggle`, `grp:shifts_toggle`, `caps:escape`, `ctrl:nocaps`, `ctrl:swapcaps`, `altwin:swap_lalt_lwin`, `compose:ralt`, `keypad:pointerkeys`, `lv5:caps_switch`, `shift:breaks_caps`, `nbsp:level3`, `lv3:ralt_switch,compose:ralt` |
| LETTERS | 40 | 40 | 0 | 40 | 16 | 0 | letters across dvorak/colemak/br-dvorak/multi |
| DIGITS | 18 | 18 | 0 | 18 | 10 | 0 | `0`..`9`, incl. one row per layout |
| PUNCT | 38 | 38 | 0 | 37 | 18 | 1 | `slash question backslash bar at numbersign semicolon ... guillemotleft` |
| DEAD | 27 | 27 | 0 | 15 | 1 | 12 | `dead_*` on br/us-intl/de + deleted on nodeadkeys |
| KEYPAD | 25 | 25 | 0 | 23 | 5 | 2 | `KP_0..KP_9`, `KP_Add/Subtract/Multiply/Divide/Decimal/Enter/Separator/Equal/Space/Tab/Begin/Home/End/Insert` |
| FUNCTION | 59 | 59 | 0 | 37 | 17 | 22 | `F1..F35`, `Return Tab BackSpace Escape Delete Insert Home End Page_Up Page_Down Up Down Left Right space Menu Print Pause Scroll_Lock Num_Lock Begin Clear Linefeed` |
| XF86 | 24 | 24 | 0 | 24 | 4 | 0 | `XF86Audio* XF86MonBrightness* XF86Kbd* XF86Touchpad* XF86PowerOff XF86Calculator XF86WakeUp ...` |
| MODIFIER | 16 | 16 | 0 | 12 | 3 | 4 | `Shift_L/R Control_L/R Alt_L/R Super_L/R Caps_Lock ISO_Level3_Shift ISO_Level5_Shift ISO_Next_Group Mode_switch Meta_* Hyper_L Shift_Lock` |
| ABSENT | 15 | 15 | 0 | 0 | 0 | 15 | valid keysym, not in the keymap |
| NUMERIC | 21 | 21 | 0 | 16 | 5 | 5 | `0x2f 47 0x1000e9 0xff0d 0x20 0xfe51 0xffb7 0x61 97 0x1008ff12 0x7e1 10 0x3` |
| CASE | 27 | 9 | 18 | 9 | 4 | 18 | canonical vs Hyprland-upper vs lower forms |
| INVALID | 20 | 0 | 20 | 0 | 0 | 20 | rc-2 path |
| BIND | 58 | 44 | 14 | 44 | 30 | 14 | every keysym the host's 192 binds name |

`rc0=581, rc2=52, rows>=1=496 (0.784), rows>=2=180 (0.284), max_rows=15, mean_rows=1.74`.
`max_rows=15` occurs in 23 fixtures (`F1`..`F12`, `KP_Add`, `KP_Multiply`, `KP_Divide`, `KP_Subtract`): one row per
(level × Lock × other mask) combination, e.g. `F9` on the host keymap. 27 distinct RMLVO keymaps; the biggest groups are
`br+compose:caps` (185 cases, shared by HOST/CASE/BIND) and `us,ru,de` (95).

## 4. Facts the set pins down (measured, with the receipt line that shows it)

1. **Lookup is case-sensitive, both directions.** `Return` rc0 one row (`36 RTRN ... 1 [ ]`); `return`, `RETURN`, `Slash`,
   `SLASH`, `Space`, `escape`, `backspace`, `kp_7`, `DEAD_ACUTE` all rc2 with **empty stdout** (`receipt-samples.txt`).
   `Delete` (capital D only) is rc0 — Hyprland's own mixed-case key in the capture resolves, its all-caps siblings do not.
   Because of this the 58 BIND cases split 44 rc0 / 14 rc2; that split is the C2 key-name question in fixture form.
2. **ABSENT prints the header and nothing else, rc 0.** `--keysym Greek_alpha` → 120 B: `keysym: Greek_alpha (0x07e1)`, blank,
   `=== Direct access ===`, blank, the column header, no rows. A tool that emits rows-or-exit-nonzero is wrong.
3. **A numeric keysym with no name prints its hex in the name field**: `--keysym 0x1000e9` → `keysym: 0x001000e9 (0x1000e9)`,
   0 rows — the `%08x` form, wider than `0x%04x`.
4. **Numeric and name forms agree**: `47` and `0x2f` both print `keysym: slash (0x002f)` with the same 5 rows; `0x0`,
   `999999999`, `0xfffffffff` and `-1` are rc2 (the last one comes from getopt, `invalid option -- '1'`, not from keysym
   conversion; stdout is empty either way, which is all the contract compares).
5. **Multi-layout rows carry the real layout index and name**, e.g. `41 AC04 2 Russian 1 [ ]` for `Cyrillic_a` on `us,ru,de`,
   and `11 AE02 4 French 1 [ ]` for `eacute` on `us,ru,de,fr`. A single-layout assumption dies here.
6. **The host's SLASH is two keys**: `AD01` levels 3/4 under `[ Mod5 LevelThree ]`/`[ Shift Mod5 LevelThree ]` plus Lock
   variants, and `AB11` level 1 `[ ]` — unchanged from the L1's sample, now a fixture (`HOST/slash`).
7. **`--disable-compose` does not remove dead keys**: `dead_acute` on the host keymap still yields `AD11` level 1 and `AC10`
   level 3 under Mod5. On `br(nodeadkeys)` the same keysym yields 0 rows. `br` maps neither `cedilla` nor `dead_cedilla`;
   the ç character is `ccedilla` on `AC10` level 1 on both `br` and `br(abnt2)`.
8. **Virtual modifier names appear as libxkbcommon names them**: `[ Mod2 NumLock ]` for `KP_8`, `[ Lock Mod5 LevelThree ]`,
   `[ Mod1 Alt Meta ]` (`KP_Add`), `[ Control ]` — not XKB `real_mods` indices.
9. **Options act on the keysym the bind would name**: `compose:ralt` → `Multi_key` on `RALT` levels 1 and 2;
   `lv3:ralt_switch` → `ISO_Level3_Shift` on `RALT` (and `LVL3` on keycode 92 in the evdev map);
   `lv5:caps_switch` → `ISO_Level5_Shift` on `CAPS` (66) **and** `LVL5` (203);
   `altwin:swap_lalt_lwin` puts `Alt_L` on `LWIN` (133) and `Super_L` on `LALT` (64), and both also appear at keycode
   204/206 level 2 under `[ Shift ]`.
10. **All-caps Hyprland key names are not keysym names.** This is the single most useful cross-claim fact for C2: 14 of the
    58 host bind keys (`SLASH`, `RETURN`, `TAB`, `ESCAPE`, `BACKSPACE`, `SPACE`, `DELETE`, `LEFT`, `RIGHT`, `UP`, `DOWN`,
    `COMMA`, `PERIOD`, `PRINT`) fail `xkb_keysym_from_name` as written; Hyprland must be normalising them itself.

## 5. Fixture-level invariants enforced by `build.py` (a mis-classed arg fails the build)

- classes HOST, MULTI, VARIANT, OPTIONS, LETTERS, DIGITS, PUNCT, DEAD, KEYPAD, FUNCTION, XF86, MODIFIER, ABSENT, NUMERIC:
  every `arg` must resolve — `rc 0` and the fixed header present.
- ABSENT: additionally `rows == 0`.
- INVALID: `rc == 2` and `stdout == ""`.
- BIND: `rc 2` implies empty stdout.
- ids unique and sequential (`r49-c1-0001`..`r49-c1-0633`); no duplicate `(rmlvo, arg)` pair; ASCII only; `rmlvo` always has
  all five keys; `model` is `pc105` and `rules` `evdev` throughout (the defaults; `--variant thinkpad` as a *symbols*
  variant exists only for `br` in xkeyboard-config 2.48 — `us(thinkpad)` is rc 1 at compile, so VARIANT carries
  `br(thinkpad)`, and `pc105`/`evdev` are never omitted from the fixture metadata).

## 6. Counter recipe notes for the freeze (what bit me, so it does not bite w2)

- The judge's stdout is **column-padded fixed width** (`KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS`,
  two-space gaps, width-8 keycode). Compare bytes, not tokens.
- Compile each distinct RMLVO **once** and reuse the file; 27 compiles is ~0.7 s, 633 compiles would be ~17 s.
- Reject a work dir under `/tmp` (SentScratch) and any inherited `TMPDIR`: the clean env is `PATH=/usr/bin` plus
  `HOME`/`XDG_CONFIG_HOME` inside the work dir, and `env -i` is what keeps a user `~/.config/xkb` include path out.
- `--disable-compose` is mandatory in every invocation; the compose-table path was never exercised here and is out of
  contract (no fixture uses it).
- Do not pre-bake keymap files: `verify.py` shows `rmlvo` alone reproduces every expect, so the counter can compile at count
  time, which is what the C1 contract asks of it.

## 7. Not claimed / left to other seats

- Whether the 2659-line `xkbcommon-keysyms.h` is sufficient to reproduce `xkb_keysym_get_name` (canonical-name choice,
  deprecated aliases, `0x%08x` unnamed form) is the **tool** seat's question. This set only fixes the observable outputs,
  including the two shapes that table must get right: unnamed numerics (§4.3) and rc2 on non-canonical case (§4.1).
- The keysym↔value direction for `U+`-prefixed arguments: with `--keysym`, `U+0041` is rc2 (fixture `INVALID`), i.e. the
  codepoint interpretation is a different argument mode and correctly refused.
- C2's Hyprland-side reading (how `SLASH` becomes a matchable keysym) is elsewhere; §4.10 is offered as evidence, not analysis.

## 8. Safety / hygiene

- Host writes: none. No `~/.config`, `~/.cache`, `~/.local` touched; `hyprctl` used read-only (`version`, `binds -j`) and only
  key strings were kept (device name in the two `switch:` rows never copied — `receipt-bind-keys.txt` names those rows by
  shape only). No pacman, no service or compositor mutation, no input injection, no terminal/GUI.
- Scratch `/fast/scratch/hyaku/mado-r49/ExecFixtures` (work dirs `w/`, `km/`, `v/`, the raw binds capture) removed after the
  receipts were copied; `ulimit -f 65536` on every writer shell; `build.py`/`verify.py` both refuse a `/tmp` work dir.
- Tools installed/upgraded: **none**.
- Lane writes: only `.ufo/waves/round-49/w1/ExecFixtures/` (8 files above) and this report. No tracked file edited, no
  git/jj command run in the lane.

Checks the integrator should run: `python3 .ufo/waves/round-49/w1/ExecFixtures/verify.py --work <dir-not-under-/tmp>
--fixtures .ufo/waves/round-49/w1/ExecFixtures/fixtures.json` (expects `TOTAL 633/633 keymaps=27 mismatches=0`), and
`python3 -c "import json;d=json.load(open('.ufo/waves/round-49/w1/ExecFixtures/fixtures.json'));print(len(d))"` → `633`.
