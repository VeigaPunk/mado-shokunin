# ExecOracle — C1 judge harness (round 49, w1 BUILD)

**Status: complete.** Deliverable: `.ufo/waves/round-49/w1/ExecOracle/oracle.py` (sha256
`f6a10533603c46f47f936b3cd0ef82830a9abfaf988badc1b4d85f563493c3d1`, Python 3 stdlib only,
no network, no socket, writes only inside the caller's work dir).
Receipts: `receipts/oracle-selfcheck-run1.txt`, `receipts/oracle-selfcheck-run2.txt`,
`receipts/oracle-selfcheck-cross-process.diff`, `receipts/extra-probes.txt`,
`receipts/quote-check.txt`, `receipts/commands.txt`. Pins: `PINS.txt` + `pins/` (5 files, sha256 each).

Nothing outside the seat dir was written. No counter, gate, tool under test (`tools/mado-keysym.py`)
or frozen instrument was touched. Scratch `/fast/scratch/hyaku/mado-r49/ExecOracle` removed at close.

---

## 1. What the harness is

```python
oracle(rmlvo, arg, work) -> (keymap_bytes, stdout, stderr, rc)
```

* `keymap_bytes` — stdout of the pinned `xkbcli-compile-keymap` for `rmlvo` (a mapping with any of
  `rules, model, layout, variant, options`; `None`/absent = the tool's own default).
* `stdout`, `stderr`, `rc` — the pinned `xkbcli-how-to-type` run on those exact bytes.

Supporting API: `compile_keymap(rmlvo, work) -> bytes`, `judge(keymap_bytes, arg, work) -> (stdout,
stderr, rc)`, `verify_pins()`, `resolve_work()`, `clean_env()`, plus a CLI (`pins|compile|judge|run|selfcheck`).

## 2. Exact argv (verbatim from `receipts/oracle-selfcheck-run1.txt` §2)

```
/usr/lib/xkbcommon/xkbcli-compile-keymap --layout us
/usr/lib/xkbcommon/xkbcli-how-to-type --keymap=<work>/argv/us-return/keymap.xkb --disable-compose --keysym Return
env: HOME=<work>/argv/us-return/home LC_ALL=C PATH=/usr/bin XDG_CONFIG_HOME=<work>/argv/us-return/cfg
```

Construction rules, fixed in code:

| point | behaviour |
|---|---|
| compile flags | only for RMLVO components that are not `None`, in the order `--rules --model --layout --variant --options`; never `--include*`, `--format`, `--enable-environment-names` |
| keymap file | `<work>/keymap.xkb`, written by the harness; argv element is the single token `--keymap=<path>` (equals form, as the contract pins it) |
| judge flags | `--disable-compose --keysym ARG`; `--keysym` is a **no-argument** flag (`pins/xkbcommon-tools-how-to-type.c:167`) and `ARG` is the single positional parameter — `argc - optind` must be 1 (`:255`) |
| child env | exactly `PATH=/usr/bin HOME=<work>/home XDG_CONFIG_HOME=<work>/cfg LC_ALL=C` (a freshly built vector — byte-equivalent to `env -i` with those four) |
| stdin | `/dev/null` (`stdin=DEVNULL`); measured identical to a garbage pipe, because an explicit `--keymap` overrides the AUTO source |
| cwd | the work dir |

Two argv traps, both measured (`receipts/extra-probes.txt` §B, §C):

* `--keymap` is declared `optional_argument`, so the **equals form is mandatory**: `--keymap <file>`
  (space) leaves the file as the positional and ends at rc 2 `ERROR: missing positional parameter`
  with 0 bytes of stdout, while `--keymap=<file>` gives the intended 505-byte answer for
  `--keysym slash`. A counter that rewrites the token breaks the judge silently.
* an `ARG` beginning with `-` is parsed by `getopt_long` as an option, not as the keysym:
  `--keysym -a` → rc 2, `invalid option -- 'a'`. Such an argument is passed through unchanged (it is
  a real judge result); only an empty arg or one containing NUL is refused by the harness.

## 3. Pins

`verify_pins()` is called by `compile_keymap()`, `judge()` and every CLI verb; it hashes both binaries
once per process (`cached=False` forces a re-hash, as the selfcheck does) and raises `PinMismatch` on
any difference:

```
43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250  /usr/lib/xkbcommon/xkbcli-compile-keymap
f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54  /usr/lib/xkbcommon/xkbcli-how-to-type
package libxkbcommon: libxkbcommon-1.13.2-1
package xkeyboard-config: xkeyboard-config-2.48-1
```
(receipt §1; the package lines are a read-only `/var/lib/pacman/local` directory listing — no pacman run.)

Upstream pins used to read the judge's behaviour (tag `xkbcommon-1.13.2`, no branch URLs):
`tools/how-to-type.c` `f774882e…`, `src/keysym.c` `123e3390…`, `include/xkbcommon/xkbcommon-keysyms.h`
`13023369…` (the digest the brief names), `src/compose/table.c` `36ac39d9…`, `src/compose/paths.c`
`e9824c89…`. Every quote below is verified by `receipts/quote-check.txt` (grep, computed locator, 12/12 PASS).

The keysym header is *not* needed by this harness: the judge is the real binary, so name↔value
resolution is the binary's. It matters for a reimplementation, i.e. C1's tool seat.

## 4. Determinism — 3 identical runs on 72 cases

`receipts/oracle-selfcheck-run1.txt` §3: `cases=72 reps=3 identical=72/72`. Each case is compared on
**four** channels — keymap sha, stdout sha, stderr sha, rc — over 3 runs in the same work dir.

The fixture set spans: 16 layouts (`us br de fr ru jp gb es pt it no se pl tr gr in`); variants
`intl/nodeadkeys/dvorak/colemak`; options `compose:caps compose:ralt lv3:ralt_switch
grp:alt_shift_toggle ctrl:nocaps caps:escape`; models `pc104/pc105/apple/abnt2`; rules `evdev/base`;
keysym args by name (`Return slash EuroSign eacute U00e9 U20AC dead_acute ISO_Level3_Shift
Multi_key …`), by hex (`0xff0d 0x20 0x2f`) and by decimal (`13`), plus two invalid names
(`NoSymbol`, `nosuchsym`) that exercise the rc-2 path, and an empty RMLVO (`defaults-return`).

**Cross-process**: a second process, a different work dir, `receipts/oracle-selfcheck-run2.txt`;
`receipts/oracle-selfcheck-cross-process.diff` is 0 lines after dropping the timestamp line and the
timing block. So the result does not depend on the process, on the work-dir path, or on run order.

Cross-round tie: `--layout br --options compose:caps` yields keymap `efd487a399201523…` — the digest
the round-48 entry recorded for the same RMLVO (`efd487a39920…`, 73079 B).

## 5. Cost per call (n=50, one fresh work dir per call, both binaries spawned)

| run | oracle | compile | judge |
|---|---|---|---|
| 1 | median 3.00 ms (2.60–6.08) | 1.73 ms | 1.23 ms |
| 2 | median 2.97 ms (2.63–4.64) | 1.76 ms | 1.21 ms |

~3 ms per case ⇒ the whole 72-case × 3-rep matrix is ≈ 0.7 s of process time; a 500-case counter
costs ~1.5 s. Cost is dominated by two `execve`s, not by the keymap work. Warm-page-cache numbers.

## 6. Environment isolation

Parent-side (the harness must not inherit): with `XKB_CONFIG_ROOT=/nonexistent`,
`XKB_CONFIG_EXTRA_PATH=/nonexistent`, all five `XKB_DEFAULT_*` and `XKB_LOG_LEVEL=debug` set in the
**parent**, `oracle()` returns the byte-identical result to the clean baseline (§5a:
`km=efd487a399201523 out=3d895204319dae0c rc=0`, `identical=yes`).

Child-side (proving the vector is load-bearing, not merely unused): §5b passes those variables to the
child on purpose —

| child env | result |
|---|---|
| `XKB_CONFIG_ROOT=/nonexistent` | rc 0, 73079 B (libxkbcommon falls back to `DFLT_XKB_LEGACY_ROOT`) |
| `XKB_CONFIG_EXTRA_PATH=/nonexistent` | rc 0, 73079 B |
| both `/nonexistent` | rc 0, 73079 B (same fallback) |
| `XKB_CONFIG_ROOT=''` + `XKB_CONFIG_EXTRA_PATH=/nonexistent` | **rc 1**, 0 B, `xkbcommon: ERROR: [XKB-338] Couldn't find file "rules/evdev" in include paths` |

So a single bogus root is *not* a determinism hazard on this host — the legacy fallback masks it —
and a fixture designer must not assume it is. The real hazard is the user tree: §5c shows
`$XDG_CONFIG_HOME/xkb/symbols/br` (a 4-line file) changes the compiled keymap
(`a091e655…` vs `6ef21276…`, `identical=NO`), and `receipts/extra-probes.txt` §D measures all three
locations the library searches — `$HOME/.xkb/symbols/br`, `$HOME/.config/xkb/symbols/br` and
`$XDG_CONFIG_HOME/xkb/symbols/br` — each yielding the same poisoned digest `a091e655…` against clean
`6ef21276…`. That is why `HOME` and `XDG_CONFIG_HOME` point at empty scratch dirs, and why
`resolve_work()` **refuses** a work dir that already carries `cfg/xkb`, `home/.config/xkb` or
`home/.xkb` (§5c last line: `refused: WorkDirRefused`).

`XKB_LOG_LEVEL=debug` handed to the child changes stderr 0 → 231 B and leaves stdout+rc identical
(§5d) — it is a stderr-only vector, which is one reason stderr is not a contract channel.

`XKB_DEFAULT_*` never reach the judge: `how-to-type` builds its context with
`XKB_CONTEXT_NO_ENVIRONMENT_NAMES` unless `--enable-environment-names` is given
(`pins/xkbcommon-tools-how-to-type.c:580`), and `--enable-environment-names` together with `--keymap`
is a usage error (`rc 2`, `ERROR: --keymap is not compatible with --enable-environment-names`), so the
contracted argv structurally cannot take RMLVO from the environment.

## 7. Locale

Seven vectors — `LC_ALL=C`, `C.UTF-8`, `en_US.UTF-8`, `pt_BR.UTF-8`, `LANG=en_US.UTF-8`,
`LANG=tr_TR.UTF-8`, and neither variable — give identical **compile** and **judge** results
(§7: `km=efd487a399201523 out=3d895204319dae0c err=… rc=0 same_as_C=yes` ×7). `LC_ALL=C` is
therefore a convention, not a dependency, for the contracted argv.

Mechanism: `how-to-type` does call `setlocale(LC_ALL, "")` (`…how-to-type.c:542`), but with
`--disable-compose` the compose table is never created (§9 measures the difference), so the only
locale consumer is gone. Even *with* compose, this host's 62 locale `Compose` files resolve to the
same table: `C/Compose` is 0 bytes and `src/compose/paths.c:185` falls back to
`static const char * const fallback = "en_US.UTF-8";`.

## 8. Why `--disable-compose` is in the contracted argv (§9)

| argv | plain | `XCOMPOSEFILE` = `<Multi_key> <a> : "X"` | identical |
|---|---|---|---|
| compose **on** (`--keysym U0058` only) | out `a6c0cd45…` | out `a9faf82e…` | **NO** |
| compose **off** (contracted argv) | out `7eb309de…` | out `7eb309de…` | yes |

With compose enabled, `XCOMPOSEFILE`, `$XDG_CONFIG_HOME/XCompose`, `$HOME/.XCompose` and
`XLOCALEDIR` are stdout inputs (`src/compose/paths.c:136`, `src/compose/table.c:177/183/189`) — an
unbounded environment surface the tool cannot reproduce without reading files. `--disable-compose`
deletes that whole class. The poison is only *visible* when the keymap actually binds a `Multi_key`
key, so §9 uses `--layout br --options compose:caps`: plain `br` answers 0 rows for `Multi_key` and
shows no difference at all (§13 finding 3).

## 9. Malformed keymap — what the judge does (§6 of the selfcheck, §A of `extra-probes`)

| variant | rc | stdout | stderr lines | last line |
|---|---|---|---|---|
| truncated at 50 % | 1 | 0 B | 3 | `ERROR: Failed to create XKB keymap` |
| truncated last 8 B | 1 | 0 B | 3 | `ERROR: Failed to create XKB keymap` |
| `!!! not xkb !!!` appended | 1 | 0 B | 3 | `ERROR: Failed to create XKB keymap` |
| `// trailing line comment` appended | **0** | 176 B | 0 | — |
| `/* trailing block comment */` appended | 1 | 0 B | 3 | `ERROR: Failed to create XKB keymap` |
| empty file | 1 | 0 B | 3 | `ERROR: Failed to create XKB keymap` |
| plain text (`hello`) | 1 | 0 B | 3 | `ERROR: Failed to create XKB keymap` |
| file missing | 1 | 0 B | 2 | `ERROR: Failed to create XKB keymap` |

The judge does **not** pre-validate and the harness does **not** special-case: it returns exactly the
binary's `(stdout, stderr, rc)`. Consequence for the counter: a malformed fixture is a legitimate
case, and a tool that answers one with anything but *empty stdout + rc 1* fails.

"Extra comment" is **not** one behaviour — measured in `receipts/extra-probes.txt` §A:

| keymap variant | rc | stdout | stderr |
|---|---|---|---|
| base (`--layout br`, 73043 B) | 0 | 176 B, `9697ab0c…` | empty |
| + `// a line comment` at EOF | 0 | **byte-identical** to base | empty |
| + `/* a block comment */` at EOF | 1 | 0 B | `[XKB-769] …:2089:1: syntax error, unexpected /, expecting end of file` |
| + `/* mid-file block */` after line 1 | 1 | 0 B | `[XKB-769] …:2:1: syntax error, unexpected /` |

So a `//` comment is accepted and ignored, while any `/* */` block comment is a syntax error wherever
it sits. Those two make a strong malformed pair: same keymap, one comment form parses, one does not.

Note the parse-error line: failures inside a readable file say `(unknown file)` and never contain the
path, while a *missing* file prints the path. That is the root of the channel rule in §10.

## 10. Channels: stdout + rc only

* **stdout + rc are the contract.** Both are independent of the work-dir path (§11: the same case in
  two work dirs gives the same km digest, the same stdout digest and the same rc).
* **stderr is diagnostics.** It carries (a) the work-dir path for a missing file (§11:
  `stderr identical=NO` between two dirs), (b) the include-path list on `XKB-338`, (c) `XKB_LOG_LEVEL`
  chatter, and (d) the usage text on rc 2 — which embeds `argv[0]`. A counter that compares stderr
  will produce false negatives on every one of those vectors.
* The rc-2 path is reproducible: empty stdout, rc 2, usage on stderr; the measured
  `nosuchsym`/`NoSymbol` cases carry the same stderr digest across all 3 runs (§3).

## 11. Wrapper and stdin (§10 of the receipt)

* `/usr/bin/xkbcli how-to-type --keymap=… --disable-compose --keysym slash` gives **identical
  stdout, stderr and rc** to `/usr/lib/xkbcommon/xkbcli-how-to-type …` — the wrapper execs the inner
  binary, so even `argv[0]` in the usage text is the same. Either spelling is a valid judge.
* stdin: a garbage pipe vs `/dev/null` gives identical stdout+rc.

## 12. Work-dir safeguards (SentScratch + round-48 M48-10)

* `resolve_work()` refuses `/tmp`, `/var/tmp`, `/dev/shm` (and refuses a work dir that is a file);
  measured refusal in §8 and in the CLI smoke test (`rc 2`, `WorkDirRefused: work dir /tmp/nope is
  under /tmp`).
* `HOME`, `XDG_CONFIG_HOME` always point inside the work dir; no `~/.cache`, `~/.config`, `~/.local`
  is ever touched by the harness (it creates only `home/` and `cfg/` under `work/`).
* A pre-poisoned `cfg/xkb` / `home/.config/xkb` / `home/.xkb` is refused rather than silently used.
* Argument guards: empty keysym, NUL in keysym, unknown RMLVO key, empty RMLVO value — all
  `ValueError` (§8).
* Concurrency: one work dir per concurrent call (the harness does not lock; two calls in the same
  dir would race on `keymap.xkb`). The selfcheck uses one dir per case.

## 13. Findings for the L1 freeze

1. **Compare stdout+rc, never stderr** (§10). If the frozen predicate says "stdout+rc equal", the
   harness already satisfies it; write it that way in `registration.md`.
2. **`--model` alone does not discriminate.** `us --model pc104`, `us --model apple` and `br --model
   abnt2` serialize to the *same* keymap bytes as their defaults (`7f40cb5f…`, `6ef21276…` in §3).
   Fixtures that vary only the model cost time and test nothing.
3. **`compose:*` options move the keymap but not every answer.** `br` vs `br --options compose:caps`
   differ in keymap (`6ef21276…` vs `efd487a3…`) yet `--keysym slash` is identical
   (`3d895204…` both). They only discriminate on keysyms the option moves: `--keysym Multi_key` gives
   0 rows / `out=2c1912cd…` without the option and 2 rows / `out=aac42bb0…` with it
   (`receipts/extra-probes.txt` §E).
4. **Keymap bytes are path- and process-independent**, so each fixture can be pinned by its keymap
   sha256 and re-verified cheaply without running the judge.
5. **The compile step needs `/usr/share/xkeyboard-config-2`; the judge run does not.** The counter
   should compile *outside* the tool's sandbox (as the brief already says) and bind only the keymap
   file into it — with `env -i`-equivalent scrubbing on both sides.

## 14. Risks / limits

* **Warm numbers.** Cost figures are with the binaries and xkeyboard-config tree in page cache; a cold
  first call is not measured.
* **Host-scoped.** Everything is measured on this host (libxkbcommon 1.13.2-1 / xkeyboard-config
  2.48-1). The pins make a different library a hard failure rather than a silent drift, but the
  fixture answers themselves are host-scoped by construction (xkeyboard-config bytes).
* **Not a sandbox.** `oracle.py` does not create the bwrap jail for the tool under test; it produces
  the judge's bytes. The counter owns the jail.
* **`stderr` shape is unpinned** (by design); a future predicate that adds stderr would have to
  normalise the work path and `argv[0]`.
* I did not test `--keysym` args containing UTF-8 multi-byte characters (the judge's non-`--keysym`
  path treats a single character as a code point; out of contract here).

## 15. Verification performed (all from committed bytes)

`python3 -I oracle.py selfcheck --work <scratch>/sc1` and `…/sc2`, twice, in `env -i` with
`HOME`/`XDG_CONFIG_HOME` in scratch, `timeout 600`, `ulimit -f 65536`: both `rc 0`, stderr empty,
72/72 cases identical, cross-process diff 0 lines. CLI verbs `pins`, `compile`, `judge`, `run` each
smoke-tested once; `/tmp` refused with rc 2. `receipts/extra-probes.txt` records the argv-form,
comment-form, user-tree and `Multi_key` probes; `receipts/quote-check.txt` is 12/12 PASS. Scratch
removed.
