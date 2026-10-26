# ExecFixtureMap — which script branches the frozen C1 fixtures reach

Seat `ExecFixtureMap`, mado round 47, wave w2 (FALSIFY), 2026-10-26.
Target: the 190 frozen C1 fixtures against the pinned resolver. Status: **complete**.

## Answer

The 190 fixtures (×2 variants = 380 traced runs) execute **549 of the 1499 lines of
xdg-terminal-exec v0.14.3 (36.6 %)**. **119 statement lines are never executed**, in 19 classes;
**67 of those lines lie inside the print-mode contract the C1 claim is written against and are
not named in the registration's residual list**. Two functions are never entered at all
(`usage` 84-90, `help` 91-142 — declared residual), and the resolver's whole cache machinery is
unreachable **by construction** of the fixture protocol (`read_cache` 3/74 statements seen).

Consequence for `PRED-C1-r47`: clause f judges stdout+rc only, so every line below is invisible
to it. A candidate tool that omits the debug path, the cache path/arms, `\n \t \r` value escapes,
the quoted-backslash tokenizer arms, the tokenizer error arms, consecutive-space skipping, the
content-after-path delimiter, the `TerminalArgTitle=`-form, `NotShowIn` for fallback ids, the
`%D %n %N %v %m` deprecation, the duplicate-exclusion arms, `replace()`'s no-match exit, the
empty-entry-id arm and the hash-failure arm can still score `fixtures=190/190`.

## Method (reproducible, nothing launched)

Instrumentation is `set -x` line tracing of a byte copy of the pin:
`/bin/sh -x SCRIPT ARGS` with `PS4='+${LINENO} '` (bash 5.3.20). Every executed simple command
prints `+<lineno> ...`; nesting adds `+`s (`++<lineno>`), which the parser accepts.

Each fixture is materialised exactly as `quality/counters/c1-r47-terminal.py` does
(same `materialize()`, same `case_env()`: `HOME`, `PATH=<root>/bin:/oracle/bin`,
`XDG_CACHE_HOME=<root>/.rw/cache`, `LANG`, the fixture's five `XDG_*`) and run in the counter's
own sandbox: `bwrap --unshare-all --die-with-parent --new-session --clearenv`, read-only
`/usr/lib`, host bash at `/bin/sh`, the resolver's seven externals at `/oracle/bin`, tmpfs `/tmp`,
case root read-only with `.rw` writable. No `/usr/bin`, `/usr/share`, `/etc`, `/home`, `/fast` of
the host is visible. Variants A (root `<work>/fx-XXXX/r`, `LANG=C.UTF-8`) and B
(`<work>/job-XXXX/deep/XXXXXX/r`, `LANG=en_US.UTF-8`), 30 s timeout each.

Drift control: **every variant-A run reproduced its fixture's recorded `rc` and `stdout`**
(`drift=[]` in `out/lines.json`), so tracing did not perturb behaviour. Fixture argv never leaves
print mode: `arg[0]` is `--print-id` (130), `--print-cmd` (53), `--print-path` (2),
`--print-content` (2), `--print-cmd=,` / `--print-cmd=\s` (2), `--test` (1). No fixture sets any
`XTE_*` variable (env keys union = the five `XDG_*` only).

```
S=/fast/scratch/hyaku/mado-r47/ExecFixtureMap; mkdir -p $S/w
python3 -I map-fixtures.py --work $S/w --out out --variant AB      # 380 runs, ~6 s
python3 -I gen-unreached.py --lines out/lines.json \
        --script ../../fetch/xdg-terminal-exec --out out/unreached-statements.tsv
python3 -I stats.py --lines out/lines.json --script ../../fetch/xdg-terminal-exec
python3 -I probe-artifacts.py --work $S/w --out receipts/02-lineno-and-cache.txt
python3 -I gen-vocabulary.py ; python3 -I verify-quotes.py
```

## Coverage by function (statement lines = non-blank, non-comment; `receipts/03-stats.txt`)

| function | range | stmt | seen | missed |
|---|---|---|---|---|
| error | 45-49 | 2 | 1 | 1 |
| check_bool | 50-76 | 22 | 6 | 16 |
| shcat | 77-83 | 4 | 2 | 2 |
| usage | 84-90 | 5 | 0 | 5 **never entered** |
| help | 91-142 | 36 | 0 | 36 **never entered** |
| make_paths | 143-178 | 21 | 15 | 6 |
| gen_hash | 179-216 | 28 | 12 | 16 |
| read_cache | 217-299 | 74 | 3 | 71 |
| save_cache | 300-341 | 39 | 11 | 28 |
| list_contains | 342-350 | 6 | 4 | 2 |
| read_config_paths | 351-476 | 95 | 44 | 51 |
| replace | 477-500 | 12 | 8 | 4 |
| de_expand_str | 501-560 | 41 | 15 | 26 |
| de_tokenize_exec | 561-693 | 99 | 41 | 58 |
| de_strip_fields | 694-741 | 38 | 23 | 15 |
| reset_keys | 742-753 | 9 | 8 | 1 |
| find_entry_paths | 754-801 | 28 | 18 | 10 |
| check_entry_key | 802-969 | 134 | 83 | 51 |
| read_entry_path | 970-1019 | 33 | 23 | 10 |
| validate_entry_id | 1020-1038 | 12 | 6 | 6 |
| validate_action_id | 1039-1054 | 9 | 5 | 4 |
| find_entry | 1055-1112 | 39 | 28 | 11 |
| get_default_execarg | 1113-1130 | 15 | 8 | 7 |
| `<toplevel>` | 1133-1499 | 300 | 181 | 119 |

Per run: median 270 distinct lines (min 98, max 307); 89 lines run in every one of the 380 runs.

## The 119 never-executed statements, by class (`out/unreached-statements.tsv`)

Bucket `new` = inside the print-mode contract, **not** in the registration residual list;
`decl` = named in `.ufo/waves/round-47/registration.md:54`; `oos` = outside the print-only claim.

| class | bucket | n | lines | what would reach it |
|---|---|---|---|---|
| debug-enabled | new | 5 | 63, 66, 67, 689, 690 | `XTE_DEBUG` or `DEBUG` set; never set by any fixture, and `DEBUG` occurs 0× in the counter |
| help-usage | decl | 4 | 85, 92, 1137, 1138 | `-h`/`--help` in argv |
| check-bool-invalid | new | 2 | 55, 56 | an unrecognised boolean (`XTE_HOLD`/`XTE_CACHE_ENABLED`/… invalid) |
| cache-read | decl | 44 | 222-241, 248-253, 259-260, 272-288, 291-292, 1180 | an existing cache file at `read_cache` time |
| cache-write-arms | new | 9 | 306-308, 314-316, 336-338 | hash failure, a newline in a terminal arg, `XTE_CACHE_ENABLED=false` |
| env-knob | new | 10 | 381-384, 389-392, 404-405 | `/enable_cache`, `/execarg_compat` directives, strict-mode directive ignore |
| expand-escapes | new | 12 | 533-535, 538-540, 543-545, 548-550 | `\n`, `\t`, `\r`, `\\` inside a DE value (only `\s` occurs) |
| tokenizer-escape | new | 9 | 633, 636, 637, 643-648 | a backslash surviving `de_expand_str` into the tokenizer (i.e. `\\` while quoted) |
| tokenizer-error | new | 4 | 628, 629, 676, 677 | unescaped quoted `$`/`` ` ``, or an unclassifiable char |
| tokenizer-space-run | new | 2 | 598, 599 | two consecutive interior spaces in `Exec=` |
| print-order-content | new | 1 | 1359 | `--print-content` after `--print-id`/`--print-path` |
| arg-form-title | new | 4 | 1418, 1419, 1427, 1442 | `TerminalArgTitle=` ending in `=`; `--title`/`--app-id` on an entry lacking the key (the `--dir` and `--hold` counterparts *are* covered: 1412, 1397 traced) |
| entry-checks | new | 2 | 869, 870 | `NotShowIn` on a *fallback* id (`de_checks=false`) |
| field-deprecation | new | 1 | 704 | a deprecated `%D %n %N %v %m` field |
| exclusion-dedup | new | 2 | 449, 459 | a repeated `-id`/`+id` marker |
| replace-break | new | 1 | 492 | `replace()` reaching a string without its separator |
| find-entry-empty-id | new | 1 | 1069 | an empty entry id in the id list |
| gen-hash-fail | new | 2 | 211, 212 | `md5sum` output that is not 32 hex chars |
| launch-path | oos | 4 | 1494-1496, 1499 | argv without any print/test option |

Totals: `new` 67 lines (16 classes), `decl` 48 lines (2 classes), `oos` 4 lines.
The nine further residue lines (28, 41, 68, 258, 473, 691, 792, 1017, 1125) are not statements
(loop/group closers, the second line of a multi-line assignment) and are listed as such in the TSV.
The remaining **448** untraced non-blank non-comment lines are lines bash never reports: case
patterns, heredoc literal text, continuation lines, `fi/then/else/do/done/esac`, `{`/`}`. Every
non-trivial line outside the TSV was audited by hand (74 non-pattern candidates, all function
headers or heredoc/`$()` bodies).

## Measurement artifacts (they bound the numbers; both are reproducible)

**A1 — `LINENO` is shifted inside a heredoc-attached `$( )`.** In `find_entry_paths` the
substitution body at 793-797 never appears; the commands land on other lines:

```
raw| ++756 LC_ALL=C                        # real line 794
raw| ++758 awk '{ print; sub(".*/[.]/", ""); ... }'   # real line 796, 758 is a comment line
```
(`receipts/02-lineno-and-cache.txt`.) In `gen_hash` the body 191-202 never carries its own
numbers: the traced numbers are 190 (229 runs), 193 (23), 194 (22), 195 (21), 197 (19), 199 (14),
200 (15) and nothing at
191/192/196/198/201/202 — exactly the shift 191→190, 194→193, 195→194, 196→195, 198→197, 200→199,
201→200, landing 193/197/199 on *comment* lines.
`receipts/07-heredoc-lineno.txt` shows the mechanism deterministically: a two-command heredoc `$( )`
body at probe lines 4 and 5 is reported as 3 and 4. So lines 191-202 and 793-797 are **executed with
an unreliable line number** and are excluded from the "unreached" count in both directions.

**A2 — the forked `save_cache` child races the parent's exit.** `save_cache "$1" &` (1457) is
started and the parent `exit 0`s in print mode; the sandbox dies with it. Three sequential runs of
the same fixture in one materialised root leave `cache_before=[] cache_after=[]` every time, and
only **1 of 380** runs traced the child past line 305 (the 12 variant-A-only lines
`186, 204, 206-208, 310, 312, 319-321, 333-334`). So `read_cache` can never warm in this protocol
and cache writing is *nondeterministically* traced — the same is true inside the counter, which
also never runs a case twice in one root.

**A3 — variant B adds nothing.** `B_only=[]`; the deep-root/`en_US.UTF-8` variant reaches no line
the flat-root/`C.UTF-8` variant misses. Its only unique contribution to clause f is the path-shape
comparison, not branch coverage.

## What clause g adds, and what stays open

Clause g is **not** measured here (I did not run the counter's generator, only the frozen fixtures).
The statements below are vocabulary facts: what `gen_case()` *can* produce.
From the counter's literal generator vocabulary (`receipts/05-generator-vocabulary.txt`,
`ast`-evaluated): `TerminalArgTitle=-T=` is present (1418-1419), so is `/enable_cache`,
`/execarg_compat`, `/execarg_strict` (381-392, 404-405), `Exec={n} %i %d` (704), the
`Exec={n} "a\\"b"` form (548-550), `NotShowIn=Hyprland;` (869-870) and the
`["--print-path","--print-content","--print-cmd"]` vector (1359). It does **not** contain
`\n`/`\t`/`\r` in a DE value (533-545 stays open), and it never produces `XTE_DEBUG`,
`XTE_CACHE_ENABLED`, `XTE_EXECARG_COMPAT` or `DEBUG` (`XTE_DEBUG`/`XTE_CACHE`/`DEBUG` occur 0× in
the whole counter file). The cache-read path and the launch path stay open under any arm of the
predicate.

So the hole is not only "the fixtures are narrow": five classes are unreachable by the *predicate*
as a whole — cache-read, the write-side cache arms, the `\n`/`\t`/`\r` arms of expand-escapes,
debug-enabled and check-bool-invalid — and the registration declares only the first of them
(warm cache).

## What this supports

The selection core is well exercised: `check_entry_key` 83/134 statements, `read_config_paths`
44/95, `find_entry` 28/39, `de_strip_fields` 23/38, `de_tokenize_exec` 41/99, `make_paths` 15/21,
`find_entry_paths` 18/28, `read_entry_path` 23/33. The arms that carry the behaviour the fixtures
target (list precedence, exclusion markers, actions, categories/show-in, TryExec/Exec/Hidden/
NoDisplay, print composition and exit map, argument prepending for `dir`/`app-id`/`hold` — 1412 and
1397 are traced) are represented in the trace, so the fixtures do pin the *print* behaviour they
set out to pin.

## Risks and limits of this map

- Line, not arm, coverage: a `case` arm's body shares a line with its pattern in several places;
  such an arm counts as reached when its command line is traced. Arm-level claims in this report
  were each read back in the source.
- The class table is authored by hand (19 classes); it is mechanically enforced instead:
  `gen-unreached.py` refuses to run if any listed line was reached, and flags any never-traced
  non-trivial line it does not cover (448 structural lines remain, all audited).
- Tracing perturbs timing (A2). Counting the forked child's lines as "reached" would overstate
  coverage; they are reported separately.
- `PS4`/`LINENO` behaviour is bash-version dependent; the offsets in A1 are probed, not assumed.
  A different judge shell could shift the reported numbers for the two substitution bodies only.
- Nothing here measures `tools/mado-terminal.py` (absent from the lane, as registered).

## Files

Seat dir `.ufo/waves/round-47/w2/ExecFixtureMap/`:

| file | what |
|---|---|
| `map-fixtures.py` | tracer/sweeper: materialise + bwrap + `/bin/sh -x` + per-line parse |
| `stats.py` | every number in this report, recomputed from `out/lines.json` |
| `gen-unreached.py` | class table with assertions; writes the TSV |
| `gen-vocabulary.py` | clause-g vocabulary census (ast, read-only) |
| `probe-artifacts.py` | A1 (`++756`/`++758`) and A2 (cache stays empty) |
| `heredoc-lineno-probe.sh` | deterministic A1 mechanism: heredoc `$( )` body reports line −1 |
| `verify-quotes.py` | re-locates every quote below by line |
| `out/lines.json` | per-line hit counts, per-run line sets, drift record |
| `out/unreached-statements.tsv` | line, class, cases, text, reach condition |
| `receipts/00-pins.txt` | sha256 of host script, pin and fixtures against the counter's constants |
| `receipts/02-lineno-and-cache.txt` | A1 + A2 raw |
| `receipts/03-stats.txt` | full per-line table (1499 rows) + per-function table |
| `out/summary.txt` | one-line sweep summary written by `map-fixtures.py` |
| `receipts/04-unreached-classes.txt` | class census and bucket totals |
| `receipts/05-generator-vocabulary.txt` | clause-g literal vocabulary |
| `receipts/06-quotes.txt` | quote verification |
| `receipts/07-heredoc-lineno.txt` | A1 mechanism probe output |

Pins: host `/usr/bin/xdg-terminal-exec` and `.ufo/waves/round-47/fetch/xdg-terminal-exec` both
`89f2be9a…27ac`; fixtures `4836cc1d…dd86` — equal to `PIN_SHA256`/`FIXTURES_SHA256` in the counter.

## Quotes (locators computed by `grep -n`, verified by `verify-quotes.py`)

- `xdg-terminal-exec:221` — `if [ -f "${XTE__CACHE_FILE}" ]; then` (the cache gate that never opens).
- `xdg-terminal-exec:552` — `# unsupported sequence, reappend backslash` (and it does not: an
  unknown escape is dropped, which is why `\"` reaches the tokenizer as `"`).
- `xdg-terminal-exec:1456` — `# saves or removes cache, forked out of the way`;
  `:1457` — `save_cache "$1" &` (A2).
- `xdg-terminal-exec:1418` — `set -- "${XTE__TITLEARG}${XTE__TITLEVAL}" "$@"`.
- `xdg-terminal-exec:1499` — `exec "$@"`.
- `xdg-terminal-exec:882` — `# Default in this case is to succeed` (NotShowIn tail; the
  fallback-id skip at 869-870 is never taken).
- `registration.md:54` — declares the warm-cache path and `-h/--help` out of contract, and nothing
  else that this map finds.

## Blockers

None. No lane or host state was modified; `xdg-terminal-exec` ran only inside bwrap with
`XDG_CACHE_HOME` under scratch and only with print/test argv; scratch was removed.
