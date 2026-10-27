# Round 48 lesson — the XKB compile and the resolver cache (2026-10-26, hyaku run 9)

Lane mado-shokunin. Claims (`.ufo/waves/round-48/claims.md`; registration `.ufo/waves/round-48/registration.md`, freeze
`<AFTER>`): C1 operability (capability acquisition) `tools/mado-terminal.py` warm-cache path, judged by `PRED-C1-r48-<AFTER>`;
C2 coverage (sourced) `corpus/knowledge/xkb-keymap-compile-r48.md`, judged by `PRED-C2-r48-<AFTER>`. Base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585` (the round-47 non-author closure commit); the round-48 setup commit
`5ff167423ee410251da0ef0c82f8e6fa25875665` adds only `claims.md`, the w1 spec/dispatch and the census-before, so every count
below is the base state plus nothing but that setup. Round shape: two v1 waves — `w1` build (41 seats), then `w2` falsify
against the frozen v1 instruments (`.ufo/waves/round-48/claims.md:3-5`); no seat scores a frozen counter in `w1`.

**Draft status.** This file is the w1 skeleton, written by seat `ScrLesson` before the freeze and before any data commit.
Every `<AFTER>` marker below is a value that cannot exist yet: predicate names and freeze commit ids, admitted row ids and
GATE lines (from `w1/ScrRows`), rejects (from `w1/ScrRows` + `w1/ScoutXkbSpecs`), census-after, the two id-guard receipts,
the `considerthese` verdict, every mistakes row (from `w1/ScrMistakes`), and the closure acceptance results. Nothing in this
draft is evidence for a claim; the L1 integrates the frozen values around this prose. Two sections are drafted with content
already measured at the setup commit and say so: the census-before block (pasted verbatim) and the id-guard counts (recomputed
here from the dispatch artifacts).

## Gate

Candidates considered: two planes, one per claim.

- **C1 (cache edge).** The resolver's cache path, against the script already pinned in round 47 —
  `https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec` (pin
  `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256 `89f2be9a…27ac`, byte-equal to `/usr/bin/xdg-terminal-exec`), read
  cache first at `:1179`, `read_cache` at `:217-298`, `gen_hash` at `:179-215`, the background save at `:1455-1458`; the
  README's cache sentence (row S327). No new C1 rows are expected: the source of truth is the row-47 pin, re-read this
  round; `<AFTER>`: `w1/ScoutHeld` names every held row the cache paragraph touches, and `w1/RevengerCache` records which
  invalidation gaps upstream accepts. C1's executed evidence is the counter's primed warm run, not a source.
- **C2 (XKB compile).** libxkbcommon 1.13.2 tag sources and docs (`doc/rules-format.md`, `doc/user-configuration.md`, the
  compiler's include handling), xkeyboard-config 2.48 at the tag (rules/evdev, the symbols files the host's names take), and
  the host-read `xkbcli compile-keymap` receipt (`/usr/bin/xkbcli`, `/usr/lib/xkbcommon/xkbcli-compile-keymap`).
  `<AFTER>`: `w1/ScoutXkbSpecs` candidate list and `w1/ScrRows` rows/gate-lines. C2's ground at base is open in two places:
  `corpus/knowledge/hyprland-input-devices-r46.md:69` ("The XKB compile itself is not reproduced") and `corpus/README.md:112`
  ("the XKB compile itself").

Admitted: rows `S340`-`<AFTER>`, tier `<AFTER>`, status `mined`, opened `2026-10-26`, used-by
`corpus/knowledge/xkb-keymap-compile-r48.md`, continuing the registry after `S339` (276 rows at base). GATE lines are emitted
by `w1/ScrRows/gate-lines.md` in the round-47 shape — receipt path, sha256, and a ≤25-word quote located by a computed line
number — and pasted here by the L1:

```
<AFTER>: one GATE line per admitted row, in S-number order, from w1/ScrRows/gate-lines.md
```

Quote discipline for this round: each quote is ≤25 words, word-bounded, and unique in its receipt; `<AFTER>`: the list of rows
whose quote spans or de-spaces source lines, with the start line, as round 46 and round 47 stated theirs.

Held ground, deliberately not re-claimed (named so a later reader sees the overlap is a decision, not an omission):

- **S326/S327** — the resolver script and README (round 47, `mined`). C1 extends the tool against the already-pinned script;
  a new row on the same tag URL would be a duplicate with no new scope (`<AFTER>`: the census W04 line the round adds).
- **S318/S319** — Hyprland `src/config/values/ConfigValues.cpp` and `src/devices/IKeyboard.cpp` (round 46, held). The
  `us` fallback after a failed compile is cited, never re-claimed (`claims.md`: "cite, never re-claim"); C2 clause h asserts
  these rows and the round-46 entry byte-equal to base.
- **`corpus/knowledge/hyprland-input-devices-r46.md`** — its step 4 states the fallback; C2 answers the compile gap at its
  `:69` without rewriting the entry (append-only rule, `CORPUS.md` rule 2).
- **`corpus/knowledge/xdg-terminal-selection-r47.md`** — cold-cache selection. This round adds the warm path; the round-47
  entry's launch half stays `[UNK]` and is not restated.
- **`corpus/README.md:110`, `:112`** — the two open sentences this round moves ("the warm-cache path", "the XKB compile
  itself"); the frontier bullet below is where they close.

Rejected: `<AFTER>` — one `REJECT <source>` bullet per screened-and-refused candidate, each naming the decisive line and a
flip condition, from `w1/ScrRows` (at least two) and `w1/ScoutXkbSpecs`. Two rejection classes this round must state
explicitly, because they are the round's premise:

- a row on the **host binary** `/usr/bin/xdg-terminal-exec` as a separate source from the tag URL would cite the same bytes;
  the host is a pin comparison (`sha256sum` equality, round-47 precedent), not its own row. `<AFTER>`: whether that holds
  inside this round's rows (it should — no new C1 row).
- `<AFTER>`: whether the host xkb tree under `/usr/share/X11/xkb` (package bytes at xkeyboard-config 2.48) is reached by the
  package/tag pin or would need a host-bytes row; `w1/ScoutXkbSpecs` must decide, and the entry cites the tag pin, not the
  installed copy, unless the two are byte-equal.

### Census before → after

Before (`.ufo/waves/round-48/receipts/census-before.txt`, base `579f694b`, exit 0) — 17 `W04` lines and 1 `W01` line:

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
mado	W04	S303 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp across scopes
mado	W04	S307 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp across scopes
mado	W04	S317 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp across scopes
mado	W04	S318 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp across scopes
mado	W04	S320 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp across scopes
mado	W04	S321 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp across scopes
mado	W04	S324 duplicate url raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp across scopes
mado	W04	S326 duplicate url raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec across scopes
mado	W04	S327 duplicate url raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md across scopes
mado	W04	S332 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.cpp across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```

After `<AFTER>`: the same command at the round tip must exit 0; the new `W04` lines are the repeated URLs among
`S340`-`<AFTER>` (the script/README pins are already repeated, so the count may hold) and are listed here by row id; `W01`
count is `<AFTER>`.

Command (both ends): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.

### Registry changes

| surface | old (base `579f694b`) | new |
|---|---|---|
| `corpus/SOURCES.md` | 276 rows, top `S339` (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `276`; top by `sort -n | tail -1` → `339`) | <AFTER>: `276 + n`; rows `S340`-`<AFTER>` appended after the last `S` row, 11 cells each, tier `<AFTER>`, `mined`, opened `2026-10-26`, used-by the entry |
| `corpus/knowledge/` | 64 files | 65 (`xkb-keymap-compile-r48.md`) |
| `corpus/README.md` | 64 index rows (last the round-47 row at `:75`) | 65 (one three-cell row after `:75`), plus the `## Frontier` bullet at `:110` |
| `corpus/lessons/` | 70 files | 71 (this lesson) |
| `tools/` | 15 files, `mado-terminal.py` the newest | <AFTER>: 15 if C1 extends the file in place (expected), or +1 if a second model lands |
| held rows `S318`/`S319`, `corpus/knowledge/hyprland-input-devices-r46.md` | as at base | byte-identical (C2 clause h; command in the acceptance table) |
| `quality/` | `counters/c1-r47-terminal.py`, `c2-r47-terminal-entry.py`; `<AFTER>`: the r48 pair and the fixture schema | <AFTER>: `c1-r48-terminal-cache.py`, `c2-r48-xkb-entry.py`, `c1-r48-fixtures.json` (schema v2) |

### Renumber map

None this round, and the reason is measured: the registry's top id is `S339` (276 ids, `S001`-`S339`), the C2 block opens at
`S340`, and no supersession or staged adoption is drafted, so no row changes its id. The staged band still runs `S203`-`S349`
(147 ids) — the upper end `S340`-`S349` lies inside the new C2 block — so **any later adoption of a staged row is renumbered
by document first**, exactly as round 47's S346-S353 → S332-S339 map did. `<AFTER>`: re-check against the L1's landed rows;
if `w1/ExecIdGuard` or the C2 seats force a shift, the old→new map goes here, one line per row, URL unchanged.

### Id guard and quarantine

The dispatch artifacts under `.ufo/waves/round-48/assimilation/` are measured, not typed; re-derived here read-only:
`reg-ids` 276 lines (`S001`-`S339`), `staged-ids` 147 lines (`S203`-`S349`), `collisions` 84 lines (`S203`-`S339`), and the
collision set is exactly the intersection (`python3` set comparison: `equal_to_file=True`). Round 47 reported 70 collisions on
the 262-id registry; the delta is the 14 rows landed since (S326-S339). `<AFTER>`: `w1/ExecIdGuard` re-runs the prompt's
section-10 commands, proves the guard on a scratch registry with an indented `  | S002 |` row (non-empty `collisions`), writes
the quarantine slice from `…/corpus-expansion-1/absent-defect-register.md`, and greps the staged knowledge tree for XKB,
keymap, xkbcommon and terminal-cache themes — its counts and verdict go here, not the dispatch values above.

Quarantine (round-47 slice, inherited): `.ufo/waves/round-47/assimilation/quarantine-slice` is a 13-line file — six
`payload-absent` rows (`S189`, `S195`, `S201`, `S205`, `S224`, `S228`) and seven `no quote was checked` rows (`S199`, `S200`,
`S209`, `S222`, `S223`, `S225`, `S235`). None was appended or hand-checked in round 47 (`corpus/lessons/round-47.md:233-234`),
so all 13 stay quarantined unless this round's slice re-derives one; `<AFTER>`: `w1/ExecIdGuard`'s round-48 slice path, row
count and whether any row left quarantine (with the check that clears it).

### considerthese

`considerthese/2026-10-26.md` is the latest reflection (`ls considerthese/`; no newer file). Proposal 2 was refused in round 47
with its reason (`corpus/lessons/round-47.md:227`), proposal 3 landed as QUALITY 90, so `w1/ScrConsider` drafts exactly one
still-unimplemented proposal as a checkable landing (QUALITY criterion, lesson paragraph or SOURCES row). `<AFTER>`: the
proposal number and its disposition — admitted only beside a check that can fail, or refused with the reason and the flip
condition. `w1/SentPrivacy` measures the privacy classes of this round's own receipts (proposal 1's substance) and its
counts decide whether that proposal is admissible this round.

### The D1 delta line (round-47 contract narrowing, paid forward)

The frozen C1 contract is the docstring of `.ufo/waves/round-47/l1-draft/mado-terminal.py`
(`.ufo/waves/round-47/registration.md:30-31`). Its out-of-contract sentence names `-h/--help`, an empty-string argument, XDG
dirs or HOME containing ':' inside a default, glob characters or a quote, `\u`/`\U` escapes beyond ASCII and locale-sensitive
file names (`:84-87`) — and **not** HOME unset, a FIFO entry or symlink loops. The landed `tools/mado-terminal.py` added all
three to that same sentence after the freeze: "HOME unset, a FIFO named like a desktop file in a later application dir"
(`tools/mado-terminal.py:85-86`, the quote spanning the line break), plus `symlink loops` (`:86`). On these inputs the tool exits 2 where the pin exits 1 (HOME
unset, empty stdout) or blocks (FIFO); the closure recorded the defect at
`corpus/lessons/round-47-verifier-spotcheck.md:126-131`. Round 48 pays it forward instead of re-narrowing: the C1 contract
models HOME unset as the pin does (exit 1, empty stdout), the FIFO and symlink-loop exclusions are registered at this round's
freeze rather than appended to a docstring, and `w1/ExecHomeUnset` (pin-vs-tool sides) and `w1/ScrD1Line` (the one-line-per-item
delta with both locators) are the receipts. `<AFTER>`: the measured pin/tool pairs, and the exact contract sentence the
registration carries.

## Search log

Question: which `kb_rules/kb_model/kb_layout/kb_variant/kb_options` names compile into a keymap on this host (libxkbcommon
1.13.2, xkeyboard-config 2.48), which fail and which are dropped with a warning, and how a failed compile maps onto
Hyprland 0.56.2's `us` fallback — and, separately, which cache invalidation the resolver applies before it trusts
`$XDG_CACHE_HOME/xdg-terminal-exec`?

Where searched: the libxkbcommon tag tree and its docs, the xkeyboard-config tag tree (rules, symbols, the include order),
the host read-only (`xkbcli compile-keymap` with `--layout/--variant/--model/--options/--rules`, never a compositor verb;
`~/.config/hypr/input.conf` as bytes for the host names), the round-47 script pin and its README, and the lane registry
`corpus/SOURCES.md`. `<AFTER>`: `w1/ScoutXkbSpecs` and `w1/ScoutHeld` name the opened candidates and the held overlap.

Identified: `<AFTER>` — candidate sources opened, with the candidate rejects.

Screened: `<AFTER>` — each at its decisive lines.

Included: `<AFTER>` — the admitted rows, one per step the entry states: RMLVO → KcCGST component selection, the include-path
order, unknown-name failures (rules, layout, variant) vs warnings (options, model), multi-layout variant alignment, and the
fallback mapping (cited to S318/S319).

Excluded: `<AFTER>` — decisive line per candidate, in the Gate's Rejected block.

Stop: every compile outcome the entry states has a host receipt and a pinned line; re-open when libxkbcommon or
xkeyboard-config moves past 1.13.2 / 2.48, when the host's `kb_*` names change, or when Hyprland's keymap construction leaves
`efb50993`. For C1: stop when the warm run's stdout+rc is reproduced on the invalidation fixtures; re-open when
`xdg-terminal-exec` leaves 0.14.3 or upstream changes the cache format.

## Mistakes

<AFTER>: `M48-1`..`M48-N`, drafted by `w1/ScrMistakes`, in the round-47 shape — **id** · class · evidence (a path:line, a
command and its output, or a hash) · captured-by (criterion number or `none`) · fix, where a fix counts only once shown able
to fail. At least one mined mistake is mandatory (frontier step §3); if the sweep finds none, the sweep command and its output
are pasted here instead. Each row's class must come from the existing vocabulary (`provider`, `landing`, `vacuous`,
`number-drift`, `reference-drift`, `scope`), and a proposed criterion 96+ must fail on a named input and must not duplicate an
existing criterion (`corpus/QUALITY.md` tops at 95).

Slots the round already knows it must fill (candidates for `ScrMistakes` to confirm or refute — not mistakes until a seat
shows them):

- **M48-1 — D1, post-freeze contract narrowing** (`reference-drift` or `landing`): evidence is the two docstrings above;
  captured-by: none today; fix is the D1 delta line plus the round-48 registration carrying the exclusions.
- **M48-2 — D2, a number in a report without a receipt** (`number-drift`): the round-47 report's `findings=128` at the tip;
  `w1/ExecD2Receipt` runs the gate at three named revisions; the receipt that settles it goes here.
- **M48-3 — D3, an unrouted seat finding** (`landing`): `w2/ExecC1Determinism.md:10` was found in round 47 and not routed;
  this round's fixture schema v2 carries the two-valid-candidates case — `<AFTER>`: the fixture id and the clause that fails
  without it.
- **M48-4 — D4, a locator off by one** (`reference-drift`): the round-47 entry's Limits cite `terminal-route-r17.md:150-151`
  for text at `:149-150`; `w1/ScrErrataD4` drafts the append-only erratum.
- **M48-5 — M47-7/M47-8 recurrence check** (`provider`): the runaway scratch write and the host-cache write were mined in
  round 47; `<AFTER>`: this round's receipts either show the bounds held (no scratch file over the cap, `XDG_CACHE_HOME`
  always redirected) or the recurrence is the mistake.

### Applications of existing criteria

<AFTER>: `M48-n` → criterion number(s) and the sentence saying why the criterion captures it.

### Conflicts recorded for the judge

`<AFTER>`: any pair of w1 seats that measured the same thing with different numbers, quoted verbatim, with the population each
counted. Reported, not silently resolved.

## Round-47 closure items (`corpus/lessons/round-47-verifier-spotcheck.md` section 6)

Each item is non-claim work with its own seat; the L1 may tighten the acceptances.

| item | closure locator | what it is | seat (w1) | planned landing |
|---|---|---|---|---|
| D1 | `round-47-verifier-spotcheck.md:126` | the C1 contract was narrowed after the freeze without re-registration | `ExecHomeUnset`, `ScrD1Line` | appended lesson line (this file, §The D1 delta line) + HOME unset modelled as the pin in the C1 contract |
| D2 | `:132` | the round-47 report's session-material counts have no committed receipt | `ExecD2Receipt` | a receipt naming its revision, or the corrected number |
| D3 | `:136` | readdir-order blind spot not routed (two valid candidates in one dir) | `ExecFixturesV2`, `ExecCounterC1` | fixture-schema-v2 cases with the expected readdir order and a clause that fails on a `sorted()` walk |
| D4 | `:139` | the round-47 entry's Limits locator is off by one | `ScrErrataD4` | append-only erratum line in `xdg-terminal-selection-r47.md` |
| R3 | `:113` (round-46) | `mado-session-material` marker still not installed | `ExecSessionMarker` | tracked gate + marker registry + `SKILL.md` row; shown able to fail both ways |
| R4b | `:116` (round-46) | round-45 entry errata in a form that keeps the frozen round-45 counter's verdict | `ExecErrataR45` | appended errata block; the frozen counter's verdict must not move |
| M47-10 | `corpus/lessons/round-47.md` M47-10 | fixture schema v2: non-regular paths and option-like Exec words (H1/H2) | `ExecFixturesV2`, `ExecOracleV2`, `ExecCounterC1` | schema v2 with `mtime`/`prime`/`after`/`cache`; H1/H2 cases judged by the pin |
| CritC1Explain | `.ufo/waves/round-47/w2/CritC1Explain.md` | `explain`'s `cmd=` was not compared | `ExecCounterC1` | clause x compares `cmd=` against the oracle's print |
| SentC1Sandbox F1-F4 | `.ufo/waves/round-47/w2/SentC1Sandbox.md` | sandbox wording/fail-closed gaps | `ExecCounterC1`, `ExecControlsC1` | F1-F4 fixes, each with the receipt showing the pre-fix state |

What the next closure needs to see (drafted acceptance — command and expected observation; `<AFTER>`: results once the
receipts land):

- **D1.** The C1 docstring models HOME unset with pin exit 1 and empty stdout; the lesson carries one line per post-freeze
  out-of-contract item, each with both locators (frozen `:84-87`, landed `:85-86`). Fails if a new exclusion is added to the
  docstring without a registration entry or a lesson line.
- **D2.** A committed receipt under the seat names its revision and prints the gate's `findings=` value, or the corrected
  number appears in the round-48 report with that receipt. Fails if a number appears with no receipt behind it.
- **D3.** A fixture with two valid entries in one directory, whose expected stdout depends on readdir order, is in
  `c1-r48-fixtures.json` and is scored by the pin; a `sorted()` walk must fail it. Fails if the fixture's expect is
  order-independent.
- **D4.** The r47 entry's diff is append-only (`git diff --numstat <base> <rev> -- corpus/knowledge/xdg-terminal-selection-r47.md`
  deletion column `0`) and the erratum names `terminal-route-r17.md:149-150` with the quote at that line.
- **R3.** Five demonstrations with receipts, as round 47's acceptance stated (gate red count, marked set, planted dump,
  planted dump in a marked file, a real serial in a registered file); the serial value is never printed.
- **R4b.** Each erratum subject re-derived from its pin; the frozen round-45 counter re-run at the tip must keep its verdict
  (this is the constraint that refused the round-47 draft, `w2/ExecErrataR45.md` H1).
- **M47-10 / CritC1Explain / F1-F4.** The counter's own selftest prints the case ids and clause letters; each item names the
  case that fails before the fix and passes after.

## Spot-check (pending non-author)

Not written by this seat: the closure is a non-author integrator's file
(`corpus/lessons/round-48-verifier-spotcheck.md`), and no author may fill it. Shape it must follow, so it can be checked
against this lesson:

1. **Step-1 conformance** — lane HEAD before/after, the report's producer identity, cited-commit existence and ancestry,
   lane pushed and clean, the prompt's contract diff, commits authored by the lane identity; defects listed status-neutral.
2. **Per-claim re-check** — C1: tool present and selftest from committed bytes; live AGREE against the real resolver with a
   redirected cache (cold and primed warm); the counter's before/target receipts re-verified; the H1/H2 and schema-v2 cases.
   C2: entry absent at base and present at tip; the two open-ground sentences (`hyprland-input-devices-r46.md:69`,
   `README.md:112`) answered, not restated; rows `S340`-`<AFTER>` `mined` with the entry as used-by; sampled citations
   re-fetched; the `xkbcli` live receipt's rc/sha256 agreeing with the entry's host sentence.
3. **Per-axis verdicts** — operability, coverage, depth, freshness, calibration, adjacency, each with the basis.
4. **Discernment spot-check** of the five gate decisions above (three admits, two rejects) on outside re-reading, agree or
   disagree, with the reason.
5. **Trend verdicts** — expansion, quality, discernment, each `improved`/`unchanged`/`harmed` with limits named.
6. **Routed defects** — new identity, first locator, and what the next round must fix.

`<AFTER>`: the closure's ruling (attempt 1) and the routed defect list.

## Frontier

The frontier step runs inside the 1-3 claim cap and is not a fourth claim. Its items as they stand:

1. **Registry curation** — rows `S340`-`<AFTER>` added; held rows `S318`/`S319` and the round-46 entry unchanged; the census
   block above is the record. `<AFTER>`: any `status`/`recheck`/`used-by` change logged old→new (expected: none).
2. **Census** — before: 17 `W04` + 1 `W01` + `mado ok`, exit 0; after: `<AFTER>` (must exit 0).
3. **Mined mistake** — `<AFTER>` (see `## Mistakes`; mandatory).
4. **Sourced claim** — C2 rests on rows `S340`-`<AFTER>` opened this round; C1's oracle is the row-47 pin those rows already
   hold, so C1 adds no registry row.
5. **README frontier** — one bullet above the round-47 bullet in `corpus/README.md` `## Frontier` (`:110`), drafted here in the
   section's existing voice and left for the L1 to reconcile with what landed:

> - Round 48 moves two edges onto executed ground. ([XKB keymap compile](knowledge/xkb-keymap-compile-r48.md), rows S340-<AFTER>):
>   which `kb_rules/kb_model/kb_layout/kb_variant/kb_options` names compile through libxkbcommon 1.13.2 and xkeyboard-config
>   2.48, which fail and which are dropped with a warning, and how a failed compile becomes Hyprland's `us` fallback — with a
>   read-only `xkbcli compile-keymap` receipt for this host's names. And the resolver's warm cache: `tools/mado-terminal.py`
>   now predicts `xdg-terminal-exec` 0.14.3's stdout and exit status with an existing `$XDG_CACHE_HOME/xdg-terminal-exec`
>   (hit, out-of-date, invalid, disabled), still starting no process and opening no socket; `explain` names the cache verdict.
>   Still open: whether the cache's `ls -LRl` md5 can be fooled by a same-size, same-minute edit (the counter's fixtures say
>   how far), the launch half of the round-17 `[UNK]`, and the terminal binary's own argument handling.

Provenance, so the L1 can check it before pasting: C1's contract is `.ufo/waves/round-48/claims.md` (cache read at
`xdg-terminal-exec:1179`, trust at `:179-298`, save at `:1455-1458`); C2's ground is
`corpus/knowledge/hyprland-input-devices-r46.md:69` and `corpus/README.md:112`; the host compile facts (rc 0 for `br` +
`compose:caps`, rc 1 for `zz`/`nope` variant, rc 0 + XKB-595 for an unknown option, rc 0 for an unknown model, rc 1 for
`--rules nope`) are the L1's 2026-10-26 observations and must be re-derived by `w1/ExecXkbLive`'s receipt before the bullet
lands. `<AFTER>`: delete any "still open" item this round closes; never widen the bullet to a launch observation (no terminal
was started, by rule).
