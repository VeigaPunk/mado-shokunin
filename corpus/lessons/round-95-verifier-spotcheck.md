# round-95 verifier spot-check — mado

author: hyaku closure (non-author integrator, @m_zfl)

- Date: 2026-11-07. Lane repo `mado-shokunin`, branch `master`; round base
  `4a2af6817024f6ed47084a5217c1825ae247f4fe` → reported tip `5ef746b7a678185d1fd1b84283af1f18aee33816`.
- Report: `.ufo/reports/round-95/mado.md` (fleet repo). This file is my only write; I did not author, improve
  or edit any lane artifact, and I did not run any lane gate end to end (committed receipts were verified).

## 1. Step-1 conformance

| item | observed | verdict |
|---|---|---|
| report committed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-95/mado.md` → `mado-shokunin <mado@shokunin.local> d18e00be4f4d27dafff0551db097de4c0ed71297` | pass |
| report lands last | commit date (committer) `2026-11-07 08:22:45 -03` is after the cited lane tip `5ef746b7` (`2026-11-07 08:21:50 -03`); the author date `07:32:49 -03` is earlier — the report text cites the addendum, so the author date is a skewed/preserved value; ordering on committer time holds | pass (author-date skew noted) |
| SHONEN heading, one line per box | heading present; four `[~]` lines = the four boxes of `SHONEN.md`; no `[x]` | pass |
| cited commits exist and are ancestors of `master` | all six OK: `497c6fcd`, `a689d2e3`, `9afa39f5`, `6f6955f9`, `5a41b438`, `5ef746b7` (`git merge-base --is-ancestor <h> master` rc 0 each) | pass |
| lane repo clean and pushed | `git -C mado-shokunin status --porcelain` empty; `jj-lane.sh state` at check: `ahead=0 behind=0`. After the check the remote advanced one operator commit `611f73c5` (`considerthese: 2026-11-07 daily reflection`, `João Pedro Veiga`, a path outside this round); local `5ef746b7` is its ancestor, no lane work unpushed | pass (remote moved by an operator commit; no lane debt) |
| prompt carries the template contract | `.ufo/prompts/mado-round-95.md` §1–§5 is `templates/round-prompt.md` verbatim with the render substitutions (`FLEET_ROOT`, `LANE=mado`, `ROUND=95`, axes `coverage + operability (desktop and compositor craft)`), plus the hyaku addendum §6; all five child-lane items present (report path, SHONEN heading, commit-hash citation, commit-then-report §5, write scope). The quoted run-15 route map is stale against the live `task.agentModelOverrides` (live: scout `@m_mim`, connector `@m_antigravity`, executor `@m_zfl`, reviewer/critic/mutation-tester `@m_flash`); the prompt names the live table as authority and the report routes through it — operator-side addendum drift, not a lane defect | pass |
| marker vs report | real report: named commits, receipts, every required section, checkable hash citations | report, not a marker |

Dispatch/complete digest carried into the closure notes:
`04:55:31 launch mado round=95 pgid=3134634 attempt=1`; `07:22:25 lane-dead-no-report (FAIL report_of)`; `07:22:32 launch attempt=2 pgid=769407`; `07:23:22 lane-dead-no-report (FAIL report_of)`; `07:23:29 launch attempt=3 pgid=899374`; `10:50:51 complete mado round=95; hyaku-inline attempt=3`.

## 2. Claim re-checks

Legend: **re-measured** = I ran the count myself over committed bytes; **evidence-verified** = I read the
committed receipt/frozen evidence (self-test tally, frozen-run verdict, revision measured) and did not
re-execute the lane's counter.

### C1 — coverage, new surface: GLib content-type guess given file bytes (capability)

| check (command) | observed | matches report |
|---|---|---|
| `git cat-file -e 4a2af681:tools/mado-mimesniff.py` | absent at base (0/300 is "no tool", as declared) | yes |
| `git show 9afa39f5:tools/mado-mimesniff.py \| sha256sum` | `4ef019c69ea8ae4147f83d1558683f012fb4aac0815d36770304717aaca6af24` = declaration pin | yes |
| `sha256sum .ufo/waves/round-95/controls/mimesniff-cases-r95-frozen.json` | `ee815b4f…a8a2` = pin; 300 cases, 2863 inputs, 20 classes (min `name0`=9), 94 counted mutants | yes (re-measured) |
| `sha256sum` mutants / oracle / fresh generator / host list / forgery / panel | `0e45964a…bf07` / `99df35f8…124a` / `15396113…b809` / `9d5947a7…ba87` / `5cb0fbad…f75c` / `8c6dfdac…b0f5` — all equal the declaration | yes (re-measured) |
| `git ls-tree 9afa39f5 corpus/knowledge \| wc -l` vs base | `115 → 116`; `corpus/README.md:19` lists `mime-magic-sniff-r95.md`; frontier line at `:151` | yes (re-measured) |
| SOURCES rows: `grep -cE '^ {0,3}\| S[0-9]{3,} '` at base vs tip | `453 → 458`; S519–S523 present, tier A; S505 used-by now carries `…mime-magic-sniff-r95.md` | yes (re-measured) |
| `receipts/c1-measured-r95.txt` | `MADO_MIMESNIFF_COUNT: TARGET_MET … rev=9afa39f5 tool_pin=ok cases=300 correct=300 classes=20/20 fresh=120/120 host=9822/9822 mutants=94 killed=94 class_kills=20/20 real_rebuild=11/11 static_no_external_resolver=ok audit_denials=0 controls do_nothing=17 name_only=57 naive=186 base=0 memoriser_fresh=0/120 forgery=rejected`, rc 0 | yes (evidence-verified) |
| `receipts/c1-at-tip-r95.txt` (separability at C2 tip) | same verdict at `6f6955f9`, `memoriser_fresh=1/120`, rc 0 | yes (evidence-verified) |
| `receipts/c1-controls-prefreeze-r95.txt` | wave `c1` 268/300 and `c1b` 283/300 MISS, `c1c` MET, forgery rejected with `audit_denials=5764` | yes (evidence-verified) |

Before → after confirmed: **0/300 (no tool) → 300/300**, measured at `9afa39f5`; fresh 120/120, host 9822/9822,
94/94 mutants, 20/20 class kills, 11/11 real rebuilds. Verdict: **coverage improved**.

### C2 — operability: kill-sets that let the round-93 selftest-strength gate guard two more tools

| check | observed | matches report |
|---|---|---|
| base vs tip `quality/selftest-kills/mado-{mimeglob,portals}.json` | absent at base; at `6f6955f9` `fab72daf…a593` with `jq '.kills\|length'` = 22, `4c7fc2b3…c83d` = 42 | yes (re-measured) |
| gate and tools unchanged | `quality/check-selftest-strength.py` `2d6f1219…da61b` at base and tip; `tools/mado-mimeglob.py` `65f80a6c…e2453`, `tools/mado-portals.py` `e46a861e…b021` at base and tip; `git diff --name-only base..tip -- tools/ quality/check-selftest-strength.py quality/check-*.py` → only `tools/mado-mimesniff.py` (new) | yes (re-measured) |
| `receipts/c2-at-tip-r95.txt` | `MADO_SELFTEST_KILLS: TARGET_MET … gate_pin=ok kills_pin=ok,ok tools=2 checks=47 positive=OK:0,OK:0 neutralised_flagged=47/47 hand_flagged=75/75 neutral_ok=6/6 do_nothing_flagged=0 always_weak_positive=WEAK:1,WEAK:1 singleton_labels=36/47 tool_pin=ok,ok`, rc 0 | yes (evidence-verified) |
| `receipts/c2-at-c1-r95.txt` | `SETUP_ERROR … kill-sets absent` at `9afa39f5`, rc 2 | yes (evidence-verified) |
| `receipts/c2-controls-prefreeze-r95.txt` | first drafts as candidates `28/75` hand_flagged MISSED; blanket forgery `34/75` MISSED, singletons `0/47`; empty kill-sets `0/47`/`0/75` MISSED; frozen `75/75`, `47/47` | yes (evidence-verified) |
| harm watch `receipts/harm-final-r95.txt` | `MADO_SELFTEST: 460/460 assertions passed`; every named counter TARGET_MET; new kill-sets on the real gate `kills=22 held=22` and `kills=42 held=42`; `unchanged-tool diff empty` | yes (evidence-verified) |

Before → after confirmed: hand weakenings flagged **0/75 → 75/75**, single-check neutralisations **0/47 → 47/47**
(first drafts 28/75; no instrument existed before). Verdict: **operability improved**.

## 3. Per-axis verdicts

| axis | verdict | reason |
|---|---|---|
| coverage | **improved** | new surface (bytes → type, magic/alias/parent sections) enters core; entry index 115 → 116; five tier-A rows; capability row demonstrated at 300/300 |
| operability | **improved** | two more tools guarded by the unchanged gate; 0/75 → 75/75 and 0/47 → 47/47 with first-draft and forgery controls |
| depth | unchanged | no depth claim this round; the entry's rules are sourced and were spot-checked |
| freshness | unchanged | S505 re-opened and both freedesktop locators re-checked, but no freshness claim/score move was declared |
| calibration | unchanged | no calibration claim; self-assessment checks out (all SHONEN `[~]`, limits declared, own defects mined) |
| adjacency | unchanged | cross-domain evidence (GLib, freedesktop, tsukuroi hook, revenger/libmagic) cited, not absorbed; PROVINCE refined only for the lane's own surfaces |

No owned axis is harmed: no existing tool or gate bytes changed (the new tool, two counters and two kill-sets are
additions; the rest is registry/documentation bytes), every prior counter was re-run green in the harm receipt, and
both guarded tools keep their base digests.

## 4. Discernment spot-check (outside the lane)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/mime-magic-sniff-r95.md` (admit) | admit | S519 `xdgmimecache.c` (HTTPS 200, sha256 `ccda4366…db69`): `if (i + data_length > len)` / `return FALSE;` at 185-186; S520 `xdgmimeint.c` (`c2364aa8…2f29`): the `chardata[i] < 32 && != 9/10/13` test at 185-186; S521 `gcontenttype-fdo.c` (`8a5b4f47…2d7c`): `g_ascii_iscntrl && !g_ascii_isspace && c != '\b'` at 542-544; S522 `glocalfileinfo.c` (`b006a93d…4497`): `if (!fast && result_uncertain && path != NULL)` at 1340 | **agree** | every sampled rule's cited line exists and says what the entry says; the entry's central VT claim matches `g_ascii_isspace`, not C `isspace` |
| S523 (admit) | admit | `https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html` HTTP 200, sha256 `e00fa00e…c61e`; text: "Checking the first 128 bytes of the file for ASCII control characters is a good way to guess whether a file is binary or text" | **agree** | the located quote is present verbatim and is exactly 25 words; the registered digest equals the fetched page |
| the L1 `sources-open-r95.txt` smi-s02 digest `1566c459…` (reject) | reject | `.ufo/waves/round-95/fetch/smi-s02.html` = 109 B, `<a href="…ar01s02.html">Moved Permanently</a>`, sha256 `1566c459…a3c66`; live old locator now answers 301 (this re-fetch: empty body) | **agree** | the digest is a redirect stub, not the spec page (`e00fa00e…`, 59208 B); the exact 109-byte body was served at 07:57Z and is not re-served now, so the reject stands on class (301 + non-page body), not byte-exact reproduction |
| wave candidate `build/mado-mimesniff.c1.py` / `c1b` (reject, replaced by `c1c`) | reject | `receipts/c1-controls-prefreeze-r95.txt` first two blocks: `c1` `cases=300 correct=268`, `c1b` `correct=283`, both `DRAFT_TARGET_MISSED` | **agree** | the rejected candidates measurably miss the frozen set; `c1c` MET with the VT/table and recursion fixes |
| first-draft C2 kill-sets (reject, replaced by c2b) | reject | `receipts/c2-controls-prefreeze-r95.txt`: first drafts `hand_flagged=28/75`, `DRAFT_TARGET_MISSED`; blanket forgery `34/75`, singletons `0/47` | **agree** | the frozen c2b kill-sets reach 75/75 and 47/47 while the first drafts and the blanket forgery do not; the control discriminates |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` →
`mado ok`, rc 0, with the inherited W04 duplicate-url warnings (S518/S519/S521 among them) and the old W01 row S277.

## 5. Trend verdicts

- **expansion — improved:** a desktop surface the coverage map did not hold (bytes → MIME type) moves into core with
  an admitted entry (index 115 → 116, frontier line `corpus/README.md:151`), five tier-A rows S519–S523 and a
  capability row demonstrated at 300/300 — evidence above.
- **quality — improved:** C1 300/300 + 94/94 mutants + fresh 120/120 + host 9822/9822 + real_rebuild 11/11, C2 75/75 +
  47/47 where no instrument existed, and a green harm watch over every prior round's counters; no admitted entry
  failed this re-check.
- **discernment — improved:** my outside spot-check agrees on 2/2 sampled admits and 3/3 sampled rejects; the lane
  mined two of its own defects (M95-1 VT/`isspace`, M95-2 301 stub) into QUALITY 163/164, recorded M95-3 as a routed
  gate blind spot and M95-4 as a closed label-granularity fix, and re-mined the round-94 "not reproducible" reject
  reason as a flip.

## 6. Routed defects (status-neutral; the lane fixes them next round)

1. `tools/mado-mime.py` HOME edges (round-94 routed defect 1): still open; a change needs its round-94 kill-set
   `tool_sha256` re-pinned in the same round.
2. `tools/mado-mimeglob.py` docstring citation (round-94 routed defect 2): still open; the correct line is recorded in
   the round-95 lesson (`xdgmimecache.c:126-139`); fix with the next behavioural change.
3. Three tools still without kill-sets: `tools/mado-mako.py`, `tools/mado-verify.sh`,
   `quality/check-receipt-presence.py`.
4. The gate's own selftest cannot be kill-set-guarded under `non_selftest_prefix` (M95-3; cut at line 73): needs a
   predicate change and re-anchored round-93/94 counters (QUALITY 153/155).
5. QUALITY 158 instrument gap (HTTP status only for URLs outside the registry) and the portal entry §8 frozen cases
   (round-93 routed, still open); M95-2 exposes the gap.
6. The C1 tool docstring's citation check (report, "Routed to round 96").
7. Cosmetic: the round-95 lesson/declaration name the L1 `MadoR95` / "attempt 1" while the round completed under
   attempt 3 (`MadoR95a3`); the report discloses it — name the completing attempt (or the freeze author) next time.
