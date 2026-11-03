# R65ExecC1Counter — C1 register counter (round 65, w1 build)

Seat: `R65ExecC1Counter` (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Deliverable (draft for the L1 to integrate as `quality/counters/c1-r65-register.py` — **not**
written into `quality/`):

    .ufo/waves/round-65/w1/R65ExecC1Counter/c1-r65-register.py
    sha256 2ccedc6852a35a8cfbaaf8a92b1ad473c1464499cc892fa8753dc199eaaa1871   277 lines / 11668 bytes
    syntax=ok  top-level imports=argparse,os,re,subprocess,sys  (stdlib only)

Supporting artifacts in this seat dir: `evidence-transcript.txt` (the generated, verbatim run
log every paste below is taken from), `fixtures/` (the exact fixture inputs, sha256 above).

Installs: **none** (used the host's `/usr/bin/python3` = 3.14.8 and `git` 2.56.0).
Scratch `/fast/scratch/hyaku/mado-r65/w1/R65ExecC1Counter/` was created and **removed** at exit.

## What the counter does (frozen contract, claim C1)

`python3 c1-r65-register.py --repo DIR [--rev REV]` (REV required). Reads **git objects at
`--rev` only** — `git -C repo show <rev>:PROVINCE.md`, `git ls-tree -r -z --name-only <rev>`,
`git show <rev>:<receipt>`; it never opens a worktree path (no `open()`, no `tempfile`, no
`Path()` in the file — `grep` returns no matches, see transcript). No file writes, no scratch,
no network, no child other than `git`.

One stdout line:

```
MADO_R65_REGISTER: rows=<n> groups=<k>/8 receipts=<j> resolved=<i> gate=ok|missing verdict=TARGET_MET|TARGET_MISSED rev=<REV>
```

exit 0 iff `rows >= 8` **and** `groups == 8` **and** every extracted receipt resolves at rev
**and** `gate == ok`; else exit 1. Diagnostics (`C1_R65: detail=…`) go to stderr only.
Setup errors (bad `--repo`, non-repository, missing `--rev`) exit 2 — the lane's counter
convention (cf. `quality/counters/c1-r51-ledger.py`).

Parsed exactly as the frozen text says: block from the first line starting
`### Surface state register (2026-11-03` to the first later line starting `## ` or the sentinel
`<!-- r65 register end -->` (exclusive), whichever first, else EOF; data rows are `|`-lines at
column 0 (exact `startswith("|")`) that are neither separator nor markdown header (header = the
pipe row immediately above a separator row) and have ≥3 non-empty cells after splitting on `|`;
a group matches when a row's trimmed **first cell equals the group string**.

Three deliberate, documented readings (none changes a predicate):

1. **Receipt tokens** — frozen anchored pattern `^\.ufo/waves/round-65/receipts/[^ |,)]+\.(txt|json|md|sh)$`
   applied to whitespace-separated tokens; a token the strict pattern rejects is retried once
   with one markdown wrapper/bracket/quote run stripped from each end. This is what lets the
   table's backticked pointers (`` `.ufo/…/gate-live-r65.txt` ``) count; the path shape itself is
   never relaxed, and prose still cannot produce a false pointer. Tokens are de-duplicated in
   first-seen order.
2. **`rev=`** prints the resolved commit sha (house convention), not the raw `--rev` string; for
   the claim's own commands (full 40-hex shas) the two are byte-identical.
3. **Sentinel** is matched after `strip()`, heading by `startswith` at column 0 (frozen text).

## Evidence

All commands below were run as recorded; the interpreter printed as `/usr/bin/python` is the same
binary as `python3` (`/usr/bin/python3` → `python3.14`, 3.14.8).

### (a) Control through the implemented counter — frozen base `524fa1f9…` (must MISS)

```
$ python3 c1-r65-register.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 524fa1f90b1f2de44b3019bacf833d54e0af13a0
[stderr] C1_R65: detail=no '### Surface state register (2026-11-03' block at 524fa1f90b1f2de44b3019bacf833d54e0af13a0
MADO_R65_REGISTER: rows=0 groups=0/8 receipts=0 resolved=0 gate=missing verdict=TARGET_MISSED rev=524fa1f90b1f2de44b3019bacf833d54e0af13a0
RC=1
```

Same at the frozen-contract rev `cb63ab13…` (block not yet landed): `rows=0 … verdict=TARGET_MISSED
rev=cb63ab13ccaf85191318701d5db5ace050bd5bd4`, RC=1. Also RC=1 under `python3 -I` (isolated mode),
i.e. no environment dependence.

### (b) Green leg — fixture repo with a minimal valid block + two receipts (must MEET)

```
$ python3 c1-r65-register.py --repo /fast/scratch/hyaku/mado-r65/w1/R65ExecC1Counter/fx --rev de8a6722d1b92c95d4115ed09b5403761f58b6e7
MADO_R65_REGISTER: rows=8 groups=8/8 receipts=2 resolved=2 gate=ok verdict=TARGET_MET rev=de8a6722d1b92c95d4115ed09b5403761f58b6e7
RC=0
```

### (c) Negative fixture — same fixture, windows-desktop row deleted (must MISS)

```
$ python3 c1-r65-register.py --repo /fast/scratch/hyaku/mado-r65/w1/R65ExecC1Counter/fx --rev ad81e766422f553353a131796b72543360baa7b2
[stderr] C1_R65: detail=rows=7, need >= 8 data rows
[stderr] C1_R65: detail=groups missing (1): windows desktop plane
MADO_R65_REGISTER: rows=7 groups=7/8 receipts=2 resolved=2 gate=ok verdict=TARGET_MISSED rev=ad81e766422f553353a131796b72543360baa7b2
RC=1
```

Note the isolating detail: receipts and gate stay green — the miss is caused only by the missing
group, so the count is not a blanket "anything red" switch.

### Truth table (every leg isolated; full log in `evidence-transcript.txt`)

| leg | what it isolates | line (rev abbreviated) | rc |
|---|---|---|---|
| a1 | no 2026-11-03 block (base) | `rows=0 groups=0/8 … verdict=TARGET_MISSED` | 1 |
| a2 | no block at frozen-contract rev | `rows=0 groups=0/8 … verdict=TARGET_MISSED` | 1 |
| b | full valid block, two receipts | `rows=8 groups=8/8 receipts=2 resolved=2 gate=ok … TARGET_MET` | 0 |
| c | one group row deleted | `rows=7 groups=7/8 … TARGET_MISSED` | 1 |
| d | block ended by `## ` (no sentinel) | `rows=8 groups=8/8 receipts=2 resolved=2 gate=ok … TARGET_MET` | 0 |
| e | bare repo, **no worktree exists at all** | `rows=8 groups=8/8 … TARGET_MET` | 0 |
| f | real-lane rehearsal clone, worktree `PROVINCE.md` deleted, rev unchanged | `rows=8 groups=8/8 receipts=6 resolved=6 gate=ok … TARGET_MET` | 0 |
| g | 10-31-style first cell `hypr plane (…)` | `rows=8 groups=7/8 … TARGET_MISSED` + exact-cell hint | 1 |
| h1 | no `MADO_VERIFY: CLEAN` in any receipt | `… gate=missing … TARGET_MISSED` | 1 |
| h2 | pointer names an absent receipt | `… receipts=3 resolved=2 gate=ok … TARGET_MISSED` | 1 |
| h3 | `PROVINCE.md` absent at rev (fail closed) | `rows=0 … verdict=TARGET_MISSED … reason=province-unreadable` | 1 |
| s1–s3 | `--repo` missing / non-repo / `--rev` omitted | `C1_R65: setup=error …` (no MADO line) | 2 |

Leg (f) is a rehearsal of the **landing shape on real bytes**: a `--shared --no-checkout` clone of
the lane at `cb63ab13…`, one appended synthetic 2026-11-03 block naming the six committed round-65
receipts, one scratch-only commit `c1c2688b…` → `rows=8 groups=8/8 receipts=6 resolved=6 gate=ok
verdict=TARGET_MET rc=0`. That run also proves the real receipts resolve at a rev and that
`gate-live-r65.txt` and `gate-fileplane-r65.txt` each carry `MADO_VERIFY: CLEAN` **as committed**
(counter's own leg: `git show <rev>:… | grep -c` → `1` for each), and that the block is found with
the older `### Surface state register (2026-10-31…)` block still present above it.

Legs (e) and (f) are the structural proof of "reads git objects at `--rev` only": the counter is
green against a repository with no worktree, and green against a worktree whose `PROVINCE.md` was
deleted — the verdict tracks the rev, not the filesystem.

## Integration constraints for the C1 landing (read before writing the block)

These are consequences of the frozen text, not of my implementation; each one is a way the block
can be written correctly but counted wrong:

1. **First cell must be the group name alone.** The 2026-10-31 block writes
   ``| hypr plane (`~/.config/hypr/**`, `hyprctl`) | … |`` — copying that style yields
   `groups=0/8`. The eight exact strings (case- and space-sensitive) are:

   ```
   hypr plane
   waybar
   walker
   terminal configs
   theme/wallpaper omarchy plane
   idle/lock plane
   omarchy skill docs
   windows desktop plane
   ```

   Put the path/binaries in the *probe* cell. The counter prints a stderr hint naming the exact
   near-miss cell (leg g).
2. **`|` at column 0** — an indented table is not a row. The counter says so on stderr when it
   sees indented pipe lines.
3. **≥3 non-empty cells per data row** — a 2-column row is not counted.
4. **Heading prefix must be exactly** `### Surface state register (2026-11-03` at column 0; the
   block then runs to the next `## ` heading or the sentinel `<!-- r65 register end -->`,
   whichever comes first. End the block with the sentinel or the following `## ` heading, else any
   later pipe tables and any later round-65 receipt mention inside the same section also count
   (rows inflate; a stale pointer in that window would force a miss).
5. **Receipt pointers must be committed at the landing rev** and the file must contain the literal
   `MADO_VERIFY: CLEAN` for at least one of the resolved ones. Pointers are extracted from the
   whole block window, so every round-65 receipt path mentioned there — table cell or prose — must
   exist at the landing.
6. `rows` is checked **>= 8** (frozen), while the claim prose says `rows=8`; a block carrying an
   extra tool table would print `rows=9+` and still met. Keep the block to the single 8-row table
   if the literal `rows=8` matters to the scorecard row.
7. `rev=` prints the resolved sha; pass the full landing sha in the scorecard/receipt command.

## Findings

- The counter meets the frozen contract on both sides of the predicate and on every leg that can
  independently make it miss: block absence, row count, group equality, receipt resolution and the
  gate token (table above). Fixtures are preserved under `fixtures/` so the mutation-tester can
  rebuild the same controls (the fixture build is three `git init`/`commit` calls; revs are
  content-addressed and will differ per rebuild).
- The single real integration hazard is constraint 1: the lane's existing register row style
  (parentheticals in the first cell) is incompatible with the frozen group predicate. This is a
  property of the frozen wording, not a defect in either artifact — but the landing must use bare
  group names in cell 1.
- No lane file was touched: `git -C <lane> status --porcelain` shows **no tracked change**; my
  writes are confined to this seat dir (plus the now-removed scratch).

## Defects seen

None in the lane or in the frozen contract. Two wording-level notes for the L1's landing prose
(not defects, and no predicate change is proposed):

- Claim C1's after-state says "rows=8" while its counting rule says `rows>=8`; the counter
  implements the rule.
- The claim's control receipt already records the base miss by grep; the same miss through the
  implemented counter is pasted in (a) above, so the receipt can be extended with the counter's own
  `RC=1` line at integration time.
