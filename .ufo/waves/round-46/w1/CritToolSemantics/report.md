# CritToolSemantics — C1 contract vs the pins (round 46, w1)

Seat: critic on the C1 contract (`l1-draft/mado-devices.py` docstring) against
`.ufo/waves/round-46/fetch/` (Hyprland 0.56.2 @ efb50993, hyprlang 0.6.8) and the host's own
Hyprland 0.56.2 headers. Leaf seat; no subagent, no background job, no compositor write; host
only read (`hyprctl version`).

**Bottom line.** The *output* contract is right on every construct I could exercise: a 12-config
differential against the real hyprlang parser agrees on 10; of the two disagreements one is F1 and
one is an artifact of my oracle (it printed the raw `[[EMPTY]]` where Hyprland's own
`getDeviceString` returns `""` — `Hyprland-ConfigManager.cpp:1163` — so the tool was right). Two docstring sentences are **false** against the pins (`kb_file`; the virtual
keyboard rationale), one model rule is **wrong** (the `#hyprlang` directive trigger), one state
rule is **missing** (`source =` inside a block), and two bullets **under-describe** their own
code. None of that is visible to clause g (it judges the tool with the reference — declared
residual) and none is covered by controls V01–V20. The frozen predicate is *not* threatened:
fixtures and the nonce generator contain no `source` and no `#hyprlangX if` (checked:
`c1-r46-fixtures.json` matches only `# hyprlang if`/`# hyprlang endif`; `gen_case()` at
`c1-r46-devices.py:211` emits only those forms), and the F3 fix is docstring-only, so the
proposed changes move no frozen expectation. The fixtures do use `kb_file` (84 occurrences) — as a
name for the `kb_file=<set|->` field, never as a keymap-source case.

## What I ran (receipts in `w1/CritToolSemantics/receipts/`)

| # | Receipt | What it establishes |
|---|---------|---------------------|
| 1 | `hx.out`, `h2.out`, `h3.out`, `h5.out` (+ `*.cpp`) | the pinned hyprlang parser run directly on the host's `libhyprlang.so` 0.6.8 (`CConfig` stream, `device` special category, the real `input:kb_*` defaults) |
| 2 | `eff2-source-in-block.out`, `eff2-source-top.out` | a `source =` inside a `device` block: the sourced file inherits the block and **clears the stack at its EOF**, silently inerting the rest of the block |
| 3 | `differential.out` | 12 configs: reference tool vs the hyprlang oracle; 10 agree; the 2 disagreements are F1 (c5) and an oracle artifact on `[[EMPTY]]` (c11: the oracle printed the raw sentinel, Hyprland maps it to `""` at `ConfigManager.cpp:1163` — the tool is right) |
| 4 | `tool-c5-hyprlangfoo-if.out`, `tool-src-in-block.out` | end-to-end tool output on the two counterexample configs |
| 5 | `verify_quotes.out` | every quote in this report located by `grep -n` in the pins (no typed locators) |

Build (host, read-only): `g++ -std=c++23 -O0 -o hx hx.cpp -lhyprlang`; `hyprctl version` →
`Hyprland 0.56.2 … at commit efb50993780079460b0cbed1363e2166a2de1d9f`. `STRVAL_EMPTY` pinned on
the host: `/usr/include/hyprland/src/macros.hpp:24` = `#define STRVAL_EMPTY "[[EMPTY]]"`.

## Sentence ledger

`S` supported by a pin · `W` wrong · `U` unpinned (or not decidable from the fetch set).

| Docstring sentence (abridged) | | Evidence |
|---|---|---|
| "applies keyboard config per device … reads the value of the `device` block whose name equals the keyboard's name when that block SETS the key, else the global `input:` option" | S | `Hyprland-ConfigManager.cpp:1119` `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`; `:1156` getDeviceString; harness `hx.out` t1 (block wins, else default) |
| "defaults 'us' for kb_layout and empty for the others" (ConfigValues.cpp) | S | `Hyprland-ConfigValues.cpp:271-276`; `Hyprland-ConfigManager.cpp:521-527` device defaults |
| "The keyboard stores those five names as its current rules **and compiles a keymap from them**" | **W** | `Hyprland-IKeyboard.cpp:66` stores the names *before* any compile; `:87` `if (!m_xkbFilePath.empty())` loads `kb_file` into `m_xkbKeymap`; `:98` then skips the compile-from-names. With a readable `kb_file` the keymap is the file's, the names are inert labels |
| "when the names do not compile, it resets the stored rules to layout 'us' with every other name empty" | S (but) | `Hyprland-IKeyboard.cpp:101-113` exactly `rules="" model="" variant="" options="" layout="us"`; the reset is only reached when **no** keymap exists, so a valid `kb_file` suppresses it (see F3) |
| "`hyprctl devices -j` prints the stored rules of every keyboard (rules, model, layout, variant, options)" | S | `Hyprland-HyprCtl.cpp:780` (no filter, `m_enabled` irrelevant), `:788-792` field order |
| "for every pointer `scrollFactor`: the device block's scroll_factor clamped 0..100 when that block sets it, else -1, two decimals" | S | `Hyprland-InputManager.cpp:1379-1382`, `:1380` `0.F, 100.F`; `Hyprland-HyprCtl.cpp:770,773`; differential c9 (`150→100.00`, `-5→0.00`, both AGREE) |
| "the global `input:scroll_factor` never reaches that field" | S | only `m_scrollFactor` is printed (`HyprCtl.cpp:773`); it is written only at `InputManager.cpp:1380/1382` |
| "A virtual keyboard … takes the keymap its client sends and ignores later rule changes, so its printed rules do not witness its keymap" | **W** (rationale; verdict sound) | `InputManager.cpp:1195` applies config **at creation**; `Hyprland-VirtualKeyboard.cpp:41` sets `m_keymapOverridden = true` only on the client keymap event; `IKeyboard.cpp:61` thereafter. Before that event rule changes *do* apply, and if no keymap is ever sent the printed rules witness the compiled keymap exactly. F4 |
| "Device names are the compositor's: lower-cased, space/newline/comma → `-`, `-N` for duplicates" | S | `Hyprland-MiscFunctions.cpp:777-786` (`:782` comma case), `Hyprland-InputManager.cpp:2119-2135` |
| "a `device` block whose name matches no device applies to nothing" | S | lookup is by stored `name` value (`hyprlang-config.cpp:1083-1097`), nothing else reads the category |
| "a DIFFER may come from a runtime `hyprctl keyword`, a config file not passed, or a `source =` line it does not follow" | U/incomplete | missing F1/F2 and "a per-line parse error leaves the block half-applied"; the list is not fatal to the verdict, only to the diagnosis |
| "joined with the next raw line … spaces and tabs before it are removed (a final such line is dropped)" | S | `hyprlang-config.cpp:44-63` (`MULTILINE_SPACE_CHARSET = " \t"`, join verbatim; EOF → `GETNEXTLINEFAILURE_BACKSLASH` so the line is never applied) |
| "a line matching `#[ \t]*hyprlang\b` … adds one to `unsupported`" | **W** | `hyprlang-config.cpp:568-598`: the trigger is `trim(comment).starts_with("hyprlang")` **plus** a token `if`/`endif`/`noerror` among args[1:]; `\b` misses `#hyprlangfoo if false` and `#hyprlangx if false`, both of which Hyprland honours (F1) |
| "a line starting with `#` is a comment" + comment cut with `##` pairs | S | `hyprlang-config.cpp:676-704`; harness `hx.out` t F (`name = a##b` → device `a#b`, tool AGREE in differential c7) |
| "stripped of spaces, tabs and carriage returns" then ASCII whitespace | U | hyprlang's `trim` is not in the fetch set (not in `hyprlang.hpp` either); measured on the host: it strips VT/FF too (`h5.out` `vt_directive`, `vt_rhs`) |
| "`}` pops … when it empties, the current device is forgotten; `… {` pushes; anything else is ignored" | S (approx.) | `hyprlang-config.cpp:888-899`; hyprlang *errors* on a stray `}` / garbage after `{` (does not push), which is outcome-equivalent; harness `h2.out` H (nested `input {` inside `device` does not disturb the device), J/L (one-line block does not open) |
| "the KEY is the stack and LHS joined with `:`; `[`…`]` is a BRACKET NAME cut out" | S | `hyprlang-config.cpp:291-330`; `hx.out` t3 (`device[kbd] {` → `kbd/kb_layout=fr`), differential c2 AGREE |
| "`device:name` with no current device selects device RHS; `device:F` with a current device sets F" | S | `hx.out` t1/t5; differential c1/c3 AGREE |
| "`device:F` with no current device … Hyprland reports 'special category's first value must be the key' and keeps reading the block into a device it names itself" | S (under-described) | `hyprlang-config.cpp:435`, `:438`; `hx.out` t2: the later `name = kbd` really *names* the anonymous category `kbd` (all keys default, `set=0`) and later keys in that block would land on it. Tool marks the block unsupported → NOT_COMPARED, no wrong verdict |
| "`name` (a rename) adds one to unsupported; other F are ignored" | U (under-describes code) | the code also poisons the rest of the block (`cur = False`); the pin renames the *same* category (`hx.out` t6: `b` gets the later key, `a` does not exist). Conservative, but the sentence should say "and every later `device:` line in that block" |
| "scroll_factor … std::stof as [regex] … no prefix leaves the key unset; inf/nan/hex … unsupported" | S (conservative) | measured `std::stof`: `1e-50`, `1e-40`, `5e39`, `abc` throw; `inf`, `nan`, `0x10`=16, `1.2.3`=1.2, `+.5`=0.5 (`h2.out`). A throw skips `setFrom`, so the key stays unset (`hyprlang-config.cpp:513` never runs) → expected `-1` — the tool instead counts `unsupported` for inf/hex/overflow, which is safe but loses a decidable case |
| "the stored string `[[EMPTY]]` reads as ''" | S | `macros.hpp:24`, `Hyprland-ConfigManager.cpp:1163` (`VAL == STRVAL_EMPTY`), `hx.out` t4 (literal stored) |
| "AGREE when all five equal; FALLBACK when the reported names are exactly layout 'us' and four empty names (the compositor's fallback after a keymap that does not compile)" | S for the tuple, W for the parenthetical | tuple `IKeyboard.cpp:109-113`; but F5: the tuple also appears whenever the *tool's expectation* is wrong (F1) and is *suppressed* when `kb_file` supplies the keymap (F3) |
| "MATCHED when its name equals the `name` of some element of any top-level list … or `belongsTo`" | S | `HyprCtl.cpp:748-860` lists `mice, keyboards, tablets, touch, switches`; `tabletPad.belongsTo.name` |

## The five probes

**P1 — when does `applyConfigToKeyboard` run for a virtual keyboard, relative to its keymap event?**
At creation, *before* the event. `newVirtualKeyboard` → `setupKeyboard` → `applyConfigToKeyboard(keeb)`
(`Hyprland-InputManager.cpp:1195`, `:1128`); the client keymap arrives later through
`setKeymap` on the protocol resource (`Hyprland-protocols-VirtualKeyboard.cpp:74-110`) and only
then sets `m_keymapOverridden` (`Hyprland-VirtualKeyboard.cpp:41`), after which `setKeymap`
returns at `Hyprland-IKeyboard.cpp:61` without touching `m_currentRules`.
Consequences: (a) a virtual keyboard's printed rules are the **config at creation**, not the
current file — once a keymap has been sent, a reload that changes `input:kb_layout` never updates
them (the equality guard at `Hyprland-InputManager.cpp:1271` re-enters `setKeymap`, which returns
at `:61`); (b) "ignores later rule
changes" holds only once a keymap was sent; (c) with no keymap sent, the printed rules *do*
witness the compiled keymap. The VIRTUAL verdict is still sound because the name is always
prefixed (`Hyprland-protocols-VirtualKeyboard.cpp:12`, `misc:name_vk_after_proc` only appends a
suffix).

**P2 — can a non-virtual keyboard print rules that differ from config after a reload?**
Yes, in four ways: (i) F1 (`#hyprlang<token> if` — the tool models a line Hyprland skipped);
(ii) F2 (`source =` inside a block — Hyprland clears the stack at the sourced file's EOF, the tool
keeps it); (iii) a runtime `hyprctl keyword` / `device[...]` (already declared); (iv) a `device`
block abandoned after a first-value error, whose earlier keys are dropped while later blocks
apply (`hx.out` t2/I). **Not** via a failed reload: `postConfigReload` applies unconditionally
(`Hyprland-ConfigManager.cpp:970-980`, `:977` is called before the error branch), and **not** via
stale `m_bSetByUser`: `clearState` erases every non-static special category on each parse
(`hyprlang-config.cpp:1070-1076`), so device blocks are rebuilt from the file.

**P3 — does `enabled = false` hide a keyboard from the dump?**
No. `devicesRequest` walks `g_pInputManager->m_keyboards` with no filter
(`Hyprland-HyprCtl.cpp:780`); `applyConfigToKeyboard` only stores `pKeyboard->m_enabled = ENABLED`
(`Hyprland-InputManager.cpp:1240`), and `disableAllKeyboards` only clears `m_active`
(`:1934-1942`). A disabled keyboard is still printed, still compared, and its block is still
MATCHED.

**P4 — does `kb_file` change what is printed?**
Not the printed names: `m_currentRules = rules` happens before the file load
(`IKeyboard.cpp:66`), so `hyprctl devices` prints the config names either way. It changes what
they *mean*: with a readable file the keymap is the file's (`:87-97`), and because `m_xkbKeymap` is
then non-null the reset at `:101-113` never runs — so a bogus layout is printed verbatim and
**never becomes FALLBACK**. This is F3.

**P5 — is FALLBACK exactly us + four empties?**
Yes as a tuple (`IKeyboard.cpp:109-113`: rules, model, variant, options = `""`, layout = `"us"`),
printed by `HyprCtl.cpp:788-792`. As a *cause* the label is over-claimed (F5).

## Counterexamples

### F1 (wrong model) — the directive trigger is a regex, not `parseComment`

`DIRECTIVE_RE = r"#[ \t]*hyprlang\b"` misses tokens that Hyprland accepts, because
`parseComment` only requires `starts_with("hyprlang")` and a later token `if`/`endif`/`noerror`
(`hyprlang-config.cpp:568-598`).

Receipt `h2.out`: `#hyprlangfoo if false` + `input:kb_layout = fr` → `global='us' set=0` (skipped);
same for `#hyprlangx if false` (`hx.out` t7) and for `#  hyprlangx  if  false` (`h2.out` E).
`h5.out`: a leading VT before `#hyprlang if false` also skips (hyprlang's `trim` strips VT/FF,
the tool's first strip is `" \t\r"`), while `#hyprlangx` **without** a keyword is inert
(`h2.out` C) — so the fix must be the token rule, not "starts with hyprlang".

End-to-end (`tool-c5-hyprlangfoo-if.out`, config `c5_hyprlangfoo_if.conf`, dump = what Hyprland
would print):

```
MADO_DEV_KEYBOARD: name="extra" block=no layout="fr" variant="" … differ=layout verdict=FALLBACK
MADO_DEV_BLOCK: name="kbd" keys=1 verdict=NO_SUCH_DEVICE
MADO_DEVICES: … fallback=1 … stale=1 unsupported=0 verdict=DIFFER   (exit 1)
```

The truth (`eff-c5.out`): the global stayed `us`, no device block was configured at all
(`devices:{}`) — `unsupported` should be ≥ 1 and the verdict `NOT_COMPARED`. One unrecognised
directive therefore yields a false DIFFER, a false FALLBACK and a false stale block.

### F2 (missing state rule) — `source =` inside a block clears the stack

Sourced files are parsed with `m_config->parseFile(value)` on the same `CConfig`
(`Hyprland-ConfigManager.cpp:1839`), and `parseFile` clears the category stack at its EOF
(`hyprlang-config.cpp:1004`, `:1052`). So a source *inside* a `device` block inherits the block
for its own lines and then empties the stack, silently inerting the remainder of the block.

Receipt `eff2-source-in-block.out`:
`device { name = kbd / source = sub.conf / kb_layout = fr }` with `sub.conf: kb_variant = intl`
→ `dev=kbd kb_layout='' set=0 kb_variant='intl' set=1` (no parse error).
The top-level variant is benign (`eff2-source-top.out`).

End-to-end (`tool-src-in-block.out`) against the truthful dump:

```
MADO_DEV_KEYBOARD: name="kbd" block=yes layout="fr" variant="" … differ=layout,variant verdict=DIFFER
```

Truth: `layout` falls back to `us` (AGREE), `variant` is `intl` (AGREE) — a false DIFFER with the
wrong differing names, and `unsupported=0`.

### F3 (wrong sentence) — `kb_file` makes AGREE silent about the keymap, and suppresses FALLBACK

`IKeyboard.cpp:87-99`: a readable `kb_file` is loaded and the names are never compiled. So
`device { name = X  kb_file = <valid>  kb_layout = us }` prints `layout "us"` (AGREE) while the
keyboard runs the file's keymap, and `kb_layout = zz` prints `zz` (AGREE) without any FALLBACK
although the name can never compile. The tool *does* print `kb_file=set`, but the headline ("does
each keyboard run the XKB names its config declares") and the FALLBACK parenthetical both claim
more than the join establishes. This also means the frozen census word `fallback_layout=us` is a
layout value, not a guarantee that any observed FALLBACK was a compile failure.

### F4 (wrong rationale) — the virtual-keyboard sentence

See P1. The verdict and the ordering are fine; the sentence explains the observation with the
wrong mechanism (the creation-time apply is what freezes the names) and overstates the case where
no keymap is ever sent.

### F5 (over-claimed diagnosis) — "printed us+empty = keymap failed to compile"

Three producers, one signature: the real reset (`IKeyboard.cpp:109-113`), a model divergence
(F1 above produced `FALLBACK` with a default-config keyboard), and a `kb_file` that suppresses the
reset (F3). Keep the tuple test, drop the identity.

### F6/F7 (under-described bullets) — rename poisoning; strip charset

`parse_config` sets `cur = False` after a `device:F … name` line, so every later `device:` line in
that block is `unsupported`; the docstring bullet says only that the `name` line does. And the
first strip is `" \t\r"` while hyprlang's `trim` also eats VT/FF (`h5.out`).

## What I did not find

- No divergence on 10/12 differential configs (the 11th is F1; the 12th is my oracle's raw
  `[[EMPTY]]` print, not a tool defect): flat and block `input` globals, `device[k] { }`
  and `device[k]:key`, two blocks with the same name, nesting, CRLF, `##`, `kb_model`/`kb_rules`,
  scroll clamp both ends, comments after `{`/values, `[[EMPTY]]`, `-N` duplicate names.
- `enabled` does not filter the dump (P3).
- The clamp is exactly `0..100` and the printed precision exactly `2` (both pinned above).
- The device key **set** is pinned after all: `Hyprland-ConfigManager.cpp:518` registers
  `device`, then `:519-565` has exactly **47** `addSpecialConfigValue("device", …)` lines
  (`grep -c` = 47), matching the C2 census `device_keys=47`; `kb_layout` default `"us"` at `:523`,
  `scroll_factor` default `-1` at `:545` (the default is unreachable because of the
  `m_bSetByUser` fallback, which is what the tool models).
- No claim here contradicts the live host receipt (`9 AGREE, 1 VIRTUAL, OK`): `input.conf` has one
  `input` block and no `device` block, so F1–F4 are unreachable on this host today.

## Impacted axes

- **C1 operability (contract).** The docstring *is* the contract: F3/F4 are false sentences and
  F1/F2 are wrong state rules in the thing that defines the claim. Clauses a/s/f/i/r are untouched;
  clause g is blind to a contract error by construction (declared residual) — this report is that
  residual's non-author reading.
- **C2 coverage.** Rows S316-S325 quote the same pins; any sentence resting on
  `IKeyboard.cpp:87-99` (kb_file) or on the `setKeymap` sentence inherits F3, and any sentence
  claiming a FALLBACK means "compile failure" inherits F5. The census fields themselves
  (`default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100
  json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard`) are corroborated above, including
  `device_keys=47` (47 `addSpecialConfigValue("device", …)` lines, `Hyprland-ConfigManager.cpp:519-565`) and
  `virtual_prefix` (`Hyprland-protocols-VirtualKeyboard.cpp:12`).
- **Controls.** V01-V20 would need V21 (`kb_file` + non-compiling layout → AGREE, no FALLBACK),
  V22 (`#hyprlangx if` → NOT_COMPARED), V23 (`source` inside a block → NOT_COMPARED),
  V24 (virtual keyboard created, no keymap sent → names witness the keymap) to separate the
  repaired model from the current one.

## Smallest safe corrections (none moves a frozen expectation)

1. **F1** — in `parse_config`, strip the raw line with `WS` (not `" \t\r"`) and replace
   `DIRECTIVE_RE` with: comment text after `#`, whitespace-split; if token[0].startswith
   (`"hyprlang"`) and any token[1:] is exactly `if`/`endif`/`noerror` → `unsupported += 1`.
   (Fixtures match only `# hyprlang if`/`# hyprlang endif`; `gen_case()` emits only those.)
2. **F2** — when a line's KEY is `source` and the category stack is non-empty, `unsupported += 1`
   (the sourced file's EOF will clear Hyprland's stack; the tool cannot know what it set).
   Leave top-level `source` as today (marking it unsupported would make every real config
   NOT_COMPARED).
3. **F3** — qualify the headline and the AGREE/FALLBACK sentences: the five names are printed
   from `m_currentRules` regardless; with `kb_file=set` and readable, the keymap is the file's and
   a non-compiling name set does not reset. No output change.
4. **F4** — rewrite to: config is applied at creation (before any keymap event); the client keymap
   then sets the override, so later rule changes are ignored; with no keymap sent the printed
   rules witness the compiled keymap. Keep VIRTUAL first.
5. **F5** — keep the tuple test, drop "= keymap failed to compile" (or list all three producers).
6. **F6/F7** — say that a `name`-rename line also makes the rest of its block unsupported, that a
   later `name = RHS` after a first-value error really names the anonymous category, and use the
   full `WS` set for the leading strip.

Residual of this review: no live Hyprland run (compositor writes are out of scope), so F3/F4 are
read off the pins plus the same-version host headers, not observed on a running compositor.

Adjacent, *not mine* (predicate/implementation, not contract): seat `SentTool-3` reports clause i/r
holes in `quality/counters/c1-r46-devices.py` (no fake bin on the selftest PATH; absolute-path
`/usr/bin/hyprctl` possible; `--ro-bind / /` leaves AF_UNIX open) and a quadratic `cut_comment` in the
reference itself (`l1-draft/mado-devices.py:196-203`, 1 MiB line ≈ 8.9 s) — see
`.ufo/waves/round-46/w1/SentTool/findings.md` F1/F2/F7. F7 is in the same function cluster my F1 fix
touches (comment/directive handling), so a v2 reference should take both at once.
No interaction with F1-F7 above: my model fixes (1, 2) change only `unsupported` counts in the
reference/tool, and the F3 fix is docstring-only, so neither can move a clause-r/i score.
