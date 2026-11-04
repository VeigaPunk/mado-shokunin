#!/usr/bin/env python3
"""Falsification: does the C1 r67 draft still reject a row whose receipt cell
names the genuine live receipt AND an unresolved second receipt (an invariant
the r66 counter enforced)?  Read-only; imports both counters into scratch."""
import importlib.util
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r67/R67CriticClaims/c1-reg"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DRAFT = os.path.join(LANE, ".ufo/waves/round-67/w1/R67ExecRegister/draft/quality/counters/c1-r67-register.py")
LIVE = ".ufo/waves/round-65/receipts/gate-live-r65.txt"
PLANE = ".ufo/waves/round-65/receipts/gate-fileplane-r65.txt"
MISSING = ".ufo/waves/round-65/receipts/not-committed.txt"
LIVE_LINE = "MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)"
GROUPS = ("hypr plane", "waybar", "walker", "terminal configs",
          "theme/wallpaper omarchy plane", "idle/lock plane", "omarchy skill docs",
          "windows desktop plane")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_bytes(*args):
    return subprocess.run(["git", "-C", LANE, *args], capture_output=True, check=True).stdout


def main():
    shutil.rmtree(S, ignore_errors=True)
    os.makedirs(S)
    r66_path = os.path.join(S, "c1-r66-register.py")
    with open(r66_path, "wb") as fh:
        fh.write(git_bytes("show", "0b28ffb4baac9586566d246c3f0986b2bb650a33:"
                           "quality/counters/c1-r66-register.py"))
    r66 = load(r66_path, "r66")
    r67 = load(DRAFT, "r67")
    header = ("### Surface state register (2026-11-03, this host)\n"
              "| surface group | state | probe | receipt |\n|---|---|---|---|\n")
    rows = [f"| {g} | unmeasured state | probe | `{LIVE}` |" for g in GROUPS]
    bodies = {LIVE: LIVE_LINE + "\n", PLANE: "MADO_VERIFY: CLEAN (file plane)\n"}
    # Case A: one row's receipt cell names the live receipt plus an unresolved receipt.
    rows_a = list(rows)
    rows_a[0] = f"| hypr plane | unmeasured state | probe | `{LIVE}` `{MISSING}` |"
    text_a = header + "\n".join(rows_a) + "\n<!-- r65 register end -->\n"
    # Case B: unresolved second receipt in a different row than the live citation.
    rows_b = list(rows)
    rows_b[1] = f"| waybar | unmeasured state | probe | `{LIVE}` `{MISSING}` |"
    text_b = header + "\n".join(rows_b) + "\n<!-- r65 register end -->\n"
    for name, text in (("live+unresolved same row", text_a),
                       ("live+unresolved live row", text_b)):
        r66_reasons, _ = r66.assess(text, bodies.get)
        r67_reasons, _, _ = r67.assess(text, bodies.get)
        print(f"CASE {name}")
        print(f"  r66 accept={not r66_reasons} reasons={r66_reasons}")
        print(f"  r67 accept={not r67_reasons} reasons={r67_reasons}")
    shutil.rmtree(S, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
