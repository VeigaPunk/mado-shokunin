# RevC1Counter — findings on PRED-C1-r42's frozen counter

Target attacked: `quality/counters/c1-r42-geometry.py` (sha256 `ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99`,
byte-identical to the freeze commit 809dc2c blob and to the round-43 base a35cfdf blob — verified by `git show <rev>:quality/counters/c1-r42-geometry.py | sha256sum`).
No edit was made to the counter or any tracked file. All experiments ran in scratch `/fast/scratch/hyaku/mado-r43/RevC1Counter/` (deleted at seat end);
reproduction scripts and logs are copied to `evidence/` in this seat dir. Tooling installed: none (python3/bwrap/git already present; no pacman).

Severity scale: MEDIUM = can flip the gate's verdict or crash it for a contract-conforming tool; LOW = doc/code sentence mismatch or unpinned domain, no verdict flip for the reference-class tool; INFO = observation/declared-residual sharpening.

---

## F1 — MEDIUM — docstring says "not UTF-8 JSON"; the code (and the pinned fixture) mean "whatever Python's json.loads accepts" (NaN/Infinity)

- Attacks: the model-vs-contract sentence "a clients input that is not UTF-8 JSON … is bad_json" (counter docstring :21-22; the same sentence is the contract, since the contract is the reference's docstring, `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` :22-23).
- Exact line: `quality/counters/c1-r42-geometry.py:268` — `doc = json.loads(clients_raw.decode("utf-8"))`. Python's `json.loads` accepts `NaN`, `Infinity`, `-Infinity` (non-RFC-8259). RFC 8259 JSON has no such literals, so under the docstring sentence they are "not UTF-8 JSON" → bad_json; under the code they parse and score as ordinary clients (float sizes → BADSIZE).
- Reproduction (evidence/tier1.log, hand case 1): input `[{"class":"a","size":[NaN,2],"floating":true},…,{"class":"a","size":[100,2],"floating":true}]` — counter model emits a full run (BADSIZE, BADSIZE, BADSIZE, AGREE, verdict OK); an independent model built from the docstring sentence alone (strict JSON) emits `SETUP bad_json`. Fixture `nan0` (:649-651 in FIXED via `score_nan0`) **pins the lenient reading**, so a tool implementing its own docstring strictly (rejecting NaN) fails nan0 → 36/37 → honest miss caused by a sentence the code does not mean.
- Reach: only the clients input; hyprctl never emits NaN, so practical impact is nil — but the builder implements from the docstring, and the docstring and the fixture disagree. The counter docstring's claim that the code is "the same sentence" as the reference docstring (:14) is false in exactly this dialect point.

## F2 — MEDIUM — the timeout breaker is global, order-dependent and load-sensitive: a clause-perfect tool that is merely slow scores fixtures=0/37

- Attacks: the "Cost bound" gate (docstring :65-66; code `TIMEOUTS` :84, checked at :207 and :432, incremented at :212 and :444).
- Mechanism: one global counter for the whole run; the first three 30 s fixture timeouts (in fixture order gen0, gen1, gen2, …) permanently skip every later fixture and selftest, each scored as a failure (`rc=None`).
- Reproduction (evidence/e6breaker.log): reference tool + a pure-Python burn (`for i in range(2*10**9)`) inserted in `run()` for every non-`--selftest` invocation — no new imports, clause g passes, selftest 73/73, b2 teeth 6/6 kills, b3 passes; then gen0/gen1/gen2 time out and the log ends `fixtures=0/37 tool=present verdict=TARGET_MISSED`, wall 92 s. 34 fixtures the tool would have passed were never run.
- Load sensitivity, measured: the frozen reference scores 37/37 in 10.5 s total (evidence/e5ref.log); its heaviest fixture `many0` (20000 clients × 300 rules ≈ 6M `re.fullmatch` calls) takes **6.0 s unloaded = 20 % of the 30 s cap**; bwrap+`python3 -I` startup ≈ 27 ms (tier2: 78 sandboxed runs in 2.1 s). This wave runs ~77 seats on one host; a 5× slowdown under contention trips many0, and a correct tool that recompiles regexes per client (no cache) can legitimately exceed 30 s. The verdict is then a function of host load, not of the tool's correctness — and the nonce does not control speed, so `--nonce` replay does not make it reproducible.
- Phase coupling: selftest-phase timeouts (60 s cap, :883-886) increment the same `TIMEOUTS` global, so three slow mutant-selftest copies (clause b2 runs six) erase the entire fixture phase. The docstring declares "a run that hits 3 timeouts … every remaining fixture and selftest fails" but not that selftest/mutant timeouts share the fixture budget.

## F2b — MEDIUM-LOW — clause b2's verdict is a nonce coin-flip for a borderline-teeth selftest (sampling determinism)

- Attacks: `teeth()` :904-931 — 6 sites sampled by nonce from the tool's comparison sites; pass iff the forced site dies and ≥3 of the other 5 die.
- Quantification (evidence/probes.log): the frozen reference has **35 sites, 4 of them in the summary function** (`report`). For a hypothetical tool whose selftest kills exactly K of its 35 sites (summary sites assumed killed), P(b2 pass) by hypergeometric sampling: K=26 → 0.47, K=27 → 0.55, K=28 → 0.64, K=30 → 0.87. So a tool in the 26-30 band flips TARGET_MET/TARGET_MISSED between runs, because the counting command uses a fresh nonce per run (registration: "fresh nonce per run, replayable with `--nonce`").
- Not a false-MET path for the reference-class tool (its selftest kills all sampled sites — receipt `receipts/ctl-c1.txt` and my e5ref run), but the gate is not run-to-run stable at the boundary it is designed to police.

## F3 — MEDIUM — a working tool whose source `ast.parse` rejects crashes the counter (traceback, no final P line)

- Attacks: gate robustness — `imports_ok` :791-793 (catches SyntaxError → clause g=0) vs `function_sites` :847 and `neutrality` :938 (`ast.parse(src)` uncaught; `main()` catches only `Setup`, :1009).
- Reproduction (evidence/e7bom.log): reference source with a UTF-8 BOM prepended (`\xef\xbb\xbf`). CPython executes it fine (selftest **73/73**, clause b passes), clause g=0 (SyntaxError caught), then `teeth()` → `function_sites` → `ast.parse` raises `SyntaxError: invalid non-printable character U+FEFF` → traceback, rc=1, **no `PRED-C1-r42: fixtures=…` final line**.
- Consequence: not a false MET (the kill rule routes any non-MET to an honest stop), but the counter violates its own output contract (final line) and reports a crash instead of a scored miss; a driver grepping the final line gets nothing. Same family: any source CPython runs but `ast.parse(decoded_str)` rejects (BOM; exotic `coding:` cookies).

## F4 — LOW-MEDIUM — fixture vacuity: no fixture ever passes ≥4 rules files, so a tool supporting at most 3 files scores 37/37

- Attacks: the CLI contract "`--rules V` one or more times" (docstring :16-17, unbounded) vs the fixture domain.
- Exact lines: `gen_texts` :367 `n_files = rng.randrange(1, 4)` (1-3 files); `score_multi0` :536-540 (3 texts); `score_order0` :709-717 (3 texts); every other fixture passes exactly 1 text. I checked all 37 case builders — none ever passes 4.
- Reproduction (evidence/tier2.log, cases `files4`/`files5`): the frozen reference handles 4 and 5 rules files correctly (output matches the model) — the capability is inside the contract domain, the fixtures never ask for it. A tool containing `rules = rules[:3]` (or a 3-iteration loop) is indistinguishable from a correct one on all 37 fixtures.
- Cross-file semantics themselves ARE pinned at 3 files (multi0/order0 exercise last-matching-wins across files), so the gap is only the count bound.

## F5 — LOW — unpinned ordering/size domains (fixture gaps; the docstring sentences are never exercised)

- (a) **bad_json clients × unreadable rules**: the docstring's check order (:22-24: "usage, then the clients input …, then the rules files") is pinned for too_large-beats-unreadable-rules (`score_toolarge0` :599-611 third form) but NOT for bad_json-clients-beats-unreadable-rules — `score_badjson0` :626-643 always pairs invalid clients with a readable `r.conf`, and `unreadable0`/`toolarge0` always use valid clients. A tool that stats the rules files before parsing clients passes all 37 fixtures. (Related: `model_out` :265-268 can only express bad_json for the clients input — too_large/unreadable clients exist solely in the direct-judge fixtures, so the model itself never exercises that ordering.)
- (b) **usage × unreadable**: no fixture pairs a usage-violating argv with an unreadable path (`score_usage0` :549-567 uses existing files; `score_unreadable0` :569-583 uses valid argv); "usage, then the clients input" is unpinned for that combination.
- (c) **stdin is never larger than 1048577 bytes**: `score_stdinbig0` :515-521 is exactly at the cap (`b"[]" + 1048576 spaces`); no fixture feeds more. A tool that reads stdin to EOF and too_larges on the full length is indistinguishable from one that stops at 1048577; a tool that reads unbounded and never checks the size at all also passes (nothing larger is ever sent). The "at most 1048577 bytes" sentence (:21) is only pinned at the exact boundary.

## F6 — LOW — clause g's code is not the docstring's sentence, in both directions (probes in evidence/probes.log)

- Stricter than "the source calls none of …" (:78-80): `imports_ok` :808-816 rejects **any** `ast.Name` occurrence of exec/eval/compile/__import__/getattr/setattr/delattr/vars/globals/locals/breakpoint/__file__ — a local variable named `compile` (`compile = x`) → g fails; a bare expression statement `eval` (never called) → g fails; `vars = {}` → g fails. A docstring-conforming tool that merely names one fails clause g.
- Stricter: a tool with **zero imports** fails (`bool(mods)` :834) — the docstring does not require any import; `os.spawn*`/`posix_spawn` are rejected though the docstring lists only "os.system, os.popen, os.exec*".
- Looser than "never names `sys.argv[0]`" (:81): only the direct Subscript form is banned (:824-829); `a = sys.argv; a[0]` passes the probe (g=True) — the tool learns its own path, though inside the sandbox that path is a scratch copy, so no lane exposure results.
- Declared residual covers this ("clause g is a heuristic over names", :87-88); these are the concrete instances, with direction.

## F7 — LOW — dead guard: `STDLIB_DENY` is enforced entirely by `STDLIB_ALLOW`

- Exact line: :834 `return bool(mods) and mods <= STDLIB_ALLOW and not (mods & STDLIB_DENY)` — `STDLIB_ALLOW ∩ STDLIB_DENY = ∅` (probe `DEAD-GUARD allow∩deny= set()`), so `not (mods & STDLIB_DENY)` is implied by the allow-list conjunct and can never fire independently. Harmless; noted because the task asked for dead guards.

## F8 — LOW — many0's generator seed ignores REV, contradicting the docstring's fixture formula

- Exact line: :764 `rng = rng_for("many", nonce, "many", 0)` — the first parameter of `rng_for(rev, nonce, tag, i)` (:344-348) is the REV slot; the docstring says fixtures key on `sha256(REV:NONCE:tag:i)` (:10). many0's 20000 clients and 300 rules are therefore identical across revisions for the same nonce. No scoring consequence (the nonce is fresh per run and gen0-9 do key on REV), but the sentence and the code differ.

## F9 — LOW — the selftest phase runs without RLIMIT_NPROC, and clause g does not ban `os.fork`

- Exact lines: `run_sandboxed` :200-205 (`nproc=False` default; `lead` empty), `selftest_result` :883-886 (no `nproc` argument → no prlimit), vs `execute` :435 (fixtures always get `--nproc=1:1`). Clause g bans `os.exec*`/`spawn*`/`system`/`popen` and the `subprocess` import (:117-121, :808-816) but not `os.fork`. A selftest may therefore fork inside the sandbox (pid-ns-contained, killed at the 60 s timeout). The docstring scopes nproc to "fixture runs" (:9) accurately — this is a hardening note, not a doc/code mismatch.

## F10 — LOW — `run_piped`'s comment describes a stub that does not exist; file-mode stdin blocks until the timeout

- Exact lines: :188-190 — the comment says "so a child that does not redirect its own children's stdin is visible to the stub", but this counter has no stub; the real effect is that the pipe's write end is held by the parent for the whole run, so a child that reads stdin in file mode blocks with no EOF until the 30 s timeout (burning breaker budget, cf. F2). Correct tools never read stdin in file mode; noted as a stale sentence plus a breaker-coupling path for buggy tools.

## F11 — INFO — the REGEX alphabet admits catastrophic-backtracking patterns the counter can never test (it would hang on its own model)

- The alphabet (:105-106, :88-89 residual) allows e.g. `(a|a)*b` — every character permitted, no banned substring, compiles under `re`. My first tier-1 sample draw hit exactly such a case (`re.fullmatch("(a|a)*b", "a"*300)`) and hung until killed; the counter's own `model_out` calls `re.fullmatch` on fixture regexes, so no fixture can ever cover that domain without the counter DoS-ing itself. A contract-compliant tool may therefore hang on a real host config containing such a rule and the counter cannot score it. Sharpens the declared residual ("the REGEX alphabet is restricted so the two agree on it"): they agree on match RESULTS on this alphabet, not on complexity.

## F12 — INFO/PASS — gate integrity and model≡reference (positive results)

- **Freeze integrity**: worktree counter == 809dc2c blob == a35cfdf blob (sha256 `ed78d693…` all three); BASE 62dd798 lacks `tools/mado-geometry.py` (`git show` fails; clause a's precondition holds).
- **Reference re-run at the round-43 base** (evidence/e5ref.log): `fixtures=37/37 tool=present verdict=TARGET_MET`, clauses `a:1 b:1 b2:1 b3:1 g:1`, exit 0, wall 10.5 s, nonce 0123456789abcdef — consistent with `receipts/ctl-c1.txt` :50 ("reference met: 1").
- **Independent docstring model vs counter model**: 314 cases (16 handcrafted edges + 298 sampled from a generator wider than the counter's pools — regexes outside the alphabet, control-char classes, lone surrogates, mapped matrix, huge ints, BOM, dupkeys, CRLF, NBSP): **zero divergences** except the two strict-JSON NaN/Infinity cases (F1).
- **Frozen reference in the counter's own sandbox vs model**: 78 cases (NaN, BOM clients, dupkeys, control classes, mapped matrix, CRLF/NBSP rules, 4- and 5-file rules, boundary sizes 99999/100000, 200/201-char regexes, usage forms, /dev/null, missing/dir rules, stdin at both boundaries): **zero real mismatches** (the single flagged case was my harness expecting the model's verdict where the contract's stdin cap correctly yields `too_large` — see F5(c); the tool was right).

## Negative results (attacked, not found)

- **Not vacuous for first-file-only / stdin-only / first-client-only tools**: multi0 and order0 place decisive rules in the 2nd/3rd file (cross-file last-matching-wins pinned); gen0-9 alternate stdin/file by parity (`via_stdin=bool(i % 2)`, :493) and draw 0-14 clients with mixed verdicts; empty0 pins the empty-clients and `[{}]` states, including rc 4 with one client present (empty0 case 2).
- **No pool-overfit path**: a tool implementing the model only for `CLASS_POOL`/`RX_POOL` members fails regex0/ctlclass0/unicode0/size0/space0/float0 (all use non-pool values); the gen lattice (nonce-seeded, astronomically large) cannot be content-matched without implementing the model.
- **Fixed-fixture memorization is unprofitable**: fixture directory names are `sha256(NONCE:name)` with the nonce never given to the tool (env cleared, :166-168), so content-matching the 27 public fixed fixtures still fails the 10 gen draws.
- **Sandbox does not expose the counter or the lane**: `sandbox_cmd` :156-169 binds only /usr (ro), the fixture dir and the tool dir (ro), fresh /proc and /dev, tmpfs /tmp, `--clearenv`, HOME=/nonexistent; the counter source and lane are not reachable from the tool (verified by reading the bind set; nothing in the lane is written — the counter writes only under `C1R42_TMP`/tmp).
- **judge() is byte-exact on stdout** (:449-464) and enforces empty stderr exactly on rc 0/1/3/4 — matches the docstring's output contract; rc=None (timeout/skip) always fails the fixture.
- **teeth counting matches its docstring**: `killed >= KILL_NEED and forced_dead` (:931) ⇔ forced dies and ≥3 of the other 5 die (KILL_NEED=4 includes the forced kill); `mutate_source` returning None is effectively unreachable (sites and mutation use the same walk/keys).
- **Fixture names are unique per run** (each `prepare(tmp, name)` name used once); my harness's `FileExistsError` on a repeated name was a harness artifact, not a counter path.

## Residual risk and verification gaps

- F2/F2b mean the gate's verdict is environment-dependent (host load) and nonce-dependent (b2 sampling) at the boundaries; a TARGET_MET at the data tip is strong evidence, a TARGET_MISSED is not proof of incorrectness without a per-fixture `ok=1` inspection (the counter prints per-fixture lines — the L1 should read them, not just the final line, when a miss is reported).
- F1/F4/F5 are docstring-vs-fixture traps for the builder seat: implement the fixtures' pinned behavior (lenient JSON, unbounded files, cap-checked stdin), not the most literal docstring reading.
- Not verified (out of my seat's scope): the controls runner's 46-control tally, C2, the reference's Hyprland-fidelity (RE2 semantics beyond the alphabet), and any compositor behavior.
