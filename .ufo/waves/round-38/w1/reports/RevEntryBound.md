# RevEntryBound — sentence-level audit of `corpus/knowledge/request-socket-live-bound-r8.md`

Round 38, wave 1. Scope: every quoted span and file:line citation in the entry checked
byte-verbatim against the committed round-38 receipts, plus the fairness of the declared
amend of `ipc-contract-r25.md`. Lane files untouched; no tool installs; scratch was
in-kernel only (no files written outside this report).

## Method

- Python bytes-in checks of every quoted span against `.ufo/waves/round-38/fetch/`
  receipts (`S158.bin`, `S187.bin`, `S277.bin`, `stat-sockets.txt`), with line-number
  location of each hit.
- sha256 of all five round-38 receipts, compared against the `SOURCES.md` rows
  (`corpus/SOURCES.md:170,199,220-223`) and, for the byte-identical re-fetch claims,
  against the earlier-round receipts (`.ufo/waves/round-24/fetch/S158.bin`,
  `round-26/fetch/SrcHyprctlAnims.bin`, `round-32/fetch/S187.bin`).
- S158 handler read in full (`:2239-2346`) for the "no byte bound anywhere in the
  handler" claim; package original read at
  `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/request-socket-live-bound-r8.md`
  for the re-grounding/corrections claims; `ipc-contract-r25.md` §1-§3 read for the amend.

## Verified (PASS)

1. **`:2264` poll** — `int ret = poll(pollfds, 1, 5000);` is byte-verbatim and sits
   exactly at S158.bin line 2264. PASS.
2. **`:2266-2268` close on `ret <= 0`** — 2266 `if (ret <= 0) {`, 2267
   `close(ACCEPTEDCONNECTION);`, 2268 `return 0;`. PASS.
3. **`:2274` read** — `read(ACCEPTEDCONNECTION, readBuffer.data(), 1023)` byte-verbatim
   at S158.bin:2274 (quoted span is an exact substring of that line). PASS.
4. **S187 synchronous-evaluation sentences** — `Hyprland evaluates connections to this
   socket completely synchronously,` byte-verbatim at S187.bin:2855 (line ends at that
   comma); `will cause Hyprland to freeze` byte-verbatim at :2856 (inside `<em>` tags;
   inner text exact). PASS.
5. **S187 request grammar** — `[flag(s)]/command args` byte-verbatim at S187.bin:2850
   (inside `<code>`). PASS. (Note: S187 renders it lowercase `basically, write`; the
   entry quotes only the code span — fine.)
6. **S277** — `There is no length prefix or newline.` byte-verbatim at S277.bin:84;
   `[[BATCH]]` and `;` separators both in :85 ("Batch requests\nstart with `[[BATCH]]`
   and use `;` separators."). The entry's paraphrase is fair and its quoted spans are
   exact. PASS.
7. **stat-sockets / S258 modes** — receipt lines: `700 directory
   /run/user/1000/hypr/efb5099..._1792804449_426444678`, `755 socket .../.socket.sock`,
   `755 socket .../.socket2.sock`. The entry's 0700-dir / 0755-sockets claim matches.
   PASS on modes (path wording defect below, F6).
8. **"the host's own commit"** — the instance directory in the stat receipt embeds
   `efb50993780079460b0cbed1363e2166a2de1d9f`, the same commit S158 cites. PASS.
9. **"no byte bound anywhere in the handler"** — `REQUEST_LIMIT`, `1 << 20`,
   `1048576` all count 0 in S158.bin; handler `:2242-2319` accumulates chunks into
   `request` with no size check. PASS.
10. **Byte-identical re-fetch claims** — S158: round-38 receipt sha256
    `798b7c6c…47b91fa` equals `round-24/fetch/S158.bin` and
    `round-26/fetch/SrcHyprctlAnims.bin`; S187: round-38 receipt sha256
    `136e5511…f6a37a4` equals `round-32/fetch/S187.bin`. S277 exists only in round-38
    (first fetch). PASS.
11. **Amend of `ipc-contract-r25.md` is fair** — r25 §1 indeed names the five-second
    timeout only from prose (S186:21-23 basis, "the five-second timeout" in its INF) and
    reads code solely for the event socket (S189, EventManager.cpp); it never opens
    HyprCtl.cpp. The r8 entry's INF (temporal bound; unclosed connection blocks until
    the timeout) is mechanism-compatible with r25's INF ("queued no-ops until the
    timeout") and adds the implementation read without contradicting it. FAIR. PASS.
12. **Package re-grounding honesty** — package cited S272 (tag-URL HyprCtl.cpp), S276
    (0.56.0 IPC page), S277 (chonkstep `main`); landed entry re-points to pinned rows
    S158 (commit URL), S187, S277 (pinned commit `707cf7f8`), exactly as its
    "Corrections applied while re-grounding" paragraph states. S277 kept at tier C
    (SOURCES row S277: tier C). PASS.

## Findings (by severity)

### MEDIUM

- **F1 — SOURCES.md byte-size fields are false for every new round-38 row, including
  the two rows this entry cites.** `corpus/SOURCES.md:222` (S258) records "receipt
  1401 B" but `fetch/stat-sockets.txt` is 673 B; `:223` (S277) records "19737 B" but
  `fetch/S277.bin` is 35,421 B. Same defect class in sibling rows: S221 "35046 B" vs
  actual 306,865 B (`:220`), S253 "39464 B" vs actual 11,602 B (`:221`). In all five
  cases the sha256 recorded in the row matches the committed receipt exactly — only the
  byte-size figures are wrong — so the digest binding the round relies on holds, but
  each Gate line states a false size for its own receipt. Read-only bound: not fixed by
  me; the lane should correct the four size fields.
  Evidence: computed sizes/digests — S158.bin 97,582 B `798b7c6c…47b91fa` (row correct),
  S187.bin 268,731 B `136e5511…` (row records size, no digest — see F4), S221.bin
  306,865 B `35046ba0…5d30a` (row size wrong), S253.bin 11,602 B `3ba8e461…d6cf` (row
  size wrong), S277.bin 35,421 B `ff561fe0…781e6` (row size wrong), stat-sockets.txt
  673 B `fcc60820…b27421928` (row size wrong).

### LOW

- **F2 — wrong line anchor for the short-read break.** Entry §1: "`:2278` break on a
  short read". S158.bin:2278 is `request += recvd;`; the short-read break is the
  condition at :2279 (`if (messageSize < 1023)`) and `break;` at :2280. (The other
  break, on `messageSize < 1` at :2275-2276, is an EOF/error break, not a short read.)
  The claim's content is correct; the anchor is off by two lines and, in a lane whose
  calibration axis treats line anchors as canonical, must be corrected to `:2279-2280`.
- **F3 — S258 cited but absent from the entry's `source:` line.** §2 OBS opens
  "**OBS** S258: on this host the transport is equally modest …" while `source:` lists
  only S158, S187, S277. Both siblings list their cited rows (`hyprctl-flags-r28.md`
  lists S221; `request-limits-upstream-r31.md` lists S253), the SOURCES S258 row's
  used-by names this entry, and LOG.md's round-38 data line records the entry as
  "(S158/S187/S258/S277)". The `source:` line should carry S258.
- **F4 — `EVENT>>DATA\n` is not byte-verbatim in the cited receipt.** §2 attributes the
  event framing to S187; S187.bin's only occurrence is the HTML-escaped
  `<code>EVENT&gt;&gt;DATA\n</code>` (:2864) — the plain span `EVENT>>DATA\n` has zero
  byte-occurrences in S187.bin. The unescaped form is byte-verbatim in the round-32
  raw-markdown receipt S186 (`EVENT>>DATA\n` count 1). Semantically true of the
  document, and the r25 Gate already recorded the rendered form, but against this lane's
  own verbatim standard the cite should either point at S186 for the literal span or
  note the escaping.
- **F5 — "sha256 in the round-38 Gate block" is only three-quarters true.** The entry's
  corrections paragraph points at sha256 evidence; SOURCES rows carry sha256 for S158,
  S258 and S277, but the S187 row (`corpus/SOURCES.md:199`) records only "268731 B"
  with no digest. The byte-identity itself is real (I verified round-32 vs round-38
  digests match), so the claim is true while its recorded evidence for S187 is
  size-only. Adding the S187 digest to the row closes it.
- **F6 — imprecise path in the S258 sentence.** "the instance directory `directory
  /run/user/1000/hypr/` carries mode 0700" — the receipt measured the instance
  directory `/run/user/1000/hypr/efb5099…_1792804449_426444678`, not its parent
  `/run/user/1000/hypr/` (never stat'ed), and the code span mixes in the stat output's
  `%F` field word "directory". Modes as claimed are otherwise exact.

### INFO

- **I1 — the title slightly overstates the bound's completeness.** The poll's 5 s bounds
  only the wait for the first byte; the chunk loop that follows has no timeout and
  continues while full 1023-byte chunks keep arriving (any read < 1023 breaks), so a
  client streaming full chunks can hold the handler open past five seconds with no byte
  cap — the temporal claim is true for the idle/unclosed case the entry quotes
  (S187:2855-2857), and the entry's UNK already declares the practical bound unmeasured.
  No quoted statement is falsified; noting for the record.

## Residual risk / verification gaps

- **Tag↔commit equality not verifiable offline**: "same bytes as the package's
  tag-URL citation" (package S272 used `…/v0.56.2/src/debug/HyprCtl.cpp`; lane fetched
  `…/efb5099…/src/debug/HyprCtl.cpp`) rests on v0.56.2 = `efb5099…`. Strongly supported
  by the host's instance dir embedding that commit id and by ~20 registry rows asserting
  the mapping, but no offline receipt pins the tag object. A one-line `git ls-remote`
  equivalence check would close it.
- SOURCES S253 row contains a garbled cross-reference ("receipt …
  fetch/S187.bin is unrelated - see S187") — sibling scope (request-limits-upstream-r31
  reviewers), flagged here because it sits in the same Gate block this entry's
  corrections paragraph points to.
- All receipts are committed bytes; I did not re-fetch over the network (bounds: no
  unnecessary network; digests anchor everything).
