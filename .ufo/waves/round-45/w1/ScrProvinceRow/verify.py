#!/usr/bin/env python3
"""verify.py - check the round-45 province draft against its receipts (seat ScrProvinceRow).

Checks, in order, and prints one `OK`/`FAIL` line each:
  1  every quote row in province.md is <= 25 words, its source locator exists at that line in
     `receipts/quotes.txt` (computed there with `grep -n -F`), and the quote text occurs on that line;
  2  the PROVINCE anchors the draft cites are the live file's lines (header 22, last tool row 32,
     coverage claim 34, round-23 refinement 20, file length 97, 9 tool rows) and SKILL.md:343 is rule 4;
  3  the counter facts the draft states are the frozen modules' own values (49 fixtures, 17 surfaces,
     9 pins, seed default 45) and the reference tool still passes its in-memory selftest 33/33;
  4  the two conditional rows are still conditional: the tool blob and the gate are absent at HEAD;
  5  the draft itself carries no session material (no /home/ path, no `users:(("`, no `serial=`);
  6  no quote is repeated with a different locator.
Exit 0 iff every check is OK.
"""
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
DRAFT = os.path.join(HERE, "province.md")
QUOTES = os.path.join(HERE, "receipts", "quotes.txt")
C1 = os.path.join(LANE, "quality", "counters", "c1-r45-monitors.py")
C2 = os.path.join(LANE, "quality", "counters", "c2-r45-monitor-entry.py")
REF = os.path.join(LANE, ".ufo", "waves", "round-45", "l1-draft", "mado-monitors.py")
PROVINCE = os.path.join(LANE, "PROVINCE.md")

fails = []


def check(ok, line):
    print(("OK   " if ok else "FAIL ") + line)
    if not ok:
        fails.append(line)


def load(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def grep_receipt(path, source, line, quote):
    """True iff receipts/quotes.txt has a `== source` section whose `<line>:` line holds quote."""
    cur = None
    want = "%d:" % line
    for raw in load(path).splitlines():
        if raw.startswith("== "):
            cur = raw[3:].strip()
            continue
        if cur == source and raw.startswith(want) and quote in raw:
            return True
    return False


def main():
    draft = load(DRAFT)
    rows = re.findall(r"^\| (.+?) \| `([^`]+):(\d+)` \| `receipts/quotes\.txt` \|$", draft, re.M)
    check(len(rows) == 16, "quote rows in the draft: %d (expected 16)" % len(rows))
    for quote, src, line in rows:
        n = len(quote.split())
        check(n <= 25, "quote words %d <= 25 :: %s" % (n, quote[:60]))
        check(grep_receipt(QUOTES, src, int(line), quote),
              "quote at %s:%s verified in receipts/quotes.txt :: %s" % (src, line, quote[:60]))

    prov = load(PROVINCE).splitlines()
    check(len(prov) == 97, "PROVINCE.md length %d (draft says 97)" % len(prov))
    check(prov[21].startswith("| Tool | Reads |"), "PROVINCE.md:22 is the table header")
    check(prov[31].startswith("| `tools/mado-geometry.py` |"), "PROVINCE.md:32 is the last tool row")
    check(sum(1 for l in prov if l.startswith("| `tools/")) == 9, "tool table rows: 9")
    check(prov[33].startswith("**Round-23 wave-2 correction"), "PROVINCE.md:34 is the coverage claim")
    check(prov[19].startswith("**Round-23 refinement"), "PROVINCE.md:20 is the round-23 refinement")
    skill = load(os.path.join(LANE, "SKILL.md")).splitlines()
    check(skill[342].startswith("4. **Session material stays shape-only.**"), "SKILL.md:343 is rule 4")
    check(sum(1 for l in os.scandir(os.path.join(LANE, "tools")) if l.is_file()) == 12,
          "tools/ holds 12 tracked files or more")

    c1 = module(C1, "c1_r45")
    c2 = module(C2, "c2_r45")
    check(len(c1.FIXTURES) == 49, "C1 fixtures: %d" % len(c1.FIXTURES))
    ap_default = re.search(r'--seed", type=int, default=(\d+)', load(C1))
    check(bool(ap_default) and ap_default.group(1) == "45", "C1 --seed default 45")
    check(len(c2.SURFACES) == 17, "C2 surfaces: %d" % len(c2.SURFACES))
    check(len(c2.PINS) == 9, "C2 pins: %d" % len(c2.PINS))
    run = subprocess.run([sys.executable, "-I", REF, "--selftest"], capture_output=True, text=True)
    check(run.returncode == 0 and run.stdout.strip() == "MADO_MONITORS_SELFTEST: 33/33 passed",
          "reference selftest: %r" % run.stdout.strip())

    for rel in ("tools/mado-monitors.py", "quality/check-session-material.py"):
        ls = subprocess.run(["git", "-C", LANE, "ls-tree", "HEAD", "--", rel],
                            capture_output=True, text=True)
        check(ls.stdout == "", "%s absent at HEAD (row/paragraph stays conditional)" % rel)
    gate_draft = os.path.join(LANE, ".ufo", "waves", "round-45", "w1", "ExecPrivacyGate",
                              "check-session-material.py")
    check(os.path.isfile(gate_draft), "gate draft present at the seat path the draft names")

    check("/home/" not in draft, "no /home/ path in the draft")
    check('users:(("' not in draft, "no ss process-table row in the draft")
    check("serial=" not in draft, "no serial value in the draft")

    body = re.sub(r"\s+", " ", draft.split("## 4. Quotes and locators")[0])
    flat = re.sub(r"\s+", " ", load(QUOTES))
    quoted = re.findall(r'"([^"]{12,})"', body)
    for q in quoted:
        check(len(q.split()) >= 3 and q in flat,
              "body quote present in receipts/quotes.txt :: %s" % q[:60])

    seen = {}
    dup = 0
    for quote, src, line in rows:
        dup += seen.setdefault(quote, (src, line)) != (src, line)
    check(dup == 0, "no quote repeated with a different locator")

    print("VERIFY: %s (%d failures)" % ("OK" if not fails else "FAILED", len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
