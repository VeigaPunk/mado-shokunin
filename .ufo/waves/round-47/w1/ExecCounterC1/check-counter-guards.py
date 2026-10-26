#!/usr/bin/env python3
"""Guards and non-vacuity checks for c1-r47-terminal.py: every guard must fail the way it claims to fail, and every
comparison must be able to report a mismatch (a check that cannot fail is not a check).

Usage: check-counter-guards.py --counter c1-r47-terminal.py --fixtures fixtures-placeholder.json --work DIR
Prints `GUARD <name> PASS|FAIL <detail>` lines and a final `GUARD VERDICT: PASS|FAIL (k/n)`.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(d, *args):
    p = subprocess.run(["git", "-C", d, "-c", "user.name=g", "-c", "user.email=g@example.invalid",
                        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"] + list(args),
                       capture_output=True, env=GIT_ENV)
    if p.returncode != 0:
        raise SystemExit("git %s: %s" % (" ".join(args), p.stderr.decode()[:300]))
    return p.stdout


def repo_with(work, name, tool_text):
    d = tempfile.mkdtemp(dir=work, prefix="g-%s-" % name)
    git(d, "init", "-q")
    if git(d, "rev-parse", "--show-toplevel").decode().strip() != d:
        raise SystemExit("fixture repo toplevel mismatch at %s" % d)
    if tool_text is not None:
        os.makedirs(os.path.join(d, "tools"))
        with open(os.path.join(d, "tools", "mado-terminal.py"), "w") as f:
            f.write(tool_text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "--allow-empty", "-m", name)
    return d


def run(counter, repo, rev, work, fixtures, nonce=47, extra=()):
    w = tempfile.mkdtemp(dir=work, prefix="gw-")
    cmd = [sys.executable, counter, "--repo", repo, "--rev", rev, "--work", w,
           "--fixtures", fixtures, "--nonce", str(nonce)] + list(extra)
    p = subprocess.run(cmd, capture_output=True, timeout=3600)
    return p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    cases = json.load(open(a.fixtures))
    results = []

    def record(name, ok, detail):
        results.append((name, ok))
        print("GUARD %s %s %s" % (name, "PASS" if ok else "FAIL", detail))

    good = repo_with(a.work, "empty", None)
    stub = "#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n"
    stub_repo = repo_with(a.work, "stub", stub)

    rc, out = run(a.counter, good, "HEAD", a.work, a.fixtures)
    record("tool-absent", rc == 1 and "tool=absent" in out and "TARGET_MISSED" in out, "exit=%d" % rc)

    rc, out = run(a.counter, stub_repo, "bogusrev", a.work, a.fixtures)
    record("bad-rev", rc == 2 and "SETUP" in out, "exit=%d" % rc)

    short = os.path.join(a.work, "short.json")
    json.dump(cases[:99], open(short, "w"))
    rc, out = run(a.counter, stub_repo, "HEAD", a.work, short)
    record("fewer-than-100", rc == 2 and "fewer than 100" in out, "exit=%d" % rc)

    unsafe = json.loads(json.dumps(cases[:105]))
    unsafe[3]["args"] = ["--print-delimiter=|"]
    unsafe_path = os.path.join(a.work, "unsafe.json")
    json.dump(unsafe, open(unsafe_path, "w"))
    rc, out = run(a.counter, stub_repo, "HEAD", a.work, unsafe_path)
    record("no-print-mode", rc == 2 and "print mode" in out, "exit=%d" % rc)

    escape = json.loads(json.dumps(cases[:105]))
    escape[7]["files"] = {"../outside.txt": "x\n"}
    esc_path = os.path.join(a.work, "escape.json")
    json.dump(escape, open(esc_path, "w"))
    rc, out = run(a.counter, stub_repo, "HEAD", a.work, esc_path)
    record("path-escape", rc == 2 and "escapes the case root" in out, "exit=%d" % rc)

    dup = json.loads(json.dumps(cases[:105]))
    dup[9]["id"] = dup[8]["id"]
    dup_path = os.path.join(a.work, "dup.json")
    json.dump(dup, open(dup_path, "w"))
    rc, out = run(a.counter, stub_repo, "HEAD", a.work, dup_path)
    record("duplicate-id", rc == 2 and "duplicate fixture id" in out, "exit=%d" % rc)

    bad_exp = json.loads(json.dumps(cases[:105]))
    bad_exp[5]["expect"]["stdout"] = "MUTATED-BY-GUARD-CHECK\n"
    bad_path = os.path.join(a.work, "badexpect.json")
    json.dump(bad_exp, open(bad_path, "w"))
    rc, out = run(a.counter, stub_repo, "HEAD", a.work, bad_path)
    record("oracle-vs-expect-live", rc == 1 and "oracle-vs-expect" in out,
           "fixture=%s" % bad_exp[5]["id"])

    lane_work = os.path.join(os.path.dirname(os.path.abspath(a.counter)), "guard-work")
    os.makedirs(lane_work, exist_ok=True)
    try:
        rc, out = run(a.counter, stub_repo, "HEAD", lane_work, a.fixtures)
        # the lane lives under the operator's home, so the /home refusal fires before the lane refusal; either is a
        # refusal, and the hidden-path refusal proper is exercised by work-inside-repo below
        record("work-inside-lane", rc == 2 and ("hidden path" in out or "under /home" in out),
               "exit=%d %s" % (rc, out.strip().splitlines()[-1][:90] if out.strip() else ""))
    finally:
        shutil.rmtree(lane_work, ignore_errors=True)

    inside = os.path.join(stub_repo, "w")
    os.makedirs(inside)
    rc, out = run(a.counter, stub_repo, "HEAD", inside, a.fixtures)
    record("work-inside-repo", rc == 2 and "hidden path" in out, "exit=%d" % rc)

    for label, line in (("selftest-29", "MADO_TERMINAL_SELFTEST: 29/29 passed\n"),
                        ("selftest-30", "MADO_TERMINAL_SELFTEST: 30/30 passed\n"),
                        ("selftest-mismatch", "MADO_TERMINAL_SELFTEST: 31/30 passed\n"),
                        ("selftest-unicode", "MADO_TERMINAL_SELFTEST: \u0663\u0663/33 passed\n")):
        txt = "#!/usr/bin/env python3\nimport sys\nprint(%r)\nsys.exit(0)\n" % line.rstrip("\n")
        r = repo_with(a.work, label, txt)
        rc, out = run(a.counter, r, "HEAD", a.work, a.fixtures)
        want = "selftest=ok" if label == "selftest-30" else "selftest=fail"
        record(label, want in out, "exit=%d" % rc)

    # nonce dependence of the generated clause: two nonces must not draw the same first case
    rng_repo = repo_with(a.work, "stub2", stub)
    rc1, out1 = run(a.counter, rng_repo, "HEAD", a.work, a.fixtures, nonce=1)
    rc2, out2 = run(a.counter, rng_repo, "HEAD", a.work, a.fixtures, nonce=2)
    first1 = [ln for ln in out1.splitlines() if "clause=g" in ln]
    first2 = [ln for ln in out2.splitlines() if "clause=g" in ln]
    record("nonce-dependence", bool(first1) and bool(first2) and first1[0] != first2[0],
           "nonce=1 vs 2 differ in the first generated case")

    ok = sum(1 for _, o in results if o)
    print("GUARD VERDICT: %s (%d/%d)" % ("PASS" if ok == len(results) else "FAIL", ok, len(results)))
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
