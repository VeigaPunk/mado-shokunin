# ExecIndepA — independent reimplementation of C1's contract

Seat: implement `tools/mado-devices.py` from the **docstring only** of the frozen reference, score it with
`quality/counters/c1-r46-devices.py`, report every failing fixture verbatim with a docstring-based judgement, then
list every contract sentence I had to read twice.

**State: `TARGET_MET`, 90/90 fixtures and 150/150 clause-g cases, on nine nonces (8 fixed + 1 random).**

## 1. What I built

| item | value |
|---|---|
| file | `.ufo/waves/round-46/w1/ExecIndepA/mado-devices.py` |
| sha256 | `fc237d49d737519d7418e74965a7c52aadad89d391660a7d32b643a572fe1a59` |
| size | 680 lines, python3 stdlib only (`json math os re stat struct sys`) |
| selftest | `MADO_DEVICES_SELFTEST: 80/80 passed`, exit 0 |
| reads | regular files and `--devices -` only; no subprocess, no socket, no `hyprctl` |

Method: I read lines 1–90 of `.ufo/waves/round-46/l1-draft/mado-devices.py` (the docstring; my read stopped at the
closing `"""` on line 90) and nothing below it. I never opened lines 91–566. The only other reference material was
the frozen counter `quality/counters/c1-r46-devices.py` (the predicate: how it invokes the tool, the selftest line
format, the fixtures) and the frozen fixtures, plus the published live receipt
`.ufo/waves/round-46/receipts/live-devices-host-l1.txt` (the reference's own stdout, used for output *format*, not semantics).

## 2. Scoring

Installed at `tools/mado-devices.py` in a scratch clone of the lane at the freeze commit, committed there:

```
$ D=$(mktemp -d -p /fast/scratch/hyaku/mado-r46/ExecIndepA); git clone -q --shared --no-checkout \
    /home/vgpnk/Projects/shokunin/mado-shokunin "$D"; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
$ git -C "$D" checkout -q --detach 8c5434c60e03f147ee1f75ab195e8bc3f0db4dec
$ cp .ufo/waves/round-46/w1/ExecIndepA/mado-devices.py "$D/tools/mado-devices.py" && git -C "$D" add tools/mado-devices.py
$ git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m "c1 tool (ExecIndepA)"   # rev 8f53ea8
$ python3 -I quality/counters/c1-r46-devices.py --repo "$D" --rev HEAD --work /fast/scratch/…/w [--nonce N]
```

Final tree rev `8f53ea829e3d0381ffe9236db3bbce154f53eb87`; every run below is that rev:

| run | log | result |
|---|---|---|
| no `--nonce` (random 906358063) | `.ufo/waves/round-46/w1/ExecIndepA/receipts/c1-random-nonce.txt:95` | fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present **TARGET_MET** |
| `--nonce 7` | `.ufo/waves/round-46/w1/ExecIndepA/receipts/c1-nonce7.txt:95` | identical line, **TARGET_MET** |
| `--nonce 1234` | `.ufo/waves/round-46/w1/ExecIndepA/receipts/c1-nonce1234.txt:95` | **TARGET_MET** |
| `--nonce 1, 2, 3, 42, 999, 987654` | `.ufo/waves/round-46/w1/ExecIndepA/receipts/c1-nonce{1,2,3,42,999,987654}.txt` | six more **TARGET_MET**, each 90/90 + 150/150 |

Progression (kept as evidence of what each fix bought): rev `e294cec` 85/90 + 126/150 (`.ufo/waves/round-46/w1/ExecIndepA/receipts/c1-run1.txt`),
rev `097b988` 90/90 + 149/150 (`.ufo/waves/round-46/w1/ExecIndepA/receipts/c1-run2.txt`), rev `a583813` 90/90 + 149/150 (`.ufo/waves/round-46/w1/ExecIndepA/receipts/c1-run3.txt`),
rev `8f53ea8` 90/90 + 150/150.

### Host differential (allowed read only: `hyprctl devices -j`)

My build, fed the live dump and `~/.config/hypr/input.conf`, prints **byte-identical** output to the reference's
published live receipt (`.ufo/waves/round-46/receipts/live-devices-host-l1.txt`), exit 0, empty stderr:
`.ufo/waves/round-46/w1/ExecIndepA/receipts/host-diff.txt:23` (`diff` produced no output; summary line `keyboards=10 agree=9 differ=0 fallback=0
virtual=1 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK`).
That is a differential check on real host data, not a re-run of a fixture.

## 3. Every failing fixture of my first build, verbatim, and how I judged it

**None of the seven failures was the fixture's or the contract's fault; all seven were my file.** Verbatim expected
line and the counter's verbatim failure line per fixture are in `.ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt`; the two clause-g
cases are in `.ufo/waves/round-46/w1/ExecIndepA/receipts/generated-cases.txt`.

### F1 `matched-touch` — a bracket line must create its device even when F is not a DEVICE key

<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:4 -->
```
config 0: "device[logitech-keyboard]:output = DP-1\n"
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:7 -->
```
MADO_DEV_BLOCK: name="logitech-keyboard" keys=0 verdict=MATCHED
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:10 -->
```
PRED-C1-r46 clause=f fixture=matched-touch FAIL 46A:rc=0 want_rc=0 stderr=b'' got='MADO_DEV_KEYBOARD: name="logitech-touchpad" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK\n'; 46B:rc=0 want_rc=0 stderr=b'' got='MADO_DEV_KEYBOARD: name="logitech-touchpad" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK\n'; nA:rc=0 want_rc=0 stderr=b'' got='MADO_DEV_KEYBOARD: name="at-translated-set-2-deathadder-v2-2" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK\n'
```

Config `device[logitech-keyboard]:output = DP-1`: `output` is neither a DEVICE KEY nor `name`, so my build created
no block (`blocks=0`); the fixture wants the block created with `keys=0` and matched through the dump's `touch` list.
Deciding sentence:

> device N is created if absent; F one of the DEVICE KEYS sets that key of N to RHS  <-- draft:52

Creation is unconditional and precedes the per-F rules; my file was wrong (I created only for DEVICE KEYS). Same fix
also cleared F5.

### F2 `comment-triple-hash` — where the `##` scan resumes

<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:12 -->
```
config 0: "input:kb_options = a###b\n"
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:14 -->
```
MADO_DEV_KEYBOARD: name="logitech-touchpad" block=no layout="us" variant="" options="a##b" model="" rules="" kb_file=- differ=- verdict=AGREE
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:17 -->
```
PRED-C1-r46 clause=f fixture=comment-triple-hash FAIL 46A:rc=1 want_rc=0 stderr=b'' got='MADO_DEV_KEYBOARD: name="logitech-touchpad" block=no layout="us" variant="" options="a#" model="" rules="" kb_file=- differ=options verdict=DIFFER\nMADO_DEVICES: keyboards=1 agree=0 differ=1 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=DIFFER\n'; 46B:rc=1 want_rc=0 stderr=b'' got='MADO_DEV_KEYBOARD: name="logitech-touchpad" block=no layout="us" variant="" options="a#" model="" rules="" kb_file=- differ=options verdict=DIFFER\nMADO_DEVICES: keyboards=1 agree=0 differ=1 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=DIFFER\n'; nA:rc=1 want_rc=0 stderr=b'' got='MADO_DEV_KEYBOARD: name="at-translated-set-2-deathadder-v2-2" block=no layout="us" variant="" options="a#" model="" rules="" kb_file=- differ=options verdict=DIFFER\nMADO_DEVICES: keyboards=1 agree=0 differ=1 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=DIFFER\n'
```

I read the pair rule as "consume both `#` and resume after the pair", giving `a#b` for `a###b`. Deciding sentence:

> resumes two characters after the first `#` of the pair in the shortened line; any other `#` ends the line there  <-- draft:42

"in the shortened line" is the operative clause: one `#` is erased, so resuming two characters after the pair's
first `#` *in the shortened line* leaves the character after the literal unexamined — `a###b` → `a##b`, and
`a####b` → `a##`. My file was wrong, the sentence is right.

### F3 `block-first-not-name` — the whole block after a non-`name` first key

<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:19 -->
```
config 0: "device {\nkb_layout = de\nname = logitech-touchpad\n}\n"
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:22 -->
```
MADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=2 verdict=NOT_COMPARED
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:24 -->
```
PRED-C1-r46 clause=f fixture=block-first-not-name FAIL 46A:rc=5 want_rc=5 stderr=b'' got='ad" block=yes layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEV_BLOCK: name="logitech-touchpad" keys=0 verdict=MATCHED\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED\n'; 46B:rc=5 want_rc=5 stderr=b'' got='ad" block=yes layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEV_BLOCK: name="logitech-touchpad" keys=0 verdict=MATCHED\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED\n'; nA:rc=5 want_rc=5 stderr=b'' got='ut="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEV_BLOCK: name="at-translated-set-2-deathadder-v2-2" keys=0 verdict=MATCHED\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=1 stale=0 unsupported=1 verdict=NOT_COMPARED\n'
```

For `device { kb_layout = de / name = X }` I counted one `unsupported` and then let the `name` line select X
(`blocks=1`); the fixture wants `unsupported=2` and `blocks=0`. Deciding sentence:

> later `device:` lines go the same way until the stack empties  <-- draft:60

So a failed block refuses *all* of its later `device:` lines, `name` included; a `name` line no longer selects.
My file was wrong.

### F4 `rename` — a rename also refuses the rest of the block

<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:26 -->
```
config 0: "device {\nname = keychron-mx-master-3-keyboard\nname = logitech-touchpad\nkb_layout = de\n}\n"
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:29 -->
```
MADO_DEV_BLOCK: name="keychron-mx-master-3-keyboard" keys=0 verdict=NO_SUCH_DEVICE
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:32 -->
```
PRED-C1-r46 clause=f fixture=rename FAIL 46A:rc=5 want_rc=5 stderr=b'' got='t="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEV_BLOCK: name="keychron-mx-master-3-keyboard" keys=1 verdict=NO_SUCH_DEVICE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=1 stale=1 unsupported=1 verdict=NOT_COMPARED\n'; 46B:rc=5 want_rc=5 stderr=b'' got='t="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEV_BLOCK: name="keychron-mx-master-3-keyboard" keys=1 verdict=NO_SUCH_DEVICE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=1 stale=1 unsupported=1 verdict=NOT_COMPARED\n'; nA:rc=5 want_rc=5 stderr=b'' got='"us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEV_BLOCK: name="hp--inc-yubikey-otp+fido+ccid-2" keys=1 verdict=NO_SUCH_DEVICE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=1 stale=1 unsupported=1 verdict=NOT_COMPARED\n'
```

`device { name = X / name = Y / kb_layout = de }`: the fixture wants `keys=0` and `unsupported=2`, i.e. the
`kb_layout` after the failed rename did *not* reach X. The docstring only says:

> `name` (a rename) adds one to `unsupported`; other F are ignored  <-- draft:57

which by itself would leave the following `kb_layout` applied (`keys=1`). **The fixture is stricter than the
sentence**; I made my file follow the fixture, because F3's sentence ("later `device:` lines go the same way until
the stack empties") shows the reference refuses the remainder of a block whose special key went wrong, and a rename
failure is the same class of error. My file was wrong; the contract sentence is incomplete here (see H2).

### F5 `bracket-name-key` — bracket + `name`: refused, block still created

<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:34 -->
```
config 0: "device[keychron-mx-master-3-keyboard]:name = logitech-touchpad\n"
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:37 -->
```
MADO_DEV_BLOCK: name="keychron-mx-master-3-keyboard" keys=0 verdict=NO_SUCH_DEVICE
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/failing-fixtures.txt:40 -->
```
PRED-C1-r46 clause=f fixture=bracket-name-key FAIL 46A:rc=5 want_rc=5 stderr=b'' got='MADO_DEV_KEYBOARD: name="logitech-touchpad" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=1 verdict=NOT_COMPARED\n'; 46B:rc=5 want_rc=5 stderr=b'' got='MADO_DEV_KEYBOARD: name="logitech-touchpad" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=1 verdict=NOT_COMPARED\n'; nA:rc=5 want_rc=5 stderr=b'' got='MADO_DEV_KEYBOARD: name="at-translated-set-2-deathadder-v2-2" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=- verdict=AGREE\nMADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 unsupported=1 verdict=NOT_COMPARED\n'
```

`device[keychron…]:name = logitech-touchpad` wants the block created with `keys=0`, `stale=1`, `unsupported=1`.
My build created nothing. Deciding sentences: draft:52 (creation first, F1) and

> F `name` adds one to `unsupported`; any other F is ignored  <-- draft:53

My file was wrong (missed creation; already fixed by F1's fix).

### F6 clause-g case 13 (nonce 3930529855) — a top-level bracket+`name` error must not leak into the next block

<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/generated-cases.txt:4 -->
```
config 0: "input:kb_options = nodeadkeys\ndevice[at-translated-set-2-hyperx-alloy-origins-core-keypad]:name = x\ndevice {\n  name = at-translated-set-2-hyperx-alloy-origins-core-keypad\n  scroll_factor = nan\n  kb_variant = 0.125\n  kb_layout = -3\n}\n"
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/generated-cases.txt:11 -->
```
MADO_DEV_BLOCK: name="at-translated-set-2-hyperx-alloy-origins-core-keypad" keys=2 verdict=MATCHED
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/generated-cases.txt:16 -->
```
MADO_DEVICES: keyboards=1 agree=0 differ=0 fallback=0 virtual=1 mice=3 mice_differ=1 blocks=5 stale=2 unsupported=2 verdict=NOT_COMPARED
```

After fixing F4 my poison flag was set by the bracket+`name` line at an empty stack and survived into the next
`device {` block: my block printed `keys=0` and I printed `unsupported=5` where the reference prints `keys=2` and
`unsupported=2`. Deciding sentence: the scope clause, twice —

> later `device:` lines go the same way until the stack empties  <-- draft:60

> the current device until the stack empties  <-- draft:55

An error raised with an already-empty stack has no block to live in, so it must not outlive its own line. My file
was wrong (over-scoped the flag).

### F7 clause-g case 132 (nonce 1625735376) — a top-level flat `device:F` error *does* reach the next block

<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/generated-cases.txt:18 -->
```
config 0: "device[yubico-keyboard-keypad] {\n  kb_rules = \n}\ndevice {\n  name = yubico-keyboard-keypad\n  kb_variant = \n  kb_options = 0x10\n  kb_layout = 0x10\n}\ninput:kb_options = a##b # c\ndevice:kb_layout = de\ndevice {\n  name = Razer DeathAdder\n  kb_layout = 0x10\n}\n"
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/generated-cases.txt:26 -->
```
MADO_DEV_BLOCK: name="yubico-keyboard-keypad" keys=4 verdict=MATCHED
```
<!-- evid .ufo/waves/round-46/w1/ExecIndepA/receipts/generated-cases.txt:28 -->
```
MADO_DEVICES: keyboards=2 agree=1 differ=1 fallback=0 virtual=0 mice=3 mice_differ=0 blocks=2 stale=0 unsupported=3 verdict=NOT_COMPARED
```

`device:kb_layout = de`, then `device { name = Razer DeathAdder / kb_layout = 0x10 }`: the reference prints no Razer
block and `unsupported=3`; my fixed build printed the block (`blocks=3`, `stale=1`) and `unsupported=1`. So the flat
form's error is *not* scoped to the empty stack the way the bracket form's is: it refuses the next block's `name`
and keys until that block closes. Same sentence as F6 decides the "until the stack empties" end point; the
*difference between the two error forms* is nowhere in the docstring — see H3. My file was wrong; the contract is
silent.

## 4. Docstring sentences I had to read twice

| # | quote (located) | reading A | reading B | decided by |
|---|---|---|---|---|
| A1 | > ending in a backslash is joined with the next raw line after the backslash and the spaces and tabs before it are removed  <-- draft:38 | remove the spaces/tabs *before the backslash* (trailing) of the first line | remove the *leading* spaces/tabs of the continued line | fixture `continuation-spaces` (`br  \t\` + `,us` → `br,us`): only A yields it → A. The other half (leading spaces of the continued line) → H1 |
| A2 | > resumes two characters after the first `#` of the pair in the shortened line; any other `#` ends the line there  <-- draft:42 | consume the pair, resume in the original line | resume two after the pair's first `#` in the *shortened* line (skip one more char) | fixture `comment-triple-hash` (`a###b` → `a##b`) → B (F2) |
| A3 | > device N is created if absent; F one of the DEVICE KEYS sets that key of N to RHS  <-- draft:52 | create only if F is a DEVICE KEY | create first, unconditionally, then interpret F | fixtures `matched-touch` + `bracket-name-key` → B (F1, F5) |
| A4 | > later `device:` lines go the same way until the stack empties  <-- draft:60 | every later `device:` line of the block is refused, `name` included | only the non-`name` lines are refused; a later `name` still selects | fixture `block-first-not-name` → A (F3) |
| A5 | whether a *rename* refuses the rest of the block (only "adds one to `unsupported`" is written) | only that line | the rest of the block too | fixture `rename` → B (F4); the sentence does not say it → H2 |
| A6 | > the current device until the stack empties  <-- draft:55 | the error state is void if the stack was already empty (bracket form) | the error state survives the empty stack | clause-g case 13 → A; clause-g case 132 → B for the flat form. Two forms, one sentence → H3 (no fixture decides; only clause g) |
| A7 | > kb_file=<set\|-> differ=<names\|->  <-- draft:81 | `set` = the resolved `kb_file` is non-empty | `set` = the key is set anywhere, even to `""` | **none** → H4 (fixture `kb-file` only has a non-empty value) |
| A8 | > both print the same with two decimals  <-- draft:76 | compare the two 2-decimal strings | numeric equality of the floats | fixture `mouse-round-half-even` (`0.125` → `0.12`, AGREE) → A |
| A9 | > scroll_factor clamped to 0..100 when the block set it, else -1  <-- draft:75 | `-1` also when stof rejected the value | `-1` only when no block sets the key | fixtures `mouse-stof-none` and `mouse-nan` (`keys=0`, `scroll_factor=-1.00`) → A |
| A10 | > keys counts the DEVICE KEYS the block set  <-- draft:86 | a `scroll_factor` that stof refused does not count | a written key counts even if unparsable | fixtures `mouse-stof-none`/`mouse-nan` (`keys=0`) → A |
| A11 | > (<json> is json.dumps with ensure_ascii  <-- draft:85 | `ensure_ascii=True` (escaped) | parameter left at default (same) / `False` (raw UTF-8) | fixture `unicode-name` (`name="t\u00e9clado"`) → escaped, A |
| A12 | > differ=<names\|->  <-- draft:81 | comma | space or `+` | fixture `global-differ-two` (`differ=layout,variant`) → comma |

Everything else in the docstring was single-reading for me: the verdict order, the FALLBACK definition, the
`VIRTUAL` prefix, the `[[EMPTY]]` marker, the std::stof rules, `--selftest`/usage, the setup reasons, the summary
order and the exit codes.

## 5. Holes (no fixture, and in four cases no generated case, decides)

- **H1 continuation, leading side.** No fixture joins a line whose successor starts with spaces/tabs
  (`input:kb_layout = br,\` + `"    us"`). Both candidate semantics print `br,    us` vs `br,us`; fixtures only vary
  the trailing side. My build keeps the successor's leading spaces.
- **H2 rename scope.** `draft:57` says only "adds one to `unsupported`", but fixture `rename` requires the rest of
  the block to be refused as well. A contract reader implementing the sentence literally fails that fixture: the
  sentence, not the fixture, is what is missing a clause.
- **H3 two error forms, one scope sentence.** F6 and F7 need *different* scopes for the same wording: a bracket
  `name` error at an empty stack is void, a flat `device:F` error at an empty stack refuses the next block. Nothing
  in the docstring distinguishes them and **no fixture covers either** (only clause-g cases do, and only because the
  oracle is the reference). This is the largest hole I found: it is exactly the residual the registration declares
  ("clause g's oracle is the reference, so a contract error shared by reference and tool is invisible to it").
- **H4 `kb_file=<set|->`.** The predicate is never defined; `device { name = X / kb_file = [[EMPTY]] }` (block sets
  it to `""`) is untested. My build prints `-` for an empty resolved value (`set` only when non-empty).
- **H5 setup-error precedence.** With two bad inputs at once (e.g. an unreadable config *and* a non-JSON devices
  file, or a too-large config plus a bad-JSON dump) the docstring does not say which reason wins. No fixture
  combines two failures. My build reads inputs in argument order (unreadable/too_large) and parses the dump after,
  so bad_json loses to a read error.
- **H6 bracket lines inside an already-refused block.** Untested; my build still lets a bracket line create and set
  its device while the block is refused.
- **H7 nested `device` scopes** (`device { sub { … } }`, key `device:sub:kb_layout`): untested; my build ignores
  such keys (not a DEVICE KEY at that depth).

## 6. Residual risk of this build

- The poison model (F3/F4/F6/F7) is inferred from three fixtures and two oracle diffs; it is a *model of the
  reference*, not of hyprlang. If the reference misreads hyprlang, my build copies that misreading — clause g cannot
  see it (declared residual in the registration).
- The selftest is a printed line (declared residual of clause s); mine is 80 real assertions over parsing, verdicts,
  setup failures and the mouse factor, all in-memory (it writes no file, so it also runs inside the read-only
  sandbox).
- `--config` accepts any number of files; a `--config -` is treated as a non-regular path → `SETUP unreadable`
  (the docstring only blesses `--devices -`).

## 7. Files, tool state, scratch

- Written by me, only inside my seat: `.ufo/waves/round-46/w1/ExecIndepA/mado-devices.py`, this report,
  `.ufo/waves/round-46/w1/ExecIndepA/receipts/{c1-run1,c1-run2,c1-run3,c1-nonce1,c1-nonce2,c1-nonce3,c1-nonce7,c1-nonce42,c1-nonce999,
  c1-nonce1234,c1-nonce987654,c1-random-nonce}.txt`, `.ufo/waves/round-46/w1/ExecIndepA/receipts/{failing-fixtures,generated-cases,contract-docstring,
  host-diff,verify-quotes}.txt`, and the four seat scripts `gen-fixtures-receipt.py`,
  `gen-generated-receipt.py`, `fill-evidence.py`, `verify-quotes.py`.
- No tracked file was edited; no counter/fixture/control/reference file was touched; no git or jj mutation anywhere
  outside my scratch clone.
- **Tools installed: none.** No pacman, no uv, no npx; python3 and git only, as shipped.
- Scratch: one clone + work dir under `/fast/scratch/hyaku/mado-r46/ExecIndepA`, deleted before finishing; every
  citable artefact was copied into `.ufo/waves/round-46/w1/ExecIndepA/receipts/` first.

## 8. Verification of this report

`python3 -I .ufo/waves/round-46/w1/ExecIndepA/verify-quotes.py` (output in `.ufo/waves/round-46/w1/ExecIndepA/receipts/verify-quotes.txt`) re-checks
every `> quote <-- draft:N` against `.ufo/waves/round-46/w1/ExecIndepA/receipts/contract-docstring.txt` (substring, start line, ≤ 25 words) and every
`<!-- evid file:line -->` block against the receipt line it cites.
