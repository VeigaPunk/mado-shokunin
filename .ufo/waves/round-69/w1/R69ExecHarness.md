# R69ExecHarness — C1 scored harness (production draft)

Seat R69ExecHarness, round 69 wave 1. Axes: C1 calibration (harness kills paired
decision+oracle forgeries), C2 operability (untouched by this seat). No production path
written; L1 integrates.

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69ExecHarness/draft/quality/counters/c1-r69-landing-controls.py`
- sha256 `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73`
- 38461 bytes, 875 newlines, mode `-rw-r--r--` (matches the 0644 r68 sibling; invoked as `python3 <path>`)
- provenance: byte copy of `.ufo/waves/round-69/proto/c1-r69-landing-controls.proto.py`
  (sha256 `f4d138bfe806f787a98d5ca4d48ebf44896a4276cb0964df5d99e16f6b25390f`), then three
  scoped passes:
  1. docstring: round-69 title, explicit **exit map 0/1/2**, selftest paragraph (scripted
     children drive the real `measure()` body; spawn guard asserted live), **declared limits**
     (crash-vs-kill and missing-summary oracle only; no claim about real children);
     stale "candidate's new zero-citation case" parenthetical corrected.
  2. identity: scratch work dirs `r68-c1` → `r69-c1` (docstring, `measure()`, `selftest_main()`)
     and fixture author/message `r68-c1` → `r69-c1`; zero `r68` byte sequences remain
     (`str.count(b"r68") == 0`). Rationale: both harnesses `shutil.rmtree` a hard-coded work
     dir under the caller's scratch root, so keeping `r68-c1` makes r68 and r69 collide when
     run under one scratch root.
  3. `r"""` docstring prefix, matching the already-committed production copy (`6a5cefd2`,
     `quality/counters/c1-r69-landing-controls.py`, which is the proto + `r` and still carries
     the proto docstring). Docstring contains no backslash, so `__doc__` is unchanged.
- measurement body is otherwise byte-identical to the r68 harness apart from `R68` → `R69`
  labels in the evidence/receipt strings.

## Frozen call sites (unchanged, asserted)

Byte-level `str.count` on the draft:

| recipe | text | count |
|---|---|---|
| R1 | `mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)` + `\n` + 29sp `and forged_credit(mr_rc, mr_marker))` | **1** |
| R2 | `        mz_killed = mz_rc != 0` | **1** |
| R3 | `    subprocess.run = _no_spawn` | **1** |

`grep -cF` on the same patterns: R2=1, R3=1, R1=2 **lines** — expected, the R1 pattern is a
two-line text and grep counts matching lines; the byte-level occurrence count above is the
"exactly once" assertion the frozen counter uses. No reformatting of those lines.

## Proofs (all on the final draft bytes, scratch under `/fast/scratch/hyaku/mado-r69/R69ExecHarness`)

a) `python3 -I <draft> --selftest --scratch-root <scratch>/st-final`
   → **rc 0**, `MADO_R69_LANDING_CONTROLS_SELFTEST: 59/59 assertions passed`.
   Scratch work dir leaves no residue (`ls -A st-final` empty). Selftest drives the real
   `measure()` body through `_measure_case` (patched `run`), carrying the two original
   scripted cases plus the paired ones: crashing M-R child (rc 2, no marker) not a kill; M-Z
   run with no `MADO_LANDING_COUNTERS_SELFTEST:` summary not a kill; spawn guard installed and
   an attempted spawn under it raises.

b) frozen recipes applied once each to scratch copies, then `--selftest`:

| mutant | sha256 | occurrences | rc | failing assertion lines | tally |
|---|---|---|---|---|---|
| R1 | `0391b4e8aec1d22cb94a30a337933b820893352e0ca0be6bb99723840938daa6` | 1 | **1** | `a crashing M-R child is not a kill (decision + oracle pair)`, `mr-crash exits 1` | 57/59 |
| R2 | `55a5d6c2785c8926cefb234f852a0e49a1ef9e14d32b6aa11f86611e3a1f414a` | 1 | **1** | `an M-Z run with no assertion summary is not a kill` | 58/59 |
| R3 | `63d4f0e9aaa155c514b1062ce6e7feeebd0479b2910fea42b607793a30efc8ad` | 1 | **1** | `the hermetic spawn guard is installed for the check body`, `an attempted spawn under the guard raises` | 57/59 |

Tally and per-recipe failing assertions match the pre-freeze prototype baseline
(`.ufo/waves/round-69/control-baseline-r69.txt` § C1 proto: 57/59, 58/59, 57/59).

c) equivalence probe `mz_killed = mz_rc != 0` → `mz_killed = mz_rc != 0 or mz_rc is None`:
   occurrences=1, mutant sha256 `623f6b07cfc59ab7c8c343f37480983b4152a3e4b208b81f47680ac6e2a7d3b4`,
   **rc 0**, `59/59 assertions passed` → **equivalent mutant**, correctly excluded from the
   frozen set (it is this round's mined mistake, not a kill).

d) `PYTHONPYCACHEPREFIX=<scratch>/pycache3 python3 -m py_compile <draft>` → **rc 0**
   (no `__pycache__` written into the lane; draft dir holds only the `.py`).
   `python3 -I <draft> --help` → **rc 0**, prog line `c1-r69-landing-controls.py`, three options.
   Scratch-root refusals on the final bytes, all rc 2 with the prototype's messages:
   `/tmp/r69-x`, `/var/tmp/x`, `/dev/shm/x` (tmp-family), missing `--scratch-root`,
   symlinked component → `unsafe scratch root` / `--scratch-root is required` /
   `scratch root contains a symlink component`.

e) real-run parity (requirement 4), `--rev 04093b83f73a841117d3b31dbb2a6063f4f2a454`:
   `quality/counters/c1-r68-landing-controls.py` → rc 0, 13 evidence lines;
   draft → rc 0, 13 evidence lines. After normalising the `R68`→`R69` label, the fixture
   commit sha, the scratch root and the harness's own work-dir token, `diff -u` is **empty**
   (`NORMALIZED_DIFF_RC=0`); both receipts are
   `... selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=04093b83...`.
   Without the work-dir normalisation exactly one line differs (2 diff lines, one `CHILD_ENV`
   line) and only in `HOME=`/`TMPDIR=` pointing at `.../r68-c1/home` vs `.../r69-c1/home` —
   the harness's own work dir, renamed on purpose (collision rationale above). This is the
   only intended deviation from "same evidence lines as the r68 harness".

## Commands (all run with absolute paths, cwd = seat scratch)

```
python3 -I <draft> --selftest --scratch-root /fast/scratch/hyaku/mado-r69/R69ExecHarness/st-final          # rc 0, 59/59
python3 -I <draft> --repo <lane> --rev 04093b83... --scratch-root <scratch>/parity-final                   # rc 0
python3 -I <lane>/quality/counters/c1-r68-landing-controls.py --repo <lane> --rev 04093b83... \
        --scratch-root <scratch>/parity68                                                                 # rc 0
PYTHONPYCACHEPREFIX=<scratch>/pycache3 python3 -m py_compile <draft>                                       # rc 0
python3 -I <draft> --help                                                                                  # rc 0
python3 -I <draft> --selftest --scratch-root /tmp/r69-x                                                    # rc 2
python3 -I <draft> --selftest                                                                              # rc 2
python3 -I <draft> --selftest --scratch-root <scratch>/lnk2/st                                             # rc 2
<scratch driver>: replace-once + `sha256sum` + `python3 -I mutant --selftest --scratch-root <scratch>/stf-*`  # rc 0 driver
```

## Risks / notes for L1

- Recipe text is address-fragile: any reformat of the two `mr_killed` lines, the
  `mz_killed = mz_rc != 0` line or `subprocess.run = _no_spawn` turns `applied` down and the
  frozen counter scores 0. Draft keeps them verbatim (counts above).
- R2's replacement keeps the old text as a **prefix** of the new line, so a mutant still
  contains `mz_killed = mz_rc != 0` as a substring. The frozen counter asserts the old text
  occurs exactly once *before* applying and does not re-check absence after; an integrator
  that adds an "old text gone" post-check would misreport `applicable=no`. Not changed here.
- `r"""`: no backslash in the docstring, no `__doc__` change, needed only for byte-parity with
  the already-committed copy's first line.
- The committed production copy at `6a5cefd2` is the proto + `r` (37647 bytes, proto docstring
  with "Round-68 ... attempt 1" and `<scratch>/r68-c1`); this draft is the docstring-complete,
  identity-consistent version. Diff is docstring + 3 renames only, no decision-call-site drift.
- Real-children leg was exercised only by the parity run in scratch (read-only, writes under
  scratch); it remains harm-watch, not asserted by `--selftest` — as declared in the docstring.
- No tool installs this seat (none needed); no pacman transaction; no git/jj mutation anywhere;
  no desktop/service/socket/compositor probe; no writes outside the seat dir and scratch.
- Scratch `/fast/scratch/hyaku/mado-r69/R69ExecHarness` and the stray
  `/fast/scratch/hyaku/mado-r69/diff-r68-r69.txt` removed before yield.
