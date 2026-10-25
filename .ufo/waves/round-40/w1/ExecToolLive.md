# ExecToolLive — C1 deliverable candidate: production `--live` tool

Seat: `w1/ExecToolLive` (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Freeze read first: `.ufo/waves/round-40/registration.md` (freeze `5e7e88525cc539563de7746361b2650802e81809`,
base `9fc511ddce708327377161202f358ce37dc266ba`). C1 target: `fixtures=13/13 verdict=TARGET_MET`, clause b
`k == n >= 79`, clauses a/g/k hold.

## Files written (all inside this seat dir; no tracked file touched)

| path | what |
|---|---|
| `.ufo/waves/round-40/w1/ExecToolLive/mado-options.py` | **DELIVERABLE candidate**, 1698 lines, sha256 `9cf9ae88a8eb077bfe60f6cd034877f5d8d0b94f4abfb8b524356a5620ab4e39` |
| `.ufo/waves/round-40/w1/ExecToolLive/base-mado-options.py.txt` | copy of BASE `tools/mado-options.py` (1050 lines, sha256 `461f8c3c245bdfb6dcaac068a5ab378326c75dc91992b8012f9ca0e5019fb03a`, selftest 71/71) |
| `.ufo/waves/round-40/w1/ExecToolLive/ctl-ref-tool.py.txt` | copy of the CONTROL reference (sha256 `f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa`); never delivered |
| `.ufo/waves/round-40/w1/ExecToolLive/live-host-census.txt` | out-of-distribution census receipt (see §4) |
| `.ufo/waves/round-40/w1/ExecToolLive.md` | this report |

`git status --porcelain` in the lane: 0 tracked files modified (only the wave's own untracked `.ufo/` dirs).
No `pacman`, no package transaction, no compositor mutation, no socket of my own; the only compositor verb run
was read-only `hyprctl version` and `hyprctl getoption -j` (through the tool and through the control).

## 1. What the candidate does (contract as implemented)

Added to BASE, in five contained hunks (docstring, `declared_angle` + angle bookkeeping in `State.declare`,
the live section, `main` wiring, selftest helpers/block). BASE behaviour of the static table and of
`--getoption FILE` is untouched (byte-identical output, §3).

- `--live`: one `HYPRCTL getoption -j KEY` per declared key, once, nothing else on the argv; rows get
  `agreement` (`agreement`, `agreement*`, `mismatch`, `config-only`) plus `live` (native value as text, `null`
  for `config-only`).
- `--hyprctl PATH` (default `hyprctl`): the program to run.
- `--probe KEY` (repeatable): extra live keys with no declarer → `live-default` (row `owner/layer/line = null`,
  `value` and `live` = the native text, `set` carried); a probe the compositor answers `no such option` is
  dropped; a probe naming a declared key is not queried twice.
- Native forms: one JSON object `{"option":K,"set":B,"<form>":V}` with exactly one of `int|float|str|custom`,
  or the text line `no such option` (exit 0) → `config-only`.
- Conversion: `int` = hyprlang v0.6.8 `configStringToInt` (`0x` hex; `rgba(rrggbbaa)`; `rgba(r,g,b,a)` with
  alpha×255 rounded; `rgb(rrggbb)`; `rgb(r,g,b)`; prefixes `true/on/yes`→1, `false/off/no`→0; signed decimal);
  `float` = 1e-6 numeric; `str` = exact trimmed; `custom` by the reply's own shape — gradient
  (`<argb hex>… <N>deg`, angle inherited from the previous declarer when the redeclaration carries no `deg`
  token), CSS gap (`a b c d`, 1–4 declared integers), font weight (name → 100…1000, case-insensitive).
- Exit 5, naming the key, on: program missing / non-zero exit / non-JSON reply / object without exactly one
  known form or without `set`. Exit 2, before any program runs, on a probe key that is empty or starts with `-`.
- Stdlib only: `argparse glob json os re shutil stat subprocess sys tempfile` (no `socket`/`urllib`/`http`/`ssl`).

`--selftest` grew 71 → **144** assertions and now builds a stub `hyprctl` (shebang, `0755`, `table.json`,
`mode`, `calls.log`) inside its private `mkdtemp` dir. It covers: the four native forms + `no such option`;
every `int` spelling (0x, rgba 8-hex, rgba(r,g,b,a), rgb 6-hex, rgb(r,g,b), true/on/yes, false/off/no,
negative, decimal); float 1.50≡1.5; str; gradient with a declared angle, without an angle (→ `0deg`), and with
an inherited angle (→ `agreement*`, the host's `rgb(e68e0d)` after `…45deg`); gap 1/2/3/4 and a gap mismatch;
font weight lowercase / UPPERCASE / mismatch; value-differs, `set=false`, str-differs; `config-only` with
`live=null`; shadowed declarer keeps the last declaration; probe `live-default` + no-owner + `set` + native
`value` + unknown-probe-dropped + declared-key-not-duplicated; exact argv (`getoption -j KEY`, one call per
declared key and probe, no duplicates); config root unchanged (path/size/mtime listing); exit 5 for compositor
exit / malformed reply / unknown reply form / missing program (each naming the key); exit 2 for `-x`,
`--version`, `""` with **no** program run; `--live` without `--home` = 2; and the static path emitting neither
`agreement` nor `live`.

## 2. Required outputs, verbatim

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ python3 -I .ufo/waves/round-40/w1/ExecToolLive/mado-options.py --selftest
MADO_OPTIONS_SELFTEST: 144/144 passed
rc=0
```

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live.py --repo . --rev 5e7e88525cc539563de7746361b2650802e81809 --tool .ufo/waves/round-40/w1/ExecToolLive/mado-options.py
PRED-C1-r40-v1 clause=b rc=0 selftest=144/144
PRED-C1-r40-v1 fixture=gen0 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen1 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen2 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen3 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen4 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen5 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen6 ok=1 rows=15
PRED-C1-r40-v1 fixture=gen7 ok=1 rows=15
PRED-C1-r40-v1 fixture=probe0 ok=1 rows=17
PRED-C1-r40-v1 fixture=fail0 ok=1 rc=5 named=1
PRED-C1-r40-v1 fixture=bad0 ok=1 rc=5 named=1
PRED-C1-r40-v1 fixture=missing0 ok=1 rc=5
PRED-C1-r40-v1 fixture=hostile0 ok=1 all three refused=1
PRED-C1-r40-v1 clauses=a:1 b:1 g:1 k:1
PRED-C1-r40-v1: fixtures=13/13 tool=present verdict=TARGET_MET rev=5e7e88525cc539563de7746361b2650802e81809
rc=0
```

Clauses a, b (144 ≥ 79), g and k all hold; 13/13 fixtures. The frozen counter and the control were not edited.

## 3. Paths kept unchanged (byte-level evidence)

BASE vs candidate, same trees, `cmp` on stdout+stderr+exit:

- `--getoption FILE` on a tree with 33 declared keys and an 8-key live JSON (incl. `custom` gradient and an
  extra `live-default` key): **identical bytes**, both rc 0.
- static `--home` on that same tree: **identical bytes**.
- three layered trees (sources/variables/glob toggles/nested categories/`##` escape/continuation/`{{1 + 1}}`/
  `# hyprlang if`) plus a recursive-source tree: **identical bytes and identical exit code** in all four cases
  (11, 10 and 1 rows at rc 0; the recursive-source tree rc 3 on both, stderr
  `mado-options.py: recursive source: …/hyprland.conf`).

## 4. Out-of-distribution check on the running host (read-only, reported not scored)

Receipt: `.ufo/waves/round-40/w1/ExecToolLive/live-host-census.txt`.

```
# host: Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f
# exit=0 stderr_bytes=0
# rows=70
# labels: agreement=62 agreement*=8
# mismatch rows: 0
# agreement* keys: decoration:rounding general:border_size general:col.active_border general:gaps_in
#                  general:gaps_out group:col.border_active input:kb_layout input:kb_options
# live field == committed capture for all 70 keys: True
# label map identical to the reference control: True
# live map identical to the reference control: True
```

So: the candidate reproduces the claim's provisional host census (62/8/0) on the real compositor, its `live`
field equals the committed `.ufo/waves/round-40/c1/native-capture.jsonl` value for all 70 keys, and its label
and live maps are identical to the reference control's on real data (the counter's fixtures cannot see the
host, so this is the model-vs-host check).

## 5. Deliberate divergences from the control (all outside the scored fixtures, documented in the docstring)

1. `native_query` checks `isinstance(reply, dict)` **before** probing for form keys; the control computed
   `f in rec` first (a JSON list reply would still be refused, but by a type-unsafe path).
2. Decimal `int` uses `re.fullmatch(r"-?\d+")`; the control's `lstrip("-").isdigit()` + `int()` raises
   `ValueError` on `"--3"` instead of returning "not an int".
3. `gap_text` returns "no match" for counts other than 1–4 (the counter docstring's contract). The control
   truncated to the first four values, so a 5-value declaration could match a 4-value reply.
4. An unparsable `deg` token yields "no match" instead of raising.
5. `--probe` keys beginning with `-` are refused by argparse (exit 2, message names `--probe`) before the
   tool's own empty/`-` check runs; both refuse before any program runs, which is what the counter asserts.

## 6. Risks, handoff notes, blockers

- **Integration is the L1's**: copy the candidate to `tools/mado-options.py`; the C2 own-work receipt must then
  repeat that committed file's sha256 (`9cf9ae88a8eb077bfe60f6cd034877f5d8d0b94f4abfb8b524356a5620ab4e39` if
  copied verbatim) — I did not write any tracked path.
- **Declared residual** (registration): a tool hardcoding the reference model's tables for the generator's
  value space passes; §4 is the reported OOD evidence, not a scored receipt.
- **Historical predicates**: `quality/counters/c4-r39-options-entry.py` clause e binds the S219 receipt to the
  sha256 of `tools/mado-options.py` **at REV**, so re-scoring that round-39 predicate at a new tip will see a
  different tool sha. Pre-existing predicate variance, not remediated here. `c3-r39-options.py` needs
  `n >= 40` (candidate: 144) and its static/`--getoption` paths are byte-identical to base on 4 trees, but I
  did **not** run it (an unrun check is not a pass; it has no `--tool` flag and scoring it needs the lane
  history).
- **Not run here**: `tools/mado-verify.sh --selftest` (460/460 harm-watch line) and `check-index.py` /
  `check-axis-scores.py` — none of them read this seat dir; the L1 runs them post-integration.
- No installs or updates were made (nothing needed); no blockers.
