#!/usr/bin/env python3
"""Round-46 C2 controls (registration.md) for PRED-C2-r46 - the round-45 v2 control set re-cut for the input-device entry.

P   the positive control: l1-draft/build-pos.py applied on a clone of the freeze (entry, rows S316-S325, lesson Gate,
    README row) - must be admitted;
then do-nothing / near-do-nothing / forged variants, each a throwaway clone under --work (git clone --shared; every
git call names -C <clone>; the scratch identity is used only inside the clone, checked by rev-parse --show-toplevel)
- none may be admitted:
  C2-BASE        the base revision (entry absent);
  R45-COPY       the held round-45 monitor-rule entry copied to the entry path on P's rows, lesson and README;
  SHELL          P's header plus the census line only;
  WIDE-RANGE     P with every Hyprland-InputManager.cpp locator widened to the whole file;
  HIDDEN-LINE    P plus a line naming S316 with no quote or locator;
  FORGED-PIN     P with fetch/Hyprland-ConfigValues.cpp doctored to a `de` default, its Gate sha256, rows, quote and
                 census recomputed to match;
  FALSE-URL      P with S323's location rewritten to https://example.com/VirtualKeyboard.cpp (S321's URL is also
                 held by S182, so the first cut's single-occurrence assertion stopped the runner before any score);
  PROSE-CENSUS   P plus a line claiming `default_layout=de`;
  ANCHOR-PAST-EOF P with S322's anchor range moved past the receipt's end;
  PROSE-CENSUS-SPACED  P plus `scroll_factor_max = 10`;
  ROW-SUPERSEDES P with S318's teaches cell claiming it supersedes S158;
  FENCE-TABLE    P plus a fenced false decision table;
  RECEIPT-CONTRADICT P plus a line saying the tool reported DIFFER, citing the live receipt that says AGREE;
  README-IDS     P with the README row listing S316-S320 only.
Usage: run-c2-controls.py --repo LANE --freeze FREEZE --base BASE --work SCRATCHDIR"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
ENTRY = "corpus/knowledge/hyprland-input-devices-r46.md"
LESSON = "corpus/lessons/round-46.md"
FETCH = ".ufo/waves/round-46/fetch/"
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


CENSUS = ("hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100 "
          "json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    counter = os.path.join(a.repo, "quality", "counters", "c2-r46-input-device-entry.py")
    os.makedirs(a.work, exist_ok=True)
    runs = []
    d = positive(a.repo, a.freeze, a.work, "P"); commit(d, "P"); runs.append(("P", d, "HEAD", True))
    runs.append(("C2-BASE", a.repo, a.base, False))

    d = positive(a.repo, a.freeze, a.work, "R45-COPY")
    wr(d, ENTRY, rd(d, "corpus/knowledge/hyprland-monitor-rule-r45.md"))
    commit(d, "R45-COPY"); runs.append(("R45-COPY", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "SHELL")
    wr(d, ENTRY, "\n".join(rd(d, ENTRY).split("\n")[:20]) + "\n\n" + CENSUS + "\n")
    commit(d, "SHELL"); runs.append(("SHELL", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "WIDE-RANGE")
    import re
    t = re.sub(r"Hyprland-InputManager\.cpp:\d+(?:-\d+)?", "Hyprland-InputManager.cpp:1-2315", rd(d, ENTRY))
    wr(d, ENTRY, t)
    commit(d, "WIDE-RANGE"); runs.append(("WIDE-RANGE", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "HIDDEN-LINE")
    wr(d, ENTRY, rd(d, ENTRY) + "\nper S316 the compositor reads the global layout before the device block.\n")
    commit(d, "HIDDEN-LINE"); runs.append(("HIDDEN-LINE", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "FORGED-PIN")
    src = rd(d, FETCH + "Hyprland-ConfigValues.cpp")
    a_, b_ = '"Appropriate XKB keymap parameter", "us",', '"Appropriate XKB keymap parameter", "de",'
    forged = src.replace(a_, b_)
    assert forged != src
    wr(d, FETCH + "Hyprland-ConfigValues.cpp", forged)
    old, new = hashlib.sha256(src.encode()).hexdigest(), hashlib.sha256(forged.encode()).hexdigest()
    wr(d, LESSON, rd(d, LESSON).replace(old, new).replace(a_, b_))
    wr(d, ENTRY, rd(d, ENTRY).replace("default_layout=us", "default_layout=de").replace(a_, b_))
    wr(d, "corpus/SOURCES.md", rd(d, "corpus/SOURCES.md").replace(old, new))
    commit(d, "FORGED-PIN"); runs.append(("FORGED-PIN", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "FALSE-URL")
    reg = rd(d, "corpus/SOURCES.md")
    url = "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/VirtualKeyboard.cpp"
    assert reg.count(url) == 1, reg.count(url)
    wr(d, "corpus/SOURCES.md", reg.replace(url, "https://example.com/VirtualKeyboard.cpp"))
    commit(d, "FALSE-URL"); runs.append(("FALSE-URL", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "PROSE-CENSUS")
    wr(d, ENTRY, rd(d, ENTRY) + "\nINF on this host the global block behaves as default_layout=de.\n")
    commit(d, "PROSE-CENSUS"); runs.append(("PROSE-CENSUS", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "ANCHOR-PAST-EOF")
    reg = rd(d, "corpus/SOURCES.md")
    old = "Hyprland-VirtualKeyboard.cpp:36-44 keymap listener"
    assert reg.count(old) == 1
    wr(d, "corpus/SOURCES.md", reg.replace(old, "Hyprland-VirtualKeyboard.cpp:900-950 keymap listener"))
    commit(d, "ANCHOR-PAST-EOF"); runs.append(("ANCHOR-PAST-EOF", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "PROSE-CENSUS-SPACED")
    wr(d, ENTRY, rd(d, ENTRY) + "\nINF the pointer clamp is scroll_factor_max = 10 on this host.\n")
    commit(d, "PROSE-CENSUS-SPACED"); runs.append(("PROSE-CENSUS-SPACED", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "ROW-SUPERSEDES")
    reg = rd(d, "corpus/SOURCES.md")
    old = "The global layout defaults to us and the other keymap names to empty"
    assert reg.count(old) == 1
    wr(d, "corpus/SOURCES.md", reg.replace(old, "Supersedes S158; the global layout defaults to us"))
    commit(d, "ROW-SUPERSEDES"); runs.append(("ROW-SUPERSEDES", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "FENCE-TABLE")
    wr(d, ENTRY, rd(d, ENTRY) + "\n```\n| source | wins |\n|---|---|\n| the global input block | always |\n```\n")
    commit(d, "FENCE-TABLE"); runs.append(("FENCE-TABLE", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "RECEIPT-CONTRADICT")
    wr(d, ENTRY, rd(d, ENTRY) + "\nOBS on this host the tool reported DIFFER for every keyboard "
       "(.ufo/waves/round-46/receipts/live-devices-host-l1.txt).\n")
    commit(d, "RECEIPT-CONTRADICT"); runs.append(("RECEIPT-CONTRADICT", d, "HEAD", False))

    d = positive(a.repo, a.freeze, a.work, "README-IDS")
    readme = rd(d, "corpus/README.md")
    assert readme.count("| draft | S316-S325 |") == 1
    wr(d, "corpus/README.md", readme.replace("| draft | S316-S325 |", "| draft | S316-S320 |"))
    commit(d, "README-IDS"); runs.append(("README-IDS", d, "HEAD", False))

    wrong, padm = 0, 0
    print("CTL_C2: freeze=%s base=%s controls=%d (P positive; %d do-nothing/forged)" % (
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
        print("CTL_C2 %s want=%s got=%s rc=%d %s | %s | %s" % (name, "admitted" if want else "rejected",
              "admitted" if got else "rejected", p.returncode, "ok" if ok else "WRONG", cl,
              lines[-1] if lines else ""))
    for name, repo, rev, want in runs:
        if repo != a.repo:
            shutil.rmtree(repo, ignore_errors=True)
    print("CTL_C2 VERDICT: %s (wrong=%d of %d; positive admitted=%d)" % (
        "PASS" if not wrong else "FAIL", wrong, len(runs), padm))
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
