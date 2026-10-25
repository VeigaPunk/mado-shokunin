# RevTrendExpansion — attack on the round-30 expansion verdict

Item: attack the expansion trend verdict (report only). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. All measurements read committed bytes at
named revisions.

**Revision note.** This file supersedes my first pass, which commit `274f735` committed as
`w1/reports/RevTrendExpansion.md` and integrated (capability-row correction, lesson
"w1 addendum part 3"). Findings below are re-pinned to the current lane tip `274f735`; F2 from
that draft is now verified **resolved**, and F1 is amended with the round-19 control, which the
integrated lesson does not address.

**Verdict returned.**
`improved — narrow, capability-only` is **admissible only as an explicitly named contract
reading**, and the record has taken it (`corpus/lessons/round-30.md`, w1 addendum part 3). The
honest verdict under the contract as written is **`unchanged`**: `LEARNING.md:33`'s `improved`
cell requires net new admitted entries (round 30: zero), `LEARNING.md:88`/`AXES.md:66-73` scope
capability growth to a saturated lane (round 30 is not saturated), and the lane's round-19
control reported `unchanged` for a demonstrated capability row with no new entry. If the closure
keeps capability-only `improved`, it should record that it is superseding that practice, with
the reason — not call it an application of the existing rule.

---

## 0. The verdict under attack (current committed state)

| Where | Text |
|---|---|
| fleet report `.ufo/reports/round-30/mado.md:123-126` (fleet `bbae16bf`, erratum `31bb8e9`) | "**expansion — improved**: a new capability enters the table … one own-work registry row added. No new `corpus/knowledge/` entry — bounded to the capability + the index rows." — **still the three-legged version**; no fleet erratum corrects the bullet |
| non-author spot-check `corpus/lessons/round-30-verifier-spotcheck.md:81-83` (`d72243e`) | "**expansion — improved:** one new capability row … plus one own-work registry row" |
| lane correction, `corpus/lessons/round-30.md` w1 addendum part 3 (`274f735`) | three-legged verdict declared padded; "Corrected reading (capability-inclusive, adopted): **expansion — improved, narrow, capability-only** … this is the lane's first capability-only expansion verdict … The strict entries-only reading would be `unchanged`" |
| capability record `SCORECARD.md:1922-1923` (`274f735`) | original row + "corrected scope" row: new surfaces = `--root`, symlink/refusal, `--selftest`, setup-error exit 2, exit contract; evidence `c3-repair-d72243e.txt` |

Contract text applied: `LEARNING.md:33` (expansion row), `LEARNING.md:85-88` (axis relation,
capability route scoped to saturation), `AXES.md:57-64` (capability table), `AXES.md:66-73`
(stagnation nudge).

## 1. What I reproduced independently (committed bytes)

| Check | Result |
|---|---|
| capability row exists, distinct identity | yes — `SCORECARD.md:1918-1923` at `274f735`; the 18th real row across the `Capabilities` tables (17 prior: gate, tripwire, resolver, mutation, assessment families); no prior row covers index completeness/navigation; no duplicate entry |
| gate red at base, green at tip (pre-repair) | `git show 451e8b3c:quality/check-index.py` (sha256 `fc4a10a2…`, git blob `df01b20f…`): `--rev 8f51071b` → `indexed=41/43 missing=2 … coverage=9.5349/10` exit 1, missing exactly the two notes; `--rev 446dc396` → `indexed=43/43` exit 0; `--selftest` → `6/6`, exit 0. Byte-identical to `evidence/c3-after-446dc396.txt` / `controls/C3K1-base-red.txt`. |
| gate red at base, green at tip (current gate) | `git show 274f735:quality/check-index.py` (sha256 `51b513f5…`): `--selftest` → `9/9`; base `8f51071b` red `41/43`; `446dc396` and `274f735` green `43/43`; bare invocation `SETUP_ERROR … exit 2`. Matches `evidence/c3-repair-d72243e.txt` (gate sha256 `51b513f5…`, `9/9`). |
| no new `knowledge/` entry | confirmed — `git diff --stat 8f51071b 274f735 -- corpus/knowledge/` empty; note count 43 → 43 |
| no frontier / province move | `git diff --stat 8f51071b 274f735 -- PROVINCE.md SKILL.md tools/` empty; `corpus/README.md` §Frontier unchanged |
| S185 anchor | block body + trailing newline of the `SCORECARD.md` counting-command fence hashes to `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` — exact; `used-by` paths exist; no other SOURCES row pins this fence (not a duplicate row) |
| source kinds at tip | `code 87, docs 68, spec 12, own-work 10, community 4, paper 2, dataset 1, book 1`; own-work before S185: S001, S002, S014, S015, S019, S041, S044, S049, S055 (9) |
| S185 lesson quote | `git show 446dc39:SCORECARD.md \| grep -c 'indexed=$covered'` → 0; the block prints `indexed={covered}/{len(notes)}` → the quote at `round-30.md:24` is **not verbatim** |
| r19 control | `SCORECARD.md:1159-1163` enters capability `landedness check` (first-working round 19, T1–T9 matrix); round-19 report `.ufo/reports/round-19/mado.md` Trend verdicts: "**expansion: unchanged.** No new knowledge entry on uncovered ground; three new rows harden existing routes." |

**Answer to "did C3's gate enter the capabilities table with a real demonstration (red at base,
green at tip)?" — yes.** The row exists, the demonstration reproduces at the pre-repair
(`451e8b3c`), repair (`15ddd7d`) and current (`274f735`) bytes, and the carrier `AXES.md:62-64`
requires ("in the round report") exists in the fleet report (`bbae16bf`, C3 section). The
capability leg is real; the verdict leg is the attack surface.

## 2. Findings (severity order)

### F1 — High — capability-only `improved` is a practice change presented as an application of the rule

The lesson's part-3 correction does the right thing procedurally — it names the reading and
records the strict alternative — but its justification is incomplete in two ways the closure
should resolve before the round closes:

1. **The contrary control is missing.** Round 19 entered a demonstrated capability row
   (`landedness check`) plus three source rows and **no** new knowledge entry, and the round's
   recorded verdict was `expansion: unchanged` for exactly that reason (r19 report, Trend
   verdicts). The lesson's "this is the lane's first capability-only expansion verdict" is true
   only for *claimed* verdicts; as *observed practice* r19 is the first instance and it says
   unchanged. The correction must either name r19 and state why it is superseded, or drop to
   `unchanged`. (r19's capability was incidental, not a declared expansion claim — that is a
   reason the practice is thin, not a reason it does not exist.)
2. **The saturation scope is not addressed.** `LEARNING.md:88` places the capabilities-table
   route under "when the quality axes saturate", and `AXES.md:66-73` makes the capability move
   the saturated-lane remedy. Round 30 is not saturated: lowest axis 7.949/10 (resolved-active
   0.7949) against a 9.0 line. So the one contract clause that authorizes capability growth is
   not triggered, and the fallback is the `improved` cell's entries test — zero.

Everything else the correction says is right: the two extra supports are non-expansion
(registry row: r21 "Source growth alone is not expansion", r29 `+S184` → unchanged; index rows:
`registration.md:41` "no new domain claim admitted", and the notes were already booked as
r27/r28 expansion — r27 "new measured surface … +5 new A-tier", r28 "new admitted surface on
uncovered ground" — so crediting C1 would double-count). The fleet report bullet
(`mado.md:123-126`) still carries the three-legged version; the lesson correction is the only
place the reading is named. An erratum line in the fleet report would keep the round's primary
record from contradicting its lesson.

Effective outcome to record: **either** `expansion: unchanged` (contract as written), **or**
`improved` with an explicit note that the lane is superseding its r19 practice and that the
round is outside the saturation clause — a fleet-contract reading, not a per-round verdict
choice.

### F2 — Resolved — capability scope corrected and evidence pointer re-pointed (verified)

My first-pass F2 (row overstated novelty; pointer named the pre-repair blob) is fixed at
`274f735`: `SCORECARD.md:1923` appends the corrected scope (plain-tree mode, symlink/refusal,
`--selftest`, setup-error exit 2, lane-owned exit contract; revision scoring pre-existed) and
points at `evidence/c3-repair-d72243e.txt`. I verified that receipt's numbers against committed
bytes: gate sha256 `51b513f5…`, `9/9` selftest, base `8f51071b` red `41/43`, `446dc396` and
`d72243e` green `43/43`, bare invocation exit 2. The original demonstration receipt stays as
the pre-repair record, as the erratum says. No residual action.

### F3 — Low — S185 is neither "a new kind of source" nor registry noise; it carries zero expansion weight

- Not a new kind: `own-work` is an existing kind with 9 prior rows (§1); "new kinds of source"
  is unmet.
- Not noise: unique identity (no prior SOURCES row pins the fence), exact content anchor
  (block sha verified), live consumers (`quality/check-index.py`, `registration.md`), correct
  `mined` status. Contract-valid registry provenance.
- Its anti-circularity risk is already routed (`round-30.md:68`, "own-work sourcing has no
  anti-circularity guard; 3 formality defects") — sourcing formality, distinct from expansion
  weight.
- The verbatim-quote requirement is unmet (`registration.md:104`; the quote at `round-30.md:24`
  renders `$covered/$total`, which appears nowhere in the block). Already routed by the
  spot-check; independently confirmed. The exact block sha means the source really was opened
  and pinned — a formality defect, not a false anchor.

### F4 — What would make `improved` uncontroversial (route map, not a defect)

- **Entry route (open now):** one admitted `corpus/knowledge/` entry on ground the coverage map
  does not hold, `source:` citing a `mined` row, indexed — e.g. a note distilling
  index-completeness semantics and own-work provenance limits, which would also give S185 a
  knowledge consumer instead of only a gate.
- **Contract route (needs to be named):** amend `LEARNING.md:88` / `AXES.md:66-73` so a
  capability row counts for expansion outside saturation, and record r19 as superseded
  precedent. Then capability-only `improved` is an application of the rule, not an exception to
  it.
- Until either, the capability stays in the table exactly as `AXES.md:57-64` requires; only the
  trend credit is in question.

## 3. Residual risk

- The current gate filters `ls-tree` to blob entries and NUL-parses names (`quotepath=off`);
  the fence's `--name-only` would treat a directory named `*.md` as a candidate note. Gate is
  stricter (safe direction), latent (no subdirectories in `corpus/knowledge/`).
- The corrected-scope row (`SCORECARD.md:1923`) is an errata row inside the round-30
  capabilities table; any future population counter that enumerates rows under `Capabilities`
  headings would read it as a second identity (19 rows, one capability). Harmless today (the
  round-24 12-row population is a frozen historical set), but a re-demonstration sweep should
  skip it by name.
- The capability is not on the round's scoring path (C1 is still scored by the fence) and is
  not wired into `tools/mado-verify.sh --selftest`; already routed by the spot-check/erratum.
- Both the author record and the non-author spot-check adopt `improved`; my finding disagrees
  with the *basis*, not with the capability's reality. The decision belongs to the closure.
- Live worktree churn during review: `quality/check-index.py` was rewritten in the worktree and
  restored mid-review; `quality/q36-successor-receipts.txt` was regenerated with ephemeral
  paths (reverted in `15ddd7d`, recorded in the erratum). Committed bytes unaffected; every
  finding here is measured on committed revisions.

## 4. Verification gaps

- I did not read all 24 w1 seat reports end-to-end; I re-derived every claim I rely on from
  committed bytes (including reproducing the pre-repair gate divergence class before the repair
  landed and re-running each repaired gate revision).
- The fleet report lives outside the lane repo's commit graph; I verified its expansion bullet
  at committed fleet revisions `bbae16bf` and `31bb8e9` (unchanged between them).
- No `tools/mado-verify.sh --selftest` run (not an expansion input; harm watch receipted
  460/460 in the round records).
- Census W04 warning adjudication not re-opened (not expansion scope; covered by the spot-check
  and `ExecCensusRerun`).
- I did not audit rounds 12–14/22–23 line-by-line for a zero-entry expansion-improved round;
  the two candidates that could have been were checked directly (r19 control; r20, which did
  add `corpus/knowledge/tripwire-precision-r20.md` in `4362219`).

No edits to lane corpus, gate, counters, or registry were made by this seat.
