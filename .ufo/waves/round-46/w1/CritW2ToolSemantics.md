# CritW2ToolSemantics — round-46 w1 (the round-45 w2 falsification, run late)

Subject: `tools/mado-monitors.py` at tip `4d22eeb66c2835af8aaa3fac6ad838fa616aa663` (landed `ee6659b`), sha256
`2f007417…ff5609`; selftest 48/48. Judged against the round-45 pins, plus the round-46 pins of the same commit
(`efb50993`) for the `monitorv2` plane. Full detail: `.ufo/waves/round-46/w1/CritW2ToolSemantics/report.md`.
Receipts: `.ufo/waves/round-46/w1/CritW2ToolSemantics/receipts/` (hashes in `SHA256SUMS`; 28 quote checks, 0 fail).

## Verdict

The six semantics w1 left unexamined split cleanly: **reserved areas, `desc:` padding, transform-on-mirror-line and
the disabled/re-enabled plane are faithful**; **`monitorv2` carries a defect that defeats the tool's own gate**;
**mirror resolution and `source` includes are undeclared model gaps**. w1's four findings are fixed in the landed
blob (float32 scale rule, `transform, 07`, `addreserved` stoi prefixes, no-divisor scale → `UNPREDICTED`).

## F1 — defect, high: `monitorv2[KEY] { … }` is not counted as a monitorv2 block

Same rule, same dump, two spellings (`receipts/control-keyed-vs-bracket.txt`):

| config | tool |
|---|---|
| `monitorv2 {` / `output = DP-1` / `mode = 3440x1440@100` | `v2=1 … verdict=NOT_COMPARED`, rc 5 |
| `monitorv2[DP-1] {` / `mode = 3440x1440@100` | `v2=0 … differ=mode verdict=DIFFER`, rc 1 |

* The bracket form is a real monitorv2 block: hyprlang 0.6.8 (`libhyprlang.so.2`, compiled probe
  `receipts/hyprlang-probe.{cpp,txt}`) returns key `DP-1`, `mode` `setByUser=1`, identical to the keyed form;
  mechanism `hyprlang-config.cpp:291`; the spelling is documented for the same kind of category at
  `wiki-Keywords.md:121` (`keyword device[my-device]:sensitivity -1`).
* `monitorv2` is a keyed special category (`Hyprland-ConfigManager.cpp:567`), its rules go into the same manager
  (`:876`, `:883`) **after** the whole parse (`:743` then `:747`), and `add` erases same-selector rules
  (`MonitorRuleManager.cpp:37-42`) — so v2 always supersedes a same-selector `monitor =` line.
* The tool's docstring promises `NOT_COMPARED (exit 5, v2 > 0…)` (`tools/mado-monitors.py:100`) but
  `V2_RE = monitorv2(?:[ \t={]|$)` (`:116`) misses `[`. It then reports on the superseded rule: false `OK` when that rule is `preferred/auto/auto`
  (`control-keyed-vs-bracket.txt`, third block, rc 0) or false `differ=<field>` DIFFER when it is explicit
  (`cases.txt` R1a, `cases2.txt` R7b);
  with `disabled = 1` inside the bracket block and a live disabled output it still prints `differ=disabled`, rc 1
  (`cases.txt` R1b).
* The frozen counter cannot see it: `quality/counters/c1-r45-monitors-v2.py` emits v2 only in the keyed form
  (`:229`, `:99`); `monitorv2[` appears in neither round-45 nor round-46 counter.
* **Smallest safe correction:** `V2_RE = re.compile(r"monitorv2(?:[ \t={\[]|$)")` (or count any first token that
  starts with `monitorv2`), plus one fixture per spelling.

## F2 — model gap, medium: mirror target resolution and refusals are not modelled

* Self-mirror (`mirror, DP-2` on DP-2) → `differ=mirror` DIFFER, rc 1 (`cases2.txt` R3e), but Hyprland refuses by
  design: `"Cannot mirror self!"` (`Monitor.cpp:1346`); a mirror-of-a-mirror is refused at `:1341`. Reachable live
  state is always `"none"`, so the tool prints a permanent DIFFER for a config the compositor tolerates (its
  DIFFER-cause list, docstring `:17-19`, lists neither refusal).
* `mirror, desc:Dell Inc.` with the host mirroring → `differ=mirror` DIFFER (`R3g`); the compositor resolves the
  target through the monitor query `configString(mirrorOf)` (`Monitor.cpp:1335`), the tool through dump-name
  equality (`tools/mado-monitors.py:422`). [INFERENCE] the query grammar is not pinned; the query-vs-`==` fact is.
* Inference flagged, not scored: `setMirror` overwrites the mirror's position with the source's (`:1386`), so an
  explicit position on a mirror rule may be compared against a replaced coordinate (`MonitorLayoutController` is not
  pinned, so whether `arrange()` restores it is open).
* **Correction:** resolve `desc:` targets / route non-name mirror values to `NOT_COMPARED`, and state the two
  refusals in the docstring.

## F3 — declaration gap, medium-low: `source =` includes are invisible

A config holding only `source = monitors.conf` prints `lines=0 … verdict=NO_RULES`, rc 4 (`cases2.txt` R7a) although
Hyprland follows the include (`source` handler registered, `Hyprland-ConfigManager.cpp:614`) and the wiki's own layout
puts `monitor =` lines in a sourced file. The "Lines." section (`tools/mado-monitors.py:36`) never mentions `source`.
**Correction:** count `source` lines into `sources=<n>` and emit `NOT_COMPARED` when `sources>0` and no rules were
seen, or state "includes are not followed" in the docstring.

## Attacks that found nothing (support the contract)

| # | Semantic | Case | Pin that settles it |
|---|---|---|---|
| N1 | `desc:` padded with spaces / tab / VT | R2a-c, all `AGREE` | `trim()` = `std::isspace` (`Monitor.cpp:1204`, `hyprutils-String.cpp:11`); tool's `WS` set matches. |
| N2 | transform on a mirror line, incl. `transform, 07` | R3a, R3b correct | `isNumber`+`stoi`+clamp (`Parser.cpp:214-221`). |
| N3 | reserved areas: default rule, present rule, stoi prefixes, short and long field lists | R5a-d, R8b faithful | `legacy-ConfigManager.cpp:1323`, `:1341`; defaults `MonitorRule.hpp:41-46`. |
| N4 | disabled output, runtime re-enable | R4a/b correct | JSON `disabled` = `!m_enabled` (`Hyprland-HyprCtl.cpp:285`); `ensureMonitorStatus` → `onDisconnect/onConnect` (`MonitorRuleManager.cpp:186`). |
| N5 | `auto-left` / `auto-right` | R6a/b: not compared, as declared | parse `Parser.cpp:146-171`; live value computable (`MonitorPositionController.cpp:68`) — capability gap, and the headline/`Not compared` list (`:1`, `:20`) overstate it. |
| N6 | `monitor =` inside another block | probe case 1: handler fires | hyprlang dispatches unscoped handlers regardless of category (`hyprlang-config.cpp:838-875`) — the tool's block-blind scanner is right. |

## Ledger-facing notes

* Round-45 C1 operability: F1 (verdict plane), F2/F3 (model/declaration). No new pin needed; all locators are in the
  frozen fetch sets.
* `c1-r45-monitors-v2.py`: no fixture can express F1, none carries a `desc:` mirror or a self-mirror — green is not
  correctness here.
* `corpus/knowledge/hyprland-monitor-rule-r45.md`: not contradicted (`:105` already limits its v2 claim); no row
  edit needed.

## Tool / host state

No install, no package transaction, no PATH write, no compositor command, no Wayland client, no host config read
outside the pins. `g++` (existing) compiled one throwaway probe against the installed `hyprlang` 0.6.8 headers inside
scratch; the probe source is kept in `receipts/`. Scratch removed after the receipts were copied.

Report: .ufo/waves/round-46/w1/CritW2ToolSemantics.md
