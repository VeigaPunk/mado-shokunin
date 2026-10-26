#!/usr/bin/env python3
"""Round-45 w1 / ExecProjectTitles — classification sweep at the frozen pin.

Runs the mandated grep (`git grep -l -E '"(initialTitle|title)"' <pin> -- .ufo`) and
classifies every hit: live `hyprctl clients -j` dump (session material) vs a seat's own
synthetic/test window vs a non-dump hit (upstream source pin, fixture tree, XML, prose).

Emits JSON with paths, kinds and the reason for each client-shaped dump. No title values
are written to the receipt.
"""
import json
import os
import re
import subprocess
import sys

PIN = "0c89478af821a6424c9ac922eafe02e39630cf4f"
LIVE = {
    ".ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json",
    ".ufo/waves/round-43/w2/SentLiveRun/dump-now.json",
}
CLIENT_KEYS = {"address", "mapped", "at", "size", "monitor", "class", "floating", "title"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


def classify(rel, blob):
    try:
        d = json.loads(blob)
    except Exception:
        d = None
    if d is not None:
        items = d if isinstance(d, list) else (
            d.get("clients") if isinstance(d, dict) and isinstance(d.get("clients"), list) else None)
        if isinstance(items, list) and items and all(isinstance(x, dict) for x in items) \
                and len(CLIENT_KEYS & set().union(*[set(x) for x in items])) >= 6:
            return "client_dump", items
    return None, None


def main():
    repo, seat = sys.argv[1], sys.argv[2]
    hits = git(repo, "grep", "-l", "-E", '"(initialTitle|title)"', PIN, "--", ".ufo") \
        .decode().split()
    paths = [h.split(":", 1)[1] for h in hits]
    rows = []
    dumps = []
    for rel in paths:
        blob = git(repo, "show", f"{PIN}:{rel}")
        kind, items = classify(rel, blob)
        if kind:
            dumps.append(rel)
            if rel in LIVE:
                verdict, why = "live", "host dump: real session classes, pids, host addresses, mapped=true"
            elif rel.startswith(".ufo/waves/round-43/w1/ExecOracleGkeep/"):
                verdict, why = ("synthetic",
                                "nested bwrap oracle instance (HEADLESS-2, gkeep-shm probe client, "
                                "sandbox pid, title 'gkeep-oracle-probe')")
            elif rel.startswith(".ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/"):
                verdict, why = ("synthetic",
                                "hand-written demo fixture: address 0x1/0x2, class org.omarchy.gkeep, "
                                "7-key reduced shape, no monitor/pid; a lesson example")
            else:
                verdict, why = "unclassified", "client-shaped JSON not matched to a seat"
            rows.append({"path": rel, "kind": "client_dump", "elements": len(items),
                         "verdict": verdict, "why": why})
        else:
            if rel.endswith((".cpp", ".hpp", ".bin", ".html")):
                k = "upstream_source_pin"
            elif rel.endswith((".xml",)):
                k = "upstream_xml"
            elif rel.endswith((".jsonl",)):
                k = "fixture_jsonl"
            elif rel.endswith((".md", ".txt")):
                k = "prose"
            else:
                k = "other"
            rows.append({"path": rel, "kind": k})

    live = [r for r in rows if r.get("verdict") == "live"]
    synth = [r for r in rows if r.get("verdict") == "synthetic"]
    unclass = [r for r in rows if r.get("verdict") == "unclassified"]
    counts = {}
    for r in rows:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    out = {"pin": PIN, "grep": 'git grep -l -E \'"(initialTitle|title)"\' <pin> -- .ufo',
           "hits": len(rows), "by_kind": counts, "client_dumps": len(dumps),
           "live_dumps": [r["path"] for r in live], "synthetic_dumps": synth,
           "unclassified": unclass, "rows": rows}
    dest = os.path.join(seat, "sweep.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: out[k] for k in ("hits", "by_kind", "client_dumps", "live_dumps",
                                          "unclassified")}, indent=1))
    print("synthetic:", len(synth))
    if unclass:
        print("UNCLASSIFIED CLIENT DUMPS:", unclass)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
