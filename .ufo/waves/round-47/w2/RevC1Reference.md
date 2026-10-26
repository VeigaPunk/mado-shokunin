# RevC1Reference — w2 FALSIFY report: reference-vs-script branch walk (C1, operability)

Walked `/usr/bin/xdg-terminal-exec` (= pinned `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`, verified identical, 1499 lines) line range by
line range against the L1 draft `.ufo/waves/round-47/l1-draft/mado-terminal.py` (1055 lines). Full table:
`.ufo/waves/round-47/w2/RevC1Reference/walk.md`; probe + e2e evidence: `evidence-probes.md`, `evidence-e2e.txt`,
harness `harness-e2e.py` (all under this dir). Ground truth obtained by probes on the host judge (bash 5.3.20
POSIX mode via `/bin/sh`) and an end-to-end real-vs-draft matrix: **14 AGREE / 4 DIVERGE**.

## Findings

### F1 — MEDIUM — undeclared OutOfContract: HOME unset (real selects, tool refuses)
- Attacks: `.ufo/waves/round-47/l1-draft/mado-terminal.py:406-407` (`raise OutOfContract("HOME unset")`,
  unconditional in `make_paths`); the reference expands `${HOME}` only inside `:-` defaults
  (`fetch/xdg-terminal-exec:148,168,172`), so with `XDG_CONFIG_HOME/XDG_DATA_HOME/XDG_CACHE_HOME` set the real
  resolver never touches `HOME` and selects normally. The contract docstring's out-of-contract list does NOT
  include HOME-unset, so this refusal narrows the declared domain ("Prints exactly what xdg-terminal-exec prints
  ... in the same environment").
- Repro (harness case `e2-home-unset`): env with `HOME` removed, all four XDG vars set, `foot.desktop` +
  `xdg-terminals.list`, `--print-id` → REAL rc=0 stdout `foot.desktop`; DRAFT rc=2 stderr
  `MADO_TERM_OUT_OF_CONTRACT: HOME unset`. Command: `python3 harness-e2e.py` (this seat dir; real run is
  `--print-id` only, `XDG_CACHE_HOME` per-tree).
- Class: clause f/g shape (stdout+rc agreement); NOT reachable at count time (clause i always sets
  `HOME=<root>/home`), so it cannot flip the round verdict — but it is a v2-re-registerable hole before data.

### F2 — MEDIUM — undeclared OutOfContract: PATH unset (real proceeds with bash's default path, tool refuses)
- Attacks: `l1-draft/mado-terminal.py:374` (`raise OutOfContract("PATH unset")` in `command_v`); reference
  consults PATH only via `command -v` (x:936, x:964). With PATH unset the host bash resolves bare words against
  its built-in default path — the real script picks `tr`/`find` up and can SELECT: harness `e3b-path-unset-exec-sh`
  (entry `Exec=sh`, PATH removed) → REAL rc=0 stdout `foot.desktop`; DRAFT rc=2
  `MADO_TERM_OUT_OF_CONTRACT: PATH unset`. `e3` (bare `Exec=foot` absent from the default path) → REAL rc=1
  "No valid terminal entry was found in: ..." vs DRAFT rc=2 — rc divergence even when stdout matches.
- Undeclared in the docstring OOC list; same class/reachability as F1.

### F3 — LOW — undeclared OutOfContract: HOME unset with defaults needed (real set -u death rc 1, tool rc 2)
- Harness `e2b-home-unset-default-paths` (HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_CACHE_HOME all removed):
  REAL rc=1, stderr `…/xdg-terminal-exec: line 148: HOME: unbound variable` (locator computed: line 148 is
  `for xte__dir in ${XDG_CONFIG_HOME:-"${HOME}/.config"}…`); DRAFT rc=2 OOC. stdout equal (empty) on both sides;
  the exit-status contract (`print … exits with its exit status`) is broken.

### F4 — INFO — stderr-text mismatches (not judged by PRED-C1 f, still model drift)
- Misspelled +/- entry lines: the reference strips the marker before the error (x:431 `xte__line=$_line`,
  error at x:467), the draft re-adds it (`l1-draft/mado-terminal.py:479`, `excl + line`).
- Redirect failure on an unreadable list: real stderr carries the shell prefix `…: line 361: <path>:
  Permission denied`, draft prints the bare path (stdout+rc agree: e18 both rc 1).
- `XTE_DEBUG`/`DEBUG` are read by the reference (x:61) and produce `D: ` stderr lines plus an `IFS=$XTE__LF`
  leak at x:1203/x:1205 that is neutralized because `find_entry` and every later split site sets IFS
  explicitly (x:920, x:934, x:1448) — no stdout/rc effect found; the two env names are absent from the
  docstring's environment list.

## Explicitly cleared (attacked, did not break)
- bash `read`-remainder rule (9 probes, incl. `x:y::`→`y::` and `--title=a:b=`→`a:b`): draft `read_split` exact.
- `printf %b`: `\NNN` octal, `\0NNN`, `\xHH`, ASCII `\uHHHH`, `\c`, unknown-escape literal — draft `printf_b` exact;
  non-ASCII `\u` divergence is OOC-DECLARED.
- `command -v`: `-`/`-x` fail; empty PATH entry and empty PATH value → cwd — wait, empty PATH *value* searches cwd
  (probe: `./foo` found) and draft models `d or cwd` — agree; x-bit FIFO found (non-regular, non-dir) — draft
  `_execable` agrees; builtin/keyword/function tables: 61/61 and 22/22 vs host bash 5.3.20, 24/24 script functions.
- Digit-leading entry IDs (`2048qt.desktop`): POSIX-mode bash expands those aliases (my first non-POSIX probe rc 127
  was an artifact); e1a/e1b AGREE.
- Option loop order incl. execarg-match-before-`--hold`, unknown-option discard, last `--print-cmd=` wins, empty
  delimiter, `--test` precedence (s1-s3, e15, e17 AGREE); empty-argv infinite loop is OOC-DECLARED.
- print modes: content+cmd composition, action suffix on id/path, `/./` fold, unterminated-last-line drop in
  content (e8, e12, e14 AGREE).
- errexit: unreadable list → rc 1 both sides (e18); loop-status carry cases (selftest) agree.
- IFS leaks (x:700 strip-fields early return; x:819/x:840/x:862 empty `;`-value loops; x:1203 debug lines): benign
  by static reachability — every later unquoted expansion sets IFS explicitly; no observable stdout/rc divergence.
- Docstring line citations all verified by computed `grep -n` locators (x:143, 179, 217, 300, 351, 477, 501, 561,
  694, 742, 754, 802, 970, 1020, 1039, 1055, 1113, 1133, 1144, 1179, 1224, 1457, 1499).

## Severity summary / recommendation
Three undeclared OutOfContract guards (F1-F3), one family: the draft refuses env states the contract docstring
never excluded, and the real script either selects (F1, F2) or exits 1 with a different shape (F3). None is
reachable under PRED-C1 clause i (sandbox always sets PATH and HOME), so the frozen counter cannot be flipped by
them; they are pre-data contract holes — v2 re-registration could either model them (HOME-unset-with-XDG-set →
proceed; HOME-unset-without → rc 1 + `HOME: unbound variable` stderr shape; PATH-unset → bash default path,
host-dependent) or declare them OOC in the docstring. The L1 decides; no data is affected.

## Residual risk and verification gaps
- IFS-leak benignness is static analysis, not an executed leak-observation case.
- `XTE_DEBUG=1` path inspected, not e2e-run (stderr-only by construction).
- Non-regular executables (FIFO) verified at `command -v` probe level only, not through a full selection.
- Non-UTF8 byte entries/delimiters and locale-variant filenames: not e2e-run (OOC-DECLARED class).
- The read/printf/table semantics are pinned to host bash 5.3.20 (the judge); other bash versions could drift —
  the counter's drift check covers the oracle, not the model's hardcoded tables.
- Selftest re-run here: `MADO_TERMINAL_SELFTEST: 43/43 passed`, exit 0 (clause s shape confirmed).

Tooling record: no tools installed or upgraded; no pacman; scratch was
/fast/scratch/hyaku/mado-r47/RevC1Reference (receipts copied into this dir, scratch deleted at seat end).
Every resolver invocation used a `--print-*` option and a per-tree `XDG_CACHE_HOME` inside scratch; no process
launched, no empty argv element passed.
