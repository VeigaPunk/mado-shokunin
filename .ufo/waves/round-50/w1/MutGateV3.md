# MutGateV3 mutation probe

Target: round-49 draft `w1/ExecSessionShapes/check-session-material.py` (round-50 C2 v3 candidate), copied to isolated `/fast/scratch/hyaku/mado-r50/MutGateV3/check-session-material.py`. Detector: exact candidate `--selftest` with `HOME`, all XDG dirs, and `TMPDIR` rooted inside this scratch. Baseline: `SELFTEST: passed=94/94 failed=0`, rc 0. Twenty-two one-point mutants were run with the same detector. KILLED means nonzero detector; SURVIVED means detector returned 0; no baseline failure.

| Mutant | Result; observed selftest summary | Missing selftest case for survivor |
|---|---|---|
| R7 grep located-path delimiter `:`→`X` | KILLED; 90/94 | — |
| R8 account match owner-or-group→both | SURVIVED; 94/94 | Separate owner-only and group-only `ls -l` row cases must each find R8; current account case apparently does not distinguish requiring both. |
| R9 cache threshold `<`→`<=` | KILLED; 93/94 | — |
| default scope `all`→`ufo` | KILLED; 93/94 | — |
| Drop R7 from WAIVABLE_RULES | KILLED; 91/94 | — |
| home-listing threshold `>`→`>=` | KILLED; 93/94 | — |
| account resolver returns empty | SURVIVED; 94/94 | Exercise CLI default account resolution against a nonempty account-column fixture under a controlled account resolver, proving default invocation finds it; current cases only show explicit account and inert unresolved account. |
| synthetic home-user namespace becomes case-sensitive | SURVIVED; 94/94 | Marked fixture for a home-user token with alternate case (e.g. `Someone`) that must remain waivable; this asserts namespace case-insensitivity. |
| waiver roots `.ufo/waves/`→`.ufo/` | KILLED; 93/94 | — |
| broaden HOME_PATH_RE to any `/home/...` component | SURVIVED; 94/94 | R4 positive/negative boundary with a malformed username component (e.g. `/home/user name/...`) that must not count as a bare home listing. |
| R1 title/initialTitle `or`→`and` | KILLED; 83/94 | — |
| proc pid digit regex `\d`→`[0-9]` | SURVIVED; 94/94 | Not a semantic change for this regex in Python; equivalent mutant, not a useful gap. |
| serial minimum 4→5 | SURVIVED; 94/94 | Two-digit capital run serial-like token case; current cases include two capitals only, and should establish the min boundary via valid 3-capital token. |
| default home limit 10→11 | SURVIVED; 94/94 | CLI/default threshold boundary around exactly 11 distinct paths, distinct from explicit threshold case. |
| serial minimum 4→3 | SURVIVED; 94/94 | Two-digit capital run case should assert excluded adjacent boundary below the minimum, while 3-capital valid token is detected. |
| R6 serial matching case-insensitive | KILLED; 93/94 | — |
| R7 HOME_ANY_RE username class widened | SURVIVED; 94/94 | R7 `ls -l` row with malformed username component (slash/invalid username) that should not be recognized as a home path. |
| R8 account-column predicate inverted | KILLED; 87/94 | — |
| R9 cache `=`→`:` | KILLED; 90/94 | — |
| title fixture-prefix namespace made case-insensitive | KILLED; Python regex compilation error (invalid global flag placement), rc 1; no selftest summary | — (mutation invalid; excluded from semantic kill count). |
| waiver delta retain dropped findings instead of remove | KILLED; 65/94 | — |
| waiver target sha check bypass | KILLED; 92/94 | — |
| registry allows all RULES instead of WAIVABLE_RULES | SURVIVED; 94/94 | Registry row naming R5/R6 must be rejected even when that rule is otherwise known; marker-side serial rejection exists, but no isolated registry-validation case currently distinguishes the rule-set predicate. |

Summary: 22 attempted; 11 semantic mutants killed, 9 semantic survivors, 1 equivalent R2 regex mutant survived, 1 invalid-syntax mutation inconclusive. The first 20-mutant batch used a few incorrect anchors and is not counted; final report reflects only the corrected batch above. Restoration evidence: pristine rerun `SELFTEST: passed=94/94 failed=0`; scratch candidate and source both SHA-256 `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`; `cmp=identical`. No candidate/source bytes were modified. Scratch harness/copy remain under the assigned scratch root; no tracked lane files touched.
