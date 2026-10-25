# ScribeRows — SOURCES.md rows S212–S214 and used-by changes, mado round 37 wave 1

Seat: `L1Mado37-2.ScribeRows` (scribe, leaf). Assignment: `.ufo/waves/round-37/w1/prompts/ScribeRows.md`.
Writes: only `.ufo/waves/round-37/w1/scratch/ScribeRows/` and `/dev/shm/mado37-ScribeRows/`, plus this report.
No tools installed. No hyprctl, no socket, no git or jj write. LANE status for
`corpus quality tools SKILL.md LOG.md SCORECARD.md` after the work: `lane-status-lines=0`.

## Verdict

**PASS.** The three rows and the two used-by changes are drafted in
`scratch/ScribeRows/rows.md` (sha256 `a8df43b66cc6e95d2279dc056a666a6120bee16f17f094d5d27387ccadd67592`).
The scratch mirror validates with **exit 0**. Four findings follow, two of which matter for the
append: the package entry still names the wrong source ids (F-2), and the rows can only land
together with the two entries (F-4).

## Deliverables

| item | path | verdict |
|---|---|---|
| S212, S213, S214 rows (11 columns, status `mined`, opened `2026-10-25`) | `scratch/ScribeRows/rows.md` § New rows | PASS |
| S189 used-by old→new | `rows.md` § In-place used-by changes | PASS |
| S201 used-by old→new | same | PASS |
| validation mirror | `scratch/ScribeRows/validate/corpus/SOURCES.md` (sha256 `0cb0aec932df6ed87b472d9ebb94bfd3154763ef07b1d0a1d535768de68fb661`) | exit 0 |

Old→new used-by values:
- S189: `corpus/knowledge/ipc-contract-r25.md` → `corpus/knowledge/ipc-contract-r25.md, corpus/knowledge/event-delivery-limits-r26.md, corpus/knowledge/event-queue-observability-r37.md`
- S201: `corpus/knowledge/waybar-module-text-route-r25.md` → `corpus/knowledge/waybar-module-text-route-r25.md, corpus/knowledge/event-delivery-limits-r26.md`

Recheck values are bare tokens: S212 `90d`, S213 `on-change` (the same cadence as the own-work
rows S206–S210), S214 `90d`. None of the three rows has a `|` inside a cell; the validator
reported no E01 (13 awk fields per row, confirmed: `S212 13`, `S213 13`, `S214 13`).

## How each anchor was grounded (re-read from the fetched bytes in this seat)

```
$ sha256sum fetch/*
eea605dfe5ce09e1…540d  S189.bin    1e19d92638e7923f…97d7e9  S212.bin
799bf02f6d18ae04…4f9e  S201.bin    1c1b0ce149ecd7b1…ce58    S213.receipt.txt
d04e3a2fe5c73ad8…b868  S214.bin
$ wc -c: S212.bin 41392, S213.receipt.txt 1814, S214.bin 1789
```

- **S212** (`S212.bin`): `803: auto Workspaces::registerIpc() -> void {`, then lines 804–815 hold twelve
  `m_ipc.registerForIPC(...)` calls, workspacev2 through configreloaded. Lines 817–821
  register `windowtitlev2` only `if (windowRewriteConfigUsesTitle() || m_taskbarWithTitle)`.
- **S213** (receipt): `debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}`,
  `core_logger_lines (prefix 'LEVEL ]', no 'from'): 21`, `last_core_logger_line_number: 21`,
  `27280 DEBUG from aquamarine ]`. The log and the unit journal each count `0` for
  "overflowed event queue", "failed writing event" and "Socket2 fd".
- **S214** (`S214.bin`): `15: if (!m_logsEnabled)` / `16: return;` come before `21–24` (the
  rolling-log follower and `m_logger.log`). `37` re-checks the setting on `config.reloaded`,
  `42` reads `CConfigValue<Config::INTEGER>("debug:disable_logs")`, and `48` sets
  `m_logsEnabled = !*PDISABLELOGS;`.

Suggested quotes (25 words or fewer) for the round lesson's `## Gate` (CORPUS.md SOURCES rule 1): S212
`m_ipc.registerForIPC("workspacev2", this);` (workspaces.cpp:804). S213 the
`debug:disable_logs ... "int":1` line (receipt line 27). S214 `m_logsEnabled = !*PDISABLELOGS;`
(Logger.cpp:48).

## Validation — exact command and output

The mirror is a copy of `LANE/corpus`. The three rows were inserted after S211, at mirror lines
214–216 (`registry 9 last_row_before 213 inserted_at 214`), and the two used-by edits applied.
Empty placeholders were created at `corpus/knowledge/event-delivery-limits-r26.md` and
`corpus/knowledge/event-queue-observability-r37.md`.

The first run against a corpus-only mirror **exited 1**. All of its findings were pre-existing
E11s, from older rows whose used-by points outside `corpus/`:
`file E11 S096 missing used-by tools/mado-verify.sh`, `… SKILL.md`,
`S173/S174 … tools/mado-binds.py`, `S178–S182 … tools/mado-wsrules.py`,
`S184 … .ufo/waves/round-29/registration.md`, `S185 … quality/check-index.py`,
`S185 … .ufo/waves/round-30/registration.md`. Each of those seven paths was confirmed present in
LANE (`lane-has <path>` ×7) and mirrored as an empty placeholder. Final run:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/w1/scratch/ScribeRows/validate/corpus/SOURCES.md
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/w1/scratch/ScribeRows/validate/corpus/SOURCES.md
exit=0
```

The seven W04 warnings are pre-existing and identical to the baseline: unmodified
`LANE/corpus/SOURCES.md` gives `exit=0` with the same 7 W04 lines plus `file ok`. The new rows
add no warning. A diff confirms mirror lines 214–216 are byte-identical to the rows in
`rows.md` (`rows-identical`).

## Falsifiers (run on the mirror, and on a mutant copy in `/dev/shm/mado37-ScribeRows/mut`)

| # | mutation | output | exit | verdict |
|---|---|---|---|---|
| F1 | remove placeholder `event-queue-observability-r37.md` | `E11 S189 …`, `E11 S213 …`, `E11 S214 missing used-by corpus/knowledge/event-queue-observability-r37.md` | 1 | killed — the used-by values are checked |
| F2 | `|` inserted into the S214 anchor | `file E01 S214 fields=12` | 1 | killed |
| F3 | S213 recheck set to `on-change when the host log changes` | `file ok …` | 0 | **SURVIVED** (finding F-3) |
| F4 | S213 id changed to S212 | `file E03 S212 duplicate id` | 1 | killed |

After all mutations, the mirror was restored and re-run: `file ok …`, `exit=0`.

## Findings

- **F-1, anchor coverage (the rows are fine; this affects the entries).** The two held rows'
  anchors do not reach the lines the new entries rely on. S189's anchor (SOURCES.md:201) lists
  EventManager.cpp `:14 :21 :35 :126 :128 :129`, but the entries rest on `:155` (write-failure log),
  `:169` (`MAX_QUEUED_EVENTS = 64`) and `:174-175` (overflow, then removal), all confirmed by
  `grep -n` on S189.bin. S201's anchor (SOURCES.md:203) is only `backend.cpp:38`, but the
  1024-byte read the package entry cites is at `:115`
  (`std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes`). Anchors are
  append-only (CORPUS.md SOURCES rule 2: only status, recheck and used-by change in place), so the
  entries must carry these line pointers themselves.
- **F-2, id collision inside the package entry.** The package text
  (`shokuknow/merge/mado/knowledge/corpus/knowledge/event-delivery-limits-r26.md`) has the header
  `source: S214 — …/workspaces.cpp` and cites `S187`/`S188` throughout. In the lane, S214 is
  now Logger.cpp, and workspaces.cpp is S212. The re-grounded entry must rewrite S214→S212,
  S187→S189 and S188→S201, or it will cite the wrong document under a valid id. The package's
  staged row (SOURCES.append.md:18) also listed `host-bar-and-idle-binding-r26.md` in used-by. As
  assigned, S212 lists only `event-delivery-limits-r26.md`, because that is the only admitted entry
  citing it.
- **F-3, validator gap.** `sources-census.sh:582`
  `function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ }` allows spaces, so a prose
  recheck passes E09 (falsifier F3). The "no prose" rule for these rows was enforced by hand, not
  by the gate. The script is outside this lane's write scope; this is reported only.
- **F-4, append ordering.** Neither `event-delivery-limits-r26.md` nor
  `event-queue-observability-r37.md` exists in `LANE/corpus/knowledge/` (`ls | grep -i event`
  returned nothing). If these rows and used-by edits are appended to the live registry before both
  entries land, validation fails with E11, as F1 shows. They must land in the same change.
- **Provenance limit.** I did not re-fetch any URL. The S214 URL path `src/debug/log/Logger.cpp`
  and both commit pins come from `assimilation/renumber-map.md`. What I verified is that the local
  bytes match the recorded sha256 values and sizes (above).

## Scratch artefacts

- `scratch/ScribeRows/rows.md`: the deliverable rows and the old→new table.
- `scratch/ScribeRows/validate/`: the validation mirror (corpus copy, plus 2 entry placeholders and 7 placeholders for older rows' paths outside `corpus/`).
- `scratch/ScribeRows/run0.out`: the first, corpus-only run (exit 1, pre-existing E11s). `outside-corpus-paths.txt` lists the 7 paths. `baseline.out` is the unmodified LANE run.
- `/dev/shm/mado37-ScribeRows/mut/`: the mutant copy used for falsifiers F2–F4.

Out of scope, not done: appending to `LANE/corpus/SOURCES.md`, writing the round lesson's
`## Gate` or old→new log, authoring either knowledge entry, and changing `sources-census.sh`.
