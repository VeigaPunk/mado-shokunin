#!/usr/bin/env python3
"""Round-48 w1 (seat ExecErrataR45) locator check for block.md.

Every `file:line[-line]` and "line N" the append block states is recomputed from the pinned
bytes of this tree with grep-equivalent scans, never trusted from the block. Read-only: no
process is started except `git show` for one revision-addressed read, nothing is written.

usage: verify-locators.py [--repo DIR] [--block FILE] [--tool-rev REV]
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/hyprland-monitor-rule-r45.md"
ENTRY_SHA = "128df1bd1055fcbb09f611c48286cd013e9d8bade992f4c17e81ba0615bb9c7b"
FETCH45 = ".ufo/waves/round-45/fetch/"
PINS_W1 = ".ufo/waves/round-47/w1/ScrErrataR45/pins/"
PINS_W2 = ".ufo/waves/round-47/w2/ExecErrataR45/pins/"
SHA_MANIFEST = ".ufo/waves/round-45/receipts/fetch-sha256.txt"
R45_RECEIPT_TOOL = ".ufo/waves/round-45/receipts/live-monitors-host-r45.txt"
R45_RECEIPT_DRAFT = ".ufo/waves/round-45/receipts/live-monitors-host-l1.txt"
COMMIT_JSON = PINS_W1 + "hyprland-commit-a9902ea.json"
LEGACY_404 = PINS_W1 + "legacy-cfg-a9902ea.txt"
TOOL = "tools/mado-monitors.py"
TOOL_SHA = "2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609"
COMMIT_SHA = "a9902ea65f461af868497c4e74fed798ade0b1b0"

# source path -> pinned copy, for the citations that name an upstream path
LAYOUT = {
    "src/backend/Wayland.cpp": "aqua-Wayland-v0.15.1.cpp",
    "src/backend/Headless.cpp": "aqua-Headless-v0.15.1.cpp",
    "src/output/Output.cpp": "aqua-Output-v0.15.1.cpp",
    "include/aquamarine/output/Output.hpp": "aqua-Output.hpp",
    "src/backend/drm/DRM.cpp": "aqua-DRM-v0.15.1.cpp",
    "src/config/lua/bindings/LuaBindingsConfigRules.cpp":
        "hyprland-LuaBindingsConfigRules-a9902ea.cpp",
    "src/config/lua/ConfigManager.cpp": "hyprland-lua-cfg-a9902ea.cpp",
    "src/config/ConfigManager.cpp": "hyprland-main-cfg-a9902ea.cpp",
    "src/config/ConfigManager.hpp": "hyprland-ConfigManager-hpp-a9902ea.hpp",
    "src/config/legacy/ConfigManager.cpp": "legacy-cfg-a9902ea.txt",
}
STOP = set("""the and for that this with from into only then than there their these those
entry block landed cited citation claim claims line lines text above stands round source list
names name file files keeps keep left keeps same commit removes remove still single comes
corrected fresh starts falls through site hard has have does not open remains push guard""".split())

FAILS = []
NOTES = []


def fail(msg):
    FAILS.append(msg)
    print("FAIL " + msg)


def read(repo, rel):
    p = os.path.join(repo, rel)
    with open(p, "rb") as fh:
        return fh.read()


def lines_of(blob):
    return blob.decode("utf-8", "replace").split("\n")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    return p.stdout


def landed_lines(repo):
    """The entry as landed, i.e. without any appended `## Errata` block."""
    ls = lines_of(read(repo, ENTRY))
    return ls[:next((i for i, l in enumerate(ls) if l.startswith("## Errata")), len(ls))]


class Pins:
    def __init__(self, repo):
        self.repo = repo
        self.paths = {}
        for base in (FETCH45, PINS_W1, PINS_W2):
            d = os.path.join(repo, base)
            for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
                self.paths.setdefault(name, base + name)
        self.cache = {}

    def find(self, token):
        tok = token
        if "/" in tok:
            if tok in LAYOUT:
                tok = LAYOUT[tok]
            else:
                tok = tok.rsplit("/", 1)[-1]
        return self.paths.get(tok)

    def lines(self, token):
        rel = self.find(token)
        if rel is None:
            return None, None
        if rel not in self.cache:
            self.cache[rel] = lines_of(read(self.repo, rel))
        return rel, self.cache[rel]


LOC_RE = re.compile(r"(?<![\w.-])(?:(?P<file>[A-Za-z0-9_./-]+\.(?:cpp|hpp|md)))?"
                    r":(?P<a>\d+)(?:-(?P<b>\d+))?(?![\d])")
BT_RE = re.compile(r"`([^`]+)`")
DQ_RE = re.compile(r'"([^"]{10,})"')
ENTRY_REF_RE = re.compile(r"\bentry\s+line\s+(\d+)\b")
RECEIPT_REF_RE = re.compile(r"\breceipt\s+line\s+(\d+)\b")
RECEIPT_PATH_RE = re.compile(r"(?<![\w.-])(\.ufo/waves/round-\d+/receipts/[A-Za-z0-9._-]+)")
HEX_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
DEC_RE = re.compile(r"(?<![\w.])\d+\.\d+(?![\w.])")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{4,}")


def bullets(text):
    out = []
    for line in text.splitlines():
        if line.startswith("- E"):
            out.append([line])
        elif out and line.startswith((" ", "\t")):
            out[-1].append(line)
    return ["\n".join(b) for b in out]


def locators(bullet):
    """(file-or-context, a, b) in reading order, shorthand carrying the last file."""
    found, ctx = [], None
    for line in bullet.splitlines():
        for m in LOC_RE.finditer(line):
            if m.group("file"):
                ctx = m.group("file")
            if ctx is None:
                continue
            found.append((ctx, int(m.group("a")), int(m.group("b") or m.group("a"))))
    return found


def check_pin_integrity(repo, pins):
    blob = read(repo, SHA_MANIFEST)
    rows = [l.split() for l in lines_of(blob) if l.strip()]
    ok = 0
    for digest, name in ((r[0], r[-1]) for r in rows):
        rel = FETCH45 + name.rsplit("/", 1)[-1]
        try:
            got = sha256(read(repo, rel))
        except OSError:
            got = None
        good = got == digest
        ok += good
        print("pin  %-40s want=%s got=%s %s"
              % (name, digest[:12], (got or "MISSING")[:12], "OK" if good else "MISS"))
        if not good:
            fail("pin integrity %s" % name)
    print("pins round-45 fetch: %d/%d byte-identical to fetch-sha256.txt" % (ok, len(rows)))
    return ok == len(rows)


def check_citations(pins, bullet, tag):
    seen = set()
    for name, a, b in locators(bullet):
        rel, lines = pins.lines(name)
        if rel is None:
            fail("%s cites %s:%d but no pinned copy of %s is in this tree"
                 % (tag, name, a, name))
            continue
        if b > len(lines) or a < 1:
            fail("%s cites %s:%d-%d outside the %d-line receipt %s"
                 % (tag, name, a, b, len(lines), rel))
            continue
        key = (rel, a, b)
        if key in seen:
            continue
        seen.add(key)
        shown = " ".join(l.strip() for l in lines[a - 1:b])
        print("cite %-4s %-42s:%d-%d  %s" % (tag, rel.rsplit("/", 1)[-1], a, b,
                                             shown[:150]))
        print("     receipt=%s sha256=%s lines=%d"
              % (rel, sha256(read(pins.repo, rel)), len(lines)))


def check_anchors(pins, bullet, tag):
    """Multi-word quoted spans must land inside a range the same bullet cites."""
    cites = {}
    for name, a, b in locators(bullet):
        rel, _ = pins.lines(name)
        if rel:
            cites.setdefault(rel, []).append((a, b))
    spans = [s for s in BT_RE.findall(bullet) + DQ_RE.findall(bullet)
             if " " in norm(s) and len(norm(s)) >= 12
             and not s.strip().startswith((".ufo/", "http"))]
    if not spans:
        return
    for span in spans:
        n = norm(span)
        hits, miss = [], []
        for rel, ranges in cites.items():
            text = norm("\n".join(pins.lines(rel)[1]))
            flat, idx = [], []
            pos = 0
            for ln, line in enumerate(pins.lines(rel)[1], 1):
                flat.append(norm(line))
                idx.append(ln)
            # line-local search, plus one joined search for spans split over a line
            local = [idx[i] for i, f in enumerate(flat) if n in f]
            whole = norm("\n".join(pins.lines(rel)[1]))
            joined = None
            k = whole.find(n)
            if k >= 0:
                joined = whole.count("\n", 0, k) + 1
            land = local or ([joined] if joined else [])
            hit = [L for L in land if any(a <= L <= b for a, b in ranges)]
            if hit:
                hits.append((rel, hit))
            elif land:
                miss.append((rel, land))
        if hits:
            rel, land = hits[0]
            print("anchor %-4s %-38s -> %s:%s cited OK"
                  % (tag, n[:38], rel.rsplit("/", 1)[-1], land[:4]))
        elif miss:
            rel, land = miss[0]
            fail("%s anchor %r sits at %s:%s, outside every range the bullet cites"
                 % (tag, n[:60], rel, land[:4]))
        else:
            entry_hits = [i for i, l in enumerate(landed_lines(pins.repo), 1)
                          if n.lower() in norm(l).lower()]
            refs = [int(x) for x in ENTRY_REF_RE.findall(bullet)]
            if entry_hits and any(h in refs for h in entry_hits):
                print("anchor %-4s %-38s -> entry:%s cited OK (entry quote)"
                      % (tag, n[:38], entry_hits[:4]))
            elif entry_hits:
                fail("%s span %r sits at entry:%s, not at the entry lines the bullet cites"
                     % (tag, n[:50], entry_hits[:4]))
            else:
                print("info %-6s %-38s absent from pins and entry (negative claim)"
                      % (tag, n[:38]))


def support_tokens(bullet):
    toks = set()
    for loc in LOC_RE.finditer(bullet):
        if loc.group("file"):
            toks.add("%s:%d" % (loc.group("file"), int(loc.group("a"))))
    for s in BT_RE.findall(bullet):
        toks.add(norm(s))
    for h in HEX_RE.findall(bullet):
        toks.add(h[:7])
    toks.update(DEC_RE.findall(bullet))
    for w in WORD_RE.findall(bullet):
        if w.lower() not in STOP:
            toks.add(w)
    return toks


def check_receipt_lines(repo, bullet, tag):
    ok = True
    paths = [(m.start(), m.group(1)) for m in RECEIPT_PATH_RE.finditer(bullet)]
    for m in RECEIPT_REF_RE.finditer(bullet):
        n = int(m.group(1))
        path = next((p for pos, p in reversed(paths)
                     if pos < m.start() and _line_ok(repo, p, n)), None)
        if path is None:
            fail("%s claims receipt line %d but no receipt the bullet names has it"
                 % (tag, n))
            ok = False
            continue
        line = lines_of(read(repo, path))[n - 1]
        flat = norm(line)
        low = flat.lower()
        hits = [norm(t) for t in support_tokens(bullet)
                if norm(t) and (norm(t) in flat or norm(t).lower() in low)]
        if hits:
            print("receipt %-2s %s:%d support=%s" % (tag, path.rsplit("/", 1)[-1], n,
                                                     hits[:4]))
        print("           %3d| %s" % (n, line[:170]))
    return ok


def _line_ok(repo, path, n):
    try:
        ls = lines_of(read(repo, path))
    except OSError:
        return False
    return 1 <= n <= len(ls)


def check_entry_lines(repo, bullet, tag):
    entry = lines_of(read(repo, ENTRY))
    ok = True
    for n in ENTRY_REF_RE.findall(bullet):
        n = int(n)
        if not 1 <= n <= len(entry):
            fail("%s cites entry line %d, the entry has %d lines" % (tag, n, len(entry)))
            ok = False
            continue
        line = entry[n - 1]
        flat = norm(line)
        low = flat.lower()
        hits = []
        for t in sorted(support_tokens(bullet)):
            t2 = norm(t)
            if not t2:
                continue
            if t2 in flat or (len(t2) >= 5 and t2.lower() in low):
                hits.append(t2)
        if hits:
            print("entry %-4s line %-4d support=%s" % (tag, n, hits[:4]))
        else:
            fail("%s cites entry line %d but no token of the bullet occurs there" % (tag, n))
            ok = False
        print("      %4d| %s" % (n, line[:170]))
    return ok


def grep_count(lines, needle, substr=True):
    return [i for i, l in enumerate(lines, 1)
            if (needle in l if substr else re.search(needle, l))]


def check_negatives(pins):
    ok = True
    rel, mon = pins.lines("Hyprland-Monitor.cpp")
    emit = grep_count(mon, "monitor.added.emit")
    good = emit == [389]
    print("neg  monitor.added.emit in %s -> lines %s (want [389]) %s"
          % (rel, emit, "OK" if good else "MISS"))
    ok &= good
    if not good:
        fail("monitor.added.emit not uniquely at Hyprland-Monitor.cpp:389")
    total = 0
    for name in ("Hyprland-Monitor.cpp", "Hyprland-MonitorState.cpp",
                 "Hyprland-Parser.cpp", "Hyprland-legacy-ConfigManager.cpp",
                 "Hyprland-MonitorRuleManager.cpp", "Hyprland-macros.hpp",
                 "Hyprland-HyprCtl.cpp", "Hyprland-legacy-ConfigManager.cpp"):
        rel2, ls = pins.lines(name)
        hits = grep_count(ls, "monitor.added.emit")
        total += len(hits)
        print("     %-38s emits at %s" % (name, hits))
    for name in ("aqua-Wayland-v0.15.1.cpp", "aqua-Headless-v0.15.1.cpp",
                 "aqua-Output-v0.15.1.cpp"):
        rel2, ls = pins.lines(name)
        hits = grep_count(ls, "description")
        good = hits == []
        print("neg  %-34s 'description' occurrences=%s (want none) %s"
              % (name, hits, "OK" if good else "MISS"))
        ok &= good
        if not good:
            fail("%s sets a description" % name)
        hits = grep_count(ls, "createOutput")
        print("     %-34s createOutput at %s" % (name, hits))
    rel2, drm = pins.lines("aqua-DRM-v0.15.1.cpp")
    assign = grep_count(drm, "output->description = ")
    good = assign == [2101]
    print("neg  %s assigns output->description at %s (want [2101]) %s"
          % (rel2.rsplit("/", 1)[-1], assign, "OK" if good else "MISS"))
    ok &= good
    if not good:
        fail("DRM description assignment not at 2101")
    rel2, maincfg = pins.lines("hyprland-main-cfg-a9902ea.cpp")
    legacy = grep_count(maincfg, "Legacy")
    lua = grep_count(maincfg, "makeUnique<Lua::CConfigManager>")
    good = legacy == [] and lua == [30, 33]
    print("neg  %s Legacy=%s Lua instantiations=%s (want [] and [30,33]) %s"
          % (rel2.rsplit("/", 1)[-1], legacy, lua, "OK" if good else "MISS"))
    ok &= good
    if not good:
        fail("src/config/ConfigManager.cpp still selects a legacy manager")
    rel2, hpp = pins.lines("hyprland-ConfigManager-hpp-a9902ea.hpp")
    enum = grep_count(hpp, "enum eConfigManagerType")
    luaenum = grep_count(hpp, "CONFIG_LUA")
    oldenum = grep_count(hpp, "CONFIG_LEGACY")
    good = enum == [27] and luaenum == [28] and oldenum == []
    print("neg  %s enum at %s CONFIG_LUA at %s CONFIG_LEGACY at %s (want [27],[28],[]) %s"
          % (rel2.rsplit("/", 1)[-1], enum, luaenum, oldenum, "OK" if good else "MISS"))
    ok &= good
    if not good:
        fail("ConfigManager.hpp at a9902ea is not the post-removal header")
    return ok


def check_facts(repo, pins, tool_rev):
    ok = True
    blob = read(repo, ENTRY)
    text = blob.decode("utf-8", "replace")
    cut = text.find("\n\n## Errata")
    prefix = blob if cut < 0 else text[:cut + 1].encode()
    good = sha256(prefix) == ENTRY_SHA
    print("fact entry %s landed-prefix sha256=%s want=%s (%s) %s"
          % (ENTRY, sha256(prefix)[:12], ENTRY_SHA[:12],
             "whole file" if cut < 0 else "up to the Errata heading", "OK" if good else "MISS"))
    ok &= good
    if not good:
        fail("entry bytes differ from the round-45 landed entry")
    j = json.loads(read(repo, COMMIT_JSON).decode())
    facts = (j.get("sha") == COMMIT_SHA
             and j["commit"]["committer"]["date"] == "2026-07-22T16:35:10Z"
             and j["commit"]["message"].strip()
             == "config: remove legacy config support (#15539)"
             and len(j["files"]) == 29)
    rem = [f for f in j["files"]
           if f["filename"] == "src/config/legacy/ConfigManager.cpp"
           and f["status"] == "removed" and f["deletions"] == 2184]
    good = bool(facts and rem)
    print("fact commit %s %s 29 files %s; legacy ConfigManager.cpp removed 2184 deletions %s"
          % (COMMIT_SHA[:12], "OK" if facts else "MISS",
             "OK" if facts else "MISS", "OK" if rem else "MISS"))
    ok &= good
    if not good:
        fail("commit a9902ea facts do not match the block")
    body = read(repo, LEGACY_404)
    good = body == b"404: Not Found"
    print("fact raw legacy file at a9902ea: %r %s" % (body[:20], "OK" if good else "MISS"))
    ok &= good
    if not good:
        fail("raw legacy file is not the 14-byte 404")
    if tool_rev:
        got = git(repo, "show", "%s:%s" % (tool_rev, TOOL))
        good = sha256(got) == TOOL_SHA
        print("fact %s at %s sha256=%s want=%s %s"
              % (TOOL, tool_rev[:12], sha256(got)[:12], TOOL_SHA[:12],
                 "OK" if good else "MISS"))
        ok &= good
        if not good:
            fail("%s at %s is not the landed tool" % (TOOL, tool_rev))
    l1 = lines_of(read(repo, R45_RECEIPT_DRAFT))
    r45 = lines_of(read(repo, R45_RECEIPT_TOOL))
    checks = [("draft receipt line 4 tool sha",
               "c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be" in l1[3]),
              ("draft receipt line 1 names the draft",
               "l1-draft/mado-monitors.py" in l1[0]),
              ("landed receipt line 4 tool sha",
               "2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609" in r45[3]),
              ("landed receipt line 7 AGREE", "verdict=AGREE" in r45[6]),
              ("landed receipt line 8 OK", "verdict=OK" in r45[7]),
              ("landed receipt line 9 exit=0", r45[8].strip() == "exit=0"),
              ("landed receipt line 3 config sha", "69c9d899" in r45[2])]
    for label, good in checks:
        print("fact %-38s %s" % (label, "OK" if good else "MISS"))
        ok &= good
        if not good:
            fail(label)
    return ok


def check_paths(repo, block):
    ok = True
    seen = set()
    pins = Pins(repo)
    for m in re.finditer(r"(?<![\w./-])((?:\.ufo|tools|l1-draft|corpus|src|include)"
                         r"/[A-Za-z0-9_./-]+\.[a-z0-9]+)", block):
        tok = m.group(1)
        if tok in seen:
            continue
        seen.add(tok)
        cands = [tok, ".ufo/waves/round-45/" + tok]
        rel = next((c for c in cands if os.path.exists(os.path.join(repo, c))), None)
        if rel is None:
            rel = pins.find(tok)
        if rel is None:
            fail("path %s cited by the block does not exist in this tree" % tok)
            ok = False
        else:
            print("path %-58s -> %s" % (tok, rel))
    return ok


BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja", "zenn.dev", "qiita.com", "/jp/",
           "/cn/", "t.co/", "bit.ly", "\u65e5\u672c", "\u4e2d\u6587")
CENSUS = ("default_refresh", "refresh_tolerance", "scale_step", "scale_search",
          "json_refresh_decimals", "line_keys")


def check_tripwires(repo, block):
    """The wording constraints of PRED-C2-r45 clause g/h/b/i, checked directly."""
    ok = True
    checks = []
    ids = [m.group(0) for m in re.finditer(r"\b[Ss]\d{3,}\b", block)]
    checks.append(("no source id token (clause g would demand a Gate quote)",
                   ids == [], ids[:4]))
    keys = re.findall(r"\b(%s)\s*[:=]" % "|".join(CENSUS), block)
    checks.append(("no census token with a value (clause h T1)", keys == [], keys[:4]))
    fences = [l for l in block.splitlines() if re.match(r"^\s{0,3}(```|~~~)", l)]
    checks.append(("no fence marker (v2 clause b T3)", fences == [], fences[:2]))
    head = [l for l in block.splitlines()
            if re.match(r"^(source|verified-at|recheck):", l)]
    checks.append(("no source:/verified-at:/recheck: line (clause b)", head == [], head[:2]))
    bad = [b for b in BAD_LOC if b in block.lower()]
    checks.append(("no location marker from BAD_LOC (clause i)", bad == [], bad[:3]))
    entry = read(repo, ENTRY)
    checks.append(("block opens with one blank line then an H2 (H2 shape)",
                   block.startswith("\n## ") and entry.endswith(b"\n"), block[:4]))
    for label, good, seen in checks:
        print("tripwire %-58s %s%s" % (label, "OK" if good else "MISS",
                                       "" if good else " -> %r" % (seen,)))
        ok &= good
        if not good:
            fail("tripwire: " + label)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--block", required=True)
    ap.add_argument("--tool-rev", default="4d22eeb66c2835af8aaa3fac6ad838fa616aa663")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    block = open(args.block, encoding="utf-8").read()
    pins = Pins(repo)
    print("# repo %s" % repo)
    print("# block %s (%d bytes)" % (os.path.abspath(args.block), len(block.encode())))
    check_pin_integrity(repo, pins)
    check_tripwires(repo, block)
    check_paths(repo, block)
    for b in bullets(block):
        tag = re.match(r"- (E\d)", b).group(1)
        print("-- %s" % tag)
        check_citations(pins, b, tag)
        check_anchors(pins, b, tag)
        check_entry_lines(repo, b, tag)
        check_receipt_lines(repo, b, tag)
    check_negatives(pins)
    check_facts(repo, pins, args.tool_rev)
    print("RESULT: checks_failed=%d" % len(FAILS))
    for f in FAILS:
        print("  FAILED: %s" % f)
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
