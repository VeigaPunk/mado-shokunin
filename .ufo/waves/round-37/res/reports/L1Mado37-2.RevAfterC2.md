# L1Mado37-2.RevAfterC2 — residual falsify review of the landed C2 deliverable (mado r37)

Seat: reviewer, after the landed data commit `3f424257a1ea69cd2655770259ba00b423293f4f`
(round-37 C2: `tools/mado-eventq.py`, `quality/counters/c2-r37-eventq.py`, receipts).
Scope: re-run the frozen counting command; run the tool live read-only and compare
subscriber set and server inodes against `receipts/eventq-live.txt` and `/proc`; feed
five out-of-fixture inputs; check the module docstring against behaviour (exit map,
read-only guarantee). No lane file was edited; no socket was connected; the only
subprocesses run were the registered read verbs (`ss -xpa`, `journalctl`, one-shot
`hyprctl getoption debug:disable_logs -j`). Scratch only under
`/dev/shm/mado37-L1Mado37-2.RevAfterC2/`. No tool installed or upgraded; no pacman.

## 1. Frozen C2 counter re-run — PASS

Command (registered, registration.md:63):

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r37-eventq.py --repo . --rev 3f424257a1ea69cd2655770259ba00b423293f4f
```

Output (verbatim):

```
PRED-C2-r37-v2 case=clean want_rc=0 rc=0 ok=1
PRED-C2-r37-v2 case=overflow-log want_rc=1 rc=1 ok=1
PRED-C2-r37-v2 case=writefail-journal want_rc=1 rc=1 ok=1
PRED-C2-r37-v2 case=not-listening want_rc=2 rc=2 ok=1
PRED-C2-r37-v2 case=missing-client want_rc=1 rc=1 ok=1
PRED-C2-r37-v2 case=lagging want_rc=0 rc=0 ok=1
PRED-C2-r37-v2 case=unparseable want_rc=2 rc=2 ok=1
PRED-C2-r37-v2 case=logs-disabled want_rc=0 rc=0 ok=1
PRED-C2-r37-v2 case=overflow-twice want_rc=1 rc=1 ok=1
PRED-C2-r37-v2 case=decoy want_rc=0 rc=0 ok=1
PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET rev=3f424257a1ea69cd2655770259ba00b423293f4f
```

`echo $?` → `0`. **PASS** against the registered target (registration.md:65).

Blob identity at the rev:
`git show 3f424257…:tools/mado-eventq.py | sha256sum` = `436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24`
= working-tree `tools/mado-eventq.py` = the receipt's `tool_sha256=` line
(`eventq-live.txt:3`). The counter blob
(`6fae177fd5f42d7b28759eb08770bc1af63e8ad29c27f971978336bfde060f7a`) is byte-identical
to the freeze (w1 RevC2Code:38-40). The measured tool is the committed blob.

## 2. Live run vs receipt vs /proc — PASS

Live run (read-only, same command shape as the receipt's):

```
$ python3 -I tools/mado-eventq.py --snapshot-out /dev/shm/mado37-L1Mado37-2.RevAfterC2/live-ss.txt
MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 peer_recv_q=0 server_send_q=0 server_fd=250,236
MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 peer_recv_q=0 server_send_q=0 server_fd=147,145
MADO_EVENTQ_MARKERS: source=log:/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/hyprland.log overflow=0 write_fail=0 fds=-
MADO_EVENTQ_MARKERS: source=journal overflow=0 write_fail=0 fds=-
MADO_EVENTQ: socket2=/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock subscribers=2 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=no verdict=CLEAN
```

exit `0`. The CLIENT lines and the summary are line-identical to the committed receipt
(`eventq-live.txt:5-9`); subscriber set `{waybar 935660/21, socat 2293/5}` unchanged.
`diff receipt.py/eventq-live-ss.txt live-ss.txt` → empty (`diff-exit=0`): the snapshot
reproduces the committed one exactly — same server inodes, same peer inodes.

`/proc` cross-check (inode = `ss` "port" column, peer inode on the server row = the
client row's local inode):

| ss row (inode) | /proc fd | /proc symlink |
|---|---|---|
| LISTEN 38117 | Hyprland 1619 fd 11, 10 | both `socket:[38117]` |
| ESTAB server (waybar) 181151236 | Hyprland 1619 fd 250, 236 | both `socket:[181151236]` |
| ESTAB client waybar 181143087 | waybar 935660 fd 21 | `socket:[181143087]` |
| ESTAB server (socat) 10029 | Hyprland 1619 fd 147, 145 | both `socket:[10029]` |
| ESTAB client socat 40790 | socat 2293 fd 5 | `socket:[40790]` |

Every inode in the tool's rows resolves to a real `/proc/<pid>/fd` socket symlink on the
same process that the row names. Pids persist from the receipt time (waybar 935660,
socat 2293, Hyprland 1619, `pgrep -a`). **PASS**: the subscriber set and server inodes
reported by the tool match both the committed receipt and the kernel/proc ground truth.

## 3. Five out-of-fixture inputs

All run as `python3 -I tools/mado-eventq.py --ss-file <t> --log empty.log --journal-file empty.journal --disable-logs 0` (empty log/journal keep it replay-only).

- **T1 — second socket2 path** (two LISTEN rows ending in `/.socket2.sock`):
  `MADO_EVENTQ: SETUP socket2_ambiguous candidates=2`, exit `2`. Documented behaviour
  (docstring exit map; `tools/mado-eventq.py:162-163`). PASS.
- **T2 — peer row from another uid, no `users` field** (client row with no `users:`
  segment): counted as a subscriber, `comm=- pid=- fd=- peer_recv_q=0 server_send_q=0
  server_fd=250`, summary `subscribers=1 … verdict=CLEAN`, exit `0`. Graceful: a
  subscriber `ss` cannot attribute (cross-uid, or no `-p` info) is reported with the
  documented `-` placeholder rather than skipped. Matches the docstring's "`-` marks a
  value whose row is absent" spirit (holder absence → `("-","-","-")`, `:179-183`). PASS.
- **T3 — ss header variants**:
  - leading whitespace before `Netid` → parsed fine (`parse_ss` lstrip, `:150`), exit `0`. PASS.
  - header without the word `Netid` → `SETUP ss_unparseable`, exit `2`. PASS (documented).
  - `Netid` header but no `Process` column, no `users` fields → silently accepted; a
    subscriber is reported with `comm=- pid=- fd=- server_fd=-`, exit `0`. Finding (LOW):
    header schema is only checked by `startswith("Netid")`; tokenized but malformed tables
    produce a plausible census instead of the documented SETUP token. Not promised by the
    docstring, but worth a note. (md: `parse_ss` `:147-153`, `parse_row` `:136-144`).
- **T4 — CRLF lines**: identical output to the LF run (waybar/socat clients, `subscribers=2`,
  `verdict=CLEAN`, exit `0`). `splitlines()` and the `users` partition handle `\r\n`; the
  `HOLDER` regex is unaffected by a trailing `\r`. PASS.
- **T5 — 10k-row ss dump** (9997 filler rows, mixed with/without `users`, socket2 cluster
  inserted at random offsets): `subscribers=2` (waybar, socat) `verdict=CLEAN`, exit `0`,
  `real 0m0.081s`. No blowup; parse is linear over rows + dict inode join (`:169-171`). PASS.

## 4. Docstring vs behaviour

- **Exit map** (`docstring:56-62`): 0 `CLEAN`, 1 `MARKERS`/`MISSING_CLIENT`, 2
  `SETUP` token. Observed: rc 0 (fixture `clean`, live run, T2/T3a/T3c/T4/T5), rc 1
  (fixtures `overflow-log`, `writefail-journal`, `missing-client`, `overflow-twice`), rc 2
  (`unparseable`, `not-listening`, T1 `socket2_ambiguous`, w1 `no_instance`/`ss_unreadable`)
  — the code raises exactly the documented token set (`:98-99,116,126,132-133,153,161-163,168,223,225,244,255`). PASS.
- **Read-only guarantee** (`docstring:77-81`): imports are stdlib only (`argparse`,
  `json`, `os`, `re`, `subprocess`, `sys` — grep of `:83-88`); zero occurrences of
  `connect(`; no `socket` import; subprocess argv are exactly the three registered read
  verbs (`:221,242,200-201`) with `stdin=subprocess.DEVNULL` (`:105`); files are opened
  for reading except the `--snapshot-out` target (`:252`, the only write). PASS.
- **Marker exactness** — finding (LOW): `OVERFLOW`/`WRITE_FAIL` (`:92-93`) are used with
  unanchored `re.search` (`:190,194`), so a log line containing the marker sentence embedded
  in longer text would count. The fixture `decoy` (`c2-r37-eventq.py:95-97`) only covers
  prose mentioning the words, not embedding. The docstring's "only the exact marker shapes
  above are matched" (`:23-24`) is thus slightly stronger than the code. Same issue already
  recorded as SentEventqSafety F6 (Low).
- **Info**: registration.md:53-54 registers the journal default without `-o cat`; the tool
  runs `journalctl --user -u … --no-pager -q -o cat` (`:242`) and its own docstring
  documents that form — self-consistent, diverges from the registration wording (w1 F9).
  `server_fd=` lists two server fds per connection (250,236 / 147,145); `/proc` confirms two
  fds per server side (`socket:[181151236]`, `socket:[10029]`), so the multi-fd output is
  real, not an artifact.

## Verdict

All assigned items **PASS** (counter re-run; live subscriber set; server inode
cross-check vs receipt and `/proc`; the five out-of-fixture inputs; docstring exit map and
read-only guarantee), with three LOW/info findings: unanchored marker matching (T3-header
tolerance, and the registration-vs-tool journal flag wording. No blocking finding.

## Residual risk / verification gaps

- The counter's `live=1` clause remains a self-consistency replay (w1 CritC2Cheap F1 /
  RevC2Code F1); the host-level binding is this review's independent live run + `/proc`
  cross-check, which passed. Any future claim "observed on this host" should cite a live
  run like this one, not the replay alone.
- This host has `debug:disable_logs = 1` (`markers_observable=no`), so the overflow/removal
  path cannot be observed live: `CLEAN` means "no marker seen, all expected subscribers
  present", never "never overflowed" — consistent with the docstring and the registration
  refusal (registration.md:88-95).
- Cross-uid or unattributed subscribers surface as `comm=-` rows rather than being hidden;
  a consumer should know that a `-` comm is a live subscriber, not an absent one.
