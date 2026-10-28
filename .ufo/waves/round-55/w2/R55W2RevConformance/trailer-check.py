#!/usr/bin/env python3
# R55W2RevConformance: per-seat report-trailer check at a committed revision (read-only git).
# usage: python3 -I trailer-check.py <lane> <rev> <round-dir-rel>   e.g. .ufo/waves/round-55/w1
import json, re, subprocess, sys, collections
lane, rev, wdir = sys.argv[1], sys.argv[2], sys.argv[3]
def git(*a):
    return subprocess.run(["git", "-C", lane, *a], capture_output=True)
def exists(p):
    return git("cat-file", "-e", f"{rev}:{p}").returncode == 0
def blob(p):
    return git("show", f"{rev}:{p}").stdout.decode("utf-8", "replace")
disp = json.loads(blob(f"{wdir}-dispatch.json"))
res = json.loads(blob(f"{wdir}-results.json"))
mapping = json.loads(blob(f"{wdir}.ready.dispatched").split("\n")[1])
out = []
tasks = disp["taskCall"]["tasks"]
ok = 0
for t in tasks:
    tr = [l for l in t["task"].splitlines() if l.startswith("Report:")]
    m = re.search(r"(\.ufo/waves/round-\d+/\S+\.md)", tr[0]) if tr else None
    rp = m.group(1) if m else None
    e = bool(rp) and exists(rp)
    ok += e
    rec = next((r for r in res["results"] if r["name"] == t["name"]), None)
    stub = rec is not None and not re.search(r"\{|\[", rec.get("output") or "") and len(rec.get("output") or "") < 400 and rec.get("note") is None
    out.append(f"SEAT name={t['name']} trailer={rp} report_at_rev={e} recorded={rec is not None} map={mapping.get(t['name'])} short_output={stub}")
out.append(f"SUMMARY dispatched={len(tasks)} results={len(res['results'])} trailer_reports_at_rev={ok} missing={len(tasks)-ok}")
names = collections.Counter(r["name"] for r in res["results"])
out.append("DUP_RESULT_NAMES " + str([n for n, c in names.items() if c > 1]))
out.append("RENAMED " + str({k: v for k, v in mapping.items() if k != v}))
print("\n".join(out))
