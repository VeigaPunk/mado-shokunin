author: hyaku closure (non-author integrator, @m_zfl)

# mado round 90 — verifier spot-check (non-author)

Round report `.ufo/reports/round-90/mado.md`; lane repo `mado-shokunin`, branch `master`; round base
`5041acf99e27263872bf0441ad5f9d4316152605`; freeze `1d9bc40414a5d6bddd449cc633a12f2e7e338652`; C1 measured revision
`7bec239929cdd1d7c796a89ddccefe47d802673a`; C2 measured revision `c09d3465299c53a8158a96b2214c2bcda44bcb41`; D3
`7c28090e99ca99b799e16a92797bf33f63aca372`; records `6156d399895ed74faa431ebc688d55d3b47efaa0`; round tip (closed)
`1f07e84133921a8be0a2de074dc8f04e7e015cdf`. I did not author this round; every command below was run by me against committed
bytes (or the re-opened source) on this host, 2026-11-06. Driver digest (closure prompt; verified against
`.ufo/watchdog.log` lines 3055, 3078, 3079, 3094 at read time):
`2026-11-06T18:30:34-03:00 launch mado round=90 pgid=3266809 driver=hyaku-inline attempt=1` /
`2026-11-06T20:22:51-03:00 lane-dead-no-report mado round=90; retry same round` /
`2026-11-06T20:22:53-03:00 launch mado round=90 pgid=1592428 driver=hyaku-inline attempt=2` /
`2026-11-06T20:47:59-03:00 complete mado round=90; hyaku-inline attempt=2`.

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-90/mado.md` (fleet repo) | `mado-shokunin <mado@shokunin.local> 115ccdf4fc20de3a2bc6a0f48b691c3e97b7f617 2026-11-06T20:47:24-03:00` (before the 20:47:59 completion line) | pass |
| `## SHONEN` heading, one line per box | read of the report, lines 114-119 | heading present; 4 lines, all `[~]`, each with a pointer | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -t <h> && git merge-base --is-ancestor <h> master` for `1d9bc404`, `7bec2399`, `c09d3465`, `7c28090e`, `6156d399`, `1f07e841`, base `5041acf9` | all `commit`, all ancestors | pass |
| lane pushed, nothing left over | `scripts/hyaku/jj-lane.sh state mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=1f07e84133921a8be0a2de074dc8f04e7e015cdf ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote prints `1f07e841…` | pass |
| round commits all lane-authored | `git log --format='%h %an <%ae> %s' 5041acf9..1f07e841` | 6 commits, all `mado-shokunin <mado@shokunin.local>`, subjects `round-90: …` | pass |
| prompt carries the template contract | `diff <(head -140 .ufo/prompts/mado-round-90.md) kimi-shokunin/templates/round-prompt.md` | only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions differ; §6 hyaku addendum follows at line 141 | pass |
| SCORECARD append-only | `git diff --numstat 5041acf9 1f07e841 \| awk '$2>0'` | empty (no deleted line in any file); SCORECARD gains only the `## Round 90` section | pass |

Attempt 1 (`MadoR90`) died without a report; attempt 2 (`MadoR90a2`) inherited the declaration after re-checking pins and
filed. Not a marker report: six commits of checkable work.

## Per-claim re-check

### C1 — coverage (capability): xdg-desktop-portal 1.22.1 backend routing, 21 interfaces

Re-measured (plain commands, mine):

- Before: `git -C mado-shokunin cat-file -e 5041acf9:tools/mado-portals.py` → exit 128 (absent; 0 interfaces resolvable).
- After: `git show 1f07e841:tools/mado-portals.py | sha256sum` → `d1bd9b9a7c98f9e573bf8ba0594d796853f81539eed1d87052aa7906195e6ab1`, equal to the
  frozen candidate pin in `claims-declaration-r90.md:43` and to the bytes at `7bec2399`. `IFACES` (tool lines 69-73) lists 21 names.
- Host re-run (mine, read-only, from a temp copy of the committed bytes): `python3 -I mado-portals.py` → 21 `MADO_PORTAL:`
  lines, `gtk` 11, `hyprland` 4, `none` 6 (`Background`, `Wallpaper`, `Secret`, `RemoteDesktop`, `Clipboard`, `Usb`) —
  identical to `receipts/host-run-r90.txt`; `pacman -Q xdg-desktop-portal` → `1.22.1-2`.
- Frozen inputs: `sha256sum` of `controls/portal-cases-r90.json` = `66d4ffff…192da2`, `portal-mutants-r90.json` = `e761a4e4…2c2451`
  (= the counter's `--expect-*` pins); `jq '.cases|length'` → 229; `jq '.mutants|length'` → 60. Counter
  `quality/counters/c1-r90-portal-routing.py` sha256 `a92f4c3d…51a2` = declaration pin; `git log 5041acf9..1f07e841 --
  quality/counters/ .ufo/waves/round-90/controls/` → only the freeze `1d9bc404` (nothing edited after the freeze).

Evidence-verified (lane-owned gate, not executed by me — §Gate standard, Closure consequence):
`receipts/c1-measured-r90.txt` → `MADO_PORTAL_ROUTING: TARGET_MET rev=7bec2399… cases=229 correct=229 blind=66/66 fresh=120/120
mutants=60 killed=60 r12_rule_correct=70 host_table_correct=10 do_nothing_correct=35 base_tool=absent base_correct=0`, rc 0;
separability `receipts/c1-harm-at-c2-r90.txt` TARGET_MET at `c09d3465`. Registry row `mado-r90-portal-routing` at `SKILL.md:867`.

**Verdict: coverage `improved`.** Reported before→after (0 → 21 interfaces, 0 → 229/229) matches.

### C2 — operability: receipt-presence gate over records changes

Re-measured:

- Before: `git cat-file -e 5041acf9:quality/check-receipt-presence.py` → exit 128 (absent).
- After: `git show 1f07e841:quality/check-receipt-presence.py | sha256sum` → `04b8be60415f2e505f6a1414099402203eb3a1fd17b21542c3afdd24b38a1d6c` (= frozen pin).
- Frozen inputs: `receipt-presence-set-r90.json` sha256 `f7ab86c2…7939`, `receipt-mutants-r90.json` `68b39a80…be82d` (= pins);
  `jq` → 6 revisions, 35 fixtures, mutants 28. The counter enumerates `(revisions + fixtures) × ENVS{clean, mnemonic}` + 1
  `POPULATION` row (`c2-r90-receipt-presence.py:39-44,101-121`) = (6+35)×2+1 = **83**, matching `expectations=83`.
  `git rev-list --no-merges 5f174ca4..5041acf9 | wc -l` → 38 = `population=38`.
- The defects it must flag are real: `git ls-tree -r --name-only 498855cb | grep -c harm-final-r88.txt` → 0 while
  `git show 498855cb | grep -c receipts/harm-final-r88.txt` → 1; at `51bf076f` `census-end-r89.txt` and `harm-final-r89.txt`
  each 0 in the tree, 1 in the diff.
- Report-wide: all 13 `receipts/*.txt` names cited in `.ufo/reports/round-90/mado.md` are present in `1f07e841`'s tree.

Evidence-verified: `receipts/c2-measured-r90.txt` → `MADO_RECEIPT_PRESENCE: TARGET_MET rev=c09d3465… expectations=83 met=83
defects_detected=4/4 population=38 mutants=28 killed=28 base_met=0 do_nothing_met=44 smart_always_ok_met=46 always_missing_met=0`,
rc 0; `receipts/c2-at-c1-r90.txt` `SETUP_ERROR … absent` rc 2 (separable); `receipts/harm-final-r90.txt` `RECEIPT_PRESENCE: … rev=6156d399
records=6 cited=31 present=31 missing=0 verdict=OK`.

**Verdict: operability `improved`.**

### Routed work (not claims)

- D3: `git diff 5041acf9 7c28090e -- tools/mado-mako.py` → three `check(…)` additions inside `selftest()` only (59 → 62); no
  resolution code touched. `receipts/d3-mako-survivors-r90.txt`: each of RS01/RS05/RS12 `rc=0 checks=59 failed=0` on base,
  `rc=1 checks=62 failed=1` on the candidate. Agree.
- D2: `SKILL.md:861-870` holds ten rows `mado-r87-mako-criteria` … `mado-receipt-presence`. Agree.

### Harm

`git diff 5041acf9 1f07e841 -- SCORECARD.md` appends only the round-90 section; no axis score lowered. Harm watch evidence-verified
from `receipts/harm-final-r90.txt` at `6156d399`: `MADO_SELFTEST: 460/460`, `--no-live` CLEAN 29, index 111/111, ledger 169/169
uncovered 0, mako selftest 62/62, portals selftest 22/22, round-89 C1 TARGET_MET 141/141 and C2 TARGET_MET, all rc 0. No axis harmed.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 re-measured (absence at base, frozen bytes, 21 interfaces, host re-run 11/4/6) + evidence-verified counter TARGET_MET 229/229 |
| operability | improved | C2 re-measured (absence at base, frozen bytes, 83 = (6+35)×2+1, real D88/D89 misses) + evidence-verified counter TARGET_MET 83/83 |

## Discernment spot-check (`corpus/lessons/round-90.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/xdg-portal-routing-resolver-r90.md` | admit | S501: `curl -sSL https://codeload.github.com/flatpak/xdg-desktop-portal/tar.gz/refs/tags/1.22.1 \| sha256sum` → `5afeda95…3625`; `src/xdp-portal-config.c` sha256 `2da4fd83…4fe1`; `grep -n 'As a last resort'` → line 827 | agree | tarball and file pins reproduce; the gtk last-resort rule the entry relies on sits at 827-829 as cited; the entry opens with `source:`/`verified-at:`/`recheck:` and its host answers reproduce on my own run |
| `portals.conf(5)` "lexicographical order" as the `*` rule | reject | S501 `xdp-portal-config.c:267-296` (`sort_impl_by_use_in_and_name`; desktop loop 278-293, name fallback 295), `:389-390` (sort applied), `:690-711` (`*` → `find_any_impl_config` walks the sorted array); S503 `man -l /usr/share/man/man5/portals.conf.5.gz` rendered 95-96 | agree | the comparator returns `use_b - use_a` at the first desktop where the two backends' UseIn differ, and only falls to `g_strcmp0(source)` otherwise, so `*` is not plain lexicographic; the man page says lexicographic. Nuance: the lesson says "UseIn hits for the first desktop"; the loop actually continues past desktops where neither matches — same decision, wording slightly narrow |
| round-12 hand table as C1 baseline | reject (kept as control) | `receipts/c1-measured-r90.txt` `r12_rule_correct=70` of 229 | agree | a rule scoring 70/229 against the binary's own decisions cannot be the baseline rule |

New `corpus/SOURCES.md` rows re-opened (rows 453-455 at `1f07e841`):

- S502: `curl -sSL https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c | sha256sum` → `e1d1270f…f656` (= pin);
  `sed -n 1766-1770p` shows `if (key_file->start_group == key_file->current_group` / `&& strcmp (key, "Encoding") == 0)` at
  1768-1769 — the lesson's ≤25-word quote is located verbatim. Agree.
- S503: `sha256sum /usr/share/man/man5/portals.conf.5.gz` → `01eba9b4…ad51` (= pin); rendered lines 92-96 carry
  "none — Do not provide a portal implementation for this interface." and "* — Use the first portal implementation found, in
  lexicographical order." (each ≤25 words). Agree.

Census (mine): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, rc 0; 55 W04 plus
the pre-existing `W01 S277` line, identical to `receipts/census-end-r90.txt`. Rows 435 → 438 (`grep -cE '^ {0,3}\| S[0-9]{3,} '`
at base and tip).

## Trend verdicts

- **expansion — improved:** `git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` 110 → 111; SOURCES 435 → 438 (three
  tier-A rows, all re-opened above); capability row 0 → 21 interfaces.
- **quality — improved:** both claims TARGET_MET on frozen, pinned inputs with mutant kills (60/60, 28/28); D3 kills three named
  survivors with selftest-only changes; harm watch green.
- **discernment — improved:** 3/3 sampled gate decisions (1 admit, 2 reject) agree on re-open; the new gate mechanically flags
  the round-88/89 records commits whose cited receipts I confirmed absent from their trees.

## Routed defects (lane fixes next round)

1. **Gate self-test missing.** `SKILL.md:870` registers `mado-receipt-presence` as a `gate` with "no `--selftest` flag"; rows
   867-868 register the r90 counters with "no counter selftest" / "no selftest". PROTOCOL §Gate standard, Self-test, requires a
   self-invocation mode over isolated fixtures asserting exit code and a stable finding-id. Add `--selftest` to
   `quality/check-receipt-presence.py` (fixtures for OK, MISSING with a finding line, and rc 2) and record it in the row.
   Status-neutral (Closure consequence).
2. **Seat outputs not retained.** `w1-results.json` holds no seat outputs and the two scout seats left no report (lesson M90-4);
   S501-S503 rest on the L1's re-open (confirmed independently above). Keep the routed M90-4 fix: seats write their report file
   before yielding.
3. **Lesson wording (minor).** `round-90.md` `## Gate` reject reason: "ranks UseIn hits for the first desktop" — state that
   the comparator walks desktops until one where the backends' UseIn differ (`xdp-portal-config.c:278-293`). Append-only note,
   no rewrite.

Observation, no defect: the host `MADO_PORTALS:` header lists `/usr/share/xdg-desktop-portal/hyprland-portals.conf` twice because
`XDG_DATA_DIRS=/usr/local/share:/usr/share` and `datadir=/usr/share` are both searched (`tools/mado-portals.py:391-393`, modelled on
S501's six search roots); whether 1.22.1 dedupes these roots was not checked here [INFERENCE: harmless — the same file yields
the same selection].

SHONEN: all four boxes `[~]`; none is fully checkable by a non-author from this round alone (they ask for an outside-lane
executability test and PROVINCE approval). Nothing promoted.
