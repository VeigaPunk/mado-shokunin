# round-32 verifier spot-check (integrator, hyaku): non-author admit/reject

author: hyaku closure (non-author integrator, Kimi fresh closure agent)
Round: mado 32 (attempt 1). Lane tip measured at closure: `d9ed38166cc3be8ef4c52b41d66ad94010feb047`
(= `master`, remote-verified `ahead=0`). Round-start tip: `91862344b9fddbb5b4c3a9977acc776632993799`;
registration base: `256222890d935212874a09751ff9b7869943c2d7` (r31 tip, parent of the round-start tip).
This file is the non-author closure artifact; no lane-authored file was edited.

## Conformance results

- Report committed on the fleet repo by the lane identity: `git log --format='%an %H' -- .ufo/reports/round-32/mado.md`
  → `mado-shokunin <mado@shokunin.local> ead8050566e537b7439310f5021bce2490979848 round-32: mado report`. PASS.
- `SHONEN` heading: report carries `## SHONEN` with 4 `[~]` lines; `SHONEN.md` has exactly those 4 boxes; no `[x]` was written by anyone. PASS.
- Commit ancestry: every cited hash (`f5910876`, `48f9fe09`, `a551f71c`, `d9ed3816`, base `25622289`, round-start `9186234`) is an ancestor of `master` (`git merge-base --is-ancestor`, all PASS). Lane pushed: `jj-lane.sh state` → `local=d9ed3816 remote=d9ed3816 ahead=0 behind=0`; `git ls-remote origin refs/heads/master` → `d9ed3816`. PASS.
- Dispatch/complete digest verified in `.ufo/watchdog.log`: line 1196 `2026-10-24T19:56:38-03:00 launch mado round=32 pgid=1636979 driver=hyaku-inline attempt=1`; line 1203 `2026-10-24T20:33:30-03:00 complete mado round=32; hyaku-inline attempt=1`. No `lane-dead-no-report mado round=32` line exists. PASS.
- Prompt fidelity: `.ufo/prompts/mado-round-32.md` §1–§5 headers match `templates/round-prompt.md` byte-for-byte at the same line offsets (3/9/42/80/99/131) plus the hyaku addendum §6; round-level items (mission/axes binding, L2 minimum "at least 8 in ONE batched call", commit-then-push, push scope, L0 channel) and the five child-lane items (report path, commit-before-report, SHONEN heading, hash-citation rule, write scope) all present. PASS.
- Lane commit identity: all 6 round-32 lane commits carry `mado-shokunin <mado@shokunin.local>`; the two intervening commits (`a327cd4`, `57a772b`) are operator (`João Pedro Veiga`) `considerthese` appends, not lane work. PASS.
- Uncommitted round work: `git status --porcelain` shows 5 paths, all round-30 leftovers (routed defect D7 below) — the driver's `WARN … 5 paths` reproduces. DEFECT (routed), status-neutral.
- Wave evidence: `w1-spec.json` has 32 items with exactly the reported role mix (scout 7, executor 5, scribe 4, reviewer 6, critic 4, connector 2, revenger 1, sentinel 1, mutation-tester 1, simplifier 1) → 13/32 = 40.6% attack roles; `w1-taskcall.json` has 32 tasks, each led by `/skill:godspeed`; `dispatch-w1.sh` = one batched launch of 32 concurrent `omp -p` seats; 32 seat reports committed; `w1/exit-codes.tsv` records 24 seats, all exit 0 (8 seats' codes missing — the disclosed 600 s background-timeout cut; every seat's report exists). PASS with a note: the claimed validator receipt (`counts.spawn=32`, `dispatch.calls=1`) is not committed in the wave set.

## Claim re-checks (re-executed by this verifier)

### C1 — coverage (frozen counter, verbatim from `registration.md` §C1)

Run over committed bytes (`git archive <rev> corpus | tar -x` into /tmp, then the verbatim counter):

| rev | output |
|---|---|
| `256222890d…` (registration base) | `entries=0 rows=0 cited_entries=0` |
| `91862344b9…` (round-start tip) | `entries=0 rows=0 cited_entries=0` |
| `d9ed38166c…` (tip) | `entries=3 rows=5 cited_entries=7` |

Registered target: `entries=3 rows=5 cited_entries=3`. The tip prints **`cited_entries=7`** (the three entries carry 3+1+3 `source:` lines across S186/S187/S188/S189/S196), so **C1 is NOT MET under its frozen predicate** — matching the report's honest stop. Controls re-run by this verifier:

- **Junk control** (3 stub files of one `source:` line each + 5 stub rows whose `used-by` names a nonexistent path): counter prints `entries=3 rows=5 cited_entries=3` — **TARGET MET on junk**. The counter is unsound, reproducing `w1/reports/CriticC1Predicate.md` v1 (verdict CLAIM DEAD).
- **Realistic control** (tip tree + one extra `source:` line): `cited_entries=8` — honest work is rejected on line count (false-negative direction confirmed).
- **Do-nothing controls**: rows-only → `entries=0 rows=5 cited_entries=0`; entries-only → `entries=3 rows=0 cited_entries=3`. Neither one-sided half reaches the target (matches `ExecThemeHoldCheck.md`).

Verdict: the landed data is real (see spot-check table), but the frozen predicate cannot certify it and its target is unreachable at the tip. **C1 = honest stop, claim unverified (`unprovable`).**

### C2 — calibration (lane-owned gate: evidence-verified, not executed, per PROTOCOL §Gate standard)

- Committed publication at base (`9186234:SCORECARD.md:2014-2017`): "Axis table re-derived at base … navigation 43/43 … calibration resolved-active 39/40 … operability selftest 9/9". Committed republication at tip (`master:SCORECARD.md:2063-2065`): navigation 46/46, calibration 41/41, operability 12/12. PASS (byte-verified).
- Committed gate evidence: `LOG.md` round-32 entry records "(selftest 17/17): the base revision measures `MADO_AXIS: checked=3 mismatched=2` exit 1 and the tip measures `mismatched=0` exit 0"; the SCORECARD claims row names the command and both revisions. The gate script (255 L, `quality/check-axis-scores.py`) carries a `--selftest` with 17 committed assertions including "missing publication is not a pass" and "missing instrument is not a pass". Instrument receipts (`CriticC2Predicate.md` ground truth: check-index 43/43, count.py `resolved_active=41`, selftest 12/12 at `50e6a8f`) are committed. PASS as evidence-verified.
- C2's supporting knowledge-file count: `corpus/knowledge/` holds 46 files at the tip (43 + 3). PASS.
- **C2 = target met (`improved`)** on the committed evidence — with instrument-level defects routed (D4, D6).

No owned axis harmed: `git diff 9186234..d9ed3816 -- SCORECARD.md` = +30 lines, no deletions, no lowered row; corpus and LOG appends only.

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | `unprovable` | C1 fails its frozen predicate at the tip (7 ≠ 3) and the counter is falsifiable in both directions; the underlying entries/rows are real and verified (see table) but the claim as frozen does not verify |
| calibration | `improved` | C2 verified on committed evidence: stale published table (39/40, 9/9) republished from re-derivation (41/41, 12/12); gate base mismatched=2 exit 1 → tip mismatched=0 exit 0 |
| operability | `unchanged` | no operability claim; gate selftest count moved 9→12 as a measurement, not an axis move |
| sourced-art / navigation | `unchanged` | rows re-verified, no entry failed re-check; navigation 43→46 is the coverage instrument's movement |

## Spot-check table (LEARNING.md — ≥1 admit, ≥1 reject, ≥1 new SOURCES row re-opened)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/ipc-contract-r25.md` (S186, S187, S189) | admit | committed fetch bytes `.ufo/waves/round-32/fetch/S186.bin` (6,539 B, sha256 `535bc4c385a06162…` — matches row and lesson) and `.189.bin` (6,479 B, `eea605dfe5ce09e1…`) | **agree** | provenance trio opens the entry; quote anchors verified verbatim (`S186:14` `## $XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`; `S189:21` `const auto PATH = …"/.socket2.sock";`); contract kept separate from implementation; unknowns kept |
| `corpus/knowledge/dispatcher-semantics-r25.md` (S188) | admit | `fetch/S188.bin` (12,879 B, sha256 `c830ce0717f92776…`) | **agree** | `S188:8` "Dispatchers return tables that describe an action you want to make." verified verbatim; the wiki's own instability statement carried, not smoothed |
| `two-literature-drift-r26.md` (S195, S198, S199) | reject | staged package bytes `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/two-literature-drift-r26.md`; its S199 row | **agree** | documentation-localization is outside `PROVINCE.md` (no translation-lag surface claimed), and S199 is a CSDN blog, kind `community`, tier `C` — never sole support (CORPUS.md tier rule); flip condition recorded |
| new registry row S186 (`corpus/SOURCES.md:198`) | row write | re-opened committed `fetch/S186.bin`; census schema | **agree** | ≤25-word located quote at `:14` verified; 11-column schema, `status=mined`, `opened=2026-10-24`, `recheck=90d`, `used-by` names exactly the two citing entries; full frozen census over the tip: 190 rows, 0 malformed, no dup ids, no enum violations, all `used-by` paths resolve |

Item-10 checks: id-collision receipts committed (`.ufo/waves/round-32/assimilation/`: reg-ids=185, staged-ids=132, `collisions` empty); guard proven able to fail on the indented fixture (`fixture-ids` finds S002, `fixture-ids-col0` empty — reproduced); validate-before-append mirror committed under `assimilation/validate/`; quarantine slice = exactly 13 rows (6 payload-absent + 7 never-checked, including the register's stray-backtick defect the lesson names), per-row verdicts in `ExecQuarantineSlice.md` (5 PRESENT, 1 ABSENT S224, 7 UNVERIFIABLE); S224 and the unverifiable rows were not appended; S189 was slice→hand-checked PRESENT→adopted, which is the prescribed flow (the report's flat sentence "No quarantined row was appended" is imprecise wording, D11). considerthese provenance: `considerthese/2026-10-23.md` proposal 3 verified verbatim (line 49); every `considerthese/` commit is operator-authored — the lane never edited it.

## Trend verdicts

- **expansion — improved.** 3 admitted entries on ground the lane did not hold (`ExecThemeHoldCheck.md`: no note holds the two-socket contract; 0 registry rows before), each citing `mined` rows opened 2026-10-24; registry 185→190, knowledge 43→46 files (counted). Uncovered-ground + mined-row citation verified by this verifier.
- **quality — improved.** A real self-assessment defect (published table stale against its own counters) was found and repaired by re-derivation, no admitted entry failed re-check, staged line anchors were re-derived rather than copied, and the round disclosed its own unsound counter. The ledger-accuracy defects below are routed and do not flip the corpus-quality trend.
- **discernment — unchanged.** This verifier's spot-check agrees with the gate on the sampled admits and the reject, but the same round froze a junk-admitting predicate without the §9 pre-freeze junk control, published a claims row its own falsifier had already killed (D1), and added no grounded QUALITY.md criterion (deferral reasoned in the lesson). Gate agreement gained, instrument judgment lost — net unchanged, honestly graded by the lane.

## Routed defects (lane must fix in round 33; recorded here, not repaired here)

1. **Falsified claims row left standing.** `SCORECARD.md` round-32 C1 row (landed `a551f71c` 20:27:38) says "target met … tip: `entries=3 rows=5 cited_entries=3`". The tip measures `cited_entries=7` (this verifier re-ran it; the fleet report itself says 7 and honest-stop). No appended correction exists. Append a correction entry (append-only discipline) in r33.
2. **Report timeline inaccuracy.** The report calls 20:05:38 "the data commit"; that commit is `50e6a8f` (ExecCollisionGuard report). The data commit is `f5910876` at **20:22:50** — ~15 min *after* `CriticC1Predicate.md` (mtime 20:08:00), and the "target met" claims row landed 19 min after the falsification was known. File an erratum with the corrected sequence.
3. **"187 MB" unsupported by history.** Committed scratch at `f5910876` is 11.6 MB / 554 blobs (`git ls-tree -r -l`); `48f9fe09` deleted 130 files / 2.7 MB; no gitlinks. The LOG honest note and report both say "187 MB … committed … bytes remain in history" — the on-disk figure was published as committed bytes. Correct in r33.
4. **Gate not registered.** `quality/check-axis-scores.py` has no row in `SKILL.md` `## Gate registry` (registry home per PROTOCOL §Gate standard). Register it (verdict map, selftest spelling, write scope, owner) or the gate stays not-conformant.
5. **K2 control receipts missing.** Registration promises C2 do-nothing receipts "committed under `.ufo/waves/round-32/c2/controls/`"; that dir holds only the critic's `c1-predicate-attack` trees. Commit the K2 receipts (or re-point the registration reference).
6. **CriticC2Predicate DEAD verdicts undisclosed.** The report cites the two SURVIVES verdicts but not attacks 3 and 5 (CLAIM DEAD: `rfind` locator shadowing by quoted errata, 400-char parse truncation; single-axis control coverage). Route the locator and control-coverage repairs to r33; they do not change the measured before→after.
7. **Five uncommitted round-30 leftovers in the lane repo at closure** (the driver's WARN, 5 paths): modified `.ufo/waves/round-30/w1/reports/RevRecordsChain.md`, `RevTrendExpansion.md`, `SentScope.md`; untracked `RevTrendDiscernment.md`, `SimplifierC2.md`. Uncommitted round work under the landed-means-committed rule — resolve (commit under the round's entry or revert) next round; not named in the round-32 report. Not touched by this closure.
8. **Budget-overrun claim unreconciled.** Report: "~35 minutes over its 170-minute budget"; watchdog digest: 19:56:38→20:33:30 = 36m52s wall, well under `ROUND_MAXTIME=170m` (hyaku.env). Reconcile the budget accounting or correct the note.
9. **Minor:** SCORECARD claims rows cite base as `25622288` — an unresolvable hash (real short hash `2562228`).
10. **Minor:** the report's "Round-32 commits, in order" omits `b1b740d1` + `50e6a8f3` (id-collision guard + ExecCollisionGuard evidence), which carry work items the report cites.
11. **Minor wording:** "No quarantined row was appended" — S189 was a quarantine-slice row adopted after its hand-check; state the cleared-then-adopted flow instead.
12. **Process:** the §9 cheapest control (junk tree) was built only post-data by the critic; the registered K1 one-sided controls could not catch a two-sided junk commit. The counter repair the lane already routed to r33 should include a pre-freeze junk control.

## Closure decision

`status=ok` (real report, real committed work, honest final verdict), `admitted=false`, verdict `rejected-honest-stop`: C1 does not verify under its frozen predicate and the counter is provably unsound; C2 verifies. The lane's own honest-stop disclosure is confirmed by independent re-measurement.
