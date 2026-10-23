# CritAxisFit — are round 24's two claims on their named axes?

Role: critic (leaf; no spawns). Question put to me: per prompt §6.9 (kaidoku r29 lesson), is C1
really coverage (a surface moved frontier → sourced) and C2 really calibration (SCORECARD
self-assessment vs observed repo state), or is either quality work in disguise? Is C2's after-state
reachable by merely transcribing counter output, and does that matter under AXES calibration?

Inputs read: `.ufo/waves/round-24/registration.md`; `/home/vgpnk/Projects/shokunin/AXES.md`;
`corpus/lessons/round-23-verifier-spotcheck.md`; `.ufo/prompts/mado-round-24.md` §6.9;
`.ufo/prompts/closure/kaidoku-round-29.md`; both frozen counters and manifests; the landed C1 note
and C2 status table; peer reports `CritC1Predicate.md`, `ScoutAttributionSweep.md`,
`ScoutPriorNotes.md`, `ScribeC2Evidence.md`. No tool was installed or updated. Every command below
was read-only outside sandboxes under `/fast/scratch/hyaku/mado-r24/crit-axis/`.

## Verdict summary

| Claim | Named axis | Axis fit | Verdict line |
|---|---|---|---|
| C1 rule attribution | coverage | **yes, by content — not by the counter** | `C1_AXIS=coverage`; landed note answers the frontier item; `PASS_ROW=23/26` is necessary, not sufficient (fixture below reaches `TARGET_MET` with no attribution) |
| C2 capability re-demonstration | calibration | **yes, narrowly; the counted zero is a consistency check** | `C2_AXIS=calibration`; after-state is reachable by transcription and is direction-blind (control below scores 0/12 after deleting a capability's fixtures) |

Neither claim is quality work in disguise **as landed**. C1's note contains the new negative-route
answer, and C2's `fails` row catches a real overreach. The defects are in what the frozen counters
prove, not in the axis labels. The kaidoku r29 precedent does not reject either claim; it rejects
substituting the counter's number for the surface, which the report and closure must not do.

## C1 — coverage (frontier → sourced)

### What the landed bytes show

- Tip `cf86f9e0e532767bd6989e1d288a681fd72e3651` adds `corpus/knowledge/rule-attribution-r24.md`
  (122 lines), 16 SOURCES rows (S153–S168; S161 `queued`, 15 `mined`), the coverage-map row
  (`corpus/README.md:47`) and a Frontier bullet (`:203-208`). The bullet explicitly supersedes the
  round-12 "Still open: rule *attribution*" wording only for the documentary question; observed host
  attribution, plugin-side recording and the other three items stay open (`:208`).
- The note's answer is on the question, not beside it (`rule-attribution-r24.md:15-24`): no upstream
  channel maps an applied property back to the rule; the available routes are `getprop` (value
  only), `workspacerules` (workspace rules only), a unique `tag` effect read from `clients`, a named
  rule's `set_enabled`/`is_enabled` handle, the applicator's rule-property mask plus priority class,
  and logs (none name a rule). Ordering-inference is labelled inference.
- Independent counter run at the tip (counted/refetch mode):

```sh
python3 -I .ufo/waves/round-24/c1/count.py cf86f9e0e532767bd6989e1d288a681fd72e3651
# A5, A7, A8 FAIL_ROW quote-off-topic; 23 PASS_ROW
# counter_version=v2 ... rows=26 PASS_ROW=23 distinct_sources=14 readme_indexed=True verdict=TARGET_MET
```

Receipt `/fast/scratch/hyaku/mado-r24/crit-axis/c1-tip.txt`, sha256:`81f910a23af6d90e91bfbb1f99f16012f8f35e3d038fa4d234adb1169acb85c4`.
Before, at base `8e5d9369`: `note_present=False rows=0 PASS_ROW=0 verdict=TARGET_NOT_MET`
(`.ufo/waves/round-24/evidence/c1-before-v2-8e5d9369.txt`). The surface is unmoved at base and moved
at tip; the command that shows it unmoved is the same counter.

### The counter does not prove the surface

I built a sandbox note that deliberately contains **no attribution finding** and says so in its
header. It uses six true, non-tautological claims about rule *syntax* from three pinned
hyprland-wiki pages (window-rules, layer-rules, workspace-rules), **three** SOURCES rows opened
`2026-10-23` (six claim rows cite them), and a coverage-map row. The frozen v2 counter scores it
`TARGET_MET`:

```sh
MADO_LANE=/fast/scratch/hyaku/mado-r24/crit-axis/c1fix \
  python3 -I .ufo/waves/round-24/c1/count.py 5712e4f4bd791b6d04cdb9ede50f28a4a25e8ca3
# A1..A6 PASS_ROW
# rows=6 PASS_ROW=6 distinct_sources=3 readme_indexed=True verdict=TARGET_MET  (exit 0)
```

Receipt `/fast/scratch/hyaku/mado-r24/crit-axis/c1-syntax-fixture.txt`,
sha256:`ef4e20dfbac6cfb472e72fca3befa94e338d360982bff4566e7f6f27164ebf11`.
The fixture commit is `5712e4f4bd791b6d04cdb9ede50f28a4a25e8ca3` in a minimal sandbox repo; the
three source pages were fetched at `c66e8de21f5ecdc4bc5e278e7d94800ea10957af` and their sha256s
recorded in the fixture rows. This is the on-topic counterpart of peer
`CritC1Predicate.md`'s udev-homonym attack (which also showed same-URL/three-id sourcing, rows
hidden in HTML comments, and a fabricated anchor span). The point here is narrower and worse for
axis fit: **genuine Hyprland rule pages, true claims, visible rows, three distinct documents** still
pass without the attribution surface. `PASS_ROW ≥ 6` measures sourcing/restatement quality.

The counter cannot be changed now (predicate frozen before controls; §6.9: a rule changed after a
seat scores is not the claim's rule). The correction is therefore review-level, and it matters:

- The closure must read `rule-attribution-r24.md:15-24` and the negative sweep section (`:62-73`),
  not accept `PASS_ROW=23` as the coverage move.
- The note's own heading at `:31` says every quote is "counted by" the counter. It is not: A5, A7
  and A8 are `FAIL_ROW quote-off-topic` (their quotes contain `PRIORITY_WINDOW_RULE`,
  `eRuleProperty` and `COverridableVar` members, which the lexical topic regex rejects). The
  receipt says 23/26, so the note text overstates. Change the heading to 23/26 and name A5/A7/A8 as
  retained code evidence outside the lexical gate.
- The negative answer "no upstream channel" rests on the lane-observation sweeps, not on the
  counted rows (the note says so at `:76-78`). That is honest, but the sweep's own limit — a
  mechanism spelled without a `rule` token would evade the token sweep — belongs in the note's
  Limits (`:87-93`), not only in `ScoutAttributionSweep.md`.
- Most of A19–A26 restate wiki semantics the corpus already holds (syntax, dynamic effects,
  ordering, tags, all-props, named-first): see `keybind-rule-semantics.md:203-213`,
  `window-rule-effects-getprop.md` and the config-era note; the layer-rule handle (A23) is the
  exception. A11 restates the r12 getprop read. The new ground is the code-level storage/engine
  evidence (A1–A18) and the negative synthesis. The report should claim coverage from those, not
  from the row count.

Why this is still coverage and not kaidoku r29's misfit: at base the frontier item was open and the
r12 note left matching-rule identity `[UNK]`; the new note resolves that `[UNK]` to a bounded,
pinned negative and enumerates the partial routes. That is a new surface answer, not a re-score of
a rule the lane already held. The counted rows include restatement, but the note's answer is new
ground.

## C2 — calibration (SCORECARD self-assessment vs observed state)

### What the landed bytes show

- `81955bd` appends `SCORECARD.md:1566-1586`, the `Capability status (round 24 re-demonstration)`
  table: 11 `works`, 1 `fails`. The `fails` row names the real overreach: `tripwire evidence marker`
  is stated in the round-20 capability row (`SCORECARD.md:1342`) with `L 17/18` at `28c6837`; at
  base the same command gives `L 15/18` (P 66/66), with two named reset-cleared L cases failing and
  `L-AdoptW2-AdvHelperFn-b14` failing in both runs. That is round-21 H2, still unrepaired.
- The lane's after run at `81955bd` is `mismatches=0/12` (`.ufo/waves/round-24/evidence/c2-after-81955bd5.txt`).
  Base was 1/12. The status table's `fails` row is the only correction; the other eleven are the
  counter's observed statuses.
- I re-ran the frozen C2 counter at the C1 tip `cf86f9e`; it returns `mismatches=0/12` with the
  same 11 `works` and `tripwire evidence marker stated=fails observed=fails`. Receipt
  `/fast/scratch/hyaku/mado-r24/crit-axis/c2-tip.txt`. The C1 landing did not flip a capability:
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` prints
  `mado ok .../corpus/SOURCES.md`, exit 0, with only the seven pre-existing W04 warnings
  (S030, S042, S045, S097, S119, S120, S121), so `sources registry` is observed `works` at the C1
  tip as well. The target is met at this tip by the frozen counter; if a later data commit lands,
  the counter must be re-run there.

### Is the after-state reachable by transcription? Yes

The predicate reads the status cell only (`c2/count.py`: `status[name] = row[1]...lower()`;
`stated = status.get(name, "works")`; `ok = in_population and stated == observed`). The evidence
column is never consulted. Therefore a table whose status cells are copied from the counter's
`observed` column scores 0 by construction. The wave-1 seat's own draft says it:
`ScribeC2Evidence.md` — "Draft from the do-nothing base run's observed values." The landed table
adds the H2 trace and the L 15/18 detail, which the counter does not require but which is the
actual calibration act.

### The counted zero is direction-blind — control

I built the harm-absorption control in a sandbox clone at `81955bd` (the status-table commit), using
an **append-only** change so the registration's no-harm guards apply: delete
`.ufo/waves/round-21/assessment-fixtures` from the tree and append a second
`### Capability status (round 24 re-demonstration)` table whose one row sets `artifact-only
assessment integrity` to `fails`; commit
`46981925d06741f737d56a5ba300868b5cc75e6a`. The diff from base `8e5d9369` is SCORECARD `35 0`
(additions/removals), and `corpus/SOURCES.md`, `LOG.md`, `PROVINCE.md` and `tools/` are unchanged, so
the no-harm guard on removed lines and `git diff tools/` is clean. The frozen counter returns:

```text
artifact-only assessment integrity  stated=fails  observed=fails  OK  exit=125
mismatches=0/12 revision=46981925d06741f737d56a5ba300868b5cc75e6a
```

Receipt `/fast/scratch/hyaku/mado-r24/crit-axis/c2-harm-append.txt`,
sha256:`bff36ad6b805b57e62ac8aaca4e699311e4c0f96596e89e8cb3d0ab03a8692c9`.
A round can harm a capability (delete its fixtures) and *improve* the C2 count from 1/12 to 0/12 by
appending the failure as status. The registration's no-harm guards do not enumerate the manifest's
fixture populations, and the counter's own `sources registry` capability ran the census on the
harmed tree and observed `works` (exit 0 in the run above). Only a base-observed vs tip-observed
comparison catches this. The actual base, `81955bd` and `cf86f9e` observed lists are identical, so no
capability flipped this round, but the predicate cannot tell.

### Does that matter under AXES calibration?

Yes, for what the claim may assert; no, for the axis label.

- AXES defines calibration as self-assessment quality and its signal as "SHONEN.md/SCORECARD
  entries match observed repo state". The status table is a SCORECARD entry that now matches the
  observation, so the axis is calibration, not operability or freshness. The twelve command runs
  are the method; the changed surface is the assessment.
- But `mismatches=0` is a consistency count between two round-24 artifacts. It is reachable by
  transcription, and it is non-monotonic: a worse repo state can score better (control above). The
  calibration value is the `fails` disposition — the stale `L 17/18` pointer is caught and H2 named
  — which the counter does not measure. The report must credit that row, not the zero.
- Duplicate authority remains: the round-20 capability row (`SCORECARD.md:1342`) still asserts the
  capability with its `28c6837` pointer, while the round-24 table says `fails`. The table's
  "supersedes the implied works" sentence `:1570-1571` gives precedence, but the capability table is
  the repertoire authority under AXES. Append a disposition to that capability row (or an adjacent
  round-24 line) scoping the row to its `28c6837` demonstration and naming `L 15/18` at base.

Verdict: C2 is calibration, narrowly and validly, because the one mismatch was investigated and an
overreach was caught. The counted zero is not evidence of assessment quality; it is evidence that
the status table is internally consistent with the run. That distinction must survive into the
report and closure.

## Cross-claim separability

The claims are separable in the direction that matters: C1 does not depend on C2's table, and C2's
manifest commands do not read the new note except through `sources registry` (census). The census at
the C1 tip is `ok`/exit 0, so C1's 16 new SOURCES rows did not flip that capability. Latent coupling
remains: any future corpus change that breaks census or a fixture would surface as a C2 mismatch (or,
worse, as an absorbed `fails`). The final-tip C2 run at `cf86f9e` returns 0/12, so the C1 landing
does not flip a capability and the separability holds for this tip.

## Smallest safe corrections (no predicate edits, no re-scoring)

1. **C1 note heading (`rule-attribution-r24.md:31`).** Say `23/26` rows pass the frozen counter and
   name A5, A7, A8 as retained code evidence that fails its lexical topic gate. Do not leave a
   reader thinking all 26 are counted.
2. **C1 negative-claim limit.** Add the token-sweep caveat from `ScoutAttributionSweep.md` ("a
   mechanism spelled without a `rule` token would evade the sweep") to the note's Limits. The answer
   stays bounded to `efb50993` and is still a negative over pinned bytes, not host behaviour.
3. **C1 report/SCORECARD.** Claim coverage from the note's answer table and sweep (`:15-24`,
   `:62-73`) plus the README coverage row (`corpus/README.md:47`) and Frontier bullet (`:203-208`),
   not from `PASS_ROW≥6`.
   The fixture above shows the count alone is satisfiable without the surface.
4. **C2 receipt.** Add a base-observed vs tip-observed per-capability comparison (from the base smoke
   and the final-tip run). Any `works → fails` flip at the tip is a harm to report, not an `OK` status.
   The same table closes the harm-absorption hole without touching the frozen counter.
5. **C2 capability-row disposition.** Append a line scoping `SCORECARD.md:1342` to its `28c6837`
   demonstration and naming `L 15/18` at base and the two reset-cleared cases, so the repertoire row
   and the status table do not remain two authorities.
6. **Final tip.** The C2 count is confirmed 0/12 at `cf86f9e`; re-run
   `python3 -I .ufo/waves/round-24/c2/count.py <landed tip>` after the last data commit changes the
   tree, and keep the receipt with the base-observed comparison.
7. **Next round, not this predicate.** If a v3 C1 counter is ever frozen: count distinct sha256
   sources (not S ids), strip HTML comments/fenced blocks, check the SOURCES anchor span against the
   fetched bytes, and tighten the topic gate. If a v3 C2 counter is ever frozen: count
   stated-vs-observed flips from base as harm, not as statuses. Do not touch v2 now.

## Evidence index

| Item | Path | sha256 / commit |
|---|---|---|
| C1 tip counter receipt | `/fast/scratch/hyaku/mado-r24/crit-axis/c1-tip.txt` | sha256:`81f910a2…` |
| C1 no-attribution fixture counter receipt | `/fast/scratch/hyaku/mado-r24/crit-axis/c1-syntax-fixture.txt` | sha256:`ef4e20df…`; fixture commit `5712e4f` |
| C2 harm-absorption control (append-only) | `/fast/scratch/hyaku/mado-r24/crit-axis/c2-harm-append.txt` | sha256:`bff36ad6…`; clone commit `46981925` |
| C2 base smoke | `.ufo/waves/round-24/c2/smoke/base-8e5d9369.txt` | 1/12 |
| C2 after at status table | `.ufo/waves/round-24/evidence/c2-after-81955bd5.txt` | 0/12 at `81955bd` |
| C2 after at C1 tip | `/fast/scratch/hyaku/mado-r24/crit-axis/c2-tip.txt` | sha256:`786e3280…`; 0/12 at `cf86f9e` |
| C1 after at note | `.ufo/waves/round-24/evidence/c1-after-cf86f9e0.txt` | 23/26 at `cf86f9e` |

No host command was run in this review; `hyprctl` was not invoked. The sandbox git repositories
are under `/fast/scratch/hyaku/mado-r24/crit-axis/`; no lane or fleet git/jj write command ran. Only
this report was written to the lane.

## What these bytes do not establish

- The counter fixtures do not show that the lane's note is bad; they show the frozen predicates can
  be satisfied without the surface they are supposed to measure. The landed C1 note and C2 table
  are stronger than their counters.
- The C2 harm control is a synthetic mutation in a sandbox, not a claim that round 24 harmed
  anything. The base, `81955bd` and `cf86f9e` observed lists are identical; no capability flipped this
  round in the receipts I could read.
- No claim is made about host Hyprland behaviour, any tag value, or a live rule toggle. Host
  attribution stays `[UNK]` beyond the read-only join recorded in the note.

**Verdict line:** `CritAxisFit: C1_AXIS=coverage (verified by content; PASS_ROW=23/26 necessary-not-sufficient) C2_AXIS=calibration (verified narrowly; 0/12 transcribable and direction-blind) — both fit, counters under-prove, corrections listed`.
