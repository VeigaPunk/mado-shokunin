# SimpContract — dead weight in the C1 contract and code (round 46, w1)

Target: `.ufo/waves/round-46/l1-draft/mado-devices.py` (frozen reference), sha256
`b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` (also pinned as `MODEL_SHA256` in
`quality/counters/c1-r46-devices.py:67`). Nothing in the lane tree was edited: this seat wrote only
`.ufo/waves/round-46/w1/SimpContract*` and its scratch dir.

Question asked per sentence/branch: **is there an input that makes the output depend on it?** A branch with a
witness is load-bearing regardless of how unlikely the input is; a branch with no witness inside its own condition
is dead and is deleted.

## 1. Method

67 one-anchor variants of the reference (each replaces exactly one branch/condition/guard with its deletion or a
1-token change, anchored so the text occurs exactly once), compared against the reference on

* 81 fixture cases rebuilt from `quality/counters/c1-r46-fixtures.json` (names substituted with `names(46)`),
* 3,992 generated cases from the counter's own `gen_case` (4 seeds),
* 2,436 hand-built cases (every config × a dump matrix that includes non-string names, extra non-list keys,
  non-object list elements, NaN/Infinity/`belongsTo` variants, virtual and fallback keyboards),
* 23 **file-level** cases through real processes: argv shapes, missing/dir/FIFO/`/dev/null` paths, stdin, >1 MiB
  dump and config, 100k-deep JSON, bad UTF-8, a dump without `mice`, a symlinked config.

Total 6,509 in-process comparisons + 23 file-level per variant. Recorded in `witnesses.txt` (one killer witness per
live variant), `variants-summary.txt`, `dead-pairs.txt`, `differential.out` (reference vs simplified), `proofs.out`.

Reproduce (harness copied into this seat dir; scratch root is the only path used):

```
cd /fast/scratch/hyaku/mado-r46/SimpContract
python3 probe2.py                 # all variants, LIVE/NO-DIFF + killer witness
python3 witnesses.py              # compact per-variant witness table
python3 proofs.py                 # unreachability proofs P1-P5
python3 diff_check.py             # reference vs mado-devices-simplified.py, 6509 + 23 cases
```

Verdicts: **54 variants LIVE**, 13 NO-DIFF. Of the 13: five are the deletions below, one (`V52`) is dead test data,
five (`V58`, `V42b`, `V39b`, `V40b`, `V41b`) are live **only** at the file level (FIFO open, 100k-deep JSON, argv
shapes, a dump without `mice`), one (`V49`) is an equivalent rewrite, and `V53` is a deliberate no-op anchor
(identity control that must print NO-DIFF).

## 2. Direct answers to the four suspected spots

| suspect | verdict | witness (reference vs variant) |
|---|---|---|
| `else: st.device(bracket)` for unknown fields (lines 290-291) | **LIVE** | `device[logitech-keyboard]:output = DP-1` (fixture `matched-touch`): ref `keys=0 MATCHED` vs variant no `MADO_DEV_BLOCK` line at all (V10, 602 cases) |
| `cur is False` paths (lines 296-303) | **LIVE** (three independent ways) | `device {\n kb_layout = de\n name = k\n}`: ref `unsupported=2 blocks=0` vs variant without `cur = False` `unsupported=1 blocks=1` (V15); `device {\n kb_layout=de\n kb_options=x\n}`: ref `unsupported=2` vs variant `KeyError: False` (V14); rename: `device {\n name=a\n name=k\n kb_layout=de\n}` ref `unsupported=2` vs variant `unsupported=1` + block `a` gains `kb_layout` (V16) |
| FLT_MIN check vs `isinf` (line 216) | **LIVE, both conjuncts** | `isinf`: `device[m]:scroll_factor = 1e39` ref `NOT_COMPARED` vs variant `DIFFER` with `scroll_factor=100.00` (V09); `x < FLT_MIN`: `1.17549430e-38` ref `NOT_COMPARED` vs variant `DIFFER` (V08) |
| `if not isinstance(lst, list):` in `dump_names` (line 328) | **LIVE** | an extra top-level key that is not a list (`{"extra_key": null}` / `"abc"` / `7`): ref `OK`, variant `TypeError: 'NoneType' object is not iterable` / `AttributeError` (V05, V04) — the contract admits "any top-level list of the dump", so a dump may carry arbitrary other keys |

So all four are load-bearing; none may be deleted. The dead weight is elsewhere (§3).

## 3. Deletions made (5), with proof and exact text

The result is `mado-devices-simplified.py` (sha256
`7a3fa6120e64ff8b4f365f999380fb3a9f1e687ac7bc8230768e8c243eb64372`); the whole change is
`simplified.diff` and is 6 hunks totalling 5 deleted lines.

### D1 — `rb != -1` in the bracket condition (line 270)

```
-        if lb != -1 and rb != -1 and lb < rb:
+        if lb != -1 and lb < rb:
```

* `witnesses.txt`: `V01-bracket-rb-conjunct NO-DIFF` over 6,509 + 23 cases.
* `dead-pairs.txt` D1: 231 adversarial pairs (keys carrying `]` with no `[`, `][`, `[a]b`, `[]`, flat and
  in-block) — 231 identical.
* Proof (`proofs.out` P1): if `lb != -1` then `lb >= 0`; if `lb < rb` then `rb > lb >= 0`, hence `rb != -1`.
  The conjunct is implied by the two it sits between; brute force over all 137,257 strings of length ≤ 6 over
  `"[]:dk_ "` finds 0 counterexamples.
* The neighbours are load-bearing and stay: dropping `lb != -1` (V02) and dropping `lb < rb` (V01b) both change
  output — `device:kb_layout][ = fr` gives ref `unsupported=1 blocks=0`, `NOT_COMPARED` vs V01b `blocks=1` (an
  empty-named device) `unsupported=0`, `STALE_BLOCK`.

### D2 — the `isinstance(..., str)` guard on the reported names (line 371)

```
-        rep = tuple(kb.get(n) if isinstance(kb.get(n), str) else None for n in NAMES)
+        rep = tuple(kb.get(n) for n in NAMES)
```

* `witnesses.txt`: `V03-kb-rep-isinstance NO-DIFF`; `dead-pairs.txt` D2: 2,838 pairs (dumps whose layout/variant/
  options/model/rules are `5`, `null`, `["us"]`, `true`, `1.5`, `NaN`) — identical.
* Proof (`proofs.out` P2): `rep` has exactly two readers — `[n for n, e, r in zip(NAMES, exp, rep) if e != r]` and
  `rep == FALLBACK`. Every element of `exp` is a `str` (device-block/global values are `str`; defaults are
  `"us"`/`""`), and `FALLBACK` is all-`str`. For a non-`str` JSON scalar or container `r`, `e != r` is `True` for
  every `str` `e`, exactly as for `None`; and a tuple holding a non-`str` never equals `FALLBACK`, exactly as a
  tuple holding `None`. Checked over 124,416 (expected-tuple, reported-value) pairs: 0 counterexamples.
* Contract sentence retained verbatim in behaviour: "a missing or non-string value never equals an expected name".

### D3 — `"\n"` in `WS` (line 100)

```
-WS = " \t\r\n\v\f"
+WS = " \t\r\v\f"
```

* `witnesses.txt`: `V24-WS-no-newline NO-DIFF`; `dead-pairs.txt` D3: 2,838 pairs.
* Proof (`proofs.out` P3): `parse_config` starts with `text.split("\n")` (line 245) and `join_continuations`
  concatenates raw lines without inserting a separator, so every line later handed to `strip(WS)` is
  newline-free by construction; 200,000 random texts over `"\n\r\t\v\f ab#=\\{}[]$"` produce zero lines
  containing `"\n"`.
* `"\r"` in `WS` must stay: `input:kb_layout\r# c` is live (a CR before a comment is interior after the first
  `strip(" \t\r")`, survives the comment cut and is removed only by `strip(WS)`), `witnesses.txt` V20.

### D4 — the sign of the overflow infinity in `f32` (line 121)

```
-        return math.inf if x > 0 else -math.inf
+        return math.inf
```

* `witnesses.txt`: `V43b-f32-sign NO-DIFF`; `dead-pairs.txt` D4: 132 pairs including `-1e39` and `-1e46`.
* Proof (`proofs.out` P4): `f32` has one call site (line 215) and its value is consumed only by `math.isinf(v)`
  (line 216) — `+inf` and `-inf` take the same branch, so the sign is unobservable. (`f32`'s rounding is live and
  stays: V43 shows 249 cases where dropping the float32 round-trip changes output, e.g. `0.335`.)
* If a later contract ever reads the parsed value instead of only testing `isinf`, this deletion must be reverted.

### D5 — three copies of `st.device(bracket)` hoisted to one (lines 283-291)

```
         if bracket is not None:
+            st.device(bracket)
             if field in DEVICE_KEYS:
-                set_device_key(st.device(bracket), field, rhs, st)
+                set_device_key(st.devices[bracket], field, rhs, st)
             elif field == "name":
-                st.device(bracket)
                 st.unsupported += 1
-            else:
-                st.device(bracket)
```

* `witnesses.txt`: `V12-bracket-hoisted NO-DIFF`; `dead-pairs.txt` D5: 165 pairs over all bracket shapes.
* Proof by equivalence: all three arms perform `st.device(bracket)` first (`set_device_key(st.device(...))`
  evaluates it before the call), so creation order and effects are unchanged; `st.devices[bracket]` is safe
  because the hoisted call just created the key. This removes a duplicated authority, it does not change it.

## 4. Branch census (what stays, with its witness)

`witnesses.txt` names the first differing case for each; counts are cases differing out of 6,509.

**Constants.** `MAX_BYTES`/`WS` (D3)/`NAMES`/`INPUT_KEYS` (V27, 2,747)/`DEVICE_KEYS` (V13)/`DIRECTIVE_RE`
(`\b` V26; `[ \t]*` V26c, a tab after `#`)/`FLOAT_RE` (sign V57, exponent V56)/`SPECIAL_RE` (`[+-]?` V45,
`re.I` V55)/`EMPTY` (V37, 173)/`FALLBACK` (V31, 1,490)/`VIRTUAL_PREFIX` (V30, 694)/`FLT_MIN` (V08, V09).

**`f32`** round-trip V43 (249); sign D4. **`read_regular`** `O_NONBLOCK` V58 (FIFO: ref `SETUP unreadable`, variant
hangs); `S_ISREG` (fixtures `setup-config-dir`, `devices-dir`, `/dev/null`); >`MAX_BYTES` (fixtures
`setup-dump-too-large`, `setup-config-too-large`); `OSError`→unreadable (fixtures `setup-missing-file`).
**`read_stdin`** bound (file case `stdin-too-large`). **`parse_args`** `--devices` once (V39b file-level:
`SETUP usage` vs `SETUP unreadable`), odd argv (V40b: `SETUP usage` vs traceback), `--selftest` alone
(file case `selftest-extra`).

**`join_continuations`** final-line drop (V21), `rstrip` (V22). **`cut_comment`** `##` pairing and resume point
(V25: `resume = pos + 3` differs; comment-escape fixtures). **`read_float`** SPECIAL-before-FLOAT (V45/V55),
prefix match (V56/V57), no-prefix unset (`mouse-stof-none`), `isinf`/`FLT_MIN` (V09/V08), `unsupported` counter
(V13, 676).

**`parse_config`** first strip (V20), comment skip and directive count (V26b), whitespace strip incl. `\r` (V20),
`}` pop with `if stack` (V39, stray `}` → `IndexError`), `cur = None` on empty stack (V17, 857), `{` push with its
strip (V23, 3,567), empty-LHS skip (V18: `device { = $x }` → ref silent vs variant `unsupported+1`), `$`-LHS skip
(V19), KEY join (V29, 2,629), bracket `lb != -1` (V02) and `lb < rb` (V01b), relevance filter (V27),
`$`/`{{`/`\` unsupported, `device:` guard (V28), bracket DEVICE/name/other arms (V11, V10, D5), flat select
(fixtures `device-block`), no-current device (V15), `cur is False` guard (V14), device-key write (V49 equivalent: `cur` is only ever set
right after `st.device(rhs)`, so `st.device(cur)` cannot create a block and equals `st.devices[cur]`), rename (V16).

**`parse_devices`** UTF-8/JSON `RecursionError` (file case `dump-deep`: `SETUP bad_json` vs traceback), object
check (fixture `setup-not-object`), both lists (V41b file-level `dump-no-mice`: `SETUP bad_json` vs traceback),
element `dict` + `name` `str` (V51b: numeric name → `AttributeError`).

**`dump_names`** list guard (V05), element guard (V04), element-name `str` (V06c: `KeyError`), `belongsTo` `dict`
guard (V06/V06d: `AttributeError` when a tablet has no `belongsTo`), `belongsTo` name `str` (V06b: unhashable name
→ `TypeError`). **`expected_names`** `.get` (V48: 4,560), `EMPTY` (V37), default layout (V38, 3,413), `kb_file`
(`file` fixture). **`is_num`** bool exclusion (V35), `isfinite` (V36).

**`report`** VIRTUAL-first order (V30), FALLBACK-after-AGREE order (V31), clamp (V33), two-decimal *string*
comparison (V34: numeric equality differs in 26 cases), `reported=?` (V35), `dump_names` for presence (V44: 152,
tablet/touch owners), stale count (V46, 2,023), `differ` separator `,` (V47), NOT_COMPARED first (V50, 1,569),
NO_KEYBOARDS branch (V32, 431). **`main`/`run`** `lines is not None` (selftest prints its own lines; file cases).

Not probed because they are not branches: the docstring (the contract, untouched), the output literal formats
(pinned by 90 fixtures), the selftest's case table (test data; see §6).

## 5. Finding outside dead weight — the `v != 0.0` guard contradicts both the docstring and the pin

Line 216 reads

```
    if math.isinf(v) or (v != 0.0 and abs(float(m.group(0))) < FLT_MIN):
```

The `abs(float(m.group(0)))` form is **right** and the `v != 0.0` guard is **wrong**, for the same reason: this
host's `std::stof` underflow boundary is the decimal magnitude, not the rounded float. `stof-grounding.txt`
(compiled on this host: `g++ -O0 -std=c++20`) shows `1e-46`, `-1e-46`, `1e-45`, `1e-40`, `1.17549428e-38`,
`1.17549430e-38`, `1e39` all **throw**, while `0x10`, `0.335`, `5.`, `.5` return values. hyprlang wraps that call
in a try/catch that turns a throw into a parse error (`fetch/hyprlang-config.cpp:466-471`).

Consequence of the guard: `device[m]:scroll_factor = 1e-46` → `f32` = `0.0`, guard skips the range check, the
reference stores `0.0` with **no** `unsupported` flag and prints `scroll_factor=0.00`; the docstring says "a nonzero
value below 2\*\*-126 in magnitude adds one to `unsupported`", and the pin rejects the line. Witness pair
(`witnesses.txt`, V07): dump `scrollFactor: 0.0` → ref `AGREE / OK` where the compositor rejected the line
(expected would be unset → `-1.00`, or `NOT_COMPARED`).

This is *live* code, not dead weight, so it is **not** in the simplification. It is a contract defect for the L1:
the one-line fix is to delete `v != 0.0 and`. No fixture and no `FACTORS` value reaches the underflow-to-zero region
(`1e-40` and `1e39` throw on both readings), so C1 clause f/g cannot see it — this is exactly the declared residual
"a contract error shared by reference and tool is invisible to it".

The `0x` arm of `SPECIAL_RE` is the opposite direction (the pin returns 16.0 for `0x10`, the reference marks it
unsupported): conservative and declared in the docstring, leave it.

## 6. Test-data dead weight (optional)

`kb()` (line 427) carries `address`, `active_layout_index`, `active_keymap`, `capsLock`, `numLock`, `main`;
`mouse()` (line 433) carries `address`, `defaultSpeed`. `report()` reads only `name`, the five keyboard names and
`scrollFactor`. `V52-selftest-unused-kb-fields` deletes the unread fields: selftest still `48/48`, 0/6,509 output
difference. Tradeoff: keeping them documents the real `hyprctl devices -j` shape, deleting them makes the selftest
say only what it checks. Harmless either way; no recommendation.

## 7. Retained contract and score

* `selftest.out`: reference `48/48`, simplified `48/48`, rc 0.
* `differential.out`: reference vs simplified — 6,509 in-process cases, 0 differing; 23 file-level cases,
  0 differing (rc, stdout and stderr-presence all equal).
* Frozen counter on a scratch clone of the freeze with the simplified tool at `tools/mado-devices.py`:
  `counter-simplified-4601.txt` and `counter-simplified-777.txt` — `fixtures=90/90 generated=150/150 selftest=ok
  readonly=ok tool=present verdict=TARGET_MET` (two nonces). Control with the unmodified reference tool at the
  same nonce: `counter-reference-4601.txt` — same line, `TARGET_MET`. The counter's `MODEL_SHA256` pin is
  untouched, so clause g still judges against the frozen contract.
* The deletions remove no docstring sentence: every behaviour the contract states still holds on both sides of the
  differential (the only sentence whose *code* disagreed with it, §5, was left alone).

## 8. Tradeoffs and limits

* D1/D2/D3/D4 are invisible to anything that compares output; they are only found by reading the condition and
  proving reachability, so the proof (not the corpus) is the evidence, and the corpus is the falsification attempt.
* D4 trades nothing today; it is the one deletion that would have to be reverted if a future contract starts
  reading the parsed float instead of testing `isinf`.
* D2 slightly weakens debuggability (a non-string reported name is no longer normalised to `None`), with no
  observable difference; keep it if the L1 prefers the guard as documentation, but then note it is not load-bearing.
* Not measured: whether the *host's* `std::stof` is what hyprlang links at runtime (libstdc++ here, verified by
  compiling against it); a toolchain swap could move the underflow boundary in §5.
* Clause-r soundness raised by another seat (absolute-path execs, AF_UNIX) is outside this seat; the simplified
  tool imports only `json, math, os, re, stat, struct, sys` and starts no process and no socket, so it neither
  depends on nor widens that hole.
