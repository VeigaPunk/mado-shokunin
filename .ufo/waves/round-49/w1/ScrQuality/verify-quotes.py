#!/usr/bin/env python3
"""verify-quotes.py - check every receipt locator this seat's criteria.md cites.

Criterion 77's rule applied to the seat's own prose: a locator is computed, and the
cited line must carry the fragment the sentence quotes. For every `(:NN)` or
`(:NN, :MM)` in criteria.md this reads the named line of the receipt and reports
whether at least one backticked fragment from the same sentence occurs in it.

Reads only. Usage: verify-quotes.py --criteria FILE --receipt FILE
Exit: 0 every locator supported, 1 at least one misses, 2 usage.
"""
import argparse
import re
import sys

LOCATOR = re.compile(r'\(:(\d{1,4})(?:,\s*:(\d{1,4}))?\)')
def fragments_of(text):
    """Backtick spans paired in order, so an odd backtick cannot shift the pairing."""
    out, spans = [], [i for i, ch in enumerate(text) if ch == "`"]
    for start, end in zip(spans[0::2], spans[1::2]):
        body = text[start + 1:end]
        if len(body) >= 4:
            out.append(body)
    return out


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--criteria", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    try:
        criteria = open(args.criteria, "r", errors="replace").read().splitlines()
        receipt = open(args.receipt, "r", errors="replace").read().splitlines()
    except OSError as exc:
        print("VERIFY_QUOTES: error=%s" % exc)
        return 2
    checked = supported = 0
    # Walk blank-line-separated paragraphs: a sentence wraps, so its locator and the
    # fragment it quotes may sit on different physical lines.
    index, paragraphs = 0, []
    current, start = [], 1
    for line in criteria:
        if line.strip():
            if not current:
                start = index + 1
            current.append(line)
        elif current:
            paragraphs.append((start, " ".join(current)))
            current = []
        index += 1
    if current:
        paragraphs.append((start, " ".join(current)))
    for idx, line in paragraphs:
        for match in LOCATOR.finditer(line):
            for group in match.groups():
                if not group:
                    continue
                number = int(group)
                checked += 1
                if number < 1 or number > len(receipt):
                    print("LOC criteria=%d:%d receipt=%d verdict=OUT_OF_RANGE" %
                          (idx, number, number))
                    continue
                target = receipt[number - 1]
                window = line[:match.start()]
                fragments = [f for f in fragments_of(window) if not LOCATOR.search(f)]
                if not fragments:
                    print("LOC criteria=%d:%d receipt=%d verdict=NO_FRAGMENT" %
                          (idx, number, number))
                    continue
                # nearest-first: the fragment a locator names is the one just before it
                hits = []
                for frag in reversed(fragments):
                    parts = [p for p in frag.split("…") if p.strip()]
                    if parts and all(part in target for part in parts):
                        hits.append(frag)
                        break
                    if parts and parts[0].strip() and parts[0].strip() in target:
                        hits.append(frag)
                        break
                if hits:
                    supported += 1
                    print("LOC criteria=%d:%d receipt=%d supported=yes frag=%s"
                          % (idx, number, number, hits[0][:60]))
                else:
                    print("LOC criteria=%d:%d receipt=%d supported=no line=%s"
                          % (idx, number, number, target[:100]))
    print("VERIFY_QUOTES: checked=%d supported=%d verdict=%s"
          % (checked, supported, "OK" if checked == supported else "MISS"))
    return 0 if checked == supported else 1


if __name__ == "__main__":
    sys.exit(main())
