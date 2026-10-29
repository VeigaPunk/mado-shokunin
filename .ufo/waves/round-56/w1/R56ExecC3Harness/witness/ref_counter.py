#!/usr/bin/env python3
"""WITNESS reference counter for PRED-C3-r56 (seat R56ExecC3Harness; NOT the scored counter). Reads git objects at --rev."""
import re, subprocess, sys
MODE = "full"  # variants for the harness differential: full | missing_only | no_fence | always_green | always_red


def g(repo, *a):
    p = subprocess.run(["git", "-C", repo] + list(a), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p


def main(argv):
    o = dict(zip(argv[::2], argv[1::2]))
    repo, rev = o["--repo"], o["--rev"]
    if MODE == "always_green":
        print("MADO_USED_BY: rev=%s entries=70 rows=319 missing=0 extra=0 dangling=0 verdict=TARGET_MET missed=none" % rev)
        return 0
    if MODE == "always_red":
        print("MADO_USED_BY: rev=%s entries=70 rows=319 missing=1 extra=0 dangling=0 verdict=TARGET_MISSED missed=missing" % rev)
        return 1
    reg = g(repo, "show", "%s:corpus/SOURCES.md" % rev)
    if reg.returncode:
        sys.stderr.write("no registry\n"); return 2
    rows = {}
    for ln in reg.stdout.decode("utf-8", "replace").split("\n"):
        if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|", ln):
            cells = ln.strip().strip("|").split("|")
            if len(cells) != 11:
                sys.stderr.write("bad row\n"); return 2
            rows.setdefault(cells[0].strip(), set()).update(re.findall(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md", cells[10]))
    ents = {}
    for rec in g(repo, "ls-tree", "-z", rev, "corpus/knowledge/").stdout.split(b"\0"):
        if not rec:
            continue
        meta, name = rec.split(b"\t", 1)
        mode, typ, sha = meta.decode().split()
        name = name.decode()
        if typ == "blob" and mode in ("100644", "100755") and name.endswith(".md"):
            ents[name] = g(repo, "cat-file", "blob", sha).stdout.decode("utf-8", "replace")
    cite, src = {}, {}
    for name, txt in ents.items():
        lines = txt.split("\n")
        infence, c, s = False, set(), set()
        for i, ln in enumerate(lines):
            isf = re.match(r"^ {0,3}(```|~~~)", ln) is not None
            if isf and MODE != "no_fence":
                infence = not infence
                continue
            if infence and MODE != "no_fence":
                continue
            c.update(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])", ln))
        for ln in lines[:15]:
            if ln.startswith("source:"):
                s.update(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])", ln))
        cite[name], src[name] = c, s
    missing = sum(1 for n in ents for s in cite[n] if s in rows and n not in rows[s])
    extra = sum(1 for s, ps in rows.items() for p in ps if p not in ents or s not in cite[p])
    dangling = sum(1 for n in ents for s in src[n] if s not in rows)
    if MODE == "missing_only":
        extra = dangling = 0
    legs = [k for k, v in (("missing", missing), ("extra", extra), ("dangling", dangling)) if v]
    ok = not legs
    print("MADO_USED_BY: rev=%s entries=%d rows=%d missing=%d extra=%d dangling=%d verdict=%s missed=%s" % (
        rev, len(ents), len(rows), missing, extra, dangling, "TARGET_MET" if ok else "TARGET_MISSED", ",".join(legs) or "none"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
