# YAGNI pass — C1 and C2 instrument designs (mado round 51, w1)

Seat `SimplifierLedger`. Contract reviewed: the two frozen sentences in
`.ufo/waves/round-51/claims.md` (§C1 `PRED-C1-r51`, §C2 `PRED-C2-r51`), the routed defect
list in `corpus/lessons/round-50-verifier-spotcheck.md` §6, and the drafts that landed while
this pass ran. Nothing here edits a tracked file: every object named below is a draft in a
seat directory or a measurement of one.

Drafts reviewed (digests bound at 2026-10-27T07:06-03:00; the executors were still editing —
the C2 counter moved twice during this pass (`1d3984f9` → `abf41d4b`) and its line numbers moved
with it, so the line references below are advisory and function names are the anchor):

| draft | bytes | lines | sha256 (12) |
|---|---|---|---|
| `w1/ExecLedgerGate/check-tool-ledger.py` | 31,406 | 782 | `6756bdb8dbbe` |
| `w1/ExecLedgerCounter/c1-r51-ledger.py` | 18,179 | 440 | `11fc2ca77047` |
| `w1/ExecCounterC2/c2-r51-dispatch-entry.py` | 22,572 | 615 | `abf41d4b84f8` |
| `w1/ExecLedgerPopulation/tool-ledger.md` | 21,096 | 115 | `c0a89805f4e5` |

What I measured (not asserted) before recommending anything:

- C1 counter at the round base: `C1_R51: verdict=TARGET_MISSED ledger=absent population=79
  rev=6ca8c559…`, exit 1, 0.9 s. `population=79` reproduces an independent count
  (`tools/` 17 + `quality/*.py` 18 + `quality/counters/*.py` 44).
- Checker selftest: `LEDGER_SELFTEST: 42/42 passed`, exit 0, 0.8 s.
- Both C1 instruments on the draft ledger, inside a scratch clone committed at a synthetic rev:
  `population=81 ledger_rows=79 uncovered=2 dangling=0 bad_pointer=0 empty_desc=0` — identical
  from both, and **zero bad pointers across 79 rows**, so the frozen pointer clause is
  satisfiable by the ledger as drafted. The two uncovered rows are the two new C1 scripts; at
  freeze the ledger needs **three** new rows (both C1 scripts + `c2-r51-dispatch-entry.py`).
- C2 counter at the base: `clauses=abcd clauses_met=0 admitted=0/1 verdict=TARGET_MISSED`,
  exit 1 — the frozen base behaviour, plus a **leaked scratch dir** (see C2-D1).
- A 119-line reference sketch (`SimplifierLedger/ref-minimal-c1.py`) reproducing all five frozen
  C1 controls, the duplicate case and the green case from a three-file fixture (receipt matrix in
  "Preserved contract"). It is a *lower bound on the accounting*, **not** a drop-in replacement —
  two of its missing pieces are load-bearing on the real ledger, and measurement says so (see
  "Withdrawn deletions").

Design target for this pass: delete surface the frozen sentences do not need. Every deletion
below is judged against "does a frozen clause or a frozen control stop holding?" — not against
"is it nice to have". Where a deletion *would* weaken a frozen clause, I say so and keep it.

---

## C1-a — `quality/counters/c1-r51-ledger.py` (440 lines)

Frozen obligations: population `P` at `--rev`; each population file exactly once with non-empty
description and a pointer naming an existing repo file containing the basename; final line
`C1_R51: population=<P> ledger_rows=<P> uncovered=0 dangling=0 bad_pointer=0 empty_desc=0
selftest=ok verdict=TARGET_MET rev=<rev>`; base → `verdict=TARGET_MISSED ledger=absent` exit 1.

### DELETE

1. **`checker_ledger()` and the whole checker-output protocol — L297–L343, plus `LEDGER_LINE`
   (L68), `FIELD` (L69), `RATIO_PASSED` (L70), `SELFTEST_FAIL`/`SELFTEST_OK` (L71–72), and the
   `checker=` / six-field-agreement suffix on the final line (L421–422). ~140 lines.**
   Reasons, in order of weight:
   - *It is a second parser for one grammar.* Measured divergence on a duplicate row: the counter
     prints `dangling=0 dup=1`, the checker prints `dangling=1` for the same bytes. The frozen
     field `dangling` therefore means two things in two instruments that are supposed to agree.
   - *It makes the verdict hostage to a sibling file.* A checker disagreement flips a
     counter-green ledger to `verdict=TARGET_MISSED checker=failed`, which the frozen sentence
     does not authorise.
   - *No frozen clause names `checker=`; the frozen line has six numbers and two tokens.*
   Keep exactly one subprocess call — `checker --selftest` — because the frozen line carries
   `selftest=ok`, and collapse its four output regexes to one: `(\d+)/(\d+) passed` with
   `passed == total`. Delete the with-work/bare fallback probing in `checker_selftest()`
   (L273–L296): the checker's CLI is written this round and known; probing for a shape that
   cannot occur is speculative generality. Tradeoff stated under "Tradeoffs".
2. **`dup` accounting — `describe()`'s duplicate branch, the `dup` key, and ` dup=%d` (L420).
   ~8 lines.** Redundant: a duplicate row makes `ledger_rows != population`, which already
   misses. Proven in the sketch: duplicate fixture → `ledger_rows=4 population=3` → MISS with
   `dangling=0 dup` never needed.
3. **`PLACEHOLDER` (L75) and `EMPHASIS` stripping of the *path* cell (L77).** "Non-empty
   description" is the frozen words; a 13-item `-`/`tbd`/`none` blocklist is a strengthening the
   frozen controls do not cover and that can reject a legal ledger. Keep `desc.strip()`.
4. **`population()`'s `__pycache__`/`.pyc`/`.pyo` exclusions and the `not rest.startswith(".")`
   guard (L135).** Git does not track bytecode; the guard is a rule for a tree that cannot
   exist. `tools/` keeps any extension (measured: `tools/mado-verify.sh` is in the population).
5. **`--checker` (L356) and `normalise_checker()` (L344).** A knob for a path the artifact list
   fixes.
6. **`make_clone()`'s fetch fallback and HEAD/toplevel asserts (L105–L127, ~12 lines).** Keep
   the bare `clone --shared --no-checkout` + `checkout --detach` (it is what makes the checker
   read rev bytes instead of lane-worktree bytes — a real mutant class, round-51
   `RevLedgerPred` attack 5). The retry/verification scaffolding around it is belt over braces.
7. **`sandbox_env()`'s `XDG_CACHE_HOME`/`XDG_CONFIG_HOME`/`XDG_DATA_HOME`/`XDG_STATE_HOME`
   (L246–L272, 4 entries).** Only `HOME`/`TMPDIR`/`PATH`/`LC_ALL` matter for a checker that
   writes nothing outside `--work`.
8. **`--repo` default `"."` (L353) → `required=True`.** The frozen command always passes it; a
   default is a silent widening of the invocation.

### KEEP (judged, not skipped)

- Object-addressed reads (`git -C <repo> show <rev>:<path>`); no worktree read anywhere.
- The scratch clone, because it is what denies a worktree-reading checker the lane's worktree.
- `LINE_SUFFIX` (`:NN`/`:NN-MM` strip on pointer tokens). **Measured load-bearing:** the drafted
  ledger writes pointers as `PROVINCE.md:114`; without the strip, 79/79 rows become
  `bad_pointer` (my sketch's exact failure on the real ledger).
- `resolve_work()`'s create/validate and the `TMPDIR` default (scratch rule 4).
- Exit 1 for an absent ledger with `ledger=absent` — not exit 2 (frozen base clause).
- `git_env()`'s `GIT_*` scrub (house convention; stops an ambient `GIT_DIR` making `--repo` a lie).

Net: ~175 of 440 lines are not required by the frozen sentence or a frozen control.

---

## C1-b — `quality/check-tool-ledger.py` (782 lines)

Frozen obligations: none directly — the sentence pins the *counter*, and claims.md asks this file
for a ledger check and a hermetic `--selftest`. Its behaviour is therefore free to be minimal,
but whatever it does must not contradict the counter's six numbers (it does today; see C1-a.1).

### DELETE

1. **`PLACEHOLDERS` (L79–L80) and `description_empty()`'s "must carry a letter or digit" rule
   (L203).** Same reasoning as C1-a.3: beyond "non-empty". Freeze one definition —
   `not cell.strip()` — and use it in both instruments. Measured: control (c) as specified by
   `w1/CritLedgerControls/controls-c1.md` is an *empty* cell, so the placeholder table is doing
   no control work.
2. **The scratch-refusal policy: `REFUSED_WORK_PREFIXES` (L69), `home_roots()` (L391), and
   selftest arm **O** (L704–L730, ~30 lines).** The operator scratch rule is honoured by
   *accepting* `TMPDIR`/`--work`; *refusing* `/tmp`, `/var/tmp`, `/dev/shm` and the caller's home
   is a policy feature the tasking already enforces on the caller. Keep arm **P**
   (`TMPDIR` honoured), which is the actual rule.
3. **Usage-error battery **N** (L660–L700, 5 subprocess runs).** Predicate fixes exit 0/1 only;
   the counter drives this checker with a fixed flag set. Beyond that, one defence is enough:
   unresolvable rev → exit 2 (keep).
4. **`HEADER_CELLS` (L75) — five accepted header spellings.** The ledger has one header; the
   separator-row rule already skips it.
5. **`SELFTEST_CHECKS = 42` and its inventory comparison (L67, L381–L383).** The suite already
   prints `n/n passed`; freezing the count adds an edit to every future selftest change and buys
   only "someone deleted a case", which the reviewer sees in the diff. Keep the ratio, delete the
   constant.
6. **`--verbose` (and `Suite.verbose` threading, ~10 lines).** A failing assertion already prints
   its detail; no frozen clause reads a verbose transcript.
7. **`pointer_tokens()`'s bare-path fallback, `PATH_TOKEN`, the `#`-split and the
   `rstrip(".,;:")` (L213–L232, ~12 lines).** The ledger's own header documents one grammar
   (backticked repo paths). Two grammars is how a mutant hides: the fallback exists only to guess
   at hand-written cells. Freeze one.
8. **`norm_path()`'s absolute/`..` rejection (L193–L202).** Redundant with the membership test
   that follows: a token not in the rev tree is already `pointer-missing`. (Keep `LINE_SUFFIX` —
   measured load-bearing, see C1-a.)
9. **`clean()`'s `**` stripping and `SAFE`/`safe()` (L81, L324).** Cosmetic normalisation of
   cells and of the checker's own detail text. One cell grammar, one output.

### KEEP

- **`unfenced()`.** **Measured load-bearing and therefore NOT deleted**, contrary to my first
  instinct: the drafted ledger carries a fenced row-grammar example whose row starts with
  `` | `<path>` ``. A naive row scan counts **80** rows against a population of 79; the fence-aware
  parser counts 79. Deleting `unfenced()` would make the real ledger self-invalidate. Its selftest
  arm **J** stays with it.
- **Malformed-row → `dangling` mapping (L251–L253).** Also load-bearing: a two-cell row would
  otherwise vanish silently and *under*-count, which is precisely the omission the C1 claim exists
  to catch. Keep (with arm **H**).
- Population globs exactly as the sentence states them (any extension under `tools/`, direct
  children of `quality/` and `quality/counters/`); arm **L** stays.
- **`P > 0` requirement** (arm **M**): an empty population must not satisfy "every file has a row".
- Rev-addressed reads + arm **K2** (same repo absent one commit earlier). Delete arm **K**
  (a worktree-garbage variant of the same property) if a second one is wanted gone; it is 10 lines
  and duplicates K2's evidence.
- Exit 2 for setup/usage, exit 1 for every MISS.

Net: ~90–110 of 782 lines are beyond both the sentence and the controls, and ~55 of those are
test arms for features that go away with them.

---

## C2 — `quality/counters/c2-r51-dispatch-entry.py` (615 lines)

Frozen obligations: (a) entry exists + indexed; (b) ≥2 rows S364–S379 `mined`, opened
2026-10-27, each bound to a pin named in the entry's pin manifest whose cited line contains **the
row's quote** verbatim (≤25 words); (c) max word-8-gram overlap vs base `corpus/knowledge/*.md`
and every `.ufo/waves/round-*/candidate/**` file ≤30% per file; (d) ≥3 distinct `held:` citations
naming `corpus/knowledge/<file>:<line>` at base whose line carries every pinned key token; final
line `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=<rev>`; base →
`admitted=0/1` exit 1.

### DELETE

1. **The `c2-r51-probe.json` write (L576), `import json` (L45), `scratch_dir()` (L518) and
   the whole `--work`/mkdtemp path.** The predicate's command sets `TMPDIR` and passes no
   `--work`; the final line and the per-clause lines already carry everything the probe records.
   **Measured defect this deletion also fixes:** the base run left `c2-r51-6wvysd66/` behind —
   the counter creates a mkdtemp and never removes it, so every invocation leaks a directory.
   Keep `--work`/`TMPDIR` *accepted* (scratch rule 4) and write nothing.
2. **"the row's quote" read from the wrong place — `quote_candidates()` and the candidate zoo
   `QASSIGN_RE`/`SQUOTE_RE`/`BACKTICK_RE`/`SHA_RE`/`LOC_SKIP` (L76–L84).**
   This is the largest divergence in either instrument, not a style point:
   - The sentence binds **the registry row's** quote; the draft binds a quote found on the
     *entry's* `source:` line. An entry line can therefore supply a self-chosen string that
     happens to appear in the pin, while the S364+ row carries no quotation at all.
   - The candidate order accepts **backticked identifiers as quotations**. Measured at both C2
     digests: `quote_candidates("source: S364 - … `xkb_state_key_get_one_sym`(Pin:369)")` →
     `['xkb_state_key_get_one_sym']`. One identifier satisfies "≤25 words, verbatim at the pin",
     which is exactly what the round-50 falsification taught us to stop allowing.
   - The `quote:` branch is a second grammar for the same field, and at digest `1d3984f9` it
     **raised** on its own documented input (`quote: “a smart quoted span”` → `ValueError: too
     many values to unpack (expected 2)`); at `abf41d4b` it returns
     `['a smart quoted span']`. A branch that shipped broken is a branch that nothing ran, which
     is the argument for one grammar rather than two: `DQUOTE_RE` alone.
   Fix by deleting, not by patching: read one double-quoted span from the SOURCES row
   (house precedent, `corpus/SOURCES.md` S105/S110 style) with a single regex. Measured caveat for
   the freeze: only 35 of 300 rows carry such a span and **all twelve round-50 rows carry none**,
   so this is a *writing requirement* on rows S364+ and must be in the freeze, not just the code.
3. **`MIN_BODY_SHINGLES = 300` (L69) and its branch (L403).** An invented floor on the entry's own
   body that no clause states and that can reject a legal entry. Delete.
4. **`pin_name()`/`resolve_pin()`'s case-fold and stem tiers (L239–L255, ~10 lines).** One tier —
   exact manifest pin name — plus a frozen locator grammar. Measured: for a path-shaped token the
   exact tier never fires (basename `KeybindManager.cpp` ≠ pin `Hyprland-KeybindManager.cpp`), so
   the tiers only rescue misspellings; that is a writing problem, not a counter feature.
5. **`KEYS_RE` / the `keys=TOK,…` grammar (L76, L437–L452).** Two grammars for "pinned key
   token": `keys=` and the backticked identifier fallback. Freeze one (the backticked identifiers
   are already the entry's idiom). Delete the other branch.
6. **`IDENT_RE` (L85) — byte-identical to `TOKEN_RE` (L84).** A literal duplicate.
7. **`clause_b`'s "fetch and retry once" loop (L363–L371).** Dead on arrival: `pin_blobs` starts
   empty and `bind_row()` returns `pin_file_absent` when a pin is not cached, so the *first* call
   can never bind; the retry then loads every pin and re-runs the whole line. Load the pins once
   before the loop (~8 lines) and delete the loop. The same line also mis-diagnoses "not cached"
   as "pin file absent", which is what hides the bug.
8. **The "base already holds ENTRY" setup guard (L604).** The base is a frozen commit where the
   entry is absent by construction; the guard tests a state that cannot occur and turns a
   mis-invocation into exit 2 instead of the frozen `admitted=0/1`.
9. **`manifest()`'s header aliases `("pin", "pinfile", "name")` (L226–L241).** Freeze `pin`.
10. **`git_rc()` (one `cat-file -e` caller).** Fold into the existing `git()` helper.

### KEEP

- `clause_a` index-row check (one table scan for `knowledge/<name>` in a first cell).
- `clause_c`'s baseline construction, and specifically that it reads candidates **at `<rev>`**
  via `ls_files(rev, WAVES)` and base knowledge at `BASE`; the two are different revisions on
  purpose and the predicate only names a revision for the knowledge side.
- `clause_d`'s dedup of repeated `file:line` citations (round-51 `MutC2Counter` mutant 10).
- `unfenced()`/`tables()`/`cells_of()` on the entry (the entry is prose + tables; the same
  measured reason as C1-b).
- The frozen constants (`BASE`, `ROW_MIN/ROW_MAX`, `OPENED`, `MIN_ROWS`, `MIN_HELD`,
  `MAX_QUOTE_WORDS`, `NGRAM`, `MAX_OVERLAP`): each is a word of the sentence, not a knob. No
  flags to change them — none exist, keep it that way.

Net: ~90 of 614 lines, and one measured crash path, one measured weakening, and one measured
directory leak go away.

---

## Cross-instrument deletions

1. **One parser authority for the ledger.** Today: 782-line checker + 440-line counter, two
   row grammars, two `dangling` meanings (measured, C1-a.1). Options, pick one and freeze it:
   - **(i) counter = authority**, checker = library + `--selftest` only, counter runs
     `--selftest` and nothing else (recommended: matches the sentence, which only constrains the
     counter, and keeps the frozen line's six numbers in one place);
   - (ii) checker = authority, counter prints its line — then the counter has no independent
     measurement, which the claim explicitly wants ("the counter's own measurement").
   Freeze the choice in the registration; today's runtime cross-check is neither (i) nor (ii) and
   is the thing to delete.
2. **No `-v2` this round.** Six of the 44 counters in the population at base are v1/v2(/v3) pairs
   (`c1-r40-live`, `c1-r41-globals`, `c1-r44-geometry-states`, `c1-r45-monitors`,
   `c1-r46-devices`, `c1-r48-terminal-cache`). Those are historical provenance and stay; the
   *habit* costs two rows, two digests and a second review surface. Edit in place before the
   freeze, and do not ship `c1-r51-ledger-v2.py` / `c2-r51-dispatch-entry-v2.py`.
3. **Three-column ledger, no extra columns.** The drafted grammar is
   `| <path> | <description> | <pointer> |` and both parsers require exactly three cells. The
   `considerthese/2026-10-26.md` proposal 2 additions that a sibling seat already found unscored
   (last live run, per-tool verdict) would be a fourth and fifth cell that the sentence never
   scores and that `len(cells) != 3 → dangling` would reject. Do not add them; record the gap in
   the lesson instead.
4. **Three new rows at freeze.** `quality/check-tool-ledger.py`,
   `quality/counters/c1-r51-ledger.py`, `quality/counters/c2-r51-dispatch-entry.py` join the
   population the moment they land. Measured consequence: the drafted ledger at base covers 79,
   the tip population is 81 without the C2 counter — freeze-time population is **82**.

---

## Preserved contract (what the deletions must not break, measured)

| Check | Command (drafts as reviewed) | Measured |
|---|---|---|
| C1 base clause | counter `--rev 6ca8c559…` | `ledger=absent`, `verdict=TARGET_MISSED`, exit 1, 0.9 s |
| C1 real ledger | checker + counter at a synthetic rev holding the drafted ledger | both: `population=81 ledger_rows=79 uncovered=2 dangling=0 bad_pointer=0 empty_desc=0`; pointer binding holds for 79/79 rows |
| C1 selftest | checker `--selftest` | `42/42 passed`, exit 0, 0.8 s |
| C1 five controls (sketch, 119 lines) | omit / bad pointer / empty desc / dangling / base-absent | MISS with `uncovered=1` / `bad_pointer=1` / `empty_desc=1` / `dangling=1` / `ledger=absent`, all exit 1; green fixture exit 0 |
| C1 duplicate | sketch + both drafts | sketch and drafts MISS via `ledger_rows != population`; the drafts disagree on *which* counter moves (`dup=1` vs `dangling=1`) — the reason for cross-instrument item 1 |
| C2 base clause | counter at base | `clauses_met=0 admitted=0/1 verdict=TARGET_MISSED`, exit 1; plus one leaked mkdtemp |
| Novelty cost | naive 8-gram pass over base knowledge (66 files, 1,071,092 B) + candidates (3 files, 133,110 B) | 0.10 s total, 4,864 shingles in the round-50 entry, worst overlap 81.0% vs `round-49/candidate/hyprland-bind-key-match-r49.md` — the falsification reproduces, and there is no reason for caching, persistence or parallelism in clause (c) |

## Withdrawn deletions (measurement changed the verdict)

- **`unfenced()` / fence tracking** — kept. The real ledger carries a fenced grammar example;
  naive counting gives 80 rows against 79 (measured).
- **`LINE_SUFFIX` (`:NN` on pointer tokens)** — kept. The real ledger annotates line numbers;
  without the strip, 79/79 pointers go bad (measured).
- **Malformed-row → dangling** — kept; it is what stops a row from vanishing.

A YAGNI pass that had deleted those three on first read would have broken the artifact it was
meant to shrink. The lower bound that survives measurement is ~130 lines of accounting
(the sketch) plus those three features — against 1,222 lines of draft.

## Tradeoffs

- **Deleting the runtime cross-check (C1-a.1) trades corroboration for a single meaning.** The
  corroboration it buys is weak — on the positive path the lane worktree equals the rev, so the
  two parsers can only disagree where they already do (duplicates), and a parroting checker was
  already shown unfalsifiable in round 50. If L1 wants it, take it as a *freeze-time receipt*
  (run both, diff, commit the diff) rather than a runtime gate, so a sibling's parse quirk cannot
  turn a counter-green ledger red.
- **`selftest=ok` honesty is unfalsifiable in every design here.** Every deletion above shrinks
  the surface w2 can mutate; none of them makes `selftest=ok` prove anything. Say that in the
  freeze rather than paying for arms that look like proof.
- **The ledger's durability is a writing problem.** 79 pointer bonds hold today; the two rows
  added at freeze must be written to the same grammar (backticked path, `:NN` annotation) or both
  instruments will (correctly) call them bad.

## Freeze wording this pass cannot settle (for L1, not for a seat)

Each of these changes observable output, so it must be frozen before controls are recorded:

1. **The exact base-absent line.** claims.md fixes the tokens `verdict=TARGET_MISSED
   ledger=absent`; the counter prints `C1_R51: verdict=… ledger=absent population=79 rev=…` and
   the checker prints `LEDGER: population=4 verdict=… ledger=absent rev=…`. Freeze one byte
   string, and say whether the checker's is allowed to differ.
2. **"Non-empty description"** = `not cell.strip()`, or the stricter alnum/placeholder rule. The
   two drafts currently disagree (C1-a.3 / C1-b.1).
3. **"The row's quote"** = the first double-quoted span of the SOURCES row, ≤25 words, verbatim
   at the row's first anchor line in the pin named by the manifest row. The draft reads the
   entry's line instead (C2.2); the new rows must carry the span (35/300 precedent).
4. **The locator token** = exactly a manifest pin name (measured: upstream paths do not resolve).
5. **Duplicate rows** count as `dangling` (checker) or as `ledger_rows > population` only
   (counter). Pick one; the frozen line has no `dup` field.
6. **The candidate baseline is read at `<rev>`**, while the knowledge baseline is read at `BASE`.
