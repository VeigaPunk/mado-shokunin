author: hyaku closure (non-author integrator, @m_sonnet)

# mado round 41 — non-author closure spot-check

Lane HEAD before `ab2bfaab661c846d1de9d58c01651cd156a13949`, after `b20155b10a84e4c2a82a1f59bef417e470abd91e`.
Driver digest (`.ufo/watchdog.log`, mutable): `2026-10-25T19:30:25-03:00 launch mado round=41 pgid=535349 driver=hyaku-inline attempt=1` / `2026-10-25T22:13:09-03:00 complete mado round=41; hyaku-inline attempt=1`.
I did not author the round. All re-checks ran on committed bytes (`git archive` / fresh `git clone` of the tip under `/tmp`, never in the lane tree).

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-41/mado.md` | `mado-shokunin 866affa32260b63503920d70a78b3c0c8e0cbfe8` |
| SHONEN heading | `grep -c '^## SHONEN' …/mado.md`; `grep -c '^- \[' …` | 1 heading; 4 box lines (SHONEN.md has 4 boxes, all `[~]` with pointers) |
| cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for the 9 report hashes (60c3914, cd950ec, 294c667, 07f2641, 9919e16, 6fd2234, 2a65350, 4d00de3, b20155b) | all 9 `ok` |
| pushed | `jj-lane.sh state …` ; `git ls-remote origin refs/heads/master` | `local=remote=b20155b… ahead=0 behind=0`; remote head `b20155b…` |
| uncommitted round work | `git status --porcelain` | none tracked; **2 untracked** scratch files `.ufo/waves/round-41/w2/ExecDiffFuzzV2/scratch/s-grow`, `s-size` (not round deliverables; status-neutral defect) |
| prompt contract | heading comparison `.ufo/prompts/mado-round-41.md` vs `templates/round-prompt.md` | §1–§5 identical headings, §6 hyaku addendum present |
| real report, not a marker | work, commits, receipts, pointers present | real report → status `ok` |

Defects (status-neutral): (a) two untracked scratch files left in the lane tree; (b) the report's one-line claim cells are very long (cut at 768 B in tooling); (c) the lesson cites `PROVINCE.md:75` for the localized-channel exclusion — the clause is lines 75–76 (cosmetic).

## 2. Per-claim re-check

Both claims rest on lane-owned counters (`quality/counters/c1-r41-globals-v2.py`, `c2-r41-focus-entry-v2.py`). Per §Gate standard I verified committed receipts; additionally, as an independent fresh-nonce confirmation over a clean clone of the tip (not a sibling's gate: it is this lane's own), I ran both. The decisive evidence is plain measurement.

**C1 — operability, capability acquisition (`tools/mado-globals.py`) — re-measured + receipts verified**
- `git cat-file -e ab2bfaa:tools/mado-globals.py` → absent; at `b20155b` → present (437 lines per `git diff --stat`).
- `python3 -I tools/mado-globals.py --selftest` (tip archive) → `MADO_GLOBALS_SELFTEST: 63/63 passed` (matches `receipts/harm-tip.txt`).
- `python3 -I tools/mado-globals.py --live` on this host → `MADO_GLOBALS_SESSION n=2 … interfaces=63 adverts=63` and `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab` (live end-to-end demonstration, matches the reported 63-interface latest session).
- Committed receipts: before `receipts/c1-v2-before-base.txt` `fixtures=0/39 tool=absent TARGET_MISSED`; after `c1-v2-after-tip.txt` `clause=b rc=0 selftest=63/63`, 6/6 b2 mutants killed.
- Fresh-nonce counter run on a clean clone at tip: `PRED-C1-r41-v2: fixtures=39/39 tool=present verdict=TARGET_MET rev=b20155b… nonce=24222cea8dafd277`, exit 0 (reported nonces were `be51c3bc…`/`352a9fb7…`).
- Honest limit: the lane itself reports the C1 predicate is weak (5 of 11 new cheats reach TARGET_MET, 33 of 64 mutants survive). That bounds the *counter*, not the tool: the tool's selftest and a live run on the real host both pass, so the capability is genuinely present. Verdict **improved** (operability).

**C2 — coverage, sourced (`corpus/knowledge/hyprland-focus-grab-r41.md`) — re-measured**
- Entry absent at base (`git cat-file -e ab2bfaa:…` fatal); present at tip; base `git grep -il 'focus.grab' ab2bfaa -- corpus/knowledge` → empty (ground not held).
- Registry rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` base 219 → tip 226 (reported 219 → 226); knowledge entries (`git ls-tree --name-only <rev> corpus/knowledge/ | wc -l`) 58 → 59.
- Counter on clean clone of tip: `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET rev=b20155b…`, exit 0; receipts `c2-v2-before-base.txt` `admitted=0/1` → `c2-v2-after-tip.txt`.
- Honest limit (reported by lane): 10/10 real-seeded forgeries pass the predicate; so the claim rests also on the spot-check of quotes below. Verdict **improved** (coverage).

**Harm watch** — re-ran on the tip archive: `MADO_SELFTEST: 460/460`, `MADO_OPTIONS_SELFTEST: 211/211`, `MADO_GLOBALS_SELFTEST: 63/63` (all equal `receipts/harm-tip.txt`); `quality/receipts/axis-2a65350….txt`: `MADO_AXIS checked=3 mismatched=0` (59/59, 63/63, 12/12). `git diff ab2bfaa b20155b -- SCORECARD.md` is append-only (+34 lines, no existing row edited); no published score fell.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured (tool absent → present, selftest 63/63, live census) |
| coverage | improved | C2 re-measured (entry, 7 rows, focus-grab ground absent at base) |
| depth | unchanged | no decision-table regression; SKILL.md only gains a probe row/decision row/subsection |
| freshness | unchanged | S037 used-by edit logged old→new; no stale claim left unmarked found |
| calibration | unchanged | v1→v2 re-registration and w2 data defects are disclosed, repaired (`6fd2234`), counters' limits stated; axis receipt 63/63 MATCH |
| adjacency | unchanged | localized-channel material refused; sibling scan recorded |

No axis harmed.

## 4. Discernment spot-check (round-41 lesson `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S283 focus-grab-v1.xml quote "This interface restricts input focus to a specified whitelist of surfaces" | admit | `.ufo/waves/round-41/fetch/focus-grab-v1.xml` (sha256 `0bc60c14…c0285b4` re-computed: match); phrase wraps lines 62–63, found after whitespace normalisation | agree | quote is present, 11 words (≤25), digest matches the SOURCES row |
| S289 journal "Got interface: hyprland_focus_grab_manager_v1 (ver 1)" | admit | `…/fetch/xdph-journal.txt` (sha256 `bf8fa91a…aa600aaf7` match; `grep -c` = 1) and live `mado-globals.py --live` | agree | own-work row corroborated by an independent live run on the host |
| S284 `m_grab->m_keyboard = true;`, S285, S287, S288 quotes | admit | `grep -n` in the respective receipts: found (FocusGrab.cpp:20; quickshell-grab.cpp:78; protocols-README, issue-565 hit) | agree | all quotes present; each ≤25 words |
| entry `focus-grab-protocol-live-on-host-r14.md` → `hyprland-focus-grab-r41.md` | admit (successor) | `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md`; base has no focus-grab text | agree | re-grounded on lane receipts; w2 repairs fixed overstatements (six requests, ten branches) |
| `privileged-client-surface-r29.md` | reject | same package dir; 37 lines, one source (S244 blog), a truncated quote ("But there is also `WAYLAND_SOCKET`, which"), §2 says "Nothing here was measured on this host" | agree | single secondary source, truncated quote, no measurement: fails the bar; refusal justified |
| `focus-control-surfaces-r28.md` §3 | reject | package file cites S230 `amgsk.dev/posts/hyprland-rules/` (JetBrains…フォーカス問題 = Japanese channel); `PROVINCE.md:75-76` excludes "documentation written in a localized channel" | agree | out of province by the lane's own text; §1–§2 ground re-sourced by S287/S283 |

New-row quote check (`corpus/SOURCES.md` S283, S284, S288, S289 re-read at `b20155b`): quotes ≤25 words, locators and digests resolve. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, exit 0, the same W04×7 + W01 S277 set as base (`receipts/census-before.txt`).

## 5. Trend verdicts

- **expansion: improved** — one new admitted entry on ground absent at base, 7 new `mined` rows (219→226), one new capability row.
- **quality: improved** — w1/w2 falsification turned into repairs (`6fd2234`) and QUALITY 69–76; the cost is disclosed (v1 predicates were wrong; data commit had defects before repair). No admitted entry fails its re-check in my sample.
- **discernment: improved** — I agree with all 3 assimilation decisions and the quote checks, on admits and rejects; the outside check is now this document.

## 6. Routed to the lane for round 42

1. Delete or commit the two untracked `ExecDiffFuzzV2/scratch/s-grow`, `s-size` files.
2. Tighten the C1 predicate (selftest teeth: AST-fingerprint/zero-test selftest cheats) and C2 (mid-word quote ends, swapped captions) as already planned; until then treat TARGET_MET as weak evidence and keep a plain measurement beside it.
3. Open items the lane lists: S041 held-row citation, tool ergonomics O1–O5.
4. Correct `PROVINCE.md:75` → `75-76` in the lesson citation when next touched.

SHONEN: all four boxes remain lane-asserted `[~]`; a non-author could now check box 2 (live census reproduced above) but box 1, 3 and 4 need the operator; promotion stays operator-owned.
