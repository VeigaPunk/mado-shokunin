# MutC1CounterGates - C1 counter mutation matrix (round 43, w1)

Counter under mutation: `quality/counters/c1-r42-geometry.py` (frozen; sha256
`ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99` before and after - the
frozen file was never edited; every mutant is a one-edit copy in scratch, deleted after the run).
Reference: `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (sha256 `e3c2e471...a99`).
Controls regenerated into scratch by the frozen runner's own generation logic
(`.ufo/waves/round-42/ctl/run-c1-controls.py`, sha256 `4ac11b55...0af5`); nonce fixed at
`42aa42aa42aa42aa`, rev `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f` (the round-43 base), so
pristine rows reproduce `.ufo/waves/round-43/receipts/ctl-c1.txt` exactly.

81 mutants (one edit each: 77 built in the first batch, of which one - deny-ctypes - turned out
to be a whitespace no-op and is excluded, leaving 76; plus 3 pattern-collision rebuilds -
call-eval, call-import, streq-builtins - and 2 late additions, deny-ctypes-real and allow-open).
Each mutant scored on REF + 8 bad controls
(M01-fifo-block, M04-toolarge-ge, M27-nomatch-rc, K1-zero-test-selftest, K3-exec-model,
K4-child-interpreter, K5-getattr, D1-constant), 749 counter runs total (704 + 27 + 18).

## Pristine anchors (counter-orig.py, this seat, same nonce/rev)

| target | verdict | rc | clauses | failed fixtures |
|---|---|---|---|---|
| REF | MET | 0 | a:1 b:1 b2:1 b3:1 g:1 | - |
| BASE-absent | MISSED | 1 | a:0 b:0 b2:0 b3:0 g:0 | - |
| M01-fifo-block | MISSED | 1 | a:1 b:1 b2:1 b3:1 g:1 | fifo0 |
| M04-toolarge-ge | MISSED | 1 | a:1 b:1 b2:1 b3:1 g:1 | boundary0 |
| M27-nomatch-rc | MISSED | 1 | a:1 b:0 b2:0 b3:0 g:1 | gen1, gen3, gen5, gen6, gen7, stdinok0 |
| K1-zero-test-selftest | MISSED | 1 | a:1 b:1 b2:0 b3:1 g:1 | - |
| K3-exec-model | MISSED | 1 | a:1 b:1 b2:1 b3:1 g:0 | - |
| K4-child-interpreter | MISSED | 1 | a:1 b:1 b2:1 b3:1 g:0 | - |
| K5-getattr | MISSED | 1 | a:1 b:1 b2:1 b3:1 g:0 | - |
| D1-constant | MISSED | 1 | a:1 b:0 b2:0 b3:0 g:1 | gen0, gen1, gen2, gen3, gen4, gen5 |

All ten rows match the frozen receipt `receipts/ctl-c1.txt` (REF met=1; every control met=0).

## Matrix

| mutant | edit (counter copy) | reference verdict | worst control verdict | survivor? |
|---|---|---|---|---|
| allow-open | `mods <= STDLIB_ALLOW and not (mods & STDLIB_DENY)` -> `True` | MET | MET | NO - gate broken |
| bool-mods | `bool(mods)` -> `True` | MET | MISSED | YES - survivor |
| call-compile | `"compile", "__import__"}` -> `"__import__"}` | MET | MISSED | YES - survivor |
| call-eval | `CALL_DENY = {"exec", "eval",` -> `CALL_DENY = {"exec",` | MET | MISSED | YES - survivor |
| call-exec | `{"exec", "eval", "compile", "__import__"}` -> `{"eval", "compile", "__import__"}` | MET | MET | NO - gate broken |
| call-import | `"__import__"}` -> `}` | MET | MISSED | YES - survivor |
| cap-drop | `"--cap-drop", "ALL", ` -> `(deleted)` | MET | MISSED | YES - survivor |
| clause-a-1 | `cl = {"a": int(present),` -> `cl = {"a": 1,` | MET | MISSED | YES - equivalent |
| clearenv | `"--clearenv", ` -> `(deleted)` | MET | MISSED | YES - survivor |
| deny-ctypes-real | `"ssl", "ctypes",` -> `"ssl",` | MET | MISSED | YES - survivor |
| deny-http | `"http", "requests"` -> `"requests"` | MET | MISSED | YES - survivor |
| deny-importlib | `"importlib", "pty"` -> `"pty"` | MET | MISSED | YES - survivor |
| deny-pty | `"pty", "subprocess"` -> `"subprocess"` | MET | MISSED | YES - survivor |
| deny-requests | `"requests", "ssl"` -> `"ssl"` | MET | MISSED | YES - survivor |
| deny-socket | `{"socket", "urllib"` -> `{"urllib"` | MET | MISSED | YES - survivor |
| deny-ssl | `"ssl", "ctypes"` -> `"ctypes"` | MET | MISSED | YES - survivor |
| deny-subprocess | `"pty", "subprocess"}` -> `"pty"}` | MET | MISSED | YES - survivor |
| deny-urllib | `"urllib", "http"` -> `"http"` | MET | MISSED | YES - survivor |
| exit-always-0 | `return 0 if met else 1` -> `return 0` | MET | MISSED | SPLIT |
| home-env | `"/nonexistent"` -> `"/home"` | MET | MISSED | YES - survivor |
| judge-rc | `if rc != want_rc:` -> `if False:` | MET | MISSED | YES - survivor |
| judge-stderr | `if want_rc in (0, 1, 3, 4) and err:` -> `if False and err:` | MET | MISSED | YES - survivor |
| kill-need | `KILL_NEED = 4` -> `KILL_NEED = 1` | MET | MISSED | YES - survivor |
| min-selftest | `MIN_SELFTEST = 50` -> `MIN_SELFTEST = 1` | MET | MISSED | YES - survivor |
| min-sites | `MIN_SITES = 12` -> `MIN_SITES = 1` | MET | MISSED | YES - survivor |
| model-client-labels | `floating=%s size=%s ` -> `size=%s floating=%s ` | MISSED | MISSED | n/a - over-strict |
| model-differ-truthy | `elif t["DIFFER"]:` -> `elif t["DIFFER"] >= 1:` | MET | MISSED | YES - equivalent |
| model-nosize | `if nsize == 0:` -> `if nsize < 0:` | MISSED | MISSED | n/a - over-strict |
| model-rc-differ | `verdict, rc = "DIFFER", 1` -> `verdict, rc = "DIFFER", 2` | MISSED | MISSED | n/a - over-strict |
| model-summary-swap | `t["AGREE"], t["DIFFER"],` -> `t["DIFFER"], t["AGREE"],` | MISSED | MISSED | n/a - over-strict |
| n-mut | `N_MUT = 6` -> `N_MUT = 2` | MISSED | MISSED | n/a - over-strict |
| name-breakpoint | `"breakpoint", "__file__"}` -> `"__file__"}` | MET | MISSED | YES - survivor |
| name-delattr | `"delattr", "vars"` -> `"vars"` | MET | MISSED | YES - survivor |
| name-file | `"breakpoint", "__file__"}` -> `"breakpoint"}` | MET | MISSED | YES - survivor |
| name-getattr | `{"getattr", "setattr"` -> `{"setattr"` | MET | MET | NO - gate broken |
| name-globals | `"globals", "locals"` -> `"locals"` | MET | MISSED | YES - survivor |
| name-locals | `"locals",
             "breakpoint", "__file__"}` -> `"breakpoint", "__file__"}` | MET | MISSED | YES - survivor |
| name-setattr | `"getattr", "setattr", "delattr"` -> `"getattr", "delattr"` | MET | MISSED | YES - survivor |
| name-vars | `"vars", "globals"` -> `"globals"` | MET | MISSED | YES - survivor |
| neutral-minselftest | `good = rc == 0 and has and k == n and n >= MIN_SELFTEST` -> `good = rc == 0 and has and k == n` | MET | MISSED | YES - survivor |
| neutral-or | `ok &= good` -> `ok |= good` | MET | MISSED | YES - survivor |
| nonce-fixed | `nonce = args.nonce or secrets.token_hex(8)` -> `nonce = args.nonce or "42aa42aa42aa42aa"` | MET | MISSED | YES - survivor |
| nproc-lead | `["/usr/bin/prlimit", "--nproc=1:1"] if nproc` -> `[] if nproc` | MET | MISSED | YES - survivor |
| os-execl | `"execl", "execle"` -> `"execle"` | MET | MISSED | YES - survivor |
| os-execle | `"execle",
           "execlp"` -> `"execlp"` | MET | MISSED | YES - survivor |
| os-execlp | `"execlp", "execvpe"` -> `"execvpe"` | MET | MISSED | YES - survivor |
| os-execlpe | `"execlpe", "spawnl"` -> `"spawnl"` | MET | MISSED | YES - survivor |
| os-execv | `"execv", "execve"` -> `"execve"` | MET | MISSED | YES - survivor |
| os-execve | `"execve", "execvp"` -> `"execvp"` | MET | MISSED | YES - survivor |
| os-execvp | `"execvp", "execl"` -> `"execl"` | MET | MISSED | YES - survivor |
| os-execvpe | `"execvpe", "execlpe"` -> `"execlpe"` | MET | MISSED | YES - survivor |
| os-popen | `"system", "popen", "execv"` -> `"system", "execv"` | MET | MISSED | YES - survivor |
| os-posix-spawn | `"spawnv", "posix_spawn"}` -> `"spawnv"}` | MET | MISSED | YES - survivor |
| os-spawnl | `"spawnl", "spawnv"` -> `"spawnv"` | MET | MISSED | YES - survivor |
| os-spawnv | `"spawnv", "posix_spawn"` -> `"posix_spawn"` | MET | MISSED | YES - survivor |
| os-system | `{"system", "popen"` -> `{"popen"` | MET | MISSED | YES - survivor |
| proc-flag | `"--proc", "/proc", ` -> `(deleted)` | MET | MISSED | YES - survivor |
| rng-nonce | `("%s:%s:%s:%d" % (rev, nonce, tag, i))` -> `("%s:%s:%d" % (rev, tag, i))` | MET | MISSED | YES - survivor |
| stdlib-allow-bypass | `and not (mods & STDLIB_DENY)` -> `(deleted)` | MET | MISSED | YES - survivor |
| str-c1r42 | `"c1-r42", "quality/counters"` -> `"quality/counters"` | MET | MISSED | YES - survivor |
| str-proc | `("/proc", "c1-r42"` -> `("c1-r42"` | MET | MISSED | YES - survivor |
| str-qc | `"quality/counters")` -> `)` | MET | MISSED | YES - survivor |
| streq-builtins | `"popen",                "builtins", "__builtins__"` -> `"popen",                "__builtins__"` | MET | MISSED | YES - survivor |
| streq-compile | `"eval", "compile", "__import__", "system"` -> `"eval", "__import__", "system"` | MET | MISSED | YES - survivor |
| streq-dunder-builtins | `"__builtins__", "__file__"}` -> `"__file__"}` | MET | MISSED | YES - survivor |
| streq-eval | `"exec", "eval", "compile", "__import__", "system"` -> `"exec", "compile", "__import__", "system"` | MET | MISSED | YES - survivor |
| streq-exec | `STR_EQ_DENY = {"exec", "eval"` -> `STR_EQ_DENY = {"eval"` | MET | MISSED | YES - survivor |
| streq-file | `"__builtins__", "__file__"}` -> `"__builtins__"}` | MET | MISSED | YES - survivor |
| streq-import | `"compile", "__import__", "system"` -> `"compile", "system"` | MET | MISSED | YES - survivor |
| streq-popen | `"system", "popen",
               "builtins"` -> `"system",
               "builtins"` | MET | MISSED | YES - survivor |
| streq-system | `"__import__", "system", "popen"` -> `"__import__", "popen"` | MET | MISSED | YES - survivor |
| teeth-dead-def | `dead = rc != 0 or not has or k != n_` -> `dead = rc != 0` | MET | MISSED | YES - survivor |
| teeth-forced-site | `forced = rng.choice(summ)` -> `forced = rng.choice(rest + summ)` | MISSED | MISSED | n/a - over-strict |
| teeth-no-summ | `if not summ:` -> `if False:` | MET | MISSED | YES - equivalent |
| teeth-or | `return killed >= KILL_NEED and forced_dead` -> `return killed >= KILL_NEED or forced_dead` | MET | MISSED | YES - survivor |
| teeth-rng | `("mut:" + nonce)` -> `"mut:"` | MET | MISSED | YES - survivor |
| timeout-breaker | `TIMEOUTS[0] += 1` -> `TIMEOUTS[0] += 0` | MET | MISSED | YES - survivor |
| total-const | `TOTAL = 37` -> `TOTAL = 36` | CRASH(rc=1) | MISSED | n/a - over-strict |
| total-ge | `and passed == TOTAL` -> `and passed >= TOTAL - 1` | MET | MET | NO - gate broken |
| unshare-all | `"--unshare-all", ` -> `(deleted)` | MET | MISSED | YES - survivor |
| verdict-string | `"TARGET_MET" if met else "TARGET_MISSED"` -> `"TARGET_MET"` | MET | MET | NO - gate broken |

## Per-mutant classification

- **allow-open**: missed defect: K4-child-interpreter now scores MET (rc=0, clauses=a:1 b:1 b2:1 b3:1 g:1)
- **bool-mods**: missing control: an import-free tool (zero top-level imports) that is otherwise contract-perfect
- **call-compile**: missing control: a tool calling compile() (K3 probes only exec)
- **call-eval**: missing control: a tool calling eval() (K3 probes only exec)
- **call-exec**: missed defect: K3-exec-model now scores MET (rc=0, clauses=a:1 b:1 b2:1 b3:1 g:1)
- **call-import**: missing control: a tool calling __import__() (K3 probes only exec)
- **cap-drop**: missing control: a tool exploiting the retained namespace capabilities (e.g. remounting a read-only bind rw)
- **clause-a-1**: EQUIVALENT (verdict-level, proof): met requires passed == TOTAL (37), so an absent tool still scores MISSED with passed=0 regardless of clause a; for a present tool a was already 1. Only the printed clause value on the absent path differs (diagnostic, not verdict)
- **clearenv**: missing control: a cheat reading inherited counter environment variables to detect being scored
- **deny-ctypes-real**: missing control: a tool importing ctypes and otherwise contract-perfect
- **deny-http**: missing control: a tool importing http.* and otherwise contract-perfect
- **deny-importlib**: missing control: a tool importing importlib and otherwise contract-perfect
- **deny-pty**: missing control: a tool importing pty and otherwise contract-perfect
- **deny-requests**: missing control: a tool importing requests and otherwise contract-perfect
- **deny-socket**: missing control: a tool importing socket and otherwise contract-perfect
- **deny-ssl**: missing control: (unclassified)
- **deny-subprocess**: missing control: none needed for K4 - the allow-side gate (mods <= STDLIB_ALLOW) independently rejects K4; the deny entry is redundant with it (defense in depth, unprobed in isolation)
- **deny-urllib**: missing control: a tool importing urllib and otherwise contract-perfect
- **exit-always-0**: line channel honest (all controls MISSED), exit channel dead (every control exits rc=0); the frozen runner ignores the counter's exit code, so this mutant passes CTL_C1
- **home-env**: missing control: a tool branching on HOME (the declared sandbox tell is removed)
- **judge-rc**: missing control: a tool with a wrong exit code whose selftest passes (selftest blind to rc); M27 cannot isolate this gate because its own selftest also fails (b:0)
- **judge-stderr**: missing control: a tool writing to stderr on rc 0/1/3/4 with byte-correct stdout/rc
- **kill-need**: missing control: a tool whose selftest kills only 1-3 of the 6 sampled mutants including the forced site
- **min-selftest**: missing control: a tool with selftest k==n and 1<=n<50
- **min-sites**: missing control: a tool with 1-11 comparison sites and otherwise full teeth
- **model-client-labels**: counter rejects the reference (MISSED); model/teeth drift is caught by the byte-exact judge on the reference
- **model-differ-truthy**: EQUIVALENT (proof): t["DIFFER"] is a non-negative int, truthy iff >= 1; branch condition identical for every input
- **model-nosize**: counter rejects the reference (MISSED); model/teeth drift is caught by the byte-exact judge on the reference
- **model-rc-differ**: counter rejects the reference (MISSED); model/teeth drift is caught by the byte-exact judge on the reference
- **model-summary-swap**: counter rejects the reference (MISSED); model/teeth drift is caught by the byte-exact judge on the reference
- **n-mut**: counter rejects the reference (MISSED); N_MUT=2 < KILL_NEED=4 makes teeth impossible - fails closed
- **name-breakpoint**: missing control: a tool calling breakpoint() (K5 probes only getattr)
- **name-delattr**: missing control: a tool calling delattr()
- **name-file**: missing control: a tool naming __file__
- **name-getattr**: missed defect: K5-getattr now scores MET (rc=0, clauses=a:1 b:1 b2:1 b3:1 g:1)
- **name-globals**: missing control: a tool calling globals()
- **name-locals**: missing control: a tool calling locals()
- **name-setattr**: missing control: a tool calling setattr()
- **name-vars**: missing control: a tool calling vars()
- **neutral-minselftest**: missing control: a tool whose b3 variants pass with a weak-count selftest (n<50 accepted as neutral)
- **neutral-or**: missing control: a tool whose selftest is non-neutral (one b3 variant fails) but otherwise perfect - no b3-only control exists
- **nonce-fixed**: missing control: a cheat hardcoding answers for the predictable default nonce
- **nproc-lead**: missing control: a tool forking children at fixture time (RLIMIT_NPROC=1 removed; spawn paths are otherwise deny-listed)
- **os-execl**: missing control: a tool calling os.execl (no control probes os.*)
- **os-execle**: missing control: a tool calling os.execle (no control probes os.*)
- **os-execlp**: missing control: a tool calling os.execlp (no control probes os.*)
- **os-execlpe**: missing control: a tool calling os.execlpe (no control probes os.*)
- **os-execv**: missing control: a tool calling os.execv (no control probes os.*)
- **os-execve**: missing control: a tool calling os.execve (no control probes os.*)
- **os-execvp**: missing control: a tool calling os.execvp (no control probes os.*)
- **os-execvpe**: missing control: a tool calling os.execvpe (no control probes os.*)
- **os-popen**: missing control: a tool calling os.popen (no control probes os.*)
- **os-posix-spawn**: missing control: a tool calling os.posix_spawn (no control probes os.*)
- **os-spawnl**: missing control: a tool calling os.spawnl (no control probes os.*)
- **os-spawnv**: missing control: a tool calling os.spawnv (no control probes os.*)
- **os-system**: missing control: a tool calling os.system (no control probes os.*)
- **proc-flag**: missing control: a tool reading /proc inside the sandbox (no fresh proc is mounted)
- **rng-nonce**: missing control: a tool overfit to the rev-derived fixture stream (fixtures become nonce-independent)
- **stdlib-allow-bypass**: missing control: none needed for K4 - same redundancy as deny-subprocess: the allow-side gate independently rejects K4
- **str-c1r42**: missing control: a tool containing the string c1-r42 (counter fingerprint)
- **str-proc**: missing control: a tool containing the string /proc (sandbox detection)
- **str-qc**: missing control: a tool containing the string quality/counters (counter-path probe)
- **streq-builtins**: missing control: (unclassified)
- **streq-compile**: missing control: a tool with a string constant equal to compile (no control probes string constants)
- **streq-dunder-builtins**: missing control: a tool with a string constant equal to __builtins__
- **streq-eval**: missing control: a tool with a string constant equal to eval
- **streq-exec**: missing control: a tool with a string constant equal to exec
- **streq-file**: missing control: a tool with a string constant equal to __file__
- **streq-import**: missing control: a tool with a string constant equal to __import__
- **streq-popen**: missing control: a tool with a string constant equal to popen
- **streq-system**: missing control: a tool with a string constant equal to system
- **teeth-dead-def**: missing control: a tool whose flipped-comparison copies exit 0 with a wrong-count or missing summary (the k!=n / no-summary half of the kill definition is unprobed)
- **teeth-forced-site**: counter rejects the reference (MISSED); model/teeth drift is caught by the byte-exact judge on the reference
- **teeth-no-summ**: EQUIVALENT (verdict-level, proof): with a summary site present the path is untouched; without one, pristine cleanly rejects (b2:0) and the mutant crashes (IndexError, exit 1) - a bad tool is never admitted; only diagnostics degrade
- **teeth-or**: missing control: a tool with >=4 killed sampled mutants but a surviving forced site (the forced-site rule is unprobed in isolation)
- **teeth-rng**: missing control: a tool crafted to survive the nonce-independent forced-site choice
- **timeout-breaker**: missing control: a tool hanging on >=3 fixtures and correct elsewhere (the declared cost bound is unprobed)
- **total-const**: counter rejects the reference (CRASH(rc=1)); assert tripwire: TOTAL edit fails closed via crash
- **total-ge**: missed defect: M01-fifo-block,M04-toolarge-ge now scores MET (rc=0, clauses=a:1 b:1 b2:1 b3:1 g:1)
- **unshare-all**: missing control: a tool reaching host namespaces (pid/net/ipc shared, e.g. signalling host processes)
- **verdict-string**: missed defect: M01-fifo-block,M04-toolarge-ge,M27-nomatch-rc,K1-zero-test-selftest,K3-exec-model,K4-child-interpreter,K5-getattr,D1-constant now scores MET (rc=1, clauses=a:1 b:1 b2:1 b3:1 g:1)

## Control -> flipping-mutant index

- M01-fifo-block <- total-ge, verdict-string
- M04-toolarge-ge <- total-ge, verdict-string
- M27-nomatch-rc <- verdict-string
- K1-zero-test-selftest <- verdict-string
- K3-exec-model <- call-exec, verdict-string
- K4-child-interpreter <- allow-open, verdict-string
- K5-getattr <- name-getattr, verdict-string
- D1-constant <- verdict-string

## Totals

- equivalent: 3
- gate-broken: 5
- over-strict: 7
- split: 1
- survivor-missing-control: 65

## Findings

1. **Four one-edit counter mutants admit a bad control as full MET (rc=0, all clauses 1):**
   `call-exec` admits K3-exec-model (a tool holding `EXEC = exec`), `name-getattr` admits
   K5-getattr, `total-ge` (`passed == TOTAL` -> `>= TOTAL-1`) admits M01-fifo-block and
   M04-toolarge-ge (each failing exactly one fixture), and `allow-open` (dropping the
   `mods <= STDLIB_ALLOW` conjunct) admits K4-child-interpreter. Each named control's sole
   failing gate is exactly the mutated one - the gates are real and single points of failure
   for those defect classes.
2. **The two verdict channels are independent and each has a one-edit bypass.**
   `verdict-string` (always print TARGET_MET) makes all 8 controls print MET with rc=1 -
   the frozen runner, which parses only the printed line, would mark every control BAD
   (detected). `exit-always-0` keeps the line honest but exits 0 for every control - the
   frozen runner ignores the counter's exit code entirely, so CTL_C1 still says PASS while
   every bad control exits 0: a runner-side coverage gap (exit-code consumers are unprotected).
3. **The deny lists are defense in depth, not the load-bearing gate.** Removing any single
   STDLIB_DENY entry (including `subprocess`) still rejects K4 because
   `mods <= STDLIB_ALLOW` independently rejects it; conversely `allow-open` (allow side
   dropped) admits K4 outright. No control isolates a deny-list entry in the absence of the
   allow gate, and no control probes os.* calls, string constants, or non-getattr NAME_DENY
   entries - all those mutants survive.
4. **Model edits fail closed.** Every model/field-order/exit-code mutant (model-nosize,
   model-rc-differ, model-summary-swap, model-client-labels) is caught by the byte-exact
   judge on the reference itself (over-strict), as are `n-mut` (N_MUT < KILL_NEED makes
   teeth impossible) and `total-const` (the `assert len(cases) == TOTAL` tripwire crashes
   the counter). `teeth-forced-site` (forced site drawn from all functions) also rejects the
   reference at this nonce - the forced-site rule is load-bearing for the reference.
5. **65 survivors, each with a named missing control or an equivalence proof** (see
   classification above): the unprobed gate classes are b3-neutrality in isolation, weak-count
   selftests (1<=n<50), 1-11-site selftests, partial teeth (1-3 kills), the k!=n half of the
   kill definition, stderr cleanliness, exit-code-only defects with a passing selftest,
   nonce predictability/overfitting, sandbox flags (cap-drop, unshare, proc, nproc, HOME,
   clearenv), os.* calls, string-constant equality, and the timeout breaker.
6. **Three designed equivalences, proved:** `model-differ-truthy` (int truthiness),
   `clause-a-1` (verdict needs passed==TOTAL, so the absent-tool verdict is unchanged; only
   the printed clause value differs), `teeth-no-summ` (summary-less tools: clean reject vs
   crash - admission identical, diagnostics degrade).

## Restoration evidence

- Frozen counter sha256 before: `ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99`
- Frozen counter sha256 after (re-hash at close): see report; the file was only ever read.
- Scratch `/fast/scratch/hyaku/mado-r43/MutC1CounterGates` deleted after copying evidence
  (results jsonl, drivers, pristine log) into this seat dir.
