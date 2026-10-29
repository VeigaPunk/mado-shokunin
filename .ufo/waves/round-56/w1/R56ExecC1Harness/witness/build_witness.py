#!/usr/bin/env python3
"""Build the C1 WITNESS tree used to test r56_ctl_c1.py before the real entry exists.

    python3 -I build_witness.py --repo LANE --src-rev REV --out DIR [--counter-from PATH]

DIR becomes a git repo with one commit holding: the frozen tables, the pins, corpus/README.md and
corpus/SOURCES.md at --src-rev plus an index row, registry rows S383-S390 and a generated witness
entry (propositions share an identifier token with their quote and use only quote numbers).
Prints the commit sha. Nothing here is a claim about Hyprland: the propositions are lexical fillers
that satisfy the registered grammar, exactly like the L1 witness of receipts/witness.txt.
"""
import argparse, json, os, re, subprocess, sys
from pathlib import Path

TABLES = ".ufo/waves/round-56/frozen-tables.json"
ID_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")


def sh(*a, inp=None, cwd=None):
    env = {"PATH": os.environ["PATH"], "HOME": str(cwd or "/"), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
    p = subprocess.run(a, input=inp, capture_output=True, cwd=cwd, env=env)
    if p.returncode:
        sys.exit("fail %s: %s" % (a[:4], p.stderr.decode()))
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--src-rev", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    sh("git", "-C", str(out), "init", "-q", "-b", "main")
    assert os.path.realpath(sh("git", "-C", str(out), "rev-parse", "--show-toplevel").decode().strip()) == os.path.realpath(str(out))
    tar = sh("git", "-C", a.repo, "archive", "--format=tar", a.src_rev, "--", TABLES, ".ufo/waves/round-56/fetch", "corpus/README.md", "corpus/SOURCES.md")
    sh("tar", "-x", "-C", str(out), inp=tar)
    c1 = json.loads((out / TABLES).read_bytes())["c1"]
    entry = c1["entry"]

    # registry rows S383-S390 (11 cells: id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by)
    by_sid = {}
    for r in c1["k"]:
        by_sid.setdefault(r["sid"], []).append(r["line"])
    rows = []
    for sid, pin in c1["rows"].items():
        suffix = c1["pin_suffix"][pin]
        base = suffix.rsplit("/", 1)[-1]
        if pin.startswith("Hyprland-"):
            url = "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/%s" % (c1["commit"], suffix)
            kind = "code"
        else:
            url = "https://man7.org/linux/man-pages/%s" % suffix
            kind = "doc"
        ls = by_sid[sid]
        anchor = "%s:%d-%d" % (base, min(ls), max(ls) + 1) if max(ls) > min(ls) else "%s:%d" % (base, ls[0])
        rows.append("| %s | witness row for %s - %s | %s | A | witness scope | %s @ witness | witness teaches | mined | 2026-10-28 | on-release | %s |"
                    % (sid, base, url, kind, anchor, entry))
    sp = out / "corpus/SOURCES.md"
    txt = sp.read_text()
    assert not txt.endswith("\n\n")
    sp.write_text(txt.rstrip("\n") + "\n" + "\n".join(rows) + "\n")

    rp = out / "corpus/README.md"
    rt = rp.read_text().split("\n")
    i = next(k for k, l in enumerate(rt) if l.startswith("| `knowledge/"))
    rt.insert(i, "| `%s` (WITNESS) | witness index row | S383-S390 |" % entry.replace("corpus/", "", 1))
    rp.write_text("\n".join(rt))

    # entry
    L = ["# Witness: Hyprland config auto-reload", "",
         "source: " + " ".join(sorted(c1["rows"])),
         "verified-at: 2026-10-28", "recheck: on-release", "", "| id | proposition | src | pin:line | quote |", "|---|---|---|---|---|"]
    for r in c1["k"] + c1["h"]:
        tok = ID_RE.findall(r["quote"])[0]
        pre = "Row %s witnesses the identifier %s in the pinned line for this entry" % (r["id"], tok)
        src = r["sid"] if "sid" in r else "host"
        L.append("| %s | %s | %s | %s:%d | `%s` |" % (r["id"], pre, src, r["pin"], r["line"], r["quote"]))
    L.append("")
    ep = out / entry
    ep.parent.mkdir(parents=True, exist_ok=True)
    ep.write_text("\n".join(L))
    sh("git", "-C", str(out), "add", "-A")
    sh("git", "-C", str(out), "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "witness")
    print(sh("git", "-C", str(out), "rev-parse", "HEAD").decode().strip())


main()
