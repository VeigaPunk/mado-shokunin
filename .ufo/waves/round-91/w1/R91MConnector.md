# R91MConnector — sibling, assimilation, and source overlap (mado round 91, w1)

Seat: `R91MConnector` (connector). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round 91, ONE v1 wave `w1`, base `cc0381db585cc44c3dfc13ced807409c32c45bb0` (master; `git -C` read-only
`rev-parse HEAD` printed that value, rc 0). Scratch `S=/fast/scratch/hyaku/mado-r91/R91MConnector` was
created and removed; the final `test ! -e "$S"` printed true. One **DRAFT** oracle-probe fixture was
transiently created under the default temp dir because S had been removed by the preceding trap; the
probe's own `shutil.rmtree` removed it, and a residue check printed `none` (seat-process defect,
§5(d)). No install, no pacman, no mutating git/jj; the only durable writes are this report and the
three assimilation files named in this seat's item.

**Axes named.** C1 = **coverage** (default-application resolution as GLib 2.90.1 performs it).
C2 = **operability** (seat-report retention gate). This seat does not edit either candidate; it maps
the sibling/source ground and returns one bounded move for the coverage axis (§4).

Everything labelled **DRAFT** below is a pre-freeze probe, not a measurement. No receipt was written.

## 1. Sibling scan — no lane owns the default-application plane

Search terms: `mimeapps`, `xdg-mime`, `gdesktopappinfo`, `mimeinfo.cache`, `default application`,
plus `mime type`/`mimetype` and `.desktop`/`desktop entry` as widening terms. Scope was each sibling
lane's `corpus/knowledge`, `tools`, `SKILL.md` (and, for the exact-token pass, the whole lane root).
The exact-token whole-lane pass returned only souji's census capture; no lane's
`corpus/knowledge`, `tools` or `SKILL.md` holds a primary-term hit. The items below are the complete
set of hits (exact-token souji plus widening-term adjacents):

| lane | file:line | what it actually holds | owns the plane? |
|---|---|---|---|
| souji | `census/round-22/attempt2/sources/arch-gio.1.raw:407`; `.../arch-gio.1.txt:424` | the `gio(1)` man page as census source capture: “per-user overrides stored in `$XDG_DATA_HOME/applications/mimeapps.list`” and “The `mime` command can be used to change the default handler for a MIME type” | **no** — source capture only; souji's `PROVINCE.md`/`SKILL.md` have no MIME/default-app row (the only XDG hit in its SKILL is an unrelated writer/counter environment-scrub line at `SKILL.md:901`) |
| tabi | `corpus/knowledge/browser-surface-census.md:21` (also `:218`, `:248`) | `xdg-settings get default-web-browser` → `chromium.desktop` | **no** — a browser fact, not the MIME resolution chain |
| tsukuroi | `corpus/knowledge/aur-risk-plane-ver-s6.md:56`; `aur-risk-plane.md:208` | `~/.config/autostart/walker.desktop` as package-wiring evidence | **no** — package ownership, not default-app resolution |
| kaidoku | `corpus/knowledge/2026-10-13-r4-15-appimage-inner.md:16` | `MimeType=x-scheme-handler/...` inside an AppImage's desktop file | **no** — artifact internals |
| kake | `corpus/knowledge/link-preview-metadata.md:40` | MIME type for `og:image:type` | **no** — web metadata |
| kengaku / mori / audio / game-dev-3d | vendored evidence (`bottle.py` `default_app`, WHATWG MIME text, RTP `rtp.mime`, three.js `mimeType`) | unrelated source/vendored material | **no** |

Mado's own `tools/`, `corpus/` and `SKILL.md` return no match for the same terms, confirming the
declaration's base statement. The nearest sibling reader is tabi's browser-default probe; nobody
holds the search order, the Added/Removed/Default groups, the desktop-file load rules, or the
`gio mime` output shape.

**Does mado's PROVINCE cover it? No line.** The Owns block (`PROVINCE.md:6-12`, quoted verbatim):

> **Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,
> animations), `~/.config/waybar/`, `~/.config/walker/`, terminal emulator
> configs (`~/.config/alacritty|foot|kitty|ghostty/`), themes/wallpapers as
> declared files, screen/idle behavior (hypridle/hyprlock where present).
> The omarchy skill (`~/.agents/skills/omarchy/`) is documentation surface,
> read-only. All config trees are READ-ONLY for this lane: probe, measure,
> recommend — the operator applies changes.

`grep -n -i -E 'mime|xdg-open|mimeapps|default app' PROVINCE.md` returns no line. The closest owned
surface is `~/.config/walker/` (the launcher UI that consumes the default-app chain); the data C1
reads (`~/.config/mimeapps.list`, `$XDG_CONFIG_DIRS/*mimeapps.list`, `~/.local/share/applications`,
`/usr/local/share/applications`, `/usr/share/applications`, `/usr/share/mime`) is outside the Owns
block. **The plane is genuinely new, but the landing must add a PROVINCE row for the read set and
the write refusals** (`gio mime TYPE HANDLER`, `xdg-mime default`, `update-desktop-database` are
never run). This is a contract observation, not the move in §4.

## 2. Assimilation — no staged MIME/default-app/desktop entry; 94 exact id collisions, 53 more below the floor

Read-only reads of `/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md` and
`SOURCES.append.md`; nothing was run or written in shokuknow.

`MERGE-REPORT.md` stages **147 accepted rows (0 refused), 69 knowledge entries, rounds 1–16**, with
“lane registry currently holds **192** rows; first staged id is **S203**”. Neither file contains a
staged entry on the MIME/default-application/desktop-entry plane: the literal tokens `mime` and
`.desktop` return **no match** in either file. The 69 staged knowledge targets are the IPC,
idle-lock, focus-grab, bar-producer, gkeep and Japanese/Chinese-literature entries. Therefore
**Assimilation: none** on this plane for round 91; C1's citations come from the GLib 2.90.1 upstream
files, not from the merge package. (The merge package's only `gio`-adjacent material is absent; the
`gio(1)` man page is a *souji census* artifact, §1.)

**Id collision check — exact round-prompt §10 commands.** Run from the lane root with the 0–3-space
extractor; the artifact directory is
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-91/assimilation/`:

```
CHECK_RC=0 reg=438 staged=147 collisions=94
reg-ids     sha256 3df08cd2da49dbe6fe2cb0cb0cc5974321425af0d62a1693dab5071340a9bf81
staged-ids  sha256 079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d
collisions  sha256 18e1d089c96fd5f43af25a6a1c656cc296d5048192f08f1ffd6cc45ba5f82a5c
```

The registry is 438 unique ids `S001`–`S503`; the staged set is 147 unique ids `S203`–`S349`.
The **94 exact collisions** are `S203–S221, S253, S258, S277–S349` (full list in Appendix A and in
`collisions`). Guard proof (scratch fixture, then removed): a registry row written `  | S002 |`
produced `indented_collisions=1` under the 0–3-space pattern and `columnzero_collisions=0` under the
old column-zero pattern — the guard is live. The old pattern's grep exited 1 (no match) as expected;
the driver handled it explicitly and printed `GUARD indented_collisions=1 columnzero_collisions=0`.

**Finding — the exact-collision file is not sufficient for adoption.** 53 further staged ids are
**absent from the registry but below its maximum** (`S222–S252`, `S254–S257`, `S259–S276`); `comm`
does not flag them, yet they are not “continuing” the registry. All 147 staged ids (`S203`–`S349`)
are below the current maximum `S503`. The round prompt's own fix says “adopted ids continue the
lane's registry (append-only)”; the safe allocation floor is therefore `S504`, and the full map is

```
new_id(S_n) = S_(504 + (n - 203))      for every staged row S203..S349
first S203 -> S504; last S349 -> S650; 147 pairs, no reuse of a below-max gap
```

State the contradiction plainly: the merge report fixes the first staged id at `S203` against a
registry that then held 192 rows, but it does not establish that `S203` was `max+1`; the current
registry is 438 rows / max `S503`. Either way, an adapter that renumbers only the 94 `comm` hits
would insert 53 ids below the floor. The renumber map is an id map only; citations must still be
re-pointed **by document**, never by arithmetic. This seat does not adopt; the L1 owns the decision.

## 3. considerthese — what this round touches, and what it does not

| proposal | status at the r91 draft | r91 touch |
|---|---|---|
| `2026-11-06.md` P4 “Widen desktop coverage past bar + mako … Prefer one operator-config gap over another harness counter” | **still open as written**: its named gaps are window-rule live semantics, xdph/screen-share, clipboard, non-bar exclusive surfaces and hypridle volatility | **cited by the declaration**; C1 opens a *different* non-bar plane (default applications) and is the round's only P4-adjacent move. It does not implement the named gaps. Note r90 already covers xdg-desktop-portal **routing** (`corpus/knowledge/xdg-portal-routing-resolver-r90.md`), so “portals” is not wholly absent; screen-share and clipboard state remain open |
| `2026-11-05.md` P4 “Cover the compositor plane around the bar, not only the bar” | **still open**; r90 covers only portal routing | **adjacent, not implemented**: C1 is a desktop-file/MIME plane, not a compositor surface |
| `2026-11-06.md` P5 “Verify QUALITY 145 has an instrument, not only a criterion” | **still open as a claim-gating question**: `quality/check-wave-done.py` exists and is tool-ledgered (`quality/tool-ledger.md:63`), but no r91 claim binds `TARGET_MET` to it | **not touched**; C2 is a seat-report gate, not the wave-done/null-output instrument |
| `2026-11-06.md` P2 “emit `score_scope=finite-cases`” | **partially adopted earlier, not in r91**: `quality/counters/c1-r89-mako-regex.py:203` prints it; the r91 C1/C2 counters have no `score_scope` (grep: no match) | **not touched** |
| `2026-11-06.md` P1, `2026-11-05.md` P1/P2 (cross-round survivor ledger) | **still open**: r89 has a survivor-kill counter, but no cross-round ledger; the r87 mako survivors (`M03/M05/M06/M08/M10`) are not tracked as survivors in round-91 (the r91 C1 mutant file reuses those ids for *different* mutants) | **not touched** |
| `2026-11-06.md` P3, `2026-11-05.md` P3 (live mako check), P5 (daily re-measure), P6 (smaller reads), P7 (stable proposal ids), `2026-11-06.md` P6/P7 | no r91 artifact cites them | **not touched** |

## 4. Proposed move — one bounded coverage move for C1 (DRAFT evidence)

**Move: before the L1 freeze, add three boundary cases and four matching mutant recipes to the C1
set, covering load-rule flags the current L1 set never exercises.**

### Evidence (DRAFT, 2026-11-06)

The current L1 file is
`controls/mime-cases-r91-l1.json` (sha256 `42a08f2cc19f137ac591df5f558e0fb2fba65c7471ce0760e2d755497c53e874`,
89 cases at read time (an earlier read of the same file returned 88; the later read includes `w06`);
the generator
`controls/gen-c1-cases-r91.py` sha256 `7f99d7e071af643343b7fe047d82430c7dcc22245c9531b6099629ebe8e6d2be`
regenerates the same 89 ids, so there is no drift *at this read*). The candidate is
`build/mado-mime.c1.py` sha256 `79645659c5a257e57c90ef4fb25d32bfb134b6f2ed03d3ead6788bdfbb1be160`.

Three gaps, all oracle-labelled:

1. **`NoDisplay` / `OnlyShowIn` / `NotShowIn` are never exercised.** The L1 file contains 0
   occurrences of each token. Probe (fixture-only XDG roots, `env -i`-equivalent, `/usr/bin/gio mime
   text/plain`, one type argument, read form; gio rc 0):
   - `NoDisplay=true` on the default/cache app: `Default application … a.desktop`; registered and
     recommended both `a.desktop, b.desktop` — **ignored**, not dropped.
   - `OnlyShowIn=GNOME;` under `XDG_CURRENT_DESKTOP=Hyprland`: default `a.desktop`; lists `a,b` — **ignored**.
   - `NotShowIn=Hyprland;` under `Hyprland`: default `a.desktop`; lists `a,b` — **ignored**.
   The candidate's `load()` reads only `Hidden` (candidate:572-573) and ignores these three flags, so
   it matches gio today; a mutant that filters any of them would survive the current 89-case L1 set
   because no case distinguishes it.
2. **No case removes *all* loadable apps from a nonempty cache.** Every L1 `Removed Associations`
   case leaves at least one app (`l05`, `l06`, `l12`, `l17`, `x07`, `w02`, `w06`). Probe: cache
   `a;b` + `[Removed Associations] text/plain=a.desktop;b.desktop` → gio prints
   `No default applications for “text/plain”` and **no list lines** (oracle shape: default null,
   registered null, recommended null). This is the missing branch of the declaration's own “prints
   the lists only after a default” rule; a mutant that applies the blocklist only to defaults would
   survive the current L1 set.
3. **The `Hidden` boolean case is not exercised.** The L1 has only `Hidden=true`, `Hidden=false`,
   `Hidden=1`. Probe: `Hidden=true` and `Hidden=1` drop the app from the lists (registered `b` only),
   while `Hidden=TRUE` and `Hidden=True` **do not** (registered `a,b`). The boolean is
   case-sensitive in GLib's desktop-file parser here. The candidate's exact `("true","1")` check
   (candidate:572-573) matches gio; a mutant that lowercases would survive the current L1 set. `Hidden=true`
   is already accepted as a default (`l20`), so the missing half is the lists with an uppercase
   spelling.

No current candidate defect was found by these probes: the candidate's model is right on all four
classes. The move is a **coverage/discrimination guard**, not a bug report.

### Affected axes

- **Coverage (C1): improves.** Three new oracle-labelled boundary classes; the either/or branches
  become decidable on the frozen set instead of only at fresh-leg time.
- **Operability (C2): unchanged.** No C2 file, expectation, or fixture is touched.
- **Contract: one wording decision.** The draft declaration's load-rule sentence names only
  “Type, TryExec, Exec program lookup, Hidden”. If the three cases are to be *scored*, the L1 should
  add “`NoDisplay`/`OnlyShowIn`/`NotShowIn` are ignored for this question” (one clause) before the
  freeze; otherwise keep the two show-in cases as unscored blind cases. The all-removed case needs
  no wording change — it is the declared “lists only after a default” branch.

### Move details

- Add to the L1 generator (ids follow its `rule` tags):
  - `m15-nodisplay-onlyshowin-ignored` — `NoDisplay=true` + `OnlyShowIn=GNOME;` on the cache-listed
    default app under `desktop="Hyprland"`; expect default + both lists (probe 1).
  - `l23-removed-all-suppresses-lists` — cache `a;b`, `[Removed Associations] text/plain=a.desktop;b.desktop`;
    expect default null, registered null, recommended null (probe 2).
  - `k13-hidden-uppercase-not-hidden` — `Hidden=TRUE` (and a second type/app for `Hidden=1` as the
    positive control, or a separate type) with cache `a;b`; expect `a,b` listed (probe 3).
- Route to `R91MMutC1` for the matching mutant recipes (the mutants file is that seat's):
  `M-ND` drop NoDisplay apps, `M-SI` apply show-in filtering, `M-RA` apply `[Removed]` only to the
  default, `M-HC` lowercase the `Hidden` value before comparison. Each should be killed by the
  matching case and survive the current set (the honest do-nothing control).
- Do not edit the L1 file from this seat; stage the three cases in a scratch file and let the L1
  merge them at the freeze (M87-5: the case file is live).

### Risks

1. **Claim widening** if the show-in cases are added without the declaration clause; the L1 decides
   before the freeze. A pre-freeze draft may change; after freeze it is an erratum.
2. **Live case file**: it changed 88→89 during this seat's read; pin the generator and case-file
   sha256 before adding, and re-label after the merge.
3. **Mutant ownership**: the mutant file is `R91MMutC1`'s; if it freezes before these cases, the
   kill predicate cannot include them. Route early.
4. **Duplicate blind/fuzz coverage**: the fuzz seat's vocabulary may already include `NoDisplay`/
   `OnlyShowIn`; duplicates are harmless but inflate N. Dedupe by id at the freeze.
5. **Oracle label cost**: three cases × one type each; negligible.

### Verification (all DRAFT; no receipt)

```
python3 -I controls/mime-oracle-r91.py --cases <new.json> --scratch-root "$S" --label <labelled.json>
# expect: MIME_ORACLE: cases=3 types=3 gio_sha256=d2164260… libgio_sha256=b38001cc… changed=3
# and the probe outputs above; gio is invoked only as `/usr/bin/gio mime TYPE`
python3 -I quality/counters/c1-r91-mime-resolution.py --repo <lane> --rev <frozen-rev> \
  --base-rev cc0381db… --cases <merged-labelled.json> --mutants <scratch-mutants.json> \
  --oracle controls/mime-oracle-r91.py --fuzz-gen controls/fuzz-gen-r91.py \
  --expect-cases-sha256 <sha> --expect-mutants-sha256 <sha> --expect-oracle-sha256 <sha> \
  --expect-gio-sha256 d216… --expect-libgio-sha256 b380… --expect-fuzz-sha256 <sha> \
  --scratch-root "$S" --draft-tool build/mado-mime.c1.py   # DRAFT_* only, never a measurement
# expect: candidate correct on all three; a scratch mutants file with M-ND/M-SI/M-RA/M-HC
#         kills each against its case and not against the old 89
```

At the freeze, re-run the oracle label, record the new case-file sha256, and let the frozen counter
include the cases in N. The move stops here; no second proposal.

## 5. Command log (what was run, and the result)

| # | command (read-only unless noted) | result |
|---|---|---|
| 1 | `git -C <lane> rev-parse HEAD` | `cc0381db585cc44c3dfc13ced807409c32c45bb0`, rc 0 |
| 2 | `git -C <lane> diff --stat cc0381db -- corpus/SOURCES.md`; `git status --porcelain -- corpus/SOURCES.md` | empty, rc 0 (registry identical to base) |
| 3 | grep tool: five primary terms over sibling `corpus/knowledge`, `tools`, `SKILL.md` | no primary-term match; the whole-lane exact-token pass hit only souji's census (row 4) |
| 4 | grep tool: exact tokens `mimeapps\|xdg-mime\|gdesktopappinfo\|mimeinfo.cache` over each lane root | only souji's census `arch-gio.1` files; no tool/knowledge owner |
| 5 | grep tool: `mime\|xdg-open\|mimeapps\|default app` in mado `PROVINCE.md`, `SKILL.md`, `corpus/` | no matches in `PROVINCE.md`/`SKILL.md`/`corpus` |
| 6 | `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' … \| grep -oE 'S[0-9]+' \| sort` on both registries; `comm -12` | rc 0; `reg=438 staged=147 collisions=94`; hashes in §2 |
| 7 | guard fixture `  \| S002 \|` with the same extractor vs column-zero-only extractor | indented=1, column-zero=0; old grep rc 1 (expected no match), driver rc 0 |
| 8 | `python3 -I controls/gen-c1-cases-r91.py` (stdout only) | rc 0; 89 cases; ids identical to the 89-case file at read time |
| 9 | oracle probes via Python `subprocess` with a fully specified env (no inherited vars), `/usr/bin/gio mime text/plain` | gio rc 0 for 11 + 6 probes; outputs in §4 (one fixture transiently in the default temp dir, removed; §5(d)) |
| 10 | scratch cleanup `rm -rf -- "$S"` + `test ! -e "$S"` | rc 0; removed |

Dead steps / tool notes (not blockers): (a) the first collision+guard driver exited 1 under
`set -euo pipefail` because the *expected* column-zero no-match grep returned 1; rerun with explicit
rc handling, check itself unchanged. (b) The `read` JSON query on `w1-spec.json` failed with
“cannot use null as iterable” because the record's key is `items`, not `seats`; used Python to read
the same file. (c) `CORPUS.md` is at the fleet root, not the lane root; the failed lane read was
followed by `/home/vgpnk/Projects/shokunin/CORPUS.md`. (d) **Seat-process defect:** the first oracle
probe called `tempfile.mkdtemp` with `dir=None` because the preceding guard trap had removed S, so
its fixture lived under the default temp dir for the probe's lifetime and was removed by the probe's
own `shutil.rmtree`; a follow-up `ls -d /tmp/ndprobe-* /tmp/hiddenprobe-*` printed `none`, and S is
absent. The probe should have re-created S first; the later Hidden probe did exactly that. No
install, no upgrade, no pacman.

## Appendix A — id lists (exact, from the artifact files)

**staged-ids (147, S203–S349):**
`S203,S204,S205,S206,S207,S208,S209,S210,S211,S212,S213,S214,S215,S216,S217,S218,S219,S220,S221,S222,S223,S224,S225,S226,S227,S228,S229,S230,S231,S232,S233,S234,S235,S236,S237,S238,S239,S240,S241,S242,S243,S244,S245,S246,S247,S248,S249,S250,S251,S252,S253,S254,S255,S256,S257,S258,S259,S260,S261,S262,S263,S264,S265,S266,S267,S268,S269,S270,S271,S272,S273,S274,S275,S276,S277,S278,S279,S280,S281,S282,S283,S284,S285,S286,S287,S288,S289,S290,S291,S292,S293,S294,S295,S296,S297,S298,S299,S300,S301,S302,S303,S304,S305,S306,S307,S308,S309,S310,S311,S312,S313,S314,S315,S316,S317,S318,S319,S320,S321,S322,S323,S324,S325,S326,S327,S328,S329,S330,S331,S332,S333,S334,S335,S336,S337,S338,S339,S340,S341,S342,S343,S344,S345,S346,S347,S348,S349`

**collisions (94):**
`S203,S204,S205,S206,S207,S208,S209,S210,S211,S212,S213,S214,S215,S216,S217,S218,S219,S220,S221,S253,S258,S277,S278,S279,S280,S281,S282,S283,S284,S285,S286,S287,S288,S289,S290,S291,S292,S293,S294,S295,S296,S297,S298,S299,S300,S301,S302,S303,S304,S305,S306,S307,S308,S309,S310,S311,S312,S313,S314,S315,S316,S317,S318,S319,S320,S321,S322,S323,S324,S325,S326,S327,S328,S329,S330,S331,S332,S333,S334,S335,S336,S337,S338,S339,S340,S341,S342,S343,S344,S345,S346,S347,S348,S349`

**reg-ids (438, S001–S503 minus these 65 gaps):**
`S190,S191,S192,S193,S194,S195,S197,S198,S199,S200,S222,S223,S224,S225,S226,S227,S228,S229,S230,S231,S232,S233,S234,S235,S236,S237,S238,S239,S240,S241,S242,S243,S244,S245,S246,S247,S248,S249,S250,S251,S252,S254,S255,S256,S257,S259,S260,S261,S262,S263,S264,S265,S266,S267,S268,S269,S270,S271,S272,S273,S274,S275,S276,S468,S469`
(Full sorted list and sha256 are in `assimilation/reg-ids`; the two other files are alongside.)
