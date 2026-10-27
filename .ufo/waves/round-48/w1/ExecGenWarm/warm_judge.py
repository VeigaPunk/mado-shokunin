#!/usr/bin/env python3
"""warm_judge.py - seat-local driver for round-48 C1 clause g v2 (ExecGenWarm).

Builds each `gen_warm.gen_warm_case()` case in the round-47 bwrap geometry, primes the pinned resolver, applies the
`after` mutations, and records:

  * determinism: the prime + scored run 3 times on fresh trees (rc, root-normalized stdout, measured cache verdict,
    root+hash-normalized cache bytes);
  * the warm oracle answer vs the cold answer (a third tree, never primed) and vs the round-47 tool
    (`tools/mado-terminal.py` at the round's base rev, cold-only), which is how many cases the v1 instrument misses;
  * the measured cache verdict (XTE_DEBUG=1 stderr: "cache is actual" / "cache is out-of-date" / "invalid cache data" /
    "no cache data"; "disabled" from a false XTE_CACHE_ENABLED in the scored env).

Prime mechanism (measured, see receipts/prime-mechanism.txt): the round-47 argv (`--unshare-all`) makes the pin PID 1
of a new PID namespace, and the resolver's `save_cache "$1" &` is killed with the namespace - no cache ever appears.
The prime therefore runs the pin through a `/bin/bash` wrapper that stays alive until the cache file is complete, with
`sleep` added to `/oracle/bin`; the sandbox geometry is otherwise the round-47 one byte for byte.

Seat-local; not part of the frozen instrument. Stdlib only. Scratch is whatever --work names (never /tmp by default).
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_warm  # noqa: E402

C1 = gen_warm.R47
BASE_REV = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
LANE = os.path.realpath(os.path.join(HERE, *[".."] * 5))
TOOL_REL = "tools/mado-terminal.py"
SENTINEL = "\x1eEND_OF_EXEC_USEP\n"

PRIME_SH = """#!/bin/bash
# Seat-local prime wrapper: the resolver saves its cache in the BACKGROUND and the round-47 sandbox makes the
# resolver PID 1 of a new PID namespace, so the writer is killed when the resolver exits. Stall the namespace's init
# until the cache file is complete, then hand the resolver's exit status back.
/oracle/xdg-terminal-exec "$@"
rc=$?
i=0
while [ "$i" -lt 80 ]; do
	[ -s "${XDG_CACHE_HOME}/xdg-terminal-exec" ] && break
	sleep 0.01
	i=$((i + 1))
done
exit "$rc"
"""


class Box(C1.Box):
    """The round-47 sandbox plus a /oracle/prime.sh wrapper and `sleep`."""

    def __init__(self, work, tool_path=None):
        C1.Box.__init__(self, work, tool_path)
        self.prime_sh = os.path.join(work, "prime.sh")
        with open(self.prime_sh, "w") as fh:
            fh.write(PRIME_SH)
        os.chmod(self.prime_sh, 0o755)
        shutil.copy(os.path.realpath("/usr/bin/sleep"), os.path.join(self.bin, "sleep"))

    def prime_argv(self, root, env, args):
        argv = self.argv(root, env, None, args)
        i = argv.index("--chdir")
        argv[i:i] = ["--ro-bind", self.prime_sh, "/oracle/prime.sh"]
        tail = len(args) + 1
        if argv[-tail] != "/oracle/xdg-terminal-exec":
            raise SystemExit("prime argv: pin not at -%d (%r)" % (tail, argv[-tail:]))
        argv[-tail:] = ["/bin/bash", "/oracle/prime.sh"] + list(args)
        return argv

    def runx(self, root, env, args, timeout=60, prime=False):
        argv = self.prime_argv(root, env, args) if prime else self.argv(root, env, None, args)
        p = subprocess.run(argv, capture_output=True, timeout=timeout, env={"PATH": "/usr/bin"})
        return (p.returncode, p.stdout.decode("utf-8", "surrogateescape"),
                p.stderr.decode("utf-8", "surrogateescape"))


# ------------------------------------------------------------------------------------------------ tree helpers
def pin_tree(root, mt):
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for name in filenames + dirnames:
            try:
                os.utime(os.path.join(dirpath, name), (mt, mt), follow_symlinks=False)
            except OSError:
                pass
        try:
            os.utime(dirpath, (mt, mt))
        except OSError:
            pass


def tokens(text, root, cache_hash):
    return (text.replace("$ROOT", root).replace("$CACHE_HASH", cache_hash)
            .replace("$USEP", "\x1f").replace("$RS", "\x1e"))


def write_file(path, text):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8", "surrogateescape"))


def apply_cache(root, ops, cache_hash):
    p = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
    if not os.path.isfile(p):
        return False
    lines = open(p, encoding="utf-8", errors="surrogateescape").read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    for op in ops if isinstance(ops, list) else [ops]:
        k = op["op"]
        if k == "set":
            i = int(op["line"]) - 1
            while len(lines) <= i:
                lines.append("")
            lines[i] = tokens(op["text"], root, cache_hash).replace("\n", "")
        elif k == "append":
            lines += [tokens(x, root, cache_hash) for x in op["lines"]]
        elif k == "truncate":
            lines = lines[:int(op["keep"])]
        elif k == "write":
            lines = tokens(op["text"], root, cache_hash).split("\n")
            if lines and lines[-1] == "":
                lines.pop()
        else:
            raise SystemExit("bad cache op %r" % k)
    open(p, "wb").write(("\n".join(lines) + "\n").encode("utf-8", "surrogateescape"))
    return True


def mutate(root, case, cache_hash):
    after = case.get("after") or {}
    for rel, text in (after.get("files") or {}).items():
        p = os.path.join(root, rel)
        if text is None:
            if os.path.isdir(p) and not os.path.islink(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.lexists(p):
                os.unlink(p)
        elif rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
        else:
            write_file(p, tokens(text, root, cache_hash))
    for rel in after.get("exec_remove") or []:
        p = os.path.join(root, rel)
        if os.path.lexists(p):
            os.unlink(p)
    for rel in after.get("exec_add") or []:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            write_file(p, "#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    if after.get("cache"):
        apply_cache(root, after["cache"], cache_hash)
    mt = after.get("mtime", case.get("mtime"))
    if mt is not None:
        pin_tree(root, mt)


def build(box, case, prime_it):
    """Materialize one tree; prime it if asked. Returns (root, workdir, prime_out)."""
    d = tempfile.mkdtemp(dir=box.work, prefix="t-")
    root = os.path.join(d, "r")
    C1.materialize(root, case)
    if case.get("mtime") is not None:
        pin_tree(root, case["mtime"])
    pout = None
    if "cache" in case:
        write_file(os.path.join(root, ".rw", "cache", "xdg-terminal-exec"), tokens(case["cache"], root, ""))
    elif prime_it:
        penv = C1.case_env(case, root, "C.UTF-8")
        for k, v in (case.get("prime", {}).get("env") or {}).items():
            penv[k] = tokens(v, root, "")
        pout = box.runx(root, penv, case["prime"]["args"], prime=True)
        complete = False
        for _ in range(200):
            try:
                data = open(os.path.join(root, ".rw", "cache", "xdg-terminal-exec"), "rb").read()
            except OSError:
                data = b""
            if data.endswith(SENTINEL.encode()):
                complete = True
                break
        pout = (pout[0], pout[1], pout[2], complete)
    cache = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
    chash = ""
    try:
        first = open(cache, "rb").read().decode("utf-8", "surrogateescape").split("\n", 1)[0]
        chash = first
    except OSError:
        pass
    mutate(root, case, chash)
    return root, d, pout, cache_bytes(root)


def scored_env(case, root):
    env = C1.case_env(case, root, "C.UTF-8")
    for k, v in ((case.get("after") or {}).get("env") or {}).items():
        env[k] = tokens(v, root, "")
    return env


FALSE_WORDS = ("false", "0", "no", "False", "FALSE", "No", "NO")


def disabled_flag(env):
    return str(env.get("XTE_CACHE_ENABLED", "true")).strip() in FALSE_WORDS


def classify(err, env):
    if disabled_flag(env):
        return "disabled"
    for needle, verdict in (("cache is actual", "hit"), ("cache is out-of-date", "stale"),
                            ("invalid cache data", "invalid"), ("no cache data", "absent"),
                            ("reached cache line limit", "invalid")):
        if needle in err:
            return verdict
    return "?"


def norm(text, root):
    return text.replace(root, "$ROOT")


def norm_cache(data, root):
    if data is None:
        return None
    lines = data.decode("utf-8", "surrogateescape").replace(root, "$ROOT").split("\n")
    if lines:
        lines[0] = "<HASH>"
    return "\n".join(lines)


def cache_bytes(root):
    p = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
    try:
        return open(p, "rb").read()
    except OSError:
        return None


def one_run(box, case, prime_it):
    """Prime (or write the literal cache), mutate, run the pin with XTE_DEBUG=1."""
    root, d, pout, cbytes = build(box, case, prime_it)
    try:
        env = scored_env(case, root)
        env["XTE_DEBUG"] = "1"
        rc, out, err = box.runx(root, env, case["args"])
        verdict = classify(err, env)
        return {"rc": rc, "out": norm(out, root), "verdict": verdict,
                "cache": norm_cache(cbytes, root), "prime": pout}
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------------------------------------------------ receipts
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=4801)
    ap.add_argument("--work", required=True)
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--probe-only", action="store_true")
    a = ap.parse_args()
    work = os.path.realpath(a.work)
    os.makedirs(work, exist_ok=True)
    os.makedirs(a.receipts, exist_ok=True)
    for h in (LANE, os.path.dirname(LANE)):
        if work == h or work.startswith(h + "/"):
            raise SystemExit("work inside %s" % h)

    # the round-47 tool, pinned at the round's base revision
    blob = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (BASE_REV, TOOL_REL)],
                          capture_output=True, check=True).stdout
    tool = os.path.join(work, "tool-r47.py")
    open(tool, "wb").write(blob)
    tool_sha = hashlib.sha256(blob).hexdigest()
    pin_sha = hashlib.sha256(open(C1.PIN_PATH, "rb").read()).hexdigest()
    with open(os.path.join(a.receipts, "env.txt"), "w") as fh:
        fh.write("seat=ExecGenWarm round=48 wave=w1\n")
        fh.write("base_rev=%s\n" % BASE_REV)
        fh.write("tool=%s sha256=%s bytes=%d\n" % (TOOL_REL, tool_sha, len(blob)))
        fh.write("pin=%s sha256=%s\n" % (os.path.realpath(C1.PIN_PATH), pin_sha))
        fh.write("python=%s\n" % sys.version.split()[0])
        fh.write("bwrap=%s strace=%s\n" % (shutil.which("bwrap"), shutil.which("strace")))
        fh.write("gen_warm.py sha256=%s\n" % hashlib.sha256(open(os.path.join(HERE, "gen_warm.py"), "rb").read()).hexdigest())

    box = Box(work, tool)

    if a.probe_only:
        probe(box, a.receipts)
        return 0

    rng = random.Random(a.seed)
    cases = [gen_warm.gen_warm_case(rng, k) for k in range(a.n)]
    for c in cases:
        gen_warm.check_case(c)

    det_bad, prime_bad, mix, rows = [], [], {}, []
    prime_by_design = 0
    fam = {}
    miss, tool_misses, tool_cold_mismatch, div = [], [], [], 0
    examples = []
    for case in cases:
        cid = case["id"]
        family = case["class"].split(":", 1)[1]
        runs = [one_run(box, case, True) for _ in range(3)]
        key = [(r["rc"], r["out"], r["verdict"], r["cache"]) for r in runs]
        if len(set(map(repr, key))) != 1:
            det_bad.append((cid, family, [repr(k) for k in key]))
        warm = runs[0]
        by_design = disabled_flag((case.get("prime") or {}).get("env") or {})
        if "prime" in case and not by_design and not (warm["prime"] and warm["prime"][3]):
            prime_bad.append((cid, family))
        prime_by_design += 1 if (by_design and "prime" in case) else 0
        v = warm["verdict"]
        mix[v] = mix.get(v, 0) + 1
        fam.setdefault(family, {}).setdefault(v, 0)
        fam[family][v] += 1

        # the tool tree: primed and mutated exactly like the oracle tree
        root, d, _p, _c = build(box, case, True)
        try:
            t_rc, t_out = box.run(root, scored_env(case, root), True, ["print"] + list(case["args"]))
            t_out = norm(t_out, root)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        # the cold tree: same case, never primed (what a cache-less resolver answers)
        croot, cd, _p, _c = build(box, case, False)
        try:
            c_rc, c_out, _err = box.runx(croot, scored_env(case, croot), case["args"])
            c_out = norm(c_out, croot)
        finally:
            shutil.rmtree(cd, ignore_errors=True)

        warm_eq_cold = (warm["rc"], warm["out"]) == (c_rc, c_out)
        div += 0 if warm_eq_cold else 1
        tool_ok = (t_rc, t_out) == (warm["rc"], warm["out"])
        tool_eq_cold = (t_rc, t_out) == (c_rc, c_out)
        if not tool_ok:
            miss.append(cid)
            tool_misses.append((cid, family, warm["verdict"]))
        if not tool_eq_cold:
            tool_cold_mismatch.append((cid, family))
        if not tool_ok and len(examples) < 8:
            examples.append("%s %s verdict=%s\n  pin   rc=%d out=%r\n  tool  rc=%d out=%r"
                            % (cid, family, warm["verdict"], warm["rc"], warm["out"][:200],
                               t_rc, t_out[:200]))
        rows.append("%s %-28s pin=%-8s warm-vs-cold=%-7s tool=%s prime=%s"
                    % (cid, family, warm["verdict"], "same" if warm_eq_cold else "DIFFER",
                       "match" if tool_ok else "MISS", "ok" if ("prime" not in case or
                                                               (warm["prime"] and warm["prime"][3])) else "FAIL"))

    total = len(cases)
    with open(os.path.join(a.receipts, "determinism.txt"), "w") as fh:
        fh.write("cases=%d seed=%d runs=3 (fresh tree per run: prime -> after -> scored pin, XTE_DEBUG=1)\n" % (total, a.seed))
        fh.write("compared: (rc, root-normalized stdout, measured verdict, root+hash-normalized cache bytes)\n")
        fh.write("identical=%d/%d\n" % (total - len(det_bad), total))
        for cid, family, ks in det_bad:
            fh.write("MISMATCH %s %s\n%s\n" % (cid, family, "\n".join(ks)))
        fh.write("prime-failures=%d/%d (plus %d primes that ran with XTE_CACHE_ENABLED=false: no cache by design)\n"
                 % (len(prime_bad), sum(1 for c in cases if "prime" in c), prime_by_design))
        for cid, family in prime_bad:
            fh.write("PRIME-FAIL %s %s\n" % (cid, family))

    with open(os.path.join(a.receipts, "mix.txt"), "w") as fh:
        fh.write("measured verdicts over %d generated cases (XTE_DEBUG=1 stderr of the scored pin run)\n" % total)
        for k in sorted(mix):
            fh.write("verdict %-9s %d\n" % (k, mix[k]))
        fh.write("warm answer differs from cold answer: %d/%d\n" % (div, total))
        fh.write("\nper family (generator label -> measured verdicts):\n")
        for f in sorted(fam):
            fh.write("  %-30s %s\n" % (f, " ".join("%s=%d" % (k, v) for k, v in sorted(fam[f].items()))))

    with open(os.path.join(a.receipts, "base-tool-miss.txt"), "w") as fh:
        fh.write("tool=%s at %s sha256=%s\n" % (TOOL_REL, BASE_REV, tool_sha))
        fh.write("missed=%d/%d (tool stdout+rc != warm pin stdout+rc, roots normalized)\n" % (len(miss), total))
        fh.write("tool equals the cold answer: %d/%d\n" % (total - len(tool_cold_mismatch), total))
        for cid, family in tool_cold_mismatch:
            fh.write("TOOL-NOT-COLD %s %s\n" % (cid, family))
        by_fam = {}
        for cid, family, v in tool_misses:
            by_fam.setdefault(family, []).append("%s(%s)" % (cid, v))
        fh.write("\nmisses by family:\n")
        for f in sorted(by_fam):
            fh.write("  %-30s %3d  %s\n" % (f, len(by_fam[f]), " ".join(sorted(by_fam[f]))))
        fh.write("\nexamples:\n" + "\n".join(examples) + "\n")

    with open(os.path.join(a.receipts, "cases.txt"), "w") as fh:
        fh.write("\n".join(rows) + "\n")
    with open(os.path.join(a.receipts, "cases-sample.json"), "w") as fh:
        json.dump(cases[:12], fh, indent=1, sort_keys=True)
        fh.write("\n")
    probe(box, a.receipts)
    print("cases=%d identical=%d/%d prime_fail=%d missed=%d/%d mix=%s"
          % (total, total - len(det_bad), total, len(prime_bad), len(miss), total, mix))
    return 0


def probe(box, receipts):
    """Receipt: the round-47 argv kills the background save; the wrapper prime survives and writes it."""
    case = {"id": "probe", "class": "probe",
            "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                    "XDG_DATA_HOME": "$ROOT/home/.local/share",
                    "XDG_DATA_DIRS": "$ROOT/opt/share:$ROOT/usr/share",
                    "XDG_CURRENT_DESKTOP": "Hyprland"},
            "files": {"usr/share/applications/foot.desktop":
                      "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\n"},
            "exec": ["bin/foot"], "args": ["--print-cmd"], "mtime": gen_warm.MT_ANCHOR,
            "prime": {"args": ["--print-cmd"]}}
    lines = []
    for label, wrapped in (("direct (round-47 argv, resolver runs unwrapped)", False),
                           ("wrapper prime (/oracle/prime.sh holds the namespace)", True)):
        seen = []
        for _ in range(3):
            d = tempfile.mkdtemp(dir=box.work, prefix="probe-")
            root = os.path.join(d, "r")
            try:
                C1.materialize(root, case)
                pin_tree(root, case["mtime"])
                env = C1.case_env(case, root, "C.UTF-8")
                rc, out, _err = box.runx(root, env, case["prime"]["args"], prime=wrapped)
                cache = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
                first = cache_bytes(root)
                time.sleep(0.5)                      # host-side grace: a live writer would have finished by now
                second = cache_bytes(root)
                state = ("absent" if not first and not second else
                         "complete" if second and second.endswith(SENTINEL.encode()) else "partial")
                seen.append("stdout=%r/rc=%d/cache=%s(+0.5s=%s)" % (out[:12], rc, state,
                                                                    "absent" if not second else "present"))
            finally:
                shutil.rmtree(d, ignore_errors=True)
        lines.append("%s: %s" % (label, "; ".join(seen)))
    with open(os.path.join(receipts, "prime-mechanism.txt"), "w") as fh:
        fh.write("sandbox: the round-47 Box.argv (quality/counters/c1-r47-terminal.py:Box.argv) verbatim; the wrapper\n"
                 "prime only adds `--ro-bind <work>/prime.sh /oracle/prime.sh` and runs `/bin/bash /oracle/prime.sh\n"
                 "<prime args>`, with `sleep` copied into /oracle/bin. 3 repetitions each, fresh tree per run.\n\n")
        fh.write("\n".join(lines) + "\n")
        fh.write("\nThe round-47 argv uses --unshare-all, so the resolver is PID 1 of a new PID namespace; the kernel\n"
                 "kills the rest of the namespace when PID 1 exits, so its background `save_cache \"$1\" &` never\n"
                 "writes a cache. The wrapper keeps PID 1 (`/bin/bash`) alive until the cache file is complete.\n"
                 "A v2 counter must prime this way (or equivalently hold the namespace open); otherwise the warm\n"
                 "path of the pin is unreachable inside the frozen sandbox and every warm fixture would be judged\n"
                 "against a cold oracle.\n")


if __name__ == "__main__":
    sys.exit(main())
