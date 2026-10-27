# CritC1LsEnv — environment-semantics falsification

## Result

**Found a cold-path OOC enforcement hole and a concrete wrong-answer counterexample for `POSIXLY_CORRECT=1`.** The frozen fixture corpus itself contains none of the tested environment keys, so this does not alter its current score; it is a pre-data contract defect and must not be hidden by narrowing the predicate.

## Counterexample: POSIXLY_CORRECT cold cache

Reproduced using the round-47 pin `/usr/bin/xdg-terminal-exec` and draft `mado-terminal.py`, with a fresh app tree, no cache, a valid `TerminalEmulator` entry (`Exec=foot`), and `foot` executable on PATH. Both runs used the same explicit environment except for `POSIXLY_CORRECT=1`.

- Pin: exit **1**, stdout **empty**, stderr ends `No valid terminal entry was found in:`.
- Draft model: exit **0**, stdout **`foot\n`**, no OOC diagnostic.
- Draft with the same environment and a pre-existing cache: exit **2**, `MADO_TERM_OUT_OF_CONTRACT: POSIXLY_CORRECT set ...`.

The pin's failure occurs before its hash calculation: debug output reaches config reads but no entry is accepted; the final diagnostic has an empty search-directory list. The draft only checks `LS_ENV` inside `gen_hash`; code inspection shows `gen_hash` is called for cache validation (`read_cache`) but not when a cold resolver selects an entry. Therefore a cold invocation bypasses the OOC guard. This is both a violation of the declared OOC behavior and a silent wrong stdout/exit prediction for this environment.

Smallest safe correction: enforce the LS environment guard before selection on all invocation paths (and preserve OOC exit 2); separately, accurately represent the pin's cold POSIXLY_CORRECT failure if the intended contract is exact pin behavior. Do not change frozen predicates/fixtures in response; this is a miss to carry forward under the wave rules.

## GNU ls environment sweep

Differential harness called **`/usr/bin/ls -LRl`** (absolute path; this host's interactive command shell has a distinct `ls` builtin, so shell `ls` results were excluded) and compared stdout bytes against `lsemu.ls_lRL` on one fixed tree containing size-boundary files, quoted names, links, nested/empty directories, old/recent files, and DST-edge mtimes. Env was explicitly cleared for each run, with `LC_ALL=C`, `LANG=C`, `PATH=/usr/bin` plus the tested overlay. All rows returned ls rc=2 because one operand was intentionally missing; stdout was still compared.

| Environment | GNU stdout vs clean | Model vs GNU | Interpretation |
|---|---:|---:|---|
| `BLOCK_SIZE=1`, `512`, `1024`, `4096`, `human-readable`, empty, invalid; `LS_BLOCK_SIZE=1` and precedence combination | changed | differs | Hash listing changes (totals and/or size fields); all keys are in `LS_ENV`. |
| `POSIXLY_CORRECT=1` and empty | changed | differs | Total changes from 1024-byte to 512-byte blocks; key is in `LS_ENV`. |
| `TIME_STYLE=long-iso`, `full-iso`, `iso`, `+FORMAT`, empty | changed/error | differs | Date bytes change or ls errors; key is in `LS_ENV`. GNU ignores tested `posix-*` styles without `POSIXLY_CORRECT`; model matches those cases, but guard conservatively returns OOC when warm. |
| `QUOTING_STYLE=shell-always`, `escape`, `c`, `locale`, `clocale`, `shell` | changed | differs | Names/operands are quoted differently; key is in `LS_ENV`. Empty is ignored by GNU (warning) and model matches, but guard still rejects when warm. |
| `LS_COLORS` set/nonempty or empty | unchanged | matches | Plain `ls -LRl` output is a pipe, so no color is emitted; guard is conservative. |
| `TZ=UTC`, empty, `Pacific/Auckland`, `:Pacific/Auckland`, `EST5EDT`, `EST5`, invalid zone, `UTC0` | changed for zones affecting local display | matches all | `lsemu`'s `time.localtime` tracks GNU byte-for-byte, including the DST-edge fixture. `TZ` is intentionally not in `LS_ENV`. |
| `COLUMNS=1/1000`, `TABSIZE=1`, `CLICOLOR_FORCE=1`, `LS_OPTIONS=--color=always`, `TERM=xterm-256color`, `_POSIX2_VERSION=199209` | unchanged | matches | No effect on this `-LRl` pipe invocation. |

The instrumented sweep covers the listed environment names and extras above. For set LS variables, the tool correctly emits OOC **when the cache/hash path is reached**; `XTE_CACHE_ENABLED=0` skips hashing and both pin/tool return `foot\n`. On a true cold path, the draft does not hash, so the OOC guard does not run; for most LS variables stdout remains equal to the pin, but POSIXLY_CORRECT is the counterexample above.

## Frozen-counter context

The counter sandbox uses `bwrap --clearenv` and sets only each fixture's explicit environment plus its constructed HOME/PATH/LANG/cache values. A recursive JSON walk of all **204** frozen C1 fixtures found only `XDG_*`, `XTE_CACHE_ENABLED`, and `XTE_EXECARG_COMPAT` keys—none of `BLOCK_SIZE`, `LS_BLOCK_SIZE`, `POSIXLY_CORRECT`, `TIME_STYLE`, `QUOTING_STYLE`, `LS_COLORS`, `TZ`, or `COLUMNS`. Thus host environment cannot leak into scoring, and the current fixture set does not exercise this cold-path defect. Warm cases with an LS environment key would hit the OOC branch and fail against the pin oracle; do not infer that the cold-path hole is thereby covered.

## Evidence / commands

- `gnu_truth.py`: runs absolute `/usr/bin/ls -LRl` and model for the complete env matrix; output `sweep1/gnu_truth.txt`.
- `sweep.py`: first-pass SHA/length sweep; output `sweep1/sweep.tsv` (superseded for GNU identity by `gnu_truth.py`).
- `diff_tool_pin.py`: cold/warm/cache-disabled pin-vs-tool sweep; output `sweep1/diff.tsv`. The initial labels `cold` were not valid cold comparisons because the pin ran first and primed the cache; direct fresh-tree runs below corrected that interpretation.
- Direct fresh-tree pin/tool repro: exact command pattern used Python `subprocess.run` with explicit environment and `cwd=APP`: `/usr/bin/xdg-terminal-exec --print-cmd` versus `python3 -I <draft>/mado-terminal.py print --print-cmd`; `POSIXLY_CORRECT=1` yielded pin `(1, b'')` versus tool `(0, b'foot\n')`. Clean env yielded `(0, b'foot\n')` from both. Warm-cache tests yielded tool OOC as expected.
- Counter source evidence: `Box.prefix` uses `--clearenv`; `case_env` builds from fixture env; `gen_hash` checks `LS_ENV`; `read_cache` calls `gen_hash`; `select` reads cache before selecting paths; no cold-path hash call appears in runtime flow.
- The lane clone attempt was abandoned because the required 1 MiB file limit prevented writing the large Git index/checkout. No lane files or Git refs were changed.

Largest generated files observed: `sweep1/sweep.tsv` 10,260 bytes; `sweep1/gnu_truth.txt` under 1 MiB; `sweep1/diff.tsv` under 1 MiB. No package/tool installs. Scratch was cleaned before return.
