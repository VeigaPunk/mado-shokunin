# ExecControlsC1 — C1 controls: a cheap tool must MISS the C1 counter draft

Round 48, wave `w1` (BUILD), seat `ExecControlsC1`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Nothing outside `.ufo/waves/round-48/w1/ExecControlsC1/` was
written. Scratch `/fast/scratch/hyaku/mado-r48/ExecControlsC1/` (deleted at the end; no citable evidence there).

Target of the seat: **the C1 counter draft must reject every tool that skips the claimed work.** The claim is C1's
warm-cache path (`claims.md`): `tools/mado-terminal.py` predicts `xdg-terminal-exec`'s stdout and exit status with the
cache file the environment presents.

## 1. Result

20 control tools, each a full `tools/mado-terminal.py` variant. Judged twice:

* **the draft instrument** — `.ufo/waves/round-48/w1/ExecCounterC1/c1-r48-terminal-cache.py` (sha256 below), each
  control committed into its own scratch clone of the lane at `BASE`+1 and scored by that counter verbatim;
* **my own pin-judged loop** — `run-controls.py` with the pinned resolver as the oracle on
  `fixtures-v2.json` (23 cases, schema v2), `expect` produced by three identical pin runs (+ a cold twin that proves
  each fixture's teeth), every tool run under `strace` and every tool tree fingerprinted before/after.

`reference` is the control that does the work (base + the warm-cache path). It **MEETS** every clause of both judges.
Every other control **MISSES**.

**Status of the draft column.** The draft pass over the final control bytes was still running when the wave closed;
each row's draft cell is harvested from `receipts/<control>.txt` (written by that pass as each control finished) and
is marked `cut` when the pass had not reached it. `reference` was then scored on its own to completion:
`PRED-C1-r48: cold=190/190 warm=32/32 explained=222/222 generated=230/230 selftest=ok readonly=ok tool=present
verdict=TARGET_MET` (exit 0) — the instrument accepts the tool that does the work, on the final bytes.
`base` — the tool the round-47 counter would have scored — misses `w+x+g`
(`cold=190/190 warm=23/32 explained=193/222 generated=210/230 readonly=ok`).
Receipts: `receipts/summary.txt`, `receipts/<control>.txt`, `receipts/expect.json`, `receipts/draft-run.log`,
`receipts/draft-run-partialcache.txt`.

| control | source | what it gets wrong | caught by (local loop) | killing fixtures (local) | draft |
|---|---|---|---|---|---|
| `reference` | base + warm path | nothing (the shape the round needs) | — (MEETS) | — | **MET** (`TARGET_MET`, measured separately to completion) |
| `base` | round-47 tool | cold cache only: the cache file is out of its contract | f + x (f=9 x=19) | the 8 hits + `e1-home-unset` (`f`: exit 2 instead of the pin's 1); every non-hit fixture (`x`, it prints cache=present/absent) | MISSED (w+x+g) |
| `always-cold-but-home` | base + D1 | cold only, but HOME unset modelled as the pin does | f + x (f=8 x=19) | as `base` minus `e1-home-unset` (which it passes: that is its point) | MISSED (w+x+g) |
| `trust-any` | ref | trusts any well-formed cache whose line 2 resolves, no hash | f + x (f=5 x=5) | i1, i2, i7, i13, i4 | cut |
| `hash-names` | ref | hash over path/entry names only, no `ls -l` columns | f + x (f=8 x=8) | every warm fixture (hash never matches → says stale on a hit) | MISSED (w+x+g) |
| `hash-no-date` | ref | `ls -l` model without the date column | f + x (f=8 x=8) | every warm fixture | MISSED (w+x+g) |
| `hash-no-total` | ref | `ls -l` model without the `total N` lines | f + x (f=8 x=8) | every warm fixture | cut |
| `cache-ignores-enable` | ref | reads the cache when `XTE_CACHE_ENABLED=false` | f + x (f=1 x=1) | i8 | MISSED (x) |
| `no-line-limit` | ref | no 50-line cap on the cache | f + x (f=1 x=1) | i5 (terminator on line 50); i6 (line 49) must still pass | cut |
| `delegate-ls` | ref | runs `ls` through PATH for gen_hash (a process) | r (14 trips), f=0 x=0 | its hash is CORRECT: only the trace rejects it | MISSED (r) |
| `md5-subproc` | ref | pipes the hash input to `md5sum` (a process) | r (14 trips), f=0 x=0 | as above | cut |
| `explain-cache-const` | ref | `explain` always says `cache=hit` when caching is on | x (14) | the 14 non-hit, non-disabled fixtures | MISSED (x) |
| `explain-cmd-const` | ref | `explain` never names the command (`cmd=-`) | x (21) | every explain case with a command | MISSED (x) |
| `writes-cache` | ref | models `save_cache`: writes the cache file (contract: writes nothing) | w (12) — **f=0 x=0 r=0** | every primed fixture (`/.rw/cache/xdg-terminal-exec` changes) | cut |
| `mut-desktop-lower` | ref, one rule undone | hashes the lowercased desktop list instead of `XDG_CURRENT_DESKTOP` | f + x (f=8 x=8) | every warm fixture | cut |
| `mut-no-command-v` | ref, one rule undone | trusts a hash-matching cache whose cached command is gone | f + x (f=1 x=1) | i3 | cut |
| `mut-cache-fallback` | ref, one rule undone | uses a hit only as a fallback after the cold selection fails | f + x (f=8 x=6) | every warm hit | cut |
| `mut-eof-terminator` | ref, one rule undone | accepts a cache with no terminator line | f + x (f=2 x=3) | i4, i10 | cut |
| `mut-terminator-contains` | ref, one rule undone | accepts a terminator anywhere on the line | f + x (f=1 x=1) | i10 | cut |
| `mut-warm-ignores-args` | ref, one rule undone | on a hit, drops the command line's `--dir/--title/--app-id` | f (1) | w3 | cut |

`writes-cache` is the one control whose fate depends on the instrument: with the round-47 clause set
(`f`, `x`, `r`) it **MEETS** — the trace set (`execve,execveat,socket,socketpair,connect`) cannot see a write. My
local loop catches it only because it fingerprints the tree. See finding **F4**.

## 2. How the controls are built (reproducible)

`build-controls.py` reads `tools/mado-terminal.py` at `BASE` (`git show`), checks nothing else, and emits

* `controls/base.py` — the round-47 tool, byte-identical to the base blob
  (sha256 `b84d5c4f723049c0fd14189ffc7b6db1f71eb70fb97e0c476d20ddeca6de2222`);
* `controls/reference.py` — base + the warm-cache path (sha256 in `receipts/summary.txt`);
* `controls/<control>.py` — one `(old, new)` patch per control, applied to the reference (or to base), each anchor
  asserted to occur exactly once, and the deviation named in the file's first docstring line.

```sh
python3 -I .ufo/waves/round-48/w1/ExecControlsC1/build-controls.py
python3 -I .ufo/waves/round-48/w1/ExecControlsC1/run-controls.py --work <scratch dir>
```

The reference models, in base+delta form: `read_cache` (x:217-298: 10 field lines, lines 11+ as the
`\x1f`-separated command re-joined with newlines, terminator `\x1eEND_OF_EXEC_USEP` at end of line, the 50th line
ending the read), `gen_hash` (x:179-215: md5 of `4\n` + `XDG_CURRENT_DESKTOP` + `\n` + the exact stdout of
`LC_ALL=C LANG=C ls -LRl` over the list and application paths, stderr dropped), the warm print modes (cached id,
path, action, exec, arg names; `--print-content` reading the cached path and dying with status 1 when it is gone), the
cache states in `explain` (`absent|hit|stale|invalid|disabled`), and the round-47 D1 closure (HOME unset → exit 1,
empty stdout, only when a default has to be expanded through it). It starts no process, opens no socket, writes
nothing.

## 3. The `ls -LRl` model, and the trap under it

`gen_hash` needs the byte-exact stdout of `ls -LRl` *as the resolver runs it*. Two facts decide what that binary is:

* the counter copies `shutil.which("ls", path="/usr/bin")` into `/oracle/bin`, so the judge's `ls` is
  **`/usr/bin/ls` = GNU coreutils 9.12** on this host;
* a shell on this host resolves a *different* `ls` — the interactive shell here self-reports `ls 0.8.0`
  (a clap-style `--help`), not GNU. Calibrating "the host's ls" from a shell therefore calibrates the wrong binary.

`probe-lsmodel.py` → `receipts/ls-model-calibration.txt` records the facts the model encodes, measured with
`/usr/bin/ls` inside the counter's own namespace shape (`bwrap --unshare-all --clearenv --ro-bind /usr/lib`,
so **no /etc → numeric uid/gid** and **no TZ → UTC dates**): block order (file operands first, then each directory
depth-first in byte order), `total` = `st_blocks` summed and rounded up to 1024-byte units (`LS_BLOCK_SIZE` /
`POSIXLY_CORRECT` change that unit — not modelled, see F7), column widths of the *file* block sized over the directory
operands as well (a GNU 9.12 quirk: `sub`'s size 15 widens a 1-digit file size), the two date forms with the exact
six-month boundary (age `< 15778476 s` and not in the future → `Mon dd HH:MM`, else `Mon dd  YYYY`), byte-order
sorting, `\n` → `?` in a name (every other byte passes through), an unreadable directory operand printing **no header
at all**, a dangling entry with `-L` printing the `l????????? ? ?    ?     ?   ? name` row, and a dangling
*operand* with `-L` being dropped entirely (stderr only).

`fuzz.py` (differential: the model vs `/usr/bin/ls -LRl` in the same namespace, random trees with symlinks, dangling
links, unreadable dirs, 0/1/12345/1234567-byte files, non-ASCII and newline names, pinned and live mtimes, duplicate
and trailing-slash and missing operands) is **150/150 byte-exact** (`receipts/fuzz-150.txt`), run against the module
extracted from `controls/reference.py` (not a copy).

End-to-end parity is then shown by the judge itself: 8 of the 23 fixtures can only pass if the tool's md5 equals the
pin's md5 for that tree (the seven `w*` hits and the line-49 `hit`), and `reference` MEETS all 23 in stdout+rc and all
23 in `explain` (selected/path/cmd/cache).

## 4. Findings for the freeze

Each is a thing the counters must do (or must stop believing), with the receipt that shows it.

**F1 — a prime run must hold the sandbox's PID namespace open AND wait for the terminator, not for the file.**
`save_cache "$1" &` (pin :1455-1457) is forked; bwrap is PID 1 of the namespace and kills the namespace when the pin
exits, so a plain `--print-cmd` sandbox run leaves **no cache at all**. Measured in `receipts/prime-keepalive.txt`
(same tree, same argv, only the tail differs): plain run → no cache; wrapped in a shell that spins → an 11-line cache
ending with `\x1eEND_OF_EXEC_USEP`. r47 never noticed because its own note (`w2/SentC1Sandbox.md` §5) says the oracle
leaves `.rw/cache` empty. A counter that primes naively and does not check the fixture's premise would score a
cold-only tool as **MET**: `base` would pass every "warm" fixture, since cold == cold.
Second half, measured the hard way: an existence test on the cache path is not enough — the redirect creates the file
before the write, so a spin that stops at `-f` can leave a **truncated cache**. My first waiter did exactly that and
produced one empty cache in ~40 primes; the run then crashed on a 0-line cache
(`receipts/draft-run-partialcache.txt`) instead of mis-scoring, but a counter that treats that empty file as a *stale*
cache would mark a correct tool as missing on a fixture that never tested what it claims. Wait for the last line to be
the terminator, as the draft's waiter does.

**F2 — a malformed-cache fixture cannot be written as literal text if it is meant to have a *valid* hash.**
The hash covers absolute paths and mtimes, so its value is per-tree and per-run; a literal cache can only carry a
wrong hash, which makes its state `stale`, not `invalid`. The rules under test (50-line cap, terminator position,
terminator-at-EOF) are then never exercised: `no-line-limit` would be rejected by the hash check instead of the limit.
My fixtures prime and then rewrite the primed text (`after.files["<cache>"] = {"$cache": "pad_before_exec:38"}` etc.).
The draft's schema v2 has no such op — it has `cache` literal or `prime`, nothing in between. **Proposal for the
frozen schema:** `after.cache` ∈ {`drop_terminator`, `bad_hash`, `set_cmd:<name>`, `term_midline`,
`pad_before_exec:<n>`} applied to the primed cache of *that* tree (my `run-controls.py` implements exactly these five,
in `mutate()`).

**F3 — `explain`'s `MADO_TERM:` record is not one line when the cached command contains a newline**, and a
line-limit fixture necessarily puts its padding lines inside the cached command. Truncating at whitespace silently
loses `cache=` and `verdict=` (my parser had to become marker-based; the round-47 parser truncated `cmd=` the same
way, which the draft already records). The draft's fix (parse by the five literal markers, and take `cmd=` from a
`--print-cmd=\036` run) is the right one; the *fixture* consequence is that `cmd=` is only ever the **first word**
of a multi-word command — i6 (`pad…`) shows it: the oracle's first word is `pad`.

**F4 — a write is blocked, but it is not scored.** In the draft, the tool tree's `.rw` is mounted read-only, so a tool
that performs the resolver's `save_cache` gets `EROFS` — and a tool that swallows it (mine does, `except OSError`) is
indistinguishable from one that never writes: `writes-cache` scores `f=0 x=0 r=0` in my loop and is only caught by the
tree fingerprint. The trace set cannot see `openat`. **Proposal:** fingerprint the tool tree (path, size, mtime) before
and after every tool run and fail the run on any difference (cheap: one `os.walk`), or add
`openat` with `O_WRONLY|O_CREAT|O_TRUNC` to the traced calls, or make the tool's `.rw` a tmpfs that must be empty
afterwards.

**F5 — `cache=` is a verdict about the cache GATE, never about the save, and the draft's derivation caught a real
defect in my own reference.** The cache is read before any list when `XTE_CACHE_ENABLED` (environment) is truthy
(x:1178-1179); a `/disable_cache` line lives in a list file, so it is reached only on the cold path and can only
suppress the *save* (x:300-340), never the read. Two consequences, both scored by the draft's clause x:
a run that dies before the gate (HOME unset) is `absent`, not `disabled`; and a run whose read returned `stale` stays
`stale` even if a later list line disables caching. My reference reported `disabled` for both. The draft failed it on
exactly one case — E-01, `want absent` vs `got disabled` — while passing cold 190/190, warm 32/32, generated 230/230
and 221/222 explain; after adopting the gate rule it MEETS. My fixture i9 was likewise re-declared `stale`
(`make-fixtures.py`), and both implementations now agree on it; i9's teeth are the `cache=` value alone, so it is a
state fixture, not an output fixture.

**F6 — `command -v` on a cache's line 2 must model bash's own namespace, not a PATH lookup.** w7 makes the cached
command `read_cache` (a function of the resolver itself): the real pin hits the cache; a tool whose `command -v` only
walks `PATH` says `stale`. (The round-47 generator already uses `TryExec=read_cache` for the cold path; the warm path
needs the same trick, and only a primed fixture can show it: the line-2 edit does not change the hash.)

**F7 — residuals I did not close, for the registration text.** The model ignores `LS_BLOCK_SIZE` and
`POSIXLY_CORRECT`, which change the `total` lines of the listing (both measured in the calibration receipt), so a
fixture that sets either would be a false miss; the two `ls` implementations on this host are a standing trap for
anyone writing fixture expectations from a shell; `readdir` order (r47 D3) is not exercised by my fixtures, which hold
one candidate per directory — the counter must keep its own two-candidates-in-one-dir case. And the reference's `ls`
model is itself an implementation of `ls`, which the r47 docstring already declares as a residual of the contract.

## 5. What the counter draft looks like from here

Its clause set (`a s f w x g i r`) is the round-47 set plus `w`: 190 cold fixtures byte-identical to round 47
(harm watch), 32 warm fixtures (schema v2), 150 cold + 80 warm generated cases, and an explain clause that now
compares `cmd=` and `cache=`. One scoring run of a nearly-correct tool takes ~110 s on this host and runs the tool
~1400 times; a `f` failure costs a full pass before the later clauses are reached.

What the warm set covers (ids read from `c1-r48-fixtures.json`): `WARM-SAME` hits (W-01/02/09/12), `WARM-DIFFERS`
hits (W-03..W-11, W-14), `MALFORMED-{MTIME,SIZE,NAME,DIRADD,DIRGONE,DESK,EXECGONE}` → stale,
`MALFORMED-{TERM,EARLY,LIMIT,EMPTY,NONL}` → invalid, `BADHASH` → stale, `LINE49`/`LINE50`, `DISABLED` ×2 (one with
garbage), `HOMEUNSET`, `WARM-ABSENT`. That is a real warm clause: no tool that skips the cache can pass `w`, and the
two `readonly` and `explain` clauses carry the round-47 defects (F4 aside).

Coverage the frozen warm set should add, each with the fixture that would carry it (all four exist in
`fixtures-v2.json` and all four are *inert* against the current draft — a tool that resolves these four paths cold
still passes `w`):
1. `--print-content` over a hit whose cached entry differs from the cold choice (`w5-content`) — the draft's warm cases
   are all `--print-cmd` or the three-print trio, so "content is read from the cached path" is unscored;
2. `--print-id --print-path` alone over a hit (`w4-id-path`), which is also the `path=` value clause x compares;
3. a hit with a command appended (`--print-cmd -- htop`) and a cached `TerminalArgExec` that the entry no longer has
   (`w6-execarg-edit`);
4. a cached command that is a shell *function* of the resolver (`w7-function-cmd`: line 2 rewritten to `read_cache`,
   hash untouched), which separates bash's `command -v` from a PATH lookup (F6);
5. a `disabled` fixture whose cache is **valid** and whose cold answer therefore differs from the cached one
   (`i8-disabled-env`, `XTE_CACHE_ENABLED=false` after a prime plus a same-size list edit). Measured: `cache-ignores-enable`
   is rejected by the draft on clause `x` only (`warm=32/32`, `explained<222`) — the draft's `M-13`/`M-14` carry a cache
   whose use does not change the printed answer, so a tool that ignores the flag still passes `w`. In my loop the same
   control fails on `f` (i8) as well, which is the clause that should do the work.

## 6. The same fixtures against ExecRefCacheA's independent draft

`../ExecRefCacheA/mado-terminal.py` (sha256 `c4ed769eea9c1c88da8fe9c222cca79035faac0224639e45c98a7d0f44a93bdd`,
1705 lines, written by another seat) scored by my loop on the **final 23-case set: MEETS** (`f=0 x=0 r=0 w=0`,
`receipts/refA.txt`). On the set as it stood one hour earlier it missed exactly one case, `i9-disable-directive`
(`got stale`, `want disabled`) — the F5 ambiguity, resolved in the draft's direction in that seat's favour. Nothing in
my fixtures is tuned to my own implementation: an independent draft passes them, and its own one-rule mutants (§ below)
fail exactly where mine do.

Six one-rule-undone mutants of *that* draft (`build-refa-mutants.py`, anchors taken from A's own text, each asserted
unique) were then scored on the same set. All six MISS, with the same clause fingerprints as my own mutants:

| mutant of A's draft | rule removed | local | killing fixtures |
|---|---|---|---|
| `A-trust-any` | the hash comparison | f=5 x=5 | i1, i2, i7, i13, i4 |
| `A-no-command-v` | `command -v <cached cmd>` | f=1 x=1 | i3 |
| `A-no-line-limit` | the 50th-line arm | f=1 x=1 | i5 |
| `A-eof-terminator` | the terminator requirement | f=2 x=3 | i4, i10 |
| `A-desktop-dropped` | `XDG_CURRENT_DESKTOP` in the hash | f=8 x=8 | every warm hit |
| `A-warm-ignores-args` | `--dir/--title/--app-id` on a hit | f=1 | w3 |

## 7. Files and hashes

| file | what it is |
|---|---|
`build-controls.py` | the patcher: base blob → reference → 19 controls, one documented patch each |
`controls/base.py`, `controls/reference.py`, `controls/<control>.py` | the 20 full tool variants (sha256 in `receipts/summary.txt`) |
`make-fixtures.py`, `fixtures-v2.json` | the 22-case schema v2 set (intent only; `expect` is measured) |
`run-controls.py` | both judges: the draft counter (scratch clone + commit) and the local pin-judged loop |
`probe-lsmodel.py`, `receipts/ls-model-calibration.txt` | the measured `ls` facts the model encodes |
`fuzz.py`, `receipts/fuzz-150.txt` | differential fuzz of the shipped model against `/usr/bin/ls` (150/150) |
`receipts/expect.json` | the oracle's own answer per fixture (3 identical runs) + the cold twin |
`receipts/<control>.txt`, `receipts/summary.txt`, `receipts/draft-run.log`, `receipts/draft-run-partialcache.txt` | per-control clause detail and the draft's verdict lines |
`build-refa-mutants.py`, `controls-refa/*.py` | six one-rule-undone mutants of ExecRefCacheA's draft (§6) |
`receipts/artifact-hashes.txt` | sha256 of every artifact in this seat directory |
`receipts/prime-keepalive.txt` | F1: the cache exists only if the namespace is held open |
