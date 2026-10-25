# RevLessonGate — audit of `corpus/lessons/round-38.md` (mado round 38, wave 1)

Scope: the six `GATE` lines (digests, quotes, word floor), the assimilation ledger table
against `assimilation/` + the staged register, the three refusal characterizations against
the package files, and the claims paragraph against the frozen `registration.md`.
Lane read-only; no lane state touched. HEAD audited: `bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5`
("round-38 scorecard: move-log rows + capabilities section"); `git ls-tree` confirms
`corpus/lessons/round-38.md`, all six `fetch/` receipts and all four `assimilation/` files are
in that commit; working tree clean except untracked `w1/scratch/`.

## Verdict

GATE block and refusal characterizations: **PASS** (one wording defect, L1).
Assimilation ledger: **FAIL** — four high-severity defects (H1–H4); the ledger's collision
and register claims are contradicted by the staged register it summarizes.
Claims paragraph: **MISMATCH** vs frozen registration (M1); one declared refusal missing
from the ledger (M2).

## PASS items (evidence)

1. **Digests.** `sha256sum .ufo/waves/round-38/fetch/*` reproduces all six GATE sha256 values exactly:
   ```
   798b7c6c…47b91fa  S158.bin      136e5511…4f6a37a4  S187.bin
   35046ba0…451879d30a S221.bin    3ba8e461…778f4833d6cf S253.bin
   ff561fe0…451879d30a — see raw below
   fcc60820…27421928  stat-sockets.txt
   ```
   (raw: `798b7c6c4c16…`, `136e5511fba5…`, `35046ba0dc1d…`, `3ba8e461bd46…`,
   `ff561fe0d096…`, `fcc608203f66…` — each identical to its GATE line.)
2. **Quotes.** Python check `quote.encode() in blob` over every GATE line: 6/6 verbatim in the
   receipt bytes, 6/6 verbatim in the citing entry (`hyprctl-flags-r28.md`,
   `request-socket-live-bound-r8.md`, `request-limits-upstream-r31.md` — all present in the
   lane), 6/6 verbatim in the lessons body. Word counts 6/7/8/8/2/7 — all ≤25, all >1 token,
   no bare ids. The lessons' claim "Every quote is verbatim in its receipt bytes and in the
   citing entry body" holds.
3. **Re-fetch byte-identity (S272→S158, S276→S187).** The round-38 receipts are byte-identical
   to the original held receipts:
   ```
   798b7c6c…  .ufo/waves/round-24/fetch/S158.bin   ==  round-38/fetch/S158.bin
   136e5511…  .ufo/waves/round-32/fetch/S187.bin   ==  round-38/fetch/S187.bin
   ```
   "adopt — byte-identical to held S158/S187" is verified against the originals, not just asserted.
4. **Staged-row digest prefixes.** Staged `SOURCES.append.md` rows S221 ("sha256 prefix
   `35046ba0dc1dd1db`") and S253 ("sha256 prefix `3ba8e461bd466a8a`") match the committed
   receipts — the adopted ids follow the same documents the package staged.
5. **S221 HTML claim.** `grep -o` in S221.bin: `i -&gt; select instance (id or index in hyprctl instances)`
   — the "the `>` arrow is `&gt;` in the HTML" parenthetical is exact.
6. **Refusal characterizations (all three substantively accurate).**
   - `event-queue-host-measurement-r28.md`: "never overflowed" is exactly its title/INF; the
     null-channel ground is round-37's `event-queue-observability-r37.md` (`debug:disable_logs`
     defaults on, S215; "the zero counts are a null channel, not a measurement", §3; §4 refuses
     precisely this package reading). Its source instance `_1792772698_564628331` is stale
     (this round's stat shows the instance dir has rolled to `_1792804449_426444678`).
   - `event-queue-journal-measurement-r29.md`: same null channel — r37 §3: the unit journal
     "carries 4 start-up `Using config` lines and none of the runtime log"; r37 made the
     journal measurement (probe string 7× in log, 0× in journal). See L1 for the garbled figure.
   - `socket-client-contract-measurements-r29.md`: quotes "Requests are capped at 64 KiB" and
     "0700 … 0600" from chonkstep; S253 pins `REQUEST_LIMIT`/`FOLLOW_QUEUE_LIMIT`, so 64 KiB is
     the followed-queue bound; `stat-sockets.txt` measures `700 directory` / `755 socket` ×2 on
     this host — the supersession claim is correct.
7. **Register/free-id claims that do hold.** `reg-ids` = 207 rows ending S217 (registration's
   "reg-ids 207" ✓); S221/S253/S258/S277 are free in the *held* register; held rows jump
   S217 → S221 ✓ (lessons open item 3 correct for the held register); `collisions` = exactly
   S203–S217 (15) ✓ as a file; `staged-ids` = 147 ✓; `quarantine-slice` = 13 rows
   (6 `payload-absent`, 7 unchecked) ✓.
8. **Lane-row column.** `request-socket-live-bound-r8.md` source line pins S158, S187, S277,
   S258; §2 carries the S277 and S258 OBS — matches the ledger's "lane row / entry" column.

## Findings — HIGH (assimilation ledger)

- **H1 — "Id collisions … all in the refused register's block" is false.** The staged rows
  S203–S217 cite: `ipc-contract-r25.md` (S203, S204, S206), `dispatcher-semantics-r25.md`
  (S205), `waybar-module-text-route-r25.md` (S207, S208), `two-literature-coverage-r25.md`
  (S209–S211), `two-literature-drift-r26.md` (S212, S215–S217),
  `dispatcher-surface-and-request-grammar-r26.md` (S213), `host-bar-and-idle-binding-r26.md` +
  `event-delivery-limits-r26.md` (S214). The four refused entries' register rows are S226,
  S242, S243, S252 — none in S203–S217. Not one collided row belongs to a refused entry.
- **H2 — "The staged register … its rows covered only the refused entries" is false.** The
  147-row register covers ~69 entries across every theme (idle-lock, focus-grab, gkeep,
  two-literature, waybar, weather, update-check…). The refused four account for 4 of 147 rows.
- **H3 — The round created an id collision at S258 and the ledger denies it.** Staged S258 is
  "Hyprland (ArchWiki, English) — the diff against the revision the Chinese translation was
  synced from" (`oldid=887257`, used-by `chinese-translation-drift-r31.md`). The lane's new
  S258 is the own-work stat receipt (`corpus/SOURCES.md:222`). That ArchWiki-diff document is
  held nowhere in the lane (`grep 887257|882352 corpus/SOURCES.md` → 0 hits) and
  `chinese-translation-drift-r31.md` was not adopted (0 files), so the staged S258 row still
  needs an id — which the lane has now given to a different document. `collisions` records only
  S203–S217, and the lessons claims "The three adopted new ids (S221, S253, S277, S258) were
  free" — false with respect to the staged register. Assimilating the register later will
  collide at S258.
- **H4 — The ledger's sixth row cites a staged id that does not exist.** "S212a → S258" —
  `S212a` appears in neither `staged-ids` (S203–S349 contiguous), the package, nor
  `collisions`. Lane S258 is a new own-work row (registered this round), not a staged remap;
  the "Staged id →" column is fabricated for this row. Same sentence also counts four ids as
  "The three adopted new ids (S221, S253, S277, S258)".

## Findings — MEDIUM

- **M1 — The claims paragraph does not match the frozen registration.** Lessons: "three claims
  — C1 (v3 re-grounding counter …), C2 (request-socket admission …), C3 (the live triplet …)".
  Registration declares **two** claims: C1 = *both* round-37 counters repaired to v3 and shown
  to discriminate (calibration; the three-artifact live triplet is a C1 deliverable, not a
  claim), C2 = request-ground coverage. The lessons drops the eventq counter
  (`c2-r38-eventq.py`) from the claim enumeration entirely and promotes its live clause to a
  standalone claim C3.
- **M2 — A registration-declared refusal is missing from the ledger.** Registration refuses
  `socket-modes-and-request-read-r30.md` (stale own-work source instance
  `_1792772698_564628331` — verifiable: the package entry's source line cites exactly that
  instance, and this round's stat shows the directory has rolled to
  `_1792804449_426444678`). The lessons table has no row for it; its "refuses the other two"
  text disagrees with its own three-row refuse list, of which two rows (the event-queue pair)
  are outside the five considered entries and one declared refusal (socket-modes) is gone.

## Findings — LOW

- **L1 — "its 0/21-marker journal reading" is garbled.** observability-r37 §3: "the session
  log (27,331 lines) holds **21 core-logger lines**, the last at line 21" — 21 is a session-log
  figure, not a journal marker count; the journal figures are 717 lines / probe 7×log vs 0×
  journal. The substance (same null channel; r37 made the measurement) is correct.
- **L2 — S277 citation drift.** Lane `SOURCES.md` S277 pins
  `chriskearney/chonkstep@707cf7f8…`; the lane entry's source line and the staged row say
  `iconidentify/chonkstep` `main`. The Gate binds by digest (`ff561fe0…`) so evidence is
  pinned, but the two textual citations disagree and byte-identity to the staged row's fetch
  is locally unverifiable.
- **L3 (nit) — "Staged table: 5 knowledge entries".** The package stages 69 entries; five is
  the round's considered request-socket set. Ambiguous next to "147-row SOURCES.append".

## Residual risk and verification gaps

- No network re-fetch was performed: S221/S253 receipt identity rests on the committed bytes
  plus the package rows' sha-prefix cells (package-side claims); only S158/S187 could be
  checked against earlier lane receipts (done, PASS).
- S277 staged-vs-lane byte identity unverified (L2).
- H3 is prospective: nothing in `corpus/` is corrupted today; the collision fires when the
  staged register is next assimilated.
- I did not audit the counters, the discrimination run, or the scorecard (other seats);
  lessons statements about them were checked only for consistency with registration.
- No tools were installed for this audit (sha256sum, grep, python3 sufficed).
