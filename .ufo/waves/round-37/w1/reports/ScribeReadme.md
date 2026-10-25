# ScribeReadme — round 37 wave 1 report (scribe seat)

Seat: `L1Mado37-2.ScribeReadme`. Lane HEAD at start and end: `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`
(the lane was not mutated; `git -C LANE status --porcelain -- corpus quality tools` printed nothing).
Assignment: `.ufo/waves/round-37/w1/prompts/ScribeReadme.md`.

## Behavior

Drafted the round-37 `corpus/README.md` changes into
`.ufo/waves/round-37/w1/scratch/ScribeReadme/readme.md` (80 lines, sha256 `7551110cbd7ef88d…`):

- (a) two `## Coverage map` rows in the existing 3-cell form (Note | Holds | Sources), one each for
  `knowledge/event-delivery-limits-r26.md` and `knowledge/event-queue-observability-r37.md`;
- (b) a `### Round-37 event-socket delivery route` subsection for the end of `## Frontier`, modelled
  on `### Round-35 idle-lock offer route` (README:238-254). It covers what moved (the compositor's
  queue cap, removal and partial-write resume, the Waybar client half, and the null log channel while
  `debug:disable_logs` = 1) and what stays open (no event observed, no socket connected, no client
  stalled, the 64-event cap never exercised, whether any client was ever removed, and Waybar's
  behaviour after removal);
- (c) an optional in-place annotation of the first Frontier bullet (README:98-100), following the
  round-35 precedent at README:102-106.

It also records the landing prerequisites and two conditional sentences: one for the C2 tool, to be
added only if C2's passing run lands, and one for a ScoutWaybarDrop result.

## Gates — exact commands and output

1. **Gate commands as written in the prompt: they refuse to run (FINDING).**
   `cd LANE && python3 -I quality/check-index.py --repo .` gave
   `SETUP_ERROR: --rev or --root is required`, `exit=2`.
   `python3 -I quality/check-index-rows.py --repo .` gave the same line and `exit=2`.
   Both gates require an explicit `--rev` or `--root` (check-index.py `main()`: "No silent default";
   check-index-rows.py `main()`). Instead I ran:
   - `python3 -I quality/check-index.py --rev HEAD --repo .` →
     `MADO_INDEX: rev=HEAD indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0.
   - `python3 -I quality/check-index-rows.py --rev HEAD --repo .` →
     `MADO_INDEX_ROWS: rev=HEAD rows=50 errors=0 warns=3`, exit 0. The three WARNs are pre-existing
     `cited-glob-nomatch` on the getprop, drift and `S###.bin` rows.
   - `python3 -I quality/check-index.py --root .` → `indexed=50/50 … coverage=10.0000/10`, exit 0.
   - `python3 -I quality/check-index-rows.py --root .` → `rows=50 errors=0 warns=0`, exit 0.

2. **What the gates require of a new row (read from source; confirmed by sandbox runs).**
   - `check-index.py`: exactly one line matching `^\| \`knowledge/<name>.md\`` per
     `corpus/knowledge/*.md` blob. That means a column-0 pipe, one space and the backticked name.
     A row whose note is absent is `dangling`; a note without a row is `missing`; two rows for one
     note is `duplicate`. Exit 1 on any of these. It does not check table placement or cell content.
   - `check-index-rows.py`, ERROR-level checks:
     - `row-outside-map`: the row must sit in the contiguous `|` block after the
       `|Note|Holds|Sources|` header. The block ends at the first line that does not start with `|`.
     - `row-cells`: at least 3 cells, with Holds and Sources both non-empty.
     - `cited-s-undefined`: every `\bS\d{3}\b` anywhere in the line must be a `^| S### |` row of
       `SOURCES.md`.
     - `cited-path-missing`: every backticked lane path in the Sources cell (`.ufo/`, `tools/`,
       `quality/`, `corpus/`, `scripts/`, `templates/`) must exist at REV. Bare names such as
       `` `S201.bin` `` are skipped.
     - WARN `holds-no-overlap`: the Holds cell shares no 5-word run (and fewer than 5 distinct words)
       with the note.
   - C1 counter, clause e (`quality/counters/c1-r37-event-ground.py`): a first cell under
     `## Coverage map` containing `knowledge/<basename>`. It reads nothing else from the README.

3. **Sandbox run A: draft rows and subsection only (FAIL as expected; shows the prerequisites).**
   Setup: `git clone -q --no-local LANE /dev/shm/mado37-ScribeReadme/sb`, insert the two rows right
   after the `idle-lock-offered-in-the-bar-r15` row, append the subsection, commit with the
   `sandbox@invalid` identity.
   - check-index `--rev HEAD`: `indexed=50/50 missing=0 dangling=2`, listing
     `dangling: knowledge/event-delivery-limits-r26.md` and
     `dangling: knowledge/event-queue-observability-r37.md`; exit 1.
   - check-index-rows `--rev HEAD`: `rows=52 errors=9 warns=3`. The errors are
     `cited-s-undefined: S212` ×3 (event-delivery row), `S213` ×2 and `S214` ×2 (observability row),
     and `cited-path-missing: \`corpus/lessons/round-37.md\`` ×2; exit 1. There was no
     `row-outside-map`, no `row-cells` and no `cited-path-missing` for any `.ufo/waves/round-37/fetch/*`
     path, because all five fetch files are committed at HEAD (`git cat-file -e` succeeded for each).
   - C1: both entries `a=0 b=0 c=0 d=0 e=1 f=0 g=0 ids=- ok=0`, `admitted=0/2 verdict=TARGET_MISSED`,
     exit 1. The README rows satisfy clause e and nothing else, so rows alone cannot move C1.

4. **Sandbox run B: run A plus stand-in prerequisites (PASS on both gates).**
   Stand-ins: the package entry copied byte-exact; a 3-line placeholder for the observability entry;
   an empty-bodied `corpus/lessons/round-37.md`; placeholder SOURCES rows for S212–S214.
   - check-index `--rev HEAD`: `indexed=52/52 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`,
     exit 0.
   - check-index-rows `--rev HEAD`: `rows=52 errors=0 warns=3` (the same three pre-existing WARNs),
     exit 0. With `--root`: `errors=0 warns=0`, exit 0. No `holds-no-overlap` on either new row, but
     the observability note was a placeholder, so overlap must be re-checked against the real entry.
   - C1: `event-delivery-limits-r26.md a=1 b=1 c=0 d=0 e=1 f=0 g=0 ids=S214 ok=0`. See finding F1.

5. **Mutation: a blank line between the table and the new rows (gate catches it).**
   In a `--root` copy: `ERROR row-outside-map: knowledge/event-delivery-limits-r26.md at line 63` and
   `… event-queue-observability-r37.md at line 64`, while check-index still printed `indexed=52/52`,
   exit 0. Only the row gate enforces placement. The 20 other ERRORs in that partial copy were
   `cited-path-missing` on older rows, because that copy held only `.ufo/waves/round-37/fetch`. They
   are an artefact of the copy, not of the draft; run B on the full clone shows 0.

## Findings

- **F1 (stale id in the package entry).** The package entry's `source:` line cites `S214`, meaning
  Waybar `workspaces.cpp`. In the lane, S214 is `Logger.cpp`, and the renumber map
  (`assimilation/renumber-map.md`, first map row) moves `workspaces.cpp` to **S212**. Run B's C1
  output reports `ids=S214` for a byte-exact copy. The re-grounded entry must rewrite every `S214` to
  `S212` and the merge-note ids "wave-1 S187/S188" to S189/S201. An un-rewritten copy cites the wrong
  document; C1 clause c should still reject it, provided S214's `used-by` does not name the entry.
- **F2 (a package id inside a row).** My first draft's Sources note "the package's staged S214" made
  the row gate resolve S214 for the event-delivery row (run on the partial copy:
  `cited-s-undefined: S214 in row knowledge/event-delivery-limits-r26.md`). The gate scans the whole
  line, so a mention reads as a citation. I removed it; the draft now says "the package's staged
  Waybar `workspaces.cpp` row" and carries a landing note against bare package ids.
- **F3 (the package's "matching" sentence overstates; [INF] from source).** Waybar's listener reads
  lines with `std::array<char, 1024> buffer` and `fgets(buffer.data(), buffer.size(), file)`
  (`S201.bin:115,117`), so one read holds at most 1023 characters. The compositor truncates only the
  data part to 1024, in `std::format("{}>>{}\n", event.event, data.substr(0, 1024))` (`S189.bin:128`),
  so a full line can exceed the buffer. The package sentence "reads at most 1024 bytes per event,
  matching the compositor's own 1024-character truncation" therefore does not hold, and the draft
  rows say only "a 1024-byte `fgets` buffer". What happens to a split long line was not observed.
- **F4 (Waybar after removal stays open; [INF], ScoutWaybarDrop owns it).** On a null `fgets`, the
  listener sleeps 1 ms and `continue`s (`S201.bin:119-122`). There is no reconnect path in lines
  92-139. That is a source reading only; no removal was observed. ScoutWaybarDrop had no report or
  scratch directory when I checked (`ls w1/scratch/ScoutWaybarDrop`: "No such file or directory"), so
  the draft keeps the item open and carries a replacement hook for the scout's result.
- **F5 (the "twelve subscriptions" count holds, with a qualifier).** `workspaces.cpp:804-815` has 12
  unconditional `registerForIPC` calls; `:821` (`windowtitlev2`) and `:827` (`activewindowv2`) are
  config-gated. The draft says "twelve events unconditionally".
- **F6 (receipt facts used, quoted).** From `S213.receipt.txt`:
  `debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}`,
  `core_logger_lines (prefix 'LEVEL ]', no 'from'): 21`, `last_core_logger_line_number: 21`,
  `config_load_line_numbers: 12 18`, `probe_string: … in_log=7 in_unit_journal=0`, and all six
  marker counts 0. From `S214.bin:15-16`: `if (!m_logsEnabled)` / `return;`; from `:48`:
  `m_logsEnabled = !*PDISABLELOGS;`. From `S189.bin`: `:169`
  `const size_t MAX_QUEUED_EVENTS = 64;`, `:174-176` removal at `QUEUESIZE >= MAX_QUEUED_EVENTS`,
  `:139-153` `writeOffset` resume plus the `EAGAIN`/`EWOULDBLOCK` and `EINTR` handling, `:155` the
  "failed writing event" log, `:164-166` shutdown suppression. No journal line or window title is
  reproduced. `"set":false` is reported as read; whether 1 is Hyprland's default was not checked.
- **Digests (sha256sum, computed this run):** S189 `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`, S201
  `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e`, S212
  `1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9`, S213
  `1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58`, S214
  `d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868`. S201 and S212 match the
  renumber map's prefixes; the draft's Sources cells quote 16-hex prefixes of S213 and S214.

## Verdicts

| Item | Verdict |
|---|---|
| (a) two coverage-map rows drafted, 3 cells, existing style | PASS: both gates pass in sandbox run B |
| (b) Round-37 Frontier subsection drafted, round-35 style | PASS (drafted; prose, not gated) |
| Gate commands as written (`--repo .` only) | FINDING: exit 2 SETUP_ERROR; ran with `--rev HEAD` / `--root .` instead |
| Rows land cleanly at current HEAD | FAIL until prerequisites land: notes, SOURCES rows for S212–S214, `corpus/lessons/round-37.md` (run A) |
| Placement sensitivity | PASS: a blank line gives `row-outside-map` (mutation run) |

## Touched surfaces

- Written: `.ufo/waves/round-37/w1/scratch/ScribeReadme/readme.md`; this report; `/dev/shm/mado37-ScribeReadme/`
  (sandbox clone `sb`, two sandbox commits `bc5a4873…` and `d798126c…`, the `rows.txt` and `sub.txt`
  extracts, and the partial `--root` copies, since removed).
- Read only: `corpus/README.md`, `corpus/SOURCES.md`, `quality/check-index.py`,
  `quality/check-index-rows.py`, `quality/counters/c1-r37-event-ground.py`, `registration.md`,
  `assimilation/renumber-map.md`, `fetch/*`, and the package entry under `/home/vgpnk/Projects/shokuknow/merge/mado/`.
- No hyprctl call, no socket connection, no lane or jj mutation. No tool was installed or upgraded.

## Out of scope / not done

- The SOURCES rows, entries and lesson Gate lines belong to other seats. The Holds cells must be
  re-checked against the final entries before landing (semantic accuracy is review-only).
- The C2 tool sentence and the ScoutWaybarDrop replacement are conditional hooks in the draft, not
  claims.

## Artifacts

- Draft: `.ufo/waves/round-37/w1/scratch/ScribeReadme/readme.md`
- Report: `.ufo/waves/round-37/w1/reports/ScribeReadme.md`
