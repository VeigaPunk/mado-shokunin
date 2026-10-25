# RevScorecard — round-35 scorecard rows, attacked

Seat: RevScorecard (round 35, wave 2, mado). Leaf member: zero subagent dispatch.
Wrote only under `.ufo/waves/round-35/scratch/RevScorecard/` and this report. No lane
corpus file, counter, control, `SOURCES.md`, `SCORECARD.md`, `LOG.md`, Git index or
sibling repo was written; `/home/vgpnk/Projects/shokuknow` was read only.
Installs: none (python3 3.14 + git + bash sufficed).

## 0. The rows under test, and where they actually live

`SCORECARD.md` at the lane tip `19e4ab3171c1540c40d6b12097745af98053b07d` contains
**no round-35 rows**:

```
$ git status --porcelain=v1 | grep SCORECARD      -> (empty)
$ grep -n "Round 35" SCORECARD.md                 -> (empty)
$ tail -60 SCORECARD.md | head -3                 -> "## Round 34 — …"
```

The only round-35 row text in the tree is the wave-1 draft
`.ufo/waves/round-35/scratch/ScribeScorecard/draft.md` (lines 24-38, + axis line 29-32,
+ harm watch). This seat therefore re-derives every number **in that draft** with the
row's own counting command, and reports where the draft would publish an
unmeasured value if applied as-is.

Method. All committed-byte measurements were taken from `git clone --shared` copies of
this repo under `scratch/RevScorecard/`: `clone` at `19e4ab3` (the freeze commit) and
`clone34` at `dff3941` (the commit the row calls the r34 tip). `--shared` reads the
lane's objects through alternates and writes nothing into the lane `.git`. Worktree
measurements are labelled as such.

## 1. Cell-by-cell — C1 row (draft line 26)

```
$ (clone@19e4ab3) python3 -I .ufo/waves/round-35/c1/count.py --root . \
      --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
exit=1

$ (lane worktree) same command
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0

$ (committed control tree, clone@19e4ab3)
python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/controls/golden \
      --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
```

| Cell | Published | Re-derived from committed bytes | Verdict |
|---|---|---|---|
| axis | `C1 coverage` | Published axis set carries `navigation` as the coverage sub-axis, at 47/47 = 1.0 (below) | AGREE (label) |
| "three admitted entries" (`idle-lock-never-asked-r12.md`, `…chain-armed-r14.md`, `…offered-in-the-bar-r15.md`) | exist | `git status --porcelain` → all three are `??` (untracked); counter needs them to read as regular files, and does on the worktree | AGREE on worktree bytes; **not committed at any revision** |
| "eight registry rows S203–S210" | exist, 11 cells, `mined`, used-by exact | `corpus/SOURCES.md` (worktree) `grep -cE '^\| S[0-9]'` → 200; S203–S210 each present once, 11 cells, `status=mined`, `used-by` exactly the citing entry; `git show HEAD:corpus/SOURCES.md` → 192 rows, **0** of S203–S210 | AGREE on worktree bytes; **not committed** |
| "package ids S309/S310/S321/S329/S330/S331/S334/S336 recorded in the round lesson" | mapping | **No.** The round lesson records that this exact set is the registration's erratum: "Seven of the eight are wrong … Only S336 matches", and gives the authoritative remap `S315, S316, S327, S335, S336, S337, S340, S342` (`corpus/lessons/round-35.md:122-131,162-163`). The package originals' own `source:` lines confirm it (`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/idle-lock-*.md` cite S315/S316, S327, S335/S336/S337/S340/S342). The lesson itself is `??` (untracked) | **DIVERGE** — the row publishes the pre-erratum list that its own cited lesson falsifies |
| "pre-data freeze `19e4ab3`: `closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED` exit 1" | before | exact string reproduced at `19e4ab3`; `exit=1` | AGREE |
| "data commit ⟨fill commit hash⟩" | after commit | no such commit exists: `git rev-parse HEAD` = `19e4ab3`; `git rev-parse master` = `19e4ab3`; no commit contains the entries (`git cat-file -e HEAD:corpus/knowledge/idle-lock-never-asked-r12.md` fails) | **UNMEASURED / no referent** |
| "`closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` exit 0" | after | TRUE only on the uncommitted worktree and on the committed `controls/golden` fixture; at HEAD the same command prints `0/0/8 TARGET_MISSED` exit 1 | **DIVERGE at every commit that exists**; agrees on uncommitted bytes |
| "registry 192 → 200 rows" | 192 → 200 | left: `git show 6d754bd:corpus/SOURCES.md \| grep -cE '^\| S[0-9]'` → 192 and `git show HEAD:…` → 192. right: worktree `grep -cE` → 200; `git show HEAD` → 192 | left AGREE; right **worktree-only** (mixed provenance) |
| "navigation 47/47 → ⟨50/50⟩" | 47/47 → 50/50 | `python3 -I quality/check-index.py --rev HEAD --repo .` → `indexed=47/47 … exit 0`; worktree `--root .` → `indexed=50/50 … exit 0` | left AGREE; right **worktree-only** |
| counting command cell | `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen …/frozen.json` | byte-equal to `registration.md` §C1 | AGREE |
| verdict cell `⟨pending data commit — expected: target met⟩` | pending | not a measurement | **UNMEASURED** |
| "kill rule discharged by the eleven committed pre-data receipts: every defect control `TARGET_MISSED` exit 1, `controls/golden` `3/8/0 TARGET_MET` exit 0; all eleven reproduced byte-for-byte" | 11 controls | re-ran all 11 committed trees at `19e4ab3`: 10 defect trees `TARGET_MISSED` exit 1, `golden` `3/8/0 TARGET_MET` exit 0; every receipt's `PRED-C1` line matched the re-run stdout byte-for-byte and every recorded `exit=` matched | **AGREE** |
| "scratch additions: entry `nlink=2` → MISSED; receipt-side `S_ISLNK` → MISSED (w1 ExecSymlink)" | scratch | re-ran both scratch trees: `closed_entries=2 closed_rows=6 open_cites=2 TARGET_MISSED` exit 1 and `closed_entries=2 closed_rows=7 open_cites=1 TARGET_MISSED` exit 1; `stat -c %h` on the hardlinked entry → 2 | **AGREE** (scratch-only, as the cell says) |

## 2. Cell-by-cell — C2 row (draft line 27)

```
$ (clone@19e4ab3) python3 -I .ufo/waves/round-35/c2/count.py --repo . \
      --frozen .ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
exit=0

$ (clone34@dff3941) python3 -I <clone@19e4ab3>/…/c2/count.py --repo <clone34> \
      --frozen <clone@19e4ab3>/…/c2/frozen.json
PRED-C2-r35-v1 error=clause-ledger-missing
exit=2
```

| Cell | Published | Re-derived | Verdict |
|---|---|---|---|
| axis | `calibration`, "tied for lowest; all three scored sub-axes at 1.0" | `MADO_AXIS_ROW: axis=navigation published=47/47 derived=47/47 MATCH`, `calibration 41/41 MATCH`, `operability 12/12 MATCH`; `MADO_AXIS: checked=3 mismatched=0 rev=19e4ab3` exit 0 | AGREE — all three at 1.0, so all three are jointly lowest |
| "capability entered in round 34, so the stagnation nudge does not waive" | no waiver | `SCORECARD.md:2142` `### Capabilities (round 34)` carries the row `crib-rejecting coverage counter`, first-working round 34; declared window N=3; round 34 is one round prior | AGREE (see residual R2 on the two capability tables) |
| before `@ dff3941`: `error=clause-ledger-missing` exit 2 — "no clause ledger, no re-issued blob ledger existed" | before | reproduced with the committed r35 counter over the `dff3941` tree; `.ufo/waves/round-35/` does not exist at `dff3941` (`ls` → No such file) | AGREE |
| after `@ 19e4ab3`: `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET` exit 0 | after | exact string, exit 0, from the clone at `19e4ab3` | AGREE |
| counting command cell | as given | byte-equal to `registration.md` §C2 | AGREE |
| "do-nothing receipt (`controls/c2-donothing.txt`) prints `uncovered=1 … TARGET_MISSED` exit 1" | control | committed receipt says `uncovered=1 … verdict=TARGET_MISSED` / `exit=1`; rebuilt the defect from the committed clause ledger (drop one clause's `control`): `uncovered=1 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MISSED` exit 1 | AGREE |
| caveat "ledger membership is unauthenticated worktree bytes — RevDoNothing V1 (truncated live pool) and V3 (receipt aliasing) also print TARGET_MET" | caveat | w1 RevDoNothing records V1 `TARGET_MET` exit 0 and V3 `TARGET_MET` exit 0 against scratch ledgers; the counter reads `repo / spec["clause_ledger"]` with `is_file()` and only `ledger_tip_ok` touches git | AGREE |
| "retire the r34 dead word-bound clause" | repair by retirement | r34 counter (`git show dff3941:.ufo/waves/round-34/c1/count.py`) line 152 is `found == quote`, which pins the quote, so the 1-25 word bound could not fail; r35 `frozen.json` carries no `quotes` block and `controls/c1-quote-long` kills the bound (`TARGET_MISSED` exit 1). `clauses.json.retired` = `r34-word-bound-1-25`, absent from `live` | AGREE |
| "split S_ISLNK/O_NOFOLLOW: load-bearing vs declared-TOCTOU" | split | `clauses.json`: `o-nofollow-open` carries `not-load-bearing.reason`; `entry-regular` (S_ISLNK component walk) carries `control.receipt=c1-entry-symlink.txt`, which prints `TARGET_MISSED`; `toctou_declared=1` requires the singleton | AGREE |
| "re-issue the frozen-blob ledger at the real r34 tip" | `dff3941` = r34 tip | **No.** `RevFrozenBlobs-r35.md:9-13` asserts "Round-34 lane tip = `master` = `dff394109…`". `git rev-parse master` = `19e4ab3`; `git rev-list --count dff3941..master` = **2** (the intervening commit `6d754bd` is itself titled "round-34 verifier spot-check"). Blob ids in the ledger are nonetheless correct at `dff3941`, `6d754bd` and `19e4ab3` for all seven paths (verified by `git rev-parse <rev>:<path>`; identical) | **DIVERGE** — the re-issue repeats the stale-label defect it was written to repair; `ledger_tip_ok=1` passes on a false premise the counter cannot see |

## 3. Section-level numbers (draft header, axis line, sources block, capabilities)

| Claim | Re-derived | Verdict |
|---|---|---|
| "frozen at `19e4ab3` — the same commit carries both frozen predicates, both counters, the clause ledger, the eleven committed control receipts and the re-issued frozen-blob ledger" | `git ls-tree HEAD` has both `count.py`, both `frozen.json`, `c1/clauses.json`, `ledger/RevFrozenBlobs-r35.md`; `.ufo/waves/round-35/controls/*.txt` = **12** (10 c1 defect + `golden.txt` + `c2-donothing.txt`) | mostly AGREE; **count is 12, not 11** |
| "round-34 counters are NOT amended — blob ids unchanged at the r34 freeze, the r34 tip `dff3941` and this tip (`RevFrozenBlobs-r35.md` §3 re-verifies all seven at the real tip)" | blob ids identical at `dff3941`, `6d754bd`, `19e4ab3` (all seven). The blob table is §1, not §3; §3 states the no-later-write argument; no section re-verifies at `19e4ab3` (this seat did) | AGREE on substance; **§ citation mis-numbered**; "real tip" false per §2 |
| "One wave, 64 seats (13 executor, 12 scout, 11 reviewer, 8 critic, 3 mutation-tester, 2 each simplifier/sentinel/revenger, 7 scribe, 4 connector)" | `dispatch.out`: "launching 64 seats concurrently"; 64 files in `w1/reports/`; prefix census matches the listed composition exactly (`Scout*.md` = 12, `Rev*.md` = 11, `Exec*.md` = 13, `Crit*.md` = 8, …). `w1/seat-plan.tsv` holds only **63** data rows (11 scout) | AGREE against dispatch/report evidence; the seat plan is short one scout row (adjacent evidence defect, not the row's) |
| axis line "Axis table re-derived at ⟨data commit⟩: navigation ⟨50/50⟩ = 1.0; calibration resolved-active ⟨N/N⟩ = 1.0; operability selftest 12/12 = 1.0" | navigation 50/50 only on the worktree (`47/47` at HEAD); calibration derives **41/41** (cell unfilled); operability `12/12` reproduced | operability AGREE; navigation and calibration **uncommitted / unfilled** |
| "Sources 192 → ⟨200⟩ rows" | 192 committed; 200 worktree | same split as the row |
| capabilities table | `## Capabilities` still `| — none yet — |`; `SCORECARD.md` has no diff | **UNTOUCHED** (see §4) |

### 3a. Harm path the draft's ⟨fill⟩ cells create (demonstrated, not argued)

```
# (i) apply the draft section verbatim at 19e4ab3 (sim commit 53f91cd)
MADO_AXIS_ROW: axis=navigation published=47/47 derived=47/47 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=- derived=41/41 verdict=NOT-PUBLISHED
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=1                                   exit=1

# (ii) commit the data without the publication line (sim commit 6a45c68)
MADO_AXIS_ROW: axis=navigation published=47/47 derived=50/50 verdict=STALE
MADO_AXIS: checked=3 mismatched=1                                   exit=1

# (iii) positive control: data + navigation 50/50 + calibration 41/41 + operability 12/12
MADO_AXIS: checked=3 mismatched=0  (sim commit 4bc38a96)            exit=0
```

So the three ⟨fill⟩ cells are load-bearing for a green axis gate. Applied as drafted
today, the lane's own calibration gate goes red on `calibration NOT-PUBLISHED`; and the
data cannot land without the filled publication line without going red on navigation.

## 4. The four mandated structural checks

1. **Claims name distinct axes.** AGREE. C1 = coverage (idle-lock control surface, the
   navigation sub-axis), C2 = calibration (clause ledger / blob ledger). Two claims, two
   axes; they are also causally separable (C1 reads `corpus/`; C2 reads the predicate
   machinery and git blobs; neither counter reads the other's artifacts).
2. **At least one claim works the lowest non-retired axis.** AGREE. The published axis
   table is `navigation 47/47`, `calibration resolved-active 41/41`, `operability
   selftest 12/12` — three sub-axes tied at 1.0, re-derived by
   `quality/check-axis-scores.py --rev 19e4ab3` (`mismatched=0`, exit 0); no other scored
   sub-axis sits below 1.0 in the current table. Both claims sit on two of the three
   lowest-tied axes. The stagnation nudge does not waive (capability entered in round
   34; see residual R2).
3. **No axis is claimed harmed.** The registration says "no axis is lowered"; the draft's
   harm-watch cell is `⟨fill after data commit⟩` with "expected unchanged" — i.e. the
   claim cell itself is unmeasured. Measured at the worktree (where the data lives):
   `MADO_INDEX: root=. indexed=50/50 missing=0 dangling=0 duplicates=0` exit 0;
   `MADO_SELFTEST: 460/460 assertions passed` exit 0;
   `MADO_AXIS: checked=3 mismatched=0 rev=19e4ab3` exit 0;
   `MADO_REGRESSION: PASS (case=mado-verify-hardened; … target=367ff5ec9613701a…)`
   exit 0. So **no measured harm**, but the row publishes no harm measurement.
4. **Capabilities table untouched.** AGREE. `git status` shows no `SCORECARD.md` change;
   the canonical `## Capabilities` table still reads `— none yet —`; no round-35 row has
   entered any capability table. The draft's proposed row would be *eligible* on the
   demonstration rule — I reproduced both halves from committed bytes (`TARGET_MET`
   exit 0 at `19e4ab3`; the do-nothing ledger `uncovered=1 … TARGET_MISSED` exit 1) — but
   its name ("audit of an admission counter") is wider than the demonstrated thing (a
   shape audit of whatever ledger the caller's `--frozen` points at), which the draft's
   own caveat states. That caveat must travel with the row, not sit three lines below it.

## 5. Findings, by severity

**F1 — HIGH — the C1 after-column is false at every commit that exists.**
`closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` holds only on the
uncommitted worktree (`git status`: `M corpus/SOURCES.md`, `M corpus/README.md`,
`??` the three `idle-lock-*` entries) and on the committed `controls/golden` fixture. At
`HEAD`/`19e4ab3` the same command prints `0/0/8 TARGET_MISSED` exit 1. The row's
"data commit" is a ⟨fill⟩. Applying the row now would publish a measured-looking number
that no commit contains.

**F2 — HIGH — the row publishes unmeasured cells as if ready.**
Draft line 26-31 carries `data commit ⟨fill commit hash⟩`, `⟨re-run at that commit and
paste actual⟩`, verdict `⟨pending data commit — expected…⟩`, axis `⟨50/50⟩`,
`⟨N/N⟩`, and harm watch `⟨fill after data commit⟩`. Under the lane's own rule ("an unrun
check has not passed") these are non-measurements; §3a shows two concrete ways the draft
as-written turns `quality/check-axis-scores.py` red.

**F3 — HIGH — the C1 row asserts the package-id mapping its own lesson calls wrong.**
The row says "package ids S309/S310/S321/S329/S330/S331/S334/S336 recorded in the round
lesson". That is precisely the registration's list which `corpus/lessons/round-35.md`
records as erratum **M35-1**: seven of eight wrong, correct remap
`S315, S316, S327, S335, S336, S337, S340, S342` — which the package originals' `source:`
lines confirm. Additionally the lesson is untracked (`?? corpus/lessons/round-35.md`), so
the cited proof resolves to no committed byte.

**F4 — HIGH — the C2 row's "real r34 tip" is false; the re-issue repeats the defect it
repairs.** `RevFrozenBlobs-r35.md` states "Round-34 lane tip = `master` = `dff394109…`".
`git rev-parse master` = `19e4ab3` and `git rev-list --count dff3941..master` = 2; the
intervening commit is titled "round-34 verifier spot-check". The seven blob ids are
identical at `dff3941`, `6d754bd` and `19e4ab3`, so the ledger's *conclusion* survives —
but the label is stale by two commits and "= master" is provably false. `ledger_tip_ok=1`
is therefore true only relative to a false premise; the counter substring-matches the
literal tip and cannot detect this.

**F5 — MEDIUM — the axis line as drafted reds the lane's calibration gate.**
See §3a: verbatim application at the freeze commit → `calibration published=- derived=41/41
verdict=NOT-PUBLISHED`, `checked=3 mismatched=1`, exit 1; data committed without the
publication → navigation `STALE 47/47 vs 50/50`, exit 1. The filled form is exactly what
produces `mismatched=0`. The publication line must be filled and ride the data commit.

**F6 — MEDIUM — `digest-match` does not implement the frozen predicate's sentence.**
`count.py:174` computes `digest = hashlib.sha256(blob).hexdigest()` and never reads it;
the conjunct is `receipt["sha256"] in cs[5]` — the *spec's* digest appearing in the row's
anchor cell, not the receipt bytes' hash. Probe (scratch copy of `controls/golden`, one
line appended to `S203.receipt.txt`; new sha256 `ef2f322c815054fa…`, cell still
`1b7fa87ffe93…`):
`PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` exit 0.
On the committed bytes all eight spec digests equal the committed receipt hashes
(verified), so the published `closed_rows=8` stands; the predicate text ("whose anchor
cell carries the sha256 of the named receipt") does not.

**F7 — LOW — three count/label nits.** (a) "the eleven committed control receipts": 12
`.txt` are committed at `19e4ab3` (11 c1 kill set + `c2-donothing.txt`); (b) the C1 row
asserts "registry 192 → 200 rows" while the Sources block prints the same value as
`⟨200⟩`; (c) "`RevFrozenBlobs-r35.md` §3" is §1 for the blob table. Also the C1 row's
"(frontier → core)" label has no mado frontier list behind it — `PROVINCE.md` already
names "screen/idle behavior (hypridle/hyprlock where present)" in the owned surface list
(the label follows rounds 32/34 precedent, not a PROVINCE frontier entry).

## 6. Residual risk and verification gaps

- **R1 — two tables named "capabilities".** The round-34 row lives in
  `### Capabilities (round 34)`, while the canonical `## Capabilities` table still reads
  `— none yet —`. The nudge argument ("a capability entered in round 34") depends on
  reading the per-round subsection as the table. If the canonical table were the only
  one, the nudge would be *available* — which would not harm the round, only weaken the
  necessity of the lowest-axis claim.
- **R2 — ledger authentication.** The C2 capability's limit is real and correctly
  caveated: V1 (truncate `live` to the TOCTOU clause) and V3 (alias all eight receipts to
  one committed MISSED receipt) both reach `TARGET_MET`. Nothing in either counter pins
  `clauses.json` or any receipt to a blob id.
- **R3 — golden ≠ lane data.** The committed golden fixture is byte-identical to the
  worktree only for `idle-lock-never-asked-r12.md`; `…chain-armed-r14.md`,
  `…offered-in-the-bar-r15.md` and `SOURCES.md` differ (`sha256` differ). The golden tree
  is an anti-vacuity fixture, not a preview of the data: its `TARGET_MET` must not be
  quoted as the data's verdict.
- **Unverified by this seat:** nothing claimed in the draft remains unrun except (i) the
  after-state at a nonexistent data commit, and (ii) the two scratch link controls, which
  I did re-run and which agreed. `--regression` was run at the worktree and passed
  (harm-watch expectation), though the draft leaves that cell unfilled.
