# R68ScribeLesson — round 68 w1 scribe report

Seat: `R68ScribeLesson` (mado lane, round 68, wave 1). Role: lesson scribe, draft only.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base: `510100c81e6cf63fec6be380c2f2f9c670f32cbc`.
Freeze: `e0727cda15621766c35dcf8b70c211b6531aab45` (2026-11-03T22:04:51-03:00).
Lane HEAD at write time: `18d692f346298d6a185b7a38190821245e2133a9` (L1 integration head; the record
landing is later). No production file was edited; the lane's `corpus/lessons/round-68.md` at
`18d692f3` is the L1's integration of this seat's earlier 255-line draft.

## Deliverable

- Draft: `.ufo/waves/round-68/w1/R68ScribeLesson/draft/corpus/lessons/round-68.md`
- sha256 `9b749dece602ebdcdb75bf655835bbdcf386559445f0dabbdfe0979536554738`, 26,755 B, 306 lines.
- Sections: header; Outcome and boundaries; Mistakes (`M68-1`..`M68-5`); Gate (`S437`); Frontier and
  scope; Controls and limits (C1 recipes, C2 cases/population, auxiliary hazard probe, dominance,
  freeze-text conflicts, reviewer findings, integration placeholders).
- The draft is the later, fuller version. It adds, over the 255-line integrated draft: `M68-2`
  (frozen C2 command exits 2) and `M68-3` (C2 denominator not enforced), the R68RevC1/R68RevC2
  findings, the guard-dominance negative control, the S436 used-by old→new correction, and the
  QUALITY 110 id conflict. The L1 must reconcile the integrated bytes with this draft at landing.

## Draft content (what is claimed and bounded)

- C1: `quality/counters/c1-r68-selfmutants.py` (freeze blob `bdea8dc6b4455f45c59896a44f0bd4ede21c26b82c67e0618a05ac069ef50a85`,
  12,769 B) scores three frozen recipes S1-S3 against
  `quality/counters/c1-r68-landing-controls.py` at `REV`; base `510100c8` is 0/3 because the scored
  harness is absent and the same recipes survive the r67 harness (`killed=0/3 applied=3`).
- C2: `quality/counters/c2-r68-reader-guard.py` scores `quality/check-[^/]+\.py` (20 files, 13
  readers) and requires `guarded=13 unguarded=0 controls=11/11`; base is `guarded=1 unguarded=12`.
  Control set sha256 `b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91` (11 cases).
- Not claimed: state truth, universal fault coverage, honest invocation, runtime gate behaviour,
  authenticity, already-rewritten repositories, exhaustive harness mutants, desktop health.

## Commands and observations (this seat; read-only)

| command | rc | observed |
|---|---|---|
| `git log -1 --format='%H %cI %s' e0727cda` | 0 | freeze commit, 2026-11-03T22:04:51-03:00 |
| `git cat-file -e e0727cda:.ufo/waves/round-68/claims-declaration-r68.md` | 0 | declaration present; blob `1f3a2392f9140b6828511c5bc1f433e4417d9c04159ce061dde7fc9b549e5f12`, 9,261 B |
| `sha256sum .ufo/waves/round-68/controls/c2-controls.json`; `git show e0727cda:... \| sha256sum` | 0 | both `b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91` |
| `git show 510100c8:corpus/SOURCES.md \| grep -c '^| *S[0-9]'` | 0 | `373` rows |
| `grep -c '^| *S437 ' corpus/SOURCES.md`; `grep -c 'git-cat-file.adoc' corpus/SOURCES.md` | 1 | `0` matches each (no id/URL collision) |
| `curl -fsSL -o git-cat-file.adoc https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-cat-file.adoc` (scratch) | 0 | 16,099 B, 470 lines, sha256 `6c32dbda8c2106be08bda471592db50b5afaf185de32f2e513e80d802b4a95b2` |
| `git ls-remote https://github.com/git/git 'v2.56.0' 'v2.56.0^{}'` | 0 | tag `2478544319491bbd2a42cc57a83e3d2f4730a280`; peeled `a018953688f1b10bddf91bff8747068f5f4746a4` |
| `git --version` | 0 | `git version 2.56.0` |
| `grep -oF` for S1/S2/S3 in `quality/counters/c2-r67-landing-controls.py` at `510100c8` and `c1-r68-landing-controls.py` at `40d2bef8` | 0 | `1/1/1` each; base harness blob `a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58` (30,697 B); candidate blob `25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527` (36,005 B) |
| `git show e0727cda:quality/counters/c1-r68-selfmutants.py \| sha256sum` | 0 | `bdea8dc6b4455f45c59896a44f0bd4ede21c26b82c67e0618a05ac069ef50a85` (12,769 B) |
| `git show e0727cda:quality/counters/c2-r68-reader-guard.py \| sha256sum` | 0 | `8eb99a63e324fce18eda824d7aefa48d72650ff6abb7c4afa45def9191ce880e` (13,429 B; lacks `--scratch-root`) |
| `git show 2a39e741:...c2-r68-reader-guard.py \| sha256sum` | 0 | `0e853b1b11b3f327bc2c0e6a4aa6ce32a5fc5561d9575b0bf1bc548c7f4dfea8` (14,057 B; accepts the flag) |
| `git show 425d4b2f:...c2-r68-reader-guard.py \| sha256sum` | 0 | `5a6b386545889e3b072740d1d5fa39b3a4c523661d4a788993d48d4607410faa` (15,794 B; `verdict_met` enforces `population=20 readers=13`; `update()`/annotated guards) |
| `git diff 425d4b2f 18d692f3 -- corpus/SOURCES.md` | 0 | S436 used-by old `corpus/lessons/round-67.md, corpus/knowledge/replace-ref-citation-boundaries-r67.md` → new plus `corpus/knowledge/gate-git-read-guards-r68.md`; S437 appended |
| `sha256sum` of the draft | 0 | `9b749dece602ebdcdb75bf655835bbdcf386559445f0dabbdfe0979536554738` |

Sibling receipts read (not re-run by this seat): `R68ExecHazard.md` (frozen C2 command `rc=2`;
hazard probe on `check-axis-scores.py`), `R68RevC1.md` (C1 3/3 at `40d2bef8`; mutants 51/52,
51/52, 50/52; survivors D1/D2c/G/L/I), `R68RevC2.md` (denominator deletion `readers=12 TARGET_MET`
rc 0; fixture 13/13 at `f17140c1`; key-as-value false positive; update/annotated misses;
end-to-end hazard on `check-landed-contract.py`), `R68ConnSiblings.md` (assimilation none; 94/147
staged-row collision; dominance proposal), `R68ScoutSources.md` (row/quote/pin/id/duplicate checks;
12/12 quoted-line audit; recipes 1x each; three row nits), and `R68ScribeKnowledge.md` (row draft
`cbf4cf5e…`).

## Conflicts / findings reported in the draft

1. **S436 used-by drift:** the r68 SOURCES sweep paragraph says "No existing status, recheck,
   used-by or opened cell changed.", but the same commit changes S436's used-by cell (old→new
   above). The row-level change is intentional; the sweep sentence is the drift. Draft records both.
2. **QUALITY 110 id ground:** the criterion's ground names `M68-1`/`M68-2`; in the integrated
   lesson at `18d692f3`, `M68-2` is the M-R kill-rule row, not the command defect QUALITY 110(a)
   describes. The draft renumbers `M68-2` as the command defect (`landing`) and moves the kill rule
   to `M68-4`.
3. **Frozen C2 command:** the counter at `e0727cda` exits 2 on the declared `--scratch-root`
   (`c2-command-erratum-r68.txt`, fixed at `2a39e741`). Instrument-only.
4. **C2 denominator:** the counter at `2a39e741` accepted `readers=12 … TARGET_MET` rc 0; the fix at
   `686d6345` requires `population=20 readers=13` (`c2-denominator-erratum-r68.txt`, red/green,
   selftest 25/25).
5. **C2 dominance:** a guard built then erased by a `GIT_*` purge reads `guarded=yes` but reads
   forged bytes (`aux-dominance-r68.txt`); the census is presence-only, not order-aware.
6. **C2 classifier over-acceptance:** `carries_key` accepts a constant equal to the key anywhere in
   an env-named/`env=` subtree, so `env={"LABEL": "GIT_NO_REPLACE_OBJECTS"}` reads guarded with no
   guard key; disclosed beyond the comment/docstring/unrelated-dict rejects.
7. **Declaration case-number parenthetical:** `claims-declaration-r68.md:114` names "cases 6, 8,
   10, 11" as not-guards; the frozen JSON's sixth case is `module-const-guard` with
   `expect_guard=true`; the non-guard positions are 7 (`comment-only-mention`), 8
   (`docstring-only-mention`), 10 (`unrelated-dict-as-env`) and 11 (`non-reader`). The counter
   scores by name/expectation, so the predicate is unaffected; the parenthetical is a frozen-text
   number-drift.
8. **C1 winner/losers:** the C1 reviewer's survivors D1/D2c (decision+oracle), G (`forged_credit`
   removed), L (`mz_rc is None` credits a kill) and I (no-spawn guard removed) are within the
   declared "not exhaustive" limit, recorded not smoothed. C1 `killed=3/3` is a seat measurement at
   `40d2bef8`; the record landing re-run is `TBD-INTEGRATION`.
9. **Integrated lesson gap:** the lane's `corpus/lessons/round-68.md` at `18d692f3` (255 lines)
   predates findings 3-8 and the used-by correction; the delivered 306-line draft carries them.

## Bounds and hygiene

- No counter, selftest or gate was executed by this seat; the seat-level after lines are cited from
  `R68RevC1`/`R68RevC2` and marked as seat measurements, not the record landing.
- No production edit, commit, stage, stash, checkout, switch, reset or sibling-lane write. Read-only
  git used: `log`, `show`, `cat-file -e`, `ls-remote`, `rev-parse`, `diff`, `status`. `git status`
  was run without `GIT_OPTIONAL_LOCKS=0`; it may refresh the index stat cache (QUALITY 63 hazard) but
  staged/committed nothing and no tracked content was changed by this seat.
- No desktop/compositor/socket/service/session probe; no package-manager transaction or install;
  no credential material.
- Scratch `/fast/scratch/hyaku/mado-r68/R68ScribeLesson/` removed before yield (verified absent).
