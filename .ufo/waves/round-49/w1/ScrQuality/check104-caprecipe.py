#!/usr/bin/env python3
"""check104-caprecipe.py - candidate criterion 104 (a cap and the recipe it must survive).

Question answered: can the dispatch's own heaviest named recipe complete under
the resource cap the same dispatch carries?

Round-48 M48-13: the a4r1 context required `ulimit -f` before every writer and
named `git clone -q --shared <lane>` as the clone recipe; the lane tracks
evidence files far above that cap, so a checkout cannot complete - two seats
aborted with no report and three fell back to `--no-checkout` clones. Criterion
98 asks whether the cap is executed; this asks whether the cap is *compatible*
with the recipe that runs under it.

Reads committed bytes only: the revision's blob sizes (`git ls-tree -r -l`)
against the cap, and, when a probe receipt is given, its last `PROBE rc=` value.

Usage:
  check104-caprecipe.py --repo REPO --rev REV --cap-bytes N
                        [--recipe checkout|clone|none] [--probe FILE]
Exit: 0 compatible (and probed), 1 incompatible / probe failed required,
      2 usage / unreadable.

Recipe semantics: `checkout` and `clone` both materialise every tracked blob,
so one blob above the cap makes the recipe fail under a per-file cap; `none`
means the dispatch runs no checkout and the cap is only a writer bound.

Declared limit: a per-file cap is not the only failure mode of a clone (the git
index, object packing and rename all matter), so a compatible reading is a
necessary condition, not a pass; the probe receipt is what proves the recipe
ran. Sparse checkout / partial clone recipes need their own recipe name.
"""
import argparse
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--rev", required=True)
    parser.add_argument("--cap-bytes", type=int, required=True)
    parser.add_argument("--recipe", default="checkout")
    parser.add_argument("--probe")
    args = parser.parse_args()

    proc = subprocess.run(["git", "-C", args.repo, "ls-tree", "-r", "-l", args.rev],
                          capture_output=True)
    if proc.returncode != 0:
        print("CHECK104: error=rev-unreadable %s" % args.rev)
        return 2
    over, largest, largest_path, total = [], 0, "-", 0
    for line in proc.stdout.decode("utf-8", "replace").splitlines():
        fields = line.split()
        if len(fields) < 5:
            continue
        try:
            size = int(fields[3])
        except ValueError:
            continue
        total += 1
        if size > largest:
            largest, largest_path = size, fields[4]
        if size > args.cap_bytes:
            over.append((size, fields[4]))
    over.sort(reverse=True)
    for size, path in over:
        print("BLOB_OVER_CAP size=%d cap=%d path=%s" % (size, args.cap_bytes, path))

    bad = 0
    materialises = args.recipe in ("checkout", "clone")
    if over and materialises:
        bad += len(over)
        print("CAP_RECIPE_INCOMPATIBLE recipe=%s cap=%d blobs_over=%d" %
              (args.recipe, args.cap_bytes, len(over)))
    probe = None
    if args.probe:
        try:
            for line in open(args.probe, "r", errors="replace"):
                match = re.search(r'\bPROBE\b.*\brc=(\d+)', line)
                if match:
                    probe = int(match.group(1))
        except OSError as exc:
            print("CHECK104: error=probe-unreadable %s: %s" % (args.probe, exc))
            return 2
        print("PROBE receipt=%s rc=%s" % (args.probe, probe))
        if probe != 0:
            bad += 1
    else:
        print("PROBE absent")
    print("CAP_RECIPE: cap=%d recipe=%s blobs=%d blobs_over=%d max_blob=%d max_path=%s verdict=%s"
          % (args.cap_bytes, args.recipe, total, len(over), largest, largest_path,
             "INCOMPATIBLE" if bad else ("PROBED" if probe == 0 else "UNPROBED")))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
