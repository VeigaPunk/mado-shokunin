# RevR46 — round-46 landed-state review (round 47 w1, base 60edb66)

Reviewer: RevR46, leaf seat, non-author of round 46. Target: the round-46 landed state at
`60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (the round-46 closure commit; data tip
`edc147898e9de3c4e40f003277f20dbf67f18956` is its ancestor — `git merge-base --is-ancestor` ok).
Method: re-ran both round-46 counters as measurements at the base rev, ran the landed tool's
selftest from committed bytes, cross-checked every SCORECARD Round 46 number against the
committed receipts, then hunted defects beyond R1-R4 of
`corpus/lessons/round-46-verifier-spotcheck.md`. All commands read-only; no tool installs
(python3/git/curl/jq present; `bc` absent, not needed). Scratch
`/fast/scratch/hyaku/mado-r47/RevR46` deleted at completion; receipts copied into this seat dir first.

## 1. Re-measurements (all reproduce)

| measurement | result |
|---|---|
| C1: `python3 -I quality/counters/c1-r46-devices-v3.py --repo <lane> --rev 60edb66… --work /fast/scratch/hyaku/mado-r47/RevR46/w` | `fixtures=110/110 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0, `seeds=46,1121157060`, `clause=r trips=0` — receipt `receipts/c1-rerun-r47.txt` (this seat dir) |
| C2: `python3 -I quality/counters/c2-r46-input-device-entry-v2.py --repo <lane> --rev 60edb66…` | `clauses a:1…k:1 admitted=1/1 verdict=TARGET_MET`, exit 0 — receipt `receipts/c2-rerun-r47.txt` |
| tool selftest from committed bytes (`git cat-file blob 60edb66:tools/mado-devices.py`, sha256 `3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f`) | `MADO_DEVICES_SELFTEST: 59/59 passed`, exit 0 |
| wave results | `jq` on `.ufo/waves/round-46/w1-results.json`: `seats=66, n=66, nulls=0` |

Nonce independence: my C1 nonce `1121157060` differs from every committed receipt's
(after-data `4292010041`, tip `3350998614`, closure tip-run `1593941714`); four independent
nonces, all pass.

## 2. SCORECARD Round 46 vs receipts — every cell traces

| SCORECARD cell (SCORECARD.md:2625-2646) | committed receipt | verdict |
|---|---|---|
| C1 before at base, MISSED exit 1 | `receipts/c1-v3-before-base.txt` final line verbatim, `rev=b22ea56…`, `seeds=46,46` | match |
| C1 after at `1001bda`, MET exit 0 | `receipts/c1-after-data.txt` verbatim, `rev=1001bda…` | match |
| C2 before/after | `c2-v2-before-base.txt` `admitted=0/1` exit 1; `c2-after-data.txt` `admitted=1/1` exit 0 at `1001bda`; `c2-tip.txt` same at `9879964` | match |
| C1 controls "PASS 0 of 40" | `ctl-c1-v3.txt`: `VERDICT: PASS (controls scoring TARGET_MET: 0 of 40; reference met: 1)`, exit=0; 41 scored runs = 40 controls + REF | match |
| C2 controls "PASS wrong 0 of 22" | `ctl-c2-v2.txt`: `VERDICT: PASS (wrong=0 of 22; positive admitted=1)`, exit=0; header `controls=22 (P positive; 21 do-nothing/forged)` | match |
| capability row live run "9 AGREE, 1 VIRTUAL, 4 pointers AGREE, OK, exit 0" | `live-devices-host-r46.txt`: `keyboards=10 agree=9 … virtual=1 mice=4 mice_differ=0 … verdict=OK`, exit=0; header tool sha256 = `3a803689…` | match |
| report's v1 controls: C1 "0 of 23", C2 "P admitted, 14 rejected" | `ctl-c1.txt` verdict `0 of 23`; `ctl-c2.txt` `wrong=0 of 15` (= P + 14) | match |
| knowledge 62→63; rows 252→262; SCORECARD +29 pure append; SOURCES +10/−0 | recomputed: `git ls-tree … grep -c` 62/63; SOURCES S-row count 252/262; `git diff --numstat` `10 0`; SCORECARD numstat `29 0` | match |
| session-material "findings=115; 18 in round-46 seat files" | `session-material-data.txt`: 115 `FINDING` lines, exactly 18 with `round-46` in `file=` | match |
| M46-1..16; QUALITY 87-90; LOG Round 46 bullets; PROVINCE +15; ten pins; ScoutRecheck | `corpus/lessons/round-46.md` has 16 `**M46-n**` rows; `corpus/QUALITY.md:428-459` rows 87-90 with M46 mappings; LOG.md:2515-2521; PROVINCE.md diff `+15`; `fetch-sha256.txt` 10 rows; `w1/ScoutRecheck.md` exists | match |
| fleet report commit | `b25732fc…` by `mado-shokunin <mado@shokunin.local>` 2026-10-26T18:27:52-03:00, after lane tip 18:26:38 | match |

## 3. Defects beyond R1-R4

### D1 — LOW, citation precision: SCORECARD axis line cites the red data-commit receipt
`SCORECARD.md:2646`: "Axis table re-derived at `1001bda` (`receipts/axis-data.txt`): navigation
63/63; calibration resolved-active 77/77; operability selftest 12/12."
- The cited receipt at the named rev reads otherwise: `.ufo/waves/round-46/receipts/axis-data.txt:1-5`
  = navigation `published=62/62 derived=63/63 verdict=STALE`, calibration
  `published=73/73 derived=77/77 verdict=STALE`, `mismatched=2`, `exit=1`. The MATCH rows for
  63/63 and 77/77 live in `receipts/axis-tip.txt:2-5` at `9879964`.
- The lane's own precedent names the second commit in this line:
  `SCORECARD.md:2493` (round 40) "…re-derived at `3c80537a…` plus the round-40 axis-line commit…",
  `SCORECARD.md:2521` (round 41) "…plus the round-41 records commit…"; round-43's
  `.ufo/waves/round-43/w2/ExecHarmTip.md:29-31` verified that shape and round-44's line
  (`SCORECARD.md:2560`) says "no harm beyond the declared two-phase axis publication".
  Round 45 (`SCORECARD.md:2617`) already dropped the clause and the round-45 closure passed it —
  consistency drift, not a new class.
- The round report discloses the window honestly (report "Harm watch": data commit reads STALE in
  the declared two-phase window, citing axis-tip.txt). A reader following only the SCORECARD
  pointer hits `exit=1` with no pointer to the MATCH receipt.
- Fix: append "plus the records commit `9879964`" or cite `axis-tip.txt` beside `axis-data.txt`.

### D2 — LOW-MED, dangling pointer (QUALITY-24 citation class): bare `receipts/synthetic-verdicts.txt`
`SKILL.md:2129`, `:2134`, `:2137` cite `receipts/synthetic-verdicts.txt` bare. The file exists only
at `.ufo/waves/round-46/w1/ScrSkill/receipts/synthetic-verdicts.txt` (`git ls-tree -r 60edb66`) and
NOT in `.ufo/waves/round-46/receipts/` — the directory the same section cites full-path at
`SKILL.md:2121` (`live-devices-host-r46.txt`). These are the only three bare `receipts/` citations
in SKILL.md (grep), so the section's own convention contradicts them; resolving `receipts/` as the
round receipts dir finds nothing. The receipt's content is real and supports the rows (it exercises
DIFFER>STALE_BLOCK, pure STALE rc 4, NOT_COMPARED rc 5, FALLBACK, mouse DIFFER, NO_SUCH_DEVICE on
caps, VIRTUAL with top OK, NO_KEYBOARDS rc 3, SETUP rc 2 — exactly the "(tested NOT_COMPARED,
DIFFER, NO_KEYBOARDS, STALE_BLOCK, OK)" claim at SKILL.md:2110). Fix: full path in the three rows.

### D3 — LOW-MED, mis-located quote (round-45 F1 class): `mado-devices.py:87`
`SKILL.md:2134` quotes "an unmodelled line can change any expectation" with locator
`mado-devices.py:87`. In the landed bytes the sentence spans `tools/mado-devices.py:98-99`
(`:98` "…V = NOT_COMPARED (exit 5, unsupported > 0: an unmodelled line can change any" /
`:99` "expectation) | DIFFER (exit 1 …)"); `:87` is the mouse-factor/MATCHED sentence
("…else DIFFER. A device block AGREEs as MATCHED when its"). Off by 11 lines; grep finds exactly
one occurrence of the phrase in the tool (:98). Same class as routed R4-F1 ("mis-located `:84b`").
Fix: `mado-devices.py:98-99`.

## 4. Observations (not defects)

- **Tool ≡ counter reference, byte-identical.** `git ls-tree 60edb66` gives blob `2f7c5288…` for
  BOTH `tools/mado-devices.py` and `.ufo/waves/round-46/v2/mado-devices.py` (the counter's MODEL;
  `MODEL_SHA256 3a803689…` = the landed tool's sha256 = `live-devices-host-r46.txt:1`). Clause g's
  150/150 (tool vs model) therefore carries no independent evidence for this tool — tautological up
  to environment nondeterminism. This sits inside the counter's declared residuals
  (`quality/counters/c1-r46-devices-v3.py:57-63`: "a tool holding a model of the contract is an
  implementation of it"; "clause g's oracle is the reference, so a contract error shared by
  reference and tool is invisible to it"). The discriminative weight is elsewhere and present:
  clause f (110 pinned fixtures, committed expectations), clause r (0 trips), the w1 independent
  rebuilds (`w1/ExecIndepA.md`, `ExecIndepB.md`), and the closure's live independent check. Stated
  so the L1's freeze can carry it explicitly.
- **Discernment extended beyond the closure's 5/5.** Re-fetched S319 and S322 at efb50993 on
  2026-10-26: sha256 `8a800efe…` / `bc6d984a…` byte-equal to the Gate lines
  (`corpus/lessons/round-46.md:38,41`) and `fetch-sha256.txt`; quotes present at the counter's
  locators (`m_currentRules.layout  = "us";` at :113 — whitespace-aligned source, which is why the
  counter's normalized match is the right checker; `m_keymapOverridden = true;` at :41). With the
  closure's samples: 7 gate admits re-opened, 0 disagreements.
- **Session-material phrasing is internally consistent.** "18 findings in round-46 seat files"
  counts FINDING lines, the receipt's own unit (`findings=115` = 115 lines); single files carry
  larger object counts on one line (e.g. `w1/ExecW2Monitors/adversarial.txt` `count=26`).

## 5. Pins fetched this seat (stored with sha256 + URL)

| file | url | sha256 |
|---|---|---|
| `receipts/pins/Hyprland-IKeyboard.cpp` | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.cpp | `8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d` |
| `receipts/pins/Hyprland-VirtualKeyboard.cpp` | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/VirtualKeyboard.cpp | `bc6d984a4c9e62313501c1cdb4ace3659c16d3b77e029a3c082a77f21500ed86` |

## 6. Verdict

Round 46's landed state re-verifies at `60edb66`: both counters TARGET_MET under fresh nonces,
selftest 59/59 from committed bytes, every SCORECARD Round 46 number traced to a committed
receipt. Three new defects, all citation-layer (D1 LOW, D2 LOW-MED, D3 LOW-MED), none in R1-R4,
none touching the claims' substance; the two LOW-MED ones are the same QUALITY-24 class the round
itself mined (M46-5/R1). No axis harmed: my runs wrote only this seat's files.

Report: .ufo/waves/round-47/w1/RevR46.md
