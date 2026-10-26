# RevRefTool — attack findings on the C1 reference tool (round 43 w1, 2026-10-26)

Target: `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` — sha256
`e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` (20507 B, 417 lines).
Interpreter: host `python3` 3.14.8. Full per-case log: `receipt.txt` in this seat dir (rounds 1–4).
Method: 45 timed subprocess cases; every hang probe killed at 6–8 s; stdout/stderr captured.
Fixtures lived under `/fast/scratch/hyaku/mado-r43/RevRefTool` and were removed after the round;
repro commands below rebuild everything they need. No `lsp` device is mounted in this session —
all citation checks are text grep against the frozen files (recorded per lane rules).

Contract = the tool's own docstring; the counter states: "The tool's contract is the docstring of
the reference at `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (frozen at the round-42 freeze) and is
restated here" (quality/counters/c1-r42-geometry.py:13). Promises attacked:
- tool:18 "Setup failure: stdout is exactly one line `MADO_GEOMETRY: SETUP <reason>`, exit 2,"
- tool:21 "larger than 1048576 bytes is too_large"
- tool:51 "stderr empty on exit 0/1/3/4"
  every run ends in a verdict block + final summary line, or a SETUP line; exit in {0,1,2,3,4};
  counter restatement adds "must return, never block on one" for PATH inputs
  (quality/counters/c1-r42-geometry.py:20) and "on rc 0/1/3/4 stderr must be empty"
  (quality/counters/c1-r42-geometry.py:63).

Repro preamble for every command below:

```bash
T=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt
D=$(mktemp -d -p /fast/scratch/hyaku/mado-r43); cd "$D"
```

## Violations

### V1  HIGH — ReDoS hang through the tool's own SAFE regex gate (tiny input, no output, no exit)
- Input: rules file `windowrule = size 420 500, match:class (a|aa)+$` (44 B) + one client whose
  class is `"a"*n + "b"`. `(a|aa)+$` passes the tool's own gate: every char is in the SAFE alphabet
  (tool:69), it contains none of the banned substrings `(?` `*+` `++` `?+`, it is ≤200 chars, and it
  compiles under `re` — the small-n runs show it accepted: `MADO_GEOM_RULE: n=1 ... class=(a|aa)+$`.
  The gate's blacklist targets quantifier stacking, not alternation under `+`; blowup is exponential
  in the CLASS length, so the 200-char regex cap does not help. The match itself is
  tool:183 "return re.fullmatch(rx, cls) is not None" with Python `re` (backtracking).
- Expected per contract: a verdict or a SETUP line, exit in {0,1,2,3,4}, in bounded time.
- Observed (timed ladder, class `a`*n+`b`): n=20 → 0.019 s rc=3; n=26 → 0.033 s; n=30 → 0.120 s;
  n=34 → 0.692 s; n=38 → 4.573 s (≈×6.6 per +4 a's ≈ 1.6^n); n=1000 (JSON ≈ 1.1 KB) → killed at
  6 s, stdout 0 B, stderr 0 B; n=1048175 (largest class whose JSON stays ≤ 1 MiB, 1048254 B) →
  killed at 6 s, 0 B/0 B. Exit observed only via the killer (124 under `timeout`).
- Severity: HIGH. ~1.2 KB of total input hangs the tool indefinitely; the tool buffers all output
  and writes once (tool:261), so a hung run shows zero bytes — a consumer cannot even see progress.
- Repro:
```bash
python3 -c 'open("cl.json","w").write(__import__("json").dumps([{"class":"a"*45+"b","size":[420,500],"floating":True,"mapped":True}]))'
printf 'windowrule = size 420 500, match:class (a|aa)+$\n' > r.conf
time timeout 6 python3 "$T" --clients cl.json --rules r.conf; echo "exit=$?"   # 124, no output
```

### V2  MEDIUM — legal-input scan blowup: O(rules × clients) `re.fullmatch` with pattern-cache thrash
- Input: rules file with 24000 supported size rules (distinct regexes `c00000`..`c23999`,
  1,008,000 B ≤ 1 MiB, every line individually contract-legal) + 5000 clients (≈350 KB).
- Expected: verdict or SETUP in bounded time (both inputs are under the size cap and well-formed).
- Observed: killed at 8 s with stdout 0 B, stderr 0 B. Anchors: 4 clients × 24000 rules = 96k
  matches → 0.941 s (≈9.8 µs/match — the `re` cache holds ~512 patterns, 24000 distinct regexes
  thrash it, so each call recompiles); 400 rules × 200 clients → 0.100 s. Extrapolation for the
  full case: 1.2e8 matches ≈ 20 min [INFERENCE from the two measured anchors].
- Severity: MEDIUM (needs a ~1 MiB hostile rules file, but nothing in the contract bounds the
  rules×clients product).
- Repro:
```bash
python3 -c 'open("r.conf","w").write("".join("windowrule = size 1 2, match:class c%05d\n"%i for i in range(24000)))'
python3 -c 'open("cl.json","w").write(__import__("json").dumps([{"class":"c%05d"%i,"size":[3,4],"floating":True} for i in range(5000)]))'
time timeout 8 python3 "$T" --clients cl.json --rules r.conf; echo "exit=$?"   # 124, no output
```

### V3  MEDIUM — deeply nested JSON: RecursionError traceback, exit 1, stderr nonempty
- Input: clients file = `[`*D + `]`*D (valid JSON — a list whose elements are lists, so the
  contract maps it to SETUP bad_json: "a clients input that is not UTF-8 JSON holding a list whose
  every element is an object is bad_json", tool:22-23).
- Expected: `MADO_GEOMETRY: SETUP bad_json`, exit 2, stderr empty.
- Observed through the tool: D=50000 → clean `SETUP bad_json` exit 2 (the C scanner still parses
  that depth); D=55000, 60000, 70000, 100000, 524288 → traceback, exit 1, stderr 1499 B, stdout 0 B.
  Tail of the D=100000 stderr: `RecursionError: Stack overflow (used 8152 kB) while decoding a JSON
  array from a unicode string`. The tool catches only `(UnicodeDecodeError, ValueError)`
  (tool:165) — `RecursionError` escapes; main catches only `Setup` (tool:411).
- Severity: MEDIUM (1 MiB of `[` is a legal-sized input that crashes instead of SETUP).
- Repro:
```bash
python3 -c 'open("cl.json","wb").write(b"["*55000 + b"]"*55000)'
printf 'windowrule = size 1 2, match:class a\n' > r.conf
python3 "$T" --clients cl.json --rules r.conf; echo "exit=$?"   # 1 + RecursionError traceback
```

### V4  MEDIUM — broken pipe: silent truncation with exit 0 on this host (traceback shape on EPIPE-writing kernels)
- Input: 30000 matched clients with no `size` key (fixture 1,020,000 B ≤ 1 MiB) → 30001 output
  lines, 2,880,203 B; consumer reads one line then closes the pipe (`| head -1`).
- Expected per contract: either the full output with the final summary line, or a SETUP line;
  "stderr empty on exit 0/1/3/4" (tool:51) — and exit 0 must mean the promised output was delivered.
- Observed on this host: `python3 "$T" --clients cl.json --rules r.conf | head -1` → consumer gets
  exactly 1 line, tool exit code 0 (`PIPESTATUS=0`), stderr empty. The final `MADO_GEOMETRY:`
  summary line is never delivered while exit 0 asserts OK — silent truncation.
- Mechanism (measured, not assumed): the tool writes its whole output as ONE write (tool:261);
  `/proc/<pid>/syscall` showed the child blocked in `write(fd=1, count=2880203)`,
  wchan `anon_pipe_write`, pipe capacity `F_GETPIPE_SZ` = 4096 B. When the reader closes, THIS
  host's kernel wakes the blocked writer with SUCCESS (data discarded): an instrumented child
  doing the identical single-write shape reported `RETURNED 2880262` after the close and exited 0;
  raw `os.waitpid` on the tool gave status 0x0 (exit 0, no signal). A write that STARTS after the
  close does get EPIPE: a child whose post-close third write (`END\n` after a flushed rule line and
  a blocked 3 MB write) died with `BrokenPipeError: [Errno 32] Broken pipe`, raw status 0x100
  (exit 1), and an in-process 3 MB writer raised `BrokenPipeError` the same way. The tool has no
  handler for either shape: no
  try/except around tool:261, main catches only `Setup` (tool:411). On a kernel that wakes blocked
  writers with EPIPE (mainline behavior [INFERENCE]) the same sequence yields a traceback, exit 1,
  stderr nonempty — violating tool:51. Either kernel behavior breaks the output contract; this
  host's breaks it silently.
- Severity: MEDIUM (`| head` is a plausible consumer; the counter never exercises a short-lived
  reader, so this is outside its fixtures).
- Repro:
```bash
python3 -c 'open("cl.json","w").write(__import__("json").dumps([{"class":"a","floating":True}]*30000))'
printf 'windowrule = size 1 2, match:class a\n' > r.conf
python3 "$T" --clients cl.json --rules r.conf | head -1; echo "PIPESTATUS=${PIPESTATUS[0]}"
# -> 1 line, PIPESTATUS=0, stderr empty; 30000 client lines + summary silently discarded
```

### V5  LOW-MEDIUM — stdin closed (fd 0): AttributeError traceback, exit 1, no SETUP
- Input: `--clients -` with fd 0 closed at exec (`0<&-`).
- Expected: a SETUP line, exit 2 (a closed standard input is a setup failure; the contract's
  reason list has no slot for it, but the promise is "a verdict or SETUP and an exit code").
- Observed: exit 1, stdout 0 B, stderr 463 B ending
  `AttributeError: 'NoneType' object has no attribute 'buffer'` — with fd 0 closed, CPython sets
  `sys.stdin = None` and tool:410 `run(sys.argv[1:], sys.stdin.buffer)` raises before any logic.
- Severity: LOW-MEDIUM (environmental trigger; crash instead of SETUP).
- Repro: `printf 'windowrule = size 1 2, match:class a\n' > r.conf; python3 "$T" --clients - --rules r.conf 0<&-; echo "exit=$?"`

### V6  LOW — stdout closed (fd 1), normal path: AttributeError traceback, exit 1
- Input: valid run with fd 1 closed at exec (`>&-`).
- Expected: cannot print — but the contract promises an exit code and no crash noise; a robust
  shape is SETUP (or a silent defined code). Observed: exit 1, stderr 597 B ending
  `AttributeError: 'NoneType' object has no attribute 'write'` at tool:261 (`sys.stdout` is None).
- Severity: LOW. Repro: `python3 "$T" --clients cl_ok.json --rules gk.conf >&-; echo "exit=$?"`

### V7  LOW — stdout closed (fd 1), SETUP path: exit 2 with NO SETUP line anywhere
- Input: `--clients /nonexistent` with fd 1 closed.
- Expected per tool:18 "stdout is exactly one line `MADO_GEOMETRY: SETUP <reason>`" — impossible
  with fd 1 closed, but the observed shape is the worst one: `print()` to `sys.stdout is None`
  no-ops SILENTLY — exit 2, stdout 0 B, stderr 0 B. The caller sees exit 2 with no reason at all.
- Severity: LOW. Repro: `python3 "$T" --clients /nonexistent --rules gk.conf >&-; echo "exit=$?"`

### V8  LOW — 5000-digit integer in `size`: valid JSON rejected as `bad_json`
- Input: `[{"class":"a","size":[<5000 nines>,1],"floating":true,"mapped":true}]` — per contract
  this IS "UTF-8 JSON holding a list whose every element is an object" (tool:22-23), so it must
  NOT be bad_json; the size is simply not two small ints → BADSIZE verdict. The contract's
  definition is at tool:22-23.
- Observed: `MADO_GEOMETRY: SETUP bad_json`, exit 2. Python 3.11+ caps int string conversion at
  4300 digits; `json.loads` raises `ValueError`, which tool:165 catches as bad_json. A 201-digit
  size works correctly (parsed, verdict DIFFER, exit 1, 201-digit size echoed in the client line).
- Severity: LOW (hyprctl never emits such sizes; but the SETUP reason contradicts the contract's
  own bad_json definition).

## Robust under attack (no violation found)

| case | input | observed | time |
|---|---|---|---|
| baseline | gkeep rules + 1 AGREE client | rc=0, verdict OK, stderr empty | 0.022 s |
| selftest | `--selftest` | `MADO_GEOMETRY_SELFTEST: 73/73 passed`, rc=0 | 0.023 s |
| stdin /dev/null | `--clients -`, stdin=DEVNULL | `SETUP bad_json` exit 2 (contract-clean) | 0.021 s |
| FIFO as --rules | mkfifo path | `SETUP unreadable` exit 2, returns immediately (never blocks — counter:20 satisfied) | 0.019 s |
| FIFO as --clients PATH | mkfifo path | `SETUP unreadable` exit 2 | 0.020 s |
| /dev/stdin as --clients | data available on stdin | `SETUP unreadable` exit 2 (non-regular refused per contract) | 0.016 s |
| symlink dangling / loop / →/dev/null | rules path | `SETUP unreadable` exit 2 each | ~0.019 s |
| symlink → regular file | rules path | follows it, normal verdict rc=0 | 0.017 s |
| sparse 2 GiB clients file | truncate -s 2G | `SETUP too_large` exit 2, bounded read, no memory blowup | 0.019 s |
| 1 MiB single-line rules (effect-token shape) | one 1 MiB line | counted `other=1`, rc=4 NO_SIZE_RULES | 0.030 s |
| 1 MiB single-line rules (200k-field shape) | one 1 MiB `windowrule = size 1 2,junk,…` line | `unsupported=1`, rc=4 | 0.029 s |
| 201-digit integer size | size [10^200, 1] | verdict DIFFER, exit 1, size echoed | 0.019 s |
| 1e999 float size | size [1e999, 2] | verdict BADSIZE, exit 0 OK | 0.019 s |
| 400k-char UTF-8 class (800 KB JSON) | class "ä"*400000, rule `.*` | verdict OK rc=0, 2.4 MB stdout | 0.034 s |
| 30000 BADSIZE clients (1.02 MB) | no size key | rc=0 OK, 2.88 MB stdout | 0.085 s |
| 30000 minimal clients | {"mapped":true} ×30000 | rc=0 OK | 0.078 s |
| file changing during read | 20 runs, +100 KB × 30 appends racing each read | stable rc=3 every run, never too_large/SETUP flip; reads are single open-anchored passes (fd fstat'ed, tool:73-86) — no violation | avg 0.017 s |

## Environment notes (measured on this host)
- python3 3.14.8; `json` C-scanner parses nesting depth 50000 but raises RecursionError at 60000
  (in-kernel probe) — the tool's crash zone starts between those (clean at 50000, traceback at
  55000, both through the tool).
- int→str digit limit (Python 3.11+ default 4300) is what turns the 5000-digit size into a
  `ValueError` inside `json.loads`.
- Pipe capacity `F_GETPIPE_SZ` = 4096 B; a blocked `anon_pipe_write` is woken with SUCCESS (data
  discarded) when the reader closes; only a write STARTED after the close gets EPIPE. This is the
  host kernel's behavior (measured via instrumented children and raw `waitpid`); mainline Linux
  wakes blocked writers with EPIPE [INFERENCE]. The tool's V4 shape lands on the silent branch.
- No tools were installed for this seat (system python3 only); no pacman transactions; no
  compositor contact; no git/jj mutations; no subagents spawned.

## Residual / not covered
- TTY stdin (`--clients -` on a real terminal): no tty available to a leaf seat; /dev/null covered.
- SIGINT/SIGTERM disposition and stderr-closed: not probed (out of the assigned input list).
- The rules×clients race between two `--rules` reads: single open-anchored read per file makes the
  window sub-millisecond; 20-run append probe showed no effect. A deterministic inter-read swap
  was not attempted.
- Memory ceilings under the counter's bwrap/RLIMIT sandbox: out of scope for a host-side attack.
