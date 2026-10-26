#!/usr/bin/env python3
"""Verify every quote cited in CritAssimilation/findings.md against its source file.

Each row of quotes.tsv is: id<TAB>absolute-path<TAB>quote
Prints one line per quote: id status=OK|MISS lines=<comma list> file=<basename>
Exit 0 iff no MISS. Read-only.
"""
import sys, os

SEAT = os.path.dirname(os.path.abspath(__file__))

def norm(s):
    return " ".join(s.split())

def main():
    rows = []
    with open(os.path.join(SEAT, "quotes.tsv"), encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) != 3:
                print("BADROW %r" % ln)
                return 2
            rows.append(parts)
    miss = 0
    for qid, path, quote in rows:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as e:
            print("%s status=NOSRC file=%s err=%s" % (qid, os.path.basename(path), e))
            miss += 1
            continue
        q = norm(quote)
        hits = [str(i + 1) for i, line in enumerate(text.splitlines())
                if q in norm(line)]
        if not hits:
            # allow multi-line quotes
            if q in norm(text):
                print("%s status=OK_SPANS lines=- file=%s" % (qid, os.path.basename(path)))
                continue
            print("%s status=MISS lines=- file=%s quote=%s" % (qid, os.path.basename(path), q[:60]))
            miss += 1
        else:
            print("%s status=OK lines=%s file=%s words=%d" % (
                qid, ",".join(hits), os.path.basename(path), len(q.split())))
    print("QUOTES: checked=%d miss=%d" % (len(rows), miss))
    return 0 if miss == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
