author: mado

# mado round 27 — registration (frozen before any control or data seat)

Base: lane tip `543f0445e9d60bdfa026c54772d29e8b96bc844b` (round-26 closure: admitted). Paths below resolve under
`.ufo/waves/round-27/` unless they start with `tools/`, `quality/` or `corpus/`.

## Claims

**C1 — coverage (sourced), new operation: the workspace-rule table.** Surface moved: the Hyprland workspace-rule
plane (`workspace = SELECTOR, RULES` lines and the table Hyprland builds from them, `hyprctl workspacerules -j`) is
not derived by any lane tool or note at base: `git grep -n -i "workspacerules\|workspace rule" 543f0445 -- tools
corpus/knowledge` finds no tool and only the fact that the verb exists (`corpus/knowledge/rule-attribution-r24.md:21,58`,
A24; `window-rule-effects-getprop.md:12`); after: `tools/mado-wsrules.py` predicts it from config bytes, measured against
Hyprland v0.56.2 itself through the isolated oracle (`harness/oracle.py`, the round-26 harness with the M26-5 and
symlink fixes). The command that would show it unmoved: the counter below at the after revision printing anything
but 41/41.

**PRED-C1-r27**: At REV, the committed bytes of tools/mado-wsrules.py, run in the tool sandbox (no network, no /run,
cleared environment, the case tree read-only at /snap/home from a randomly named directory), print for the
unperturbed snapshot of the four Hyprland config roots and for each of 40 generated cases (25 that add workspace
rules to the snapshot, 15 independent trees that contain none of the snapshot's files) a JSON array equal, entry by
entry and in order, to the array Hyprland v0.56.2 itself prints with `hyprctl workspacerules -j` for the same tree
(a nested, headless, session-isolated instance run by the counter on a copy with exec lines removed); target:
cases_pass=41/41.

Counter: `python3 -I .ufo/waves/round-27/c1/count.py REV [--seed HEX] [--jobs N]` (exit 0 met, 1 missed, 2 guard).
Before: REV `543f0445`: `tool=MISSING_TOOL`, 0/41 (pilot receipt `evidence/c1-before-543f0445.txt`).

**C2 — operability: the lane's two offline gates fail when their subject is broken.** Surface moved: the lane's
gate suites over its round-26 counters and population checker (`quality/counter-selftest.py`,
`quality/population-suite.py`, new at lane root; the round-26 self-test fails green on the active C1 v2 counter
(7/9) and passes 6 of its 10 mutants; the round-26 population fixtures pass 3 of 6 checker mutants: lesson
round-26 M26-8). The command that would show it unmoved: the counter below at the after revision.

**PRED-C2-r27**: At REV, the committed suites quality/counter-selftest.py (gate over the round-26 counters
c1/count-v2.py and c2/count.py) and quality/population-suite.py (gate over the round-26 checker
quality/check-population.py), each run on a fresh clone of REV, exit 0 on all 8 green runs (each pristine subject
set and each subject with one of two behaviour-preserving edits: an appended comment, an inserted unused
module-level assignment), exit non-zero on each of the 15 W mutants (the round-26 wave-2 mutation probes of those
subjects, re-expressed on the active C1 v2 counter) and exit non-zero on at least three quarters of the valid
sealed held-out mutants, with at least 6 valid held-out mutants; target: green=8/8, w_killed=15/15,
h_killed>=ceil(0.75*h_valid), h_valid>=6.

Counter: `python3 -I .ufo/waves/round-27/c2/count.py REV --heldout DIR` (W set `c2/mutants-w.json`, 15 mutants:
9 of the round-26 MutSelftest probes, `c1-*` re-expressed on `c1/count-v2.py`, and the 6 MutQ37 probes; the
round-26 suite-mutant `selftest-drop-embed-assertion` is out of scope because it mutates the suite, not a subject).
Held-out set H: wave-1 mutation-tester seats write mutants of the three subjects to
`/fast/scratch/hyaku/mado-r27/heldout/*.json`; the L1 commits the sha256 of every H file before any repair seat is
dispatched and commits the bytes after the single C2 measurement. Repair seats never read that directory.
Before: REV `543f0445`: both suites missing, `green=0/8 w_killed=0/15` (pilot receipt `evidence/c2-before-543f0445.txt`).

## Kill rule and controls (before data)

A control that meets a target under its frozen counter forces redesign of that claim before data (or the claim is
declared exploratory). Each control is scored with **two seeds** (M26-9), receipts under `controls/`:

- C1: DoNothing (prints `[]`), Junk, Echo (one entry per `workspace =` line, selector only), LabelKeyed (looks for
  case labels in paths, environment, mountinfo), StaticBase (prints the unperturbed snapshot's table), NaiveGrep
  (root file only, line by line, no merge, no variables), RootOnly (merges, root file only), NoMerge (every file,
  no merge), NoVariables (every file, merges, `$var` left literal).
- C2: DoNothing (= base: suites missing), R26Suites (round-26 self-test and a runner of the five round-26 population
  fixtures), RejectAll (suites always exit 1), AcceptAll (always exit 0), ShaPin (exit 1 unless the subject's
  sha256 equals the pristine pin), ASTPin (exit 1 unless `ast.dump` equals the pristine one), WBlocklist (exit 1 when
  a subject contains any W mutant's `new` text). Scored on W first; the L1 re-scores every C2 control with H after H
  is sealed, before data.

## Data rule

C1: two executor seats build `tools/mado-wsrules.py` independently; the first file returned lands unmodified and is
measured once with a fresh seed; the other stays a second implementation. C2: two seats build each suite; the first
returned of each lands unmodified; one measurement. No data seat feeds Hyprland known-crash inputs (overflowing
numbers, source cycles); each data seat reports its own coredump delta (M26-6).

## Host safety

Every nested Hyprland runs inside the round-26 tinywl + bubblewrap sandbox (`harness/oracle.py`), now launched under
`env -i PATH=/usr/bin` (M26-5); the tool sandbox likewise. Receipts print `HOST_SAFETY ... delta=`. The live session
is only read with `hyprctl -j` query verbs.

## C1 redesign before data: counter v2 (10:38Z, before any data seat)

w1 `CritC1Counter` (non-author critic) showed a source-blind reader that never follows `source =` (it scans every
file in the tree and orders them by file-name buckets) meeting v1 at 41/41 on two fresh seeds
(`controls/K1FlatScan-v1-seed{1,2}.txt`, tool `controls/K1FlatScan.py` sha256 `68339595…abf1ea`): v1 sourced every
file it wrote, at the end of the root. Under the kill rule v1 is retired as C1's rule before data; v1 and its receipts
stay. Counter v2 `c1/count-v2.py` (sha256 `f7f86d75eb45a2dcd6a2094dcb614b701c948d6fee90f46da911831213c1a2c4`) adds
unsourced DECOY files carrying workspace rules (mentioned only in a commented-out source line or sourced only from
another unsourced decoy), places each new `source =` line at a random position among the root's rule lines (ORDER),
sources files from sourced files (NESTED) and through glob patterns (GLOB), and draws file names of random length and
extension. Same comparison, guards, oracle and population (BASE + 25 APPEND + 15 SYNTH).

**PRED-C1-r27-v2**: At REV, the committed bytes of tools/mado-wsrules.py, run in the tool sandbox (no network, no /run,
cleared environment, the case tree read-only at /snap/home from a randomly named directory), print for the
unperturbed snapshot of the four Hyprland config roots and for each of 40 generated cases (25 that add workspace
rules to the snapshot, 15 independent trees that contain none of the snapshot's files; cases carry unsourced decoy
files, nested and glob sources and source lines placed among rule lines) a JSON array equal, entry by entry and in
order, to the array Hyprland v0.56.2 itself prints with `hyprctl workspacerules -j` for the same tree (a nested,
headless, session-isolated instance run by the counter on a copy with exec lines removed); target: cases_pass=41/41.

Counter: `python3 -I .ufo/waves/round-27/c1/count-v2.py REV [--seed HEX] [--jobs N]`. Before (L1 pilot, REV
`543f0445`): `tool=MISSING_TOOL`, 0/41 (`evidence/c1v2-before-543f0445.txt`). L1 pilot of the flat reader under v2:
9/41 (`controls/v2/K1FlatScan-L1pilot.txt`). Every C1 control is re-scored under v2 with two fresh seeds by the seat
that built it (receipts `controls/v2/<Control>-seed{1,2}.txt`) before any data seat.

### C1 v2 amendment (10:42Z, before any seat scored v2)

Two more w1 `CritC1Counter` findings were folded into v2 before any control or data seat ran it: the comparison is
type-strict canonical JSON (`json.dumps(..., sort_keys=True)`; Python's `1 == True` and `5 == 5.0` let a wrong type
pass), and a VARREDEF trap (a variable used, redefined and used again) defeats a reader that binds each name once.
Final v2 sha256 `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87` (the `f7f86d75…` above was the
unamended file; only the L1 pilot ran it). PRED-C1-r27-v2's sentence is unchanged. Pilots on the final file:
`evidence/c1v2-before-543f0445.txt` 0/41; `controls/v2/K1FlatScan-L1pilot.txt` 1/41.

## C2 redesign before data: counter v2 (10:45Z, before any data seat)

w1 `CritC2Counter` showed a normalised-source pin accepting all 8 public green runs and rejecting all 15 W mutants
without executing a subject, and synthetic held-out rows that are equivalent, uncompilable or duplicates being
accepted; w1 `SentinelC2Clone` (HIGH) showed suites running unsandboxed against a `--shared` clone. Counter v2
`c2/count-v2.py` (sha256 `4dfb34b5551a908aa7fd56e75526417b43659018c47fa5993ad39a72b6b109d3`): sealed
behaviour-preserving edits written by the w1 Held* seats join the green set; every sealed row must compile, differ
from the pristine AST and be byte-distinct from the pristine subject, every W mutant and every other row; sealed
files are read once and must match `--seal FILE`; runs are shuffled, each in its own directory; clones are
`--no-local`; suites run under bubblewrap with `/home` and `/fast` hidden except the run directory. v1 and its
receipts stay.

**PRED-C2-r27-v2**: At REV, the committed suites quality/counter-selftest.py (gate over the round-26 counters
c1/count-v2.py and c2/count.py) and quality/population-suite.py (gate over the round-26 checker
quality/check-population.py), each run on a fresh no-local clone of REV inside a sandbox that hides the lane and the
host home, exit 0 on every green run (each pristine subject set, each subject with one of two public
behaviour-preserving edits, and each valid sealed behaviour-preserving edit, with at least 3 valid sealed edits
covering all three subjects), exit non-zero on each of the 15 W mutants (the round-26 wave-2 mutation probes of those
subjects, re-expressed on the active C1 v2 counter) and exit non-zero on at least three quarters of the valid sealed
held-out mutants, with at least 6 valid held-out mutants and at least 2 per subject; target: green=all,
w_killed=15/15, h_killed>=ceil(0.75*h_valid), h_valid>=6.

Counter: `python3 -I .ufo/waves/round-27/c2/count-v2.py REV --heldout /fast/scratch/hyaku/mado-r27/heldout --seal
.ufo/waves/round-27/c2/heldout-seal.txt`. Before (L1 pilot, REV `543f0445`, no sealed set):
`evidence/c2v2-before-543f0445.txt` green=0/8 w_killed=0/15. Every C2 control is re-scored under v2 by its seat, and
by the L1 with the sealed set once sealed, before any data seat.

## C1 redesign before data: counter v3 (11:0xZ, before any data seat)

w1 `CritC1Counter`, attacking v2 on the L1's request, met v2 at 41/41 on two fresh seeds with a reader that follows
`source =` but binds variables globally, except for names starting with `$wsr` (the prefix v2 gave its
redefinition probes): a shortcut keyed on a fixture label (`controls/K1PrefixKeyed.py`, receipts
`controls/v2/K1PrefixKeyed-seed{1,2}.txt`). Under the kill rule v2 is retired before data; v2 and its receipts stay.
Counter v3 `c1/count-v3.py` (sha256 `ee4cea19c11a1a8160115f4754e88c11c58aac9a3bff40ccfd16920cd1d691bd`) is v2 with
every generated variable name drawn as `$` + 5-9 random letters (no fixed prefix). L1 pilots: before (REV `543f0445`)
0/41 (`evidence/c1v3-before-543f0445.txt`); K1PrefixKeyed 23/41, K1FlatScan 2/41 (`controls/v3/*-L1pilot.txt`).

**PRED-C1-r27-v3**: the PRED-C1-r27-v2 sentence above, word for word, with the counter `c1/count-v3.py`; target:
cases_pass=41/41. Every C1 control is re-scored under v3 with two fresh seeds by the seat that built it before any
data seat (`controls/v3/<Control>-seed{1,2}.txt`).

## C1 redesign before data: counter v4 (11:10Z, before any data seat)

w1 `CritC1Counter` met v3 at 41/41 on two fresh seeds each with two partial readers that key on no label: GlobalOnce
(a name defined once applies everywhere; only redefined names bind by position; whole-field substitution; each file
read once) and FileScope (definitions in a sourced file never reach the sourcing file)
(`controls/K1GlobalOnce.py`, `controls/K1FileScope.py`). Cause: v3 wrote every definition at the top of the root,
every use as a whole field, and never sourced a file twice. Under the kill rule v3 is retired before data. Counter v4
`c1/count-v4.py` (sha256 `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`) adds the critic's four
shapes: VAREMBED (a variable holding only an item's value, used inside the item), SRCDEF (definitions in a sourced
file that runs before their uses), USEBEFOREDEF (an item variable used once before its only definition, then after)
and TWICE (one file sourced twice with a conflicting rule in between); same population, oracle and comparator.
L1 pilots: before 0/41 (`evidence/c1v4-before-543f0445.txt`); FileScope 24/41, GlobalOnce 18/41, PrefixKeyed 16/41
(`controls/v4/*-L1pilot.txt`).

**PRED-C1-r27-v4**: the PRED-C1-r27-v2 sentence above, word for word, with the counter `c1/count-v4.py`; target:
cases_pass=41/41. Every C1 control (now 13 shapes) is re-scored under v4 with two fresh seeds before any data seat
(`controls/v4/<Control>-seed{1,2}.txt`).
