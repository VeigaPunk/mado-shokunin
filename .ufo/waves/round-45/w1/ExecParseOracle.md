# ExecParseOracle — findings (round 45 w1)

Differential test of the reference tool `.ufo/waves/round-45/l1-draft/mado-monitors.py`
(sha256 `c6ac5fc2…726be`) against a model of Hyprland 0.56.2 (efb50993): `handleMonitor`
(legacy ConfigManager.cpp:1293-1387), `CMonitorRuleParser` (Parser.cpp), `MonitorRuleManager::add/get`
(:37-117), `matchesStaticSelector` (Monitor.cpp:1201-1211), the hyprutils `CVarList2` splitter (v0.14.2,
pinned by me) and hyprlang's line/comment layer (v0.6.8). Full write-up + reproduction commands:
`.ufo/waves/round-45/w1/ExecParseOracle/report.md`. Raw output: `w1/ExecParseOracle/receipts/`.

## Contract bugs: four, all on lines the tool models (no `unsupported` excuse)

| # | tool's claim (locator) | Hyprland (locator) | minimal repro | share of 390 divergences |
|---|---|---|---|---|
| A | `addreserved` fields must fullmatch `-?[0-9]{1,6}` (`:41`, `:259`) | `std::stoi` prefix parse (ConfigManager.cpp:1323) then add (`:1341`): `+5`, `1.5`, `0x10`, `10abc` are accepted | `monitor=DP-1, addreserved, 10abc, 0, 0, 0` → tool `rules=0`; Hyprland 1 rule | 305 (76.2 %) |
| M | any first token `modeline` is `mode=modeline` and is never compared (`:48`, `:194`, `:370`) | `parseModeLine` validates (10 args, Parser.cpp:23) and stores an explicit resolution + `vrefresh/1000` (`:121`); a malformed one falls through to `(0,0)` = preferred | `monitor = DP-1, modeline 419.00 3440` → tool `modeline`; Hyprland preferred | 88 (22.0 %) |
| T | field-1 `transform` must be exactly one digit 0-7 (`:38`, `:224`) | `isNumber` (String.hpp:9, `allowfloat=false`) + `std::stoi` (Parser.cpp:219) accept `03`/`007` → transform applied | 2-line: `…, 0x0, 1` then `monitor = DP-1, transform, 03` → tool keeps 0, Hyprland sets 3 | 2 (0.5 %) |
| W | lines/fields stripped of `" \t"` only (`:32`, `:35`) | `std::isspace` trim (hyprlang:672, `:723`; VarList2.cpp:67) | `monitor=DP-1\r\n` → tool rule `sel="DP-1\r"` → UNRULED; Hyprland `DP-1` | 5 (1.2 %) |

`classes.py` leaves **0 unexplained** divergences on both corpora (400 of 3600 `modelled` configs).

## Verdict-plane findings (rule lists identical, answers differ)

* **`0x0` is the preferred sentinel**: `applyMonitorRule` branches on `m_resolution == Vector2D()`
  (Monitor.cpp:773), the tool compares `width==0 && height==0` → a false `DIFFER` on every real output.
* **A valid `modeline`** gives Hyprland an explicit mode; the tool skips the mode check → a false `OK`
  (`AGREE`) for an output that is not running the mode the rule names.
* `desc:` against the EDID long description: declared in the tool's docstring, reproduced (UNRULED).

## Numbers

* 3600-config corpora, seed 45. `modelled` (only forms the tool models): 3087 agree, 400 divergences, 113
  masked, unsupported 115/5456 lines = 2.11 % (112 of those lines are the deliberately included key
  `transform` with no value). `stress` (adversarial pool): 2624 agree, 202 divergences, 774 masked,
  unsupported 2927/5275 lines = 55.49 %. `clean` control (the four classes removed): **3600/3600 agree, 0
  unsupported, 0 masked**.
* `receipts/run-modelled/families.txt`: one construct per line — 11 constructs diverge while the tool is
  comparing, 18 are declined.
* Grounding: `receipts/splitcheck.txt` — the model's CVarList2 transcription vs the compiled pinned C++:
  3397 compared, **0 mismatches**. `receipts/host-anchor.txt` — model and tool agree on this host's real
  `monitors.conf` + a shape-only live projection (1 rule, DP-1). `receipts/quotes.txt` — 40 citations,
  line-addressed, 0 failed.

## Upstream hazards (the pins, not the tool)

* `CVarList2` keeps `string_view`s into `m_copyStrings`; a second escaped field reallocates that vector and
  earlier views dangle. Demo: `a\,b, c\,d, 0x0, 1` → field 0 empty (`receipts/varlist-ub.txt`). The tool's
  blanket backslash-`unsupported` accidentally avoids this.
* `parseTransform`'s `std::stoi` is unguarded: `transform, 99999999999` passes `isNumber` and throws
  `out_of_range` out of `handleMonitor`.

## Relevance to C1 (data, not a ruling)

`PRED-C1-r45`'s fixtures contain none of the four forms: transform fixtures are `1`/`3`/`9`
(counter `:125`, `:133`, `:137`, `:139`), addreserved fixtures are `10, 0, 0, 0` (`:212`, `:214`), and
`grep -n -e modeline -e 'transform, 0' -e '\r'` over the counter matches nothing
(`receipts/counter-coverage.txt`). The 33 selftests have one plain `addreserved` case (`:487`) and one
single-digit transform, and no modeline or CRLF case. So the counter can stay green while the contract is
wrong in four places; a v2 would need the six edits listed in `report.md`.

## Risks / limits

Model is a transcription, not a build of Hyprland; `applyMonitorRule` is modelled only where a comparison
depends on it; hyprlang pinned to v0.6.8 (latest tag) rather than the host's build; synthetic dumps only —
no compositor mutation, no Wayland client, one read-only `hyprctl monitors all -j` projected to
id/name/size/rate/pos/scale/transform/disabled/mirrorOf. No frozen file was modified and the counter was not
run.

## Files

`w1/ExecParseOracle/{report.md, model.py, diff.py, minimize.py, classes.py, directed.py, splitcheck.py,
quotes.py, pins/ (5 upstream files + 2 drivers + SHA256SUMS.txt + PINS.md), receipts/}`. Scratch
`/fast/scratch/hyaku/mado-r45/ExecParseOracle/` deleted after the receipts were copied.
