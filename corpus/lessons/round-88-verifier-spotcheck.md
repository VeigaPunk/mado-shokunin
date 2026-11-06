author: hyaku closure (non-author integrator, @m_zfl)

# mado round 88 — verifier spot-check (non-author)

Round report `.ufo/reports/round-88/mado.md`; lane repo `mado-shokunin`, branch `master`; round base
`24ba2a9ddac21c1211579231e6ee1d98963f9988`; freeze `9e36e3a3103349b939982e532feca443f02e660d`; C1 measured revision
`650e18bdf0ae404ec9a80874c4503ecf3237e8e6`; C2 measured revision `7d3074865a9f5acfa0f1c9c66b460e73d4031331`; records
`498855cb327cd4e3debfa9446ea38398c216dda1`; round tip (closed) `8e8f7ea354cf23178ad08c400cd8aee9668d7bb3`. I did not
author this round; every command below was run by me against committed bytes on this host, 2026-11-06. Driver digest
(closure prompt; verified against `.ufo/watchdog.log`, lines 3012 and 3031 at read time):
`2026-11-06T15:39:33-03:00 launch mado round=88 pgid=1086569 driver=hyaku-inline attempt=1` /
`2026-11-06T16:58:32-03:00 complete mado round=88; hyaku-inline attempt=1`.

## 1. Conformance (step 1)

| item | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-88/mado.md` (fleet repo) | `mado-shokunin <mado@shokunin.local> 75c13c39af254e3a7fabe033e8a7fb0a1216b8a8 2026-11-06 16:57:55 -0300` — after the lane tip (`8e8f7ea3` committed 16:56:53), before the driver `complete` (16:58:32) | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` | heading present; 4 `[~]` lines, one per canonical box, each with a pointer | pass |
| cited lane commits exist, ancestors of the branch ref | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` over `24ba2a9`, `9e36e3a3`, `650e18bd`, `7d307486`, `498855cb`, `8e8f7ea3` | all six `commit`, all ancestors of `master` | pass |
| no uncommitted round work; pushed | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 head=detached tracked=0 untracked=2`; untracked = `.ufo/waves/round-88/{w1,r1}.ready.dispatched`; remote `8e8f7ea3…` | pass (note) |
| prompt carries the template contract | `diff <(sed 's/{{[^}]*}}//g' templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/mado-round-88.md)` | only placeholder substitutions in §1–§5; §6 hyaku addendum and run-15 notes follow; prompt committed `1f52a516` (15:39:31) before the launch line (15:39:33) | pass |
| dispatch evidence | `.ufo/watchdog.log` | launch and complete lines match the digest above | pass |

**Conformance defects (status-neutral):** the two untracked `*.ready.dispatched` files are the inline-handoff
dispatch markers (orchestrator consumption markers next to the committed `w1.ready`/`r1.ready`), not lane round work,
but they sit uncommitted in the lane tree. Lane commits in `24ba2a9..8e8f7ea` also include two operator
`considerthese:` commits (`1ee8b669`, `f271f7fe`) — operator-owned, not round work.

## 2. Claims (step 2)

Gate standard: I executed no lane gate or counter. The counters' TARGET_MET verdicts are **evidence-verified** (receipt
tallies, pinned digests recomputed by me from committed bytes, revisions measured). The capability itself is
**re-measured** by a direct plain run of the lane tool (`tools/mado-mako.py`, a read-only resolver, not a gate) at the
base and at the tip on a fixture I wrote.

### C1 — coverage (capability): ten mako criteria fields + upstream boolean/urgency grammar

| re-check | command | observed |
|---|---|---|
| fields modelled before→after (re-measured) | `git show <rev>:tools/mado-mako.py \| grep -n MODELLED_FIELDS -A1` at `24ba2a9`, `650e18bd`, `8e8f7ea` | `("app-name", "urgency", "mode")` = 3 → `("app-name", "app-icon", "summary", "body", "urgency", "category", "desktop-entry", "actionable", "expiring", "mode")` = 10; of 12 first-pass fields (summary~, body~ refused). Matches report 3/12 → 10/12 |
| DND grammar (re-measured) | fixture config `invisible=false` / `[mode=do-not-disturb]` / `invisible=true` / `[app-name=Slack]` / `invisible=false`; `python3 -I <tool@rev> --config … --home … --app-name Firefox --mode do-not-disturb` | base `24ba2a9`: `refusals=3`, effective `"invisible": "0"` (true/false refused); tip `8e8f7ea`: `refusals=1`, `"invisible": "1"`. The host-DND motivation reproduces |
| tool digests = receipts (evidence) | `git show <rev>:tools/mado-mako.py \| sha256sum` | `24ba2a9` 67a955a5… (= receipt base_tool_sha256), `650e18bd` 07930521… (= c1-measured-A tool_sha256), `7d307486`/`8e8f7ea` c374d715… (= c1-harm-at-B / c2 tool_sha256) |
| frozen bytes unchanged freeze→tip (evidence) | `git show {9e36e3a,8e8f7ea}:<file> \| sha256sum` | c1 counter 3678425a…, c2 counter f8e18b7c…, mako cases a0e81b19…, containment cases 8b16c0cb… identical at freeze and tip; equal to the receipt pins |
| receipt tallies (evidence) | `jq '.cases\|length'`, `grep -c` over `receipts/c1-measured-A-r88.txt` | 62 cases, 22 mutants in frozen files; `case … ok ok` 62; `mutant … killed` 22; `control base-tool … ok` 33 of 62; final line `TARGET_MET … correct=62 … killed=22 … base_tool_correct=33 … score=10.0000`, `rc=0`; same at `7d307486` (`c1-harm-at-B-r88.txt`) |
| residual attack | `r1/R88MResidCasesC1.md`, `r1/R88MResidCritic.md` | C1 VERIFIES; critic STANDS (reproduced byte-for-byte) |

**C1 verdict: coverage `improved`.** Reported before→after (33/62 → 62/62; 3/12 → 10/12) agrees with my measurements.

### C2 — operability: include= containment under declared read roots

| re-check | command | observed |
|---|---|---|
| symlinked include escaping HOME (re-measured) | fixture `~/.config/mako/esc -> /etc`, config `include=~/.config/mako/esc/hostname`; tool at base and tip | base `24ba2a9`: `"applied": ["include:…/esc/hostname"]` (escape read — r87 R2 reproduces); tip `8e8f7ea`: `"applied": []`, `refusals=1` |
| receipt tallies (evidence) | `grep -c` over `receipts/c2-measured-B-r88.txt`, `c2-supp-base-is-A-r88.txt` | 26 cases `ok ok`, 7 `killed`, `control base-tool … ok` 11; final `TARGET_MET rev=7d307486… correct=26 mutants=7 killed=7 base_tool_correct=11 refuse_all_includes_correct=14 score=10.0000`, `rc=0`; supplementary with `base_rev=650e18bd` also 11/26 |
| residual attack | `r1/R88MResidCasesC2.md`, `r1/R88MResidCritic.md` | C2 VERIFIES; critic STANDS on the predicate, FALLS on the declaration's "Before" sentence (counter rc 2 at `650e18bd`, not TARGET_MISSED) — erratum appended in SCORECARD and the declaration at `8e8f7ea3` |

**C2 verdict: operability `improved`.** Before (11/26 via the base-tool control; counter has no verdict at `650e18bd`,
disclosed erratum) → 26/26 agrees.

### Harm check

- `git diff 24ba2a9 8e8f7ea -- SCORECARD.md`: append-only — one new `## Round 88` section (claims table, capability row,
  named limits, errata); no prior row or axis score edited.
- Files changed outside `.ufo/waves/` and counters: `LOG.md`, `SCORECARD.md`, `corpus/{QUALITY,README,SOURCES}.md`,
  `corpus/knowledge/mako-fields-containment-r88.md`, `corpus/lessons/round-88.md`, `quality/tool-ledger.md`,
  `tools/mado-mako.py` (+ operator `considerthese/`). `PROVINCE.md`, `SKILL.md` untouched.
- Harm receipt `receipts/harm-final-r88.txt` (committed at `8e8f7ea3`, after r1 critic H2 found it uncommitted): gate
  selftest `460/460`, file plane `CLEAN (29 pass, 4 notes)`, index `109/109`, ledger `163/163 uncovered=0 TARGET_MET`,
  tool selftest `checks=52 failed=0`, counter selftests `40/40`, `28/28` (evidence-verified, not executed).
- Plain counts: SOURCES rows `grep -c '^| S[0-9]'` 428 → 430; `corpus/knowledge/` entries 108 → 109.
- Tool-ledger descriptions at the tip (lines 197, 200) now carry 52 checks / 22 mutants (r1 critic H3 fixed).

No owned axis harmed.

### Per-axis verdicts (match the MANIFEST entry)

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 re-measured (fields 3 → 10; DND resolves) + receipts evidence-verified |
| operability | improved | C2 re-measured (escape include refused) + receipts evidence-verified |

Closure: status `ok`, admitted (every claim verifies, no axis harmed).

## 3. Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/mako-fields-containment-r88.md` | admit | S494: `curl -fsSL https://raw.githubusercontent.com/emersion/mako/v1.11.0/{criteria,types,config}.c` → sha256 22767742…, c2f3398d…, 94c3a4e7… (all three = row); criteria.c 85-86, 90-91 actionable/expiring compared as booleans, 110-111 `spec.summary && strcmp(criteria->summary, notif->summary)`; types.c 19-28 `parse_boolean` accepts `true`/`1` (strcasecmp) and `false`/`0`; host `pacman -Q mako` → 1.11.0-1 | agree | every rule I sampled is at the cited line of the tag-pinned upstream of the installed version, and the boolean grammar is exactly what the tool now implements (my DND re-run) |
| `summary~`/`body~` modelled with Python `re` | reject | `zcat /usr/share/man/man5/mako.5.gz \| nl -ba` lines 450, 456: "a POSIX extended regular expression match on the summary/body"; criteria.c 2 `#include <regex.h>`, 47-48 `regexec` | agree | POSIX ERE (regcomp/regexec) and Python `re` differ in syntax and semantics; refusing is the honest stance |
| containment as a mako rule | reject | mako.5 lines 45-48 "The path must be absolute or otherwise start with ~/." (no boundary); config.c 545-547 `include` → `expand_config_path` → `load_config_file` with no root check | agree | upstream bounds nothing, so containment is correctly recorded as the lane's stance, not mako's behaviour |

**SOURCES row re-opened:** S495 — `sha256sum /usr/share/man/man7/path_resolution.7.gz` → `2a21ab67…` (= row);
`zcat … \| sha256sum` → `20726811…` (= row); `zcat … \| nl -ba` line 145: `One cannot walk up past the root: "/.." is
the same as "/".` — 11 words, ≤25, present verbatim at the cited line; host `man-pages 6.19-1` (= row).

**Census:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok …/corpus/SOURCES.md`,
rc 0; 55 `W04` duplicate-URL warnings as in `receipts/census-{start,end}-r88.txt` (55 and 55).

## 4. Trend verdicts

- **expansion — improved:** one admitted knowledge entry (108 → 109) on ground the coverage map did not hold (fields
  beyond app-name/urgency/mode, upstream grammar, containment), citing two new `mined` rows S494/S495 (428 → 430) that I
  re-opened; capability row "mako effective settings over ten criteria fields" (first-working round 88).
- **quality — improved:** the r87 case set is carried pinned (22/22) inside a superseding 62-case set with 22 mutants
  all killed; QUALITY 146–147 each cite a round-88 lesson and a shown-failure; the r1 critic's false figures (H2/H3) were
  corrected by name at `8e8f7ea3`, and the falsified declaration "Before" sentence carries a named erratum. No admitted
  entry failed its re-check.
- **discernment — improved:** the outside spot-check agrees with the gate on the admit and on both rejects.

## 5. Routed defects (lane must fix next round)

- R1 (C1, mutation survivors, `r1/R88MResidMut.md` §3.1): app-name casefold (RM2C1), `!` on a string field (RM3C1),
  mode casefold (RM5C1), `include=` inside a criteria section (RM7C1) — add the missing cases.
- R2 (C2, survivors, §4.1): trailing-slash refusal dropped (RM3C2), `~//` re-join dropped (RM4C2), root-equality refused
  (RM5C2, live branch — `--read-root` may be a file).
- R3 (C2, survivor **not in the report's routing list**): RM6C2 lexical cycle detection survives (§4.1 item 4; missing
  case `probe-cycle-via-second-lexical-path`). The report routes RM2C2 (opens the unresolved target) instead, which the
  mutation seat ruled a confirmed named limit (TOCTOU), not a defect — correct the routing in round 89.
- R4 (record): the records commit `498855cb` cited `receipts/harm-final-r88.txt` before it was committed (fixed at
  `8e8f7ea3`); commit cited receipts in the same commit that cites them.
- R5 (hygiene): commit or remove `.ufo/waves/round-88/{w1,r1}.ready.dispatched` per the handoff convention so the lane
  tree is clean.
- Note for the operator (promotion is operator-owned): the four SHONEN boxes carry concrete pointers; box 1 points at a
  knowledge entry, not `SKILL.md` (unchanged this round), so it is not yet fully checkable as worded.
