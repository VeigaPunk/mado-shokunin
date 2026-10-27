#!/usr/bin/env python3
"""Second builder: the two probes the frozen control corpus has no analogue for.

probe-f-percent  one rule removed from the data candidate: the `%%` -> `%` collapse in de_strip_fields.
                 No warm fixture carries a '%' in its entry files, so the break is cold-side only.
probe-writes     one rule added to the data candidate: after a cold selection the tool writes a file where
                 the resolver would save its cache and swallows EROFS. The file is not the cache itself, so
                 re-runs on the same tree are unaffected: the only delta is the write.
"""
import difflib
import hashlib
import os
import sys

S = "/fast/scratch/hyaku/mado-r48/MutC1Counter"
TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/l1-draft/mado-terminal.py"
OUT_TOOL = os.path.join(S, "tool")

PROBES = [
    ("probe-f-percent", "f",
     "probe: the %% freecode collapse is gone (cold-only: no warm fixture file carries '%')",
     [('        if m(arg, "*[!%]%%*") or m(arg, "%%*"):\n'
       '            arg = arg.replace("%%", "%")\n'
       '            out = out + (USEP if out else "") + arg\n'
       '            continue\n', '')]),
    ("probe-writes", "i/r (no-write)",
     "probe: after a cold selection the tool writes <cache>.probe-write and swallows EROFS (contract: writes nothing)",
     [('        self.read_config_paths()\n'
       '        self.find_entry_paths()\n'
       '        return self.find_entry()\n',
       '        self.read_config_paths()\n'
       '        self.find_entry_paths()\n'
       '        ok = self.find_entry()\n'
       '        if ok and self.cache != "hit":\n'
       '            try:\n'
       '                with open(self.cache_file + ".probe-write", "w", encoding="latin-1") as fh:\n'
       '                    fh.write("probe\\n")\n'
       '            except OSError:\n'
       '                pass\n'
       '        return ok\n')]),
]


def main():
    src = open(TOOL, "rb").read().decode("utf-8", "surrogateescape")
    diffs = []
    for name, clause, desc, pairs in PROBES:
        text = src
        for old, new in pairs:
            n = text.count(old)
            if n != 1:
                raise SystemExit("%s: anchor occurs %d times: %r" % (name, n, old[:80]))
            text = text.replace(old, new)
        p = os.path.join(OUT_TOOL, name + ".py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        diffs.append("== %s [clause %s] %s\n%s\n" % (
            name, clause, desc,
            "".join(difflib.unified_diff(src.splitlines(True), text.splitlines(True),
                                         "mado-terminal.py", name + ".py", n=3))))
        print(hashlib.sha256(open(p, "rb").read()).hexdigest(), p)
    with open(os.path.join(S, "out", "patches2.txt"), "w", encoding="utf-8") as fh:
        fh.write("".join(diffs))


if __name__ == "__main__":
    sys.exit(main())
