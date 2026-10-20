# ReviewPathSafety — `refuse_path` / `discover` / `scan_file` adversarial review (round 17, w2 FALSIFY)

- **Lane**: `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Target**: `tools/mado-tripwire.py` at lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`
- **File identity**: `git show 988b858:tools/mado-tripwire.py | sha256sum` =
  `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`, identical to the worktree
  copy (`git status --porcelain -- tools/mado-tripwire.py` empty; 818 lines). Every finding below
  is bound to the pushed commit, not to a local edit.
- **Installs**: **none**. No pacman/yay/paru/sudo/doas/uv/npx/cargo/curl-to-shell, no
  systemctl/journalctl/hyprctl/libinput/evtest/pgrep, no compositor, device or `<bin> --version`
  command. No file under the real `/home/vgpnk/.omp/agent` was opened; the tool was never pointed
  at the real store (fake HOME only).
- **Method**: a fake HOME per scenario under `/tmp/psaf/` so `os.path.expanduser("~/.omp/agent")`
  resolves into an isolated tree (HOME **is** honoured by `python3 -I`; only `PYTHON*` is ignored).
  Every transcript is a real-shape OMP record,
  `{"type":"message","timestamp":…,"message":{"role":"assistant","content":[{"type":"toolCall","id":…,"name":"bash","arguments":{"command":CMD}}]}}`;
  nothing in any fixture was executed. Command under test:
  `python3 -I tools/mado-tripwire.py --scan PATH…` (plus `--permit` where stated). No lane file was
  modified; all fixtures live under `/tmp/psaf` and are reproducible from the inputs quoted below.

## Verdict

**The attack succeeded.** Seven defects reproduced, each with a literal input/expected/got:
the `~/.omp/agent/sessions` boundary is **inverted** (ancestor accepted, allowed root refused);
duplicate/overlapping roots **double every count and finding**; `REFUSED_NAMES` is **dead for
every alternative that could protect a secret and harmful for the only alternatives that can
fire**, letting one benign filename nullify a whole scan; the **internal-error verdict violates
its own `mado-tripwire-verdict-v1` schema** and is reachable from an unmodified run; a **symlinked
subtree is silently dropped under `clean`**; a verdict can contain **non-JSON `Infinity`**; and an
early-closed stdout yields **exit 120**, outside the documented `0/1/2` map.

What this is **not**: the C3 numeric claims are not refuted. All three suites reproduce exactly
(core `9/9`, compound `16/16`, hardening `33/33`, `SELFTEST_SCRIPT_SHA256: 4ced68d3…`) and the two
path cases the suites carry (`refused-db-name`, `refused-symlink`) are correct. The defects are
outside the 58 cases — the green light does not support the path-safety reading, in the same shape
as `ReviewPrefixes.md` §Suite gap for classifier coverage. No anchor/pacman-log join was rerun by
this item (owned by `AnchorRerun`).

## Findings

### F1 — HIGH: the agent-store boundary is inverted; the natural "all sessions" root is unusable

`refuse_path` (lines 589–590) refuses only a path strictly **under** `~/.omp/agent` and strictly
**under** `…/agent/sessions`; equality and ancestors satisfy neither test.

**Input** (fake HOME `H=/tmp/psaf/home3`, agent root contains only
`H/.omp/agent/sessions/p/s/benign.jsonl` with one `ls` toolCall):
`--scan H/.omp/agent`.

**Expected**: exit 2, `refused path outside ~/.omp/agent/sessions`, because the path is *outside*
that subtree and the message/`SKILL.md:528` posture is "sessions only" (`SiblingOverlap` records
"never default-walk the agent store").

**Got**: exit **0**, `MADO_TRIPWIRE: clean`,
`files[0].path = ~/.omp/agent/sessions/p/s/benign.jsonl`. The entire store (including
`credentials/`, `agent.db`, every non-session directory) was walked and `stat`ed, and the sessions
file was scanned as if the root were legal. (`agent.db` itself is not opened — only `.jsonl` are
opened — but the caller's refusal expectation is violated.)

**Companion, same predicate** (fake homes `home`, `home2`, `home3`, repeated):
`--scan H/.omp/agent/sessions` (and the trailing-slash form) → exit **2**
`refused path outside ~/.omp/agent/sessions: /tmp/psaf/home3/.omp/agent/sessions` — the path *is*
`~/.omp/agent/sessions`, yet is refused because the allow test is
`real.startswith(os.path.join(agent,"sessions") + os.sep)`, which equality fails.

So the two natural roots produce the two wrong answers: **the ancestor is accepted and the allowed
root is refused**. The documented per-lane form `<session-dir>/<Lane>R<N>` still works (exit 0/1 as
appropriate, verified), which is why no suite case catches this.

**Minimal fix**: `refuse` iff `(real == agent or real.startswith(agent+os.sep)) and not
(real == sessions or real.startswith(sessions+os.sep))`.

### F2 — MEDIUM: duplicate / overlapping roots double `files`, `counts` and `findings`

`discover` (596–616) appends every walked `.jsonl` with no de-duplication and `scan` (692–702)
loops over the list, so a file reachable twice is measured twice.

**Input**: `dupdir/one.jsonl` = one `pacman -Syu` toolCall.
- `--scan dupdir dupdir`
- `--scan dupdir dupdir/one.jsonl`

**Expected**: each file once — `files` length 1, `counts.host_mutation == 1`, one finding row.

**Got** (both forms): `files` length **2**, the same `sha256` twice;
`counts={"host_mutation": 2, …}`; **two identical finding rows** (same `file`, `line: 1`,
`rule: pacman:-Syu`, same `tool_call_id`). Single-root control: `files=1`, `host_mutation=1`.

This is a measurement error, not a detection error, and it lands directly in the receipt fields
the round quotes (`files`, `counts`). Any invocation that passes a directory plus a glob of the
same directory (e.g. `--scan SESS SESS/MadoR15`) silently doubles the evidence.

**Minimal fix**: de-duplicate by `(st_dev, st_ino)` (or `os.path.realpath`) in `discover`.

### F3 — MEDIUM: `REFUSED_NAMES` cannot protect anything it names, and the branches that do fire are false positives

`REFUSED_NAMES` (87–88) is applied at line 591, but every file that reaches `scan_file` must end
`.jsonl` (`discover` 606–607 for walks, 609 for explicit files; `scan_file` is the only opener,
628). Therefore the regex can only ever see `*.jsonl` basenames:

| alternative | can match a scanned `.jsonl`? | effect |
|---|---|---|
| `.*\.db`, `.*\.db-(shm\|wal)`, `auth\.json` | **no** (must end `.db`/`-shm`/`-wal`/`.json`) | unreachable — dead branch |
| `agent\.db.*` | yes (`agent.db.jsonl`) | the only branch with a defensible target |
| `oauth.*` | yes (`oauth-login-flow.jsonl`) | refuses a legitimate transcript |
| `credentials?(\.[a-z]+)?` | yes (`credentials.jsonl`) | refuses a legitimate transcript |

**Input**: session dir containing
`ok.jsonl` (one `sudo pacman -Syu`) and `oauth-login-flow.jsonl` (one `ls`);
`--scan <sess>`.

**Expected**: both scanned; exit 1 with the `sudo`/`pacman` findings.

**Got**: exit **2** `refused file name: …/oauth-login-flow.jsonl`, `files=[]`, `findings=[]` —
one benignly named file suppresses **every finding in the tree** (exit 2 discards partial results
by design). Same class: `credentials.jsonl` → exit 2 refused; `agent.db.jsonl` → exit 2 refused
(kills the hardening fixture if it is ever scanned in place); `auth.jsonl` and
`x.db-wal.jsonl` → exit 0 clean (dead branches confirmed by construction).

`refused-db-name` in `hardening` only tests the single live branch; no case tests the false-positive
side. A name policy over a `.jsonl`-only reader is either inert or harmful unless it is limited to
`agent\.db.*`.

**Minimal fix**: keep only `^agent\.db.*$` (or drop the name check entirely, since no non-`.jsonl`
file is ever opened) and do not refuse `oauth*`/`credentials*` `.jsonl` transcripts.

### F4 — MEDIUM: the internal-error verdict violates its own schema, reachable unmodified

`classify_eval` guards `compile` only with `except (SyntaxError, ValueError)` (521–525). CPython
raises `MemoryError: Parser stack overflowed - Python source too complex to parse` for a long
unary chain; the exception is not `CouldNotEvaluate`, escapes `run_scan` (709–726), and is caught
by the top handler (809–818), which prints its **own literal payload**.

**Input**: valid JSONL record whose only toolCall is
`{"name":"eval","arguments":{"language":"py","code":"x=" + "-"*100000 + "1"}}` (a valid-JSON
string whose value is that Python expression's result);
`--scan trig`.

**Expected**: a `could_not_evaluate` verdict with the same `mado-tripwire-verdict-v1` key set as
every other exit-2 verdict (`files`, `findings`, `counts`, `permitted`, `unpermitted`).

**Got**: exit 2, but line 2 is exactly
`{"schema":"mado-tripwire-verdict-v1","exit":2,"error":"internal MemoryError"}`
— `files`, `findings`, `counts`, `permitted`, `unpermitted` are **missing**. Compare the F1 exit-2
payload, which carries all five. A consumer doing `jq -r '.counts.host_mutation'` gets `null`;
a key-checking consumer errors. The same shape is produced when the trigger follows a real finding
in the same run (exit 2 correctly wins, but the payload still lacks the receipt fields).

Secondary: `except BaseException` also swallows `KeyboardInterrupt`, and the handler itself is
unguarded — a second failure (e.g. closed stdout) escapes as a traceback.

**Minimal fix**: add `MemoryError`/`RecursionError` to the `compile` guard (count the cell as
`eval_unparsed`), and emit the internal verdict through one helper that always supplies the full
key set.

### F5 — LOW: a symlinked subtree inside a walked tree is silently skipped and reported `clean`

`os.walk(..., followlinks=False)` (603) never descends symlinked directories, and nothing counts or
discloses the omission; the leaf cases fail closed, this one fails open.

**Input**: `walklink2/real/benign.jsonl` (one `ls`) and
`walklink2/into -> outside2/` where `outside2/find.jsonl` is one `pacman -Syu`; `--scan walklink2`.

**Expected**: exit 2 (consistent with the leaf-symlink refusal: explicit symlink arg → 2, dangling
symlink `.jsonl` in a walk → 2), or at least a declared skipped-link count so `clean` is not
overbroad.

**Got**: exit **0** `MADO_TRIPWIRE: clean`, `files=[walklink2/real/benign.jsonl]`; the finding
behind the symlink is invisible and undisclosed. The docstring's limit list names scripts,
functions, other tools and other sessions — not symlinked subtrees — so this is an undeclared
coverage hole. Three symlink policies coexist: ancestor symlink in an argument is followed
(link-to-sessions scanned fine), leaf symlink is refused, interior symlink is skipped silently.

### F6 — LOW: the verdict line can contain `Infinity` (not JSON)

`json.loads(..., parse_constant=reject_constant)` rejects the literals `NaN`/`Infinity`/`-Infinity`
but not exponent overflow: `1e400` parses to `float('inf')`. `scan_file` copies `timestamp`
verbatim into every finding and `emit` (704–707) uses `json.dumps` defaults (`allow_nan=True`).

**Input**: `{"type":"message","timestamp":1e400,"message":{…"command":"pacman -Syu"…}}`.

**Expected**: RFC 8259 JSON on line 2.

**Got**: `… "rule": "pacman:-Syu", "timestamp": Infinity, …` with exit 1. Python and jq 1.7 accept
it; strict parsers (e.g. `JSON.parse`, Go `encoding/json`) reject the entire verdict. The tool is
a machine interface, so the payload — not just the exit code — is the contract.

**Minimal fix**: `parse_float` that rejects non-finite values (line → invalid line → exit 2), or
normalise to `null`; serialise with `allow_nan=False`.

### F7 — LOW: early-closed stdout exits 120, outside the documented `0/1/2` map

**Input**: `big/many.jsonl` = 400 `pacman -Syu` records;
`python3 -I tools/mado-tripwire.py --scan big | head -c 1`.

**Expected**: `0`, `1` or `2` with the second line intact, per the docstring/`SKILL.md` verdict map.

**Got**: `PIPESTATUS[0]=120`, stderr
`Exception ignored while flushing sys.stdout: BrokenPipeError: [Errno 32] Broken pipe`; line 2 is
truncated/absent. (Small outputs hide this because both lines fit the pipe buffer; the failure
appears once findings exceed it.) The internal handler never sees the error because it happens at
interpreter flush.

**Minimal fix**: on `BrokenPipeError`, close/detach `sys.stdout` and exit 2 (the documented
"could-not-evaluate"), or write the verdict once and `os._exit` after a checked flush.

### F8 — INFO: `files[].path` echoes the argv form, not a canonical path

`--scan one.jsonl` from inside the fixture directory records `"path": "one.jsonl"`, while the same
file via `./one.jsonl`, a relative directory, or an absolute path records those strings. `sha256`
identifies the bytes, but any receipt join keyed on `file` (the hardening/`expected.json` key
function itself has a `file` mode) is invocation-form dependent, and F2's duplicate problem is
invisible to a reader who compares path strings. Fix: store `os.path.realpath(path)` alongside the
argv form.

### F9 — INFO: `--permit` must be the last argument or the path is parsed as a class

`--scan DIR --permit package_query` → exit 1 as intended. `--scan --permit package_query DIR` →
exit 2 `unknown permit class` (the directory is consumed as a permit class because everything after
`--permit` becomes the class set, 789–797). Correct exit code, misleading diagnostic; the usage
line shows only the trailing form.

## Verified correct (so the report is not one-sided)

With the same hermetic harness: explicit symlink file → 2 `refused symlink`; explicit symlink
directory → 2; dangling `.jsonl` symlink inside a walk → 2; FIFO passed directly → 2; FIFO inside a
walked directory → 2 with no hang and no open; `/dev/null` → 2 `not a regular file or directory`;
unreadable directory (mode 000, uid 1000) → 2 `unreadable directory: <path>`; unreadable file → 2
`unreadable file`; empty directory and a directory containing only `A.JSONL` → 2 `no .jsonl file
found`; `sessions/../agent.db` → 2 (path check precedes name/suffix checks); explicit
`agent.db` → 2; invalid JSON line → 2 `invalid line (ValueError)`; a directory named `x.jsonl`
containing `inner.jsonl` is walked and its findings found; "2 wins over 1" holds (a valid finding
followed by a FIFO/refused file → 2 with `files: []`).

## Suite gap

`SELFTEST_SUMMARY: 9/9`, `16/16`, `33/33` with the pinned script SHA. The only path-relevant cases
are `refused-db-name` (`agent.db.jsonl`, the one live `REFUSED_NAMES` branch) and `refused-symlink`.
No case exercises: agent-root ancestor (F1), exact `sessions` root (F1), duplicate/overlapping
roots (F2), `oauth*`/`credentials*` false positives (F3), the internal `MemoryError` payload (F4),
a symlinked subtree (F5), `Infinity` (F6), broken pipe (F7), FIFO (already correct, untested), or
unreadable directories. Add at least F1–F4 as cases before citing the suites as path-safety
evidence.

## Residual risks and verification gaps

- **TOCTOU between check and open** [INFERENCE, not raced]: `refuse_path` uses `os.lstat` (582) and
  `scan_file` later calls `open(path, "rb")` (628) — no `O_NOFOLLOW`, no `os.fstat` on the
  descriptor. A swap of a regular file for a symlink in that window defeats the symlink refusal.
  The window is small; I did not construct a race, so this is a design reading, not a
  counterexample.
- **Hardlink/copy bypass** [INFERENCE from design]: the policy is path/name based, so a hardlink or
  copy of an `agent.db` payload placed at `sessions/.../x.jsonl` is opened and parsed. Non-JSON
  content aborts at `invalid line` before any text is echoed; a JSON-shaped secret would be parsed
  and its strings echoed in findings.
- **Unbounded read** (629): the whole `.jsonl` is buffered; a very large file OOMs into the F4
  handler path, i.e. a schema-incomplete verdict rather than a sized refusal.
- **Not tested as root** (uid 1000): the unreadable-directory/file cases relied on normal
  permissions; root would bypass them.
- **Real-store behaviour not exercised**: no run against `/home/vgpnk/.omp/agent`; F1's impact on
  the real tree is inferred from the fake-home tree of identical shape.
- Not attacked here (other items own them): command classification (wrapper arity, quoting),
  redaction, `--selftest` spec handling, the real-transcript anchor and pacman-log joins.
