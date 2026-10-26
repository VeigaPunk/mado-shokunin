#!/usr/bin/env python3
"""capture-twice.py — two independent read-only captures of the live desktop, compared.

Runs nothing but `hyprctl clients -j` (an allowed read verb) twice. The raw bytes are
never written: each capture is hashed, projected to the ten contract fields, and the two
projections are compared byte for byte. Then rows for the four state columns are printed
so the receipt's state block can be checked against today's host.

usage: python3 capture-twice.py [--tool TOOL --rules RULES]
"""
import argparse, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = ("address", "mapped", "class", "floating", "size", "at", "monitor",
        "fullscreen", "fullscreenClient", "fullscreenHandler")


def capture():
    raw = subprocess.run(["hyprctl", "clients", "-j"], capture_output=True, check=True).stdout
    doc = json.loads(raw)
    proj = json.dumps([{k: c[k] for k in KEEP if k in c} for c in doc], indent=1) + "\n"
    return raw, doc, proj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", default=os.path.join(os.path.dirname(HERE), "..", "..", "..", "..", "tools", "mado-geometry.py"))
    ap.add_argument("--rules", default=os.path.expanduser("~/.config/hypr/gkeep.conf"))
    a = ap.parse_args()
    raws, docs, projs = [], [], []
    for _ in range(2):
        r, d, p = capture()
        raws.append(r); docs.append(d); projs.append(p)
    out = ["two captures of the same desktop, read-only (`hyprctl clients -j` x2)", ""]
    for i, (r, d, p) in enumerate(zip(raws, docs, projs), 1):
        out.append("capture %d: raw_bytes=%d raw_sha256=%s projected_sha256=%s clients=%d"
                   % (i, len(r), hashlib.sha256(r).hexdigest(), hashlib.sha256(p.encode()).hexdigest(), len(d)))
    out.append("projections identical: %s" % ("YES" if projs[0] == projs[1] else "NO"))
    out.append("state columns (class, floating, fullscreen, fullscreenClient):")
    for c in docs[0]:
        out.append("  %s %s %s %s" % (c.get("class"), c.get("floating"), c.get("fullscreen"),
                                      c.get("fullscreenClient")))
    dump = os.path.join(HERE, ".capture.json")
    open(dump, "wb").write(raws[0])
    for label in ("round-43", "landed"):
        tool = os.path.join(os.path.dirname(HERE), "..", "..", "..", "..", "tools", "mado-geometry.py")
        if label == "round-43":
            tool = os.environ.get("R43_TOOL", "")
            if not tool:
                out.append("round-43 run skipped: R43_TOOL not set")
                continue
        p = subprocess.run([sys.executable, "-I", tool, "--clients", dump, "--rules", a.rules],
                           capture_output=True, timeout=60)
        out.append("%s: rc=%d stdout_sha256=%s stderr_bytes=%d"
                   % (label, p.returncode, hashlib.sha256(p.stdout).hexdigest(), len(p.stderr)))
    os.unlink(dump)
    text = "\n".join(out) + "\n"
    open(os.path.join(HERE, "capture-twice.txt"), "w").write(text)
    print(text, end="")


if __name__ == "__main__":
    main()
