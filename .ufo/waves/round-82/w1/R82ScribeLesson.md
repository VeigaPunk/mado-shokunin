# R82ScribeLesson — round-82 lesson draft (scribe, prose only)

Seat: `R82ScribeLesson` (leaf). Deliverable: `corpus/lessons/round-82.md`; evidence for every
number in it; sweep + gate + next round; this report.

## Deliverable

- `corpus/lessons/round-82.md` — **13198 B / 120 lines**, sha256
  `a3e0ab51bb214271b000c9428ce1de9ba7bb929e83c64c567f953a80443e1d6b`, committed at `57789ab6`
  (the committed blob hashes to the same value; worktree clean for this path). This
  seat wrote 12412 B / 112 lines (sha256 `50fef1a4…`); at 10:37:56 the L1 appended a "L1
  correction" bullet in the precision block and the `## Erratum (append-only, round 82)` section
  (E1's re-cut of the C2 instrument and the carried `waybar-pgrep` PID that cannot be edited under
  the carried-unchanged assertion). This seat's sections are unchanged by that edit.
- Sections: header (both claims, freeze `780c30fc`, base `6ea2386d`), `## Mistakes`
  (M82-1 admitted and reproduced; M82-2 source-name substitution; candidate (b) examined and
  explicitly not admitted), `## Sweep for further mistakes` (marker, dead keys C1/C2, mutants),
  `## Gate` (census, S481/S482/S483 rows, precision notes), `## Next round`.
- Provenance note: a draft of this lesson had already been committed by the L1 at `3ec7fb75`
  (before this seat wrote). This seat replaced it with a version whose claims are traceable to
  lane bytes: M82-1 now carries a reproduced experiment, candidate (b) is demoted to
  "not admitted" (its only lane-visible `anchor-absent` lines are the base control), the S481
  locator is stated from the pinned bytes, and the receipt revisions are those the receipts
  actually print.

## Evidence run (commands and outcomes)

| check | command / source | outcome |
|---|---|---|
| frozen instrument hashes (seat start) | `sha256sum` on the five paths named in the dispatch | all match the dispatch prefixes: tool `38007528…` (full `380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59`), C1 counter `1e9f394d…`, C2 counter `1e8eb499…` (later changed by erratum E1, see F4), C1 controls `e404bb3f…`, C2 controls `f64d7d5d…` (later changed by E1) |
| C1 receipt | `.ufo/waves/round-82/receipts/measurement-c1-r82.txt` | `cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 carried=39/39 tool_selftest=133/133 verdict=TARGET_MET rev=780c30fc… tool_sha256=38007528…` (last line) |
| C2 receipt | `.ufo/waves/round-82/receipts/measurement-c2-r82.txt` | `cases=29 executed=29 matched=29 shapes=24/24 anchors=29/29 rows=29/29 control_new=0/3 mutants=25 killed=25 verdict=TARGET_MET rev=89acb06c… tree=bound`; first line `MADO_R82_CONTROLS: sha256=07599b24… cases=29` |
| M82-1 reproduction (scratch only) | imported the frozen C1 counter's `run_cases`/`expected_ok`/`case_files` over `.ufo/waves/round-82/controls/c1-cases-r82.json` (47 cases), four tool copies written to scratch | frozen shape: 47/47; frozen + `alloc-explicit-overridden` patch: 12/47 (killed); reconstructed old call shape (`band_of` reached only when the band axis is 0): 47/47; old shape + patch: **47/47 (survives)** |
| tool selftests on the same copies | `python3 tool-*.py --selftest` | old shape 133/133; old shape + patch 132/133 (fails "the vertical band axis is the width"); frozen + patch errors in the selftest harness (non-zero) |
| counter selftests (read-only) | `python3 -I quality/counters/c1-r82-allocation-band.py --selftest`; same for C2; `TMPDIR` in scratch | `MADO_R82_BARFOOT_SELFTEST: 84/84` rc 0; `MADO_R82_RUNBOOK_SELFTEST: 90/90` rc 0; no transcript for either exists under `receipts/` |
| marker sweep | `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py quality/counters/c*-r82-*.py` | no output, exit 1 |
| dead keys | all case keys of both control sets vs every `case[...]`/`case.get(...)`/loop read in the counters | C1: none dead (9 top keys, 14 `expect` keys all read); C2: `tool` present on 4/29 cases and read by nothing; `samples`/`negatives` `rc`/`out` both read; document `lane`/`round` unread metadata; C1 `layers_raw` branch supported but no case uses it (0/47) |
| census start | `git show 6ea2386d:corpus/SOURCES.md \| grep -c '^\| S'`; `.ufo/waves/round-82/receipts/census-start-r82.txt` | 415 rows; validate exit 0 with one `W04 S477 duplicate url …/tests/desktop/Reserved.cpp across scopes` |
| census tip | `git show 3ec7fb75:corpus/SOURCES.md \| grep -c '^\| S'` | 418 rows (415 + S481 + S482 + S483-rejected), unchanged at `89acb06c` |
| source pin hashes | lane fetch dir + read-only re-fetch into scratch | S481 `87e0b9c8…`, 19326 B (also byte-identical to the host package `wlr-protocols r112.a741f0a-1` file `/usr/share/wlr-protocols/unstable/wlr-layer-shell-unstable-v1.xml`); S482 `19df7f18…`, 1151 B; S483 `f22928e1…`, 6395 B |
| S481 line map | `grep -n` on `.ufo/waves/round-82/fetch/S481.xml` | `set_size` `:122-137` (`</request>` `:137`; zero clause `:128-131`), `configure` `:327-353` (zero clause `:347-348`) |
| S482 line map | `grep -n` on `.ufo/waves/round-82/fetch/S482.xml` | interface `:3`, `RegisterStatusNotifierItem` `:6`, `RegisterStatusNotifierHost` `:10`, `RegisteredStatusNotifierItems` `:17` |

## Findings

- **F1 (low; resolved at `57789ab6`).** At `3ec7fb75`/`d645edb5` the S483 row
  (`corpus/SOURCES.md:435`) cited `.ufo/waves/round-82/fetch/S482.html`, and that file was absent
  (`git ls-tree -r HEAD .ufo/waves/round-82/fetch/` listed three blobs; `find . -name S482.html`
  found none). At 10:33 (mtime) the file appeared in the worktree: 6395 B, sha256 `f22928e1…`,
  listed in the worktree's `fetch/sha256-r82.txt`; commit `57789ab6` then pinned it
  (blob `856d950e…`) and the row's citation is now true.
- **F2 (low; open, partly corrected mid-seat).** `corpus/SOURCES.md:433` (S481) first landed as
  "`set_size` `:122-142`, clause at `:347-348`": the request ends at `</request>` `:137` (overrun
  five lines), and `:347-348` is the **`configure` event's** zero-size sentence (event
  `:327-353`), not `set_size`'s (`:128-129`). A worktree revision appeared at 10:37 (uncommitted,
  `corpus/SOURCES.md` `M`): "`set_size` `:122-138` (zero clause `:128-131`) and the `configure`
  event's zero-size sentence `:347-348`" — the split is now right, but the request still overruns
  `:137` by one line and the quoted sentence ends at `:129`, not `:131`. The row's bytes and hash
  are correct; the claim's substance is unaffected (both clauses delegate a zero size to the
  client). L1's to finish.
- **F3 (low; open).** Dead key: the four C2 refusal cases carry `tool: tools/mado-barfoot.py`, and
  `quality/counters/c2-r82-runbook.py` never reads it (tree binding at `:656-660`, execution from
  `case["argv"]` at `:685-697`). C1's `case_files` supports `layers_raw`, but no case in the 47
  carries it.
- **F4 (state change by the L1, not this seat).** Erratum `89acb06c` ("redact the new C2 fixture
  tokens and pin TMPDIR … sentinel F1/F2") rewrote two instruments the dispatch listed as frozen:
  `quality/counters/c2-r82-runbook.py` (`1e8eb499…` → `a87bceab…`) and
  `.ufo/waves/round-82/controls/c2-runbook-cases-r82.json` (`f64d7d5d…` → `07599b24…`), and the C2
  receipt was re-measured at `89acb06c` (still `29/29`, `25/25`, `TARGET_MET`, `tree=bound`). The
  frozen list in the dispatch and the C2 sha in the claim declaration (`f64d7d5d…`, rev
  `780c30fc`) therefore no longer match the tree; the lesson cites the receipt's actual rev and
  controls sha. Reported for the canonical judge; this seat changed none of it.
- **F5 (low; open).** Repair R4 ("selftest tallies lack receipts") is not visible: no
  `--selftest` transcript for either counter sits under `receipts/`. Both tallies do hold when run
  at the content tip (84/84, 90/90, rc 0 each).
- **F6 (info).** The committed `3ec7fb75` lesson asserted a second mistake — `alloc-axis-lost` and
  `alloc-composition-ignored` reporting `reason=anchor-absent` after the M82-1 refactor, `killed=32`
  — citing "first sandbox runs (not committed)". No lane byte shows that event; the only
  `anchor-absent` lines are `control-c1-r82-at-base.txt:76-81`, where all six `alloc-*` mutants are
  absent because the base tool has no allocation input (`:83`, `rule=held-r81-model(no-allocation-input)`).
  This draft records it as a candidate not admitted. If the L1 holds the sandbox transcript, pin it
  and the row can return.
- **F7 (info).** The declaration's S481 locator (`set_size` `:116-123`) matches nothing in
  `fetch/S481.xml` (`set_size` opens at `:122`). Frozen text; substance unaffected.

- **F8 (state; timestamped, resolved).** The L1's appended "correction" bullet says the `S482.html`
  capture and the `fetch/sha256-r82.txt` line "are committed with this correction". At 10:38 that
  was not yet true (HEAD `89acb06c`, `corpus/SOURCES.md` `M`, `S482.html` `??`,
  `sha256-r82.txt` ` M`); commit `57789ab6` then committed them, and the worktree is clean for
  those paths. The report records both states so "committed" and the tree do not drift.

## Touched surfaces

- `corpus/lessons/round-82.md` — rewritten (uncommitted).
- `.ufo/waves/round-82/w1/R82ScribeLesson.md` — this report.
- Scratch `/fast/scratch/hyaku/mado-r82/R82ScribeLesson/` — fetched read-only copies, four tool
  variants, case-run trees; removed after this report.
- Nothing else. No write to `SOURCES.md`, the knowledge entry, the counters, the tool, the
  declaration, `SKILL.md`, the fetch dir, `.ufo/state/`, `.ufo/watchdog.log`, `/tmp`, the fleet
  root, or a sibling lane. No git/jj mutation; no commit; no message to another seat; no subagent.

## Known limits

- The "old call shape" is reconstructed from the dispatch's description, not from a lane commit
  (sandbox commits `2dad6c01`/`1bb580ad` are never in the lane). The reproduction uses the frozen
  47-case set and the frozen counter's own runner, but its tool copies are scratch artifacts; the
  round's measurement remains `receipts/measurement-c1-r82.txt`.
- The reproduction ran cases only (no `--base-rev`, no tree binding); it shows discrimination, not
  the frozen predicate.
- `Assimilation: none` is the round's §2b record; the shokuknow package was not read (lane bounds).
- No redaction-sensitive capture was taken; the only host read was the installed protocol XML
  (`/usr/share/wlr-protocols/...`, no personal data).

## Tooling

None installed or upgraded (no `pacman`, no `uv`, no `npx`).

STATUS: defect — `corpus/SOURCES.md:433` (S481) still overruns the request (`set_size` `:122-138`
vs `</request>` `:137`) and labels its quote `:128-131` for a sentence ending `:129` (F2; L1's to
finish); F1 resolved at `57789ab6`; F4 recorded (erratum `89acb06c` rewrote the C2 instruments
after the freeze).
