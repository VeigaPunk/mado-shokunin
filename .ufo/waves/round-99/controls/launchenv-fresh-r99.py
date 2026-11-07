#!/usr/bin/env python3
"""mado round-99 C1 fresh-case generator (seat R99MExecOracle).

Instrument, not candidate: labels fresh cases through the oracle module
(launchenv-probe-r99.py, loaded by path) at measurement time, so the labels
are written outside the candidate's reach.  stdlib only; the only spawned
process is the oracle's own /usr/bin/gio probe.

The seed selects every shape decision (random.Random(int(seed, 16))); the
same seed builds byte-identical cases.  Fresh cases never put a host
directory on the case PATH and never name a host program: every executable
a case needs is materialised from the probe script under the case root.

CLI (counter contract):
  launchenv-fresh-r99.py --seed HEX --dir D --out F --count N

stdout, after the work:
  FRESH_GEN: cases=N ok=A refused=B
  FRESH_GEN_PIN: gio_sha256=<...> oracle_sha256=<...>
JSONL, one case dict per line on --out:
  {"id": "fresh-<seed>-NN", "class": "fresh", ..., "expect": {...}}

A case whose two measurements disagree is redrawn (up to three shapes per
slot) and otherwise skipped; a dropped slot never freezes a guessed label.
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
PROBE_PATH = os.path.join(HERE, "launchenv-probe-r99.py")

_spec = importlib.util.spec_from_file_location("lprobe_fresh", PROBE_PATH)
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)

PROBE_B64 = base64.b64encode(P.PROBE_SH.encode("ascii")).decode("ascii")
DATA_B64 = base64.b64encode(b"x\n").decode("ascii")


def bcase(cid, **kw):
    kw["id"] = cid
    kw["class"] = "fresh"
    kw.setdefault("files", {})
    kw.setdefault("path", ["{root}/bin"])
    kw.setdefault("desktop", {"Type": "Application", "Name": "case",
                              "Exec": "{root}/probe.sh"})
    return kw


def build_case(rng, cid):
    """One fresh case shape; every decision comes from rng."""
    files = {}
    dirs = []
    modes = {}
    desktop = {"Type": "Application", "Name": "case"}
    path = ["{root}/bin"]
    args = []

    # --- exec program shape -------------------------------------------
    exec_shape = rng.choice(["abs", "bare", "bare-first", "dir", "missing",
                             "dot", "sub", "exec644", "empty-entry",
                             "dot-entry"])
    probe_rel = None
    if exec_shape == "abs":
        desktop["Exec"] = "{root}/probe.sh"
    elif exec_shape == "bare":
        files["bin/probe"] = PROBE_B64
        desktop["Exec"] = "probe"
    elif exec_shape == "bare-first":
        files["bin/probe"] = PROBE_B64
        files["bin2/probe"] = PROBE_B64
        path = ["{root}/bin", "{root}/bin2"]
        desktop["Exec"] = "probe"
    elif exec_shape == "dir":
        where = rng.choice(["adir", "bin/direxe"])
        dirs.append(where)
        desktop["Exec"] = "{root}/adir" if where == "adir" else "direxe"
    elif exec_shape == "missing":
        if rng.random() < 0.5:
            desktop["Exec"] = "nope"
        else:
            desktop["Exec"] = "bin/nope"
            if "Path" not in desktop:
                desktop["Path"] = "{root}"
    elif exec_shape == "dot":
        desktop["Exec"] = "./probe.sh"
        if "Path" not in desktop:
            desktop["Path"] = "{root}"
    elif exec_shape == "sub":
        files["sub/probe.sh"] = PROBE_B64
        probe_rel = "sub/probe.sh"
        desktop["Exec"] = "sub/probe.sh"
        if "Path" not in desktop:
            desktop["Path"] = "{root}"
    elif exec_shape == "exec644":
        files["bin/probe"] = PROBE_B64
        modes["bin/probe"] = "644"
        desktop["Exec"] = "probe"
    elif exec_shape == "empty-entry":
        # the empty PATH entry searches the working dir for a bare name
        files["work/probe"] = PROBE_B64
        probe_rel = "work/probe"
        path = ["{root}/bin", ""]
        dirs.append("work")
        desktop["Exec"] = "probe"
        desktop["Path"] = "{root}/work"
    else:  # dot-entry: "." searches the launcher cwd, keeps the "./"
        files["probe"] = PROBE_B64
        probe_rel = "probe"
        path = ["."]
        desktop["Exec"] = "probe"

    # --- working directory shape (when the exec shape left it open) ----
    if "Path" not in desktop:
        cwd_shape = rng.choice(["none", "none", "empty", "work"])
        if cwd_shape == "work":
            desktop["Path"] = "{root}/work"
            dirs.append("work")
        elif cwd_shape == "empty":
            desktop["Path"] = ""
    if "Path" in desktop and desktop["Path"] == "{root}/work":
        dirs.append("work")

    # --- terminal shape -------------------------------------------------
    term_shape = rng.choice(["none-declared", "none-declared", "row",
                             "row", "row-644", "row-rel", "declared-absent"])
    term_name, _term_arg = rng.choice(P.KNOWN_TERMINALS)
    if term_shape in ("row", "row-644", "row-rel"):
        if term_shape == "row-rel":
            # reachable only through a relative PATH entry + working_dir
            files["work/bin/" + term_name] = PROBE_B64
            dirs.append("work")
            path.append("bin")
            if "Path" not in desktop:
                desktop["Path"] = "{root}/work"
        else:
            files["bin/" + term_name] = PROBE_B64
            if term_shape == "row-644":
                modes["bin/" + term_name] = "644"
                winner = ("gnome-terminal" if term_name != "gnome-terminal"
                          else "kgx")
                files["bin/" + winner] = PROBE_B64
        desktop["Terminal"] = True
    elif term_shape == "declared-absent":
        desktop["Terminal"] = True

    # --- TryExec shape ---------------------------------------------------
    tx_shape = rng.choice(["none", "none", "ok", "viawd", "missing", "tx644"])
    if tx_shape == "ok":
        files["bin/helper"] = PROBE_B64
        desktop["TryExec"] = "helper"
    elif tx_shape == "viawd":
        files["work/helper"] = PROBE_B64
        desktop["TryExec"] = "helper"
        if "Path" not in desktop:
            desktop["Path"] = "{root}/work"
    elif tx_shape == "missing":
        desktop["TryExec"] = "missingprog"
    elif tx_shape == "tx644":
        files["bin/helper"] = PROBE_B64
        modes["bin/helper"] = "644"
        desktop["TryExec"] = "helper"

    # --- arguments --------------------------------------------------------
    if rng.random() < 0.5 and probe_rel is None:
        n = rng.randint(1, 3)
        for i in range(1, n + 1):
            files["f%d" % i] = DATA_B64
            args.append("f%d" % i)
        desktop["Exec"] = desktop["Exec"] + " %f"

    kw = bcase(cid, path=path, files=files, dirs=dirs, desktop=desktop)
    if modes:
        kw["modes"] = modes
    if args:
        kw["args"] = args
    if rng.random() < 0.1 and not args:
        kw["rel_desktop"] = True
    return kw


def selftest():
    rng = random.Random(0)
    seen_exec = set()
    for _ in range(400):
        c = build_case(rng, "t")
        seen_exec.add(c["desktop"]["Exec"].split(" ")[0])
        for rel, val in c["files"].items():
            base64.b64decode(val)
        for rel in (c.get("modes") or {}):
            if rel not in c["files"]:
                print("FRESH_GEN_SELFTEST: modes-without-file %s" % rel)
                return 1
        # a Terminal=true case always has a terminal file or expects refusal
    for want in ("{root}/probe.sh", "probe", "direxe", "{root}/adir",
                 "sub/probe.sh", "./probe.sh", "bin/nope", "nope"):
        if want not in seen_exec:
            print("FRESH_GEN_SELFTEST: missing exec shape %s" % want)
            return 1
    print("FRESH_GEN_SELFTEST: checks=2 failed=0")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="mado r99 C1 fresh-case generator")
    ap.add_argument("--seed", default=None, help="hex seed")
    ap.add_argument("--dir", default=None, help="case-root parent directory")
    ap.add_argument("--out", default=None, help="JSONL output file")
    ap.add_argument("--count", type=int, default=40)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.seed and args.dir and args.out):
        ap.error("--seed, --dir and --out are required")
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
    slot = 0
    with open(args.out, "w", encoding="ascii", newline="\n") as out_fh:
        while written < args.count:
            slot += 1
            cid = "fresh-%s-%02d" % (seed[:12], slot)
            case = None
            expect = None
            for _attempt in range(3):
                cand = build_case(rng, cid)
                expect_i, _metas, agreed = P.measure_case(cand, args.dir, pin)
                if agreed and expect_i.get("error") != "setup-error":
                    case = cand
                    expect = expect_i
                    break
            if case is None:
                continue
            case["expect"] = expect
            out_fh.write(json.dumps(case) + "\n")
            written += 1
            if "error" in expect:
                refused += 1
            else:
                ok += 1
    print("FRESH_GEN: cases=%d ok=%d refused=%d" % (written, ok, refused))
    print("FRESH_GEN_PIN: gio_sha256=%s oracle_sha256=%s" % (pin, oracle_sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
