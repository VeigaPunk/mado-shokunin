#!/usr/bin/env python3
"""Round-45 C2 controls v2 (registration-v2.md) for PRED-C2-r45-v2.

P   the positive control: v2/build-pos.py applied on a clone of the v2 freeze (entry, rows S302-S315, lesson Gate,
    README row) - must be admitted;
then do-nothing / near-do-nothing / forged variants, each a throwaway clone under --work (git clone --shared; every
git call names -C <clone>; the scratch identity is used only inside the clone, checked by rev-parse --show-toplevel)
- none may be admitted:
  C2-BASE        the base revision (entry absent);
  R14-COPY       the held round-14 output/colour entry copied to the entry path on P's rows, lesson and README
                 (old ground under a new name);
  SHELL          P's header plus the census line only;
  WIDE-RANGE     P with every Hyprland-Monitor.cpp locator widened to the whole file (round-44 D5: clause j had no
                 width bound);
  HIDDEN-LINE    P plus a line naming S306 with no quote or locator;
  FORGED-PIN     P with fetch/Hyprland-MonitorRule.hpp doctored to a 144 Hz default, its Gate sha256 and the census
                 line recomputed to match;
  FALSE-URL      P with S309's location rewritten to https://example.com/String.cpp;
  PROSE-CENSUS   P plus a line claiming `default_refresh=144`;
  ANCHOR-PAST-EOF P with S305's anchor range moved past the receipt's end;
  PROSE-CENSUS-SPACED  P plus `default_refresh = 144` (T1; w1/CritC2Forgery F3);
  ROW-SUPERSEDES P with S304's teaches cell claiming it supersedes S158 (T2; F5);
  FENCE-TABLE    P plus a fenced false decision table (T3; F6);
  RECEIPT-CONTRADICT P plus a line saying the tool reported DIFFER, citing the live receipt that says AGREE (T4; F7);
  README-IDS     P with the README row listing S302-S310 only (T5; F8).
Usage: run-c2-controls-v2.py --repo LANE --freeze FREEZE --base BASE --work SCRATCHDIR"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
ENTRY = "corpus/knowledge/hyprland-monitor-rule-r45.md"
LESSON = "corpus/lessons/round-45.md"
FETCH = ".ufo/waves/round-45/fetch/"
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
    subprocess.run([sys.executable, "-I", os.path.join(W, "v2", "build-pos.py"), d], check=True,
                   env=dict(ENV, L1DRAFT=os.path.join(W, "v2")), capture_output=True)
    return d


def rd(d, p):
    return open(os.path.join(d, p), encoding="utf-8").read()


def wr(d, p, s):
    os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
    open(os.path.join(d, p), "w", encoding="utf-8").write(s)


CENSUS = ("hyprland monitor-rule default_refresh=60 refresh_tolerance=1 scale_step=1/120 scale_search=89 "
          "json_refresh_decimals=5 line_keys=8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    counter = os.path.join(a.repo, "quality", "counters", "c2-r45-monitor-entry-v2.py")
    os.makedirs(a.work, exist_ok=True)
    runs = []
    d = positive(a.repo, a.freeze, a.work, "P"); commit(d, "P"); runs.append(("P", d, "HEAD", True))
    runs.append(("C2-BASE", a.repo, a.base, False))

    d = positive(a.repo, a.freeze, a.work, "R14-COPY")
    wr(d, ENTRY, rd(d, "corpus/knowledge/output-colour-boundaries-r14.md"))
    commit(d, "R14-COPY"); runs.append(("R14-COPY", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "SHELL")
    wr(d, ENTRY, "\n".join(rd(d, ENTRY).split("\n")[:20]) + "\n\n" + CENSUS + "\n")
    commit(d, "SHELL"); runs.append(("SHELL", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "WIDE-RANGE")
    import re
    t = re.sub(r"Hyprland-Monitor\.cpp:\d+(?:-\d+)?", "Hyprland-Monitor.cpp:1-2815", rd(d, ENTRY))
    wr(d, ENTRY, t)
    commit(d, "WIDE-RANGE"); runs.append(("WIDE-RANGE", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "HIDDEN-LINE")
    wr(d, ENTRY, rd(d, ENTRY) + "\nper S306 the compositor never corrects a scale written with two decimals.\n")
    commit(d, "HIDDEN-LINE"); runs.append(("HIDDEN-LINE", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "FORGED-PIN")
    src = rd(d, FETCH + "Hyprland-MonitorRule.hpp")
    forged = src.replace("m_refreshRate   = 60; // Hz", "m_refreshRate   = 144; // Hz")
    assert forged != src
    wr(d, FETCH + "Hyprland-MonitorRule.hpp", forged)
    old, new = hashlib.sha256(src.encode()).hexdigest(), hashlib.sha256(forged.encode()).hexdigest()
    wr(d, LESSON, rd(d, LESSON).replace(old, new).replace("float m_refreshRate = 60;", "float m_refreshRate = 144;"))
    wr(d, ENTRY, rd(d, ENTRY).replace("default_refresh=60", "default_refresh=144")
       .replace("float m_refreshRate = 60;", "float m_refreshRate = 144;"))
    wr(d, "corpus/SOURCES.md", rd(d, "corpus/SOURCES.md").replace(old, new))
    commit(d, "FORGED-PIN"); runs.append(("FORGED-PIN", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "FALSE-URL")
    reg = rd(d, "corpus/SOURCES.md")
    url = "https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/String.cpp"
    assert reg.count(url) == 1
    wr(d, "corpus/SOURCES.md", reg.replace(url, "https://example.com/String.cpp"))
    commit(d, "FALSE-URL"); runs.append(("FALSE-URL", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "PROSE-CENSUS")
    wr(d, ENTRY, rd(d, ENTRY) + "\nINF on this host the line form behaves as default_refresh=144.\n")
    commit(d, "PROSE-CENSUS"); runs.append(("PROSE-CENSUS", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "ANCHOR-PAST-EOF")
    reg = rd(d, "corpus/SOURCES.md")
    old = "Hyprland-MonitorRule.hpp:41-69 class CMonitorRule fields"
    assert reg.count(old) == 1
    wr(d, "corpus/SOURCES.md", reg.replace(old, "Hyprland-MonitorRule.hpp:900-950 class CMonitorRule fields"))
    commit(d, "ANCHOR-PAST-EOF"); runs.append(("ANCHOR-PAST-EOF", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "PROSE-CENSUS-SPACED")
    wr(d, ENTRY, rd(d, ENTRY) + "\nINF the line form behaves as default_refresh = 144 on this host.\n")
    commit(d, "PROSE-CENSUS-SPACED"); runs.append(("PROSE-CENSUS-SPACED", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "ROW-SUPERSEDES")
    reg = rd(d, "corpus/SOURCES.md")
    old = "One rule per selector string; the newest matching rule wins"
    assert reg.count(old) == 1
    wr(d, "corpus/SOURCES.md", reg.replace(old, "Supersedes S158 and S162; the first matching rule wins"))
    commit(d, "ROW-SUPERSEDES"); runs.append(("ROW-SUPERSEDES", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "FENCE-TABLE")
    wr(d, ENTRY, rd(d, ENTRY) + "\n```\n| rule | wins |\n|---|---|\n| the first matching rule | always |\n```\n")
    commit(d, "FENCE-TABLE"); runs.append(("FENCE-TABLE", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "RECEIPT-CONTRADICT")
    wr(d, ENTRY, rd(d, ENTRY) + "\nOBS on this host the tool reported DIFFER for DP-1 "
       "(.ufo/waves/round-45/receipts/live-monitors-host-l1.txt).\n")
    commit(d, "RECEIPT-CONTRADICT"); runs.append(("RECEIPT-CONTRADICT", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "README-IDS")
    readme = rd(d, "corpus/README.md")
    assert readme.count("| draft | S302-S315 |") == 1
    wr(d, "corpus/README.md", readme.replace("| draft | S302-S315 |", "| draft | S302-S310 |"))
    commit(d, "README-IDS"); runs.append(("README-IDS", d, "HEAD", False))

    wrong, padm = 0, 0
    print("CTL_C2v2: freeze=%s base=%s controls=%d (P positive; %d do-nothing/forged)" % (
        a.freeze, a.base, len(runs), len(runs) - 1))
    for name, repo, rev, want in runs:
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--base", a.base],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        cl = next((l.split(" clauses=")[-1] for l in lines if " clauses=" in l), "-")
        got = p.returncode == 0
        ok = got == want
        wrong += not ok
        if name == "P":
            padm = int(got)
        print("CTL_C2v2 %s want=%s got=%s rc=%d %s | %s | %s" % (name, "admitted" if want else "rejected",
              "admitted" if got else "rejected", p.returncode, "ok" if ok else "WRONG", cl,
              lines[-1] if lines else ""))
    for name, repo, rev, want in runs:
        if repo != a.repo:
            shutil.rmtree(repo, ignore_errors=True)
    print("CTL_C2v2 VERDICT: %s (wrong=%d of %d; positive admitted=%d)" % (
        "PASS" if not wrong else "FAIL", wrong, len(runs), padm))
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
