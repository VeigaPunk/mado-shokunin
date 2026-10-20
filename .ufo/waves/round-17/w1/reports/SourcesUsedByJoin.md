# SourcesUsedByJoin — reciprocal joins for the P4/P6 route notes (round 17, W1)

Seat `MadoR17.SourcesUsedByJoin`, leaf, report-only. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline `27cd06f`. Date 2026-10-20.

Deliverable: for every source the two new notes cite, the exact `used-by` cell and the
exact note line/token it must occupy, plus the duplicate-URL check against S001–S055.
Nothing in the lane was edited except this report. No commit, no `git`/`jj` mutation,
no delegation, no host command (no pacman/sudo/systemctl/hyprctl/omarchy-*/hypridle/
hyprlock/alacritty/xdg-terminal-exec), no tool installed or upgraded; all remote reads
previously made by the scout/note seats were used as recorded, and the only execution was
my own stdlib checker on `/tmp` inputs (§7).

Inputs read: `corpus/SOURCES.md` (S001–S055), `corpus/knowledge/terminal-route-r17.md`,
`corpus/knowledge/idle-lock-route-r17.md`, `.ufo/waves/round-17/drafts/NoteTerminal-rows.md`,
`.ufo/waves/round-17/drafts/NoteIdle-rows.md`, `.ufo/waves/round-16/measure.py`,
`scripts/sources-census.sh`, `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, the landed P4/P6
scout reports, and `SCORECARD.md` § "Round 17 — declared claims".

## 1. What the join is, mechanically (not prose)

The reciprocal join is enforced in both directions by the lane's own counter
(`.ufo/waves/round-16/measure.py`), and the registry's own validator
(`scripts/sources-census.sh`). The rules that decide pass/fail:

| Rule | Implemented at | Consequence for this round |
|---|---|---|
| header = first 15 lines; exactly one `^source:` line; `verified-at:` and `recheck:` non-empty; one `^surface: P<n>$` | `measure.py:222-227`; round-17 rubric in `SCORECARD.md` C2 | both notes already comply (lines 1–4, §3/§4) |
| cited ids = `\bS\d{3,}\b` on that line; a row counts only if `status=mined`, `tier` A/B, `used-by` names the note | `measure.py:232-234`; `used_by()` at `:82-83` | a cited id must resolve to a mined tier-A row whose used-by cell is exactly the note path |
| **inverse**: every mined row whose `used-by` names the note must be cited on that same line | `measure.py:250-256` (U5), `:263-270` (U6), `:282-290` (U7) — same rule reused for V | the used-by-cell ↔ note-line relation is a **bijection** over mined rows; an orphan cell fails C2 |
| used-by cell is split on `,` only, exact string match | `measure.py:83`; census E11 split at `sources-census.sh:563-568` | one path per cell here; no backticks, parentheses or semicolons inside it |
| E11: every used-by path must exist on disk relative to the lane root | `sources-census.sh:566-568` | the note files must exist in the same validated tree (they do, §3/§4) |
| E05 kind enum `spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work` | census `validate` E05; contract § Shape | `kind=config` is a hard error (found, §6/D1) |
| URL identity: strip `#fragment`, strip trailing `/`, strip scheme, lowercase host only | `sources-census.sh:600-607` | duplicate test below uses exactly this normalisation |
| E04 same URL+scope (error); W04 same URL across scopes (warning) | `sources-census.sh:644-649` | no proposed row repeats an existing URL |

Contract Rule 1 also binds every new row: "Write it only after opening the source in the
round that writes the row", with a gate quote per new row in the round lesson's `## Gate`
(`SOURCES-CONTRACT-v1.md`, § Rules 1). That rule is why §6/D2 flags the two snippet-only
rows.

## 2. Baseline: no existing row covers these surfaces; no URL collision

Measured on `corpus/SOURCES.md` at `27cd06f` (55 rows, 39 unique normalised URLs):

- Term scan of the `source`, `scope`, `anchor`, `teaches` cells for
  `hypridle`, `hyprlock`, `alacritty`, `xdg-terminal`, `xdg-terminals`, `login1`,
  `session-lock` → **0 hits each**. The only `terminal` hit is **S020**
  (`omarchy/default/hypr/apps/terminals.conf`), whose scope is *window-rule opacity for
  terminals*, not the P4 launch/config route; it is not a P4 source and is not cited.
- The three pre-existing W04 lines are unchanged and unrelated
  (`S030` and `S045` on `wiki.hypr.land/Configuring/Basics/Window-Rules`, `S042` on
  `wayland.freedesktop.org/extras.html`; the baseline receipt is
  `.ufo/waves/round-17/evidence/census-start.txt`, exit 0).
- Normalised URL sweep of all 10 proposed URLs that carry a scheme against the 39
  existing normalised URLs, and against each other: **0 collisions**. The two rejected
  P4 source cells currently omit `https://`, so the census parser extracts no URL from
  them; with `https://` prefixed they are also clean (`manpages.ubuntu.com/...`,
  `github.com/Vladimir-csp/xdg-terminal-exec/blob/master/README.md`).

Candidate sweep result (`joincheck.py`, §7): `URL collisions: none ; unique proposed
urls 10`.

## 3. P4 join — `corpus/knowledge/terminal-route-r17.md`

Header is already in rubric shape: line 1 `source:`, line 2 `verified-at:`, line 3
`recheck:`, line 4 `surface: P4`; the note file exists, so E11 passes once rows name it.
It cites five sources, each with a matching mined tier-A row in
`drafts/NoteTerminal-rows.md`:

| id | source (pin) | note line | used-by cell (exact) | status/tier |
|---|---|---|---|---|
| S056 | xdg-terminal-exec v0.14.3 README | line 1, token 1 | `corpus/knowledge/terminal-route-r17.md` | mined / A |
| S057 | xdg-terminal-exec v0.14.3 script | line 1, token 2 | `corpus/knowledge/terminal-route-r17.md` | mined / A |
| S058 | Alacritty v0.17.0 `extra/man/alacritty.5.scd` | line 1, token 3 | `corpus/knowledge/terminal-route-r17.md` | mined / A |
| S059 | host declarations (`bindings.conf:2-3`, `xdg-terminals.list:3`, `alacritty.toml:1`) | line 1, token 4 | `corpus/knowledge/terminal-route-r17.md` | mined / A |
| S060 | host system list `/usr/share/xdg-terminal-exec/xdg-terminals.list` | line 1, token 5 | `corpus/knowledge/terminal-route-r17.md` | mined / A |
| S061 | Ubuntu manpage xdg-terminal-exec (rejected candidate) | — not cited | `—` (must stay `—`) | rejected / C |
| S062 | GitHub `master` blob (rejected candidate) | — not cited | `—` (must stay `—`) | rejected / C |

Exact replacement for note line 1 (only the five `-pending` suffixes removed):

```text
source: S056 (xdg-terminal-exec v0.14.3 README.md:55-57,100-101,115-118,131,153-166,264; S057 xdg-terminal-exec:106,148-162,919,1252; S058 alacritty v0.17.0 extra/man/alacritty.5.scd:27-41,57-61; S059 host ~/.config/hypr/bindings.conf:2-3, ~/.config/xdg-terminals.list:3, ~/.config/alacritty/alacritty.toml:1; S060 /usr/share/xdg-terminal-exec/xdg-terminals.list:1-25)
```

Reciprocal check (simulated after that edit): cited `{S056..S060}` = rows naming the note
`{S056..S060}`; `missing_row_for_cited=[]`, `uncited_row_naming=[]`. Rejected rows name
no note and are not cited, so they do not enter the bijection.

## 4. P6 join — `corpus/knowledge/idle-lock-route-r17.md`

Header shape is the same: line 1 `source:` (seven citations), line 2 `verified-at:`,
line 3 `recheck:`, line 4 `surface: P6`; the note file exists. `drafts/NoteIdle-rows.md`
drafts exactly seven mined tier-A rows, in the same order as the citation line, all with
`used-by = corpus/knowledge/idle-lock-route-r17.md`:

| id | source (pin) | note line | used-by cell (exact) | status/tier |
|---|---|---|---|---|
| S063 | Hypr wiki hypridle page (`Latest git`, modified 2026-08-26; HTML sha256 `b45c03dc…`) | line 1, token 1 | `corpus/knowledge/idle-lock-route-r17.md` | mined / A |
| S064 | Hypr wiki hyprlock page (`Latest git`, modified 2026-08-26; HTML sha256 `f69cff6b…`) | line 1, token 2 | `corpus/knowledge/idle-lock-route-r17.md` | mined / A |
| S065 | hypridle v0.1.8 README (`f5b852ee…`, 2598 B) | line 1, token 3 | `corpus/knowledge/idle-lock-route-r17.md` | mined / A |
| S066 | hypridle v0.1.8 `src/core/Hypridle.cpp` (`2dd4d73d…`, 29880 B) | line 1, token 4 | `corpus/knowledge/idle-lock-route-r17.md` | mined / A |
| S067 | hypridle v0.1.8 `src/core/Hypridle.hpp` (`f9e4e558…`, 3611 B) | line 1, token 5 | `corpus/knowledge/idle-lock-route-r17.md` | mined / A |
| S068 | hypridle v0.1.8 `src/main.cpp` (`379bf321…`) | line 1, token 6 | `corpus/knowledge/idle-lock-route-r17.md` | mined / A |
| S069 | hyprlock v0.9.6 README (`83096def…`, 1458 B) | line 1, token 7 | `corpus/knowledge/idle-lock-route-r17.md` | mined / A |

Exact replacement for note line 1 (all seven positional `S0xx-pending` tokens replaced in
order):

```text
source: S063 https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ (Configuration, General, Listeners, Examples); S064 https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ (Warning, Command-line Arguments, Configuration, General, Authentication, System Configuration); S065 https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md (Features, Configuration); S066 https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp (setupDBUS, handleDbusSleep, dbus Lock/Unlock, onIdled, onResumed, onInhibit, onLocked, config load); S067 https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.hpp (SIdleListener); S068 https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp (config lookup); S069 https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md (Features, Docs)
```

Reciprocal check (simulated): cited `{S063..S069}` = naming `{S063..S069}`;
`missing_row_for_cited=[]`, `uncited_row_naming=[]`, 0 residual `S0xx-pending` tokens.
No existing S001–S055 row names either note, so the inverse rule adds nothing on top of
the seven new rows.

## 5. Id allocation and budget

| Block | Rows | Ids | Consumes |
|---|---|---|---|
| P4 | 5 mined + 2 rejected | S056–S062 | 7 |
| P6 | 7 mined | S063–S069 | 7 |
| total | 14 | S056–S069 | **exactly the reserved 14** |

The reserve has **zero slack**. If the P4 rejected rows are dropped instead of opened
(§6/D2), the clean shift is P4 = S056–S060 and P6 = S061–S067, leaving S068–S069 unused —
do not leave an interior gap, and renumber only before any row is written.
Rows outside the two notes' citation lines — `SrcLogindLock`'s two opened logind/systemd
sources, `SrcIdleNotifyProto`'s XML, `SrcHyprlockLockProto`'s XML, `SrcAlacrittyChangelog`'s
CHANGELOG, any `SrcTerminalAlternates` rejects — would need **S070+** with an explicit
lesson note. If any of them is registered as `mined` with `used-by` naming a note, the note
must cite it or the inverse check fails; registering them as `queued` with `used-by = —`
keeps C2 unaffected.

## 6. Defects found (ordered by severity)

**D1 — hard census error: `kind=config` (P4 rows).** `drafts/NoteTerminal-rows.md` lines
15–16 (S059, S060) carry `kind = config`, which is outside the contract enum; the census
validator emits `E05` for each (§1). Fixed to `code` (precedent: S020, host config files),
the same draft validates with no findings. Apply the fix before integration.

**D2 — contract Rule 1: rejected rows were not opened.** S061/S062 are described in the
draft as "search snippet only, not opened", while contract Rule 1 requires a row to be
written "only after opening the source in the round that writes the row". Both URLs
return HTTP 200 today (`manpages.ubuntu.com/.../xdg-terminal-exec.1.html`,
`github.com/Vladimir-csp/xdg-terminal-exec/blob/master/README.md`, checked 2026-10-20), so
L1 can open them and record a gate line, or drop the rows and use the shift in §5. A
snippet-only row is not made valid by its `rejected` status.

**D3 — P6 line 1 cannot be string-replaced.** It contains the *identical* literal
`S0xx-pending` seven times (`grep -c` = 7), so `s.replace('S0xx-pending','S063')` would
collapse all seven citations to one id and the note would fail the reciprocal check.
Rewrite line 1 wholesale with the block in §4. P4's placeholders are distinct
(`S056-pending`…`S060-pending`), so suffix removal is safe there.

**D4 — zero id slack.** Any additional row (D2 alternative, logind/XML/changelog/alternate
sources) must be allocated S070+ explicitly. Silently reusing S068/S069 for something else
would break both notes' positional mapping.

**D5 — P6 `recheck:` counts are wrong.** Line 3 says "the two wiki URLs and the four
tag-pinned raw URLs" but line 1 cites five raw URLs (hypridle README, `Hypridle.cpp`,
`Hypridle.hpp`, `main.cpp`, hyprlock README); it also says "six files in § Host
declaration" while that table has seven rows. Fix both counts while rewriting line 1–3.
(These are quality defects; the rubric only requires `recheck:` non-empty.)

**D6 — integration ordering.** Both notes now exist, but neither is in `corpus/README.md`
(`grep -c r17 corpus/README.md` = 0) and no row names them yet (`grep -c r17
corpus/SOURCES.md` = 0). The note rows, the 14 registry rows and the README index/coverage
rows should land in the same integration commit: E11 reads the used-by paths from disk, and
the navigation count moves 30 → 32 when the two index rows land.

**D7 — allocation ambiguity in the drafts.** `NoteTerminal-rows.md` starts at S056 and
`NoteIdle-rows.md` says "L1 assigns S056-S069", so both drafts nominally claim the whole
range. The binding split is §5 (P4 first). Keep each file's mapping explicit; never apply
a cross-file id replacement.

## 7. Verification performed

Own stdlib checker at `/tmp/r17join/joincheck.py` (`python3 -I`, no third-party imports,
reads the lane read-only; scratch is outside the lane). It re-implements the census
row/URL checks (`E02/E03/E04/E05/E06/E07/E08/E09/E11/W01/W04`) and the measure header +
reciprocal logic, then simulates the two line-1 rewrites. Outputs:

```text
registry rows 55 ids S001 .. S055
P4 drafted-row findings: [('E05','S059','kind=config'), ('E05','S060','kind=config')]
P4 fixed-kind findings: none
P4 header: source_lines=1 surface=['P4'] verified=True recheck=True cited=S056..S060 dup=[] unknown=[]
P4 reciprocal: cited=S056..S060 naming=S056..S060 missing=[] uncited=[]
P6 before rewrite header ids: []            # identical S0xx placeholder yields no id
P6 draft-row findings: none
P6 reciprocal (draft rows): cited=S063..S069 naming=S063..S069 missing=[] uncited=[]
P6 residual S0xx token: 0
URL collisions: none ; unique proposed urls 10
```

Not run (lane rule: seats do not run gates/tests): `sources-census.sh validate`, the round-17
`measure.py`, the legacy gate, and any live/no-live host run. After integration L1 should run
once: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` (expect exit 0 plus only the three historical W04
lines) and `python3 .ufo/waves/round-17/measure.py REV` (expect C2 = 4/6 with both notes
counted). Expected row moments: P4 5 mined + 2 rejected, P6 7 mined, cited == naming.

## 8. Residual unknowns / limits

- The hyprlock-wiki HTML digest (`f69cff6b…`) and `main.cpp` digest (`379bf321…`) come from
  a single fetch in `drafts/NoteIdle-rows.md`; no scout independently reproduced those two
  (the other five digests match their scout reports). Treat them as recorded, not
  cross-verified.
- `SrcTerminalAlternates` had not landed when this was written; any rejected/queued rows it
  proposes fall outside S056–S069 (§5).
- Every row is tag- or page-pinned documentary evidence. None supports a host binary
  version or observed behaviour; both notes already say so, and the rows' `teaches` cells
  must not be read as host facts.
- The `source:` line must stay inside the first 15 lines after any header edit; moving it
  below line 15 silently drops the note from C2 regardless of the used-by join.
