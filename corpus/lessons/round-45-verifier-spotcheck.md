author: hyaku closure (non-author integrator, @m_opus)

# mado round 45 — non-author closure spot-check (attempt 1)

Lane HEAD before `0c89478af821a6424c9ac922eafe02e39630cf4f`, after `4d22eeb66c2835af8aaa3fac6ad838fa616aa663`.
Driver digest (`.ufo/watchdog.log`, mutable — copied here):
`2026-10-26T15:20:26-03:00 launch mado round=45 pgid=2926682 driver=hyaku-inline attempt=1` /
`2026-10-26T16:55:41-03:00 complete mado round=45; hyaku-inline attempt=1` (one launch, one completion).
I did not author the round. Re-checks ran on committed bytes (`git show`/`git ls-tree`/`git grep` at the cited revisions), on upstream
raw files re-fetched 2026-10-26, and read-only on the host (`hyprctl monitors all -j` piped straight into the tool; nothing written).
The deliverable `tools/mado-monitors.py` was run from committed bytes (`git show 4d22eeb:tools/mado-monitors.py`, sha256 `2f007417…`,
equal to the live receipt's tool hash) in a `/tmp` scratch directory. I ran the two claim counters
(`quality/counters/c1-r45-monitors-v2.py`, `c2-r45-monitor-entry-v2.py`) as measurements: they have no registry row (`SKILL.md`
registry holds only `mado-axis-scores`, `SKILL.md:769`), so they are not registered gates. I did not execute the registered gate
`mado-axis-scores` nor the new `quality/check-session-material.py`: their committed evidence is verified instead.
`git status --porcelain` in the lane was unchanged by my runs (one pre-existing untracked file, below).

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-45/mado.md` (fleet repo) | `mado-shokunin 4f8a65b7df8be7e6e7d8741a044bb1de7d7fbd4f 2026-10-26 16:55:02 -0300` |
| report lands after the lane commit | commit times | lane tip `4d22eeb` 16:54:18, report 16:55:02 → commit-then-report holds |
| prompt committed, template contract | `git log -- .ufo/prompts/mado-round-45.md`; `diff` of prompt lines 1-140 vs `templates/round-prompt.md` (140 lines, `cmp`-equal to `kimi-shokunin/templates/round-prompt.md`) | `mado-shokunin 1b08ce90` 15:20:24 (before launch); every differing line is a rendered `{{…}}` placeholder; §6 hyaku addendum and §7 scratch discipline follow |
| SHONEN heading | report `## SHONEN` | present, 4 lines, all `[~]` with pointers |
| cited commits exist + ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for 0c89478, 22a8ded, ebdba13, 7c0b003, ee6659b, ac3f9de, 4d22eeb | all 7 `commit`, all `anc=0`; the 6 round commits are authored and committed by `mado-shokunin <mado@shokunin.local>` |
| pushed | `scripts/hyaku/jj-lane.sh state …`; `git ls-remote origin refs/heads/master` | `local=remote=4d22eeb6… ahead=0 behind=0 head=detached tracked=0 untracked=1`; remote `4d22eeb6…` |
| leftovers | `git status --porcelain` | `?? .ufo/waves/round-45/w1/MutC1Counter/results.json` (4,020,571 B; disclosed in the report; its `summary.txt`/`matrix.md` are committed) → D4 |
| L2 floor / round size | `git ls-tree --name-only 4d22eeb .ufo/waves/round-45/w1/ \| grep -c '\.md$'`; `jq '{seats, n:(.results\|length)}' w1-results.json`; `git ls-tree -r … \| grep -c '^w2'` | 41 reports; `seats=41 n=41`, every `output: null` (orchestrator kernel restart, noted in-file); w2 absent (0). Round total 41 < the run-9 64-seat floor (prompt §6 :152-154) → D1 |
| real report, not a marker | `git diff --stat 0c89478 4d22eeb -- . ':!.ufo'` | 15 files, +3768/−0 outside `.ufo/` → status `ok` |
| round-44 routed items | lesson `## Round-44 closure items` | D1 fixed (re-checked: both round-43 dumps now 7-key, `grep -c '"title"'` → 0 each); D2 values appended in SCORECARD Round 45; D3 tip receipt names `ac3f9de` and states the last commit adds only receipts; D4 → M45-6; D6 deferred again; D7 recorded, not corrected → D6 below |

## 2. Per-claim re-check

| claim | plain measurement (base → tip) | observed | reported | ruling |
|---|---|---|---|---|
| C1 operability (capability) — `tools/mado-monitors.py` | `git cat-file -e <rev>:tools/mado-monitors.py` | base absent → tip present | same | **verified** |
| C1 counter (re-measured, fresh nonce) | `python3 -I quality/counters/c1-r45-monitors-v2.py --repo . --rev <rev> --work /tmp/…` | base `fixtures=0/81 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` exit 1 (seeds 45,1372511230); tip `4d22eeb` `fixtures=81/81 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` exit 0 (seeds 45,2969453451) | base same; data `ee6659b` same MET (seeds 45,2279173463) | **verified** |
| C1 freeze integrity | `git diff --stat 7c0b003 4d22eeb -- quality/counters/c1-r45-monitors-v2.py quality/counters/c2-r45-monitor-entry-v2.py .ufo/waves/round-45/registration-v2.md .ufo/waves/round-45/v2` | empty: counters, registration and v2 reference unchanged from the pre-data freeze to the tip | — | **verified** |
| C1 live (SHONEN box 2) | `hyprctl monitors all -j \| python3 -I <tip tool> --monitors - --config ~/.config/hypr/monitors.conf` | Hyprland 0.56.2 `efb50993`; conf sha256 `69c9d899…` (= receipt); `rule n=1 sel="DP-1" mode=3440x1440@100.00 …`, `DP-1 … verdict=AGREE`, `MADO_MONITORS: … agree=1 differ=0 … verdict=OK`, exit 0 | `receipts/live-monitors-host-r45.txt` identical | **verified** |
| C1 can fail | same pipe with a scratch copy of the conf (`@100`→`@60`, `3440x1440`→`2560x1440`) | `differ=mode verdict=DIFFER`, `agree=0 differ=1 … verdict=DIFFER`, exit 1 (as the docstring's exit map, tool `:100-103`) | — | **verified** |
| C1 read-only | `grep -nE '^\s*(import\|from) '`; `grep -nE 'socket\|subprocess\|os\.system\|Popen\|urllib'` on the tip tool | imports json, math, os, re, stat, struct, sys only; the one pattern hit is the docstring sentence at `:26` | "starts no process, opens no socket" | **agree** |
| C1 controls (evidence-verified) | `receipts/ctl-c1-v2.txt` | `CTL_C1v2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 45; reference met: 1)`, exit 0 | same | **verified** |
| C2 coverage (sourced) — `corpus/knowledge/hyprland-monitor-rule-r45.md` | `git cat-file -e`; `git ls-tree -r --name-only <rev> corpus/knowledge \| wc -l`; README `` grep -cE '^\| `knowledge/' ``; `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | entry absent → present; knowledge 61 → 62; README index rows 61 → 62; rows 238 → 252; S302-S315 all tier A, `mined`, opened 2026-10-26, used-by the entry | same | **verified** |
| C2 ground absent at base | `git grep -n -E 'parseMode\|parsePosition\|parseScale\|searchScale\|MonitorRuleManager\|applyMonitorRule\|handleMonitor' <rev> -- corpus SKILL.md` | base exit 1 (no hit); tip exit 0 (SOURCES 4, entry 8, lesson 2) | `receipts/c2-ground-base.txt` exit 1 | **verified** |
| C2 counter (re-measured) | `python3 -I quality/counters/c2-r45-monitor-entry-v2.py --repo . --rev <rev>` | base `clauses a-j all 0 admitted=0/1 TARGET_MISSED` exit 1; tip `4d22eeb` `clauses a-j all 1 admitted=1/1 TARGET_MET` exit 0 | same | **verified** |
| C2 controls (evidence-verified) | `receipts/ctl-c2-v2.txt` | `CTL_C2v2 VERDICT: PASS (wrong=0 of 15; positive admitted=1)` | same | **verified** |
| C2 entry head | `git show 4d22eeb:<entry> \| head` | provenance trio first: 14 `source: S302…S315` lines, `verified-at: 2026-10-26`, `recheck: on-release …`, `ground:` U5 | — | **agree** |

Evidence-verified only (registered gate, not executed): `receipts/axis-base.txt` `MADO_AXIS: checked=3 mismatched=0 rev=0c89478…`
(navigation 61/61, calibration 71/71, operability 12/12); `receipts/axis-tip.txt` `checked=3 mismatched=0 rev=ac3f9de…` (62/62, 73/73,
12/12); `receipts/axis-data.txt` STALE ×2 at `ee6659b` — the declared two-phase window (publication follows in `ac3f9de`).
`ac3f9de..4d22eeb` adds only receipts/wave files (the tip receipt states this). The new `quality/check-session-material.py` exits 1 at
the data commit (`receipts/session-material-data.txt`: `findings=97`, 49 synthetic by the lane's count) — red, reported by the lane → D3.

Harm watch: `git diff 0c89478 4d22eeb -- SCORECARD.md` is a pure append (+32: Round 45 section, capability row, axis line, planned).
`git diff --numstat` outside `.ufo/`: insertions only (LOG +10, PROVINCE +3, SKILL +5, QUALITY +5, README +3, SOURCES +14, entry +107,
lesson +81, tool, counters, gate). The only deletions in the round are the two round-43 dumps projected for round-44 D1 (−133 each).
Axis inputs re-derived plainly: README knowledge index 61 → 62 (navigation 61/61 → 62/62); QUALITY gains 85-86 (+2 = calibration 71 → 73).
No axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured: tool absent → present; counter 81/81 + 150/150 MET at the tip under my own nonce; live AGREE/OK and a DIFFER exit 1 on an altered scratch conf reproduced |
| coverage | improved | C2 re-measured: entry 0 → 1, knowledge 61 → 62, rows 238 → 252, ground grep exit 1 → 0, counter 1/1 MET at the tip, sampled pins byte-equal to upstream |
| depth | unchanged | SKILL gains one tool section (verdict/exit map, `monitors all` note); no new held decision table re-graded |
| freshness | unchanged | new pins opened 2026-10-26 with a precise on-release recheck; no held claim re-verified as stale or fixed |
| calibration | unchanged | v1 → v2 re-registration before data with controls 0 of 45 / 0 of 15; axis fraction stays 1.0 (71/71 → 73/73); M45-2 undercounts the serial's spread (D2) |
| adjacency | unchanged | PROVINCE refinement only; `w1/ScoutSiblings.md` 0 sibling lanes on the monitor plane; nothing absorbed |

## 4. Discernment spot-check (`corpus/lessons/round-45.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `GATE S306` / row S306 | admit (tier A, `code`) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/output/Monitor.cpp` re-fetched: 112738 B, sha256 `9cf88e15…` = pin and row; quote at `:1001` (`float    searchScale = std::round(m_scale * 120.0);`, whitespace-normalized as the lesson declares) | **agree** | `:996-1025` shows the integrality test, the 1/120 search and `i < 90` — the row's `teaches` ("corrected to a 1/120 step") is grounded; quote ≤25 words. |
| `GATE S312` / row S312 | admit (tier A, `code`) | `…/efb50993…/src/macros.hpp` re-fetched: 10778 B, sha256 `b62d5140…` = pin; quote verbatim at `:40` | **agree** | Strict `<` on `abs(a-b)` — the entry's "strictly less than 1 px and 1 Hz" follows. |
| `GATE S313` / row S313 | admit (tier A, `code`) | `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/math/Vector2D.hpp` re-fetched: 8301 B, sha256 `967bd9d7…` = pin; `operator/(const double& a)` at `:39`, `double x = 0; double y = 0;` at `:21-22` | **agree** | Doubles held and divided; supports both the row and the float32 rejection below. |
| REJECT `w1/CritToolSemantics` finding 1 (float32 integrality) | reject | S306 `:996` `Vector2D logicalSize = m_pixelSize / m_scale;` with S313 `:39` | **agree** | `m_scale` is promoted to `double` by the `const double&` operator; the integrality comparison runs on doubles, so a float32 model of the logical size is wrong. (The search counter itself is `float`, which the rejection does not contradict.) |
| REJECT hyprland-wiki Monitors.md at main | reject | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Monitors.md` → HTTP 404; GitHub API commit `e99eac80a6` (2026-04-26, "Update Configuration pages for the new lua configuration system") removes it; current `…/main/content/configuring/core/monitors/_index.md` (5324 B): 4 `hl.monitor(` hits, 0 `monitor =` lines | **agree** | Main documents only the Lua form; the hyprlang-era pin S310 (`ecc06f3b`, sha256 `f2ac7025…` re-fetched = pin, quote `monitor = name, resolution, position, scale` at `:11`) is the right source for a 0.56.2 host. |

SOURCES row re-opened for its quote: S310 (quote at `:11`, 6 words) and S312 (`:40`, ≤25 words) — both present at the pinned revisions.
Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → W04 ×7 (S030, S042,
S045, S097, S119, S120, S121) + W01 S277 + W04 S303, S307 (held URLs under a new scope), `mado ok`, exit 0 — identical to `receipts/census-after.txt`.

## 5. Trend verdicts

- **expansion: improved** — one capability shown running (my live run and a DIFFER probe), one knowledge entry on ground absent at base
  (ground grep exit 1 → 0; knowledge 61 → 62), rows 238 → 252, all sampled pins byte-equal to upstream today.
- **quality: unprovable-but-better** — as the named non-author reviewer: both instruments were re-registered before data after w1 broke
  them (v1: 16 C1 cheats/controls and 9 C2 forgeries met; v2: 0 of 45, 0 of 15), the round-43 title leak (round-44 D1) is projected and a
  privacy gate shown able to fail landed. No held entry was superseded or re-verified, the planned w2 never attacked the landed bytes,
  and the new gate is red at the data commit with 48 un-triaged pre-existing findings — better, not countably improved.
- **discernment: improved** — 5/5 sampled gate decisions (three admits, two rejects) agree on outside re-reading; the lane withdrew
  its own v1 predicates on evidence. Limit: M45-2 names one held file where three hold the serial (D2).

Closure: status `ok`, **admitted=true**, verdict `admitted` — both claims verify, no axis harmed.

## 6. Routed defects (lane fixes next round)

1. D1 — round size 41 seats, below the run-9 64-seat floor (prompt §6 :152-154); w2 falsification not run; the round ran one v1 wave
   (32-64 band) and called no residual. Conformance, status-neutral. Run the planned w2 (SCORECARD Round 45 planned 1) against
   `ee6659b`'s tool, entry and gate before building on them.
2. D2 — M45-2 undercounts: the host monitor serial is in three held entries, not one — `corpus/knowledge/config-health-report-r3.md:149`,
   `hyprctl-verification-layer.md:153`, `hyprland-config-plane.md:184` (`git grep -n -F <serial> 4d22eeb -- . ':!.ufo'`), plus 21
   copies under `.ufo/waves/round-32/` and `round-37/` (24 files total). None was introduced this round (`git diff 0c89478 4d22eeb | grep -c` → 0).
   Append a correction to the lesson; teach the gate a prose rule (R3 reads JSON keys only). **Operator note:** removal from pushed
   history is the operator's decision.
3. D3 — `quality/check-session-material.py` is called a gate (QUALITY 85, report "privacy gate") but has no registry row in `SKILL.md`
   (registry holds only `mado-axis-scores`, `:769`): PROTOCOL §Gate standard grades no gate conformant without one. Add the row (verdict
   map, self-test spelling, pinned-value path). It exits 1 at `ee6659b` (`findings=97`): triage the 48 pre-existing findings and mark the
   synthetic fixtures (SCORECARD planned 2).
4. D4 — untracked `.ufo/waves/round-45/w1/MutC1Counter/results.json` (4 MB) sits in the lane worktree: commit a digest line next to
   `summary.txt` and remove the file, or state its retention.
5. D5 — `w1-results.json` holds 41 `output: null` seats (kernel restart): the seat report files are the only record; say so in the
   wave README or the next lesson so a reader does not treat the results file as evidence.
6. D6 — carried open: round-44 D6 (S290-S297 supersession) deferred a second time; round-44 D7 (`w1/ConnCalibration` 6 mismatches)
   recorded, not corrected — land both by appended errata.

SHONEN boxes remain `[~]`. Box 2 (end-to-end live run) is reproducible by a non-author — I reproduced `DP-1 AGREE`, `verdict=OK`, exit 0
— and box 3 held for me: the `SKILL.md` command for this tool ran as written with no oral context. Promotion review is operator-owned.
