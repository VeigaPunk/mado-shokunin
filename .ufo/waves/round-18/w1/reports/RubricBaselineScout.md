# RubricBaselineScout — independent rubric-V recomputation at `d9a5a18`

Scope: recompute rubric V (C2 coverage) at baseline
`d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` (detached git HEAD; lane is
jj-colocated and no git/jj write was issued) using `git show`, `git grep`,
`grep`, `awk` and `sha256sum` over the lane repo only. `measure.py` was
**not run**; the count below comes from my own join.

Disclosure: unlike the round-17 scout, I did read
`.ufo/waves/round-17/measure.py`'s C2 block at `d9a5a18` **before** running my
join, in order to enumerate the facets the instrument actually implements and
compare them with the declared rubric. I did not execute it, did not copy its
code, and did not read
`.ufo/waves/round-18/evidence/measure-before.json` until after my numbers were
fixed (it is used below only as a cross-check).

No host operation, no package query, no compositor/service/input probe, no
web fetch (so no fetch receipts). No tool installed or upgraded. No file
written outside this report.

## Rubric V as pre-registered (round-18 text, `d3a0000` SCORECARD)

Quoted from `git show d3a0000:SCORECARD.md` §"Round 18 — declared claims":
surfaces P1 Hyprland, P2 Waybar, P3 Walker, P4 terminals, P5
themes/wallpapers, P6 idle/lock; "rubric V (unchanged instrument)"; baseline
declared `4/6 = 6.6667`, "P3 Walker, P5 themes open". The counting predicate
is the round-17 declaration plus the tightenings recorded in that round's
"pre-measurement corrections": a `corpus/knowledge/` entry counts when its
first 15 lines carry `source:` citing a `mined` tier-A `SOURCES` row whose
`used-by` names the entry, and the entry declares the surface by exact
`surface: P<n>` (new entries) or by the fixed legacy map `U1|U2 → P1`,
`U7 → P2`; surface entries additionally need one cited upstream-https
docs/spec/code row naming the surface in its source or scope cell, all four
required sections, ≥3 non-blank lines each, and `[UNK]` in
`## Unexercised behavior`.

## Inventory at `d9a5a18`

- `corpus/knowledge/` contains **32** `.md` entries (round 17 added
  `terminal-route-r17.md`, `idle-lock-route-r17.md`). All 32 names appear in
  the `corpus/README.md` navigation table ("navigation map of admitted
  evidence", `corpus/README.md:5`). `git ls-tree` → 32; per-entry README
  membership test → 0 missing.
- `corpus/SOURCES.md` has **71** registry rows (`S001`–`S071`, `## Registry`
  at line 9): tier A 64 / B 1 / C 6; status mined 56 / queued 8 / rejected 7.
  Every mined row is tier A (`mined+A = 56`), so tier and status cannot
  disagree in this join.
- Digests: `corpus/SOURCES.md` `fec7f698ae4447ee…`, `PROVINCE.md`
  `7aad7b863dc3c10b…`, `.ufo/waves/round-17/measure.py`
  `de4c422b55c67f82…` (all `git show d9a5a18:<path> | sha256sum`).

## Join table — every entry whose head carries an `S###` token

Legend: `self` = the row's `used-by` cell, comma-split, names this entry
path. `kind`/`https` are from the source cell. Ten entries carry `source:`
S-tokens in their first 15 lines:

| entry | `source:` head line | S tokens | token-level join | `covers:` | `surface:` | province |
|---|---|---|---|---|---|---|
| `config-drift-r12.md` | 3 | S013 S014 S015 | all A/mined/self | — | — | none (no declaration) |
| `hyprland-config-era-r12.md` | 3 | S021–S030 | S021–S029 A/mined/self; **S030 A/rejected, used-by `—`** | `U2` (l.6) | — | **P1** |
| `idle-lock-route-r17.md` | 1 | S063–S069 | all A/mined/self | — | `P6` (l.4) | **P6** |
| `input-debugging-boundaries-r15.md` | 1 | S051 S052 | both A/mined/self | `U6` (l.4) | — | none (U6 unmapped) |
| `output-colour-boundaries-r14.md` | 1 | S041 S047 S048 S050 | all A/mined/self | `U5` (l.4) | — | none (U5 unmapped) |
| `terminal-route-r17.md` | 1 | S056–S060 S071 | all A/mined/self | — | `P4` (l.4) | **P4** |
| `waybar-observation-boundaries-r16.md` | 1 | S053 S054 | both A/mined/self | `U7` (l.4) | — | **P2** |
| `wayland-protocol-boundaries-r13.md` | 1 | S005 S040 S041 S042 S043 S046 | all A/mined/self | `U4` (l.4) | — | none (U4 unmapped) |
| `window-rule-effects-getprop.md` | 3 | S002 S016–S020 | all A/mined/self | `U1` (l.6) | — | **P1** |
| `xdg-portal-routing-r12.md` | 3 | S031–S035 S037 | all A/mined/self | `U3` (l.6) | — | none (U3 unmapped) |

Remaining **22** entries fail the source leg: **3** carry a prose `source:`
line with no `S###` token (`arc-synthesis.md:3`, `closeout-r11.md:3`,
`gate-standing-use.md:3`) and **19** carry no `source:` line in their first 15
lines at all: `config-health-report-r3`, `executor-test-sufficiency`,
`gate-mutation-proof`, `gate-mutation-sweep-r8`, `hyprctl-verification-layer`,
`hyprland-config-plane`, `idle-lock-plane`, `keybind-rule-semantics`,
`omarchy-drift-watch`, `province-accuracy-selfaudit`,
`remaining-planes-census`, `snapshot-diff-receipt-r9`, `terminals-and-omarchy`,
`theme-wallpaper-plane`, `walker-deep`, `walker-deep-r9`,
`walker-live-surface`, `waybar-walker-plane`, `waybar-walker-semantics`.

`covers:` appears exactly once per value, `U1`…`U7` each on one entry (no
duplicate and no combined `covers: U1|U2` token in any file; the `U1|U2` form
exists only as prose in `SCORECARD.md`). `surface:` appears in exactly two
files in the whole tree — the r17 P4 and P6 routes, both at line 4.

## Result — baseline is exactly 4/6 = 6.6667

| surface | covered by | via |
|---|---|---|
| P1 Hyprland config tree | `window-rule-effects-getprop.md` and `hyprland-config-era-r12.md` | `covers: U1` → P1, `covers: U2` → P1 |
| P2 Waybar | `waybar-observation-boundaries-r16.md` | `covers: U7` → P2 |
| P3 Walker | **none** | no `surface: P3`; U3–U6 are portal/wayland/colour/input and are unmapped |
| P4 terminal configs | `terminal-route-r17.md` | `surface: P4` |
| P5 themes/wallpapers | **none** | no `surface: P5`; no theme/wallpaper row exists to cite |
| P6 idle/lock | `idle-lock-route-r17.md` | `surface: P6` |

Covered = {P1, P2, P4, P6} = **4/6 = 0.6667 = 6.6667/10**, matching the
round-18 pre-registration. Robustness notes: P1 is carried twice (U1 and U2),
so the rejected `S030` cited by the U2 entry cannot un-cover P1 — the U1
entry's six cited rows all join (S002 is own-work/non-https but mined tier A
and names the entry). P2 rests on one entry (S053/S054, both docs+code https).

### Facet evidence for the two counted `surface:` notes

- Exact declaration line `surface: P4` / `surface: P6`, head line 4, one
  surface each (a second `surface:` line would be rejected by the instrument's
  single-surface rule).
- Required headings all present, non-blank body lines (awk, body to next
  `## `): `terminal-route-r17` Upstream 50 / Host 26 / Safe 9 / Unexercised
  29; `idle-lock-route-r17` 26 / 35 / 6 / 12. Both above the 3-line floor.
- `[UNK]` inside `## Unexercised behavior`: 5 occurrences (P4), 12 (P6).
- Upstream facet (docs/spec/code **and** `https://` in source cell **and**
  surface keyword in source+scope, case-insensitive): P4 — S056 `docs`
  matches `terminal` (`xdg-terminal-exec` URL), S057 `code` `terminal`, S058
  `docs` `alacritty`; P6 — S063/S065/S066/S067/S068 match `hypridle`/`idle`,
  S064/S069 match `hyprlock`. Non-https rows S059/S060/S071 (P4) do not
  satisfy this facet but do satisfy the source join, which is all the legacy/
  source leg requires.

## No existing entry covers P3 or P5 (four independent checks)

1. `git grep -n '^surface:' d9a5a18 -- corpus/knowledge` returns exactly two
   lines: `idle-lock-route-r17.md:4:surface: P6` and
   `terminal-route-r17.md:4:surface: P4`. No `P3`, no `P5`, at any line.
2. Only `U1`/`U2`/`U7` are mapped, and those three tokens sit on exactly the
   three legacy entries above. `U3`–`U6` entries are xdg-portal, wayland
   protocol, output colour and input debugging — none of them Walker or
   themes, and all unmapped regardless.
3. `SOURCES.md` contains **zero** occurrences of `walker`, `elephant`,
   `wallpaper`, `swaybg` or `hyprpaper` (`grep -ic` each → 0). `theme` occurs
   only inside S059's anchor cell ("omarchy theme import target"), a
   non-https host-file row for P4. So at baseline there is no tier-A upstream
   row that could satisfy the P3/P5 keyword facet even if a note declared it.
4. Subject-named candidate notes all fail the head leg outright:
   `walker-deep.md`, `walker-deep-r9.md`, `walker-live-surface.md`,
   `waybar-walker-plane.md`, `waybar-walker-semantics.md`,
   `theme-wallpaper-plane.md`, `remaining-planes-census.md`,
   `terminals-and-omarchy.md`, `idle-lock-plane.md` carry no
   `source:`/`covers:`/`surface:` line in their first 15 lines.

## What C2 (→ 6/6) must produce, mechanically

Two new `corpus/knowledge/*.md` notes, each with: `source:` S-token(s) in the
first 15 lines, exactly one exact `surface: P3` / `surface: P5` line, the four
required headings with ≥3 non-blank lines each and `[UNK]` in
`## Unexercised behavior`, ≥1 cited row that is `mined` tier A whose
`used-by` names the note path, and ≥1 cited row that is kind
docs/spec/code with an `https://` source and `walker|elephant` (P3) or
`theme|wallpaper|hyprpaper|swaybg` (P5) in its source or scope cell. Round-18
C2 adds a committed raw fetch receipt per newly credited row
(`.ufo/waves/round-18/fetch/<Seat>/`, R17-V3) — the instrument cannot check
that, so closure must.

## Hazards a closure should not miss

1. **Instrument ≠ declaration on admission.** `measure.py` counts any
   `corpus/knowledge/**.md`; it never reads `corpus/README.md`. "Admitted"
   (README nav row) must be checked separately, as it was at round 17.
2. **Keyword substring test is weak.** Source/scope substring `walker` or
   `theme` passes even when the fetched document is a different project or a
   glossary page; only the receipt bodies + quote review (R17-V3) distinguish
   a real route from a label. This is the P3/P5 replay of round-17's
   `AttackRubricGaming` risk.
3. **Silent rejection.** The instrument collects `rejected[]` and still exits
   0; a malformed note (two `surface:` lines, a section under the floor, no
   `[UNK]`, no upstream row) simply does not count. At baseline `rejected` is
   empty; closure should require it stays empty rather than reading only
   `count`.
4. **Instrument identity.** The C2 command hashes nothing. The file at
   `d9a5a18`/`d3a0000` is `de4c422b55c67f82…`; the round-17 correction
   paragraph names `4023124f…` (state at `ab0bc9b`), and the later 12-line
   wave-2 change (Registry-section scoping, `ab0bc9b..f71ccbe`) produced
   `de4c422b…`. A round-18 receipt that cites `4023124f…` would cite a stale
   instrument — the R17-V1/V2 pattern on the C2 side.
5. **Baseline receipt is not git-bound.** `SCORECARD.md` (round-18) cites
   `evidence/measure-before.json`; at `d3a0000` that path is **untracked**
   (`git status --porcelain` → `?? .ufo/waves/round-18/evidence/measure-before.json`;
   `git log --all -- <path>` → empty; `git ls-tree -r d3a0000` shows only
   `census-start.txt` under round-18 evidence). The round-17 analogue
   (`.ufo/waves/round-17/evidence/measure-before.json`) *is* committed. My
   own recomputation agrees with that untracked file's `c2` block exactly
   (count 4, P1/P2/P4/P6, `rejected: []`, `u_routes: 7`), but a closure cannot
   re-derive it from a commit as things stand.
6. **Legacy pinning is a no-op here.** The instrument pins legacy credit to
   the three paths that held it at `27cd06f`; my declared-map recomputation
   (no pin) gives the same three entries, so the pin changes no number at
   this baseline.

## Cross-check against the baseline receipt (not used as the oracle)

`.ufo/waves/round-18/evidence/measure-before.json`
(`sha256 19bd0fee1c30b625…`, untracked) reports `c2.count = 4`,
`score = 6.6667`, P1 = {`hyprland-config-era-r12` (S021–S029),
`window-rule-effects-getprop` (S002, S016–S020)}, P2 = {`waybar-observation-
boundaries-r16` (S053/S054)}, P4 = {`terminal-route-r17` (S056–S060, S071)},
P6 = {`idle-lock-route-r17` (S063–S069)}, P3/P5 empty, `rejected: []`,
`u_routes: 7` (`U1`–`U7`). Every field matches my independent join; no
disagreement to report.

## Reproduction (read-only; no lane write)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git ls-tree -r --name-only d9a5a18 -- corpus/knowledge | wc -l          # 32
git grep -n '^surface:' d9a5a18 -- corpus/knowledge                    # 2 lines, P6/P4
git grep -h '^covers:'  d9a5a18 -- corpus/knowledge | sort | uniq -c   # U1..U7 x1
git show  d9a5a18:corpus/SOURCES.md | awk -F'|' '/^## /{r=($0=="## Registry");next}
  r && /^\| *S[0-9][0-9][0-9]/{print $2,$5,$9,$12}'                    # id tier status used-by
for f in $(git ls-tree -r --name-only d9a5a18 -- corpus/knowledge); do
  git show d9a5a18:$f | sed -n '1,15p' | grep -E '^(source|covers|surface):'; done
git show d9a5a18:corpus/SOURCES.md | grep -icE 'walker|elephant|wallpaper|swaybg|hyprpaper'  # 0
```

## Limits / remaining unknowns

- I did not run `measure.py` and so cannot certify that its runtime output
  equals this join in every rejected/fringe case (the receipt cross-check
  above is agreement on this baseline, not a proof).
- I did not verify fetch receipts for any baseline-credited row; R17-V3 binds
  rows credited in round 18, and P4/P6 credit predates that rule. Whether the
  r17 receipts under `.ufo/waves/round-17/` cover S056–S060/S071 and
  S063–S069 was not re-audited here.
- "Admitted" is treated as README-nav-table membership (the repo's own stated
  admission map); the instrument uses bare path presence.
- No content-honesty judgement: I confirm the predicate joins, not that the
  cited documents actually teach what the notes claim.
- Confidence: **high** on 4/6 and the per-entry token join (mechanical,
  revision-pinned); **high** on the P3/P5 absence; **medium** on admission
  semantics (README table vs instrument path scan, disclosed above).
