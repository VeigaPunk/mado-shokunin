# RevengerHyprlang — hyprlang 0.6.8 `device` special-category state machine (round 46, w1)

Seat: RevengerHyprlang (leaf, no dispatch). Target: reconstruct the exact state machine behind
`device` blocks in hyprlang 0.6.8 from the pinned source, and confirm the three murky cases
against the **host library** with a C++ probe.

Status: **complete**. 28/28 quotes verified (`quote-check.txt`), 49 config streams run
(55 receipts in `out/`), one reproducible **SIGSEGV** found in the parser.

## 0. What was read / what was run

| item | value |
|---|---|
| parser source | `.ufo/waves/round-46/fetch/hyprlang-config.cpp` (hyprwm/hyprlang v0.6.8 `src/config.cpp`, 1158 lines, sha256 `fa1b6898…e1de3e`) |
| consumer source | `.ufo/waves/round-46/fetch/Hyprland-ConfigManager.cpp` (Hyprland `efb50993`, sha256 `9db68cf4…5be62b`) |
| host library | `/usr/lib/libhyprlang.so.0.6.8` (`hyprlang 0.6.8-5`, soname `libhyprlang.so.2`) — **the same object the running compositor links** (`ldd /usr/bin/Hyprland`, receipt `versions.txt`) |
| probe | seat dir `probe.cpp` (registers `device` exactly as `ConfigManager.cpp:518-563`, then dumps every instance + `m_bSetByUser`), rebuilt by `run.sh` |
| host contact | none: no `hyprctl`, no compositor socket, no input injection, no package transaction; the probe only calls into an already-installed shared library in-process |
| tooling | nothing installed or updated: no package transaction, no `uv`/`npm`/cargo channel used; only the pre-existing `g++` 16.2.1, `gdb`, `python3` |

Confidence convention: **[S]** = read in pinned source, **[P]** = observed with the probe on the
host library, **[I]** = inference (stated as such).

## 1. State (what the parser actually carries)

```
impl->categories              std::vector<std::string>        // block-name stack, raw text
impl->currentSpecialCategory  SSpecialCategory*               // RAW pointer into instances
impl->currentSpecialKey       std::string
impl->specialCategories       std::vector<unique_ptr<SSpecialCategory>>  // instances, creation order
impl->specialCategoryDescriptors …->defaultValues             // mutable *during* parsing (see §3.3)
```

For Hyprland `device`: descriptor `name="device"`, `key="name"`, 47 field defaults, **no**
`name` entry among the defaults (`ConfigManager.cpp:518-563`; `grep -c '"device", "name"'` → 0),
not anonymous, `ignoreMissing` unset. Values are read back by name only through
`getSpecialConfigValuePtr("device", field, deviceName)` (`ConfigManager.cpp:1117`), with the
global `input:*` fallback when the per-device value is not `m_bSetByUser` (`:1119`) **[S]**.

## 2. Transitions

### 2.1 Block open / close
* `X {` → the trimmed text minus `{` is pushed verbatim (`hyprlang-config.cpp:908`). So `device[` + `A] {` pushes the single string `device[A]`; the bracket is **not** interpreted here **[S]**.
* `}` → pop (`:893`). **Only** if the stack becomes empty are the two special fields reset (`:896-897`) **[S]**.
  A `}` that leaves a non-empty stack leaves `currentSpecialCategory`/`currentSpecialKey` untouched.
* Because the reset is tied to "stack empty", closing an inner block does not reset routing state;
  and a file that ends with an unclosed block keeps a live pointer (see §3.7).

### 2.2 Value line (`lhs = rhs`)
`valueName = join(categories, ':') + ':' + lhs`, then five stages in order **[S]**:

1. **Bracket pre-pass** (`:291-334`), runs whenever `valueName` contains both `[` and `]` with `[` before `]`:
   * `CATKEY` = text between the first `[` and the last `]` (`:296`);
   * `currentSpecialKey = CATKEY` (`:297`) — this is *assignment site 1*;
   * the bracket slice (with the key) is spliced out of `valueName`; the splice is purely positional, so `device[A]x:kb_layout` becomes `devicex:kb_layout` **[P: z22]** and a lone `[` is not a bracket line at all **[P: z21]**;
   * for the first descriptor with a non-empty key whose `name + ":"` prefixes the spliced name: scan **all** instances of that descriptor and take the **last** one whose key field equals `CATKEY` (`:311-315`, the loop has no `break`, `:318` only breaks the descriptor loop) → `overrideSpecialCat`;
   * if no instance matched, **create** one (`:322-332`): descriptor defaults, then the descriptor's key default is overwritten by `CATKEY` (`:326`) and the instance key is set to `CATKEY` (`:330`).
   This pre-pass **bypasses the first-key rule** — a bracket line can name a device out of thin air (§3.4).
2. **Global values** (`:337`): `impl->values` (e.g. `input:kb_layout`). Nothing under `device:` lives there **[S]**.
3. **Routing** (`:342-381`): `overrideSpecialCat` if the pre-pass set one; else `currentSpecialCategory` when `valueName` shares its name prefix; else scan instances by `name + ":"`, where
   * the **key field itself** is matched by the RHS *value* being assigned, and
   * every other field is matched by `currentSpecialKey`;
   * **first** matching instance wins (`break` at `:380`); `ignoreMissing` would swallow a miss (`:386-387`).
4. **Dynamic creation** (`:393-441`): if a descriptor with a non-empty key prefixes `valueName` and the remaining trunk is one of its defaults (or is the key itself), an instance is created with the key default `"0"` (`:411`), defaults applied, `VALUEIT` looked up, and `currentSpecialCategory` pointed at it (`:382`/`:416`). Then
   * anonymous categories get an auto key (`:421-432`), else
   * if the line being applied is **not** the key field → error `special category's first value must be the key…` (`:435`) and **return**; the instance stays, `currentSpecialCategory` points at it, the RHS is dropped;
   * if it **is** the key field → `currentSpecialKey = value` (`:438`) — *assignment site 2*.
5. **Miss** → `config option <X> does not exist.` (`:446-448`), and the handler stage runs (`:839-877`).

Then the type switch writes the value and sets `m_bSetByUser` (`:452-521`). `name` gets **no**
special case anywhere: it is an ordinary STR field, so a second `name =` is simply a second write.

### 2.3 Where the two special fields change

| event | `currentSpecialKey` | `currentSpecialCategory` |
|---|---|---|
| `device[X]:…` line | = X (`:297`) | unchanged by the pre-pass; set in stage 3/4 |
| `name = V` (stage 4 creation) | = V (`:438`) | = new instance (`:416`) |
| any routed field line | unchanged | = routed instance (`:382`/`:416`) |
| `}` that empties the stack | `""` (`:896`) | `nullptr` (`:897`) |
| `parseDynamic()` return | unchanged | `nullptr` (`:1060`/`:1066`) |
| `clearState()` at `parse()` | **unchanged** | **unchanged** (`:1070-1076`) |

### 2.4 The `device` block, end to end

| config | resulting instance name(s) | notes |
|---|---|---|
| `device { name = A` / `kb_layout = de }` | `A` | baseline, `kb_layout=de,set` **[P: c01]** |
| `device { kb_layout = de` / `kb_variant = intl }` | `0` | first line error, value dropped, second line lands **[P: c02]** |
| `device { name = A` / `kb_layout = de` / `name = B }` | `B` | rename in place, values kept, `A` gone **[P: c03]** |
| `device[X]:name = Y` | `Y` | **`X` never exists** **[P: c04]** |
| `device[X]:kb_layout = de` | `X` | no `name` needed **[P: c05, c13]** |
| two blocks `name = A` | one `A` | fields merge, last write wins **[P: c07, z24]** |
| `device[A]:name = B` then `device:kb_layout = de` | `B` **and** a second instance | the second carries the *poisoned* default name `A` **[P: z2, z3]** |

## 3. The three murky cases (asked) + four more that fell out

### 3.1 M1 — a block whose first key is not `name`
**Which device name results:** the descriptor's key default *at that moment*: `"0"` on a virgin
descriptor (`:411`), but any earlier bracket line has already emplaced its `CATKEY` into the
descriptor defaults (`:326`, `emplace` = first-wins, so `:411`'s `"0"` is a no-op) **[S+P]**.
**Do later keys land there:** **yes** — the error at `:435` returns *after*
`currentSpecialCategory = PCAT` (`:416`), so every following non-bracket field line in that block
routes to the phantom (`:348-353`) **[P: c02 → `kb_variant=intl,set` on `0`; z3 → `intl` on the poisoned `A`]**.
**The offending line's value is dropped** (`:435` returns before the type switch) **[P: z19** —
`enabled = 0` as the block's first line leaves `enabled=1,def`**]**. A later `name = X` line
re-keys that same phantom to `X`, rescuing the block but not the lost value **[P: z19, c24]**.
The parse error is recorded once (`throwAllErrors` off keeps only the first) and parsing continues
(`:982-986` in `parseFile`, `:1034-1038` in `parseRawStream`) **[S+P: c15, c26]**.

**Operational reading:** such a block is a *live* device entry named `0` (or the poisoned name)
holding defaults plus the later fields; a live device is essentially never called `0`, so in the
round-46 C1 terms that block can never be `MATCHED` and the operator's settings on it are dead.

### 3.2 M2 — rename via a second `name =`
Same instance is re-keyed; the old name disappears; sibling values survive; no error **[P: c03
`[B]` with `kb_layout=de`]**. Two consequences:
* **duplicate keys** are reachable: `device { name = A }` + `device[B]:name = A` yields two
  instances both keyed `A` **[P: z7 `[A][A]`]**;
* duplicate keys resolve **inconsistently**: reads (`getSpecialConfigValuePtr`, `:1083-1101`, and
  `getConfigValueSafeDevice`, `ConfigManager.cpp:1115-1123`) take the **first** instance, while the
  bracket pre-pass **writes** to the **last** (`:311-315`). So `device[A]:kb_layout = fr` with two
  `A` instances writes an instance the compositor never reads **[P: z10, z8, z24]**.
  Non-bracket blocks (`name = A` then fields) route to the **first** (`:380` break) **[P: z24]**.

### 3.3 M3 — `device[X]:name = Y`
The pre-pass creates (or finds, by key `X`) the instance, then the ordinary STR write sets the key
field to `Y` → the device is named `Y` and `X` never exists **[P: c04 `[Y]`]**. If `X` already
existed it is **renamed**, values kept **[P: c08 `[B]` with `kb_layout=de`]**. `currentSpecialKey`
keeps the stale `X` (`:297`; the later name write does not touch it), so a following
non-bracket `device:<field>` line routes by `X`, not `Y`: it misses and creates a phantom when no
instance is keyed `X` **[P: z3]**, and it hits `X`'s instance while that instance is still keyed `X`
**[P: z9]**. In dynamic (`hyprctl keyword`) use the same routing survives across calls, because
`parseDynamic` clears only `currentSpecialCategory` **[P: z18 dyn → `device:kb_variant` lands on the
`K` created by the previous `device[K]:kb_layout`]**.

### 3.4 A bracket line is a device definition, not just a selector
`device[X]:field = v` and `device[X] { … }` create the device `X` with defaults + `v` and never
raise the first-key error (`:317-332` runs before the rule at `:435`) **[P: c05, c13]**.
`device[A] { name = B` / `kb_layout = de }` therefore produces **two** devices — `B` (defaults only,
because line 1 created and then renamed the `A` instance) and a fresh `A` (with `kb_layout`) **[P: c14 `[B][A]`]**.

### 3.5 `currentSpecialKey` is sticky across statements
It is assigned only at `:297` and `:438` and cleared only at `:896` **[S]**. Consequences: after a
bracket line, the following non-bracket field lines of that block (and of the rest of the file,
until the stack empties) route by that key, not by the block's `name` **[P: z9 — `sensitivity =
0.5` lands on the bracket-named instance with no error]**. This is what makes a "bracket then
block" pair behave like one device **[P: c06]**.

### 3.6 Descriptor defaults are parser state, not configuration
`addSpecialConfigValue` **inserts into the descriptor's default map** and `emplace` never
overwrites, so the key default for `device` is fixed by whichever code path touches it first: a
bracket line (`:326`, the first `CATKEY` ever seen) or the dynamic path (`:411`, `"0"`) **[S]**.
Every later instance created without a name therefore inherits that name. This is why the phantom
in z2/z3 is called `A` and not `0` **[P]**. `clearState()` does not undo it (`:1070-1076`).

### 3.7 A re-parse after an unclosed block **segfaults** the parser
`parseFile`/`parseRawStream` clear `categories` at EOF (`:998`, `:1052`) but leave
`currentSpecialCategory`/`currentSpecialKey` set (`:896-897` is the only reset), while
`clearState()` at the next `parse()` **erases the instance** (`:1075`) without clearing the pointer.
The next value line then dereferences freed memory (`:348`). Reproduced on the host library:
`device {` / `name = A` / `kb_layout = de` (no closing brace), then a second `parse()` →
`SIGSEGV`, `#2 Hyprlang::CConfig::configSetValueSafe` (`out/c28_backtrace.txt`, `out/c28_twice.txt`
→ `EXIT|139`) **[P]**. A closed block re-parses cleanly **[P: c01 twice]**.
Hyprland re-parses the same `CConfig` object on reload/verify (`ConfigManager.cpp:743`, `:757`
inside `reload()`, `:726`), so an unclosed block in the main config *or in a `source =` file*
followed by a reload reaches this crash **[S for the call chain, P for the crash, I for the exact
reload sequencing]**.

### 3.8 Other edges worth knowing
* Nested blocks make the path part of the name: `input { device { name = A } }` →
  `config option <input:device:name> does not exist.` **[P: c11]**; an unknown category `devices { … }` →
  `<devices:name>` **[P: c10]**; a nested `subcat {` inside a device block →
  `<device:subcat:kb_layout>` while the surrounding device state survives the inner `}` **[P: c25]**.
* `name =` with an empty RHS re-keys the device to the empty string, which exists and matches
  nothing **[P: c12, z23]**; `device[]:kb_layout = de` does the same **[P: z20]**.
* Names with spaces are preserved verbatim (`name = Elan Touchpad`) **[P: c22]**.
* `device[A]:name = A` is a no-op rename **[P: c21]**; `device[0]:name = A` leaves no `0`
  behind **[P: c19]**.

### 3.9 FLOAT/INT literal acceptance (asked by the round's C1 model as F1) — the parser is `std::stof`
`scroll_factor`/`sensitivity`/… are FLOAT: the value goes through `VALUEIT->second.setFrom(std::stof(value))`
(`hyprlang-config.cpp:467`), so whatever `std::stof` accepts is accepted and the field ends `m_bSetByUser`;
a throw becomes `failed parsing a float: stof` and the field keeps its default. Measured on the host
library, one fresh `CConfig` per literal (`out/floats.txt`) **[P]**:

| literal | `scroll_factor` stored | error |
|---|---|---|
| `0.5`, `100`, `101`, `-5`, `1e2`, `+3`, `.5`, `5.`, `1e3` | 0.5, 100, 101, -5, 100, 3, 0.5, 5, 1000 | none |
| `inf`, `-inf`, `infinity`, `NAN`, `nan` | `inf`, `-inf`, `inf`, `nan`, `nan` | none |
| `0x10`, `0X1p4` (hex floats) | 16, 16 | none |
| `` (empty), `1e40`, `1e-45`, `true` | -1 (default, not set) | `failed parsing a float: stof` |

INT fields go through `configStringToInt` instead: decimals/exponents/`+3`/`.`/`inf`/`nan`/`1e40` are all
rejected (`cannot parse "…" as an int.`), while `0x10` → 16 and `true`/`on`/`yes` → 1, `false`/`off`/`no` → 0 **[P: same receipt]**.

**Why it matters for the plane, not just the parser:** the clamp that produces what the dump shows is
`std::clamp(getDeviceFloat(devname, "scroll_factor", "input:scroll_factor"), 0.F, 100.F)`
(`InputManager.cpp:1380`), applied only when `deviceConfigExplicitlySet` — and `hyprctl devices -j` prints
`m->m_scrollFactor.value_or(-1)` with `{:.2f}` (`HyprCtl.cpp:770`, `:773`). Therefore **[S + derived]**:
`101`→`100.00`, `1e3`→`100.00`, `-5`→`0.00`, `inf`→`100.00`, `-inf`→`0.00`, unset→`-1.00`, but
`nan` passes `std::clamp` unchanged (both comparisons are false for NaN) and formats as the bare token
`nan` — i.e. `scroll_factor = nan` makes the JSON dump **non-JSON** **[I]**. A tool that must parse one
`hyprctl devices -j` dump cannot assume its input is valid JSON.

## 4. What a config→state reader must reproduce (implications for round-46 C1/C2)

Marked **[I]**: these follow from §2-§3 but are statements about tooling, not about hyprlang.

1. A `device { … }` block is only "for" its `name` if `name` is the block's **first effective
   key**. Otherwise the settings live on a phantom (`0`, or the first bracket key ever seen) that
   matches no real device, and the first line's value is lost. Such a block is a config error, not
   a stale device: C1's `NO_SUCH_DEVICE`/`STALE_BLOCK` distinction should not be decided by mere
   text presence of `name =` inside the block.
2. `device[<name>]:<field>` lines are device definitions; a file with only bracket lines has live
   device entries.
3. Repeated blocks with the same effective name merge; later fields overwrite earlier ones, so a
   per-field "last write wins" model is correct — but see (4).
4. With duplicate effective names (reachable via `device[B]:name = A`), the compositor reads the
   **first** instance and bracket writes go to the **last**: a config can look set and be inert.
5. The effective name of a block is its **last** `name =` value, not the first, and not the
   block's bracket key.
6. `input { device { … } }` is never a device block.
7. Since parsing does not abort on error, one malformed line does not invalidate the rest of the
   file; a whole-block "ignore" rule would misreport.
8. Literal handling is asymmetric and must be modeled as measured, not as "numeric": FLOAT accepts
   `inf`/`nan`/hex and rejects overflow/underflow, INT accepts hex and the on/off words but no
   exponent or sign prefix; and a `nan` scroll_factor reaches the JSON dump as a bare `nan` token
   (§3.9).

## 5. Evidence index (all under `.ufo/waves/round-46/w1/RevengerHyprlang/`)

| receipt | contents |
|---|---|
| `probe.cpp`, `run.sh` | probe source (Hyprland-identical `device` registration) + rebuild/run driver |
| `cases/*.conf` | 49 config streams (c01-c28, z1-z14, z18-z24) |
| `out/*.txt` | per-case probe output: `ERR`, `NKEYS`, `KEYS`, per-instance field values with `set`/`def`, `EXISTS` for `0`/`""`/`A`/`B`/`Lexa`; `z18_dyn.txt` (two `parseDynamic` calls), `c01_twice.txt`, `c28_twice.txt` (`EXIT|139`), `c28_backtrace.txt` (gdb `bt`) |
| `quotes.txt`, `verify-quotes.py`, `quote-check.txt` | 28 located quotes (≤25 words), verified verbatim against the pins: `-- 28/28 quotes verified` |
| `out/floats.txt` | FLOAT/INT literal matrix (21 literals × 2 fields) measured on the host library: what `std::stof`/`configStringToInt` accept, store and reject |
| `out/perturb.txt` | `MALLOC_PERTURB_=42` re-runs of c01/z11/z12: byte-identical, i.e. the stored key/value strings are not freed-heap pointers |
| `versions.txt` | host Hyprland/hyprlang versions, `ldd` of the probe and of `/usr/bin/Hyprland` (same `libhyprlang.so.2`), pin sha256 vs the wave's `receipts/fetch-sha256.txt` |

## 6. Limits

* The probe is not the compositor: it registers `device` with the 47 fields and defaults copied
  from `ConfigManager.cpp:518-563` (`STRVAL_EMPTY` written as `""`, same value), and feeds a raw
  stream (`pathIsStream`) instead of the on-disk file. Everything above is about hyprlang's state
  machine, not about Hyprland's later use of it (InputManager/device application was not traced).
* `CConfigValue::setFrom`/`defaultFrom` are not in the pinned source (they live in another TU of
  the library); their behaviour is only used through observable effects. No dangling-string
  behaviour was observed (`MALLOC_PERTURB_=42` left three re-runs byte-identical, `out/perturb.txt`).
* Crash reachability in a live session (reload after an unclosed block) is the reload call chain
  plus in-process library behaviour; no compositor was reloaded or touched to confirm it
  end-to-end, by host guard.
