author: hyaku closure (non-author integrator, @m_opus)

# Round 18 — non-author verifier spot-check (mado)

Date: 2026-10-20. Closure of mado round 18, hyaku phase 2. Baseline
`d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` → lane tip
`b7148a1eec4f9726b09a7679261ec6e8f5a74c58` (`refs/heads/master`). The closure
did not author any of this round's work. Driver digest (`.ufo/watchdog.log`, lines 489/494 at closure time):
`2026-10-20T12:29:34-03:00 launch mado round=18 pgid=1899513 driver=hyaku-inline attempt=1`;
`2026-10-20T13:48:31-03:00 complete mado round=18; hyaku-inline attempt=1`.
Every command below was re-run at closure time. The closure did not execute the
lane's gates or selftests (`tools/mado-verify.sh`, `tools/mado-tripwire.py`,
`.ufo/waves/round-18/receipt-check.py`, `measure-mutants.py`): their claims are
evidence-verified from committed receipts. It did run the declared read-only rubric
counter `.ufo/waves/round-17/measure.py` (reads `git show REV:path` only; sha256
`de4c422b…` at both revisions) as a cross-check of its own hand counts.

## 1. Conformance (PROTOCOL §Round-robin closure step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-18/mado.md` (fleet) | `mado-shokunin bc5d2802c39ddf83c17963cc9f9734eba9201cec`, 13:48:10 -03, after lane tip commit 13:47:14 -03 | ok |
| `SHONEN` heading, one line per box | `sed -n '/^## SHONEN/,/^## /p' report \| grep -c '^- \['`; `grep -c '^- \[' SHONEN.md` | 4 and 4, all `[~]` | ok |
| Cited hashes exist and are ancestors | `git merge-base --is-ancestor <h> refs/heads/master` for d3a00003, 4c103b55, abfbf35b, be886a3c, a210241b, b7148a1e (+ baseline d9a5a18) | 7/7 ok; `refs/heads/master` = HEAD = `b7148a1e…` | ok |
| Pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `local=remote=b7148a1… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `b7148a1e…` | ok |
| Round commits by lane | `git log --format='%h %an' d9a5a18..refs/heads/master` | 6 commits, all `mado-shokunin` | ok |
| Prompt carries the contract | `diff <(sed '/^## 6/,$d' .ufo/prompts/mado-round-18.md) templates/round-prompt.md`; §6 vs `git show b8afbd0:scripts/hyaku/lane-addendum.md` rendered | sections 1–5 differ only in placeholder substitution (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §6 equals the last pre-dispatch addendum `b8afbd0` with `{{LANE}} {{ROUND}} {{ATTEMPT}} {{TARGET}} {{FLEET_ROOT}} {{LANE_CWD}} {{CANON}}` substituted; prompt committed `20a06f7` (mado-shokunin, 12:29:32 -03, before launch) | ok |
| LOG entry | `grep -n 'round 18' LOG.md` | `LOG.md:1287 ## 2026-10-20 — round 18: …` | ok |
| Seats | `jq '.members\|length' .ufo/waves/round-18/w{1,2}/record.json`; `ls w3/reports` | 88 + 73 members; w3 6 reports → 167 as reported; 14 wave-2 seats without report disclosed (lesson M8) | ok (disclosed) |

Not a marker: real committed work with checkable hashes. No conformance defect found.

## 2. Claims — re-checks

### C1 calibration (literal lesson-citation fraction) — re-measured

```
for r in d9a5a18 b7148a1; do q=$(git show $r:corpus/QUALITY.md)
  echo "$r total=$(grep -cE '^[0-9]+\. ' <<<"$q") lessons=$(grep -cE '^[0-9]+\. .*lessons/' <<<"$q")"; done
d9a5a18 total=23 lessons=15
b7148a1 total=26 lessons=18
```
15/23 = 6.5217 → 18/26 = 6.9231; matches the report. Counter cross-check:
`python3 -I .ufo/waves/round-17/measure.py <rev>` → c1 15/23 and 18/26. Criteria 24–26
(`corpus/QUALITY.md:131,138,144`) each cite `lessons/round-18.md#mistakes` M1/M2/M3 plus an
outside source. The "fails on a real d9a5a18 artifact" part, checked by plain reads:
- 24 (producer identity): `git show d9a5a18:.ufo/waves/round-17/evidence/tripwire-r{13,14,15,16,17,17-w1}.txt | grep -c tool_sha256=` → 0 in all six; the first line is the bare verdict (`MADO_TRIPWIRE: findings`). The criterion's check has a real red to read.
- 25 (mutant receipts): `git show f52f43f8:.ufo/waves/round-17/measure.py | sha256sum` → `a280b3ab…` = the receipt's loose instrument; tight = `de4c422b…` (d9a5a18). `evidence/measure-mutants.json` `.summary` → `{"mutants":6,"bites":6,"no_bite":[],"baselines_agree":true}` (evidence-verified).
- 26 (pipe status): `git show d9a5a18:tools/mado-verify.sh | sed -n 3406p` → `blob=$(tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null | sha256sum | cut -d' ' -f1)` with no `pipefail`: a failed `git show` yields `e3b0c442…`, non-empty, so the row reports a local edit. At `b7148a1:3477` the substitution runs `set -o pipefail`. Criterion 26's red-before rests on `evidence/gate-rc-redbefore.txt` (no producer header; the lane's own append correction says so) and the w3 swap result 383/389 in `w3/reports/W3CriticC1Final.md`.
Verdict: **improved** (re-measured).

### C2 coverage, rubric V — re-measured

Hand check of the two new entries (`git diff --name-status d9a5a18 b7148a1 -- corpus/knowledge` → only `A walker-route-r18.md`, `A theme-route-r18.md`):
`surface: P3` / `surface: P5` in the first 15 lines; headings `## Upstream contract`,
`## Host declaration`, `## Safe observation`, `## Unexercised behavior` present in both;
`[UNK]` inside `## Unexercised behavior` 15× (walker) and 10× (theme); head `source:` tokens
S072… / S092…; rows S076, S092, S094 read as `mined | … | A` with `used-by` naming the note.
Counter cross-check: `measure.py d9a5a18` → c2 4/6 (P3, P5 false), `measure.py b7148a1` →
6/6, 0 rejected, `u_routes` 7 at both. SOURCES rows: `grep -cE '^\| *S[0-9]{3} '` → 71 → 95.
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0,
the same three historical W04 (S030/S042/S045). 4/6 → 6/6; matches. Documentary routes only —
behaviour stays `[UNK]`, as the lane states. Verdict: **improved** (re-measured).

### C3 operability — capability acquisition, tripwire frozen replay — evidence-verified

Gate (registry row `SKILL.md:566` `mado-tripwire-frozen | gate | … 0 clean / 1 failed / 2 could-not-evaluate`), so
§Gate standard (Closure consequence) binds: not executed. Committed evidence:
- Tool shas by revision: `git show <r>:tools/mado-tripwire.py | sha256sum` → d9a5a18 `962919ce…`, abfbf35 `c87a31ef…`, be886a3 = b7148a1 `c1ae45a7…` (unchanged after be886a3, so the be886a3 receipts describe the tip's tool).
- Before: `evidence/tripwire-frozen-before.txt` header `tool_sha256=962919ce… measured_commit=d9a5a18…`, usage, `exit=2`.
- After: `evidence/final/tripwire-frozen-match.txt` (`tool_sha256=c1ae45a7… measured_commit=be886a3…`) `MADO_TRIPWIRE_FROZEN: frozen_match`, `exit=0`, `expected_sha256 4f3534ae…`; `tripwire-frozen-tampered.txt` `snapshot_tampered`, `exit=2`.
- Pins re-hashed by the closure: `sha256sum frozen/expected.json` → `4f3534ae…` (= receipt); every `inputs[]` digest in `expected.json` equals `sha256(inputs/<file>)`, 5/5 ok.
- Selftest: `tripwire-frozen-selftest.txt` `SELFTEST_SUMMARY: 31/31 passed`, `exit=0`; `tripwire-frozen-selftest-redbefore.txt` (abfbf35 tool, same suite) `17/31 passed`, 14 failed, `exit=1`. The report's "fails 14/31" counts failures; SCORECARD's "17/31" counts passes — consistent.
- Scope (lane-stated, agreed): detects classifier-output changes on 5 pinned incident files (8 findings, 3 known misses); not classifier correctness or prevention.
Verdict: **improved** (capability acquired, evidence-verified).

### Harm watch (no owned axis harmed)

`git diff d9a5a18 b7148a1 -- SCORECARD.md` → one hunk `@@ -927,3 +927,131 @@`, pure append.
`git diff --numstat d9a5a18 b7148a1 | awk '$2>0'` → only `SKILL.md` (2 lines: the probe
description now points to the frozen gate), `tools/mado-tripwire.py`, `tools/mado-verify.sh`.
Receipts (`evidence/final/`, header `measured_commit=be886a3c`): gate selftest
`MADO_SELFTEST: 389/389` (`tool_sha256=c9fb0cef…` = `git show b7148a1:tools/mado-verify.sh | sha256sum`),
scan suites 9/9, 16/16, 33/33, 30/30 (unchanged counts), frozen 31/31, failsafe 1/1, classifier
`SELFTEST_SUMMARY: 52/52`, U and navigation exit 0, census exit 0. U-routes 7 → 7 re-measured above.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 re-measured 15/23 → 18/26 |
| coverage | improved | C2 re-measured 4/6 → 6/6; U 7/7 held |
| operability | improved | C3 evidence-verified; gate 372 → 389/389, scan suites unchanged |
| freshness | unchanged | not claimed or scored; walker 2.17.0 → 2.17.2 move marked by SKILL erratum (`SKILL.md:1822`) and the superseding note |
| depth | unchanged | not claimed |
| adjacency | unchanged | `PROVINCE.md` unchanged; `~/.config/omarchy/**` refinement routed to r19 by the lane |

## 4. Discernment spot-check (`lessons/round-18.md` § Gate)

| Item | Lane decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S076 walker `src/data.rs` @ v2.17.2 | admit | `curl https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/data.rs` → 200, 26,338 B, sha256 `996db119…`; lines 156-161 | agree | digest equals the row anchor; lines 156-161 hold `env::var("XDG_RUNTIME_DIR")` … `socket_path.push("elephant.sock")` as quoted; `git ls-remote …walker refs/tags/v2.17.2` → `a515085f…`, as the row states |
| S091 host `/etc/xdg/walker/config.toml` | admit (host row) | `sha256sum /etc/xdg/walker/config.toml` → `3c5c6867…`; line 1 `force_keyboard_focus = false` | agree | digest equals the row anchor and the upstream S073 digest; the row claims file bytes only, not a running binary |
| S092 swaybg `swaybg.1.scd` @ v1.2.2 | admit | `curl …/swaybg/v1.2.2/swaybg.1.scd` → 200, 1,124 B, sha256 `68ed5503…`; lines 29-30 | agree | digest equals the anchor; the Gate line's 13-word quote ("Scaling mode for images: … Default is _stretch_.") is verbatim at 29-30, within 25 words |
| GitHub tree HTML pages as sole support (S094 secondary anchor) | reject as support; digest-only | `curl -sSL https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black \| sha256sum` twice → `1a3ddca5…`, then `4d001dc8…` | agree | the digest changes between two fetches seconds apart, so it cannot anchor; this confirms lesson M7 and `fetch-verify`'s 4 `CONFLICT`s. The credited raw `colors.toml` reproduces (200, 461 B, `dbdd13a6…`, line 4 `background = "#121212"`) |

New SOURCES row re-opened for its quote: S092 (above), agree. Census validate: exit 0, three historical W04 (S030/S042/S045), as at round start.

## 5. Trend verdicts

- **expansion: improved.** There are two admitted entries on ground rubric V did not cover at d9a5a18 (P3, P5). Each `source:` resolves to mined tier-A rows, and the sampled rows reproduce.
- **quality: improved.** The gate's false-local-edit arm was fixed (d9a5a18:3406 → b7148a1:3477 pipefail; 389/389) and receipts were re-cut with a producer header. The lane corrected its own overbroad SCORECARD sentence in an append. No sampled admitted entry failed re-check.
- **discernment: improved.** The closure sample agrees with the gate on 3 admits and 1 reject. The outside R17-V1/V2/V5 disagreements and audit F10 became lessons M1–M3 with QUALITY 24–26, each with a d9a5a18 red read above.

## 6. Routed defects (lane fixes next round)

1. **R18-V1 (S094 anchor):** the secondary anchor cites per-fetch GitHub HTML digests (re-shown above: `1a3ddca5…` ≠ `4d001dc8…`), so `fetch-verify` exits 1. Land the superseding row the lane planned (lesson M7).
2. **R18-V2 (criterion 26 receipt):** the d9a5a18 red-before for criterion 26 lives in `gate-rc-redbefore.txt` (no producer header) and in a w3 report (383/389). Commit a header-bound receipt (`tool_sha256`, `measured_commit`) of the swapped-block run, so QUALITY 24 holds for criterion 26's own evidence.
3. **R18-V3 (stale walker pins in sibling notes):** `walker-deep-r9.md`, `walker-live-surface.md`, `waybar-walker-plane.md` (and others: `grep -rln '2\.17\.0' corpus/`) still state 2.17.0 pins with no in-file pointer. Today the supersession is marked only in `SKILL.md` errata and `walker-route-r18.md`. Append a dated forward pointer (§Evidence standard: corrections sweep every mention).
4. **R18-V4 (S084 durability):** the docs.rs `latest` alias is unpinned. The re-opening seat advised re-pointing to the crate tarball; the row is unchanged.
5. **Carried, lane-listed:** frozen F1/F2 (blank-line pin reads mismatch; `link/.` bypasses the symlinked-dir check), and `measure-mutants.py` defaulting `--out` into the lane. Also jj-audit F6/F9 (not fixed, with reasons) and the three tripwire drafts.

Host evidence (operator-owned, not lane debt): `/var/log/pacman.log:3161-3169` shows
`[2026-10-20T13:23:08-0300] [PACMAN] Running 'pacman -U --needed --noconfirm … /home/vgpnk/.cache/yay/zcode/zcode-3.16.2-1-x86_64.pkg.tar.zst'` → `installed zcode (3.16.2-1)`,
then `pacman -D --asexplicit zcode` during the round (host pause in force). The yay cache path suggests an AUR-helper build [INFERENCE]. The actor is `[UNK]`; the lane's seat scan reports no mado tool call. R15-V1 stays operator-owned.

SHONEN: all four boxes are `[~]` author assertions, and box 2 cites no new end-to-end task.
They are not yet checkable by a non-author from this report; promotion is operator-owned.
