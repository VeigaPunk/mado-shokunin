# w2 ExecC1Nonce — stability of PRED-C1-r47 on the L1 reference

Seat: ExecC1Nonce (leaf; no dispatch, no background jobs, no spawns). Wave w2 = FALSIFY, round 47 / hyaku run 9, 2026-10-26.
Target: **does the frozen C1 counter reliably score the L1 reference MET — 5 fixed nonces + 1 default-random, 2 counts at
a time** — and, if any run misses, is that a contract error or a flaky judge.

**Result: 12/12 runs TARGET_MET, no hole found, no FAIL line, no trip.** Every run:
`fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`.

Evidence: `receipt.txt` (generated from the logs), `logs/` (12 full stdout captures), `verify.sh` + `verify-out.txt`.

## Setup (exact, reproducible)

```
S=/fast/scratch/hyaku/mado-r47/ExecC1Nonce ; D=$S/clone
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"        # asserted before the first commit: ok
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a
cp .ufo/waves/round-47/l1-draft/mado-terminal.py "$D/tools/mado-terminal.py"
git -C "$D" add tools/mado-terminal.py
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand   # ddac61bcbd01d5e2de2dbdde914bf7289dcf1579
TMPDIR=$S/tmp python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r47-terminal.py \
    --repo "$D" --rev HEAD --work "$S/w" [--nonce N]
```

Pins re-verified at count time (each matches the counter's constant):
- `l1-draft/mado-terminal.py` sha256 `762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08`
  → committed blob `100755 ee46a8a67231eb7f99186bf41764cb6f30c2cfde`
- `fetch/xdg-terminal-exec` sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (= `PIN_SHA256`)
- `c1-r47-fixtures.json` sha256 `4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86` (= `FIXTURES_SHA256`), 190 fixtures
- host: nproc=32, `/usr/bin/bwrap`, `/usr/bin/strace`, python3 = `/usr/bin/python3.14` (bound inside the sandbox at
  `/usr/bin/python3`, `c1-r47-terminal.py:133,146`).

## Runs (every one: rc=0, exit 0)

| # | log | nonce | wall | concurrency |
|---|-----|-------|------|-------------|
| 1 | `logs/nonce-1.txt` | 1 | 53.1 s | with #2 |
| 2 | `logs/nonce-2.txt` | 2 | 53.0 s | with #1 |
| 3 | `logs/nonce-3.txt` | 3 | 57.3 s | with #4 |
| 4 | `logs/nonce-4.txt` | 4 | 57.2 s | with #3 |
| 5 | `logs/nonce-5.txt` | 5 | 48.5 s | alone (its pair was an aborted invocation, no count) |
| 6 | `logs/default.txt` | 1422439636 (drawn by the counter from `os.urandom`, printed in its summary) | 74.4 s | with #7 |
| 7 | `logs/nonce-1-repeat.txt` | 1 (repeat) | 74.3 s | with #6 |
| 8 | `logs/default-repeat.txt` | 1422439636 (repeat) | 64.0 s | with #11 |
| 9 | `logs/nonce-0.txt` | 0 | 53.7 s | with #10 |
| 10 | `logs/nonce-max32.txt` | 4294967295 (2³²−1) | 53.6 s | with #9 |
| 11 | `logs/nonce-max64.txt` | 18446744073709551615 (2⁶⁴−1) | 63.9 s | with #8 |
| 12 | `logs/nonce-7-timed.txt` | 7 | 53.092 s (elapsed written by the harness into `receipt.txt`) | alone |

Wall range 48.5–74.4 s; a single uncontended run is 53.1 s. Rows 7–12 are extras beyond the six required, added
because nonce only enters through `random.Random(nonce)` / `random.Random(nonce ^ 0x47C1)`
(`c1-r47-terminal.py:426,446`; default seed `c1-r47-terminal.py:473`) — so seeds at the boundaries and a same-seed
repeat are the cheap places a nondeterminism would hide.

Clause lines, identical in all 12 logs (`cat logs/*.txt | grep -E "clause=(a|s|x|g|r) " | sort | uniq -c`):
```
12 clause=a tool=present
12 clause=g generated=150/150
12 clause=r trips=0
12 clause=s rc=0 last='MADO_TERMINAL_SELFTEST: 43/43 passed'
12 clause=x explained=190/190
```
`verify.sh` additionally checks 12 logs, 0 `FAIL` lines, 12 summary lines, all `TARGET_MET`, all at rev
`ddac61bc…`, `trips=0` and `43/43` in every log.

## What the runs support (no hole)

- **Determinism per seed.** Two same-nonce pairs run minutes apart, each with fresh `mkdtemp` case roots
  (`run_case` builds `fx-*` / `job-<hex>-*` under `--work`), produced **byte-identical stdout**:
  `nonce-1 vs nonce-1-repeat: IDENTICAL line-for-line`, `default vs default-repeat: IDENTICAL line-for-line`.
  So path randomness of the harness roots does not leak into the judged text — the `$ROOT` rewrite holds.
- **No nonzero-trip run.** `clause=r trips=0` in all 12: over ~1820 sandbox invocations per count nothing forked or
  opened a socket after the sandboxed `python3` execve (`check_trace`, `c1-r47-terminal.py:186`).
- **No oracle drift.** No `SETUP`/drift line in any log, i.e. the pin reproduced its recorded `expect` for all 190
  fixtures on this host every time (`c1-r47-terminal.py:432` is the drift collector; it never fired).
- **Concurrent counts do not interfere.** Five pairs of concurrent counts (plus two singles) shared one `--work` dir
  (`$S/w`) and 32 host cores; each run
  creates its own `c1r47-*` work root, and `$S/w` was empty again after every run — no collision, no residue.
- **Host untouched.** Every resolver run carried `XDG_CACHE_HOME` inside the case root (`case_env`), and
  `~/.cache/xdg-terminal-exec` still has mtime `2026-10-26 17:42:25` (pre-run). No write outside `$S` and this seat dir;
  no terminal launched, no `dispatch`/`keyword`, no pacman.

## Judge-vs-contract reading (the question the task asks on failure)

No run failed, so no discrimination is needed. Had one failed, the separable gates are: `clause=a` (tool blob) and
`clause=s` (printed `43/43` ≥ `SELFTEST_MIN = 30`, `c1-r47-terminal.py:73`) are contract-shaped; a lone fixture `FAIL`
with the rest passing points at the per-invocation wall clock, the only load-sensitive gate — every sandbox call runs
under `timeout=30` with no retry (`c1-r47-terminal.py:158`), and a timeout is reported as `rc=124` and scored as a
mismatch. Margin, measured: ~1820 invocations (s 1; f 190×2 variants×2 processes = 760; x 190×(1 oracle + 1 explain +
≤2 observed) = ≤760; g 150×2 = 300) inside 53.1 s ⇒ ≈29 ms mean per invocation [INFERENCE: arithmetic on the observed
total, not per-call timing], i.e. ~1000× below the 30 s cap even with two counts sharing the host. The worst observed
total (74.4 s) still leaves the same order of margin.

## Risks / residuals (declared, not holes)

1. The 30 s per-invocation cap (`c1-r47-terminal.py:158`) is the single load-sensitive gate; a ≥30 s host stall inside
   any one of ~1820 invocations would turn into a spurious fixture FAIL. Not observed at 2-concurrent/32-core load;
   a 3rd+ concurrent count was not tried (seat cap: at most 2).
2. The judge is the host's bash/find/awk/tr/ls/md5sum (copies from `self.bin`, `c1-r47-terminal.py:121-146`) — a host
   tool upgrade changes the judge; this is the registration's declared residual, unchanged by these runs.
3. Seed coverage: 1–5, 0, 7, 2³²−1, 2⁶⁴−1 and one URANDOM seed per count. `gen_case` only consumes
   `random.Random` bits, so unsearched seeds can differ only by case *content*, which clause g judges against the live
   oracle — a latent contract hole there would show as a `first_fail` in `clause=g`, and none appeared
   (`c1-r47-terminal.py:449-452`).
4. Clause r trusts strace to see `execve("/usr/bin/python3"`; the argv literal is fixed at
   `c1-r47-terminal.py:146` and matched at `:186`, so that path cannot drift with the host's python version — observed
   stable across 12 runs on python 3.14.

## Reproduce

```
bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/ExecC1Nonce/verify.sh   # re-greps receipt + logs
```
`verify-out.txt`: 14/14 PASS, `VERDICT: all seat checks pass`.

Scratch `/fast/scratch/hyaku/mado-r47/ExecC1Nonce` (292 MB peak, all under `/fast`, never `/tmp`) was deleted after the
logs and receipt were copied here; tool installs/upgrades: none (no pacman, no uv/npx). Report trailers below.
