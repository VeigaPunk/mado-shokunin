# ExecOracle — w1 round 47: the bwrap oracle for the pinned xdg-terminal-exec

STATUS: COMPLETE. Scope: `.ufo/waves/round-47/w1/ExecOracle/` only (harness + receipts + demo
fixtures generated from host runs). No tracked file edited, no git/jj mutation, no pacman, nothing
installed, no terminal or GUI launched, no compositor mutation.

Delivered code (sha256):

| file | sha256 | lines |
|---|---|---|
| `.ufo/waves/round-47/w1/ExecOracle/oracle.py` | `2b5c7f4167b2c3175d2b0413ba47502682b065b0782dd8f589c2cb1a52c2a5a6` | 1066 |
| `.ufo/waves/round-47/w1/ExecOracle/gen-demo-fixtures.py` | `97da1bd9554624a2e8384fe31f816275f8e4f4b98fece14b9e6dc0feae6273a3` | 407 |
| `receipts/fixtures-demo.json` | `f65b1f291aa37366c620b2fd1f89f5b8dc7f91cc7672e34627b29d85e3103e4a` | 16 cases |

`oracle.py`'s own sha256 is recorded inside every `run.json` (`code_sha256`) together with the
fixtures sha256 and the pin sha256, so a receipt names the exact code that produced it.

## 1. Interface

```
oracle.py run   --fixtures F.json --work DIR [--tool T] [--receipts R]
                [--repeat N] [--timeout S] [--alt-work DIR] [--allow-timeout]
oracle.py trace --fixtures F.json --work DIR [--receipts R] [--limit N]
oracle.py bin   --work DIR [--tool T] [--receipts R]        # materialize bin/ + pin/ only
```

* `run` materializes each case of the frozen schema under `DIR/<id>/` (files, executable stubs),
  copies the pinned script to `DIR/pin/xdg-terminal-exec` after checking sha256
  `89f2be9a…27ac` (source `/usr/bin/xdg-terminal-exec`, sha256 re-checked on every invocation),
  then runs the pinned script with the case args in a fresh bwrap sandbox. With `--tool T` the same
  case, env and sandbox are used to run `T print <args>` and both results are compared.
* Per case output: `rc`, `stdout` with the case root replaced by `$ROOT`, `stdout_sha256`,
  `stderr_digest` (`sha256:<hex>` of stderr, root-normalized), `stderr_bytes`, `stderr_head`,
  `stub_ran`, `timed_out`, `duration_ms`, plus three repeat fingerprints and the alt-root
  fingerprint; `cases.tsv` carries the same columns.
* Timeout: every run has a hard per-case budget (`--timeout`, default 30 s). A run that does not
  answer is killed (bwrap `--die-with-parent`, plus SIGKILL of the bwrap child), reported with
  rc 124 and `timed_out=yes`, and it fails the harness — a hanging oracle is not an answer. With
  `--allow-timeout` a timeout is comparable only when `expect.rc` is 124 (opt-in, recorded in
  `run.json` as `allow_timeout`).
* Exit status: `0` every checked property held, `1` expect mismatch / non-determinism / root
  dependence / executed stub / tool differs / invalid fixture, `2` usage error.
* Fixture handling: `$ROOT` is substituted in env values, in materialized file contents and in
  args; a `{"cases": [...]}` wrapper is accepted as well as a bare list; `expect` may be absent
  (reported `no_expect`, not an error); duplicate ids, unsafe ids (`/`, `..`, reserved `bin`,
  `pin`, `tool`, `receipts`) and unsafe relative paths are rejected as invalid instead of run.
* Safety guards: `env` may not set `HOME`, `PATH` or `XDG_CACHE_HOME` (harness-controlled); a case
  whose args contain no `--print-*` / `--test` is refused with `INVALID` — it would launch a
  terminal. Unknown env keys are passed through and listed in `extra_env` (forward compatibility).
* `exec` entries are made `0755`; a missing or non-`#!` file there is replaced by a stub that
  appends `STUB-RAN $0 $*` to `<ROOT>/.oracle-rw/stub-ran` and exits 1, so "a terminal was
  launched" is a recorded failure, not an inference.

## 2. The sandbox (exact argv)

Template as written to `receipts/sandbox-argv.txt` (one real invocation, `<WORK>`/`<ROOT>`
abstracted; a scratch path is never citable evidence):

```
/usr/bin/bwrap
  --unshare-all --die-with-parent --new-session --clearenv
  --ro-bind /usr/lib /usr/lib
  --symlink usr/lib /lib
  --symlink usr/lib /lib64
  --ro-bind /usr/bin/bash /bin/sh
  --ro-bind /usr/bin/bash /bin/bash
  --ro-bind <WORK>/bin /oracle/bin
  --ro-bind <WORK>/pin/xdg-terminal-exec /oracle/xdg-terminal-exec
  --dev /dev
  --proc /proc
  --tmpfs /tmp
  --ro-bind <ROOT> <ROOT>
  --bind <ROOT>/.oracle-rw <ROOT>/.oracle-rw
  --chdir /
  --ro-bind /usr/bin/python3 /usr/bin/python3      # only with --tool
  --ro-bind /usr/bin/env /usr/bin/env              # only with --tool
  --ro-bind <WORK>/tool/<tool> /oracle/tool        # only with --tool
  --setenv <CASE ENV KEYS, $ROOT substituted>
  --setenv HOME <ROOT>/home
  --setenv PATH <ROOT>/bin:/oracle/bin
  --setenv XDG_CACHE_HOME <ROOT>/.oracle-rw/cache
  /oracle/xdg-terminal-exec <case args>            # or /oracle/tool print <case args>
```

The sandbox root is a fresh tmpfs; the only host content is read-only: `/usr/lib` (shared objects
and `ld-linux`), `/usr/bin/bash` at `/bin/sh` and `/bin/bash` (this host has no dash), the
externals, the pin, the case root, and (`--tool`) python3 + env. `--chdir /` removes any host cwd
from the picture; `--die-with-parent` makes a stuck run die with the harness; `--timeout` is
enforced on top (rc 124, flagged `timed_out`).

A real blocking vector exists and is receipted (`receipts/fifo-hang-proof.txt`): the entry scan
binds `-type f` only to the *first* find path group (`:766` sets it, `:774` joins the rest with
`-o`), so a named pipe named `*.desktop` in the last applications directory — which is
`XDG_DATA_HOME/applications`, because `make_paths` prepends each dir while walking
`XDG_DATA_HOME` then `XDG_DATA_DIRS` — is discovered and then opened, and the resolver blocks in
`open(2)`. The proof materializes exactly that case, runs it through `run_once()` with a 3 s
budget and observes `rc=124 timed_out=True duration_ms≈3003`, `stdout=''`, no reader left on the
FIFO (non-blocking `O_WRONLY` open returns ENXIO) and no process whose argv names the case root.
Namespace teardown after the kill is normally immediate (0 ms in three consecutive proofs); the
check polls for up to 5 s so an asynchronous teardown is not misread as residue. Independently
reported by SentHost-3 (`w1/SentHost/receipts/fifo-hang.txt`).

No-network, as measured (`receipts/netns-probe.txt`, same flags):

```
connect 127.0.0.1:53 rejected: Connection refused (errno 111)
dns example.com failed: gaierror
udp bind ok
interfaces: lo
```

Filesystem isolation, as measured (`receipts/isolation-probe.txt`, same flags): `/usr/bin`, `/home`,
`/fast`, `/etc`, `/etc/xdg`, `/usr/share`, `/usr/share/applications`, `/var`, `/run` are all absent;
the root listing is `bin dev lib lib64 oracle proc tmp usr`; `command -v` sees exactly
`tr find awk ls md5sum mkdir rm` from `/oracle/bin` and nothing else (`sh`, `bash`, `python3`,
`alacritty`, `xdg-terminal-exec` are not on PATH).

`/oracle/bin` contents were derived, not guessed. `oracle.py trace` runs the pinned script under
`strace -f -e trace=execve`, once inside the sandbox and once directly on the host (print modes
only, `XDG_CACHE_HOME` redirected into scratch, so the background cache saver completes), over all
16 demo cases:

```
TRACE_EXT:      awk find mkdir tr                 # sandbox census
HOSTTRACE_EXT:  awk find ls md5sum rm tr          # host census (foreground + cache saver)
```

Union = `tr find awk ls md5sum mkdir rm` = `EXTERNALS` in `oracle.py`; `receipts/trace.txt`,
`receipts/trace-execve.json`, `receipts/bin-manifest.tsv` (each external with its host path and
sha256; `/bin/sh` = `/usr/bin/bash` sha256 `c14c8f49…358d`). Any execve of a path outside
`/oracle/bin`, `/bin/sh`, `/bin/bash` and the pin makes `trace` exit 1 (`TRACE_MISSING`).

Script facts used here, locators recomputed by grep (`receipts/script-locators.txt`):
cache file at `${XDG_CACHE_HOME}/xdg-terminal-exec` (:173), entry scan `LC_ALL=C find -L "$@"`
(:795), cache saver forked with `save_cache "$1" &` (:1457), terminal launch `exec "$@"` (:1499),
`Hidden` check (:938), `TryExec` check (:933), `TerminalEmulator` check (:817).

## 3. Evidence

E1 pin. `receipts/pin.txt`: source `/usr/bin/xdg-terminal-exec`, expected = copied sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`. `prepare()` refuses to run
when the host script or its copy does not match.

E2 fidelity of the sandbox against the host. 16 demo cases, `expect` produced **only** by running
the pinned script directly on the host on the materialized case (print modes only, cache in
scratch, PATH = case `bin` + a directory holding only the 7 externals, so the host run sees no
extra commands): `ORACLE cases=16 valid=16 match=16 mismatch=0`. Every rc and every stdout byte
matches (`receipts/cases.tsv`, `receipts/run.json`, `receipts/host-reference.json`). Classes
covered: config list wins, fallback scan, Hidden, wrong category, TryExec missing, listed id
absent, action id (`ID:Action`), OnlyShowIn, `XDG_CURRENT_DESKTOP=GNOME:Hyprland` list order,
print delimiters (`--print-delimiter=,` + `--print-cmd=|`), no terminal (rc 1), data-dir
precedence, `TerminalArgAppId/Title/Dir/Hold` + extra argv, `/disable_cache`, Exec quoting/field
codes, `--print-content` on a 2000-line entry.

E3 determinism. `--repeat 3` per case with the per-run dir wiped between runs, plus a full second
work root (`<WORK>-altroot`, own bin/pin copies): 16/16 identical fingerprints on all three
measures (rc, stdout sha256, stderr digest) and identical after root substitution across roots —
`receipts/determinism.txt` ends `ALL_DETERMINISTIC_AND_ROOT_INDEPENDENT: YES`. Sample: `c16` rc 0
stdout `ac04203f1d58293f…`, stderr digest `e3b0c442…` (empty) on all runs and both roots.

E4 comparator, positive control. `--tool receipts/controls/tool-exact.sh` (a shim that re-execs
the pinned script; self-test only, not a re-implementation): `tool_match=16 tool_differ=0`,
`ORACLE_RESULT: PASS`.

E5 comparator, negative control. `tool-echo.sh` (constant `bogus-tool`): `tool_differ=16/16`, each
with `rc`/stdout shown, `ORACLE_RESULT: FAIL`, exit 1.

E6 tripwire. `tool-tripwire.sh` runs the case stub: `tool_stub_ran=13/16` (the 3 cases without
`bin/alacritty` cannot), the stub marker received `STUB-RAN …` lines, `ORACLE_RESULT: FAIL`. The
pinned script's own runs never set the marker (`stubs_ran=0` in every suite run).

E7 expectation is really checked. `expect.rc` falsified to 7 for one case → `out=mismatch`,
`ORACLE_FAIL … rc 0 != expect 7`, exit 1 (`receipts/controls/harness-controls.txt`).

E8 guards. `args: []` → `INVALID refused: args ask the resolver to launch a terminal`; missing
`expect` → `no_expect` (not an error); `env.HOME` → `INVALID env must not set
harness-controlled HOME`. Usage errors exit 2.

E9 scale. 128 cases (the 16 demo cases ×8 with distinct ids) → `match=128/128`,
`determinism=ok`, `root-independence=ok`, wall 1.7–2.9 s (measured three times, the spread is
host load) for 128 × (1 run + 1 alt-root) = 256 bwrap runs ≈ 6.7–11 ms/run. The C1 counter's ≥100 fixtures +
≥150 nonces with `--repeat 3` is ~4 runs per case, i.e. the order of 10–20 s on this host.

E10 timeout policy, exercised end to end (`receipts/controls/timeout-policy.txt`): a 1 ms budget
on a normal case yields `rc=124 … TIMEOUT!`, `timed_out=1` in the summary and
`ORACLE_FAIL … resolver did not answer within 0.001s`, `ORACLE_RESULT: FAIL`; the same fixture
with `--allow-timeout` and `expect.rc=124` yields `ORACLE_RESULT: PASS`.

E11 receipts index (all under `.ufo/waves/round-47/w1/ExecOracle/receipts/`): `pin.txt`,
`bin-manifest.tsv`, `sandbox-argv.txt`, `cases.tsv`, `run.json`, `run-stdout.txt`, `trace.txt`,
`trace-execve.json`, `determinism.txt`, `host-reference.json`, `fixtures-demo.json`,
`isolation-probe.txt`, `netns-probe.txt` (+`netprobe.py`), `script-locators.txt`,
`fifo-hang-proof.py` + `fifo-hang-proof.txt`,
`controls/{controls.txt,harness-controls.txt,timeout-policy.txt,tool-exact.sh,tool-echo.sh,tool-tripwire.sh}`.

## 3b. Cross-checks against SentHost-3 (independent seat, same round)

| SentHost-3 point | status here |
|---|---|
| per-case timeout is mandatory (FIFO hang) | already enforced (default 30 s); now first-class: `timed_out` column, hard failure, `--allow-timeout` opt-in, own FIFO proof `receipts/fifo-hang-proof.txt` |
| `--print-cmd` spawns awk, find, ls, md5sum, tr | my bin set is a superset: `tr find awk ls md5sum mkdir rm` (two-sided census in `receipts/trace.txt`); `mkdir`/`rm` come from `save_cache` |
| keep `XDG_CACHE_HOME` explicitly empty per run | enforced: `--clearenv`, harness-set `XDG_CACHE_HOME=<ROOT>/.oracle-rw/cache` recreated per run, fixtures that set it are rejected as invalid |
| `--unshare-all` works unprivileged, needs `/usr/lib` + loader | same bind set (`/usr/lib` ro, `/lib` and `/lib64` → `usr/lib`); measured in `receipts/isolation-probe.txt` |

## 4. Freezing notes, risks and limits

1. **The cache is out of contract and racy by construction.** The resolver forks its saver
   (`:1457`) and bwrap's init kills it when the main process exits, so `ls`/`md5sum`/`mkdir` may or
   may not run (`mkdir` seen in 3/16 sandbox runs, `ls`+`md5sum` in 7/16 host runs). Nothing about
   that reaches stdout or rc — all 16 cases were byte-identical over 3 repeats and both roots,
   stderr digests included. Do not freeze a predicate on the cache file.
2. **The bin set is complete for both branches** (union of the two censuses), and `trace` fails
   loudly if a future fixture makes the script exec anything else. A fixture that needs an extra
   host command (none exists today) would show up as `TRACE_MISSING` rather than silently
   differing.
3. **`find` traversal order is filesystem-dependent.** Selection across data dirs uses find's
   argument order (dir precedence), which is stable; two entries mapping to the same ID *inside one
   directory* would depend on dirent order. The 16-case root-independence check passed on this
   host; a fixture author should not build semantics on intra-directory order.
4. **Host-coupled substrate.** The sandbox uses host `/usr/lib` and host bash as `/bin/sh`
   (this host has no dash). Bash or glibc drift changes resolver behaviour only as it would on the
   host too; the pin sha256, the per-external sha256 in `bin-manifest.tsv` and the fixtures sha256
   make drift visible.
5. **bwrap needs unprivileged user namespaces.** If they are unavailable the harness fails loudly
   (non-zero, stderr retained) — it never falls back to an unsandboxed run.
6. **`--tool` runtime is python3 + env at `/usr/bin/...`** (not on PATH, so the resolver's own
   `command -v` probing is unaffected). A tool that needs another absolute path would have to
   bring it; `mado-terminal.py` is stdlib-only, so this covers it.
7. **The harness refuses non-print cases by design.** A fixture intended to launch a terminal is
   reported `INVALID`, never executed.
8. **A resolver hang is an observation, not a pass.** A FIFO entry (see §2) costs one full
   `--timeout` per repeat and per root, so a hang-heavy fixture set multiplies the wall clock; the
   verdict is FAIL unless `--allow-timeout` is given and `expect.rc` is 124. Keep hang cases out of
   the C1 comparison set unless the C1 predicate defines what a hang means.
9. **Do not check residue with a global process pattern.** `/oracle/...` is shared by every seat's
   sandbox; the FIFO proof checks the FIFO reader (ENXIO on a non-blocking write-open) and the
   case-root path in argv instead, because a bare `pgrep -f /oracle/xdg-terminal-exec` also matches
   other seats' live sandboxes.
8. `expect` values are never computed by `oracle.py`; the demo generator runs the real script on
   the host (print modes only, cache in scratch) and normalizes the root. Fixture authors should do
   the same for the C1 set.

Intended use for C1 (not run here — that tool is another seat's deliverable):

```
oracle.py run --fixtures <C1 fixtures>.json --work <scratch>/oracle-work \
              --receipts <scratch>/oracle-receipts --tool tools/mado-terminal.py --repeat 3
```

`tool` verdicts are per case (`match`/`differ`), stdout is kept verbatim for `differ` rows, and
the exit status separates "the oracle itself is broken" (expect mismatch, non-determinism, stub
ran) from "the tool disagrees with the judge".
