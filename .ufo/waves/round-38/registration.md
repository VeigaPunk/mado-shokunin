# mado round 38 — registration (frozen before any round-38 data)

Base: `f6e3247f73152a39afb86066af48f3cedf95fb0a` (lane `master` at round start; attempt 1).
The watchdog shows no `lane-dead-no-report mado round=38`; nothing is inherited. This file,
the three counters, the discrimination gate and its frozen manifest, the fetch receipts, the
live triplet and the assimilation scratch land in one freeze commit; any later change to a
counter is a new predicate and the claim it belongs to then fails as declared.

## Lowest-axis rule

`python3 -I quality/check-axis-scores.py --repo . --rev master` at the base prints
`navigation published=52/52`, `calibration published=50/50`, `operability published=12/12`,
`MADO_AXIS: checked=3 mismatched=0` (`receipts/axis-base.txt`) — every published axis ties at
its maximum, so each is a lowest axis; C1 works `calibration`, C2 works `coverage`. The
stagnation nudge does not apply (the event-socket census capability entered in round 37,
inside the lane's window of 3).

## Routed defect being worked

`corpus/lessons/round-37.md` M37-5 (kept on the routed-defect queue by the round-37 non-author
closure `corpus/lessons/round-37-verifier-spotcheck.md` §6): both frozen round-37 counters are
crib-reachable — C1 by a 19-line self-receipt tree (no source opened), plus quote floor,
duplicate row and verbatim-refused holes; C2's live clause by the counter's own fixture
committed as the snapshot, plus undiscriminated `lagging` and `--expect-client` and a read-only
clause that both bypasses (`import socket`) and false-misses (`connect(` in a docstring).
The routed v3 design: re-fetch digest binding, a `/proc` inode cross-check, discriminating
cases. This round implements exactly that.

## C1 — calibration: the two round-37 counters are repaired to v3 and shown to discriminate

- **Deliverables:** `quality/counters/c1-r38-event-ground.py` (`PRED-C1-r38-v3`) and
  `quality/counters/c2-r38-eventq.py` (`PRED-C2-r38-v3`) — the v2 instruments repaired:
  Gate receipts bound to the `fetch/` pin table by (path, sha256) (re-fetch digest binding),
  a located-quote floor, unique registry rows, parsed header values, a lineage floor for the
  package ground, four new discriminating fixture cases (clients-first, no-users,
  comm-spaces, expect-present) plus a `lagging=0` assertion, a comment/docstring-aware
  read-only clause, and a three-artifact live clause (receipt + full-table `ss` snapshot +
  committed `/proc` binding with `ss_sha256` and `OVERALL: AGREE`).
- **Predicate:** the docstring of `quality/check-r38-discrimination.py` and the frozen
  manifest `.ufo/waves/round-38/controls/manifest.json` (`MANIFEST-r38-v1`, 19 controls).
- **Counting command:**
  `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-r38-discrimination.py --c1 <counter> --c2 <counter> --manifest .ufo/waves/round-38/controls/manifest.json --rev <data-rev>`
- **Before:** the same manifest scored with the frozen v2 counters
  (`--c1 quality/counters/c1-r37-event-ground.py --c2 quality/counters/c2-r37-eventq.py`) —
  the cribs pass where they should fail, so `correct<19 verdict=TARGET_MISSED`, exit 1.
  **Target:** the v3 counters score `correct=19/19 verdict=TARGET_MET`, exit 0.
- **Kill rule:** anything other than `correct=19/19` at the measured lane tip is a miss,
  reported as an honest stop; no target narrowing.
- **Residual (declared, not hidden):** fully fabricated self-consistent artifacts (invented
  lineage phrases; invented inode triples) still pass — the same accept-path tradeoff the
  round-37 clause test recorded. The v3 counters raise the crib from trivial (a one-line
  self-receipt; a committed fixture file) to fabricating consistent sets; they do not make
  live truth provable from committed bytes.

## C2 — coverage (assimilation + sourced): three request-socket contract entries land on unheld ground

- **Predicate `PRED-C2-r38-v1`** — the docstring of `quality/counters/c2-r38-request-ground.py`;
  the code is the same sentence. Target set (frozen):
  `corpus/knowledge/hyprctl-flags-r28.md` (tokens `flag list`, `select instance`),
  `corpus/knowledge/request-socket-live-bound-r8.md` (tokens `poll(pollfds`, `1023`),
  `corpus/knowledge/request-limits-upstream-r31.md` (tokens `REQUEST_LIMIT`,
  `FOLLOW_QUEUE_LIMIT`).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev <rev>`
- **Before** (at base): `admitted=0/3 verdict=TARGET_MISSED`, exit 1.
  **Target:** `admitted=3/3 verdict=TARGET_MET`, exit 0.
- **Kill rule:** as C1.
- **Sourced:** every cited row is a `SOURCES.md` row opened this round — S158 and S187
  re-fetched byte-identical (documents the package called S272 and S276; ids follow
  documents), S221, S253, S277 and the host stat receipt fetched/read 2026-10-25 — each with
  a Gate line binding a committed receipt by sha256 and a located quote.
- **Unheld ground (checked 2026-10-25):** `git grep` at the base finds no `flag list`,
  `select instance`, `poll(pollfds`, `REQUEST_LIMIT`, `FOLLOW_QUEUE_LIMIT`, `length prefix`
  or `BATCH` in `corpus/knowledge` — the flags, the accept-loop bound and the upstream
  ceilings are new edge classes under the held IPC contract (`ipc-contract-r25.md` holds the
  prose contract; the 5000 ms poll and the ceilings were never read).

## Assimilation (rides C2; no extra claim)

Package `/home/vgpnk/Projects/shokuknow/merge/mado/` (read-only). One theme: **the request
socket's operational contract**. Five package entries considered.

- **Admit, re-grounded:** `hyprctl-flags-r28.md` (S221), `request-socket-live-bound-r8.md`
  (S272→S158, S276→S187, S277), `request-limits-upstream-r31.md` (S253; `src/ipc/s1/Unix.cpp`
  404s at the host tag — the ceiling is upstream-ahead, and the entry must say so).
- **Refuse:** `socket-client-contract-measurements-r29.md` — its load-bearing numbers
  conflict with first-party ground this round re-opened: "requests capped at 64 KiB" vs the
  compositor's own `REQUEST_LIMIT = 1 MiB` / `FOLLOW_QUEUE_LIMIT = 64 KiB` (S253), and
  "sockets are 0600" vs this host's measured 0755 in a 0700 directory
  (`fetch/stat-sockets.txt`). Flip: an upstream cite for 64 KiB as a request cap and a host
  where the sockets stat 0600.
- **Refuse:** `socket-modes-and-request-read-r30.md` — its cited own-work source (instance
  `_1792772698_564628331`) no longer exists on the host (stale artefact); the modes it
  reports are re-measured by this round's stat receipt and live in E4's OBS instead.
  Flip: a fresh own-work source covering the same facts.

Id collisions and the renumber map live in `assimilation/` (reg-ids 207, staged-ids 147,
collisions 15: S203–S217); ids follow documents, never arithmetic. New rows continue the
lane's S-space: S221, S253, S258 (own-work stat receipt, cited by E4), S277; S272 and S276
re-point to S158 and S187. Quarantine: the mado slice is 13 rows (6 `payload-absent`,
7 unchecked); no adopted citation's document is among them — S189 (round1) was hand-checked
last round (present at `:128`); the remaining 12 name documents no admitted entry cites and
stay unappended.

## Separability

C1 reads only `quality/` instruments, the frozen manifest and sandbox clones. C2 reads only
`corpus/` files and `fetch/` receipts. No C2 entry cites the counters or the receipts they
score; the counters read no C2 entry. Each is measurable with the other's files deleted.

## Controls (do-nothing and cribs, scored with the frozen predicates before data)

The manifest itself is the control set: `c1-donothing` (round-37 base), `c1-selfreceipt`,
`c1-quotefloor`, `c1-duprow`, `c1-nolineage`, `c1-r28-verbatim`, `c1-token-stub`,
`c1-clause-b` (all reject; `c1-live` accept) and `c2-donothing`, `c2-forged`, `c2-impsock`,
`c2-lagconst`, `c2-missall`, `c2-onepass`, `c2-stub-clean`, `c2-proc-mismatch` (reject),
`c2-live`, `c2-docconn` (accept). For C2's domain counter the cheapest do-nothing control is
the base run itself (`admitted=0/3`); crib controls ride wave-1 seats (junk rows, wrong
digest, self-receipt, stated-quote stub, unindexed, refused-paste).

## Not claimed

No axis score change is claimed by either counter; no socket is connected, no request is
sent, no config, service or compositor state is touched; `/home/vgpnk/Projects/shokuknow`
and `considerthese/` are read-only.
