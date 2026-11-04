# R72ScribeEntryC2 — scoped report

## Behavior and axes

C1: calibration, kill credit requires the run's own failure detail. C2: operability, harness outcome reads the gate's own summary rather than its exit status. This seat drafted only the C2 knowledge entry; no harness, counter, control, receipt, registry or product file changed.

Draft: `.ufo/waves/round-72/w1/R72ScribeEntryC2/draft/corpus/knowledge/outcome-verdict-gate-summary-r72.md`.

The draft includes the three-key frontmatter, one-sentence rule, complete helper decision table, four held-wrong cases and explanations, contradiction-by-summary limit, measured 8/8 versus 4/8 results and exact receipt, source URLs/S444/S445, and the finite function-only scope. It distinguishes harness outcome exit from counting-command exit and labels implementation-only table rows as not additional measured controls.

## Gates and provenance

Read frozen declaration first. Existing `.ufo/waves/round-72/measurement-c2-r72.txt` records `cases=8 correct=8 base_correct=4 verdict=TARGET_MET` at instruments `9bcb4fd5b598844f168230dc05e441721d95b272`, with `C2_RC=0`; base is `976684a27e99c2508037a60eec415f550f53d70e`. This seat did not run those gates, counters, tests, builds, formatters, runtimes or fixture drivers. No new verification result is claimed.

Read existing functions `summary_green`, `outcome_exit`, `outcome_verdict`, C2 counter extraction/scoring, frozen eight-case JSON, held r71 functions, source receipts and corpus source rows. Local CPython source receipts were present and quoted, but absent from the observed HEAD inventory; they are not represented as committed execution evidence. L1 confirmed S444/S445 are working-tree mined rows and fetches are currently uncommitted. No source fetch or source installation was performed by this seat.

### Exact shell commands and outcomes

1. `mkdir -p /fast/scratch/hyaku/mado-r72/R72ScribeEntryC2/ /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/R72ScribeEntryC2/draft/corpus/knowledge/` — success, no output.
2. From `/home/vgpnk/Projects/shokunin/mado-shokunin`: `git ls-tree HEAD -- .ufo/waves/round-72/claims-declaration-r72.md quality/counters/c1-r72-landing-controls.py quality/counters/c2-r72-outcome.py .ufo/waves/round-72/controls/c2-controls-r72.json .ufo/waves/round-72/measurement-c2-r72.txt quality/counters/c1-r71-landing-controls.py .ufo/waves/round-72/fetch/Doc_library_unittest.rst.1 .ufo/waves/round-72/fetch/Lib_unittest_main.py.1` — success; six committed blobs listed, no fetch entries. Blob identities: declaration `41a1811e3aa4b9cdb78a18235704bcaa432054cb`; controls `6cb26f7d6460fafa3781a1fbb9bd7553e848e30f`; receipt `566dbfdafb6c7432298cc89b6cf195f65e681d4f`; held harness `1b1e293c3e80863061911f039e19b91f9537cb5b`; successor `c39f38a5dd057646e1703191929af5c0acc19acd`; counter `6c241f5d87197e4d9f361b5bc9076c1205d5c53b`. This inventory establishes committed presence, not a fresh execution or independent worktree-byte comparison.
3. `rmdir /fast/scratch/hyaku/mado-r72/R72ScribeEntryC2/` — success, no output; empty scratch removed, no scratch receipts to preserve.

Reads/searches used specialized tools. One source-registry search used the nonexistent root `SOURCES.md` and returned “Path not found”; the actual `corpus/SOURCES.md` was provided by L1 and read successfully. All artifact writes used write/edit and stayed within this seat's directory. No git/jj mutation, host probe, credentials, PATH-directory write, service restart, or install/update occurred.

## Findings and known limits

- Held errors are exactly `failing-summary-exit0`, `green-summary-exit2`, `no-summary-exit0`, `garbled-summary-exit0`.
- The declaration says **last parsed** summary; implementation actually selects the last prefixed line and then parses it. A later malformed prefixed line blocks fallback to earlier valid text. Draft records this precisely without claiming the frozen eight cases test that combination.
- The counter calls committed decision functions; it does not execute a whole harness. No end-to-end claim is added.
- Summary/status contradiction is scored by the summary by design. No authenticity or process-health guarantee follows.
- Source references are local receipt context; publication/mining and any execution evidence remain L1-owned.

## Scope conflict (verbatim) and resolution

“Your ONLY write directory is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/<your name>/.”

“Report: write your scoped findings to .ufo/waves/round-72/w1/R72ScribeEntryC2.md”

The requested report filename is beside, not inside, the only write directory. Strict bound wins; report is here inside the directory. L1 expressly agreed: “Correct call: strict directory bound wins — put the report at .../w1/R72ScribeEntryC2/report.md, never a file beside the dir.” No sibling-level report was written.

## Touched surfaces and out of scope

Created draft and this report only; created then removed own empty scratch. Permanent corpus publication, index/ledger/registry changes, frozen receipts, lane code, judging, commits and verification are intentionally untouched and owned by L1. The supplied recheck command is for L1, not an executed command here.

## Self-evaluation

Accuracy 4/5: exact existing result and function behavior cited, but no independent worktree-byte comparison was performed. Completeness 4/5: all draft requirements covered; source receipts remain explicitly local. Clarity 4/5: selector wording discrepancy requires extra explanation. Actionability 4/5: ready-to-integrate draft and exact recheck provided; integration is intentionally not performed. Conciseness 4/5: provenance adds length but prevents execution overclaim. Overall 4.0/5. Highest-impact actions for L1: preserve the local/committed source distinction during integration; retain selector caveat unless separately resolved. Would the user agree: likely, because no additional measured or execution claim is invented.
