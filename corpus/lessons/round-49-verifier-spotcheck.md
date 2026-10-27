author: hyaku closure (non-author integrator, @m_opus)

# mado round 49 — non-author closure spot-check

Lane HEAD before `03e4ae76aff7a4be59cb69970dd553baa319695a`, after `8a370cd481c6044b2f5c09fd66acde8fc54d173c`.
Driver digest (`.ufo/watchdog.log`, mutable — copied here):
`2026-10-27T01:23:18-03:00 launch mado round=49 pgid=519055 driver=hyaku-inline attempt=1` /
`2026-10-27T02:37:17-03:00 complete mado round=49; hyaku-inline attempt=1`.

I did not author the round. I re-checked committed bytes with `git show`/`git ls-tree`/`git diff` at the cited revisions. I re-fetched
the sampled upstream sources on 2026-10-27, ran the landed tool from committed bytes (`git show 430d2569:tools/mado-keysym.py`) in a
scratch dir outside the lane, and compared it with the host's `xkbcli how-to-type` myself. I did not execute the lane counters or
gates (§Gate standard, Closure consequence); I verified their committed receipts instead. No reviewer seats were dispatched. The
scratch dir was removed.

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report landed by the lane | `git log --format='%an %H %ci' -- .ufo/reports/round-49/mado.md` (fleet) | `mado-shokunin b0184c436c2e8d33fb34984a0cfee1c597b37c6f 2026-10-27 02:36:01 -0300`, after lane tip 02:35:14 and before the complete line 02:37:17 | ok |
| SHONEN heading | `grep -n '^## SHONEN'` on the report | `:97`; 4 lines, all `[~]`, one per box | ok |
| cited commits exist and are ancestors | `git cat-file -t <h>` and `git merge-base --is-ancestor <h> master` for 5f37c1b8, dd2e827e, 430d2569, 602e39e3, 8a370cd4 (+ base 03e4ae76) | all `commit`, all ancestors | ok |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain \| wc -l`; `git ls-remote origin refs/heads/master` | `local=remote=8a370cd4… ahead=0 behind=0 head=detached tracked=0 untracked=0`; 0; `8a370cd4…` | ok |
| commits authored by lane identity | `git log --format='%an <%ae> %cn' 03e4ae76..8a370cd4` | 5 commits, all `mado-shokunin <mado@shokunin.local>` | ok |
| prompt carries the contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/mado-round-49.md)` | placeholder substitutions only (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §1-5 at `:3/:9/:42/:80/:99/:131`, §6 hyaku addendum `:141`, §7 scratch `:603`; prompt committed by `mado-shokunin` at `31d30d98` | ok |
| round size | `jq -c .counts .ufo/waves/round-49/w1-dispatch.json` (lane) | `{"spawn":45,"resume":0,"total":45}`; the prompt's floor is 64 (`:161`, `:208`); w2 (38 items) never dispatched | defect D1 (status-neutral) |
| report vs WAVE-DONE | report `:3`, `:122` | filed with 7 w1 seats unsettled (ExecControlsC1, ExecSessionTriage, ScoutHyprBinds, CritPremiseC1, CritPremiseC2, CritRoutedItems, SentPrivacy); the lane repo is clean at closure | defect D2 (status-neutral) |

The report names real committed round work, so it is a report, not a marker: status `ok`.

## 2. Per-claim re-check

**C1 — operability (capability acquisition): `tools/mado-keysym.py` reproduces `xkbcli how-to-type --keymap=FILE --disable-compose --keysym ARG`.**
Re-measured plainly, plus evidence-verified counter.
- Presence: `git cat-file -e 03e4ae76:tools/mado-keysym.py` → `fatal: … not in '03e4ae76'` (absent at base). `git rev-parse
  430d2569:tools/mado-keysym.py 8a370cd4:tools/mado-keysym.py` → `0d65ab7f…` both (unchanged data → tip).
- Identity: `git show 430d2569:tools/mado-keysym.py | sha256sum` → `dcc13cce3b71…0265` = `candidate/mado-keysym.py` = the
  `registration.md:21` candidate sha (`dcc13cce…`).
- Selftest from committed bytes: `python3 -I mado-keysym.py --selftest` (stdin `/dev/null`) → `MADO_KEYSYM_SELFTEST: 38/38 passed`, rc 0.
- Independent parity (my run; `pacman -Q libxkbcommon xkeyboard-config` → `1.13.2-1`, `2.48-1`; `xkbcli --version` → `1.13.2`):
  three keymaps from `xkbcli compile-keymap` (`--layout us`; `--layout de,fr,ru`; `--layout us,gr --variant intl,`) × 30 keysym
  arguments (names, `U20AC`, `U00E9`, `0x41`, `65`, dead keys, keypad, `XF86AudioMute`, modifiers, `Multi_key`, an invalid name,
  `nosuchsym`) = 90 pairs. `xkbcli how-to-type --keymap=F --disable-compose --keysym A` vs the tool: **stdout byte-equal and exit
  code equal in 90/90** (84 rc 0, 6 rc 2). The only stderr differences are the usage banner on the 6 rc-2 errors (`greek_alpha`,
  `nosuchsym`); the first stderr line `ERROR: Failed to convert argument to keysym` is equal. The contract is stdout + exit.
- Fixtures: `jq length quality/counters/c1-r49-fixtures.json` → 633 (report: 633).
- Counter (evidence-verified, not executed): `receipts/c1-base.txt` `rev=03e4ae76… fixtures=0/633 generated=0/150 selftest=fail
  readonly=fail tool=absent verdict=TARGET_MISSED exit=1`; `c1-after-data.txt` `rev=430d2569… nonce=4949` and `c1-after-data-nonce2.txt`
  `nonce=31337`, both `fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET exit=0`, `clause=r trips=0`.
  Do-nothing control `w1/ExecCounterC1/receipts-stub-always2.txt`: `fixtures=52/633 generated=7/60 … TARGET_MISSED rc=1` — measured on
  the w1 draft counter (60 generated), not the frozen 150-case counter (D4). Mutation: `w1/MutCounterC1Draft.md:3` "All five clauses
  (f, g, s, r, t) killed".
- Ruling: **verified**. Before→after reproduces on committed receipts and on my own judge comparison. The freeze was not attacked by
  w2 (the report says so). The report's "57,865 random pairs over 400 keymaps" (reference B, L1 run; `registration.md:22`) has no
  committed receipt; the committed seat evidence is `w1/ExecRefKeysymB.md:51` "24898 comparisons, 0 mismatched" (D3). The claim does
  not rest on that number.

**C2 — coverage (sourced): `corpus/knowledge/hyprland-bind-key-match-r49.md`.** Re-measured plainly.
- `git cat-file -e 8a370cd4:corpus/knowledge/hyprland-bind-key-match-r49.md` → absent. `git ls-tree --name-only <rev> corpus/knowledge/ | wc -l`
  → 65 at base, 65 at tip. Rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 288 at base, 288 at tip.
- Counter receipt `receipts/c2-at-data.txt`: `clause=a entry_absent admitted=0/1 verdict=TARGET_MISSED rev=430d2569… exit=1`.
- Ruling: **honest stop**, as reported. No data commit; no claim of landing.

Re-measured vs evidence-verified: tool presence/identity, selftest, 90-pair judge parity, fixture count, C2 absence, knowledge and
row counts, SCORECARD/LOG diffs, census, operator-cache digest were re-measured by me. PRED-C1-r49/PRED-C2-r49 verdicts, the stub
control, the mutation result and the axis check were verified from committed receipts.

Harm watch: `git diff --numstat 03e4ae76 8a370cd4 -- LOG.md SCORECARD.md corpus/ SKILL.md PROVINCE.md` → LOG +9/0, SCORECARD +23/0,
`corpus/lessons/round-49.md` +64/0; nothing else under corpus/, SKILL.md, PROVINCE.md. `git diff --diff-filter=DMR --name-status` → only
`M LOG.md`, `M SCORECARD.md`: no file deleted or renamed. The round adds 992 files: 938 under `.ufo/waves/round-49/`, the 47 round-48
`*.synthetic` sidecars (45 under `round-45/w1`, 2 under `round-46/w1`; N1's 47 reproduces), the lesson, two counters + fixtures, the tool.
Axis receipt `receipts/axis-tip.txt` (evidence-verified): `MADO_AXIS: checked=3 mismatched=0 rev=602e39e3…` (navigation 65/65,
calibration 86/86, operability 12/12). Operator state: `receipts/operator-state-before.txt` and `-after.txt` carry the same five digests;
today `sha256sum ~/.cache/xdg-terminal-exec` → `ddd94f6b…b3d5`, `stat` → mtime 1793069967, 190 B (unchanged). No axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1: tool absent → present; base `TARGET_MISSED` → `633/633 + 150/150 TARGET_MET` (receipts, two nonces); selftest 38/38 from committed bytes; my 90/90 stdout+exit parity against host `xkbcli how-to-type` 1.13.2; capability row in SCORECARD round 49 |
| coverage | unchanged | C2 honest stop: entry absent at tip; knowledge 65 → 65; rows 288 → 288 |
| depth | unchanged | `SKILL.md` diff empty; the `w1/ScrSkill` draft not landed |
| freshness | unchanged | no held claim re-verified as stale and fixed; upstream pins re-fetched byte-equal (sampled four) but no row written |
| calibration | unchanged | axis stays at max (`checked=3 mismatched=0`); the report self-states the honest stop, the 45-seat floor miss and the unattacked freeze; one cited number (57,865) has no committed receipt (D3) |
| adjacency | unchanged | `w1/ConnSiblings.md`: no sibling claims keysym/bind ground; held S318/S319 cited, not re-registered |

## 4. Discernment spot-check (`corpus/lessons/round-49.md` `## Gate`; full lines `w1/ScrRows/gate.md` §1)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S352 (drafted admit, tier A, code) | admit | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp` re-fetched: HTTP 200, 39334 B, 975 lines, sha256 `8d8f35fc84c4a2f8…` = `fetch/Hyprland-KeybindManager.cpp`; `:369` `const xkb_keysym_t keysym = xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);` | **agree** | Commit-pinned primary source for the bind matcher; quote verbatim at the stated line. A sweep of the pinned files (`grep -n 'xkb_state_update_mask\|m_xkbTranslationState' fetch/Hyprland-*.cpp`) shows the translation state is created at `:332` and only `m_xkbState`/`m_xkbSymState` get `update_mask` (`IKeyboard.cpp:379/382/422`), which grounds the L1's removal of the "8 Shift binds dead" seat claim (M49-1). |
| S355 (drafted admit, tier A, code) | admit | `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keysym.c` re-fetched: HTTP 200, 14948 B, 450 lines, sha256 `123e3390d443b85c…` = pin; `:268` `* The "best" case-insensitive match is the lower-case keysym name. Most` | **agree** | Tagged source of the exact library on the host (1.13.2-1); it is the authority for name→keysym resolution the tool reproduces. Quote verbatim, 9 words. |
| REJECT `https://wiki.hypr.land/0.56.0/Configuring/Basics/Binds/` | reject | re-fetched: HTTP 200, 386362 B, title "Binds – Hyprland Wiki"; 40-hex sha ×0, `efb5099` ×0; `git ls-remote --tags https://github.com/hyprwm/hyprland-wiki` → 0 lines | **agree** | The content is relevant (it has the "segment after" sentence), but the rendered page carries no commit anchor and the wiki has no tags, so the bytes cannot be re-checked. The flip (commit-pinned raw source, drafted S359) is the right one. |
| REJECT ArchWiki `Hyprland` (`https://wiki.archlinux.org/title/Hyprland`) | reject | re-fetched: HTTP 200, 123942 B; `0.56.2` ×0, `resolve_binds_by_sym` ×0, `xkb_keysym` ×0 | **agree** | Community page with no version-pinned bind-resolution behaviour; the primary sources already cover the scope. Counts match the gate line. |
| REJECT re-registering `src/devices/IKeyboard.cpp` at `efb50993` | reject | `corpus/SOURCES.md:268` S319: same URL at the same commit | **agree** | A new row would duplicate held S319 (census would add a W04); citing S319 with a locator is correct. |

Newly written `corpus/SOURCES.md` rows: none this round (288 → 288). I re-opened drafted row S359 instead (`candidate/rows.md:8`):
`https://raw.githubusercontent.com/hyprwm/hyprland-wiki/d5f07c60e16fe03744aabb76e492117b7f7c4679/content/Configuring/Basics/Binds.md`
→ HTTP 200, 19526 B, 600 lines, sha256 `3d8a2a6832da5930…` = the row's digest and `fetch/wiki-Binds.md`. Its gate quote
`The name you should use is the segment after \`XKB_KEY_\`.` (10 words, ≤25) is verbatim at `:40`; `:469` holds the
`resolve_binds_by_sym = 1` note the row cites.
Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0;
`W04` ×17, `W01` ×1, `mado ok`; byte-identical to `receipts/census-after.txt` (minus its `exit=` line).

## 5. Trend verdicts

- **expansion: improved.** One capability row (keysym-to-key parity with how-to-type) enters SCORECARD with a passing run at
  `430d2569`, which I reproduced from committed bytes against the host judge (90/90). No knowledge entry (65 → 65) and no row (288 → 288).
- **quality: unprovable-but-better** (non-author ruling). For: the round-48 routed items are closed with committed, re-checkable
  evidence — N1's 47 reproduces in the diff; N2 (the r48 receipt's "untouched" digest was the mutant's bytes) is now marked in a committed
  lesson (`round-49.md:52-54`) and a labelled operator-state digest pair exists, which I confirmed against today's file; N3 is corrected by
  appended text; the 47 sidecars are committed with their reason. Against: no held knowledge entry was re-verified or superseded, gate v3
  and the host guard are drafts, the session-material gate is still red (110 findings per `w1/CritSidecars`), and the C1 freeze was never
  attacked. Better, not countable; nothing found false and left unmarked.
- **discernment: improved.** All 5 sampled gate decisions (2 admits, 3 rejects) agree on outside re-reading, and the L1 rejected a false
  seat claim (M49-1) that the pinned source refutes. Against: the M49-1 and M49-3 criteria are owed, not landed, and the lesson's gate
  counts drift from `gate.md` (D8).

Closure: status `ok`, **admitted=false**, verdict `rejected-honest-stop`. C1 verifies and no axis is harmed, but declared claim C2
stopped honestly without landing, so not every claim verifies.

## 6. Routed defects (lane fixes next round)

1. **D1** (report `:3`, `w1-dispatch.json` counts): 45 seats, below the prompt's 64 floor; w2 (38 items, `w2-items.json`) never
   dispatched (self-reported M49-4). Fix: run w2 against the round-49 freeze before any C2 data, and size the round inside the band.
2. **D2** (report `:3`, `:122`): the report was filed with 7 w1 seats unsettled and no WAVE-DONE. At closure the lane repo is clean.
   Fix: name each of those seats' final state (landed / dead / superseded) in the round-50 report, and confirm no post-report seat
   bytes are pending.
3. **D3** (`registration.md:22`, report `:16`): "57,865 random pairs over 400 random RMLVO keymaps (L1 run)" has no committed receipt or
   counting command; the committed reference-B evidence is `w1/ExecRefKeysymB.md:51` (24898 comparisons). Fix: commit the run's
   receipt with its command, or append a correction naming the committed figure.
4. **D4** (`w1/ExecCounterC1/receipts-stub-always2.txt`): the do-nothing control ran on the w1 draft counter (`generated=7/60`), not on
   the frozen `quality/counters/c1-r49-keysym.py` (150 generated). Fix: commit a do-nothing control run on the frozen counter.
5. **D5** (report `:84`): the round's sourced-claim item is unmet (C2 not landed; S352-S363 rightly held back under CORPUS rule 4).
   Carried with C2 into round 50.
6. **D6** (`round-49.md:35`, `:43`): QUALITY criteria owed for M49-1 (host-consequence model must cite the source line that sets its
   state) and M49-3 (`test -f` every reported deliverable). Lane's own planned item 3.
7. **D7** carried: M48-8 gate v3 drafted, not installed; session-material gate red (110); M48-10 host guard drafted, not installed.
8. **D8** (`round-49.md:26`): "the 2 drafted admits and 4 rejects above" — the section lists 2 located admits and 5 rejected
   sources (wiki ×2, ArchWiki, IKeyboard.cpp, ConfigValues.cpp), and `w1/ScrRows/gate.md` §1 holds 12 admits and 5 REJECT lines.
   Same class as round-48 N3. Fix: append a correction line with the counting command.

SHONEN boxes remain `[~]` (the closure writes no `[x]`). For the operator: box 3 (instructions executable without oral context) held for
me — the tool's docstring usage (`--selftest`, `how-to-type --keymap FILE --disable-compose --keysym ARG`) ran as written. Box 2's LOG
round-49 task is reproducible by a non-author (my 90-pair parity). Boxes 1 and 4 were not independently swept this pass. Promotion
review is operator-owned.
