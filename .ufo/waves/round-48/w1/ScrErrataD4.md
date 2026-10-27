# ScrErrataD4 — round-48 w1: D4 erratum draft for `xdg-terminal-selection-r47.md`

Routed item D4 (`corpus/lessons/round-47-verifier-spotcheck.md:139-140`: "Limits cites
`terminal-route-r17.md:150-151` for the helper `[UNK]`; the text sits at `:149-150`. Append an erratum
line."). Leaf seat: no subagents, no product file edited, nothing run against a shell/host for this
item. Read-only `git` only; no `pacman`, no package transaction, no tool installed.

## Behavior delivered

1. **D4 verified by computed locator.** `corpus/knowledge/terminal-route-r17.md` (sha256
   `8ae41c4c889d93531e8cff2593923165ef3e227ff17f536aae68ec8fb8d632af`, 152 lines) holds the helper
   `[UNK]` on lines **149–150**, not 150–151: :149 opens the sentence ("[UNK] Whether the `--dir=`
   value from `omarchy-cmd-terminal-cwd` is valid at launch time."), :150 closes it ("The helper is not
   run."), and :151 is a blank line — 1 byte, the newline. The entry cites `:150-151` at
   `corpus/knowledge/xdg-terminal-selection-r47.md:95`. Confirmed exactly as routed.
2. **Same-method sweep of every other `terminal-route-r17.md` locator** in the entry and in the
   round-47 lesson: **6 citing locators — 5 correct, 1 wrong**, plus one deliberate defect mention.
   Entry: `:76` → `:144-145` MATCH, `:88` → `:144-145` MATCH, `:95` → `:150-151` **MISMATCH**
   (correct `:149-150`). Lesson: `:56`, `:84`, `:110` → `:144-145` MATCH; `:139` quotes the wrong
   locator to route it and states `:149-150`, CONFIRMED.
3. **Draft erratum block written**, append-only, house style (`## Erratum (2026-10-26, round 48)`,
   modelled on `corpus/knowledge/hyprland-input-devices-r46.md:75`), **one line per wrong locator**
   (there is one), with the corrected citation, what stands unchanged, and the limit of the erratum.
   It is ready to append at EOF; the block itself records that the stale range stays in the body
   because appending does not edit it.
4. **Append simulated in scratch**: copy of the entry + block → lines 1–96 byte-identical (diff exit 0),
   file 96 → 123 lines, the appended bullet classifies MATCH for `:149-150`, and the copy still reports
   entry line 95 as wrong (by design). Copy totals `citing_locators=7 match=6 mismatch=1`.

## Gates

| gate | command | result |
|---|---|---|
| sweep receipt, 3 identical runs | `python3 .ufo/waves/round-48/w1/ScrErrataD4/sweep.py . <out>` ×3 | same sha256 `41baf414bb008ce1b44108f7382e1a06c0079d6855d2885eedcb9cdd1a95351e` each run |
| independent verifier | `python3 .../verify.py . .../d4-sweep.txt .../erratum.md` | `VERDICT PASS checks=112 passed=112 failed=0` (rc 0) |
| body unchanged by the append | `diff <(sed -n '1,96p' $SIM/corpus/knowledge/xdg-terminal-selection-r47.md) $LANE/corpus/knowledge/xdg-terminal-selection-r47.md` | no output, exit 0 |
| write scope | `git status --porcelain` in the lane | only untracked `.ufo/waves/round-48/w1/ScrErrataD4*`; no tracked file modified |
| quotes | every quote ≤ 25 words, locator computed, verbatim check | 17/17 `QUOTE ... inside=true`; `used=true` spans grepped inside `erratum.md` by the verifier |

The verifier (`.../ScrErrataD4/verify.py`) is a second code path over the same bytes: excerpt text must
equal the real file line, the locator must still sit on the recorded citing line, a MATCH must contain
the anchor line and a MISMATCH must not, the sentence bounds are recomputed here instead of trusted
from the sweep, and every `used=true` quote must appear in the draft.

## Touched surfaces

- Wrote (new, untracked, seat only):
  `.ufo/waves/round-48/w1/ScrErrataD4.md` (this report),
  `.ufo/waves/round-48/w1/ScrErrataD4/erratum.md` (draft block + sweep receipt),
  `.../sweep.py`, `.../verify.py`,
  `.../receipts/d4-sweep.txt`, `.../receipts/d4-verify.txt`,
  `.../receipts/d4-sim-append.txt`, `.../receipts/d4-sim-diff.txt`.
- Read only: `corpus/knowledge/xdg-terminal-selection-r47.md`, `corpus/knowledge/terminal-route-r17.md`,
  `corpus/lessons/round-47-verifier-spotcheck.md`, `.ufo/waves/round-47/registration.md`,
  `corpus/knowledge/hyprland-input-devices-r46.md`, `corpus/knowledge/bind-table-r25.md`,
  `.ufo/waves/round-47/w1/ScrEntry/entry.md`, `.ufo/waves/round-47/w1/ScrLesson/lesson.md`,
  `.ufo/waves/round-48/claims.md`, read-only `git log/diff/status`.
- Scratch `/fast/scratch/hyaku/mado-r48/ScrErrataD4/` used for the append simulation and the
  determinism runs, receipts copied into the seat dir, scratch deleted before yielding.
- No product file, no fleet file, no `~/.local/bin`, no PATH directory, no jj/git index.

## Findings

**F1 — D4 confirmed (the routed item).** Entry `xdg-terminal-selection-r47.md:95` cites
`terminal-route-r17.md:150-151`; the sentence sits at `:149-150`. Receipt
`receipts/d4-sweep.txt` (`CITING ... citing_line=95 ... corrected=149-150 verdict=MISMATCH`, cited
excerpt shows `151|` empty). This is the only wrong locator in either swept file.

**F2 — entry `:88` examined and *not* an erratum.** `:88` cites `:144-145` as the "launch half", the
same range `:76` calls the "selection half". Round 47's own registration splits that one `[UNK]` into
those halves and defines the launch half as "at launch"
(`.ufo/waves/round-47/registration.md:16-19`), and the clause behind the label — "that entry over the
system one at launch; no launcher ran" (`terminal-route-r17.md:145`) — is inside the cited range, so
the cite is consistent with the round's vocabulary. Recorded, not scored: the process-start question
has its own sentence at `terminal-route-r17.md:128-130` ("Whether a terminal process actually started
from that selection … no launcher ran in this round"), emitted as
`RELATED ... anchor_line=128 sentence=128-130 also_cited=no`. If the L1 wants the stricter cite, `:88`
could name `:128-130`; no correction is drafted because the landed cite is defensible.

**F3 — the round-47 lesson needs no erratum.** `:139-140` quotes the wrong locator on purpose and its
asserted correction `:149-150` is CONFIRMED by the sweep. Its three `:144-145` citations are correct.

**F4 — provenance of the wrong locator.** It reached the draft unchanged
(`.ufo/waves/round-47/w1/ScrEntry/entry.md:85`, seat artifact, untracked) and the landed entry. A third
variant `:149-151` existed in the round-47 lesson draft
(`.ufo/waves/round-47/w1/ScrLesson/lesson.md:274`) but the landed lesson dropped that parenthetical, so
it never reached a tracked file. Independently corroborated by two round-48 seats
(`.ufo/waves/round-48/w1/ScoutHeld.md:41`, `.ufo/waves/round-48/w1/CritRoutedItems/findings.md:16`).

**F5 — note for the freeze / w2 sentinel.** Appending the erratum does not remove the stale
`terminal-route-r17.md:150-151` from entry line 95. A frozen predicate that greps the entry for the
wrong locator will still hit it after integration; the erratum block says so in its own text. The draft
phrase avoids re-introducing the full wrong locator in the *new* lines (bare `:150-151` only), so a
locator sweep after the append sees exactly one full-file locator there — the corrected `:149-150`,
which classifies MATCH (verified in the simulation).

## Out of scope / not done

- No product file edited (write scope is the seat dir; the L1 applies the block).
- Nothing executed against the resolver, the host cache, Hyprland or any terminal — this item is a
  byte-level citation check.
- `:76` / `:88` / `:95` line numbers were not "fixed" in place: append-only is the house rule and it
  keeps every external locator into them valid (lesson `:139`, round-48 seats).
- Not swept: other files' locators into `terminal-route-r17.md` (only the entry + round-47 lesson were
  in the ticket), and the round-47 seat drafts beyond the provenance observation.
- Tool installs: none.

## Provenance / hashes at HEAD `5ff167423ee410251da0ef0c82f8e6fa25875665`

Declared base `579f694b` is the round-47 closure; between base and HEAD only `.ufo/waves/round-48/*`
opening files changed (`git diff --name-only`), so the corpus bytes below are the base bytes.

```
a1c184eaca512d1ddbba5a97ddd6986913eadebac8f26d8ba381fab41747a0ba  corpus/knowledge/xdg-terminal-selection-r47.md  (96 lines)
8ae41c4c889d93531e8cff2593923165ef3e227ff17f536aae68ec8fb8d632af  corpus/knowledge/terminal-route-r17.md  (152 lines)
bd4a203a97eec404459dc52e9f9aa4b19e240d7ebbf84405195f13151c5dcaf2  corpus/lessons/round-47-verifier-spotcheck.md  (146 lines)
41baf414bb008ce1b44108f7382e1a06c0079d6855d2885eedcb9cdd1a95351e  .ufo/waves/round-48/w1/ScrErrataD4/receipts/d4-sweep.txt
5dc7a0e70e35df0eede9aee54f1d0cf80909b60343f118e51e0e2c7b0b9deb0a  .ufo/waves/round-48/w1/ScrErrataD4/receipts/d4-verify.txt  (re-running verify.py on the final erratum.md reproduces these bytes: `cmp` clean, 112/112)
603976d8ba7dbc1c77a2a48fe7047dbfa4419222dbeb2ecb5512d34296c3fcd9  .ufo/waves/round-48/w1/ScrErrataD4/receipts/d4-sim-append.txt
132f61e66aae806c440ade4226cbf837b287b11380ae536b8872509ec9eec009  .ufo/waves/round-48/w1/ScrErrataD4/receipts/d4-sim-diff.txt
```

## Artifact paths

- Draft block + embedded sweep receipt: `.ufo/waves/round-48/w1/ScrErrataD4/erratum.md`
- Sweep receipt: `.ufo/waves/round-48/w1/ScrErrataD4/receipts/d4-sweep.txt`
- Verifier output: `.ufo/waves/round-48/w1/ScrErrataD4/receipts/d4-verify.txt`
- Append simulation: `.../receipts/d4-sim-append.txt`, `.../receipts/d4-sim-diff.txt`
- Scripts (reproducible): `.../ScrErrataD4/sweep.py`, `.../ScrErrataD4/verify.py`

## Limits

- All line numbers are the bytes at the hashes above; any re-landing that edits the entry or
  `terminal-route-r17.md` invalidates them and the sweep must be re-run (`sweep.py` resolves anchors
  and aborts if a typed anchor no longer occurs exactly once).
- The classification rule is a proxy: "the cited range must contain the `[UNK]` sentence's start and
  end inside the same bullet". It is what produced both the D4 hit and the F2 non-hit, so F2's
  judgement (defensible, not wrong) rests on the round-47 registration wording, not on a mechanical
  rule alone.
- The sweep reads only markdown bytes; it does not verify that the source's own claims are true.
