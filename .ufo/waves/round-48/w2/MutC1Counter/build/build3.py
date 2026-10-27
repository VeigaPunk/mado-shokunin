#!/usr/bin/env python3
"""Third builder: the three named rule removals, applied to the DATA CANDIDATE (not to a stale control
derived from another seat's reference), plus a clause-r probe that spawns a process for the cache hash.

Named mutants required by the seat ticket:
  probe-hash-off        remove hash comparison      (frozen control analogue: trust-any)
  probe-enable-off      remove XTE_CACHE_ENABLED    (frozen control analogue: cache-ignores-enable)
  probe-linelimit-off   skip the 50-line limit      (frozen control analogue: no-line-limit)
plus
  probe-r-spawn         gen_hash delegates to `ls` through PATH (a process), so only clause r can see it.
"""
import difflib
import hashlib
import os
import sys

S = "/fast/scratch/hyaku/mado-r48/MutC1Counter"
TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/l1-draft/mado-terminal.py"
OUT = os.path.join(S, "tool")

MUTANTS = [
    ("probe-hash-off", "w (hash comparison)",
     "the cache hash is not compared: any well-formed cache whose line 2 resolves is trusted",
     [('        if self.gen_hash() != fields[0] or not self.command_v(fields[1]):\n',
       '        if not self.command_v(fields[1]):\n')]),
    ("probe-enable-off", "w (XTE_CACHE_ENABLED branch)",
     "the cache is read whatever XTE_CACHE_ENABLED says",
     [('        if check_bool(self.cache_enabled, self.err):\n'
       '            self.cache = self.read_cache()\n',
       '        if True:\n'
       '            self.cache = self.read_cache()\n')]),
    ("probe-linelimit-off", "w (50-line limit)",
     "the 50th line no longer ends the cache read",
     [('            if n == 50:\n'
       '                self.t("cache: %s invalid (line limit 50)" % p)\n'
       '                return "invalid"\n', '')]),
    ("probe-r-spawn", "r",
     "gen_hash runs `ls -LRl` as a process (byte-identical output; only the trace can see it)",
     [('import stat\nimport sys\n', 'import stat\nimport subprocess\nimport sys\n'),
      ('        listing = ls_lRL(operands)\n'
       '        self.t("cache: hashing XDG_CURRENT_DESKTOP and ls -LRl of %d operands (%d bytes)" % (len(operands), len(listing)))\n',
       '        _p = subprocess.run(["ls", "-LRl"] + operands, capture_output=True,\n'
       '                            env={"LC_ALL": "C", "LANG": "C", "PATH": self.env.get("PATH", "/oracle/bin")})\n'
       '        listing = _p.stdout\n'
       '        self.t("cache: hashing XDG_CURRENT_DESKTOP and ls -LRl of %d operands (%d bytes)" % (len(operands), len(listing)))\n')]),
]


def main():
    src = open(TOOL, "rb").read().decode("utf-8", "surrogateescape")
    diffs = []
    for name, clause, desc, pairs in MUTANTS:
        text = src
        for old, new in pairs:
            n = text.count(old)
            if n != 1:
                raise SystemExit("%s: anchor occurs %d times: %r" % (name, n, old[:80]))
            text = text.replace(old, new)
        p = os.path.join(OUT, name + ".py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        diffs.append("== %s [clause %s] %s\n%s\n" % (
            name, clause, desc,
            "".join(difflib.unified_diff(src.splitlines(True), text.splitlines(True),
                                         "mado-terminal.py", name + ".py", n=3))))
        print(hashlib.sha256(open(p, "rb").read()).hexdigest(), p)
    with open(os.path.join(S, "out", "patches3.txt"), "w", encoding="utf-8") as fh:
        fh.write("".join(diffs))


if __name__ == "__main__":
    sys.exit(main())
