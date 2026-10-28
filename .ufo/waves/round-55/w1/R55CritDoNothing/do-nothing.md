# R55CritDoNothing — do-nothing controls scored against the frozen round-55 predicates

Seat: R55CritDoNothing (critic, do-nothing lane). Base `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`; freeze commit
`54dacbd843d64ba744cd3f1bdc2ec622e5010039` (verified: `freeze-verify.py` → `FREEZE_VERIFY: bad=0 … OK`,
frozen-tables sha256 `bf46c889…9490`). The wave's own counters (`quality/counters/c1-r55-*`, `c3-r55-p19.py`,
`tools/mado-kbdopts.py`, `quality/check-r55-controls.py`) are not in the base or freeze commit, so every checker used
here is a seat-written mirror of the contract text (`claims-frozen.md`, `registration.md`); none is the wave's counter.
Scratch and every temporary repo lived under `/fast/scratch/hyaku/mado-r55/R55CritDoNothing/` (removed before yield).
Artifacts copied here: `artifacts/` (tools, C1 junk entry, C3 errata variants, C2 reference and probes), `logs/`.

## Verdict table

| claim | do-nothing control | what it skips | visible result | frozen predicate |
|---|---|---|---|---|
| C1 | junk entry (frozen quotes transcribed, placeholder propositions, 3 registry rows + README row; K17 cites a constructed `efb50993…/1.26.0/protocol/wayland.xml` URL) | opening any pin, writing any proposition | counter `TARGET_MET rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3` (tolerant cell reading); harness `good=ok controls=7/7 verdict=OK` | **PASSES — predicate is wrong** |
| C1 | same junk, literal "no `\|` inside a cell" reading | — | `rows=17/18 … missed=row:K16`; harness `good=bad` | fails (the frozen grammar is self-contradictory for K16, see D1) |
| C1 | junk with K17 → registered S052 (literal source rule) | — | `missed=source_cell:K17` (tolerant); `row:K16,source_cell:K17` (strict) | fails (see D2) |
| C2 | `ctl/const-host.py` (frozen control) | the tool | visible 1/18 | fails visible half |
| C2 | `ctl/empty.py` (frozen control) | the tool | visible 0/18 | fails visible half |
| C2 | `ctl/lookup-committed.py` (frozen control; replays committed fixtures by argv) | the tool | visible **18/18** | visible half passes; holdout 8/8 is the only rejecter and is **not verifiable by this seat** (sealed) |
| C2 | global-values-only tool (`c2ref.py --variant global`) | device blocks | visible 14/18, failing F04 F05 F09 F10 | fails |
| C2 | device-block-ignoring tool (`c2ref.py --variant nodev`) | device blocks | visible 15/18, failing F04 F05 F09 | fails |
| C3 | plain append: P23 cell = P19 sentence verbatim, Q01–Q13, heading, README line | the correction | `p23=bad verdict=TARGET_MISSED missed=p23` | fails (predicate correct here) |
| C3 | **stuffed append**: P23 cell = P19 false sentence verbatim + a keyword clause; Q01–Q13; heading; README line | the correction | `prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET`; harness `good=ok controls=6/6 verdict=OK` | **PASSES — predicate is wrong** |
| C3 | stuffed append without the heading `## Correction (round 55)` | heading | `verdict=TARGET_MET missed=none` | **PASSES — heading unenforced (D6)** |

## Scoring detail

### C1 junk entry (PASSES)
Build: `tools/build_c1_junk.py` writes the entry from `frozen-tables.json` only. Each row is
`| Kxx | placeholder … | Sxxx | pin:line | `quote` |`; propositions are placeholder text (≥40 chars) that was never
checked against any pin. Registry rows S378–S380 (opened 2026-10-28, tier A, mined, URL = frozen commit + new-row
suffix, used-by = entry path) and one README row are added. K17 cites S381, a row whose URL is
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/1.26.0/protocol/wayland.xml`
(constructed; the seat did not fetch it; [INFERENCE] it does not resolve to the wayland spec).
Diff: `artifacts/c1/junk-registry-readme.diff`; entry: `artifacts/c1/junk-entry.md`.
Counter run (tolerant cells): `MADO_KBD_ENTRY: rev=4ed47cd… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none`.
Harness mirror: all seven mutants fail the named leg (`quote:K04`, `anchor:K01`, `source_cell:K10`, `row:K17`,
`host:H02`, `pin_hash`, `entry_absent`) and `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`.
So the C1 predicate accepts an entry whose propositions were never read. The declared limit in `claims-frozen.md`
acknowledges the proposition is unchecked; the predicate still prints TARGET_MET and the claim is "sourced entry".

### C2 controls (none passes the visible half except the lookup; holdout not runnable)
Reference `tools/c2ref.py` (written from §C2 text) reproduces 18/18 committed fixtures byte-for-byte and rc, so the
grammar text and committed expectations agree on the visible set. Probes I wrote (`artifacts/c2/probe-inputs/`,
not the sealed set) show the device-ignoring controls diverge from the reference on key-before-name (p1), duplicate
keyboard blocks (p2) and bad device values (p4):
- p1 kbd-a: reference `repeat_rate=25 … from=-/-/- unsupported=1`; global and nodev `unsupported=0` (the device line
  is silently dropped, not counted).
- p2 kbd-a: reference `repeat_rate=50 repeat_delay=300 from=D/D/-`; global and nodev give defaults `from=-/-/-`.
- lookup: `MADO_KBDOPT: SETUP usage` on every probe (it only knows committed argv).
The holdout is sealed and was not opened (see report). Those probes are my evidence that device-block inputs separate the
controls; they do not prove the sealed result.

### C3 stuffed append (PASSES)
Build: `tools/ctl_c3.py` → `artifacts/c3/errata-stuffed.md` (base bytes unchanged; block appended; README line
`| knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md (round 55 correction) | P23 supersedes P19 |`).
P23 cell = the P19 sentence verbatim (false: pin `Hyprland-ConfigActions.cpp` lines 1566–1569 send PRESSED in the
`else` arm — Q09 at 1568, Q10 at 1569) followed by: "The `== 0` arm sends a RELEASED key; `otherwise` (any other value)
sends no key, and the `else` arm is not a PRESSED path." The appended clause is also false (Q09 PRESSED, Q10 RELEASED,
Q11/Q12 pointer buttons in the same arm). The predicate's p23 leg only greps tokens (`m_passPressed`, `== 1`, `== 0`,
`PRESSED`, `RELEASED`, one of `otherwise`/`any other`/`else`, Supersedes `P19`), so it passes.
Counter: `MADO_P19_FIX: rev=4492933f… prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none`.
Harness mirror: C3-CTL-1..6 each hit the named leg; `MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK`.
The plain variant (verbatim P19 sentence, no keywords) is correctly rejected by `p23`; the predicate fails only when
keywords are appended, which is the do-nothing's point.

### C3 heading-less variant (PASSES)
Same as the stuffed variant without `## Correction (round 55)`: `MADO_P19_FIX: … verdict=TARGET_MET missed=none`.
The registration grammar requires the heading; no leg names it.

## Defects and ambiguities in the frozen predicates (input that shows each)

- **D1 (C1, self-contradiction).** `frozen-tables.json` K16 quote is `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`.
  The registration says every row is `| ID | … | pin:line | `quote` |` with "no `|` inside a cell". A literal split gives
  8 cells; my strict run prints `row:K16` on the junk and on any honest row. Under a tolerant parse (quote = text between
  the final backtick pair) K16 passes. The predicate is either unsatisfiable as written or passable only by a tolerant
  reading the text does not state.
- **D2 (C1, source rule vs reuse list).** Rule: `source_cell:<id>` fails unless the registry URL "contains the frozen
  commit". K17's pin `wayland-1.26.0-wayland.xml` has registered row S052 with URL
  `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` (no `efb50993`). The registration
  nevertheless says "Existing rows reused: … S052". With S052 the honest entry fails `source_cell:K17` under the literal
  rule (`MADO_KBD_ENTRY … missed=source_cell:K17`). The only way to satisfy the rule is a row whose URL merely contains
  the commit (D3).
- **D3 (C1, source leg is a string test).** The `source_cell` leg tests URL suffix, commit substring and status `mined`
  in SOURCES.md. Nothing is fetched or hashed; the junk's constructed S381 URL passes. Combined with D2 this means the
  predicate's sourcing evidence is textual.
- **D4 (C1, proposition unchecked).** No leg tests proposition text (length is in the grammar, no leg). Placeholder text
  passes. Declared in claims-frozen; still counted as coverage.
- **D5 (C3, false sentence accepted).** `p23` is a keyword presence test. The stuffed correction keeps the false P19
  sentence and passes. The leg cannot distinguish a corrected proposition from an uncorrected one with added words.
- **D6 (C3, heading unenforced).** The grammar (`registration.md` §C3, `claims-frozen.md` C3) requires a heading containing
  `Correction (round 55)`; no leg in `missed=` names it. The heading-less variant passes.
- **D7 (C3-CTL-1 wording).** The "absent" control also misses `readme` (base README has no P23 line) — the frozen text
  says it misses "rows+p23". Harmless because the named legs appear, but the stated expectation is inexact.
- **D8 (C2, lookup rejection depends only on the seal).** The lookup passes all 18 committed fixtures (`MADO_KBDOPT`
  byte-equal). Its rejection by the predicate is entirely the sealed holdout's argv difference (any non-committed
  argv gets `SETUP usage`). If a holdout fixture expects `SETUP usage` rc 2, the lookup matches it and the frozen
  `0/8` claim fails for a correct-or-not reason the harness would report as a control failure. Not checkable here.
- **D9 (C2, unpinned grammar corner).** For an empty stack the frozen KEY rule "stack joined with `:` then `:` then LHS"
  is ambiguous: `lhs` alone (my reading) or `:lhs`. Under `:lhs` a top-level `input:repeat_rate = 40` is ignored;
  under `lhs` it is global. The committed fixtures contain no top-level colon keys, `$` lines or `source =` lines (grep
  of `fixtures/c2` for `^\s*(input:|\$|source\s*=)` → no matches), so the visible 18 do not decide it.

## Not verified / not run
- The sealed C2 hold-out (8 fixtures, `holdout_commit`): not opened, not searched for, not run. The C2 "passes the
  predicate" answers for lookup, global-only and device-ignoring controls therefore rest on the visible 18 plus my probes.
- The wave's own counters and `check-r55-controls.py` are not in the base or freeze commit; the mirrors are my reading.
  A divergence between my mirror and the wave's counter is possible; D1–D9 are reproducible from the frozen text and
  the inputs listed above.
- No proposition was checked for truth against the pins beyond the quote/line legs (the C1 entry is a placeholder by
  design; the C3 stuffed clause is false by design, see above).
- Network: none used. The constructed S381 URL was not fetched.

## Reproduction (commands in `logs/`)
- `python3 -I artifacts/tools/c1check.py --repo <scratch repo> --rev <rev> --work <dir> [--strict-cells]`
- `python3 -I artifacts/tools/ctl_c1.py <repo> <rev> <work> tolerant|strict` ; `ctl_c3.py <repo> <base> <work> plain|stuffed|stuffed-nohead`
- `python3 -I artifacts/tools/c2run.py <frozen export root> -- python3 -I artifacts/tools/c2ref.py [--variant global|nodev]`
- Full run outputs: `logs/c1-checker.txt`, `logs/c1-harness.txt`, `logs/c3-controls.txt`, `logs/c2-visible.txt`.
