#!/usr/bin/env python3
"""Mechanical quote extraction for the round-96 registry rows and the entry.

Reads the fetched bytes (round-95 fetch copies whose digests equal the
round-96 sources receipt) and prints, per row: the located line, the
whitespace-collapsed text, its word count and the file digest.  Nothing is
hand-typed into the quote cells by the author.
"""
import hashlib
import os
import re

FETCH = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/fetch"

# (id, file, first_line, last_line, anchor_line)
ROWS = [
    ("M01", "xdgmimemagic.c", 812, 812, 812),
    ("M02", "xdgmimemagic.c", 814, 814, 814),
    ("M03", "xdgmimemagic.c", 807, 810, 809),
    ("M04", "xdgmimemagic.c", 244, 245, 244),
    ("M05", "xdgmimemagic.c", 247, 247, 247),
    ("M06", "xdgmimemagic.c", 256, 257, 256),
    ("M07", "xdgmimemagic.c", 267, 268, 267),
    ("M08", "xdgmimemagic.c", 269, 273, 269),
    ("M09", "xdgmimemagic.c", 204, 208, 204),
    ("M10", "xdgmimemagic.c", 211, 212, 211),
    ("M11", "xdgmimemagic.c", 220, 220, 220),
    ("M12", "xdgmimemagic.c", 168, 168, 168),
    ("M13", "xdgmimemagic.c", 292, 293, 292),
    ("M14", "xdgmimemagic.c", 93, 94, 93),
    ("M15", "xdgmimemagic.c", 98, 99, 98),
    ("M16", "xdgmimemagic.c", 350, 350, 350),
    ("M17", "xdgmimemagic.c", 367, 371, 367),
    ("M18", "xdgmimemagic.c", 382, 382, 382),
    ("M19", "xdgmimemagic.c", 410, 411, 411),
    ("M20", "xdgmimemagic.c", 420, 421, 420),
    ("M21", "xdgmimemagic.c", 440, 443, 440),
    ("M22", "xdgmimemagic.c", 476, 480, 476),
    ("M23", "xdgmimemagic.c", 486, 486, 486),
    ("M24", "xdgmimemagic.c", 451, 453, 453),
    ("M25", "xdgmimemagic.c", 468, 471, 471),
    ("M26", "xdgmimemagic.c", 501, 502, 501),
    ("M27", "xdgmimemagic.c", 777, 778, 777),
    ("M28", "xdgmimemagic.c", 780, 781, 780),
    ("M29", "xdgmimemagic.c", 608, 608, 608),
    ("M30", "xdgmimemagic.c", 618, 618, 618),
    ("M31", "xdgmimemagic.c", 666, 673, 668),
    ("M32", "xdgmimemagic.c", 685, 692, 685),
    ("M33", "xdgmimemagic.c", 521, 521, 521),
    ("M34", "xdgmimemagic.c", 525, 526, 525),
    ("M35", "xdgmimemagic.c", 532, 533, 532),
    ("M36", "xdgmimemagic.c", 542, 544, 544),
    ("M37", "xdgmimemagic.c", 551, 552, 551),
    ("M38", "xdgmimemagic.c", 563, 563, 563),
    ("M39", "xdgmimemagic.c", 567, 575, 571),
    ("M40", "xdgmimemagic.c", 578, 582, 582),
    ("M41", "xdgmimemagic.c", 714, 714, 714),
    ("M42", "xdgmimemagic.c", 645, 648, 648),
    ("X01", "xdgmime.c", 530, 535, 532),
    ("X02", "xdgmime.c", 535, 535, 535),
    ("X03", "xdgmime.c", 523, 527, 523),
    ("X04", "xdgmime.c", 540, 540, 540),
    ("X05", "xdgmime.c", 226, 231, 231),
    ("X06", "xdgmime.c", 255, 255, 255),
    ("X07", "xdgmime.c", 184, 184, 184),
    ("X08", "xdgmime.c", 648, 648, 648),
    ("X09", "xdgmime.c", 830, 831, 830),
    ("X10", "xdgmime.c", 833, 834, 833),
    ("X11", "xdgmime.c", 841, 842, 841),
    ("X12", "xdgmime.c", 847, 848, 847),
    ("X13", "xdgmime.c", 851, 852, 851),
    ("X14", "xdgmime.c", 861, 861, 861),
    ("G01", "gcontenttype-fdo.c", 597, 598, 597),
    ("G02", "gcontenttype-fdo.c", 607, 607, 607),
    ("G03", "gcontenttype-fdo.c", 614, 614, 614),
    ("G04", "gcontenttype-fdo.c", 622, 622, 622),
    ("G05", "gcontenttype-fdo.c", 624, 624, 624),
    ("G06", "gcontenttype-fdo.c", 625, 625, 625),
    ("G07", "gcontenttype-fdo.c", 636, 638, 637),
    ("G08", "gcontenttype-fdo.c", 641, 641, 641),
    ("G09", "gcontenttype-fdo.c", 654, 654, 654),
    ("G10", "gcontenttype-fdo.c", 663, 663, 663),
    ("G11", "gcontenttype-fdo.c", 680, 680, 680),
    ("G12", "gcontenttype-fdo.c", 682, 682, 682),
    ("G13", "gcontenttype-fdo.c", 589, 589, 589),
    ("I01", "xdgmimeint.c", 185, 186, 185),
    ("I02", "xdgmimeint.c", 189, 189, 189),
    ("P01", "smi2-s02.html", 387, 387, 387),
    ("P02", "smi2-s02.html", 391, 391, 391),
    ("P03", "smi2-s02.html", 394, 395, 394),
    ("P04", "smi2-s02.html", 403, 403, 403),
    ("P05", "smi2-s02.html", 405, 405, 405),
    ("P06", "smi2-s02.html", 415, 415, 415),
    ("P07", "smi2-s02.html", 421, 421, 421),
    ("P08", "smi2-s02.html", 422, 423, 422),
    ("P09", "smi2-s02.html", 426, 427, 426),
    ("P10", "smi2-s02.html", 429, 430, 429),
    ("P11", "smi2-s02.html", 443, 444, 443),
]


def html_text(line):
    import html
    t = re.sub(r"<[^>]+>", "", line)
    return html.unescape(t)


def main():
    digests = {}
    lines = {}
    for f in {r[1] for r in ROWS}:
        p = os.path.join(FETCH, f)
        b = open(p, "rb").read()
        digests[f] = hashlib.sha256(b).hexdigest()
        text = b.decode("utf-8", "replace").split("\n")
        lines[f] = text
    print("digests:")
    for f in sorted(digests):
        print("  %-20s %s bytes=%d" % (f, digests[f], len(open(os.path.join(FETCH, f), "rb").read())))
    print()
    for rid, f, a, b, anchor in ROWS:
        seg = lines[f][a - 1:b]
        if f.endswith(".html"):
            seg = [html_text(x) for x in seg]
        t = " ".join(x.strip() for x in seg)
        t = re.sub(r"\s+", " ", t).strip()
        if rid == "P08":
            t = t[len("missing, "):]
        if rid == "P10":
            t = t[:t.index("ignored") + len("ignored")]
        if rid == "P06":
            t = t[:t.index("byte-swapping.") + len("byte-swapping.")]
        if rid == "P07":
            t = t[:t.index("optional.") + len("optional.")]
        if rid == "P09":
            t = t[t.index("The parent"):]
        if rid == "P11":
            t = t[:t.index("directories") + len("directories")]
        n = len(t.split())
        flag = "" if n <= 25 else "  ** OVER 25 **"
        print("%-4s %s:%d  words=%d%s\n     %s" % (rid, f, anchor, n, flag, t))


if __name__ == "__main__":
    main()
