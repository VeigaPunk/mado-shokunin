#!/usr/bin/env python3
"""CritC2Cheat: forged C2 entry+registry+lesson sets scored by the FROZEN PRED-C2-r43.

Fixtures are built with the frozen controls' own helpers (base_files/admitted/row/gate_line/
commit_all), so every forgery differs from control P exactly where its comment says. Each
forged fixture's changed files are dumped under <seat>/fixtures/<tag>/ as evidence.
Every git call names -C <D>; D lives under /fast/scratch/hyaku/mado-r43/CritC2Cheat.
The counter is never edited (probe variants are scratch copies, see probes.py).
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WORK = "/fast/scratch/hyaku/mado-r43/CritC2Cheat"
SEAT = os.path.join(LANE, ".ufo/waves/round-43/w1/CritC2Cheat")
COUNTER = os.path.join(LANE, "quality/counters/c2-r43-gkeep-entry.py")
CTL = os.path.join(LANE, ".ufo/waves/round-43/ctl/run-c2-controls.py")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
os.environ["TMPDIR"] = os.path.join(WORK, "tmp")
os.makedirs(os.environ["TMPDIR"], exist_ok=True)

spec = importlib.util.spec_from_file_location("ctl", CTL)
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)
ENTRY, SRC, LES, FETCH = ctl.ENTRY, ctl.SRC, ctl.LES, ctl.FETCH
EL = {i: ctl.entry_line(i) for i in ctl.REAL}
Q = {i: ctl.REAL[i][3] for i in ctl.REAL}
RULES_LINE, CLIENTS_LINE, UI_LINE = ctl.CENSUS
BASE = ctl.base_files()
P = ctl.admitted()


def copy(g):
    return {k: v for k, v in g.items()}


def rep(g, key, old, new):
    assert old in g[key], (key, old[:60])
    g[key] = g[key].replace(old, new, 1)


def dump(tag, g):
    d = os.path.join(SEAT, "fixtures", tag)
    shutil.rmtree(d, ignore_errors=True)
    for rel in (ENTRY, SRC, LES, "corpus/README.md"):
        os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
        data = g[rel]
        with open(os.path.join(d, rel), "wb") as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())


def run(files_after):
    d = tempfile.mkdtemp(prefix="fx-", dir=WORK)
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ENV).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), (top, d)
        b = ctl.commit_all(d, BASE, "base")
        a = ctl.commit_all(d, files_after, "after")
        p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        return p.returncode, p.stdout
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------------------ fixtures
def fx_P(g):
    return g


def fx_A1(g):
    rep(g, ENTRY, EL["S291"],
        "**OBS** S291 the compositor applies every rule size to the live client at once, "
        "and the client never resizes itself again (" + Q["S291"]
        + ", Hyprland-WindowRuleApplicator.cpp:%d)."
        % ctl.line_of("Hyprland-WindowRuleApplicator.cpp", Q["S291"]))


def fx_A2(g):
    rep(g, ENTRY, EL["S298"],
        '**OBS** S298 the only gkeep client is mapped, floating and reports the rule size ('
        + Q["S298"] + ", host-clients-r43.json:%d)."
        % ctl.line_of("host-clients-r43.json", Q["S298"]))


BQ = "const auto& expr = std::get<Math::SExpressionVec2>(value);"
BF = "Hyprland-WindowRuleApplicator.cpp"


def fx_B1(g):
    rep(g, LES, 'quote="%s"' % Q["S291"], 'quote="%s"' % BQ)
    rep(g, ENTRY, EL["S291"],
        "**OBS** S291 " + BQ + " - the size rule stores this expression as static_.size "
        "(%s:%d)." % (BF, ctl.line_of(BF, BQ)))


def fx_B2(g):
    rep(g, LES, 'quote="%s"' % Q["S291"], 'quote="%s"' % BQ)
    rep(g, ENTRY, EL["S291"],
        "**OBS** S291 " + BQ + " - the size rule stores this expression as static_.size "
        "(%s:414)." % BF)


CQ = "TODO: not very OOP, is it?"
CF = "Hyprland-DefaultFloatingAlgorithm.cpp"
CQ2 = "Reserved area must be updated before this is called"
CF2 = "Hyprland-WindowTarget.cpp"


def fx_C1(g):
    rep(g, LES, 'quote="%s"' % Q["S292"], 'quote="%s"' % CQ)
    rep(g, ENTRY, EL["S292"],
        "**OBS** S292 " + CQ + " - the floating algorithm leaves the size to the client; "
        "the author records that no size path exists (%s:%d)."
        % (CF, ctl.line_of(CF, CQ)))


def fx_C2(g):
    rep(g, LES, 'quote="%s"' % Q["S294"], 'quote="%s"' % CQ2)
    rep(g, ENTRY, EL["S294"],
        "**OBS** S294 " + CQ2 + " - the target defers every box until the reserved area "
        "is refreshed (%s:%d)." % (CF2, ctl.line_of(CF2, CQ2)))


def fx_D1(g):
    g[ENTRY] = g[ENTRY].replace(
        "\n" + RULES_LINE,
        "\nThe census below proves the applied geometry: the single gkeep client is "
        "floating and reports 420x500, so the rule size is the rendered size.\n" + RULES_LINE)


def fx_E1(g):
    g[ENTRY] += "**NOTE** S291 is unrelated to the size path: no rule ever writes static_.size.\n"


def fx_E2(g):
    g[ENTRY] += "**NOTE** the size rule is never applied: no code writes static_.size.\n"


def fx_F1(g):
    fake = "merge/mado/not-a-real-dir/"
    g[LES] = g[LES].replace("ADMIT " + ctl.PKG + " as ",
                            "ADMIT " + fake + os.path.basename(ctl.PKG) + " as ")
    g[LES] = g[LES].replace("REFUSE " + ctl.PKG2 + " reason=",
                            "REFUSE " + fake + os.path.basename(ctl.PKG2) + " reason=")


def fx_F2(g):
    old = [l for l in g[LES].splitlines() if l.startswith("REFUSE ")][0]
    g[LES] = g[LES].replace(old, "REFUSE %s reason=this refusal says nothing else" % ctl.PKG2)


def fx_G1(g):
    rep(g, SRC, ctl.REAL["S293"][2], "https://example.invalid/nope/Hyprland-Target.cpp")


def fx_G2(g):
    rep(g, SRC, ctl.REAL["S292"][2], "nowhere/DefaultFloatingAlgorithm.cpp")


def fx_H1(g):
    g[ENTRY] = g[ENTRY].replace(
        "\n" + RULES_LINE,
        "\nNothing here is determined by the sources below; the compositor picks the size "
        "on its own.\n" + RULES_LINE)


FIX = [("P-genuine", fx_P), ("A1-unsupported-claim", fx_A1),
       ("A2-census-contradiction", fx_A2), ("B1-second-occurrence", fx_B1),
       ("B2-second-locator-negative", fx_B2), ("C1-comment-quote", fx_C1),
       ("C2-comment-quote-dup", fx_C2), ("D1-census-irrelevant", fx_D1),
       ("E1-id-contradiction", fx_E1), ("E2-anonymous-contradiction", fx_E2),
       ("F1-fake-package-dir", fx_F1), ("F2-refuse-no-flip", fx_F2),
       ("G1-fake-url", fx_G1), ("G2-relative-path", fx_G2),
       ("H1-theme-contradiction", fx_H1)]

print("counter sha256:", __import__("hashlib").sha256(open(COUNTER, "rb").read()).hexdigest())
adm = 0
for tag, fx in FIX:
    g = copy(P)
    fx(g)
    dump(tag, g)
    rc, out = run(g)
    lines = out.strip().splitlines()
    final = [l for l in lines if ": admitted=" in l][-1]
    cls = [l for l in lines if " clauses=" in l][0].split("clauses=")[1].split(" admitted")[0]
    ok = rc == 0 and "admitted=1/1" in final
    adm += ok
    print("### %-28s rc=%d %s clauses=%s %s" % (
        tag, rc, final.split("PRED-C2-r43: ")[-1].split(" verdict")[0], cls,
        "ADMITTED" if ok else "rejected"))
print("=== forged fixtures admitted by the frozen counter: %d/%d" % (adm, len(FIX)))
