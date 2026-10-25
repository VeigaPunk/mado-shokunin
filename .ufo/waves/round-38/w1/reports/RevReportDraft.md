# RevReportDraft — round-38 report skeleton + evidence-pointer audit (wave 1)

Scope: draft the round-38 report skeleton (every contract-§4 section, evidence
pointer per slot) and audit the pointers it must cite. Skeleton delivered at
`/tmp/mado38-RevReportDraft/mado38-skeleton.md`. Read-only elsewhere; no lane
production file touched.

## What I attacked and the exact commands

1. Commit chain: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%h %s' -8`
2. Receipt existence: `for f in <each registration-cited path>; do [ -e "$f" ] …` under
   `.ufo/waves/round-38/`
3. Gate quotes vs receipt bytes: `grep -cF '<quote>' <receipt>` for all six GATE lines
4. SOURCES rows: `grep -nE '^\| S(221|253|258|277|158|187)[[:space:]]*\|' corpus/SOURCES.md`
5. Domain counter reproduction: `python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev 3f14bd2d7c3aa067091bc52e63fb8abdd944c3b8`
6. Registration, LOG.md:2297+, SCORECARD round-38 rows (:200-201, :2409-2420),
   `corpus/lessons/round-38.md` (whole), both discrimination receipts, `before-c2.txt`,
   `axis-base.txt`, `census-before.txt` — read and cross-checked.

## PASS items (evidence audited)

- **Commit hashes PASS.** `git log -8` at audit time printed, top-down: `f0c9432`,
  `b6c1d31`, `859d0cf`, `efb0ec2`, `245065c`, `58e55ec`, `32c3ea3`, `f6e3247`. During
  the audit the tip moved: `bb1adce` (scorecard records) and `3f14bd2` (RevCommitChain
  F1–F3 errata) landed; full hashes pinned (`git rev-parse master` →
  `3f14bd2d7c3aa067091bc52e63fb8abdd944c3b8`). The round span is 7 commits,
  `58e55ec9e905c85fb5a794f9a51dc06cc16166ba` (freeze, full hash verified) → tip.
- **Receipt existence PASS.** All registration-cited receipts exist:
  `registration.md`, `controls/manifest.json`, `receipts/{axis-base,census-before,
  before-c2,before-discrimination-v2,after-discrimination-v3,eventq-live,
  eventq-live-proc,eventq-live-ss}.txt`, `fetch/{S221,S253,S277,S158,S187}.bin`,
  `fetch/stat-sockets.txt`. Two of my own probe names were correctly absent:
  `receipts/before-c1.txt` (C1's before is the v2 discrimination run, not a c1 counter
  run) and `fetch/S258.bin` (S258 is the own-work stat row; its receipt IS
  `stat-sockets.txt`, per SOURCES.md:222 and Gate line S258).
- **Gate quotes PASS.** All six quotes verbatim in receipt bytes: `grep -cF` = 1 for
  `static constexpr size_t REQUEST_LIMIT` (S253.bin), `select instance (id or index in
  hyprctl instances)` (S221.bin), `int ret = poll(pollfds, 1, 5000);` (S158.bin),
  `There is no length prefix or newline.` (S277.bin), `directory /run/user/1000/hypr/`
  (stat-sockets.txt), `evaluates connections to this socket completely synchronously`
  (S187.bin). sha256 pins present in each GATE line (`corpus/lessons/round-38.md:10-16`).
- **Registry rows PASS.** S221/S253/S258/S277 exist at `corpus/SOURCES.md:220-223`;
  S158:170 and S187:199 carry the used-by extension. Row count now **211**
  (`grep -cE …` = 211), i.e. 207 → 211 with the four new rows.
- **Verdict receipts quote cleanly.** `before-discrimination-v2.txt` last line:
  `MADO_R38_DISCRIMINATION: controls=19 correct=13/19 verdict=TARGET_MISSED`;
  `after-discrimination-v3.txt` last line: `… correct=19/19 verdict=TARGET_MET`;
  per-control lines show exactly the six v2 flips (`c1-duprow`, `c1-nolineage`,
  `c1-r28-verbatim`, `c2-forged`, `c2-docconn`, `c2-proc-mismatch`) going ok=1 after.
  `before-c2.txt`: `PRED-C2-r38-v1 admitted=0/3 verdict=TARGET_MISSED
  rev=f6e3247…exit=1`. `axis-base.txt`: all three axes MATCH at
  `rev=f6e3247f73152a39afb86066af48f3cedf95fb0a`.
- **Domain counter reproduces at tip.** Run of
  `python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev 3f14bd2d…`:
  `admitted=3/3 verdict=TARGET_MET`, exit 0, per-entry lines all ok=1 with ids
  `S221`, `S158,S187,S277`, `S253`. Consistent with SCORECARD.md:2413 ("at efb0ec2").

## Findings

- **F1 (HIGH, conformance — frontier step open): no mined mistake yet.**
  `corpus/lessons/round-38.md` has sections `## Gate` (:10), `## Assimilation ledger`
  (:26), `## Findings` (:49) — **no `## Mistakes` section and no `M38-` id**
  (`grep -n 'M38-'` empty). Contract §2b item 3 requires mining one mistake or
  pasting the found-none sweep. Obvious candidate with evidence in hand: the
  freeze-discipline failure (counter patched post-freeze `859d0cf`, manifest
  post-data `b6c1d31` ⇒ frozen C1 fails as declared, 18/19) — captured-by: the
  registration's freeze clause ("any later change to a counter is a new predicate and
  the claim it belongs to then fails as declared"); fix: the errata + re-registration
  routing; shown able to fail: the 18/19 receipt.
- **F2 (MEDIUM): no committed after-receipt for the domain counter.** The 3/3 after
  run exists only as a SCORECARD citation (":2413 … at efb0ec2") and a LOG phrase
  (:2307); `receipts/` holds only `before-c2.txt` for `c2-r38-request-ground.py`. The
  report contract wants a pasteable counting command + output per claim: commit an
  after receipt at the final tip (my tip run's output is reproducible; I did not write
  one — that would be a lane production edit).
- **F3 (MEDIUM, record integrity): refusal set mismatch between frozen registration
  and landed ledger.** `registration.md` §Assimilation refuses TWO package entries:
  `socket-client-contract-measurements-r29.md` and `socket-modes-and-request-read-r30.md`
  (stale own-work source `instance _1792772698_564628331`; flip: a fresh own-work
  source covering the same facts). The lesson ledger (:26-45) records three refuse
  rows — the two event-queue null-channel entries and r29-client — and **no r30 row**;
  its facts were folded into S258 / `request-socket-live-bound-r8.md` §2 instead.
  LOG.md:2307 compounds it: "two refusals stand (null-channel r28/r29, the
  64 KiB-as-request-cap r29 draft)" names three things under "two". Repair: add the
  r30 refusal row with reason + flip (or an explicit fold-in note), and fix the LOG
  count.
- **F4 (LOW, wording):** `corpus/lessons/round-38.md` ledger says "The three adopted
  new ids (S221, S253, S277, S258) were free" — four ids after "three" (same class as
  round-37's CritEntryE2 corrections).
- **F5 (INFO, SCORECARD structure):** `bb1adce` moved the round-38 rows out of the
  rollout-snapshot capabilities table (now `— none yet —`, SCORECARD.md:203-205) into
  `### Capabilities (round 38)` (:2409-2420) — but that section carries only the
  `request-socket admission` row; the former `counter-discrimination audit` row
  survives in no capabilities table. If AXES.md §Capabilities credits it, restore it
  into the round-38 section or record why not — the closure will look.
- **F6 (INFO, instrument provenance):** the two discrimination receipts are not the
  same instrument: before 13/19 = frozen **v2** counters × original manifest; after
  19/19 = **v3** counters × manifest as fixed at `b6c1d31`; and at the frozen pair
  (`58e55ec`) the gate scores **18/19** (errata). The report's Before→after table
  must state all three numbers with which-instrument qualifiers or the closure reads
  it as an inconsistency.
- **F7 (INFO, claim count):** the lesson's round-intent line (:4-6) says "three
  claims — C1, C2, C3 (the live triplet)"; the frozen registration declares two
  claims and makes the live triplet a C1 deliverable. Pick one phrasing in the
  report; claim-count drift is closure bait.

## Residual risk / verification gaps

- I did not re-run the 19-control discrimination gate (needs sandbox clones; receipts
  + RevCommitChain/LabratProcProof cover it) nor the C1 counter itself.
- `census-after`, harm watch at tip, misroot sweep, and the wave's final seat counts
  are round-end items — slots are marked [TO RUN/TO RECORD] in the skeleton.
- Tool installs: none.

Skeleton: `/tmp/mado38-RevReportDraft/mado38-skeleton.md` — fills every contract-§4
section for this round with the audited pointers above.
