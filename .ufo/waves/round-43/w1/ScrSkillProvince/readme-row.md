# corpus/README.md insertion text — round 43 (seat `ScrSkillProvince`)

Draft only. Nothing here edits `corpus/README.md` (sha256
`53aa91cd7fbdc1dc6a573d5f29e71bb3269ebeea60cc33c935c11bd0a5ffdd84` at this seat's read, 2026-10-26; clean in
`git status`). The L1 integrates.

Checker receipt for the row: `.ufo/waves/round-43/w1/ScrSkillProvince/receipts/check-index-rows.txt`
(`python3 -I quality/check-index-rows.py --root <scratch>` → `errors=0`, exit 0; the scratch tree is the lane's
`corpus/` plus this row, plus the `S290-S299` registry rows and a stub entry note, both scratch-only). The run is
reproducible with `python3 -I .ufo/waves/round-43/w1/ScrSkillProvince/run-index-evidence.py`, which also carries five
negative controls (Sources cell emptied, two cells only, undefined S-id, missing Sources path, row outside the map) —
each fails with the expected `ERROR` line, so `errors=0` is a live check, not a vacuous one.

---

## 1. Coverage-map index row

**Insert as a new line after line 70** (`| knowledge/hyprland-focus-grab-r41.md | …`), i.e. as the new last row of the
coverage-map table (header line 11, separator 12, last row 70); line 71 is blank and line 72 is `## Quality bar`.
All four cells are present: Note, Holds, Sources — and the Note cell carries the note path, the claim id, the round and
the assimilation provenance, as every row above it does.

```markdown
| `knowledge/hyprland-gkeep-geometry-r43.md` (MADO-R43-1, round 43; assimilation of the gkeep-geometry theme of the staged mado package) | What determines the size of the host's gkeep window, end to end: the host rule text (`float on`, `center on`, `size 420 500` for `^(org.omarchy.gkeep)$`), the rule engine's anchored `re2::RE2::FullMatch`, the floating algorithm's first-map read of the rule's `size` expression, the target and window that store the box, `hyprctl clients -j` printing the animation GOAL rather than the current value, the app's own `set_default_size(420, 500)`, and today's census (4 clients, none floating, no gkeep window). Tool `tools/mado-geometry.py`; the rendered size and any live gkeep window stay `[UNK]`. | `source:` S290, S291, S292, S293, S294, S295, S296, S297, S298, S299 in [SOURCES](SOURCES.md); fetched bytes `.ufo/waves/round-43/fetch/`; sha256 list `.ufo/waves/round-43/receipts/fetch-sha256.txt`; recheck on-release |
```

### Why each cell says what it says

- **Note** — the round-41 row's shape: path, `(MADO-R<n>-<k>, round <n>; assimilation of …)`. The assimilation clause is
  required by the registration (§ Frontier step: one successor entry admitted from the staged gkeep theme); the package
  name stays generic ("staged mado package") because the staged tree is a read-only foreign checkout, not a lane path.
- **Holds** — the eight links of the chain the entry must carry, in order, each a fact the pinned receipts can carry:
  rule text (S297), `FullMatch` (S290), floating-branch read (S292), target/window storage (S293/S294), the GOAL variable
  (S295/S296), the app's declared request (S299), the census (S298). It names the tool, because a row whose instrument is
  not named cannot be re-run. It ends with the two `[UNK]` items so the row cannot be read as a rendered-size claim —
  the boundary `host-bar-producer-census-r40.md:37` and `config-drift-r12.md:50` already set (see
  `ConnSiblingOverlap/overlap.md` §5).
- **Sources** — all ten ids spelled out, not a range: `check-index-rows.py` resolves every `S###` token, and a range
  (`S290-S299`) would only resolve its two ends. Plus the two paths the checker can verify exist at REV: the fetch
  directory and the sha256 list — both are already committed at the freeze commit `b2e2efd`
  (`git ls-tree -r --name-only b2e2efd -- .ufo/waves/round-43/fetch .ufo/waves/round-43/receipts`), so
  `cited-path-missing` cannot fire for them at any later REV. No `.md`-target path is cited beyond the note's own
  name in cell 1, so the row adds no dangling link.
- The row deliberately cites **no** sibling-lane source: the fleet-wide scan found none (`ConnSiblingOverlap` §1/§4).
- **Registry dependency (confirmed with `ScrRowsDraft`, 2026-10-26):** all ten rows are drafted and census-validated at
  `.ufo/waves/round-43/w1/ScrRowsDraft/rows-block.txt`, so the ten-id Sources cell resolves as written. If the L1 takes
  that seat's alternative (drop `S291`/`S296` and cite held `S155`/`S158` for the same bytes under the commit-form URL),
  this cell must drop `S291` and `S296` and add `S155`/`S158` in the same edit, or `check-index-rows.py` reports
  `cited-s-undefined`.

### The one thing that can move after integration

`check-index-rows.py` also emits `WARN holds-no-overlap` when the Holds cell shares no ≥5-word sequence with the note's
own bytes (it never affects the exit code). The Holds cell above is written from the registration's own C2 sentence and
the note's planned section order, so it should quote the landed note; if the entry seat words the note differently, the
WARN fires and the fix is to copy one of the note's own sentences into the Holds cell. Recheck at the data commit:

    python3 -I quality/check-index-rows.py --repo . --rev <data-commit>

---

## 2. Frontier bullet

**Insert after line 291** (end of file; the `### Round-38 request-socket bound route` section runs 282-291), keeping one
blank line before it.

```markdown
- Round 43 opens the **rule size versus reported size** join: what a `windowrule = size W H, match:class RX` line
  declares against the goal box the compositor prints for the matching client
  ([gkeep geometry](knowledge/hyprland-gkeep-geometry-r43.md), S290–S299), instrumented by `tools/mado-geometry.py`
  (round-43 C1; the frozen round-42 counter scores 37 fixtures byte-exactly against the contract). The reported `size`
  is the animation's goal, not the value on screen, and a tiled client never reads the rule — so AGREE, DIFFER, TILED
  and BADSIZE are read-only joins, not health calls. Still open: whether Hyprland applies a rule's size to a live window
  on this host (no gkeep window was open; an oracle observation, if obtained, is reported and not scored), the rendered
  size after the animation, the client's own request path, and rule attribution.
```

### Why this bullet, and what it does not claim

- It names the **new** surface (a rule-size ↔ reported-size join) and the two artifacts (entry, tool) that carry it. It
  does not move any earlier Frontier item: the "per-window rule effects" item stays open (the join reads two printed
  values; it does not attribute an effect), and the "rendered UI" item stays open (the goal box is not pixels).
- The "still open" clause is the registration's own residual, restated: the live-application question is a compositor
  fact the counter does not score, and no gkeep window was open on 2026-10-26 (`fetch/host-clients-r43.json`, 4 clients,
  `floating=false`, size 1720x1414).
- No C1 number is claimed beyond what the frozen instruments say: the round-42 counter is the scorer, the reference is a
  control and not the deliverable, and the tool's own `--selftest` is not a corpus claim.
