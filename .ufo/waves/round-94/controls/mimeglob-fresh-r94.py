#!/usr/bin/env python3
"""mimeglob-fresh-r94 — seeded generator of UNLABELLED mimeglob cases (round-94 C1).

Writes a case file (CASE FILE SCHEMA envelope, no labels) of N random layouts:
half text mode (globs2/globs bytes), half cache mode (mime.cache bytes produced by
running update-mime-database on packages/*.xml inside --scratch-root).  Names are
drawn to both hit and miss the generated globs.  Deterministic for a seed: all
randomness comes from random.Random(seed) and update-mime-database output is
byte-stable for a given XML (verified on shared-mime-info 2.5.1-2).

Usage:
  mimeglob-fresh-r94.py --seed S --n N --out FILE --scratch-root DIR

--scratch-root is required; it receives every generated tree and the
update-mime-database runs (run with TMPDIR=<scratch-root>); nothing is written
outside it and the output FILE.  Envelope keys match the frozen case file; fresh
cases carry "class": "fresh" and no "labels" key (they are labelled at
measurement time by the live oracle).
"""
import argparse
import base64
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys

ORACLE_SRC_SHA = "9c4337b36f93fa71bce13938f93d2e9758bb752815a67c57eb934a70bbfa6b11"
GLIB2 = "2.90.1-1"

STEMS = ["data", "img", "log", "note", "run", "cfg", "tmp", "arc", "bin", "doc",
         "song", "clip", "src", "pkg", "core", "dump", "idx", "map", "set", "x1"]
EXTS = ["frt", "z7", "qk", "mvv", "pl9", "oz", "kd", "wv2", "tx1", "br5", "nv", "st3"]
WORDS = ["make", "todo", "readme", "index", "license", "build", "changelog", "notice"]
FLAGS = [b"", b":cs", b":cs,extra", b":x,cs"]
WEIGHTS = [0, 10, 40, 50, 50, 60, 80, 100]


def _put(files, rel, data):
    files[rel] = data


def _rand_word(rng):
    return rng.choice(WORDS) + (rng.choice(["", "2", "-x"]) if rng.random() < 0.4 else "")


def _rand_stem(rng):
    return rng.choice(STEMS) + (str(rng.randrange(100)) if rng.random() < 0.4 else "")


def _rand_ext(rng):
    return rng.choice(EXTS)


def text_layout(rng, idx):
    """One text-mode fixture: globs2 lines plus the names that hit/miss them."""
    lines = []
    hits = []
    n_types = rng.randrange(1, 4)
    for t in range(n_types):
        typ = ("app/x-fresh-%d-%d" % (idx, t)).encode()
        kind = rng.randrange(3)
        w = rng.choice(WEIGHTS)
        if kind == 0:  # simple suffix
            ext = _rand_ext(rng)
            lines.append(b"%d:%s:*.%s%s" % (w, typ, ext.encode(), rng.choice(FLAGS)))
            hits.append(("%s.%s" % (_rand_stem(rng), ext)).encode())
            if rng.random() < 0.5:
                hits.append(("%s.%s" % (_rand_stem(rng), ext.upper())).encode())
        elif kind == 1:  # literal
            word = _rand_word(rng)
            lines.append(b"%d:%s:%s%s" % (w, typ, word.encode(), rng.choice([b"", b":cs"])))
            hits.append(word.encode())
        else:  # full glob
            a = rng.choice(["", "d"])
            cls = rng.choice(["[ab]", "[[:digit:]]", "?"])
            pat = ("*%s%sz" % (a, cls)).encode() if rng.random() < 0.5 else b"?e*"
            lines.append(b"%d:%s:%s" % (w, typ, pat))
            stem = _rand_stem(rng)
            if pat.startswith(b"?e*"):
                hits.append((stem[:1] + "e" + _rand_word(rng)).encode())
            else:
                filler = rng.choice(["a", "b", "7"]) if cls == "[ab]" or cls == "[[:digit:]]" else "q"
                hits.append((stem + (a or "") + filler + "z").encode())
    misses = [( _rand_stem(rng) + "." + _rand_ext(rng) + "zz").encode() for _ in range(2)]
    names = hits + misses
    rng.shuffle(names)
    env = {"HOME": "{root}/h"}
    files = {}
    dh = rng.choice([True, False])
    if dh:
        env["XDG_DATA_HOME"] = "{root}/dh"
        dir_ = "dh"
    else:
        env["XDG_DATA_HOME"] = None
        dir_ = "h/.local/share"
    ndirs = rng.choice([1, 1, 2])
    dirs = [dir_] + ["s%d" % (i + 1) for i in range(ndirs - 1)]
    env["XDG_DATA_DIRS"] = ":".join("{root}/" + d for d in dirs[1:]) or None
    if rng.random() < 0.15:
        # v1 fallback in the last dir
        split = max(1, len(lines) - 1)
        head, tail = lines[:split], lines[split:]
        _put(files, dirs[0] + "/mime/globs2", b"\n".join(head) + b"\n")
        if tail:
            _put(files, dirs[-1] + "/mime/globs",
                 b"\n".join(l.split(b":", 1)[1] for l in tail) + b"\n")
    else:
        per = max(1, len(lines) // len(dirs))
        for i, d in enumerate(dirs):
            chunk = lines[i * per:(i + 1) * per] if i < len(dirs) - 1 else lines[i * per:]
            if chunk:
                _put(files, d + "/mime/globs2", b"\n".join(chunk) + b"\n")
    mode = "text"
    return mode, env, files, names


def cache_layout(rng, idx, scratch):
    """One cache-mode fixture: mime.cache from update-mime-database + hit/miss names."""
    types = ["application/x-freshc-%d-%d" % (idx, t) for t in range(rng.randrange(1, 4))]
    hits = []
    body = []
    for t, typ in enumerate(types):
        kind = rng.randrange(3)
        if kind == 0:
            ext = _rand_ext(rng)
            body.append('  <mime-type type="%s">\n    <glob pattern="*.%s"/>\n  </mime-type>\n'
                        % (typ, ext))
            hits.append(("%s.%s" % (_rand_stem(rng), ext)).encode())
        elif kind == 1:
            body.append('  <mime-type type="%s">\n    <glob pattern="*.%s" weight="80"/>\n  </mime-type>\n'
                        % (typ, _rand_ext(rng)))
            ext = "w8"
            body.append('  <mime-type type="%s">\n    <glob pattern="*.%s"/>\n  </mime-type>\n'
                        % (typ, ext))
            hits.append(("%s.%s" % (_rand_stem(rng), ext)).encode())
        elif kind == 2:
            body.append('  <mime-type type="%s">\n    <glob pattern="*%s*"/>\n  </mime-type>\n'
                        % (typ, _rand_word(rng)))
            word = body[-1].split('pattern="*')[1].split('*"')[0]
            hits.append((_rand_stem(rng) + word + _rand_stem(rng)).encode())
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">\n'
           + "".join(body) + '</mime-info>\n')
    gendir = os.path.join(scratch, "fresh-gen-%d-%d" % (idx, rng.randrange(1 << 30)))
    # NOTE: gendir is derived from seeded rng only -> deterministic path.
    os.makedirs(os.path.join(gendir, "packages"), exist_ok=True)
    with open(os.path.join(gendir, "packages", "t.xml"), "w") as fh:
        fh.write(xml)
    env2 = dict(os.environ)
    env2["TMPDIR"] = scratch
    subprocess.run(["update-mime-database", gendir], env=env2, check=True,
                   capture_output=True, timeout=120)
    cache = open(os.path.join(gendir, "mime.cache"), "rb").read()
    shutil.rmtree(gendir, ignore_errors=True)
    misses = [(_rand_stem(rng) + ".zz" + _rand_ext(rng)).encode() for _ in range(2)]
    names = hits + misses
    rng.shuffle(names)
    env = {"HOME": "{root}/h"}
    files = {}
    ndirs = rng.choice([1, 1, 2])
    dirs = ["s%d" % (i + 1) for i in range(ndirs)]
    if rng.random() < 0.5:
        env["XDG_DATA_HOME"] = "{root}/dh"
        dirs = ["dh"] + dirs[:ndirs - 1]
    else:
        env["XDG_DATA_HOME"] = None
    env["XDG_DATA_DIRS"] = ":".join("{root}/" + d for d in dirs[1:]) or None
    _put(files, dirs[0] + "/mime/mime.cache", cache)
    if len(dirs) > 1 and rng.random() < 0.5:
        _put(files, dirs[1] + "/mime/mime.cache", cache)
    if rng.random() < 0.3 and len(dirs) > 1:
        # a decoy globs2 dir that must be ignored while a cache is present
        _put(files, dirs[1] + "/mime/globs2", b"50:app/x-freshc-decoy:*.txt\n")
    return "cache", env, files, names


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scratch-root", required=True)
    a = ap.parse_args()
    os.makedirs(a.scratch_root, exist_ok=True)
    rng = random.Random(a.seed)
    cases = []
    for i in range(a.n):
        if i % 2 == 0:
            mode, env, files, names = text_layout(rng, i)
        else:
            mode, env, files, names = cache_layout(rng, i, a.scratch_root)
        cases.append({
            "id": "fresh-%s-%03d" % (a.seed, i),
            "class": "fresh",
            "mode": mode,
            "env": env,
            "files": {k: base64.b64encode(v).decode() for k, v in sorted(files.items())},
            "names_b64": [base64.b64encode(n).decode() for n in names],
        })
    out = {"version": 1, "oracle_src_sha256": ORACLE_SRC_SHA, "glib2": GLIB2,
           "seed": a.seed, "cases": cases}
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %s: %d cases (seed %d)" % (a.out, len(cases), a.seed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
