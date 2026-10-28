# R55RevC2Spec — report (round 55, wave w1, seat R55RevC2Spec)

Role: leaf reviewer for §C2 (`tools/mado-kbdopts.py`), read as a hostile parser author. No subagents. No tracked-file edits, no git/jj mutations, no commits, no host mutations. Scratch: `/fast/scratch/hyaku/mado-r55/R55RevC2Spec/`, removed before yield.

Deliverable: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC2Spec/ambiguities.md` (34 numbered ambiguities A1–A34, 7 resolved/non-divergent notes R1–R7, pinning table, severity summary).
Receipts (copies, in the deliverable directory): `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC2Spec/receipts/` — `ref.py`, `fixtures_run.py`, `cases.py`, `cases.txt`, `cases-stdout.txt`, `fixture-pinning.txt`.

## 1. What I did

1. Read `registration.md` (§C2 and §C1/§C3 for context) and `claims-frozen.md` at the lane root. Confirmed the working-tree copies of the frozen C2 files are identical to freeze commit `54dacbd843d64ba744cd3f1bdc2ec622e5010039`.
2. Dumped all 18 committed fixtures (`fixtures/c2/F01..F18`), the three `ctl/` stubs, `fetch/host-input.conf`, `fetch/host-getoption.json`, and the c2 section of `frozen-tables.json`. Did not open or search for `fixtures/c2-holdout` (absent at the freeze commit; `ls -d` returned no such directory).
3. Built a scratch reference model of §C2 with one switch per ambiguity (`receipts/ref.py`). The default switch set reproduces all 18 committed fixtures (`receipts/fixture-pinning.txt`: `LIT committed=18/18`). Checked each alternative reading against the 18 fixtures to see which ones they pin.
4. Ran 43 concrete cases under the default reading and each alternative (`receipts/cases.txt`), recording stdout, rc, and how many committed fixtures each reading fails.
5. Checked the hyprlang/hyprutils pins for the value grammar (`round-46/fetch/hyprlang-config.cpp`, `round-45/fetch/hyprutils-String.cpp`) and the installed library's imports.
6. Probed the host read-only (see §3) and a few small Python behaviours (argparse stdout, JSON recursion, UTF-16 decoding, FIFO open).

## 2. Commands and decisive output (trimmed)

Fixture pinning:
```
$ python3 -I fixtures_run.py
LIT committed=18/18
ALT topcolon=literal: fails 1 committed: F10
ALT split=splitlines: fails 0 committed: none
...            (all other single alternatives: fails 0 committed: none)
```

The F10 fact that pins the join reading (`topcolon=literal` gives unsupported=3 where F10 expects 4):
```
$ python3 -I -c "...ref.kbdopt(['--config','.ufo/waves/round-55/fixtures/c2/F10/c1.conf','--keyboard','kbd-a'], dict(ref.LIT, topcolon='literal'))"
(['MADO_KBDOPT: keyboard=kbd-a repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=3', ...], 0)
```

Cases (excerpts; full output in `receipts/cases.txt`):
```
## C09 `device {` inside `input {`        literal: keyboard=kbd-a repeat_rate=25 ... from=-/-/- unsupported=0
                                          innermost: keyboard=kbd-a repeat_rate=50 ... from=D/-/- unsupported=0
## C43 numlock_by_default = -0            literal: repeat_rate=25 ... from=-/-/- unsupported=2
                                          hyprutils: repeat_rate=0 numlock=0 from=G/-/G unsupported=0
## C34 missing config + bad getoption     literal: SETUP unreadable (rc 2)
                                          getopt-first: SETUP bad_json (rc 2)
## C36 200000 x '[' on a getoption line   model: UNHANDLED RecursionError (rc 1, empty stdout)
```

Source checks:
```
$ grep -n 'starts_with("true")' round-46/fetch/hyprlang-config.cpp          -> line 259
$ sed -n '46,84p' round-45/fetch/hyprutils-String.cpp                        -> isNumber2 accepts a leading '-'; returns isdigit(str.back())
$ nm -D --undefined-only /usr/lib/libhyprlang.so.0.6.8 | grep -i isnumber
  U _ZN9Hyprutils6String8isNumberERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEb
$ pacman -Q hyprlang          -> hyprlang 0.6.8-5      (query only; no transaction)
```

Read-only checks against the freeze commit and the lane tree:
```
$ git --no-pager -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --stat 54dacbd8… -- <frozen C2 files>   -> (empty)
$ git ... ls-tree -r --name-only 54dacbd8… -- .ufo/waves/round-55/fixtures/c2            -> 73 files
$ git ... ls-tree -r --name-only 54dacbd8… -- .ufo/waves/round-55/fixtures/c2-holdout     -> 0 files
$ ls tools | grep -c kbd                                                                 -> 0   (tools/mado-kbdopts.py absent)
```

## 3. Host reads (all read-only; nothing changed)

```
$ hyprctl version                                  -> Hyprland 0.56.2 built from v0.56.2 at efb50993…
$ hyprctl getoption input:repeat_rate -j          -> {"option": "input:repeat_rate", "int": 40, "set": true }
$ hyprctl getoption input:numlock_by_default -j   -> {"option": "input:numlock_by_default", "int": 1, "set": true }
$ hyprctl devices -j                              -> keyboard list read (names only, not recorded)
$ grep -n 'repeat\|numlock\|^input' ~/.config/hypr/input.conf
  3:input {  14:  repeat_rate = 40  15:  repeat_delay = 250  18:  numlock_by_default = true
```
Observed: `hyprctl getoption -j` prints one JSON object per line (no pretty-printing), so the line-per-object `--getoption` input shape matches the real output. No `keyword`, `dispatch`, `reload` or config write was run.

## 4. Tooling

Nothing installed or upgraded. `pacman -Q hyprlang` is a database query, not a transaction. `nm`/`objdump`-style binary inspection used the system binutils already present. No file in `~/.local/bin` or any PATH directory was created or changed.

## 5. Findings (by severity; full detail and both readings' stdout in `ambiguities.md`)

**High**
- **A9 — contract contradicts source on the sign rule.** §C2 says "sign → unsupported". The pinned hyprutils `isNumber2` (round-45 pin, lines 46–84) accepts a leading `-` followed by digits, and the installed `libhyprlang.so.0.6.8` imports that function. `numlock_by_default = -0` and `repeat_rate = -0` therefore parse to 0 in Hyprland, but the contract model gives `unsupported=2`. No fixture pins this.
- **A12 — the contract's join sentence is wrong as written, and F10 pins the other reading.** "KEY is the stack joined with `:` then `:` then LHS" gives `:input:repeat_rate` for a top-level key. F10 expects `unsupported=4`; the literal text gives 3. Fixture is right, sentence is wrong.
- **A2 — `input { # main` is not a block opener under the literal rule**, so the block's keys are silently lost (`repeat_rate=25` where the comment-cut reading gives 30). No fixture.
- **A8 — "matches `[0-9]+`" needs to say fullmatch.** Source and the contract's own examples agree on fullmatch; the word "matches" does not say it.
- **A13 — `device {` inside `input {`:** exact-stack reading ignores it (25); innermost-device reading uses it (50, `from=D`).
- **A15 — `name = $kbd` with `$kbd = kbd-a`:** literal reading creates a device named `$kbd` (the keyboard `kbd-a` gets global values, `unsupported=0`); the "never guessed" reading counts `unsupported=2`. Real Hyprland expands the variable.
- **A17 — a device named `*` collides with the default line:** `from=D` (rate 50) versus `from=-` (rate 25).

**Medium** (full list in `ambiguities.md` §7): `} # end` (A1); indented comment ending in `{` (A3); CR-only files (A4); `str.strip()` vs the listed set (A5); UTF-8 BOM (A6); `$`/`\` in a comment (A7, same principle as F12 by analogy); nested bracket vs plain device keys counted differently (A14); empty device name (A16); stray `{` (A18); `source =` silently ignored (A19); `--keyboard ""` (A21); repeated `--getoption` (A23); argparse writes usage to stderr with empty stdout (A25, measured); setup-failure precedence (A26); symlinks (A27); `too_large` for getoption (A28); FIFO hangs if opened before classified (A29, measured: rc 124 after 5 s); deep JSON → `RecursionError` (A30, measured); `40.0` as integer (A32).

**Low**: A11, A20, A22, A24, A31, A33, A34.

Operator note (R1): `--getoption` compares only the global value. With a device override `repeat_rate = 50` for `kbd-a` and live `30`, the output is `repeat_rate=50 … from=D` and `config=30 live=30 verdict=AGREE`. Text-correct, but it does not verify the per-keyboard value.

## 6. Pinning result

- All 18 committed fixtures pass under the default reading (LIT).
- Only A12 (join vs literal colon) is refuted by a committed fixture (F10), and A7's `##` part is pinned by F12.
- Every other ambiguity is unpinned. A parser built to the wrong reading in those places still passes all 18 committed fixtures. Hold-out fixtures could catch them only if they happen to hit the same input.

## 7. Defects in the contract text (for the L1 to decide; I did not edit the frozen files)

1. §C2 "KEY is the stack joined with `:` then `:` then LHS" — wrong for an empty stack (F10 pins join).
2. §C2 "matches `[0-9]+`" — should say fullmatch.
3. §C2 "sign → unsupported" — contradicts the source for `-0` (A9).
4. §C2 "a line ending in `{`" / "`}`" — silent on trailing comments.
5. §C2 `$`/`{{`/backslash check — "a line" vs "a RHS": unspecified for comment text.
6. §C2 `*` default NAME — collides with a device named `*`.
7. §C2 "any parse failure" for `bad_json` — the JSON recursion case must be `bad_json`, not an uncaught exception.
8. §C2 stdout/stderr for usage — stdout is specified; stderr is not.

## 8. What I could not verify

- The installed hyprlang's `isNumber` body: only the import is confirmed (`nm`), not its code. The hyprutils body I cite is the round-45 pinned copy; I assume the installed `libhyprutils` matches it.
- `tools/mado-kbdopts.py` does not exist in the lane, so no implementation was run. All stdout in `ambiguities.md` is from my scratch model of the text, not from the tool.
- The `hyprctl getoption` JSON shape was observed for `repeat_rate` and `numlock_by_default` only; `repeat_delay` was not read live.
- A29 and A30 were each measured once, on this host; the FIFO timing and the RecursionError depth are specific to the Python 3.14 build here.
- Did not run `freeze-verify.py` or any counter (they can write; not needed for a reading review).
- No hold-out material was seen or used; the hold-out tree is absent from the freeze commit.

## 9. Coverage of the brief's examples

| Brief example | Where |
|---|---|
| `}` line with trailing text | A1 |
| `name = X # c` | ambiguities R7 (resolved by text: RHS cut at first `#`, stripped; `name = kbd#1` → `kbd`); `name = # none` is A16 |
| `device {` opened inside `input {` | A13 |
| RELEVANT key in a nested block of device | A14 |
| empty `--keyboard` value | A21 |
| repeated `--getoption` | A23 |
| keyboard named `*` | A17 |
| `from` letters, device then later-file global | A20 (both within-file and across-file orders) |
| `repeat_rate = 30 = 4` | A8 |
