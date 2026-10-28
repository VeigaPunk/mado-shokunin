# Round 55 — registration v2 (pre-data re-registration; v1 files are untouched)

Written 2026-10-28 by the L1 after wave 1 settled, BEFORE the real C1 entry, the real C3 block, the C1/C3 counters and
every harness were integrated or scored on real data. It is a NEW versioned file (claims-frozen.md rule: "a falsified
predicate is an honest stop or a pre-data re-registration under a NEW versioned file, never an edit of this one"); the v1 files
`claims-frozen.md`, `registration.md`, `frozen-tables.json` stay byte-identical (freeze commit `54dacbd8`). Wave-1 seats scored
only synthetic trees; the sealed C2 hold-out was revealed to the L1 only after the candidates were committed (`3c868d82`,
committer 2026-10-28T20:07:02-03:00) and all four independently written tool candidates tied 18/18 committed + 8/8 hold-out, so
the choice among them (`R55ExecTool4`, robustness probes, 82 selftest assertions) was not made on hold-out score.

**Disclosure the report repeats:** read literally, v1 PRED-C1-r55 could not be met by any entry. `frozen-tables.json` K16's
quote contains `||` while §C1 says "no `|` inside a cell" (R55ExecC1CounterA/B, R55ExecC1Harness, R55RevC1Contract D1), and
K17's `source_cell` leg required a URL containing the Hyprland commit while its registry row S052 is a gitlab wayland tag URL
(R55CritControls A6, R55ConnClaims D2, R55CritDoNothing D2). These are L1 freeze defects; v2 fixes only them and the other
mechanical contract defects below. No predicate sentence, output-line grammar, target value or control COUNT changes.

## Changes (each names the seat evidence under `.ufo/waves/round-55/w1/`)

| id | v1 text | v2 text | evidence |
|---|---|---|---|
| E1 | K16 quote `if ((!VAL \|\| !VAL->m_bSetByUser) && !fallback.empty())` at legacy ConfigManager.cpp:1119 | K16 quote is the pipe-free substring `!VAL->m_bSetByUser) && !fallback.empty())` of the SAME line (`frozen-tables-v2.json`; `freeze-verify-v2.py` proves it; no quote of any table contains `\|`) | R55ExecC1CounterA.md D1, R55RevC1Contract.md D1 |
| E2 | `source_cell`: registry URL must contain the frozen commit | per-pin revision rule (`frozen-tables-v2.json` `c1.rev_rule`): `Hyprland-*` pins need the commit `efb50993…` in the URL; the wayland pin needs the URL to end `1.26.0/protocol/wayland.xml`; S052 satisfies it | R55ConnClaims.md D2, R55CritControls.md A6 |
| E3 | `host:<id>` unreachable when the quote leg fires first | the counter reports EVERY failing leg per row (list-all); `host:<id>` is evaluated on the row's quote cell as a substring of the committed host pin line, independently of `quote:<id>`; C1-CTL-6 requires `host:H02` in `missed=` | R55CritControls.md A3, R55ExecC1Harness.md item 3 |
| E4 | `sources=<c>/<d>` undefined | `<c>` = K rows whose `source_cell` leg holds, `<d>` = 18 | R55RevC1Contract.md D6 |
| E5 | cells never hold `\|` | unchanged; additionally a row containing a backslash-escaped pipe is a malformed row (`row:<id>`) | R55RevC1Contract.md D1 |
| E6 | C1-CTL-7 edits the tree's `frozen-tables.json` AND a pin | required leg is `pin_hash`; collateral legs (`tables_sha`, `quote:`, `host:`) are allowed; counters and the C1 harness read `frozen-tables-v2.json` and embed ITS sha256 `13d6e2f9c0dfe1287e2cd9a7d814d95a4fb0ff0ad7ce644aad7ead18af69a7b9` | R55ExecC1CounterA.md item 5, R55CritControls.md A5 |
| E7 | §C2: "KEY is the stack joined with `:` then `:` then LHS" | KEY is LHS when the stack is empty, else stack joined with `:` + `:` + LHS (committed fixture F10 pins this reading); numlock's 0..1 range is the lane's modelling rule, not a source range (ConfigValues.cpp:277 is a Bool without min/max); the harness runs the tool under test in a private directory holding only the tool and the input files its argv names; the hold-out commitment is sha256 over `<relpath>\0<sha256 of file bytes>\n` for each regular file under the hold-out root in sorted UTF-8 byte order of the relative path (the same function the L1 used to seal it) | R55RevC2Spec.md A12, R55RevC2Fixtures.md A1/A2, R55CritHoldout.md D1/D2/D4 |
| E8 | §C3 legs | adds `heading` (ATX heading containing `Correction (round 55)` must exist before the P23 row; reported as `rows:heading`) and `stale` (the bytes appended after the base prefix must not contain `only when`, any case, nor the exact P19 proposition sentence); C3-CTL-5 becomes "P19's sentence kept verbatim plus ` == 0 RELEASED otherwise`" with required leg `stale`; C3-CTL-1 requires `rows:` legs and `p23`; the control count stays 6 | R55CritDoNothing.md D5/D6, R55ExecC3Harness.md item 2, R55RevC3.md |
| E9 | harness environment unspecified | harnesses run counters as child processes with `python3 -I`, a scrubbed `GIT_*` environment and `TMPDIR`=`--work`; declared limit: a counter that sniffs its environment, keys on mutation text, caches runs or forges a consistent tree passes the harness (R55CritControls cheats.md) — the harness is evidence against a counter that prints green without work, not against an adversarial one; the freeze-order checker is likewise forgeable by backdated committer dates and a forged `createdAt` (R55CritChronology) | R55CritControls.md, R55CritChronology.md |

## Unchanged and still declared limits

The C1 counter proves quote identity at an exact pin line, row, source and host binding; it does not prove a proposition is
entailed by its quote (R55RevC1Contract: a junk entry with frozen quotes and placeholder propositions reaches `TARGET_MET`;
R55CritDoNothing calls that "predicate wrong" under §9). Entailment is carried by the w2 sentence-to-pin audit and the
non-author closure, reported and not counted. The same holds for C3's lexical `p23` leg (R55RevC3), now narrowed by `stale`
but still presence-only. v1's `claims-frozen.md` do-nothing control for C1/C3 (entry or block absent) stays what it scores.
