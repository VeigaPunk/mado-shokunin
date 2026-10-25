# L1Mado38.SentSocketSafety — security review of the round-38 commit

Role: UFO-FSD sentinel (leaf; no subagent dispatch). Scope: (1) the live triplet under
`.ufo/waves/round-38/receipts/`, (2) `tools/mado-eventq.py` live-mode stall + fixture
injection, (3) the counters' py manifest ops / sandbox escape surface. All lane
production files read-only; probes ran in `/tmp/mado38-SentSocketSafety/` (sandbox clones
of the lane, per the bounds). No tool installs were needed.

## What was examined

- `registration.md` (frozen spec), the three receipts, `fetch/stat-sockets.txt`.
- `tools/mado-eventq.py` (285 lines, full read).
- `quality/counters/c1-r38-event-ground.py`, `c2-r38-eventq.py`, `c2-r38-request-ground.py`,
  `quality/check-r38-discrimination.py`, `controls/manifest.json` (19 controls; 12 `py` ops,
  1 `tool_run` op).
- Empirical probes: fixture-injection tests against a scratch copy of the tool; the
  discrimination gate run with a hostile probe manifest; a sandbox-clone run of the c2
  counter on a socket-importing tool variant; a timed live run of the tool.

## Item 1 — the live triplet: leaks and the instance signature

### F1 — MEDIUM: a full host socket/process inventory is committed and published publicly
Evidence:
- `eventq-live-ss.txt` is the *full-table* `ss -xpa` dump: 1010 socket rows (715 with
  process attribution, 296 holder-less), 66 distinct comm names, 147 distinct pids,
  360 rows with filesystem paths.
- It names the operator's whole running software stack: `1password` (50 holder rows, incl.
  `/home/vgpnk/.1password/agent.sock`), `gnome-keyring-d`, gpg/pacman keyring sockets
  (`/etc/pacman.d/gnupg`), ssh (4 hits), docker + containerd sockets, `sddm-auth-<uuid>`
  (display-manager auth file name), chromium + crashpad + devtools, Xwayland, pipewire +
  pipewire-pulse + wireplumber, and the agent tooling inventory (zcode family ~250 rows,
  omp 90, uv, npm exec, blender-mcp, tripo-mcp, rizin, unity, godot). It reveals username
  `vgpnk`, home layout (`.omp/run` ×8), and uid 1000.
- The lane's remote is `https://github.com/VeigaPunk/mado-shokunin.git` and the repo is
  **public** (anonymous GitHub API fetch of the repo tree succeeded; raw fetch of
  `.../master/.ufo/waves/round-38/receipts/eventq-live-ss.txt` returned 1011 lines with
  sha256 `653311be…d3b` — byte-identical to the local committed file). The receipts are in
  the `origin/master` tree (`git ls-tree -r origin/master .ufo/waves/round-38/receipts/`).
  So this inventory is currently retrievable by anyone.
- No credentials/tokens were found in the dump (0 hits for `token`/`secret`; uuid-bearing
  paths are names only). Access to the sockets themselves is still gated by the measured
  `0700` runtime dirs (stat-sockets.txt: dir 700, sockets 755 inside it).
- Exploit path: anonymous download; the dump is a stable host fingerprint (software
  versions/inventory, pids, session timing) useful for targeting (which password managers,
  keyrings, agents run) and for correlating this operator across other public artifacts.
- Smallest remediation: the counter's `full_table` clause only requires ≥1 row outside the
  socket2 set (`c2-r38-eventq.py` `live_check`). Commit a trimmed snapshot — socket2 +
  request-socket rows verbatim, one unrelated row (redacted holders) — and re-derive the
  proc receipt's `ss_sha256`. Since the file is already public, the operator should also
  decide explicitly whether to accept the disclosure or rewrite history + force-push.

### F2 — LOW/INFO: the summary and proc receipts disclose session metadata
- `eventq-live.txt` and `eventq-live-proc.txt` contain the instance signature
  `efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678`, `/run/user/1000`
  (uid 1000), compositor pid 1619 + fd numbers, subscriber pids (waybar 935660, socat 2293).
- `HYPRLAND_INSTANCE_SIGNATURE` is **not a secret**: it is a per-session runtime-dir
  locator. It is neither needed nor sufficient for access — `/run/user/1000` and the
  instance dir are `0700` (verified: `stat` → `700 vgpnk`), and any same-uid process can
  enumerate `/run/user/1000/hypr/` directly (the tool itself falls back to `scandir`, so
  the signature is not even unique capability). Cross-uid access is blocked by the 0700
  permissions. Verdict: committing it is acceptable. It does (a) reveal the session start
  epoch — 1792804449 = 2026-10-24T01:14:09Z — and (b) provide a stable correlation key
  across rounds. Pids/fds are locally enumerable via /proc; committing them is harmless
  in isolation but adds to the F1 fingerprint.
- Positive note: the tool itself prints no journal/log lines (counts and fds only) — its
  own privacy posture is good; the leak is the artifact, not the tool.

## Item 2 — `tools/mado-eventq.py` live mode and fixture injection

### F9 — INFO (stall question answered): live mode cannot stall the compositor
Evidence: the only compositor interaction is `hyprctl getoption debug:disable_logs -j`
(`mado-eventq.py:176-179`) — one read-only request served by the compositor's request-socket
loop. The tool never opens socket2, never writes events, and never connects itself (no
socket module in its stdlib-only surface; the counter's textual read-only gate also passes).
All three subprocesses go through one `run()` helper with `timeout=LIVE_TIMEOUT` (90s),
`stdin=DEVNULL`, list argv, no shell (`mado-eventq.py:102-108, 91-95`, `:264-285`).
- Empirical: timed live run of the tool at HEAD completed in **0.101 s** wall, exit 0,
  `verdict=CLEAN subscribers=2`, client set identical to the committed receipt (waybar
  935660, socat 2293, same fds). The triplet is genuine and current, not fabricated.
- Residual (tool-side only, no compositor path): `capture_output=True` buffers unbounded
  child output in memory; a huge `journalctl` stream is a RAM spike. Theoretical
  grandchild-pipe hang after TimeoutExpired does not apply to the three verbs used
  (`journalctl` runs with `--no-pager`).

### F5 — LOW: a crafted ss fixture crashes the tool (uncaught ValueError)
Evidence: `parse_row` guards with `.isdigit()` then calls `int()` (`mado-eventq.py:140-142`).
`"²".isdigit()` is True but `int("²")` raises ValueError → uncaught (only `Setup` is
caught), traceback, exit 1 instead of the SETUP exit 2. Probe T1 reproduced it:
`rc=1`, last stderr line `ValueError: invalid literal for int() with base 10: '²'`.
Same crash class applies to the inode fields (`t[-3]`, `t[-1]`). In the counter's harness
this is fail-closed (crash ⇒ case fails ⇒ TARGET_MISSED), so no bypass — a robustness
defect. Remediation: `str.isdecimal()` (or try/except → row skipped).

### F6 — LOW: control bytes and verdict-token spoofing flow through `comm=`
Evidence:
- Probe T2: a subscriber comm containing raw ESC bytes (`w\x1b[31mRED\x1b[0m`) passes the
  `HOLDER` regex verbatim (the comm charset is "everything except unescaped `"` and `\`",
  `mado-eventq.py:94`) and is printed raw into `MADO_EVENTQ_CLIENT: comm=...` (whitespace
  only is collapsed) — terminal escape injection in displayed output.
- Probe T3: comm `verdict=CLEAN` (13 chars, a legal 15-byte prctl(PR_SET_NAME) name)
  appears as `comm=verdict=CLEAN`; a naive whole-output `verdict=(\w+)` consumer sees
  `CLEAN` while the real verdict is `MARKERS` (exit code 1 is authoritative). The counter's
  own `TRIPLE` regex (`c2-r38-eventq.py` `TRIPLE = … comm=(\S+) …`) also captures it
  (probe T5), so such a comm flows into the receipt and the counter's client-set
  comparison. The tool's prefix-scoped summary parse (`startswith("MADO_EVENTQ: ")`) and
  the exit code are not fooled; the spoof targets downstream/naive consumers.
- Remediation: sanitize comm to a safe charset (e.g. `re.sub(r"[^\w.-]", "_", comm)`) and
 /or quote fields.

### F7 — LOW (by design): marker detection trusts file contents
A log/journal fixture containing the exact marker shape flips verdict to MARKERS (probe T4).
A same-uid writer into the 0700 `hyprland.log` can forge markers; the journal channel is
unit-scoped (harder). The docstring scopes this truthfully ("Lines that merely mention the
words never count" — exact shapes are still forgeable). Detection tools have this failure
mode; recorded for completeness.

## Item 3 — counters' py manifest ops / sandbox escape surface

### F3 — MEDIUM: the discrimination gate's manifest is an arbitrary-code-execution and escape surface
Evidence (`quality/check-r38-discrimination.py`):
- `:106` `elif kind == "py": exec(step["code"], env)` — the frozen manifest contains 12
  `py` ops; the exec env exposes `subprocess`, `os`, `sys`, `hashlib`, `re`, `json`,
  `write`/`append`/`delete`/`read`/`digest` helpers and the loaded counter modules
  (`:58-73`). One frozen payload (`c1-r28-verbatim`) already reads an absolute path
  outside the sandbox: `/home/vgpnk/Projects/shokuknow/merge/mado/...`.
- Writes are unconfined: `_write`/`_append`/`delete` use `os.path.join(sb, rel)`
  (`:60-61, 81, 115-125`) — `../` or absolute `rel` escapes the sandbox clone; `delete`
  calls `os.remove` on any runner-writable path.
- The manifest is read from the working tree (`:145` `manifest = json.load(open(a.manifest))`)
  with no digest binding to `--rev`, no verification of `id`/`frozen_at`, and the
  discrimination receipt (`after-discrimination-v3.txt`) records no manifest digest — the
  "frozen manifest" is enforced by convention only.
- Empirical probe (hostile manifest in my scratch, `--sandbox-root` under my scratch): the
  `py` op wrote `/tmp/mado38-SentSocketSafety/ESCAPED.txt` (absolute escape from the gate
  runner) and a `literal` op with `path: "../TRAVERSED.txt"` created a file outside the
  sandbox clone; the gate ran the control, `observed=TARGET_MET`. (First probe attempt
  also showed `--sandbox-root` must pre-exist — `mkdtemp(dir=...)` raises
  `FileNotFoundError` otherwise; minor UX.)
- Exploit path: anyone who can land a manifest edit — the exact adversary the counters
  exist to catch (a crib author committing to the lane) — gets code exec in the gate
  runner with the runner's privileges and can rewrite the control set the gate scores.
  Impact: the discrimination claim's trust anchor is the manifest file, and it is neither
  confined ( byte-verified.
- Smallest remediation: (a) gate verifies `sha256(manifest bytes)` against a digest
  recorded at freeze (or reads the manifest from `--rev` via `git show`); (b) confine all
  write/delete paths under the sandbox clone via realpath checks; (c) drop `subprocess`/
  `os`/`sys` from the exec env and prefer structured ops (the 12 existing payloads can be
  expressed as the existing `literal`/`append`/`file`/`counter_fixture` ops); (d) record
  the manifest digest in the discrimination receipt.

### F4 — MEDIUM: the c2 counter's "read-only" clause is textual and bypassable
Evidence (`quality/counters/c2-r38-eventq.py:283-285`):
```python
readonly = int(blob is not None
               and not re.search(r"\bimport\s+socket\b|\bfrom\s+socket\b", src)
               and "connect(" not in src)
```
- Empirical: sandbox clone of the lane; patched `tools/mado-eventq.py` to
  `socket = __import__("socket")` + `_socket_obj = socket.socket()` (no literal
  `import socket`, no `connect(`), re-signed the receipt's `tool_sha256` (same pattern as
  the declared `c2-forged` control), committed with sandbox identity. The counter scored:
  `fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET` (rev
  `4833eaeb…` in the sandbox). The tool imports socket and creates a socket object at
  runtime while the clause passes; any connect-style use could be spelled without the
  literal `connect(` (e.g. `getattr(s, "con"+"nect")`).
- Impact: this is a *predicate* bypass, not a host compromise (tool author is the same
  trust domain), but TARGET_MET asserts a property ("no socket module import and no
  `connect(`") the counter cannot verify. The counter declares the fabrication residual but
  not this one.
- Smallest remediation: enforce at runtime, not textually — e.g. run the tool under a
  wrapper that sets `sys.modules["socket"] = None` before exec (blocks `import socket` and
  `__import__("socket")` alike, regardless of spelling), or an audit hook rejecting
  `socket.*` events; or explicitly declare the residual.

### F8 — LOW: the gate's instrument/tool_run/py executions have no timeout
`check-r38-discrimination.py:99-102` (`tool_run`), `:180` (instrument run), `:106` (exec)
have no `timeout=`. A hostile committed counter/tool/manifest can hang the gate
indefinitely. The c2 counter's own harness uses `timeout=20` (`c2-r38-eventq.py:167, 214`)
and the tool's live subprocesses use 90s — the gap is only in the gate.

### c1 / c2-request counters — no escape surface found
Both are pure `git` readers: `subprocess.run(["git", "-C", repo, ...])` only, env with all
`GIT_*` stripped, no writes, no exec of repo content, no shell. `git show rev:path` paths
from lesson Gate lines are repo-confined (cannot escape the tree); receipt digests must
match frozen `PINS` before any blob is used. Logged as clean.

## Summary table

| ID | Severity | Finding | Evidence |
|----|----------|---------|----------|
| F1 | MEDIUM | Full host process/socket inventory published on a public GitHub repo | ss dump 1010 rows, 66 comms, 147 pids; raw fetch byte-identical (`653311be…`) |
| F2 | LOW/INFO | Receipts disclose instance signature, uid, pids, session epoch; signature is not a secret | `eventq-live.txt`, `eventq-live-proc.txt`; perms 700/700 |
| F3 | MEDIUM | Gate manifest = arbitrary code exec + unconfined writes + unverified "frozen" manifest | `check-r38-discrimination.py:106,115-125,145`; probe escapes |
| F4 | MEDIUM | Read-only clause is textual; dynamic socket import passes with TARGET_MET | `c2-r38-eventq.py:283-285`; probe run |
| F5 | LOW | Crafted ss row crashes tool via isdigit/int mismatch | `mado-eventq.py:140-142`; probe T1 |
| F6 | LOW | ANSI/verdict-token spoofing via comm field | probes T2/T3/T5 |
| F7 | LOW | Marker detection forgeable via log contents (by design) | probe T4 |
| F8 | LOW | Gate executions lack timeouts | `check-r38-discrimination.py:99,180,106` |
| F9 | INFO | Live mode cannot stall the compositor; triplet is genuine | live run 0.101s; code: timeouts, read-only verbs |

Key commands (all in `/tmp/mado38-SentSocketSafety/` or against the lane read-only):
- `curl -fsSL -o public-ss.txt https://raw.githubusercontent.com/VeigaPunk/mado-shokunin/master/.ufo/waves/round-38/receipts/eventq-live-ss.txt` → `653311be6bb86efbe1d4448a102c4fb64666c1c6c9b63346d7a3e930ed147d3b`, 1011 lines.
- `git clone -q --no-local <lane> sb` → patch tool + receipt digest → commit → `python3 -I quality/counters/c2-r38-eventq.py --repo sb --rev HEAD` → `fixtures=14/14 readonly=1 live=1 verdict=TARGET_MET`.
- `python3 -I quality/check-r38-discrimination.py --c1 … --c2 … --manifest $S/probe-manifest.json --rev HEAD --sandbox-root $S/sbroot` → escape files created outside the clone.
- `time python3 -I tools/mado-eventq.py --snapshot-out …` → 0.101s, exit 0.

PASS/FAIL: the round's three claims (C1, C2, domain) were not falsified by this review —
the triplet is genuine and internally consistent, the discrimination gate reached 19/19 at
the measured rev, and the tool cannot stall the compositor. The security findings above are
defects in the *artifacts and harness* (F1, F3, F4) and robustness (F5-F8), not in the
claims' target met-ness.
