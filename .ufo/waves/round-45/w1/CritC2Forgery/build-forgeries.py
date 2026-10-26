#!/usr/bin/env python3
"""Seat CritC2Forgery - build forged C2 candidates on top of the positive control and score them with the frozen
PRED-C2-r45 counter. Every mutation is asserted before the commit."""
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r45/CritC2Forgery"
D = os.path.join(S, "pc")
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c2-r45-monitor-entry.py")
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
ENTRY = "corpus/knowledge/hyprland-monitor-rule-r45.md"
REG = "corpus/SOURCES.md"
README = "corpus/README.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def g(*a):
    p = subprocess.run(["git", "-C", D, *a], capture_output=True, text=True, env=ENV)
    assert p.returncode == 0, (a, p.stderr)
    return p.stdout


def rd(p):
    return open(os.path.join(D, p), encoding="utf-8").read()


def wr(p, s):
    open(os.path.join(D, p), "w", encoding="utf-8").write(s)


def sub(p, old, new, n=1):
    t = rd(p)
    assert t.count(old) == n, (p, t.count(old), old[:80])
    wr(p, t.replace(old, new))


def app(p, s):
    wr(p, rd(p) + s)


def score(rev, counter=COUNTER, tag=""):
    p = subprocess.run([sys.executable, "-I", counter, "--repo", D, "--rev", rev, "--base", BASE],
                       capture_output=True, text=True, env=ENV)
    return p.returncode, p.stdout


# --- mutations ---------------------------------------------------------------------------------------------------
def f1(d):
    sub(ENTRY,
        "**OBS** S304 - adding a rule first erases every rule with the same selector string: "
        "`std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });` "
        "(Hyprland-MonitorRuleManager.cpp:38). The add function (Hyprland-MonitorRuleManager.cpp:37-42) then "
        "appends, so a re-added selector moves to the end of the list.",
        "**OBS** S304 - adding a rule first erases every rule with the same selector string: "
        "`std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });` "
        "(Hyprland-MonitorRuleManager.cpp:38). The add function (Hyprland-MonitorRuleManager.cpp:37-42) appends, "
        "and the stored order is the order rules are honoured in.")
    sub(ENTRY,
        "**OBS** The lookup walks the list in reverse and returns the first match, so the newest matching rule "
        "wins; with none it returns the first rule whose selector is empty, then a built-in default (preferred, "
        "auto, auto) (Hyprland-MonitorRuleManager.cpp:96-106).",
        "**OBS** The lookup does not run in reverse: it takes the first match from the top of the list, so a rule "
        "written in an earlier config file wins over a later one, and an exact selector always loses to a "
        "`desc:` rule (Hyprland-MonitorRuleManager.cpp:96-106).")


def f2(d):
    sub(ENTRY,
        "| What does `WxH` without `@RATE` request? | the rule keeps its 60 Hz default, so the mode closest to "
        "60 Hz at that size is chosen | OBS (source) + INF (mode choice not exercised) |",
        "| What does `WxH` without `@RATE` request? | the output's fastest mode at that size | "
        "OBS (verified on the host) |")
    sub(ENTRY,
        "| Does the documented `sdr_eotf` key work on a `monitor =` line? | the wiki documents it; the host's "
        "handler reads it only in `monitorv2` blocks | OBS (source, docs) + INF (rejection not exercised) |",
        "| Does the documented `sdr_eotf` key work on a `monitor =` line? | yes, on `monitor =` lines too | "
        "OBS (host) |")


def f3(d):
    app(ENTRY, "\nINF The census line above is narrower than the searched grid: scale_search = 44 steps and "
               "default_refresh : 45 Hz, so a scale written with two decimals may land a whole screen away.\n")


def f4(d):
    app(ENTRY, "\nINF The mode is accepted within two hertz of the request, the scale search walks ninety steps "
               "up and down, and the line takes nine key pairs.\n")


def f5(d):
    sub(REG, "One rule per selector string; the newest matching rule wins, else the first empty-selector rule, "
             "else a built-in default",
        "Supersedes S158 and S162; the first matching rule in file order wins and later files cannot override it")


def f6(d):
    app(ENTRY, "\n```\n| question | answer |\n|---|---|\n| which stored rule wins | the first matching rule, so "
               "later files are ignored |\n| mode without @RATE | the output's fastest mode |\n| disabled "
               "outputs in monitors all | never listed |\n```\n")


def f7(d):
    sub(ENTRY,
        "**OBS** `~/.config/hypr/monitors.conf` declares one rule, DP-1 at 3440x1440@100, position 0x0, scale 1; "
        "`hyprctl monitors all -j` reports DP-1 at 3440x1440, 99.99700 Hz, 0x0, scale 1, transform 0, not "
        "disabled, mirroring none; the round's tool reports AGREE and verdict OK, exit 0 "
        "(.ufo/waves/round-45/receipts/live-monitors-host-l1.txt). The 0.003 Hz gap is inside the 1 Hz closeness "
        "bound.",
        "**OBS** `~/.config/hypr/monitors.conf` declares one rule, DP-1 at 3440x1440@100, position 0x0, scale 1; "
        "`hyprctl monitors all -j` reports DP-1 at 3440x1440, 59.94000 Hz, 0x0, scale 1.25, transform 1, not "
        "disabled, mirroring none; the round's tool reports DIFFER on the refresh rate and verdict 1, exit 1 "
        "(.ufo/waves/round-45/receipts/live-monitors-host-l1.txt).")


def f8(d):
    sub(README, "| `knowledge/hyprland-monitor-rule-r45.md` (MADO-R45-1, round 45) | draft | S302-S310 |",
        "| `knowledge/hyprland-monitor-rule-r45.md` (MADO-R45-1, round 45) | merged | S290-S310 "
        "(supersedes S290-S297) |")


def f9(d):
    sub(ENTRY,
        "**OBS** For a requested `WxH@R` the available modes are sorted by closeness in width, then height, then "
        "rate, and when the best one is not within 1 px and 1 Hz of the request the requested mode is tried first "
        "as a custom mode (Hyprland-Monitor.cpp:819-840);",
        "**OBS** For a requested `WxH@R` the modes are taken in the order the kernel reports them, and the best "
        "one is accepted when it is within 100 px and 10 Hz of the request; anything further away silently keeps "
        "the previous mode (Hyprland-Monitor.cpp:819-840);")


MUT = [("F1-quote-beside-claim", f1), ("F2-table-overclaim", f2), ("F3-spaced-census-token", f3),
       ("F4-census-in-words", f4), ("F5-registry-supersession", f5), ("F6-fenced-smuggle", f6),
       ("F7-false-live-verdict", f7), ("F8-readme-index-row", f8), ("F9-surface-sentence-inverted", f9)]


def ensure_pc():
    """Build the positive control clone at the freeze if it is not there yet (positive-control recipe)."""
    os.makedirs(S, exist_ok=True)
    if os.path.isdir(os.path.join(D, ".git")):
        return
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, D], check=True, env=ENV)
    assert g("rev-parse", "--show-toplevel").strip() == D, "clone toplevel is not the clone"
    g("checkout", "-q", "--detach", "22a8dedd02f507689c567777e0f20b5e645c8ce0")
    subprocess.run([sys.executable, "-I", os.path.join(LANE, ".ufo/waves/round-45/l1-draft/build-pos.py"), D],
                   check=True, env=dict(ENV, L1DRAFT=os.path.join(LANE, ".ufo/waves/round-45/l1-draft")))
    g("add", "-A")
    g("-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid", "commit", "-q", "-m", "pos")


def main():
    ensure_pc()
    P = g("rev-parse", "HEAD").strip()
    print("P=%s" % P)
    os.makedirs(os.path.join(S, "logs"), exist_ok=True)
    out = []
    for name, fn in MUT:
        g("checkout", "-q", "--detach", P)
        fn(D)
        g("add", "-A")
        g("-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid", "commit", "-q", "-m", name)
        h = g("rev-parse", "HEAD").strip()
        diff = g("show", "--format=", "--unified=1", h)
        open(os.path.join(S, "logs", name + ".diff"), "w").write(diff)
        rc, o = score("HEAD")
        open(os.path.join(S, "logs", name + ".score.txt"), "w").write(o)
        last = o.strip().splitlines()[-1]
        cl = [l for l in o.splitlines() if "clauses=" in l]
        print("%-26s rc=%d %s | %s" % (name, rc, last, cl[0].split("clauses=")[1] if cl else "?"))
        out.append((name, h, rc, last))
    import json
    json.dump({"P": P, **{n: h for n, h, _, _ in out}},
              open(os.path.join(S, "logs", "revs.json"), "w"), indent=1)
    g("checkout", "-q", "--detach", P)
    return out


if __name__ == "__main__":
    main()
