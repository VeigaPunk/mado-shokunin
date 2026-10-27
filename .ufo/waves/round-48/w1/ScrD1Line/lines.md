# ScrD1Line — routed D1/D3: the post-freeze contract delta lines and the readdir blind-spot line

Target: append to `corpus/lessons/round-47.md` `## Mistakes`, after **M47-10** (`corpus/lessons/round-47.md:205`); ids
continue at M47-11. (The L1 may instead anchor the block in the round-48 entry's `## Mistakes`; the ids then become M48-*.
The L1 decides — nothing below depends on the anchor.)

Sources diffed, with both blobs named (no working-tree guess):

| side | path | revision | blob sha256 |
|---|---|---|---|
| frozen | `.ufo/waves/round-47/l1-draft/mado-terminal.py` | `d7527d60` (registration C1 reference) = base `579f694b` | `762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08` |
| landed | `tools/mado-terminal.py` | base `579f694b` | `b84d5c4f723049c0fd14189ffc7b6db1f71eb70fb97e0c476d20ddeca6de2222` |

The module docstring differs in **exactly two hunks** (86 → 87 lines; `difflib` opcodes in `verify-lines.py`): the step-5
`command -v` sentence and the out-of-contract list. The first is already recorded as **M47-10**
(`corpus/lessons/round-47.md:205`, `w2/ExecC1Diff.md` H1/H2), so it gets no new line. The second hunk adds three
out-of-contract items (M47-11..M47-13). A fourth post-freeze delta left **no docstring hunk** — the code was fixed (H1) and
step 4 of the docstring was not — and is drafted as M47-14.

Measurement discipline for this plane: the *session* environment exports `XDG_CONFIG_HOME`, `XDG_DATA_HOME` and
`XDG_CACHE_HOME`, so `env -u HOME` alone removes **nothing that the pin needs** and the pin answers normally
(`receipts/receipt-ambient-xdg.txt`). A host probe that keeps the ambient environment therefore cannot measure the pin's
HOME failure; the matrix below was taken inside the C1 counter's own `bwrap` sandbox (`--clearenv`, explicit env) and
cross-checked with `env -i` on the host. `receipts/probe3-out.txt` is kept only to show the trap and is **not** cited as
evidence.

---

## M47-11

**M47-11** · class `contract-drift` · evidence: the landed docstring adds "HOME unset" to the out-of-contract list
(`tools/mado-terminal.py:85`: "Also out of contract: -h/--help, HOME unset, a FIFO named like a desktop file in a") where the
frozen reference lists only "-h/--help, an empty-string argument" (`.ufo/waves/round-47/l1-draft/mado-terminal.py:84`:
"Also out of contract: -h/--help, an empty-string"). The refusal itself predates the freeze — the same
`raise OutOfContract("HOME unset")` sits at `.ufo/waves/round-47/l1-draft/mado-terminal.py:407` and at
`tools/mado-terminal.py:410` — so the delta is in the contract *text*, not in the code. Measured, and this is where the
round-47 closure reads the pin wrong: the pin dies on an absent HOME **only where an `XDG_*` default is actually expanded**
— `/usr/bin/xdg-terminal-exec:148` (`XDG_CONFIG_HOME`), `:166` (`XDG_DATA_HOME`), `:172` (`XDG_CACHE_HOME`), under
`set -euf` (`/usr/bin/xdg-terminal-exec:23`), each printing `HOME: unbound variable`, `rc 1`, empty stdout. With all three
set the pin never mentions HOME and answers `rc 0` with the entry id while the tool exits 2
(`receipts/probe5-out.txt`: `pin rc=0 out='term.desktop\n' | tool rc=2 out=''`; `receipts/probe4-out.txt` reproduces it
inside the counter's sandbox). The fatal sub-case is **three** isolated sites, one per default: `XDG_CONFIG_HOME` empty → `x:148`,
`XDG_DATA_HOME` empty → `x:166`, `XDG_CACHE_HOME` empty → `x:172`, each `rc 1`, empty stdout — measured here in the
all-absent row (`pin rc=1 out='' | tool rc=2 out=''`, `receipts/probe5-out.txt`) and site by site by peer seat
`w1/ExecHomeUnset.md` C3/C3b/C3c, whose fixtures are `--clearenv` + explicit `--setenv` and so do not fall into the
ambient-XDG trap below. On the host `env -i /usr/bin/xdg-terminal-exec --print-id` reads
`line 148: HOME: unbound variable`, `rc=1` (`receipts/receipt-home-unset-host.txt`). So the round-47 sentence "pin exit 1,
empty stdout" is the defaults-needed sub-case only, and the tool refuses a selection the resolver makes in the all-set case.
· captured-by: none — the frozen contract's own text was the only predicate, and no fixture exercises it
(`quality/counters/c1-r47-fixtures.json`: 190 cases, 0 with `HOME` in `env`; `case_env` at
`quality/counters/c1-r47-terminal.py:222` always injects `HOME`). · fix: register the exclusion **with its condition** in the
round-48 C1 freeze — either model HOME absent as the pin does (refuse only where a default must expand it, i.e.
`XDG_CACHE_HOME` / `XDG_CONFIG_HOME` / `XDG_DATA_HOME` unset) or keep the unconditional exit 2 and state the divergence it
accepts (pin `rc 0` + id, tool `rc 2`). A schema-v2 fixture that leaves HOME absent **with all `XDG_*` set** must not be
frozen with an exit-1 expectation; with `XDG_CACHE_HOME` also absent the exit-1 row is available and the two refusals differ
only in status (`1` vs `2`), so the fixture must expect the divergence, not equality.

## M47-12

**M47-12** · class `contract-drift` · evidence: the landed docstring adds "a FIFO named like a desktop file in a later
application dir (the script blocks reading it)" (`tools/mado-terminal.py:85-86`); the frozen reference has no such item
(`.ufo/waves/round-47/l1-draft/mado-terminal.py:84-85`) and its walk skipped every non-regular path
(`.ufo/waves/round-47/l1-draft/mado-terminal.py:519`: "if not stat.S_ISREG(cst.st_mode):"). The landed walk instead raises
at **walk time**, for any id-shaped FIFO in a dir walked after the first (`tools/mado-terminal.py:526-529`), which is
broader than the script: the resolver *registers* such a FIFO as a candidate and blocks only if it actually reads it. Two
measurements pin this down. (a) FIFO `pipe.desktop` in the later-walked dir, no list file, so the FIFO is the first
fallback candidate: pin blocks, killed at `timeout 5`, `rc 124`; tool `rc 2` with
`MADO_TERM_OUT_OF_CONTRACT: a FIFO named like a desktop file (the resolver blocks reading it)`
(`receipts/probe2-out.txt` case B). (b) The same FIFO with a list file naming the valid `term.desktop`: pin answers
`rc 0` and prints `term.desktop` — the FIFO is never read — while the tool still exits `2`
(`receipts/probe7-out.txt`). The same FIFO in the **first**-walked dir is skipped by both sides and the valid entry is
selected, `rc 0` (`receipts/probe6-out.txt` tree B) — peer seat `w1/ExecHomeUnset.md` reports the same shape (a FIFO in
the lowest-preference `XDG_DATA_DIRS` entry, pin `x:766` single `find -type f`) — so the docstring's "later application
dir" scoping is right about the registration and wrong about the refusal. The peer's blocking receipt is a strace
open on the FIFO with no return, killed at 3 s, which is the same event my `rc 124` under `timeout 5` observes. Corroborated independently: `w1/ExecHomeUnset.md` (peer seat, same round) reports
the pin registering the FIFO ("registered … as entry") and answering `rc 0` when it is not the candidate read. ·
captured-by: none. · fix: register the item in the round-48 freeze as a **hang** exclusion with its condition — a FIFO that
becomes the candidate read — and either narrow the tool's raise to that condition or record the over-refusal (pin `rc 0`,
tool `rc 2`) as accepted. A v2 fixture cannot express "the pin blocks" as an `expect` (a timeout is `rc 124`, no stdout), so
the predicate must be the documented refusal, never pin-vs-tool equality.

## M47-13

**M47-13** · class `unsupported-exclusion` · evidence: the landed docstring adds "symlink loops" (`tools/mado-terminal.py:86`)
to a list whose closing sentence promises "On these the tool prints `MADO_TERM_OUT_OF_CONTRACT: <reason>` on stderr and exits
2." (`tools/mado-terminal.py:88`) — but no code path raises for a loop. The walk prunes a repeated `(st_dev, st_ino)` and
returns an ordinary answer (`tools/mado-terminal.py:512-514`: "if key in ancestors:", unchanged from
`.ufo/waves/round-47/l1-draft/mado-terminal.py:503`). Measured on three loop shapes in the first-walked application dir, a
self-loop (`self -> .`), an ancestor loop (`up -> ..`) and an entry reachable only through a looped subdir: tool and pin agree
on `rc` and stdout every time (`term.desktop` / `rc 0`; `sub-deep.desktop` / `rc 0`), no `OUT_OF_CONTRACT` on stderr
(`receipts/probe2-out.txt` cases C, C3). So the item is (a) not a refusal and (b) not a divergence on any shape built.
Corroborated independently: `w1/ExecHomeUnset.md` (peer seat) reports 4 loop shapes agreeing, and names the only
trace-level residual — `find -L` drops a loop path from *registration* while the tool registers it and then refuses to
recurse; a find-refused loop path is a directory, and both sides skip a directory when it is read as an entry
(`tools/mado-terminal.py:551-552`, pin `line 985: read: 0: read error: Is a directory`), so no printed id, stdout or
status can differ in the shapes measured. ·
captured-by: none, and no fixture can reach it — 0 of the 190 cases use a symlink (`quality/counters/c1-r47-fixtures.json`,
scan in `verify-lines.py`). · fix: delete the item from the out-of-contract list (the ancestor prune **is** the model, and it
is the same rule `find -L` applies), or replace it with the shape that really diverges. Do not freeze an exit-2 predicate
for a loop: a v2 fixture carrying one would be a `TARGET_MISSED` the tool cannot fix without a raise the pin does not
justify.

## M47-14

**M47-14** · class `contract-drift` · evidence: the H1 fix changed the walk and not step 4 of the docstring. Step 4 still
reads "`find -L <dir>/. -type f` over the application dirs in ascending preference" and "a path counts when its part after
`<dir>/./` starts with [a-zA-Z0-9_], ends in `.desktop`" (`tools/mado-terminal.py:49-52`, byte-identical to the frozen
`.ufo/waves/round-47/l1-draft/mado-terminal.py:49-52`), i.e. it describes the pre-H1 model in which only regular files
count in every dir. The landed walk knows better and says so only in a code comment — "`-type f` binds to the first group"
(`tools/mado-terminal.py:494-495`) — and registers **any** path type in every dir after the first
(`tools/mado-terminal.py:535`: "elif self._id_ok(rel):"). Measured difference: `x.desktop` a regular entry in the
first-walked dir and a **directory** in the later one → tool prints nothing, `rc 1`, and its explain line reads
"is shadowed by … (the later application dir wins)"; pin prints nothing, `rc 1` (`read error: Is a directory`)
(`receipts/probe6-out.txt` tree A). Read literally, the docstring predicts the earlier regular file wins — it does not. ·
captured-by: M47-10 recorded the *reference* drift and the code fix; the landed contract text was not re-read against the
landed code. · fix: amend step 4 in the round-48 freeze to state the first-dir-only `-type f` binding and the any-type
registration in later dirs (the code comment is already the right sentence), so the frozen predicate matches the pin. Until
then a w2 seat can quote the docstring to contradict the tool on a directory- or `/dev/null`-symlink shadow.
**Numbering collision, resolved on the peer side:** peer seat `w1/ExecHomeUnset.md` section 5 drafted the same finding
as its own `**M47-12**`; it has since relabelled that line "placeholder label only — `ScrD1Line` numbers the step-4
item M47-14 and the FIFO item M47-12" and asks the L1 to land one step-4 line and renumber rather than append both
sets. So the labels to land are: M47-11 out-of-contract delta (HOME / FIFO / loops), M47-12 FIFO, M47-13 loops,
M47-14 step 4, M47-15 readdir routing; the peer's first line folds the three HOME/FIFO/loop deltas into one and does
not need to land beside this block.

---

## D3 routing line

**M47-15** · class `blind-spot` · evidence: the C1 counter's frozen fixtures are blind to the readdir axis
(`.ufo/waves/round-47/w2/ExecC1Determinism.md:10`: "the frozen fixture set — clause f/x are blind to the readdir axis"),
and this defect was never routed in the round-47 report or lesson. A walk that sorts directory entries scores 190/190
fixtures and 190/190 explain checks and is caught only by a nonce case (1/150 at nonce 4242;
`.ufo/waves/round-47/w2/ExecC1Determinism.md:75-76`); the fixture `expect` rebuilds byte-identically on a second filesystem
(`:62`), and the builder is blind to the axis by construction — it varies only path depth and demands three identical runs
(`.ufo/waves/round-47/ctl/build-fixtures.py:70`, `:76`). · captured-by: none — the frozen builder's stability test compares
repeats on one filesystem, not orders across two. · fix: route into round 48 with M47-10's fixture work (non-claim, schema
v2): at least one fixture with two **valid** candidates in one directory whose selected id depends on readdir order,
recorded with the order it ran under (or a set-valued `expect`), so a `sorted()` mutant is a fixture failure and not a
lottery among the 150 nonce cases.

---

## Conflicts reported, not resolved

1. **round-47 closure D1 against measurement.** `corpus/lessons/round-47-verifier-spotcheck.md:46` says "Two refusals
   diverge from the pin: a FIFO named `*.desktop` (pin blocks, tool exit 2) and HOME unset (pin exit 1,", and the round-48
   assignment repeats the shape — "HOME unset modelled as the pin (round-47 D1)", `.ufo/waves/round-48/claims.md:20` with
   "pin exit 1, empty stdout". Measurement: the pin exits 1 **only** where an unset `XDG_*` default must expand HOME; with
   all three set it answers `rc 0` and an id, and the tool exits 2. Both regimes are receipts (`probe4`, `probe5`,
   `receipt-home-unset-host`). The C1 contract and any v2 fixture depend on which regime is frozen — the L1 must pick one
   and say which, because the exit-1 row and the `rc 0` row cannot both be the pin's behaviour for one fixture.
2. **FIFO "the script blocks reading it"** is true only when the FIFO is the candidate read; it is registered otherwise and
   the resolver answers (`probe7`). The tool's walk-time raise is broader than the script it models.
3. **"symlink loops" as an exit-2 exclusion** has no implementing raise (M47-13) and no measured divergence on the shapes
   built. Freezing it as written would make the frozen predicate describe behaviour the tool does not have.
4. **Readdir order and the 190 fixtures**: unchanged (D3), routed here as M47-15 rather than claimed.

Host-cache hygiene: `~/.cache/xdg-terminal-exec` read-only throughout; the pin ran only with `--print-id` and with
`XDG_CACHE_HOME` inside the scratch root; the host cache mtime is `2026-10-26 17:42:25.200770484 -0300` before and after
(`receipts/probe-out.txt` tail, `receipts/probe2-out.txt` tail).
