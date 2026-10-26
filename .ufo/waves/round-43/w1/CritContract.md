# CritContract — ambiguity hunt in C1's contract against the real compositor (r43 w1)

Seat `CritContract` (leaf, no dispatch), round 43 wave w1. **Deliverable: `findings.md` in this
directory** (9 findings, amendments, and a "checked and confirmed" list). Evidence bundle:
`receipts/` (contract and reference excerpts, pinned-source cites, seat-fetched upstream cites, docs
quotes, host config bytes, reference-tool runs, fetch hashes, quote-check output);
`check-quotes.py` re-greps every quote against those receipts (52/52 PASS, `receipts/check-quotes.txt`).

Target: the frozen C1 contract = docstring of `quality/counters/c1-r42-geometry.py` (sha256
`ed78d693…`), reference `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (sha256 `e3c2e471…`), read
against pinned Hyprland 0.56.2 sources (`fetch/S290-S296`), the upstream legacy rule parser at commit
`efb50993780079460b0cbed1363e2166a2de1d9f`, the 0.54 wiki page (legacy syntax), and the host's own
config bytes. No lane file outside this seat directory was written; the reference was copied read-only
into scratch and run there.

## Findings (severity, contract quote, contradicted/missing source, amendment)

| # | Sev | Finding |
|---|---|---|
| F1 | **HIGH** | Grammar narrower than the legacy parser: the contract requires effect-first and exactly two fields, but `handleWindowrule` classifies each comma field by `starts_with("match:")` — any order, any number (`ConfigManager.cpp:2016-2050`); docs and the host's own `input.conf:45` / `steam.conf:6` use it. Measured: a later match-first or multi-effect size line is dropped, and the reference prints a **false `AGREE`** against the wrong rule (`ref-cases.txt`). Amendment: field = prop iff starts with `match:`; size/float effects contribute per field order; class-joinable = exactly one prop, `match:class`; new fixtures. |
| F2 | **HIGH** | "a tiled window never reads it" (ref:5-6) is false: `readStaticRules` applies static rules (incl. `static_.size`) to **every** matching window, tiled or not (`WindowRuleApplicator.cpp:483-509`, `:421-428`, `:526-543`); only the default floating algorithm's first-map branch consumes it (`DefaultFloatingAlgorithm.cpp:51-66`). Amendment: "stores always, consumed only on first map of a floating window". |
| F3 | MED | "Rules apply in file order" has two readings (tool argv order vs compositor order) and no fixture decides (`order0` only orders its own argv). The compositor registers all named `windowrule { … }` blocks before all keyword lines in parse order (`ConfigManager.cpp:946-963`), and parse order is the `source=` expansion (host `hyprland.conf:4-32`, glob at `:23`). Amendment in `findings.md`. |
| F4 | MED | The class guard `holds no character below U+0020` is presented as `RE2::FullMatch` fidelity but diverges from it: `.` matches every char except `\n` in RE2 and Python, so `\t`/`\r`/`\x01` classes match in the compositor; `ctlclass0` locks the divergence in. Amendment: delete the guard (and the fixture expectation) or declare it conservative. |
| F5 | MED | Whitespace model: the contract separates on runs of spaces/tabs, while `handleWindowrule` requires a literal space and takes everything after the **first** space as the value (`ConfigManager.cpp:2026-2030`; elements trimmed only at edges). Measured both ways: tab-separated fields are accepted by the tool and rejected by Hyprland; two spaces after `match:class` become part of Hyprland's regex (no match) but are swallowed by the tool (prints `AGREE`). `space0` locks in the tab reading. |
| F6 | LOW/MED | No inline `#` comment handling: hyprlang truncates at the first unescaped `#` (`hyprlang config.cpp:686, 702-716`) and the legacy docs' own examples carry trailing comments; the reference reports `NO_SIZE_RULES` for such a line. Amendment: strip comments (with `##`) before the field split. Host currently writes full-line comments only. |
| F7 | LOW | `unsupported` conflates malformed lines with well-formed size rules the class join cannot attribute (host: `pip.conf:6` match:tag, `system.conf:4` match:tag, `steam.conf:6-7` class+title; docs: expression sizes). `NO_SIZE_RULES` then reads as "no size rules". Amendment: split the counter or document the meaning. |
| F8 | LOW | Two sentences with two readings and no deciding fixture: the 1048577-byte stdin boundary (`stdinbig0` feeds 1048578) and a repeated `--rules` path (reference processes it twice, `rules=2`). Amendment: one sentence each. |
| F9 | EDITORIAL | "The effect is the first / first token of field 0" duplicates `first` across the line break (contract:29-30; ref:29 has it once). |

## Consequence for the round

- **C1's contract needs a v2**: F1, F4, F5 and F6 change fixtures (`matchfirst0`, `multieffect0`,
  `inlinecomment0`; `space0` and `ctlclass0` expectations change), so the counter, its reference and its
  controls would have to be re-frozen and re-run — the L1's call, per registration.md ("a hole `w1`
  finds before any data commit re-registers as v2 with a new freeze, and the report names both
  predicates"). Predicates named: **PRED-C1-r42** (C1) and **PRED-C2-r43** (C2).
- **C2** is not touched by these amendments, but the C2 entry must not repeat "a tiled window never
  reads it" (F2) and must name the reported size field `GEOMETRIC_GOAL` if it cites it.
- The host's actual gkeep line (`gkeep.conf:4`, effect-first, single space, no comment) is the contract's
  happy path and is joined correctly by the reference; the defects are in the general claim, not in
  today's one-file invocation. The census that says no gkeep window is open is the pinned
  `fetch/host-clients-r43.json` (4 clients, all `floating: false`: Alacritty, zcode, grok-bot, chromium).

## Tooling, scratch, safety

- No tools installed, no pacman, no compositor mutation, no Wayland connection; only read verbs and
  file reads. Scratch `/fast/scratch/hyaku/mado-r43/CritContract/` (downloads, reference copy, fixtures)
  was removed after the receipts were copied here; no cited path is outside this seat directory.
- The reference copy's sha256 equals the frozen reference's (`receipts/ref-sha.txt`).
- An untracked `tools/mado-geometry.py` appeared in the lane during this run (another seat's build).
  This seat did not create, edit, or run it; the findings are about the frozen contract only.
