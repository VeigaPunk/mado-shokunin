# ScoutRollingLog — mado r37 w1, scout seat

Question: does `hyprctl rollinglog` (a third channel, after the session log file and the unit journal) agree with the null-channel claim? The claim is that with `debug:disable_logs` = 1, core-logger lines, including `Socket2 fd N overflowed event queue, removing`, never reach any log channel.

**Verdict: AGREES (PASS).** The rolling log holds 0 core-logger lines and 26 aquamarine lines, and a 4-second follow added 0 lines. The source shows the rolling buffer, the follow feed and the file are all fed downstream of the `m_logsEnabled` return. So a zero overflow-marker count in rollinglog cannot show "never overflowed" either.

**Additional finding:** the on-disk `hyprland.log` is not current. It lags the in-memory rolling buffer by 2732 bytes of unflushed stream output (details in item 4).

Privacy: counts, digests and prefix histograms only. No raw log text is quoted.

## Host facts (commands run 2026-10-25 ~12:13Z)

```
$ hyprctl version | head -n 3
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
$ hyprctl getoption debug:disable_logs
int: 1
set: false
$ pacman -Q hyprutils aquamarine hyprland     # read-only query, no transaction
hyprutils 0.14.2-1
aquamarine 0.15.1-1
hyprland 0.56.2-4
```

- Hyprland PID 1619 was started Fri Oct 23 22:14:09 2026.
- Session log: `/run/user/1000/hypr/efb5…_1792804449_426444678/hyprland.log`, 27331 lines (`wc -l`), size 4259033 bytes, mtime `2026-10-25 04:24:03 -0300` (07:24Z). At observation time, about 12:14Z, the file had not been written for about 4 h 50 min.

## Item 1 — `hyprctl rollinglog` histogram: PASS (0 core / 26 aquamarine)

```
$ hyprctl rollinglog > rl.txt; echo rc=$?
rc=0
rollinglog_lines=26 bytes=4042 sha256=1a0fac91db5fb415
$ sed -E 's/^([A-Z]+( from [a-z]+)? \]).*/\1/' rl.txt | sort | uniq -c
     26 DEBUG from aquamarine ]
core(no from) rl: 0  aq rl: 26
overflow marker rl: 0
```

- 26 lines: 0 are core lines (`^[A-Z]+ \]`, with no `from`), and 26 are aquamarine.
- The rolling log contains 4041 bytes of content. This fits hyprutils' `ROLLING_LOG_SIZE = 4096` cap, which trims at a newline boundary (`hyprutils v0.14.2 src/cli/Logger.cpp:156-162`).

## Item 2 — session log last 200 lines: PASS (same shape)

```
$ tail -n 200 $XDG_RUNTIME_DIR/hypr/*/hyprland.log | sed -E 's/^([A-Z]+( from [a-z]+)? \]).*/\1/' | sort | uniq -c
    200 DEBUG from aquamarine ]
core(no from) tail200: 0  aq tail200: 200
core(no from) fullLog: 21  last core line no: 21
overflow marker rl: 0 fullLog: 0
```

- The tail matches the rolling log: 0 core lines and only aquamarine lines.
- Across the whole file there are 21 core lines, and the last one is line 21. This agrees with the brief ("21 core lines all precede line 22") and with S213 (`S213.receipt.txt:13-14,31`).

## Item 3 — bounded follow (`-f` for 4 s, under the 5 s cap): PASS (0 new lines)

```
$ timeout 4 hyprctl rollinglog -f > follow.txt; echo rc=$? lines=$(wc -l < follow.txt)
follow rc=124 lines=27
     26 DEBUG from aquamarine ]
      1 [hyprctl] reading …   (hyprctl's own banner, len 47)
      1 [LOG]                 (hyprctl marker, len 6)
core in follow: 0
follow_aq == rl lines: True
log lines after follow: 27331
```

- The 26 aquamarine lines are byte-identical to the `rollinglog` snapshot. This is [INFERENCE] the initial dump of the rolling buffer when follow starts.
- No new line arrived in 4 s, and the file line count did not change (27331 before and after).

## Item 4 — is the rolling buffer the file tail? FINDING: it is newer than the file

My first comparison was positional and naive. The rolling log did not equal `tail -n 26`; only 1 of 26 lines matched by position. Its 26-line sequence matched the file contiguously only at lines 11293 and 11564. That match is a coincidence: the rolling log has 8 distinct lines and the file has 311, so blocks repeat.

The real alignment came from a byte-suffix test:

```
file ends with newline: False size 4259033
longest rl-prefix that is a file-suffix (bytes): 1309 of 4041
line overlap (file last k == rl first k): 8
```

Reading of this result:
- The first 8 rolling-log lines are the last 8 file lines, and the file stops without the final `\n`.
- The remaining 18 rolling-log lines plus that newline (4041 − 1309 = 2732 bytes) exist in the in-memory rolling buffer but not on disk.

Source explains why:
- `CLoggerImpl::log` writes each line both to the file stream, `m_logOfs << logPrefix << logMsg << "\n"` (hyprutils `Logger.cpp:145-146`, no flush), and to the rolling buffer, `appendToRolling(logPrefix + logMsg)` (`:148-149`), in the same call.
- So the rolling buffer is always the newest data, and the file trails by whatever is still buffered in the stream.
- [INFERENCE] The file ending exactly between a message and its `\n` matches a buffer flush landing between the separate `<<` inserts.

Consequence for C1/C2: a `tail` or count over `hyprland.log` is a lagging, incomplete view, even for the aquamarine lines that do get logged. `hyprctl rollinglog` is fresher, but it only covers the last 4 KiB.

## Item 5 — S214 Logger.cpp:21-22 vs observation: AGREES

S214.bin has sha256 `d04e3a2f…eaf6b868` and 59 lines (Hyprland v0.56.2 `Logger.cpp`):

```
14|void CLogger::log(Hyprutils::CLI::eLogLevel level, const std::string_view& str) {
15|    if (!m_logsEnabled)
16|        return;
...
21|    if (SRollingLogFollow::get().isRunning())
22|        SRollingLogFollow::get().addLog(str);
23|
24|    m_logger.log(level, str);
48|    m_logsEnabled = !*PDISABLELOGS;
53|const std::string& CLogger::rolling() {
54|    return m_logger.rollingLog();
```

Three things are all downstream of the `:15-16` return:
- the follow feed (`:21-22`);
- the rolling buffer, because `rolling()` (`:53-54`) returns hyprutils' `m_rollingLog`, which is filled only inside `CLoggerImpl::log`, reached via `m_logger.log` at `:24`;
- the file write, in the same `CLoggerImpl::log` call.

With `disable_logs` = 1, `:48` makes `m_logsEnabled` false, so every core line is dropped before any of the three channels.

Why aquamarine lines still appear:
- hyprutils `CLoggerConnection::log` (`Logger.cpp:180-189`) checks only `m_logger->m_shouldLogAtAll`, which is `m_fileEnabled || m_stdoutEnabled` (`:152-153`). It then calls `m_impl->log(level, msg, m_name)`, and that call emits the `from <name> ` prefix (`:128-131`).
- That path never reaches Hyprland's `CLogger::log`, so it skips `m_logsEnabled`.
- [INFERENCE] Hyprland hands aquamarine a `CLoggerConnection` on `hu()` (S214:57-58) named `aquamarine`. The `from aquamarine ]` prefix shows this, but no opened receipt shows the call that sets it up.
- [INFERENCE] Connection lines also bypass the follow feed (S214:21-22 is reached only through `CLogger::log`). The 4 s follow cannot confirm this, because no new line arrived during it.

The overflow marker is a core line:
- `S189.bin:175`: `Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", it->fd.get());` (S189 sha256 `eea605df…ee9540d`).
- Every other Socket2 line in S189 also goes through `Log::logger->log`: accept at `:85`, hung up at `:100`, failed writing at `:155`.

On this host, then, the overflow marker cannot appear in the file, the journal, `rollinglog` or `rollinglog -f`. The third channel is as blind as the first two, and the observed 0 core / 0 marker count is exactly what the source predicts.

## Side effect — orphaned follower left by my `rollinglog -f` (added ~12:20Z after SentEventqSafety F9)

`L1Mado37-2.SentEventqSafety` flagged this (reports/SentEventqSafety.md:172-187, F9). I re-checked it read-only (`ss -xap`, `/proc`, no connection):

```
$ ss -xap | rg '\.socket\.sock' | rg -v socket2      (columns trimmed)
u_str LISTEN 0 10 37746     * 0 users:(("Hyprland",pid=1619,fd=70),("Hyprland",pid=1619,fd=69))
u_str ESTAB  0 0  235508591 * 0 users:(("Hyprland",pid=1619,fd=153))
$ pgrep -a hyprctl
no hyprctl client running
```

- **Cause:** almost certainly my `timeout 4 hyprctl rollinglog -f` run at about 12:13Z. Across the w1 reports, mine is the only one recording a `-f` run. ScoutLogger, ScoutPkgRefuse and SentEventqSafety explicitly avoided it.
- **Mechanism:** `timeout` killed the client, so the peer inode is 0. Per F9, the follow thread (`HyprCtl.cpp:2205-2223`) closes only after a failed write. With `disable_logs` = 1, no line reaches `SRollingLogFollow::addLog` (S214:21-22 is behind the `:15-16` return), so the thread never writes and never notices the dead peer.
- **Effect:** one leaked fd (153) and one idle follow thread in PID 1619. [INFERENCE from F9] It does not block the event loop. `SRollingLogFollow::isRunning()` stays true, but nothing ever reaches it.
- **Lifetime:** [INFERENCE] until Hyprland exits, or until core logging is turned back on and the first write to the dead peer fails.
- **Not remedied:** clearing it needs a write verb (re-enabling logs) or a compositor restart. Both are outside this seat's bounds, so this is left to L1/operator.
- **Correction:** the 5 s cap in the brief did not make `-f` harmless on this host. With `disable_logs` = 1, any `rollinglog -f` client that exits leaves a connection like this behind. Future briefs should forbid `-f` here, matching F9's "tool must never use `rollinglog -f`".
- **Attribution limits:** I can't prove from the inode or the `/proc` fd ctime that this is my connection. The fd ctime (12:18:28Z) only records when the `/proc` entry was first looked up. The attribution rests on there being exactly one recorded `-f` run.

## Unresolved gaps

- No opened receipt shows Hyprland's aquamarine logger wiring; that part is inferred from the prefix plus the hyprutils source.
- The `SRollingLogFollow` source (`RollingLogFollow.hpp`) was not opened, so I can't say what follow sends on start beyond what I observed.
- The hyprutils source I fetched is the upstream tag `v0.14.2`, assumed to match the Arch `hyprutils 0.14.2-1` binary. I did not verify that it matches the installed `.so`.

## Receipts / scratch

- hyprutils source: `curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/cli/Logger.cpp` (rc=0, 202 lines). sha256 `91dec1f3efae49bba36816eaf66cfdb822a38ffab52ced60eb18a8a36e1ef834`. Copied to `.ufo/waves/round-37/w1/scratch/ScoutRollingLog/hyprutils-v0.14.2-Logger.cpp`.
- Raw log captures (`rl.txt`, `follow.txt`, `tail*.txt`) were kept only under `/dev/shm/mado37-ScoutRollingLog/` and deleted after counting. Digest kept: rollinglog sha256 prefix `1a0fac91db5fb415`.
- Bounds kept:
  - Hyprland: read verbs only (`version`, `getoption`, `rollinglog`, `rollinglog -f` for 4 s), no write verbs. The `-f` run did leave a lasting connection inside Hyprland; see "Side effect" below.
  - System: no pacman transaction (only `pacman -Q`).
  - Lane: no lane production files touched.
- Tools installed or updated: none.
