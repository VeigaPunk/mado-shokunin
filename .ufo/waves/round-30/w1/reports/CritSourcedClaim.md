# CritSourcedClaim — r30 w1 — falsify the sourced-claim chain

Scope: report only. Attacked the S185 → C3 chain (own-work + mined + teaches),
the `used-by` cell, the anchor/quote vs SOURCES-CONTRACT-v1, prior own-work
precedent (S013–S015, S184), and the vacuity counterexample (green-at-base
gate). Verdict name for C3: **SOURCED-LEG VALID / TARGET_MET** — the
self-citation counterexample fails to falsify, but the attack exposes a real
systemic absence (no anti-circularity guard on own-work sourcing) and three
fixable formality defects.

## 1. Counterexample tested and result

**CE1 — self-citation loophole (the assignment's hypothesis).** Attack: a
round can satisfy "sourced" by opening an own-work row over lane text it
controls, letting any claim self-ground. **Not falsified** — three defenses
hold, each verified this session:

1. The sourced bytes **predate the round**. The anchored fence (SCORECARD.md
   "Fleet round 1 — coverage navigation", "Counting command" block) was
   introduced 2026-10-15 in commit `7cd7f33` (`git log -S` on the block's
   `raise SystemExit(1 if ...)` line) — nine days before round 30. The row
   *registers* existing authority; the round did not author the text it cites.
   This is the load-bearing fact against the loophole: the claim cannot be
   shaped by the source, because the source already pinned the semantics the
   claim had to implement.
2. The anchor is **content-pinned**. Recomputed
   `sed -n '70,89p' SCORECARD.md | sha256sum` =
   `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` —
   byte-identical to the anchor cell in `corpus/SOURCES.md:197` and the
   lesson `## Gate` quote-table in `corpus/lessons/round-30.md:24`. A sha256
   of the block is stronger revision evidence than most own-work anchors
   (S013 uses `HEAD`, which drifts).
3. The scope is **lane-semantics-only**: "the index-completeness semantics
   this lane's coverage-navigation rubric uses." For semantics the lane
   itself defines, own-work is the only possible primary — the contract's
   tier-A list ("the lane's own re-runnable gate output" is an A example)
   supports this reading. S185 admits no domain claim.

**CE2 — vacuous gate (control K3).** Re-ran the gate, not just the receipt:
`python3 -I quality/check-index.py --rev 8f51071b…` prints
`indexed=41/43 missing=2` naming both routed notes, `EXIT=1`;
`--rev 446dc396…` prints `indexed=43/43`, `EXIT=0`. Matches
`evidence/c3-after-446dc396.txt`. A do-nothing round cannot produce this
pair; the capability is non-vacuous.

**CE3 — teaches over-claim.** `teaches` asserts "every corpus/knowledge note
must have exactly one index row"; the verbatim Gate quote is only the
output-format line (`revision=$rev indexed=… duplicates=… coverage=…`), which
shows fields, not the normative rule. The rule lives in the block's code
lines (`duplicates = sorted(p for p, n in counts.items() if n != 1)`). The
quote *locates* the anchor but does not independently ground `teaches` —
contract rule 1 satisfied in letter, thin in spirit. Cosmetic: the anchored
block does contain the normative code, so the claim is still grounded.

## 2. Prior own-work rows (comparison)

| Row | Source bytes | Grounds | Predates claim? |
|---|---|---|---|
| S013 | gkeep `install.sh` (external repo, pinned `HEAD` 133b867) | provenance of observed config deltas | yes (foreign work) |
| S014 | `tools/mado-verify.sh` EXPECT/LOCAL lists (own-work) | gate re-anchor record | yes |
| S015 | `corpus/knowledge/omarchy-drift-watch.md:284-287` (own-work) | append-only re-anchor *form* | yes — and a round-13 erratum had to *narrow* its cited scope |
| S185 | SCORECARD.md counting fence (own-work, block-sha) | gate row-set semantics | yes (r1 block) |

S185 is the *same* shape as S014/S015: claim about the lane's own method
grounded on own text. It is the second gate-sourcing row in consecutive
rounds (S184 → r29 gate, S185 → r30 gate), i.e. a pattern, not a novel
bypass. S015's history is the cautionary precedent: an own-work row's cited
scope was later narrowed by erratum — S185's scope is already narrow.

## 3. Fixable defects (report-worthy, none falsify C3)

1. **`used-by` non-conformance.** Cell = `quality/check-index.py,
   .ufo/waves/round-30/registration.md`. Contract defines `used-by` as
   "knowledge entries or lessons citing the row" — neither is a knowledge/
   lesson path, while `corpus/lessons/round-30.md` (which *does* cite S185)
   is absent. S184's cell (`.ufo/waves/round-29/registration.md,
   corpus/lessons/round-29.md`) shows the conforming shape: registration +
   lesson. Append-only status means an L1 `used-by` append next round,
   logged old→new.
2. **Regex semantics drift.** Gate `ROW_RE = r"^\|\s*`knowledge/([^`]+\.md)`"
   tolerates `|  `knowledge/x.md`` (N spaces); the frozen fence requires
   exactly one space (`^\| `knowledge/…`). A non-canonical row counted as
   indexed by the gate but missing by the fence is a silent semantic
   divergence — the gate claims to implement the fence's semantics. Edge
   case only; currently vacuous (all committed rows are canonical).
3. **Anchor lacks a file revision.** Anchor pins by heading + block-sha
   only — sufficient, but weaker than S013–S015's revision-carrying anchors.
   The block-sha *is* revision data (arguably stronger), so this is
   observation-grade.

## 4. Systemic finding — the loophole is real but dormant

The attack's premise survives at the *contract* level: SOURCES-CONTRACT-v1
contains **no rule that own-work source bytes predate the claim**. Nothing in
the contract stops a future round from writing a SCORECARD sentence, opening
an S### row over it, and declaring the claim sourced — a closed loop S185
comes within one edit of exemplifying. Rule 1's "write the row only after
opening the source" only enforces ordering, not independence. S185 dodges
the loophole by accident of provenance (r1 bytes), not by rule. Impacted
axes: calibration/admission-integrity primarily; coverage secondarily (any
axis could launder its counting command through a same-round row).
Smallest safe correction (judge-class suggestion, not a defect in C3): a
QUALITY criterion requiring `sourced:` rows to anchor bytes committed at or
before the round's base revision — one clause turns S185's de-facto
safety into an invariant.

## 5. Implied verdict for C3

The sourced leg is **not falsified**: S185 satisfies the contract's row
shape (11 columns, valid kind/tier/status), its anchor is content-verified,
`teaches` is grounded by the anchored block, the Gate entry carries
URL-equivalent + access date + verbatim ≤25-word quote, and both `used-by`
paths exist at the data commit (verified: `git show
446dc396:corpus/SOURCES.md` carries S185, absent at base). C3's predicate is
independently confirmed red-at-base / green-at-tip with selftest 6/6 per
the receipt and a re-run this session. Implied C3 verdict: **TARGET_MET**.
The sourced-claim requirement is met on the strongest reading available
(pre-existing, content-pinned own-work), though the pattern's systemic
guard is absent and the used-by/regex items deserve repair.

Tooling: none installed. Read-only git (`log -S`, `show REV:path`) and
stdout-only gate runs; no repo bytes mutated.

## 6. Peer addendum (RevC1Fence, post-yield)

RevC1Fence's fence-vs-gate audit sharpens defect 2: the gate's `^\|\s*` is a
strict *superset* of the fence's `^\| ` (accepts 0 spaces/tabs), so
divergence is bidirectional — the gate can print green where the fence says
missing, AND fabricate `duplicates` the fence never sees. A gate claiming to
"implement the fence's row-set semantics" implements a superset of them.
Still latent on committed bytes (all 43 rows canonical); no verdict moved —
but it strengthens the case that the semantics-claim is imprecise, which is
exactly the teaches/anchor surface this item reviews.

Also noted from RevC1Fence (outside my item, recorded for provenance
honesty): lane worktree shows `M quality/q36-successor-receipts.txt` — a
committed evidence file rewritten with fresh ephemeral run dirs; no
rc/expected/PASS line moved. Committed bytes at 92d3c86 are intact; the
dirt is worktree-only and outside registered write scope.
