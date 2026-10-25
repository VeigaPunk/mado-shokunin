# Review findings — c1/ctl-ref-tool.py.txt (reference `tools/mado-globals.py`)

Reviewer seat: RevRefTool (round-41 w1). Object: the frozen reference at
`.ufo/waves/round-41/c1/ctl-ref-tool.py.txt` (346 lines; "it will likely be
the delivered tool"). Contract: `quality/counters/c1-r41-globals.py` docstring
(PRED-C1-r41-v1). Review is read-only; no file was modified.

## Score baseline (verification I exercised)

- Full counter run at lane tip rev `cd950ec781149040cc73d71cd67c2b67452e7724`
  with `--tool /tmp/revref/mado-globals.py` (copy of the reference):
  `fixtures=24/24 tool=present verdict=TARGET_MET`, clauses a:1 b:1 b2:1 g:1,
  `--selftest` 47/47 rc=0, b2 sites=12 killed=6/6. Matches
  `receipts/ctl-c1.txt` (47/47).
- Host live sanity (allowed journal verb only): `--live` returned 2 sessions
  (pid 1918, 8 interfaces; pid 1952 boot 7ab69e…, 63 interfaces),
  `hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab`, rc=0;
  `--live --diff` rc=0. Numbers agree with the fetch receipt `xdph-journal.txt`
  census (2 sessions, 63 distinct, one focus_grab advert pid 1952).

## Findings by severity

### M1 (Medium) — `--journal-file` on a FIFO hangs forever
- Attacks: the read-only census tool's robustness/availability contract
  (exit codes 2/3 are reachable for bad input, but there is no bound for this
  input class). Lines 194–196: `open(path, "rb")` on a FIFO blocks at `open`
  until a writer appears; no `os.stat` pre-check, no timeout in file mode.
- Repro:
  `mkdir -p /tmp/revref/probes && mkfifo /tmp/revref/probes/fifo`
  `timeout 4 python3 mado-globals.py --journal-file /tmp/revref/probes/fifo`
  → exits 124 (killed by `timeout`); without `timeout` it never returns.
- Practical trigger: a stale/leftover FIFO, or a user who points the flag at a
  named pipe. Suggestion: require `stat.S_ISREG` (as `resolve_program` already
  does for the live program) or open non-blocking; a directory is already
  handled correctly (SETUP unreadable, rc 2 — verified, no finding).

### M2 (Medium) — `--live` output cap is post-hoc; memory is unbounded before it
- Attacks: the claim "bounded output" (registration C1 / docstring
  "more than 8 MiB of output is SETUP journalctl_too_large"). Lines 179–189:
  `subprocess.run(..., stdout=subprocess.PIPE)` buffers the entire stream in
  memory; the `len(p.stdout) > MAX_BYTES` check runs only after EOF.
- Repro (300 MB fast writer):
  stub `dd if=/dev/zero bs=1M count=300 2>/dev/null`; measured child peak RSS
  **615 MB** (cap is 8 MiB, ~77×) before rc=5 `journalctl_too_large` printed.
  Enforced via `resource.getrusage(RUSAGE_CHILDREN)` in the probe driver.
- Root cause shared with L1; suggestion: stream with `Popen` and chunked reads,
  kill once accumulated bytes exceed MAX_BYTES (still stdlib-only, still honors
  the 30 s timeout).

### L1 (Low) — slow-but-large live output reports `journalctl_failed`, not `journalctl_too_large`
- Attacks: docstring line "more than 8 MiB of output is SETUP journalctl_too_large"
  is only decidable at EOF; the 30 s timeout wins first for slow producers.
  Lines 179–189 (timeout=30 in `subprocess.run`), 183 `SubprocessError` catch.
- Repro: stub `sleep 31; exit 1` → after 30.07 s rc=5 `SETUP journalctl_failed`
  (not too_large). A >8 MiB stream trickled over >30 s gets the same verdict —
  the size-bound claim is not honored for streaming output. Severity low in
  practice (both are rc 5; real journald output is ≪ 8 MiB).

### L2 (Low) — a non-executable-but-writable candidate earlier in PATH blocks a later valid program
- Attacks: PATH search semantics (docstring "found through PATH"). Lines 155–162:
  the loop stops at the first `isfile`+`X_OK` candidate, then lines 168–170
  reject it if group/other-writable — the later, valid entry is never tried.
- Repro: `PATH=/tmp/revref/probes/gwdir:/tmp/revref/probes/okdir`, both contain
  an executable `jc` (gwdir one chmod 775, okdir 755) →
  `--live --journalctl jc` → rc=5 `journalctl_unusable`, though a valid
  executable exists further down PATH. Shells continue searching; stricter here
  is not wrong per the contract, but it is an un-tested behavioral sharp edge
  (the tool is more brittle than the shell it replaces).

### L3 (Low) — TOCTOU between stat/access and exec in `resolve_program`
- Attacks: the live program's integrity decision (lines 154–171). The
  `os.stat`/`os.access` checks run before `subprocess.run` execs by path; a
  swap in between goes undetected. Not exploitable in the counter's sandbox
  (scratch read-only, cap-drop), and any actor able to write the containing
  directory owns the check anyway. Filed for completeness; a dirfd/`fexecve`
  fix is out of scope for the stdlib-only g clause.

### L4 (Low) — PATH unset/empty makes bare `journalctl` resolve to the working directory
- Attacks: `--live` program resolution when the environment has no PATH.
  Lines 156–157: `os.environ.get("PATH", "").split(":")`; an unset or empty
  PATH yields `[""]` → `d or "."` → cwd searched. Verified:
  `env -u PATH python3 mado-globals.py --live --journalctl stub.sh` in cwd
  finds and runs `./stub.sh`. This is POSIX-consistent (empty PATH entry =
  cwd) but means the tool's execution choice in a stripped environment depends
  on cwd; worth documenting, not a contract violation.

## Checks that passed (no finding)
- Directory passed to `--journal-file`: SETUP unreadable, rc 2, empty stderr
  (lines 193–197; `IsADirectoryError` is caught as OSError). Verified.
- Non-UTF-8 path (bytes 0xff/0xfe) as `--journal-file`: read fine, rc 3
  NO_SESSIONS, empty stderr (argv surrogateescape round-trips). Verified.
- Symlinked `--journalctl` program: runs (target checked via stat, incl. the
  group-writable-target rejection — rc 5). Verified.
- Python-keyword names ("class" global in journal; `--expect import`): accepted,
  reported `class=other` / listed missing; no crash. Verified.
- `ver 000001`: parsed as 1 (int()), matches the model. Verified.
- Huge counts (20 000 adverts, fixture gen7) and 129-char names: fixture pass.
- Exit codes and stdout/stderr discipline: usage/unreadable/too_large → rc 2,
  journalctl_* → rc 5, NO_SESSIONS → rc 3, MISSING_EXPECTED → rc 1, OK → rc 0;
  every path tested showed the report on stdout, empty stderr (ap.error override
  suppresses argparse's stderr usage text). Verified.
- `--expect` duplicates dedupe + sort; `--diff` ordering/format; verdict
  precedence NO_SESSIONS > MISSING_EXPECTED: all match the model byte-exactly
  (24/24 fixtures + explicit probes).

## Residual risk / verification gaps
- The 24 fixtures and b2 mutation sweep cover the parser, class table, env/argv
  hygiene, and the unreadable/too_large/usage/live exit paths; they do not
  exercise FIFO input, unbounded buffering, slow-stream overlap, or PATH search
  precedence — exactly the gaps above.
- `--live` on the running desktop is reported, not scored (registration
  "Residuals": host receipt). My host run is the receipt evidence.
- All findings carry concrete repro commands; none required any mutation of the
  lane, fleet, or host. Scratch (/tmp/revref) removed after this report.
