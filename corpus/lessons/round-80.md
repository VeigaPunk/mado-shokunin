# mado round 80 — the composition under the band, and two matcher classes (2026-11-04, hyaku run 15)

Claims: **C1 coverage** — a second exclusive layer surface composes under the running usable box:
thirty-three frozen cases 33/33 (the twenty-three round-79 cases carried unchanged, parsed-equal),
twenty-two named mutations killed 22/22, the held round-79 tool `base_correct=23/33`, tool selftest
111/111; **C2 operability** — the read-only runbook gains a chord grammar over the keybindings chord
column and a state/exit-status matcher for `systemctl --user is-active` (24 cases / 24 rows / 24
distinct anchors, `control_new=0/2`, sixteen matcher mutants killed). Freeze
`6c302a53eb8f577e83fbcadc01e05a286778df8e`; base `e10f7e9f528b13195a1cdde28a68a702af3045c4`.
Declaration: `.ufo/waves/round-80/claims-declaration-r80.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M80-1 | reference-drift: the round-79 report's C1 after-cell quotes `tool_selftest=44/44` at `d6be05ef` while citing `receipts/measurement-final-r79.txt`, whose committed bytes print `50/50` at `999a4a3f` (44/44 is the R1 receipt `measurement-c1-r79-repair.txt`) | round-79 closure D1; `grep -n 'tool_selftest' .ufo/waves/round-79/receipts/measurement-final-r79.txt` → `50/50`, and `measurement-c1-r79-repair.txt` → `44/44` | QUALITY 118 (replay the declared command before filing) does not read a *quoted receipt line* against the file; nothing did | every Before→after cell in this round's report copies its tally from the receipt's literal line and names the file; the r79 sentence fails the check by construction (`grep -c 'tool_selftest=44/44' measurement-final-r79.txt` → 0 while the cell says 44/44). Erratum appended to this round's report (§ Errata) |
| M80-2 | attribution: S467's rejection reason said the source "documents the line syntax only", while the committed fetch states the stacking in prose at `:183` | round-79 closure D2(a/b); `.ufo/waves/round-45/fetch/wiki-Monitors.md:183` = "This does stack on top of the calculated reserved area (e.g. bars)." | the rejection was written from the line-syntax line alone; no rule requires the reject reason to quote the whole passage it denies | a new rejected row **S475** whose `teaches` opens `supersedes S467 —` and names the dead URL, the missing pin and the tier-B scope, quoting `:183`; shown able to fail: the old reason's text ("syntax only") contradicts the quote S475 carries, and `grep -n 'stack on top' .ufo/waves/round-45/fetch/wiki-Monitors.md` prints the sentence |
| M80-3 | number-drift: LOG.md's round-79 entry says "Seven mined" while `corpus/lessons/round-79.md` carries eight `## Mistakes` rows (M79-1…M79-8) | round-79 closure D3; `grep -c '^\| M79-' corpus/lessons/round-79.md` → 8 | no counter cross-checks a LOG sentence against the lesson table it summarises | a `## Corrections (round 80, append-only)` block at the end of LOG.md names the eight; shown able to fail: the appended line contradicts the entry above it, and the count command prints 8, not 7 |
| M80-4 | scope: `.ufo/waves/round-79/fetch/S468.bin` and `S469.bin` were described as "pinned as S468/S469" but have no `SOURCES.md` rows and no manifest entry — the names read as registry ids | round-79 closure D4; `grep -cE '^\|[[:space:]]*S468[[:space:]]*\|' corpus/SOURCES.md` → 0 while `ls .ufo/waves/round-79/fetch/S468.bin` → the file | `sources-census.sh` validates registry rows, not file names inside a wave dir | new ids start at **S470** (S468/S469 stay unused) so no row retroactively blesses bytes no round opened; this lesson names both files as fetched-but-unregistered. Shown able to fail: `S468` is still unregistered (`grep -c` → 0), and the round-80 fetch manifest lists exactly five pins (`sha256sum -c fetch/sha256-r80.txt` → 5/5 OK, no self-entry) |
| M80-5 | landing: the round-79 wave's `R79ExecC1Tool` settled without a `.md`; its `out.txt` (73 OK / 0 FAIL against the pre-R2 tool) is the only trace and cannot be audited | round-79 closure D5; `ls .ufo/waves/round-79/w1/R79ExecC1Tool/` → `out.txt` and no `findings.md` | the seat prompt did not require a findings file, only a report trailer | every r80 seat prompt names `findings.md` and a final `STATUS:` line, and the wave results are read against `ls .ufo/waves/round-80/w1/*/findings.md`; shown able to fail: a seat that writes only `out.txt` is visible as a missing `findings.md` in that listing |
| M80-6 | reference-drift (caught inside the round): the S473 row's anchor said the mask table runs `:100-120` and holds "the twelve masks"; the pinned bytes hold sixteen `s/^N,/` rules over `:100-115` (the twelve is the count of distinct rendered tuples this host's binds produce), and the S472 row's empty-case span said `:40-52` where the bytes say `:39-52` | wave seat `R80ScribeSources` §3; `.ufo/waves/round-80/fetch/S473.txt:100-115` (`grep -c 's/\^'` over that span → 16) and `S472.bin:39-52` | nothing did: the rows were written from the seat brief's own wording, and the census checks row shape, not whether an anchor's span is true | two superseding rows, **S476** (S473) and **S477** (S472), each with `teaches` opening `supersedes S4NN —` and the corrected span/count; entry §10 records both. Shown able to fail: `awk 'NR>=100 && NR<=115' S473.txt | grep -c 's/\^'` prints 16, and lines 116-120 hold the closing brace and `static_bindings`, so the old `:100-120`/twelve reading cannot be reproduced |

Sweep for a sixth: `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py quality/counters/c1-r80-multisurface.py quality/counters/c2-r80-runbook.py` → no output (2026-11-04, at the freeze).
Second sweep (dead keys in the two new control sets): the C1 case keys are read by `case_files`/`expected_ok` (`config`, `layers`, `layers_raw`, `monitors`, `rules`, `surfaces`, `monitor`, `expect`, `name`) and the C2 keys by `case_correct`/`held_rule` (`argv`, `kind`, `value`, `samples`, `negatives`, `frozen`, `skill_anchor`, `fixtures`, `tool`); `python3 -c "…set(case)-{'name','config','layers','layers_raw','monitors','rules','surfaces','monitor','expect'}"` prints nothing for the C1 set, and the C2 set's extra keys are `tool`/`fixtures` only on the four refusal cases the counter reads.

## Gate (sources opened this round)

Census at round start `e10f7e9f` → 404 registry rows, `sources-census.sh validate --root …
mado` exit 0 (standing W04 duplicate-URL warnings); at round end → 412 rows, exit 0. Eight rows
added (seven mined, one rejected; three are supersede rows — S475 supersedes S467, S476 supersedes
S473, S477 supersedes S472). No `status`/`used-by` cell of an older row moved; one `recheck` cell
moved in place (S475 `on-change` → `180d`, because a 404 URL cannot fire an on-change re-probe) and
is logged here old→new. All five newly fetched rows are pinned under `fetch/` and verify 5/5 with no
self-entry (`sha256sum -c fetch/sha256-r80.txt`); S473/S476 and S474 are read from the installed
payload and the installed man page.

| row | source and locator (opened 2026-11-04) | status | located quote (≤25 words) | what it licenses / does not |
|---|---|---|---|---|
| S470 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp — `applyExclusive` `:2529-2586`, `arrangeLayerArray` `:2587-2671`, `arrangeLayersForMonitor` `:2673-2700`; sha256 `9af8a74e…`, 143211 B (byte-identical to the round-78 pin S457) | mined (new) | `if ((exclusiveEdge == edges[i].singular_anchor \|\| anchor == edges[i].singular_anchor \|\| anchor == edges[i].anchor_triplet) &&` (at `:2575`) | the first-match edge rule and its guard; it does not say which surface contributed a band (nothing does) |
| S471 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/LayerShell.cpp — `setSetExclusiveZone` `:100-102`, `setSetExclusiveEdge` `:156-169`; sha256 `ad9314da…`, 9935 B | mined (new) | `"Exclusive edge doesn't align with anchor"` (at `:163`) | an exclusive edge outside the anchor set is a protocol error, so the join refuses such a declaration; it does not say how the compositor arranges the box |
| S472 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/tests/desktop/Reserved.cpp — the parent/child case `:32-38`, the empty cases `:40-52` (corrected by S477 to `:39-52`), the not-contained case `:53-54`; sha256 `37988cca…`, 1532 B | mined (new) | `EXPECT_EQ(e.ok(), false);` (at `:54`) | a child box outside its parent is an invalid area with a zeroed result; it does not specify the runtime path that builds it |
| S473 | `~/.local/share/omarchy/bin/omarchy-menu-keybindings` (installed omarchy payload, 251 L) — the modmask table `:100-120` (corrected by S476 to `:100-115`, sixteen rules), the `code:201` rewrite `:50`, the mouse-button symbols `:58-66`, `parse_bindings` `:164`; sha256 `3487bbb8…` | mined (new, own-work) | `printf "%-35s → %s\n", key_combo, action;` (at `:164`) | the chord column's shape and the twelve modifier renderings the grammar accepts; it does not say which binds exist |
| S474 | `man systemctl` on this host — systemd 262 (262.1-1-arch); the `is-active PATTERN...` paragraph; sha256 `d3c36760…` | mined (new) | `Returns an exit code 0 if at least one is active, or non-zero otherwise.` | the row must bind the state word and the exit status together; it does not enumerate every state word |
| S475 | https://wiki.hypr.land/Configuring/Monitors/ as committed at `.ufo/waves/round-45/fetch/wiki-Monitors.md:179` and `:183`; the live URL **404s** on 2026-11-04 | rejected (new; supersedes S467) | `This does stack on top of the calculated reserved area (e.g. bars).` (at `:183`) | REJECTED: dead live URL, no revision pin, tier-B prose only — and it *does* state the stacking, so S467's "syntax only" reason was too narrow; flip: a resolving, pinned page stating the static-plus-dynamic arithmetic |
| S476 | the same installed payload as S473, re-read: `~/.local/share/omarchy/bin/omarchy-menu-keybindings` `:100-115` and `:164`; sha256 `3487bbb8…` | mined (new; supersedes S473) | `-e 's/^77,/SUPER SHIFT CTRL ALT,/'` (at `:115`) | the mask table's last rule and the sixteen-rule span; it does not say which masks a host's binds actually use |
| S477 | the same URL as S472, re-read: `tests/desktop/Reserved.cpp:32-54`; sha256 `37988cca…` | mined (new; supersedes S472) | `EXPECT_EQ(e.ok(), false);` (at `:54`) | the not-contained verdict with its corrected span; it does not read the zeroed area |

Precision notes for the closure: the S470 anchor names the whole `applyExclusive` and
`arrangeLayersForMonitor` ranges; the quoted line `:2575` is inside `applyExclusive`. S470/S471/S472
intentionally duplicate URLs held at other scopes (S457, S458/S459, and the round-78 pins), so the
census's standing W04 warnings are expected. S475 is the supersede row CORPUS.md rule 2 requires;
`status` stays `rejected` because the narrowed reason still rejects.

Admit/reject sample for the non-author spot-check: admit S470 and S472 (the two rules the claim
rests on), reject S475 (same reason as filed, narrowed).

## Wave findings (append-only; written as the seats settle)

Seats: 14 in one v1 wave (`w1-spec.json`, `w1-dispatch.json`, `w1.ready`). Findings land here as the
wave reports; a seat that settles without a report is disclosed, never backfilled.

**R80ScoutLive** (scout; `w1/R80ScoutLive/findings.md`, STATUS: ok). Live recon on today's host:
both registered joins reproduce `receipts/live-join-r80.txt` byte for byte (`CLEAN`, rc 0); the host
carries exactly two layer surfaces (`waybar` level 2 `0,0,3440,26` pid 1720; `wallpaper` level 0
`0,0,3440,1440` pid 1722), levels 1 and 3 empty, `reserved [0,26,0,0]`; the composition run prints
`gt=0,26,0,0 attr=0,26,0,0` so nothing is unattributed. Two named limits: **(a)** `--surfaces`
cannot express "no extras" — an empty declaration is refused `stage=setup` (`tools/mado-barfoot.py`,
the `the surfaces declaration is empty` branch), so the honest no-extras run is the omitted flag;
**(b)** `hyprctl layers -j` carries no anchor and no exclusive-zone field, so a declaration is pinned
only where the box moves with the field — the seat's `exclusive: 0` probe (same captures, box
`0,26,3440,1414`, `verdict=DIFFER`) is what pins `exclusive: -1` for `wallpaper`. The real
`is-active` answer here is `inactive` rc 3, with a contrasting active unit
(`wayland-wm@hyprland.desktop.service`, rc 0) available as a discriminating row.

**R80ConnSiblings** (connector; report at `w1/R80ConnSiblings.md`, STATUS: ok). No sibling claims
either claim's ground: `game-dev-3d/PROVINCE.md:75` explicitly cedes "desktop/compositor display
behavior" to mado, `kotoba/PROVINCE.md:72` and `tsukuroi … adjacency-anchors-r19.md:84` both cite
mado's ownership of the Hyprland/waybar plane, and no sibling `tools/` file models a layer surface
(the only `exclusive` tokens in sibling tools are lock modes and argparse flag conflicts). Two
homonyms are named so a later census does not merge them: tabi's "chord" is a browser input-event
construct, not the keybindings text column; kake's `is-active` line is an adjacent observation about
a different unit, not the verb's rc↔state mapping. Two cautions: kotoba's round-74 sibling census
(`sibling-overlap-census-round74.md:66`) is pinned 363 commits behind this base and predates
`tools/mado-barfoot.py`, so it clears nothing; and no staged `merge/mado/` entry touches r80 ground
(one future reconciliation: `host-bar-producers-r28.md:12`'s 6354 B claim about the host waybar
config, which a later landing check must re-measure).

**Evidence pointers, re-pointed by the wave's lesson seat** (append-only; the rows above stand,
these are the byte-exact cells seat `R80ScribeLesson` re-derived, `w1/R80ScribeLesson/mistakes-r80.md`
§1): M80-1 `.ufo/reports/round-79/mado.md:95` vs `receipts/measurement-final-r79.txt:41` and
`receipts/measurement-c1-r79-repair.txt:38`; M80-2 `.ufo/waves/round-45/fetch/wiki-Monitors.md:179`
and `:183`; M80-3 `LOG.md:3928` vs `corpus/lessons/round-79.md:15-22`, with a probe that exits 1 on
`git show 6c302a53:LOG.md` (`rows=8 correction=no`) and 0 on `git show b65f3227:LOG.md`
(`rows=8 correction=yes`); M80-4 the twelve `S*` stems under `.ufo/waves/round-79/fetch/` against the
ten manifest entries, the files named at `.ufo/reports/round-79/mado.md:211` and
`corpus/lessons/round-79.md:20`; M80-5 the r79 seat directory holding `drive.py`, a copied
`mado-barfoot.py` and `out.txt` with no `.md`, against 13 of 14 seats that did file `w1/<name>.md`.
The seat also named the limit I keep: the runner's `Report:` trailer and the seat brief's
`w1/<name>/findings.md` are two paths by construction (two r80 seats followed the trailer), so
M80-5's fix is "one canonical path *first*", not "one path exists".

**Seat-copy redaction (security duty, applied by the L1).** `w1/R80ScoutLive/monitors.json` was the
seat's raw `hyprctl monitors -j` capture and carried the monitor's EDID-shaped `description` and
`serial` under the r78 L0 question's R5 rule; the L1 replaced `description`, `serial`, `make` and
`model` with `<redacted: …>` before committing the seat report, and the lane receipt
(`receipts/live-join-r80.txt`) never printed those fields. The join reads name/size/`reserved`/
scale/transform only, so the redaction costs no evidence. `grep -rn 508AZFMF7323` over the round-80
files prints nothing.

**R80ExecC1Run** (executor; `w1/R80ExecC1Run/findings.md`, STATUS: ok). Ran the C1 counting command
verbatim at the freeze (rc 0, `TARGET_MET`), then re-derived `overlay-compose-top`,
`same-level-order` and `ls-area-invalid` by hand from `S470.bin` (four-band arithmetic with the
running-usable-box shifts) without reading the tool's code, built the three fixtures from the frozen
set and ran the tool on them: **every field AGREE** (`band`/`expected`/`attributed`/`attr`/`boxes`/
`ls`), and both selftests green (`tools/mado-barfoot.py --selftest` 111/111, the C1 counter 60/60).

**R80ScribeSources** (scribe; report at `w1/R80ScribeSources.md` plus `sources-rows-r80.md`,
STATUS: ok). Drafted the six rows and verified all six quotes against the fetch bytes; its **F1** is
the one substantive catch — the committed S473 anchor said the mask table runs `:100-120` and holds
"the twelve masks", while the bytes hold sixteen `s/^N,/` rules over `:100-115`; F2 corrected S472's
empty-case span to `:39-52`. Both became supersede rows S476/S477 (this lesson's M80-6) and the
committed Gate cells now point at them. F3 named the expected W04 warnings for S470/S477.

**R80ScribeLesson** (scribe; `w1/R80ScribeLesson/{findings.md,mistakes-r80.md}`, STATUS: ok). Its
draft carries the five routed defects with byte-exact evidence pointers (folded into this lesson's
re-pointed block) and a probe matrix for each fix's red side. Its finding against the landed lesson:
12 of 14 r80 task bodies name the canonical `findings.md` path explicitly while 2 carry only the
shared context sentence (one canonical path first — the r80 wave still produced two root-level
`<name>.md` reports, `R80ScoutLive.md` and `R80ConnSiblings.md`, from seats that followed the
runner's trailer); M80-5's green is not yet observable because the wave had not closed.

**R80ScoutModel** (scout; `w1/R80ScoutModel.md`, STATUS not yet read at this append — the report is
present and its class table is 27 rows). Probed 28 declaration quadruples against the frozen tool and
the sources. Correct where unpinned: monitor origin `x/y ≠ 0`, static plus a second exclusive
surface, `exclusive == 0`/`-2` bounds, a lower-level non-exclusive surface, an exclusive surface with
an empty box, a left/right attribution vector, a non-top bar, a negative anchored margin with a
positive sum, a same-namespace duplicate (refused, `stage=model`). **Wrong on four reachable
classes** (recorded as entry §11 / SCORECARD limits, made round 81's ground): the centring formula is
not `CBox::round` at a negative tie (1001-wide panel on a 1000-wide monitor → tool `x=0`, source
`-1`/w `1002`); an `auto` zone on a dynamic band size is taken from the declared `0` instead of the
allocation (`S464:276-280`), so a lone auto/dynamic surface reads `DIFFER` deterministically; `auto`
on a corner/parallel anchor pair prints a zone gtk never sends (`S464:269-288`); and a declared
surface without an `exclusive` key defaults to `auto` where the protocol's default is `0`
(`S460:183`). None of the four touches the frozen thirty-three, and no expectation, mutant or target
moved.

**R80ScribeEntry** (scribe; `w1/R80ScribeEntry/findings.md`, STATUS: ok). Its draft entry was not
adopted — the L1 had already landed `corpus/knowledge/bar-footprint-composition-r80.md` — but the
seat's review found one **real instrument defect**: `evaluate_composition` read
`boxes[order.index(0)]` while `boxes` is appended in arrangement-sequence order, so the printed
`box=` field would name another surface's verdict for a non-exclusive bar with an exclusive surface
sorting after it (reachable, not in the frozen 33; the `verdict` itself stayed correct). Repaired as
**R1** (`boxes[sequence.index(0)]`), the case set and target unchanged, re-measured at the repair
commit (`receipts/measurement-c1-r80-at-tip.txt`, tool sha256 `5b9e2930…`). It also caught the C1
counter's stale docstring contract (`cases=30 … base_correct=23/30` → `33/23`) — repaired in the same
commit — and six citation errors in the landed entry (the `box.round()` line, the
`ReservedArea.cpp` ranges, the C1 `source:` line naming the two C2 rows while omitting S464/S458,
the match-condition span, and §7 item 4's conflation), all now in the entry's §12 errata. Its F4 is
correct and stays a limit: `preview_scale` has no pin this round, so the entry names it unmodelled
without asserting a mechanism.

**L1 note on C2's chord grammar (limit, named not fixed).** The row binds
`omarchy menu keybindings --print | cut -c1-35`, and `printf "%-35s → %s"` pads the chord to 35
columns; a chord longer than 35 columns (a long keysym under three or four modifiers, e.g.
`SUPER SHIFT CTRL ALT + XF86AudioRaiseVolume` at 47) is truncated by `cut` and then reads as a
shorter chord that still parses, so the grammar cannot see that truncation. Today's longest chord on
this host is 29 columns (`omarchy menu keybindings --print | cut -c1-35` → max 29), so no live
instance exists; a later round that wants the guard needs a `max_chord_len` field and a truncated-line
negative, which the frozen set cannot carry without a new round.

**L1 repair R2 (C2 grammar).** A live-byte check of the chord column found 41 lines reading
`SUPER +` (a keycode whose symbol map is empty) in one invocation, none in the next — the
formatter's keymap resolution is intermittent, and the grammar rejected that shape. Repaired in the
counter: a line ending ` +` is a chord with an empty key; a *padded* key (`SUPER +  X`), a doubled
key, a foreign modifier, a numeric mask, a repeated modifier and an arrow still fail, and the
`chord-key-padded` mutant was re-cut to drop only the strip check. Selftest 80 → 81, no case, sample,
negative, expectation, mutant or target moved. Named consequence: the row's live answer depends on
the formatter's `xkbcli compile-keymap` map being populated, which is why the empty-key shape has to
pass — the old grammar would have failed the row on a host whose keymap cache was cold.

**R80Sentinel** (sentinel; `w1/R80Sentinel/findings.md`, STATUS: ok — no high/medium boundary
defect). Its three findings: **F1 (LOW)** the C2 counter handed every child the caller's whole
environment (carried from r79); **F2 (LOW)** it pinned no `TMPDIR`, so the no-`/tmp` property was
implicit; **F3 (INFO)** `parse_surfaces` accepts negative surface margins and an `exclusive` below
−1, both inert because `apply_exclusive` only shrinks when `zone + margin > 0`. F1 and F2 are
repaired as **R3** (an allowlisted child environment plus `TMPDIR` inside the scratch root; 24/24
re-measured); F3 stays a named model limit.

**R80ReviewerC2** (reviewer; `w1/R80ReviewerC2/{findings.md,<name>.md}`, STATUS: ok). Its review
independently found the empty-key false negative (F1, HIGH — repaired as R2) and three residuals,
one of which is a **real defect repaired here**: **F3 (MEDIUM)**, the state matcher pinned a non-zero
status to 3 while the man page only promises non-zero, a nonexistent unit answers `inactive` rc 4,
and systemd's own `is-active` treats `reloading` as active (`arg_states`), so a genuine `reloading`
reply (rc 0) was wrongly rejected — repaired as **R4** (`(rc == 0) == (text in ("active",
"reloading"))`, 24/24 re-measured). Named limits it leaves for the next set: **F2** the
`code:201 → COPILOT KEY` rewrite is mask-65-only and a leaked `code:201` token is accepted (no frozen
negative covers a `code:` token, so a narrowed rewrite would pass); **F4** the frozen enum omits
`maintenance`/`refreshing` (systemd 262's ACTIVE table) and carries `unknown`; **F5** >35-column
chords truncate and still parse; **F6** five of the eight keybinding negatives are synthetic (a
double space, a numeric mask, a repeated modifier, an arrow and a doubled key cannot come out of the
piped formatter), which is fine as mutant-killers but not host-faithful; **F7** prose counts.

**R80ExecC2Run** (executor; report at `w1/R80ExecC2Run.md`, STATUS: ok). Re-ran the C2 counting
command at the measured rev (rc 0, `TARGET_MET`), captured both new rows' real replies
(`chords.txt`, `state.txt` + `state.rc` = `inactive`/3), and wrote an independent checker
(`chords-check.json`): 193 lines, 169 chords, 24 bare lines in 23 distinct forms (`F9` ×2, `PRINT`,
`COPILOT KEY`, both `switch:` keys and 18 `XF86*` keys), **zero hard failures**, and 12 distinct
modifier renderings — the count the S476 supersede row now records as the *rendered* tuples rather
than the table's sixteen rules. It flagged three multi-word-key lines (`COPILOT KEY`,
`SUPER + LEFT MOUSE BUTTON`, `SUPER + RIGHT MOUSE BUTTON`, both `switch:` keys) as soft notes; the
grammar accepts them (a key may be more than one token), which is what the formatter's own
`code:201`/mouse-button rewrites produce.

**R80CriticClaims** (critic; `w1/R80CriticClaims.md`, STATUS: ok). Its verdicts, recorded as they
stand: **Q1c (accepted)** — C2's declared before-state is a *setup refusal*, never a verdict, and the
refusal is structural (the counter pins `CASES=24`, the round-80 section title and a 1:1 anchor
binding, so it refuses the base revision at any tree); the C2 claim is therefore **one-sided**
(after-only plus mutant kills), not a measured before→after. It demonstrated the honest fix on a
labelled copy (key the section by `round \d+`, score a zero-hit anchor as `row=-1`, waive the tree
binding for the before-run): `rows=22/24 → 24/24`, `verdict=TARGET_MISSED rc 1` at the base — that
becomes round 81's instrument, since a rule changed after a seat scored is not this round's rule.
**Q1d (accepted as a named limit)** — removing the `cases[:CARRIED] == carried` comparison lets a
tampered set certify a weakened tool; the check is present and the control sha is printed, but the
sha is not compared to a frozen constant (the r79 counter-self-mutation limit, unchanged).
**Q2** — the claims are causally separable as landings but C2's verdict is gated on C1's bytes (both
live in one checkout); named, not a claim defect. **Q3** — C1 is coverage-shaped and C2
operability-shaped, distinct axes; its caveat is adopted in the report: C1's denominator is a new
diagnostic model-space, so the round must **not** book it as a move of an existing coverage score
(the U-route 7/7 and rubric-V 6/6 rows are untouched).

**R80ReviewerC1** (reviewer; report recovered from `w1-results.json` into `w1/R80ReviewerC1/`, STATUS:
ok — the seat settled without writing a file). Verdict: **C1 SUPPORTED as measured; no falsifying
finding.** It re-ran the counter (`33/33`, `22/22`, `base_correct=23/33`, selftest 60/60) and
re-derived five cases by hand: `same-level-order` (order-desc sort quoted, 36 + 26 = 62),
`overlay-compose-top` (26 + 40 = 66), `ls-area-invalid` (the decisive fork: `CBox::empty()` is
`|w| < ε ∨ |h| < ε` in hyprutils, so the negative-height child takes the *not-contained* branch,
`m_ok = false`, and the whole layer reserve — the bar's 26 included — is zeroed, static band
untouched), `empty-box-skip` (the `continue` precedes `applyExclusive`; also live-unreachable because
the protocol commit guard refuses a zero desired size without both-vertical anchors) and
`full-box-vs-usable` (`exclusive == -1` arranged on `full_area`). Predicate honesty confirmed: the
r79 tool has no `--surfaces` argument at the base and cannot emit `boxes`/`attr_ns`/`attributed`,
which all ten composition cases require, and the 22 mutants are single-anchor by construction
(`apply_mutation` enforces one occurrence) with ten of them in composition paths. Its three minors:
the C1 docstring drift (repaired in R1), the S472 span (repaired as S477), and a **boundary-label
nit** now in entry §11: an *exactly empty* composed box zeroes via the `empty()` early return with
`ok() == true`, while the tool prints `ls=INVALID` — the numbers agree, the label differs, and no
frozen case sits on that boundary.

**Dead and partial seats (disclosed, never backfilled).** `R80ExecMutants` settled with a 590-byte
progress note and no findings (it had located the seven checks and was planning the tamper probes);
`R80MutC1Counter` settled with a 457-byte progress note, a byte-identical pristine copy of the C1
counter and a full baseline run (`w1/R80MutC1Counter/baseline.out`, which reproduces the freeze
measurement verbatim); both died provider-side on the zai 429 path the orchestrator reported, and
their assignment (the counters' own load-bearing checks) stays open ground — the critic's Q1d and
the r79 counter-self-mutation limit are the standing record of what that work would test.
