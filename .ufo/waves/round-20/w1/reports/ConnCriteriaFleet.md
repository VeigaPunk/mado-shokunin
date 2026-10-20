# ConnCriteriaFleet — fleet already demands the count command; it does not demand a fail-closed isolation harness. Keep criterion 30 only for a real second predicate, and do not treat 155-vs-154 as one.

Axes judged: non-duplication against fleet and existing mado criteria; calibration honesty (a stated integer matches the predicate that produced it); fail-closed isolation; no-harm to C1 and to criterion 21's host pause.

## Verdict on the two planned numbers

**Criterion 30's opening clause is already demanded. Criterion 29 is not.**

Planned text compared: `SCORECARD.md:1263-1273` and the wave draft `.ufo/waves/round-20/w1/drafts/ScribeQuality.md:8-15`. `MISSION.md` (94 lines, read through) names neither obligation. The fleet count rule lives in `CORPUS.md`, not in the mission file.

### Count re-derivation — already a fleet rule, and already mado criteria 6 and 10

`/home/vgpnk/Projects/shokunin/CORPUS.md:34-38`:

> **A count carries its command.** Any number in a corpus entry (rows, files, lines, packages) is written as `<number> — <command> <date>`.

Lessons are corpus entries (`CORPUS.md:15`, layout `lessons/`). That rule already covers `corpus/lessons/round-19.md:123-124`, which states `155 round-19 transcripts` beside a receipt path and a tool sha, and beside no command whose stdout is 155.

Mado already copied the rule into the admission bar:

- Criterion 6, `mado-shokunin/corpus/QUALITY.md:12` — publish each pinned value with a re-derivation command and a named revision.
- Criterion 10, `QUALITY.md:16` — `Report each count as <n> — <command> <date> and rederive it from the named revision instead of transcribing a prior summary.`
- Criterion 22, `QUALITY.md:107` — re-derive each active axis under its recorded counting rule before picking the lowest axis. This is axis selection, not a prose tally. It does not discharge R19-V2 or R19-V5.

`measure.py:83-93` counts a criterion only when `^[0-9]+\. ` and `lessons/` share that line. Criteria 6 and 10 already sit in the 20 lesson-cited lines (`SCORECARD.md:1264`; instrument behaviour recorded in `.ufo/waves/round-20/w1/reports/ScoutMeasureC1.md:40-56`). A new line that only repeats "cite a command and re-derive at the revision" increments `c1` and restates 10. Round 19 refused that shape: `SCORECARD.md:1132` kept the ≥21/29 miss because a restatement of criterion 24 was not numbered 29; `corpus/lessons/round-19-verifier-spotcheck.md:149` (R19-V1) says the same. The round-20 pre-registration (`SCORECARD.md:1272`) only promises that 29 and 30 do not restate 24, 27, or 28. It does not clear 6, 10, or `CORPUS.md:34-38`.

Other lanes restate the same fleet rule. They do not create a second fleet obligation:

| Lane | Where | What it demands |
|---|---|---|
| souji | `souji-shokunin/corpus/QUALITY.md:7-8` | Names the fleet floor as "a count carries its command". |
| kagi | `kagi-shokunin/corpus/QUALITY.md:25` (QA6) | Same sentence; reject "N rows" with no command. |
| kotoba | `kotoba-shokunin/corpus/QUALITY.md:24` (Q13) | `<number> — <command> <date>`, citing `CORPUS.md`. |
| kumitate | `kumitate-shokunin/corpus/QUALITY.md:23-26` (Q3) | Every count carries its command and a dated re-run, or an explicit `recalled` label. |
| chousa | `chousa-shokunin/corpus/QUALITY.md:33-37` (9), `:52-55` (12) | A restated count names its owner and the re-deriving command; a kept score is re-measured or marked frozen. |
| mori | `mori-shokunin/corpus/QUALITY.md:40-41` (20) | A tally cites the counted universe recomputed from delivered artifacts. |
| tsukuroi | `tsukuroi-shokunin/corpus/QUALITY.md:40` (30) | A named count correction includes the exact finite input set. |
| revenger | `revenger-shokunin/corpus/QUALITY.md:20-23` (Q08, Q11) | Each count carries, inside the entry, the command and that command's output. |
| tabi | `tabi-shokunin/corpus/QUALITY.md:143-146` (34) | A prose count carries its command against the named revision. |
| audio | `audio-shokunin/corpus/QUALITY.md:10` (Q2) | Every reported number is re-derivable or marked attestation-only. |
| kaidoku | `kaidoku-shokunin/corpus/QUALITY.md:16` (6) | Explicitly generalizes "a count carries its command" to an Evidence id or reproducing call. |
| kasegi | `kasegi-shokunin/corpus/QUALITY.md:16` (Q3) | Numbers are copied from the source; the motivating row is `451/1506 re-derived`. |
| kama | `kama-shokunin/corpus/QUALITY.md:28` (KQ6) | A frozen host fact cited without re-derivation at its live line is a reject. Narrower object (vendor/spec statements). |

Keyword sweep (`fail-closed`, `abort before`, `count carries`, `re-deriv`, `harness`, `isolation`) found no count-command rule in `kengaku-shokunin`, `lore-shokunin`, `kotodama-shokunin`, or `game-dev-3d-shokunin` `corpus/QUALITY.md`. `tameshi-shokunin` had no such rule; an earlier hit was the substring inside "counterexample".

What the fleet rule does **not** say: when two commands are both legal, the sentence must name which predicate it used. That gap is real, and it is the only part of draft criterion 30 (`ScribeQuality.md:12`) that is not already criterion 10. Mori 20 and tsukuroi 30 are other lanes' versions of it. They are not fleet text, so mado may number its own, provided the numbered line's bite is the predicate and not the command.

### Fail-closed isolation harness — not a fleet rule

No sentence in `CORPUS.md` or `MISSION.md` says an isolation setup failure aborts before a payload.

The nearest fleet sentence is a different obligation. `CORPUS.md:179-183`: **A fix is shown able to fail before it counts** — one red-before where the same command exits non-clean for the named reason, fix as the only delta. That is how any repair, including 29, must be shown. It does not require a mount or `unshare` failure to skip the payload. Draft 29's red arm (the round-19 `inns.sh` shape) is this red-before applied to a new obligation, not a copy of the fleet sentence.

Adjacent lane "fail-closed" rows are other actuators:

- `kama-shokunin/corpus/QUALITY.md:68-72` (KQ17) — malformed offline-replay input fails closed to `unknown`/`invalid_input`. `:80-87` (KQ18) — a duplicate corpus is rejected before any classifier child is spawned. Abort-before-work, measurement runner, not a user-namespace mount.
- `souji-shokunin/corpus/QUALITY.md:32` (Q8) — a hang or a FIFO on staging/digest aborts fail-closed. `:50` (Q21) — credential-namespace paths fail closed before enumeration. Not `unshare`/`mount`.
- `kasegi-shokunin/corpus/QUALITY.md:25-26` — a legacy `recheck:` command stays fail-closed until a lost tree is restored.
- `kaidoku-shokunin/corpus/QUALITY.md:28` (18) — recheck text must match the isolation flags actually exercised, or name the variant as unexercised. Record the flags; do not abort a payload.
- `game-dev-2d-shokunin/corpus/QUALITY.md:22` (Q10) — fixture row isolation (order and shared-project controls).

Mado criterion 21 (`QUALITY.md:82-105`) is the host-pause boundary. A green criterion 29 does not lift it: the same block says a green configuration gate erases no safety trade, and `SCORECARD.md:1235-1237` still forbids a real `hyprctl`. The closure's incident remains `round-19-verifier-spotcheck.md:124`: failed mount setup did not stop `/usr/bin/hyprctl probe`. This seat did not re-execute that harness. `inns.sh` bytes are not in the lane tree (search hit only `SCORECARD.md:1267` and the scribe draft's transcript digests).

## Evidence against calling 155 a second rule

`corpus/lessons/round-19.md:123-124` says `155 round-19 transcripts` and points at `evidence/final/tripwire-seat-scan.txt`. The closure calls that stale (`round-19-verifier-spotcheck.md:125`, R19-V4 at `:152`).

This seat parsed the committed receipt (JSON object on the line that starts with `{`; header is line 1). `files` length **154**, unique paths **154**, every path ends in `.jsonl`. Top-level keys are `counts`, `exit`, `files`, `findings`, `permitted`, `schema`, `unpermitted`. There is no transcripts field and no 155. `counts` matches the prose beside the 155 (`host_mutation` 0, `package_query` 0, `tool_install` 0, `live_probe` 3, `vcs_write` 164, `exit` 1) — those integers match the receipt; the file/transcript integer does not. The universe of the mismatched number is one list of jsonl transcripts, not "receipt entries versus transcript files".

Draft 30 (`ScribeQuality.md:12`) puts `receipt entries versus transcript files` in the same parenthetical as any-line versus first-line and labeled versus distinct. Those other two pairs are real second predicates (`round-19-verifier-spotcheck.md:59` and `:153`; `SCORECARD.md:1167` still says `5/13`; `SCORECARD.md:1225` still says `ten old OM10 assertions`). The 155 pair is not. Treating it as a defensible alternative lets a correction keep 155 by renaming the noun, with no command that prints 155.

## Proposed move

One change to the criterion 30 sentence before it is landed. Leave criterion 29 as drafted in `ScribeQuality.md:8` (new obligation; canary payload; `&&` / `set -e` is not a gate).

On criterion 30's single col-0 numbered line:

- Keep the clause the fleet rule lacks: if two cited commands at the measured revision print different values, the sentence names which command it uses (any-line versus first-line; labeled occurrences versus distinct labels).
- Drop "receipt entries versus transcript files" from that pair list. A stated integer that is not the stdout of its cited command is the existing criterion 10 / `CORPUS.md:34-38` failure, including 155 against `len(files)==154` on this receipt. A second rule is present only when a second command is cited and its stdout is the stated number.
- Cite a lesson path that exists at the landing commit on that same line (`lessons/round-19.md` and `lessons/round-19-verifier-spotcheck.md`). `ScribeQuality.md:8` and `:12` currently cite `lessons/round-20.md#mistakes M2`, which the draft itself marks unverified (`ScribeQuality.md:17`). `measure.py` will count a dangling `lessons/` path (`ScoutMeasureC1.md:106-109`); criterion 8 (`QUALITY.md:14`) will not.

Do not add a third numbered line. Two col-0 `N. ` lines with `lessons/` on each line are what makes 20/28 → 22/30 (`ScoutMeasureC1.md:64-77`). A third line, or a wrapped citation, misses the pre-registered score.

Affected axes: calibration honesty up (155 cannot be laundered; 5/13 and "ten OM10" still need their predicate). Non-duplication held (30's new bite stays the second predicate; 29 stays new). C1 untouched (no tripwire edit). Criterion 21 untouched (29's payload stays a `/tmp` canary; a green 29 is not pause lift).

## Risks

- Landing draft 30's first clause alone, without the predicate clause, repeats R19-V1: a critic can refuse the number as a restatement of criterion 10, and C2 misses 22/30 the way round 19 missed ≥21/29. `measure.py` cannot see that refusal.
- Landing the draft parenthetical as written makes the 155 red dischargeable by a rename. The receipt has one universe.
- A registered-claim checker (`ScribeQuality.md:15`) stays blind to an unregistered count. That limit is the draft's. It is not a fleet waiver of `CORPUS.md:34-38`.
- Criterion 29's own `unshare`/`mount` probe must exit before the canary if setup fails. This seat did not run that probe. Sibling notes in the wave cache are not re-checked here.

## Verification

At the commit that lands the QUALITY text, none of this was run by this seat:

1. `python3 -I .ufo/waves/round-17/measure.py <that-commit>` from a checkout whose `measure.py` parents[3] is that checkout (`measure.py:50`, `ScoutMeasureC1.md:17-19`). Expect `criteria` 30, `lesson_cited` 22, `score` 7.3333, and no extra col-0 `N. ` line.
2. The count checker, once landed: `round-19.md:123-124` stays red until the stated integer equals a cited command at the measured revision (the receipt parse above prints 154, not 155). A sentence that only changes the noun to "transcripts" and cites no such command stays red.
3. `SCORECARD.md:1167` stays red for a bare `5/13`. It is green for `8/13` only with the any-line command, and for `6/13` only with the first-line command, each stated separately.
4. `SCORECARD.md:1225` stays red for "ten". Nine labeled and eight distinct are green only when each is the stdout of the command the sentence names.
5. Criterion 29: red arm writes no host path; setup failure leaves the `/tmp` canary absent. A green run does not edit criterion 21 and does not execute `hyprctl`.

## Limits

- Fleet files read for the obligation search: `CORPUS.md` (rules at `:34-38` and `:179-183`, file not read end to end), `MISSION.md` (full, 94 lines), `PROTOCOL.md` and `AXES.md` (keyword only; no hits). Lane comparison is canonical `corpus/QUALITY.md` by keyword, not a full read of every line, and not worktrees, frozen copies, or `.ufo/waves/**/corpus/QUALITY.md`.
- Did not run `measure.py`, `unshare`, `mount`, `inns.sh`, or the tripwire. The 154 count is a parse of the committed receipt this turn. File sha256 of that receipt was not recomputed. ScribeQuality's script digests were not re-hashed.
- Did not read session transcripts. The `inns.sh` body is cited only as the closure and the SCORECARD describe it.

## Installs

none
