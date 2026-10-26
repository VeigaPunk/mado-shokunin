# RevLesson — review of `corpus/lessons/round-44.md` (round 44, wave w2, seat RevLesson-2)

Method: read-only `git` (rev-parse/log/ls-tree/grep/show at pinned revs), `grep`/`awk` on lane files, one re-run of
`quality/ratio-domain-meta.py` (read-only counter). No LSP device is mounted in this seat, so all checks are text-level;
nothing below is semantic-proof beyond the quoted bytes. Tools installed: **none**. Scratch `/fast/scratch/hyaku/mado-r44/RevLesson-2/`
created empty, deleted before this report (nothing to cite from it). Lane-relative note: `assimilation/…` in the lesson resolves to
`.ufo/waves/round-44/assimilation/…`; `merge/mado/…` resolves only inside the shokuknow checkout
(`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/`) — convention carried from round 43, noted, not attacked.

## Findings

### MODERATE

**R1 — The three "tip" receipts the lesson names do not exist, and no committed counter/axis line names the published tip.**
Attacks: Census bullets `corpus/lessons/round-44.md:232-233` (`receipts/c1-after-tip.txt`, `receipts/c2-after-tip.txt`) and the M44-7
fix `:176` (`receipts/axis-tip.txt`, "committed with the round's last commit").
Evidence: `git ls-tree -r --name-only 290cddea .ufo/waves/round-44/receipts/` lists 23 files, none named `*after-tip*` or `axis-tip*`;
`git log --all --oneline -- '*axis-tip*'` → empty. The newest committed lines are at the data commit: `receipts/c1-after-data.txt:53`
and `receipts/c2-after-data.txt:29` end `rev=e46789213830597348fe96a351ae004d10587385`; `receipts/axis-data.txt:4` the same. The
published tip is `290cddea` ("after-data receipts"), so `git grep -n 'MADO_AXIS:' HEAD -- .ufo/waves/round-44/receipts/` shows no line
for the tip rev — the exact shape M44-7 attacked in round 43 (receipts stop one commit short of the tip). Registration-v2's Target says
"at the data commit and at the tip"; the after-data receipts satisfy the data commit (which was the tip when they were produced), but the
round then moved the tip without re-running anything.
Correction (exact): read `:232-233` as "At the data commit `e4678921` (the tip at counter-run time; no separate tip receipts exist):
`receipts/c1-after-data.txt`, `receipts/c2-after-data.txt`"; read `:176` as "`receipts/axis-data.txt`, committed with the after-data
receipts commit"; and record the open residual: no axis/counter receipt records `290cddea`.

**R2 — M44-2 misattributes its own evidence: the S293 teaches cell restates the refuted premise, it does not contradict it.**
Attacks: `corpus/lessons/round-44.md:119-121` — "the row's own teaches cell contradicts it … while the same row's teaches cell and
`Hyprland-WindowTarget.cpp:70-71` show the target writing `m_box.logicalBox` derived from the rule's `static_.size`".
Evidence: the S293 row (`corpus/SOURCES.md:242`), cells split by ` | `: the cell showing the hand-off is the **locations** cell
("`:69-78` the floating branch hands the box to the window"); the **teaches** cell reads "The desired geometry is the client's own
geometry clamped by min and max size … so the client's request is only the layout's input" — it reasserts the client-as-input premise.
`Hyprland-WindowTarget.cpp:70-71` (`m_window->setBox(m_box.logicalBox);`) and `Hyprland-DefaultFloatingAlgorithm.cpp:56`
(`calculateExpression(*…static_.size)`) do resolve.
Correction (exact): "Evidence: `corpus/SOURCES.md:242` titles S293 'the client's request as input', while the same row's locations cell
(':69-78 the floating branch hands the box to the window') and `.ufo/waves/round-43/fetch/Hyprland-WindowTarget.cpp:70-71` show the
target writing `m_box.logicalBox` derived from the rule's `static_.size` (`.ufo/waves/round-43/fetch/Hyprland-DefaultFloatingAlgorithm.cpp:56`)
— the client is the recipient, not the input; the row's teaches cell ('the client's request is only the layout's input') restates the
superseded premise rather than contradicting it, which widens the D2 supersession scope by one cell."

### MINOR

**R3 — Off-by-one locator: the seat-count sentence is `registration.md:6`, not `:5`.** Attacks: closure item 5 (`:97`) and E3's fix
(`:152`), both saying "`registration.md:5` of this round records seat counts from `*-results.json`". Evidence:
`grep -n 'the seat counts are recorded' .ufo/waves/round-44/registration.md` → 6; line 5 carries the host versions and the wave Shape.
Round-43's own `registration.md:5` ("37 seats") is correct as cited (`:149`, `:206`). Correction: read `:6` in both places — the same
typed-locator class E4 documents, one layer down.

**R4 — The Census names a `clause=h` line that is not in the receipt.** Attacks: `:240` — "The counter's `clause=h` and the twelve
`clause=j` lines are in `receipts/c2-after-data.txt`". Evidence: the receipt holds `clause=c`×5, `clause=d`×5, `clause=g`×5,
`clause=j`×12 and one summary line; `grep -c 'clause=h' .ufo/waves/round-44/receipts/c2-after-data.txt` → 0; `h` appears only inside the
summary `clauses=a:1 … h:1 … j:1` (`:28`). Correction: "the summary line's `h:1` and the twelve `clause=j` lines are in
`receipts/c2-after-data.txt`".

**R5 — The Spot-check table's new-row grep cannot match anything.** Attacks: `:221` — `grep -nE '^\| S(29[89]\|30[01])\b'
corpus/SOURCES.md`. In ERE `\|` is a literal pipe, so the group matches `298|`/`299|`/`|30…` and a row shaped `| S298 | …` never
matches; run at the tip it prints nothing (count 0, exit 1) — a spot-check that cannot fire, misreadable as "0 problems".
Correction: `grep -nE '^\| S(29[89]|30[01])\b' corpus/SOURCES.md` (verified by hand to return `:247`–`:250`). The neighbouring bare name
`sources-census.sh` resolves only as a fleet script (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`), not from the lane — note only.

**R6 — The Census pairs superseded v1 before-receipts with v2 after-receipts.** Attacks: `:231` (C1 base cited as
`receipts/c1-before-base.txt`, `fixtures=12/26`) and `:233` (C2 base cited as `receipts/c2-before-base.txt`). Evidence: those are the
**v1** counters' base runs (`PRED-C1-r44: fixtures=12/26 … exit=1`; `PRED-C2-r44 … admitted=0`), while the claims' rule is
PRED-C1/C2-r44-**v2**, whose own before-receipts are `receipts/c1-v2-before-base.txt` (`fixtures=11/26 … exit=1`,
`clauses=a:1 b:0 b4:0 b5:0 e:1 g:1 r:1`) and `receipts/c2-v2-before-base.txt`. Both cited files resolve and both exit 1, so nothing is
false — but the before→after line the Census records crosses the supersession the lesson itself declares only for the after side
(`:232`). Correction: cite the two `-v2-before-base` files as the predicates' before-states; keep the v1 receipts as superseded history.

## Verified (no action) — every check below was executed at this seat

- **Header**: revs `6a1a9052`/`e4678921`/tip `290cddea` resolve; freeze hashes are commit ids (`git rev-parse` full = the 40-hex
  strings at `:5-7`); commit order freeze → w1-spec → v2-freeze → data is correct in `git log`; `w1-results.json` has `seats:38`,
  `results:38`; lesson structure 1 `## Gate`, 5 `GATE S`, 1 ADMIT, 4 REFUSE, 9 `**M44-`.
- **Gate**: all five pin sha256 byte-equal to `receipts/fetch-sha256.txt` (recomputed), modes 100644, committed at the freeze
  `e2289516`; each GATE quote located in its own pin (`Hyprland-Window.cpp:1687`, `Hyprland-XDGShell.cpp:455`, `xdg-shell.xml:1150`
  — sentence wraps to `:1151`, prefix-quote is faithful — `gdktoplevel-wayland.c:681`, `gkeep-ui.py:475-476`) and absent from the
  other four pins; the entry's locators equal the counter receipt's `clause=g` lines exactly (`c2-after-data.txt:11-15`).
  `fetch-c1/` three pins hashed; `corpus/SOURCES.md` cites none of them (grep → 0). The 0 ADMIT-side package files exist in the
  shokuknow checkout; r11:15's S310 scope line reads "rule lines, app request, client count" — exactly the three things M44-1/E2 claim.
- **Ledger**: round-43 REFUSE lines at `corpus/lessons/round-43.md:46/:47/:48` as claimed; `:74` re-grounds S310 as "S295/S296";
  `.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt:232` carries the `windowrule = size 875 600, match:tag floating-window` line;
  `git ls-tree -r --name-only HEAD | grep -c 'lanes/mado/round1[345]/fetch'` → 0 (r13/r14/r15 refusal ground); no genuine round-9
  receipt paths in the lane (only unrelated fixture/plan name collisions); S297 row byte-identical base→tip (`diff` → empty).
- **Registry log**: `corpus/SOURCES.md:176` is S164; `diff` of the S164 line base→tip shows only the `used-by` cell extended
  (cells 1-10 byte-equal); new rows at `:247-:250`, each `mined`/`2026-10-26`/`on-release` with `used-by` naming the entry; rows
  234→238 and knowledge 60→61 (recounted at both revs); base's top id S297; README index row (`corpus/README.md:72`) and Frontier
  section (`:304`) present; `.ufo/waves/round-44/assimilation/id-guard.md` (collisions 42, S203..S297; the indented-row pattern
  result) and `renumber-map.tsv` (S311→S164, S312→S301) match the lesson verbatim; `census-before.txt` == `census-after-data.txt`
  (W04 ×7 named ids + W01 S277, exit 0).
- **Closure items 1-9**: `corpus/lessons/round-43-verifier-spotcheck.md:97/:100/:102/:104/:106/:107-108/:109/:110/:111` all carry
  what the lesson reports, including the D1 routing "`round-43.md:75`" (E4's target) and the round-41 open list; w1/ScrSupersedeRows
  documents the E04/W04 supersession economics quoted in closure item 2; round-44 `registration.md:6` does record seat counts from
  `*-results.json` (locator itself is R3).
- **M44-1..9 evidence**: `:46` refusal text and `GeometricMovableAnimated.cpp:19` / `HyprCtl.cpp:427-429` (M44-1, E1);
  S293 title "the client's request as input" grep-count 1, `WindowTarget.cpp:70-71`, `DefaultFloatingAlgorithm.cpp:56` (M44-2 — but
  see R2); SKILL.md base `:276` text and `read TILED as "not floating" only` counts 0/1/1 at base/data/tip, pseudo-size block at the
  round-44 pin `Hyprland-Window.cpp:2402-2408` (M44-3); `ls-tree 1959770` → 0 files vs tip → 2, r43 entry `:66`, `20-observation.txt:24`
  citing `gkeep-shm.c:156-164` with the true block `:150-159` (M44-4); `registration.md:5` "37 seats", spec `items:38`, SCORECARD
  `:2548` "Mistakes M43-1..8" (base and data commits), `grep -c '^\*\*M43-'` → 9, and the landed erratum in SCORECARD Round 44
  (`:2583`) (M44-5/E3); closure `:107-108` numbers, `ctl-c1.txt:2/:17/:18` (REF 26/26, K13 b:0/b4:0, verdict 0 of 15),
  `ctl-c2.txt:5` (0 of 3, no positive control), w1/ExecC1ExtraMutants "51 … 20 reach TARGET_MET … true equivalence",
  w1/MutC1CounterGates floor-50 matrix (M44-6); tip `5846662` exists, `git grep 'MADO_AXIS:' 5846662 -- …ExecHarmTip/logs/` → the
  four lines at base/data/2a3707c/a47efeb, none at the tip rev (M44-7 — but see R1 for the fix side); `pin_ok = True` +
  `if i in new_ids:` at `quality/counters/c2-r44-gkeep-size-request.py:496-497` and the same branch in the r43/r42/r41 counters,
  docstring `:30-32` "a held id's receipt is not pinned … must be byte-equal to be counted by i+", control FORGED-PIN `d:0` rejected
  while P admitted, w1/CritC2Cheat "9 of 9", `frozen-F2-FORGED-PIN.txt` and `log-forged_s164.txt` exist (M44-8); base tool `:57`
  "DIFFER is a report, not a fault", `registration.md:13` "a false report", v2 `:9` "Wording withdrawn", w1/CritFsPremise item 1,
  w1/CritClaimSizing F5, K14 rejected `r:0` in `ctl-c1-v2.txt:17` (M44-9).
- **Errata E1-E4**: E1's `getReportedSize` block `Hyprland-Window.cpp:1861-1866` (`m_current.ackedSize`) and onAck store `:1526` are
  in the round-44 pin (round-43 fetch has no Window.cpp; E1's "both halves are S164 here" covers the shorthand); E2 verified against
  r11:15; E3 verified including the landed SCORECARD erratum; E4's `:97` routing vs `:46`/`:74-75` verified.
- **considerthese**: `considerthese/2026-10-25.md:46` is proposal 1 with the quoted "4 domain rounds to 2 calibration rounds"; the
  re-run prints exactly `DOMAIN_META: domain=12 meta=5 window=34-43 default=1` at `03fa5c6`, and its line `36 | C2 | operability |
  meta` is the declared hand-labelled disagreement (w1/ExecDomainMetaRatio.md `:46,:104,:129` agree); QUALITY 82 (`:411`), 83
  (`:413`), 84 (`:415`) match the lesson's account.
- **Quarantine**: w1/ScoutQuarantine/verdicts.md matches the lesson (13 rows, slice cmp identical, 7 prose `unverifiable`, no
  adopt/refuse); S189 — the register quote is present at `EventManager.cpp.efb5099:128`
  (`std::format("{}>>{}\n", event.event, data.substr(0, 1024))`), so "the register's 'absent' is false for it" is right.
- **Census/measurements**: `axis-base.txt` = three MATCH rows at the base rev; `live-geometry-host-r44.txt` = NO_MATCHING_CLIENT,
  exit 3, three clients, all `fullscreen` 0; pin census recomputed (gkeep: 1 `set_default_size`, 0 `set_size_request(`, 1
  `application_id=`; Window.cpp `:1732-1754`: 1 `->setSize(`, 1 `->configure(`); `c2-ground-base.txt` git-grep exit 1; all four
  after-data receipt lines quoted in the lesson are byte-present.

## Residual risk and gaps

- I did not execute the C1 counter (26-fixture sandbox run) or `run-c2-controls-v2.py`; the v2 verdict lines are byte-verified from
  the frozen receipts, not re-run. The `:236` Census line already discloses the same limitation for the controls.
- `sources-census.sh validate` and the spot-check's closure-run rows were not re-executed (the script lives outside the lane).
- R1's severity rests on reading "the tip" as the published tip `290cddea`; if the round's Target intended the data commit as tip,
  the phantom filenames (`c1-after-tip.txt`, `c2-after-tip.txt`, `axis-tip.txt`) remain defects regardless.
- No LSP server: every resolution above is textual; semantic equivalence of counters was not re-derived beyond w1's reports.
