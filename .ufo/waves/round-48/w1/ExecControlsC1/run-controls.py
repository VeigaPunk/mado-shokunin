#!/usr/bin/env python3
"""run-controls.py - score every C1 control against the C1 counter (round 48, wave w1, seat ExecControlsC1).

Two judging paths, in this order:

  1. DRAFT: if ExecCounterC1's draft counter is present (.ufo/waves/round-48/w1/ExecCounterC1/c1-r48-*.py), each
     control is committed into its own scratch clone of the lane and scored by that counter (the real instrument),
     verbatim. Its verdict and clause lines are the receipt.
  2. LOCAL: always, and alone when the draft is absent: the same oracle the counter uses - the pinned resolver
     (.ufo/waves/round-47/fetch/xdg-terminal-exec, sha256 89f2be9a...27ac) - inside the counter's allowlist sandbox
     (bwrap, no /etc, numeric ids), on this seat's fixture schema v2 set (fixtures-v2.json):
        prime    a cold `--print-cmd` run of the PIN in the tree, then wait for the background cache save
        after    the fixture's post-prime mutations, mtimes re-pinned
        scored   the PIN again in the oracle tree, the TOOL in its own identically primed tree; the tool's
                 stdout (root -> $ROOT) and exit status must equal the pin's
        cold     the PIN in a twin tree with the post-mutation state and no prime: this is what the resolver
                 would print without a cache, so a fixture only has teeth when warm != cold, and a fixture
                 whose declared cache state is not "hit" must have warm == cold
        explain  the tool's `explain` MADO_TERM line: selected=, path= and cmd= against the oracle, cache= against
                 the verified state of the fixture
        readonly every tool run under strace; any execve/socket event after the sandboxed python3 is a trip
     `expect` is never typed: it is produced by three identical pin runs and stored in receipts/expect.json.

Output: receipts/summary.txt (+ receipts/<control>.txt), and a one-line-per-control console table.
Exit 0 iff every control MISSES and no control writes into its tree.

usage: run-controls.py [--controls DIR] [--only NAME[,NAME]] [--fixtures PATH] [--work DIR] [--no-draft]
"""
import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.realpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
PIN = os.path.join(LANE, ".ufo", "waves", "round-47", "fetch", "xdg-terminal-exec")
PIN_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")
TRACE_SET = "trace=execve,execveat,socket,socketpair,connect"
DRAFT_DIR = os.path.join(HERE, "..", "ExecCounterC1")
BASE_REV = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
ENV_GIT = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def pin_blob():
    blob = open(PIN, "rb").read()
    if hashlib.sha256(blob).hexdigest() != PIN_SHA256:
        raise SystemExit("pin sha256 mismatch: %s" % PIN)
    return blob


# ------------------------------------------------------------------------------------------------ sandbox
class Box:
    def __init__(self, work):
        self.work = work
        self.bwrap = shutil.which("bwrap")
        self.strace = shutil.which("strace")
        if not self.bwrap:
            raise SystemExit("bwrap missing")
        if not self.strace:
            raise SystemExit("strace missing")
        self.bin = os.path.join(work, "bin")
        os.makedirs(self.bin, exist_ok=True)
        for n in EXTERNALS:
            src = shutil.which(n, path="/usr/bin")
            if not src:
                raise SystemExit("external %s missing" % n)
            shutil.copy(os.path.realpath(src), os.path.join(self.bin, n))
        self.pin = os.path.join(work, "xdg-terminal-exec")
        with open(self.pin, "wb") as fh:
            fh.write(pin_blob())
        os.chmod(self.pin, 0o755)
        self.bash = os.path.realpath("/usr/bin/bash")
        self.python = os.path.realpath(sys.executable)

    def argv(self, root, env, tool, args):
        rw = os.path.join(root, ".rw")
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
             "--ro-bind", self.bash, "/bin/sh", "--ro-bind", self.bash, "/bin/bash",
             "--ro-bind", self.bin, "/oracle/bin", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
             "--ro-bind", root, root, "--bind", rw, rw, "--chdir", root]
        if tool:
            a += ["--ro-bind", self.python, "/usr/bin/python3", "--ro-bind", tool, "/oracle/tool.py"]
        else:
            a += ["--ro-bind", self.pin, "/oracle/xdg-terminal-exec"]
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        a += (["/usr/bin/python3", "-I", "/oracle/tool.py"] if tool else ["/oracle/xdg-terminal-exec"]) + args
        return a

    # bwrap is PID 1 of the namespace and kills every process in it when the pin exits, so a prime run must hold
    # the namespace open until the forked save_cache has written the cache (bash spin, no external command).
    KEEPALIVE = ('f="$XDG_CACHE_HOME/xdg-terminal-exec"; i=0; while [ "$i" -lt 4000 ]; do '
                 'if [ -f "$f" ]; then mapfile -t L < "$f"; '
                 'if [ "${#L[@]}" -ge 11 ] && [ "${L[-1]}" = "$(printf %b \\036)END_OF_EXEC_USEP" ]; then break; fi; '
                 'fi; i=$((i+1)); done')

    def run(self, root, env, tool, args, timeout=60, keepalive=False):
        argv = self.argv(root, env, tool, args)
        if keepalive:
            argv = argv[:-(len(args) + 1)] + ["/bin/bash", "-c",
                                        "/oracle/xdg-terminal-exec " + " ".join(shlex.quote(x) for x in args)
                                        + "; " + self.KEEPALIVE]
        trace = None
        if tool:
            fd, trace = tempfile.mkstemp(dir=self.work, prefix="trace-")
            os.close(fd)
            argv = [self.strace, "-f", "-qq", "-e", TRACE_SET, "-e", "signal=none", "-o", trace] + argv
        try:
            p = subprocess.run(argv, capture_output=True, timeout=timeout, env={"PATH": "/usr/bin"})
            res = [p.returncode, p.stdout.decode("latin-1"), p.stderr.decode("latin-1")]
        except subprocess.TimeoutExpired:
            res = [124, "", "timeout"]
        trips = self.trips(trace) if trace else []
        return res[0], res[1], res[2], trips

    def trips(self, path):
        try:
            lines = open(path, encoding="latin-1").read().splitlines()
        except OSError:
            return ["trace-missing"]
        seen, py_pid, out = False, None, []
        for ln in lines:
            pid, _, rest = ln.partition(" ")
            rest = rest.strip()
            if not seen:
                if 'execve("/usr/bin/python3"' in rest:
                    py_pid = pid
                    seen = rest.endswith("= 0")
                elif pid == py_pid and rest.startswith("<... execve resumed>"):
                    seen = rest.endswith("= 0")
                continue
            out.append(rest[:70])
        if not seen:
            out.append("python-execve-not-seen")
        os.unlink(path)
        return out


# ------------------------------------------------------------------------------------------------ trees
def materialize(root, case):
    os.makedirs(os.path.join(root, "home"), exist_ok=True)
    os.makedirs(os.path.join(root, ".rw", "cache"), exist_ok=True)
    for rel, text in (case.get("files") or {}).items():
        if ".." in rel.split("/"):
            raise SystemExit("unsafe path %r in %s" % (rel, case["id"]))
        p = os.path.join(root, rel)
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("latin-1"))
    for rel in case.get("exec") or []:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    pin_mtimes(root, case.get("mtime"))
    if case.get("cache") is not None:
        p = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
        with open(p, "wb") as fh:
            fh.write(case["cache"].replace("$ROOT", root).encode("latin-1"))


def pin_mtimes(root, epoch):
    if epoch is None:
        return
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for n in filenames + dirnames:
            paths.append(os.path.join(dirpath, n))
    paths.sort(key=lambda p: p.count("/"), reverse=True)      # children before their parents
    for p in paths:
        try:
            os.utime(p, (epoch, epoch), follow_symlinks=False)
        except OSError:
            pass
    os.utime(root, (epoch, epoch))


def mutate(root, after):
    if not after:
        return
    for rel, text in (after.get("files") or {}).items():
        p = os.path.join(root, rel)
        if isinstance(text, dict) and "$cache" in text:
            op = text["$cache"]
            try:
                cur = open(cache_path(root), encoding="latin-1").read()
            except OSError:
                continue                    # the cold twin has no cache to rewrite

            lines = cur.split("\n")
            if lines and lines[-1] == "":
                lines.pop()
            if len(lines) < 11:
                raise SystemExit("cache op %r on a %d-line cache: the prime did not complete" % (op, len(lines)))
            if op == "drop_terminator":
                lines = lines[:-1]
            elif op == "bad_hash":
                lines[0] = "0" * 32
            elif op.startswith("set_cmd:"):
                lines[1] = op.split(":", 1)[1]
            elif op == "term_midline":
                lines[-1] = lines[-1] + "TRAILING"
            elif op.startswith("pad_before_exec:"):
                n = int(op.split(":", 1)[1])
                lines = lines[:-1] + ["pad"] * n + lines[-1:]
            else:
                raise SystemExit("unknown cache op %r" % op)
            with open(p, "w", encoding="latin-1") as fh:
                fh.write("".join(x + "\n" for x in lines))
            continue
        if text is None:
            try:
                os.unlink(p)
            except OSError:
                pass
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("latin-1"))
    for rel in after.get("exec_add") or []:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    for rel in after.get("exec_remove") or []:
        try:
            os.unlink(os.path.join(root, rel))
        except OSError:
            pass
    pin_mtimes(root, after.get("mtime", None))


def case_env(case, root, with_after=True):
    env = {k: v.replace("$ROOT", root) for k, v in case["env"].items()}
    env["HOME"] = os.path.join(root, "home")
    env["PATH"] = os.path.join(root, "bin") + ":/oracle/bin"
    env["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "cache")
    env.setdefault("LANG", "C.UTF-8")
    for k in case.get("unset") or []:
        env.pop(k, None)
    after = case.get("after") or {}
    if with_after:
        for k, v in (after.get("env") or {}).items():
            env[k] = v.replace("$ROOT", root)
    return env


def norm(text, root):
    return text.replace(root, "$ROOT")


def cache_path(root):
    return os.path.join(root, ".rw", "cache", "xdg-terminal-exec")


def prime(box, root, case):
    """A cold `--print-cmd` run of the pin leaves the cache; save_cache is forked, so wait for it."""
    args = (case.get("prime") or {}).get("args") or ["--print-cmd"]
    rc, out, err, _ = box.run(root, case_env(case, root, with_after=False), None, args, keepalive=True)
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            text = open(cache_path(root), encoding="latin-1").read()
        except OSError:
            text = ""
        if text.rstrip("\n").endswith("\x1eEND_OF_EXEC_USEP"):
            return rc, out
        time.sleep(0.02)
    raise SystemExit("%s: the prime left no complete cache (rc=%d stdout=%r)" % (case["id"], rc, out[:60]))


def tree(box, base, name, case, mtime=None):
    root = os.path.join(base, name, "r")
    shutil.rmtree(os.path.join(base, name), ignore_errors=True)
    os.makedirs(os.path.join(base, name), exist_ok=True)
    materialize(root, case)
    if mtime is not None:
        pin_mtimes(root, mtime)
    return root


def dir_signature(root):
    """Every file under root with size and mtime, to catch a tool that writes."""
    sig = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for n in filenames:
            p = os.path.join(dirpath, n)
            try:
                st = os.lstat(p)
            except OSError:
                continue
            sig[p[len(root):]] = (st.st_size, st.st_mtime_ns)
    return sig


# ------------------------------------------------------------------------------------------------ case scoring
def oracle_and_cold(box, base, case):
    """The scored oracle result of a fixture, produced twice in a fresh tree (3 pin runs), plus the cold twin."""
    results = []
    for k in range(3):
        root = tree(box, base, "o%d" % k, case)
        if case.get("prime"):
            prime(box, root, case)
        mutate(root, case.get("after"))
        rc, out, err, _ = box.run(root, case_env(case, root), None, case["args"])
        results.append((rc, norm(out, root)))
        if k == 0:
            shutil.copytree(root, os.path.join(base, "keep"), symlinks=True)
        else:
            shutil.rmtree(os.path.join(base, "o%d" % k), ignore_errors=True)
    if results[0] != results[1] or results[0] != results[2]:
        raise SystemExit("%s: the oracle is not stable over 3 runs: %r" % (case["id"], results))
    warm = results[0]
    # cold twin: the post-mutation state, no cache at all
    root = tree(box, base, "cold", case)
    mutate(root, case.get("after"))
    dst = cache_path(root)
    for rel in ("xdg-terminal-exec",):
        try:
            os.unlink(os.path.join(root, ".rw", "cache", rel))
        except OSError:
            pass
    cold_rc, cold_out, _, _ = box.run(root, case_env(case, root), None, case["args"])
    cold = (cold_rc, norm(cold_out, root))
    state = case.get("state", "hit")
    if state == "hit" and warm == cold:
        raise SystemExit("%s: declared hit, but warm==cold=%r (no teeth)" % (case["id"], warm))
    if state != "hit" and warm != cold:
        raise SystemExit("%s: declared %s, but warm=%r cold=%r" % (case["id"], state, warm, cold))
    # the three print modes of the same environment, for the explain clause
    root = tree(box, base, "x", case)
    if case.get("prime"):
        prime(box, root, case)
    mutate(root, case.get("after"))
    rc3, out3, _, _ = box.run(root, case_env(case, root), None, ["--print-id", "--print-path", "--print-cmd"])
    parts = norm(out3, root).split("\n")
    case["_expect3"] = (parts[0] if parts else "", parts[1] if len(parts) > 1 else "",
                        parts[2].split("\n")[0].split(" ")[0] if len(parts) > 2 and parts[2] else "-", rc3,
                        state)
    shutil.rmtree(os.path.join(base, "x"), ignore_errors=True)
    return warm, cold


def tool_tree(box, base, case, tool):
    """Materialize the tool's own tree, prime it with the PIN (cold), mutate, and return it."""
    root = tree(box, base, "t", case)
    if case.get("prime"):
        prime(box, root, case)
    mutate(root, case.get("after"))
    return root


def score_case(box, base, case, tool):
    warm, cold = case["_expect"]
    root = tool_tree(box, base, case, tool)
    before = dir_signature(root)
    rc, out, err, trips = box.run(root, case_env(case, root), tool, ["print"] + case["args"])
    after = dir_signature(root)
    wrote = [k for k in set(before) | set(after) if before.get(k) != after.get(k)]
    ok = (rc, norm(out, root)) == warm
    detail = "" if ok else "oracle=%r tool=%r" % (warm, (rc, norm(out, root)[:120]))
    # explain: selected=, path= and cmd= against the oracle, cache= against the verified state
    exp_ok, exp_why = explain_case(box, base, case, tool, warm)
    return {"ok": ok, "detail": detail, "trips": trips, "wrote": wrote,
            "explain_ok": exp_ok, "explain": exp_why}


def explain_case(box, base, case, tool, warm):
    root = tool_tree(box, base, case, tool)
    rc, out, err, trips = box.run(root, case_env(case, root), tool, ["explain"])
    text = norm(out, root)
    idx = text.rfind("MADO_TERM: ")
    if idx < 0:
        return False, "no MADO_TERM line (rc=%d %s)" % (rc, err.strip()[:80])
    f = {}
    for kv in text[idx + len("MADO_TERM: "):].split():
        if "=" in kv:
            k, v = kv.split("=", 1)
            if k in ("cache", "verdict"):
                f[k] = v
            else:
                f.setdefault(k, v)
    sel3, path3, cmd3, rc3, state = case["_expect3"]
    if rc3 == 0:
        want = (sel3, path3, cmd3, state, "OK", 0)
    else:
        want = ("-", "-", "-", state, "NO_TERMINAL", 3)
    got = (f.get("selected"), f.get("path"), f.get("cmd"), f.get("cache"), f.get("verdict"), rc)
    if got != want:
        return False, "explain got=%r want=%r" % (got, want)
    return True, ""


# ------------------------------------------------------------------------------------------------ draft counter
def find_draft():
    d = os.path.realpath(DRAFT_DIR)
    if not os.path.isdir(d):
        return None, None
    counters = sorted(os.path.join(d, n) for n in os.listdir(d)
                      if n.endswith(".py") and ("r48" in n or "cache" in n))
    fixtures = sorted(os.path.join(d, n) for n in os.listdir(d) if n.endswith(".json"))
    return (counters[0] if counters else None), (fixtures[0] if fixtures else None)


def run_draft(box, work, counter, tool, name):
    """Score one control with the real draft counter: a scratch clone of the lane, the control at the tool path."""
    d = os.path.join(work, "clones", name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    p = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, d], env=ENV_GIT)
    if p.returncode:
        return None, "clone failed"
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, env=ENV_GIT)
    if os.path.realpath(top.stdout.decode().strip()) != os.path.realpath(d):
        return None, "clone top-level is not the fixture dir"
    subprocess.run(["git", "-C", d, "checkout", "-q", "--detach", BASE_REV], env=ENV_GIT, check=True)
    shutil.copy(tool, os.path.join(d, "tools", "mado-terminal.py"))
    subprocess.run(["git", "-C", d, "add", "tools/mado-terminal.py"], env=ENV_GIT, check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid",
                    "commit", "-q", "-m", "control " + name], env=ENV_GIT, check=True)
    wk = os.path.join(work, "draft-work", name)
    os.makedirs(wk, exist_ok=True)
    cmd = [sys.executable, "-I", counter, "--repo", d, "--rev", "HEAD", "--work", wk, "--nonce", "48"]
    p = subprocess.run(cmd, capture_output=True, env={**ENV_GIT, "TMPDIR": work})
    txt = (p.stdout + p.stderr).decode("utf-8", "replace")
    return p.returncode, txt


# ------------------------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls", default=os.path.join(HERE, "controls"))
    ap.add_argument("--only", default=None)
    ap.add_argument("--fixtures", default=os.path.join(HERE, "fixtures-v2.json"))
    ap.add_argument("--work", default=None)
    ap.add_argument("--no-draft", action="store_true")
    a = ap.parse_args()
    work = a.work or os.environ.get("TMPDIR") or tempfile.mkdtemp(prefix="mado-controls.")
    work = os.path.abspath(work)
    os.makedirs(work, exist_ok=True)
    receipts = os.path.join(HERE, "receipts")
    os.makedirs(receipts, exist_ok=True)
    cases = json.load(open(a.fixtures))
    names = [n[:-3] for n in sorted(os.listdir(a.controls)) if n.endswith(".py")]
    if a.only:
        keep = set(a.only.split(","))
        names = [n for n in names if n in keep]
    box = Box(work)
    expect_path = os.path.join(receipts, "expect.json")
    expect = {}
    print("== oracle: %d fixtures, prime + 3 identical pin runs + cold twin" % len(cases))
    for case in cases:
        base = os.path.join(work, "fx", case["id"])
        shutil.rmtree(base, ignore_errors=True)
        os.makedirs(base)
        warm, cold = oracle_and_cold(box, base, case)
        case["_expect"] = (warm, cold)
        expect[case["id"]] = {"state": case.get("state"), "warm": warm, "cold": cold,
                             "teeth": case.get("prime") is not None or case.get("cache") is not None}
        print("   %-34s state=%-8s warm=%r" % (case["id"], case.get("state"), warm))
    with open(expect_path, "w") as fh:
        json.dump(expect, fh, indent=1, sort_keys=True)
        fh.write("\n")

    draft, draft_fx = (None, None) if a.no_draft else find_draft()
    print("== draft counter: %s" % (draft or "ABSENT (local pin-judged loop only)"))
    rows = []
    for name in names:
        tool = os.path.join(a.controls, name + ".py")
        base = os.path.join(work, "run", name)
        shutil.rmtree(base, ignore_errors=True)
        os.makedirs(base)
        fails, exp_fails, trips, writes = [], [], [], []
        for case in cases:
            r = score_case(box, base, case, tool)
            if not r["ok"]:
                fails.append((case["id"], r["detail"]))
            if not r["explain_ok"]:
                exp_fails.append((case["id"], r["explain"]))
            if r["trips"]:
                trips.append((case["id"], r["trips"][:2]))
            if r["wrote"]:
                writes.append((case["id"], r["wrote"][:3]))
        draft_rc, draft_txt = (None, "")
        if draft:
            draft_rc, draft_txt = run_draft(box, work, draft, tool, name)
        missed = bool(fails or exp_fails or trips or writes)
        verdict = "MISS" if missed else "MEETS"
        clause = "+".join(x for x in (("f" if fails else ""), ("x" if exp_fails else ""), ("r" if trips else ""),
                                      ("w" if writes else "")) if x)
        r47 = "MISS" if (fails or exp_fails or trips) else "MEETS"
        rows.append((name, verdict, clause, fails, exp_fails, trips, writes, draft_rc, r47))
        with open(os.path.join(receipts, name + ".txt"), "w") as fh:
            fh.write("control %s\nverdict %s (clauses: %s)\n" % (name, verdict, clause or "-"))
            for label, items in (("fixture-miss", fails), ("explain-miss", exp_fails), ("trace-trip", trips),
                                 ("tree-write", writes)):
                for cid, det in items:
                    fh.write("%-13s %-34s %s\n" % (label, cid, det))
            if draft:
                fh.write("\ndraft counter (rc=%s):\n%s\n" % (draft_rc, draft_txt))
        print("%-22s %-5s %-8s f=%d x=%d r=%d w=%d r47-clauses=%s%s" % (
            name, verdict, clause or "-", len(fails), len(exp_fails), len(trips), len(writes), r47,
            ("  draft_rc=%s" % draft_rc) if draft else ""))
        for cid, det in fails[:3]:
            print("      f %-32s %s" % (cid, det))
        for cid, det in exp_fails[:3]:
            print("      x %-32s %s" % (cid, det))
        for cid, det in trips[:2]:
            print("      r %-32s %s" % (cid, det))
        for cid, det in writes[:2]:
            print("      w %-32s %s" % (cid, det))
    with open(os.path.join(receipts, "summary.txt"), "w") as fh:
        fh.write("oracle: %s sha256 %s\n" % (PIN, PIN_SHA256))
        fh.write("fixtures: %s (%d cases)\n" % (a.fixtures, len(cases)))
        fh.write("draft counter: %s\n\n" % (draft or "absent"))
        for name, verdict, clause, fails, exp_fails, trips, writes, drc, r47 in rows:
            fh.write("%-22s %-5s clauses=%-6s f=%d x=%d r=%d w=%d r47-clauses=%s draft_rc=%s\n" % (
                name, verdict, clause or "-", len(fails), len(exp_fails), len(trips), len(writes), r47, drc))
    met = [r for r in rows if r[1] == "MEETS"]
    print("\n== %d controls: %d MISS, %d MEET%s" % (len(rows), len(rows) - len(met), len(met),
                                                   (": " + ", ".join(r[0] for r in met)) if met else ""))
    return 1 if met else 0


if __name__ == "__main__":
    sys.exit(main())
