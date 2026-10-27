#!/usr/bin/env python3
"""Score every control commit with the w1 draft PRED-C2-r49.

Runs `.ufo/waves/round-49/w1/ExecCounterC2/c2-r49-bind-entry.py` once per control commit
from revs.json, with TMPDIR inside that control's scratch dir (never /tmp) and the
inherited read-only compositor socket variables that clause r needs. Writes
receipts/controls.txt (summary, one line per control plus the full clause line) and
receipts/<control>.txt (the complete counter output).
"""
import json
import os
import subprocess

SEAT = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(os.path.dirname(SEAT), "ExecCounterC2", "c2-r49-bind-entry.py")
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
OUT = os.path.join(SEAT, "receipts")


def main():
    os.makedirs(OUT, exist_ok=True)
    revs = json.load(open(os.path.join(SEAT, "revs.json")))
    env = dict(os.environ)
    env.pop("TMPDIR", None)
    lines = []
    lines.append("PRED-C2-r49 control scoring - seat ExecControlsC2, round 49 w1")
    lines.append("draft: %s  sha256=%s" % (DRAFT, file_sha(DRAFT)))
    lines.append("base: %s   harness: drive.py (scratch clone per control)" % BASE)
    lines.append("scoring env: TMPDIR=<control scratch>/tmp (never /tmp), inherited "
                 "XDG_RUNTIME_DIR + HYPRLAND_INSTANCE_SIGNATURE for the read-only replay")
    lines.append("")
    for rec in revs:
        name, repo, rev = rec["control"], rec["repo"], rec["rev"]
        tmp = os.path.join(os.path.dirname(repo), "tmp")
        e = dict(env)
        e["TMPDIR"] = tmp
        p = subprocess.run(["python3", DRAFT, "--repo", repo, "--rev", rev, "--base", BASE],
                           capture_output=True, text=True, env=e)
        out = p.stdout + p.stderr
        open(os.path.join(OUT, name + ".txt"), "w").write(out)
        final = [l for l in out.splitlines() if l.startswith("PRED-C2-r49:")]
        clauses = [l for l in out.splitlines() if " clauses=" in l]
        expect = json.load(open(os.path.join(SEAT, "controls", name, "expect.json")))
        verdict = final[-1].split("verdict=")[1].split()[0] if final else "SETUP"
        want = ("TARGET_MET" if expect["expect"] in ("MET", "ADMIT")
                or expect["expect"].startswith("MET") else "TARGET_MISSED")
        pred = expect.get("predicted", "")
        tag = "AGREE" if verdict == want else ("DEFECT" if verdict == "TARGET_MET" else "DISAGREE")
        lines.append("%-30s rc=%d verdict=%-13s correct=%-13s predicted=%-4s %-7s clause=%s" % (
            name, p.returncode, verdict, want, pred, tag, expect["clause"]))
        if clauses:
            lines.append("    %s" % clauses[-1].strip())
        for l in out.splitlines():
            if l.startswith("PRED-C2-r49 ") and (" clause=" in l) and l.rstrip().endswith(
                    ("0", "1", "ok=0", "ok=1")) is False:
                pass
        lines.append("    rev=%s" % rev)
    open(os.path.join(OUT, "controls.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


def file_sha(p):
    import hashlib
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


if __name__ == "__main__":
    main()
