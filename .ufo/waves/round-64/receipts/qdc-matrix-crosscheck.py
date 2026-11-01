#!/usr/bin/env python
"""mado round-64 crosscheck: the flag-matrix probe's 0x02 baseline leg against the
round-63 committed snapshot (independent artifacts, different rounds). Stable fields
only, numeric equality; nothing is written; reads the two named JSON files."""
import json
import sys
from pathlib import Path

def load(repo, rel):
    p = Path(repo) / rel
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)

def numeq(a, b):
    return float(a) == float(b)

def main(argv):
    if len(argv) != 2:
        print("usage: qdc-matrix-crosscheck.py <repo-root>", file=sys.stderr)
        return 2
    repo = argv[1]
    try:
        snap = load(repo, ".ufo/waves/round-63/receipts/windisplayconfig-snapshot.json")
        matrix = load(repo, ".ufo/waves/round-64/receipts/qdc-matrix-run1.json")
    except (OSError, ValueError) as exc:
        print("MADO_QDC_CROSSCHECK: ERROR (stage=input detail=%s)" % type(exc).__name__)
        return 2
    base = next((s for s in matrix if s.get("qdc_flags") == 2), None)
    if base is None or not snap.get("path_list") or not base.get("path_list"):
        print("MADO_QDC_CROSSCHECK: ERROR (stage=shape detail=missing 0x02 leg or empty path_list)")
        return 2
    s_path, b_path = snap["path_list"][0], base["path_list"][0]
    s_tm, b_tm = s_path.get("target_mode") or {}, b_path.get("target_mode") or {}
    checks = [
        ("qdc_flags", numeq(snap["qdc_flags"], base["qdc_flags"])),
        ("buffer_hr", numeq(snap["buffer_hr"], base["buffer_hr"])),
        ("query_hr", numeq(snap["query_hr"], base["query_hr"])),
        ("paths", numeq(snap["paths"], base["paths"])),
        ("modes", numeq(snap["modes"], base["modes"])),
        ("mode_info_types", list(snap["mode_info_types"]) == list(base["mode_info_types"])),
        ("path_flags", numeq(s_path["flags"], b_path["path_flags"])),
        ("target.mode_info_idx", numeq(s_path["target"]["mode_info_idx"], b_path["target"]["mode_info_idx"])),
        ("refresh_num", numeq(s_path["target"]["refresh_num"], b_path["target"]["refresh_num"])),
        ("refresh_den", numeq(s_path["target"]["refresh_den"], b_path["target"]["refresh_den"])),
        ("pixel_rate", numeq(s_tm["pixel_rate"], b_tm["pixel_rate"])),
        ("hsync_num", numeq(s_tm["hsync_num"], b_tm["hsync_num"])),
        ("vsync_num", numeq(s_tm["vsync_num"], b_tm["vsync_num"])),
        ("vsync_den", numeq(s_tm["vsync_den"], b_tm["vsync_den"])),
        ("active_cx", numeq(s_tm["active_cx"], b_tm["active_cx"])),
        ("active_cy", numeq(s_tm["active_cy"], b_tm["active_cy"])),
        ("total_cx", numeq(s_tm["total_cx"], b_tm["total_cx"])),
        ("total_cy", numeq(s_tm["total_cy"], b_tm["total_cy"])),
        ("join_agree", s_tm["join_agree"] == b_tm["join_agree"]),
    ]
    for name, ok in checks:
        print("CROSSCHECK %s: %s" % (name, "AGREE" if ok else "DIFFER"))
    agree = sum(1 for _, ok in checks if ok)
    total = len(checks)
    verdict = "AGREE" if agree == total else "DIFFER"
    print("MADO_QDC_CROSSCHECK: %d/%d stable fields %s (r63 snapshot vs r64 matrix 0x02 leg)" % (agree, total, verdict))
    return 0 if agree == total else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
