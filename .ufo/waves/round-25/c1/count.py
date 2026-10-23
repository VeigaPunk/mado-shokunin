#!/usr/bin/env python3
"""mado round 25 C1 counter v4 (attempt 3; frozen before any v4-scoring seat and before any data seat).

Why v4 (a design gap, not an observed score under v4): v1-v3 compute the expected bind table of
every generated case with the counter's own line model. A tool that transcribes that model meets
them by construction, whether or not the model is what Hyprland does. v4 keeps v3's case generator
unchanged (count-v3.py, imported and sha256-pinned below, so a seed replays v3's case trees) and
takes every expected value from Hyprland v0.56.2 itself: a nested Hyprland instance started by the
counter on a copy of the case tree, read back with `hyprctl -i <instance> binds -j`. The tool
cannot reach that oracle (its sandbox has no /run, no display socket and no network), and no
fixture id, label or cached line predicts a fresh random tree's oracle table.

PRED-C1 (v4) (same sentence in registration.md, this code and the receipt label):
  At REV, the committed bytes of tools/mado-binds.py, run in a bubblewrap sandbox (no network,
  no /run, cleared environment, HOME = a fresh case directory), reproduce exactly over all 18
  hyprctl JSON fields the bind multiset that Hyprland v0.56.2 itself builds from the same case
  tree (a nested Hyprland instance run by the counter on a copy of the tree with its exec lines
  removed, read with hyprctl binds -j), for the unperturbed snapshot of the four Hyprland config
  roots and for each of the 40 cases v3 generates (4 each of ADD, UNBIND, VARIABLE, SOURCE, GLOB,
  UNSOURCED, COMMENT, REWRITE, SYNTH and HARD), and the tool bytes contain none of the live
  capture's arg or description strings of 12 or more characters; target: cases_pass=41/41 and
  embed_hits=0.

Guards (exit 2, nothing measured): the live `hyprctl binds -j` capture changes during the snapshot
(UNSTABLE); the oracle's table for the unperturbed snapshot differs from the live capture
(ORACLE_DRIFT); a nested instance fails to answer (ORACLE_FAIL); count-v3.py bytes differ from the
pin. `V3_MODEL_AGREE` (v3's own expectation vs the oracle) is printed as a diagnostic only; it is not
part of the predicate.

Oracle input: the case tree, copied; lines matching EXEC_RE (exec, exec-once, execr, execr-once,
exec-shutdown keywords; they create no binds) removed from every text file; ORACLE_EXTRA appended
to the root config (non-bind options that stop update/donation screens). Each instance runs with a
cleared environment (PATH, HOME = the oracle copy, XDG_RUNTIME_DIR, WAYLAND_DISPLAY), in its own
process group, and is killed with that group once read. At most SLOTS instances run host-wide
(lock files under SLOT_DIR).

Usage: python3 -I count.py REV [--tool-file PATH] [--seed HEX] [--jobs N]
  REV          lane revision whose tools/mado-binds.py is measured.
  --tool-file  score this file instead of REV's tool (controls only; the receipt names it and its
               sha256).
  --seed       replay a run's case trees (default: fresh os.urandom).
  --jobs       oracle instances this run starts at once (default 4, capped by SLOTS host-wide).
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error / UNSTABLE / ORACLE_DRIFT / ORACLE_FAIL.
Reads host config bytes, runs `hyprctl binds -j` / `hyprctl instances -j` (read verbs) on the live
compositor, and starts nested Hyprland instances (wayland backend, windows on the live session)
that it kills; writes only a private temporary directory it removes, the instances' runtime
directories it removes, and lock files under SLOT_DIR.
"""
import argparse, collections, concurrent.futures, fcntl, hashlib, importlib.util, json, os, random, re, shutil
import signal, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
V3_PATH = os.path.join(HERE, "count-v3.py")
V3_SHA = "8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375"
SLOT_DIR = "/fast/scratch/hyaku/mado-r25-oracle-slots"
SLOTS = 6
EXEC_RE = re.compile(r"^\s*exec(?:r)?(?:-once|-shutdown)?\s*=")
ORACLE_EXTRA = ["", "ecosystem {", "    no_update_news = true", "    no_donation_nag = true", "}", ""]


def load_v3():
    b = open(V3_PATH, "rb").read()
    if hashlib.sha256(b).hexdigest() != V3_SHA:
        print("SETUP_ERROR count-v3.py sha256 differs from the pin")
        sys.exit(2)
    spec = importlib.util.spec_from_file_location("mado_r25_count_v3", V3_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v3 = load_v3()
die, sha, compare, brief, run_tool = v3.die, v3.sha, v3.compare, v3.brief, v3.run_tool
LANE, TOOL_PATH, TYPES, PER_TYPE = v3.LANE, v3.TOOL_PATH, v3.TYPES, v3.PER_TYPE


def strip_exec(home):
    removed = 0
    for dp, dn, fn in os.walk(home):
        for f in fn:
            p = os.path.join(dp, f)
            if os.path.islink(p) or not os.path.isfile(p):
                continue
            b = open(p, "rb").read()
            if b"\0" in b:
                continue
            try:
                t = b.decode("utf-8")
            except UnicodeDecodeError:
                continue
            lines = t.split("\n")
            keep = [l for l in lines if not EXEC_RE.match(l)]
            if len(keep) != len(lines):
                removed += len(lines) - len(keep)
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(keep))
    return removed


class Slot:
    def __enter__(self):
        os.makedirs(SLOT_DIR, exist_ok=True)
        while True:
            for i in range(SLOTS):
                fh = open(os.path.join(SLOT_DIR, "slot-%d.lock" % i), "w")
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.fh = fh
                    return self
                except OSError:
                    fh.close()
            time.sleep(0.2)

    def __exit__(self, *exc):
        fcntl.flock(self.fh, fcntl.LOCK_UN)
        self.fh.close()


def hyprctl(args, timeout=10):
    p = subprocess.run(["timeout", str(timeout), "hyprctl"] + args, capture_output=True)
    return p.returncode, p.stdout


def oracle(case_home, work):
    """Hyprland v0.56.2's own bind table for case_home (nested instance). Returns (list, error)."""
    ohome = os.path.join(work, "home")
    shutil.copytree(case_home, ohome, symlinks=False)
    strip_exec(ohome)
    root = os.path.join(ohome, ".config/hypr/hyprland.conf")
    with open(root, "a", encoding="utf-8") as fh:
        fh.write("\n".join(ORACLE_EXTRA))
    rt = os.environ.get("XDG_RUNTIME_DIR", "/run/user/%d" % os.getuid())
    env = {"PATH": "/usr/bin", "HOME": ohome, "XDG_RUNTIME_DIR": rt,
           "WAYLAND_DISPLAY": os.environ.get("WAYLAND_DISPLAY", "wayland-1")}
    with Slot():
        log = open(os.path.join(work, "hyprland.log"), "wb")
        p = subprocess.Popen(["Hyprland", "-c", root], env=env, cwd=ohome, stdin=subprocess.DEVNULL,
                             stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        sig = None
        try:
            t0 = time.time()
            while sig is None and time.time() - t0 < 40:
                if p.poll() is not None:
                    return None, "nested Hyprland exited rc=%s before answering" % p.returncode
                rc, out = hyprctl(["instances", "-j"])
                if rc == 0:
                    try:
                        for inst in json.loads(out):
                            if inst.get("pid") == p.pid:
                                sig = inst["instance"]
                    except ValueError:
                        pass
                if sig is None:
                    time.sleep(0.25)
            if sig is None:
                return None, "no instance for pid %d within 40 s" % p.pid
            prev, same, t1 = None, 0, time.time()
            while time.time() - t1 < 30:
                rc, out = hyprctl(["-i", sig, "binds", "-j"])
                if rc == 0:
                    try:
                        data = json.loads(out)
                    except ValueError:
                        data = None
                    if isinstance(data, list):
                        if out == prev:
                            same += 1
                            if same >= 2:
                                return data, ""
                        else:
                            prev, same = out, 0
                time.sleep(0.3)
            return None, "binds -j never stable within 30 s (instance %s)" % sig
        finally:
            try:
                os.killpg(p.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                p.wait(timeout=8)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                p.wait(timeout=8)
            log.close()
            if sig:
                shutil.rmtree(os.path.join(rt, "hypr", sig), ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--tool-file")
    ap.add_argument("--seed")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    rev = subprocess.run(["git", "-C", LANE, "rev-parse", "--verify", a.rev + "^{commit}"], capture_output=True, text=True)
    if rev.returncode != 0:
        die("bad REV %s" % a.rev)
    rev = rev.stdout.strip()
    me = open(os.path.abspath(__file__), "rb").read()
    print("counter v4 sha256:%s rev=%s generator count-v3.py sha256:%s" % (sha(me), rev, V3_SHA))
    tmp = tempfile.mkdtemp(prefix="mado-r25-c1v4-")
    try:
        tool = os.path.join(tmp, "tool.py")
        if a.tool_file:
            tb = open(a.tool_file, "rb").read()
            print("tool=override:%s sha256:%s" % (a.tool_file, sha(tb)))
        else:
            p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, TOOL_PATH)], capture_output=True)
            if p.returncode != 0:
                print("tool=MISSING_TOOL at %s" % rev)
                tb = None
            else:
                tb = p.stdout
                print("tool=%s@%s sha256:%s" % (TOOL_PATH, rev[:12], sha(tb)))
        if tb is not None:
            with open(tool, "wb") as fh:
                fh.write(tb)
        seed = a.seed or os.urandom(8).hex()
        print("seed=%s" % seed)
        snap0 = os.path.join(tmp, "snap0")
        raw1 = v3.live_capture()
        nfiles, digest = v3.copy_roots(os.path.expanduser("~"), snap0)
        raw2 = v3.live_capture()
        if raw1 != raw2:
            die("UNSTABLE live capture changed during snapshot", 2)
        live = json.loads(raw1)
        print("live=hyprctl binds -j sha256:%s" % sha(raw1))
        print("snapshot files=%d digest sha256:%s live_binds=%d" % (nfiles, digest, len(live)))
        embed_hits = 0
        if tb is not None:
            text = tb.decode("utf-8", errors="replace")
            strs = {e[f] for e in live for f in ("arg", "description") if isinstance(e[f], str) and len(e[f]) >= 12}
            hits = sorted(s for s in strs if s in text)
            embed_hits = len(hits)
            for s in hits[:5]:
                print("EMBED_HIT %r" % s[:60])
        # 1. Generate every case tree in v3's order (same rng stream as v3 for the same seed).
        cases = [("BASE", None)] + [(t, i) for t in TYPES for i in range(PER_TYPE)]
        rng = random.Random(int(seed, 16))
        gen = v3.Gen(rng, live)
        built = []
        for kind, i in cases:
            label = "%s%s" % (kind, "" if i is None else "-%d" % i)
            home = os.path.join(tmp, "cases", label, "home")
            shutil.copytree(snap0, home, symlinks=False)
            if kind == "BASE":
                desc, model_exp = "unperturbed", [dict(e) for e in live]
            else:
                desc, model_exp = v3.perturb(kind, rng, home, live, gen)
            built.append((label, home, desc, model_exp))
        # 2. Oracle: Hyprland's own table for every case tree.
        jobs = max(1, min(a.jobs, SLOTS))
        with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
            futs = {label: ex.submit(oracle, home, os.path.join(tmp, "oracle", label))
                    for label, home, _, _ in built}
            truth = {label: f.result() for label, f in futs.items()}
        for label, (data, err) in truth.items():
            if data is None:
                die("ORACLE_FAIL %s: %s" % (label, err), 2)
        nm, ne, missing, extra = compare(truth["BASE"][0], live)
        print("ORACLE_CHECK base_vs_live missing=%d extra=%d" % (nm, ne))
        if nm or ne:
            for k in list(missing)[:3]:
                print("    live-only   " + brief(k))
            for k in list(extra)[:3]:
                print("    oracle-only " + brief(k))
            die("ORACLE_DRIFT the nested instance's table for the unperturbed snapshot differs from the live capture", 2)
        # 3. Score the tool against the oracle.
        npass = agree = 0
        for label, home, desc, model_exp in built:
            exp = truth[label][0]
            m_ok = compare(model_exp, exp)[:2] == (0, 0)
            agree += m_ok
            if tb is None:
                print("CASE %-12s FAIL tool absent (%s) v3_model=%s" % (label, desc, "agree" if m_ok else "differs"))
                continue
            got, err = run_tool(tool, home)
            if got is None:
                print("CASE %-12s FAIL %s (%s) v3_model=%s" % (label, err, desc, "agree" if m_ok else "differs"))
                continue
            nm, ne, missing, extra = compare(got, exp)
            ok = nm == 0 and ne == 0
            npass += ok
            print("CASE %-12s %s missing=%d extra=%d oracle_binds=%d (%s) v3_model=%s" % (
                label, "PASS" if ok else "FAIL", nm, ne, len(exp), desc, "agree" if m_ok else "differs"))
            for k in list(missing)[:2]:
                print("    missing " + brief(k))
            for k in list(extra)[:2]:
                print("    extra   " + brief(k))
        print("V3_MODEL_AGREE %d/%d (diagnostic, not the predicate)" % (agree, len(built)))
        met = npass == len(built) and embed_hits == 0
        print("PRED-C1 (v4) cases_pass=%d/%d embed_hits=%d verdict=%s" % (
            npass, len(built), embed_hits, "TARGET_MET" if met else "TARGET_MISSED"))
        return 0 if met else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
