# CritClaimSizingV2 — post-data claim sizing and honesty (round 44, w2)

Seat: CritClaimSizingV2. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Read first: `.ufo/waves/round-44/registration-v2.md` (freeze `03fa5c61`). Data commit `e4678921`; base `6a1a9052`;
current tip `290cddea` (data → tip diff touches `.ufo/` only, verified below).
Every locator below is from `grep -n` / `git ls-tree` at the named revision, never typed.

## Verdict on the five assigned checks

| # | check | verdict | evidence |
|---|---|---|---|
| 1 | no rule changed after data (both v2 counters) | **PASS** | `git log --oneline -- quality/counters/c1-r44-geometry-states-v2.py` and `…c2-r44-gkeep-size-request-v2.py` each print exactly one commit, `03fa5c61`; the control runners, `c1/ctl-ref-tool-v2.py.txt`, `l1-draft/` and the two `ctl-*-v2.txt` receipts are also single-commit at `03fa5c61`. `git diff --name-only e4678921 290cddea -- . ':!.ufo'` prints nothing, so no counter, reference or freeze file moved after data. |
| 2 | after-states equal the registered targets | **PASS** | C1 at data **and** tip: `fixtures=26/26 tool=present verdict=TARGET_MET`, clauses `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1`, exit 0 (re-run by this seat at both revs). C2 at data **and** tip: `admitted=1/1 verdict=TARGET_MET`, exit 0. Byte-for-byte these are the targets in registration-v2 §C1/§C2 (modulo the per-run nonce the counter declares). |
| 3 | SCORECARD / LOG Round 44 numbers re-derive | **PASS** (every number; see F1 for the citation rev) | sources 234→238 (`grep -c '^| S[0-9]' corpus/SOURCES.md` 234 at base, 238 at data); knowledge 60→61 (`git ls-tree -r … corpus/knowledge/ | grep -c '\.md$'`); M44 = 9 and M43 = 9 (`grep -c '^\*\*M44-'`, `'^\*\*M43-'`); `DOMAIN_META: domain=12 meta=5 window=34-43 default=1` (same at data rev and at `03fa5c6`); tool selftest `94/94`; w1 `seats: 38` in `w1-results.json` and 38 `w1/*.md`; `ctl-c1-v2.txt` `0 of 20`, `ctl-c2-v2.txt` `wrong=0 of 11; positive admitted=1`; S164 cells 1-10 byte-equal, cell 11 (used-by) the only diff. |
| 4 | axis publication (navigation 61/61, calibration 71/71) re-derives | **PASS** | `python3 -I quality/check-axis-scores.py --rev e4678921…  --repo .` → `MADO_AXIS_ROW: axis=navigation published=61/61 derived=61/61 verdict=MATCH`, `axis=calibration published=71/71 derived=71/71 verdict=MATCH`, `axis=operability published=12/12 … MATCH`, `mismatched=0`, exit 0. The instrument reads its scripts from the rev (`show()` + `run_script()`), and base is `60/60`, `68/68`, `12/12`. The parenthetical cause is exact: navigation +1 = the one new index entry; calibration +3 = criteria 82-84 (`count.py` counts `^[0-9]+\. ` lines of `corpus/QUALITY.md`: 81 at base, 84 at data). |
| 5 | QUALITY 82-84 each have a mistake and a fail-able check | **PASS with one self-inflicted caveat (F1)** | 82 ← lesson `## considerthese` + proposal 1; its check fails two ways (mutant `domain=13` vs 12; draft 1 classes round-40 C1 `meta` while the deliverable is `tools/mado-options.py`) — both re-run by this seat at the data rev. 83 ← M44-4; its check re-run at `1959770` prints `CHECK83: verdict=FAIL citations=3 violations=2`. 84 ← M44-8; the named command re-run by this seat prints `CTL_C2v2 FORGED-PIN … rejected … d:0` and `VERDICT: PASS (wrong=0 of 11; positive admitted=1)`. Criterion 84's fail-ability is also proven by the v1 branch (forgery admitted under `PRED-C2-r44`). |

## Findings

### F1 — MEDIUM — the data commit lands QUALITY 82-84 and the lesson citing w1 evidence that is not in that tree; criterion 83 fails its own document

Attacks: the round's claim that a citation resolves at the revision it is judged at (`.ufo/waves/round-44/w1/ScrQualityCriteria` semantics), and the sizing of "Shown able to fail" in `corpus/QUALITY.md:411,413,415`.

Evidence (all run at the data rev):

    $ python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . \
        --rev e46789213830597348fe96a351ae004d10587385 --doc corpus/QUALITY.md --prefix .ufo/
    LATE .ufo/waves/round-44/w1/ExecDomainMetaRatio/ratio-mutant-axis-token.py (added 410f193 after e467892)
    LATE .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py (added 410f193 after e467892)
    LATE .ufo/waves/round-44/w1/CritC2Cheat/frozen-F2-FORGED-PIN.txt (added 410f193 after e467892)
    CHECK83: verdict=FAIL citations=60 violations=5 rev=e467892
    $ … --doc corpus/lessons/round-44.md --prefix .ufo/
    LATE .ufo/waves/round-44/w1-results.json (added 541c5c4 after e467892)
    CHECK83: verdict=FAIL citations=13 violations=1 rev=e467892

`git cat-file -e e4678921:.ufo/waves/round-44/w1/ScrQualityCriteria/check83.py` → absent; the same path exists at `290cddea`. So at the data commit each of the three new criteria points at evidence admitted before it was in the tree — the M44-4 class, one round later, in the commit that lands M44-4's criterion. At the tip the same command prints `violations=2` for `corpus/QUALITY.md` (both pre-round-44 `NOWHERE` placeholders, present already at base) and `PASS` for the lesson.

Impacted axes: none of C1/C2 values move (the counters never read w1); the operability/coverage after-states stand as verified in check 2. Impact is on the round's citation honesty.

Smallest safe correction (L1 decides; data is frozen, so this is an appended erratum): add `290cddea` as the rev of the evidence in each criterion's pointer — line 411: `Shown able to fail at `290cddea`: the axis-word mutant …`; line 413: `Check at `290cddea`: `python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py …`; line 415: `Check at `290cddea`: the counter's FORGED-PIN control …` — plus one erratum line in the Round-44 SCORECARD section:

> Erratum (w2/CritClaimSizingV2): at the data commit `e4678921` the round's own QUALITY 82-84 evidence pointers are `LATE` — `check83.py --rev e4678921 --doc corpus/QUALITY.md --prefix .ufo/` prints `CHECK83: verdict=FAIL citations=60 violations=5` (3 round-44 LATE) and `--doc corpus/lessons/round-44.md` prints `violations=1`; the pointers resolve at the evidence commit `290cddea`, where the same run prints `violations=2` (both pre-round-44 `NOWHERE`).

### F2 — MEDIUM — the lesson cites two receipts that exist at no revision

Attacks: `corpus/lessons/round-44.md:232-233` (C1/C2 census bullets).

Evidence:

    $ grep -n 'after-tip' corpus/lessons/round-44.md
    232:  `receipts/c1-after-data.txt`, `receipts/c1-after-tip.txt` (PRED-C1-r44-v2; the v1 counter is superseded and is not the claim's rule).
    233:- C2 at base: `receipts/c2-before-base.txt` (`admitted=0/1`, exit 1). At the data commit / tip: `receipts/c2-after-data.txt`, `receipts/c2-after-tip.txt` (PRED-C2-r44-v2).
    $ git ls-tree --name-only 290cddea .ufo/waves/round-44/receipts/ | grep after-tip   # (no output)
    $ git cat-file -e e4678921:.ufo/waves/round-44/receipts/c1-after-tip.txt             # absent

The round-44 receipts dir holds 17 files at data and no `*-after-tip.txt` at the tip either. Round 43 did land tip receipts (`5846662`), so the sentence promises the same and does not yet deliver. Criterion 79 needs a committed receipt at the round tip. The *state* is not in doubt — this seat re-ran both counters at `290cddea` (C1 `26/26`, C2 `1/1`, exit 0) — only the pointer is.

Corrected sentences:
- line 232: `- C1 at base: `receipts/c1-v2-before-base.txt` (`fixtures=11/26 tool=present verdict=TARGET_MISSED`, exit 1). At the data commit: `receipts/c1-after-data.txt` (PRED-C1-r44-v2).`
- line 233: `- C2 at base: `receipts/c2-before-base.txt` (`admitted=0/1`, exit 1). At the data commit: `receipts/c2-after-data.txt` (PRED-C2-r44-v2).`
(If the close lands `c1-after-tip.txt` / `c2-after-tip.txt`, the original wording becomes true and no edit is needed.)

### F3 — MEDIUM — OPEN predicate defect: criterion 83's universal is wider than its instrument, so round-relative `w1/…` citations escape it

Attacks: `corpus/QUALITY.md:413` universal ("every repository path a document formats as code exists in that revision's tree") vs its checker's scope.

Evidence: `SCORECARD.md:2566` and `:2573` format five w1 reports as code (`w1/CritC1Cheat.md`, `w1/CritC2Cheat.md`, `w1/CritClaimSizing.md`, `w1/RevC2Counter.md`, `w1/CritFsPremise.md`). Resolved under the round dir those are `.ufo/waves/round-44/w1/…` and are absent at `e4678921` (`git cat-file -e` → no for each). Yet the same check run over `SCORECARD.md` at the data rev reports only two `NOWHERE` and no `LATE`:

    $ check83.py --repo . --rev e4678921… --doc SCORECARD.md --prefix .ufo/
    NOWHERE .ufo/waves/kaika/steer.md (no ref of the repository holds it)
    NOWHERE .ufo/prompts/mado-round-12.md (no ref of the repository holds it)
    CHECK83: verdict=FAIL citations=112 violations=2 rev=e467892

The instrument only inspects paths that literally begin with the `--prefix`, so a round-relative shorthand is invisible while the criterion text does not say so. Either the universal is narrowed ("every path written from the repository root") or the checker resolves round-relative shorthands. No re-registration after data: report as an open defect for round 45.

Impacted axes: calibration's instruments only in the sense that criterion 83's coverage claim is larger than its check; no number moves.

### F4 — LOW — the lesson's C1 "base" line quotes the superseded v1 counter's receipt, not the v2 base the round registered

Attacks: `corpus/lessons/round-44.md:231` vs `SCORECARD.md:2570` and registration-v2 §C1.

Evidence: `c1-before-base.txt` is `PRED-C1-r44` (v1): `fixtures=12/26 … nonce=c207ce6303ef9781`, exit 1. The round's v2 before-state is `c1-v2-before-base.txt`: `fixtures=11/26 … TARGET_MISSED`, and SCORECARD:2570 says `fixtures=11/26 … (`receipts/c1-v2-before-base.txt`)`. The lesson's own next clause says "the v1 counter is superseded", so the 12/26 is not a v2 measurement.

Corrected sentence (line 231): `- C1 at base: `receipts/c1-v2-before-base.txt` (`fixtures=11/26 tool=present verdict=TARGET_MISSED`, exit 1; the superseded v1 counter's `receipts/c1-before-base.txt` prints `12/26` at a different nonce). At the data commit: `receipts/c1-after-data.txt` …`

### F5 — LOW — the landed SKILL.md host-run block is round 43's and disagrees with the round-44 receipt

Attacks: `.ufo/waves/round-44/receipts/live-geometry-host-r44.txt` vs `SKILL.md:225` and `:293-299`.

Evidence: SKILL prints `clients=4` and "the dump holds four tiled clients" (both dated 2026-10-26); the r44 receipt prints `clients=3` and lists three clients (`Alacritty`, `zcode`, `grok-bot`). Both are honest observations, but the round edited SKILL (rows + exit-map note) without pointing the example at its own receipt, so a reader at the data tree sees two different counts for the same day.

Corrected sentence (line 293): `Host run 2026-10-26, no gkeep window open (round-43 dump; the round-44 receipt `receipts/live-geometry-host-r44.txt` has three clients and still `NO_MATCHING_CLIENT`, exit 3): …`

### F6 — LOW — QUALITY 84's check command and its committed receipt use different freezes

Attacks: `corpus/QUALITY.md:415` vs `.ufo/waves/round-44/receipts/ctl-c2-v2.txt:1`.

Evidence: the criterion passes `--freeze 03fa5c618b089064a657b3d79d3d4272ae4b6894`; the receipt header reads `CTL_C2v2: freeze=e2289516a9a857f55cda7be635933e89b931c3da … controls=11`. This seat ran the criterion's exact command: it reproduces the cited line and verdict (`CTL_C2v2 FORGED-PIN … rejected … d:0`; `VERDICT: PASS (wrong=0 of 11; positive admitted=1)`) but with `FORGED-PIN … rev=76da95ea…`, not the receipt's `rev=d37bd410…`, so the receipt is not byte-reproducible from the command as written.

Corrected sentence: use `--freeze e2289516a9a857f55cda7be635933e89b931c3da` (the freeze the committed receipt used) in criterion 84, or land a receipt produced with `03fa5c61`.

### F7 — LOW — a present-tense universal the same landing falsifies

Attacks: `corpus/lessons/round-44.md:152` ("nothing recomputes a lesson's mistake count against the SCORECARD").

Evidence: `SCORECARD.md:2583` in the same round reads `Mistakes M44-1..9 mined (`grep -c '^\*\*M44-' corpus/lessons/round-44.md`)` — the SCORECARD now recomputes the count, as the same paragraph's Fix prescribes. The sentence is true only of the pre-fix state.

Corrected sentence: `… its step-1 table; before this round nothing recomputed a lesson's mistake count against the SCORECARD.`

### F8 — INFO — LATE witnesses are attributed to jj keep snapshots, not the master commit

`check83.py` prints `added 410f193` / `added 541c5c4`; `git cat-file -p 410f193` shows parent `e4678921`, empty subject, `change-id vwuklrpx…`, and `git for-each-ref` maps it to `refs/jj/keep/410f1935…` (`4b781071` likewise, parent `290cddea`, same tree `007263a1`). The reader-facing commit for every one of these additions is `290cddea`. Not a rule change (the v2 counters still have exactly one commit); a wording fix in F1's erratum should cite `290cddea`.

## What is untouched by these findings

- C1 and C2 after-states and their targets: verified at both revs, exit 0.
- The axis table: all three rows MATCH at the data rev.
- The freeze: both v2 counters, both v2 references, both v2 control runners and both control receipts are single-commit at `03fa5c61`; no rule moved after data.
- Controls: C1 `0 of 20` and C2 `wrong=0 of 11; positive admitted=1` re-read from the frozen receipts; C2's exact QUALITY-84 command re-executed here and passes.

## Tooling / scratch

No tool installed. Python 3 stdlib and read-only `git` only; no pacman, no compositor write, no lane mutation.
Scratch `/fast/scratch/hyaku/mado-r44/CritClaimSizingV2/` was used for the two counter `--work` dirs and the
control clone tree; it is deleted before this seat finishes. All citable evidence is in this file (command + output)
or in the lane's committed receipts.
