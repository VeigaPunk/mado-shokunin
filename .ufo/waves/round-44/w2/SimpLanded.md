# w2/SimpLanded — dead weight in the landed round-44 text and the tool

Seat target: the sentences of `corpus/knowledge/hyprland-gkeep-size-request-r44.md`, the round-44 `SKILL.md` rows and paragraph
(`:280-291`), the `corpus/README.md` index row and Frontier section (`:72`, `:304-320`), `corpus/lessons/round-44.md`, and the
`tools/mado-geometry.py` docstring — at the data commit `e4678921` (base `6a1a905`). Nothing in the lane was edited: the six
deletions below were applied to a throwaway clone under `/fast/scratch/hyaku/mado-r44/SimpLanded/` (deleted before this report) and
scored there. The L1 decides and lands.

Texts are identical at the tip: `git diff e4678921 290cddea -- SKILL.md PROVINCE.md corpus/ tools/` prints nothing.

**Result: six deletions, 109 words, each removing a second copy of a fact that survives at a computed locator; all six are neutral on
both predicates and on the tool's selftest (proof in §2). Two tradeoffs are declared in §3.** No new predicate hole was found; what the
counter's silence shows is the residual `registration-v2.md:64-65` already declares (§5).

## 1. The deletions

| id | file:line at `e4678921` | words | the copy it removes | fact survives at | line-map shift |
|---|---|---|---|---|---|
| D1 | `corpus/knowledge/hyprland-gkeep-size-request-r44.md:40` | 18 | a UNK boundary stated a second time | same file `:79` | 0 |
| D2 | `corpus/knowledge/hyprland-gkeep-size-request-r44.md:9` | 8 | four pinned versions, five lines above their own `source:` lines | same file `:3-7` | 0 |
| D3 | `corpus/README.md:318` | 17 | the reason TILED is narrow, stated twice more | `SKILL.md:291`, `tools/mado-geometry.py:61-63` | −1 below `:318` |
| D4 | `SKILL.md:289-290` | 33 | the same reason, inside the appended D3 correction | `SKILL.md:276` (row caveat), `corpus/lessons/round-44.md:130` | −2 below `:290` |
| D5 | `corpus/lessons/round-44.md:52` | 17 | a pointer to two blocks the reader is looking at | — (pure navigation) | 0 |
| D6 | `tools/mado-geometry.py:16-17` | 16 | the round-43 tool's old behaviour, narrated in this tool's docstring | `.ufo/waves/round-44/registration-v2.md:13`, `corpus/lessons/round-44.md:190` | −1 below `:17` |

Full unified diff, verbatim: `.ufo/waves/round-44/w2/SimpLanded/deletions.diff`. Every quote below is checked by
`.ufo/waves/round-44/w2/SimpLanded/verify_quotes.py` (output `quotes-verified.txt`, `QUOTE-VERIFY PASS (19 checks, 0 failures)`);
locators are computed there (`grep -n` equivalent), not typed.

### D1 — entry `:40`, drop the duplicated UNK boundary (18 words)

Delete: `What Hyprland does with a buffer of another size after the ack is outside this entry's pins (UNK).`

Survives, word for word in meaning, at `corpus/knowledge/hyprland-gkeep-size-request-r44.md:79`: `What Hyprland does when a client
commits a buffer whose size differs from the acked one (not among the pins).` — the entry's own "What this entry does not establish"
list. Nothing is lost: the section is the canonical place for a boundary, and after the deletion §2's INF still carries its claim
(`it does not force the client's next buffer to be that size`), whose ack locator (`:38`, `Hyprland-Window.cpp:1514`) is untouched.
`grep -rF 'What Hyprland does with a buffer of another size'` over the landed tree → 1 hit, the line being deleted: no other
document quotes it. Line count unchanged (edit is inside one line), so no locator moves.

### D2 — entry `:9`, drop the version parenthetical from `recheck:` (8 words)

Delete from the `recheck:` line: `(Hyprland efb5099, wayland-protocols 1.49, GTK 4.24.1, gkeep 133b867)`.

The same four versions sit five lines above in the header the counter itself parses: `:3` `@ efb5099`, `:5` `wayland-protocols 1.49`,
`:6` `@ 4.24.1`, `:7` `@ 133b867` (also `:81`). Nothing is lost: `recheck: 90d - re-pull the five pinned files and re-run the counter;`
keeps its trigger and the counter's `recheck` clause only reads the leading token (`RECHECK_RE`, `c2-r44-gkeep-size-request-v2.py:92`).
`grep -rF 'five pinned files (Hyprland'` over the landed tree → 1 hit, the line being deleted. Line count unchanged.

### D3 — README Frontier `:318-319`, drop the parentheses (17 words)

Delete: `(a pseudo-tiled client takes its box from the stored pseudo size, which `clients -j` does not print).`

The widened sentence is a route summary: `TILED is narrowed to "not floating"` stays, and the *reason* is intact twice over — the tool's
own contract (`tools/mado-geometry.py:61-63`: `TILED claims only that the client is not floating`) and the SKILL correction
(`SKILL.md:291`: `read TILED as "not floating" only`). Nothing is lost: all three copies say the same thing and the README's is the only
one no check reads (`PRED-C2-r44-v2` clause f matches only the index row, `c2-r44-gkeep-size-request-v2.py:627-628`; the lesson's
"Shown able to fail" greps only the SKILL phrase, `corpus/lessons/round-44.md:133` — still `1` after this deletion).
`grep -rF 'a pseudo-tiled client takes its box'` over the landed tree → 1 hit, the text being deleted.

### D4 — SKILL `:289-290`, drop the reason, keep the ruling (33 words)

Delete the clause that runs from `— "the tiler, not the floating rule path, set its box"` (`:289`) through
`round-44 pin \`.ufo/waves/round-44/fetch/Hyprland-Window.cpp\`);` (`:290-291`), leaving
`Licenses cell overstates; read TILED as "not floating" only.`

The reason is already in the row the correction is about: `SKILL.md:276` says the size is stored `as its pseudo size (`Window.cpp:2402-2408`, round-43 pin)`
and `clients -j` has no pseudo field — the exact falsifier the correction names. Nothing is lost: the ruling stays, the greppable phrase
the round's own failable check uses stays (`SKILL.md` `grep -c 'read TILED as "not floating" only'` → `1`), and the round-44 pin path is
still cited in the lesson's M44-3 (`corpus/lessons/round-44.md:130`). This is the 3-way duplicate of D3's reason measured directly:
`grep -n pseudo` → `SKILL.md:276,289,290`, `tools/mado-geometry.py:62,63`, `corpus/lessons/round-44.md:130`, `corpus/README.md:318`.

### D5 — lesson `:52`, drop the pointer to the blocks it sits between (17 words)

Delete from the opening of the sentence: `Rejected staged material, with reasons and flips, is in the REFUSE lines above and the ledger below;`

Nothing is lost: the `REFUSE` lines are twelve lines above (`corpus/lessons/round-44.md:37-40`, computed) under the section caption
`## Assimilation ledger (theme: the gkeep size request; package merge/mado/, read-only)` at `:57`; the clause only reports what the
reader can see. The surviving half (`The r12 claims the pins refute are listed in the entry's "What the staged predecessor said"
section (w1/ScoutStagedResidue, w1/CritAssimilation).`) is the part that carries a way out of the page. Line count unchanged (rewrapped
to two lines).

### D6 — docstring `:16-17`, drop the previous version's behaviour (16 words)

Delete: `; the round-43 tool printed` + `DIFFER there, true about the box and silent about the cause.` — leaving
`state (FULLSCREEN, MAXIMIZED) instead of comparing.`

The docstring is this tool's contract; the sentence describes a tool that no longer exists and no line of it tells a reader what this
version prints. Nothing is lost: the same calibration is recorded three times — `registration-v2.md:13` (frozen, `"true about the box,
silent about the cause"`), the round's mistake row `corpus/lessons/round-44.md:190` (`The box really differs; the tool could not say
why.`), and the w1 source `w1/CritFsPremise.md:12`. The deleted lines hold no behavioural word, and the tool's own check proves the
behaviour untouched: `--selftest` is 94/94 after it (§2).

## 2. Preserved contract — the fixture proof

Fixture: `git clone -q --shared` of the lane, `git -C $D checkout e4678921`, `git -C $D rev-parse --show-toplevel` == `$D`, then two
commits (`6d1d513` five deletions, `155cdd3` + D6). Receipts in this seat dir:

- `c1-after-deletion.txt` — `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=6d1d513…`, clauses `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1`
  (clause `r`, the round-42 contract, re-ran `fixtures=37/37 TARGET_MET`).
- `c2-after-deletion.txt` — `admitted=1/1 verdict=TARGET_MET` with `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1`, i.e. every clause
  including the twelve-surface `j` and the census `h` is unchanged by all five text deletions.
- `after-docstring-deletion.txt` — the same two counters at `155cdd3` (all six deletions): C1 `26/26`, C2 `1/1`, and
  `MADO_GEOMETRY_SELFTEST: 94/94 passed`; the removed hunk is the two docstring lines and nothing else.
- `baseline-at-data-commit.txt` — the lane itself at `e4678921`, before any edit: C1 `fixtures=26/26 … TARGET_MET`, C2
  `admitted=1/1 … TARGET_MET` with all ten clauses `1`. The after-states above are therefore a comparison, not a coincidence.

Nothing deleted is quoted elsewhere: for each removed string the landed tree holds exactly one hit — the line being deleted
(`quote-collisions.txt`; counts `1` for all five prose strings, the docstring pair checked by `verify_quotes.py`). And every removed
fact has a survivor at a computed locator (`quotes-verified.txt`, ten survivor checks).

## 3. Tradeoffs declared

1. **Line-map shifts.** D3, D4 and D6 reduce their files by one, two and one lines. Landed documents cite into two of those files:
   `SKILL.md:337` (`corpus/knowledge/omarchy-drift-watch.md:145`), `SKILL.md:344` (`corpus/knowledge/hyprland-config-era-r12.md:93`),
   `SKILL.md:351` (`corpus/knowledge/omarchy-drift-watch.md:78`) and the range `SKILL.md:288-300`
   (`corpus/knowledge/config-drift-r12.md:100`) would each point two lines early. **This drift is not created here**: the data commit's
   own +9 insertion at `:280` already moved that range off its target — at base `6a1a905` `SKILL.md:288-292` is the host-run block, at
   `e4678921` it is the new correction block (`ref-identity-and-drift.txt`). No landed document cites a `tools/mado-geometry.py` line
   after `:17` at a rev where D6 would move it (`:6` and a `base … :57` are the only two, computed), and no landed document cites
   `corpus/README.md` past `:318`. If the L1 wants zero shift, D4 and D3 can be rewrapped to their current line counts; I did not,
   because the result is ragged prose and the shift is already the status quo.
2. **Tool and frozen reference.** At `e4678921` `tools/mado-geometry.py` and the frozen `c1/ctl-ref-tool-v2.py.txt` are the same bytes
   (`sha256 1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4`, `ref-identity-and-drift.txt`); `LOG.md:2503` records
   that identity. D6 makes the tip's tool differ from that freeze-time artifact by two lines of prose, so a later byte check must name
   the rev, and `LOG.md:2503` stays true only as a statement about the data commit (which is what `Data:` there means). No clause
   requires the equality: `PRED-C1-r44-v2` runs the tool from `--tool`/`REV` and its clauses are behavioural (all `1` at `155cdd3`).
   This is the one deletion whose cost is real; skip D6 if the reference's byte identity is worth more than the 16 words.
3. **D4 drops the round-44 pin path from SKILL.** The `fetch/Hyprland-Window.cpp:2402-2408` mention leaves `SKILL.md`; the row keeps the
   round-43 pin and the lesson keeps the round-44 one (`corpus/lessons/round-44.md:130`). A SKILL-only reader loses the newer pin's path;
   nothing else changes.

## 4. Considered and rejected (each would harm an axis)

- **Entry `:30`, the X11 clamp clause** (`which for an X11 client clamps at 1x1 and may scale by the monitor instead`). It is beyond the
  entry's subject (`:80` says the X11 path is not established), so it reads like scope creep — but it is an `OBS` from S164 with no
  duplicate anywhere, and deleting a sourced observation trades coverage for weight. Rejected: coverage.
- **Entry licence table `:24` vs bullet `:78`.** Both answer "was a gkeep window seen"; the table asks about *acknowledging*, the bullet
  about *rendering*. Rejected: not the same question, and the table is the entry's licence index.
- **Entry `:62` INF vs `:60` OBS** (`minimum is set by its widget tree` vs `no set_size_request call`). One is the observation, one the
  conclusion drawn from it; the INF also states the non-competition, which appears nowhere else. Rejected.
- **README index row `:72` restates the entry.** Index convention, and clause f counts exactly one such row
  (`c2-r44-gkeep-size-request-v2.py:672-673`). Rejected.
- **Lesson `:149-151` vs `:206-209` (M44-5 vs erratum E3).** Verbatim duplicates: `:151` and `:209` are the same `grep -c '^\*\*M43-'`
  line, `grep` distance 58 lines. Same for `:110` vs `:199` (M44-1 vs E1). Deleting one copy's commands makes an erratum unfalsifiable
  for the reader who arrives from `corpus/lessons/round-43-verifier-spotcheck.md` §6, which routes to the errata section, not to M44-x.
  Rejected: provenance/falsifiability — this is the duplication the method requires, not dead weight.
- **Lesson `:236` vs `:163-164`** (`no positive control exists for C2`). The census section is where a reader checks control status; the
  M44-6 copy is evidence for the mistake. Rejected: same receipt read for two purposes.
- **SKILL rows `:280-282`.** No cell restates another; `the same as FULLSCREEN` is already the compact pointer. Nothing to cut.
- **QUALITY 82-84, SCORECARD and LOG Round 44** are outside this seat's named target; criteria 82-84 are rules, the lesson a record, and
  the LOG/SCORECARD lines are per-round history. Not judged here.

## 5. No new predicate hole — the counter's silence is the declared residual

`registration-v2.md:64-65` declares it: `clause j binds a locator and a keyword per surface, not the truth of the sentence`. D1-D6 keep
every clause at `1` while 109 words leave the four documents, which is that residual, measured. Read together with this round's
`w2/ExecDoNothingV2` (C2 v2 admits entry-plus-or-minus-prose controls), it is the same open defect, not a second one: a prose deletion
that removes a boundary statement (D1) would have been admitted had the survivor at `:79` not existed. I report no OPEN predicate defect
of my own; if the L1 wants this class closed, the next registration needs a clause that binds a *removed* UNK to its surviving statement,
which no current clause does.

## 6. Seat hygiene

- Lane untouched: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain --untracked-files=no | wc -l` → `0`; HEAD
  `290cddea`. No git/jj mutation in the lane; the only fixture repo was created with `mktemp -d -p /fast/scratch/…`, verified with
  `rev-parse --show-toplevel`, and committed with an identity supplied on the command line (`-c user.name=SimpLanded`).
- Scratch `/fast/scratch/hyaku/mado-r44/SimpLanded/` (clone + work dirs, well under 2 GB) deleted before this report; every citable
  file is in this seat dir.
- Tools installed: none (python3, git only). No pacman, no host service, no compositor mutation; the only host reads were earlier seats'
  receipts, not the live compositor.
- Files written: this report and the eleven receipts beside it (`deletions.diff`, `locators.txt`, `verify_quotes.py`,
  `quotes-verified.txt`, `baseline-at-data-commit.txt`, `c1-after-deletion.txt`, `c2-after-deletion.txt`,
  `after-docstring-deletion.txt`, `surviving-copies.txt`, `quote-collisions.txt`, `ref-identity-and-drift.txt`).
