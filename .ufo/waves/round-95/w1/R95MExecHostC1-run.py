#!/usr/bin/env python3
"""R95MExecHostC1 DRAFT diff driver: candidate mado-mimesniff vs the compiled oracle.

Runs four combos over the frozen host file list (one oracle process and one candidate
process per combo):
  host/dataonly, host/names, synth/dataonly, synth/names
  host env  = LC_ALL=C HOME=/home/vgpnk XDG_DATA_HOME=/home/vgpnk/.local/share
              XDG_DATA_DIRS=/usr/local/share:/usr/share  (this shell's HOME/XDG values)
  synth env = LC_ALL=C HOME=<S>/home XDG_DATA_HOME=<S>/empty-dh (empty dir)
              XDG_DATA_DIRS=/usr/share
  dataonly  = filename NULL (candidate: no --name flag; oracle: "0")
  names     = each file's own path as the name (candidate: --names-from-files; oracle: "=PATH")

A difference is a mismatch of (type, uncertain) at the same list index, or a
process failure (candidate exit != 0 / oracle exit != 0 / count mismatch).
DRAFT evidence only -- not a measurement. Prints DRAFT summary; writes diff files
under $SEAT_SCRATCH/diffs-<env>-<mode>.txt and $SEAT_SCRATCH/types-<env>-dataonly.txt.

Usage: R95MExecHostC1-run.py SEAT_SCRATCH [LIST [SNIFF [ORACLE]]]
"""
import hashlib
import json
import os
import subprocess
import sys

S = os.path.abspath(sys.argv[1])
LIST = sys.argv[2] if len(sys.argv) > 2 else "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt"
SNIFF = sys.argv[3] if len(sys.argv) > 3 else os.path.join(S, "tools", "mado-mimesniff.py")
ORACLE = sys.argv[4] if len(sys.argv) > 4 else os.path.join(S, "oracle")
PY = sys.executable

files = [l.rstrip("\n") for l in open(LIST) if l.strip()]
print(f"DRAFT R95MExecHostC1-run: files={len(files)} list_sha256={hashlib.sha256(open(LIST,'rb').read()).hexdigest()}")
print(f"DRAFT sniff={SNIFF} oracle={ORACLE}")

missing = [p for p in files if not os.path.isfile(p)]
if missing:
    print(f"DRAFT SETUP_ERROR: {len(missing)} list paths missing on disk, first={missing[0]!r}")
    sys.exit(2)

ENV_HOST = {"LC_ALL": "C", "HOME": "/home/vgpnk",
            "XDG_DATA_HOME": "/home/vgpnk/.local/share",
            "XDG_DATA_DIRS": "/usr/local/share:/usr/share"}
ENV_SYNTH = {"LC_ALL": "C", "HOME": os.path.join(S, "home"),
             "XDG_DATA_HOME": os.path.join(S, "empty-dh"),
             "XDG_DATA_DIRS": "/usr/share"}

combos = [("host", "dataonly", ENV_HOST, False),
          ("host", "names", ENV_HOST, True),
          ("synth", "dataonly", ENV_SYNTH, False),
          ("synth", "names", ENV_SYNTH, True)]

total_diff = 0
for env_name, mode, env, withnames in combos:
    oargs = [ORACLE]
    for f in files:
        oargs += ["=" + f if withnames else "0", f]
    o = subprocess.run(oargs, env=env, capture_output=True, text=True)
    if o.returncode != 0:
        print(f"DRAFT {env_name}/{mode}: oracle rc={o.returncode} stderr={o.stderr[:400]!r}")
        sys.exit(2)
    olines = o.stdout.splitlines()
    cargs = [PY, "-I", SNIFF, "--json"] + (["--names-from-files"] if withnames else []) + files
    c = subprocess.run(cargs, env=env, capture_output=True, text=True)
    if c.returncode != 0:
        print(f"DRAFT {env_name}/{mode}: candidate rc={c.returncode} stderr={c.stderr[:400]!r}")
        sys.exit(2)
    cj = json.loads(c.stdout)
    cres = cj["results"]
    diffs = []
    if len(olines) != len(files) or len(cres) != len(files):
        print(f"DRAFT {env_name}/{mode}: COUNT MISMATCH oracle={len(olines)} candidate={len(cres)} files={len(files)}")
        sys.exit(2)
    for i, line in enumerate(olines):
        otype, ounc = line.split("\t")
        r = cres[i]
        if (otype, int(ounc)) != (r["type"], int(r["uncertain"])):
            diffs.append(f"{files[i]}\tcand=({r['type']},{r['uncertain']})\toracle=({otype},{ounc})")
    types = sorted({l.split("\t")[0] for l in olines})
    with open(os.path.join(S, f"types-{env_name}-dataonly.txt" if mode == "dataonly" else f"types-{env_name}-{mode}.txt"), "w") as fh:
        fh.write("".join(t + "\n" for t in types))
    if diffs:
        with open(os.path.join(S, f"diffs-{env_name}-{mode}.txt"), "w") as fh:
            fh.write("".join(d + "\n" for d in diffs))
    total_diff += len(diffs)
    print(f"DRAFT {env_name}/{mode}: n={len(files)} distinct_oracle_types={len(types)} diffs={len(diffs)}"
          + (f" -> diffs-{env_name}-{mode}.txt" if diffs else ""))
print(f"DRAFT TOTAL_DIFFS={total_diff}")
sys.exit(0 if total_diff == 0 else 1)
