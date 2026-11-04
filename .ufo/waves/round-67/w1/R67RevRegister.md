# R67RevRegister — C1 adversarial review

Axes: calibration C1 (reviewed), operability C2 (unchanged/out of scope).

## Findings by severity

**P1 found and fixed — dangling receipt alongside genuine live receipt.** Initial draft sha256 `d14fcad80922548f8b45225dc824bf69c5b5984aff1f920bf923b07ee78fbd8d` accepted a row containing both the genuine live receipt and an unresolved second receipt, while committed r66 rejected identical input. Executor repaired the fourth-cell invariant. Independently re-exercised final draft `R67ExecRegister/draft/quality/counters/c1-r67-register.py`, sha256 **`58d6c0aba4281ba0c75f653ea0c1fa4d8c90b6450d49b681bec34247eba1c9ec`**: same forgery now rejects with `receipt-unresolved-in-receipt-cell=.ufo/waves/round-65/receipts/not-committed.txt`; canonical lines 169–173 reject dangling fourth-cell tokens. All results below refer to this final SHA. No production edits made by reviewer.

**Specification blocker — predicate sentence does not independently entail two expectations.** `claims-declaration-r67.md` C1's live-path-in-receipt-cell condition is still true for `duplicate-heading` and `row-without-receipt`: both have other rows citing genuine live receipts. Thus their rejection is not entailed by that semantic condition alone. Both ARE explicitly required by the adjacent frozen controls enumeration and inherited r66 structural contract; I agree with their frozen verdicts under the complete declaration. Do not describe the one-sentence live-cell condition as a complete semantic specification. No expectations changed.

## Frozen cases: independent results

| Case | Draft | Frozen | Judgment/evidence |
|---|---|---|---|
| genuine | accept | accept | agree; eight groups, receipt-cell live citation, exact live line |
| duplicate-heading | reject | reject | agree under enumerated structural contract; two headings; sentence-only entailment gap above |
| row-without-receipt | reject | reject | agree under enumerated structural contract; hypr receipt cell is `none`; sentence-only gap above |
| file-plane-only | reject | reject | agree; no live receipt-cell citation and no live object |
| unreferenced-live-object | reject | reject | agree; live object exists but no row receipt cell cites it |
| live-in-state-cell-only | reject | reject | agree; state-cell mention is not receipt-cell citation |

All six `(province, objects)` payloads are pairwise distinct: six SHA256 identities recorded in `R67RevRegister/evidence.json`. File-plane-only versus unreferenced-live-object share province text, but differ in committed-object maps. Genuine fixture is intentionally synthetic, not byte-identical to the real register; the real register was separately accepted at the frozen revision.

## New adversarial inputs

All inputs preserved in `R67RevRegister/forgeries.json`; assessed through the same `assess` used by real mode.

| Input | Draft verdict |
|---|---|
| live path only in heading | reject |
| live cited twice, object lacks exact line | reject |
| live path only in probe cell | reject |
| receipt path with trailing punctuation | **accept** |
| nine rows | reject |
| seven rows | reject |
| live plus unresolved second receipt in same row | **reject — fixed after initial finding** |
| duplicate group via distinct capitalization, replacing waybar with HYPR PLANE | reject |
| sentinel moved above table | reject |
| invented state prose with genuine receipts | **accept — explicit nonclaim** |

Punctuation acceptance is not a defect: the receipt cell still cites the exact live path, with punctuation outside its code span. Invented state prose remains outside C1's claim. Every accepted extra has this reproduction command, substituting the named case:

```sh
R=/home/vgpnk/Projects/shokunin/mado-shokunin
D=$R/.ufo/waves/round-67/w1/R67ExecRegister/draft/quality/counters/c1-r67-register.py
P=$R/.ufo/waves/round-67/w1/R67RevRegister
python3 -I "$P/reproduce.py" "$D" receipt-trailing-punctuation
python3 -I "$P/reproduce.py" "$D" live-plus-unresolved-same-row
python3 -I "$P/reproduce.py" "$D" forged-state-known-nonclaim
```

## Exact measurements

Executed independently (full argv/stdout/stderr/rc preserved in `R67RevRegister/evidence.json`):

```sh
R=/home/vgpnk/Projects/shokunin/mado-shokunin
D=$R/.ufo/waves/round-67/w1/R67ExecRegister/draft/quality/counters/c1-r67-register.py
C=$R/.ufo/waves/round-67/controls/c1-controls.json
S=/fast/scratch/hyaku/mado-r67/R67RevRegister
python3 -I "$D" --selftest
# rc 0; PASS cases=15 failed=0
python3 -I "$D" --repo "$R" --rev 061dc329b598b2723a224b6c7b305b436946ec91 --controls "$C" --scratch-root "$S/counter"
# rc 0; register=accept controls=6/6 headings=1 rows=8 groups=8/8 live-cited=yes TARGET_MET
python3 -I "$R/.ufo/waves/round-67/controls/score-baseline-c1.py" --repo "$R" --base 0b28ffb4baac9586566d246c3f0986b2bb650a33 --controls "$C" --scratch-root "$S/baseline"
# rc 0; correct=4/6; wrong cases are unreferenced-live-object and live-in-state-cell-only
```

The scorer worktree bytes equal its frozen committed bytes; sha256 `595b7a3f1df2f030656c3fe1b4ddbada812f44476308076d92b0191a8943ef22`.

Complete independent exercise command (rc 0):

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-67/w1/R67RevRegister/review.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-67/w1/R67ExecRegister/draft/quality/counters/c1-r67-register.py
```

The first driver invocation failed rc 1 because candidate `assess` returns three values, not r66's two. Driver corrected before successful exercise; no candidate behavior was inferred from this harness failure.

## Live-line bytes and worktree isolation

`git -C "$R" show 061dc329b598b2723a224b6c7b305b436946ec91:.ufo/waves/round-65/receipts/gate-live-r65.txt`: rc 0. Full-object sha256 `676ba88b484e194d4962ee27d07a54b5b7441a8461256b0f3ea0c83d1910e8ed`. Line **65** equals both frozen JSON `live_line` and candidate `LIVE_LINE`, byte-for-byte. Without newline all three hash to `3b9416a549bf3ced25592467588940d6f1755f927b1d168d548246a7701ea34d`; with LF the line hashes to `192bd7ee38048419a46971f24352ae187a66c1a0aa1ef1fef8f18a51c4e41a34`. This is line equality, not a claim that the full multiline receipt equals the one-line fixture stub.

Driver creates its fixture under the mandated scratch, `git -C fixture init -q`, verifies `rev-parse --show-toplevel == fixture` before fetching the frozen commit, then runs the candidate twice. Second run poisons fixture worktree PROVINCE.md and live receipt. Both runs rc 0, stdout and stderr identical. Canonical final source lines 303–310 read PROVINCE and receipts only via `git show REV:path`; the git wrapper scrubs GIT variables and disables replace objects. **Measured register/receipt input does not read worktree bytes.** External `--controls` JSON is deliberately read from its supplied filesystem path; not a claim that the program opens no filesystem input whatsoever.

## Verdict and residual gaps

**C1 finite six-case predicate: sound as bounded, target independently met on final SHA.** Initial actionable dangling-fourth-cell defect fixed and independently verified; no remaining failing forgery among the requested additional inputs. Literal sentence-only semantic entailment remains incomplete as identified above; this does not invalidate the explicit frozen verdict enumeration. This recommendation is not admission or integration authority.

LSP unavailable: `xd://lsp` returns “No such tool”; no semantic references/definition/diagnostics available. Review used direct source inspection and executed behavior, not grep as semantic proof. No claim of universal forgery resistance, state-cell truth, current desktop health, or saturation beyond frozen finite denominator. Integrated production revision was not measured; review is pinned to the draft SHA above against frozen input revision.

Scratch removed by driver `finally: shutil.rmtree(S)`; absence confirmed. No tool installs, no host probes, no lane/fleet git mutation. Only own seat artifacts and the explicitly assigned report path written.

Self-evaluation: accuracy 4 (draft-only, not integrated revision); completeness 4 (no LSP available); clarity 4 (finite-target vs structural distinction requires care); actionability 5 (saved inputs, exact commands and offending source lines); conciseness 4 (evidence necessarily spans several checks). Overall 4.2. Highest-impact remaining action: measure integrated revision and avoid claiming a complete standalone semantic predicate. User should agree with scope-limited assessment.
