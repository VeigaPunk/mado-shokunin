author: hyaku closure (non-author integrator, @m_opus)

# mado round 23 — non-author verifier spot-check (hyaku closure)

Reviewer: fresh hyaku closure subagent `HyakuCloseMado23`, dispatched by the hyaku orchestrator, not by
the lane; runtime model as exposed to the reviewer: `anthropic/claude-opus-5-5` (route `task` → `@m_opus`).
I did not author or steer any part of round 23. No review seats were dispatched; every check below was
run by me. No tools were installed or updated.

Inputs: report `.ufo/reports/round-23/mado.md` (fleet commit `36edb174`), prompt
`.ufo/prompts/mado-round-23.md` (fleet commit `bcee3007`), lane base `e33ea30461f6e9bbeee40beef19770a953f7a105`,
lane tip `fa819d561d613cf3cfd8f58ed763e1ca57ab5eb4`. Driver digest (copied from `.ufo/watchdog.log`):

```
2026-10-22T07:43:10-03:00 launch mado round=23 pgid=555711 driver=hyaku-inline attempt=1
2026-10-22T09:13:47-03:00 complete mado round=23; hyaku-inline attempt=1
```

Scratch: `/fast/scratch/hyaku/mado-r23-closure/` (classifier extracts and fetched upstream bytes; not evidence by itself,
every result below carries its command).

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report authored by lane identity | `git log --format='%an %H' -- .ufo/reports/round-23/mado.md` | `mado-shokunin 36edb174ba05b75d1a6817595ac2b7dd778c01a7` (09:13:22 −03, after lane tip 09:12:44) | pass |
| SHONEN heading, one line per box | read report §SHONEN | 4 lines, all `[~]`; lane `SHONEN.md` byte-unchanged `e33ea304..fa819d56` | pass |
| Cited lane commits exist and are ancestors of `master` | `git cat-file -t` + `merge-base --is-ancestor <h> master` over every hex token in the report | 6b383c46, a28e4815, 4de44647, 2e592aff, c8cb3930, 2f1134f3, 03227ddf, 3732c7a7, 3df10626, fa819d56, e33ea304: commit + ancestor | pass |
| Non-commit hex tokens | same | `cd9da20c`, `e1dc8029` are not git objects; they are SHA256 prefixes of `tools/mado-tripwire.py` (base/tip `cd9da20c2f562efb…`, `03227ddf` `e1dc8029ced9fcc6…`, recomputed with `git show REV:tools/mado-tripwire.py \| sha256sum`) | note (see routed defect 4) |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain \| wc -l` | `state branch=master local=fa819d56… remote=fa819d56… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain `0` | pass |
| Range authorship | `git log --format='%an' e33ea304..fa819d56` | 10 commits, all `mado-shokunin` | pass |
| Prompt carries template contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/mado-round-23.md)` | only `{{…}}` placeholder substitutions differ; §1–§5 headings identical; §6 hyaku addendum appended | pass |
| Registration before any tool change | `git log --reverse --format='%h %ci %s' e33ea304..fa819d56` + per-commit `--name-status` | `6b383c4` (07:51:02) registration + frozen repair set; `a28e481`, `4de4464` touch only `.ufo/waves/round-23/`; first `tools/` change is `2e592af` (08:49:38) | pass |

Status: real report with checkable commits → `ok`.

## 2. Claims (re-measured over committed bytes)

Classifier bytes for each revision were extracted with `git show REV:tools/mado-tripwire.py > tool-REV.py`.

| Claim | Command (lane root) | Before `e33ea304` | After `fa819d56` | Reported | Verdict |
|---|---|---|---|---|---|
| C1 operability, frozen 12-case repair set, target 12/12 | `python3 -I .ufo/waves/round-23/repair/measure.py --tool tool-REV.py` | **6/12** rc=1, tool `cd9da20c` | **6/12** rc=1, tool `cd9da20c` | 6/12, target not met | **not met** (honest stop) |
| C2 coverage, foot/kitty/ghostty sourced routes, target 3/3 | `python3 -I .ufo/waves/round-23/c2/count.py REV` | **0/3** (note absent) rc=1 | **3/3** rc=0 (foot 8, kitty 9, ghostty 8 citing rows) | 0/3 → 3/3 | **verified** |
| C3 calibration, SHONEN box 4 vs tracked tools without a PROVINCE row, target 0 | `python3 -I .ufo/waves/round-23/c3/count.py REV` | **5** rc=1 | **0** rc=0 (5/5 tools accounted by table rows) | 5 → 0 | **verified** |

C1 detail. Failing at base and tip, identical set: ReturnedGlobalCallableShadow,
ForwardExistingClosureWithoutFrameContamination, ForwarderInvokesCallback, CallerLocalShadowsHelperGlobal,
ForwarderPassesCallerArgument, ForwarderInvokesFactoryClosure. The withdrawn candidates did reach the target:
`2e592aff` (tool `41489991`) 12/12 rc=0 and `03227ddf` (tool `e1dc8029`) 12/12 rc=0. The tip restores base bytes
(`git diff --quiet e33ea304 fa819d56 -- tools/` → identical). The withdrawal reasons are evidence-verified, not
re-executed: `w2/reports/AttackLateCell.md:75-87` (1 regression `SecondFrameRelayInvokesFirstClosure` at the repaired
tip) and `w2/reports/ReClosureNeighbour.md:10-21` (7 worse stored-callable shapes); candidate kept at
`evidence/candidate-classifier-e1dc8029.py` (sha256 `e1dc8029ced9fcc6…`, matches).

Plain cross-checks. C2: SOURCES rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` 122 → 152;
new-row status histogram `mined=29 queued=1`; malformed rows 0. C3: the registration's v1 shell form gives 4 → 0;
`git show fa819d56:PROVINCE.md | grep -nE '^\| \`tools/'` lists five rows (lines 24–28).

Target integrity. Registered targets (`registration.md:28-56`, landed `6b383c46`): C1 12/12, C2 3/3, C3 0. The two
counter changes (`4de44647`, 08:11:58) tightened C2/C3 before any after-measurement and raised C3's base 4 → 5; the
targets were not changed. The report and SCORECARD (`3df10626` append-only disposition) state C1 as 6/12 with the
12/12 target kept. No target was narrowed.

Precision guard H2: registration clarification 3 rewords the guard from "same passing set" to "no base-passing case
fails, count ≥166/175". This is a guard, not a target, and is moot at the tip because the classifier equals base.
H2 (172 → 166/175, round 21) is not repaired; L0 line filed at fleet `.ufo/l0-questions.md:103` (commit `4fe983a`).

## 3. No-harm check (base → tip)

`git diff --numstat e33ea304 fa819d56 -- . ':!.ufo'` shows only additions: LOG.md +46, PROVINCE.md +12, SCORECARD.md +48,
SKILL.md +8, corpus/README.md +13, corpus/SOURCES.md +30, `corpus/knowledge/terminal-trees-r23.md` +117 (new),
`corpus/lessons/round-23.md` +229 (new). Removed lines in PROVINCE, SOURCES, LOG, SKILL, README, SCORECARD, QUALITY: 0
each. `tools/` is byte-identical, so every operability guard that held at base still holds: restoring the base bytes harms
no axis relative to base. SCORECARD diff: one appended round-23 section; its first C1 row (12/12 at `3732c7a7`) is
superseded by an appended "final C1 disposition … 6/12 — target 12/12 not met" paragraph (no rewrite); no axis score was changed.

PROVINCE spot reads: `tools/mado-verify.sh` row's scratch paths match the script (`mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX`
at :418, `mktemp -d /tmp/mado-verify-regression.XXXXXX` at :2251). Host fact in the note: `command -v foot kitty ghostty`
rc=1 and no `/usr/bin/{foot,kitty,ghostty}`, while `~/.config/{foot,kitty,ghostty}` exist (read-only `ls -d`): matches
"declared bytes, no consumer".

| Axis | Verdict | Reason |
|---|---|---|
| operability | unchanged | C1 6/12 → 6/12; `tools/` identical to base; target missed, nothing harmed |
| coverage | improved | C2 0/3 → 3/3 re-measured; sampled sources agree (§4) |
| calibration | improved | C3 5 → 0 re-measured; PROVINCE rows spot-read accurate |
| depth | unchanged | not claimed; an added SKILL.md terminal table (`SKILL.md:121-127`) is noted, not graded as a move |
| freshness | unchanged | not claimed |
| adjacency | unchanged | not claimed; PROVINCE rows name mori, tsukuroi, kagi, tameshi owners without absorbing scope |

## 4. Discernment spot-check (sources re-opened by ordinary fetch, 2026-10-22)

Tag pins re-checked with `git ls-remote`: kitty `v0.49.2^{}` = `b2cb871254fbdac19a085188813c8dfb258b95cd`; foot `1.28.0^{}` =
`ab33c9a19d626f8d0ac0bd1adfdba21946ada948`; ghostty `v1.3.1` tag object `22efb0be…`, peeled `332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28`.
All match the rows.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S128 kitty SIGUSR1 reload (note route row) | admit (mined) | `raw.githubusercontent.com/kovidgoyal/kitty/b2cb871…/kitty/child-monitor.c` | agree | sha256 `a4fbe5472c50249c…`, 100305 B = row; line 1708 reads `case SIGUSR1: ss->reload_config = true; break;` verbatim |
| S146 foot ignores SIGHUP (no reload by hangup) | admit (mined) | `codeberg.org/dnkl/foot/raw/tag/1.28.0/main.c` | agree | sha256 `d50034046894cde4…`, 23528 B = row; :675-676 register only SIGUSR1/SIGUSR2, :681-687 set SIGHUP and SIGPIPE to `SIG_IGN` |
| S136 ghostty `config.ghostty` vs legacy `config` | admit (mined) | `raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/config/file_load.zig` | agree | sha256 prefix `96e8165c5a365808` = row; :12 `subdir = "ghostty/config.ghostty"`, :18 comment "Ghostty <1.3.0 default path", :21 `subdir = "ghostty/config"` |
| `kitty/conf/generate.py` dropped (no dash/underscore equivalence claim) | reject (not registered) | `raw.githubusercontent.com/kovidgoyal/kitty/b2cb871…/kitty/conf/generate.py` | agree | :617 `return x.replace('-', '_')` sits in `cval` inside `gen_go_code` (:567), which emits Go `Config` structs; it is not config-key parsing, so it cannot support the claim |
| S132 kitty built HTML (moving build) | queued, supports no claim | `https://sw.kovidgoyal.net/kitty/conf.html` | agree | HTTP 200, 325 B, body is `location.replace('./conf/' + window.location.hash)`: a redirect to an unpinned build, rightly kept out of claim support |

New SOURCES row quote check — **S149** (foot wiki FAQ): cloned `https://codeberg.org/dnkl/foot.wiki.git`, `git show
2475351ace3c8a618a3f2b8a7a486e987d125e07:Home.md` → sha256 `78bd64dc27cff31a…`, 32739 B = row. Lesson quote "There is no way to
dynamically reload the configuration." (10 words, ≤25) is present verbatim in §FAQ :1011-1015, wrapped across :1013-1014.
**Agree**; anchor nit in routed defect 5.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → 7 W04 lines
(S030, S042, S045, S097, S119, S120, S121, all pre-round-23), `mado ok …/corpus/SOURCES.md`, rc=0. Byte-identical to the report's
pasted end census and to the lesson's (routed round-22 defect on census paste: fixed).

Spot-check result: 5/5 agree (3 admits, 1 reject, 1 queued) plus 1/1 new-row quote agree; the C1 withdrawal decision also agrees
with the wave-2 evidence.

## 5. Trend verdicts

- **expansion: improved.** One new knowledge entry `corpus/knowledge/terminal-trees-r23.md` on ground the coverage map marked
  unsourced (base `corpus/README.md:124` "…ghostty trees remain unsourced"), with provenance trio and `source:` citing 29 `mined`
  rows S123–S152 (S132 queued); C2 counter 0/3 → 3/3; sampled admits re-verify.
- **quality: unchanged.** No older entry superseded or re-verified; production classifier equals base; in-round errata to the
  new note are appended (`terminal-trees-r23.md:97`). Two stale sentences were left by the C1 withdrawal and a scribe draft
  (routed defects 1–2); they are in the README and lesson, not admitted knowledge entries, so this is not graded harmed.
- **discernment: improved.** The outside spot-check agrees with the gate on admits and the reject; the lane's own wave-2
  base-versus-tip attacks caught guard-blind regressions and the lane withdrew the candidate instead of landing a trade.

## 6. Closure verdict

C2 and C3 verify; C1 (the repair-first claim) misses its registered 12/12 target at the landed tip (6/12) and no axis is harmed.
Not every claim verifies → **not admitted, `rejected-honest-stop`**. Under the session ruling a rejected recovery round re-blocks the
lane through the driver (Main owns that step).

SHONEN: all four boxes `[~]`; box 2 (end-to-end task) and box 3 are unchanged this round, so the boxes are not yet fully checkable
by a non-author. No promotion signal.

## 7. Routed defects (lane fixes next round)

1. `corpus/lessons/round-23.md:197-199` still says "The note file does not yet exist … until the integrator creates the note"
   (copied scribe draft); the note exists at the tip. Append a correction (Evidence standard, "Corrections sweep every mention").
2. `corpus/README.md` round-23 bullet ("The round-23 tripwire repair … is instrument work") does not say the repair was withdrawn
   to base bytes. Append the withdrawal pointer.
3. M23-4, M23-5 and M23-7 carry `captured-by` none / no registered guard, but `corpus/QUALITY.md` is unchanged (`git diff
   e33ea304 fa819d56 -- corpus/QUALITY.md` empty). LEARNING §Understanding: add criteria citing lesson 23 (base-versus-tip
   discovery attacks before a classifier lands; absolute result paths with the measured tool sha printed).
4. Report and registration print SHA256 prefixes (`cd9da20c`, `e1dc8029`) in the same form as commit hashes; they resolve to no
   git object. Label them `sha256:` in future reports.
5. Lesson/S149 anchor quotes the foot wiki sentence at `:1014`; it spans `:1013-1014`.
6. C1 carries forward: repair set 6/12 at the tip, H3–H5 open; freeze the wave-2 regression fixtures (AttackLateCell,
   ReClosureNeighbour, AttackRecallRegress, AttackFrameScopes, AttackEscapeGate) as a registered population before any tripwire
   change (lane's own SCORECARD plan).
7. H2 precision 166/175 (round 21) stays unrepaired; L0 question open at fleet `.ufo/l0-questions.md:103`.
