#!/usr/bin/env python3
"""Falsify23 novelty audit (seat-local instrument, not a lane counter).

Question: does the frozen C2 predicate's admitted fixture entry introduce any source bytes or
cited source spans that were not already on the lane's ground at the round-52 base?

Inputs: the fixture repository (candidate entry committed), the lane base tree, and the probe
module's clause-(b) bindings (same row/pin/quote grammar as the committed round-51 counter).

Outputs one JSON record: per-row pin sha256, whether that sha already exists under the base
tree's .ufo/waves fetch dirs, and whether the round-51 entry at base already cites the same
pin:line span with the same quote.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "fixture")
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "85d57a818c3707397e21c840b6498b105ba798aa"


def load_probe():
    spec = importlib.util.spec_from_file_location("probe", os.path.join(HERE, "probe-c2-r52.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True).stdout


def base_fetch_blobs(lane, base):
    """git blob id -> [paths] for every file under .ufo/waves/*/fetch in the base tree.

    A git blob id is a content hash: equal ids mean byte-identical files, which is exactly the
    identity this audit measures (no working-tree bytes are read).
    """
    index = {}
    out = git(lane, "ls-tree", "-r", base, "--", ".ufo/waves").decode().splitlines()
    for line in out:
        meta, path = line.split("\t", 1)
        parts = path.split("/")
        if len(parts) < 5 or parts[3] != "fetch":
            continue
        index.setdefault(meta.split()[2], []).append(path)
    return index


def main():
    probe = load_probe()
    rev = git(FIXTURE, "rev-parse", "HEAD").decode().strip()
    entry = git(FIXTURE, "show", "%s:%s" % (rev, probe.ENTRY)).decode()
    ok, detail = probe.clause_b(FIXTURE, rev, entry)
    verified = probe.LAST_VERIFIED
    r51 = git(LANE, "show", "%s:%s" % (BASE, "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"))
    r51 = r51.decode()
    index = base_fetch_blobs(LANE, BASE)
    pins_new = 0
    rows = []
    for rowid in sorted(verified):
        pin, first, last, quote, _line = verified[rowid]
        path = probe.FETCH_ROOT + "/" + pin
        blob = git(FIXTURE, "show", "%s:%s" % (rev, path))
        sha = hashlib.sha256(blob).hexdigest()
        blob_id = git(FIXTURE, "rev-parse", "%s:%s" % (rev, path)).decode().strip()
        earlier = index.get(blob_id, [])
        span_cited_at_base = ("%s:%d" % (pin, first)) in r51 and quote in r51
        if not earlier:
            pins_new += 1
        rows.append({
            "row": rowid,
            "pin": pin,
            "span": "%s:%d-%d" % (pin, first, last),
            "pin_sha256": sha,
            "pin_already_in_base_fetch": sorted(earlier)[:3],
            "pin_sha_matches_at_base": len(earlier),
            "same_span_and_quote_in_r51_entry_at_base": bool(span_cited_at_base),
        })
    out = {
        "fixture_rev": rev,
        "clause_b": {"ok": ok, "detail": detail},
        "rows": rows,
        "pins_with_no_base_copy": pins_new,
        "pins_with_base_copy": len(rows) - pins_new,
        "rows_reusing_r51_span": sum(1 for r in rows if r["same_span_and_quote_in_r51_entry_at_base"]),
    }
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
