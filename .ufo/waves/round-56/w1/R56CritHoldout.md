# R56CritHoldout — C2 hold-out and commitment attack (wave w1)

Seat: R56CritHoldout (critic, leaf). Lane commit read: `3423ae285676c2a10273000f4519163472b443db` (read-only `git ls-tree` / `cat-file` / `archive`).
Deliverables: `.ufo/waves/round-56/w1/R56CritHoldout/` (scripts + `probe-output.txt`). Scratch removed before yield.
No tool installed or upgraded. No pacman. No `hyprctl` call of any kind. No sealed hold-out path was opened; the only
`fixtures/c2-holdout` used is a synthetic stand-in I created under scratch (labelled below). Nothing in the lane was written.

## Verdict

C2 as frozen does not establish that a tool implements the grammar. The harness, as the predicate describes it, runs the
tool with the expected answer on its filesystem, so a three-line tool that prints `<display-root>/expected.out` and exits
with `expected.rc` scores **18/18 committed and 8/8 hold-out** with no grammar. The three registered controls do not
catch this. The commitment binds the bytes of the fixture tree and does not bind what the tool may read. Defects below are
ranked; the first is decisive for the claim.

## F1 (decisive) — the expected answer sits beside the input the tool receives

- Every committed `args.json` passes `--display-root {FX}` (18 of 18; counted by `grep`). `{FX}` is the fixture directory,
  which contains `expected.out` and `expected.rc` next to `tree/` (`fixtures/c2/F##/`). The harness replaces `{FX}` by that
  directory's absolute path in its export (predicate text). The tool therefore receives the path of its own answer key.
- The tool's cwd is the export root, and `fixtures/c2/` and `fixtures/c2-holdout/` are siblings under it. From any hold-out
  directory `../../c2/F01/expected.out` resolves (checked with `ls` on the export). Even a tool that reads only "its" sibling
  can reach every fixture.
- Demonstration (`cheat_sibling.py`, 6 lines, no parsing): reads `expected.out` and `expected.rc` from `--display-root`.
  Run through a predicate-faithful mini-harness (`mini_harness.py`: `{FX}` substitution, `python3 -I`, cwd = export root,
  byte and rc compare) on the export of `fixtures/c2` at `3423ae28`:

  ```
  {'fixtures/c2': '18/18', 'fixtures/c2-holdout': '1/1'}     # 1/1 = SYNTHETIC stand-in H01, not sealed H01-H08
  ```
  The predicate would print `MADO_R56_C2: ... fixtures=18/18 holdout=8/8 ... verdict=TARGET_MET`: the cheat changes no
  harness input, so `holdout_commit` (a commitment over the tree, which is unchanged) still reads `ok`.
- Why this is non-adversarial: a tool author who reads "the fixture directory" and "`--display-root {FX}`" reaches for the
  fixture directory first. The claims file's declared limit ("passes a non-adversarial harness") is hit by the first shortcut
  an author would try, not by a sophisticated counter.
- Mitigation probe (verified): stage each fixture as `tree/` plus rewritten args only, and run the child under
  `bwrap --unshare-all --ro-bind /usr ... --ro-bind <stage> /work --ro-bind <tool> /tool.py` (`sandbox_harness.py`,
  `probe-output.txt`). The cheat then scores `0/18`; the tool's stderr:
  `FileNotFoundError: '/work/expected.out'`. Inside the sandbox `/work` contains only `tree` (listing verified), and `/fast`
  is not visible. A sandbox therefore removes the sibling channel; a faithful grammar tool needs only `tree/` and args.
- Consequence: the hold-out is not sealed at run time. Its expected files are revealed into `fixtures/c2-holdout/` at
  integration (predicate text), so they are on the filesystem when the harness runs. "Sealed" holds for seats' reads, not for
  the tool under test.

## F2 — the controls do not measure F1, and say less than their label

- `ctl/lookup-committed.py` passes 18/18 committed and 0/8 hold-out by construction: it keys on an `F##` path component and
  only knows committed ids. Measured by the same mini-harness: `{'fixtures/c2': '18/18', 'fixtures/c2-holdout': '0/1'}`.
  Its `0/8` shows that name-keyed lookup fails hold-out. It says nothing about a tool that reads the sibling `expected.out`,
  which passes `26/26` (F1). "controls=3/3" therefore does not show the tool implements the grammar.
- `ctl/empty.py` scores `0/18` (`{'fixtures/c2': '0/18', ...}`). It proves the harness is not vacuous for empty output. It
  would pass only a fixture with an empty `expected.out` and rc 0; none is committed, and the hold-out is unseen, so the
  "passes 0" claim is not checkable before reveal.
- `ctl/const-host.py` scores `1/18` (F02 only), consistent with "at most 1 of 26". "At most 1 of 26" is a claim about the
  sealed hold-out; the wave's harness must compute it at reveal rather than assume it. A hold-out tree identical to F02 would
  make it 2.
- Net: the controls prove that the harness is not satisfied by constant, empty or name-keyed output. They do not prove
  grammar implementation, and they do not exercise the one cheat that works. Any added control must be a new versioned
  registration; the claims file freezes `controls=3/3`.

## F3 — pattern-matching without reading siblings

- A tool that hashes its config tree and replays the committed `expected.out` of the matching `fixtures/c2/F##/` (reachable
  from its cwd) scores 18/18 and 0/8 by construction. The hold-out does catch this route, but only because the hold-out is
  not in the committed set. Under F1 the hold-out is reachable, so this route is not needed.
- `$ROOT` display is an output-side transformation. Keying on it adds nothing: the input path, not the output text, carries
  the answer key.

## F4 — commitment: what it binds and what it does not

Verified (`commit_check.py`, from git objects at `3423ae28`, `LC_ALL=C`, sha256 over sorted `relpath\0kind\0hex\n`, link
kind hashes link text):
```
files: 119 committed_count: 18
computed: a9f552511cc4939e3c83190e7ca55a09d5f01dd520c59b3a6feeba2e0c4647d6
frozen  : a9f552511cc4939e3c83190e7ca55a09d5f01dd520c59b3a6feeba2e0c4647d6 MATCH
modes non-644: {}
```
- **Binds:** every regular file under `fixtures/c2` including `args.json`, `expected.out`, `expected.rc`, `note.txt` and every
  tree file (dotfiles included); symlink link text (`F05/tree/linked.conf -> real/theme.conf`,
  `F06/tree/hyprland.conf -> real/main.conf`, `F10/tree/mix/b.conf -> missing-target.conf`); relative paths; any addition or
  removal of a file.
- **Does not bind access:** the commitment proves the bytes of the tree, not what the tool reads. F1 is outside what a
  commitment can detect. The "commitment ok" line in the predicate is about the data.
- **Does not bind directories.** Git stores no empty directory; the commitment sees none. F14's `tree/` is absent in the lane
  and in every export (`git ls-tree` shows no `F14/tree`), which is fine for F14 but shows the gap. A hold-out with an empty
  directory (for example `source = emptydir` → `SKIP reason=directory`) commits `ok` on disk and loses the directory after
  `git add`/archive, so the hold-out result diverges with no `bad` on the commitment. [INFERENCE: the revealed hold-out is
  committed to git at integration, as the committed tree is.]
- **Does not bind file mode bits** (executable or 000). An unreadable sourced file or `--getoption` (listed, not parsed, per
  the model) depends on the user running the harness (root reads mode 000). No committed case exercises this; environment
  dependence is untested.
- **Does not forbid absolute or root-escaping link text.** Link text is bound, but an absolute target makes the output
  host-dependent. All three committed links are relative and none escapes the root (verified); nothing in the harness
  checks this.
- **Hold-out commitment is aggregate only.** `holdout_commit_sha256 = 65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183`
  has no per-file manifest, so a reveal mismatch reports only `bad` and gives no location.
- **Symlink preservation (answers the environment question).** `git archive <rev> .ufo/.../fixtures/c2 | tar -x` recreates
  all three links as symlinks (`find -printf '%y'` → `l`; verified). With symlink-capable POSIX filesystems the committed
  fixtures are reproducible. Failure modes:
  - Dereferencing copy (`cp -rL`): fails loudly on the dangling `F10/tree/mix/b.conf` (`cannot stat ...`). A copy that drops
    the dangling link instead changes the commitment: recomputed `0dd3a93140a0a52c233bf8ed6733ec8d507eb1471611aabfeb077a005c58b2b1`
    ≠ frozen (verified). Loud, not silent.
  - `core.symlinks=false` checkouts turn links into text files: the lstat kind `l` becomes `f` and the commitment changes.
    [INFERENCE: not run; reasoned from the kind rule.]
  - Silent dependence: `F02` expects `source = /dev/null` to be a non-regular path (`SKIP reason=nonregular`). That depends
    on the host's `/dev/null`, outside the export. Not a silent risk on Linux; it is host-dependent.
- The `--display-root` realpath alternative is not exercised by the committed set here (`readlink -f` of the scratch and lane
  paths equals their input).

## F5 — what a committed-fixture reader can infer about the hold-out

- The frozen tables publish `holdout_count = 8` and `holdout_file_count = 56`, visible to every seat. 56 = 8 × 4 metadata
  files + 24 tree files, so the hold-out has three tree files per fixture on average. Low harm; it is a seat-visible leak
  that the registration does not mention.
- Coverage of the committed expected outputs (grep over `fixtures/c2/*/expected.out`):

  | grammar element | committed output |
  |---|---|
  | `type=dir` watch line | never |
  | `IN_CREATE` mask (dir) | never |
  | `verdict=UNKNOWN` / `live=?` | never (F12 is `SETUP bad_json`) |
  | `SETUP unreadable` | never |
  | `SETUP too_large` | never |
  | `--home` absent with `~` source (unsupported) | never |
  | `role=canonical` | F05, F06 |
  | `reason=bogus / nomatch / inaccessible / directory / nonregular` | F10 / F06,F10 / F10 / F03,F16 / F02 |
  | `SETUP usage` / `SETUP bad_json` | F17 / F12,F18 |

  The committed notes name the themes, so a reader knows which branches the 18 do not test. Inference (not in the frozen
  text): the hold-out most likely targets the rows marked never. Against those rows 18/18 is weak evidence.
- The committed fixtures agree with the registration in every case I checked by hand (F01, F02, F03, F04, F05, F06, F08, F09,
  F10, F11, F13, F14, F16); one note contradicts its output (F6 below).

## F6 — defects in committed material

- **F12 note contradicts its expected output.** `F12/note.txt` says `UNKNOWN: no record; non-object lines are bad_json`, but
  `F12/expected.out` is `MADO_WATCH: SETUP bad_json` with rc 2. The `UNKNOWN` path (registration: `live=?` /
  `verdict=UNKNOWN`) has no committed expected output at all (grep shows none). The note describes a case the fixture does
  not test. Fixing the note changes the committed fixture set and needs a new versioned registration.
- **`--config` "regular file" is ambiguous.** The model says "parsed when it is a regular file". F06 (symlink main config,
  parsed) shows the test is `stat`-following; the text does not say so.
- **F02 host dependence** (see F4): `/dev/null` is outside the export.

## F7 — what I did not verify

- Hold-out content, hold-out commitment preimage and the sealed hold-out: not opened (per instruction) and not checked.
- `tools/mado-watchplan.py`: does not exist at `3423ae28` (w1 seats build it); not run. The F1 cheat and sandbox results are
  against the predicate-faithful mini-harness, not the real harness or the real tool.
- `core.symlinks=false` behaviour: reasoned, not run.
- Entailment, the sentence-to-pin audit and C1/C3: out of scope for this seat.

## Smallest safe corrections (for the integrator; none applied, the freeze forbids edits)

1. Harness: run each child with the tool's view limited to a staged `tree/` and rewritten args, under `bwrap` (verified
   available at `/usr/bin/bwrap`) or an equivalent namespace. Keep expected bytes in harness memory, never on the tool's
   filesystem. Add a sibling-read control that must score 0/26 under the sandbox. This is a new registration version.
2. Harness: before running, assert the three committed link kinds (`islink`, `readlink` equal to the committed text) and
   reject absolute or root-escaping link text. Fail loudly on a mismatch.
3. Commitment: add directory entries (or assert the tree has no empty directories) and mode bits. Keep the hold-out aggregate
   hash. Stop publishing `holdout_file_count` if the leak matters.
4. Fix the F12 note (or add an UNKNOWN fixture) in a new registration; both change the committed set.
5. Consider committed fixtures for the never-covered rows in F5, for the same reason.

## Commands and receipts

- `python3 -I commit_check.py` → MATCH (above).
- `python3 -I mini_harness.py <export> cheat_sibling.py` → `18/18`, synthetic `1/1`.
- `python3 -I mini_harness.py <export> ctl/{const-host,empty,lookup-committed}.py` → `1/18`, `0/18`, `18/18`; holdout `0/1` each.
- `python3 -I sandbox_harness.py <export> cheat_sibling.py <stage>` → `sandboxed cheat_sibling.py 0/18`.
- `bwrap ... --ro-bind <stage>/F01 /work ... python3 -I /tool.py --display-root /work` → `FileNotFoundError: '/work/expected.out'`, rc 1.
- Full output: `.ufo/waves/round-56/w1/R56CritHoldout/probe-output.txt`.
