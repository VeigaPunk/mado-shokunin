#!/usr/bin/env python3
"""Round-99 C2 measurement runner.

Runs the frozen C2 counting command (the declaration's freeze block) against the
measured revision and writes the receipt. The counter's own output is the only
content; this wrapper adds the command header, the date and the exit code.
"""
import datetime
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r99/c2-measured-r99"
RECEIPT = os.path.join(LANE, ".ufo/waves/round-99/receipts/c2-measured-r99.txt")

CMD = [
    "python3", "-I", "quality/counters/c2-r99-harm-watch.py",
    "--repo", ".",
    "--rev", "3b69f04113a235aace713bc1c84ea2b695606b6a",
    "--base-rev", "2cbaa141f42df9dfeee4d207cae6558a4dd59863",
    "--panel", ".ufo/waves/round-99/controls/harm-panel-r99.json",
    "--expect-panel-sha256",
    "160763ce7aa447016bad8e5b2c5a7c25f8866b1e8724d8eb0b75d8abb1dae39a",
    "--planted-dir", ".ufo/waves/round-99/controls/harm-planted",
    "--expect-gate-sha256",
    "37a0544b160d9c5c5568fc45f9ed309f41b36fb093983313d72699423b4165b9",
    "--scratch-root", SCRATCH,
]


def main():
    proc = subprocess.run(CMD, cwd=LANE, capture_output=True, text=True)
    out = proc.stdout or ""
    err = proc.stderr or ""
    head = ("# C2 counting receipt (round 99, hyaku run 15, attempt 4)\n"
            "# command: " + " ".join(CMD) + "\n"
            "# date: " + datetime.date.today().isoformat() + "\n\n")
    body = head + out
    if err:
        body += "\n# stderr:\n" + err
    body += "\n# exit: %d\n" % proc.returncode
    with open(RECEIPT, "w", encoding="utf-8") as fh:
        fh.write(body)
    sys.stdout.write(out)
    sys.stderr.write(err)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
