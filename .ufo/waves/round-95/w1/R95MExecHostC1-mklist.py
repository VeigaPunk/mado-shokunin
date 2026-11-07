#!/usr/bin/env python3
"""R95MExecHostC1: build the frozen round-95 host file list (deterministic).

Reads only /usr (no home paths). Emits one absolute path per line, sorted, deduped,
to the path given as argv[1] (default: the frozen controls path). Prints per-bucket
counts, the union size and the sha256 of the emitted file.

Determinism: one os.walk('/usr', followlinks=False) pass collects every readable
regular file (path, size); /usr/lib64 (a symlink to lib) is not descended and adds
nothing beyond /usr/lib. Every bucket is a sorted (Python str codepoint order,
locale-free) list truncated to a fixed quota (head -N, or all for quota 10**9);
the union is sorted and deduped. No time, no randomness, no locale, no network.

Bucket plan (variety first: the oracle gives 64 distinct data-only types on the
union, 73 with names): ELF exec/sharedlib, shebang scripts (sh/python/perl/ruby/
lua/groovy/modelica/matlab/csh/bat/qml), gz|xz|zst|bz2|zip|jar, icons+pixmaps
(png/svg/xpm/ico/cur), fonts (ttf/otf/ttc/woff/woff2/type1 pfa+pfb), desktop,
xml/html/xhtml/gtk-builder/dtd/qml, json, docs+pdf+postscript, zoneinfo, terminfo,
mime DB, python sources+pyc, perl, empty files, sounds (ogg/wav/mp3), vim, i18n,
X11/drirc/vulkan, glib schemas, certs, java, gettext .mo, webp/bmp/gif/jpeg/tga/
pcx/netpbm ppm+pgm+pnm, static .a archives, ICC profiles, LibreOffice ODF
templates, wasm, efi (PE), glb (gltf-binary), hdr (radiance), exr, rtf-bat,
resolved symlink targets.
"""
import hashlib
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else ("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt")

ALL = 10**9
QUOTA = {
    "elf-exec": 350,        # ELF regular files directly in /usr/bin
    "elf-shlib": 350,       # /usr/lib/**, basename contains '.so'
    "shebang": 250,         # /usr/bin regular files whose first two bytes are '#!'
    "gz": 350,              # /usr/**, suffix .gz
    "xz": 30,               # suffix .xz
    "zst": 30,              # suffix .zst
    "bz2": 30,              # suffix .bz2
    "zip": 60,              # suffix .zip
    "jar": ALL,             # suffix .jar
    "icons": 350,           # /usr/share/icons, /usr/share/pixmaps
    "fonts": 200,           # /usr/share/fonts
    "desktop": ALL,         # /usr/share/applications/*.desktop
    "xml": 250,             # /usr/share/**, suffix .xml
    "html-json": 250,       # /usr/share/**, suffix .html or .json
    "doc": 150,             # /usr/share/doc
    "zoneinfo": 120,        # /usr/share/zoneinfo
    "terminfo": 120,        # /usr/share/terminfo
    "mimedb": ALL,          # /usr/share/mime/packages/*.xml
    "mimedb-fixed": 3,      # /usr/share/mime/mime.cache, generic-icons, types
    "pyscripts": 200,       # /usr/lib/python3.*/**, suffix .py
    "perl": 100,            # /usr/share/perl5 + /usr/lib/perl5, suffix .pm|.pod
    "empty": 60,            # /usr/** regular files of size 0
    "sounds": ALL,          # /usr/share/sounds
    "vim": ALL,             # /usr/share/vim
    "i18n": 80,             # /usr/share/i18n
    "x11-drirc": 60,        # /usr/share/X11, /usr/share/drirc.d, /usr/share/vulkan
    "glib2": 60,            # /usr/share/glib-2.0
    "certs": ALL,           # /usr/share/ca-certificates
    "java": ALL,            # /usr/share/java
    "symlink-targets": 40,  # realpath of /usr/bin symlinks resolving to regular readable files
    "gettext-mo": 60,       # /usr/share/locale/**/*.mo
    "pdf": 40,              # /usr/share/**, suffix .pdf
    "postscript": 40,       # suffix .ps/.eps
    "jpeg": 40,             # suffix .jpg/.jpeg
    "gif": 40,              # suffix .gif
    "webp": ALL,            # suffix .webp
    "audio": 40,            # suffix ogg|oga|wav|flac|mp3|opus|mid (mp3 kept by the mp3 bucket too)
    "kbd-consolefonts": 40,  # /usr/share/kbd/consolefonts
    "ar-static": 40,        # /usr/lib/*.a
    "icc": ALL,             # /usr/share/color/**
    "xml-dtd": ALL,         # /usr/share/xml/**
    "ttc": ALL,             # /usr/share/fonts/*.ttc
    "woff": 30,             # suffix .woff
    "lo-templates": 60,     # /usr/lib/libreoffice/share/template/**
    "pyc": 20,              # /usr/lib/python3.*/**, suffix .pyc
    "ico": ALL,             # suffix .ico
    "elisp": ALL,           # /usr/share/emacs/**/*.el
    "wasm": ALL,            # suffix .wasm
    "bmp": ALL,             # suffix .bmp
    "mp3": ALL,             # suffix .mp3
    "lua": ALL,             # suffix .lua
    "type1-fonts": ALL,     # suffix .pfa/.pfb
    "netpbm": ALL,          # suffix .ppm/.pgm/.pbm/.pnm
    "pcx": ALL,             # suffix .pcx
    "tga": ALL,             # suffix .tga
    "bat": ALL,             # suffix .bat
    "qml": 30,              # suffix .qml
    "hdr": ALL,             # suffix .hdr
    "exr": ALL,             # suffix .exr
    "cur": ALL,             # suffix .cur
    "glb": ALL,             # suffix .glb
    "efi": ALL,             # suffix .efi
}


def collect(top):
    """All readable regular files under top as (path, size), sorted."""
    out = []
    for root, dirs, files in os.walk(top, followlinks=False):
        dirs.sort()
        for f in files:
            p = os.path.join(root, f)
            try:
                st = os.lstat(p)
            except OSError:
                continue
            if not os.path.isfile(p):
                continue
            if not os.access(p, os.R_OK):
                continue
            out.append((p, st.st_size))
    out.sort()
    return out


def head(paths, n):
    return sorted(paths)[:n]


ONCE = collect("/usr")
BY_PATH = dict(ONCE)
paths = [p for p, _ in ONCE]
starts = {d: [p for p in paths if p.startswith(d + "/")] for d in
          ("/usr/bin", "/usr/lib", "/usr/share/locale", "/usr/share/doc",
           "/usr/share/icons", "/usr/share/pixmaps", "/usr/share/fonts", "/usr/share/applications",
           "/usr/share/zoneinfo", "/usr/share/terminfo", "/usr/share/mime", "/usr/share/perl5",
           "/usr/lib/perl5", "/usr/share/sounds", "/usr/share/vim", "/usr/share/i18n",
           "/usr/share/X11", "/usr/share/drirc.d", "/usr/share/vulkan", "/usr/share/glib-2.0",
           "/usr/share/ca-certificates", "/usr/share/java", "/usr/share/kbd/consolefonts",
           "/usr/share/color", "/usr/share/xml", "/usr/lib/libreoffice/share/template",
           "/usr/share/emacs")}

buckets = {k: [] for k in QUOTA}

buckets["elf-exec"] = head([p for p in starts["/usr/bin"] if open(p, "rb").read(4) == b"\x7fELF"], QUOTA["elf-exec"])
buckets["shebang"] = head([p for p in starts["/usr/bin"] if open(p, "rb").read(2) == b"#!"], QUOTA["shebang"])
buckets["elf-shlib"] = head([p for p in starts["/usr/lib"] if ".so" in os.path.basename(p)], QUOTA["elf-shlib"])

suf = lambda exts: [p for p in paths if p.endswith(exts)]  # noqa: E731
buckets["gz"] = head(suf(".gz"), QUOTA["gz"])
buckets["xz"] = head(suf(".xz"), QUOTA["xz"])
buckets["zst"] = head(suf(".zst"), QUOTA["zst"])
buckets["bz2"] = head(suf(".bz2"), QUOTA["bz2"])
buckets["zip"] = head(suf(".zip"), QUOTA["zip"])
buckets["jar"] = head(suf(".jar"), QUOTA["jar"])

buckets["icons"] = head(starts["/usr/share/icons"] + starts["/usr/share/pixmaps"], QUOTA["icons"])
buckets["fonts"] = head(starts["/usr/share/fonts"], QUOTA["fonts"])
buckets["desktop"] = head([p for p in starts["/usr/share/applications"] if p.endswith(".desktop")], QUOTA["desktop"])
buckets["xml"] = head(suf(".xml"), QUOTA["xml"])
buckets["html-json"] = head(suf((".html", ".json")), QUOTA["html-json"])
buckets["doc"] = head(starts["/usr/share/doc"], QUOTA["doc"])
buckets["zoneinfo"] = head(starts["/usr/share/zoneinfo"], QUOTA["zoneinfo"])
buckets["terminfo"] = head(starts["/usr/share/terminfo"], QUOTA["terminfo"])
buckets["mimedb"] = head([p for p in starts["/usr/share/mime"] if p.startswith("/usr/share/mime/packages/") and p.endswith(".xml")], QUOTA["mimedb"])
buckets["mimedb-fixed"] = head([p for p in (("/usr/share/mime/mime.cache", "/usr/share/mime/generic-icons", "/usr/share/mime/types")) if p in BY_PATH], QUOTA["mimedb-fixed"])
buckets["pyscripts"] = head([p for p in paths if p.startswith("/usr/lib/python3.") and p.endswith(".py")], QUOTA["pyscripts"])
buckets["perl"] = head([p for p in starts["/usr/share/perl5"] + starts["/usr/lib/perl5"] if p.endswith((".pm", ".pod"))], QUOTA["perl"])
buckets["empty"] = head([p for p, sz in ONCE if sz == 0], QUOTA["empty"])
buckets["sounds"] = head(starts["/usr/share/sounds"], QUOTA["sounds"])
buckets["vim"] = head(starts["/usr/share/vim"], QUOTA["vim"])
buckets["i18n"] = head(starts["/usr/share/i18n"], QUOTA["i18n"])
buckets["x11-drirc"] = head(starts["/usr/share/X11"] + starts["/usr/share/drirc.d"] + starts["/usr/share/vulkan"], QUOTA["x11-drirc"])
buckets["glib2"] = head(starts["/usr/share/glib-2.0"], QUOTA["glib2"])
buckets["certs"] = head(starts["/usr/share/ca-certificates"], QUOTA["certs"])
buckets["java"] = head(starts["/usr/share/java"], QUOTA["java"])

targets = []
for name in sorted(os.listdir("/usr/bin")):
    p = os.path.join("/usr/bin", name)
    if os.path.islink(p):
        rp = os.path.realpath(p)
        if rp in BY_PATH:
            targets.append(rp)
buckets["symlink-targets"] = head(targets, QUOTA["symlink-targets"])

buckets["gettext-mo"] = head([p for p in starts["/usr/share/locale"] if p.endswith(".mo")], QUOTA["gettext-mo"])
buckets["pdf"] = head(suf(".pdf"), QUOTA["pdf"])
buckets["postscript"] = head(suf((".ps", ".eps")), QUOTA["postscript"])
buckets["jpeg"] = head(suf((".jpg", ".jpeg")), QUOTA["jpeg"])
buckets["gif"] = head(suf(".gif"), QUOTA["gif"])
buckets["webp"] = head(suf(".webp"), QUOTA["webp"])
buckets["audio"] = head(suf((".ogg", ".oga", ".wav", ".flac", ".opus", ".mid")), QUOTA["audio"])
buckets["kbd-consolefonts"] = head(starts["/usr/share/kbd/consolefonts"], QUOTA["kbd-consolefonts"])
buckets["ar-static"] = head([p for p in starts["/usr/lib"] if p.startswith("/usr/lib/") and "/" not in p[len("/usr/lib/"):] and p.endswith(".a")], QUOTA["ar-static"])
buckets["icc"] = head(starts["/usr/share/color"], QUOTA["icc"])
buckets["xml-dtd"] = head(starts["/usr/share/xml"], QUOTA["xml-dtd"])
buckets["ttc"] = head(suf(".ttc"), QUOTA["ttc"])
buckets["woff"] = head(suf(".woff"), QUOTA["woff"])
buckets["lo-templates"] = head(starts["/usr/lib/libreoffice/share/template"], QUOTA["lo-templates"])
buckets["pyc"] = head([p for p in paths if p.startswith("/usr/lib/python3.") and p.endswith(".pyc")], QUOTA["pyc"])
buckets["ico"] = head(suf(".ico"), QUOTA["ico"])
buckets["elisp"] = head([p for p in starts["/usr/share/emacs"] if p.endswith(".el")], QUOTA["elisp"])
buckets["wasm"] = head(suf(".wasm"), QUOTA["wasm"])
buckets["bmp"] = head(suf(".bmp"), QUOTA["bmp"])
buckets["mp3"] = head(suf(".mp3"), QUOTA["mp3"])
buckets["lua"] = head(suf(".lua"), QUOTA["lua"])
buckets["type1-fonts"] = head(suf((".pfa", ".pfb")), QUOTA["type1-fonts"])
buckets["netpbm"] = head(suf((".ppm", ".pgm", ".pbm", ".pnm")), QUOTA["netpbm"])
buckets["pcx"] = head(suf(".pcx"), QUOTA["pcx"])
buckets["tga"] = head(suf(".tga"), QUOTA["tga"])
buckets["bat"] = head(suf(".bat"), QUOTA["bat"])
buckets["qml"] = head(suf(".qml"), QUOTA["qml"])
buckets["hdr"] = head(suf(".hdr"), QUOTA["hdr"])
buckets["exr"] = head(suf(".exr"), QUOTA["exr"])
buckets["cur"] = head(suf(".cur"), QUOTA["cur"])
buckets["glb"] = head(suf(".glb"), QUOTA["glb"])
buckets["efi"] = head(suf(".efi"), QUOTA["efi"])

union = set()
for k in QUOTA:
    union.update(buckets[k])
union.discard("")
lines = sorted(union)
with open(OUT, "w") as fh:
    fh.write("".join(l + "\n" for l in lines))
h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print("buckets:")
for k in QUOTA:
    print(f"  {k}={len(buckets[k])}")
print(f"union={len(lines)}")
print(f"sha256={h}")
print(f"out={OUT}")
