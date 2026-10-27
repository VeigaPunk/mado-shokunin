# SimplifierLedger — YAGNI pass on the C1/C2 instruments (round 51, w1)

Status: complete. Leaf seat; no subagents, no `agent://all`, no tracked-file edits, no git/jj
mutation in the lane.

## What was reviewed

The instrument drafts landed while this pass was reading, so the review is bound to digests
(2026-10-27T07:06-03:00): `ExecLedgerGate/check-tool-ledger.py` `6756bdb8dbbe` (782 lines),
`ExecLedgerCounter/c1-r51-ledger.py` `11fc2ca77047` (440), `ExecCounterC2/c2-r51-dispatch-entry.py`
`abf41d4b84f8` (615, moved twice during the pass), `ExecLedgerPopulation/tool-ledger.md`
`c0a89805f4e5` (79 rows at base). Where a draft was still empty at first read I reviewed the
frozen sentence instead — no recommendation below rests on an absent artifact.

## Headline

- **One instrument authority, not two.** The counter re-parses the checker's printed text and
  compares six fields. Measured on the same ledger with a duplicate row: counter
  `dangling=0 dup=1`, checker `dangling=1`. The frozen field `dangling` means two things, and a
  sibling's parse quirk can flip a counter-green ledger to MISS. Delete the runtime cross-check
  (`checker_ledger`, ~140 lines) or make it a freeze-time receipt.
- **C2 reads "the row's quote" from the entry line, not from the SOURCES row**, and accepts a
  backticked identifier as a quotation (measured: `\`xkb_state_key_get_one_sym\`` passes the
  ≤25-word verbatim test). That is a weakening of the frozen clause (b), not a style issue.
- **C2 leaks a scratch dir per run** (measured: `c2-r51-ey53pkjh` left behind at base) because it
  writes a probe JSON nothing reads; deleting the probe deletes the leak.
- **Two of my own first-read deletions were wrong**, and measurement says so: `unfenced()` is
  load-bearing (the real ledger carries a fenced grammar example — naive counting gives 80 rows
  against a population of 79) and `LINE_SUFFIX` is load-bearing (the ledger annotates pointers as
  `path:NN`; without the strip 79/79 rows go `bad_pointer`). A YAGNI pass that deleted them would
  have broken the artifact it was meant to shrink.
- Frozen clauses are **satisfiable** by the drafts as written: both C1 instruments agree on the
  drafted ledger (`population=81 ledger_rows=79 uncovered=2 dangling=0 bad_pointer=0 empty_desc=0`
  — the two uncovered rows are the new scripts), the checker selftest is 42/42 in 0.8 s, and the
  C1 counter at base prints `ledger=absent`, exit 1, in 0.9 s. C2 at base prints
  `clauses_met=0 admitted=0/1 verdict=TARGET_MISSED`, exit 1.

## Measurements behind the recommendations

- Population at base by independent count: 79 = `tools/` 17 + `quality/*.py` 18 +
  `quality/counters/*.py` 44. At freeze it is 82 (three new instruments).
- The 119-line reference sketch (`SimplifierLedger/ref-minimal-c1.py`) reproduces all five frozen
  controls plus green and duplicate from a three-file fixture; it is the lower bound on the
  accounting (~130 lines with the three load-bearing grammar features), against 1,222 draft lines.
- C2 novelty cost: naive 8-gram pass over base knowledge (66 files) + every candidate file
  (3) = 0.10 s; worst overlap against the round-50 entry reproduces at 81.0% vs
  `.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md`. No case for caching,
  persistence or parallelism in clause (c).
- Six freeze wording items are listed in `yagni.md` because each changes observable output
  (base-absent line shape, "non-empty" definition, quote location/grammar, locator token,
  duplicate accounting, candidate baseline revision).

## Housekeeping

- Scratch: `/fast/scratch/hyaku/mado-r51/SimplifierLedger/` (reference sketch, a `--shared` clone
  used as a fixture repo, control-matrix transcripts). Removed before yielding; the receipts that
  matter are quoted in `yagni.md` and the sketch is copied into the seat dir.
- No tool installed or upgraded; no pacman transaction; no compositor socket touched; the config
  planes were read only indirectly (nothing under `~/.config` was opened at all).
- Disk: `/fast/scratch/hyaku` 293.5 G free at start (64% used), `/tmp` 124.3 G — no guard trip.

## Deliverables

- `.ufo/waves/round-51/w1/SimplifierLedger/yagni.md`
- `.ufo/waves/round-51/w1/SimplifierLedger/ref-minimal-c1.py`

Report: .ufo/waves/round-51/w1/SimplifierLedger/yagni.md
Report: .ufo/waves/round-51/w1/SimplifierLedger/ref-minimal-c1.py
Report: .ufo/waves/round-51/w1/SimplifierLedger.md
