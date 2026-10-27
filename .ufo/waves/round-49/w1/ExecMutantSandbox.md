# ExecMutantSandbox — mado round 49, w1: an executed host-state guard for mutants and counters (M48-10)

Seat `ExecMutantSandbox`, leaf, wave `w1` = BUILD, base `03e4ae76aff7a4be59cb69970dd553baa319695a`. Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Nothing tracked was edited and no lane/fleet Git state was touched:
the seat wrote only inside `.ufo/waves/round-49/w1/ExecMutantSandbox/` plus this file. Scratch
`/fast/scratch/hyaku/mado-r49/ExecMutantSandbox/` was created under `ulimit -f 65536`, used by every case, and
removed by the driver's `trap` (the directory is gone; no scratch path is cited as evidence, only values emitted
inside the receipts).

Files (all new):

| path | sha256 | size |
|---|---|---|
| `.ufo/waves/round-49/w1/ExecMutantSandbox/hostguard.py` | `4329050cba9f5be468588da1e1633e480cee647ecfac4a6f92a8d408aa085052` | 431 lines |
| `.ufo/waves/round-49/w1/ExecMutantSandbox/demo.sh` | `16ce3d98d6453604b9cf7174bea0ea2cc7df05c3a3d64bf59eda24607ba45198` | 261 lines |
| `.ufo/waves/round-49/w1/ExecMutantSandbox/receipts/` | 20 files, 32,196 B | driver output |
| `.ufo/waves/round-49/w1/ExecMutantSandbox.md` | this report | |

`receipts/00-setup.txt:3-4` pins the run: `hostguard_sha256=4329050c…`, `python=Python 3.14.8 bwrap=bubblewrap 0.13.1 ulimit_f=65536`.

---

## 1. What the guard is

`hostguard.py` is Python 3 stdlib only, no third-party imports, runs under `python3 -I` (`receipts/j-isolated-mode.txt:2`, `exit=0`). Two
subcommands:

- `digest --declare PATH…` — read-only: lstat + full sha256, prints one record per path and exits 0. This is the
  only subcommand that may be pointed at real operator state.
- `run --work DIR --declare PATH… -- COMMAND…` — digests, runs COMMAND with `HOME`, `XDG_CACHE_HOME`,
  `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME` and `TMPDIR` pointed into `--work`, digests again, and exits 3
  if any record moved. `--sandbox bwrap --mask DIR` additionally mounts an empty tmpfs over each masked path;
  `--ro-root` makes the host read-only except `--work`.

Each record is `label kind= size= mtime_ns= ino= dev= sha256= path=` with the label defaulting to
`operator-owned`, so a receipt can be read without the tool's prose. A change line names the fields that moved, so a
same-size same-mtime rewrite reports `fields=sha256` alone.

Exit codes (`hostguard.py:43-48`): `0` no declared path changed; `2` usage error or a refused path; `3` a declared
path changed; `4` prerequisite missing (bwrap absent, a `--mask` that is not a directory); `5` the child failed;
`6` internal error. The child's own status is never propagated — a child that exits 3 with nothing changed reads 5
(`receipts/e-refusals.txt:22,36`).

Refusals, all fixed and not overridable by a flag:

- a write-side directory (`--work`, `--home`, any XDG dir, TMPDIR) under `/tmp`, `/var/tmp` or `/dev/shm`
  (`hostguard.py:108`, round-48 `w2/SentScratch`); inside the operator home of the invoking uid — taken from
  **passwd, not `$HOME`** (`hostguard.py:111`); or inside the repository the script itself lives in
  (`hostguard.py:114`);
- a `--declare` target that is a directory, FIFO, device or socket: refused before any open
  (`hostguard.py:147-152`, kind test at `:151-152`), so a declared FIFO is never opened;
- a `--mask` that covers `--work` or the child cwd (the child could not reach its scratch);
- no declaration at all, or more than 64.

`--mask` is deliberately the one argument that may name the real home: a tmpfs over it writes nothing to it. This
seat never ran the guard against the real home in any mode; the demonstration substitutes a fake home for it.

## 2. The demonstration, on a fake operator home only

Fixture: `$S/fakehome/.cache/xdg-terminal-exec`, 331 B, sha256 `0de3d0c6…101b`, mtime pinned to
`1793047345000000000` (`receipts/00-setup.txt:6`) — the shape and mtime convention of the round-47/48 records, with
content that cannot be mistaken for the operator's file. The mutant is M48-10's own shape (write
`$HOME/.cache/xdg-terminal-exec`), plus a second variant that takes a **hardcoded absolute target**, which HOME
redirection cannot stop.

| case | child, guard mode | receipt | observed |
|---|---|---|---|
| A | mutant, `--home <fake home>`, no sandbox | `a-unsandboxed-caught.txt:15-16` | `CHANGED … fields=sha256,size,mtime_ns`, `status=violation exit=3` |
| A2 | same, payload of the original size, original mtime restored by the mutant | `a2-same-size-mtime-restored.txt:15-16` | `fields=sha256`, `size=331->331`, `mtime_ns=…000->…000`, `exit=3` |
| B | same mutant, `--sandbox bwrap --mask <fake home>` | `b-sandboxed-contained.txt:14` + mutant line 1 | mutant reports `out_size=19` written (so the write **succeeded**), guard `changed=0 status=ok exit=0` |
| B2 | `--sandbox bwrap --ro-root`, write attempted at HOME | `b2-ro-root.txt:1-2` | `WRITE_BLOCKED errno=30` (EROFS), `TMPDIR_WRITE_OK size=1`, `caseB2_exit=0` |
| C | `true`, nothing to change | `c-control-no-change.txt:13` | `changed=0 status=ok exit=0` |
| C2 | child writes `$XDG_CACHE_HOME/legit-probe.txt` | `c2-legit-scratch-write.txt:20` | `caseC2_exit=0 … probe_exists=yes` — a scratch write is not a violation |
| I1 | **hardcoded** target = fake cache, no sandbox | `i1-hardcoded-unsandboxed.txt:14-15` | `CHANGED … size=331->17`, `exit=3` |
| I2 | same hardcoded target, `--mask <fake home>` | `i2-hardcoded-masked.txt:14` + line 1 | mutant reports the write succeeded, `changed=0 status=ok exit=0`, cache sha still `0de3d0c6…` |
| H1/H2 | the adoption shape (below), fake home standing in for the operator home | `h1-…txt:14`, `h2-…txt:15` | both `exit=0`, cache sha `0de3d0c6…` |
| E1-E8 | refusals and the child-status separation | `e-refusals.txt:1-52` | eight `exit=2`/`exit=5` lines as designed |
| G | `--json` + `--declare-file`, mutant run | `g-json.txt:3` | `JSON status=violation changed=1 child_rc=0 sandbox=none declared_label=operator-owned` |

Case B/I2 is the containment claim and it is measured, not assumed: the mutant prints the size and hash it wrote,
so the write happened, and the declared bytes outside are unchanged. The two ways a counter would otherwise fool
itself are both closed — HOME redirection alone (H1) and the tmpfs mask for a hardcoded path (I2) — and the
`--ro-root` mode (B2) blocks the write at the kernel instead of diverting it.

`receipts/00-case-exits.txt` is the one-line-per-case index of this table; all ten lines read the expected status.

## 3. The one real-state read (read-only, shape-only)

`receipts/d-operator-cache-digest.txt` (the home directory is written as `~`):

```
operator-owned kind=file size=190 mtime_ns=1793069967287759266 ino=143468605 dev=56 sha256=ddd94f6bca4bcd42c426da9bbeb9955ca5d77b8778b4e290fcfffcc984a1b3d5 path=~/.cache/xdg-terminal-exec
```

An independent `stat`/`sha256sum` of the same path in the same receipt agrees (`size=190 mtime=1793069967
inode=143468605`). This is the N2 pair the closure asked for: today's operator cache is 190 B, `ddd94f6b…`, mtime
`1793069967` — the same values `corpus/lessons/round-48-verifier-spotcheck.md:180` states, now emitted by a tool
that labels the record `operator-owned` instead of `host_cache_untouched_sha256`. Nothing was opened for write.

## 4. Exact usage the counters should adopt

Mutant / any command that may write (the M48-10 shape). `$WORK` is the counter's own scratch root; the guard does
not create it outside `--work`:

```sh
python3 tools/hostguard.py run \
    --work "$WORK/guard" --work-prefix /fast/scratch \
    --sandbox bwrap --mask "$HOME" --mask "$XDG_CACHE_HOME" \
    --declare "$HOME/.cache/xdg-terminal-exec" \
    --env-keep LANG \
    -- <env-scrubbed command ...>
```

- `--work-prefix /fast/scratch` makes the seat's scratch rule an executed refusal rather than prose;
- `--mask "$HOME"` is replaced here by the fake home (cases B/H2/I2 execute exactly this shape); it contains a
  mutant with a hardcoded operator path, which HOME redirection cannot;
- HOME/XDG are redirected by the guard itself, so a mutant that derives its target from ambient `HOME` writes into
  `$WORK/guard/home` (case H1) and the declared operator path is untouched;
- the guard never forwards the child's exit status: read `child_rc=`/`status=` from the table or `--json`.

Judge / read-only command (score runs, `xkbcli`, a Python tool with no network):

```sh
python3 tools/hostguard.py run --work "$WORK/guard" --work-prefix /fast/scratch \
    --sandbox bwrap --ro-root --declare "$HOME/.cache/xdg-terminal-exec" \
    -- <judge argv>
```

`--ro-root` keeps the host read-only except `--work` (case B2 shows the EROFS and a writable TMPDIR), so a scored
tool that tries to write anywhere outside its scratch fails loudly instead of mutating the host.

Counters that need machine-readable output add `--json` (case G) and read `status`, `changed[].fields`,
`child_rc`, `env`, `mask`.

## 5. What it does not do (stated, not hidden)

- A digest is "no change observed across the run", never "the child caused it". An operator-side write during the
  window is reported as a violation — honest for a guard, useless for attribution; the same limitation N2 recorded
  for the old `host_cache_untouched` field.
- It watches what is declared. A mutant that writes somewhere else (e.g. `/tmp`) is caught only by `--ro-root`
  or by declaring that path. Up to 64 declared paths, each read in full (no size cap: declarations are meant for
  small state files).
- Singleton paths only: a directory, FIFO, device or socket is refused rather than walked, so a tree change is out
  of contract by design.
- bwrap needs user namespaces; without `bwrap` on PATH the run exits 4 and never silently degrades to unsandboxed.
  `--mask`/`--ro-root` are Linux-only.
- The guard does not stop a command from spawning, it contains where the command may write. It is not a seccomp
  profile and says nothing about a child that escapes its mount namespace.
- `--declare` resolves `~` with the invoking uid's home, which is what a counter wants; a receipt should still
  print `~` (the driver does, `demo.sh` sed of the D receipt).

## 6. Integration notes for the L1

- Suggested landing is `tools/hostguard.py` (the L1 integrates; this seat wrote no tracked file). Stdlib only, so
  the counters can copy-invoke it exactly as C1's judge invokes `xkbcli`.
- It closes the mechanism behind M48-10 for any counter that adopts it, and closes `w2/SentScratch` F1/F2 *for
  those counters only*: `--work` under `/tmp` is refused by the tool, not by seat discipline. The round-48 frozen
  counters still carry the old `--work` gate until w2 attacks the new one.
- The demonstration is a fake home by construction. Whether the operator wants `hyprctl`-style live state in the
  declared list is an operator decision, not a seat one; the tool supports it with the same command.
- No pacman, no package transaction, no host service, no compositor mutation, no terminal, no network, no subagent.
  Scratch removed. Tool installs: none.

## 7. What was run and what was not

Run: the ten demonstration cases, the eight refusals, the `--json`/`--declare-file` surface, `python3 -I -E -s`
on the tool (`receipts/j-isolated-mode.txt:2`, exit 0), child-flag passthrough (`ARG=--keymap=x`, a child
`--keymap=x` reached the child untouched), and the single read-only digest of the operator cache.
Not run: no counter scoring, no lane gate, no build, no commit — those are the main agent's post-integration gate.
