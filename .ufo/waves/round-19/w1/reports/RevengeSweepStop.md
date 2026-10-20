# RevengeSweepStop — the round-18 supersession fix stopped at SKILL.md because the sweep was commissioned to erratum *present-tense* claims only, classified every dated note "no erratum", and read the S015 central MOVED table as their carrier; the rule that would have forced the full sweep is PROTOCOL.md:363 "Corrections sweep every mention", which the dispatch cited but scoped down in the same sentence.

Round 19, wave 1, revenge lane. Baseline `9c54c56` (round-18 closure), pre-registration
`17661e0`. Target root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Write scope: this
report only. Read-only git only; no pacman/service/process probe (host pause); no web fetch.

## 1. What the sweep listed

`MadoR18.ConnStalePinsSweep` (wave 2, 2026-10-20) was dispatched with this task text —
`.ufo/waves/round-18/drafts/gen_w2.py:127` (same string committed at
`.ufo/waves/round-18/w2/dispatch.json:790` and `spec.json:320`):

> Corrections sweep (PROTOCOL: corrections sweep every mention): grep SKILL.md,
> corpus/README.md and corpus/knowledge/\*.md for **present-tense** walker 2.17.0 /
> elephant 2.21 / packaged-config 5b4e47b7 claims that the round-18 walker note now
> shows moved; list each with path:line and whether it is **dated (historical) or
> present-tense (needs an erratum)**.

The seat's report (`.ufo/waves/round-18/w2/reports/ConnStalePinsSweep.md`) inventoried
every hit and split it with a D/PT rule (§ Classification rule there):

- **PT — erratum required: exactly two sites**, both in `SKILL.md` — `:22-23` (top-of-manual
  pin, "walker 2.17.0 … re-verified `hyprctl version`") and `:114` (plane-map launcher row,
  "walker 2.17.0" + packaged table "298 L"). Verdict line: "Two claim sites are
  present-tense and now false … Every other hit is either an explicitly dated measurement …
  or an explicit old-value record …; none needs an erratum."
- **D / D-h — "No erratum"**: ~50 further hits across 10 knowledge notes
  (`walker-deep-r9.md`, `walker-deep.md`, `walker-live-surface.md`,
  `waybar-walker-plane.md`, `waybar-walker-semantics.md`, `arc-synthesis.md:229`,
  `closeout-r11.md:43`, `config-health-report-r3.md:900`, `remaining-planes-census.md:246`,
  `walker-route-r18.md` as OK authority) — dated 2026-10-14 measurements; D-h recipes
  flagged "re-baseline or re-date before reuse".
- Its **Proposed move was bounded to SKILL.md only** ("for L1 — not applied; SKILL.md is
  outside my write scope"): replace the `:22-23` pin fragment and the `:114` values, with a
  § "Verification for the erratum" expecting `:23`/`:114` to read 2.17.2 / 305 L after.
  Optional extras it named and L1 did not apply: extend `README.md:135` ("round-5/9" →
  pre-round-18) and a one-line pointer at `:22` ("a reader who stops at the top of the
  manual is the failure mode").
- Its § Contradictions #3 named the carrier gap in advance: `walker-route-r18.md:234-237`
  records the moved pins "recorded, not edited here" (S015 protocol), which "means the
  `SKILL.md` correction has no carrier in this round". § Limits: `SCORECARD.md`, `LOG.md`,
  `reports/`, `corpus/SOURCES.md` were not swept.

## 2. What was applied (commit `be886a3`, 2026-10-20 13:25:12 -0300)

`git show --stat be886a3` doc paths: `SKILL.md +11`, `corpus/knowledge/walker-route-r18.md
+4 −1`, `corpus/knowledge/theme-route-r18.md +20 −1`, `corpus/QUALITY.md +7` (the rest is
fetch bodies/tools). Per file:

- **SKILL.md**: an appended `## Errata (round 18, append-only)` block (now `SKILL.md:1820-1830`)
  naming the two stale sites, quoting `/var/log/pacman.log:2929` (walker 2.17.0-1 → 2.17.2-1)
  and `:3095` (elephant 2.21.0-1 → 2.22.1-1), the new `/etc/xdg` shape (13,743 B / 305 L /
  `3c5c6867…`), `running binary [UNK]`, and "Current documentary route:
  `corpus/knowledge/walker-route-r18.md`". **The sweep's in-place replacement of `:23`/`:114`
  was NOT applied** — append-only protocol forbids the rewrite — so both lines still read
  `walker 2.17.0` / `298 L` today (`grep -n 'walker 2\.17\.0' SKILL.md` → 23, 114, 1475 …;
  verified this session). No pointer was added near `:22` either.
- **walker-route-r18.md**: the +4 −1 is the elephant global-config `[INF]` qualification
  (`:212`, CriticC2W2 D2) — not a pin edit. **theme-route-r18.md**: wave-2 corrections block
  (swaybg wording, consumer edges, S094 tree digests) — not a pin edit. **QUALITY.md +7** is
  the receipt-check note. **Zero lines changed in the ten dated sibling notes** — no forward
  pointers anywhere in `be886a3` (or in `a210241`/`b7148a1`/`9c54c56`: `git log -S'Current
  routing: corpus/knowledge/walker-route-r18.md' -- corpus/knowledge` is empty through
  `17661e0`).
- The round-18 record says exactly this: `corpus/lessons/round-18.md:91` — "`SKILL.md`
  erratum for the dated walker 2.17.0 pins (ConnStalePinsSweep)." The verifier spot-check
  scored freshness "unchanged … move marked by SKILL erratum (`SKILL.md:1822`) and the
  superseding note" (`corpus/lessons/round-18-verifier-spotcheck.md:94`) and routed the rest
  as **R18-V3**: "`walker-deep-r9.md`, `walker-live-surface.md`, `waybar-walker-plane.md`
  (and others: `grep -rln '2\.17\.0' corpus/`) still state 2.17.0 pins with no in-file
  pointer … Append a dated forward pointer (§Evidence standard: corrections sweep every
  mention)" (`round-18-verifier-spotcheck.md:119`).

## 3. Why it stopped at SKILL.md (causal chain, each step evidenced)

1. **The commissioning sentence attached the erratum duty to present-tense only.** The
   dispatch (gen_w2.py:127) cites the PROTOCOL rule by name, then immediately narrows it:
   hits are to be split "dated (historical) or present-tense (needs an erratum)". The D
   bucket is defined as exempt in the same line that commissions the sweep.
2. **The seat's classification rule inherited that frame.** ConnStalePinsSweep §
   Classification rule: "D — dated … No erratum." Its § Contradictions #8 even flags the
   borderline (`walker-live-surface.md:19`, `walker-deep.md:27` read present-tense but sit
   under dated stamps) and resolves them to D. D-h recipes ("re-baseline, do not rewrite")
   got no owner either.
3. **S015 "recorded, not edited here" made per-note pointers look redundant.**
   `walker-route-r18.md:234-237` ("### MOVED pins against the 2026-10-14 notes (recorded,
   not edited here) … The older notes are not edited in this round."; S015 =
   `corpus/SOURCES.md:27`, the `omarchy-drift-watch.md` re-anchor protocol). The central
   table is the correct form *for values* — the sweep itself says "Do not edit the dated
   notes … that would break the evidence chain" — but nothing in S015 says the *sibling
   files* may stay pointer-less; the sweep's Contradictions #3 shows it noticed the
   unowned-correction problem for SKILL.md and stopped there.
4. **The append-only correction rule forced the erratum form but not its reach.**
   PROTOCOL.md:366-367 ("appended, never rewritten") legitimately replaced the sweep's
   in-place `:23`/`:114` edit with the end-of-file erratum — and the sweep's own
   "Optional precision" (pointer at `:22`) and the dated notes were both outside the
   applied move.
5. **Nothing mechanical enforced the sweep, so closure passed.** The rule was prose only:
   round-19 draft `.ufo/waves/round-19/drafts/LessonDraft.md:7` — "Round-18
   ConnStalePinsSweep listed the files, but the fix stopped at the SKILL erratum and one
   note (`corpus/lessons/round-18.md:91`). The sweep rule ('corrections sweep every
   mention') was prose only." No counter existed to go red on 11 files holding bare
   `2.17.0` with no in-file pointer at `9c54c56` (C2 red: "11/13 stale", same line).
   A contributing frame conflict: the round-17 spot-check had read the same
   `SKILL.md:22-26` as "declared claim pins with a re-verify rule, not present-tense host
   facts" (`corpus/lessons/round-17-verifier-spotcheck.md:138`), so the top-of-manual line
   had already survived one freshness pass under a weaker reading.

## 4. The rule that would have forced the sweep

`/home/vgpnk/Projects/shokunin/PROTOCOL.md:363-365` (§ Evidence standard, verified this
session; the round-13 admission row `ReanchorErratum.md:92` cites the same clause as "the
correction mechanism and sweep duty"):

> **Corrections sweep every mention.** Before a round's commit, grep every file the lane
> touches (`corpus/README.md`, `SKILL.md`, `knowledge/`) for the superseded claim — a
> corrected fact left standing in a sibling file is still a defect.

Read literally it sweeps **every mention**, not every present-tense claim. Combined with
S015/append-only (values of dated measurements are never rewritten), the forced move is
exactly R18-V3's: keep `2.17.0` where it was measured, append a dated forward pointer in
each sibling file — "a corrected fact left standing in a sibling file is still a defect"
covers a bare `2.17.0` with no pointer, because the file then asserts a moved pin
unqualified. Round 19 operationalizes it: C2 requires each of the 13 owned files containing
`2.17.0` to gain "a line holding `2.17.2` plus an S### row token" and the gate pin to move
with its selftest (pre-registration `17661e0`, claim C2), enforced by the fresh-pins
counter instead of prose.

Observed state at write time (2026-10-20, mid-wave-1): the forward-pointer blocks exist in
the **working copy only** — 9 knowledge notes modified, uncommitted
(`git diff --stat`: `arc-synthesis.md`, `closeout-r11.md`, `config-health-report-r3.md`,
`remaining-planes-census.md`, `walker-deep-r9.md`, `walker-deep.md`,
`walker-live-surface.md`, `waybar-walker-plane.md`, `waybar-walker-semantics.md`, plus
`measure-mutants.py`, `tools/mado-verify.sh`; `git log -S` for the pointer phrase is empty),
e.g. `walker-deep-r9.md:403` "… On 2026-10-20 the host package moved to 2.17.2:
`/var/log/pacman.log:2929` (S090). Current routing: corpus/knowledge/walker-route-r18.md."
Sibling round-19 seats are landing them now; `SKILL.md:23/:114` still hold the stale
values with the erratum 1,800 lines away.

## Limits

- Host reads (pacman.log, binaries, config bytes) were taken from committed records
  (`walker-route-r18.md:223-228`, S090 rows in `corpus/SOURCES.md:102-103`) and the
  round-18 reports; not re-read from the host (host pause).
- Uncommitted sibling edits were observed mid-flight; their final landed content and the
  eventual C2 score are outside this report.
- I did not re-sweep `SCORECARD.md`, `LOG.md`, `.ufo/reports/` or `corpus/SOURCES.md` for
  stray `2.17.0` (the round-18 sweep's own scope gap); the 13-file count is taken from the
  pre-registered C2 claim, not independently re-derived here.
- be886a3 contains ~340 fetch-body/tool files; only the doc paths were inspected.
- Line numbers of PROTOCOL bullets are from the current fleet worktree; the round-13
  admission row cites identical text at `:363`/`:366-367`, which still matches today.

## Installs

none.
