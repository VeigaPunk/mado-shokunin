# UnknownsJoin — P6 route ↔ §11 / Frontier: what a documentary route narrows

Seat: `MadoR17.UnknownsJoin` (connector, leaf; report only). Date 2026-10-20.
Target root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read first:
`corpus/lessons/round-16-verifier-spotcheck.md` (all 185 lines), including
R16-V1 and its distinction between a receipt's exit code and its finding.

Gates: no delegation, no commits, no `jj`, no `agent://all`. No `pacman`/
`yay`/`paru` (not even `-Q`/`-Si`), no `sudo`, `systemctl`, `hyprctl`,
`hypridle`/`hyprlock`, `omarchy-*`, `notify-send`, screenshot or input/device
probe. Only `read`/`cat`/`grep`/`sed`/`sha256sum` file reads. No tool
installed or updated.

## 1. Axes named

- **C2 coverage (rubric V).** The move must not change the count or the
  measurement; it bounds what "P6 covered" means by publishing the
  documentary split where readers of the historical note and the Frontier
  actually land.
- **C1 calibration (literal QUALITY lesson-citation fraction).** R16-V1's
  defect class is "a receipt cited for a token it does not carry". A route
  note admitted as "P6 covered" without a statement of what it does *not*
  establish reproduces that class at note scale. The move is the same label
  discipline applied to the new route; no `corpus/QUALITY.md` text changes.
- **Harm watch (freshness/operability/depth/adjacency).** Must stay
  unchanged: no host operation, no new measurement, no gate byte touched.

## 2. Baseline anchors `[OBS]`

| Fact | Anchor |
|---|---|
| Historical idle note, 382 lines; §11 at l.327, items 1–8 at l.329, 330–332, 333–334, 335–337, 338–341, 342, 343–344, 345; §12 at l.347; E2 block begins l.358 | `corpus/knowledge/idle-lock-plane.md` |
| §10 heading says errata are append-only: "add blocks, never edit above" (l.318) | same |
| Existing Frontier bullet invokes exactly the two open halves | `corpus/README.md:81-83` |
| Province "Screen / idle / lock" route row | `corpus/README.md:62` |
| Coverage-map row for the historical note | `corpus/README.md:20` |
| README ends at l.116 (round-16 Frontier bullet) | `wc -l` |
| P6 route target path and section list are fixed by the dispatch item | `.ufo/waves/round-17/w1/spec.json`, `NoteIdle` prompt: `corpus/knowledge/idle-lock-route-r17.md`, sections `## Upstream contract` / `## Host declaration` / `## Safe observation` / `## Unexercised behavior`, header lines 1–6 with `source:` and `surface: P6` |
| Sibling route note landed in the same shape (header `source:` l.1, `surface: P4` l.4; 120 lines) | `corpus/knowledge/terminal-route-r17.md` |
| P6 route note landed at 11:04: 134 lines, sha256 `0820cd50dfbdb7a38cc6c9cea39a65a2eeb9f34c7ed5390163f7453b414ca4b2`; its `## Unexercised behavior` names §11 items **1, 2, 5, 6, 8** and the file contains no `IdleHint`/`LockedHint` mention | `corpus/knowledge/idle-lock-route-r17.md` |
| Rubric-V baseline: 2/6, no `surface:` token anywhere in `corpus/knowledge/` at `27cd06f`; the historical idle note fails the source leg (no `source:` line) | `.ufo/waves/round-17/w1/reports/RubricBaselineScout.md` §§Observed facts, Result |
| Existing Frontier draft appends a round-17 bullet after l.116 and a coverage row linking the new note to "§11 for open unknowns" | `.ufo/waves/round-17/drafts/FrontierDraft.md` |
| File-plane gate pins host config paths only; no `corpus/knowledge/*` byte pins in `tools/mado-verify.sh` (grep for `corpus/knowledge` returns comments only) | `tools/mado-verify.sh:2561-2579` |
| Historical pin (`381` lines, `a0597be96c107799`) still matches the working file's sha256 exactly; `wc -l` reports **382** (trailing-line counting convention, not content drift) | `corpus/knowledge/arc-synthesis.md:90`; `sha256sum corpus/knowledge/idle-lock-plane.md` |

`[OBS]` The link is still **one-way**. The landed note names
`idle-lock-plane.md` in backticks and cites §11 item numbers in its
`## Unexercised behavior` (items 1, 2, 5, 6, 8), but it carries no markdown
link and the historical note has no pointer forward; the README bullet that
names the two unknowns is unchanged. A reader who starts at README or §11
cannot reach the route; a reader who starts at the route gets no per-item
verdict, only the note's own open list.

## 3. What the documentary route narrows vs leaves open

The landed note's source set is the two wiki pages (hypridle, hyprlock) and
tag-pinned hypridle v0.1.8 (README, `Hypridle.cpp`, `Hypridle.hpp`,
`main.cpp`) plus hyprlock v0.9.6 README (header, l.1-3). It does **not** open
a logind document or the hyprlock source; the `Lock`/`Unlock`/`PrepareForSleep`
behaviour it cites is hypridle's own handler, not logind's contract. Its
`## Unexercised behavior` names idle timing, listener firing, lock success,
lock-notify availability, stop cause, multi-monitor and host version as open.

| §11 item | Route material that can touch it | Verdict |
|---|---|---|
| 1 daemon absence / stop-cause (l.329) | `## Host declaration` start route (omarchy `autostart.conf:1`); no stop-cause evidence; `## Unexercised behavior` names item 1 | **open**; only the *start* route is documented. E2's `omarchy-toggle-idle` and `omarchy-restart-app` remain the only file-visible stoppers |
| 2 live transitions, "screensaver resets idle timer", ≈302 s (l.330-332) | `## Upstream contract` listener `timeout`/`on-timeout`/`on-resume`; route states firing unexercised | **open** for the host timeline; the route may cite only the declared contract. The L14 comment's reset story stays an untested `[INF]` from comment text |
| 3 logind `IdleHint`/`LockedHint` writer; hyprlock participation (l.333-334) | adjacent only: dbus `Lock`/`Unlock` → `lock_cmd`, `PrepareForSleep`, `ext-session-lock` [LR:5]; the note never mentions `IdleHint`/`LockedHint` and does not list item 3 | **open**; do not cite the route for this item. The trigger surface is documented; neither the hint writer nor hyprlock's participation is |
| 4 config parse (l.335-337) | `## Host declaration` key vocabulary and bytes; `## Safe observation` | **open**; documented keys are not a parser run, and loading either config stays a session mutation |
| 5 cursor restore after kill (l.338-341) | none — reset lives in `omarchy-screensaver`'s trap, outside the route's files | **open** |
| 6 `inhibit_sleep = 3` semantics (l.342) | `## Upstream contract`: mode 3 = "wait until locked" [HW:22-26,33], gated on `lockNotifier` [HC:128-129] and the `hyprland-lock-notify-v1` warning [HC:104-107]; `## Unexercised behavior` names item 6 | **narrowed to a testable criterion**: documented semantics + precondition replace the L5 comment; whether this host exposes the protocol (hence whether mode 3 waits) stays `[UNK]` |
| 7 waybar idle-indicator rendering (l.343-344) | none — P2 surface | **open** |
| 8 multi-monitor chain (l.345) | none — route covers auth/grace, not background/monitor surface, and the host is single-monitor | **open** |

Nothing in this matrix adds a consumer, a transition, a lock attempt or a
host version. That is the whole narrowing: **one item gains a documented
criterion (6); the other seven stay open — item 1 gains only start-route
context, never a cause — including both halves the README bullet names.**

One mapping wrinkle: the note cites §11 item 5 under "Listener firing and
on-resume execution", but item 5 is the cursor-restore question. The citation
does not claim cursor behaviour, and E3's item 5 stays **open**; L1 should
not read the note's list as covering it.

## 4. Proposed move (one bounded package, four exact edits)

Ownership split so item numbers never fork: the **new note** owns its own
boundary (`## Unexercised behavior`), the **old note's append-only errata**
owns the §11 numbering, the **README** owns the public claim.

### A. `corpus/knowledge/idle-lock-plane.md` — append after l.382

Keep E1/E2 unedited; this is a new block, not a rewrite of §11.

```markdown
## Errata (round 17) — appended 2026-10-20 (P6 documentary route)

Append-only block; E1/E2 above stand unedited and §11's list is not
rewritten. Round 17 adds
[`idle-lock-route-r17.md`](idle-lock-route-r17.md), a **documentary** route
(tagged hypridle/hyprlock wiki and raw upstream, including the logind/D-Bus
lock-signal handling they declare; host files joined by sha256). It adds no
process observation, no transition, no lock attempt and no host binary
version. P6 coverage under round 17's rubric V is a route admission, not a
behavioural measurement: the transition and stop-cause unknowns below are
not narrowed by it.

- **E3 (UNK dispositions, documentary side only).** Items keep the status
  recorded in §11; only their documented side changes:
  1. *Daemon absence / stop-cause* — **open**. The route documents only the
     start route (omarchy `autostart.conf:1`, `uwsm-app -- hypridle`) and
     records that the file loading the default autostart, and the stop
     cause, are `[UNK]` there; E2's toggle and restart routes remain the
     only file-visible stoppers.
  2. *Live transitions (≈302 s)* — **open**. The route cites the declared
     listener contract (`timeout`/`on-timeout`/`on-resume`) and states that
     firing is unexercised. The L14 comment's "screensaver resets idle
     timer" stays an untested `[INF]` from comment text; the route does not
     measure it.
  3. *logind `IdleHint`/`LockedHint` writer* — **open**. The route
     documents the dbus `Lock`/`Unlock` trigger that runs `lock_cmd`, the
     `PrepareForSleep` hook, and that hyprlock uses `ext-session-lock`, but
     it makes no claim about the hint properties; which component writes
     them, and whether hyprlock takes part, stay `[UNK]`.
  4. *Config parse* — **open**. The route fixes the documented key
     vocabulary and file bytes only; no parser was run, and loading either
     config remains a session mutation (§11.4 unchanged).
  5. *Cursor restore after a kill* — **open**. The reset still lives in
     `omarchy-screensaver`'s trap (L9-14), outside the route's files.
  6. *`inhibit_sleep = 3`* — **narrowed to a testable criterion**: mode 3
     is documented as wait-until-locked and gated on the compositor's
     `hyprland-lock-notify-v1` (`lockNotifier`); whether this host exposes
     it, and therefore whether mode 3 waits, stays `[UNK]`.
  7. *Waybar idle-indicator rendering* — **open**. P2 surface; the route
     carries nothing about it.
  8. *Multi-monitor chain* — **open**. Single-monitor host; no chain
     observation.
```

Link correctness: the note sits in `corpus/knowledge/`, so the sibling link
is bare `idle-lock-route-r17.md`. Do **not** write `knowledge/...` there;
the existing sibling-link precedent is bare-filename
(`input-debugging-boundaries-r15.md:33` → `hyprctl-verification-layer.md`).

### B. `corpus/README.md` — replace l.81-83

Old (verbatim):

```markdown
- Idle/lock transitions and daemon stop-cause: [idle/lock unknowns](knowledge/idle-lock-plane.md)
  §11 and [terminal dispositions](knowledge/closeout-r11.md) §5. No new
  consumer or transition measurement is claimed.
```

New:

```markdown
- Idle/lock transitions and daemon stop-cause: [idle/lock unknowns](knowledge/idle-lock-plane.md)
  §11 and [terminal dispositions](knowledge/closeout-r11.md) §5. Round 17
  adds only a [documentary route](knowledge/idle-lock-route-r17.md); neither
  half of this line is narrowed, and the [§11 E3](knowledge/idle-lock-plane.md)
  split records which other §11 items are narrowed, documented side only.
  No new consumer or transition measurement is claimed.
```

The invariant sentence is preserved verbatim; the bullet gains a forward
pointer and an explicit "neither half" so a green C2 cannot be read as
closing it.

### C. `corpus/README.md:62` — Province-routes "Start here" cell only

Old substring: `[idle/lock plane](knowledge/idle-lock-plane.md) §§2–5, §§7–11;`
New substring: `[idle/lock plane](knowledge/idle-lock-plane.md) §§2–5, §§7–11, [round-17 documentary route](knowledge/idle-lock-route-r17.md);`

Leave the Limit cell unchanged: it already says "No idle/lock transition was
exercised; consumer presence and stop-cause are dated observations/unknowns,
not a new live verdict."

### D. `corpus/README.md:20` — forward pointer in the historical row

Old substring: `Never execute lock/wake/toggle scripts as a probe.`
New substring: `Never execute lock/wake/toggle scripts as a probe. Round 17 adds only a [documentary route](knowledge/idle-lock-route-r17.md); its § Unexercised behavior keeps transitions and stop-cause open.`

And, in the round-17 coverage row that `FrontierDraft` adds, change
`§11 for open unknowns` → `§11/E3 for the open/narrowed split` so the index
points at the dispositions rather than the raw list.

## 5. Risks and contradictions stated

1. **Claim inflation (the real risk, now exercised).** A pre-landing draft of
   E3 called items 3 and 6 narrowed. Against the landed note, item 3 fails
   the gate (the note never mentions `IdleHint`/`LockedHint` and does not
   list item 3), so it is recorded **open**; item 6 passes ([HW:22-26,33],
   [HC:128-129], [HC:104-107]). Do not restore item 3 to "narrowed" without
   a note claim that names the hint properties — that would be R16-V1 again,
   one artifact over.
2. **Contradiction with the rubric count.** Rubric V counts P6 as covered on
   a documentary predicate; §11 counts transitions and stop-cause as
   unknown. Both are true at once, but only if the artifacts say so. A is
   the statement; without it the count reads as behaviour.
3. **Append-only vs historical pins.** Appending E3 changes the note's
   trailing bytes; the historical pin at `arc-synthesis.md:90` (`381`,
   `a0597be…`) then no longer matches the file. That row is historical
   (r4) and is not re-anchored by this move: do not edit it, and do not
   rewrite §11. The gate does not pin knowledge bytes
   (`mado-verify.sh` EXPECT = host config paths only), so the file plane is
   not at risk. If L1 wants a receipt for the new bytes, record the
   post-append sha256 in the round lesson, not in the arc row.
4. **Rubric gaming vector 1 (relabel-only).** Do not "help" by adding
   `source:` or `surface: P6` to `idle-lock-plane.md` itself. Its first 15
   lines carry neither token today; adding them would manufacture a second
   P6 count from an unsourced historical note — exactly the relabel vector
   the baseline scout names and the rubric cannot detect.
5. **Link target exists, but the reverse link is prose only.** The note
   landed at 11:04 (134 lines, sha256 `0820cd50…`); it names
   `idle-lock-plane.md` in backticks and cites §11 item numbers, but carries
   no markdown link. A/C/D add the clickable path and can land now. If the
   note is later renamed or its `## Unexercised behavior` heading moves, B's
   link text goes stale — re-grep before integration.
6. **Duplication.** Do not copy the 8-item disposition table into the new
   note: item numbers live in §11 and would fork. The new note cites §11 in
   prose and item numbers; E3 links back with the verdicts; README points
   at E3.

## 6. Verification (falsifiable; L1 runs once)

```sh
# 1 append-only proof: pre-edit bytes are a prefix of post-edit bytes
sha256sum corpus/knowledge/idle-lock-plane.md            # before
head -n 382 corpus/knowledge/idle-lock-plane.md | sha256sum   # after = before

# 2 link resolution + direction
test -f corpus/knowledge/idle-lock-route-r17.md
grep -n 'idle-lock-route-r17' corpus/knowledge/idle-lock-plane.md corpus/README.md
grep -n 'idle-lock-plane.md' corpus/knowledge/idle-lock-route-r17.md

# 3 E3 completeness: exactly items 1..8, each once
sed -n '/## Errata (round 17)/,$p' corpus/knowledge/idle-lock-plane.md \
  | grep -cE '^  [1-8]\. '

# 4 Frontier invariant survives verbatim
grep -c 'No new consumer or transition measurement is claimed' corpus/README.md

# 5 README tail untouched by the bullet edit (33 lines after old l.83)
tail -n 33 corpus/README.md | sha256sum    # compare before/after

# 6 narrowing gate (must precede A): item 6 anchors present; item 3 absent
grep -nE 'inhibit_sleep|lock-notify|lockNotifier' corpus/knowledge/idle-lock-route-r17.md
grep -c 'IdleHint\|LockedHint' corpus/knowledge/idle-lock-route-r17.md  # 0 → item 3 open

# 7 no-harm check on the scored axis: rubric V reads only a note's first 15
# lines and the SOURCES used-by cells; none of A-D touches either.
git show <REV>:corpus/knowledge/idle-lock-route-r17.md | sed -n '1,15p'
python3 .ufo/waves/round-17/measure.py <REV>   # must equal the header-only count
```

`[OBS]` Read-only gate run against the landed note: item 6 passes — mode-3
semantics [HW:22-26,33], the `lockNotifier` guard [HC:128-129] and the
`hyprland-lock-notify-v1` warning [HC:104-107] are present; item 3 fails —
the file contains no `IdleHint`/`LockedHint` text, and § Unexercised
behavior lists items 1, 2, 5, 6, 8 only. E3 above is written to that result.
I ran no other check and no host command; 1–5 and 7 are L1's. Command 6 is
what decides A's narrowed line; command 7 proves the move did not buy
coverage with a measurement.

## 7. Integration order

1. **Done at 11:04**: `corpus/knowledge/idle-lock-route-r17.md` exists
   (134 lines, sha256 `0820cd50…`), with `surface: P6` on l.4 and its
   `source:` line on l.1; it cites §11 in prose and carries no markdown
   link.
2. L1 applies C and D, then B, then A (the note now exists, so no ordering
   constraint remains).
3. Run §6 checks 1–7; if check 6 fails, edit A's narrowed line (item 6) to
   "open" rather than dropping it — the disposition map is the move, the
   verdicts are its evidence.
4. Log the append in the round lesson and leave `arc-synthesis.md:90` as
   historical; do not re-pin it.
