# R69ConnSiblings — cross-instrument overlap scan (round 69, read-only)

Seat: connector, leaf (no dispatch). Scan target: the lane `mado-shokunin` at base
`04093b83f73a841117d3b31dbb2a6063f4f2a454`, working-tree snapshot `2026-11-04T01:51:39Z`,
lane HEAD at snapshot `6a5cefd252c41c7ff71217da65126fc831f8bc34`
(`5fc29ae7 round-69: paired-recipe harness, C1 counter and C2 dominance counter`,
`6a5cefd2 round-69: claim measurements, harm watch and census receipts`).

Read-only seat. No lane file was written except this report. No counter was edited, re-scoped or
aliased. Scratch `/fast/scratch/hyaku/mado-r69/R69ConnSiblings/` was used for probe scripts, inline
probes and the counter runs below, then removed (trailer). Findings only; integration belongs to the L1.

Commands used and their rcs are named per section. `r68` below means the rule of
`quality/counters/c2-r68-reader-guard.py:91-138`; `r69` means the rule of
`.ufo/waves/round-69/proto/c2-classify.proto.py:230-300` and of the integrated
`quality/counters/c2-r69-guard-dominance.py` (worktree sha256 `56ae28b6…3e7`, which scored
identically to the prototype on every case below).

---

## 1. `GIT_NO_REPLACE_OBJECTS` — where the round-69 ground already is

Scan: `grep -rn --exclude-dir=.git --exclude-dir=.jj 'GIT_NO_REPLACE_OBJECTS' .` (575 lines across
code, receipts, corpora and `.ufo`). Differential classification over the frozen population,
`python3 …/classify_diff.py 04093b83…`, rc 0:

```
SUMMARY rev=04093b83… population=20 readers=13 r68_guarded=13 r69_guarded=13 diffs=0
```

So inside the frozen population the new dominance rule changes **no verdict**; it discriminates
only on the four frozen negative shapes (below). The integrated counter reproduces the target
end-to-end, rc 0:

```
MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET rev=6a5cefd252c41c7ff71217da65126fc831f8bc34
```

Cross-set check (prototype and integrated counter, `classify` per case): the r69 rule scores
**11/11 on the round-68 control set** as well as 11/11 on its own — the new predicate loses nothing
the old set caught, and the r68 rule scores 7/11 on the new set (matches
`control-baseline-r69.txt` § C2). No discrimination regression exists on the union.

### 1a. The 13 population readers — construction shape (all `key position` + a dominance flow)

| file | construction (key position) | used at | flow |
|---|---|---|---|
| `quality/check-anchor-cover.py:104` | dict-literal key | `env=` at same call | (a) inline |
| `quality/check-axis-scores.py:99,122` | `env[…] = "1"` | `env=env` | (b) name |
| `quality/check-control-receipts.py:62` | `env[…] = "1"` | `env=env` | (b) name |
| `quality/check-deliverables.py:96,116` | `dict(os.environ, KEY="1")` | inline `env=` | (a) inline |
| `quality/check-evidence-pointers.py:72` | module `GIT_ENV[…] = "1"` | `env=GIT_ENV` | (b) name |
| `quality/check-freeze-order.py:46` | `env[…] = "1"` | `env=env` | (b) name |
| `quality/check-index.py:50`, `:283` | `env[…] = "1"`; `dict(KEY="1")` | `env=` | (b)/(a) |
| `quality/check-index-rows.py:57,406` | `env[…] = "1"` | `env=env` | (b) name |
| `quality/check-landed-contract.py:57` | `env=dict(…KEY…)` | inline | (a) inline |
| `quality/check-round-outcome-first.py:74,128` | inline `env=dict(…KEY…)` | inline | (a) inline |
| `quality/check-session-material.py:927,984` | inline `env=dict(…KEY…)` | inline | (a) inline |
| `quality/check-tool-ledger.py:109` | producer `git_env()` | `env=git_env()` at `:119-120` | (b) producer |
| `quality/check-wave-done.py:187` | `env[…] = "1"` | `env=env` | (b) name |

No `os.environ[KEY] = …` store exists in the population (the only `os.environ[…]` stores are
`TMPDIR`/`HOME` at `quality/check-tool-ledger.py:847,860` and `quality/check-wave-done.py:1041`),
so rule 1 (key position) costs the population nothing.

### 1b. Constructions the r69 rule treats differently from the r68 rule

| shape | r68 | r69 | rule sentence that changes |
|---|---|---|---|
| key only in **value** position (`{"LABEL": "GIT_NO_REPLACE_OBJECTS"}`) | guard | not a guard | key-position rule (C2 §1) |
| guard in a literal-false branch (`if False:` / `while False:`) | guard | not a guard | dominance, literal-false exclusion |
| guard built in an **uncalled** helper | guard | not a guard | dominance flow (b) requires a use at the call |
| guard **overwritten** before the call | guard | not a guard | "no intervening rebinding … without the key" |

These are exactly the four frozen cases that score `7/11` under r68 and `11/11` under r69. No
other *population* shape differs.

### 1c. Out-of-population code constructors, and the three real verdict flips

Read with the same classifiers; `probe` = per-file `classify` over the file's bytes.

| file:line | construction | r68 | r69 | note |
|---|---|---|---|---|
| `quality/counters/c1-r56-autoreload-entry.py:58,67` | `self.env = {…KEY…}`, `env=self.env` | no | no | attribute flow, both rules blind; runtime guarded |
| `quality/counters/c1-r66-register.py:45` | `env.update(KEY="1")` | yes | yes | `git()` at `:41-49`: literal argv + `env=env` |
| `quality/counters/c1-r67-register.py:97` | same | yes | yes | |
| `quality/counters/c1-r68-landing-controls.py:109` | producer + `env=child_env(home)` at git calls | yes | yes | |
| `quality/counters/c1-r68-selfmutants.py:65` | producer `git_env()` | **yes** | **no** | git launch is `run(argv, …)`/`git(args)`; argv arrives as a parameter (`:72`, `:104`, `:115`) |
| `quality/counters/c2-r67-landing-controls.py:107` | producer + `env=git_env(home)` at literal git calls | yes | yes | |
| `quality/counters/c2-r68-reader-guard.py:67` | producer `git_env()` | **yes** | **no** | same two-hop shape (`:72-78`) |
| `quality/counters/c3-r56-used-by.py:70` | dict-literal key; production use `env=self.env` at `:95` | no | **yes** | the `yes` is carried by the **selftest**: `env = git_env(work)` at `:350` handed to `sh(D, […], env)` at `:357-358`, whose `env` parameter reaches `subprocess.run(["git", …], env=env)` at `:310`. The production read at `:95` is attribute flow and matches neither rule. |
| `tools/mado-receipt-citecheck.py:103` | inline `env=dict(os.environ, KEY="1")` | yes | yes | |
| `quality/counters/c1-r65-register.py:88-93` | `env = dict(os.environ)` + LOCKS/LC_ALL/PAGER, **no key**, `env=env` | no | no | genuinely unguarded git reader |
| `quality/counters/c2-r65-landing-instrument.py:46-48,69,77` | `GIT_ENV` strips every `GIT_*`, no key; `env=GIT_ENV` | no | no | genuinely unguarded; its extraction cannot be protected by a parent export |
| `quality/counters/c2-r66-landing-instrument.py:29,69,77` | same shape | no | no | same defect one generation later |
| `quality/counters/c1-r69-paired-recipes.py:84-86,435` | `run(argv)` builds the guarded env; git calls pass argv | n/a | **no** | new counter reads "unguarded" under its own rule |
| `quality/counters/c2-r69-guard-dominance.py:94-96,435` | same two-hop shape | n/a | **no** | same |

Mentions only (not constructors): `corpus/knowledge/gate-git-read-guards-r68.md:80-245`,
`corpus/knowledge/replace-ref-citation-boundaries-r67.md:5-111`, `corpus/lessons/round-6{6,7,8}*.md`,
`corpus/QUALITY.md:646-669`, `corpus/README.md:90`, `corpus/SOURCES.md:386`, `LOG.md:3226-3269`,
`PROVINCE.md:281-307`, `.ufo/waves/round-69/{claims-declaration-r69.md,controls/c2-controls-r69.json,make-spec-r69.py}`,
`c1-r66-register.py:43` (comment), `c1-r68-landing-controls.py:14,28,31,64` (docstring/`R_TOKEN`),
and the ignored compiled residue `quality/counters/__pycache__/c1-r68-landing-controls.cpython-314.pyc`
(`git check-ignore` confirms `.gitignore:3`; it is a grep-only artifact, never part of a REV census).

**Rule that changes for the flips.** The three flips are not the four frozen shapes: they are the
cost of *dominance*. r69 binds a guarded name only where a call site is recognized as a git launch
(`call_is_git`, argv literal or a name bound to one), so a module whose launch is behind a
`run(argv)`/`git(args)` helper — argv arriving as a parameter — or whose env rides on an attribute
reads **no** even when it dominates at runtime. Conversely `c3-r56-used-by.py` reads **yes** because
a test-local producer dominates a test-local `sh()` git call. Both are stated limits
("one module, one hop, no alias/attribute/container flow") but the declaration's flow (a)-(c) does
not name the *argv-parameter* shape, which is the one that demotes two r68 tools and both new
counters.

### 1d. Consolidated ground table (ground · path:line · r69 verdict · action for the L1)

| ground | lane path:line | r69 rule verdict | action for the L1 |
|---|---|---|---|
| frozen population, 13 readers | `quality/check-*.py` (13 files, §1a) | guarded=13, unguarded=0 at `04093b83` and `6a5cefd2` | none; commit the per-file table already produced by the C2 seat |
| value-position key | `.ufo/waves/round-69/controls/c2-controls-r69.json` case `value-position-only` | not a guard | none (frozen case) |
| dead branch | same file, `dead-branch-only` | not a guard | none (frozen case) |
| uncalled helper | same file, `uncalled-helper` | not a guard | none (frozen case) |
| overwritten env | same file, `overwritten-env` | not a guard | none (frozen case) |
| two-hop launch helper (argv parameter) | `quality/counters/c2-r68-reader-guard.py:72-78`, `quality/counters/c1-r68-selfmutants.py:62-72`, `quality/counters/c1-r69-paired-recipes.py:84-86,435`, `quality/counters/c2-r69-guard-dominance.py:94-96,435` | **no** (grammar boundary; runtime guarded) | name it in the C2 entry's Limits; do not widen the population without restructuring |
| attribute-carried env | `quality/counters/c3-r56-used-by.py:95`, `quality/counters/c1-r56-autoreload-entry.py:67` | **no** for the production read; `c3` reads yes only via its selftest `:350,:357-358` | state "file-level flow-existence, not call-level coverage" in the entry/counter docstring |
| shell export | `quality/landing-counters.sh:8` (nav child `:24-28`) | **no** (not Python; guard is inherited) | keep the shell boundary sentence concrete in the entry |
| r65/r66 landing instruments | `quality/counters/c2-r65-landing-instrument.py:46-48,69,77`, `quality/counters/c2-r66-landing-instrument.py:29,69,77`, `quality/counters/c1-r65-register.py:88-93` | **no** (genuinely unguarded) | record as outside the population; candidate ground for a future round, not this claim |
| r68 tools retained as base legs | `quality/counters/c1-r68-landing-controls.py:109`, `quality/counters/c2-r68-reader-guard.py:67` | harness yes; classifier yes under its own rule, no under r69 | supersession note in the lesson; no alias (none added) |
| new counters | `quality/counters/c1-r69-*.py`, `c2-r69-guard-dominance.py` | C1 counter no, C2 counter no, harness yes | do not cite their own guard shape as evidence anywhere; population stays `check-*.py` |

---

## 2. The other instruments that read git objects outside `quality/check-*.py`

("Would the dominance rule pass it?" = `classify()` on the file's bytes, i.e. reader + guard.)

| instrument | carries the guard? | dominance pass? | bytes read |
|---|---|---|---|
| `quality/landing-counters.sh` | yes, by **shell export** at `:8` (`export GIT_OPTIONAL_LOCKS=0 GIT_NO_REPLACE_OBJECTS=1`), after `:7` unsets every `GIT_@` | **no** — not Python; `ast.parse` cannot read it, so both rules say no. Its inline nav child (`:24-28`, `subprocess.check_output(['git', …])`, no `env=`) is guarded only by inheritance. | shell; effective for the nav child and for every leg child that does not build its own env |
| `quality/counters/c3-r56-used-by.py` | yes, dict-literal key `:70`; production use `env=self.env` `:95` | **yes, but for the wrong reason** — the recognized flow is the selftest's `:350` producer + `:357-358` `sh(…, env)`; the production attribute flow at `:95` is outside both rules | py |
| `tools/mado-receipt-citecheck.py` | yes, inline `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` `:103` | **yes** (flow (a)) | py |
| r65 instrument `quality/counters/c2-r65-landing-instrument.py` | **no** — `GIT_ENV` at `:46-48` strips every `GIT_*` and re-adds none; `env=GIT_ENV` at `:69` (own `git()` extraction) and `:77` (legs) | **no** (correctly: genuinely unguarded) | py |
| r65 extracted children | `quality/check-tool-ledger.py:109` yes (producer, `env=git_env()` `:119-120`); `quality/counters/c3-r56-used-by.py:70` yes (see above); `tools/mado-receipt-citecheck.py:103` yes; `quality/landing-counters.sh:8` yes by export | the three `.py` children pass; the shell child is invisible to the rule (export + inheritance) | py+sh |
| r66 sibling `quality/counters/c2-r66-landing-instrument.py:29,69,77` | **no** — same stripping `GIT_ENV`, same `env=GIT_ENV` | no (correct) | py |

The r65/r66 instruments are the sharp case: they *strip* the parent's guard and do not re-add it,
so the r67 lesson's parent-export reasoning does not reach their own object reads. They are outside
the frozen 20-file population and outside this round's target; recording, not absorbing.

---

## 3. Shared housekeeping between C1 and C2

### 3a. Files each claim touches (from `w1-spec.json` seat scopes + declaration)

| claim | own artifacts | shared round-record files |
|---|---|---|
| C1 | `quality/counters/c1-r69-landing-controls.py`, `quality/counters/c1-r69-paired-recipes.py` | `corpus/lessons/round-69.md` (M69-1 lives here) |
| C2 | `quality/counters/c2-r69-guard-dominance.py`, `corpus/knowledge/gate-guard-dominance-r69.md`, `corpus/SOURCES.md` row S438 (`:388` now), `corpus/README.md` row | `corpus/lessons/round-69.md` (same file), and via the cadence seat `SKILL.md`, `SCORECARD.md`, `PROVINCE.md`, `LOG.md` |

The declaration's "the two claims share only the wave and the lesson" is exact for claim artifacts;
the round-record files are shared by every round and are not claim scope. The one real intersection
is `corpus/lessons/round-69.md`: C1's M69-1 (equivalent-mutant misclassification) and C2's
boundary/limits prose must not contradict each other about what "unguarded" means.

### 3b. Selftest helpers both claims duplicate

| helper | `c1-r69-landing-controls.py` | `c1-r69-paired-recipes.py` | `c2-r69-guard-dominance.py` | identical? |
|---|---|---|---|---|
| `emit` | `:158` | `:93` | `:103` | yes (3×, 43 chars) |
| `want` | `:623`, `:667` | `:325` | `:607` | yes (3×, 59 chars) |
| `_no_spawn` guard | `:796`, installed `:799` | `:408`, installed `:411` | `:686`, installed `:689` | yes (3×, 95 chars) |
| `absolute_scratch` | `:125-147` (880 chars; walks every path component for symlinks at `:129-136`, refuses `/` at `:141-142`, does not require the dir to exist) | `:101-113` (592 chars; root-symlink only at `:107-108`, no `/` refusal, **requires the dir to exist** at `:105-106`) | `:111-123` (same 592-char body) | **no — diverged** |
| `git_env` | `:105` `git_env(home)` | `:75` no-arg | `:86` no-arg | no (three bodies) |
| `run` | `:149` `run(argv, env, …)` | `:84` builds env internally | `:94` builds env internally | no |
| `UNSAFE_ROOTS` | `:67` | `:60` | `:70` | yes tuple; validation differs |

Divergence consequence: the counters **accept** a scratch root (or a path) the harness **refuses** —
the harness rejects any symlinked *component* (`:129-136`) and `/` (`:141-142`); the counters reject
only a root that is itself a symlink (`:108` / `:118`) and never check `/`. C1's counter passes
`<its scratch>/st-candidate` to the harness, so a caller root with a symlinked ancestor passes the
counter's check and fails the harness's with rc 2. Also the counters require the root to exist
(`:105-106` / `:115-116`) while the harness creates its own `<root>/r68-c1/…` tree without
requiring the root (`:393-395`, `:829-831`) — observed: the C1 frozen command with an uncreated
`<scratch>` exits **2** (`c1-r69-paired-recipes.py: --scratch-root is not a directory`); the same
command succeeds once the directory exists.

### 3c. Scratch-tree collision risks (`--scratch-root` subdirectory names)

| owner | fixed path | line | risk |
|---|---|---|---|
| r69 harness | `<root>/r68-c1` then `rmtree` | `c1-r69-landing-controls.py:393-394` | **same names as the r68 harness** (`c1-r68-landing-controls.py:393-394`, `:801-802`): both generations' `measure()` and `--selftest` trees are `r68-c1` / `r68-c1-selftest`; concurrent runs on one root destroy each other while running |
| r69 harness | `<root>/r68-c1-selftest`, `rmtree` in finally | `:829-830`, `:835` | same, selftest leg |
| C1 counter | `<root>/r69-c1-paired`, `rmtree` **without** `ignore_errors` | `:193-195` | fixed, non-pid; second concurrent run or a planted symlink at that name raises |
| C1 counter | `<root>/st-candidate`, `<root>/st-<label>-<name>`, `<root>/case-<name>` | `:213`, `:165`, `:295` | fixed; a future C2 use of `st` or `case-*` would collide by name |
| C2 counter | `<root>/r69-c2-dominance`, `rmtree` | `:503-505` | fixed, non-pid |
| C2 counter | `<root>/base-counter.py`, `<root>/controls-tampered.json` | `:465-466`, `:663-664` | unnamespaced **files at the shared root**; safe against C1 only because C1 uses `r69-c1-paired/` |
| C2 counter | `<root>/base` | `:532` | inside the C2 work tree (`r69-c2-dominance/`); no name shared with C1 |

Cross-claim collision by top-level name: **none today** (`r69-c1-paired` vs `r69-c2-dominance`).
The hazards are (i) the r68/r69 harness name duplication, (ii) per-counter fixed names with no pid
suffix (two verifier runs on one root), (iii) two unnamespaced files at the root, and (iv) the
scratch-root validator divergence in 3b. The L1 should give each frozen-command invocation its own
subdirectory and pre-create it.

---

## 4. The r68 tools this round supersedes

Selftests run today (rc in parentheses, all read-only):

| tool | selftest result | still works? | becomes misleading? | supersession note needed |
|---|---|---|---|---|
| `quality/counters/c1-r68-selfmutants.py` | `MADO_R68_SELFMUTANTS_SELFTEST: 27/27`, rc 0 | yes at its pinned revisions; it is the r68 calibration counter | its recipe labels S1-S3 are **not** r69's R1-R3 (the declaration says so); under the r69 rule its own source reads `guard=no` (two-hop, `:62-72`) | yes: "r69's R1/R2/R3 supersede this tool as the calibration gate; S1-S3 are not R1-R3; the r69 census's silence about this file's guard is a grammar boundary, not an absent guard" |
| `quality/counters/c1-r68-landing-controls.py` | `MADO_R68_LANDING_CONTROLS_SELFTEST: 52/52`, rc 0 | yes; it is C1's **base artifact** (`base=0/3`) and its three decision sites are byte-identical to the r69 harness (`:439`, `:491-492`, `:799`) | only if read as the paired-oracle harness — it lacks the r69 selftest assertions by design | yes: "kept at its revision as the do-nothing base; not an alias target; do not run it as the current harness" |
| `quality/counters/c2-r68-reader-guard.py` | `MADO_R68_READER_GUARD_SELFTEST: 26/26`, rc 0; full measure at `04093b83` rc 0 → `population=20 readers=13 guarded=13 unguarded=0 controls=11/11` | yes on its own control set; it is C2's base classifier (`base_controls=7/11`) | yes: docstring `:16-19` rule (d) "a constant inside any `env=` keyword subtree" is precisely the shape r69 rejects; a reader who takes its `guarded=yes` as dominance evidence is wrong for 4/11 frozen cases | yes: "superseded as the census; retained as the base leg; value-position is not a guard under r69" |

No compatibility alias was added anywhere: the r69 counters reach the r68 files only by path
constants used for **base-leg extraction** (`c1-r69-paired-recipes.py:49`,
`c2-r69-guard-dominance.py:57,531`), never by import/re-export. Current registry rows
`SKILL.md:2809-2810` still describe the r68 rules as the mado gates; no `mado-r69` row exists yet
(`grep -rn 'mado-r69' SKILL.md` → empty), so the cadence seat's rows are the only place the
supersession becomes visible to an operator.

---

## 5. Sibling-lane overlap (adjacency duty: report, never absorb)

| lane path:line | what it implements | same craft? | contested scope? |
|---|---|---|---|
| `kotodama-shokunin/tools/harness/receipt_guard_adoption.py:285` (`NodeMaps`, parent/statement-list walking), dominance rule bullet at `:17-21` | a guard **call** must dominate a receipt **write** in the same statement block; try-handlers that terminate count, flag-gated calls do not | **same craft family** as r69 dominance (intra-module statement-order walk, explicit control-flow rules) | no: different guard (a receipt guard function), different sink (a JSON write), different lane; no `GIT_NO_REPLACE_OBJECTS` involvement |
| `kotodama-shokunin/tools/harness/round_runner_conformance.py:462` | states the limit verbatim: "Guard dominance recognizes an unconditional earlier guard call in the enclosing suite; unrecognized call-flow and dynamic publication mechanisms remain outside this checker" | same craft family; the boundedness rationale is the same | no |
| `tsukuroi-shokunin/tools/score-selftest-literals-r40.py:1-30` | frozen substring mutants, applied only at `occurrences == 1`, killed iff the selftest does not print its PASS line / rc ≠ 0, with an unmutated green control | **same craft** as C1's recipe counter | no: different surface (`tools/tsukuroi-census.sh`), different lane; C1's claim is its own harness + recipes |
| `tameshi-shokunin/tools/mutate-and-run.sh:1-80` | generic mutation runner: pristine copy, mutant sha256, KILLED = suite exit ≠ 0, kill-rate regression gates | same craft | no |
| `kaidoku-shokunin/tools/round-25/instrument-custody.py:117` | custody of git instrument references; constructs the guard in its own env | not dominance (custody/contract checker) | no |
| `tsukuroi-shokunin/tools/score-census-readers-r45.py:128-129` | `git()` = `subprocess.run(['git', …])` with **no** `env=` — an unguarded git reader in a sibling lane | not the new rule | no; adjacent observation only |

**Adjacency verdict.** The dominance *craft* already exists in the fleet — Kotodama walks
statement-order dominance with parent/statement-list maps and publishes the same call-flow limit,
and Tsukuroi/Tameshi harden selftests with exact-once frozen recipes and kill-on-nonzero. None of
them implements a **guard-census over another lane's gate population**, and none scores
`GIT_NO_REPLACE_OBJECTS` key position; r69's claimed work (11-case discrimination + 20-file census)
is not duplicated or contested. The one thing worth carrying across lanes is the *discipline*, not
the code: publish the dominant shape and its boundary in the entry's Limits section, as Kotodama
does at `round_runner_conformance.py:462`. Report only; no absorption, no cross-lane citation in
the frozen claim (S438 is the claim's ground).

---

## 6. Contradictions and hazards the L1 must see (state, not smoothed)

1. **Production paths are being written during the scan, and the copies disagree with the drafts.**
   At `01:51:39Z`: `quality/counters/c2-r69-guard-dominance.py` is **tracked and modified**
   (HEAD blob `99595319…`, worktree `56ae28b6…`, `git diff --stat` = 172 insertions / 132 deletions
   = 303 changed lines). The other two worktree copies differ from their seat drafts:
   harness worktree `b374cfb8…` vs draft `9461a059…`; C1 counter worktree `2060da8d…` vs draft
   `f7cd7bb2…`. Any proof that names a sha must be re-run at the final integrated rev. My runs at
   `6a5cefd2` with the worktree bytes reached C1 `verdict=TARGET_MET` rc 0 and C2
   `verdict=TARGET_MET` rc 0 (exact lines in §1), but those bytes may move again. After the
   snapshot (by `01:54Z`) `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md` and
   `quality/tool-ledger.md` had become modified and `corpus/knowledge/gate-guard-dominance-r69.md`
   and `corpus/lessons/round-69.md` appeared untracked — scribe integration in progress, none of
   the counter bytes measured here.
2. **Frozen commands need a pre-created scratch subdirectory.** Both new counters refuse a
   non-existent `--scratch-root` (`c1-r69-paired-recipes.py:105-106`, `c2-r69-guard-dominance.py:115-116`);
   the harness does not require it (it creates `<root>/r68-c1/…`, `c1-r69-landing-controls.py:393-395`,
   `:829-831`). Observed rc 2 before `mkdir -p`.
3. **Scratch-root validation diverged** (§3b): counters accept a symlinked *ancestor* and `/`;
   the harness refuses both. A caller root that passes the counter can fail the harness rc 2.
4. **Name collisions** (§3c), especially `r68-c1` / `r68-c1-selftest` in **both** harness
   generations, and fixed non-pid work dirs with `rmtree`.
5. **Self-application.** Both new counters read `guard=no` under their own rule (two-hop
   `run(argv)`); the r69 harness reads `yes`. If a future round widens the population to
   `quality/counters/`, the target `unguarded=0` fails for grammar reasons, not for absent guards.
6. **Shell boundary.** `quality/landing-counters.sh:8` is a genuine, dominant guard that no
   Python-AST rule can see; the C2 entry must keep its boundary sentence concrete (shell export +
   inheritance), or a reader will take the census's silence about `.sh` files as absence.
7. **Grep residue.** `quality/counters/__pycache__/c1-r68-landing-controls.cpython-314.pyc`
   contains the token and the guard text; it is untracked and ignored, so it is never in a REV
   census, but a working-tree `grep` will show it. Not ground.

No contradiction with the frozen predicate was found: the contract line, the control digest
(`975ca3ba…f90b9`, verified), the recipe occurrence counts (R1 two-line 1/1, R2 1/1, R3 1/1 in both
the r69 and r68 harnesses) and the target counts all hold at `6a5cefd2`. The hazards above are
operability/integration, not predicate failures.

---

## 7. Bounded proposal (one move; no predicate or declaration change)

**Move.** In the C2 knowledge entry `corpus/knowledge/gate-guard-dominance-r69.md` (ScribeEntry
draft) and in `quality/counters/c2-r69-guard-dominance.py`'s docstring Limits, make the abstract
bound falsifiable with the three verified shapes, and state the aggregation explicitly:

- `yes` is **file-level flow-existence, not call-level coverage** — `quality/counters/c3-r56-used-by.py`
  reads `yes` on a test-local flow (`:350`, `:357-358`) while its production read (`:95`,
  `env=self.env`) is attribute flow the rule cannot follow; `quality/check-*` files with two git
  calls are likewise certified by one dominant call.
- `no` **outside the 20-file population is not evidence of an absent guard** — two-hop launch
  helpers (`quality/counters/c2-r68-reader-guard.py:72-78`,
  `quality/counters/c1-r68-selfmutants.py:62-72`), attribute-carried env
  (`quality/counters/c3-r56-used-by.py:95`, `quality/counters/c1-r56-autoreload-entry.py:67`),
  and shell export (`quality/landing-counters.sh:8`) are all dominant at runtime and invisible.
- the population is `quality/check-*.py` only; `quality/counters/c*`, `quality/*.sh` and
  `tools/*` stay outside (the entry already says this; the three cites make it checkable).

**Axes.** C2 (operability/discrimination prose — the claim's own axis) improves: the receipt's
`unguarded` label acquires a stated scope; C1 untouched (harness contract and 52/52→59/59
assertions unchanged); verification surface unchanged (selftest 11/11 + cross-set 11/11, no new
control case, no alias, no predicate edit). **Risk:** the entry grows; any sentence that reads as a
*rule change* would exceed the frozen predicate — the move adds only limits and cites, which the
declaration's "Not claimed" already permits. **Verification:** entry Limits section carries the
three file:line cites; counter selftest still rc 0 with `controls=11/11`; the frozen command still
prints the target line at the final rev; `grep -cF 'GIT_NO_REPLACE_OBJECTS'` on the entry is
unchanged in kind (mentions only).

Scratch: `/fast/scratch/hyaku/mado-r69/R69ConnSiblings/` removed `2026-11-04T01:54:42Z`
(`rm -rf --`; `test -e` false after). No lane write outside this report; no commit, stage or
checkout was run in the lane or any sibling lane.

Report: .ufo/waves/round-69/w1/R69ConnSiblings.md
