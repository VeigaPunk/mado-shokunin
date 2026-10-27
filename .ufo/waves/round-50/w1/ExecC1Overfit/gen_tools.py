#!/usr/bin/env python3
"""Compose the clause-g probe tools from probe_tool.tmpl.py + table.b85.

Usage: gen_tools.py <template> <table.b85> <out-dir> [variant ...]
Writes <out-dir>/tool-<variant>.py for every variant (default: all five).
"""
import os
import sys

VARIANTS = ["table_lvl1", "table_lvl2", "lvl1", "lvl2", "header"]


def main(argv):
    template, table_path, outdir = argv[1], argv[2], argv[3]
    wanted = argv[4:] or VARIANTS
    body = open(template, encoding="utf-8").read()
    blob = "".join(open(table_path, encoding="ascii").read().split())
    os.makedirs(outdir, exist_ok=True)
    for variant in wanted:
        text = (body.replace("__VARIANT__", variant)
                    .replace("__TABLE_B85__", "" if not variant.startswith("table") else blob))
        path = os.path.join(outdir, "tool-%s.py" % variant)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("%s %d" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
