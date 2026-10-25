# ExecAllOptionsForms — all-options native `getoption` form census (w1, round 40)

Seat: `ExecAllOptionsForms` · mado round 40 (hyaku run 7) · wave w1 · 2026-10-25
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Freeze read first: `.ufo/waves/round-40/registration.md` (freeze `5e7e88525cc539563de7746361b2650802e81809`,
base `9fc511ddce708327377161202f358ce37dc266ba`).

## Assignment

Survey the compositor's native `getoption` reply forms over **every** option, not just the 70
declared keys; write `forms.tsv` (name, form, set, value) plus a summary; state plainly whether
the counter's assumption of exactly four forms holds over the whole option set.

## Headline

**The four-form assumption holds exactly over the 70 declared keys and over the frozen capture,
and does NOT hold over the whole option set.** The compositor answers a **fifth** form, `vec2`,
for 6 of its 353 options. Over all 353: `int 264 / float 34 / str 28 / custom 21 / vec2 6`.

## What was run (read-only, serially)

1. `hyprctl version` → `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`,
   hyprlang `built 0.6.8 / system 0.6.8` (re-derives the provisional fact).
2. `hyprctl descriptions -j` → 353 names, 353 unique, all non-empty strings; entry keys
   `{name, description, default, current, min, max, map}`. Captured twice: byte-identical
   (`sha256 4aa2745c11b92d36abbf5355f2dc9217ed54e143a2f0621e0cc7a2b3e2652aab`). No fallback to
   `ConfigValues.cpp` was needed — `descriptions -j` is the compositor's own value registry and
   answered exit 0 with 76138 bytes.
3. `hyprctl getoption -j <name>` once per name, serially, in `descriptions` order — 353 calls,
   `rc = 0` for all 353, `stderr` empty for all 353. Full second pass: the two raw captures are
   byte-identical (`sha256 c1e82034000f53c8b9eb6e687e27cf4408cfe38e7f6da842e0884a48bd8fbcf5`), so
   the reply set is deterministic across runs at this host state.
4. Strict parse per reply: `JSONDecoder.raw_decode` on the stripped text, remainder must be empty,
   top level must be a `dict`.
5. `python3 -I tools/mado-options.py --home $HOME` (static table) to derive the declared-70 set —
   **70 keys, 70 unique**, so the comparison set is exact.
6. `python3 -I quality/counters/c1-r40-live.py --repo . --rev 5e7e8852…` at the freeze commit →
   `clauses=a:1 b:0 g:1 k:1`, `fixtures=0/13 verdict=TARGET_MISSED` (the counter and its clause k
   run clean at the freeze; the tool has no `--live` yet).

Only compositor verbs used: `hyprctl version`, `hyprctl descriptions -j`, `hyprctl getoption -j`.
No `keyword`/`dispatch`/`reload`/`setprop`/`--batch`, no socket, no config-tree write.

## Findings

### F1 — five reply forms over the whole option set (attacks the four-form sentence)

| form | all 353 | declared 70 | not in capture (283) |
|---|---|---|---|
| `int` | 264 | 44 | 220 |
| `float` | 34 | 5 | 29 |
| `str` | 28 | 8 | 20 |
| `custom` | 21 | 13 | 8 |
| **`vec2`** | **6** | **0** | **6** |

The declared-70 column is the provisional fact verbatim (`int 44, float 5, custom 13, str 8`),
re-derived from the live compositor, not copied.

### F2 — the six `vec2` keys (evidence)

```
decoration:shadow:offset            {"option": "decoration:shadow:offset", "vec2": [0,0], "set": false }
input:tablet:region_position        … "vec2": [0,0], "set": false
input:tablet:region_size            … "vec2": [0,0], "set": false
input:tablet:active_area_size       … "vec2": [0,0], "set": false
input:tablet:active_area_position   … "vec2": [0,0], "set": false
layout:single_window_aspect_ratio   … "vec2": [0,0], "set": false
```

Reproduced identically on a direct re-run (`hyprctl getoption -j decoration:shadow:offset`,
`… input:tablet:active_area_size`, exit 0 both). The `vec2` value is a **JSON array**, unlike
`custom` (JSON string) — so the form is not a string shape.

Three independent corroborations that `vec2` is a first-class type, not an artifact:
- `/usr/include/hyprlang.hpp:282-288` — `enum eDataType { CONFIGDATATYPE_EMPTY,
  CONFIGDATATYPE_INT, CONFIGDATATYPE_FLOAT, CONFIGDATATYPE_STR, **CONFIGDATATYPE_VEC2**,
  CONFIGDATATYPE_CUSTOM }`; `VEC2` is `SVector2D` (`hyprlang.hpp:45`).
- `/usr/include/hyprland/src/config/values/types/Vec2Value.hpp:20` — `class CVec2Value` lives in
  the same value registry `descriptions -j` enumerates; `ConfigValues.hpp:25-26` validates
  `Config::VEC2`.
- `descriptions -j` independently marks exactly these six by `"default"`/`"current"` being JSON
  arrays (`[0, 0]`) while scalar options carry scalars there.

### F3 — reply-shape hygiene: no anomalies

- Replies that are **not exactly one JSON object**: **0** (all 353 parse as one dict with an empty
  remainder).
- Replies with **no** form: **0**. Replies with **more than one** of the four forms: **0**.
- `option` field equals the requested name: **353/353**.
- `set` present in all 353: **70 `true`** (exactly the declared-70 set) / **283 `false`**.
- Value JSON types by form: `int` → int (264), `float` → number (34), `str` → string (28),
  `custom` → string (21), `vec2` → array (6). No form/value-type contradiction.
- `no such option` is plain text with **exit 0** — reproduced on `nosuch:option` and
  `general:nosuch`; **no** name taken from `descriptions -j` produced it, so the 353-name list is
  entirely getoption-answerable.

Read through the assignment's own four-form lens (`int|float|str|custom`), the anomaly lists are
**not** empty: the six `vec2` keys (F2) carry **none** of the four. They are the only 6 keys with
"no form" under that lens, and they are the only keys that carry a form outside the frozen set.
There is no key with two or more of the four, and no reply that fails to be a single JSON object.

### F4 — the frozen capture is exactly the declared-70 set, and is reproducible

Comparing the census's 70-key subset against `.ufo/waves/round-40/c1/native-capture.jsonl`
(parsed, floats compared numerically, not as text): **0 disagreements** on form, `set` and value.
Both directions of the set difference are empty (0 capture keys undeclared, 0 declared keys
missing from the capture). Clause k of `PRED-C1-r40-v1` (`capture_ok`, counter lines 598-616:
70 lines, one form per line, `seen == set(FORMS)`) is therefore sound **as a statement about the
declared keys** — it is a 70-key census receipt, not a survey of the option set.

### F5 — keys the frozen capture could not have contained: 283

`not-in-capture.tsv` lists all 283 names with their form/`set`/value. None is `set: true`; six
carry `vec2`. So the capture's information horizon is 70/353 ≈ 20% of the option names.

### F6 — what this means for C1's `--probe` (risk, with the counter's own lines)

The counter's contract says an answer "with no known form" must exit 5 with the key on stderr
(`quality/counters/c1-r40-live.py:41-42`), and `FORMS` is the four-form tuple (line 99). Under
that sentence, a `--probe decoration:shadow:offset` on this host must **exit 5 naming the key** —
i.e. the tool is required to report a *legitimate* option as a compositor failure, because the
option answers a form outside the frozen four.

Worse, that behaviour is **not pinned by any fixture**: the stub's failure modes are
`fail:` (stderr + exit 1) and `bad:` (`{not json`) only (lines 417-422), and every generated
fixture record is built with `form` ∈ the four (lines 260-300, kinds `bool/num/colour/float/str/
grad/gap/weight/ginh`). No fixture emits a well-formed JSON object carrying an unknown form.
Consequently two different tools — one that exits 5 on a `vec2` answer and one that labels it
`live-default` — both score 13/13. The `vec2` branch is a contract sentence without a witness.

This is a report, not a request: C1's declared target is untouched by the finding (its stub is
four-form by construction), and I did not edit the counter, the tool or any C2 file.

### F7 — C2's sentence "the four native forms" is census-scoped

`corpus/knowledge/hyprctl-getoption-native-forms-r40.md` and the registration both speak of "the
four native forms". That is **true of the 70 declared keys and of the capture** (F4) and **false
of the compositor's option set** (F1). The entry needs the scope qualifier ("over the declared
option keys / the 70-key census"), or a fifth-form sentence. Flagged for the C2 seat and the L1;
no file of C2's was touched.

## Files written (all new, all inside my seat directory)

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ExecAllOptionsForms/`

| file | content | sha256 |
|---|---|---|
| `forms.tsv` | `name\tform\tset\tvalue`, 353 rows + header | `e26deb4aac35939bfd6343b093975227049d0fff173c4e3ada1f40138a8b2c66` |
| `raw-census.jsonl` | 353 rows `{i,name,rc,stdout,stderr}`, pass 1 | `c1e82034000f53c8b9eb6e687e27cf4408cfe38e7f6da842e0884a48bd8fbcf5` |
| `raw-census-2.jsonl` | pass 2, byte-identical to pass 1 | same as above |
| `descriptions-r40.json` | `hyprctl descriptions -j` bytes | `4aa2745c11b92d36abbf5355f2dc9217ed54e143a2f0621e0cc7a2b3e2652aab` |
| `not-in-capture.tsv` | 283 non-declared names, form/set/value | `47362ef8585b5428d8f03b72ef58338ae69001b91c5a49295d81efadd600bab9` |
| `summary.json` | machine summary (counts, anomaly lists) | `5a2ba509fde2e1b575906c737fa8de7fb099d47ede76b9bca73ec15c6520341a` |
| `summary.md` | human summary + boundary | — |

`forms.tsv` hygiene: every row has exactly 3 tabs, no value contains a tab or newline, 4 `str`
values are legitimately empty (`general:locale` set=false; `input:kb_model`, `input:kb_variant`,
`input:kb_rules` set=true) — a real empty-string reply, not a parse failure.

Nothing outside the seat directory was written. Scratch dir `/tmp/aof.6pZHi3` removed after use.
No tool installed or updated (stdlib `python3` + the host's `hyprctl` only).

## Risks / limits (declared, not hidden)

- **Single host, single state, single moment.** `set` mirrors the loaded config; a different host
  config would move the 70/283 split (not the form vocabulary of the unset options).
- **All six `vec2` keys are `set: false`.** A *set* `vec2` value was never observed, and producing
  one needs a compositor mutation, which is out of bounds for this seat. That a set `vec2` prints
  `[x, y]` under the same form is `[INFERENCE]`.
- **`CONFIGDATATYPE_EMPTY` was never observed** as a reply form (0 keys without a form), so the
  theoretical sixth shape is unmeasured.
- **No source-level completeness check beyond 50 names.** Only headers are installed — no
  `HyprCtl.cpp`, no `ConfigValues.cpp` — so the type→form emitter was not read. The 50 names
  quoted in `ConfigValues.hpp` are all inside the 353; the authority for the 353 is
  `descriptions -j` itself (the compositor's own registry).
- The counter run at the freeze rev is a read-only scoring run and writes nothing; its
  `TARGET_MISSED` is the declared base state, not a defect I introduce.

## Blockers

None.
