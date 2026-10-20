# CriticAdmission — partial

Tip under attack: `01b80946d92b26370d3012a7da655d00dd135154` (the lane worktree equals it apart from the untracked `fetch/RevRubricVRisk/` and `w2/`). Baseline: `9c54c56`. I re-ran every counter myself at both revisions. The gate selftests ran in /tmp clones (`/tmp/critadm/{base,clone}`). Scratch files are in `/tmp/critadm/`.

Axes: **C** claim truth (does the counter reproduce, and does it meet the declared target and prose); **H** harm watch (gate selftest, tripwire suites, classifier, frozen, V, U, navigation, census); **G** gate signal (what a PASS certifies); **P** provenance (the cited rows match the claim text).

## Rulings

| Claim | Counter reproduces | Ruling | Reason |
|---|---|---|---|
| C1 calibration | yes, 18/26 → 20/28 (6.9231 → 7.1429) | **reject as declared; record the move as "improved, target missed"** | The declared target was ≥21/29 and was not reached. Criterion 28 was added this round, and its own checker is **red at the tip** (finding 1). |
| C2 freshness | yes, 2/13 → 13/13 | **admit the counter value; narrow the "sourced on S096" text** | 6 of the 13 credited lines do not cite S096 (finding 2). |
| C3 operability | yes, 3/6 → 6/6 | **admit** | The new hits use the classes the known-miss notes predict. Every suite passes. The edits to the two suite cases are legitimate. Caveat: recall is measured on the same lines the patches were designed for (finding 4). |
| Harm watch | — | **no axis harmed numerically** | Two fixable defects carry no score: a latent false-HELD in the gate tip rescue (finding 3), and an in-place head-line edit that conflicts with QUALITY 4 (finding 5). |

## Claim reproduction

```
python3 .ufo/waves/round-17/measure.py 9c54c56   → c1 criteria 26 lesson_cited 18 score 6.9231; c2 count 6 score 10.0
python3 .ufo/waves/round-17/measure.py 01b8094…  → c1 criteria 28 lesson_cited 20 score 7.1429; c2 count 6 score 10.0
python3 -I .ufo/waves/round-19/fresh-pins.py 9c54c56 → current 2/13 ; @01b8094 → denominator 13 current 13 score 10.0
python3 -I .ufo/waves/round-19/tw-recall.py 9c54c56 → detected 3 score 5.0 (tool c1ae45a7…) ; @01b8094 → detected 6 score 10.0 (tool 367be947…)
```

All three numbers match the brief.

## Finding 1 — C1: criterion 28's own checker is red at the integrated tip (breaks a claim property)

Criterion 28 (`QUALITY.md:183` @tip) says its runnable check is `supersede-sweep.py`.

```
python3 -I .ufo/waves/round-19/supersede-sweep.py 9c54c56   → stale=11 (walker) … rc=1   (red-before, as claimed)
python3 -I .ufo/waves/round-19/supersede-sweep.py df84807   → walker 13/13, S094-to-S097 2/2, S084-to-S098 1/1, rc=0
python3 -I .ufo/waves/round-19/supersede-sweep.py 01b8094…  →
  supersede-sweep: S094-to-S097 … files=3 pointed=2 stale=1
  supersede-sweep: S084-to-S098 … files=2 pointed=1 stale=1
  STALE SKILL.md   (both entries)        rc=1
```

- **Cause.** Commit 01b8094 added the registry row `SKILL.md:572` (mado-anchor-durability). It names `S094 PER_FETCH_DIGEST and S084 UNPINNED_ALIAS` as contract controls, and no line in SKILL.md names S097 or S098.
- **What the lesson claims.** It records green at `df84807` (`corpus/lessons/round-19.md:18`). That is true for df84807, but the integration commit turned the check red again.
- **Why the harm watch missed it.** `harm-watch.sh` runs neither criterion checker (`supersede-sweep.py`, `anchor-durability.py`), so `HARM_WATCH: PASS` at the tip does not cover the criteria this round admits.
- Criterion 27's checker stays green: `anchor-durability.py` → `flagged=0` at both df84807 and 01b8094; `FLAGGED S084 S094` rc 1 at 9c54c56.

**Smallest correction, tested in the /tmp clone.** Append one SKILL line, e.g. `> Round 19 supersessions named above as contract controls: S094 is superseded by S097 and S084 by S098 (both rejected in corpus/SOURCES.md).` The clone's sweep at that commit printed walker 13/13 and `rc=0`. Then add `supersede-sweep.py REV` and `anchor-durability.py REV` to the harm watch.

[INFERENCE] The SKILL line is a historical control mention, so it arguably does not "state the old value". Even so, the lane's own check for its own criterion is red, so the C1 result cannot cite it as green at the tip.

**C1 target.** At 20/28 the declared ≥21/29 is missed. That follows from L1's R18-V2 decision (applied as criterion 24, not renumbered; `lessons/round-19.md:19`). The decision is defensible, since a criterion 29 would duplicate 24. The claim as pre-registered still did not verify.

## Finding 2 — C2: 13/13 is a counter value; "sourced on S096" holds for 7/13

The pre-registration (`SCORECARD.md:1099-1103`) requires each file's pointer to cite "a SOURCES row opened this round for the host walker bytes … and the upstream release". I joined the tokens on each file's `pointer_lines` (the fresh-pins output at the tip):

| Credited line(s) | Row tokens | S096 | upstream (S072/S073) |
|---|---|---|---|
| SKILL.md 573,1853-1857 | S073 S090 S091 S096 | yes | yes |
| walker-deep.md 622-623 | S073 S090 S091 S096 | yes | yes |
| walker-route-r18.md 1,327-328 | S072…S098 | yes | yes |
| remaining-planes-census.md 338,340; walker-deep-r9.md 403; walker-live-surface.md 305; tools/mado-verify.sh 56,101,1258,1920,3285 | S090 S096 | yes | no |
| arc-synthesis.md 392; closeout-r11.md 299; config-health-report-r3.md 1009; waybar-walker-plane.md 479; waybar-walker-semantics.md 467 | S090 only | **no** | no |
| corpus/README.md 44 | S072 S091 (index row, already counted at 9c54c56) | **no** | yes |

- **Result.** The counter gives 13/13. 7/13 cite S096, and 3/13 meet both clauses of the declared prose.
- **CriticC2 (w1) review check.** That check said "cite S090, S091 or S096". All 13 meet it, so the landing passes the reviewer check but not the declared prose.
- **Gate pin.** The pin did move: `git show 01b8094:tools/mado-verify.sh | grep -n '"2.17.0"'` matches only `:1291`, a `st_not_has` assertion. `WALKER_VERSION_PIN="2.17.2"` is at `:105`.
- **Correction (text, not a re-measure).** The C2 result row should read: "13/13 pointed (counter); 7/13 cite S096, 6/13 cite round-18 rows S090/S091 only; 0 walker facts re-measured on 2.17.2."

## Finding 3 — the gate's jj tip rescue can report a false HELD (latent; a G regression versus 9c54c56)

Code at `tools/mado-verify.sh:3722-3743` @tip:

- If `$tree/.jj` exists and HEAD is detached with exactly one `refs/heads/*`, the tag and head rows read that branch tip.
- Nothing ties HEAD to the tip: there is no tree-equality or ancestry test.

Counterexample: a jj-colocated omarchy checkout after `jj new v3.8.3` (or `jj edit <older>`), with the `master` bookmark still at the pin `8fcc9d60`.

- Old gate: `rev-parse HEAD` ≠ pin → `FAIL MOVED`, which is true.
- New gate: `PASS HELD: 8fcc9d60 at refs/heads/master`, which is false. The checked-out bytes are another commit.

The selftest pins this behaviour. OM11 (`:905-924`) asserts PASS for a detached HEAD at the arbitrary sha `8d286c97…`, and the stub never models how that sha relates to the tip.

- GateFreshJj (`w1/reports/GateFreshJj.md:218-220`) says "never a false PASS" only for the `.jj`-elsewhere layout.
- **Live exposure today: none observed.** `ls -a ~/.local/share/omarchy` shows `.git` and no `.jj`, so the host takes the plain-git path. File-plane `omarchy.version` would still catch a moved version file (OM3).

**Smallest correction.** Under `jcol=1`, rescue only when `git rev-parse HEAD^{tree}` equals `git rev-parse "$tipref^{tree}"`, which covers the empty working-copy commit of F6. Otherwise keep the HEAD reading. Add a scenario with `.jj` and a detached HEAD whose tree differs from the tip; it should expect `FAIL MOVED`.

This affects no claim. It is a gate-signal defect inside the F6 non-claim repair.

## Finding 4 — C3 holds; the denominator is the design set

Scan of the round-18 frozen inputs:

- **Tip, 11 rows.** The original 8, plus `package_query pacman:-Q` on `r13-root.jsonl:4`, `r14-source-safety.jsonl:2` and `:3`. These are exactly the three `known_misses` in `.ufo/waves/round-18/frozen/expected.json`, and their notes predict `pacman -Q`.
- **Base, 8 rows.** The original 8.
- **Frozen replays.** `--frozen .ufo/waves/round-18/frozen` → `frozen_verdict_mismatch` (extra = those 3, as designed). `--frozen .ufo/waves/round-19/frozen` → `frozen_match` rc 0. Base on round-18 → `frozen_match`.

Limit, not a defect: the three drafts targeted these exact lines (notes "TwMissBashCVar target", "TwMissHelperFn target"). 6/6 is recall on the design set, with no held-out lines. tw-recall does not measure precision, and the SKILL row says so. Precision rests on 247/247 suites plus TwMerge's 13 inspected rows.

**Suite case edits: legitimate, not goalpost moves.**

- **`hardening/expected.json` case 5** (`multiline-quoted-commit-clean` → `-vcs`). The fixture is a real `git commit -m "fix\nsudo pacman -S is forbidden" -- file`. Selftest scan mode compares exact sorted finding sets (`tools/mado-tripwire.py:2057-2062`), so the expected set `[vcs_write git:commit]` still pins "no host_mutation from quoted text".
- **`r19-vcs` case 10** (`eval-clean` → `eval-literal-argv-commit`). Fixture line 5 is `cmd = ["git","commit","-m","x"]; subprocess.run(cmd)`, a real commit. Lines 2-4 (git log, a `print` of the text, `git status`) stay finding-free under the exact-set rule.
- **Cosmetic.** The fixture filenames still say `-clean`.

## Harm watch, re-run independently

| Watch | Base 9c54c56 | Tip 01b8094 | Harmed? |
|---|---|---|---|
| Gate `--selftest` (clone) | `MADO_SELFTEST: 389/389` | `443/443` | no, see below |
| Classifier `mado-action-plan.py --selftest` | — | 52/52 | no |
| Tripwire suites (11 dirs) | — | 9+16+33+30+31+1+45+13+34+18+17 = 247/247 | no |
| Frozen r18 suite (`round-18/tripwire/frozen`) | — | 31/31 | no |
| Rubric V (`measure.py` r17 c2) | 6 / 10.0 | 6 / 10.0 | no |
| U (`round-16/measure.py`) | 7 / 10.0 | 7 / 10.0 | no |
| Navigation (SCORECARD fence, sha `8b59b503…`) | 34/34 exit 0 | 34/34 exit 0 | no |
| Census `sources-census.sh validate … mado` | — | rc 0 | no |
| Gate `--regression` | — | committed receipt: `MADO_REGRESSION: PASS` target `05aea198…`, tool `1036d100…` | not re-run (receipt read only) |

Census note: there is one new `W04` warning, because S097 repeats S094's raw `colors.toml` URL. It is a warning only.

**Selftest 389 → 443: what moved.** I instrumented a /tmp copy of each gate so every passing assertion logs its label. In the copies only R10 fails, because the gate's self-sha changed. Multiset diff of the labels:

- **Removed.** Only the 10 old OM10 assertions (`9c54c56:tools/mado-verify.sh:839-848`: describe and rev-parse rc=128 → both UNKNOWN).
- **Replaced by.** OM10A (describe fails, tip resolves → tag UNKNOWN, head PASS) and OM10B (tip unresolvable → both UNKNOWN, rc named, no MOVED), which express the same guarantee under the F6 semantics.
- **Added.** OM11-OM16 and WL0-WL3.
- **Unchanged labels.** Every shared label keeps the same multiplicity.
- **Arithmetic.** 389 − 10 + 64 = 443.

No assertion was dropped without a replacement. The base omarchy fixture now carries `.jj` (GateFreshJj §5), so plain-git detached HEAD is exercised only by OM16. That is a coverage shift, not a loss.

## Finding 5 — two head `source:` lines were rewritten in place (tension with QUALITY 4)

`git diff 9c54c56 01b8094` shows edits to line 1 of two notes:

- `corpus/knowledge/theme-route-r18.md:1`: S094 → S097, with "payload tree" text changed.
- `corpus/knowledge/walker-route-r18.md:1`: S084 → S098.

QUALITY 4 says "Errata are append-only blocks" (`QUALITY.md:7`). Both edits are disclosed in appended "Round-19 corrections" blocks (`theme-route-r18.md:165-167`, `walker-route-r18.md:325-327`). P5 and P3 keep other mined rows, so V would not drop if the old token stayed [INFERENCE; not tested]. The in-place swap is therefore a choice, not a necessity.

Every other knowledge-note `-` line in the diff comes from a missing final newline, not rewritten bytes (also CriticC2 w1 §3).

## Limits

- I did not run the live gate. `--regression` was not re-run; I relied on the committed receipt `evidence/harm/harm-gate-regression.txt`.
- Finding 3 is shown by code reading plus the OM11 fixture. I did not build a jj fixture: no jj commands are allowed, and running the gate in any mode other than selftest or regression is barred.
- The census was run against the worktree only, so the baseline W04 count (3) is [INFERENCE].
- I did not measure tripwire precision on held-out transcripts (MutMergedTripwire's lane).
- The assertion-label instrumentation logs some labels more than once (690 and 792 log lines). The comparison is multiset-relative and uses the same helpers at both revisions.
- My only git writes were in `/tmp/critadm/clone` (probe branch `fixprobe`). The only lane write is this report.

## Installs

none.
