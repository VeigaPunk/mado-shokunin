# ScrQualityR50 — D6: QUALITY criteria for M49-1, M49-3 and round-49 D2 (round 50, w1)

**Verdict: three criteria drafted (100-102) in QUALITY.md's 96-99 format, each with the lesson line it
owes and an instrument shown failing on a red input and passing on a green one.** Lane
`mado-shokunin`, base `8ae47b957034ae21012bbf09173cca2c48be345e`, claims `13631f2`. Nothing tracked was
edited; the L1 integrates. No criterion is scored against round-50 data here (w1 builds and attacks only).

## What the seat produced

- `criteria.md` — criteria **100** (M49-1: a host-consequence claim cites the source line that *sets*
  the state, and the claim's value must agree with the setters that exist), **101** (M49-3: every
  deliverable a seat or report *declares* exists at the cited revision, `test -f` pre-commit /
  `git cat-file -e REV:path` at a revision), **102** (round-49 D2: a round report is committed only
  after every dispatched wave's results file exists with every seat settled). Numbers 100-102 are free
  (`QUALITY_MAX=99`, `receipts/locators.txt`); round 49's unlanded draft used 100-104, so the L1
  renumbers if it lands both.
- `round-50.md` — the **M50-1** row criterion 102 cites, in `corpus/lessons/round-49.md`'s row format.
  `corpus/lessons/round-50.md` does not exist yet (`ROUND50_LESSON=absent`); the row's locator is this
  draft's line 11, and criteria.md says it must be re-anchored when the lesson lands.
- `check100-state-cite.py`, `check101-deliverables.py`, `check102-wave-done.py` — seat prototypes of the
  instruments the criteria name (`quality/check-state-cite.py`, `quality/check-deliverables.py`,
  `quality/check-wave-done.py`). `measure-prose-population.py` measures the population criterion 101
  deliberately excludes. `run-instruments.sh` reproduces every arm quoted below; `verify-locators.py`
  proves all 14 cited locators from their own bytes.

## Evidence (all quoted from `receipts/`, all produced in this seat)

| arm | observed | rc |
|---|---|---|
| 100 red — M49-1 reproduction against the round-49 pins | `STATE_CLAIM … state=m_xkbTranslationState attr=modmask value=nonzero cite=KeybindManager.cpp:369 line=READ_ONLY_CITE setters=0 nonzero_setters=0 verdict=FAIL` → `CHECK100: claims=1 set=0 readonly=1 … verdict=FAIL` | 1 |
| 100 green — three claims citing the setter | `setters=2`/`setters=1` on `IKeyboard.cpp:382`/`:379`, `KeybindManager.cpp:332` → `CHECK100: claims=3 set=3 … verdict=OK` | 0 |
| 100 contradicted — locator repaired, value still wrong | `line=SITE_SET setters=2 nonzero_setters=0 … verdict=FAIL` / `contradicted=1` | 1 |
| 101 red — M49-3 ordering in a fixture repo (report committed, seat dir empty) | `…/ExecRefKeysymA/receipts/parity.txt … status=ABSENT` ×2 → `CHECK101: reports=1 declared=3 exists=1 absent=2 … verdict=FAIL` | 1 |
| 101 green — same report at the commit carrying both receipts | `declared=3 exists=3 absent=0 … verdict=OK` | 0 |
| 101 population — prose tokens at `8a370cd4` | `reports=41 tokens=1354 absent=478` (round 48), `reports=43 tokens=1232 absent=504` (round 49) — why the population is declarations | 0 |
| 101 on this round's own bytes | 53 round-50 w1 report files → `declared=15 exists=15 absent=0 undeclared=49` | 0 |
| 102 red A — fixture, dispatched wave with no results file | `WAVE wave=w1 dispatched=2 results=missing settled=0 unsettled=2`, `REPORT_BEFORE_WAVE_DONE …` → `verdict=FAIL` | 1 |
| 102 red B — the real round-49 closure (report `b0184c43`, lane `8a370cd4`) | `RESULTS_NOT_AT_REV wave=w1 results_rev=8a370cd4 path=.ufo/waves/round-49/w1-results.json`, `REPORT_BEFORE_WAVE_DONE … results_missing=1 unsettled=45` → `verdict=FAIL` | 1 |
| 102 note arm — `output: null` + note, no seat report | `SEAT … name=ExecB status=note_no_report` → `unsettled=1 verdict=FAIL`; with `.ufo/waves/round-X/w1/ExecB.md` present → `settled_with_note … verdict=OK` | 1 / 0 |
| 102 green A — fixture audited at the results commit | `dispatched=2 settled=2 unsettled=0` → `verdict=OK` | 0 |
| 102 green B — the real round-48 closure at `8a370cd4` | `CHECK102: waves=3 dispatched=97 settled=97 results_missing=0 unsettled=0 … verdict=OK` | 0 |
| 102 lane instrument — ExecWaveDone's draft `check-wave-done.py` `check-wave-done.py` at the same two revisions | `WAVE wave=w1 ready=1 results=absent seats=0 dispatched=45 settled=0 verdict=MISSING reason=results-missing` / round 48: `waves=3 settled=3 verdict=OK` | 1 / 0 |

The last row matters: an instrument built by another seat, from committed bytes only, reads the same
round-49 verdict at the same revision. Two independent implementations agree on the red.

## Findings

1. **M49-1's class is mechanically detectable.** The model cited the *read* (`KeybindManager.cpp:369`)
   for a state that has no setter at all in the traced file (`setters=0`); the setter for the same
   attribute on a neighbouring state is at `IKeyboard.cpp:379`/`:382`. Criterion 100 classifies the
   cited line and checks the value against the setters — the two arms fail independently (receipt arms 1
   and 3).
2. **An "any path named in prose" rule is not viable** — 478/1354 and 504/1232 prose tokens in
   round-48/49 seat reports resolve to nothing under the seat-dir-then-lane rule, because reports name
   upstream pins, sibling-lane files and other rounds' artifacts. Criterion 101 therefore bites on two
   declaration grammars (the `Report:` trailer the dispatch mandates, and `## Deliverables` bullets) and
   declares the exclusion instead of hiding it.
3. **This round's reports are almost entirely undeclared under that grammar** — 49 of 53 round-50 w1
   report files carry neither a `Report:` trailer nor a deliverables block (at the moment of the
   receipt; the 15 declarations that do resolve all read `EXISTS`). The round-50 dispatch asks for the trailer in every seat's write-scope block
   (`.ufo/waves/round-50/w1-spec.json`), so criterion 101's `--require-declaration` arm is currently
   red on the round's own population: that is a process finding for the L1, not a scoring result.
   This seat's own report carries both grammars so it reads `EXISTS` in the same sweep.
4. **Round-49 D2 is exactly `results-missing`, and the file that answers it was written after the fact.**
   `.ufo/waves/round-49/w1-results.json` is not in the closure commit
   (`R49_RESULTS_AT_CLOSURE=absent`, `git cat-file -e` fatal), yet an untracked 227 903 B file with that
   name is in the worktree with mtime `2026-10-27 02:58`, written while round 50 w1 was running
   (the dispatcher writes it only at wave finalize, `scripts/hyaku/inline-dispatcher.py:295`). This is
   precisely why criterion 102's audit form reads the file **at the report's revision**: against the
   reconstructed worktree file, round 49 would read `dispatched=45 settled=45 verdict=OK`, i.e. green on
   a run that never happened. Both my prototype and ExecWaveDone's instrument read it red at `8a370cd4`.
5. **D2's substance for the round-50 report** (names the 7 unsettled seats' final state — the L1's item,
   measured here, not adjudicated): at `8a370cd4`, `ExecControlsC1.md`, `ScoutHyprBinds.md`,
   `CritPremiseC1.md`, `CritPremiseC2.md` and `CritRoutedItems.md` exist; **`ExecSessionTriage.md` and
   `SentPrivacy.md` are absent** (`git cat-file -e` → absent for both). So 5 of 7 left bytes, 2 did not.
6. **Write-scope observation for the L1 (not this seat's finding).** At 03:03 the lane worktree carried
   4 modified tracked files, all under `.ufo/waves/round-49/w1/`
   (`ExecControlsC1.md`, `ExecControlsC1/check-c07-isolation.py`, `ExecControlsC1/make-controls-receipt.py`,
   `ExecCounterC1.md`), plus the untracked round-49 results file above. This seat authored none of them
   (its paths are untracked drafts under `.ufo/waves/round-50/w1/ScrQualityR50/` and this report);
   recorded because a wave in flight should not mutate tracked files and because the round-49 bytes are
   the evidence criterion 102's red arm reads.

## Deltas the L1 must decide

- **102's note semantics.** ExecWaveDone's instrument scores `output: null` + non-empty `note` as
  *settled* (63 records in round 39, the kernel-restart lossy case); this seat's prototype scores it
  settled only when the seat's own report exists (`status=settled_with_note` vs `note_no_report`).
  Criterion 102 names the lane instrument as primary and declares the stricter rule as a proposed
  clause: land it in `check-wave-done.py` or drop it from the criterion. Both readings score round 49
  `MISSING`, so the D2 red does not depend on the choice.
- **The `.ready` marker.** `check-wave-done.py` scopes a wave to a committed `<wave>.ready`; this seat's
  prototype scopes to `<wave>-dispatch.json`. Rounds 39-48 agree under both; a round with a dispatch but
  no marker would differ. The criterion's text says "dispatched", so the marker (the launch record) is
  the more faithful signal — adopt it, and read the dispatch only for the seat set, as the lane
  instrument already does.
- **Numbering.** If the L1 lands round-49's unlanded 100-104 drafts (host-write, field-name,
  text-projection, envelope), renumber these three to 105-107.

## Out of scope / not done

- No criterion landed, no tracked file edited, no counter frozen; no round-50 predicate scored.
- No review of ExecWaveDone's instrument beyond the two runs quoted (its own report owns its selftest
  and mutants); no attempt to reconcile 101 with the lane's gate registry (neither criterion is
  registered as a gate — that is the L1's call under criterion 93).
- Instruments are seat prototypes: their fixture populations were authored by the author of the
  criteria, so the criterion-33 discovery attack on them is w2 work, not claimed here.
- No tool installed or upgraded (Python 3.14.8, git 2.56.0, bash 5.3.20 were present); no pacman; no compositor
  or host-state write; every run used `python3 -I`, the lane's `TMPDIR`/work-dir rule, and the
  ExecWaveDone run used `env -i` with `HOME`/`XDG_*` under scratch.

## Deliverables

- `.ufo/waves/round-50/w1/ScrQualityR50.md` (this report)
- `.ufo/waves/round-50/w1/ScrQualityR50/criteria.md`
- `.ufo/waves/round-50/w1/ScrQualityR50/round-50.md`
- `.ufo/waves/round-50/w1/ScrQualityR50/check100-state-cite.py`
- `.ufo/waves/round-50/w1/ScrQualityR50/check101-deliverables.py`
- `.ufo/waves/round-50/w1/ScrQualityR50/check102-wave-done.py`
- `.ufo/waves/round-50/w1/ScrQualityR50/measure-prose-population.py`
- `.ufo/waves/round-50/w1/ScrQualityR50/run-instruments.sh`
- `.ufo/waves/round-50/w1/ScrQualityR50/verify-locators.py`
- `.ufo/waves/round-50/w1/ScrQualityR50/fixtures/claims-red.txt`, `claims-green.txt`,
  `claims-contradicted.txt`, `ExecRefKeysymA.md`, `w1-dispatch.json`, `w1-results-full.json`,
  `w1-results-note.json`, `mado-round-X.md`
- `.ufo/waves/round-50/w1/ScrQualityR50/receipts/criteria-red-green.txt`, `receipts/locators.txt`

Report: .ufo/waves/round-50/w1/ScrQualityR50.md
