# ReMeasureC2 — independent re-derivation of rubric V at 988b858

Lane: MadoR17.ReMeasureC2 (round-17 wave 2, falsify). Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Revision bound:
`988b858bd6049bc709807534fd725c05264f7e60`.

## Verdict

**My count: 4/6 — P1, P2, P4, P6 — score 6.6667. It agrees with
`measure.py 988b858…` exactly; there is no disagreement to report.**
Baseline re-derived independently: **2/6, P1+P2, 3.3333** at `27cd06f`.
The round-17 target (4/6) is met under the declared rule, by exactly the two
named surfaces (P4 terminal, P6 idle/lock).

**The count attack failed.** I could not move 4/6 down: the two new entries
cite real bytes (every upstream and host digest reproduced), they are not
hollow shells, the baseline is honest, the criterion was pre-registered before
the instrument and the entries, and nothing in the measured corpus was edited
after the C2 commit.

Two things the number does **not** establish, with concrete counterexamples
below: (F1) the rubric is procedurally gameable — a fabricated entry plus a
fabricated registry row scores 5/6 with `rejected: []`; (F2) 4/6 means "4 of 6
surfaces have ≥1 sourced *declaring* entry", not "4 surfaces are covered".

## Method (no measure.py in the derivation)

Rules taken only from `SCORECARD.md:842-853` (C2 bullet) and the
pre-measurement corrections block `SCORECARD.md:867-895`. I wrote an
independent checker, `/tmp/r17c2_indep.py`, which reads committed blobs
(`git show REV:path`, `git ls-tree`) and implements from the declaration text:
first-15-lines `source:` tokens → `corpus/SOURCES.md` row with `status=mined`,
`tier=A`, `used-by` naming the entry; `surface: P<n>` exact form **or** the
fixed legacy map `U1|U2→P1`, `U7→P2` pinned to the three baseline holders;
four required `## ` headings, ≥3 non-blank lines each, `[UNK]` inside
`## Unexercised behavior`; ≥1 cited mined tier-A row that is an upstream
`https://` source of kind docs/spec/code naming the surface. It does not import
or copy `measure.py`.

```
python3 /tmp/r17c2_indep.py 988b858bd6049bc709807534fd725c05264f7e60
  INDEPENDENT COUNT 4/6 = 6.6667   P1 P2 P4 P6 covered; P3, P5 uncovered; REJECTED: none
python3 /tmp/r17c2_indep.py 27cd06f
  INDEPENDENT COUNT 2/6 = 3.3333   P1 P2 covered; P3 P4 P5 P6 uncovered
python3 .ufo/waves/round-17/measure.py 988b858bd6049bc709807534fd725c05264f7e60
  c2 count 4, score 6.6667, provinces P1 P2 P4 P6, rejected []
```

### Per-province derivation

| Prov | Declaring entry (anchor) | Head `source:` join (all mined/A, `used-by` names the entry) | Upstream row naming surface |
|---|---|---|---|
| P1 | `corpus/knowledge/hyprland-config-era-r12.md:6` `covers: U2` | S021–S029 (`SOURCES.md` rows 33-41) | S021 `https://hypr.land/news/update53/` (docs) |
| P1 | `corpus/knowledge/window-rule-effects-getprop.md:6` `covers: U1` | S002 (`SOURCES.md:14`), S016–S020 (`:28-32`) | S016 `https://wiki.hypr.land/…/Using-hyprctl/`, S018 tagged HyprCtl.cpp (code) |
| P2 | `corpus/knowledge/waybar-observation-boundaries-r16.md:4` `covers: U7` | S053, S054 (`SOURCES.md:65-66`) | S053 `…/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd` |
| P4 | `corpus/knowledge/terminal-route-r17.md:4` `surface: P4` | S056–S060 (`SOURCES.md:68-72`) | S056/S057/S058 tagged xdg-terminal-exec + Alacritty (docs/code) |
| P6 | `corpus/knowledge/idle-lock-route-r17.md:4` `surface: P6` | S063–S069 (`SOURCES.md:75-81`) | S063/S064 hypridle/hyprlock wiki (docs), S066 Hypridle.cpp (code) |
| P3 | — none | — | — |
| P5 | — none | — | — |

P3/P5 cannot be credited: `git grep '^surface:' 988b858 -- corpus/knowledge`
returns only `idle-lock-route-r17.md:4` and `terminal-route-r17.md:4`; the seven
`covers:` lines are identical at `27cd06f` and `988b858` (U1–U7), and the
declared map maps only U1/U2/U7. No widening occurred.

Content floors (non-blank lines per required section), both real:
terminal-route 39/25/9/21, idle-lock-route 25/34/6/11; both carry `[UNK]` in
`## Unexercised behavior` (terminal lines 110-128, idle lines 124-134). Both
entries are index-admitted (`corpus/README.md:42` idle, `:43` terminal).

## Integrity of the two new routes (the attack that should have been fatal)

I re-fetched the sources myself with `curl` and hashed them. **All ten
reproduce byte-exact** (SHA-256, and byte counts where the entry states them):

- S056 `README.md` `c7a1a8bb…9d40` 14762 B; S057 `xdg-terminal-exec`
  `89f2be9a…27ac` 44020 B; S058 `alacritty.5.scd` `e444fa45…4107` 28787 B;
  S065 hypridle `README.md` `f5b852ee…81f6`; S066 `Hypridle.cpp`
  `2dd4d73d…2d75`; S067 `Hypridle.hpp` `f9e4e558…a2b8`; S068 `main.cpp`
  `379bf321…2a38`; S069 hyprlock `README.md` `83096def…50f3`; S063 wiki HTML
  `b45c03dc…f640`; S064 wiki HTML `f69cff6b…abf5`.
- **All 16 host files named in the two `## Host declaration` sections hash to
  the claimed values**: `bindings.conf e574a1ed…`, `~/.config/xdg-terminals.list
  d035da57…`, `alacritty.toml 695301c8…`, theme `alacritty.toml 8c3d1457…`,
  system `xdg-terminals.list a2b5bf69…`, `Alacritty.desktop 713703ba…`,
  `alacritty.toml.bak… ea3e0fa0…`, `hypridle.conf e7d3b8dd…`,
  `hyprlock.conf b8d173dc…`, theme `hyprlock.conf 3ef010e7…`,
  `omarchy-system-lock c1dd3881…`, `omarchy-system-wake 09ad52b0…`,
  `omarchy-launch-screensaver ba783a3a…`, omarchy default `autostart.conf
  acb6a668…`, `~/.config/hypr/autostart.conf 5ace1701…`, `hyprland.conf
  ce7483f3…`.
- Quoted lines exist as quoted: `bindings.conf:2-3`; `xdg-terminals.list:3` =
  `Alacritty.desktop` with lines 1-2 comments; `alacritty.toml:1` =
  `general.import = [ … ]`; `hyprland.conf:4` sources the omarchy autostart;
  `~/.config/hypr/autostart.conf:1` is a comment (does not start hypridle);
  omarchy default `autostart.conf:1` = `exec-once = uwsm-app -- hypridle`;
  `hypridle.conf:2,3,4,11,14-19` match the quoted lock/before/after/screensaver/
  listener text; `hyprlock.conf:1` sources the theme file.
- Load-bearing Hypridle.cpp anchors verify verbatim: [HC:104-107] the
  `hyprland-lock-notify-v1` warning, [HC:473] `if (MEMBER == "Lock") {`,
  [HC:477-478] `spawn(*LOCKCMD)`, [HC:504]/[HC:509-510] sleep cmd,
  [HC:120]/[HC:128-129] `case 2: // auto` and `if (m_sWaylandState.lockNotifier)`.
- The wiki quotation is verbatim: `"3 makes your system wait until the session
  gets locked by a lock screen app."` appears in the fetched hypridle article;
  the unfetched-today marker `2026-08-26` is present.

## Baseline, pre-registration and order (no post-hoc fitting found)

- `27cd06f` has **no** `surface:` lines; seven `covers:` lines only
  (U1–U7); `used-by` for S002/S016–S020/S053/S054 already names the three
  entries at that revision (checked with `git show 27cd06f:corpus/SOURCES.md`).
  So 2/6 is a property of the baseline, not of round-17 registry edits.
- `27cd06f→0175f13` changes only `SCORECARD.md` + `census-start.txt`;
  `0175f13→f52f43f` adds only the instrument, `gen_w1.py`, and w1
  spec/dispatch/record. Corpus untouched — `evidence/measure-instrument.json`
  (rev `f52f43f`, loose instrument) measuring 2 is a clean baseline reading.
- The C2 bullet is **byte-identical** at `0175f13` and `988b858` (compared
  with `git show … | sed -n '/C2 coverage/,/C3 operability/p'`). The legacy
  map and the "target 4/6" were pre-registered before any entry existed.
- Instrument bytes: `f52f43f` `a280b3ab…d3508e` (loose) → `ab0bc9b`
  `4023124f…66466b` (tight) = `a9998d1` = `988b858` (`git diff ab0bc9b
  a9998d1 -- measure.py` empty). The loose→tight diff at `ab0bc9b` is
  **strictly additive narrowing** (LEGACY_PATHS pin, SURFACE_KEYWORDS,
  MALFORMED form, FACET_MIN_LINES, exact-surface form, keyword-qualified
  upstream); no clause was widened.
- `git diff a9998d1 988b858 -- corpus/SOURCES.md` and `-- corpus/knowledge/`
  are empty: the measured corpus was not edited after the C2 commit.
- `evidence/measure-c2.json` (rev `a9998d1`) has `c2` **equal** to the live
  HEAD `c2` (4, P1/P2/P4/P6, `rejected: []`); `measure-before.json` (27cd06f,
  tight) = 2; `measure-instrument.json` (f52f43f, loose) = 2.

## Findings by severity

### F1 — Medium: rubric V is procedurally gameable; concrete counterexample

`measure.py` verifies *claims about* sources, never sources. `:108` accepts any
13-cell registry row; `:242-247` tests the row's own `source`+`scope` strings
for a surface keyword; there is no fetch, no digest, no content binding, and
`corpus/README.md` admission is **never read** (`grep -n README measure.py` →
no match; `QUALITY` is read only for C1).

Counterexample, on a throwaway clone of `988b858` at `/tmp/r17attack` (lane
untouched): add `corpus/knowledge/fake-p5.md` (a `source:` line citing `S999`,
`surface: P5`, four headings with three filler lines each, `[UNK]` filler) and
append one fabricated row

```
| S999 | fabricated theme doc — https://example.invalid/theme-doc | docs | A | theme and wallpaper scope | none | none | mined | 2026-10-20 | never | corpus/knowledge/fake-p5.md |
```

Then `python3 .ufo/waves/round-17/measure.py HEAD` returns
`c2 5/6 = 8.3333, P1 P2 P4 P5 P6, rejected []`, with
`P5 entries [{'path': 'corpus/knowledge/fake-p5.md', 'reason': 'surface: P5',
'sources_ok': ['S999']}]`. No README row was added and none was needed.

Consequence: the "at least one cited mined tier-A row that is an upstream
https source … naming the surface" tightening does not bind to bytes. The
round-17 4/6 survives only because I verified the real rows' bytes by hand
(above). A future round can buy a surface for ~15 lines of filler.

### F2 — Low/medium: 4/6 is declaring-entry presence, not surface coverage

- P1 is credited by a window-rule effects note and a config-era note; the
  `~/.config/hypr/` tree inventory (`hyprland-config-plane.md`), keybind note
  and live layer carry no `covers:`/`surface:` and are not counted.
- P4's credit is Alacritty-only by the entry's own text
  (`terminal-route-r17.md:16`: "it covers Alacritty only, not foot, kitty or
  ghostty").
- P6's credit is documentary (no listener, lock or transition executed).
- The measured inventories already existed: `terminals-and-omarchy.md:10`
  ("All four terminal config trees exist"), `idle-lock-plane.md:3` (idle/lock
  depth note). So round 17 added **+2 sourced documentary routes**, not +2
  surfaces newly known. The declaration says "Documentary routes, not observed
  behaviour", so this is disclosed — but "2/6 → 4/6" should be read as a
  provenance gain, not a coverage gain.

### F3 — Low: wiki anchor line numbers are not mechanically reproducible

S063/S064 bind raw-HTML digests (both reproduce today), but `[HW:n]`/`[LW:n]`
are defined as "line n of the tag-stripped `<article>` text, one line per block
(table cells run together in the text)" (`idle-lock-route-r17.md:22-23`) with
no stripping command recorded. The facts I checked are verbatim; the *line
addresses* would need the original transformation re-invented. The tag-pinned
rows S065–S069 use plain file lines and are mechanically recheckable, so P6
does not depend on the wiki anchors alone.

### F4 — Informational: live-tree divergence during review (not the measured rev)

At 11:56:37–11:56:52 a concurrent lane modified the worktree
`corpus/SOURCES.md`, `corpus/README.md`,
`corpus/knowledge/terminal-route-r17.md`, `corpus/lessons/round-17.md`,
adding row **S071** (`Alacritty.desktop`, mined/A, `used-by`
terminal-route-r17.md) and citing it in the terminal head. At HEAD `988b858`
that row does not exist and the entry's head cites **S056–S060 only**
(`git show 988b858:corpus/knowledge/terminal-route-r17.md | sed -n '1p'`), so
the measured revision has no dangling citation. HEAD re-checked at the close of
this review: still `988b858`; the only commit-affecting changes are the four
worktree files above. If the edit lands, re-measure:
S071 can only add a `sources_ok` token to P4; the count stays 4/6. Two notes
for the owner of that edit: its `recheck:` line still says "corpus/SOURCES.md
S056-S060" while the head would cite S071, and the worktree now differs from
every revision-bound receipt in this wave.

### F5 — Informational: V's baseline is inherited by construction

V is a new axis declared this round with a 2/6 floor made of round-12 and
round-16 entries. The 3.3333→6.6667 move is therefore a renormalization on a
new denominator; the corrections block discloses V as the lowest active row but
not that its baseline costs nothing. Net round-17 contribution to V is
**+2/6**; state it that way in the wrap-up.

## Residual risk

- The 4/6 is correct **at `988b858`** and only under the declared rule; the
  corpus worktree is now ahead of that revision (F4), so any later reading of
  `corpus/` without a revision pin is not the measured artifact.
- Host declarations are true as of review time; they can drift, and the P6
  route remains declared-only by design (host pause).
- The rubric's gameability (F1) is a criterion-level risk that no amount of
  this round's execution can close.

## Verification gaps

- I did not fetch rejected rows S061/S062/S070 — they carry no credit.
- "Admitted" has no formal gate I could locate; I checked README index presence
  only (`corpus/README.md:42-43`), and the instrument checks neither.
- I did not parse desktop-entry semantics for `Alacritty.desktop`; I verified
  its digest and that its row text matches the file.
- I did not run the loose instrument from `f52f43f` against HEAD (its REPO
  anchor is `parents[3]`, so a `/tmp` copy cannot resolve the lane); the
  "stricter only" conclusion is from the full diff, which is additive.

## Hygiene

Installs: **none** (no pacman/yay/paru/uv/npm/cargo/sudo/systemctl/hyprctl or
live probe). Only this report was written in the lane; `/tmp/r17c2_indep.py`
and the `/tmp/r17attack` clone are scratch. Web sources were fetched with
`curl` and hashed; host config trees were read as file bytes only.
