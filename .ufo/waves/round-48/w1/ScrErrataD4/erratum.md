# D4 erratum - draft block for `corpus/knowledge/xdg-terminal-selection-r47.md`

Seat `ScrErrataD4`, round 48 wave 1, 2026-10-26. Write scope: this seat dir only; the L1 is the
integrator and applies the block below. No product file was edited by this seat.

Target: `corpus/knowledge/xdg-terminal-selection-r47.md`
(sha256 `a1c184eaca512d1ddbba5a97ddd6986913eadebac8f26d8ba381fab41747a0ba`, 96 lines, clean at lane
HEAD `5ff167423ee410251da0ef0c82f8e6fa25875665`).
Source swept: `corpus/knowledge/terminal-route-r17.md`
(sha256 `8ae41c4c889d93531e8cff2593923165ef3e227ff17f536aae68ec8fb8d632af`, 152 lines).
Second swept file: `corpus/lessons/round-47-verifier-spotcheck.md`
(sha256 `bd4a203a97eec404459dc52e9f9aa4b19e240d7ebbf84405195f13151c5dcaf2`, 146 lines).

Sweep result: 6 citing locators in the two files - **5 correct, 1 wrong**
(`xdg-terminal-selection-r47.md:95`), plus 1 deliberate defect mention in the round-47 lesson that
quotes the wrong locator in order to route it. One correction therefore, one erratum line.

---

## APPLIED BLOCK - append at EOF, nothing above it changes

Append a blank line after the current last line (line 96, the `Hyprland's own exec path` bullet), then
this block verbatim. Nothing else in the file is touched, so lines 76 / 88 / 95 and every external
locator into them stay where they are.

````markdown
## Erratum (2026-10-26, round 48)

E1 - one locator in Limits points at the wrong lines of `corpus/knowledge/terminal-route-r17.md`
(sha256 `8ae41c4c889d93531e8cff2593923165ef3e227ff17f536aae68ec8fb8d632af`, 152 lines). This is a
citation correction only: no claim, number, table row or verdict in this entry changes.

- `xdg-terminal-selection-r47.md:95` - cites `:150-151` of `terminal-route-r17.md`; corrected to
  **`terminal-route-r17.md:149-150`**. The bullet says the `--dir=` helper value "resolves at launch time stays `[UNK]`";
  in the source the sentence opens on :149 -
  "[UNK] Whether the `--dir=` value from `omarchy-cmd-terminal-cwd` is valid at launch time." - and
  closes on :150 - "The helper is not run." The cited :151 is a single byte, the newline of a blank
  line, so `:150-151` keeps the sentence's tail and drops its subject.

*What stands unchanged:* the answer chain, the cache section and the entry's other two locators into
that file - `:144-145` at :76 (the selection half) and `:144-145` at :88 (the launch half) - each
recomputed against the pinned bytes and landing on the sentence its line claims. The round-47 lesson's
three citations of `:144-145` (`corpus/lessons/round-47-verifier-spotcheck.md:56,84,110`) are correct
for the same reason, and its D4 line (`:139-140`) already states this correction; appending here leaves
all four line numbers where they were read. The body above is not edited, so the bullet at :95 keeps the
stale range inline: this block is the correction of record, and a sweep of the entry will keep
reporting :95 until a re-landing rewrites it.

*Limit of this erratum:* nothing was run against a shell, a resolver or a host file. The check is a
byte re-read of the two pinned markdown files (sweep `.ufo/waves/round-48/w1/ScrErrataD4/receipts/d4-sweep.txt`,
three identical runs, sha256 `41baf414bb008ce1b44108f7382e1a06c0079d6855d2885eedcb9cdd1a95351e`;
independent verifier `.ufo/waves/round-48/w1/ScrErrataD4/receipts/d4-verify.txt`, 112/112).
````

---

## Sweep receipt

Method: locators are parsed out of the two citing files by regex over real `grep -n` output; every
source range (bullet, `[UNK]` sentence start, sentence end) is computed by scanning
`terminal-route-r17.md`. No line number in the table below was typed. Scripts:
`.ufo/waves/round-48/w1/ScrErrataD4/sweep.py` (produces the receipt) and
`.../verify.py` (independent re-check of the receipt against the same bytes: excerpt lines equal the
file lines, the locator is still on the recorded citing line, the anchor sits inside a MATCH range and
outside a MISMATCH range, sentence bounds recomputed by a second code path, quotes verbatim and <= 25
words).

| citing line | cited range | claim of that line | anchor sentence | verdict |
|---|---|---|---|---|
| `xdg-terminal-selection-r47.md:76` | `:144-145` | selection half of the round-17 `[UNK]` | :144 | MATCH |
| `xdg-terminal-selection-r47.md:88` | `:144-145` | launch half (process start not observed) | :145 | MATCH |
| `xdg-terminal-selection-r47.md:95` | `:150-151` | the `--dir=` helper `[UNK]` | :149 | **MISMATCH** -> `:149-150` |
| `round-47-verifier-spotcheck.md:56` | `:144-145` | base ground, `[UNK]` quoted | :144 | MATCH |
| `round-47-verifier-spotcheck.md:84` | `:144-145` | base ground `[UNK]` answered | :144 | MATCH |
| `round-47-verifier-spotcheck.md:110` | `:144-145` | ground held `[UNK]` at base | :144 | MATCH |
| `round-47-verifier-spotcheck.md:139` | `:150-151` | *mentions* the entry's wrong locator while routing it | - | DEFECT-MENTION, its own asserted `:149-150` CONFIRMED |

The mismatch, from the receipt:

```
CITING file=corpus/knowledge/xdg-terminal-selection-r47.md citing_line=95 cited=150-151
  claim='helper' anchor_line=149 sentence_start=149 bullet=149-150 corrected=149-150 verdict=MISMATCH
EXCERPT cited=150-151 begin
150|   launch time. The helper is not run.
151|
EXCERPT end
EXCERPT corrected=149-150 begin
149| - [UNK] Whether the `--dir=` value from `omarchy-cmd-terminal-cwd` is valid at
150|   launch time. The helper is not run.
EXCERPT end
```

Totals line of the receipt:
`TOTAL citing_locators=6 match=5 mismatch=1 defect_mentions=1`,
`WRONG citing=corpus/knowledge/xdg-terminal-selection-r47.md:95 cited=150-151 corrected=149-150`.

### Post-append simulation

The block was appended to a scratch copy of the entry and the same sweep re-run on the copy
(`receipts/d4-sim-append.txt`, `receipts/d4-sim-diff.txt`): lines 1-96 of the copy are byte-identical
to the lane file (`diff` exit 0), the file grows 96 -> 123 lines, the appended erratum bullet (copy line
105) classifies MATCH for `:149-150`, and the copy still reports entry line 95 as the wrong locator -
which is the append-only design, not a miss: the body keeps the stale range and the block is the
correction of record. Copy totals: `TOTAL citing_locators=7 match=6 mismatch=1 defect_mentions=1`.

## Checked and deliberately not an erratum

- **`xdg-terminal-selection-r47.md:88` is not wrong.** It cites `:144-145` as the "launch half", and
  `:144-145` is the range round 47 itself calls the round-17 `[UNK]` and splits into a selection and a
  launch half (`.ufo/waves/round-47/registration.md:16-19`, 'launch half ("at launch") stays
  `[UNK]`'). The source clause behind the label is "that entry over the system one at launch; no
  launcher ran" (:145), which is inside the cited range. The other reading is recorded, not scored: the
  process-start question has its own sentence at `:128-130` ("Whether a terminal process actually
  started from that selection ... no launcher ran in this round"), and the sweep emits it as
  `RELATED ... anchor_line=128 sentence=128-130 also_cited=no`. A stricter cite would name `:128-130`;
  the landed cite is consistent with the round's own vocabulary, so no correction is drafted.
- **`round-47-verifier-spotcheck.md:139`** quotes `terminal-route-r17.md:150-151` on purpose - it is
  the routing line for this defect - and states the correction as `sits at `:149-150``. The sweep
  confirms that asserted range holds the helper sentence, so the lesson needs no erratum.

## Provenance of the wrong locator

- Landed entry `xdg-terminal-selection-r47.md:95` carries `:150-151`.
- The round-47 draft carried the same text: `.ufo/waves/round-47/w1/ScrEntry/entry.md:85`
  (read-only observation; seat artifact, not tracked).
- The round-47 lesson draft carried a third variant, `:149-151`
  (`.ufo/waves/round-47/w1/ScrLesson/lesson.md:274`); the landed lesson dropped that parenthetical, so
  the variant never reached a tracked file.
