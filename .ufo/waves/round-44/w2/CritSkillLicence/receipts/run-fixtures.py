#!/usr/bin/env python3
"""Reproduce CritSkillLicence's round-44 SKILL.md licence-row probes.

Runs the landed tool (tools/mado-geometry.py at the lane HEAD) and the round-43 tool
(git show 6a1a9052:tools/mado-geometry.py, asserted sha256 e3c2e471...) over 16 frozen
dumps and prints rc + stdout for both, with an identical= marker.

  python3 -I .ufo/waves/round-44/w2/CritSkillLicence/receipts/run-fixtures.py

Scratch: /fast/scratch/hyaku/mado-r44/CritSkillLicence (created, removed at exit).
Writes nothing outside this seat dir's receipts/fixtures/ and that scratch dir.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-44/w2/CritSkillLicence")
FIX = os.path.join(SEAT, "receipts/fixtures")
SCRATCH = "/fast/scratch/hyaku/mado-r44/CritSkillLicence"
R43_REV = "6a1a9052"
R43_SHA = "e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99"
NEW = os.path.join(LANE, "tools/mado-geometry.py")


def client(**kw):
    base = dict(address="0x1", mapped=True, cls="org.omarchy.gkeep", floating=False,
                size=[800, 600], fullscreen=0)
    base.update(kw)
    d = {"address": base["address"], "mapped": base["mapped"], "class": base["cls"],
         "floating": base["floating"], "size": base["size"], "fullscreen": base["fullscreen"]}
    return d


CASES = {
    "A_tiled": [client()],
    "B_agree": [client(floating=True, size=[420, 500])],
    "C_differ": [client(floating=True, size=[900, 700])],
    "D_unmapped_fs": [client(mapped=False, fullscreen=2, size=[3440, 1440]), client(address="0x2")],
    "E_nonmatch_fs": [client(cls="other.App", fullscreen=2, size=[3440, 1440]), client(address="0x2")],
    "F_fs_only": [client(floating=True, fullscreen=2, size=[3440, 1440])],
    "G_fs_plus_differ": [client(floating=True, fullscreen=2, size=[3440, 1440]),
                         client(address="0x2", floating=True, size=[900, 700])],
    "H_max_only": [client(floating=False, fullscreen=1, size=[3440, 1414])],
    "I_fs_coincide": [client(floating=True, fullscreen=2, size=[420, 500])],
    "J_nomatch_fs": [client(cls="other.App", fullscreen=2, size=[3440, 1440])],
    "K_fs_plus_tiled": [client(floating=True, fullscreen=2, size=[3440, 1440]),
                        client(address="0x2", floating=False, size=[800, 600])],
    "L_badsize_plus_fs": [client(floating=True, fullscreen=2, size=[3440, 1440]),
                          client(address="0x2", floating=True, size=None)],
    "M_fs_bool": [client(floating=True, fullscreen=True, size=[3440, 1440])],
    "N_fs_zero": [client(floating=True, fullscreen=0, size=[900, 700])],
    "O_fs3": [client(floating=True, fullscreen=3, size=[3440, 1440])],
    "P_badsize_fs_only": [client(floating=True, fullscreen=2, size=None)],
}


def run(tool, dump, rules):
    p = subprocess.run([sys.executable, "-I", tool, "--clients", dump, "--rules", rules],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    shutil.rmtree(SCRATCH, ignore_errors=True)
    os.makedirs(SCRATCH)
    os.makedirs(FIX, exist_ok=True)
    try:
        r43 = os.path.join(SCRATCH, "tool-r43.py")
        blob = subprocess.run(["git", "-C", LANE, "show", f"{R43_REV}:tools/mado-geometry.py"],
                              capture_output=True, check=True).stdout
        open(r43, "wb").write(blob)
        got = hashlib.sha256(open(r43, "rb").read()).hexdigest()
        assert got == R43_SHA, f"round-43 tool sha {got} != {R43_SHA}"
        new_sha = hashlib.sha256(open(NEW, "rb").read()).hexdigest()

        rules = os.path.join(FIX, "rules.conf")
        open(rules, "w").write(
            "windowrule = float, match:class ^(org.omarchy.gkeep)$\n"
            "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$\n")

        print("# CritSkillLicence fixtures — round-44 SKILL.md licence-row probes")
        print(f"# lane HEAD tool sha256 {new_sha}")
        print(f"# round-43 tool = git {R43_REV}:tools/mado-geometry.py sha256 {got}")
        print("# rules.conf: float on + size 420 500 for ^(org.omarchy.gkeep)$")
        print()
        for name, clients in CASES.items():
            dump = os.path.join(FIX, name + ".json")
            json.dump(clients, open(dump, "w"), sort_keys=True)
            o_rc, o_out, o_err = run(r43, dump, rules)
            n_rc, n_out, n_err = run(NEW, dump, rules)
            identical = (o_rc, o_out) == (n_rc, n_out)
            print(f"== {name} identical={identical} stderr_empty={not o_err and not n_err}")
            for tag, rc, out in (("r43", o_rc, o_out), ("r44", n_rc, n_out)):
                lines = out.rstrip("\n").splitlines()
                print(f"   {tag} rc={rc}")
                for ln in lines:
                    print(f"     {ln}")
            if not identical:
                print("   DELTA: r44 output differs from the round-43 contract")
            print()
    finally:
        shutil.rmtree(SCRATCH, ignore_errors=True)


if __name__ == "__main__":
    main()
