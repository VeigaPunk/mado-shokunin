# CriticC2Inflation — 29 is real, 30 is inflation: its normative core restates criterion 10 and its flagship red is false

Reviewed at lane tip `e629f73` (HEAD). Ran `python3 .ufo/waves/round-17/measure.py e629f73` (c1: 20/28, 7.1429), ran `.ufo/waves/round-20/isolation-check.sh` on both harnesses, reproduced the `set -e`/`&&` mechanism and three harness-mutant verdicts. `tally-check.py`/`tally-claims.json` are unlanded at this tip — criterion 30's runnable check does not yet exist.

## Verdict per criterion

| Criterion | Judgment |
|---|---|
| 29 (fail-closed isolation harness) | **Discernment** — novel requirement, real red artifact, check demonstrably fails. Three check gaps need closing before it bites fully. |
| 30 (re-derived stated counts) | **Inflation, as drafted** — the first clause restates criterion 10 (round-12 M7); the pre-registration's non-restatement screen named only 24/27/28 and missed the direct hit on 10/6. Its flagship red (5/13 → 8/13) compares unlike revision + unlike counting rule: a false red the criterion's own second clause would forbid. |
| 22/30 target | **Goal-seeked by construction** — measure.py is a regex, so 22/30 is authored, not measured; the target pre-commits to two new numbered criteria, foreclosing R19-V1's no-duplicate disposition. |

## Counterexample 1 (the decisive one): criterion 30 ≈ criterion 10

`corpus/QUALITY.md:16`:
> `10. Report each count as `<n> — <command> <date>` and rederive it from the named revision instead of transcribing a prior summary.`

Draft criterion 30, first clause (`w1/drafts/ScribeQuality.md:12`):
> `A count stated in a SCORECARD, lesson, or report claim is re-derived at the measured revision by a cited command`

Same norm. `SCORECARD.md:1270-1273` ("neither criterion restates 24, 27 or 28") screens the three *most recent* criteria and stops; criterion 30's verbatim overlap is with criterion **10** (and the "re-derivation command" half of criterion **6**). R19-V1 (`corpus/lessons/round-19-verifier-spotcheck.md:149`: "Do not add a duplicate criterion") is violated in fact if 30 lands as drafted. Sibling `w1/reports/RevCriterion30.md` reached the same conclusion independently; this seat verified the text overlap directly.

What remains genuinely new in 30: the *counting-rule disclosure* clause ("names its counting rule whenever two defensible rules give different values"). That is a distinct norm no prior criterion states. The smallest safe correction is RevCriterion30's narrowed line (claim revision + population + predicate + selection rule), or — cleaner under R19-V1 — an append-only extension note under criterion 10 with no new number, following the precedent at `corpus/QUALITY.md:192-204` where R18-V2 was applied under 24 "with no new number" rather than granted criterion 29.

## Counterexample 2: the planned S096 red compares unlike terms

Draft red (`w1/drafts/ScribeQuality.md:14`): `SCORECARD.md:1167` "5/13 name S096 on the crediting line" is red because it re-derives to 8/13 / 6/13. Verified:

- The claim is scoped: `SCORECARD.md:1163` — "Wave 2 (67 seats over `01b8094` …)".
- Its measuring rule is *S096 cited as evidence* (tally line, `.ufo/waves/round-19/w2/reports/RerunC2.md:72`), not "S096 on a `2.17.2`-containing line".
- The 8/13 / 6/13 figures are measured at a *different revision* (`b435568`) under *different rules* (any-matching-line / first-matching-line, `round-19-verifier-spotcheck.md:59`).

A registry entry that marks `SCORECARD.md:1167` MISMATCH against a `b435568` any-line re-derivation is a **false red**: the claim as scoped may be true at `01b8094` under its rule. Worse, it instantiates the exact failure the criterion's own second clause prohibits — comparing two defensible rules without naming which was used. If the checker ships this entry, criterion 30's first credited act is a criterion-30 violation. Fix: registry needs `claim_rev` and `rule` per entry (gen_w1.py:93's schema has only `statement.rev/path/line_regex`, `stated`, `derive.argv` — `statement.rev` binds where the text lives, not the revision the *count* describes); register the `b435568` 8/13 as a *new* claim with the any-line rule named, and keep the `01b8094` 5/13 under "cited-as-evidence" as historical.

The other two reds are grounded: 155-vs-154 (`corpus/lessons/round-19.md:124` vs receipt `9572d2a6…`, 154 `files` entries — seat `len(files)=154` agrees with RevCriterion30's parse) and ten-vs-nine (`SCORECARD.md:1225` vs nine labeled occurrences/eight distinct at `9c54c56`, `round-19-verifier-spotcheck.md:88`).

## Counterexample 3: the counter can't distinguish 22 from padding — and the target assumes padding survives

`measure.py:92-93` scores `^[0-9]+\. .*lessons/` — a line mentioning any `lessons/` path counts as cited. It cannot detect (a) a nonexistent anchor (`lessons/round-20.md` does not exist at `e629f73`; `corpus/lessons/` ends at round-19 files), (b) a duplicate criterion, (c) a criterion whose check never lands or never fails. ScribeQuality's own placement note (`drafts/ScribeQuality.md:17`) documents score-by-construction: "so the QUALITY counter … reads 30 criteria and 22 lesson-cited, the pre-registered C2 target 22/30". The score rise is *guaranteed the moment the lines land* regardless of substance; discernment is entirely delegated to the closure reviewer, which is exactly where R19-V1's suspicion belongs.

Sharper still: the registered target `22/30` presumes both new criteria survive as *numbered* lines. If the Rust judge applies R19-V1 literally and 30 merges under 10, the honest end-state is 21/29 — the number the pre-registration cannot distinguish from round 19's standing miss. A target written as "20 + N_new_distinct / 28 + N_new_distinct, ≥ 22/30 only when both criteria are outside-ruled non-duplicate" survives any disposition; `22/30` as written creates pressure to keep a duplicate numbered rather than lose the target.

Additional weak points in the authored count: criterion 30's lesson anchor cites `lessons/round-20.md#mistakes M2`, but ScribeMistakes' draft assigns M2 to the *harness* mistake and M3 to stale tallies (`w1/drafts/ScribeMistakes.md:8-9`) — the regex credits the line either way; the citation is wrong in substance. Same class of defect as the round-12 provenance note already records (`QUALITY.md:28-30`, criterion 8's miscited anchor).

## Criterion 29 — genuine, but the landed check has three gaps

Verified by execution (payloads were `/tmp` canaries only; no host binary touched):

- **Red reproduces.** `isolation-check.sh evidence/inns-r19-shape.sh` → `FAIL_OPEN`, canary created, harness exit 0, check exit 1. The mechanism is real: `set -e` does *not* abort on a failing non-final `&&` member — reproduced standalone (`set -e; [ -e /nonexistent ] && false && echo armed; echo PAYLOAD-RAN` prints `PAYLOAD-RAN`, exit 0). Fidelity to the incident confirmed by `w1/reports/RevengeInnsHarness.md` against the transcript heredoc (jsonl line 34).
- **Green reproduces.** `isolation-check.sh isolate.sh` → `FAIL_CLOSED` (exit 125, no canary) + `POSITIVE_CONTROL_OK`.
- Novel requirement: no prior criterion covers harness/actuator semantics (24-26 cover receipts/status propagation; 27-28 cover anchors/sweeps). Grounded on R19-V4, a real closed-routed defect.

Gaps, smallest-first:

1. **exit-0-no-canary reads `COULD_NOT_EVALUATE`, not FAIL_OPEN** (`isolation-check.sh:59-67`). Verified: a skip-shaped harness (setup fails silently, payload never runs, `exit 0` — the `chousa research-gate.sh:4666-4671 tnscase` shape `w1/reports/ConnSiblingIsolation.md:27` names as a real red) produces `COULD_NOT_EVALUATE … (exit 0, canary absent)` → exit 2, not 1. Per the connector's red-3, exit 0 after a failed arming *is* fail-open — the harness reported success without isolation. One-line fix: canary-absent + exit 0 ⇒ `FAIL_OPEN` (reserve COULD_NOT_EVALUATE for indeterminate states, or drop it).
2. **PATH injection only reaches harnesses that resolve `mount` via PATH.** A harness calling `/usr/bin/mount`, `command -p mount`, or sanitizing PATH before `unshare` is immune to the failure stub; the check then reads whatever real mount does (on this host, success → FAIL_OPEN mislabel risk is low, but the injection is silently vacuous). Verified the `unset -f mount` guard *does* work against exported `BASH_FUNC` mounts (probe: exported `mount(){ exit 0; }` was scrubbed, PATH stub fired — FAIL_CLOSED on isolate.sh). Complement with a real-mount failure arm: pass a nonexistent or non-mountable `--target` so `mount --bind` fails for real (see 3).
3. **The draft's second red arm was dropped.** `w1/drafts/ScribeQuality.md:9` plans an absent-target arm to catch the `[ -e ] || continue` skip (the post-fix transcript shape at jsonl `:36`, which still `exec`s with zero targets armed); `isolation-check.sh` implements only the mount-failure arm. Adding the missing-target arm also fixes gap 2 for ungated harnesses (real mount fails on the missing path) — two birds, one fixture. Minor: partial-arm (N targets, mount k fails) is untested; the draft's "every arming step is tested" clause arguably requires it, but ConnSiblingIsolation's three-fixture proposal is the higher-value expansion.
4. Name drift to fix in the criterion text: draft cites `harness-fail-closed.py` and `count-rederive.py`/`count-claims.json`; landed/assigned names are `isolation-check.sh`, `isolate.sh`, `tally-check.py`, `tally-claims.json`. `ScribeQuality.md:27` report confirms the draft names are stale.
5. Criterion 30's checker is **entirely unlanded** — TallyCheck's deliverables (`tally-check.py`, `tally-claims.json`) are absent at `e629f73`. The C2 claim's "runnable check" is currently runnable for 29 only.

## What would make C2 genuine rather than inflation

1. **30 narrowed or folded.** Either adopt RevCriterion30's narrowed line (rule/revision/population disclosure — novel) or append it under criterion 10 with no new number, and accept a target of `21/29`-shaped form. Keeping broad-30 numbered *is* the inflation R19-V1 anticipates: +1 numerator point for a restated norm.
2. **Registry entries carry `claim_rev`, `rule`, `population`.** The S096 entry must be re-scoped (claim at `01b8094` under cited-as-evidence vs new claim at `b435568` under any-line) or it demonstrates the criterion's own violation.
3. **Checker must exist and red before the criterion scores.** Land `tally-check.py` + the registry with the two grounded reds (154, nine-labels) and the corrected S096 entry; receipt the red run.
4. **29's check gets the missing-target arm and treats exit-0-no-canary as FAIL_OPEN**, matching the criterion text's "missing or unverified target is a setup failure" clause — currently a harness that skips arming and exits 0 is merely inconclusive.
5. **Anchor `M3`, not `M2`,** and only after `corpus/lessons/round-20.md` lands; the regex will not catch the wrong row.
6. **Report the semantic count alongside the literal** (criterion 22): "22/30 literal; semantic: 21/29 + one extended criterion" — this is the disclosure that turns a constructed number back into a measurement.

## Limits

- Did not run `tally-check.py` (unwritten); criterion-30 check critique is from spec (`gen_w1.py:93`), draft, and direct re-derivation of the claim texts.
- Did not re-run RerunC2's counter at `01b8094`; the "5/13 may be true at `01b8094` under its rule" point is grounded in the claim's own scope text and table, not a re-measurement.
- Harness tests used `/tmp` canaries and a PATH-injected `mount` stub only; `unshare`/`mount` on real targets were not exercised. Did not test root-capable namespace behavior.
- measure.py semantic/literal divergence confirmed by reading the regexes and the placement note, not by landing criteria.
- Checked for restatement against criteria 6-28 by direct read of `corpus/QUALITY.md`; criterion-30's overlap with 10 (and partially 6) is the found instance; no second-order duplicate of 29 found.

## Installs

none
