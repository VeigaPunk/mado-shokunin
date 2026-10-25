# ConnRound30Cite — citation rule for rewritten round-30 seat reports

Scope: extract ScoutRound30's verdicts on the five rewritten round-30 files; write the citation sentence round-34 reports must use.

## Verdicts (quoted verbatim from `.ufo/waves/round-33/w1/reports/ScoutRound30.md`)

Overall: "**all five are real seat reports. Recommend commit (all five).**"

| file | verdict |
|---|---|
| `RevRecordsChain.md` | "yes — final pass re-pinned to `274f735`" — **commit** |
| `RevTrendExpansion.md` | "yes — supersedes the `274f735` draft" — **commit** |
| `SentScope.md` | "yes — full re-audit at `a0dd664` + new F12 finding" — **commit** |
| `RevTrendDiscernment.md` | "yes — complete advisory report at `274f735`" — **commit** |
| `SimplifierC2.md` | "yes — complete YAGNI review + post-report addendum" — **commit** |

## Commit state (verified at write time)

- All five files were committed together at `d40b35f90ad8bf630ad9404d25aeee1d9737f300` ("round-33: correct the false r32 C1 row, register the axis gate, and keep the killed coverage counter frozen"), an ancestor of HEAD (`fa7ba11346116672352b5d41494141c5c4d738d0`; `git merge-base --is-ancestor` = 0).
- `git status --porcelain` on the five paths: clean — no uncommitted rewrites.
- Superseded committed copies: `RevRecordsChain.md` and `RevTrendExpansion.md` had earlier drafts at `a0dd664`/`274f735`; `SentScope.md` had one at `15ddd7d`; `RevTrendDiscernment.md` and `SimplifierC2.md` first appear at `d40b35f`.

## Citation sentence (written to `.ufo/waves/round-34/scratch/ConnRound30Cite/cite.md`)

> The round-30 `<REPORT>` cited here is the rewritten, final-pass seat report verified by ScoutRound30 (round-33 w1) and committed at `d40b35f90ad8bf630ad9404d25aeee1d9737f300`; its earlier committed drafts (from the `15ddd7d`/`a0dd664`/`274f735` repair window) are superseded and must not be quoted.

Substitute the filename for `<REPORT>`. Required because HEAD reads and earlier blob reads of the same path differ — `git show <rev>:...` against `15ddd7d`/`a0dd664`/`274f735` yields stale content.

## Lane bounds

Leaf member: no subagents dispatched. Read-only on round-30/33 surfaces; writes limited to the scratch file and this report.
