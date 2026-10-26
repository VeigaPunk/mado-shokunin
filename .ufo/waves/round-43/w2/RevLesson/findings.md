# RevLesson — w2 falsification of `corpus/lessons/round-43.md`

Seat: RevLesson (reviewer, w2). Review target: `corpus/lessons/round-43.md` at the data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`). All checks are
read-only git against that rev unless stated; re-runs are recorded in this seat dir
(`receipt-checker-reruns.txt`, `receipt-nogate-demo.txt`); line numbers cite `git show <rev>:<file>`.
Working-tree `corpus/lessons/round-43.md` is byte-identical to the data-commit blob (`git diff 19597706 HEAD --` empty).

## Findings (by severity; each names what it attacks)

### F1 (major) — the Census section cites two tip receipts that exist nowhere; the claim's tip condition has no receipt
- Attacks: lesson "Census and measurements": "C1 at the data commit: `receipts/c1-after-data.txt`; at the tip:
  `receipts/c1-after-tip.txt`" and the C2 twin "at the tip: `receipts/c2-after-tip.txt`".
- Evidence: `git cat-file -e 19597706:.ufo/waves/round-43/receipts/c1-after-tip.txt` → absent; same for
  `c2-after-tip.txt`; `git log --all --oneline -- <both paths>` → empty; no worktree file
  (`find .ufo/waves/round-43/receipts -name '*after-tip*'` → none). The registered kill rule scores "at the data
  commit **and at the tip**" (registration.md:17-18, registration-v2 target line), so the tip half of both claims is
  asserted with a pointer to bytes never recorded — the exact class M43-3 mines and criterion 79 (QUALITY.md:403)
  forbids.
- Fix text: either run both counters at the round tip and land them as `receipts/c1-after-tip.txt` /
  `receipts/c2-after-tip.txt`, or delete the two "at the tip" clauses and state the tip measurement as open.

### F2 (major) — the Gate paragraph's locator list misstates the entry's bytes for four of ten ids, and M43-1's fix text repeats the stale form
- Attacks: lesson Gate paragraph "Locators the entry carries (computed): … `Hyprland-WindowTarget.cpp:70`, …
  `Hyprland-HyprCtl.cpp:428`, … `host-clients-r43.json:50`, `gkeep-ui-excerpt.py:33`." and M43-1 fix "the entry's
  claim lines carry the counter-computed locator (`<receipt>:<line>`, the list above the ledger)".
- Evidence: the landed entry carries ranges for exactly those four — entry lines 46/54/60/66 read
  `Hyprland-WindowTarget.cpp:70-71`, `Hyprland-HyprCtl.cpp:428-429`, `gkeep-ui-excerpt.py:33-34`,
  `host-clients-r43.json:50-51` (confirmed by `check-locators.py` LOC lines in `receipt-checker-reruns.txt`) —
  which is M43-7's own fix ("the locators became ranges (`:70-71`, `:428-429`, `:33-34`, `:50-51`)"). The list is
  the counter's start-line view (`quote_at` → 70/428/33/50), not "the locators the entry carries".
- Fix text: change the four list items to `Hyprland-WindowTarget.cpp:70-71`, `Hyprland-HyprCtl.cpp:428-429`,
  `host-clients-r43.json:50-51`, `gkeep-ui-excerpt.py:33-34` (or reword the lead-in to "start lines of the locators
  the entry carries"), and reword M43-1's fix to "`<receipt>:<line>[-<line>]`".

### F3 (major) — the Gate paragraph's draft-duplication anecdote is wrong for the clients JSON: no draft quote occurred twice, and there are four 1720x1414 objects, not two
- Attacks: lesson Gate paragraph: "The scribe drafts' first quotes for HyprCtl.cpp and the clients JSON occurred
  twice in their receipts (lines 427/447-448; two 1720x1414 objects), which v2's d+ refuses; the quotes above
  replace them."
- Evidence (counter's own `occurrences` on the drafts vs the pinned receipts):
  - HyprCtl.cpp: TRUE — ScrLessonSkeleton draft S296 occurs at lines 427 and 448; ScrEntryB draft S296 at 427 and
    447 (`w1/ScrLessonSkeleton/round-43-lesson.md:39`, `w1/ScrEntryB/gate-lines.txt`).
  - clients JSON: FALSE — ScrLessonSkeleton draft S298 (`"mapped": true, "class": "Alacritty", "floating": false,`)
    occurs exactly once; ScrEntryB draft S298 (`"floating": false, "size": [ 1720, 1414 ],`) occurs FOUR times
    (lines 6, 21, 36, 51). No draft quote occurred twice.
  - "two 1720x1414 objects": FALSE — all four objects in `host-clients-r43.json` carry `size 1720 1414`; the
    landed S296 row itself says "each mapped true, floating false, size 1720 1414" (corpus/SOURCES.md:245).
- Fix text: "(the HyprCtl draft quote occurred twice, at lines 427 and 447-448; the clients-JSON draft quote
  occurred four times — the dump's four objects all read `size 1720 1414`)".

### F4 (moderate) — M43-4's "Shown able to fail" is cited to a receipt that shows the pass; the fail path was never run before this seat's demo
- Attacks: M43-4: "a lesson with no `## Gate` prints `gates=0 bound=0` for every cited id and `clause=d:0`
  (`quality/counters/c2-r43-gkeep-entry.py:396-446`); measured at the data commit: `receipts/c2-after-data.txt`."
- Evidence: `receipts/c2-after-data.txt` (landed at 2a3707c) records `gates=1 bound=1` per id and
  `clauses=… d:1 … admitted=1`, `admitted=1/1 verdict=TARGET_MET` — the opposite branch. No committed artifact
  showed the fail. This seat ran it (scratch fixture repo: `git archive 19597706` + fetch of the base rev,
  `## Gate` section removed, committed; receipt `receipt-nogate-demo.txt`): intact tree `admitted=1/1` exit 0;
  Gate-less tree prints `clause=d id=… gates=0 bound=0` for all ten ids,
  `clauses=a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:0 i:0 admitted=0`, `admitted=0/1 verdict=TARGET_MISSED`, exit 1 — the
  claimed print is real but was unshown (and the counter source spans :396-446 as cited).
- Fix text: point M43-4's shown-able-to-fail at a committed fail-run receipt (land this seat's demo or an L1
  re-run of the Gate-less fixture) instead of `receipts/c2-after-data.txt`.

### F5 (moderate) — census pointer name wrong: `receipts/census-after.txt` does not exist under that name
- Attacks: lesson "Census after the data commit: `receipts/census-after.txt` (expected: the same W04 ×7 … +
  W01 S277 set as `receipts/census-before.txt`, exit 0)".
- Evidence: no `census-after.txt` at the data commit, at 2a3707c, or on disk; the receipt is
  `receipts/census-after-data.txt` (tracked at 2a3707c), and its bytes match the expectation exactly: W04 S030,
  S042, S045, S097, S119, S120, S121 + W01 S277 + `mado ok …/corpus/SOURCES.md`, `exit=0`.
- Fix text: `receipts/census-after.txt` → `receipts/census-after-data.txt`.

### F6 (moderate) — four present-tense claims about round state that only became true at `2a3707c` (the w1-evidence commit), i.e. the M43-3 class committed as fact
- (a) Intro "LOG.md Round 43 records the change" and M43-1's "the correction entry is the first bullet of LOG.md
  Round 43": at the data commit LOG.md has no Round 43 section (`git show 19597706:LOG.md | grep -c 'Round 43'`
  → 0; last section is Round 42 ending at line 2483). Both land at 2a3707c:2485-2489 — the locator correction is
  indeed the section's first bullet (line 2487) and the 38-seat change is recorded (line 2489).
- (b) M43-6 "this round's verdict is read from the two counters at the data commit (`receipts/c1-after-data.txt`,
  `receipts/c2-after-data.txt`)" and the Census section's data-commit pointers: both receipts are absent at the
  data commit, present at 2a3707c with exactly the claimed bytes (`fixtures=37/37 tool=present verdict=TARGET_MET
  … exit=0`; `admitted=1/1 verdict=TARGET_MET … exit=0`, rev=19597706). Inherent for receipts that measure the
  commit they land in — but the lesson itself uses the honest form for `live-geometry-host.txt` ("untracked at
  this seat's read, landed by the data commit", M43-3 fix) and did not apply it here.
- (c) M43-6 shown-able-to-fail "round 43's `ls .ufo/waves/round-43/w1/*.md | wc -l` → 36 or more": 0 at the data
  commit (no w1 .md files in `git ls-tree -r 19597706 .ufo/waves/round-43/w1/`); 38 at 2a3707c/worktree — the
  discriminating count did not separate anything at the rev the lesson is landed in.
- (d) M43-3 fix parenthetical "the box itself is the report's (`.ufo/reports/round-43/mado.md` SHONEN box 2 points
  at this receipt)": no `.ufo/reports/round-43/` exists at the data commit or at HEAD (`git ls-tree` → only
  `round-1`; `git log --all -- …/round-42/` empty too); the report lands at closure (the spot-check table itself
  marks the row "(closure)").
- Fix text: phrase (a)-(d) as landing with the w1-evidence commit / closure ("recorded at `2a3707c` as LOG.md
  Round 43", "receipts landed at the w1-evidence commit", "count 0 at the data commit, 38 once w1 lands"), or land
  the artifacts with the data commit in future rounds.

### F7 (minor) — M43-3's file enumeration omits `.ufo/waves/round-42/w1-dispatch.json`
- Attacks: M43-3: "at `a62f2e0` the `NO_MATCHING_CLIENT` string appears in `ctl-ref-tool.py.txt`,
  `run-c1-controls.py`, `make-w1-spec.py`, `w1-spec.json`, the counter, and `registration.md`".
- Evidence: `git grep -l NO_MATCHING_CLIENT a62f2e0` → seven files: the six listed **plus**
  `.ufo/waves/round-42/w1-dispatch.json` (1 hit). The conclusion "never in a run receipt" still holds (none of the
  seven is a run receipt).
- Fix text: add `w1-dispatch.json` to the list (or "the w1 spec and dispatch files").

### F8 (minor) — M43-2's fix pointer `registration.md:59` does not carry the definition it claims
- Attacks: M43-2 fix: "`registration.md:59` states the count and its definition once for round 43".
- Evidence: registration.md:59 carries the count (`controls=46`, 48 `ok` lines, `0 of 47`); the definition sentence
  ("Count definition (round-42 closure routed item 3): `controls=` in the header counts … excludes / the two
  anchors …") spans lines 60-61. By the round's own criterion 77 (QUALITY.md:401, "the cited range must contain
  the fact's own identifier") the pointer misses the definition.
- Fix text: `registration.md:59` → `registration.md:59-61`.

## Verified correct (no defect; evidence re-opened at the data commit)

- **All ten GATE sha256s recompute exactly** from `git show 19597706:<receipt> | sha256sum`; all ten fetch pins are
  mode 100644; hashes equal `receipts/fetch-sha256.txt`; the seven Hyprland pins and `host-gkeep.conf` are
  byte-identical to the round-42 blobs (`git ls-tree` blob ids equal); `gkeep-ui-excerpt.py` (3695b788…) and
  `host-clients-r43.json` (21db902e…) are the new captures as stated.
- **All ten GATE quotes pass the v2 counter's own functions** (`quote_at`, `occurrences`, `quote_in_code`): exactly
  one word-bounded occurrence in the own receipt (start lines 16, 426, 56, 10, 70, 19, 428, 4, 50, 33), outside
  comments, absent from every other cited receipt, word counts 3-11 (min S155=3, max S158=11, embedded `""` in the
  S158 quote handled by GATE_RE's greedy `quote="(.+)"`). The Gate paragraph's per-quote claims are true.
- **M43-1**: `LOG.md:2483` at `a62f2e0` carries the wrong locator quote verbatim; round-42 `registration.md:61`
  repeats it; `grep -n GEOMETRIC_GOAL` on the pinned HyprCtl receipt → 426, 427, 428, 447, 448; cited 394-395 and
  412-413 are template fields; `negative:` at RegexMatchEngine 7-8, `FullMatch` at 16; closure routing at
  round-42-verifier-spotcheck.md:83-84 and the round-41 class at round-41-verifier-spotcheck.md:21
  (`PROVINCE.md:75` → 75-76); `da384db4d4848186ade6810a6718f5b24e909bdf` does not resolve ("could not get object
  info", rc 128); `.ufo/reports/` holds only round-1 at every ref. Shown able to fail RE-RUN: `check-locators.py`
  on the base LOG bytes → `LOC …:2483 … verdict=MISS`, `locators=1 miss=1`, exit 1 (my re-run matches
  `w1/ExecLocatorGate/receipt.txt:60` exactly; `:67` corrected-copy `miss=0` and `:72-73` registration MISS
  verified at those lines). Landed `quality/check-locators.py` is byte-identical to the seat deliverable
  (sha256 c1ea52ad…). On the landed entry: `locators=10 miss=0`, exit 0 (M43-7 fix state).
- **M43-2**: closure `:85` quotes the report's "46 controls (absent base, 3 do-nothing, 5 cheats, 37 mutants)";
  `receipts/ctl-c1.txt:1` `controls=46`, `:50` `0 of 47`; 48 `ok` lines, 38 `^ok  M[0-9]` (both greps re-run);
  `run-c1-controls.py:139` prints `controls=%d` as `len(jobs) - 2`; three numbers 45/46/47 name three sets.
- **M43-3**: `git grep -n NO_MATCHING a62f2e0 -- LOG.md` → no hit (re-run); round-42 `registration.md:24` is the
  only tracked assertion; closure `:66` and `:87` match; `receipts/live-geometry-host.txt` is 11 lines with
  `verdict=NO_MATCHING_CLIENT`, `exit=3`, tool sha e3c2e471…, config sha 3726e488…, and IS in the data commit;
  both shown-able-to-fail greps re-run (1 vs 0).
- **M43-5**: round-42 excerpt line 1 claims "lines 446-495"; `wc -l ui.py` → 488; body diff `44d43` with a blank
  line (re-run); round-43 excerpt header says "lines 446-488 (end of file)", 45 lines, and `diff <(tail -n +3 r43)
  <(sed -n '446,$p' ui.py)` is empty (re-run) — the discriminating control holds; r42 full-file sha 48a5c92f…
  confirmed.
- **M43-6**: watchdog.log:1462 reads exactly `2026-10-26T01:03:32-03:00 complete mado round=42; hyaku-inline
  attempt=1`; 29 files under `.ufo/waves/round-42/` with 0 `/w1/.*\.md` at the data commit; closure `:28`, `:88`,
  `:21` and `:57`-`:59` all match their quotes; w1-spec.json `items` length 38 at both 5add5b4 and the data commit.
- **M43-8**: `w1/CritClaimSizing.md:15` "17-line entry"; `c2-4new-receipt.txt` `observed=admitted=1/1 …
  verdict=TARGET_MET`; `w1/CritC2Cheat/run-more.log` X3 `admitted=1/1` (v1); `ctl/v2-forgeries/more-v2.log` X3
  `admitted=0/1 … i:0` (v2) — the shown-able-to-fail pair verifies.
- **Assimilation ledger**: the five decision files exist in the package; r11's sources are S302-S305 (the four
  upstream files ↔ S291-S294) + S310; r8 cites S275 = `lanes/mado/round8/...` and this lane holds 0
  `round8/fetch` paths; observation-route r11 has the single S310 source; r30's 875×600 rests on the config
  comment (quoted at its line 23); r10's §1 carries the "client reports the one it used" inference; r9
  (Window.cpp fetchClass + wiki), r12 (sendWindowSize), r13 (onAck), r15 (journal), r31 (two themes) all match
  their ledger rows; the base grep for rendered-geometry knowledge returns nothing (rc=1).
- **Registry and census numbers**: SOURCES rows 226 → 234 (top S289 at base; S298/S299 absent); knowledge entries
  59 → 60; one README index row + one Frontier bullet (diff verified); the SOURCES diff touches only S155/S158
  used-by cells (exactly one item appended each, tails verified) plus the eight appended rows; S290-S294
  `on-release`, S295-S297 `2027-01-24`; entry header has exactly one `verified-at: 2026-10-26` and `recheck: 90d`;
  the three census lines sit verbatim at entry lines 72-74 and re-derive from host-gkeep.conf:2-4 (float/center/
  size on `^(org.omarchy.gkeep)$`), host-clients-r43.json (4 objects, none floating, all mapped) and
  gkeep-ui-excerpt.py:6,33; `axis-base.txt` matches (59/59, 63/63, 12/12, checked=3 mismatched=0 rev=a35cfdf);
  `c1-before-base.txt` (0/37 absent, exit 1), `c2-v2-before-base.txt` (0/1, exit 1), `census-before.txt`
  (W04 ×7 + W01 S277, exit 0) all as cited; `^## Gate` count 1, `^GATE S` count 10 (lines 34-43, inside the
  section); QUALITY criteria 77-81 landed (77 locator, 78 tally, 79 pointer, 80 excerpt header, 81 closure count).

## Residual risk and verification gaps

- The "prompt §6 item 9" that M43-8 quotes is not a repo artifact at the data commit (no w2 spec committed there);
  the quote is taken on trust. Its substance is corroborated: v1's clause b is the at-least-four-ids count, v2 i+
  requires all ten PINS, and the X3 forgery receipts show the v1/v2 difference.
- M43-7's first-integration-draft run (`CHECK_LOCATORS: locators=10 miss=4`) is cited from an uncommitted draft; no
  committed receipt carries the MISS on the round-43 draft. The checker's teeth are nonetheless demonstrated
  (selftest + this seat's base-LOG MISS re-run) and the fix state (`miss=0` on the landed entry) is re-run here.
- `receipts/axis-base.txt` and the live-host receipt bytes are accepted as pinned; axes were not re-derived and no
  compositor read was taken (none needed).
- No tool installs (python3/git/standard shell only); no pacman; no host-service or compositor mutation; scratch
  under `/fast/scratch/hyaku/mado-r43/RevLesson/` used and deleted; the M43-4 fixture repo was created, fetched
  from (read-only), committed in, and deleted inside scratch only.
