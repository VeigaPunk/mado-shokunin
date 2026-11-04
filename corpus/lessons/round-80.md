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
