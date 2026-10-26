# Seat Report — `RevDeliveredTool` (round-41 w2, delivered `tools/mado-globals.py` review)

Full findings and reproductions: `.ufo/waves/round-41/w2/RevDeliveredTool/findings.md`.

## Summary & Verification Baseline
Reviewed `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:tools/mado-globals.py` (428 lines, byte-identical to `.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt`) as a delivered operator capability alongside `tools/mado-eventq.py` and `PRED-C1-r41-v2`.

- **Counter verification (`PRED-C1-r41-v2` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`):** `fixtures=39/39 tool=present verdict=TARGET_MET rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 nonce=8c2b2284a44fa9e1` (`clauses=a:1 b:1 b2:1 b3:1 g:1`, `selftest=63/63`, `b2 sites=18 killed=6/6 forced_dead=1`, `rc=0`).
- **Live host & committed journal runs:** `--live`, `--live --diff`, and `--journal-file .ufo/waves/round-41/fetch/xdph-journal.txt --diff` all exit `0` with empty stderr and produce byte-identical 67-line outputs (`sessions=2 latest_pid=1952 interfaces=63`, `focus-grab:1`, `verdict=OK`).
- **Wave-1 `RevRefTool` medium findings confirmed closed:** FIFO hang (`M1`) is closed by `O_NONBLOCK` + `stat.S_ISREG` (`read_file:229-245`, `rc=2 unreadable`); unbounded live stream memory (`M2`) is closed by chunked `os.read(fd, 65536)` + `proc.kill()` at `MAX_BYTES` (`read_live:195-214`, 300 MB writer stopped in `0.053s` at `54 MB` RSS, `rc=5 journalctl_too_large`).

## Findings (by severity; repros in `RevDeliveredTool/findings.md`)
All findings are **Low** severity operator-ergonomics / edge-case observations; none falsifies `PRED-C1-r41-v2` or requires blocking the round-41 data commit:

- **O1 (Low — `--help`/`-h` disabled and no usage docstring):** `add_help=False` (`:250`) and `ap.error` (`:256`) make `--help` and `-h` print `MADO_GLOBALS: SETUP usage` (`rc=2`) without listing valid flags, and the module docstring (`:1-25`) omits `--journalctl` and `--selftest` (unlike `mado-eventq.py`, `mado-options.py`, `mado-wsrules.py`, and `mado-verify.sh`, which exit `0` with help text). This is dictated by the counter's single-line `SETUP usage` contract.
- **O2 (Low — permission-denied live journal conflated with `NO_SESSIONS` or `journalctl_failed`):** Because `read_live` redirects `journalctl` stderr to `DEVNULL` (`:185`), an inaccessible `/var/log/journal` directory where `journalctl` prints `-- No entries --` on stdout and exits `0` reports `verdict=NO_SESSIONS` (`rc=3`), while an unreadable `.journal` file (`EACCES`, `journalctl` exit `1`) reports `SETUP journalctl_failed` (`rc=5`).
- **O3 (Low — `PATH` edge cases in `resolve_program`):** An unset/empty `PATH` splits to `[""]` (`:165`) and resolves bare `journalctl` to `./journalctl` in `cwd`; and a group-writable `journalctl` earlier in `PATH` halts the search with `SETUP journalctl_unusable` (`rc=5`, `:165-179`) instead of continuing to `/usr/bin/journalctl`.
- **O4 (Low — non-expert readability of multi-session and mixed-format verdicts):** `MADO_GLOBAL:` rows and the summary line (`interfaces=`, `classes=`, `verdict=`) reflect only the *latest* session (`sessions[-1]`), so without `--diff` a truncated/crashed latest session or a mixed-format file with `sessions >= 1` and `ignored > 0` still prints `verdict=OK` (`rc=0`).
- **O5 (Low — unhandled `BrokenPipeError` when piped to `head`):** Printing >64 KiB of output into a consumer that closes early (`| head -n 1`) raises an uncaught `BrokenPipeError` traceback on stderr (`:423-424`).

## Audited Clean (no defect found)
- Exit-code map (`0, 1, 2, 3, 4, 5`) matches the docstring and counter model on every path.
- Stdout/stderr discipline: all normal and `SETUP` paths emit structured `MADO_GLOBALS*` on stdout and empty stderr.
- Journal with no portal unit (`-- No entries --`): cleanly reports `verdict=NO_SESSIONS` (`rc=3`), including with `--diff` (`sessions=0 none`) and `--expect` (`NO_SESSIONS` precedence over `MISSING_EXPECTED`).
- Large inputs: 8 MiB boundary (`0.14s`), 500 MiB sparse file (`0.07s`, reads at most 9 MiB), single-line 8 MiB regex (`0.06s`, no catastrophic backtracking).
- Python version floor: clean stdlib AST floor of Python `>= 3.5`, verified on host Python `3.14.8`.

## Tooling & Safety
- No tools installed or updated; no pacman, compositor, socket, or mutating git/jj operations run.

Report: .ufo/waves/round-41/w2/RevDeliveredTool.md
