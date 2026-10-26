# ExecParseOracle — differential test of the monitor-line parser

Round 45, w1 (hyaku run 9). Lane `mado-shokunin`. Claim under test: C1's reference tool
`.ufo/waves/round-45/l1-draft/mado-monitors.py` (sha256 `c6ac5fc2…726be`), whose docstring is the
contract. This seat did **not** score the counter and did not touch a frozen file: it built an
independent model of Hyprland's own line handling and diffed the two.

## Result

Four ways in which the tool's model of `handleMonitor` differs from the pinned C++, all reachable from
`monitor =` lines the tool **models** (no `unsupported` excuse):

| class | what the tool gets wrong | minimal repro | modelled corpus |
|---|---|---|---|
| **A** | `addreserved` numbers: the tool demands `-?[0-9]{1,6}`; Hyprland uses `std::stoi` prefix parsing, so `+5`, `1.5`, `0x10`, `10abc` are **accepted** and a rule is added | `monitor=DP-1, addreserved, 10abc, 0, 0, 0` → tool: `rules=0`; Hyprland: 1 rule | 305 / 400 divergences |
| **M** | `modeline`: the tool labels any first token `modeline` as `mode=modeline` and never compares it; Hyprland validates it (≥10 args, 9 numbers) and turns it into an **explicit** resolution + rate, or falls through to `(0,0)` = preferred | `monitor = DP-1, modeline 419.00 3440` → tool: `mode=modeline`; Hyprland: preferred | 88 / 400 |
| **T** | field-1 `transform`: the tool requires exactly one digit; `isNumber` + `std::stoi` accept `03`/`007` and apply that transform | two lines, second `monitor = DP-1, transform, 03` → tool: `badrules`, transform stays 0; Hyprland: transform 3 | 2 / 400 |
| **W** | field trimming: the tool strips `" \t"`; Hyprland trims with `std::isspace`, so a CRLF config's `\r` reaches the tool's selector/keys/values | `monitor=DP-1\r\n` → tool selector `"DP-1\r"`, output UNRULED; Hyprland: `DP-1` | 5 / 400 |

Zero divergences remain unexplained (`classes.py` reports `U = 0` on both corpora: 400 of 3600 `modelled`
configs diverge, classed A 305 / M 88 / T 2 / W 5), and a control corpus built only from forms both sides
accept agrees **3600/3600** with no `unsupported` at all.

Two further findings sit outside the rule list (they change verdicts, not rules): `0x0` is read as the
preferred-mode sentinel by `applyMonitorRule`, and a valid `modeline` gives a mode the tool never compares
— so the tool can print `OK` for an output that does not run the mode its rule names.

Two hazards **in the pinned upstream code**, not in the tool, fell out of the same work: `CVarList2`
invalidates its own argument views when a line has two or more escaped fields, and `parseTransform`'s
`std::stoi` is unguarded against `out_of_range`.

## What was modelled, and from where

`model.py` transcribes, field for field:

* the splitter: `CVarList2(std::string(args))` (legacy ConfigManager.cpp:1295), whose `construct()` trims
  each field with `hyprutils::String::trim` (`std::isspace`) and whose escape rule looks two characters
  back (`pins/src_string_VarList2.cpp:41`, `:67`);
* the line layer: `hyprlang` trims the line and the RHS (`.ufo/…/pins/hyprlang-v0.6.8-src-config.cpp:672`,
  `:723`), strips `#` comments but turns `##` into a literal `#` (`:691`, `:701`), joins backslash
  continuations (`:53`), and dispatches the *unscoped* `monitor` handler even inside a block (`:844`, `:866`);
* `handleMonitor`: the `disable|disabled|addreserved|transform` branch (ConfigManager.cpp:1299), the
  `std::stoi` area parse (`:1323`), the unconditional add (`:1341`), the key loop
  `while (!ARGS[argno].empty())` (`:1351`) that aborts without adding on an unknown key and *ignores* a bad
  value (Parser.cpp:219 is not wrapped in a try, the loop's `parseTransform` return is dropped);
* `CMonitorRuleParser`: `parseMode` (preferred/highrr/highres/maxwidth ranking, then `parseModeLine` with
  its 10-argument gate at Parser.cpp:23, then `stoi`-prefix `WxH[@R]` with the rate as `stof` → float32,
  `m_refreshRate` staying 60 when the rule has no `@` — MonitorRule.hpp:46), `parsePosition`,
  `parseScale` (`isNumber` requires a whole number; `< 0.25` becomes 1), `parseTransform`;
* the manager: erase-then-append per selector (MonitorRuleManager.cpp:38), reverse scan then first empty
  selector (`:97`), `matchesStaticSelector` matching `desc:` against the long **or** short description
  (Monitor.cpp:1206).

`splitcheck.py` compiles the pinned `VarList2.cpp` + `String.cpp` against a driver and feeds both the same
4000 random strings: **3397 compared, 0 mismatches** (`receipts/splitcheck.txt`). The model's riskiest
transcription is therefore checked against the C++, not asserted.

## Method

* `diff.py` generates config files from three pools (selector, mode, position, scale, key, modifier,
  comment, line ending), runs the tool **in process** (`importlib` → `report()`, so the tool's own parser
  and printer run), parses its printed `MADO_MON_RULE`/`MADO_MON_OUTPUT` lines back, and compares against
  the model's rule list and `get()` assignment per synthetic output. Comparison is on
  (selector, disabled, resolution, rate, offset, scale, transform, mirror) — the fields the tool prints.
* Three corpora, 3600 configs each, seed 45: `stress` (adversarial pool), `modelled` (only forms the tool
  models), `clean` (control: also drops the four classes above).
* `minimize.py` drops lines while a divergence persists, so every class is reported with a minimal repro.
* `directed.py` runs 15 hand cases: 10 divergences and 5 positive controls.
* `receipts/host-anchor.txt` runs both on this host's real `~/.config/hypr/monitors.conf` and a
  shape-only projection of `hyprctl monitors all -j` (id/name/size/rate/pos/scale/transform/disabled/
  mirrorOf; no serial or description): both produce one rule `DP-1 3440x1440@100 0x0 1.0000 0` and assign
  it to `DP-1`.

### Corpora

| profile | configs | monitor lines | agree | diverged, tool comparing | diverged but tool said NOT_COMPARED | tool `unsupported` share |
|---|---|---|---|---|---|---|
| stress | 3600 | 5275 | 2624 | 202 | 774 | 2927 lines = **55.49 %** |
| modelled | 3600 | 5456 | 3087 | 400 | 113 | 115 lines = **2.11 %** |
| clean (control) | 3600 | 5336 | 3600 | 0 | 0 | **0 %** |

The 55 % is a property of the adversarial pool (half its constructs are deliberately forms the tool
declines), not of the tool. The 2.11 % of the `modelled` corpus is two causes, measured line by line:
112 of the 115 are the deliberately included key `transform` with **no value** at the end of the line, and
the rest are CRLF lines whose last field the tool cannot parse (`receipts/run-modelled/diverge.txt`).

The per-construct table (`receipts/run-modelled/families.txt`, 159 rows, one construct per line) names the
11 constructs that diverge while the tool is still comparing, and the 18 it declines.

Class shares below are of the 400 `modelled`-corpus divergences (`receipts/run-modelled/classes.txt`).

## Class A — `addreserved` numbers are `std::stoi`, not a fullmatch

The tool's contract says:

> `- field 1 `addreserved`: fields 2-5 must each fullmatch `-?[0-9]{1,6}`, else `badrules`. If a rule with`
> — mado-monitors.py:41, enforced at `:259`

Hyprland does:

> `area = {std::stoi(std::string{ARGS[2]}), std::stoi(std::string{ARGS[5]}), std::stoi(std::string{ARGS[3]}), std::stoi(std::string{ARGS[4]})};`
> — ConfigManager.cpp:1323, then `add` at `:1341`

`std::stoi` takes a sign and stops at the first non-digit, so `+5` → 5, `1.5` → 1, `0x10` → 0, `10abc` → 10
all parse and the rule is added (a default rule when the selector has none, otherwise the existing rule's
area is overwritten — the drop of the parsed area on the add path is Hyprland's own quirk, and the tool
models it correctly). `99999999999` overflows → both reject. Consequences: the tool reports
`NO_MATCHING_MONITOR` where Hyprland has a rule, and after a `disable` line the tool reports the output
UNRULED while Hyprland keeps it DISABLED.

Minimal repro (from `receipts/run-modelled/minimal.txt`):

```
monitor=DP-1, addreserved, 10abc, 0, 0, 0
tool:   MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=0 badrules=1 … verdict=NO_MATCHING_MONITOR
model:  1 rule  ("DP-1", preferred, auto, auto, transform 0)
```

## Class M — `modeline` is resolved by Hyprland, never by the tool

> `highrr`, `highres`, `maxwidth` is that keyword; a first token `modeline` (any case) is modeline; else it`
> — mado-monitors.py:48, implemented at `:194`

Hyprland runs `parseModeLine` first (10-argument gate at Parser.cpp:23), and on success stores the mode:

> `m_rule.m_refreshRate = sc<float>(m_rule.m_drmMode.vrefresh) / 1000;`
> — Parser.cpp:121

so a rule with a valid modeline is an **explicit** resolution and the output should be compared against it.
The tool prints `mode=modeline` and, because `:370` compares only `mode == "explicit"`, skips the mode
check entirely. On a malformed modeline (fewer than 10 tokens) Hyprland falls through to the `WxH` branch,
which for a modeline string has no `x` and ends at `(0,0)` — preferred — while the tool still says
`modeline`. Two minimal repros:

```
monitor = DP-1, modeline 419.00 3440 3448 3520 3680 1440 1443 1448 1481 +hsync -vsync
tool:   MADO_MON_RULE: … mode=modeline …   MADO_MON_OUTPUT: … differ=- verdict=AGREE   (live 3440x1440@99.997)
model:  resolution (3440,1440), rate 76.879  → the live mode is not the mode this rule names
```

```
monitor = DP-1, modeline 419.00 3440
tool:   MADO_MON_RULE: … mode=modeline …        (nothing compared)
model:  resolution (0,0) = preferred → the tool's rule line describes the rule wrongly
```

Verdict-plane effect: for a valid modeline the tool can print `OK` for an output that is not running the
mode the rule specifies (`receipts/directed.txt`, V2). Rule-list effect: `mode=modeline` is printed for
rules Hyprland holds as `(0,0)` or as a real `WxH@R`.

## Class T — field-1 `transform` accepts leading zeros

> `- field 1 `transform`: field 2 must be one digit 0-7, else the line adds one to `badrules`. The first rule`
> — mado-monitors.py:38; the check is `:224`

Hyprland's gate is `isNumber`, which for one argument is hyprutils'
`bool             isNumber(const std::string& str, bool allowfloat = false);` (String.hpp:9), then

> `const auto TSF = std::stoi(value);`
> — Parser.cpp:219

`isNumber("03")` is true (all digits, ends in a digit) and `stoi("03")` is 3, so the existing rule is
copied with transform 3 and re-added. The tool calls `03` and `007` invalid and changes nothing. (`3.0` and
`+3` are *rejected* by `isNumber`, so the tool is right about those — the divergence is only the
leading-zero form.) Needs an earlier rule for the same selector, which is why it is rare in random
corpora (2 of 390) and obvious in one:

```
monitor = DP-1, 1920x1080, 0x0, 1
monitor = DP-1, transform, 03
tool:   transform=0   badrules=1
model:  transform=3
```

## Class W — "spaces and tabs" is not `std::isspace`

> `modelled; else it is cut at its first `#`, split on ",", and each field is stripped of spaces and tabs;`
> — mado-monitors.py:35 (the line-level claim is at `:32`)

Hyprland trims with `std::isspace` in three places — hyprlang's line (`:672`) and RHS (`:723`), and every
split field (`pins/src_string_VarList2.cpp:67` → `trim`, whose first loop is
`while (countBefore < in.length() && std::isspace(in.at(countBefore))) {`). A CRLF config therefore leaves
no `\r` anywhere; the tool strips only `" \t"`, so the `\r` survives into whichever field ends the line.
Four observed shapes (`receipts/run-modelled/minimal.txt`, `receipts/run-stress/diverge.txt`):

| config | tool | model |
|---|---|---|
| `monitor=DP-1\r` | rule with selector `"DP-1\r"` → output UNRULED | selector `DP-1` |
| `monitor = desc: Samsung\r` | selector `"desc: Samsung\r"` → matches nothing | `desc: Samsung` |
| `…, mirror , transform 2\r` | mirror value `"transform 2\r"` | `transform 2` |
| `…, 0x0, 1\r` | scale `"1\r"` fails the fullmatch → `unsupported` (file NOT_COMPARED) | scale 1 |

The last row is the benign direction (the tool refuses rather than answers), the first three are silently
wrong answers on a file the tool reports as fully compared.

## Verdict-plane divergences (rule lists identical)

* **`0x0` is the preferred sentinel.** `parseMode` stores `(0,0)` for `0x0`, exactly as for `preferred`, and
  `applyMonitorRule` branches on it:
  `if (RULE->m_resolution == Vector2D()) {` (Monitor.cpp:773) → preferred mode. The tool compares
  `width == 0` and `height == 0`, so for any real output it must print `differ=mode`:

  ```
  monitor = DP-1, 0x0, 0x0, 1     (live DP-1 3440x1440@99.997)
  tool: differ=mode verdict=DIFFER      Hyprland: preferred mode → the rule is satisfied
  ```

  The rule *fields* agree (`(0,0)`, rate 60), so no rule-list class catches this; it is a false `DIFFER`.
* **Valid `modeline`** — covered above: a false `AGREE` (`OK`) for a rule naming a mode the output is not
  running.
* **`desc:` against the long description** — declared in the tool's docstring and reproduced by V3:
  Hyprland matches the long **or** the short description (Monitor.cpp:1206), the dump carries only the
  short one (the `"description"` field at HyprCtl.cpp:234 is fed `m_shortDescription` at `:277`), so a
  `desc:` selector that matches only the EDID long text reports UNRULED.
  Declared, therefore not a contract bug.
* **`source =` trees** are read by neither side: a config that pulls monitor rules from a third file is
  compared against an incomplete rule list without any `unsupported` signal. Not a parser divergence (no
  `monitor` line is involved) but the same class of silent wrong answer; mentioned because the host's
  `hyprland.conf` uses `source`.

## Checked, no divergence (so the diff has teeth)

Positive controls and the mechanisms behind them: newest-match and the erase+append that produces it
(MonitorRuleManager.cpp:38, `:97`); empty-selector fallback and the fact that an empty selector never
matches by name; `disable`/`disabled`; a valid `addreserved` with and without an existing rule; a valid
single-digit `transform` modifier (including its re-ordering to the end of the list); `desc:` prefix
matching; `scale 0.2 → 1`; `preferred`/`pref`; `highrr`/`highres`/`maxwidth`; empty bodies; missing fields;
a key whose value is missing (`mirror`); unknown keys (both drop the rule); duplicate selectors; `#`
comments; unknown `auto` directions; `monitor =` inside a block (hyprlang calls the unscoped handler
regardless of category depth — `:844`, `:866`, so the tool's nesting-blind walk is right).

## Gaps where the tool declines (masking, not wrongness)

113 of 3600 `modelled` configs and 774 of 3600 `stress` configs are `NOT_COMPARED` because of one line. The
largest single cause, 109 of the 113 masked configs, is a key with no value,
e.g. a trailing `…, 1, transform`: Hyprland returns a parse error **and still adds the rule** (the key loop
drops the return value of the `transform` arm, so `m_transform` keeps its default 0), while the tool's
`unsupported` discards the line and the file's verdict. Also:

* `$` and `##` are tested on the raw body (`:230`) **before** the comment is cut (`:233`), so
  `…, 1 # $x` — which hyprlang reduces to a clean value — is declined;
* `##` is not just a comment: hyprlang removes one `#` and keeps a literal `#` in the value (`:691`, `:701`),
  so the tool's refusal is the safe choice but the construct is modellable.

Conservatism, not a bug — but it means a five-line file with one odd line loses comparison for all its
rules.

## Hazards in the pinned upstream code (found while grounding the model)

* **`CVarList2` invalidates its own views.** `m_args` holds `string_view`s into `m_copyStrings`
  (`pins/src_string_VarList2.cpp:77`); a *second* escaped field reallocates that vector and the earlier
  views dangle. Demonstrated (`receipts/varlist-ub.txt`):
  `a\,b, c\,d, 0x0, 1` → `size=4 : [] [c,d] [0x0] [1]` — the selector silently became empty. Any
  `monitor =` line with two escaped commas mis-parses field 0. The tool's blanket "any backslash is
  unsupported" is, accidentally, the safest possible treatment of this.
* **`parseTransform`'s `std::stoi` is unguarded.** `transform, 99999999999` passes `isNumber` and throws
  `out_of_range` out of `handleMonitor`; nothing in the pinned handler or `parseLine` catches it. The model
  records these as escapes (79 in the `modelled` corpus, from the deliberately impossible values in the
  pool); the tool's `badrules` predicts "no rule", which is the same *outcome* for the rule list while
  hiding the crash path.

## What this means for C1 (data, not a ruling)

`PRED-C1-r45`'s fixtures contain none of these four forms: its transform fixtures use `transform, 1`,
`transform, 3` and `transform, 9` (counter `:125`, `:133`, `:137`, `:139`), its addreserved fixtures use
`addreserved, 10, 0, 0, 0` (`:212`, `:214`), and `grep -n -e modeline -e 'transform, 0' -e '\r'` over the
counter matches nothing (`receipts/counter-coverage.txt`). The 33 selftest cases likewise contain one
`addreserved` case with a plain decimal (mado-monitors.py:487), one single-digit `transform` modifier, and
no modeline or CRLF case. Nothing here contradicts the counter's clauses — it reads a tool present, a
selftest N/N and 49 fixtures — but a green counter does not mean the contract matches Hyprland.

The edits a v2 of the tool would need, none of them applied by this seat:

1. trim fields (and the line) with `std::isspace`, not `" \t"` — fixes class W and the CRLF `unsupported`;
2. accept `std::stoi`'s prefix grammar for `addreserved` fields (sign, digits, trailing garbage, int range) —
   fixes A;
3. accept leading-zero integers for the field-1 `transform` (`isNumber` then `stoi`, clamp 0..7) — fixes T;
4. either parse a modeline (≥10 space-separated tokens, 9 numbers) into `WxH@rate` and compare it, or count
   it `unsupported` — the current `mode=modeline` + skip is a false `OK`; a malformed modeline is
   `preferred`, not `modeline`;
5. read `0x0` as the preferred sentinel (`Monitor.cpp:773`), in parse and in compare;
6. cut the comment before testing for `$`/`##`/backslash.

## Limits

* The model is a transcription, not a build: Hyprland was never compiled here, `applyMonitorRule` was read
  (`Monitor.cpp:719-880`, `:960-1075`) but is modelled only where a comparison depends on it (the `(0,0)`
  sentinel). `CMonitor` state, mode enumeration and the wlr-output-management override
  (`MonitorRuleManager.cpp:39-67`) are out of scope.
* hyprlang is pinned to v0.6.8 (latest tag), not to the host's build; every hyprlang statement above is in
  the parts identical in `main` and `v0.6.8`.
* Synthetic monitor dumps: no compositor was mutated, no Wayland client was started; the only host read is
  the shape-only projection in `receipts/host-anchor.txt`.
* Generators are seeded (45) and the receipts are the raw output; run the commands below to reproduce.
* Whether these classes matter enough to re-register C1 is the L1's call, not this seat's.

## Reproduction

```
cd .ufo/waves/round-45/w1/ExecParseOracle
python3 model.py <config> <monitors.json>       # model alone
python3 splitcheck.py                          # pinned CVarList2 vs model.varlist2
python3 diff.py --profile modelled --out receipts/run-modelled
python3 diff.py --profile stress   --out receipts/run-stress
python3 diff.py --profile clean    --out receipts/run-clean
python3 minimize.py --profile modelled --out receipts/run-modelled
python3 classes.py  --profile modelled --out receipts/run-modelled
python3 directed.py                            # 15 directed cases
python3 quotes.py                              # every citation in this file, line-addressed
```

## Files in this seat

`report.md` (this), `../ExecParseOracle.md` (the scoped report), `model.py`, `diff.py`, `minimize.py`,
`classes.py`, `directed.py`, `splitcheck.py`, `quotes.py`, `pins/` (fetched sources + `SHA256SUMS.txt` +
`PINS.md` + the two drivers), `receipts/` (`splitcheck.txt`, `varlist-ub.txt`, `quotes.txt`,
`counter-coverage.txt`, `host-anchor.txt`, `directed.txt`, `run-{modelled,stress,clean}/` with
`summary.json`, `diverge.txt`, `families.txt`, `minimal.txt`, `classes.txt`).
