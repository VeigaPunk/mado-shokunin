# RevR19V4Wording — Append-only incident correction needed

## Findings

### Medium — the lesson’s scan paragraph retains a stale receipt count

`corpus/lessons/round-19.md:123-130` says “155 round-19 transcripts.” The closure states that the committed receipt actually contains **154 files** (`corpus/lessons/round-19-verifier-spotcheck.md:125`). This is a concrete count mismatch. The lesson already correctly says the scan did not detect the invocation inside a written-then-executed script and, after the correction at `round-19.md:144-146`, that captured-by is `none (seat self-report)`. Preserve both; do not attribute detection to the tripwire.

### Low — the lesson does not state the full fail-open outcome or the closure’s recheck limit

The M12 row says the stub harness’s mount step failed and the real probe ran (`corpus/lessons/round-19.md:87`), but does not say the failed setup failed open: it did not stop the payload. Its “no state change observed” wording also needs the closure’s qualification. The closure says no mutating request was accepted in the captured output, but host-state change was not independently measured and the closure performed **no live recheck** (`round-19-verifier-spotcheck.md:124`). R19-V4 routes these requirements explicitly at `round-19-verifier-spotcheck.md:152`.

## Proposed append-only correction (not applied)

Append this block to `corpus/lessons/round-19.md` after its existing final correction at line 160. Leave the original M12 row and post-wave scan paragraph intact as historical text:

> **R19-V4 verifier correction (round 20):** The SentinelGatePath harness’s mount setup failed but did not fail closed: execution continued to the real `/usr/bin/hyprctl probe` (`unknown request`, rc=0). The committed post-wave scan receipt contains 154 files, not the 155 transcripts stated above. The invocation was in a written-then-executed script, outside the parser’s documented analysis; the scan did not detect it. M12’s captured-by is `none (seat self-report)`, not the tripwire. The captured output shows no mutating request was accepted, but no independent measurement established whether host state changed, and the closure performed no live recheck. Do not rerun a real host probe while the host pause binds. (Verifier closure: `corpus/lessons/round-19-verifier-spotcheck.md:124-125`; routed as R19-V4 at `:152`.)

## Locations and disposition

- `corpus/lessons/round-19.md:87` — clarify the failed-mount fail-open behavior and qualify “no state change observed”; append a correction, do not rewrite the incident row.
- `corpus/lessons/round-19.md:123-130` — correct the 155/154 discrepancy through an append-only note; retain the explicit written-script scan blindness and the corrected self-report attribution.
- `corpus/lessons/round-19.md:144-146` — already supersedes the table’s tripwire attribution with `none (seat self-report)`; retain it.
- `corpus/lessons/round-19-verifier-spotcheck.md:124-125,152` — closure and R19-V4 are the fact/routing authority; they already state the breach, count, scan miss, lack of independent state-change measurement, no live recheck, and do-not-reexercise boundary. No correction to the closure is indicated.
- `SCORECARD.md:1266-1279` — the round-20 declaration already routes fail-closed setup with a canary and records 154 files, written-script scan blindness, and self-report rather than detection. No conflicting count/detection claim found there; it does not itself spell out the no-live-recheck limit, which the proposed lesson addendum supplies.

## Residual risk

The host-state outcome remains unknown: the closure did not independently measure a state change and performed no live recheck. Do not treat the absence of an accepted mutating request in the transcript as proof that no state changed.

## Verification gaps

This was a document-only comparison of the cited lesson, closure, and scorecard ranges. No live recheck, harness execution, fixture execution, or tests were performed; this review does not establish host state. No LSP check was applicable to these prose-only records.

## Limits

Did not edit the lesson, closure, scorecard, or any other lane file; only this scoped report was written. Did not verify receipt file membership independently beyond the closure’s statement.

## Installs

none
