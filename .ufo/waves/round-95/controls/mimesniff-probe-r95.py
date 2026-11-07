#!/usr/bin/env python3
"""round-95 L1 DRAFT probe: compare a mado-mimesniff candidate with the compiled GLib oracle.

  mimesniff-probe-r95.py --tool T --oracle BIN --scratch DIR selftest   # the selftest fixtures, both dir sets
  mimesniff-probe-r95.py --tool T --oracle BIN --scratch DIR host FILE  # FILE: one path per line; each sniffed
                                                                          # data-only and with its own path as name
The tool is loaded as a module (its directory must hold mado-mimeglob.py).  Prints DIFF lines and a summary.
"""
import argparse
import importlib.util
import os
import subprocess
import sys


def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def oracle(bin_, env, pairs, scratch):
    args, files = [], []
    for k, (name, data) in enumerate(pairs):
        f = os.path.join(scratch, f"d{k}")
        with open(f, "wb") as fh:
            fh.write(data)
        args += ["0" if name is None else b"=" + name, f]
    out = []
    for s in range(0, len(args), 2000):
        r = subprocess.run([bin_] + args[s:s + 2000], env=env, capture_output=True, check=True)
        out += [tuple(x.split(b"\t")) for x in r.stdout.splitlines()]
    return [(t.decode(), int(u)) for t, u in out]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("leg")
    ap.add_argument("arg", nargs="?")
    a = ap.parse_args()
    m = load(a.tool)
    os.makedirs(a.scratch, exist_ok=True)
    diffs = total = 0
    if a.leg == "host":
        env = dict(os.environ)
        dirs = m.mg.xdgmime_dirs(env.get("XDG_DATA_HOME"), env.get("HOME"), env.get("XDG_DATA_DIRS"))
        sn = m.Sniffer(dirs)
        pairs = []
        for line in open(a.arg, "rb").read().splitlines():
            try:
                with open(line, "rb") as fh:
                    data = fh.read(4096)
            except OSError:
                continue
            pairs += [(None, data), (line, data)]
        want = oracle(a.oracle, env, pairs, a.scratch)
        for (name, data), w in zip(pairs, want):
            r = sn.guess(name, data)
            total += 1
            if (r["type"], r["uncertain"]) != w:
                diffs += 1
                print("DIFF", name, data[:16], (r["type"], r["uncertain"]), w)
    print(f"PROBE leg={a.leg} total={total} diffs={diffs}")


if __name__ == "__main__":
    main()
