# R56ExecC3Harness — C3 control harness (w1)

## Deliverables
- `.ufo/waves/round-56/w1/R56ExecC3Harness/r56_ctl_c3.py` — module, `run(argv)->int` (also runnable as a script). Args `--repo --rev --work [--counter PATH]`, each once, two-token form.
- `.../witness/ref_counter.py` — witness reference counter (my reading of registration §C3, git objects only; also carries the differential `MODE` variants).
- `.../witness/build_witness.py` — builds witnesses A and B plus the counter variants, runs the harness on each. Writes only under `--work`.
- `.../receipt-witness-run.txt` — full output of that run (12 harness runs, per-control PASS/FAIL lines).
Nothing else written in the lane. Scratch `/fast/scratch/hyaku/mado-r56/R56ExecC3Harness/` removed. No installs. No hold-out path seen. No lane/fleet mutation.

## What the harness does
1. Setup (any failure → exit 2, reason on stderr, **nothing on stdout**, fail closed; any unexpected exception also exit 2): `--rev` resolved to a commit; `frozen-tables.json` at `--rev` must be a regular blob with sha256 `d50d2b7b…f9af` (embedded); its `base` must be a readable commit in `--repo` and `corpus/SOURCES.md` a regular blob there (control 1 input). Absent base object → `SETUP: frozen base revision <sha> is not readable in <repo> (control 1 cannot run)`, rc 2 (shown by test below).
2. Reads registry and `corpus/knowledge/*.md` (regular blobs only, direct children) at `--rev` through `git ls-tree`/`cat-file`; computes its OWN `entries/rows/missing/extra/dangling` per §C3 definitions.
3. Applies each control's mutation in memory, then **checks it is effective against the harness's own metric** (leg count must exceed the good tree's; control 1: leg>0). An ineffective mutation is a setup error, never a silently passed control.
4. Per control: `D=$(mktemp -d -p WORK)`, `git -C D init -q`, toplevel asserted == D, `git archive` of the good tree extracted with `tar -x` (symlinks preserved), mutated file(s) overwritten, `git add -A -f`, commit with `-c user.name=ctl -c user.email=ctl@ctl`. Counter run as child: `python3 -I COUNTER --repo D --rev <commit sha> --work WORK`, env scrubbed (no GIT_*, HOME=TMPDIR=WORK), cwd WORK, 180 s timeout.
5. Control passes only if: rc==1, stdout is exactly one newline-terminated `MADO_USED_BY:` line matching the registration grammar with `rev=` equal to the requested rev, `verdict=TARGET_MISSED`, `missed` ⊇ required leg, `missed` set == set of non-zero counts (self-consistency), and `TARGET_MET` appears nowhere in stdout.
6. `good` = same parse on `--repo --rev` as given: rc 0, one consistent line, `verdict=TARGET_MET`, all counts 0, `missed=none`.
7. Prints `MADO_R56_CONTROLS: claim=c3 good=<ok|bad> controls=<k>/6 verdict=<OK|FAIL>`; rc 0 only if good=ok and k=6, else 1. Counter default (no `--counter`): blob `quality/counters/c3-r56-used-by.py` at `--rev`, exported under WORK.

Controls (registry order): 1 base-registry, 2 fill-all, 3 drop-one, 4 dangling-source, 5 ghost-path, 6 fenced-cite (required legs missing/extra/missing/dangling/extra/extra).

## Witnesses built (scratch git repos with `objects/info/alternates` → lane objects so the frozen base object is readable)
- **A (realistic):** `git archive 13f0acbe corpus` + frozen-tables.json blob from `3423ae28`; used-by fixed by script (65 additions over 45 rows) → harness metrics `entries=70 rows=319 missing=0 extra=0 dangling=0`.
- **B (synthetic):** 6 registry rows (11 cells), 4 entries, one fenced non-citation (`S004`), one non-row prose id (`S243`), correct used-by → `entries=4 rows=6 0/0/0`.

## Results (decisive lines; full text in receipt-witness-run.txt)
```
witnessA ref counter        MADO_R56_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK        rc=0
witnessA always_green stub  MADO_R56_CONTROLS: claim=c3 good=ok controls=0/6 verdict=FAIL      rc=1   (every control: "counter printed TARGET_MET on a mutated tree")
witnessA missing_only       good=ok controls=2/6 FAIL      witnessA no_fence (ignores fences) good=ok controls=5/6 FAIL (control 6 fails)
witnessA always_red         good=bad controls=2/6 FAIL     witnessA silent_exit0 good=bad controls=0/6 FAIL
witnessB ref counter        good=ok controls=6/6 verdict=OK rc=0 ; always_green good=ok controls=0/6 FAIL ; missing_only 2/6 ; no_fence good=bad 5/6 ; always_red good=bad 2/6 ; silent_exit0 good=bad 0/6
```
Negative / fail-closed runs (all rc 2, empty stdout): lane HEAD without `--counter` (counter absent at rev); missing `--work`; repeated `--rev`; bad rev; nonexistent `--counter`; `--rev 13f0acbe` (no tables blob); `--repo` lacking the base object (`SETUP: frozen base revision … is not readable`).
Real lane HEAD (registry unfixed, ref counter): `good=bad controls=6/6 verdict=FAIL` rc 1 (counter reports missing=65 as in before.txt; all 6 controls still pass).
Scratch left empty after every run (`ls -A` of work dir empty).

## Defects / ambiguities found (registration read literally, listed per §C3 rule)
1. **Counter default / path**: registration names no counter path for the harness; I took `quality/counters/c3-r56-used-by.py` (claims-frozen.md) from the blob at `--rev`. Integrator should confirm the file name.
2. **Control 3 "first entry (sorted)"**: if the first sorted entry is listed by no row the literal mutation is vacuous; I pick the first sorted entry that some row lists (at base this is `animation-table-r26.md`, row S158 — the first sorted entry anyway). Sort is plain string order of ids.
3. **Control 6 pair order**: "(S, entry) pair … by sorted order" read as tuple order (S, entry); additionally S must be a registry row id and the row must still list the entry. At base-fixed A the pick is S002 in `window-rule-effects-getprop.md`, line 3 — its `source:` line, which also carries other citations, so wrapping hides them all (extra=4, not 1). Wrapping a `source:` line leaves it a line starting `source:` within 15 lines, so `dangling` is unaffected. Literal reading kept.
4. **Fence grammar** is not defined in §C3 beyond "``` / ~~~ with 0-3 leading spaces". Harness uses CommonMark-style (close needs same char, ≥ opening length, nothing after). A counter that toggles on any fence line agrees on every fixture here; on malformed/nested fences they could differ.
5. **Duplicate registry ids**: harness unions USEDBY over duplicate rows; spec silent.
6. **Used-by pair multiplicity**: `extra`/`missing` count distinct (S, path) pairs (sets), per "pairs".
7. **D1 archive scope**: scratch repos are `git archive REV -- corpus .ufo/waves/round-56/frozen-tables.json` (3 MB), not the whole 389 MB/27.6k-file tree. A counter that reads other tracked paths would fail every control for the wrong reason; claims-frozen "Causal separability" says C3 reads only corpus/knowledge + registry (+ tables).
8. Counter numbers (entries/rows/legs) vs harness's own are compared as **stderr diagnostics only**, not scored (a different reading of an ambiguity above must not fail a correct counter). Only leg *presence*, exit status, grammar, consistency and rev echo are scored.
9. Control 1 on a tree whose registry already equals the base bytes (e.g. lane HEAD) is an identical commit (`--allow-empty`); it still passes if the counter reports `missing`, and `good=bad` carries the verdict.
10. Registration conflict with the task text: registration says a setup error prints nothing on stdout; the r55 harness printed `SETUP` on stdout. I followed registration (stderr only, rc 2).

## Not verified
- The real C3 counter does not exist yet; only the witness counter was exercised. Harness ↔ real counter agreement on ambiguities 3-5 is untested.
- No `check-r56-controls.py` dispatcher written (not assigned); the module is importable as `r56_ctl_c3.run`.
- Anti-forgery limits per registration declared limit (a counter that detects the scratch repo or forges a tree passes).
- Timing: harness on witness A ≈ 1–2 s per run.
