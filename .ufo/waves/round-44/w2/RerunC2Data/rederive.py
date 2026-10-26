#!/usr/bin/env python3
"""Independent re-derivation of the C2 Gate bindings for round 44 at rev e467892.

Deliberately does NOT import quality/counters/c2-r44-gkeep-size-request-v2.py.
Different algorithms: token-run collapsing (not char-wise), regex word-boundary
around the escaped quote, line-oriented comment stripping, own census scan.
Reads git objects read-only through `git show`; writes nothing.
"""
import hashlib
import os
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "e46789213830597348fe96a351ae004d10587385"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
LESSON = "corpus/lessons/round-44.md"
FETCH = ".ufo/waves/round-44/fetch/"
IDS = ["S164", "S298", "S299", "S300", "S301"]
PIN_URL = {
    "Hyprland-Window.cpp": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp",
    "Hyprland-XDGShell.cpp": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/XDGShell.cpp",
    "gdktoplevel-wayland.c": "https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c",
    "gkeep-ui.py": "https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py",
    "xdg-shell.xml": "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml",
}
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


def git(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True, env=env)
    if p.returncode != 0:
        raise SystemExit("git failed: %s\n%s" % (args, p.stderr.decode()))
    return p.stdout


def blob(path):
    return git("show", "%s:%s" % (REV, path))


def collapse(text):
    """Token-run collapse. Returns (flat, line_of_each_char)."""
    out, lines = [], []
    pos = 0
    for m in re.finditer(r"\S+", text):
        if out:
            out.append(" ")
            run_start = pos
            lines.append(text.count("\n", 0, run_start) + 1)
        ln = text.count("\n", 0, m.start()) + 1
        for ch in m.group(0):
            out.append(ch)
            lines.append(ln)
        pos = m.end()
    return "".join(out), lines


def strip_comments(text, path):
    ext = os.path.splitext(path)[1]
    if ext in (".cpp", ".hpp", ".h", ".cc"):
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        text = "\n".join(re.sub(r"//.*$", " ", l) for l in text.split("\n"))
        return text
    if ext in (".py", ".conf"):
        return "\n".join(re.sub(r"#.*$", " ", l) for l in text.split("\n"))
    return text


def main():
    report = []
    add = report.append

    lesson = blob(LESSON).decode("utf-8")
    gate = {}
    for n, line in enumerate(lesson.split("\n"), 1):
        m = re.match(r'^GATE (S\d+) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.*)"\s*$', line)
        if m:
            gate[m.group(1)] = (n, m.group(2), m.group(3), m.group(4))
    add("## Gate lines (corpus/lessons/round-44.md@rev)")
    for i in IDS:
        n, path, sha, quote = gate[i]
        add("- %s  GATE line %d  receipt=%s  declared_sha256=%s  words=%d" % (
            i, n, path, sha, len(quote.split())))

    raw, hashes = {}, {}
    add("\n## Receipt sha256 (git show | sha256sum equivalent)")
    for i in IDS:
        path = gate[i][1]
        b = blob(path)
        raw[i] = b
        h = hashlib.sha256(b).hexdigest()
        hashes[i] = h
        add("- %s  %s  %d B  sha256=%s  match=%s" % (
            i, path, len(b), h, "YES" if h == gate[i][2] else "NO"))

    # HTML heuristic: first 4096 bytes with <!doctype|<html|<body|<div|<p followed by non-word
    add("\n## HTML heuristic on each receipt (affects normalization path)")
    for i in IDS:
        head = raw[i][:4096]
        html_like = re.search(rb"<(doctype|html|body|div|p)\b", head, re.I) is not None
        add("- %s  html_like=%s" % (i, html_like))

    flat = {}
    add("\n## Quote occurrence (token-collapsed text, \\b word boundaries)")
    for i in IDS:
        quote = re.sub(r"\s+", " ", gate[i][3])
        text = raw[i].decode("utf-8")
        f, lines = collapse(text)
        flat[i] = f
        pat = re.compile(r"(?<!\w)" + re.escape(quote) + r"(?!\w)")
        hits = list(pat.finditer(f))
        add("- %s  word-bounded occurrences=%d  substring occurrences=%d  start_line=%s" % (
            i, len(hits), f.count(quote),
            lines[hits[0].start()] if hits else "NONE"))
        if len(hits) == 1:
            ln = lines[hits[0].start()]
            src = text.split("\n")
            add("    receipt line %d: %s" % (ln, src[ln - 1].strip()[:160]))
        # comment-stripped presence
        sc = re.sub(r"\s+", " ", strip_comments(text, gate[i][1]))
        add("    comment-stripped contains quote=%s" % (quote in sc))

    add("\n## Cross-receipt absence (quote of id X inside every other cited receipt)")
    for i in IDS:
        quote = re.sub(r"\s+", " ", gate[i][3])
        others = [j for j in IDS if j != i and quote in flat[j]]
        add("- %s  present_in_other_receipts=%s" % (i, others or "none"))

    entry = blob(ENTRY).decode("utf-8")
    ent_lines = entry.split("\n")
    body = []  # (raw line number, text) unfenced, raw index >= 20
    fenced = False
    for k, l in enumerate(ent_lines):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced = not fenced
            continue
        if not fenced and k >= 20:
            body.append((k + 1, l))
    unfenced_all = []
    fenced = False
    for k, l in enumerate(ent_lines):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced = not fenced
            continue
        if not fenced:
            unfenced_all.append((k + 1, l))

    add("\n## Entry line carrying quote + locator (per id)")
    for i in IDS:
        quote = re.sub(r"\s+", " ", gate[i][3])
        base = os.path.basename(gate[i][1])
        f, lines = collapse(raw[i].decode("utf-8"))
        pat = re.compile(r"(?<!\w)" + re.escape(quote) + r"(?!\w)")
        hits = list(pat.finditer(f))
        at = lines[hits[0].start()] if len(hits) == 1 else None
        rows = []
        for n, l in unfenced_all:
            if re.search(r"\b%s\b" % i, l):
                ids_on = sorted(set(re.findall(r"\bS\d{3,}\b", l)))
                rows.append((n, ids_on, quote in re.sub(r"\s+", " ", l),
                             ("%s:%d" % (base, at)) in l))
        add("- %s  quote_start_line=%s  lines_naming_id=%s" % (i, at, len(rows)))
        for n, ids_on, has_q, has_loc in rows:
            add("    entry:%d ids=%s quote=%s locator=%s" % (n, ids_on, has_q, has_loc))

    add("\n## Lines naming a cited id but not carrying its quote+locator (excluding the 2 census lines)")
    census = ["gkeep client default_size=", "hyprland sendWindowSize xdg_setSize="]
    flagged = 0
    for n, l in unfenced_all:
        if any(l.startswith(c) for c in census):
            continue
        if not re.search(r"\bS\d{3,}\b", l):
            continue
        if l.startswith("source:"):
            continue
        ok = True
        for i in IDS:
            if not re.search(r"\b%s\b" % i, l):
                continue
            q = re.sub(r"\s+", " ", gate[i][3])
            base = os.path.basename(gate[i][1])
            f, lines = collapse(raw[i].decode("utf-8"))
            pat = re.compile(r"(?<!\w)" + re.escape(q) + r"(?!\w)")
            hits = list(pat.finditer(f))
            at = lines[hits[0].start()] if hits else None
            if q not in re.sub(r"\s+", " ", l) or not re.search(r"(?<![\w.-])%s:%d(?!\d)" % (re.escape(base), at), l):
                ok = False
        if not ok:
            flagged += 1
            add("- entry:%d  %s" % (n, l[:150]))
    if not flagged:
        add("- none")

    add("\n## Registry rows (corpus/SOURCES.md@rev, ## Registry)")
    src = blob("corpus/SOURCES.md").decode("utf-8")
    inside, regrows = False, {}
    for n, l in enumerate(src.split("\n"), 1):
        if l.startswith("## "):
            inside = l.strip() == "## Registry"
            continue
        if inside:
            m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", l)
            if m:
                cells = [c.strip() for c in l.strip().split("|")[1:-1]]
                regrows.setdefault(m.group(1), []).append((n, cells))
    for i in IDS:
        rs = regrows.get(i, [])
        if len(rs) != 1:
            add("- %s  rows=%d (EXPECTED 1)" % (i, len(rs)))
            continue
        n, cells = rs[0]
        loc = cells[1].split()[-1] if cells[1].split() else ""
        pin = PIN_URL.get(os.path.basename(gate[i][1]))
        add("- %s  line %d  cells=%d status=%s opened=%s recheck=%s" % (
            i, n, len(cells), cells[7], cells[8], cells[9]))
        add("    location=%s" % loc)
        add("    pin_url=%s  location==pin=%s" % (pin, loc.split("#")[0] == pin))
        add("    used_by lists entry=%s" % (ENTRY in [x.strip() for x in re.split(r"[,;]", cells[10])]))
        same = [j for j, rr in regrows.items() for (_, r) in rr if len(r) == 11
                and r[1].split() and r[1].split()[-1].split("#")[0] == loc.split("#")[0]]
        add("    rows_sharing_location=%s" % same)

    add("\n## Census recomputation (entry lines, not counter helpers)")
    ui = strip_comments(raw["S301"].decode("utf-8"), "gkeep-ui.py")
    sd = re.findall(r"set_default_size\((\d+), (\d+)\)", ui)
    ai = re.findall(r'application_id="([^"]+)"', ui)
    nreq = ui.count("set_size_request(")
    add("- gkeep-ui.py set_default_size=%s application_id=%s set_size_request( count=%d" % (sd, ai, nreq))
    win = raw["S164"].decode("utf-8").split("\n")
    try:
        k = [n for n, l in enumerate(win) if l == "void CWindow::sendWindowSize(bool force) {"]
        add("- sendWindowSize start line(s)=%s" % [x + 1 for x in k])
        st = k[0]
        end = next(n for n in range(st + 1, len(win)) if win[n] == "}")
        fn = "\n".join(win[st:end + 1])
        add("- sendWindowSize body lines %d-%d  ->setSize( =%d  ->configure( =%d" % (
            st + 1, end + 1, fn.count("->setSize("), fn.count("->configure(")))
    except (IndexError, StopIteration):
        add("- sendWindowSize body NOT FOUND")
    want = [
        "gkeep client default_size=%sx%s size_request_calls=%d application_id=%s" % (
            sd[0][0], sd[0][1], nreq, ai[0]),
        "hyprland sendWindowSize xdg_setSize=%d x11_configure=%d" % (
            fn.count("->setSize("), fn.count("->configure(")),
    ]
    for w in want:
        hits = [(n, l) for n, l in unfenced_all if l == w]
        add("- census line %r exact_unfenced_occurrences=%d at %s" % (w, len(hits), [n for n, _ in hits]))

    add("\n## Clause-j surfaces (anchor line, cited range in body, keyword)")
    sur_ok = True
    for rname, anchor, kw, label in SURFACES:
        rl = raw_of = None
        rl = blob(FETCH + rname).decode("utf-8").split("\n")
        hits = [n for n, l in enumerate(rl, 1) if anchor in l]
        if len(hits) != 1:
            add("- %-13s anchor_count=%d  ANCHOR_NOT_UNIQUE" % (label, len(hits)))
            sur_ok = False
            continue
        L = hits[0]
        pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(rname))
        found = []
        for n, l in body:
            if not re.search(kw, l, re.I):
                continue
            for a, b in pat.findall(l):
                if int(a) <= L <= int(b or a):
                    found.append((n, a, b or a))
        add("- %-13s %s anchor_line=%d cited_range=%s ok=%s" % (
            label, rname, L, found or "NONE", bool(found)))
        sur_ok &= bool(found)
    add("- clause-j all_twelve=%s" % sur_ok)

    out = "\n".join(report)
    print(out)
    return 0 if sur_ok else 1


if __name__ == "__main__":
    sys.exit(main())
