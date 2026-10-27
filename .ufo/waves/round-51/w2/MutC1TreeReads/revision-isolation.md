# C1 revision-isolation mutation probe

## Predicate tested
PRED-C1-r51 requires ledger rows and accountability evaluated at `<rev>` and final output records `rev=<rev>`. Counter implementation is `quality/counters/c1-r51-ledger.py`; its `listing`, `show`, and clone path use the commit object, not checkout worktree. The test attacks those frozen semantics without changing lane files.

## Isolated setup
Scratch root: `/fast/scratch/hyaku/mado-r51/MutC1TreeReads`. Fixture is an archive of freeze commit `56026fcb9800370ae04bc65952a6567181c398d0`, initialized as an isolated git repository; explicitly checked `git rev-parse --show-toplevel` = fixture path. Fetched the actual freeze commit object from the lane so `--rev` resolves. Invoked counter from the frozen artifact with `python3 -I`, dedicated `--work` directories under the scratch fixture. Pristine archive run was a positive control.

## Probe 1 — altered worktree, frozen rev
Pristine output (exit 0):
```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=56026fcb9800370ae04bc65952a6567181c398d0)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
```
Then appended a row naming nonexistent `tools/mutated-not-in-rev.py` to worktree `quality/tool-ledger.md` and replaced worktree `quality/check-tool-ledger.py` with `print("selftest ok")`. The counter was rerun against the unchanged freeze rev (exit 0):
```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=56026fcb9800370ae04bc65952a6567181c398d0)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
```
The intended worktree mutation did NOT affect this result: counter clones/checks out rev, then reads ledger/checker from that clone's committed tree (`show`/`checker_script`); worktree-only mutation is not an effective mutant for a revision-object predicate. This is a pass for revision isolation, not a counter bypass. It also confirms no same-revision worktree contamination.

## Probe 2 — valid committed data at a different rev
Fresh fixture from the same frozen archive and fetched freeze object; created alternate commit `3d54ca196696b2555173f18f147538774c5457ae` with the same valid ledger/checker bytes (empty commit, tree unchanged). Ran against `--rev 3d54ca196696b2555173f18f147538774c5457ae`, exit 0:
```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=3d54ca196696b2555173f18f147538774c5457ae)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=3d54ca196696b2555173f18f147538774c5457ae
```
Since the alternate revision's tree is the same as the freeze tree, this establishes that `--rev` is not required to differ from freeze; output reports the exact selected commit. It is not a mismatched-ledger control: valid data is committed at that selected revision.

## Verdict
**PASS / mutant not applicable (inconclusive as a kill test).** The proposed worktree-only ledger/checker alteration is ignored because the frozen counter reads the selected commit tree. No mutant was killed; there is no evidence of counter being fooled by changed worktree bytes. The reverse run is consistent with predicate: the selected alternate rev is read and reported. The frozen predicate explicitly requires `<rev>`-scoped population, ledger, pointer resolution and checker evidence, so object reads are required by its semantics; it does not demand that `<rev>` equal the freeze revision.

## Hashes / restoration
Freeze artifact hashes verified from lane objects: counter `143cc4fd59eb363da0861921f596e48441086a26`; ledger `ebe380430704594cf5cca6b87807661ebf76a407`; checker `9fac1c3ea66540e1403563f54a740041ef1cf1ba` (git blob IDs). Probe-2 pristine working ledger SHA-256 `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b`; checker SHA-256 `6dd4061c1d8a82d5a9efa8ae954ff1c4559e43abefbb69210fa831bd758a98d4`. The probe's mutated fixture is scratch-only; lane bytes were never altered. (An initial disposable fixture attempt failed before probing because it lacked the freeze commit object; the corrected fixture explicitly fetched it.)

Report: `.ufo/waves/round-51/w2/MutC1TreeReads.md`
