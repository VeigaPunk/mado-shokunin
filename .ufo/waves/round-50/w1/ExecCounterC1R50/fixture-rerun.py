#!/usr/bin/env python3
"""Rebuild the fixture, add the no-pins control revision, and re-run every case + mutant.

Writes every receipt into the seat dir with the final counter bytes. Run it with TMPDIR
under the seat scratch and the script copied there (the fixture dir is <script dir>/fx).
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-50/w1/ExecCounterC1R50"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "8ae47b957034ae21012bbf09173cca2c48be345e"
D = os.path.join(HERE, "fx")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
COUNTER = os.path.join(SEAT, "c1-r50-bind-entry.py")
R49 = os.path.join(LANE, ".ufo/waves/round-49")
ENTRY = "corpus/knowledge/hyprland-bind-key-match-r50.md"

MUTANTS = (
    ("m1-quote-word", ENTRY, "const auto         KEYCODE = e.keycode + 8;",
     "const auto         KEYCODE = e.keycode + 9;"),
    ("m2-receipt-name", ENTRY, ".ufo/waves/round-50/receipts/binds-live-r50.txt",
     ".ufo/waves/round-50/receipts/census-before.txt"),
    # clause e: append a numbered step that carries no quote at all (removing one of several
    # quotes from a step is an equivalent mutant: e requires one verified quote per step)
    ("m3-step-no-quote", ENTRY, "\n## Observations",
     "\n18. **Synthetic step without a quote.** No located span on this line.\n\n## Observations"),
    # clause j: a step quote whose locator no longer covers the line that carries the topic
    ("m4-topic-line", ENTRY,
     "`pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState`"
     "(Hyprland-KeybindManager.cpp:369)",
     "`pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState`"
     "(Hyprland-KeybindManager.cpp:370)"),
    # clause h: the Limits section loses its heading (so its bullets are no longer a section)
    ("m5-no-limits", ENTRY, "\n## Limits", "\n## Limits and open questions"),
    # clause g: the held row S319 is edited at REV (held ground must be byte-equal)
    ("m6-held-row-moved", "corpus/SOURCES.md",
     "Hyprland-IKeyboard.cpp:60-145 setKeymap", "Hyprland-IKeyboard.cpp:60-146 setKeymap"),
)


def repo(*args):
    p = subprocess.run(["git", "-C", D, *args], capture_output=True, env=ENV)
    if p.returncode != 0:
        sys.exit("git %s rc=%d %s" % (args, p.returncode, p.stderr.decode()))
    return p.stdout.decode()


def run(rev, out, counter=COUNTER, repo_path=D):
    with open(os.path.join(SEAT, "receipts", out), "w") as fh:
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo_path,
                            "--rev", rev], capture_output=True, env=ENV)
        fh.write(p.stdout.decode())
    lines = p.stdout.decode().splitlines()
    print("%-28s rc=%d %s" % (out, p.returncode, lines[-1][:150] if lines else "(empty)"))
    return p.returncode


def mutate(name, relpath, old, new, c2):
    repo("checkout", "-q", "--detach", c2)
    path = os.path.join(D, relpath)
    text = open(path).read()
    assert text.count(old) >= 1, (name, "pattern absent")
    open(path, "w").write(text.replace(old, new))
    repo("add", "-A")
    repo("commit", "-q", "-m", "mutant %s" % name)
    rev = repo("rev-parse", "HEAD").strip()
    run(rev, "mutant-%s.txt" % name)
    print("   %s rev=%s" % (name, rev))
    repo("checkout", "-q", "--detach", c2)


def main():
    built = subprocess.run([sys.executable, os.path.join(HERE, "build_fixture.py")],
                           check=True, env=ENV, capture_output=True)
    revs = dict(re.findall(r"^(c[12])=([0-9a-f]{40})$", built.stdout.decode(), re.M))
    c1, c2 = revs["c1"], revs["c2"]
    top = repo("rev-parse", "--show-toplevel").strip()
    assert os.path.realpath(top) == os.path.realpath(D), (top, D)

    # no-pins control revision: the entry alone
    repo("checkout", "-q", "--detach", BASE)
    entry = open(os.path.join(R49, "candidate",
                              "hyprland-bind-key-match-r49.md")).read()
    entry = entry.replace("round-49", "round-50").replace("r49", "r50")
    entry = entry.replace("hyprland-bind-key-match-r49.md",
                          "hyprland-bind-key-match-r50.md")
    os.makedirs(os.path.dirname(os.path.join(D, ENTRY)), exist_ok=True)
    open(os.path.join(D, ENTRY), "w").write(entry)
    repo("add", ENTRY)
    repo("commit", "-q", "-m", "fixture nopins: entry only, no round-50 pins")
    nopins = repo("rev-parse", "HEAD").strip()

    print("c1=%s c2=%s nopins=%s" % (c1, c2, nopins))
    run(BASE, "base-run.txt", repo_path=LANE)
    run(c1, "fixture-c1.txt")
    run(c2, "fixture-c2.txt")
    run(nopins, "control-no-pins.txt")

    for name, relpath, old, new in MUTANTS:
        mutate(name, relpath, old, new, c2)

    # old GROUND tuple, as the round-49 counter carried it
    old = ('GROUND = ("xkb_state_key_get_layout", "m_modifiersState", "keysym_to_name",\n'
           '          "xkb_keysym_get_name")')
    new = ('GROUND = ("xkb_state_key_get_one_sym", "m_xkbSymState", "keysym_to_name",\n'
           '          "xkb_keysym_get_name")')
    text = open(COUNTER).read()
    assert text.count(old) == 1
    alt = os.path.join(HERE, "old-ground.py")
    open(alt, "w").write(text.replace(old, new))
    run(c2, "old-ground-r49-terms.txt", counter=alt)
    os.remove(alt)

    # rows and documents present, fetch dir removed: clause c alone must fail
    repo("checkout", "-q", "--detach", c2)
    pack = subprocess.run(["git", "-C", D, "rm", "-r", "-q", "--cached",
                           ".ufo/waves/round-50/fetch"], capture_output=True, env=ENV)
    assert pack.returncode == 0, pack.stderr.decode()
    shutil.rmtree(os.path.join(D, ".ufo/waves/round-50/fetch"))
    repo("commit", "-q", "-m", "fixture nopins-with-rows: rows kept, fetch pins removed")
    c_only = repo("rev-parse", "HEAD").strip()
    run(c_only, "mutant-c-nopins.txt")
    repo("checkout", "-q", "--detach", c2)

    with open(os.path.join(SEAT, "receipts", "fixture-identity.txt"), "w") as fh:
        fh.write("recipe: fixture-rerun.py -> build_fixture.py "
                 "(git clone -q --shared <lane> fx ; checkout --detach %s)\n" % BASE)
        fh.write("toplevel: %s\nexpected: %s\n" % (top, os.path.realpath(D)))
        fh.write("base: %s\n" % repo("rev-parse", BASE).strip())
        for label, rev in (("c2", c2), ("c1", c1), ("nopins", nopins)):
            fh.write("%s %s %s\n" % (label, rev,
                                     repo("log", "-1", "--format=%s", rev).strip()))
        fh.write("counter sha256: %s\n" % subprocess.run(
            ["sha256sum", COUNTER], capture_output=True).stdout.decode().split()[0])
        fh.write("fixture files at c2: %s\n" % repo(
            "ls-tree", "-r", "--name-only", c2).count("\n"))
        fh.write("r50 paths at c2:\n")
        for p in repo("ls-tree", "-r", "--name-only", c2).splitlines():
            if p.startswith(".ufo/waves/round-50/fetch/") \
                    or p.startswith(".ufo/waves/round-50/receipts/") \
                    or p.endswith("hyprland-bind-key-match-r50.md") \
                    or p == "corpus/lessons/round-50.md":
                fh.write(p + "\n")


if __name__ == "__main__":
    main()
