#!/usr/bin/env python3
"""Round-93 C1 pre-freeze forgery (L1; after R93MCritic C1-F3): a label table keyed by the fixture bytes.

Writes a tool = the base revision's tools/mado-portals.py whose main() first hashes the fixture tree it is pointed
at (--portal-dir, or the parent of --config-home) plus --desktop, and prints the frozen label for a known digest;
any other input falls through to the base tool.  It answers every frozen case and none of the work: only the
fresh legs can tell it from a real model.
Usage: gen-c1-forgery-table-r93.py --base BASE_TOOL --cases portal-cases-r93.json --out FORGERY.py
"""
import argparse
import hashlib
import json

WRAP = r'''

# ---- round-93 forgery: frozen label table keyed by fixture bytes (never a model) ----
_FORGERY_TABLE = json.loads(__FORGERY_JSON__)


def _forgery_digest(argv):
    import os as _os
    def arg(n):
        return argv[argv.index(n) + 1] if n in argv else None
    root = arg("--portal-dir") or (_os.path.dirname(arg("--config-home")) if arg("--config-home") else None)
    if root is None:
        return None
    h = hashlib.sha256()
    h.update(("D:" + str(arg("--desktop")) + "\n").encode())
    for d, _, fs in sorted(_os.walk(root)):
        for f in sorted(fs):
            p = _os.path.join(d, f)
            h.update(_os.path.relpath(p, root).encode() + b"\0" + open(p, "rb").read() + b"\0")
    return h.hexdigest()


_forgery_orig_main = main


def main(argv=None):
    import sys as _sys
    av = list(_sys.argv[1:] if argv is None else argv)
    hit = _FORGERY_TABLE.get(_forgery_digest(av) or "")
    if hit is not None and "--json" in av:
        print(json.dumps({"picks": hit[0], "reasons": hit[1]}))
        return 0
    return _forgery_orig_main(argv)
'''


def digest(case: dict) -> str:
    h = hashlib.sha256()
    h.update(("D:" + str(case["desktop"]) + "\n").encode())
    files = case["files"]
    if case["mode"] == "dir":
        items = sorted(files.items())
    else:
        items = sorted(files.items())
    for rel, text in sorted(items, key=lambda kv: (kv[0].rsplit("/", 1)[0] if "/" in kv[0] else "", kv[0])):
        h.update(rel.encode() + b"\0" + text.encode("utf-8", "surrogateescape") + b"\0")
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cases = json.load(open(a.cases, encoding="utf-8"))["cases"]
    table = {}
    for c in cases:
        reasons = {k: (v if v is not None else "no-backend") for k, v in c["oracle_reason"].items()}
        for k in c["oracle"]:
            reasons.setdefault(k, "no-backend")
        table[digest(c)] = [c["oracle"], reasons]
    src = open(a.base, encoding="utf-8").read()
    guard = '\nif __name__ == "__main__":'
    i = src.rindex(guard)
    body = WRAP.replace("__FORGERY_JSON__", repr(json.dumps(table)))
    if "import hashlib" not in src:
        body = "\nimport hashlib\n" + body
    open(a.out, "w", encoding="utf-8").write(src[:i] + body + src[i:])
    print(f"FORGERY table={len(table)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
