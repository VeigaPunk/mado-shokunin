# CritFailClosed — round 36 wave 1 critic seat report

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (LANE).
Reviewed: `quality/check-counter-discrimination.py` (C1) and `quality/check-evidence-pointers.py` (C2), both at the live tip `ea89bde` (the wave's hardening commit) *and* at their pre-hardening refs. All probes ran from `/tmp` clones/harnesses; nothing production was modified.
Gate refs cited by line: C1 = `check-counter-discrimination.py` HEAD; C2 = `check-evidence-pointers.py` HEAD. Pre-hardening behavior observed on the committed versions from before `ea89bde`.

## Summary of verdicts

| # | Probe | Gate | Verdict | Status at HEAD |
|---|---|---|---|---|
| T1 | Manifest truncated to the 3 accept controls (reject controls dropped) | C1 | **FAIL-OPEN** | present |
| T2 | Frozen spec file missing, instrument that ignores it | C1 | **FAIL-OPEN** | present |
| T3 | Instrument prints `verdict=TARGET_MET` then exits 1 | C1 | was FAIL-OPEN; now fail-closed | **fixed by ea89bde** |
| T4 | Instrument prints MET then aborts (rc=-6) | C1 | fail-closed | present |
| T10 | Instrument exits 2 while printing MET | C1 | fail-closed (ERROR) | fixed by ea89bde |
| T-timeout | Instrument hangs past TIMEOUT | C1 | fail-closed (`ERROR`, exit 124) | present |
| T6 | Malformed JSON manifest | C1 | fail-closed but uncaught traceback (exit 1) | present |
| T5/T7 | Empty / missing manifest | C1 | fail-closed (die exit 2) | present |
| T8/T9 | Unwritable / non-directory receipts path | C1 | fail-closed but uncaught traceback (exit 1) | present |
| B1 | `## Round 36` heading renamed → `## Round-36` | C2 | fail-closed (setup=missing-r36-sections) | present |
| B2 | `## Round 360` / `## Pre-round 36` substring headings added; prose-only body | C2 | **FAIL-OPEN for the R36 pointer clause** (still exit 0) | present |
| B3 | `corpus/lessons/round-36.md` empty / heading-only | C2 | fail-closed (MISSED) | present |
| B4 | Dangling R35 citations silently deleted from R35 records | C2 | fail-closed (`record_intact`/`named` fence) | present |
| B5 | `--repo` = bare clone (no worktree; `git status` fails) | C2 | **FAIL-OPEN** (`inherited_dirty` reads 0; exit 0) | present |
| B6 | Hostile ambient `GIT_DIR` exported before the gate | C2 | was FAIL-OPEN; now fail-closed | **fixed by ea89bde** |
| B7 | `--rev` naming a tag / arbitrary commit / pre-tip commit | C2 | exit 0 on any tree containing R36 records; unanchored claim | present |

## Details — C1 (`check-counter-discrimination.py`)

### T1 — manifest truncation (FAIL-OPEN, at HEAD)
The gate never pins the manifest's size or identity. `manifest = json.loads(...)`; `controls = manifest.get("controls") or []`; only `if not controls: die("manifest-empty")` (C1:97-100). The final `met = correct == total` (C1:196) is evaluated against whatever N the caller-supplied manifest happens to contain. There is no check that the manifest id is `MANIFEST-r36-v1` or that N=25 / the reject set is present.

Probe (HEAD, `/tmp/mado-cur-c1`, stub instruments scoring MET; stub files are copied into `quality/counters/` so `scripts` is non-empty):

```
$ python3 -I check-counter-discrimination.py --profile r36 --manifest manifest-3accept.json --repo . --no-receipts
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-golden-r36 instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-live instrument=c2 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=3 correct=3/3 label='round-36 repaired counters' verdict=TARGET_MET
exit=0
```

`controls=3 correct=3/3` → exit 0, while the frozen manifest's 22 reject controls are absent. The claim "25 controls, 3 accept / 22 reject, all classified correctly" is not what was measured. Same class: a manifest that rewrites every reject's `expect` to `TARGET_MET` passes identically. If count/identity pinning is intended, the gate must verify `manifest["id"] == "MANIFEST-r36-v1"` and the exact expected control ids/count against a frozen constant.

### T2 — missing frozen spec (FAIL-OPEN, at HEAD)
`--frozen` is passed to the instrument; the gate itself never reads or validates the frozen spec. Fail-closed behavior for drift/missing frozen is entirely delegated to the instrument. The repaired counters do die on both (verified):

```
$ python3 -I quality/counters/c2-ledger.py --repo . --frozen .ufo/waves/round-36/c2/no-such.json
PRED-C2-r36-v1 error=frozen-missing
exit=2
$ python3 -I quality/counters/c1-idle-lock.py --root . --frozen .ufo/waves/round-36/c1/frozen.json   # drifted target
PRED-C1-r36-v1 error=target-drift
exit=2
```

But an instrument that does not self-check passes: with `met_exit0.py` (prints MET, exits 0, tolerates a missing frozen file) and the frozen files removed from the harness repo, the gate reported:

```
$ python3 -I check-counter-discrimination.py --profile r36 --manifest manifest-allmet.json --repo . --no-receipts
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=2 correct=2/2 label='round-36 repaired counters' verdict=TARGET_MET
exit=0
```

So the gate is fail-open with respect to the frozen spec when the instrument is; the "frozen spec" guarantee is an instrument property, not a gate property. A cheap fix: the gate itself checks `(repo / prof[inst]["frozen"]).is_file()` and dies `frozen-missing` before scoring (mirroring `manifest-missing`).

### T3 — verdict printed, exit 1 (FAIL-OPEN pre-hardening; FIXED at HEAD)
Pre-hardening `observed_of` (old lines 68-72) returned the printed verdict regardless of rc unless rc==2, so `print("verdict=TARGET_MET"); sys.exit(1)` scored `ok=1` and the gate exited 0:

```
# pre-hardening observed
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-live instrument=c2 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
MADO_DISCRIMINATION: ... verdict=TARGET_MET
exit=0
```

HEAD `observed_of` (C1:68-79) requires `rc == 0` for MET and `rc == 1` for MISSED; anything else → ERROR. Re-run of the same probe at HEAD:

```
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=ERROR ok=0
control=c2-live instrument=c2 clause=- expected=TARGET_MET observed=ERROR ok=0
MADO_DISCRIMINATION: ... verdict=TARGET_MISSED
exit=1
```

Closed.

### T4 / T10 — abort and exit-2 with MET printed (fail-closed)
`os.abort()` → rc=-6; `observed_of` maps to ERROR (no `rc==0` match) → MISSED, exit 1. Exit 2 with MET printed → ERROR → MISSED. Both fail-closed.

### Timeout — fail-closed
`run()` catches `TimeoutExpired` → `(124, "<timeout>")` (C1:59-65); `VERDICT` doesn't match → ERROR → MISSED. Verified with TIMEOUT patched to 3s and a 15s-sleep instrument: `observed=ERROR`, exit 1.

### T6/T5/T7 — malformed/empty/missing manifest
- missing file → `die("manifest-missing")` exit 2 (fail-closed);
- `"controls": []` → `die("manifest-empty")` exit 2 (fail-closed);
- malformed JSON → uncaught `JSONDecodeError` traceback, exit 1. Fail-closed, but not a clean `die`; the same class of unhandled error applies to any `json.loads` failure (C1:97).

### T8/T9 — unwritable receipts path
`receipts_dir.mkdir(parents=True, exist_ok=True)` (C1:131) raises uncaught OSError when the path is unwritable (e.g. `/proc/mado-test` → `FileNotFoundError`; an existing file → `FileExistsError`). Both exit 1 without a verdict line. Fail-closed, but again an unhandled traceback rather than `die`.

## Details — C2 (`check-evidence-pointers.py`)

### B1 — heading rename (fail-closed)
`sections(text, "Round 36")` (C2:98-106) matches only a line that *starts with* `## ` and contains the needle substring. Renaming `## Round 36` → `## Round-36` empties the R36 section:

```
PRED-PTR-r36-v1 rev=master ... pointers_r36=24 ... setup=missing-r36-sections verdict=TARGET_MISSED
exit=1
```

Fail-closed.

### B2 — substring heading collision (FAIL-OPEN for `dangling_r36`, at HEAD)
`sections` uses substring containment, so any heading containing `Round 36` is swept into the R36 section; a heading like `## Round 360` or `## Pre-round 36` is merged with the real R36 section. Adding such sections with prose-only bodies still yields exit 0:

```
# added "## Round 360\nplaceholder prose with no pointers\n" and "## Pre-round 36\nplaceholder prose again\n" to LOG.md
PRED-PTR-r36-v1 rev=master ... pointers_r36=35 dangling_r36=0 ... verdict=TARGET_MET
exit=0
```

Also, `dangling_r36 == 0` is vacuous when the section cites no pointers (zero pointers → zero dangling). The clause "dangling_r36 == 0" does not require that any pointer be cited; a prose-only R36 section trivially satisfies it (B2 above, and B3b's heading-only lesson with a disposition line would too). This is the weakest clause: it catches renamed headings only exactly, and it never checks that records cite the evidence they are supposed to cite.

### B3 — lesson file empty / heading-only (fail-closed for exit 1; weak pointer clause)
Empty `corpus/lessons/round-36.md` → `setup=missing-r36-sections`, `scratch_disposition_ok=0`, MISSED, exit 1. Heading-only lesson → `setup=ok` but `scratch_disposition_ok=0` (no disposition line) → MISSED. Fail-closed, but only because the disposition clause fails; the pointer clause itself stays vacuous.

### B4 — record rewrite (fail-closed)
Deleting the two SUPERSEDED citations from the R35 LOG.md section:

```
$ python3 -I quality/check-evidence-pointers.py --repo .
PRED-PTR-r36-v1 ... pointers_r35=6 dangling_r35=0 dangling_r35_closed=0 ... verdict=TARGET_MISSED
exit=1
```

`record_intact` (C2:160) and the `named` supersession fence (C2:167-169) both fail. The anti-rewrite fence works.

### B5 — bare `--repo` (FAIL-OPEN, at HEAD)
`git()` (C2:75-79) returns `""` on any non-zero exit, swallowing `git status`'s failure (`fatal: this operation must be run in a work tree`, rc=128). `inherited_dirty = len(dirty)` (C2:171-172) thus reads 0 for a bare repository, so the observable behaves as "clean" when the truth is "unmeasurable". Verified:

```
$ python3 -I quality/check-evidence-pointers.py --repo /tmp/mado-ptr-b5.git
PRED-PTR-r36-v1 rev=master ... inherited_dirty=0 ... verdict=TARGET_MET
exit=0
```

While the identical worktree run on a dirty clone exits 1:

```
# same clone, untracked .ufo/waves/round-35/scratch/RevQuoteS203/zzz-untracked
inherited_dirty=1 ... verdict=TARGET_MISSED
exit=1
```

The bare case (and any other case where `git status` cannot run) is indistinguishable from a clean worktree. `git()` should treat a non-zero `git status` exit as an error (`die`), not as an empty list.

### B6 — hostile ambient `GIT_DIR` (was FAIL-OPEN; FIXED at HEAD)
Pre-hardening, the gate copied `os.environ` verbatim (`env = dict(os.environ)`), so a caller's `GIT_DIR` was inherited by the gate's own `git -C` calls; `git -C <dir>` does not override an inherited `GIT_DIR`. Exporting `GIT_DIR=/tmp/lane-bare.git` (clean bare clone) while the actual `--repo` worktree was dirty:

```
# pre-hardening
GIT_DIR=/tmp/lane-bare.git python3 -I quality/check-evidence-pointers.py --repo /tmp/mado-ptr-b6
... inherited_dirty=0 ... verdict=TARGET_MET
exit=0
# same worktree, no export
... inherited_dirty=1 ... verdict=TARGET_MISSED
exit=1
```

HEAD scrubs all `GIT_*` vars before setting its own (`env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}`; C1:102-106 — note this lives in the C1 file but the C2 gate runs as the same process; the C2 gate itself does not set GIT_DIR, so the scrub is what protects it). Verified at HEAD: with the same export, `inherited_dirty=1 ... verdict=TARGET_MISSED` (the dirty worktree is now seen). Closed.

### B7 — `--rev` unanchored (exit 0 on arbitrary revs, at HEAD)
`--rev` default `master` (C2:121) is passed verbatim to `git ls-tree` and `git show`. It accepts any tree-ish: HEAD, tags, and arbitrary commits. The only branch anchor is the axis-transcript ancestor check, which tests the transcript's hash against `--branch` (C2:196), not the chosen `--rev`. Verified:

```
$ python3 -I quality/check-evidence-pointers.py --repo . --rev prober-tag   # tag -> HEAD
... rev=prober-tag ... verdict=TARGET_MET    # exit 0
$ python3 -I quality/check-evidence-pointers.py --repo . --rev 2d90524     # R36 data commit, pre-hardening
... rev=2d90524 ... verdict=TARGET_MET        # exit 0
$ python3 -I quality/check-evidence-pointers.py --repo . --rev 4243d03     # base (pre-R36)
... setup=missing-r36-sections verdict=TARGET_MISSED   # exit 1
$ python3 -I quality/check-evidence-pointers.py --repo . --rev no-such-ref
PRED-PTR-r36-v1 error=revision-not-readable:no-such-ref   # exit 2
```

A gate run against a stale tree that contains R36 records (2d90524) exits 0. The claim is honestly scoped to the named rev, but the recipe's implied "the lane at the tip" is not enforced: nothing requires `--rev` to be the tip, an ancestor of `--branch`, or even on the branch. If the intent is "the lane's current records", the gate should reject a `--rev` that is not the branch tip (or default to it and refuse explicit non-tip revs).

## Additional notes
- C1 mutant fixtures are generated into `/tmp/mado-r36-mutants-<profile>` by default; each mutant is a file tree (ledger, receipts, `mutation.txt`) with no `.git/`, and the c2 counter's `git -C <mutant> rev-parse <rev>:<blob>` reads the *lane's* objects via the gate's `GIT_DIR` (C1:104). This is what makes `c2-blob-*` mutants observable; confirmed working in a clean clone (25/25 with the repaired counters).
- `--mutants <dir>` reuses the output path for `shutil.rmtree(out)` inside `gen-mutants.py` — a caller-supplied `--mutants` pointing at an existing non-scratch directory deletes it. Not exercised on production paths; foot-gun only.
- C2 `tip_axis_transcript` accepts the *first* sorted ancestor transcript file; `MADO_AXIS:` line check uses substring `"mismatched=0"` and `f"rev={candidate}"` (C2:204-206), which also matches `prev=<candidate>`; trivial to forge, but the file must still be an ancestor (`--branch`) and committed — low severity.

## Which of the prompt's candidate attacks are fail-open
1. **missing frozen spec** → FAIL-OPEN at the gate (instrument-gated; gate does not validate).
2. **predicate drift / target drift** → fail-closed (instruments die; verified both counters).
3. **missing manifest entry / truncated manifest** → FAIL-OPEN (no count/id pin; T1).
4. **instrument exits 1 but prints TARGET_MET** → fixed at HEAD; fail-closed now.
5. **timeout** → fail-closed.
6. **unwritable receipts dir** → fail-closed (ugly traceback).
7. **`--rev` naming a tag** → accepted; a tag pointing at the tip behaves like a commit (exit 0); the real issue is unbounded rev choice (B7).
8. **pointer list empty because a section heading was renamed** → fail-closed for exact renames (B1); FAIL-OPEN for substring-matching headings and for any prose-only section (B2).
9. **lesson file present but empty** → fail-closed (B3).
10. **bare/non-worktree `--repo`** → FAIL-OPEN (B5) — not in the prompt's list, but the strongest C2 find.

## Smallest safe corrections
- C1: pin the manifest: require `manifest["id"] == "MANIFEST-r36-v1"` and exactly the frozen 25 control ids (or at least count == 25) before scoring; validate `--frozen` files exist (`die("frozen-missing")`) and have the expected `id` before running instruments.
- C2: `git()` → treat non-zero exits for `status`/`ls-tree` as `die` (distinguish "no such rev" from "status failed"); make `sections` match `## Round 36` as a whole heading (`^## Round 36` anchored, or exact match), and consider requiring ptr36 to be non-empty before allowing `dangling_r36 == 0`.
- C2: constrain `--rev` to the tip (or an explicit, documented non-default mode) so the verdict is always scoped to a rev the claim can name.
