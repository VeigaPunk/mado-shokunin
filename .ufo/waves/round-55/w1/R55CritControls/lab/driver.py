#!/usr/bin/env python3
"""Scratch driver: lane model, probes, consistent forgery, harness runs and direct (predicate-style) runs."""
import json, os, shutil, subprocess, sys
LAB = "/fast/scratch/hyaku/mado-r55/R55CritControls/lab"
sys.path.insert(0, LAB)
import r55lab as L

LM = LAB + "/lanemodel"
PR = LAB + "/probes"
FORGE = LAB + "/forged"
W = LAB + "/work"
WD = LAB + "/work-direct"
RC = LAB + "/receipts"
CT = LAB + "/counters"
RD = "corpus/README.md"
SRC = "corpus/SOURCES.md"
ENT = L.ENTRY
CNT = ["c_honest", "c_echo", "c_green", "c_presence", "c_ppid", "c_path", "c_committer", "c_history",
       "c_cache", "c_mutkey", "c_spot", "c_killsink", "c_forged"]


def rm(p):
    shutil.rmtree(p, ignore_errors=True)


def append_bytes(path, b):
    with open(path, "ab") as f:
        f.write(b)


def build_forged():
    L.clone_of(LM, FORGE)
    cv = FORGE + "/" + L.ROUND + "/fetch/Hyprland-ConfigValues.cpp"
    s = open(cv, encoding="utf-8").read()
    old = '"Engage numlock by default.", false'
    assert s.count(old) == 1
    open(cv, "w", encoding="utf-8").write(s.replace(old, '"Engage numlock by default.", true'))
    tb = FORGE + "/" + L.ROUND + "/frozen-tables.json"
    T = json.load(open(tb))
    T["c1"]["pin_sha256"]["Hyprland-ConfigValues.cpp"] = L.sha(open(cv, "rb").read())
    for r in T["c1"]["k"]:
        if r["id"] == "K15":
            assert r["quote"].endswith(", false")
            r["quote"] = r["quote"][:-len("false")] + "true"
    open(tb, "w").write(json.dumps(T, indent=1) + "\n")
    L.edit_line(FORGE + "/" + ENT, "| K15 |", ", false`", ", true`")
    L.commit_all(FORGE, L.L1_ID, "forged consistent tree (lab)")
    forged_sha = L.sha(open(tb, "rb").read())
    src = ('#!/usr/bin/env python3\n# CHANNEL: consistent forgery. Counter constant re-pinned to the forged frozen-tables.json.\n'
           'import sys; sys.path.insert(0, "' + LAB + '")\nimport r55lab as L\n'
           'FORGED = "' + forged_sha + '"\n'
           'def evaluate(repo, rev, work):\n    return L.honest_eval(repo, rev, work, tables_sha=FORGED)\n'
           'if __name__ == "__main__":\n    L.cli(evaluate)\n')
    open(CT + "/c_forged.py", "w").write(src)
    return forged_sha


def mk_probe(name, fn):
    pd = PR + "/" + name
    L.clone_of(LM, pd)
    fn(pd)
    L.commit_all(pd, L.L1_ID, "probe " + name)
    return pd


PROBES = [
    ("P01", "quote:K13", lambda D: L.edit_line(D + "/" + ENT, "| K13 |", ", 25, {.min", ", 26, {.min")),
    ("P02", "anchor:K07", lambda D: L.edit_line(D + "/" + ENT, "| K07 |", "InputManager.cpp:1271", "InputManager.cpp:1272")),
    ("P03", "host:H01", lambda D: L.edit_line(D + "/" + ENT, "| H01 |", "repeat_rate = 40", "repeat_rate = 45")),
    ("P04", "source_cell:K11", lambda D: L.edit_line(D + "/" + ENT, "| K11 |", "| S379 |", "| S316 |")),
    ("P05", "new_rows", lambda D: L.drop_line(D + "/" + SRC, "| S378 |")),
    ("P06", "row:K18", lambda D: L.dup_line(D + "/" + ENT, "| K18 |")),
    ("P07", "provenance", lambda D: L.drop_line(D + "/" + ENT, "verified-at:")),
    ("P08", "index", lambda D: L.drop_line(D + "/" + RD, L.INDEX_ROW)),
    ("P09", "quote:K16", lambda D: L.edit_line(D + "/" + ENT, "| K16 |", "fallback.empty())`", "fallback.empty()) `")),
    ("P10", "pin_hash", lambda D: append_bytes(D + "/" + L.ROUND + "/fetch/Hyprland-ConfigValues.cpp", b" ")),
    ("P11", "quote:K17", lambda D: L.edit_line(D + "/" + ENT, "| K17 |", "repeating (regardless", "repeating (regardles")),
    ("P12", "anchor:H03", lambda D: L.edit_line(D + "/" + ENT, "| H03 |", "host-input.conf:18", "host-input.conf:19")),
]


def classify(rc, out, req):
    v, missed = L.parse_missed(out)
    if rc == 0 and v == "TARGET_MET":
        return "ADMIT"
    if rc == 1 and missed is not None and req in missed:
        return "CAUGHT"
    if rc == 1 and missed is not None:
        return "WRONG-LEG"
    return "BROKEN"


def main():
    for p in (PR, FORGE, W, WD, RC):
        rm(p)
    os.makedirs(RC, exist_ok=True)
    os.makedirs(PR, exist_ok=True)
    rm(LM)
    L.build_lane_model(LM)
    forged_sha = build_forged()
    for name, _, fn in PROBES:
        mk_probe(name, fn)

    out = []
    out.append(f"lane model HEAD {L.git(LM, 'rev-parse', 'HEAD').stdout.decode().strip()} "
               f"forged {forged_sha}")
    matrix = {}
    for cname in CNT:
        C = f"{CT}/{cname}.py"
        # harness-shaped run on the good tree (lane model) and the controls
        wname = os.path.join(W, cname)
        p = subprocess.run(["python3", "-I", LAB + "/check-r55-controls.py", "--counter", C,
                            "--repo", LM, "--work", wname], capture_output=True, text=True)
        summary = p.stdout.strip() or ("HARNESS-ERR " + p.stderr.strip()[-300:])
        harness_forged = ""
        if cname in ("c_forged", "c_honest"):
            p2 = subprocess.run(["python3", "-I", LAB + "/check-r55-controls.py", "--counter", C,
                                 "--repo", FORGE, "--work", wname + "-forged"], capture_output=True, text=True)
            harness_forged = p2.stdout.strip() or ("HARNESS-ERR " + p2.stderr.strip()[-300:])
        # direct predicate-style run: the counter line on the good tree first (a prior green run at HEAD),
        # then on each probe with --rev HEAD and the same --work (exposes the prior-run cache channel).
        dwork = os.path.join(WD, cname)
        rc0, out0 = L.run_counter(C, LM, "HEAD", dwork)
        direct_good = f"rc={rc0} {out0}"
        cls = []
        for name, req, _ in PROBES:
            rc, o = L.run_counter(C, os.path.join(PR, name), "HEAD", dwork)
            cls.append((name, req, classify(rc, o, req), o))
        forged_direct = ""
        if cname in ("c_forged", "c_honest"):
            rc3, o3 = L.run_counter(C, FORGE, "HEAD", os.path.join(WD, cname + "-forged"))
            forged_direct = f"rc={rc3} {o3}"
        admitted = [c[0] for c in cls if c[2] == "ADMIT"]
        wrong = [c[0] for c in cls if c[2] == "WRONG-LEG"]
        matrix[cname] = dict(harness=summary, harness_forged=harness_forged, direct_good=direct_good,
                             forged_direct=forged_direct, admitted=admitted, wrong=wrong,
                             caught=[c[0] for c in cls if c[2] == "CAUGHT"], cls=cls)
        with open(os.path.join(RC, f"direct-{cname}.txt"), "w") as f:
            for name, req, c, o in cls:
                f.write(f"{name} req={req} {c} :: {o}\n")
            f.write(f"GOOD :: {direct_good}\n")
    for cname in CNT:
        m = matrix[cname]
        out.append(f"== {cname}")
        out.append(f"  harness(LM):     {m['harness']}")
        if m["harness_forged"]:
            out.append(f"  harness(FORGE):  {m['harness_forged']}")
        out.append(f"  direct good:     {m['direct_good'][:160]}")
        if m["forged_direct"]:
            out.append(f"  direct forged:   {m['forged_direct'][:160]}")
        out.append(f"  probes caught={len(m['caught'])} wrong-leg={m['wrong']} admitted={m['admitted']}")
    txt = "\n".join(out) + "\n"
    open(LAB + "/matrix.txt", "w").write(txt)
    print(txt)
    json.dump({k: {kk: vv for kk, vv in v.items() if kk != "cls"} for k, v in matrix.items()},
              open(RC + "/matrix.json", "w"), indent=1)


if __name__ == "__main__":
    main()
