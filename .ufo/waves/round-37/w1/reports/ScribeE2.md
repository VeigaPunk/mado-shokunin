# ScribeE2 — draft of `corpus/knowledge/event-queue-observability-r37.md` (mado round 37, wave 1)

Verdict: **DRAFT DELIVERED**, with five findings for the L1 (F1–F5 below). Nothing outside my
scratch directory and this report was written. No socket was connected, no option set, no
production file edited, no git/jj command run in LANE. Tools installed: none.

Draft: `.ufo/waves/round-37/w1/scratch/ScribeE2/event-queue-observability-r37.md`
(66 lines, sha256 `f88f2ec1d87496e36cd25914bca165281e4769cc65c92368856c72e188cf49cf`).

Axes: coverage (C1 clauses b/f/g that the entry itself controls) and honesty of tagging (no
upgraded claim). Claim separability: the draft cites neither `tools/mado-eventq.py` nor any
`receipts/eventq-*` file. §5 states `ss -xpa` as a documented read-only command (ss(8)).

## Sources read (sha256 recomputed this seat)

| id | file | sha256 |
|---|---|---|
| S189 | `.ufo/waves/round-37/fetch/S189.bin` (192 lines) | `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` |
| S213 | `.ufo/waves/round-37/fetch/S213.receipt.txt` (32 lines) | `1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58` |
| S214 | `.ufo/waves/round-37/fetch/S214.bin` (59 lines) | `d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868` |

The S214 digest matches the renumber map's `d04e3a2f…f6b868`. Command: `sha256sum S189.bin S213.receipt.txt S214.bin`.

## Self-check against the frozen C1 clauses the entry controls (b, f, g)

Command: an inline `python3 -I` check. It reimplements the counter's clause-b regexes, the
clause-f token test and the clause-g quote/`**OBS**` test against the draft and the three
receipts. It is not the counter: clauses a, c, d and e need committed rows, Gate lines and a
README map row that do not exist yet. Output:

```
b ids ['S189', 'S213', 'S214'] verified True recheck True ground True
g S213 words 2 in_receipt True in_body True obs_lines 7
g S214 words 3 in_receipt True in_body True obs_lines 3
g S189 words 7 in_receipt True in_body True obs_lines 3
f debug:disable_logs body True ['S213', 'S214']
f m_logsEnabled body True ['S214']
```

The first run also flagged one elided span on draft line 20 (`'Log::logger->log(Log::ERR, ...)'`
not in S189). I replaced it with verbatim fragments and re-checked them:
`True Log::logger->log(Log::ERR,`, `True Log::logger->log(`, and both DEBUG strings True.

Proposed Gate quotes, each verbatim in its receipt and in the draft body:

- `GATE S213 … quote="debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}"`
  (2 words; carries token `debug:disable_logs`). Alternative without inner `"`:
  `last_core_logger_line_number: 21`.
- `GATE S214 … quote="m_logsEnabled = !*PDISABLELOGS;"` (3 words; carries `m_logsEnabled`).
- `GATE S189 … quote="Socket2 fd {} overflowed event queue, removing"` (7 words).

`GATE_RE` ends in `quote="(.+)"\s*$` (greedy), so the S213 quote with inner `"` should parse.
[INFERENCE — not run through the counter.]

## Claim → line ledger (draft line numbers)

| line | tag | claim | ground |
|---|---|---|---|
| 1–3 | — | `source:` S213, S214, S189 | header |
| 4–6 | — | `verified-at: 2026-10-25`, `recheck: on-change …`, `ground: F1 …` | header |
| 18 | OBS | write-failure marker is a core-logger ERR call | S189:155 |
| 19 | OBS | overflow marker is a core-logger ERR call, before removal | S189:175–176 |
| 20 | OBS | same `Log::logger->log(` call carries the accept/hang-up DEBUG lines | S189:85, :100, :155, :175 |
| 21 | INF | every socket2 line passes through one logger | S189 lines above |
| 25 | OBS | `log()` returns first when `!m_logsEnabled`, before any level test | S214:15–16 (vs :18) |
| 26 | OBS | quote `m_logsEnabled = !*PDISABLELOGS;`, run on every config (re)load | S214:37–38, :42, :48 |
| 27 | OBS | stdout off unless `!disable_logs && enable_stdout_logs` | S214:47 |
| 28 | OBS | live `debug:disable_logs` = 1 (getoption line verbatim) | S213:28 |
| 29 | OBS | live `debug:enable_stdout_logs` = 0 (verbatim) | S213:29 |
| 30 | INF | `"set":false` → the 1 is the build default | S213:28 fields |
| 31 | INF | both markers dropped at any level, ERR included | S214:15–16, :47–48; S213 |
| 35 | OBS | log 27,331 lines / 4,259,033 B; histogram 27,280 / 31 / 21 | S213:6–7, :13–15 |
| 36 | OBS | core lines are 1–21; config loads at 12 and 18 | S213:16–18 |
| 37 | OBS | 0 / 0 / 0 marker counts in the log | S213:9–11 |
| 38 | INF | core logger went silent after the second config load, as S214:48 predicts | S213:17–18; S214:37–38, :48 |
| 39 | OBS | unit journal 717 lines, 0 of each marker | S213:20–24 |
| 40 | OBS | probe 7× in log, 0× in journal (verbatim) | S213:25 |
| 41 | INF | journal is stdout-fed and stdout is off → journal cannot carry log lines | S214:47; S213:29, :25 |
| 45 | INF | r28's "never hit its … cap" reading refused (null channel) | §2–§3; package r28:27–28 |
| 46 | INF | r29's "never overflowed … retained history" reading refused | S214:47; package r29:26–27 |
| 47 | INF | zero cannot separate never-overflowed from not-logged; flip = `disable_logs` 0 | S214:15–16, :48 |
| 48 | INF | r28's instance `_1792772698_564628331` is gone; S213 is another session | S213:5; renumber map |
| 52 | INF | `ss -xpa` flags `-x`/`-p`/`-a`; read-only, no connect | ss(8), iproute2-7.2.0 |
| 53 | INF | table names client holders and Recv-Q; a stalled reader's Recv-Q grows first | ss(8); S189:137–150 |
| 54 | INF | path on the compositor's rows only; client end matched via peer inode | unix binding semantics (see F3) |
| 55 | INF | table shows kernel buffer, not the 64-event user-space queue | S189:169–180 |
| 56 | INF | removal erases the client; a vanished row cannot tell removal from hang-up | S189:119–124, :176 |
| 60–66 | UNK | 7 unknowns: aquamarine bypass via `hu()` (S214:57–59); `Log::logger` ≡ `CLogger`; `m_logsEnabled` initializer; ss Recv-Q semantics for unix; `CFileDescriptor` close on erase; queue depth via a read verb; actual overflow history | — |

The untagged lane paragraph (draft lines 10–14) is provenance prose in the lane's convention
(cf. `corpus/knowledge/idle-lock-never-asked-r12.md:3-5`), not a factual claim.

## Findings for the L1

**F1 — the prompt's "no ERR-class line" in the unit journal is not in S213 (finding; wording
kept off OBS).** S213 records no level count for the journal (S213:19–26). The draft therefore
states only the probe's 7-to-0 split as OBS. My own count-only read, not a registered S-id:

```
journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat | rg -c <re>
journal_lines=717
journal_count[ERR]=4            # substring hits
journal_re[ERR \]]=0
journal_re[\bERR\b]=0
journal_re[DEBUG \]]=42
journal_re[from aquamarine]=0
journal_sha256=43bf1f07176502bf   # 16-hex prefix
```

So the journal holds 0 logger-format ERR lines and 0 standalone `ERR` words. The 4 substring
hits sit inside other words. It holds 0 aquamarine lines of either level and 42 core-format
`DEBUG ]` lines. The line count matches S213 (717). If the entry should say "no ERR-class
line" as OBS, this count must be added to S213 or a new receipt.
[INFERENCE] 42 = 2×21 suggests two sessions' startup core lines reached stdout before
`recheckCfg()` disabled it (S214:32 enables stdout in `initIS`, :47 disables it). Not verified.

**F2 — the probe line is an aquamarine ERR line (finding; supports the registration).**
Count only: `probe_in_log_total=7`, `probe_in_log_on_ERR_aquamarine_lines=7`. This supports
registration line 92 ("an ERR line present in the log is absent from the journal"), but S213
itself does not state the probe's level.

**F3 — `ss` shape on this host: the path is only on the compositor's side (finding; kept
INF in the draft).** Command: `ss -xa` (no `-p`, no titles), saved to `/dev/shm` and deleted.
Count-only output:

```
rows_with_socket2_path: 3
      2 u_str ESTAB local_is_path=1 peer_is_path=0 peer_field=*
      1 u_str LISTEN local_is_path=1 peer_is_path=0 peer_field=*
estab_server_rows_whose_peer_inode_matches_a_pathless_client_row: 2 of 2
```

A census that greps client rows for `.socket2.sock` finds none. The client end (local `*`)
must be joined through the server row's peer inode. This bears on C2's tool and fixtures. I
have not read them, so whether they handle the join is UNK.

**F4 — the core logger is silent even for live clients (finding; falsifier survived).**
S189:85 logs "Socket2 accepted a new client at FD {}" through the same logger. Two clients are
connected now (F3). The S213 log is unchanged since the receipt (`bytes=4259033`, 27331
lines, `mtime=2026-10-25T04:24:03.444802113`, the same as S213:6–8) and holds 0 of that string:

```
Socket2 accepted a new client	0
Socket2	0
overflowed event queue	0
failed writing event	0
core_ERR=0
```

The instance started at `2026-10-23T22:14:09-03:00` (`date -d @1792804449`). Accepting a
socket2 client after startup without a log line is consistent with `m_logsEnabled` = false.
[INFERENCE: the clients may have connected after line 21. The accept time is not observed.]
This is a stronger check than the marker zeros, because a log line is known to have been due.
It is not in the draft because it is not in a registered receipt.

**F5 — S213's histogram sums to one more than its line count (finding; minor).**
27,280 + 31 + 21 = 27,332, but `lines: 27331` (S213:7, :13–15). The likely cause is an
unterminated last line under `wc -l` [INFERENCE]. The draft avoids derived counts. Its Unknowns
line quotes "27,311 aquamarine lines (S213 histogram)", which is the histogram sum.

## Out of scope / not done

- No C1 counter run: the entry, `SOURCES.md` rows, Gate lines and the README row are not
  committed, so clauses a/c/d/e cannot be evaluated by this seat.
- No `ss -p` output, journal line or window title reproduced; counts and digests only.
- No read of `Logger.hpp`, aquamarine wiring, Hyprutils or kernel sock_diag. Those stay as
  the draft's `## Unknowns`.
