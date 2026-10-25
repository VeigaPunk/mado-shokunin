# RevC2v3 — review of `quality/counters/c2-r38-eventq.py` (PRED-C2-r38-v3) at round-38 HEAD

- Reviewer: L1Mado38.RevC2v3 (leaf; no subagents)
- Lane rev (HEAD): `bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5`; base: `f6e3247f73152a39afb86066af48f3cedf95fb0a`; freeze: `58e55ec`
- Scope: C2 v3 clause-by-clause (live triplet, readonly, tool-presence, 14 fixtures vs live `ss -xpa` shapes, HEAD+base runs) + discrimination re-run
- Lane was READ-ONLY; all git writes in sandboxes `/tmp/mado38-RevC2v3/sb{,2,3}`. No tools installed. All quotes verbatim.

## 1. Headline

| Item | Result |
|---|---|
| Counter at HEAD | `fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET` (exit 0) |
| Counter at base f6e3247f | `fixtures=14/14 readonly=1 live=0 tool=present verdict=TARGET_MISSED` (exit 1) — `live-detail artifacts-missing` |
| Discrimination v3 (solo rerun) | `controls=19 correct=19/19 verdict=TARGET_MET` (exit 0); c2 controls 10/10 |
| Discrimination v2-before (same manifest) | `correct=12/19 verdict=TARGET_MISSED`; c2-forged/c2-docconn/c2-proc-mismatch behave as the known v2 defects |
| Committed run record | `.ufo/waves/round-38/receipts/after-discrimination-v3.txt` (b6c1d31): `19/19 TARGET_MET` — matches my rerun |
| Live ground truth (2026-10-25) | committed triplet matches **live** `ss -xpa` rows, `/proc/net/unix`, and `/proc/1619/fd` now |

## 2. Commands (exact)

```bash
# HEAD run (lane, read-only)
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c2-r38-eventq.py --repo . --rev master        # -> TARGET_MET, exit 0
# base run
python3 -I quality/counters/c2-r38-eventq.py --repo . --rev f6e3247f73152a39afb86066af48f3cedf95fb0a
# -> TARGET_MISSED, exit 1
# live shapes
ss -xpa | grep -F .socket2.sock
ss -xpa | grep -m1 ^Netid
# discrimination (sandbox)
git clone -q --no-local LANE /tmp/mado38-RevC2v3/sb
cd /tmp/mado38-RevC2v3/sb
python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py \
  --c2 quality/counters/c2-r38-eventq.py \
  --manifest .ufo/waves/round-38/controls/manifest.json --rev master
# v2-before in /tmp/mado38-RevC2v3/sb2 with --c1 c1-r37-event-ground.py --c2 c2-r37-eventq.py
# digests
git show master:.ufo/waves/round-38/receipts/eventq-live-ss.txt | sha256sum
git show master:tools/mado-eventq.py | sha256sum
# /proc cross-check
grep -E '181151236| 38117 | 10029 ' /proc/net/unix
ls -l /proc/1619/fd | grep -oE 'socket:\[(181151236|38117|10029)\]' | sort | uniq -c
```

## 3. Live triplet clause — PASS at HEAD

`live-detail replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1`

- **Replay multiset equality** (c2-r38-eventq.py:219-220): replaying `tools/mado-eventq.py` on the committed snapshot reproduces exactly the receipt's client set. Receipt client lines: `MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 …`, `comm=socat pid=2293 fd=5 …`; summary `subscribers=2`; replay equality holds.
- **tool_sha256 match** (:221-222): receipt `tool_sha256=436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24` == `sha256sum` of `git show master:tools/mado-eventq.py` = `436f550e…71f24`. ✓
- **full-table** (:227-229): committed snapshot is a real, full ~1011-line `ss -xpa` capture (not a subset). sha256 = `653311be6bb86efbe1d4448a102c4fb64666c1c6c9b63346d7a3e930ed147d3b` == proc artifact's `ss_sha256=653311be…` ✓
- **/proc binding** (:241-244): snapshot socket2 server inodes `{38117, 181151236, 10029}`; proc artifact names all three; `OVERALL: AGREE` present.
- **Live ground truth, now**: `ss -xpa | grep -F .socket2.sock` prints exactly the three rows with the same inodes and holders (Hyprland pid=1619 fd=10/11/145/147/236/250); `/proc/net/unix` binds all three inodes to the `.socket2.sock` path; `/proc/1619/fd` holds exactly 2 fds per inode (`2 socket:[10029]`, `2 socket:[181151236]`, `2 socket:[38117]`). The committed triplet matches live kernel state today — genuine, not fabricated.

## 4. Readonly clause — PASS as declared; bypass class remains (see F3/F4)

`code_lines` (:177-188) strips `#` lines, inline ` #` comments, and `"""…"""` blocks; the check (:283-285) is `\bimport\s+socket\b|\bfrom\s+socket\b` and `"connect(" not in src`.

- Real tool at HEAD/base: `readonly=1` ✓
- c2-docconn control (docstring mentions `connect(` + receipt sha updated): observed `TARGET_MET` — no false-miss ✓ (F6 fixed)
- c2-impsock control (`import socket`): observed `TARGET_MISSED` ✓
- Variant battery (via counter's own `code_lines`):
  - caught: `import socket as s`, `from socket import socket`, string literal `"import socket"`, `# connect(` comment
  - **bypassed (false-accept)**: `__import__("socket")`, `importlib.import_module("socket")`, backslash-continued `import \`/`socket`, `.connect_ex(`, `asyncio.open_unix_connection(`, `subprocess.run(["socat","-","UNIX-CONNECT:…"])`
  - **false-miss (conservative)**: `'''…connect(…'''` triple-single-quoted docstring; inline comment without space (`x=1#connect(`)

## 5. Tool-presence clause — PASS

`tool=present` at HEAD and at base (tool committed in round 37, `3f42425`, byte-identical since). At base the receipts do not exist → `live=0 artifacts-missing` → honest `TARGET_MISSED`. At round-37 base (`b4e47e98`) c2-donothing control: tool absent → `TARGET_MISSED` ✓.

## 6. 14 fixture CASES vs real `ss -xpa` shapes — PASS

All 14 pass at HEAD and at base (`14/14` both). Live shapes confirmed to exist on this host:

- Header: live `Netid State  Recv-Q Send-Q … Local Address:Port      Peer Address:Port     Process`; fixtures use a compact header. `parse_ss` only requires the `Netid` prefix; the counter's own live replay over the *real wide* committed snapshot succeeds (`replay=1`), proving whitespace tolerance end-to-end.
- LISTEN backlog `0 10` — live socket2 LISTEN row is exactly `u_str LISTEN 0 10 … 38117 …` ✓
- Server ESTAB rows with two holder tuples — live `users:(("Hyprland",pid=1619,fd=250),("Hyprland",pid=1619,fd=236))` ✓
- Client rows (`* <inode> * <peer>`), no-users rows (live e.g. `u_str ESTAB  0      0 * 33448 * 33447`), comm-with-spaces (live `omp daemon brok`), Recv-Q backlog (live `ESTAB 414 0`), `u_dgr`/`u_seq` rows — all present live and token-equivalent to the fixtures (parser is whitespace-agnostic).

## 7. Findings by severity

- **MEDIUM-HIGH — F1: the documented anti-`--snapshot-out` property is not enforced.** The predicate docstring states the snapshot "is not a `--snapshot-out` subset (it must name a request-socket or unrelated row too)". Implemented `full_table` (:227-229) counts any row that lacks the substring `.socket2.sock` and matches the row shape — **including socket2 client rows**. End-to-end demo in sandbox: I replaced the committed snapshot with the tool's own `--snapshot-out` output (header + 3 socket2 server rows + 2 client rows, extracted from the *real* capture; first line `Netid State  Recv-Q Send-Q …`), a receipt generated by rerunning the tool on it (`tool_sha256=` of the real tool, 2 client lines, `subscribers=2`), and a proc artifact carrying the real `/proc` lines for the same inodes + the subset digest + `OVERALL: AGREE`. Counter still printed `fixtures=14/14 … live-detail replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1 … verdict=TARGET_MET` (exit 0). So the v2 crib class "commit the tool's own snapshot-out output as the live snapshot" survives v3; only the byte-equal-to-fixture crib (c2-forged) is killed. This exceeds the declared residual: the docstring explicitly claims the check exists.
- **MEDIUM — F2: proc clause under-implements its docstring.** Docstring: "names every socket2 LISTEN/ESTAB server inode from the snapshot as `/proc` rows held only by the compositor pid(s) the receipt names". Code (:241-244) only checks (a) `ss_sha256=<digest>` substring, (b) each inode appears anywhere in the proc text (`\b<inode>\b`), (c) `OVERALL: AGREE` substring. It verifies neither `/proc` row format, nor inode→path binding, nor holder pids, nor any compositor pid (the receipt names no compositor pid at all — only client pids). The committed artifact passes because it is genuine (verified live), not because the counter proves it.
- **LOW-MEDIUM — F3: readonly clause bypasses (false-accept).** `__import__("socket")`, `importlib.import_module("socket")`, backslash-continued `import`, `.connect_ex(`, `asyncio.open_unix_connection(`, `socat … UNIX-CONNECT:` via subprocess all pass the clause (battery above). The declared clause ("no socket module import and no `connect(`") is implemented exactly as written, so these are clause-level residuals not named in the registration's residual paragraph.
- **LOW — F4: readonly false-misses (conservative).** `'''`-docstrings mentioning `connect(` stay in the scan (`'` is not stripped), inline comments without a space before `#` are not stripped, and a string literal `"import socket"` trips the import regex — all reject genuine tools.
- **LOW — F5:** replay equality is (comm,pid,fd)-only (`TRIPLE` captures 3 fields); the receipt's `peer_recv_q/server_send_q/server_fd` values are not cross-checked. Declared in docstring ("same (comm,pid,fd) client set").
- **LOW — F6:** the live clause does not check the receipt's `socket2=` path equals the snapshot's socket2 path, nor `verdict=CLEAN`; a consistent triplet from another instance/session would pass if the client set matches.

## 8. Freeze integrity / notes

- `c2-r38-eventq.py` byte-identical since freeze `58e55ec` (0-line diff to HEAD) ✓
- Post-freeze receipts change = only `after-discrimination-v3.txt` added (b6c1d31; a run record, 19/19 — not a counter change)
- Out-of-scope flag: `c1-r38-event-ground.py` changed +7 lines post-freeze (b6c1d31 area) — C1 reviewers should confirm that edit's predicate status
- First parallel v3/v2 run showed `17/19` / `12/19` with `clone-failed` ERRORs on c1 controls; rerunning the v3 suite alone gives `19/19`. Clone smoke test 5/5 OK. The 17/19 was concurrency flakiness of `git clone --shared` under load, not a C2 counter defect; all **c2** controls scored 10/10 in both v3 runs.

## 9. Residual risk / verification gaps

- The triplet matches live state as of review time (compositor pid/inodes unchanged); it remains a point-in-time receipt by nature.
- I did not audit `c1-r38-event-ground.py` (out of scope); only noted its post-freeze diff.
- The declared residual (fully fabricated self-consistent triplets still pass) holds; F1 narrows it further: even a *genuine-subset + genuinely-rerun-tool* triplet passes.
