# ConnLessons — round 46 w1: do rounds 43-45 mistake classes repeat in this freeze?

Seat: ConnLessons (task, leaf). Scope: read `corpus/lessons/round-43.md`, `round-44.md`, `round-45.md`
`## Mistakes` plus the three non-author spot-checks (`round-43/44/45-verifier-spotcheck.md`); group by
class; check each class against the round-46 freeze (registration, counters, controls, receipts) with
file:line. Tools installed: none. Scratch: `/fast/scratch/hyaku/mado-r46/ConnLessons` (used for the
reference selftest run only; deleted at exit).

Freeze under test: `.ufo/waves/round-46/registration.md` at `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`
(base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`); counters `quality/counters/c1-r46-devices.py`,
`c2-r46-input-device-entry.py`, `c1-r46-fixtures.json`; receipts under `.ufo/waves/round-46/receipts/`;
drafts under `.ufo/waves/round-46/l1-draft/`.

## Verdict table

| # | class (source mistakes) | round 46 | one-line basis |
|---|---|---|---|
| G | session material / host identity committed (M45-1, M45-2, r44-closure D1) | **REPEATED (new form)** | `receipts/live-devices-host-l1.txt:6-19` prints 14 host device names verbatim; the fence `SKILL.md:571-572` says device inventory keeps "only counts/shape"; the privacy gate cannot see it |
| B | pointer whose target is not committed at the cited revision (M43-3, M44-4) | **REPEATED, resolved before data** | `registration.md:30,52` cite `receipts/ctl-c1.txt`/`ctl-c2.txt`; both absent from freeze `8c5434c`; they land one commit later at `e0be61e4` |
| J | declared residuals left as prose (M44-6; r43-D6, r44-D5) | **PARTIALLY** | same residuals as r45 re-declared (`registration.md:36,56`); kill rule now present (`:27`,`:51`) |
| A | locator asserted, not computed (M43-1, M43-7) | not repeated | ~20 entry locator ranges re-opened in the pins; all contain their anchor; all anchors inside receipt line counts |
| C | count/range published without a recomputing command (M43-2, M44-5) | not repeated | "0 of 23" recomputed by grep = 23 non-reference controls; "controls=15" = P + 14 enumerated; 90/150/28/10/4 all re-derived |
| D | write-time run / driver line read as outcome (M43-6, M44-7) | not repeated at the freeze | `axis-base.txt` committed at the freeze names rev `b22ea56…`; before receipts deterministic |
| E | vacuous gate, subset of named inputs checked (M43-8, M44-8, M45-3, M45-4) | not repeated | C2 clause d digest-checks held ids too, clause i covers every PINS name; C1 sandbox+nonce+readonly clauses; all controls die in `ctl-c1.txt`/`ctl-c2.txt` |
| F | universal inference from a partial source set (M43-9) | not repeated, pin-scoped | the entry's two "never" claims survive whole-file greps of the pins (2 assignment sites of `m_scrollFactor`, both read) |
| H | stale premise / contract mis-model (M45-5) | addressed | 20 semantic variants V01-V20 each die; contract locators verified against pins |
| I | number drift / nonce-dependent before state (M45-6, r44-D4) | fixed | `c1-before-base.txt` is `tool=absent` at `seeds=46,46`; deterministic |
| K | premise overstated to size a claim (M44-9) | not repeated | registration wording measured; no "false report" class overstatement |
| L | support claim broader than the code (M44-3) | not repeated | tool docstring "starts no process and opens no socket" (`mado-devices.py:26`) matches imports (json, math, os, re, stat, struct, sys only) |
| M | refusal reason citing a subset; row cell restating a refuted premise (M44-1, M44-2) | N/A at the freeze | no assimilation ADMIT/REFUSE at the freeze; rows S316-S325 are built by the positive control, their teaches cells verified consistent |
| N | frontier step skipped, lesson never written (M43-4) | in flight | "mined mistakes" is a routed frontier step this round; this report is part of it |

---

## G — session material: REPEATED (new form)

Mistake source: M45-1 (live window titles in tracked clients dumps, `corpus/lessons/round-45.md` `## Mistakes`)
and M45-2 (the host monitor serial in a seat file and three held entries, same section), both class `scope`.

Round-46 evidence:
- `.ufo/waves/round-46/receipts/live-devices-host-l1.txt:6-19` — the frozen live run prints 14 verbatim
  host input-device names (`yubico-yubikey-otp+fido+ccid`, `razer-razer-deathadder-v2`,
  `hp--inc-hyperx-alloy-origins-core`, `video-bus`, `power-button`, …) together with the layouts/options
  they run. `hyprctl devices -j` is a device inventory; the receipt retains device identity, not shape.
- The lane's standing fence names this exactly: `SKILL.md:571-572` — "No raw keycodes, keymap contents,
  timings, **device identity** or input recordings are retained. **Device inventory rechecks keep only
  counts/shape.**"
- The registration quotes the receipt (`registration.md:16-17`), so the freeze endorses it.
- Captured-by: **none** — `quality/check-session-material.py` rules R1-R4 (docstring lines 30-48) cover
  client dumps with titles, process tables, monitor serial+description, home listings. No rule reads
  input-device names — the same "the gate reads JSON serial keys, not prose" capture gap as M45-2
  (`corpus/lessons/round-45-verifier-spotcheck.md` §6 D2).
- Spread: the frozen C1 counter embeds the same identities in its fixture name pool
  (`quality/counters/c1-r46-devices.py:96-99`: `hp--inc`, `yubico`, `deathadder-v2`,
  `hyperx-alloy-origins-core`).

Mitigating read (stated for honesty): the seat spec's forbidden list — "window titles, monitor serials/
  process tables or home-directory listings" — does not name input-device names, and device
names are arguably closer to allowed window-class names than to serials. But the lane's own standing fence
(`SKILL.md:571-572`) covers "device identity" without that narrowness, and the
round-45 lesson's class was "session material stayed shape-only", not "titles and serials only". The
routed D2/D3 gate work (prose serial rule) would still not cover device names. **Recommend the w1
privacy-gate triage rule on this receipt** and a counts/shape re-projection for future live device runs.

## B — pointer whose target is not committed at the cited revision: REPEATED (resolved before data)

Mistake source: M44-4 — round-43 entry cited `w1/ExecOracleGkeep/` receipts "by bare path before they
existed" (`corpus/lessons/round-44.md` `## Mistakes` M44-4); M43-3 is the parent class (a box pointing at
a LOG.md line never written).

Round-46 evidence:
- `registration.md:30` — "Controls (`ctl/run-c1-controls.py` → `receipts/ctl-c1.txt`)"; `registration.md:52`
  — "→ `receipts/ctl-c2.txt`".
- `git ls-tree -r --name-only 8c5434c -- .ufo/waves/round-46/receipts/` lists 7 receipts
  (axis-base, c1-before-base, c2-before-base, c2-ground-base, census-before, fetch-sha256,
  live-devices-host-l1) — **no `ctl-c1.txt`, no `ctl-c2.txt`**.
- Both land at `e0be61e4` ("round-46: controls at freeze … w1 spec and dispatch (66 seats, policy v2)");
  `git merge-base --is-ancestor 8c5434c e0be61e4` → 0, so the freeze is the parent.
- Same shape as M44-4 then: a frozen artifact cites files that do not exist at its own revision; they
  resolve at the tip. Difference in impact: the resolution landed before any data commit and before the
  wave, and the receipt contents check out (`ctl-c1.txt:25` "0 of 23"; `ctl-c2.txt:1,17`). The class
  repeated; the harm did not materialise.

## J — declared residuals left as prose: PARTIALLY

Mistake source: M44-6 ("the round closed with predicate holes it had itself declared… no kill rule",
`corpus/lessons/round-44.md`), carried by r43-D6 and r44-D5.

Round-46 evidence:
- The same residuals are re-declared: `registration.md:36` — "a tool may detect a sandbox by means not
  varied in environment B" and "clause g's oracle is the reference, so a contract error shared by
  reference and tool is invisible to it" are carried over from r45 v2 unmitigated; `registration.md:56`
  re-declares the C2 reading-residuals (claim-to-quote binding, word-form census).
- What is new vs M44-6: an explicit kill rule (`registration.md:27`, `:51` — "anything else at the data
  tip is a miss, reported as an honest stop; no narrowing") and a single-wave v2 design, so the "no kill
  rule" half of the class is fixed. The "residuals as prose, no instrument" half repeats by design — no
  new instrument covers sandbox detection or the self-referential oracle.

---

## Not repeated — with the evidence

**A (locators).** Re-opened ~20 locator ranges carried by `.ufo/waves/round-46/l1-draft/entry.md`
(steps 1-7 and the OBS lines) inside the pins: `Hyprland-InputManager.cpp:1213-1238`
(applyConfigToKeyboard, six `getDeviceString` calls), `:1226-1231` (LAYOUT at :1229), `:1282-1295`
(setKeymap at :1287), `:1376-1383` (the if/else scroll-factor block), `:2119-2131`
(getNameForNewDevice); `Hyprland-ConfigManager.cpp:518-540` (device registration), `:1115-1123`
(set-by-user test at :1119), `:1156-1168` (STRVAL_EMPTY), `:1196-1201` (deviceConfigExists);
`Hyprland-ConfigValues.cpp:272` (`MS<String>("input:kb_layout", …, "us",`, exactly 1 occurrence);
`Hyprland-IKeyboard.cpp:60-64` (overridden early return), `:87-96` (kb_file), `:101-116` (fallback, layout
reset at :113 — the only `m_currentRules.layout =` site); `Hyprland-HyprCtl.cpp:765-772` (scrollFactor
`{:.2f}` at :770, exactly 1); `Hyprland-MiscFunctions.cpp:777-789` (normalizer, `case ','` at :782);
`Hyprland-VirtualKeyboard.cpp:36-44` (`m_keymapOverridden = true` at :41);
`Hyprland-protocols-VirtualKeyboard.cpp:12` (`std::string name = "hl-virtual-keyboard"`, exactly 1);
`hyprlang-config.cpp:44-66,291-320,420-440` (error text at :435),`:674-700` (`##` escape),`:885-899`
(reset at close); `wiki-Keywords.md:64-70` (ONLY sentence at :67),`:79`. All anchors land; all anchors
are inside the pin line counts (`wc -l`: InputManager 2315, hyprlang 1158, HyprCtl 2346, …).

**C (counts).** `ctl-c1.txt:25` "0 of 23" recomputes: `grep -c '^CTL_C1 '` → 25 lines = REF + BASE + STUB
+ MONITORS-COPY + V01..V20 + VERDICT; non-reference, non-verdict = 23, and `registration.md:30-33`
enumerates exactly those 23. `ctl-c2.txt:1` "controls=15 (P positive; 14 do-nothing/forged)" matches the
14 named rejections at `registration.md:52-55`. Fixtures JSON has 90 entries and sha256
`027ed508…` = the counter's `FIXTURES_SHA256`; reference sha256 `b229efd0…` = `MODEL_SHA256` =
the live receipt's header hash. Selftest "48/48" (`registration.md:16`) reproduced:
`python3 -I l1-draft/mado-devices.py --selftest` → `MADO_DEVICES_SELFTEST: 48/48 passed`, exit 0 (scratch run).

**D (write-time read).** `receipts/axis-base.txt` is committed at the freeze and names
`rev=b22ea56…` (the base). `receipts/c1-before-base.txt` names the base rev and is deterministic
(`tool=absent`). The live receipt exists at the freeze with the reference hash in its header.

**E (vacuous gate).** C2 counter clause d: "a receipt whose file name is one of PINS must be at FETCH/<name>
with exactly the pinned sha256 — held ids included" (`c2-r46-input-device-entry.py` docstring); clause i:
"the Gate receipts of the cited ids cover every name in PINS"; T1-T5 carried from r45 v2. Control
evidence: `ctl-c2.txt` FORGED-PIN dies `d:0`; P admitted `a:1..j:1`. C1 counter clauses i (bwrap
sandbox), r (PATH trap for hyprctl/libinput/journalctl/udevadm), g (150 nonce cases judged by the pinned
reference) — all 20 variants V01-V20 MISS (`ctl-c1.txt:7-24`), reference MET (`:1`). bwrap present at
`/usr/bin/bwrap`.

**F (universal from partial set).** The entry's "never" claims survive whole-file checks of the pins:
"The global `input:scroll_factor` therefore never reaches the printed field" — `m_scrollFactor` has
exactly two assignment sites in InputManager.cpp (`:1380` clamp under `deviceConfigExplicitlySet`,
`:1382` `std::nullopt` in the else); the else makes the universal exact, not inferred. "A block written
with the product name never matches" — `deviceConfigExists` compares the stored key exactly
(`ConfigManager.cpp:1196-1201`). The census line the entry carries verbatim (`entry.md:53`) recomputes
from the pins: device_keys `grep -c 'addSpecialConfigValue("device", "'` → 47; clamp ceiling 100
(InputManager.cpp:1380); JSON decimals 2 (HyprCtl.cpp:770); prefix `hl-virtual-keyboard`
(protocols/VirtualKeyboard.cpp:12); fallback us (IKeyboard.cpp:113); default us (ConfigValues.cpp:272).
`receipts/fetch-sha256.txt` is byte-identical to the counter's PINS table.

**H (stale premise).** Each of the 20 modelled semantics has a control that undoes exactly one; all die on
fixtures + generated cases (`ctl-c1.txt`). The contract's chain (device-first → set-by-user test →
global fallback → setKeymap → compile-or-reset → dump) was verified at the pins above. Declared residual
stands: "whether the contract matches Hyprland beyond the pins is the non-author reading"
(`c1-r46-devices.py` docstring).

**I (number drift).** The C1 before-state is `tool=absent` — no nonce dependence (`c1-before-base.txt`,
`seeds=46,46`); the r45 v2 fix (deterministic before, fixture part seeded separately) is carried
unchanged into r46.

**K/L/M/N.** K: the registration's only strong wording — "the round-45 w2 falsification the last round
never ran" — is in the goal text and is true (r45 closure §6 D1: w2 absent, 41 seats < 64 floor). L: the
tool's self-description matches its code (imports json math os re stat struct sys; no socket/subprocess
outside the docstring sentence). M: no assimilation decisions exist at the freeze to under-cite. N: the
lesson is routed work this round, not yet due.

## One synthesis note

The two repeated classes (G, B) are both "the freeze cites bytes that are not there / not shape-only" —
the M43-3/M44-4/M45-1 family. B was caught and repaired in-commit before the wave (e0be61e4 exists
precisely to land "controls at freeze"). G is not yet caught by any instrument and rides into the wave as
committed bytes; it is the better attack target for w1's privacy triage.
