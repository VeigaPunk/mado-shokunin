# ReceiptBuild — round 14 / w1 — report (rejected candidate)

**Seat:** `MadoR14.ReceiptBuild` (executor, leaf). **Target:**
`/home/vgpnk/Projects/shokunin/mado-shokunin`. **Observation date:** 2026-10-20.
**Status:** **rejected at L1 integration; candidate removed. No capability claim, no check run.**

## Disposition

L1 decided to reject the standalone arbitrary-command receipt wrapper as an unnecessary second
receipt format and a general execution surface. R13-V3 will be fixed directly in every committed
round-14 selftest receipt using the resolved measured gate commit, raw SHA-256, and the exact
command before the stdout/exit body. L1 removes `receipt.py`; these reports are retained only as
rejected candidate evidence.

Observed after the decision: `.ufo/waves/round-14/receipt.py` is absent. Last candidate bytes had
SHA-256 `210d4c47f85b04ca9e25b7036be7ce077476c88dc3b7e40f6d0caa59d3f80563` (245 lines, `+x`);
the post-decision edit failed because L1 had already removed the file. No further artifact edit
was made.

## Candidate (rejected; not in tree)

It would have run `receipt.py --revision REV --output PATH -- COMMAND...` from the lane root,
persisting command, cwd, captured stdout/stderr, exit, and a header with the resolved commit plus
whole-file gate digests at `REV` and in the worktree. `--selftest` proposed 13 isolated-temp-git
assertions. It was never executed, so none of this is a measured behavior.

## Why it was rejected (review findings, retained)

- **ReviewReceipt:** refusal exit 2 is indistinguishable from a child exit 2 and the gate's fixed
  “2 = tool/usage error” (`git show HEAD:tools/mado-verify.sh:12-13`); digest comparison can fail
  open if it copies the snapshot writer's literal fallback (`mado-verify.sh:2006-2008`); an
  uncommitted gate cannot be bound while seats may not commit; arbitrary COMMAND output can breach
  the data fence; stable text, digest naming, TOCTOU, exit precedence, and duplicate-format
  questions remain planner decisions.
- **AttackMistake:** blocking — the digest header is not bound to COMMAND, so any command would get
  `status: ran` with authentic gate digests. A bare `bash tools/mado-verify.sh` defaults to a live
  run (`git show HEAD:tools/mado-verify.sh:16` usage; `LIVE_REQ="${MADO_VERIFY_LIVE:-auto}"` at
  `:84`; `--no-live` opt-out at `:92-95`), so persisted output could retain raw host identities.
  Its proposed hardening was an exact argv allowlist (`--selftest|--no-live`), never-overwrite, a
  non-`exit=2` refusal marker, and a wrapper self-digest.

These findings support the rejection: the wrapper was a general execution surface whose header
did not identify what was measured.

## Axis effect

| Axis | Effect |
|---|---|
| coverage | None; no corpus/source/feature change. |
| operability | Negative evidence only: a second receipt convention and unbound execution surface were rejected. No scoreable improvement, no added tool/capability. |

R13-V1 is untouched. R13-V2 is untouched; no output-equality-across-revisions claim was made and
the rejected surface is removed. R13-V3 remains open and is now L1-owned in the committed
round-14 selftest receipts; its recorded gap is unchanged:
`corpus/lessons/round-13-verifier-spotcheck.md:205` and
`.ufo/waves/round-13/evidence/gate-selftest.txt:1-9` (no revision/digest header).

## Evidence

- Candidate absent at disposition; last digest `210d4c47…f80563`.
- `git show HEAD:tools/mado-verify.sh:12-13,16,84,92-95` — exit map, live-default usage,
  `MADO_VERIFY_LIVE` default, `--no-live` opt-out.
- `.ufo/waves/round-14/w1/ReviewReceipt.md`; `.ufo/waves/round-14/w1/AttackMistake.md`.
- Lane HEAD `873ff081b2ac363df771261b0ed950cba50d8988`; gate worktree concurrently edited by
  GateImplement.
- No external source opened; no tool installed or upgraded; no check executed by this seat.

## Blockers

None. Disposition complete; no further artifact work is in scope for this seat.
