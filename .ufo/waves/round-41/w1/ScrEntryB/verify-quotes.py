#!/usr/bin/env python3
"""ScrEntryB verifier - simulates the quote/shape clauses of PRED-C2-r41-v1 on the
draft entry. Read-only; writes nothing. Usage: python3 verify-quotes.py [entry]"""
import html
import re
import sys

ENTRY = (sys.argv[1] if len(sys.argv) > 1 else
         ".ufo/waves/round-41/w1/ScrEntryB/hyprland-focus-grab-r41.md")
FETCH = ".ufo/waves/round-41/fetch/"

GATE = {
    "S283": ("focus-grab-v1.xml",
             "This interface restricts input focus to a specified whitelist of surfaces"),
    "S284": ("Hyprland-FocusGrab.cpp", "m_grab->m_keyboard = true;"),
    "S285": ("quickshell-grab.cpp",
             "the protocol will always send cleared() when the grab is deactivated,"),
    "S286": ("xdph-PortalManager.cpp", "Got interface: {} (ver {})"),
    "S287": ("issue-565.html", "Tried to set workspace silent rule to a nofocus window!"),
    "S288": ("protocols-README.md",
             "for grabbing input focus, primarily for complex context menus"),
    "S289": ("xdph-journal.txt",
             "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
    "S290": ("input-capture-v1.xml", "Add one barrier to the current session"),
}
ADV_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}) (\S+) "
    r"xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver (\d{1,6})\)")
BOOT_RE = re.compile(r"-- Boot ([0-9a-f]{32}) --")
JOURNAL_RE = re.compile(
    r"^journal sessions=(\d+) adverts=(\d+) interfaces=(\d+) focus_grab=(\d+)$")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def unfenced(text):
    out, fenced = [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out, fenced


def journal_counts(blob):
    sessions, changed, cur = [], False, None
    for line in blob.split("\n"):
        if BOOT_RE.fullmatch(line):
            changed = True
            continue
        m = ADV_RE.fullmatch(line)
        if not m:
            continue
        pid, name = m.group(3), m.group(4)
        if cur is None or changed or pid != cur[0]:
            cur = [pid, 0, {}]
            sessions.append(cur)
            changed = False
        cur[1] += 1
        cur[2][name] = cur[2].get(name, 0) + 1
    last = sessions[-1][2]
    return (len(sessions), sum(x[1] for x in sessions), len(last),
            last.get("hyprland_focus_grab_manager_v1", 0))


def main():
    text = open(ENTRY, encoding="utf-8").read()
    lines = text.splitlines()
    body, unclosed = unfenced(text)
    ok = True

    def bad(msg):
        nonlocal ok
        ok = False
        print("FAIL", msg)

    head = lines[:20]
    ids = []
    for line in head:
        m = SRC_RE.match(line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    if len(ids) < 4:
        bad("header source lines: %d" % len(ids))
    if not any(l.strip() == "verified-at: 2026-10-25" for l in head):
        bad("verified-at line")
    rc = [l for l in head if l.startswith("recheck:")]
    if not rc or not RECHECK_RE.match(rc[0][len("recheck:"):].strip()):
        bad("recheck line")
    print("header ids:", " ".join(ids))
    print("lines:", len(lines), "fenced-balanced:", not unclosed)

    for i in ids:
        if i not in GATE:
            bad("%s has no receipt mapping in this verifier" % i)
            continue
        fname, quote = GATE[i]
        blob = open(FETCH + fname, encoding="utf-8", errors="replace").read()
        words = len(quote.split())
        in_receipt = norm(quote) in norm(blob)
        q = re.sub(r"\s+", " ", quote)
        hits = [l for l in body
                if re.search(r"\b%s\b" % i, re.sub(r"\s+", " ", l))
                and q in re.sub(r"\s+", " ", l)]
        if not (3 <= words <= 25):
            bad("%s quote words=%d" % (i, words))
        if not in_receipt:
            bad("%s quote not in receipt %s" % (i, fname))
        if not hits:
            bad("%s quote not on an entry line naming %s" % (i, i))
        print("%-4s %-28s words=%2d receipt=%d entry-line=%d"
              % (i, fname, words, in_receipt, len(hits)))

    # a gate quote must not sit on a line that names a different cited id
    for i in ids:
        fname, quote = GATE[i]
        q = re.sub(r"\s+", " ", quote)
        for l in body:
            n = re.sub(r"\s+", " ", l)
            if q in n:
                others = [j for j in ids if j != i and re.search(r"\b%s\b" % j, n)]
                if others:
                    bad("%s quote shares a line with %s" % (i, ",".join(others)))

    # census line
    census = [l for l in body if JOURNAL_RE.match(l)]
    counts = journal_counts(open(FETCH + "xdph-journal.txt", encoding="utf-8").read())
    if len(census) != 1:
        bad("census lines=%d" % len(census))
    else:
        got = tuple(int(x) for x in JOURNAL_RE.match(census[0]).groups())
        print("census:", census[0], "| parsed:", counts, "| equal:", got == counts)
        if got != counts:
            bad("census mismatch")

    # out-of-province channel guard (clause i applies to registry rows; kept here too)
    for token in ("amgsk.dev", "zhihu", "/zh", "/ja"):
        if token in text:
            bad("forbidden channel token %r in entry" % token)

    # every cited id must appear in the body (not only the header)
    for i in ids:
        if not any(re.search(r"\b%s\b" % i, l) for l in body):
            bad("%s named only in the header" % i)

    print("VERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
