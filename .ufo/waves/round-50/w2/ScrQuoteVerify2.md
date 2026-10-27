# ScrQuoteVerify2 — round 50 w2 (FALSIFY) — committed-bytes quote/anchor verification

Attack rev `b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip). Read-only: pins, lesson, entry and
registry were materialised with `git show <rev>:<path>`; the lane worktree was never read as evidence.

Blob identity at the attack rev (equal to the frozen `906178b6` table in `registration.md`):
lesson `e7cd29620aeed655f54fa3401b901acba8fe3f47ffdb4b5e9d6f3a62e20be794`,
entry `ae8f8d4de6fa8ede452423095942ee9f2182efdbab79c02744271c6fb0016977`,
SOURCES `b3a1a041d4a9ce0c2555f028ce415bac5a4b1a0e38bf782e730cbb24ddf52744`
(`receipts/blob-hashes.txt`).

## Verdict

Quote fidelity **passes**; anchor registration **fails** for 4 of the 10 `source:` lines.

- §1 Gate admit lines (committed lesson vs committed pins): **12/12 PASS**, 5/5 reject lines present.
  Every line carries a source (URL, or the own-work path for S361), `opened 2026-10-27`, a pin:line,
  and a ≤25-word quote that is a literal substring of the pin at that line; the stated word count is
  exact (5,3,13,9,10,7,4,10,12,6,6,5); each id resolves to a `## Registry` row whose anchor covers the
  admitted line, whose pin digest equals the committed blob, and whose status/opened/used-by match the
  lesson. **No falsification of PRED-C1-r50's quote/location evidence.**
- §2 `source:` lines of `corpus/knowledge/hyprland-bind-key-match-r50.md`: **6/10 PASS**. 4 lines cite
  pin regions that lie outside the anchor cell of the row they name (details in F2).
- §3 located quotes `` `q`(alias:line[-line]) `` in the entry: **90/90 are literal at the cited pin
  line**, but **33 tokens (32 unique cites) sit outside every anchor** of the rows naming that pin file.
- §4 pins: `fetch/SHA256SUMS` 15/15 digests equal the committed blobs; all 12 admit rows' stated pin
  digests equal the committed blobs.

## Commands (all read-only)

```sh
REV=b4a79843cc2545bbe800db9322e58f6e00436629
bash .ufo/waves/round-50/w2/ScrQuoteVerify2/verify-quotes-committed.sh      # rc 1, "FAILED: 37"
bash .ufo/waves/round-50/w2/ScrQuoteVerify2/compare-w1-data.sh             # rc 0, mismatches=0
python3 -I .ufo/waves/round-50/w2/ScrQuoteVerify2/calibrate-anchors.py     # calibration note
```

`verify-quotes-committed.sh` is the port of `w1/ScrRowsR50/verify-quotes.sh` (which read the worktree
`gate.md` and a hard-coded quote table): it parses the admit lines out of the committed lesson, reads the
pins from `git show <rev>:.ufo/waves/round-50/fetch/<file>`, adds the registry/anchor/digest resolution,
and re-checks every located quote in the entry. Working copies of every blob it scores are written under
`$SCRATCH/run` (scratch, deleted after the receipts were copied).

## §1 Gate admit lines — 12/12 PASS

| id | pin:line | words | row anchor covers | row pin sha256 = blob |
|---|---|---|---|---|
| S352 | Hyprland-KeybindManager.cpp:369 | 5 | yes | yes |
| S353 | Hyprland-legacy-ConfigManager.cpp:1484 | 3 | yes | yes |
| S354 | Hyprland-InputManager.cpp:1711 | 13 | yes | yes |
| S355 | xkbcommon-keysym.c:268 | 9 | yes | yes |
| S356 | xkbcommon-ks_tables.h:3 | 10 | yes | yes |
| S357 | xkbcommon-tools-how-to-type.c:101 | 7 | yes | yes |
| S358 | xkbcommon-xkbcommon-keysyms.h:471 | 4 | yes | yes |
| S359 | wiki-Binds.md:40 | 10 | yes | yes |
| S360 | wiki-Variables.md:219 | 12 | yes | yes |
| S361 | binds-live-r50.txt:9 | 6 | yes (`whole file` anchor) | yes |
| S362 | xkbcommon-state.c:116 | 6 | yes | yes |
| S363 | Hyprland-IKeyboard.hpp:14 | 5 | yes | yes |

Notes for a re-scorer: S361 is the only line with no URL — it carries `Source: .ufo/…/binds-live-r50.txt
(own-work capture, no remote URL)` and the row's `source` cell names the same path; S361's anchor cell is
`binds-live-r50.txt whole file`, so an anchor test that only looks for `file:N` tokens would report a
false FAIL. Other rows naming the same files (S303, S316, S318, S319) cover some of these cites but
were not substituted for the row the line names.

Receipt: `receipts/verify-quotes-committed.txt` (§1 block).

## §2 `source:` lines vs registry anchors — 6/10 PASS

PASS: entry:8 S356, entry:9 S354, entry:10 S360, entry:12 S362, entry:13 S363, entry:14 S361.
FAIL (cited pin lines outside the row's anchor cell):

- **entry:5 → S353** (`Hyprland-legacy-ConfigManager.cpp`), anchors `1481-1490, 1492, 1511-1548, 1525, 1624-1651`;
  cited outside: `:607, :1555, :1567, :1603, :1616, :1617, :1620` (7).
- **entry:6 → S352** (`Hyprland-KeybindManager.cpp`), anchors `369, 652, 691-724, 419, 488, 537-545, 773-793,
  855-899, 289-334`; cited outside: `:189, :224, :236, :367, :370, :377, :461, :634, :671, :702-726, :728,
  :738, :747, :928-942` (14; 725-726 is the only part of `702-726` outside `691-724`).
- **entry:7 → S355** (`xkbcommon-keysym.c`), anchors `70-94, 237-250, 255-289, 293-343`; cited outside:
  `:252` — inside the 251-254 hole between the 237-250 and 255-289 anchors (1).
- **entry:11 → S359** (`wiki-Binds.md`), anchors `36-52, 74-84, 434-441, 464-471`; cited outside:
  `:111, :144, :155, :462` (4; `:462` is two lines above the 464 anchor).

Interpretation used: a `source:` line's "cited region" is every pin line the entry cites from that row's
pin file(s), since the lines themselves carry no ranges except entry:13/16. Receipt: §2 block of
`receipts/verify-quotes-committed.txt`; per-cite table in `receipts/uncovered-cites.tsv`.

## §3 located quotes vs committed pins

90 located quote tokens parsed. 90/90 quotes are literal substrings of the committed pin at the cited
line or inside the cited range — zero quote/location mismatches. 57/90 also sit inside an anchor of a row
naming that pin file; 33 do not (32 unique cites: S352 14, S353 7, S359 4, S355 1, S319 6; quote tokens
count 33 because ConfigManager:1616 appears twice). Receipt: §3 block of
`receipts/verify-quotes-committed.txt`.

## Findings

- **F1 (supports C1).** The round-50 lesson's 12 Gate admit tuples are equal, field for field (id, pin
  file, line, word count, quote), to the DATA table inside the committed
  `w1/ScrRowsR50/verify-quotes.sh` (`mismatches=0`, `receipts/w1-data-vs-lesson.txt`), and the w1 receipt
  it cites exists at the rev: 12 `PASS S3…` lines and a final `ALL QUOTES VERIFIED`
  (`receipts/blob-hashes.txt`). Caveat: that w1 script verified the worktree `gate.md` text, not the
  lesson text; this seat re-ran the checks against the lesson bytes and got the same 12/12.
- **F2 (attacks the C1 claim's "grounded on registry rows" sentence).** 27 unique pin cites in
  `corpus/knowledge/hyprland-bind-key-match-r50.md` are outside the anchor cells of the rows that name
  their pin file, undeclared in the entry: S352 14, S353 7, S359 4, S355 1, and `Hyprland-IKeyboard.cpp`
  `:221-271` (cited at entry:63 and entry:132) outside S319's `60-145, 101-116`. The entry only declares
  the other S319 reads (`entry:16`: `:118, :214-219, :18-20, :139, :360, :372, :381-382, :421-422` —
  exactly the 5 remaining S319 cites). The quotes themselves are all present at those lines, so this is
  under-registration of anchors, not wrong locations: e.g. the mask-parse step cites
  `Hyprland-KeybindManager.cpp:224` and `:236`, which S352 does not anchor while anchoring `:652`.
- **F3 (provenance of F2).** The anchor cells are byte-identical between the w1 draft
  `w1/ScrRowsR50/rows.md` and the committed `corpus/SOURCES.md` rows, S352-S363 all `SAME`
  (`receipts/anchors-draft-vs-committed.txt`) — the gap originates in the w1 row draft, not in the L1
  integration.
- **F4 (calibration; keeps F2 honest).** Applying the same anchor rule to earlier entries gives
  uncovered 5/46 (`hyprland-input-devices-r46.md`), 7/26 (`keybind-rule-semantics.md`), 19/19
  (`bind-table-r25.md`) and 36/97 for this entry (`receipts/calibration-prior-entries.txt`). The lane's
  practice is therefore not "anchors bound every cite", so F2 is an under-registration finding, not a
  claim that the entry is unsourced; round 50 is nevertheless an outlier against the recent round-46 entry.
- **F5 (supports the freeze).** All 12 admit rows carry `status=mined`, `opened=2026-10-27`, the right
  `used-by` (`corpus/knowledge/hyprland-bind-key-match-r50.md`, lessons for S357/S358) and a pin digest
  equal to the committed blob; `fetch/SHA256SUMS` matches all 15 committed pins it lists. The 16-file pin
  dir materialises at the rev (16/16).
- **F6 (checked, no defect).** The entry's `ground:` line (entry:19) resolves at the rev: all 7 cites
  (`hyprland-input-devices-r46.md:71`, `keybind-rule-semantics.md:106` and `:108`, `bind-table-r25.md:46`,
  `round-49-verifier-spotcheck.md:91`, `round-49.md:15`, `PROVINCE.md:114`) exist and carry the named term
  (`receipts/ground-cites.txt`). `PROVINCE.md` lives in the lane, not the fleet root; the lane blob at the
  rev was used.
- **F7 (why this port had to read committed bytes).** At report time the lane worktree's
  `corpus/lessons/round-50.md` differs from the committed blob: an uncommitted M50-5 block appended after the
  Gate section (worktree sha256 `b77fe238…a5aff9` vs committed `e7cd2962…be794`, `git diff` +8 lines, not this
  seat's edit). A verifier reading the worktree would hash and score different bytes than the freeze names;
  every receipt here comes from `git show <rev>:`.

## Limits

- Anchor coverage and the per-`source:`-line aggregation are the assignment's rule as I operationalised it;
  the SOURCES contract (`anchor` = "exact section/heading/page/line plus revision") does not itself bound
  an entry's cites, and F4 shows the lane has not enforced it as a bound.
- No semantic check that a quote supports its row's `teaches` text, and no scoring/verdict on C1/C2 — these
  are attack receipts for the L1.
- Bare `:line` shorthand (entry:16 `:372`, `:381-382`, `:421-422`; entry:7 `:252` inside a range already
  cited) is not attributable to a file by the parser and is not counted as a cite.
- Held rows S318/S319 register round-46 receipts, so their anchor digests were not compared to round-50
  pins; the round-50 pins of the same basenames do match `SHA256SUMS`.
- SHA256SUMS' own line (a self-digest) is excluded from the 15.

## Out of scope

No lane/fleet tracked file was edited, no counter was run to score a claim, no tool installed, no host
state touched; nothing in `.ufo/state/`, `scripts/`, `templates/` or sibling lanes was written.

## Artifacts

- `verify-quotes-committed.sh` — ported, committed-bytes verifier (this seat).
- `compare-w1-data.sh` — w1 DATA table vs committed lesson admits.
- `calibrate-anchors.py` — anchor-coverage calibration on earlier entries.
- `receipts/verify-quotes-committed.txt` — full §1-§4 output, rc 1, `FAILED: 37`.
- `receipts/uncovered-cites.tsv` — 82 unique pin cites: file, range, owning row, covered/UNCOVERED, entry lines.
- `receipts/anchors-draft-vs-committed.txt`, `receipts/w1-data-vs-lesson.txt`,
  `receipts/ground-cites.txt`, `receipts/calibration-prior-entries.txt`, `receipts/blob-hashes.txt`.
