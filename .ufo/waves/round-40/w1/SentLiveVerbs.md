STATUS: complete. 9 findings on the `--live` verb surface: 1 critical, 1 high, 3 medium,
3 low, 1 info. Every finding below is either exercised (command + output) or a source
citation at the pinned commit. No compositor verb was run except the allowed read verbs;
the `[[BATCH]]` path was proven **without** sending it (see S1 evidence).

Seat: SentLiveVerbs. Target: security review of `--live` / `--hyprctl` / `--probe` in the
reference tool (`c1/ctl-ref-tool.py.txt`, a CONTROL, never delivered) against the stub
contract in `quality/counters/c1-r40-live.py` (`PRED-C1-r40-v1`). Findings are stated as
requirements on the *delivered* `tools/mado-options.py`.

## What the tool can execute (the answer to "path from `--hyprctl`")

1. `argv[0]` of the child = the `--hyprctl` value verbatim, default `"hyprctl"`
   (`ctl-ref-tool.py.txt:695`), resolved through `PATH` by `subprocess.run` and never
   validated (no absolute-path, regular-file, or executable-bit check anywhere).
2. `--selftest` runs `sys.executable -I <itself>` in a private temp dir (`:746-750`) — bounded, self.
3. **Indirectly, arbitrary host commands**: the key argument is unvalidated and hyprctl
   dispatches on substring containment of its joined argv, so a config-declared key can
   turn one `getoption -j` call into a `[[BATCH]]` request that the compositor executes
   with `dispatch exec` (S1, critical).

Nothing else: no shell, no other program, no network (`STDLIB_DENY` at
`c1-r40-live.py:89` keeps socket/urllib/http out, clause g).

## Risk table

| # | Surface | Sev | Attacks | Evidence | Exact mitigation for the delivered tool |
|---|---|---|---|---|---|
| S1 | config-declared key → `hyprctl` argv → `[[BATCH]]` → `dispatch exec` | **CRITICAL** | the "read-only, no mutation" claim and the operator's shell | see below | key validator (M1) applied to *every* key before it becomes argv |
| S2 | `--hyprctl` / default `hyprctl` resolved via `PATH`, unvalidated | HIGH | code execution as the operator from a poisoned `PATH` | exercised, see S2 | resolve + type/mode check (M2) |
| S3 | child inherits the whole environment, cwd, and stdin | MEDIUM | `LD_PRELOAD` into the child; evidence taken from the wrong compositor instance | exercised, 269 vars incl. `LD_PRELOAD` | explicit env allowlist + `stdin=DEVNULL` (M3) |
| S4 | unbounded reply buffering | MEDIUM | memory exhaustion from a hijacked program/compositor | exercised: 32 MiB reply → 118 MiB RSS | reply cap (M4) |
| S5 | reply schema not type-checked (`bool(rec["set"])`) | MEDIUM | a hostile reply flips `mismatch` → `agreement` | code `:623-641` + capture types | strict reply typing (M5) |
| S6 | control chars in a key reach stderr/stdout verbatim; NUL crashes | LOW-MED | terminal escape injection; un-named traceback instead of exit 5 | exercised (ESC, NUL) | M1 + escaped diagnostics + catch `ValueError` (M6) |
| S7 | per-key 10 s timeout only, no total budget; grandchildren survive | LOW | 11.7 min worst case; orphaned process after a hijack | exercised: timeout fires, grandchild alive | total budget + process-group kill (M7) |
| S8 | read-path fan-out feeding the live pass (`source =` absolute/glob, no size cap, unbounded key count) | LOW | config-driven amplification of subprocess spawns; whole-file reads | code `:363-365`, `:437`, host-tree grep | caps (M8) |
| S9 | `--getoption FILE` + `--live` both accepted | INFO | a "live" label that came from a file | code `:718-722` | refuse the combination (M9) |

## S1 — CRITICAL: a hostile config key executes an arbitrary command through the compositor

**Exploit path.** A config file that the operator does not fully control (the tool accepts
`source =` with absolute paths and globs, `ctl-ref-tool.py.txt:353-370`) declares one line:

```
x/--batch;dispatch exec touch /tmp/pwn = 1
```

That lhs is not a handler keyword and has no `:`, so `is_directive` keeps it and it becomes
a declared key (`:433-436`). `native_query` then runs exactly
`[hyprctl, "getoption", "-j", key]` (`:623-626`).

hyprctl at the pinned commit parses argv as follows:
- the flag loop only intercepts args that start with `-` (`hyprctl/src/main.cpp:411`); this
  key does not, so it is appended verbatim to `fullRequest` (`main.cpp:470`);
- `fullRequest = "j/" + "getoption x/--batch;dispatch exec touch /tmp/pwn"`;
- dispatch is **substring containment**, not equality: `if (fullRequest.contains("/--batch")) batchRequest(fullRequest, json)` (`main.cpp:524-525`);
- `batchRequest` drops everything up to the first space, rewrites `;` → `;j/`, prefixes
  `j/`, and sends `"[[BATCH]]" + commands` (`main.cpp:339-348`), i.e.
  `[[BATCH]]j/x/--batch;j/dispatch exec touch /tmp/pwn`;
- the compositor's `dispatchBatch` splits on `;` (`src/debug/HyprCtl.cpp:1309-1332`) and
  calls `getReply` per chunk; an unknown first chunk returns the string `"unknown request"`
  (`HyprCtl.cpp:2113-2130`) and **does not abort the loop**, so the second chunk runs;
- `dispatchRequest` (`HyprCtl.cpp:1126-1158`) looks up the `exec` dispatcher and runs the
  argument as a shell command;
- there is no IPC authorisation: the accepted connection's request goes straight to
  `getReply` (`HyprCtl.cpp:2265-2290`), gated only by socket file permissions.

**Evidence, tool side (exercised).** A temp `--home` with that exact line and a logging stub:

```
tool rc=0
["getoption", "-j", "general:gaps_in"]
["getoption", "-j", "x/--batch;dispatch exec touch /tmp/pwn"]
```

**Evidence, hyprctl side (exercised, socket-free).** Two probes that never reach the socket
because the rerouted handler fails before `connect` (`main.cpp:216-231`), plus a control:

```
=== P1: key x/--help      -> usage: hyprctl [flags] <command> [args...|--help]
=== P2: key a/setprop     -> Not enough arguments in 'j/getoption a/setprop', expected at least 3   rc=255
=== P3 control: a_setprop -> Couldn't connect to /tmp/hv-nonexistent/hypr/deadbeef/.socket.sock. (4) rc=4
```

P2 prints the exact request string hyprctl would have written, and shows the `/setprop`
handler was selected for a key with no `-` and no space — the reroute mechanism. I did not
send `--batch` to the live compositor (harm watch: never `--batch`); the last step is the
cited source, not an executed request.

**Impact.** Running the lane's census (`--live`) on a tree containing a sourced file with
such a line executes an arbitrary command as the operator, from a tool whose claim is
"standard library only; no write" and whose harm watch says `getoption -j` is the only
compositor verb. It also silently violates "no compositor mutation".

**Mitigation M1 (mandatory).** Validate every key — declared *and* probe — before it can
become argv:

```python
KEY_RE = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")
```
- a probe key that fails → exit 2, message contains `probe` and the key (`PRED`'s hostile
  fixture needs rc 2 + `"probe" in stderr` for `-x`, `--version`, `""`; all three fail M1);
- a declared key that fails → exit 2 naming the key and its `owner:line`, and run **no**
  program (fail closed; never silently drop the row — the tool's own "no silent skip" policy);
- apply the check in `merge_live` *and* in `run_static`/`declare` so no path reaches argv unchecked.

Compatibility checked: all 70 host keys are inside the allowlist
(`[A-Za-z0-9_.:-]`, longest 40 chars, alphabet `{. : _}` + alnum — verified against
`.ufo/waves/round-40/c1/native-capture.jsonl`), and the counter's fixture keys are
`opt<tag><n>:<kind><n>` (`c1-r40-live.py:257`), also inside it. `--probe zzprobe:one`
passes. M1 is strictly a superset of the claim's `-`-prefix rule, so no fixture changes
verdict.

## S2 — HIGH: `--hyprctl` is executed unvalidated, default resolved through `PATH`

`subprocess.run([hyprctl, ...])` uses `execvp` semantics; `--hyprctl` accepts any string
including a relative path (`ctl-ref-tool.py.txt:695`, `:623-626`). Exercised: with a stub
`hyprctl` first on `PATH` and no `--hyprctl`, the tool ran the stub (`hits=1`). Anyone who
can write a `PATH` entry (a venv/bin dir, `.` on `PATH`, a shared temp dir) gets code
execution in the census run, and the census then reads *that* program's output as
"the compositor's native reply".

**Mitigation M2.** Resolve once, before the loop:
- if the value contains `/`: require `os.path.isabs` (refuse `./x`, `../x`, `x/y`) → else exit 2;
- if it contains no `/`: search `PATH` yourself, skipping empty entries and `.`/`..`, and
  take the first `S_ISREG` + `X_OK` candidate; none → exit 5 naming the value (this is the
  missing-program fixture: `--hyprctl <tmp>/no-such-dir/hyprctl` must stay rc 5 with
  `hyprctl` in stderr, `c1-r40-live.py:565-567`);
- require `stat.S_ISREG` and `os.access(path, os.X_OK)` and refuse `mode & 0o022`
  (group/other writable) → exit 2 naming the path;
- use the resolved absolute path as `argv[0]` for every call, and write
  `hyprctl: resolved <abs path>` to **stderr** (never into the row array, which is the
  counter's contract).

Counter-compatible: the harness creates the stub with `os.chmod(path, 0o755)` inside a
`mktemp -d` directory (`c1-r40-live.py:431-444`), so 0755/0700 passes the mode check, and
the stub path is already absolute.

## S3 — MEDIUM: full environment, cwd and stdin are inherited

Exercised: the child's own dump —

```
{"LD_PRELOAD": "/tmp/not-a-lib.so", "MADO_CANARY": "yes", "SIG": "deadbeef",
 "XDG": "/tmp/x", "cwd": "/home/vgpnk/Projects/shokunin", "nvars": 269}
```

Three distinct harms: (a) `LD_PRELOAD`/`LD_LIBRARY_PATH`/`PYTHON*` from the parent apply to
the child, so "the child is hyprctl" is not a security boundary; (b) the compositor that
answers is whatever `HYPRLAND_INSTANCE_SIGNATURE` + `XDG_RUNTIME_DIR` say, so a live
receipt can be produced against a different instance than the operator believes (evidence
integrity — the claim's `70/70` host receipt has this hole); (c) stdin is inherited, so a
future `--batch`-style code path in hyprctl would read the operator's TTY or a hostile pipe.

**Mitigation M3.** Pass an explicit allowlist env:
`{"PATH": <resolved PATH>, "HYPRLAND_INSTANCE_SIGNATURE": <os.environ value>, "XDG_RUNTIME_DIR": <os.environ value>}`
(only names present in the parent; nothing else), plus `stdin=subprocess.DEVNULL`,
`close_fds=True`, `cwd` left unset. Print `live: instance <signature>` to stderr so the
receipt can state which instance answered. Counter-compatible: the stub's shebang is the
absolute `sys.executable` (`c1-r40-live.py:406`) and it reads only its own directory, so it
needs no environment.

## S4 — MEDIUM: unbounded reply buffering

`capture_output=True` (`:625-626`) buffers stdout/stderr with no cap, and the value is then
`str()`d into the row. Exercised with a stub replying 32 MiB:

```
rc=0  stdout_bytes=33554578  child_peak_rss_kb=117912
```

≈3.6× amplification per reply, no limit, and the blob is echoed into the row array (hence
into any receipt).

**Mitigation M4.** After the call, `if len(p.stdout) > 65536 or len(p.stderr) > 65536: raise
CtlError("%s: reply too large" % key)` (exit 5, key named), and truncate the rendered live
value to 4096 chars in the row. A truly bounded read needs `Popen` + a manual read loop;
with M2 the program is at least pinned to a non-writable file, so the post-hoc cap is the
proportionate control. Residual: a pinned program that floods faster than 10 s can still
grow to the cap.

## S5 — MEDIUM: reply schema is not type-checked

`native_query` accepts `bool(rec["set"])` and any JSON type for the value
(`:636-641`); `"set": "false"` is truthy, `{"int": "1"}` is accepted, duplicate keys take
the last. A hostile reply (S2/S3) can therefore turn `mismatch` into `agreement` without
touching the model.

**Mitigation M5.** Require exactly one form key, `isinstance(rec.get("set"), bool)`, and a
type matching the form — `int`→`int` (not `bool`), `float`→`int|float`, `str`/`custom`→`str`
— else exit 5 naming the key. Verified compatible with the real capture: `int`→int 44,
`float`→float 5, `str`→str 8, `custom`→str 13, `set`→bool 70/70.

## S6 — LOW-MEDIUM: control characters in a key; NUL crashes

Exercised on the reference tool:

```
=== ESC in key, child fails:  mado-options.py: a^[[31mRED: /tmp/.../hyprctl exited 1   (rc=5)
=== NUL in key:               ValueError: embedded null byte ... rc=1   (traceback)
```

The ESC byte is written raw into the exit-5 diagnostic (terminal escape injection from a
sourced file; the same bytes reach stdout JSON and any markdown receipt that renders the
key). The NUL byte escapes the `except (OSError, SubprocessError)` guard (`:627-628`) —
`subprocess` raises `ValueError` — so a malformed config produces an un-named traceback
instead of exit 5, contradicting the claim's "failures are named".

**Mitigation M6.** M1 removes both inputs. Additionally: render every key in diagnostics
through a printable escaper (`key.encode("unicode_escape").decode("ascii")`), and add
`ValueError` to the caught set (mapped to `CtlError` → exit 5), which also covers
`E2BIG`-style argv rejection. (A 200 KB key already yields the correct named exit 5 with
the key on stderr, because `OSError` is caught.)

## S7 — LOW: no total budget; grandchildren survive the timeout

Exercised: the 10 s per-key timeout fires correctly and names the key
(`mado-options.py: k: cannot run ...: timed out after 10 seconds`, rc=5), but a
`start_new_session=True` grandchild spawned by the child was **still alive** after the tool
exited (`alive=YES`, pid killed by me afterwards). With 70+ keys the worst case is
~11.7 min, and a hijacked program can leave a process behind.

**Mitigation M7.** Add `--live-timeout SEC` (default 120) as a wall-clock budget for the
whole live pass → exit 5 naming the key that exhausted it; spawn with
`start_new_session=True` and on `TimeoutExpired` `os.killpg(os.getpgid(pid), SIGKILL)`.
Residual: a double-forked daemon cannot be contained without cgroups.

## S8 — LOW: read-path fan-out feeding the live pass

`source =` accepts absolute paths and globs (`:353-370`), `read_bytes` reads whole files with
no size cap (`:226-240`), and the number of declared keys — hence of subprocess spawns — is
unbounded by anything but the config's size. Recursion is guarded (`:363-365`), so no cycle
blow-up. The host tree uses only `~`-relative sources (grep of `~/.config/hypr/hyprland.conf`
and `~/.local/share/omarchy/default/hypr/**`: every `source =` starts with `~`), and this
tool maps `~` to DIR, so a DIR restriction costs nothing on the host.

**Mitigation M8.** Cap total parsed bytes (4 MiB) and file count (1024) → exit 3 naming the
file; refuse an absolute `source =` target outside DIR unless `--allow-outside-source` →
exit 3 naming it; cap live queries at 512 keys → exit 5 naming the cap (the host has 70).

## S9 — INFO: `--getoption FILE` and `--live` together

`merge_live` runs after `merge_rows` and overwrites the labels (`:718-722`), so a row can
carry a live label from a file or vice versa. No security impact; refuse the combination
with exit 2 so a `live` label can only come from the compositor (M9).

## Mitigation set, in one place (what the delivered tool should carry)

**Must carry (security-blocking): M1, M2, M3.** Recommended: M4–M9.

M1 key allowlist `[A-Za-z0-9_.:-]{1,128}` on every key before argv (exit 2, no program run)
· M2 `--hyprctl` resolution to an absolute, regular, executable, not group/other-writable
file (exit 2), exit 5 when unresolvable, resolved path on stderr · M3 env allowlist
`{PATH, HYPRLAND_INSTANCE_SIGNATURE, XDG_RUNTIME_DIR}` + `stdin=DEVNULL` + `close_fds` +
instance signature on stderr · M4 64 KiB reply cap (exit 5) + 4096-char value cap ·
M5 strict reply typing (exit 5) · M6 escaped diagnostics + catch `ValueError` (exit 5) ·
M7 `--live-timeout` total budget + process-group kill · M8 read caps and DIR-scoped
`source =` · M9 refuse `--getoption` with `--live`.

All of M1–M9 keep `PRED-C1-r40-v1` satisfiable: none adds or reorders argv
(`["getoption","-j",KEY]` stays exact, `c1-r40-live.py:413`), none touches the four reply
forms or the `no such option` text, none writes under the config root, and the exit codes
used (2/3/5) are already in the tool's map. M1/M5/M6 must be reflected in the `--selftest`
count (clause b needs `k == n >= 79`).

## Not tested / residual (declared, not passed)

- I did not send `[[BATCH]]` to the live compositor (harm watch). S1's last hop is source
  (`HyprCtl.cpp:1309-1332`, `:2113-2130`, `:1126-1158`), not an executed request; the
  reroute *mechanism* and the tool-side argv are executed evidence.
- I did not bind a socket or impersonate the compositor; the hyprctl probes used a
  nonexistent `XDG_RUNTIME_DIR` so nothing was contacted.
- `--live` against the real compositor was not run by this seat (other seats hold that
  receipt); nothing here depends on it.
- Residual: a *legitimate* absolute `--hyprctl` under a directory the attacker can replace
  between resolution and exec (TOCTOU) is not covered by M2 without `O_PATH`+`fexecve`,
  which stdlib cannot express; acceptable given the operator supplies the path.

## Tooling

Nothing installed, nothing upgraded. Research sources fetched read-only into `/tmp` and
removed: Hyprland tarball at `efb50993780079460b0cbed1363e2166a2de1d9f` (codeload), used for
`hyprctl/src/main.cpp` and `src/debug/HyprCtl.cpp` citations. All scratch fixtures were
`mktemp -d` under `/tmp`, never in a config tree, and were removed.
