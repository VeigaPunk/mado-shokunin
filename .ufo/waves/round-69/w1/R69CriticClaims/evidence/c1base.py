#!/usr/bin/env python3
"""Independent re-run: apply the three frozen recipes to the r68 harness (base rev) and
to the frozen r69 prototype; count kills by the counter's stated rule (nonzero --selftest)."""
import os, subprocess, sys, hashlib, shutil

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = os.path.dirname(os.path.abspath(__file__))
BASE = "04093b83f73a841117d3b31dbb2a6063f4f2a454"
FREEZE = "789a87f1a667b43dd759222a2f048bf8f75b43ce"

R1_OLD = (b"            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)\n"
          b"                             and forged_credit(mr_rc, mr_marker))")
R1_NEW = b"            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker))"
R2_OLD = b"        mz_killed = mz_rc != 0"
R2_NEW = b'        mz_killed = mz_rc != 0 or mz_summary == "none"'
R3_OLD = b"    subprocess.run = _no_spawn"
R3_NEW = b"    pass  # spawn guard removed by recipe"
RECIPES = [("R1", R1_OLD, R1_NEW), ("R2", R2_OLD, R2_NEW), ("R3", R3_OLD, R3_NEW)]


def blob(rev, path):
    return subprocess.check_output(["git", "-C", LANE, "cat-file", "-p", "%s:%s" % (rev, path)])


def lastline(out):
    lines = [l for l in out.decode("utf-8", "replace").splitlines() if l.strip()]
    return lines[-1] if lines else "(no output)"


def run_subject(tag, src, scratch):
    os.makedirs(scratch, exist_ok=True)
    path = os.path.join(scratch, tag + ".py")
    open(path, "wb").write(src)
    work = os.path.join(scratch, "w-" + tag)
    env = {"PATH": "/usr/bin:/bin", "HOME": os.path.join(scratch, "home-" + tag),
           "LC_ALL": "C", "PYTHONDONTWRITEBYTECODE": "1"}
    os.makedirs(env["HOME"], exist_ok=True)
    counts = []
    for name, old, new in RECIPES:
        counts.append((name, src.count(old)))
    r = subprocess.run([sys.executable, path, "--selftest", "--scratch-root", work],
                       cwd=scratch, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=1800)
    killed = []
    per = []
    for name, old, new in RECIPES:
        c = src.count(old)
        if c != 1:
            per.append((name, c, "n/a", "n/a"))
            continue
        mut = src.replace(old, new)
        mp = os.path.join(scratch, "%s-%s.py" % (tag, name))
        open(mp, "wb").write(mut)
        mr = subprocess.run([sys.executable, mp, "--selftest", "--scratch-root",
                             os.path.join(scratch, "wm-%s" % name)],
                            cwd=scratch, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=1800)
        k = mr.returncode != 0
        killed.append(k)
        per.append((name, c, mr.returncode, lastline(mr.stdout + mr.stderr)))
    print("== %s sha=%s" % (tag, hashlib.sha256(src).hexdigest()))
    print("   unmutated rc=%d %s" % (r.returncode, lastline(r.stdout + r.stderr)))
    for name, c, rc, line in per:
        print("   %s occurrences=%d rc=%s killed=%s | %s"
              % (name, c, rc, "yes" if (rc != "n/a" and rc != 0) else "no", line))
    print("   KILLED=%d/3" % sum(killed))
    return sum(killed)


def main():
    sub = os.path.join(S, "c1")
    shutil.rmtree(sub, ignore_errors=True)
    os.makedirs(sub)
    base_src = blob(BASE, "quality/counters/c1-r68-landing-controls.py")
    proto_src = blob(FREEZE, ".ufo/waves/round-69/proto/c1-r69-landing-controls.proto.py")
    kb = run_subject("r68base", base_src, os.path.join(sub, "base"))
    kp = run_subject("r69proto", proto_src, os.path.join(sub, "proto"))
    print("RESULT base_killed=%d/3 proto_killed=%d/3" % (kb, kp))


if __name__ == "__main__":
    main()
