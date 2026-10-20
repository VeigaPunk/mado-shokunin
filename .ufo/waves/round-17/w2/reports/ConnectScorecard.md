# ConnectScorecard — round-17 results-table number audit

Lane HEAD audited: `988b858bd6049bc709807534fd725c05264f7e60`.
Sources read: `SCORECARD.md:821-895` (declaration + pre-measurement corrections),
`.ufo/waves/round-17/drafts/ScoreTableDraft.md` (the table L1 must fill),
`.ufo/waves/round-17/evidence/*` (24 files), `corpus/SOURCES.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-16.md`, `corpus/lessons/round-17.md`, `/var/log/pacman.log`
(file bytes only, `grep`/`awk`).
Instruments re-run (read-only, permitted by the contract): `measure.py` at `27cd06f`,
`3722ba4`, `988b858`; `label-check.py`; `mado-tripwire.py --selftest core|compound|hardening`;
`sources-census.sh validate`. Install/update: **none**. No sudo, pacman, systemctl, hyprctl,
or live probe; transcripts read only where the round names them.

Paths below are relative to the lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.

---

## 1. Every number the round-17 results table can carry, with its receipt

Status legend: **R** = reproduced this session from committed bytes;
**C** = committed receipt at `988b858`; **U** = receipt exists only in the worktree;
**N** = no receipt (derived or absent).

### 1.1 C1 — calibration, literal QUALITY lesson-citation fraction

| # | Table cell | Value | Receipt path | St |
|---|---|---|---|---|
| A1 | baseline numerator / denominator | 14 / 22 | `.ufo/waves/round-17/evidence/measure-before.json` (`c1.lesson_cited`=14, `c1.criteria`=22) | RC |
| A2 | baseline score | 6.3636 | same file (`c1.score`) | RC |
| A3 | after numerator / denominator | 15 / 23 | `.ufo/waves/round-17/evidence/measure-c1.json` (rev `3722ba4`) | RC |
| A4 | after score | 6.5217 | same file; agrees with `measure-c3.json` | RC |
| A5 | delta | +0.1581 score points (raw fraction +0.015810) | **none** — arithmetic on A2/A4 | **N** |
| A6 | label check, ok-labels | **4/7** | `.ufo/waves/round-17/evidence/label-check.txt` (`LABEL_SUMMARY`) | RC |
| A7 | label check, expectations met | **7/7** | same file (`EXPECT_SUMMARY`) | RC |
| A8 | label check exit status | **1** | same file (`exit=1`); confirmed by direct run | RC |
| A9 | declared label claims | 7 | `.ufo/waves/round-17/label-claims.json` (7 objects) | RC |
| A10 | semantic block-citation counter (required by QUALITY 22 / corrections) | 17/22 = 7.7273 → 18/23 = 7.8261 | **none** — `grep -rl "semantic\|block-citation" evidence/` = 0 hits; my values are `[INFERENCE]` under the rule "numbered line **or** any continuation line of its block contains `lessons/`" | **N** |

Raw cross-check of A1/A3 by the declaration's own command
(`git show REV:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'` over
`grep -cE '^[0-9]+\. '`): `27cd06f` → 14/22, `3722ba4` → 15/23, `988b858` → 15/23.
`git diff 27cd06f 3722ba4 -- corpus/QUALITY.md` contains exactly one added numbered
line (`+23.`) and no other numbered-line change; ordinals 1–23 are contiguous.
Criterion 23's own line contains `lessons/round-17.md#mistakes M1`.

### 1.2 C2 — coverage, declared rubric V (PROVINCE P1–P6)

| # | Table cell | Value | Receipt path | St |
|---|---|---|---|---|
| B1 | baseline count / denominator | 2 / 6 | `evidence/measure-before.json`, `evidence/measure-instrument.json` (`c2.count`=2) | RC |
| B2 | baseline score | 3.3333 | same files | RC |
| B3 | after count / denominator | 4 / 6 | `evidence/measure-c2.json` (rev `a9998d1`), `measure-c1.json`, `measure-c3.json` | RC |
| B4 | after score | 6.6667 | same files | RC |
| B5 | delta | +3.3333 (=10·(4/6−2/6)); **not** +3.3334, which is only the rounded-value subtraction | **none** — derived | **N** |
| B6 | covered surfaces | P1, P2, P4, P6 | `evidence/measure-c2.json`.`c2.provinces[*].covered` | RC |
| B7 | uncoved surfaces | P3, P5 | same | RC |
| B8 | P1 evidence | `hyprland-config-era-r12.md` (legacy `covers: U2`), `window-rule-effects-getprop.md` (legacy `covers: U1`) | `evidence/measure-c2.json`.`P1.entries` | RC |
| B9 | P2 evidence | `waybar-observation-boundaries-r16.md` (legacy `covers: U7`) | same, `.P2.entries` | RC |
| B10 | P4 sources | S056, S057, S058, S059, S060 | same, `.P4.entries[0].sources_ok` | RC |
| B11 | P6 sources | S063, S064, S065, S066, S067, S068, S069 | same, `.P6.entries[0].sources_ok` | RC |
| B12 | SOURCES rows added | **15** rows S056–S070, of which **12** are cited tier-A; S061, S062, S070 are tier **C** and carry no coverage | row count: `corpus/SOURCES.md` (no `evidence/` file); cited set: measure receipts above | C (partial) |
| B13 | U-route harm watch | 7/7 (U1–U7) | `evidence/measure-before.json`, `measure-c1/c2/c3.json`.`c2.u_routes` | RC |
| B14 | instrument shas | `a280b3ab…` at `f52f43f`; `4023124f…` at `ab0bc9b` and `988b858` | **none in `evidence/`** — corrections state 8-hex prefixes only; I reproduced the full shas via `git show REV:.ufo/waves/round-17/measure.py \| sha256sum` | **N** |

Note B12: the SCORECARD/README phrasing "SOURCES S056–S070" is a **row range**, not a
coverage set. The coverage-relevant union is S056–S060 ∪ S063–S069. S061/S062/S070 must
be named as opened-but-tier-C-and-uncited, or the row overstates coverage by 3.

### 1.3 C3 — operability capability, post-hoc transcript tripwire

| # | Table cell | Value | Receipt path | St |
|---|---|---|---|---|
| C1 | capability before | absent (`c3.tool_present`=false, `sha256`=null) | `evidence/measure-before.json` | RC |
| C2 | capability after | present, `sha256` = `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44` | **no committed receipt** — `evidence/measure-c3.json` is untracked (see F1); value reproduced by `measure.py 988b858` and printed by all three selftest receipts | **U** |
| C3 | selftest core | 9/9, exit 0 | `evidence/tripwire-selftest-core.txt` | RC |
| C4 | selftest compound | 16/16, exit 0 | `evidence/tripwire-selftest-compound.txt` | RC |
| C5 | selftest hardening | 33/33, exit 0 | `evidence/tripwire-selftest-hardening.txt` | RC |
| C6 | total hermetic cases | 58 (9+16+33) | sum of C3–C5 receipts | RC (derived sum) |
| C7 | red anchor finding | `MadoR15.LibinputEvents.jsonl` line 54, `call_38165`, class `host_mutation`, rules `sudo` **and** `pacman:-S` | `evidence/tripwire-anchor-r15.txt` (`findings[]` line 54, two entries, same `tool_call_id`) | RC |
| C8 | red anchor exit | 1 | same file (`"exit": 1`) | RC |
| C9 | anchor file totals | 8 unpermitted; counts host_mutation 2, live_probe 1, package_query 5; 14 bash calls; 173 lines; sha256 `78388d42…` | same file | RC |
| C10 | pacman.log join | 4/4 mado-window transactions joined to one `host_mutation` pacman finding each; 0 tripwire pacman findings without a log line | `evidence/tripwire-pacmanlog-join.txt` | RC |
| C11 | oracle comparison | r13 26/26, r14 25/25, r15 131/131, r16 2/2 agree; `oracle_only` empty in all four; tripwire emitted 29/25/149/2 (i.e. +3 and +18 beyond the oracle) | `evidence/tripwire-vs-oracles.json` | RC |
| C12 | full-corpus scan counts | r13 2/12/19, r14 4/0/46, r15 3/28/177, r16 0/0/2 (host_mutation/live_probe/package_query), each exit 1 except r17-w1 exit 0 | `evidence/tripwire-r13.txt` … `tripwire-r16.txt`, `tripwire-r17-w1.txt` | RC |

Anchor verified against the raw transcript itself: record 54 (3977 bytes) carries
`"id": "call_38165"`, `"name": "bash"`, `"command": "sudo pacman -S --needed --noconfirm libinput libinput-tools"`,
timestamp `2026-10-20T07:25:16.905Z`. `pacman.log:2429` is
`04:25:16-0300` = `07:25:16Z`. The join's timestamp arithmetic holds.

### 1.4 Harm watch (the draft pre-commits: "each row must be re-observed at `<REV-after>`")

| # | Table cell | Value | Receipt path | St |
|---|---|---|---|---|
| D1 | hermetic selftest at `988b858` | **not re-observed** | only round-16 baseline: `.ufo/waves/round-16/evidence/legacy-selftest.json` (372/372, exit 0); `grep -rl "372/372" .ufo/waves/round-17/evidence/` = 0 | **N** |
| D2 | classifier selftest at `988b858` | **not re-observed** | only round-16 baseline: `.ufo/waves/round-16/evidence/action-selftest-final.json` (52/52, exit 0); 0 hits in round-17 evidence | **N** |
| D3 | U-route coverage 7/7 | 7 | `evidence/measure-c1/c2/c3.json` | RC |
| D4 | navigation | **no number available** | `grep -rl "30/30\|navigation" evidence/` = 0; "30/30 at round 16" is a prose baseline only | **N** |
| D5 | census | exit 0 with **3 retained W04 warnings** (S030, S042, S045 duplicate URL) | `evidence/census-start.txt` — **baseline run** (`2026-10-20T10:56:14-03:00`, 14 s *before* the `0175f13` commit); I reproduced exit 0 + the same 3 warnings at the current tree | C (baseline only) |
| D6 | freshness | 29/29 (r12) | **none** in round-17 evidence (0 hits); inherited | **N** |
| D7 | host transactions / installs, round | 0 in wave 1 **only** | `evidence/tripwire-r17-w1.txt`: 70 files, counts 0/0/0, exit 0 — exactly the 70 `w1` spec items; **excludes** `…/MadoR17.jsonl` (L1's own transcript) and all 78 wave-2 items | C (wave 1 only) |
| D8 | "13 non-lane runs 07:45–09:39, none after launch" | 13 `[PACMAN] Running` entries in `pacman.log:2440-3160`, last at line 3152 `09:39:21-0300`; launch `0175f13` = `10:56:28` → 0 after launch | **none captured** — direct read only (I re-derived it: `awk 'NR>=2440 && NR<=3160' /var/log/pacman.log \| grep -c '^\[[^]]*\] \[PACMAN\] Running'` = 13) | **N** |

---

## 2. Numbers with no receipt (the short list L1 must not publish bare)

1. C1 delta **+0.1581** — arithmetic, no receipt (A5).
2. C1 **semantic** block-citation counter **17/22 → 18/23** — required by QUALITY 22 and by
   the corrections, but no file carries it; my values are `[INFERENCE]` under a stated rule (A10).
3. C2 delta **+3.3333** — arithmetic; the rounded-subtraction value 3.3334 is wrong (B5).
4. C3 **after** state (`tool_present` true + tool sha256) — **no committed receipt**; the only
   file is untracked (F1).
5. **372/372** at REV-after (D1).
6. **52/52** at REV-after (D2).
7. **30/30** navigation (D4).
8. **Census at REV-after** — baseline-only receipt (D5).
9. **Round-level "0 host transactions"** — wave-1-only coverage; wave 2 and L1's own
   transcript unscanned (D7).
10. **13** non-lane pacman runs / "none after launch" (D8).
11. Instrument shas `a280b3ab…`, `4023124f…` — reproducible, present in prose only (B14).

Items 1–3 are legitimately derived; the table must label them "derived" rather than attach a
receipt path. Items 5–9 are the dangerous class: they look measured but are not.

---

## 3. Falsifiers and contradictions found

**F1 — C3's only "after" receipt does not exist at lane HEAD (highest).**
`.ufo/waves/round-17/evidence/measure-c3.json` is untracked:
`git ls-files --error-unmatch` → *"did not match any file(s) known to git"* (rc 1);
`git check-ignore` → rc 1 (not ignored, just untracked); absent from
`git ls-tree -r 988b858`; mtime `2026-10-20 11:50:30` is the **same second** as the C3
commit `988b858` (11:50:30), so it was written after the commit object was created.
Its `"rev"` field is the literal string `"HEAD"`, not a commit — it is not revision-bound.
A fresh `measure.py 988b858` differs from it in **exactly one key** (`rev`: `"HEAD"` vs
`"988b858"`), so the content is honest but the artifact is not in the lane.
Consequence: if L1 cites `evidence/measure-c3.json` for "absent → present", the citation
names a path that a reader of `988b858` cannot open. This is precisely the defect class
criterion 23 was added to catch, occurring in the round's own receipt set.
Remedy inside L1's authority: cite the reproduction (`measure.py 988b858` → `c3.tool_present`
true, sha `4ced68d3…`) and/or commit the receipt; do not cite the worktree path as if pinned.

**F2 — The label check's pass state is `exit 1`, and QUALITY 23 does not say so.**
`label-check.py` returns **1** while `EXPECT_SUMMARY` is 7/7, because exit 1 means "a declared
MISMATCH is present" (three are present *by design*: R16-V1-red and the two mutants). So the
single run yields three different-looking numbers: `LABEL_SUMMARY 4/7`, `EXPECT_SUMMARY 7/7`,
`exit=1`. QUALITY 23 says only "`EXPECT_SUMMARY` must be 7/7"; `SKILL.md:558` carries the
exit contract ("1 any MISMATCH (expected for declared red claims)"). A table cell that prints
only "7/7" hides a nonzero exit; one that prints only "4/7" or "exit 1" reads as failure.
All three must appear together. (Not a defect in the claim — C1's red is real: `round-16.md`
lines 131-132 attribute `snapshot_tampered` to a receipt whose recorded outcome is
`frozen_error` at `measured_commit 9dcf248…`.)

**F3 — `SOURCES S056–S070` is 15 rows, but coverage cites 12.**
Measured `sources_ok` is S056–S060 (P4, 5) and S063–S069 (P6, 7). S061 (Arch Wiki),
S062 (Linux Junkies), S070 (FlareXes) are tier **C** and appear in neither entry's cited set.
Any sentence of the form "P4/P6 rest on S056–S070" overstates by three rows and by the tier
claim. Correct phrasing: "rows opened S056–S070; admitted support S056–S060 and S063–S069".

**F4 — "Agrees with an independent oracle" is recall-complete, not set-equal.**
`tripwire-vs-oracles.json` shows `oracle_only: []` in all four rounds (tripwire misses nothing
the oracle found) but tripwire emits 29 vs 26 (r13) and 149 vs 131 (r15). Reporting only
"agrees" implies equality that the receipt contradicts; the honest cell is
"0 oracle-only misses; +3 and +18 extra findings".

**F5 — Two harm-watch numbers cannot be re-observed under this round's own command fence.**
372/372 and 52/52 come from `tools/mado-verify.sh --selftest` and
`tools/mado-action-plan.py --selftest`, neither of which is on the permitted command list for
this round, and neither has a round-17 receipt. The draft already pre-commits "none is claimed
here"; the published table must keep that stance or it will present round-16 numbers under a
round-17 "Observed at" column.

**F6 — "Admitted" knowledge entries are not machine-checked.** `measure.py` accepts any
committed `corpus/knowledge/*.md` meeting the head/heading/source rules; admission is only
evidenced by the index rows in `corpus/README.md:42-43,120-121`. C2's claim is otherwise
sound: the instrument is stricter than declared only (single `surface:` token, four exact
headings, 3-line content floor per heading, `[UNK]` inside `## Unexercised behavior`, at least
one cited mined tier-A **https** row of kind docs/spec/code whose source/scope names the
surface, and legacy credit pinned to the three entries that held it at `27cd06f`). P4/P6 pass
on S056/S057/S058 and S063/S064/S065–S069 respectively, all `mined`/`A` with `used-by`
naming the entry.

**F7 — C1's receipt postdates C1's claim by two commits.** `measure-c1.json` was added in
`988b858`, not in `3722ba4`; it is bound to `3722ba4` by its `rev` field and reproduces, so the
number is valid, but the table must not imply the receipt existed at the C1 commit.

**Attacks that failed (claims that survived):**
C1's 14/22 → 15/23 by the declared command (pure append, contiguous ordinals, lesson-cited
criterion); the round-16 mislabel is genuine and the checker flags it; C2's 2/6 → 4/6 at
`a9998d1` under both instrument versions (`measure-before.json`, `measure-instrument.json`
both show 2/6; the tightened instrument is stricter only); C3's 9/9, 16/16, 33/33 all re-run
green with the same script sha; the anchor tuple (line 54, `call_38165`, `host_mutation`,
`sudo` + `pacman:-S`, exit 1) is exact against the raw transcript; the 4/4 pacman.log join is
timestamp-consistent; `measure.py` was genuinely absent at `0175f13` (`git cat-file -e` rc 128).

---

## 4. Proposed move (one, bounded)

Add a **receipt-state column** to the results table with three admissible values —
`committed@REV`, `reproducible (command + REV)`, `absent` — and print the label-check triple
(`4/7` ok-labels, `7/7` expectations met, `exit 1`) as one cell. For C3's after-state, use
`reproducible (measure.py 988b858)` until `evidence/measure-c3.json` is committed; for
372/372, 52/52 and navigation, use `absent` and keep the draft's "not re-observed" wording;
for C2, replace "S056–S070" with the cited union and name S061/S062/S070 as tier-C/uncited.

This improves calibration (no unreceipted number is published as measured) and operability
(the receipt set becomes existence-checkable) and harms no axis: coverage V stays 4/6, U stays
7/7, and nothing is re-scored. It also makes the round's own criterion 23 self-applying.

Risks: the table gets a wider shape; and a reader may read `absent` as a lost claim rather than
a scope limit — the D1/D2 rows must keep the "baseline reference / not re-observed" split the
draft already specifies. Do **not** satisfy the column by committing `measure-c3.json` as a
wave-2 mutation of the C3 claim; L1 owns that decision, not this report.

Verification available to L1, read-only:
`for p in measure-before.json measure-c1.json measure-c2.json measure-instrument.json label-check.txt tripwire-*.txt tripwire-vs-oracles.json census-start.txt; do git cat-file -e 988b858:.ufo/waves/round-17/evidence/$p; done`
(and `measure-c3.json` must fail); `python3 -I .ufo/waves/round-17/label-check.py; echo $?` → 1;
`python3 -I .ufo/waves/round-17/measure.py 988b858` → `c3.tool_present true`.

---

## 5. Axes touched

- **calibration (6.3636 → 6.5217, lowest active scored row):** improved by refusing to publish
  A5/A10/D1/D2/D4 as receipted; F2 prevents the label check from being read as either 7/7-green
  or 4/7-red.
- **coverage V (3.3333 → 6.6667):** unchanged; F3/F6 bound the claim to the measured union.
- **operability:** capability unchanged (real, reproduced); F1 repairs the only unbound receipt.
- **harm watch:** D1/D2/D4/D5/D7/D8 delimit exactly what was and was not observed at `988b858`.
