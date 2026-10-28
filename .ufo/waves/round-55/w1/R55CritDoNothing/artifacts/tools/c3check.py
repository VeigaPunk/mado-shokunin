#!/usr/bin/env python3
"""Seat-written C3 checker, built from registration.md §C3 + claims-frozen PRED-C3-r55 text.
NOT the wave's quality/counters/c3-r55-p19.py. Reads git objects only.
Usage: c3check.py --repo R --rev REV --base-rev BASE --work W"""
import argparse, hashlib, json, re, subprocess, sys

ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
README = "corpus/README.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
TABLES_SHA = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"
ERRATA_NAME = "hyprland-synthetic-dispatch-r52-errata-r53.md"


def git_blob(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "cat-file", "-p", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    legs = []

    tb = git_blob(a.repo, a.rev, TABLES)
    if tb is None:
        print("MADO_P19_FIX: SETUP no frozen tables"); sys.exit(2)
    if hashlib.sha256(tb).hexdigest() != TABLES_SHA:
        legs.append("tables_sha")
    C3 = json.loads(tb)["c3"]

    cur = git_blob(a.repo, a.rev, ENTRY) or b""
    base = git_blob(a.repo, a.base_rev if False else a.base_rev, ENTRY) or b""
    prefix = "identical" if cur.startswith(base) and base else "changed"
    if prefix != "identical":
        legs.append("prefix")
    text = cur.decode("utf-8", "replace")

    # Q rows
    pin_b = git_blob(a.repo, a.rev, C3["pin"]) or b""
    pin_ok = hashlib.sha256(pin_b).hexdigest() == C3["pin_sha256"]
    if not pin_ok:
        legs.append("pin")
    plines = pin_b.decode("utf-8", "replace").split("\n")
    rows_ok = 0
    qrows = {}
    for l in text.split("\n"):
        if l.startswith("| Q"):
            c = l.split("|")
            if len(c) >= 4:
                qrows.setdefault(c[1].strip(), []).append(c)
    for q in C3["q"]:
        cands = qrows.get(q["id"], [])
        ok = False
        if len(cands) == 1 and len(cands[0]) == 5:
            c = cands[0]
            pinname = C3["pin"].rsplit("/", 1)[-1]
            ok = (c[2].strip() == f"{pinname}:{q['line']}"
                  and c[3].strip() == f"`{q['quote']}`"
                  and 0 < q["line"] <= len(plines) and plines[q["line"] - 1].strip() == q["quote"])
        if not ok:
            legs.append(f"rows:{q['id']}")
        rows_ok += ok

    # P23
    p23_lines = [l for l in text.split("\n") if l.startswith("| P23 |")]
    p23 = False
    if len(p23_lines) == 1:
        c = p23_lines[0].split("|")
        if len(c) >= 6:
            prop = c[3]
            sup = c[2].strip()
            toks = ["m_passPressed", "== 1", "== 0", "PRESSED", "RELEASED"]
            p23 = (all(t in prop for t in toks) and any(t in prop for t in ["otherwise", "any other", "else"])
                   and sup == C3["supersedes"])
    if not p23:
        legs.append("p23")

    # readme
    rd = (git_blob(a.repo, a.rev, README) or b"").decode("utf-8", "replace").split("\n")
    readme = any(ERRATA_NAME in l and "P23" in l for l in rd)
    if not readme:
        legs.append("readme")

    legs = list(dict.fromkeys(legs))
    verdict = "TARGET_MET" if not legs else "TARGET_MISSED"
    print(f"MADO_P19_FIX: rev={a.rev} prefix={prefix} rows={rows_ok}/13 pin={'ok' if pin_ok else 'bad'} "
          f"p23={'ok' if p23 else 'bad'} readme={'ok' if readme else 'bad'} verdict={verdict} "
          f"missed={','.join(legs) if legs else 'none'}")
    sys.exit(0 if verdict == "TARGET_MET" else 1)


if __name__ == "__main__":
    main()
