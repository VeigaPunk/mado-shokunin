# R89MReviewC2 — review of C2 (survivor list, supplementary sets, counter)

Seat: reviewer (w1, round 89, mado lane). Scope: `survivor-mutants-r89.json`,
`survivor-cases-c1side-r89.json`, `survivor-cases-c2side-r89.json`,
`quality/counters/c2-r89-survivor-kills.py` (PRED-C2-r89-v1), against
`R88MResidMut.md` §3–§4 and the round-88 tool `7d3074865a9f5acfa0f1c9c66b460e73d4031331`
(sha256 `c374d71514f1…92237`, re-hashed from git bytes; working-tree `tools/mado-mako.py`
is byte-identical). Only this report was written in the lane. No git/jj mutation anywhere.
Scratch `/fast/scratch/hyaku/mado-r89/R89MReviewC2` deleted on exit.

## 1. Survivor list vs R88MResidMut — per-entry verdict table

All eight `old` anchors occur **exactly once** in the round-88 tool (`7d307486:tools/mado-mako.py`)
and **exactly once** in the C1 candidate `.ufo/waves/round-89/build/mado-mako.c1.py`
(verified by exact-string count; the counter enforces the same with a SetupError). Each new
text expresses the same semantic change the r88 seat described.

| id | r88 report desc/verdict | old anchor @ 7d307486 | old @ 650e18b (r88 §3 ref) | in C1 candidate | same semantic change? |
|---|---|---|---|---|---|
| RM2C1-app-name-casefolded | §3.1.1, survived | `mado-mako.py:377` | :358 ✓ | 1× | yes — `!=` → `casefold() != casefold()` |
| RM3C1-bang-accepted-on-string-fields | §3.1.2, survived | :329 | :310 ✓ | 1× | yes — drops `key[1:] in BOOLEAN_FIELDS`, bare `!<field>` becomes `field="false"` for any field |
| RM5C1-mode-casefolded | §3.1.3, survived | :367 | :348 ✓ | 1× | yes — membership casefolded on both sides |
| RM7C1-include-accepted-inside-criteria | §3.1.4, survived | :310-313 | :292 ✓ | 1× | yes — if/refuse/else replaced by unconditional `self.include(value, where)` |
| RM3C2-trailing-slash-refusal-dropped | §4.1.1, survived | :437-439 (= §4 ref :437 ✓) | n/a | 1× | yes — 3-line refusal block deleted (`new: ""`) |
| RM4C2-double-slash-join-dropped | §4.1.2, survived | :430 ✓ | n/a | 1× | yes — join line (with its config.c comment) deleted |
| RM5C2-root-equality-refused | §4.1.3, survived | :276 ✓ | n/a | 1× | yes — `real == root or` removed from `within_roots` |
| RM6C2-cycle-detected-on-lexical-target | §4.1.4, survived | :458 ✓ | n/a | 1× | yes — `if real in self.stack` → `if target in self.stack` |

Documentation nuance (no defect): the seat item states R88MResidMut's line refs "refer to the
round-88 tool = 7d307486…". That holds for §4 (:437/:430/:276/:458 verified exactly). §3's refs
(:358/:310/:348/:292) refer to the **C1 tool `650e18b`** — consistent with R88MResidMut §1, which
pins c1-tool.py = `650e18b` for §3 and c2-tool.py = `7d307486` for §4. The re-expression to
`7d307486` is correct: the four anchor strings are byte-identical in both revisions.

## 2. Supplementary cases — re-derived expectations and separation

DRAFT in-process scoring (counter `evaluate` on working bytes; **not a measurement**):
B = 61+26 (c53 excluded), S = 4+4, total 95; candidate **correct 95/95, no FAIL lines**;
killed_full = 7, killed_base (B-only) = 0 → TARGET_MET. Each survivor differs from the tool on
exactly its own S case (`differs_on`), B alone kills none (`killed_by_b=False` for all 8).

| case | expectation re-derivation (upstream / tool stance) | separates |
|---|---|---|
| s1-appname-case-differs | criteria.c:75-77 `strcmp(criteria->app_name, notif->app_name)` — case-sensitive; section skipped → `anchor=bottom-left`, refusals none (tool docstring L443-444) | RM2C1 ✓ |
| s1-bang-string-field | criteria.c apply_criteria_field: bare key → boolean chain only; `app-name` not boolean → `Invalid boolean criteria field 'app-name'` (criteria.c:409-411) → upstream load error; tool stance L510-516 records a refusal, section REFUSED → anchor stays bottom-left, refusals present | RM3C1 ✓ |
| s1-mode-case-differs | criteria.c:155 `has_mode` → mode.c:12 `strcmp` — case-sensitive → section skipped, refusals none | RM5C1 ✓ |
| s1-include-in-criteria | mako.5:45 (include in the global-options list); config.c:545 `include` lives in `apply_config_option`, reachable only when `section == NULL` (config.c:867) → inside a criteria section upstream fails the option; tool stance (docstring L26-52, refusal at tool:311) → refusals present, `layer=top` | RM7C1 ✓ |
| s2-trailing-slash | tool stance (docstring L45-50 "target must be a regular file"; selftest `trailing-slash`); upstream direction consistent: `fopen("$HOME/inc.ini/")` → ENOTDIR → load_config_file:781-784 fails | RM3C2 ✓ |
| s2-double-slash | config.c:505-521 `expand_config_path` = `asprintf("%s/%s", home, path+2)` → `$HOME//inc.ini` ≡ `$HOME/inc.ini`; tool join (tool:430, comment cites config.c) → `width=321`, refusals none | RM4C2 ✓ |
| s2-root-is-a-file | lane containment stance (docstring containment paragraph; `real == root` at tool:276); no upstream counterpart — mako has no read roots; case pin states the stance | RM5C2 ✓ |
| s2-cycle-second-lexical-path | tool stance (docstring L45-50 "an include cycle is refused"; selftest `cycle`) → refuse at the second reach of `a.ini` via `link.ini`; expectation `width=2`, refusals present holds on the tool | RM6C2 — crash only (declared) ✓ |

Separation mechanics verified per mutant: RM3C2's continuation reads `$HOME/inc.ini`
(realpath drops the trailing `/`) → `width=321`, well-formed FAIL; RM4C2's continuation hits
`os.path.join(home, "//inc.ini")` → absolute `"//inc.ini"` → realpath `/inc.ini` → outside every
root → well-formed `unexpected-refusal` FAIL; RM5C2's continuation refuses a root-equal path →
well-formed FAIL; RM7C1's applies `layer=bottom` → FAIL. All four counted C2 kills are
well-formed verdict differences, satisfying the frozen "crash is not a kill" rule.

## 3. RM6C2 crash-only argument — CONFIRMED

Attempted to construct a terminating input where the mutant returns a well-formed (exit 0 JSON)
result differing from the tool. Result: impossible; every separating shape crashes.

Argument (matches declaration §C2):
1. **No false-positive separation.** The stack holds only realpath outputs (config realpath at
   tool main; `self.stack.append(real)` at tool:462). If `target ∈ stack` then `target` is a
   realpath output `R`, `realpath(R) == R`, so `real == target ∈ stack` — the tool refuses the
   same cycle at the same include with the same message. Mutant refusals ⊆ tool refusals.
2. **Every separation is nonterminating.** A difference requires `real ∈ stack ∧ target ∉ stack`.
   A target whose realpath differs from itself contains a symlink or `..` component, so its
   lexical string can never equal a realpath output; pushes are `realpath(target) ≠ target`, so
   `target ∉ stack` stays true forever. All other per-iteration decisions (trailing `/`,
   containment, stat/regular, parse refusals, file bytes, unconditional global-section include)
   are iteration-invariant → the mutant replays the identical iteration indefinitely →
   RecursionError. The tool catches only `OSError/UnicodeDecodeError` (load) and `ValueError`
   (realpath) — RecursionError propagates to exit 1 → `CRASH_PREFIXES "exit="` → per the frozen
   rule, not a kill.
3. **Empirical probes (DRAFT, in-process, all rc 0):**
   - P1 pure regular-file 3-cycle (c→a→b→a, no symlinks): mutant `survived`, no difference —
     `target == realpath(target)`, mutant refuses like the tool (declaration sentence 1 holds).
   - P2 re-entry via the *resolved* name (`link.ini→a.ini`, then `a.ini` includes `~/a.ini`):
     mutant `survived`, no difference — the lexical target equals the stacked realpath, so the
     mutant's test fires too.
   - P3 re-entry via a second lexical path (`~/sub/../a.ini`): mutant `crashed-not-killed`
     (RecursionError, exit 1).
   - s2-cycle-second-lexical-path (symlink alias): `crashed-not-killed`, `crashed_on=[case]`,
     counted=False, and its crash is printed in the row output as declared.

Verdict: **crash-only claim correct**; `s2-cycle-second-lexical-path` is the minimal carried
demonstration and the frozen kill rule cannot count RM6C2. No counter change needed.

## 4. Counter review (PRED-C2-r89-v1)

- **Predicate sentence vs code:** declaration §C2 = counter docstring = `predicate()` verbatim:
  `correct == total and killed_full == counted and killed_base < counted`, with
  `counted = 8 − |crash_only| = 7`. Kill = `F.semantic_kill` (verdict differs ∧ mutant
  well-formed there) — unchanged r88 machinery, pin-verified.
- **B-only control index arithmetic:** cases are scored in the fixed order
  `base_f, supp_f, base_k, supp_k`; `b_index = range(0,|base_f|) ∪ range(|base_f|+|supp_f|, +|base_k|)`;
  `sorted(b_index)` aligns with the verdict list and the id list is zipped in the same order.
  Correct; the selftest exercises both directions (separating cases in B ⇒ do-nothing conjunct
  fails; S-only kill ⇒ MET with `do_nothing_B_only_killed=0`).
- **c53 exclusion:** `EXCLUDED_B=("c53-summary-tilde-refused",)` filters `base_f`; the id exists
  in the frozen r88 file (62 cases → B=61, verified `B=61+26` in the run header). Rationale is
  sound: excluding the summary~-refusal case keeps B ∪ S runnable green at both the freeze
  revision (tool still refuses summary~) and the C1 revision (harm re-run, where summary~ is
  modelled), so C2's harm check does not depend on C1.
- **Pins:** machinery pins match R88MResidMut §1 and the working tree:
  `c1-r88-mako-fields.py 3678425a…cc1f`, `c2-r88-include-containment.py f8e18b7c…6767`,
  r88 case pins `a0e81b19…a091` / `8b16c0cb…d039` (all re-hashed, equal). The three round-89
  inputs are pinned via required CLI args; current sha256 for the freeze:
  survivors `9f25df3cac28d9085d2e7d2a89e6002df24f76e6c5264df98f83d4d32c8104f0`,
  c1side `c710a3e5a2a0e88692de68c6dec9815f14f5964099ec7ef6fdb8cb20bb743c1a`,
  c2side `e02e2b4de83410ab16fcf7ad92f5374c5178a3e49c80d6aa2c4994e0d04e612e`.
- **Do-nothing (no S) cannot reach TARGET_MET:** three layers — (i) CLI SetupError if either
  supplementary set is empty; (ii) in-process S=∅ gives `killed_full == killed_base`, and
  (b) `killed_full == 7` with (c) `killed_base < 7` is then contradictory → MISSED; (iii) the
  noop-survivor selftest case shows an S-independent survivor blocks MET. A "B alone kills all
  7" world also fails (c). The control is causally sound, and the DRAFT run confirms
  `killed_base=0` today.
- **Exit map / setup errors:** anchor-count, duplicate-id, crash-only-id-present, and empty-set
  violations are SetupError (exit 2), never a verdict — matches the declaration's kill rule.
  `--selftest` passed 18/18 (DRAFT, rc 0) against the working-tree tool.

## DRAFT runs disclosed (not measurements; no receipts written)

1. `python3 -I quality/counters/c2-r89-survivor-kills.py --selftest --scratch-root $S` → rc 0, 18/18.
2. In-process `evaluate` (driver in scratch): full B ∪ S scoring with all 8 survivors →
   95/95 correct, killed=7, B-only killed=0, TARGET_MET (DRAFT).
3. RM6C2 probes P1/P2/P3 (DRAFT): no-separation / no-separation / crash; plus the s2 crash row.
All runs DRAFT on working bytes; nothing written under `.ufo/waves/round-89/receipts/`.

## Minor observations (no action required from this seat)

- N1: line-reference provenance §3 vs §4 (see §1) — worth one sentence in the L1's freeze notes,
  not a defect; anchors verified byte-identical in both revisions and the C1 candidate.
- N2: the tool docstring's containment paragraph says a resolved path must "lie inside a declared
  read root"; equality-with-root counts as inside only per tool:276. `s2-root-is-a-file`'s pin
  documents the stance; a future doc pass could add "(the root itself counts as inside)". C2 does
  not change the tool.
- N3: RM3C2/RM4C2 use `new: ""`; `R87.load_mutants` permits it and `replace(old,new,1)` deletes
  cleanly — verified in the DRAFT runs.

## Verdict

**READY.** Survivor list correct and uniquely anchored (8/8, in both the round-88 tool and the C1
candidate); both supplementary sets re-derive from upstream/stance and each separates its survivor
(7 well-formed kills + 1 declared crash); RM6C2 crash-only confirmed by proof and four attempted
counterexamples; counter predicate, B-only control, c53 exclusion, pins and do-nothing behavior
all check out.

Report: .ufo/waves/round-89/w1/R89MReviewC2.md
