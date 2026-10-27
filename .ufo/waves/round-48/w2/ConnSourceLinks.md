# ConnSourceLinks — w2 FALSIFY: C2 source crosswalk (entry ↔ rows ↔ Gate ↔ README ↔ receipt)

Seat: ConnSourceLinks (leaf, connector). Attack: crosswalk every source S340–S350 cited in
`l1-draft/xkb-keymap-compile-r48.md` to exactly one SOURCES row, pin file/digest, Gate
URL/quote and README coverage ID. No lane files edited. Evidence in
`w2/ConnSourceLinks/` (`counter-replay.txt`, `census-mirror-codes.txt`, `rows-gen-diff.txt`).

## Verification harness

- Replayed the freeze per `l1-draft/c2-mirror.sh` in my own seat scratch
  (`/fast/scratch/hyaku/mado-r48/ConnSourceLinks/`, removed after; git index 2,794,431 B was
  the largest internal file, git-internal, inside the 2 GB budget; my largest written evidence
  file 9,651 B, all writer shells ran `ulimit -f 2048`). Mirror rev
  `a7f490aadb56f501e1a3136c9e165492527b2477` = base `579f694b…` + the l1-draft C2 bytes.
- Result: `PRED-C2-r48: admitted=1/1 verdict=TARGET_MET`, exit 0, clauses a–r all ok,
  live replay byte-matched keymap sha `efd487a39920…`, negatives (1,1,0) (`counter-replay.txt`).
- `sources-census.sh validate` on the mirrored registry: code set identical to
  `receipts/census-before.txt` (1 pre-existing W01, 17 pre-existing W04, exit 0; E11 lines are
  an artifact of validating outside a full corpus tree and hit all 308 historical rows equally;
  no code touches S340–S350).

## Crosswalk matrix (S340–S350)

| id | entry head | row (11 cells, tier A, mined, used-by=entry) | pin digest/bytes/lines (recomputed == row) | Gate URL/quote | README |
|---|---|---|---|---|---|
| S340 | yes | S340 | xkbcommon-rules.c 04dfd934… 74868 B/2125 ✓ | same URL as row; quote `No index provided…` @:1259 ✓ | in S340-S350 range |
| S341 | yes | S341 | xkbcommon-xkbcomp.c ae6823a8… 7920 B/239 ✓ | URL ✓; quote @:157 ✓ | ✓ |
| S342 | yes | S342 | xkbcommon-include.c 95b5d8b5… 17209 B/510 ✓ | URL ✓; quote @:355 ✓ | ✓ |
| S343 | yes | S343 | xkbcommon-context.c e6547abb… 16074 B/592 ✓ | URL ✓; quote @:503 ✓ | ✓ |
| S344 | yes | S344 | xkbcommon-context-priv.c c2ffff03… 5898 B/225 ✓ | URL ✓; quote @:218 ✓ | ✓ |
| S345 | yes | S345 | xkbcommon-meson_options.txt 496455ea… 2411 B/102 ✓ | URL ✓; quote `value: 'us',` @:46 ✓ | ✓ |
| S346 | yes | S346 | 3 pins: rules-evdev 0cc48ee1… 31520 B/747 ✓; rules.in 16389776… 15768 B/425 ✓; rules-meson.build 1b4ab1d4… 3356 B/94 ✓ | URL ✓; quote `pc+%l%(v)` @rules.in:243 ✓ (byte-checked) | ✓ |
| S347 | yes | S347 | xkeyboard-config-symbols-br 8cf65550… 19592 B/368 ✓ | **MISSING from Gate** | ✓ |
| S348 | yes | S348 | xkbcommon-tools-compile-keymap.c 099664ce… 23033 B/631 ✓ | URL ✓; quote @:587 ✓ | ✓ |
| S349 | yes | S349 | xkbcommon-messages-codes.h 4e721d31… 9554 B/214 ✓ | URL ✓; quote @:150 ✓ | ✓ |
| S350 | yes | S350 (own-work) | receipt 14270 B ab5fa971…; fetch byte-copy same sha ✓ | own-work; quote `rc=0` @receipt:57 ✓ (byte-checked) | ✓ |

All 18 entry quotes (steps 1–9 + OBS block) verified verbatim at their pinned lines; all Gate
quotes verified at their pinned lines. Entry head: 11 `source:` lines inside the first 20 raw
lines, one `verified-at: 2026-10-26`, one `recheck: on-release`, no ghost ids, no `source:`
outside the window. README row: exactly 3 cells, coverage id `MADO-R48-1` (unique in
l1-draft), sources cell `rows S340-S350` covers all 11 head ids, no redirect word, names no
other `knowledge/` file; base README contains the `xdg-terminal-selection-r47.md` anchor row
the integrator inserts after. Receipt crosswalk: version 1.13.2, `br`+`compose:caps` rc 0,
keymap 73079 B/2090 lines sha `efd487a3…`, negative probes rc (1,1,0) with XKB-595 text —
every value the entry states matches the receipt windows. Held S318/S319 byte-equal, r46
entry unchanged, ground terms absent at base.

## Findings

1. **Gate omits S347 (evidence-completeness defect).** `l1-draft/gate-rows.md` is headed
   "Gate — rows S340-S350" but records only 10 dispositions (S340–S346, S348–S350). Row S347
   (xkeyboard-config 2.48 `symbols/br`, pin `fetch/xkeyboard-config-symbols-br`, quote
   `xkb_symbols "nodeadkeys" {` @:47 — both verified true) has no admit/reject line, while the
   entry cites S347 in its head and OBS block, `rows-c2.md` registers it, and the README row
   covers it. The w1 gate evidence `w1/ScrRows/gate-lines.md` *did* contain a symbols/br
   admission (there numbered "S341"); it was lost in the L1 renumber to S340–S350. The same
   consolidation also dropped w1's third reject (Hyprland `IKeyboard.cpp` as a duplicate of
   held S319) — the l1 Gate carries only the two URL rejects. The frozen counter never reads
   the Gate, so this does not change the TARGET_MET replay; it is a freeze-evidence
   inconsistency (header claims 11 rows, body disposes 10) for the L1 to repair before data
   commit, e.g. by adding the S347 admit line and the third reject.
2. **Receipt header generator path disagrees with the row and the committed tree (minor).**
   `receipts/xkbcli-compile-keymap-r48.txt:1` records
   `generator .ufo/waves/round-48/receipts/make-xkb-receipt.sh`, but the generator is
   committed at `.ufo/waves/round-48/tools/make-xkb-receipt.sh` and row S350's anchor cites
   `tools/`. The committed script writes its output next to itself (`OUT="$HERE/…"`), so the
   receipt was produced before the move and not regenerated. `l1-draft/make-rows.py` still
   emits the stale `receipts/` path — the committed `rows-c2.md` was hand-corrected
   (`rows-gen-diff.txt` shows exactly this one-line difference). Crosswalk mismatch:
   receipt line 1 vs row S350 anchor vs on-disk script.
3. **Entry recheck line says "the nine upstream code pins" (stale count, prose).** The entry
   cites 12 distinct upstream pins across S340–S349 (13 fetch files including the receipt
   byte-copy; 14 on disk including the uncited `fetch/xkbcommon-meson.build`). "Nine" matches
   no current count — leftover from the 8-row w1 draft. Counter-tolerant; fix the number or
   drop it.
4. **Row S349 anchor cell omits :150.** Entry OBS S349 quotes `messages-codes.h` at :116 and
   :150; the Gate anchors its quote at :150; the row's anchor cell lists only :116. The
   counter validates only that listed anchors resolve inside the pin, so this passes, but the
   row's locator list is incomplete against entry/Gate usage.
5. **Uncited pin `fetch/xkbcommon-meson.build` (50.4K) in the freeze set.** No row, entry
   citation or Gate line names it and its digest is recorded nowhere, against the freeze
   checklist ("any file measured or cited at the freeze has its digest in the corresponding
   counter or receipt"). Counter-tolerant (clause d refuses quotes from uncited pins), but it
   should either gain a digest citation or be removed from the fetch set.
6. **Receipt date label split (cosmetic).** Receipt header says
   `taken: 2026-10-27T00:08:08Z (UTC)` while entry/rows/Gate all say opened/verified
   2026-10-26 (local take was 2026-10-26 22:08). Same instant, two date labels; reviewers
   cross-reading dates will see the discrepancy.

## Axes affected

- **quality/operability (C1 trend untouched)**: findings 1–6 are C2 freeze-evidence issues;
  none weakens the counter's verdict (mirror replay TARGET_MET, exit 0). Finding 1 is the only
  one that misstates what was admitted (a coverage-claim surface: the Gate claims to dispose
  S340–S350 and does not).

## Risks / notes

- Fixing finding 1/3/4/5 is pre-data editorial work; none touches the frozen predicate,
  counters, fixture set or claims, so no re-registration trigger arises from these items
  themselves (registration allows re-register only for predicate/fixture defects; this report
  finds none).
- Proposed verification after any fix: re-run `l1-draft/c2-mirror.sh`-style mirror +
  `quality/counters/c2-r48-xkb-entry.py` (expect TARGET_MET) and `sources-census.sh validate`
  (expect the `census-before.txt` code set).
