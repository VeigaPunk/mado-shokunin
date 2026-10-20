# RubricBaselineScout — independent rubric-V baseline at `27cd06f`

Scope: recompute the pre-registered rubric V (C2 coverage) at baseline
`27cd06f5067c3d3540ab9aa7cc734eb8eee162cc` using only `git show`/`git grep`
over the lane repo. `measure.py` was **not** read or run. No host operation,
package query, service call, compositor/input probe, or tool install; no file
outside this report was written. No siblings messaged; no delegation.

Pre-registration read from `0175f13d83dceb9344fd0ecc5f94aa4aac5dfb53`
(`SCORECARD.md` §"Round 17 — declared claims", l.842–852 at that revision).
The same commit's `PROVINCE.md` is byte-identical to baseline (`git diff
27cd06f 0175f13 -- PROVINCE.md` empty); the P1–P6 labels exist only in the
SCORECARD pre-registration text.

## Rubric V as pre-registered (quoted, l.842–852)

- Surfaces: `P1` Hyprland config tree, `P2` Waybar, `P3` Walker, `P4`
  terminal-emulator configs, `P5` themes/wallpapers, `P6` screen/idle
  (hypridle/hyprlock).
- Covered = an admitted `corpus/knowledge/` entry whose **first 15 lines**
  carry `source:` citing a **`mined` tier-A** `SOURCES.md` row whose
  **`used-by` names that entry**, and the entry declares the surface either
  by `surface: P<n>` (new entries) or by the fixed legacy map
  `covers: U1|U2 → P1`, `covers: U7 → P2` — "declared now, never widened in
  this round".
- Declared baseline `2/6 = 3.3333`; target `4/6` (P6 idle/lock, P4 terminal).

## Method (mechanical join; reproducible)

```sh
# 1. first 15 lines per entry: source:/covers:/surface:
git show 27cd06f:corpus/knowledge/<entry>.md | sed -n '1,15p' \
  | grep -E '^(source|covers|surface):'
# 2. SOURCES row join: tier=$5 status=$9 used-by=$12 (11-column table)
git show 27cd06f:corpus/SOURCES.md | grep -E '^\| *S[0-9]{3}'
# 3. membership test: does used-by contain the entry path?
```

## Observed facts

Inventory at baseline: **30** `corpus/knowledge/*.md` entries, all 30 also
present in the `corpus/README.md` navigation table (the repo's only
admission map: "navigation map of admitted evidence"). `SOURCES.md` has 55
rows; 43 are `mined`, all 43 tier A (no mined B/C row exists to confuse the
join).

First-15-line metadata defficiencies (exact):

| entry | source: line | S tokens | tier/status/used-by result | covers: | surface: |
|---|---|---|---|---|---|
| window-rule-effects-getprop.md | 3 | S002,S016,S017,S018,S019,S020 | all A/mined, used-by names entry | l.6 `U1` | — |
| hyprland-config-era-r12.md | 3 | S021…S030 (10) | S021–S029 A/mined, used-by names entry; **S030 A/rejected, used-by `—`** | l.6 `U2` | — |
| xdg-portal-routing-r12.md | 3 | S031–S035,S037 | all A/mined, used-by names entry | l.6 `U3` | — |
| wayland-protocol-boundaries-r13.md | 1 | S005,S040,S041,S042,S043,S046 | all A/mined, used-by names entry | l.4 `U4` | — |
| output-colour-boundaries-r14.md | 1 | S041,S047,S048,S050 | all A/mined, used-by names entry | l.4 `U5` | — |
| input-debugging-boundaries-r15.md | 1 | S051,S052 | both A/mined, used-by names entry | l.4 `U6` | — |
| waybar-observation-boundaries-r16.md | 1 | S053,S054 | both A/mined, used-by names entry | l.4 `U7` | — |
| config-drift-r12.md | 3 | S013,S014,S015 | all A/mined, used-by names entry | **none** | — |

The other 22 entries fail the source leg outright: 3 carry a prose `source:`
line with **no `S###` token** (`arc-synthesis.md:3`, `closeout-r11.md:3`,
`gate-standing-use.md:3`) and 19 carry no `source:` line in their first 15
lines. `surface:` appears **nowhere** in `corpus/knowledge/` at baseline
(`git grep -n '^surface:' 27cd06f -- corpus/knowledge` → no rows); the only
`surface:`-like token in the tree is prose in `.ufo/waves/*` reports.

## Result — baseline confirmed 2/6

| surface | covered by | via |
|---|---|---|
| P1 Hyprland config tree | `window-rule-effects-getprop.md` **and** `hyprland-config-era-r12.md` | `covers: U1` → P1; `covers: U2` → P1 |
| P2 Waybar | `waybar-observation-boundaries-r16.md` | `covers: U7` → P2 |
| P3 Walker | **none** | U-mapped entries are U1–U7; only U1/U2/U7 are in the legacy map |
| P4 terminal-emulator | **none** | no `surface: P4`; no terminal entry with a qualifying `source:` |
| P5 themes/wallpapers | **none** | no `surface: P5`; `theme-wallpaper-plane.md` has no `source:` |
| P6 screen/idle | **none** | no `surface: P6`; `idle-lock-plane.md` has no `source:` |

**Covered = {P1, P2} = 2/6 = 0.3333 = 3.3333/10**, matching the declared
baseline exactly. P1 has two independent qualifying entries, so the count is
robust to the S030 caveat: under a stricter "every cited row must qualify"
reading the U2 entry would fail, but P1 still counts through U1. P2 rests
solely on the r16 entry via U7.

Reading note (recorded because it affects the count): `covers: U1|U2 → P1`
must be read as alternation. Read as the literal token `U1|U2`, no entry
would map to P1 and the baseline would be 1/6 — contradicting the declared
2/6; the alternation reading is the only one internally consistent with the
pre-registration.

## Entries that could be *argued* to cover P3–P6 (gaming risk)

Under the literal rubric, **no** baseline entry covers P3–P6. Every
subject-matching note fails the source leg completely:

| candidate | subject surface | first-15 `source:` S-token | `surface:`/`covers:` | literal verdict |
|---|---|---|---|---|
| `terminals-and-omarchy.md` | P4 (four terminal trees measured by bytes) | 0 (no `source:` line at all) | 0 / 0 | fails |
| `idle-lock-plane.md` | P6 (names PROVINCE screen/idle, hypridle/hyprlock) | 0 | 0 / 0 | fails |
| `waybar-walker-plane.md` | P2 + P3 + P6 (title names waybar/walker/mako/swayosd/hypridle/hyprlock) | 0 | 0 / 0 | fails |
| `walker-deep.md`, `walker-deep-r9.md`, `walker-live-surface.md`, `waybar-walker-semantics.md` | P3 | 0 | 0 / 0 | fail |
| `theme-wallpaper-plane.md` | P5 | 0 | 0 / 0 | fails |
| `remaining-planes-census.md` | P5 + P6 ("themes/wallpapers as declared files", "display/session shape") | 0 | 0 / 0 | fails |
| `province-accuracy-selfaudit.md` | would name every PROVINCE surface | 0 | 0 / 0 | fails |
| `arc-synthesis.md` | U1–U7 gap inventory | prose `source:`, 0 `S###` | 0 / 0 | fails |

These are the plausible "the surface is obviously already documented" claims;
none satisfies the pre-registered predicate. Counting any of them would be
gaming. Note the rubric rewards a *sourced declaration*, not host-byte
measurement — the strongest measured notes (terminals, idle) intentionally do
not count.

Residual gaming vectors inside the rubric wording itself (for L1/reviewers,
not an accusation):

1. **Relabel-only.** Any of the 8 already-qualifying entries could gain a
   `surface: P<n>` line with no new source work; the rubric never joins the
   surface token to the cited row's subject/anchor. A single false line on
   `config-drift-r12.md` (P1/P2 subject) or `hyprland-config-era-r12.md`
   would add an uncovered surface at 2/6→3/6. Content coherence of
   `surface:` is the only defence and it is human review.
2. **Multi-surface declaration.** The rubric counts surfaces, not entries and
   sets no cap; one new note declaring `surface: P4` and `surface: P6` (or a
   combined line) reaches 4/6 with one note rather than two. That may be
   legitimate (surfaces are the unit) but departs from C2's target wording
   ("P6 idle/lock, P4 terminal" from "sources opened this round").
3. **Pre-existing SOURCES row.** The predicate only requires `mined` tier-A;
   it does not require a round-17 row. A new P4 note could cite an existing
   row (e.g., S029/S041) plus a `used-by` append (allowed in place with a
   lesson log) and pass the join without opening a new source, contradicting
   C2's "sources opened this round". The join cannot distinguish this;
   only anchor/quote review can.
4. **`covers:` retro-fit.** Low yield: the map is fixed and "never widened",
   so newly invented `covers: U8+` values must not count, and `covers: U1`
   only re-covers P1. A seat editing `covers:` to U7 would still need the
   source leg and Waybar-relevant content.
5. **Prose `source:` look-alikes.** `arc-synthesis`/`closeout-r11`/
   `gate-standing-use` show a `source:` line but no `S###`; counting them is
   a likely false positive. Likewise a `source:` placed after line 15, or a
   `surface:` after line 15, must not count.

## Limits / remaining unknowns

- I did not cross-check `measure.py` by instruction; if the round's
  implementation joins citations differently (e.g., requires *all* cited rows
  to qualify, or accepts `covers:` values outside the declared map), its
  number can legitimately differ from mine. My result is the literal reading
  above and matches the declared 2/6.
- "Admitted" has no machine-readable marker at baseline; all 30 entries sit
  in the README table, so admission was treated as "present in
  `corpus/knowledge/` + README row", which all pass.
- No host fact about P3–P6 behaviour was observed or asserted here; this is a
  documentary-count computation only.
- Confidence: **high** on the 2/6 count and the per-entry join (mechanical,
  revision-pinned); **medium** on the gaming-risk catalogue (wording
  interpretation).

No tools were installed or updated.
