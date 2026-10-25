# ScoutR29Refusal — can the host's v0.56.2 limit a request near 64 KiB?

**Lane:** mado-shokunin · **Wave:** round 38 / wave 1 · **Seat:** ScoutR29Refusal (leaf scout, no subagents)
**Target:** the refusal of the package's `socket-client-contract-measurements-r29.md`
(`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/socket-client-contract-measurements-r29.md`),
and the specific question: *is there ANY reading under which the host's v0.56.2 limits a request near 64 KiB?*

**Verdict: `partially-wrong`.** The refusal *outcome* is right (r29's numbers do not describe this host,
and r29 says so itself). The refusal's *recorded reason* is a false provenance claim, and the 64 KiB
figure is mis-attributed to a document that never carried it. Separately: **no** reading exists under
which the host's v0.56.2 imposes a ~64 KiB request ceiling — the host imposes **no byte ceiling at all**.

Read-only throughout. No lane production file was modified. Scratch in `/tmp/mado38-ScoutR29Refusal/`,
sandbox clone in `/tmp/mado38-ScoutR29Refusal/sb.1ZQpQg`. **No Hyprland socket was connected** — every
socket test used a local `socketpair(AF_UNIX, SOCK_STREAM)` I created myself, plus read-only
`/proc/net/unix`, `ss -xpmi`, `sysctl`, `stat`. **No tool was installed** (no pacman/uv/npx/cargo —
nothing was needed beyond `python3`, `curl`, `ss`, `grep`, `awk`, already present).

---

## 1. What was attacked, and the result

### 1.1 The four candidate readings of "the host caps a request near 64 KiB" — all fail

The assignment named four mechanisms. Each was tested against first-party source and against the
running host's kernel.

#### (a) `net.unix.max_dgram_qlen` — **n/a**, confirmed on two independent grounds

```
$ sysctl net.unix.max_dgram_qlen net.core.rmem_default net.core.wmem_default
net.unix.max_dgram_qlen = 512
net.core.rmem_default = 212992
net.core.wmem_default = 212992
```

`max_dgram_qlen` bounds the *datagram* queue; the request socket is a stream socket. Confirmed at
source — `.ufo/waves/round-38/fetch/S158.bin:2322`:

```
m_socketFD = CFileDescriptor{socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0)};
```

and confirmed from the kernel's own table (`/proc/net/unix`, field 5 = Type, `0001` = SOCK_STREAM):

```
400:00000000b00286f8: 00000002 00000000 00010000 0001 01 37746 /run/user/1000/hypr/.../.socket.sock
711:00000000ae9871c4: 00000002 00000000 00000000 0001 03 235508591 /run/user/1000/hypr/.../.socket.sock
```

**PASS (as n/a).** The dgram knob cannot touch a stream request socket.

#### (b) `SO_SNDBUF` / `SO_RCVBUF` on the accepted fd — **212 992 B (208 KiB), and not a request cap**

Measured on the **live compositor's own request socket**, read-only:

```
$ ss -xpmi | grep -E "\.socket\.sock"
u_str ESTAB 0 0 /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_.../.socket.sock 235508591 * 0 \
  users:(("Hyprland",pid=1619,fd=153)) skmem:(r0,rb212992,t0,tb212992,f0,w0,o0,bl0,d0)
```

`rb212992` / `tb212992` — the live socket's buffer is **208 KiB, 3.25× 64 KiB**, not 64 KiB.

The **accepted** fd inherits the listener's buffers (verified by accepting a connection on my own
local listener):

```
listener  SO_SNDBUF: 212992  SO_RCVBUF: 212992
accepted  SO_SNDBUF: 212992  SO_RCVBUF: 212992   (inherited from listener: True )
one-shot write bytes accepted before EAGAIN (peer not draining): 233152 = 227.7 KiB
  ratio to 64 KiB: 3.56 x
```

But the decisive point is that **a socket buffer is flow control, not a message ceiling.** The
compositor's loop drains the socket continuously, so the writer is never blocked and the accumulated
request is unbounded. Demonstrated in §1.3: a 4 MiB request assembles in full.

**PASS (as not-a-cap; and the number is 3.25–3.56× 64 KiB, not 64 KiB).**

#### (c) The 1023-byte chunk loop's effective bound — **no ceiling; the stop point is a drainage artifact**

The host's accept loop, `S158.bin:2271-2281` (exact lines):

```
2271:     std::string request;
2272:     while (true) {
2273:         readBuffer.fill(0);
2274:         auto messageSize = read(ACCEPTEDCONNECTION, readBuffer.data(), 1023);
2275:         if (messageSize < 1)
2276:             break;
2277:         std::string recvd = readBuffer.data();
2278:         request += recvd;
2279:         if (messageSize < 1023)
2280:             break;
2281:     }
```

`std::string request` is appended with no size check. The loop's exit is a **short read** (`messageSize
< 1023`, `:2279`), i.e. it ends when the socket runs momentarily dry — not when a byte count is hit.

Faithful replica of exactly this loop over a local socketpair (the `read()` semantics, the 1023 cap,
the `readBuffer.fill(0)`, the `std::string recvd = readBuffer.data()` C-string conversion, and the
short-read break are all reproduced):

```
== A. one-shot write then shutdown: bytes the host loop assembles ==
  write      1023 B -> assembled      1023 B in     1 reads [ok]  FULL
  write      1024 B -> assembled      1024 B in     2 reads [ok]  FULL
  write     65535 B -> assembled     65535 B in    65 reads [ok]  FULL
  write     65536 B -> assembled     65536 B in    65 reads [ok]  FULL
  write     65537 B -> assembled     65537 B in    65 reads [ok]  FULL
  write    131072 B -> assembled    131072 B in   129 reads [ok]  FULL
  write    262144 B -> assembled    262144 B in   257 reads [ok]  FULL
  write   1048576 B -> assembled   1048576 B in  1026 reads [ok]  FULL
  write   4194304 B -> assembled   4194304 B in  4101 reads [ok]  FULL
```

**A 64 KiB request is delivered whole; so is a 4 MiB one.** The host has no byte ceiling.

**Where a "~64 KiB" number can nevertheless appear** — client write pacing, not a host cap:

```
== G. 64 KiB, pause 0.3 s, 64 KiB more -> truncation at the pause boundary ==
   (65536, 65, 'ok')
== J. 1 MiB in 64 KiB pieces with 5 ms gaps ==
  (65536, 65, 'ok')
```

A client that writes its request in 64 KiB pieces with gaps **observes** its request truncated at
exactly 64 KiB — the host stops because the socket drained, not because of a size check. This is the
one genuine route to a *superficially* 64 KiB-looking observation on this host, and it is a property of
the client's chunking, not of the compositor.

**PASS (as no-cap).**

#### (d) `poll 5 s × read rate` — **the poll is a one-shot gate on the FIRST byte, not a per-chunk deadline**

`S158.bin:2264-2269`:

```
2264:     int ret = poll(pollfds, 1, 5000);
2265:
2266:     if (ret <= 0) {
2267:         close(ACCEPTEDCONNECTION);
2268:         return 0;
2269:     }
```

The poll runs **once**, before the loop. Two measurements settle its semantics:

```
== D. poll(5000) is a ONE-SHOT gate on the first byte, not a per-chunk deadline ==
   send after 6.5 s idle -> BrokenPipeError [Errno 32] Broken pipe
   server result: (0, 0, 'poll-timeout', 5.01)
```

```
K. send exactly 1023 B (a FULL chunk), then stall 8 s: is there a per-chunk deadline?
   after 8 s stall: server thread still blocked (no timeout fired)? True
   partial result so far: None
   final: (1033, 2, 'ok', 8.05)
```

So: idle >5 s → the connection is closed at 5.01 s and a later write gets `BrokenPipeError`. But once
the first byte has arrived, **there is no deadline at all** — after a full 1023-byte chunk the loop
blocked for 8 s and only completed when the remaining bytes arrived. `poll(5000) × read rate` therefore
cannot yield a byte ceiling; if anything the request is unbounded *in time* after the first byte,
which is exactly the upstream prose's freeze warning (`S187`: "Hyprland evaluates connections to this
socket completely synchronously").

**PASS (as no-cap; and the "temporal not volumetric" reading in `request-socket-live-bound-r8.md` §1 is
the correct one).**

### 1.2 Collateral finding the corpus does not record: NUL truncates each chunk

`S158.bin:2277` — `std::string recvd = readBuffer.data();` — reads the 1024-byte `readBuffer` as a
**C string**, so a NUL byte inside a chunk truncates that chunk's contribution and discards the rest
of it. Measured in the replica:

```
B. NUL inside the request: std::string recvd = readBuffer.data() truncates at NUL ==
  1001 B with one NUL at 500 -> assembled 500 B (reads 1)  [truncated at NUL: True]
L. 2146 B with NUL at offset 1023 -> assembled 1124 B in 3 reads ok
```

(2146 B with a NUL at 1023: chunk 1 contributes 1023, chunk 2 is `\0` + 1022 `B`s → contributes **0**,
chunk 3 contributes the remaining 101 → 1023 + 0 + 101 = 1124.) So a request containing a NUL is
silently mangled long before any size boundary. This is a real host behaviour, unrelated to 64 KiB,
and it is not in the corpus. It is also a plausible *mechanism* by which a third-party re-implementation
would arrive at a smaller effective cap than the host has.

### 1.3 The falsification: the refusal's recorded reason is false by provenance

This is the finding that changes the verdict.

**What the refused draft actually says and where the number came from.**
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/socket-client-contract-measurements-r29.md`:

- line 9: `source: S243 — https://raw.githubusercontent.com/iconidentify/chonkstep/main/docs/hyprland-ipc.md`
- lines 18-19: `> "There is no `/tmp` fallback. Requests are capped at 64 KiB"`
- lines 46-48 (its own **UNK**): `This is a third-party measurement of a re-implementation, not of`
  `Hyprland itself; the numbers describe what the client saw against a synthetic socket and a`
  `compatible server, not a measurement of this host's compositor.`

**The number's real source is chonkstep's own server, and it is a REQUEST cap there.**
The lane's own receipt `.ufo/waves/round-38/fetch/S277.bin` is **byte-identical** to the draft's
cited document (S243 and S277 are the same file; the lane re-pointed it to a pinned commit):

```
$ sha256sum s243.md  fetch/S277.bin
ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6  s243.md
ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6  fetch/S277.bin
$ cmp s243.md fetch/S277.bin && echo IDENTICAL
IDENTICAL
```

Its context, `S277.bin:61-63`:

```
61:There is no `/tmp` fallback. Requests are capped at 64 KiB, all request readers together
62:share a 128 KiB budget per server pass, and all descriptors are
63:non-blocking. The server retains at most **64 one-shot request clients**
```

So in the document the number came from, 64 KiB **is a request ceiling** — of chonkstep's re-implementation
server, sitting next to a "128 KiB budget per server pass" and a 64-client cap. It is not, and never was,
upstream Hyprland's `FOLLOW_QUEUE_LIMIT`.

**But the landed round says it is.** Three places carry the false attribution:

1. `corpus/knowledge/request-limits-upstream-r31.md:29-32`:
   > `the 64 KiB figure in the refused package draft (..., "requests are`
   > `capped at 64 KiB") is the *follow-queue* ceiling of a different`
   > `implementation, not a request ceiling`

   `S253.bin:44` is `static constexpr size_t FOLLOW_QUEUE_LIMIT = 64 * 1024;` — upstream's follow-**queue**
   ceiling, a completely different fact that merely shares the number 64 KiB. The claim "is the
   follow-queue ceiling of a different implementation, not a request ceiling" is therefore false twice
   over: in its own cited source the 64 KiB **is** a request ceiling (of chonkstep), and the
   "different implementation" whose follow-queue ceiling it supposedly is — upstream Hyprland — is not
   the source of the number at all. r31 cites only `S253`; it never cites `S243`/`S277`, the document
   the number actually came from, so the attribution has no evidentiary bridge at all.

2. `corpus/lessons/round-38.md:42`:
   > `**refuse** — "requests capped at 64 KiB" is the follow-queue bound; its socket census is superseded by S258's stat and round-37's live census`

3. `.ufo/waves/round-38/registration.md:87`:
   > `"requests capped at 64 KiB" vs the compositor's own `REQUEST_LIMIT = 1 MiB` / `FOLLOW_QUEUE_LIMIT = 64 KiB` (S253)`

   Note this frames S253 as a *contradicting first-party ground* for a number that S253 never
   contained.

**Counterpart: what r31 gets right.** `request-limits-upstream-r31.md:32-34` states the host's own
position correctly, and my measurement confirms it: *"this host's v0.56.2 declares neither — its handler
accumulates 1023-byte chunks with no total bound."* Verified: `grep -c "REQUEST_LIMIT\|MAX_REQUEST\|FOLLOW_QUEUE" S158.bin`
→ `0`, and the running binary carries no such constant
(`strings /usr/bin/Hyprland | grep -cE "REQUEST_LIMIT|MAX_REQUEST|FOLLOW_QUEUE"` → `0`).

### 1.4 The refusal's *other* ground is sound, and independently confirmed

The second ground — "sockets are 0600" vs the host's measured 0755 in a 0700 directory — holds.
Confirmed by the lane's own receipt `fetch/stat-sockets.txt` and re-measured by me read-only:

```
700 directory /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678
755 socket    .../.socket.sock
755 socket    .../.socket2.sock
```

And `request-limits-upstream-r31.md`'s own operative INF (`:36-38`) — *"a client can therefore send a
request larger than 64 KiB to this compositor and stay within the documented contract"* — is **true**,
and is exactly what my 64 KiB / 1 MiB / 4 MiB replica runs demonstrate. So the *conclusion* survives;
the *chain of reasoning* printed underneath it does not.

### 1.5 Collateral citation slip

`corpus/knowledge/request-socket-live-bound-r8.md:23-24` cites *`:2278` break on a short read*. Line
2278 is `request += recvd;`; the short-read break is at `:2279` (`if (messageSize < 1023)`) and `:2280`
(`break;`). One line off, in an entry that is otherwise exactly right about the semantics. r31's range
citation `:2270-2280` does cover the loop correctly.

---

## 2. Is the mis-attribution load-bearing for the landed counters? — No

The landed claim is "domain counter admits 3/3". If the mis-attribution were counter-protected, fixing
it would break the round. Tested in a **sandbox clone** (`/tmp/mado38-ScoutR29Refusal/sb.1ZQpQg`,
`git clone -q --no-local` from the lane; `rev-parse --show-toplevel` verified; **no git write of any
kind was performed in the lane**):

```
BASELINE:   admitted=3/3 verdict=TARGET_MET  exit 0
MUT-1 (r31 attribution fixed):   admitted=3/3 verdict=TARGET_MET  exit 0
MUT-2 (lesson row reason fixed): admitted=3/3 verdict=TARGET_MET  exit 0
MUT-3 (r31 INF line reworded):   admitted=3/3 verdict=TARGET_MET  exit 0
RESTORED:                        admitted=3/3 verdict=TARGET_MET  exit 0
```

MUT-1 rewrote the false sentence to the true provenance ("is the request cap of the third-party
re-implementation's own server, not a ceiling of Hyprland at all"); MUT-2 rewrote the lesson row's
reason; MUT-3 reworded r31's INF line. All three keep `admitted=3/3 verdict=TARGET_MET`.

Why: `quality/counters/c2-r38-request-ground.py` binds the entry only through (i) the surface tokens
`REQUEST_LIMIT` / `FOLLOW_QUEUE_LIMIT` (`:56`, `:103`), (ii) the S-id registry row, (iii) a Gate-quoted
receipt digest, and (iv) a lineage floor of 3-of-5 phrases — `"1 mib"`, `"64 kib"`, `"accumulated
request"`, `"queued"`, `"later"` (`:89-95`). The counter never checks *which fact* the 64 KiB belongs
to. **The false attribution is free to correct at zero cost to the landed counters.**

I also verified the host-side factual claims in r31 that I could check, since a claim about the 64 KiB
figure's provenance that is wrong makes its neighbours worth checking:

- `S253.bin:43-44` = the two constants — **confirmed** (matches `corpus/SOURCES.md:221`'s `Unix.cpp:43-44`).
- `S253.bin:118` = `if (m_input.size() > REQUEST_LIMIT)` — **confirmed**.
- `S253.bin:166` = `if (queuedBytes() + data.size() > FOLLOW_QUEUE_LIMIT)` — **confirmed**.
- "src/ipc/s1/Unix.cpp returns 404 at the host's tag" — **confirmed**: `404 src/ipc/s1/Unix.cpp`,
  `404 src/ipc/s1/Unix.hpp`, `404 src/ipc/s1/IpcManager.cpp` at `efb50993780079460b0cbed1363e2166a2de1d9f`.

---

## 3. Verdict

| Item | Verdict |
|---|---|
| Does the host's v0.56.2 cap a request near 64 KiB? (kernel dgram knob) | **PASS** — n/a; stream socket (`S158.bin:2322`, `/proc/net/unix` type `0001`) |
| …(socket buffers on the accepted fd) | **PASS** — live socket `rb212992/tb212992` = 208 KiB (3.25× 64 KiB); accepted fd inherits; and a buffer is flow control, not a ceiling |
| …(the 1023-byte chunk loop's effective bound) | **PASS** — no ceiling: 64 KiB, 1 MiB and 4 MiB requests all assemble in full; exit is a short read, i.e. a drainage artifact |
| …(`poll 5 s × read rate`) | **PASS** — poll is a one-shot gate on the first byte (5.01 s close on idle; 8 s stall after the first chunk → no timeout); no byte bound follows |
| **Is the refusal's outcome right?** | **PASS** — r29's numbers do not describe this host (0755 sockets, S258), and r29's own UNK says it describes a re-implementation |
| **Is the refusal's recorded reason right?** | **FAIL** — the 64 KiB is chonkstep's own **request** cap (`S277.bin:61`, byte-identical to the draft's S243), not upstream's `FOLLOW_QUEUE_LIMIT`; the three landed locations assert the latter with no cited bridge |
| Does the mis-attribution block a fix? | **NO** — MUT-1/2/3 all keep `admitted=3/3 verdict=TARGET_MET` |

**Overall: `partially-wrong`.** Refuse r29 — correctly — but for the ground r29 itself supplies
(its numbers describe a third-party re-implementation's server, not this host), and correct the
recorded reason. The sentence to retire is the identity claim that the draft's 64 KiB *is* upstream's
follow-queue ceiling; it is a numerical coincidence between two unrelated third-party facts, and it
is currently the load-bearing justification in `registration.md:87`, `lessons/round-38.md:42` and
`request-limits-upstream-r31.md:29-32`.

Two further facts to carry into the fix, both established above and neither counter-protected:

- The host's v0.56.2 imposes **no byte ceiling** on requests at all — the bound is temporal (5 s to
  first byte) and the request is unbounded in size *and* in time thereafter.
- The host's chunk loop drops everything after a NUL byte in each 1023-byte chunk
  (`S158.bin:2277`) — a real, unrecorded behaviour that bounds a request's *effective* content well
  below 64 KiB when a NUL is present, and a plausible mechanism behind a third-party implementation's
  smaller effective cap.

**Not claimed / not checked:** I did not connect to the live Hyprland socket, so I have no live
measurement of the host's request socket — every socket number here comes from a faithful replica of
the host's own source loop over a local socketpair, plus read-only inspection of the live socket's
kernel state (`ss -xpmi`, `/proc/net/unix`, `sysctl`). I did not audit the r29 draft's third claim
(hyprctl's exit-status vocabulary) — it is out of the assigned question and unaffected by this finding.
The `HOST-R2`/`RevEntryLimits` seats may already cover the socket-mode half of the refusal; this report
is scoped to the 64 KiB figure and the request-ceiling question only.

**Scratch:** `/tmp/mado38-ScoutR29Refusal/` (`replica4.py` — the accept-loop replica; `temporal.py`,
`trunc.py`, `nul.py`, `bufs.py`, `stall.py` — the measurements; `sb.1ZQpQg/` — the sandbox clone).
**No lane production file was modified.** No tool installs.
