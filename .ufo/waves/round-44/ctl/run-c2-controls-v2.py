#!/usr/bin/env python3
"""Round-44 C2 controls v2 (registration-v2.md) for PRED-C2-r44-v2.

P   the L1 positive control: l1-draft/build-pos.py applied at the freeze (entry, rows S298-S301, S164 used-by,
    lesson Gate with ADMIT/REFUSE, README row) - must be admitted;
then do-nothing / near-do-nothing / forged variants, each built in a throwaway clone under --work
(git clone --shared; every git call names -C <clone>; the fixture identity is used only inside the clone,
verified by rev-parse --show-toplevel) - none may be admitted:
  C2-BASE            the base revision;
  STAGED-COPY        the staged r12 file verbatim at the entry path (+ README row, ADMIT/REFUSE lesson);
  SHELL              header + correct census lines only;
  R12-REPOINT        w1/CritClaimSizing/controls/entry-r12-repoint.md on P's rows/lesson/README;
  MINIMAL-QUOTES     w1/CritClaimSizing/controls/entry-minimal.md on P's rows/lesson/README;
  HIDDEN-LINE        P plus a line `gkeep client follow-up: per S164 ...` without quote/locator (w1/RevC2Counter F2);
  FORGED-PIN         P with fetch/Hyprland-Window.cpp replaced by a doctored copy whose sendWindowSize body has no
                     setSize call, the S164 Gate sha256 and the census line recomputed to match (w1/CritC2Cheat F2);
  FALSE-URL          P with S301's location rewritten to https://example.com/docs/ui.py (w1/RevC2Counter F3);
  PROSE-SIZE-REQUEST P plus a line asserting `set_size_request(420, 500)` (w1/CritC2Cheat F4);
  ANCHOR-PAST-EOF    P with S300's anchor ranges moved past the receipt's end (w1/CritC2Cheat F9).
Usage: run-c2-controls-v2.py --repo LANE --freeze FREEZE --base BASE --work SCRATCHDIR"""
import argparse, hashlib, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
LESSON = "corpus/lessons/round-44.md"
FETCH = ".ufo/waves/round-44/fetch/"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def g(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, env=ENV)


def clone(repo, rev, work, name):
    d = os.path.join(work, name)
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", repo, d], check=True, env=ENV)
    assert g(d, "rev-parse", "--show-toplevel").stdout.strip() == os.path.realpath(d)
    assert g(d, "checkout", "-q", "--detach", rev).returncode == 0
    return d


def commit(d, name):
    g(d, "add", "-A")
    r = g(d, "-c", "user.name=ctl", "-c", "user.email=ctl@scratch.invalid", "commit", "-q", "-m", name)
    assert r.returncode == 0, r.stderr


def positive(repo, freeze, work, name):
    d = clone(repo, freeze, work, name)
    subprocess.run([sys.executable, "-I", os.path.join(W, "l1-draft", "build-pos.py"), d], check=True,
                   env=dict(ENV, L1DRAFT=os.path.join(W, "l1-draft")), capture_output=True)
    return d


def rd(d, p):
    return open(os.path.join(d, p), encoding="utf-8").read()


def wr(d, p, s):
    os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
    open(os.path.join(d, p), "w", encoding="utf-8").write(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    counter = os.path.join(a.repo, "quality", "counters", "c2-r44-gkeep-size-request-v2.py")
    os.makedirs(a.work, exist_ok=True)
    runs = []
    d = positive(a.repo, a.freeze, a.work, "P"); commit(d, "P"); runs.append(("P", d, "HEAD", True))
    runs.append(("C2-BASE", a.repo, a.base, False))
    pos_lesson = rd(d, LESSON)
    readme_row = "| `knowledge/hyprland-gkeep-size-request-r44.md` | control row | - |\n"
    for name, entry in (("STAGED-COPY", open(STAGED).read()),
                        ("R12-REPOINT", open(os.path.join(W, "w1/CritClaimSizing/controls/entry-r12-repoint.md")).read()),
                        ("MINIMAL-QUOTES", open(os.path.join(W, "w1/CritClaimSizing/controls/entry-minimal.md")).read())):
        if name == "STAGED-COPY":
            d = clone(a.repo, a.freeze, a.work, name)
            wr(d, ENTRY, entry); wr(d, LESSON, pos_lesson)
            open(os.path.join(d, "corpus/README.md"), "a").write(readme_row)
        else:
            d = positive(a.repo, a.freeze, a.work, name)
            wr(d, ENTRY, entry)
        commit(d, name); runs.append((name, d, "HEAD", False))
    d = positive(a.repo, a.freeze, a.work, "SHELL")
    wr(d, ENTRY, "\n".join(rd(d, ENTRY).split("\n")[:12]) + "\n\ngkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep\nhyprland sendWindowSize xdg_setSize=1 x11_configure=1\n")
    commit(d, "SHELL"); runs.append(("SHELL", d, "HEAD", False))
    d = positive(a.repo, a.freeze, a.work, "HIDDEN-LINE")
    wr(d, ENTRY, rd(d, ENTRY) + "\ngkeep client follow-up: per S164 the compositor always waits for the ack before drawing.\n")
    commit(d, "HIDDEN-LINE"); runs.append(("HIDDEN-LINE", d, "HEAD", False))
    d = positive(a.repo, a.freeze, a.work, "FORGED-PIN")
    src = rd(d, FETCH + "Hyprland-Window.cpp")
    forged = src.replace("        m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());",
                         "        m_pendingSizeAcks.emplace_back(0, REPORTSIZE.floor());")
    assert forged != src
    wr(d, FETCH + "Hyprland-Window.cpp", forged)
    sha_old = hashlib.sha256(src.encode()).hexdigest(); sha_new = hashlib.sha256(forged.encode()).hexdigest()
    wr(d, LESSON, rd(d, LESSON).replace(sha_old, sha_new))
    wr(d, ENTRY, rd(d, ENTRY).replace("xdg_setSize=1", "xdg_setSize=0"))
    commit(d, "FORGED-PIN"); runs.append(("FORGED-PIN", d, "HEAD", False))
    d = positive(a.repo, a.freeze, a.work, "FALSE-URL")
    reg = rd(d, "corpus/SOURCES.md")
    url = "https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py"
    assert reg.count(url) == 1
    wr(d, "corpus/SOURCES.md", reg.replace(url, "https://example.com/docs/ui.py"))
    commit(d, "FALSE-URL"); runs.append(("FALSE-URL", d, "HEAD", False))
    d = positive(a.repo, a.freeze, a.work, "PROSE-SIZE-REQUEST")
    wr(d, ENTRY, rd(d, ENTRY) + "\nINF gkeep also pins its window with `set_size_request(420, 500)`.\n")
    commit(d, "PROSE-SIZE-REQUEST"); runs.append(("PROSE-SIZE-REQUEST", d, "HEAD", False))
    d = positive(a.repo, a.freeze, a.work, "ANCHOR-PAST-EOF")
    reg = rd(d, "corpus/SOURCES.md")
    old = "gdktoplevel-wayland.c:444-545 compute_size, gdktoplevel-wayland.c:606-700 handle_configure"
    assert reg.count(old) == 1
    wr(d, "corpus/SOURCES.md", reg.replace(old, "gdktoplevel-wayland.c:9999-10005 compute_size, gdktoplevel-wayland.c:9999-10005 handle_configure"))
    commit(d, "ANCHOR-PAST-EOF"); runs.append(("ANCHOR-PAST-EOF", d, "HEAD", False))
    wrong = 0
    print("CTL_C2v2: freeze=%s base=%s controls=%d (P positive; %d do-nothing/forged)" % (a.freeze, a.base, len(runs), len(runs) - 1))
    for name, repo, rev, want in runs:
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--base", a.base],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        cl = next((l.split(" clauses=")[-1] for l in lines if " clauses=" in l), "-")
        got = p.returncode == 0
        ok = got == want
        wrong += not ok
        print("CTL_C2v2 %s want=%s got=%s rc=%d %s | %s | %s" % (name, "admitted" if want else "rejected",
              "admitted" if got else "rejected", p.returncode, "ok" if ok else "WRONG", cl, lines[-1] if lines else ""))
    for name, repo, rev, want in runs:
        if repo != a.repo:
            shutil.rmtree(repo, ignore_errors=True)
    print("CTL_C2v2 VERDICT: %s (wrong=%d of %d; positive admitted=%d)" % ("PASS" if not wrong else "FAIL", wrong, len(runs), int(runs[0][3])))
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
