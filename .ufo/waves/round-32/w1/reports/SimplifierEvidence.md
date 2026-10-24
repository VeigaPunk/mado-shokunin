# SimplifierEvidence — minimal committed evidence set for round 32 (proposal only)

Seat: simplifier · 2026-10-24 · lane tip `50e6a8f` (full: `git -C . rev-parse master` at write time).
Inputs: `corpus/QUALITY.md` (active criteria 1–54), `corpus/lessons/round-30.md`,
`.ufo/waves/round-32/registration.md`, `.ufo/waves/round-32/w1-spec.json` (all 32
seat items), on-disk wave state at the tip (file list in the log). **Nothing
deleted, moved or rewritten — proposal only.**

Counters smoked read-only at the tip while writing this (both verbatim below in
§1/§2): C1 frozen counter → `entries=0 rows=0 cited_entries=0` (pre-landing);
`python3 -I quality/check-axis-scores.py --rev 50e6a8f… --repo .` →
`MADO_AXIS: checked=3 mismatched=2` (navigation MATCH; calibration 39/40 vs 41/41
STALE; operability 9/9 vs 12/12 STALE). The C2 gate bites; the C1 counter is live.

## 0. Verdict

Twelve committed artifacts carry the whole round's evidence (§1–§4; five of them
already exist). Eight groups of wave byproducts are discardable (§5). Four
ordering/hygiene risks need action before the append (§6). All seat reports stay
committed — they are the non-author verification evidence (criterion 12); the
length problem is fixed by what the reports *embed*, not by dropping reports
(§6.4).

## 1. (a) C1 — counter and do-nothing controls

| # | path | holds | produced by |
|---|------|-------|-------------|
| A1 | `.ufo/waves/round-32/c1/controls/k1-do-nothing.txt` | The K1 receipt (registration mandates it; **does not exist yet**). Three blocks: (a) rows-only scratch copy → `entries=0 rows=5 cited_entries=0`; (b) entries-only copy → `entries=3 rows=0 cited_entries=0`; tip block appended after landing → `entries=3 rows=5 cited_entries=3`. Baseline at tip `50e6a8f` is `entries=0 rows=0 cited_entries=0` (measured 2026-10-24). Each block names the producer (`registration.md@<commit>`, the frozen inline counter), the copy's source rev and the date. | for each control: `git worktree add /tmp/k1-<mode> <rev>` (or `cp -a` of the two paths into a scratch root), `cd` there, run the registration's frozen counter verbatim, `; echo exit=$?` — output appended to the receipt; scratch copy deleted after |
| A2 | `w1/reports/CriticC1Predicate.md` (exists, uncommitted) | The counter's bypass evidence: v1–v3 junk trees reach `entries=3 rows=5 cited_entries=3`, v4 shows honest formatting rejected (`cited_entries=4`), verdict CLAIM DEAD, minimal repairs listed. This is the counter's able-to-fail record in the other direction — no separate receipt needed; the committed report is it. | already written by the critic seat |

Why one receipt file: registration says "A control receipt is committed under
`.ufo/waves/round-32/c1/controls/`" (singular); both one-sided controls plus the
tip triple in one file is the round-30 pattern (`evidence/c3-repair-d72243e.txt`:
base red + tips green + selftest). The do-nothing scratch trees themselves are
not evidence (criterion 13) — outputs are.

Honest-stop note: if the real data lands, the counter prints the target while A2
proves the instrument is shape-only. The evidence set must carry both facts;
predicate repair is routed, not done here (no narrowing after data).

## 2. (b) C2 — counter and control (c)

| # | path | holds | produced by |
|---|------|-------|-------------|
| B1 | `quality/check-axis-scores.py` | The C2 counter bytes — **untracked at the tip; commit before any receipt names it** (criterion 24: `tool_sha256=` must resolve via `git show <rev>:<tool>`). | already written; `git add quality/check-axis-scores.py` |
| B2 | `.ufo/waves/round-32/c2/controls/k2-controls.txt` | The K2 receipt (**does not exist yet**; `c2/controls/` currently holds only the critic's C1 attack trees). Legs: (a) stale r31 publication at tip rev → `MADO_AXIS: checked=3 mismatched=2` (smoked 2026-10-24, quoted above); (b) corrected-publication copy → `mismatched=0`; (c) perturbed copy (41/41→40/41, nothing else) → `mismatched=1` — the non-vacuity leg. Tip-green block (`mismatched=0`, exit 0) appended once the SCORECARD append lands. Every block: `tool_sha256=$(git show <rev>:quality/check-axis-scores.py | sha256sum)`, `measured_commit=`, `exit=`, date. | per leg: copy the lane (or flip the one cell in a scratch copy), `python3 -I quality/check-axis-scores.py --rev <rev> --repo <copy>; echo exit=$?` — capture the python exit directly, never through a pipe (a `sed` in my own smoke ate the exit code; the receipt must not) |

Leg (b) duplicates the tip-green verdict, but registration's K2 names it and it
costs three lines in the same command sequence — keep. Control (c) alone proves
non-vacuity; leg (a) proves the gate detects the actual stale publication, which
my smoke already confirms it does (`mismatched=2`, both non-navigation axes).

The C2 fix itself (append the re-derived axis table + correction-ledger entry)
is production edit, not wave artifact; its evidence is B2's tip-green block plus
the SCORECARD diff.

## 3. (c) item-10 gates

| # | path | holds | produced by |
|---|------|-------|-------------|
| C1 | `assimilation/{guard-proof-registry-fixture.md, guard-proof-staged-fixture.md, guard-proof-collisions-tolerant.txt, guard-proof-collisions-col0.txt, collisions.txt}` | The guard proof **already committed** at `b1b740d`/`50e6a8f`: indented `  | S002 |` fixture; tolerant extractor → collisions `S002` (non-empty); column-zero extractor → 0 bytes (false green); real run → `collisions.txt` empty (185 reg ids S001–S185 ∩ 132 staged S186–S317 = 0). | already run by ExecCollisionGuard |
| C2 | `w1/reports/ExecCollisionGuard.md` (committed at `50e6a8f`) | The guard's transcript and verdict (0 collisions, re-run rule if the registry moves before the append). | exists |
| C3 | `.ufo/waves/round-32/assimilation/census-validate.txt` | Validate-before-append receipt (**does not exist yet**): full `sources-census.sh validate` output on the scratch mirror + `exit=$?` (must be 0, warnings allowed) + `tool_sha256=$(sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh)` + sha of the mirrored `validate/corpus/SOURCES.md` + date. Run BEFORE the first append (registration item 4; criterion 34's absolute-path + tool-digest rule). | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file .ufo/waves/round-32/assimilation/validate/corpus/SOURCES.md; echo exit=$?` > census-validate.txt |
| C4 | `assimilation/quarantine-slice` (committed at `b1b740d`) + `w1/reports/ExecQuarantineSlice.md` (pending) | The derived expected row set (awk one-liner, filter-stable) and the per-row verdicts with fetched URLs/quotes. Class counts (`located`/`absent`/`unverifiable`) are copied as one line into the lesson `## Gate` — no separate receipt. | already / seat in flight |
| C5 | lesson `corpus/lessons/round-32.md` `## Gate` (lands with the round) | Item-2 admits/rejects with flip; item-3 stripped recheck prose (durable home — `assimilation/recheck-prose-stripped.md` is only its draft, see §5); quarantine counts; search-log note. | L1 integration |

## 4. (d) mistake fixes able to fail

| # | path | holds | produced by |
|---|------|-------|-------------|
| D1 | `.ufo/waves/round-32/evidence/fixes-redgreen.txt` | One section per `## Mistakes` fix in the round lesson: the failing-before command/fixture, its output at the pre-fix rev, the passing-after output at the post-fix rev, both revs named (pattern: `.ufo/waves/round-24/quality/m23-4-7-red-green.txt`, criterion 33's receipt). Lesson rows cite `fixes-redgreen.txt#<fix-id>` instead of inlining both runs — this is what keeps the lesson short. Already-shown-able-to-fail instruments reuse §1–§3 receipts; only *new* fixes append here. | per fix: run the named check at pre-fix rev (expect non-clean) and post-fix rev (expect clean), append both transcripts with rev + date |
| — | existing: `b1b740d` guard proof; A1 controls; B2 leg (c) | These three ARE able-to-fail proofs for this round's own instruments; no additional artifact. | — |

Anchor bytes (rides with (c)/(d)): commit `.ufo/waves/round-32/fetch/S{186,187,188,189,196}.bin`.
The re-grounding leg depends on fetched bytes; version-pinned wiki pages
(S187/S196) are not content-pinned, so committed bytes — not re-fetch — are the
anchor (criterion 50: commit the bytes or name the committed receipt; criterion
27: rotating digests don't anchor). Five small files, sha256 recorded once in
the lesson Gate.

## 5. Discardable (propose only; nothing deleted)

| group | status | reason |
|---|---|---|
| `assimilation/reg-ids.txt`, `assimilation/staged-ids.txt` | committed `b1b740d` | Superseded: both lists (185 + 132 lines) are embedded verbatim in the committed ExecCollisionGuard.md and re-derived by its extractor one-liner. Pure duplication of committed report content. |
| `assimilation/guard-proof-reg-ids-tolerant.txt`, `-reg-ids-col0.txt`, `-staged-ids-tolerant.txt` | committed `b1b740d` | Redundant intermediates: the verdict-bearing bytes are the two `guard-proof-collisions-*.txt` plus the fixtures; the per-extractor id sets are quoted in the report's table. |
| `assimilation/validate/` (~60-file mirror) | untracked | Ephemeral by construction (corpus copy + append block); rebuildable from `corpus@<rev>` + `append-block.md`. Evidence = C3 receipt. |
| `assimilation/append-block.md` | untracked | Superseded at landing by `git diff <pre>..<post> -- corpus/SOURCES.md` and ExecAppendTransform's per-cell table. Needed only until the append; discard after. |
| `assimilation/recheck-prose-stripped.md` | untracked | Duplicate: registration item 3 names the lesson `## Gate` as the home of the stripped prose. Discard once the lesson lands. |
| `c2/controls/c1-predicate-attack/` (6 trees) | untracked | Attack byproducts: every counter output is embedded in the committed CriticC1Predicate.md and each tree is rebuildable from its construction table (≤10 lines each). Criterion 25's committed-mutant-receipt rule binds instrument *tightenings* — none is registered this round (routed, per the round-30 precedent). |
| `scratch/` (scout fetch copies, scribe entry drafts, ExecCensusManual transcripts, MutExistingGates copies) | untracked | Ephemeral: URL+sha256+access date in committed scout reports are the provenance (criterion 13 — scratch records provenance only); drafts superseded by the landed `corpus/knowledge/*.md` at the landing commit (criterion 8); census transcripts pasted in the report; mutant copies = diffs in the report. |
| `w1/logs/` (32), `w1/prompts/` (32), `w1/seat-plan.tsv`, `w1/exit-codes.tsv`, `dispatch-w1.sh`, `w1-taskcall.json`, `w1-spec.json`, `w1/reports/swarm-registry.json` | untracked | Driver runtime and seat bookkeeping, not evidence. Round-30 committed exactly `w1/reports/` (+ `registration.md`) and nothing else of the wave; `registration.md` + the reports carry the contract and the evidence. |

Kept in full: all 32 seat reports, `registration.md` (currently untracked —
commit it, §6), the guard-proof core, `quarantine-slice`, `fetch/`, the lesson,
the SCORECARD append, the three landed knowledge entries and five registry rows.

## 6. Ordering and hygiene risks (action needed before the append)

1. **Criterion-36 ordering is already strained**: control receipts were to be
   committed before data seats were created; wave seats have run. Stop the
   bleeding — commit A1 and B2 *before* the L1 append lands, and disclose the
   boundary in the lesson (r21 registration-integrity note).
2. **Untracked producers**: `registration.md` and `quality/check-axis-scores.py`
   must be committed before any receipt that names them (criterion 24
   `tool_sha256` / producer anchor resolves only against committed bytes).
3. **Misfiled path**: the C1 attack trees sit under `c2/controls/`, which
   registration reserves for the K2 receipt. Land B2 as
   `c2/controls/k2-controls.txt` alongside; leave existing bytes where they are
   (append-only discipline); future attack trees nest under `c1/`.
4. **Report bloat mechanism**: ExecCollisionGuard.md embeds 317 id lines. The
   fix is the §5 rule — quote verdict-bearing outputs, count the rest, keep raw
   lists in one-command-derivable files (or omit them). Same for the pending
   census/quarantine reports.

Out of scope: round-30 leftovers in the worktree (modified `LOG.md`,
`RevRecordsChain.md`/`RevTrendExpansion.md`/`SentScope.md`, untracked
`RevTrendDiscernment.md`/`SimplifierC2.md`) are not round-32 artifacts; no
proposal made on them.
