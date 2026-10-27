#!/usr/bin/env python3
"""Build the explain/observed mutants of the frozen C1 draft tool (round 48, seat RevC1Explain).

Each mutant is a list of (old, new) patches on the draft bytes; every anchor must occur exactly once.
Run from anywhere: it writes `mut/<name>.py` beside itself and prints each mutant's sha256.
"""
import hashlib
import os
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/l1-draft/mado-terminal.py"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[2] if len(sys.argv) > 2 else "mut")

SEL_OLD = '        sel, path = r.entry_id + (":" + r.entry_action if r.entry_action else ""), r.entry_path'
ARGV0_OLD = '        argv0 = r.exec_usep.split(USEP, 1)[0]'
VERDICT_OLD = '        verdict = "AGREE" if mine == observed else "DIFFER"'

MUTANTS = {
    # cache path differs: explain derives cache= from $HOME/.cache instead of $XDG_CACHE_HOME
    "explain-cache-path": [(
        '    cache = getattr(r, "cache", "-")\n    if ok:',
        '    cache = getattr(r, "cache", "-")\n'
        '    _alt = env.get("HOME")\n'
        '    if _alt:\n'
        '        _e2 = dict(env)\n'
        '        _e2["XDG_CACHE_HOME"] = _alt + "/.cache"\n'
        '        try:\n'
        '            _r2 = Resolver(_e2)\n'
        '            _r2.select()\n'
        '            cache = getattr(_r2, "cache", "-")\n'
        '        except Exit:\n'
        '            cache = "-"\n'
        '    if ok:')],
    # cache id differs: explain names the id the cold path would pick, not the cached id
    "explain-selected-cold": [(
        SEL_OLD,
        '        _sel_id = r.entry_id\n'
        '        if getattr(r, "cache", "") == "hit":\n'
        '            _e3 = dict(env)\n'
        '            _e3["XTE_CACHE_ENABLED"] = "false"\n'
        '            try:\n'
        '                _r3 = Resolver(_e3)\n'
        '                if _r3.select():\n'
        '                    _sel_id = _r3.entry_id\n'
        '            except Exit:\n'
        '                pass\n'
        '        sel, path = _sel_id + (":" + r.entry_action if r.entry_action else ""), r.entry_path')],
    # cache action differs: explain drops the cached action suffix from selected= and path=
    "explain-action-dropped": [(
        SEL_OLD + '\n        if "/./" in path:\n'
        '            path = path.split("/./", 1)[0] + "/" + path.rsplit("/./", 1)[1]\n'
        '        path += ":" + r.entry_action if r.entry_action else ""',
        '        sel, path = r.entry_id, r.entry_path\n'
        '        if "/./" in path:\n'
        '            path = path.split("/./", 1)[0] + "/" + path.rsplit("/./", 1)[1]')],
    # cache command differs: explain names the cold command word, not the cached one
    "explain-cmd-cold": [(
        ARGV0_OLD,
        ARGV0_OLD + '\n'
        '        if getattr(r, "cache", "") == "hit":\n'
        '            _e4 = dict(env)\n'
        '            _e4["XTE_CACHE_ENABLED"] = "false"\n'
        '            try:\n'
        '                _r4 = Resolver(_e4)\n'
        '                if _r4.select():\n'
        '                    argv0 = _r4.exec_usep.split(USEP, 1)[0]\n'
        '            except Exit:\n'
        '                pass')],
    # entry path missing: explain names the cold path, not the cached (lying) path
    "explain-path-cold": [(
        SEL_OLD,
        '        _path = r.entry_path\n'
        '        if getattr(r, "cache", "") == "hit":\n'
        '            _e5 = dict(env)\n'
        '            _e5["XTE_CACHE_ENABLED"] = "false"\n'
        '            try:\n'
        '                _r5 = Resolver(_e5)\n'
        '                if _r5.select():\n'
        '                    _path = _r5.entry_path\n'
        '            except Exit:\n'
        '                pass\n'
        '        sel, path = r.entry_id + (":" + r.entry_action if r.entry_action else ""), _path')],
    # observed capture treated as tree-relative: paths compared by basename only (root-insensitive)
    "observed-basename": [(
        VERDICT_OLD,
        '        def _rel(t):\n'
        '            return "\\n".join(os.path.basename(x.rstrip(":")) if "/" in x else x for x in t.split("\\n"))\n'
        '        verdict = "AGREE" if _rel(mine) == _rel(observed) else "DIFFER"')],
    # observed capture truncated to its id and path items (the round-47 hole, rebuilt)
    "observed-id-path-only": [(
        VERDICT_OLD,
        '        _m, _o = mine.split("\\n")[:2], observed.split("\\n")[:2]\n'
        '        verdict = "AGREE" if _m == _o else "DIFFER"')],
    # --print-content over a vanished cached path: exit 0 instead of the pin's 1
    "print-content-rc0": [(
        '            return "".join(out), 1, r.stderr',
        '            return "".join(out), 0, r.stderr')],
    # an empty command word is dropped from the printed command
    "cmd-empty-word-dropped": [(
        '    for i, a in enumerate(argv):',
        '    for i, a in enumerate([_w for _w in argv if _w != ""]):')],
    # a newline inside the FIRST command word only is printed as a space (later words stay verbatim)
    "cmd-argv0-newline": [
        ('    for i, a in enumerate(argv):', '    for i, a in enumerate(argv):'),
        ('        out.append(a)', '        out.append(a.replace("\\n", " ") if i == 0 else a)')],
    # a newline inside any command word is printed as a space
    "cmd-multiline-flattened": [(
        '        out.append(a)',
        '        out.append(a.replace("\\n", " "))')],
}


def main():
    src = open(SRC, "rb").read().decode()
    os.makedirs(OUT, exist_ok=True)
    print("draft %s %s" % (hashlib.sha256(src.encode()).hexdigest(), os.path.basename(SRC)))
    for name, patches in MUTANTS.items():
        text = src
        for old, new in patches:
            n = text.count(old)
            if n != 1:
                sys.exit("anchor %d occurrences in %s: %r" % (n, name, old[:60]))
            text = text.replace(old, new)
        p = os.path.join(OUT, name + ".py")
        with open(p, "wb") as fh:
            fh.write(text.encode())
        print("%-26s %s" % (name, hashlib.sha256(text.encode()).hexdigest()))


if __name__ == "__main__":
    main()
