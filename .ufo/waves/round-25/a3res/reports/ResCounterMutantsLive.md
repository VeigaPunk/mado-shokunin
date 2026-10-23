COUNTERMUT: killed 2/4 with a passing tool; survivors: skip-oracle-check, embed-threshold-1000.

# Residual counter-mutation probe

The two-input detector kills **expected-live** with the landed passing tool and **missing-only** with its deliberately wrong extra-entry variant. The passing tool alone kills 1/4; the reported 2/4 includes both assigned inputs. These are the four survivors from `a3w1/reports/MutCounterV4.md`; final-threshold-reversed was already killed there and is not in this denominator.

## Scope and axes

Read registration.md's Attempt 3 rule, including PRED-C1 (v4) and its kill rule. Axes: correct-tool acceptance, exact-multiset rejection (including duplicate multiplicity), oracle authority/drift protection, embed eligibility, and frozen-byte/process isolation. This is a mutation-coverage result, not a canonical judgment or a new C1 measurement claim. No counter, tool, registration, SCORECARD, or other lane source was edited.

Private scratch root (`R` below):
`/fast/scratch/hyaku/mado-r25a3/res/ResCounterMutantsLive`.

- Revision: `ef94763c6a75d1b0860091b19bb61c9bd7cda9e3`.
- Fixed diagnostic replay seed: `ed0d8a943980d2f2` (the supplied landed measurement's seed, not a fresh acceptance measurement).
- `R/tools/landed.py` is byte-identical to both the supplied lane tool and `git show ef94763c:tools/mado-binds.py`: SHA256 `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`.
- `R/tools/extra-entry.py` differs only at tool line 490: `json.dumps(st.entries)` becomes `json.dumps(st.entries + st.entries[:1])`. It duplicates the first fully resolved entry, changing multiset multiplicity without altering any entry fields or embedding a live table. SHA256 `c44ed314c3203823f4fa95d1c1bb5e78dd84e1840646803715d321e5d15931e2`.

All 41 generated tables were nonempty. Against the original counter, this variant had `missing=0 extra=1` in every case and was rejected 0/41. It is not merely invalid JSON or an empty-output control.

## Observed verdicts

Every cell below has `embed_hits=0`. MET means `TARGET_MET`, exit 0; MISSED means `TARGET_MISSED`, exit 1. A mutant is killed when either input's final verdict differs from the original counter on that same input.

| Counter | Landed tool | Extra-entry variant | Changed verdict? |
|---|---|---|---|
| Original frozen v4 | 41/41 MET | 0/41 MISSED | Reference |
| expected-live | 5/41 MISSED | 0/41 MISSED | **Killed: rejects the passing tool** |
| skip-oracle-check | 41/41 MET | 0/41 MISSED | No; survives |
| embed-threshold-1000 | 41/41 MET | 0/41 MISSED | No; survives |
| missing-only | 41/41 MET | 41/41 MET | **Killed: accepts the wrong variant** |
| Restored frozen v4 (expected-live copy) | 41/41 MET | 0/41 MISSED | Matches original |

Twelve complete counter CLI runs: two shared original controls, eight mutant/input combinations, and two shared restored controls. All completed on their first attempt with one predicate line and a normal exit 0 or 1. No setup failures, timeouts, or inconclusive runs occurred. This does not claim separate pristine/restored behavioral runs for every identical copy.

Every run reported:

```text
ORACLE_CHECK base_vs_live missing=0 extra=0
```

All twelve used the same 192-bind live capture, SHA256 `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`, and the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. Original/restored and non-expected-live mutants reported model agreement 41/41; expected-live reported 5/41. Model agreement was not used as a verdict.

## Counterexamples and impacted axes

### expected-live: changed authority causes false rejection

Sole mutation at counter line 275: `exp = truth[label][0]` → `exp = live`.

`R/receipts/mutated-expected-live-landed.txt:7-8`:

```text
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        FAIL missing=0 extra=1 oracle_binds=192 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=differs
```

Its final predicate is `cases_pass=5/41 embed_hits=0 verdict=TARGET_MISSED`, whereas the original and restored counter accept the identical tool at 41/41. BASE and the four UNSOURCED cases are the only passing cases. This is a concrete correct-tool acceptance and per-case oracle-authority regression, not an acceptable diagnostic tradeoff.

Smallest safe correction: retain `truth[label][0]` as each case's expected table; retain the passing-tool witness in the audit detector.

### missing-only: duplicate multiplicity is incorrectly accepted

Sole mutation at counter line 286: `ok = nm == 0 and ne == 0` → `ok = nm == 0`.

Original receipt `R/receipts/original-original-extra-entry.txt:7`:

```text
CASE BASE         FAIL missing=0 extra=1 oracle_binds=192 (unperturbed) v3_model=agree
```

Mutant receipt `R/receipts/mutated-missing-only-extra-entry.txt:7`:

```text
CASE BASE         PASS missing=0 extra=1 oracle_binds=192 (unperturbed) v3_model=agree
```

The same `missing=0 extra=1` difference occurs in all 41 cases. The original finishes `cases_pass=0/41 ... verdict=TARGET_MISSED`; the mutant finishes `cases_pass=41/41 ... verdict=TARGET_MET`. This violates exact multiset equality, not just ordering or presentation.

Smallest safe correction: retain both zero-missing and zero-extra conditions; retain the one-extra-copy negative control. No change to the landed resolver is indicated by this probe.

### Survivors are unexercised checks, not validated weakenings

- **skip-oracle-check**, counter line 266 `if nm or ne:` → `if False:`: all twelve BASE oracle checks had zero drift. Neither assigned input changes that upstream condition. [INFERENCE] A private snapshot/oracle-drift fault is needed to distinguish the guard; no such fault was injected here. The oracle-drift-protection axis remains uncovered by these inputs.
- **embed-threshold-1000**, counter line 236 `len(e[f]) >= 12` → `len(e[f]) >= 1000`: both assigned tool files had zero hits even under the original threshold. [INFERENCE] A semantically unchanged passing tool containing a live arg/description string of length 12–999 would distinguish the thresholds; that third input was not run. The embed-eligibility axis remains uncovered here.

Smallest safe correction to the earlier audit conclusion: update its detector coverage from these four surviving to two killed/two still unexercised. Keep the frozen contract and counter unchanged; neither surviving weakening is established as safe. No canonical judgment or admission is supplied by this review.

## Reconstruction, hashes, commands, and receipts

Five scratch layouts (`original` plus the four named mutants) each contain copied `count.py` and the unmodified pinned `count-v3.py`. As in the prior report:

```text
R/NAME/lane/.git -> /home/vgpnk/Projects/shokunin/mado-shokunin/.git
R/NAME/lane/.ufo/waves/round-25/c1/count.py -> R/NAME/count.py
R/NAME/lane/.ufo/waves/round-25/c1/count-v3.py -> R/NAME/count-v3.py
```

The logical invocation path preserves v3's five-directory LANE calculation. The `.git` link is used only by read-only revision resolution; no git/jj write command ran. All child environments remove `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`.

Original counter SHA256 (`F4`): `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`.
Pinned generator SHA256 (`F3`): `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.

| Mutant | Mutated counter SHA256 |
|---|---|
| expected-live | `0252183e62efae3e25416b241652673e749d46ad40e512b09efad4b3b5b579c8` |
| skip-oracle-check | `0cd3e5ed93560adece2757add398ca84788c10d3bb56e81038648c039b48d926` |
| embed-threshold-1000 | `578ca2b3907142888baa98c1582c35e21557ffdad3eead631a9ce292c692b01a` |
| missing-only | `b08c0aa8def9dfd60e9c3da2076fe230d41f4b47dca84e6dd1cb5524fd56ed63` |

These exactly match the four mutations in the prior report. All four counter copies were reverse-edited after the matrix; the restored driver asserted their SHA256s were F4 before running its two restored controls. Every generator used in a run was checked against F3.

Executed phase commands (R expanded to the absolute scratch root):

```sh
timeout --kill-after=20 3400 prlimit --as=4000000000 --core=0 --fsize=33554432 python3 -I -B R/probe.py matrix
timeout --kill-after=20 1200 prlimit --as=4000000000 --core=0 --fsize=33554432 python3 -I -B R/probe.py restored
```

Each concrete command is retained in phase metadata, with this shape:

```sh
timeout --kill-after=15 600 prlimit --as=4000000000 --core=0 --fsize=33554432 python3 -I -B R/NAME/lane/.ufo/waves/round-25/c1/count.py ef94763c6a75d1b0860091b19bb61c9bd7cda9e3 --tool-file R/tools/TOOL.py --seed ed0d8a943980d2f2 --jobs 2
```

The supplied instance signature is set only if absent. At most two counter commands run concurrently, with two oracle workers each and the frozen six-slot host-wide lock. All oracle results came from the counter's own nested-Hyprland `oracle()` on exec-stripped copies; all tools used its unchanged bubblewrap sandbox. No mocked tables or substitute comparator were used.

Evidence under R:

- `probe.py`: retained bounded driver.
- `matrix-results.json`: all ten original/mutated commands, hashes, case lines, predicates, exits, timings, capture identities, and process-cleanup results.
- `restored-results.json`: the two restored controls with the same metadata.
- `receipts/original-original-{landed,extra-entry}.txt`.
- `receipts/mutated-{expected-live,skip-oracle-check,embed-threshold-1000,missing-only}-{landed,extra-entry}.txt`.
- `receipts/restored-expected-live-{landed,extra-entry}.txt`.

Each receipt includes combined stdout/stderr and an `exit=N` trailer. Every run's private-TMPDIR process scan found no leftovers before or after the driver's cleanup; a final `/proc/*/cmdline` scan found no process containing this private scratch root. Counter-created temporary case trees were removed. Counter copies are restored, while tool copies and receipts remain as evidence.

No package/tool installation or update, service/config change, live-compositor write verb, model call, or external judge runtime was performed. Only this report was written in the lane.
