Report: .ufo/waves/round-44/w1/ScrEntryA.md

# ScrEntryA - C2 entry draft (mado round 44, w1)

Seat: ScrEntryA. Lane: mado-shokunin. Date: 2026-10-26. Claim: C2 (coverage), entry
`corpus/knowledge/hyprland-gkeep-size-request-r44.md`. Shape: chain-first, eight sections.

## Behavior (what was produced)

1. `.ufo/waves/round-44/w1/ScrEntryA/hyprland-gkeep-size-request-r44.md` - the full entry draft: title, five
   `source:` lines (S164 held, S298-S301 provisional), one `verified-at: 2026-10-26`, one `recheck: 30d`,
   `ground:`, `Lane: mado-shokunin. Round: 44.`, an `amends:` line for the staged r12, a decision table, and the
   eight required sections (goal box -> report size -> configure+serial -> ack -> protocol -> GTK -> gkeep ->
   observed/unobserved), the two census lines verbatim on their own lines, and a "does not establish" list.
2. `.ufo/waves/round-44/w1/ScrEntryA/quotes.tsv` - id, quote, receipt file, computed line, sha256 for all five ids.
3. `.ufo/waves/round-44/w1/ScrEntryA/verify-quotes.py` and `lint-entry.py` - the checkers (both print; both exit 0).
4. Fixture integration set (`fixture-*.txt`/`fixture-lesson-round-44.md`): the exact registry rows, S164 used-by
   append, lesson Gate block and README row that make the draft score - ready for the L1 to renumber and commit.

No product file, counter, control, registration, pin or reference was written or edited.

## Gates (exercise receipts in this seat dir)

| check | command | result | receipt |
|---|---|---|---|
| pin bytes | `python3 -I verify-quotes.py` | 5/5 sha256 equal the frozen PINS (`Hyprland-Window.cpp` held row, same bytes) | `receipt-verify-quotes.txt` |
| quote clauses d/d+ | same script | each quote 3-25 words, exactly one word-bounded occurrence, inside comment-stripped code/text, absent from the other four receipts, locator recomputed by the frozen counter's `quote_at` | `receipt-verify-quotes.txt` |
| entry clauses b/g/h simulation | `python3 -I lint-entry.py` | 5 source lines inside the first 20 raw lines, one verified-at/recheck, no key line after line 20, no ghost S-id, one bound claim line per id with quote+locator, census lines exactly once, census recomputation identical | `receipt-lint-entry.txt` |
| full frozen predicate | `python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <fixture> --rev HEAD --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f` | `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1 verdict=TARGET_MET`, exit 0, at fixture rev `1265d07f43b2b34dbf81b2389b385d6ae1a38e2e` | `receipt-counter-fixture.txt` |

The full-predicate run used a scratch clone of the lane (`git clone -q --shared <lane> <scratch>/fixture`,
`git -C <fixture> rev-parse --show-toplevel` = fixture path) carrying the draft plus the fixture registry rows,
lesson Gate and README row; every git call named `-C <fixture>`; the lane index was never touched. The receipt is
therefore **a fixture score of the draft's clauses, not a lane admission** - admission is the L1's data commit.
The fixture tree was deleted per the scratch rule; every input of that run (draft, `fixture-registry-rows.txt`,
`fixture-s164-row.txt`, `fixture-lesson-round-44.md`, `fixture-readme-row.txt`) is in this seat dir, and
`verify-quotes.py` / `lint-entry.py` re-run against the lane's pins alone.

Computed locators (from `quote_at`, not typed): `Hyprland-Window.cpp:1752`, `Hyprland-XDGShell.cpp:354`,
`xdg-shell.xml:1150`, `gdktoplevel-wayland.c:681`, `gkeep-ui.py:474`. The S164 quote begins on the `else if` line
(1752), not on the `setSize` line (1753); the S301 quote begins on the `Gtk.ApplicationWindow` line (474) and holds
`set_default_size` from line 476.

## Integration requirements for the L1 (the draft does not self-admit)

1. **Ids.** S298-S301 are provisional (registration: final ids by document at the data commit). Substitution must
   touch: the four `source:` lines, the four claim lines, the lesson GATE lines and the four registry rows. The entry
   must keep exactly five S-tokens outside fences (clause b).
2. **Pins at the data rev.** All five receipts must be committed at `.ufo/waves/round-44/fetch/<name>` (mode 100644,
   sha256 from the table) - clause d reads them at the scored rev. They are already tracked at `ae996fcf`
   (`git ls-files .ufo/waves/round-44/fetch` = 5).
3. **Lesson.** `corpus/lessons/round-44.md` must exist with the five GATE lines (quotes/sha256 in
   `fixture-lesson-round-44.md`), one `ADMIT .../gkeep-client-size-request-r12.md as corpus/knowledge/
   hyprland-gkeep-size-request-r44.md`, and >= 1 `REFUSE` of a STAGED file with a flip word. Stages excluded by the
   predicate: `gkeep-size-to-real-size-r11.md` (admitted in round 43, neither admit nor refuse again).
4. **Registry.** S164 (held): append the entry to used-by, leave cells 1-9 byte-equal. New rows: 11 cells, status
   `mined`, opened 2026-10-26, valid recheck, location ending in the receipt's file-name component (raw-commit URL
   for both `Hyprland-*` receipts).
5. **README.** Exactly one column-zero row starting ``| `knowledge/hyprland-gkeep-size-request-r44.md` ``.

## Findings

- **F1 (quote binding).** Each of the five quotes is unique inside its own pinned receipt and absent from the other
  four (`receipt-verify-quotes.txt`); the S300 quote is real code outside the toolkit's `/* */` restatement of the
  0x0 rule, so the entry's GTK claim rests on the handler's own write, not on its comment.
- **F2 (census teeth).** The counter's own parser reproduces both census lines from the pinned bytes:
  `set_default_size(420, 500)` once, `set_size_request(` zero times, one `application_id`, and in the
  `sendWindowSize` body one `->setSize(` (1753) and one `->configure(` (1751) - `host_census` returned exactly the
  two lines the draft carries (`receipt-lint-entry.txt`, last check).
- **F3 (what the ack does and does not do).** `onAck` stores the acknowledged size as `m_pending.ackedSize` and
  `getReportedSize()` returns `m_current.ackedSize` for a wayland window (Hyprland-Window.cpp:1514-1528,
  1861-1866), but **no caller of `getReportedSize()` exists in the five pins** - recorded in the entry as UNK, not
  upgraded to a compositor behaviour.
- **F4 (protocol reading kept honest).** The 1.49 text calls the numbers "a hint", gives zero to the client, and
  makes only the ack mandatory; the entry states the absence of a duty-to-adopt as INF and the conformance question
  as UNK rather than claiming a licence the text does not grant.
- **F5 (r12 handling).** The draft amends the staged `gkeep-client-size-request-r12.md` in a header line and names
  the non-adoption of its "settled"/"complete" wording in the body; the body's only `merge/mado/...` reference is
  that line, so no ADMIT/REFUSE decision is smuggled into the entry (clause i stays the lesson's).
- **F6 (live state).** No gkeep window was observed; §8 says so and the decision table's live row is UNK. The only
  host fact carried is the round-43 census/tool receipt, cited by path (`.ufo/waves/round-43/receipts/
  live-geometry-host.txt:10` carries `verdict=NO_MATCHING_CLIENT`, re-read).

## Touched surfaces

- Written: `.ufo/waves/round-44/w1/ScrEntryA/` (entry draft, quotes.tsv, two checkers, five receipts, fixture rows,
  this report).
- Read-only: the five pins, `quality/counters/c2-r44-gkeep-size-request.py` (imported, never edited),
  `corpus/knowledge/hyprland-gkeep-geometry-r43.md`, `corpus/SOURCES.md`, `corpus/README.md`,
  `corpus/lessons/round-43.md`, the registration.
- Scratch `/fast/scratch/hyaku/mado-r44/ScrEntryA/` (clone + fixture) deleted after the receipts were copied.
  No mutation inside the lane: `git status --porcelain` shows only this seat's untracked directory.
- No tool installed (nothing needed), no pacman, no `hyprctl dispatch`/`keyword`/`reload`, no host-service action,
  no input injection, no protocol client of my own, no git/jj mutation in the lane or the fleet.

## Out of scope (named, not done)

- The data commit and the actual id assignment; the C1 tool; the lesson prose beyond the Gate block; the
  assimilation decisions for the other staged files; any live gkeep observation (needs the operator).
