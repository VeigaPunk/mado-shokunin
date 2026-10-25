# Round 36 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-25
scope: mado round 36 only. Base `4243d031e3441f5063f92c33aa58377c6f9ff120`, lane tip
`a5aaa09ad38bfd90c13d76ccf371e36c45a2697e`, report `.ufo/reports/round-36/mado.md`
(final fleet commit `b26422a6f7062bcd0fe5768b55467cd320056860`).
Method: committed bytes only. No lane gate, selftest, or jj command was executed by this
reviewer (§Gate standard, Closure consequence); a lane gate's verdict is graded from its
committed receipts and their digest bindings. Three read-only seats re-derived independent
slices (pointer observables, errata arithmetic, the S211 source re-open).

## 1. Step-1 conformance

| Item | Result |
|---|---|
| Report committed in the fleet repo by the lane identity | **pass** — `git log --format='%an %ae %H' -- .ufo/reports/round-36/mado.md` → six commits, all `mado-shokunin <mado@shokunin.local>`; final `b26422a6` (committed 05:40:34 -0300) |
| Report lands after the lane tip (D1) | **pass** — lane tip `a5aaa09` committed 05:40:09 -0300, 25 s before the report commit |
| `SHONEN` heading, one line per box | **pass** — 4 boxes, 4 lines, each `[~]` with a pointer |
| Every cited lane commit exists and is an ancestor of the branch | **pass** — `merge-base --is-ancestor <h> master` → anc-ok for `4243d03 dbf8b57 a3094c9 520c631 ebc5437 c5d7773 cf175c7 2d90524 ea89bde 64979ef a5aaa09` (tested against `master`, not `@{u}`) |
| Lane pushed, no uncommitted round work | **partial** — `jj-lane.sh state` → `ahead=0 behind=0`, `ls-remote origin refs/heads/master` = `a5aaa09…`; but `git status --porcelain` → `?? .ufo/waves/round-36/w1/reports/DistillerFindings.md` (19,033 B, mtime 05:31), a round-36 seat report left uncommitted while the report's line 379 asserts "working tree clean". Defect R1 |
| Prompt carries the template contract | **pass** — `.ufo/prompts/mado-round-36.md`, 481 lines: `## 1 … ## 5` identical to `templates/round-prompt.md` headings (incl. `## 2b. Frontier step`), plus `## 6. Campaign addendum — hyaku …` at line 141 |
| Marker-vs-real | **real report** — checkable work, commits, receipts |

## 2. Claim re-checks

### C1 — calibration: the two round-35 admission counters are repaired and shown to discriminate

Re-measured from committed receipts, plus digest binding against the committed gate bytes:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
grep -c ' ok=1$' .ufo/waves/round-36/receipts/before-discrimination.txt   # 14
grep -c ' ok=1$' .ufo/waves/round-36/receipts/after-discrimination.txt    # 25
grep -c '^control=' .ufo/waves/round-36/receipts/after-discrimination.txt # 25
sha256sum quality/check-counter-discrimination.py quality/counters/c1-idle-lock.py \
          quality/counters/c2-ledger.py .ufo/waves/round-36/controls/manifest.json
```

Observed: `14` / `25` / `25`; `e396b95e…db86`, `5e0b9824…99a9`, `92db777e…3833`,
`cace34b4…8ab7` — byte-identical to the four digests the after receipt's header binds.
Manifest: 25 controls, 25 unique ids, `expect` counter `{'TARGET_MET': 3, 'TARGET_MISSED': 22}`
(`c1-live`, `c1-golden-r36`, `c2-live` accept; 14 `c1` + 8 `c2` rejects); both receipts' control-id
sets equal the manifest's, no duplicate control line. The before run's 11 wrong lines split
4 `c1` (`c1-shape-only`, `c1-fabricated-payload`, `c1-no-registry-heading`, `c1-row-moved-out`)
and 7 `c2`, exactly as the report states.

Verdict: **improved** — re-measured (counts, id sets, digest binding) over committed bytes; the
instrument's own run is evidence-verified from the committed receipt, not re-executed here.

### C2 — operability: the lane's records pass an evidence-pointer durability gate

Re-derived each observable from committed bytes:

```sh
git ls-tree -r master --name-only | grep -c 'round-35/scratch/SimplifyCounter/\|round-35/scratch/MutC1Drop/mutants/'  # 0
git ls-tree -r master --name-only -- .ufo/waves/round-35/scratch | wc -l                                            # 124
sed -n '2156,2157p' LOG.md          # the two `old -> new` correction pairs, machine form
git ls-tree -r master --name-only | grep -c 'round-35/scratch-evidence/\(SimplifyCounter\|MutC1Drop\)/'               # 4
git ls-tree -r master --name-only -- quality/receipts
```

Observed: the two round-35 pointers resolve to nothing (dangling=2), each is paired to a
`scratch-evidence/` replacement that does resolve (closed=1), the round-35 scratch tree carries
**124** tracked paths, the lesson line 267 reads "**retained** as round-35 evidence: tracked
paths=124", and `quality/receipts/axis-520c631d…txt` is committed with
`MADO_AXIS: checked=3 mismatched=0 rev=520c631d…` (a hex ancestor of `master`). `setup` = ok
(LOG `## Round 36`, SCORECARD `## Round 36`, lesson all non-empty). Six of seven observables
are reproducible from committed bytes alone; `inherited_dirty` reads `git status` on the
worktree and is the receipt's disclosed non-reproducible reading (before-state header records
`inherited_dirty=10` and says why it cannot be re-run). Defect R5.

Verdict: **improved**.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | **improved** | C1: 14/25 → 25/25 on 25 frozen controls, digest-bound |
| operability | **improved** | C2: `TARGET_MISSED` → `TARGET_MET`, five observables at target |
| coverage (published as navigation 50/50) | **unchanged** | `SCORECARD.md` axis table: 50/50 before and after; no knowledge entry (`git diff --numstat 4243d03 a5aaa09 -- corpus/knowledge/` empty) |
| freshness, depth, adjacency | **unchanged** | not claimed; adjacency boundaries written into the capability rows |

No axis harmed: `git diff --numstat 4243d03 a5aaa09 -- quality/ tools/ corpus/QUALITY.md SCORECARD.md`
→ insertions only (`SCORECARD.md 124/1`, the single deletion being the `## Retired` line that the
round had to correct), `tools/mado-verify.sh` blob `9113c7c05e58…` identical at `4243d03`,
`7a068cb` and `a5aaa09`, `quality/check-index-rows.py` blob `319e6720…` untouched (the inherited
rev-mode defect routed, not patched inside the discovering round).

Exploratory claim: **none declared**, so no `unprovable-but-better` ruling is owed by this
reviewer.

## 3. Discernment spot-check (LEARNING.md — checked from outside)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S211 negative controls | admit, tier A, `mined` | `https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/`, re-fetched 2026-10-25, 150,283 B | **agree** | the 17-word quote appears exactly once after tag-strip, inside `<p id="P15">` under section `S2` "Examples of the use of negative controls in epidemiology"; ≤25 words; article metadata (Epidemiology 2010;21(3):383, PMID 20335814) matches the row |
| guessed PMCID `PMC2833407` | reject before citation | `https://pmc.ncbi.nlm.nih.gov/articles/PMC2833407/` | **agree** | it is a proteomics paper (concanavalin A hepatitis, *J Zhejiang Univ Sci B* 2010;11(3):221), 0 occurrences of "negative control" — the guess was checked and dropped, which is the behaviour the reject records |
| `PMC12186581` | considered, not opened, not a row | not re-opened (by design) | **agree** | CORPUS rule 1 admits a row only after opening; refusing an unread source, with the flip condition written down, is the correct call |
| quote location convention | row carries no quote cell | lesson `round-36.md` `## Gate` + receipt | **agree** | CORPUS rule 1 puts the ≤25-word quote in the lesson's Gate; it carries URL, access date, the quote and `#S2/#P15` |
| receipt identity ruling | extraction digest, not raw sha | three fresh fetches | **agree** | raw HTML sha rotates (`27fee95e…`, `db3e74ff…`) at an invariant 150,283 B while the extracted plain sha256 `3b2f9bde…` is stable |
| census before → after | 200 → 201 rows, exit 0 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | **agree** | exit 0, the same seven pre-existing `W04` warnings (S030…S121), `mado ok`; `grep -c '^| S[0-9]'` → 200 at `4243d03`, 201 at `a5aaa09`, `numstat` `1 0` (no existing row touched) |

## 4. Trend verdicts

- **expansion: unchanged.** One grounding row (S211) and zero admitted knowledge entries
  (`git diff --numstat 4243d03 a5aaa09 -- corpus/knowledge/` empty). The report says so and
  refuses to call a method row coverage — the right call.
- **quality: improved.** Two instruments that could not tell work from shape now discriminate
  (14/25 → 25/25 with the live bytes still accepted); the records pass a pointer gate for the
  first time; the harm watch is green on committed evidence (`MADO_SELFTEST: 460/460 assertions
  passed` in `w1/reports/RevSelftest.md`, `MADO_INDEX: indexed=50/50 missing=0 dangling=0` in
  `w1/reports/RevIndexGate.md`, census exit 0). Evidence-verified, not re-executed.
- **discernment: improved, with named limits.** The lane's own counters are attacked by 25
  committed controls (always-reject 23/25 killed by the two `c1` accepts; accept-all 11/25
  killed by the 14 rejects; five receipt forgeries probed), a wave seat's finding against the
  freeze became criterion 61 in the same round, and the report lists its remaining holes
  (digest-clause anchor half unexercised by the frozen manifest, no exit/verdict coherence,
  three-substring transcript, manifest identity now bound). The one honesty gap is that the
  holes are routed to round 37 rather than closed here, which the report states.

## 5. Routed defects (lane fixes next round; none changes this round's status)

1. **R1 — uncommitted round artifact at closure.** `.ufo/waves/round-36/w1/reports/DistillerFindings.md`
   is untracked in the lane work tree (19,033 B) while report line 379 claims "working tree
   clean". Commit it (its scratch ledger `scratch/DistillerFindings/catalog.md` did land in
   `a5aaa09`) or delete it, and correct the clean-tree assertion. This is the D2 class the round
   itself closed for round 35.
2. **R2 — report's measured revision contradicted by its own receipts.** Report lines 196, 215
   and 231 name the after state at `64979ef`; `receipts/after-discrimination.txt` and
   `receipts/after-pointers.txt` (re-pinned in `fe55a90`) both name
   `4d28b193e52f6cc8f04e81fda2664e018d62e209`, and `SCORECARD.md` was corrected to that hash in
   `a5aaa09`. Append an erratum; the gate blobs are unchanged across `4d28b19..a5aaa09`, so the
   claim itself is unaffected.
3. **R3 — criteria arithmetic.** The report says "six criteria (57–61)" twice; the tree holds
   exactly five new criteria (`57.`–`60.` at `a3094c9`, `61.` later), which the scorecard states
   correctly as "all five new criteria, including 61".
4. **R4 — stale receipt size in the lesson.** `round-36.md` §Sources says the S211 receipt is
   "1,037 B"; at the tip it is 1,756 B (`git cat-file -s`: 1037 at `a3094c9` → 1756 at
   `f77b554`, when the identity note was added).
5. **R5 — one observable is a worktree reading.** `inherited_dirty` is measured from
   `git status` rather than a revision, so C2's after-state is not fully reproducible from
   committed bytes (the before receipt discloses this for its own state only). Commit a
   `git status --porcelain` witness with the receipt or derive the observable from a revision.
6. Already lane-routed and named in the report, carried forward: manifest identity inside the
   gate (now bound), exit-code/verdict coherence, the three-substring transcript, the
   undocumented control order, the inherited `quality/check-index-rows.py` rev-mode
   `exists_glob` defect, the generator's `/tmp` traversal and race, and the digest clause's
   anchor half not exercised by the frozen manifest.

Environment note (fleet, not a mado defect): `/tmp` is 100 % full on this host (3.0 MB free),
which is why the S211 re-fetch was redirected to `/dev/shm`; any lane gate that writes fixtures
under `/tmp` should expect failure until it is cleared.
