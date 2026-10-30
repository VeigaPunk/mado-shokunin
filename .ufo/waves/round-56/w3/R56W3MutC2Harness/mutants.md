# R56W3MutC2Harness — mutation test of the round-56 C2 control harness

Revision attacked: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (lane tip; the attacked blobs are identical at the
content revision `8a7b7346…`):
- `quality/r56_ctl_c2.py` sha256 `080d772037608a9c2fe2ee033a463d681575e0a220df1f8e5bc8c1489062923e`
- `quality/check-r56-controls.py` sha256 `e34ef1b95dd181081da5b08f972715b47f49066854181d4f96706caac5489f2e`

Attack framing (seat): the C2 artifacts landed once and their selftests/harness runs are the only kill evidence.
Question: does the landed harness run — the frozen claim's own observable plus the fail-closed behaviour — actually
kill one-line defects in the harness itself, and which defect classes slip through?

## 1. Verdict in numbers

46 one-line mutants, all run through the full 11-probe battery (528 harness runs):

| verdict | count | meaning |
|---|---|---|
| KILLED-ORACLE | 31 | the frozen claim's own evidence catches the mutant (green line or fail-closed refusal changes) |
| KILLED-EXTENDED | 7 | green line intact; caught only by an added discrimination probe (coverage gap in the claim's evidence) |
| KILLED-DIAGNOSTIC | 3 | green line intact; caught only by E10/E6 residue (work-dir leftovers) |
| SURVIVED | 5 | no probe distinguishes the mutant (4 non-equivalent, all with verified killing additions; 1 argued equivalent) |

Kill rates: oracle 31/46 = **67.4 %**; + extended 38/46 = **82.6 %**; + diagnostic 41/46 = **89.1 %**
(41/45 = 91.1 % excluding the one argued-equivalent mutant).

No pristine-harness defect was found by the exercise; what it found is (a) seven defect classes the frozen
predicate cannot see (§4), (b) four sandbox-flag drops invisible to the entire fixture+control surface (§5),
(c) an E10 residue of the pristine harness on the refusal path (§6).

## 2. Method

1. `git archive 0f3a5436… | tar -x` into a fresh scratch repo; `git init`; toplevel asserted = the scratch dir;
   committed as `base` (`df3285c985ba668eba14d3ea02a0c108ce8b6aa0`, tree = the lane tip tree). All later git calls
   name `-C` that repo; identity `-c user.name=ctl -c user.email=ctl@ctl`; lane never touched.
2. Nine PROBE commits, each `base` + exactly one change (tool copy, ctl stub, one appended note byte), plus two
   invocation modes that hide bwrap inside a private mount namespace (`unshare -rm` + `mount --bind /dev/null
   /usr/bin/bwrap`; the host file is untouched, the mount dies with the namespace):
   - P1_base — honest exported tool copy at the tip (the seat's main oracle run);
   - P2_nobwrap_refusal — bwrap hidden, no flag → the fail-closed refusal;
   - P3_nobwrap_degraded — bwrap hidden + `--no-sandbox` → the degraded run must report `sandbox=none`;
   - P4_cheat_tool — a tool that replays `<display-root>/expected.out` (the answer key beside the tree);
   - P5_broken_tool — a tool that prints a plausible but wrong watch plan;
   - P6 / P8 — one appended byte in a committed / hold-out `note.txt` (commitment flip, no scoring change);
   - P7a / P7b / P7c — control stubs that over-answer (empty→1, const-host→2, lookup-committed→17 committed);
   - P9_wrongrc_tool — a tool that prints F01's expected bytes but exits 1.
3. 46 one-line mutants, each applied to a fresh COPY of the harness in scratch (asserted single-anchor; one anchor
   was ambiguous on the first pass — E09 — and was re-anchored and re-run in stage 2). Every mutant ran all 11 probes.
4. Classification (stage 3, `classify.py`): ORACLE = P1 (rc + stdout line) + P2 (rc ≠ 0, empty stdout, refusal
   marker) + P3 (rc + stdout line + `sandbox=none` token); EXTENDED = P4–P9 (rc + stdout line); DIAGNOSTIC =
   work-dir leftovers, stderr `fixture_commit` token.
5. Every non-equivalent survivor and every extended-kill got a proposed smallest addition, applied to a scratch
   copy of the pristine harness plus the mutant copy, and verified: pristine+proposal stays green, mutant+proposal
   is caught (`verify2.py`; all checks PASS).

Baseline (pristine, read-only against the lane, writes only under `--work`):

```
python3 -I quality/check-r56-controls.py --claim c2 --repo <scratch repo> --rev df3285c9… --work <w>
-> MADO_R56_C2: rev=df3285c9… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET  (rc 0)
   stderr: r56_ctl_c2: sandbox=bwrap fixture_commit=ok control_scores={'const-host': (1, 0), 'empty': (0, 0),
           'sibling-reader': (0, 0), 'lookup-committed': (18, 0)}
```

Determinism of the P1 observable was cross-checked against the lane's own receipt
(`receipts/at-final.txt`, same line at `8a7b7346…`), and P2/P3 reproduce the registered fail-closed and degraded
behaviours exactly (P2: rc 2, empty stdout, `setup error: bwrap is not installed…`; P3: green line,
`sandbox=none`). A probe whose pristine outcome is degenerate would have been reported inconclusive; none was.

## 3. Full mutant table

`target` C = `quality/r56_ctl_c2.py`, D = `quality/check-r56-controls.py`. `∅` = the token is deleted.

| id | family | target | mutation | verdict | killed by |
|---|---|---|---|---|---|
| B01 | sandbox | C | drop `"--unshare-all"` from the bwrap argv | SURVIVED | — (PR-jail kills) |
| B02 | sandbox | C | drop `--ro-bind /usr /usr` | KILLED-ORACLE | P1,P5,P6,P7a,P7b,P7c,P8 |
| B03 | sandbox | C | drop `--tmpfs /w` | KILLED-ORACLE | P1,P5,P6,P7a,P7b,P7c,P8 |
| B04 | sandbox | C | drop `--chdir /w` | SURVIVED | — (PR-jail kills) |
| B05 | sandbox | C | drop `--symlink usr/lib /lib` | SURVIVED | — (PR-jail kills) |
| B06 | sandbox | C | drop `--dev /dev` | KILLED-ORACLE | P1,P6,P7a,P7b,P7c,P8 |
| B07 | sandbox | C | drop `--ro-bind stage stage` | KILLED-ORACLE | P1,P6,P7a,P7b,P7c,P8 |
| B08 | sandbox | C | drop `--ro-bind program program` | KILLED-ORACLE | P1,P5,P6,P7a,P7b,P7c,P8 |
| B09 | sandbox | C | drop `--die-with-parent` | SURVIVED | — (PR-argv kills) |
| B10 | sandbox | C | `not _NO_SANDBOX[0]` → `not _NO_SANDBOX[1]` (IndexError instead of the refusal) | KILLED-ORACLE | P2,P3 |
| B11 | sandbox | C | sandbox token `"bwrap" if _BWRAP else "none"` → always `"bwrap"` | KILLED-ORACLE | P3 |
| D01 | denom | C | `a == 18` → `a == 17` in `met` | KILLED-ORACLE | P1,P3 |
| D02 | denom | C | `b == 8` → `b == 7` in `met` | KILLED-ORACLE | P1,P3 |
| D03 | denom | C | `ctl_ok == 4` → `ctl_ok == 3` in `met` | KILLED-ORACLE | P1,P3,P7a,P7b,P7c |
| D04 | denom | C | `COMMITTED_IDS` `range(1, 19)` → `range(1, 18)` | KILLED-ORACLE | all 10 line probes |
| D05 | denom | C | `HOLDOUT_IDS` `range(1, 9)` → `range(1, 8)` | KILLED-ORACLE | P1,P3,P6,P7a,P7b,P7c,P8 |
| D06 | denom | C | const-host bound `<= 1` → `<= 2` | KILLED-EXTENDED | P7b |
| D07 | denom | C | empty/sibling-reader bound `== 0` → `<= 1` | KILLED-EXTENDED | P7a |
| D08 | denom | C | lookup-committed `c_pass == 18` → `== 17` | KILLED-ORACLE | all 10 line probes |
| D09 | denom | C | lookup-committed `c_pass == 18` → `>= 17` | KILLED-EXTENDED | P7c |
| D10 | denom | C | drop `ho_commit == "ok"` from `met` | KILLED-EXTENDED | P8 |
| D11 | denom | C | drop `fx_ok` from `met` | KILLED-EXTENDED | P6 |
| D12 | denom | C | drop `ctl_ok == 4` from `met` | KILLED-EXTENDED | P7a,P7b,P7c |
| E01 | expect | C | `rc == exp_rc` → `rc != exp_rc` (and stdout inverted) | KILLED-ORACLE | all 10 line probes |
| E02 | expect | C | `out == exp_out` → `out != exp_out` | KILLED-ORACLE | all 10 line probes |
| E03 | expect | C | `and` → `or` between the rc and stdout comparisons | KILLED-ORACLE | all 10 line probes |
| E04 | expect | C | `rc is not None` → `rc is None` | KILLED-ORACLE | all 10 line probes |
| E05 | expect | C | `passed += 1` → `passed += 2` | KILLED-ORACLE | all 10 line probes |
| E06 | expect | C | `exp_rc = int(...)` → `exp_rc = 0` | KILLED-ORACLE | all 10 line probes |
| E07 | expect | C | commitment record drops its trailing `b"\n"` | KILLED-ORACLE | P1,P3,P4,P5,P6,P7a,P7b,P7c,P9 |
| E08 | expect | C | commitment sort key `r[0]` → `r[1]` | KILLED-ORACLE | P1,P3,P4,P5,P6,P7a,P7b,P7c,P9 |
| E09 | expect | C | `if os.path.islink(full):` → `if False:` in the rows loop (symlinks hashed as file content) | KILLED-ORACLE | P1,P3,P4,P5,P6,P7a,P7b,P7c,P9 |
| E10 | expect | C | drop the `rc == exp_rc` comparison | KILLED-EXTENDED | P9 (+ PR-wrong-rc verified) |
| S01 | staging | C | `{FX}` → the export fixture dir instead of the stage | KILLED-ORACLE | P1,P3,P6,P7a,P7b,P7c,P8 |
| S02 | staging | C | drop `fid` from the stage path | KILLED-ORACLE | all 10 line probes (cleanup `dirname` then deletes `--work`) |
| S03 | staging | C | `copytree(..., symlinks=True)` → `symlinks=False` | KILLED-ORACLE | P1,P3,P4,P5,P6,P7a,P7b,P7c,P8,P9 |
| S04 | staging | C | shared cwd `work/cwd` instead of `work/cwd-N` | KILLED-DIAGNOSTIC | P2 (leftover name only) |
| S05 | staging | C | `os.makedirs(cwd)` → `os.makedirs(cwd, exist_ok=True)` | SURVIVED | — (EQUIVALENT, argued) |
| S06 | staging | C | staged tree copied to `stage/TREE` | KILLED-ORACLE | P1,P3,P6,P7a,P7b,P7c,P8 |
| S07 | staging | C | `copytree(fx, stage/tree)` (whole fixture dir incl. `expected.out`) | KILLED-ORACLE | P1,P3,P6,P7a,P7b,P7c,P8 |
| S08 | staging | C | per-fixture cleanup `rmtree(dirname(stage))` → `rmtree(stage)` (parent leaks) | KILLED-DIAGNOSTIC | leftovers on 10 probes |
| S09 | staging | C | per-fixture cleanup `rmtree(cwd)` → `pass` | KILLED-DIAGNOSTIC | leftovers on 10 probes |
| S10 | staging | C | shared stage `work/stage` | KILLED-ORACLE | all 11 probes |
| X01 | dispatch | D | `MODULES["c2"] = "r56_ctl_c1"` | KILLED-ORACLE | all 11 probes |
| X02 | dispatch | D | `sys.path.insert(0, os.path.dirname(HERE))` (import breaks) | KILLED-ORACLE | all 11 probes |
| X03 | dispatch | D | `if claim in MODULES:` (check inverted) | KILLED-ORACLE | all 11 probes |

Per-mutant receipts: `receipts/<id>/{P*,mutant.json}` (stdout, stderr, rc per probe; before/after hashes in
`mutant.json`), plus `receipts/summary.json`, `receipts/classified.tsv|json`.

## 4. Coverage gaps in the frozen predicate (seven mutants the claim's own evidence cannot see)

All seven keep the exact green line on the honest tree at the tip. Each has a verified killing addition; the
probes were run against the mutant in scratch, and each is small enough to be a round-57 registration change.

| mutant | weakened rule (registration-v2 §C2 / E6 / E7) | why the frozen evidence is blind | verified kill |
|---|---|---|---|
| D06 | "ctl/const-host.py passes at most 1 of the 26" (bound `<=1`) | the committed const-host stub scores exactly (1,0); any bound ≥ 1 accepts it | P7b — a const-host stub answering F01+F02: pristine 3/4 TARGET_MISSED, mutant 4/4 TARGET_MET |
| D07 | "ctl/empty.py passes 0; ctl/sibling-reader.py passes 0" (bound `==0`) | both committed stubs score 0 | P7a — empty answering F01: pristine 3/4 MISSED, mutant 4/4 MET |
| D09 | "ctl/lookup-committed.py passes 18/18 committed and 0/8 hold-out" | the committed stub scores exactly (18,0) | P7c — lookup answering F01–F17: pristine 3/4 MISSED, mutant 4/4 MET |
| D10 | the hold-out commitment gates the verdict | on the clean tree `holdout_commit` is "ok" | P8 — one appended byte in H01/note.txt: pristine `holdout_commit=bad` MISSED, mutant MET |
| D11 | the fixture commitment gates the verdict | on the clean tree `fixture_commit` is ok | P6 — one appended byte in F01/note.txt: pristine `fixture_commit=bad` MISSED, mutant MET |
| D12 | `controls=4/4` gates the verdict | no committed control ever fails | P7a/P7b/P7c — pristine MISSED, mutant MET |
| E10 | stdout bytes AND exit status are compared | all 26 fixtures' expected.rc match the honest tool's rc, so the rc leg is never differentially exercised | P9 — a tool printing F01's expected bytes but exiting 1: pristine 0/18 MISSED, mutant 1/18; and PR-wrong-rc (below) |

Proposals, verified in scratch (`verify2.py`, `receipts/proposals/`):

- **PR-wrong-rc** (kills E10): add `ctl/wrong-rc.py` — it replays a committed fixture's expected.out but exits 1 —
  as a fifth control in the "passes 0 of 26" family, denominator 5. Verified: pristine+proposal →
  `controls=5/5 … TARGET_MET` (rc 0); E10+proposal → `controls=4/5 … TARGET_MISSED` (rc 1).
- The other five are killed by registering the three negative control stubs of P7a/P7b/P7c (a stub that over-answers
  must be rejected) and a tamper self-check for D10/D11: the P6/P8 runs already are the mutant runs against the
  proposed additions, in scratch.

## 5. Sandbox-flag drops invisible to the entire fixture + control surface

B01, B04, B05, B09 survive all 11 probes. The jail each builds was probed with a fixed report program
(`receipts/jail-shape-probe.txt`; no further probes were run after the operator stop):

| mutant | jail shape observed | claim impact |
|---|---|---|
| B01 (no `--unshare-all`) | host network namespace shared: `ifaces = ['lo','enp7s0','docker0',…]`, pid = host pid | no answer-key channel opens (the export is not bound into the jail; `/proc` is not mounted), but a tool gains host network reach — the isolation property is no longer pinned by any lane test |
| B04 (no `--chdir /w`) | jail cwd is `/` (jail root listing) instead of the empty `/w` tmpfs | E6's "empty staging cwd" is no longer what runs; no observable in any fixture |
| B05 (no `usr/lib → /lib`) | `/lib` absent; python still runs via `/lib64` | fidelity loss, not a leak; no observable |
| B09 (no `--die-with-parent`) | in-jail shape identical to pristine (pid 2, ppid 1) | matters only if the harness dies mid-run; never exercised by a scored run |

Proposals, verified in scratch (`receipts/proposals/PR-jail`, `PR-argv`):

- **PR-jail** (kills B01, B04, B05): the harness must self-probe the jail it builds — run a fixed probe program
  through the same `staged_run` and require `{cwd: /w, /proc absent, interfaces == ['lo'], /lib present}`; a
  deviation flips the verdict. Verified: pristine+proposal → the unchanged green line `TARGET_MET` (rc 0);
  B01/B04/B05+proposal → `TARGET_MISSED` (rc 1).
- **PR-argv** (kills B09): the harness must assert its own bwrap argv still carries `--die-with-parent` and
  `--unshare-all` (fail closed otherwise). Verified: pristine+proposal → `TARGET_MET`; B09+proposal → rc 2
  `setup error: sandbox flag missing…`.

S05 (`os.makedirs(cwd, exist_ok=True)`) is argued EQUIVALENT: `_stage_n[0]` increments before each cwd build, so
`work/cwd-N` is unique per fixture and `exist_ok` never fires; identical observables on all 11 probes. The argument
is from the code plus the battery, not an exhaustive input differential.

## 6. Pristine observations (no mutant needed)

- **O1 — the fail-closed path leaks its stage into `--work` (E10 letter).** When bwrap is absent the harness
  refuses (rc 2) but the per-fixture cleanup is skipped, so `--work` keeps `stage-1/F01/tree/…` (a copy of the
  committed fixture files) and `cwd-1` (`receipts/…/P2_nobwrap_refusal`). No answer key is exposed (the stage never
  contains `expected.*`), but registration E10's "removes what it created before exit" does not hold on the failure
  path. Severity: cosmetic. The same blind spot is what makes S04/S08/S09 diagnostics-only kills.
- **O2 — the degraded `--no-sandbox` run still certifies 18/18.** With bwrap hidden and `--no-sandbox` given, the
  harness runs unsandboxed and the honest tool still scores `TARGET_MET` with `sandbox=none` on stderr (P3). This
  is the documented opt-in waiver, not a defect; it is recorded because the wave-3 dispatch wording — "run without
  bwrap: must refuse with sandbox=none" — conflates the two paths: the landed refusal prints
  `setup error: bwrap is not installed…` (no `sandbox=` token), and `sandbox=none` appears only on the waived
  path. Severity: cosmetic / documentation; B10 and B11 confirm both paths are load-bearing.

## 7. Defect list (severity per seat convention)

| id | finding | severity |
|---|---|---|
| D1 | control acceptance bounds are loose and there are no negative controls: D06, D07, D09 (and D12) keep the green line | weakens the claim |
| D2 | the commitment terms are invisible on the clean tree: D10, D11 keep the green line | weakens the claim |
| D3 | the exit-status comparison is invisible: E10 keeps the green line | weakens the claim |
| D4 | sandbox-flag drops B01/B04/B05/B09 are invisible to every fixture and control | weakens the claim (isolation guarantees unpinned) |
| D5 | refusal path leaves `stage-1`/`cwd-1` in `--work` (E10 letter, pristine) | cosmetic |
| D6 | per-fixture stage/cwd cleanup is invisible to the claim line (S08/S09 diagnostics-only) | cosmetic |
| O2 | dispatch wording "refuse with sandbox=none" vs landed refusal text (see §6) | cosmetic / documentation |

Every D1–D4 entry has a verified killing addition in scratch (§4, §5); none is applied to the lane — they are
round-57 material (the claims, counters, kill rules and targets are frozen).

## 8. Limits and explicitly unverified items

- The battery is bounded: one host (bwrap 0.13.1, python 3.14.8, git 2.56.0), 11 probes, one mutant ordering. A
  different host without user namespaces could change the B-family outcomes; not tested.
- The no-bwrap probes are simulations (private mount namespace hiding `/usr/bin/bwrap`), not a host without
  bubblewrap. `shutil.which("bwrap")` returning None was verified directly.
- The proposal patches (PR-wrong-rc changes the printed control denominator to `/5`; PR-jail adds a stderr-only
  self-probe; PR-argv adds an argv assertion) are scratch simulations of round-57 changes, never applied to the
  lane. PR-wrong-rc's denominator bump is itself a registration change that round 57 would have to freeze.
- S05's equivalence is argued (code reading + 11-probe identity), not an exhaustive differential over all inputs.
- B09's parent-death behaviour was not executed (operator stop); only the in-jail shape and the argv assertion are
  evidenced.
- Tool semantics (mado-watchplan.py) are out of scope here — wave 2 seats R56W2MutC2ToolA/B covered them at
  `28fc86ac…`; the tool blob is unchanged since `8a7b7346…` (blob `089c2a69…`), so their findings carry.
- Cleanup of `--work` between probes was verified only for the probes run here (P1–P9 on the good tree).

## 9. Reproduce

```
S=/fast/scratch/hyaku/mado-r56/R56W3MutC2Harness
D=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3MutC2Harness
python3 -I $D/driver.py   $S $D     # stage 1: 46 mutants x 11 probes (~4.5 min, 6 workers)
python3 -I $D/verify2.py  $S $D     # stage 2: E09 rerun + proposal verifications
python3 -I $D/classify.py $D        # stage 3: tier classification -> receipts/classified.tsv|json
```

Tooling: nothing was installed or upgraded (python3, git, tar, bwrap preinstalled; no pacman transactions).

Scratch `/fast/scratch/hyaku/mado-r56/R56W3MutC2Harness` was removed after the deliverables were copied. The lane
was never written to except this seat's deliverable directory and report; `quality/r56_ctl_c2.py` and
`quality/check-r56-controls.py` in the lane are byte-identical to the tip blobs (sha256 above), and
`git status --porcelain --untracked-files=no` in the lane is empty.
