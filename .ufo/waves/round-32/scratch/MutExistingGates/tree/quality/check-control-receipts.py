#!/usr/bin/env python3
"""Round-27 successor of the QUALITY criterion 36 checker (round-26 spot-check §7 repairs 2 and 5).

Usage:
    python3 -I check-control-receipts.py --round N --data-registry PATH [--repo PATH] [--tip REV]
                                         [--shapes S1,S2,...] [--seeds N]
                                         [--receipt-glob PATTERN ...] [--any-md] [--counter-sha SHA]

Reads only git history and blobs at TIP (git log, show) with GIT_OPTIONAL_LOCKS=0; never writes.

Rule (one sentence): exit 0 only if, at TIP, the oldest commit that adds a qualifying control
receipt under `.ufo/waves/round-N/controls/` has a committer time strictly earlier than the
`createdAt` of the named data-wave registry, and every named shape is covered by at least
`--seeds` distinct qualifying receipts; exit 1 otherwise; exit 2 when the history cannot be
evaluated.

Differences from the round-26 checker (which stays in round-26/quality/ and is read-only here):
  * `--receipt-glob PATTERN` (repeatable) — repair 5. Round-26's pre-data controls landed as
    `.txt` counter transcripts and the round-26 checker, which only ever looked at `.md`, exited
    1 with `reason=no-receipt-under-...`. A receipt is now selected by extension/path instead
    of format. Default patterns are `*.md` and `*.txt`; a pattern matches a controls/ path when
    it matches the path relative to `controls/` or that path's basename (case-insensitive and
    `*` crosses `/`), so the defaults reach every depth (`controls/v2/x.txt` included). A
    pattern that matches nothing is not an error: it fails as `receipts=0`.
  * The `CONTROL ` / `# Control` marker line is required of markdown receipts only. A verbatim
    counter log carries `exit=` and no markdown marker by construction; demanding one would
    keep repair 5 red. `--any-md` keeps its round-26 meaning (every markdown receipt under the
    globs qualifies, marker or not).
  * `--seeds N` (default 1) — repair 2, M26-9. Every named shape must be covered by at least N
    distinct receipts; a receipt covers a shape when its file name contains one of the shape's
    `|` alternatives (case-insensitive). A pre-data control set registered "two fresh seeds"
    per shape therefore fails at one receipt per shape instead of passing.
  * `--counter-sha SHA` (repeatable), the `updatedAt` exclusion and the strict `<` ordering are
    unchanged from round 26, as are the exit codes and the printed field order (new fields are
    appended, so a stored round-26 receipt line remains a substring of the current line).

Definitions
  qualifying receipt  a file under `.ufo/waves/round-N/controls/` (any depth) matching one of
                      `--receipt-glob`; a `.md` receipt additionally needs a line starting with
                      `CONTROL ` or `# Control` (case-sensitive) unless --any-md is given; and,
                      when `--counter-sha` is given, whose first line names one of those shas.
  receipt commit      the oldest commit reachable from TIP (`git log --reverse --diff-filter=A`)
                      adding a qualifying file; its committer time (`%ct`). Older wins: a later
                      receipt commit never supplies the timestamp.
  data registry       PATH (repo-relative), read at TIP; its JSON `createdAt` (ISO 8601) is when
                      the data seats were created. `updatedAt` is never consulted.
  shapes              comma list (default: DoNothing,EmptyArray|AllFalse,Junk,Echo,LabelKeyed,
                      NoReader); both coverage and seed counts key on the receipt file name,
                      after the glob and marker/sha filters.

Exit codes: 0 pass; 1 fail; 2 unevaluable (bad tip, unreadable registry, no adding commit).
"""
import argparse, datetime, fnmatch, json, os, re, subprocess, sys

DEFAULT_SHAPES = "DoNothing,EmptyArray|AllFalse,Junk,Echo,LabelKeyed,NoReader"
DEFAULT_GLOBS = ("*.md", "*.txt")
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


def seeds_arg(value):
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("--seeds expects a positive integer, got %r" % value)
    if n < 1:
        raise argparse.ArgumentTypeError("--seeds expects a positive integer, got %r" % value)
    return n


def has_marker(text):
    return any(l.startswith("CONTROL ") or l.startswith("# Control") for l in text.split("\n"))


def names_counter(text, counter_shas):
    if not counter_shas:
        return True
    first = text.split("\n", 1)[0].lower()
    return any(s in first for s in counter_shas)


def selected(rel, globs):
    """True when a controls-relative path matches the globs as given or by basename."""
    rel = rel.lower()
    base = rel.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatchcase(rel, p.lower()) or fnmatch.fnmatchcase(base, p.lower())
               for p in globs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--data-registry", required=True)
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--tip", default="HEAD")
    ap.add_argument("--shapes", default=DEFAULT_SHAPES)
    ap.add_argument("--seeds", type=seeds_arg, default=1, metavar="N",
                    help="distinct receipts required per named shape (default 1)")
    ap.add_argument("--receipt-glob", action="append", default=[], metavar="PATTERN",
                    help="controls-relative path or basename glob; repeatable "
                         "(default %s)" % ", ".join(DEFAULT_GLOBS))
    ap.add_argument("--any-md", action="store_true")
    ap.add_argument("--counter-sha", action="append", type=sha_arg, default=[], metavar="SHA")
    a = ap.parse_args()
    cdir = ".ufo/waves/round-%d/controls/" % a.round
    globs = a.receipt_glob or list(DEFAULT_GLOBS)
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
    excluded_glob = 0
    for f in files.decode().split("\n"):
        if not f:
            continue
        rel = f[len(cdir):] if f.startswith(cdir) else f
        if not selected(rel, globs):
            excluded_glob += 1
            continue
        rc, b = git(a.repo, "show", "%s:%s" % (tip, f))
        if rc:
            continue
        text = b.decode("utf-8", "replace")
        if f.lower().endswith(".md") and not (a.any_md or has_marker(text)):
            continue
        if not names_counter(text, a.counter_sha):
            excluded_sha += 1
            continue
        receipts.append(f)
    print("tip=%s round=%d receipts=%d counter_sha=%s excluded_by_counter_sha=%d "
          "receipt_glob=%s excluded_by_glob=%d seeds=%d"
          % (tip, a.round, len(receipts), ",".join(a.counter_sha) or "-", excluded_sha,
             ",".join(globs), excluded_glob, a.seeds))
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
    names = [os.path.basename(r).lower() for r in receipts]
    counts = {}
    missing = []
    for shape in a.shapes.split(","):
        opts = [o.strip().lower() for o in shape.split("|") if o.strip()]
        n = sum(1 for name in names if any(o in name for o in opts))
        counts[shape] = n
        if n == 0:
            missing.append(shape)
    short = [s for s in counts if counts[s] < a.seeds]
    print("order=%s gap_s=%.0f shapes_missing=%s seeds_short=%s"
          % ("ok" if order_ok else "LATE", cts - first[1],
             ",".join(missing) or "-",
             ",".join("%s(%d<%d)" % (s, counts[s], a.seeds) for s in short) or "-"))
    print("shape_counts=%s" % ",".join("%s:%d" % (s, counts[s]) for s in counts))
    ok = order_ok and not missing and not short
    print("CONTROL_RECEIPTS verdict=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
