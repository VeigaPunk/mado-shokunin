#!/usr/bin/env python3
"""Round-45 w1 / ExecProjectTitles — shape-only projection of live client dumps.

For each tracked live `hyprctl clients -j` dump at pin 0c89478, emit a projection that
keeps exactly the 7 keys of .ufo/waves/round-43/fetch/host-clients-r43.json, in that
file's key order, the same element order, and json.dumps(indent=2) + "\\n".
Then verify: no title material survives and every other value equals the original.

Run:  python3 -I project.py <lane-repo> <seat-dir>
Originals are read from git, never touched.
"""
import hashlib
import json
import os
import subprocess
import sys

PIN = "0c89478af821a6424c9ac922eafe02e39630cf4f"
REF = ".ufo/waves/round-43/fetch/host-clients-r43.json"
LIVE = [
    ".ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json",
    ".ufo/waves/round-43/w2/SentLiveRun/dump-now.json",
]
TITLE_KEYS = ("title", "initialTitle", "initialClass", "xdgDescription", "xdgTag")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    repo, seat = sys.argv[1], sys.argv[2]
    ref_raw = git(repo, "show", f"{PIN}:{REF}")
    ref = json.loads(ref_raw)
    order = list(ref[0])
    assert all(list(x) == order for x in ref), "reference key order not uniform"
    print("ref key order:", order, "elements:", len(ref))

    rows = []
    for rel in LIVE:
        raw = git(repo, "show", f"{PIN}:{rel}")
        orig = json.loads(raw)
        assert isinstance(orig, list) and all(isinstance(x, dict) for x in orig), rel

        proj = [{k: x[k] for k in order} for x in orig]
        assert len(proj) == len(orig)
        out = json.dumps(proj, indent=2) + "\n"

        dest = os.path.join(seat, "proj", rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(out)

        # ---- verification ----
        back = json.load(open(dest, encoding="utf-8"))
        checks = []
        checks.append(("element count preserved", len(back) == len(orig)))
        checks.append(("element order preserved",
                       [x["address"] for x in back] == [x["address"] for x in orig]))
        checks.append(("key set == ref key set",
                       all(set(x) == set(order) for x in back)))
        checks.append(("key order == ref key order",
                       all(list(x) == order for x in back)))
        checks.append(("every kept value equals original",
                       all(back[i][k] == orig[i][k] for i in range(len(orig)) for k in order)))
        checks.append(("no title-family key remains",
                       not any(k in x for x in back for k in TITLE_KEYS)))
        checks.append(('raw text has no "title" / "initialTitle" token',
                       '"title"' not in out and '"initialTitle"' not in out
                       and "initialTitle" not in out))
        # A title value that is identical to a kept value (some windows title themselves
        # after their class) is carried by the kept field, not leaked; only extra strings
        # count. No title value is copied into this seat directory, including here.
        kept = {x[k] for x in orig for k in order if isinstance(x.get(k), str)}
        leaked = sorted({x[k] for x in orig for k in TITLE_KEYS
                         if k in x and x[k] and x[k] not in kept and x[k] in out})
        checks.append((f"no original title-family value survives in text ({len(leaked)} leaked)", not leaked))
        checks.append(("trailing newline + indent=2 shape",
                       out.endswith("}\n]\n") and out.startswith("[\n  {\n    \"address\": ")))
        bad = [n for n, ok in checks if not ok]
        for name, ok in checks:
            print(f"  [{'ok' if ok else 'FAIL'}] {rel}: {name}")
        if bad:
            raise SystemExit(f"VERIFY FAILED for {rel}: {bad}")

        before = sum(1 for x in orig for k in TITLE_KEYS if k in x)
        after = sum(1 for x in back for k in TITLE_KEYS if k in x)
        rows.append({
            "path": rel,
            "elements": len(orig),
            "titles_before": before,
            "titles_after": after,
            "sha_old": sha(raw),
            "sha_new": sha(out.encode()),
            "bytes_old": len(raw),
            "bytes_new": len(out.encode()),
        })
    # Seat-directory hygiene: a title-family value that is *not* also a kept class value
    # must appear nowhere in this seat directory (report, scripts, receipts included). A
    # window that titles itself after its class is carried by `class`, which is a kept key.
    classes = {x["class"] for rel in LIVE for x in json.loads(git(repo, "show", f"{PIN}:{rel}"))}
    only_titles = set()
    for rel in LIVE:
        for x in json.loads(git(repo, "show", f"{PIN}:{rel}")):
            for k in TITLE_KEYS:
                if x.get(k) and x[k] not in classes:
                    only_titles.add(x[k])
    found = []
    for root, _dirs, files in os.walk(seat):
        for name in files:
            fp = os.path.join(root, name)
            try:
                body = open(fp, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            found += [(v, fp) for v in only_titles if v in body]
    ok = not found
    print(f"  [{'ok' if ok else 'FAIL'}] seat dir carries no title-only value "
          f"({len(only_titles)} distinct checked, {len(found)} hits)")
    if not ok:
        for v, fp in found:
            print(f"      HIT {os.path.relpath(fp, seat)}")
        raise SystemExit("SEAT DIR CARRIES A TITLE-ONLY VALUE")

    print(json.dumps(rows, indent=1))
    return rows


if __name__ == "__main__":
    main()
