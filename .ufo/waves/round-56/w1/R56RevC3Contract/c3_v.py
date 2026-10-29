# Seat-local C3 counter (registration §C3 literal reading) with variant switches for sensitivity tests.
# usage: c3_v.py REPO REV WORK [--commonmark] [--ranges] [--allsource] [--sregex=3|3+]
import os, re, subprocess, sys
args = sys.argv[1:]
REPO, REV, WORK = args[0], args[1], args[2]
FLAGS = set(a for a in args[3:] if a.startswith("--"))
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": WORK, "TMPDIR": WORK, "LC_ALL": "C"}
def git(*a, text=True):
    p = subprocess.run(["git", "-C", REPO, *a], env=ENV, capture_output=True)
    if p.returncode: raise SystemExit("git: %r %s" % (a, p.stderr.decode(errors="replace")))
    return p.stdout.decode("utf-8", errors="replace") if text else p.stdout
def blob(path): return git("cat-file", "blob", f"{REV}:{path}", text=False).decode("utf-8", errors="replace")
ENTRIES = {}
for line in git("ls-tree", REV, "corpus/knowledge/").splitlines():
    meta, path = line.split("\t", 1); mode, typ, sha = meta.split()
    if typ == "blob" and mode in ("100644", "100755") and path.endswith(".md") and "/" not in path[len("corpus/knowledge/"):]:
        ENTRIES[path] = sha
ROW_RE = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
rows = {}
for ln in blob("corpus/SOURCES.md").split("\n"):
    if not ROW_RE.match(ln): continue
    s = ln.strip(); s = s[1:] if s.startswith("|") else s; s = s[:-1] if s.endswith("|") else s
    cells = [c.strip() for c in s.split("|")]
    if len(cells) != 11: raise SystemExit("SETUP rowcells %d" % len(cells))
    rows.setdefault(cells[0], cells)
row_ids = set(rows)
S_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
RANGE_RE = re.compile(r"(?<![A-Za-z0-9])S([0-9]{3})\s*[-\u2013\u2014]\s*S([0-9]{3})(?![0-9])")
USEDBY_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")
FENCE_TOGGLE = re.compile(r"^ {0,3}(```|~~~)")
def fenced_mask(lines):
    """Return list of booleans: True if line is inside a fence (or is a fence line)."""
    mask = [False]*len(lines)
    if "--commonmark" not in FLAGS:
        inf = False
        for i, ln in enumerate(lines):
            if FENCE_TOGGLE.match(ln):
                inf = not inf; mask[i] = True; continue
            mask[i] = inf
        return mask
    # CommonMark-ish: opener run of >=3 ` or ~ with 0-3 spaces; closer same char, len>=opener, 0-3 spaces, no info
    open_ = None
    for i, ln in enumerate(lines):
        if open_ is None:
            m = re.match(r"^ {0,3}(`{3,}|~{3,})", ln)
            if m:
                open_ = m.group(1); mask[i] = True
        else:
            mask[i] = True
            m = re.match(r"^ {0,3}(`{3,}|~{3,})\s*$", ln)
            if m and m.group(1)[0] == open_[0] and len(m.group(1)) >= len(open_):
                open_ = None
    return mask
def cites(lines):
    mask = fenced_mask(lines)
    out = []
    for i, ln in enumerate(lines):
        if mask[i]: continue
        toks = set(S_RE.findall(ln))
        if "--ranges" in FLAGS:
            for a, b in RANGE_RE.findall(ln):
                lo, hi = int(a), int(b)
                if lo <= hi and hi - lo < 100:
                    toks.update("S%03d" % k for k in range(lo, hi+1))
        for t in toks: out.append((i+1, t))
    return out
CITE = {}; SRC = {}
for p in ENTRIES:
    lines = blob(p).split("\n")
    CITE[p] = cites(lines)
    window = lines if "--allsource" in FLAGS else lines[:15]
    t = set()
    for ln in window:
        if ln.startswith("source:"): t.update(S_RE.findall(ln))
    SRC[p] = t
USEDBY = {rid: set(USEDBY_RE.findall(rows[rid][10])) for rid in rows}
citeset = {p: set(t for _, t in CITE[p]) for p in ENTRIES}
missing = [(s, p) for p in sorted(ENTRIES) for s in sorted(citeset[p]) if s in row_ids and p not in USEDBY[s]]
extra = [(r, p) for r in sorted(rows) for p in sorted(USEDBY[r]) if p not in ENTRIES or r not in citeset.get(p, set())]
dangling = [(p, s) for p in sorted(ENTRIES) for s in sorted(SRC[p]) if s not in row_ids]
print(f"MADO_USED_BY: rev={REV} entries={len(ENTRIES)} rows={len(rows)} missing={len(missing)} extra={len(extra)} dangling={len(dangling)} flags={sorted(FLAGS)}")
if "--dump" in FLAGS:
    with open(WORK + "/dump-%s.tsv" % ("_".join(sorted(f[2:] for f in FLAGS)) or "base"), "w") as f:
        for s, p in missing: f.write(f"missing\t{s}\t{p}\n")
        for r, p in extra: f.write(f"extra\t{r}\t{p}\n")
        for p, s in dangling: f.write(f"dangling\t{p}\t{s}\n")
