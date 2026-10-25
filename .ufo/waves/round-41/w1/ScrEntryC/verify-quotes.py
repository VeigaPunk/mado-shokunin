#!/usr/bin/env python3
"""ScrEntryC self-check for the C2 draft: every quote verbatim in its receipt,
one quote per cited id, the census line once, header clauses b, line count.

Reads only .ufo/waves/round-41/fetch/ and this seat's draft. Writes nothing.
norm() and the census regex are copied from quality/counters/c2-r41-focus-entry.py
so a quote that passes here passes the counter's clause d/g normalisation.
"""
import html
import re

FETCH = ".ufo/waves/round-41/fetch/"
ENTRY = ".ufo/waves/round-41/w1/ScrEntryC/hyprland-focus-grab-r41.md"
QUOTES = {
    "S283": ("focus-grab-v1.xml",
             "This interface restricts input focus to a specified whitelist of surfaces"),
    "S284": ("Hyprland-FocusGrab.cpp", "m_grab->m_keyboard = true;"),
    "S285": ("quickshell-grab.cpp",
             "the protocol will always send cleared() when the grab is deactivated,"),
    "S286": ("xdph-PortalManager.cpp", "Got interface: {} (ver {})"),
    "S287": ("issue-565.html", "Tried to set workspace silent rule to a nofocus window!"),
    "S288": ("protocols-README.md",
             "for grabbing input focus, primarily for complex context menus"),
    "S289": ("xdph-journal.txt", "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
}
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
JOURNAL_RE = re.compile(
    r"^journal sessions=(\d+) adverts=(\d+) interfaces=(\d+) focus_grab=(\d+)$")
ADV_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}) (\S+) "
    r"xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver (\d{1,6})\)")
BOOT_RE = re.compile(r"-- Boot ([0-9a-f]{32}) --")


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


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
    if not sessions:
        return None
    total = sum(x[1] for x in sessions)
    last = sessions[-1][2]
    return (len(sessions), total, len(last),
            last.get("hyprland_focus_grab_manager_v1", 0))


def main():
    text = open(ENTRY, encoding="utf-8").read()
    lines = text.splitlines()
    head = lines[:20]
    ids = [SRC_RE.match(l).group(1) for l in head if SRC_RE.match(l)]
    print("lines=%d sources_in_head=%s" % (len(lines), ",".join(ids)))
    rc = [l[len("recheck:"):].strip() for l in head if l.startswith("recheck:")]
    print("clause_b verified-at=%s recheck=%s ok=%s" % (
        any(l.strip() == "verified-at: 2026-10-25" for l in head),
        bool(rc and RECHECK_RE.match(rc[0])),
        len(set(ids)) >= 4 and any(l.strip() == "verified-at: 2026-10-25"
                                   for l in head)
        and bool(rc and RECHECK_RE.match(rc[0]))))
    census = [l for l in lines if l.startswith("journal ")]
    jm = [m for m in map(JOURNAL_RE.match, lines) if m]
    journal = open(FETCH + "xdph-journal.txt", encoding="utf-8",
                   errors="replace").read()
    jc = journal_counts(journal)
    print("clause_h census_lines=%d matches=%d computed=%s entry=%s ok=%s" % (
        len(census), len(jm), jc,
        tuple(int(x) for x in jm[0].groups()) if len(jm) == 1 else None,
        len(jm) == 1 and tuple(int(x) for x in jm[0].groups()) == jc
        and jc[0] >= 2 and jc[1] >= 40 and jc[2] >= 20 and jc[3] >= 1))
    ok = True
    for i in sorted(QUOTES):
        f, q = QUOTES[i]
        qn = re.sub(r"\s+", " ", q)
        body = norm(open(FETCH + f, encoding="utf-8", errors="replace").read())
        hit = [l for l in lines
               if re.search(r"\b%s\b" % i, l) and qn in re.sub(r"\s+", " ", l)
               and not l.startswith("journal ")]
        good = qn in body and len(hit) == 1 and 3 <= len(qn.split()) <= 25
        ok &= good
        print("clause_dg id=%s receipt=%s words=%d in_receipt=%s entry_lines=%d ok=%s"
              % (i, f, len(qn.split()), qn in body, len(hit), good))
    print("ALL_QUOTES_OK=%s cited=%s" % (ok, ",".join(sorted(QUOTES))))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
