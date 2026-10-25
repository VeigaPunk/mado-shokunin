# ExecToolIndep — C1 independent `--live` implementation (round 40, w1)

**Seat:** ExecToolIndep (leaf, no dispatch, no background jobs).
**Deliverable:** `.ufo/waves/round-40/w1/ExecToolIndep/mado-options.py` — the BASE tool plus an
independently written `--live` / `--hyprctl` / `--probe` merge, written from the frozen spec and
the upstream sources only, then scored with the frozen counter.
**File facts:** 1675 lines (base 1050), sha256 `05b639be8dd599dea978aa9fc0b07bcb449d22b383fd21b571fbadccd457b6d2`,
base copy sha256 `461f8c3c245bdfb6dcaac068a5ab378326c75dc91992b8012f9ca0e5019fb03a`.
**Verdict on the frozen counter:** `fixtures=13/13 tool=present verdict=TARGET_MET`, exit 0.

## 1. What was read before writing (spec-only, per the assignment)

- `.ufo/waves/round-40/registration.md` § C1 (frozen at `5e7e88525cc539563de7746361b2650802e81809`).
- `tools/mado-options.py` (the BASE, all 1050 lines).
- Upstream, pinned: Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f`
  `src/config/legacy/ConfigManager.cpp` (gradient handler 103-160, gap 168-185, font weight 193-205),
  `src/config/shared/complex/ComplexDataTypes.hpp` (toString 69-76, gap 105-145, weight 154-176),
  `src/debug/HyprCtl.cpp` (dispatchGetOption 1647-1725), `src/config/shared/parserUtils/ParserUtils.cpp`
  (parseColor 23-152), `src/helpers/Color.{hpp,cpp}` (ctor/getAsHex); hyprlang `v0.6.8`
  `src/config.cpp` (configStringToInt 185-264, FLOAT via `std::stof` 462-468, STR 492-494);
  hyprutils `isNumber2`/`strToNumber` (`src/string/String.cpp:46-82`).
- **Not read before writing:** `c1/ctl-ref-tool.py.txt`, `quality/counters/c1-r40-live.py`.
  The counter was opened only after the first full implementation existed, to score it and to run
  the assigned conversion-table diff. The reference control was never read and never run.

## 2. Behaviour implemented (line refs into the delivered copy)

| Piece | Where | Behaviour |
|---|---|---|
| flags | `main` 998-1008 | `--live` and `--getoption` are a mutually exclusive group; `--hyprctl PATH`; `--probe KEY` (repeatable, implies `--live`) |
| probe guard | `probe_is_safe` 848, `main` 1014-1019 | probe key must fullmatch `[A-Za-z0-9_.:]+` and not start with `-`; otherwise exit 2 **before** any program runs |
| one read verb | `run_getoption` 853 | exactly `[program, "getoption", "-j", key]`, one call per declared key (sorted) then one per new probe (`read_live` 896) |
| reply parse | `native_record` 871 | `no such option` → no record (key stays `config-only`); otherwise one JSON object with a known form and `set`, else exit 5 naming the key |
| failures | `CompositorError` 205, `main` 1038 | program missing / non-zero exit / non-JSON / no form / no `set` → exit 5, key on stderr |
| int | `hl_int` 586 | hyprlang `configStringToInt`: `0x` hex, `rgba(r,g,b,a)` (alpha×255 rounded half-away, `uint8` wrap), 8-digit RGBA→ARGB, `rgb(...)` comma/6-hex, `true|on|yes`→1, `false|off|no`→0, else `isNumber(allowfloat=false)` + integer literal |
| float | `hl_float` 639 | `std::stof` front end (leading literal, trailing text ignored) |
| str | `native_equal` 819 | trimmed exact equality |
| custom | `custom_equal` 804 | dispatch on the reply's own shape: ends `deg` → gradient, 4 integer tokens → gap, 1 token → font weight, else exact text |
| gradient | `gradient_angle` 708 + `gradient_text` 725 + `parse_color` 647 | colours via `ParserUtils::parseColor` → lowercase unpadded ARGB hex words then `<N>deg`; angle inherited from the last earlier declarer that carried `deg` (0 if none), matching the handler's colours-clear-but-angle-keep |
| gap | `gap_text` 743 | 1→all, 2→v h, 3→t h b, 4→t r b l, >4 uses the first four (`CCssGapData`) |
| font weight | `font_weight_text` 766 | case-insensitive `WEIGHTS` name → value; else numeric with `<100 or >1000 → 400` |
| labels | `merge_live_rows` 912 | base vocabulary (`agreement` / `agreement*` / `mismatch` / `config-only` / `live-default`), plus each met reply kept verbatim in a new per-row `live` field |
| history | `State.declare` 372-390 | per-key `_history` list (append-only) so the gradient angle can be inherited across declarers |
| selftest | 1514-1640 | 26 new hermetic checks (stub compositor, exact argv log, every form, inheritance, `no such option`, probe, set=false, missing program, non-zero exit, hostile probe with an empty call log, root-unchanged snapshot) |

Static path untouched: `python3 -I <copy> --home "$HOME"` is byte-identical to the base output
(70 rows, `cmp` clean).

## 3. Evidence (commands and their exact output)

### 3.1 Frozen counter — first scoring run, verbatim

`cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live.py --repo . --rev 5e7e88525cc539563de7746361b2650802e81809 --tool .ufo/waves/round-40/w1/ExecToolIndep/mado-options.py`
(exit 1)

```
PRED-C1-r40-v1 clause=b rc=0 selftest=94/94
PRED-C1-r40-v1 fixture=gen0 ok=0 row optx010:float10 lacks live
PRED-C1-r40-v1 fixture=gen1 ok=0 row optx110:gap10 lacks live
PRED-C1-r40-v1 fixture=gen2 ok=0 row optx210:weight10 lacks live
PRED-C1-r40-v1 fixture=gen3 ok=0 row optx310:bool10 lacks live
PRED-C1-r40-v1 fixture=gen4 ok=0 row optx410:str10 lacks live
PRED-C1-r40-v1 fixture=gen5 ok=0 row optx510:num10 lacks live
PRED-C1-r40-v1 fixture=gen6 ok=0 row optx611:gap11 lacks live
PRED-C1-r40-v1 fixture=gen7 ok=0 row optx710:bool10 lacks live
PRED-C1-r40-v1 fixture=probe0 ok=0 row optprobe11:str11 lacks live
PRED-C1-r40-v1 fixture=fail0 ok=0 valid run: row optfail10:bool10 lacks live
PRED-C1-r40-v1 fixture=bad0 ok=0 valid run: row optbad10:ginh10 lacks live
PRED-C1-r40-v1 fixture=missing0 ok=0 valid run: row optmissing10:weight10 lacks live
PRED-C1-r40-v1 fixture=hostile0 ok=0 valid run: row opthostile10:colour10 lacks live
PRED-C1-r40-v1 clauses=a:1 b:1 g:1 k:1
PRED-C1-r40-v1: fixtures=0/13 tool=present verdict=TARGET_MISSED rev=5e7e88525cc539563de7746361b2650802e81809
```

**Reading of the failure (a spec finding, not a conversion defect):** every fixture failed on the
same clause — `check_live` (counter 514-517) requires each row that met a reply to carry a
non-`None` `live` field. The registration's C1 deliverable text never asks for that field; it says
the counter "checks the labels, the exact argv and that the config root is unchanged". The field is
only visible in the counter's code (and in the mutant list's "live field dropped"). The conversion,
labels, argv and exit codes were already right on that run: `clauses=a:1 b:1 g:1 k:1`, and the
first failure reported per fixture is the `live` clause, which the counter evaluates last.
Fix: `merge_live_rows` now stores the native reply value in `live` (912-937) and the selftest pins
it (three checks: int reply kept, custom text kept, `config-only` row carries none).

### 3.2 Frozen counter — final scoring run, verbatim

`cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live.py --repo . --rev 5e7e88525cc539563de7746361b2650802e81809 --tool .ufo/waves/round-40/w1/ExecToolIndep/mado-options.py`
(exit 0)

```
PRED-C1-r40-v1 clause=b rc=0 selftest=97/97
PRED-C1-r40-v1 fixture=gen0 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen1 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen2 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen3 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen4 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen5 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen6 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen7 ok=1 rows=15
PRED-C1-r40-v1 fixture=probe0 ok=1 rows=17
PRED-C1-r40-v1 fixture=fail0 ok=1 rc=5 named=1
PRED-C1-r40-v1 fixture=bad0 ok=1 rc=5 named=1
PRED-C1-r40-v1 fixture=missing0 ok=1 rc=5
PRED-C1-r40-v1 fixture=hostile0 ok=1 all three refused=1
PRED-C1-r40-v1 clauses=a:1 b:1 g:1 k:1
PRED-C1-r40-v1: fixtures=13/13 tool=present verdict=TARGET_MET rev=5e7e88525cc539563de7746361b2650802e81809
```

No failing fixture line remains. Clause b: `MADO_OPTIONS_SELFTEST: 97/97 passed`, k == n = 97 >= 79
(base 71).

### 3.3 Out-of-distribution check on the live host (the declared residual, reported not scored)

`python3 -I <copy> --home "$HOME" --live > /tmp/live-host.json` → exit 0, 70 rows:
`{'agreement': 62, 'agreement*': 8}` — 0 mismatch. This reproduces the reference model's declared
host census (62/8/0) on an independently written implementation, so the two models agree on the
whole host population, not only on the counter's generated value space.

Cross-check against the frozen capture `.ufo/waves/round-40/c1/native-capture.jsonl`:
70 keys, forms `{'int': 44, 'float': 5, 'custom': 13, 'str': 8}`, key sets equal, and **0**
disagreements between my rows' `live`/`set` fields and the committed capture.

`hyprctl getoption -j zz:no-such-option` → `no such option`, rc 0 (the argv form the tool uses is
accepted by the real client, and an unknown key is not a failure).

Probe path on the host: `--probe general:gaps_workspaces --probe decoration:screen_shader` → 72 rows,
`{'agreement': 62, 'agreement*': 8, 'live-default': 2}`; e.g.
`{'key': 'general:gaps_workspaces', 'value': '0', ..., 'set': False, 'live': 0, 'agreement': 'live-default'}`.
`--probe zz:nothing` (compositor answers `no such option`) adds no row — the same choice the counter's
probe fixture expects (`zzprobe:nothing` is not in `want`).

Failure/hostile paths on the host:
- `--hyprctl /nonexistent/hyprctl` → `mado-options.py: animations:enabled: cannot run /nonexistent/hyprctl: No such file or directory`, rc 5.
- `--probe 'general:gaps_in; rm -rf /'` → `mado-options.py: hostile probe key 'general:gaps_in; rm -rf /' refused`, rc 2.
- `--probe --version` / `--probe -x` → argparse `argument --probe: expected one argument`, rc 2.
- `--probe ""` → `hostile probe key '' refused`, rc 2.

### 3.4 Static regression

`cmp` of base and copy output on the host tree: identical, 70 rows.

## 4. Conversion-table diff against the counter's reference model

Script `.ufo/waves/round-40/w1/ExecToolIndep/diff-model.py` (seat artifact; run it from the lane
root) imports both modules with bytecode writing disabled and compares `hl_int`,
`gradient_text(declared, 0)`, `gap_text`, `WEIGHTS` over a designed value space. `WEIGHTS` is **identical** (12 entries, same numbers).

### 4.1 On the fixtures' own value space: no disagreement

`gradient_text` over the generator's spellings (`rgba(rrggbbaa)`, `0xARGB`, `rgba(r,g,b,a)` with
alpha in {1, 0.8, 0.4}, `rgb(rrggbb)`, `rgb(r,g,b)`) × 1-3 colours × angles {none, 0deg, 45deg,
90deg}: **0 of 620** declarations disagree. `hl_int` agrees on every spelling the generator emits
(including the quirk spellings `yes, please :)`, `on # note`, negative integers, `rgba(r,g,b,0.8)`).
`gap_text` agrees on 1-4 plain integers. Font weight agrees on all 12 names plus `ultraheavy`
case-insensitively.

### 4.2 Every disagreement over the wider space (8 880 gradient declarations + edge inputs)

1. **`hl_int`, 1 case:** `' 5 '` → mine `5`, counter `None`. Mine strips inside `hl_int`; the
   counter does not, but its `model_equal` always passes `declared.strip()`, so this is
   unobservable in the scored path. (Mine follows the C++ caller, which trims the value.)
2. **`gradient_text`, 7332/8880 — three classes, none in the fixture space:**
   - **`#` spellings, 5688 cases:** `'#e68e0d'` → mine `'ffe68e0d 0deg'`, counter `None`.
     Mine parses colours with `ParserUtils::parseColor` (which accepts `#rgb`, `#rrggbb`,
     `#rrggbbaa` and bare integers); the counter's model reuses `hl_int`, which has no `#` branch.
     Mine is the faithful one; the host tree does use `#`-free spellings, so nothing observed
     changes.
   - **Unparseable colour token, 1128 cases:** `'zzz'` → mine `'0 0deg'`, counter `None`.
     The real handler logs the parse error, keeps the tokens it could parse, and substitutes
     transparent when none parsed (`ConfigManager.cpp:146-151`); mine models that, the counter
     aborts. Mine is faithful, the counter stricter.
   - **Malformed angle prefix, 516 cases:** `'rgba(33ccffee) deg'` → mine `'ee33ccff 0deg'`,
     counter raises `ValueError` (its `int('')`). C++ `std::stoi` throws, the handler keeps the
     inherited angle and still breaks out of the loop (`ConfigManager.cpp:117-127`); mine models
     that (`_stoi` + keep-inherited), the counter raises.
3. **`gap_text`, 5 cases:** `'0x1'` mine `'0 0 0 0'` (C++ `std::stoi("0x1")` = 0) vs counter
   `ValueError`; `'a b'` mine `None` vs `ValueError`; `'4.0 5'` mine `'4 5 4 5'` (`stoi` front end)
   vs `ValueError`; `''` and `'  '` mine `None` vs `''`. The generator only emits plain integers.
4. **Font weight, 10 cases:** numeric and whitespace inputs — `'400'` mine `'400'` vs counter
   `'-1'`; `'50'`/`'2000'` mine `'400'` vs `'-1'`; `'garbage'`/`''` mine `None` vs `'-1'`;
   `'  bold  '` mine `'700'` (counter `'-1'` only because the raw value is passed; its
   `model_equal` strips first, so this one is unobservable). Mine implements
   `CFontWeightConfigValueData::parseWeight`'s numeric path; the counter's model only does the name
   lookup. The generator emits names only, so this never scores.

**Source quirk found while diffing, deliberately not modelled:** `parseWeight`
(`ComplexDataTypes.hpp:163-176`) lowercases into `lcWeight`, and in the numeric branch assigns
`m_value` only when the number is **out of** 100..1000 (`m_value = 400`); an in-range numeric
declaration (`"500"`) leaves `m_value` at its previous value (400 on a first declaration). My
`font_weight_text` returns the in-range number (the evident intent); the counter's model returns
`-1`. Neither matches the C++ exactly. Not exercised by the fixtures or the host (no numeric
font-weight option is declared there); recorded as a known divergence.

**Counter finding:** `model_equal` (counter 199-220) is never called anywhere in the counter — the
scored path uses `Fixture.live_of`/`Fixture.want` only. So the docstring's "the code is the same
sentence" comparison model is not itself exercised; only the generator's `live_of` is. This is why
the four divergences above do not affect scoring.

## 5. Risks / limitations of the delivered implementation

1. `custom` dispatch uses the reply's own shape (ends `deg` / 4 int tokens / 1 token). That is how
   the compositor's registered type is recovered from a `custom` reply; a custom type whose
   `toString` happened to look like another shape would be mis-dispatched. Not reachable on the
   host census (13 custom replies on the host: 9 gradients, 2 CSS gaps, 2 font weights - `400` and `1000`).
2. `live` is added only by the `--live` merge; the `--getoption FILE` path is byte-for-byte the
   base behaviour (base selftest still green inside the 97).
3. An invalid gradient declaration is modelled as "colours it could parse, else transparent"; the
   real compositor instead *rejects* the line and keeps the previous value. A fixture that declared
   a syntactically invalid gradient after a valid one would expose this; the generator does not.
4. Gradient angles are rendered with plain `int()` on the double round trip. The real
   `float m_angle` is float32, and a float32 round trip truncates 18 of 721 integer degrees by one
   (e.g. `31deg` → `30deg`). The counter's stub does not model float32 either, so modelling it
   would have *lost* fixtures; recorded, not implemented.
5. Float comparison is exact (`hl_float` vs the JSON number); `hyprctl` prints `{:.2f}`, so a
   declaration with more than two decimals can never agree. That is the compositor's own display
   truncation, not a tool defect.
6. `--probe` implies `--live`; the counter never tests the bare `--probe`.
7. `--hyprctl` without `--live` is ignored rather than refused.

## 6. Write scope / hygiene

- Wrote only `.ufo/waves/round-40/w1/ExecToolIndep/` (the tool copy) and this report. No tracked
  file touched (`git status --porcelain` shows only untracked round-40 wave dirs).
- No mutating git/jj call. No pacman. No compositor verb beyond `hyprctl getoption -j`,
  `hyprctl version`-class reads (`descriptions -j` attempted once) — all read-only.
- Tooling: nothing installed (stdlib only; `re` added to the imports, inside the counter's
  `STDLIB_ALLOW`).
- Scratch: upstream sources were fetched to `/tmp/r40src/` and host runs to `/tmp/live-*.json`;
  all of it is deleted. The differential analysis is preserved in-seat as `diff-model.py` so the
  L1 can re-run it (`python3 .ufo/waves/round-40/w1/ExecToolIndep/diff-model.py`).
- Disclosed by-product: importing the counter to diff it refreshed the gitignored
  `quality/counters/__pycache__/c1-r40-live.cpython-314.pyc` (that directory pre-exists with
  sibling seats' `.pyc` files; no tracked file and no source byte changed).

## 7. What the L1 should run after integration

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live.py --repo . --rev <data-tip>`
   (expect `fixtures=13/13 ... TARGET_MET`, exit 0, `selftest=k/n` with n >= 79).
2. `python3 -I tools/mado-options.py --selftest` (expect 97/97 after the copy lands).
3. `python3 -I tools/mado-options.py --home "$HOME" --live` (expect 70 rows, 62 agreement /
   8 agreement*, 0 mismatch) if the live receipt is wanted.
4. `bash tools/mado-verify.sh --selftest` (unchanged, 460/460) and `quality/check-axis-scores.py`.
5. Optional: `python3 .ufo/waves/round-40/w1/ExecToolIndep/diff-model.py` reprints the
   conversion-table diff in §4 (it imports the counter with bytecode writing disabled).

Seat directory contents: `mado-options.py` (the deliverable), `diff-model.py` (the analysis,
not a lane tool), and this report at `.ufo/waves/round-40/w1/ExecToolIndep.md`.
