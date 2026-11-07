#!/usr/bin/env python3
"""Build fixture MIME roots in scratch, run the oracle and the candidate on them, print a table."""
import json
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(S, "oracle")
TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-94/build/mado-mimeglob.c1.py"
ROOT = os.path.join(S, "roots")

CASES = []


def put(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode) as fh:
        fh.write(data)


def case(cid, files, names, data_home="dh", data_dirs="s1:s2", home="h", build=None):
    CASES.append(dict(id=cid, files=files, names=names, data_home=data_home,
                      data_dirs=data_dirs, home=home, build=build))


def build_cache(pkg_xml, out_rel):
    """Write a package XML and run update-mime-database on <root>/<out_rel>."""
    def f(root):
        d = os.path.join(root, out_rel)
        os.makedirs(d, exist_ok=True)
        put(os.path.join(d, "packages", "p.xml"), pkg_xml)
        r = subprocess.run(["update-mime-database", d], capture_output=True)
        if r.returncode != 0:
            raise SystemExit(f"update-mime-database failed: {r.stderr!r}")
        for junk in ("packages",):
            shutil.rmtree(os.path.join(d, junk), ignore_errors=True)
    return f


# ---- E1 text mode basics -------------------------------------------------
case("e1-text-basics", {"dh/mime/globs2": (
    "50:text/plain:*.txt\n"
    "50:text/x-c:*.c:cs\n"
    "50:text/x-c++:*.C:cs\n"
    "20:app/x-gz:*.gz\n"
    "50:app/x-tgz:*.tar.gz\n"
    "60:app/hi:*.dup\n"
    "40:app/lo:*.dup\n"
    "50:text/x-make:Makefile\n"
    "50:app/full:x?y\n"
    "50:t/one:*.two\n"
    "50:t/other:*.two\n"
    "50:img/gif:*.gif\n")},
    ["a.txt", "A.TXT", "x.C", "x.c", "Makefile", "MAKEFILE", "x.tar.gz", "X.TAR.GZ",
     "x.gz", "x.dup", "xzy", "XZY", "x?y", "f.two", "zz", "d/", "dir.txt/f.c", "IMAGE.GIF"])

# ---- E2 deepest suffix vs weight ----------------------------------------
case("e2-deep-vs-weight", {"dh/mime/globs2": (
    "10:app/deep:*.a.b.c\n"
    "90:app/shallow:*.c\n"
    "5:app/deep2:*.tar.gz\n"
    "95:app/gz:*.gz\n")},
    ["x.a.b.c", "x.tar.gz"])

# ---- E3 full glob case handling in text mode -----------------------------
case("e3-full-glob", {"dh/mime/globs2": (
    "50:app/full:x?y\n"
    "50:app/full2:*[0-9].dat\n"
    "50:app/full3:*.x*y\n")},
    ["xzy", "XZY", "x1.dat", "X1.DAT", "a.xY", "a.Xy"])

# ---- E4 __NOGLOBS__ in a later dir --------------------------------------
case("e4-noglobs-text", {
    "s1/mime/globs2": "50:text/x-diff:*.patch\n50:text/x-diff:*.diff\n",
    "s2/mime/globs2": "0:text/x-diff:__NOGLOBS__\n50:text/x-diff:*.d2\n"},
    ["a.patch", "a.diff", "a.d2", "__NOGLOBS__"])

# ---- E5 user globs2 next to a system cache ------------------------------
_cache_pkg = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
              "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
              " <mime-type type=\"sys/one\"><glob pattern=\"*.sys\" weight=\"50\"/></mime-type>\n"
              "</mime-info>\n")


def _mk_e5(root):
    build_cache(_cache_pkg, "s2/mime")(root)


case("e5-globs-beside-cache", {"dh/mime/globs2": "50:usr/two:*.sys\n"},
     ["a.sys", "b.txt"], build=_mk_e5)

# ---- E6 two caches, overlapping suffixes --------------------------------
_pkg_a = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"c/one\"><glob pattern=\"*.gz\" weight=\"20\"/></mime-type>\n"
          "</mime-info>\n")
_pkg_b = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"c/two\"><glob pattern=\"*.tar.gz\" weight=\"50\"/></mime-type>\n"
          " <mime-type type=\"c/three\"><glob pattern=\"Makefile\" weight=\"50\"/></mime-type>\n"
          " <mime-type type=\"c/four\"><glob pattern=\"zz?q\" weight=\"50\"/></mime-type>\n"
          "</mime-info>\n")


def _mk_e6(root):
    build_cache(_pkg_a, "s1/mime")(root)
    build_cache(_pkg_b, "s2/mime")(root)


case("e6-two-caches", {}, ["x.tar.gz", "Makefile", "MAKEFILE", "zzXq", "zzxq"], build=_mk_e6)

# same globs in text mode for contrast
case("e6b-two-text", {
    "s1/mime/globs2": "20:c/one:*.gz\n",
    "s2/mime/globs2": "50:c/two:*.tar.gz\n50:c/three:Makefile\n50:c/four:zz?q\n"},
    ["x.tar.gz", "Makefile", "MAKEFILE", "zzXq", "zzxq"])

# ---- E7 a single cache with a cs glob and weights ----------------------
_pkg_c = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"c/cs\"><glob pattern=\"*.c\" weight=\"50\"/><glob pattern=\"*.C\" weight=\"50\"/></mime-type>\n"
          " <mime-type type=\"c/hi\"><glob pattern=\"*.dup\" weight=\"60\"/></mime-type>\n"
          " <mime-type type=\"c/lo\"><glob pattern=\"*.dup\" weight=\"40\"/></mime-type>\n"
          "</mime-info>\n")


def _mk_e7(root):
    build_cache(_pkg_c, "dh/mime")(root)


case("e7-cache-multi", {}, ["x.C", "x.c", "x.dup", "X.DUP"], build=_mk_e7)

# ---- E8 dir/环境 rules --------------------------------------------------
case("e8-data-dirs-unset", {"s1/mime/globs2": "50:from/s1:*.one\n",
                            "s2/mime/globs2": "50:from/s2:*.two\n",
                            "dh/mime/globs2": "50:from/dh:*.dh\n"},
     ["a.one"], data_dirs=None)
case("e8b-data-dirs-empty", {"s1/mime/globs2": "50:from/s1:*.one\n"},
     ["a.one"], data_dirs="")
case("e8c-data-home-empty", {"dh/mime/globs2": "50:from/dh:*.dh\n",
                             "s1/mime/globs2": "50:from/s1:*.one\n"},
     ["a.one"], data_home="")
case("e8d-home-unset", {"s1/mime/globs2": "50:from/s1:*.one\n"}, ["a.one"], data_home=None)
case("e8e-empty-element", {"s1/mime/globs2": "50:from/s1:*.one\n"},
     ["a.one"], data_dirs=":s1:")

# ---- E9 literal vs glob on the same name -------------------------------
case("e9-literal-vs-glob", {"dh/mime/globs2": (
    "90:app/glob:*.mk\n"
    "10:app/lit:build.mk\n")},
    ["build.mk"])

# ---- E10 cache weight > 255 (fabricated cache) -------------------------
def _mk_e10(root):
    # minimal cache: header + literal list with one entry of weight 0x12C (300)
    import struct
    d = os.path.join(root, "dh/mime")
    os.makedirs(d, exist_ok=True)
    entries = []      # (name, mime, weight)
    off = 40
    n = len(entries)
    blob = b""
    # literal list at 40: count + n*12, then strings
    literal_at = 40
    strings_at = literal_at + 4 + 12 * 1
    names = b"big.dat\0app/weight\0"
    header = bytearray(40)
    struct.pack_into(">HH", header, 0, 1, 2)
    struct.pack_into(">I", header, 12, literal_at)
    struct.pack_into(">I", header, 16, 0)   # suffix list offsets left 0 -> bounds check skips
    struct.pack_into(">I", header, 20, 0)
    body = struct.pack(">I", 1)
    body += struct.pack(">III", strings_at, strings_at + 8, 300)
    put(os.path.join(d, "mime.cache"), bytes(header) + body + names)


case("e10-cache-weight-300", {}, ["big.dat"], build=_mk_e10)
case("e10b-text-weight-300", {"dh/mime/globs2": "300:app/weight:*.big\n10:app/other:*.big\n"},
     ["x.big"])


# ---- E11 text: a suffix match does not stop full globs -----------------
case("e11-text-suffix-plus-full", {"dh/mime/globs2": (
    "50:a/suffix:*.y\n"
    "50:a/full:x?y\n"
    "50:a/tgz:*.tar.gz\n"
    "50:a/fullgz:x*.gz\n")},
    ["x.y", "x.tar.gz"])

_pkg_d = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"d/suffix\"><glob pattern=\"*.y\" weight=\"50\"/></mime-type>\n"
          " <mime-type type=\"d/full\"><glob pattern=\"x?y\" weight=\"50\"/></mime-type>\n"
          " <mime-type type=\"d/tgz\"><glob pattern=\"*.tar.gz\" weight=\"50\"/></mime-type>\n"
          " <mime-type type=\"d/fullgz\"><glob pattern=\"x*.gz\" weight=\"50\"/></mime-type>\n"
          "</mime-info>\n")


def _mk_e11(root):
    build_cache(_pkg_d, "dh/mime")(root)


case("e11b-cache-suffix-plus-full", {}, ["x.y", "x.tar.gz"], build=_mk_e11)

# ---- E12 fabricated caches: weight masking and cs literal --------------
def _mk_e12(root):
    import struct
    d = os.path.join(root, "dh/mime")
    os.makedirs(d, exist_ok=True)
    header = bytearray(40)
    struct.pack_into(">HH", header, 0, 1, 2)
    struct.pack_into(">I", header, 12, 0)
    struct.pack_into(">I", header, 16, 0)
    struct.pack_into(">I", header, 20, 40)      # fnmatch list at 40
    # 2 entries: (pattern, mime, weight) 300 -> low byte 44, and 50
    strings_at = 40 + 4 + 24
    pats = b"*.big\0high/one\0low/two\0"
    body = struct.pack(">I", 2)
    body += struct.pack(">III", strings_at, strings_at + 7, 300)
    body += struct.pack(">III", strings_at, strings_at + 16, 50)
    put(os.path.join(d, "mime.cache"), bytes(header) + body + pats)


case("e12-cache-weight-lowbyte", {}, ["x.big"], build=_mk_e12)

def _mk_e13(root):
    import struct
    d = os.path.join(root, "dh/mime")
    os.makedirs(d, exist_ok=True)
    header = bytearray(40)
    struct.pack_into(">HH", header, 0, 1, 2)
    struct.pack_into(">I", header, 12, 40)      # literal list at 40
    struct.pack_into(">I", header, 16, 0)
    struct.pack_into(">I", header, 20, 0)
    strings_at = 40 + 4 + 12
    names = b"Makefile\0text/x-make\0"
    body = struct.pack(">I", 1) + struct.pack(">III", strings_at, strings_at + 9, 0x100 | 50)
    put(os.path.join(d, "mime.cache"), bytes(header) + body + names)


case("e13-cache-cs-literal", {}, ["Makefile", "makefile", "MAKEFILE"], build=_mk_e13)

# ---- E14 cache header validation --------------------------------------
def _mk_e14(root):
    d = os.path.join(root, "dh/mime")
    os.makedirs(d, exist_ok=True)
    put(os.path.join(d, "mime.cache"), b"\x00" * 39)
    put(os.path.join(d, "globs2"), "50:text/fallback:*.f\n")


case("e14-short-cache-fallback", {}, ["a.f"], build=_mk_e14)

def _mk_e15(root):
    import struct
    d = os.path.join(root, "dh/mime")
    os.makedirs(d, exist_ok=True)
    h = bytearray(40)
    struct.pack_into(">HH", h, 0, 2, 2)          # major 2: not loadable
    put(os.path.join(d, "mime.cache"), bytes(h))
    put(os.path.join(d, "globs2"), "50:text/fallback:*.f\n")


case("e15-bad-version-fallback", {}, ["a.f"], build=_mk_e15)

# ---- E16 trailing slash and empty name --------------------------------
case("e16-slash-basename", {"dh/mime/globs2": (
    "50:text/x-make:Makefile\n"
    "50:app/txt:*.txt\n")},
    ["Makefile/", "a.txt/", "", "/", "a//b.txt", "/usr/share/doc/x.txt"])

# ---- E17 non-ASCII suffix never matches -------------------------------
case("e17-nonascii-suffix", {"dh/mime/globs2": (
    "50:app/e:*.\u00e9\n"
    "50:app/t:*.t\n")},
    ["x.\u00e9", "x.t"])

# ---- E18 dir order in text mode ---------------------------------------
case("e18-dir-order-text", {
    "s1/mime/globs2": "50:t/first:*.q\n50:t/lit-a:Makefile\n",
    "s2/mime/globs2": "50:t/second:*.q\n50:t/lit-b:Makefile\n"},
    ["x.q", "Makefile"])

# ---- E19 same dir: cache wins over its own globs2 ----------------------
def _mk_e19(root):
    build_cache(("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                 "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
                 " <mime-type type=\"cc/in\"><glob pattern=\"*.cc\" weight=\"50\"/></mime-type>\n"
                 "</mime-info>\n"), "dh/mime")(root)
    put(os.path.join(root, "dh/mime/globs2"), "50:globs/lost:*.cc\n50:globs/ok:*.gg\n")


case("e19-cache-shadows-globs2", {}, ["a.cc", "a.gg"], build=_mk_e19)

# ---- E20 cs suffix + full glob -> two types ---------------------------
case("e20-cs-suffix-and-full", {"dh/mime/globs2": (
    "50:a/cs:*.y:cs\n"
    "50:a/full:x?y\n")},
    ["x.y"])

# ---- E21 same type twice: merged, still one answer --------------------
case("e21-dupe-merge", {"dh/mime/globs2": (
    "10:a/both:*.y\n"
    "90:a/both:*.y\n"
    "50:a/both:x?y\n")},
    ["x.y", "x.y"])

# ---- E22 two caches, same glob ----------------------------------------
_pkg_e = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"e/high\"><glob pattern=\"*.qq\" weight=\"50\"/></mime-type>\n"
          "</mime-info>\n")
_pkg_f = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"e/low\"><glob pattern=\"*.qq\" weight=\"50\"/></mime-type>\n"
          "</mime-info>\n")


def _mk_e22(root):
    build_cache(_pkg_e, "s1/mime")(root)
    build_cache(_pkg_f, "s2/mime")(root)


case("e22-two-caches-same-glob", {}, ["x.qq"], build=_mk_e22)

# ---- E23 fabricated caches: cs literal stops the folded search --------
def _mk_e23(root):
    import struct

    def cache_bytes(lit, mime, weight):
        header = bytearray(40)
        struct.pack_into(">HH", header, 0, 1, 2)
        struct.pack_into(">I", header, 12, 40)
        struct.pack_into(">I", header, 16, 0)
        struct.pack_into(">I", header, 20, 0)
        strings_at = 40 + 4 + 12
        body = struct.pack(">I", 1) + struct.pack(">III", strings_at, strings_at + len(lit) + 1, weight)
        return bytes(header) + body + lit + b"\0" + mime + b"\0"

    put(os.path.join(root, "s1/mime/mime.cache"), cache_bytes(b"makefile", b"stop/first", 0x100 | 50))
    put(os.path.join(root, "s2/mime/mime.cache"), cache_bytes(b"Makefile", b"stop/second", 50))


case("e23-cs-literal-stop", {}, ["MAKEFILE", "makefile"], build=_mk_e23)

# ---- E24 glob-deleteall via a real package ----------------------------
_pkg_g = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"dl/x\"><glob pattern=\"*.patch\" weight=\"50\"/></mime-type>\n"
          "</mime-info>\n")
_pkg_h = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"dl/x\"><glob-deleteall/><glob pattern=\"*.diff\" weight=\"50\"/></mime-type>\n"
          "</mime-info>\n")


def _mk_e24(root):
    put(os.path.join(root, "s1/mime/packages/p1.xml"), _pkg_g)
    put(os.path.join(root, "s2/mime/packages/p2.xml"), _pkg_h)
    for rel in ("s1/mime", "s2/mime"):
        subprocess.run(["update-mime-database", os.path.join(root, rel)], capture_output=True, check=True)
        shutil.rmtree(os.path.join(root, rel, "packages"), ignore_errors=True)


case("e24-deleteall-two-dirs", {}, ["a.patch", "a.diff"], build=_mk_e24)

def _mk_e25(root):
    put(os.path.join(root, "s2/mime/packages/p2.xml"), _pkg_h)
    subprocess.run(["update-mime-database", os.path.join(root, "s2/mime")], capture_output=True, check=True)


case("e25-deleteall-alone", {}, ["a.patch", "a.diff"], build=_mk_e25)

# ---- E26 full glob with a bracketed class, text vs cache --------------
case("e26-class-text", {"dh/mime/globs2": "50:src/c:*.[ch]\n"}, ["X.C", "x.c"])
_pkg_i = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<mime-info xmlns=\"http://www.freedesktop.org/standards/shared-mime-info\">\n"
          " <mime-type type=\"src/c\"><glob pattern=\"*.[ch]\" weight=\"50\"/></mime-type>\n"
          "</mime-info>\n")


def _mk_e26(root):
    build_cache(_pkg_i, "dh/mime")(root)


case("e26b-class-cache", {}, ["X.C", "x.c"], build=_mk_e26)

# ---- E27 a bare "*" glob in text mode ---------------------------------
case("e27-star-glob", {"dh/mime/globs2": "50:app/star:*\n"}, ["x"])

# ---- E28 cs suffix and uppercase name ---------------------------------
case("e28-cs-upper", {"dh/mime/globs2": "50:app/zip:*.zip:cs\n50:app/pdf:*.pdf\n"},
    ["FILE.ZIP", "file.zip", "REPORT.PDF"])

# ---- E30 invalid UTF-8 in a globs2 line --------------------------------
case("e30-invalid-utf8-line", {"dh/mime/globs2": b"50:text/bad:*.\xff\n50:text/ok:*.ok\n"},
     ["a.ok", "a.\xff"])

# ---- E31 a globs2 line longer than fgets' 255 byte buffer -------------
long_glob = "50:app/long:*." + "z" * 300 + "\n50:app/ok2:*.ok2\n"
case("e31-long-line", {"dh/mime/globs2": long_glob},
     ["a." + "z" * 300, "a.ok2"])

# ---- E32 a lowercase literal vs a mixed-case literal ------------------
case("e32-literal-case", {"dh/mime/globs2": "50:text/x-make:makefile\n50:text/x-mk:Makefile\n"},
     ["MAKEFILE", "Makefile", "makefile"])

def run(c):
    root = os.path.join(ROOT, c["id"])
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root, exist_ok=True)
    for rel, data in c["files"].items():
        put(os.path.join(root, rel), data)
    if c["build"]:
        c["build"](root)
    env = {"LC_ALL": "C", "HOME": os.path.join(root, c["home"]) if c["home"] else None}
    if c["data_home"] is not None:
        env["XDG_DATA_HOME"] = os.path.join(root, c["data_home"])
    if c["data_dirs"] is not None:
        env["XDG_DATA_DIRS"] = ":".join(os.path.join(root, d) if d else ""
                                        for d in c["data_dirs"].split(":"))
    else:
        env["XDG_DATA_DIRS"] = None
    full = {k: v for k, v in env.items() if v is not None}
    e = {"PATH": "/usr/bin:/bin"}
    e.update(full)
    out = subprocess.run([ORACLE] + c["names"], capture_output=True, text=True, env=e)
    if out.returncode != 0:
        raise SystemExit(f"{c['id']}: oracle rc={out.returncode} {out.stderr}")
    labels = [tuple(l.split("\t")) for l in out.stdout.splitlines()]
    args = [sys.executable, "-I", TOOL, "--json"]
    if c["data_home"] is None:
        args.append("--data-home-unset")
    else:
        args += ["--data-home", full["XDG_DATA_HOME"]]
    if c["data_dirs"] is None:
        args.append("--data-dirs-unset")
    else:
        args += ["--data-dirs", full["XDG_DATA_DIRS"]]
    args += ["--home", full["HOME"]]
    args += c["names"]
    t = subprocess.run(args, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    if t.returncode == 3:
        return labels, {"mode": "refused", "results": [{"type": "UNSUPPORTED", "uncertain": "-"}] * len(c["names"])}
    if t.returncode != 0:
        raise SystemExit(f"{c['id']}: tool rc={t.returncode} {t.stdout} {t.stderr}")
    res = json.loads(t.stdout)
    return labels, res


def main():
    rows = []
    bad = 0
    for c in CASES:
        labels, res = run(c)
        got = [(r["type"], str(r["uncertain"])) for r in res["results"]]
        for name, lab, g in zip(c["names"], labels, got):
            agree = lab == g
            bad += 0 if agree else 1
            rows.append((c["id"], res["mode"], name, lab[0], lab[1], g[0], g[1],
                         "OK" if agree else "DIFF"))
    w = max(len(r[0]) for r in rows)
    print(f"{'case':<{w}} {'mode':<5} {'name':<14} {'oracle':<16} {'u':<1} {'tool':<16} {'u'} ")
    for r in rows:
        print(f"{r[0]:<{w}} {r[1]:<5} {r[2]:<14} {r[3]:<16} {r[4]:<1} {r[5]:<16} {r[6]:<1} {r[7]}")
    print(f"\nROWS={len(rows)} DIFFS={bad}")
    json.dump([[list(r) for r in rows]], open(os.path.join(S, "probe-rows.json"), "w"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
