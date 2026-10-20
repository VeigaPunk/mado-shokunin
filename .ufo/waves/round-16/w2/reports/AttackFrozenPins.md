# AttackFrozenPins — round 16 w2 (mado), critic

Seat: `MadoR16.AttackFrozenPins` (critic, leaf). Target: `tools/mado-action-plan.py --frozen DIR`, with these claims under attack: mandatory plan/policy digests are checked before classification, the bytes hashed are the bytes parsed, and expectation errors exit 2.

Method: I read the source only. Files read: `tools/mado-action-plan.py` (working tree, sha256 `e506bc23…b535`); `.ufo/waves/round-16/frozen/{expected,plan,policy}.json`; `safety-policy.json`; `safety-cases.json`; `adjudication.json`; SKILL rows `:529-543`; SCORECARD `:690-735`; the w1 reports `FrozenDesign.md` and `FrozenInputs.md`; and the round-13 `frozen/verify.py` precedent. I also read `corpus/lessons/round-15-verifier-spotcheck.md` first, as required.

Commands I ran were read-only: `sha256sum`, `cmp`, `stat`, `ls`, `jq`, `git status`. I did not run any gate, selftest, `--frozen` run, `measure.py`, test or probe. Every behavioural statement below is **[INFERENCE] from source**. Nothing was installed or updated. I edited no files except this report.

## Axes

- **A1 pin ordering**: both digests are mandatory and checked before classification.
- **A2 byte identity**: the bytes hashed are the bytes parsed.
- **A3 expectation integrity**: every expectation error exits 2 with the right stable id.
- **A4 selftest discrimination**: the frozen fixtures kill the relevant mutants.
- **A5 claim calibration**: the SKILL, SCORECARD and receipt wording matches what the code does.

## What holds (credited)

- **A1 holds.** In `run_frozen`, expected.json is loaded and its keys and types are checked first (`:386-413`). Next the four mandatory keys are checked (`:400-404`). The digest loop over plan and policy (`:414-422`) finishes before `_evaluate` is called (`:424`). A missing pin is reported as `frozen_error`, exit 2. A missing or non-regular input is reported as `snapshot_tampered`, exit 2, through `_sha256` → `_read_regular` (`:150-178`, `:211-215`).
- **No classifier output in frozen mode.** Frozen mode prints only its own frozen finding. `_evaluate` returns a tuple and never calls `_emit`, so no `plan_safe` token can appear (FrozenInputs T22).
- **The committed snapshot is intact (working tree).** Observed hashes:
  - `plan.json` = `82bc7652…ebc3`, matching its pin.
  - `policy.json` = `fb134d8f…b7fc`, matching its pin, and byte-identical to `safety-policy.json` (`cmp` passed).
  - All three files are regular files.
- **The expected verdict is correct.** `denied_executable:sudo`/1 follows from `_classify` (`:325-347`): the kind is `read-source`, which is allowed and not paused; argv is non-empty; and `sudo` is in the deny list. The policy passes `_validate_policy`, because an absent `argv_nonempty` defaults to False (`:269`), which equals the pinned value.

## Counterexamples

### F1 — Medium-high (fixable): the bytes hashed are not the bytes parsed (A2)

`run_frozen` hashes each file with `_sha256(path)` (`:416`). That opens the file, reads it and throws the bytes away (`:211-215`). `_evaluate(plan_path, policy_path)` then opens both paths again through `_load_json` (`:356`, `:364`). That makes four separate `os.open` calls, none of which uses `O_NOFOLLOW` (`:154`).

Counterexample (bounded: it needs write access to DIR during the run):
1. Let DIR/plan.json be the pinned red plan.
2. After the digest check passes at `:420` and before the re-read at `:364`, swap the file with `rename(2)` or `ln -sfn` to a different plan.
3. If the swapped plan has the same verdict, the run reports `frozen_match`, exit 0, on bytes that never matched the pin.
4. If it has a different verdict, the run reports `frozen_verdict_mismatch`, exit 1. That is tampering reported as a changed verdict, which FrozenInputs §1/T20/T21 forbid.

Symlinks that point outside DIR are followed. The round-13 precedent rejected those (`round-13/frozen/verify.py:82-87`); this tool does not, which is a regression.

Why it matters: an out-of-band receipt that pins plan and policy at commit time cannot guarantee that the verdict printed by a run was computed from those pinned bytes.

Provenance: FrozenInputs R-3/R-4/R-8 (`FrozenInputs.md:60-65`) and FrozenDesign advice 4 (`FrozenDesign.md:100`) both required a single read with `O_NOFOLLOW`. `adjudication.json` neither accepts nor rejects that requirement; it only bounds the "broader legacy gate rewrite". The requirement was dropped without a decision.

Calibration: I found no *published* claim that the tool reads each file once. The docstring (`:53-54`, `:65-66`) and the SCORECARD phrase "digest-bound frozen run" (`:706`) are true at hash time. So this is a code defect against the w1 requirement and against what C2 credit implies. It is not false provenance in any published text.

### F2 — Medium (fixable): expectation errors that exit 1 instead of 2 (A3)

The type checks (`:409-413`) test `type(want_exit) is int` and `isinstance(want_finding, str)` and nothing more. Each of these expected.json edits leaves both digests intact, triggers a replay, and ends as `frozen_verdict_mismatch`, **exit 1**:
- `"expected_exit": 7`, or `-1`
- `"expected_finding": ""`
- `"expected_finding": "frozen_match"`
- an impossible pair such as `"plan_safe"` with exit 1
- an unreachable finding such as `"denied_executable:curl"`

The reachable (finding, exit) set is finite and can be derived from the `PINNED_*` constants: `plan_safe`/0; `unknown_action_kind`/1; `empty_argv`/1; `blocked_action_kind:` plus each of the 4 paused kinds, exit 1; `denied_executable:` plus each of the 12 denied executables, exit 1; `plan_malformed`/2; `policy_malformed`/2. That is 21 pairs. FrozenInputs R-6 (`:63`) required exit ∈ {0,1,2}; that check was not implemented.

### F3 — Low-medium (fixable): `--frozen ''` gives a traceback and exit 1 (A3, usage)

`main` tests `if args.frozen:` (`:744`). An empty string is falsy, so the code falls through to `run_evaluate(args.plan=None, policy)` (`:748`).

With `--frozen '' --policy .ufo/waves/round-16/safety-policy.json`:
1. The policy validates.
2. `_load_json(None)` → `os.open(None, …)` raises `TypeError`.
3. `_read_regular` catches only `OSError` (`:155`), so the error is uncaught: traceback, exit 1.

Exit 1 is the gate's "denied" code (SKILL `:529`). The docstring promises no traceback (`:31-33`). Without `--policy`, the same input exits 2 with the misleading message "--plan requires --policy".

A related point: `--frozen D --policy P` is accepted, and P is silently ignored, because `--policy` sits outside the mutually exclusive group (`:739-740`).

### F4 — Low (fixable): a malformed pin gets the wrong stable id (A3)

The pin's format is never validated. A pin of `""`, `"deadbeef"`, `"sha256:<hex>"` or one with a trailing `"\n"` reaches the comparison at `:420` and is reported as `snapshot_tampered`. The exit code (2) is right, but this is an expectation-file error being labelled as input tampering.

`.lower()` also accepts uppercase hex. The round-13 precedent rejects malformed pins as `frozen_error` (`round-13/frozen/verify.py:69-71`).

### F5 — Tradeoff, judge-relevant: expected.json is self-attesting, and its anchor has not landed yet (A5)

Nothing in-band binds the expected.json bytes. Two edits show the effect:
- Rewriting `expected_finding`/`expected_exit` alone gives exit 1, not tamper (FrozenInputs T13).
- A consistent rewrite of all three files (a safe plan, new pins, `plan_safe`/0) gives `frozen_match`, exit 0, which cannot be detected in-band (T14).

Committed history as the anchor is accepted precedent ("protected by committed history, not a circular self-hash", `round-13-verifier-spotcheck.md:157`). However, `git status` shows `.ufo/waves/round-16/` and `tools/mado-action-plan.py` as **untracked**, and `.ufo/waves/round-16/evidence/` holds only `census-before.txt` and `source-bindings.json`.

SKILL `:530` says the "receipt separately binds executable and expectation digests to measured commit". That receipt does not exist yet, so under QUALITY 8 it is a planned artifact. Until L1 commits a binding (`git show <rev>:<path> | sha256sum` for the tool, expected.json, plan.json and policy.json), the frozen credit should stop at plan/policy digests checked at run time.

### F6 — Medium (fixable): the selftest does not discriminate key mutants (A4)

There are five frozen fixtures (`:674-704`). `safety-cases.json` has no frozen rows: all 31 cases are `--plan` cases. These mutants would survive:
- **M1.** Drop the policy entry from the digest loop (`:415`). No fixture tampers with the policy; `frozen-missing-pin` is caught earlier, at `:400-404`. If this mutant ran on real input, a whitespace edit to the policy would come out `frozen_match`, exit 0.
- **M2.** Compare the code only at `:425`. The mismatch fixture differs in both code (0 vs 1) and finding. **M3**, comparing the finding only, survives for the same reason. This contradicts FrozenInputs R-9 ("code-only comparison is not enough").
- **M4.** Remove `plan_sha256` from the mandatory tuple (`:400`). Every fixture carries the plan pin. On real input this mutant gives a KeyError traceback.
- **M5.** Remove the type check (`:409-413`), the unknown-key check (`:393-396`) or `.lower()`. Each survives.

Ordering itself is not observable, because the classifier is pure. That is not a defect.

### F7 — Tradeoff, document it: exit-2 expectations replay to exit 0

A snapshot that pins a malformed policy plus `policy_malformed`/2 reports `frozen_match`, exit 0. SKILL `:530`/`:541` covers red *plans* ("frozen match … never that a red plan is safe") but not could-not-evaluate expectations. Either restrict expectations to exit ∈ {0,1}, or state in the SKILL row that a frozen exit 0 can replay an exit-2 verdict.

## Impacted axes

- **Operability (C2):** F1, F2, F3 and F6 are real defects in the frozen path. None of them falsifies the `--plan` classifier or the committed snapshot's expected verdict.
- **Calibration:** F5 matters if the round report credits a "receipt-bound" frozen run before that receipt is committed.
- **Coverage (C1) and C3:** not affected.

## Smallest safe correction (about 25 lines in `run_frozen`/`main`, plus 4 fixtures)

1. Split `_load_json` into `_read_regular` plus a new `_parse_json(raw)`, and add `_evaluate_raw(plan_raw, policy_raw)`. In `run_frozen`, read each file once with `O_NOFOLLOW`, hash those bytes, and classify those same bytes. No path should be reopened after `:416`.
2. Validate the pin with `re.fullmatch(r"[0-9a-f]{64}", pin)`; on failure report `frozen_error`, exit 2. Require `(want_finding, want_exit)` to be one of the 21 pairs derived from `PINNED_*`; on failure report `frozen_error`, exit 2.
3. Change `main` to test `if args.frozen is not None`, and call `parser.error` when `--policy` is combined with `--frozen`.
4. Add four selftest fixtures with literal expectations:
   - a whitespace edit to the policy → 2 `snapshot_tampered`
   - the sudo plan expecting `denied_executable:pacman`/1 → 1 `frozen_verdict_mismatch`
   - an `"expected_exit": 7` file → 2 `frozen_error`
   - a non-hex pin → 2 `frozen_error`
5. L1 should commit a binding for the tool, expected.json, plan.json and policy.json, or change SKILL `:530` to say the receipt is planned.

## Limits

- Everything here is source-level inference; no run was performed.
- The race in F1 needs concurrent write access to DIR and was not demonstrated.
- Hashes are of untracked working-tree files, not committed blobs.
- I did not review classifier wrapper or basename limits, which other seats own.
