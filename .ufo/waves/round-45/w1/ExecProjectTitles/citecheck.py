#!/usr/bin/env python3
"""Locator check for every path:line this seat's report cites.

Each citation is verified mechanically at the pin: the line exists and contains the token
the report claims it does. A citation that does not verify fails the run, so the report
cannot drift from the tree.
"""
import subprocess
import sys

PIN = "0c89478af821a6424c9ac922eafe02e39630cf4f"
CITES = [
    # (path, line, token the report says is there)
    (".ufo/waves/round-43/w1/ExecLiveHost/live-census.txt", 109,
     "hyprctl clients -j > host-clients-live.json"),
    (".ufo/waves/round-43/w1/ExecLiveHost/live-census.txt", 112, "6cdada1a"),
    (".ufo/waves/round-43/w1/ExecLiveHost.md", 17, "6cdada1a"),
    (".ufo/waves/round-43/w1/ExecLiveHost.md", 55, "6cdada1a"),
    (".ufo/waves/round-43/w1-results.json", 40, "6cdada1a"),
    (".ufo/waves/round-43/w2/SentLiveRun/hashes.txt", 1, "e4b1fb72"),
    (".ufo/waves/round-44/w1/ExecLiveHost/live-states.txt", 9, "shape-only projection"),
    (".ufo/waves/round-44/w1/ExecLiveHost/live-states.txt", 18, "raw_sha256"),
    (".ufo/waves/round-44/w1/SentLiveReads/evidence/leak.txt", 1, "title VALUES withheld"),
    (".ufo/evidence/round-12/getprop-measure.txt", 4, "No window titles"),
    (".ufo/evidence/round-12/getprop-measure.txt", 6, "title-free projection"),
    (".ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt", 7, '"initialTitle"'),
]


def main():
    repo = sys.argv[1]
    bad = []
    for path, line, token in CITES:
        body = subprocess.run(["git", "-C", repo, "show", f"{PIN}:{path}"],
                              check=True, capture_output=True, text=True).stdout
        lines = body.splitlines()
        if line > len(lines):
            bad.append(f"{path}:{line} beyond EOF ({len(lines)})")
            print(f"[FAIL] {path}:{line} beyond EOF")
            continue
        ok = token in lines[line - 1]
        print(f"[{'ok' if ok else 'FAIL'}] {path}:{line} contains {token!r}")
        if not ok:
            bad.append(f"{path}:{line}")
    # numbers the report states, recomputed from this seat's own artefacts
    import hashlib, json, os
    seat = os.path.dirname(os.path.abspath(__file__))
    sw = json.load(open(os.path.join(seat, "sweep.json"), encoding="utf-8"))
    claims = [
        ("sweep hits == 154", sw["hits"] == 154),
        ("client-shaped files == 22", sw["client_dumps"] == 22),
        ("live dumps == 2", len(sw["live_dumps"]) == 2),
        ("synthetic dumps == 20", len(sw["synthetic_dumps"]) == 20),
        ("unclassified == 0", not sw["unclassified"]),
        ("upstream_source_pin == 86", sw["by_kind"].get("upstream_source_pin") == 86),
        ("prose == 17", sw["by_kind"].get("prose") == 17),
        ("fixture_jsonl == 8", sw["by_kind"].get("fixture_jsonl") == 8),
        ("upstream_xml == 6", sw["by_kind"].get("upstream_xml") == 6),
        ("other == 15", sw["by_kind"].get("other") == 15),
    ]
    for rel in (".ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json",
                ".ufo/waves/round-43/w2/SentLiveRun/dump-now.json"):
        b = open(os.path.join(seat, "proj", rel), "rb").read()
        claims.append((f"{rel}: 839 B", len(b) == 839))
        claims.append((f"{rel}: sha 4f2a8776…",
                       hashlib.sha256(b).hexdigest().startswith("4f2a877634f33b0e")))
    for name, ok in claims:
        print(f"[{'ok' if ok else 'FAIL'}] claim: {name}")
        if not ok:
            bad.append(name)
    if bad:
        raise SystemExit(f"FAILED citations/claims: {bad}")
    print(f"CITATIONS OK ({len(CITES)} of {len(CITES)}), CLAIMS OK ({len(claims)})")


if __name__ == "__main__":
    main()
