# MutC2Counter — C2 counter mutation sweep (round 48, w2 FALSIFY)

Seat: `MutC2Counter` (leaf, mutation-tester). Lane `mado-shokunin`, base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`, freeze `3e6c848a` (instruments + draft committed).
Attacked: `quality/counters/c2-r48-xkb-entry.py` (`PRED-C2-r48`), sha256
`4a0e6924eada0d12c70b4ce6e681a118896b93532e280ea3c15cc148b794a9f1`, scored on the L1 C2 draft
(`l1-draft/xkb-keymap-compile-r48.md`, `l1-draft/rows-c2.md`, `l1-draft/readme-row.md`) overlaid on a
scratch clone at BASE. Nothing in the lane, the registry, the counters or the fleet repo was written;
there was no Git/JJ mutation in the lane and no commit outside my scratch trees.

Verdict up front: **no falsified tree breaks the frozen predicate.** All nine single-clause defect trees
(V1-V9) are rejected (`admitted=0/1 TARGET_MISSED`, exit 1) and the draft-only tree and the base are scored
exactly as the registration says. All eight required clause mutants admit their own defect, so every clause
in the list below is load-bearing. Three further trees (V10-V12) are admitted: each one sits inside an
allowance that the frozen clause text itself grants, so they are not predicate failures — they are pre-data
tighten-or-declare decisions for L1, listed in §5 with the exact clause wording that lets them through.

## 1. Replay tree and scoring

A full `git clone --shared` + checkout of the lane cannot be made under this seat's 1 MiB/file writer bound
(the lane index is 2 771 712 B). The clone is therefore cone-sparse with `index.sparse=true`
(index 29 594 B), which keeps every blob the counter reads (`git show REV:path`) and every file the defect
trees modify. Recipe and exact commands: `w2/MutC2Counter/commands.md` §1-§2.

| tree | revision | content |
|---|---|---|
| BASE | `579f694b` | lane base, C2 entry absent |
| V0 | `c28505ab` | BASE + draft entry, 11 rows S340-S350 after S339, README index row, 14 fetch pins, receipt, receipt generator |

Real-counter results (`python3 -I quality/counters/c2-r48-xkb-entry.py --repo <tree> --rev HEAD`,
`TMPDIR` inside scratch, host `xkbcli 1.13.2`):

- **BASE** → `PRED-C2-r48: admitted=0/1 verdict=TARGET_MISSED rev=579f694b…`, exit 1.
- **V0 (positive control)** → `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1`,
  `verdict=TARGET_MET rev=c28505abcbc1204871fd82ab27b05cba8c5c0a3d`, exit 0.
  Clause r really replayed: `clause=r replay=ok sha=efd487a39920 neg=(1,1,0) ver=1.13.2`.

So the draft, as it stands, is admitted by the frozen counter on a tree I built from the committed
instruments and draft bytes alone; the L1 did not supply a passing tree to me.

## 2. One defect per clause (V1-V9) — all rejected

Each tree is V0 plus a single textual change, committed (`defect-diffs/V*.stat.txt` holds the commit and
full patch; `commits.txt` the hashes).

| tree | mutation | real-counter diagnostics (abridged) | verdict |
|---|---|---|---|
| V1 `13bf643e` | S340 row pin digest last hex `…4e42a8`→`…4e42a9` | `clause=c id=S340 pin_sha_mismatch=xkbcommon-rules.c`; then `c:0 d:0 e:0` | MISSED |
| V2 `e58d4242` | S341 URL ref `xkbcommon-1.13.2`→`master` | `clause=c id=S341 url_branch_ref:…/master/src/xkbcomp/xkbcomp.c` | MISSED |
| V3 `ce8df8e4` | OBS S342 quoted span `in include paths`→`in include path` (locator kept at `xkbcommon-include.c:355`) | `clause=d quote_not_in_pin line=53` | MISSED |
| V4 `baffa0e6` | step 9 loses its only pin locator (`(xkbcommon-context.c:503)`→`(default)`) | `clause=e step_without_pin_range line=43 uncited=[]` | MISSED |
| V5 `bee57b2b` | receipt `host.keymap` digest `…cf6fce81`→`…cf6fce82` (entry untouched) | `clause=r positive_replay_failed rc=0 sha=efd487a39920` | MISSED |
| V6 `5baba242` | held row S318 prose gets ` (edited)` | `clause=h held_row_moved=S318` | MISSED |
| V7 `bd866689` | README index row `rows S340-S350`→`rows S340-S349` | `clause=g readme_missing_ids=['S350']` | MISSED |
| V8 `08828352` | README index row deleted | `clause=g readme_rows=0` | MISSED |
| V9 `5f05b9bf` | synthetic base `4f79087f` = BASE + `corpus/knowledge/zz-ground-probe.md` containing `compile-keymap`, draft on top, scored with `--base 4f79087f` | `clause=i ground_present_at_base=compile-keymap rc=0` | MISSED |

Notes that matter for how the freeze reads:

- **V1 is not a one-clause hit.** The digest mismatch in clause c aborts before `rowp[fname]` is bound, so
  clause d then reports `pin_not_cited_by_row=xkbcommon-rules.c` for every S340 quote and clause e reports
  `step_without_pin_range` for the steps citing it (`c:0 d:0 e:0`). Clause c's digest gate is therefore the
  single gate for c, d and e on head-row pins; a repair anywhere in c/d/e must keep that cascade in mind.
- **V9 needs a non-frozen base.** Clause i's BASE side is unreachable for the frozen data (BASE is a fixed
  commit whose corpus contains none of the four GROUND terms; `clause=i all_absent_at_base=1 present_at_rev=3/4`
  on V0). V9 is a counter-behaviour probe with `--base <synthetic>`, not a reachable data defect.
  The other direction (fewer than 2 GROUND terms at REV) is not isolatable either: `present` counts any
  corpus occurrence at REV, and the remaining terms live in `SOURCES.md`/`README.md` and in the pinned URL
  tags, so driving `present<2` would also break clause c's tag pinning. Recorded as a falsifiability limit,
  not a missed defect.

## 3. Eight clause mutants — each is load-bearing

One textual mutation per clause on a scratch copy of the counter (never on the lane file); 19 changed lines
total, `mutants/counter-mutant.diff`, scripts kept in `mutants/`.

| mutant | edit | on clean V0 | on its defect |
|---|---|---|---|
| `m-c-digest` | `if False and digest not in digests:` | admitted=1 | V1 admitted=1 |
| `m-c-branch` | branch/ref restriction dropped (refs unchecked) | admitted=1 | V2 admitted=1 |
| `m-d-quote` | `at = [a]` (span never searched in the pin) | admitted=1 | V3 admitted=1 |
| `m-e-locator` | step with no resolvable cited pin counts as cited | admitted=1 | V4 admitted=1 |
| `m-r-digest` | `if rc != 0:` (replay digest not compared) | admitted=1 | V5 admitted=1 |
| `m-h-heldrow` | `if not a:` (held row content change ignored) | admitted=1 | V6 admitted=1 |
| `m-g-readme` | `clause_g` returns True | admitted=1 | V7 and V8 admitted=1 |
| `m-i-ground` | `clause_i` returns True | admitted=1 | V9 admitted=1 |

Every mutant still admits the clean tree, so the mutation removes exactly its own guard and nothing else.
The full 8×12 grid (`matrix.tsv`, 96 runs) shows a one-to-one mapping: each mutant flips **only** its own
defect tree to admitted, and every other column still misses on a different clause. There is no clause whose
removal lets an unrelated defect through, and no defect that any two clauses redundantly catch except the
c→d/e cascade noted above.

## 4. Admitted trees (false-positive controls) — V10-V12

Run with the untouched lane counter. All three are `admitted=1/1 verdict=TARGET_MET`, and all three are
admitted by every one of the eight mutants as well (they are caught by no clause at all).

| tree | change | observed | why the frozen text allows it |
|---|---|---|---|
| V10 `bda05cb0` | entry states keymap `sha256 …cf6fdead`; receipt and live replay say `…cf6fce81` | `clause=f … sha=efd487a39920 probes=3`, `clause=r replay=ok sha=efd487a39920`, admitted | clause f: "the digest (**or its first >= 12 hex**) beside `sha256`" — the entry's digest is compared to 12 hex only |
| V11 `960c70e6` | OBS S342 span falsified (`paths`→`path`) **and** its locator de-adjacented (` at ` → ` — from `) | `clause=d quotes=17` on V11 vs `quotes=18` on V0 (one quote left the net); admitted | clause d sees a quote only when the span is "immediately followed by `, <loc>` / ` at <loc>` / `(<loc>)`"; residual: "a quote with no adjacent locator is out of its reach" |
| V12 `63e6960e` | S340 anchor gains `, nonexistent-pin.c:9999-10000` | `clause=c id=S340 pins=xkbcommon-rules.c digests=1 ranges=11`; admitted | clause c: an anchor token may "resolve to no fetch copy, i.e. an upstream path name the pin is a renamed copy of" |

Assessment, without narrowing anything:

- **V10** is inside the frozen wording, so `TARGET_MET` is the correct verdict for it. The exploitable part is
  that a 52-hex misstatement in the entry survives both f (12-hex prefix) and r (r never reads entry text).
  This is a residual worth writing down if L1 keeps v1; tightening it to full 64-hex equality is a v2 decision.
- **V11** is a declared residual, now demonstrated end to end: one dash between a span and its locator removes
  the span from the check while the locator itself is still range-validated. The registration's Residuals
  sentence predicts this exactly; I confirm it is live in a tree that otherwise passes all ten clauses.
- **V12** is the one I would flag as *under-declared*. The Residuals paragraph binds "URL+digest+name" but does
  not say that an anchor token resolving to no fetch copy is unfalsifiable. Because the counter fetches
  nothing, it cannot tell `rules/rules.in` (a real upstream name whose pin is a renamed copy) from
  `nonexistent-pin.c`; a fabricated locator therefore rides along in the row's provenance cell with no
  diagnostic. Either declare it in Residuals, or bind an unresolvable anchor token to the row's URL path
  (the `wants()` relation already used for URL-vs-pin) so a fabricated name cannot pass.

None of the three contradicts a frozen clause, so none of them is a miss under this wave's rule; the decision
to re-register as v2 (pre-data is the only window) or to declare them belongs to L1.

## 5. What I did not change, and what could still go wrong

- The predicate, counters, fixture set, claims and target were not modified, and no clause was narrowed.
  All eight clause mutants are scratch-only copies; the lane counter's sha256 is unchanged.
- The replay in clause r ran against the host's `/usr/bin/xkbcli 1.13.2`; a host package change moves r, as
  the registration says ("changed package outputs are a miss").
- V0's admission depends on pre-existing corpus/registry content only through clause h (bytes equal at BASE),
  clause i (`present_at_rev=3/4`) and clause g's id coverage; the draft rows and README row are the only
  corpus additions, exactly as `l1-draft/integrate-c2.py` would land them. The Frontier bullet that
  `integrate-c2.py` also inserts is not in V0 and is read by no clause.
- Observed while working (not mine, recorded for the integrator): the lane working tree is dirty —
  `git status --porcelain --untracked-files=no` lists `M SKILL.md`, `M corpus/QUALITY.md`, `M corpus/README.md`,
  `M corpus/SOURCES.md`, `M corpus/knowledge/hyprland-monitor-rule-r45.md`,
  `M corpus/knowledge/xdg-terminal-selection-r47.md`, `M corpus/lessons/round-47.md`,
  `M quality/check-session-material.py`, `M tools/mado-terminal.py`. My replay tree was cloned at the committed
  BASE, so none of this sweep depends on, or asserts anything about, those uncommitted changes.

## 6. Evidence (all under `w2/MutC2Counter/`)

- `real-counter/` — 17 run transcripts: `BASE-real.txt`, `V0-real.txt` … `V12-real.txt`, `mut-<mutant>-<tree>.txt`.
- `mutants/` — the eight mutated counters + `counter-mutant.diff` (the only differences from the lane file).
- `defect-diffs/` — per-tree commit hash, stat and full patch for V1-V12.
- `matrix.tsv` — counter-mutant × defect-tree verdict grid (96 runs); `commits.txt` — tree revisions;
  `commands.md` — exact commands, sparse-clone rationale, scratch accounting.

Scratch `/fast/scratch/hyaku/mado-r48/MutC2Counter` was created explicitly with `ulimit -f 2048` active in
every writer shell, peaked at 100 M / 373 905 B largest file (both inside the 2 GB / 1 MiB bounds; largest
output file 4 889 B), and was deleted after these receipts were copied here. No host, service, package or
PATH state was touched; no `pacman` ran; no install was needed.
