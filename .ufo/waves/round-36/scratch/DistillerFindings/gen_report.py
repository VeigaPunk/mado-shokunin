import sys
sys.path.insert(0, '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-36/scratch/DistillerFindings')
import findings as F

rows = []
claim_order = {"C1":0, "C2":1, "frontier":2, "harm-watch":3}
status_order = {"open":0, "needs L1":1, "refuted":2}
for key, items in F.groups.items():
    target, claim, status = key
    sev = max((i["sev"] for i in items if i["sev"]), key=lambda x: {"HIGH":3,"MEDIUM":2,"LOW":1}.get(x,0), default="")
    seats = sorted({i["seat"] for i in items})
    texts = []
    for i in items:
        t = i["text"]
        if t not in texts:
            texts.append(t)
    rows.append(dict(target=target, claim=claim, status=status, sev=sev,
                     seats=", ".join(seats), text="; ".join(texts), n=len(items)))
rows.sort(key=lambda r: (claim_order[r["claim"]], status_order[r["status"]], -{"HIGH":3,"MEDIUM":2,"LOW":1}.get(r["sev"],0)))

L = []
L.append("# DistillerFindings — wave-1 findings, deduplicated")
L.append("")
L.append("Seat: `L1Mado36.DistillerFindings` (simplifier). Date: 2026-10-25. Lane: mado-shokunin.")
L.append("")
L.append("## Snapshot")
L.append("")
L.append(f"- Reports read: **50** (all files present in `LANE/.ufo/waves/round-36/w1/reports/` at run time besides the registry; the registry lists 64 members).")
L.append(f"- Seats whose reports had **not** landed at snapshot time: {', '.join(F.MISSING_SEATS)}.")
L.append("- Normalization: each finding is keyed by the file/clause it concerns, the claim it touches (C1/C2/frontier/harm-watch) and its status; restatements of the same key across reports are merged.")
L.append("")
L.append("## Counts")
L.append("")
L.append(f"| metric | count |")
L.append(f"|---|---|")
L.append(f"| raw finding rows extracted | {F.raw_n} |")
L.append(f"| distinct rows after dedup/merge | {F.distinct_n} |")
L.append(f"| merged rows (restatements collapsed) | {F.merged_n} |")
L.append("")
L.append("## Findings table")
L.append("")
L.append("| # | Where it points | Claim | Status | Source seats | Finding (normalized) |")
L.append("|---|---|---|---|---|---|")
for idx, r in enumerate(rows, 1):
    sev = f" ({r['sev']})" if r["sev"] else ""
    L.append(f"| F{idx:02d} | `{r['target']}` | {r['claim']} | {r['status']}{sev} | {r['seats']} | {r['text']} |")
L.append("")
L.append("## Status legend")
L.append("")
L.append("- **open** — an actionable defect/gap on the current bytes (counter, gate, manifest, record, or security posture); severity in parentheses.")
L.append("- **refuted** — the probed defect/harm did not materialize: the tested attack failed, the baseline held, or the finding confirms load-bearing behavior of the shipped instrument.")
L.append("- **needs L1** — a decision or application owned by the L1 (production edits, policy phrasing, authorship confirmation); the seat cannot apply it under read-only bounds.")
L.append("")
L.append("## Coverage note")
L.append("")
L.append("The 50 read reports cover all 64 registry members except the 17 listed above (Scribe seats may deliver to scratch instead of the reports dir; ScoutPriorArt2 was observed unassigned by RevSourceQuotes). Findings are normalized per file/clause, so late reports for the same targets would merge into the rows above.")

open('/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-36/w1/reports/DistillerFindings.md','w').write("\n".join(L))
print("written", len(L), "lines")
