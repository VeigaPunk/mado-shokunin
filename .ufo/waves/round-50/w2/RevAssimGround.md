# RevAssimGround — round-50 w2 falsification review

Seat: RevAssimGround (leaf). Scope: the Assimilation section of `corpus/lessons/round-50.md` (lines 46-62 at the
freeze) vs ground truth. Attack revision: `b4a79843cc2545bbe800db9322e58f6e00436629`; data commit `906178b6…`.
Lesson bytes at the data commit hash to the freeze table value (`sha256 = e7cd29620aeed655f54fa3401b901acba8fe3f47ffdb4b5e9d6f3a62e20be794`, verified via `git show 906178b6:corpus/lessons/round-50.md | sha256sum`).

**Verdict: the lesson's assimilation records SURVIVE all four falsification checks. No actionable defect found.**
One minor omission noted under (a) — not a false claim.

## (a) considerthese proposal 1 vs proposal 6 — SUPPORTS the lesson

- `considerthese/2026-10-26.md` proposal 1 is indeed the privacy-receipt check: numbered proposal 1 reads
  "Add a privacy check on new receipts." (file, proposals list item 1). The lesson's parenthetical
  "(a privacy check on new receipts)" (round-50.md:48) matches.
- Proposal 6 ("Lead with round-level outcomes, not counter internals") was landed in round 48 as QUALITY 99:
  `corpus/QUALITY.md:543` names `(proposal: considerthese/2026-10-26.md proposal 6, 2026-10-26 — "Lead with
  round-level outcomes, not counter internals")` with instrument `quality/check-round-outcome-first.py`;
  `corpus/lessons/round-48.md:186-188,286,363` records the landing. Verified.
- The round-50 lesson admits **only** proposal 1 (round-50.md:48) and never mentions proposal 6 — no re-credit.
  The Gate/Mistakes sections likewise cite no proposal-6 outcome. SUPPORTS.
- Minor observation (not a defect): `corpus/lessons/round-45.md:81` already mapped proposal 1 →
  `quality/check-session-material.py` + QUALITY 85 (gate v1/v2 era). The round-50 lesson's admit says "grounded
  this round through C2" without that history; the claim is still true (gate v3 is the new grounding) and
  `w1/ScoutAssimR50.md` carries the same framing, but the sentence omits the prior partial mapping.

## (b) `merge/mado/MERGE-REPORT.md` theme scan — SUPPORTS the lesson

Read-only grep of `/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md`:

| keyword | count in report | count in staged entry names (69 files under `knowledge/` + `amendments/`) |
|---|---|---|
| hyprland | 5 | 1 |
| bind | 2 | 1 |
| keysym | 0 | 0 |
| keymap | 0 | 0 |
| privacy | 0 | 0 |
| session-material | 0 | 0 |

Every report hit is an unrelated description, matching the seat's "only unrelated 'binding' descriptions"
(`w1/ScoutAssimR50.md`): `ipc-contract-r25.md` (IPC sockets), `waybar-module-text-route-r25.md` (bar text route),
`two-literature-drift-r26.md` (ArchWiki coverage), `host-bar-and-idle-binding-r26.md` (bar/idle stack binding),
`focus-grab-protocol-live-on-host-r14.md` ("the portal that saw it does not bind it"), `chinese-hyprland-window-rules-r16.md`
(window rules), and one S276 SOURCES row quoting "Hyprland". The two staged entry-name hits
(`host-bar-and-idle-binding-r26.md`, `chinese-hyprland-window-rules-r16.md`) are bar/idle and window-rule themes,
not keybind/keysym/keymap. No staged theme matches C1 or C2 — the lesson's Reject sentence (round-50.md:53-55) holds.

## (c) Id-collision guard numbers — SUPPORTS the lesson

Artifacts under `w1/ScoutAssimR50/assimilation/` (wc -l): `reg-ids` = **288**, `staged-ids` = **147**,
`collisions` = **94** — exactly the lesson's "lane registry ids 288, staged ids 147, intersection 94"
(round-50.md:56-57). Guard fixture files: `guard-registry` carries the indented row `| S002 | fixture |`,
`guard-reg-ids`/`guard-staged-ids`/`guard-collisions` each hold the single id S002 → reg=1, staged=1, collisions=1,
matching "the indented-row fixture (`  | S002 |`) produced a nonempty `collisions` file, proving the 0-3-space
pattern" (round-50.md:57-58).
"reg 288 → now 300": `git show b4a79843:corpus/SOURCES.md | grep -cE '^\| S[0-9]+ '` = **300** = 288 + 12
(rows S352-S363), corroborating "No staged row was appended" (round-50.md:58): the only registry growth is the
round-50 rows, none from the staged package.

## (d) Quarantine pending verdicts — SUPPORTS the lesson

- `w1/ScoutAssimR50/assimilation/quarantine-slice`: **13 rows**, all carrying S-ids; 6 `payload-absent`
  (S189, S195, S201, S205, S224, S228) + 7 unchecked prose classes (S199, S200, S209, S222, S223, S225, S235:
  "source could not be fetched, so no quote was checked" ×2, "gate block named no locator, so no quote was
  checked" ×5). Matches the lesson (round-50.md:59-60) row for row, id for id.
- The lesson claims **no** verdicts: "Hand-check verdicts per row are wave-w2 work
  (`.ufo/waves/round-50/w2/ScoutAssimQuarantine/`); until they land, adoption from the register stays closed"
  (round-50.md:61-62). That seat's report currently reads "Status: IN PROGRESS … Verdicts land in
  `.ufo/waves/round-50/w2/ScoutAssimQuarantine/quarantine-verdicts.md`" — so no lesson sentence claims a verdict
  the seat's file does not carry. The pending framing was true at freeze (906178b6 precedes w2) and remains true now.
- "Nothing from the register was appended this round" (round-50.md:62) is consistent with the registry arithmetic
  in (c): 300 = 288 + 12 round-50 rows only.

## Evidence base (all read-only; nothing written outside this seat)

- `considerthese/2026-10-26.md` (proposals 1 and 6, located); `corpus/QUALITY.md:543` (criterion 99);
  `corpus/lessons/round-48.md:186-188,286,363`; `corpus/lessons/round-45.md:81` (prior proposal-1 mapping).
- `/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md` grep counts above (read-only; no campaign tool run there).
- `.ufo/waves/round-50/w1/ScoutAssimR50.md` + `assimilation/{reg-ids,staged-ids,collisions,guard-*,quarantine-slice}`.
- `.ufo/waves/round-50/w2/ScoutAssimQuarantine.md` (IN PROGRESS status line).
- `git show` on the lane at `906178b6` (lesson hash) and `b4a79843` (registry row count = 300).

Deliverable: this file only. Scratch (`/fast/scratch/hyaku/mado-r50/RevAssimGround/`) contained a derived
staged-filename list used for the (b) name grep; it was deleted after use. No tools installed; no host state read
beyond the read-only compositor-free artifacts above.
