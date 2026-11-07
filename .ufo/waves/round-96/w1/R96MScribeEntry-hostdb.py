#!/usr/bin/env python3
"""Read-only facts about the host's TEXT magic database (no mime.cache read).

Counts sections, matchlets, priorities, word sizes, masks, ranges, indents and
the parse-error rate of /usr/share/mime/magic, and prints the file digests the
round-96 host-db control lists.  Stdlib only; opens one host file read-only.
"""
import hashlib
import sys

PATH = "/usr/share/mime/magic"
HEADER = b"MIME-Magic\x00\n"


class Bad(Exception):
    pass


def read_number(buf, i):
    j = i
    while j < len(buf) and 48 <= buf[j] <= 57:
        j += 1
        if j - i == 30:
            break
    if j == i:
        return -1, i
    return int(buf[i:j]), j


def parse(buf):
    """Return (sections, errors) with the C's state machine semantics."""
    sections = []
    errors = []  # (line_start, reason)
    i = 0
    n = len(buf)
    cur = None
    line_start = 0
    while i < n:
        line_start = i
        if buf[i] != 0x5B:  # '['
            # parse_error: skip to newline
            nl = buf.find(b"\n", i)
            errors.append((line_start, "not-a-section-line"))
            if nl < 0:
                break
            i = nl + 1
            continue
        i += 1
        prio, i = read_number(buf, i)
        if prio < 0 or i >= n or buf[i] != 0x3A:  # ':'
            nl = buf.find(b"\n", i)
            errors.append((line_start, "bad-priority-or-colon"))
            if nl < 0:
                break
            i = nl + 1
            continue
        i += 1
        j = i
        while j < n and buf[j] not in (0x00, 0x0A):
            j += 1
        if j >= n:
            errors.append((line_start, "eof-in-type"))
            break
        k = buf.find(b"]", i, j)
        if k < 0:
            errors.append((line_start, "unterminated-type"))
            i = j + 1
            continue
        typ = buf[i:k]
        i = j + 1  # the C consumed the newline (or NUL) with read_to_newline
        # matchlets
        mls = []
        while i < n and buf[i] != 0x5B:
            mstart = i
            if buf[i] == 0x0A:
                i += 1
                continue
            indent = 0
            if 48 <= buf[i] <= 57:
                indent, i = read_number(buf, i)
            if i >= n or buf[i] != 0x3E:  # '>'
                # error: free the section, skip to newline
                nl = buf.find(b"\n", i)
                errors.append((mstart, "expected-gt"))
                mls = None
                i = n if nl < 0 else nl + 1
                break
            i += 1
            off, i = read_number(buf, i)
            if off < 0 or i >= n or buf[i] != 0x3D:  # '='
                nl = buf.find(b"\n", i)
                errors.append((mstart, "bad-offset"))
                mls = None
                i = n if nl < 0 else nl + 1
                break
            i += 1
            if i + 1 >= n:
                errors.append((mstart, "eof-in-length"))
                mls = None
                i = n
                break
            vlen = (buf[i] << 8) | buf[i + 1]
            i += 2
            if i + vlen > n:
                errors.append((mstart, "eof-in-value"))
                mls = None
                i = n
                break
            i += vlen
            mask = False
            word = 1
            rng = 1
            if i < n and buf[i] == 0x26:  # &
                mask = True
                i += 1
                if i + vlen > n:
                    errors.append((mstart, "eof-in-mask"))
                    mls = None
                    i = n
                    break
                i += vlen
            if i < n and buf[i] == 0x7E:  # ~
                i += 1
                word, i = read_number(buf, i)
                if word < 0:
                    word = (1 << 32) - 1
                if word not in (0, 1, 2, 4):
                    nl = buf.find(b"\n", i)
                    errors.append((mstart, "bad-word-size"))
                    mls = None
                    i = n if nl < 0 else nl + 1
                    break
            if i < n and buf[i] == 0x2B:  # +
                i += 1
                rng, i = read_number(buf, i)
                if rng < 0:
                    nl = buf.find(b"\n", i)
                    errors.append((mstart, "bad-range"))
                    mls = None
                    i = n if nl < 0 else nl + 1
                    break
            if i >= n or buf[i] != 0x0A:
                nl = buf.find(b"\n", i)
                errors.append((mstart, "unknown-char"))
                mls = None
                i = n if nl < 0 else nl + 1
                break
            i += 1
            if word > 1 and vlen % word != 0:
                nl = buf.find(b"\n", i)
                errors.append((mstart, "word-len-mismatch"))
                mls = None
                i = n if nl < 0 else nl + 1
                break
            mls.append((indent, off, vlen, mask, word, rng))
        if mls is not None:
            sections.append((prio, typ, mls))
    return sections, errors


def main():
    buf = open(PATH, "rb").read()
    print("path %s bytes %d sha256 %s" % (PATH, len(buf), hashlib.sha256(buf).hexdigest()))
    print("header_ok %s" % (buf[:12] == HEADER))
    sections, errors = parse(buf[12:])
    print("sections %d errors %d" % (len(sections), len(errors)))
    for e in errors[:10]:
        print("  error line_off=%d %s" % e)
    n_match = sum(len(m) for _, _, m in sections)
    print("matchlets %d" % n_match)
    from collections import Counter
    prio = Counter(p for p, _, _ in sections)
    print("priorities %s" % " ".join("%d:%d" % (k, prio[k]) for k in sorted(prio)))
    print("sections_at_ge80 %d" % sum(v for k, v in prio.items() if k >= 80))
    print("sections_at_0 %d" % prio.get(0, 0))
    words = Counter(m[4] for _, _, m in sections for m in m_ml(m))
    print("word_sizes %s" % " ".join("%d:%d" % (k, words[k]) for k in sorted(words)))
    masks = sum(1 for _, _, m in sections for m in m_ml(m) if m[3])
    rngs = Counter(m[5] for _, _, m in sections for m in m_ml(m))
    print("masked %d range_gt1 %d max_range %d" % (masks, sum(1 for _, _, m in sections
          for m in m_ml(m) if m[5] > 1), max(rngs) if rngs else 0))
    indents = Counter(m[0] for _, _, m in sections for m in m_ml(m))
    print("indents %s max_indent %d" % (" ".join("%d:%d" % (k, indents[k]) for k in sorted(indents)),
                                        max(indents) if indents else 0))
    ext = max((m[1] + m[2] + m[5] for _, _, ml in sections for m in ml), default=0)
    print("max_extent %d" % ext)
    types = Counter(t for _, t, _ in sections)
    print("distinct_types %d" % len(types))
    # duplicate priority+type sections (first in file order wins)
    dup = sum(1 for t, c in types.items() if c > 1)
    print("types_listed_more_than_once %d" % dup)
    longest = max((len(t) for _, t, _ in sections), default=0)
    print("longest_type_bytes %d" % longest)


def m_ml(m):
    return m


if __name__ == "__main__":
    sys.exit(main())
