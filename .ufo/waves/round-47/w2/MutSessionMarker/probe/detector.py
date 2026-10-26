#!/usr/bin/env python3
"""MutSessionMarker probe: bounded behavioral detector for the R3 marker gate.

Runs the gate once per state rev listed in the manifest and asserts, per
state, that every planted real-material case is KEPT (exit 1, FINDING line
present, named WAIVER_REJECTED reason) and every legitimately synthetic case
is waived. Prints one `CASE <state> PASS|FAIL` line per state and writes the
raw gate output to <out-dir>/<state>.txt.

Exit code: 0 iff every requested state passed.
"""
import argparse
import json
import os
import subprocess
import sys

C00 = ".ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C00_shipped/mons.json"
PR = ".ufo/waves/round-47/w2/MutScratch/planted"
FR = ".ufo/waves/round-47/w2/MutScratch/fixtures"
RULES_BASE = "SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=29 R2_PROC_TABLE=31 R3_MONITOR_IDENT=53 R4_HOME_LISTING=2 R5_SERIAL_PROSE=21"


def expect(state, manifest):
    rev = manifest[state]
    summary = "SESSION_MATERIAL: files=%d findings=%d rev=%s" % (
        manifest[state + ".files"], manifest[state + ".findings"], rev)
    req = [("SESSION_MATERIAL", summary)]
    forbidden = []
    if state == "S0-base":
        req.append(("RULES", RULES_BASE))
        forbidden.append("WAIVER")
    elif state == "S1-unmarked":
        req += [
            ("R1", "FINDING file=%s/clients-live.json rule=R1_CLIENT_DUMP count=2 " % PR),
            ("R2", "FINDING file=%s/proc-table.txt rule=R2_PROC_TABLE count=2 " % PR),
            ("R3", "FINDING file=%s/monitors-live.json rule=R3_MONITOR_IDENT count=1 " % PR),
        ]
        forbidden.append("WAIVER")
    elif state == "S2a-cleanwaive":
        req += [
            ("W", "WAIVER file=%s rule=R3_MONITOR_IDENT kind=fixture" % C00),
            ("WC", "SESSION_MATERIAL_WAIVED: findings=1 files=1"),
        ]
        forbidden += ["FINDING file=%s " % C00, "WAIVER_REJECTED"]
    elif state == "S2b-tampered":
        req += [
            ("REJ", "WAIVER_REJECTED file=%s rule=R3_MONITOR_IDENT reason=sha-mismatch" % C00),
            ("F", "FINDING file=%s rule=R3_MONITOR_IDENT count=2 " % C00),
        ]
        forbidden.append("WAIVER file=%s " % C00)
    elif state == "S34-realcontent":
        req += [
            ("REJ1", "WAIVER_REJECTED file=%s/real-content.json rule=R1_CLIENT_DUMP "
                     "reason=value-not-synthetic:title-not-synthetic" % FR),
            ("REJ2", "WAIVER_REJECTED file=%s/real-content.json rule=R2_PROC_TABLE "
                     "reason=value-not-synthetic:program-not-synthetic" % FR),
            ("REJ3", "WAIVER_REJECTED file=%s/real-content.json rule=R3_MONITOR_IDENT "
                     "reason=value-not-synthetic:serial-not-synthetic" % FR),
            ("F1", "FINDING file=%s/real-content.json rule=R1_CLIENT_DUMP count=2 " % FR),
            ("F2", "FINDING file=%s/real-content.json rule=R2_PROC_TABLE count=2 " % FR),
            ("F3", "FINDING file=%s/real-content.json rule=R3_MONITOR_IDENT count=1 " % FR),
            ("REJG", "WAIVER_REJECTED file=%s/not-a-gate-copy.json rule=R1_CLIENT_DUMP "
                     "reason=gate-source-mismatch" % FR),
            ("FG", "FINDING file=%s/not-a-gate-copy.json rule=R1_CLIENT_DUMP count=2 " % FR),
        ]
        forbidden += [
            "WAIVER file=%s/real-content.json" % FR,
            "WAIVER file=%s/not-a-gate-copy.json" % FR,
        ]
    elif state == "S5-proseserial":
        req += [
            ("REJ5", "WAIVER_REJECTED file=%s/prose-serial.md rule=R5_SERIAL_PROSE "
                     "reason=serial-rule-not-waivable" % FR),
            ("F5", "FINDING file=%s/prose-serial.md rule=R5_SERIAL_PROSE count=1 " % FR),
        ]
        forbidden.append("WAIVER file=%s/prose-serial.md" % FR)
    else:
        raise SystemExit("unknown state %r" % state)
    return req, forbidden, {"exit": 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--clone", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--states", default="S0-base,S1-unmarked,S2a-cleanwaive,"
                                        "S2b-tampered,S34-realcontent,S5-proseserial")
    args = ap.parse_args()

    with open(args.manifest, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    os.makedirs(args.out_dir, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(args.out_dir, "tmp")
    os.makedirs(env["TMPDIR"], exist_ok=True)

    failures = 0
    for state in args.states.split(","):
        rev = manifest[state]
        proc = subprocess.run(
            ["python3", "-I", args.gate, "--repo", args.clone, "--rev", rev],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=240,
        )
        out = proc.stdout.decode("utf-8", "replace")
        with open(os.path.join(args.out_dir, state + ".txt"), "w", encoding="utf-8") as handle:
            handle.write("gate=%s\nclone=%s rev=%s rc=%d\n---\n%s"
                         % (args.gate, args.clone, rev, proc.returncode, out))
        req, forbidden, _ = expect(state, manifest)
        problems = []
        if proc.returncode != 1:
            problems.append("exit=%d (want 1)" % proc.returncode)
        for tag, line in req:
            if not any(l.startswith(line) for l in out.splitlines()):
                problems.append("missing[%s] %s" % (tag, line))
        for prefix in forbidden:
            if any(l.startswith(prefix) for l in out.splitlines()):
                problems.append("forbidden %s*" % prefix)
        if problems:
            failures += 1
            print("CASE %s FAIL %s" % (state, "; ".join(problems)))
        else:
            print("CASE %s PASS" % state)
    print("DETECTOR %s passed=%d failed=%d"
          % ("PASS" if failures == 0 else "FAIL",
             len(args.states.split(",")) - failures, failures))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
