author: hyaku closure (non-author integrator, @m_opus)

# Round 19 — non-author verification and admission decision

Date: 2026-10-20. Integrator: ClosureMadoR19; independent read-only reviewers GateOm10Check, TripwireCaseCheck, IncidentCheck, DiscernmentCheck were dispatched by this closure, not by mado. No lane-authored file was changed. No gate, selftest, regression, live compositor operation, package query, or package transaction was executed by this closure. No tools were installed. Only registered measurement/scan probes were executed; their temporary fixtures were removed.

## Decision

**status: ok; admitted: false; verdict: rejected-harmed.** This is substantial committed work, not a marker. All three reported counter deltas reproduce, but counter success is not the entire pre-registered claim or the no-harm condition. C1 missed its target; C2's all-file new-source requirement remains unmet; C3 trades greater bounded recall for an independently demonstrated new false positive on pure data. Honest disclosure does not waive the no-trade admission rule (AXES.md §Working the axes, PROTOCOL.md §Evidence/Gate standards).

Reviewed baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`, landed round tip `b435568540f9a28f4f7bb902af8dbe6a5b084dfe`, and final tool revision `7b4839d31d60af5bac40e3e74aec70e928601dfc`.

## Step-1 conformance

- `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %s' -- .ufo/reports/round-19/mado.md` returned `mado-shokunin <mado@shokunin.local> 3b7be51dac75ddb84c484968326f5df79c3acc0e round-19: mado report`.
- Report commit time `2026-10-20T16:05:39-03:00` follows lane tip `2026-10-20T16:05:20-03:00` (`git show -s --format='%H %an %aI %cI'` in each owning repo).
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse --verify HASH^{commit}` and `merge-base --is-ancestor HASH refs/heads/master` succeeded for every round-work commit in the report's landed table: `17661e0f`, `df84807d`, `01b80946`, `61eaa071`, `6963d34b`, `0fa41252`, `c7693eb2`, `7b4839d3`, `d642ce52`, `daf6543e`, `b4355685`. The branch ref, not detached HEAD or an upstream shorthand, was used.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin` returned `branch=master local=b435568540f9a28f4f7bb902af8dbe6a5b084dfe remote=b435568540f9a28f4f7bb902af8dbe6a5b084dfe ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git ... status --porcelain` was empty; `git ... ls-remote origin refs/heads/master` returned the same full tip.
- The report has four `[~]` SHONEN lines matching the four lane checklist boxes. Template fidelity was checked by rendering `/home/vgpnk/Projects/shokunin/templates/round-prompt.md` with LANE=mado, ROUND=19, FLEET_ROOT=/home/vgpnk/Projects/shokunin, AXES=`coverage + operability (desktop and compositor craft)`, and the actual lane path; dispatched prompt sections 1–5 compare exactly after trailing-whitespace removal. Section 6 carries the hyaku overrides, including L1 planner ownership. No prompt contract omission found.
- Relevant protocol, AXES, CORPUS and LEARNING requirements were read. The driver digest, preserved rather than cited by mutable line number, is:

```text
2026-10-20T13:54:23-03:00 launch mado round=19 pgid=1145815 driver=hyaku-inline attempt=1
2026-10-20T16:05:57-03:00 complete mado round=19; hyaku-inline attempt=1
```

## Claims: direct re-measurement versus evidence verification

The following commands were run from `/home/vgpnk/Projects/shokunin/mado-shokunin`, for each of `9c54c56`, `7b4839d`, and `b435568`:

```text
python3 -I .ufo/waves/round-17/measure.py REV
python3 -I .ufo/waves/round-19/fresh-pins.py REV
python3 -I .ufo/waves/round-19/tw-recall.py REV
```

These are registered probes, not gate/selftest invocations. C3's producer runs only `--scan` over digest-pinned transcript text in a temporary directory, not the recorded commands.

| Claim | Observed before | Observed at tools-final and round tip | Judgment |
|---|---|---|---|
| C1 calibration | criteria=26, lesson_cited=18, score=6.9231 | criteria=28, lesson_cited=20, score=7.1429 | Literal improvement verified; **target ≥21/29 not met**. Folding R18-V2 into existing criterion 24 is reasonable anti-duplication, not permission to change the registered target after seeing the result. |
| C2 freshness | denominator=13, current=2, score=1.5385 | denominator=13, current=13, score=10.0 | File-pointer improvement verified; does not certify all files cite the source opened this round, nor re-measure walker behavior. |
| C3 operability | incident_lines=6, detected=3, score=5.0, tool `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` | incident_lines=6, detected=6, score=10.0, tool `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` | Six-line target verified; broader no-harm condition fails on precision. |

### C1: independent text census and criterion evidence

An independent Python/subprocess census over `git show REV:corpus/QUALITY.md`, matching `^\d+\..*` and counting own-line `lessons/` citations, reproduced 18/26 → 20/28. The first 26 numbered lines at the tip equal the baseline numbered lines exactly. New 27/28 cite round-19 M1/M2 and M3; R18-V2 is explicitly treated as criterion 24's existing provenance requirement.

The committed final receipts were **evidence-verified, not gate-executed**:

- `evidence/final/anchor-durability-red.txt`: producer `9e66dce8c6af26df13769ce47fdaa3ff1464296d3929ea80bf13ee6aa77bc9e4`, measured_commit `7b4839d…`, data argument `9c54c56…`, `FLAGGED S084 S094`, exit=1. Green receipt: data argument `7b4839d…`, flagged=0, exit=0.
- `evidence/final/supersede-sweep-red.txt`: producer `fd7c31df15e43309e7c425f811bdfb3fcd16cadf9698277e2e6ac665bd7a7dc4`, same measured revision, walker pointed=2/stale=11, exit=1. Green: pointed=13/stale=0 plus both source supersessions fully pointed, exit=0.
- `hashlib.sha256(git show 7b4839d:PRODUCER)` matched each header, and producer bytes at `b435568` are unchanged. Criterion 28's walker green overlaps C2; it is not an independent behavioral freshness result.

### C2: stronger source condition versus permissive counter

The fixed set was independently reconstructed from `git ls-tree -r --name-only 9c54c56` and the baseline bytes: knowledge Markdown, README, SKILL, PROVINCE, tools, containing `2.17.0`. Same-line `2.17.2` plus `\bS\d{3}\b` counting independently gave 2/13 → 13/13.

**The report's repeated “5/13 name S096 on the crediting line” is stale at the reviewed tip.** Define the measurement precisely: a file has S096 credit if *any* line satisfying the registered version+source regex contains `\bS096\b`. At `b435568` this is **8/13**: SKILL, README, remaining-planes-census, walker-deep-r9, walker-deep, walker-live-surface, walker-route-r18, mado-verify. Using only the *first* matching line instead gives **6/13**, not 5/13. `w2/reports/RerunC2.md:50-73` measures the earlier `01b8094` snapshot; later corrections add positive S096 references in the two formerly “reserved” pointers and change README's same-line credit. This discrepancy must not be silently copied into later rounds.

Five tip files still have no S096 on any qualifying line: `arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`; their truthful dated pointers cite the pre-existing S090 log row. Thus the pre-registered promise that **every file** cite the new host-byte row remains unmet even though the permissive counter is green. The substantive baseline had no round-19 dated pointers; two pre-existing round-18 lines already happened to pass the regex. Zero walker behavior facts were re-measured on 2.17.2; this is a provenance/pin-pointer claim only.

### C3: recall attribution and independently demonstrated precision harm

The six distinct incident pairs were independently counted from baseline frozen `expected_findings ∪ known_misses`: 6 incident lines among 26 total input lines, hence 20 controls. Reviewer's own `--scan` over copied pinned inputs found the three additions exactly as `package_query/pacman:-Q`: `inputs/r14-source-safety.jsonl:2,3` by BashCVar and `inputs/r13-root.jsonl:4` by HelperFn rule B alone. Without B that last line is unrecognized, giving 5/6. The 4,728 stable-transcript, zero-lost-findings/13-added-outside-new-classes precision sweep was **evidence-verified** from `w2/reports/RerunPrecision.md`, not rerun; the same report documents 78 nonwrite VCS rows (74 `jj --help`, four `git --dry-run/-n`). `CriticC3W2.md:122-160` is the actual source of the **12/12 synthetic data-only false positives** tally; AdvHelperFn separately demonstrates pure-data false positives.

For an unambiguous independent counterexample, the integrator copied the JSON envelope of committed `tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl` into a temporary `data-only.jsonl`, replacing only its `message.content[0].arguments.code` with:

```python
BLOCK=frozenset(['pacman','-Q','hyprland'])
```

For each revision, `git show REV:tools/mado-tripwire.py` was copied to the temporary `tool.py`, then `python3 -I tool.py --scan data-only.jsonl` was run with that directory as cwd. **The fixture code was never executed.** Observed:

```text
9c54c56: exit=0; MADO_TRIPWIRE: clean; findings=[]
b435568: exit=1; MADO_TRIPWIRE: findings;
  class=package_query rule=pacman:-Q command="pacman -Q hyprland"
```

`frozenset` constructs data and executes no package command. The tip promotes this to an ordinary finding without a lead marker. This is a real before→after precision regression in the runnable artifact, even though the exposure test is synthetic and the two current-corpus B hits were true. A bounded recall gain and honest limit paragraph do not make that trade harm-free.

## Guard evidence and weakening review

No sibling gate was executed. The final receipts name `7b4839d31d60af5bac40e3e74aec70e928601dfc`; gate/tool/frozen-input bytes are unchanged at `b435568`. Independent SHA-256 checks bind the gate to `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1` and tripwire to `367be947…`.

- Gate receipts `evidence/final/gate-selftest.txt` and `final/harm/harm-gate-selftest.txt`: **460/460**, exit=0; baseline receipt states 389/389. Gate regression receipt: `MADO_REGRESSION: PASS`, killed=10/10, flips=0, inconclusive=0, control=green, restore=ok. Classifier receipt: 52/52.
- OM10 replacement is **not weakening**. Reviewer compared baseline and final selftest helper labels: 390 source occurrences / 370 distinct → 461 / 440 (one mutually exclusive R10 branch accounts for source-vs-runtime difference). Exactly **nine old labeled assertion occurrences (eight distinct)** disappeared, all OM10, replaced by OM10A six + OM10B eight. No shared label disappeared. Thus the report's “ten old assertions” is a counting defect. A checks failed tag lookup but successful branch-tip rescue; B retains failed tag+tip lookup UNKNOWN semantics, diagnostics, no false MOVED, skill comparison and count checks. The F6 change explains the split. Neither old nor new OM10 block asserts its captured overall `om_rc`; that is an existing coverage limit, not a dropped guarantee. CriticAdmission's intermediate review agrees; closure additionally compared final `7b4839d`.
- Eleven tripwire selftest receipts sum **16+9+33+30+31+1+45+13+34+18+17=247/247**, all carrying the final tool hash and revision. These are evidence-verified suite results, not an independent execution or a precision proof.
- Baseline round-17/18 fixture diff changes exactly `hardening/expected.json`: `multiline-quoted-commit-clean` → `multiline-quoted-commit-vcs`, exit 0→1, empty expected findings → required `vcs_write/git:commit` on line 1, input unchanged. This strengthens the expected result for a real commit, not an escape from a failure. Existing suite case counts are unchanged. The round-19 eval case likewise requires the actual `git commit` finding while harmless cells remain clean; its rename predates the committed merge. No pre-existing fixture deletion found.
- Frozen receipts: round 18 `frozen_verdict_mismatch`, exit=1, precisely the three formerly missed package-query rows; round 19 `frozen_match`, exit=0. Independent committed-byte hashing confirmed all five input digests in each expectation file. Expected-file digests are respectively `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9` and `50d2a45e2602cb430b94043f6c658204b0b1802e8c1931cb2a3eda167af02435`. This expected old-baseline red is not an unexplained broken gate.
- `git diff 9c54c56 b435568 -- SCORECARD.md` was reviewed. The revision-bound counter retained rubric V=6/6 and U-routes=7 at baseline and tip. Committed navigation receipt reports 34/34. These bounded guards remain green but do not negate the demonstrated precision harm.

## Outside discernment spot-check

Sources were reopened on 2026-10-20; source text was treated as data, never instructions. Integrator directly reopened S096 bytes, S097 raw text and S084's latest page; the closure's independent source reviewer also reopened all five below.

| Item | Decision | Reopened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S096 | admit | `/usr/bin/walker`, read as bytes only | agree | `sha256sum` = `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`; `2.17.2` once at offset 856302, `2.17.0` zero times. Full quoted `version2.17.2` begins 856295, exactly as the appended correction states. No runtime conclusion. |
| S097 | admit | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | agree | Raw digest `dbdd13a6…01786` matches; line 4 is `background = "#121212"`, **3 whitespace words**, ≤25 and at the stated location. Only the payload/quote was rechecked, not the full tag-clone object chain. |
| S098 | admit | https://static.crates.io/crates/xdg/xdg-3.0.0.crate and walker v2.17.2 Cargo.lock | agree | Reviewer fetched archive, obtaining `2fb43323…85b5`, equal to Cargo.lock line 2708; fixed-version registry archive improves on latest-alias support. |
| S084 | reject as version-specific support | https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html | agree | Page reopens and currently says 3.0.0, but the canonical path remains `latest`; current content correctness does not make the alias an immutable version anchor. |
| S094 | reject HTML digest as durable anchor | https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black | agree | Reviewer's two fetch hashes differ, `19b82494…10101` versus `1dfd4c0c…f34d`. A rotating HTML-response hash is not the theme payload identity. |

`git show` field projections confirm S084/S094 `mined → rejected`, used-by knowledge path → `—`. `git grep -n -E '^source:.*(S084|S094)' b435568 -- corpus/knowledge` returned no live source-header hits; remaining mentions are historical/supersession notes.

Required independent census command:

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado W04 S030 duplicate url ... across scopes
mado W04 S042 duplicate url ... across scopes
mado W04 S045 duplicate url ... across scopes
mado W04 S097 duplicate url ... across scopes
mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```

Independent parsing of committed rows: **95 → 98**, tiers A **88 → 91**, B=1 and C=6 unchanged; mined **80 → 81**, queued=8, rejected **7 → 9**. Duplicate-URL warnings are acknowledged, not hidden errors.

## Incidents and wave accountability

- **Host pause was breached**, not merely nearly breached: SentinelGatePath executed the real `/usr/bin/hyprctl probe` through `unshare --user --map-current-user --mount --propagation private /tmp/sgp/inns.sh bash -c '... /usr/bin/hyprctl probe; echo rc=$?'`. The harness's failed mount setup did not prevent payload execution. Transcript result: `unknown request`, rc=0. No mutating request was accepted in that output; **absence of any host state change was not independently measured**, and this closure performed no live recheck. The lane's self-report and appended captured-by correction are candid. Prompt-only isolation is insufficient; a post-hoc tool scan is not an actuator or proof of host safety.
- `c7693eb` durably records the post-wave scan and correction. The committed receipt actually has **154 files**, versus lesson prose **155 transcripts**. It reports host_mutation=0, package_query=0, tool_install=0, live_probe=3, vcs_write=164, exit=1. The hyprctl invocation ran inside a written-then-executed script, outside the parser's documented analysis; it was **not detected**. The live-probe tally includes a walker data-string false positive. The round-20 plan does not specifically route this script-wrapper/fail-open mount defect; this closure does below.
- **Misroot:** QualityDraft's `.ufo/waves/round-19/drafts/QualityDraft.md` and `.ufo/waves/round-19/w1/reports/QualityDraft.md` now reside in the lane and landed at `df84807`. The fleet-root round-19 directory is absent, fleet history for that directory is empty, and scoped fleet status contains no copies. L1's historical `cmp` equality is recorded by the lane; deleted originals cannot be independently compared now. This was an actual write-scope violation followed by documented cleanup, not permission to use relative paths again.
- Wave 1 membership is 86 with exactly **25 members lacking reports**, matching all dead seats named in the lane report. The directory contains **62 Markdown files plus one registry JSON (63 files)**; membership reports must be joined to the roster, not inferred from raw file count. Reported zai 429 retry exhaustion is provider failure, not learner output; no claim was credited to a missing seat and no dead-seat replacement was reported. W2 still used 10 m_zfl reviewers; no routing changes were made by closure.
- Round install record: L1 none; author-disclosed AdvInstallers used pip 26.2.1 ephemerally via `uv run --no-project --with pip` to inspect grammar (uv-cache channel, no PATH installation). Closure installs: none.

## Per-axis and trend verdicts

| Owned axis | Verdict | Basis |
|---|---|---|
| calibration | improved | Literal lesson-linked criteria 18/26 → 20/28; original numbered criteria retained; target nevertheless missed and some final prose tallies are stale. |
| freshness | improved | Dated file-pointer coverage 2/13 → 13/13 and verified host-byte pin; no claim of behavioral remeasurement or all-file S096 coverage. |
| operability | **harmed** | Greater six-line recall and stronger gate coverage coexist with a new unmarked ordinary finding on provably pure frozenset data. No-harm condition therefore fails. |
| coverage | unchanged | V=6/6, U=7/7; no newly admitted uncovered domain surface. |
| depth | unchanged | Source anchoring improves evidence quality but no independently measured new domain-depth claim. |
| adjacency | unchanged | PROVINCE path clarification preserves the routing boundary; no new cross-domain absorption evidenced in this review. |

Trends: **expansion unchanged** (no uncovered-domain knowledge admission; landedness probe is a locally documented tooling candidate, not an admitted capability of this rejected round); **quality improved**, specifically corpus evidence quality (S097/S098 replace weaker anchors; old factual claims are dated rather than presented as remeasured; this is not a blanket artifact/no-harm pass); **discernment improved** (outside sample agrees on three admits and two rejects, and grounded 27/28 address real prior failures). No scalar is assigned.

SHONEN boxes are **not all newly checkable from this review**: neither current no-oral-context execution nor end-to-end desktop behavior was verified here. No box was edited; promotion/minting remains operator-owned.

## Routed defects — durable queue for the next mado round

| ID | Owner | Required disposition |
|---|---|---|
| R19-V1 | mado | Preserve C1's ≥21/29 miss as a miss. Do not add a duplicate criterion or retroactively redefine the target. Any next calibration claim needs a fresh pre-registration and grounded failure evidence. |
| R19-V2 | mado | Reconcile C2's all-file new-source/upstream promise with the actual tip. Correct the snapshot-stale 5/13 statement in a named next-round correction: current precisely defined all-matching-line S096 count is 8/13; first-matching-line count is 6/13. A token-only count does not prove provenance or behavior. |
| R19-V3 | mado | Repair Rule-B precision and distinguish leads from observed execution; include pure containers/formatters, binding/shadowing, real wrapper misses and help/dry-run nonwrites in red-before fixtures. Preserve six-line recall and existing controls rather than trade precision for it. |
| R19-V4 | mado; operator for host isolation authorization | Specifically route the fail-open mount/script-wrapper incident. An isolation setup failure must abort before any payload; do not re-exercise a real host probe while the pause binds. Keep written-script scan blindness explicit; repair the stale 155-vs-154 receipt count and never recast self-report as tripwire detection. |
| R19-V5 | mado | Correct “ten OM10 assertions” to the measured nine labeled occurrences (eight distinct); maintain OM10A/B guarantees. Keep open worktree-ledger/harm-watch execution/provenance and anchor-alias checker limits from the lane's own lesson on the next-round queue; green bounded checks do not close those limits. |
| R19-V6 | mado; operator for generated trailer delivery | Keep the QualityDraft misroot lesson and absolute lane paths at every seat boundary; final directory cleanup is verified, historical byte equality is lane evidence only. Dead seats remain dead and uncredited; provider recovery must not be reported as claim evidence. |

This artifact is closure evidence only. It does not improve or silently correct the lane's filed round work.
