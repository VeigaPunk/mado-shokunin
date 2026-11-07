#!/usr/bin/env python3
"""magictext-fresh-r96 — seeded random case generator for the round-96 C1 text-magic wave.

  python3 -I magictext-fresh-r96.py --seed N --out FILE [--oracle BIN] [--scratch DIR]

Generates text/none-mode cases in the round-96 case schema (version 2) with >= 120
inputs in total, labels EVERY input by running the compiled GLib oracle (Shared
contract 3), and writes the labelled envelope to --out.  Deterministic for a given
seed on the same host; never reads the frozen case file; stdlib only; ASCII output.

If --oracle is not given, the pinned round-95 oracle source is compiled into the
scratch dir with the contract-3 command (cc -O0 ... $(pkg-config gio-2.0)).
No reachable mime.cache fixture is ever generated (fresh stays text/none).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import random
import subprocess
import sys
import tempfile

ORACLE_SHA = "99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a"
ORACLE_SRC = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/controls/mimesniff-oracle-r95.c"
GLIB = "2.90.1-1"
CLASSES = ["header", "sect", "value", "mask", "word", "range", "indent", "order",
           "drop", "multi", "glob", "alias", "fallback", "zerosize", "mode", "desktop"]
HDR = b"MIME-Magic\x00\n"
MIN_INPUTS = 140
MAX_CASES = 90
ORACLE_TIMEOUT = 10.0

PRIOS = [0, 1, 10, 50, 79, 80, 90, 100, 1000, 2147483647]


def be16(n):
    return bytes([(n >> 8) & 0xFF, n & 0xFF])


def mline(indent, offset, value, mask=None, word=None, rng=None):
    b = b"%d>%d=" % (indent, offset) + be16(len(value)) + value
    if mask is not None:
        b += b"&" + mask
    if word is not None:
        b += b"~" + str(word).encode()
    if rng is not None:
        b += b"+" + str(rng).encode()
    return b + b"\n"


class CaseGen:
    def __init__(self, rng):
        self.rng = rng
        self.serial = 0

    def token(self):
        self.serial += 1
        return b"TK%02d" % (self.serial % 100)

    def mtype(self, case_idx, k):
        return "app/x-f%d_%d" % (case_idx, k)

    def value_bytes(self, tok):
        r = self.rng
        kind = r.randrange(6)
        if kind == 0:
            return tok
        if kind == 1:
            return bytes([r.randrange(0x80, 0x100) for _ in range(r.randrange(1, 5))]) + tok
        if kind == 2:
            return tok + b"\n" + tok
        if kind == 3:
            return tok + b"\x00" + tok
        if kind == 4:
            return b"\x89PNG\r\n\x1a\n" if r.randrange(2) else tok
        return tok[::-1] + b"."

    def matchlet_chain(self, tok):
        """A structurally nested matchlet line list: parents at lower indents."""
        r = self.rng
        depth = r.randrange(1, 4)
        lines = []
        offset = 0
        for lvl in range(depth):
            val = self.value_bytes(tok) if r.randrange(4) else tok
            word = None
            if r.randrange(3) == 0:
                word = r.choice([0, 1, 2, 4])
                if word > 1 and len(val) % word:
                    val += b"\x00" * (word - len(val) % word)
            mask = None
            if r.randrange(2) == 0:
                mask = bytes([r.choice([0x00, 0x0F, 0xF0, 0xFF, 0xDF]) for _ in val])
            rng_len = r.choice([None, 1, 1, 2, 3, 0])
            lines.append(mline(lvl, offset, val, mask=mask, word=word, rng=rng_len))
            offset += len(val) + r.randrange(0, 3)
        return lines, offset

    def magic_file(self, case_idx, n_sections):
        r = self.rng
        out = bytearray(HDR)
        toks = []
        for k in range(n_sections):
            if r.randrange(12) == 0:
                out += b"[%d:%s\n" % (r.choice(PRIOS), self.mtype(case_idx, k).encode())
                continue
            prio = r.choice(PRIOS)
            mtype = self.mtype(case_idx, k)
            out += b"[%d:%s]\n" % (prio, mtype.encode())
            tok = self.token()
            toks.append((mtype, tok))
            lines, _end = self.matchlet_chain(tok)
            out += b"".join(lines)
            if r.randrange(10) == 0:
                out += b"X>0=broken\n"          # first-char parse error line
        if r.randrange(10) == 0:
            out += b">9=trunc"                   # truncated final line at EOF
        return bytes(out), toks

    def case(self, idx):
        r = self.rng
        use_dh = r.randrange(2) == 0
        dirs = ["dh"] if use_dh else []
        dirs += [d for d in ("d1", "d2") if r.randrange(3) or not dirs]
        if not dirs:
            dirs = ["d1"]
        files = {}
        toks = []
        n_magic_dirs = 0
        for d in dirs:
            kind = r.randrange(10)
            if kind == 0:                      # none-mode-ish dir: no mime files
                files[d + "/.keep"] = b""
                continue
            if kind == 1:
                files[d + "/mime/globs2"] = b"".join(
                    b"50:%s:*.f%d\n" % (self.mtype(idx, 50 + j).encode(), j)
                    for j in range(r.randrange(1, 3)))
                continue
            mg, t = self.magic_file(idx, r.randrange(1, 4))
            files[d + "/mime/magic"] = mg
            toks += t
            n_magic_dirs += 1
            if r.randrange(3) == 0:
                a, c = self.mtype(idx, 70), toks[0][0] if toks else self.mtype(idx, 71)
                files[d + "/mime/aliases"] = b"%s %s\n" % (a.encode(), c.encode())
            if r.randrange(3) == 0:
                t1 = toks[0][0] if toks else self.mtype(idx, 72)
                files[d + "/mime/subclasses"] = b"%s text/plain\n" % t1.encode()
        env = {"HOME": "{root}/h",
               "XDG_DATA_HOME": "{root}/dh" if use_dh else None,
               "XDG_DATA_DIRS": "{root}/d1:{root}/d2"}
        inputs = []
        for mtype, tok in toks[:6]:
            data = tok + b"tail"
            if r.randrange(2):
                data = b"head" + data
            inputs.append((None, data))
            flip = bytearray(data)
            flip[r.randrange(len(flip))] ^= 0x01
            inputs.append((None, bytes(flip)))
        if r.randrange(3) == 0:
            inputs.append((None, b"plain text only\n"))
        if r.randrange(3) == 0:
            inputs.append((None, bytes([r.randrange(256) for _ in range(12)])))
        if r.randrange(4) == 0:
            inputs.append((None, b""))
        if r.randrange(3) == 0:
            inputs.append((b"zz.nope", b"whatever data"))
        if not inputs:
            inputs.append((None, b"plain text only\n"))
        inputs = inputs[:12]
        cls = "mode" if n_magic_dirs == 0 else r.choice(
            ["header", "sect", "value", "mask", "word", "range", "indent", "order",
             "drop", "multi", "glob", "alias", "fallback", "zerosize", "mode", "desktop"])
        cid = "fresh-%s-%03d" % (cls, idx)
        return {"id": cid, "class": cls, "env": env,
                "files": {k: base64.b64encode(v).decode("ascii") for k, v in sorted(files.items())},
                "inputs": [{"name_b64": None if n is None else base64.b64encode(n).decode("ascii"),
                            "data_b64": base64.b64encode(d).decode("ascii")} for n, d in inputs],
                "labels": []}


def compile_oracle(scratch):
    binary = os.path.join(scratch, "oracle")
    pkg = subprocess.run(["pkg-config", "--cflags", "--libs", "gio-2.0"],
                         capture_output=True, check=True)
    cmd = ["cc", "-O0", "-o", binary, ORACLE_SRC] + pkg.stdout.decode().split()
    subprocess.run(cmd, check=True)
    return binary


def run_oracle(oracle, env, pairs, timeout):
    args = [oracle]
    for name, fp in pairs:
        args.append("0" if name is None else b"=" + name)
        args.append(fp)
    r = subprocess.run(args, env=env, capture_output=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError("oracle rc=%d" % r.returncode)
    lines = r.stdout.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    if len(lines) != len(pairs):
        raise RuntimeError("oracle line count %d != %d" % (len(lines), len(pairs)))
    out = []
    for ln in lines:
        t, u = ln.rsplit(b"\t", 1)
        if u not in (b"0", b"1"):
            raise RuntimeError("bad oracle line %r" % ln[:60])
        out.append([t.decode("utf-8", "surrogateescape"), int(u)])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--oracle", help="path to the compiled mimesniff-oracle-r95 binary")
    ap.add_argument("--scratch", help="scratch dir (default: a fresh tempdir)")
    a = ap.parse_args()

    scratch = a.scratch or tempfile.mkdtemp(prefix="magictext-fresh-")
    os.makedirs(scratch, exist_ok=True)
    oracle = a.oracle
    if oracle is None:
        oracle = compile_oracle(scratch)

    rng = random.Random(a.seed)
    gen = CaseGen(rng)
    cases = []
    dropped = []
    total_inputs = 0
    idx = 0
    while len(cases) < MAX_CASES and (total_inputs < MIN_INPUTS or idx < 40):
        c = gen.case(idx)
        root = os.path.join(scratch, "case-%03d" % idx)
        os.makedirs(os.path.join(root, "h"), exist_ok=True)
        os.makedirs(os.path.join(root, ".inputs"), exist_ok=True)
        for rel, v in c["files"].items():
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(base64.b64decode(v))
        pairs = []
        for i, inp in enumerate(c["inputs"]):
            fp = os.path.join(root, ".inputs", "d%03d" % i)
            with open(fp, "wb") as fh:
                fh.write(base64.b64decode(inp["data_b64"]))
            name = None if inp["name_b64"] is None else base64.b64decode(inp["name_b64"])
            pairs.append((name, fp))
        env = {"LC_ALL": "C", "HOME": os.path.join(root, "h")}
        if c["env"]["XDG_DATA_HOME"] is not None:
            env["XDG_DATA_HOME"] = c["env"]["XDG_DATA_HOME"].replace("{root}", root)
        env["XDG_DATA_DIRS"] = c["env"]["XDG_DATA_DIRS"].replace("{root}", root)
        try:
            c["labels"] = run_oracle(oracle, env, pairs, ORACLE_TIMEOUT)
        except Exception as e:                                   # drop, keep going
            dropped.append((c["id"], str(e)))
            idx += 1
            continue
        total_inputs += len(c["inputs"])
        cases.append(c)
        idx += 1

    doc = {"version": 2, "db_mode": "text", "oracle_src_sha256": ORACLE_SHA,
           "glib2": GLIB, "classes": CLASSES, "cases": cases}
    with open(a.out, "wb") as fh:
        fh.write(json.dumps(doc, indent=1).encode("ascii"))
        fh.write(b"\n")
    print("magictext-fresh-r96: seed=%d cases=%d inputs=%d dropped=%d out=%s"
          % (a.seed, len(cases), total_inputs, len(dropped), a.out))
    for cid, err in dropped:
        print("magictext-fresh-r96: DROPPED %s: %s" % (cid, err))
    return 0


if __name__ == "__main__":
    sys.exit(main())
