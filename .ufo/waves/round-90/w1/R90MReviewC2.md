# R90MReviewC2 — C2 receipt-presence check: rev-mode sweep, grammar audit, worktree-mode review

Seat: R90MReviewC2 (w1, mado round 90, hyaku run 15 attempt 1). Base 5041acf9. All runs below are **DRAFT**
(pre-freeze; the measured scoring happens only after the L1 freezes). Nothing was written under `receipts/`.
No installs (nothing needed). Scratch `/fast/scratch/hyaku/mado-r90/R90MReviewC2` removed at exit.

## 1. Rev-mode sweep over every lane commit since round 80 (DRAFT)

Command (per commit, read-only; 31 commits, `git log --format=%H 5041acf9 --since=2026-11-04`):

    python3 .ufo/waves/round-90/build/check-receipt-presence.c2.py \
      --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev <H>        # DRAFT

Result: 28 rc=0/OK, 3 rc=1/MISSING (5 missing citations total). No rc=2.

| commit | subject (truncated) | verdict | missing citations |
|---|---|---|---|
| 498855cb | round-88: records — knowledge entry, S494/S495 … | MISSING (1) | `receipts/harm-final-r88.txt` SCORECARD.md:5140 |
| 51bf076f | round-89: records — knowledge entry, S496-S500 … | MISSING (2) | `receipts/harm-final-r89.txt` SCORECARD.md:5179; `receipts/census-end-r89.txt` corpus/lessons/round-89.md:144 |
| 01be4234 | round-86: land the knowledge entry, lesson, registry rows and scorecard | MISSING (2) | `receipts/cleanup-r86.json` corpus/lessons/round-86.md:51; `receipts/census-end-r86.txt` corpus/lessons/round-86.md:95 |

All other 28 commits: OK (16 with cited=0 — tool/C1 commits and reflections touch no record file;
12 with cited 1–9). Reported line numbers verified against file bytes: `git show 498855cb:SCORECARD.md`
line 5140, `git show 51bf076f:SCORECARD.md` line 5179 and `…round-89.md` line 144 contain exactly the
cited citation text — the `-U0` hunk numbering is correct.

### Adjudication of the three MISSING verdicts

- **498855cb — real cite-before-commit defect (already routed).** `.ufo/waves/round-88/receipts/harm-final-r88.txt`
  first committed in 8e8f7ea3 (`git log --diff-filter=A`), i.e. after the records commit. This is the
  round-88 spot-check R4 defect; the verdict reproduces frozen expectation D88 exactly (same citation, no
  extra). Not a false positive: SCORECARD.md:5140 is a live evidence cell ("gate/file-plane/index/ledger in
  `receipts/harm-final-r88.txt`"), not a quote.
- **51bf076f — real cite-before-commit defect (already routed).** `harm-final-r89.txt` and
  `census-end-r89.txt` first committed in 16ee97b5. Matches frozen D89 exactly (the two citations, the
  lesson citation included). SCORECARD.md:5179 is the round-89 harm-watch row; round-89.md:144 is
  "End: `receipts/census-end-r89.txt` (records revision)." Both live pointers.
- **01be4234 — real cite-before-commit defect, NOT routed, NOT in the frozen set (new detection).**
  `cleanup-r86.json` first committed in d7ffa762 and `census-end-r86.txt` first committed in 3afdb713 —
  both **after** 01be4234 in history (`git cat-file -e 01be4234:<path>` fails for both: "exists on disk,
  but not in '01be4234'"). The citations are evidence pointers, not prose/quotes: round-86.md:51 is the R7
  scratch-cleanup row's receipt cell; :95 is the round-end bullet pointing at the census receipt. This fits
  lesson class M89-4 verbatim ("a receipt path written into SCORECARD/lesson before the receipt is
  committed") and the same-round final-commit-carry standard that routed R4/D1. Neither the round-86 spot
  check (5e78674f) nor its correction (e4875ba5) caught it. Consequences: (a) the candidate generalizes
  beyond the frozen defect commits — it finds a third instance of the routed class the lane's verifiers
  missed; (b) the frozen revision set labels only 2 of the 3 defect commits in the window, so `defects_detected=2/2`
  undercounts the class's true incidence. Routing decision for the L1 (I only report; the declaration's
  frozen set is untouched).

### OK-verdict audit (no real miss skipped)

- Independent recount: I re-parsed `git show -U0 --format=` for all 31 commits with my own diff walker and
  the candidate's citation/resolution logic re-implemented; `(cited, present, missing)` matched the tool on
  **all 31 commits** — no miscounted or mis-resolved citation, and no `present` claim was wrong (each
  `present` recomputed via `git cat-file -e <rev>:<path>`).
- Every added-line receipt reference in the 12 cited>0 OK commits that the grammar did **not** count was
  enumerated and its target checked at that commit:
  - af998dcc: brace cite `receipts/census-{start,end}-r88.txt` → both targets exist at af998dcc
    (`census-start-r88.txt`, `census-end-r88.txt` in `.ufo/waves/round-88/receipts/`). Invisible but harmless here.
  - 24ba2a9d: glob cites `receipts/index-*.txt`, `receipts/ledger-*.txt` → targets exist at 24ba2a9d
    (`index-{start,measured}-r87.txt`, `ledger-{start,measured}-r87.txt` in round-87 receipts). Invisible but harmless here.
  - f4dfd0a9: directory pointer `` `.ufo/waves/round-87/receipts/`. `` → not a file cite; all r87 receipts pre-exist.
  - 498855cb: five invisible citations of `.ufo/waves/round-88/w1/receipt-base-host-config-r88.txt`
    (a w1 evidence path, not `receipts/` → grammar-blind). That file was committed earlier in 9e36e3a3, so
    no harm — but had the freeze commit not carried it, the check would have printed OK. See §2 item 5.
  - All remaining added-line "receipt" hits are prose ("receipt tallies", "committed receipts", "see
    receipts", "control receipt", "receipt-presence check") — correctly not counted.
- Conclusion: no OK verdict in the window hides a materialized miss; two OK verdicts (af998dcc, 24ba2a9d)
  survive only because the glob/brace targets happened to already exist.

## 2. Citation grammar and resolution vs how the lane actually writes receipt paths

Probe: ran the candidate's exact `CITE` regex and `candidates()` on the forms below (DRAFT, module import
of check-receipt-presence.c2.py).

| form (live lane instance) | matched? | resolution |
|---|---|---|
| `.ufo/waves/round-89/receipts/harm-final-r89.txt` (51bf076f) | yes | as written |
| `quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt` (LOG round-36) | yes | as written |
| bare `receipts/harm-final-r89.txt` + `receipts/x.txt:12` line ref | yes | `-r89` suffix → round-89 receipts, then quality/ |
| `receipts/index-*.txt`, `receipts/ledger-*.txt` (24ba2a9d; LOG round-87; round-87 spotcheck:60-61) | **no** | silently invisible |
| `receipts/census-{start,end}-r88.txt` (af998dcc; SCORECARD:4242,4489,4561,4851,4944; LOG r84/r85) | **no** | silently invisible |
| nested `receipts/v2/ctl-c1v2.txt`, `receipts/a4/pre-60edb66e.txt` (LOG:2537-2538, round-48 lesson) | **no** | name class has no `/` |
| seat-dir `w1/ExecD2Receipt/receipts/session-material-60edb66e.txt` (round-48.md:247) | **no** | |
| `.ufo/waves/round-90/w1/w1-results.json` (SCORECARD evidence blocks; declaration) | **no** | by design (`receipts/` only) — w1 evidence cite-before-commit is unguarded |
| dir cite `.ufo/waves/round-87/receipts/.` (f4dfd0a9) | **no** | unverifiable without enumeration (declared-limit shape) |
| `receipts/x-r89.txt.bak` | yes (as `x-r89.txt`) | would report missing for a suffixed real file — theoretical FP shape, no live instance found in the window |
| `corpus/receipts/x-r89.txt` | no | lookbehind correctly rejects path-prefixed forms |

Findings:

- **G1 (main grammar gap): globs and brace expansion are silently invisible.** Both are the lane's
  established citation style for census/index/ledger/final receipts (dozens of instances in
  SCORECARD/LOG/lessons, including the round-84–88 evidence blocks the round-90 records commit will imitate).
  The check's OK verdict means "no grammar-form citation missing", not "no receipt citation missing".
  Recommend: extend the grammar (expand `{a,b}` and `*` against the commit tree), or pair the round-90 gate
  with a cheap audit grep for `receipts/` forms outside the grammar.
- **G2: nested receipt paths (`receipts/<sub>/<name>.<ext>`) and seat-dir receipts are invisible.** Older
  rounds used `receipts/v2/…`, `receipts/a4/…`, `w1/<Seat>/receipts/…` heavily; recent rounds (86–89) are
  flat with `-rNN` names, so impact on the round-90 gate is low, but the docstring's "every receipt path"
  overstates.
- **G3: suffixless bare names depend on the round fallback.** Pre-round-72 receipts mostly lack `-rNN`
  (`census-after.txt`, `PINS.txt`, `live-geometry-host.txt`, …). In rev mode the round comes from the
  subject prefix `round-N`; a records commit whose subject doesn't start `round-N` (`mado r86: …`,
  `considerthese: …`) with no `--round` resolves such names only to `quality/receipts/` → false MISSING.
  Worktree mode takes `--round` explicitly (the counter passes it; the L1 must too).
- Resolution rules otherwise verified correct: full-path cites must exist as written; bare-name suffix wins
  over `--round` (W11/K01); quality/ fallback present (W5/K02); presence tries candidates in order and
  accepts either location.

## 3. Worktree mode for the L1's round-90 records gate (paths passed to jj-lane.sh)

Verified live: the lane is jj-colocated (`.jj` present) and git HEAD is **detached**
(`git rev-parse --symbolic-full-name HEAD` → bare `HEAD`); current untracked set includes
`.ufo/waves/round-90/`, `corpus/lessons/round-90.md`, both counters.

- **Detached HEAD: safe.** The check never reads HEAD — `--base` is explicit; only
  `diff <base>` / `ls-files --others` / `cat-file <base>:p` are used. W4/W9 cover base-tree and untracked
  presence.
- **`snapshot.auto-track="none()"` (jj-lane.sh contract): handled.** New files are not in the git index, so
  `git diff <base>` cannot see them; the check's `ls-files --others --exclude-standard` scan is what catches
  the new lesson (`corpus/lessons/round-90.md` is untracked right now and would be scanned whole). W9 kills K12 on
  exactly this path.
- **`.ufo` committability:** jj-lane.sh header line 30 says "`.ufo` … never committable", but
  `repo_path_allowed` (jj-lane.sh:506-518) blocks only `.ufo`, `.ufo/state`, `.ufo/state/*`,
  `.ufo/watchdog.log` — `.ufo/waves/round-90/receipts/**` passes, so the receipts CAN be carried by the same
  helper commit that the worktree gate precedes. Header comment overstates; the check's W1/W2 semantics
  match the helper's actual behavior.
- **W1 (carry-set mismatch) — the one real worktree finding.** `present()` accepts a receipt that merely
  exists on disk under a commit-path **directory**. jj-lane.sh's actual carry-set is narrower: named files
  are tracked with `--include-ignored` (ignored named files DO land — consistent), but a named **directory**
  is tracked "like `git add <dir>`, so ignored content stays out" (jj-lane.sh:678), and named files >10 MiB
  are refused without `--allow-large` (post-commit warning at :724-727 covers named files only). So a
  receipt that matches a .gitignore pattern or exceeds the size cap, living inside a named receipts
  directory, is accepted by the gate and silently dropped by the helper — the exact class C2 closes, through
  a side door. Latent only: lane `.gitignore` is `.ufo/interactive-sessions/`, `.ufo/state/`,
  `__pycache__/` (none match receipt paths today). Cheap hardening: require `git check-ignore -q` false for
  on-disk acceptance (or document the limit in the docstring).
- **W2 (commit-path canonicalization):** `--commit-path` values are used raw; an absolute path would make
  `os.path.join(top, p)` check the absolute file but the citation-vs-commit-path prefix match would never
  fire → false MISSING. jj-lane.sh canonicalizes named paths with `realpath -m --relative-to=.`; the check
  should do the same (or the L1 must pass repo-relative paths).
- **W3 (gate scope):** the diff half is not filtered by `--commit-path` — any modified/untracked record file
  anywhere in the worktree is gated even if the records commit will not carry it. Conservative; for the L1's
  clean-tree pre-commit run this is the intended reading, but an unrelated dirty lesson in the worktree can
  false-fail the gate. Observation, not a defect for the declared use.

## 4. Counter review (quality/counters/c2-r90-receipt-presence.py)

- DRAFT run (`--draft-check` on the candidate, exit 3 as specified):
  `DRAFT_TARGET_MET expectations=15 met=15 defects_detected=2/2 mutants=13 killed=13 base_check=absent
  base_defects_detected=0/2 always_ok_met=7/15 always_missing_met=0/15
  check_sha256=300e5029…` — byte-for-byte the declaration's concrete after-state (15 = 4 revisions + 11 fixtures).
- All 13 mutant `find` strings occur exactly once in the candidate (no SETUP_ERROR), each killed by a
  distinct-named expectation; controls fail as designed. Fixture build asserts
  `git rev-parse --show-toplevel` == fixture dir before the single fixture commit, fixture-only identity
  (`fixture@invalid`), all scratch under `--scratch-root`. Lane access is `git show`/`cat-file`/`diff` only.
  Host-guard compliant.
- **Defect (cosmetic, frozen bytes): the counter docstring says "the ten worktree fixtures" while the frozen
  set carries 11 (W1–W11)** — the declaration correctly says 11 and its after-state sums to 15. The
  docstring is inside the frozen counter; if exact docstring fidelity matters at freeze, the L1 should
  either fix the word before freezing or note the erratum. The predicate itself counts the set, so the
  measurement is unaffected.

## Verdict for the L1

The C2 candidate is sound on its declared surface: rev mode reproduces both frozen routed defects exactly,
finds a third, un-routed instance of the same class (01be4234 — recommend routing/errata decision), and the
DRAFT counter reproduces the declaration's after-state with all mutants killed. Before the records-commit
gate is relied on: (1) decide the grammar position on globs/braces (G1 — the round-90 records commit will
likely cite brace forms, which the gate will not see); (2) optionally harden worktree present() with a
check-ignore guard (W1) and realpath the commit paths (W2); (3) fix or footnote the counter docstring's
"ten". Line numbers, resolutions and presence claims verified against tree bytes; no verification gap found
in the swept window beyond the grammar forms themselves.

Residual risks: non-grammar citation forms silently invisible (G1/G2); subject-prefix round fallback for
suffixless bare names (G3); the 01be4234 detection is DRAFT evidence only until the L1 routes it.
