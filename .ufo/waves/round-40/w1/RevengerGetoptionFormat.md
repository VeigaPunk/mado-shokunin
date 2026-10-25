# RevengerGetoptionFormat — why the base `--getoption FILE` format is not the compositor's

Seat: `.ufo/waves/round-40/w1/RevengerGetoptionFormat/` (leaf). Lane: `mado-shokunin`.
Target: reconstruct the origin of `tools/mado-options.py --getoption FILE`'s schema
`{key: {value, custom_type, set}}`, who normalised the dump, and which held statement the
native forms contradict. Read-only throughout except this seat dir; no compositor mutation
(only `hyprctl version` and `hyprctl getoption -j` were run, both allowed read verbs).
No tools installed.

## 0. Answer

1. **The base format is not a compositor reply and never was.** The compositor's `-j` reply
   is `{"option": K, "<form>": V, "set": B}` (`HyprCtl.cpp:1701-1728` at the host commit;
   live probe below). The base tool's file is a **keyed map with the form split out into a
   field named `custom_type` and the value renamed `value`** — a hand transcription of the
   held table's columns, not of any hyprctl output.
2. **Origin: the round-39 L1 wrote the schema into the seat prompt**, before any seat ran.
   It is verbatim in the dispatched record `.ufo/waves/round-39/w1-dispatch.json:426` and in
   `.ufo/waves/round-39/w1-spec.json` (items[0] = `ExecOptionsTool`), and it is the
   only occurrence of the string `custom_type` in that dispatch. The round-39 registration
   declared only "an optional `--getoption <json>` live-value merge"
   (`.ufo/waves/round-39/registration.md:59-64`) — the field names are the L1's invention,
   modelled on `corpus/knowledge/hyprctl-verification-layer.md` §3's `form: value` + `set`
   columns (`:67-71`) and on the text form's literal label `custom type:`
   (`HyprCtl.cpp:1691`; captured at `.ufo/evidence/round-12/drift-precedence.txt:5`).
3. **Who normalised the dump:** (a) the L1 chose the schema; (b) seat `ExecOptionsRealTree`
   produced the only host-wide dump, `getoption-synthetic.json` (56 keys), by re-encoding
   held §3 plus the round-37 native captures into that schema; (c) seat `ExecOptionsFixtures`
   wrote a second dump with type names the compositor never emits (`bool`, `string`);
   (d) the frozen counter `quality/counters/c3-r39-options.py:298-330` bakes the schema and
   `custom_type: "str"` into the predicate, so round 39 *scored* the schema, never checked it.
4. **Held statements the native forms contradict:** `config-option-table-r39.md:91` and
   `tools/mado-options.py:20-22` call the file "a `hyprctl getoption` dump / JSON mapping"
   (false); `hyprctl-verification-layer.md:69-71` calls its cells "verbatim from
   `hyprctl -j getoption`" (they are `form: value` concatenations); and the provisional
   round-40 fact "forms int|float|str|custom" is a *host subset*, not the vocabulary
   (source has nine JSON form keys plus a text-only set). Details in §4.

## 1. The two shapes the compositor actually emits (re-derived, not relayed)

Source, Hyprland v0.56.2 `src/debug/HyprCtl.cpp` @ `efb50993780079460b0cbed1363e2166a2de1d9f`,
read from the round-40 fetch `.ufo/waves/round-40/fetch/hyprctl-efb5099.bin`
(byte copy of the pinned commit; line numbers are that file's):

| Branch | Emitted shape |
|---|---|
| `:1670` | unknown key → `return "no such option";` (plain text, even under `-j`) |
| text `FORMAT_NORMAL` `:1675-1699` | `int:`, `bool:`, `float: {:2f}`, `vec2: [{}, {}]`, `str:`, `custom type:`, `css gap data:`, `gradient data:`, `font weight data:`, each followed by `\nset: {}` |
| JSON `:1701-1728` | `{"option": "<key>", "int"|"bool"|"float"|"vec2"|"str"|"custom"|"css"|"gradient"|"font_weight": <v>, "set": <b> }` |
| `:1731` | `return "invalid type (internal error)";` |

Note the JSON format strings end `"set": {} })` — the reply carries a space before `}`.
`bool` is emitted as the JSON literals `true`/`false` (`:1703-1704`), not `0`/`1`.

Live probes (allowed read verbs, 2026-10-25, host `Hyprland 0.56.2 … efb5099… clean`):

```
$ hyprctl getoption -j mado:bogus_key_xyz
no such option
exit=0
$ hyprctl getoption -j general:border_size
{"option": "general:border_size", "int": 0, "set": true }
exit=0
$ hyprctl getoption -j general:gaps_in
{"option": "general:gaps_in", "custom": "0 0 0 0", "set": true }
```

So the native reply is **self-labelling**: the key is echoed, the form is the *name of the
value field*, and there is no `value` and no `custom_type` field anywhere.

## 2. Timeline of the base format (all commits read-only)

| When (author date) | Artifact | What it shows |
|---|---|---|
| 2026-10-14 (round 2) | `corpus/knowledge/hyprctl-verification-layer.md:67-149` | the 56-pair table; live cells written `custom: 0 0 0 0`, `int: 0`, `str: dwindle`, `float: 0.600000`, with a separate `set` column; header claims "verbatim from `hyprctl -j getoption`" (`:69-71`) and correctly notes "`-j` renders `custom`-type options under a `custom` key, not `str`" |
| round 12 | `.ufo/evidence/round-12/drift-precedence.txt:1-12` | the **text** form captured: `custom type: 0 0 0 0` / `set: true`; `str: br` / `set: true` — the literal spelling `custom type` that becomes `custom_type` |
| round 37 | `.ufo/waves/round-37/w1/scratch/RevFreezeOrder/getoption.txt:1`, `.../ConnFrontier/desc-vs-getoption.txt:2-4` | native JSON kept **verbatim**: `{"option": "debug:disable_logs", "int": 1, "set": false }`, `{"option": "general:gaps_out", "custom": "0 0 0 0", "set": true}` |
| round 39 freeze (`457d1b1`, 13:00) | `.ufo/waves/round-39/registration.md:59-64` | C2 declares "an optional `--getoption <json>` live-value merge"; **no field names**, and "no compositor, socket or network" in the read path |
| round 39 dispatch (same day) | `.ufo/waves/round-39/w1-dispatch.json:426`; `.ufo/waves/round-39/w1-spec.json` items[0] | the L1 writes the schema: "a file mapping key -> {value, custom_type, set} merges live values"; `grep` over the whole dispatch finds exactly **one** string containing `custom_type` — that prompt. The wave `context` contains **zero** occurrences of `hyprctl`, so no seat was allowed or asked to capture a reply. Caveat: these two records were *committed* in `b6078c3` (17:13), after the data commit, so their commit time is not the authoring time; the mitigation is that the tool seat reports the schema as its assignment (`ExecOptionsTool.md:16`, `:43-45`) and the only other artifacts carrying the field names are the seat-built tool and the counter draft committed at `fca5161` (17:03), both downstream of the same dispatch |
| round 39 attempt-2 freeze (`d9b4e4a`, 17:03) | `quality/counters/c3-r39-options.py:298-330` (frozen as `PRED-C3-r39-v2`) | the predicate generates flat dumps: `live[k] = {"value": v, "custom_type": "str", "set": True}` — **every** key typed `str`, so int/float/custom conversion is never exercised |
| round 39 data (`4ec582e`, 17:04) | `tools/mado-options.py` (1050 lines) | the tool lands with the schema; `git blame -L 18,26` puts the sentence "merges a live `hyprctl getoption` JSON mapping (key -> {value, custom_type, set})" in that commit |
| round 39 entry (`3783961`) | `corpus/knowledge/config-option-table-r39.md:91` | the delivered entry repeats the misdescription: "`--getoption FILE` merges a `hyprctl getoption` dump (key → value, custom_type, set)" |
| round 40 (`5e7e885`) | `quality/counters/c1-r40-live.py`, `c2-r40-forms-entry.py` | no `custom_type` and no `--getoption` anywhere in the round-40 predicates: the file format is superseded by one `hyprctl getoption -j KEY` per declared key |

Pickaxe confirms there is no earlier origin: `git log --all -S'custom_type'` hits only
`d9b4e4a`, `fca5161`, `4ec582e`, `3783961` (plus an unrelated round-17 session-JSONL
`custom_types` census), and `git log --all -S'--getoption'` hits nothing before the round-39
freeze family.

### Why a file at all (original intent, `[INF]` on motive)

The round-39 claim forbade the compositor in the tool's read path
(`registration.md:59-64`, "no compositor, socket or network"; `RevC2Tool.md:25-26`
re-verified "`--getoption` reads a JSON file, never hyprctl"). A live layer therefore had
to arrive as recorded bytes, and the L1 specified the shape from the only live artifact it
had in front of it: the held §3 table. The *stated* provenance is weaker than that — see §4.6.

## 3. Who normalised the dump

1. **L1 (schema author).** The schema is in the dispatched prompt
   (`w1-dispatch.json:426`), not in any seat output. Seat `ExecOptionsTool` reports
   "Behavior (per assignment spec)" (`ExecOptionsTool.md:16`) and reproduced the schema
   sentence verbatim (`ExecOptionsTool.md:43-45`); the schema's shape is therefore the L1's,
   not the tool author's.
2. **Seat `ExecOptionsRealTree` (the only host-wide dump).**
   `.ufo/waves/round-39/w1/ExecOptionsRealTree/getoption-synthetic.json` — 56 keys, built
   "from the lane's own recorded getoption pairs: the 56-row claim→live mapping of
   `corpus/knowledge/hyprctl-verification-layer.md` §3 … plus the verbatim recorded JSONs in
   round-37 scratch" (`ExecOptionsRealTree.md:59-66`). Its encoding, checked key by key:
   `general:gaps_in` → `{"custom_type": "custom", "set": true, "value": "0 0 0 0"}`;
   `general:col.active_border` → `custom` / `ffe68e0d 45deg`; `animations:enabled` →
   `int` / `1`; `input:sensitivity` → `float` / `0.0`; `input:kb_variant` → `str` / `""`
   (the held `(empty)` and `[[EMPTY]]` sentinels were normalised to the empty string).
   Census `{int: 37, str: 8, custom: 6, float: 5}`. The conversion is careful and lossless
   **for the held table**, but it never touched a compositor: the `option` echo is dropped
   (redundant in a keyed map), and the form label becomes a field.
3. **Seat `ExecOptionsFixtures` (a second, private vocabulary).**
   `.ufo/waves/round-39/w1/ExecOptionsFixtures/trees/main-home/.config/hypr/live.json` uses
   `"custom_type": "bool"` and `"custom_type": "string"`. `bool` is a real JSON form
   (`HyprCtl.cpp:1703-1704`); **`string` is emitted by nothing** — the native name is `str`
   (`:1713-1716`). Its prompt only said "a `--getoption` JSON dump", so the type names there
   are the seat's own.
4. **Frozen counter (schema encoded as oracle).** `c3-r39-options.py:310-319` writes
   `custom_type: "str"` for every key, including integer options, and only ever compares
   string equality. A schema that never had a producer cannot be falsified by a predicate
   that generates the same schema.

Two consequences already on record in round 39: `ConnOverlapScan.md:84-86` called
`--getoption FILE` "an ad-hoc JSON format that requires an undocumented multi-process
gathering loop" and proposed `hyprctl --batch -j` (round-40 C1 implements the per-key
version of that), and `SctHeldEntries.md:161-176` measured that the tool cannot reproduce
the held classification (§4.3).

## 4. Held statements the native forms contradict

**4.1 `config-option-table-r39.md:91` / `tools/mado-options.py:20-22` — "a `hyprctl getoption`
dump (key → value, custom_type, set)".**
Contradicted by the compositor's bytes (§1) and by the tool's own behaviour on them. Four
runs against the untouched round-39 fixture tree
(`.ufo/waves/round-39/w1/ExecOptionsFixtures/trees/main-home`, read-only):

```
native reply keyed by option : exit=4  mado-options.py: …/native-one.json: entry for 'input:kb_layout' lacks value/custom_type/set
native JSONL (2 replies)     : exit=4  …: cannot load getoption JSON: Extra data: line 2 column 1 (char 57)
round-37 native capture file : exit=4  …/RevFreezeOrder/getoption.txt: … Extra data: line 2 column 1 (char 58)
round-40 native capture (70) : exit=4  …/c1/native-capture.jsonl: … Extra data: line 2 column 1 (char 57)
flat control (same key)      : exit=0
```

Every artifact of the compositor the lane owns is rejected by the format that claims to be
its dump; the flat control on the same key exits 0. This is the sharpest statement in the
record that is simply false, and it is duplicated in the delivered entry and the tool
docstring.

**4.2 `hyprctl-verification-layer.md:69-71` — "Live values are verbatim from
`hyprctl -j getoption <opt>`".**
Not verbatim: the cells are `form: value` concatenations (`custom: 0 0 0 0`,
`int: 0`, `str: dwindle`) with `set` moved to its own column, while the reply is
`{"option": "general:gaps_in", "custom": "0 0 0 0", "set": true }`. The parenthetical on the
next line ("`-j` renders `custom`-type options under a `custom` key, not `str`") is correct,
so the entry knew the JSON shape and still transcribed. This cell format is the direct
ancestor of `custom_type`.

**4.3 `hyprctl-verification-layer.md` §3 class census (`:143-144`) — "0 `mismatch`", 52 agreement
(6 `agreement*`).**
Reproducible only with the hand normalisation the entry performed. Fed its own 56 pairs
(re-encoded flat), the base tool prints `agreement 41, agreement* 6, config-only 27,
mismatch 5, live-default 4` (`ExecOptionsRealTree.md:71-72`;
`run-getoption.stdout`), and the five mismatches are exactly the five form conversions:
`animations:enabled` (`yes, please :)` → `int: 1`, hyprlang truthy-string parse),
`decoration:shadow:color`, `general:col.active_border`, `general:col.inactive_border`,
`group:col.border_active` (config colour → `<ARGB> <angle>deg` gradient string). Under the
native-form model with host-style conversion the census returns to 0 mismatch
(62 agreement / 8 agreement*, the number C1's claim states; not re-measured by this seat). So the held
"0 mismatch" is not wrong about the host — it is wrong about what a *machine* reading the
native form gets without the conversion step, and the base format names the form
(`custom_type`) while dropping the conversion obligation.

**4.4 The provisional round-40 fact "native forms int|float|str|custom".**
A host subset, not the vocabulary: `HyprCtl.cpp:1701-1728` emits nine JSON form keys
(`int`, `bool`, `float`, `vec2`, `str`, `custom`, `css`, `gradient`, `font_weight`) plus the
fallback string `invalid type (internal error)`; the text form has a different set of nine
labels (`custom type:`, `css gap data:`, `gradient data:`, `font weight data:`, …). The
70-key capture (int 44, float 5, custom 13, str 8) is exactly the subset this host's
declared keys reach — `[INF]` whether `css`/`gradient`/`font_weight` are reachable at all
for config options, since the observed gap/gradient keys answer `"custom"` through the
`void*`/`IComplexConfigValue` branches (`:1717-1721`) before the later branches. Any round-40
entry that says "the four native forms" without "for the host's declared keys" overstates.

**4.5 `-j` is not JSON on every path.** `hyprctl getoption -j <unknown>` prints the bare line
`no such option` and exits 0 (probed above; `HyprCtl.cpp:1670`). A JSON-consuming schema
needs a sentinel for that; the base format has none (a missing key means `config-only`, a
*different* class — so an unknown-key probe would silently become "declared, no live row").
Round-40's claim ("native replies … or the text `no such option`") states this correctly.

**4.6 Provenance of the schema is cited to a proposal that does not exist.**
`registration.md:97-99`, `corpus/lessons/round-39.md:80-82` and
`config-option-table-r39.md:6-8` all attribute the config-option table to
"`considerthese/2026-10-24.md` proposal 4 ('the config-option table — who owns each key,
checked against `getoption`')". That file's proposal 4 is "**Suggest the next desktop table
explicitly**" (next surface to cover, with sources), and the quoted phrase appears nowhere:
`git grep -n "who owns each key"` over every revision of `considerthese/` is empty,
`grep -c "who owns" considerthese/2026-10-24.md` → 0, and the pre-correction revision
`a327cd4` has the same six proposals as `57a772b`. The schema's real provenance is therefore
the L1's own prompt, and the "mined proposal" citation cannot be used to justify it.

## 5. What is *not* contradicted (fidelity check of the held pairs)

Re-derived against the 70-key native capture: 56 held §3 rows parsed; 52 are in the capture,
**49 of them agree exactly on form, value and `set`** (numeric comparison), and the other 3
differ only in notation (`input:kb_variant`/`kb_model`/`kb_rules` written `(empty)` vs native
`"str": ""`); 4 rows (`general:snap:enabled`, `decoration:dim_inactive`,
`input:accel_profile`, `input:touchpad:disable_while_typing`) are absent from the capture
because they have no declarer — consistent with their `live-default` class, and the capture
contains no `set=false` row at all (all 70 declared keys are `set=true`), which supports §2's
`set` correlation.

So the held *values* survive; it is the **container** (the flat schema, and the word
"verbatim"/"dump") that does not. Two held entries use a *third* normalisation in the same
corpus, which shows the corpus never fixed one: `config-health-report-r3.md:785-830` is a
pipe table `key|form|value|set|class`, and `:520-545` is a markdown table with value plus
`set`/`unset` and **no** form column. `[[EMPTY]]` is a lane sentinel that appears in the same
pipe table (`:824`) beside genuinely empty cells (`:818-821`), so it is notation, not data.

## 6. Confidence

- Native shape, the nine JSON branches, the `no such option` path, the tool's exit 4 on every
  native artifact, the schema's presence in the dispatched prompt, the synthetic dump's
  encoding, and the counter's `str`-only fixtures: **observed** (source lines, live probes,
  command exits, file contents).
- "The L1 chose the schema because the claim banned the compositor and the held table was the
  only live artifact available": **`[INF]`** — no artifact states the reasoning; the ban and
  the table are both observed, the causal link is inference.
- "The `custom_type` field name is a transcription of the text form's `custom type:` label":
  **`[INF]`** — the spelling match and the round-12 capture are observed; the naming act
  itself is not recorded.
- Whether `css`/`gradient`/`font_weight` JSON branches are reachable for config options:
  **`[INF]`** (see §4.4).

## 7. Commands, artifacts, tool state

Runs (all read-only; no lane file edited):

```
python3 -I tools/mado-options.py --home <r39 fixtures tree> --getoption <native-one.json>      # exit 4
python3 -I tools/mado-options.py --home <r39 fixtures tree> --getoption <native-jsonl.json>    # exit 4
python3 -I tools/mado-options.py --home <r39 fixtures tree> --getoption .ufo/waves/round-37/w1/scratch/RevFreezeOrder/getoption.txt   # exit 4
python3 -I tools/mado-options.py --home <r39 fixtures tree> --getoption .ufo/waves/round-40/c1/native-capture.jsonl                    # exit 4
python3 -I tools/mado-options.py --home <r39 fixtures tree> --getoption <flat-one.json>        # exit 0
hyprctl version | hyprctl getoption -j mado:bogus_key_xyz | hyprctl getoption -j general:border_size | hyprctl getoption -j general:gaps_in
git log --all -S'custom_type' ; git log --all -S'--getoption' ; git blame -L 18,26 tools/mado-options.py
```

Seat artifacts: `native-one.json` (`26a7812a…`), `native-jsonl.json` (`970db7e6…`),
`flat-one.json` (`7efc421a…`), and `out.<case>.{stdout,stderr}` for all five runs.
No `/tmp` scratch was created; nothing outside this seat dir was written. No packages
installed (stdlib + the already-present `hyprctl`).
