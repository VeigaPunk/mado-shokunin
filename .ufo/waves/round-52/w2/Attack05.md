# Attack05 — C1 TMPDIR and workdir boundary

Seat `Attack05` (connector, leaf). Lane `mado-shokunin`. Base
`85d57a818c3707397e21c840b6498b105ba798aa`. Wave `w2`. Axes: **operability** (C1
boundary surface); no coverage move. This is an attack, not an author judgment:
every verdict below is "reproduced" (the boundary premise held under test) or
"not reproduced" (concrete falsifier found), with limitations stated.

**Two byte states are in play.** The W1-evidenced draft lives at
`.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`, sha256
`0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31` (847 lines,
the bytes every W1 harness/probe/selftest ran). While this seat worked, an
untracked, different implementation appeared at `quality/counters/c1-r52-ledger.py`,
sha256 `923faf02cd0c2db374f7757d38ef24fc8381c2882cb3d853882f0fadce1c17d7` (78
lines). The worktree also shows modified `corpus/README.md`, `corpus/SOURCES.md`,
`quality/tool-ledger.md` and untracked `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`,
`corpus/lessons/round-52.md`, `quality/counters/c2-r52-proposition-entry.py` — in-flight
sibling/L1 integration, not this seat's; I read and executed but did not modify it.
I attack the boundary of both byte states; the landed one changes the answer
substantially (§B).

Fixture discipline: all tests ran against a `git clone -q --shared --no-checkout`
of the lane at `$S/fix/repo`, asserted `git rev-parse --show-toplevel` ==
`$S/fix/repo` before checkout to the base SHA, then `git checkout -q $BASE`
(read-only afterward; measurement mode issues only `ls-tree`/`show`). No tracked
edit, no lane write, no host mutation outside `/fast/scratch/hyaku/mado-r52/Attack05`.
Driver and transcript: `.ufo/waves/round-52/w2/Attack05/run-probes.sh`,
`.ufo/waves/round-52/w2/Attack05/probe-output.txt`.

## Frozen text attacked

`claims-frozen.md:7` — "a new committed counter … Demonstrate production pass and
control fail at the frozen revision." `registration.md:7` — counter "runs at a
requested pinned revision". `registration.md:11` — "Scratch only
`$HYAKU_SCRATCH/mado-r52/<seat>/`". `C1Evidence` ER-9 — "`python3 -I`; `--work`
under `/fast/scratch/hyaku/mado-r52/<seat>`; `/tmp`, `/var/tmp`, `/dev/shm`
refused; after-run `git status --porcelain` in the lane empty". `C1CounterDesign`
§9 — "`--work` is validated and created if absent, but nothing is written into
it". The boundary premise under attack: **the counter's filesystem footprint is
bounded by `--work`/`TMPDIR`, and current verification (`lane_unchanged`,
`fixture_worktree_residue`, receipts' porcelain checks) would detect a
violation.**

## A — Draft counter `0fe862f1` (the W1-evidenced artifact)

### A1 — Measurement mode performs an unconditional, git-invisible filesystem write; the boundary's own verification cannot see it — NOT REPRODUCED (falsifier)

`resolve_work()` (`c1-r52-ledger.py:768-787`, invoked at `:815` in measurement
mode, *before* `--repo`/`--rev` validation) ends with
`os.makedirs(real, exist_ok=True)`. Commands:

```
$ python3 -I c1-r52-ledger.py --repo $FIX --rev $BASE --work $FIX/sideeffect-dir
C1_R52: population=82 ledger_rows=82 ... verdict=TARGET_MET rev=85d57a8…   exit=0
$ test -d $FIX/sideeffect-dir   → DIR-CREATED
$ git -C $FIX status --porcelain              → 0 matching lines
$ git -C $FIX status --porcelain=v2 -uall     → 0 matching lines
$ git -C $FIX ls-files --others --exclude-standard → 0 matching lines
```

The counter's docstring ("nothing is written into it") is literally true and
materially false: nothing is written *into* `--work`, but `--work` itself is
*created* — a persistent filesystem mutation that every git-native view and the
`C1Fixture` harness's file-only walks (`c1-fixture-harness.py:91-137`
`lane_integrity` = `ls-files --others` + diffs; `:550-558` residue = `os.walk` →
`for name in files`) are blind to. A counter run whose `--work` names a path
inside the scored repo leaves litter `lane_unchanged=True` cannot detect. The
write also precedes validation, so exit-2 runs still mutate:

```
$ python3 -I c1-r52-ledger.py --repo /nonexistent --rev $BASE --work $S/p2/early-created
C1_R52: setup=error detail=--repo /nonexistent is not a directory     exit=2
→ $S/p2/early-created CREATED despite exit 2          (same for bogus --rev,
  missing --ledger file: dir created, exit 2)
```

Precedent this drops: `c1-r51-ledger.py:344` had a `W_OK|X_OK` writability check
and auto-removed a work dir it created (`finally: … rmtree(work)`); the draft
creates and never removes. The sibling C2 draft counter
(`c2-r52-proposition-entry.py:841-847`) already carries the exact guard —
`"scratch dir inside the scored repository"` refused before creation — so the
guard is established round convention, and C1's draft lacks it.

### A2 — No confinement: `--work` inside the scored repo is accepted; selftest nests a repo in it; crash residue is real — NOT REPRODUCED (falsifier)

```
$ python3 -I c1-r52-ledger.py --selftest --work $FIX/st-nest
C1_R52_SELFTEST: 53/53 passed   exit=0
→ $FIX/st-nest/ REMAINS inside the repo worktree (empty, git-invisible, porcelain 0)
$ python3 -I c1-r52-ledger.py --selftest --work $FIX/a/b/c
→ $FIX/a/b/c REMAINS (makedirs 3-level litter inside the repo)
```

SIGKILL mid-fixture (attempt 3 of 6) left the whole nested repository —
`$S/p5/kill3/c1-r52-selftest.4ro4kves/fixture/.git/**` — behind; `finally:
shutil.rmtree(root, ignore_errors=True)` (`:763-764`) cannot run on SIGKILL and
silently swallows partial deletes on other errors. The selftest's own
`rev-parse --show-toplevel` assertion (`:623-625`) checks the *fixture* root, not
that `--work` is outside the scored repo; `--selftest` ignores `--repo` entirely
(`:806-808`), so nesting inside the lane is permitted by construction.

### A3 — TMPDIR semantics changed from r51 and steer host state — NOT REPRODUCED (partial falsifier)

`cand = explicit or os.environ.get("TMPDIR")` (`:776`): with no `--work`, the
*ambient TMPDIR path itself* becomes the work root — and is created if absent.

```
$ env -u TMPDIR python3 -I c1-r52-ledger.py --repo $FIX --rev $BASE
C1_R52: setup=error detail=--work <dir> or a TMPDIR outside /tmp, /var/tmp, /dev/shm is required
   exit=2            ← measurement is inoperable without scratch it never uses;
                       the docstring usage line `… --repo <lane> --rev <rev>` fails as written
$ TMPDIR=$S/p3/steered-by-env python3 -I … --repo $FIX --rev $BASE   → TARGET_MET, exit 0
→ TMPDIR-CREATED: the env var alone caused a host dir creation
$ TMPDIR=/tmp python3 -I … --repo $FIX --rev $BASE
C1_R52: setup=error detail=refusing work dir under /tmp (got /tmp)    exit=2
   ← ambient /tmp TMPDIR (a normal host setting) hard-fails a write-free measurement
$ cd $S/p4 && python3 -I … --work relwork    → created $S/p4/relwork (cwd-floating)
$ cd $S/p4 && TMPDIR=rel-tmp python3 -I …    → created $S/p4/rel-tmp  (cwd-floating)
```

r51 took TMPDIR as a *base* for an auto-removed `mkdtemp` (`resolve_work`
`:333-335`, `finally` teardown) so a bare run worked; the draft uses TMPDIR as
the root itself, creates it, keeps it, and requires it for a mode that writes
nothing. Consequence for the harness: a caller who forgets `--work` gets exit 2
(setup error), not a measurement — ambient environment, not the CLI contract,
decides whether the counter runs at all.

### A4 — Harness/counter refusal asymmetry — REPRODUCED (fail-closed but inconsistent contract)

Harness `c1-fixture-harness.py:511` refuses only exact `/tmp|/var/tmp|/dev/shm`
(`realpath(work) in (...)`); the counter refuses any path *under* them
(`startswith(bad + os.sep)`). `--work /tmp/undertmp` therefore passes the harness
contract and is refused by the counter — verified `exit=2`,
`refusing work dir under /tmp (got /tmp/undertmp)`. Safe direction (fail-closed),
but the two apparatuses disagree on where the boundary is.

### Verified non-findings (draft `0fe862f1`)

`/tmp`, a symlink resolving to `/tmp`, and `/tmp/undertmp` all exit 2; `--work`
naming an existing file exits 2 with no mutation; `git_env()` (`:103-106`)
strips `GIT_*` — `GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent` measurement
still printed correct `rev=85d57a8…`, exit 0; selftest children inherit the
scrubbed env, and `TMPDIR=<probe>` during `--selftest --work <other>` leaked
zero files into the probe TMPDIR; `--work` == `--repo` root is accepted and
leaves nothing new (the root pre-exists); a symlink to a real scratch dir is
accepted via realpath; non-writable `--work` measures fine and selftest exits 2
on `mkdtemp` EACCES. Fixture repo afterward: `HEAD` still the base SHA,
porcelain lists only the git-visible untracked files that were already there.

## B — Landed bytes `923faf02` (worktree, in-flight): the boundary is absent entirely — NOT REPRODUCED (falsifier, worse)

The replacement implementation drops every boundary mechanism the draft had:

| premise attacked | command | observed | verdict |
|---|---|---|---|
| refused-roots guard exists | `--work /tmp` | TARGET_MISSED printed, **exit 1 — accepted, arg ignored** | falsified |
| `--work` validated | `--work $FIX/inside-work`, `--work /dev/null` | both run the measurement, exit 1; nothing created only because the arg is dead | falsified (silence, not confinement) |
| env-scrubbed git children (`git_env`) | `GIT_DIR=$S/foreign/frepo/.git python3 -I c1-r52-ledger.py --repo $FIX --rev HEAD` | prints `population=1 ledger_rows=1 … verdict=TARGET_MISSED rev=HEAD` — it measured **my foreign scratch repo** while `--repo` named the fixture; `rev=` echoes the unverified argument | falsified — environment steers the measurement |
| `--selftest` implemented | `--selftest --repo … --rev …` | runs the normal measurement; bare `--selftest` → argparse error exit 2 | falsified (dead flag) |
| pinned-rev echo | `--rev HEAD` | summary prints `rev=HEAD` verbatim, not the resolved sha | falsified |

And the decisive spillover this seat must report even though it is adjacent to
my scoped item: **the landed counter fails the green arm at the frozen base.**

```
$ python3 -I quality/counters/c1-r52-ledger.py --repo $FIX --rev $BASE
C1_R52: population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1
        self_pointer=0 generic_desc=0 verdict=TARGET_MISSED rev=85d57a8…   exit=1
```

`ledger_rows=83`: the base ledger's fenced grammar-example row (line 12,
`` `<repo-relative path>` | … ``) is parsed as data — the draft's `unfenced()`
(`:155-168`) is gone. The phantom row is `dangling=1 bad_pointer=1`, so
production **fails**, and the same shape-blindness means the frozen 4-cell
control's rows are silently dropped (`len(cells)==3` filter) rather than
scored-with-note as the draft did. If these bytes are what gets scored, C1's
green arm and red-arm attribution both collapse; all W1 receipts (harness
PASS 5/5, 53/53 selftest, hole-probes 6/6) were measured against `0fe862f1`
and do not transfer to `923faf02`. Second-order effect: `bad_pointer` semantics
also differ (landed checks `basename(path) in data` unbounded — substring, not
name-bounded), so W1's laundering probes are unverified against the landing.

## Synthesis (bounded, one move)

The draft's boundary is a refusal list with a side effect; the landed bytes have
no boundary at all. The compatible synthesis across the round's own artifacts
already exists and costs nothing new: adopt the C2 draft's
`scratch_dir()` guard (`c2-r52-proposition-entry.py:841-847` — refuse realpath
inside scored repo before creating), keep the draft's `realpath` + refused-roots,
drop `os.makedirs` from measurement mode (create lazily in selftest only, or
validate without creating), restore `git_env()` scrubbing into the landed file,
and delete the dead `--selftest`/`--work` args or implement them. That improves
operability (boundary becomes a stated, enforced contract) and harms no axis.

## Limitations

- `--work`-inside-repo was exercised only inside my scratch fixture, never the
  lane (fences); the code path is identical, so the conclusion transfers.
- Empty-dir invisibility is shown vs `git status` v1/v2+`-uall` and
  `ls-files --others`, and by reading the harness checks (file-only by line
  number); I did not re-run the full harness end-to-end against the residue.
- SIGKILL residue is timing-dependent: reproduced on attempt 3 of 6;
  `ignore_errors=True` partial-delete silence not separately exercised.
- `GIT_DIR` redirection demonstrated on this host's git; `-C`+env precedence is
  git-version behavior [INFERENCE elsewhere].
- The landed `923faf02` is untracked in-flight work; it may be superseded before
  scoring. Every §B verdict is against those exact bytes; if integration swaps
  them again, §B must be re-run — the sha256 is named for that check.
- A3's "inoperable without `--work`" is a designed trade-off (fail-closed
  scratch contract), scored here as an operability defect because measurement
  writes nothing; reasonable reviewers may weigh it lower than A1/A2/B.
- Scratch `/fast/scratch/hyaku/mado-r52/Attack05/` removed on exit; receipts
  retained in the seat dir. No installs, no package query, no live/host reads
  beyond spawning the counter under test against my own fixture.

Report: .ufo/waves/round-52/w2/Attack05.md
