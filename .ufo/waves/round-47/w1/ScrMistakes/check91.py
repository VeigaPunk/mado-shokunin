#!/usr/bin/env python3
"""check91 — a cited run receipt names the landed surface as its producer (proposed criterion 91).

Reads a knowledge entry and every `.ufo/waves/round-N/receipts/<file>` it cites, reads each cited
receipt at REV, extracts its producer line (`live host run of <path> (sha256 <hex>)`), and requires
the producer path to equal --tool and its hash at REV to equal the receipt's stated hash.

Exit 0 = every cited receipt names --tool and its hash matches at REV; 1 = DIFFER; 2 = setup error.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

CITE = re.compile(r"\.ufo/waves/round-\d+/receipts/[A-Za-z0-9._-]+")
PROD = re.compile(r"(?:run of|reference\s*\()\s*([A-Za-z0-9_./-]+\.py)[^)]*?sha256\s*([0-9a-f]{64})")


def _at(git, repo, rev, path):
    return git(repo, "cat-file", "-e", "%s:%s" % (rev, path)).returncode == 0


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--entry", required=True)
    ap.add_argument("--tool", required=True)
    a = ap.parse_args()
    try:
        text = open(a.entry, encoding="utf-8").read()
    except OSError as e:
        print("CHECK91: verdict=SETUP_ERROR %s" % e)
        return 2
    cites = sorted(set(CITE.findall(text)))
    differ = unparsed = absent = 0
    for p in cites:
        r = git(a.repo, "show", "%s:%s" % (a.rev, p))
        if r.returncode != 0:
            print("PRODUCER %s verdict=ABSENT_AT_REV" % p)
            absent += 1
            continue
        head = r.stdout.decode("utf-8", "replace").splitlines()[:4]
        m = None
        for line in head:
            m = PROD.search(line)
            if m:
                break
        if not m:
            print("PRODUCER %s verdict=UNPARSED" % p)
            unparsed += 1
            continue
        producer, stated = m.group(1), m.group(2)
        # A receipt's producer may be named relative to its wave directory.
        wave = os.path.dirname(os.path.dirname(p))
        cand = producer if _at(git, a.repo, a.rev, producer) else os.path.join(wave, producer)
        blob = git(a.repo, "show", "%s:%s" % (a.rev, cand))
        actual = hashlib.sha256(blob.stdout).hexdigest() if blob.returncode == 0 else "absent"
        verdict = "AGREE" if producer == a.tool and actual == stated else "DIFFER"
        print("PRODUCER %s producer=%s (at %s) stated=%s at_rev=%s want=%s verdict=%s"
              % (p, producer, cand, stated[:12], actual[:12], a.tool, verdict))
        if verdict == "DIFFER":
            differ += 1
    bad = differ + unparsed + absent
    print("CHECK91: rev=%s entry=%s receipts=%d differ=%d unparsed=%d absent=%d verdict=%s"
          % (a.rev[:12], a.entry, len(cites), differ, unparsed, absent, "AGREE" if bad == 0 else "DIFFER"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
