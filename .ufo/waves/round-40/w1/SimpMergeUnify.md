# w1 seat SimpMergeUnify — one labeller for the reference `--live` merge (round 40)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · freeze `5e7e88525cc539563de7746361b2650802e81809`
· base `9fc511ddce708327377161202f358ce37dc266ba`.

Artifact: `.ufo/waves/round-40/w1/SimpMergeUnify/unified.py` — a copy of the CONTROL
`.ufo/waves/round-40/c1/ctl-ref-tool.py.txt` with **one** merge and **one** labeller.
Evidence in the same seat dir: `parity.py`/`parity-receipt.txt` (BASE↔unified and
REF↔unified byte parity), `rejected-design-a.py`/`.txt` (why `values_equal` cannot go),
`merge.diff` (the whole change), `selftest-receipt.txt`, `counter-receipt.txt`. Nothing outside
the seat dir was written; no tracked file was edited; no install was made (no tool needed).

## What the reference duplicated, and what I deleted

The reference carried two copies of the same merge: `merge_rows` (file source, 24 lines) and
`merge_live` (compositor source, 29 lines). Both repeated the four label rules, the
`live-default` append and the sort. In `unified.py`:

- **deleted `merge_live` (29 lines) and the old `merge_rows` (24 lines)** → one `merge_rows`
  (37 lines) + `label` (5 lines): `label(equal, isset, decls)` is the only place the
  agreement vocabulary exists; `merge_rows(rows, options, source, extra=(), record_live=False,
  equal=native_equal)` is the only place rows are labelled, `live-default`-appended and sorted.
- **deleted the per-source record assembly** (`file_source`/`ctl_source` closures and the
  `live.items()` loop): both sources now hand the merge the same `(form, value, set)` through
  `source(key)`. The file source is `load_live(...).get` (the loader owns the shape);
  the compositor source is `lambda key: native_query(args.hyprctl, key)`.
- **`load_live` returns `(custom_type, value, bool(set))`** instead of the raw dict, so the
  record shape is defined once, next to the validation that guarantees it.
- **`values_equal` accepts the merge's shared call shape** (`*_angle`, documented as unused:
  the file mode carries the angle inside the value), so both comparisons are
  `equal(form, declared, live, angle)` and `merge_rows(..., equal=values_equal)` needs no
  adapter.
- `record_live=True` is the only remaining source difference: the compositor mode also copies
  the live value into `live` (and `live: null` on `config-only`), the file mode does not —
  that is exactly the BASE tool's row shape.

Line counts (`ast` end-lineno, and `wc -l`):

| unit | reference | unified |
|---|---|---|
| merge machinery (`merge_rows` + `merge_live`) | 24 + 29 = **53** | `merge_rows` 37 + `label` 5 = **42** |
| `load_live` | 17 | 18 (docstring) |
| `values_equal` | 19 | 21 (docstring) |
| whole file | **1217** | **1211** |

`merge.diff`: 45 lines removed, 39 added. The −6 line delta understates the change: the point
is that the label rules, the `live-default` assembly and the sort now have a single authority,
so the two modes can no longer drift apart.

## Preserved contract (behaviour, not shape)

`unified.py` keeps `values_equal` **and** `native_equal`. They are not duplicates: they are the
two frozen models (the `--getoption` file vocabulary vs the native-form model). The BASE
selftest's own fixtures prove it — see the rejected candidate below.

Checks run (all from the lane, read-only):

1. `python3 -I .ufo/waves/round-40/w1/SimpMergeUnify/unified.py --selftest` →
   `MADO_OPTIONS_SELFTEST: 71/71 passed` (same k as the reference; the base's 71).
2. `python3 -I quality/counters/c1-r40-live.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin
   --rev 5e7e88525cc539563de7746361b2650802e81809 --tool .ufo/waves/round-40/w1/SimpMergeUnify/unified.py`
   → `fixtures=13/13 tool=present verdict=TARGET_MISSED`, `clauses=a:1 b:0 g:1 k:1`
   (13/13 is this seat's bar; the overall `TARGET_MISSED` is clause b's `k >= 79` selftest
   requirement, which the reference control misses too — not my ticket).
3. `python3 -I .ufo/waves/round-40/w1/SimpMergeUnify/parity.py` → `PARITY: PASS (0 failures)`,
   26 `OK` lines. Byte comparisons of stdout, BASE = `git show REV:tools/mado-options.py`:
   - S1 `--getoption` on the **BASE selftest's own fixture tree + live.json** (captured by
     running the base selftest with `mkdtemp`/`rmtree` patched): `4894/4894` bytes, 28 rows,
     labels `agreement, agreement*, config-only, live-default, mismatch` all present.
   - S2 `--getoption` on the counter's 8 generated trees + the probe tree, dumped as
     native-typed records: `2360/2360`, `2362/2362`, `2316/2316`, `2327/2327`, `2360/2360`,
     `2380/2380`, `2345/2345`, `2345/2345`, `2638/2638` bytes.
   - S4 `--getoption` on the **host tree** with `c1/native-capture.jsonl` as the file dump:
     `12940/12940` bytes.
   - S5 `--live` REF vs UNI on the same 9 trees through the counter's stub compositor:
     `2667/2667`, `2655/2655`, `2599/2599`, `2604/2604`, `2652/2652`, `2704/2704`,
     `2639/2639`, `2632/2632`, `2961/2961` bytes.
   - S6 `--live` REF vs UNI on the **host tree** replayed from the 70-line capture through a
     stub `hyprctl` (no compositor contact): `14066/14066` bytes, labels
     `{agreement: 62, agreement*: 8}` — the same 62/8 the claim's residual states.
   - S7 `--getoption` + `--live` together on the host tree: `14066/14066` bytes.
   - S8 exit 5 on a failing stub: both `rc=5`, byte-identical stderr naming the key.
   - S9 exit 2 on `--probe -x`: both `rc=2`, byte-identical stderr.
4. No compositor verb was run by me except through the stub; no write outside the seat dir and
   `/tmp` scratch (cleaned); `git -C . status --porcelain` shows only `.ufo/waves/round-40/*`
   untracked seat output.

## Deletion candidates found and rejected (each with evidence)

- **Fold the file mode into `native_equal` and delete `values_equal`** (the only way to make
  the two merges share one *comparison*, not just one labeller). Rejected: it changes the
  frozen file-mode vocabulary. `rejected-design-a.py` builds exactly that variant (the default
  `equal=native_equal`) and diffs it against BASE:
  - the **BASE selftest's own fixtures**: not byte-identical, `4894/4887` bytes, 5 flips —
    `misc:disable_autoreload agreement→mismatch` (declared `true`, live `"1"`),
    `decoration:shadow:enabled agreement→mismatch`, `general:border_size agreement*→mismatch`,
    `decoration:rounding agreement*→mismatch`, `input:repeat_rate agreement→mismatch`
    (the file's `int` values are JSON strings, `hl_int("true") == "1"` is false).
  - the 9 counter dumps: 6 flips each, 54 total.
  - the host capture dump: 14 of 70 flips (`general:col.active_border mismatch→agreement*`,
    `group:groupbar:font_weight_active mismatch→agreement`, …).
  So the "one comparison" version fails the ticket's own byte-identity bar; the two compares
  stay. Tradeoff accepted: one shared labeller and one shared row path, not one comparison.
- **Merge `load_live` into `native_query`.** Both turn a transport into records, but they
  validate different key sets (`value/custom_type/set` vs `option/<form>/set`) and raise
  different classes/exit codes (`LiveError`→4, `CtlError`→5) with messages the base selftest
  asserts (`merge: non-object getoption fails` rc 4). The only shared part is the 3-tuple
  shape, which now lives in `load_live`. Rejected: a shared validator would need a
  key-convention parameter and would rewrite asserted messages.
- **Factor the `deg` token parse** shared by `State.declare` and `native_equal` (~4 lines
  each). Rejected: the two answer different questions. `declare` tolerates a malformed
  `xdeg` token (angle stays unset, `_cur` unchanged); `native_equal` must return `False` for
  it. A shared helper needs a tri-state sentinel (no token / angle / malformed), which costs
  more lines than it saves and hides the difference.
- **Express `hl_int`'s boolean prefixes through `truthy`.** `truthy` returns a bool and is
  `parse_line`'s predicate; `hl_int` must yield `0/1` **after** the `0x`/`rgba(`/`rgb(` forms
  and distinguishes `false/off/no` from "not a value". Sharing it would still need both
  `startswith` tests, so nothing is deleted; `hl_int` also has no BASE counterpart
  (`grep -n "rgba(" tools/mado-options.py` hits only the fixture text at line 647).

## Where I stopped

The next deletion that would shorten the file is the `record_live` flag (3 two-line branches).
It cannot go without a 4th element in the source tuple or a second merge: the file mode must
**not** emit `live` (BASE row shape) while the compositor mode must (`live: null` on
`config-only`, `live` on every other row), and a `None` record cannot carry that difference.
That is the axis boundary for this seat.

Checks the integrator should run on the delivered tool (not on this control):
`bash tools/mado-verify.sh --selftest` (460/460), `python3 -I tools/mado-options.py --selftest`
(n ≥ 79 for C1 clause b), and the C1 counter at the data commit.
