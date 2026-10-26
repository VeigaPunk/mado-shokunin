#!/usr/bin/env python3
"""Check that findings.md is grounded in the receipts it cites.

Checks, in order:
 1. the pinned target still hashes to the declared sha256;
 2. no @@CASE:@@ placeholder survived assembly;
 3. every inline JSON case parses, carries the frozen schema keys, and its
    "expect" is byte-identical to the same id in receipts/minimal-cases.jsonl
    (which was produced by running the real script);
 4. every `xdg-terminal-exec:<n>` citation is in range and has a dump line in
    receipts/locators.txt;
 5. every case id mentioned in prose exists in the receipts.

Exit 0 = every check passed; 1 = at least one failure (each is printed).

Usage: verify_findings.py [--seat DIR] [--receipts DIR]
"""
import argparse
import hashlib
import json
import os
import re
import sys

PIN = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
TARGET = "/usr/bin/xdg-terminal-exec"
SCHEMA = ("id", "class", "env", "files", "exec", "args", "expect")


def main(argv):
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--seat", default=here)
    ap.add_argument("--receipts", default=os.path.join(here, "receipts"))
    ap.add_argument("--write-locators", action="store_true",
                    help="regenerate receipts/locators.txt from the citations found")
    a = ap.parse_args(argv)
    md_path = os.path.join(a.seat, "findings.md")
    text = open(md_path, encoding="utf-8").read()
    fails = []

    digest = hashlib.sha256(open(TARGET, "rb").read()).hexdigest()
    print("target sha256: %s %s" % (digest, "OK" if digest == PIN else "MISMATCH"))
    if digest != PIN:
        fails.append("target sha256 is not the declared pin")

    if "@@CASE:" in text:
        fails.append("unassembled @@CASE:@@ placeholder(s) remain")
    print("placeholders: %s" % ("none" if "@@CASE:" not in text else "PRESENT"))

    receipt = {}
    with open(os.path.join(a.receipts, "minimal-cases.jsonl"), encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            receipt[obj["id"]] = obj
    print("receipt cases: %d" % len(receipt))

    inline = 0
    for i, line in enumerate(text.split("\n"), 1):
        if not line.startswith("{"):
            continue
        inline += 1
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            fails.append("findings.md:%d inline JSON does not parse: %s" % (i, e))
            continue
        missing = [k for k in SCHEMA if k not in obj]
        if missing:
            fails.append("findings.md:%d case %s lacks %s"
                         % (i, obj.get("id"), ",".join(missing)))
            continue
        ref = receipt.get(obj["id"])
        if ref is None:
            fails.append("findings.md:%d case %s is not in the receipt"
                         % (i, obj["id"]))
        elif obj["expect"] != ref["expect"]:
            fails.append("findings.md:%d case %s expect != receipt (claimed %s, got %s)"
                         % (i, obj["id"], json.dumps(obj["expect"]),
                            json.dumps(ref["expect"])))
    print("inline cases checked: %d" % inline)
    if inline == 0:
        fails.append("no inline cases found in findings.md")

    locators = set()
    with open(os.path.join(a.receipts, "locators.txt"), encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\s*(\d+)\|", line)
            if m:
                locators.add(int(m.group(1)))
    body, fence = [], False
    for ln in text.split("\n"):
        if ln.startswith("```"):
            fence = not fence
            continue
        if not fence:
            body.append(ln)
    cited = set()
    for m in re.finditer(r":(\d{2,4})(?:-:(\d{2,4}))?", "\n".join(body)):
        lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
        cited.update(range(lo, hi + 1))
    cited = sorted(cited)
    if a.write_locators:
        src = open(TARGET, encoding="utf-8", errors="surrogateescape").read().split("\n")
        with open(os.path.join(a.receipts, "locators.txt"), "w", encoding="utf-8") as f:
            f.write("# every line cited by findings.md, computed from the pinned script\n")
            f.write("script: %s\nsha256: %s\nlines: %d\ncited: %d\n\n"
                    % (TARGET, digest, len(src), len(cited)))
            for n in cited:
                f.write("%4d| %s\n" % (n, src[n - 1]))
        locators = set(cited)
        print("locators.txt rewritten: %d cited lines" % len(cited))
    print("cited lines: %d (dumped: %d)" % (len(cited), len(locators)))
    for n in cited:
        if not (1 <= n <= 1499):
            fails.append("cited line %d out of range" % n)
        if n not in locators:
            fails.append("cited line %d has no locator dump" % n)

    ids = set(receipt)
    with open(os.path.join(a.receipts, "probes.tsv"), encoding="utf-8") as f:
        for line in f:
            ids.add(line.split("\t")[0])
    with open(os.path.join(a.receipts, "cases.jsonl"), encoding="utf-8") as f:
        for line in f:
            ids.add(json.loads(line)["id"])
    mentioned = set(re.findall(r"\b(?:P\d\d[a-z]?-[a-z0-9-]+|F\d\d-[a-z0-9-]+)\b", text))
    unknown = sorted(m for m in mentioned if m not in ids)
    print("case ids mentioned: %d (unknown: %d)" % (len(mentioned), len(unknown)))
    for m in unknown:
        fails.append("case id %s is mentioned but has no receipt" % m)

    print()
    if fails:
        for f_ in fails:
            print("FAIL %s" % f_)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
