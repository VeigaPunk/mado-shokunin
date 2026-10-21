# FinalRemovalReview — round-21 removal-side adjudication check

Seat: MadoR21-2.FinalRemovalReview (author-lane advice, not independent promotion or admission).
Scope: the removal/false-positive side of the round-21 corpus adjudication and its raw receipt. Read-only over committed evidence; no corpus or VCS payload rerun; no production edits. Peer-note acknowledged: C1 binding falsification is FinalBindingReview's finding, not mine; nothing here re-judges it.

## Identity and hash chain (all verified against working-tree bytes)

| Object | sha256 / value | Match |
|---|---|---|
| lane HEAD | `a6cef8984d3815775587ab634ce558e13338b0eb` | ✓ |
| `tools/mado-tripwire.py` (after tool) | `46c82902896da0ec0ebd54254b1891667fa5da48f8cb297ee08bfb337e34c8c1` | = `after_tool_sha256` = every suite `SELFTEST_SCRIPT_SHA256`; also `git show a6cef89:tools/mado-tripwire.py` hash — the delivered tool is the committed measured revision ✓ |
| `.ufo/waves/round-21/evidence/tool-before.py` | `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458` | = `before_tool_sha256` ✓ |
| `.ufo/waves/round-21/corpus/compare.py` (runner) | `60cef7bebe6eef0bbf09448fec70f1b55375b5f511aad4c968dc22ee4036a653` | = `runner_sha256` ✓ |
| `corpus-final-a6cef89.json` receipt file | `57eb2590cff07fae9044f355ffeedc6028c64f9da805418e7922ed33bd56d803` | = adjudication `receipt_sha256` ✓ |
| `corpus/snapshot/manifest.json` | `8e1cf206c85563b418630ef1d094559a9522431ff4e077ca1b51f249436a1377` | = `manifest_sha256` = the constant pinned inside `compare.py` (`MANIFEST_SHA`) ✓ |
| fixtures pin | `6a7d9ca0d2124a4077074b800c94a9bc1184441c` | adjudication `pure24_final.pin` = `guards-legacy-a1e1b60.json` `fixtures_rev` ✓ |
| population | 1356 manifest paths; before/after run arrays 1356 rows each | ✓ |

`compare.py` integrity is real, not decorative: it verifies every file sha from the manifest before scanning, re-verifies the manifest after scanning, checks tool sha stability during the run, per-finding `file` attribution, population order, and errors exit `int(bool(errors))`.

## Raw comparator honesty (exit 1, not all-input green)

The raw `stdout` diff reconciles exactly:

- **108 error pairs** = 20 `RecursionError` + 1 `TimeoutError` (per-file 15 s deadline) + 86 `CouldNotEvaluate` (≈79 `unknown record shape` on non-transcript `fetch/*/receipts.jsonl` and `CorpusRuntime` run logs, `malformed.jsonl` invalid line, `agent.db.jsonl` refused name, `fixtures2/float_inf_field`, `deep_json_line`) + 1 before-only `MemoryError`.
- **107 pairs identical before==after**; **1 improvement**: `AdvCrash/fixtures/huge_many_stmts.jsonl` before `MemoryError:` → after evaluable, `findings: 0`, `eval_calls: 1` — correct output (5000 int assignments spawn nothing). `improved_allocation_failure: 1` verified.
- `new_error_flips: []` verified independently: 0 pairs where before was clean and after errored.
- exit 1 is the errors signal, not finding diffs. The framing "108 error-bearing pairs explicit; not a green all-input evaluation" is accurate.

Diff rows: removed 31 (26 lead + 5 observed); added 104 (102 observed + 2 lead) across 60 distinct paths; retained 836. The 5 removed observed rows are exactly: `reset_cell` line 3 (demoted to lead), `Z-kwonly`/`Z-named` (command corrected), `git-add--dry`, `git-push--dry` (removed). The 31 adjudication groups match the removed side; the adjudication does **not** itemize the added side (see limitations).

## Attacked slices — independent source inspection (inert snapshot reads; nothing executed)

**1. B14 callbacks (both fp removals sound).**
- `b14_called_real_spawner`: `run_all(subprocess.run)` → `subprocess.run('q', ['pacman','-Q','wayland-utils'])`. In CPython the second positional is `bufsize` (a list) → `TypeError` before any process; the pacman vector is never an argv. Tool models first-positional argv only → `findings: []`, `unparsed_spawns: 0`. Correct.
- `b14_called_spawner`: `spawn(argv)` invoked with two positionals; `bind_literal` returns `None` on arity overflow (`len(values) > len(params) and vararg is None`) → binding fails before the body; in-body `subprocess.run(argv)` is kept visible as `after_unparsed_spawns: 1`. No pacman process possible; nothing excused silently.
- Precision twin `L-AdoptW2-AdvHelperFn-b14` defines `run_all` and never calls it — nothing executes; the legacy lead want is stale, not a lost finding.

**2. Dict-splat defaults (both binding corrections correct).**
`h(**{"argv": ["pacman","-S","advdepth-pkg"]})` overrides the default in both the positional-or-keyword and kwonly forms: `bind_literal` binds `**`-expanded keys into `keyword_params` before defaults are applied, and an unbound kwonly param without default aborts the follow (conservative). Old tool reported the invented default `pacman -S other`; new reports the actual `pacman -S advdepth-pkg`, same class/rule/evidence. This is a factual correction of a wrong old finding, not concealment.

**3. Reset (removals and demotion grounded in real kernel semantics).**
After tool tombstones reset bindings as `reset_unbound` (before tool deleted them yet still reported spawn-named attrs `observed` — the old defect). Real omp eval kernel reset wipes the namespace before the cell runs, so:
- 5 reset-cleared-helper removals verified at source: `CaseLeadsInvisible` (helper cleared by reset; its body's `subprocess` never imported anyway), `CasePureCrossCell` (helper cleared **and** body only `join`s — never spawns, doubly safe), `TwRuleB` (body is `print`, never spawns). No real process loss; only stale lead wants die.
- `reset_cell` line 3 `subprocess.run(['pacman','-S','z'])` under `reset:true` → import cleared → guaranteed `NameError` → demoted observed→lead. Correct direction; intent still surfaced as lead, and the new lead row appears in the raw diff as expected.

**4. Default-lambda override (one real catch, one honest removal).**
- `helper_lambda_default`: `f()` invokes the pacman-bearing default lambda → upgraded lead→observed. The old tool **under-reported a real spawn**; this relabel catches it. Verified at source.
- `helper_lambda_default_call`: supplied `g` replaces the default; pacman never runs (removal correct). The replacement runs `rm -rf /`, which is not a tracked rule and is explicitly disclaimed ("not a claim that the replacement command is harmless"). Honest scoping.

**5. git `--dry` removals (tool behavior verified, gap closed in final revision).**
`git_prints_or_simulates` accepts `--dry` as the unique prefix of `--dry-run` for add/push (`f.startswith("--dry") and "--dry-run".startswith(f)`); abbreviated negations (`--no-dry`) keep the finding; `-n` exempt add/push but is `--no-verify` for commit. W2's `AtkGitAddDry.md` had measured `git add --dry new.txt` still a write at the earlier candidate tool (`2e152f6d…`, commits `f499a8db`/`843d301`) — the final tool closed exactly that counterexample. Both corpus fixtures verified at source.

## Legacy precision 175 → 166: all 9 disagreements direction-classified

`precision-legacy-a6cef89.json`: 175 cases, 166 pass, 9 fail. Every failure's source inspected:

- **3 L-family** (`CasePureCrossCell--reset-lead`, `CaseLeadsInvisible--reset-cleared-helper`, `AdvHelperFn-b14`): wants demand lead markers on calls that cannot execute post-reset (or are never called). No real process loss; loss is lead-level intent visibility only.
- **1 W-family** (`CaseWrapperForms--class-method-instance`): want clean, got observed `pacman -Q` — source is `Runner().run(['pacman','-Q','hyprland'])`, which **really spawns**. The legacy want is factually wrong; the new finding is a recall gain that breaks a frozen want. This item must never be cited as harm.
- **5 H-family** (`commit-dry-run`, `pct-bash-dry-runs`, `p33-git-dryrun`, `git-commit-a-dry-run-short`, `jj-var-verb-help`): all conservative over-reports — `git commit` is a write regardless of `--dry-run/--short/--porcelain/-z` (early `return False` for commit in `git_prints_or_simulates`), and `jj $c --help` with an unresolved variable verb stays `jj:$c` (config alias could forward `--help`). Direction-safe precision cost; this is the "strict commit/index-write boundary" disagreement, deliberate and documented in code comments if not in the docstring.

So "Legacy 175 now 166, unchanged wants" is count-accurate and none of the 9 hides a real loss; one of them is a new correct finding.

## VCS fp 26 vs 20 — not universally proven

- **26 is receipt-backed**: `guards-legacy-a1e1b60.json` `vcs_fp: 26` over the frozen 74-fixture VCS population at fixtures_rev `6a7d9ca0`, with the full file list.
- **20 is narrative only**: it appears in `w1/reports/ScribeKnowledge.md:55` as a "bounded historical result"; I found **no final receipt** in `.ufo/waves/round-21/evidence/final/` recording `vcs_fp: 20` at `a6cef89`. The 26→20 improvement is not independently re-measured in the final evidence set.
- Even taking 20 at face value: one frozen population, five live H-family dry-run/verb over-reports, and `AtkGitAddDry`'s own scoping ("not a claim that every Git abbreviation or environment-dependent parse is modeled") mean counts alone must not be read as universal VCS no-harm.

## Defects and limitations found

1. **Stale docstring vs strict-commit code** (documentation defect, shipped tool): `tools/mado-tripwire.py` ~lines 110–120 still describe `git commit` with `--dry-run/--short/--porcelain/--long/-z` as exempt and say "`commit --dry-run` … neither moves a ref, the index or the worktree", but the code returns False for **every** commit before the dry logic (making commit's `GIT_DRY_NEGATIONS` entry and the commit branches of the dry loop unreachable). Measured behavior follows the code (legacy H failures; selftests pass against the code). The docstring should be corrected to the strict-commit boundary.
2. **Added side unitemized**: the adjudication inventories its 31 removed/relabelled groups but not the +102 observed / +2 lead additions outside those groups (60 distinct added paths, e.g. the new lead on `AdvRecallShapes/fixtures/ar06-gather-inside-main.jsonl`, `pacman -Q w2shape2`). Direction-safe (additions can only widen detection) but not individually adjudicated.
3. **vcs_fp=20 unreceipted** at the measured commit (gap above).
3b. The unitemized `ar06-gather-inside-main.jsonl` lead was verified at source: `asyncio.gather(create_subprocess_exec('pacman','-Q','w2shape'), create_subprocess_exec('pacman','-Q','w2shape2'))` — the new tool adds the second element as a lead the old tool never surfaced (39 added-only paths total; additions are recall/visibility gains, unadjudicated individually).
4. **Final evidence is uncommitted**: 28 dirty/untracked lane paths, including all `evidence/final/*-a6cef89.json` receipts and this `residual/` directory. Hashes are verified against working-tree bytes, but freeze/commit is required before any immutability claim.
5. I did not rerun any corpus, suite, or VCS payload; one new bounded probe allowance went unused. All conclusions come from committed sources, the embedded per-file run arrays in the receipt, and the receipts themselves.

## Verdict

The removal-side adjudication is honest and source-accurate on every attacked slice: B14, dict-splat defaults, reset, and default-lambda override each check out against the exact inert snapshot sources, and no wrongly-excused real old process loss was found — the one demotion (reset_cell) is correct under real reset semantics and keeps the intent visible as a lead. The raw receipt matches every claimed number checked (31/10/19/2 groups, 107+1 errors, exit 1, 1356 paths, pins). Residual exposure is documentation (stale commit-dry-run docstring), provenance (unreceipted vcs_fp=20), completeness framing (unitemized added-side rows), and repo hygiene (uncommitted final evidence). Counts — including VCS fp 26 vs 20 — are population-bounded and must not be promoted to universal no-harm claims.
