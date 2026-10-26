#!/usr/bin/env python3
"""MutC1CounterGates driver: build counter mutants, score each on REF + bad controls."""
import concurrent.futures, hashlib, json, os, shutil, subprocess, sys, tempfile, time

SCRATCH = "/fast/scratch/hyaku/mado-r43/MutC1CounterGates"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(SCRATCH, "counter-orig.py")
CTL = os.path.join(SCRATCH, "ctl")
TMP = os.path.join(SCRATCH, "tmp")
LOGS = os.path.join(SCRATCH, "logs")
MUTDIR = os.path.join(SCRATCH, "mut")
RES = os.path.join(SCRATCH, "results.jsonl")
REV = "a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f"
NONCE = "42aa42aa42aa42aa"
REF = os.path.join(CTL, "REF.py")
PANEL = ["M01-fifo-block", "M04-toolarge-ge", "M27-nomatch-rc", "K1-zero-test-selftest",
         "K3-exec-model", "K4-child-interpreter", "K5-getattr", "D1-constant"]
PRIS = [("/fast/scratch/hyaku/mado-r43/MutC1CounterGates/ctl/" + n + ".py") for n in PANEL]

# ---- mutant table: (name, old, new, expected_count)
M = []
def mu(name, old, new, cnt=1):
    M.append((name, old, new, cnt))

# constants / gate arithmetic
mu("total-const", "TOTAL = 37", "TOTAL = 36")
mu("total-ge", "and passed == TOTAL", "and passed >= TOTAL - 1")
mu("min-selftest", "MIN_SELFTEST = 50", "MIN_SELFTEST = 1")
mu("min-sites", "MIN_SITES = 12", "MIN_SITES = 1")
mu("n-mut", "N_MUT = 6", "N_MUT = 2")
mu("kill-need", "KILL_NEED = 4", "KILL_NEED = 1")
# sandbox flags
mu("cap-drop", '"--cap-drop", "ALL", ', "")
mu("unshare-all", '"--unshare-all", ', "")
mu("proc-flag", '"--proc", "/proc", ', "")
mu("nproc-lead", '["/usr/bin/prlimit", "--nproc=1:1"] if nproc', "[] if nproc")
mu("home-env", '"/nonexistent"', '"/home"')
mu("clearenv", '"--clearenv", ', "")
# nonce handling
mu("nonce-fixed", "nonce = args.nonce or secrets.token_hex(8)", 'nonce = args.nonce or "42aa42aa42aa42aa"')
mu("rng-nonce", '("%s:%s:%s:%d" % (rev, nonce, tag, i))', '("%s:%s:%d" % (rev, tag, i))')
mu("teeth-rng", '("mut:" + nonce)', '"mut:"')
# STDLIB_DENY: one entry removed each
mu("deny-socket", '{"socket", "urllib"', '{"urllib"')
mu("deny-urllib", '"urllib", "http"', '"http"')
mu("deny-http", '"http", "requests"', '"requests"')
mu("deny-requests", '"requests", "ssl"', '"ssl"')
mu("deny-ssl", '"ssl", "ctypes"', '"ctypes"')
mu("deny-ctypes", '"ctypes",\n', '"ctypes"')
mu("deny-importlib", '"importlib", "pty"', '"pty"')
mu("deny-pty", '"pty", "subprocess"', '"subprocess"')
mu("deny-subprocess", '"pty", "subprocess"}', '"pty"}')
mu("stdlib-allow-bypass", "and not (mods & STDLIB_DENY)", "")
mu("bool-mods", "bool(mods)", "True")
# CALL_DENY
mu("call-exec", '{"exec", "eval", "compile", "__import__"}', '{"eval", "compile", "__import__"}')
mu("call-eval", '{"exec", "eval",', '{"exec",')
mu("call-compile", '"compile", "__import__"}', '"__import__"}')
mu("call-import", '"__import__"}', '')
# NAME_DENY
mu("name-getattr", '{"getattr", "setattr"', '{"setattr"')
mu("name-setattr", '"getattr", "setattr", "delattr"', '"getattr", "delattr"')
mu("name-delattr", '"delattr", "vars"', '"vars"')
mu("name-vars", '"vars", "globals"', '"globals"')
mu("name-globals", '"globals", "locals"', '"locals"')
mu("name-locals", '"locals",\n             "breakpoint", "__file__"}', '"breakpoint", "__file__"}')
mu("name-breakpoint", '"breakpoint", "__file__"}', '"__file__"}')
mu("name-file", '"breakpoint", "__file__"}', '"breakpoint"}')
# OS_DENY
mu("os-system", '{"system", "popen"', '{"popen"')
mu("os-popen", '"system", "popen", "execv"', '"system", "execv"')
mu("os-execv", '"execv", "execve"', '"execve"')
mu("os-execve", '"execve", "execvp"', '"execvp"')
mu("os-execvp", '"execvp", "execl"', '"execl"')
mu("os-execl", '"execl", "execle"', '"execle"')
mu("os-execle", '"execle",\n           "execlp"', '"execlp"')
mu("os-execlp", '"execlp", "execvpe"', '"execvpe"')
mu("os-execvpe", '"execvpe", "execlpe"', '"execlpe"')
mu("os-execlpe", '"execlpe", "spawnl"', '"spawnl"')
mu("os-spawnl", '"spawnl", "spawnv"', '"spawnv"')
mu("os-spawnv", '"spawnv", "posix_spawn"', '"posix_spawn"')
mu("os-posix-spawn", '"spawnv", "posix_spawn"}', '"spawnv"}')
# STR_DENY
mu("str-proc", '("/proc", "c1-r42"', '("c1-r42"')
mu("str-c1r42", '"c1-r42", "quality/counters"', '"quality/counters"')
mu("str-qc", '"quality/counters")', ')')
# STR_EQ_DENY
mu("streq-exec", 'STR_EQ_DENY = {"exec", "eval"', 'STR_EQ_DENY = {"eval"')
mu("streq-eval", '"exec", "eval", "compile", "__import__", "system"', '"exec", "compile", "__import__", "system"')
mu("streq-compile", '"eval", "compile", "__import__", "system"', '"eval", "__import__", "system"')
mu("streq-import", '"compile", "__import__", "system"', '"compile", "system"')
mu("streq-system", '"__import__", "system", "popen"', '"__import__", "popen"')
mu("streq-popen", '"system", "popen",\n               "builtins"', '"system",\n               "builtins"')
mu("streq-builtins", '"builtins", "__builtins__"', '"__builtins__"')
mu("streq-dunder-builtins", '"__builtins__", "__file__"}', '"__file__"}')
mu("streq-file", '"__builtins__", "__file__"}', '"__builtins__"}')
# judge
mu("judge-stderr", "if want_rc in (0, 1, 3, 4) and err:", "if False and err:")
mu("judge-rc", "if rc != want_rc:", "if False:")
# model
mu("model-nosize", "if nsize == 0:", "if nsize < 0:")
mu("model-rc-differ", 'verdict, rc = "DIFFER", 1', 'verdict, rc = "DIFFER", 2')
mu("model-summary-swap", 't["AGREE"], t["DIFFER"],', 't["DIFFER"], t["AGREE"],')
mu("model-client-labels", "floating=%s size=%s ", "size=%s floating=%s ")
mu("model-differ-truthy", 'elif t["DIFFER"]:', 'elif t["DIFFER"] >= 1:')
# teeth
mu("teeth-dead-def", "dead = rc != 0 or not has or k != n_", "dead = rc != 0")
mu("teeth-forced-site", "forced = rng.choice(summ)", "forced = rng.choice(rest + summ)")
mu("teeth-or", "return killed >= KILL_NEED and forced_dead", "return killed >= KILL_NEED or forced_dead")
mu("teeth-no-summ", "if not summ:", "if False:")
# neutrality
mu("neutral-or", "ok &= good", "ok |= good")
mu("neutral-minselftest", "good = rc == 0 and has and k == n and n >= MIN_SELFTEST",
   "good = rc == 0 and has and k == n")
# main / output
mu("clause-a-1", 'cl = {"a": int(present),', 'cl = {"a": 1,')
mu("exit-always-0", "return 0 if met else 1", "return 0")
mu("verdict-string", '"TARGET_MET" if met else "TARGET_MISSED"', '"TARGET_MET"')
mu("timeout-breaker", "TIMEOUTS[0] += 1", "TIMEOUTS[0] += 0", 2)

os.makedirs(MUTDIR, exist_ok=True)
src0 = open(COUNTER).read()
built, build_err = [], []
for name, old, new, cnt in M:
    n = src0.count(old)
    if n != cnt:
        build_err.append((name, old, n, cnt))
        continue
    text = src0.replace(old, new)
    path = os.path.join(MUTDIR, name + ".py")
    open(path, "w").write(text)
    try:
        compile(text, name, "exec")  # syntax check; DOA mutants excluded and logged
    except SyntaxError as e:
        build_err.append((name, "SyntaxError %s" % e, 0, 0))
        continue
    built.append(name)
print("mutants built+parsed:", len(built), "build_errors:", build_err)


def run_one(counter_path, tool_path, tag):
    env = dict(os.environ, C1R42_TMP=TMP)
    cmd = [sys.executable, "-I", counter_path, "--repo", LANE, "--rev", REV, "--nonce", NONCE]
    if tool_path:
        cmd += ["--tool", tool_path]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = 124, "", "driver-timeout"
    dt = time.time() - t0
    final = [ln for ln in out.splitlines() if ln.startswith("PRED-C1-r42:")]
    cl = [ln for ln in out.splitlines() if " clauses=" in ln]
    failed = [ln.split("fixture=")[1].split(" ok=0")[0] for ln in out.splitlines() if " ok=0 " in ln]
    met = bool(final) and "TARGET_MET" in final[-1]
    return {"counter": os.path.basename(counter_path), "target": tag, "rc": rc, "sec": round(dt, 1),
            "met": met, "final": final[-1] if final else "NO_FINAL_LINE " + (out[-160:] + err[-160:]).replace("\n", " | "),
            "clauses": cl[-1].split(" clauses=")[1] if cl else "-",
            "failed": failed}


jobs = []
targets = [("REF", REF)] + [(n, os.path.join(CTL, n + ".py")) for n in PANEL]
for name in built:
    for tag, path in targets:
        jobs.append((os.path.join(MUTDIR, name + ".py"), path, tag))
# pristine anchors on the panel + absent-base; clause-a mutant also on absent-base
for tag, path in targets:
    jobs.append((COUNTER, path, tag))
jobs.append((COUNTER, None, "BASE-absent"))
jobs.append((os.path.join(MUTDIR, "clause-a-1.py"), None, "BASE-absent"))

with open(RES, "w") as fh:
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
        futs = {ex.submit(run_one, c, t, tag): (c, tag) for c, t, tag in jobs}
        done = 0
        for f in concurrent.futures.as_completed(futs):
            r = f.result()
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            done += 1
            if done % 100 == 0:
                print("done %d/%d" % (done, len(jobs)), flush=True)
print("ALL RUNS", done)
