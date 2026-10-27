# Round 49 lesson — the keysym tool and the bind key match (2026-10-27, hyaku run 9)

Lane mado-shokunin. Claims (`.ufo/waves/round-49/claims.md`): C1 operability (capability acquisition) —
`tools/mado-keysym.py`, which physical key and which modifiers type a given keysym under a compiled keymap, judged byte-for-byte
against the pinned `xkbcli-how-to-type`; C2 coverage (sourced) — `corpus/knowledge/hyprland-bind-key-match-r49.md`, how
Hyprland 0.56.2 (`efb50993780079460b0cbed1363e2166a2de1d9f`) turns the key field of `bind = MODS, KEY, dispatcher, arg` into
something a key press matches. Round shape: two v1 waves — `w1` build (45 seats, measured from the dispatch's own spec:
`python3 -I -c "import json;print(len(json.load(open('.ufo/waves/round-49/w1-spec.json'))['items']))"` → `45`), then `w2`
falsify against the predicates, counters, fixtures and controls frozen after `w1` returns. Round total TODO-L1
(`w2` seat count and the residual-call count land at the closure). Base `03e4ae76aff7a4be59cb69970dd553baa319695a` (the
round-48 non-author closure commit); the round-49 L1 prep commit `5f37c1b8` sits above it carrying the claims, the w1 spec and
dispatch, `receipts/census-before.txt` and `receipts/operator-state-before.txt`. Axis selection: the published table is tied at
its maximum at the round-48 tip (`.ufo/waves/round-48/receipts/axis-tip-final.txt`: `MADO_AXIS: checked=3 mismatched=0
rev=627914f6…`; navigation 65/65, calibration 86/86, operability 12/12), so no single axis is lowest; C1 is the quality-trend
move and C2 the expansion move (`.ufo/waves/round-49/claims.md`). The same command re-run at the round-49 base is TODO-L1.
Nothing is frozen at the time this skeleton was drafted: the L1 freezes `PRED-C1-r49`/`PRED-C2-r49`, the fixtures and the
complete control set after `w1` returns, and `w2` attacks the frozen instruments. Freeze hash TODO-L1.

**Integration note.** This file is the w1 seat `ScrLesson`'s skeleton: every section the round needs is present with its
shape, and every value still pending is marked `TODO-L1`. The L1 substitutes landed values at integration; where a seat's
draft disagrees with the merged data the merged value wins and the conflict is recorded in
`### Conflicts recorded for the judge`. Counts are written as the command that emits them wherever the number is not yet
measured — round-48 N3 is the standing example: its spot-check template typed a decision count in words while the `## Gate`
block held a different number (measured now: `sed -n '/^## Gate/,/^## Search log/p' corpus/lessons/round-48.md | grep -cE
'^- \*\*(S[0-9]+ admit|REJECT)'` → `15`, of which `12` admit and `3` reject).

## Gate

Candidates considered: two planes, one per claim.

- **C1 (keysym → key and modifiers).** The judge is a binary on this host, not a document:
  `/usr/lib/xkbcommon/xkbcli-how-to-type` (sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`,
  libxkbcommon 1.13.2-1; `xkbcli how-to-type` is the same program through `/usr/bin/xkbcli`), fed a keymap SERIALIZED by
  `/usr/lib/xkbcommon/xkbcli-compile-keymap` (sha256 `43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250`)
  from xkeyboard-config 2.48 RMLVO names. The names ↔ values half of the contract rests on
  `/usr/include/xkbcommon/xkbcommon-keysyms.h` (sha256 `13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3`,
  2659 `#define XKB_KEY_` lines) and on libxkbcommon 1.13.2 `src/keysym.c`'s `xkb_keysym_from_name`/`xkb_keysym_get_name`
  (name choice, deprecated aliases, `U+` names, case folding) — whether the header is sufficient or the tool must embed a
  generated table is one of this round's measured questions (`w1/ExecKeysymNames`, `w1/ScoutHowToType`,
  `w1/RevengerHowToType`). C1's ground at base is that no lane artifact answers the question: the round-48 entry
  `corpus/knowledge/xkb-keymap-compile-r48.md` compiles a keymap and stops, and the bind plane is documentary only
  (`corpus/knowledge/keybind-rule-semantics.md` §2.3). Held ground cited, never re-claimed: rows `S340`-`S351`
  (libxkbcommon 1.13.2 / xkeyboard-config 2.48 compile), `S326`/`S327` (the resolver script), `S318`/`S319` (Hyprland
  config values and `IKeyboard.cpp`). C1's executed evidence is the counter's AGREE run against the pinned judge, not a
  source.
- **C2 (bind key match).** Hyprland at the host's own commit `efb50993780079460b0cbed1363e2166a2de1d9f`
  (`src/managers/KeybindManager.cpp`, `src/config/ConfigManager.cpp` `handleBind`, `src/devices/IKeyboard.cpp` — held as
  `S319`, cited by URL not re-registered), libxkbcommon 1.13.2 `src/keysym.c`, and the Hyprland wiki at a pinned commit
  (Binds / Variables pages). The live half is read-only: `hyprctl version`, `hyprctl binds -j`, `hyprctl getoption
  input:resolve_binds_by_sym -j` (`w1/ExecBindsLive`); the numbers those commands emit (the bind count, the option's int
  value) are quoted from that receipt and never typed here. Ground open at base: `corpus/knowledge/keybind-rule-semantics.md`
  §2.3 states the key forms at `[INF-docs]` level only, and `corpus/knowledge/hyprland-input-devices-r46.md:71` names bind
  resolution as outside its join.

Admitted: rows `S352`-`TODO-L1`, tier `TODO-L1`, status `mined`, opened `2026-10-27`, used-by
`corpus/knowledge/hyprland-bind-key-match-r49.md`, continuing the registry after `S351` (288 rows at base —
`git show 03e4ae76:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,} *\|'` → `288`). The admit-line count is emitted by the
block itself and never typed (round-48 N3):
`sed -n '/^## Gate/,/^## Search log/p' corpus/lessons/round-49.md | grep -cE '^- \*\*S[0-9]+ admit'` = TODO-L1. GATE lines
are emitted by `w1/ScrRows/gate-lines.md` in the round-48 shape — receipt path, sha256, and a ≤25-word quote located by a
computed line number — and pasted here by the L1:

```
- **S<n> admit**, tier <A|B>, <code|own-work>. URL: `<tag-or-commit URL, never a branch>`; opened 2026-10-27; quote `<≤25 words, word-bounded, unique>` (`fetch/<pin name>:<line, computed by grep -n>`). <one sentence: what it teaches for this entry or this tool.>
```

Rows this block must carry, one admit line each (content TODO-L1, the set is the L1's after `w1/ScrRows`; the candidate files
below are the ones the w1 fetch sets actually hold, measured by `ls` in the seat dirs, not a guess): Hyprland
`src/managers/KeybindManager.cpp` (bind dispatch and the `code:`/`mouse:`/`catchall` forms); Hyprland
`src/config/ConfigManager.cpp` (the `handleBind` key-field parse — note the held rows `S303`/`S317` are the **legacy**
`src/config/legacy/ConfigManager.cpp`, a different file, so the census must show no `W04` for the new one); Hyprland
`src/devices/IKeyboard.cpp` is held as `S319` and is **cited, not re-registered**; the Hyprland wiki Binds / Variables pages at
a pinned commit; libxkbcommon `src/keysym.c` (name ↔ value, the perfect-hash and alias behaviour the tool must match);
libxkbcommon `scripts/update-keysyms-derived-headers.py` (how the keysyms header is generated — the question of whether the
host header is sufficient turns on it); libxkbcommon `tools/how-to-type.c` (the exact output columns and masks the tool must
reproduce); libxkbcommon `include/xkbcommon/xkbcommon.h` (the public name/value API); `src/keymap.c` is held as `S351` and is
cited, not re-registered; and one own-work live-receipt row for the read-only `hyprctl` capture (`w1/ExecBindsLive`).

### Rejected after opening

Shape (one short paragraph per refusal, kept even when it loses): `- **REJECT** <url>, opened 2026-10-27. <what it says>. <why
it cannot ground the claim>. Flip: <the condition under which the refusal reverses>.` TODO-L1 for the actual set. Three
rejection classes this round must state explicitly, because they are the round's premise:

- a row on the **host binary** as a separate source from its tag URL would cite the same bytes; the host is a pin
  comparison (`sha256sum` equality, round-47/round-48 precedent), not its own row. Packaged binaries in play this round:
  `xkbcli-how-to-type`, `xkbcli-compile-keymap`, `/usr/bin/xkbcli`, and the header file — each is a digest comparison
  against its tag-side origin (for the keysyms header the origin is the generating script and its inputs, which is one of
  this round's measured questions), never a registry row. holds: TODO-L1 (`w1/CritPremiseC1`, `w1/CritPremiseC2`).
- the **Hyprland wiki** is admissible only at a pinned commit: a page read from a moving default branch cannot be
  digest-pinned. Two `wiki.hypr.land` rows are already held (`S030`, `S045`, both the Window-Rules page), so re-registering
  any held wiki page shows up as a new `W04` in the census. holds: TODO-L1.
- **`IKeyboard.cpp` at `efb50993`** is held as `S319` (round 46, same commit, same bytes): a new row would duplicate a held
  URL with no new scope. C2 cites `S319` instead. Flip: Hyprland leaves `efb50993` or the round needs a line `S319`'s anchor
  does not carry. holds: TODO-L1 (`w1/ConnSiblings`).

No existing row's `status`, `recheck`, or `used-by` changed; all changes here are new rows. The rejected entries stay outside
the registry, with reason and flip above. The entry claims C2 on `S352`-TODO-L1, opened this round.

Quote discipline for this round: each quote is ≤25 words, word-bounded, and unique in its receipt; no landed quote spans or
de-spaces a source line; locators are computed (`grep -n`), never typed. Receipt: `w1/ScrRows/quote-check.txt`
`checked=<n> failed=0` TODO-L1, and the L1's row build.

Held ground, deliberately not re-claimed (named so a later reader sees the overlap is a decision, not an omission):

- **S340-S351** — the round-48 XKB compile block. C2's plane is what the compositor does *with* a compiled keymap; the
  compile itself is not re-argued. A new row on any `xkbcommon-1.13.2` URL those rows already hold (`src/keymap.c`,
  `tools/compile-keymap.c`, `src/xkbcomp/*`) would be a duplicate — the census must show no new `W04`.
- **S318/S319** — Hyprland `src/config/values/ConfigValues.cpp` and `src/devices/IKeyboard.cpp` (round 46, held). The
  keymap construction and the `us` fallback are cited, never re-claimed; C2's clause asserting these rows and the round-46
  entry are byte-equal to base is TODO-L1.
- **`corpus/knowledge/xkb-keymap-compile-r48.md`** — the compile half. Append-only rule (`CORPUS.md` rule 2): the round-49
  entry is a new file, and any correction to the round-48 entry is an appended erratum, never a rewrite.
- **`corpus/knowledge/keybind-rule-semantics.md` §2.3** — the key forms at `[INF-docs]` level; C2 upgrades the level for the
  key field and states which part it still leaves open (TODO-L1: `catchall`, `code:`, `mouse:`, `switch:` coverage).

### Census before → after

Before (`.ufo/waves/round-49/receipts/census-before.txt`, base `03e4ae76`, exit 0) — 17 `W04` lines and 1 `W01` line:

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

After (`.ufo/waves/round-49/receipts/census-after.txt`, exit 0, captured at the integrated data state) — TODO-L1: the same 17
`W04` + 1 `W01` + `mado ok` if no new row repeats a held URL, and one new `W04` line per repetition otherwise. Both ends:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.

### Registry changes

| surface | old (base `03e4ae76`) | new |
|---|---|---|
| `corpus/SOURCES.md` | `288` rows, top `S351` (`git show 03e4ae76:corpus/SOURCES.md \| grep -cE '^\| *S[0-9]{3,} *\|'`) | TODO-L1 rows, top TODO-L1; rows `S352`-TODO-L1 appended after the last `S` row, 11 cells each, `mined`, opened `2026-10-27`, used-by `corpus/knowledge/hyprland-bind-key-match-r49.md` |
| `corpus/knowledge/` | `65` files (`git ls-tree --name-only 03e4ae76 corpus/knowledge/ \| wc -l`) | `66` (`hyprland-bind-key-match-r49.md`) |
| `corpus/README.md` | `13` `- Round <n> moves` Frontier bullets | `14` (one three-cell-separated bullet naming the bind key match and rows `S352`-TODO-L1), plus the index row |
| `corpus/lessons/` | `72` files (`git ls-tree --name-only 03e4ae76 corpus/lessons/ \| wc -l`) | `73` (this lesson) |
| `tools/` | `15` files (`git ls-tree --name-only 03e4ae76 tools/ \| wc -l`), `mado-terminal.py` the newest | `16` — C1 adds `mado-keysym.py` |
| `quality/` | `99` numbered criteria in `corpus/QUALITY.md` (`git show 03e4ae76:corpus/QUALITY.md \| grep -cE '^[0-9]+\. '`) | TODO-L1 criteria if the round mines a new mistake class; `counters/c1-r49-keysym.py`, `c2-r49-bind-entry.py`, the C1 fixtures and the controls land at the freeze |
| held rows `S318`/`S319`, `corpus/knowledge/xkb-keymap-compile-r48.md`, `corpus/knowledge/hyprland-input-devices-r46.md` | as at base | byte-identical (C2 clause; command in the acceptance table) |

### Renumber map

Measured at base, not typed: registry top is `S351` (288 ids —
`git show 03e4ae76:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,} *\|'`), and the staged band is `S203`-`S349` (147 ids, from
the most recent slice, `.ufo/waves/round-48/assimilation/staged-ids`; the tree holds 19 `staged-ids` paths —
`find .ufo -name staged-ids | wc -l` — of which the round-47 and round-48 slices are both 147 lines). A set intersection of
the registry ids against that band, run 2026-10-27, gives 94 ids (`S203`-`S349`); round 48 reported 84 on a 276-id registry,
and the delta is the ten rows `S340`-`S349` landed since. Round-49's own guard artifacts are TODO-L1 (`w1-spec.json` carries
no `ExecIdGuard` seat this round — round 48 had one; whoever runs the guard writes `reg-ids`, `staged-ids`, `collisions`
under `.ufo/waves/round-49/assimilation/`). Because the C2 block opens at `S352`, above
the band's upper end `S349`, **no row added this round can collide with a staged id**; the 94 collisions are pre-existing ids
and stay untouched. Any later adoption of a staged row is renumbered by document first, exactly as round 47's S346-S353 →
S332-S339 map did. Re-checked against the landed rows at integration: TODO-L1 (if any staged row was adopted, name which and
where it moved).

### Id guard and quarantine

The dispatch artifacts under `.ufo/waves/round-49/assimilation/` are empty at the time this skeleton was drafted (measured:
`find .ufo/waves/round-49/assimilation -type f | wc -l` → `0`), so the round-49 numbers are TODO-L1: `reg-ids` TODO-L1 lines,
`staged-ids` TODO-L1 lines, `collisions` TODO-L1 lines, and the collision set must equal the set intersection exactly
(`equal_to_file=` TODO-L1). The guard run — round 48's `w1/ExecIdGuard` is the precedent; this round's spec names no
`ExecIdGuard` seat, so the L1 assigns it — runs the section-10 block verbatim, proves the guard on a scratch registry whose
indented `  | S002 |` row produces a non-empty `collisions`, and sweeps the staged knowledge tree for
`keysym|keybind|bind|xkbcommon` to show no staged entry touches this round's plane (TODO-L1).

Quarantine (round-47 slice, inherited unchanged; `.ufo/waves/round-48/assimilation/quarantine-slice`, 13 lines): six
`payload-absent` rows (`S189`, `S195`, `S201`, `S205`, `S224`, `S228`) and seven `no quote was checked` rows (`S199`, `S200`,
`S209`, `S222`, `S223`, `S225`, `S235`). No row left quarantine in rounds 47 or 48; TODO-L1 for this round — if no staged
entry is adopted, no row is hand-checked either.

### considerthese

Latest reflection: `considerthese/2026-10-26.md` (measured `ls considerthese/ | tail -1`; no `2026-10-27` file exists yet —
TODO-L1 if one lands). Round 48 landed its proposal 6 (lead with round-level outcomes) as QUALITY 99; proposals 1-5 stand as
recorded there. This round drafts exactly one still-unimplemented proposal as a checkable landing (QUALITY criterion, lesson
paragraph or SOURCES row) — TODO-L1, with the seat named: `w1-spec.json` carries no `ScrConsider` seat this round, so the
drafting seat is the L1's assignment among `ScrQuality`/`ScrCorrections`. Do not re-mine proposal 1's substance as a proposal:
its measurement is M48-8's instrument widening, which is routed below.

### The contract delta line (round-48 D1 paid forward)

Round 48 paid the D1 debt by modelling the pin instead of narrowing the contract; round 49's freeze is stricter, because the
C1 contract exists only as this round's docstring + `registration.md`. The rule this section records: the freeze names the
complete out-of-contract list, the landed tool's docstring quotes that same list, and any item added to the docstring after
the freeze gets one line here with **both** locators (frozen paragraph, landed line) and the input pair that separates them.
Measured pairs TODO-L1 (`w1/ScrCorrections`, `w1/CritPremiseC1`): Compose sequences and the character/code-point
interpretation are out of contract by declaration (the tool refuses without `--disable-compose --keysym`, exit 2), and a raw
XKB source with `include` statements is out of contract (the keymap must be `xkbcli compile-keymap` output) — both must be
*tested* as refusals by the counter, not merely written down.

### Applications of existing criteria

TODO-L1: one line per mistake of this round mapped to an existing QUALITY criterion (`M49-n → **<k>** (applied|new)`), plus
the round-48 routed criteria named as applied here — 10/counts, 52/routing, 92/produced-vs-committed, 94/carried numbers,
96/contract delta, 97/locators, 98/scratch cap, 99/outcome-first.

### Conflicts recorded for the judge

TODO-L1. The round-48 lesson's form stands: each conflict names both seats, what they measured, and the L1's ruling or the
alternative reading it kept. Candidate collision this round already visible in the dispatch (name it if it materialises):
several seats read the same libxkbcommon pin set (`ExecKeysymNames`, `ExecKeymapParse`, `ExecXkbSrc`, `ExecOracle`,
`RevengerHowToType`) — a duplicate *row* proposal from two seats is a `ConnClaims` conflict, not two rows.

## Search log

Question: how does Hyprland 0.56.2 turn the key field of a `bind` line into something a key press matches — name to keysym,
which keysym of the pressed key is compared under which layout and `input:resolve_binds_by_sym`, how the modifier mask is
compared, and how `code:`/`mouse:`/`switch:`/`catchall` differ — and, separately, which keycode, level and modifier mask type
a given keysym under a compiled keymap?

Where searched: the Hyprland sources at the host's commit `efb50993` (`src/managers/KeybindManager.cpp`,
`src/config/ConfigManager.cpp`, `src/devices/IKeyboard.cpp` held as `S319`), libxkbcommon 1.13.2
(`src/keysym.c`, `tools/how-to-type.c`, `src/keymap.c`, `include/xkbcommon/xkbcommon.h`), the host's keysym header
`/usr/include/xkbcommon/xkbcommon-keysyms.h`, the Hyprland wiki at a pinned commit, the host read-only (`xkbcli compile-keymap`,
`xkbcli how-to-type`, `hyprctl binds -j`, `hyprctl getoption input:resolve_binds_by_sym -j`, `hyprctl version`), and the lane
registry `corpus/SOURCES.md`. Opened candidates this round (measured, not typed): TODO-L1, from the fetch sets under
`.ufo/waves/round-49/w1/ExecHyprSrc/fetch/`, `ExecXkbSrc/`, `ExecKeysymNames/`, `ExecKeymapParse/`.

Identified: TODO-L1 candidate sources opened — TODO-L1 admitted as `S352`-TODO-L1, TODO-L1 rejected (plus the held-duplicate
refusal of `IKeyboard.cpp`).

Screened: TODO-L1 — each admitted pin at the ranges its row cites, with the `grep -n` line for its quote.

Included: TODO-L1 — one clause per admitted row, in the order the entry uses them.

Excluded: TODO-L1 — the rejections with reasons and flip conditions (Gate's Rejected block).

Stop: every outcome the entry and the tool state has a pinned line and, where it is a host behaviour, a live receipt. Re-open
when Hyprland leaves `efb50993`, when libxkbcommon leaves 1.13.2 or xkeyboard-config leaves 2.48, when the host's `kb_*` names
change, or when `xkbcli how-to-type` changes its output format. For C1: stop when the counter's AGREE run covers every fixture
and nonce pair; re-open when `how-to-type.c`'s printed columns change.

## Mistakes

One line per finding, in the round-48 form — `**M49-<n>** · class \`<class>\` · evidence: <receipt or command and its output>
· captured-by: <criterion number, or none (criterion now covers it)> · fix: <what landed>`. The L1 numbers these; a w1 seat
drafts a line only for its own seat's defect and defers the number (round-48's `ExecHomeUnset`/`ScrD1Line` M47-12 collision).
Class vocabulary in use: `contract-narrowing`, `unreceipted-number`, `routing`, `locator`, `provider`, `vacuous`,
`flaky-instrument`, `instrument-blind-spot`, `freeze-before-controls`, `host-write`. Findings TODO-L1, with the classes this
round is already exposed to named so a seat can claim them:

- **`contract-narrowing`** — the C1 docstring against the frozen out-of-contract list (§The contract delta line). Round-48
  M48-1's instrument is QUALITY 96; it must read `added=0 removed=0 verdict=OK` on this round's pair.
- **`host-write`** — any seat run that writes outside its scratch/bwrap (M48-10 below). Evidence required: the
  before/after digest pair of operator-owned state.
- **`unreceipted-number`** — any number in this lesson or the round report that no committed receipt emits (M48-11), including
  the bind count and the axis line.
- **`provider`** — the scratch bound and the clone recipe (M48-13 below); the bound is executed, not prose.
- **`flaky-instrument`** — a frozen counter read once and reported as a verdict (M48-12): every run of a frozen counter is
  committed, and a `readonly` trip is read, not averaged.

Template for each line (fill, do not restyle):

```
**M49-<n>** · class `<class>` · evidence: <path:line or command and its output, with the revision named> · captured-by:
<criterion <k>, or none (criterion <k> now covers it)> · fix: <what landed, with the receipt that shows it>.
```

### w2 routing (criterion 52 applied to every w2 seat)

TODO-L1: every w2 seat with its disposition — `fixed` (repaired before the data commit), `residual` (declared in
`registration.md` or the counter docstring), `routed` (round 50, with this lesson as the age anchor), `held` (attacked and
stood). Table shape: `| seat | finding | disposition |`, seat reports under `.ufo/waves/round-49/w2/<Seat>.md`.

## Round-48 closure items (routed; `corpus/lessons/round-48-verifier-spotcheck.md` §6)

Each item is non-claim work with its own receipt; the L1 may tighten the acceptances. Locators are section-6 item numbers as
the spot-check writes them.

| item | closure locator | what it is | seat (w1) | planned landing / acceptance |
|---|---|---|---|---|
| N1 | §6 item 1 | the round-48 report's "52 untracked `*.synthetic` files" does not reproduce; the count is 47 | `ScrCorrections`, `CritRoutedItems` | the lesson and report state the count with its command: `git status --porcelain -uall \| grep -c 'synthetic'` → `47` at the round-49 base, all `*.synthetic`, 45 under `.ufo/waves/round-45/` and 2 under `.ufo/waves/round-46/` (measured 2026-10-27). Fails if a count appears without the command. |
| N2 | §6 item 2 | the round-48 `host_cache_untouched_sha256` digest is the w2 mutant's 7 bytes: the field name reads as clean | `SentHost`, `ExecMutantSandbox` | a lesson line naming what that digest is, plus this round's operator-owned before/after digest pair — before at `.ufo/waves/round-49/receipts/operator-state-before.txt` (committed at `5f37c1b8`: `~/.cache/xdg-terminal-exec` sha256 `ddd94f6b…`, 190 B, `~/.config/hypr/{input.conf,bindings.conf,hyprland.conf}` digests, `~/.local/bin` 106 entries), after at `receipts/operator-state-after.txt` TODO-L1. Fails if a digest is labelled "untouched" without a before/after pair. |
| N3 | §6 item 3 | `corpus/lessons/round-48.md:425` types the Gate's decision count in words, and the typed number does not match the block (pipeline on that file: `15` total, `12` admits, `3` rejects) | `ScrLesson` (this file), `ScrQuality` | the `## Spot-check` shape below carries **no typed count**: it names the `sed`/`grep` pipeline that computes the admit, reject and total counts from the Gate block. Round-48 is frozen: the correction is a note here, not an edit there. Fails if any line in this lesson types a gate-decision number. |
| N4 | §6 item 4 | the text matrix shows 96 of 98 variants (`a-entry-at-base`, `a-rev-base-direct` only in `summary.json`) | `ExecN4Matrix` | a text receipt with every variant row — `variants=` and `rows=` equal TODO-L1. Fails if the emitted rows are fewer than the summary's. |
| N5 | §6 item 5 | GitLab `-/raw/` returns an anti-bot HTML page; the files API serves the pinned bytes | `RevR48`, `ScoutHeld` | an append-only note (README or lesson) naming the API form `/api/v4/projects/<id>/repository/files/<path>/raw?ref=<tag>` for freshness re-fetch; no row edit. Fails if a re-fetch uses `-/raw/` and calls the HTML page a mismatch. |
| M48-8 | §6 item 6 | the session-material gate is red at the round-48 tip (the closure's `findings=159`) and blind to 16 of 19 synthetic `/home/<user>` shapes, scanning `.ufo/` only | `ExecSessionTriage`, `ExecSessionShapes`, `SentPrivacy` | three measurements this round: the gate's count at the round-49 base, the shape classes it misses with the synthetic inputs that show it (each planted in scratch, never home), and a scope statement for paths outside `.ufo/`. Fails if a synthetic shape is claimed covered without a run showing it. |
| M48-10 | §6 item 6 | a round-48 w2 mutant wrote the operator's real `~/.cache/xdg-terminal-exec`; the "L0 question filed" claim was false | `ExecMutantSandbox`, `SentHost` | mutants run with `HOME`/`XDG_CACHE_HOME`/`XDG_CONFIG_HOME`/`XDG_DATA_HOME`/`XDG_STATE_HOME` under scratch and inside bwrap with the real home unbound; a mutant that writes targets a sandbox path; the operator-state before/after pair (N2) is the detector. Fails if any mutant run is unsandboxed. |
| M48-13 | §6 item 6 | `ulimit -f 2048` (1 MiB) broke `git clone --shared` checkouts, so the clause-r mutant attack and the gate both-ways demonstration never ran | `ExecCloneRecipe` | the seat clone recipe under the wave's cap (`ulimit -f 65536` = 64 MiB, as the round-49 dispatch carries) with the measured largest file; the two owed demonstrations run: the clause-r mutant attack on the frozen C1 counter, and the session-material gate failing both ways. Fails if the recipe is asserted without a completed checkout. |
| SentScratch F1-F7 | `.ufo/waves/round-48/w2/SentScratch.md` | counters accept a `/tmp` work dir (`c2` replay any `TMPDIR`; `c1 --work` admits `/tmp`) | `ExecCounterC1`, `ExecCounterC2`, `ExecControlsC1`, `ExecControlsC2` | the frozen counters refuse a work dir under `/tmp` (exit 2 with a named message) and honour `TMPDIR`/`--work`; both refusals shown by a control that would otherwise pass. Fails if a counter runs with `/tmp` as its work dir and scores. |
| registration-v2 residuals | `.ufo/waves/round-48/registration-v2.md:103-110` | receipt generator path; the uncited meson pin | `RevRegResiduals` | each residual either cited in the round-49 registration or closed with a receipt. Fails if the round-49 registration repeats an uncited pin. |
| 47 sidecars | §6 (the untracked set) | 47 `*.synthetic` sidecars under `.ufo/waves/round-45/w1/RevengerOmarchy/` and `.ufo/waves/round-46/w1/`, written by round-48 w1 `ExecSessionMarker` outside its seat dir; digests at `.ufo/waves/round-48/w1/ExecSessionMarker/SHA256SUMS` | `CritSidecars` | the L1 decides commit vs remove; the seat verifies each sidecar against its digest, lists any not covered by the digest file, and states the disposition. Fails if a sidecar is committed with no digest row. |

What the next closure needs to see (drafted acceptance — command and expected observation):

- **N1.** The round-49 report and lesson print the sidecar count beside its command; the two lines agree.
- **N2.** `receipts/operator-state-before.txt` and `receipts/operator-state-after.txt` are both committed, name the same five
  paths, and the after file states which digests moved and why (a resolver run is the only legitimate mover).
- **N3.** No line of this lesson types a gate-decision count (the two mentions of round-48's stale wording are references to
  the defect, not counts of this Gate), and the Spot-check line names the
  computing pipeline; run that pipeline on `corpus/lessons/round-48.md` as the control → `T=15`, `A=12`, `R=3`, which is the
  number the N3 correction states.
- **N4.** The matrix receipt's `rows=` equals its `variants=`.
- **M48-13.** The clone receipt shows `git -C "$D" rev-parse --show-toplevel` equal to `$D` after a checkout under the cap,
  plus the largest file the seat produced.

## Spot-check (pending non-author)

Not written by this seat: the closure is a non-author integrator's file (`corpus/lessons/round-49-verifier-spotcheck.md`), and
no author may fill it. Shape it must follow, so it can be checked against this lesson:

1. **Step-1 conformance** — lane HEAD before/after, the report's producer identity, cited-commit existence and ancestry, lane
   pushed and clean, the prompt's contract diff, commits authored by the lane identity; defects listed status-neutral.
2. **Per-claim re-check** — C1: `tools/mado-keysym.py` present at the tip and its selftest from committed bytes; AGREE against
   `/usr/lib/xkbcommon/xkbcli-how-to-type` (pin sha256 `f6c0b122…`) on fixed fixtures whose keymaps are compiled at count time
   with the pinned `xkbcli-compile-keymap` in `env -i` (`PATH=/usr/bin`, `HOME`/`XDG_CONFIG_HOME` in scratch), and on nonce
   `(RMLVO, keysym)` pairs; the tool run in a bwrap sandbox that sees only the keymap file; the refusal paths (no
   `--disable-compose` or no `--keysym` → exit 2, named message); the read-only guarantee observed (no child process, no
   socket, no write). C2: entry absent at base (`03e4ae76`) and present at tip; the two open-ground sentences
   (`keybind-rule-semantics.md` §2.3, `hyprland-input-devices-r46.md:71`) answered, not restated; rows `S352`-TODO-L1 `mined`
   with the entry as used-by; sampled citations re-fetched byte-equal; the live receipt's `hyprctl` rc and shape agreeing with
   the entry's host sentence (device names never printed).
3. **Per-axis verdicts** — operability, coverage, depth, freshness, calibration, adjacency, each with the basis.
4. **Discernment spot-check** of the `## Gate` decisions — the counts are **computed from the Gate block, never typed**
   (round-48 N3: its template typed a decision count in words and the typed number did not match its block):
   `T=$(sed -n '/^## Gate/,/^## Search log/p' corpus/lessons/round-49.md | grep -cE '^- \*\*(S[0-9]+ admit|REJECT)')`,
   `A=$(sed -n '/^## Gate/,/^## Search log/p' corpus/lessons/round-49.md | grep -cE '^- \*\*S[0-9]+ admit')`,
   `R=$(sed -n '/^## Gate/,/^## Search log/p' corpus/lessons/round-49.md | grep -cE '^- \*\*REJECT')`, with the invariant
   `T = A + R`. Control for the pipeline: run the same three commands on `corpus/lessons/round-48.md` → `T=15`, `A=12`, `R=3`
   (measured 2026-10-27), the numbers the N3 correction states. The closure re-opens `max(min(T, 6), 3)` of the decisions and
   at least one reject whenever `R > 0`, and prints `T`, `A`, `R` and the ids it re-opened. A line that states a decision
   count without that pipeline is the N3 defect again.
5. **Trend verdicts** — expansion, quality, discernment, each `improved`/`unchanged`/`harmed` with limits named.
6. **Routed defects** — new identity, first locator, and what the next round must fix (this round's items are the §Round-48
   closure table plus anything `w2` routes).

## Frontier

The frontier step runs inside the 1-3 claim cap and is not a fourth claim. Its items as they stand:

1. **Registry curation** — rows `S352`-TODO-L1 added; held rows `S318`/`S319` and the round-46/round-48 entries unchanged; the
   census block above is the record. No `status`/`recheck`/`used-by` cell on an existing row changed (verify: the rows.md
   append is insert-only after `| S351 |`, `git diff corpus/SOURCES.md` shows only `+` lines).
2. **Census** — before: 17 `W04` + 1 `W01` + `mado ok`, exit 0 (`.ufo/waves/round-49/receipts/census-before.txt`); after:
   TODO-L1 with the same command.
3. **Mined mistake** — `M49-1`..TODO-L1 above.
4. **Sourced claim** — C2 rests on rows `S352`-TODO-L1 opened this round; C1's oracle is a host binary plus its tag source,
   so C1 adds rows only for the libxkbcommon name/output behaviour it must reproduce (TODO-L1: how many).
5. **README frontier** — the landed bullet names the bind key match (rows `S352`-TODO-L1) and, in the same bullet, what the
   keysym tool now answers and what it refuses (Compose sequences, character/code-point interpretation, raw XKB sources with
   includes), with what stays open: TODO-L1 (the compositor's own keysym pick under a non-`us` layout at runtime, any
   `hyprctl` observation that needs a key press, and the `catchall`/`switch:` forms if the entry cannot ground them).

Provenance: C1's contract is `.ufo/waves/round-49/claims.md` and, after the freeze, `registration.md`; C2's ground at base is
`corpus/knowledge/keybind-rule-semantics.md` §2.3 and `corpus/knowledge/hyprland-input-devices-r46.md:71`; the pins are the
byte digests under `.ufo/waves/round-49/fetch/` (L1-owned, TODO-L1 count); the live facts (bind count, `input:resolve_binds_by_sym`
value, `hyprctl version` line) are read-only captures in `w1/ExecBindsLive`'s receipt and are quoted from it, never typed here.
