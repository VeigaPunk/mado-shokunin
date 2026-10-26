# CritPremise — round 46 w1: is the input-device ground new, and is the tool useful?

Seat `CritPremise`. Base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe` (all lane reads are `git show <base>:<path>`),
freeze `8c5434c6`. Every locator below is computed by `.ufo/waves/round-46/w1/CritPremise/critpremise-receipt.py`
and re-derived by its `verify` mode: **PASS, 0 failures, 16 quotes, 3 reference reruns, 2 probe lines**
(`.ufo/waves/round-46/w1/CritPremise/receipt.txt`). Quotes are <= 25 words and occur exactly once in the cited file.

**Verdict.** The premise holds, and holds strongest exactly where the registration puts it: the *resolution chain*
(device block first, global second, default third; compile fallback to `us`; virtual-keyboard override; scroll
factor -1/clamp; name normalisation) has no precursor in the lane. But two of the registration's *phrasings* are
wrong in ways a reader can check in one grep: the headline join is not new, and the repeat count is under-declared.
Neither blocks C1/C2 — both are prose defects the canonical judge can note without rejecting a claim.

## Axes

| axis | question | finding |
|---|---|---|
| A1 novelty precision (C2) | is the ground new? | new as a chain, **not** as an observation |
| A2 discriminative power (C1) | does the tool answer what the two read verbs cannot? | yes in principle (proved), **near-zero on this host** (0 device blocks) |
| A3 provenance accuracy | do the registration's counts match the bytes? | **no**: 5 duplicate-URL introductions declared as 2 |
| A4 cross-entry consistency | does it contradict held entries? | no — it completes `r15`'s deliberately left gap, but re-parses what `mado-options.py` already parses |
| A5 non-regression | does anything harm the round-45 plane? | no interaction found; disjoint files and counters |

## 1. Counterexample: the headline join is already in the lane

`corpus/knowledge/hyprctl-verification-layer.md:159` (base) performs the join C2 announces — config value →
per-keyboard printed keymap — and grades it:

> `agreement (keymap-level, stronger than the string getoption)` — receipt `held-join`

The record it is in is a table row mapping `kb_layout = br` (`L-IN:10`) to "`hyprctl -j devices` → 8 keyboard
nodes, all `active_keymap: Portuguese (Brazil)`, layout `br`". So "config → dump" is a held join at *whole-dump
granularity*. Two further precedents:

- `corpus/knowledge/config-health-report-r3.md:731` — `hyprctl -j devices > "$D/devices.json"` (receipt
  `held-dump-parse`): the lane already had a parser for the dump (counts keymaps, layouts, touch, mice).
- `corpus/knowledge/config-health-report-r3.md:413` — `power-button ×2, `hl-virtual-keyboard-fcitx5`), all keymap`
  (receipt `held-virtual-node`): the virtual-keyboard node, the name that C1's `VIRTUAL` class keys on, is already
  recorded by name; `SKILL.md:467` (`device lists are hotplug-sensitive`, receipt `held-hotplug`) already carries
  the hotplug/count lesson that `STALE_BLOCK` neighbours.

What is genuinely absent (0 rows on the URL, 0 mentions): `deviceConfigExists`, `scrollFactor`, `m_bSetByUser`,
hyprlang's `special category's first value must be the key`, and any `device {` / `device[` form outside
`tools/mado-options.py`. Receipt `C url-rows` shows `managers/input/InputManager.cpp`, `devices/IKeyboard.cpp`,
`devices/VirtualKeyboard.cpp`, `protocols/VirtualKeyboard.cpp` and `Configuring/Keywords.md` at **0** base rows.

So the defensible claim is: *the resolution chain*, not *the join*. The entry's `ground:` line currently says the
held neighbours are "point readings of `input:kb_layout`" — that is a mischaracterisation of
`verification-layer.md:159`, which is a live dump join, not a `getoption` reading.

## 2. Counterexample: on this host the tool's differential collapses to the two read verbs

From the claim's own live receipt, `.ufo/waves/round-46/receipts/live-devices-host-l1.txt:19`:

> `blocks=0 stale=0 unsupported=0` … `keyboards=10 agree=9 differ=0 fallback=0 virtual=1 mice=4 mice_differ=0 verdict=OK`

With `blocks=0`, every non-virtual keyboard's expected names *are* the global `input:kb_*` values, and all four
mice expect `-1.00`. Thirteen of the fourteen verdict rows are therefore reproducible by
`hyprctl getoption input:kb_layout` (the value) plus a field compare against the dump — i.e. by the two read verbs
the seat was given, with no config parser at all. The single non-trivial row is the virtual keyboard, and that row
is pre-recorded at `config-health-report-r3.md:413`.

That does not make the tool useless — it makes its value *prospective*, and it means the live run is not evidence
for the per-device branch. Proof that the branch is real and that no read verb replaces it:

| probe (receipt line) | result |
|---|---|
| `P getoption device[foo]:kb_layout -> no such option` | the per-device store is unreachable through `getoption` |
| `P getoption device:kb_layout -> no such option` | same for the flat form |
| `R A-block-sets-layout exit=1 … differ=1 … blocks=1 … verdict=DIFFER` | one `device { name = <kbd> kb_layout = de }` flips exactly one keyboard to DIFFER |
| `R B-stale-block exit=4 … stale=1 … verdict=STALE_BLOCK` | an unmatched block gives 4, 9 AGREE, no collateral DIFFER |
| `R C-omarchy-enabled-only exit=0 … blocks=1 … verdict=OK` | an `enabled`-only block: `block=yes`, no compared key, OK |

The structural reason is pinned: `Hyprland-HyprCtl.cpp:1667` resolves `getoption` with
`const auto VAR = Config::mgr()->getConfigValue(curitem);` (receipt `getoption-flat-lookup`), a flat registered-option
lookup, while the per-device path is a different call, `getDeviceString(devname, "kb_layout", "input:kb_layout")` at
`Hyprland-InputManager.cpp:1229` (receipt `device-store-separate`). The live `no such option` replies agree with the
code; this is the strongest *support* for C1's usefulness and should be stated in the entry, because it is the only
argument that survives the `blocks=0` objection.

`SKILL.md:562` (`getoption` is a config read, not applied per-device state, receipt `skill-getoption-limit`) already
says in words that `getoption` is not the applied per-device state — C2 supplies the mechanism behind that sentence,
which is a *completion*, not a contradiction.

## 3. Omarchy: the plane has a live producer, and the tool is blind to its keys

Nothing equivalent exists for the *join*: omarchy reads the plane with
`hyprctl devices -j | jq -r` (`omarchy-hw-touchpad:5`, receipt `omarchy-reader`; same shape in
`omarchy-hw-touchscreen`) but only prints a device *name* to feed a `device { }` block — no expectation, no
comparison, no layout/scroll semantics. So C1 is not duplicating an omarchy capability.

The sharper fact: omarchy **writes** the plane. `omarchy-toggle-touchpad:24` persists
`enabled = false\n}\n' "$device"` (receipt `omarchy-writer`) into
`~/.local/state/omarchy/toggles/hypr/touchpad-disabled.conf`, and `~/.config/hypr/hyprland.conf:23` sources
`~/.local/state/omarchy/toggles/hypr/*.conf`. A `device` block can therefore exist on this host at any time — but it
sets `enabled`, a key the dump does not print, and the tool compares only `kb_*` + `scroll_factor`. Probe C shows
the consequence: `block=yes`, `verdict=OK`. The plane's only live producer is outside the tool's comparison set, and
a persisted toggle conf whose device is absent (undock) would read as `STALE_BLOCK` 4 — a legitimate state graded as
a failure. Both are Limits prose, not tool defects.

## 4. Provenance: five duplicate-URL introductions, not two

`registration.md:47` says `The two cross-scope URL repeats` (receipt `declared-repeats`), naming S317 (with
S162/S303) and S320 (with S158/S307). The census rule is URL identity across scopes —
`W04 same URL across scopes` (`scripts/sources-census.sh:33`, receipt `w04-rule`), and warnings do not fail a clean
lane. Measured base rows per exact URL (receipt `C url-rows`):

| new row | URL | base rows |
|---|---|---|
| S317 | `config/legacy/ConfigManager.cpp` | 2 (S162, S303) |
| S318 | `config/values/ConfigValues.cpp` | **1 (S215)** — opens a new duplicate group |
| S320 | `debug/HyprCtl.cpp` | 3 (S018, S158, S307) |
| S321 | `helpers/MiscFunctions.cpp` | **1 (S182)** — opens a new duplicate group |
| S324 | `hyprlang/v0.6.8/src/config.cpp` | **1 (S173)** — opens a new duplicate group |

Five W04 lines, three of them previously non-duplicated URLs. The verdict is unaffected (W04 is a warning), but the
registration understates duplication by three, and the round-45 precedent it cites ("as in round 45") counts its own
repeats exactly.

## 5. Duplicate parser authority (A4)

`tools/mado-options.py:189` at base already declares `"device", "monitorv2", "windowrule", "layerrule", "plugin"`
(receipt `options-special-categories`) with the locator set `ConfigManager.cpp:518, 567, 591, 595, 626`, and its
self-fixture at `:1245` contains `name = some-mouse` (receipt `options-device-fixture`). It excludes device fields
from its model by design ("never global options"), so it does **not** resolve per-device expectations — C1's purpose
is additive. But the *parse* (keyed category, three spellings, `##`, continuation) is now implemented twice in
`tools/`, with no shared module. C2's S317 also supplies the first registry anchor for the very locator
`mado-options.py:186` has been citing unsourced since round 39 — that is a provenance gain worth recording.

## Impacted axes and the smallest safe corrections

1. **A1 — entry `ground:` line.** Replace "point readings of `input:kb_layout`" with the measured state: the
   devices join is held at whole-dump granularity (`hyprctl-verification-layer.md:159`) and the dump was already
   parsed and the virtual node already named (`config-health-report-r3.md:731`, `:413`, `SKILL.md:467`); new is the
   per-device resolution chain only. One paragraph, no claim change.
2. **A2 — entry Limits + live section.** State that with `blocks=0` the live run exercises the global-fallback
   branch only, so `verdict=OK` is not evidence for the per-device branch; cite the two `no such option` replies and
   `HyprCtl.cpp:1667` as the reason the join is not replaceable by a read verb; note that an `enabled`-only block
   (omarchy's own shape) is `block=yes` with nothing compared, and that a persisted toggle conf grades `STALE_BLOCK`.
3. **A3 — lesson errata (not the frozen registration).** Correct "two cross-scope URL repeats" to five, naming the
   three new groups (S318/S215, S321/S182, S324/S173); the census will show them anyway.
4. **A4 — one sentence in the entry** pointing at `mado-options.py:186-190` as the existing special-category
   authority and stating that C1 re-implements that parse deliberately (standalone tool), so the duplication is a
   recorded choice rather than an accident.

None of the four touches a frozen counter, fixture, control or the reference; all are inside the entry/lesson prose
that C2 owns, so they cost no re-registration.

## Limits of this review

- I did not run the C1/C2 counters, the controls, or `build-pos.py`; no scrub clone was made. Scored state is taken
  from the registration and the claims' own receipts.
- `R` lines were produced against a live `hyprctl devices -j` dump captured in scratch with synthetic configs; only
  the `MADO_DEVICES` counters are retained, never a device name, and the scratch dump is deleted.
- omarchy was read only (`bin/omarchy-hw-touchpad`, `bin/omarchy-toggle-touchpad`, version 3.8.3 tag `v3.8.4`); no
  omarchy command was executed.
- Host reads used: `hyprctl devices -j`, `hyprctl getoption` on two per-device forms plus one `input:kb_layout`
  control. No dispatch/keyword/reload, no
  package transaction, no compositor or session mutation, no Wayland client.
- Tooling: nothing installed; python3 stdlib only.

Receipt: `.ufo/waves/round-46/w1/CritPremise/receipt.txt` (37 lines) · generator/verifier:
`.ufo/waves/round-46/w1/CritPremise/critpremise-receipt.py` (`gen` / `verify --scratch <dir>`, `VERDICT: PASS`).
