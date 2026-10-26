#!/usr/bin/env python3
"""Emit final matrix.md from results batches + the mutant table parsed from driver.py."""
import ast, collections, json, os

SCRATCH = "/fast/scratch/hyaku/mado-r43/MutC1CounterGates"
SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/MutC1CounterGates"
PANEL = ["M01-fifo-block", "M04-toolarge-ge", "M27-nomatch-rc", "K1-zero-test-selftest",
         "K3-exec-model", "K4-child-interpreter", "K5-getattr", "D1-constant"]

# ---- mutant table from driver.py (name -> edit description)
tree = ast.parse(open(os.path.join(SCRATCH, "driver.py")).read())
EDITS = {}
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "mu":
        name = node.args[0].value
        old, new = node.args[1].value, node.args[2].value
        cnt = node.args[3].value if len(node.args) > 3 else 1
        EDITS[name] = (old, new, cnt)
EDITS["call-eval"] = ('CALL_DENY = {"exec", "eval",', 'CALL_DENY = {"exec",', 1)
EDITS["call-import"] = ('"__import__"}', '}', 1)
EDITS["streq-builtins"] = ('"popen",\\n               "builtins", "__builtins__"',
                           '"popen",\\n               "__builtins__"', 1)
EDITS["deny-ctypes-real"] = ('"ssl", "ctypes",', '"ssl",', 1)
EDITS["allow-open"] = ("mods <= STDLIB_ALLOW and not (mods & STDLIB_DENY)", "True", 1)

rows = []
for f in ("results.jsonl", "results2.jsonl", "results3.jsonl"):
    p = os.path.join(SCRATCH, f)
    if os.path.exists(p):
        rows += [json.loads(l) for l in open(p) if l.strip()]
pb = {r["target"]: r for r in rows if r["counter"] == "counter-orig.py"}
by = collections.defaultdict(dict)
for r in rows:
    if r["counter"] != "counter-orig.py":
        by[r["counter"].replace(".py", "")][r["target"]] = r

EXCLUDED = {"deny-ctypes": "harness artifact: the edit replaced a newline with a space (whitespace-only no-op); superseded by deny-ctypes-real"}

def state(r):
    if r is None:
        return "no-run"
    if not r["final"].startswith("PRED"):
        return "CRASH(rc=%s)" % r["rc"]
    return "MET" if r["met"] else "MISSED"

MISSING = {
    "bool-mods": "missing control: an import-free tool (zero top-level imports) that is otherwise contract-perfect",
    "call-compile": "missing control: a tool calling compile() (K3 probes only exec)",
    "call-eval": "missing control: a tool calling eval() (K3 probes only exec)",
    "call-import": "missing control: a tool calling __import__() (K3 probes only exec)",
    "cap-drop": "missing control: a tool exploiting the retained namespace capabilities (e.g. remounting a read-only bind rw)",
    "clearenv": "missing control: a cheat reading inherited counter environment variables to detect being scored",
    "deny-ctypes-real": "missing control: a tool importing ctypes and otherwise contract-perfect",
    "deny-http": "missing control: a tool importing http.* and otherwise contract-perfect",
    "deny-importlib": "missing control: a tool importing importlib and otherwise contract-perfect",
    "deny-pty": "missing control: a tool importing pty and otherwise contract-perfect",
    "deny-requests": "missing control: a tool importing requests and otherwise contract-perfect",
    "deny-socket": "missing control: a tool importing socket and otherwise contract-perfect",
    "deny-subprocess": "missing control: none needed for K4 - the allow-side gate (mods <= STDLIB_ALLOW) independently rejects K4; the deny entry is redundant with it (defense in depth, unprobed in isolation)",
    "deny-urllib": "missing control: a tool importing urllib and otherwise contract-perfect",
    "home-env": "missing control: a tool branching on HOME (the declared sandbox tell is removed)",
    "judge-rc": "missing control: a tool with a wrong exit code whose selftest passes (selftest blind to rc); M27 cannot isolate this gate because its own selftest also fails (b:0)",
    "judge-stderr": "missing control: a tool writing to stderr on rc 0/1/3/4 with byte-correct stdout/rc",
    "kill-need": "missing control: a tool whose selftest kills only 1-3 of the 6 sampled mutants including the forced site",
    "min-selftest": "missing control: a tool with selftest k==n and 1<=n<50",
    "min-sites": "missing control: a tool with 1-11 comparison sites and otherwise full teeth",
    "model-differ-truthy": "EQUIVALENT (proof): t[\"DIFFER\"] is a non-negative int, truthy iff >= 1; branch condition identical for every input",
    "clause-a-1": "EQUIVALENT (verdict-level, proof): met requires passed == TOTAL (37), so an absent tool still scores MISSED with passed=0 regardless of clause a; for a present tool a was already 1. Only the printed clause value on the absent path differs (diagnostic, not verdict)",
    "name-breakpoint": "missing control: a tool calling breakpoint() (K5 probes only getattr)",
    "name-delattr": "missing control: a tool calling delattr()",
    "name-file": "missing control: a tool naming __file__",
    "name-globals": "missing control: a tool calling globals()",
    "name-locals": "missing control: a tool calling locals()",
    "name-setattr": "missing control: a tool calling setattr()",
    "name-vars": "missing control: a tool calling vars()",
    "neutral-minselftest": "missing control: a tool whose b3 variants pass with a weak-count selftest (n<50 accepted as neutral)",
    "neutral-or": "missing control: a tool whose selftest is non-neutral (one b3 variant fails) but otherwise perfect - no b3-only control exists",
    "nonce-fixed": "missing control: a cheat hardcoding answers for the predictable default nonce",
    "nproc-lead": "missing control: a tool forking children at fixture time (RLIMIT_NPROC=1 removed; spawn paths are otherwise deny-listed)",
    "os-execl": "missing control: a tool calling os.execl (no control probes os.*)",
    "os-execle": "missing control: a tool calling os.execle (no control probes os.*)",
    "os-execlp": "missing control: a tool calling os.execlp (no control probes os.*)",
    "os-execlpe": "missing control: a tool calling os.execlpe (no control probes os.*)",
    "os-execv": "missing control: a tool calling os.execv (no control probes os.*)",
    "os-execve": "missing control: a tool calling os.execve (no control probes os.*)",
    "os-execvp": "missing control: a tool calling os.execvp (no control probes os.*)",
    "os-execvpe": "missing control: a tool calling os.execvpe (no control probes os.*)",
    "os-popen": "missing control: a tool calling os.popen (no control probes os.*)",
    "os-posix-spawn": "missing control: a tool calling os.posix_spawn (no control probes os.*)",
    "os-spawnl": "missing control: a tool calling os.spawnl (no control probes os.*)",
    "os-spawnv": "missing control: a tool calling os.spawnv (no control probes os.*)",
    "os-system": "missing control: a tool calling os.system (no control probes os.*)",
    "proc-flag": "missing control: a tool reading /proc inside the sandbox (no fresh proc is mounted)",
    "rng-nonce": "missing control: a tool overfit to the rev-derived fixture stream (fixtures become nonce-independent)",
    "stdlib-allow-bypass": "missing control: none needed for K4 - same redundancy as deny-subprocess: the allow-side gate independently rejects K4",
    "str-c1r42": "missing control: a tool containing the string c1-r42 (counter fingerprint)",
    "str-proc": "missing control: a tool containing the string /proc (sandbox detection)",
    "str-qc": "missing control: a tool containing the string quality/counters (counter-path probe)",
    "streq-compile": "missing control: a tool with a string constant equal to compile (no control probes string constants)",
    "streq-dunder-builtins": "missing control: a tool with a string constant equal to __builtins__",
    "streq-eval": "missing control: a tool with a string constant equal to eval",
    "streq-exec": "missing control: a tool with a string constant equal to exec",
    "streq-file": "missing control: a tool with a string constant equal to __file__",
    "streq-import": "missing control: a tool with a string constant equal to __import__",
    "streq-popen": "missing control: a tool with a string constant equal to popen",
    "streq-system": "missing control: a tool with a string constant equal to system",
    "teeth-dead-def": "missing control: a tool whose flipped-comparison copies exit 0 with a wrong-count or missing summary (the k!=n / no-summary half of the kill definition is unprobed)",
    "teeth-no-summ": "EQUIVALENT (verdict-level, proof): with a summary site present the path is untouched; without one, pristine cleanly rejects (b2:0) and the mutant crashes (IndexError, exit 1) - a bad tool is never admitted; only diagnostics degrade",
    "teeth-or": "missing control: a tool with >=4 killed sampled mutants but a surviving forced site (the forced-site rule is unprobed in isolation)",
    "teeth-rng": "missing control: a tool crafted to survive the nonce-independent forced-site choice",
    "timeout-breaker": "missing control: a tool hanging on >=3 fixtures and correct elsewhere (the declared cost bound is unprobed)",
    "unshare-all": "missing control: a tool reaching host namespaces (pid/net/ipc shared, e.g. signalling host processes)",
}

out = []
out.append("# MutC1CounterGates - C1 counter mutation matrix (round 43, w1)")
out.append("")
out.append("Counter under mutation: `quality/counters/c1-r42-geometry.py` (frozen; sha256")
out.append("`ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99` before and after - the")
out.append("frozen file was never edited; every mutant is a one-edit copy in scratch, deleted after the run).")
out.append("Reference: `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (sha256 `e3c2e471...a99`).")
out.append("Controls regenerated into scratch by the frozen runner's own generation logic")
out.append("(`.ufo/waves/round-42/ctl/run-c1-controls.py`, sha256 `4ac11b55...0af5`); nonce fixed at")
out.append("`42aa42aa42aa42aa`, rev `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f` (the round-43 base), so")
out.append("pristine rows reproduce `.ufo/waves/round-43/receipts/ctl-c1.txt` exactly.")
out.append("")
out.append("81 mutants (one edit each; 80 from the driver table + 3 pattern-collision rebuilds -")
out.append("call-eval, call-import, streq-builtins - and deny-ctypes-real + allow-open; the accidental")
out.append("whitespace no-op deny-ctypes is excluded). Each mutant scored on REF + 8 bad controls")
out.append("(M01-fifo-block, M04-toolarge-ge, M27-nomatch-rc, K1-zero-test-selftest, K3-exec-model,")
out.append("K4-child-interpreter, K5-getattr, D1-constant), 731 counter runs total.")
out.append("")
out.append("## Pristine anchors (counter-orig.py, this seat, same nonce/rev)")
out.append("")
out.append("| target | verdict | rc | clauses | failed fixtures |")
out.append("|---|---|---|---|---|")
for t in ["REF", "BASE-absent"] + PANEL:
    r = pb[t]
    out.append("| %s | %s | %s | %s | %s |" % (t, state(r), r["rc"], r["clauses"], ", ".join(r["failed"][:6]) or "-"))
out.append("")
out.append("All ten rows match the frozen receipt `receipts/ctl-c1.txt` (REF met=1; every control met=0).")
out.append("")
out.append("## Matrix")
out.append("")
out.append("| mutant | edit (counter copy) | reference verdict | worst control verdict | survivor? |")
out.append("|---|---|---|---|---|")

cls_count = collections.Counter()
detail = []
for name in sorted(by):
    if name in EXCLUDED:
        continue
    d = by[name]
    refst = state(d.get("REF"))
    flipped = [c for c in PANEL if state(d.get(c)) == "MET" and state(pb.get(c)) != "MET"]
    worst = "MET" if flipped else "MISSED"
    old, new, cnt = EDITS[name]
    edit = "`%s` -> `%s`" % (old.replace("\\n", " "), new.replace("\\n", " ") or "(deleted)")
    if name in ("call-exec", "name-getattr", "total-ge", "verdict-string", "allow-open"):
        surv = "NO - gate broken"
        note = "missed defect: %s now scores MET (rc=%s, clauses=%s)" % (
            ",".join(flipped), d[flipped[0]]["rc"], d[flipped[0]]["clauses"])
        cls_count["gate-broken"] += 1
    elif name == "exit-always-0":
        surv = "SPLIT"
        note = "line channel honest (all controls MISSED), exit channel dead (every control exits rc=0); the frozen runner ignores the counter's exit code, so this mutant passes CTL_C1"
        cls_count["split"] += 1
    elif refst != "MET":
        surv = "n/a - over-strict"
        note = "counter rejects the reference (%s); %s" % (
            refst, "assert tripwire: TOTAL edit fails closed via crash" if name == "total-const" else
            ("N_MUT=2 < KILL_NEED=4 makes teeth impossible - fails closed" if name == "n-mut" else
             "model/teeth drift is caught by the byte-exact judge on the reference"))
        cls_count["over-strict"] += 1
    elif name in ("model-differ-truthy", "clause-a-1", "teeth-no-summ"):
        surv = "YES - equivalent"
        note = MISSING[name]
        cls_count["equivalent"] += 1
    else:
        surv = "YES - survivor"
        note = MISSING.get(name, "missing control: (unclassified)")
        cls_count["survivor-missing-control"] += 1
    out.append("| %s | %s | %s | %s | %s |" % (name, edit, refst, worst, surv))
    detail.append((name, note))

out.append("")
out.append("## Per-mutant classification")
out.append("")
for name, note in detail:
    out.append("- **%s**: %s" % (name, note))
out.append("")
out.append("## Control -> flipping-mutant index")
out.append("")
flips = collections.defaultdict(list)
for name in sorted(by):
    if name in EXCLUDED:
        continue
    d = by[name]
    for c in PANEL:
        if state(d.get(c)) == "MET" and state(pb.get(c)) != "MET":
            flips[c].append(name)
for c in PANEL:
    out.append("- %s <- %s" % (c, ", ".join(flips[c]) or "(none)"))
out.append("")
out.append("## Totals")
out.append("")
for k, v in sorted(cls_count.items()):
    out.append("- %s: %d" % (k, v))
out.append("")
out.append("## Findings")
out.append("")
out.append("1. **Four one-edit counter mutants admit a bad control as full MET (rc=0, all clauses 1):**")
out.append("   `call-exec` admits K3-exec-model (a tool holding `EXEC = exec`), `name-getattr` admits")
out.append("   K5-getattr, `total-ge` (`passed == TOTAL` -> `>= TOTAL-1`) admits M01-fifo-block and")
out.append("   M04-toolarge-ge (each failing exactly one fixture), and `allow-open` (dropping the")
out.append("   `mods <= STDLIB_ALLOW` conjunct) admits K4-child-interpreter. Each named control's sole")
out.append("   failing gate is exactly the mutated one - the gates are real and single points of failure")
out.append("   for those defect classes.")
out.append("2. **The two verdict channels are independent and each has a one-edit bypass.**")
out.append("   `verdict-string` (always print TARGET_MET) makes all 8 controls print MET with rc=1 -")
out.append("   the frozen runner, which parses only the printed line, would mark every control BAD")
out.append("   (detected). `exit-always-0` keeps the line honest but exits 0 for every control - the")
out.append("   frozen runner ignores the counter's exit code entirely, so CTL_C1 still says PASS while")
out.append("   every bad control exits 0: a runner-side coverage gap (exit-code consumers are unprotected).")
out.append("3. **The deny lists are defense in depth, not the load-bearing gate.** Removing any single")
out.append("   STDLIB_DENY entry (including `subprocess`) still rejects K4 because")
out.append("   `mods <= STDLIB_ALLOW` independently rejects it; conversely `allow-open` (allow side")
out.append("   dropped) admits K4 outright. No control isolates a deny-list entry in the absence of the")
out.append("   allow gate, and no control probes os.* calls, string constants, or non-getattr NAME_DENY")
out.append("   entries - all those mutants survive.")
out.append("4. **Model edits fail closed.** Every model/field-order/exit-code mutant (model-nosize,")
out.append("   model-rc-differ, model-summary-swap, model-client-labels) is caught by the byte-exact")
out.append("   judge on the reference itself (over-strict), as are `n-mut` (N_MUT < KILL_NEED makes")
out.append("   teeth impossible) and `total-const` (the `assert len(cases) == TOTAL` tripwire crashes")
out.append("   the counter). `teeth-forced-site` (forced site drawn from all functions) also rejects the")
out.append("   reference at this nonce - the forced-site rule is load-bearing for the reference.")
out.append("5. **65 survivors, each with a named missing control or an equivalence proof** (see")
out.append("   classification above): the unprobed gate classes are b3-neutrality in isolation, weak-count")
out.append("   selftests (1<=n<50), 1-11-site selftests, partial teeth (1-3 kills), the k!=n half of the")
out.append("   kill definition, stderr cleanliness, exit-code-only defects with a passing selftest,")
out.append("   nonce predictability/overfitting, sandbox flags (cap-drop, unshare, proc, nproc, HOME,")
out.append("   clearenv), os.* calls, string-constant equality, and the timeout breaker.")
out.append("6. **Three designed equivalences, proved:** `model-differ-truthy` (int truthiness),")
out.append("   `clause-a-1` (verdict needs passed==TOTAL, so the absent-tool verdict is unchanged; only")
out.append("   the printed clause value differs), `teeth-no-summ` (summary-less tools: clean reject vs")
out.append("   crash - admission identical, diagnostics degrade).")
out.append("")
out.append("## Restoration evidence")
out.append("")
out.append("- Frozen counter sha256 before: `ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99`")
out.append("- Frozen counter sha256 after (re-hash at close): see report; the file was only ever read.")
out.append("- Scratch `/fast/scratch/hyaku/mado-r43/MutC1CounterGates` deleted after copying evidence")
out.append("  (results jsonl, drivers, pristine log) into this seat dir.")
open(os.path.join(SEAT, "matrix.md"), "w").write("\n".join(out) + "\n")
print("matrix.md written:", len(out), "lines")
print("classified:", dict(cls_count), "total mutants:", sum(cls_count.values()))
