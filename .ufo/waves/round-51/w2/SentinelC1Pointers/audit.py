#!/usr/bin/env python3
"""SentinelC1Pointers: dereference every pointer in quality/tool-ledger.md at the freeze rev."""
import collections
import json
import os
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "56026fcb9800370ae04bc65952a6567181c398d0"
BASE = "6ca8c559a4a3d6d361101592116eea2bc7452437"
LEDGER = "quality/tool-ledger.md"

ENV = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent", "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
       "GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C"}


def git(*args, binary=False):
    p = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, env=ENV)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.decode()[:300]))
    return p.stdout if binary else p.stdout.decode("utf-8", "replace")


def files_at(rev):
    return set(p for p in git("ls-tree", "-r", "--name-only", rev).splitlines() if p)


def blob(rev, path):
    try:
        return git("show", "%s:%s" % (rev, path), binary=True).decode("utf-8", "replace")
    except SystemExit:
        return None


BASE_FILES = files_at(BASE)
FREEZE_FILES = files_at(REV)
POP = sorted(p for p in FREEZE_FILES
             if p.startswith("tools/") or re.match(r"^quality/[^/]+\.py$", p)
             or re.match(r"^quality/counters/[^/]+\.py$", p))

text = blob(REV, LEDGER)
lines = text.splitlines()

# parse rows exactly as the counter does (no fences in this ledger) and as the checker does
rows = []
for i, raw in enumerate(lines, 1):
    s = raw.strip()
    if not s.startswith("|"):
        continue
    cells = [c.strip() for c in s.strip("|").split("|")]
    first = cells[0].strip("`*_ \t")
    if not first or "/" not in first or set(first) <= set("-: "):
        continue
    rows.append({"line": i, "path": first, "desc": cells[1] if len(cells) > 1 else "",
                 "ptr": " | ".join(cells[2:]) if len(cells) > 2 else ""})

# checker-strength basename regex
def names(text_, want):
    return re.search(r"(?<![A-Za-z0-9._-])" + re.escape(want) + r"(?![A-Za-z0-9_-])", text_) is not None


def tokens(cell):
    out = []
    for span in re.findall(r"`([^`\n]+)`", cell):
        span = span.strip()
        out.append(span)
    return out


cache = {}
def content(rev, path):
    key = (rev, path)
    if key not in cache:
        cache[key] = blob(rev, path)
    return cache[key]

results = []
cls = collections.Counter()
for r in rows:
    base = os.path.basename(r["path"])
    toks = tokens(r["ptr"])
    deref = []
    for t in toks:
        p = re.sub(r":\d+(?:-\d+)?$", "", t)
        exists = p in FREEZE_FILES
        body = content(REV, p) if exists else ""
        contains_sub = body is not None and base in body
        contains_name = body is not None and names(body, base)
        line_hit = None
        m = re.search(r":(\d+)(?:-(\d+))?$", t)
        if m and exists and body is not None:
            lo = int(m.group(1)); hi = int(m.group(2) or lo)
            seg = "\n".join(body.splitlines()[lo - 1:hi])
            line_hit = names(seg, base)
        deref.append({"token": t, "path": p, "exists": exists,
                      "substring": bool(contains_sub), "as_name": contains_name,
                      "line_anchor_ok": line_hit})
        if exists:
            cls[p] += 1
    results.append({"ledger_line": r["line"], "path": r["path"],
                    "in_population": r["path"] in POP,
                    "desc_len": len(r["desc"]), "pointers": deref})

summary = {
    "rows": len(rows),
    "population": len(POP),
    "rows_without_pointer": [x for x in results if not x["pointers"]],
    "missing_rows": sorted(set(POP) - {x["path"] for x in results}),
    "extra_rows": sorted({x["path"] for x in results} - set(POP)),
    "deref_failures": [(x["ledger_line"], x["path"], p["token"]) for x in results
                       for p in x["pointers"] if not p["exists"]],
    "no_name_failures": [(x["ledger_line"], x["path"], p["token"], p["substring"])
                         for x in results for p in x["pointers"]
                         if p["exists"] and not p["as_name"]],
    "substring_only": [(x["ledger_line"], x["path"], p["token"]) for x in results
                       for p in x["pointers"] if p["substring"] and not p["as_name"]],
    "line_anchor_checked": [(x["ledger_line"], x["path"], p["token"], p["line_anchor_ok"])
                            for x in results for p in x["pointers"]
                            if p["line_anchor_ok"] is not None],
    "pointer_classes": cls.most_common(),
}

lineanchors = summary["line_anchor_checked"]
summary["line_anchor_total"] = len(lineanchors)
summary["line_anchor_bad"] = [a for a in lineanchors if a[3] is False]

# round-51 provenance: which pointer files changed base..freeze and gained the basename
prov = []
for x in results:
    for p in x["pointers"]:
        if not p["exists"]:
            continue
        try:
            at_base = content(BASE, p["path"])
        except SystemExit:
            at_base = None
        if at_base is None:
            state = "absent-at-base"
        elif names(at_base, os.path.basename(x["path"])):
            state = "named-at-base"
        else:
            state = "named-only-at-freeze"
        if state != "named-at-base":
            prov.append((x["ledger_line"], x["path"], p["path"], state))
summary["provenance"] = prov
summary["rows_detail"] = results

print(json.dumps(summary, indent=1))
