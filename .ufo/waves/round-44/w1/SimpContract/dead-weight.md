# SimpContract — dead weight in the C1 contract extension and the C2 clause-h delta

w1 / mado round 44. Lane `mado-shokunin`, base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, freeze
`e2289516a9a857f55cda7be635933e89b931c3da`. Lane files read only; **deletions made: none**
(frozen files, leaf seat, no edit scope). **Deletion candidates found: 7 in the C1 contract text,
3 in the C2 clause-h text/code.** One of them (C2-3) is not merely weight: the exemption it
describes is a channel a forged entry can use.

Everything below is measured, not read. The instruments were run in a scratch tree (since
deleted) against the frozen counters at the freeze revision; the scripts that produced every
number travel in this seat dir (§7) and every number quoted here appears in a receipt beside this
file.

---

## 1. Criterion

A sentence of the contract is **load-bearing** iff some input can distinguish a tool that obeys it
from a tool that obeys the rest of the contract and violates it. Two ways a sentence fails that
test, and both were tested the same way — build the pair, run the reference:

- **Entailed** — the violating tool necessarily violates another sentence, so the sentence adds no
  constraint. Proof is a derivation plus the mutant that shows the violation is caught elsewhere.
- **Unobservable** — the two readings are satisfied by the same outputs on every input, so no
  reading of the sentence can be wrong. Proof is a mutant that violates it and still scores
  `TARGET_MET`, plus a structural argument.

Method: one minimal mutant per sentence, scored against the frozen fixture lattice the predicate
actually uses (`quality/counters/c1-r44-geometry-states.py`, nonce `simpaudit`, all 26 cases of
clause f plus the tool's own `--selftest` in the counter's bubblewrap sandbox), then the **frozen
counter end-to-end** on the one mutant the lattice does not see. The judge is the counter's own
extended model, so "the mutant fails fixture X" means the lattice compares the two behaviours and
the fixture wins for the model.

Files and hashes this document reasons about (`receipts-entailment.txt`, last block):

| file | sha256 |
|---|---|
| `quality/counters/c1-r44-geometry-states.py` | `f6b42b05…c614de65` |
| `quality/counters/c2-r44-gkeep-size-request.py` | `5b72c16d…e47860a68` |
| `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` | `8e871a00…34131c788d` |
| `.ufo/waves/round-44/fetch/gkeep-ui.py` | `07a3c4a5…d27fe5d66a` |
| `.ufo/waves/round-44/fetch/Hyprland-Window.cpp` | `d735d454…72211ded` |

---

## 2. The C1 extension, sentence by sentence

Counter docstring (`c1-r44-geometry-states.py` lines 16-25), reference docstring
(`ctl-ref-tool.py.txt` lines 9-16, 54-62, 68-69). E = counter docstring, R = reference.

| id | sentence (fragment) | verdict | evidence |
|---|---|---|---|
| **E1** | fsmode is the `fullscreen` value when it is a JSON integer (not a boolean, not a float) equal to 1 or 2, else 0 | **LOAD-BEARING** | `mut_float` 22/26 (sgen7, sgen11, fsvals0, fsmany0 fail; selftest 89/91); `mut_bool` 22/26 (sgen0, sgen7, fsvals0, fsmany0) |
| **E2** | the enumeration `(absent, null, 0, 3, -1, true, 2.0, "2", lists and objects are 0)` | **ENTAILED** | each of the 10 values falsifies E1's antecedent and yields 0 (receipt §E2); all 10 already drawn by `FS_POOL`/`fsvals0`, so deleting it loses no coverage |
| **E3a** | order: BADSIZE before FULLSCREEN/MAXIMIZED | **LOAD-BEARING** | `mut_badsizeafter` 24/26 (sgen0, fsbad0) |
| **E3b** | order: `FULLSCREEN (fsmode 2)` before `MAXIMIZED (fsmode 1)` | **UNOBSERVABLE** | `mut_swap` **26/26, selftest 91/91**, frozen counter `verdict=TARGET_MET`, clauses `a:1 b:1 b4:1 g:1 r:1`; differential 4088/4088 identical |
| **E3c** | order: state verdicts before TILED | **LOAD-BEARING** | `mut_tiledfirst` 23/26 (sgen11, max0, fsmany0) |
| **E3d** | order: TILED before AGREE | **LOAD-BEARING** | `mut_agreetiled` 24/26 (sgen11, fsmany0) |
| **E3e** | order: `AGREE` before `DIFFER` | **UNOBSERVABLE (inherited from r42, not part of the r44 delta)** | `mut_differagree` 26/26, selftest 91/91; the guards partition the remaining space, so no input sees the order. Not a deletion candidate: it costs nothing and r42 is frozen and out of scope |
| **E4** | The client line is unchanged except for the two new verdict words. | **ENTAILED** by the r42 client-line template that the counter docstring puts in force | violating it is caught (`mut_clientextra` 7/26) *because* it also violates r42's template; the sentence states nothing r42 does not |
| **E5** | the summary carries ` maximized=… fullscreen=…` … exactly when maximized + fullscreen > 0 | **LOAD-BEARING** | `mut_always` 8/26 (18 fixtures); `mut_unmatched` 6/26 |
| **E5b** | the pair sits `between `badsize=<n>` and ` verdict=`` | **LOAD-BEARING but duplicate of the reference template** | `mut_afterverdict` 17/26; the position is already in R's output template (line 67, `badsize=<n>[ maximized=<n> fullscreen=<n>] verdict=<V>`) |
| **E6** | otherwise it is byte-identical to the round-43 line. | **ENTAILED** by E5 + the reference template; **retained: it is the claim clause r tests** | identity check: 500 docs without a `fullscreen` field, extended tool vs r42 model, 0 differing (receipt §E6); clause r exits 0 |
| **E7** | FULLSCREEN and MAXIMIZED clients count as matched and never as differ, so the top verdict rules … are unchanged. | **ENTAILED** by r42's MATCHED definition + E3 + r42's V table | its violation is caught (`mut_statenotmatched` 15/26) but every such tool also breaks r42's rule-conditional MATCHED or E3 |
| **R1** | While a window is maximized or fullscreen the compositor sets its box to the workspace work area or the monitor box … | **GROUNDING** (no input depends on it) | retained: it is the reason the verdicts exist; deleting it leaves E1/E3 unmotivated |
| **R2** | `hyprctl clients -j` carries that internal mode as the integer `fullscreen` (… 0 none, 1 maximized, 2 fullscreen …) | **GROUNDING**; the encoding itself is pinned by E1 | retained; the `eFullscreenMode` enumeration is stated twice (E1's parenthetical names 1 and 2, R2 names 0/1/2) — two authorities for one fact, but each docstring is read alone |
| **R3** | Such a client's reported size says nothing about the rule, so it gets its own verdict instead of AGREE, DIFFER or TILED. | **ENTAILED** by the verdict order (R5/E3) | **candidate** |
| **R4** | TILED claims only that the client is not floating: a pseudo-tiled client … carries no pseudo field … | **NOT A CONSTRAINT** (D3 licence fix), retained | the behavioural half is r42's `TILED (not floating)` unchanged; its factual half holds in the pin (`grep -c pseudo` on `fetch-c1/Hyprland-HyprCtl.cpp` = 0) |
| **R5** | verdict order in the reference docstring (BADSIZE … FULLSCREEN … MAXIMIZED … TILED … AGREE … DIFFER) | same as E3, including the unobservable adjacency | duplicate authority: the counter docstring is the scored one; see §6 |
| **R7** | (the bracketed pair is printed exactly when maximized + fullscreen > 0, so a dump with no maximized or fullscreen matched client prints the round-43 line unchanged) | first clause duplicates E5; second clause **ENTAILED** by the first | **candidate (second clause only)** |

### 2.1 Why E3b is unobservable (the one real finding)

Two independent proofs, because this is the sentence I propose to change:

1. **Structural.** `fsmode` is a function of one field with range `{0, 1, 2}` (`fsmode_of`,
   `c1-r44-geometry-states.py:88-92`). The two tests `fsmode == 2` and `fsmode == 1` are
   therefore mutually exclusive: for every client at most one can be true, so no chain of
   `elif`s can reach the second test after the first fires, and the summary counters are indexed
   by the verdict word, so the permutation cannot move a count either.
2. **Differential.** Reference vs branch-swapped tool over the reachable cross product
   (17 `fullscreen` values × 8 sizes × 4 classes × floating true/false) plus 3000 random
   multi-client docs: **4088 inputs, 0 differing outputs** (`receipts-differential.txt`).

And the frozen instrument does not see it either:

```
PRED-C1-r44: fixtures=26/26 tool=present verdict=TARGET_MET rev=e2289516a9a857f55cda7be635933e89b931c3da nonce=swapaudit
PRED-C1-r44 clauses=a:1 b:1 b4:1 g:1 r:1
```

The tool's own selftest passes 91/91 with the swap — the reference has
`maximized-before-tiled` and `badsize-before-fullscreen` cases (`ctl-ref-tool.py.txt:442,444`)
but no case can exist for FULLSCREEN-vs-MAXIMIZED.

The cost is not hypothetical: `ctl-c1.txt` is built from "13 single-defect variants"; a future
seat adding "MAXIMIZED checked before FULLSCREEN" as a defect control would register a
false-MISSED expectation and could not build one that behaves as expected.

---

## 3. Mutant matrix (evidence for §2)

`mutrun.py` scores a tool file with the counter's own 26 clause-f cases and its own selftest
(nonce `simpaudit`, revision `e2289516…`). `fails=` lists the fixtures that caught the violation.

| mutant | what it violates | fixtures | selftest | caught by |
|---|---|---|---|---|
| `ref.py` (control) | — | 26/26 | 91/91 | — |
| `mut_float.py` | E1 "not a float" (`2.0` → mode 2) | 22/26 | 89/91 | sgen7, sgen11, fsvals0, fsmany0 |
| `mut_bool.py` | E1 "not a boolean" (`true` → mode 1) | 22/26 | 89/91 | sgen0, sgen7, fsvals0, fsmany0 |
| `mut_badsizeafter.py` | E3a (BADSIZE after the state branches) | 24/26 | 90/91 | sgen0, fsbad0 |
| **`mut_swap.py`** | **E3b (MAXIMIZED before FULLSCREEN)** | **26/26** | **91/91** | **nothing; TARGET_MET end-to-end** |
| `mut_tiledfirst.py` | E3c (TILED before the state branches) | 23/26 | 90/91 | sgen11, max0, fsmany0 |
| `mut_agreetiled.py` | E3d (AGREE before TILED) | 24/26 | 89/91 | sgen11, fsmany0 |
| `mut_differagree.py` | E3e (DIFFER before AGREE, inherited) | 26/26 | 91/91 | nothing (partition) |
| `mut_clientextra.py` | E4 (extra `fsmode=` field) | 7/26 | 89/91 | 19 fixtures |
| `mut_always.py` | E5 (pair always printed) | 8/26 | 78/91 | 18 fixtures |
| `mut_unmatched.py` | E5/E7 (count unmapped/unmatched states) | 6/26 | 85/91 | 20 fixtures |
| `mut_afterverdict.py` | E5b (pair after `verdict=`) | 17/26 | 88/91 | 9 fixtures |
| `mut_statediffer.py` | E3/E7 (state client reported DIFFER) | 17/26 | 85/91 | 9 fixtures |
| `mut_statenotmatched.py` | E7 (state clients not counted as matched) | 15/26 | 87/91 | 11 fixtures |

The hint in the ticket that "not a float" might be dead is refuted by measurement: without it,
`2.0` (which arrives in Python as a float and compares equal to `2`) becomes FULLSCREEN and four
fixtures fail. Same for "not a boolean".

---

## 4. Deletion candidates — C1 text (exact text)

None of these can be applied by this seat (frozen files, no edit scope). Each is stated as the
byte-exact current text and its byte-exact replacement.

**D1 — E3b, the FULLSCREEN/MAXIMIZED ordering claim. Priority 1 (it is false precision, and it
traps future defect controls).** In `quality/counters/c1-r44-geometry-states.py:20`, replace

```
BADSIZE (size none) | FULLSCREEN (fsmode 2) | MAXIMIZED (fsmode 1) | TILED | AGREE | DIFFER.
```

with

```
BADSIZE (size none) | FULLSCREEN (fsmode 2) or MAXIMIZED (fsmode 1) | TILED | AGREE | DIFFER
(the two state verdicts are mutually exclusive, so their relative order is not observable).
```

and the same in `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt:58-60` — the two texts must move
together or the reference (a control) states a rule the predicate does not score.

**D2 — E2, the example table. Priority 2.** In `c1-r44-geometry-states.py:18-19`, delete

```
 (absent, null, 0, 3, -1,
true, 2.0, "2", lists and objects are 0)
```

leaving `… equal to 1 or 2, else 0).` It restates E1's closed rule for ten values that clause f
already draws; it is a second statement that can only ever drift from E1.

**D3 — E4. Priority 3.** Delete the whole sentence at `c1-r44-geometry-states.py:21`:

```
The client line is unchanged except for the two new verdict words.
```

r42's template (in force per lines 16-17 of the same docstring) already fixes every field of that
line, and the new verdict words are named by E3. Nothing is lost; `mut_clientextra` still fails 19
fixtures because it breaks r42.

**D4 — E5b, the position clause. Priority 4.** At `c1-r44-geometry-states.py:22`, delete

```
between `badsize=<n>` and ` verdict=` exactly when
```

and keep `The summary line carries ` maximized=<n> fullscreen=<n>` exactly when maximized +
fullscreen > 0`. The position is already exact in the reference template
(`ctl-ref-tool.py.txt:67`) and in the counter's own format string.

**D5 — E7. Priority 5.** Delete the sentence at `c1-r44-geometry-states.py:23-25`:

```
FULLSCREEN and
MAXIMIZED clients count as matched and never as differ, so the top verdict rules (NO_SIZE_RULES,
DIFFER, NO_MATCHING_CLIENT, OK and their exit codes) are unchanged.
```

MATCHED is rule-conditional in r42 and does not look at `fullscreen`; "never as differ" is E3a-E3c;
the top-verdict table and its exit codes are r42's lines 55-56, unmodified.

**D6 — R3, the reference's consequence sentence. Priority 6.** Delete
`ctl-ref-tool.py.txt:14-16`:

```
Such a
client's reported size says nothing about the rule, so it gets its own verdict
instead of AGREE, DIFFER or TILED.
```

R1/R2 already give the reason (the compositor replaced the box) and the order gives the
consequence. *(Tradeoff: this is the most readable one-line rationale in the file; deleting it is
a taste call, not a correctness one. It is listed because it states no constraint.)*

**D7 — R7's second clause. Priority 7.** Delete `ctl-ref-tool.py.txt:68-69`'s tail:

```
so a dump
with no maximized or fullscreen matched client prints the round-43 line unchanged
```

after the first clause `the bracketed pair is printed exactly when maximized + fullscreen > 0`.
"If P then print" makes "if not P then do not print" a restatement, not new information; the
no-harm claim is E6 and it is checked by clause r.

**Kept deliberately (not candidates):** E1, E3a, E3c, E3d, E5, E6 (E6 is the claim clause r
tests — deleting the sentence would orphan the check), R1, R2, R4, and the inherited E3e. R4 is
the D3 licence fix and its factual half is true in the pin; deleting it would reopen D3. R5 is a
duplicate authority with the counter docstring, but the two audiences differ and the scored copy
is unambiguous — reported as a tradeoff, not a defect.

---

## 5. C2 clause h (counter docstring lines 15-25, code lines 386-408, 556-563)

The clause has two kinds of content: **entry constraints** (falsifiable — vary the entry, the
verdict changes) and **instrument bookkeeping** (not falsifiable — the receipts are sha256 pins,
so every recomputed number is a constant). Measured values of the two census lines from the pins
(`host_census` with the entry carrying both lines, `ok=True`):

```
gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
hyprland sendWindowSize xdg_setSize=1 x11_configure=1
```

| id | sentence | verdict | evidence |
|---|---|---|---|
| **H1** | the Gate receipts of the cited ids include gkeep-ui.py and Hyprland-Window.cpp | **ENTAILED** by clause i (`bad |= not set(PINS) <= used`, line 604; both names are in `PINS`, lines 168/171) | retained anyway: it is the only place that says *which* receipts the census reads (the code guard at lines 384-386 needs it to avoid a `KeyError`) |
| **H2a** | with `#` comments removed | **INERT on the pin → candidate** | raw vs stripped give the identical triple: `set_default_size=[('420','500')]`, `application_id=['org.omarchy.gkeep']`, `set_size_request(=0`; the two matching lines (449, 476) carry no `#` |
| **H2b** | the single `set_default_size(W, H)` call … the number N of `set_size_request(` … the single `application_id="<ID>"` | **NOT FALSIFIABLE** (pin constants) | same receipt; "single" is enforced only as `len(sd) != 1 → clause h false`, which no entry can influence. Keep: it is what makes the line a recomputation instead of an authored number (the declared residual) |
| **H3** | and the entry carries `gkeep client default_size=… size_request_calls=… application_id=…` | **LOAD-BEARING** (one of the two things an entry must do) | the only entry-side condition with a varying input |
| **H4** | the body of `void CWindow::sendWindowSize(bool force) {` | **LOAD-BEARING** (scope) | body gives `->setSize(=1 ->configure(=1`; whole file gives `2` and `3` |
| **H5** | up to the first following line that is exactly `}` | **EQUIVALENT to brace matching on this pin → candidate** | first exact-`}` line is line 1754; brace match also ends at 1754; no exact-`}` line strictly inside (1733-1753) |
| **H6** | counts X = `->setSize(` and Y = `->configure(` … and the entry carries `hyprland sendWindowSize xdg_setSize=<X> x11_configure=<Y>` | **LOAD-BEARING** (the second entry-side condition) | the line is one of the two the entry must reproduce |
| **H7** | each line verbatim, outside fences, exactly once, and neither line is a clause-g claim line | first three clauses **LOAD-BEARING**; the fourth **NEVER HAPPENS** for a real census line and is implemented as a broader exemption → **defect** | see below |

### 5.1 H7's fourth clause: no constraint, and the code implements something else

A census line names no `S###` id (checked: `re.search(r"\bS\d{3,}\b", line)` is false for both),
so clause g's `hit` test and `all_body_lines_bound`'s `if not re.search(id, l): continue` skip it
whether or not it is exempt. The sentence describes a situation that cannot occur.

The code, however, exempts by **prefix**, not by membership:

```
    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census_lines
                   and not l.startswith("gkeep client ")
                   and not l.startswith("hyprland sendWindowSize ")]
```

Three measured consequences (`receipts-entrylines.txt`):

1. `l not in census_lines` is **dead**: both census strings start with one of the two prefixes,
   so the `startswith` tests alone exclude them.
2. Removing all three predicates changes nothing for an entry that carries the two lines
   (they are invisible to g either way — verified against both predicates).
3. It **does** change things for a line that starts with a census prefix *and* cites an id: such a
   line is exempt from clause g today, and would be judged (and would fail, having no quote and no
   locator) once the exemption is removed. That is an escape hatch for exactly the kind of forged
   line round 43 admitted 16 times, in a clause with **no positive control**.

**D8 — C2, the exemption. Priority 1 for C2 (it is a hole, not only weight).** In
`quality/counters/c2-r44-gkeep-size-request.py:560-563`, replace

```
    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census_lines
                   and not l.startswith("gkeep client ")
                   and not l.startswith("hyprland sendWindowSize ")]
```

with

```
    entry_lines = [re.sub(r"\s+", " ", l) for l in lines]
```

and delete the clause-h tail `, and neither line is a clause-g claim line`
(`c2-r44-gkeep-size-request.py:25`). No entry that carries the two required lines changes
admission; a prefixed forged line stops escaping clause g.

**D9 — C2 H2a. Priority 2.** Delete `with `#` comments removed ` at
`c2-r44-gkeep-size-request.py:17`, leaving `from gkeep-ui.py this counter computes the single`.
`strip_comments` stays in the file — clause d+ (`quote_in_code`) needs it, which is why the
qualification belongs to clause d and not to h.

**D10 — C2 H5. Priority 3.** Delete ` up to the first following line that is exactly `}`` at
`c2-r44-gkeep-size-request.py:22`, leaving `force) {` and counts X =`. "The body of <signature>"
is already exact, and the two candidate readings agree on the pin (receipt above).

### 5.2 Adjacent, not dead weight (reported, not proposed for removal)

- `set_default_size(W, H)` in H2b does not state that the counter's regex requires `", "` with the
  space and ASCII digits (`set_default_size\(([0-9]+), ([0-9]+)\)`, line 391). A future pin without
  the space makes `len(sd) == 0`, clause h false, with no diagnostic beyond `admitted=0`. Under-
  specified, not redundant.
- The inherited `--- PRED-C2-r43-v2 text (inherited) ---` block still contains the *old* clause h
  (host census: `host rules size=`, `host clients total=`, `gkeep request default_size=`), which
  contradicts the rebuilt one. The precedence sentence at line 27 ("Where the text below says …
  the round-43 host census, read the round-44 values above") reconciles it, and the block is
  provenance explicitly marked as inherited, so **nothing is proposed for deletion here**. Worth
  one pointer word ("superseded") at the head of the inherited block only if the L1 wants it.
- Round-43 closure D6 ("open predicate defects") is not closed by any of the above; see the
  report.

---

## 6. Preserved contract

The candidates in §4 and §5 change no admissible behaviour:

- D1 removes a statement no input can observe; D2-D5, D7 remove statements already made by the
  round-42 contract (in force) or by another sentence of the same paragraph; D6 removes a
  restatement of the verdict order.
- **Every load-bearing sentence stays**: the fsmode rule (all three qualifications), the order
  BADSIZE → state → TILED → AGREE → DIFFER (minus the unobservable adjacency), the summary
  condition, the client line, the top verdict rules and their exit codes, and E6 as the clause-r
  claim.
- C2: the two entry-side conditions, "verbatim/outside fences/exactly once", the body scope, and
  the recomputation-from-pins guarantee stay. D8 only removes an exemption no real census line
  needs and closes a forged-line channel; D9/D10 remove qualifications that cannot change the
  constants (1/1 and 420x500/0/org.omarchy.gkeep).
- Clause f, b, b4, g and r are untouched, so the r44 predicate's teeth are unchanged: after
  D1-D7 the `mut_swap` tool would still pass 26/26, and every other mutant in §3 would still fail
  the same fixtures.

**Tradeoff.** The deletions trade a little standalone readability for the absence of a second
statement: a reader of the counter docstring alone loses the example table (D2), the client-line
sentence (D4), and the position of the new fields (D4) — all recoverable from the reference and
from clause f. The one candidate with a real cost is D6 (R3), which is the most compact rationale
in the reference docstring while stating no constraint. Nothing here needs doing before the data
commit: none of the candidates makes the predicate admit a bad entry or reject a good one, so none
is a `v2` re-registration trigger by itself — **except D8, which is a tightening and should ride
a `v2` freeze rather than the data commit, because tightening a predicate after data would be a
kill-rule violation.**

---

## 7. Repro

The scripts travel with this seat (`mutrun.py`, `receipts.py`, `mut_swap.py`, `verify-quotes.py`
below are in this directory; they read the lane read-only and write only receipts here):

```
cd <seat>
python3 mutrun.py <lane>/.ufo/waves/round-44/c1/ctl-ref-tool.py.txt   # 26/26, selftest 91/91
python3 mutrun.py ./mut_swap.py                                      # 26/26, selftest 91/91  <- the finding
cd <lane> && python3 -I quality/counters/c1-r44-geometry-states.py --repo . \
  --rev e2289516a9a857f55cda7be635933e89b931c3da --tool <seat>/mut_swap.py \
  --nonce swapaudit --work $TMPDIR   # verdict=TARGET_MET, clauses a:1 b:1 b4:1 g:1 r:1
cd <seat> && python3 receipts.py                                     # §E2, §E6, C2 measurements, hashes
python3 verify-quotes.py                                             # 41 quotes, 0 failures
```

`mut_swap.py` is the frozen reference with exactly one change — the two state branches of
`evaluate` swapped:

```
         if size is None:
             verdict = "BADSIZE"
+        elif fsmode == 1:
+            verdict = "MAXIMIZED"
         elif fsmode == 2:
             verdict = "FULLSCREEN"
-        elif fsmode == 1:
-            verdict = "MAXIMIZED"
         elif not floating:
             verdict = "TILED"
```

Receipts in this seat dir: `receipts-entailment.txt` (§E2 entailment, §E6 identity, C2 comment /
body / census / exemption measurements, file hashes), `receipts-differential.txt` (4088 inputs,
0 differing), `receipts-entrylines.txt` (exemption reachability), `receipts-mutants.txt` (the §3
matrix as run).

---

## 8. Quote locators (machine-checked)

Every quotation above is a single-line fragment of its source; `verify-quotes.py` in this seat dir
re-derives each locator with `grep -n`-equivalent search over the source and fails if a quote is
absent from the cited line, spans >25 words, or is missing from this file.

| # | source | line | quote |
|---|---|---|---|
| Q01 | quality/counters/c1-r44-geometry-states.py | 17 | fsmode is the `fullscreen` value when |
| Q02 | quality/counters/c1-r44-geometry-states.py | 18 | (not a boolean, not a float) equal to 1 or 2, else 0 (absent, null, 0, 3, -1, |
| Q03 | quality/counters/c1-r44-geometry-states.py | 19 | true, 2.0, "2", lists and objects are 0). A matched client's verdict is tested in the order |
| Q04 | quality/counters/c1-r44-geometry-states.py | 20 | BADSIZE (size none) \| FULLSCREEN (fsmode 2) \| MAXIMIZED (fsmode 1) \| TILED \| AGREE \| DIFFER. |
| Q05 | quality/counters/c1-r44-geometry-states.py | 21 | The client line is unchanged except for the two new verdict words. |
| Q06 | quality/counters/c1-r44-geometry-states.py | 22 | ` maximized=<n> fullscreen=<n>` between `badsize=<n>` and ` verdict=` exactly when |
| Q07 | quality/counters/c1-r44-geometry-states.py | 23 | maximized + fullscreen > 0; otherwise it is byte-identical to the round-43 line. |
| Q08 | quality/counters/c1-r44-geometry-states.py | 24 | MAXIMIZED clients count as matched and never as differ, so the top verdict rules (NO_SIZE_RULES, |
| Q09 | quality/counters/c1-r44-geometry-states.py | 25 | DIFFER, NO_MATCHING_CLIENT, OK and their exit codes) are unchanged. |
| Q10 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 9 | While a window is maximized or fullscreen the compositor sets its box to the |
| Q11 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 13 | mode as the integer `fullscreen` (FullscreenController.hpp eFullscreenMode: |
| Q12 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 15 | client's reported size says nothing about the rule, so it gets its own verdict |
| Q13 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 16 | instead of AGREE, DIFFER or TILED. |
| Q14 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 58 | is MATCHED and reports a verdict, tested in this order: BADSIZE (size none) \| |
| Q15 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 60 | TILED claims only that the client is not floating: a |
| Q16 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 62 | carries no pseudo field, so TILED does not say which path set the box. |
| Q17 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 68 | (the bracketed pair is printed exactly when maximized + fullscreen > 0, so a dump |
| Q18 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 69 | with no maximized or fullscreen matched client prints the round-43 line unchanged) |
| Q19 | .ufo/waves/round-44/c1/ctl-ref-tool.py.txt | 67 | badsize=<n>[ maximized=<n> fullscreen=<n>] verdict=<V> |
| Q20 | quality/counters/c2-r44-gkeep-size-request.py | 15 | clause h   (rebuilt; the round-43 host census is held knowledge now) the client-side census: |
| Q21 | quality/counters/c2-r44-gkeep-size-request.py | 16 | the Gate receipts of the cited ids include gkeep-ui.py and Hyprland-Window.cpp; from |
| Q22 | quality/counters/c2-r44-gkeep-size-request.py | 17 | gkeep-ui.py with `#` comments removed this counter computes the single |
| Q23 | quality/counters/c2-r44-gkeep-size-request.py | 18 | `set_default_size(W, H)` call, the number N of `set_size_request(` occurrences and |
| Q24 | quality/counters/c2-r44-gkeep-size-request.py | 20 | `gkeep client default_size=<W>x<H> size_request_calls=<N> application_id=<ID>`; |
| Q25 | quality/counters/c2-r44-gkeep-size-request.py | 21 | from Hyprland-Window.cpp it takes the body of `void CWindow::sendWindowSize(bool |
| Q26 | quality/counters/c2-r44-gkeep-size-request.py | 22 | force) {` up to the first following line that is exactly `}` and counts X = |
| Q27 | quality/counters/c2-r44-gkeep-size-request.py | 24 | carries `hyprland sendWindowSize xdg_setSize=<X> x11_configure=<Y>`; each line |
| Q28 | quality/counters/c2-r44-gkeep-size-request.py | 25 | verbatim, outside fences, exactly once, and neither line is a clause-g claim line. |
| Q29 | quality/counters/c2-r44-gkeep-size-request.py | 561 | if l not in census_lines |
| Q30 | quality/counters/c2-r44-gkeep-size-request.py | 562 | and not l.startswith("gkeep client ") |
| Q31 | quality/counters/c2-r44-gkeep-size-request.py | 563 | and not l.startswith("hyprland sendWindowSize ") |
| Q32 | quality/counters/c2-r44-gkeep-size-request.py | 604 | bad \|= not set(PINS) <= used |
| Q33 | quality/counters/c1-r44-geometry-states.py | 88 | def fsmode_of(c): |
| Q34 | quality/counters/c1-r44-geometry-states.py | 16 | The contract extension (the reference is .ufo/waves/round-44/c1/ctl-ref-tool.py.txt; everything |
| Q35 | quality/counters/c1-r42-geometry.py | 52 | float_rule=<on\|off\|-> verdict=<V> |
| Q36 | quality/counters/c1-r42-geometry.py | 55 | V = NO_SIZE_RULES (rules=0; exit 4) \| DIFFER (differ>0; exit 1) \| NO_MATCHING_CLIENT (matched=0; |
| Q37 | quality/counters/c2-r44-gkeep-size-request.py | 168 | "Hyprland-Window.cpp": "d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded", |
| Q38 | quality/counters/c2-r44-gkeep-size-request.py | 171 | "gkeep-ui.py": "07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a", |
| Q39 | quality/counters/c2-r44-gkeep-size-request.py | 391 | sd = re.findall(r"set_default_size\(([0-9]+), ([0-9]+)\)", ui) |
| Q40 | quality/counters/c2-r44-gkeep-size-request.py | 401 | end = src.index("}", k + 1) |
| Q41 | quality/counters/c1-r44-geometry-states.py | 27 | Clauses (all must hold; the counter imports the round-42 counter c1-r42-geometry.py from its own |
