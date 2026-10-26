# LabVirtualRules — round 46 w1: what a virtual keyboard prints as its rules

Hypothesis under test: *a virtual keyboard's printed rules are the config names at its creation and never change
after its client's keymap arrives.*

**Verdict: supported, with two carve-outs that falsify the literal wording.** `hyprctl devices -j` prints
`IKeyboard::m_currentRules` for every keyboard (fetch/Hyprland-HyprCtl.cpp:788-792, 799-800). For a virtual keyboard
those five names are written only by `setKeymap` at creation, from the resolved config; the client's keymap
never reaches them, and no reload or `keyword` re-writes them. But what is stored is "the names set at creation", not
always "the config names": when the config's names do not compile, creation stores layout `us` with four empty names
(test T1); and the freeze starts when the client's keymap *compiles*, not when it arrives (test T2). Neither
carve-out changes the tool's verdict, because VIRTUAL is decided before any comparison (l1-draft/mado-devices.py:373).

Evidence paths are `fetch/<file>` under mado-shokunin/.ufo/waves/round-46/ (read-only pins; hashes receipts/proof-greps.txt)
plus one extra fetch, receipts/IKeyboard.hpp (URL and sha256 in receipts/fetch-extra.txt). Every quote below is
listed with its line in receipts/citations.tsv and checked by receipts/verify_citations.py
(output receipts/citations-check.txt: 42 rows, 42 pass).

## 1. Order of events

1. **Client creates the object.** `CVirtualKeyboardProtocol::onCreateKeeb` (fetch/Hyprland-protocols-VirtualKeyboard.cpp:164)
   constructs `CVirtualKeyboardV1Resource` — its name is assigned in the constructor (:110) — and emits `newKeyboard`
   (:176).
2. **InputManager adopts it.** The listener installed at fetch/Hyprland-InputManager.cpp:89 calls `newVirtualKeyboard`
   (:1127), which builds `CVirtualKeyboard` (:1128). Its constructor installs the keymap listener
   (fetch/Hyprland-VirtualKeyboard.cpp:37-45). `setupKeyboard` (:1130) then calls `applyConfigToKeyboard` (:1195).
3. **Creation applies the config.** `applyConfigToKeyboard` resolves the five `kb_*` names for the device and calls
   `setKeymap` (:1286). `m_keymapOverridden` is still false (default, receipts/IKeyboard.hpp:94), so the guard at
   fetch/Hyprland-IKeyboard.cpp:61 does not fire and the config names are stored (:66). The guard immediately before
   that call (:1271-1276) cannot short-circuit a fresh keyboard: it compares the config against the object's fields,
   and a fresh object has `m_repeatRate = 0`, `m_repeatDelay = 0`, `m_numlockOn = -1`
   (receipts/IKeyboard.hpp:121-123) while the config defaults are repeat 25/600 and numlock false
   (fetch/Hyprland-ConfigValues.cpp:277-280). The first application is therefore unconditional.
4. **Later the client's keymap arrives.** The `set_keymap` request handler (fetch/Hyprland-protocols-VirtualKeyboard.cpp:74-105)
   compiles the client's keymap string. If compilation fails it returns without emitting anything (:94-99). On
   success it emits the keymap event (:101) and sets `m_hasKeymap` (:104). The listener refs that keymap into
   `m_xkbKeymap`, sets `m_keymapOverridden = true` (fetch/Hyprland-VirtualKeyboard.cpp:40-41) and rebuilds the
   translation state and keymap fds (:42-44). **Nothing in this path touches `m_currentRules`.**
5. **The dump prints the stored names.** `hyprctl devices -j` prints `m_currentRules` (fetch/Hyprland-HyprCtl.cpp:788-792),
   while `active_layout_index`/`active_keymap` come from the keymap in use (:793-794; `getActiveLayout` reads
   `m_xkbKeymap`, fetch/Hyprland-IKeyboard.cpp:307). So the two halves of the same JSON object can disagree by
   design: rules = creation config, active_keymap = client keymap.

The freeze is structural, not incidental. Across the whole pin set the only writes to `m_currentRules` are
fetch/Hyprland-IKeyboard.cpp:66 and :109-113, and both sit inside `setKeymap` behind the guard at :61
(receipts/proof-greps.txt). There is exactly one construction path (:1128), two `applyConfigToKeyboard` call sites
(fetch/Hyprland-InputManager.cpp:1195 setup, :1208 reload), and `m_keyboards.clear()` only in the destructor (:117).
Ordering is also safe: the resource exists before `newKeyboard` is emitted, and a Wayland client cannot send
`set_keymap` for an object it has not created, so the config keymap is always installed first.

## 2. What a reload does

`hyprctl reload` → `CConfigManager::postConfigReload` (fetch/Hyprland-ConfigManager.cpp:970) →
`setKeyboardLayout` (:977) → `applyConfigToKeyboard` for every keyboard (fetch/Hyprland-InputManager.cpp:1208).
`hyprctl keyword input:kb_*` and `device:*` take the same route (fetch/Hyprland-HyprCtl.cpp:1203-1204).

For a virtual keyboard whose client keymap compiled, there are only two outcomes:

- **Config unchanged since creation:** the guard at fetch/Hyprland-InputManager.cpp:1271-1276 logs "Not applying
  config to keyboard, it did not change." and returns; nothing changes.
- **Config changed:** the guard fails, fetch/Hyprland-InputManager.cpp:1282-1286 update the repeat rate/delay, numlock
  and `m_xkbFilePath` (:1285), then call `setKeymap`, which returns at fetch/Hyprland-IKeyboard.cpp:61-64
  ("Ignoring setKeymap: keymap is overridden"). Neither the stored names nor `m_xkbKeymap` change. Note the
  asymmetry: `m_xkbFilePath` *is* updated even though it can no longer influence the keymap.

No reload path re-creates the keyboard, so nothing recomputes the names. `switchxkblayout` only moves the effective
layout index (fetch/Hyprland-HyprCtl.cpp:1359-1381 via `updateModifiers`) and never the stored names.

Net: a reload of the input plane updates repeat/numlock/enabled/keybinds/tags/permissions and the stored kb_file, and
leaves a virtual keyboard's printed rules and keymap exactly as they were. A stale creation-time rule set therefore
survives arbitrarily many reloads — which is why the tool must not compare these five names at all.

## 3. Falsification tests

**T1 — uncompilable config at creation (strongest; falsifies "the config names").** If the creation-time names do not
compile, `setKeymap` overwrites what it just stored: layout `us`, four empty names
(fetch/Hyprland-IKeyboard.cpp:101-113). The dump then shows `us`/empty — not the config's names. For a physical
keyboard the tool calls this FALLBACK; for a virtual keyboard the verdict short-circuits to VIRTUAL
(l1-draft/mado-devices.py:373), so the difference is invisible in a run yet makes the entry's sentence false in
exactly the branch the entry already teaches for physical keyboards.

**T2 — a client keymap that does not compile (falsifies "after its client's keymap arrives").** The handler returns
before emitting (fetch/Hyprland-protocols-VirtualKeyboard.cpp:94-99), so `m_keymapOverridden` stays false
(receipts/IKeyboard.hpp:94) and a later reload with a changed config passes the guard and rewrites the stored names
(fetch/Hyprland-IKeyboard.cpp:61 → :66). The invariant is "after the client's keymap is installed", not "after it
arrives"; the reference docstring's absolute "sends and ignores later rule changes" (l1-draft/mado-devices.py:15) is
too strong for this branch. A client that keeps sending a broken keymap also never satisfies `m_hasKeymap`
(fetch/Hyprland-protocols-VirtualKeyboard.cpp:104), so its key events are rejected too — a state the dump cannot
show either.

**T3 — object lifetime (bounds "never").** Destroy and re-create the virtual keyboard (an input method restart) and
the new object resolves the config again at its own creation. The freeze is per device object, not per name.

**T4 — ordering (not falsified).** Could the keymap event precede the construction-time `setKeymap`? No: the
resource and its name exist before `newKeyboard` is emitted (fetch/Hyprland-protocols-VirtualKeyboard.cpp:110, :176),
the listener is installed in the constructor, and the client's request cannot be sent before the object exists.

## 4. Live evidence (consistent, not discriminating)

Projected fields of the one virtual keyboard on this host (`hyprctl devices -j`, receipts/live-vk.json):

```
name=hl-virtual-keyboard-fcitx5 rules="" model="" layout="br" variant="" options="compose:caps"
active_layout_index=0 active_keymap="Portuguese (Brazil)"
```

That is the same line as the lane's own receipt receipts/live-devices-host-l1.txt:14 (`verdict=VIRTUAL`). It is
consistent with the hypothesis but does not discriminate it: fcitx5's own keymap also resolves to a Brazilian layout
name, and the compositor's DEBUG keymap lines are not in this session's log (receipts/log-probe.txt: 0 hits for
"provided keymap", "Ignoring setKeymap", "VKeyboard" in 1185 lines). The freeze is established by the code trace, not
by the dump; a discriminating live test would need a client whose keymap differs from the config, i.e. an input
source I am not allowed to inject.

## 5. Impacted axes and the smallest safe correction

- **C1 operability — not affected.** VIRTUAL is tested before any comparison (l1-draft/mado-devices.py:373-375), so
  T1, T2 and T3 can never turn into a false AGREE, DIFFER or FALLBACK. One reading hazard, not a defect: the
  MADO_DEV_KEYBOARD line prints the *expected* names (l1-draft/mado-devices.py:387), as the docstring states, so
  `layout="br"` on the virtual line of receipts/live-devices-host-l1.txt:14 is the tool's expectation, not the dump's
  value. The docstring's VIRTUAL description (l1-draft/mado-devices.py:15) is right for the reachable case and only
  absolute for T2.
- **C2 coverage — the sentence to fix.** l1-draft/entry.md:35 says the dump's rules "are the config's names at
  creation"; T1 and T2 show two branches where they are not. The frozen counter does not test this: its virtual
  clause only requires the anchor to occur near the word "virtual"
  (quality/counters/c2-r46-input-device-entry.py:374), so the wording passes regardless of meaning.
- **Smallest safe correction (wording only; no clause, fixture, verdict or anchor change).** In entry step 6:
  "…so the rules the dump prints are the names set at creation — the config's, or `us` with four empty names when the
  config's do not compile (Hyprland-IKeyboard.cpp:101-113)" and "when its client's keymap compiles
  (Hyprland-protocols-VirtualKeyboard.cpp:94-99) the keyboard marks the keymap overridden". In the reference
  docstring, "takes the keymap its client sends" → "takes the keymap its client compiles". build-pos.py's S322/S323
  anchors stay valid.

## 6. Bounds

No compositor was started, no input injected, no Wayland connection opened, no host service or config touched, no
`pacman`. Compositor reads used: `hyprctl devices -j` only. The reload behaviour is derived from code; I did not run
`hyprctl reload` (forbidden). Scratch under /fast/scratch/hyaku/mado-r46/LabVirtualRules was removed; the extra fetch
is kept as receipts/IKeyboard.hpp.

## Receipts

- receipts/citations.tsv — 42 file:line:quote rows; receipts/verify_citations.py — checker;
  receipts/citations-check.txt — 38 pass, 0 fail.
- receipts/proof-greps.txt — pin hashes, every `m_currentRules` write, the construction/call/clear sites, the
  `m_keymapOverridden` sites.
- receipts/fetch-extra.txt — IKeyboard.hpp URL, sha256 82e0bc9e…, size, reason.
- receipts/live-vk.json — one-line projection of the host's virtual keyboard (no serials, no titles).
- receipts/log-probe.txt — the zero-hit compositor-log probe.
