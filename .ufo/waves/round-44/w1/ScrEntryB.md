# ScrEntryB - C2 entry draft (round 44, wave w1)

Status: **done** - the C2 entry draft exists at its seat path, all five Gate quotes and every locator in it were
recomputed from the pinned receipts, and `PRED-C2-r44` scored the draft `admitted=1/1 verdict=TARGET_MET` in a
throwaway clone with a synthetic integration (registry rows, lesson Gate, README row) built only in scratch.

## Behavior delivered

- `.ufo/waves/round-44/w1/ScrEntryB/hyprland-gkeep-size-request-r44.md` - 65 raw lines (limit 90). Title, the
  exact `Lane: mado-shokunin. Round: 44.` line, five `source: S### - <title> - <anchor>` lines at raw lines 5-9
  (S164, S298, S299, S300, S301), one `verified-at: 2026-10-26` (line 10), one `recheck: 30d - ...` (line 11),
  `ground:` and `assimilated-from:` lines, then the decision table (`| question | where the answer lives | state |`,
  7 rows) opening the body, five short evidence sections with exactly one claim line per cited id (Gate quote
  verbatim + computed locator), a limits section, and the two census lines verbatim on their own lines outside
  fences as the last two lines.
- `.ufo/waves/round-44/w1/ScrEntryB/quotes.tsv` - id, receipt, sha256, computed locator line, word count, quote for
  the five cited ids (the input for the lesson's `GATE` lines).
- `.ufo/waves/round-44/w1/ScrEntryB/receipts/gate-lines.txt` - the five ready `GATE` lines (receipt path, pinned
  sha256, quote) for the L1 to paste into `corpus/lessons/round-44.md` `## Gate`; the ADMIT/REFUSE pair is the L1's
  choice and is not in this file.
- No gkeep window was observed, no `hyprctl` verb was run, no compositor or host state was touched, no package was
  installed.

## Gates (what was actually run)

| command | outcome |
|---|---|
| `python3 -I fixtures/verify-entry.py` (re-implements clauses b, g, h and re-checks every locator in the entry) | `FAILS: []`, 65 lines, `ids=[S164,S298,S299,S300,S301] ghosts=set() window=0 va=1 rc=1` |
| `python3 -I fixtures/quote-probe.py` (PRED-C2-r44's own `quote_at`/`occurrences`/`quote_in_code`/`norm_receipt`) | each quote `occ=1`, `code=1`, words 13/6/22/9/7, `others=[]`; census recomputed to the two required lines |
| `python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <scratch clone> --rev 92682f7f846dce7998c75774a5b4f858cbcdc7c3 --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f` | `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` -> `admitted=1/1 verdict=TARGET_MET`, exit 0 (`receipts/fixture-counter-c2.txt`; the rev is the scratch clone's, not a lane rev, and the clone is deleted) |

The fixture clone was `git clone -q --shared` of the lane at the freeze commit `e2289516`, `rev-parse
--show-toplevel` asserted equal to the clone before any commit, commits made with a scratch identity inside the
clone only; the clone and every other scratch path were removed after the receipts were copied here. The fixture's
registry rows, lesson and README row are **verification scaffolding, not lane data** - the L1 must write the real
ones.

## Integration requirements proved by the fixture (for the L1)

1. Registry, `corpus/SOURCES.md`: four new 11-cell rows for S298, S299, S300, S301 - status `mined`, opened
   `2026-10-26`, a valid recheck cell, the location as the last whitespace token of the source cell holding the
   pinned raw URL (clause e: `xdgshell.cpp` in `hyprland-xdgshell.cpp`, etc.), and `used-by` listing
   `corpus/knowledge/hyprland-gkeep-size-request-r44.md`.
2. Registry: S164 already exists at base, so its row keeps cells 1-9 and must have the entry path **appended** to
   `used-by`; without that append clause c fails (`used=0 ok=0` - observed in the first fixture run, fixed in the
   second).
3. Lesson `corpus/lessons/round-44.md` `## Gate`: the five column-zero `GATE` lines from
   `receipts/gate-lines.txt` (sha256 must equal `receipts/fetch-sha256.txt`), plus at least one `ADMIT
   merge/mado/knowledge/corpus/knowledge/<staged> as corpus/knowledge/hyprland-gkeep-size-request-r44.md` and one
   `REFUSE ... reason=` naming a **different** staged file, >= 20 chars, >= 4 distinct words, holding a flip word.
   Clause i+ needs all five pinned receipts cited, which the five ids give.
4. `corpus/README.md`: exactly one column-zero index row matching `| \`knowledge/hyprland-gkeep-size-request-r44.md\``.
5. The entry itself is byte-final at the path above; it must be copied unchanged (its sha256 is
   `29becd1951061500c5717fd4b15c4ef70d8c6615acfdebc73af1bc8e4d99534f`).

## Findings and limits

- **Quote choice is constrained, not free.** The obvious S164 quote
  `m_pendingSizeAcks.emplace_back(...)` is two whitespace words and would fail clause d's 3-word minimum; the draft
  uses the whole `if (m_isX11 && m_xwaylandSurface) ... else if (...) ...` chain (13 words, starts at
  `Hyprland-Window.cpp:1750`), which also carries the X11-versus-xdg split the claim needs. S299's quote starts at
  line **1150**, not 1151: the counter's collapse assigns a quote's first character to the line it sits on, and the
  indentation tab lives on the preceding line boundary - the typed 1151 would be wrong.
- **The staged r12 is not adopted.** `gkeep-client-size-request-r12.md` ends by declaring the chain complete and the
  rendered geometry 420x500; the draft's `assimilated-from:` line records the amendment and supersession and states
  that the conclusion and the settled wording are not adopted. `gkeep-size-to-real-size-r11.md` is neither admitted
  nor refused here (round 43 admitted it).
- **Title** departs from the registration's working phrasing ("What establishes the size ...") and reads "What can
  and cannot establish the size ...", because the entry does not establish a rendered size; a falsifier reading the
  registration wording against the body would otherwise find an overclaim.
- **Id coincidence, declared.** The provisional ids S298-S301 also appear in the package's own id list
  (`assimilation/staged-ids:96-99`), but the lane registry tops at S297 (234 rows), so there is no lane collision;
  the mapping stays by document (`assimilation/renumber-map.tsv:3` maps the staged S312 to provisional S301). Any
  lane id chosen by the L1 must keep the five receipt basenames in `quotes.tsv` unchanged, or the Gate lines and the
  claim locators stop matching.
- **UNK stays UNK.** The entry says the live gkeep state is UNK and never claims a gkeep window was seen; the
  compositor-dump statement is referred to by entry path (`corpus/knowledge/hyprland-gkeep-geometry-r43.md`), not
  by a held id, so no unregistered `S###` token enters the file.
- The C2 side does not depend on C1: nothing here reads `tools/mado-geometry.py` or the C1 counter.
- Not my scope: D1-D7 closure edits, the SKILL/PROVINCE rows, the round-43 counter's own `TILED` licence, the C1
  tool, and the data commit.

## Touched surfaces

- Written: `.ufo/waves/round-44/w1/ScrEntryB/` only (entry, `quotes.tsv`, `receipts/`, `fixtures/`) and this report
  file. No tracked lane file edited, no counter/control/registration/reference/pin touched, no git or jj mutation in
  the lane. The only git writes happened inside the scratch clone, now deleted.

## Artifact paths

- Entry draft: `.ufo/waves/round-44/w1/ScrEntryB/hyprland-gkeep-size-request-r44.md`
- Quotes: `.ufo/waves/round-44/w1/ScrEntryB/quotes.tsv`
- Gate lines: `.ufo/waves/round-44/w1/ScrEntryB/receipts/gate-lines.txt`
- Fixture counter run: `.ufo/waves/round-44/w1/ScrEntryB/receipts/fixture-counter-c2.txt`
- Clause verifier output: `.ufo/waves/round-44/w1/ScrEntryB/receipts/verify-entry.txt`
- Quote probe output: `.ufo/waves/round-44/w1/ScrEntryB/receipts/quote-probe.txt`
- Scripts: `.ufo/waves/round-44/w1/ScrEntryB/fixtures/{build-fixture.py,verify-entry.py,quote-probe.py}`
