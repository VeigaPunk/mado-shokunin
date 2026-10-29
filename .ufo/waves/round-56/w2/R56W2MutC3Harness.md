# R56W2MutC3Harness — mutation test of `quality/r56_ctl_c3.py` at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed

Seat: R56W2MutC3Harness (wave w2, falsify). Leaf member, no subagents, no lane edits, no git mutation of the lane.
Full mutant table, per-survivor arguments and verifications: `.ufo/waves/round-56/w2/R56W2MutC3Harness/mutants.md`.

## 1. Attacked

Item: **the C3 control harness itself** — `quality/r56_ctl_c3.py` at 28fc86ac (the nine mutations, their expected legs,
the shared-clone scratch builder, `judge_good` with exempt=24, `judge_control`). Attack hypothesis: wave 1 wrote each
artifact once and its own selftests are the only kill evidence; a one-line change to the harness could weaken its
discrimination while the printed line stays `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK`.

## 2. What I did

1. Read `claims-frozen-v2.md`, `registration-v2.md` (C3-v2 and E9/E12), `registration.md` §C3, `RULES.md`.
2. `git -C <lane> archive 28fc86ac…` into `/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness/tree` (read-only git; the lane is not written).
3. Built a reduced scratch repo `mini` whose blobs are the lane blobs at 28fc86ac (SOURCES.md, 71 entries, frozen-tables-v2.json,
   c3-name-only.tsv, the counter) and whose object store borrows the lane's via `.git/objects/info/alternates`, so the frozen
   base `13f0acbe` stays readable. Fidelity: `receipts/06-environment-note.txt` (all four inputs and the 71-entry listing
   identical by blob hash; base registry identical).
4. Oracle sanity (unmutated harness, real counter), `receipts/01-reference-oracle.txt`:
   ```
   A real counter           rc=0 stdout=MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
   B always-green stub      rc=1 stdout=MADO_R56_CONTROLS: claim=c3 good=ok controls=0/9 verdict=FAIL
  C every-leg-missed stub  rc=1 stdout=MADO_R56_CONTROLS: claim=c3 good=bad controls=8/9 verdict=FAIL   (allow_sha, exempt, tables_sha are absent from its missed list, so control 7 fails by design)
   ```
   Both stubs score FAIL, as required. A also reproduces against the REAL lane repo (`receipts/02-lane-crosscheck.txt`:
   `rc=0 … good=ok controls=9/9 verdict=OK`, 44.8 s).
5. Wrote 54 one-line mutants (`mutants.py`; each old fragment asserted to occur exactly once in the target): constant changes
   (N_CONTROLS, `"24"`, TIMEOUT), operator and inversion swaps, off-by-one slices and bounds, dropped legs and guards,
   removed `continue`, widened regexes, swapped arguments, the nine controls' own mutations, the scratch builder, and the judge.
   Each mutant was run through the UNCHANGED driver `quality/check-r56-controls.py --claim c3` three times:
   A with the real counter (must equal the OK line, rc 0), B with always-green, C with every-leg (both must FAIL).
   KILLED = any of A/B/C deviates; SURVIVED = all hold. `run_mutants.py`, `receipts/03-sweep.json`, `receipts/04-sweep.txt`.
6. For each survivor: an observable comparison against the reference (stdout and stderr), an argument for EQUIVALENT, or a
   proposed addition run against the pristine module (must pass) and the mutant (must fail). `verify_survivors.py`,
   `receipts/05-survivors.txt`, `receipts/08-verify-survivors-stdout.txt`, `survivor_verification.json`.
7. Probe (extra, not a mutant): does `judge_good` gate the population? `probe_population.py`, `receipts/07-population-probe.txt`.

## 3. Results

```
mutants=54 killed=29 survived=25 (EQUIVALENT 11, non-equivalent 14)
kill rate, shipped oracle, all 54:                 29/54 = 53.7%
kill rate, shipped oracle, non-equivalent 43:      29/43 = 67.4%
kill rate, with the 14 proposed additions, non-equivalent 43: 43/43 = 100%  (each addition: ref=pass, mutant=fail)
```

Of the 29 kills, 25 fail the GOOD-tree run (check A): 8 of them are the harness's own fail-closed SETUP errors (rc=2, empty
stdout, a `SETUP:` line on stderr; M22, M28, M39, M40, M42, M46, M53, M54), and 17 change the verdict line. Four are caught by
the control logic alone (M17, M18 via B; M19 and M45 via B or C). The silent-acceptance surface is the 25 survivors.

### 3.1 Survivors, mutated line, verdict

Non-equivalent (14), each killed by a verified addition:

| id | mutated fragment (old → new) | why it survives | addition (ref passes / mutant fails) |
|---|---|---|---|
| M13 | `if any(x not in ALL_LEGS …) or len(set…)` → `if len(set(missed)) != len(missed):` | parse_line accepts a bogus leg name in `missed` | parse_line on `missed=missing,totally_bogus_leg` must return None |
| M15 | counts `"missing": int(d["m"])` → `0` | self-consistency ignores missing= | parse_line on `missing=41 … missed=extra` must reject |
| M24 | `new = USEDBY_RE.sub(lambda m: "" if m.group(0)==path else m.group(0), cell)` → `…lambda m: "", cell)` | drop-one empties the whole used-by cell (9 paths) | exactly one path removed from exactly one cell |
| M25 | `continue` → `break` (control 3 loop) | dead on this tree (first sorted entry is listed); raises Setup when it is not | with first entry stripped from all cells, mut_drop_one must return, not raise |
| M26 | `for i, ln in enumerate(lines[:15])` → `lines[:150]` | dangling-source may pick a source: line outside the SRC window | synthetic: first entry source: at index 20, second at 3 → second must be mutated |
| M27 | `if sid == "S001":` → `"S002"` | ghost path written to the wrong row; note is hard-coded "of S001" | ghost path must be in S001's used-by |
| M29 | `s, path, li = sorted(cands)[0]` → `[-1]` | fences the last candidate, not the first | mutated entry must be the first sorted candidate |
| M30 | `lines[li:li+1] = ["```", lines[li], "```"]` → `["```", lines[li]]` | fence left open (5 markers) | ``` count must be even |
| M32 | `for (s, p), ls in sorted(pl.items()))` → `…[:1])` | allowlist with 1 row instead of 390 | allowlist row per pair |
| M36 | `ok = own[leg] > 0 if … else own[leg] > own_good[leg]` → `ok = own[leg] > 0` | no-op control accepted | patched harness + no-op control must exit 2 "ineffective" (empty mutation) |
| M37 | effectiveness check → `ok = True` | same | same as M36 |
| M38 | `if leg in ("missing","extra","dangling")` → `("missing","extra")` | dangling control not checked for effectiveness | no-op-entry control with leg=dangling must exit 2 |
| M44 | `m_ent.update({… if k_.startswith(KNOW+"/")})` → unfiltered | allowlist counted as an entry in control 7 (72 vs 71) | DIAGNOSTIC-level kill only: stderr must not report `entries counter=71 harness=72` |
| M52 | `CITE_RE = (?<![A-Za-z0-9])S[0-9]{3}(?![0-9])` → `S[0-9]{3}` | harness model matches inside identifiers | on `XS001 and S0021 and S003` only S003 may match (ref `['S003']`, mutant `['S001','S002','S003']`) — DIAGNOSTIC-level kill (verdict unchanged) |

Equivalent (11), each with an argument and byte-identical stdout and stderr against the reference (`mutants.md` §5):
M10 (`in d["missed"]` vs `in d["missed_list"]`, no leg name is a substring or contains `,`), M12 (`!= 1` vs `> 1` after the
`\n` check), M23 (reverse order of set-valued cell), M31 (reason column `y` vs `x`, never read), M33 (`count=0` vs `count=1`
on a token occurring exactly once: `occ != 1: continue`), M35 (` y` vs ` x`, stale still fires), M41 (`add -A` vs `-A -f`,
no target is ignored), M43 (drops the final newline after prose, not a row), M47 (drops the trailing newline of the allowlist,
still parsed), M49 (`python3` vs `python3 -I`, stdlib only, no shadowing), M50 (timeout 180→5 s: EQUIVALENT ONLY because a run
took 1.07–1.93 s here; margin ~2.6×, run-conditional).

Two of the 14 non-equivalent (M44, M52) are killed only at the stderr diagnostic; their scored verdict is unchanged. I label
them so rather than count them as verdict-level kills.

## 4. Defects (with the input that shows each)

| # | severity | defect | input / evidence |
|---|---|---|---|
| D1 | weakens the claim | 14 non-equivalent survivors of the harness (table §3.1); the shipped oracle cannot tell them from the good harness. | `results.json` status SURVIVED; `survivor_verification.json` verdicts KILLED_BY_ADDITION (14/14). |
| D2 | weakens the claim | `judge_good` does not gate the population: a green counter printing `entries=0 rows=0` scores `good=ok` on the unmutated harness. Only the controls (0/9) stop it; a counter that fakes missed legs would pass. Fix: compare `d["e"]`, `d["r"]` with the harness's own 71/328. | `receipts/07-population-probe.txt`: unmutated+empty stub `good=ok controls=0/9 verdict=FAIL`; patched+empty stub `good=bad`; patched+real counter `good=ok controls=9/9 verdict=OK`. |
| D3 | weakens the claim | Control-effectiveness is weak where it matters: controls 7/8/9 need only `bool(new_entries)`; the control-5 note is hard-coded to "S001" so a wrong-row mutation is invisible in diagnostics; the dangling leg is not checked (M38). | M27 and M38 survivors; `mut_ghost_path` note string. |
| D4 | weakens the claim | The harness's "independent" model is not the contract. On the GOOD tree it reports `missing=24` while the counter reports `missing=0`, because it does not implement the frozen allowlist exemption. The note prints on every run (`note[good]: … missing counter=0 harness=24`). Its effectiveness baseline for `missing` is therefore 24, not 0. Not scored, so no false verdict, but the stated cross-check is noise. | `receipts/01-reference-oracle.txt` and `receipts/02-lane-crosscheck.txt` stderr lines; harness metrics line `{'missing': 24, …}`. |
| D5 | cosmetic | The declared deviation D1 in the harness docstring is not what the code does. Docstring: scratch built from `git archive … corpus frozen-tables` (3 MB). Code: `git clone --shared --no-checkout` then `git checkout --detach` of the whole 27,734-file tree per control; `ARCHIVE_PATHS` is an unused constant. The harness is correct, but slow: 44.8 s on the lane, 2.8 s on the mini repo. | `git ls-tree -r --name-only 28fc86ac… \| wc -l` = 27734; lane run wall time 44.78 s. |
| D6 | cosmetic | Stale docstring: "holds the six frozen controls", "exit 0 only when good=ok and k=6". The harness has nine controls and prints `controls=<k>/9`. | `r56_ctl_c3.py` lines 6 and 19. |
| D7 | cosmetic (unverified by run) | Controls 3 and 6 do not exclude allowlisted pairs, though registration-v2 §C3-v2 says "first entry … that is not an allowlist pair" (control 3) and "first non-allowlist, single-occurrence citation" (control 6). Not exercised on this tree: `grep -n "S158\|S002" c3-name-only.tsv` returns nothing, so the chosen targets are not allowlisted. A future allowlist row on the chosen pair would silently change the control's target. By code reading only; no input constructed. | `mut_drop_one`, `mut_fenced_cite` source. |
| D8 | cosmetic | M50: the counter child timeout of 180 s has ~2.6× margin on a loaded machine (run times 1.07–1.93 s). Not a defect today; it makes M50 run-conditional. | `receipts/`; `mutants.md` M50 note. |

Not defects: the oracle's behaviour on the real counter and the real lane is exact and reproducible; the frozen tables, base
blob, allowlist and counter blobs in the mini repo match the lane byte for byte. The 8 rc=2 kills are the harness's own `SETUP:` fail-closed errors (checked on stderr), not uncaught exceptions.

Process note: my own first additions had two errors (an M52 test string that the contract's rule also matches, and a
patched-harness helper that re-wrote its reference into the mutant's file); both were corrected and every number in this
report comes from the final runs (`receipts/08`, `05`, `07`).

## 5. Null results (what I looked for and did not find)

* Oracle leaks: none. Both stubs fail on the good tree and on every control; no mutant made the real counter print a
  TARGET_MET line on a mutated tree (`judge_control` `"TARGET_MET" in out` check is exercised by M07).
* Missing-path or symlink false negatives in the scratch builder: not reached by any mutant (M40–M42, M45–M46 killed).
* Allowlist exclusion on the control targets: not exercised (see D7).
* Equivalence overclaim: each EQUIVALENT is backed by byte-identical stdout and stderr on this tree; the argument covers
  the code path, not all trees (M50 is run-conditional, see D8).

## 6. Not verified / limits

* Entailment of the registry text, sentence-to-pin audit, and the non-author closure are outside this seat's item.
* I did not construct an allowlist-collision input for D7, so D7 is by code reading.
* Mutants are one-line by design (as specified); multi-line or semantic mutants were not generated.
* The kill rate is a property of this 54-mutant table, not of the harness universe.
* Scratch was removed after the receipts were copied; `mutants.md` §7 reproduction needs `git archive 28fc86ac…` re-run into a scratch `tree/`.

## 7. Tooling

No tools installed or upgraded. Used the existing Python 3.14.8 (`python3 -I`), git 2.56.0. No pacman, no sudo, no
`uv tool`/`npm` installs. No host configuration read or changed. No subagent dispatched.

## 8. Deliverables

* `.ufo/waves/round-56/w2/R56W2MutC3Harness/mutants.md` — the report with the full mutant table and per-survivor arguments.
* `.ufo/waves/round-56/w2/R56W2MutC3Harness/mutants.py` — the 54-mutant table.
* `…/run_mutants.py` — the sweep driver (oracle A/B/C per mutant).
* `…/verify_survivors.py` — the survivor additions and their reference/mutant verification.
* `…/probe_population.py` — the population probe.
* `…/collect_receipts.py`, `…/make_mutants_md.py` — receipt and report generators.
* `…/stub_green.py`, `…/stub_legs.py` — the two oracle stubs.
* `…/receipts/` — 00 environment, 01 reference oracle, 02 lane cross-check, 03 sweep JSON, 04 sweep table, 05 survivors,
  06 fidelity note, 07 population probe, 08 survivor-verification stdout, 09 mini reference run, plus `results.json` and
  `survivor_verification.json`.
