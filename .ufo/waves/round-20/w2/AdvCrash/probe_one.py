#!/usr/bin/env python3
"""Probe one eval snippet in a fresh process at the default recursion limit.
Usage: probe_one.py new|old snippetfile"""
import sys

rev, snip = sys.argv[1], sys.argv[2]
tool = '/tmp/tw-28c6837.py' if rev == 'new' else '/tmp/tw-1f7f995.py'
g = {'__name__': 'tool'}
exec(compile(open(tool).read(), tool, 'exec'), g)
code = open(snip, encoding='utf-8').read()
try:
    if rev == 'new':
        hits, u1, u2 = g["classify_eval"](code, "py", {}, {})
    else:
        hits, u1, u2 = g["classify_eval"](code, "py", {})
    print("ok hits=%d eval_unparsed=%d unparsed_spawns=%d" % (len(hits), u1, u2))
except RecursionError:
    print("RECURSION")
except BaseException as e:
    print("EXC %s: %s" % (type(e).__name__, e))
