# CritRegistration — attack on `.ufo/waves/round-46/registration.md`

Seat: **CritRegistration** (critic, leaf; no subagents). Date 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`
at `master = e0be61e4f6e34896f8b1c329f9c6d129e5af81f7` (base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`, freeze
`8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`). Host reads limited to `hyprctl version` and `hyprctl devices -j`.
Receipts for every command below: `.ufo/waves/round-46/w1/CritRegistration/receipts/`.

Verdict: **the registration's measurements and its two claim descriptions hold; one count is wrong (five cross-scope URL
repeats, not two), one framing statement is imprecise, and two routed-item pointers are stale/paraphrased.** No C1 or C2
admission is threatened by any of them.

---

## 1. Findings — wrong or imprecise

### F1 (wrong count) — "The two cross-scope URL repeats (S317 with S162/S303 … S320 with S158/S307 …)"

Truth: **five** round-46 rows reuse a held URL across scopes, and the census prints **five new W04 lines**, not two.

- Held rows whose URL is *exactly* a pin URL: **7 rows on 5 URLs** — S158+S307 (`src/debug/HyprCtl.cpp`), S162+S303
  (`src/config/legacy/ConfigManager.cpp`), S173 (`hyprlang/v0.6.8/src/config.cpp`), S182 (`src/helpers/MiscFunctions.cpp`),
  S215 (`src/config/values/ConfigValues.cpp`). Command: the script in `receipts/held-pin-rows.txt` (extracts each row's URL
  and compares for exact equality against the ten pin URLs). A careless suffix grep also returns **S018**, whose URL is
  `github.com/hyprwm/Hyprland/blob/v0.56.2/src/debug/HyprCtl.cpp` — a different URL from the pin, not a repeat.
- New rows reusing those URLs (`l1-draft/build-pos.py:30-71`): **S317** (ConfigManager), **S318** (ConfigValues),
  **S320** (HyprCtl), **S321** (MiscFunctions), **S324** (hyprlang).
- Census over the positive-control tree (clone at the freeze + `build-pos.py`, recipe of the seat brief):
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <posclone>/corpus/SOURCES.md`
  → `W04 S317`, `W04 S318`, `W04 S320`, `W04 S321`, `W04 S324` on top of the nine already present at base
  (`receipts/census-pos.txt`, 14 W04 lines; `receipts/census-base.txt`, 9 W04 lines incl. S303 and S307). The base run
  was over a copied registry, so it also shows E11 noise; the W04 lines are URL-derived and unaffected.
- **Impacted:** coverage/provenance bookkeeping only. C2's clause e permits a repeat only under a *different* scope cell,
  which all five satisfy, so admission is unaffected and the census still exits 0 with warnings.
- **Smallest safe correction:** in the round lesson/errata (the registration is frozen), write the five:
  S317 with S162+S303; S318 with S215; S320 with S158+S307; S321 with S182; S324 with S173. No counter, fixture, pin,
  reference or control change.

### F2 (imprecise, and not what the cited receipt tests) — "At base the lane holds point readings of `input:kb_layout` only"

Truth: the base corpus holds point `getoption` readings of **all five global keymap names**, not only `kb_layout`:
`input:kb_options` (4 hits), `input:kb_variant` (3), `input:kb_model` (3), `input:kb_rules` (3), plus non-keymap input
readings (`input:touchpad` 20, `input:accel_profile`, `input:sensitivity`, `input:follow_mouse`, `repeat_rate`, …).
Located examples at base: `corpus/knowledge/hyprctl-verification-layer.md:120-124` (layout, variant, model, options, rules
rows) and `corpus/knowledge/config-health-report-r3.md:534-538`. Only `SKILL.md` is `kb_layout`-only (6 hits, no other
`kb_*` name). Command: `git grep -n -o 'input:kb_[a-z_]*' b22ea56 -- corpus SKILL.md | sort | uniq -c`.

The cited receipt (`receipts/c2-ground-base.txt`) proves only that the per-device chain symbols are absent
(`applyConfigToKeyboard|getDeviceString|deviceConfigExists|getConfigValueSafeDevice|scrollFactor|m_keymapOverridden`,
`exit=1`); I reproduced that exit 1. It does not test "`kb_layout` only".

- **Impacted:** the C2 novelty framing (what base already reads), not the predicate.
- **Smallest safe correction:** say "point readings of the global `input:kb_*` names only, and no per-device chain", or
  scope the sentence to `SKILL.md`.

### F3 (stale pointer) — "D4 the untracked `MutC1Counter/results.json`"

Truth at review: that file no longer exists. `.ufo/waves/round-45/w1/MutC1Counter/` now holds an **untracked**
`results.digest.txt` (282 B, mtime 2026-10-26 17:33) whose text says "results.json (untracked, never committed; removed in
round 46 per round-45 closure D4)". `git status --porcelain` reports `?? …/results.digest.txt`; `git ls-files` in that
directory lists only `c1-r45-monitors.py`, `matrix.md`, `mutdrive.py`, `summary.txt`; `find . -name results.json` finds
none under round-45. Commands in the transcript below (`ls -la`, `cat results.digest.txt`, `git ls-files`).

So: true as a description of the closure text (§6 item 4), but false as a present-state pointer, and the D4 remedy is
half-done — the replacement digest is itself untracked and would be lost. A seat assigned D4 must not chase
`results.json`; it must commit the digest (or state retention).

- **Impacted:** routed non-claim bookkeeping only (no claim slot).
- **Smallest safe correction:** point D4 at `results.digest.txt` and commit it (282 B).

### F4 (minor paraphrase) — "considerthese `2026-10-26.md` proposal 3 (age count per routed defect)"

The source line says "I could keep an age count per routed item so long-open ones stand out."
(`considerthese/2026-10-26.md:49`). The queue includes non-defect debts (missing receipts, carry-overs), so "defect"
narrows it. Minor; the proposal number and file are correct.

---

## 2. Precision notes (statements that are true but easy to misread)

- **N1 — `ahead=0 behind=0` is freeze-scoped.** True when written: `git reflog show master` shows `b22ea56` at
  2026-10-26 17:02:19, `8c5434c6` at 17:23:23, `e0be61e4` at 17:33:35; `origin/master` matched at each push. At the
  review revision `git rev-list --left-right --count master...b22ea56` prints **`2 0`** (freeze + controls commits).
  Read as present state, the parenthetical is false; read as "at round start", it is exact.
- **N2 — "one `input` block" is file-scoped and understates the plane.** `~/.config/hypr/input.conf` indeed holds one
  `input` block (`:3`) and no `device` block. The **sourced** plane also holds the stock block
  `~/.local/share/omarchy/default/hypr/input.conf:2` (`kb_layout = us`, sourced at `~/.config/hypr/hyprland.conf:11`), so
  the global-option chain has two `input` blocks. There is **no** `device` block anywhere in the sourced tree
  (`~/.config/hypr/`, `~/.local/share/omarchy/default/hypr/`, `~/.local/state/omarchy/toggles/hypr/`), which is stronger
  than the claim. Registered as a note, not a defect, because the sentence names the user file.
- **N3 — the "10 keyboards and 4 pointers" host line is exact** (`keyboards` 10, `mice` 4, `tablets`/`touch`/`switches` 0),
  but "pointers" is the `mice` array; tablets/touch would be separate arrays and are empty on this host.

---

## 3. Statements verified (claim → command/evidence)

| Registration statement | Evidence |
|---|---|
| Base `b22ea56…`, lane `master` at round start, `ahead=0 behind=0` | `git rev-parse master` = `b22ea56…` in reflog at 17:02:19; `git merge-base --is-ancestor b22ea56 HEAD` → yes; `git rev-list --left-right --count master...b22ea56` → `2 0` (see N1) |
| Hyprland 0.56.2 (`efb50993`) | `hyprctl version` → `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f … Tag: v0.56.2` |
| hyprlang 0.6.8-5; libxkbcommon 1.13.2-1; xkeyboard-config 2.48-1 | `/var/lib/pacman/local/hyprlang-0.6.8-5`, `libxkbcommon-1.13.2-1`, `xkeyboard-config-2.48-1` present; `hyprctl version` reports system hyprlang 0.6.8 |
| 10 keyboards, 4 pointers in `hyprctl devices -j` | `hyprctl devices -j` → `keyboards` 10, `mice` 4 (`receipts/devices-count.txt`) |
| `~/.config/hypr/input.conf` one `input` block, no `device` block | `grep -nE '^\s*input\s*[:{]'` → `:3` only; no `device` token in the file or any sourced file |
| Ground grep `receipts/c2-ground-base.txt`, exit 1 | reproduced: `git grep -n -E "applyConfigToKeyboard\|getDeviceString\|deviceConfigExists\|getConfigValueSafeDevice\|scrollFactor\|m_keymapOverridden" b22ea56 -- corpus SKILL.md` → no match, exit 1 |
| Registry tops at S315 at base (252 rows) | `grep -c '^| S[0-9]' corpus/SOURCES.md` = 252; max id `S315` |
| Axis `MADO_AXIS: checked=3 mismatched=0` | `receipts/axis-base.txt:4`, three `MADO_AXIS_ROW … verdict=MATCH` rows (`:1-3`) |
| Reference selftest 48/48 | `python3 -I l1-draft/mado-devices.py --selftest` → `MADO_DEVICES_SELFTEST: 48/48 passed`, rc 0 |
| Live host run: 9 AGREE, 1 VIRTUAL, 4 pointers AGREE, `verdict=OK`, exit 0 | `receipts/live-devices-host-l1.txt:5-20`; reproduced live from `hyprctl devices -j` → byte-identical body, rc 0 (`receipts/live-rerun.txt`); reference sha256 `b229efd0…` = receipt header |
| C1 predicate clauses a/s/f/i/r/g as described | `quality/counters/c1-r46-devices.py` docstring (a tool, s last line `N>=30`, f three runs seed 46 A/B + nonce A, i bwrap hide repo/lane/parent, r markers for hyprctl/libinput/journalctl/udevadm, g 150 generated judged by pinned reference of the counter's lane) |
| C1 before (base) line + `exit 1` | reproduced: `… --rev b22ea56 --work <scratch>` → `PRED-C1-r46: fixtures=0/90 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED`, rc 1 (`receipts/c1base.out`) |
| C1 controls: reference MET; base, stub, monitors copy, V01-V20 MISSED | `receipts/ctl-c1.txt:2-25`, 23 control lines, `VERDICT: PASS (… 0 of 23; reference met: 1)` |
| 90 fixtures; `case-exact-dump-name` added | `quality/counters/c1-r46-fixtures.json` is a 90-element list; label `case-exact-dump-name` present; its sha256 `027ed508…` equals `FIXTURES_SHA256` |
| C2 ten pins, sha256 in `fetch-sha256.txt` | `sha256sum .ufo/waves/round-46/fetch/*` matches all 10 lines of `receipts/fetch-sha256.txt` |
| Census values `default us / fallback us / device_keys=47 / scroll_factor_max=100 / json_scroll_decimals=2 / virtual_prefix=hl-virtual-keyboard` | pins: `Hyprland-ConfigValues.cpp:272` `"us"`, `Hyprland-IKeyboard.cpp:113` `m_currentRules.layout  = "us";`, `grep -c 'addSpecialConfigValue("device", "'` = 47, `Hyprland-InputManager.cpp:1380` `0.F, 100.F`, `Hyprland-HyprCtl.cpp:770` `{:.2f}`, `Hyprland-protocols-VirtualKeyboard.cpp:12` `"hl-virtual-keyboard"` |
| 28 surfaces; locator width ≤ 30 | `SURFACES` literal length 28; clause j `b - a <= 30` |
| C2 before (base) `admitted=0/1 … TARGET_MISSED`, exit 1 | reproduced (`receipts/c2base.out`), rc 1 |
| C2 controls: P admitted; 14 rejected | `receipts/ctl-c2.txt:1-18`, `controls=15 (P positive; 14 do-nothing/forged)`, `VERDICT: PASS (wrong=0 of 15; positive admitted=1)` |
| C2 positive control admitted on a clone of the freeze | own clone + `build-pos.py` → `admitted=1/1 verdict=TARGET_MET` (`receipts/c2pos.out`) |
| Round-45 data at `ee6659b`, tip `4d22eeb`, w2 never ran | `git ls-tree ee6659b` holds `tools/mado-monitors.py`, `corpus/knowledge/hyprland-monitor-rule-r45.md`, both r45 counters, `quality/check-session-material.py`; `ee6659b` is an ancestor of `4d22eeb` (2 commits); no `.ufo/waves/round-45/w2` directory |
| Wave shape: one v2 wave, 66 seats, band 64-128, ≥25 % attack roles | `w1-spec.json` items = 66; policy v2 `waveMinLanes=64`, `waveMaxLanes=128`; attack roles per policy (reviewer, critic, mutation-tester, labrat) = 6+15+4+0 = **25/66 = 37.9 %** |
| D1/D2/D3/D5/D6 restatements | `corpus/lessons/round-45-verifier-spotcheck.md` §6 items 1,2,3,5,6; `w1-results.json` `seats=41`, 41 results, 41 `output: null` (D5) |
| `considerthese/2026-10-26.md` proposal 3 | file exists; line 49 is the age-count proposal (see F4 for the wording) |
| considerthese mined into the lesson | not yet true at review: it is a planned round-46 discharge, like the C1/C2 targets |

## 4. Not verifiable locally (recorded, not falsified)

- The pre-freeze V03 run ("a pre-freeze run met V03"): the only receipt is the post-freeze `ctl-c1.txt`, which shows V03
  MISSED at 89/90. The fixture it was separated by (`case-exact-dump-name`) exists and is pinned; the history of the
  earlier run is not in the repo.
- "the L1 holds the planner seat": organizational; the 66-item spec contains no planner seat.
- The C1/C2 **targets** (`TARGET_MET` at the data tip): not runnable until data lands; the control references show the
  target line is producible.

## 5. Axis impact and disposition

- Affected axis: **coverage** (census/provenance accounting). **Operability** and both claim predicates are untouched:
  the census exits 0 either way and C2 clause e accepts every cross-scope repeat; C1 never reads the registry.
- Corrections needed, in order of importance: F1 wording (five repeats) in the round lesson/errata; F3 (commit the
  282 B digest, stop naming `results.json`); F2 and F4 wording in the lesson; N1–N3 as reader notes.
- Nothing here requires a re-registration, a control change, or a counter edit.

## 6. Tooling and cleanup

- No tools installed, no package transactions, no compositor mutation; only `hyprctl version` and `hyprctl devices -j`
  were read. Git in the lane was read-only; the only commits were in the scratch clone (identity `seat@scratch.invalid`,
  `--show-toplevel` asserted).
- Scratch `/fast/scratch/hyaku/mado-r46/CritRegistration` (evidence copied into `receipts/` first) removed before yield.
