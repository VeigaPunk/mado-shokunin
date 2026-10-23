# AtkQualityCriteria — attack on QUALITY criteria 33-35 (round 24, wave 2)

VERDICT: partial — criterion 33 **partial**, criterion 34 **partial**, criterion 35 **partial**.

Each criterion's lesson citation is faithful and both named checks are runnable and can
fail; none of the three checks measures the clause its criterion rests on beyond the
commit-order precondition (33/35) or digest-plus-absoluteness (34). Counterexamples below
were executed, not inferred.

## Target and method

- Target: `corpus/QUALITY.md:318-320` at `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`
  (`sha256:e72d15039ad111b6fc88eb351629bc4bedbbb9a5fe1973354e194014c137e326`).
  `git diff 8e5d9369 39c59630 -- corpus/QUALITY.md` = 6 insertions, 0 deletions; the lane
  later moved to `87429be` and `git diff 39c59630 HEAD -- corpus/QUALITY.md` is empty.
- Lesson inputs re-opened: `corpus/lessons/round-23.md:23` (M23-4), `:24` (M23-5),
  `:229` (M23-7); routed requirement in
  `corpus/lessons/round-23-verifier-spotcheck.md:145-147`.
- Lane access was read-only (`git log/rev-list/diff-tree/show/diff`, file reads). Sandbox
  git ran only under `/fast/scratch/hyaku/mado-r24/w2/atk-qc/` with `GIT_DIR`,
  `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset. The only lane write is this report.
- Sibling reports read for overlap: `w2/reports/MutCheckRegOrder.md` (surviving `--base`
  mutant; vacuous round-24 green) and `w2/reports/MutCheckReceipt.md` (delete-before-run
  mutant survives; Markdown receipts misparse). Where I reproduce their findings I say so;
  the same-path-pairing gap, the same-commit green, the path-name population arm, the
  prose-word repair arm and the cross-round carry blindness are not in either report.
- No installs or updates were made.

## Reproduction — receipts are real

| Assertion in the criterion / receipt | Re-run result |
|---|---|
| checker sha256 `c27f474d…b75ed2` (m23-4-7 receipt) | `sha256sum` matches (14,609 B) |
| checker sha256 `5b463510…0e585f9` (m23-5 receipt) | `sha256sum` matches (16,412 B) |
| round-23 red: `--round 23 --tip 8e5d9369` → exit 1, first tools `2e592af`, first population `3df1062` | exit 1; recorded section-1 stdout diffs clean against the fresh run (8 lines, diff rc 0) |
| bare `--round 23` (the form printed in QUALITY.md) | exit 1, same RED reason |
| receipt sandboxes §2/§3/§4 (`ExecCheckM2347/sandbox-*`) | GREEN 0 / RED 1 / RED 1, same reasons |
| `--round 24` on the lane | exit 0, `verdict=GREEN reason=no commit in the window changes tools/` (vacuous) |
| m23-5 selftest | `selftest=pass cases=8 mismatches=0`, exit 0 |
| m23-5 red `quality/red/r23-l1-attacks-first.sh` | exit 1, 5 reasons; blob `602ecd7` sha256 = red file sha256 `599a92da…7425d` |
| m23-5 green `quality/fixtures/l1-attacks-green.sh` | exit 0, `verdict=pass reasons=0` |

So "runnable and shown able to fail" holds for both scripts as recorded. The defect is
what they do not measure.

## Criterion 33 — partial

**Citation: holds.** M23-4's mistake is "C1 as first landed at `2e592aff` … none of the
registered guards: the 1356-file corpus, precision suite, oracles and selftests hold none
of these shapes". Criterion 33's first sentence and three named classes map onto M23-4's
"1 global-store silent miss", "13 of 45 recall shapes where base kept a lead and the tip
reported nothing", and the frame/nested-binder/match-binder regressions. One narrowing:
the landed text keeps only "frame or scope reuse" and drops M23-4's nested-binder and
match/with-binder shapes that the wave-1 scribe draft still named
(`w1/reports/ScribeQualityCriteria.md:7`). The carry README's AttackFrameScopes row keeps
them, so the criterion is weaker than its own lesson, not wrong about it.

**Runnable and can fail: holds** (round-23 red reproduced exactly; two negative controls
and one guard reproduce).

**Measurement: does not measure what 33 says.** The checker never opens a fixture and
never reads an outcome. `population_evidence` (`check-registration-order.py:146-192`)
classifies by path names only; `file_at` is called solely for a repair manifest's prose
(`:182-188`). No code path inspects the three attack classes, base-versus-tip verdicts, or
"each kept with its outcome at both revisions". Executed counterexamples:

| # | History (all under `/fast/scratch/hyaku/mado-r24/w2/atk-qc/`) | Checker result |
|---|---|---|
| A | `sbx-triv`: one 30-B JSONL `{"id":"noop","src":"x = 1\n"}` under `…/w1/out/AttackTrivial/fixtures/`, **no manifest, no outcomes**; next commit changes `tools/detector.py` | `verdict=GREEN … precedes the first tools/ change`, exit 0 |
| B | `sbx-perf`: one 20-B `timings.jsonl` under `…/w2/out/AttackPerf/` (a timing dump, not a fixture) | GREEN, exit 0 — the string "attack" in a directory name is the whole admission test (`:160-163`) |
| C | `sbx-same`: carry population **and** `tools/detector.py` in one commit | GREEN, "land in the same commit; neither strictly precedes the other" (`:270-273`), exit 0 — contradicts "frozen before the patch" |
| D | `sbx-repair-word`: repair set whose manifest says `"note":"no attack here, repair target only"`; commit 2 changes `tools/` | GREEN, `kind=repair`, exit 0 — the repair arm is a case-insensitive word search (`:78`, `:184`), so one prose word converts a repair set into a "discovery population" |

A and B show the check is satisfiable with **none** of criterion 33's three classes and no
base/tip outcome. C defeats the strict "before the patch" reading even in the intended
path class. The checker's own receipt §7 admits "it does not judge whether the fixtures are
meaningful discovery attacks", but the criterion still names this gate as its `Check:`; a
seat applying criterion 33 gets a green from a no-op.

**VERDICT: partial** — citation and red/green fidelity hold; the named check does not
measure the criterion.

## Criterion 34 — partial

**Citation: holds.** M23-5 is exactly "wrote probe results through a relative path that did
not resolve where it read them, so it read stale files from an earlier tool", with the
repair "Results now go to absolute paths and are deleted before each run; the script prints
the tool sha256 it measured". The criterion's three clauses match that row.

**Runnable and can fail: holds** (selftest 8/8; real red artifact exit 1 with 5 reasons;
synthetic green exit 0).

**Measurement: enforces the digest form and absoluteness; the same-path and deletion
clauses are unenforced.** The gate's contract
is R1 (a 64-hex digest on a line with a tool hint) and R2 (each extracted write/read path is
absolute). `staging_notes` is reported only under `--notes` and "never fail[s] the gate"
(docstring `:45-46`; called at `:287`, printed at `:290-298`). R2 tests each token in
isolation (`judge_path` `:145-174`); nothing pairs a read with the write that produced it.
The selftest matrix (`:329-365`) has no pairing case and no missing-delete case. Executed
counterexamples:

| Artifact | Content | Gate result |
|---|---|---|
| `atk-qc/receipts/split-paths.sh` (`sha256:211e3780…90dd`) | writes `/fast/…/atk-qc/results/repair.json`; reads `/fast/…/atk-qc/stale/repair.json` — a **different absolute file**, the M23-5 stale-read shape with absoluteness; **no `rm`**; digest is a made-up `0123…` | `PASS … verdict=pass reasons=0`, exit 0 |
| `atk-qc/receipts/no-rm.sh` (`sha256:41ae453b…c38d`) | green sample with the `rm -f` line removed | `PASS … verdict=pass reasons=0`, exit 0 |

So the check does not enforce "writer and reader use the same absolute result paths" (a
stale sibling passes) and does not enforce "prior results are removed before each run" (the
same result as `MutCheckReceipt.md` M3, reached from the receipt side). It also cannot tie
the named digest to the measured bytes (disclosed at `:55-57`), which is acceptable for
"names" but means the `0123…` digest above is not distinguished from a true one.

The gate is also over-broad on real lane artifacts: fed unmodified,
`w2/reports/ReRepair.md` returns `verdict=fail reasons=23` whose reasons are prose tokens
(`'.'`, `'the'`, `'and'`, `'schema'`, a shell continuation `'\\'`), and
`w1/reports/ExecFullA.md` fails R1 even though it does state a full candidate-tool digest,
because the line lacks a `tools/` or `tool*.py|sh` hint. This matches
`MutCheckReceipt.md`'s real-receipt section and means the gate's admission population is
narrower than "a scratch measurement receipt" in the criterion's wording.

**VERDICT: partial** — citation, runnability and failability hold; two of the three
admission clauses are unenforced, including the "same paths" clause that is the M23-5
mistake itself.

## Criterion 35 — partial

**Citation: holds.** M23-7 is "Production bytes withdrawn to base; the next registration
must include these fixtures before any patch." Criterion 35's three steps (register,
withdraw, assess only after registration) are a faithful expansion.

**The carry parenthetical is true.** Independently verified, not taken from the report:
`carry/manifest.json` has `fixture_count: 28` and 28 entries; every entry's `sha256` and
`bytes` match the committed file; 19 lane-origin entries are byte-identical to
`git show 8e5d9369:<origin_path>`; the 9 scratch-origin entries (`SecondFrameRelay…`,
`EscapeNonlocalHook`, the seven `ReClosureNeighbour` W2* files) are still present at their
origin paths and match the manifest sha256; `tools/mado-tripwire.py` is byte-identical to
base (`sha256:cd9da20c…ea84`, `git diff 8e5d9369 HEAD -- tools/` empty). The checker does
recognise the carry at `39c5963` (`kind=carry`).

**Runnable and can fail: holds only for the ordering property, on round 23.** The same run
that makes 33 red is the only non-vacuous demonstration.

**Measurement: the criterion cannot be demonstrated by the named check, and the carry
cannot be credited in the round that would use it.**

| # | History | Checker result |
|---|---|---|
| E | `sbx-vacuous`: two commits, no population, no `tools/` change | GREEN, exit 0 — so on round 24 the check passes whether `carry/` exists or not; the criterion's own round is vacuous (`m23-4-7` receipt §5 says so) |
| F | `sbx-cross`: commit 1 `round-24: register the carry discovery population` (carry manifest + fixture), commit 2 `round-25: change tools/detector.py against the round-24 carry`; run `--round 25` | RED, `first-registered-discovery-attack-population=none`, exit 1 |

F is the load-bearing one: `infer_round` sets base to the parent of the oldest round-25
commit (`:93-127`), so the round-24 carry commit is outside `BASE..TIP`; a future patch
against exactly the population criterion 35 says is registered is scored as having no
population. `MutCheckRegOrder.md` W8 observed the same base-exclusion mechanism for an
explicit `--base`; F shows it defeats the cross-round purpose without any explicit base.
The workaround — re-adding/copying the carry into the new round so it appears as `A` — is
not stated in criterion 35 and would duplicate bytes.

The second and third steps of 35 are also unmeasured: no check requires `tools/` to equal
base for the affected production change, and no check reads whether the fixtures were
"first discovered after a patch" (only commit order is visible).

**VERDICT: partial** — citation and the factual carry registration hold; the named check is
vacuous on this round and blind to the registered carry in the next one, and the withdrawal
step has no check.

## Cross-cutting findings

1. **Duplicate authority.** One check is the named `Check:` for two different criteria
   (33 and 35). Its pass/fail is offered as evidence for two distinct defects, but it
   measures only the ordering precondition they share; a wrong verdict in it is
   double-counted, and a green demonstrates neither criterion's substance.
2. **Identity conflation in "registered discovery/attack population".** The checker uses
   one label for three different evidence standards: any `.jsonl` under an `attack` path
   (no manifest, no outcomes), a carry population (cases + manifest), and a repair set
   (cases + manifest containing the word "discovery" or "attack"). Criterion 33's phrase
   "discovery attacks frozen before the patch" is not the same object as the checker's
   label; the receipts' §7 disclosure names the gap but the criterion does not.
3. **Axis impact — calibration / lesson-grounded admission criteria.** The SCORECARD
   rubric `10 × criteria citing a lesson / criteria` moves from 23/32 = 7.1875 at
   `8e5d9369` to 26/35 = 7.4286 at `39c5963` (`grep -cE '^[0-9]+\. .*lessons/'` over
   `grep -cE '^[0-9]+\. '`). The three criteria do cite lessons, so the literal counter is
   entitled to move; the semantic content behind the +0.24 is the ordering precondition
   (33, 35) and two of three clauses (34), not demonstrated no-harm admission.
4. **No evidence-standard regression elsewhere.** The append is append-only, the red
   provenance is real (blob `602ecd7` hash = red file hash), the carry is byte-exact, and
   `tools/` is untouched; no false provenance or duplicate authority was found outside the
   points above.
5. **Minor: criterion 33's class list narrowed.** The landed text drops M23-4's
   nested-binder and match/with-binder shapes that the scribe draft kept; the carry README
   retains them, so the omission is in the criterion, not the population.

## Smallest safe corrections

- **33 + 35 (order gate):**
  1. Make the same-commit case RED (`check-registration-order.py:270-273`): a population
     that lands with the patch is not "frozen before" it and not "only after registration".
     One verdict-branch edit; the round-23 red is unaffected.
  2. Require a manifest for the `attack` arm (route `:160-163` through the carry arm at
     `:166-181`) so a no-op or perf dump cannot be the population. Round 23 stays RED —
     the `AttackPerf` manifest and fixtures, added at `3df1062`/`fa819d5`, would still
     qualify and still follow the `2e592af` tools change — but the printed
     first-population line changes and the red/green receipt must be regenerated. Note
     that a manifest-qualified arm would still call `AttackPerf` (a timing population) a
     discovery population; the class check in fix 4 is the one that separates them.
  3. Add a `--population DIR --tip REV` mode (or extend the window to a declared carry
     path) that verifies the carry manifest against `git show REV:<path>`; otherwise the
     round-24 carry cannot serve the round-25 patch it was frozen for (F).
  4. Either narrow 33's `Check:` sentence to "ordering precondition only" and name the
     seat that reads the three classes and both-revision outcomes, or add a manifest-schema
     check for those fields; keep the receipt's §7 honesty in the criterion, not only in
     the receipt.
- **34 (receipt gate):** add two rules with selftest mutants — (a) a read at an absolute
  data path under a results root that the same receipt never writes is a `stale-read`
  failure (kills `split-paths.sh`); (b) every write target needs a preceding `rm` of that
  exact path (kills `no-rm.sh`); (c) restrict `HARNESS`/`extract_paths` to command and
  redirection positions so Markdown prose is not data (kills the `ReRepair.md` 23-reason
  false failure), or scope criterion 34 to shell receipts explicitly.
- **35 (withdrawal):** add the assertion `git diff --quiet <base> <tip> -- tools/` (or
  "the affected tool equals its base blob") to the same check, so the "withdraw the
  affected production change to base" step is measured rather than narrated.

## Reproduction commands and raw outputs

All sandbox roots: `/fast/scratch/hyaku/mado-r24/w2/atk-qc/`. Checker paths below are the
lane files at `39c5963`; each sandbox was created with
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git init` and local user config.
Long path lists are elided with `…` in the excerpts below; verdict and reason text is
verbatim.

```text
# A — 30-B no-op JSONL under an attack path, no manifest, no outcomes
$ python3 -I .ufo/waves/round-24/quality/check-registration-order.py --round 99 --repo .../sbx-triv
first-tools-change=5bc8dc43834cb68f4d84f41f95161b40c46b0dd5 … paths=tools/detector.py
first-registered-discovery-attack-population=4b8e8f990d063f424b215b8192521ba79de7fbf9 … kind=attack-fixture paths=.ufo/waves/round-99/w1/out/AttackTrivial/fixtures/NoOp.jsonl
verdict=GREEN reason=first registered discovery/attack population 4b8e8f9… precedes the first tools/ change 5bc8dc4…
exit=0

# B — 20-B timing dump under AttackPerf
first-registered-discovery-attack-population=72aad439db887b50f524d9b4c9e09f2215dd4088 … kind=attack-fixture paths=.ufo/waves/round-99/w2/out/AttackPerf/timings.jsonl
verdict=GREEN … exit=0

# C — carry population and tools change in one commit
first-tools-change=7df25ab3700ec358177a35405031b4a7e7fe6e9d … paths=tools/detector.py
first-registered-discovery-attack-population=7df25ab3700ec358177a35405031b4a7e7fe6e9d … kind=carry …
verdict=GREEN reason=population 7df25ab… and the earliest tools/ change land in the same commit; neither strictly precedes the other
exit=0

# D — repair manifest with the word "attack" in prose
first-tools-change=080b9cc6559a26842c4cf1cadf7fc7483db126c2 … paths=tools/detector.py
first-registered-discovery-attack-population=d198aa877afb435fe660d81f178a755c551421bd … kind=repair paths=.ufo/waves/round-99/repair/expected.json,.ufo/waves/round-99/repair/fixtures/R1.jsonl
verdict=GREEN … exit=0

# E — no population, no tools change
first-tools-change=none
first-registered-discovery-attack-population=none
verdict=GREEN reason=no commit in the window changes tools/   exit=0

# F — round-24 carry, round-25 tools change
window=ccc6843a7de18612d112c34a16f0e7d7d33efd07..ad6463562213841678a6b7738424eb9fdab59a7a7 commits=1
first-tools-change=ad6463562213841678a6b7738424eb9fdab59a7a7 … paths=tools/detector.py
first-registered-discovery-attack-population=none
verdict=RED reason=tools/ changed at ad646356… but no commit in the window adds a registered discovery/attack population
exit=1

# Positive directions (the check can fail): sbx-red-carry (carry after tools) RED 1;
# sbx-no-pop (tools only) RED 1; lane --round 23 RED 1; lane --round 24 GREEN 0.

# 34 — split absolute write/read paths, no rm, fabricated digest
$ python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py atk-qc/receipts/split-paths.sh
PASS /fast/scratch/hyaku/mado-r24/w2/atk-qc/receipts/split-paths.sh
verdict=pass reasons=0   exit=0

# 34 — green sample with the rm removed
$ python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py atk-qc/receipts/no-rm.sh
PASS /fast/scratch/hyaku/mado-r24/w2/atk-qc/receipts/no-rm.sh
verdict=pass reasons=0   exit=0

# 34 — over-broad on real report receipts (excerpt of last line)
$ python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py .ufo/waves/round-23/w2/reports/ReRepair.md
FAIL …:73: R2 data position: relative path '.' (resolved against the receipt's current directory)
verdict=fail reasons=23   exit=1
$ python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py .ufo/waves/round-23/w1/reports/ExecFullA.md
verdict=fail reasons=6   exit=1
```

Carry verification (independent of the manifest's own claim):

```text
entries 28  byte mismatches 0  lane-origin byte-identical at 8e5d9369: 19  scratch-origin present and matching: 9
tools/mado-tripwire.py sha256:cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
git diff 8e5d9369 HEAD -- tools/ : empty
```

Sandbox artifact hashes (scratch provenance, not lane evidence):
`NoOp.jsonl sha256:b1eaa12ab1cbfa8e0d9125cc0d68e190587c0e35a2e63c8b62b2a7a0f95b05ce`,
`timings.jsonl sha256:978307ec0694b9b15767a2acfb9373255deb7343b377b0c4b037e3742cf7ea87`,
`split-paths.sh sha256:211e37802974b3f3f381cbdbdc00a65913a8c280d65834806fdc27c76d3290dd`,
`no-rm.sh sha256:41ae453bcbc954a5e5ca44a14cf7e5312e5abd3cce3e24796bc863d8eed0c38d`.

## Disposition

No round-acceptance or integration decision is made here. C1 (coverage) and C2
(calibration) claims are untouched by this report; the finding lands on the round's
non-claim repair (routed defect 3) and on the calibration rubric's literal lesson-citation
count. The criteria are directionally right and the receipts are honest about their
boundaries; the smallest fix is to make the order gate strict (same-commit red, manifest
required) and to add the two missing receipt rules, or to narrow the criteria's `Check:`
sentences to exactly what their gates measure.
