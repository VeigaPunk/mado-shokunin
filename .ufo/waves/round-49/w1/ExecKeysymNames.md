# ExecKeysymNames — the `--keysym ARG` path and the `keysym:` header line (C1, round 49 w1)

Seat: `ExecKeysymNames`. Target: how `xkbcli how-to-type --keysym ARG` turns ARG into a keysym, and how
`xkb_keysym_get_name` picks the name in the header line `keysym: NAME (0x....)`. Everything below is grounded on
libxkbcommon 1.13.2 sources pinned in this seat dir (`receipts/pins.txt`) and on the pinned judge binary
`/usr/lib/xkbcommon/xkbcli-how-to-type` (sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`).

## Verdict (for the L1 freeze)

1. **Delivered:** `keysyms.py` (seat dir, 29,252 bytes, sha256 `beaacbf9fbd38b4196f1853094b1c8a184706752f1a025b37b9f762d21d1173c`), Python 3
   stdlib only, no process, no socket, no write. Exposes `parse_arg(ARG) -> keysym|None`, `get_name(keysym)`,
   `header_line(keysym)`, plus `derive/emit/verify` for the table. Drop it next to `tools/mado-keysym.py` and import it.
2. **The keysym header `xkbcommon-keysyms.h` is sufficient to derive both tables** — but only with the rule
   *canonical name = the **first** `#define XKB_KEY_<name>` line for that value, in file order*. With that rule the
   header reproduces the committed `src/ks_tables.h` `keysym_to_name[]` (2505 entries) and `name_to_keysym[]`
   (2638 names) **exactly, zero mismatches** (`receipts/summary.txt` line `D`, `receipts/rule-check.txt`).
   The tempting sibling rule fails loudly: taking the **last** define per value would change 120 of the 2505 names
   (`0xff20`: `Multi_key` first, `SunCompose` last; `0xff37`: `Codeinput` first, `Hangul_Codeinput` last; `0xff7e`:
   `ISO_Group_Shift` first, `SunAltGraph` last). Trailing comments are **not** the marker: only 1 of the 133 alias
   comments equals the canonical name (`#define XKB_KEY_Zen_Koho 0xff3d /* Multiple/All Candidate(s) */` prints
   `MultipleCandidate`). Count discipline: the pin has **2659 lines** matching `#define XKB_KEY_` but only
   **2638 real defines** — the other 21 sit inside the header's doc comment; anchor on
   `^\s*#\s*define\s+XKB_KEY_` and the number is 2638.
3. **The tool must NOT read the header at run time.** The derived table is embedded (zlib+base85, 19,248 chars).
   Proven with `/usr/include` masked to an empty tmpfs: `keysym: slash (0x002f)`, rc 0
   (`receipts/sandbox-no-header.txt` A-D). The counter sandbox therefore has to expose **only the keymap file**;
   the header pin is needed at *build* time, not at count time. Same receipt D runs with `--ro-bind / /` (whole
   filesystem read-only) and still prints, i.e. no write path exists.
4. **Judge parity: 10,613 ARG values, 0 differences** on first stdout line + exit status
   (`receipts/names-diff.txt`, recomputed in `receipts/summary.txt`: `rows=10613 ok=10613 fail=0`, of which
   `accept_rc0=10557 refuse_rc2=56`). That covers **every one of the 2638 names in the header**, every one of the
   2505 distinct values in decimal and in `0x` hex (5008 forms), 2900 nonce numerics and 65 hand-picked edge
   strings (10613 − 10548). Plus 344 rows under a second keymap (us) and 44 hostile shapes
   (`receipts/names-diff-edge.txt`, `rows=344 ok=344 fail=0`).
5. **Keymap independence:** the header line is printed before the keymap is walked, so it never depends on FILE.
   Proven: all 300 sampled ARGs give byte-identical line 1 under `--layout us` and `--layout br`.

## 1. What the judge does with ARG (tools/how-to-type.c:269-299)

With `--keysym` the character/code-point stage is skipped entirely, so ARG goes straight to
`xkb_keysym_from_name(argv[optind], XKB_KEYSYM_NO_FLAGS)` — `tools_how-to-type.c:286`, i.e. **case-sensitive**,
then to a base-10 `strtol` fallback — `tools_how-to-type.c:291` — gated by
`tools_how-to-type.c:292`. In `xkb_keysym_from_name` (`src_keysym.c:237`) the order is:

| # | form | rule | evidence |
|---|------|------|----------|
| a | **name** | exact `strcmp` against the 2638 names (`name_to_keysym[]`, perfect hash then `strcmp`). Case-sensitive: `SLASH`, `Slash` refused; `slash` → `keysym: slash (0x002f)`. | `names-diff.txt` rows `SLASH`,`Slash` = rc 2; `slash` rc 0 |
| b | `U` + 1..8 hex digits | `src_keysym.c:305`, then `src_keysym.c:309`: `0xff < v <= 0x10ffff` → `0x1000000+v`; otherwise `xkb_utf32_to_keysym(v)` (`src_keysym-utf.c:912`). No `+` after `U`: `U+0041` refused; lowercase `u0041` refused. `U000d` → `Return (0xff0d)`; `U0001` → `0x01000001`; `U0100` → `U0100`; `U110000`, `U00110000`, `U0000` refused. | `names-diff.txt` |
| c | `0x` + 1..8 hex digits | `src_keysym.c:330`: value used verbatim, refused when `v > 0x1fffffff` **or** `v == 0` (0 is `XKB_KEY_NoSymbol`, indistinguishable from "not found"). `0x0` refused, `0x1fffffff` → `keysym: 0x1fffffff (0x1fffffff)`. `0X2f` refused (uppercase `X` needs `XKB_KEYSYM_CASE_INSENSITIVE`). 9+ hex digits refused (`0x`+`f`*9). | `names-diff.txt`, `names-diff-edge.txt` |
| d | `XF86_` fallback | `src_keysym.c:338`: retry once with the underscore removed, then the whole function again. `XF86_ScreenSaver` → `XF86ScreenSaver (0x1008ff2d)`; `XF86_0x2f`, `XF86_` refused. | `names-diff.txt` |
| e | decimal | glibc `strtol(…, 10)`: optional C leading whitespace, optional `+`/`-`, then **all** remaining chars must be digits (`endp` must hit NUL), no `ERANGE`, and `0 < v <= 0x1fffffff`. Consequences: ` 47` and `+47` **accepted** (both `slash`); leading zeros are fine and **unbounded** (`0047`, `0000000047` → `slash`; the 8-digit cap is hex/`U` only); `-47`, `00`, `0`, `536870912`, `4294967296`, `9223372036854775807`, `9223372036854775808`, `9999999999999999999999`, `12abc`, `1.5` refused; `536870911` (`=XKB_KEYSYM_MAX`) accepted. | `names-diff.txt`, `handpicked.txt` |
| f | anything else | `ERROR: Failed to convert argument to keysym` + usage, rc 2 (`tools_how-to-type.c:293`). | `judge-refusal-sample.txt` |

Two traps the counter must not step into:

* Names `"0"`..`"9"` exist (`name_to_keysym` starts `{ 0x00000030, … } /* 0 */`), so the ARG `0` yields
  `keysym: 0 (0x0030)` — **not** keysym 0. Keysym value 0 is unreachable from ARG in any spelling (`0x0` is
  refused, `0` means the digit). Do not draw value 0 as a nonce. The judge's own `--help` text says so:
  *"Note that values '0' .. '9' are special: they are both names and numeric values"* (`receipts/invocation-form.txt`).
* ARG is consumed by `getopt_long` **before** the keysym parser: a dash-leading ARG never reaches it. `-h` and
  `--help` make the judge print usage **on stdout** and exit **0** (`receipts/handpicked.txt`); our tool refuses
  with rc 2. Every other dash form measured (`-v`, `-47`, `--keysym`, `-?`) ends at rc 2 with empty stdout, so
  they agree by accident — but `-h`/`--help` are outside the contract and must not be drawn. Keep the nonce
  alphabet free of a leading `-`.

**Invocation form matters for the judge itself:** `--keymap` is `optional_argument`
(`tools-how-to-type.c:171`), so only the `--keymap=FILE` spelling binds the file. Measured
(`receipts/invocation-form.txt`): `--keymap=FILE …` → `keysym: slash (0x002f)`, rc 0;
`--keymap FILE …` → `ERROR: missing positional parameter` + usage, rc 2 (FILE becomes a second positional).
The C1 counter must always emit `--keymap=FILE`.

## 2. The header line (tools/how-to-type.c:625)

`printf("keysym: %s (%#06"PRIx32")\n\n", name, keysym);` — line 1 is `keysym: <name> (0x<hex>)`, line 2 empty,
then `=== Direct access ===`, empty, then the column header. `keysyms.header_line()` reproduces line 1 only.

`name` comes from `xkb_keysym_get_name` (`src_keysym.c:70`), which is a three-way choice:

1. **explicit table hit** (`keysym_to_name[]`, 2505 values) → the canonical name. 133 header names print
   *another* name because they are aliases; `receipts/summary.txt` line `B` counts them and lists samples:
   `quoteright`→`apostrophe`, `quoteleft`→`grave`, `guillemetleft`→`guillemotleft`, `Kanji_Bangou`→`Codeinput`,
   `XF86_Screensaver`→`XF86ScreenSaver`, `Arabic_ha`→`Arabic_heh`.
2. **Unicode band** `0x01000100 … 0x0110ffff` and not in the table → `U%04X` of the low 24 bits
   (`src_keysym.c:66`): `0x1000100`→`U0100`, `0x110ffff`→`U10FFFF`. Note 717 table values live *inside* this band
   and print their explicit name instead (`0x100012c` → `Ibreve`).
3. **everything else unnamed** → `0x%08x` (`src_keysym.c:93`), lowercase, 8 digits:
   `0x1000000`→`0x01000000`, `0x10000ff`→`0x010000ff`, `0x1110000`→`0x01110000`, `0x1008ffb9`→`0x1008ffb9`.
   The band `0x01000000…0x010000ff` deliberately does **not** use Unicode notation.

Format details: `%#06` is the 0x prefix plus zero padding to 6 columns, so values below 0x10000 get 4 hex digits
(`0x002f`, `0x0001`) and larger values are not truncated (`0x1008ffb8`); Python `"0x%04x"` is equivalent for
every reachable value. `%#x` prints no `0x` for the value 0 (it would give `000000`), but value 0 never reaches
this line. `name` longer than 30 chars would make `snprintf` truncate and the judge print
`ERROR: Failed to get name of keysym` with rc 1 (`tools/how-to-type.c:570`) — unreachable: the longest canonical
name is exactly 30 (`XF86ElectronicPrivacyScreenOff`) and the fallbacks are at most 10 chars, against
`XKB_KEYSYM_NAME_MAX_SIZE 31` (`src_keysym.h:55`).

## 3. Error matrix (measured, `receipts/judge-refusal-sample.txt`, `receipts/handpicked.txt`)

| case | rc | stdout | stderr |
|------|----|--------|--------|
| valid name / `U…` / `0x…` / decimal | 0 | line 1 header, blank line, `=== Direct access ===`, blank, column header, rows | empty |
| unknown name, wrong case, `U+0041`, `0x0`, `0`, `00`, `-47`, overflow, `>0x1fffffff`, empty ARG, 9+ digit hex | 2 | **empty (0 bytes)** | `ERROR: Failed to convert argument to keysym` then the full 51-line usage block, starting `Usage: <argv0> [--help] …` |
| `-h`, `--help` (getopt, before the parser) | 0 | the usage block | empty |
| keysym whose name cannot be produced | 1 | — | unreachable as shown above |

Because the usage text embeds `argv[0]`, byte-identical **stderr** is not achievable by a reimplementation; the C1
contract compares **stdout + rc only**, which is exactly what these two remaining classes need.

## 4. Files and receipts (all under `.ufo/waves/round-49/w1/ExecKeysymNames/`)

* `keysyms.py` — the deliverable (library + tiny CLI: `header ARG`, `--verify HEADER`, `--emit-table HEADER`).
* `receipts/names-diff.txt` (10,618 lines) — the sweep: `STATUS judge_rc tool_rc judge_line1 tool_line1 ARG`.
* `receipts/names-diff-edge.txt` — 300 sampled ARGs under **two** keymaps + 44 hostile ARGs.
* `receipts/summary.txt` — computed counts (`A` sweep, `B` aliases, `C` value forms, `D` header-vs-ks_tables). `RESULT PASS`.
* `receipts/rule-check.txt` — 2638 anchored defines / 2505 values / 133 aliases; the last-define rule's 120 flips;
  the 1-of-133 alias-comment count.
* `receipts/handpicked.txt` — boundary panel (band edges, `XF86FullScreen`, option-looking ARGs).
* `receipts/invocation-form.txt` — `--keymap=FILE` vs `--keymap FILE`, plus the judge's own `--help` text.
* `receipts/judge-refusal-sample.txt` — rc/stdout/stderr shape of four refusals.
* `receipts/sandbox-no-header.txt` — bwrap: header masked, whole fs read-only, tool still correct.
* `receipts/table-verify.txt` — embedded table == header-derived table (`verify_rc=0`).
* `receipts/pins.txt` — every fetched source: sha256 + tag URL; plus the three host pins from `claims.md`.
* `receipts/quotes-verified.txt` — 28/28 locators recomputed by `receipts/verify-quotes.py` (greps the pinned file
  and requires a match within ±2 lines of the cited line).
* Runners: `receipts/run_judge_sweep.py`, `receipts/run_judge_edge.py`, `receipts/summarize.py`,
  `receipts/verify-quotes.py`.

Reproduce: compile the fixture keymap with the pinned `xkbcli-compile-keymap --layout br --options compose:caps`
under `env -i PATH=/usr/bin` with HOME/XDG_CONFIG_HOME in scratch, then run the two `run_judge_*.py` scripts.

## 5. Notes for the counter / freeze

* Compare **stdout + rc**; ignore stderr. Refusals must show **0 bytes** on stdout.
* Draw ARGs from: the 2638 names (case-sensitive, exact), `U`+1..8 hex, `0x`+1..8 hex, decimal with
  `0 < v <= 0x1fffffff`. Exclude: leading `-`, `-h`/`--help`, keysym value 0, `0X` prefix, `U+…`.
* The gate is keymap-independent for this target, so the nonce can pair *any* RMLVO-derived keymap with any ARG;
  the keymap only matters for the `=== Direct access ===` rows (other seat's target).
* If a later variant wants the tool to derive from the header instead of embedding, the sandbox must expose
  `/usr/include/xkbcommon/xkbcommon-keysyms.h` at its pinned sha256
  `13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3` and `--verify` proves equivalence; the
  recommendation is the embedded table (fewer sandbox surfaces, no header drift).
* Host header drift is the only silent-failure mode of the embedded table. `keysyms.py --verify` re-derives and
  compares in one call; wire it into the C1 fixture setup if the counter host may differ from this one.

## 6. Risks

* **Unreachable-but-modelled paths.** `get_name` error (rc 1) and the `%#06x` zero quirk cannot be reached from ARG;
  they are implemented for completeness, not proven by the judge.
* **Non-ASCII ARGs** (`é`, `日本語`, `\u00a047`) refuse identically (rc 2, empty stdout) — covered in
  `names-diff-edge.txt`, not in the main sweep.
* **`strtol` locale.** The judge never calls `setlocale` when `--disable-compose` is used, so it parses in the C
  locale. If a future fixture drops `--disable-compose`, compose loading calls `setlocale(LC_CTYPE, NULL)` and a
  UTF-8 locale could change `strtol` grouping behaviour for exotic inputs; the contract keeps `--disable-compose`,
  so this is outside it.
* Scratch dir `/fast/scratch/hyaku/mado-r49/ExecKeysymNames` was used for the keymap builds and is deleted after
  the receipts were copied; no receipt cites a scratch path as evidence (only the `$SCRATCH` placeholders).
