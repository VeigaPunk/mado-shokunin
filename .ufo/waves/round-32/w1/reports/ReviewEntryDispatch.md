# ReviewEntryDispatch — review of the two drafted dispatcher entries (round 32, w1)

Leaf reviewer; no subagents dispatched. Report only; no edits to the drafts.

## Inputs and timeline

- Draft A: `.ufo/waves/round-32/scratch/ScribeEntryDispatchers/dispatcher-semantics-r25.md` (landed during this review, 20:08 local).
- Draft B: `.ufo/waves/round-32/scratch/ScribeEntryDispatcherSurface/dispatcher-surface-and-request-grammar-r26.md` (landed during this review, 20:08 local).
- Seat reports: `.ufo/waves/round-32/w1/reports/ScoutDispatchersWiki.md` (S188 re-open, fetch sha256 `c830ce0717f92776…`, 12,879 bytes) and `.ufo/waves/round-32/w1/reports/ScoutDispatchers0560.md` (S196 re-open, sha256 `f9b51362f2440e02…`, 297,863 bytes).
- Bar: `corpus/QUALITY.md` (criteria 1–4, 6, 10, 13, 15, 16 applied); corpus contract per `corpus/README.md` (navigation map; admission bar is QUALITY.md).
- Method: every quote, count, hash and absence claim below was checked mechanically against the seat-report bytes and the sha-matched scratch fetches (`scratch/ScoutDispatchersWiki/dispatchers.md`, `scratch/ScoutDispatchers0560/dispatchers-0.56.0.html`). Full sha256 equality verified for both fetches (64-hex present verbatim in the seat reports and in draft B's Gate).

## Fetch-chain integrity (precondition)

PASS. Draft A's `source:` commit `c04680a28301ab4b5ee5f94eaff5395efe28dbac` equals the wave pin in `w1-spec.json`; A's recheck prefix `c830ce0717f92776` matches seat W's recorded sha256; B's Gate sha256 equals seat F's recorded sha256 byte-for-byte; B's recheck prefix `f9b51362f2440e02…` is a true prefix (QUALITY 6).

## Check 1 — per claim: does the supporting quote appear in the seat report at the stated anchor?

**Verdict: PASS for draft A · FAIL for draft B.**

Draft A (7 quote claims):

| Claim | Anchor | In seat report |
|---|---|---|
| "They do not invoke any action immediately, and their contents are not guaranteed to be stable at all." | S188:9 | YES (18 w) |
| "Simply writing `hl.dsp.whatever()` on its own will do nothing." | S188:15 | YES (9 w) |
| "To use a dispatcher (any of `hl.dsp.*`) inside a function, you need to wrap it in `hl.dispatch()` …" | S188:14 | YES (22 w) |
| "Send an event to socket2" | S188:59 | YES (5 w) |
| force_idle full cell (28 w, see Check 3) | S188:69 | As one contiguous quote: NO. Seat W deliberately split L69 into two ≤25-word fragments (both present; the joined 28-word form is verbatim in the scratch bytes) |
| "Do not use with a keybind directly!" | S188:58 | YES (7 w) |
| "It is NOT recommended to set DPMS or force_idle with a keybind directly, as it might cause undefined behavior." | S188:82 | YES (19 w) |

Draft B §1 (S196): the three signature quotes `exec_cmd(cmd, rules?)` / `dpms({ action?, monitor? })` / `event(string)` — YES, seat F General rows 1/15/16. The 47-name enumeration — verified item-by-item against seat F: **47 == 47, zero missing, zero extra** (`comm` of extracted sets empty, 2026-10-24). But the following §1 claims have **no quote and no anchor in either seat report**:

- FAIL — B L30: "…is **45** distinct names:" — contradicts its own 47-name enumeration (same paragraph) and seat F's "Distinct dispatcher base names across all `hl.dsp.*` tables: **47**".
- FAIL — B L48: "current-git page (S188) carries `reload_config`, which the 0.56.0 page (S196) does not" — no seat measured the current-page name set. Byte check: TRUE (present in scratch wiki bytes, absent in scratch 0.56.0 HTML), but unanchored.
- FAIL — B L50–52 (fullscreen signature-order drift, `resize()` fold): the two quoted forms are byte-verbatim in the respective scratch fetches, but neither seat report quotes or measures any dispatcher signature.
- FAIL — B L15: "answers **404** (re-checked 2026-10-24)" and B L124: "→ HTTP 404, re-fetched 2026-10-24" — no fetch artifact exists in the scribe scratch dirs (each holds only the draft .md), and neither seat report records a this-round 404 check. Independent probe 2026-10-24 (urllib GET): **404 confirmed** — fact true, receipt absent.
- FAIL — B L44–45: "`exec` … on the current page not at all" — the S196 half is anchored (seat F: `exec` only in prose snippets); the S188-half absence is not anchored. Byte check: TRUE (`\bexec\b` count 0 in scratch wiki bytes).
- FAIL — B L108–109: "`flags` has" / "zero occurrences in its bytes." (line-wrapped) — absence claim with no anchor or re-derivation command. Byte check: TRUE (0 case-insensitive occurrences of "flags" in the scratch 0.56.0 HTML).

Draft B §2 (S018): all five code quotes anchor to S018 by declaration, and B L66 states plainly: "S018 was not re-opened in round 32". Per this check they do not appear in the seat reports — correctly disclosed, not a honesty defect (see Check 5).

Draft B Gate located-quote 1 — FAIL as anchored: B L122 "**Located quote (15 words):** \"hl.dsp. contains: method description exec_cmd(cmd, rules?) execute a command.\"" does not appear in seat F (seat F only paraphrases the table intro as `hl.dsp.` + "contains:"); it is verbatim in the scratch bytes. Gate located-quote 2 ("Last updated on July 15, 2026") — YES, seat F records it.

## Check 2 — claims with no quote

**Verdict: FAIL (draft B).** All are listed in Check 1; summary: B L30 (count "45"), B L43–53 (reload_config, both fullscreen orderings, resize fold, "45 vs 46" totals), B L15/L124 (this-round 404 re-measurement), B L44–45 (current-page `exec` absence), B L108–109 (flags zero-occurrence), B L122 (Gate located-quote 1). Draft A: none — every OBS carries a quoted, anchored sentence; INF/UNK items carry explicit bases.

## Check 3 — quotes over 25 words

**Verdict: FAIL.** One instance:

- FAIL — draft A L32 blockquote, **28 words**: "Sets elapsed time for all idle timers in seconds, ignoring idle inhibitors. Timers return to normal behavior upon the next activity. Do not use with a keybind directly!" (S188:69). Seat W split this exact row into two fragments precisely to stay ≤25 ("table row, split for quote limit"); the draft re-joined them. Fix: keep the seat's two-fragment split, or trim to ≤25 words and move the remainder to prose. All other quotes: A max 22 w; B max 19 w.

Cosmetic count-label errors (not >25, but self-declared labels are wrong): B L122 says "15 words" for a 9-word quote; B L123 says "8 words" for a 6-word quote. Draft A's "18 words" label is correct.

## Check 4 — missing provenance lines

**Verdict: FAIL (partial).**

- Draft A header: PASS — `source:` / `verified-at:` / `recheck:` / `ground:` all present, per-claim anchors present, Gate present.
- FAIL — A L60–61: "Queued in `CANNOT-ANSWER.md`." — the file does not exist in the lane tree, the lane `.ufo/`, or the merge tree (`glob` empty, 2026-10-24). Inherited from the staged entry; repoint or drop.
- FAIL — B §1 unanchored block (L43–53): no source id, no receipt, no quote for the name-set totals and signature-drift claims (see Check 1).
- FAIL — B L109 and B L15/L124: absence/measurement claims without a re-derivation command, artifact path, or receipt (QUALITY 10/13).
- FAIL — both drafts' `ground: F1 — "dispatcher behavior" in arc-synthesis §6 U1`: `arc-synthesis` resolves to no file in the lane or merge trees. Inherited pointer; flag to the operator or the L1.
- B §2: PASS — provenance exists via the S018 registry row, its pinned commit `efb50993780079460b0cbed1363e2166a2de1d9f` (matches the `w1-spec.json` pin), plus the explicit not-re-opened label at B L66; re-verification is owed and declared.

## Check 5 — assertions the sources only document (not measure)

**Verdict: FAIL (draft B) · one nit (draft A).**

- B §1 name-set/signature/404/exec/flags block (L15, L29–53, L108–109): all documentary claims carried without this-round measured receipts; I byte-verified most as TRUE against the sha-matched scratch fetches, but the two totals ("45", "46 (current)") are **wrong or unverified** (true 0.56.0 count per seat F: 47; crude byte scan of the current wiki page: ~48, not 46). These must either gain a receipt (command + date + bytes) or be demoted to UNK/trimmed to the seat-anchored facts.
- B §2 S018 block (L63–101): documented by the staging campaign's 2026-10-23 read, not measured this round — correctly labeled as such (B L66) and correctly excluded from this round's re-open scope. Disclosed, acceptable; the wave's tier/used-by seats should rule on its currency.
- B INF L55–58 ("`reload_config` is a post-0.56 addition"): documented inference; B's own UNK L115 concedes the release dating is unpinned. Consistent.
- Nit — A §2 OBS "This is the documented bridge from the Lua config into the compositor's event socket described in `ipc-contract-r25.md`": a cross-document interpretation inside an OBS sentence; only "Send an event to socket2" is measured. Relabel as INF with the sibling-entry pointer as basis, or move the clause.

## Check 6 — overlap between the two drafts

**Verdict: PASS — no duplicated dispatcher fact; ownership is correctly split.**

- "Dispatchers describe, they do not act" (return-tables semantics): only draft A (S188:9/15). B never restates it. Keep in A.
- Dispatcher name vocabulary and per-name membership: only draft B. A names only the three dispatchers it quotes semantically. Keep in B.
- `force_idle`: A owns the semantics (clock-op INF over the full L69 cell); B mentions it only inside the keyword-membership sentence. Complementary.
- `event` → socket2: A owns the bridge fact; B covers the request-socket resolution grammar (S018) — a different surface. No dup.
- Lua wrapper: A's S188:14 usage doc vs B's S018:1132 `std::format("return hl.dispatch({})", in)` — different sources, different facts. No dup.
- Instability caveat: only A (§3). B is silent. Clean.
- Boundary note (not duplication): B's keyword sentence (L43–45) reaches into A's source (S188 bytes) for its "both pages" claim; if kept, anchor the current-page half or scope the sentence to S196.

## Overall

- Draft A: landable after one edit — split or trim the 28-word S188:69 quote (Check 3), and repoint the dangling `CANNOT-ANSWER.md` line. Everything else anchors.
- Draft B: NOT landable as-is. Blocking: the "45 distinct names" contradiction (its own enumeration and the seat both say 47), the unanchored §1 measurement block, and the unrecieipted 404/flags/exec claims. Its 47-name enumeration is otherwise verified perfect item-by-item against seat F.

## Verification log (commands and outputs, 2026-10-24)

- Quote containment + word counts: normalized substring match of every draft quote against seat-report bytes — outputs in Check 1/3.
- Fetch identity: `sha256(scratch/ScoutDispatchersWiki/dispatchers.md)` and `sha256(scratch/ScoutDispatchers0560/dispatchers-0.56.0.html)` each present verbatim in their seat reports; prefixes match both drafts' recheck lines.
- Name sets: token extraction from draft B's enumeration (47 unique) vs union of seat F's five group lists (General 16 + Window 20 + Workspace 4 + Group 7 + Cursor 2 = 47) — `draftB − seatF = ∅`, `seatF − draftB = ∅`.
- Signatures: `fullscreen({ window?, action?, mode?, layout_aware? })` present only in scratch wiki bytes; `fullscreen({ mode?, action?, layout_aware?, window? })` only in scratch 0.56.0 HTML; `resize()` bare form only in 0.56.0 — drift forms byte-true, seat-unmeasured.
- Absences: `\bexec\b` in scratch wiki bytes = 0; `flags` (case-insensitive) in scratch 0.56.0 HTML = 0.
- Live probe: `GET https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Dispatchers/` → HTTP 404 (urllib, 2026-10-24).
- Pointers: `CANNOT-ANSWER.md` and `arc-synthesis` — no hits in lane tree or `/home/vgpnk/Projects/shokuknow/merge/` (recursive glob).
