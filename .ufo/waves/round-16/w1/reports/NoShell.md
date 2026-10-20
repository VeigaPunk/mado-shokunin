# NoShell — sentinel report (mado round 16, wave w1)

Scope: security review of the C2 action-plan gate's "supplied argv is data,
never executed" property and the isolation requirements of its `--selftest`
subprocess self-invocation. Read-only review; no execution of the gate, its
selftest, `mado-verify.sh`, or any host/live probe. No installs, no package or
service operations (pacman pause honoured; RULES.md read, nothing installed —
none needed).

## Inputs read

- `corpus/lessons/round-15-verifier-spotcheck.md` (R15-V1 actual transaction
  at :254-266; R15-V2 fixture-vs-real-plan at :268-277; fixtures not guards :159-163).
- `.ufo/waves/round-16/w1/spec.json` item `SafetyGate` (gate API contract:
  `--plan PATH --policy PATH`, `--selftest` self-invocation, `--frozen DIR`,
  exit 0/1/2, "must never execute supplied argv or inspect host").
- `tools/mado-verify.sh` prior selftest isolation pattern: `mktemp -d` scratch
  :395, `env PATH="$SANDBOX"` stub-PATH children :994, :1017, nested-marker
  recursion guard `MADO_SELFTEST_NESTED` :1028-1042, cleanup-on-pass /
  keep-on-fail :1533-1541.
- State at review time: `tools/mado-action-plan.py`,
  `.ufo/waves/round-16/safety-policy.json`, `.ufo/waves/round-16/safety-cases.json`
  **did not exist**. Findings below are therefore design requirements against
  the SafetyGate contract, not a code audit of landed bytes. L1 must check the
  landed file against the "Acceptance checks" list at the end.

## Axes

1. Execution: can any argv element (or policy/expected field) reach a process
   spawn, shell, evaluator or PATH lookup?
2. Host inspection: can gate inputs make the gate read host state (devices,
   credentials, live sockets) beyond the two/three named JSON files?
3. Selftest blast radius: if a regression *does* execute argv, what can the
   self-invoked child reach?
4. Verdict integrity: can a crash, parse ambiguity or output injection make the
   receipt lie?

## Findings

### H1 — Selftest fixtures carrying the real R15 transaction become a live package transaction under any execution regression (High)

- Exploit path: SafetyCases is required to include "actual libinput sudo pacman
  transaction" (`sudo pacman -S --needed --noconfirm libinput libinput-tools`,
  spotcheck :256). The host has passwordless `sudo` (operator directive). If the
  gate, now or after a later edit, ever passes argv to `subprocess`, `os.exec*`,
  `os.system`, `shell=True`, or a "probe/which" helper, the selftest itself runs
  that transaction during the host-wide pacman pause. An absolute fixture such
  as `/usr/bin/sudo` or `/usr/bin/pacman` (natural for a "basename of absolute
  path" case) bypasses any PATH sandbox.
- Evidence: contract lists exactly these verbs as denied basenames; prior gate
  only sandboxed PATH (`mado-verify.sh:994`), which does not cover absolute argv.
- Impact: repeat of R15-V1 harm, caused by the safety gate's own test.
- Smallest remediation:
  1. Denied-verb fixtures use relative argv0 (`sudo`, `pacman`) or a
     non-existent prefix (`/nonexistent-mado-canary/bin/pacman`); never a real
     host directory (`/usr/bin`, `/bin`, `/sbin`, `/usr/local/bin`). Selftest
     asserts this statically over its own fixture table before spawning.
  2. Child env is an explicit minimal dict (not `os.environ` copy):
     `PATH=<tmp>/canary-bin`, `HOME=<tmp>/home`, `TMPDIR=<tmp>`, `LC_ALL=C`.
     Absent by construction: `SUDO_*`, `SSH_AUTH_SOCK`, `WAYLAND_DISPLAY`,
     `DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, `XDG_RUNTIME_DIR`,
     `DBUS_SESSION_BUS_ADDRESS`, all `PYTHON*`. Without these, an accidentally
     executed `hyprctl`/`systemctl --user`/`omarchy` cannot locate the
     compositor socket or user bus.
  3. `<tmp>/canary-bin` holds one executable stub per denied basename
     (pacman, yay, paru, systemctl, hyprctl, omarchy, libinput, evtest, sudo,
     sh, bash, env) whose only action is appending its name to
     `<tmp>/executed`; it never calls through. After every case the selftest
     asserts `<tmp>/executed` absent — a direct red control for "argv never
     executed", which an exit-code/finding assertion alone cannot provide.
  4. `stdin=subprocess.DEVNULL` (no tty for a sudo prompt), finite `timeout`,
     `start_new_session=True`, kill the process group on timeout.

### H2 — Input paths can make the gate itself read a raw input device or block forever (High for this lane's no-input-probe rule; Medium generally)

- Exploit path: `--plan /dev/input/eventN` (or a `--frozen` dir whose
  `plan.json` is a symlink to it) makes a naive `open(path).read()` open an
  evdev node and block reading keystrokes if the user is in `input` — the gate
  becomes an input-capture tool, exactly what `input-capture` is blocked for.
  A FIFO or `/dev/zero` hangs or exhausts memory; `/proc/self/environ` or a
  credential file symlinked as `policy.json` gets read and possibly echoed in a
  JSON parse error.
- Impact: violates "never inspect host"; secrets may reach the receipt via
  error text.
- Smallest remediation: for every input file: `os.lstat` reject non-regular /
  symlink → `os.open(path, O_RDONLY|O_NONBLOCK|O_NOFOLLOW|O_CLOEXEC|O_NOCTTY)`
  → `os.fstat` must be `S_ISREG` → bounded read (e.g. ≤1 MiB, reject larger).
  Any failure → exit 2 with stable finding (e.g. `input_not_regular_file`),
  never echoing file bytes. Selftest uses an `os.mkfifo` in `<tmp>` and a
  `<tmp>` symlink as red fixtures (never a real `/dev/input` path — that would
  itself be an input-device probe).

### M1 — Uncaught exception exits 1, indistinguishable from "unsafe plan" (Medium; cross-ref ExitMap/FindingStability ownership)

- Exploit path: deep-nesting JSON (`RecursionError`), non-UTF-8 bytes, NUL in
  argv, or an unexpected type raises; CPython's default traceback exit status
  is **1**, which the contract reserves for "failed stable reason". The receipt
  would record a refusal that was really a crash.
- Remediation: a single top-level `except BaseException` (excluding the
  deliberate `SystemExit`) → exit 2 `could_not_evaluate`. Selftest asserts
  finding text, not exit code alone, so crash-1 cannot pass as a red.

### M2 — `--frozen` must not treat `expected.json` content as paths (Medium)

- Exploit path: if `expected.json` maps *filenames* to digests and the gate
  hashes whatever names it lists, `{"../../../.ssh/id_ed25519": "<guess>"}`
  turns the gate into an arbitrary-file reader and a digest oracle for
  credential files (contract forbids opening credential/auth files).
- Remediation: frozen mode reads exactly `DIR/plan.json`, `DIR/policy.json`,
  `DIR/expected.json` (fixed literals, H2 open rules, no symlinks); expected
  digests are compared against those two fixed files only. Unknown keys or
  extra files → exit 2 `snapshot_tampered`.

### M3 — Interpreter environment injection (Medium)

- Exploit path: `PYTHONPATH=<dir with json.py|subprocess.py|sitecustomize.py>`,
  `PYTHONINSPECT`, user site-packages, or a planted module in the script
  directory replace stdlib behaviour in the gate and its child, silently
  changing verdicts or adding execution.
- Remediation: child argv is `[sys.executable, "-I", os.path.realpath(__file__), ...]`
  (`-I` = ignore `PYTHON*`, no user site; on Python ≥3.11 also `-P`, no
  script-dir prepend). Never resolve `python3` through the (stubbed) PATH.
  L1's verification command should likewise be `python3 -I tools/mado-action-plan.py ...`;
  a `#!/usr/bin/env python3` shebang is acceptable for convenience but is not
  the receipt command (and `env` is itself a denied basename in plans).
  Python version was not queried (no host probes); `-P` applicability is
  `[INFERENCE]` until L1 records the interpreter version in the receipt.

### M4 — Echoing untrusted argv enables terminal-escape injection into the operator's terminal (Medium)

- Exploit path: argv element `"\x1b]52;c;<b64>\x07"` (OSC 52 clipboard write)
  or OSC 8 hyperlinks / cursor rewrites printed raw in a finding line can
  rewrite the visible verdict or plant clipboard content.
- Remediation: every argv/kind fragment in output goes through
  `json.dumps(..., ensure_ascii=True)` (or `repr`), never raw `print`. Selftest
  fixture: argv containing ESC/BEL; assert no `0x1b`/`0x07` byte in child stdout.

### L1 — Lexical-only basename; no host resolution (Low, design rule)

- `shutil.which`, `os.path.realpath`, `os.path.expanduser`, `expandvars`,
  `glob` on argv are host inspection, make verdicts host-dependent (e.g.
  `/usr/bin/sh` → `bash`), and are one step from execution. Basename must be
  `posixpath.basename` on the literal string after type checks. Edge cases
  (trailing `/`, `./pacman`, case, whitespace, homoglyphs, wrapper verbs like
  `doas`, `pkexec`, `run0`, `systemd-run`, `nice`, `xargs`, `python3 -c`,
  `zsh`, `dash`) are ExecBasename/PolicyScope territory; noted only so the
  finite-list limit is not misreported as "argv safely classified".

### L2 — Parse determinism (Low; cross-ref PlanSchema)

- Duplicate keys (`{"kind":"read-source","kind":"package-install"}`) — Python
  keeps the last, other readers the first; reject via `object_pairs_hook` →
  exit 2. Reject `NaN`/`Infinity` via `parse_constant`. Non-`str` argv items,
  empty strings, NUL bytes → malformed, exit 2.

### L3 — Selftest hygiene (Low)

- Scratch via `tempfile.mkdtemp(prefix="mado-action-plan-selftest.")` (0700,
  unpredictable), removed in `finally` on pass, kept and printed on failure
  (mirrors `mado-verify.sh:1533-1541`); never write into the repo or `.ufo/`.
- Recursion guard: child env carries `MADO_ACTION_PLAN_SELFTEST_NESTED=1`;
  `--selftest` with that marker refuses (exit 2) — mirrors `:1028`.
- Policy has no field interpreted as a command (no "probe", "verify_cmd",
  "hook"); policy is classification data only.

## Defence in depth (recommended, not required for C2 credit)

In evaluation mode the gate can install `sys.addaudithook` that raises on
`subprocess.Popen`, `os.system`, `os.exec`, `os.posix_spawn`, `os.spawn`,
`os.fork`, `os.forkpty`, `socket.connect`, `ctypes.dlopen` and maps to exit 2
`could_not_evaluate`. Audit hooks cannot be removed once added, so a future
edit that introduces execution fails closed instead of running argv. The
selftest parent installs no such hook (it must spawn itself). A static AST
self-check (only the selftest function references `subprocess`; no
`shell=True`, `eval`, `exec`, `compile`, `pickle`, `shlex`, `os.system`,
`os.popen`, `pty`) catches regressions but is not proof against obfuscation.

## Addendum — landed `.ufo/waves/round-16/safety-cases.json` (SafetyCases-owned; read only)

Read after the main review (20 cases, schema `mado-action-plan-expected-cases-v1`).
`tools/mado-action-plan.py` and `safety-policy.json` still absent at that read.

- Good for H1: every denied-verb argv0 is relative (`sudo`, `pacman`,
  `systemctl`, `hyprctl`, `libinput`, `evtest`, `bash`, `sh`, `env`); no
  `/usr/bin/...` absolute argv0.
- Still H1-relevant: relative argv0 is only safe if the child PATH is the
  canary dir. With inherited PATH, case `r15_libinput_sudo_pacman_transaction`
  (`sudo pacman -S --needed --noconfirm libinput libinput-tools`) resolves real
  passwordless sudo under any execution regression; `raw_input_evtest`
  (`evtest /dev/input/event3`) and `raw_input_libinput_debug_events`
  (`/dev/input/event5`) would be live input capture.
- New requirement: the canary dir must contain **only** marker stubs, never
  symlinks to real tools (the `mado-verify.sh:990-993` sandbox pattern links
  real `cat`, `ls`, … and must not be copied here). Stub every argv0 used in
  the fixtures, including allowed ones (`cat`, `write`) and `ls`
  (`unknown_action_kind`): an "execute the allowed read to verify it" regression
  is the most plausible one and only a `cat` stub detects it.
- Low: `repo-write` cases use argv0 `write`, which is also the util-linux
  terminal-messaging binary on typical Linux hosts `[INFERENCE: not queried]`.
  Harmless as data, but the vocabulary collides with a real host command;
  documenting repo-write argv as a declarative label avoids future confusion.
- `subject` field invokes `python3 tools/mado-action-plan.py` without `-I`
  (see M3).
- Gaps relative to this report, for SafetyCases/L1 to decide: no non-regular
  or symlinked input case (H2), no ESC/BEL argv output case (M4), no
  non-`str` argv item / NUL / duplicate-key / deep-nesting case (M1, L2), no
  absolute-path basename case (if added, use `/nonexistent-mado-canary/…`).

## Acceptance checks for L1 (on landed bytes; static reading suffices for most)

1. No `subprocess`/`os.*exec*`/`os.system`/`os.popen`/`pty`/`shell=True`/
   `eval`/`exec`/`shutil.which`/`realpath` reachable from `--plan`/`--frozen`
   paths; `subprocess` used only inside selftest with list argv rooted at
   `sys.executable -I`.
2. Selftest child: explicit minimal env, `stdin=DEVNULL`, timeout,
   new session, cwd in mkdtemp.
3. Every denied-verb fixture argv0 is relative or under a non-existent prefix;
   canary-bin + `executed` marker absence asserted.
4. Input opening: regular-file + no-follow + size cap; FIFO/symlink red
   fixtures → exit 2 with stable finding.
5. Catch-all → exit 2; selftest asserts exit **and** finding.
6. Frozen mode reads fixed filenames only.
7. Output escapes control bytes.

## Limits

- Not a code audit: target files absent at review time. A static classifier of
  declared plans does not stop an agent that runs `sudo pacman` without
  submitting a plan; it neither remediates R15-V1 nor proves enforcement
  (HostHarm/SafetyLearning own that wording).
- Basename denial is a finite list; wrappers and interpreters escape it by
  design. "argv never executed" is a property of the gate, not of the host.
- Selftest isolation reduces blast radius of a gate regression; it is not a
  sandbox (no namespaces/seccomp) and is not claimed as one.

## Coordination / tooling

- One message sent to `MadoR16` summarising H1-H2, M1, M3-M4, L1, L3 for
  SafetyGate integration. No other seats contacted; no files besides this
  report written.
- Tools installed/updated: none (contract forbids installs this round; none needed).
