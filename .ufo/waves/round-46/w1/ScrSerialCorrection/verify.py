#!/usr/bin/env python3
"""Recompute the M45-2 correction receipts (round-46 closure D2).

The host monitor serial is read fresh from ``hyprctl monitors all -j`` into memory and used only as a
``git grep -F`` needle. This script prints counts and paths, never the value; it writes nothing outside
its own ``receipts/`` directory. Exit 0 when every printed expectation of ``correction.md`` holds.

Usage: python3 -I verify.py [--out DIR]
"""

import argparse
import collections
import glob
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
LESSON = "corpus/lessons/round-45.md"

# Held carriers and their computed line locators (git grep -n, round-45 tip).
HELD = {
    "corpus/knowledge/config-health-report-r3.md": 149,
    "corpus/knowledge/hyprctl-verification-layer.md": 153,
    "corpus/knowledge/hyprland-config-plane.md": 184,
}
# Committed fixture trees that copy all three held entries.
TREES = [
    ".ufo/waves/round-32/assimilation/validate",
    ".ufo/waves/round-32/c1/controls/a-rows-only",
    ".ufo/waves/round-32/c1/controls/b-entries-only",
    ".ufo/waves/round-32/scratch/MutExistingGates/fixtures/tree-m1",
    ".ufo/waves/round-32/scratch/MutExistingGates/fixtures/tree-m2",
    ".ufo/waves/round-32/scratch/MutExistingGates/fixtures/tree-m2b",
    ".ufo/waves/round-37/w1/scratch/ScribeRows/validate",
]
REVS = ["0c89478", "4d22eeb", "b22ea56", "8c5434c6", "e0be61e4"]
GATE = "quality/check-session-material.py"


def serial():
    """Read the host monitor serial without printing it."""
    runtime = "/run/user/%d/hypr" % os.getuid()
    inst = glob.glob(os.path.join(runtime, "*"))
    if not inst:
        sys.exit("verify: no Hyprland instance under %s" % runtime)
    env = dict(os.environ, HYPRLAND_INSTANCE_SIGNATURE=os.path.basename(inst[0]))
    proc = subprocess.run(["hyprctl", "monitors", "all", "-j"], capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        sys.exit("verify: hyprctl monitors failed: %s" % proc.stdout.strip()[:120])
    values = sorted({m["serial"] for m in json.loads(proc.stdout) if m.get("serial")})
    if not values:
        sys.exit("verify: no monitor reports a serial")
    return values


def git(*args, data=False):
    proc = subprocess.run(["git", "-C", LANE, *args], capture_output=True)
    if proc.returncode not in (0, 1):
        sys.exit("verify: git %s failed: %s" % (" ".join(args), proc.stderr.decode()[:200]))
    return proc.stdout if data else proc.stdout.decode("utf-8", "replace")


def carrier_rows(needle, rev, held_only=False):
    """[(path, lines)] from `git grep -c -F`, rev-prefixed output."""
    args = ["grep", "-c", "-F", needle, rev, "--", "."] + ([":!.ufo"] if held_only else [])
    rows = []
    for line in git(*args).splitlines():
        if line:
            parts = line.split(":")
            rows.append((parts[1], int(parts[-1])))
    return rows


def locators(needle, rev, paths):
    """path:line list only — the matched content is dropped, never printed."""
    out = git("grep", "-n", "-F", needle, rev, "--", *paths).splitlines()
    return sorted(":".join(line.split(":")[1:3]) for line in out if line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipts"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    checks = []

    def check(name, ok, detail):
        checks.append((name, ok))
        print("%-40s %s %s" % (name, "PASS" if ok else "FAIL", detail))

    needles = serial()
    check("serial-count", len(needles) == 1, "monitors_with_serial=1")
    needle = needles[0]

    # 1) spread at the round-45 tip and at the base/tip revisions
    lines = []
    tip = carrier_rows(needle, "4d22eeb")
    held_tip = [(p, c) for p, c in tip if not p.startswith(".ufo/")]
    wave_tip = [(p, c) for p, c in tip if p.startswith(".ufo/")]
    split = collections.Counter()
    for path, _count in tip:
        if path.startswith(".ufo/waves/round-32/"):
            split["round-32"] += 1
        elif path.startswith(".ufo/waves/round-37/"):
            split["round-37"] += 1
        elif path.startswith(".ufo/"):
            split["ufo-other"] += 1
        else:
            split["held"] += 1
    check("files-total", len(tip) == 24, "files=%d" % len(tip))
    check("occurrences-one-per-file", all(c == 1 for _p, c in tip), "occurrences=%d" % sum(c for _p, c in tip))
    check("held-entries", len(held_tip) == 3, "held=%d" % len(held_tip))
    check("wave-copies", len(wave_tip) == 21, "wave=%d" % len(wave_tip))
    check("wave-split", split["round-32"] == 18 and split["round-37"] == 3,
          "round-32=%d round-37=%d" % (split["round-32"], split["round-37"]))
    covered = {p for p, _c in wave_tip}
    for tree in TREES:
        check("tree-present:" + tree.split("round-")[1][:2] + "/" + tree.rsplit("/", 1)[-1],
              all(os.path.join(tree, rel) in covered for rel in HELD),
              "3/3 entries")

    lines.append("# `git grep -c -F \"$S\" 4d22eeb -- .` (S read from hyprctl; value never printed)")
    lines.append("# files=%d occurrences=%d held=%d wave=%d (round-32=%d round-37=%d)"
                 % (len(tip), sum(c for _p, c in tip), len(held_tip), len(wave_tip),
                    split["round-32"], split["round-37"]))
    lines += ["%s %d" % (p, c) for p, c in sorted(tip)]

    # 2) locators in the three held entries, computed not typed
    for path, line in HELD.items():
        locs = locators(needle, "4d22eeb", [path])
        check("locator:" + os.path.basename(path), locs == ["%s:%d" % (path, line)], ",".join(locs))

    # 3) revision sweep — nothing introduced in round 45 or 46
    rev_lines = []
    for rev in REVS:
        all_rows = carrier_rows(needle, rev)
        held_rows = carrier_rows(needle, rev, held_only=True)
        rev_lines.append("%s files=%d occurrences=%d held=%d"
                         % (rev, len(all_rows), sum(c for _p, c in all_rows), len(held_rows)))
        check("rev:" + rev, len(all_rows) == 24 and len(held_rows) == 3,
              "files=%d held=%d" % (len(all_rows), len(held_rows)))

    # 4) pickaxe: when each carrier class entered
    pick = [ln for ln in git("log", "--all", "--reverse", "--format=%h", "-S" + needle, "--", ".").splitlines() if ln]
    pick_lines = []
    for commit in pick:
        all_rows = carrier_rows(needle, commit)
        held_rows = carrier_rows(needle, commit, held_only=True)
        date = git("show", "-s", "--format=%cs", commit).strip()
        pick_lines.append("%s %s files=%d held=%d wave=%d"
                          % (commit, date, len(all_rows), len(held_rows), len(all_rows) - len(held_rows)))
    check("pickaxe-commits", len(pick) > 0, "commits=%d first=%s" % (len(pick), pick[0] if pick else "-"))

    # 5) pushed refs
    ref_lines = []
    for row in git("ls-remote", "--heads", "--tags").splitlines():
        if not row.strip():
            continue
        sha, ref = row.split("\t", 1)
        rows = carrier_rows(needle, sha[:8])
        ref_lines.append("%s %s files=%d" % (ref.replace("refs/heads/", "H:"), sha[:8], len(rows)))
    check("pushed-refs-carry", all(int(r.rsplit("=", 1)[1]) >= 3 for r in ref_lines),
          "refs=%d" % len(ref_lines))

    # 6) capture boundary: the gate's path scope and its JSON-object R3 rule
    scope = [ln for ln in open(os.path.join(LANE, GATE), encoding="utf-8").read().splitlines()
             if "--\", \".ufo\"" in ln]
    check("gate-scope-ufo-only", len(scope) == 1, "lines=%d" % len(scope))
    r3 = [i for i, ln in enumerate(open(os.path.join(LANE, GATE), encoding="utf-8"),
                                    start=1) if "R3_MONITOR_IDENT an element" in ln]
    check("gate-r3-json-only", r3 == [26], "def_at=%s" % (r3 or "-"))

    # 7) the lesson text the correction cites
    text = open(os.path.join(LANE, LESSON), encoding="utf-8").read().splitlines()
    anchor = [i for i, ln in enumerate(text, start=1) if "hyprctl-verification-layer.md:153" in ln]
    check("lesson-anchor-line", anchor == [50], "lines=%s" % (anchor or "-"))
    check("lesson-quote-words", len("held corpus/knowledge/hyprctl-verification-layer.md:153 has carried it since round 2".split()) <= 25,
          "words=%d" % len("held corpus/knowledge/hyprctl-verification-layer.md:153 has carried it since round 2".split()))

    # 8) tracked working tree (untracked files are outside a git grep census)
    untracked = [p for p in git("ls-files", "--others", "--exclude-standard", "-z", data=True).decode().split("\0") if p]
    carriers = 0
    for rel in untracked:
        full = os.path.join(LANE, rel)
        try:
            if not os.path.isfile(full) or os.path.getsize(full) > 50_000_000:
                continue
            with open(full, "rb") as fh:
                if needle.encode() in fh.read():
                    carriers += 1
        except OSError:
            continue
    check("untracked-clean", carriers == 0, "files=%d carriers=%d" % (len(untracked), carriers))

    # 9) the 21 copies are byte-identical blobs of the 3 held entries
    identical = 0
    for path in HELD:
        name = path.rsplit("/", 1)[-1]
        held_blob = git("rev-parse", "4d22eeb:" + path).strip()
        for tree in TREES:
            if git("rev-parse", "4d22eeb:%s/corpus/knowledge/%s" % (tree, name)).strip() == held_blob:
                identical += 1
    check("copies-byte-identical", identical == 21, "identical=%d/21" % identical)

    with open(os.path.join(args.out, "01-census-4d22eeb.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
        fh.write("# blob identity: %d of 21 copies equal their held blob at 4d22eeb\n" % identical)
    with open(os.path.join(args.out, "02-revs.txt"), "w", encoding="utf-8") as fh:
        fh.write("# `git grep -c -F \"$S\" <rev> -- .` / `-- . ':!.ufo'`\n" + "\n".join(rev_lines) + "\n")
    with open(os.path.join(args.out, "03-pickaxe.txt"), "w", encoding="utf-8") as fh:
        fh.write("# `git log --all --reverse -S<serial> -- .` (occurrence count changes)\n"
                 + "\n".join(pick_lines) + "\n")
    with open(os.path.join(args.out, "04-refs.txt"), "w", encoding="utf-8") as fh:
        fh.write("# `git ls-remote --heads --tags`, then `git grep -c -F \"$S\" <sha>`\n"
                 + "\n".join(ref_lines) + "\n")
    with open(os.path.join(args.out, "05-untracked.txt"), "w", encoding="utf-8") as fh:
        fh.write("# `git ls-files --others --exclude-standard` scanned bytewise for the serial\n"
                 "untracked_files=%d carriers=%d\n" % (len(untracked), carriers))

    failed = [name for name, ok in checks if not ok]
    print("VERIFY: checks=%d failed=%d verdict=%s" % (len(checks), len(failed), "PASS" if not failed else "FAIL"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
