# ScrTrendEvidence — round-44 trend evidence table (draft)

Seat `w2/ScrTrendEvidence` (scribe). Task: draft the round's **expansion / quality / discernment** verdict
candidates from `LEARNING.md` and the committed round-44 bytes, with a pointer for every statement. This is a
draft for the L1 and for the non-author closure: it issues no verdict of its own where the protocol assigns the
decision elsewhere.

- Lane `mado-shokunin`; base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`; data `e46789213830597348fe96a351ae004d10587385`;
  tip at my read `290cddea` (w2 spec/dispatch commit).
- Rule set: `LEARNING.md:26-29` (vocabulary; "no trend is a scalar"), `:33` expansion row, `:34` quality row,
  `:35` discernment row, `:37-38` ("Growth without quality is not learning"), `:40-46` (outside spot-check;
  "A subagent the lane dispatched is still the lane").
- Every locator below is emitted by `grep -n`/`git` in `.ufo/waves/round-44/w2/ScrTrendEvidence/verify-pointers.sh`
  and recorded in `.ufo/waves/round-44/w2/ScrTrendEvidence/pointers.txt`: **85 checks, 0 miss,
  `PTRCHECK verdict=PASS`** (last line). Tracked-file line numbers are the tip worktree `290cddea`; the
  `README_base.txt` pointers are a byte copy of `git show 6a1a905:corpus/README.md` made by that script.
- I re-ran no counter, control, census or compositor read. The counters' own committed receipts are the only
  evidence for those lines (§7).

---

## 1. Expansion — candidate: **`improved`** (supported)

`LEARNING.md:33` improved leg: "net new admitted entries on uncovered ground, each `source:` citing a `mined`
`corpus/SOURCES.md` row (own-work rows included); frontier areas entered; … a capability admitted to
`SCORECARD.md`".

| # | observable (LEARNING:33) | evidence pointer | read |
|---|---|---|---|
| E1 | net **+1** admitted lane entry | `corpus/README.md:72` (index row `MADO-R44-1` names the entry); index rows 60 at base → 61 at data (`pointers.txt` `CNT index_rows base=60 data=61`); the data commit's only knowledge change is `A corpus/knowledge/hyprland-gkeep-size-request-r44.md` (`pointers.txt` `CNT knowledge_diff`) | holds |
| E2 | the ground was **not** held at base | `receipts/c2-ground-base.txt:1-2` (`git grep -ciE 'sendWindowSize\|pendingSizeAcks\|xdg_toplevel.configure\|set_size_request' 6a1a905 …` → `exit=1`); `receipts/c2-v2-before-base.txt:2` (`admitted=0/1 verdict=TARGET_MISSED rev=6a1a905…`); independent scout sweep `.ufo/waves/round-44/w1/ScoutCoverage.md:3` (zero hits across `corpus/knowledge`, `PROVINCE.md`, `SKILL.md`, `tools`) | holds |
| E3 | each `source:` cites a `mined` SOURCES row | five source lines in the entry (`src_lines=5`); `receipts/c2-after-data.txt:1-5` — five `clause=c` rows, all `status=mined used=1 ok=1` (`c2_c_rows=5`, `c2_c_s301` = `:5`); registry rows `corpus/SOURCES.md:247` (S298), `:248` (S299), `:249` (S300), `:250` (S301), and held `:176` (S164) all carry the entry in `used-by` | holds |
| E4 | coverage map now holds it; **frontier area entered** | index row `corpus/README.md:72`; Frontier subsection `corpus/README.md:304` ("Round-44 gkeep size-request route"), detail `:314`; the base frontier named this exact gap — "the client's acknowledgement path" (`README_base.txt:301`, same sentence names the other still-open items) | holds |
| E5 | a **capability admitted** | `SCORECARD.md:2575` ("Capabilities (round 44)"), row `:2579` (state-aware rule size vs reported size join, first-working round 44) | holds |
| E6 | the claim's countable after-state at the data commit | `receipts/c2-after-data.txt:29` (`admitted=1/1 verdict=TARGET_MET`), `:30` (`exit=0`) | holds (bookkeeping; see §2 caveat Q6) |

Caveats that belong in the verdict's reasons (none removes E1-E5):

1. **The entry is an assimilation successor, not a lane-discovered topic.** Its `assimilated-from:` line names the
   package text `gkeep-client-size-request-r12.md` (`corpus/knowledge/hyprland-gkeep-size-request-r44.md:12`), and
   three of that text's sentences are corrected rather than adopted (`:64`, bullets `:69`, `:71`, `:73`).
   `LEARNING.md:33` admits own-work rows, and the lane's count did move 60 → 61, so E1 stands; a reader who
   treats package text as "already held" would read the round as deepening instead of expansion — that is a
   non-author call (§6.1).
2. **w1's sizing finding.** `.ufo/waves/round-44/w1/CritClaimSizing.md:26` (F3): the ground "is legitimate" but
   the after-state that was counted is *admission*, and 3 of the entry's 6 elements already sat verbatim in the
   staged file. This bounds the *breadth* of the expansion, not its occurrence.
3. **C1 earns no coverage credit.** `.ufo/waves/round-44/w1/ScoutCoverage.md:5`: "C1: no coverage credit
   (operability)" — the operability claim is not part of this trend (it is the operability axis; `SCORECARD.md`
   row `:2579` is a capability admission, E5, not a knowledge entry).

Result: **expansion candidate `improved`**; the one thing a non-author must decide is whether a successor of
package text counts as a "net new admitted entry" or only as deepening (§6.1).

---

## 2. Quality — candidates: **`unchanged`** (literal, primary) | `improved` (wider reading) | `harmed` (weakest)

`LEARNING.md:34` observable: "entries re-verified, deepened, or superseded by stronger ones; `verified-at`
freshness"; improved = "a weaker entry is superseded by a stronger one, or stale entries re-verify, with no
admitted entry failing its re-check"; harmed = "an entry is found false or stale and left unmarked".

| # | what actually moved | evidence pointer | read |
|---|---|---|---|
| Q1 | **no held `knowledge/` entry was edited** this round | `pointers.txt` `CNT knowledge_diff` = the one added path; nothing else under `corpus/knowledge/` | no entry re-verified, deepened or superseded in the literal sense |
| Q2 | the new entry is fresh | `corpus/knowledge/hyprland-gkeep-size-request-r44.md:8` (`verified-at: 2026-10-26`), `:9` (`recheck: 90d`); it is the only entry dated 2026-10-26 besides the round-43 entry | freshness of the *new* entry, not of a held one |
| Q3 | a held **source row** was re-verified byte-identically | `.ufo/waves/round-44/w1/CritAssimilation/id-receipts.txt:3` (fetch sha `d735d454…`) and `:4` (the tag copy at `v0.56.2` has the same sha); the digest is pinned in `receipts/fetch-sha256.txt` (8 digests) | source re-verification; the trend's observable says "entries", so this is adjacent evidence |
| Q4 | a **false published statement** was marked | `SKILL.md:276` still reads "the tiler, not the floating rule path, set its box"; `SKILL.md:289` says that "is false for a pseudo-tiled client", and `:291` narrows it ("read TILED as …"); M44-3 at `corpus/lessons/round-44.md:128` books it | the mark exists in the same file below the table (append-only house rule) — not "left unmarked" |
| Q5 | four **round-43 errata** were appended | `corpus/lessons/round-44.md:196` (errata head, E1-E4); the routed items at `:90` | record repair; lesson-level, not entry-level |
| Q6 | **what the counter verifies** | `receipts/c2-after-data.txt:29`; the declared residual (`.ufo/waves/round-44/registration-v2.md:64`: claim-to-quote binding "are the non-author reading") says the truth of the sentences is not what clause j tests | the re-check that passed is bookkeeping; it is not evidence that the entry's claims are the receipts' claims |
| Q7 | candidate **harmed** evidence (LOW) | two usage rows still describe the join without the state verdicts: `SKILL.md:158` and `SKILL.md:225` (both are the lines that point at `mado-geometry.py --clients -`), while the only `FULLSCREEN` occurrences in the file are `:280`, `:281`; flagged by the lane's own scout at `w1/ScoutCoverage.md:5` ("stale sentences … `SKILL.md:158,225`") | omission, not a falsehood — the rows are narrower than the shipped vocabulary |
| Q8 | candidate **harmed** evidence (LOW) | the round-43 entry still points at seat receipts that did not exist at its own data commit: `corpus/knowledge/hyprland-gkeep-geometry-r43.md:66` names `ExecOracleGkeep` files; `git ls-tree -r --name-only 1959770 .ufo/waves/round-43/w1/ExecOracleGkeep/` → 0 files at that revision vs 48 at the tip (`CNT execoracle r43data=0 tip=48`); M44-4 at `corpus/lessons/round-44.md:135`, captured-by at `:142` | marked in the lesson erratum, **not** in the entry |

Reading the three candidates:

- **`unchanged` (literal, primary).** No lane entry was re-verified, deepened or superseded (Q1); the new entry
  belongs to expansion; Q3/Q4/Q5 are source- and record-level moves. Nothing in the table's improved leg is met
  on entries.
- **`improved` (wider reading).** If "entries" is read as the lane's understanding surfaces (`SKILL.md`,
  lessons), Q4 + Q5 are a stale statement marked and a predecessor text superseded by a stronger one with three
  corrections listed (Q1's entry `:64`), with no admitted entry observed failing its re-check.
- **`harmed` (weakest).** Only if a non-author rules that (a) the un-updated usage rows (Q7) are "stale … left
  unmarked", or (b) an erratum in the round lesson does not mark the entry it corrects (Q8). Neither is settled
  by the committed bytes: Q7's rows are narrow, not wrong, and Q4's mark is in the same file as the claim.

**Discriminator for the L1/non-author:** does the quality observable range over `corpus/knowledge/` entries only
(→ `unchanged`) or over the lane's understanding surfaces (→ `improved`)? And does a lesson erratum count as the
mark for the entry it corrects (Q8)? If the answer to the second is "no" and Q7 is also ruled stale, the verdict
is `harmed` — and `LEARNING.md:37-38` then forces the round to be reported as a **trade**, not admitted.

---

## 3. Discernment — candidate: **not self-issuable**; `improved` iff the closure agrees, `harmed` if a disagreement is left unlearned

`LEARNING.md:35` + `:40-46`: the trend is read off "gate decisions vs the outside spot-check" and the
`QUALITY.md` criteria, with **at least one admit and one reject** spot-checked by a non-author and
`agree`/`disagree` recorded in the round's lesson.

| # | state at the data commit | evidence pointer | read |
|---|---|---|---|
| D1 | the round's own outside check **has not run** | `corpus/lessons/round-44.md:215` is a header "Spot-check (non-author closure; placeholders)" whose expected cells are four literal `(closure)` placeholders (`spot_placeholders=4`); no `corpus/lessons/round-44-verifier-spotcheck.md` exists (`round44_verifier_file present=0`) | the lane cannot attest its own discernment |
| D2 | decisions a non-author can sample | `corpus/lessons/round-44.md:36` (`ADMIT` the r12 successor), `:37`, `:38`, `:39`, `:40` (four `REFUSE`, `refuses=4`); the ledger continues with "no new decision" rows | sample exists, verdict pending |
| D3 | three `QUALITY.md` criteria landed, each citing a lesson | `corpus/QUALITY.md:411` (82 → `## considerthese`, `corpus/lessons/round-44.md:248`), `:413` (83 → M44-4 `:135` + round-43 closure D4), `:415` (84 → M44-8 `:178`) | the "criterion with no lesson behind it" harm condition is **not** met on the text |
| D4 | one literal instance of the improved leg ("a disagreement becomes … a grounded criterion") | round-43's **non-author** closure disagreement D4 (the closure's own spot-check table is `corpus/lessons/round-43-verifier-spotcheck.md:70`; its trend verdicts at `:84`-`:90`; routed at `corpus/lessons/round-44.md:90`, booked as M44-4 `:135`, captured at `:142`) → criterion 83 (`corpus/QUALITY.md:413`), with an able-to-fail check named in the criterion | the disagreement was **last** round's outside check, landed as a criterion this round |
| D5 | the other two criteria do not have an outside disagreement behind them | 82 is the `considerthese` proposal (`:411`, operator-side reflection, not a gate disagreement); 84's mistake M44-8 records `Captured-by: **none** for four rounds` (`corpus/lessons/round-44.md:183`) — it was found by a lane-dispatched critic, and `LEARNING.md:46` says that is still the lane | bar sharpened; not outside-agreement evidence |
| D6 | no round-44 self-attestation | neither `expansion` nor `discernment` appears anywhere in the round lesson (`trend_words got=0`) | the lesson correctly leaves the verdict to the closure |

Candidate readings:

- **`improved`** — the closure's spot-check agrees on the sampled admit and reject **and** the criterion leg
  counts (D3, D4). This is the only `improved` route the committed bytes support, and it needs the closure's
  agree rows: D1 is empty.
- **`unchanged`** — if the closure considers a carried-over disagreement (D4) an improvement of round 43 and not
  of round 44, and no round-44 sample is taken.
- **`harmed`** — if the closure disagrees with a gate decision and that disagreement adds no lesson/criterion.

**Do not write `improved` from the lane side**: D1's placeholders are the committed proof that no outside check
exists yet.

---

## 4. Cross-trend interaction and the prior baseline

`LEARNING.md:37-38`: "`expansion: improved` with `quality: harmed` is a trade, reported as a trade, never
admitted." So the three candidates are not independent: if quality lands `harmed` (§2), the expansion candidate
must be reported as a trade even though E1-E5 hold.

Prior round for continuity (not evidence for this one): round-43's non-author closure recorded
`expansion: improved` (`corpus/lessons/round-43-verifier-spotcheck.md:86`), `quality: improved` (`:88`) and
`discernment: improved` (`:90`). Round 43's quality reading ("C2 instrument tightened before data; … every w2
content finding … corrected") is the precedent for the wider reading of §2's observable; round 43's discernment
reading rested on a spot-check the round-44 lesson has not yet received (§3 D1).

---

## 5. What only a non-author can decide

1. **§1 caveat 1 against `LEARNING.md:33`:** is an assimilation successor of package text a "net new admitted entry on
   uncovered ground" (expansion `improved`), or a deepening whose entry count is bookkeeping?
2. **§2 discriminator:** the scope of "entries" for the quality trend (`knowledge/` only vs understanding
   surfaces), and whether a lesson erratum marks the entry it corrects (Q8).
3. **§3 D1:** the round's own spot-check — at least one admit (`corpus/lessons/round-44.md:36`) and one reject
   (`:37`-`:40`), with `agree`/`disagree` and a reason recorded in the round lesson, before any discernment
   verdict.
4. **§3 D4 vs D5:** whether the round-43-carried disagreement → criterion 83 counts toward round 44's
   discernment.
5. **§2 Q6:** whether the bookkeeping-only admission (declared residual) is enough to say "no admitted entry
   failed its re-check" — the counter cannot speak to the entry's claim truth.

---

## 6. Not evidence (unrun by this seat)

- The counters, controls, census, axis check and the live compositor read were **not re-run**: their lines are
  quoted from the committed receipts only (`receipts/c1-after-data.txt:53-54`,
  `receipts/c2-after-data.txt:29-30`, `receipts/ctl-c1-v2.txt:23`, `receipts/ctl-c2-v2.txt:13`,
  `receipts/axis-data.txt:4`, `receipts/census-after-data.txt:9`). No `hyprctl` call was made; no package
  transaction; no tool installed.
- The pointer script is the only execution: `grep -n`, `git show/log/ls-tree/diff`, `wc`. The receipt is the
  last run (85 checks, all `OK`, `PTRCHECK verdict=PASS`).
- A "no harm" verdict is not mine to give: `.ufo/waves/round-44/w1/ExecHarmBase.md:108` records that the
  no-harm comparison belongs to the integrating seat, and that file is only the base side.

## 7. Artifacts

- This report: `.ufo/waves/round-44/w2/ScrTrendEvidence.md`
- Pointer receipt: `.ufo/waves/round-44/w2/ScrTrendEvidence/pointers.txt` (85 checks, PASS)
- Pointer script: `.ufo/waves/round-44/w2/ScrTrendEvidence/verify-pointers.sh`
- Base README copy used by the script: `.ufo/waves/round-44/w2/ScrTrendEvidence/README_base.txt`
- Scratch: none used beyond the seat dir (the `/fast/scratch/hyaku/mado-r44/ScrTrendEvidence/` directory created
  at start was removed before this report; nothing citable lived there).
