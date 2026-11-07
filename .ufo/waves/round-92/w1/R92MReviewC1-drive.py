#!/usr/bin/env python3
"""Compare the C1 candidate against the oracle labels over a case file (DRAFT, scratch only)."""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

ORACLE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-92/controls/xdgmime-oracle-r92.py"
CAND = os.environ.get("CAND", "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-92/build/mado-xdgmime.c1.py")

spec = importlib.util.spec_from_file_location("orc", ORACLE)
orc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orc)


def run_case(case, scratch):
    root = tempfile.mkdtemp(prefix="c", dir=scratch)
    try:
        orc.materialise(case, root)
        env = orc.env_of(case, root)
        args = ["python3", "-I", CAND, "--json", "--cwd", root]
        for k, v in env.items():
            args += ["--env", f"{k}={v}"]
        args += ["--"] + case["types"]
        r = subprocess.run(args, cwd=root, capture_output=True, timeout=120)
        if r.returncode != 0:
            return {"error": r.stderr.decode("utf-8", "replace").strip()[:300], "rc": r.returncode}
        doc = json.loads(r.stdout)
        return {x["type"]: {"default": x["default"], "rc": x["rc"]} for x in doc["results"]}
    finally:
        orc.restore_modes(root)
        shutil.rmtree(root, ignore_errors=True)


def main():
    path = sys.argv[1]
    only = sys.argv[2] if len(sys.argv) > 2 else None
    scratch = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.getcwd()
    doc = json.load(open(path, encoding="utf-8"))
    bad = 0
    tot = 0
    for c in doc["cases"]:
        if only and only not in c["id"]:
            continue
        got = run_case(c, scratch)
        exp = c.get("expect", {})
        for t in c["types"]:
            tot += 1
            e = exp.get(t)
            g = got.get(t) if "error" not in got else got
            if e != g:
                bad += 1
                print(f"MISMATCH {c['id']} {t}\n  expect={e!r}\n  got   ={g!r}")
    print(f"cases={tot} mismatches={bad}")


main()
