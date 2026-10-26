# Review Findings — `tools/mado-globals.py` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`

- **Seat:** `RevDeliveredTool` (round-41 wave `w2`, operator-use & delivered-capability review)
- **Target:** `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:tools/mado-globals.py` (428 lines, sha256 identical to `.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt`)
- **Comparison peer:** `tools/mado-eventq.py` (285 lines) and sibling `tools/mado-*.py`
- **Predicate contract:** `quality/counters/c1-r41-globals-v2.py` (`PRED-C1-r41-v2`)

---

## 1. Exercised Verification Baseline (Live Host, Committed Journal, Counter)

1. **`PRED-C1-r41-v2` counter on `07f2641696b5ac73de1404ea737a9f27e9819aa1`:**
   - Command: `python3 -I quality/counters/c1-r41-globals-v2.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1`
   - Result (72.05 s, `rc=0`):
     - `PRED-C1-r41-v2 clause=b rc=0 selftest=63/63`
     - `PRED-C1-r41-v2 clause=b2 sites=18 killed=6/6 forced_dead=1`
     - `PRED-C1-r41-v2 clause=b3 variant=comment rc=0 selftest=63/63 ok=1`, `variant=unparse rc=0 selftest=63/63 ok=1`
     - `PRED-C1-r41-v2 clauses=a:1 b:1 b2:1 b3:1 g:1`
     - `PRED-C1-r41-v2: fixtures=39/39 tool=present verdict=TARGET_MET rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 nonce=8c2b2284a44fa9e1`

2. **Live host execution (`--live`, `--live --diff`, `--live --expect`):**
   - Command: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-globals.py --live --diff`
   - Result (`rc=0`, empty stderr, 67 lines on stdout):
     - `MADO_GLOBALS_SESSION: n=1 boot=- pid=1918 first=2026-10-25T13:16:45-03:00 last=2026-10-25T13:16:45-03:00 interfaces=8 adverts=15`
     - `MADO_GLOBALS_SESSION: n=2 boot=7ab69ee4149c4811a3faf6c08c9d119b pid=1952 first=2026-10-25T13:36:24-03:00 last=2026-10-25T13:36:24-03:00 interfaces=63 adverts=63`
     - 63 `MADO_GLOBAL:` lines sorted bytewise (including `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab`)
     - `MADO_GLOBALS_DIFF: from=1 to=2 added=<55 names> removed=- ver_changed=-`
     - `MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK`
   - `--live --expect hyprland_focus_grab_manager_v1` -> `rc=0`, `verdict=OK`.
   - `--live --expect nonexistent_proto_v1` -> `rc=1`, `expected_missing=nonexistent_proto_v1 ignored=0 verdict=MISSING_EXPECTED`.

3. **Committed journal execution (`.ufo/waves/round-41/fetch/xdph-journal.txt`):**
   - Command: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-globals.py --journal-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/fetch/xdph-journal.txt --diff`
   - Result (`rc=0`, empty stderr, 67 lines on stdout): byte-identical (`out_live == out_file` is `True`) to `--live --diff`.

4. **Confirming wave-1 `RevRefTool` medium findings are closed in v2:**
   - **M1 (FIFO hang):** `tools/mado-globals.py:229-245` (`read_file`) now opens with `os.O_RDONLY | os.O_NONBLOCK` and checks `stat.S_ISREG(os.fstat(fd).st_mode)`, returning `rc=2` (`MADO_GLOBALS: SETUP unreadable`) immediately on a FIFO or directory.
   - **M2 (unbounded live memory buffering):** `tools/mado-globals.py:182-225` (`read_live`) now reads incrementally in 65536-byte chunks via `select.select` and kills `proc` immediately once `total > MAX_BYTES`. Tested with a 300 MB fast writer (`dd if=/dev/zero bs=1M count=300`): completed in `0.053s`, `rc=5` (`MADO_GLOBALS: SETUP journalctl_too_large`), child peak RSS `54,168 KB` (down from `615 MB` in w1).

---

## 2. Findings by Severity (Operator-Use & Delivered Capability Attack)

### Finding O1 (Low / Operator Usability & CLI Contract) — `--help` and `-h` are disabled and indistinguishable from a syntax error (`rc=2`, `MADO_GLOBALS: SETUP usage`)

- **Attacks:** `tools/mado-globals.py:249-260` (`run`: `argparse.ArgumentParser(prog="mado-globals", add_help=False, allow_abbrev=False)` and `ap.error = lambda msg: (_ for _ in ()).throw(Setup("usage"))`), and the module docstring (`tools/mado-globals.py:1-25`), which omits any `Usage:` or CLI flags section.
- **Evidence & Comparison with `tools/mado-eventq.py`:**
  - `mado-eventq.py:209` uses standard `argparse.ArgumentParser(description="Read-only Hyprland socket2 subscriber census.")` (with `add_help=True`) and documents all flags in its docstring (`:64-75`). Running `python3 -I tools/mado-eventq.py --help` (or `-h`) exits `0` and prints full flag help on stdout; `mado-options.py`, `mado-wsrules.py`, `mado-evidence-audit.py`, `mado-assessment.py`, `mado-action-plan.py`, and `mado-verify.sh` all likewise exit `0` with usage text on `--help`/`-h`.
  - In `tools/mado-globals.py`, `--help` and `-h` are rejected as unknown flags by `add_help=False`, triggering `Setup("usage")` (`rc=2`, stdout `MADO_GLOBALS: SETUP usage`, empty stderr) without naming a single valid flag (`--journal-file`, `--live`, `--journalctl`, `--expect`, `--diff`, `--selftest`). Even reading the module docstring (`:1-25`) does not show `--journalctl` or `--selftest`.
  - Note: this behavior is coupled to the `PRED-C1-r41-v2` contract (`quality/counters/c1-r41-globals-v2.py:32-34`: "Setup failure: stdout is exactly one line `MADO_GLOBALS: SETUP <reason>`"), so it is not a counter failure, but it is a concrete operator usability defect.
- **Repro:**
  ```sh
  python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-globals.py --help
  # stdout: MADO_GLOBALS: SETUP usage
  # stderr: (empty)
  # exit: 2
  ```

### Finding O2 (Low / Live Journal Diagnostics) — Permission-denied or missing user journal in `--live` mode is conflated with `NO_SESSIONS` (`rc=3`) or generic `journalctl_failed` (`rc=5`) because `journalctl` stderr is discarded

- **Attacks:** `tools/mado-globals.py:182-187` (`subprocess.Popen(..., stderr=subprocess.DEVNULL)`) and `tools/mado-globals.py:217-224` (`if rc != 0: raise Setup("journalctl_failed", 5)`).
- **Evidence:**
  - `systemd`'s `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` has two distinct failure behaviors when the user cannot read journal files, depending on whether the directory or the `.journal` file denies access:
    1. **Unreadable journal directory (e.g. `/var/log/journal/<machine-id>` mode `000` or absent, and no `/run/log/journal`):** `journalctl` writes `No journal files were found.` to stderr, writes `-- No entries --` to stdout, and **exits `0`**. Because `mado-globals.py` discards `stderr` to `DEVNULL` and ignores `-- No entries --`, it reports `MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- expected_missing=- ignored=0 verdict=NO_SESSIONS` (`rc=3`). An operator cannot distinguish "permission denied / no journal storage accessible" from "journal storage is readable, but `xdg-desktop-portal-hyprland` has never logged a session".
    2. **Unreadable `.journal` file inside a readable `<machine-id>` directory (`user-1000.journal` mode `000`):** `journalctl` writes `No journal files were opened due to insufficient permissions.` to stderr, writes nothing to stdout, and **exits `1`**. `mado-globals.py` discards stderr and collapses this into `MADO_GLOBALS: SETUP journalctl_failed` (`rc=5`), indistinguishable from a timeout, bad arguments, or killed process.
- **Repro:**
  ```sh
  # Case 1: unreadable /var/log/journal directory -> journalctl exits 0 with stderr warning, tool reports NO_SESSIONS (rc=3)
  bwrap --unshare-all --cap-drop ALL \
    --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin \
    --proc /proc --dev /dev --tmpfs /tmp --tmpfs /run \
    --ro-bind /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-globals.py /tmp/mado-globals.py \
    -- /usr/bin/python3 -I /tmp/mado-globals.py --live
  # stdout: MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- expected_missing=- ignored=0 verdict=NO_SESSIONS
  # exit: 3

  # Case 2: unreadable .journal file -> journalctl exits 1 ("insufficient permissions"), tool reports SETUP journalctl_failed (rc=5)
  ```

### Finding O3 (Low / PATH Resolution Semantics) — `resolve_program` searches `cwd` when `PATH` is unset/empty or contains an empty component, and stops at the first group-writable candidate in `PATH` instead of continuing

- **Attacks:** `tools/mado-globals.py:163-180` (`resolve_program`).
- **Evidence:**
  1. **Unset/empty `PATH` searches `cwd` (`.`):** At line 165, `os.environ.get("PATH", "").split(":")` produces `[""]` when `PATH` is unset or empty, and `os.path.join(d or ".", prog)` resolves bare `"journalctl"` to `./journalctl` in the current working directory. While POSIX `execvp` treats an empty `PATH` entry (`:/usr/bin`) as `.`, an *unset* `PATH` in `resolve_program` silently executes `./journalctl` from `cwd`.
  2. **Early termination on group/other-writable candidate in `PATH`:** At lines 165-169, the loop breaks on the first directory in `PATH` where `os.path.isfile(cand) and os.access(cand, os.X_OK)` is true, and then lines 177-179 reject `cand` with `Setup("journalctl_unusable", 5)` if `st.st_mode & (stat.S_IWGRP | stat.S_IWOTH)` is non-zero — even when a valid `0755` `/usr/bin/journalctl` exists later in `PATH`.
- **Repro:**
  ```sh
  # 1. Unset PATH runs ./journalctl from cwd:
  D=$(mktemp -d)
  printf '#!/bin/sh\nprintf "2026-10-25T13:36:24-03:00 h xdg-desktop-portal-hyprland[99]: [LOG]  | Got interface: wl_seat (ver 9)\\n"\n' > "$D/journalctl"
  chmod 0755 "$D/journalctl"
  (cd "$D" && env -i /usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-globals.py --live)
  # stdout ends with: MADO_GLOBALS: sessions=1 latest_pid=99 ... verdict=OK (rc=0)
  rm -rf "$D"

  # 2. Group-writable earlier PATH entry blocks valid /usr/bin/journalctl:
  D=$(mktemp -d)
  printf '#!/bin/sh\nexit 0\n' > "$D/journalctl"
  chmod 0775 "$D/journalctl"
  PATH="$D:/usr/bin" /usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-globals.py --live
  # stdout: MADO_GLOBALS: SETUP journalctl_unusable (rc=5)
  rm -rf "$D"
  ```

### Finding O4 (Low / Non-Expert Readability & Partial-Session Trap) — Summary line and `MADO_GLOBAL:` rows report only the latest session while `sessions=k` counts all sessions, and mixed-format journals with `>=1` valid session still report `verdict=OK` (`ignored > 0`)

- **Attacks:** `tools/mado-globals.py:118-160` (`report`) and module docstring (`:16-24`).
- **Evidence:**
  1. **Partial/truncated latest session:** On this host (`xdph-journal.txt`), session 1 (`pid=1918`) has `interfaces=8 adverts=15` (a truncated mid-stream slice) and session 2 (`pid=1952`) has `interfaces=63 adverts=63`. If the ordering is reversed (e.g., a portal restart crashed mid-startup after logging 1 interface, or a user journal slice ends mid-startup), `MADO_GLOBALS_SESSION: n=1` prints `interfaces=63`, `MADO_GLOBALS_SESSION: n=2` prints `interfaces=1`, and the `MADO_GLOBAL:` table plus final summary `MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=1 ... verdict=OK` report **only** the 1 interface of session 2 (`rc=0`). Without `--diff` (which prints `removed=<62 interfaces>`), a non-expert reading `verdict=OK` can miss that 62 interfaces vanished compared to the prior session.
  2. **Mixed-format journal with `ignored > 0` and `sessions >= 1`:** Docstring lines 13-16 state: *"A line that contains `Got interface: ` but does not match it (another -o format, a different level, a different spacing) is counted in `ignored=`; an input whose every advert is ignored is UNRECOGNIZED_FORMAT (exit 4), never a silent NO_SESSIONS."* When a file concatenates a `-o short` capture (or `short-iso-precise`, or ISO-8601 `Z` suffix) with even a single `-o short-iso` session (as in fixture `mixed0`), `verdict` is `OK` (`rc=0`) and only `ignored=N` indicates that earlier sessions were skipped due to format mismatch.
- **Repro:**
  ```sh
  D=$(mktemp -d)
  printf 'Oct 25 13:16:45 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: hyprland_focus_grab_manager_v1 (ver 1)\n2026-10-25T13:36:24-03:00 plazir27 xdg-desktop-portal-hyprland[1952]: [LOG]  | Got interface: wl_seat (ver 9)\n' > "$D/mixed.log"
  python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-globals.py --journal-file "$D/mixed.log"
  # MADO_GLOBALS: sessions=1 latest_pid=1952 interfaces=1 classes=other:1 expected_missing=- ignored=1 verdict=OK (rc=0)
  rm -rf "$D"
  ```

### Finding O5 (Low / Operator Pipeline Discipline) — Piping large output to a pager/filter that closes early (`| head`) emits an unhandled `BrokenPipeError` traceback on stderr

- **Attacks:** `tools/mado-globals.py:422-424` (`for line in lines: print(line)` without catching `BrokenPipeError` or setting `SIGPIPE` to `SIG_DFL`).
- **Evidence:** When a journal has many sessions (or `MADO_GLOBAL` lines exceed the 64 KiB pipe buffer) and an operator pipes `mado-globals.py` into `head -n 1`, Python's default `SIGPIPE` handler raises `BrokenPipeError` inside `print(line)`, dumping a multi-line traceback to stderr and exiting `120`/`1`.
- **Repro:**
  ```sh
  D=$(mktemp -d)
  python3 -c '
  for i in range(1, 2001):
      print(f"2026-10-25T13:36:24-03:00 plazir27 xdg-desktop-portal-hyprland[{i}]: [LOG]  | Got interface: wl_seat (ver 9)")
  ' > "$D/many.log"
  python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-globals.py --journal-file "$D/many.log" | head -n 1
  # stderr: Traceback (most recent call last): ... BrokenPipeError: [Errno 32] Broken pipe
  rm -rf "$D"
  ```

---

## 3. Audited Dimensions with No Defect Found (Verified Clean)

1. **Exit-code map vs docstring (`tools/mado-globals.py:21-24` vs `quality/counters/c1-r41-globals-v2.py:29-100`):**
   - Docstring (`:21-24`): `Exit: 0 OK, 1 MISSING_EXPECTED, 3 NO_SESSIONS, 4 UNRECOGNIZED_FORMAT, 2 usage/input (MADO_GLOBALS: SETUP <reason> on stdout), 5 live journal failure.`
   - Verified every exit code and setup reason in code:
     - `0`: `verdict=OK` (`report:153`)
     - `1`: `verdict=MISSING_EXPECTED` (`report:151`, or failed `--selftest` at `:413`)
     - `2`: `MADO_GLOBALS: SETUP usage|bad_expect|unreadable|too_large` (`Setup` default `code=2` at `:74`, raised at `:232,235,242,246,257,260,262,264,267`)
     - `3`: `verdict=NO_SESSIONS` (`report:149`)
     - `4`: `verdict=UNRECOGNIZED_FORMAT` (`report:147`)
     - `5`: `MADO_GLOBALS: SETUP journalctl_unusable|journalctl_failed|journalctl_too_large` (`Setup(..., 5)` at `:170,175,179,193,204,212,221,223`)
   - Note: `--selftest` returning `0` (pass) / `1` (fail) is omitted from the module docstring's 25-line header (it is documented in the counter docstring at `c1-r41-globals-v2.py:128-130`).

2. **Stdout/stderr discipline:**
   - Every normal verdict (`0, 1, 3, 4`) and every `Setup` failure (`2, 5`) writes structured `MADO_GLOBALS*` lines to `stdout` and `0` bytes to `stderr`.
   - Verified across all 39 counter fixtures and direct probes (`usage`, `bad_expect`, `unreadable`, `too_large`, `journalctl_unusable`, `journalctl_failed`, `journalctl_too_large`).

3. **Journal with no portal unit (`-- No entries --` or empty file):**
   - Tested against real `journalctl --user -u nonexistent-portal-unit-r41 --no-pager -o short-iso` output (`-- No entries --\n`, `rc=0`):
     - Plain: `MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- expected_missing=- ignored=0 verdict=NO_SESSIONS` (`rc=3`).
     - With `--expect hyprland_focus_grab_manager_v1`: `expected_missing=hyprland_focus_grab_manager_v1 ignored=0 verdict=NO_SESSIONS` (`rc=3` — `NO_SESSIONS` takes precedence over `MISSING_EXPECTED` per contract).
     - With `--diff`: prints `MADO_GLOBALS_DIFF: sessions=0 none` followed by `verdict=NO_SESSIONS` (`rc=3`).

4. **Large inputs & algorithmic complexity (`--journal-file` and `--live`):**
   - `--journal-file` at exactly `8,388,608` bytes (`76,260` adverts): completes in `0.143s`, `rc=0`.
   - `--journal-file` at `8,388,609` bytes (`8 MiB + 1 B`): completes in `0.064s`, `rc=2` (`SETUP too_large`).
   - `--journal-file` on a `500 MiB` file: reads at most `9 MiB` (`while len(data) <= MAX_BYTES: os.read(fd, 1 << 20)`) and exits in `0.071s`, `rc=2` (`SETUP too_large`).
   - `--journal-file` single `8 MiB` line with no newline and `Got interface: `: `ADVERT.fullmatch` fails without catastrophic backtracking in `0.063s`, `rc=4` (`ignored=1 verdict=UNRECOGNIZED_FORMAT`).
   - `--live` with a `300 MB` fast writer: killed at `8 MiB + 64 KiB` in `0.053s`, `rc=5` (`SETUP journalctl_too_large`), child max RSS `54 MB`.

5. **Python version floor:**
   - AST inspection of `tools/mado-globals.py` confirms **Python >= 3.5** is the exact floor (`re.Pattern.fullmatch` added in 3.4; `subprocess.SubprocessError` in 3.3; `time.monotonic` in 3.3; `tempfile.TemporaryDirectory` in 3.2; `ArgumentParser(allow_abbrev=...)` in 3.5). It uses `%` string formatting throughout (no f-strings, no walrus `:=`, no `match`/`case`, no `tomllib`), making it the most backwards-compatible tool in `tools/`. Runs cleanly under the host's Python `3.14.8` with `python3 -I`.

6. **Comparison with `tools/mado-eventq.py` style & readability:**
   - **Shared strengths:** Both use `TAG_SECTION: key=val ...` line-oriented records ending in a single `TAG: ... verdict=V` summary line; both use `Setup(Exception)` mapped to `TAG: SETUP <reason>`; both are stdlib-only and socket-free.
   - **Where `mado-globals.py` is stronger than `mado-eventq.py`:**
     - Bounded file and live stream reads (`8 MiB` cap, `O_NONBLOCK` + `S_ISREG` check against FIFOs/devices, `30s` monotonic deadline with `proc.kill()`), whereas `mado-eventq.py:113` does unbounded `open(path).read()`.
     - Sanitizes subprocess environment (`PATH`, `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS`, `LC_ALL`) and verifies executable permissions (`!S_IWGRP & !S_IWOTH`) before spawning.
     - Includes an embedded 63-assertion `--selftest` (`mado-eventq.py` has no `--selftest`).
     - Detects format mismatches via `ignored=` and `UNRECOGNIZED_FORMAT` (`rc=4`).
   - **Where `mado-eventq.py` is stronger for an operator:**
     - Supports `-h`/`--help` (`rc=0`) and runs `--live` by default when given no arguments (`mado-globals.py` exits `2` with `MADO_GLOBALS: SETUP usage` on both `[]` and `--help`).
     - Includes an 80-line operator manual in its module docstring explaining every output column, failure marker, and flag default.

---

## 4. Tooling & Safety Attestation

- No tools were installed or updated.
- No pacman, service, compositor, Wayland socket, or mutating git/jj commands were run.
- Only the allowed read-only `journalctl --user -u <unit> --no-pager -o short-iso` verb was executed.
- All temporary directories created under `/tmp` during probing were removed.
