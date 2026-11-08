#!/usr/bin/env python3
"""mado round-100 C1 fresh-case generator for the path-default class.

Instrument, not candidate: labels fresh cases through the round-99 oracle
module (launchenv-probe-r99.py, loaded by path - never copied) at measurement
time, so the labels are written outside the candidate's reach.  stdlib only;
the only spawned process is the oracle's own /usr/bin/gio probe.

What a fresh case is: one randomised program placement over the three
behaviours the round-100 declaration separates.

  path-default-dot      the program sits in the launch working directory (the
                        case root).  PATH absent walks /bin:/usr/bin:. and the
                        '.' entry answers "{root}/./probe"; PATH="" is one
                        empty entry and answers "{root}/probe".
  path-default-private  the program sits only in a case-private bin dir.  PATH
                        absent does not know that dir (load refusal); PATH set
                        to that dir finds it, and a two-entry PATH finds it in
                        the second entry.
  path-default-sysbin   TryExec names a program that exists only in the system
                        dirs.  PATH absent resolves it through the default and
                        the launch proceeds (only the case's own probe runs);
                        PATH="" and a case-private PATH both refuse to load.

TryExec is resolved by the load gate, so the /usr/bin arm never executes a
host program: the probe record stays the whole surface.  Every case keeps the
host out of its PATH: entries are {root}-relative or empty.

Seed selects every shape decision (random.Random(int(seed, 16))); the same seed
builds byte-identical cases.  A case whose two measurements disagree is redrawn
(up to three shapes per slot) and otherwise skipped; a dropped slot never
freezes a guessed label.

CLI (counter contract):
  launchenv-fresh-r100.py --seed HEX --dir D --out F --count N
  launchenv-fresh-r100.py --selftest

stdout, after the work:
  FRESH_GEN: cases=N ok=A refused=B dot=D private=P sysbin=S
  FRESH_GEN_PIN: gio_sha256=<...> oracle_sha256=<...>
JSONL, one case dict per line on --out:
  {"id": "fresh-<seed>-NN", "class": "path-default-*", ..., "expect": {...}}
"""

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE_PATH = os.path.normpath(os.path.join(
    HERE, "..", "..", "round-99", "controls", "launchenv-probe-r99.py"))

_spec = importlib.util.spec_from_file_location("lprobe_fresh_r100", PROBE_PATH)
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)

PROBE_B64 = base64.b64encode(P.PROBE_SH.encode("ascii")).decode("ascii")
DATA_B64 = base64.b64encode(b"x\n").decode("ascii")

# TryExec candidates: names that exist only in the system directories.  Every
# name is re-checked at build time; a name that is not executable there, or
# that could shadow the case's own probe, is dropped rather than guessed.
SYSTEM_NAMES = ("sh", "xauth", "gzip", "sed", "awk", "env", "tr", "cat")

BEHAVIOURS = ("dot", "private", "sysbin")


def system_names():
    """Host names executable in /usr/bin and absent from a case root."""
    out = []
    for name in SYSTEM_NAMES:
        path = os.path.join("/usr/bin", name)
        if os.access(path, os.X_OK) and not os.path.isdir(path):
            out.append(name)
    return out


def bcase(cid, cls, path, desktop, files, dirs, args=None):
    c = {"id": cid, "class": cls, "path": path, "files": files,
         "dirs": dirs, "desktop": desktop}
    if args:
        c["args"] = args
    return c


def case_dot(rng, cid):
    """Program in the launch working directory; the '.' vs empty entry."""
    path = rng.choice([None, [], [], None])
    desktop = {"Type": "Application", "Name": "case", "Exec": "probe"}
    if rng.random() < 0.5:
        desktop["Path"] = ""
    files = {"probe": PROBE_B64}
    args = []
    if rng.random() < 0.5:
        n = rng.randint(1, 2)
        for i in range(1, n + 1):
            files["f%d" % i] = DATA_B64
            args.append("f%d" % i)
        desktop["Exec"] = "probe %f"
    return bcase(cid, "path-default-dot", path, desktop, files, [], args)


def case_private(rng, cid):
    """Program only in a case-private bin dir; the ambient search does not
    know it, an entry naming it does."""
    priv = "pbin" + "".join(rng.choice("0123456789abcdef") for _ in range(4))
    other = "qbin" + "".join(rng.choice("0123456789abcdef") for _ in range(4))
    shape = rng.choice(["unset", "onpath", "onpath-second", "empty"])
    files = {priv + "/probe": PROBE_B64}
    dirs = []
    desktop = {"Type": "Application", "Name": "case", "Exec": "probe"}
    if shape == "unset":
        path = None
    elif shape == "onpath":
        path = ["{root}/" + priv]
    elif shape == "onpath-second":
        files[other + "/keep"] = DATA_B64
        dirs.append(other)
        path = ["{root}/" + other, "{root}/" + priv]
    else:
        path = []
    if rng.random() < 0.5:
        desktop["Path"] = "{root}/work"
        files["work/keep"] = DATA_B64
        dirs.append("work")
    return bcase(cid, "path-default-private", path, desktop, files, dirs)


def case_sysbin(rng, cid, names):
    """TryExec names a system-only program: found through the unset default,
    not through PATH="" nor through a case-private directory."""
    name = rng.choice(names)
    shape = rng.choice(["unset", "unset", "empty", "private"])
    desktop = {"Type": "Application", "Name": "case",
               "Exec": "{root}/probe.sh", "TryExec": name}
    files = {}
    dirs = []
    if shape == "unset":
        path = None
    elif shape == "empty":
        path = []
    else:
        priv = "dbin" + "".join(rng.choice("0123456789abcdef")
                               for _ in range(4))
        files[priv + "/decoy"] = PROBE_B64
        path = ["{root}/" + priv]
    if rng.random() < 0.4:
        desktop["Path"] = "{root}/work"
        files["work/keep"] = DATA_B64
        dirs.append("work")
    return bcase(cid, "path-default-sysbin", path, desktop, files, dirs)


def build_case(rng, cid, behaviour, names):
    if behaviour == "dot":
        return case_dot(rng, cid)
    if behaviour == "private":
        return case_private(rng, cid)
    return case_sysbin(rng, cid, names)


def selftest():
    names = system_names()
    if not names:
        print("FRESH_GEN_SELFTEST: no system TryExec name available")
        return 1
    rng = random.Random(0)
    seen = set()
    for slot in range(60):
        behaviour = BEHAVIOURS[slot % len(BEHAVIOURS)]
        c = build_case(rng, "t%02d" % slot, behaviour, names)
        seen.add(c["class"])
        for rel, val in c["files"].items():
            base64.b64decode(val)
        if c["path"] is not None:
            for entry in c["path"]:
                if not entry.startswith("{root}/"):
                    print("FRESH_GEN_SELFTEST: host-capable entry %r" % entry)
                    return 1
        if c["path"] is None or c["path"] == []:
            continue
        for rel in c["files"]:
            if rel.startswith(c["path"][-1][len("{root}/"):]):
                break
        else:
            if behaviour == "private":
                print("FRESH_GEN_SELFTEST: private program not under its entry")
                return 1
    if seen != {"path-default-dot", "path-default-private",
                "path-default-sysbin"}:
        print("FRESH_GEN_SELFTEST: behaviours %s" % sorted(seen))
        return 1
    print("FRESH_GEN_SELFTEST: checks=3 failed=0 names=%s" % ",".join(names))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado r100 C1 fresh-case generator")
    ap.add_argument("--seed", default=None, help="hex seed")
    ap.add_argument("--dir", default=None, help="case-root parent directory")
    ap.add_argument("--out", default=None, help="JSONL output file")
    ap.add_argument("--count", type=int, default=60)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.seed and args.dir and args.out):
        ap.error("--seed, --dir and --out are required")
    names = system_names()
    if not names:
        sys.stderr.write("FRESH_GEN_SETUP: no system TryExec name available\n")
        return 2
    seed = args.seed
    rng = random.Random(int(seed, 16))
    os.makedirs(args.dir, exist_ok=True)
    pin = P.gio_sha256()
    if pin != P.GIO_SHA256:
        sys.stderr.write("MADO_LAUNCHENV_FRESH_GIO_MISMATCH %s\n" % pin)
    oracle_sha = hashlib.sha256(open(PROBE_PATH, "rb").read()).hexdigest()
    written = 0
    ok = 0
    refused = 0
    census = {b: 0 for b in BEHAVIOURS}
    slot = 0
    with open(args.out, "w", encoding="ascii", newline="\n") as out_fh:
        while written < args.count:
            slot += 1
            behaviour = BEHAVIOURS[slot % len(BEHAVIOURS)]
            cid = "fresh-%s-%02d" % (seed[:12], slot)
            case = None
            expect = None
            for _attempt in range(3):
                cand = build_case(rng, cid, behaviour, names)
                expect_i, _metas, agreed = P.measure_case(cand, args.dir, pin)
                if agreed and expect_i.get("error") != "setup-error":
                    case = cand
                    expect = expect_i
                    break
            if case is None:
                sys.stderr.write("FRESH_GEN_DROPPED slot=%d\n" % slot)
                continue
            case["expect"] = expect
            out_fh.write(json.dumps(case, sort_keys=True) + "\n")
            written += 1
            census[behaviour] += 1
            if "error" in expect:
                refused += 1
            else:
                ok += 1
    print("FRESH_GEN: cases=%d ok=%d refused=%d dot=%d private=%d sysbin=%d"
          % (written, ok, refused, census["dot"], census["private"],
             census["sysbin"]))
    print("FRESH_GEN_PIN: gio_sha256=%s oracle_sha256=%s" % (pin, oracle_sha))
    return 0 if written == args.count else 1


if __name__ == "__main__":
    sys.exit(main())
