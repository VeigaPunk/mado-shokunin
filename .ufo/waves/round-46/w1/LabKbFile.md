# LabKbFile — `kb_file`: does the dump print the declared names?

Seat: `LabKbFile` (leaf, no dispatch). Seat directory: `.ufo/waves/round-46/w1/LabKbFile/` — every
`receipts/…` path below is relative to it. Round 46 w1, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, freeze
`8c5434c6` (base `b22ea56b`). Reviewed against the pins in `.ufo/waves/round-46/fetch/` (opened 2026-10-26).

## Verdict (short)

| hypothesis | verdict | precondition |
|---|---|---|
| 1. with a readable `kb_file` the dump still prints the declared names | **SUPPORTED** | only if the declared names compile; a readable file can skip the name compile entirely |
| 2. an unreadable `kb_file` falls back to the names | **SUPPORTED with a counterexample if stated unconditionally** | only if the declared names compile; otherwise the dump shows `us` + four empty names |

Both clauses are true for the same underlying reason, and that reason is sharper than either clause: **`kb_file`
changes not *what* is printed but *whether the printed names were ever attempted*.** `hyprctl devices -j` prints
`m_currentRules` (`Hyprland-HyprCtl.cpp:799-800`), which `setKeymap` assigns from the config at
`Hyprland-IKeyboard.cpp:66` — before any file work — and rewrites to `us`/empty only on the names-failure path
(`Hyprland-IKeyboard.cpp:107-113`). The file branch is guarded by `if (!m_xkbKeymap)` at
`Hyprland-IKeyboard.cpp:98`, so when the file compiles the name compile is **never attempted**, and even an
invalid declared layout survives verbatim into the dump.

C1's handling (`kb_file=set`, compare the five names) is **mechanically right and semantically under-specified**:
presence is derived exactly as the compositor derives it, and the five names must not be transformed by
`kb_file` — but `kb_file=set` + `AGREE` is printable for three mutually exclusive real states (file applied and
its keymap live; file missing/unreadable; file readable but not a keymap) and even for a keyboard whose declared
names are not in effect. Smallest safe correction: one docstring sentence declaring the limitation (behaviour, fixtures and
expectations unchanged) — see §5.

## 1. The chain, with computed locators

1. `applyConfigToKeyboard` reads the six strings, `kb_file` included:
   `Hyprland-InputManager.cpp:1226` — `getDeviceString(devname, "kb_file", "input:kb_file")`.
2. Device-else-global precedence is "the block value only when the block set it":
   `Hyprland-ConfigManager.cpp:1119-1120` — `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` →
   `return m_config->getConfigValuePtr(fallback.c_str());`. A block value of `STRVAL_EMPTY` reads as `""`
   (`Hyprland-ConfigManager.cpp:1163` — `if (VAL == STRVAL_EMPTY)`), and `input:kb_file` is registered `STRVAL_EMPTY`
   (`Hyprland-ConfigValues.cpp:276`), so "set to empty" and "unset" both reach `setKeymap` as `""`.
3. `setKeymap` stores the declared names first: `Hyprland-IKeyboard.cpp:66` — `m_currentRules          = rules;`
   (after the overridden-keymap early return at `:61-62`).
4. Then, and only then, the file branch: `Hyprland-IKeyboard.cpp:87` — `if (!m_xkbFilePath.empty()) {`;
   `Hyprland-IKeyboard.cpp:88` — `auto path = absolutePath(m_xkbFilePath, Config::mgr()->currentConfigPath());`;
   `fopen`; on failure only a log line (`Hyprland-IKeyboard.cpp:91` — `Cannot open input:kb_file= file for
   reading`) and `m_xkbKeymap` stays null (it was released by `clearManuallyAllocd()` at `:82`).
5. Names path, guarded on a null keymap: `Hyprland-IKeyboard.cpp:98` — `if (!m_xkbKeymap)`;
   `Hyprland-IKeyboard.cpp:99` — `xkb_keymap_new_from_names2(CONTEXT, &XKBRULES, …)`.
6. Names-failure rewrite: `Hyprland-IKeyboard.cpp:107` — `memset(&XKBRULES, 0, sizeof(XKBRULES));` and
   `Hyprland-IKeyboard.cpp:113` — `m_currentRules.layout  = "us";` (rules/model/variant/options emptied on the
   preceding lines), then one more `new_from_names2` with the zeroed struct.
7. The dump prints exactly those stored names: `Hyprland-HyprCtl.cpp:800` —
   `escapeJSONStrings(k->m_currentRules.layout)` (rules at `:799`). Nothing else in the keyboard object is
   name-bearing; the single keymap-derived field is `Hyprland-HyprCtl.cpp:794` — `"active_keymap": "{}"`, fed
   from `getActiveLayout()` (`Hyprland-IKeyboard.cpp:306`), which returns
   `xkb_keymap_layout_get_name(KEYMAP, i)` (`Hyprland-IKeyboard.cpp:313`) — a *display* name, e.g. `German`.

Consequence for clause 1: `m_currentRules` is a copy of the config's strings, and the file branch never touches
it. Consequence for clause 2: an unreadable file lands on the names path with those same strings, so the dump
shows the declared names — **provided the names compile**.

## 2. Counterexamples (the strongest local ones)

**X1 — clause 1, readable is not sufficient.** `input { kb_layout = zz }` + `kb_file` pointing at a *readable
non-keymap* file. Probe (`receipts/probe-xkbcommon.txt`): `file junk.xkb: NULL keymap` for a 20-byte readable
file, so stage 4 yields null and stage 5 runs; probe `names zz: NULL keymap` shows the names do not compile, so
stage 6 fires and the dump prints `us` + empty — **not the declared `zz`**, although the file was readable. The
dump's names therefore depend on whether the *declared names* compile; readability of the file is neither
necessary nor sufficient.

**X2 — clause 2, the unreadable file can fall back to `us`.** `input { kb_layout = zz; kb_file = ~/missing.xkb }`:
`fopen` fails (`Hyprland-IKeyboard.cpp:90-91`), the names `zz` fail (probe: `names zz: NULL keymap`), the rewrite
runs and the dump prints `us`/empty. Contract run C (`receipts/contract-kb-file-states.txt`):
`layout="zz" … kb_file=set differ=layout verdict=FALLBACK`, exit 1. So "falls back to the names" holds only under
the same precondition as clause 1.

**X3 — the masked config error (the case the contract cannot see).** `input { kb_layout = zz; kb_file =
~/good.xkb }` with a compiling file: stage 4 sets `m_xkbKeymap`, so the `:98` guard is false, `zz` is *never
compiled*, no error is raised, and the dump prints `layout="zz"` while the keyboard actually runs the file's
keymap (probe: a valid `de.xkb` compiles to layout name `German`). Contract run A:
`layout="zz" … kb_file=set differ=- verdict=AGREE … verdict=OK`, exit 0. The headline question of C1 ("does each
keyboard run the XKB names its config declares") is answered `yes` for a keyboard running something else.
`active_keymap` would carry the contradiction (`German` vs `zz`) but the contract does not read it.

**X4 — the silent-OK state the frozen fixture asserts.** Contract run B (`input { kb_layout = us; kb_file =
~/missing.xkb }`, dump `layout="us"`) prints `kb_file=set differ=- verdict=AGREE … verdict=OK`, exit 0 — the
same line run A prints, and the same line the frozen fixture `kb-file`
(`quality/counters/c1-r46-fixtures.json`) expects for a *global* `input:kb_file = ~/x.xkb`. The fixture is
consistent with the contract; it is also structurally unable to separate the four states, because a fixture is
config text + a dump (no filesystem).

Supporting evidence that the VIRTUAL branch of the contract is right, for contrast: a keyboard whose keymap was
overridden never receives new rules — `Hyprland-IKeyboard.cpp:61-62` returns *before* `:66`, and
`Hyprland-VirtualKeyboard.cpp:41` — `m_keymapOverridden = true;` is set when the client's keymap arrives. The
live host receipt (`.ufo/waves/round-46/receipts/live-devices-host-l1.txt`) shows the fcitx5 virtual keyboard
printing `br`/`compose:caps` while its keymap belongs to the IME.

## 3. `absolutePath()` — which directory a relative `kb_file` resolves against

`Hyprland-MiscFunctions.cpp:61` — `std::string absolutePath(const std::string& rawpath, const std::string&
currentPath) {`; `~` is replaced by `$HOME` (`:63-65`), an absolute path is returned untouched, and a bare
relative path is joined to the *directory of `currentPath`* (`Hyprland-MiscFunctions.cpp:68` —
`auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));`). No globbing, no `~user`, no XDG
expansion.

The base is `Config::mgr()->currentConfigPath()` (`Hyprland-IKeyboard.cpp:88`) = `m_configCurrentPath`
(`Hyprland-ConfigManager.cpp:2146`), and that variable holds the **main** config path at the time `setKeymap`
runs:

- `reload()` resets it to the main path before parsing (`Hyprland-ConfigManager.cpp:736` —
  `m_configCurrentPath = m_mainConfigPath;`), calls `m_config->parse()` (`Hyprland-ConfigManager.cpp:743`) and
  only then `postConfigReload(...)` (`Hyprland-ConfigManager.cpp:750`).
- A `source =` file is parsed with the variable temporarily set to that file and restored straight after
  (`Hyprland-ConfigManager.cpp:1838` — `m_configCurrentPath          = value;`, `:1840` —
  `= configCurrentPathBackup;`).
- The apply happens *after* the parse returns: `Hyprland-ConfigManager.cpp:977` —
  `g_pInputManager->setKeyboardLayout();` → `CInputManager::setKeyboardLayout`
  (`Hyprland-InputManager.cpp:1206-1211`) → `applyConfigToKeyboard` → `setKeymap`
  (`Hyprland-InputManager.cpp:1286`). The hotplug call site is likewise outside any parse
  (`Hyprland-InputManager.cpp:1195` — `applyConfigToKeyboard(keeb);`).

So a relative `kb_file` declared inside a sourced sub-config resolves against the **main config file's
directory**, not the declaring file's: `source = conf/input.conf` containing `kb_file = kbmap.xkb` reads
`<maindir>/kbmap.xkb`. The contract cannot express this (it prints `kb_file=set` only), so the C2 entry is where
it has to be stated.

## 4. The `did not change` short-circuit

`Hyprland-InputManager.cpp:1273` — `FILEPATH == pKeyboard->m_xkbFilePath) {` closes a conjunction over
`numlock_by_default`, `repeat_delay`, `repeat_rate`, the five rule names and the raw `kb_file` string; on a match
`Hyprland-InputManager.cpp:1274` — `Not applying config to keyboard, it did not change.` — returns **before**
`Hyprland-InputManager.cpp:1285` — `pKeyboard->m_xkbFilePath = FILEPATH;` and `:1286` `setKeymap(…)`.

Three consequences that bear on the hypothesis and on the contract:

1. **No content awareness.** The comparison is on config strings, never on the resolved path or the file's
   contents. Editing the keymap behind an unchanged `kb_file =` line, or creating a file that was missing, does
   not recompile on `hyprctl reload`. The dump keeps printing the declared names in *every* state, so the tool's
   `AGREE` is stable — and therefore silent about all of them.
2. **A retry asymmetry.** After the `us`/empty rewrite the stored names differ from the config's (unless the
   config declared `us` + empties), so the next apply passes the check and retries; in the X4 shape (declared
   `us`, missing file) the stored names equal the config, the check passes on every later reload, and a file that
   appears afterwards is not picked up until some compared value changes. The two unreadable-file cases therefore
   do not converge.
3. **First apply always passes.** With `kb_file` set, `m_xkbFilePath` is empty on a fresh keyboard and the
   `FILEPATH ==` clause fails, so the `did not change` path cannot swallow the first apply.
   The comparison is also wrapped in a `try/catch` at `Hyprland-InputManager.cpp:1270-1280` (comment at
   `Hyprland-InputManager.cpp:1278` — `can be libc errors for null std::string`), i.e. on an exception the check is skipped and the apply proceeds.

## 5. Is the C1 contract's `kb_file` handling right?

Mechanics: **yes.**
- Presence: `l1-draft/mado-devices.py:341-353` takes the device block's `kb_file` when the block set it, else the
  global, else `""`, and reads the `[[EMPTY]]` marker as `""` — exactly `getConfigValueSafeDevice`
  (`Hyprland-ConfigManager.cpp:1119-1120`) plus `getDeviceString`'s `STRVAL_EMPTY` rule (`Hyprland-ConfigManager.cpp:1163`) against
  `Hyprland-ConfigValues.cpp:276`.
- Names: expected names are independent of `kb_file`, which is what the pins say (assignment at
  `Hyprland-IKeyboard.cpp:66` precedes the file branch at `:87`).
- FALLBACK: the ordering in `report()` (`l1-draft/mado-devices.py:360`, branches VIRTUAL `:373-374` → AGREE `:376-377` → FALLBACK `:379-380` → else DIFFER `:382-383`) means FALLBACK fires
  only when expected ≠ reported and reported = `us`/empty, so it can never fire for a config that itself declares
  `us`/empty. The docstring's parenthetical ("the compositor's fallback after a keymap that does not compile")
  matches `Hyprland-IKeyboard.cpp:107-113` — and the failed keymap may be the *file's* (X1) as well as the
  names', which the dump cannot distinguish and the contract does not claim to.

One pin gap worth handing to C2: the `[[EMPTY]]` marker the contract models (`l1-draft/mado-devices.py:107`)
is only half pinned. `hyprlang`'s carrier is `STRVAL_EMPTY` (`Hyprland-ConfigManager.cpp:1163`), whose `#define`
lives in a header that is **not** in `fetch/`; what the pins do show is the literal string used as a config
default (`Hyprland-ConfigValues.cpp:439`, `:481`). An entry that asserts "`[[EMPTY]]` is the empty sentinel"
therefore has no locator for the equality itself and should say so, or scope the sentence to the
`getDeviceString` mapping.

Semantics: **under-specified, and the docstring is where it should say so.** The docstring already concedes for
the virtual keyboard that "its printed rules do not witness its keymap"; `kb_file` deserves the same sentence,
because `kb_file=set … verdict=AGREE` covers those three realities, one of which (X3) makes the tool's
headline question vacuously true. This is a claim-meaning gap, not a predicate miss: the frozen fixtures and the
150 nonce cases compare the tool against a reference that behaves identically.

**Smallest safe correction** (docstring-only, no behaviour, no fixture, no expectation change): state that
`kb_file` is reported as presence only, that the five names are invariant to whether the file opened, compiled
or was applied, and that the only dump field derived from the keymap (`active_keymap`) is deliberately not read.
If the L1 wants more than that (e.g. a DIFFER when `kb_file=set` and `active_keymap` contradicts the declared
layout), it is a behaviour change and therefore a **v2 re-registration under the registration's "a hole wave w1
finds before any data commit" rule** — not a w1 edit of a frozen artifact. My recommendation: keep C1 frozen;
carry the sentence into the docstring only if a v2 freeze happens anyway, and put the facts in C2's entry either
way.

## 6. Impacted axes

- **C1 (operability).** Contract sound, meaning narrowed: `kb_file=set` is informational, and `AGREE` cannot
  witness that a `kb_file` was applied. No PRED-relevant defect found (nothing here makes the tool disagree with
  the pinned reference); the residual is a one-line docstring limitation.
- **C2 (coverage).** The entry must state three facts the pins decide: (a) the declared names are stored before
  the file branch, so the dump prints config, not keymap; (b) a relative `kb_file` resolves against the **main**
  config file's directory, not the declaring file's; (c) with an unchanged config, `hyprctl reload` recompiles
  nothing, so an edited or newly-created keymap file is not picked up. And one unknown the entry should not
  overclaim: the dump distinguishes a compiling `kb_file` from a failed one only through `active_keymap`'s
  display name, and only when that name differs from the declared layout.
- **Lesson / session gate.** Mineable mistake: "symptom absent because the step was never attempted" — the
  `if (!m_xkbKeymap)` guard turns a config error into silence, which is the same class of trap as the virtual
  keyboard's frozen rules. Round-45 closure D2 territory (a gate rule for a prose claim) is not needed here.
- **Live evidence gap.** The host config has no `device` block and no `kb_file`
  (`receipts/live-devices-host-l1.txt`: every row `kb_file=-`), so the kb_file branch is exercised only by
  fixtures and the reference selftest. Any claim text implying live coverage of it would be false.

## 7. Receipts, tooling, scratch

- `receipts/quotes-verified.txt` — 41 quotes checked by `verify-quotes.py` (fragment must occur on the cited
  line, ≤ 25 words; longest fragment 10 words), `MADO_QUOTES: total=41 failed=0`, exit 0. Locators are the script's
  computed line numbers.
- `receipts/probe-xkbcommon.txt` — local `libxkbcommon` 1.13.2 probe (gcc 16, `gcc -dumpversion`): `names zz: NULL keymap`,
  `names us: layouts=1 name[0]=English (US)`, `file good.xkb: … English (US)`, `file junk.xkb: NULL keymap`,
  `de: layout name = German`, `us(q): NULL`, `file de.xkb: layout name = German`, plus sha256 of the three
  probe keymap files (all ≤ 37 KB). Pure computation: no compositor, no socket, no Wayland client, no input
  injection; `pacman` untouched.
- `receipts/contract-kb-file-states.txt` — the three contract runs (A/X3, B/X4, C/X2) against
  `l1-draft/mado-devices.py` sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b`, which
  matches the tool hash in `receipts/live-devices-host-l1.txt`. Read-only (file/stdin in, stdout out).
- Tooling installed: none. Scratch `/fast/scratch/hyaku/mado-r46/LabKbFile/` removed before finishing; no
  clone or fixture repo was created (no git mutation anywhere).
