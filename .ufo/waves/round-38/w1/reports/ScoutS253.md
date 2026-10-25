# ScoutS253 — re-open the upstream limits source (S253)

Round 38, wave 1. Scope: the S253 upstream receipt `src/ipc/s1/Unix.cpp` @ commit
`a1c2428f79b3b05c3fd36c27378e3538c8c6a014`, and the contrast the entry
`corpus/knowledge/request-limits-upstream-r31.md` draws.

All fetches performed read-only into `/tmp/mado38-ScoutS253/`. No lane production
file was modified. No tool was installed (stock `curl`, `git`, `python3`, `grep`,
`cmp`, `sha256sum`, `wc` sufficed).

> **Status note (added after the run).** While this report was being written, the
> lane HEAD advanced from `bb1adce` to `23a0e0f`, passing through the seat-fix
> fold `b8400aa` ("registry row corrections (sizes/anchors/stamp/S277 URL)"), which
> **repaired the defect this report found**. The findings below are stated
> against the frozen/reviewed state (`bb1adce`, the rev the round-38 counters
> were run at) and are re-verified against current HEAD in
> §7 "Post-fold re-verification". No finding below was retracted; the
> `SOURCES.md` row defect was fixed, not invalidated.
>
> **Final re-check at tip `23a0e0f`:**
> the S253 row still reads `Unix.cpp:43-44` / `11602 B sha256`; all six
> registry byte figures still match their receipts; the counter still reports
> `3/3 TARGET_MET` at `rev=23a0e0f…` (unchanged since the freeze commit
> `58e55ec`); and **both residues remain open** — the S277 row still pins the
> non-existent commit `707cf7f8…` under the `chriskearney` spelling, and r8
> still carries the `:2278` anchor. See §7.4.
>
> **Extended at tip `c46f868`:** the S253 repairs still hold; the `:2278` anchor
> (F2), the S187 escaping note (F4) and the S277 dead pin are all still open;
> a commit-hygiene finding appears — `5e4c2ba`'s message claims F2/F4/F6 fixed
> while its diff contains only F6 (§7.5); the F6 revert at `919d7d0` is
> shown to be *required* by the counter's g-clause rather than a regression
> (§7.6); and the S277 entry and row are shown to diverge in citation *shape*,
> with only the row actually broken (§7.7).

---

## Item 1 — fetch the pinned commit and `cmp` with `S253.bin`

**PASS — byte-identical.**

```
$ curl -sS -o Unix.cpp.pinned 'https://raw.githubusercontent.com/hyprwm/Hyprland/a1c2428f79b3b05c3fd36c27378e3538c8c6a014/src/ipc/s1/Unix.cpp'
$ cmp Unix.cpp.pinned .ufo/waves/round-38/fetch/S253.bin && echo "IDENTICAL exit=0"
IDENTICAL exit=0
$ cmp -l Unix.cpp.pinned .ufo/waves/round-38/fetch/S253.bin | wc -l
0
```

```
$ sha256sum Unix.cpp.pinned .ufo/waves/round-38/fetch/S253.bin
3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf  Unix.cpp.pinned
3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf  .ufo/waves/round-38/fetch/S253.bin
```

The digest also matches the pinned value in the `GATE` line
(`corpus/lessons/round-38.md:15`) and in `corpus/SOURCES.md:221`. Independently
confirmed against the GitHub blob API at the same ref:

```
$ curl -sS ".../contents/src/ipc/s1/Unix.cpp?ref=a1c2428f79b3b05c3fd36c27378e3538c8c6a014"
size: 11602
sha256(decoded): 3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf
```

The pinned commit is real and upstream: API reports
`a1c2428f79b3b05c3fd36c27378e3538c8c6a014`, dated `2026-10-23T23:31:33Z`,
"layout/scrolling: fix inconsistent column widths at tape edges…(#16581)".

## Item 2 — REQUEST_LIMIT / FOLLOW_QUEUE_LIMIT at `:19-20`

**FAIL — the citation is wrong. The constants are at `:43-44`, not `:19-20`.**

```
$ grep -n 'static constexpr size_t REQUEST_LIMIT\|static constexpr size_t FOLLOW_QUEUE_LIMIT' Unix.cpp.pinned
43:static constexpr size_t REQUEST_LIMIT      = 1024 * 1024;
44:static constexpr size_t FOLLOW_QUEUE_LIMIT = 64 * 1024;
```

What actually occupies `:19-20` of the pinned file:

```
19	using namespace IPC::Socket1;
20	
```

`corpus/SOURCES.md:221` records the locator as:

> `src/ipc/s1/Unix.cpp:19-20` (REQUEST_LIMIT, FOLLOW_QUEUE_LIMIT)

This is the **only** line-cite defect; `:118` and `:166` are correct (Item 3).
The two constants' *values* and their *verbatim text* are correct everywhere they
appear (verified below), so this is a locator defect, not a factual one.

**Where `:19-20` came from.** It is not a stale line-number for this file. The
constants have sat at `:43-44` in every revision of `src/ipc/s1/Unix.cpp` that
exists upstream — the file was created by the socket1/socket2 refactor
`ff24e1755fd3` (2026-07-28) and the file has only three upstream revisions:

```
59177602ffd7 11602 2026-09-02  log: update logging macro to include callsite (#16111)
88c6386994c9 11732 2026-08-01  chore: replace string concatenation with std::format (#15652)
ff24e1755fd3 11718 2026-07-28  ipc: refactor socket1 and socket2 (#15624)
```

Grepping each of those three revisions for the constants returns `43:` and `44:`
in all three. So `:19-20` matches no revision of this file.

The most likely origin is the **package draft's own copy** of the file, which the
lane inherited. The package cached the identical bytes
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/f10cd38b11211352a7eb2e93.txt`,
11602 B, same sha256) — and *its* constants are also at `:43-44`, with the
`:118` and `:166` checks at the same lines. The upstream package text
(`.qcache/f10cd38b11211352a7eb2e93.txt:43-44`) shows the same layout:

```
43:static constexpr size_t REQUEST_LIMIT      = 1024 * 1024;
44:static constexpr size_t FOLLOW_QUEUE_LIMIT = 64 * 1024;
```

So `:19-20` is unexplained by any byte source I can find. [INFERENCE] It is most
likely a hand-transcription error (an off-by-24 drift from the `:43-44` truth),
not a captured-from-another-revision figure.

**Scope of the defect — important.** The wrong `:19-20` locator appears in
exactly one committed place:

- `corpus/SOURCES.md:221` (the S253 registry row).

The **entry body** `corpus/knowledge/request-limits-upstream-r31.md` does *not*
repeat it. The entry cites only the two check sites, `:118` and `:166`, both of
which are correct. The entry's quotes of the two constants are verbatim and
whitespace-exact:

```
$ grep -c 'static constexpr size_t REQUEST_LIMIT      = 1024 \* 1024;' .ufo/waves/round-38/fetch/S253.bin
1
$ grep -c 'static constexpr size_t FOLLOW_QUEUE_LIMIT = 64 \* 1024;' .ufo/waves/round-38/fetch/S253.bin
1
```

So the round's *substantive* claim set (constants, values, check sites, later-revision
caveat) survives; what fails is the registry row's line locator.

## Item 3 — the `readRequest` check at `:118` and `addFollowData` at `:166`

**PASS — both exact.**

```
$ awk 'NR==118 || NR==166 {printf "%d\t%s\n", NR, $0}' Unix.cpp.pinned
118	            if (m_input.size() > REQUEST_LIMIT)
166	    if (queuedBytes() + data.size() > FOLLOW_QUEUE_LIMIT)
```

Both are inside the functions the entry names:

```
111	bool CUnixPeer::readRequest(std::string& request) {
...
165	bool CUnixPeer::addFollowData(std::string&& data) {
```

The entry's prose quotes (`if (m_input.size() > REQUEST_LIMIT)`,
`if (queuedBytes() + data.size() > FOLLOW_QUEUE_LIMIT)`) match the bytes verbatim.

## Item 4 — current upstream head of `src/ipc/s1/Unix.cpp`: do the constants still exist?

**PASS — yes, unchanged. The pinned commit is still the current upstream byte-for-byte.**

```
$ curl -sS -o Unix.cpp.master '.../hyprwm/Hyprland/master/src/ipc/s1/Unix.cpp'
$ curl -sS -o Unix.cpp.main   '.../hyprwm/Hyprland/main/src/ipc/s1/Unix.cpp'
$ sha256sum Unix.cpp.pinned Unix.cpp.master Unix.cpp.main
3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf  Unix.cpp.pinned
3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf  Unix.cpp.master
3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf  Unix.cpp.main
```

`master` and `main` are the same bytes. Two caveats on how I established that:

- **`master` is not a branch in this repo.** `git ls-remote` shows only
  `refs/heads/main`; the GitHub API's default branch is `main`; there is no
  `refs/heads/master` (`api.github.com/repos/hyprwm/Hyprland/git/ref/heads/master`
  → `404`). The 34 upstream branches are `main` plus `v0.3x`–`v0.56.x` release
  branches and a few feature branches.
- **`raw.githubusercontent.com/.../master/...` still resolves**, because the raw
  host falls back to the repository's default branch for a legacy `master` ref.
  I proved the fallback is real rather than a stale cache by fetching two files
  that *changed* between the pinned commit and current HEAD — they differ from
  the pinned bytes but are byte-identical between `master` and `main`:

```
src/config/lua/objects/LuaMonitor.cpp  pinned=5356989ddb1e  master=bcf04d2cbb50  main=bcf04d2cbb50
src/desktop/view/window/Window.cpp      pinned=ec5b4f5977da  master=c3103d415f07  main=c3103d415f07
```

  A bogus ref correctly 404s (`nosuchbranchzz` → `404`), so the `master`
  fallback is not a catch-all.

Current upstream HEAD is `c4e7596a3db89cb0d213eeb3e436599422995b43`
(`2026-10-25T09:15:06Z`), which is **4 commits ahead** of the pinned commit
(`status: ahead ahead_by: 4 behind_by: 0` via the compare API). The pinned
commit is therefore *not* literally upstream HEAD any more — but the file itself
has not changed since `59177602` (2026-09-02), so the pinned bytes remain the
current upstream bytes of this path.

The entry's `source:` line says "@ commit `a1c2428f…` (current upstream)". As of
today that commit is 4 commits behind upstream HEAD. [INFERENCE] The phrase is
already stale, though harmlessly so: the cited file is identical at HEAD. It is
worth a `recheck: on-release` already declared in the entry (present at
`verified-at: 2026-10-25`, `recheck: on-release`).

**Line numbers at HEAD are the same** — `:43-44`, `:118`, `:166` — so the
correct locator survives upstream drift.

## Item 5 — `src/debug/HyprCtl.cpp` at that commit has no byte bound (the contrast)

**PASS on the substance; the file named in the task does not exist at that commit.**

The task asked me to confirm `src/debug/HyprCtl.cpp` at the pinned commit has no
byte bound. That path does not exist at `a1c2428f…`:

```
$ curl -sS -o /dev/null -w '%{http_code}\n' '.../a1c2428f.../src/debug/HyprCtl.cpp'
404
```

The pinned tree's `src/debug/` contains only `Overlay.cpp`, `Overlay.hpp`,
`TracyDefines.hpp`, `crash/`, `log/` — no `HyprCtl.cpp`. Upstream moved the
`hyprctl` client out of the compositor tree; at the pinned commit the client
lives at `hyprctl/src/main.cpp` (604 lines, 18155 B), and `hyprctl/` is a
separate top-level directory in the tree.

**The contrast the entry actually draws is against the host's own v0.56.2
handler, not against upstream's current `HyprCtl.cpp`** — and that contrast
holds. The entry (`request-limits-upstream-r31.md`, §1) claims the host's
v0.56.2 "handler accumulates 1023-byte chunks with no total bound (S158
`:2270-2280`)". Verified against the host's own file at tag `v0.56.2`
(= `efb50993780079460b0cbed1363e2166a2de1d9f`; `git ls-remote --tags` confirms
`efb5099… refs/tags/v0.56.2`):

```
2271	    std::string request;
2272	    while (true) {
2273	        readBuffer.fill(0);
2274	        auto messageSize = read(ACCEPTEDCONNECTION, readBuffer.data(), 1023);
2275	        if (messageSize < 1)
2276	            break;
2277	        std::string recvd = readBuffer.data();
2278	        request += recvd;
2279	        if (messageSize < 1023)
2280	            break;
2281	    }
```

The loop accumulates into `std::string request` with **no total-size ceiling** —
each iteration is capped at 1023 bytes but the accumulation is unbounded. A
whole-file search for any request-size ceiling in the host's handler returns
nothing:

```
$ grep -nE '65536|64 \* 1024|64\*1024' HyprCtl.v0562     # → no match
$ grep -nE 'request\.size|request\.length' HyprCtl.v0562
1318:    for (size_t i = 0; i <= request.size(); ++i) {
1319:        char ch = (i < request.size()) ? request[i] : ';';
1326:        reply += g_pHyprCtl->getReply(trim(request.substr(idx, i - idx))).append(DELIMITER);
```

Both hits are *read* sites of `request.size()` (a parser loop and a reply
splitter), not a bound. The host's receipt `S158.bin` is byte-identical to what
I fetched from the host tag (`sha256 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`,
97582 B — matching the S158 registry row and the round-38 `GATE` line).

**So the contrast holds**: host v0.56.2 has no request byte bound; upstream
`a1c2428f…` declares 1 MiB. The entry's §1 `INF` and the r31 `INF` ("this
host's v0.56.2 declares neither") are correct.

### 5.1 Which commit the 404 applies to — a distinction worth stating precisely

`src/debug/HyprCtl.cpp` 404s at **one** of the two commits in play and exists at
the other. Getting this backwards would wrongly indict S158, whose row cites
the host tag. Verified both ways:

```
$ curl -sS -o /dev/null -w 'a1c2428f (S253 upstream) src/debug/HyprCtl.cpp: HTTP:%{http_code}\n' \
    '.../a1c2428f79b3b05c3fd36c27378e3538c8c6a014/src/debug/HyprCtl.cpp'
a1c2428f (S253 upstream) src/debug/HyprCtl.cpp: HTTP:404

$ curl -sS -o /dev/null -w 'master src/debug/HyprCtl.cpp: HTTP:%{http_code}\n' \
    '.../hyprwm/Hyprland/master/src/debug/HyprCtl.cpp'
master src/debug/HyprCtl.cpp: HTTP:404
```

The 404 is at **S253's pinned upstream commit** — where the `hyprctl` client had
already been split out to `hyprctl/src/main.cpp`. It **exists** at the host tag
`efb50993…` (v0.56.2), which is the commit S158's row cites. The client move
happened upstream *after* the host tag, which is exactly why the host's v0.56.2
still carries the handler in `src/debug/HyprCtl.cpp`.

S158's locator is therefore sound — four independent confirmations:

```
$ curl -sS -o s158.tmp '.../efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp'
HTTP:200 bytes:97582
sha256 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa   == S158.bin
CMP: IDENTICAL to S158.bin

$ # git tree at efb5099 (truncated:false)
src/debug/HyprCtl.cpp   size 97582
src/debug/HyprCtl.hpp   size 1985

$ git ls-tree efb5099… src/debug/HyprCtl.cpp
100644 blob 060e25b096e682770e4be64a4e1570f355ce72b3   src/debug/HyprCtl.cpp
$ git cat-file blob 060e25b096e682770e4be64a4e1570f355ce72b3 | sha256sum
798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa   == S158.bin, cmp IDENTICAL
```

A caution on method: the GitHub **contents API** for that path returned a
`KeyError: 'content'` which looks like a 404 but was in fact
`"API rate limit exceeded for 179.218.13.209."` — the `size` field was `None`
and the body was a rate-limit message, not a not-found. The git tree and the
raw fetch are the reliable evidence here, not the contents API. I record this
because a rate-limit response silently read as "file absent" is exactly how a
false "file-not-at-commit" finding gets manufactured.

[Cross-lane note.] A sibling report initially recorded S158's locator as a
"file-not-at-commit" instance of the dead-citation class, attributing the claim
to me. It was neither true nor mine — the 404 belongs to the *other* commit.
Corrected with the evidence above; `RevRegistry` independently confirmed S158
is clean, and the class is two instances, not three.

One corroborating detail, in the entry's favour: upstream's `s2` (event) socket
has **no** byte ceiling either — `src/ipc/s2/Unix.cpp` at the pinned commit
contains only `MAX_QUEUED_EVENTS = 64` (`:187`) and a comment `// 10 max queued.`
(`:106`). The `FOLLOW_QUEUE_LIMIT` in `s1` is the follow-queue bound only. So
the entry's scoping of the two constants to "the request socket" and its
distinction between the request ceiling and the follow-queue ceiling are both
accurate.

## Item 6 — the "64 KiB" characterization in the entry

The entry corrects the refused r29 draft's "requests are capped at 64 KiB",
attributing that figure to the *follow-queue* ceiling of a different
implementation rather than to a request ceiling. Traced to source:

- The r29 draft (`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/socket-client-contract-measurements-r29.md:20`)
  quotes S243 (chonkstep): `"There is no `/tmp` fallback. Requests are capped at 64 KiB"`.
- The pinned chonkstep receipt `S277.bin` says the same and more
  (`:61-65`):

```
61:There is no `/tmp` fallback. Requests are capped at 64 KiB, all request readers together
62:share a 128 KiB budget per server pass, and all descriptors are
63:non-blocking. The server retains at most **64 one-shot request clients**
64:and **64 event subscribers**; an accepted connection beyond either cap
65:is closed immediately and the continuously-full population is logged
```

This confirms the entry's correction is well-founded: the 64 KiB figure the
refused draft cited came from a third-party re-implementation's description of
its *own* server's caps, and upstream's actual request ceiling at the pinned
commit is 1 MiB, not 64 KiB. The entry's wording — "the *follow-queue* ceiling
of a different implementation, not a request ceiling" — is a fair reading of the
number's provenance. Note that 64 KiB is numerically identical to upstream's
`FOLLOW_QUEUE_LIMIT = 64 * 1024`, which is what makes the correction
non-obvious and worth making explicitly.

Also checked: the `S187` receipt is the 0.56.0 IPC wiki page and contains
**no** occurrence of "64 KiB" (`grep -c -i '64 KiB'` → 0), so the 64 KiB claim
cannot be sourced to S187 either. The `S253` registry row's aside that
"`S187.bin` is unrelated" is accurate.

---

## Finding (one defect, non-substantive)

**F1 — `corpus/SOURCES.md:221` cites `src/ipc/s1/Unix.cpp:19-20` for the two
constants. The correct locator is `:43-44`.** `:19-20` in the pinned file is
`using namespace IPC::Socket1;` and a blank line. The constants have been at
`:43-44` in all three upstream revisions of the file, so no revision supports
the cited locator. The `:118` and `:166` cites in the same row are correct, and
the entry body does not repeat the error.

Suggested repair (row `S253`, `corpus/SOURCES.md:221`):
`` `src/ipc/s1/Unix.cpp:43-44` (REQUEST_LIMIT, FOLLOW_QUEUE_LIMIT) ``

Two secondary items, both non-defects, noted for the record:

- The row also records the file as `39464 B`. The actual size is **11602 B**
  (verified three ways: `wc -c` on both the fetch and the pinned download; the
  GitHub contents API `size: 11602`; and the digest matching across all four
  copies). The sha256 in the same row is correct. `39464` corresponds to no file
  of that size in the pinned tree (nearest is `ScrollingFullscreenHandler.cpp`
  at 39486) and to no revision of this file (11602 / 11732 / 11718). Since the
  row's digest is right and the byte count is wrong, this is a second
  transcription slip in the same row. **I did not count this as a separate
  scored defect** — the SOURCES schema check passes on it (`sources-census.sh
  validate` → `mado ok .../corpus/SOURCES.md`) and the digest is the
  load-bearing field — but it is the same row and the same class of error, so a
  single repair pass should fix both.
- The entry's `source:` phrase "(current upstream)" is 4 commits stale
  (upstream HEAD is now `c4e7596a…`, 2026-10-25). The cited file is
  byte-identical at HEAD, so no factual claim is affected.

## Why the landed round did not catch F1

The round's own counters and validators were run against this material and
passed:

```
$ python3 quality/counters/c2-r38-request-ground.py --repo . --rev HEAD
PRED-C2-r38-v1 entry=corpus/knowledge/request-limits-upstream-r31.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 ids=S253 lineage=5/3 ok=1
PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 base=f6e3247f73152a39afb86066af48f3cedf95fb0a

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

Neither checks line locators or byte counts. The request-ground counter's
clauses verify the registry row's *shape* (clause `c`: exactly one row, 11
cells, `mined` flag, correct used-by), the `GATE` pin↔digest binding (clauses
`d`/`f`/`g`), the coverage-map row (`e`), and lineage phrases (`l`) — but
nothing inside `corpus/SOURCES.md`'s locator cell is ever resolved against the
cited file's bytes. Clause `f` does check that the entry's *surface tokens*
appear in the receipt bytes, and clause `d` verifies the `GATE` quote is
byte-present in the receipt — which is why the constants' **values** and the
`:118`/`:166` **quotes** are solid while the **locator** is not.

So the gap is a tooling blind spot, not a reasoning gap: a round-39 counter
clause that resolves each `SOURCES.md` locator (`file:line-range`) against its
cited receipt — asserting the named construct actually occupies those lines —
would have caught F1 mechanically.

---

## 7. Post-fold re-verification (against current HEAD `c46f868`)

The seat-fix fold `b8400aa` (2026-10-25 11:23:56) landed mid-run. Current HEAD
is `c46f868`; `corpus/SOURCES.md` is clean against it (`git status --porcelain
corpus/SOURCES.md` → empty).

### 7.1 F1 and the byte-count slip are now repaired

```
$ grep -oE 'S253 \|.*' corpus/SOURCES.md | grep -oE 'Unix\.cpp:[0-9-]+|[0-9]+ B sha256'
Unix.cpp:43-44
11602 B sha256
```

The row now reads `` `src/ipc/s1/Unix.cpp:43-44` (REQUEST_LIMIT,
FOLLOW_QUEUE_LIMIT) `` and `11602 B` — exactly the repair this report
recommended. The `:118`/`:166` cites and the digest are unchanged and correct.

The fold repaired the **same class** across the other new rows. Pre-fold
(`bb1adce`) versus actual receipt sizes, all four wrong in the same way:

| id | stated at `bb1adce` | actual receipt | note |
|---|---|---|---|
| S221 | `35046 B` | 306865 B | `35046` is **S221's own sha256 prefix** (`35046ba0…`) — a paste slip |
| S253 | `39464 B` | 11602 B | transcription slip |
| S258 | `1401 B` | 673 B | transcription slip |
| S277 | `19737 B` | 35421 B | transcription slip |

S158 (`97582 B`) and S187 (`268731 B`) were already correct. Every one of the six
rows' byte figures is now correct at HEAD:

```
$ for f in .ufo/waves/round-38/fetch/*; do ... done
S158.bin          97582 B  sha256=798b7c6c4c16
S187.bin         268731 B  sha256=136e5511fba5
S221.bin         306865 B  sha256=35046ba0dc1d
S253.bin          11602 B  sha256=3ba8e461bd46
S277.bin          35421 B  sha256=ff561fe0d096
stat-sockets.txt     673 B  sha256=fcc608203f66
```

This corroborates the class: the figures were **transcription artifacts, not
measurements**. S221's is the clearest instance — `35046` is literally the first
five hex digits of S221's own digest, so the byte-count cell was populated from
the neighbouring digest cell.

### 7.2 Two defects I could NOT confirm as fixed at HEAD

These are outside my assigned scope (S253) but were surfaced by the same fold
and are left here because they are the residue of the class my finding belongs
to. Both were reported to `L1Mado38.RevRegistry` / `L1Mado38.RevDomCounter`.

**(a) The r8 entry's `:2278` anchor is still wrong at HEAD.** The entry says
"`:2278` break on a short read". In the S158 receipt, `:2278` is
`request += recvd;` — the break is at `:2280` and its guard `if (messageSize <
1023)` at `:2279`:

```
$ awk 'NR>=2274 && NR<=2281 {printf "%d\t%s\n", NR, $0}' .ufo/waves/round-38/fetch/S158.bin
2274	        auto messageSize = read(ACCEPTEDCONNECTION, readBuffer.data(), 1023);
2275	        if (messageSize < 1)
2276	            break;
2277	        std::string recvd = readBuffer.data();
2278	        request += recvd;
2279	        if (messageSize < 1023)
2280	            break;
2281	    }
```

Still present at HEAD (`corpus/knowledge/request-socket-live-bound-r8.md:24`).
The fold touched only that file's `source:` header line, not this anchor.

**(b) The S277 pinned-commit URL is dead — and the fold changed it to another
dead URL.** This is worth recording because the fold's own commit message claims
"S277 URL" correction. The receipt `S277.bin` is byte-identical to the
**current `main`** of the repo (sha256 `ff561fe0…` matches
`raw.githubusercontent.com/iconidentify/chonkstep/main/docs/hyprland-ipc.md`
exactly), so the receipt is a `main` snapshot, not a pinned-commit snapshot.

The pinned commit `707cf7f8b39d0b4e2cba46d0a2559b562d8821ce` **does not exist**
in the repository. Proved via the git protocol, not just HTTP:

```
$ git fetch --depth=1 origin 707cf7f8b39d0b4e2cba46d0a2559b562d8821ce
fatal: remote error: upload-pack: not our ref 707cf7f8b39d0b4e2cba46d0a2559b562d8821ce
```

Control on the same remote (a known-good SHA) succeeds, so the method is sound:

```
$ git fetch --depth=1 origin c37fbe3e439dc27db9ce8176546febb58680dfc5 && git cat-file -t c37fbe3e...
commit
```

Fetching all 260 refs of the repo also does not surface it. Raw HTTP 404s for
both owner spellings, and `git ls-remote` shows the repo's `HEAD` is
`c37fbe3e…`. `iconidentify/chonkstep` is a **renamed** repository (GitHub
returns `301 Moved Permanently`); the new canonical owner is `chriskearney`.

The fold `b8400aa` changed the row's URL owner from `iconidentify/chonkstep` to
`chriskearney/chonkstep`. Both spellings 404 at the pinned commit
(`raw.githubusercontent.com/chriskearney/chonkstep/707cf7f8…/docs/hyprland-ipc.md`
→ 404; `iconidentify/...` → 404, and `codeload` tarball for that sha → 404), so
the fold **did not** make the pinned-commit URL resolvable — it only renamed the
owner. The correct fix is to pin a commit that exists (the `main` snapshot the
receipt actually is: `c37fbe3e439dc27db9ce8176546febb58680dfc5`), or to relabel
the row's locator as `main` with a recheck cadence — which is what the receipt
digest already describes.

For contrast, my own S253 pinned commit resolves cleanly by the same method:

```
$ git fetch --depth=1 origin a1c2428f79b3b05c3fd36c27378e3538c8c6a014 && git cat-file -t a1c2428f...
commit
```

so the S253 pin is a genuine, existing upstream commit — unlike S277's.

**The recommended replacement pin is verified to yield the receipt exactly.**
`c37fbe3e439dc27db9ce8176546febb58680dfc5` (the repo's `HEAD`) serves a blob
that is byte-identical to `S277.bin` under **both** owner spellings:

```
$ curl -sS -o pin.tmp ".../iconidentify/chonkstep/c37fbe3e439dc27db9ce8176546febb58680dfc5/docs/hyprland-ipc.md"
raw c37fbe3e: 200 ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6
receipt:          ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6
CMP: IDENTICAL to S277.bin

$ curl -sS -o pin2.tmp ".../chriskearney/chonkstep/c37fbe3e.../docs/hyprland-ipc.md"
chriskearney@c37fbe3e: 200 ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6
CMP: identical across owner spellings
```

So the repair is unambiguous: re-pin S277 to `c37fbe3e` (keeping either owner
spelling, since the rename redirects) and the row's receipt/digest/locator all
become mutually consistent, with no change to the committed receipt bytes.

### 7.3 Item-4 conclusion still holds at the new HEAD

Re-fetched `src/ipc/s1/Unix.cpp` at the new upstream HEAD and at the lane's new
HEAD: the file's upstream bytes are unchanged (last upstream commit touching it
is still `59177602`, 2026-09-02), so `:43-44`, `:118` and `:166` all still hold.

### 7.4 Final re-check at tip `23a0e0f`

HEAD advanced again (`ff81aaf` → `23a0e0f`, three further round-38 records
commits). Re-verified at this tip:

```
$ git rev-parse --short HEAD
23a0e0f

$ grep -oE 'S253 \|.*' corpus/SOURCES.md | grep -oE 'Unix\.cpp:[0-9-]+|[0-9]+ B sha256'
Unix.cpp:43-44
11602 B sha256

$ for f in .ufo/waves/round-38/fetch/*; do printf '%-16s %8d\n' ...; done
  S158.bin            97582
  S187.bin           268731
  S221.bin           306865
  S253.bin            11602
  S277.bin            35421
  stat-sockets.txt     673

$ python3 quality/counters/c2-r38-request-ground.py --repo . --rev HEAD
PRED-C2-r38-v1 entry=corpus/knowledge/request-limits-upstream-r31.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 ids=S253 lineage=5/3 ok=1
PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=23a0e0f91e034527f10f787efab62d8b1e9dbfcb base=f6e3247f73152a39afb86066af48f3cedf95fb0a
```

The fold's repairs hold at this tip: the S253 anchor and byte figure are
correct, and all six registry byte figures still match their receipts. The
counter is unchanged since the freeze commit and still reports `3/3 TARGET_MET`
— i.e. the class defect is still invisible to it, exactly as F9 describes.

**Both residues are still open at this tip.** The S277 row still pins the
non-existent commit:

```
$ grep -oE 'S277 \|.*' corpus/SOURCES.md | grep -oE 'githubusercontent\.com/[^ ]*hyprland-ipc\.md'
githubusercontent.com/chriskearney/chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce/docs/hyprland-ipc.md
```

(the `b8400aa` owner rename kept the dead sha), and r8 still carries the
`:2278` anchor (`grep -c ':2278' corpus/knowledge/request-socket-live-bound-r8.md`
→ `1`). The verified repair for the first is §7.2b: re-pin to
`c37fbe3e439dc27db9ce8176546febb58680dfc5`, whose blob is byte-identical to
`S277.bin` under either owner spelling.

### 7.5 A commit message claims a fix its diff does not contain (tip `5e4c2ba`)

HEAD moved once more to `5e4c2ba` — "round-38 r8 entry fixes (RevEntryBound
F2/F4/F6): short-read break :2279-2280, EVENT framing escape note, stray
directory word". **Only F6 (the stray directory word) is actually in the diff.**
F2 and F4 are named in the message but absent from it:

```
$ git show 5e4c2ba --stat
 corpus/knowledge/request-socket-live-bound-r8.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git show 5e4c2ba | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)'
-directory `directory /run/user/1000/hypr/` carries mode 0700, its sockets
+the instance directory `/run/user/1000/hypr/` carries mode 0700, its sockets
```

That is the whole diff — one line, the F6 wording fix. The F2 anchor is still
wrong in the file at this tip:

```
$ grep -n -o '.\{0,60\}:2278.\{0,60\}' corpus/knowledge/request-socket-live-bound-r8.md
24:readBuffer.data(), 1023)`, `:2278` break on a short read); the request is the
```

and `:2279` has never been introduced into the file at all:

```
$ git log --oneline -S ':2279' -- corpus/knowledge/request-socket-live-bound-r8.md
(empty — never)
$ git log --oneline -S ':2278' -- corpus/knowledge/request-socket-live-bound-r8.md
245065c round-38 data: three request-socket package entries re-grounded ...
```

(The `:2278` string has existed unchanged since the entry was first landed.)

F4 is likewise unapplied: r8 §2 still attributes the framing to S187 with the
plain span, with no escaping note and no pointer to S186:

```
$ awk 'NR==39' corpus/knowledge/request-socket-live-bound-r8.md
**OBS** S187: the event socket's framing is `EVENT>>DATA\n`, and the request
$ grep -c 'S186' corpus/knowledge/request-socket-live-bound-r8.md
0
$ grep -c -i 'escap' corpus/knowledge/request-socket-live-bound-r8.md
0
```

This is not a disagreement about the findings — `RevEntryBound.md`'s F2 and F4
are correct on the evidence I independently verified (§7.2a for the anchor,
and RevEntryBound's own byte check for the escaping). It is a **commit-message
vs. diff mismatch**: a reader who trusts the message will believe F2 and F4
were repaired when the file still carries both defects. Verified to be a
genuine mismatch rather than a message-only slip, since the diff contains no
other hunks and `git log -S ':2279'` shows the corrected anchor was never
committed. Reported to `L1Mado38.RevEntryBound` and `L1Mado38.RevRegistry`.

### 7.6 The F6 revert at `919d7d0` is *required* by the g-clause, not a regression

`RevEntryBound` reports that F6 was reverted by `919d7d0` ("keep S258 Gate
quote verbatim in the transport OBS"). I verified the revert's rationale is
**correct and necessary** — it is not a step backwards.

The `GATE` line pins S258's quote as a byte-exact span:

```
GATE S258 receipt=.ufo/waves/round-38/fetch/stat-sockets.txt sha256=fcc608203f66879f469b61761619e555e04b67127f215d495bd35b9b27421928 quote="directory /run/user/1000/hypr/"
```

and that span is a genuine byte-substring of the receipt (count 1), because the
`stat -Lc '%a %F %n'` output's `%F` field puts the word `directory` immediately
before the path:

```
3	700 directory /run/user/1000/hypr/efb5099…_1792804449_426444678
```

The counter's clause `g` requires that the pinned quote appear **verbatim in the
entry body** (`c2-r38-request-ground.py:221`: `stated = stated or quote in body`).
So the two constraints are in direct tension:

```
g-clause quote-in-body, F6-fixed form ("the instance directory `/run/user/1000/hypr/` …"): False
g-clause quote-in-body, reverted form ("the instance directory — `directory /run/user/1000/hypr/` — …"): True
```

The F6 "fix" (replacing the code span with the bare path) **breaks clause `g`**,
because the pinned quote includes the `directory` word that the fix deleted. The
revert restores clause `g` at the cost of the prose nit RevEntryBound flagged.

That is a genuine conflict between a counter clause and a wording preference —
the kind of interaction worth recording, because the fix that reads better is
precisely the one the gate forbids. The honest resolutions are to change the
`GATE` quote to the bare path (and re-verify it is still byte-present in the
receipt) or to accept the awkward-but-verbatim phrasing. The current tip does
the latter, and the counter still passes:

```
$ python3 quality/counters/c2-r38-request-ground.py --repo . --rev HEAD
PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=9c6e6135049f6754ee9c3f05c33538b024bae332 …
```

**Residue status at tip `9c6e613`** — all three remain open:

```
r8 ':2278' count:                1     (F2 — anchor still wrong)
r8 'S186' refs:                  0     (F4 — escaping note still absent)
r8 'escap' mentions:             0
S277 pin: chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce   (residue B — dead pin)
```

The S253-specific repairs (F1 and the byte-count class) continue to hold at this
tip: the row reads `:43-44` / `11602 B sha256`, all six registry byte figures
match their receipts, and the counter is unchanged since the freeze commit
`58e55ec`.

### 7.7 The entry and the row disagree on how S277 is cited — and only the row is broken

`RevEntryBound` reports that "entry source: line + SOURCES:223 still pin
`707cf7f8` under the `iconidentify` spelling while the row now spells
`chriskearney`". Verifying that precisely, the entry does **not** pin a commit
at all — it cites the repo and path only:

```
entry  (r8:9):  S277 — `iconidentify/chonkstep` `docs/hyprland-ipc.md` (community measurement, tier C)
row (SOURCES:223): https://raw.githubusercontent.com/chriskearney/chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce/docs/hyprland-ipc.md
```

So there are two independent divergences, and the one that is *not* a defect is
the one the entry happens to have:

| | repo spelling | commit | resolves? | bytes == `S277.bin`? |
|---|---|---|---|---|
| entry (r8:9) | `iconidentify` | none | **yes** (at `main`) | **yes** (`cmp` IDENTICAL) |
| row (SOURCES:223) | `chriskearney` | `707cf7f8…` | **no** (404) | n/a — unreachable |

Both owner spellings serve identical bytes at `main` (GitHub preserves the
redirect across the rename), so the entry's uncommitted form is currently
fetchable and byte-exact against the receipt:

```
iconidentify/chonkstep     main: 200 CMP IDENTICAL to S277.bin
chriskearney/chonkstep     main: 200 CMP IDENTICAL to S277.bin
```

The entry's form is nevertheless the weaker citation for a lane whose whole
calibration axis is committed, pinned bytes: it names no commit, so the bytes
it resolves to can move under it. The row's form is the stronger shape but
pins a ref that does not exist, so it resolves to nothing at all.

**The single change that repairs both:** re-pin the row to
`c37fbe3e439dc27db9ce8176546febb58680dfc5` (§7.2b — verified byte-identical to
the receipt) and let the entry cite the same commit, ideally under the
canonical `chriskearney` spelling so the two agree. Alternatively, pin the row
to `main` with a recheck cadence and mark the row as a moving reference — but
that forfeits the pin the lane's recheck cadence depends on.

At tip `c46f868` none of this is applied yet:

```
$ grep -c c37fbe3e corpus/SOURCES.md
0
$ grep -c 707cf7f8 corpus/SOURCES.md
1
$ grep -c '707cf7f8\|c37fbe3e' corpus/knowledge/request-socket-live-bound-r8.md
0
```

Note also that `S187`'s row still carries **no** `sha256` (F5 in
`RevEntryBound.md`), which I re-confirmed at this tip (`grep -c sha256` on the
S187 row → `0`) — and that the counter passes regardless, since clause `c`
checks cell count and shape, not whether the digest is present.

---

## Verdict

| # | Item | Result |
|---|---|---|
| 1 | Pinned fetch ≡ `S253.bin` | **PASS** — byte-identical, sha256 `3ba8e461…`, 11602 B |
| 2 | Constants at `:19-20` | **FAIL** — they are at `:43-44`; `:19-20` is `using namespace IPC::Socket1;` + blank. Registry row only; entry body unaffected |
| 3 | `readRequest` check `:118`, `addFollowData` `:166` | **PASS** — both exact, both inside the named functions |
| 4 | Constants still exist at upstream head | **PASS** — unchanged since 2026-09-02; pinned bytes ≡ HEAD bytes. Note: no `master` branch exists (default is `main`); `master` in raw URLs is a fallback alias to `main`. Pinned commit is 4 commits behind HEAD, so "current upstream" is stale phrasing |
| 5 | Host handler has no byte bound (the contrast) | **PASS on substance.** `src/debug/HyprCtl.cpp` does not exist at the pinned commit (404; client moved to `hyprctl/src/main.cpp`), but the entry's actual contrast is against the **host's** v0.56.2 `HyprCtl.cpp`, whose request loop (`:2271-2281`) accumulates 1023-byte chunks with **no** total ceiling — confirmed, and `S158.bin` matches the host-tag fetch |
| 6 | 64 KiB characterization | **PASS** — traced to chonkstep (S243/S277 `:61`), a third-party server's own caps; upstream's request ceiling is 1 MiB. S187 contains no "64 KiB" |

**One defect found: F1** (`corpus/SOURCES.md:221` locator `:19-20` → `:43-44`),
plus a same-row byte-count slip (`39464 B` → `11602 B`) and a stale
"(current upstream)" phrase. No defect in the entry body
`corpus/knowledge/request-limits-upstream-r31.md`; every substantive claim in it
that I could test — the two constants, their values, both check sites, the
no-byte-bound contrast against the host, the later-revision caveat, and the
64 KiB correction — verified against the fetched bytes.

**Disposition at current HEAD (`c46f868`): F1 and the byte-count slip are
repaired** by the seat-fix fold `b8400aa` (§7.1) — the row now reads `:43-44`
and `11602 B`, and all six registry byte figures match their receipts (§7.4).
Two residue items from the same class remain open at this tip and are reported
to their owners: the r8 entry's `:2278` anchor, which points at
`request += recvd;` rather than the break at `:2280` (§7.2a), and the S277
row's pinned-commit URL, which names a commit that does not exist in the
repository — a dead pin the fold renamed but did not repair (§7.2b). The
verified repair for the latter is re-pinning to `c37fbe3e…`, whose blob is
byte-identical to the committed receipt under either owner spelling.

**Bounds honored**: read-only on all lane production files; writes limited to
this report and `/tmp/mado38-ScoutS253/`. No git mutation in the lane; no
sandbox clone was needed (all fetches are read-only `curl` to `/tmp`; the two
`git` probes used disposable `mktemp -d` repos with `rev-parse --show-toplevel`
verified to equal the temp dir before use). No Hyprland socket was connected; no
compositor, config, service or package was touched. No subagent dispatched. No
tools installed.
