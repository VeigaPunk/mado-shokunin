# ExecQuarantineSlice — seat report (mado round 43, w1)

Status: **complete**. Deliverables written; all claims re-runnable from the seat directory.
Access date for every fetch: 2026-10-26. Register and staging area were read-only throughout
(register re-hashed after the run: unchanged).

## Result in one paragraph

The lane's slice of the payload-absent register is **13 data rows** (6 `payload-absent`, 2 "could not be
fetched", 5 "gate block named no locator"), written to `assimilation/quarantine-slice`
(sha256 `d9ea803d…`). The 11 staged gkeep-theme files cite **28 distinct ids**; **none is a slice id**.
A source-level join finds exactly **one** contact: register row **S199** (CSDN `149787804`, unreachable,
no quote ever taken) is the same document as packaged row **S216**, cited inline at
`glyph-and-geometry-r31.md:28`. Verdict for it: **`unverifiable`** (unreachable, not fabrication) —
totals adopt 0, refuse 0, unverifiable 1. A register-wide join confirms no other quarantined row cites
any document the theme relies on. The two files named "in particular" (`gkeep-size-to-real-size-r11`,
`gkeep-rendered-geometry-chain-r9`) are clean: every row they cite resolves outside the register.

## Deliverables

| path (relative to the lane) | what |
|---|---|
| `.ufo/waves/round-43/assimilation/quarantine-slice` | the 13-row slice, exact `awk` from the assignment |
| `.ufo/waves/round-43/assimilation/quarantine-verdicts.md` | id / class / URL / quote-or-absence evidence / verdict for all 13 rows, the three joins, the two named files, the quotes table |
| `.ufo/waves/round-43/w1/ExecQuarantineSlice/join-evidence.py` + `.txt` | the join receipt (id-level, source-level, register-wide, offsets, collisions) |
| `.ufo/waves/round-43/w1/ExecQuarantineSlice/verify-quotes.py` + `.txt` | 63 assertions: every quote re-grepped at its stated file:line (≤25 words), slice/register hashes, join results, fetch evidence |
| `…/quarantine-slice.raw` | byte copy of the slice |
| `…/csdn-2301_76324845.body`, `…/csdn-lxyoucan.body` | the two direct-fetch 521 stubs (2 263 B / 2 167 B) |
| `…/proxy-149787804.txt` | reader-proxy body, 71 957 B, sha256 `81a5e78a…` |

Re-run: `python3 join-evidence.py | diff - join-evidence.txt` (empty) and `python3 verify-quotes.py`
(exit 0, `FAILURES: 0`).

## Findings for the L1

1. **The theme's only quarantine contact is a stale inline id, not a quotation.**
   `glyph-and-geometry-r31.md:28` bases a claim on "round 5's row S216"; packaged S216 is the CSDN
   window-rule blog (the quarantined row). The producer row is **S248**; the same file's `:36` names
   "round 5's row S219" (omarchy `hypridle.conf`) where the host rule is **S251**; and
   `gkeep-size-to-real-size-r11.md:63` names "round 10's S281" (a Chinese ArchWiki API fetch) where the
   claim's base is a compositor-side row (round 10's S298 / pin S296). Three inline ids, none resolvable
   to the sentence it carries in any numbering on disk. Header `source:` lines are sound.
2. **Do not join the register or the theme by id.** The register's ids are +17 from the packaged ids for
   all eight source-bearing slice rows (S189→S206 … S199→S216, S200→S217, S228→S245); and 7 of the 28
   cited ids also name a *current lane row with a different subject* (S216 `Compositor.cpp`, S219
   mado-options, S281 notification-silencing, S284 `FocusGrab.cpp`, S285 quickshell, S286 xdph portal,
   S287 issue #565). Source/URL identity is the only sound join.
3. **`r9`/`r11` host-side rows are campaign-only paths.** `lanes/mado/round9|11/fetch/…` exists in the
   campaign checkout and nowhere in the lane (find → 0 hits), so S292/S293/S310-style rows can only be
   opened against a real lane path or refused — independently reproduces the id-guard's finding.
4. **S199/S200 are reachable only through a reader proxy.** Direct `curl` re-run today: HTTP 521 with a
   JS-challenge stub for both. The proxy returns the article (71 957 B, and it still carries the exact
   `opacity 0.80` rule line the packaged row quotes, proxy line 160, though the page title has changed).
   So the class cell is a fetch-method artifact, but with no quote recorded in the register there is
   nothing to match: `unverifiable`, never the fabrication class.
5. **Two of the six payload-absent rows are outside the province on their face** (S195 Chinese wiki
   package, S205 interwiki map — "documentation written in a localized channel", PROVINCE.md:76);
   S189 is on the theme's own commit pin (efb5099) but a file no theme row cites.

## Risks / limits

- This seat issues no verdict on the twelve rows the theme never names; their `payload-absent` state is
  unchanged (that matches round 41's precedent under the same task).
- I did not re-verify the theme's *upstream* quotes (other seats own that); my claims are about identity,
  joining and reachability only.
- The round-41 captured proxy body was used only as a hash-verified secondary copy (72 130 B, sha256
  `d9b9ebe8…`); the primary evidence is today's own fetch.

## Tools / scratch

- No tool installed (no pacman, no uv, no npx). Commands used: `awk`, `python3`, `curl`, `grep`, `find`,
  `sha256sum`, `wc`, `sed`.
- Scratch `/fast/scratch/hyaku/mado-r43/ExecQuarantineSlice/` removed before this report; no scratch path
  is cited as evidence anywhere in the deliverables.

Report: .ufo/waves/round-43/w1/ExecQuarantineSlice.md
