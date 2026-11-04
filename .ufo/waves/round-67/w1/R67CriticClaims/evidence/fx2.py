#!/usr/bin/env python3
"""Two falsifications, read-only, all writes under $S:
1. C1 residual: a receipt path in a PROBE cell that does not resolve is rejected
   by the r66 counter but accepted by the r67 draft (receipt-cell-only scope).
2. C2/M-R: the base c3-r56-used-by.py git_env() reads a planted refs/replace
   forgery; the r67 draft env reads the real bytes.
"""
import importlib.util
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r67/R67CriticClaims/fx2"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
LIVE = ".ufo/waves/round-65/receipts/gate-live-r65.txt"
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
    base = "0b28ffb4baac9586566d246c3f0986b2bb650a33"
    r66p = os.path.join(S, "r66.py")
    with open(r66p, "wb") as fh:
        fh.write(git_bytes("show", base + ":quality/counters/c1-r66-register.py"))
    usedp = os.path.join(S, "usedby_base.py")
    with open(usedp, "wb") as fh:
        fh.write(git_bytes("show", base + ":quality/counters/c3-r56-used-by.py"))
    r66 = load(r66p, "r66")
    draft = load(os.path.join(LANE, ".ufo/waves/round-67/w1/R67ExecRegister/draft/"
                              "quality/counters/c1-r67-register.py"), "r67")
    used_base = load(usedp, "used_base")
    used_draft = load(os.path.join(LANE, ".ufo/waves/round-67/w1/R67ExecChildren/draft/"
                                   "quality/counters/c3-r56-used-by.py"), "used_draft")

    header = ("### Surface state register (2026-11-03, this host)\n"
              "| surface group | state | probe | receipt |\n|---|---|---|---|\n")
    rows = [f"| {g} | unmeasured state | probe | `{LIVE}` |" for g in GROUPS]
    bodies = {LIVE: LIVE_LINE + "\n"}
    rows[2] = f"| walker | unmeasured state | read {MISSING} | `{LIVE}` |"
    text = header + "\n".join(rows) + "\n<!-- r65 register end -->\n"
    r66r, _ = r66.assess(text, bodies.get)
    r67r, _, _ = draft.assess(text, bodies.get)
    print("CASE unresolved receipt in PROBE cell (rows still cite live)")
    print(f"  r66 accept={not r66r} reasons={r66r}")
    print(f"  r67 accept={not r67r} reasons={r67r}")

    # --- M-R: planted replace ref, read with each child's own git_env() ------
    D = os.path.join(S, "replace-fx")
    os.makedirs(D)
    run = lambda *a, env=None: subprocess.run(
        ["git", "-C", D, *a], capture_output=True, text=True, env=env)
    run("init", "-q")
    top = run("rev-parse", "--show-toplevel").stdout.strip()
    assert top == D, top
    open(os.path.join(D, "f.txt"), "w").write("real\n")
    run("add", "-A")
    run("-c", "user.name=p", "-c", "user.email=p@example.invalid",
        "-c", "commit.gpgsign=false", "commit", "-qm", "base")
    real = run("rev-parse", "HEAD:f.txt").stdout.strip()
    forged_tmp = os.path.join(S, "forged.txt")
    open(forged_tmp, "w").write("forged\n")
    forged = run("hash-object", "-w", "--path=f.txt", forged_tmp).stdout.strip()
    run("replace", real, forged)
    work = os.path.join(S, "work")
    os.makedirs(work)
    for label, mod in (("base", used_base), ("draft", used_draft)):
        env = mod.git_env(work)
        got = subprocess.run(["git", "-C", D, "show", "HEAD:f.txt"],
                             capture_output=True, text=True, env=env).stdout.strip()
        print(f"M-R child_env={label} GIT_NO_REPLACE_OBJECTS="
              f"{env.get('GIT_NO_REPLACE_OBJECTS', '<absent>')} read={got}")
    shutil.rmtree(S, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
