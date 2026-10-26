author: hyaku closure (non-author integrator, @m_opus)

# mado round 44 — non-author closure spot-check (attempt 1)

Lane HEAD before `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, after `8ac15c412051874836e0db36b1178723ade6c340`.
Driver digest (`.ufo/watchdog.log`, mutable — copied here):
`2026-10-26T13:00:54-03:00 launch mado round=44 pgid=304371 driver=hyaku-inline attempt=1` /
`2026-10-26T15:12:15-03:00 complete mado round=44; hyaku-inline attempt=1` (`watchdog.log:1531,1541`; one launch, one completion).
I did not author the round. Re-checks ran on committed bytes (`git show`/`git ls-tree` at the cited revisions), on upstream raw files
re-fetched today, and read-only on the host (`hyprctl clients -j` piped straight into the tool; nothing written). The deliverable
`tools/mado-geometry.py` was run from committed bytes in a scratch directory. I ran the two claim counters
(`quality/counters/c1-r44-geometry-states-v2.py`, `c2-r44-gkeep-size-request-v2.py`) as measurements with a `/tmp` work dir; they are
not registry gates (`SKILL.md` registry has no row for them), and `git status --porcelain` stayed empty. I did not execute the registered
gate `mado-axis-scores` (`SKILL.md:769`): its committed evidence is verified instead, and its inputs are re-derived plainly.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-44/mado.md` | `mado-shokunin 5c0676bea9523b18caa8709aa6d49e9be1a3e950 2026-10-26 15:11:52 -0300` |
| report lands after the lane commit | commit times | lane tip `8ac15c4` 15:11:30, report 15:11:52 → commit-then-report holds |
| prompt committed, template contract | `git log -- .ufo/prompts/mado-round-44.md`; `diff` of prompt lines 1-140 vs `kimi-shokunin/templates/round-prompt.md` (140 lines) | `mado-shokunin 9c29c166…` 13:00:51 (before launch); every differing line is a rendered placeholder (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §6 hyaku addendum and §7 scratch directive follow |
| SHONEN heading | report `## SHONEN` | present, 4 lines, all `[~]` with pointers |
| cited commits exist + ancestors of `master` | `git cat-file -e <h>^{commit}`; `git merge-base --is-ancestor <h> master` for 6a1a905, e228951, ae996fc, 03fa5c6, e467892, 290cdde, 74c606a, 8ac15c4 | all 8 exist, all ancestors; the 7 round commits are authored `mado-shokunin`. `241196d` (operator `considerthese: 2026-10-26`) also sits in the range — operator's, not round work |
| pushed, clean | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=8ac15c41… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `8ac15c41…` |
| L2 floor | `jq` on `w1-results.json`, `w2-results.json`; `ls w1/*.md w2/*.md` | 38/38 and 33/33 results, 38 + 33 reports (71 seats, 0 dead) |
| real report, not a marker | 7 lane commits; `git diff --stat 6a1a905 8ac15c41 -- . ':!.ufo'` | 16 files +2986/−15 outside `.ufo/` → status `ok` |
| round-43 routed items | lesson `## Round-43 closure items`, `## Round-43 errata` | D3 corrected in `SKILL.md` (verified in the diff, below); D7 tip axis receipt committed (`receipts/axis-tip.txt`); D1/D4/D5 errata appended; D2 deferred with reason (lesson `:93`) |

## 2. Per-claim re-check

| claim | plain measurement (base → tip) | observed | reported | ruling |
|---|---|---|---|---|
| C1 operability — tool names FULLSCREEN/MAXIMIZED, NOT_COMPARED exit 5 | `git show <rev>:tools/mado-geometry.py \| sha256sum`; `grep -c -E 'FULLSCREEN\|MAXIMIZED\|NOT_COMPARED'` | base `e3c2e471…`, 0 hits → data `e467892` and tip `1da3ddae…`, 10 hits | tool changed at data, unchanged to tip | **verified (re-measured)** |
| C1 behaviour | my own dumps: `fs.json` (gkeep floating, `fullscreen` 2 at 1920x1080 and 1 at 1900x1040) and `mix.json` (one fullscreen, one 800x600 floating) with rules `size 800 600` + `float on` for `gkeep`, base vs tip tool | base: both `DIFFER`, exit 1 / `DIFFER`+`AGREE`, exit 1. Tip: `FULLSCREEN`, `MAXIMIZED`, `maximized=1 fullscreen=1 verdict=NOT_COMPARED`, exit 5 / `FULLSCREEN`+`AGREE`, `verdict=OK`, exit 0 | contract text in the tool docstring and `SKILL.md` exit map | **verified** |
| C1 selftest | `python3 <rev tool> --selftest` | base `73/73`, tip `94/94 passed`, exit 0 | 94/94 | **verified** |
| C1 counter | `python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo . --rev <rev> --work /tmp/…` | base `fixtures=15/26 … TARGET_MISSED`, clauses `a:1 b:0 b4:0 b5:0 e:1 g:1 r:1`, exit 1; tip `8ac15c41` `fixtures=26/26 … TARGET_MET`, all clauses 1, clause r `37/37`, exit 0 | base `11/26` MISSED; data/tip `26/26` MET | **verified**; base share differs (15 vs 11) — nonce-dependent as `registration-v2.md` declares; verdict stable (routed D4) |
| C1 grounding | `fetch-c1/Hyprland-FullscreenController.hpp:12-16` | `FSMODE_NONE = 0, FSMODE_MAXIMIZED, FSMODE_FULLSCREEN` — 1 maximized, 2 fullscreen as the tool reads them | same | **agree** |
| C1 live (SHONEN box 2) | `hyprctl clients -j \| python3 -I <tip tool> --clients - --rules ~/.config/hypr/gkeep.conf`; `sha256sum ~/.config/hypr/gkeep.conf` | `clients=3 matched=0 … verdict=NO_MATCHING_CLIENT`, exit 3; conf `3726e488…`; Hyprland 0.56.2 `efb50993…` | `receipts/live-geometry-host-r44.txt` same line, exit 3 | **agree** |
| C2 coverage (sourced) — `corpus/knowledge/hyprland-gkeep-size-request-r44.md` | `git cat-file -e <rev>:<entry>`; `git ls-tree -r --name-only <rev> corpus/knowledge \| wc -l`; `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | entry absent → present (83 lines); knowledge 60 → 61; rows 234 → 238 (S298-S301 new, none removed) | same | **verified (re-measured)** |
| C2 counter | `python3 -I quality/counters/c2-r44-gkeep-size-request-v2.py --repo . --rev <rev>` | base `admitted=0/1 … TARGET_MISSED` (all clauses 0); tip `8ac15c41` `admitted=1/1 … TARGET_MET`, clauses a-j all 1 | same | **verified** |
| C2 Gate bindings | upstream re-fetch of the five Gate URLs, `sha256sum`, `grep -nF <quote>` (S299 whitespace-flattened: the quote wraps two lines) | all five live sha256 equal the pins (`d735d454…`, `d90b534c…`, `7ba7f9c8…`, `0ee38458…`, `07a3c4a5…`); quotes at `Window.cpp:1687`, `XDGShell.cpp:455`, `xdg-shell.xml:1150-1151`, `gdktoplevel-wayland.c:681`, `ui.py:475-476`; each ≤25 words (S299 18) | same locators | **verified** |
| C2 content (non-author reading) | entry claims opened at their receipt lines: `Window.cpp:1514,1520-1526` (onAck), `:1732,1743-1744` (sendWindowSize early return), `:1861-1865` (getReportedSize → `m_current.ackedSize`); `XDGShell.cpp:354-358` (setSize), `:601-605` (stale-ack drop); `xdg-shell.xml:839-861` (maximized must obey; fullscreen/resizing a maximum); `ui.py:87-88,449,476` | every sampled sentence supported; the entry marks the pending→current ack promotion UNK rather than claiming it; S301 "no size request; min-width/min-height only on a button style" holds (`grep size_request` 0) | v2 scores bookkeeping (clause j has no range-width bound — lane-declared); content is the non-author reading | **supported — real receipt-backed coverage** |

Evidence-verified only (registered gate, not executed): `receipts/axis-base.txt` `MADO_AXIS: checked=3 mismatched=0 rev=6a1a905…`;
`receipts/axis-tip.txt` `checked=3 mismatched=0 rev=74c606a…` (navigation 61/61, calibration 71/71, operability 12/12). `74c606a..8ac15c41`
touches only `.ufo/waves/round-44/` (`git diff --name-only … \| grep -v '^.ufo/waves/round-44/'` empty), so that receipt describes the tip's
axis inputs. Controls: `receipts/ctl-c1-v2.txt` `CTL_C1v2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 20; reference met: 1)`;
`receipts/ctl-c2-v2.txt` `CTL_C2v2 VERDICT: PASS (wrong=0 of 11; positive admitted=1)`. Lane-declared open predicate defects stand
(C1 v2 cheat-h MET, mutant M01 survives; C2 v2 clause j admits whole-file locators, 7 forgeries, 18 mutant survivors) — which is why C1
behaviour and C2 content were re-checked directly above.

Harm watch: `git diff 6a1a905 8ac15c41 -- SCORECARD.md` is a pure append (+29: Round 44 section, capability row, axis line). Outside `.ufo/`
(`git diff --numstat`): LOG +8, QUALITY +6, README +19, PROVINCE +1/−1 and SKILL +12/−1 (the tool row and exit-map line extended, the D3
correction appended), SOURCES +5/−1 where the deletion is S164 whose only changed cell (index 11, `used-by`) gains one appended item.
Axis inputs re-derived plainly: README distinct `knowledge/*.md` links 60 → 61; QUALITY numbered criteria 81 → 84 (+3 = published
calibration 68 → 71). No axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured: base tool DIFFER on state clients → tip FULLSCREEN/MAXIMIZED and NOT_COMPARED exit 5 on my own dumps; selftest 73 → 94; counter 26/26 MET at the tip; live NO_MATCHING_CLIENT reproduced |
| coverage | improved | C2 re-measured: entry 0 → 1, knowledge 60 → 61, rows 234 → 238, all five pins byte-equal to upstream today, sampled entry claims supported at their lines |
| depth | unchanged | SKILL gains three licence rows and the D3 correction; no new decision table beyond the tool's verdicts |
| freshness | unchanged | new pins opened 2026-10-26; no held claim re-verified as stale or fixed |
| calibration | unchanged | v1 → v2 re-registration before data with controls; axis fraction stays 1.0 (68/68 → 71/71) |
| adjacency | unchanged | PROVINCE tool-row note only; sibling overlap scans recorded, nothing absorbed |

## 4. Discernment spot-check (`corpus/lessons/round-44.md` `## Gate` and assimilation ledger)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `ADMIT gkeep-client-size-request-r12.md` as `hyprland-gkeep-size-request-r44.md` | admit | staged file `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md`; entry `:1-12`; pins above | **agree** | Re-grounded by document at the host's commit (tag-form Window.cpp URL → held S164 commit URL; ui.py → S301); r12's "chain is now complete" and "rendered geometry is 420x500" not adopted; ack promotion left UNK. |
| `GATE S298` / new row S298 | admit (tier A, `code`) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/protocols/XDGShell.cpp` re-fetched: sha256 `d90b534c…` = pin and row; quote at `:455`; setSize at `:354-358` | **agree** | Quote is one statement (3 whitespace tokens), single line, located; row's locator ranges land on setSize and the deferred `sendConfigure`; `opened 2026-10-26`, `used-by` the entry. |
| `REFUSE gkeep-rendered-geometry-record-r13.md` | reject | staged r13 `:10-14,65-73`; staged `SOURCES.append.md:124` (S320); `git ls-tree -r --name-only 8ac15c41 \| grep -c 'lanes/mado/round1[345]/fetch'` → 0 | **agree** | Its decisive S320 is a host-journal sweep held only in the shokuknow checkout (`shokuknow/lanes/mado/round13/fetch/host-journal-map-log-sweep.txt` exists there), not in this lane; the round makes no log claim. The flip is cheap — an in-lane re-run of the sweep — and is correctly stated. |
| S164 row edit (`used-by`) | registry edit | `git diff 6a1a905 8ac15c41 -- corpus/SOURCES.md` cell-by-cell | **agree** | 13 cells both sides; only cell 11 differs, by one appended item; logged old→new in the lesson. |
| new row S301 | admit (tier A, `code`) | `https://raw.githubusercontent.com/VeigaPunk/gkeep/133b8671…/gkeep/ui.py` re-fetched: sha256 `07a3c4a5…` = pin; quote at `:475-476`; `application_id` at `:449`; `min-width/min-height` at `:87-88` | **agree** | Quote 3 whitespace tokens spanning two adjacent lines, as the Gate note discloses; `teaches` cell ("no size request; its only min sizes belong to a button style") holds (`grep size_request` → 0). |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → W04 ×7 (S030, S042, S045,
S097, S119, S120, S121) + W01 S277, `mado ok`, exit 0 — identical to `receipts/census-before.txt` and `census-after.txt`.

## 5. Trend verdicts

- **expansion: improved** — one capability extension shown running (my dumps; live host run), one knowledge entry on ground absent at
  base (`receipts/c2-ground-base.txt` exit 1; knowledge 60 → 61), rows 234 → 238, all four new rows' bytes re-verified upstream today.
- **quality: improved** — both instruments re-registered before data after w1 broke them (controls 0 of 20, 0 of 11); w2's entry/SKILL
  findings corrected in `74c606a`; round-43 D3 corrected and D7 tip receipt committed. Limit: a round-43 session-material leak flagged by
  this round's own seat was left tracked (D1).
- **discernment: improved** — 5/5 sampled gate decisions (two admits, one refusal, one new row, one registry edit) agree on outside
  re-reading; the lane withdrew its own premise wording on critic evidence. Limit: SentLiveReads S1 ("L1 for the round-43 file") did not
  reach the lesson.

Closure: status `ok`, **admitted=true**, verdict `admitted` — both claims verify, no axis harmed.

## 6. Routed defects (lane fixes next round)

1. D1 — session material tracked at `8ac15c41`: `.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` (32 keys per client, 4
   live window titles; `git show 8ac15c41:<path> | grep -c '"title"'` → 4) and, not flagged by any seat, `.ufo/waves/round-43/w2/SentLiveRun/dump-now.json`
   (4 live titles, same `grep -c`). Violates `SKILL.md:343` (rule 4, "Session material stays shape-only … never window titles") and
   `SKILL.md:33`. Round 44 projected its own copies (`w1/SentLiveReads.md:62`) but left these; the lesson does not record the S1 finding.
   Fix in a new commit: project both files to the 7-key shape of `.ufo/waves/round-43/fetch/host-clients-r43.json` (`address, at, class,
   floating, mapped, monitor, size`), sweep every tracked live `clients -j` dump for `title`/`initialTitle`, and book a lesson mistake.
   The round-43 `ExecOracleGkeep` dumps carry only titles of the seat's own gkeep test windows — check and state it in that sweep.
   **Operator note:** the titles stay in pushed history (`2a3707c8`, `58466627`) unless history is rewritten; rewriting is the operator's
   decision, never a lane action.
2. D2 — `SCORECARD.md` Round 44 claim rows give the after-state as "see `receipts/c1-after-data.txt`" / "`receipts/c2-after-data.txt`" and
   the self-verdict as "recorded in the round report from the receipts": the published table carries no after value or verdict. Append the
   values (C1 `fixtures=26/26 TARGET_MET`, C2 `admitted=1/1 TARGET_MET`) in the next SCORECARD section; never rewrite.
3. D3 — tip receipts (`c1-after-tip`, `c2-after-tip`, `axis-tip`) name `74c606a`, not the lane tip `8ac15c41`; equivalent here because the last
   commit touches only `.ufo/waves/round-44/`, but state that equivalence in the receipt or measure the final tip.
4. D4 — C1 v2 base share is nonce-dependent (receipt `11/26`, my re-run `15/26`): a "before" number that does not reproduce is not a count.
   Report the deterministic part (clauses) as the before-state, or seed the lattice.
5. D5 — open predicate defects (lane-declared, w2): C1 v2 cheat-h (`w2/CritC1V2Cheat.md`) MET, mutant M01 survives (`w2/MutC1V2.md`);
   C2 v2 clause j has no locator range-width bound (`w2/ExecDoNothingV2.md` O1, `w2/CritC2V2Forgery.md` 7 admitted), 18 survivors
   (`w2/MutC2V2.md`). Re-register before reuse.
6. D6 — still open from round 43: D2 (S293 title / S290-S297 cell supersession) deferred to round 45 per SCORECARD plan item 2.
7. D7 — `w2/ConnCalibration.md` content mismatches (LOG mistake range, w1 paths cited before they landed, a QUALITY check path absent at the
   data commit) — the lane recorded them; correct by appended errata.

SHONEN boxes remain `[~]`. Box 2 (live run) is reproducible by a non-author — I reproduced its `NO_MATCHING_CLIENT`, exit 3 — and box 3
rests on committed independent-rebuild reports (`w1/ExecIndepA.md`, `w1/ExecIndepB.md`, `w2/ExecIndepV2.md`); promotion review is
operator-owned.
