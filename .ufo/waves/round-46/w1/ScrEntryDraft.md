# Seat ScrEntryDraft — C2 entry prose (round 46, w1)

**Status: complete.** Deliverable is a set of drop-in blocks for the C2 draft entry, plus two receipts: a locator
verification of every compositor claim I added, and a C2-counter run on the draft with my blocks merged, showing the
merge is still admissible.

## Behaviour

Rewrote three blocks of `.ufo/waves/round-46/l1-draft/entry.md` for the L1 to merge (the entry itself is untouched):

| block | replaces | what changed |
|---|---|---|
| R1 `## Reading a DIFFER or a FALLBACK` | entry.md:59-65 | four hunches become an ordered decision list: FALLBACK mechanism (failed compile + reset quintuple, and the same quintuple from a runtime keyword), DIFFER in four mechanisms (stale `hyprctl keyword`, unsourced `source` file, block name the compositor never uses, `kb_file`), and the two "looks wrong but can't be a DIFFER" cases (`enabled = 0`, `switchxkblayout`). Every sentence carries a locator. |
| R2 `## Running the join on this host` (new) | inserted after entry.md:57 | the two exact read-only commands, pipe form, `--selftest`, the exit-code order, "do not answer a DIFFER with keyword/reload", and the real host trap: the effective `input` block is split across two files (omarchy default sourced at `~/.config/hypr/hyprland.conf:11`, host file at `:17`). |
| R3 `## Limits` | entry.md:66-71 | ten limits instead of four: the compile is not reproduced (and only FALLBACK licenses that inference), the five names are the request rather than a readback (`kb_file`, virtual keyboards, `active_keymap` unread by the join), the unprinted device options, pointer scroll only where set, the unmodelled language (a recognised-form counter, not a parser — a directive spelled outside its form is unreported and its branch is read as active, and `source` is silently ignored), the C library's number grammar for `scroll_factor` (inf/nan/hex/overflow/denormal ⇒ NOT_COMPARED, while Hyprland reads the string with `std::stof` and clamps), a missing file leaving no trace, the log/overlay witness, the non-legacy parser, and shape-only output. |

R0 is a one-line optional amendment to entry.md:57, which calls the host's `input` config "one `input` block in
`~/.config/hypr/input.conf`"; three of the five keyboard names in effect come from the omarchy default file instead. R4 is
a one-locator amendment for the live-run paragraph's touchpad sentence, which otherwise states a global-option claim with
no locator of its own (`Hyprland-ConfigValues.cpp:324`).

No `S###` id was added, no line names a cited id, no fenced block is proposed for the entry (the command example is
indented, so the entry's fence rule never sees it), and no existing locator is deleted — the 28 clause-j surfaces keep the
lines the freeze needs (step 2's `hyprlang-config.cpp:885-899`, step 3's `Hyprland-InputManager.cpp:1270-1280`, step 5's
`Hyprland-HyprCtl.cpp:785-802`).

## Gates

1. **Locators (all computed, none typed).** `verify-locators.py` → `verify-locators.txt`: 42 locators over 8 cited
   files (7 pins + `mado-devices.py`), each anchor found by grep at a line inside the cited range, every range `<= 30`
   lines wide and inside the file, and every locator written in `sections.md` required to appear in the table.
   `SCR_ENTRY_DRAFT VERDICT: PASS (failures=0)`, 88 PASS/IN-TABLE lines (42 locator checks, 42 distinct locators found
   in `sections.md`, 4 host-config checks).
2. **Merge admissibility.** A scratch clone at the freeze `8c5434c6…`, my merged entry as `l1-draft/entry.md`
   (`sha256:5d322550a184e0f5…`), `build-pos.py`, then `c2-r46-input-device-entry.py --base b22ea56b…` →
   `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1 verdict=TARGET_MET` at scratch rev `fbc38d36`, **28/28
   clause-j surfaces cited=1** (`c2-preview.txt`). So the new prose neither breaks the census line (clause h) nor loses a
   surface, and clause i's receipt-token rule is unaffected (my lines carry verdict tokens but cite no
   `.ufo/waves/round-*/receipts/` path). The same run was repeated after the late R3 additions and still scored 28/28.
3. **Host claims.** Verified in the same receipt: `~/.config/hypr/hyprland.conf:11` sources the omarchy default
   `input.conf`, `:17` the host one, `:23` a glob; the omarchy file sets all five `kb_*` keys, the host file sets
   `kb_layout` and `kb_options` only.

## Touched surfaces

- Written, all inside the seat: `w1/ScrEntryDraft/{sections.md, entry-preview.md, verify-locators.py,
  verify-locators.txt, merge-preview.py, c2-preview.txt}` and this report. No lane-tracked file edited; the frozen
  registration, counters, fixtures, controls, reference, pins and `l1-draft/entry.md` are unmodified.
- Read-only compositor reads used: `hyprctl version` (Hyprland 0.56.2 at efb50993), `hyprctl getoption input:kb_layout`,
  `input:kb_options`, `input:kb_variant`, `input:kb_model`, `input:kb_rules` (all `-j`). No `devices -j` re-run (the L1
  receipt already has it), no `keyword`/`reload`/`dispatch`/`switchxkblayout`, no Wayland client, no input injection.
- Host config read only: `~/.config/hypr/hyprland.conf`, `~/.config/hypr/input.conf`,
  `~/.local/share/omarchy/default/hypr/input.conf` (no values quoted beyond key names).
- Git: one `git clone --shared` of the lane into scratch, `checkout --detach` and one commit inside that clone only
  (`rev-parse --show-toplevel` asserted equal to the clone first). No git/jj mutation in the lane or the fleet.
- No package transaction, no tool install (nothing was needed). Scratch clones (548 MB) deleted; the seat's scratch dir
  is gone.

## Findings worth the L1's decision

1. **entry.md:57 understates the host's `input` config.** Live `getoption` reads show `input:kb_variant`, `kb_model` and
   `kb_rules` are `set=true` from the omarchy default file while the host file overrides only `kb_layout` (br) and
   `kb_options` (compose:caps). The live run passed only `~/.config/hypr/input.conf`, so its AGREE on those three names
   is agreement with the built-in default, not with the file that set them — right by value (both files leave them
   empty), not by evidence. R0/R2 fix the wording.
2. **`source` fails silently in the join, not loudly.** The docstring's "a `source =` line it does not follow"
   (`mado-devices.py:20`) is accurate, but `source` is neither a `device` nor `input:kb_*` key, so it is not counted in
   `unsupported` and cannot raise NOT_COMPARED — the sourced block is simply missing from the expectation. R1 item 2 and
   R3 say this; a reader who assumed NOT_COMPARED would be wrong.
3. **`active_keymap` is the one field read out of the compiled keymap** (`Hyprland-HyprCtl.cpp:793-794`,
   `Hyprland-IKeyboard.cpp:306-321`) and the join never compares it. Step 6's "not a witness of the keymap in use" is
   true of the five names but leaves out this partial witness; R3 states it as a limit rather than editing step 6, since
   a claim change there is the L1's call.
4. **The existence test and the value lookup disagree on spaces.** `deviceConfigExists` maps `' '` to `'-'` before the
   key compare (`Hyprland-ConfigManager.cpp:1196-1201`) while the value lookup compares the stored key exactly
   (`hyprlang-config.cpp:1083-1099`), so a block named with spaces can be found for `enabled`/`keybinds` and missed for
   every `kb_*`. R1 item 3 states it; it also means "the block exists" is not the same question as "the block applied".
5. **A reload really does clear keyword values.** `parse()` calls `clearState()` before reading files
   (`hyprlang-config.cpp:915-926`) and `clearState` drops non-static special categories (`:1070-1076`), so the
   "survives a reload ⇒ not a leftover keyword" test in R1 is sound; `hyprctl keyword` itself re-applies input configs
   immediately (`Hyprland-HyprCtl.cpp:1203-1208`), which is why a keyword shows up in the dump before any reload.
6. **`scroll_factor` spellings are a declared blind spot, now written into Limits.** Hyprland hands the string to
   `std::stof` (`hyprlang-config.cpp:465-471`) and clamps the result to 0..100 (`Hyprland-InputManager.cpp:1379-1382`),
   while the join accepts only a decimal prefix and counts inf/nan/hex/infinite/denormal as unsupported
   (`mado-devices.py:62-66`) — the disagreement is safe (NOT_COMPARED, never a false AGREE) but it was unstated. Raised by
   `ConnCrossClaim-3` (reference-only assumption F1) and now R3's sixth limit. I did not run the stof differential probe it
   proposes: recording the model difference needed no execution, and the probe belongs to the C1/v2 line.
7. **The join's directive rule is a recognised-form count, not a parser.** A `#` line matching `#[ \t]*hyprlang` counts
   (`mado-devices.py:39-42`), so a directive spelled outside that form is unreported and the branch it guards is read as
   active; `source` is silent in the same way. Raised by `ConnCrossClaim-3` (F5) and `SentTool-3` (harness F1/F2); R3's
   fifth limit now states both, so the entry no longer implies a guarantee the reference does not make.
8. **The live-run touchpad sentence had no locator of its own** (F3 from the same report): R4 supplies
   `Hyprland-ConfigValues.cpp:324` for `input:touchpad:scroll_factor`, verified in the same receipt.
9. **No conflict with a sibling seat observed.** Nothing in the frozen registration, the counters or the controls
   contradicted the text I wrote; the only correction to an existing claim is finding 1 (wording, not a wrong verdict).
   Cross-seat correspondence: `SentTool-3` and `ConnCrossClaim-3` were answered; their harness findings (C1 clause r,
   sandbox reach) do not touch my C2 receipts, and I added no counter, fixture or `quality/` file.

## Out of scope (not done, by assignment)

- The C1 tool (`tools/mado-devices.py`), rows S316-S325, the lesson Gate, the README row, and the install of the entry —
  L1 integrates; my `entry-preview.md` is a preview built from the frozen draft, not a patch to land.
- Re-running the C2 counter against the lane (done only against a scratch clone), any C1 scoring, and any jj/git write in
  the lane.

## Artifacts

- `.ufo/waves/round-46/w1/ScrEntryDraft.md` — this report
- `.ufo/waves/round-46/w1/ScrEntryDraft/sections.md` — R0/R1/R2/R3 with the merge map
- `.ufo/waves/round-46/w1/ScrEntryDraft/verify-locators.py`, `verify-locators.txt` — 39 locators, 43 PASS, failures=0
- `.ufo/waves/round-46/w1/ScrEntryDraft/merge-preview.py`, `entry-preview.md` — the merged entry used for the counter run
- `.ufo/waves/round-46/w1/ScrEntryDraft/c2-preview.txt` — `PRED-C2-r46: admitted=1/1 verdict=TARGET_MET`, 28/28 surfaces
