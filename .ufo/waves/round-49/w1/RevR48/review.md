# RevR48 — full review: round-48 closure routed items vs the lane at base

Seat RevR48, mado round 49 wave w1 (BUILD, policy v1), 2026-10-27.
- Base: `03e4ae76aff7a4be59cb69970dd553baa319695a` (round-48 verifier spot-check commit). Lane tip at review time: `5f37c1b8`
  (round-49 prep: claims, w1 spec, census-before, operator-state-before). Every tracked blob cited below was read at
  `03e4ae76` unless marked otherwise; the prep commit changed none of them.
- The round-48 report is a fleet-repo file: `.ufo/reports/round-48/mado.md` at fleet commit
  `a72080e7706d5a9ecd4c7bff1c8d2ca3d8f6d7d7` (it does not exist in the lane at any cited rev — `git show
  03e4ae76:.ufo/reports/round-48/mado.md` fails; first located in the fleet repo).
- Method: read-only. `git show` / `ls-tree` / `ls-files` / `grep` at pinned revs, `sha256sum -c`, `stat`, `wc`,
  one python census over committed fixture JSONs, and two outbound fetches (bytes receipted in this seat dir).
  No lane counter or gate was executed; no tracked file written; no git/jj mutation; scratch
  `/fast/scratch/hyaku/mado-r49/RevR48` created unused, removed at close. No tools installed.

## 1. N1 — report's "52 untracked `*.synthetic`" — CONFIRMED

Claim under review (spotcheck §6.1): fleet report `:37` says 52, actual 47.

- Text: `git -C /home/vgpnk/Projects/shokunin show a72080e7706d5a9ecd4c7bff1c8d2ca3d8f6d7d7:.ufo/reports/round-48/mado.md`,
  line 37: "Inherited state: the 52 untracked `*.synthetic` files under `.ufo/waves/round-45/` and `round-46/` predate this
  round and were left untouched (not lane-authored this round). Nothing else untracked at the tip."
- Actual count now (these files are still untracked): `git status --porcelain -uall | grep '\.synthetic$'` → **47**, broken
  down by seat dir: **45** under `waves/round-45/w1/RevengerOmarchy/`, **2** under `waves/round-46/w1/CritW2Gate/`. The
  report's directory claim (round-45/ and round-46/) is true; only the number 52 is wrong. (Today's tree additionally carries
  round-49 seat dirs untracked — expected mid-wave, not part of the historical claim.)
- Digests: `.ufo/waves/round-48/w1/ExecSessionMarker/SHA256SUMS` @03e4ae76 has 77 entries; `grep -c '\.synthetic'` → **48**;
  `sha256sum -c --quiet` over the synthetic subset, cwd = lane root → **ALL-MATCH** (all 48 files exist and hash equal).
- Composition of the 48: 47 untracked sidecars + **1 tracked in-seat demo copy**
  `.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py.synthetic` (first entry of the sums file; present in
  `git ls-files -- '*.synthetic'`). The lane tracks **100** `*.synthetic` files in total — ExecSessionMarker demo trees under
  `round-47/w1/ExecSessionMarker/demo/{sidecars,sidecars-refreshed}/` and `round-48/w1/ExecSessionMarker/sidecars/` mirror
  rounds-45/46/47 sidecars inside seat dirs.
- Consequence for the L1's commit-vs-remove decision: removing the 47 untracked files leaves the tracked demo mirrors and the
  sums file's 48th entry intact; the sums file remains a valid record but 47 of its paths stop existing.

## 2. N2 — `host_cache_untouched_sha256` records the w2 mutant's bytes — CONFIRMED

- `git show 03e4ae76:.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt` line 4:
  `host_cache_untouched_sha256=c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144`.
- `printf 'r48-w2\n' | sha256sum` → `c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144`. **Equal.** At the
  23:20:44 capture the operator cache held the M-WRITE mutant's 7 bytes, and the field name asserts the opposite.
- Lesson line exists: `corpus/lessons/round-48.md:263` (M48-10) — 7 B, mtime 1793064395, later resolver rewrite to 190 B at
  mtime 1793069967.
- Operator-owned before-digest receipt for this round exists and is honest:
  `git show 5f37c1b8:.ufo/waves/round-49/receipts/operator-state-before.txt` (2026-10-27T01:27:21-03:00):
  `~/.cache/xdg-terminal-exec sha256=ddd94f6bca4b… size=190 mtime=1793069967`, plus hypr config files and a ~/.local/bin
  census, labelled "never written by this lane".
- Live re-read today: `sha256sum ~/.cache/xdg-terminal-exec` → `ddd94f6bca4bcd42c426da9bbeb9955ca5d77b8778b4e290fcfffcc984a1b3d5`,
  `stat` → size 190, mtime 1793069967. Unchanged since the receipt.

## 3. N3 — stale "five gate decisions" — CONFIRMED

- `git show 03e4ae76:corpus/lessons/round-48.md` lines 424-425: "4. **Discernment spot-check** of the five gate decisions
  above (three admits, two rejects) on outside re-reading, agree or disagree, with the reason."
- Actual Gate content: `## Gate` at :25; the GATE block admits **12** rows (S340, S341, S342, S343, S344, S345, S346, S347,
  S348, S349, S351, S350); `### Rejected after opening` at :69 holds **3** `**REJECT**` bullets (count: `grep -c
  '\*\*REJECT\*\*'` over :69-109 → 3). Total 15 decisions; the stale sentence says 5 (3+2).

## 4. N4 — text matrix shows 96 of 98 variants — CONFIRMED exactly

- `receipts/v2/c2v2-revc2counter-summary.json` @03e4ae76: JSON **list of 98**; contains
  - `a-rev-base-direct`: rc 1, "admitted=0/1 verdict=TARGET_MISSED rev=579f6…",
  - `a-entry-at-base`: rc 2, "SETUP precondition_failed entry_present_at_ba…".
- `receipts/v2/c2v2-revc2counter-matrix.txt`: 100 lines = 2 header (`candidate …`, `row pins {…}`) + **96 variant rows**
  (95 lines matching `TARGET_(MET|MISSED)` + the `pos` row, which ends `admitted=1` without a TARGET_ token) + footer
  (`variants 98`, `HARNESS_EXIT=0`). `grep -cE 'a-entry-at-base|a-rev-base-direct'` on the matrix → **0**.
- Both spotcheck-named ids are exactly the two dropped rows. Note `a-entry-at-base` is a SETUP failure whose diagnostic text
  exists only in the JSON — the text receipt is the operator-facing artifact, so the drop hides the one variant whose failure
  mode is different in kind.

## 5. N5 — GitLab `-/raw/` anti-bot premise — NOT REPRODUCED (transient)

- Rows confirmed: `corpus/SOURCES.md` @03e4ae76 :295 (S346) and :296 (S347) carry
  `https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/…` URLs.
- Fetch 1 (2026-10-27T04:41:50Z, plain `curl -fsS`, default UA, no browser):
  URL `https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/symbols/br` →
  **HTTP/2 200**, `content-type: text/plain; charset=utf-8`, `x-cache-hits: 0`, **19592 bytes**, body starts
  `// Keyboard layouts for Brazil.` — the real file, not anti-bot HTML.
  sha256 = `8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e` = the S347 row's pin **exactly**.
  Receipt: `fetch-xkb-br-rawurl.bin` in this seat dir.
- Fetch 2 (same minute): files API
  `https://gitlab.freedesktop.org/api/v4/projects/xkeyboard-config%2Fxkeyboard-config/repository/files/symbols%2Fbr/raw?ref=xkeyboard-config-2.48`
  → sha256 `8cf65550…` (pin-equal). Receipt: `fetch-xkb-br-api.bin`.
- Reading: the spotcheck observed an anti-bot page earlier on 2026-10-27; four hours later the same URL serves the pinned
  bytes to the same class of fetcher. The routed fix ("note the API fallback") is worth keeping as *procedure*, but a note
  worded as "the `-/raw/` URL now returns an anti-bot page" would commit a standing falsehood. Recommend: phrase as
  intermittent ("observed once 2026-10-26/27; not reproduced 2026-10-27T04:41Z") and prefer the API URL for future freshness
  re-fetches while recording both.

## 6. Carried items

### M48-8 — session-material gate — CONFIRMED, plus one new defect (R2)
- Red at tip: `receipts/a4/session-material-tip.txt:4` `SESSION_MATERIAL: files=21985 findings=159 rev=d8e3d6003bf3b5de…`,
  exit=1; per-rule R1=38 R2=38 R3=58 R4=3 R5=22; waived findings=3 files=1.
- Scope arithmetic: `git ls-tree -r --name-only d8e3d600 -- .ufo | wc -l` → **21985** (= the receipt's files count);
  whole tree → 22250. The run used the default `.ufo`-only scope.
- Committed gate v2 @03e4ae76: argparse `--scope` choices ("ufo","all") **default "ufo"** at `:1606-1607`;
  `run(..., scope="ufo")` and `entries = list_tree(repo, sha, (".ufo",) if scope == "ufo" else (".",))` at `:787-788`;
  `list_tree` defaults to `(".ufo",)` at `:712`. Docstring (:13) "default: `.ufo/` only" agrees with the code.
- 16-of-19 shape gap: `w1/SentPrivacy/receipts/gate-on-shapes.txt` → `SESSION_MATERIAL: files=19 findings=3` (3 caught,
  16 with empty rule hits = missed); `class-verdicts.txt` lists the per-class entries with `"rules": []` for the missed
  shapes. Lesson M48-8 at `corpus/lessons/round-48.md:259` records the same numbers. (I did not re-run the scorer —
  closure standard; the committed receipts support the recorded state.)
- **NEW DEFECT R2 (stale locator):** the lesson cites `quality/check-session-material.py:256` for the `.ufo`-only scope.
  At the committed base bytes, `:256` is inside `_monitor_reason` (monitor-identity helper — verified by printing
  :250-258). The actual scope lines are `:787-788` and `:1606-1607`. `:256` IS correct for the **pre-rewrite** gate:
  `git show 5ff16742:quality/check-session-material.py` → `:256: raw = _git(repo, "ls-tree", "-r", "-z", sha, "--", ".ufo")`.
  The w1-era number was carried across the gate v2 rewrite (the rewrite deletes 31 lines; it is one of the round's three
  deletion sites) into a lesson committed at the tip. Same stale number in `w1/SentPrivacy.md` §2/D-A, where it was correct
  at its own scan time (rev 5ff16742). Fix: recompute the locator in the M48-8 fix-up line the round is already obliged to
  write.

### M48-10 — host-write containment — CONFIRMED; round-49 prerequisite in place
Lesson `:263` (see §2); byte proof is N2's digest equality; `receipts/operator-state-before.txt` @5f37c1b8 exists, labelled
operator-owned, and matches today's live stat. Nothing further owed from this seat.

### M48-13 — 1 MiB file cap vs the clone recipe — CONFIRMED
- Lesson `:269`: a4r1 context mandated `ulimit -f 2048` (1 MiB/file) while the lane tracks evidence files >1 MiB; checkout
  fails; two seats aborted with no report, two stalled, three used `--no-checkout` clones.
- Primary evidence re-read from `.ufo/waves/round-48/a4r1-results.json` @03e4ae76:
  - `:22` "Index lock >1MiB since huge index. … requirement max 1MiB per file. Git index >1MB, operations fail. …" (MadoA4RevC2v2Diff);
  - `:40` `{"aborted": true, "error": "Scratch clone checkout could not complete because RLIMIT_FSIZE=1 MiB rejects numerous committed large files; checkout left untracked remnants, preventing retry. …"}` (MadoA4RevC1Write/RevGate class);
  - `:28`, `:34` no-checkout workarounds (MadoA4CritEntry, MadoA4CritSalvage).
- Owed work still unrung: lesson `:467-469` (clause-r mutant attack not run; gate both-ways demo rests on selftest;
  v2 C2 attacks rest on the w2 harness). Round-49's dispatch raises the cap to 64 MiB/file (`ulimit -f 65536`) and keeps the
  explicit `git clone -q --shared` recipe — consistent with the fix direction (cap and recipe checked together, criterion 98
  extension).

### w2/SentScratch — counters accept a /tmp work dir — CONFIRMED as recorded
Report `.ufo/waves/round-48/w2/SentScratch.md` committed with F1-F7; its 11 receipts committed under
`w2/SentScratch/receipts/` (`c1-work-gate.txt`, `c1-work-cleanup.txt`, `c2-arg-gate.txt`, `containment-compare.txt`,
`fixture-write-bounds.txt`, `mode000-removal.txt`, `scratch-leftovers.txt`, `seat-bounds.txt`, `spec-bounds.txt`,
`tmp-paths.txt`, `tmp-residue.txt`). Spot-check of the code claims against the committed counters: c2 gates only TMPDIR
presence (no `--work`), c1's `--work` gate rejects repo/lane/fleet-parent/run/proc but not the tmpfs family — consistent
with F1/F2 as written. Round-49's rule (work dirs refuse /tmp) matches the proposed remediation.

### registration-v2.md residuals — CONFIRMED at :102-110
`git show 03e4ae76:.ufo/waves/round-48/registration-v2.md` :102-110: "## Residuals carried (declared, not repaired)" then
all six: receipt-header generator path (`receipts/` vs committed `tools/`); `fetch/xkbcommon-meson.build` pin cited by no
row (CritC2Pin F5); S346 generator chain not self-verifying (CritC2Pin F1); C2's trust root = mutual binding of copy and row
digest; owner-column justification unscored; C1's judge is the host's coreutils/bash.

## 7. Closure numbers re-derived (spotcheck cross-check — all pass)

| claim (spotcheck §2/§5) | command | result |
|---|---|---|
| SCORECARD +31/0, LOG +10/0, pure append | `git diff --numstat 579f694b b361c846 -- SCORECARD.md LOG.md` | `10 0 LOG.md`; `31 0 SCORECARD.md` ✓ |
| round deletes 67 lines in exactly 3 files | `git diff --numstat 579f694b b361c846` filtered to deletions>0 | SKILL.md 136/1; quality/check-session-material.py 992/31; tools/mado-terminal.py 441/35 → 1+31+35=67 ✓ |
| knowledge 64 → 65 | `ls-tree --name-only …:corpus/knowledge/ \| wc -l` at 579f694b / 03e4ae76 | 64; 65 ✓ |
| SOURCES rows 276 → 288 | row-regex count at both revs | 276; 288 ✓ |
| fixtures 228 = 204 + 24; 10 `v2-hu-*`; 10 READDIR | python census over `quality/counters/c1-r48-fixtures{,-v2}.json` @03e4ae76 | 228; 204; 24; 10; 10 ✓ |
| a4 gate receipt scanned .ufo only | `files=21985` vs `ls-tree -r --name-only d8e3d600 -- .ufo \| wc -l` | 21985 = 21985 ✓ |
| SentPrivacy shapes 19/3/16 | `gate-on-shapes.txt` (`files=19 findings=3`) + `class-verdicts.txt` empty-rules entries | ✓ |

## 8. Defects the closure missed

- **R1 — N5 premise is transient (Medium, affects the freeze text).** See §5. The routed fix, worded as it is, would append a
  standing claim that failed to reproduce within hours. Keep the API fallback as the freshness procedure; word the note as an
  intermittent observation with both timestamps.
- **R2 — stale locator in the committed M48-8 lesson (Low).** `check-session-material.py:256` → actual `:787-788` /
  `:1606-1607` in the committed v2 gate; `:256` true only of the pre-rewrite blob at `5ff16742`. Recompute in the M48-8
  fix-up. (Same number in `w1/SentPrivacy.md` was correct at its scan rev; the lesson is the artifact that must carry a
  computed locator.)
- **R3 — second row-dropping receipt (Low).** `.ufo/waves/round-48/w2/RevC1Fixtures/boundary.log` = 17 rows;
  `boundary.json` = 18 entries; the `primed-cache (terminator line 11)` variant (entry 0, state=hit) appears only in the
  JSON. Same class as N4, seat-level receipt (the JSON is complete, so no evidence is lost; any text-only consumer
  undercounts the boundary sweep by one variant). Sibling pairs checked: `order` (18 json / 19 log — header line),
  `readdir` (dict+11 n-rows vs 14-line log, content-aligned), `rootsubst` (12 dynamic rows + static + masking = 14-line
  log) — no other drops found.
- **R4 — sidecar ledger nuance (informational).** The "47 sidecars" narrative counts untracked files only; the lane also
  tracks 100 `*.synthetic` demo mirrors (round-47/48 ExecSessionMarker demo trees), and `SHA256SUMS` covers 48 synthetic
  entries (47 + 1 in-seat tracked). The L1's commit-vs-remove receipt should state the sums file spans both classes and
  that removal of the 47 does not affect the tracked mirrors.

## 9. Residual risk / verification gaps

- No counter or gate executed (closure standard kept): M48-8's 16/19 tally rests on committed receipts + lesson; the 16 MiB
  MAX_TEXT truncation (SentPrivacy D-C) and the R5/R6 serial rules were not re-derived here.
- N5: one clean fetch proves the standing claim failed to reproduce at 2026-10-27T04:41Z; it cannot prove anti-bot never
  triggers (time/IP/rate dependent).
- The round-48 report is fleet-repo state; N1's correction lands in the next fleet report with the counting command cited.
- The historical "nothing else untracked at the tip" half of N1 was taken from the spotcheck's own check (the round-48-tip
  tree is not reconstructible as a working tree now); the synthetic census and its seat breakdown were re-derived live.

## 10. Evidence receipts in this seat dir

- `fetch-xkb-br-rawurl.bin` — GET `https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/symbols/br`,
  2026-10-27T04:41:50Z, HTTP/2 200, text/plain, 19592 B, `x-cache-hits: 0`, curl default UA.
  sha256 `8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e` (= S347 pin).
- `fetch-xkb-br-api.bin` — GET `https://gitlab.freedesktop.org/api/v4/projects/xkeyboard-config%2Fxkeyboard-config/repository/files/symbols%2Fbr/raw?ref=xkeyboard-config-2.48`,
  same minute. sha256 `8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e`.
