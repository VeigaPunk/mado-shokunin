# RevTrendExpansion — attack on the round-30 expansion verdict

Item: attack the expansion trend verdict (report only). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. All measurements read committed bytes
at named revisions. The lane tip moved during review (`92d3c86` → `d72243e` → `15ddd7d`);
every finding is re-pinned to `15ddd7d` unless a revision is stated.

**Verdict returned:** `improved — narrow, capability-only` is the best-supported verdict
**only after** the corrections in F1/F2; the verdict **as recorded** is overclaimed
(three stated supports, one of which clears the bar). Under a literal reading of
`LEARNING.md:33`'s `improved` cell (entries only), the honest verdict is **unchanged**.
Decision rule in F4.

---

## 0. The verdict under attack

| Where | Text |
|---|---|
| fleet report `.ufo/reports/round-30/mado.md:123-126` (fleet commits `bbae16bf`, erratum `31bb8e9`; bullet unchanged by the erratum — verified `git show 31bb8e9:… \| grep`) | "**expansion — improved**: a new capability enters the table … one own-work registry row added. No new `corpus/knowledge/` entry — bounded to the capability + the index rows." |
| non-author spot-check `corpus/lessons/round-30-verifier-spotcheck.md:81-83` (`d72243e`) | "**expansion — improved:** one new capability row … plus one own-work registry row" |
| lane capability record `SCORECARD.md:1918-1922` (`15ddd7d`) | capability row `index-completeness gate` … "at any committed revision or tree" … evidence `c3-after-446dc396.txt`, "selftest 6/6" |

Contract text being applied: `LEARNING.md:33` (expansion row: observable / `improved when` /
`harmed when`), `LEARNING.md:85-88` (axis relation + capabilities route),
`AXES.md:57-64` (capability table entry rule), `AXES.md:66-73` (stagnation nudge).

## 1. What I reproduced independently (committed bytes)

| Check | Result |
|---|---|
| capability row exists in the capabilities table | yes — `SCORECARD.md:1918-1922` at `15ddd7d`; the 18th real row across the `Capabilities` tables (17 prior: gate, tripwire, resolver, mutation, assessment families) and **no prior row covers index completeness/navigation** — distinct identity, not a duplicate entry |
| gate red at base, green at tip (pre-repair) | `git show 451e8b3c:quality/check-index.py` (sha256 `fc4a10a2…`, git blob `df01b20f…`): `--rev 8f51071b` → `indexed=41/43 missing=2 … coverage=9.5349/10` exit 1, missing exactly the two notes; `--rev 446dc396` → `indexed=43/43` exit 0; `--selftest` → `6/6`, exit 0. Byte-identical to `evidence/c3-after-446dc396.txt` and `controls/C3K1-base-red.txt`. |
| gate red at base, green at tip (post-repair) | `git show 15ddd7d:quality/check-index.py` (sha256 `373680fe…`): `8/8`; base `8f51071b` red; `446dc396` and `d72243e` green; bare invocation `SETUP_ERROR … exit 2`; a double-space index row is now **red** (fence-faithful). Byte-identical to `evidence/c3-repair-d72243e.txt`. |
| "no new `knowledge/` entry" | confirmed — `git diff --stat 8f51071b 15ddd7d -- corpus/knowledge/` empty; note count 43 → 43 |
| no frontier / province move | `git diff --stat 8f51071b 15ddd7d -- PROVINCE.md SKILL.md tools/` empty; `corpus/README.md` §Frontier unchanged |
| S185 anchor | block body + trailing newline of the `SCORECARD.md` counting-command fence hashes to `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` — exact; `used-by` paths exist; no other SOURCES row pins this fence (not a duplicate row) |
| source kinds at tip | `code 87, docs 68, spec 12, own-work 10, community 4, paper 2, dataset 1, book 1`; own-work before S185: S001, S002, S014, S015, S019, S041, S044, S049, S055 (9) |
| S185 lesson quote | `git show 446dc39:SCORECARD.md \| grep -c 'indexed=$covered'` → 0; the block prints `indexed={covered}/{len(notes)}` → the quote at `round-30.md:24` is **not verbatim** |

So the answer to "did C3's gate enter the capabilities table with a real demonstration?" is
**yes**: the row exists, the red-at-base/green-at-tip demonstration is real and reproduces
at both the pre-repair and post-repair bytes, and the demonstration carrier required by
`AXES.md:62-64` ("in the round report") exists in the fleet report (`bbae16bf`, C3 section).
The C3 capability leg is sound; the attack lands on the *rest* of the verdict.

## 2. Findings (severity order)

### F1 — Medium — two of the three stated supports are not expansion (r21/r29 precedent)

`mado.md:125-126` lists (a) "one own-work registry row added" and (b) "bounded to the
capability + the index rows" inside the expansion-improved bullet; the spot-check repeats (a)
at `round-30-verifier-spotcheck.md:82`. Neither is expansion under the lane's own settled rule:

- **Registry row.** The `improved` cell is "net new admitted entries on uncovered ground"; a
  SOURCES row is not an entry. `LOG.md:1447` (r21) and the r21 report (`expansion — unchanged…
  Source growth alone is not expansion`) and the r29 report (`+S184 but no new admitted … →
  unchanged`) both refuse source-row growth as expansion. S185 is additionally the *same kind*
  as 9 prior rows (§1), so it also fails the "new kinds of source" observable.
- **Index rows.** The registration says the rows admit no new claim
  (`registration.md:41`, "no new domain claim admitted"). The two notes were admitted in
  rounds 27/28 and those rounds already booked them as expansion (r27 report: "new measured
  surface … +5 new A-tier"; r28 report: "new admitted surface on uncovered ground"). Using
  C1's index repair as r30 expansion would double-count r27/r28 expansions.

Effect: the verdict survives on one leg, not three; the r29 lesson's own distinction
(navigation repair ≠ new ground) is being blurred in the verdict prose.

### F2 — Medium — capability novelty overstated; evidence pointer now names a superseded blob

`SCORECARD.md:1922` says the gate scores "at any committed revision or tree". Revision-mode
scoring pre-existed: `SCORECARD.md:236` documents the fence being run "via `bash -s`,
`REV=<commit>`" since fleet round 1, and C1's own counting command for this round is still the
fence, not the gate. The genuinely new surface is: plain-tree mode, symlink refusal,
`--selftest`, setup-error semantics, and a lane-owned exit-code contract. Without that
restatement the row claims a capability half of which the lane already had.

Separately, after the same-round repair (`15ddd7d`) the capability's committed bytes are the
repaired gate (sha256 `373680fe…`, `8/8`, receipt `c3-repair-d72243e.txt`), while the row still
points at the pre-repair demonstration (`c3-after-446dc396.txt`, "selftest 6/6", gate blob
`df01b20f…`). The append-only erratum (`SCORECARD.md` round-30 w1 erratum; fleet report
erratum at `31bb8e9`) records the repair but does not re-point the capability row. A reader of
the table alone reads the capability as the old blob.

### F3 — Low — S185 is neither "a new kind of source" nor registry noise; it carries zero expansion weight

- Not a new kind: `own-work` is the fourth-largest existing kind (9 prior rows, §1); the
  observable "new kinds of source" is unmet.
- Not noise: unique identity (no prior SOURCES row pins the fence), exact content anchor
  (sha verified), live consumers (`quality/check-index.py`, `registration.md`), correct
  `mined` status. The row is contract-valid registry provenance.
- It does not make expansion improved, and the anti-circularity concern is already routed
  (`round-30.md:68`, "own-work sourcing has no anti-circularity guard; 3 formality defects") —
  that is a sourcing-formality defect, distinct from expansion weight.
- The verbatim-quote requirement is unmet (`registration.md:104`; quote at `round-30.md:24`
  is a schematic rendering). Already routed by the spot-check; independently confirmed in §1.
  The exact block sha means the source really was opened and pinned, so this does not weaken
  the anchor — only the quote formality.

### F4 — Judgment — capability-only is a first-of-kind reading; name it or take `unchanged`

Facts on the table:

- `LEARNING.md:33` `improved when`: "net new admitted entries on uncovered ground, each citing
  its coverage-map row" → round 30 = **0 entries**. Strictly, the cell is unsatisfied.
- The observable column of the same row includes "a capability admitted to `SCORECARD.md`", and
  the lane's verdict vocabulary treats an admitted capability as expansion ground
  (`LOG.md:1447` "no new admitted province ground/capability"; `LOG.md:1529` "no province
  frontier or admitted recovered capability"; r16 report "one … demonstrated finite
  capability"; r20 report "two capability rows").
- But **every prior expansion-improved round also added at least one knowledge entry**
  (r16: U7 route note; r20: `tripwire-precision-r20.md`, added in `4362219`, present in its
  "improved" round's data commit; r27/r28: their notes; r17/r18: their notes). Round 30 is the
  **first capability-only expansion-improved claim**, and it is made in a **non-saturated**
  round (lowest axis 7.949/10 — resolved-active 0.7949 — below the 9.0 saturation line),
  i.e. outside the regime where `LEARNING.md:88`
  and `AXES.md:66-73` send growth through the capabilities table.

Decision rule I recommend the closure apply explicitly:

- **Capability-inclusive reading** (observable column + `LOG.md:1447/1529` vocabulary +
  `AXES.md` capability table): `expansion: improved`, **narrow, capability-only** — provided
  `mado.md:125-126`, the spot-check line, and the SCORECARD row are corrected per F1/F2, and
  the lesson records that this is the lane's first capability-only expansion verdict (a
  reading of `LEARNING.md:33`, not a self-evident application).
- **Strict reading** (the `improved` cell's entries-only text, plus `LEARNING.md:85`
  "Expansion is served by `coverage` and `adjacency`" while C3 is registered under
  *operability*): `expansion: unchanged` — the capability stays a repertoire row (it is
  legitimately in the table under `AXES.md:57-64`) without trend credit.

What is *not* honest is the recorded position: it takes the capability-inclusive reading while
padding it with two supports the lane itself has ruled non-expansion. The record should pick
one reading and state it.

## 3. Residual risk

- The repaired gate filters `ls-tree` to blob entries and NUL-parses names; the fence's
  `--name-only` would treat a directory named `*.md` as a candidate note. Gate is stricter
  (safe direction), latent (no subdirectories in `corpus/knowledge/`).
- The capability is not on the round's scoring path (C1 is still scored by the fence) and is
  not wired into `tools/mado-verify.sh --selftest`; the wiring gap is already routed by the
  spot-check and the erratum.
- r21/r29-style "rows alone" language survives in r20's verdict prose; if the closure adopts
  the capability-inclusive reading, it should not also revive source-row counting.
- Live worktree churn observed mid-review: `quality/check-index.py` was rewritten in the
  worktree at 04:09 (then restored) and `quality/q36-successor-receipts.txt` was regenerated
  with ephemeral paths (reverted in `15ddd7d`; recorded in the erratum). Committed bytes were
  unaffected; all findings here are on committed bytes.

## 4. Verification gaps

- I did not read all 24 w1 seat reports end-to-end; I read RevC1Fence's live message, the L1
  w1 addendum, and re-derived every claim I rely on from committed bytes (including the gate
  divergence class, which I reproduced against the pre-repair blob before the repair landed).
- The fleet report is outside the lane repo's commit graph; I verified its expansion bullet at
  the committed fleet revision `31bb8e9` (unchanged from `bbae16bf`).
- No `tools/mado-verify.sh --selftest` run (not an expansion input; harm watch already
  receipted at 460/460 in the round records).
- Census W04 warning adjudication not re-opened (not expansion-scope; the spot-check and
  `ExecCensusRerun` cover it).

No edits to lane corpus, gate, counters, or registry were made by this seat.
