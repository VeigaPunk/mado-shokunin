#!/usr/bin/env python3
"""PRED-C2-r44-v2 - the gkeep size-request entry is admitted (C2, coverage, sourced; assimilation).

Re-registered BEFORE any round-44 data commit (registration-v2.md), replacing PRED-C2-r44 (frozen at
e2289516a9a857f55cda7be635933e89b931c3da, quality/counters/c2-r44-gkeep-size-request.py), because wave w1 found:
a forged receipt for the held id S164 admitted with the census inverted (w1/CritC2Cheat F2, w1/RevC2Counter F1);
pinned bytes cited under a false URL (CritC2Cheat F3, RevC2Counter F3); prose contradicting the census lines
(CritC2Cheat F4, F5); a registry anchor past the receipt's end (CritC2Cheat F9); claim lines hidden behind the
census prefixes (RevC2Counter F2); and the staged r12 re-pointed to lane ids, or an 18-line quote-only entry,
admitted while holding none of the surfaces the claim names (w1/CritClaimSizing F1). The code is CritC2Cheat's
tightened copy (T1-T4, w1/CritC2Cheat/c2-r44-tightened.py) plus the prefix fix and clause j below; this docstring
replaces every inherited text (CritClaimSizing F4).

Scores one committed revision REV (revision-addressed git reads, ambient GIT_* removed; nothing in the lane is
written). ENTRY = corpus/knowledge/hyprland-gkeep-size-request-r44.md, LESSON = corpus/lessons/round-44.md,
FETCH = .ufo/waves/round-44/fetch/, BASE = 6a1a90528fe533cadee506a9fa3e9d13d15cc41f, DATE = 2026-10-26. PINS
(file name -> sha256 and URL): Hyprland-Window.cpp, Hyprland-XDGShell.cpp (raw.githubusercontent.com/hyprwm/
Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/...), xdg-shell.xml (wayland-protocols tag 1.49),
gdktoplevel-wayland.c (GTK tag 4.24.1), gkeep-ui.py (VeigaPunk/gkeep 133b867); the tables below are part of the
predicate. Fenced code blocks of the entry, README and lesson are removed before any line is matched. The entry
is admitted iff every clause holds:
  a  ENTRY exists at REV and is absent at BASE (present at BASE is a setup error, exit 2);
  b  within its first 20 raw lines, outside fences: >= 4 distinct `source: S###` lines, exactly one
     `verified-at: DATE` and exactly one `recheck:` (ISO date, `NNd` or `on-*`); no such line elsewhere; no
     `S###` token anywhere in the entry that is not a cited id;
  c  every cited id has exactly one Registry row (0-3 leading spaces), 11 cells, status `mined`, a valid recheck
     cell, and used-by listing ENTRY; ids absent at BASE (>= 3) carry opened DATE and a location (last token of
     cell 1) holding `/` and `.`; ids present at BASE keep cells 1-9 byte-equal and every BASE used-by item;
  d  LESSON `## Gate` holds per cited id exactly one column-0 line `GATE <id> receipt=<path> sha256=<hex>
     quote="<q>"` (none outside that section); the receipt is a 100644 file under FETCH at REV with that sha256,
     >= 256 bytes; distinct path, sha256 and quote per id; a receipt whose file name is one of PINS must be at
     FETCH/<name> with exactly the pinned sha256 - held ids included (T1); a new id's receipt must be one of
     PINS; the quote is 3-25 words, occurs exactly once in its receipt's normalized text at word boundaries, also
     with comments removed (C/C++ `//`,`/* */`; `#` in .py/.conf), and in no other cited receipt;
  e  each new id's location occurs in no other row and its last path component and the receipt name contain one
     another; a `Hyprland-` receipt's location starts with the efb50993 raw URL; for every cited id gated on a
     PINS receipt the location is exactly that pin's URL (T2); a new row's anchor cell names the receipt with
     `<name>:<a>[-<b>]` ranges inside the receipt's line count (T4);
  f  corpus/README.md holds exactly one column-0 index row for ENTRY;
  g  per cited id one entry line names that id and no other, carries its Gate quote and the computed locator
     `<receipt name>:<N>` (N = the receipt line where the quote starts); EVERY unfenced line naming a cited id
     (other than its `source:` line) carries that id's quote and locator; only the two exact census lines of h are
     exempt from these line checks (not every line sharing their prefixes);
  h  the Gate receipts include gkeep-ui.py and Hyprland-Window.cpp; from gkeep-ui.py with `#` comments removed
     the counter computes the single `set_default_size(W, H)`, the count N of `set_size_request(` and the single
     `application_id="<ID>"`, and the entry carries `gkeep client default_size=<W>x<H> size_request_calls=<N>
     application_id=<ID>`; from Hyprland-Window.cpp's `void CWindow::sendWindowSize(bool force) {` body (to the
     first following line that is exactly `}`) it counts X = `->setSize(` and Y = `->configure(`, and the entry
     carries `hyprland sendWindowSize xdg_setSize=<X> x11_configure=<Y>`; each verbatim, unfenced, exactly once;
     and no other entry line contradicts them: a `set_size_request(` call when N = 0, a `set_default_size(w, h)`
     other than W, H, an `xdg_setSize=` or `x11_configure=` value other than X, Y (T3);
  i  the Gate has >= 1 `ADMIT <staged path> as ENTRY` and >= 1 `REFUSE <staged path> reason=<>= 4 distinct words
     with a flip word: superseded|until|unless|once|when|if|after>` on distinct staged paths, each
     merge/mado/knowledge/corpus/knowledge/<one of STAGED>; no cited row and no entry line holds a BAD_LOC marker;
     the Gate receipts of the cited ids cover every name in PINS;
  j  surface coverage: for each of the twelve SURFACES (pinned receipt, anchor text that occurs exactly once in it,
     keyword) the counter computes the anchor's line L, and some unfenced entry line outside the first 20 raw
     lines carries a locator `<receipt>:<a>[-<b>]` with a <= L <= b (b = a when absent) and matches the keyword
     (case-insensitive). The twelve: report size (Window.cpp realToReportSize), sendWindowSize, the X11 configure
     branch, onAck (Window.cpp); setSize and the deferred sendConfigure (XDGShell.cpp); the zero-size sentence and
     the ack_configure request (xdg-shell.xml); the configured-size store, the minimum-size constraint and the 0x0
     case (gdktoplevel-wayland.c); gkeep's application_id line (gkeep-ui.py).
Final line: `PRED-C2-r44-v2: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`; exit 0 iff admitted=1/1,
else 1; setup failure exit 2.
Residuals (declared): the pins are the trust root; a true quote at a true locator can stand beside a claim it does
not support, and a decision table naming no id is not bound (w1/CritC2Cheat F1, F6: the non-author reading);
registry cells 3-6 of a new row are not read except the anchor ranges (F8); clause j binds a locator and a
keyword per surface, not the truth of the sentence around them; the census lines are bookkeeping of pinned bytes.
"""
import argparse
import collections
import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import sys

PRED = "PRED-C2-r44-v2"
BASE_DEFAULT = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
ENTRIES = ("corpus/knowledge/hyprland-gkeep-size-request-r44.md",)
LESSON = "corpus/lessons/round-44.md"
FETCH = ".ufo/waves/round-44/fetch/"
OPENED = "2026-10-26"
MIN_RECEIPT = 256
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
ADMIT_RE = re.compile(r"^ADMIT (\S+\.md) as (\S+\.md)\s*$")
REFUSE_RE = re.compile(r"^REFUSE (\S+\.md) reason=(.{20,})$")
BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja", "zenn.dev", "qiita.com", "/jp/",
           "/cn/", "t.co/", "bit.ly", "\u65e5\u672c", "\u4e2d\u6587")
# the receipts the L1 fetched before the wave (fetch/ at the v2 freeze); a NEW
# cited id's receipt must be one of them, byte for byte
PINS = {
    "Hyprland-Window.cpp": "d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded",
    "Hyprland-XDGShell.cpp": "d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0",
    "gdktoplevel-wayland.c": "0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe",
    "gkeep-ui.py": "07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a",
    "xdg-shell.xml": "7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df",
}
# the staged package files of the focus theme (the only paths an ADMIT/REFUSE may name)
PINS_URL = {
    "Hyprland-Window.cpp": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp",
    "Hyprland-XDGShell.cpp": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/XDGShell.cpp",
    "gdktoplevel-wayland.c": "https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c",
    "gkeep-ui.py": "https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py",
    "xdg-shell.xml": "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml",
}
STAGED = {
    "gkeep-geometry-unobservable-r8.md",
    "gkeep-rendered-geometry-chain-r9.md",
    "gkeep-size-rule-application-r10.md",
    "gkeep-observation-route-r11.md",
    "gkeep-client-size-request-r12.md",
    "gkeep-rendered-geometry-record-r13.md",
    "gkeep-rendered-geometry-record-r14.md",
    "gkeep-geometry-never-recorded-r15.md",
    "glyph-and-geometry-r31.md",
    "gkeep-element-rules-r30.md",
}


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                       env=ENV)
    return p.stdout if p.returncode == 0 else None


def show(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def resolve(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if not out:
        raise Setup("unresolved revision %s" % rev)
    return out.decode().strip()


def section(text, title):
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == title
            continue
        if inside:
            out.append(line)
    return out


def unfenced(text):
    out, fenced = [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def registry(blob):
    rows = {}
    for line in section((blob or b"").decode("utf-8", "replace"),
                        "## Registry"):
        m = ROW_RE.match(line)
        if m:
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            rows.setdefault(m.group(1), []).append(cells)
    return rows


def valid_date(s):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        return False
    try:
        datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return False
    return True


def recheck_ok(rc):
    m = RECHECK_RE.match(rc or "")
    if not m:
        return False
    tok = m.group(1)
    return valid_date(tok) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", tok) else True


def ls_mode(repo, rev, path):
    out = git(repo, "ls-tree", rev, "--", path)
    if not out:
        return None
    return out.split()[0].decode()


def looks_html(blob):
    return re.search(rb"<(!doctype|html|body|div|p)\b", blob[:4096], re.I) \
        is not None


def norm_receipt(blob):
    text = blob.decode("utf-8", "replace")
    if looks_html(blob):
        return norm(text)
    return re.sub(r"\s+", " ", text).strip()


def collapse_with_lines(text):
    """(collapsed text, 1-based line number of each collapsed character)."""
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


def quote_at(blob, nq):
    """Line of the first word-bounded occurrence of the normalized quote in a
    non-HTML receipt, 0 for an HTML receipt that holds it word-bounded, None."""
    isw = lambda c: c.isalnum() or c == "_"
    if looks_html(blob):
        text = norm(blob.decode("utf-8", "replace"))
        lines = None
    else:
        text, lines = collapse_with_lines(blob.decode("utf-8", "replace"))
    start = 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return None
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            return lines[k] if lines else 0
        start = k + 1




def occurrences(blob, nq):
    isw = lambda c: c.isalnum() or c == "_"
    if looks_html(blob):
        text = norm(blob.decode("utf-8", "replace"))
    else:
        text = collapse_with_lines(blob.decode("utf-8", "replace"))[0]
    out, start = [], 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return out
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            out.append(k)
        start = k + 1


def strip_comments(text, path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".cpp", ".hpp", ".h", ".cc"):
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        return re.sub(r"//[^\n]*", " ", text)
    if ext in (".py", ".conf"):
        return re.sub(r"#[^\n]*", " ", text)
    return text


def quote_in_code(blob, nq, path):
    flat = re.sub(r"\s+", " ", strip_comments(blob.decode("utf-8", "replace"), path))
    return nq in flat


def all_body_lines_bound(ids, entry_lines, gates, receipts_raw):
    for i in ids:
        gl = gates.get(i, [])
        if len(gl) != 1 or i not in receipts_raw:
            return False
        path, digest, quote = gl[0]
        q = re.sub(r"\s+", " ", quote)
        at = quote_at(receipts_raw[i], q)
        bn = os.path.basename(path)
        for l in entry_lines:
            if not re.search(r"\b%s\b" % i, l):
                continue
            if l.startswith("source:"):
                continue
            if q not in l:
                return False
            if at and ("%s:%d" % (bn, at)) not in l:
                return False
    return True


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def host_census(new_ids, reg_rev, gates, receipts_raw, lines):
    """Clause h (round 44): recompute the two client-side census lines from the pinned receipts."""
    byname = {}
    for i, gl in gates.items():
        if i in receipts_raw and gl and gl[0] is not None and len(gl) == 1:
            byname[os.path.basename(gl[0][0])] = receipts_raw[i]
    if "gkeep-ui.py" not in byname or "Hyprland-Window.cpp" not in byname:
        return False, []
    ui = strip_comments(byname["gkeep-ui.py"].decode("utf-8", "replace"), "gkeep-ui.py")
    sd = re.findall(r"set_default_size\(([0-9]+), ([0-9]+)\)", ui)
    ai = re.findall(r'application_id="([^"]+)"', ui)
    nreq = ui.count("set_size_request(")
    if len(sd) != 1 or len(ai) != 1:
        return False, []
    ui_line = "gkeep client default_size=%sx%s size_request_calls=%d application_id=%s" % (
        sd[0][0], sd[0][1], nreq, ai[0])
    src = byname["Hyprland-Window.cpp"].decode("utf-8", "replace").split("\n")
    try:
        k = src.index("void CWindow::sendWindowSize(bool force) {")
        end = src.index("}", k + 1)
    except ValueError:
        return False, []
    fn = "\n".join(src[k:end + 1])
    hy_line = "hyprland sendWindowSize xdg_setSize=%d x11_configure=%d" % (
        fn.count("->setSize("), fn.count("->configure("))
    want = [ui_line, hy_line]
    ok = all(sum(1 for l in lines if l == w) == 1 for w in want)
    return ok, want


SURFACES = [
    ("Hyprland-Window.cpp", "Vector2D CWindow::realToReportSize() {", r"report size|realToReportSize", "report-size"),
    ("Hyprland-Window.cpp", "void CWindow::sendWindowSize(bool force) {", r"sendWindowSize", "send"),
    ("Hyprland-Window.cpp", "m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});", r"X11|Xwayland", "x11"),
    ("Hyprland-Window.cpp", "void CWindow::onAck(uint32_t serial) {", r"\back", "ack"),
    ("Hyprland-XDGShell.cpp", "uint32_t CXDGToplevelResource::setSize(const Vector2D& size) {", r"setSize", "setsize"),
    ("Hyprland-XDGShell.cpp", "m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);", r"configure", "configure"),
    ("xdg-shell.xml", "If the width or height arguments are zero, it means the client", r"zero", "zero"),
    ("xdg-shell.xml", '<request name="ack_configure">', r"ack_configure", "ack_configure"),
    ("gdktoplevel-wayland.c", "wayland_surface->next_layout.configured_width = width;", r"configur", "gtk-store"),
    ("gdktoplevel-wayland.c", "gdk_surface_constrain_size (&wayland_toplevel->geometry_hints,", r"minimum|constrain", "gtk-constrain"),
    ("gdktoplevel-wayland.c", "saved_size = (width == 0 && height == 0);", r"0x0|zero", "gtk-0x0"),
    ("gkeep-ui.py", 'application_id="org.omarchy.gkeep",', r"application id|application_id", "gkeep-id"),
]


def surfaces_ok(repo, rev, text, name):
    """Clause j: every surface's computed line is cited, with its keyword, outside the header window."""
    raw_lines = text.splitlines()
    body_lines, fenced = [], False
    for k, l in enumerate(raw_lines):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced = not fenced
            continue
        if not fenced and k >= 20:
            body_lines.append(l)
    ok = True
    for rname, anchor, kw, label in SURFACES:
        blob = show(repo, rev, FETCH + rname)
        if blob is None:
            print("%s %s clause=j surface=%s receipt_missing" % (PRED, name, label))
            ok = False
            continue
        rl = blob.decode("utf-8", "replace").split("\n")
        hits = [n for n, l in enumerate(rl, 1) if anchor in l]
        if len(hits) != 1:
            print("%s %s clause=j surface=%s anchor_count=%d" % (PRED, name, label, len(hits)))
            ok = False
            continue
        L = hits[0]
        pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(rname))
        found = False
        for l in body_lines:
            if not re.search(kw, l, re.I):
                continue
            for a, b in pat.findall(l):
                if int(a) <= L <= int(b or a):
                    found = True
        ok &= found
        print("%s %s clause=j surface=%s line=%d cited=%d" % (PRED, name, label, L, found))
    return ok


def score(repo, rev, base, entry, reg_rev, reg_base, lesson, readme):
    name = os.path.basename(entry)
    cl = dict.fromkeys("abcdefghij", 0)
    raw = show(repo, rev, entry)
    text = raw.decode("utf-8", "replace") if raw is not None else ""
    lines = unfenced(text)
    cl["a"] = int(raw is not None)
    # header: only unfenced lines inside the first 20 raw lines count; every
    # source:/verified-at:/recheck: line of the whole entry must sit there
    head, fenced_state, window = [], False, 0
    for k, l in enumerate(text.splitlines()):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced_state = not fenced_state
            continue
        if not fenced_state:
            if k < 20:
                head.append(l)
            elif re.match(r"^(source|verified-at|recheck):", l):
                window += 1
    ids = []
    for line in head:
        m = SRC_RE.match(line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    cited = set(re.findall(r"\b[Ss]\d{3,}\b", "\n".join(lines)))
    ghosts = cited - set(ids)

    def hv(key):
        vals = [l[len(key) + 1:].strip() for l in head
                if l.startswith(key + ":")]
        return vals[0] if len(vals) == 1 else None
    va, rc = hv("verified-at"), hv("recheck")
    cl["b"] = int(len(ids) >= 4 and va == OPENED and recheck_ok(rc)
                  and window == 0 and not ghosts)

    rows_ok = bool(ids)
    new_ids = []
    for i in ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0]) != 11:
            rows_ok = False
            print("%s %s clause=c id=%s rows=%d" % (PRED, name, i, len(rows)))
            continue
        cells = rows[0]
        items = [x.strip() for x in re.split(r"[,;]", cells[10])]
        good = cells[7] == "mined" and entry in items \
            and recheck_ok(cells[9])
        if i in reg_base:
            old = reg_base[i]
            good &= len(old) == 1 and len(old[0]) == 11 \
                and old[0][:9] == cells[:9] and recheck_ok(cells[9]) is not None
            good &= set(x.strip() for x in re.split(r"[,;]", old[0][10])
                        if x.strip() not in ("", "\u2014")) <= set(items)
        else:
            new_ids.append(i)
            loc = cells[1].split()[-1] if cells[1].split() else ""
            good &= cells[8] == OPENED and ("/" in loc and "." in loc)
        rows_ok &= good
        print("%s %s clause=c id=%s new=%d status=%s used=%d ok=%d" % (
            PRED, name, i, i not in reg_base, cells[7], entry in items, good))
    cl["c"] = int(rows_ok and len(new_ids) >= 3)

    glines = unfenced("\n".join(section(lesson, "## Gate")))
    gates = collections.defaultdict(list)
    for line in glines:
        m = GATE_RE.match(line.rstrip("\n"))
        if m:
            gates[m.group(1)].append(m.groups()[1:])
        elif re.match(r"^\s+GATE S\d", line):
            gates["<indented>"].append(None)
    outside = 0
    in_gate = set(glines)
    for line in unfenced(lesson):
        if re.match(r"^GATE S\d", line) and line not in in_gate:
            outside += 1
    d_ok, g_ok = bool(ids), bool(ids)
    receipts, receipts_raw = {}, {}
    seen_paths, seen_sha, seen_quote = set(), set(), set()
    for i in ids:
        good = None
        gl = gates.get(i, [])
        if len(gl) == 1:
            path, digest, quote = gl[0]
            blob = show(repo, rev, path) if path.startswith(FETCH) else None
            pin_ok = PINS.get(os.path.basename(path)) in (None, digest) \
                and (os.path.basename(path) not in PINS
                     or path == FETCH + os.path.basename(path))
            nq = re.sub(r"\s+", " ", quote)
            if (blob is not None and len(blob) >= MIN_RECEIPT and pin_ok
                    and ls_mode(repo, rev, path) == "100644"
                    and hashlib.sha256(blob).hexdigest() == digest
                    and 3 <= len(quote.split()) <= 25
                    and path not in seen_paths and digest not in seen_sha
                    and nq not in seen_quote
                    and quote_at(blob, nq) is not None
                    and len(occurrences(blob, nq)) == 1
                    and quote_in_code(blob, nq, path)):
                good = quote
                receipts[i] = blob.decode("utf-8", "replace")
                receipts_raw[i] = blob
                seen_paths.add(path)
                seen_sha.add(digest)
                seen_quote.add(nq)
        print("%s %s clause=d id=%s gates=%d bound=%d" % (
            PRED, name, i, len(gl), good is not None))
        if good is None:
            d_ok = g_ok = False
    # a quote occurs in its own receipt and in no other cited receipt
    for i in receipts:
        q = re.sub(r"\s+", " ", gates[i][0][2])
        for j in receipts:
            if j != i and q in norm_receipt(receipts_raw[j]):
                d_ok = False
                print("%s %s clause=d quote of %s also in receipt of %s" % (
                    PRED, name, i, j))
    cl["d"] = int(d_ok and not gates.get("<indented>") and outside == 0)

    e_ok = True
    for i in new_ids:
        gl_ = gates.get(i, [])
        cells_ = reg_rev[i][0] if len(reg_rev.get(i, [[]])[0]) == 11 else None
        if cells_ is None or len(gl_) != 1:
            e_ok = False
            continue
        comp = re.split(r"[?#]", cells_[1].split()[-1])[0].rstrip("/") \
            .rsplit("/", 1)[-1].lower()
        rb = os.path.basename(gl_[0][0]).lower()
        e_ok &= bool(comp) and (comp in rb or rb in comp)
        if rb.startswith('hyprland-') and not cells_[1].split()[-1].startswith(
                'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/'):
            e_ok = False
        cells = reg_rev[i][0] if len(reg_rev.get(i, [[]])[0]) == 11 else None
        if cells is None:
            e_ok = False
            continue
        loc = cells[1].split()[-1] if cells[1].split() else ""
        key = loc.split("#")[0]
        same = [j for j, rr in reg_rev.items() for r in rr
                if len(r) == 11 and r[1].split()
                and r[1].split()[-1].split("#")[0] == key]
        e_ok &= bool(loc) and same == [i]
    for i in ids:
        gl_ = gates.get(i, [])
        row_ = reg_rev.get(i, [])
        if len(gl_) == 1 and row_ and len(row_[0]) == 11:
            loc_ = row_[0][1].split()[-1].split("#")[0] if row_[0][1].split() else ""
            pin_url = PINS_URL.get(os.path.basename(gl_[0][0]))
            if pin_url is not None and pin_url.split("#")[0] != loc_:
                e_ok = False
                print("%s %s clause=e+ id=%s location=%s pin=%s" % (
                    PRED, name, i, loc_, pin_url))
    # T4: a new row's anchor must name the receipt it is gated on and stay inside it
    for i in new_ids:
        row_ = reg_rev.get(i, [])
        gl_ = gates.get(i, [])
        if not row_ or len(row_[0]) != 11 or len(gl_) != 1 or i not in receipts_raw:
            e_ok = False
            continue
        rb_ = os.path.basename(gl_[0][0])
        nlines_ = len(receipts_raw[i].decode("utf-8", "replace").splitlines())
        anchor_ = row_[0][5]
        rng = re.findall(r"%s:(\d+)(?:-(\d+))?" % re.escape(rb_), anchor_)
        if not rng or any(int(b or a) > nlines_ for a, b in rng):
            e_ok = False
            print("%s %s clause=e/4 id=%s anchor=%s receipt_lines=%d" % (
                PRED, name, i, anchor_[:70], nlines_))
    cl["e"] = int(e_ok and bool(new_ids))

    h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)
    census_lines = set(census_lines)

    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census_lines
]
    if h_ok:
        joined = "\n".join(census_lines)
        m_ui = re.search(r"default_size=(\d+)x(\d+) size_request_calls=(\d+)", joined)
        m_hy = re.search(r"xdg_setSize=(\d+) x11_configure=(\d+)", joined)
        if not m_ui or not m_hy:
            h_ok = False
        else:
            W0, H0, N0 = m_ui.group(1), m_ui.group(2), int(m_ui.group(3))
            X0, Y0 = int(m_hy.group(1)), int(m_hy.group(2))
            for l in entry_lines:
                if N0 == 0 and re.search(r"set_size_request\s*\(", l):
                    h_ok = False
                    print("%s %s clause=h prose calls set_size_request: %s" % (PRED, name, l[:80]))
                for w, h in re.findall(r"set_default_size\(\s*(\d+)\s*,\s*(\d+)\s*\)", l):
                    if (w, h) != (W0, H0):
                        h_ok = False
                        print("%s %s clause=h prose default size %sx%s != %sx%s" % (
                            PRED, name, w, h, W0, H0))
                for v in re.findall(r"xdg_setSize=(\d+)", l):
                    if int(v) != X0:
                        h_ok = False
                        print("%s %s clause=h prose xdg_setSize=%s != %d" % (PRED, name, v, X0))
                for v in re.findall(r"x11_configure=(\d+)", l):
                    if int(v) != Y0:
                        h_ok = False
                        print("%s %s clause=h prose x11_configure=%s != %d" % (PRED, name, v, Y0))
    cl["h"] = int(h_ok)
    for i in ids:
        quote = None
        for path, digest, q in gates.get(i, []):
            quote = q
        if i not in receipts or quote is None:
            g_ok = False
            continue
        q = re.sub(r"\s+", " ", quote)
        at = quote_at(receipts_raw[i], q)
        base_name = os.path.basename(gates[i][0][0])
        loc_ok = True if at == 0 else (at is not None and
                                       re.search(r"(?<![\w.-])%s:%d(?!\d)" % (re.escape(base_name), at), "\n".join(entry_lines)) is not None)
        hit = any(re.search(r"\b%s\b" % i, l) and q in l
                  and len(set(re.findall(r"\bS\d{3,}\b", l))) == 1
                  and (at == 0 or (at is not None and ("%s:%d" % (base_name, at)) in l
                                   and re.search(r"(?<![\w.-])%s:%d(?!\d)" % (re.escape(base_name), at), l)))
                  for l in entry_lines)
        g_ok &= hit
        print("%s %s clause=g id=%s obs=%d locator_line=%s" % (PRED, name, i, hit, at))
    cl["g"] = int(g_ok and all_body_lines_bound(ids, entry_lines, gates, receipts_raw))

    pat = re.compile(r"^\| `knowledge/%s`" % re.escape(name))
    cl["f"] = int(sum(1 for l in unfenced(readme) if pat.match(l)) == 1)
    admits = [m for m in map(ADMIT_RE.match, glines) if m]
    refuses = [m for m in map(REFUSE_RE.match, glines) if m]
    staged_ok = lambda p: (p == 'merge/mado/knowledge/corpus/knowledge/' + os.path.basename(p)
                           and os.path.basename(p) in STAGED)
    adm = [m for m in admits if m.group(2) == entry and staged_ok(m.group(1))]
    ref = [m for m in refuses if staged_ok(m.group(1))
           and len(set(m.group(2).lower().split())) >= 4
           and all(m.group(1) != a.group(1) for a in adm)
           and re.search(r'\b(superseded|until|unless|once|when|if|after)\b',
                         m.group(2).lower())]
    bad = False
    for i in ids:
        rows = reg_rev.get(i, [])
        if rows and len(rows[0]) == 11:
            row_text = " ".join(rows[0]).lower()
            bad |= any(b_ in row_text for b_ in BAD_LOC)
    used = set(os.path.basename(gates[i][0][0]) for i in receipts)
    bad |= not set(PINS) <= used
    bad |= any(b_ in l.lower() for l in lines for b_ in BAD_LOC)
    cl["i"] = int(bool(adm) and bool(ref) and not bad)
    cl["j"] = int(raw is not None and surfaces_ok(repo, rev, text, name))
    admitted = int(all(cl.values()))
    print("%s %s clauses=%s admitted=%d" % (
        PRED, name, " ".join("%s:%d" % kv for kv in sorted(cl.items())),
        admitted))
    return admitted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    for e in ENTRIES:
        if show(repo, base, e) is not None:
            raise Setup("precondition_failed entry_present_at_base %s" % e)
    reg_rev = registry(show(repo, rev, "corpus/SOURCES.md"))
    reg_base = registry(show(repo, base, "corpus/SOURCES.md"))
    lesson = (show(repo, rev, LESSON) or b"").decode("utf-8", "replace")
    readme = (show(repo, rev, "corpus/README.md") or b"").decode(
        "utf-8", "replace")
    n = sum(score(repo, rev, base, e, reg_rev, reg_base, lesson, readme)
            for e in ENTRIES)
    met = n == 1
    print("%s: admitted=%d/1 verdict=%s rev=%s" % (
        PRED, n, "TARGET_MET" if met else "TARGET_MISSED", rev))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)
