# ExecStubFidelity — stub vs real `hyprctl getoption -j` reply shape (C1 fidelity)

Scope: the STUB in `quality/counters/c1-r40-live.py:406-428` and its argv contract, versus the
host binary `/usr/bin/hyprctl` (Hyprland 0.56.2, commit efb50993780079460b0cbed1363e2166a2de1d9f).
Everything below is measured unless marked `[INFERENCE]`. Harness:
`.ufo/waves/round-40/w1/ExecStubFidelity/stub-fidelity.py`; its full output is
`.../ExecStubFidelity/evidence.json`; the 13 real reply byte files are `.../real-<key>.bin`;
source excerpts are `.../src-excerpt.txt`.

## 1. Byte comparison — 12 keys (3 int, 2 float, 3 str, 4 custom) + 1 absent

| form | real bytes | counter STUB bytes | equal |
|---|---|---|---|
| int | `{"option": "animations:enabled", "int": 1, "set": true }\n` | `... "set": true}\n` | no |
| int (u32) | `{"option": "group:groupbar:text_color", "int": 4294967295, "set": true }\n` | same minus space | no |
| float | `{"option": "decoration:blur:brightness", "float": 0.600000, "set": true }\n` | `... "float": 0.6, "set": true}\n` | no |
| float | `{"option": "cursor:zoom_factor", "float": 1.000000, "set": false }\n` | `... "float": 1.0, "set": false}\n` | no |
| str | `{"option": "general:layout", "str": "dwindle", "set": true }\n` | same minus space | no |
| str (empty) | `{"option": "input:kb_model", "str": "", "set": true }\n` | same minus space | no |
| custom | `{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }\n` | same minus space | no |
| absent | `no such option\n` | `no such option\n` | **yes** |

`byte_equal = 1/13`. Two systematic deltas:
1. **Space before `}`** — real `"set": true }`; stub `"set": true}`. Real is built from
   `std::format(R"({{"option": "{}", "int": {}, "set": {} }})")` (`src/debug/HyprCtl.cpp:1702`,
   excerpt line 1 in `src-excerpt.txt`); the stub uses `json.dumps(rec)`, whose separators are
   `(', ', ': ')` and which cannot place a space before the closing brace.
2. **Float text** — real uses `{:2f}` (`HyprCtl.cpp:1706`), i.e. fixed 6 decimals
   (`0.600000`, `1.000000`, `0.000000`); the stub emits the Python repr (`0.6`, `1.0`).
   All 5 host floats confirm the 6-decimal form.
Matches: key order `option, form, set` (the stub preserves `table.json` insertion order and
`Fixture.table()` builds it in that order — `c1-r40-live.py:384`); exactly one trailing `\n`, no
`\r`; `"set": false` is emittable by the stub (probe `set-false`).

Whole-host check: all **70/70** keys of `python3 -I tools/mado-options.py --home $HOME` match
`^\{"option": "[^"\\]*", "(int|float|str|custom)": .*, "set": (true|false) \}\n$`, byte-identical
across two consecutive runs (0 non-deterministic, 0 non-ASCII). Forms: int 44, float 5, custom 13,
str 8 — the four-form universe the stub models is exactly right **for these 70 keys**.

## 2. Shapes the stub cannot emit that the real binary does

| # | shape | real | stub | attacks |
|---|---|---|---|---|
| a | space before `}` | `true }` | `true}` | every present-form fixture |
| b | float 6-decimal text | `0.600000` | `0.6` | float fixtures; also real never uses exponent form while the stub *can* emit `1e-05` (probe `float-exp`) — a reply the real binary never produces |
| c | `vec2` form (5th form, `HyprCtl.cpp:1708`) | `{"option": "decoration:shadow:offset", "vec2": [0,0], "set": false }\n` | `json.dumps` would give `[0, 0]`; the counter never generates it (`FORMS = ('int','float','str','custom')`, `c1-r40-live.py:99`) | 6 real host keys: `decoration:shadow:offset`, `input:tablet:region_position`, `input:tablet:region_size`, `input:tablet:active_area_size`, `input:tablet:active_area_position`, `layout:single_window_aspect_ratio` (0/353 others; 0 of the 70 declared keys) |
| d | `bool` form branch | `HyprCtl.cpp:1704` emits `"bool": true` | not modelled | source-reachable, 0/353 on this host |
| e | raw UTF-8 in `str` | `escapeJSONStrings` copies any byte >0x1f except `"`/`\` verbatim (`MiscFunctions.cpp:85-105`) | `json.dumps` default `ensure_ascii=True` → `"Sans\u00e9\u4e2d"` | same decoded str, different bytes; 0/353 host values non-ASCII, so unobserved live |
| f1 | escaped-branch escapes | `"`→`\"`, `\`→`\\`, `\n`/`\t`/`\r`/`\b`/`\f`, other <0x20 → `\u00XX` | identical (`json.dumps` probes `str-quote`, `str-newline`) | no divergence on the escaped branch — a quoted newline is `\n` on both sides |
| f | unescaped `Config::STRING` | `HyprCtl.cpp:1716` inserts the value **without** `escapeJSONStrings` → a `"` or newline in such a value yields invalid JSON | stub only emits invalid JSON in its explicit `bad:` mode | `[INFERENCE]` reachability (no host value carries a quote); the escaping asymmetry is read from source |
| g | failure stream | rc=1 `HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)\n\n` and rc=4 `Couldn't connect to ... (4)\n`, **both on stdout, stderr empty** | `fail:` mode: rc=1, message on **stderr** | a tool that reads stdout before checking rc sees a non-empty stdout on failure; the stub cannot reproduce that, nor rc=4 |
| h | multiple form keys | never (exactly one) | `json.dumps` will emit two (`{"option": "x", "int": 1, "float": 1.0, "set": true}`) | an unreal shape the stub *can* emit; the tool's `len(forms) != 1` guard is never exercised by the fixtures |
| i | `css` / `gradient` / `font_weight` form keys | dead branches on the host (those types route through `custom`; observed `general:gaps_in` → `"custom": "0 0 0 0"`) | emittable as raw keys | not a live shape |

## 3. Do the reference tool and the BASE code parse the REAL bytes?

- **Reference tool** (`c1/ctl-ref-tool.py.txt`), `native_query` fed the 13 real reply byte sets
  through a replay binary that writes the captured bytes verbatim: **13/13 correct** —
  `('int',1,True)`, `('int',4294967295,True)`, `('float',0.6,True)`, `('float',1.0,False)`,
  `('str','dwindle',True)`, `('str','',True)`, `('str','Sans',False)`,
  `('custom','ffe68e0d 45deg',True)`, `('custom','0 0 0 0',True)`,
  `('custom','ee33ccff ee00ff99 45deg',True)`, `('custom','1000',True)`, absent → `None`.
  Whitespace and the 6-decimal text are irrelevant to `json.loads` — the reference parser is
  shape-agnostic, so the fixture divergence in §1 cannot change its verdict.
- **BASE** (`9fc511dd:tools/mado-options.py`, sha256 `461f8c3c…9fb03a`, copy in the seat dir):
  `--live` and `--hyprctl` are `unrecognized arguments` (rc 2), and its only JSON path,
  `load_live`, rejects the real native replies: `LiveError: entry for 'animations:enabled' lacks
  value/custom_type/set`. So the base cannot consume the native shape at all — the required
  translation is genuinely new, not a refactor.
- **Out-of-model consequence (measured on the reference tool, not the stub):**
  `python3 -I /tmp/ref.py --home $HOME --live --hyprctl /usr/bin/hyprctl --probe
  decoration:shadow:offset` → `mado-options.py: decoration:shadow:offset: unknown reply form from
  /usr/bin/hyprctl`, **rc 5**. The compositor answered correctly; the key is simply `vec2`.

## 4. Verdict

- The stub is a faithful **semantic** stand-in and an unfaithful **byte** stand-in: 1/13 byte-equal,
  and every present-form reply differs in at least the space before `}`. This costs the counter
  nothing, because the tool parses (`json.loads`) instead of matching bytes — but it also means the
  counter cannot distinguish a correct parser from a byte-matcher that would fail on the host.
- The stub's form universe (4) is narrower than the real binary's reachable set (6: `vec2` observed
  on 6 host keys, `bool` present in source). No vec2/bool key is in the host's 70-key table, so the
  live receipt is unaffected; a `--probe` of a vec2 key exits 5 with a "compositor failure" message
  although the compositor succeeded.
- Failure shape (stdout message, rc 1 or 4) and the `Config::STRING` unescaped branch are the two
  remaining stub shapes that a delivered tool could lean on without the counter noticing.

## 5. Files written (all inside the seat dir)

`stub-fidelity.py`, `evidence.json`, `real-*.bin` (13), `base-mado-options.py` (read-only copy from
git), `src-excerpt.txt`. No lane file, config tree, compositor state or service touched; the only
compositor verbs run were `getoption -j`, `version`, `descriptions -j`. No package transaction.
