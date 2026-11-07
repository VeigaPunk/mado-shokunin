#!/usr/bin/env python3
"""R96MScribeEntry rule probes: text-mode magic rules via the round-95 oracle.

Read-only: builds fixture roots in this scratch dir, runs the oracle once per
fixture with env -i LC_ALL=C HOME=... XDG_DATA_HOME=... XDG_DATA_DIRS=..., prints one
line per (probe, input).  Oracle sha256 99df35f8...124a (round-95 control).
"""
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(S, "oracle")
FX = os.path.join(S, "fx")


def hdr(prio, typ):
    return b"[" + str(prio).encode() + b":" + typ + b"]\n"


def ml(off, value, indent=0, mask=None, word=None, rng=None, suffix=b""):
    out = (str(indent).encode() if indent else b"") + b">" + str(off).encode() + b"="
    out += bytes([(len(value) >> 8) & 0xFF, len(value) & 0xFF]) + value
    if mask is not None:
        out += b"&" + mask
    if word is not None:
        out += b"~" + str(word).encode()
    if rng is not None:
        out += b"+" + str(rng).encode()
    return out + suffix + b"\n"


MAGIC = b"MIME-Magic\x00\n"


def mkcase(cid, magic, globs2=None, magic2=None, cache=False):
    root = os.path.join(FX, cid)
    for d in ("h", "dh/mime", "d1/mime", "d2/mime"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    if magic is not None:
        open(os.path.join(root, "dh/mime/magic"), "wb").write(magic)
    if magic2 is not None:
        open(os.path.join(root, "d1/mime/magic"), "wb").write(magic2)
    if globs2 is not None:
        open(os.path.join(root, "dh/mime/globs2"), "wb").write(globs2)
    if cache:
        open(os.path.join(root, "dh/mime/mime.cache"), "wb").write(b"\x00" * 40)
    return root


def run(root, pairs):
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)
    argv = [ORACLE]
    for i, (name, data) in enumerate(pairs):
        p = os.path.join(data_dir, "d%02d" % i)
        open(p, "wb").write(data)
        argv.append("0" if name is None else "=" + name)
        argv.append(p)
    env = {
        "LC_ALL": "C",
        "HOME": os.path.join(root, "h"),
        "XDG_DATA_HOME": os.path.join(root, "dh"),
        "XDG_DATA_DIRS": os.path.join(root, "d1") + ":" + os.path.join(root, "d2"),
    }
    r = subprocess.run(argv, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        return ["<oracle rc=%d %s>" % (r.returncode, r.stderr.strip())] * len(pairs)
    return r.stdout.rstrip("\n").split("\n")


CASES = []


def case(cid, note, magic, pairs, globs2=None, magic2=None, cache=False):
    CASES.append((cid, note, magic, globs2, magic2, pairs, cache))


HI = b"HI"
# --- the 12-byte gate
case("A1-gate-ok", "well-formed magic answers", MAGIC + hdr(90, b"application/x-a") + ml(0, HI),
     [(None, HI)])
case("A2-gate-bad-nl", "header ends \\0\\r not \\0\\n", b"MIME-Magic\x00\r" + hdr(90, b"application/x-a") + ml(0, HI),
     [(None, HI)])
case("A3-gate-short", "11-byte header", b"MIME-Magic\x00" + hdr(90, b"application/x-a") + ml(0, HI),
     [(None, HI)])
case("A4-gate-prefix", "header + trailing 'X' inside the 12 bytes", b"MIME-Magic\x00\nX" + hdr(90, b"application/x-a") + ml(0, HI),
     [(None, HI)])
# --- section parse errors: whole section dropped
case("B1-bad-line-mid", "bad line mid-section; good section after",
     MAGIC + hdr(90, b"application/x-bad") + ml(0, HI) + b"X\n" + ml(0, b"NO")
     + hdr(50, b"application/x-good") + ml(0, HI),
     [(None, HI)])
case("B2-bad-header", "priority is not a number", MAGIC + hdr(b"x", b"application/x-bad") + ml(0, HI)
     + hdr(50, b"application/x-good") + ml(0, HI),
     [(None, HI)])
case("B3-bad-char-after-value", "trailing '!' where newline expected",
     MAGIC + hdr(90, b"application/x-bad") + ml(0, HI, suffix=b"!") + hdr(50, b"application/x-good") + ml(0, HI),
     [(None, HI)])
case("B4-type-unterminated", "no ']' on the header line", MAGIC + b"[90:application/x-bad\n" + ml(0, HI)
     + hdr(50, b"application/x-good") + ml(0, HI),
     [(None, HI)])
case("B5-extra-chars-two-sections", "second section alone bad -> dropped; third good",
     MAGIC + hdr(90, b"application/x-bad") + ml(0, b"NO") + b"!\n"
     + hdr(50, b"application/x-mid") + ml(0, b"NO")
     + hdr(60, b"application/x-good") + ml(0, HI),
     [(None, HI)])
# --- priority
case("C1-prio-0", "priority 0 answers in text mode", MAGIC + hdr(0, b"application/x-zero") + ml(0, HI),
     [(None, HI)])
case("C2-prio-order", "30 listed before 90, both match", MAGIC + hdr(30, b"application/x-low") + ml(0, HI)
     + hdr(90, b"application/x-high") + ml(0, HI),
     [(None, HI)])
case("C3-prio-tie", "equal priorities keep file order", MAGIC + hdr(50, b"application/x-first") + ml(0, HI)
     + hdr(50, b"application/x-second") + ml(0, HI),
     [(None, HI)])
case("C4-prio-tie-dirs", "equal priorities across dirs: XDG_DATA_HOME before XDG_DATA_DIRS",
     MAGIC + hdr(50, b"application/x-dh") + ml(0, HI), [(None, HI)],
     magic2=hdr(50, b"application/x-d1") + ml(0, HI))
case("C5-prio-overflow", "priority > INT_MAX is a parse error", MAGIC + hdr(b"9999999999", b"application/x-big")
     + ml(0, HI) + hdr(50, b"application/x-good") + ml(0, HI),
     [(None, HI)])
case("C6-indent-overflow", "indent > INT_MAX is a parse error", MAGIC + hdr(90, b"application/x-bad")
     + ml(0, HI, indent=9999999999, suffix=b"") + hdr(50, b"application/x-good") + ml(0, HI),
     [(None, HI)])
# --- matchlet structure
case("D1-range-start", "offset 2, range 3, hit at 2", MAGIC + hdr(90, b"application/x-range") + ml(2, b"RGB", rng=3),
     [(None, b"..RGB")])
case("D2-range-late", "hit at offset 3 of the range", MAGIC + hdr(90, b"application/x-range") + ml(2, b"RG", rng=3),
     [(None, b"...RG")])
case("D3-range-none", "no hit inside the range", MAGIC + hdr(90, b"application/x-range") + ml(2, b"RG", rng=3),
     [(None, b"...RX")])
case("D4-range-zero", "+0 never enters the loop", MAGIC + hdr(90, b"application/x-zero-range") + ml(0, HI, rng=0),
     [(None, HI)])
case("D5-short-value", "value longer than data is FALSE, not continue", MAGIC + hdr(90, b"application/x-long")
     + ml(0, b"ABCD"), [(None, b"ABC")])
case("D6-short-later-offset", "same value 200 bytes in on a short buffer", MAGIC + hdr(90, b"application/x-far")
     + ml(200, HI), [(None, HI)])
case("D7-mask", "masked compare", MAGIC + hdr(90, b"application/x-mask") + ml(0, b"\x10\x00", mask=b"\xf0\x00"),
     [(None, b"\x1f\x99")])
case("D8-mask-fail", "masked compare fails on the low nibble", MAGIC + hdr(90, b"application/x-mask")
     + ml(0, b"\x10\x00", mask=b"\xf0\x00"), [(None, b"\x2f\x99")])
case("D9-word2-swapped", "~2 swaps the value at parse (LE)", MAGIC + hdr(90, b"application/x-w2")
     + ml(0, b"\x00\x01\x00\x02", word=2), [(None, b"\x01\x00\x02\x00"), (None, b"\x00\x01\x00\x02")])
case("D10-word4-swapped", "~4 swaps each 4-byte group", MAGIC + hdr(90, b"application/x-w4")
     + ml(0, b"\x00\x00\x00\x01", word=4), [(None, b"\x01\x00\x00\x00"), (None, b"\x00\x00\x00\x01")])
case("D11-word0", "~0 is accepted and behaves as 1", MAGIC + hdr(90, b"application/x-w0")
     + ml(0, HI, word=0), [(None, HI)])
case("D12-word3", "~3 is a parse error -> section dropped", MAGIC + hdr(90, b"application/x-w3")
     + ml(0, HI, word=3) + hdr(50, b"application/x-good") + ml(0, HI), [(None, HI)])
case("D13-word-len-mismatch", "3 bytes with ~2 -> parse error", MAGIC + hdr(90, b"application/x-w2bad")
     + ml(0, b"ABC", word=2) + hdr(50, b"application/x-good") + ml(0, HI), [(None, HI)])
case("D14-word-empty", "bare '~' -> word_size -1 -> parse error", MAGIC + hdr(90, b"application/x-wnone")
     + b">0=\x00\x02HI" + b"~\n" + hdr(50, b"application/x-good") + ml(0, HI), [(None, HI)])
case("D15-zero-length-value", "zero-length value matches any non-empty data", MAGIC + hdr(90, b"application/x-emptyv")
     + ml(0, b""), [(None, b"Z")])
# --- nesting
case("E1-nest-hit", "child holds", MAGIC + hdr(90, b"application/x-nest") + ml(0, b"NE") + ml(4, b"Y", indent=1),
     [(None, b"NE..Y")])
case("E2-nest-miss", "child fails -> section fails", MAGIC + hdr(90, b"application/x-nest") + ml(0, b"NE")
     + ml(4, b"Y", indent=1), [(None, b"NE..Z")])
case("E3-nest-skip-child", "parent fails, child skipped, next top-level tested",
     MAGIC + hdr(90, b"application/x-two") + ml(0, b"XX") + ml(2, b"Y", indent=1) + ml(0, b"ZZ"),
     [(None, b"ZZ"), (None, b"XX..Y")])
case("E4-nest-two-children", "either child holds", MAGIC + hdr(90, b"application/x-or")
     + ml(0, b"NE") + ml(3, b"A", indent=1) + ml(3, b"B", indent=1), [(None, b"NE.B"), (None, b"NE.C")])
case("E5-nest-deep", "indent 2 chain", MAGIC + hdr(90, b"application/x-deep")
     + ml(0, b"A") + ml(1, b"B", indent=1) + ml(2, b"C", indent=2),
     [(None, b"ABC"), (None, b"ABX")])
case("E6-indent-jump", "indent 0 then indent 2: no child at indent 1, section never matches",
     MAGIC + hdr(90, b"application/x-jump") + ml(0, b"A") + ml(1, b"B", indent=2),
     [(None, b"AB")])
case("E7-first-child", "a section whose first matchlet is at indent 1 never matches",
     MAGIC + hdr(90, b"application/x-orphan") + ml(0, b"A", indent=1),
     [(None, b"A")])
case("B6-type-nul", "NUL before ']' in the header line", MAGIC + b"[90:application/x-bad\x00]\n"
     + ml(0, HI) + hdr(50, b"application/x-good") + ml(0, HI), [(None, HI)])
# --- header/type text
case("F1-empty-type", "empty type accepted", MAGIC + hdr(90, b"") + ml(0, HI), [(None, HI)])
case("F2-type-space", "type keeps a space and a slash", MAGIC + hdr(90, b"application/x a") + ml(0, HI),
     [(None, HI)])
# --- mode
case("G1-invalid-cache", "40 zero bytes as mime.cache is invalid -> text mode", MAGIC + hdr(90, b"application/x-a")
     + ml(0, HI), [(None, HI)], cache=True)
case("D16-exact-length", "i + value_length == len still matches", MAGIC + hdr(90, b"application/x-exact")
     + ml(0, HI), [(None, HI)])
case("D17-blank-line", "a bare newline inside a section is skipped", MAGIC + hdr(90, b"application/x-two")
     + ml(0, b"XX") + b"\n" + ml(0, HI), [(None, HI)])
case("D18-indent-non-gt", "indent digits not followed by '>'", MAGIC + hdr(90, b"application/x-bad")
     + b"1x\n" + hdr(50, b"application/x-good") + ml(0, HI), [(None, HI)])
case("D19-vt", "VT (0x0b) in the first 128 bytes is binary", MAGIC, [(None, b"ab\x0bcd")])
case("F3-junk-after-bracket", "bytes after ']' on the header line are ignored",
     MAGIC + b"[90:application/x-a]junk\n" + ml(0, HI), [(None, HI)])
case("G4-eof-no-newline", "EOF after a complete value, no final newline: section inert",
     MAGIC + hdr(90, b"application/x-eof2") + b">0=\x00\x02AB", [(None, b"AB")])
case("G2-no-magic", "no magic file at all -> fallback", MAGIC, [(None, HI)])
case("G3-eof-in-value", "EOF inside a value: section inert", magic=MAGIC + hdr(90, b"application/x-eof") + b">0=\x00\x05AB",
     pairs=[(None, b"AB")])
# --- name step x magic (text mode)
G2TYPES = b"50:image/png:*.two\n50:image/apng:*.two\n"
case("H1-name-one", "one name type short-circuits the bytes",
     MAGIC + hdr(90, b"application/x-hi") + ml(0, HI), [("x.one", b"\x01\x02")],
     globs2=b"50:text/x-one:*.one\n")
case("H2-name-none", "no name type -> the magic answer", MAGIC + hdr(90, b"application/x-hi") + ml(0, HI),
     [(None, HI), ("zz.nomatch", HI)])
case("H3-name-two-hi", "two name types, magic 90 -> the sniffed type", MAGIC + hdr(90, b"application/x-hi")
     + ml(0, HI), [("x.two", HI)], globs2=G2TYPES)
case("H4-name-two-low", "two name types, magic 50 -> first name type, uncertain", MAGIC + hdr(50, b"application/x-lo")
     + ml(0, HI), [("x.two", HI)], globs2=G2TYPES)
case("H5-name-two-sub", "two name types, sniffed text/plain -> first subclass name type",
     MAGIC + hdr(50, b"text/plain") + ml(0, HI), [("x.two", HI)],
     globs2=b"50:text/x-a:*.two\n50:text/x-b:*.two\n")
case("H6-desktop-name", "sniffed desktop with any name -> text/plain", MAGIC + hdr(90, b"application/x-desktop")
     + ml(0, b"[Desktop Entry]"), [(None, b"[Desktop Entry]"), ("zz.nomatch", b"[Desktop Entry]")])
case("H7-dir", "trailing slash before the bytes", MAGIC, [("d/", HI)])
case("H8-empty-data", "len 0 answers zerosize before the magic", MAGIC + hdr(90, b"application/x-hi") + ml(0, b""),
     [(None, b""), ("x.one", b"")], globs2=b"50:text/x-one:*.one\n")
case("H9-prio0-name-one", "priority 0 magic vs one name type: the name wins", MAGIC + hdr(0, b"application/x-zero")
     + ml(0, HI), [("x.one", HI)], globs2=b"50:text/x-one:*.one\n")


def main():
    if os.path.isdir(FX):
        shutil.rmtree(FX)
    os.makedirs(FX)
    out = []
    for cid, note, magic, globs2, magic2, pairs, cache in CASES:
        root = mkcase(cid, magic, globs2=globs2, magic2=magic2, cache=cache)
        lines = run(root, pairs)
        for (name, data), ans in zip(pairs, lines):
            out.append("%-28s %-58s name=%-12s data=%s -> %s" % (
                cid, note, "-" if name is None else repr(name), data.hex(), ans))
    print("\n".join(out))
    print("\nprobes=%d inputs=%d" % (len(CASES), len(out)))


if __name__ == "__main__":
    sys.exit(main())
