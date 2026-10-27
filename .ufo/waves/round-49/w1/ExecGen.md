# ExecGen — C1 clause g: nonce generator of (RMLVO, keysym) cases

seat: `ExecGen` (leaf executor, wave `w1` = BUILD) · date: 2026-10-27 · lane `mado-shokunin` @ base
`03e4ae76aff7a4be59cb69970dd553baa319695a` · run 9 of round 49.

Scope: build the generator that feeds clause g of the C1 counter — a nonce stream of
`(RMLVO, keysym)` pairs, drawn from a frozen snapshot of `xkbcli list` plus
`xkbcommon-keysyms.h`, judged at count time by the pinned `xkbcli-how-to-type`, and measured
against a naive "first match only, no modifiers" reader. No frozen predicate is scored here;
this is instrument construction for the L1's freeze.

## 1. Deliverables

| path (relative to this seat dir unless marked) | sha256 | what |
|---|---|---|
| `gen.py` | `e5de5f1b6cebca99c421a33bf6b550df81fe4321175d6dea4df0d6b22e210b5b` | the generator (Python 3 stdlib only) + judge-row parser + naive baseline + `--selftest` |
| `judge_run.py` | `4c78f48b78586944c5045db58fb45bd4abb259123953b757b7cec4daac61cb34` | seat-local harness: compile → judge → naive compare, N passes, digest, TSV/contrast receipts |
| `xkbcli-list.txt` | `2666867f599d0a0ca9c0047d011cc5f86012a66a4e141f59ca5b33a6bbe6c760` | frozen `xkbcli list` snapshot (5101 lines, clean env, stdout) |
| `xkbcommon-keysyms.h` | `13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3` | keysym header copy (pin) |
| `SHA256SUMS` | — | every file in this seat dir with its digest |
| `receipts/` | see `SHA256SUMS` | snapshot-check/stability, selftest, judge passes, census, determinism, contract facts, header sufficiency, contrasts, per-case TSV and the full 3-pass record JSON |

`gen.py` writes nothing and starts no process unless `--compile` is passed (then it runs only the
pinned `xkbcli-compile-keymap` and captures its stdout in memory). The judge harness writes only
under its `--work` dir, which it refuses outside `/fast/scratch/hyaku/mado-r49/` and refuses under
`/tmp` (SentScratch).

## 2. Pins

```
f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54  /usr/lib/xkbcommon/xkbcli-how-to-type
43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250  /usr/lib/xkbcommon/xkbcli-compile-keymap
13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3  /usr/include/xkbcommon/xkbcommon-keysyms.h
2666867f599d0a0ca9c0047d011cc5f86012a66a4e141f59ca5b33a6bbe6c760  xkbcli-list.txt (this seat)
libxkbcommon 1.13.2-1   xkeyboard-config 2.48-1          (pacman -Q, 2026-10-27)
```

`gen.py` verifies the snapshot and header digests on every load and aborts on drift; the harness
re-verifies both binaries before a pass. The snapshot was captured twice, each time in a fresh
clean environment, and compared byte-for-byte — both captures are 5101 lines with sha256
`2666867f…6c760`, `cmp: byte-identical` (`receipts/snapshot-stability.txt`).

## 3. What the generator draws

`gen_rmlvo(rng, snap)` — `rules` fixed to `evdev`; `model` from the 184 snapshot models (weighted
to the pc\* family, 20 % share over the other 178); `layout` from the 99 snapshot layouts (`custom`
excluded — it needs user symbols), weighted to a 40-layout preferred pool with a 2 % tail over the
rest; 15 % of cases draw two layouts (`--layout a,b`, variant empty); otherwise 45 % of cases draw a
non-empty `variant` that exists for *that* layout; 0–2 options, each from a distinct allowed group
(`lv2 lv3 lv5 altwin ctrl caps keypad kpdl Compose nbsp currencysign compat` — `custom`/`solaris`
compat rewrites, layout-specific `japan`/`korean`, `terminate` and the `grp*` no-ops on one layout
are excluded by policy, and the selftest proves every emitted option comes from the snapshot).

`gen_keysym(rng, present)` — 70 % weighted draw from the keysyms present in the case's compiled
keymap, 10 % uniform over the present set, 5 % uniform over the header (absent keysyms — the
"header only, zero rows" class), remainder numeric form (`0x..` or decimal; decimal never for
values 0–9, which the judge reads as names). Present-set weight is
`count + HARD_BONUS * hard_count` with `HARD_BONUS = 20`, where `hard` counts occurrences that are
not layout-1 level-1 — i.e. the draw is weighted by how many direct-access rows a reader has to get
right, not only by how often the symbol appears (`present_weighted(hard_bonus=0)` is the plain
occurrence weighting; the corpus can be regenerated that way with `--weighting plain`).

`gen_case(rng, present=None)` / `gen_case_with(rng, rmlvo, present=...)` / `iter_cases(seed, n,
compile_fn)` — the case is `{index, rules, model, layout, variant, options, keysym_arg,
keysym_name, keysym_value, keysym_form, keysym_draw, present_weighted, multi_layout, ...}`.
Draw order is fixed (RMLVO → compile → keysym), so a seed plus the compile function fixes the
whole list.

Keysym tokens are resolved through three forms the compiler actually emits, all measured:
header name (`slash`), Unicode keysym (`U2032` → `0x1002032`), raw unnamed value (`0x0100002b`).
That third form surfaced from `compat:misc:apl`/`keypad:oss_wang` keymaps and would have crashed a
naive name-only resolver (`KeyError: 'U2032'` in the first draft).

## 4. Judged runs — determinism

Canonical: `python3 judge_run.py --work /fast/scratch/hyaku/mado-r49/ExecGen/work --seed 4901
--n 400 --runs 3 --weighting difficulty` → `receipts/judge-400x3-difficulty.txt`:

```
run 1: weighting=difficulty cases=400 naive=79/400 (19.8%) digest=f03e29491fff9629
        rc0=400 rc_nonzero=0 zero_rows=18 single_row=154 multi_row=228
run 2: … naive=79/400 (19.8%) digest=f03e29491fff9629
run 3: … naive=79/400 (19.8%) digest=f03e29491fff9629
determinism: 1 distinct pass digests -> STABLE
```

The pass digest hashes every case's case-JSON sha, judge stdout sha and rc. Additional evidence:

- `receipts/corpus-census.txt` — the 3 passes produce identical keymap digests **and** identical
  judge stdout digests (400/400), so `xkbcli compile-keymap` is itself stable here;
- `receipts/gen-determinism.txt` — the case list alone is stable across three separate processes,
  `3c55eba0f4cc96d996a38ea10df246b9f5d1a816f39ee0159a37ed6ef88c9867` three times; a different
  seed gives `7da7c95b…`; `--weighting plain` gives `07e4529c…`; header-pool-only gives `fc6f1df9…`;
- a separate process at `--runs 1` reproduces `digest=f03e29491fff9629`;
- second seed 4917, n=60, 3 passes: `receipts/judge-60x3-seed4917.txt`, `9/60 (15.0%)`, one digest.

Corpus shape of the canonical run (400 cases): 340 distinct keymaps, 94 distinct layouts, 65
models, 159 cases with a variant, 191 with options, 52 two-layout cases, presence pool 472–727
keysyms (median 611). Judge row histogram: 0 rows ×18, 1 ×154, 2 ×112, 3 ×15, 4 ×26, 5 ×1, 6 ×3,
15 ×71; 228 cases need more than one row. Arg token classes: 331 names, 34 hex, 32 decimal,
3 U-names.

All 400 cases exit 0 (`rc_nonzero=0`). Rejection cases do not occur by chance — see §6 F4 — so the
counter should carry **fixed** reject fixtures (`nosuchsym`, `SLASH`, `0x0`) instead of expecting
the nonce stream to produce one.

## 5. Naive baseline — "first match only, no modifiers"

`gen.naive_stdout` is the model: it prints the `keysym:` line with the judge's naming rule, the
header, and exactly **one** row — the first occurrence in (keycode asc, layout asc, level asc)
order — with the mask `[ ]` and rc 0. It is a model of a naive *implementation*, so its formatting
is exact (a fair baseline differs only in semantics).

| corpus | naive passes | rate |
|---|---|---|
| canonical, `difficulty` weighting (seed 4901, n 400) | **79/400** | **19.8 %** |
| same seed, `plain` occurrence weighting | 251/400 | 62.8 % |
| seed 4917, n 60, difficulty | 9/60 | 15.0 % |

Per draw class (difficulty run): header-uniform (absent keysym) 20/20; numeric-present 5/61
(8.2 %); present-uniform 26/42 (61.9 %); present-weighted **28/277 (10.1 %)**. Under plain
weighting the same class is 168/277 (60.7 %) — the difficulty weighting is what buys the
discrimination, and both numbers are reported so the freeze can choose with them in view.

`receipts/contrast-naive.txt` holds the first three failures with both stdouts; case 0 (`kr`,
`parenleft`, present-weighted, keymap AD01=18/AE09 level 2, I187 level 1) — the judge prints two
rows:

```
18       AE09      1        Korean               2       [ Shift ]
187      I187      1        Korean               1       [ ]
```

while the naive prints only the first, with `[ ]` (179 bytes against the judge's 246). Case 2
(`fr`/`oss`, `--keysym 0xfe53`) fails the same way on a single row: judge
`34       AD11      1        French (alt.)        3       [ Mod5 LevelThree ]` against naive
`… 3       [ ]`; case 3 (`hu`, `--keysym 0x5d`) adds the Caps-Lock twin row the naive never emits.
The naive model formats exactly (see F6), so its measured failures are semantic, not cosmetic.

Verdict: 19.8 % overall, 8–10 % on the weighted and numeric classes, roughly three times lower
than the unbiased plain weighting (62.8 %). A first-match/no-modifier tool cannot pass the corpus; the residual fifth is
concentrated in the deliberately easy classes (absent keysym, uniform present draw), which a
correct instrument must also get right. `it must be few` — met, with the per-class split supplied
rather than a single number.

## 6. Judge facts the freeze must encode (each measured, not assumed)

All from `receipts/contract-facts.txt` and `receipts/header-sufficiency.txt`; every call ran
`env -i PATH=/usr/bin` with `HOME`/`XDG_*` inside scratch.

- **F1** `--keymap=FILE` works on a serialized keymap; stdout on the `br` fixture
  (`--layout br --options compose:caps`, sha256 `efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81`,
  73079 B) is 505 bytes / 5 rows, rc 0. `--keysym slash` reproduces the L1's host sample exactly
  (AD01 level 3/4 with `[ Mod5 LevelThree ]`, AB11 level 1 `[ ]`).
- **F2** `--keymap=-` **does** read stdin: stdout byte-identical to F1
  (`3d895204319dae0c18a405e8a2b232b67279f91c35b05c8440f64415c5bb0be2` for both). An earlier
  truncated `sed -n 1,5p` view of this command looked like zero rows; the correction and the `cmp`
  are in the receipt, because a sandboxed counter can pipe the keymap instead of binding a file.
- **F3** omitting `--keymap` also reads stdin, same bytes as F1.
- **F4** argument forms: `slash`, `0x2f`, `47` → rc 0, same 505-byte stdout. `SLASH`, `NoSymbol`,
  `nosuchsym`, `0x0` → rc 2, **0 stdout bytes**, 2123 stderr bytes (usage). So (a) names are
  case-sensitive, (b) a header define is not automatically a legal argument (`NoSymbol` is define
  #1 of the header), (c) stdout+rc alone is a safe comparison — the error path never writes stdout.
- **F5** naming rule for values: table name → else `U%04X` for a Unicode keysym with code point
  ≥ 0x100 → else `0x%08x`. Measured: `0x2032` → `0x00002032`, `U2032`/`0x1002032` → `U2032`,
  `0x100002b` → `0x0100002b`, `0x110000` → `0x00110000`. The parenthesised value is `(0x%04x)` and
  is not truncated for large values (`(0x1002032)`).
- **F6** row format: columns are width-1 + one separator space (9/10/9/21/8), mask
  `[ %s ]` with a single space for empty; a layout name longer than 20 characters keeps the
  separator and pushes `LEVEL#`/`MODIFIERS` right by one space per extra character
  (`623      I623      1        Ukrainian (Windows Enhanced) 1       [ ]`, 68 B). Fixed-offset
  parsing breaks on this; `gen.parse_judge_rows` parses by shape and the selftest pins both forms.
- **F7** two-layout keymaps: rows carry the group index and that group's `name[N]`
  (`--layout us,br`, slash → AB10 layout 1 `English (US)`, AB11 layout 2
  `Portuguese (Brazil)`), ordered by keycode.

Header sufficiency (`receipts/header-sufficiency.txt`, 2638 header defines):

- **A** for all 120 values with more than one header name, the judge's canonical name is the
  **first** define in file order (120/120) — so header order *is* the canonicalization authority
  for this version, and the deprecated-alias trap is real: `guillemotleft` (the misspelling alias,
  header `:739`) is what the judge prints, while `guillemetleft` (`:740`) is the preferred spelling.
- **B** of the 2638 header names, exactly one (`NoSymbol`) is rejected as an argument → the header
  name set is a sufficient *argument* source (F4 caveat applies to values, not names).
- **C** the header holds **no** Unicode names (0 `U+`/`U2032` defines), but compiled keymaps emit
  them (`U010C`, `U0132`, `U2032`) and raw unnamed values (`0x0100002b`). The tool must implement
  the F5 naming rule itself; the header alone is not sufficient for output.
- **D** case sensitivity: `slash` rc 0, `SLASH`/`Slash` rc 2, `dead_acute` rc 0, `DEAD_ACUTE` rc 2.

Correction to the briefed pin: `grep -c '#define XKB_KEY_'` gives **2659** because 21 of those
lines are documentation examples inside the header comment block (`:83`, `:84`, `:113`, …); the
file contains **2638** actual defines. `gen.py` pins 2638 and the selftest enforces it.

## 7. Freeze recommendation

1. Commit `gen.py` next to the counter, with `xkbcli-list.txt` (snapshot) and the two digests as
   constants. The header can stay a host path — its digest is verified — or be shipped; either way
   the digest check is the contract.
2. Counter parameters: `seed=4901`, `n=400`, `weighting="difficulty"`, `HARD_BONUS=20`, judge =
   pinned `xkbcli-how-to-type` with `--disable-compose --keysym ARG`, keymap compiled at count
   time by the pinned `xkbcli-compile-keymap` in `env -i PATH=/usr/bin` with HOME/XDG in scratch.
3. Assert per case: judge stdout bytes equal, and rc equal. Add the fixed fixtures (host sample
   `br --options compose:caps --keysym slash`, `Return`, and the reject trio `nosuchsym`/`SLASH`/
   `0x0`) because the nonce stream never produces rc 2 (§4).
4. Assert run-to-run stability with the pass digest (case JSON sha + judge stdout sha + rc), as in
   `judge_run.py`; the corpus digest for the frozen configuration is
   `f03e29491fff9629` (first 16 hex of the pass digest) and the case-list digest is
   `3c55eba0f4cc96d996a38ea10df246b9f5d1a816f39ee0159a37ed6ef88c9867`.
5. Record the naive-baseline number as the discrimination floor: a submission that scores like
   first-match/no-modifiers is at 19.8 %; the target is 400/400.

## 8. Risks and limits

- The generator cannot tell whether a keysym is "interesting" beyond the keymap-side proxy
  (`count + 20 * hard_count`); it never consults the judge. That keeps generation pure but means
  the corpus is only as discriminating as §5 measures it to be.
- Two-layout draws always have an empty variant (a per-layout variant list would need
  `--variant v1,v2` alignment); variants on multi-layout keymaps are not covered by the nonce
  stream.
- `hard_bonus` is a policy knob, not a law. `--weighting plain` is the unbiased control and its
  62.8 % naive rate is the honest upper bound on "easy" corpora.
- The naive baseline is a model I wrote, not the real counter tool; it is deliberately exact in
  formatting so its failures are semantic.
- The reject path (rc 2) is proven on three fixed arguments but never generated — by contract the
  ARG is a keysym how-to-type accepts.
- `gen.py --compile` shells out to `xkbcli-compile-keymap`; that is the generator's privilege, not
  the tool's (the tool's contract forbids starting a process).

## 9. Hygiene

- No tools installed or upgraded (nothing was needed; pacman untouched).
- No write to the operator's home: every judge/compile invocation ran with `HOME`, `XDG_CACHE_HOME`,
  `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME` under `/fast/scratch/hyaku/mado-r49/ExecGen`;
  no `hyprctl`/compositor call, no GUI, no input injection, no `xkbcli interactive-*`/`dump-keymap*`.
- No tracked lane file touched: `git -C mado-shokunin status --porcelain` has **0** non-`??` lines
  (nothing modified, added or deleted in the index or worktree). The `??` set is the inherited 47
  `*.synthetic` sidecars (rounds 45/46, untouched), sibling seats' round-49 wave files, and my own
  paths: this report plus the 18 files in this seat dir.
- Scratch `/fast/scratch/hyaku/mado-r49/ExecGen` removed after the receipts were copied into this
  seat dir; no receipt cites a scratch or `/tmp` path as evidence.
