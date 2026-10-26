# RevRefTool — round 43 w1 report (2026-10-26)

Status: DONE. The C1 reference tool was attacked outside the counter's 37 fixtures: 45 timed cases
(receipt rounds 1–4) plus a receipt-backing/quote-verification round 5. No subagents (leaf); no
tools installed (system python3 only); no pacman; no compositor contact; no git/jj mutations.

Target: `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`, sha256
`e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` (20507 B, 417 lines).
Contract = the tool's own docstring, designated by the counter
(quality/counters/c1-r42-geometry.py:13). Host python3 3.14.8.

Deliverables in this seat dir (`.ufo/waves/round-43/w1/RevRefTool/`):
- `findings.md` — every case as input / expected-per-contract / observed / time / severity / repro.
- `receipt.txt` — raw captured log: rc, wall time, stdout/stderr heads, exception tails, the
  instrumented-child and `head -1` probes, and the quote verification (fragment → line hits).

## Violations (8 — each yields a traceback, a hang > 5 s, or a broken output promise)

1. **V1 HIGH — ReDoS hang through the tool's own SAFE gate.** Rule regex `(a|aa)+$` passes every
   gate (SAFE alphabet tool:69, no `(?`/`*+`/`++`/`?+`, ≤200 chars, compiles); the match is
   `re.fullmatch` (tool:183) under backtracking Python `re`. Class `"a"*n+"b"`: 0.019 s (n=20) →
   4.573 s (n=38) ≈ 1.6^n; n=1000 (≈1.1 KB of JSON) and n=1048175 (largest legal class) killed at
   6 s with ZERO stdout/stderr — no verdict, no SETUP, no exit. The gate bans quantifier stacking,
   not alternation under `+`; the 200-char regex cap is irrelevant because blowup is exponential in
   the class length.
2. **V2 MEDIUM — legal-input scan blowup.** 24000 supported rules (1,008,000 B ≤ 1 MiB) × 5000
   clients → killed at 8 s, zero output. Anchors: 96k matches = 0.941 s (~9.8 µs/match; `re`'s
   ~512-pattern cache thrashes on 24000 distinct regexes), 80k matches = 0.100 s; full case ≈
   20 min [INFERENCE from anchors]. Nothing in the contract bounds the rules×clients product.
3. **V3 MEDIUM — deep-nested JSON crashes instead of SETUP.** `[`*D+`]`*D: D=50000 → clean
   `SETUP bad_json` exit 2 (contract-correct: elements are lists, tool:22-23); D=55000/60000/70000/
   100000/524288 → RecursionError traceback, exit 1, stderr 1499 B ("Stack overflow (used 8152 kB)
   while decoding a JSON array"). Tool catches only `(UnicodeDecodeError, ValueError)` (tool:165).
4. **V4 MEDIUM — broken pipe: silent truncation with exit 0 on this host.** `… | head -1` on a
   30001-line output: consumer gets 1 line, tool exits 0, stderr empty, final summary never
   delivered. Mechanism measured: the tool writes everything as ONE write (tool:261), blocks in
   `anon_pipe_write` (pipe capacity 4096 B), and THIS host's kernel wakes the blocked writer with
   SUCCESS (instrumented identical-shape child: `RETURNED 2880262` after the close; tool raw
   `waitpid` status 0x0). A write STARTED after the close gets real EPIPE (child died
   `BrokenPipeError`, raw status 0x100; in-process writer raised it too). No EPIPE handling
   anywhere (main catches only `Setup`, tool:411). On a kernel that wakes blocked writers with
   EPIPE (mainline [INFERENCE]) the same sequence is a traceback, exit 1, stderr nonempty —
   violating "stderr empty on exit 0/1/3/4" (tool:51). Either way the output contract breaks.
5. **V5 LOW-MEDIUM — stdin closed (`0<&-`):** `AttributeError: 'NoneType' object has no attribute
   'buffer'` at tool:410, exit 1, no SETUP line.
6. **V6 LOW — stdout closed, normal path:** `AttributeError: 'NoneType' object has no attribute
   'write'` at tool:261, exit 1, traceback.
7. **V7 LOW — stdout closed, SETUP path:** `print()` to `sys.stdout=None` no-ops SILENTLY →
   exit 2 with NO SETUP line anywhere (violates "stdout is exactly one line …", tool:18).
8. **V8 LOW — 5000-digit integer in size:** valid JSON per the contract's own bad_json definition
   (tool:22-23) rejected as `SETUP bad_json` — Python 3.11+ 4300-digit int limit raises ValueError
   inside `json.loads`, caught at tool:165. A 201-digit size works (verdict DIFFER, exit 1).

## Robust under attack (17 cases, no violation)
/dev/null stdin → `SETUP bad_json`; FIFO as --rules and as --clients PATH → `SETUP unreadable`,
returns immediately (never blocks — counter:20 satisfied); `/dev/stdin` as --clients → `SETUP
unreadable`; symlinks dangling/loop/→/dev/null → `SETUP unreadable`, →regular file works; sparse
2 GiB → `too_large` in 19 ms (bounded read, no blowup); 1 MiB single-line rule files (two shapes)
→ clean rc=4 in ~30 ms; 201-digit size → DIFFER; `1e999` → BADSIZE verdict; 400k-char UTF-8 class
→ OK; 30000-client floods → OK ~80 ms; file-mutating-during-read probe (20 runs, appends racing
each read) stable — reads are single open-anchored passes. Baseline 22 ms; selftest `73/73` 23 ms.

## Environment notes (measured)
Pipe capacity `F_GETPIPE_SZ`=4096 B; blocked pipe writer woken with SUCCESS on reader-close (host
kernel; mainline wakes with EPIPE [INFERENCE]); json RecursionError boundary between depth 50000
(parses) and 60000 (raises), tool crash zone ≥55000; int digit limit 4300. Amplifier: the tool
buffers all output and writes once (tool:261), so any hang shows zero bytes — a consumer sees
nothing, not even partial progress.

## Residual / not probed
TTY stdin (no tty available to a leaf), SIGINT/SIGTERM, stderr-closed, deterministic inter-read
file swap (sub-ms window; 20-run race probe showed no effect), memory ceilings under the counter's
bwrap/RLIMIT sandbox. Details and repro commands: `findings.md` in this dir.
