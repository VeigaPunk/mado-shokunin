# R68ConnSiblings — sibling prior art and assimilation screen (connector seat)

Read-only screen. Lane: `mado-shokunin`; round 68, wave 1, connector seat.
Base (pre-r68 tip) `510100c81e6cf63fec6be380c2f2f9c670f32cbc`; freeze `e0727cda`; pre-wave tip `40d2bef8`.
No campaign tool was run in `shokuknow`; no git/jj mutation anywhere; no desktop probe; no install or
upgrade (nothing needed). Scratch `/fast/scratch/hyaku/mado-r68/R68ConnSiblings/` created and removed.
Every `git` command below is a read (`show`, `ls-tree`, `log`, `status`), named `-C` on the lane.

Axes the screen is judged against: **C1 calibration** (the control harness kills its own forged kill
credit) and **C2 operability** (the standing gates read git objects through a guarded environment).
A finding is kept only if it improves one axis and harms neither.

---

## 0. The one bounded move (connector proposal)

**Repair by shape, not by string.** The frozen census classifies the guard by AST *presence*
(`quality/counters/c2-r68-reader-guard.py:96-127`: dict-literal key, subscript store on an
env-named target, keyword argument) and the declaration's Limits already say the guard is
"presence-tested (the value is not interpreted)". That rule cannot see **dominance**: a repair that
stores the guard and then rebuilds the env by purging every `GIT_*` name reads `guarded=yes` while
executing unguarded, because `GIT_NO_REPLACE_OBJECTS` itself starts with `GIT_`.

That is not hypothetical in this population. At the base rev, five of the twelve unguarded reader
gates construct their child env exactly that way:

| file at `510100c8` | purge line |
|---|---|
| `quality/check-axis-scores.py` | `:99`, `:121` — `{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}` |
| `quality/check-evidence-pointers.py` | `:71` — same expression bound to `GIT_ENV` |
| `quality/check-freeze-order.py` | `:45` — same expression |
| `quality/check-index-rows.py` | `:58` — same expression, passed as `env=` |
| `quality/check-index.py` | `:51` — same expression, passed as `env=` |

The sibling lane that measured this trap is **kaidoku**:
`.ufo/waves/round-23/w1/CounterGitIsolation.md:75-91` (F2, "Order is load-bearing: purge `GIT_*`
first, then set `GIT_NO_REPLACE_OBJECTS=1`"; the observation `before_has_no_replace "1" ->
after_loop_has_no_replace null`). Mado's repair set contains the same construction five times.

**Move.** Keep the twelve repairs and the census unchanged, and place the *already-declared*
auxiliary hazard probe (claims declaration, "Auxiliary hazard probe (outside the denominator)") on a
purge-shaped gate — `quality/check-index.py` — with two repaired variants in the same scratch
fixture:

- **A (correct order):** purge, then `env["GIT_NO_REPLACE_OBJECTS"] = "1"` → reads the real bytes;
- **B (guard before the purge):** the same store placed above the comprehension → reads the forged
  bytes under a planted `refs/replace`, while the census still counts the file `guarded=yes`.

B is the negative control. It costs one extra run of one gate against the scratch repo the probe
already builds, changes no counter, no predicate, no control set and no denominator.

**Axes.** C2 improves (the aux probe now samples the repair shape that can silently fail).
C1 is untouched (no harness, no recipe, no selftest change). No axis is harmed: the census's
`guarded=13` stays the claim; B only shows what that count does *not* mean.

**Risks.** (i) A reviewer may read B as re-scoping the claim — it must be reported as a harm-watch
receipt, exactly where the declaration already puts the probe. (ii) `check-index.py`'s purge sits in
a `env=` keyword (line 51), so the probe must copy the file, not the helper. (iii) If the wave's
executor instead repairs by adding the guard *inside* the comprehension's output, the AST rule
accepts it and the probe shows real bytes — the move must not be used to demand a particular style.

**Verification.** Two receipts: the census line unchanged at the measured rev
(`population=20 readers=13 guarded=13 unguarded=0 controls=11/11`), and the A/B pair printing
`real`/`forged` for the same gate. Re-derivable with
`python3 quality/counters/c2-r68-reader-guard.py --repo . --rev REV --controls .ufo/waves/round-68/controls/c2-controls.json --scratch-root DIR`
plus the probe's own two gate runs.

---

## 1. Prior art, with fit and disposition

### (a) Git environment guards / `GIT_NO_REPLACE_OBJECTS` / replace-ref controls

| item | source file:line | fit | owning lane | what mado does about it |
|---|---|---|---|---|
| Earliest production guard: purge `GIT_*`, then `GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL`, `GIT_NO_LAZY_FETCH`, `GIT_NO_REPLACE_OBJECTS`, `LC_ALL` | `kagi-shokunin/corpus/revision-audit.py:40-46` | fits (the guard shape C2 repairs toward) | kagi | cite as the fleet's first guarded reader; no adoption (kagi's file is not mado's) |
| Replace-ref mechanism proof: a replaced commit flips a counter's verdict (`exit 0 dispositions_complete`) and `GIT_NO_REPLACE_OBJECTS=1` restores the real answer (`exit 1`, count 0) | `kaidoku-shokunin/.ufo/waves/round-22/w2/C2Path.md:11-13` | fits (this is exactly C2's hazard) | kaidoku | cite as the measured mechanism; mado's r67 K05/H01 already states the doc side, this is the sibling's behavioural proof |
| Guard-ordering defect (F2): `GIT_NO_REPLACE_OBJECTS` starts with `GIT_`, so a later purge deletes it; frozen order at `count-c1.py:190-193` | `kaidoku-shokunin/.ufo/waves/round-23/w1/CounterGitIsolation.md:75-91` | fits (the move in §0) | kaidoku | cite; use as the aux probe's negative control |
| Fixture that *drops* the guard to prove the counter sets it itself (`replace_ref_control`: `env.pop('GIT_NO_REPLACE_OBJECTS')`, plant `git replace`, expect the counter to fail) | `kaidoku-shokunin/.ufo/waves/round-22/tools/counter-fixtures.py:255-260` | fits (the control-set idea behind C2's `controls=11/11`) | kaidoku | cite as prior art for a replace-ref control case; do not copy code |
| Latent replace-ref defect, articulated first as R4/F8 with the two remediations (`--no-replace-objects` or the env var) | `kaidoku-shokunin/.ufo/waves/round-16/w1/SafetyReads.md:61-67`, `.ufo/waves/round-16/w2/FProducerBytes.md:53-57` | fits | kaidoku | cite as the origin of the defect class |
| Production counter guards | `kaidoku-shokunin/tools/round-25/a2/c1-calibration.py:24`, `tools/round-25/a2/c2-coverage.py:25`, `tools/round-25/instrument-custody.py:117` | fits | kaidoku | none needed |
| Hardened guard: refuse any `refs/replace/` entry, pin `PINNED_GIT_ENV`, drop every other `GIT_*` | `kotodama-shokunin/tools/ledger-token-guard.py:52-58`, `:113-116`, `:126-132` | fits (strongest sibling repair; goes beyond env presence to refusal) | kotodama | cite as the sibling that refuses rather than ignores; mado's claim explicitly does *not* add refusal (r67 knowledge limits), so no adoption this round |
| `check-*.py` that already guards itself and is the model repair | `tsukuroi-shokunin/tools/check-self-assessment.py:100` (guard in the env literal) and `mado-shokunin`'s own `quality/check-tool-ledger.py:101-112` (allowlist + `env["GIT_NO_REPLACE_OBJECTS"]="1"`) | fits | tsukuroi / mado | use mado's own file as the repair template (it is the base's only guarded reader, per the baseline receipt) |
| Inherited-`GIT_DIR` leak probe (writes redirected by ambient `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`, canary run) | `tsukuroi-shokunin/tools/probe-git-env-leak.py:6-9`, `:56-64`, `:147-150` | does-not-fit (different hazard: *write* redirection, not object-read shadowing) | tsukuroi | do not absorb; name in Limits if an executor is tempted to "close the whole git-env class" |
| Child-env contract probe (strace `execve`, pinned `GIT_CONFIG_*`) | `tsukuroi-shokunin/tools/probe-git-child-env-r31.py:20-39`, `:83-98` | does-not-fit | tsukuroi | do not absorb |
| AST source channel over a gate population (ambient reads / inheriting spawns / hiding constructs) | `tsukuroi-shokunin/tools/probe-child-env-allowlist-r33.py:44-60`, `:553` | partially fits (same instrument *kind*: static env construction over gate files) | tsukuroi | cite as the sibling static-env instrument; note its r32 finding that presence-only rules are dodged by value channels — the empirical support for mado's presence-tested Limit |
| Guard in a census/landing tool | `souji-shokunin/census/round-26/waves/assimilation/validate/tools/souji-landing-gate.py:185`, `souji-size-census.py:96`, `souji-rev-pin.py:60`; `mori-shokunin/tools/mori-content-review.py:84-92`; `mori-shokunin/tools/mori-evidence-loss.py:229-238` | fits | souji / mori | cite as fleet-wide convention: the guard belongs in the child env constructor, not the parent's export |
| Rule recorded but no production code in the lane (`tools/`/`quality/` carry no guard) | `tabi-shokunin/corpus/lessons/round-37.md:35` ("B1 `GIT_NO_REPLACE_OBJECTS=1` on every git read plus `refs/replace/*` enumeration") | fits as a *rule* | tabi | cite the rule, not code; tabi's implementation lives only in its wave sandboxes |

Verdict on C2: **not a duplicate**. Sibling lanes guard their own readers one file at a time (and
kotodama additionally refuses); none counts a *declared gate population* and classifies each file's
guard construction, and none repairs twelve gates in one move. The census shape is novel; the
mechanism, the ordering trap and the fixture design are all siblings' and must be cited.

### (b) Harness self-mutation (a selftest that kills its own kill credit)

| item | source file:line | fit | owning lane | what mado does about it |
|---|---|---|---|---|
| A battery that mutates a copy of its counter (`BAD_ENV` drop) and asserts the mutant fails detection, `SystemExit("mutant anchor is not unique")` on a non-unique anchor | `kama-shokunin/tools/round56-env-leg-battery.py:72-82` | fits (same family: mutate a copy, assert the detector goes red) | kama | cite; mado's S1-S3 are behaviourally the same idea applied to the harness's *scoring* |
| Replaces a syntactic call-site walk because "dead code, an unused function, an early return or a rebound `run` all satisfy" it; executes the battery and profiles `run` / `assert_mutant_breaks_detection` | `kama-shokunin/tools/round58-battery-exec-check.py:1-12`, `:45` | fits (the "selftest never runs the decision body" class) | kama | cite as the sibling that solved the same defect one level up; mado's fix is inside the harness's own `--selftest`, kama's is an external profiler |
| No-op mutant roster including `N06-run-body-noop`, `N07-mutant-assert-noop`, `N12-ignore-leg-result`, `N14-ignore-mutant-result` | `kama-shokunin/tools/round59-c1-counter.py:13-17` | fits (closest in kind: force/ignore the credit) | kama | cite; mado's S1/S2/S3 are the three-point subset of this roster for one harness |
| Supplement for mutants "the built-in selftest fails to kill" | `kama-shokunin/tools/release-recheck-selftest-extra.py:4-5`, `:16` | fits (selftest mutation coverage as an explicit object) | kama | cite |
| Kill accounting splits "killed by the tool's own selftest" from "killed by the frozen counter" | `kama-shokunin/tools/shortcut-tally.py:33-40` | fits (attribution of a kill) | kama | cite; C1's `selftest=0 killed=3/3` must stay attributable to the harness's selftest, not to the outer recipe driver |
| The defect itself, recorded by the lane | `mado-shokunin/SCORECARD.md:3592` ("two harness self-mutants survive its selftest (C2-R1/R2)"); `corpus/lessons/round-67-verifier-spotcheck.md:181-186` | fits (ground truth C1 answers) | mado | C1's target; no sibling needed |
| Should-fail batteries over fixture shapes (mutate the *fixtures*, not the checker) | `tsukuroi-shokunin/tools/mutants-owed-statements-r29.py:1-25` | does-not-fit (different object) | tsukuroi | none |

Verdict on C1: **novel in shape, same family as kama's**. No sibling counter applies frozen recipes
to the *scored harness's kill-credit call sites* and scores a kill by the harness's *own* `--selftest`
rc, with the same recipes applied to the predecessor harness at `--base-rev` as the do-nothing
control. Kama's `round56` battery is the nearest precedent and should be cited; kama's r58/r59 work
is the evidence that this whole class is real, not invented here.

### (c) Git-reader censuses over a gate population

| item | source file:line | fit | owning lane | what mado does about it |
|---|---|---|---|---|
| Population census over a counter gate set (`.ufo/waves/round-*/count-*.py` + `tools/round<N>-*.py`), registered vs unregistered, from `git ls-tree HEAD` | `kama-shokunin/tools/gate-registry-check.py:11-19`, `:43`, `:56-59`, `:123-127` | fits (population-from-objects, not worktree/index) | kama | cite: kama shipped a "stale-index population" arm (`:365`, `:428`) because an index-sourced population is a defect; mado's `population=20` is already object-enumerated |
| Lexical instrument census over `quality/` + `tools/` (82 mention git, 79 contain `show`/`cat-file`, 3 guarded) | `mado-shokunin/corpus/knowledge/replace-ref-citation-boundaries-r67.md:78-104`, `:152-153`, `:168` | fits (mado's own predecessor) | mado | C2 **supersedes** it for gate files only; the entry's 76 unguarded files of the wider set stay uncovered and should be re-stated in C2's Limits so `unguarded=0` is not read lane-wide |
| Reader counters that count *fixture readers*, not git readers | `tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py:251` (`rekeyed=… readers=R/7`), `round-56/c1/measure.py:288` | does-not-fit (same token, different meaning) | tameshi | do not cite as prior art; naming it prevents a wrong comparison |

Verdict: **no sibling census classifies guard construction over a gate population.** Kama owns the
population-from-objects pattern, tsukuroi owns static env analysis, mado combines them. Novel, with
those two citations owed.

---

## 2. `shokuknow/merge/mado/` assimilation screen

Read `MERGE-REPORT.md` and `SOURCES.append.md` (read-only; no campaign tool run).

- **Fit as evidence: none.** All 147 staged rows are compositor/desktop documentation from rounds
  1-16 (Hyprland IPC, Waybar modules, hypridle/omarchy, ArchWiki translations, two literature rows,
  the gkeep/focus-grab chain). A case-insensitive screen of the staged rows for
  `no_replace|replace-ref|selftest|mutant|mutation-test|counter` returns two lines, both the word
  "counterpart" in prose (`SOURCES.append.md:34`, `:98`) — zero rows bear on C1 or C2. The package
  would add no evidence to either claim.
- **Collision count: 94 of 147.** Derived with the round prompt's 0-3-space tolerant row pattern,
  against the registry at the pre-r68 base and again against the worktree (both 94):

```sh
python3 - <<'PY'
import re, subprocess
pat = re.compile(r'^ {0,3}\|[ \t]*S([0-9]{3,})')
ids = lambda t: [int(m.group(1)) for m in map(pat.match, t.splitlines()) if m]
staged = ids(open('/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md').read())
lane = ids(subprocess.run(['git','-C','.','show','510100c8:corpus/SOURCES.md'],
                          capture_output=True, text=True).stdout)
print(len(staged), len(lane), len(set(staged) & set(lane)))
PY
# -> 147 373 94          (exit 0)
```

  Staged-only ids are `S222-S252`, `S254-S257`, `S259-S276` (53 rows); the other 94 already exist in
  the lane registry. The package's own header ("lane registry currently holds **192** rows") is 181
  rows stale — the registry holds 373 at `510100c8` and its max id is `S436`, above the staged max
  `S349`. This reproduces the round-67 connector figure exactly (`LOG.md:3242`, "staged ids collide
  94/147"), up from the round-32 screen's 27 (`LOG.md:2473`). **Disposition: do not append; a future
  adoption would have to re-id 94 rows and re-open the rows that the lane already mined under those
  ids.**
- No staged row is a new claim; nothing here touches the frozen declaration.

---

## 3. `considerthese` screen

Newest file is `considerthese/2026-10-28.md` (no newer file exists; `ls considerthese/` ends there).
Its six proposals were checked against both claims.

- **Proposal 2 was executed once at the pre-r67 tip** (`LOG.md:3258-3263`): gate exit 1,
  `files=33466 findings=280`, `waived 49/47`, the r37/r38 socket tables carrying 5 and 715 process
  rows; routed to L0 as an operator history/redaction decision. **What remains is that operator
  decision, not lane work** — and it is not C1 or C2. It must not be re-run as evidence for either
  claim: a privacy-gate finding count is neither a harness kill nor a reader guard.
- **Answer: none.** No still-unimplemented proposal fits this round's claims without widening them.
  Proposals 1, 3, 5 and 6 are reflection-process changes; proposal 4 (a live-tool table for the eight
  live-state tools) is operability-flavoured but its object is the host tools, whereas C2's frozen
  object is `quality/check-*.py`; adopting it would add a second object to a frozen predicate.
  Proposal 2's remainder is operator-owned (above). The nearest *lane-internal* item that does fit is
  not a considerthese proposal at all: r67 routed defect 3's "unguarded git-reader census"
  (`corpus/lessons/round-67-verifier-spotcheck.md:183`), which C2 is executing.

---

## 4. Adjacent-domain evidence mado must not absorb

| item | source file:line | fit | owning lane | what mado does about it |
|---|---|---|---|---|
| Secret-route scrubbing before a URL/path is written into a receipt (`path_carries_secret`, secret route names, query stripping) | `kagi-shokunin/corpus/release-clock.py:151-179`, `:222` | does-not-fit (secrets in receipt construction) | kagi | C2 classifies the *presence* of one env key; it must not grow into a credential sweep, and no repair may add/remove env names beyond `GIT_NO_REPLACE_OBJECTS` |
| Retention/minimization decisions over a frozen content population (`retain` / `minimized` / `unresolved`, blob digests, content basis) | `mori-shokunin/tools/mori-content-review.py:1-23`, `:84-92` | does-not-fit (session-material retention) | mori | the r37/r38 socket tables and the r67 privacy finding stay operator/L0-owned; C2's repair of `quality/check-session-material.py` (a reader at base — see §5) must not be reported as progress on redaction |
| Package state and the pause gate (premise verdicts, evidence pointers, "does not authorize lifting the pacman pause") | `tsukuroi-shokunin/tools/check-pause-gate.py:1-14` | does-not-fit | tsukuroi | no install/upgrade this round; the read-only census proves nothing about package state |
| Inherited `GIT_DIR`/`GIT_WORK_TREE` write redirection (canary probe) | `tsukuroi-shokunin/tools/probe-git-env-leak.py:6-9` | does-not-fit | tsukuroi | C2's guard is about object reads; do not claim it stops a write-redirecting environment |

---

## 5. Repair-shape map for the twelve (evidence only, no counter claimed)

Read at `510100c8` with a local heuristic (`git show` + the frozen verb vocabulary). It reproduces
the baseline's `readers=13 guarded=1` exactly — 13 files carry a git token plus a quoted verb, and
`quality/check-tool-ledger.py` is the only guarded one — which is an independent corroboration of
`.ufo/waves/round-68/control-baseline-r68.txt`, not a replacement for the frozen command.

| shape | files (line of the env construction) | what a correct repair looks like |
|---|---|---|
| purge-all-`GIT_*` (5 of 12) | `check-axis-scores.py:99,121`; `check-evidence-pointers.py:71`; `check-freeze-order.py:45`; `check-index-rows.py:58`; `check-index.py:51` | store the key **after** the purge; a store before it is erased (kaidoku F2) and still census-guarded |
| allowlist helper (2) | `check-wave-done.py:177-190` (`git_env()` + `GIT_ENV_KEYS` at `:172`); `check-tool-ledger.py:101-112` (already correct, the template) | add `env["GIT_NO_REPLACE_OBJECTS"] = "1"` inside the helper |
| four-key literal passed positionally (1) | `check-anchor-cover.py:102-103` (env handed to `git_blob(...)` positionally, not as `env=`) | add the key to that literal; an `env=` keyword elsewhere would not reach the call |
| remaining unguarded readers (5) | `check-control-receipts.py`, `check-deliverables.py`, `check-landed-contract.py`, `check-round-outcome-first.py`, `check-session-material.py` — each builds its own env at its call site | one store per env constructor (`5 purge + 1 allowlist-unguarded + 1 literal + 5 here = 12`) |

⚠ `quality/check-session-material.py` is among the twelve. Its repair changes which bytes the privacy
gate reads under a planted replace ref; it must not be described as a privacy remedy (§4).

---

## 6. What was not found

- No sibling lane reads a *declared gate population* and classifies `GIT_NO_REPLACE_OBJECTS`
  construction (C2's census shape) — novelty confirmed against `kagi`, `kaidoku`, `kama`, `kotodama`,
  `mori`, `souji`, `tabi`, `tameshi`, `tsukuroi`.
- No sibling counter mutates a harness's kill-credit call sites and scores the kill with the harness's
  own selftest (C1's shape); kama's r56/r58/r59 are the family, not the shape.
- No staged `merge/mado` row bears on either claim; 94/147 ids collide.

## 7. Receipts

```
$ git -C mado-shokunin log --oneline -3
40d2bef8 round-68: successor control harness and the one-wave dispatch evidence
e0727cda round-68: freeze the two claims, predicates and control sets
2ca2bec3 round-68: baseline counters and frozen control sets (pre-freeze)

$ git -C mado-shokunin ls-tree -r --name-only 510100c8 quality | grep -cE '^quality/check-[^/]+\.py$'
20
$ collision derivation (above): 147 373 94        exit 0
$ heuristic at 510100c8: readers=13 guarded=1     (agrees with control-baseline-r68.txt)
```

No production file was written. Seat directory contains this file only.
