# R70RevC1 — C1 predicate sound as bounded

Recommendation only; no admission/integration. Axes: calibration C1 (reviewed), operability C2 (unchanged; not reviewed). No blocking defect in the frozen successful predicate.

## Findings, severity order

- **Informational, disclosed discrimination limit:** `quality/counters/c1-r70-real-children.py:172-185,302-319` scores the extracted harness's `mz` answers, not the provenance of its decision. A stand-in reading `MODE=genuine` from the fixture source scores 3/3 without parsing a child assertion or spawning bash. This is a real counter limitation, not evidence that the scored harness cheats. The counter's opening declared-limits paragraph explicitly discloses agreement-by-coincidence; declaration C1 freezes three inputs and excludes universal coverage. Therefore not a blocker under that bounded sentence. Do not promote this result to proof of arbitrary harness authorship or all malformed-summary handling.
- **Informational, receipt diagnostics:** the candidate-absent path (`real-children.py:276-279`) prints `correct=absent base_correct=0` and exits 1 without running the base. This is not a measured baseline of 0/3. The declaration's independently measured base is 1/3. Successful-predicate labels/denominators match exactly; the absent diagnostic is the one qualification readers must disclose.
- **Informational, mutation robustness:** `contract_line()` hardcodes `cases=3`. A scratch module with MODES truncated to genuine/crash prints cases=3 despite executing two cases, but correct=2 and TARGET_MISSED; no false TARGET_MET. No production mutation was made.

## Frozen bytes attacked

All extracted with read-only `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 5144a6b5f43225d8021a469f4d24c19558026b9e:<path>` into own scratch. SHA256:

| Path | SHA256 |
|---|---|
| quality/counters/c1-r70-landing-controls.py | 71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58 |
| quality/counters/c1-r70-real-children.py | b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b |
| quality/counters/c1-r69-landing-controls.py | 9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73 |
| quality/counters/c1-r69-paired-recipes.py | 15a43adcb304b2f93cf373535f61d0be13b554f4abcdf9759215334536039088 |

Round-69 harness hash at b37a5aec4ea03f2223d8e09dd5d386d055c24179 is identical. Declaration hash: 01aa0d23d726f836d142e513e73ff70ee5b3d3618c8d8fe185f63585f731501a. Baseline receipt: 675b18dfbe257ac95e9951f89d9862d4f0ef4d696efb9a1ad64e91210eff1021. Proto: 9e31681dd95976af4b107566b1710a50d962b9af36d3e5db6b73078393c91b6f.

## Commands, exact verdicts, and evidence

Abbreviations solely for command readability:

```
R=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r70/R70RevC1
P=$R/.ufo/waves/round-70/w1/R70RevC1
REV=5144a6b5f43225d8021a469f4d24c19558026b9e
BASE=b37a5aec4ea03f2223d8e09dd5d386d055c24179
```

Exact full child outputs are retained under P, not merely inferred from semantic grep. Fixture mutation commands use explicit `git -C D`, assert toplevel equals D before committing, and specify fixture identity.

### 1. Do-nothing control independently reproduced

`python3 -I $S/rc.py --repo $R --rev $REV --base-rev $BASE --scratch-root $S/meas` → rc 0; exact last line:

```
MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=5144a6b5f43225d8021a469f4d24c19558026b9e
```

Full output: P/meas-full.txt. Real bash scenarios: genuine candidate/base pass/pass; crash fail/pass; garbage fail/pass. Thus base_correct=1/3, candidate_correct=3/3.

Independent fixture built directly from proto, not the counter fixture builder: `python3 -B $P/real-probes.py` → process rc 0. Its generated commands are `python3 -I $S/{r69,r70}.py --repo $S/fixture.4__z7zx0 --rev <fixture-sha> --scratch-root $S/real-<mode>-<version>`; exact revisions and outputs are retained in P/<mode>-<version>.log. Genuine revision 01b7553b5d24cadf6ffd9633d57fbdc998274eb0: r69/r70 rc 0/0, mz pass/pass. Crash 4aa489cb5cb1cf7df9f01a230e09b6c657364249: rc 0/1, mz pass/fail. Garbage e8bb95c602d480a83fae717b1ff43d45e8bf90af: rc 0/1, mz pass/fail.

Evaluated LANE_TEMPLATE equals proto bytes per mode. Lane SHA256 values exactly reproduce baseline receipt: genuine 96cf148ea48964331fb4ca19557e322a348127687b1b3a6492d1b3a3b7a9a2cc; crash e8562c3fa3e4e3c0747f8354192bb76f9ea5a7cea4a39bbd625f7912ecc3c33c; garbage 85dcd09cd619562c4a4f60b212395ccab1581fd8b5a4fb90f14bb94ba4216ff2.

### 2. Wrong-reason stand-ins

Retained source P/stand{A,B,C,E}.py. Each substituted only in a scratch fixture repo's candidate path, keeping the real base harness/children. Commands: `python3 -I $S/rc.py --repo $S/repoX --rev H --base-rev H --scratch-root $S/sX`.

| X | H | Decision | rc | Exact receipt score/verdict |
|---|---|---|---|---|
| A | b64b0ea961b0152e7f9a25b556a2543e1dce5998 | pass iff source MODE=genuine | 0 | cases=3 correct=3 base_correct=1 verdict=TARGET_MET |
| B | e8a6b01a3fec6e7d8a917b9d31b14ae946767ba8 | pass iff source contains SELFTEST | 1 | cases=3 correct=1 base_correct=1 verdict=TARGET_MISSED |
| C | 0a1d3ac9287aaca81e9768eb94ba0be2dfe41880 | always fail | 1 | cases=3 correct=2 base_correct=1 verdict=TARGET_MISSED |
| E | d9bd155623a3e57e2a4d282ab9ee183b866a9597 | no mz field on crash/garbage | 1 | cases=3 correct=1 base_correct=1 verdict=TARGET_MISSED |

Exact unabridged outputs: P/s{A,B,C,E}.log. A exposes oracle agreement only; B demonstrates that source mention alone does not pass. Frozen scored harness itself demonstrably uses parsed-summary conjunction, not these stand-ins.

### 3. Literal predicate binding

Mechanical comparison of declaration's literal with `contract_line(3,1,'<sha>')` returned True, character-for-character:

```
MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=<sha>
```

`verdict_met(3,1)=True`; (3,0), (3,3), (2,1), (0,1), (None,1) all False. CONTRACT_RE fullmatches emitted success with a 40-hex revision. Labels, successful numerators and denominators: no mismatch. Absent case qualification described above; exact observed line:

```
MADO_R70_REAL_CHILDREN: cases=3 correct=absent base_correct=0 verdict=TARGET_MISSED rev=b37a5aec4ea03f2223d8e09dd5d386d055c24179
```

### 4. Denominator attacks

`python3 -B $P/remaining.py` → process rc 0; imports scratch copy and mutates only its in-memory constants/callbacks.

- Truncated MODES=(genuine,crash): measure rc 1; exact line `MADO_R70_REAL_CHILDREN: cases=3 correct=2 base_correct=1 verdict=TARGET_MISSED rev=5144a6b5f43225d8021a469f4d24c19558026b9e`.
- Candidate crash callback raises TimeoutExpired: no successful return and no final contract emitted. CLI does not translate TimeoutExpired into a success; exception is uncaught.
- Missing scenario marker E: correct=1, rc 1 (above).
- Skipped base callback: rc 1, exact final line `MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=0 verdict=TARGET_MISSED rev=5144a6b5f43225d8021a469f4d24c19558026b9e`. P/denominator-extra.txt retains full trace and candidate-absent trace.
- Base absent: `python3 -I $S/rc.py --repo $S/repoNOBASE --rev 5ceaa54313b709946d84ebfa6fc5cbe398b9b74a --base-rev 67701b7e129d9e2c867cfefb36cca0807f64b28e --scratch-root $S/den2` → rc 2. Exact diagnostic in P/den2.log: `c1-r70-real-children.py: setup: quality/counters/c1-r69-landing-controls.py is absent at the base revision 67701b7e129d9e2c867cfefb36cca0807f64b28e`. No final contract.

Canonical logic: each mode contributes at most one to correct; missing marker contributes zero; frozen success requires exactly 3 and baseline exactly 1. No tested skip yielded TARGET_MET.

### 5. Fail-closed direction and edge summaries

Real bash probes via P/real-probes.py, not solely parser unit tests. Exact stdout/stderr-combined harness output retained in P/<case>-{r69,r70}.log. Each synthetic lane's live guard still passes 2/2; the clause-deleted child emits the test summary. M-R stayed pass in every run.

| Mutant output / exit | r69 mz; harness rc | r70 mz; harness rc |
|---|---|---|
| 1/2, exit 0 | fail; 1 | fail; 1 |
| -1/2, exit 1 | pass; 0 | fail; 1 |
| 999999999999999999999999/1, exit 1 | pass; 0 | fail; 1 |
| 0/999999999999999999999999, exit 1 | pass; 0 | pass; 0 |
| 0/2 then 2/2, exit 1 | pass; 0 | fail; 1 |
| 2/2 then 0/2, exit 1 | pass; 0 | pass; 0 |
| 0/2 on stderr only, exit 1 | pass; 0 | pass; 0 |

`last_summary` at harness:298-303 takes last marker in stdout+stderr concatenation; fullmatch at :324 rejects negative counts; :328 only requires positive total and passes<total. A huge positive total is accepted; no upper bound or cross-check against actual assertion events exists. Repeated markers are not rejected. Stderr markers count, and stderr wins over stdout in concatenated-block order, not chronological interleaving. These are residual limits, not universal fail-closed guarantees.

At :478 `mz_rc != 0 and summary_shows_failure(mz_out)` is a strict narrowing of r69's nonzero rule. A failed summary with exit 0 earns no kill: conservative false-negative direction, not a false green from the repair. It cannot widen r69's credited-kill set.

### 6. Every harness behavioral diff

Exact diff P/r69-r70.diff (`diff -u $S/r69.py $S/r70.py` rc 1, meaning differences).

Measurement changes: new summary_shows_failure and conjunction at :478; marker/TOOL/CONTRACT_RE prefixes renamed r69→r70; scratch work subdirectory renamed; R fixture commit user/email/message renamed r69-c1→r70-c1. No changes to extraction, env constructors, recipes, syntax check, M-R decisions, outcome functions, or denominators. Thus the claim 'everything else ... is the round-69 body' is not byte-literal (fixture metadata and work paths changed), but no additional scoring/decision weakening was found.

Nonmeasurement: rewritten docstring; selftest marker/filter renames; new scripted crash and allpass cases plus five parser checks; selftest scratch directory rename. No production edits.

### 7. Harm

`python3 -I $S/paired.py --repo $R --rev $REV --base-rev $BASE --scratch-root $S/paired` → rc 0. P/paired-full.txt exact last line:

```
MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=5144a6b5f43225d8021a469f4d24c19558026b9e
```

Additional instrument selftests: counter 26/26 rc 0 (P/rc-selftest.txt); harness 68/68 observed. Initial counter selftest attempt incorrectly used a nonexistent scratch subdirectory and returned a usage diagnostic; corrected by mkdir before the successful run. Initial stand-in attempts likewise used wrong-case/nonexistent scratch roots; corrected before results above. Initial raw-source template comparison failed because Python escape sequences had not been evaluated; evaluated template and independent fixture hashes match exactly. These setup failures are not instrument defects.

## Residual risk / verification gaps

LSP unavailable: reading xd://lsp returned 'No such tool'; no semantic server references/definitions/diagnostics were available. Review uses exact pinned source/diff and exercised subprocess evidence, not grep as semantic proof. No claim about C2, global gate, arbitrary runtime fault coverage, resume continuity (not in changed surface), or universal saturation. One three-case finite score only; retain the stand-in, duplicated/stderr-marker and unbounded-total limits in the final claim. No installations, desktop probes, production writes or lane git mutations.

Self-evaluation: accuracy 4 (exact pinned logs, explicit limits); completeness 4 (all seven attacks, no LSP); clarity 4 (numbered evidence); actionability 4 (sources and exact receipts retained); conciseness 3 (long because commands/output requested). Overall 3.8/5. Highest-impact improvement applied: real bash edge probes supplement scripted parsing tests. Recommendation: C1 predicate sound as bounded.

Scratch cleanup confirmed: `/fast/scratch/hyaku/mado-r70/R70RevC1` removed (`scratch_removed=True`). Evidence hashes: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/w1/R70RevC1/SHA256SUMS`. No production drafts, so draft SHA256: not applicable. Two retained Python files are review fixture drivers, not production proposals.
