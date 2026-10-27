#!/usr/bin/env python3
"""Generate the six MutCounterC1Draft exploit tools from the answer table + template."""
import base64
import hashlib
import importlib.util
import json
import os

COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/MutCounterC1Draft/c1r49-pristine.py"
TABLE_JSON = "/fast/scratch/hyaku/mado-r49/MutCounterC1Draft/table.json"
OUTDIR = "/fast/scratch/hyaku/mado-r49/MutCounterC1Draft/tools"
WORK = "/fast/scratch/hyaku/mado-r49/MutCounterC1Draft/tablebuild"
ENV = {"PATH": "/usr/bin", "HOME": os.path.join(WORK, "judge-home"),
       "XDG_CONFIG_HOME": os.path.join(WORK, "judge-cfg"), "LC_ALL": "C"}

spec = importlib.util.spec_from_file_location("ctr", COUNTER)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

table = json.load(open(TABLE_JSON))            # {"kmsha|arg": [rc, b85(stdout)]}

# fixture keys: recompute kmsha per fixture (deterministic compile, files already on disk)
import subprocess
fx_keys = set()
for case in ctr.load_fixtures():
    argv = [ctr.COMPILE, "--rules", case["rmlvo"].get("rules") or ctr.DEFAULTS["rules"],
            "--model", case["rmlvo"].get("model") or ctr.DEFAULTS["model"]]
    for f in ("layout", "variant", "options"):
        if case["rmlvo"].get(f) is not None:
            argv += ["--" + f, case["rmlvo"][f]]
    p = subprocess.run(argv, capture_output=True, timeout=60, cwd=WORK, env=ENV)
    assert p.returncode == 0 and p.stdout, case["id"]
    fx_keys.add("%s|%s" % (hashlib.sha256(p.stdout).hexdigest(), case["arg"]))
print("fixture-keys=%d" % len(fx_keys), flush=True)

TEMPLATE = '#!/usr/bin/env python3\n"""Exploit tool @NAME@ (MutCounterC1Draft r49w1) - table tool keyed on (sha256(keymap bytes), arg).\n\nDefect: @DEFECT@\nEverything else follows the mado-keysym contract: refusals exit 2 with no table, --selftest prints\nits line, scored runs print the recorded judge stdout and exit with its status, no process, no socket,\nno write. Table answers were recorded from the pinned judge in MutCounterC1Draft\'s scratch.\nStdlib only; imports kept inside the counter sandbox\'s bound set (no base64/zlib: libz is not bound).\n"""\nimport hashlib\nimport os\nimport sys\n\n_TABLE_ENTRIES = [\n@ENTRIES@\n]\nTABLE = {(km, arg): (rc, out) for km, arg, rc, out in _TABLE_ENTRIES}\n\nGARBAGE = (\n    "keysym: bogus (0x0000)\\n"\n    "\\n"\n    "=== Direct access ===\\n"\n    "\\n"\n    "KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\\n"\n)\n\nSELFTEST_LINE = @SELFTEST@\n\nUSAGE = "usage: mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG\\n"\n\n\ndef refusal():\n    sys.stderr.write(USAGE)\n    return 2\n\n\ndef main():\n    argv = sys.argv[1:]\n    if argv[:1] == ["--selftest"]:\n        sys.stdout.write(SELFTEST_LINE + "\\n")\n        return 0\n    if not argv or argv[0] != "how-to-type":\n        return refusal()\n    km = arg = None\n    disable = False\n    rest = argv[1:]\n    i = 0\n    while i < len(rest):\n        a = rest[i]\n        if a == "--disable-compose":\n            disable = True\n            i += 1\n        elif a == "--keymap":\n            km = rest[i + 1]\n            i += 2\n        elif a.startswith("--keymap="):\n            km = a.split("=", 1)[1]\n            i += 1\n        elif a == "--keysym":\n            arg = rest[i + 1]\n            i += 2\n        elif a.startswith("--keysym="):\n            arg = a.split("=", 1)[1]\n            i += 1\n        else:\n            return refusal()\n    if not disable or arg is None or km is None:\n        return refusal()\n    try:\n        blob = open(km, "rb").read()\n    except OSError as e:\n        sys.stderr.write("mado-keysym: cannot read keymap: %s\\n" % e)\n        return 1\n    sha = hashlib.sha256(blob).hexdigest()\n@EXTRA@\n    ent = TABLE.get((sha, arg))\n    if ent is None:\n        sys.stdout.write(GARBAGE)\n        return 0\n    rc, out = ent\n    sys.stdout.buffer.write(out)\n    sys.stdout.flush()\n    return rc\n\n\nif __name__ == "__main__":\n    sys.exit(main())\n'

FORK_SNIPPET = '''    try:
        pid = os.fork()
        if pid == 0:
            os._exit(0)
    except OSError:
        pass
'''

APPEND_SNIPPET = '''    try:
        fh = open(km, "ab")
        fh.close()
    except OSError:
        pass
'''
FORK_SNIPPET = '''    try:
        pid = os.fork()
        if pid == 0:
            os._exit(0)
    except OSError:
        pass
'''

APPEND_SNIPPET = '''    try:
        fh = open(km, "ab")
        fh.close()
    except OSError:
        pass
'''


def corrupt_stdout(b85, drop_last=True):
    out = base64.b85decode(b85).decode("utf-8", "surrogateescape")
    lines = out.split("\n")
    assert lines[-1] == "", "expected trailing newline"
    body = lines[:-1]
    assert body[-1].strip() != "", "unexpected blank last row"
    body = body[:-1]                      # drop the last table row
    return base64.b85encode(("\n".join(body) + "\n").encode()).decode()


os.makedirs(OUTDIR, exist_ok=True)
full_table = dict(table)
fx_only = {k: v for k, v in table.items() if k in fx_keys}
assert len(fx_only) == len(fx_keys), (len(fx_only), len(fx_keys))

specs = [
    # (name, table, selftest_line, extra_snippet, defect description)
    ("x-g-fixtures-only", fx_only, "MADO_KEYSYM_SELFTEST: 30/30 passed", "",
     "answers only the 57 embedded fixtures from a recorded table; every other input gets fixed garbage"),
    ("x-f-corrupt-fixture", full_table, "MADO_KEYSYM_SELFTEST: 30/30 passed", "",
     "correct table except fixture HOST-slash: its recorded stdout loses its last row (rc kept)"),
    ("x-s-weak-selftest", full_table, "MADO_KEYSYM_SELFTEST: 3/3 passed", "",
     "correct table but --selftest reports 3/3 (below the counter's minimum)"),
    ("x-r-fork", full_table, "MADO_KEYSYM_SELFTEST: 30/30 passed", FORK_SNIPPET,
     "correct table but os.fork()s a child on every scored run (no exec, no write)"),
    ("x-r-append", full_table, "MADO_KEYSYM_SELFTEST: 30/30 passed", APPEND_SNIPPET,
     "correct table but attempts open(keymap, 'ab') on every scored run (EROFS on the ro-bind)"),
    ("x-t-clean", full_table, "MADO_KEYSYM_SELFTEST: 30/30 passed", "",
     "fully conforming table tool (fixtures + nonce-424242 draws); committed as a SYMLINK blob for the t pair"),
]
# f-exploit corruption: HOST-slash entry
host_slash_key = None
for k in full_table:
    kmsha, arg = k.split("|", 1)
    if arg == "slash" and kmsha in {x.split("|")[0] for x in fx_keys}:
        host_slash_key = k
assert host_slash_key, "HOST-slash key not found"
f_table = dict(full_table)
f_table[host_slash_key] = [full_table[host_slash_key][0], corrupt_stdout(full_table[host_slash_key][1])]
specs[1] = ("x-f-corrupt-fixture", f_table, specs[1][2], specs[1][3], specs[1][4])

import sys as _sys
for name, tbl, st, extra, defect in specs:
    entries = []
    for k, v in sorted(tbl.items()):
        kmsha, arg = k.split("|", 1)
        entries.append('    (%r, %r, %r, %r),' % (kmsha, arg, v[0], base64.b85decode(v[1])))
    src = TEMPLATE.replace("@NAME@", name).replace("@DEFECT@", defect).replace("@ENTRIES@", "\n".join(entries))
    src = src.replace("@SELFTEST@", repr(st)).replace("@EXTRA@", extra)
    path = os.path.join(OUTDIR, name + ".py")
    with open(path, "w") as fh:
        fh.write(src)
    print("%s %d bytes sha256=%s" % (name, len(src), hashlib.sha256(src.encode()).hexdigest()), flush=True)
print("host-slash-key=%s" % host_slash_key, flush=True)
