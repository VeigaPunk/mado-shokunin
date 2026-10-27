# Round 48 lesson — the XKB compile and the resolver cache (2026-10-26, hyaku run 9)

Lane mado-shokunin. Claims (`.ufo/waves/round-48/claims.md`): C1 operability (capability acquisition) - the warm-cache
path of `tools/mado-terminal.py`; C2 coverage (sourced) - `corpus/knowledge/xkb-keymap-compile-r48.md`. Registration v1
(`registration.md`, freeze `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`, `PRED-C1-r48`/`PRED-C2-r48`) was attacked by the
w2 falsify wave (48 seats) before any data; w2 broke both v1 counters' own control rules and contract text (a cache
write and a fork met C1; a mode-755 pin and a 600-character quote met C2), so the L1 re-registered before data as v2
(`registration-v2.md`, `PRED-C1-r48-v2`/`PRED-C2-r48-v2`, 228 warm fixtures, write/fork tripwire, symlinks; pin mode and
quote length), re-ran the complete control set against v2 and then landed the data. Base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585` (the round-47 non-author closure commit). Round shape: two v1 waves - `w1`
build (41 seats), `w2` falsify (48 seats), and in attempt 4 one residual attack call `a4r1` (8 seats) against the
committed data; round total 97.

**Integration note.** The skeleton was drafted by w1 seat `ScrLesson`; attempt 2 substituted the landed values; attempt
3 folded in the w2 findings and the v2 re-registration. Attempt 3's L1 died in the orchestrator session exit
(2026-10-26 23:57:36 -03); the orchestrator committed its uncommitted outputs as salvage `cf3deeec` (rows S340-S351,
the extended `tools/mado-terminal.py`, SKILL/QUALITY/README/errata, receipts). Attempt 4 re-verified that salvage before
building on it: the frozen counters and fixtures are byte-equal to the v2 freeze `02165600` (`git diff --stat 02165600
cf3deeec -- quality/counters` empty; sha256 `5bb9aead…`, `3ab1f5d0…`, `bb0f0605…` as registered), the landed tool is the
bytes the v2 control set scored (`143820476403…`, `receipts/v2/ctl/FINAL.txt:1`), and a scratch mirror of the
salvage plus the then-untracked entry scores both predicates, v1 and v2, `TARGET_MET` (`receipts/a4/pre-*.txt`).
Where a seat's draft disagreed with the merged data the merged value wins and the conflict is recorded in
`## Conflicts recorded for the judge`.

## Gate

Candidates considered: two planes, one per claim.

- **C1 (cache edge).** The resolver's cache path, against the script already pinned in round 47 —
  `https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec` (pin
  `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256 `89f2be9a…27ac`, byte-equal to `/usr/bin/xdg-terminal-exec`), read
  cache first at `:1179`, `read_cache` at `:217-298`, `gen_hash` at `:179-215`, the background save at `:1455-1458`; the
  README's cache sentence (row S327). No new C1 rows are expected: the source of truth is the row-47 pin, re-read this
  round; `w1/ScoutHeld` names the twelve held rows/notes (H-a..H-l: r47 entry :43/:70/:76/:83, terminal-route-r17.md
  :51-53/:123-127, the r47 tool docstring :82-85, the c1-r47 counter docstring and the r47 RevengerCache receipt) as
  held; `w1/RevengerCache` records the upstream-accepted gaps (unrelated churn invalidating, a `/disable_cache` line
  ignored while a valid cache exists, list-less default changes) and the unexamined metadata blind spots
  (same-size same-minute edits, day-resolution mtimes, PATH identity, entry conditions never re-checked). C1's executed evidence is the counter's primed warm run, not a source.
- **C2 (XKB compile).** libxkbcommon 1.13.2 tag sources and docs (`doc/rules-format.md`, `doc/user-configuration.md`, the
  compiler's include handling), xkeyboard-config 2.48 at the tag (rules/evdev, the symbols files the host's names take), and
  the host-read `xkbcli compile-keymap` receipt (`/usr/bin/xkbcli`, `/usr/lib/xkbcommon/xkbcli-compile-keymap`).
  `w1/ScoutXkbSpecs` opened the libxkbcommon 1.13.2 tag tree (context.c, context-priv.c, xkbcomp.c, rules.c,
  include.c, messages-codes.h, meson_options.txt, tools/compile-keymap.c) and the xkeyboard-config 2.48 tag
  (rules/rules.in, rules/meson.build, symbols/br, the installed generated rules/evdev); `w1/ScrRows` drafted the rows
  and gate lines the L1 merged into rows S340-S350 (`l1-draft/rows-c2.md`, `l1-draft/gate-rows.md`). C2's ground at base is open in two places:
  `corpus/knowledge/hyprland-input-devices-r46.md:69` ("The XKB compile itself is not reproduced") and `corpus/README.md:112`
  ("the XKB compile itself").

Admitted: rows `S340`-`S351` (S351 added by the L1 in attempt 3 after w2 `CritDataCompleteness` C2-A), tier `A`, status `mined`, opened `2026-10-26`, used-by
`corpus/knowledge/xkb-keymap-compile-r48.md`, continuing the registry after `S339` (276 rows at base). GATE lines are emitted
by `w1/ScrRows/gate-lines.md` in the round-47 shape — receipt path, sha256, and a ≤25-word quote located by a computed line
number — and pasted here by the L1:

```
- **S340 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/rules.c`; opened 2026-10-26; quote `No index provided: match only if single layout` (`fetch/xkbcommon-rules.c:1259`). The rules matcher explains when layout/variant expansion consumes a name and why an unknown layout reaches a missing symbols-file failure rather than the ignored-name path.
- **S341 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/xkbcomp.c`; opened 2026-10-26; quote `ok = xkb_components_from_rules_names(keymap->ctx, rmlvo, &kccgst,` (`fetch/xkbcommon-xkbcomp.c:157`). This names the RMLVO-to-component resolve stage whose failure yields no keymap.
- **S342 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/xkbcomp/include.c`; opened 2026-10-26; quote `Couldn't find file "%s/%.*s" in include paths` (`fetch/xkbcommon-include.c:355`). The pin gives the failure line and the ordered include search that the live receipt probes.
- **S343 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/context.c`; opened 2026-10-26; quote `ctx->log_level = XKB_LOG_LEVEL_ERROR;` (`fetch/xkbcommon-context.c:503`). The context implementation grounds default log level and default include path order.
- **S344 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/context-priv.c`; opened 2026-10-26; quote `Options can be empty, so respect that if passed in.` (`fetch/xkbcommon-context-priv.c:218`). This distinguishes an empty options string from NULL and grounds the name defaults/environment route.
- **S345 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/meson_options.txt`; opened 2026-10-26; quote `value: 'us',` (`fetch/xkbcommon-meson_options.txt:46`). The build option pins the compiled-in default layout used when names are absent.
- **S346 admit**, tier A, code. URL: `https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/rules/rules.in`; opened 2026-10-26; quote `pc+%l%(v)` (`fetch/xkeyboard-config-rules-rules.in:243`). The tag's template plus `rules/meson.build:18-39` is the generator input for the host's `rules/evdev`, copied and hashed as `fetch/xkeyboard-config-rules-evdev` from package xkeyboard-config 2.48-1; this row ties the released mapping to the reproducible source/build recipe.
- **S347 admit**, tier A, code. URL: `https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/symbols/br`; opened 2026-10-26; quote `xkb_symbols "nodeadkeys" {` (`fetch/xkeyboard-config-symbols-br:47`). The tag's `symbols/br`, byte-equal to the host file, holds the eleven maps a `br` variant must name; the w1 seat's admit line (`w1/ScrRows/gate-lines.md`) was lost in the L1 renumber and restored here (w2 `ConnSourceLinks` 1).
- **S348 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/tools/compile-keymap.c`; opened 2026-10-26; quote `ctx_flags |= XKB_CONTEXT_NO_ENVIRONMENT_NAMES;` (`fetch/xkbcommon-tools-compile-keymap.c:587`). This grounds why bare xkbcli does not read XKB_DEFAULT_* unless its explicit environment-names option is used.
- **S349 admit**, tier A, code. URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/messages-codes.h`; opened 2026-10-26; quote `XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,` (`fetch/xkbcommon-messages-codes.h:150`). It anchors the XKB-595 identifier cited for a dropped option.
- **S351 admit**, tier A, code (attempt 3, before data). URL: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keymap.c`; opened 2026-10-26; quote `if (!ops->keymap_new_from_names(keymap, &rmlvo)) {` (`fetch/xkbcommon-keymap.c:173`). The public `xkb_keymap_new_from_names` (`:183-189`) wraps `xkb_keymap_new_from_names2`, which returns NULL at `:173-176` - the compositor-visible NULL step 8 states, which the v1 entry inferred from internal helpers that return false (w2 `CritDataCompleteness` C2-A).
- **S350 admit**, tier A, own-work. Source opened this round: the L1-generated read-only receipt `.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt`; access date 2026-10-26; quote `rc=0` (`receipt:57`, positive `--layout br --options compose:caps` compile). It is the host-specific execution result, with keymap digest in the same case; it is not an upstream source.
```

### Rejected after opening

- **REJECT** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.cpp`, opened 2026-10-26. The compositor's keymap construction and its `us` reset are already held as S319 (round 46, same commit, same bytes); a new row would duplicate a held URL with no new scope. Flip: Hyprland leaves `efb50993` or the round needs a line S319's anchor does not carry. (w1 `ScrRows` third reject, restored per w2 `ConnSourceLinks` 1.)
- **REJECT** `https://wiki.archlinux.org/title/Xorg/Keyboard_configuration`, opened 2026-10-26. The English page restates broad XKB setup, but the scoped claim is the behavior of this host's libxkbcommon 1.13.2/xkeyboard-config 2.48 combination; the direct tagged implementation, installed generated ruleset and read-only host receipt are more authoritative and version-bound. Flip: the page supplies a version-pinned behavior or implementation detail not present in those primary bytes.
- **REJECT** `https://xkbcommon.org/doc/current/index.html`, opened 2026-10-26. The current documentation index is not version-pinned and does not itself state the RMLVO/include/error behavior this entry claims; the 1.13.2 source pins already provide the primary evidence. Flip: a pinned 1.13.2 documentation page provides a distinct behavior that the source pins and host receipt do not.

No existing row's `status`, `recheck`, or `used-by` changed; all changes here are new rows. The rejected entries stay outside the registry, with reason and flip above. The entry claims C2 on S340-S351, opened this round.

Quote discipline for this round: each quote is ≤25 words, word-bounded, and unique in its receipt; no landed quote spans or de-spaces a
source line (`l1-draft/gate-rows.md` locators, one line per row; `w1/ScrRows/quote-check.txt` `checked=8 failed=0`
and the L1's row build at `make-rows.py`).

Held ground, deliberately not re-claimed (named so a later reader sees the overlap is a decision, not an omission):

- **S326/S327** — the resolver script and README (round 47, `mined`). C1 extends the tool against the already-pinned script;
  a new row on the same tag URL would be a duplicate with no new scope (the census adds no W04 for the cache: the round-48 rows carry xkbcommon/xkeyboard-config URLs and one own-work
  receipt, none repeating a held URL — W04 count unchanged, 17 → 17).
- **S318/S319** — Hyprland `src/config/values/ConfigValues.cpp` and `src/devices/IKeyboard.cpp` (round 46, held). The
  `us` fallback after a failed compile is cited, never re-claimed (`claims.md`: "cite, never re-claim"); C2 clause h asserts
  these rows and the round-46 entry byte-equal to base.
- **`corpus/knowledge/hyprland-input-devices-r46.md`** — its step 4 states the fallback; C2 answers the compile gap at its
  `:69` without rewriting the entry (append-only rule, `CORPUS.md` rule 2).
- **`corpus/knowledge/xdg-terminal-selection-r47.md`** — cold-cache selection. This round adds the warm path; the round-47
  entry's launch half stays `[UNK]` and is not restated.
- **`corpus/README.md:110`, `:112`** — the two open sentences this round moves ("the warm-cache path", "the XKB compile
  itself"); the frontier bullet below is where they close.

Rejected — the two screened-and-refused candidates of `l1-draft/gate-rows.md` (ArchWiki Xorg keyboard page and the
unversioned xkbcommon.org doc index, reasons + flip conditions verbatim in the Gate block above), plus the
assimilation near-misses `w1/ScoutShokuknow` refused by scope (a Japanese input-observation entry, a focus-grab
entry, the voxtype row and an fcitx5 window-rule row — none is this round's plane). Two rejection classes this round must state
explicitly, because they are the round's premise:

- a row on the **host binary** `/usr/bin/xdg-terminal-exec` as a separate source from the tag URL would cite the same bytes;
  the host is a pin comparison (`sha256sum` equality, round-47 precedent), not its own row. holds: no new C1 row was appended; the pin's sha256 was re-verified this round
  (`w1/ExecXkbSource`, `w1/ScrSkill` receipts).
- decided: the host's xkb tree is `/usr/share/xkeyboard-config-2` (xkeyboard-config 2.48-1); S346 rows it as the
  installed generated ruleset beside its tag source (`rules/rules.in` + `rules/meson.build`, the build recipe the
  package runs), and S347's symbols/br is byte-equal between tag and host (`w1/ScrRows` `cmp` receipts). The row
  cites the installed copy's own sha256 — a host-bytes row would duplicate it.

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

After (`.ufo/waves/round-48/receipts/census-after.txt`, exit 0, captured at the integrated data state): the same 17
`W04` + 1 `W01` + `mado ok` — no new `W04` line among `S340`-`S351` (none of the new URLs repeats a held one) and `W01`
count holds at 1 (S277 unchanged).

Command (both ends): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.

### Registry changes

| surface | old (base `579f694b`) | new |
|---|---|---|
| `corpus/SOURCES.md` | 276 rows, top `S339` | `288` rows, top `S351`; rows `S340`-`S351` appended after the last `S` row, 11 cells each, tier `A`, `mined`, opened `2026-10-26`, used-by `corpus/knowledge/xkb-keymap-compile-r48.md` |
| `corpus/knowledge/` | 64 files | 65 (`xkb-keymap-compile-r48.md`) |
| `corpus/README.md` | 64 index rows (last the round-47 row at `:75`) | 65 (one three-cell row after `:75`), plus the `## Frontier` bullet at `:112` (a4r1 `MadoA4RevLesson`: the salvaged `:110` is a blank line at the tip) |
| `corpus/lessons/` | 70 files | 71 (this lesson) |
| `tools/` | 15 files, `mado-terminal.py` the newest | 15 — C1 extended the file in place |
| held rows `S318`/`S319`, `corpus/knowledge/hyprland-input-devices-r46.md` | as at base | byte-identical (C2 clause h; command in the acceptance table) |
| `quality/` | `counters/c1-r47-terminal.py`, `c2-r47-terminal-entry.py` | adds v1 `c1-r48-terminal-cache.py`, `c2-r48-xkb-entry.py`, `c1-r48-fixtures.json` (freeze `3e6c848a`) and v2 `c1-r48-terminal-cache-v2.py`, `c1-r48-fixtures-v2.json` (228 warm: schema v2 `mtime`, `prime`, `after`, `cache`, `links`), `c2-r48-xkb-entry-v2.py`; `check-landed-contract.py` (QUALITY 96), `check-round-outcome-first.py` (QUALITY 99), `session-material-waivers.txt`; `check-session-material.py` becomes gate v2 |

### Renumber map

None this round, and the reason is measured: the registry's top id is `S339` (276 ids, `S001`-`S339`), the C2 block opens at
`S340`, and no supersession or staged adoption is drafted, so no row changes its id. The staged band still runs `S203`-`S349`
(147 ids) — the upper end `S340`-`S349` lies inside the new C2 block — so **any later adoption of a staged row is renumbered
by document first**, exactly as round 47's S346-S353 → S332-S339 map did. re-checked against the landed rows: S340-S351 are the entry's own ids, no staged row was adopted, so no row
moved.

### Id guard and quarantine

The dispatch artifacts under `.ufo/waves/round-48/assimilation/` are measured, not typed; re-derived here read-only:
`reg-ids` 276 lines (`S001`-`S339`), `staged-ids` 147 lines (`S203`-`S349`), `collisions` 84 lines (`S203`-`S339`), and the
collision set is exactly the intersection (`python3` set comparison: `equal_to_file=True`). Round 47 reported 70 collisions on
the 262-id registry; the delta is the 14 rows landed since (S326-S339). `w1/ExecIdGuard` ran the section-10 block verbatim: reg `276` / staged `147` / collisions `84` (S203-S221, S253,
S258, S277-S339 — every lane id ≥ S253 collides with a staged id), proved the guard on a scratch registry whose
indented `  | S002 |` row produced a non-empty `collisions`, wrote the 13-row quarantine slice, and swept the staged
knowledge tree for `xkb|keymap|xkbcommon|xdg-terminal|terminal cache` — no staged entry touches this round's plane
(`w1/ExecIdGuard`, `w1/ScoutShokuknow`).

Quarantine (round-47 slice, inherited): `.ufo/waves/round-47/assimilation/quarantine-slice` is a 13-line file — six
`payload-absent` rows (`S189`, `S195`, `S201`, `S205`, `S224`, `S228`) and seven `no quote was checked` rows (`S199`, `S200`,
`S209`, `S222`, `S223`, `S225`, `S235`). None was appended or hand-checked in round 47 (`corpus/lessons/round-47.md:233-234`),
the round-48 slice (`.ufo/waves/round-48/assimilation/quarantine-slice`, 13 rows: S189, S195, S201, S205, S224,
S228 `payload-absent`; S199, S200, S209, S222, S223, S225, S235 `no quote was checked`) re-derives the same set — no
row left quarantine; no staged entry was adopted, so no row was hand-checked either (Assimilation: none this round —
no package theme matches the C1/C2 planes).

### considerthese

`considerthese/2026-10-26.md` is the latest reflection (`ls considerthese/`; no newer file). Proposal 2 was refused in round 47
with its reason (`corpus/lessons/round-47.md:227`), proposal 3 landed as QUALITY 90, so `w1/ScrConsider` drafts exactly one
still-unimplemented proposal as a checkable landing (QUALITY criterion, lesson paragraph or SOURCES row). landed: proposal 6 (lead with round-level outcomes) — the only still-unimplemented lane-buildable item per
`w1/ScrConsider`'s sweep — became QUALITY 99 with `quality/check-round-outcome-first.py` (`SELFTEST: ok cases=5`;
`rounds=47 pass=0 fail=34 skip=13` at base, i.e. it fails on real bytes). `w1/SentPrivacy` measured proposal 1's
substance on this round's own receipts: the registered gate misses 16 of 19 synthetic shapes and scans `.ufo/` only
(S2) — routed to `## Mistakes` M48-6 rather than re-mined as a proposal.)

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
delta with both locators) are the receipts. Measured pairs (`w1/ExecHomeUnset`, `w1/ScrD1Line` receipts): HOME absent + all `XDG_*` set → pin `rc 0` + id, tool
`rc 2`; HOME absent + `XDG_CACHE_HOME` (or `-CONFIG` or `-DATA`) absent → pin `rc 1` `HOME: unbound variable` at
`x:148`/`:166`/`:172`, empty stdout. The round-48 contract models the pin — exit 1, empty stdout exactly where an
unset `XDG_*` default must expand HOME (registration §C1, "HOME-unset follows the resolver's `set -u` exit 1/empty
stdout when a default expansion needs HOME") — scored by the ten `v2-hu-*` fixtures plus `E-01`.

## Search log

Question: which `kb_rules/kb_model/kb_layout/kb_variant/kb_options` names compile into a keymap on this host (libxkbcommon
1.13.2, xkeyboard-config 2.48), which fail and which are dropped with a warning, and how a failed compile maps onto
Hyprland 0.56.2's `us` fallback — and, separately, which cache invalidation the resolver applies before it trusts
`$XDG_CACHE_HOME/xdg-terminal-exec`?

Where searched: the libxkbcommon tag tree and its docs, the xkeyboard-config tag tree (rules, symbols, the include order),
the host read-only (`xkbcli compile-keymap` with `--layout/--variant/--model/--options/--rules`, never a compositor verb;
`~/.config/hypr/input.conf` as bytes for the host names), the round-47 script pin and its README, and the lane registry
`corpus/SOURCES.md`. Opened candidates: the libxkbcommon 1.13.2 tag tree and its man/header interfaces, the
xkeyboard-config 2.48 tag plus the installed `rules/evdev` and `symbols/br`, the ArchWiki keyboard page and the
unpinned xkbcommon.org doc index (both rejected), and the host `xkbcli` receipt; the held overlap is S318/S319,
S326/S327 and the round-46 entry (held list above).

Identified: fourteen candidate sources opened — twelve admitted as S340-S351, two rejected (plus the held-duplicate refusal of Hyprland `IKeyboard.cpp`).

Screened: each admitted pin at the ranges its row cites (`rules.c:1257-1297, 1986-2064`; `xkbcomp.c:157-166`;
`include.c:333-506`; `context.c:243-338, 503`; `context-priv.c:129-218`; `meson_options.txt:32-59`;
`tools/compile-keymap.c:521-587`; `messages-codes.h`; `rules.in` + `meson.build:18-39` + installed `rules/evdev`;
`symbols/br`; the 14 270-B receipt).

Included: S340 rules matcher, S341 RMLVO→KcCGST resolve, S342 file/map lookup + XKB-338/661, S343 include order,
S344 empty-name defaults, S345 build defaults, S346 generated evdev mapping, S347 br variants, S348 xkbcli contract,
S349 message ids, S350 host receipt.

Excluded: the ArchWiki page and the xkbcommon.org index — reasons and flip conditions in the Gate's Rejected block.

Stop: every compile outcome the entry states has a host receipt and a pinned line; re-open when libxkbcommon or
xkeyboard-config moves past 1.13.2 / 2.48, when the host's `kb_*` names change, or when Hyprland's keymap construction leaves
`efb50993`. For C1: stop when the warm run's stdout+rc is reproduced on the invalidation fixtures; re-open when
`xdg-terminal-exec` leaves 0.14.3 or upstream changes the cache format.

## Mistakes

**M48-1** · class `contract-narrowing` · evidence: the C1 contract froze the r47 reference docstring (`.ufo/waves/round-47/l1-draft/mado-terminal.py:84`, blob `762d042c…`, six out-of-contract classes) while the delivered tool names nine (`tools/mado-terminal.py:85`, adding HOME unset, a FIFO `*.desktop` in a later dir, symlink loops) and the round-47 registration paragraph names none of the three; `check96` reads `added=3 unregistered=3 verdict=NARROWED` rc 1 (`.ufo/waves/round-48/w1/ScrMistakes/receipts/check96-run.txt`). · captured-by: none (criterion 96 now covers it). · fix: the D1 delta line (§The D1 delta line), the round-48 registrations carrying each exclusion with its condition, and QUALITY 96 with the L1-revised instrument `quality/check-landed-contract.py` (w2 `ScoutQualityCriteria` D1: the w1 draft errored rc 2 on this round's own tool; D2: a deleted class passed) — shown able to fail: `NARROWED` rc 1 on the round-47 pair, `UNDECLARED` rc 1 on a deleted `-h/--help`, `OK` rc 0 with the erratum and on round 48's freeze-vs-landed pair (`.ufo/waves/round-48/receipts/v2/check96-l1.txt`).

**M48-2** · class `unreceipted-number` · evidence: the round-47 report's `findings=128` at the tip appears in no committed receipt (`git grep -c 'findings=128' 579f694b` → no match; routed at `corpus/lessons/round-47-verifier-spotcheck.md:132`); `check97` over the report vs 1598 round-47 receipts reads `tokens=11 missing=1 verdict=UNRECEIPTED` rc 1 while criterion 69's own instrument prints PASS on the same bytes. · captured-by: criterion 10 (`corpus/QUALITY.md:16`, "rederive it from the named revision") - the rule existed, its application was skipped. · fix: the number is now receipted — `w1/ExecD2Receipt/receipts/session-material-{60edb66e,d40189c9,579f694b}.txt` print `findings=115/128/128` at the three revisions, tree-intrinsic (identical on a `--shared` clone and under `cd`); the w1 draft criterion 97 was **withdrawn before landing** as a restatement of 10 (w2 `CritMistakes`; the lane's own precedent `lessons/round-20.md` M5 withdrew criterion 30 for the same reason) and its instrument `w1/ScrMistakes/check97.py` stays a seat receipt that shows criterion 10 able to fail (`tokens=11 missing=1` rc 1 on the round-47 report).

**M48-3** · class `routing` · evidence: `.ufo/waves/round-47/w2/ExecC1Determinism.md:10` reported the frozen fixture set's readdir blind spot and was never routed — `check98` reads `finding_seats=7 unrouted=4` rc 1 on the round-47 w2 set (and `unrouted=1` on w1). · captured-by: criterion 52 (`corpus/QUALITY.md:358`, "the sweep names the gap's class, pointer and disposition") - not applied to w2 seat findings in round 47. · fix: routed here as M47-15, and the schema-v2 set carries ten `READDIR` fixtures (`v2-rd-01`..`v2-rd-10`: two or more valid candidates in one directory whose selected id depends on readdir order, including `v2-rd-05-three` and `v2-rd-06-reverse-create`); a `sorted()` walk is control `mut-warm-ignores-args`/fixture failure class, not a lottery; the w1 draft criterion 98 was **withdrawn before landing** as a duplicate of 52 (w2 `CritMistakes`), and this lesson applies 52 to all 48 w2 seats in `### w2 routing` below.

**M48-4** · class `locator` · evidence: `corpus/knowledge/xdg-terminal-selection-r47.md:95` cites `terminal-route-r17.md:150-151` for the `--dir=` `[UNK]` sentence that sits at `:149-150` (`:151` is a blank line); the same-method sweep found 6 citing locators, 5 correct (`w1/ScrErrataD4/receipts/d4-sweep.txt`, 3 identical runs); `check99` reads `checked=4 violations=4` rc 1. · captured-by: none (criterion 77's instrument reads only `--fetch` names; criterion 97 now covers corpus-to-corpus locators). · fix: the append-only `## Erratum` block landed at the entry's EOF (E1 names `terminal-route-r17.md:149-150`), QUALITY 97 (`check99.py`) reads `violations=0` on the corrected copy.

**M48-5** · class `provider` · evidence: both waves' only scratch bound is prose (round-47 and round-48 `w1-spec.json`: `grep -c ulimit` → 0); `check100` reads `enforced=0 prose=4 verdict=PROSE-ONLY` rc 1 for both (`w1/ScrMistakes/receipts/check100-run.txt`). · captured-by: none (M47-7 named it; criterion 98 now covers it). · fix: the w2 dispatch carries `ulimit -f 2048` in every seat task (the required-shell-writer bound) — QUALITY 98 (`check100.py`) reads `enforced=1 verdict=OK` on a dispatch carrying the cap; each seat records its largest file.

**M48-6** · class `vacuous` · evidence (L1, attempt 2): `w1/ExecSessionMarker`'s install set shipped `sidecars/` as an empty directory — the waivers registry named 48 marker files that were not in the tree (the seat's `install.sh` would have installed 0 of 48 while printing `installed sidecars=48` only by counting its own find over a populated dir); the set was regenerated deterministically from `quality/session-material-waivers.txt` (`SYNTHETIC-MATERIAL v1 kind=… rules=… sha256=…` per row) and all 48 verified `OK` against the seat's `SHA256SUMS`. · captured-by: criterion 92's produced-vs-committed comparison would have caught it *if* run on the seat dir; it was not run there this round — partial coverage. · fix: L1 ran the regeneration + `sha256sum -c` (48/48 OK) before installing; the gate v2 selftest `69/69` and the planted-real-dump control are the live proof.

**M48-7** · class `flaky-instrument` · evidence (L1, attempt 2): `PRED-C1-r48` clause r's strace reader counted every post-python line as a trip, so bwrap's attach noise (`??? (<detached …>)`) scored `trips=2` and flipped one of five identical reference runs to `readonly=fail` (`receipts/l1-c1-ref-final3.txt`) while four read `trips=0` (`-ref-final.txt`, `-final2.txt`, `-lsfix.txt`, `-prefreeze.txt`). · captured-by: none — the counter was not yet frozen, so the fix is a pre-freeze parser tightening, not a predicate amendment. · fix: `check_trace` now trips only on a traced syscall name at column 0 followed by `(`; `receipts/l1-c1-ref-rfix.txt` reads `trips=0 verdict=TARGET_MET` and clause-r mutants (`delegate-ls`, `md5-subproc`) still trip 14 real execve's each in the controls battery.

**M48-8** · class `instrument-blind-spot` · evidence: `w1/SentPrivacy` measured the registered session-material gate missing 16 of 19 synthetic shapes drawn from this round's own write surfaces, scanning `.ufo/` only (`quality/check-session-material.py:256`) and already red at base (`findings=128`) — every `/home/<user>` path class this round's receipts actually carry went unseen (33 receipt files, 75 `/home` lines, 0 findings). · captured-by: none (QUALITY 93 registers the gate; nothing audits its coverage envelope). · fix: routed to round 49 as an instrument-widening item (marker v2 covered the synthetic shapes R3 needed; the 16-class gap and the `.ufo/` scope are named, not silently closed).

**M48-9** · class `freeze-before-controls` · evidence: `registration.md:14` requires the 20 w1 controls re-scored on the frozen merged fixture set with "a control that meets triggers a fixture/counter repair before freeze", yet the v1 freeze `3e6c848a` committed with 11 of 20 controls `cut` (`w1/ExecControlsC1.md` §1; w2 `CritQualityTrend` §5) - and the first of them a w2 seat scored, `writes-cache`, met `PRED-C1-r48` (`w2/RevC1Counter` B1, `w2/MutC1ReadOnly` M-WRITE; seven more w2 candidates met C1 v1 and two met C2 v1). · captured-by: the registration's own control rule (not run at freeze) and criterion 61/64 (freeze binds the commands it names) - neither checks that the control receipts exist before the freeze commit. · fix: registration v2 (`registration-v2.md`) re-scored the complete set - 66 candidates, the base and absent tools included (`CTL_C1v2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 66 …)`) - against v2 before any data, receipt `receipts/v2/ctl-c1v2.txt`; shown able to fail: `writes-cache` (w1 and w2 builds), `content-cold2`, `M-WRITE`, `M-FORK`, `m4-break-cmdv`, `joinless`, `unreadable_absent` and `m3-no-deref` all `TARGET_MET` under v1 and `TARGET_MISSED` under v2 (`receipts/v2/ctl/`), and on C2 `c-pin-mode-S340` / `x-quote-600-invisible` flip admitted → missed (`receipts/v2/c2v2-revc2counter-matrix.txt`).

**M48-10** · class `host-write` · evidence: `w2/SentScope` S1 - `/home/vgpnk/.cache/xdg-terminal-exec` (the operator's resolver cache) was overwritten at 22:26:35 -03 with the 7 bytes `r48-w2\n` by an unsandboxed run of `w2/MutC1ReadOnly`'s M-WRITE mutant (`mkmutants.py:31` derives the target from the ambient `HOME`); the attempt-3 L1 confirmed the file still held those bytes (`stat`: 7 B, mtime 1793064395) and left it untouched as operator-owned. Its "L0 question filed" was not true: no `mado | round-48` line exists in `.ufo/l0-questions.md` (attempt 4, `grep -c 'mado | round-48'` → 0). Attempt 4 re-read the metadata only (`stat`: 190 B, mtime 1793069967 = 2026-10-26 23:59:27 -03): a resolver run rewrote the cache after the overwrite, so the host is no longer in the damaged state and no operator decision is open. The resolver had read the 7-byte file as `invalid cache data` and answered cold, so SUPER+RETURN was never misdirected. · captured-by: none - the wave context forbade host writes in prose; nothing ran a mutant only inside bwrap. · fix: routed to round 49: a mutant that writes is executed only through the counter's sandbox (or with `HOME`/`XDG_CACHE_HOME` pointed into scratch), and the wave context names the operator cache path as a must-not-change file with a before/after digest receipt (w1 `SentHost` already took one: `01-host-cache-before.txt`).

**M48-11** · class `unreceipted-number` (attempt 4) · evidence: the salvaged lesson stated "222 warm fixtures" for the v2 fixture set at `:8` and `:145` of `cf3deeec`'s working copy, while the registered file holds 228 (`registration-v2.md:50` "the 204 v1 fixtures unchanged + 24"; the counter prints `warm=228/228`, `receipts/v2/ctl/FINAL.txt`), and it claimed an L0 question that was never filed (M48-10). Both are numbers or facts transcribed by the author, not emitted by the instrument that owns them. · captured-by: criterion 10 (`corpus/QUALITY.md:16`, "rederive it from the named revision") and 94 (a carried number is emitted by the ledger that owns it) - the rules existed; the attempt-3 draft was never re-derived before the session ended. · fix: both corrected from the instruments (`228` from the counter's own line; the L0 claim replaced by the `grep -c` and `stat` re-reads above); shown able to fail: `grep -cE '[,(] 222 warm|[(]222 warm' corpus/lessons/round-48.md` read 2 on the salvaged copy and reads 0 at the data commit.

**M48-12** · class `flaky-instrument` (attempt 4, harm watch) · evidence: the round-47 frozen C1 counter re-run at the round-48 tip `d8e3d600` read `readonly=fail ... TARGET_MISSED` once, with its only trip `clause=r trips=1 ???( <detached ...>` (`.ufo/waves/round-48/receipts/a4/c1-r47-at-tip.txt:196`), and `trips=0 ... TARGET_MET` on three immediate re-runs of the same bytes (`receipts/a4/c1-r47-at-tip-run2.txt`..`run4.txt`). The trip is bwrap's attach noise, the class M48-7 fixed in the round-48 counters before their freeze; `PRED-C1-r47` is frozen and keeps the old reader. · captured-by: none for frozen counters (M48-7's fix reached only the counters not yet frozen). · fix: a harm watch that re-runs a frozen counter commits every run and reads a `readonly=fail` whose only trip lines are `???(`/`<detached` as instrument noise, never as harm, and re-runs it at least three times; routed to round 49 as a criterion with this receipt set as its shown-to-fail case (one red, three green, same bytes).

**M48-13** · class `provider` (attempt 4, residual dispatch) · evidence: the `a4r1` context required `ulimit -f 2048` (1 MiB per file) before every writer and named `git clone -q --shared` as the clone recipe; the lane tracks evidence files over 1 MiB (rounds 20-22), so a checkout under that cap fails. Two seats aborted with no report (`MadoA4RevC1Write`, `MadoA4RevGate`: "checkout could not complete because RLIMIT_FSIZE=1 MiB rejects numerous committed large files", `.ufo/waves/round-48/a4r1-results.json`), two more stalled on the same wall (`MadoA4RevC2v2Diff`: "Index lock >1MiB"; `MadoA4RevLesson` ended without a report file), and three worked around it with `--no-checkout` clones (`MadoA4CritEntry.md:34`, `MadoA4CritSalvage.md:17`, `MadoA4RevC1v2Diff.md:115-117`). · captured-by: none - QUALITY 98 requires the cap to be enforced (`receipts/a4/check100-a4r1.txt` reads `verdict=OK`) but nothing checks the cap against the recipe the same dispatch prescribes. · fix: routed to round 49 - a dispatch that sets a file-size cap prescribes a recipe that writes under it (`git clone --shared --no-checkout` plus `git show`/`git archive` of the needed paths, or the counter's own `--rev` reading), and QUALITY 98 gains a recipe-compatibility clause with this wave as its shown-to-fail case (4 of 8 seats lost).

### Applications of existing criteria

- M48-1 → **96** (`quality/check-landed-contract.py`): any unregistered delta between the frozen and the landed out-of-contract list fails (`NARROWED` or `UNDECLARED`).
- M48-2 → **10** (applied; draft 97 withdrawn as a restatement).
- M48-3 → **52** (applied to every w2 seat below; draft 98 withdrawn as a duplicate).
- M48-4 → **97** (`check99.py`, extends 77; also closes M46-6's residual).
- M48-5 → **98** (`check100.py`): a wave's scratch bound must be an executed cap, not prose; declared limit: a sentence that names `ulimit -f` reads OK.
- M48-6 → **92** (existing): produced-vs-committed set comparison, applied by the L1 at integration.
- M48-7 → instrument hygiene; no new criterion (fixed before the v1 freeze; v2 repaired the related split-execve parse).
- M48-8 → routed (round 49); no criterion yet.
- M48-9 → **61/64** extended in practice by registration v2's rule "the complete control set is scored before data"; no new number (a counter that reads control receipts at the freeze is round-49 work).
- M48-10 → routed (round 49).
- M48-11 → **10**/**94** (applied at attempt-4 integration; no new criterion).
- M48-12 → routed (round 49; harm-watch reading of frozen counters).
- M48-13 → routed (round 49; extends 98: the cap and the recipe are checked together).
- considerthese proposal 6 → **99** (`check-round-outcome-first.py`): the closure section leads with the round-level outcome.

### Conflicts recorded for the judge

- **`w1/ExecHomeUnset` vs `w1/ScrD1Line`** measured the same HOME/FIFO/loop shapes and agree on substance; they collided only
  on numbering — both drafted a `**M47-12**`. The peer relabelled its line a placeholder and deferred to `ScrD1Line`'s map
  (M47-11 combined delta, M47-12 FIFO, M47-13 loops, M47-14 step-4, M47-15 readdir); the round-47 lesson carries ScrD1Line's
  five lines only.
- **`w1/ScrConsider` vs `w1/ScoutShokuknow`** read the same considerthese file and reached opposite verdicts on proposal 6:
  ScrConsider lands it as buildable (criterion + runnable check, red on base bytes), ScoutShokuknow calls it
  "unimplementable in-lane" (a reflection-author behaviour). The L1 ruled with ScrConsider: a check exists that fails on
  real bytes (`rounds=47 pass=0 fail=34`), which is the admission bar; the alternative reading is recorded here, not erased.
- **`w1/ExecControlsC1` partial pass**: 9 of its 20 draft-counter control rows read `cut` by the wave deadline (each still
  MISSES the local pin-judged loop with a named clause); the report's draft column is partial — the w2 falsify wave re-scores
  every control against the frozen merged fixture set, so the count above is the seat's own, not a full battery result.
- **`SentHost`/`SentPrivacy` vs the marker set**: the marker suppresses only registered synthetic namespaces; SentPrivacy's
  point stands that the gate's coverage envelope is narrower than its registry wording — carried as M48-8, not resolved.
- **C1 clause-i census terms**: the counter reports `present_at_rev=3/4` (one of the four ground terms occurs once under
  `corpus/` at base inside this lesson's own text) — within predicate (≥2 required), recorded so the closure reads the
  counter's own number rather than an assumed 4/4.
- **`w2/CritMistakes` vs `w2/ScoutQualityCriteria`** on the w1 draft criteria: ScoutQualityCriteria admits 97 and 98
  with notes; CritMistakes calls 97 a restatement of 10 and 98 a duplicate of 52. The L1 ruled with CritMistakes: the
  lane's own precedent (`lessons/round-20.md` M5) withdrew a restatement of 10 before landing, and 52's text already
  requires naming each gap's class, pointer and disposition. Both seats' defects in 96 (the rc-2 error on this round's
  tool, the passing deletion) were fixed in `quality/check-landed-contract.py`.
- **`w2/RevC2Entry` vs the entry's step 9**: the seat's M1 was right and the draft wrong (WARNING only for more layouts
  than variants; ERROR for fewer) - the landed entry carries the split; `w2/CritQualityTrend` §4.1 found the same.
- **`w2/CritQualityTrend` trend reading**: it argues quality `harmed` on the v1 candidate (false SKILL rule, false entry
  sentence, stale README line, must-miss control met). Each item was repaired before data (SKILL rows 2277-2282, entry
  step 9, README round-48 bullet, v2 controls); the report's quality verdict is argued from the landed bytes, with this
  seat's reading recorded rather than erased.

### w2 routing (criterion 52 applied to every w2 seat)

Every w2 seat with its disposition; `fixed` = repaired before the data commit (v2 or the landed bytes), `residual` =
declared in `registration-v2.md` or the v2 counters' docstrings, `routed` = round 49 with this lesson as the age anchor,
`held` = attacked and stood. Seat reports are `.ufo/waves/round-48/w2/<Seat>.md`.

| seat | finding | disposition |
|---|---|---|
| RevC1Counter | B1 a cache-writing tool meets v1; B2 live-path `--print-content` unscored; control attributions wrong | fixed (v2 clause r write tripwire; L1-11..16; registration-v2 control table) |
| RevC1Cache | F1 multi-line cached command, F2 unreadable cache unscored; F3 `XTE_CACHE_ENABLED=''` side effect unobservable | fixed (L1-19..21); F3 superseded by L1-31 (`disabled`, observable) |
| RevC1Ls | `-L` unscored (no symlinks); owner justification unscored; OOC classes undeclared; `LS_COLORS` guard over-broad | fixed (`links`, L1-22..28); residual (owner, OOC list); routed (guard narrowing) |
| RevC1Fixtures | no drift; premise checked for DIFFERS/SAME only | held; residual |
| RevC1Explain | three bad explain controls meet v1 (foreign-root capture, empty word, newline in first word) | fixed (fourth capture, L1-33/34, explain `\n`) |
| RevC2Counter | pin mode unenforced; >600-char quote dropped; nine declared residuals | fixed (C2 v2); residual |
| RevC2Entry | M1 step 9 severity; L1 precedence overstated; N1/N2 | fixed (entry) |
| RevRoutes | none blocking; `--work` under the lane parent refused | held |
| RevErrataR45 | R4b append keeps the frozen round-45 verdicts | held |
| RevXkbIntent | LOW-1 receipt generator path; LOW-2 `kb_file` wording; LOW-3 shared libxkbcommon | residual (frozen receipt); fixed (entry) |
| RevQualityAdmission | no blocking; clause-r flake history | held (v2 also repairs the split-execve parse) |
| RevMisroot | the misroot note reproduces; writer attribution unproven | held; recorded |
| CritC1Time | six-month OOC second not in registration; dir mtimes inert | residual (v2 docstring) |
| CritC1LsEnv | `POSIXLY_CORRECT` cold run answered while the pin exits 1 | fixed (tool guard on every path; selftest 70/70) |
| CritC2Scope | new ground confirmed; two precision notes | held |
| CritC2FalseClaim | F1-F4 entry prose | fixed (entry) |
| CritC2Pin | F1 S346 chain, F3 generator path, F5 dead pin; F2 recheck triggers, F4 anchors, F6 count | residual; fixed |
| CritRouted | R3 and R4b hold | held |
| CritMistakes | 97 restates 10, 98 duplicates 52; 96/99/100 defects | fixed (96 instrument; 97/98 withdrawn; limits declared) |
| CritQualityTrend | SKILL false rule and duplicate, stale README, entry step 9, must-miss control met | fixed (SKILL rows, README bullet, entry, v2 controls) |
| CritContextDrift | two low structural gaps in the wave context | routed (spec generator) |
| CritFrontier | lesson frontier-step defects | fixed (this lesson: Gate S347/S351, README bullet, routing) |
| CritSessionMarker | marker works; SKILL row stale | fixed (`SKILL.md` gate row replaced) |
| CritDataCompleteness | C1-A/B/C fixture omissions; C2-A NULL unpinned | fixed (L1-29..32; S351) |
| CritC1OneByte | report not landed at the v2 freeze | read after data; reported in the round report |
| CritCounterTiming | report not landed at the v2 freeze | read after data; reported in the round report |
| MutC1Counter | report not landed at the v2 freeze | read after data; reported in the round report |
| MutC1Tool | `m4-break-cmdv` survives v1 | fixed (L1-17/18) |
| MutC1ReadOnly | M-WRITE, M-FORK meet v1; an unsandboxed run wrote the operator cache | fixed (v2 clause r); M48-10 routed |
| MutC2Counter | every clause mutant rejected | held |
| MutC2Entry | 16 mutants; prose-only mutants admitted | residual (clauses read locators, not sentence truth) |
| MutC2OneByte | receipt diagnostic-id swap admitted | residual (f/r bind labels, not receipt prose) |
| MutC2Receipt | receipt mutants | residual as above |
| MutC2Replay | PATH shim fakes the replay judge | fixed (C2 v2 `/usr/bin/xkbcli`, clean env) |
| MutRoutedR3 | gate v2 behaves both ways | held |
| ScoutFreezeBlobs | freeze set complete and byte-consistent | held |
| ScoutCensus | gate-prose quoting note | fixed (Gate lines quote verbatim) |
| ScoutConsiderthese | proposal 6 disposition | held (QUALITY 99) |
| ScoutMisroot | misroot confirmed, writer unattributed | recorded |
| ScoutQualityCriteria | 96 D1/D2; 97/98 admit with notes | fixed (96); 97/98 ruled withdrawn (Conflicts) |
| ScoutEntryLocators | README locator shifts at data | fixed (entry ground line) |
| ScoutControls | writes-v2 probe meets v1 | fixed (v2) |
| ConnClaimOverlap | read sets disjoint, separable both ways | held |
| ConnSourceLinks | S347 gate line lost, third reject lost; generator path; pin count; S349 anchors; dead pin | fixed; residual |
| ConnMistakes | M48-3 not landed | fixed (this table) |
| SentHost | F1 generator path; F2/F5 substrate PATH; F3/F4 receipt generator writes outside scratch | residual; routed |
| SentScratch | c2 replay accepts any TMPDIR; c1 `--work` admits `/tmp` | routed (round-49 counter amendment, scratch rule 4) |
| SentScope | S1 operator cache overwritten by a seat | M48-10, L0 question |

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

What the next closure needs to see (drafted acceptance — command and expected observation; results recorded
inline where they already exist):

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
   `README.md:112`) answered, not restated; rows `S340`-`S351` `mined` with the entry as used-by; sampled citations
   re-fetched; the `xkbcli` live receipt's rc/sha256 agreeing with the entry's host sentence.
3. **Per-axis verdicts** — operability, coverage, depth, freshness, calibration, adjacency, each with the basis.
4. **Discernment spot-check** of the five gate decisions above (three admits, two rejects) on outside re-reading, agree or
   disagree, with the reason.
5. **Trend verdicts** — expansion, quality, discernment, each `improved`/`unchanged`/`harmed` with limits named.
6. **Routed defects** — new identity, first locator, and what the next round must fix.

The closure is pending: a non-author judge writes `corpus/lessons/round-48-verifier-spotcheck.md` after this file lands.

## Frontier

The frontier step runs inside the 1-3 claim cap and is not a fourth claim. Its items as they stand:

1. **Registry curation** — rows `S340`-`S351` added; held rows `S318`/`S319` and the round-46 entry unchanged; the census
   block above is the record. No `status`/`recheck`/`used-by` cell on any existing row changed (verified: the rows.md
   append is insert-only after `| S339 |`, `git diff corpus/SOURCES.md` shows only `+` lines).
2. **Census** — before: 17 `W04` + 1 `W01` + `mado ok`, exit 0 (`.ufo/waves/round-48/receipts/census-before.txt`);
   after: identical 17 `W04` + 1 `W01` + `mado ok`, exit 0 (`receipts/census-after.txt`, same command).
3. **Mined mistake** — M48-1..M48-13 above.
4. **Sourced claim** — C2 rests on rows `S340`-`S351` opened this round; C1's oracle is the row-47 pin those rows already
   hold, so C1 adds no registry row.
5. **README frontier** — the landed bullet (`corpus/README.md:112`) names the XKB compile (rows S340-S351) and, in the
   same bullet, the warm-cache path moved from the round-47 bullet's "Still open" list to executed ground, with what
   stays open (the launch half of the round-17 `[UNK]`, `uwsm-app`'s environment, the refused `ls` corners).

Provenance: C1's contract is `.ufo/waves/round-48/claims.md` (cache read at
`xdg-terminal-exec:1179`, trust at `:179-298`, save at `:1455-1458`); C2's ground is
`corpus/knowledge/hyprland-input-devices-r46.md:69` and `corpus/README.md:112`; the host compile facts (rc 0 for `br` +
`compose:caps`, rc 1 for `zz`/`nope` variant, rc 0 + XKB-595 for an unknown option, rc 0 for an unknown model, rc 1 for
`--rules nope`) are the L1's 2026-10-26 observations, re-derived by the committed receipt and by both C2 counters' clause-r replay
(`receipts/v2/c2-mirror-*.txt`). The `us` fallback and `kb_file` stay open as stated; the warm-cache `ls -LRl` same-size/same-minute question
stays open too — the counter's fixtures bound it, they do not close it.

## a4r1 routing (attempt 4 residual call, criterion 52 applied)

Eight reviewer/critic seats attacked the committed data (`e5d0130d`, `d8e3d600`); results `.ufo/waves/round-48/a4r1-results.json`, reports `.ufo/waves/round-48/a4r1/<Seat>.md`.

| seat | finding | disposition |
|---|---|---|
| MadoA4RevC1v2Diff | no blocker; 21/26 counter hunks registered, 3 partly (docstring-only mechanics), 2 unregistered (work-dir prefix, symlink `utime` `follow_symlinks`); 204 v1 fixtures unchanged, 24 new ids match their classes; `TARGET_MET` re-derived at `d8e3d600` | held; Low 1-4 are residual registration-prose gaps (the counter docstring states them), recorded, no predicate change after data |
| MadoA4CritEntry | no false or overclaiming sentence in the sample; registration-v2 entry repairs all present; six `xkbcli` probes agree with the receipt on rc and diagnostic class | held |
| MadoA4CritSalvage | errata append-only (187+/0-); frozen `PRED-C2-r45-v2` still `admitted=1/1` at the tip (R4b); D4 locator correct; SKILL and README rows traced, none unsupported | held |
| MadoA4CritAdmission | withheld admission for missing evidence: the round-47 C1 harm-watch receipt (read mid-write, header only), the axis check at the tip, and cheapest do-nothing controls | fixed after the seat ran: `receipts/a4/c1-r47-at-tip*.txt` (M48-12), `receipts/a4/axis-at-scorecard.txt` and `receipts/axis-tip.txt` (`mismatched=0`), `receipts/a4/ctl-do-nothing.txt` (C2 stub and held-body controls `admitted=0/1`; C1 base and always-cold `TARGET_MISSED`); it ruled v2 a pre-data repair and C2 a frontier-to-core move |
| MadoA4RevLesson | (no report file; output in results) the lesson's README Frontier locator `:110` is a blank line at the tip | fixed (`:112`) |
| MadoA4RevC1Write | aborted, no report (file-size cap vs checkout) | dead; M48-13; the new-mutant attack on clause r is not run this round |
| MadoA4RevGate | aborted, no report (same) | dead; M48-13; the gate's both-ways demonstration rests on its selftest 69/69 (`receipts/a4/session-material-tip.txt`) |
| MadoA4RevC2v2Diff | no report (index over the 1 MiB cap) | dead; M48-13; v2 C2 attacks rest on the w2 harness and `receipts/v2/c2-shim-*.txt` |

