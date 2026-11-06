#!/usr/bin/env python3
"""Round 89, seat R89MExecHostDiff: host coverage grid for C1 (read-only).

Runs the base tool (revision af998dcc:tools/mado-mako.py) and the C1 candidate over the
live host mako config, and cross-checks the five host summary~ patterns against the
independent POSIX ERE oracle and Python re.

Read-only host access: only ~/.config/mako/config and the file it includes
(~/.local/share/omarchy/default/mako/core.ini). Nothing is written outside the
scratch root ($HYAKU_SCRATCH/mado-r89/R89MExecHostDiff).

Usage: R89MExecHostDiff-grid.py [--json OUT]   (scratch root from HYAKU_SCRATCH, default
       /fast/scratch/hyaku)
Exit 0 when every tool invocation ran and every oracle/python-re comparison agrees,
1 otherwise (setup errors are reported, not retried into green).
"""
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE_REV = "af998dcc41d48618ffe7afe0efc9354755a9244e"
CANDIDATE = LANE + "/.ufo/waves/round-89/build/mado-mako.c1.py"
ORACLE_SRC = LANE + "/.ufo/waves/round-89/controls/posix-ere-oracle.c"
CONFIG = os.path.expanduser("~/.config/mako/config")
HOME = os.path.expanduser("~")

SUMMARIES = [
    "Setup Wi-Fi",
    "Update System",
    "Learn Keybindings",
    "Install Dictation with Voxtype",
    "Screenshot copied & saved",
    "hello",
]
MODE_SETS = [[], ["do-not-disturb"]]
FIELDS = ["on-button-left", "max-icon-size", "format", "invisible"]
COMMON = ["--app-name", "notify-send", "--urgency", "normal",
          "--body", "x", "--app-icon", "x", "--category", "x",
          "--desktop-entry", "x", "--actionable", "false", "--expiring", "false"]

# The five host patterns as the criteria tokenizer yields them (double quotes removed).
HOST_PATTERNS = [
    "Setup Wi-Fi",
    "Update System",
    "Learn Keybindings",
    "Install Dictation with Voxtype",
    "Screenshot copied & saved",
]


def scratch():
    root = os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
                        "mado-r89", "R89MExecHostDiff")
    os.makedirs(root, exist_ok=True)
    return root


def dump_base(sdir):
    path = os.path.join(sdir, "base.py")
    with open(path, "w", encoding="utf-8") as handle:
        subprocess.run(["git", "-C", LANE, "show", BASE_REV + ":tools/mado-mako.py"],
                       check=True, stdout=handle)
    return path


def run_tool(tool, summary, modes, sdir):
    argv = [sys.executable, tool, "--config", CONFIG, "--home", HOME] + COMMON
    for mode in modes:
        argv += ["--mode", mode]
    # summary is the only criteria string input in the grid
    argv += ["--summary", summary]
    env = dict(os.environ)
    env["TMPDIR"] = sdir
    proc = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=sdir)
    out = {"rc": proc.returncode, "stderr": proc.stderr.strip().splitlines()}
    if proc.returncode != 0:
        return out
    result = json.loads(proc.stdout)
    refusals = result.get("refusals", [])
    out["refusals"] = refusals
    out["refusal_count"] = len(refusals)
    out["refusal_lines"] = [r.split(": ", 1)[0] for r in refusals]
    eff = result.get("effective", {})
    out["effective"] = {f: eff.get(f, "-") for f in FIELDS}
    out["status_line"] = out["stderr"][-1] if out["stderr"] else ""
    return out


def build_oracle(sdir):
    exe = os.path.join(sdir, "ore")
    subprocess.run(["cc", "-O0", "-o", exe, ORACLE_SRC], check=True)
    return exe


def oracle_verdict(exe, pattern, text):
    proc = subprocess.run([exe, pattern, text], capture_output=True, text=True)
    if proc.returncode != 0:
        return "ORACLE_ERROR(rc=%d)" % proc.returncode
    return proc.stdout.strip()


def main(argv):
    out_json = None
    if len(argv) == 2 and argv[0] == "--json":
        out_json = argv[1]
    sdir = scratch()
    try:
        base = dump_base(sdir)
        oracle = build_oracle(sdir)
        rows = []
        ok = True
        for modes in MODE_SETS:
            for summary in SUMMARIES:
                b = run_tool(base, summary, modes, sdir)
                c = run_tool(CANDIDATE, summary, modes, sdir)
                if b["rc"] != 0 or c["rc"] != 0:
                    ok = False
                rows.append({"summary": summary, "modes": modes, "base": b, "candidate": c})

        compare = []
        for pattern in HOST_PATTERNS:
            for text in SUMMARIES:
                o = oracle_verdict(oracle, pattern, text)
                import re as _re
                try:
                    p = "match" if _re.search(pattern, text) else "nomatch"
                except Exception:
                    p = "invalid"
                agree = (o == p)
                if not agree:
                    ok = False
                compare.append({"pattern": pattern, "text": text,
                                "oracle": o, "python_re": p, "agree": agree})

        payload = {"config": CONFIG, "home": HOME,
                   "base": base, "candidate": CANDIDATE,
                   "rows": rows, "compare": compare}
        text = json.dumps(payload, indent=1, sort_keys=True)
        if out_json:
            with open(out_json, "w", encoding="utf-8") as handle:
                handle.write(text + "\n")
        print(text)
        return 0 if ok else 1
    finally:
        shutil.rmtree(sdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
