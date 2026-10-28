#!/usr/bin/env python3
"""Run the scratch model over the 18 committed C2 fixtures under LIT and under each single alternative."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55RevC2Spec")
import ref  # noqa: E402

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
FIX = LANE / ".ufo/waves/round-55/fixtures/c2"
ALTS = {
    "split": "splitlines", "strip": "py", "comment": "raw", "close": "lead",
    "brace": "comment_cut", "empty_push": "reject", "enc": "utf-8-sig",
    "topcolon": "literal", "dollar": "rhs", "int": "prefix", "source": "unsupported",
    "name_dollar": "unsupported", "empty_name": "reject", "device_scope": "innermost",
    "star": "reserved", "symlink": "nofollow", "setup": "getopt_first",
    "argv_dash": "nodash", "repeat_getopt": "last", "empty_kb": "usage",
    "blank": "stripped", "intfloat": "integral",
}


def run_fixture(d, F):
    args = json.loads((d / "args.json").read_text())
    exp_out = (d / "expected.out").read_text()
    exp_rc = int((d / "expected.rc").read_text().strip())
    cwd = os.getcwd()
    os.chdir(LANE)
    try:
        lines, rc = ref.kbdopt(args, F)
    finally:
        os.chdir(cwd)
    got = "\n".join(lines) + "\n"
    return got == exp_out and rc == exp_rc, got, rc


def main():
    dirs = sorted(p for p in FIX.iterdir() if p.is_dir())
    lit_pass = 0
    for d in dirs:
        ok, got, rc = run_fixture(d, dict(ref.LIT))
        lit_pass += ok
        if not ok:
            print(f"LIT MISMATCH {d.name}\n{got}rc={rc}")
    print(f"LIT committed={lit_pass}/{len(dirs)}")
    for key, alt in ALTS.items():
        F = dict(ref.LIT)
        F[key] = alt
        failing = [d.name for d in dirs if not run_fixture(d, F)[0]]
        print(f"ALT {key}={alt}: fails {len(failing)} committed: {','.join(failing) or 'none'}")


if __name__ == "__main__":
    main()
