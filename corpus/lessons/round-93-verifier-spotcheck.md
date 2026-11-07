author: hyaku closure (non-author integrator, @m_zfl)

# mado round 93 — verifier spot-check (non-author)

Lane-round: mado round 93 (hyaku run 15, attempt 1). Base `4c6f723f3dca3a26f9d14475d695fe797e2e972c`, after
`28a97421a73d3205851634b0821c8f60ebc414df`. Report `.ufo/reports/round-93/mado.md` (fleet repo). This reviewer did not
author the round and changed none of its files; this file is the only lane path it writes. No reviewer seats dispatched.
Independent probes ran from scratch under `/dev/shm` (removed after closure); every command and its observed output is
quoted here, so the re-check is reproducible from this file.

Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 3137 and 3152 at closure):

    2026-11-07T00:01:27-03:00 launch mado round=93 pgid=2729949 driver=hyaku-inline attempt=1
    2026-11-07T02:52:22-03:00 complete mado round=93; hyaku-inline attempt=1

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-93/mado.md` (fleet) | `mado-shokunin mado@shokunin.local 68f249b3a93a99e963c8e16a41309fcec9896715 2026-11-07 02:51:46 -0300` | pass |
| report filed after its last cited commit | `git log --format='%h %an <%ae> %cI' 4c6f723f..28a97421` | last lane commit `28a97421` 02:50:34; report 02:51:46 | pass |
| `SHONEN` heading, one line per box | read of the report (lines 141–146) | `## SHONEN`, 4 lines, all `[~]` | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for 4c6f723f, 65dac61b, 0a85e687, 4fd3b292, 28a97421 | all `commit`, all ancestors | pass |
| lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `state branch=master local=28a97421… remote=28a97421… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `28a97421…` | pass |
| round commits by the lane identity | same `git log` | 4 commits (65dac61b freeze, 0a85e687 C1, 4fd3b292 C2, 28a97421 records), all `mado-shokunin <mado@shokunin.local>` | pass |
| prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/mado-round-93.md) kimi-shokunin/templates/round-prompt.md` | 22 changed lines, all placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §§1–5 present; hyaku addendum §6 at line 141 | pass |
| append-only lane records | `git diff --numstat 4c6f723f 28a97421 \| awk '$2>0'` | only `SKILL.md 4/1` (mado-portals row update), `quality/tool-ledger.md 4/1`, `tools/mado-portals.py 74/19` (the C1 code change); LOG/SCORECARD/QUALITY/SOURCES/PROVINCE/README/knowledge pure additions | pass |
| report minimum content: cross-domain item (round-92 routed defect 1) | `grep -c '^- \*\*Cross-domain evidence' .ufo/reports/round-93/mado.md` | 1 (GLib, Python runtime, test-mutation method; sibling `PROVINCE.md` sweep `none` ×20) | pass |

Conformance notes (status-neutral): the dispatch-evidence commit `032f6672` (00:01:24, three seconds before launch) is
under the lane identity — driver attribution, as in prior rounds. The harm receipt's first mako line is a harness defect
(scratch dir not created, `rc=2` = setup error), corrected append-only in the same receipt at 05:42:09Z (= 02:42:09-03,
before the records commit) with `MADO_MAKO_SELFTEST: checks=62 failed=0`; `tools/mado-mako.py` is unchanged in the round.

## Per-claim re-check

### C1 — coverage (edge class): GKeyFile byte classes in xdg-desktop-portal's `portals.conf`/`.portal`

Re-measured (plain measurements, mine):

- Code moved and landed bytes = frozen candidate: `git show <x> | sha256sum` → `4c6f723f:tools/mado-portals.py`
  `d1bd9b9a…6ab1` (base) → `0a85e687:tools/mado-portals.py`, `28a97421:tools/mado-portals.py` and
  `65dac61b:.ufo/waves/round-93/build/mado-portals.c1.py` all
  `e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021` = declared pin; 30188 bytes.
- Frozen inputs unchanged after the freeze: `git diff --stat 65dac61b 28a97421 -- .ufo/waves/round-93/controls
  .ufo/waves/round-93/build quality/counters` → only `controls/harm-r93.sh` added (29 lines, a new harness, no frozen
  file touched). sha256 at `28a97421`: cases `351072d1…d7d0c1`, mutants `7e45edc9…6d26`, oracle `d50d88bf…76f6`, byte
  generator `94fdfe8f…1597` — all = declaration pins. Oracle binary `sha256sum /usr/lib/xdg-desktop-portal` →
  `e1429fbe…a4f8` = `--expect-oracle-binary-sha256`; `pacman -Q` → `xdg-desktop-portal 1.22.1-2`, `glib2 2.90.1-1`.
- Case composition (python over the case file, read with `surrogateescape`): 366 cases = 229 unclassed + `a` 38, `b` 16,
  `n` 26 (byte subset 80), `ws` 42, `c` 7, `d` 8 — equal to the declaration. The 229 unclassed cases are the round-90
  set: same ids, files and oracle labels as `28a97421:.ufo/waves/round-90/controls/portal-cases-r90.json` (229/229
  identical). Mutants 75 (`equivalent_not_counted` 9, `not_counted_survivors` 2 not frozen).
- Independent probe (my harness: the installed `/usr/lib/xdg-desktop-portal -v -r` in a private `dbus-run-session`, dir
  mode `XDG_DESKTOP_PORTAL_DIR`, `gtk.portal` + `kde.portal` with FileChooser/Settings/Screenshot, `XDG_CURRENT_DESKTOP=X`;
  vs `--portal-dir … --json` of the base and landed tool bytes), 18 hand fixtures not taken from the frozen set:

  | fixture (`portals.conf`) | installed binary | base tool | landed tool |
  |---|---|---|---|
  | `# caf\xe9` comment, `default=kde` | kde | gtk ✗ | kde ✓ |
  | `default=kde`, unread `zzz=\xff\xfe` | gtk (eager per-key read voids) | ✓ | ✓ |
  | `default=kde`, `FileChooser=gt\xffk` | gtk | ✓ | ✓ |
  | `[gr\xe9]` other group, then `default=kde` | kde | gtk ✗ | kde ✓ |
  | `default=kde\v` | gtk | ✓ | ✓ |
  | `default=\vkde` | gtk | kde ✗ | gtk ✓ |
  | `default=kde\0gtk` | kde | gtk ✗ | kde ✓ |
  | `[preferred\0junk]`, `default=kde` | gtk | ✓ | ✓ |
  | plain `default=kde` (control) | kde | ✓ | ✓ |
  | `\v[preferred]` + `default=kde` + `FileChooser=kde` | all gtk (void) | all kde ✗ | ✓ |
  | `\vdefault=kde` + `FileChooser=kde` | FC kde, rest gtk (mangle) | all kde ✗ | ✓ |
  | `default\v=kde` + `FileChooser=kde` | FC kde, rest gtk | all kde ✗ | ✓ |
  | `default=\vkde` + `FileChooser=kde` | FC kde, rest gtk | all kde ✗ | ✓ |
  | `default=kde\v` + `FileChooser=kde` | FC kde, rest gtk | ✓ | ✓ |
  | `default=\tkde` | kde | ✓ | ✓ |
  | `default=kde\t` + `FileChooser=kde` | FC kde, rest gtk | — | ✓ |
  | `default=kde\f` + `FileChooser=kde` | FC kde, rest gtk | — | ✓ |
  | `\v# c` + `default=kde` + `FileChooser=kde` | all gtk (void) | — | ✓ |

  Landed **18/18**; base 7/15 on the rows it ran. Every divergent base row is a byte class of the claim (a, b, n). The
  last three rows are the entry's §8 "no frozen case" predictions (trailing TAB/FF mangle, VT before a comment voids) —
  they hold on the binary and the tool already answers them.

Evidence-verified (lane-owned counter, not executed — §Gate standard, Closure consequence):
`receipts/c1-measured-r93.txt:443` → `MADO_PORTAL_BYTES: TARGET_MET pred=PRED-C1-r93-v1 rev=0a85e687… tool_pin=ok cases=366
correct=366 answered=366/366 bytes_cases=80 bytes_correct=80 fresh=120/120 fresh_bytes=60/60 fresh_seed=3832186398
mutants=75 killed=75 crashed_not_killed=0 r12_rule_correct=74 host_table_correct=10 do_nothing_correct=35 base_correct=318
base_bytes_correct=32`, `rc=0`; separability `receipts/c1-at-c2-r93.txt` the same line at `4fd3b292`, rc 0;
`receipts/c1-controls-prefreeze-r93.txt` base tool `DRAFT_TARGET_MISSED … tool_pin=FAIL correct=318 bytes_correct=32
fresh_bytes=50/60`, label-table forgery `DRAFT_TARGET_MISSED … tool_pin=FAIL correct=366 … fresh_bytes=50/60`. Revision
measured is the cited C1 commit. Registry row `mado-r93-portal-bytes` (gate) at `SKILL.md:878`; `mado-portals` row
updated (line 869).

Verdict: **verified** — coverage `improved` (byte subset 32/80 → 80/80, re-measured composition and an independent 18/18).

### C2 — operability: `quality/check-selftest-strength.py` fails when a passing selftest assertion is weakened

Re-measured:

- Instrument absent at base: `git show 4c6f723f:quality/check-selftest-strength.py` → not present; no `selftest-kills/`
  at base; `git show 4c6f723f:SKILL.md | grep -c mado-selftest-strength` → 0. Present at `4fd3b292`/`28a97421`.
- Landed bytes = frozen candidates: gate `2d6f1219…a61b` and kill-set `00befb3e…16f9` at `4fd3b292` and `28a97421` =
  `65dac61b:build/check-selftest-strength.c2.py` / `build/check-seat-reports-kills.c2.json` = declared pins. Panel
  `a6d2cbe2…4c10`, gate mutants `be676929…770e`, round-92 counter `0aa4d1f1…945c` — all = pins.
- Kill-set coverage (my python): `case(` labels in `4fd3b292:quality/check-seat-reports.py` → 23 (23 unique); union of
  `must_fail` over the 32 kills → 23, ⊆ the labels, none missing; kill-set `tool_sha256` `176fc066…` = sha256 of the tool at
  `4fd3b292`. Panel 16 weakenings / 6 neutrals; gate mutants 22 — equal to the receipt's denominators.

Evidence-verified: `receipts/c2-measured-r93.txt:83` → `MADO_SELFTEST_STRENGTH: TARGET_MET pred=PRED-C2-r93-v1
rev=4fd3b292… checks=23 frozen_pin=ok positive=OK:0 kill_set_pin=ok neutralised_flagged=23/23 hand_flagged=16/16
neutral_ok=6/6 mutants=22 killed=22 crashed_not_killed=0 do_nothing_flagged=0/39 always_ok_flagged=0/39
always_weak_positive=WEAK:1 shadiff_flagged=39/39 shadiff_neutral_ok=0/6 gate_selftest=ok`, `rc=0`; separability
`receipts/c2-at-c1-r93.txt` `SETUP_ERROR … gate/kill-set/tool absent at 0a85e687…`, `rc=2`. Self-test tally
(`harm-final-r93.txt:78`) `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0`; live run `SELFTEST_STRENGTH: OK
kills=32 held=32 survived=0 wrong_check=0`. Registry rows `mado-selftest-strength` and `mado-r93-selftest-strength`
(gates) at `SKILL.md:879-880`. The gate itself was not executed here.

Verdict: **verified** — operability `improved` (0/23 → 23/23 single-check neutralisations flagged; do-nothing 0/39).

### Harm

- `git diff 4c6f723f 28a97421 -- SCORECARD.md`: one appended `## Round 93` section, no removed line.
- `git diff --stat 4c6f723f 28a97421 -- tools/mado-mime.py tools/mado-mako.py tools/mado-xdgmime.py tools/mado-verify.sh
  quality/check-seat-reports.py quality/check-receipt-presence.py` → empty (prior capabilities' code unchanged).
- The ported portals tool keeps the round-90 capability: all 229 round-90 cases with their labels are inside the C1 set
  (366/366 correct), and 59 of 60 round-90 mutants ride the new frozen set (9 re-anchored, X19 excluded as
  crash-shaped). The round-90 counter's `SETUP_ERROR mutant M03 find occurs 0 times` is declared (QUALITY 155) and its
  receipt stays pinned at `7bec2399` — not a harm.
- `receipts/harm-final-r93.txt` (at `4fd3b292`): `MADO_SELFTEST: 460/460`, `MADO_VERIFY: CLEAN (29 pass …)`,
  `indexed=114/114`, `LEDGER … population=179 … TARGET_MET`, portals 28/0, mime 17/0, xdgmime 12/0, mako 62/0 (after the
  append-only correction), seat-reports 23/0, receipt-presence 6/0, receipt-presence counter 83/83, round-92 C2 45/45
  with round-91 leg 59/59.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 re-measured (base bytes → frozen candidate; pins and host binary hold; 80-case byte subset composition; my 18/18 vs base 7/15 on the installed binary) and evidence-verified (366/366, 80/80 from 32/80, fresh 120/120 + 60/60, 75/75, forgery fails fresh_bytes 50/60) |
| operability | improved | C2 re-measured (instrument absent → frozen gate + kill-set; pins hold; 32 kills cover 23/23 selftest checks; tool pin = tool) and evidence-verified (23/23, 16/16, 6/6 neutral, 22/22, do-nothing 0/39, always-OK 0/39, sha-diff 0/6 neutral, selftest 11/11) |

No owned axis harmed.

## Discernment spot-check (`corpus/lessons/round-93.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/portal-keyfile-bytes-r93.md` | admit | `curl` 2026-11-07 of `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/{gstrfuncs.c,gstrfuncs.h,gkeyfile.c}` and `https://raw.githubusercontent.com/flatpak/xdg-desktop-portal/1.22.1/src/xdp-portal-config.c` → sha256 `6ea1c4333161ec4e…`, `298b0dc4c8280532…`, `e1d1270f6c9881da…`, `2da4fd835032401b…` = S511–S514 pins; `/usr/lib/xdg-desktop-portal`; my fixtures | agree | gstrfuncs.c:264 is the bytes 8–15 row `0x004, 0x104, 0x104, 0x004, 0x104, 0x104, 0x004, 0x004` (VT = `0x004`, no space bit); gstrfuncs.h:86 the `g_ascii_isspace` macro; gkeyfile.c:1625/1738/1757 the three `g_ascii_isspace` loops, :1760 `value_len = line + length - value_start` (no trailing strip), :2310/:2427 `g_utf8_validate (value…)` at value read, :4563 the C-string comment test; the entry's §3.8 table (only the group-header VT voids, the other positions mangle) reproduces on the binary with a distinguishing `FileChooser=kde` key, and its §2 per-read UTF-8 rule reproduces (comment/other-group bad bytes harmless, read value voids) |
| the draft's "a VT at line start/key end/value start voids the file" | reject (rewritten before the freeze) | same gkeyfile.c fetch :1625, :1738, :1757; my binary rows `\vdefault=kde`, `default\v=kde`, `default=\vkde` each + `FileChooser=kde` | agree | in all three the binary still applies `FileChooser=kde` from the same file, so the file is not voided — only the one key/value is mangled; only `\v[preferred]` voids (all gtk). The sentence was over-strong and correctly rejected |
| a registry row for `src/portal-impl.c` | reject | `curl -s -o /dev/null -w '%{http_code}' https://raw.githubusercontent.com/flatpak/xdg-desktop-portal/1.22.1/src/portal-impl.c` | agree | `404` at the tag; the reader at 1.22.1 is `xdp-portal-config.c` (fetched 200, sha = S513) |

`corpus/SOURCES.md` rows re-opened (all four new rows; quotes live in the lesson's `## Gate` table):

- S511 quote `0x004, 0x104, 0x104, 0x004, 0x104, 0x104, 0x004, 0x004,` — gstrfuncs.c line 264, exact; 8 tokens.
- S512 quote `((g_ascii_table[(guchar) (c)] & G_ASCII_SPACE) != 0)` — gstrfuncs.h line 86, exact; ≤ 25 words.
- S513 quote `g_critical ("Invalid portals for interface '%s' in %s", ifaces[i], portal_file);` — xdp-portal-config.c line
  430, exact; 10 words. Its scope ("eager per-key read that voids a whole config file on one failed value read") matches
  my probe row `default=kde` + unread `zzz=\xff\xfe` → binary gtk.
- S514 quote `return (*line == '#' || *line == '\0' || *line == '\n');` — gkeyfile.c line 4563, exact; ≤ 25 words.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, rc 0; findings
`W04` 56 (new: S514, shared URL with S502 under another scope), `W01` 1 (S277) — the report's "W04 55 → 56". Rows
`grep -cE '^ {0,3}\| S[0-9]{3,} ' corpus/SOURCES.md`: 445 at `4c6f723f` → 449 at `28a97421`.

## Trend verdicts

- **expansion — improved.** One admitted entry on an edge class the coverage map did not hold (`git ls-tree --name-only
  <rev> corpus/knowledge/ | wc -l` 113 → 114), four tier-A rows (445 → 449), one capability row (selftest-strength gate).
  The admit survived my re-check against all four primary sources and the installed binary.
- **quality — improved.** The round-90 tool's byte divergences (round-91 M91-1, round-92 routed defect 2) are closed
  and re-measured: landed 18/18 vs base 7/15 on my own fixtures, round-90 cases carried 229/229 with labels; the
  seat-report gate's selftest is now guarded against weakening (routed defect 3); harm watch green; the one harness
  defect in a receipt was corrected append-only before landing.
- **discernment — improved.** The outside spot-check agrees with the gate on the sampled admit and both sampled
  rejects; the over-strong VT sentence was caught by the wave and its rejection is confirmed on the binary with a
  void-vs-mangle-distinguishing fixture.

## Routed defects (lane fixes next round)

1. QUALITY 158 (seat source URLs must come from a registry row or an L1 fetch) has no instrument — the report routes it
   itself; build one or record why it stays a judgement rule.
2. The selftest-strength gate is wired for `quality/check-seat-reports.py` only; the lane's other gates' selftests
   (`mado-verify.sh`, `mado-portals.py`, `mado-mime.py`, `mado-xdgmime.py`, `mado-mako.py`, `check-receipt-presence.py`,
   `check-selftest-strength.py` itself) remain unguarded against a weakened passing assertion.
3. Entry §8 "no frozen case" classes (trailing TAB/FF in a value; VT before a `#` comment): this closure's binary probe
   confirms the entry's predictions and the tool's answers (3/3) — freeze them as cases so the prediction is gated, and
   update §8 append-only.

## For the operator (promotion is operator-owned)

SHONEN box 2 (end-to-end task) and box 3 (instructions executable without oral context) look checkable by a non-author:
this closure ran `tools/mado-portals.py` from its `--help` alone (`--portal-dir … --desktop … --json`) against the
installed xdg-desktop-portal on 18 fixtures of its own and matched 18/18. Nothing was written to `SHONEN.md`.
