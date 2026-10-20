# ReceiptBuild — round 14 / w1 — REJECTED candidate evidence

Seat: `MadoR14.ReceiptBuild` (executor, leaf; no delegation, no background jobs).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Read-only observations: **2026-10-20**.
Status: **rejected at L1 integration; candidate removed by L1. No capability or measurement claim.**
No build/lint/test/smoke was run by this seat at any point.

## 1. Disposition (supersedes the earlier candidate report)

L1 integration decision, received 2026-10-20:

- Reject the new standalone arbitrary-command receipt wrapper as an unnecessary second receipt
  format and a general execution surface.
- R13-V3 is to be fixed directly in every committed round-14 selftest receipt: resolved measured
  gate commit plus raw SHA-256 and the exact command before the stdout/exit body.
- L1 removes `receipt.py`.
- The reports are retained only as rejected candidate evidence; no added tool/capability claim.

Observed state after the decision: `.ufo/waves/round-14/receipt.py` is absent
(`ls`: “No such file or directory”). The last bytes this seat wrote had SHA-256
`210d4c47f85b04ca9e25b7036be7ce077476c88dc3b7e40f6d0caa59d3f80563` (245 lines, mode `+x`).
The post-decision revision attempt failed because L1 had already removed the file; this seat
made no further edit to the artifact.

Earlier candidate text in this report described a delivered artifact. That framing is withdrawn:
the wrapper is **not** in the tree and contributes no implemented capability.

## 2. What the candidate did (rejected; recorded only to make the rejection auditable)

- CLI: `receipt.py --revision REV --output PATH -- COMMAND...` plus `--selftest`.
- Ran an arbitrary `COMMAND` from the lane root and persisted a v1 receipt with command, cwd,
  captured stdout/stderr, and exit.
- Header carried the supplied revision, resolved commit, whole-file SHA-256 of
  `REV:tools/mado-verify.sh`, and the worktree whole-file SHA-256; digest mismatch refused with
  exit 2 before running.
- `--selftest` proposed 13 isolated-temp-git assertions (matching/mismatching digest, exit
  propagation, no-run-on-mismatch, byte-stable text).

The candidate was never executed, so none of those behaviors was measured here.

## 3. Review findings retained as rejection rationale

### ReviewReceipt (`.ufo/waves/round-14/w1/ReviewReceipt.md`)

- **H1** Refusal exit 2 collides with a propagated child exit 2 and with the gate's fixed
  “2 = tool/usage error” meaning (`git show HEAD:tools/mado-verify.sh:12-13`). A receipt file
  present on refusal weakens “file exists iff COMMAND ran.”
- **H2** Digest equality can fail open if an implementation copies the snapshot writer's literal
  fallback (`mado-verify.sh:2006-2008`, loader `:2091`, diff `:2208-2211`). Use raw
  `git cat-file blob` with a return-code check, not a `git show | sha256sum` pipeline.
- **H3** With GateImplement editing the gate and seats forbidden to commit, no receipt can bind
  the round-14 worktree gate until L1 commits; an uncommitted-gate mode is a planner decision.
- **H4** Generic output persistence breaches the data fence: COMMAND output could retain raw
  session/device/output identities (round-13 M4 precedent). Restrict scope or write outside the
  lane; planner decision.
- **M1-M8**: stable text undefined; two digest meanings (whole-file vs excised pin); TOCTOU and
  create race; exit precedence; do not inherit the gate's 0/1-only rule; captured output is not
  echoed; `--snapshot` already exists as a v1 receipt format; a receipt binds one run to one gate
  digest, not revision-output equality (R13-V2).

### AttackMistake (`.ufo/waves/round-14/w1/AttackMistake.md`)

- **Blocking:** the header digest is not bound to COMMAND. Any command would receive `status: ran`
  with authentic gate digests, so the receipt would not identify what was measured.
- A bare `bash tools/mado-verify.sh` defaults to a live run: usage says so
  (`git show HEAD:tools/mado-verify.sh:16`), `LIVE_REQ="${MADO_VERIFY_LIVE:-auto}"`
  (`:84`), and `--no-live` is an explicit opt-out (`:92-95`). Combined with full stdout/stderr
  persistence, the wrapper could commit live host output. The critic's proposed fix was an argv
  allowlist exactly `bash tools/mado-verify.sh --selftest|--no-live`, else refuse exit 2 without
  running.
- Should-fix items: O_EXCL/never-overwrite convention, refusal text that does not write `exit=2`,
  a selftest mutant that changes the recorded revision, and a wrapper self-digest header.

These findings independently support L1's decision: the candidate was a general execution surface
whose digest header did not constrain or identify the command.

## 4. R13-V3 — now L1-owned, no claim here

The routed defect remains:

- `corpus/lessons/round-13-verifier-spotcheck.md:205`: “future standalone selftest receipts should
  carry the measured gate revision/digest” (11 words).
- `.ufo/waves/round-13/evidence/gate-selftest.txt:1-9` begins `command: bash tools/mado-verify.sh
  --selftest` and ends `exit=0` / `elapsed_seconds=7.351`, with no revision or digest header.

Per the integration decision, the fix belongs in committed round-14 selftest receipts themselves
(resolved measured gate commit + raw SHA-256 + exact command before stdout/exit). This seat does
not edit, run, or claim those receipts.

## 5. Axes

| Axis | Contribution after rejection |
|---|---|
| coverage | None. No U-item, source row, knowledge note, or feature exercise. |
| operability | Negative evidence only: one candidate design was reviewed, found to add a second receipt convention and an unbound execution surface, and was rejected. No scoreable improvement and no added tool/capability. |

R13-V1 retained-data wording and R13-V2 within-run boundary vs revision-output equality are
untouched. The candidate never claimed output equality across revisions; the rejection removes
even the digest-bound run surface.

## 6. Retained evidence

| Anchor | Observation |
|---|---|
| `.ufo/waves/round-14/receipt.py` | **Absent** at disposition (L1 removal). Last candidate SHA-256 `210d4c47…f80563`, 245 lines. |
| `git show HEAD:tools/mado-verify.sh:12-13` | Gate exit map: “2 = tool/usage error (bad args; a failing --selftest)”. |
| `git show HEAD:tools/mado-verify.sh:16` | `mado-verify.sh` with no scope flag is a “live run against $HOME (read-only)”. |
| `git show HEAD:tools/mado-verify.sh:84,92-95` | `LIVE_REQ="${MADO_VERIFY_LIVE:-auto}"`; usage lists `[--no-live] [--live]`, with `--no-live` as the file-plane opt-out. |
| `.ufo/waves/round-14/w1/ReviewReceipt.md` | Independent read-only review, H1-H4/M1-M8. |
| `.ufo/waves/round-14/w1/AttackMistake.md` | Critic review, blocking binding/live-run finding. |
| `corpus/lessons/round-13-verifier-spotcheck.md:205`; `.ufo/waves/round-13/evidence/gate-selftest.txt:1-9` | The R13-V3 provenance gap. |
| Lane HEAD at observation | `873ff081b2ac363df771261b0ed950cba50d8988`; gate worktree was being edited by GateImplement. |

No external source was opened; no canonical URL/pinned-revision table applies. No tool was
installed or upgraded.

## 7. Scope, limits, blockers

- No checks were run by this seat, including the candidate's `--selftest`; the review findings are
  read-only and the candidate was never exercised.
- The rejected candidate's risks (unbound command, live-run output persistence, second receipt
  format, exit-code collision) are resolved by removal, not by hardening.
- No further artifact will be created or modified by this seat. L1 owns the receipt-header fix,
  removal, and the post-integration gate.
- Blockers: none. Disposition complete.
