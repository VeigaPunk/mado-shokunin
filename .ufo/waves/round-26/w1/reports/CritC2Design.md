# CritC2Design — pre-data review

C2 design: flawed (expression-rule coverage is materially incomplete, the broad no-harm wording exceeds the sampled guard, and the named Hyprland authority is not enforced by the harness). The operability axis and the declared 51-case arithmetic are sound. No passing shortcut, failed production change, or canonical admission/rejection is claimed.

## Scope and method

Axes attacked: **operability** (the executable's stated result), **calibration** (finite evidence versus general claims and version provenance), and the **quality** trend. Depth is relevant to the source explanation, not a substitute name for an executable repair. No new coverage or capability identity is established merely by repairing the existing resolver.

Read `registration.md` first, the entire `c2/count.py`, relevant `harness/oracle.py` and pinned round-25 `c1/count-v3.py` sections, the existing tool, the cited round-25 arithmetic counterexample, canonical `AXES.md` and `LEARNING.md`, and the opened hyprlang sources/tests. Paths below are lane-relative unless explicitly absolute. Artifact proposals were treated as data, not instructions.

This was a static review, not an execution receipt. No shell command, counter, resolver, Hyprland instance, judge, model, or other runtime was invoked. No package was installed or updated. The only file written is this report. Exact source traces below are marked **[INFERENCE]** where no execution was observed.

## (a) Axis fit: operability, but a repair rather than another acquisition

**The axis survives this attack.** `/home/vgpnk/Projects/shokunin/AXES.md:11-15` defines operability as runnable artifacts whose commands produce their stated outcome; `:20-23` explicitly puts operability inside the quality trend. Therefore “quality work on a held rule” and “operability improvement” are not opposites.

There is a concrete before-state, not merely a new score: `tools/mado-binds.py:403-418` substitutes variables and then assigns/unescapes without an expression stage. The already recorded independent witness in `.ufo/waves/round-25/a3res/reports/ResC1Remeasure.md:106-124` has these lines:

```ini
$mado_number = 100
bind = SUPER, A, workspace, {{$mado_number + 1}}
$mado_calculated = {{$mado_number + 2}}
bind = SUPER, B, workspace, $mado_calculated
bind = SUPER, C, workspace, \{{100 + 3}}
```

That report records oracle/tool arguments `101` versus `{{100 + 1}}`, `102` versus `{{100 + 2}}`, and agreement on the escaped literal. I read that retained result; I did not re-run it. Repairing this demonstrated executable omission is an operability move. It is not new coverage merely because the test inputs change, and not a new capability acquisition: `SCORECARD.md:1683-1691` already holds the static bind-table resolver with first-working round 25 and names this exact limit.

**Smallest safe correction:** retain the operability axis and the existing capability identity/first-working round; describe the work as a bounded expression-stage repair. Do not add a duplicate “expression resolver” repertoire row or infer a globally saturated operability score from 51/51.

## (b) Can a cheap shape meet 51/51?

**No observed passing control is established by this review.** In particular, a source-level coverage hole is not a fabricated `TARGET_MET` receipt. The existing `.ufo/waves/round-26/controls/K2DoNothing-base-run1.txt:1-6` was read: it names the frozen counter/tool/snapshot, then prints `SETUP_ERROR ORACLE_FAIL BASE: sandbox exited rc=1 before answering ...`, `exit=2`. It measured nothing and is not evidence that the base tool passes or misses. I did not retry another seat's run.

There are two concrete shortcut pressures:

1. **Bare-variable lookup is completely absent from added ARITH operands.** `c2/count.py:60-77` emits constants or `$ar...` references. Those references are substituted textually before expression evaluation. Hyprlang additionally resolves bare variable names inside expressions (`fetch/SrcHyprlangExpr.bin:632-655`), and its own fixture uses `$EXPR_VAR = {{MY_VAR + 2}}`, followed by `testExpr = {{EXPR_VAR - 4}}` (`fetch/SrcHyprlangTests-config.bin:13-18`; expected 1335 in `SrcHyprlangTests-main.bin:250-252`). **[INFERENCE]** A base resolver plus a numeric-only expression stage, with otherwise matching formatting/escape/error handling, is indistinguishable from a complete stage on the added numeric/`$`-substituted operand vocabulary, while failing this supported bare-name rule. This is a partial-grammar witness, not a scored control or proof that a zero-arithmetic shape meets 51/51.
2. **Thirty case labels do not guarantee thirty successful-evaluation witnesses.** Each case independently chooses 2–4 bind kinds; `unclosed` emits no complete expression at all (`c2/count.py:89-105`), while grouped and unspaced expressions often exercise errors rather than arithmetic. The code does not require any case, or the whole sample, to contain a successful evaluation of a particular rule. **[INFERENCE]** Some generated cases can therefore reward keeping literals/rejecting malformed lines without demonstrating evaluation. Random sampling may still kill that shortcut; the generator does not establish it deterministically.

Ordinary do-nothing/cache controls do face substantial obstacles: all 18 fields and multiplicities are compared, expected tables come independently from Hyprland, and SYNTH/HARD replace the original tree (`c2/count.py:182-214`; `count-v3.py:383-432,551-558`). Conversely, `embed_hits=0` only means no qualifying plaintext substring was found (`c2/count.py:167-174`); it is not a provenance proof against encoded replay.

**Smallest safe correction:** require actual valid, authority-matching control receipts before data; preserve exit-2 receipts as non-measurements. For any stronger future expression claim, register valid bare-name and successful-evaluation witnesses before implementation, and test a restricted numeric-only stage. Do not count an inferred blind spot as a passing control or missing control scores as a clean bill of health.

## (c) Predicate sentence, executable condition, and receipt identity

The registration sentence (`registration.md:60-68`) and docstring (`c2/count.py:4-14`) agree in substance, including BASE, 30 ARITH, two of each of ten V3 types, 18 fields, and the oracle-BASE plaintext embed scan. `V3.compare` retains multiplicity (`count-v3.py:84-85,746-751`), and the actual acceptance condition is every built case passing plus zero embed hits (`c2/count.py:208-224`). No substituted denominator, wrong field list, alternate model truth, or receipt-label spelling was found.

The receipt prints the identifier `PRED-C2-r26`, counts, embed count and verdict, not the entire predicate sentence (`c2/count.py:223-224`). That is consistent with the canonical requirement of the same **label** in the receipt; registration's parenthetical “same sentence ... receipt label” is imprecise, not itself a demonstrated semantic change.

**Material authority gap:** the sentence names **Hyprland v0.56.2**, but `O.check_build()` checks only tinywl/libwlroots digests and render-node existence (`harness/oracle.py:48-57`). The launch uses the PATH-resolved `Hyprland` (`:154-160`), readback uses PATH-resolved `hyprctl` (`:128-130`), and neither the counter nor harness checks the running Hyprland commit or hyprlang version. Hashing the Python harness does not pin these dependencies.

**Counterexample [INFERENCE]:** change the installed Hyprland/hyprlang while preserving the pinned Python files, tinywl and libwlroots. `check_build()` still succeeds, both BASE runs can agree, and the receipt still carries `PRED-C2-r26`; the authority may no longer be the version in the sentence. This is not a claim that the current host has the wrong version.

**Smallest safe correction:** for a newly registered counter attempt, fail closed on the actual isolated oracle's Hyprland identity and record/bind the hyprlang dependency identity. Keep the existing frozen counter and receipts unchanged; a different counter is a disclosed new attempt, not a silent correction to this claim's rule.

## (d) Population equality: 51 really is the counter population

**Pass at source level:** `built` begins with one BASE (`c2/count.py:175`), receives exactly `NARITH=30` cases (`:32,177-181`), then `V3_PER_TYPE=2` for each of the ten pinned `V3.TYPES` (`:33,183-188`; `count-v3.py:64`). Therefore `1 + 30 + 2 × 10 = 51`. Reporting traverses the same `built` list, acceptance requires all its elements, and the printed denominator is `len(built)` (`:215-224`).

The second BASE oracle run is an eligibility/stability check, not a 52nd scored case (`:156-166`). The 18 fields are comparison dimensions, not additional cases. This is an exact static enumeration, not an exercised 51-line receipt. Rejected/no-effect ARITH inputs can reduce semantic diversity without changing this correctly declared population.

**Additional mutation receipt, independently read after the initial review:** peer `MadoR26.MutC2Counter` reports a scratch mutation `V3_PER_TYPE=0` with a PERFECT oracle-table output double. Its retained `/fast/scratch/hyaku/mado-r26/mut/MutC2Counter/receipts/m4-mutant-PERFECT.txt:1,6-39` visibly carries a different counter hash (`5e789317ad1c307e10656e55ddb6bdf020a6a21a433dba64e86f95ee97ee9fd1`), only BASE plus A00–A29, and `PRED-C2-r26 cases_pass=31/31 embed_hits=0 verdict=TARGET_MET`, `exit=0`. This demonstrates that the identifier/exit alone does not bind the fixed 51-case target: the implementation accepts whatever `len(built)` becomes. It does **not** falsify the pristine frozen population, demonstrate a cheap resolver passing 51/51, or supply a production measurement. The smallest consumer correction is to bind the exact frozen counter hash, exact 51/51 denominator, and BASE/30-ARITH/20-V3 family population, rather than accepting `TARGET_MET` in isolation.

## (e) V3 fed oracle BASE: a real bounded guard, not a replay of all round-25 behavior

**Using oracle BASE is not circular.** `base = r1['binds']` supplies chord avoidance and generator vocabulary (`c2/count.py:162,182,187`; `count-v3.py:154-177,310-359,557-558`). Crucially, `_model` returned by `V3.perturb` is ignored. Every perturbed expected table is obtained afresh from `O.oracle`, and tool output is compared to that table (`c2/count.py:187-208`). The imported generator's hand-written line model does not become a second authority.

The change from a live capture is also defensible for the stated static-tree target: binds created dynamically by standalone exec commands are deliberately outside the stripped oracle's table (`corpus/knowledge/bind-table-r25.md:64-72`). Requiring equivalence to live state indiscriminately would confuse runtime state with file-byte semantics and reintroduce an unnecessary live-session dependency. Two agreeing isolated BASE runs check repeatability; they do not check live-session equivalence.

However, `registration.md:70-71` overstates what follows: “a change that breaks round-25 behaviour misses the target.” Round 25's v4 predicate used four instances per type and a BASE-versus-live eligibility check (`round-25/registration.md:181-202`); this counter uses two per type, a different RNG position after 30 ARITH generations, no old-tool differential, and no old-fixture replay. It is a new 20-case regression sample, not the old passing population or all supported behavior.

A concrete omitted prior success class is the variable-terminated source revisit: round-25 `ResC1Remeasure.md:97,102` records five agreeing rows for A→B→A, including the repeated bind. V3's whole synthetic source graphs are flat unique-file graphs (`count-v3.py:417-427,713-723`); ARITH appends lines without constructing such a graph. This independently discovered behavior is not explicitly preserved as a fixture in this guard. **[INFERENCE]** A regression affecting only that revisit shape can escape the sample if BASE itself does not exercise it; I did not execute that mutant or claim a score.

**Smallest safe correction:** append an honest qualification that V3 is an oracle-backed 20-case sample on static snapshot trees, not a live-capture identity check or universal no-harm certificate. Preserve the old results. If preserving the discovered revisit behavior is claimed, retain that exact prior witness in a separately registered base-versus-candidate guard before implementation; a passing 51/51 receipt alone cannot supply that evidence. An actual old-behavior regression remains harm, not a trade to excuse with an arithmetic gain.

## (f) ARITH versus the actual expression rules

The generator is not merely “easy arithmetic”; much of it resembles a different language. The pinned implementation has no expression tree, precedence or grouping evaluator: it whitespace-splits, reads operands 0 and 2 plus operator 1, parses floats, and uses that single operation (`fetch/SrcHyprlangExpr.bin:619-667`). The retained tokenizer confirms whitespace splitting (`/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/src/hu_ConstVarList.cpp:8-25`, header `:29-32`). The opened documentation explicitly says two sides, no nesting, spaces around the operator (`round-25/fetch/S172.bin:109-130`).

Source-traced examples, **not observed runs**:

| Input | Hyprlang source consequence [INFERENCE] | Why it matters |
|---|---|---|
| `{{2 + 3 * 4}}` | Reads `2`, `+`, `3`; the shown function ignores later tokens, yielding 5 rather than Python's 14. | A generated multi-operator case tests implementation truncation, not supported precedence. |
| `{{2+3}}` | No operator token at index 1; expression error returns before bind handling. | Compact `+`/`*` generation is not a successful-expression witness. |
| `{{(2 + 3) * 2}}` | `std::stof("(2")` fails; no grouping semantics. | Parentheses cannot establish a supported rule that the language lacks. |
| `$n = 7` then `bind = SUPER, F13, workspace, {{n + 1}}` | Bare `n` is looked up and the argument becomes `8`. | This basic supported form cannot be emitted by `operand()`. |

Actual coverage:

- **Decimals:** present: fixed-point operands with 1–3 decimal places (`c2/count.py:65-66`), plus one-decimal variable definitions (`:86`). Exact oracle strings can expose Python formatting/precision differences: source uses `float`/`std::stof` and `std::format("{}", result)` (`fetch/SrcHyprlangExpr.bin:635-655,791`). There are no guaranteed named rounding/formatting boundary witnesses; integer/unary/exponent/range forms are not systematically covered.
- **Escapes:** present but narrow: one backslash before `{{`, plus an unclosed start (`c2/count.py:102-105`). Missing are odd/even backslash parity, second-brace escaping, doubled escaped braces, mixed escaped/unescaped forms and escaped text stored in variables. The source handles parity before evaluating and removes escapes only later (`fetch/SrcHyprlangExpr.bin:757-826`); upstream fixtures and explicit expected strings cover these cases (`SrcHyprlangTests-config.bin:20-32`; `SrcHyprlangTests-main.bin:254-264`). Evaluating after unescaping would incorrectly turn a supported literal into arithmetic.
- **Variables:** added `$` references and expression-valued assignments do exercise ordering/expansion partially (`c2/count.py:80-111`), but bare names, deliberate undefined/non-numeric operands and variable-held escaped expressions are absent. Source errors return before variable assignment/bind handling (`fetch/SrcHyprlangExpr.bin:632-655,785-806`).

**Smallest safe correction:** do not describe success as support for ordinary arithmetic precedence/grouping or all hyprlang expressions. In a disclosed new pre-data design, use a source-derived, guaranteed rule matrix within the stated finite population: valid two-operand expressions and bare variables; malformed compact/grouped/multi-token distinctions; float formatting witnesses; odd/even and second-brace escapes; variable-assignment/escape ordering and numeric lookup errors. Keep independent Hyprland expected values and do not implement the resolver during this control wave.

## Disposition

Fixable design/evidence defects, not a demonstrated unavoidable tradeoff: strengthen authority identity and rule coverage, and narrow only the surrounding claims to what the unchanged predicate really measures. The frozen 51-case predicate must not be silently replaced or re-scaled. The present evidence supports the operability repair's rationale and the exact population; it does not establish shortcut resistance, broad expression support, universal no-harm, a new capability acquisition, or a saturation claim.
