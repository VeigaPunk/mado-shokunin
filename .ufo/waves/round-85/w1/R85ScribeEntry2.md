# R85ScribeEntry2 — round-85 C2 knowledge entry

Seat: scribe (leaf member, no subagent dispatch). Wrote exactly one owned file:
`corpus/knowledge/runbook-status-classes-r85.md`, plus this report. No counter, control, fixture,
tool, SKILL.md row, SOURCES.md row, README row or lesson was edited; no git mutation was run; no
tool was installed (pacman stays paused).

## What the entry says

The round-85 C2 knowledge entry opens with the provenance trio (`source:`, `verified-at:`,
`recheck:`) and records the frozen claim's honest state: **the frozen C2 claim did not verify** and
the successor is **not** a green gate (`killed=33`, `verdict=TARGET_MISSED`). It then states:

1. **The three status classes** — `ok` = exit 0, `exact` = one named nonzero code (7), `signal` =
   `128+N` (13 → 141) — with the instrument's own rule lines, the class→row mapping into the frozen
   control file, and the separation argument (a failed producer and a signalled producer are
   different facts; the round-84 blanket `rc != 0` rule collapsed both).
2. **Why a guarded pipeline is the only way the runbook can report a producer's status** — with
   the POSIX default-off rule (S488, §2.9.2 Pipelines: "The exit status of the last (rightmost)
   command specified in the pipeline."), the `pipefail` option POSIX Issue 8 defines in the same
   pinned document, the held S487 row, and the committed no-work control: unguarded, all three
   contained producers report **0**, including the one that exits 7 and the one that dies of
   SIGPIPE; guarded, they report 0, 7 and 141.
3. **The line-anchored pattern rule for the two version rows** — `anchor: "line"`, the
   `line_anchored` matcher (whole line, never a prefix), and the measured limits: the frozen
   `version` value is *already* full-line, so the frozen population cannot discriminate the anchor
   clause from plain `re.search`; the anchor matches on **any** line of the output; and the SKILL
   table's status/outcome **cells** are never read by the counter (only the command cell is bound).
4. **The boundary** — a status class proves propagation, not payload honesty and not tray health;
   `sh` vs `bash` pipefail support is a host property measured separately; the three fixtures are
   contained and no host producer is made to fail.
5. **The measured outcome** and a **limits** section, including the frozen rejection: a numeric 141
   does not prove death by signal 13 (rejected registry row S490), `128+N` is Bash's encoding rather
   than a POSIX guarantee, "the last command's status is the pipeline's status" is the
   `pipefail`-disabled default rather than a law, seven rows bypass the status gate entirely, the
   declaration's §2.9.3 / §3.7.6 locators are off by one section in both documents, and the
   "prefix extension" refusal comes from the pattern's own end anchor rather than from the anchor
   clause.

## Sources used (all already pinned by other seats; I fetched nothing new)

| source | pin | use |
|---|---|---|
| S487 (held) | `.ufo/waves/round-84/fetch/bash-pipelines.html`, sha256 `b5629f04…`, lines 121–124 | pipefail's return status is the rightmost nonzero command |
| S488 (opened this round) | `.ufo/waves/round-85/fetch/S488.bin`, sha256 `0889867a…`, 357,953 B | §2.9.2 Pipelines table rows: default-off = last command's status; the `set` builtin's `pipefail` entry; signal death = "greater than 128" |
| S489 (opened this round) | `.ufo/waves/round-85/fetch/S489-alt-tiswww.bin`, sha256 `b91026ac…`, 1,040,870 B | Bash's `128+N` encoding of a fatal signal; the `exit` builtin's wording for S490 |

The pins file `.ufo/waves/round-85/fetch/source-pins-r85.json` supplies the located quotes and byte
offsets (S488 bytes 133030–133104 and 109001–109128; S489 bytes 239046–239200; S490 bytes
266270–266361). The GNU URL named in the frozen declaration was unreachable for the pin seat
(5 attempts, curl rc 28) and is **not** pinned; S489's registry row points at the maintainer copy,
and the entry says so.

## What I measured myself (all in my scratch, now removed)

- **The three status rules, read out of the frozen instrument** (`quality/counters/c2-r85-status-classes.py:345-358`,
  freeze): `ok` accepts 0 and refuses 3; `exact` code 7 accepts 7 and refuses 141; `signal` 13
  accepts 141; `exact` code 141 also accepts 141 — the numeric ambiguity the entry reports.
- **The guarded/unguarded table**, re-run against the committed fixtures: unguarded 0/0/0, guarded
  0/7/141, matching the committed receipt `receipts/control-c2-r85-unguarded.txt`. The SIGPIPE
  fixture reports 141 only because the reader closes the pipe early (`| head -n 1`); piped to `cat`
  it reports 0 — the reader-shape dependency the entry records.
- **The frozen instrument refuses before running a row.** In a clean scratch archive of the freeze
  (`3905311c`), the counting command exits **2**:
  `MADO_R85_RUNBOOK: ERROR (stage=setup carried case 'version' changes field 'negatives')`. The
  frozen carried-field comparison does not exempt the `status`/`negatives` additions the
  declaration permits. The frozen `SKILL.md`'s heading is still `### Executable runbook rows (round
  84)`, so the counter's row extractor finds **0** rows under the round-85 heading it requires, and
  **33** under the round-84 heading (both measured).
- **The successor at `d7c40e6`**: `cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36
  rows=36/36 mutants=37 killed=33 verdict=TARGET_MISSED`, exit **1**, with the four survivors
  `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`, `samples-skipped` each at
  36/36. Measured from a clean scratch archive; identical to the lane's own receipt
  `receipts/independent-score-r85.txt` Run B2/B3.
- **The anchor clause's reach**: `line_anchored` accepts a match on a *later* line of a multi-line
  output where plain `re.search` refuses the same text; `line_anchored(r"^[0-9]+$","1720")` is
  true and `line_anchored(r"^[0-9]+","1720x")` is false.
- **The frozen pattern is what refuses the text extension**, not the anchor: `re.search` of the
  frozen `version` value refuses `"… trailing"` and `"… EXTRA"`; the round-84 value
  `^Hyprland [0-9]+\.[0-9]+\.[0-9]+ ` accepts both.
- **The SKILL table's status/outcome cells are not read by the counter.** In a scratch clone of the
  successor I replaced the status and outcome cell of all 36 documented rows with junk strings and
  re-ran: `cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36 rows=36/36 …
  verdict=MUTANTS_SKIPPED`, exit 0. The binding is by command cell only.
- **The seven bypass rows**: `special_matches` returns before the class gate, so `refusal` accepts
  rc 3, `is_active` accepts rc 3 with `inactive`, `pid_state` accepts rc 1 with empty stdout and
  `producer_failure` accepts rc 7 — all under a declared class of `ok`.
- **Host facts**: `/bin/sh` → `/usr/bin/bash` (GNU bash 5.3.20) and `set -o pipefail` is accepted
  here; the round-85 fixtures write no file and read no desktop state.

## Gates run against my own file

| gate | command | result |
|---|---|---|
| note index (completeness) | `python3 -I quality/check-index.py --root .` | `MADO_INDEX: root=. indexed=106/106 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0 |
| index-row fidelity | `python3 -I quality/check-index-rows.py --root .` | 14 errors, **all** `row-outside-map` on pre-existing rows (identical count on the pre-existing README, unchanged by my file); **0** errors and **0** warnings mention `knowledge/runbook-status-classes-r85.md` |
| prose locators | `python3 -I quality/check-locators.py --fetch .ufo/waves/round-85/fetch corpus/knowledge/runbook-status-classes-r85.md` | `locators=0 miss=0`, exit 0 |
| source census | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | exit 0; the three `E11 missing used-by corpus/knowledge/runbook-status-classes-r85.md` findings that existed before my file was written are gone; the remaining W04/W01 warnings are the standing pre-known classes |

## Out of scope / not done by this seat

- I did not re-run the two counters' full batteries (the score seat and the reviewers did); the
  numbers I quote are my own clean-archive re-executions of the C2 successor and the frozen
  setup-refusal, and the lane's committed receipt.
- I did not run the outside-lane admit/reject spot-check or any promotion review.
- The README coverage-map row, the SOURCES.md rows (S488/S489/S490 and the S487 used-by append) and
  the lesson were written by other seats; I cited them and edited none of them.
- No tool was installed or upgraded, so no install/update record is owed.

Scratch `/fast/scratch/hyaku/mado-r85/R85ScribeEntry2/` was removed before this report was written.

Self-evaluation (not a round judgment): accuracy 4/5 — every number is either re-measured here or
quoted with a pin; completeness 4/5 — all four assigned elements plus the limits are covered, but
the entry does not re-run the C1 side; clarity 4/5 — the measured-outcome section keeps the frozen
failure and the successor's non-green result in the same voice as the rule; actionability 4/5 —
the recheck command and the four limits are re-runnable, the entry does not itself repair the
survivors; conciseness 3/5 — long for a note, deliberately, because each limit names a line.
Mean 3.8. Highest-impact improvement: bind the entry's `recheck:` line to the successor revision
so a reader does not have to know that the frozen revision refuses at setup.

Report: .ufo/waves/round-85/w1/R85ScribeEntry2.md
