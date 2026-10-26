# CritW2ToolSemantics — round-45 w2, run inside round-46 w1

Subject: the landed `tools/mado-monitors.py` (blob at tip `4d22eeb66c2835af8aaa3fac6ad838fa616aa663`, first landed
`ee6659b90f7bf69aa03283dba804dd90081b7ff5`; sha256 `2f007417…ff5609`, `receipts/tool-at-tip.py`), judged against the
round-45 pins (`round-45/fetch/`) and, for the `monitorv2` plane only, the round-46 pins of the same commit
`efb50993` (`round-46/fetch/`). Selftest on the extracted blob: `MADO_MONITORS_SELFTEST: 48/48 passed`, rc 0.

Scope of this attack: the six semantics w1 did not check (monitorv2 interplay, `desc:` with trailing spaces,
transform values on the mirror line, a disabled output re-enabled at runtime, reserved areas, `auto-left`
positions), plus whatever else the pins expose. Receipts: `receipts/{cases.txt,cases2.txt,hyprlang-probe.txt,
hyprlang-probe.cpp,quotes.txt,quote-check.sh,drive1.sh,drive2.sh,tool-at-tip.py,SHA256SUMS}`.

## Verdict

Two of the six areas are clean and one is clean but under-declared; **one carries a real defect that defeats the
tool's own top-verdict gate**, and two smaller model gaps sit on the mirror and `source` planes. The tool is
faithful everywhere w1's oracle already covered; nothing here re-opens w1's four findings (all four are fixed in
the landed blob: `transform, 07` parses, `addreserved` takes stoi prefixes, a no-divisor scale is `UNPREDICTED`
not `AGREE`, and the scale expectation is built from the float32 rule value).

---

## F1 (defect, high): the `monitorv2[KEY] { … }` spelling is not a monitorv2 block to the tool

**Counterexample.** Two configs with the same meaning, one dump:

```
a) monitor = DP-1, 1920x1080@60, 0x0, 1          b) monitor = DP-1, 1920x1080@60, 0x0, 1
   monitorv2 { output = DP-1 }                      monitorv2[DP-1] {
       mode = 3440x1440@100                             mode = 3440x1440@100
   }                                                  }
   live: DP-1 3440x1440@99.997, x0 y0, scale 1
```

* (b) → `v2=0 … verdict=DIFFER`, `differ=mode`, exit 1 (`receipts/cases.txt` R1a, `cases2.txt` R7b).
* (a) → `v2=1 … verdict=NOT_COMPARED`, exit 5. Both halves, one dump, one script:
  `receipts/control-keyed-vs-bracket.txt` (control `rc=5`, attack `rc=1`).
* Same with `disabled`: `monitorv2[DP-1] { disabled = 1 }` + legacy enabled rule + live `"disabled": true` →
  `differ=disabled verdict=DIFFER`, exit 1 (`cases.txt` R1b), while the config's own v2 rule says exactly what the
  host shows.

**Evidence that the bracket form is a real monitorv2 block.**
1. hyprlang 0.6.8 (host `libhyprlang.so.2`, compiled probe `receipts/hyprlang-probe.cpp`) parses
   `monitorv2[DP-1] { mode = 1920x1080@60 }` and returns key `DP-1` with `mode` `setByUser=1`
   (`receipts/hyprlang-probe.txt`, case 2) — byte-identical to the keyed form (case 3). The mechanism is
   `hyprlang-config.cpp:291` (`valueName.contains('[')` → CATKEY), and the bracket form is documented for the same
   kind of keyed category in `wiki-Keywords.md:121` (`keyword device[my-device]:sensitivity -1`).
2. `monitorv2` is registered as a keyed special category (`Hyprland-ConfigManager.cpp:567`,
   `{.key = "output"}`), and `handleMonitorv2()` iterates `listKeysForSpecialCategory("monitorv2")`
   (`:883`) and adds each rule to the **same** rule manager (`:876`).
3. Those rules are added **after** the whole config parse: `m_config->parse()` at `:743`, `handleMonitorv2()` at
   `:747`, and `CMonitorRuleManager::add` erases same-selector rules and appends (`MonitorRuleManager.cpp:37-42`).
   So a v2 rule always supersedes a same-selector `monitor =` rule, whatever the file order.

**The tool's own contract is violated.** Its docstring promises `NOT_COMPARED (exit 5, v2 > 0…)`
(`tools/mado-monitors.py:100`) — i.e. "a monitorv2 block" routes the run to exit 5 — but the counter is
`V2_RE = re.compile(r"monitorv2(?:[ \t={]|$)")` (`:116`), which needs `space`, `tab`, `=` or `{` after the name;
`monitorv2[` matches none of them. The tool then compares the *superseded* legacy rule and prints `OK` (when that
rule is `preferred/auto/auto`) or a `differ=<field>` DIFFER (when it is explicit) — a verdict with no counterpart in
the compositor.

**Why the frozen counter cannot see it.** `quality/counters/c1-r45-monitors-v2.py` emits v2 only in the keyed form
(`:229` `"monitorv2 {\n  output = %s\n}"`, and the one hand-written case `:99`); `grep -n "monitorv2\["` over both
round-45/46 counters is empty. 49/49 green, defect present.

**Impacted axes.** Operability (round-45 C1): the tool's printed verdict *is* the claim's after-state, so this is a
false DIFFER (exit 1) and a false OK (exit 0) on configs the host accepts and honours. Coverage: not contradicted —
the round-45 entry is honest that it does not trace v2 (`hyprland-monitor-rule-r45.md:105`) — but the C2 entry would
be wrong if it ever states the gate is exhaustive.

**Smallest safe correction (one line, no fixture churn):** extend the detector to the bracket form, e.g.
`V2_RE = re.compile(r"monitorv2(?:[ \t={\[]|$)")`, or better, count a line whose first token before `=`/`{` starts
with `monitorv2` (`re.match(r"monitorv2(?:$|[^A-Za-z0-9_:])", line)`), and add one fixture per spelling to the
counter (`monitorv2[DP-1] {`, `monitorv2[ DP-1 ] {`, `monitorv2{` — the third already gates, see R7c).

---

## F2 (model gap, medium): mirror targets are resolved by a query and can be refused; the tool models neither

**Counterexamples.**
* `monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-2` (self) with a real dump (`mirrorOf: "none"`) →
  `differ=mirror verdict=DIFFER`, exit 1 (`cases2.txt` R3e). Hyprland **refuses by design**:
  `"Cannot mirror self!"` (`Hyprland-Monitor.cpp:1346`) and leaves `m_mirrorOf` unset, so `"none"` is the only
  reachable state and the tool reports a permanent DIFFER for a config the compositor deliberately tolerates.
* `monitor = DP-2, …, mirror, desc:Dell Inc.` with live `mirrorOf: "0"` (the host did mirror) →
  `differ=mirror verdict=DIFFER` (`cases2.txt` R3g). The target is resolved through the monitor query —
  `monitorState()->query().relativeTo(...).configString(mirrorOf)` (`Hyprland-Monitor.cpp:1335`) — not by name
  equality; the tool resolves the mirror string by scanning dump `name` fields (`tools/mado-monitors.py:422`).
  [INFERENCE] the query's accepted grammar is not among the pins; that it is a query and not `==` is pinned.
* Chained mirrors (`DP-1 → DP-2`, `DP-2 → DP-1`) never reach the AGREE the tool prints for that dump
  (`cases2.txt` R3f): the second `setMirror` hits `"Cannot mirror a mirror!"` (`:1341`). The dump in R3f is
  synthetic; the point is that the model has no state for "refused", so its AGREE has no reachable live twin.

**Also on the mirror plane (inference):** `setMirror` overwrites the mirror's position with the source's
(`:1386`), so a mirror rule carrying an explicit position is compared against a coordinate the compositor may have
replaced; whether `MonitorLayoutController::arrange()` re-applies the explicit position afterwards is not pinned
(the controller is not in either fetch set). Flagged, not scored.

**Impacted axes.** Operability: a join tool that prints DIFFER for a config the host refuses by design, with a cause
list ("runtime `hyprctl keyword monitor`, a wlr-output-management client, a mode the output does not offer",
docstring `:17-19`) that omits refusals and query resolution.

**Smallest safe correction.** (i) Resolve `mirror` the way the compositor does — `desc:` at minimum, and refuse-free
values as their own verdict — or (ii) at minimum state the two refusals and "name only" in the docstring and route a
`mirror` value that is not a dump name to `NOT_COMPARED` instead of `differ=mirror`.

---

## F3 (declaration gap, medium-low): `source = …` includes are invisible, and `NO_RULES` (exit 4) is printed for a config that does configure monitors

**Counterexample.** Config consisting of `source = monitors.conf` only, dump with one output →
`lines=0 rules=0 … verdict=NO_RULES`, exit 4 (`cases2.txt` R7a). Hyprland follows the include (`source` is a
registered handler, `Hyprland-ConfigManager.cpp:614`) and the layout the Hyprland wiki itself uses puts each
`monitor =` line in a sourced file. The docstring's "Lines." section (`tools/mado-monitors.py:36`) never mentions
`source`, and `NO_RULES` reads as a statement about the config, not about the files handed to the tool. Passing the
sourced file is possible (`--config` accepts several, read in argument order) but nothing tells the user that an
include was skipped.

**Impacted axes.** Operability (mis-read summary), and any ledger row that quotes `verdict=NO_RULES` as "the config
has no monitor rules".

**Smallest safe correction.** Count a line whose first token is `source` into a `sources=<n>` field and, when
`sources > 0` and `lines = 0 and v2 = 0`, print `NOT_COMPARED` (or keep exit 4 but add `sources=` and one docstring
sentence: "includes are not followed; pass every sourced file").

---

## Verified negatives — attacks that found nothing (these support the contract)

| # | Attacked semantic | Case | Result and pin that settles it |
|---|---|---|---|
| N1 | `desc:` text padded with spaces / tabs / VT, and the whole field padded | R2a, R2b, R2c | `AGREE` for all three; `trim()`/`std::isspace` (`Monitor.cpp:1204`, `hyprutils-String.cpp:11`) strips exactly the tool's `WS` set. Faithful. |
| N2 | `transform` on a mirror line (`…, mirror, DP-1, transform, 3`) and non-canonical integers (`transform, 07`) | R3a, R3b | rule `transform=3` / `transform=7`, comparisons correct; `isNumber`+`stoi`+clamp to 0..7 (`Parser.cpp:214-221`) accepts `07`, and so does the tool's `INT_RE`. Faithful, and the `badrules`-ungated path is not entered. |
| N3 | reserved areas: no prior rule, after an explicit rule, stoi prefixes, three numbers only, extra trailing fields | R5a-d, R8b | default rule (mode preferred, pos auto, scale auto, transform 0) matches `CMonitorRule`'s defaults (`MonitorRule.hpp:41-46`); a present rule is left alone (no reorder); `+5`/`10abc`/`1.5`/`0x10` accepted like `std::stoi` (`legacy-ConfigManager.cpp:1323`); a missing 4th number drops the line exactly like the `stoi` throw → no rule (`:1341`); extra fields ignored by both. Faithful. Reserved *values* stay outside the comparison, as declared. |
| N4 | disabled output / runtime re-enable | R4a, R4b | rule disabled + live disabled → `DISABLED`; rule disabled + live enabled → `differ=disabled DIFFER`. `disabled` in the JSON is `!m_enabled` (`HyprCtl.cpp:285`) and `m_enabled` is corrected across reloads by `ensureMonitorStatus` → `onDisconnect()`/`onConnect(true)` (`MonitorRuleManager.cpp:186`), so the tool's model of the flag is sound; the only miss is the declared runtime-`keyword` cause. |
| N5 | `auto-left` / `auto-right` | R6a, R6b | both parse to auto (`Parser.cpp:146-171`) and the tool compares no position — correct as declared ("position (explicit only)", `:60`). Note the live position *is* computable (`MonitorPositionController.cpp:68`), so this is a capability gap, not a false claim; the headline ("does each connected output run the … position … its rule declares?", `:1`) and the "Not compared" list (`:20`, which omits auto position/mode/scale) overstate it slightly. |
| N6 | `monitor =` written inside another category block | probe case 1 | an unscoped handler fires inside `decoration { … }` in hyprlang 0.6.8 (`hyprlang-config.cpp:838-875`: the category check applies only to scoped handlers), so the tool's block-blind line scanner is right. Supports the tool; no change needed. |

## Impact on the round-45 data under attack

* `tools/mado-monitors.py` — F1 (verdict plane), F2/F3 (model + declaration). None of them needs a new pin; all
  locators are inside the already-frozen fetch sets.
* `quality/counters/c1-r45-monitors-v2.py` — fixtures cannot express F1 (no bracket v2 spelling anywhere) and no
  fixture carries a mirror line with a `desc:` target or a self-mirror; green is not evidence of correctness here,
  the same shape as w1's counter-coverage note.
* `corpus/knowledge/hyprland-monitor-rule-r45.md` — not contradicted (`:105` already limits its v2 claim); no row
  needs editing for F1/F2/F3, but a v2 correction of the tool should be recorded against S302-S310 scope if the L1
  chooses.

## Tooling / host state

No install, no package transaction, no PATH write, no compositor command, no Wayland client, no host config read
beyond the pins. `g++` (host, existing) compiled one throwaway probe against the already-installed
`/usr/include/hyprlang.hpp` + `libhyprlang.so` (0.6.8) inside scratch; the probe source is kept in `receipts/`.
Scratch `/fast/scratch/hyaku/mado-r46/CritW2ToolSemantics/` removed after the receipts were copied here.

Report: .ufo/waves/round-46/w1/CritW2ToolSemantics.md
