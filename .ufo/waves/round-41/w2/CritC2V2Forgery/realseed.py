#!/usr/bin/env python3
"""CritC2V2Forgery (w2): forgeries applied to the REAL round-41 data.

Same fixture construction as `.ufo/waves/round-41/ctl/run-c2-v2-controls.py`
(mktemp -d, git init, -C everywhere, throwaway identity via -c, toplevel checked
by the control's own commit_all/score), but the base is the real base commit's
corpus/SOURCES.md + corpus/README.md and the after tree is the real DATA commit
(07f2641) with exactly one forgery applied.  Scored by the counter as frozen at
that commit.  Read-only against the lane.
"""
import hashlib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import forge  # noqa: E402

ctl = forge.ctl
LANE = forge.LANE
DATA, BASE = forge.DATA, forge.BASE
ENTRY, SRC, LES, FETCH = forge.ENTRY, forge.SRC, forge.LES, forge.FETCH
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
RECEIPTS = ("Hyprland-FocusGrab.cpp", "Hyprland-FocusGrab.hpp", "focus-grab-v1.xml",
            "input-capture-v1.xml", "issue-565.html", "protocols-README.md",
            "quickshell-grab.cpp", "xdph-PortalManager.cpp", "xdph-journal.txt",
            "xdph-installed-version.txt")
FILLER = ctl.FILLER


def show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                       capture_output=True, env=ENV)
    if p.returncode != 0:
        raise SystemExit("missing %s:%s" % (rev, path))
    return p.stdout


BASE_FILES = {SRC: show(BASE, SRC), "corpus/README.md": show(BASE, "corpus/README.md")}


def real_after():
    g = {SRC: show(DATA, SRC), ENTRY: show(DATA, ENTRY), LES: show(DATA, LES),
         "corpus/README.md": show(DATA, "corpus/README.md")}
    for fn in RECEIPTS:
        g[FETCH + fn] = show(DATA, FETCH + fn)
    return g


def dec(g, k):
    v = g[k]
    return v.decode() if isinstance(v, bytes) else v


def enc(g, k, s):
    g[k] = s.encode() if isinstance(g[k], bytes) else s


def gate_line(g, i):
    return [l for l in dec(g, LES).splitlines() if l.startswith("GATE %s " % i)][0]


def set_gate(g, i, path, data, quote):
    old = gate_line(g, i)
    new = ctl.gate_line(i, path, data if isinstance(data, bytes) else data.encode(), quote)
    enc(g, LES, dec(g, LES).replace(old, new))


def row_of(g, i):
    for line in dec(g, SRC).splitlines():
        m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
        if m and m.group(1) == i:
            return line
    raise KeyError(i)


# --------------------------------------------------------------------------
def fa_real(g):
    """S283's XML quote cited as what Hyprland 0.56.2 does at the seat."""
    enc(g, ENTRY, dec(g, ENTRY).replace(
        "**OBS** S283 (`hyprland_focus_grab_v1`, the grab interface's description):",
        "**OBS** S283 (Hyprland 0.56.2's seat enforcement, measured this round):"))


def fb_real(g):
    """S286's log-call quote on an inference it does not support (the portal binds it)."""
    enc(g, ENTRY, dec(g, ENTRY).replace(
        "**OBS** S286 (`src/core/PortalManager.cpp`, `CPortalManager::onGlobal`, "
        "lines 85-261): every global is logged before any branch, with",
        "**OBS** S286 (`src/core/PortalManager.cpp`, `CPortalManager::onGlobal`, "
        "lines 85-261): the portal binds the focus-grab manager and hands it to "
        "every client, logging it first with"))


def swap(g):
    """S283 <-> S284: registry rows, Gate lines, source lines and entry lines."""
    ra, rb = row_of(g, "S283"), row_of(g, "S284")
    na = re.sub(r"^\s*\|\s*S283\s*\|", "| S283 |", ra, count=1)
    nb = re.sub(r"^\s*\|\s*S284\s*\|", "| S284 |", rb, count=1)
    # swap the payload cells 1..9, keep id / status / opened / recheck / used-by
    ca = [c.strip() for c in ra.strip().split("|")[1:-1]]
    cb = [c.strip() for c in rb.strip().split("|")[1:-1]]
    ca2 = [ca[0]] + cb[1:10] + ca[10:]
    cb2 = [cb[0]] + ca[1:10] + cb[10:]
    na = "| " + " | ".join(ca2) + " |"
    nb = "| " + " | ".join(cb2) + " |"
    enc(g, SRC, dec(g, SRC).replace(ra, "@@A@@").replace(rb, "@@B@@")
        .replace("@@A@@", na).replace("@@B@@", nb))
    qa = 'This interface restricts input focus to a specified whitelist of surfaces'
    qb = 'm_grab->m_keyboard = true;'
    set_gate(g, "S283", FETCH + "Hyprland-FocusGrab.cpp", g[FETCH + "Hyprland-FocusGrab.cpp"], qb)
    set_gate(g, "S284", FETCH + "focus-grab-v1.xml", g[FETCH + "focus-grab-v1.xml"], qa)
    e = dec(g, ENTRY)
    e = e.replace("**OBS** S283 (`hyprland_focus_grab_v1`, the grab interface's "
                  "description): \"%s\"" % qa, "@@EA@@")
    e = e.replace("**OBS** S284 (`src/protocols/FocusGrab.cpp`, `CFocusGrab::CFocusGrab`): "
                  "\"%s\"" % qb, "@@EB@@")
    e = e.replace("@@EA@@", "**OBS** S283 (`src/protocols/FocusGrab.cpp`, "
                  "`CFocusGrab::CFocusGrab`): \"%s\"" % qb)
    e = e.replace("@@EB@@", "**OBS** S284 (`hyprland_focus_grab_v1`, the grab "
                  "interface's description): \"%s\"" % qa)
    enc(g, ENTRY, e)


def swap_consistent(g):
    """the same swap with the source: lines swapped too, so the id->file naming
    is internally consistent"""
    swap(g)
    e = dec(g, ENTRY)
    a = [l for l in e.splitlines() if l.startswith("source: S283 ")][0]
    b = [l for l in e.splitlines() if l.startswith("source: S284 ")][0]
    ta = a.split(" - ", 1)[1]
    tb = b.split(" - ", 1)[1]
    e = e.replace(a, "@@SA@@").replace(b, "source: S283 - " + tb).replace("@@SA@@", "source: S284 - " + ta)
    enc(g, ENTRY, e)


def fd_real(g):
    """ADMIT names focus-grab-mouse-target-r11, which the entry does not assimilate."""
    enc(g, LES, dec(g, LES).replace(
        "ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md",
        "ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-mouse-target-r11.md"))


def fe_real(g):
    """90 invented lines of uncited prose around the real quoted lines."""
    pad = "\n".join("The seat manager forwards pointer motion %d to the grab's "
                    "owner and never to a non-member surface." % k for k in range(90))
    enc(g, ENTRY, dec(g, ENTRY).replace("\n## §6 The decision table", pad + "\n\n## §6 The decision table"))


JP = ("Hyprland の フォーカス グラブ ホワイトリスト\n\n"
      "この記事は日本語で書かれた解説です。コンポジタはクライアントのサーフェス集合に"
      "フォーカスを制限します。日本語のドキュメントは PROVINCE.md の範囲外です。\n"
      "フォーカス グラブ ホワイトリスト は Hyprland の独自プロトコルです。\n"
      "フォーカス グラブ ホワイトリスト は 独自 の プロトコル です。\n")


def ff_real(g):
    """The held row S037 keeps its neutral GitHub URL; the receipt's bytes are a
    Japanese localized document."""
    body = (JP + "\n" + FILLER).encode()
    g[FETCH + "xdph-installed-version.txt"] = body
    set_gate(g, "S037", FETCH + "xdph-installed-version.txt", body,
             "フォーカス グラブ ホワイトリスト は 独自 の プロトコル です")
    e = dec(g, ENTRY)
    old = [l for l in e.splitlines() if l.startswith("**OBS** S037 ")][0]
    e = e.replace(old, "**OBS** S037 (installed package record, read-only file read): "
                  "\"フォーカス グラブ ホワイトリスト は 独自 の プロトコル です\" - "
                  "the localized upstream documentation for the installed portal.")
    enc(g, ENTRY, e)


def fg_real(g):
    """S037's receipt invented from scratch (held ids are not pinned)."""
    q = "the portal binds hyprland_focus_grab_manager_v1 for every client"
    body = ("Release notes for xdg-desktop-portal-hyprland v1.4.1. %s. %s\n" % (q, FILLER)).encode()
    g[FETCH + "xdph-installed-version.txt"] = body
    set_gate(g, "S037", FETCH + "xdph-installed-version.txt", body, q)
    e = dec(g, ENTRY)
    old = [l for l in e.splitlines() if l.startswith("**OBS** S037 ")][0]
    e = e.replace(old, "**OBS** S037 (release notes): \"%s\"." % q)
    enc(g, ENTRY, e)


def fh_real(g):
    """the pinned journal cited for a claim it does not support"""
    e = dec(g, ENTRY)
    e = e.replace(
        "journal sessions=2 adverts=78 interfaces=63 focus_grab=1",
        "**OBS** S289 both portal sessions advertise hyprland_focus_grab_manager_v1 "
        "once each; the first session carries it at version 1.\n"
        "journal sessions=2 adverts=78 interfaces=63 focus_grab=1")
    enc(g, ENTRY, e)


def fg2_real(g):
    """an invented citation the ghost scan cannot see"""
    e = dec(g, ENTRY)
    e = e.replace("\n## §6 The decision table",
                  "\n**OBS** S999a the seat manager forwards pointer motion to the "
                  "grab's owner.\n\n## §6 The decision table")
    enc(g, ENTRY, e)


FORGERIES = [
    ("RA-real-xml-quote-as-compositor-behaviour", fa_real),
    ("RB-real-true-quote-false-inference", fb_real),
    ("RC-real-swap-ids-naive", swap),
    ("RC2-real-swap-ids-consistent", swap_consistent),
    ("RD-real-admit-wrong-staged-file", fd_real),
    ("RE-real-ninety-percent-prose", fe_real),
    ("RF-real-localized-rehost-held-S037", ff_real),
    ("RG-real-fabricated-held-receipt-S037", fg_real),
    ("RH-real-pinned-journal-unsupported-claim", fh_real),
    ("RG2-real-ghost-token-S999a", fg2_real),
]


def nf4_real(g):
    """NEGATIVE: the census line overstates the journal by one advert (clause h)."""
    enc(g, ENTRY, dec(g, ENTRY).replace("adverts=78", "adverts=79"))


def nf5_real(g):
    """NEGATIVE: the entry cites an id with no registry row (clause c)."""
    enc(g, ENTRY, dec(g, ENTRY).replace("source: S289 - own-work:",
                                        "source: S291 - own-work:"))


NEGATIVES = [("RN1-journal-census-off-by-one", nf4_real),
             ("RN2-cited-id-without-row", nf5_real)]


def main():
    G = real_after()
    rc, last, cls = ctl.score(BASE_FILES, G, "real")
    print("P-real-seed rc=%d %s clauses=%s" % (rc, last, cls))
    out = {}
    for name, fn in FORGERIES:
        g = {k: (v if isinstance(v, bytes) else v) for k, v in G.items()}
        fn(g)
        rc, last, cls = ctl.score(BASE_FILES, g, "real")
        out[name] = g
        print("FORGERY %-42s %-9s rc=%d observed=%s clauses=%s" % (
            name, "ADMITTED" if (rc == 0 and "admitted=1/1" in last) else "rejected",
            rc, last, cls))
    for name, fn in NEGATIVES:
        g = {k: v for k, v in G.items()}
        fn(g)
        rc, last, cls = ctl.score(BASE_FILES, g, "real")
        print("NEGATIVE %-42s %-9s rc=%d observed=%s clauses=%s" % (
            name, "rejected" if rc == 1 else "ADMITTED", rc, last, cls))
    # T1 on the real-seeded set (the real entry's source prose names its files)
    print("\n== T1 (source line names receipt/location component) on the real seed")
    forge.t1_source_line_names_receipt(G, "P-real-seed")
    for n in ("RC-real-swap-ids-naive", "RC2-real-swap-ids-consistent"):
        forge.t1_source_line_names_receipt(out[n], n)
    print("\n== T3' (CJK-only receipt scan) on the real seed")
    for label, g in (("P-real-seed", G),
                     ("RF-real-localized-rehost-held-S037", out["RF-real-localized-rehost-held-S037"]),
                     ("RG-real-fabricated-held-receipt-S037", out["RG-real-fabricated-held-receipt-S037"])):
        les = dec(g, LES)
        bad = []
        for l in les.splitlines():
            m = re.match(r'^GATE (S\d{3,}) receipt=(\S+) ', l)
            if not m:
                continue
            data = g.get(m.group(2))
            if data is None:
                continue
            text = (data.decode("utf-8", "replace") if isinstance(data, bytes) else data)
            n = forge.cjk(text)
            if n >= 8:
                bad.append((m.group(1), n))
        print("T3' %-42s cjk-failing=%s" % (label, bad))
    print("\n== T2 (every ADMIT path must occur in the entry's assimilated-from line)")
    def t2(entry, les):
        ad = re.findall(r"^ADMIT (\S+\.md) as ", les, re.M)
        m = [l for l in entry.splitlines() if l.startswith("assimilated-from:")]
        return (bool(m) and all(p in m[0] for p in ad)), len(ad)
    for label, g in (("P-real-seed", G),
                     ("RD-real-admit-wrong-staged-file", out["RD-real-admit-wrong-staged-file"]),
                     ("control-P-fixture", forge.admitted())):
        ok, n = t2(dec(g, ENTRY), dec(g, LES))
        print("T2 %-42s admits=%d bound=%s" % (label, n, ok))
    print("\n== T4 (pin the held receipt too) on the real seed")
    genuine = show(DATA, FETCH + "xdph-installed-version.txt")
    patched = "/tmp/tmp.sBh6GeCxAU/c2-v2-pinall-real.py"
    src = open(forge.COUNTER).read()
    src = src.replace("PINS = {\n", 'PINS = {\n    "xdph-installed-version.txt": "%s",\n'
                      % hashlib.sha256(genuine).hexdigest(), 1)
    # drop clause d's held-id exemption: every cited id's receipt must be pinned
    guard = ("            pin_ok = True\n"
             "            if i in new_ids:\n"
             "                pin_ok = PINS.get(os.path.basename(path)) == digest \\\n"
             "                    and path == FETCH + os.path.basename(path)\n")
    assert guard in src, "guard not found"
    src = src.replace(guard,
                      "            pin_ok = PINS.get(os.path.basename(path)) == digest \\\n"
                      "                and path == FETCH + os.path.basename(path)\n", 1)
    open(patched, "w").write(src)
    saved = ctl.COUNTER
    ctl.COUNTER = patched
    try:
        for label, g in (("P-real-seed", G),
                         ("RF-real-localized-rehost-held-S037", out["RF-real-localized-rehost-held-S037"]),
                         ("RG-real-fabricated-held-receipt-S037", out["RG-real-fabricated-held-receipt-S037"])):
            rc, last, cls = ctl.score(BASE_FILES, g, "real")
            print("T4 %-42s rc=%d %s clauses=%s" % (label, rc, last, cls))
    finally:
        ctl.COUNTER = saved
    return 0


if __name__ == "__main__":
    sys.exit(main())
