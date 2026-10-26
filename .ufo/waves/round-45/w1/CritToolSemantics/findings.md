# Where the C1 contract diverges from Hyprland's real behaviour

Seat `CritToolSemantics`, mado round 45 w1. Target: the contract of `tools/mado-monitors.py`, i.e. the
docstring **and** the behaviour of the reference `.ufo/waves/round-45/l1-draft/mado-monitors.py`
(selftest 33/33), compared against the seven Hyprland pins (`fetch/`, sha256 in
`receipts/fetch-sha256.txt`) at `efb50993` (0.56.2) plus `hyprutils` 0.14.2 and the wiki pin.

Method. The reference was copied byte-identical to scratch (`ref.py`, sha256 in
`receipts/tool-runs.txt`) and run read-only on synthetic dumps/configs (R1-R18 in
`receipts/tool-runs.txt`); every "Hyprland actual" below is a locator in a pin, computed with `grep -n`. Every quoted source
fragment is checked by `receipts/quote-check.sh`, which greps the pinned file at the cited line and prints
`OK`/`FAIL` (`receipts/quote-check.txt`: 45/45 OK). No host state, no compositor command, no PATH tool:
the tool reads files and stdin only.

Severity vocabulary: **wrong verdict** (tool prints a verdict Hyprland's own behaviour contradicts),
**missing verdict** (tool refuses/gates, no false claim), **documented limit** (behaviour disclosed, but
the disclosure is incomplete or the field is silently dropped).

---

## 1. Wrong verdicts (three, plus one conditional)

### D-A — the scale integrality test runs in double; Hyprland's runs in float32

| | |
|---|---|
| input | `monitor = DP-1, 3440x1440@100, 0x0, 0.32`, live `3440x1440@100, 0x0, scale 0.32` |
| tool | `differ=scale verdict=DIFFER`, exit 1 (R2); the same rule against live `scale 0.333333` prints `verdict=AGREE` (R3) |
| Hyprland | `Vector2D logicalSize = m_pixelSize / m_scale;` (Hyprland-Monitor.cpp:996) is float32: `f32(3440/0.32f) = 10750.0`, `f32(1440/0.32f) = 4500.0`, both equal `round` → the correction block at :997 is not entered, `m_scale` stays `RULE->m_scale` (:992). Live scale = 0.32; the rule is exactly what runs |
| locator | Hyprland-Monitor.cpp:992-1018 (test at :996-997) |
| severity | **wrong verdict** — false DIFFER; and a false AGREE if a client ever sets 0.333333 |

The docstring's sentence `E = S when both width/S and height/S are whole` does not say in which
arithmetic; the reference computes `whole(w / s)` in Python double (`expected_scale`, mado-monitors.py:327-338),
Hyprland in `Vector2D` float. The two disagree for a family of two-decimal scales on every common
resolution — the tool's `S` test fails where Hyprland's passes, so the tool substitutes a corrected value:

| mode | scale | Hyprland (keeps) | tool `E` | tool verdict for live = rule |
|---|---|---|---|---|
| 3440x1440 | 0.32 | 0.32 | 0.333333 | DIFFER (R2) |
| 3440x1440 | 0.64 | 0.64 | 0.625 | DIFFER (R5) |
| 1920x1080 | 0.48 | 0.48 | 0.5 | DIFFER (R4) |
| 1920x1080, 2560x1440, 2880x1800, 3840x2160, 5120x1440, 1280x720, 1920x1200, 2560x1600 | 0.32 / 0.48 / 0.64 / 0.96 / 1.28 / 1.92 / 2.56 / 3.84 | S | the next k/120 divisor | DIFFER |

(computed table: f32 emulation of `w/s` vs the reference's `expected_scale`; 38 of the 54 computed
`(scale, w, h)` divergences over 2-decimal scales 0.25-4.00 on ten real modes; the rest are the
reverse direction). The commonly used
1.25 / 1.5 / 1.6 / 1.75 / 2.0 are **not** affected (the search returns S), so this is a hole, not a
broken model. The direction "Hyprland corrects, tool keeps" also exists (0.3, 0.6, 1.2, 2.4 on several
modes) but its size depends on the precision of `Vector2D operator/`, which is not pinned — [INFERENCE].

**Smallest safe correction:** run every integrality test in the same width Hyprland does —
`f32(w / f32(s))` compared with `f32(round(...))` — for the first test and for each `k/120` candidate
in the search; fixtures: 0.32 on 3440x1440, 0.48 on 1920x1080.

### D-B — the `transform` modifier accepts what Hyprland accepts (`isNumber` + `stoi` + clamp), not one digit

| | |
|---|---|
| input | `monitor = DP-1, 3440x1440@100, 0x0, 1` then `monitor = DP-1, transform, 07`; live `transform 7` |
| tool | `badrules=1 rules=1`, rule 1 `transform=0`, `differ=transform verdict=DIFFER`, exit 1 (R6); control `transform, 7` → `verdict=AGREE`, exit 0 (R7) |
| Hyprland | `isNumber("07")` true → `std::stoi` = 7 → `std::clamp(TSF, 0, 7) == TSF` (Hyprland-Parser.cpp:214-221) → the named rule is copied with transform 7 and re-added (Hyprland-legacy-ConfigManager.cpp:1303-1316) → applied at Hyprland-Monitor.cpp:655. Live 7; the config is honoured |
| locator | Hyprland-Parser.cpp:214-221; Hyprland-legacy-ConfigManager.cpp:1310-1314; hyprutils-String.cpp:50-84 (`isNumber2`) |
| severity | **wrong verdict** — and the drop is **ungated**: `badrules` is not one of the top-verdict gates (only `v2` and `unsupported` are), so the run continues and claims DIFFER |

`-0` is the same class: `isNumber2` allows `-` at index 0 (hyprutils-String.cpp:59-61), `stoi("-0")` = 0,
so Hyprland re-adds the rule with transform 0 while the tool counts `badrules` and keeps the old rule
(R8: DIFFER against live 0, which Hyprland's rule also says). Values Hyprland genuinely rejects
(`8`, `9`, `10`, `3.0`) are dropped by both, so `badrules` is right for those.

**Smallest safe correction:** model Hyprland's predicate — `[+-]?` is *not* allowed, `-` only at index 0,
digits only, then `stoi` and `0 <= v <= 7`; or, cheaper and still safe, treat any `transform`-modifier
line the tool refuses as `unsupported` so the top verdict becomes NOT_COMPARED.

### D-C — `addreserved` numbers are parsed with `std::stoi`, not `-?[0-9]{1,6}`

| | |
|---|---|
| input | `monitor = , 3440x1440@100, 0x0, 1, transform, 1` and `monitor = DP-2, addreserved, +5, 0, 0, 0`; live DP-2 `1920x1080@60, x=3440, scale 1, transform 0` |
| tool | `badrules=1`, rules=1 → DP-2 falls to the empty-selector rule → `differ=mode,position,transform verdict=DIFFER` (R9) |
| Hyprland | `std::stoi("+5")` = 5 (Hyprland-legacy-ConfigManager.cpp:1323-1324) → no rule named DP-2 → falls through to `monitorRuleMgr()->add(parser.rule())` (:1341) → DP-2 gets the default rule (preferred, auto position, auto scale, transform 0) → live matches → AGREE. Receipt R10 is the exact equivalent (`addreserved, 5`): `rule=2 ... verdict=AGREE` |
| locator | Hyprland-legacy-ConfigManager.cpp:1323-1326 (stoi, catch), :1330-1334 (mutate-or-fall), :1341 (add) |
| severity | **wrong verdict**, again through the ungated `badrules` path |

`5.5`, `10abc`, `+5` and 7+-digit values are all `stoi`-prefix-parsable; the tool's fullmatch rejects them.
The `desc:`-selector case is unaffected (string equality on `m_name` at :1330 matches the tool).

**Smallest safe correction:** for the `addreserved` fields accept `^[[:space:]]*[+-]?[0-9]+` (stoi prefix
grammar) and only count `badrules` when `stoi` would throw; keep the "a rule exists → mutate nothing"
model as is (the reserved area is not compared, so mutation has no verdict effect).

### D-E — "no clean divisor" is a defined Hyprland fallback, not "not compared"

| | |
|---|---|
| input | `monitor = DP-1, 1920x1200@60, 0x0, 14.166667`, live `1920x1200@60, 0x0, scale 1` |
| tool | `expected_scale` returns None → scale is dropped from the field list → `differ=- verdict=AGREE`, exit 0 (R15) |
| Hyprland | the search window for `K = round(14.166667*120) = 1700` is `k in [1611, 1789]`, and no such `k` divides both `1920*120` and `1200*120` (gcd 28800 has no divisor in the window) → `found == false` → `Log::ERR "failed to find a clean divisor"` → `m_scale = getDefaultScale()` (Hyprland-Monitor.cpp:1029-1036), which is 1, 1.5 or 2 by physical PPI (Hyprland-Monitor.cpp:1402-1417) — never 14.166667 |
| locator | Hyprland-Monitor.cpp:1010-1026 (search), :1029-1036 (fallback), :1402-1417 (`getDefaultScale`) |
| severity | **wrong verdict** — the one field the tool exists to check is silently removed and the top verdict still says AGREE |

The docstring does disclose `none found means the scale is not compared`, but that disclosure is wrong
about Hyprland: Hyprland substitutes a value the tool could bound (1 <= E <= 2). Skipping the field turns
a guaranteed mismatch into an AGREE.

**Smallest safe correction:** when the search fails for an explicit scale, do not print AGREE — either
compare against `getDefaultScale`'s three possible values (1, 1.5, 2; the physical size is not in the
dump, so accept any of them, which still fails for this input) or set `unsupported`/a new counter so the
top verdict is NOT_COMPARED.

### D-L — [INFERENCE, unverified] the mirror target is resolved by a monitor query, not by exact name

| | |
|---|---|
| input | `monitor = DP-2, 1920x1080@60, 0x0, 1, mirror, desc:Acme` with DP-1's description `Acme Panel X1 SER`, live DP-2 `mirrorOf=0` |
| tool | `ids = [names == "desc:Acme"]` → empty → `differ=mirror verdict=DIFFER` (R18) |
| Hyprland | `setMirror` resolves the target with `State::monitorState()->query().relativeTo(focus).configString(mirrorOf)` (Hyprland-Monitor.cpp:1335) — a monitor-query config string, not `m_name ==` equality; the same selector grammar matches `desc:` (Hyprland-Monitor.cpp:1201-1211). If `configString` accepts the description/`desc:` forms, Hyprland mirrors DP-2 onto DP-1 and `mirrorOf` is `0`, i.e. AGREE |
| locator | Hyprland-Monitor.cpp:1335; the `Query`/`CMonitorState` source is **not among the pins**, so the acceptance set beyond exact name is unverified here |
| severity | **wrong verdict if confirmed**; otherwise a documentation gap (the docstring says "`mirror` VALUE is the mirrored output's name") |

Pinned-adjacent note, no verdict effect: Hyprland refuses a self-mirror and a mirror of a mirror
(Hyprland-Monitor.cpp:1340-1346) and then leaves `m_mirrorOf` unset, so both Hyprland and the tool print
DIFFER. **Smallest safe correction:** resolve `mirror` with the same matcher as a `desc:` selector, or
state "name only" in the docstring and add it to the DIFFER causes.

---

## 2. Missing verdicts (gated by `unsupported`; safe, but the docstring states Hyprland's grammar wrongly)

### D-D — MODE / POSITION / SCALE grammar: `stoi`/`stof` vs the contract's regexes

Hyprland does not validate the mode, position or scale as a whole string:

- mode: `stoi(value.substr(0, find_first_of('x')))`, `stoi(value.substr(find_first_of('x')+1, find_first_of('@')))`,
  rate `stof(value.substr(find_first_of('@')+1))` (Hyprland-Parser.cpp:124-138) — accepts `@1e2`,
  `@100.`, `@100abc`, `@+100`, `@1000`, 6-7 digit resolutions, `3440x1440x2`; a parse failure only
  appends to `m_error`, and `handleMonitor` **still adds the rule** (:1345-1347 ignore the return values,
  :1384 adds) with resolution `0x0` (preferred) for a mode error (Hyprland-Parser.cpp:111-118).
- position: `stoi` on both halves (Hyprland-Parser.cpp:175-183); `-2147483647` is the auto sentinel.
- scale: `isNumber(value, true)` then `stof`, `< 0.25` → `m_scale = 1` and an error (Hyprland-Parser.cpp:197-205);
  the tool models the 0.25 rule correctly, but any `isNumber` rejection (`1.`, `.5`, `+1.5`, `1e1`) means
  Hyprland applies **auto** scale while the tool refuses the line.

Receipts: `@1000` and `@1e2` → `unsupported=1 ... verdict=NOT_COMPARED`, exit 5 (R12/R13). Because
`unsupported` gates the top verdict (mado-monitors.py:434-435), no false claim is made — this is a
**missing verdict**, and it is disclosed as "outside these forms". The defect is in the docstring's
attribution: it presents those forms as Hyprland's parser ("the number after `@` rounded to a 32-bit
float", "as Hyprland's parser does" for `< 0.25`). The `< 0.25` sentence is exactly right
(Hyprland-Parser.cpp:203-206); the grammar sentence is not.

Same class, same gate: a **CRLF** config (`\r` survives `strip(" \t")`) makes every line `unsupported`
(R14: `verdict=NOT_COMPARED`) while hyprutils' `trim` removes `\r` (hyprutils-String.cpp:5-30). A config
written on Windows therefore yields no verdict at all.

### D-I — a malformed or valid `modeline` is not modelled, only labelled

`parseModeLine` requires at least 10 tokens and numeric fields (Hyprland-Parser.cpp:14-26); on failure
the mode falls through to the `stoi` path and the rule is added with resolution `0x0`/preferred
(Hyprland-Parser.cpp:111-120). The tool accepts any first token `modeline` and never checks the payload,
so `monitor = X, modeline` is reported as `mode=modeline` although Hyprland stores a preferred-mode rule.
Verdicts coincide only because neither side compares a modeline/preferred mode; the rule line differs.
A **valid** modeline's mode is likewise never compared (declared: "explicit W x H only"). Documented
limit, cosmetic in the rule text.

---

## 3. Documented limits whose disclosure is incomplete

1. **`debug:disable_scale_checks`** (Hyprland-Monitor.cpp:721, :997). The docstring's correction rule is
   unconditional; with the option set Hyprland applies the raw scale and every corrected expectation the
   tool computes becomes a false DIFFER (and it combines with D-A). Say "unless `debug:disable_scale_checks`".
2. **wlr-output-management override** (Hyprland-MonitorRuleManager.cpp:44-80). `get()` mutates the returned
   rule (enabled, mode, offset, transform, scale, adaptive sync) before applying it. The docstring's
   DIFFER causes list covers this, and the resulting DIFFER is honest ("the rule is not what runs"), so
   **no verdict defect** — but the rule the tool prints is no longer the rule Hyprland applied, which the
   report format cannot show.
3. **`hyprctl monitors -j` vs `monitors all -j`** (Hyprland-HyprCtl.cpp:321-339). `all` iterates
   `allMonitors()`, the plain form `monitors()`. A disabled output is absent from the plain dump, so a
   `disable` rule produces no `MADO_MON_OUTPUT` line and no DISABLED verdict; the top verdict is still OK
   (R16 vs R17). The contract's four verdicts include DISABLED, so the dump's coverage is a precondition
   the docstring only implies through its usage examples.
4. **vrr / bitdepth / cm / sdrsaturation / sdrbrightness / icc**. All eight keys are consumed, none is
   compared (`compare` checks mode, position, scale, transform, mirror only, mado-monitors.py:362-393), so
   `monitor = DP-1, ..., vrr, 1` against live `vrr: false` is AGREE. Declared only by omission; the docstring
   should list the keys that are *consumed but not compared*, and that `cm` is applied through `icc`
   precedence (Hyprland-Monitor.cpp:658-666).
5. **the hardcoded fallback rule.** When no rule matches and no empty selector exists, `get()` returns a
   hardcoded rule (auto-right, resolution 0x0, scale -1; Hyprland-MonitorRuleManager.cpp:108-115), so an
   output Hyprland calls UNRULED is still driven by a rule. The tool's UNRULED is a statement about config
   only; the docstring never says so, and a config whose only line is `badrules` reaches
   NO_MATCHING_MONITOR/UNRULED where Hyprland applies its fallback.
6. **`addreserved` on an existing rule mutates the rule's reserved area**
   (Hyprland-legacy-ConfigManager.cpp:1330-1334). The docstring's "nothing changes" describes the tool's
   output, not Hyprland's state; no verdict effect (the reserved area is never compared).

---

## 4. What the docstring states correctly (checked, so the review is not one-sided)

| claim | locator |
|---|---|
| one rule per selector; re-adding erases earlier ones and appends | Hyprland-MonitorRuleManager.cpp:38-42 |
| the last matching rule wins, else the first empty selector | Hyprland-MonitorRuleManager.cpp:96-108 |
| `desc:TEXT` matches the description prefix, trimmed | Hyprland-Monitor.cpp:1201-1211 |
| the JSON `description` is the **short** description (make, model, serial); Hyprland also tests the long one | Hyprland-Monitor.cpp:250-256, Hyprland-HyprCtl.cpp:277 |
| no `@RATE` → 60 Hz | Hyprland-MonitorRule.hpp:46 |
| `pref*`, `highrr`, `highres`, `maxwidth`, `modeline` (case-insensitive keyword) | Hyprland-Parser.cpp:111-120, 14-26 |
| scale `K = round(S*120)`, `K/120` first, then `(K+i)/120`, `(K-i)/120`, `i = 1..89` | Hyprland-Monitor.cpp:1001-1026 |
| scale `< 0.25` becomes 1.0 and the line errors | Hyprland-Parser.cpp:197-206 |
| mode closeness `< 1` used for a requested mode | Hyprland-Monitor.cpp:835-837 |
| explicit positions are applied literally | Hyprland-MonitorPositionController.cpp:24-33 (`moveTo(*POS)`) |
| an unknown KEY drops the rule ("invalid syntax" before the add) | Hyprland-legacy-ConfigManager.cpp:1378 vs :1384 |
| `mirrorOf` is the decimal id of the target, else `"none"` | Hyprland-HyprCtl.cpp:286 |
| `disabled` is `!m_enabled` | Hyprland-HyprCtl.cpp:285 |
| the transform modifier copies the existing rule | Hyprland-legacy-ConfigManager.cpp:1303-1316 |

---

## 5. Impact on the frozen claim

The counter `c1-r45-monitors.py` scores the **reference** as its 49 fixtures' oracle: every fixture
encodes the double-precision scale model (D-A), the single-digit transform grammar (D-B), the
regex-bound `addreserved` (D-C) and the "no divisor → skip" rule (D-E). So 49/49 TARGET_MET does not
clear these four divergences; the fixtures are the contract's cases, not Hyprland's runtime
(registration's own residual). The claim can still land — the tool is a *model* and its docstring is
the contract — but two statements in the frozen reference are false about the cited source
(*the `E = S` test*, *the one-digit transform*), and one silently converts a guaranteed mismatch into
AGREE (D-E). Severity ranking for a re-registration decision: **D-A and D-B (wrong verdict on ordinary
input), then D-E (false AGREE), then D-C, then D-L [INFERENCE]**.

## 6. What this review did not establish

- The `Query`/`CMonitorState` implementation behind `configString` is not in `fetch/`, so D-L is
  conditional; the pin shows only that the target is not found by name equality.
- `Vector2D`'s scalar `operator/` precision is not pinned; the D-A direction "Hyprland corrects, tool
  keeps" therefore depends on it. The reported D-A direction (Hyprland keeps, tool corrects) does not:
  either division variant stores a `Vector2D` (float) before the comparison at :997.
- No host run: the live dump was not needed for any finding (the AGREE/DISABLED/DIFFER shape is
  reproduced from synthetic dumps), so nothing here is a claim about the host's current state.
