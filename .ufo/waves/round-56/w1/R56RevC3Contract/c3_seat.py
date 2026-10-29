# Independent C3 computation written from registration.md §C3 only (seat R56RevC3Contract).
import os, re, subprocess, sys, json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = sys.argv[1] if len(sys.argv) > 1 else "13f0acbe3a15da2d9c08357a576d91dcadc85273"
WORK = "/fast/scratch/hyaku/mado-r56/R56RevC3Contract/work"
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": WORK, "TMPDIR": WORK, "LC_ALL": "C"}

def git(*args, text=True):
    p = subprocess.run(["git", "-C", LANE, *args], env=ENV, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("git failed: %r %s" % (args, p.stderr.decode(errors="replace")))
    return p.stdout.decode("utf-8", errors="replace") if text else p.stdout

def blob(path):
    return git("cat-file", "blob", f"{REV}:{path}", text=False).decode("utf-8", errors="replace")

# ENTRIES: regular blobs corpus/knowledge/*.md, direct children
ENTRIES = {}
for line in git("ls-tree", REV, "corpus/knowledge/").splitlines():
    meta, path = line.split("\t", 1)
    mode, typ, sha = meta.split()
    if typ == "blob" and mode in ("100644", "100755") and path.endswith(".md") and "/" not in path[len("corpus/knowledge/"):]:
        ENTRIES[path] = sha

# ROWS
ROW_RE = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
rows = {}      # id -> dict
row_lines = []
for ln in blob("corpus/SOURCES.md").split("\n"):
    if not ROW_RE.match(ln):
        continue
    s = ln.strip()
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") else s
    cells = [c.strip() for c in s.split("|")]
    if len(cells) != 11:
        print("SETUP_ROWCELLS", len(cells), repr(ln[:120]), file=sys.stderr)
        raise SystemExit(2)
    rid = cells[0]
    if rid in rows:
        print("DUP_ROW", rid, file=sys.stderr)
    rows.setdefault(rid, {"cells": cells, "line": ln, "count": 0})
    rows[rid]["count"] += 1
row_ids = set(rows)

FENCE = re.compile(r"^ {0,3}(```|~~~)")
S_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
USEDBY_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")

def text_of(path):
    return blob(path).split("\n")

def cite_lines(lines):
    """Return list of (lineno, id) for S-tokens outside fenced blocks."""
    out = []
    infence = False
    for i, ln in enumerate(lines, 1):
        if FENCE.match(ln):
            infence = not infence
            continue
        if infence:
            continue
        for m in S_RE.finditer(ln):
            out.append((i, m.group(0), ln))
    return out

CITE = {}
CITE_DETAIL = {}
for p in ENTRIES:
    lines = text_of(p)
    cl = cite_lines(lines)
    CITE[p] = set(t for _, t, _ in cl)
    CITE_DETAIL[p] = cl

SRC = {}
for p in ENTRIES:
    lines = text_of(p)[:15]
    toks = set()
    for ln in lines:
        if ln.startswith("source:"):
            toks.update(S_RE.findall(ln))
    SRC[p] = toks

USEDBY = {rid: set(USEDBY_RE.findall(rows[rid]["cells"][10])) for rid in rows}

missing = []
for p in sorted(ENTRIES):
    for s in sorted(CITE[p]):
        if s in row_ids and p not in USEDBY[s]:
            missing.append((s, p))
extra = []
for rid in sorted(rows):
    for p in sorted(USEDBY[rid]):
        if p not in ENTRIES or rid not in CITE.get(p, set()):
            extra.append((rid, p))
dangling = []
for p in sorted(ENTRIES):
    for s in sorted(SRC[p]):
        if s not in row_ids:
            dangling.append((p, s))

verdict = "TARGET_MET" if not (missing or extra or dangling) else "TARGET_MISSED"
print(f"MADO_USED_BY: rev={REV} entries={len(ENTRIES)} rows={len(rows)} missing={len(missing)} extra={len(extra)} dangling={len(dangling)} verdict={verdict}")
with open(WORK + "/missing.tsv", "w") as f:
    for s, p in missing:
        f.write(f"{s}\t{p}\n")
with open(WORK + "/extra.tsv", "w") as f:
    for s, p in extra:
        f.write(f"{s}\t{p}\n")
with open(WORK + "/dangling.tsv", "w") as f:
    for p, s in dangling:
        f.write(f"{p}\t{s}\n")
# detail of every citation line for missing pairs
with open(WORK + "/missing-lines.txt", "w") as f:
    for s, p in missing:
        for ln_no, tok, ln in CITE_DETAIL[p]:
            if tok == s:
                f.write(f"{s}\t{p}\t{ln_no}\t{ln}\n")
print("rows with dup ids:", [r for r in rows if rows[r]["count"] > 1])
print("entries with S-cites:", sum(1 for p in CITE if CITE[p]))
