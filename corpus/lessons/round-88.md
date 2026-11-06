# mado round 88 — lessons

Round 88, hyaku run 15, attempt 1. Two frozen claims from `.ufo/waves/round-88/claims-declaration-r88.md`:
C1 capability (mako criteria fields and the upstream boolean grammar, coverage) and C2 operability (include
containment under declared read roots). The stagnation nudge applies (every axis at 10; no capability row since
r82), so C1 is a capability move and C2 a separate operability move.

## Mistakes

**M88-1 — the r87 resolver encoded the manual's `0|1` for style booleans and refused the host's own do-not-disturb lines.**
Class: source-scope — the manual alone is not the behaviour.
Evidence: `~/.local/share/omarchy/default/mako/core.ini:15` (`invisible=true`, section `[mode=do-not-disturb]`) and
`:18` (`invisible=false`, section `[mode=do-not-disturb app-name=notify-send]`); the r87 resolver's refusal text
`expects 0 or 1` at `tools/mado-mako.py` at 24ba2a9ddac21c1211579231e6ee1d98963f9988:114 (the validator is
`:113-114`, `return None if value in ("0", "1") else "expects 0 or 1"`), with the criteria-field refusal at `:271`
and the three-field model at `:75` (`MODELLED_FIELDS = ("app-name", "urgency", "mode")`). Upstream `types.c`
`parse_boolean` (v1.11.0, 19-29) accepts `true`/`false` in any case and the exact strings `1`/`0`, and `config.c`
648-649 parses `invisible` with it — so the host's lines are valid mako and were refused by the lane's own tool.
Captured-by: **none** in round 87 — the r87 case set was authored from the manual alone and never replayed the host
config; the frozen set carries no `invisible` token at all (`python3 -c` count over
`.ufo/waves/round-87/controls/mako-cases-r87.json`: `invisible=true` 0, `invisible=false` 0, `invisible` 0, 22
cases). Round 88 supplies the missing capture: the base tool replayed on the host chain
(`.ufo/waves/round-88/w1/receipt-base-host-config-r88.txt`, base tool sha256
`67a955a5fa06135c2748855b7e452bd3f0792c540002009ec90842ee5c986698`) reports seven refusals, two of them those
lines, and resolves `invisible` to `"0"`.
Fix: C1 accepts the upstream grammar for style booleans (and for the `actionable`/`expiring` criteria fields) while
still printing the effective value in the manual's `0|1` form, and QUALITY criterion 146 requires a resolver claim
to replay the host's own config once.

**M88-2 — a declared stance sentence and a blind-authored case file both carried errors the instruments caught only because the attack seats read draft bytes.**
Class: wording-drift (stance) and schema-drift (case file).
Evidence: the C2 draft said an escaping include is "refused before it is stat'ed or opened"; `os.path.realpath`
lstat/readlinks every component to make the containment test (`.ufo/waves/round-88/w1/R88MCritic.md` C2(c)1). The C1
case file c51 carried the arg key `exiring` (`R88MReviewC1.md` F5); the counter's loader refuses it, so the whole C1 run
would have exited 2.
Captured-by: the C1 counter's `load_cases` (unknown arg → SetupError) for c51 — shown able to fail by
`R88MReviewC1.md` F5; for the stance sentence, **none** in the instruments (no case can observe syscall order); the
critic seat caught it. Fix: the stance now says "refused before its contents are opened (the path is resolved only to
test containment)" in the tool header, the declaration and the knowledge entry; QUALITY 147 makes the frozen bytes,
not the drafts, the scored object, and lists each draft change with its finding (declaration `## Draft revisions`).

**M88-3 — lane scratch was created directly under the shared scratch root, not under the lane's own subtree.**
Class: housekeeping (scope of a writer's scratch).
Evidence: `corpus/lessons/round-85-verifier-spotcheck.md:214-216` (R7): "two L1 probe directories were created
directly under the shared scratch root (`W/receipts/cleanup-r85.json`). Keep lane scratch under the lane's own
subtree; the defect is retained, not hidden."
Captured-by: the round-85 non-author spot-check (2026-11-05), which found the directories and retained the defect
rather than deleting the record.
Fix: the round-88 seat dispatch names each seat's own scratch path (`$HYAKU_SCRATCH/mado-r88/<seat>/`, with
`trap 'rm -rf -- "$S"' EXIT`) and requires a seat that leaves its scratch behind to report it as a defect. This is
a dispatch-level fix, not a new QUALITY number; no criterion in `corpus/QUALITY.md` covers scratch-root ownership
(`grep -niE 'shared scratch|probe director' corpus/QUALITY.md` → 0 lines; criterion 34 governs result paths and
prior-result removal, criterion 98 the size bound, neither the root).

## Wave findings routed (instruments frozen or named as limits)

| finding | seat | severity | disposition |
|---|---|---|---|
| C1 counter: absent anchor scored as a miss | R88MCritic | medium | fixed before the freeze (SetupError) |
| C1 counter: carried r87 file unpinned | R88MCritic | medium | fixed (`--expect-r87-cases-sha256`) |
| C1: no ignored-inputs control; base-tool is CLI-contaminated | R88MCritic, R88MConnector | medium | fixed (`inputs-ignored` control, per-case reasons) |
| urgency `high`/casefold refused though upstream accepts | R88MCritic | low | fixed (M20, M21, c60, c61) |
| repeated criteria field refused, upstream last-wins | R88MReviewC1 F1 | high | fixed (M22, c62) |
| c51 arg key typo | R88MReviewC1 F5 | high | fixed by the scout before yield |
| crashing mutant counted killed | R88MReviewC2 F1 | medium | fixed (crash-is-not-a-kill, both counters) |
| `..` after a symlinked dir; final-component check | R88MReviewC2 F2, F3 | medium | fixed (K6, K7, k18, k19) |
| untested escape classes | R88MReviewC2 F4 | medium | fixed (k20–k23) |
| NUL byte crash; `~//`; trailing `/`; relative roots | R88MReviewC2 F5, F7, F8 | low | fixed in the tool (NUL measured by a selftest, not by a frozen case) |
| TOCTOU, hardlink, bind mount | R88MReviewC2 F6 | low | named limits |
| symlinked read root ambiguous | R88MReviewC2 F10 | low | ruled (roots resolved), k24 |
| counter selftests miss predicate mutations | R88MMutTester | medium | fixed (predicate table, in-process run(), separate guards) |
| tool selftest misses M16 | R88MExecSelftest F1 | low | fixed (selftest check added) |

## Gate

### Registry rows (S494, S495) — opened 2026-11-06

- S494 — upstream mako v1.11.0 source, tag-pinned: `criteria.c`
  sha256 `22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c`, `types.c`
  sha256 `c2f3398d45877c10ae94a61634629c22b1c4c472b526a4963d45f7981c4734de`, `config.c`
  sha256 `94c3a4e7b0bc7304dd9011c1e44d91cfffe417fe03aa3fa864205204f968ca12`, each fetched from
  `https://raw.githubusercontent.com/emersion/mako/v1.11.0/<file>`. Tier: tag-pinned upstream source of the
  installed version (criterion 27: tag pin, not an alias).
  Located quote (criteria.c:110-111, 13 words, re-read by the L1 in its own fetch, sha256 `22767742…`): `if (spec.summary && strcmp(criteria->summary, notif->summary) != 0) {`. Access date 2026-11-06; tag v1.11.0 → commit `91c6b799855762ad1eb8b4498967c270a339be0c`.
- S495 — `path_resolution(7)`, Linux man-pages 6.19 (`.TH` line 6), locator
  `/usr/share/man/man7/path_resolution.7.gz`, container sha256
  `2a21ab674e6f2c51f74c15b3709e2155873734cf867f8ffd2d1b3dec14d41077`, decompressed text sha256
  `2072681115cb012523b968eb243c5ba306ac68fca7f92d9e378949108921dc12`. Tier A (installed documentation).
  Located quote (text line 145, 11 words, re-read by the L1 with `zcat | nl -ba`): `One cannot walk up past the root: "/.." is the same as "/".` Access date 2026-11-06. (The scout's lines 77-80 quote is 25 words, not the 19 its report says — still within the bound.)

### Candidates considered (round 88)

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/mako-fields-containment-r88.md` (fields, boolean grammar, containment) | **admit** | every rule cites S493/S494/S495 at a line; C1 and C2 TARGET_MET at frozen bytes | a source line that contradicts a stated rule |
| `summary~` / `body~` modelled with Python `re` | **reject** | manual 450/456 name POSIX ERE; `re` answers a different question, so the resolver refuses | a resolver that implements POSIX ERE |
| containment as a mako rule | **reject** | manual L45-48 states no boundary and `config.c` 545-548 opens any absolute path; the stance is the lane's | a manual line stating a boundary |

### Spot-check

Pending: the non-author closure is the operator-dispatched verifier (LEARNING.md). This lesson records no
spot-check result.

### Census

- Round start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0, 428 rows (`.ufo/waves/round-88/receipts/census-start-r88.txt`).
- Round end: same command → see `.ufo/waves/round-88/receipts/census-end-r88.txt` (430 rows; S494, S495 added; status `mined` for both, used-by this entry and this lesson).
- Measurements: C1 `TARGET_MET 62/62, 22/22 killed` (`receipts/c1-measured-A-r88.txt`); C2 `TARGET_MET 26/26, 7/7 killed` (`receipts/c2-measured-B-r88.txt`).

## Considerthese

`considerthese/2026-11-04.md` proposal 5 — "Look for coverage gaps from João's own desktop, not from the lane's
backlog." — proposes "A one-time read of João's Omarchy `hypr`, `waybar` and menu config (read-only, with his
consent) would let me name desktop surfaces nothing in the corpus covers yet, such as the portals, notifications,
screen sharing and clipboard."

This round acts on the notifications half of that proposal, within the credential-material rule (the mako config
chain only): C1's host-config case is the host's own `core.ini` replayed through the resolver, and the round-88
base-tool replay (`receipt-base-host-config-r88.txt`) is what turned the r87 refusal into a visible defect. The
portals, screen-sharing and clipboard surfaces remain uncovered; this round names them and does not claim them.

## Domain share

New artifacts this round: one knowledge entry (`mako-fields-containment-r88.md`, desktop-facing), one tool change
(`tools/mado-mako.py`, desktop-facing: reads the mako config), two record counters (lane-internal).
Desktop-facing: 2 of 4 (the entry and the tool; the two counters are lane-internal).
Command: `git diff --name-only --diff-filter=AM 24ba2a9..HEAD -- corpus/knowledge tools quality/counters | wc -l` → 4.
