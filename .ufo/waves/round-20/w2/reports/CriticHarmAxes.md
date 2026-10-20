# CriticHarmAxes — partly falsified: every owned axis count holds (V 6/6, U 7/7, navigation 35/35, depth+1, adjacency clean), but the new note's malformed `surface:` head lands the first-ever MALFORMED rejection in the r17 measure counter and contradicts its own README row

## Scope and method

Ran the two checks my item names — `python3 .ufo/waves/round-17/measure.py REV` (c1/c2/c3) and the navigation "Counting command" block extracted from `SCORECARD.md` — at the pre-round-20 base `1f7f995caa25627db804e996cccd87fe38a3a1b6`, the pre-harm reference `9c54c56`, every round-20 commit (`e629f73`, `f3da504`, `28c6837`, `4362219`), and tip `a4046a8216080d4004de3f268c62cf142095ac07`. All reads are `git show`/`ls-tree` bytes in the lane and a `/tmp/mado-r20w2-CriticHarmAxes` clone (origin removed). The navigation block itself was extracted from `git show a4046a8:SCORECARD.md` (the REV-pinned form the harm-watch uses) and run with `REV=<full sha>`.

## Findings

### F1 — MINOR / fixable — `surface: lane tooling` on `tripwire-precision-r20.md` is malformed under the rubric grammar and self-contradicts the index

- `corpus/knowledge/tripwire-precision-r20.md:4` reads
  `surface: lane tooling — the post-hoc transcript tripwire and hermetic stub harnesses (not a host plane)`.
- `corpus/README.md:46` describes the same note as `(round 20; lane tooling, no surface)`. The index says *no surface*; the head declares a `surface:` field.
- `measure.py` (T2, lines 197–212): a `surface:` line must `fullmatch(r'surface: (P[1-6])')`; anything else is `MALFORMED` and the entry is listed under `rejected`. Reproduction:

  ```
  $ python3 .ufo/waves/round-17/measure.py a4046a8
  "rejected": [{"path": "corpus/knowledge/tripwire-precision-r20.md",
                "declared": ["MALFORMED"],
                "reason": "surface line must be exactly `surface: P<n>`"}]
  ```

- This is the **first non-empty `rejected` list in the lane's measured history**: `rejected: []` at `9c54c56`, `1f7f995`, `e629f73`, `f3da504`, `28c6837`; the anomaly appears exactly at `4362219` (the commit that adds the note) and persists at `a4046a8`. Rejections are otherwise reserved for real quality failures (missing required headings, thin sections, missing `[UNK]`, unjoined sources, multi-surface claims) — the note is rejected for none of those, so `rejected` now mixes a malformed-head bookkeeping artifact with genuine admission failures, weakening the signal any future reader draws from it.
- Why it is a defect and not a tradeoff: the declared axis (harm-watched counts) is untouched — the entry never claimed a province, so no `P<n>` coverage depends on it; but the note itself is now an uncountable, rejected entry whose head field disagrees with its README row. Two honest readings both end in "fix the note": (a) `surface:` is reserved for `P[1-6]` (the only grammar `measure.py` admits and the only form the four route notes use — `idle-lock-route-r17.md:4`, `terminal-route-r17.md:4`, `walker-route-r18.md:4`, `theme-route-r18.md:4`), so line 4 is a misused field; (b) `surface:` is free-text, in which case the README's "no surface" is false and `measure.py` over-rejects. Reading (b) would require changing the pinned counter grammar mid-round; (a) requires a one-line note edit.
- **Smallest safe correction:** rename the head field on `tripwire-precision-r20.md:4` to a non-rubric key (e.g. `scope: lane tooling — …`), keeping the "(not a host plane)" qualifier. `measure.py` then sees no `surface:` line, the note returns to the ordinary unsurfaced-entry path (it is still `sourced` via S099–S112 mined tier-A rows naming it in used-by), `rejected` returns to `[]`, and the README row becomes literally true. No score changes at any revision; no counter or prose change needed.
- Impacted axis: none of the six counts (below) — the harm is to the **honesty of the counter's `rejected` facet and head/index consistency**, a fixable defect, not a canonical-judge rejection of the round.

### F2 — No harm found on the six named axes (confirmation with commands that would have shown otherwise)

| Axis | Base → tip | Command | Result |
|---|---|---|---|
| Coverage V (provinces P1–P6) | 6/6 → 6/6 | `python3 .ufo/waves/round-17/measure.py <rev>` | `c2.count=6` at `9c54c56`, `1f7f995`, and `a4046a8` (score 10.0 both ends); covering entries unchanged: `hyprland-config-era-r12`+`window-rule-effects-getprop` (P1 legacy), `waybar-observation-boundaries-r16` (P2), `walker-route-r18` (P3), `terminal-route-r17` (P4), `theme-route-r18` (P5), `idle-lock-route-r17` (P6). Would have shown harm as `count<6` or a missing `entries` list. |
| U routes | 7/7 → 7/7 | same | `u_routes=7`, `u_routes_seen=[U1..U7]` identical at base and tip; the new note adds no `covers:` line, so the census did not shrink or inflate. |
| Navigation | 34/34 → 35/35, exit 0 | `REV=<sha> bash <extracted SCORECARD Counting command>` | `1f7f995`: `indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0. `a4046a8`: `indexed=35/35 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0. The new note is indexed by its README row (`README.md:46`); would have shown harm as `missing≥1`, `dangling≥1`, `duplicates≥1` or exit 1. |
| Depth | — | `git ls-tree -r a4046a8 -- corpus/knowledge` | 35 `.md` notes (34 → 35); the addition (`tripwire-precision-r20.md`, S099–S112 mined tier-A, verified-at/recheck in head) is a real depth gain, not a dilution: no existing note was truncated or demoted (`git diff --name-status 1f7f995..a4046a8` shows `A` for the note, no `D`/`M` under `corpus/knowledge/`). |
| Adjacency | unchanged | `git diff --name-status 1f7f995..a4046a8` | All touched paths are lane-owned: `corpus/`, `tools/mado-tripwire.py`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `.ufo/waves/`. The only edits outside round-20's own tree are `.ufo/waves/round-19/tripwire/{r19-bashcvar,r19-helperfn}/expected.json` — declared and reasoned (`r20_edit` fields, lesson Decisions), re-verified by me: `--selftest` on both suites at tip passes 45/45 and 34/34 with script sha `9613f510…` matching the pinned tool. No substrate, fleet, sibling-lane, or operator-owned path absorbed. |
| Freshness (rubric a, observational) | 15 → 16 | head-15 `source:`+`verified-at:`+`recheck:` census at both revs | +1 (the new note, `verified-at: 2026-10-20` naming tool sha `9613f510…@28c6837` and recheck triggers). No existing head lost its freshness fields. `sources-census.sh validate --file corpus/SOURCES.md` on the tip clone: `ok`, exit 0 (4 pre-existing W04 duplicate-url notes only). |

### F3 — C1/c3 context (not my axes, recorded for completeness)

`measure.py` c1: `20/28 = 7.1429` at `1f7f995` → `22/30 = 7.3333` at `a4046a8`, matching the committed C2 claim; criteria 29/30 are the two new lesson-cited lines. c3 tool sha `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` matches the SCORECARD-pinned value at every round-20 commit after `28c6837`.

## Limits

- The gate `--selftest` full run and the pending whole-corpus tripwire diff vs `9c54c56` (SCORECARD "C1 guards" explicitly marks it `pending (wave 2)`) are **not** my item and were not run here; other seats own them. My adjacency verdict is path-ownership only, not a tripwire output diff.
- I did not run `--regression` (requires the tameshi harness) or the live gate (forbidden by the host pause).
- The `rejected` list being previously empty is verified only across the seven revisions above; earlier history assumed from `measure.py`'s rejections being introduced in round 17+ [INFERENCE].
- F1's "first-ever MALFORMED" claim covers the measured revisions `9c54c56…a4046a8`; I did not census every historical rev [UNK for pre-9c54c56].

## Installs

none — all checks ran with stock `git`, `python3`, `bash` on a `/tmp` clone; no pacman (paused), no installs.
