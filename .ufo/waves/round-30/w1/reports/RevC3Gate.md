# RevC3Gate — attack review of `quality/check-index.py` (C3)

Scope: the C3 gate only, as assigned: (1) `--rev` injection, (2) `--root` symlink
refusal order, (3) the selftest's six cases, (4) the `master` default on a
detached-HEAD lane. Report only — no lane byte, jj state or index touched.
Probe host: git 2.56.0, Python 3.14.8. All probes ran in `/tmp` fixtures or
read-only against the lane repo. Mutation probes ran on `/tmp` copies of the
gate, never on the lane file.

Gate blob frozen: `df01b20f…` identical at `451e8b3` (pre-data), `446dc396`
(data), `d72243e` (tip) and the worktree.

Predicate re-run (verified, not trusted): base `8f51071b` →
`indexed=41/43 missing=2` exit 1; data `446dc396` → `indexed=43/43` exit 0;
`--selftest` → `6/6` exit 0. The frozen S185 fence reproduces `41/43` and
`43/43` at the same two revisions, so **C3's predicate passes**; every finding
below is a defect in the gate's robustness and stated semantics, not a failed
claim.

---

## HIGH

### H1 — default rev `master` silently gates a stale revision · line 213

`main()` line 213: `rev = _git(args.repo, "rev-parse", "master").strip()`.
The default is a *branch name*, not `HEAD`, and the resolved SHA is printed as
`rev=…`, so a stale measurement is indistinguishable from a current one.

Probe D3 (temp repo, `master` at `4642e95`, detached `HEAD` advanced to
`05c50aef` with a new note `c.md`):

```
default (master) rc=0  MADO_INDEX: rev=4642e95… indexed=2/2 missing=0 … coverage=10.0000/10
--rev HEAD       rc=1  MADO_INDEX: rev=HEAD indexed=2/3 missing=1 … coverage=6.6667/10
                       missing: knowledge/c.md
```

This is exactly the false-green class C3's own kill rule forbids ("a green-at-base
gate is vacuous"): a bare `python3 quality/check-index.py` can report complete
while the lane's current tree is incomplete. It matters specifically here —
the lane is jj-colocated (`.jj` present) and already detached
(`git rev-parse --abbrev-ref HEAD` → `HEAD`). Detached HEAD alone is harmless
(probe D2: detached at the same commit as `master` → rc=0, `2/2`); the break is
that in a jj lane `master` is a bookmark that lags the working-copy commit
between rounds, so the lag, not the detach, is the normal state.
Recommendation: default to `HEAD`, and print both the requested ref and the
resolved SHA.

## HIGH

### H2 — `rev-parse master` failure is uncaught: setup error reported as exit 1 · line 213

Unlike `load_rev` (lines 39-44, `CalledProcessError` → `SETUP_ERROR` → exit 2),
line 213 sits outside any `try`.

Probe N5 (temp repo on branch `trunk`, one note, one correct row; no `master`):

```
rc=1
stdout=''                       # no MADO_INDEX line at all
stderr[0]='Traceback (most recent call last):'
stderr[-1]="subprocess.CalledProcessError: Command '['git', '-C', …, 'rev-parse',
           'master']' returned non-zero exit status 128."
```

Docstring lines 18-20 define `1 = gap (missing/dangling/duplicate) or refused
input` and `2 = setup error`. A missing-ref setup error therefore exits 1 with
*empty stdout*: a wrapper that treats exit 1 as "coverage gap" (which the
registration's red-at-base controls also treat as a legitimate signal) records
a false red, and a wrapper that parses `MADO_INDEX:` gets nothing. Same probe
with `--rev HEAD` → rc=0 `2/2`. Every `main`-level git call should share
`load_rev`'s error boundary.

## MEDIUM

### M1 — `--root` cannot distinguish "no knowledge dir" from "empty knowledge dir": vacuous green · lines 64-74

`load_root` only set-checks `if os.path.isdir(kdir)` (line 64); if the path is
absent or is a regular file, `notes` stays empty and `report` prints a green
summary.

```
E1  corpus/ present, corpus/knowledge absent:
    rc=0  MADO_INDEX: root=…/noknow indexed=0/0 missing=0 dangling=0 duplicates=0 coverage=0.0000/10
N3  corpus/knowledge exists but is a regular file:
    rc=0  MADO_INDEX: root=…/kfile indexed=0/0 … coverage=0.0000/10
```

A mis-rooted invocation (`--root` at the wrong directory depth, a checkout
without `corpus/`) passes. `coverage=0.0000/10` beside exit 0 is internally
incoherent — the same line says "nothing covered" and "complete". `N1`
(`--root` nonexistent entirely) does exit 2, so only the partial-tree shape is
affected. Selftest case 6 (see L3) *enshrines* this as desired behavior.
Recommendation: absent/non-directory `corpus/knowledge` → `SETUP_ERROR`/exit 2;
keep 0/0 green only for a directory that actually exists.

### M2 — row-set regex is strictly more permissive than the S185 fence it claims to implement · line 29

Gate: `ROW_RE = re.compile(r"^\|\s*`knowledge/([^`]+\.md)`", re.M)`.
Fence (`SCORECARD.md:78`, pinned as S185):
`re.findall(r"^\| `knowledge/([^`]+\.md)`", index, re.M)`.

Two learned behaviors the fence does not have: `\s*` accepts **zero** spaces,
and `\s` **includes `\n`**, so a row can start on one line and finish on the
next.

```
H1  README row `|`knowledge/a.md`|h|s|` (no space after the pipe)
    gate rc=0 indexed=1/1 green;  fence rows = []  (would be red)
N4  README: a line `|` then a line `` `knowledge/a.md` | h | s | ``
    gate rc=0 indexed=1/1 green;  fence rows = []
same-line canonical control: gate rows ['a.md'], fence rows ['a.md']
```

Three artifacts state the stronger claim this contradicts: docstring lines 7-9
("the same semantics as the SCORECARD.md fleet-round-1 counting command"),
`corpus/SOURCES.md:197` S185 ("Gives the exact row-set semantics an
index-completeness gate must implement"), `SCORECARD.md:1922` capability row.
At the two measured revisions the numbers agree (verified above), so this is
latent, not active — but the gate cannot be substituted for the fence as
claimed, and a README formatting drift would green the gate while the fence
stays red. Recommendation: use the fence's literal pattern
`^\| \`knowledge/([^\`\n]+\.md)\``.

### M3 — `names.split()` vs the fence's `splitlines()`: whitespace in a note name is a false gap · line 45

Line 45 `names = {n for n in names.split() if n.endswith(".md")}`; the fence
splits on lines. Probe I1 (temp repo, notes `a b.md`, `c.md`, both rowed):

```
--rev HEAD rc=1 indexed=1/2  missing: knowledge/b.md  dangling: knowledge/a b.md
--root     rc=0 indexed=2/2
```

One note produces both a phantom missing and a phantom dangling, and the two
modes disagree on the same tree. Latent for the kebab-only corpus, but it is a
second divergence from the "same semantics" claim (M2) and a mode asymmetry.
Recommendation: `names.splitlines()`.

Corroborated independently by `RevC1Fence`, and extended here with the
mechanism: `_git` reads `ls-tree` **without `-z`**, so git C-quotes any
non-ASCII path (`core.quotePath` default). Probe U (temp repo, note `café.md`,
both modes):

```
ls-tree raw : '"caf\\303\\251.md"'      # quoted
ls-tree -z  : 'café.md\0'
--rev HEAD  : rc=1  indexed=0/0 dangling=1  dangling: knowledge/café.md
--root      : rc=0  indexed=1/1
```

The quoted name fails `endswith(".md")` and is dropped, so `--rev` counts 0
notes while `--root` counts 1 on the same tree. The fence shares this defect
(it also reads un-`-z` output), so this instance is fence-parity rather than
drift — but it is a hard `--rev`/`--root` disagreement, and the `0/0` note count
is the same vacuous-green shape as M1. Recommendation: `git ls-tree -z` +
`split("\0")`, which also makes `splitlines()` safe.

## LOW

### L1 — REV is never verified with `rev-parse`; injection is blocked only by accident · lines 40-41

`rev + ":corpus/knowledge"` / `rev + ":corpus/README.md"` are concatenated into
argv positions where git may parse them as options if `rev` starts with `-`.
`_git` uses list argv (line 33), so **shell/word injection is impossible**;
argument injection is reachable only through `--rev=<opt>=<value>` (argparse
rejects the space-separated form: probe C1 space form → argparse
`expected one argument`, exit 2).

Attempted payloads, all failing closed at line 40 with `SETUP_ERROR`/exit 2:

| payload | result |
|---|---|
| `--rev=--output=/tmp/x` (C1) | exit 2 — `ls-tree` has no `--output` |
| `--rev=--format=%x41` (C2) | exit 2 — `fatal: --format can't be combined with other format-altering options` |
| `--rev=--pretty=raw` (C3) | exit 2 — `ls-tree` rejects |
| `--rev=--abbrev=4` | exit 2 — `option 'abbrev' expects a numerical value` |

The write vector is real in principle: `git show --output=<path>` **is**
supported on this host (`rc=0`, file created), and a direct
`git show "--output=/tmp/x:corpus/README.md"` fails only because the parent
directory `/tmp/x:corpus` does not exist (pre-creating it would allow the
write). It is unreachable today because line 40 (`ls-tree --name-only`) runs
first and rejects every `=`-valued option that matters — a property of this
git's option parser (2.56.0), not of the gate. That makes docstring line 14
("Writes: nothing") true only by version luck. Recommendation: resolve once
with `git rev-parse --verify --end-of-options <rev>^{commit}`, then build
`<sha>:path` from the SHA (a SHA cannot start with `-`).

### L2 — symlink refusal is correct at the leaves but not transitive across ancestors · lines 56-60 / 66-67

**Check order is right.** `islink` precedes `isfile`/`isdir` for both top-level
paths (58 before 60/64) and for members (67), which is the only order that
works, since `isfile` follows symlinks. Positive controls: symlinked member
file → `REFUSED` exit 1 (G1); symlinked `corpus/README.md` → `REFUSED` exit 1
(N2). But an ancestor or the root argument itself is followed:

```
F2  <root>/corpus is a symlink to an outside tree:
    rc=1  MADO_INDEX: root=…/anc2 indexed=0/1 … missing: knowledge/a.md
F3  --root itself is a symlink to an outside tree: rc=1, same shape
```

The gate reads outside the named root with no `REFUSED`, so docstring lines
12-14 ("plain filesystem tree; regular files only — symlinked or non-regular
members are REFUSED") holds only for the two leaf paths and members. Harm is
bounded (the operator supplied the root; the read is read-only), but the claim
should say "members", not "tree", or the root/`corpus` components should be
`realpath`-checked. A TOCTOU window (check at 58/67, open at 72) exists and is
not worth fixing here.

### L3 — the six selftest cases are not tautological, but they never exercise the mode the C3 predicate runs · lines 123-193

No case is vacuous in the "always passes" sense: mutation M7 (force
`report()` to `return 0`) fails 3/6, and M4 (delete the duplicates detector)
fails 1/6, so the exit-code assertions have teeth. The coverage claim is
nevertheless overstated:

* **All six cases are `--root`-only.** `load_rev` (lines 38-45) and the default
  rev (line 213) have **zero** assertions. The two measurements C3's predicate
  actually cites (`--rev 8f51071b`, `--rev 446dc396`) are outside the suite.
  Proven by mutation: M6 (`split()` → `splitlines()`, line 45) → still 6/6;
  M5 (default `master` → `HEAD`, line 213) → still 6/6.
* **Case 5 is misnamed and tests the wrong guard.** It symlinks the
  `corpus/knowledge` *directory* (line 169-171) yet is named "symlinked member";
  it exercises the top-level guard, not the member guard. Mutation M2 (delete
  the top-level `islink` loop, lines 57-59) → 5/6, so that guard is covered;
  mutation M1 (delete `os.path.islink(fpath) or` at line 67) → **still 6/6**,
  so the per-member refusal that docstring line 13 advertises is untested.
* **The regex drift (M2 finding) is invisible to the suite.** M3 (narrow
  `ROW_RE` to the fence's exact `^\| \``) → still 6/6, because every fixture
  writes canonical `| \`knowledge/…\`` rows via `_write_tree`.
* **Case 6 blesses the vacuous green** (lines 183-188: "empty tree exits 0 with
  indexed=0/0"). Combined with M1 finding, a *missing* knowledge path produces
  the identical output; the suite certifies that as correct.
* Dead weight: `_write_tree`'s `symlink_knowledge=False` parameter (line 112) is
  never read.

Recommendation: add a `--rev` case against a throwaway git repo (complete + one
missing), a non-canonical-spacing case, a member-file symlink case, and split
"empty existing dir" from "absent dir".

### L4 — minor observability inconsistencies · lines 50 vs 44/62, 199-207

`_refuse` prints `REFUSED:` to **stdout** while `SETUP_ERROR` goes to stderr
(44, 62), so exit 1 has two differently-channelled causes and the refusal line
never carries the `MADO_INDEX:` prefix. `--repo` is silently ignored when
`--root` is given (207 only rejects `--rev` + `--root`). Neither affects the
predicate.

---

## Residual risk

1. **Latent, not active, semantic drift.** At the only two revisions the claim
   measures, gate and fence agree (`41/43`, `43/43`, verified independently).
   M2/M3 are correct today only because `corpus/README.md` uses canonical
   `| \`knowledge/…\`` rows and kebab note names (43 row lines, no
   non-canonical pipe row found in a grep of the README tables).
2. **Default-rev false green (H1) is dormant only because `master` and `HEAD`
   coincide today** (`d72243e` both). The first jj bookmark lag reopens it, and
   nothing in the output distinguishes the two.
3. **Injection is version-scoped.** L1's conclusion rests on git 2.56.0's
   refusal to combine `--name-only` with `--format`, and on `ls-tree` lacking
   `--output`. A different git build is the only thing standing between `--rev`
   and a `git show --output=` file write.
4. **Not wired, so it can rot.** No caller: `grep -n 'check-index'
   tools/mado-verify.sh` → no hit; references exist only in SCORECARD, LOG,
   SOURCES, registration and lessons. The missing `SKILL.md` §Gate registry row
   is already routed to round 31 in
   `corpus/lessons/round-30-verifier-spotcheck.md` (lines 94-98) and is not
   re-raised here.

## Verification gaps

* I could not produce the H1 state in the real lane: advancing a jj
  working-copy commit past the `master` bookmark is a jj mutation, which this
  seat is forbidden to perform. D3 models it in a temp git repo instead; the
  real lane is currently non-lagged, so H1 is untriggered in situ.
* Injection probes cover `--output=`, `--format=`, `--pretty=`, `--abbrev=`
  only; I did not enumerate every `=`-valued option of this git's `ls-tree`
  and `show`. The structural gap (no `rev-parse --verify`) stands regardless.
* Mutation probes were 7 hand-picked mutants on `/tmp` copies, not an exhaustive
  sweep; the sibling `MutC3Gate` lane owns the full mutation matrix — the M1/M3/
  M5/M6 survivors above are the subset relevant to the selftest question.
* No Windows/path-separator or permission-denied testing (out of scope for this
  lane).

## Adjacent observation (outside the C3 item; read-only, no restore performed)

The lane worktree is dirty with one modification outside the registered write
scope: `M quality/q36-successor-receipts.txt` (mtime `2026-10-24 04:06:46`,
`git status --porcelain` → ` M quality/q36-successor-receipts.txt` and
`?? .ufo/waves/round-30/w1/`). Diff: 4 insertions / 4 deletions, and after
normalizing every `/tmp/…` and `/fast/scratch/…` run directory the `+` and `-`
lines are byte-identical — every mutant/pristine name, `rc=`, `expected=`, and
`PASS` token is unchanged. So the delta is ephemeral run-dir paths only and no
recorded verdict moves, but a committed round-28/29 evidence file now differs
from its committed bytes in the worktree. Surfaced by `RevC1Fence`; I did not
write or restore it (out of my item, and restoring is a mutation I may not
perform). Harm-watch implication: the registration's "no `tools/` byte changes"
scope is intact, but the lane worktree is not clean at review time, so any
receipt claiming a clean tree at this commit should be read as worktree-scoped.
