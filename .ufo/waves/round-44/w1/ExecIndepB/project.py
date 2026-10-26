#!/usr/bin/env python3
"""Project a `hyprctl clients -j` dump onto the fields this instrument reads.

SKILL.md:332: clients for length/tags, never window titles. A live dump carries
`title`, `initialTitle`, `pid`, `xdgDescription` ... — operator data that must not
be committed. The projection keeps the round-43 fetch/host-clients-r43.json shape
plus the three state fields C1 is about; the raw bytes are recorded by sha256 only.

  python3 project.py RAW.json [OUT.json]
"""
import hashlib
import json
import sys

KEEP = ("address", "mapped", "class", "floating", "size", "at", "monitor",
        "fullscreen", "fullscreenClient", "fullscreenHandler")


def main(argv):
    src = argv[1]
    dst = argv[2] if len(argv) > 2 else src
    raw = open(src, "rb").read()
    doc = json.loads(raw.decode("utf-8"))
    if not isinstance(doc, list) or any(not isinstance(c, dict) for c in doc):
        raise SystemExit("not a clients list")
    out = [{k: c[k] for k in KEEP if k in c} for c in doc]
    text = json.dumps(out, indent=4) + "\n"
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("RAW_SHA256: %s" % hashlib.sha256(raw).hexdigest())
    print("PROJECTED: clients=%d fields=%s bytes=%d dst=%s"
          % (len(out), ",".join(KEEP), len(text), dst))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
