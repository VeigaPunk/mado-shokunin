# AttackMistake — critic review of the R13-V3 receipt wrapper (round 14, w1)

Seat: `MadoR14.AttackMistake` (critic, leaf). Date: 2026-10-20. I attacked the approach, not its author.

**Target.** The ReceiptBuild assignment (`.ufo/waves/round-14/w1/spec.json`, item `ReceiptBuild`) and the draft it produced:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/receipt.py`: 245 lines, SHA-256 `210d4c47f85b04ca9e25b7036be7ce077476c88dc3b7e40f6d0caa59d3f80563`, observed 2026-10-20.
- Its write-up, `.ufo/waves/round-14/w1/ReceiptBuild.md`.

**Outside items read.** `corpus/lessons/round-13-verifier-spotcheck.md:203-205` (R13-V1..V3).

**Axes I named:**
- **operability.** The receipt must be able to go red, and must not file false provenance.
- **coverage.** No harm: no U-item, source row or identity leak may be added by evidence capture.

**Evidence class.** Local repository reads plus read-only digest and grep observations. I made no external source opens, so the URL/quote/tier block does not apply. I installed or upgraded no tools. I did not run the wrapper, the gate, or any test.

Tags: `[OBS]` = observed by me this session; `[INF]` = inference from read code, not executed.

---

## Verdict in one paragraph

The wrapper is a sound shape for R13-V3, and its digest-mismatch refusal can genuinely go red. Its header correctly separates `revision` from the resolved `commit`. But as drafted, the receipt **attests a file the command is not required to execute**. The same gap lets it **persist live output identities**. It also **silently overwrites earlier evidence**, refusals included, and it **writes `exit=2` on refusals**, which collides with the gate's own "failing selftest" exit. Five small corrections make it fit for purpose: argv allowlist, no-overwrite, refusal exit line, symbolic-revision test, and self digest. None of them is a framework. R13-V3 is grounded by existing QUALITY criteria 7/9/13; it needs no new criterion and earns no C2 score.

---

## Counterexample 1 — header digest is not bound to what runs (operability, false provenance; blocking)

**Evidence:**
- `capture()` hashes the fixed path `GATE = 'tools/mado-verify.sh'` (`receipt.py:26,51-55,117-119`).
- `capture()` then runs any `COMMAND` (`receipt.py:135`).
- No check ties `COMMAND` to `GATE`.

**[INF] Concrete cases that would each produce `status: ran` with matching gate digests:**
- `receipt.py --revision HEAD --output X -- sh -c 'echo "MADO_SELFTEST: 310/310 assertions passed"'`. A fabricated verdict, filed under a real gate digest.
- `-- bash .ufo/waves/round-13/frozen/gate.sh --selftest`. A different file. Its bytes equal the gate only by coincidence of round 13 (`committed-bindings.json`, `frozen_gate_matches_working_commit`). That equality breaks as soon as this round's gate commit lands.
- `-- bash /tmp/copy.sh --selftest`. Any edited copy.

**Why this matters for R13-V3.** The routed defect asks that a standalone receipt carry "the measured gate revision/digest" (`round-13-verifier-spotcheck.md:205`). A digest of a file the command never read is not the *measured* gate's digest. It is the false-provenance pattern the outside reviewer was careful to say round 13 did *not* commit.

**Smallest safe correction.** Make the wrapper gate-specific, which the assignment already states as its purpose. Refuse before running unless the argv is exactly one of:
- `bash tools/mado-verify.sh --selftest`
- `bash tools/mado-verify.sh --no-live`

Then add one selftest case: matching digests with a non-gate command (for example `sh -c ':'` writing a sentinel) must exit 2, write `status: refused` with reason `command does not run tools/mado-verify.sh in an allowed mode`, and leave the sentinel absent.

Rejected alternative: "the gate prints its own sha". That needs a gate edit, which only GateImplement may make. It also moves `PIN_MADO`, and costs more than an argv check.

## Counterexample 2 — arbitrary command persists output identities (coverage/safety no-harm; blocking)

**Evidence:**
- [OBS] At `HEAD:tools/mado-verify.sh:84`, `LIVE_REQ` defaults to `auto`. At `:3407-3408`, `auto` turns the live layer on when `ROOT` is `$HOME`, which is the default.
- So `bash tools/mado-verify.sh` with no flag runs live.
- [OBS] A retained live run in `.ufo/evidence/round-12/gate-live-after.txt:21,28` contains an output connector name and mode. I deliberately do not reproduce them here.
- The draft persists all stdout (`receipt.py:135-149`).
- The ReceiptBuild write-up suggests no restriction (`ReceiptBuild.md` §4).

**[INF] Consequence.** One natural invocation, `-- bash tools/mado-verify.sh`, writes an output identity into a round-14 evidence path. This round's contract forbids that ("No … device/output identities").

**Smallest safe correction.** The argv allowlist from counterexample 1 closes this too. `--no-live` takes precedence over `MADO_VERIFY_LIVE` (flag parsing after `:84`), and `--selftest` is hermetic. Add no redaction machinery.

## Counterexample 3 — receipts and refusals overwrite earlier evidence (operability, duplicate convention; should fix)

**Evidence:**
- `write_receipt()` uses `os.replace(tmp, output)` unconditionally (`receipt.py:85-98`).
- Refusals are written to the same `--output` (`receipt.py:113,124`).
- The gate's own receipt convention refuses an existing destination:
  - [OBS] `HEAD:tools/mado-verify.sh:1787`: "FILE must not exist — receipts are never overwritten".
  - `:1902`: the refusal text.
  - `:1245`: selftest S7.
- The repository records red history rather than smoothing it (SCORECARD row 5: "mid-round red history … recorded, not smoothed").

**[INF] Counterexample.** L1 runs the suggested command (`ReceiptBuild.md` §4) while the gate is still uncommitted:
- [OBS] Right now the worktree gate is `b50dae25504dd6cc93f89a46847af41a9a6bad95ba255924701e00fe479d36d7` and `git show HEAD:tools/mado-verify.sh | sha256sum` is `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569`.
- So the run writes a refusal to `evidence/gate-selftest.txt`.
- After the commit, the rerun replaces it. The red disappears.
- In the other order, a later accidental refusal replaces a good green receipt with `status: refused`.

Either way, the wrapper establishes a second, weaker receipt convention beside the gate's existing one.

**Smallest safe correction:**
- Create the destination with `O_EXCL` semantics (link or rename only if absent).
- On an existing path: exit 2, write nothing, and print `MADO_RECEIPT: REFUSED (destination exists: PATH)`.
- Add one selftest case: an existing file is byte-unchanged after a refused call.

## Counterexample 4 — `exit=2` on a refusal reads as "the gate's selftest failed" (operability, false measurement; should fix)

**Evidence:**
- Refusal receipts end `exit=2` (`receipt.py:111-113,122-124` passing `USAGE_EXIT` as `rc`, rendered at `:79`).
- The gate's exit map: `2 = tool/usage error (bad args; a failing --selftest)` (`HEAD:tools/mado-verify.sh:12-13`).
- Round-13 receipts use the `exit=` line as the **command's** exit (`.ufo/waves/round-13/evidence/*.txt`).
- R13-V3 itself stresses that the provenance gap is "not … a failed C2 measurement".

**[INF] Counterexample.** `grep -H '^exit=' .ufo/waves/round-14/evidence/*.txt` lists a refused receipt as a gate that exited 2. The command never ran.

**Smallest safe correction:**
- On refusal, write `exit=not-run`, or omit the `exit=` line and write `wrapper-exit: 2`.
- Keep process exit 2.
- Adjust the selftest assertions (`receipt.py:200-204,206-209`) to require that refused receipts contain no `exit=2` line.
- Readers then cite `status:`; the process exit alone stays ambiguous by design.

## Counterexample 5 — the selftest cannot detect an unresolved revision in the header (operability; should fix)

**Evidence:**
- The selftest always passes the full commit id as `--revision` (`receipt.py:175-177,189,196`).
- The `commit:` field is never asserted.

**[INF] Surviving mutant.** Change the `('commit', commit)` header to `('commit', revision)`, or skip `resolve_revision`'s output on success. All 13 assertions still pass.

**Why it matters.** The documented L1 invocation uses `--revision HEAD` (`ReceiptBuild.md` §4). A receipt with `commit: HEAD` is meaningless one commit later. That is exactly the "named revision" requirement of QUALITY 6/7.

**Smallest safe correction.** One assertion: capture with `--revision HEAD` and require `revision: HEAD\n` plus `commit: <fixture 40-hex>\n` in the receipt.

## Counterexample 6 — the wrapper itself is unpinned (operability; cheap, recommended)

**Evidence:**
- `receipt.py` is untracked under `.ufo/waves/round-14/` (`git status --short` shows `?? .ufo/waves/round-14/`).
- Its receipt header carries no digest of itself.
- QUALITY 13: "Evidence meant to outlive a round is a committed path or quoted lines plus sha".

**Correction.** Add `wrapper-sha256: <sha256 of Path(__file__) bytes>` to the header. L1 binds it at the commit via `git show <commit>:.ufo/waves/round-14/receipt.py | sha256sum` (QUALITY 7).

## Tradeoffs, not defects

- **Post-run re-hash (TOCTOU).** ReceiptBuild deliberately leaves it out (`ReceiptBuild.md` §5.2). Seats finish before L1 runs, so the remaining window is L1's own. Adding a re-hash is cheap: equal digests → keep; unequal → `status: changed`, output kept. I recommend it, but its absence does not falsify a receipt taken with no concurrent writer.
- **No timestamp.** This buys byte-stable receipts. QUALITY 10 dates live in the report line (`<n> — <command> <date>`), so this is acceptable if L1 dates each cited receipt in the report.
- **stdin inherited** (`receipt.py:135`). The gate modes allowed above do not read stdin. `stdin=subprocess.DEVNULL` matches the tameshi runner's `</dev/null` contract and costs one argument. Optional.
- **Signal mapping** (`128 - returncode`) is correct but untested. Signals are outside the criterion. Optional.

## Interaction with R13-V1 / R13-V2 (must not be over-credited)

- **R13-V2.** The wrapper only runs when the worktree gate equals the `--revision` blob. After GateImplement's edit, the wrapper therefore **cannot produce a baseline-revision gate receipt**: the worktree no longer holds the baseline gate, and restoring it would be a repository mutation. Consequences:
  - Two wrapper receipts can never evidence "byte-identical outputs across before/after revisions".
  - The gate's `boundary.readonly` row stays a within-run fact (`round-13/evidence/gate-file-plane.txt:47`).
  - Before/after revision comparison belongs to `measure.py`'s `git show`-extracted temp gate, not to this wrapper.
  - L1 wording must keep the two distinct.
- **R13-V1.** Untouched by this artifact. ReceiptBuild says so correctly. It must not be counted as addressed by the wrapper.

## Criterion grounding

- **Already covered by existing criteria; mint no new one:**
  - R13-V3 is a conformance gap against QUALITY **9** ("Bind each audit verdict to a commit or frozen-copy sha") and **7** ("Hash committed artifacts from `git show <commit>:<path>`").
  - The wrapper's persistence falls under QUALITY **13**.
  - A new "receipts carry revision/digest" criterion would duplicate 9: two authorities for one rule.
  - Cite the lesson line `round-13-verifier-spotcheck.md:205` as the trigger and criteria 7/9/13 as the rule.
- **Score.**
  - SCORECARD round-14 declares R13-V1..V3 "lesson-backed corrections within these claims/frontier duties, not a third axis claim" (`SCORECARD.md:482-483`).
  - R13-V3 was "status-neutral provenance debt" (`round-13-verifier-spotcheck.md:205`).
  - The wrapper's selftest count must not enter C2's 0/3 → 3/3 directory-target counter or the gate's own selftest total.

## Minimal red-before / green-after evidence for L1

| # | Evidence | Red (before / negative) | Green (after / positive) | Status now |
|---|---|---|---|---|
| E1 | Historical gap | `round-13/evidence/gate-selftest.txt` has **0** lines matching `^(commit|revision|gate-source-sha256|gate-worktree-sha256|sha256)[:=]` | Round-14 gate selftest receipt has non-empty `commit:` (40-hex), `gate-source-sha256:` and `gate-worktree-sha256:`, equal to each other | [OBS] red side: count 0 (`grep -c -E …`, 2026-10-20). Green: L1-owned |
| E2 | Wrapper able to fail (fixture) | `receipt.py --selftest` cases: digest mismatch → exit 2, no run; **non-gate argv → exit 2, no run** (CE1); **existing output → exit 2, file unchanged** (CE3); refusal has no `exit=2` (CE4) | matching digest, allowed argv → `status: ran`, command exit propagated; `--revision HEAD` resolves to 40-hex `commit:` (CE5) | Not run; CE1/3/4/5 cases absent from the draft |
| E3 | Selftest discriminates (mutation) | Suite: `python3 "$MUTANT" --selftest` via `tameshi-shokunin/tools/mutate-and-run.sh`. Three single-edit mutants: (a) `if source_sha != worktree_sha:` → `if False:`; (b) header `('commit', commit)` → `('commit', revision)`; (c) delete the argv allowlist check. Each must be **KILLED**; control GREEN; `MUTATE_RESTORE: OK` | — | Not run. Mutant (b) **survives the current draft** [INF]; (c) does not exist yet |
| E4 | Real-repo fail-closed (optional, zero fixtures) | One L1 run before the gate commit into a **distinct** path such as `evidence/receipt-refused-uncommitted.txt`: expect `status: refused`, both digests, no `MADO_SELFTEST` line | After the commit, `evidence/gate-selftest.txt` → `status: ran`, digests equal | [OBS] precondition holds now: worktree `b50dae25…` ≠ HEAD `037b05dc…` |
| E5 | Independent re-derivation | — | `git show <commit>:tools/mado-verify.sh \| sha256sum` equals the receipt's `gate-source-sha256`; `git show <commit>:.ufo/waves/round-14/receipt.py \| sha256sum` equals `wrapper-sha256` (CE6) | L1/verifier-owned |

**Minimum sufficient set:** E1 + E2 + E5. Add E3 only if the wrapper is presented as "shown able to fail" beyond its own assertions. E4 is free if L1 runs before committing, but it must use a distinct path, and must not be done by overwriting (CE3).

## Smallest safe correction, consolidated (for ReceiptBuild / L1; I made no edits)

1. **Argv allowlist:** exactly `bash tools/mado-verify.sh --selftest` or `--no-live`. Anything else → refused, exit 2, not run. Plus 1 selftest case.
2. **No overwrite:** existing `--output` → exit 2, nothing written. Plus 1 selftest case.
3. **Refusal exit line:** refusals write `exit=not-run` (or `wrapper-exit: 2`), never `exit=2`. Adjust 2 assertions.
4. **Symbolic revision:** `--revision HEAD` test asserting 40-hex `commit:`. Plus 1 selftest case.
5. **Self digest:** `wrapper-sha256:` header line.
6. **Optional:** post-run re-hash; `stdin=DEVNULL`.

Owned-axis impact if uncorrected:
- operability: false-provenance receipts and lost red history.
- coverage/safety no-harm: a live identity leak into evidence.

Impact if corrected: operability gains a falsifiable provenance receipt, credited as an R13-V3 correction only and not as a score. Coverage is unaffected.

## Checks for L1 (after all seats; I ran none)

- `python3 .ufo/waves/round-14/receipt.py --selftest`
- the E3 mutation sweep
- the E1 grep on both receipts
- the E5 `git show … | sha256sum` re-derivations
- `grep -c -E 'DP-|HDMI|eDP' .ufo/waves/round-14/evidence/*.txt` expecting 0, as a no-identity sanity sweep

## Post-decision status (appended 2026-10-20; review text above unchanged)

- [OBS] L1 rejected the arbitrary-command wrapper and removed `.ufo/waves/round-14/receipt.py`; `ls` reports no such file. `ReceiptBuild.md:1,6` records the rejection and says no capability or measurement claim was made. Its §3 keeps CE1–CE4 as the rejection rationale. No hardening landed.
- So corrections 1–6 and evidence rows E2–E5 above no longer have a target. Do not run or claim them. E1's red side still stands: the round-13 `gate-selftest.txt` has 0 revision/digest header lines. R13-V3 therefore remains open provenance debt under QUALITY 7/9/13, and nothing in this round closes it.
- The live-default anchor is also stated in the gate's own usage text: `HEAD:tools/mado-verify.sh:16,92-95` ("(default) live read-only run against $HOME"), alongside `:84`.
- The no-credit rule still applies: the rejected candidate adds no C2 score, no tool and no capability.
