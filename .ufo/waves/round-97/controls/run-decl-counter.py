#!/usr/bin/env python3
"""Run a round declaration's published counting command at a revision (harm-watch helper).

Usage: run-decl-counter.py --decl PATH --rev REV --scratch-root DIR [--repo DIR] [--dry-run]

Reads the LAST fenced ```sh block that follows a "**Counting command**" line in the
declaration, substitutes `--rev <...>` / `--rev REV` with --rev and `--scratch-root <...>`
with the scratch dir, then runs it from --repo with bash -lc. Prints the command and its
exit code; the caller checks the verdict line. No writes outside the scratch root.
"""
import argparse, os, re, shlex, subprocess, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--decl", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--repo", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--index", type=int, default=0, help="1-based counting-command block; 0 = last")
    ap.add_argument("--force-rev", action="store_true", help="replace any --rev <hex> with --rev REV")
    a = ap.parse_args()
    text = open(a.decl, encoding="utf-8", errors="replace").read()
    blocks = list(re.finditer(r"Counting command[^\n]*\n(?:[^`\n][^\n]*\n|\n)*?```sh\n(.*?)```", text, re.S))
    if not blocks:
        print("SETUP_ERROR no counting-command block", file=sys.stderr)
        return 2
    idx = a.index - 1 if a.index else len(blocks) - 1
    if idx < 0 or idx >= len(blocks):
        print("SETUP_ERROR no counting-command block %d of %d" % (a.index, len(blocks)), file=sys.stderr)
        return 2
    cmd = blocks[idx].group(1)
    if a.force_rev:
        cmd = re.sub(r"--rev\s+[0-9a-f]{40}", "--rev " + a.rev, cmd)
    cmd = re.sub(r"--rev\s+<[^>]*>", "--rev " + a.rev, cmd)
    cmd = re.sub(r"--rev\s+REV\b", "--rev " + a.rev, cmd)
    cmd = re.sub(r"--scratch-root\s+<[^>]*>", "--scratch-root " + a.scratch_root, cmd)
    cmd = re.sub(r"--scratch-root\s+DIR\b", "--scratch-root " + a.scratch_root, cmd)
    repo = a.repo or os.getcwd()
    print("CMD " + " ".join(cmd.split()))
    if a.dry_run:
        return 0
    os.makedirs(a.scratch_root, exist_ok=True)
    r = subprocess.run(["bash", "-lc", cmd], cwd=repo)
    print("EXIT %d" % r.returncode)
    return r.returncode

if __name__ == "__main__":
    sys.exit(main())
