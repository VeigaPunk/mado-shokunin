# w2 / SentScratch — containment and bounds of every C1/C2 scratch writer

Seat: `SentScratch` (sentinel, leaf). Round 48, wave w2 = FALSIFY, policy v1, base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
(lane HEAD at inspection `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`; this seat wrote no tracked file).
Target: check every C1/C2 scratch writer's containment and bounds — counter `--work`, the c2 replay
`TMPDIR`, the w1/w2 seat dispatch text, and unbounded loops/large writes — against the 2026-10-25 rule
(`/fast/scratch` only, no `/tmp`, ≤1 MiB/file, ≤2 GB/seat, scratch removed before return).

Method: read the frozen instruments (`quality/counters/c1-r48-terminal-cache.py`,
`quality/counters/c2-r48-xkb-entry.py`), the L1 draft helpers (`l1-draft/c1-score.sh`,
`l1-draft/c2-mirror.sh`), the wave dispatch JSON, and every `mktemp`/`TMPDIR`/`mkdtemp`/`while :`
site in the round-48 wave tree; then executed bounded probes: the c1 gate evaluated with the counter's
own `under()` for nine candidate work paths, a real c1 run that proves cleanup on a Setup exit, and the
c2 argument surface. Counter scoring itself was **not** run (that is the scoring seats' surface); no
claim here depends on a score.

Verdict: **no containment defect that breaks the frozen predicate or either counter's verdict was
found.** Seven bounds defects stand: two in the frozen instruments (F1, F2), one in the L1 mirror helper
(F5), one in three writers' `/tmp` fallbacks (F3), one inherited dispatch-rule conflict (F4), one
cleanup-failure class that makes the mandated trap lie (F6), and one unbounded counter write (F7). None
changes a predicate; F1/F2 mean a *compliant* invocation can still write outside `/fast`, so the wave's
scratch rule is prose for those two writers.

---

## F1 — c2 replay scratch accepts any `TMPDIR`, including `/tmp` and the lane repo (Medium, frozen instrument)

`quality/counters/c2-r48-xkb-entry.py:813-815`

```
            if not os.environ.get("TMPDIR"):
                raise Setup("TMPDIR required for replay scratch")
            S = tempfile.mkdtemp(dir=os.environ["TMPDIR"], prefix="c2r-")
```

The gate is *presence only*. There is no `--work` argument (`--help` shows `--repo/--rev/--base`; passing
`--work` exits 2 — `receipts/c2-arg-gate.txt`), and the counter carries no path-containment primitive at
all: `def under` 0, `realpath` 0, `commonpath` 0 (`receipts/containment-compare.txt`). c1 has all three
for the same purpose.

Exploit path (no privilege needed, no predicate change): `TMPDIR=/tmp python3 -I quality/counters/c2-r48-xkb-entry.py --repo <clone> --rev HEAD`
creates `/tmp/c2r-XXXX/{home,xdg,cache}`, runs the 73 KB keymap compile into it, and removes it in
`finally` — a host `/tmp` write by a documented invocation. `TMPDIR=<lane worktree>` instead plants an
untracked `c2r-*` tree inside the scored repository. The docstring's promise at `:92` ("with TMPDIR set to
an explicit round scratch root") is unenforced, so the clause cannot be cited as a containment property.
Scoring is unaffected (the counter reads the repo only through `git -C … show/rev-parse/grep`, `:178-183`),
so this is a rule/containment defect, not a scoring hole.

Impact: the 2026-10-25 rule is satisfiable only by operator discipline; a seat that exports `TMPDIR` once
(the wave asks exactly that) and is wrong writes host `/tmp` and no clause records it.

Smallest remediation: give c2 the c1 shape — `--work` required, the four-line gate
(`os.path.realpath` + `under` vs `{repo, lane_root(), dirname(lane_root())}`, `/run`, `/proc`), plus a
rejection of the `/tmp`, `/var/tmp`, `/dev/shm` realpaths (or an allowlist requiring the
`/fast/scratch/` prefix), and print the chosen scratch root on a clause line. Re-registration is allowed
pre-data (§ registration: "only before data may L1 re-register as a new version and re-run the complete
control set"), so this is fixable now; after data it is a miss, not an erratum.

## F2 — c1 `--work` admits `/tmp`, `/var/tmp`, `/dev/shm` (Medium-Low, frozen instrument)

`quality/counters/c1-r48-terminal-cache.py:998` (`--work` required) and `:1002-1014`:

```
1005        for h in sorted({os.path.realpath(a.repo), lane_root(), os.path.dirname(lane_root())}):
1006            if under(a.work, h):
1007                raise Setup("work dir inside a hidden path %s" % h)
1008        if under(a.work, "/run") or under(a.work, "/proc"):
...
1014            shutil.rmtree(work, ignore_errors=True)
```

`under()` is sound — both sides `os.path.realpath`, so a symlinked work path cannot dodge the gate
(`:891-893`) — and the lane-parent gate rejects the whole fleet root. But nothing rejects the tmpfs
family. Evaluated with the counter's own `under()` (`receipts/c1-work-gate.txt`):

```
/tmp/ss-x        rejected=False        /fast/scratch/hyaku/mado-r48/SentScratch/work  rejected=False
/tmp             rejected=False        <lane>/.ufo/x                                  rejected=True
/var/tmp/ss-x    rejected=False        <fleet root>/other-lane                        rejected=True
/dev/shm/ss-x    rejected=False        /run/x, /proc/x                                rejected=True
```

Exploit path: `--work /tmp/w` runs the full 394-fixture plus 230-generated matrix with every fixture tree,
`.rw` dir and oracle cache on tmpfs; a fixture family that writes 4 KB caches × 204 × 2 variants is small,
but the *budget* is the problem — the work is RAM-backed and vanishes on reboot, so the 2 GB ceiling cannot
be audited afterwards and a runaway seat is invisible to `du /fast`. Cleanup is correct when the process
exits normally: a real Setup-exit run left `work/` with 0 entries (`receipts/c1-work-cleanup.txt`), and
`finally` covers exceptions, not SIGKILL.

Impact: same rule class as F1, lower because the counter never leaks residue by itself and the L1's own
invocation (`l1-draft/c1-score.sh:9-10`, `--work "$S/work"` under `/fast`) is compliant.

Smallest remediation: extend the gate with `for t in ("/tmp","/var/tmp","/dev/shm")` → `Setup`, or require
`under(a.work, "/fast/scratch")`; print the resolved work root on clause `meta`.

## F3 — three round-48 writers still fall back to host `/tmp` (Low-Medium)

| path:line | code |
|---|---|
| `.ufo/waves/round-48/w1/ExecXkbSource/verify.sh:155` | `TMPD=$(mktemp -d "${TMPDIR:-/tmp}/xkbverify.XXXXXX")` |
| `.ufo/waves/round-48/w1/ExecLsEmu/fuzz.py:557` | `base = os.environ.get("TMPDIR") or "/tmp"` → work dir `/tmp/lsemu-fuzz` |
| `.ufo/waves/round-48/l1-draft/add-replay-clause.py:39` | `S = tempfile.mkdtemp(dir=os.environ.get("TMPDIR") or "/tmp", prefix="c2r-")` |

(`receipts/tmp-paths.txt`.) Every other seat writer in the wave either mints under an explicit `/fast`
root (`mktemp -d -p "$S"` in `w1/ExecXkbLive/probe.sh:21`, `w1/ScrEntry/receipts/make-receipt.sh:12`,
`w1/SentHost/probe.sh:11`, `w1/ExecErrataR45/counter-append-test.sh:22`) or hardcodes the `/fast` path
(`w1/ExecHomeUnset/run.py:20`, `w1/ExecHomeUnset/probe-fifo.py:18`). `verify.sh:15` even advertises the
fallback as a feature ("Writes only under `$TMPDIR` (default: a fresh mktemp dir)").

Exploit path: `env -u TMPDIR ./verify.sh` from the seat dir writes its generation tree (copied
`rules/generator` sources, ~300 symbol symlinks, two `rules.generator` runs) into host `/tmp`; the trap
removes it, so the failure is silent. `add-replay-clause.py` is the *generator that installed the frozen c2 clause*:
re-running it with `TMPDIR` unset demonstrates the same class in the instrumentation path.

Observed residue: none — `/tmp/xkbverify.*`, `/tmp/lsemu-fuzz`, `/tmp/c2r-*`, `/tmp/c1r48-*` all absent
(`receipts/tmp-residue.txt`: `matches=0`). Latent, not realized.

Smallest remediation: `${TMPDIR:?TMPDIR required}` / `os.environ["TMPDIR"]` (fail closed), or an explicit
`-p /fast/scratch/hyaku/mado-r48/<Seat>` root. `add-replay-clause.py:39` should mirror the installed
counter, which is already strict (`os.environ["TMPDIR"]`, no fallback).

## F4 — the w1 dispatch sanctions 50 MB per file in `/tmp` and carries no executable bound (Medium, historical)

`.ufo/waves/round-48/w1-spec.json:3` (the shared `context` string handed to all 41 items) reads:

> …(operator directive 2026-10-25): every clone, venv, build, fixture tree and work dir lives under
> /fast/scratch/hyaku/mado-r48/&lt;YourSeatName&gt;/ …; **/tmp only for files under 50 MB**; keep it under
> 2 GB AND bound every loop and every write (round-47 incident: a seat streamed ~590 GB into a
> FIFO-named path; never `yes`, never an unbounded redirect, never write into a FIFO or device; cap
> generated files at 1 MB)…

Item-level count (`receipts/spec-bounds.txt`): `w1-spec.json` **41 items, `ulimit` 0, "1 MB|1 MiB" 0,
"50 MB" 0, `/fast/scratch` 0** — the 1 MB cap and the `/fast` root exist only in the shared context, and
no item carries the writer command. `w2-spec.json` is **48/48 items with `ulimit -f 2048` and "1 MB"**.

Two distinct defects, one already on record: the missing executable bound is w1's recorded mistake
`M48-5` (`w1/ScrMistakes.md:15`, `enforced=0 prose=4 verdict=PROSE-ONLY`; mined text
`w1/ScrMistakes/receipts/m47-7-mined.txt`, "r47 : … /tmp only for files under 50 MB …" vs the r48 variant
"AND bound every loop"). Not on record: that clause is **the round-47 wording**, and it *permits* up to
50 MB per file in host `/tmp`, contradicting the 2026-10-25 rule ("Never use /tmp") that the very same
sentence claims to implement. A seat reading its own dispatch got an explicit grant to write 50 MB files
to `/tmp`, with no ulimit and no per-file 1 MB cap in its item text.

Impact: w1 evidence produced by shell writers has no enforced write ceiling, and the dispatch that told
them so also authorised the wrong filesystem — exactly the blast radius of the 590 GB incident (prose-only
bound). w2 is correct, so this does not touch the frozen predicate; it does mean any w1 receipt whose
producer was a shell writer cannot be cited as *bounded by construction*.

Smallest remediation (freeze note, not a rewrite): strike "…/tmp only for files under 50 MB" from the
carried-forward rule text; the w2 wording is the reference. Any future wave dispatch that re-uses the r47
sentence reintroduces the conflict.

## F5 — `l1-draft/c2-mirror.sh` leaks a 313 MB clone per run (Low-Medium, live)

`l1-draft/c2-mirror.sh:8-9`:

```
S=${2:-/fast/scratch/hyaku/mado-r48/L1c2}
rm -rf "$S"; mkdir -p "$S/m"
```

Cleanup happens **only at the start of the next run**; there is no `trap … EXIT`, and the script ends with
`echo census exit=…`. `c1-score.sh` is better (`:21 rm -rf "$S/c" "$S/work"`) but still leaves `$S` and
`out.txt`, and also has no trap.

Measured state (`receipts/scratch-leftovers.txt`): five full clone trees remain under
`/fast/scratch/hyaku/mado-r48` — `L1c2` (21:40:22, 313 MB on disk, 20 396 files), `L1c2-r2` (22:09:39,
313 MB), `L1c2-r3` (22:11:15, 313 MB), `RevC2Counter` (22:23:32, 313 MB, 20 987 files), `L1cnt` (20:58:42,
310 MB) — ≈1.55 GB of the 2.3 GB aggregate at 22:25 UTC. Each is a `git clone --shared` + full worktree
copy + `corpus` copy (`c2-mirror.sh:12-30`). At 01:26 UTC the aggregate was 4.5 GB (`du --apparent-size`,
all live w2 seats), but the per-seat figures stayed inside the budget: the largest seat tree then was
`ConnMistakes` 323 MB apparent, and every other seat `≤283 MB` — so the 2 GB/seat ceiling held; what leaked
is the *superseded* mirror class, not a single seat's budget.

Impact: a seat that ran the helper twice (as the L1 did: `L1c2`, `-r2`, `-r3`) has no evidence that its
scratch was removed, and the round aggregate carries ~1.5 GB of dead clones for the life of `/fast`. Any
future seat copying this helper inherits the leak.

Smallest remediation: `trap 'rm -rf -- "$S"' EXIT INT TERM` in both helpers (keeping the `rm -rf` at start
for a stale-previous-run), and remove the five leftovers at wave close.

## F6 — a mode-000 scratch directory is unremovable by `rm -rf` and defeats size audit (Medium-Low)

`/fast/scratch/hyaku/mado-r48/RevC1Ls/probe/u/app/unread` is mode `d---------` (harness class:
`w1/ExecRefCacheA/harness/harness.py:212` `os.chmod(sub, rng.choice([0o444, 0o000, 0o500]))`). Measured
(`receipts/mode000-removal.txt`), not assumed:

```
$ rm -rf -- "$S/rmtest"            # own fixture: one 000 directory holding one file
rm: cannot remove '…/rmtest/inner': Permission denied
rc=1
left behind
$ chmod -R u+rwX -- "$S/rmtest" && rm -rf -- "$S/rmtest"
rc=0
removed
```

So the standard cleanup idiom the wave mandates — `trap 'rm -rf -- "$S"' EXIT` — **fails on the whole
tree** as soon as one fixture pins mode `000` on a non-empty directory (GNU `rm` must traverse it), and the
seat's "delete your scratch dir before you finish" claim then cannot be true. The same class reaches the
frozen counter: `shutil.rmtree(work, ignore_errors=True)` (`c1-r48-terminal-cache.py:1014`) would silently
leave `c1r48-*` behind — latent only because the frozen set has no mode-0 entry (204 fixtures, `modes=0`
count 0), so the counter's own work is currently safe.

Impact on audit: `du -sh /fast/scratch/hyaku/mado-r48` aborts with `Permission denied` on that path, so any
aggregate is a floor — 2.3 GB at 22:25 UTC, 4.5 GB at 01:26 UTC with w2 seats live (the growth is concurrent
seats, not proof of leakage; each individual seat measured then was ≤323 MB, i.e. inside the 2 GB budget).
The "clean before return" and "<2 GB" checks are therefore unverifiable for that one seat and countable only
as a lower bound for the round.

Smallest remediation: the cleanup trap should be
`trap 'chmod -R u+rwX -- "$S" 2>/dev/null; rm -rf -- "$S"' EXIT` (and the counters should chmod-and-retry
rather than pass `ignore_errors=True`); any size audit should walk with `find -printf '%s\n'` after the
chmod, which is how the per-seat numbers above were obtained.

## F7 — the strace trace file is the only unbounded-size host write inside c1 (Low)

`c1-r48-terminal-cache.py:302` creates `trace-*` under `--work` via `tempfile.mkstemp` and `:310` runs
`strace -f -o <trace>`; `check_trace` (`:331`) then reads the whole file into memory. The trace's size
scales with what the traced tree execs in the 60 s window (`timeout=60` at `:301`), and the counter imposes
no per-file ceiling of its own — it inherits the caller's `RLIMIT_FSIZE`. With the w2 rule
(`ulimit -f 2048`) that is 1 MiB; with the w1 dispatch (F4, `ulimit` 0) it was unbounded. A mutant that
fork-execs in a loop trips clause r on the first post-python `execve`, but only after the trace grew for the
rest of the run.

Impact: bounded in practice by the 60 s timeout and by the trip list, unbounded by contract; it is the one
place where a hostile or broken tool can inflate a *counter* write.

Smallest remediation: treat a trace file larger than 1 MiB as a trip (`self.trips.append("trace-oversize")`),
or set `RLIMIT_FSIZE` in the sandboxed child.

---

## Verified clean (each claim backed by a command above or by the cited lines)

- c1 `--work` is required (`:998`), must exist (`:1003-1004`), and rejects the repo, the lane, the lane's
  parent (i.e. the whole fleet root) and `/run`, `/proc`, via realpath-normalised `under()` (`:891-893`,
  `:1005-1009`). A real run that exits through `Setup` left `work/` empty (`receipts/c1-work-cleanup.txt`):
  `c1r48-*` removal is in `finally` (`:1010-1014`).
- c2's replay tree is removed in `finally` (`c2-r48-xkb-entry.py:815-849`); its only remaining gap is F1.
- Both counters touch the repository read-only and revision-addressed: `git -C <repo>` only
  (c1 `:171`, c2 `:178-183`); no checkout, no worktree, no write into the scored tree.
- Every sandbox invocation has a timeout: c1 `run()` 60 s, `prime()` 120 s, selftest 120 s
  (`:301`, `:319`, `:900`); c2 probes 60 s (`:828`). No hang class that could grow scratch without bound.
- Fixture-driven write sizes are small by construction: 204 fixtures, longest `cache` literal 4 225 B,
  longest `after.files` value 203 B, fixture file 241 156 B (`receipts/fixture-write-bounds.txt`).
- No unbounded loop in the frozen instruments: c1's `WAITER` is bounded at 1 200 spins × 400 increments
  (`:146-162`); the two `while :` loops in w1 (`ExecFixturesV2/gen.py:60`, `ExecFixturesV2/prime-wrap.sh:24`)
  are deadline-bounded on `EPOCHREALTIME` (5 s) *and* terminator-bounded; they ran only during w1 fixture
  generation, and the installed counter carries its own inline waiter, so no scoring run executes them.
- In-sandbox `/tmp` is a bwrap tmpfs, not a host write: `--tmpfs /tmp` and `--chdir … or "/tmp"`
  (`c1:274-288`, mirrored in the seat harnesses). Not counted as a finding.
- w2 dispatch: 48/48 items carry `ulimit -f 2048` and the 1 MB/file cap; the context forbids `/tmp`
  (`receipts/spec-bounds.txt`).
- `l1-draft/mado-terminal.py:1397` mints its selftest tree with `dir=os.environ.get("TMPDIR") or None` and
  removes it in `finally` (`:1423-1425`): it honours `TMPDIR` and cleans up; with `TMPDIR` unset Python's
  `gettempdir()` picks `/tmp`, so it is *compliant* with "never hardcode /tmp" but not exempt from F3's
  fail-closed recommendation.

## Bounds accounting for this seat

- Scratch: `/fast/scratch/hyaku/mado-r48/SentScratch` (created explicitly, removed at close).
- Every writer shell began with `ulimit -f 2048` (512-byte units → 1 MiB per regular file); no shell
  command in this seat wrote more than 2 KB in one file (the 19 KB report was written by the editor tool,
  not by a shell writer).
- Receipts: `.ufo/waves/round-48/w2/SentScratch/receipts/` — 11 files, 6 324 B total; largest
  `tmp-paths.txt` 1 126 B. `receipts/seat-bounds.txt` lists the other ten (5 771 B).
- Largest output file of this seat: `w2/SentScratch.md` (this report, 18 561 B at final measurement — the
  only file above 2 KB; every receipt is under 1.2 KB).
- No package transaction, no `xdg-terminal-exec` run, no host config, no compositor, no GUI, no `/tmp`
  write, no lane Git/jj mutation and no commit.

## Residuals / not covered here

- Counter scoring, fixture content correctness and the predicate itself are other seats' surfaces; this
  seat read the instruments and executed only gate/argument/cleanup probes.
- Sizes are what `du` could see; F6 makes the round aggregate a lower bound (2.3 GB observed).
- The five leftover mirror trees (F5) were left in place: they are other seats' live scratch and deleting
  them is outside this seat's write scope.
