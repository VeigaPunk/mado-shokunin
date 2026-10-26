#!/usr/bin/env python3
"""Render the seat artifacts from results.json: cases.md + receipts. Writes only into SEAT."""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/ExecHyprlangOracleB"
R = json.load(open(os.path.join(HERE, "results.json")))


def digest(cid):
    r = R[cid]
    out = []
    for line in r["oracle_out"].splitlines():
        if line.startswith("ORACLE_CAT") or line.startswith("ORACLE_PARSE") or line.startswith("ORACLE_NKEYS"):
            out.append(line)
    return out


def kinds(cid):
    """one compact state line per queried device name seen in the oracle output"""
    r = R[cid]
    rows = {}
    for line in r["oracle_out"].splitlines():
        if line.startswith("ORACLE_FIELD:"):
            body = line[len("ORACLE_FIELD: "):]
            nm = json.loads(body[5: body.index(" field=")])
            fld = body.split("field=", 1)[1].split(" ")[0]
            st = body.split("state=", 1)[1].split(" ")[0]
            pr = json.loads(body.split("projected=", 1)[1])
            rows.setdefault(nm, {})[fld] = ("%s:%s" % (st[0], pr)) if st != "default" or pr else st[0]
        elif line.startswith("ORACLE_SCROLL:"):
            body = line[len("ORACLE_SCROLL: "):]
            nm = json.loads(body[5: body.index(" explicit=")])
            rows.setdefault(nm, {})["scroll"] = "explicit=%s float=%s" % (
                body.split("explicit=", 1)[1].split(" ")[0], body.split("float=", 1)[1].split(" ")[0])
    return rows


md = ["# Targeted edge cases: host hyprlang 0.6.8 oracle vs the frozen reference",
      "",
      "Each case: `oracle <case>.conf <8 names>` (host hyprlang 0.6.8, registrations copied from",
      "Hyprland ConfigManager.cpp:481-628) and `python3 -I mado-devices.py --devices devices.json --config <case>.conf`",
      "(reference sha256 b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b).",
      "Oracle state cells: `s` = set by user, `d` = default, value shown; `scroll` = explicit flag + stored float.",
      "",
      "| case | ref exit | unsupported | ref verdict | class | diverged |",
      "| --- | --- | --- | --- | --- | --- |"]
for cid in sorted(R):
    r = R[cid]
    md.append("| %s | %d | %d | %s | %s | %s |" % (cid, r["ref_rc"], r["ref_unsupported"], r["ref_verdict"], r["class"],
                                                   "; ".join(r["diverged"]) or "-"))
md.append("")
for cid in sorted(R):
    r = R[cid]
    md.append("## %s" % cid)
    md.append("")
    md.append("config (`cat -A`):")
    md.append("```")
    try:
        raw = subprocess.run(["cat", "-A", os.path.join(HERE, "work", cid + ".conf")], capture_output=True, text=True).stdout
    except Exception:
        raw = "<missing>"
    md.append(raw.rstrip("\n"))
    md.append("```")
    md.append("")
    md.append("oracle: " + " | ".join(digest(cid)))
    md.append("")
    for nm, fields in kinds(cid).items():
        md.append("- %s: %s" % (json.dumps(nm), " ".join("%s=%s" % (k, v) for k, v in fields.items())))
    md.append("")
    md.append("reference:")
    md.append("```")
    md.append(r["ref_out"].rstrip("\n"))
    md.append("```")
    md.append("")
open(os.path.join(SEAT, "cases.md"), "w").write("\n".join(md) + "\n")
print("cases.md bytes:", os.path.getsize(os.path.join(SEAT, "cases.md")))
