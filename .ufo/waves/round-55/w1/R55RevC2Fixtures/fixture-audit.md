# Round 55 — C2 fixture audit (seat R55RevC2Fixtures, wave w1)

Scope: the 18 committed fixtures `fixtures/c2/F01..F18` (lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`).
Method: each expected output was derived by hand from `registration.md` §C2 alone (the tool, the config model,
the output grammar). The derivation was then re-checked by an independent interpreter written from the same text
(`receipts/interp.py`, scratch-origin, read-only). `expected.out` and `expected.rc` were diffed only after derivation.
No other seat's work, tool source or hold-out file was read.

## Result

- Committed expectations that disagree with the contract text: **none**. 18/18 derived stdout is byte-equal to
  `expected.out`; 18/18 derived exit status equals `expected.rc`.
- Committed fixture bytes: all 73 fixture files hash to the sha256 recorded in `frozen-tables.json` `c2.fixture_file_sha256`
  (no fixture changed after the freeze).
- One contract ambiguity decides one fixture (F10): see A1. Under the intended reading F10 holds; under a literal
  reading of the KEY sentence it does not. This is a contract-text defect, not a fixture disagreement.
- One source-citation gap affects F18 (A2): the numlock 0..1 range is cited to `ConfigValues.cpp:277-280`, which does
  not show it.
- F02 args: the committed pins are byte-consistent with the host and the live `hyprctl getoption` values. The keyboard name
  `at-translated-set-2-keyboard` is not in any committed pin and not on the live host (O1).

## Per-fixture hand derivation (contract §C2 only)

Defaults 25 / 600 / 0; global `input:` keys set GLOBAL; `device` block with `name` sets the current device; `from` letters D/G/-.

| id | args (summary) | hand-derived output (key fields) | rc | expected.out | verdict |
|---|---|---|---|---|---|
| F01 | `--config c1.conf` (empty file) | `keyboard=* 25 600 0 -/-/- unsupported=0`; DONE keyboards=1 live=NONE | 0 | same | match |
| F02 | `--config fetch/host-input.conf --keyboard at-translated-set-2-keyboard --getoption fetch/host-getoption.json` | globals rate 40 (G), delay 250 (G), `true`→numlock 1 (G); no device blocks; 3 LIVE lines all AGREE 40/250/1; DONE AGREE | 0 | same | match |
| F03 | `input { repeat_rate = 30 }` | `keyboard=* 30 600 0 G/-/- unsupported=0` | 0 | same | match |
| F04 | `input{rate 30, delay 300}`, `device{name=kbd-a; rate 50}`, `--keyboard kbd-a --keyboard kbd-b` | kbd-a `50 300 0 D/G/-`; kbd-b `30 300 0 G/G/-`; keyboards=2 | 0 | same | match |
| F05 | `input{numlock false}`, `device{name=kbd-a; numlock true}` | kbd-a `25 600 1 -/-/D`; kbd-b `25 600 0 -/-/G` | 0 | same | match |
| F06 | `input{rate 30}`, `device{name=kbd-a}` (no keys) | kbd-a `30 600 0 G/-/-` (named block with no keys falls back to global) | 0 | same | match |
| F07 | `numlock_by_default = nope` | VALUE `nope` starts with `no` → 0 (prefix rule, not unsupported); `-/-/G`; unsupported=0 | 0 | same | match (literal prefix rule) |
| F08 | `numlock_by_default = online` | VALUE starts with `on` → 1; `-/-/G`; unsupported=0 | 0 | same | match (literal prefix rule) |
| F09 | `input{rate 30}`, `input{rate 35}`, `device{name=kbd-a; rate 50}`, `device{name=kbd-a; delay 100}`, `--keyboard kbd-a` | merged device: rate 50 (D), delay 100 (D); numlock default 0 `-`; global rate 35 not used | 0 | same | match |
| F10 | `input{ repeat_rate = $r; repeat_delay = 9999 }`, top-level `device[kbd-a]:repeat_rate = 70`, `device[kbd-a]{ repeat_delay = 100 }`, `--keyboard kbd-a` | `$r` line → +1; 9999 out of 0..2000 → +1; two bracket-form device keys → +1 each; total 4; no value applied → `25 600 0 -/-/-` | 0 | same | match (depends on A1) |
| F11 | `--config c1.conf --config c2.conf` (c1 rate 30; c2 rate 45, numlock 1) | globals persist across files: rate 45 (G), delay default `-`, numlock 1 (G) | 0 | same | match |
| F12 | `repeat_rate = 33 # fast`; `repeat_delay = 4##0` | rate: RHS has one `#`, cut → 33 (G); delay RHS has `##` → +1, ignored → 600 `-`; unsupported=1 | 0 | same | match |
| F13 | `input{rate 30}` + `--getoption getoption.json` (live 40/250/1) | keyboard `30 600 0 G/-/-`; LIVE config 30/600/0 vs live 40/250/1 → DIFFER×3; DONE DIFFER | 0 | same | match |
| F14 | `input{rate 40}` + getoption with only repeat_rate=40 | rate AGREE; delay `live=?` UNKNOWN (config 600); numlock `live=?` UNKNOWN (config 0); DONE UNKNOWN | 0 | same | match |
| F15 | `--config .../does-not-exist.conf` | path missing → `unreadable`; stdout `MADO_KBDOPT: SETUP unreadable`; rc 2 | 2 | same | match |
| F16 | `--config c1.conf --getoption getoption.json` (`{not json`) | non-empty getoption line not a JSON object → `bad_json`; rc 2 | 2 | same | match |
| F17 | args `[]` | no `--config` → `usage`; rc 2 | 2 | same | match |
| F18 | `numlock_by_default = 2`, `repeat_delay = 2000`, `repeat_rate = 200` | numlock 2 out of 0..1 → +1 ignored; delay 2000 in range (inclusive) → G; rate 200 in range → G; numlock default `-`; from=G/G/-; unsupported=1 | 0 | same | match (depends on A2 for the numlock range) |

Derived lines for F13/F14/F16 and the setup-failure lines are exact (no extra lines before `SETUP`).

## Freeze-order and hash check

`frozen-tables.json` `c2.fixture_file_sha256` lists 18 fixtures with the same file set as on disk. Every on-disk file
matched its recorded sha256 (`receipts/drive-output.txt`: `frozen=ok` for all 18). `c2.committed_count=18`.

## Defects and ambiguities (contract text and cited sources)

**A1 — KEY formation with an empty stack (decides F10).** §C2 says "KEY is the stack joined with `:` then `:` then LHS".
With an empty stack this literally yields `:<LHS>`, which matches no RELEVANT rule and would not count the top-level
`device[kbd-a]:repeat_rate = 70` line. Under that literal reading F10 derives `unsupported=3`, not 4.
Evidence: `receipts/ablation-literal-empty-stack.txt` → `FAILS: ['F10']` (all other 17 still match); intended reading
→ `FAILS: none`. The committed expectation (4) assumes the intended reading (empty stack → KEY = LHS). The frozen text
should say so; a counter or tool written from the literal sentence would fail F10.

**A2 — numlock 0..1 range is not in the cited pin (decides F18).** §C2 "Range (ConfigValues.cpp:277-280 pin …)" lists
`numlock_by_default` 0..1. The pin at `fetch/Hyprland-ConfigValues.cpp` line 277 is
`MS<Bool>("input:numlock_by_default", "Engage numlock by default.", false, {.refresh = …})` — a Bool with no `.min`/`.max`.
Lines 279–280 do show `repeat_rate` `{.min = 0, .max = 200}` and `repeat_delay` `{.max = 2000}` (matching the contract).
So the 0..1 numlock range is the seat's inference, not the cited source. F18 `numlock_by_default = 2` → unsupported is what the
contract text says; the source is silent. Noted, not a fixture-vs-text disagreement.

**O1 — F02 keyboard name is unverifiable against the pins and absent on this host.** `--keyboard at-translated-set-2-keyboard`
is not in any committed pin (`SHA256SUMS.txt` lists no device-list pin). `hyprctl devices -j` on this host lists 10 keyboards
(`razer-razer-deathadder-v2-keyboard`, `hp--inc-hyperx-alloy-origins-core`, `hl-virtual-keyboard-fcitx5`, …) and no
`at-translated-set-2-keyboard`. The expected output does not depend on the name (host config has no device block), so the
expectation is correct, but F02 therefore does not exercise a per-keyboard join against a real device. The contract does not
require the name to exist; this is a provenance note.

**O2 — unspecified precedence (no fixture uses it).** When a `--config` file is unreadable and `--getoption` is bad JSON,
the contract does not say which setup reason prints. Also "non-empty `--getoption` line" does not say whether a
whitespace-only line is empty. No C2 fixture exercises either case.

## F02 args against the committed host pins (requested check)

| check | command (read-only) | result |
|---|---|---|
| pin sha256 | `sha256sum -c fetch/SHA256SUMS.txt` | `host-input.conf: OK`, `host-getoption.json: OK` |
| pin == live config | `cmp fetch/host-input.conf ~/.config/hypr/input.conf` | identical, 1584 bytes |
| pin values == live | `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j` | 40 / 250 / 1 (pin: 40 / 250 / 1) |
| host build | `hyprctl version` | Hyprland 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f` (matches registration pin) |
| keyboard name | `hyprctl devices -j` | not present (O1) |

Derived F02 from the pin: `keyboard=at-translated-set-2-keyboard repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0`;
LIVE AGREE ×3; DONE AGREE. Matches `expected.out` exactly.

## Not verified / not run

- The committed tool `tools/mado-kbdopts.py` was not run and was not read (the audit is against the text, not the tool).
- The hold-out fixtures were not looked for and not read (sealed; not a seat input).
- The C2 counter/harness (`quality/check-r55-controls.py`) was not run; this audit is a hand/independent check only.
- Source semantics (the contract's citations beyond the two checked above) were not re-audited.
- The `numlock` source gap (A2) and the empty-stack reading (A1) are reported for the L1; no contract text was edited.

## Receipts (in this directory, `receipts/`)

- `interp.py` — independent interpreter written from §C2 (sha256 `1abe00b6…df2d35c2`).
- `drive.py` — runs it on the 18 committed fixtures (cwd = lane root), compares bytes and rc, checks frozen sha256 (sha256 `c5dca9e0…106e2`).
- `drive-output.txt` — `FAILS: none`, 18 × `out_match=True rc_match=True frozen=ok`.
- `ablation-literal-empty-stack.txt` — `FAILS: ['F10']` under the literal empty-stack reading.
