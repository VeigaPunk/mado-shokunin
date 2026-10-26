# w1/ScrReadme — `corpus/README.md` index row + Frontier subsection (round 45)

Seat: `ScrReadme` (scribe, leaf; no subagents, no background jobs). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Freeze read first: `.ufo/waves/round-45/registration.md` (freeze `22a8dedd02f507689c567777e0f20b5e645c8ce0`, base
`0c89478af821a6424c9ac922eafe02e39630cf4f`). Entry under index: `corpus/knowledge/hyprland-monitor-rule-r45.md`
(L1 draft `.ufo/waves/round-45/l1-draft/entry.md`, 90 lines, census line at `:72`).

**Status: DONE.** Two paste-ready blocks drafted; no tracked lane file edited; scratch clone removed.

## Behavior (what this seat produced)

Draft at `.ufo/waves/round-45/w1/ScrReadme/readme.md`:

1. **Index row** (one line, three cells) to paste after `corpus/README.md:72`, the round-44 row — the text
   `build-pos.py:98` inserts into the positive control is a placeholder
   (`| \`knowledge/hyprland-monitor-rule-r45.md\` (MADO-R45-1, round 45) | draft | S302-S310 |`) and this row replaces
   its cells 2 and 3 while keeping the prefix the frozen predicate reads. Cell 2 states the monitor-rule chain (line
   grammar and eight-key loop with whole-line rejection, 60 Hz default, erase-then-append and reverse search with the
   empty-selector fallback, `desc:` on short/long description, 1 px / 1 Hz closeness, 1/120 scale search, explicit
   positions before `auto`, five-decimal `refreshRate` and the `all` argument, the wiki's `sdr_eotf` divergence), the
   tool and its verdict/exit vocabulary, and the host reading (AGREE/OK, 99.997 Hz against a declared 100). Cell 3 is
   the bare id range `S302-S310` — the newest-row convention (`corpus/README.md:70`, `:72`).
2. **Frontier subsection** `### Round-45 monitor-rule route`, one bullet, appended after current line 320 (the round-44
   tail subsection; file ends there). It states the relation to the two held bullets it touches —
   `corpus/README.md:131` ("output-management behavior") and `:137-139` ("runtime state agreement") — without rewriting
   either (append-only convention, round-21 correction at `:193-195` as the model), carries a locator per factual
   clause, and names what stays open: colour/HDR rendering and physical accuracy (round-14 item, unchanged),
   output-management *apply* (`Hyprland-MonitorRuleManager.cpp:45-84`), `monitorv2` field parsing beyond `sdr_eotf`,
   a `desc:` selector that matches only the long description (the dump carries the short description only), and
   runtime `hyprctl keyword` monitor overrides — with the entry's §6 UNK paragraph as the reason nothing was applied.

Axes named (godspeed) and how they moved: **row-shape conformance** (exactly one column-0 prefix row, three cells, no
inner pipe, bare id range) — verified against the frozen predicate and the lane's two index gates; **claim truth**
(every clause traced to a pin line recomputed by `grep -n`, 34 anchors re-asserted by script); **Frontier honesty**
(moves the read half only, names four spec items plus the runtime-override case, leaves held bullets untouched);
**integration friction** (numbered insertion points, no serials / descriptions / window titles / process tables — the
row names no serial field, checked).

## Gates (run; receipts in the seat dir)

| gate | command | result |
|---|---|---|
| Locator truth | `python3 -I check-locators.py` (seat dir) | `SUMMARY failures=0`; 34 locator PASS lines (42 PASS total with the shape checks), each cited `file:line` re-read from `.ufo/waves/round-45/fetch/` and required to contain its token (`locators-check.txt`) |
| Row shape | same script | PASS: exactly one row occurrence, 3 cells, no inner pipe, `source cell = 'S302-S310'`, clause-f prefix matches |
| Lane index completeness | `python3 -I quality/check-index.py --repo D --rev HEAD` | `MADO_INDEX: rev=HEAD indexed=62/62 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0 |
| Lane index-row fidelity | `python3 -I quality/check-index-rows.py --repo D --rev HEAD` | `MADO_INDEX_ROWS: rev=HEAD rows=62 errors=0 warns=3`, exit 0 — the three warns are pre-existing `cited-glob-nomatch` lines on `window-rule-effects-getprop.md`, `config-drift-r12.md`, `rule-attribution-r24.md`; **no** `holds-no-overlap` warn on the new row, i.e. the Holds cell shares no >=5-word sequence with the note |
| Frozen C2 predicate | `python3 -I quality/counters/c2-r45-monitor-entry.py --repo D --rev HEAD --base 0c89478a…` | `PRED-C2-r45: admitted=1/1 verdict=TARGET_MET rev=7e6e2ed41956b54dcbc00aa07828715a4d2bf725`, exit 0; `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1`; `clause=j` reports all seventeen surfaces `cited=1` |

`D` = a scratch clone of the freeze under `/fast/scratch/hyaku/mado-r45/ScrReadme/clone` (removed after the run):
`git clone -q --shared <lane> "$D"`, `git -C "$D" rev-parse --show-toplevel` asserted equal to `$D`, `checkout
--detach 22a8dedd…`, `python3 -I .ufo/waves/round-45/l1-draft/build-pos.py "$D"`, the row replaced at README line 73,
`git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit`. The clone revision is a gate fixture, not
evidence: the receipt is `ScrReadme/gate-clone.txt`.

Not run (deliberately): the C1 counter, the tool, the tool's selftest, any host or compositor command. No tracked lane
file, no index, no counter was modified. No tool was installed or updated, so no channel/version entry applies.

## Touched surfaces

- New (mine): `.ufo/waves/round-45/w1/ScrReadme.md` (this report) and the seat dir
  `.ufo/waves/round-45/w1/ScrReadme/` — `readme.md` (draft), `check-locators.py`, `locators.txt`,
  `locators-check.txt`, `gate-clone.txt`.
- Read only: the freeze registration, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/`,
  `.ufo/waves/round-45/l1-draft/{entry.md,build-pos.py,mado-monitors.py}`, `.ufo/waves/round-45/fetch/*`,
  `receipts/live-monitors-host-l1.txt`, `quality/{check-index.py,check-index-rows.py}`,
  `quality/counters/c2-r45-monitor-entry.py`, `.ufo/waves/round-45/w1/ScoutFrontier/map.md`.
- No host config, no `pacman`, no compositor verb; no serial, description, title or listing committed.

## Findings

1. **The row passes the predicate and both lane index gates** (above). Supports C2 clause f, and shows the integrator
   can replace `build-pos.py`'s placeholder with this row without touching any other clause — the placeholder itself
   is shape-legal but says `draft`, so leaving it in place would ship a row that claims nothing.
2. **The Holds cell is not a quote of the note.** `check-index-rows.py` raised no `holds-no-overlap` warn for the row
   while raising three unrelated pre-existing warns on other rows — i.e. no >=5-word sequence is shared with
   `corpus/knowledge/hyprland-monitor-rule-r45.md`. That attacks the `ScribeRowAccuracy` F1 failure mode (a row
   overclaiming or echoing its note) for this row.
3. **One self-caught citation error.** My first draft cited the census line as `entry.md:76`; `grep -n` puts
   `hyprland monitor-rule default_refresh=60 … line_keys=8` at `entry.md:72`. Corrected and re-verified. Reported
   because a citation typed from reading order is exactly the defect class the lane has been routing.
4. **Frontier form is independently agreed.** `ScoutFrontier/map.md` §2 names the same insertion (after `:320`), the
   same subsection form (r43/r44 tail subsections), the same two held phrases (`:131`, `:137-139`) and the same
   do-not-rewrite rule; this draft follows it. Divergence: the scout's list also carries "hotplug" and "`keyword
   monitor` runtime overrides" as open; only the `keyword` case is grounded in the entry (§6 UNK, `Limits` 1), so the
   bullet names that one and not hotplug.
5. **Held-row pointer note (not a claim of this seat).** `ScoutFrontier` §1 records that `SKILL.md:179` holds the
   "monitor 99.997 vs 100" class as `[INF]` while this round's 1 Hz tolerance is the sourced replacement. Nothing in
   my blocks edits that row; the row's Holds cell states the host reading as the receipt's AGREE/OK, not as a
   reclassification of the held `[INF]`.

## Out of scope (routed, not done here)

- Applying any of this: `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `corpus/SOURCES.md` and the lesson are the L1's
  integration; this seat wrote drafts only.
- The entry body, the registry rows S302-S310, the lesson `Gate` block and the tool: other seats / the L1.
- Round-44 closure items D1-D7 and considerthese proposal 1: not this seat's; no receipts were rewritten and no
  privacy check is claimed.

## Artifacts

| path (relative to the lane) | bytes | what |
|---|---|---|
| `.ufo/waves/round-45/w1/ScrReadme/readme.md` | 13181 | the two paste-ready blocks + phrase→ground table + limits |
| `.ufo/waves/round-45/w1/ScrReadme/locators.txt` | 2944 | `grep -n` output for every cited locator |
| `.ufo/waves/round-45/w1/ScrReadme/check-locators.py` | 5366 | the checker (read-only; re-reads pins and the draft) |
| `.ufo/waves/round-45/w1/ScrReadme/locators-check.txt` | 2781 | its output, `SUMMARY failures=0` |
| `.ufo/waves/round-45/w1/ScrReadme/gate-clone.txt` | 4482 | index gates + C2 counter on the scratch clone |
| `.ufo/waves/round-45/w1/ScrReadme.md` | this file | seat report |

Report: `.ufo/waves/round-45/w1/ScrReadme.md`
