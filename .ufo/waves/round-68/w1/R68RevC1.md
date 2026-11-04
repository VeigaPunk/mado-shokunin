# R68RevC1 — adversarial review of claim C1 (round 68, wave 1)

- date: 2026-11-03; lane base `510100c81e6cf63fec6be380c2f2f9c670f32cbc`; lane tip `40d2bef8964a098ae50f01094fa19e4725952010`
- reviewed bytes: `quality/counters/c1-r68-selfmutants.py` (worktree == tip blob; file history: last commit `2ca2bec3`, i.e. pre-freeze — never modified after freeze) and `quality/counters/c1-r68-landing-controls.py` (worktree sha256 `25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527` == blob at `40d2bef8`; `git diff --stat e0727cda 40d2bef8 -- quality/counters/` shows only this new file, +834).
- All runs executed by this seat; no self-attestation accepted. No tool installs were needed (none performed).

## Verdict

**C1 predicate SOUND as bounded.** The frozen counting command reproduces the declared Before and After exactly; the three frozen recipes each occur exactly once in the candidate and are killed by its selftest; the do-nothing control genuinely scores the r67 harness at the base rev; the scripted cases drive the real `measure()` body; the printed contract line is the one the counter asserts. Survivors found are exactly the class the declaration's Limits carve out (multi-point decision+oracle forgeries and crash-credit widenings the three single-point recipes cannot reach) — no re-scoping needed, but the concrete survivor shapes are recorded below for the lesson.

## Per-check results (command → rc → key lines)

1. Counter selftest — `python3 -I quality/counters/c1-r68-selfmutants.py --selftest` (lane root):
   `MADO_R68_SELFMUTANTS_SELFTEST: 26/26 assertions passed`, rc=0.
2. Frozen command at base (Before leg) — `python3 -I quality/counters/c1-r68-selfmutants.py --repo . --rev 510100c8… --base-rev 510100c8… --scratch-root <scratch>`:
   rc=1, last line `MADO_R68_SELFMUTANTS: selftest=absent killed=0/3 applied=0/3 base=0/3 verdict=TARGET_MISSED rev=510100c81e6cf63fec6be380c2f2f9c670f32cbc` — identical to `.ufo/waves/round-68/control-baseline-r68.txt`. `MADO_R68_BASE_EXTRACT … sha256=a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58` ✓ equals the required r67-harness digest (also re-hashed independently: `git cat-file blob 510100c8:quality/counters/c2-r67-landing-controls.py | sha256sum` → same).
3. Frozen command at tip (After leg) — `--rev 40d2bef8…`:
   rc=0, last line `MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=40d2bef8964a098ae50f01094fa19e4725952010` — the declaration's After predicate, candidate extract sha256 `25470bc4…f5527`.
4. Scratch-repo candidate leg — fixture repo: `git init` in `$S/repo.XXXX`, toplevel asserted == fixture dir, `git fetch <lane> HEAD`, `checkout --detach 510100c8…`, commit the candidate harness on top (HEAD `6b055c18c473db22c7f7c1c6a453dd4418dfe0a5`), then one invocation `--repo "$D" --rev HEAD --base-rev 510100c8…`:
   rc=0, `…killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=6b055c18…`. The counter extracts from ONE repo per run; both legs are satisfied because the scratch repo carries the fetched base history — it scored the candidate blob from HEAD (sha256 `25470bc4…`, identical to the lane legs) and the r67 base harness from `510100c8` inside the scratch repo (sha256 `a4376fa7…`, byte-identical).
5. Hand-applied frozen recipes (copy of harness, exact replace, `--selftest`): S1 rc=1 51/52 fail `scripted none-killed prints the miss line`; S2 rc=1 51/52 same; S3 rc=1 50/52 adds `scripted none-killed exits 1`. Mutant sha256s `7bacfa10…/867b4894…/dd284ac4…` match the counter's own `recipe_sha256` values — hand and counter agree.
6. Break-the-selftest battery: see table. Each edit applied at exactly one occurrence (asserted), compile-checked, then `--selftest`.
7. Scripted-body evidence: with `_scripted_run` patched over module `run` (as `_measure_case` does), both scripted cases' captured output contains: 4× `MADO_R68_EXTRACT …`, `MADO_R68_SELFTEST instrument=… rc=0 assertions=62/62`, `MADO_R68_MUTANT M-Z … recipe=clause-delete …` (first mutant copy executed), `MADO_R68_R_CONTROL fixture_rev=cccc… real_tree=bbbb… forged_tree=dddd… forged_visible=yes guarded_visible=no` (returns from `build_r_fixture` after planting and cross-checking the `refs/replace` fixture), `MADO_R68_CHILD_ENV no_replace_objects=absent keys=…`, `MADO_R68_R_CHILD role=unmutated rc=1 verdict=TARGET_MISSED missing=1 control=green` (first `run_r_child`), `MADO_R68_MUTANT M-R … recipe=line-delete removed_line='env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")\n' …` (second mutant copy via second `run_r_child`), and the final `MADO_R68_LANDING_CONTROLS:` line (`killed=2/2 … TARGET_MET` / `killed=0/2 … TARGET_MISSED` per case).
8. No-spawn enforcement — quoted from harness `selftest()`:
   ```python
   saved_run = subprocess.run
   def _no_spawn(*_args, **_kwargs):
       raise AssertionError("selftest must not spawn a process")
   subprocess.run = _no_spawn
   try:
       try:
           checks = _selftest_checks(work)
       except AssertionError:
           checks = [("selftest body must not spawn a process", False)]
   finally:
       subprocess.run = saved_run
   ```
   The scripted path additionally substitutes `globals()["run"]` in `_measure_case`, and `measure()`/helpers spawn only through that module-level `run`; the scripted `run` returns `subprocess.CompletedProcess` without spawning. Verified behaviorally: I removed the guard (mutant I) and the scripted cases still ran green without spawning.
9. Contract-line assertion — counter source: `met = result["rc"] == 0 and result["killed"] == len(RECIPES)`; `CONTRACT_RE` fullmatches the tip final line (True) and the baseline final line (True). The harness's own `contract_line()` output is pinned by exact-string `want`s in `_scripted_checks` (both directions) and the harness `CONTRACT_RE`.

## Break-the-selftest battery (killed vs survived)

| id | exact edit (find → replace, 1 occurrence each) | selftest | verdict |
|---|---|---|---|
| S1 (frozen) | `mr_killed = bool(` → `mr_killed = True or bool(` | rc=1 | KILLED |
| S2 (frozen) | `mz_killed = mz_rc != 0` → `mz_killed = True` | rc=1 | KILLED |
| S3 (frozen) | `killed = int(mz_killed) + int(mr_killed)` → `killed = 2` | rc=1 | KILLED |
| A | `return rc == 0 and marker == ("TARGET_MET", 0)` → `return True` (`forged_credit`) | rc=1 51/52, fail `forged credit is rc0 + TARGET_MET + missing=0` | KILLED |
| B | `return rc == 1 and marker == ("TARGET_MISSED", 1)` → `return True` (`control_ok`) | rc=1 48/52, fails `control rejects forged read` / `control rejects setup error` / `scripted both-killed …` | KILLED |
| C | `return 0 if selftest_rc == 0 and killed == 2 else 1` → `return 0` (`outcome_exit`) | rc=1 49/52, fails `one kill is a miss` / `red selftest is a miss` / `scripted none-killed exits 1` | KILLED |
| D1 | S2 **plus** oracle edit `selftest=0 mz=fail mr=fail killed=0/2 ` → `… mz=pass mr=fail killed=1/2 ` | rc=0 52/52 | **SURVIVED** |
| D2c | S3 **plus** consistent oracle edits (`killed=2/2`, `TARGET_MET`, `rc2 == 0`) | rc=0 52/52 | **SURVIVED** |
| G | `mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)\n and forged_credit(mr_rc, mr_marker))` → same without the `forged_credit` term | rc=0 52/52 | **SURVIVED** |
| L | `mz_killed = mz_rc != 0` → `mz_killed = mz_rc != 0 or mz_rc is None` | rc=0 52/52 | **SURVIVED** |
| I | `subprocess.run = _no_spawn` → `pass  # spawn guard disabled by R68RevC1` | rc=0 52/52 | **SURVIVED** |
| H | `outcome_verdict` → constant `"TARGET_MET"` | rc=1 49/52 | KILLED |
| K | `mz_killed = mz_rc != 0` → `mz_killed = mz_rc is not None` | rc=1 51/52 | KILLED |
| D2/D2b | my first two forgery attempts with **inconsistent** oracles (`mr=pass`/`mz=pass` where the mutated body prints `mr=fail`/`mz=fail`) | rc=1 | KILLED (my bug, not the selftest's — recorded as oracle-tightness evidence) |

Mutant sha256s: S1 `7bacfa10…`, S2 `867b4894…`, S3 `dd284ac4…`, A `c03cc917…`, B `f8da9f54…`, C `2a75e223…`, G `bc2d71bc…`, H `cde0c195…`, I `8bfeb342…`, D1 `7c8f2863…`, D2 `6f11c7b6…`, D2b `4df8a1c2…`, D2c `c4a98f34…`, K `3c321d9d…`, L `8753a591…`.

## Which credit-forgeries survive — the claim's boundary, made concrete

1. **D1/D2c (decision+oracle, two-point):** any forgery that edits a kill-credit site *and* the matching expected line in `_scripted_checks` stays green. The frozen recipes are single-point by construction, so the counter cannot see these. (Declaration Limits: "does not prove the harness's own mutants are exhaustive" — this is that limit, instantiated.)
2. **G (credit widening at the M-R gate):** dropping `forged_credit` from `mr_killed` credits a kill for *any* mutant-child outcome except the exact control outcome — including rc=2 / unparseable marker (child crash) in a real measurement. All three recipe target texts are still present exactly once, so the counter still scores 3/3 TARGET_MET on this harness.
3. **L (credit widening at the M-Z gate):** `or mz_rc is None` credits a kill when the M-Z recipe itself errors (clause count ≠ 1, `bash -n` failure) — recipe-inapplicability still reports a kill. Also invisible to the counter (S2 still applies and dies).
4. **I (hermeticity weakening, not credit):** removing the no-spawn guard keeps 52/52; the counter scores rc only, so it cannot detect a selftest that spawns. Today's harness enforces it (check 8); nothing pins it for the future.

A, B, C are **not** survivors: the suggested forgeries of `forged_credit`/`control_ok`/`outcome_exit` are each pinned by direct unit assertions and/or scripted-case coupling. K and H show the oracle also catches cruder credits. D2/D2b show the exact-line oracle rejects inconsistent forgeries — only a self-consistent multi-edit forgery passes.

## Findings by severity

- **No defect in the frozen predicate.** All legs reproduce exactly; chronology clean (counter unmodified since pre-freeze `2ca2bec3`; only the harness was added at `40d2bef8`).
- **Boundary finding (within declared limits, report to lesson):** survivors G and L are real credit forgeries reachable in a real measurement run, invisible to the frozen counter. If the round wants a harder successor, the frozen recipe set would need paired (decision+oracle) recipes or outcome-set recipes (crash ≠ kill), e.g. asserting `mz_killed` is False when `mz_rc is None` and `mr_killed` implies a well-formed forged marker.
- **Minor:** the hermeticity assertion is itself unguarded against removal (I survives); acceptable for this round's predicate.

## Residual risk / verification gaps

- I verified the harness's kill logic against scripted children only (per the frozen denominator); the real `landing-counters.sh`/`mado-receipt-citecheck.py` run at the measured revision is the harm-watch leg, owned by another seat — not re-run here.
- The `MADO_R68_SELFTEST_FIXTURE assertions=` display parses the harness summary line; a harness printing a bogus summary but rc 0 would display wrong numbers without changing the kill/verdict logic (kill is rc-based). Cosmetic only.

## Provenance & hygiene

- Probe scripts copied for audit into this seat directory: `probe_c1.py` (sha256 `b3abc699…6765d61040`), `probe_c1b.py` (`c74dfa97…af3000e`), `probe_c1c.py` (`deefcf76…946d0b6`) (mutants themselves were scratch-only and deleted with the scratch root).
- Scratch `/fast/scratch/hyaku/mado-r68/R68RevC1/` (incl. fixture repo `repo.XXXX`, mutant copies, staged selftest dirs) removed before yield.
- No lane git/jj mutation, no pacman transaction, no desktop/compositor probe, no writes outside the seat directory, this report, and the scratch root.
