# R54W2Seat11 — w2 item 11: C1 self-consistent pin laundering

Axes (godspeed): **falsification power** (does the frozen hash binding survive a
self-consistent pin+SUMS mutation?), **freeze fidelity** (every verdict derived
only from frozen contract lines, no post-score predicate edits), **harm
containment** (lane untouched except this report; fixtures git-isolated in
scratch).

## Item attacked

Item 11 — "C1 self-consistent pin laundering. Mutate pin and refresh its
SHA256SUMS; test frozen hash binding."

Frozen contract lines attacked:

- `claims-frozen.md:21` — predicate line `… pins=4/4 … verdict=TARGET_MET`.
- `claims-frozen.md:28-29` — clause (c): "each of the four pins' bytes hash to
  the round-52 recorded sha256".
- `claims-frozen.md:77-81` — C1 causal separability: the counter "reads only"
  its own file, the errata entry, `.ufo/waves/round-52/fetch/` (+SHA256SUMS)
  "and the frozen table of this file". `registration.md` is **not** in the
  readable set, and the frozen table of `claims-frozen.md` (:25-35) carries **no
  digests** — only ID / pin file / anchor / quote.
- `registration.md:12-19` — the four round-52 digests, frozen only here
  (`a83abeb5…`, `746c6f51…`, `8d8f35fc…`, `7248cbb8…`); prose calls the file
  "its committed `SHA256SUMS.txt`".
- `registration.md:44` — C1-CTL-3 hash-tamper: "one recorded sha256 in **the
  tree's SHA256SUMS** changed by one hex nibble → `pins≤3/4` MISSED".
- `registration.md:51-52` — judge clause (verbatim = byte contiguity after
  single-space normalization of interior newlines).
- Exact pin spans: P19 `ConfigActions.cpp:1554-1558` (5 physical lines; 1772
  lines in the pin at the base content), P20 `ConfigActions.cpp:1576` (single
  line), P21 `DispatcherTranslator.cpp:619-622` inside 591–627, P22
  `DispatcherTranslator.cpp:573-574` after 571. All four verified present at
  their exact spans in the green fixture (probe `at_anchor=True`).

## Counter status: NOT RUN / absent

```
$ ls /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters | grep -c r54
0            (grep exit 1)
```

No `c1-r54-*` file committed or untracked (`git status --porcelain` shows only
`M corpus/SOURCES.md` plus round-54 wave files). Matches the pinned before
receipt (`receipts/before.txt`: "r54 counters present: 0"). The w1 seat01 draft
counter lived in that seat's scratch and is gone. **Every real-counter run for
this item is NOT RUN; the falsification below is executed against the frozen
contract itself via a fixture probe, not against a landed counter.**

## Experiment (fixtures in scratch; every git call `git -C D`; toplevel asserted)

Probe (`probe.py`, scratch) reads all inputs from git objects at `--rev` via
`git -C D show <rev>:<path>`, embeds the frozen rows byte-exact (extracted from
`registration.md` @ `350d30e4`) and the four digests, and evaluates clause (c)
under its two possible implementations:

- `binding=tree` — expected digest = the scored tree's
  `.ufo/waves/round-52/fetch/SHA256SUMS(.txt)` entry, basename-keyed;
- `binding=frozen` — expected digest = the registration-frozen digest AND the
  tree's SUMS entry must equal it.

Quote/anchor legs are shared by both bindings (whitespace-collapsed contiguity
spanning exactly the cited anchor, `registration.md:51-52` collapsed reading).

Four fixtures, each a fresh `mktemp -d` git repo seeded with the base content of
the C1 inputs (errata entry + round-52 fetch), one commit each:

| fixture | mutation |
|---|---|
| `g` (green) | none |
| `launder` | append `\n/* seat11 launder probe: … */\n` to `Hyprland-ConfigActions.cpp` (lines 1772→1774; every cited anchor ≤ 1578, so no span moves) **and** replace that pin's digest in `SHA256SUMS` with the recomputed one |
| `pinedit` | same append, SUMS left stale |
| `ctl3` | SUMS digest nibble-tamper only (`…7637`→`…7634`), pin untouched |

Identity guard output for every fixture commit:
`git -C D rev-parse --show-toplevel` → the fixture dir itself (asserted `True`).

### Result matrix

```
TREE g        (rev eb81c5dde4609f8657a4287981cf0be56f8b8634)
  [SUMS-trusting counter] binding=tree:   quotes=4/4 anchors=4/4 pins=4/4 verdict=TARGET_MET exit=0
  [frozen-digest counter] binding=frozen: quotes=4/4 anchors=4/4 pins=4/4 verdict=TARGET_MET exit=0
TREE launder  (rev d7083af4907f707b92390c784fe3e48c81a6b392)
  [SUMS-trusting counter] binding=tree:   quotes=4/4 anchors=4/4 pins=4/4 verdict=TARGET_MET exit=0   <-- LAUNDERING ADMITTED
  [frozen-digest counter] binding=frozen: quotes=4/4 anchors=4/4 pins=2/4 verdict=TARGET_MISSED exit=1
TREE pinedit  (rev 863a5e08b2e409d321a971adb2169f2e3b8979e7)
  binding=tree: pins=2/4 TARGET_MISSED exit=1 ; binding=frozen: pins=2/4 TARGET_MISSED exit=1
TREE ctl3     (rev eb4d8dbc50d4e4df9d51954f7c47ca3cc987115c)
  binding=tree: pins=2/4 TARGET_MISSED exit=1 ; binding=frozen: pins=2/4 TARGET_MISSED exit=1
```

On the laundered tree, basename-keyed `sha256sum` self-consistency over the
mutated SUMS passes for all five entries (`laundered tree basename-keyed SUMS
self-consistent: True`), and `git diff --stat green→laundered` shows exactly
`Hyprland-ConfigActions.cpp | 2 ++` and `SHA256SUMS | 2 +-`.

(The `exit=` values are the simulated counter's mapped exits; the probe process
itself exits 0. Probe source and all raw outputs lived in
`/fast/scratch/hyaku/mado-r54/R54W2Seat11`, removed before this yield.)

## Findings

**F1 — HIGH (control-suite insufficiency; the frozen hash binding is not
frozen-enforceable).** A counter that takes clause (c)'s expected digests from
the scored tree's own `SHA256SUMS` passes **all six frozen C1 controls**
(including CTL-3 — demonstrated: `ctl3` fixture → `pins=2/4 TARGET_MISSED`
under `binding=tree`) and yet prints the frozen green line on a self-consistent
laundered tree (`launder` fixture → `pins=4/4 … TARGET_MET exit=0`). The
landered tree is indistinguishable from a genuine tree on every leg a
tree-derived check can compute: quotes 4/4, anchors 4/4 (pure EOF byte-append;
spans 1554-1558/1576/619-622/573-574 unchanged), pins 4/4 (SUMS refreshed). The
only artifact that separates it from `TARGET_MET` is the digest set frozen in
`registration.md:14-19` — which `claims-frozen.md:77-81` does not let the
counter read, and no frozen control compels the counter to embed. The frozen
six therefore underdetermine the implementation, and one of the two admissible
implementations launders. This closes w1 R54Seat01's §7 open item 2 with proof:
the gap is not hypothetical, it is reachable by a contract-obeying counter.

**F2 — MEDIUM (clause-(c) referent ambiguity).** "The round-52 recorded sha256"
(`claims-frozen.md:28-29`) is ambiguous between the immutable registration
digests (`registration.md:14-19`) and the mutable tree file
(`.ufo/waves/round-52/fetch/SHA256SUMS`). CTL-3's own wording — "one recorded
sha256 in **the tree's** SHA256SUMS" (`registration.md:44`) — endorses the
mutable referent, i.e. precisely the source laundering defeats. Freeze
self-consistency holds (base `e25149fe` SUMS digests == registration digests,
verified byte-for-byte), so the frozen table is usable as the binding source;
the contract just never says it is the binding source.

**F3 — LOW (frozen-prose filename defect).** `registration.md:12` says the
digests come from the round-52 dir's committed "`SHA256SUMS.txt`"; the tree
ships the file as `SHA256SUMS` (no extension) — `git ls-files
.ufo/waves/round-52/fetch` → `SHA256SUMS`; the round-54 fetch dir uses
`SHA256SUMS.txt`. A literal resolver of the registered name finds nothing for
C1. (Concurs with w1 R54Seat01 §4.7.)

**F4 — LOW (recorded paths are absolute).** The round-52 SUMS entries record
absolute lane-checkout paths (`/home/vgpnk/Projects/shokunin/mado-shokunin/…`).
A counter that resolves them literally reads the live worktree, not `--rev`, and
is blind to fixture-resident laundering while over-reading the lane; basename
keying plus blob-at-rev reads is required (w1 R54Seat01 §4.1/edge 11 concur;
my `launder` fixture proves basename-keyed self-consistency passes on the
mutated tree).

**Required shape for the landed counter (acceptance input for L1; predicates
themselves are frozen and were not touched):** (i) bind clause (c) to the four
registration digests embedded in the counter source — `sha256(blob at --rev) ==
frozen` AND `tree SUMS entry == frozen`; (ii) key SUMS by basename, accept both
`SHA256SUMS`/`SHA256SUMS.txt`; (iii) add a `launder` red case (pin+SUMS
co-mutation) to the `--selftest` red runs; (iv) never resolve the recorded
absolute paths.

## Relevant w1 reports

- `w1/R54Seat01.md:205-236` (§4.1 pin-byte laundering hole, "the frozen six
  miss it"), `:238-243` (§4.2 `launder`), `:324,340` (their draft harness:
  `case launder … OK`), `:402-405` (§7 open item 2). My work is the independent
  fixture proof that the SUMS-trusting implementation **passes CTL-3 while
  admitting launder** — the asymmetry Seat01 asserted but did not demonstrate —
  plus the freeze-vs-base digest equality check and the exact-span/line-count
  evidence.
- My own w1 report `w1/R54Seat11.md` was C2 frontier recon (`uwsm-app`
  environment); item 11 is fresh ground for this seat, no self-overlap.

## Honest iteration note

A first probe pass using the strict judge reading (newline→space only,
`registration.md:51-52` literal) failed to find P19/P21/P22 even in the
**pristine** pins (source indentation produces multi-space runs the frozen
single-line quote cells do not carry); this reproduces w1 R54Seat01 §1's judge
ambiguity and is not this item's axis. The matrix above uses the collapsed
reading, which is green-on-green. The laundering conclusion is
judge-independent: the mutation is a pure EOF byte-append and cannot move any
quote/anchor leg under any reading that passes the green tree.

## Harm watch and scope

- No lane file written except this report; no source/fixture/predicate/
  registration edits; no git/jj mutation in the lane; no commits/pushes outside
  fixtures; no delegation, background jobs, host/config/service/compositor
  reads or mutations, package queries, screenshots, or producer execution.
- Fixtures: `mktemp -d` under `/fast/scratch/hyaku/mado-r54/R54W2Seat11`;
  every git command `git -C D`; toplevel equality asserted before each commit;
  throwaway identity (`user.name=seat11`) used only inside fixtures.
- No tool installed or updated (RULES.md had nothing to act on; python 3.14.8
  and git already present).
- Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat11` removed before yield; no
  ENOSPC observed.

## Report trailer

Lane-relative report: `.ufo/waves/round-54/w2/R54W2Seat11.md`.
