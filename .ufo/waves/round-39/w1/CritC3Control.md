# CritC3Control — anti-claim control for C3 (sourced coverage)

Review date 2026-10-25, lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `457d1b125932c1e0d797061a2156b917bcd7edaa` (freeze).

## 1. Control inventory at review time (what exists)

- **c4 counter `quality/counters/c4-r39-options-entry.py` is ABSENT** from every ref and the worktree:
  - `git log --all --oneline -- quality/counters/c4-r39-options-entry.py` → empty (exit 0, no output).
  - `git ls-tree -r --name-only HEAD | grep -c c4-r39` → 0; `ls quality/counters/ | grep -c c4-r39` → 0.
  - Only `quality/counters/c3-r39-options.py` (C2) exists, untracked. Corroborated by the ExecOptionsCounter report ("Implemented only quality/counters/c3-r39-options.py as assigned").
  - ⇒ the C3 counting command cannot be executed at review time; PRED-C4-r39-v1 is not yet measurable.
- **round-39 lesson is ABSENT**: `ls corpus/lessons/` has no `round-39.md` (round-38 is the latest). The registration requires S218/S219 Gate lines *in the round lesson* binding a committed receipt by sha256 + located quote — none can exist yet.
- **Knowledge entry not committed**: `corpus/knowledge/config-option-table-r39.md` absent from HEAD and worktree; only the seat draft `.ufo/waves/round-39/w1/ScrKnowledgeEntry/config-option-table-r39.md` exists, whose `**OBS S218/S219**` lines are provisional citations, not verbatim located Gate quotes (ScrKnowledgeEntry.md confirms).
- **SOURCES rows S218/S219 absent**: `git show HEAD:corpus/SOURCES.md | grep -cE '^\| S21[89] '` → 0. Drafts live in `w1/ScrSourcesRows/rows.md`; **S219's receipt is INCOMPLETE** (no data commit; `tools/mado-options.py` uncommitted; no sha256 fabricated). Receipts fetched only as `w1/ExecAssimFetches/{S218,S220}.bin` (uncommitted; no `round-39/fetch/` dir yet).

## 2. Census experiment (fleet script, read-only, /tmp scratch)

Script: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (fleet root; lane has no `scripts/`). Scratch root `/tmp/crit-c3-scratch/crit-shokunin/` with `corpus/SOURCES.md` baseline (S218/S219-shaped rows) + empty `corpus/knowledge/config-option-table-r39.md` (so E11 does not fire on the baseline). All runs: `sources-census.sh validate --today 2026-10-25 <root>`.

| variant | mutation | findings | exit |
|---|---|---|---|
| baseline | none | `ok` | 0 |
| A | append well-formed **sourceless** row (source cell text-only, no URL, no receipt; opened 2026-10-25) | `ok` | 0 |
| B | append well-formed row whose S-id is **not opened this round** (opened 2026-10-24) | `ok` | 0 |
| C | append row with **future** opened date 2026-10-26 | `E08 S999 opened=2026-10-26` | 1 |
| D | append row with **duplicate id** S219 | `E03 S219 duplicate id` | 1 |
| F | append mined row with used-by `—` | `W03 S999 mined but unused` (warning only) | 0 |
| G | append row with **dangling used-by** (knowledge file missing) | `E11 S999 missing used-by corpus/knowledge/no-such-file.md` | 1 |

Conclusions from local evidence:
- The census **does fail structural junk**: duplicate ids (E03), future opened dates (E08), dangling used-by targets (E11), malformed rows/NFC, outside-Registry rows (E12), bad enums (E05-E07/E10). Exit 1.
- The census **does NOT fail a sourceless row**: it has no receipt column check, no quote/verbatim check, no "opened this round" check (E08 only rejects *future* dates), no requirement that the source cell contain a URL. Variants A and B pass with exit 0. A row whose S-id was not opened this round is indistinguishable from a compliant row to the census.
- Therefore census alone cannot block the claimed junk class; only the (absent) c4 counter can bind the counted rows to receipts/Gates.

## 3. c4-counter reachability analysis

- If the c4 counter is built to the round-38 Gate pattern (`GATE S158 receipt=... sha256=... quote="..."`, verbatim in receipt bytes and in the citing entry body), it can block the **counted** rows being sourceless: S218 must show a committed receipt hash + located verbatim quote; S219 must show the sha256 of the committed `tools/mado-options.py` bytes (own-work). A junk *replacement* of S218/S219 fails that check.
- **Enumerability gap (the counting command cannot enumerate):**
  1. `admitted=1/1` counts one admission unit. An **additional** sourceless junk row/entry (e.g., S999 with used-by pointing at the same knowledge file) leaves the count at 1/1 and passes census (variant A). The claim is therefore reachable by a junk-augmented state even if the counted pair is clean. Smallest safe correction: make the counter assert row-set equality — the only SOURCES rows whose used-by names `corpus/knowledge/config-option-table-r39.md` are exactly {S218, S219} (enumerable).
  2. **Universal clauses in the claim wording the counting command cannot enumerate:**
     - S219's row scope (ScrSourcesRows/rows.md, S219 cell) adopts C2's deliverable phrase: "(all non-bind/non-animation/non-workspace/non-rule `key = value` settings)". No byte-count can enumerate the key universe; the real-tree coverage is only proxied by C2's `fixtures=N/N`, which itself covers fixture rows, not every real key. The word "all" is not countable by `admitted=1/1`.
     - The entry's substantive claims (layer order, parser boundaries, the five divergence labels) are tool-behavior claims (C2's predicate), not derivable from the two source quotes; c4 verifies provenance marks, not entry-internal truth. A counter cannot enumerate "every claim in the entry is true of the shipped tool" — that authority is duplicated in C2, and c4 passing does not imply it.
     - "the config-option ownership ground is admitted" is an existential over one unit; the ownership-table rows themselves are never enumerated by C3's counting command.
- **Fabricated self-consistent bundle** (invented receipt bytes + invented Gate line + invented quote, all internally consistent) still passes any byte-level counter — this is the declared accepted-path tradeoff already recorded in registration C1 Residual; it is a tradeoff, not a fixable defect.

## 4. Verdict

- Fixable defect: the counting command's single admission unit cannot enumerate additional junk rows nor the "all … settings" universal; the claim as worded is reachable by a sourceless junk-append (variant A passes census; admitted count unchanged).
- Tradeoff (not rejectable): fully fabricated self-consistent artifacts pass — declared residual.
- Smallest safe correction: (a) add the row-set-equality clause above to PRED-C4-r39-v1; (b) scope the "all … settings" phrase to the counted/tested fixture set (C2) in the S219 row and entry, removing the unenumerable universal from the C3 deliverable.
- Current-state note: at review time the claim is not yet measurable/not met (c4 absent, round-39 lesson absent, S219 receipt missing, OBS lines provisional) — expected pending the data commit; this is not itself a defect.

No other file written; no tools installed; no git/jj mutation. Scratch retained at `/tmp/crit-c3-scratch` (outside the lane).
