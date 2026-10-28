# R55W2MutTool1 — mutants of `tools/mado-kbdopts.py` (focus: device/global fallback, D/G/- letters)

Baseline: `tools/mado-kbdopts.py` at `57584ed67716340b3d466fa04333ac0bab3fb79e`, sha256
`9c69dd62c1737d4842a4a0e73db3f8317eda71ee103e71ad3cda11a19c837c2e` (`mutants/orig/mado-kbdopts.py`,
`mutants/receipts/orig.sha256`). Original: 26/26 fixtures pass (18 committed + 8 hold-out, stdout bytes and rc),
`--selftest` = `MADO_KBDOPT_SELFTEST: 83/83 assertions passed`, rc 0.

Note: `R55ExecTool4.md` records 82 selftest assertions; the committed tool at 57584ed runs 83. Measured, not reconciled.

Every mutant is a one-edit copy in scratch (`/fast/scratch/hyaku/mado-r55/R55W2MutTool1/work/mut/`). No lane file was
modified; nothing was restored in the lane because nothing in the lane was touched. Line numbers below are from the
committed file.

## Scoring procedure

`mutants/harness.py <root> <tool>` runs the tool with `python3 -I`, cwd = `<root>`, argv = `args.json`, and compares
stdout bytes and exit code with `expected.out` / `expected.rc` for F01–F18 (`c2/`) and H01–H08 (`c2-holdout/`). It then
runs `<tool> --selftest` and records whether the selftest line is not `N/N` with rc 0. Root = a tree built by
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 57584ed67716340b3d466fa04333ac0bab3fb79e tools/mado-kbdopts.py .ufo/waves/round-55/fixtures .ufo/waves/round-55/fetch | tar -x -C <root>`.
Raw scores: `mutants/receipts/harness-scores.jsonl`, original: `mutants/receipts/harness-orig.jsonl`.

## Mutant table (22 mutants)

"Fixtures killed" lists the fixtures whose stdout or rc differs from expected (of 26). "Selftest" = whether
`--selftest` stops passing. "Survivor" = passes all 26 fixtures. Diffs: `mutants/Mxx.diff`; mutant source: `mutants/Mxx.py`.

| mutant | edit (line in 57584ed) | fixtures killed (of 26) | selftest killed? | survivor? |
|---|---|---|---|---|
| M01 | L205 `if n in dev:` → `if n in dev and n not in st.glob:` (global beats device when both set) | F04 F05 F09 H03 H04 (5) | yes (`device beats global`) | no |
| M02 | L207 device branch letter `"D"` → `"G"` | F04 F05 F09 H01 H03 H04 (6) | yes (5 cases) | no |
| M03 | L213 default branch letter `"-"` → `"G"` | F01 F03–F14 F18 H01–H08 (22) | yes (31/83 pass; 52 cases fail) | no |
| M04 | L205 `if n in dev:` → `if n in dev and dev[n] != DEFAULTS[n]:` (device value equal to default falls through to global) | **H03 only** | **no** (83/83) | no — killed only by hold-out H03 |
| M05 | L208 `elif n in st.glob:` → `elif n in st.glob and st.glob[n] != DEFAULTS[n]:` (global set to its default labelled `-`) | F05 F07 (2) | yes | no |
| M06 | L175 `st.devices.setdefault(cur, {})` → `st.devices[cur] = {}` (second same-name block wipes first) | F09 (1) | yes | no |
| M07 | L154 add `st.devices = {}` at start of `parse_config` (device table reset per file) | none | yes (`device state resets per file but devices persist`) | **SURVIVOR S07** |
| M08 | L194 `st.glob[name] = value` → `st.glob.setdefault(name, value)` (first global wins; later-file global ignored) | F11 (1) | yes | no |
| M09 | L174 `cur = rhs.split("#", 1)[0].strip(WS)` → `cur = rhs.strip(WS)` (device name comment not cut) | none | yes (`device name cut at comment`) | **SURVIVOR S09** |
| M10 | L164 `cur = None` → `pass` (device not forgotten when stack empties) | none | yes (`device forgotten after block`) | **SURVIVOR S10** |
| M11 | L163 `if not stack:` → `if True:` (device forgotten on any `}`, incl. nested) | none | yes (`device retained after nested block closes`) | **SURVIVOR S11** |
| M12 | L203 `st.devices.get(keyboard, {})` → `st.devices.get((keyboard or "").lower(), {})` (case-folded name match) | none | **no** (83/83) | **SURVIVOR S12** |
| M13 | L252 `effective(st, None)` → `effective(st, names[0])` (live compare uses first keyboard's device) | none | yes (`live compares the global, not a device`) | **SURVIVOR S13** |
| M14 | L205 `if n in dev:` → `if n in dev and n != "numlock_by_default":` (device numlock ignored) | F05 H03 (2) | **no** | no |
| M15 | L179 `key in OPTIONS` → `key in OPTIONS or (key.startswith("input:") and key.rsplit(":",1)[-1] in NAMES)` (nested `input:` block keys become global) | H02 only | **no** | no — killed only by hold-out H02 |
| M16 | L198 `st.devices[cur][name] = value` → `st.devices[cur].setdefault(name, value)` (first device key wins, not later) | none | **no** (83/83) | **SURVIVOR S16** |
| M17 | L196 `st.unsupported += 1` (device key with no current device) → `st.glob[name] = value` | H01 only | yes | no — killed only by hold-out H01 |
| M18 | L198 add `st.glob.setdefault(name, value)` after the device store (device key also leaks into global) | none | yes (`live compares the global`, side effect) | **SURVIVOR S18** |
| M19 | L214 `return vals, frm` → `return vals, frm[::-1]` (sanity: letter order) | F03 F04 F05 F06 F07 F08 F09 F12 F13 F14 F18 H01 H03 H04 H05 H06 (16) | yes | no |
| M20 | L154 `stack, cur = [], None` → `stack, cur = [], st.__dict__.get("cur")` plus `st.cur = cur` after the loop (current device carried across files) | none | **no** (83/83) | **SURVIVOR S20** |
| M21 | L205 `if n in dev:` → `if n in dev and (n not in st.glob or dev[n] != st.glob[n]):` (device value equal to global labelled `G`) | none | **no** (83/83) | **SURVIVOR S21** |
| M22 | L173 `if in_device and lhs == "name":` → `if in_device and lhs == "name" and rhs:` (empty `name =` ignored) | none | **no** (83/83) | **SURVIVOR S22** |

Summary: 22 mutants; 11 survive all 26 fixtures (M07 M09 M10 M11 M12 M13 M16 M18 M20 M21 M22). Of those, 5 also pass
the tool's own selftest (M12 M16 M20 M21 M22). Three mutants (M04 M15 M17) are killed only by hold-out fixtures, so the
18 committed fixtures alone would not detect them (M14 is killed by F05 as well as H03).

## Survivors: minimal killing config, expected output, runnable repro

Each survivor is a config (plus argv) the frozen grammar accepts. The "expected" output is what the **original** tool
prints; I checked each against the registration.md §C2 text (quoted in the notes). Files:
`mutants/survivors/Sxx/{args.json,c*.conf,getoption.json,expected.out,expected.rc}`. `args.json` paths are relative to
`mutants/`.

Repro (reads only, writes nothing): `cd mutants && python3 -I repro.py` (prints original and mutant output per survivor,
then KILL / NO-KILL). Captured: `mutants/receipts/survivor-repro.txt`. Full mutant × survivor matrix (original vs mutant,
stdout+rc): `mutants/receipts/survivor-matrix.txt`, produced by `mutants/matrix.py`.

### S07 (M07: device table reset per file) — 2 files

`S07/c1.conf`
```
device {
  name = kbd-a
  repeat_rate = 50
}
```
`S07/c2.conf`
```
input {
  repeat_delay = 300
}
```
argv: `--config survivors/S07/c1.conf --config survivors/S07/c2.conf --keyboard kbd-a`
Expected (original, = §C2 "device value … else global"; devices persist, only the current device resets):
`MADO_KBDOPT: keyboard=kbd-a repeat_rate=50 repeat_delay=300 numlock=0 from=D/G/- unsupported=0`
Mutant: `... repeat_rate=25 repeat_delay=300 numlock=0 from=-/G/- unsupported=0`

### S09 (M09: name line comment not cut) — 1 file

`S09/c1.conf`
```
device {
  name = kbd-a # built-in keyboard
  repeat_rate = 50
}
```
argv: `--config survivors/S09/c1.conf --keyboard kbd-a`
Expected (§C2: "with a trailing `#`-comment cut and stripped"): `MADO_KBDOPT: keyboard=kbd-a repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`
Mutant: `... repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`

### S10 (M10: device not forgotten when stack empties) — 1 file

`S10/c1.conf`
```
device {
  name = kbd-a
}
device {
  repeat_rate = 50
}
```
argv: `--config survivors/S10/c1.conf --keyboard kbd-a`
Expected (§C2: "when the stack empties the current device is forgotten"; device-key line with no current device → unsupported +1, ignored):
`MADO_KBDOPT: keyboard=kbd-a repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1`
Mutant: `... repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`

### S11 (M11: device forgotten on any `}`) — 1 file

`S11/c1.conf`
```
device {
  name = kbd-a
  repeat_rate = 50
  touchpad {
  }
  repeat_delay = 100
}
```
argv: `--config survivors/S11/c1.conf --keyboard kbd-a`
Expected (§C2: the device is forgotten only when the stack EMPTIES; the nested block's `}` leaves stack `["device"]`):
`MADO_KBDOPT: keyboard=kbd-a repeat_rate=50 repeat_delay=100 numlock=0 from=D/D/- unsupported=0`
Mutant: `... repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=1`

### S12 (M12: case-folded device-name match) — 1 file

`S12/c1.conf`
```
device {
  name = Kbd-A
  repeat_rate = 50
}
```
argv: `--config survivors/S12/c1.conf --keyboard Kbd-A`
Expected (§C2: "the device block whose name equals the keyboard's name"; exact equality):
`MADO_KBDOPT: keyboard=Kbd-A repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`
Mutant: `... keyboard=Kbd-A repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`
Note: survives the selftest too (83/83). The committed fixtures contain no uppercase device name.

### S13 (M13: live compare uses a device) — 1 file + getoption

`S13/c1.conf`
```
input {
  repeat_rate = 40
}
device {
  name = kbd-x
  repeat_rate = 50
}
```
`S13/getoption.json`: `{"option": "input:repeat_rate", "int": 40, "set": true}`
argv: `--config survivors/S13/c1.conf --keyboard kbd-x --getoption survivors/S13/getoption.json`
Expected (§C2 `config=<global effective value, default if unset>`): 
```
MADO_KBDOPT: keyboard=kbd-x repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0
MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=40 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:repeat_delay config=600 live=? verdict=UNKNOWN
MADO_KBDOPT_LIVE: option=input:numlock_by_default config=0 live=? verdict=UNKNOWN
MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=UNKNOWN
```
Mutant: `config=50 live=40 verdict=DIFFER` and `DONE ... live=DIFFER`.

### S16 (M16: first device key wins) — 1 file

`S16/c1.conf`
```
device {
  name = kbd-a
  repeat_rate = 50
}
device {
  name = kbd-a
  repeat_rate = 60
}
```
argv: `--config survivors/S16/c1.conf --keyboard kbd-a`
Expected (§C2: "a second block with the same name merges, later keys win"):
`MADO_KBDOPT: keyboard=kbd-a repeat_rate=60 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`
Mutant: `... repeat_rate=50 ... from=D/-/- unsupported=0`
Note: survives selftest too; the selftest merge case uses different keys in each block.

### S18 (M18: device key also sets the global) — 1 file

`S18/c1.conf`
```
device {
  name = kbd-a
  repeat_rate = 50
}
```
argv: `--config survivors/S18/c1.conf --keyboard kbd-b`
Expected (§C2: "a device key sets the CURRENT device's value" — not the global):
`MADO_KBDOPT: keyboard=kbd-b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`
Mutant: `... keyboard=kbd-b repeat_rate=50 repeat_delay=600 numlock=0 from=G/-/- unsupported=0`

### S20 (M20: current device carried across files) — 2 files

`S20/c1.conf` (no closing brace: the device block is still open at end of file)
```
device {
  name = kbd-a
  repeat_rate = 50
```
`S20/c2.conf`
```
device {
  repeat_delay = 9
}
```
argv: `--config survivors/S20/c1.conf --config survivors/S20/c2.conf --keyboard kbd-a`
Expected (§C2: "the category stack and the current device reset at each file's start"; device key with no current device → unsupported +1):
`MADO_KBDOPT: keyboard=kbd-a repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=1`
Mutant: `... repeat_rate=50 repeat_delay=9 numlock=0 from=D/D/- unsupported=0`
Note: survives selftest too. The selftest "device state resets per file" case closes its block, so no device stays open.

### S21 (M21: device equal to global labelled `G`) — 1 file

`S21/c1.conf`
```
input {
  repeat_rate = 30
}
device {
  name = kbd-a
  repeat_rate = 30
}
```
argv: `--config survivors/S21/c1.conf --keyboard kbd-a`
Expected (§C2: "the device value if set for NAME … `from` letters D / G / -"; device value is set → `D`):
`MADO_KBDOPT: keyboard=kbd-a repeat_rate=30 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`
Mutant: `... repeat_rate=30 ... from=G/-/- unsupported=0`

### S22 (M22: empty `name =` ignored) — 1 file

`S22/c1.conf`
```
device {
  name =
  repeat_rate = 50
}
```
argv: `--config survivors/S22/c1.conf --keyboard ""`
Expected (§C2: "the current device becomes RHS … (created if absent)"; RHS is empty, so the device `""` is created and matches the empty NAME):
`MADO_KBDOPT: keyboard= repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`
Mutant: `MADO_KBDOPT: keyboard= repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1`
Note: the frozen text does not discuss an empty NAME; the expected value is the literal reading. An L1 ruling is needed if
an empty name should be unsupported instead; this survivor is a contract-wording question as well as a coverage gap.

## Thin kills (noted, not survivors)

- M04 (device value equal to default must still win): only H03 kills it. A committed-only suite would pass it.
- M15 (nested `input { touchpad { … } }` keys are not global): only H02.
- M17 (device key before its `name`, global not touched): only H01.
- M14 (device `numlock_by_default` ignored): F05 and H03.

## Ledger

- Tools installed: none. Python 3.14.8 as provided (`python3 -I`).
- Host: no `hyprctl` calls; no host reads.
- Lane: nothing written in the lane except this directory (`.ufo/waves/round-55/w2/R55W2MutTool1/`). No git or jj mutation.
- Scratch: `/fast/scratch/hyaku/mado-r55/R55W2MutTool1/` (removed before yield).
