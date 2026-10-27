# ExecHomeUnset — round-47 closure D1: HOME unset, FIFO entries and other refusals — pin vs landed tool

Seat `ExecHomeUnset`, round 48 wave `w1` (BUILD), lane `mado-shokunin`, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Read-only seat: no lane file edited, no package installed, no compositor or terminal launched.

**Verdict.** 19 fixtures, pin and landed tool side by side in the round-47 C1 counter's own sandbox: 11 agree on
exit status and stdout, 8 diverge. The three refusals the landed docstring added after the freeze (D1) are **not one
class**: unreadable inputs are modelled correctly; **symlink loops are modelled** (4 shapes agree — the docstring
over-declares them); **HOME unset** is modelled only for the case the closure measured, and the tool refuses a
selection the pin *does* make when all three XDG defaults are set; **a FIFO is refused at walk time, one step too
early**, so a tree where the pin answers normally (`rc 0`) gets `exit 2` from the tool. The closure's sentence
"exits 2 where the pin exits 1 (HOME unset) or blocks (FIFO)" (`corpus/lessons/round-47-verifier-spotcheck.md:129-130`)
is therefore true only of the sub-case it happened to test. Sections 5 and 6 give the D1 lesson line and the
round-48 contract text this measurement supports.

## 1. Method (reproducible)

Driver `.ufo/waves/round-48/w1/ExecHomeUnset/run.py` (sha256 in `run.log`) imports the round-47 C1 counter read-only
and uses its **own** `Box`/`materialize`/`case_env`, so the pin runs under exactly the instrument's allowlist:
`bwrap --unshare-all --die-with-parent --new-session --clearenv`, `/usr/lib` ro, `/bin/sh` = host bash,
`/oracle/bin` = copies of the resolver's seven externals (`tr find awk ls md5sum mkdir rm`), `/dev`, `/proc`, tmpfs
`/tmp`, case root ro with its `.rw` writable (`XDG_CACHE_HOME=$ROOT/.rw/cache`), no `/etc`, `/home`, `/usr/share`
or `/fast` of the host. The tool run is wrapped in `strace -f -e trace=execve,execveat,socket,socketpair,connect`
and every run reports `trips=[]` (no process, no socket) — the seat's own read-only witness.

| item | value |
|---|---|
| pin | `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (= `/usr/bin/xdg-terminal-exec`) |
| tool scored | `tools/mado-terminal.py` at base, sha256 `b84d5c4f723049c0fd14189ffc7b6db1f71eb70fb97e0c476d20ddeca6de2222` |
| trees | one tree per fixture per side (pin and tool never share a root, so the pin's background cache save cannot leak) |
| env baseline | `HOME=$ROOT/home`, `PATH=$ROOT/bin:/oracle/bin`, `XDG_CONFIG_HOME=$ROOT/home/.config`, `XDG_CONFIG_DIRS=$ROOT/etc/xdg`, `XDG_DATA_HOME=$ROOT/home/.local/share`, `XDG_DATA_DIRS=$ROOT/usr/share`, `XDG_CACHE_HOME=$ROOT/.rw/cache`, `LANG=C.UTF-8`; a fixture may delete a variable |
| pin timeout | 10 s per run (`124` = still running at the cap) |
| env construction | `--clearenv` plus an explicit `--setenv` per variable; a fixture "deletes" a variable by omitting it, so nothing of this session's environment leaks into the pin or the tool (a host probe with only `env -u HOME` proves nothing here — see the trap in section 7) |
| determinism | 3 full runs (19 fixtures each), `determinism-run{1,2,3}.json`: every `rc`, `stdout` and `agree` field identical; the only byte difference is the scratch work-dir prefix inside `stderr1`, which `stderr` normalises to `$ROOT` |

Reproduce: `TMPDIR=<scratch> python3 -I .ufo/waves/round-48/w1/ExecHomeUnset/run.py` (receipts: `pin-vs-tool.json`,
`run.log`; probes `probe-fifo.py` → `fifo-block.txt`, `probe-registration.py` → `registration-traces.txt`).

## 2. Results (pin vs tool, exit status and stdout)

`$ROOT` is the case root; stdout is quoted verbatim.

| fixture | args | pin rc | pin stdout | tool rc | tool stdout | agree |
|---|---|---|---|---|---|---|
| C0-baseline | `--print-id` | 0 | `term.desktop\n` | 0 | `term.desktop\n` | yes |
| C1-home-unset-no-xdg (`HOME` and every `XDG_*` from the baseline unset) | `--print-id` | 1 | `` | 2 | `` | **no** |
| C2-home-unset-all-xdg (`HOME` unset, all four XDG dirs + cache set) | `--print-id` | **0** | `term.desktop\n` | 2 | `` | **no** |
| C2b-home-unset-all-xdg-print-cmd | `--print-cmd` | **0** | `$ROOT/bin/term\n` | 2 | `` | **no** |
| C3-home-unset-no-cache-home (`XDG_CACHE_HOME` unset) | `--print-id` | 1 | `` | 2 | `` | **no** |
| C3b-home-unset-no-data-home (`XDG_DATA_HOME` unset) | `--print-id` | 1 | `` | 2 | `` | **no** |
| C3c-home-unset-no-config-home (`XDG_CONFIG_HOME` unset) | `--print-id` | 1 | `` | 2 | `` | **no** |
| C4-home-empty (`HOME=""`, XDG set) | `--print-id` | 0 | `term.desktop\n` | 0 | `term.desktop\n` | yes |
| C4b-home-empty-no-xdg (`HOME=""`, all XDG unset) | `--print-id` | 1 | `` | 1 | `` | yes |
| C5-fifo-later-dir-unused (FIFO `foot.desktop` in `XDG_DATA_HOME/applications`, `term.desktop` in `XDG_DATA_DIRS` wins) | `--print-id` | **0** | `term.desktop\n` | 2 | `` | **no** |
| C6-fifo-later-dir-listed (same FIFO, named as the listed candidate) | `--print-id` | **124** (blocks) | `` | 2 | `` | **no** |
| C7-fifo-first-dir (FIFO in the lowest-preference app dir) | `--print-id` | 0 | `term.desktop\n` | 0 | `term.desktop\n` | yes |
| C8-symlink-loop (`applications/loop -> applications`) | `--print-id` | 0 | `term.desktop\n` | 0 | `term.desktop\n` | yes |
| C12-loop-desktop-symlink (`applications/loop.desktop -> applications`, listed) | `--print-id` | 1 | `` | 1 | `` | yes |
| C13-subdir-cycle (`applications/sub/loop -> applications`, `sub/term.desktop` listed) | `--print-id` | 0 | `sub-term.desktop\n` | 0 | `sub-term.desktop\n` | yes |
| C9-unreadable-entry-not-candidate (`aaa.desktop` mode 000, never listed) | `--print-id` | 0 | `term.desktop\n` | 0 | `term.desktop\n` | yes |
| C10-unreadable-entry-only (mode 000, the only listed candidate) | `--print-id` | 1 | `` | 1 | `` | yes |
| C14-dir-shadows-file-later-dir (a *directory* named `x.desktop` in `XDG_DATA_HOME/applications`, valid `x.desktop` file in `XDG_DATA_DIRS`, listed) | `--print-id` | 1 | `` | 1 | `` | yes |
| C11-unreadable-list (`xdg-terminals.list` mode 000) | `--print-id` | 1 | `` | 1 | `` | yes |

Tool stderr on every "**no**" row is one line, `MADO_TERM_OUT_OF_CONTRACT: <reason>` with reason `HOME unset` or
`a FIFO named like a desktop file (the resolver blocks reading it)`, exit 2.

## 3. What the pin actually does, per refusal class

### 3.1 HOME unset — fatal only where a default is expanded, and only three places do that

`grep -n HOME` over the pin returns exactly three expansion sites, all in `make_paths`:
`:148` `for xte__dir in ${XDG_CONFIG_HOME:-"${HOME}/.config"}…`,
`:166` `for xte__dir in ${XDG_DATA_HOME:-${HOME}/.local/share}…`,
`:172` `XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}` (quotes Q1-Q3, `quotes-check.txt` 13/13 ok).
The script is `set -euf`, so an unset `HOME` under `-u` aborts the shell with `rc 1` and empty stdout; measured
stderr is the shell's own text, naming the first failing line: `line 148` (C1, C3c), `line 166` (C3b),
`line 172` (C3). Nothing else in the pin reads `HOME`.

So `HOME` unset is **not** by itself fatal: when `XDG_CONFIG_HOME`, `XDG_DATA_HOME` and `XDG_CACHE_HOME` are all set,
none of the three defaults is expanded and the resolver behaves normally — C2 `rc 0` printing `term.desktop`, and
C2b `rc 0` printing the command line (the background cache save also works, `XDG_CACHE_HOME` being set). The landed
tool refuses both with exit 2 (`tools/mado-terminal.py:410`), i.e. **on C2/C2b it refuses a selection the resolver
makes**, which is a stronger divergence than the closure recorded (it said "pin exit 1, tool exit 2").

`HOME=""` (set but empty) is in contract on both sides: defaults become `/.config`, `/.local/share`, `/.cache`
(C4b `rc 1` no terminal on both; C4 `rc 0` on both with the XDG dirs set) — the tool already models it.

### 3.2 FIFO named like a desktop file — refused at the wrong moment

The pin's `find` (`x:795`, quote Q4) sends its own diagnostics to `/dev/null`, and `-type f` binds to the first
application dir only, so in every later dir a FIFO whose path matches the id pattern is **registered as an entry**.
The pin's debug channel says so on C5: `registered '$ROOT/home/.local/share/applications/./foot.desktop' as entry
'foot.desktop'` (`registration-traces.txt`), and the run still answers `term.desktop`, `rc 0`. The tool raises
before resolving anything (`tools/mado-terminal.py:529`, quote Q6) → `exit 2`.

Blocking is real but conditional: only when the FIFO is the path the resolver *reads* as a candidate. C6 proves the
block rather than slowness — the pin under `strace -f -e trace=openat,read,newfstatat` is killed at 3 s and the last
event is `openat(AT_FDCWD, "$ROOT/home/.local/share/applications/./foot.desktop", O_RDONLY` with no return
(`fifo-block.txt`); the 10 s run also yields `124`. Nothing was written to the FIFO.

In the lowest-preference dir `find -type f` skips it and both sides agree (C7).

### 3.3 Symlink loops — modelled, not a refusal

Four shapes, all agreeing on `rc` and stdout: a loop dir symlink next to a valid entry (C8), a loop symlink *named*
`*.desktop` and listed (C12: pin `rc 1` "No valid terminal entry", tool `rc 1`, and `explain` prints
`verdict=NO_TERMINAL`), a cycle in a subdirectory beside `sub/term.desktop` (C13), and the same trees under the pin's
debug channel. The landing therefore does not need a loop refusal, and the docstring's third added item
("symlink loops") **over-declares**: a shape that agrees is listed as out of contract.

Residual worth freezing rather than refusing: the pin's `find -L` drops a loop path from registration while the tool
registers the path and then refuses to recurse (its `ancestors` inode set, `tools/mado-terminal.py:505-519`). This is
trace-level only in the shapes measured: a `find`-refused loop path is a directory, and both sides skip a directory
when it is read as an entry (`tools/mado-terminal.py:551-552`; pin C12 `rc 1`). It cannot change the printed id,
stdout or exit status — measured, not argued, for C8/C12/C13.

### 3.4 Unreadable inputs — in contract already

An unreadable *entry* is rejected and the next candidate wins (C9) or the run ends `rc 1` with no terminal (C10);
an unreadable *list file* ends the run `rc 1` with `Permission denied` on stderr (C11 — pin `line 361`, tool the same
path text without the `line N` prefix; stderr is not compared). Both sides agree on `rc` and stdout in all three.

## 4. The D1 delta (frozen reference vs landed docstring)

`diff -u .ufo/waves/round-47/l1-draft/mado-terminal.py tools/mado-terminal.py` (frozen reference
`sha256 762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08`, landed
`sha256 b84d5c4f…`):

1. out-of-contract list: draft `:84-85` (`Also out of contract: -h/--help, an empty-string argument (the script loops
   forever)`, quote Q8) → landed `:85-86` adds **HOME unset**, **a FIFO named like a desktop file in a later
   application dir (the script blocks reading it)** and **symlink loops** (quote Q7);
2. `command -v`: draft `:71-73` → landed `:71-74` adds the bash-option rule (`--`, `-p`, `-v`, `-V` clusters succeed;
   any other `-`-prefixed name except `-` fails) — the M47-10 H2 fix, also post-freeze but *toward* the pin.

3. step 4 of the landed *contract prose* (`tools/mado-terminal.py:49-53`) still says
   ``` `find -L <dir>/. -type f` over the application dirs ``` while the landed walk applies `-type f` to the first
   dir only and registers any path type in later dirs (`tools/mado-terminal.py:492-497`) — the docstring contradicts
   the tool it documents (and the pin). Measured: C14, a *directory* named `x.desktop` in the later dir shadows the
   valid file of the same id in the earlier dir, and both sides print nothing with `rc 1` (pin stderr
   `line 985: read: 0: read error: Is a directory`, then "No valid terminal entry"; the landed tool has the matching
   `os.path.isdir` skip at `:551-552`). The same walk rule is what registers the FIFO in C5. This is a second,
   *prose-only* post-freeze delta: the behaviour is right, the sentence about it is the pre-H1 one.

`registration.md` still registers the draft's contract; nothing in the frozen text names any of the three. Measured
mapping: (1a) HOME unset = in contract, `rc 1` only at `:148`/`:166`/`:172`, normal answer when all three XDG vars
are set; (1b) FIFO = in contract when registered but not read (`rc 0`), out of contract only when it would be read
(blocks); (1c) symlink loops = in contract, measured agreeing, so the refusal should be withdrawn; (3) the step-4
sentence must be rewritten to the registered-any-type rule the tool and the pin both follow.

## 5. Draft D1 lesson line (ready to append to `corpus/lessons/round-47.md`, `## Mistakes`)

> **M47-11** · class `reference-drift` · evidence: the landed `tools/mado-terminal.py` (`b84d5c4f…`) widens the
> out-of-contract list of the frozen round-47 reference `l1-draft/mado-terminal.py` (`d7527d60`, `762d042c…`) at
> draft `:84-85` → landed `:85-86` with "HOME unset", "a FIFO named like a desktop file in a later application dir
> (the script blocks reading it)" and "symlink loops", and adds a `command -v` option-word rule (draft `:71-73` →
> landed `:71-74`, the M47-10 H2 fix); `registration.md` still registers the draft's list. Measured against the pin in
> the round-47 counter's sandbox (19 fixtures, 3 identical runs): HOME unset aborts the pin only where a default is
> expanded — `:148` (`XDG_CONFIG_HOME`), `:166` (`XDG_DATA_HOME`), `:172` (`XDG_CACHE_HOME`), pin `rc 1` — and with all
> three set the pin answers normally (`rc 0`) while the tool exits 2, so the tool refuses a selection the resolver
> makes; a FIFO in a later application dir is registered by the pin and answered around (`rc 0`) and only blocks when
> it is the candidate read, while the tool exits 2 at walk time; symlink loops agree on `rc` and stdout in four
> shapes, so the tool refuses an input it models. · captured-by: 48 — `.ufo/waves/round-48/w1/ExecHomeUnset.md`
> (`pin-vs-tool.json`, `registration-traces.txt`, `fifo-block.txt`, `quotes-check.txt` 13/13) · fix: freeze the
> round-48 C1 contract on the measured mapping (section 6 here); narrow the FIFO refusal from walk time to read time
> and model the registered-but-unread FIFO; model HOME unset instead of refusing it; drop the symlink-loop refusal.
>
> **M47-12** (placeholder label only — `ScrD1Line` numbers the step-4 item M47-14 and the FIFO item M47-12; the L1
> lands **one** step-4 line and renumbers) · class `reference-drift` · evidence: the landed contract prose still describes step 4 as
> `find -L <dir>/. -type f` for every application dir (`tools/mado-terminal.py:49-53`) while the walk applies
> `-type f` to the first dir only (`:492-497`), as the pin does (`-type f` at x:766, the per-dir groups at x:768-776); measured, a directory named
> `x.desktop` in a later application dir shadows the valid file of that id in an earlier one and both sides print
> nothing with `rc 1` (C14, pin stderr `read error: Is a directory`), and the same rule registers a FIFO there (C5).
> · captured-by: 48 — `.ufo/waves/round-48/w1/ExecHomeUnset.md` (`pin-vs-tool.json` C14/C5) · fix: rewrite step 4 of
> the contract prose to the registered-any-type rule (the behaviour needs no change).

`ScrD1Line` reached the same three classes independently (their own `Box.run` matrix, their fixtures) and reports the
same step-4 contradiction (`probe6-out.txt`, tree A); their drafting splits it into M47-11..M47-15, so the L1 should
merge rather than append both sets. Agreed final landing set (their numbering, re-verified by them against these
bytes: `receipts/verify-lines.txt` 113/113): **M47-11** the out-of-contract delta (HOME / FIFO / loops), **M47-12**
FIFO, **M47-13** symlink loops, **M47-14** step 4 of the contract prose, **M47-15** the readdir blind spot routed into the round-48 schema-v2 fixtures. My
folded first line does not land beside that set; my second carries the placeholder `M47-12` label for step 4 only so
their cross-seat grep keeps a locator, and both labels above are drafts, not numbers.

## 6. Round-48 contract text (draft for the C1 freeze)

Proposed replacement for the closure's one-liner, in the docstring's voice. `print` and `explain` keep their
round-47 meanings; every clause below is judged on **stdout + exit status only** (stderr and the explain trace are
not compared).

Out of contract, reported as `MADO_TERM_OUT_OF_CONTRACT: <reason>` on stderr with exit 2, shrinks to:

* `-h`/`--help`, an empty-string argument (the script loops forever), XDG dirs or HOME containing `:` inside a
  default, glob characters or a quote, `\u`/`\U` escapes beyond ASCII in a delimiter, file names with bytes the shell
  would see differently in another locale (all unchanged from the frozen round-47 list);
* **a FIFO named like a desktop file that would be read as a candidate** — the resolver blocks in `openat(O_RDONLY)`
  with no bound. The refusal must fire at the read of that candidate, not when the path is discovered. A FIFO in the
  lowest-preference application dir is *skipped by `find -type f`* (in contract, no refusal); a FIFO in a later dir
  that is never read as a candidate is *registered as an entry id* and the run answers normally (in contract, no
  refusal: pin `rc 0`, C5).

In contract, modelled like the pin (each was measured; the current tool diverges where noted):

| input | pin behaviour | round-48 requirement |
|---|---|---|
| `HOME` unset, `XDG_CONFIG_HOME`/`XDG_DATA_HOME`/`XDG_CACHE_HOME` all non-empty | never reads `HOME`; normal answer (`rc 0`, C2/C2b) | model it; **do not refuse** (current: exit 2) |
| `HOME` unset, any of those three empty | aborts at `:148`/`:166`/`:172` in that order, `rc 1`, stdout empty | `print` reproduces `rc 1` + empty stdout and says so in `explain`; stderr text not compared |
| `HOME=""` (empty) | defaults become `/.config`, `/.local/share`, `/.cache` | as now (agrees: C4, C4b) |
| unreadable entry | rejected, next candidate wins, or `rc 1` no terminal | as now (agrees: C9, C10) |
| unreadable list file | `rc 1`, `Permission denied` on stderr | as now (agrees: C11) |
| symlink loop of any shape | traversal drops the loop path (`find` diagnostics go to `/dev/null`, x:795); entry ids as if the loop were absent | **withdraw the refusal**; stdout+rc as now (agrees: C8, C12, C13). Residual: the loop path itself is registered by the tool and dropped by the pin — a find-refused loop path is a directory and both sides skip a directory as an entry, so the printed result cannot differ |

Warm-cache semantics stay C1's own section (not this seat's): `explain`'s `cache=` field keeps meaning what the
round-47 text says, extended by the warm-cache move.

## 7. Limits, risks, blockers

* The FIFO fixture is bounded as instructed: `mkfifo` only, nothing ever written into it, the pin capped at 10 s
  (and the block re-proved at 3 s under strace), `124` recorded as "would block". A `124` is not a verdict about
  what the pin would print after a write — nothing may write, so that half stays unobservable and out of contract.
* `HOME=""` with the *default* paths is only exercised where nothing exists at `/.config` / `/.local/share`: the
  sandbox root is bwrap's tmpfs and cannot be pre-populated, so an empty-HOME tree at `/` is not tested. Both sides
  build the same three path strings from the same rule, and C4b agrees.
* Reconciliation of the closure's sentence (`round-47-verifier-spotcheck.md:46-47`, quote Q9) is stated as a
  narrowing, not a refutation: its sub-case (HOME unset *and* XDG dirs unset) reproduces exactly (`rc 1`).
* Not compared: stderr text, the `explain` trace, `--print-content` (not exercised — none of these refusals touch
  it), readdir order (this seat's trees have one candidate per dir except C9, where the extra entry is unreadable
  and never listed).
* **Trap named by `ScrD1Line` and avoided here**: this session exports `XDG_CONFIG_HOME`/`XDG_DATA_HOME`/
  `XDG_CACHE_HOME`, so a *host* probe with only `env -u HOME` removes nothing the pin needs and the pin answers from
  the host tree; such a probe does not show the `:148`/`:166`/`:172` abort. Every number in this report comes from
  `--clearenv` + explicit `--setenv`, so "HOME unset" here means absent from the sandbox environment.
* Nothing frozen here; the L1 freezes the predicates after `w1`. This seat wrote only
  `.ufo/waves/round-48/w1/ExecHomeUnset/` and this report.
* Tooling: none installed or upgraded (bwrap, strace, python3.14, git pre-existing); no pacman transaction, no host
  service touched, scratch under `/fast/scratch/hyaku/mado-r48/ExecHomeUnset` and deleted at the end.

## 8. Receipts (all under `.ufo/waves/round-48/w1/ExecHomeUnset/`)

| file | content |
|---|---|
| `run.py` | the driver (imports the round-47 C1 counter's `Box`; 19 fixtures) |
| `pin-vs-tool.json` | final per-fixture record (19 fixtures): args, env shape, pin and tool `rc`/`stdout`/`stderr`(normalised), `trips`, `agree` — includes C14 |
| `run.log` | stdout of the final run (pin and tool sha256 on the first two lines) |
| `determinism-run{1,2,3}.json` | three full runs; identical `rc`/`stdout`/`agree` |
| `probe-fifo.py`, `fifo-block.txt` | strace of the pinned resolver blocked in `openat` on the FIFO (rc 124 at 3 s) |
| `probe-registration.py`, `registration-traces.txt` | pin `XTE_DEBUG=1` registration lines vs tool `explain` for C5/C8/C12/C13 |
| `quotes.json`, `check-quotes.py`, `quotes-check.txt` | the 13 quotes used here, each located and word-capped, `QUOTES: 13/13 ok` |
