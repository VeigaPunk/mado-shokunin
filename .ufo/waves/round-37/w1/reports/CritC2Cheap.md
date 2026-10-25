# CritC2Cheap — critic, mado round 37 wave 1

Target: `PRED-C2-r37-v2`, `quality/counters/c2-r37-eventq.py`, sha256
`6fae177fd5f42d7b28759eb08770bc1af63e8ad29c27f971978336bfde060f7a`. That is byte-identical at the
freeze commit `893a8aa` and at lane HEAD `80b83c8` (checked with `git show <rev>:… | sha256sum`).

## Verdict

**FINDING (blocking for C2 as frozen).** Two cribs reach `fixtures=10/10 readonly=1 live=1
verdict=TARGET_MET` under the unedited v2 counter. Neither implements the inode join that makes a
tool an `ss` subscriber census:

- **Crib B** (19 lines, 1425 B) is keyed on fixture comm names. Its live receipt comes from a
  4-line hand-written snapshot naming instance `FAKE` and Hyprland `pid=1`.
- **Crib A** (9 lines, 4453 B) is a pure memorizer: it looks up each fixture by sha256 of its
  inputs. Its "snapshot" is 2 lines of `MADO_EVENTQ` text, not `ss` output at all; the tool echoes
  them back.

Amendment 1's replay closes the v1 hole (a hand-written receipt with the right digest) only in a
narrow sense. It checks that the tool agrees with itself on a committed file, and nothing ties
that file to this host. The `readonly` clause is also lexical and evadable (item 4).

## 1. Cheapest fixture crib (no ss parser)

All work was done in `/dev/shm/mado37-CritC2Cheap/`; copies are in
`.ufo/waves/round-37/w1/scratch/CritC2Cheap/`. `score.sh` makes a sparse sandbox clone of LANE at
`80b83c8` with identity `sandbox`. It commits `tools/mado-eventq.py` and the snapshot, then writes
the receipt by running *the crib itself* on the snapshot, prefixed with `tool_sha256=`. It commits
that and runs the frozen counter with `--repo <sandbox> --rev HEAD`. LANE was never written.

| tool | sha256 | lines / bytes | how it passes |
|---|---|---|---|
| `cribB.py` | `6d44b42b…793043` | 19 / 1425 | `".socket2" not in ss` gives SETUP (kills both rc-2 cases); clients come from regex `ESTAB (\d+) (\d+) \* .*\("(waybar\|socat)",pid=…,fd=…` |
| `cribA.py` | `d60291938…0c1` | 9 / 4453 | `sha256(ss\0log\0journal\0dl\0expect…)` maps to canned `(rc, stdout)`; on a miss it echoes snapshot lines starting with `MADO_EVENTQ` |
| `refC.py` (honest reference) | `558f09f3…95e7` | 32 / 2263 | real row split plus a server/client inode join, with no fixture keys |

Commands and output (`./score.sh <name> <tool> <snapshot>`):

```
== B   (cribB.py + handsnap.txt)
PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET rev=3c467a34…
counter_exit=0 counter_wall_ms=320
== A   (cribA.py + echosnap.txt)
PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET rev=cf9c41d1…
counter_exit=0 counter_wall_ms=137
== C   (refC.py + host ss capture)
PRED-C2-r37-v2 fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET rev=201b39d3…
counter_exit=0 counter_wall_ms=642
```

Crib B's receipt as committed (digest elided):

```
tool_sha256=<64hex>
MADO_EVENTQ_CLIENT: comm=waybar pid=12345 fd=7 peer_recv_q=0 server_send_q=0
MADO_EVENTQ_MARKERS: source=log overflow=0 write_fail=0
MADO_EVENTQ_MARKERS: source=journal overflow=0 write_fail=0
MADO_EVENTQ: socket2=x subscribers=1 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=no verdict=CLEAN
```

Costs: an honest parser costs 32 lines against 19 for the cheapest crib, so cribbing saves only
about 13 lines. Even so, nothing in v2 makes the honest path the only passing path.

Crib B also fails on the real host. On a live `ss -xpa` capture it reports
`subscribers=0` (real `ss` pads its columns with variable whitespace), while `refC.py` on the same
capture reports `subscribers=2` (`comm=waybar`, `comm=socat`), matching `/proc/net/unix`. v2 cannot
see this difference, because every check runs on fixtures or on a committed file.

Why the fixtures cannot discriminate: every fixture uses the same comm names (`waybar`, `socat`,
`hyprctl`, `chromium`), single-space columns and one socket path (`…/HIS/…`). Non-subscribers can
be told apart by name, so the inode join is never forced. `--socket2` is never exercised.

## 2. Live clause: hand-written receipt plus hand-written snapshot

**FAIL (crib passes).** The replay clause (`c2-r37-eventq.py:153-176`) checks four things: the
digest line, one summary line, `subscribers=N == #client lines`, a `comm=waybar` client, and
`triples(receipt) == triples(tool(snapshot))`. Both the receipt and the snapshot are committed
files under the author's control. Any tool, run on any file the author writes, produces a receipt
that satisfies its own replay by construction:

- Crib B plus `handsnap.txt` (4 lines; fake instance `FAKE`, `pid=1`, a waybar `pid=12345`):
  `live=1`.
- Crib A plus `echosnap.txt` (2 lines, not `ss` format): `live=1`. Nothing checks that the
  snapshot even looks like `ss` output.

Cost of the crib: 2–4 hand-typed lines plus one tool run.

Independent reproduction by seat CritSeparability: its scratch tool `w1/scratch/CritSeparability/ref-eventq.py`
(102 lines, sha256 `548c314d…c8c6e`) was committed with a synthetic live receipt and snapshot
built from the counter's own `CLEAN_SS`. `probe-out-2.txt` (sha256 `9ffb6c08…416a`) records
`tree=joint-minus-c1 … fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET rev=29c2671b…`.
I read that output; I did not re-run it.

The honest tool plus a hand-written snapshot also passes. So even with a genuine tool, the v2
receipt carries **no host provenance**. It must not be cited as a host observation, for example
"waybar pid X is subscribed on this host".

## 3. Cheapest extra frozen clauses, measured

`c2-kill.py` (sha256 `c96cf514…6bc9`, scratch only) imports the frozen counter unedited, runs its
`main()` to get the v2 verdict, then adds three candidate clauses:

- **K1 heldout** (21-line generator plus a 5-line loop): 3 cases generated at score time with
  `random.Random(rev)`. Comms, pids, fds, inodes and the instance are random; columns are padded
  with 1–6 spaces; rows are shuffled. Each case also contains a decoy `waybar` on the request
  socket and a decoy orphan `socat`. A case passes when rc is 0, the (comm, pid, fd) multiset is
  exact, and `subscribers=N` is right. Because the cases are generated rather than embedded, the
  tool author cannot read them from the frozen file.
- **K2 shape** (4 lines): the snapshot starts with `Netid`, contains no `MADO_EVENTQ`, and every
  receipt triple appears as `(("c",pid=P,fd=F)` in it.
- **K3 host** (about 20 lines): at score time the counter captures `ss -xpa` itself and runs the
  tool on that capture. It requires all of the following:
  - `subscribers` equals the number of connected (`St=03`) `/proc/net/unix` rows on the single
    listening (`St=01`) socket2 path. That count is read before and after the capture; if it moved,
    the result is SETUP (exit 2), not a miss.
  - The summary reports `socket2=` as that path.
  - A waybar client is present.
  - For each client triple, `/proc/<pid>/comm` equals the comm and `/proc/<pid>/fd/<fd>` points to
    `socket:[`.

Host facts these rely on: `/proc/net/unix` filtered to the socket2 path gives `1 St=01` and
`2 St=03`; `ss -xpa` shows 3 socket2 rows; there is 1 waybar pid.

```
== A     KILL heldout=0/3 shape=0 host=0 frozen_v2=MET verdict=TARGET_MISSED  (195 ms)
== B     KILL heldout=0/3 shape=1 host=0 frozen_v2=MET verdict=TARGET_MISSED  (417 ms)
== B2    KILL heldout=0/3 shape=1 host=0 frozen_v2=MET verdict=TARGET_MISSED  (410 ms)
== Chand KILL heldout=3/3 shape=1 host=1 frozen_v2=MET verdict=TARGET_MET     (486 ms)   honest tool + hand snapshot
== Clive KILL heldout=3/3 shape=1 host=1 frozen_v2=MET verdict=TARGET_MET     (465 ms)   honest tool + real capture
```

(`cribB2.py` is crib B with a whitespace-tolerant regex `ESTAB\s+…`, still keyed on comm names.)

Smallest safe corrections, by crib:

- **Fixture cribs (A, B, B2): K1 alone kills all three.** The cheapest crib that survives K1 has to
  implement the server/client inode join, which is the capability being claimed. This is the
  recommended minimum. No harm to the accept path: the honest reference scores 3/3.
- **Echo snapshot (crib A's live half): K2 kills it** (shape=0) at 4 lines. It does not kill a
  hand-written `ss`-format snapshot (crib B shows shape=1). On its own it is not enough.
- **Degenerate tool on fabricated snapshots: K3 kills all cribs** (host=0) and makes live mean
  "observed on this host at score time". **It does not kill an honest tool paired with a
  hand-written receipt** (Chand passes). That is a tradeoff, not a fixable defect: no committed
  artifact can prove host provenance after the fact. The only binding candidate I found is to
  require the snapshot's socket2 LISTEN inode to equal the live `St=01` inode in `/proc/net/unix`.
  That breaks on every compositor restart, and anyone who reads `/proc/net/unix` can copy the
  inode, so I do not recommend it. Recommended wording instead: under v3 the receipt replay
  becomes a record, and K3 (re-observed at score time) carries the host claim.
- Separability conditions (raised by CritSeparability; both met by `c2-kill.py` as written):
  - K1's generator must take nothing from `corpus/` or `fetch/`. It draws only on
    `random.Random(rev)` and the counter's `HDR`. Deriving log shapes from S213 or E2 would
    couple C2 to C1.
  - K3 reads only `ss -xpa` and `/proc`. No C1 entry (E2 included) may cite its output.
  - Any v3 should be re-checked with `w1/scratch/CritSeparability/separability-check.py --rev <tip>`.
- Costs: K1+K2+K3 add about 50 counter lines and roughly 0.1–0.3 s of wall time
  (v2 alone 137–642 ms, v2 plus kill 195–486 ms; noisy single runs). K3 needs a live Hyprland
  session with waybar at score time, and fails closed (SETUP) without one.

## 4. `readonly` clause is lexical (extra finding)

The counter's own expression (`:181-183`) applied to source strings, without executing any of them:

```
readonly_lexical case=shell_socat readonly=1     # subprocess.run(["socat","-u","UNIX-CONNECT:…/.socket2.sock","-"])
readonly_lexical case=dunder_import readonly=1   # __import__("soc"+"ket"); getattr(c,"conn"+"ect")
readonly_lexical case=inline_import readonly=1   # import os, socket
readonly_lexical case=connect_ex readonly=1      # from _socket import socket; .connect_ex(
```

A tool that stalls on the event socket, the exact harm under study, can therefore score
`readonly=1`. Two corrections:

- **Cheapest:** widen the regex to catch `\bsocket\b` anywhere in an import line, `_socket`,
  `connect`, `socat`, `ncat`, `\bnc\b` and `UNIX-CONNECT`. This is still evadable via `__import__`.
- **Structural (measured):** run every tool invocation inside a root-private mount namespace that
  masks the Hyprland socket directory, then drop back to the invoking uid. Command run:

  ```
  sudo -n unshare -m --propagation private sh -c 'mount -t tmpfs none /run/user/1000/hypr && setpriv --reuid=1000 --regid=1000 --init-groups sh -c "…"'
  ```

  Output: `hypr_entries=0`, `ss_users_rows=819` (host: 819), `socket2_paths_visible= 0`,
  `rc=0`, `host_hypr_entries_after=1`, `host_mount_leak=no`. With the directory masked, a path
  `connect` cannot reach Hyprland, while `ss -p` still sees every process.

  The unprivileged variant (`unshare -rm`) also masks the directory but loses all process info
  (`ss_rows_with_users_in_ns=0`), so it is unusable.

  Tradeoff: the counter would need `sudo`. The masked directory also hides `hyprland.log`, which is
  harmless because the counter supplies logs explicitly. Whether the event socket uses an
  abstract-namespace name instead of a path was not checked [INFERENCE: the fixtures and the host
  show a path socket].

## Impacted axes

- **operability (C2):** the claim's `TARGET_MET` is not evidence of a working census under v2.
- **Provenance:** a v2 live receipt is self-consistency only and must not be cited as a host fact.
- **Coverage (C1):** untouched. C2 reads no corpus file.

## Hygiene

- No lane production file was edited.
- No socket was connected. The one `socket.socket()` object in the namespace probe was created
  and never connected.
- No hyprctl verb was run.
- Read-only `ss -xpa` and `/proc` reads only.
- A host `ss` capture existed only in `/dev/shm` and was deleted. Only counts are quoted here.
- Sandboxes are removed (`rm -rf sb-*`).
- `git status` of `quality tools corpus` shows other seats' corpus edits, not mine.
- No tools were installed or updated.

Checks for the main agent: re-run `bash .ufo/waves/round-37/w1/scratch/CritC2Cheap/score.sh B
$PWD/…/cribB.py $PWD/…/handsnap.txt` (paths absolute) to reproduce the v2 `TARGET_MET`, and the
same with `c2-kill.py` as the fourth argument to reproduce the kill table.
