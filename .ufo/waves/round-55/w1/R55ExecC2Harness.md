# R55ExecC2Harness — C2 independent control harness (round 55, wave w1)

Deliverable: `.ufo/waves/round-55/w1/R55ExecC2Harness/r55_ctl_c2.py` (sha256 `a872ff8d3ec09ab29e8b5944674567bbab401b9b7fe3e9883507c67e47476d5a`),
module exposing `run(argv)->int`, also runnable as `python3 -I r55_ctl_c2.py --repo R --rev REV --work DIR [--holdout DIR]`.
Receipts: `R55ExecC2Harness/receipts/scenarios-run.txt`, `receipts/standin-holdout-commit.txt`; test rig (stand-in tool,
build/scenario scripts) in `R55ExecC2Harness/test-fixtures/`. No tracked file edited; no git/jj mutation of the lane; no install.

## What it does
- Resolves `--rev` to a commit (`rev-parse --verify`), exports via `git ls-tree -r -z` + `git cat-file --batch` (no working-tree
  reads, no `git archive`/attribute filtering): `tools/mado-kbdopts.py`, `.ufo/waves/round-55/{fixtures/c2,ctl,fetch}` and, if
  present, `fixtures/c2-holdout`, into `mkdtemp` under `--work` (removed in `finally`). `frozen-tables.json` is read as a blob at `--rev`.
- Tool and each fixture run as `python3 -I <prog> <args.json argv>` with cwd = exported root, empty env except PATH/TMPDIR(=work)/
  LC_ALL/PYTHONHASHSEED, stdin /dev/null, own process group, 30 s timeout (SIGKILL on the group), stdout/stderr to files, 64 MiB RLIMIT_FSIZE.
  Pass = stdout bytes == `expected.out` AND rc == `int(expected.rc)`. Only ids F01..F18 / H01..H08 count; a missing dir fails.
- Hold-out commitment: sha256 over sorted (by relpath bytes) `<relpath>\0<sha256(file)>\n`, every file under the hold-out root,
  compared with `c2.holdout_commit_sha256`. `absent` iff the directory is not at rev (and no `--holdout`); then `holdout=0/8`.
- Controls (run over every fixture present, committed + hold-out): const-host ≤1 pass, empty 0, lookup-committed 18 committed + 0 hold-out.
- Line: `MADO_R55_C2: rev=<rev as given> fixtures=a/18 holdout=b/8 holdout_commit=… controls=k/3 verdict=…`; TARGET_MET needs 18, 8, ok, 3.
  Exit 0 MET / 1 MISSED / 2 setup error (bad args, unresolvable rev, git failure, bad `--holdout`; message on stderr, no line).
  stderr carries failing fixture ids and per-control `name:committed+holdout:ok|BAD` diagnostics.

## Interpretation choices (the spec was silent; flag for L1)
1. `--holdout DIR` REPLACES the hold-out at rev (or supplies one when rev has none); files are copied into
   `fixtures/c2-holdout/` of the export so args.json paths resolve; same commitment check. PRED-C2-r55 itself never passes it (hold-out is at rev).
2. frozen-tables.json unreadable / key missing → stderr note, `holdout_commit=bad` (if a hold-out is present) and a normal MISSED line, not exit 2.
3. Holdout dir present but empty → commitment of nothing → `bad`, not `absent`.
4. `--rev` is printed as given (not expanded); `rev=HEAD` prints `HEAD`.
5. The harness does not check the 18 committed fixtures against `c2.fixture_file_sha256` (not in the spec; freeze-verify.py owns that).
6. Controls run the exported stubs through `python3 -I` like the tool; stubs locate fixtures via `Path(__file__).parent.parent`, so the
   export preserves the `.ufo/waves/round-55/` layout (required for lookup-committed/const-host to work).

## Tests (scratch repo `$D` created by `git init`, toplevel asserted equal to `$D`, commits `-c user.name=ctl -c user.email=ctl@ctl`, `-C "$D"` throughout)
Stand-in tool = my own minimal implementation of registration §C2 (`test-fixtures/standin.py`); it passes the 18 committed fixtures
(measured directly: 18; first draft failed F10 because I overwrote KEY for empty stacks — spec reading: empty stack → KEY = LHS; fixed).
Own hold-out of 8 fixtures (key-before-name, nested touchpad, boolean prefixes, hex/sign, CRLF/tabs, duplicate keyboards, backslash, `$var`, out-of-range)
whose expected.out came from the stand-in (so it tests the harness mechanics, NOT tool correctness); commitment computed independently by
a shell `find|sort|sha256sum` loop = `bf85146e…76252`, harness agreed (rows B, C, K).

Decisive lines (full: `receipts/scenarios-run.txt`):
```
A stand-in, no hold-out at rev     fixtures=18/18 holdout=0/8 holdout_commit=absent controls=3/3 verdict=TARGET_MISSED   rc=1
B stand-in, external --holdout     fixtures=18/18 holdout=8/8 holdout_commit=ok     controls=3/3 verdict=TARGET_MET      rc=0
C stand-in, hold-out in rev        fixtures=18/18 holdout=8/8 holdout_commit=ok     controls=3/3 verdict=TARGET_MET      rc=0
D frozen sha wrong                 fixtures=18/18 holdout=8/8 holdout_commit=bad    controls=3/3 verdict=TARGET_MISSED   rc=1
E wrong tool (default delay 500)   fixtures=7/18  holdout=2/8 holdout_commit=ok     controls=3/3 verdict=TARGET_MISSED   rc=1
F lookup-table tool                fixtures=18/18 holdout=0/8 holdout_commit=ok     controls=3/3 verdict=TARGET_MISSED   rc=1
H tool absent at rev               fixtures=0/18  holdout=0/8 holdout_commit=ok     controls=3/3 verdict=TARGET_MISSED   rc=1
J unresolvable rev                 setup error: rev does not resolve to a commit: nonesuch                               rc=2
K one byte of --holdout changed    fixtures=18/18 holdout=8/8 holdout_commit=bad    controls=3/3 verdict=TARGET_MISSED   rc=1
L missing --work                   usage on stderr                                                                      rc=2
G2 empty.py patched to print F01's expected.out:  controls=2/3 (empty.py:1+0:BAD) verdict=TARGET_MISSED rc=1
```
Real lane at freeze commit 54dacbd8 (read-only through git objects): `fixtures=0/18 holdout=0/8 holdout_commit=absent controls=3/3 verdict=TARGET_MISSED`
rc=1 — the frozen "Before" state; the three frozen ctl stubs behave as specified on the committed fixtures (const-host 1/18 (F02), empty 0, lookup 18/18 + 0).
Direct unit checks: a hang tool is killed at the timeout (None after 2.0 s with TIMEOUT patched to 2); an endless-output tool is capped at 64 MiB
(returns a mismatch, no OOM). After runs `--work` is empty (scratch tree removed); nothing written to /tmp by the harness.

## Defects / ambiguities found
- Spec ambiguity: "KEY is the stack joined with `:` then `:` then LHS" read literally gives `:device[kbd-a]:…` for an empty stack; F10's expected
  `unsupported=4` only holds if an empty-stack KEY is the bare LHS (otherwise `device[kbd-a]:repeat_rate = 70` is not RELEVANT and the count is 3). Surfaced
  when my stand-in produced 3 on F10 with the literal reading. L1 should make the tool implementers' brief say so (this harness does not depend on it).
- Test-design note: row G (appending `print("x")` to empty.py) still yields controls=3/3 — correct, since printing "x" matches no fixture and the control
  spec is "passes 0"; the control is only violated when it reproduces a fixture's bytes (G2).
- Not verified: behaviour against the real sealed hold-out (not looked for, not seen; no hold-out path encountered), behaviour against the real
  `tools/mado-kbdopts.py` (does not exist at base), python versions other than the host's python3 (`-I`), SIGXFSZ/`rc=120` handling beyond the endless-output probe.
- Scratch (`/fast/scratch/hyaku/mado-r55/R55ExecC2Harness/`) removed at yield.
