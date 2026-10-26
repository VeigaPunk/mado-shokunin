#!/usr/bin/env python3
"""Reproduce one ExecC1Diff case outside the fuzz driver: build the tree, show it, run the pin and the reference.

  repro.py --cases minimal-cases.json --id find-type-f --work DIR [--keep]
"""
import argparse
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fuzz  # noqa: E402


def tree(root):
    out = []
    for dp, dns, fns in os.walk(root):
        dns.sort()
        for n in sorted(dns) + sorted(fns):
            p = os.path.join(dp, n)
            rel = os.path.relpath(p, root)
            st = os.lstat(p)
            mode = oct(st.st_mode & 0o7777)
            if os.path.islink(p):
                out.append("l %s %s -> %s" % (mode, rel, os.readlink(p)))
            elif os.path.isdir(p):
                out.append("d %s %s/" % (mode, rel))
            else:
                out.append("f %s %s" % (mode, rel))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.cases))
    recs = data if isinstance(data, list) else [data]
    case = None
    for r in recs:
        if r.get("id") == a.id:
            case = r.get("case", r.get("minimal"))
            break
    if case is None:
        print("no such case id")
        return 2
    work = tempfile.mkdtemp(dir=a.work, prefix="repro-")
    box = fuzz.Box(work)
    base = tempfile.mkdtemp(dir=work, prefix="t-")
    ro, rt = os.path.join(base, "o"), os.path.join(base, "t")
    for r in (ro, rt):
        fuzz.materialize(r, case)
    print("== case %s area=%s" % (a.id, case.get("area", "?")))
    print("== tree (o):")
    print(tree(ro))
    args = case.get("args", [])
    oenv = fuzz.case_env(case, ro)
    tenv = fuzz.case_env(case, rt)
    print("== env: %s" % json.dumps(oenv, sort_keys=True))
    print("== oracle argv: %s" % " ".join(box.argv(ro, oenv, False, args)))
    print("== tool argv:   %s" % " ".join(box.argv(rt, tenv, True, args)))
    o_rc, o_out = box.run(ro, oenv, False, args, 20)
    t_rc, t_out = box.run(rt, tenv, True, args, 20)
    print("== oracle rc=%d stdout=%r" % (o_rc, o_out.decode("latin-1")))
    print("== tool   rc=%d stdout=%r" % (t_rc, t_out.decode("latin-1")))
    print("== verdict: %s" % ("AGREE" if (o_rc, o_out.replace(ro.encode(), b"$ROOT")) ==
                              (t_rc, t_out.replace(rt.encode(), b"$ROOT")) else "DIFFER"))
    if a.keep:
        print("== kept: %s" % base)
    else:
        fuzz._chmod_walk(base)
        shutil.rmtree(base, ignore_errors=True)
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
