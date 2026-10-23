#!/usr/bin/env python3
"""Round-26 successor of the QUALITY criterion 36 checker (repair R4 of the M25-3 survivors).

Usage:
    python3 -I check-control-receipts.py --round N --data-registry PATH [--repo PATH] [--tip REV]
                                         [--shapes S1,S2,...] [--any-md] [--counter-sha SHA]

Reads only git history and blobs at TIP (git log, show) with GIT_OPTIONAL_LOCKS=0; never writes.

Rule (one sentence): exit 0 only if, at TIP, the oldest commit that adds a qualifying control
receipt under `.ufo/waves/round-N/controls/` has a committer time strictly earlier than the
`createdAt` of the named data-wave registry, and the qualifying receipts present at TIP cover
every named shortcut shape; exit 1 otherwise; exit 2 when the history cannot be evaluated.

Differences from the round-25 checker (which stays in round-25/quality/):
  * `--counter-sha SHA` (repeatable): when given, only receipts whose FIRST line names one of
    the given 64-hex counter sha256 values (case-insensitive substring) qualify. Without the
    flag the filter is off and behaviour is byte-for-byte the round-25 verdict.
  * The registry's `updatedAt` is never consulted; only `createdAt` is read.
  * `excluded_by_counter_sha=N` and `counter_sha=...` are printed so a receipt can show that
    the filter both matched and excluded something.

Definitions
  qualifying receipt  a `.md` file under `.ufo/waves/round-N/controls/` (any depth) whose bytes
                      contain a line starting with `CONTROL ` or `# Control` (case-sensitive), or
                      any `.md` there when --any-md is given; and, when --counter-sha is given,
                      whose first line names one of those shas.
  receipt commit      the oldest commit reachable from TIP (`git log --reverse --diff-filter=A`)
                      adding a qualifying file; its committer time (`%ct`). Older wins: a later
                      receipt commit never supplies the timestamp.
  data registry       PATH (repo-relative), read at TIP; its JSON `createdAt` (ISO 8601) is when
                      the data seats were created. Which wave is the data wave is the caller's
                      declaration, printed in the receipt.
  shapes              comma list (default: DoNothing,EmptyArray|AllFalse,Junk,Echo,LabelKeyed,
                      NoReader); a shape is covered when some qualifying receipt file name
                      contains one of its `|` options (case-insensitive).

Exit codes: 0 pass; 1 fail; 2 unevaluable (bad tip, unreadable registry, no adding commit).
"""
import argparse, datetime, json, os, re, subprocess, sys

DEFAULT_SHAPES = "DoNothing,EmptyArray|AllFalse,Junk,Echo,LabelKeyed,NoReader"
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def git(repo, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, env=env)
    return p.returncode, p.stdout


def sha_arg(value):
    if not HEX64.match(value):
        raise argparse.ArgumentTypeError("--counter-sha expects 64 hex characters, got %r" % value)
    return value.lower()


def has_marker(text):
    return any(l.startswith("CONTROL ") or l.startswith("# Control") for l in text.split("\n"))


def names_counter(text, counter_shas):
    if not counter_shas:
        return True
    first = text.split("\n", 1)[0].lower()
    return any(s in first for s in counter_shas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--data-registry", required=True)
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--tip", default="HEAD")
    ap.add_argument("--shapes", default=DEFAULT_SHAPES)
    ap.add_argument("--any-md", action="store_true")
    ap.add_argument("--counter-sha", action="append", type=sha_arg, default=[], metavar="SHA")
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
    excluded_sha = 0
    for f in files.decode().split("\n"):
        if not f.endswith(".md"):
            continue
        rc, b = git(a.repo, "show", "%s:%s" % (tip, f))
        if rc:
            continue
        text = b.decode("utf-8", "replace")
        if not (a.any_md or has_marker(text)):
            continue
        if not names_counter(text, a.counter_sha):
            excluded_sha += 1
            continue
        receipts.append(f)
    print("tip=%s round=%d receipts=%d counter_sha=%s excluded_by_counter_sha=%d"
          % (tip, a.round, len(receipts), ",".join(a.counter_sha) or "-", excluded_sha))
    if not receipts:
        print("CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-%s" % cdir)
        return 1
    rc, log = git(a.repo, "log", "--reverse", "--diff-filter=A", "--format=@%H %ct", "--name-only",
                  tip, "--", *receipts)
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
    print("receipt_commit=%s committed=%s data_registry=%s createdAt=%s"
          % (first[0][:12], rt, a.data_registry, created))
    order_ok = first[1] < cts
    missing = []
    names = [os.path.basename(r).lower() for r in receipts]
    for shape in a.shapes.split(","):
        opts = [o.strip().lower() for o in shape.split("|") if o.strip()]
        if not any(o in n for o in opts for n in names):
            missing.append(shape)
    print("order=%s gap_s=%.0f shapes_missing=%s"
          % ("ok" if order_ok else "LATE", cts - first[1], ",".join(missing) or "-"))
    ok = order_ok and not missing
    print("CONTROL_RECEIPTS verdict=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
