# ReviewPresent: C1 strictness beyond the counter (round-23, wave 2)

Seat: MadoR23.ReviewPresent (leaf reviewer, no dispatch). Lane tip checked: `2f1134f38930fc8b067d2d7f5bba126338faabdd`
(C1 classifier from `2e592aff`; `tools/mado-tripwire.py` unchanged at tip). Base: `e33ea30461f6e9bbeee40beef19770a953f7a105`.
Nothing in the lane was edited. Receipts are in `/fast/scratch/hyaku/mado-r23/w2/ReviewPresent/` (section 8).

## Verdict

- **Scoped check, 2 present + 10 exact frozen cases: holds.** Zero of the 12 counter-passing cases are weaker than base.
  On all 12 at tip: every `pacman -S` row is `host_mutation`, no row lies outside the truth-executed set, and unparsed is 0.
- **Beyond the frozen set: C1 is not operable as claimed.** At tip, a callback passed to a helper that the follow limits
  refuse (the call sits in the fourth nested helper body, or comes after 2000 helper descents in one cell) is silently dropped.
  The file comes back clean (no row, unparsed 0, exit 0). Base reports the same executed `pacman -S` as a lead with exit 1.
  The frozen counter cannot see this because no frozen case reaches that depth. Finding B (closure cells rebound after
  escape) gives wrong leads and clears base's unparsed signal.
- **Recommendation to L1 (advice, not an edit):** do not cite 12/12 as operability evidence until Findings A and B are
  adjudicated against truth and the registered guards are shown to exercise the same paths.

## 1. Inputs (identities verified)

| Input | Identity | How verified |
|---|---|---|
| Tip classifier | sha256 `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009` | `git show 2f1134f3:tools/mado-tripwire.py` into scratch `tool.py`. `git show 2e592aff:...` has the same sha. |
| Base classifier | sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` | Copy of `round-23/evidence/tool-base-cd9da20c.py` into scratch `base.py`. `git show e33ea30:tools/mado-tripwire.py` has the same sha. |
| Round-21 scan helper | sha256 `4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da` | Loaded unchanged with runpy; `scan(tool, fixture)` is the counter's own helper. |
| Frozen expectations | sha256 `53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9` | Checked by the counter's `verify()`; every fixture sha checked. |

Copies were used so no `__pycache__` is written into the lane. Child interpreters wrote only scratch pyc files.

## 2. Commands run (all `python3 -I`, one child at a time, helper caps 384 MiB / 15 s)

```
python3 -I .ufo/waves/round-23/repair/measure.py --tool <scratch>/tool.py     # tip  -> 12/12  receipt-counter-tip.json
python3 -I .ufo/waves/round-23/repair/measure.py --tool <scratch>/base.py     # base -> 6/12   receipt-counter-base.json
python3 -I .ufo/waves/round-23/repair/truth.py                                # truth 12/12    receipt-truth.json
python3 -I <scratch>/strict_check.py          # scoped strict pass (tip vs base, full payloads)   strict-results.json
python3 -I <scratch>/probes.py                # probe set 1 (14 fixtures in <scratch>/probes/; 25 across the four probe batches)  probes-results.json
python3 -I <scratch>/probes2.py               # depth and budget variants                     probes2-results.json
python3 -I <scratch>/probes3.py               # container variants                           probes3-results.json
python3 -I <scratch>/probes4.py               # stale closure-cell controls                  probes4-results.json
python3 -I <scratch>/mutant_check.py          # diagnostic mutant mutA against counter and probes  mutant-check-results.json
```

Probe truth is the executed-argv set from truth.py's own recording CHILD and safety check, loaded with runpy and not
re-implemented. Probe fixtures are my own, in the repair-set JSONL format. The lane's `git show` and `git diff` calls were read-only.

## 3. Scoped results: 12 frozen cases

| Case | Kind | Counter tip / base | Tip rows (class, evidence, command) | Base rows | Unparsed base to tip | Tip vs base | Weaker than base? |
|---|---|---|---|---|---|---|---|
| CallbackStoredInDict | present | pass / pass | host_mutation, lead, `pacman -S r23-hook-dict` | identical | 0 to 0 | none | no |
| CallbackStoredOnAttribute | present | pass / pass | host_mutation, lead, `pacman -S r23-hook-attr` | identical | 0 to 0 | none | no |
| ReturnedGlobalHelper | exact | pass / pass | package_query, observed, `pacman -Q r22-nhb-module` | identical | 0 to 0 | none | no |
| CallerArgumentBeforeClosureOverlay | exact | pass / pass | package_query, observed, `pacman -Q r22-callsite-argument` | identical | 0 to 0 | none | no |
| ReturnedGlobalCallableShadow | exact | pass / fail | package_query, observed, `pacman -Q r22-global-callable` | + host_mutation lead `pacman -S r22-foreign-callable` (truth: never runs) | 0 to 0 | FP dropped | no |
| ForwardExistingClosureWithoutFrameContamination | exact | pass / fail | package_query, observed, `pacman -Q r22-forward-global` | identical | 1 to 0 | unparsed_spawns 1 to 0 | no (truth agrees) |
| ForwarderInvokesCallback | exact | pass / fail | package_query, observed, `pacman -Q r23-forward-global` | host_mutation observed `pacman -S r23-forward-foreign` (truth: never runs) | 1 to 0 | FP dropped, truth row added | no (truth agrees) |
| CallerLocalShadowsHelperGlobal | exact | pass / fail | package_query, observed, `pacman -Q r23-local-global` | host_mutation observed `pacman -S r23-local-foreign` (truth: never runs) | 0 to 0 | FP dropped, truth row added | no |
| NestedDefReadsDefiningFrame | exact | pass / pass | package_query, observed, `pacman -Q r23-nested-local` | identical | 0 to 0 | none | no |
| LateGlobalRebinding | exact | pass / pass | package_query, observed, `pacman -Q r23-late-global` | identical | 0 to 0 | none | no |
| ForwarderPassesCallerArgument | exact | pass / fail | package_query, observed, `pacman -Q r23-forwarded-argument` | identical | 1 to 0 | unparsed_spawns 1 to 0 | no (truth agrees) |
| ForwarderInvokesFactoryClosure | exact | pass / fail | package_query, observed, `pacman -Q r23-closure-captured` | identical | 1 to 0 | unparsed_spawns 1 to 0 | no (truth agrees) |

Full-payload comparison (rule, argv0, line, evidence, tool-call id, timestamp, file sha, line and call counts, unparsed)
shows only these differences. Removed rows are three host_mutation rows that the truth says never run. Added rows are two
truth-executed package_query rows. Four unparsed_spawns drops, each matching the truth set. No truth-executed row was dropped.
No class or evidence downgrade occurs anywhere. Both present cases are identical to base.

Stricter properties at tip (the counter does not enforce them for present cases):

| Property | Present (2) | Exact (10) |
|---|---|---|
| `pacman -S` rows are `host_mutation` | 2/2 (rule `pacman:-S`, evidence lead) | no `-S` row at tip; base had 3 `-S` false positives, all removed |
| No row outside the truth-executed set | 0 extra | 0 extra (exact equality, counter-enforced) |
| Unparsed = 0 | 2/2 | 10/10 |
| Forbidden target as substring at any tier | n/a | 0 hits |
| Oracle self-check: wants equal truth | present wants contained in truth 2/2 | exact wants equal truth 10/10 |

Result: 0 of 12 counter-passing cases are weaker than base.

## 4. Supplementary probes outside the frozen set (my fixtures; truth from truth.py's CHILD)

| Probe | Truth executed | Tip (rows, unparsed, exit) | Base | Mutant mutA (diagnostic) |
|---|---|---|---|---|
| chain_n2 (control) | `pacman -S probe-chain-n2` | observed, 0, 1 | observed, 0, 1 | observed |
| chain_n3 (control) | `pacman -S probe-chain-n3` | lead, 0, 1 | lead, 0, 1 | lead |
| chain_n4 | `pacman -S probe-chain-n4` | **none, 0, 0** | lead, 0, 1 | lead |
| chain_n5 | `pacman -S probe-chain-n5` | **none, 0, 0** | lead, 0, 1 | lead |
| chain_n6 | `pacman -S probe-chain-n6` | **none, 0, 0** | lead, 0, 1 | lead |
| chain4_kw | `pacman -S probe-chain4-kw` | **none, 0, 0** | lead, 0, 1 | lead |
| realistic_stages | `pacman -S probe-realistic-install` | **none, 0, 0** | lead, 0, 1 | lead |
| budget_2000 | `pacman -S probe-budget` | **none, 0, 0** | lead, 0, 1 | lead |
| chain4_direct (control) | `pacman -S probe-chain4-direct` | observed, 0, 1 | observed | observed |
| chain4_global (control) | `pacman -S probe-chain4-global` | lead, 0, 1 | lead | lead |
| escape_then_rebind_registry | `pacman -S probe-reg-b` | lead `pacman -Q probe-reg-a` (never runs), **0**, 1; real command missed | none, **1**, 0 | = tip |
| escape_then_rebind_called | `pacman -S probe-cell-b` | observed S (correct) plus lead `pacman -Q probe-cell-a` (never runs), 0, 1 | observed S, **1**, 1 | = tip |
| escape_after_rebind (control) | none | lead `pacman -S probe-ctl-b`, 0, 1 | none, 1, 0 | not run |
| escape_no_rebind (control) | none | lead `pacman -Q probe-ctl-c`, 0, 1 | none, 1, 0 | not run |
| param_reassigned | `pacman -Q probe-other` | observed Q (correct) | observed Q plus lead S (false positive) | = base |
| factory_arg, keyword_callback, passthrough_n2, passthrough_n6, reg_mutated_in_helper, reg_mutated_module, reg_mutated_and_called_inside, reg_literal | as shown in `probes*-results.json` | equal to base | equal to base | equal to base |

### Finding A (high): silent false negative for an executed host command

Reproducer `probes/realistic_stages.jsonl` (truth: `pacman -S probe-realistic-install`):

```python
import subprocess
def run():
    subprocess.run(["pacman", "-S", "probe-realistic-install"])
def invoke(fn):
    fn()
def stage3():
    invoke(run)
def stage2():
    stage3()
def stage1():
    stage2()
def main():
    stage1()
main()
```

Tip: no rows, unparsed 0, exit 0 (clean). Base: `host_mutation|lead|pacman -S probe-realistic-install`, exit 1.

- Boundary: when the callback-receiving call sits in the fourth nested helper body (depth 4), or after 2000 descents
  in one cell (`budget_2000`), or with a keyword argument (`chain4_kw`), the command disappears. A depth-3 chain
  (`chain_n3`) keeps a lead; [INFERENCE] because there the refused call is the callback's own call, so its body is swept.
- Mechanism (tip line numbers in `tool.py`):
  1. `follow_helper` refuses when `depth >= DESCENT_LIMIT` (4, line 2410) or `descents >= DESCENT_BUDGET` (2000, line 2411): lines 2631–2632.
  2. The reference loop skips the callback when `reference_escapes` says the receiving call only calls it (lines 2971–2972).
     `reference_escapes` (lines 2527–2555) checks that the callee is visible, that the argument binds (lines 2553–2554), and that
     the parameter does not escape (line 2555). It does not check the depth, budget or recursion conditions that `follow_helper` applies.
  3. The refused callee falls back to `sweep_body` (lines 2806–2808). That sweep binds its parameter as opaque
     `{"kind": "parameter"}` (line 2583), so the call emits nothing and counts no unparsed spawn.
  4. Result: the callback is neither followed nor swept. The module docstring says a clean verdict does not mean no host command
     ran and that non-literal spawn arguments are counted as `unparsed_spawns`; this callback call is neither counted nor reported.
- Causal check: scratch mutant `mutA.py` (line 2971 replaced by `if False:`, so every callable reference is swept; scratch only,
  not a proposed fix). It restores the lead for all six silent probes. It also breaks the frozen set: the counter gives 10/12 on
  mutA, because `ReturnedGlobalCallableShadow` regains its foreign lead and `ForwarderPassesCallerArgument` regains unparsed 1.
  So the skip is needed for the frozen repairs, and a narrow fix would have to skip only when the receiving call will actually
  be followed. I did not build or test that fix.

### Finding B (medium): closure-cell free names read the escape-time value

- `escape_then_rebind_registry`: the cell is rebound after the closure is appended to a list, and the list entry is then called.
  Tip reports a lead for the stale value `pacman -Q probe-reg-a`, unparsed 0, and misses the real `pacman -S probe-reg-b`.
  Base reports no row and unparsed 1.
- `escape_then_rebind_called`: the closure is appended, the cell rebound, then the closure called. Tip reports the correct
  observed row plus a stale lead for `pacman -Q probe-cell-a`, which never runs, with unparsed 0. Base reports the observed row
  with unparsed 1. So tip adds a false row where base had none.
- Controls indicate that the swept lead reads the cell as it stood at the escape statement: rebinding before the escape gives the
  late value (`escape_after_rebind` gives `probe-ctl-b`), while no rebinding gives the escape-time value (`escape_no_rebind`
  gives `probe-ctl-c`).
- Mechanism, [INFERENCE] from the controls: `scope_entry` snapshots a scope only at call and reference statements, and `sweep_body`
  reads that snapshot via `scope_view`. Assignments after the last such statement are invisible to the sweep, which would explain
  the stale value. The mutant gives identical rows, so this is not the skip.
- Consistent with the tool's contract: a wrong value is reported with unparsed 0, so the accounting that base kept (unparsed 1) is lost.

### Probes that are not findings

- Container mutated in a followed helper (`reg_mutated_in_helper`, `reg_mutated_and_called_inside`, `reg_mutated_module`, `reg_literal`): tip equals base.
- `param_reassigned`: tip is correct and removes base's false lead.
- `factory_arg`, `keyword_callback` in a shallow chain, `passthrough_*`: tip equals base.

## 5. Counter observations and advice (no edits made)

1. **The present-case rule is weaker than the stricter properties.** `repair/measure.py` lines 46–48 accept any `observed|lead`
   row of the wanted command, with no class check, no unparsed check and no extra-row check. A regression to `package_query`
   or with unparsed greater than 0 would still pass. Consider an append-only refinement for present cases: `host_mutation`,
   rule `pacman:-S`, unparsed 0, and no row outside the truth set.
2. **The frozen set does not exercise these paths.** No frozen case has helper depth 4, a budget case, or a rebinding after escape.
   Consider a companion set containing Finding A (`realistic_stages`, `chain_n4`, `chain4_kw`, `budget_2000`) and Finding B
   (`escape_then_rebind_registry`, `escape_then_rebind_called`), with truth from truth.py's CHILD and expected verdicts
   that match truth.
3. **Fix direction for A (untested):** make `reference_escapes` return True when `follow_helper` would refuse the receiving call
   (depth at or above the limit, descents at or above the budget, or callee already on the stack). This keeps the skip for
   followed calls, so the two frozen repairs should survive (prediction, unverified).
4. **Fix direction for B (untested):** names rebound after the escape point should yield unparsed (as base did), or the escape
   sweep should read the defining scope at sweep time.

## 6. Residual risk and verification gaps

- **Not run by me:** round-22 primary 57/57, round-21 oracle 35/35 and 17/17, precision 166/175, the eleven selftest suites,
  the 1356-file corpus comparator and the resource guards. I do not know whether their populations contain depth-4, budget or
  post-escape-rebinding patterns. If they do not, they cannot detect A or B. The ReCorpus seat is the natural place to check.
- The probe set is 25 hand-authored fixtures, not a corpus measurement. How often A or B occurs in real transcripts is unknown.
- Present cases remain at lead tier at base and tip, although truth executes them deterministically. This is the registered rule
  and not a regression.
- The four frozen unparsed drops are truth-consistent. They rely on the same escape and scope machinery as B, so their
  correctness does not establish the general case.
- I did not verify the tip's escape analysis beyond these probes.

## 7. Installs and updates

None. Only python3 (stdlib) and read-only git were used. No pacman, sudo, package or service changes.

## 8. Receipts (scratch: `/fast/scratch/hyaku/mado-r23/w2/ReviewPresent/`)

- `strict_check.py`, `strict-results.json`: scoped strict pass (12 cases, tip and base).
- `receipt-counter-tip.json` (12/12), `receipt-counter-base.json` (6/12), `receipt-truth.json` (12/12).
- `probes.py` and `probes-results.json`; `probes2.py` and `probes2-results.json`; `probes3.py` and `probes3-results.json`;
  `probes4.py` and `probes4-results.json`; fixtures `probes/*.jsonl` (`probes-manifest.sha256`).
- `mutA.py` (diagnostic only, sha256 `054a83ad599d07d119db18b1eb3646ca327af2256ba5c253d5ebcd748757686`),
  `mutant_check.py` and `mutant-check-results.json`.
- `tip-vs-base.diff` (`git diff e33ea30 2f1134f3 -- tools/`, 472 lines); `scripts-manifest.sha256`.

Verdict: scoped C1 strictness holds on the 12 frozen cases (0 counter-passing cases weaker than base). The landed tip is not
operable beyond them: a silent `host_mutation` false negative (Finding A) and stale closure-cell evidence that clears unparsed
(Finding B). Recommend that L1 not claim C1 operability until A and B are adjudicated.
