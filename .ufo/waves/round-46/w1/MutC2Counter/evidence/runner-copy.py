#!/usr/bin/env python3
"""Round-46 C2 controls (registration.md) for PRED-C2-r46 - MutC2Counter scratch copy.

Verbatim copy of .ufo/waves/round-46/ctl/run-c2-controls.py (control definitions, verdict
logic and output format unchanged) with ONE hygiene deviation: each control clone is
created, evaluated and deleted sequentially instead of all 15 being alive at once
(freeze tree is ~236 MB; 15 concurrent checkouts would exceed the seat's 2 GB scratch
budget). The counter under test is taken from --repo's working tree, exactly as in the
original, so pointing --repo at a mutant repo tests the mutant.

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
    # (name, rev, want, mutate-or-None); C2-BASE runs against --repo itself
    runs = [("P", "HEAD", True, None), ("C2-BASE", a.base, False, None)]

    def v_ry45(d):
        wr(d, ENTRY, rd(d, "corpus/knowledge/hyprland-monitor-rule-r45.md"))
    runs.append(("R45-COPY", "HEAD", False, v_ry45))

    def v_shell(d):
        wr(d, ENTRY, "\n".join(rd(d, ENTRY).split("\n")[:20]) + "\n\n" + CENSUS + "\n")
    runs.append(("SHELL", "HEAD", False, v_shell))

    def v_wide(d):
        import re
        t = re.sub(r"Hyprland-InputManager\.cpp:\d+(?:-\d+)?", "Hyprland-InputManager.cpp:1-2315", rd(d, ENTRY))
        wr(d, ENTRY, t)
    runs.append(("WIDE-RANGE", "HEAD", False, v_wide))

    def v_hidden(d):
        wr(d, ENTRY, rd(d, ENTRY) + "\nper S316 the compositor reads the global layout before the device block.\n")
    runs.append(("HIDDEN-LINE", "HEAD", False, v_hidden))

    def v_forged(d):
        src = rd(d, FETCH + "Hyprland-ConfigValues.cpp")
        a_, b_ = '"Appropriate XKB keymap parameter", "us",', '"Appropriate XKB keymap parameter", "de",'
        forged = src.replace(a_, b_)
        assert forged != src
        wr(d, FETCH + "Hyprland-ConfigValues.cpp", forged)
        old, new = hashlib.sha256(src.encode()).hexdigest(), hashlib.sha256(forged.encode()).hexdigest()
        wr(d, LESSON, rd(d, LESSON).replace(old, new).replace(a_, b_))
        wr(d, ENTRY, rd(d, ENTRY).replace("default_layout=us", "default_layout=de").replace(a_, b_))
        wr(d, "corpus/SOURCES.md", rd(d, "corpus/SOURCES.md").replace(old, new))
    runs.append(("FORGED-PIN", "HEAD", False, v_forged))

    def v_falseurl(d):
        reg = rd(d, "corpus/SOURCES.md")
        url = "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/VirtualKeyboard.cpp"
        assert reg.count(url) == 1, reg.count(url)
        wr(d, "corpus/SOURCES.md", reg.replace(url, "https://example.com/VirtualKeyboard.cpp"))
    runs.append(("FALSE-URL", "HEAD", False, v_falseurl))

    def v_prose(d):
        wr(d, ENTRY, rd(d, ENTRY) + "\nINF on this host the global block behaves as default_layout=de.\n")
    runs.append(("PROSE-CENSUS", "HEAD", False, v_prose))

    def v_anchor(d):
        reg = rd(d, "corpus/SOURCES.md")
        old = "Hyprland-VirtualKeyboard.cpp:36-44 keymap listener"
        assert reg.count(old) == 1
        wr(d, "corpus/SOURCES.md", reg.replace(old, "Hyprland-VirtualKeyboard.cpp:900-950 keymap listener"))
    runs.append(("ANCHOR-PAST-EOF", "HEAD", False, v_anchor))

    def v_prose2(d):
        wr(d, ENTRY, rd(d, ENTRY) + "\nINF the pointer clamp is scroll_factor_max = 10 on this host.\n")
    runs.append(("PROSE-CENSUS-SPACED", "HEAD", False, v_prose2))

    def v_supersedes(d):
        reg = rd(d, "corpus/SOURCES.md")
        old = "The global layout defaults to us and the other keymap names to empty"
        assert reg.count(old) == 1
        wr(d, "corpus/SOURCES.md", reg.replace(old, "Supersedes S158; the global layout defaults to us"))
    runs.append(("ROW-SUPERSEDES", "HEAD", False, v_supersedes))

    def v_fence(d):
        wr(d, ENTRY, rd(d, ENTRY) + "\n```\n| source | wins |\n|---|---|\n| the global input block | always |\n```\n")
    runs.append(("FENCE-TABLE", "HEAD", False, v_fence))

    def v_contradict(d):
        wr(d, ENTRY, rd(d, ENTRY) + "\nOBS on this host the tool reported DIFFER for every keyboard "
           "(.ufo/waves/round-46/receipts/live-devices-host-l1.txt).\n")
    runs.append(("RECEIPT-CONTRADICT", "HEAD", False, v_contradict))

    def v_readme(d):
        readme = rd(d, "corpus/README.md")
        assert readme.count("| draft | S316-S325 |") == 1
        wr(d, "corpus/README.md", readme.replace("| draft | S316-S325 |", "| draft | S316-S320 |"))
    runs.append(("README-IDS", "HEAD", False, v_readme))

    wrong, padm = 0, 0
    print("CTL_C2: freeze=%s base=%s controls=%d (P positive; %d do-nothing/forged)" % (
        a.freeze, a.base, len(runs), len(runs) - 1))
    for name, rev, want, fn in runs:
        d = None
        if name != "C2-BASE":
            d = positive(a.repo, a.freeze, a.work, name)
            if fn:
                fn(d)
            commit(d, name)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", d if d else a.repo,
                            "--rev", rev, "--base", a.base],
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
        if d:
            shutil.rmtree(d, ignore_errors=True)
    print("CTL_C2 VERDICT: %s (wrong=%d of %d; positive admitted=%d)" % (
        "PASS" if not wrong else "FAIL", wrong, len(runs), padm))
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
