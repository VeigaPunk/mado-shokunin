# ExistingU7 — existing module-text gap, old MAN/RUN claims, source-scope collisions

Seat: `MadoR16.ExistingU7` (scout, read-only). Observed 2026-10-20 05:38–05:44 -03.
Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`. Method: source reading only;
one fresh HTTPS read of the two tagged raw Waybar files to test the reported
digests. I did not execute `measure.py`, the census, the gate, a selftest or any
mutation harness; no waybar/producer/package/service/compositor/screenshot probe
ran. The lane was being integrated by L1 while I read: `corpus/SOURCES.md`,
`corpus/README.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`,
`corpus/knowledge/waybar-observation-boundaries-r16.md`,
`corpus/lessons/round-16.md` and `tools/mado-action-plan.py` were modified or
untracked during the window. Claims below are timestamped to that window.

## 1. The gap before round 16 (observed)

- **No `covers: U7` note existed.** The six admitted notes carried exactly
  `covers: U1`–`U6`; U7 was the only unscored item of the finite rubric
  (`SCORECARD.md:242-249` defines U7 from `arc-synthesis.md` §6).
- **U7 existed only as anti-claims**, all saying the same thing in different
  words: `arc-synthesis.md:301` (“no IPC/query verb in waybar 0.15.0 (r3
  anti-claim branch)”); `waybar-walker-semantics.md:102` (“no IPC/query verb …
  **UNK**; reconstruct from the producer's own output (**RUN**) where the
  producer is pure-read”); `config-health-report-r3.md:198-201` (help lists
  launch flags only); `closeout-r11.md:42` (module text stays `[UNK]`);
  `corpus/README.md` round-15 prose (pre-edit); `corpus/SOURCES.md` study paths
  `:82, :87, :94` (pre-edit “U5–U7 / U7 remain frontier”).
- **No registry row grounded the Waybar notes.** Before round 16, `S001`–`S052`
  contained no `Alexays`/Waybar URL, and no row's `used-by` named
  `waybar-walker-plane.md` or `waybar-walker-semantics.md` (grep over
  `corpus/SOURCES.md`). `S013` (gkeep installer) merely mentions a copied
  Waybar module and is used by `config-drift-r12.md:25`.
- **The recorded sweep opened the wrong man-page family.**
  `.ufo/evidence/round-12/l2-scout.md:13` records the U7 probe as
  `waybar --help`, `man -w 5 waybar`, `man 5 waybar`, with the unopened lead
  `…/Waybar/blob/0.15.0/man/waybar.5.scd` (the **bar-level** page). But the
  round-3 note had already quoted the **module-level** `waybar-custom(5)` at
  `waybar-walker-semantics.md:137, :161, :192` from the installed man. The
  module page and `src/modules/custom.cpp` were available/known but never
  registered as a source route.
- **Why the gap persisted (inference, high confidence).** It was a
  provenance/route-registration gap, not missing local documentation. The
  round-3 tag legend explicitly exempts MAN rows from anchors — “Every non-MAN
  row carries a `path:line` or a command line”
  (`waybar-walker-semantics.md:10-14`) — so its installed-man quotes had no URL,
  tag, digest, section line or date, and could not satisfy the U7 rubric's
  provenance/reciprocal requirement. The round-12 lead then pointed at a page
  that documents bar configuration, not custom-module output. A tagged
  `waybar-custom(5)` + `custom.cpp` pair is the smallest route that closes it.

## 2. Old MAN claims — exact anchors and limits

Tag contract (`waybar-walker-semantics.md:10-14`): **MAN** = “value from the
locally installed man page for the installed package”; **RUN** = “payload
produced by executing a read-only producer script”. No MAN row carries a page
path, man-db revision, section line or digest.

| Anchor | Claim (class MAN unless stated) | Limit |
|---|---|---|
| `waybar-walker-semantics.md:86-90` | `waybar(5)` config resolution order: `$XDG_CONFIG_HOME/waybar/`, `~/.config/waybar/`, `~/waybar/`, `/etc/xdg/waybar/` | Bar-level page; not opened by S053. No installed-man anchor. |
| `:123` | `waybar-hyprland-workspaces(5)` example `"*": 5`; class hooks `.active/.empty/...` | Different page; unanchored. |
| `:133` | `waybar-clock(5)` default `interval` 60 s | Different page; unanchored. |
| `:137` | `waybar-custom(5)`: “If no interval or signal is defined, it is assumed that the out script loops itself” | Corroborated by tag 0.15.0 at `waybar-custom.5.scd:42`; installed-man digest still absent. |
| `:146` | `waybar(5)` Group Drawers: first module is leader, others get `children-class` | Bar-level page; unanchored. |
| `:161` | “`men 5 waybar-custom` documents JSON fields `text/tooltip/class/percentage` only”; `alt` undocumented | Typo “men”. Tagged man confirms the four-field JSON example (`scd:154`) and contains no `alt` key (only “Alternate Pacman”, `scd:232`); still no installed-man binding. |
| `:192` | `waybar-custom(5)` `signal`: “the number is valid between 1 and N, where SIGRTMIN+N = SIGRTMAX” | Exact at `scd:54-56`; same installed-man caveat. |
| `:415` | “`alt`-keyed `format-icons` … behaviour **INF** from producers/configs” | Correctly inference, not MAN; unchanged by S053. |

**Fresh check against the reserved source (observed).** `curl` of
`https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd`
on 2026-10-20 returned **6656 bytes**, SHA-256
`efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` — equal to
`.ufo/waves/round-16/evidence/source-bindings.json`. The same read confirms
`format-icons` icon selection “based on the set percentage” (`scd:65`), the
four-field JSON example (`scd:154`), newline-separated raw output (`scd:163`),
and `escape` default `false` (`scd:128-130`).

Conclusion: the old custom-page MAN sentences are **not contradicted** by tag
0.15.0; they are **unanchored** and package-relative (`0.15.0-3`). They must not
be retro-labelled as S053 evidence. The new note already states
“installed-binary source equivalence … `[UNK]`”, which is the right boundary.

## 3. Old RUN claims — exact anchors and limits

| Anchor | Claim | Limit |
|---|---|---|
| `waybar-walker-semantics.md:102` | No query verb; reconstruct from a pure-read producer's output (`RUN`) | Honest capability boundary; RUN is producer-side, never GTK text. |
| `:137-140` | Producer payloads: voxtype `{"alt":"","tooltip":""}`; screen-recording `{"text":""}`; idle `{"text":"󱫖","tooltip":"Idle lock disabled","class":"active"}`; DND `{"text":""}` | Payloads measured 2026-10-14; producer execution now forbidden. “⇒ no icon” / “⇒ inactive” are inferences about module selection, not rendered text. |
| `:149` | `ai-usage` RUN payload (cache-only chip) | Same producer-side limit. |
| `:186-190` | `pkill -x -RTMIN+11` delivered (`caught=45`); RTMIN+11 producer path | Signal-delivery measurement, not text. |
| `waybar-walker-plane.md:425-427` | Voxtype payload “renders the module invisible (**RUN**, measured by R3-1; not re-run here)” | **Crosses from payload to renderer state.** The integrated note's renderer boundary hides on empty *raw output*/nonzero exit, or on empty formatted text only with `hide-empty-text`; the recorded payload is non-empty stdout (JSON line) and the config does not set `hide-empty-text`. The invisibility wording is unproven and must not be cited as rendered evidence. |
| `waybar-walker-plane.md:108`, `:331` | `idle.sh` prints text/class; stale-value diagnosis = check the producer | Producer/file-level statements; no render claim. |
| `idle-lock-plane.md:288, :343` | “`[UNK]` whether the currently *rendered* waybar module reflects that state” | Correct boundary; remains open. |
| `config-drift-r12.md:117` | Waybar JSON parse establishes declarations, “not runtime rendering, text …” | Correct boundary; compatible with U7. |

The integrated U7 note's `## Safe observation` says “The old corpus's `MAN`/`RUN`
evidence keeps its dates and scope; this note does not refresh it.” That is
accurate. The one item that needs care is the plane note's
“renders the module invisible” wording: it is an old RUN-derived renderer
inference, and the U7 boundary now makes that class explicit. Adjudicating it
belongs to the `custom.cpp` branches (CustomSource/CustomFailure), not to this
report; I record it as a source-indicated tension, `[INF]`.

## 4. Source-scope collision risks (S053/S054/S055)

Observed integrated state at 05:43: `corpus/SOURCES.md:65-66` holds S053 (docs,
tier A) and S054 (code, tier A), both `mined`, both `used-by`
`corpus/knowledge/waybar-observation-boundaries-r16.md`; `:67` holds S055
(own-work, tier A) whose `used-by` is `corpus/lessons/round-16.md`. The U7 note
exists with `covers: U7`, the four required level-2 headings and `[UNK]` in
`## Unexercised rendering`. `corpus/README.md:41` indexes the note; `:112-117`
records the finite-route supersession; `SOURCES.md:95-98` adds the U7 study
path. My fresh fetch reproduces both binding digests exactly (S054:
`2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f`, 8746 B).

Census mechanics I checked statically (`scripts/sources-census.sh`): URL identity
lowercases the host only and strips scheme, fragment and trailing slash
(`:600-606`); duplicates are keyed by URL+scope (`:643`); `E04` is same URL same
scope without a `supersedes`, `W04` is same URL across scopes. Therefore:

- **R1 — wrong-page substitution is invisible to the census.** The historical
  lead `github.com/Alexays/Waybar/blob/0.15.0/man/waybar.5.scd` is the
  **bar-level** page, a different host+path from S053's
  `raw.githubusercontent.com/…/man/waybar-custom.5.scd`. The census cannot flag
  a future row that cites the bar page as if it covered module output. Keep
  `waybar(5)` and `waybar-custom(5)` as distinct scopes; S053 must not be
  amended to a page it did not open.
- **R2 — S055 can silently break the U7 inverse join.** `measure.py`'s U7 rule
  requires every `mined` row whose `used-by` names the note to appear on the
  note's `source:` line (`inverse = all(...)`, round-16 `measure.py:277-285`),
  and `U7_SOURCES = ('S053','S054')` only. S055 currently names
  `corpus/lessons/round-16.md`, so it is safe. If any later closure/safety edit
  adds the U7 note to S055's `used-by` without adding S055 to the note's
  `source:` line, the join fails and coverage drops to 6/7 with no census error.
- **R3 — `E11` is a commit-order/exact-name trap.** The census checks
  `[ -e "$dir/$path" ]` for every mined `used-by` (`sources-census.sh:567`) and
  the value is one literal path, not a list with fallbacks. Rows and note must
  land in the same commit, with the exact filename
  `corpus/knowledge/waybar-observation-boundaries-r16.md`. Today the note is
  **untracked**; a revision-bound measurement of any commit that contains the
  rows but not the note emits `E11` and yields no U7 join.
- **R4 — id reservation.** S053/S054/S055 are now adjacent. `measure.py` never
  credits S055 to U7; any seat that derives the “next id” from a stale read can
  produce an `E03` duplicate. Only L1 owns `corpus/SOURCES.md`.
- **R5 — tag vs installed package.** S053/S054 bind **tag 0.15.0** bytes. The
  host/runtime claims are `Waybar v0.15.0` with package `0.15.0-3`
  (`waybar-walker-semantics.md:22`, `waybar-walker-plane.md:37`,
  `SKILL.md:22`). The note correctly keeps installed equivalence `[UNK]`. Do not
  let the runtime version string stand in for the tag bytes, and do not attach
  S053 provenance to the installed man page.
- **R6 — README/navigation coupling.** The index has 30 rows for 30 notes and
  the new note appears exactly once as an index row (the prose link at `:112`
  does not match the row regex). Renaming or re-pathing the note breaks both
  `used-by` (R3) and the round-15-style README extraction. The prior “U7 open”
  sentence at `:109` is now superseded by the round-16 bullet at `:111-117`,
  and that supersession is explicitly limited to the finite documentary route;
  the qualification must survive edits.
- **R7 — composite-row regression (round-15 precedent).** S007's composite
  `teaches` could not support U6 and was left queued. Merging S053/S054 into one
  “Waybar docs+code” row, or letting both teach the same sentence, would repeat
  that failure. Their current scopes/teaches are disjoint (documented contract
  vs static code route); preserve the split.
- **R8 — S013 topical overlap.** `S013` cites the gkeep installer's copied
  Waybar module. It is URL-less installer-action evidence used by
  `config-drift-r12.md`; the census cannot collide with it and it must not be
  cited as producer authority.
- **R9 — digest-pointer commit dependency.** The note's `verified-at:` points to
  `.ufo/waves/round-16/evidence/source-bindings.json` rather than inline
  digests. The file exists and matches my fresh fetch, but it is untracked; the
  integration commit must include it or the note's binding pointer dangles
  (the structural counter does not check that file; closure will).

## 5. Confidence and remaining unknowns

- **High confidence:** every file anchor above; the registry/README state at
  05:43; census/measure logic as read statically; the fresh S053/S054 digest and
  byte-count match; the absence of any pre-round U7 `covers:` marker and of any
  Alexays URL in the pre-round registry.
- **Inference:** the route-registration root cause in §1; R2's failure mode
  (derived from the conjunctive inverse rule); the voxtype “invisible” tension
  (source-indicated, `[INF]`, not adjudicated here).
- **Unknown:** installed `waybar 0.15.0-3` man/binary byte equivalence to tag
  0.15.0; full `custom.cpp` branch behaviour (CustomSource/CustomFailure own
  it); final commit contents (L1); tag immutability beyond today's fetch.
- **No edits** outside this report; **no checks executed**; no package, service,
  compositor, input, producer or screenshot probe. No tools installed.

Report: .ufo/waves/round-16/w1/reports/ExistingU7.md
