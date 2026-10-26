# Round 46 drafts - SCORECARD section, capabilities row, LOG.md entry skeleton

Seat `ScrScorecard` (scribe), wave `w1` round 46, 2026-10-26. Lane `mado-shokunin`.

**Conventions.** `<AFTER>` marks a value or verdict that can only exist after the round-46 data commit; nothing here is
invented to fill one. Every *before* value is a line of the cited receipt. Insertion points: the SCORECARD block goes
after the last line of the Round 45 section (`SCORECARD.md:2623`); the LOG block goes at the end of `LOG.md`
(`LOG.md:2513`). Round 45's text is never rewritten; after values of earlier rounds are appended, not edited.

Sources seen (read-only): `registration.md` (freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, base
`b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`), `receipts/axis-base.txt`, `receipts/c1-before-base.txt`,
`receipts/c2-before-base.txt`, `receipts/c2-ground-base.txt`, `receipts/census-before.txt`,
`receipts/ctl-c1.txt`, `receipts/ctl-c2.txt`, `receipts/live-devices-host-l1.txt`, `receipts/fetch-sha256.txt`,
`.ufo/waves/round-46/l1-draft/{entry.md,mado-devices.py,build-pos.py}`, the two counter docstrings,
`.ufo/waves/round-46/w1-spec.json` (66 items), `corpus/lessons/round-45-verifier-spotcheck.md` §6.

---

## 1. SCORECARD.md - Round 46 section (append after `SCORECARD.md:2623`)

```markdown
## Round 46 - mado-devices and the input-device entry (2026-10-26, attempt 1)

Registration `.ufo/waves/round-46/registration.md` (freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`), no supersession: policy v2 from the freeze, one wave `w1` (66 seats, band 64-128) carrying build, attack and the round-45 w2 falsification the round-45 run never ran (closure D1). Data commit `<AFTER>`. Lowest-axis rule: every published axis tied at its maximum at base (`receipts/axis-base.txt`: navigation 62/62, calibration 73/73, operability 12/12; `MADO_AXIS: checked=3 mismatched=0`), so each is a lowest axis; the claims' after-states are their counters' lines. Should w1 find a hole before any data commit, a `registration-v2.md` with a new freeze and new controls supersedes this one (`<AFTER - superseded: no | yes, freeze ...>`).

Controls frozen before data (`ctl/run-c1-controls.py`, `ctl/run-c2-controls.py`): `receipts/ctl-c1.txt` - `CTL_C1 VERDICT: PASS (controls scoring TARGET_MET: 0 of 23; reference met: 1)` (REF `TARGET_MET`; BASE, STUB, the round-45 `mado-monitors.py` copy and V01-V20 `TARGET_MISSED`); `receipts/ctl-c2.txt` - `CTL_C2 VERDICT: PASS (wrong=0 of 15; positive admitted=1)` (P admitted; C2-BASE, R45-COPY, SHELL, WIDE-RANGE, HIDDEN-LINE, FORGED-PIN, FALSE-URL, PROSE-CENSUS, ANCHOR-PAST-EOF, PROSE-CENSUS-SPACED, ROW-SUPERSEDES, FENCE-TABLE, RECEIPT-CONTRADICT, README-IDS rejected).

| Claim / axis | Before -> after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **operability** (capability acquisition) - new `tools/mado-devices.py` joins the `input`/`device` config lines with one `hyprctl devices -j` dump | `fixtures=0/90 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` exit 1 at base (`receipts/c1-before-base.txt`) -> `<AFTER - receipts/c1-after-data.txt>`; target per the registration: `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` exit 0 at the data commit and the tip, under any nonce | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r46-devices.py --repo . --rev <rev> --work <scratch outside /home/vgpnk/Projects/shokunin> [--nonce N]` (`PRED-C1-r46`) | recorded in the round report from the receipts (`<AFTER>`) |
| C2 **coverage** (sourced) - new `corpus/knowledge/hyprland-input-devices-r46.md`, the chain from config to `hyprctl devices -j` at the host's Hyprland 0.56.2 and hyprlang 0.6.8 | `admitted=0/1 verdict=TARGET_MISSED` exit 1 at base, `clauses=a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 i:0 j:0` (`receipts/c2-before-base.txt`); the per-device chain grep exits 1 at base (`receipts/c2-ground-base.txt`) -> `<AFTER - receipts/c2-after-data.txt>`; target: `admitted=1/1 verdict=TARGET_MET` exit 0 at the data commit and the tip | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r46-input-device-entry.py --repo . --rev <rev>` (`PRED-C2-r46`) | recorded in the round report from the receipts (`<AFTER>`) |

Round-45 w2 (closure D1, appended, never rewriting the Round 45 text): `<AFTER - the falsification verdicts on the round-45 tool, entry and gate, from w1/ExecW2Monitors.md, CritW2ToolSemantics.md, CritW2Entry.md, CritW2Gate.md, RevW2Rows.md, RevW2Counters.md, MutW2Tool.md, SentW2Privacy.md; corrections landed after the round-45 data commit>`.

Separable: `<AFTER - w1/ExecC1Separability.md on scratch trees, both directions; the shared-assumption check is w1/ConnCrossClaim.md>`; registration's expectation: a tool-only tree meets C1 and misses C2, a data-only tree misses C1 and meets C2.

### Capabilities (round 46)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| keyboard XKB name and pointer scroll factor versus live device state join | read the `input` and `device` lines of one or more Hyprland config files and one `hyprctl devices -j` dump and report, per keyboard, the expected XKB names (device block value where the block sets it, else the global `input:kb_*`, else the default `us`/empty) against the printed rules as AGREE / DIFFER / FALLBACK (printed `us` with four empty names = a keymap that did not compile) / VIRTUAL (`hl-virtual-keyboard*`), per mouse the expected scroll factor (device block `scroll_factor` clamped 0..100 when the block sets it, else -1) as AGREE / DIFFER, per `device` block MATCHED / NO_SUCH_DEVICE, with top verdict NOT_COMPARED 5 \| DIFFER 1 \| NO_KEYBOARDS 3 \| STALE_BLOCK 4 \| OK 0; starts no process, opens no socket | `tools/mado-devices.py` (selftest `<AFTER - landed N/N; the frozen reference prints 48/48>`); `quality/counters/c1-r46-devices.py` `<AFTER - 90/90 + 150/150 at the data commit>`; live host run `.ufo/waves/round-46/receipts/live-devices-host-l1.txt` (`keyboards=10 agree=9 differ=0 fallback=0 virtual=1 mice=4 mice_differ=0 verdict=OK`, exit 0) | 46 |

### Sources, saturation, planned

Sources 252 -> 262 rows (S316-S325, tier A, `mined`, opened 2026-10-26; S317 and S320 repeat held URLs under the input-device scope - S162/S303 legacy `ConfigManager.cpp` and S158/S307 `HyprCtl.cpp` - so the census W04 count grows by two; `receipts/census-before.txt` holds 10 warnings at base). Knowledge entries 62 -> 63. Assimilation: the `merge/mado/` input-device theme read read-only (`w1/ScoutShokuknow.md`, `w1/ExecIdGuard.md`), `<AFTER - admitted as one entry / refused with reasons and flips>`. considerthese `2026-10-26.md` proposal 2 (a ledger of live-state tools) mined `<AFTER - QUALITY N>`; proposal 3 (age count per routed defect) mined into the lesson `<AFTER>`. Mistakes M46-1..`<AFTER>` (`grep -c '^\*\*M46-' corpus/lessons/round-46.md`); QUALITY `<AFTER>` (round 45 closed at 86). Saturation 9.0 / N=3 unchanged (standing line); retired: none.

Axis table re-derived at `<AFTER - data commit>` (`receipts/axis-data.txt`): navigation `<AFTER>`, calibration resolved-active `<AFTER>`, operability selftest `<AFTER>`; `receipts/axis-base.txt` gives 62/62, 73/73 and 12/12 at base.

### Planned (round 47; intent only)

1. Wave w2 falsification of the round-46 data: w1's attacks are pre-data (the contract, the entry, the counters) plus the round-45 falsification (closure D1), so the landed round-46 tool, entry and rows owe a post-data attack; `<AFTER - whether this round schedules a w2 itself>`.
2. The routed defects round 46 leaves open: `<AFTER - from the round-46 closure; candidates: C1's declared residuals (a tool that models the contract is an implementation of it; sandbox detection; a contract error shared by reference and tool is invisible to clause g); C2's claim-to-quote binding and word-form census; the two new census W04 repeats (S317, S320); S290-S297 supersession if w1/ExecSupersede.md did not land it>`.
3. A read-only FALLBACK prediction: compile the declared XKB names with the host's libxkbcommon 1.13.2 and compare a predicted compile failure against the printed `us`/empty names (the entry's Limits keep the compile out of scope; `w1/ExecXkbCompile.md` probed it, `<AFTER - result>`).
4. The virtual keyboard's real keymap (the entry leaves it UNK by design; `w1/LabVirtualRules.md` `<AFTER>`): a nested-compositor oracle, read-only on the host.
5. The `recheck:` trigger: when `hyprctl version` leaves `efb50993` or hyprlang leaves 0.6.8, re-pull the ten pins and re-run both counters; upstream main has moved to a Lua config, so a release past 0.56.x may drop the `device { }` block form the entry and the tool describe.

### Wave w1 outcome (round 46)

Wave `w1` (66 seats, band 64-128, policy v2 - at the run-9 floor of 64 and inside the band; executor 18, critic 15, scribe 9, reviewer 6, connector 5, mutation-tester 4, scout 4, sentinel 3, simplifier 1, revenger 1; attack roles 29/66 = 44 %; `<AFTER - dead seats, reports>`): independent rebuilds `<AFTER - w1/ExecIndepA.md, ExecIndepB.md>`; cheats, forgeries and contract errors `<AFTER - w1/CritC1Cheat.md, CritC1Narrow.md, CritC2Forgery.md, CritToolSemantics.md, CritEntryContent.md, MutTool.md, MutC1Counter.md, MutC2Counter.md>`; the round-45 w2 ran inside this wave `<AFTER - w1/ExecW2Monitors.md, CritW2ToolSemantics.md, CritW2Entry.md, CritW2Gate.md, RevW2Rows.md, RevW2Counters.md, MutW2Tool.md, SentW2Privacy.md>`; round-45 closure D2 `<AFTER - w1/ExecSerialRule.md, ScrSerialCorrection.md>`, D3 `<AFTER - w1/ExecSessionTriage.md>`, D4/D5 `<AFTER - w1/ScrErrata.md>`, D6 `<AFTER - w1/ExecSupersede.md>`.
```

---

## 2. LOG.md - Round 46 entry (append after `LOG.md:2513`)

```markdown
## Round 46 (2026-10-26, hyaku run 9, attempt 1)

- Protocol load; round-45 closure (`corpus/lessons/round-45-verifier-spotcheck.md` §6 D1-D6) routed into `corpus/lessons/round-46.md`; census before `receipts/census-before.txt` exit 0 (10 warnings: 9 W04 URL repeats, 1 W01 tierC used-by; registry 252 rows, last S315); base `b22ea56b`.
- Freeze `8c5434c6` (frozen once, policy v2, no supersession `<AFTER - or registration-v2.md and its freeze>`): PRED-C1-r46 (new tool `tools/mado-devices.py`, reference `.ufo/waves/round-46/l1-draft/mado-devices.py` selftest 48/48, 90 fixtures x 3 runs (seed 46 env A, seed 46 env B, nonce env A), bubblewrap isolation, no `hyprctl`/`libinput`/`journalctl`/`udevadm` run, 150 nonce-generated cases judged by the pinned reference; controls `receipts/ctl-c1.txt`: PASS, 0 of 23 met, reference met) and PRED-C2-r46 (input-device entry, ten pins fetched and opened 2026-10-26 (`receipts/fetch-sha256.txt`), census line `hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100 json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard`, 28 surfaces; controls `receipts/ctl-c2.txt`: PASS, P admitted, 14 do-nothing/forged rejected).
- Before: C1 `fixtures=0/90 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` exit 1 (`receipts/c1-before-base.txt`); C2 `admitted=0/1 verdict=TARGET_MISSED` exit 1, clauses a-j all 0 (`receipts/c2-before-base.txt`); the per-device chain grep exits 1 at base (`receipts/c2-ground-base.txt`).
- Wave `w1` (66 seats, band 64-128; executor 18, critic 15, scribe 9, reviewer 6, connector 5, mutation-tester 4, scout 4, sentinel 3, simplifier 1, revenger 1; attack roles 29/66 = 44 %; `<AFTER - dead seats / reports>`): independent rebuilds `<AFTER - w1/ExecIndepA.md, ExecIndepB.md>`; `<AFTER - cheats and forgeries met or rejected, contract errors found: w1/CritC1Cheat.md, CritC1Narrow.md, CritC2Forgery.md, CritToolSemantics.md, CritEntryContent.md>`; the round-45 w2 (closure D1) run inside this wave `<AFTER - w1/ExecW2Monitors.md, CritW2ToolSemantics.md, CritW2Entry.md, CritW2Gate.md, RevW2Rows.md, RevW2Counters.md, MutW2Tool.md, SentW2Privacy.md>`; D2 `<AFTER - ExecSerialRule.md, ScrSerialCorrection.md>`; D3 `<AFTER - ExecSessionTriage.md>`; D4/D5 `<AFTER - ScrErrata.md>`; D6 `<AFTER - ExecSupersede.md>`.
- Data `<AFTER>`: `tools/mado-devices.py`, entry `corpus/knowledge/hyprland-input-devices-r46.md`, rows S316-S325, lesson `corpus/lessons/round-46.md` (Gate + Mistakes), README index row and Frontier bullet, SKILL.md/PROVINCE.md rows, QUALITY `<AFTER>`, gate work `<AFTER>`. Measured: C1 `<AFTER>`, C2 `<AFTER>`; census `<AFTER - mado ok, W04 S317/S320 added>`; live host run of the landed tool `<AFTER - receipts/live-devices-host-r46.txt if produced; the freeze's run is receipts/live-devices-host-l1.txt: keyboards=10 agree=9 virtual=1, verdict=OK, exit 0>`.
- Not run / open: `<AFTER - the round-46 falsification wave if any; routed defects carried to round 47>`.
```

---

## 3. `<AFTER>` map - which artifact fills each placeholder

| Placeholder | Filled by |
|---|---|
| data commit hash (section intro, claim table, axis line) | the commit carrying the tool, entry, rows, lesson, README/SKILL/PROVINCE rows |
| C1 after line + exit | `receipts/c1-after-data.txt` (re-run at the data commit **and** the tip; `PRED-C1-r46` prints `seeds=46,<nonce>`) |
| C2 after line + exit | `receipts/c2-after-data.txt` (`PRED-C2-r46`; clauses a-j) |
| separability | `w1/ExecC1Separability.md` (scratch trees, both directions); shared-assumption check `w1/ConnCrossClaim.md` |
| census after | `receipts/census-after.txt` / `receipts/axis-data.txt` |
| assimilation admit/refuse | `w1/ScoutShokuknow.md`, `w1/ExecIdGuard.md` |
| QUALITY numbers, Mistakes count | `corpus/lessons/round-46.md`, `SKILL.md` registry |
| wave outcome paragraph, dead seats | `w1-results.json` + the seat reports named in the block |
| round-45 w2 line and verdicts (closure D1) | the eight `w1/*W2*` reports, `w1/RevW2Counters.md`, the re-run receipts |

## 4. Flags for the L1

1. `SCORECARD.md:2618-2623` (Round 45 planned 1-3) is the source of the round-46 work: item 1 is this round's w1;
   items 2-3 are carried and partly routed (`ExecSessionTriage`, `ExecSupersede`). Do not edit them; the round-46
   section says which closed.
2. The registration's separability sentence ("to be shown by a w1 seat on scratch trees") means the round-46 section
   must cite a scratch-tree proof, not the counter clauses; `w1/ExecC1Separability.md` is the seat for it.
3. `receipts/live-devices-host-l1.txt` is the freeze's live run of the reference (tool sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b`); if w1 produces a fresh live receipt (`w1/ExecLiveHost.md`), cite the newer one in the capabilities row.
4. The capabilities row's verdict order and exit codes are the tool's, `NOT_COMPARED 5 | DIFFER 1 | NO_KEYBOARDS 3 | STALE_BLOCK 4 | OK 0`
   (`registration.md` C1 sentence; the order of the tests is the reference docstring's, `.ufo/waves/round-46/l1-draft/mado-devices.py`),
   so a reader can check the exit map against the tool's own summary line.
