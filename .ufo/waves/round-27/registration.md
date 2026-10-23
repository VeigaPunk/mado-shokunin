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
