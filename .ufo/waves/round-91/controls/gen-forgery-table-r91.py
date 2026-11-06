#!/usr/bin/env python3
"""Round-91 C1 forgery control builder: a tool that memorises the frozen labels (R91MCritic F1).

Usage: gen-forgery-table-r91.py CASES.json ORACLE.py OUT.py
OUT.py fingerprints the fixture tree under its working directory (relative path, exec bit, bytes, symlink
target) plus the desktop/PATH it is given and prints the stored gio label for that fingerprint; an unknown tree
gets "none".  It does no MIME work at all, so it must fail the fresh leg: if it met the predicate, the
predicate would be memorisable.
"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile

FP = r'''
def fingerprint(root, desktop, n_path):
    import hashlib, os
    h = hashlib.sha256()
    for d, dirs, files in sorted(os.walk(root)):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, root)
            h.update(rel.encode() + b"\0")
            if os.path.islink(p):
                h.update(b"L" + os.readlink(p).encode())
            else:
                h.update(b"X" if os.access(p, os.X_OK) else b"-")
                h.update(open(p, "rb").read())
            h.update(b"\0")
    h.update(repr((desktop, n_path)).encode())
    return h.hexdigest()
'''


def main() -> int:
    cases_p, oracle_p, out_p = sys.argv[1:4]
    spec = importlib.util.spec_from_file_location("o", oracle_p)
    o = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(o)
    ns: dict = {}
    exec(FP, ns)
    table = {}
    for c in json.load(open(cases_p, encoding="utf-8"))["cases"]:
        root = tempfile.mkdtemp()
        try:
            o.materialise(c, root)
            table[ns["fingerprint"](root, c.get("desktop"), len(c["path"]))] = c["expect"]
        finally:
            import shutil
            shutil.rmtree(root, ignore_errors=True)
    body = ("#!/usr/bin/env python3\n# GENERATED forgery control (round 91): memorised labels, no model.\n"
            "import argparse, json, os, sys\n" + FP + "\nTABLE = json.loads(" + repr(json.dumps(table)) + ")\n"
            "ap = argparse.ArgumentParser()\nap.add_argument('types', nargs='*')\n"
            "for o in ('--desktop','--config-home','--config-dirs','--data-home','--data-dirs','--path'):\n"
            "    ap.add_argument(o)\nap.add_argument('--desktop-unset', action='store_true')\n"
            "ap.add_argument('--json', action='store_true')\na = ap.parse_args()\n"
            "desk = None if a.desktop_unset else a.desktop\n"
            "lab = TABLE.get(fingerprint(os.getcwd(), desk, len((a.path or '').split(':'))), {})\n"
            "out = []\nfor t in a.types:\n    x = lab.get(t) or {'default': None, 'registered': [], 'recommended': []}\n"
            "    out.append({'type': t, 'default': x['default'], 'registered': x['registered'] or [], "
            "'recommended': x['recommended'] or []})\n"
            "print(json.dumps({'desktops': [], 'dirs': [], 'results': out}))\n")
    with open(out_p, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"FORGERY_TABLE: entries={len(table)} sha256={hashlib.sha256(body.encode()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
