#!/usr/bin/env python3
"""Falsify43 bypass-ledger generator.

Mechanical, zero-work construction of a tool ledger that satisfies every C1-r52
predicate clause (unique population, non-self resolvable pointer, instrument-
specific context) and the committed r51 counter/checker:

  desc    = the instrument's own leading docstring/comment lines, joined until
            >= 6 normalised words (no human reading, same rule for every file)
  pointer = the production ledger's existing pointer cell for that path,
            copied verbatim (non-self, resolvable, basename-bearing)

Prints a per-row verification table using the SAME norm/bigram semantics as the
C1Simplify draft counter, then writes the ledger table to stdout path given as
argv[1]. Exits nonzero if any row cannot be filled mechanically.
"""
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
LEDGER_REL = "quality/tool-ledger.md"
EMPHASIS = "`*_ \t"
LINE_ANCHOR = re.compile(r":\d+(?:-\d+)?$")


def git(*args):
    out = subprocess.run(("git", "-C", REPO) + args, capture_output=True)
    if out.returncode != 0:
        sys.exit("git failed: %s" % out.stderr.decode()[:300])
    return out.stdout


def population(paths):
    pop = []
    for path in paths:
        if "__pycache__" in path or path.endswith((".pyc", ".pyo")):
            continue
        if path.startswith("tools/"):
            pop.append(path)
        elif path.startswith("quality/counters/"):
            rest = path[len("quality/counters/"):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
        elif path.startswith("quality/"):
            rest = path[len("quality/"):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
    return sorted(set(pop))


def norm(s):
    return " " + re.sub(r"[^a-z0-9]+", " ", s.lower()).strip() + " "


def extract_desc(body):
    """Mechanical: leading docstring/comment lines joined until >=6 norm words."""
    lines = body.decode("utf-8", "replace").splitlines()
    picked, start = [], None
    for i, raw in enumerate(lines):
        s = raw.strip()
        if not s:
            continue
        if s.startswith(("#!", "# -*-", "-*-")):
            continue
        if s.startswith(("#", '"""', "'''")):
            start = i
        break
    if start is None:
        return None
    for raw in lines[start:]:
        s = raw.strip()
        if s.startswith('"""'):
            s = s.lstrip('"').rstrip('"').strip()
        elif s.startswith("'''"):
            s = s.lstrip("'").rstrip("'").strip()
        elif s.startswith("#"):
            s = s.lstrip("#").strip()
        elif not picked:
            break
        if not s:
            if picked:
                break
            continue
        picked.append(s)
        if len(norm(" ".join(picked)).split()) >= 6:
            break
    text = " ".join(picked).strip()
    return text or None


def parse_rows(text):
    rows = {}
    fenced = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = cells[0].strip(EMPHASIS) if cells else ""
        if not first or "/" not in first or first.startswith(":") or set(first) <= set("-: "):
            continue
        rows[first] = cells[2] if len(cells) > 2 else ""
    return rows


def main():
    listing = [p for p in git("ls-tree", "-r", "--name-only", REV).decode(
        "utf-8", "surrogateescape").splitlines() if p]
    pop = population(listing)
    prod = parse_rows(git("show", "%s:%s" % (REV, LEDGER_REL)).decode("utf-8", "replace"))

    blob_cache = {}

    def blob(rel):
        if rel not in blob_cache:
            blob_cache[rel] = git("show", "%s:%s" % (REV, rel))
        return blob_cache[rel]

    out_rows, failures = [], []
    for path in pop:
        desc = extract_desc(blob(path))
        pointer = prod.get(path, "")
        if not desc:
            failures.append((path, "no-desc"))
            continue
        if not pointer:
            failures.append((path, "no-prod-pointer"))
            continue
        out_rows.append((path, desc, pointer))

    # Verification with draft-counter semantics
    print("=== per-row verification (draft semantics) ===")
    bad = 0
    for path, desc, pointer in out_rows:
        words = norm(desc).split()
        short = len(words) < 6
        body = norm(blob(path).decode("utf-8", "replace"))
        bigram = any(" %s " % " ".join(words[i:i + 2]) in body
                     for i in range(len(words) - 1))
        m = re.match(r"^`([^`]+)`$", pointer.strip())
        target = LINE_ANCHOR.sub("", m.group(1).strip()) if m else ""
        single = bool(m)
        resolvable = target in set(listing)
        nonself = target not in (path, LEDGER_REL)
        basename = os.path.basename(path).encode() in blob(target) if resolvable else False
        ok = (not short) and bigram and single and resolvable and nonself and basename
        if not ok:
            bad += 1
        print("%s short=%d bigram=%d single=%d resolvable=%d nonself=%d name_in_target=%d %s"
              % (path, not short, bigram, single, resolvable, nonself, basename,
                 "OK" if ok else "FAIL"))

    with open(sys.argv[1], "w") as fh:
        fh.write("# bypass ledger (mechanical, zero-work)\n\n")
        fh.write("| instrument | description | accountability pointer |\n")
        fh.write("|---|---|---|\n")
        for path, desc, pointer in out_rows:
            desc = desc.replace("|", "/")
            fh.write("| `%s` | %s | %s |\n" % (path, desc, pointer))
    print("=== rows=%d failures=%d table=%s ===" % (len(out_rows), len(failures), sys.argv[1]))
    for f in failures:
        print("FAIL-ROW %s %s" % f)
    return 1 if (failures or bad) else 0


import os  # noqa: E402  (used in basename check)
if __name__ == "__main__":
    sys.exit(main())
