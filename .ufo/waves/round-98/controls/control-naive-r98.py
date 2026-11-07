#!/usr/bin/env python3
"""Round-98 C1 do-nothing control: the cheapest models that skip the claimed work.

Scores two no-work models against the installed `gio launch` on a probe family built here:
  A. naive-split: one launch, argv = Exec.split()  (no quoting, no field codes, no shell grammar)
  B. no-expansion: one launch, argv = Exec.split() with each field-code token left literal
Both must score strictly fewer than the total (the declaration's control clause).

The oracle records the SEQUENCE of spawned processes: the probe appends one `@@@ <argc>` + `A<i>=`
block per spawn to `$0.out`, and the harness waits until the file stops changing.

Read-only: builds every fixture under --dir, never touches a host application.
"""
import argparse, base64, json, os, shutil, subprocess, sys, time

PROBE = """#!/bin/sh
{ printf '@@@ %s\\n' "$#"; printf 'P0=%s\\n' "$0"; i=1; for a in "$@"; do printf 'A%d=%s\\n' "$i" "$a"; i=$((i+1)); done; } >> "$0.out"
"""

CASES = [
    ("plain-01", "plain", "{probe} one two", [], {}),
    ("plain-02", "plain", "{probe} one", ["a.txt"], {"a.txt": b"a\n"}),
    ("plain-03", "plain", "{probe} one", ["a.txt", "b.txt"], {"a.txt": b"a\n", "b.txt": b"b\n"}),
    ("f-01", "f", "{probe} %f", ["a.txt"], {"a.txt": b"a\n"}),
    ("f-02", "f", "{probe} %f", [], {}),
    ("f-03", "f", "{probe} %f", ["a.txt", "b.txt"], {"a.txt": b"a\n", "b.txt": b"b\n"}),
    ("F-01", "F", "{probe} pre %F post", ["a.txt", "b.txt"], {"a.txt": b"a\n", "b.txt": b"b\n"}),
    ("F-02", "F", "{probe} %F", [], {}),
    ("u-01", "u-file", "{probe} %u", ["a.txt"], {"a.txt": b"a\n"}),
    ("u-02", "u-uri", "{probe} %u", ["http://example.invalid/x"], {}),
    ("U-01", "U-mixed", "{probe} %U", ["a.txt", "http://example.invalid/y"], {"a.txt": b"a\n"}),
    ("d-01", "d", "{probe} %d", ["sub/a.txt"], {"sub/a.txt": b"a\n"}),
    ("n-01", "n", "{probe} %n", ["sub/a.txt"], {"sub/a.txt": b"a\n"}),
    ("i-01", "i", "{probe} %i end", ["a.txt"], {"a.txt": b"a\n"}),
    ("c-01", "c", "{probe} %c", [], {}),
    ("k-01", "k", "{probe} %k", [], {}),
    ("pct-01", "pct", "{probe} 100%% done", [], {}),
    ("pct-02", "pct", "{probe} tail%", [], {}),
    ("bad-01", "bad", "{probe} %z end", [], {}),
    ("quote-01", "quote", '{probe} "a b" c', [], {}),
    ("quote-02", "quote", "{probe} a\\ b c", [], {}),
    ("path-01", "path", "{probe} %f", ["a b.txt"], {"a b.txt": b"a\n"}),
    ("path-02", "path", "{probe} %f", ["a'b.txt"], {"a'b.txt": b"a\n"}),
]


def build(root, cid, exec_t, args, files):
    d = os.path.join(root, cid)
    os.makedirs(d, exist_ok=True)
    probe = os.path.join(d, "probe.sh")
    with open(probe, "w") as f:
        f.write(PROBE)
    os.chmod(probe, 0o755)
    for rel, data in files.items():
        p = os.path.join(d, rel)
        if os.path.dirname(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    desktop = os.path.join(d, "t.desktop")
    with open(desktop, "w") as f:
        f.write("[Desktop Entry]\nType=Application\nName=Demo App\nIcon=demo-icon\nExec="
                + exec_t.replace("{probe}", probe) + "\n")
    argv = [a if a.startswith("http") else os.path.join(d, a) for a in args]
    return d, desktop, probe, argv


def oracle(desktop, argv):
    out = desktop.rsplit("/", 1)[0] + "/probe.sh.out"
    if os.path.exists(out):
        os.unlink(out)
    env = {"LC_ALL": "C", "HOME": desktop.rsplit("/", 2)[0] + "/h", "PATH": "/usr/bin:/bin"}
    r = subprocess.run(["/usr/bin/gio", "launch", desktop] + argv, env=env,
                       capture_output=True, timeout=20)
    # settle: wait until the out file stops changing
    last, stable, t0 = None, 0, time.time()
    while time.time() - t0 < 8:
        cur = os.path.getsize(out) if os.path.exists(out) else -1
        if cur == last and cur >= 0:
            stable += 1
            if stable >= 4:
                break
        else:
            stable = 0
        last = cur
        time.sleep(0.05)
    if r.returncode != 0 or not os.path.exists(out):
        return {"error": "refused", "rc": r.returncode,
                "stderr": r.stderr.decode("utf-8", "replace")[:200]}
    launches = []
    for line in open(out).read().splitlines():
        if line.startswith("@@@ "):
            launches.append([None] * (int(line[4:]) + 1))
        elif line.startswith("P0="):
            launches[-1][0] = line[3:]
        elif line.startswith("A") and "=" in line:
            idx = int(line[1:line.index("=")])
            launches[-1][idx] = line[line.index("=") + 1:]
    return {"launches": len(launches), "argv": launches}


def naive(exec_t, probe, args):
    return {"launches": 1, "argv": [exec_t.replace("{probe}", probe).split()]}


def noexp(exec_t, probe, args):
    return {"launches": 1, "argv": [exec_t.replace("{probe}", probe).split()]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.dir)
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(os.path.join(root, "h"), exist_ok=True)
    rows = []
    na = nb = tot = 0
    for cid, cls, ex, args, files in CASES:
        d, desktop, probe, argv = build(root, cid, ex, args, files)
        exp = oracle(desktop, argv)
        tot += 1
        for name, fn, ctr in (("naive", naive, "A"), ("noexp", noexp, "B")):
            got = fn(ex, probe, args)
            ok = exp.get("argv") == got.get("argv") and exp.get("launches") == got.get("launches")
            if ok:
                if ctr == "A":
                    na += 1
                else:
                    nb += 1
            rows.append({"id": cid, "class": cls, "model": name, "match": ok,
                         "expected": exp, "got": got})
    with open(a.out, "w") as f:
        json.dump({"cases": tot, "naive_correct": na, "noexp_correct": nb, "rows": rows}, f, indent=1)
    print("CONTROL: cases=%d naive_correct=%d noexp_correct=%d" % (tot, na, nb))
    return 0 if na < tot and nb < tot else 1


if __name__ == "__main__":
    sys.exit(main())
