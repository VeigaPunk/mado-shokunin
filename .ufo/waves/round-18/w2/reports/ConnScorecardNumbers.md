# ConnScorecardNumbers — every number the round-18 results must carry

Seat: `MadoR18.ConnScorecardNumbers` (connector, leaf). Date: 2026-10-20.
Scope: collect the numbers for the round-18 SCORECARD results, each with receipt
path and commit. Read-only: no package/service/compositor/input/screenshot/REA
command, no `tools/*` execution, no gate or tripwire run; no tool installed.
Only this report was written. The one derivation I ran outside a committed
receipt is the census histogram (§3), and it is flagged as such.

Revision key (named by hash, never `HEAD`):

- **B** = `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` — baseline.
- **A** = `4c103b55b1ea5c3c555884afe3eb69b5189701b7` — integration; every
  round-18 measurement was made at A.
- **R** = `abfbf35b1ed4d4a1eb294d525ef286be30f3886f` — receipts commit; child of
  A (`git merge-base --is-ancestor A R` → 0). Receipts written after A carry
  `measured_commit=4c103b55…` in their own headers.
- **P** = `6046ab72b18dd0e68c3116cb2c0134ba6f687beb` — round-17 results/harm
  receipts (the 372/372 receipt lives here).
- **K** = `d3a00003e6ef0b1e3c7b4faf52d592eb293857ba` — round-18 pre-registration;
  `git diff K A -- SCORECARD.md` is empty, so the claims read at A are the ones
  written at K.

Convention: "value @ A, receipt @ R" means the receipt records `measured_commit`
A but the file was committed at R. All receipt paths are under
`.ufo/waves/round-18/evidence/` unless another path is given.

## 1. Claim and harm-watch numbers

| # | Number the results must state | Before (B) | After (A) | Receipt path | Receipt commit |
|---|---|---|---|---|---|
| 1 | C1 calibration, literal lesson-citation fraction | 15/23 = **6.5217** | 18/26 = **6.9231** (delta **+0.4014**) | `measure-before.json.txt`, `measure-after.json.txt` | R (raw `measure-before.json` @ A) |
| 2 | C1 denominator / numerator | 23 criteria / 15 cited | 26 / 18 (fraction 0.6923) | same two receipts; `corpus/QUALITY.md` @ A | R / A |
| 3 | C1 new criteria | — | 24, 25, 26 (append-only; each names `lessons/round-18.md` M1/M2/M3) | `corpus/QUALITY.md:131,138,144` @ A | A |
| 4 | C1 lesson rows | — | M1–M6 = **6** rows | `corpus/lessons/round-18.md` @ A | A |
| 5 | C1 mutant bite (R17-V5) | — | 6 mutants, **6 bites**, `no_bite []`, `expectations_met 6`, `baselines_agree true` | `measure-mutants.json` @ A | A |
| 6 | C1 instrument shas | loose `a280b3ab…` @ `f52f43f`; tight `de4c422b…` @ B | same tight `de4c422b…` @ A (measure.py unchanged between B and A) | `measure-mutants.json` `instruments`; header of both measure receipts | A / R |
| 7 | C1 routed receipt re-cut | 5 scan receipts without producer identity | **5/5** scan receipts (`r13`, `r14`, `r15`, `r16`, `anchor-r15`) identical to round 17, now with `RECEIPT … tool_sha256=c87a31ef… measured_commit=A` first line; counts identical; `all_counts_identical true`. `tripwire-pacmanlog-join.txt` is separately re-derived, hand-authored (its line 4 names the tool sha + A, not a `RECEIPT` first line): 4 joined, 5 transactions, 1 unmatched log line (2416) | `recut-summary.json`; `tripwire-r13.txt`, `r14`, `r15`, `r16`, `tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt` | R |
| 8 | C2 rubric V provinces covered | 4/6 = **6.6667** (P3, P5 open) | 6/6 = **10.0** (delta **+3.3333**) | `measure-before.json.txt`, `measure-after.json.txt` | R |
| 9 | C2 P3 route | 0 sources, uncovered | `walker-route-r18.md`, **20** sources `S072–S091` | `measure-after.json.txt` | R |
| 10 | C2 P5 route | 0 sources, uncovered | `theme-route-r18.md`, **4** sources `S092–S095` | `measure-after.json.txt` | R |
| 11 | C2 U-route coverage (finite ceiling, harm watch) | 7/7 = 10.0 | 7/7 = 10.0 (`u_routes 7`) | `harm-measure-u.txt` | R |
| 12 | C3 tripwire tool sha | `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `tripwire-frozen-before.txt`, `tripwire-frozen-match.txt`; `git show <rev>:tools/mado-tripwire.py \| sha256sum` | R |
| 13 | C3 `--frozen` at B | usage error, **exit 2**, `MADO_TRIPWIRE: could_not_evaluate` | — | `tripwire-frozen-before.txt` | R |
| 14 | C3 frozen replay match | absent | wrapper **exit 0** `frozen_match`; `scan_exit 1`, `scan_label findings`; inputs **5/5 ok**; `missing_findings []`, `extra_findings []` | `tripwire-frozen-match.txt` | R |
| 15 | C3 frozen tamper control | absent | **exit 2** `snapshot_tampered`; `inputs ok 4/5` (one byte appended to `inputs/r15-libinput-events.jsonl`) | `tripwire-frozen-tampered.txt` | R |
| 16 | C3 frozen selftest | absent | **17/17** cases passed (`failed=[]`) | `harm-tripwire-round-18-frozen.txt` | R |
| 17 | C3 frozen snapshot composition | — | 5 inputs; **8** expected findings; **3** known misses; `expected_exit 1`, label `findings`; `expected_sha256 4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`; one source line skipped (792,861 B > 256 KiB) | `.ufo/waves/round-18/frozen/expected.json`, `provenance.json` | A |
| 18 | C3 expected-finding multiset | — | 8 = 6 `host_mutation` (3 `sudo`, 2 `pacman:-S`, 1 `pacman:-Sw`), 1 `live_probe` (`wayland-info`), 1 `package_query` (`pacman:-Q`) | `frozen/expected.json` | A |
| 19 | C3 registry row | no `mado-tripwire-frozen` row (0 hits in `SKILL.md` at B) | new row `mado-tripwire-frozen` = **gate** at `SKILL.md:566`; `mado-tripwire` scan row stays **probe** at `:563` | `SKILL.md` | A |
| 20 | Operability gate selftest | 372/372 (receipt measured at `f71ccbe`, gate sha `fba82a66…`; B gate bytes identical, sha `fba82a66…`) | **389/389** (delta **+17**), gate sha `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5` | before: `.ufo/waves/round-17/evidence/harm-legacy-selftest.txt`; after: `harm-gate-selftest.txt` (also `gate-selftest.txt` @ A) | P / R |
| 21 | Classifier (`mado-action-plan.py`) | 52/52 (r17) | **52/52** | `harm-action-plan-selftest.txt` | R |
| 22 | Tripwire scan suites | 9/16/33/30 (r17) | **9/9, 16/16, 33/33, 30/30** | `harm-tripwire-round-17-{core,compound,hardening,w2-regressions}.txt` | R |
| 23 | Frozen suite | — | **17/17** | `harm-tripwire-round-18-frozen.txt` | R |
| 24 | U routes | 7/7 (r17) | **7/7 = 10.0** | `harm-measure-u.txt` | R |
| 25 | Navigation (Counting command) | 32/32 (r17) | **34/34**, missing 0, dangling 0, duplicates 0, coverage **10.0000/10** (denominator grew 32→34: two new indexed notes) | `harm-nav-fleet-round-1.txt`; `corpus/knowledge` and `corpus/README.md` counts @ A | R / A |
| 26 | Census validate | exit 0, 3 W04 (r17) | **exit 0**, 3 historical W04: S030, S042, S045 | `harm-census-validate.txt` | R |
| 27 | Harm watch aggregate | — | **PASS**, 10/10 commands exit 0, rev A | `harm-watch-summary.txt` | R |
| 28 | Pins | — | 6 PIN rows: 5 `state=ok` (gate `c9fb0cef…`, action-plan `226220ae…`, tripwire `c87a31ef…`, round-16 measure `ea3db43f…`, census fleet `3fb72615…`) + 1 `state=extracted` (SCORECARD block) | `harm-watch-pins.txt` | R |
| 29 | Gate regression (routed F10/F14) | pin `cd1d73d7…` | **10/10 KILLED**, 0 SURVIVED, 0 INCONCLUSIVE, flips 0; control GREEN 284/284; `MUTATE_RESTORE: OK`; post-pin `match=10/10` exit 0; derived target **`20714096…`**, 2,460 L / 121,533 B; `PIN_MADO` re-cut `cd1d73d7…` → `20714096…`; `TABLE_MADO` unchanged | `regression-recut.txt` | A |
| 30 | Gate bytes | `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` | `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5` | `git show <rev>:tools/mado-verify.sh \| sha256sum`; `gate-rc-redbefore.txt` | A / B |
| 31 | Saturation / retired | 9.0 / N=3, none retired | **9.0 / N=3 unchanged**, none retired | `SCORECARD.md:270-272` and `:913` @ K | K |
| 32 | Freshness | 29/29 (round 12) | **not re-measured** (carried harm watch; no round-18 receipt) | claims text `SCORECARD.md` @ K | K |
| 33 | Capability entry | — | frozen replay, first-working round **18**; registry row gate | `SKILL.md:566`; §14–17 rows above | A |

All "before" values are read from `measure-before.json.txt` (header
`measured_commit=B`); all "after" values from `measure-after.json.txt` (header
`measured_commit=A`). Both name the instrument
`.ufo/waves/round-17/measure.py` sha256 `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc`,
which I confirmed identical at B and A by `git show`.

## 2. Sources histogram (census + awk, both revisions)

| Metric | B | A | Delta |
|---|---|---|---|
| registry rows | **71** | **95** | +24 |
| tier A | **64** | **88** | +24 |
| tier B | 1 | 1 | 0 |
| tier C | 6 | 6 | 0 |
| status mined | **56** | **80** | +24 |
| status queued | 8 | 8 | 0 |
| status rejected | 7 | 7 | 0 |
| status / tier invalid | 0 | 0 | 0 |
| new row ids | — | `S072`–`S095` (**24**, all tier A, all mined) | +24 |
| P3 credited sources | 0 | 20 (`S072`–`S091`) | +20 |
| P5 credited sources | 0 | 4 (`S092`–`S095`) | +4 |

Row-type split of the 24 new rows: **21 upstream https rows** and **3 host rows**
(`S090` host `/var/log/pacman.log` walker/elephant upgrade lines; `S091` host
walker file bytes; `S095` host P5 theme state). A 200-only URL join I ran
(read-only, in-shell Python over `fetch/*/receipts.jsonl`) found every one of the
21 upstream rows matched by **at least 3** HTTP-200 receipts, none unmatched.

Receipt status for this table: **there is no committed census-histogram output**
in round-18 evidence. `census-start.txt` and the round-17 `census-start/end.txt`
are `validate` runs (W04 lines only), not histograms. The values above were
re-derived in this seat by the commands in §4 from the two committed
`corpus/SOURCES.md` blobs:

- `git show B:corpus/SOURCES.md | sha256sum` = `fec7f698ae4447ee01ff37a7827203ad39331865a2d9fdb21dfa7f9d13fbc593`
- `git show A:corpus/SOURCES.md | sha256sum` = `9552071c0b286075ffabb3a7ea1373e8dbaef5e6c37f906d2620ae83454f26de`
- census tool `scripts/sources-census.sh` sha256 =
  `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`
  (fleet revision `534852203d551f38c68e3a1efd26b6fbe7663267`, as `harm-census-validate.txt` records).

Independent corroboration for the **after** side is committed:
`harm-measure-u.txt` (round-16 `measure.py` sha `ea3db43f…`, `measured_commit=A`)
prints `source_registry.rows 95`, tiers `A 88 / B 1 / C 6`, statuses
`mined 80 / queued 8 / rejected 7`. The **before** side is a re-derivation plus
the round-17 SCORECARD line "Sources 55 → 71 (A 51 → 64, C 3 → 6; mined 43 → 56,
rejected 4 → 7)" at `SCORECARD.md:911` @ K. The two parsers (census and awk)
agree exactly at both revisions.

## 3. Harm watch, command by command

`harm-watch-summary.txt` (R) records `HARM_WATCH: PASS`, `rev=4c103b55…`,
`commands=10`, every line `OK exit=0`.

| Command | Receipt | Observed |
|---|---|---|
| `bash tools/mado-verify.sh --selftest` | `harm-gate-selftest.txt` | `MADO_SELFTEST: 389/389`, exit 0, gate `c9fb0cef…` |
| `python3 -I tools/mado-action-plan.py --selftest` | `harm-action-plan-selftest.txt` | `SELFTEST_SUMMARY: 52/52 passed`, exit 0 |
| `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/compound` | `harm-tripwire-round-17-compound.txt` | 16/16 |
| `… /core` | `harm-tripwire-round-17-core.txt` | 9/9 |
| `… /hardening` | `harm-tripwire-round-17-hardening.txt` | 33/33 |
| `… /w2-regressions` | `harm-tripwire-round-17-w2-regressions.txt` | 30/30 |
| `… .ufo/waves/round-18/tripwire/frozen` | `harm-tripwire-round-18-frozen.txt` | 17/17 |
| `python3 .ufo/waves/round-16/measure.py A` | `harm-measure-u.txt` | U `count 7`, `score 10.0`; source rows 95 |
| `bash -s < SCORECARD Counting-command @ A` | `harm-nav-fleet-round-1.txt` | `indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | `harm-census-validate.txt` | exit 0; W04 S030/S042/S045; `ok` |

## 4. Commands and observed output (reproducible)

Read-only git and text processing; no measurement tool was executed except the
census (authorized by this item as "census + awk").

```console
$ for r in d9a5a18 4c103b5; do
    git show $r:corpus/SOURCES.md | awk -F'|' '/^\| S[0-9]+ \|/ {
      gsub(/^ +| +$/,"",$5); gsub(/^ +| +$/,"",$9); n++; t[$5]++; s[$9]++ }
    END {printf "rows=%d A=%d B=%d C=%d mined=%d queued=%d rejected=%d\n",
      n,t["A"],t["B"],t["C"],s["mined"],s["queued"],s["rejected"]}'; done
REV=d9a5a18
rows=71 A=64 B=1 C=6 mined=56 queued=8 rejected=7
REV=4c103b5
rows=95 A=88 B=1 C=6 mined=80 queued=8 rejected=7

$ scripts/sources-census.sh census --file /tmp/census-r18.*/d9a5a18….md mado
file rows 71 / tier.A 64 / tier.B 1 / tier.C 6 / status.mined 56 / queued 8 / rejected 7
FLEET rows 71 / tier.A 64 / tier.B 1 / tier.C 6 / tier.invalid 0 / status.mined 56 / queued 8 / rejected 7 / invalid 0 / missing 0
exit 0
$ scripts/sources-census.sh census --file /tmp/census-r18.*/4c103b5….md mado
file rows 95 / tier.A 88 / tier.B 1 / tier.C 6 / status.mined 80 / queued 8 / rejected 7
FLEET rows 95 / tier.A 88 / tier.B 1 / tier.C 6 / tier.invalid 0 / status.mined 80 / queued 8 / rejected 7 / invalid 0 / missing 0
exit 0

$ git show d9a5a18:tools/mado-verify.sh | sha256sum
fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207  -
$ git show 4c103b5:tools/mado-verify.sh | sha256sum
c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5  -
$ for r in d9a5a18 4c103b5; do git show $r:.ufo/waves/round-17/measure.py | sha256sum; done
de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc  -   (twice)
$ for r in d9a5a18 4c103b5; do git show $r:tools/mado-tripwire.py | sha256sum; done
962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072  -   (B)
c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb  -   (A)

$ for r in d9a5a18 4c103b5; do git ls-tree --name-only $r:corpus/knowledge | grep -c '\.md$'; done
32
34
$ for r in d9a5a18 4c103b5; do git show $r:corpus/README.md | grep -cE '^\| `knowledge/[^`]+\.md`'; done
32
34

$ python3 -c '<expected.json parse>'
inputs 5 findings 8 known_misses 3 exit 1 label findings
sha256(expected.json) = 4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9
$ python3 -c '<frozen match/tampered parse>'
match:    exit 0 outcome frozen_match scan_exit 1 scan_label findings inputs_ok 5/5
tampered: exit 2 outcome snapshot_tampered inputs_ok 4/5

$ python3 -c '<measure-mutants summary>'
{"mutants":6,"bites":6,"no_bite":[],"expectations_met":6,
 "expected_but_unmet":[],"unexpected_tight_only":[],"baselines_agree":true}

$ git merge-base --is-ancestor 4c103b55… abfbf35b… ; echo $?
0
$ git diff d3a0000 4c103b55… -- SCORECARD.md | wc -l
0
```

## 5. Precision notes (contradictions stated, not smoothed)

1. **The histogram is the only new round-18 results number without a committed
   receipt.** §2's table is reproducible from the two `SOURCES.md` blobs, but no
   `evidence/census-histogram.txt` exists. Do not cite `census-start.txt` /
   `census-end.txt` as its receipt: those are `validate` runs that print only the
   three W04 warnings. Either commit a census output at the results commit or
   mark the sentence "re-derived (blob sha + census tool sha, §4)".
2. **"372/372 at d9a5a18" is a byte-identity inference, not a run at B.** The
   receipt `harm-legacy-selftest.txt` says `measured_commit=f71ccbe` and gate sha
   `fba82a66…`; I verified `d9a5a18:tools/mado-verify.sh` hashes to the same
   `fba82a66…`. The results sentence must bind the 372 to `f71ccbe` and state the
   byte identity to B, or it reproduces the R17-V1 class (a receipt cited for a
   revision it does not name).
3. **Navigation's denominator moved 32 → 34.** `corpus/knowledge` has 32 notes at
   B and 34 at A; `corpus/README.md` has 32 and 34 indexed rows. So 34/34 is
   complete on a larger set, not "32/32 unchanged". Do not report it as harm or
   as a score change (the score is 10.0000/10 at both).
4. **C3's "registry row moves `probe` → `gate`" is inaccurate as a move.** At B
   `SKILL.md` has **zero** `mado-tripwire-frozen` rows; at A `:566` is a new row
   at `gate`, while the `--scan` row `mado-tripwire` at `:563` remains `probe`.
   The results should say "new registry row at gate".
5. **C2's "each new credited row backed by a committed raw fetch receipt" is
   overbroad.** 3 of the 24 credited rows are host rows (`S090`, `S091`, `S095`)
   and have no fetch receipt by design. The accurate line is "21 upstream rows,
   each URL-matched by ≥3 HTTP-200 receipts; 3 host rows by host file bytes".
6. **Fetch verification is partial and volatile.** The w1 verifier report
   (`.ufo/waves/round-18/w1/reports/FetchVerify.md`) records
   `SUMMARY receipts=294 ok=294 bad=0` at `2026-10-20T15:45:32Z` but it joined
   only S056–S069; S072+ did not exist then. At my read (wave 2 still writing) the
   tree had 48 seat dirs, 46 with `receipts.jsonl`, 407 receipt lines:
   399 HTTP-200, 6 HTTP-404, 2 HTTP-403. My 200-only join backs all 21 upstream
   rows, but there is no committed per-row join for S072–S095 and no committed
   verifier summary over them. Do not claim either.
7. **`receipt-claims.json` references six receipts that do not exist.** Its
   `PENDING-L1` names are `tripwire-{r13,r14,r15,r16,anchor-r15,pacmanlog-join}-recut.txt`;
   the re-cut wrote the five scan receipts in place under their round-17 names
   with `RECEIPT` headers, and re-derived the pacmanlog join with a
   `# receipt:` comment line. `ls evidence | grep -c recut` = 2
   (`recut-summary.json`, `regression-recut.txt`). Any results line citing
   `receipt-check.py` / `EXPECT_SUMMARY` must be re-pointed or omitted; the w1
   `EXPECT_SUMMARY: 9/15` is a pre-integration run.
8. **Frozen carries two exits.** `expected_exit` is **1** (a finding verdict,
   `scan_label findings`); the `--frozen` wrapper exits **0** on `frozen_match`.
   `tripwire-frozen-match.txt` prints both (`exit 0`, `scan_exit 1`); the results
   must too, or a reader will think the scan was clean.
9. **Do not cite the w2 gate receipt.** `.ufo/waves/round-18/evidence/w2-gate-selftest.txt`
   (389/389) is untracked (empty `git log` for the path). Cite
   `harm-gate-selftest.txt` @ R.
10. **Raw vs producer-header measure receipts.** `measure-before.json` is at A
    (raw JSON); `measure-before.json.txt` is at R and carries the `RECEIPT` line.
    Criterion 24 needs the `.txt`; both record B.
11. **The re-cut `RECEIPT` timestamp is not ISO-8601.** Its `utc=` is
    `Tue Oct 20 15:55:51 UTC 2026`; only the fetch receipts use `…Z`. Do not
    describe the re-cut receipts as ISO-stamped.
12. **Replace the claim placeholders.** The claim text's `N/N` for the frozen
    suite is **17/17**; its 372/372 must be reported as the pre-fix count with the
    389/389 post-fix count and the `+17` delta (the OM9/OM10 assertions).
13. **`expected_sha256` in the frozen receipts is the digest of `expected.json`**
    (`4f3534ae…`), not a transcript digest; the input digests are the five
    `inputs[].sha256` values.
14. **Freshness 29/29 has no round-18 receipt.** It is carried from round 12 and
    explicitly not re-measured; the results must not present it as a round-18
    measurement.

## 6. Lane-hygiene disclosure (self-reported)

This seat's first `write` of this report resolved a relative path against the
fleet root and landed at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-18/w2/reports/ConnScorecardNumbers.md`.
No lane byte was affected; the file was moved to the lane path
(`mado-shokunin/.ufo/waves/round-18/w2/reports/ConnScorecardNumbers.md`) and the
fleet-root copy deleted. A **sibling's** misrooted file remains at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-18/w2/reports/ReviewWalkerUpstream.md`
(21,617 B, not mine to move); L1's misroot sweep should relocate or remove it.

## 7. One bounded move (connector proposal)

**Move.** Commit one `evidence/census-histogram.txt` at the results commit and
make the SCORECARD sources sentence cite only that file: it should contain the
two §4 census invocations (or `--file` equivalents), the awk cross-check, the two
`SOURCES.md` blob shas, the census tool sha plus its fleet revision
(`5348522…`), and the 21-upstream / 3-host split of `S072–S095`. Fold the C2
wording fix (note 5) into the same sentence.

**Affected axes.** Calibration (removes the last results number with no producer
receipt; QUALITY 24 then covers the sources sentence too); coverage (histogram
and row classification become checkable by a non-author); operability (no change,
no runtime path touched).

**Risks.** (a) The census tool is fleet-rooted, so the receipt must name
`fleet:5348522…` as the tool revision and the two lane blobs by sha, or a lane
reader will mis-anchor it. (b) The file will keep growing while wave 2 writes;
pin blobs by sha, never by path or row count. (c) A lane `--file` census cannot
check E11 `used-by` paths; keep the existing `validate --root` receipt separate
rather than merging the two modes.

**Verification.** Re-run the §4 commands verbatim; confirm the two printed
histograms (71/64/1/6/56/8/7 and 95/88/1/6/80/8/7), the two `sha256sum` blob
digests, and that `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
still exits 0 with exactly the three historical W04 lines.
