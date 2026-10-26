#!/usr/bin/env python3
"""make-live-receipt.py — reproduce receipts/live-geometry-host-r44.txt with read-only verbs.

Issues exactly `hyprctl version` and `hyprctl clients -j` (two of the five allowed read
verbs) and joins the dump with the gkeep rule file through the landed tool, feeding the
`clients -j` bytes on standard input exactly as the documented pipe does. Writes
live-run.txt (command, version, tool sha256, stdout, exit, stderr) and keeps only the
four state columns of each client — class, floating, fullscreen, fullscreenClient — never
a title, pid or address, and never the raw dump.

usage: python3 make-live-receipt.py --tool TOOL --rules RULES [--out DIR]
"""
import argparse, hashlib, json, os, subprocess, sys, datetime


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--rules", required=True,
                    default=os.path.expanduser("~/.config/hypr/gkeep.conf"))
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    a = ap.parse_args()
    ver = subprocess.run(["hyprctl", "version"], capture_output=True, check=True).stdout
    version_line = ver.decode().splitlines()[0]
    dump = subprocess.run(["hyprctl", "clients", "-j"], capture_output=True, check=True).stdout
    p = subprocess.Popen(["hyprctl", "clients", "-j"], stdout=subprocess.PIPE)
    run = subprocess.run([sys.executable, "-I", a.tool, "--clients", "-", "--rules",
                          os.path.expanduser(a.rules)], stdin=p.stdout, capture_output=True)
    p.stdout.close(); p.wait()
    tool_sha = hashlib.sha256(open(a.tool, "rb").read()).hexdigest()
    doc = json.loads(dump)
    rows = ["%s %s %s %s" % (c.get("class"), c.get("floating"), c.get("fullscreen"),
                             c.get("fullscreenClient")) for c in doc]
    lines = [
        "# live host run, round 44 data tree; re-run %s" % datetime.datetime.now().astimezone()
        .isoformat(timespec="seconds"),
        "# tool sha256 %s" % tool_sha,
        "# %s" % version_line,
        "$ hyprctl clients -j | python3 -I tools/mado-geometry.py --clients - --rules "
        "~/.config/hypr/gkeep.conf",
    ]
    lines += run.stdout.decode().rstrip().splitlines()
    lines += ["exit=%d" % run.returncode,
              "# fullscreen values carried by the live dump (class, floating, fullscreen, "
              "fullscreenClient):"]
    lines += rows
    lines += ["# raw dump: %d bytes, sha256 %s (raw bytes not retained; titles/pids never printed)"
              % (len(dump), hashlib.sha256(dump).hexdigest()),
              "# stderr: %d bytes" % len(run.stderr)]
    text = "\n".join(lines) + "\n"
    open(os.path.join(a.out, "live-run.txt"), "w").write(text)
    print(text, end="")
    return run.returncode


if __name__ == "__main__":
    sys.exit(main())
