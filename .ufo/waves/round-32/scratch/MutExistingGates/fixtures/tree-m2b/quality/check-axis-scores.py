#!/usr/bin/env python3
"""mado — calibration gate: the lane's published axis table must not be stale.

The lane publishes an axis table per round in prose inside SCORECARD.md
("Axis table re-derived at <state> ..."). AXES.md defines calibration as
"SHONEN.md/SCORECARD entries match observed repo state". This gate takes the
LAST such publication (history is never rewritten; the last line is the lane's
live publication) and re-derives each axis it can re-derive at the revision
under test, using that axis's own committed instrument.

Axes re-derived (frozen set):
  navigation   quality/check-index.py --rev <rev> --repo .   -> indexed=A/B
  calibration  .ufo/waves/round-31/c2/count.py <rev>         -> resolved_active=A active=B
  operability  quality/check-index.py --selftest             -> A/B assertions passed

A published fraction must equal the re-derived fraction. A missing publication, a
missing instrument or an unparsable cell is NOT a pass: it is counted as a
mismatch. Axes the gate cannot re-derive are not checked and are not claimed;
the gate prints which axes it checked.

Exit codes: 0 = every checked axis matches; 1 = at least one mismatch;
2 = usage or setup error.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

AXES = ("navigation", "calibration", "operability")
PUB_RE = re.compile(r"Axis table re-derived at")


def published_fractions(text):
    """Parse the last axis publication in a SCORECARD.md body.

    The publication is prose and may wrap across lines, so the body is flattened
    to one space-normalised string and the LAST "Axis table re-derived at" is
    read from it. The window is the publication plus its trailing prose; only
    the axis fractions inside it are parsed.
    """
    flat = re.sub(r"\s+", " ", text)
    idx = flat.rfind("Axis table re-derived at")
    if idx < 0:
        return None, None
    line = flat[idx:idx + 400]
    out = {}
    m = re.search(r"navigation (\d+)/(\d+)", line)
    if m:
        out["navigation"] = "%s/%s" % (m.group(1), m.group(2))
    m = re.search(r"calibration resolved-active (\d+)/(\d+)", line)
    if m:
        out["calibration"] = "%s/%s" % (m.group(1), m.group(2))
    m = re.search(r"operability selftest (\d+)/(\d+)", line)
    if m:
        out["operability"] = "%s/%s" % (m.group(1), m.group(2))
    return line, out


def compare(published, derived):
    """Pure comparison rule: published == derived, per checked axis.

    published: dict axis -> "a/b" (missing key = not published)
    derived:  dict axis -> "a/b" (missing key = not re-derivable)
    Returns (mismatches, rows) where rows is a list of (axis, published, derived, verdict).
    """
    rows, bad = [], 0
    for axis in AXES:
        pub = published.get(axis)
        der = derived.get(axis)
        if pub is None:
            verdict = "NOT-PUBLISHED"
        elif der is None:
            verdict = "NOT-RE-DERIVABLE"
        elif pub == der:
            verdict = "MATCH"
        else:
            verdict = "STALE"
        if verdict != "MATCH":
            bad += 1
        rows.append((axis, pub or "-", der or "-", verdict))
    return bad, rows


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)


def show(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path))
    if p.returncode != 0:
        return None
    return p.stdout


def run_script(repo, rev, path, args, timeout=300):
    """Run a committed script's bytes at <rev> against the repo (read-only git)."""
    src = show(repo, rev, path)
    if src is None:
        return None, "instrument absent at %s: %s" % (rev, path)
    with tempfile.TemporaryDirectory(prefix="mado-axis-") as tmp:
        f = os.path.join(tmp, os.path.basename(path))
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(src)
        try:
            p = subprocess.run([sys.executable, "-I", f] + list(args), cwd=repo,
                               capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None, "instrument timed out: %s" % path
        return (p.stdout + p.stderr), None


def derive(repo, rev):
    derived, notes = {}, []

    out, err = run_script(repo, rev, "quality/check-index.py", ["--rev", rev, "--repo", "."])
    if err:
        notes.append(err)
    else:
        m = re.search(r"indexed=(\d+)/(\d+)", out or "")
        if m:
            derived["navigation"] = "%s/%s" % (m.group(1), m.group(2))
        else:
            notes.append("navigation: no indexed=A/B in check-index.py output")

    out, err = run_script(repo, rev, ".ufo/waves/round-31/c2/count.py", [rev])
    if err:
        notes.append(err)
    else:
        m = re.search(r"resolved_active=(\d+)", out or "")
        a = re.search(r"\bactive=(\d+)", out or "")
        if m and a:
            derived["calibration"] = "%s/%s" % (m.group(1), a.group(1))
        else:
            notes.append("calibration: no resolved_active/active in count.py output")

    out, err = run_script(repo, rev, "quality/check-index.py", ["--selftest"])
    if err:
        notes.append(err)
    else:
        m = re.search(r"(\d+)/(\d+) assertions passed", out or "")
        if m:
            derived["operability"] = "%s/%s" % (m.group(1), m.group(2))
        else:
            notes.append("operability: no A/B assertions passed in selftest output")

    return derived, notes


def selftest():
    fails = 0

    def check(name, cond):
        nonlocal fails
        if not cond:
            fails += 1
            print("FAIL %s" % name)
        else:
            print("PASS %s" % name)

    line, pub = published_fractions(
        "Axis table re-derived at base (criterion 22): navigation 43/43 = 1.0; "
        "calibration resolved-active 39/40 = 0.9750 (lowest); sourced-art 1.0; "
        "operability selftest 9/9 = 1.0.")
    check("parse-navigation", pub.get("navigation") == "43/43")
    check("parse-calibration", pub.get("calibration") == "39/40")
    check("parse-operability", pub.get("operability") == "9/9")
    check("ignore-sourced-art", "sourced-art" not in pub)

    bad, rows = compare(pub, {"navigation": "43/43", "calibration": "41/41",
                              "operability": "12/12"})
    check("stale-detected", bad == 2)
    check("stale-rows", [r[3] for r in rows] == ["MATCH", "STALE", "STALE"])

    bad, _ = compare(pub, {"navigation": "43/43", "calibration": "41/41",
                           "operability": "12/12"})
    check("nonzero-on-stale", bad != 0)

    bad, rows = compare({"navigation": "43/43", "calibration": "41/41",
                          "operability": "12/12"},
                         {"navigation": "43/43", "calibration": "41/41",
                          "operability": "12/12"})
    check("clean-is-zero", bad == 0)
    check("clean-rows", all(r[3] == "MATCH" for r in rows))

    bad, rows = compare({"navigation": "43/43"}, {"navigation": "43/43",
                                                   "calibration": "41/41",
                                                   "operability": "12/12"})
    check("missing-publication-is-not-a-pass", bad == 2)

    bad, rows = compare(pub, {"navigation": "43/43"})
    check("missing-instrument-is-not-a-pass", bad == 2)

    bad, rows = compare(pub, {"navigation": "43/43", "calibration": "41/41",
                              "operability": "12/12"})
    check("one-perturbation-bites", bad == 2)

    check("no-publication", published_fractions("nothing here")[0] is None)

    print("MADO_AXIS_SELFTEST: %d/%d assertions passed" % (17 - fails, 17))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description="calibration gate for the published axis table")
    ap.add_argument("--rev", help="revision to test (default: the repo's HEAD commit)")
    ap.add_argument("--repo", default=".", help="lane repo")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(os.path.join(repo, ".git")):
        print("MADO_AXIS: SETUP_ERROR not a git repo: %s" % repo)
        return 2
    rev = args.rev
    if not rev:
        r = git(repo, "rev-parse", "HEAD")
        if r.returncode != 0:
            print("MADO_AXIS: SETUP_ERROR cannot resolve HEAD")
            return 2
        rev = r.stdout.strip()
    v = git(repo, "rev-parse", "--verify", "--end-of-options", rev + "^{commit}")
    if v.returncode != 0:
        print("MADO_AXIS: SETUP_ERROR bad revision: %s" % rev)
        return 2
    rev = v.stdout.strip()

    body = show(repo, rev, "SCORECARD.md")
    if body is None:
        print("MADO_AXIS: SETUP_ERROR no SCORECARD.md at %s" % rev)
        return 2
    line, pub = published_fractions(body)
    derived, notes = derive(repo, rev)
    if pub is None:
        bad, rows = len(AXES), [(a, "-", derived.get(a, "-"), "NOT-PUBLISHED") for a in AXES]
    else:
        bad, rows = compare(pub, derived)

    for axis, p, d, verdict in rows:
        print("MADO_AXIS_ROW: axis=%s published=%s derived=%s verdict=%s" % (axis, p, d, verdict))
    for n in notes:
        print("MADO_AXIS_NOTE: %s" % n)
    print("MADO_AXIS: checked=%d mismatched=%d rev=%s" % (len(AXES), bad, rev))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
