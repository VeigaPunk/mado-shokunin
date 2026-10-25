# Seat RevToolSafety — w1 round-40: ref-tool `--live` read-only-discipline attack

Target: `.ufo/waves/round-40/c1/ctl-ref-tool.py.txt` — `native_query` (:623-645) and
`merge_live` (:646-679), plus `main`'s guard (:708-711). Program path from `--hyprctl`,
keys from the config tree and `--probe`. All exploits ran against stubs in `/tmp/rts`
(created and deleted for this review); real-hyprctl probes used only the allowed
read-only verbs (`hyprctl version`, `hyprctl getoption -j KEY`). Host banner verified:
Hyprland 0.56.2, commit efb50993780079460b0cbed1363e2166a2de1d9f (matches freeze facts).
No lsp device is available in this session (no server answers for a `.txt` control
artifact); findings below are text+runtime evidence, not semantic-proof claims.

## Verdict

No command injection is possible (single list-form `subprocess.run`, no shell, no env=,
timeout=10 enforced on Python 3.14.8), but the ref tool has one real injection-adjacent
defect and two contract breaks:

- **HIGH F1** — config-tree keys bypass the only dash guard and are argument-injected
  into the live program; against real hyprctl 0.56.2 a single config line `-j = 1` or
  `--batch = 1` kills the entire `--live` run with exit 5 misattributed as a compositor
  failure.
- **MED F2** — a `null`/number/bool JSON reply crashes the tool (unhandled TypeError,
  traceback, exit 1) because the membership test precedes the dict check.
- **MED F3** — reply capture is unbounded; memory scales with reply size (300 MB reply
  → ~916 MB RSS) despite the 10 s timeout.

## Findings by severity

### F1 HIGH — probe-only dash guard; config keys reach argv verbatim (confirmed, real hyprctl)

The only input validation on keys guards `--probe` (ctl-ref-tool.py.txt:708-711,
`if not k or k.startswith("-"): exit 2`). Config-tree keys have no guard:
`parse_line` accepts an arbitrary lhs (`lhs = trim(line[:equals])`, declared at :434;
`-j`, `--batch`, `-deco:active` are not in `EXCLUDED`/`FLAG_HANDLERS`, so they become
options), and `merge_live` feeds them straight to exec (`:648 native_query(hyprctl,
row["key"])` → `:625 subprocess.run([hyprctl, "getoption", "-j", key], ...)`).

Real hyprctl 0.56.2 parses flags anywhere in argv (black-box probes, read-only):

| command | reply | exit |
|---|---|---|
| `hyprctl getoption -j -j` | usage text | 1 |
| `hyprctl getoption -j -x` | usage text | 1 |
| `hyprctl getoption -j --batch` | `unknown request` | 0 |
| `hyprctl getoption -j --` | `no such option` | 0 |
| `hyprctl getoption -j ';keyword'` | `no such option` | 0 |

Exploits (single-line fixtures under /tmp/rts/home2, home3):

- fixture `-j = 1` → `python3 -I tool.py --home home2 --live` →
  **exit 5**, `mado-options.py: -j: hyprctl exited 1`
- fixture `--batch = 1` → **exit 5**, `mado-options.py: --batch: malformed reply from hyprctl`
- full 9-key hostile fixture (see exploit matrix) against real hyprctl → **exit 5**
  `mado-options.py: --batch: malformed reply from hyprctl`

Impact: DoS of the tool's primary output plus wrong-layer diagnosis — exit 5 is
contractually "compositor failure naming the key", but here the compositor is healthy
and a config line is the trigger. Consequence ceiling today is derail/abort only
(hyprctl consumed the key as a flag and executed nothing else). No mutation, no shell.
The probe path proves the authors knew leading-dash keys are dangerous (exit 2) — the
config path just never got the same check.

### F2 MED — non-iterable JSON reply crashes instead of named failure (confirmed)

`:638 forms = [f for f in ("int","float","str","custom") if f in rec]` runs before
`:639`'s `isinstance(rec, dict)`. Stub replying `null`:
`TypeError: argument of type 'NoneType' is not iterable` → traceback, **exit 1**
(uncaught). Numeric/bool replies crash the same way. Violates the tool's own
named-failure/exit-map (should be CtlError → exit 5). Lists are safe — `["int","set"]`
hits the isinstance check and yields the named `unknown reply form`, exit 5 (confirmed).

### F3 MED — unbounded reply capture; timeout bounds time, not memory (confirmed)

`:626 capture_output=True` slurps the whole pipe. Stub emitting 300 MB of `x`:
tool child maxRSS **938564 KB (~916 MB)**, then the named `malformed reply`, exit 5.
A hostile `--hyprctl` can OOM the run before the malformed-reply check fires.

### F4 LOW — oversized key: clean exit 5 but stderr log-flood (confirmed)

A 200 000-char config key → `execve` E2BIG → exit 5 named, but the error message
prints the full 200 KB key to stderr.

### F5 LOW — timeout kill is child-only; grandchild orphan survives (confirmed, no hang)

Stub forking a grandchild that holds the pipe write end, parent exiting:
`TimeoutExpired` at ~10.1 s → exit 5, `timed out after 10 seconds` (Python 3.14.8
does kill+wait without draining — no hang). The grandchild itself is not killed and
lives until its own timer ends; its output is discarded. Process-litter note only.

### F6 INFO — default `--hyprctl` is inherited-PATH-resolved; env flows to the child (confirmed)

`env PATH=/tmp/rts/fakebin /usr/bin/python3 -I tool.py --home home2 --live` → the tool
executed `/tmp/rts/fakebin/hyprctl` (stub) and accepted its JSON as live values
(exit 0, `ARGV ["getoption","-j","-j"]` in the stub log). Inherent to by-name exec;
`--hyprctl PATH` exists to pin the program — invocations of the delivered tool should
always pin it. The child also inherits the full environment (`env=` not set), e.g.
`HYPRLAND_INSTANCE_SIGNATURE` selects the real hyprctl's instance socket.

### F7 INFO — no aggregate deadline across keys

70 keys → 70 sequential execs, each ≤10 s; a huge hostile config multiplies runtime
unboundedly. Out of frozen scope (13 fixtures) but worth a bound in the delivered tool.

## Exploit matrix (all against /tmp/rts stubs unless noted)

| route | attempt | result |
|---|---|---|
| shell metachars in config key | `general; evil$(id)`, ``backtick`touch /tmp/rts/PWNED` ``, `> redirect`, `semi;colon` | single argv element each; `PWNED` never created; no injection |
| leading-dash config key | `--batch`, `-deco:active`, `-j` | passed verbatim to argv (guard bypass) → F1; real hyprctl derails (usage exit 1 / `unknown request`) → tool exit 5 |
| probe keys | `-x`, `''`, `--batch`, `-j` | exit 2, named `invalid probe key` — guard holds |
| probe whitespace/newline | `x;keyword`, `'newline\nkey'` | exit 0, single argv element — safe |
| mid-key flag | `middle --flag`, `a\tb` | single argv element — safe |
| `--hyprctl` = directory / non-exec / `''` / missing | dirctl, nonexec (mode 644), `''`, nope | all exit 5 naming the key (OSError caught :627) |
| slow program | stub sleeping 14 s | exit 5 at ~50 ms? — no: stub bug (missing import); with hang-stub variant timeout confirmed at ~10.1 s |
| hang via grandchild pipe-hold | stub forks + exits | no hang on 3.14.8; exit 5 `timed out after 10 seconds`; grandchild orphaned (F5) |
| huge reply | 300 MB output | ~916 MB RSS, then named exit 5 (F3) |
| hostile reply forms | `null` / `["int","set"]` / two-form obj / missing `set` / 6000-digit int / `{"str":"no such option","set":true}` | crash exit 1 (F2) / named exit 5 / named exit 5 / named exit 5 / named exit 5 (int-digit limit inside json.loads) / accepted as a str option value (cosmetic: sentinel only matched as exact stripped whole text) |
| PATH influence | hostile PATH, default `--hyprctl` | fake program executed, reply accepted (F6) |
| huge key | 200 KB key | E2BIG → exit 5 named, stderr flood (F4) |
| end-to-end real hyprctl | 9-key fixture, default PATH | exit 5 `--batch: malformed reply from hyprctl` (F1) |

## Holds (verified positives)

- `native_query` is a single list-form `subprocess.run([hyprctl, "getoption", "-j", key])`
  (:625-626): no `shell=True`, no `env=`, no cwd tricks — config content alone cannot
  execute anything; the verb is always argv[1]=`getoption`.
- Config keys cannot contain real newlines (`parse_file` splits on `\n`; continuation
  lines join without a newline); tabs/space/`;`/backticks pass through as inert argv bytes.
- Probe guard real (exit 2) for empty and `-`-prefixed probes.
- `--hyprctl` failures are all named exit 5 (dir, non-exec, empty, missing).
- Reply validation named-fails (exit 5) on: malformed JSON, non-dict lists, two forms,
  missing `set`, oversized ints.
- `no such option` sentinel is exact-text-only; real hyprctl's unknown-key reply
  (`no such option`, exit 0) maps to `config-only` as designed.
- Read-only discipline holds: the `--live` path writes nothing to disk — only opens are
  config reads `rb` (:235), `--getoption` read `r` (:489), and selftest-only fixture
  writes (:753-756, :768); results go to stdout only.
- timeout=10 is enforced (3.14.8); no fork amplification (one exec per key, sequential).

## Residual risk and verification gaps

- hyprctl flag grammar sampled, not enumerated: `-j`, `-x`, `--batch`, `--`, `;keyword`
  exercised; `-q`/`-i`/`--instance`/`--help` not (each further probe is a live
  compositor call). Flags are proven to be parsed anywhere in argv; other short flags
  presumably behave like `-j` (usage exit 1). [INFERENCE]
- `hyprwm/Hyprland` `hyprctl/main.cpp` was not fetchable in this env (raw.githubusercontent
  404 at both `v0.56.2` and `main`); conclusions rest on black-box probes of the
  installed 0.56.2 binary whose banner matches the freeze facts.
- F1's ceiling is scoped to hyprctl 0.56.2's parser; a future hyprctl that joins argv
  or splits on `;` inside batch mode would raise it. Recommend the delivered
  tools/mado-options.py apply the probe guard (reject empty/`-`-prefixed, exit 2 or a
  named skip) to config keys too, validate `isinstance(rec, dict)` before membership
  (:638→:639 order), and consider `env=` pinning + a reply-size cap.
- Unicode keys untested; byte-pass-through behavior makes an exec-level surprise
  unlikely. [INFERENCE]

## Tooling and lane bounds

No tools installed or updated (python3 3.14.8 + coreutils sufficed); pacman untouched;
no host-service or compositor mutation (only `hyprctl version` / `hyprctl getoption -j`
read-only verbs); no git/jj commands; all scratch under /tmp/rts and deleted. Writes
confined to this seat's Report file.
