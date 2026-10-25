# RevC2Code — review of `quality/counters/c2-r37-eventq.py` (PRED-C2-r37-v2)

Seat: reviewer, mado round 37 wave 1. Scope: the counter against registration §C2 and Amendment 1;
the ten CASES, the readonly clause, the live replay clause; base run. No lane production file was
edited. No Hyprland socket was connected; the only host reads were `ss -xpa` (kernel table) and the
lane's committed files. No tool was installed or upgraded.

## Verdict

The counter is sound as a *before* measurement, and the accept path exists: an honest reference tool
reaches `TARGET_MET`. But the v2 live clause, the thing Amendment 1 added, can still be met with no
live observation at all. Committing the counter's own `CLEAN_SS` fixture as the "live" snapshot
scores `TARGET_MET`. There are also four fixture gaps, each demonstrated by a variant that scores
`TARGET_MET` while being wrong (lagging, `--expect-client`, readonly) or fragile (one-pass parse).
There is also one false-miss trap that a genuine tool can fall into: the `tool_sha256` value must
sit on a line by itself.

| # | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | HIGH | Live clause met by a forged snapshot (the counter's own fixture) | scenario `ref-forged-fixture` → `TARGET_MET` |
| F2 | MEDIUM | `tool_sha256` must be a whole line; docstring says "carries" | scenario `ref-live-prefixed-sha` → `live=0` |
| F3 | MEDIUM | Fixtures always put the server row before the client row; the live table is the reverse. No fixture has a row without `users`, a two-tuple `users` field or a comm containing spaces | live line numbers; scenario `onepass-*` |
| F4 | MEDIUM | `lagging` is not discriminated: a constant `lagging=1` meets | scenario `lagconst-live` → `TARGET_MET` |
| F5 | MEDIUM | `--expect-client` has no positive case: "always missing" meets | scenario `missall-live` → `TARGET_MET` |
| F6 | MEDIUM | Readonly clause: bypassable, and a prose `connect()` false-misses a genuine tool | scenarios `impsock-live` → `TARGET_MET`, `docconn-live` → `TARGET_MISSED` |
| F7 | MEDIUM (design) | `logs-disabled` pins `verdict=CLEAN`, exit 0, when markers are unobservable | counter:91-92 vs registration:88-95 |
| F8 | LOW | `unparseable` is redundant with `not-listening` for a tool that keys SETUP on a missing listener | `nohdr` probe |
| F9 | LOW | Fixture journal lines are in `-o cat` shape, but the registered live default omits `-o cat` | S213:20 vs registration:53-54 |
| F10 | LOW | `--socket2` is never exercised; the tool subprocess inherits the session env; the fixture identities copy the live host | counter:117-118, :166-169 |
| I1 | INFO | Privacy vs robustness: the replay wants the raw full table (1102 rows on this host) | — |

## Base run (quoted)

The counter blob is unchanged since the freeze. Both of these print the same digest:
`sha256sum quality/counters/c2-r37-eventq.py` and
`git show 893a8aa…:quality/counters/c2-r37-eventq.py | sha256sum`:

```
6fae177fd5f42d7b28759eb08770bc1af63e8ad29c27f971978336bfde060f7a
```

The command was `cd LANE && python3 -I quality/counters/c2-r37-eventq.py --repo . --rev <r>`, run at
three revs. Every case line read `rc=None ok=0`. The summaries:

```
PRED-C2-r37-v2 fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MISSED rev=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
exit=1
PRED-C2-r37-v2 fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MISSED rev=893a8aadc80ab19bc163e366d674a8ac32feacd0
exit=1
PRED-C2-r37-v2 fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MISSED rev=80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b
exit=1
```

This matches the registered before (registration:64): **PASS**. It also matches
`receipts/before-c2-v2.txt`, whose last line is the same summary at b4e47e9.

## Fixture row shapes vs live `ss -xpa` (iproute2 7.2.0)

The commands were `ss -V` and `ss -xpa > /dev/shm/mado37-RevC2Code/ss-full.txt`, followed by shape-only
`awk` over the socket2 rows and their peers. The socket path is redacted here, and the raw file was
deleted afterwards. Live socket2 rows:

```
u_str ESTAB 0 0 <path> 181151236 * 181143087 users:(("Hyprland",pid=1619,fd=250),("Hyprland",pid=1619,fd=236))
u_str LISTEN 0 10 <path> 38117 * 0 users:(("Hyprland",pid=1619,fd=11),("Hyprland",pid=1619,fd=10))
u_str ESTAB 0 0 <path> 10029 * 40790 users:(("Hyprland",pid=1619,fd=147),("Hyprland",pid=1619,fd=145))
---peers
NF=9 u_str ESTAB 0 0 * 181143087 * 181151236 users:(("waybar",pid=935660,fd=21))
NF=9 u_str ESTAB 0 0 * 40790 * 10029 users:(("socat",pid=2293,fd=5))
```

- **Column count, `*` placeholders, cross-linked inodes, `users` syntax: PASS.** All fixture rows are
  9 fields (counter:51-59), like the live socket2 rows and their peers. The server's `Local` is the
  path and its `Peer` is `* <client inode>`. The client's `Local` is `* <inode>` and its `Peer` is
  `* <server inode>`. LISTEN's Send-Q is 10 and its peer port is `0`. The header (counter:44) matches
  the live header, apart from whitespace.
- **Divergence: live server rows carry two `users` tuples** (the same pid, two fds, e.g. `fd=250` and
  `fd=236`). The fixtures carry one (counter:51-57). This is harmless for the client triple, but
  untested.
- **Divergence in row order** (F3): `grep -nF .socket2.sock` gives lines `306 504 855`. The waybar and
  socat peer rows sit at lines `157 246`, so on this host clients precede their servers. Every
  fixture lists the server first.
- **Field-count histogram of the whole live table:** `29 ×11`, `2 ×13`, `291 ×8`, `779 ×9`. The
  8-field rows have no `users` field. The 11- and 13-field rows are comm names containing spaces
  (the `users` field splits across tokens). No fixture contains either shape.

## Per-case review

| Case | Real shape? | `must`/`must_not` specific to the intended behaviour? | Redundant? | Verdict |
|---|---|---|---|---|
| clean | yes | Yes. `subscribers=2` excludes the request-socket ESTAB (`REQ_E`) and the LISTEN row. `must_not comm=hyprctl` / `comm=chromium` kills "print every `*`-local row". `OTHER` reuses `fd=21`, which defeats an fd-only join. Gap: `lagging=0` is not asserted (F4) | no | PASS w/ gap |
| overflow-log | yes | The marker text equals S189:175 `"Socket2 fd {} overflowed event queue, removing"` | no | PASS |
| writefail-journal | ss yes; journal lines in `-o cat` shape (F9) | The marker text matches S189:155 `"Socket2 fd {} failed writing event: {}"` | no | PASS w/ F9 |
| not-listening | yes | `SETUP` plus `must_not verdict=CLEAN` | no | PASS |
| missing-client | yes | Yes for the negative path. The positive path (`--expect-client waybar` with waybar present) is absent (F5) | no | PASS w/ gap |
| lagging | yes | `peer_recv_q=2048` forces reading the client row's Recv-Q (the server row's is 0). `lagging=1` is not contrasted with anything (F4) | no | PASS w/ gap |
| unparseable | n/a | `must_not verdict=` | **yes**, for a tool that keys SETUP on "no listener" (F8) | LOW |
| logs-disabled | yes | `markers_observable=no` and `must_not …=yes` discriminate. `verdict=CLEAN` is a design choice in tension with the refusal (F7). dl=1 with markers present is untested | no | PASS w/ F7 |
| overflow-twice | yes | `overflow=2` kills a boolean marker check | no | PASS |
| decoy | yes | Needs the `Socket2 fd N` anchor. The v2 `c2-stub-grep` control fails it (`controls-v2.txt`: `case=decoy … rc=1 ok=0`) | no | PASS |

The summary regexes are order-dependent (`subscribers` … `overflow` … `write_fail` … `lagging` …
`missing_client` … `markers_observable` … `verdict`). That is consistent with the registered output
order (registration:58-59): PASS. Satisfiability: my scratch reference tool scores `fixtures=10/10`
(below), so all ten cases are jointly meetable.

## Sandbox probes

The sandbox was a clone made with `git clone -q --no-local LANE /dev/shm/mado37-RevC2Code/sb`, using
the identity `sandbox <sandbox@invalid>`, at sandbox base `80b83c856b8c…`. Each scenario committed a
`tools/mado-eventq.py` variant, a receipt (`tool_sha256=<digest>` plus the variant's output on the
snapshot) and a snapshot, then ran the frozen lane counter on that commit. Two scripts are kept:

- the driver, `.ufo/waves/round-37/w1/scratch/RevC2Code/drive.py` (sha256 `96084ced…63be`);
- the reference tool, `ref-eventq.py` (sha256 `0a36994a…3f5b`). It does a two-pass inode join,
  unanchored `Socket2 fd \d+ …` marker regexes and suffix-matches `/hypr/*/.socket2.sock`.

The sandbox and the raw `ss` table were then deleted. Command: `python3 -I drive.py`. The output,
with sandbox revs elided:

```
scenario=ref-live exit=0 :: PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET
scenario=ref-forged-fixture exit=0 :: PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET
scenario=ref-live-prefixed-sha exit=1 :: PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED
scenario=onepass-forged-fixture exit=0 :: PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET
scenario=onepass-live exit=1 :: PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED
scenario=lagconst-live exit=0 :: PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET
scenario=missall-live exit=0 :: PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET
scenario=impsock-live exit=0 :: PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET
scenario=docconn-live exit=1 :: PRED-C2-r37-v2 fixtures=10/10 readonly=0 live=1 tool=present verdict=TARGET_MISSED
```

These are the reference tool's client lines on the live table, as committed in the `ref-live`
receipt:

```
MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 peer_recv_q=0 server_send_q=0
MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 peer_recv_q=0 server_send_q=0
MADO_EVENTQ: socket2=<path> subscribers=2 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=no verdict=CLEAN
```

## Findings

**F1 — HIGH — the live replay does not prove "live" (counter:153-176; Amendment 1, registration:115-117).**
The replay only checks that the receipt's (comm, pid, fd) multiset equals what the committed tool
prints for *some* committed `ss` text. Nothing binds that text to this host or this session. The
counter's own `CLEAN_SS` (counter:60) contains a waybar subscriber, so committing it as
`eventq-live-ss.txt` and generating the receipt from it scores `TARGET_MET`
(`ref-forged-fixture`). The v1 hole ("a hand-written receipt carrying the right digest passed",
counter:20-21) has moved from the receipt to the snapshot, which is equally hand-writable.

Cheap binders, any of which would need a v3 re-freeze before data:
- reject a snapshot whose socket2 path is not under the instance in S213:5 (`…/hypr/efb50993…_1792804449_426444678/`), or reject the fixture instance `HIS`;
- require the receipt to carry `ss_sha256=` of the snapshot;
- require the snapshot's Hyprland pid to match a committed host receipt.

If no re-freeze happens, the claim text must state that `live=1` proves consistency, not liveness.

**F2 — MEDIUM — whole-line digest test (counter:174).** The test
`f"tool_sha256={…}" in text` checks membership in a *list of lines*, so the receipt needs a line that
is exactly `tool_sha256=<hex>`. A receipt line such as `MADO_EVENTQ_RECEIPT: tool_sha256=<hex>`
scores `live=0` (`ref-live-prefixed-sha`). The docstring (counter:13) says "carries". The executor
writing the receipt must be told the exact line form, or a genuine deliverable misses.

**F3 — MEDIUM — fixture row order and shapes are kinder than the host (counter:51-60).** A one-pass
parser that resolves a client only against server rows already seen scores `fixtures=10/10`. It is
caught only by the live replay (`onepass-live`: `live=0`, because it found 0 subscribers), and only
because the snapshot was the raw table in kernel order. The counter does not require the snapshot to
be unfiltered or in original order. A filtered, reordered snapshot (as in `onepass-forged-fixture`,
servers first) lets the fragile tool meet. The fixtures also contain no row without `users`
(291 live rows), no two-tuple server `users` field (every live socket2 server row) and no comm with
spaces (31 live rows).

**F4 — MEDIUM — `lagging` is undiscriminated (counter:70-72, :86-88).** `clean` never asserts
`lagging=0`, and `lagging` asserts only `lagging=1`. A tool printing the constant `lagging=1` meets
(`lagconst-live`), and the replay compares triples only. The lagging threshold is also unspecified.
The registration (registration:56) defines no rule that turns `peer_recv_q` into "lagging".

**F5 — MEDIUM — `--expect-client` has no positive case (counter:82-84).** No case passes
`--expect-client waybar` while waybar is subscribed. A tool that marks every expected client as
missing meets (`missall-live`). The non-missing value of `missing_client=` is also unpinned.

**F6 — MEDIUM — readonly is a text heuristic (counter:181-183).** I ran the clause's own expression on
probe strings. Each of these gave `readonly=1`:
- `import os, socket`
- `__import__('socket')`
- `importlib.import_module('socket')`
- `asyncio.open_unix_connection(p)`
- `subprocess.run(['socat','-','UNIX-CONNECT:'+p])`
- `s.connect (p)` and `s.connect_ex(p)`

`import socket` gave `readonly=0`. The `impsock-live` scenario (`import os, socket` added to an
otherwise honest tool) met. In the other direction, a docstring reading "Never calls connect() on
any socket", which is a natural sentence for this deliverable, scores `readonly=0` and
`TARGET_MISSED` (`docconn-live`). The executor must keep the literal `connect(` out of comments and
docstrings. Reviewers must read the tool for indirect socket use: the counter cannot.

**F7 — MEDIUM (design) — `CLEAN` under unobservable markers (counter:91-92).** With
`--disable-logs 1` the case requires `verdict=CLEAN`, exit 0. That is the machine form of the
inference the registration refuses for r28/r29 (registration:88-95: "A zero there cannot tell 'never
overflowed' from 'not logged'"). It is mitigated by `markers_observable=no` on the same summary line.
But a consumer that reads only exit 0 or `verdict=CLEAN` re-commits the refused inference.

This host is exactly that case (S213:28, `"int":1`). Every honest live receipt will therefore read
`markers_observable=no verdict=CLEAN`, as the `ref-live` receipt above does. The tool's help text,
the corpus and the SCORECARD row must say that `CLEAN` means "every expected subscriber present, no
marker seen", never "no overflow". The case where `dl=1` and a marker is present (left over from a
logs-enabled period) is untested.

**F8 — LOW — `unparseable` adds little.** A reference variant with the header check deleted still
passes both SETUP cases (`nohdr unparseable (True, 2)`, `nohdr not-listening (True, 2)`): garbage
has no LISTEN row, so "no listener" already returns SETUP. The case's only extra force is
`must_not verdict=` instead of `verdict=CLEAN`.

**F9 — LOW — journal shape.** S213:20 measured the unit journal with
`journalctl … --no-pager -q -o cat`, which gives bare messages, and the fixture journal is in that
shape (counter:63-65). The registered live default is `journalctl --user -u
wayland-wm@hyprland.desktop.service` without `-o cat` (registration:53-54), which prefixes a
timestamp, host and identifier. A tool that anchors `^ERR \]: Socket2` passes every fixture but would
miss prefixed live lines. `decoy` tests the `Socket2 fd N` anchor, not prefix tolerance. Recommend
an unanchored `Socket2 fd \d+ (overflowed event queue|failed writing event)` search, or `-o cat` in
the default.

**F10 — LOW — implicit interface constraints.**
- (a) `--socket2` is never passed (counter:116-117). The registration says the interface is "frozen
  by the fixtures" (registration:51-52), but this flag is not.
- (b) `run_case` and the replay inherit `os.environ`, which has no `env=` filter (counter:118,
  :166-169). On this host `HYPRLAND_INSTANCE_SIGNATURE` and `XDG_RUNTIME_DIR` are set (`HIS_set=1
  XDG_set=1`). A tool that defaults to `$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock`
  fails every non-SETUP fixture, because the fixtures use instance `HIS`. The tool must suffix-match
  when `--socket2` is absent. That is an unregistered requirement.
- (c) The fixture identities (waybar `pid=935660 fd=21`, socat `pid=2293 fd=5`) are this host's live
  subscribers. A tool that ignores `--ss-file` and reads live `ss` passes `clean`. The other cases
  (`not-listening`, `lagging`, `missing-client`, `unparseable`) still catch it.

**I1 — INFO — privacy.** A raw `eventq-live-ss.txt` publishes the comm, pid and socket path of every
process on the host (1102 rows here). Filtering the snapshot to the socket2 rows and their peers
helps privacy, but it removes the only coverage F3 has. The L1 should choose deliberately, for
example by keeping order and rows while redacting comm names of non-socket2 rows.

## Residual risk / verification gaps

- The replay does not check its own exit code or its summary line (counter:166-176). It checks
  triples only.
- `TRIPLE` (counter:40) takes `comm=(\S+)`. A comm with spaces is truncated identically on both
  sides, so equality holds without the full name being checked.
- How the summary `overflow=` combines a marker that appears in both channels (sum or max) is
  unpinned. Each fixture places markers in one channel only.
- Hyprland's userspace queue (`MAX_QUEUED_EVENTS = 64`, S189:169-175) is invisible to `ss`.
  `peer_recv_q` measures only the kernel buffer. That limits what the tool can mean; it is not a
  counter defect.
- Not checked: whether `S215.bin` / `S216.bin` (present but untracked in LANE's working tree, and not
  mine) bear on C2.
