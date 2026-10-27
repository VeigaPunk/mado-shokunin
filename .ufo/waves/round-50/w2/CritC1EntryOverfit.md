# CritC1EntryOverfit — FALSIFY report: entry vs PRED-C1-r50

Target: `corpus/knowledge/hyprland-bind-key-match-r50.md` (data `906178b6`,
sha256 `ae8f8d4d…`) vs frozen counter `quality/counters/c1-r50-bind-entry.py`
(installed sha256 `e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0`
= registration pin; git blob `b1667e18` at 906178b6).

Method: `git clone -q --shared` lane at `/fast/scratch/hyaku/mado-r50/CritC1EntryOverfit/lane`
(asserted toplevel), committed each mutant atop `906178b6…`, scored with
`TMPDIR=<scratch>/tmpwork python3 -I <counter> --repo <clone> --rev <rev>`.
Baseline at 906178b6 reproduced `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1
admitted=1/1 verdict=TARGET_MET` — freeze receipt confirmed.

| variant | rev | verdict | deciding clause(s) |
|---|---|---|---|
| va (wrong claim, quotes intact) | db90715c | TARGET_MET rc=0 | none fail — d:85 quotes, e:17/17, j:7/7 |
| vb (`binds=200`, unfenced) | a0564b40 | TARGET_MISSED rc=1 | f:0 `total=[200]` |
| vb2 (`binds=200`+`int=1` inside backticks) | b8546cf8 | TARGET_MET rc=0 | f:1 — contradiction invisible |
| vc (live-receipt section deleted) | 41520a0f | TARGET_MISSED rc=1 | f:0 `total=[] … sha=0 resolve=0`; r:1 |
| vm (steps 4↔12 quote swap) | 80fafa44 | TARGET_MET rc=0 | e:17/17, j:7/7, d:85 |

## Findings

**F1 (DEFECT — kills nothing at data rev, but a live hole).** Clause f's "entry repeats the
receipt values" check blanks every backticked span before reading numbers
(counter:790 `prose = … re.sub(r"`[^`\n]*`"," ",…)`, comment :787-789 "backticked spans
are code … and are blanked"). vb2 states `binds=200` and `input:resolve_binds_by_sym int=1`
as inline code in the same paragraph as the correct values and is ADMITTED (f:1).
An entry can visibly disagree with the receipt on total/forms/resolve-value and pass if the
disagreement is inside backticks (or a fenced block — `unfenced` :253 drops those lines too;
`version_ok`/`digest_in` read unblanked lines but `said_sha` tolerates extras via `any(...)`
:797). Smallest safe correction: in clause f also scan the *unblanked* entry for
`\bbinds\s*[=:(]` values and `resolve_binds_by_sym` lines' `int`/`set` values, requiring any
stated value to equal the receipt (superset check instead of exact set), or narrow the
blanking to spans matching `^(code|mouse|switch):\w+$`. Seat evidence: run-vb2.txt,
diff-vb2.txt.

**F2 (declared residual, strongest counterexample recorded).** va asserts in step 12 that
the mask gate at KeybindManager.cpp:652 runs *before* the state/group keysym read of step 6 —
inverted: the pinned code reads the keysym at :369, before the `for (auto& k : m_keybinds)`
loop (:634) whose per-bind mask gate sits at :652. Every quote/locator byte-identical, all
clauses pass, `TARGET_MET`. The docstring declares this tradeoff verbatim at :138
("a true quote at a true locator can stand beside a claim it does not support") and :120
("not that its sentence is true"), so the canonical judge should reject va not as a defect
but as the admitted cost of quote-grounding. Evidence: run-va.txt, diff-va.txt.

**F3 (declared residual — misattribution answer: YES, admissible).** Clause e's per-step
check (:621-648) verifies that *some* quote on the step line occurs in the pin at range —
never that the quote supports the step's sentence. vm swaps step 4's four quote+locator
spans for the mask-compare quote (`modmask != k->modmask && !k->ignoreMods`(KBM.cpp:652))
and gives step 12 the case-insensitive quote (`KBKEYLOWER…CASE_INSENSITIVE`(:711)); both
steps stay "verified", all 7 topics still covered — because clause j (:903-919) scans *all*
steps for each topic rather than binding a topic to its step. Clause e CAN be satisfied by a
correct quote attached to a wrong step; j's global window accidentally absorbs it.
Residual text at :142 ("clause e counts numbered steps and their pin locators, not the
truth of each step"). Evidence: run-vm.txt, diff-vm.txt.

**F4 (control behaved; boundary noted).** vc deletes `## Live host run` while the head row
still cites the receipt path: f fails on missing total/forms/sha/resolve (correct MISSED).
Note clause r replays receipt-vs-live only (:1123-1163) and stays 1 with the entry's value
claims gone — r cannot see entry↔receipt drift at all; f is the sole entry-value gate, which
makes F1's hole load-bearing.

## Verdicts
- vb, vc: counter correctly MISSED (no defect).
- va, vm: ADMITTED — covered by declared residuals (truth-blindness, step-agnostic topics);
  tradeoffs, not kill-rule defects, but recorded as counterexamples for the L1.
- vb2: ADMITTED — NOT declared; F1 is a fixable defect (scope: clause f value-equivalence
  evasion via code spans). Recommend the L1 weigh whether clause-f hardening belongs in a
  future round's repair list.

Files: run-{va,vb,vb2,vc,vm}.txt (full counter logs), diff-*.txt (variant vs landed entry).
Scratch `/fast/scratch/hyaku/mado-r50/CritC1EntryOverfit` (clone, pins, variants,
gen_variants.py) deleted at finish per spec after receipts copied.
