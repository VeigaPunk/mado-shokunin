# quality/tool-ledger.md append — round 66 rows

Insertion: append the two rows below at the end of `quality/tool-ledger.md` (`:144` is the current
last row). Row grammar is enforced by `quality/check-tool-ledger.py`: one row per population path,
non-empty description, and an accountability pointer that exists at `--rev` and contains the row's
basename in its bytes.

| `quality/counters/c1-r66-register.py` | Read-only round-66 C1 register counter: rejects a duplicate returned-host heading, a row with no resolving receipt, and any gate receipt other than the exact live CLEAN line, while requiring exactly one row per eight groups; reads git objects at `--rev` only and writes nothing. | `.ufo/waves/round-66/claims-declaration-r66.md` |
| `quality/counters/c2-r66-landing-instrument.py` | Read-only round-66 C2 driver: pins `--rev` to a commit SHA, extracts the hardened landing instrument and its three frozen dependencies at that rev, strips inherited `GIT_*` from git and leg children, runs the instrument selftest and the `--round 66` landing, and prints one `selftest=<rc> landing=<rc> green=<yes/no> verdict=…` line; refuses tmp-family and symlink-ancestor scratch; writes only under its declared scratch. | `.ufo/waves/round-66/w1-dispatch.json` |

Verification notes for the integrator:

1. Both pointer files exist at the freeze commit and name the row's basename:
   `claims-declaration-r66.md` names `quality/counters/c1-r66-register.py`, and
   `w1-dispatch.json` carries the R66ExecDriver seat text naming
   `quality/counters/c2-r66-landing-instrument.py`. `receipts/evidence-scope.txt` names both as well,
   but it is untracked at HEAD (`git cat-file -e HEAD:.ufo/waves/round-66/receipts/evidence-scope.txt`
   rc=128), so it is not used as a pointer; commit it in the integration rev before citing it. A
   simulated ledger with `evidence-scope.txt` as the pointer read `bad_pointer=2` (sentinel
   `R66SentFrontier`), which this revision removes.
2. Population arithmetic: the current ledger is `population=106 ledger_rows=106` at
   `ed980316e330703030d0c17b2a7098e058295b99`
   (`python3 quality/check-tool-ledger.py --repo . --rev HEAD`). Two new `quality/counters/*.py`
   files make the expected integrated state `population=108 ledger_rows=108` with
   `uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET`.
3. That 108-row state is a prediction for the integrated revision, not an observation. At draft time
   neither file is installed under `quality/`, so the ledger still reads 106/106.
4. `quality/landing-counters.sh` gets no row here: it is a `.sh` outside this checker's population
   (`.sh` counts only under `tools/`); its registration is the SKILL gate-registry row.
5. The r65 counter rows are unchanged and keep their frozen predicates.
