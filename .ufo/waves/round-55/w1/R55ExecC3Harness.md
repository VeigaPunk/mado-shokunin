# R55ExecC3Harness — C3 control harness (draft for L1)

## Deliverables (all under `.ufo/waves/round-55/w1/R55ExecC3Harness/`)
- `r55_ctl_c3.py` — module exposing `run(argv)->int`; to be installed beside `quality/check-r55-controls.py` (the dispatcher imports `r55_ctl_c3`).
- `transcript.txt` (+ `run_tests.sh`, `mk_good_repo.py`) — full test run; `dispatcher-run.txt` — run through the committed dispatcher.
- Test fixtures (NOT deliverables to commit): `min_counter_c3.py` (my own minimal counter), `stub_green.py`, `stub_red.py`, `stub_silent.py`, `lazy_noprefix.py`, `lazy_noreadme.py`, `lazy_p23.py`.

## What it does
`--repo --rev --work [--counter PATH]`. Resolves `--rev`; scratch repos are `git init` + `objects/info/alternates` onto `--repo`'s object store (nothing copied, lane never written), `rev-parse --show-toplevel == $D` asserted, mutated commit built by plumbing (`read-tree`, `hash-object -w`, `update-index --cacheinfo`, `write-tree`, `commit-tree` with `-c user.name=ctl -c user.email=ctl@ctl`, every call `git -C "$D"`) on top of `--rev`, counter run as child (`python3 -I`, cwd/HOME/TMPDIR = scratch work subdir, minimal env). Counter default = `quality/counters/c3-r55-p19.py` read from git at `--rev`; absent → good=bad, 0/6. Scratch repos removed in `finally`. stdout is exactly the one `MADO_R55_CONTROLS: claim=c3 ...` line (diagnostics on stderr); exit 0 OK / 1 FAIL / 2 setup (`MADO_R55_CONTROLS: SETUP usage|rev_unresolvable|repo_unreadable|counter_unreadable|base_entry_unreadable`).

Controls (mutation is built from the good entry bytes at `--rev`; base bytes from `3b55b6e:<entry>`):
1 absent = entry replaced by base bytes; 2 rewritten-prefix = `PRESSED`→`PRESSEd` in the base P19 row; 3 altered-quote = Q09 `key - 8`→`key - 9`; 4 old-arm-only = Q08–Q12 rows deleted; 5 old-wording = P23 cell 3 := P19 cell 3; 6 readme-missing = `P23` removed from the README line(s) naming the errata file. A no-op mutation is a failed control.

Judgment per run: exactly one `MADO_P19_FIX:` line, grammar-exact, `rev` echoes the passed rev, verdict/`missed=none`/exit status (0 MET, 1 MISSED) consistent, `prefix|pin|p23|readme` fields consistent with the `missed` legs, no unknown legs, no `MADO_R55_CONTROLS` text in counter stdout. Good = MET, `identical rows=13/13 pin=ok p23=ok readme=ok`. Each mutant must be `TARGET_MISSED` with: required legs present, only whitelisted legs, and exact `rows=<a>/13` (CTL-1 0, CTL-3 12, CTL-4 8, others 13), `prefix`/`p23`/`readme` field values (table in `CONTROLS`). `tables_sha` is forbidden in every control (nothing alters the tables); `pin` is allowed only on CTL-3 (quote ≠ pin line, per the frozen `pin` leg wording).

## Transcript (decisive lines; `transcript.txt` has all)
```
min_counter_c3.py : MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK        rc=0
stub_green.py     : good=ok, every mutant "admitted (verdict TARGET_MET)" -> controls=0/6 verdict=FAIL rc=1
stub_red.py       : good=bad controls=0/6 verdict=FAIL                                  rc=1
stub_silent.py    : good=bad controls=0/6 verdict=FAIL (no MADO_P19_FIX line)           rc=1
lazy_noprefix.py  : good=ok controls=5/6 verdict=FAIL (CTL-2 admitted)
lazy_noreadme.py  : good=ok controls=5/6 verdict=FAIL (CTL-6 admitted)
counter absent at rev, no --counter : good=bad controls=0/6 FAIL
counter committed at rev (no --counter): good=ok controls=6/6 OK
--rev deadbeef / no --rev / --bogus : MADO_R55_CONTROLS: SETUP rev_unresolvable|usage|usage   rc=2
dispatcher copy (quality/check-r55-controls.py + module) : good=ok controls=6/6 verdict=OK rc=0
```
Test good tree = real `3b55b6e` tree + appended `## Correction (round 55)` block built from `frozen-tables.json` c3.q (read from lane commit `54dacbd`) + README line edited to name P23, committed in a scratch repo with alternates on the lane. It is synthetic: the L1's real block and the real counter were not available to me, so the real pair has NOT been exercised.

## Defects / ambiguities found
1. **CTL-2 block location (contract gap).** After a one-byte change in the prefix, where "the block" starts is undefined. My first minimal counter located the block by `len(base)` and so reported rows 0/13 on CTL-2; I asserted rows=13/13 and my own control failed. Registration only says CTL-2 → `prefix`. I made CTL-2 collateral-tolerant: require `prefix`+`prefix=changed`, allow `rows:*`, `pin`, `p23`, forbid `readme`/`tables_sha`. A counter that also flags `readme` on CTL-2 fails the control; flag if the real counter does.
2. **CTL-5 does not pin the p23 token list.** `lazy_noprefix`-style weakening works as expected, but `lazy_p23.py` (p23 leg with the `== 0` and `otherwise|any other|else` requirements deleted) passes 6/6, because the frozen old-wording mutation (P19 sentence) lacks `m_passPressed`-forms/`== 0`/`RELEASED`/`otherwise` all at once, so any one of the checks catches it. Individual token requirements of the `p23` leg are therefore unfalsified by the six frozen controls (a registered-limit, not a harness bug).
3. CTL-1's wording "prefix-clean but rows+p23 missed" is implemented as `rows=0/13`, ≥1 `rows:` leg, `p23` missed, `readme` ok. A counter that omits individual `rows:Qnn` legs but prints rows=0/13 passes only if at least one `rows:` leg exists.
4. Strictness choices beyond the frozen text that the real counter must satisfy: exact `rows=<a>/13` counts; `rev=` echo of the sha I pass (I pass the resolved full sha, and for mutants the new commit sha); counter must exit 1 (not 2) on a verdict miss; `missed=` entries limited to `prefix,pin,p23,readme,tables_sha,rows:Qnn`. The real counter reads the base entry via `3b55b6e` — harness repos keep it reachable (alternates); a counter that needs the *working tree* or a ref other than `--rev` will fail.
5. Dispatcher passes `--holdout` only for c2; c3 treats it as usage error (harness rejects unknown args).

## Not verified
Not run against the real C3 counter, the real appended block or the real README row (none existed). `frozen-tables.json` is not read by the harness (it holds expectations itself); `tables_sha` leg is only checked as "never reported on any control". Host/hyprctl not touched. No hold-out path seen. Tools installed: none. Scratch `/fast/scratch/hyaku/mado-r55/R55ExecC3Harness` removed.
