# CritEntryE2 — residual falsify call, round 37 (8 seats)

Seat: `L1Mado37-2.CritEntryE2` (critic, leaf).
Target: `corpus/knowledge/event-queue-observability-r37.md` at the landed data commit
`3f424257a1ea69cd2655770259ba00b423293f4f`.
Sources: `.ufo/waves/round-37/fetch/S213.receipt.txt`, `S214.bin`, `S215.bin`, `S216.bin`,
`S217.bin`, `S189.bin`, `S201.bin`; live host read-only (`hyprctl getoption` read verbs, journal
and session-log counts, `ss -xpa`). No tools installed; no socket connected; no lane file
mutated; no journal/log line reproduced (counts and digests only).

## 0. Target identity — PASS

- Commit `3f424257` exists on `master` ("round-37: data — …"), and the committed corpus file is
  byte-identical to the working copy: `jj file show -r 3f424257… corpus/knowledge/event-queue-observability-r37.md | sha256sum` = `2785795b0d0d5fec0dfd9de18ff60fdbec9e76f52e7139d91427e0e7db6a5198` = `sha256sum corpus/knowledge/event-queue-observability-r37.md`.
- Receipt digests match the lesson's GATE lines (round-37 lesson `:28-36`): S213 `1c1b0ce…`,
  S189 `eea605df…`, S201 `799bf02f…`, S214 `d04e3a2…`, S215 `a76f050…`, S216 `74833ec…`,
  S217 `aeb07ba…` — all reproduced exactly.
- Live host still matches the receipt's instance: `$HYPRLAND_INSTANCE_SIGNATURE` =
  `efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678` (same as S213's log path);
  `hyprctl version` = v0.56.2 at `efb50993…` (same as receipt `hyprland_version`).

## 1. Every OBS line exact? — PASS (with two notes)

| Corpus sentence | Source | Verdict |
|---|---|---|
| §1 `Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", …)` at `:175` | S189.bin:175 (verbatim) | PASS |
| §1 `"Socket2 fd {} failed writing event: {}"` at `:155` | S189.bin:155 (verbatim) | PASS |
| §2 S215 `MS<Bool>("debug:disable_logs", "disable logging to a file", true),` `:629`; `debug:enable_stdout_logs` default off `:632` | S215.bin:629, :632 | PASS |
| §2 S217 gate `if (!m_logsEnabled)` / `return;` `Logger.hpp:22-24`; `bool m_logsEnabled = true;` `:42` | S217.bin:22-24, :42 | PASS |
| §2 S214 `m_logsEnabled = !*PDISABLELOGS;` `:48`; string-overload re-check `:15-16` before rolling feed `:21-22` and write `:24`; stdout gate `:47` | S214.bin:15-16, 21-22, 24, 47-48 | PASS |
| §2 S216 `Log::logger->initCallbacks();` `:298` after first stage `:296`; aquamarine handed raw `Log::logger->hu()` in `CLoggerConnection` (`:304-307`, `setName("aquamarine")` `:306`) | S216.bin:296, 298, 304-307 | PASS |
| §3 S213 option strings `{"option":"debug:disable_logs","int":1,"set":false}` / `enable_stdout_logs` `int 0` | S213 receipt `:28-29`; live `hyprctl getoption` re-run returns identical `int: 1 / set: false` and `int: 0 / set: false` | PASS |
| §3 session log: 27,331 lines; 21 core-logger lines, last at line 21; config loads at 12, 18; 27,280 DEBUG + 31 ERR aquamarine; zero marker matches | S213 receipt `:7-17`; independent recount (below) | PASS |
| §3 journal: 717 lines; zero "overflowed event queue" / "failed writing event" / "Socket2 fd"; probe string 7× in log, 0× in journal | S213 receipt `:20-25`; exact `-o cat` recount = 717; probe recount 7 / 0 | PASS |

Independent recount of the session log (read-only; file unchanged since receipt: mtime
1792913043 = 2026-10-25 04:24:03 -0300, size 4259033):
`records(splitlines)=27332 newlines=27331 ends_with_newline=False`; `core_count=21 first=1 last=21`;
`aq_debug=27280 aq_err=31`; `first_aq_line=22`; `other_count=0` (every record after line 21 is
aquamarine); `markers: overflow=0 write_fail=0 socket2fd=0`; `probe_in_log=7`.

**Note A (presentation, non-error):** "27,331 lines" is the `wc -l` count (newlines); the file
holds 27,332 records because it ends without a newline (recount: `newlines=27331`,
`ends_with_newline=False`). The histogram figures 21+27280+31 = 27,332 therefore agree with
records, not with `wc -l`. "Every later line is from aquamarine" holds under the record reading
(`other_count=0`). The sentence mixes two metrics but is not false.

**Note B (support gap, low):** §3 OBS S213 "holds no ERR-class line" is **not** in S213 — the
receipt counts only the three marker patterns plus the probe string (`S213.receipt.txt:22-25`).
A live recount of the journal (`grep -c -E '^ERR \]|^ERR from|^\[ERR\]'` = 0) confirms the claim
is true, but the cited source does not carry it. Fix: move the count into the receipt or cite the
recount.

## 2. Null-channel INF stated with its true limits? — PASS

- "Zero counts are a null channel, not a measurement" — supported: gate closes at
  `Log::logger->initCallbacks()` (S216:298 → S214:48), markers are formatted calls gated before
  formatting (S217:22-24; S189:155, :175), host flag 1 (S213, live getoption).
- "Open window before line 21 cannot carry a marker" — supported by wave-1 `CritNullChannel` SC2
  (no client accepted before the wl event loop runs; `EventManager.cpp:40` + `main.cpp`/`Compositor.cpp`
  dispatch grep). Exactly cited.
- "File written without a flush; newest lines sit in the rolling buffer; last 18 lines missing
  from disk; rollinglog fed after the same return; 26 lines, all aquamarine; growing file proves
  only aquamarine" — all match wave-1 `ScoutRollingLog` (last 18 lines / ~2660 bytes in memory,
  not on disk; 26 aquamarine lines; hyprutils `Logger.cpp:145-149` no flush; S214:21-22 behind
  the `:15-16` return). Exactly cited.
- Journal side: "never writes to the journal" — supported (S214:47 stdout gate false ⇒ nothing
  reaches the unit journal after the gate closes; probe 7/0).

## 3. §5 (socket-table route; Waybar never reconnects) supported? — PASS

- "The compositor never reads from an event client": S189 contains no `read()` on a client fd —
  the read loop is write-only (`flushClient`, S189:133-161); accept `:73`, write `:137`. PASS.
- "Removal closes the client's connection": `removeClientByFD` (S189:119-124) erases the
  `SClient`, destroying the `CFileDescriptor` (close) after `wl_event_source_remove`. PASS.
- ss semantics (server ends on `.socket2.sock`, peer inodes, holding process, Recv-Q = unread
  payload bytes): wave-1 `ScoutSsSemantics` F2-F9 (kernel `unix_diag_rqlen`, `unix_inq_len`,
  `/proc/<pid>/fd` users). PASS.
- Live reproduction (read-only `ss -xpa`): two ESTAB server rows on
  `.socket2.sock` with peer inodes 181143087 (waybar pid 935660) and 40790 (socat pid 2293),
  LISTEN row with Send-Q 10 (backlog, S189:35), client rows `* 181143087` ↔ `* 181151236` and
  `* 40790` ↔ `* 10029`. The route works as described. PASS.
- Waybar never reconnects: S201.bin:105 (connect once; failure returns), :117-122 (`fgets`
  nullptr → sleep 1 ms → continue; no reconnect/retry/log); wave-1 `ScoutWaybarDrop` Q1 replica
  (`feof=1`, ~950 polls/s). PASS. The inference "ESTAB ⇒ not removed since process start" rests on
  the connect-once code plus the ESTAB state and is properly flagged as inference in wave 1.
- §5 UNK list (disable_logs never 0 earlier; pre-reading removals; kernel send-buffer size): honest
  and appropriate; `wmem_default=212992` (ScoutWaybarDrop) is a default, not the effective
  `SO_SNDBUF` — correctly left UNK.

## 4. Sentences the lane cannot back — findings

**F1 — MEDIUM (factual error): §3 OBS S213 "the compositor's unit journal (717 lines over
four service runs)".**
The receipt contains no run count: `unit_journal_using_config_lines: 4` is a count of "Using
config" lines (`S213.receipt.txt:26`), not of service runs. Live clustering (read-only) shows
exactly **two** service runs: "Creating the" lines cluster at `2026-10-23T13:24:58-03:00`
(13) and `2026-10-23T22:14:09-03:00` (13); "Using config" appears twice within each run's same
second (4 total). Boots with service output: -1 and 0 (boot -2 shows none). So "four service
runs" is false. This also contradicts the lane's own wave-1 `CritNullChannel` SC6 ("spans two
Hyprland starts"). Does not affect the null-channel conclusion (a null is a null over any number
of runs), but the sentence as written misstates the journal's scope.

**F2 — LOW (support gap): §3 OBS S213 "holds no ERR-class line".** Not in S213 (see Note B);
true on live recount. Either the receipt must carry the count or the sentence must cite the
recount.

**F3 — LOW (wording): §1 "the two removal paths".** There are three call sites that remove a
client: overflow (S189:175-176), write-fail (:155, :183 partial), and hangup (:100-103, DEBUG, no
marker). The sentence is about the two ERR markers and is accurate as "the two removal markers",
but "the two removal paths" undersells the hangup path (which also removes, at DEBUG).

**F4 — LOW (citation): §4 "refused (round-37 lesson `## Gate`)".** The refusals live in the
lesson's "### Assimilation" table and M37-2, not under "## Gate" (which is the source-row gate).
The ground line's "refused in the round-37 lesson" (no section) is fine.

## 5. Counterexample / strongest attack

The strongest counterexample to the entry's exact wording is F1: the journal statement "over four
service runs" is wrong (two runs). The strongest attack on the *argument* fails: the null-channel
inference survives every check — markers are gated before formatting (S217:22-24), the gate closes
at initCallbacks (S216:298), no client can exist before the event loop (CritNullChannel SC2), the
file lags (ScoutRollingLog), and the journal gets nothing after the gate (S214:47). No sentence
that carries the conclusion is false.

## 6. Impacted axes

- Coverage (C1): the entry's §3 OBS contains one false scope statement (F1) and one unbacked
  count (F2); both are fixable in the entry without touching the refused-package argument.
- Operability (C2): unaffected (tool reads `ss`, not the journal's run count).

## 7. Smallest safe correction

1. §3 line 47: replace "(717 lines over four service runs)" with "(717 lines over two service
   runs)" — or, safer, remove the run count: "the compositor's unit journal (717 lines) holds
   no ERR-class line …".
2. Move the "no ERR-class line" count into S213 or cite a live recount (F2).
3. Optional: footnote the 27,331 vs 27,332 record/newline distinction (Note A); retitle §1 to
   "the two removal markers" (F3); re-point the §4 lesson citation to the Assimilation table (F4).

## 8. Commands / quoted output (load-bearing)

```
$ hyprctl getoption debug:disable_logs
int: 1
set: false
$ hyprctl getoption debug:enable_stdout_logs
int: 0
set: false
$ jj file show -r 3f424257… corpus/knowledge/event-queue-observability-r37.md | sha256sum
2785795b0d0d5fec0dfd9de18ff60fdbec9e76f52e7139d91427e0e7db6a5198  -
$ journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat | wc -l
717
$ journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat | grep -c -F 'drm: getCurrentCRTC: No CRTC 0'
0
$ journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o short-iso | awk '/Creating the/ {print $1 " " $2}' | sort | uniq -c
     13 2026-10-23T13:24:58-03:00 plazir27
     13 2026-10-23T22:14:09-03:00 plazir27
$ journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o short-iso | awk '/Using config/ {print $1 " " $2}' | sort | uniq -c
      2 2026-10-23T13:24:58-03:00 plazir27
      2 2026-10-23T22:14:09-03:00 plazir27
$ ss -xpa | grep -F .socket2.sock
u_str ESTAB  0 0 <S2> 181151236 * 181143087 users:(("Hyprland",pid=1619,fd=250),("Hyprland",pid=1619,fd=236))
u_str LISTEN 0 10 <S2> 38117     * 0         users:(("Hyprland",pid=1619,fd=11),("Hyprland",pid=1619,fd=10))
u_str ESTAB  0 0 <S2> 10029     * 40790     users:(("Hyprland",pid=1619,fd=147),("Hyprland",pid=1619,fd=145))
$ ss -xpa | grep -E 'waybar|socat' | grep -E 'u_str ESTAB' | head -n 2
u_str ESTAB 0 0 * 181143087 * 181151236 users:(("waybar",pid=935660,fd=21))
u_str ESTAB 0 0 * 40790     * 10029     users:(("socat",pid=2293,fd=5))
```

Session-log recount (python, read-only) — see §1; markers all 0; probe = 7; first aquamarine
line 22; no unclassified record. Tools installed or updated: none.
