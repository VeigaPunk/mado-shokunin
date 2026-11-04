#!/usr/bin/env python3
"""R80CriticClaims lab: build doctored-controls-new.json.

The 23 carried cases stay byte-identical; the ten new cases' expects are replaced
by whatever the given tool actually prints on them. Used to show that the
carried=23/23 clause gives the ten new cases no mechanical protection.

usage: doctor-c1.py TOOL OUTPUT.json
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r80/R80CriticClaims"

spec = importlib.util.spec_from_file_location("c1c", os.path.join(HERE, "c1-critic.py"))
c1c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1c)

TOOL = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])

controls = json.load(open(os.path.join(
    LANE, ".ufo/waves/round-80/controls/c1-cases-r80.json")))
cases = controls["cases"]
root = tempfile.mkdtemp(prefix="doctor-", dir=SCRATCH)
changed = 0
try:
    for index, case in enumerate(cases):
        if index < c1c.CARRIED:
            continue
        outdir = os.path.join(root, "doc-%02d" % index)
        cfg, layers, monitors, rules, surfaces = c1c.case_files(case, outdir)
        argv = [sys.executable, "-I", TOOL, "--config", cfg, "--layers", layers,
                "--monitors", monitors]
        if rules:
            argv += ["--rules", rules]
        if surfaces:
            argv += ["--surfaces", surfaces]
        if case.get("monitor"):
            argv += ["--monitor", case["monitor"]]
        rc, stdout, stderr = c1c.run(argv, outdir)
        got = c1c.parse_result(stdout) or {}
        expect = {"rc": rc}
        for key in ("box", "boxes", "reserved", "band", "expected", "attributed",
                    "gt", "attr", "ls", "verdict"):
            if got.get(key) is not None:
                expect[key] = got[key]
        attrs = c1c.parse_attr(stdout)
        if attrs:
            expect["attr_ns"] = attrs
        case["expect"] = expect
        ok = c1c.expected_ok(case, rc, stdout)
        assert ok, "doctored case %s does not self-verify" % case["name"]
        changed += 1
        print("doctored %-24s rc=%d %s" % (
            case["name"], rc,
            {k: v for k, v in sorted(expect.items()) if k not in ("rc", "attr_ns")}))
    with open(OUT, "w") as fh:
        json.dump(controls, fh, indent=1, sort_keys=True)
    print("wrote %s (%d of %d cases re-derived from the tool)" % (OUT, changed, len(cases)))
finally:
    shutil.rmtree(root, ignore_errors=True)
