#!/usr/bin/env python3
"""Simulate the parts of PRED-C2-r41-v1 this seat can check before integration.

The real counter reads a committed revision (`git show REV:path`), so it cannot
see an untracked draft. This script re-implements clauses b, g and h over the
draft file with the counter's own regexes (copied verbatim from
quality/counters/c2-r41-focus-entry.py), and re-checks every quote against its
receipt. Clause c/d/e/f/i need the registry rows, the lesson Gate and the
README index, which are other seats' files; they are reported as out of scope.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
ENTRY = os.path.join(HERE, "hyprland-focus-grab-r41.md")

SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
JOURNAL_RE = re.compile(
    r"^journal sessions=(\d+) adverts=(\d+) interfaces=(\d+) focus_grab=(\d+)$")
OPENED = "2026-10-25"

# the GATE quote per id, as fixed by ScrRowsDraft's row block (S037: this seat)
GATES = {
    "S283": "This interface restricts input focus to a specified whitelist of surfaces",
    "S284": "m_grab->m_keyboard = true;",
    "S285": "the protocol will always send cleared() when the grab is deactivated,",
    "S286": "Got interface: {} (ver {})",
    "S287": "Tried to set workspace silent rule to a nofocus window!",
    "S288": "for grabbing input focus, primarily for complex context menus",
    "S289": "Got interface: hyprland_focus_grab_manager_v1 (ver 1)",
    "S037": "%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2",
}
BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja")


def unfenced(text):
    out, fenced = [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def main():
    text = open(ENTRY, encoding="utf-8").read()
    lines = unfenced(text)
    head = text.splitlines()[:20]
    ids = []
    for line in head:
        m = SRC_RE.match(line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))

    def hv(key):
        for line in head:
            if line.startswith(key + ":"):
                return line[len(key) + 1:].strip()
        return None

    va, rc = hv("verified-at"), hv("recheck")
    b = len(ids) >= 4 and va == OPENED and rc is not None \
        and RECHECK_RE.match(rc) is not None
    print("b: ids=%d %s verified-at=%s recheck-ok=%d -> %d"
          % (len(ids), ",".join(ids), va,
             rc is not None and RECHECK_RE.match(rc) is not None, b))

    jm = [m for m in map(JOURNAL_RE.match, lines) if m]
    h_ok = len(jm) == 1 and tuple(int(x) for x in jm[0].groups()) \
        == (2, 78, 63, 1)
    print("h: journal-lines=%d counts=%s -> %d"
          % (len(jm), jm[0].groups() if jm else None, h_ok))

    census = {jm[0].group(0)} if jm else set()
    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census and not l.startswith("journal ")]
    g_ok = True
    for i in ids:
        q = re.sub(r"\s+", " ", GATES.get(i, ""))
        hit = any(re.search(r"\b%s\b" % i, l) and q and q in l
                  for l in entry_lines)
        g_ok &= bool(hit)
        print("g: %s quote-on-id-line=%d" % (i, hit))

    bad = [l for l in lines if any(x in l for x in BAD_LOC)]
    print("i-local: localized-channel strings in entry=%d" % len(bad))
    print("cited ids=%s; new (S283..S289)=%d; held=S037; S290 cited=%d"
          % (",".join(ids), sum(1 for i in ids if i != "S037"),
             int("S290" in ids)))
    ok = b and h_ok and g_ok and not bad and "S290" not in ids
    print("SIMULATED b/g/h -> %s" % ("OK" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
