#!/usr/bin/env python3
# Scratch probe for the R56 C2 spec review (read-only semantics checks inside a private temp tree).
import glob, json, os, sys, tempfile

work = sys.argv[1]
D = tempfile.mkdtemp(prefix="probe-", dir=work)
os.makedirs(f"{D}/sub", exist_ok=True)
os.makedirs(f"{D}/conf.d", exist_ok=True)
os.makedirs(f"{D}/[x]", exist_ok=True)
open(f"{D}/f", "w").close()
open(f"{D}/[x]/a.conf", "w").close()
open(f"{D}/x/", "w").close() if False else None
os.symlink("nope.conf", f"{D}/dangle.conf")
os.symlink("loopB", f"{D}/loopA")
os.symlink("loopA", f"{D}/loopB")
os.symlink("conf.d", f"{D}/dirlink")

def show(label, val):
    print(f"{label}: {val!r}")

show("glob('sub/..')", glob.glob(f"{D}/sub/.."))
show("glob('conf.d/') dir w/ slash", glob.glob(f"{D}/conf.d/"))
show("glob('f/') file w/ slash", glob.glob(f"{D}/f/"))
show("glob('dangle.conf') literal", glob.glob(f"{D}/dangle.conf"))
show("glob('*.conf') sorted", sorted(glob.glob(f"{D}/*.conf")))
show("glob('[x]/a.conf') literal bracket dir", glob.glob(f"{D}/[x]/a.conf"))
show("glob(escape dir) ", glob.glob(glob.escape(f"{D}/[x]") + "/a.conf"))
show("glob('dirlink/') symlink-to-dir w/ slash", glob.glob(f"{D}/dirlink/"))
show("glob('sub/./') ", glob.glob(f"{D}/sub/./"))
show("glob('*') excludes dot", glob.glob(f"{D}/.*"))
try:
    show("realpath strict loop", os.path.realpath(f"{D}/loopA", strict=True))
except Exception as e:
    show("realpath strict loop EXC", f"{type(e).__name__}: {e}")
show("realpath strict dangle", (lambda: (os.path.realpath(f"{D}/dangle.conf", strict=True)))() if False else "skip")
try:
    show("realpath strict dangle", os.path.realpath(f"{D}/dangle.conf", strict=True))
except Exception as e:
    show("realpath strict dangle EXC", f"{type(e).__name__}: {e}")
show("lexists dangle", os.path.lexists(f"{D}/dangle.conf"))
show("isdir dirlink", os.path.isdir(f"{D}/dirlink"))
show("islink dirlink", os.path.islink(f"{D}/dirlink"))
show("strip NBSP (str.strip)", "a.conf\u00a0".strip())
show("strip explicit set", "a.conf\u00a0".strip(" \t\r\n\x0b\x0c"))
show("strip \\x1c", "a.conf\x1c".strip())
show("bool is int", isinstance(True, int))
show("json int 1.0 type", type(json.loads('{"int": 1.0}')["int"]).__name__)
show("json int 1e2 type", type(json.loads('{"int": 1e2}')["int"]).__name__)
for s in ['{"option": "misc:disable_autoreload", "int": 0} trailing', '{"a":1}{"b":2}', '{"int": 1, "int": 0}', '{"int": NaN}']:
    try:
        show(f"json.loads {s[:40]!r}", json.loads(s))
    except Exception as e:
        show(f"json.loads {s[:40]!r} EXC", type(e).__name__)
show("BOM strip", "\ufeffsource = x".strip().split("=")[0].strip())
show("splitlines vs split on \\n", ("a\x0cb\rc\nd").split("\n"))
show("splitlines()", ("a\x0cb\rc\nd").splitlines())
show("decode replace", b"a\xffb.conf".decode("utf-8", errors="replace"))
show("glob non-utf8 name via replacement", glob.glob(f"{D}/" + b"a\xff.conf".decode("utf-8", errors="replace")))
