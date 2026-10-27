#!/usr/bin/env python3
"""Replay the frozen round-48 C1 fixture set against the real pin and against the frozen tool (and a mutant).

Preparation follows the counter's clause-w schema (files in meta.files_order, exec stubs, mtime pinning,
cache literal or pin-primed, after-mutations), run on the host instead of bwrap (PATH=$ROOT/bin:/usr/bin:/bin).
Variant A only. Output: per-fixture (oracle rc/stdout/state, tool rc/stdout, agreement), plus premise checks.
Usage: replay.py TOOL
"""
import json, os, shutil, stat, subprocess, sys, time

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = L + "/.ufo/waves/round-47/fetch/xdg-terminal-exec"
FX = L + "/.ufo/waves/round-48/l1-draft/c1-r48-fixtures.json"
S = "/fast/scratch/hyaku/mado-r48/RevC1Cache"
TERM = "\x1eEND_OF_EXEC_USEP"
TOOL = sys.argv[1]
TAG = os.environ.get("REPLAY_TAG", "")

def encode(text, root):
    return text.replace("$ROOT", root).encode("utf-8", "surrogateescape")

def safe_rel(root, rel):
    assert not rel.startswith("/") and ".." not in rel.split("/"), rel
    return os.path.join(root, rel)

def write_files(root, files, order=None):
    for rel in list(order or []) + [r for r in files if r not in (order or [])]:
        text = files[rel]
        if rel.endswith("/"):
            os.makedirs(safe_rel(root, rel), exist_ok=True); continue
        p = safe_rel(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(encode(text, root))

def add_execs(root, execs):
    for rel in execs:
        p = safe_rel(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            open(p, "w").write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)

def apply_mtime(root, t):
    files, dirs = [], []
    for d, ds, fs in os.walk(root):
        if os.path.relpath(d, root).split(os.sep)[0] == ".rw":
            ds[:] = []; continue
        files += [os.path.join(d, f) for f in fs]
        dirs  += [os.path.join(d, x) for x in ds
                  if os.path.relpath(os.path.join(d, x), root).split(os.sep)[0] != ".rw"]
    for p in files: os.utime(p, (t, t))
    for p in sorted(dirs, key=lambda x: x.count(os.sep), reverse=True): os.utime(p, (t, t))

def cache_path(root, default_cache):
    return os.path.join(root, "home", ".cache" if default_cache else os.path.join(".rw", "cache"), "xdg-terminal-exec") \
        if not default_cache else os.path.join(root, "home", ".cache", "xdg-terminal-exec")

def cpath(root, dc):
    return os.path.join(root, "home", ".cache", "xdg-terminal-exec") if dc \
        else os.path.join(root, ".rw", "cache", "xdg-terminal-exec")

def case_env(case, root, phase):
    e = dict(case["env"])
    unset = set(case.get("unset") or [])
    if phase == "scored":
        a = case.get("after") or {}
        for k, v in (a.get("env") or {}).items(): e[k] = v
        unset |= set(a.get("unset") or [])
    out = {k: v.replace("$ROOT", root) for k, v in e.items() if v is not None}
    for k in unset: out.pop(k, None)
    if "HOME" not in unset: out["HOME"] = os.path.join(root, "home")
    if "PATH" not in unset: out["PATH"] = os.path.join(root, "bin") + ":/usr/bin:/bin"
    if "LANG" not in unset: out["LANG"] = "C.UTF-8"
    if "XDG_CACHE_HOME" not in unset:
        if case.get("default_cache"): out.pop("XDG_CACHE_HOME", None)
        else: out["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "cache")
    return out

def apply_after(root, after, with_cache=True):
    for rel, text in (after.get("files") or {}).items():
        p = safe_rel(root, rel)
        if text is None:
            if os.path.isdir(p) and not os.path.islink(p): shutil.rmtree(p)
            elif os.path.lexists(p): os.unlink(p)
        elif rel.endswith("/"): os.makedirs(p, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(encode(text, root))
    add_execs(root, after.get("exec_add") or [])
    for rel in after.get("exec_remove") or []:
        p = safe_rel(root, rel)
        if os.path.lexists(p): os.unlink(p)
    for rel, mode in (after.get("modes") or {}).items():
        os.chmod(safe_rel(root, rel), int(mode))
    if with_cache and (after.get("cache_lines") or after.get("cache_sub") or after.get("cache_append") is not None):
        cp = cpath(root, False)
        text = open(cp, "rb").read().decode("utf-8", "surrogateescape")
        if after.get("cache_lines"):
            lines = text.split("\n")
            for ln, val in sorted(after["cache_lines"].items(), key=lambda kv: int(kv[0])):
                lines[int(ln) - 1] = val.replace("$ROOT", root)
            text = "\n".join(lines)
        for old, new in after.get("cache_sub") or []:
            text = text.replace(old.replace("$ROOT", root), new.replace("$ROOT", root))
        for ln in after.get("cache_append") or []:
            text = text + ln.replace("$ROOT", root) + "\n"
        open(cp, "wb").write(text.encode("utf-8", "surrogateescape"))

def materialize(root, case):
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, ".rw", "cache"))
    if case.get("default_cache"): os.makedirs(os.path.join(root, "home", ".cache"))
    write_files(root, case["files"], (case.get("meta") or {}).get("files_order"))
    add_execs(root, case["exec"])

def prime(root, case):
    env = case_env(case, root, "prime")
    cp = cpath(root, case.get("default_cache", False))
    os.makedirs(os.path.dirname(cp), exist_ok=True)
    args = [a.replace("$ROOT", root) for a in ((case["prime"] or {}).get("args") or ["--print-cmd"])]
    subprocess.run(["/bin/sh", PIN] + args, capture_output=True, env=env, timeout=60)
    for _ in range(1200):
        try:
            if open(cp, "rb").read().decode("latin-1").rstrip("\n").endswith(TERM): return
        except OSError: pass
        time.sleep(0.005)

def prepare(root, case, cold=False):
    materialize(root, case)
    t = case.get("mtime")
    if t is not None: apply_mtime(root, t)
    if not cold:
        if "cache" in case:
            p = cpath(root, case.get("default_cache", False))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(encode(case["cache"], root))
        elif "prime" in case:
            prime(root, case)
    after = case.get("after") or {}
    apply_after(root, after, with_cache=not cold)
    if after.get("mtime", case.get("mtime")) is not None:
        apply_mtime(root, after.get("mtime", case.get("mtime")))

STATES = (("cache is actual","hit"),("cache is out-of-date","stale"),("invalid cache data","invalid"),
          ("reached cache line limit","invalid"),("failed to get fresh hash","invalid"),
          ("no cache data","absent"),("paths:","disabled"))
def derive_state(err):
    for pat, st in STATES:
        if pat in err: return st
    return "-"

def oracle(root, case):
    env = case_env(case, root, "scored"); env["XTE_DEBUG"] = "1"
    args = [a.replace("$ROOT", root) for a in case["args"]]
    p = subprocess.run(["/bin/sh", PIN] + args, capture_output=True, env=env, timeout=60)
    return (p.returncode, p.stdout.decode("utf-8", "surrogateescape").replace(root, "$ROOT"),
            derive_state(p.stderr.decode("utf-8", "surrogateescape")))

def tool(root, case):
    env = case_env(case, root, "scored")
    args = [a.replace("$ROOT", root) for a in case["args"]]
    p = subprocess.run([sys.executable, "-I", TOOL, "print"] + args, capture_output=True, env=env, timeout=60)
    return (p.returncode, p.stdout.decode("utf-8", "surrogateescape").replace(root, "$ROOT"),
            p.stderr.decode("utf-8", "surrogateescape")[-200:])

TERM_RE = None
def explain_fields(out):
    import re
    lines=[l for l in out.split("\n") if l.startswith("MADO_TERM: ")]
    if not lines: return ("no MADO_TERM line",)
    m=re.match(r"MADO_TERM: selected=(.*?) path=(.*?) cmd=(.*?) cache=(\S+) verdict=(\S+)$", lines[-1])
    if not m: return ("unparseable", lines[-1][:80])
    return (m.group(1), m.group(2), m.group(4), m.group(5))

def explain_check(ro, rt, case, state):
    """Clause x: the oracle runs --print-id --print-path --print-cmd on its own tree; the tool's explain
    must name the same selection, path, cache state and verdict."""
    env_o = case_env(case, ro, "scored"); env_o["XTE_DEBUG"] = "1"
    q = subprocess.run(["/bin/sh", PIN, "--print-id", "--print-path", "--print-cmd"],
                       capture_output=True, env=env_o, timeout=60)
    parts = q.stdout.decode("utf-8", "surrogateescape").replace(ro, "$ROOT").split("\n")
    env = case_env(case, rt, "scored")
    p = subprocess.run([sys.executable, "-I", TOOL, "explain"], capture_output=True, env=env, timeout=60)
    got = explain_fields(p.stdout.decode("utf-8", "surrogateescape").replace(rt, "$ROOT"))
    if q.returncode == 0:
        want = (parts[0], parts[1] if len(parts) > 1 else "", state, "OK")
    else:
        want = ("-", "-", state, "NO_TERMINAL")
    ok = len(got) == 4 and got == want and (p.returncode == (0 if q.returncode == 0 else 3))
    return ok, got, want + ("rc=%d" % p.returncode,)

def run(case):
    base = os.path.join(S, "rp" + TAG, case["id"].replace("/", "_"))
    shutil.rmtree(base, ignore_errors=True)
    ro, rt = os.path.join(base, "o"), os.path.join(base, "t")
    try:
        prepare(ro, case); prepare(rt, case)
        o = oracle(ro, case)
        t = tool(rt, case)
        ex_ok, ex_got, ex_want = explain_check(ro, rt, case, o[2])
        cold = None
        if case.get("prime") or "cache" in case:
            rc_ = os.path.join(base, "c")
            prepare(rc_, case, cold=True)
            cold = oracle(rc_, case)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    return o, t, cold, (ex_ok, ex_got, ex_want)

def main():
    fx = json.load(open(FX))
    rows, fails = [], []
    for case in fx:
        o, t, cold, ex = run(case)
        ok = (o[0], o[1]) == (t[0], t[1])
        st_ok = ("state" not in case) or case["state"] == o[2]
        cold_ok = True
        if "cold" in case and cold is not None:
            cold_ok = [cold[0], cold[1]] == [case["cold"]["rc"], case["cold"]["stdout"]]
        cls = case["class"]
        prem = True
        if cls == "WARM-DIFFERS" and cold is not None:
            prem = [cold[0], cold[1]] != [case["expect"]["rc"], case["expect"]["stdout"]]
        if cls == "WARM-SAME" and cold is not None:
            prem = [cold[0], cold[1]] == [case["expect"]["rc"], case["expect"]["stdout"]]
        if cls.startswith("generated-warm-"):
            prem = prem and o[2] == cls.rsplit("-", 1)[-1]
        exp_ok = (o[0], o[1]) == (case["expect"]["rc"], case["expect"]["stdout"])
        rows.append(dict(id=case["id"], cls=cls, tool_ok=ok, ex_ok=ex[0], ex_got=ex[1], ex_want=ex[2], state=o[2], rec=case.get("state"),
                         state_ok=st_ok, cold_ok=cold_ok, prem=prem, exp_ok=exp_ok,
                         tool=(t[0], t[1][:60]), orc=(o[0], o[1][:60])))
        if not (ok and st_ok and cold_ok and prem and exp_ok and ex[0]):
            fails.append(rows[-1])
    json.dump(rows, open(os.path.join(S, "ev", "replayx%s-%s.json" % (TAG, os.path.basename(TOOL).replace(".py", ""))), "w"), indent=1)
    print("tool=%s fixtures=%d tool_agrees=%d state_ok=%d cold_ok=%d premise_ok=%d expect_ok=%d explain_ok=%d" % (
        os.path.basename(TOOL), len(rows), sum(r["tool_ok"] for r in rows), sum(r["state_ok"] for r in rows),
        sum(r["cold_ok"] for r in rows), sum(r["prem"] for r in rows), sum(r["exp_ok"] for r in rows),
        sum(r["ex_ok"] for r in rows)))
    for r in fails:
        print("FAIL", json.dumps(r))

main()
