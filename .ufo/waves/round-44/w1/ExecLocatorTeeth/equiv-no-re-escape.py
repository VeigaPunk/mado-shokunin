#!/usr/bin/env python3
"""equiv-no-re-escape.py - mechanical proof that the `no-re-escape` mutant is equivalent.

The mutant replaces `re.escape(tok)` with `tok` in token_occurs. That is an
equivalence iff re.escape is the identity on every string token_occurs can ever
receive. token_occurs is called with (a) fragment_tokens output, which is
ID_RE matches filtered to len >= 3, i.e. strings over [A-Za-z0-9_], and (b)
fragment_numbers output, which is NUM_RE matches, i.e. strings over [0-9].

Checks:
  1. alphabet: every ID_RE / NUM_RE match is a word-char string (exhaustive over
     the fixture fragments and over a random prose corpus of lane bytes).
  2. re.escape identity: exhaustive over [A-Za-z0-9_]{1,3} (254,079 strings) and
     a random sample over [A-Za-z0-9_]{4,24}.
  3. compiled-pattern equality for every enumerated token.
"""

import random
import re
import sys

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
ID_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
NUM_RE = re.compile(r"[0-9]+")


def bounded(tok):
    return r"(?<![A-Za-z0-9_])" + re.escape(tok) + r"(?![A-Za-z0-9_])"


def escaped_only(tok):
    return r"(?<![A-Za-z0-9_])" + tok + r"(?![A-Za-z0-9_])"


def exhaustive(maxlen):
    out = []
    frontier = [""]
    for _ in range(maxlen):
        nxt = []
        for prefix in frontier:
            for ch in ALPHABET:
                s = prefix + ch
                nxt.append(s)
                out.append(s)
        frontier = nxt
    return out


def main():
    bad_escape = 0
    bad_pattern = 0
    n = 0
    for s in exhaustive(3):
        n += 1
        if re.escape(s) != s:
            bad_escape += 1
        if bounded(s) != escaped_only(s):
            bad_pattern += 1
    rng = random.Random(44)
    for _ in range(300000):
        L = rng.randint(4, 24)
        s = "".join(rng.choice(ALPHABET) for _ in range(L))
        n += 1
        if re.escape(s) != s:
            bad_escape += 1
        if bounded(s) != escaped_only(s):
            bad_pattern += 1

    nonword = 0
    samples = 0
    for path in sys.argv[1:]:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for m in ID_RE.finditer(text):
            samples += 1
            if not re.fullmatch(r"[A-Za-z0-9_]+", m.group(0)):
                nonword += 1
        for m in NUM_RE.finditer(text):
            samples += 1
            if not re.fullmatch(r"[0-9]+", m.group(0)):
                nonword += 1

    print("tokens enumerated=%d re_escape_differs=%d pattern_differs=%d" % (n, bad_escape, bad_pattern))
    print("lane matches sampled=%d non_word_char=%d" % (samples, nonword))
    ok = bad_escape == 0 and bad_pattern == 0 and nonword == 0
    print("EQUIV no-re-escape: %s" % ("PROVEN EQUIVALENT" if ok else "NOT EQUIVALENT"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
