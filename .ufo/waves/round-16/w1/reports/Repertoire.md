# Repertoire — safety-plan classifier demonstration status (mado round 16, w1)

Seat: `MadoR16.Repertoire` (connector, leaf, source reading only).
Date: 2026-10-20. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Baseline: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.

## Answer

**Not demonstrated at present. No repertoire entry is admissible until the single L1 verification run passes every check in §3.**

At read time the classifier and its policy do not exist in the lane:

- `tools/mado-action-plan.py`: not found.
- `.ufo/waves/round-16/safety-policy.json`: not found.
- `.ufo/waves/round-16/` contains only `dispatch.json`, `spec.json` and `reports/swarm-registry.json`.

So there is nothing to demonstrate yet. Any "demonstrated (1)" wording written before L1's run is a premature claim.

## 1. Axes named

| Axis | Relevance to this question | Current state (from round-15 closure and SCORECARD) |
|---|---|---|
| C1 coverage | Not affected. U7 is causally separate (spec contract: "U7 source admission needs no classifier; the classifier needs no Waybar note"). | Out of scope for this seat. |
| C2 operability | The classifier is the claimed operability capability. | Host-safety **harmed** by R15-V1 (forbidden libinput partial upgrade). Unremediated and operator-owned. A static gate does not erase it. |
| Quality | Learning trend. Shares the R15-V1 event. | Harmed (unchanged by this seat). |
| Freshness, calibration, depth, adjacency | No classifier claim. | Unchanged. |

## 2. Evidence basis (source reading only)

- Spec `SafetyGate` item (spec.json:10): defines the gate API. Plan schema: object with `actions` list of `{kind, argv}`. Allowed kinds `read-source` and `repo-write` (nonempty argv). Blocked kinds `package-install`, `service-mutate`, `compositor-mutate`, `input-capture`. Unknown or malformed fails closed. Basename refusal list: `pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,evtest,sudo,sh,bash,env`. Exit codes 0 / 1 / 2. Self-invocation `--selftest`. `--frozen DIR` digest check with tamper giving `2 snapshot_tampered`. Policy must be `paused=true`.
- Spec `SafetyCases`, `SafetyControlRed`, `SafetyService`, `SafetyCompositor`, `SafetyInput`, `UnknownActions`, `FrozenInputs`, `SelftestTruth`, `ExecBasename`, `PolicyTamper`, `NoShell`: the planned verification surfaces. None has produced output yet (all are in the same wave, not yet landed).
- Round-15 closure `corpus/lessons/round-15-verifier-spotcheck.md` §Gate, lines 159-163 and 268-272: the install-predicate controls are "hard-coded in-memory controls, not real pacman dry-run output, an installed-host census, operational installation prevention or host remediation". It also requires that any future install use a real `pacman -Sp --print-format '%n %v'` plan and a complete installed-name comparison. The classifier inherits this limit: its fixtures prove classification of declared JSON only.
- Precedent, round-15 closure line 248-250: "QUALITY 20 is grounded in actual M2; its fixture is not credited as an operational guard." Round-14 SCORECARD line 681 had already overstated a fixture-backed guard as "demonstrated"; the round-15 closure corrected that. The round-16 wording must not repeat it.
- SCORECARD.md round-16 draft (lines 703-709): currently reads `C2 operability / capability acquisition: absent (0) → demonstrated (1)`. This is a numeric 0→1 scale that conflicts with the existing repertoire convention (SCORECARD lines 435-443: capability table rows with "Demonstrated evidence" and "First-working round", not a score). It also presupposes the outcome before L1 runs. SCORECARD is L1-owned, so this seat only proposes wording (§4).

Existing repertoire convention for reference: SCORECARD lines 435-438 (capability table with what-it-does, demonstrated evidence, first-working round); lines 619-622 and 681-682 (no exploratory claim, no capability-table entry unless a claim is admitted).

## 3. Conditions for a "demonstrated" repertoire entry

All must hold on the single L1 verification run, at a named committed revision R, with exact command, exit and digest recorded. Any one failure means the entry stays absent and no partial credit is given.

1. `python3 tools/mado-action-plan.py --selftest` exits 0. The self-invocation subprocess fixtures assert both exit code **and** finding for every case. Expected constants are pinned independently of the code under test; if the expected values are derived from the module they do not count.
2. A real incident-shaped plan (a `package-install` / `sudo pacman` transaction, as in `safety-cases.json`) returns exit 1 with the stable `package-install` finding.
3. A `read-source` control (allowed, nonempty argv, non-refused basename) returns exit 0 with `plan_safe`. The control must differ from the red case only in the refused element (same command reason-only delta).
4. Policy negatives: `paused` false or missing, malformed policy, unknown kind, missing or non-list argv each return exit 2 (could-not-evaluate) or the stated stable finding, not exit 0.
5. `--frozen DIR` with unmodified `expected.json` returns `frozen_match`. A tampered plan or policy returns exit 2 `snapshot_tampered`.
6. The gate never executes supplied argv and never inspects host state. Verified by source reading, not by running it.

Only the L1 run may produce these receipts. Seats must not run the gate (contract: "No build/lint/tests/check execution by seats").

## 4. Proposed bounded score wording

Replace the SCORECARD round-16 line `absent (0) → demonstrated (1)` with a capability row, not a rubric score. Use this wording only if §3 passes in full; otherwise write "attempted; not demonstrated" and no row.

> **C2 operability — bounded static capability (repertoire row, not a score move).** `tools/mado-action-plan.py` (paused policy `.ufo/waves/round-16/safety-policy.json`) classifies declared JSON action plans as `plan_safe` (exit 0), a stable refusal finding (exit 1), or could-not-evaluate (exit 2). Demonstrated on selftest, the incident-shaped red case, the read-source green control, policy negatives and the digest-bound `--frozen` run, at measured revision R. It classifies supplied declarations only: it does not execute argv, inspect the host, intercept tools, enforce anything, or repair the host. Basename refusal covers only the listed executables; wrappers and interpreters outside that list are not classified. Fixtures are hard-coded and are not real pacman plan validation. No operability score moves. The R15-V1 host-safety harm stays `harmed`, operator-owned and unremediated.

Rules for the wording:

- Do not write "absent (0) → demonstrated (1)" or any other numeric 0/1 pair. The repo has no rubric for this capability.
- Do not write "operability improved" or "guard"/"protection" without the scope qualifier above.
- Keep the round-15 harm line verbatim in the same section; a new static gate is a different observable and does not clear it.
- Record exact command, exit, measured revision and gate digest. Do not state a digest that was not produced by the run.

## 5. Risks and limits

- **Wrapper and interpreter gap.** The basename list refuses `sudo`, `env`, `sh`, `bash` and the named package/service tools. Not refused: `doas`, `pkexec`, `nice`, `timeout`, `xargs`, `busybox`, `ssh`, and interpreters such as `python3`/`perl` used with `-c`. The spec deliberately avoids shell-parsing ambitions, so this is a documented limit, not a bug. The score wording must say so. L1 may decide whether to extend the list; that is a design choice, not a repertoire claim.
- **Self-test circularity.** If the selftest expected constants are computed from the classifier's own functions, the selftest proves nothing. Verify the expected values are literal in the selftest.
- **Premature language.** Any draft that treats the classifier as installed or in effect before §3 passes is a misstatement.
- **Harm not cleared.** The gate does not stop a human or a non-declared path from running pacman. It also does not address the already-committed partial upgrade.

## 6. Verification handed to L1 (run once, after integration)

- `python3 tools/mado-action-plan.py --selftest; echo $?` → expect 0 with all assertions reported.
- `python3 tools/mado-action-plan.py --plan <safety-cases red plan> --policy .ufo/waves/round-16/safety-policy.json; echo $?` → expect 1 with `package-install`.
- Same command with the read-source control → expect 0 with `plan_safe`.
- `python3 tools/mado-action-plan.py --frozen <DIR>; echo $?` → expect `frozen_match`, 0; and a tamper copy → 2 `snapshot_tampered`.
- Confirm the policy file has `paused` true.
- Confirm the expected constants in the selftest are literal, not imported from the module under test.

## 7. Tooling and scope disclosure

- No tool was installed or updated by this seat (contract: no installs this round; operator pacman pause in force). No `pacman`, `-Sy`, `-Syu`, `-U`, `-R`, downgrade or service operation.
- No build, lint, test or gate execution. No live compositor, service, input-device, screenshot or command probe. No `~/.omp/agent/agent.db*` or credential files read.
- No subagent dispatch (leaf member).
- Files read: `/home/vgpnk/.omp/agent/RULES.md`; `corpus/lessons/round-15-verifier-spotcheck.md`; `.ufo/waves/round-16/w1/{spec.json,dispatch.json,reports/swarm-registry.json}`; `SCORECARD.md` (lines 380-485, 624-717). Non-existent and not read: `tools/mado-action-plan.py`, `.ufo/waves/round-16/safety-policy.json`.
- Only this report was written.
