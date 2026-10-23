#!/usr/bin/env python3
"""Round-25 quality check for QUALITY criterion 36 (M24-2, M24-5): control receipts land before data.

Usage:
    python3 -I check-control-receipts.py --round N --data-registry PATH [--repo PATH] [--tip REV]
                                         [--shapes S1,S2,...]

Reads only git history and blobs at TIP (git log, show) with GIT_OPTIONAL_LOCKS=0; never writes.

Rule (one sentence): exit 0 only if, at TIP, the earliest commit that adds a control receipt under
`.ufo/waves/round-N/controls/` has a committer time strictly earlier than the `createdAt` of the
named data-wave registry, and the receipt files present at TIP cover every named shortcut shape;
exit 1 otherwise; exit 2 when the history cannot be evaluated.

Definitions
  control receipt   a `.md` file under `.ufo/waves/round-N/controls/` (any depth) whose bytes contain
                    a line starting with `CONTROL ` or `# Control` (case-sensitive), or any `.md`
                    there when --any-md is given.
  receipt commit    the oldest commit reachable from TIP (`git log --reverse --diff-filter=A`) adding
                    such a file; its committer time (`%ct`).
  data registry     PATH (repo-relative), read at TIP; its JSON `createdAt` (ISO 8601) is when the
                    data seats were created. Which wave is the data wave is the caller's declaration,
                    printed in the receipt.
  shapes            comma list (default: DoNothing,EmptyArray|AllFalse,Junk,Echo,LabelKeyed,NoReader);
                    a shape is covered when some receipt file name contains one of its `|` options
                    (case-insensitive).
"""
import argparse, datetime, json, os, subprocess, sys

DEFAULT_SHAPES = "DoNothing,EmptyArray|AllFalse,Junk,Echo,LabelKeyed,NoReader"


def git(repo, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, env=env)
    return p.returncode, p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--data-registry", required=True)
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--tip", default="HEAD")
    ap.add_argument("--shapes", default=DEFAULT_SHAPES)
    ap.add_argument("--any-md", action="store_true")
    a = ap.parse_args()
    cdir = ".ufo/waves/round-%d/controls/" % a.round
    rc, tip = git(a.repo, "rev-parse", "--verify", a.tip + "^{commit}")
    if rc:
        print("UNEVALUABLE bad tip %s" % a.tip)
        return 2
    tip = tip.decode().strip()
    rc, files = git(a.repo, "ls-tree", "-r", "--name-only", tip, "--", cdir)
    if rc:
        print("UNEVALUABLE ls-tree failed")
        return 2
    receipts = []
    for f in files.decode().split("\n"):
        if not f.endswith(".md"):
            continue
        rc, b = git(a.repo, "show", "%s:%s" % (tip, f))
        if rc:
            continue
        text = b.decode("utf-8", "replace")
        if a.any_md or any(l.startswith("CONTROL ") or l.startswith("# Control") for l in text.split("\n")):
            receipts.append(f)
    print("tip=%s round=%d receipts=%d" % (tip, a.round, len(receipts)))
    if not receipts:
        print("CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-%s" % cdir)
        return 1
    rc, log = git(a.repo, "log", "--reverse", "--diff-filter=A", "--format=@%H %ct", "--name-only", tip, "--", *receipts)
    if rc:
        print("UNEVALUABLE git log failed")
        return 2
    first = None
    cur = None
    for line in log.decode().split("\n"):
        if line.startswith("@"):
            h, ct = line[1:].split()
            cur = (h, int(ct))
        elif line.strip() and cur and first is None:
            first = cur
    if first is None:
        print("UNEVALUABLE no adding commit found")
        return 2
    rc, reg = git(a.repo, "show", "%s:%s" % (tip, a.data_registry))
    if rc:
        print("UNEVALUABLE data registry %s absent at tip" % a.data_registry)
        return 2
    try:
        created = json.loads(reg)["createdAt"]
        cts = datetime.datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp()
    except Exception as ex:  # noqa: BLE001
        print("UNEVALUABLE createdAt unreadable: %r" % ex)
        return 2
    rt = datetime.datetime.fromtimestamp(first[1], datetime.timezone.utc).isoformat()
    print("receipt_commit=%s committed=%s data_registry=%s createdAt=%s" % (first[0][:12], rt, a.data_registry, created))
    order_ok = first[1] < cts
    missing = []
    names = [os.path.basename(r).lower() for r in receipts]
    for shape in a.shapes.split(","):
        opts = [o.strip().lower() for o in shape.split("|") if o.strip()]
        if not any(o in n for o in opts for n in names):
            missing.append(shape)
    print("order=%s gap_s=%.0f shapes_missing=%s" % ("ok" if order_ok else "LATE", cts - first[1], ",".join(missing) or "-"))
    ok = order_ok and not missing
    print("CONTROL_RECEIPTS verdict=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
