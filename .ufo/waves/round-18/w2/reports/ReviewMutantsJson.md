# ReviewMutantsJson — one-input isolation, M2/M6 labels, criterion-25 wording

Seat: `MadoR18.ReviewMutantsJson`, wave 2 (FALSIFY), 2026-10-20. Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Read-only in the lane: no git/jj
write, no package/service/compositor/input command, no fetch, no install. The
only lane byte written is this report.

Artifact: `.ufo/waves/round-18/evidence/measure-mutants.json`
(sha256 `58929eea…bb133e5`), produced by
`.ufo/waves/round-18/measure-mutants.py` (sha256 `075815bd…`). Criterion 25
is `corpus/QUALITY.md:138`; the 6/6 label is `corpus/lessons/round-18.md:17`.

## Verdict

- **The receipt reproduces in full.** I replayed both instruments at every
  recorded baseline and mutant commit from the committed run's kept repos
  (24/24 runs; exit and `c2` exact), and the 12 mutant runs are also
  byte-identical in stdout and stderr — not a token-substituted match. Every
  `diff_sha256` hashes the stored diff and the kept repo's `git diff`. The
  harness re-run with `--out /tmp/...` exits 0 with an identical summary. No
  fabricated number found.
- **One-input: 5/6 clean, M6 not quite.** M1–M5 each change exactly one
  entry-level input and produce exactly one credit/rejection delta. M6 produces
  one credit delta but two entry-evidence deltas: the duplicate `S016` row also
  removes `S016` from `corpus/knowledge/window-rule-effects-getprop.md`'s
  `sources_ok` (the note stays credited via S002/S017-S020). That is last-wins,
  which is the hazard the duplicate-id tightening exists to stop; no credit
  moves, but a strict "exactly one input" answer for M6 is no.
- **Criterion 25: substance met, literal wording not.** The committed receipt,
  both instrument shas and all six diff digests are present and independently
  verified. But "the post-change instrument **rejects it**" is an explicit
  rejection only for M1/M3/M4/M5; M6 is a whole-run refusal and M2 is a silent
  non-credit (tight `rejected: []`). And "a seat or `/tmp` lab run is
  provenance, not credit" literally describes this artifact's own
  `environment.workdir` (`/tmp/mado-r18-mutants-run`) and the harness its
  runnable check invokes. The lesson discloses both weaker forms ("M2 at entry
  level, M6 as a refusal"), so the labels are honest; the criterion text needs
  "rejects" defined and the `/tmp` clause narrowed to "unreceipted".

## Commands run and results

Receipt and producer identity:

```
sha256sum .ufo/waves/round-18/evidence/measure-mutants.json
  → 58929eeaf9e822042a43e45f2363885ce1b4094a3fa5e3531ca3e2845bb133e5
git show 4c103b55:.ufo/waves/round-18/evidence/measure-mutants.json | sha256sum
  → 58929eea…   (same)
git show abfbf35b:.ufo/waves/round-18/evidence/measure-mutants.json | sha256sum
  → 58929eea…   (same; the receipts commit did not re-cut it)
git show 4c103b55:.ufo/waves/round-18/measure-mutants.py | sha256sum
  → 075815bd…   (equals harness.sha256 and the worktree file)
git show f52f43f8:.ufo/waves/round-17/measure.py | sha256sum
  → a280b3ab7c4dc21a25a954056f6a0c55187fd84dc06cfcddcb28e7f897d3508e
git show d9a5a18e:.ufo/waves/round-17/measure.py | sha256sum
  → de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc
```

Instrument replay (equivalent shell):

```
for m in M1 M2 M3 M4 M5 M6; do
  repo=/tmp/mado-r18-mutants-run/$m/repo
  for side in loose tight; do
    ( cd "$repo" && python3 -I .ufo/waves/round-18/measure-$side.py <baseline-or-mutant-sha> )
  done
done
```

Results: 24/24 runs reproduce the recorded `exit` and the whole parsed `c2`
(count, score, covered path lists, `rejected` reasons, `u_routes`, `c1`,
`c3_present`). Full baseline `c2` is equal between loose and tight for every
mutant, not only the subset `baseline_assert` checks. The 12 mutant runs match
the recorded `stdout_sha256` and `stderr` exactly, byte for byte.

Diff identity:

```
sha256(stored diff) == diff_sha256 == sha256(git -C /tmp/.../repo diff --no-color HEAD^ HEAD)
```

for all six; M1 `e9f712a5…`, M2 `cf76218f…`, M3 `6a0fcaf8…`, M4 `1bf73ed9…`,
M5 `700d022a…`, M6 `d62bfcd8…`.

Baseline provenance:

```
git -C /tmp/mado-r18-mutants-run/Mx/repo rev-parse HEAD^^{tree}
  → 6487a8c20…   (all six identical)
git -C M1/repo ls-tree -r HEAD^   vs   git -C <lane> ls-tree -r d9a5a18
  → 902 vs 903 paths; 0 differing blobs/modes
  → missing: 120000 .ufo/waves/round-17/tripwire/hardening/symlink-target.jsonl
```

The one skipped symlink is an absolute-target round-17 test fixture; neither
instrument reads `.ufo/`. The baseline content is d9a5a18.

Harness end-to-end (outputs confined to `/tmp`; lane untouched):

```
python3 -I .ufo/waves/round-18/measure-mutants.py \
  --out /tmp/verify-mutants.json --workdir /tmp/mado-r18-verify
→ EXIT=0
→ M1..M6 BITES; summary {mutants 6, bites 6, no_bite [], expectations_met 6,
  expected_but_unmet [], unexpected_tight_only [], baselines_agree true}
```

All six rerun records have the same `diff_sha256`, `files`, `diff`, `compare`
and instrument shas as the committed receipt; only `generated_at`,
`baseline_commit`, `mutant_commit` and `repo` differ (the receipt's own
`harness.note` says mutant commit hashes identify that run only).

## Per-mutant isolation

Full entry-evidence delta (baseline → mutant, both instruments; every credited
entry's `reason` and `sources_ok`):

| id | mutation (one line) | loose delta | tight delta | other entry evidence |
|---|---|---|---|---|
| M1 | `surface: P4` → `surface: P4 terminal` | 0 | loses P4 `terminal-route-r17.md`; reason `surface line must be exactly` | none |
| M2 | `covers: U6` → `covers: U6, U1` | gains P1 `input-debugging-boundaries-r15.md`, reason `legacy covers: U1 -> P1`, sources S051/S052 | 0; `rejected: []` | none; `u_routes` union stays 7 (U1 already present) |
| M3 | S016 `used-by` += fixture note; new P3 note cites S016 | gains P3 `p3-upstream-keyword-mutant.md`, sources_ok `[S016]` | rejects it: `no cited mined tier-A row ... naming the surface` | no other note changes; the `used-by` edit is wiring |
| M4 | new row S900; new P3 note with a 2-line `## Host declaration` | gains P3 `p3-section-floor-mutant.md`, sources `[S900]` | rejects it: `sections under content floor: ## Host declaration` | none |
| M5 | new row S901 inserted under `## Paths`, outside `## Registry`; new P3 note | gains P3 `p3-registry-only-mutant.md`, sources `[S901]` | rejects it: `no head source: S### token resolves ...` | none |
| M6 | second `S016` row (+ fixture note) | gains P3 `p3-duplicate-id-mutant.md`, sources `[S016]`; **also** P1 `window-rule-effects-getprop.md` loses S016 from sources_ok | exit 2, stderr `duplicate SOURCES id S016`, no `c2` | second entry-evidence delta |

M6 in detail:

```
loose baseline  P1 corpus/knowledge/window-rule-effects-getprop.md
  sources_ok = S002, S016, S017, S018, S019, S020
loose mutant    P1 corpus/knowledge/window-rule-effects-getprop.md
  sources_ok = S002, S017, S018, S019, S020
```

The duplicate row replaces S016 for all citations (last-wins); because the
walker row's `used-by` names only the fixture note, the P1 note loses S016. It
remains credited via the other five rows. This is invisible in the committed
receipt: `summarize()` stores only `covered` path lists and `rejected`
reasons, not per-entry `sources_ok`. It does not change any credit, and the
tight refuses before evaluating, so the strictly measured bite is still the
duplicate id. But the diff does touch a second input (the pre-existing
source-resolution check), so M6 is not a pure one-input mutant.

## M2 and M6 labels

**M2 (entry-level) is honestly labelled.** The JSON's own `expect` says "count
may stay 4 because P1 is already covered by the pinned paths"; the data is
`loose_count=4`, `tight_count=4`, `loose_only.P1=[corpus/knowledge/input-debugging-boundaries-r15.md]`,
and tight `rejected: []`. Lesson line 17 says "M2 at entry level". Nothing
claims a count or province change. The only overstatement risk is that "bite"
in the summary is a bare boolean; a reader must read `compare.basis` to see
that the delta is one credited path in an already-covered province.

**M6 (refusal) is honestly labelled.** `compare.tight_refused=true`,
`tight_count=null`, `mutant.tight.exit=2`, `stderr="duplicate SOURCES id S016"`,
and the last `basis` line names the refusal; lesson line 17 says "M6 as a
refusal". One structured-field caveat: `compare.loose_only` then contains
`P1,P2,P3,P4,P6` because `covered_view({})` is empty. Only P3 is caused by the
mutation; the other four are baseline coverage observed by the loose run. A
consumer that counts `loose_only` would see five discriminations where there is
one. The `tight_refused` flag and basis mitigate this, but the field is
misleading on its own. The harness's own console output shows the same five.

**`expectations_met: 6` is 5 anchored + 1 unanchored.** `expectation_met()`
returns True by construction when a spec has neither `reason_contains` nor
`error_contains`; M2 has neither. M1/M3/M4/M5 are anchored on the tight
rejection reason, M6 on stderr. The `bites` gate still requires a loose-only
entry and the committed data shows the right one, so no bite depends on the
unanchored boolean. (Sibling `MeasureMutantsRerun.md` F2 reaches the same
point.)

## Criterion 25: does the wording cover this receipt?

Criterion 25 (`corpus/QUALITY.md:138`) requires "a committed mutant receipt in
which the pre-change instrument credits a committed mutant and the post-change
instrument rejects it, both instruments named by sha256 and each mutant by its
diff digest"; it adds "a seat or `/tmp` lab run is provenance, not credit".

What is satisfied, verified:

- **Committed receipt**: the JSON is byte-identical at `4c103b55` and
  `abfbf35`; its harness sha matches both commits.
- **Both instruments by sha256**: `a280b3ab…` at `f52f43f` (loose),
  `de4c422b…` at `d9a5a18` (tight), verified from lane git; the harness
  re-asserts each pin before every run (`run_instrument`), and I re-hashed the
  staged files in all six repos.
- **Each mutant by diff digest**: `diff_sha256` per record, verified against
  both the stored diff text and the kept repo's `git diff`.
- **Loose credits the mutant**: the loose run at each mutant commit credits
  the mutated entry, with the entries' own reasons proving causation
  (`surface: P4`; `legacy covers: U1 -> P1`; sources S016/S900/S901/S016).
- **Tight rejects**: M1/M3/M4/M5 explicitly, with the expected reason; M6 by
  exit 2; M2 does not credit.

What the literal wording does not cleanly cover:

1. **"Rejects it" is undefined at the level M2 and M6 operate.**
   M1/M3/M4/M5 are item-level rejections. M2 is a silent non-credit: the note
   is not in tight's `rejected`, it simply does not gain the P1 entry. M6 is a
   whole-run refusal: the tight instrument exits 2 before producing `c2`, so
   it rejects the run/mutant rather than an entry. The artifact's
   `mutant_method` defines bite more broadly than the criterion: "loose credits
   a province entry the tight run does not, **or** the tight run refuses". The
   lesson's "M2 at entry level, M6 as a refusal" discloses both. If "rejects"
   means an explicit rejection record, the count is 4/6; if it means "does not
   credit the mutated entry or refuses the run", it is 6/6. Criterion 25 should
   say which. Suggested wording: "the post-change instrument does not credit
   the mutated entry (silent non-credit is a kill) or refuses the run".
2. **The `/tmp` exclusion literally covers this artifact.** `environment.workdir`
   is `/tmp/mado-r18-mutants-run`; the six mutants are commits in throwaway
   `/tmp` clones, not lane commits. The receipt is committed, and the lesson
   says "committed-in-clone", but the criterion's clause "a seat or `/tmp` lab
   run is provenance, not credit" has no "unreceipted" qualifier. The
   criterion's own runnable check *is* the harness that creates the `/tmp`
   clones. As written, a strict scorer can cite 25 against the very receipt it
   points to. Suggested wording: "an unreceipted seat or `/tmp` run is
   provenance only; a committed receipt that embeds the mutant diff and both
   instrument shas is credit". Optionally commit the six patches under
   `.ufo/waves/round-18/mutants/` so the mutants are lane bytes rather than
   only JSON-embedded diffs.
3. **"Committed mutant receipt" is satisfied in content, not in git-object
   terms.** The mutants are committed only in throwaway clones; the committed
   receipt embeds each full diff and its digest. That is enough to reconstruct
   the mutant, but it is not a lane commit. If 25 intends lane-committed
   mutants, the artifact fails that stricter reading; the text should say
   "receipt embedding the mutant diff" or "mutant committed in the lane".
4. **The runnable check is not read-only.** The bare command
   `python3 -I .ufo/waves/round-18/measure-mutants.py` writes the lane evidence
   path by default and would replace the committed receipt with a new
   `generated_at`, `started_at`, `workdir`, `kept: false`, `repo: null` and new
   throwaway commit ids. The committed receipt's `argv` is
   `--keep --workdir /tmp/mado-r18-mutants-run`. A verifier should pass
   `--out /tmp/...`; the criterion should say so. (Sibling `MeasureMutantsRerun.md`
   F5 also notes this.)

The red claim in 25 holds: at `d9a5a18` no rubric-V tightening mutant receipt
exists. The four mutant-named files there
(`gate-mutant-gkeep.txt`, `gate-mutant-sources-resolve.txt`,
`covering-mutants.txt`, `regular-target-mutants.txt`, `retained-census-mutants.txt`)
are round-12/13/14 gate/target mutants, not rubric V; the round-17 reports
mention `a280b3ab…`/`de4c422b…` in prose only.

## Harness rigor (supporting findings)

- **`bites` is one-sided on a refusal.** `bites = bool(loose_only) or
  tight_refused` (`measure-mutants.py:378`). For M6 the refusal alone sets
  `bites=true`; `loose_only` is then every loose province because
  `covered_view({})` is empty. If the loose instrument had failed to credit the
  fixture note, the harness would still report a bite. The committed data
  credits P3, so the record is honest; the *automated gate* does not verify
  the loose side for M6. For M1–M5, `expectation_met` anchors the tight
  rejection reason but not the identity of the loose-only entry. The data
  shows the right entries in all six; the gate is weaker than the claim.
- **`baselines_agree: true` is a literal** (`:583`), guarded only by
  `baseline_assert`'s count/province/covered-set checks (`:401`). I
  independently confirmed full baseline `c2` equality including `rejected`,
  `u_routes` and `c1`, so the fact is true here; the field is not computed and
  the assertion would not catch a divergence in those other fields.
- **M2's `expectation_met` is vacuous** (`:480`), as noted above.
- **The summary's `no_bite` semantics** are "records whose `bites` is false",
  not "tightenings the loose instrument already rejects" as the criterion's
  runnable-check prose says. No impact on this receipt (`no_bite: []`).

## Residual risk and verification gaps

- The six kept repos under `/tmp/mado-r18-mutants-run` are ephemeral. The
  receipt's `repo` fields and commit ids are not durable; the diff bytes,
  `diff_sha256`, instrument shas and verdicts are, and a rerun reproduces them
  (only timestamps/commit ids change). After a `/tmp` clear, direct replay of
  the recorded commit ids is impossible; content replay is not.
- I did not run the criterion's bare command; that would rewrite the lane
  evidence. I ran the harness with `--out /tmp/verify-mutants.json --workdir
  /tmp/mado-r18-verify`, and the instrument replays inside the kept repos.
- I did not re-derive the six tightenings' intended semantics beyond the
  instrument diff (`f52f43f` → `d9a5a18`, six behavioral changes: registry-only
  parse, duplicate-id fail, exact `surface:`, legacy `(path,U)` pin, surface
  keyword, three-line floor). The per-mutant rejection reasons and single-entry
  deltas show each fires for the named check; they do not prove the checks are
  the right rubric policy.
- No network, no host probe, no package/service/compositor/input operation; no
  fetch receipts are involved in this artifact.
- Sibling `MeasureMutantsRerun.md` already reports the independent rerun (F1–F5).
  This report adds: the full entry-evidence delta showing M6's second input
  (the `sources_ok` loss), the criterion-25 "rejects"/`/tmp` wording analysis,
  and the one-sided refusal bite predicate.
