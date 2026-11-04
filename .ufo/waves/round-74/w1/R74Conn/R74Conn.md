# R74Conn — one bounded cross-claim proposal

## Axes and shared pattern

Declared axes: **C1 calibration**, **C2 operability**. Navigation, the ledger, held instrument bytes and the 460/460 selftest are no-harm obligations, not additional improvements claimed here (`claims-declaration-r74.md:19-26,92-98`).

Shared pattern: **a control set certifies an instrument only if it separates a named mutation or declared limit of that instrument**. A green aggregate alone does not establish that separation. Round 74 instantiates the pattern against held implementations: C1's four replay negatives distinguish 12/12 from 8/12; C2's four new positive carriers distinguish 36/36 from 32/36. This does not by itself establish independent single-branch mutation coverage.

Evidence below uses paths relative to `.ufo/waves/round-74/` unless otherwise qualified. No instrument or test was executed by this seat.

## Per-case discrimination: what actually separates

### C1

`measurement-c1-r74.txt:6-17` preserves all eight carried expectations and shows the held rule credits each of the four new negatives. `control-baseline-r74.txt:9-12` independently records the same held outcomes. Candidate rule `quality/counters/c1-r74-witness-rule.py:69-81` retains the arithmetic and requires `token is not None and token == nonce`.

| Named missing behavior | Separating case | Evidence and qualification |
|---|---|---|
| Refuse absent witness | **`replay-no-witness`** | Sole frozen case with otherwise-creditable arithmetic and no parsed witness. Emitter `quality/counters/c1-r74-replay-witness.py:108`; measurement line 15. A mutant accepting `token is None` would be separated here [INFERENCE from code, not an executed mutant]. |
| Reject stale captured witness | `replay-captured` | Emitter line 107 supplies frozen `0123456789abcdef`; measurement line 14 fails candidate / passes held. |
| Compare supplied challenge | `witness-mismatch` (also stale replay) | Emitter line 109 supplies `deadbeefdeadbeef`; measurement line 16. Not a sole separator of removing equality altogether. |
| Last parsed witness wins | **`witness-last-wins`** | Emitter line 110 supplies current then wrong token; measurement line 17. Sole frozen case distinguishing first/any-matching witness from last-witness semantics [INFERENCE]. |

**Contradiction to avoid:** if “missing witness check” means deleting the entire final witness requirement, there is no sole separator: all four new negatives separate it. `replay-no-witness` is sole only for the narrower mutation accepting *absence* while retaining equality for present tokens. Also, merely deleting `token is not None and` is not a useful mutant: `None == nonce` already fails for the actual string challenge, so that syntactic deletion is equivalent on this input domain.

Thin evidence: `w1/R74Mutant/` was empty when inspected, so no round-74 mutation receipt was available to substantiate the inferred unique kills. The committed receipt proves fixture outcomes, not a complete mutation matrix. The frozen limit remains: the rule authenticates the echo, not assertion truth, and is not wired into the held round-72 harness (`claims-declaration-r74.md:54-57`).

### C2

`measurement-c2-r74.txt:51-58,88-95` gives the four candidate-positive/base-negative pairs and four candidate/base-correct negatives. Exact fixture sources are `controls/c2-cases-r74.json:173-219`.

| Carrier spelling | Sole new positive exercising that exact spelling |
|---|---|
| Store `r.env[KEY]`, launch `env=cfg.runner.env`, with `r=cfg.runner` | **`twohop-attr-store-dotted-call`** |
| Store `cfg.runner.env[KEY]`, launch `env=r.env` | **`twohop-attr-store-alias-call`** |
| Store via `env=os.environ`, launch `env=dict(env)` | **`environ-alias-call-guard`** |
| Same alias store, launch `env={**env}` | **`environ-alias-splat-guard`** |

At the broad carrier-family level there are **two** positives per family, not one. “Sole separator” is valid only per direction/copy spelling; isolated branch-removal kills remain inferred without a mutation receipt. Negative neighbors cover object-store-after-launch, replacement, absent environment store and alias rebinding.

Thin evidence: the frozen sentence also names a *positive direct* `env=alias` environment launch, but neither new positive uses it. The direct-alias negative fixtures cannot certify that positive acceptance. There is no new environment-alias store-after-launch fixture, nor an object-alias-rebinding fixture, despite those contract conditions. This is bounded fixture coverage, not all carrier/dominance coverage. Source order remains an execution-order approximation, not runtime proof (`claims-declaration-r74.md:87-90`).

## Historical instrument candidates — with explicit exclusions

Read-only history used `git log --all --follow -- <path>`, introduction `git show --stat 906178b6 -- <paths>`, and `git log --all -G 'mutant|mutation|limit.scor' -- quality/check-deliverables.py quality/check-state-cite.py`. The latter returned no matching changes. Local report/lesson and mutation-report sweeps were also searched.

**Two grounded candidates with no mutation-score or limit-score receipt located:**

1. **`quality/check-deliverables.py`**. Introduced at `906178b6` (153 lines). Follow-history: `425d4b2f`, `0bf32603`, `6e8d972b`, `e248a703`, `4f05a4ba`, `906178b6`, `1b37a59e`, `e2ffe818`. Local evidence is prototype/real-report red-green behavior and replay, not a named mutation matrix: `.ufo/waves/round-50/w1/ScrQualityR50/criteria.md:30-32`; `.ufo/waves/round-50/w2/ExecFreezeReplay.md:62-78,200-203`. The latter confirms the reported absent deliverables are real declared-path failures, not checker false positives. Declared-but-unwritten versus actually-written-but-undeclared is a useful boundary, not established mutation scoring.
2. **`quality/check-state-cite.py`**. Introduced in the same commit (160 lines). Follow-history: `4f05a4ba`, `906178b6`, `1b37a59e`, `e2ffe818`. `.ufo/waves/round-50/w1/ScrQualityR50/criteria.md:25-28` supplies read-only-cite red and setter greens; `.ufo/waves/round-50/w2/ExecFreezeReplay.md:99-103` identifies an unavailable claims-file command, so even receipt replay has a named substrate limitation. No mutation/limit-score receipt surfaced in the searched local material.

**Epistemic bound:** these are “no located scoring evidence,” not proof that scoring has *never* happened anywhere. Git path history alone cannot prove that universal negative, because mutation receipts can live elsewhere. Do not publish an unqualified “never mutation-scored” claim from this sweep.

Two suggested candidates are positively **ineligible** for that wording:

- `quality/check-freeze-order.py`: `.ufo/waves/round-55/w2/R55W2MutFreeze/mutants.md:1-49` records 17 mutants, 12 selftest kills, one additional real-run kill, four survivors. Its unrelated C1 harness killed none, explicitly because it never runs this checker (`:19-21`). Follow-history reaches `3c868d82`/`9214b528`, with landing `ebd66fbf`; the historical mutation receipt is decisive contrary evidence.
- `quality/check-control-receipts.py`: `.ufo/waves/round-25/a3w2/reports/MutQ36Checker.md` and `.ufo/waves/round-26/quality/q36-mutants.txt` already hold mutation work; follow-history includes successor landing `1b0b91e9` and `b6650d58`. Round-26 registration `:101-103` expressly routes the surviving round-25 mutants. It cannot be called never mutation-scored.

## Sibling overlap

Read-only sweep of sibling `PROVINCE.md` and `SKILL.md` (excluding mado), plus exact round-74 terms across the fleet:

- **Challenge/run binding already has sibling ground:** `kaidoku-shokunin/PROVINCE.md:530` names `--challenge`/`--nonce-commitment`, `run_nonce`, binding to instrument digest and packed pins, genuine acceptance and transplant/wrong-nonce/broken-binding rejection. This is an analogous bounded replay defense, expressly not cryptographic authenticity; not ownership of mado's landing grammar.
- **Independent execution witness already has sibling ground:** `kama-shokunin/SKILL.md:1536,1564-1565` binds server identity, model and observer-chosen nonce outside the replay. Fleet `.ufo/reports/round-49/kama.md:20-21,52` corroborates the declared capability. This is stronger process observation, not evidence that mado's echo authenticates assertion truth.
- **Guard-carrier ownership:** sweep for guard census/carrier, two-hop alias and `os.environ` alias in sibling routing/ownership surfaces found none. This is a scoped negative, not a claim about every sibling implementation byte.

## One bounded proposed move

**Draft a per-clause separator matrix alongside the existing receipts, with exact mutation/limit, separating case IDs, and an explicit empty cell when no case certifies a clause.** Do not change either frozen denominator, instrument, admission result or held harness this round. Reuse the same matrix form for the two historically unscored-evidence candidates above rather than reusing an unrelated green harness.

Expected affected axes [INFERENCE]: calibration improves through narrower supported claims; operability improves through explicit diagnosis of missing carrier coverage. Navigation/ledger/runtime semantics need not change because this is an evidence companion, not another execution route. No measured axis improvement or admission is asserted by this proposal.

Second-order effects: runtime echo is separated from truth/process observation; contract prose distinguishes exact carrier spellings from broad families; substrate binds every row to the frozen revision/control digest; verification names the actual detector instead of treating any green harness as relevant. The freeze-checker history demonstrates why the last distinction matters.

Risks: relabeling inferred unique kills as observed kills; silently expanding the frozen 12/36 populations; importing sibling cryptographic/process guarantees into an echo-only rule; interpreting no-found history as universal absence. Keep these contradictions explicit.

Proposed verification for L1, not run here: inspect a receipt-backed one-branch mutation matrix for absent-witness acceptance, first/any-witness acceptance and each of the four C2 spellings, with pristine parity and isolated-mutant case differences. Require an explicit gap for positive direct `env=alias` rather than claiming it covered. Any future added case belongs to a newly frozen denominator. Preserve the declared 460/460, held bytes, ledger and navigation obligations before any integration.

## Posture and output

Only this report was written; committed receipts and instruments were read, not rewritten. No tools installed, no host/session/network probes, no git/jj mutations, no other runtime or subagent invoked. The explicitly created scratch `/fast/scratch/hyaku/mado-r74/R74Conn/` was unused and removed before handoff. The conflicting generic request for a sibling-level `.ufo/waves/round-74/w1/R74Conn.md` is not followed: the stricter seat write-directory bound and explicit requested `R74Conn/R74Conn.md` path control.
