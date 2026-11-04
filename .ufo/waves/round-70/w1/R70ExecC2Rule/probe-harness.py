#!/usr/bin/env python3
"""Independent re-derivation for seat R70ExecC2Rule: base leg, population recount, probes."""
import hashlib
import json
import os
import runpy
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "5144a6b5f43225d8021a469f4d24c19558026b9e"
BASE = "b37a5aec4ea03f2223d8e09dd5d386d055c24179"
CONTROLS = os.path.join(REPO, ".ufo/waves/round-70/controls/c2-controls-r70.json")
HELD = os.path.join(REPO, ".ufo/waves/round-69/controls/c2-controls-r69.json")
BASE_COUNTER = "quality/counters/c2-r69-guard-dominance.py"
R70_COUNTER = "quality/counters/c2-r70-carriers.py"
SCRATCH = "/fast/scratch/hyaku/mado-r70/R70ExecC2Rule"


def git_show(sha, path):
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (sha, path)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout


def load_module(path, name):
    return runpy.run_path(path, run_name="probe_" + name)


def load_cases(path):
    with open(path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)["cases"], digest


def main():
    out = []
    say = out.append

    # ---- population, independent of the counter
    pop = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", REV,
                          "--", "quality"], stdout=subprocess.PIPE, check=True).stdout
    import re
    population = sorted(p for p in pop.decode().splitlines()
                        if re.fullmatch(r"quality/check-[^/]+\.py", p))
    say("POPULATION_COUNT %d" % len(population))

    counter_path = os.environ.get("R70_COUNTER_PATH", os.path.join(REPO, R70_COUNTER))
    with open(counter_path, "rb") as fh:
        say("R70_COUNTER path=%s sha256=%s" % (counter_path,
                                               hashlib.sha256(fh.read()).hexdigest()))
    r70 = load_module(counter_path, "r70")
    readers = guarded = 0
    for path in population:
        src = git_show(REV, path).decode("utf-8", "replace")
        reader, guard = r70["classify"](src)
        readers += int(reader)
        guarded += int(guard)
        say("POP %-36s reader=%s guard=%s" % (path, "yes" if reader else "no",
                                              "yes" if guard else "no"))
    say("POPULATION_TALLY population=%d readers=%d guarded=%d unguarded=%d"
        % (len(population), readers, guarded, readers - guarded))

    # ---- base leg by hand: the round-69 classifier at the base rev
    base_src = git_show(BASE, BASE_COUNTER)
    base_path = os.path.join(SCRATCH, "c2-r69-at-base.py")
    with open(base_path, "wb") as fh:
        fh.write(base_src)
    say("BASE_COUNTER sha256=%s bytes=%d" % (hashlib.sha256(base_src).hexdigest(), len(base_src)))
    base = load_module(base_path, "r69")

    cases, digest = load_cases(CONTROLS)
    say("CONTROLS cases=%d sha256=%s" % (len(cases), digest))
    base_correct = 0
    for case in cases:
        reader, guard = base["classify"](case["src"])
        ok = reader == case["expect_reader"] and guard == case["expect_guard"]
        base_correct += int(ok)
        say("BASE %-34s reader=%s expect=%s guard=%s expect=%s correct=%s"
            % (case["name"], "yes" if reader else "no",
               "yes" if case["expect_reader"] else "no",
               "yes" if guard else "no", "yes" if case["expect_guard"] else "no",
               "yes" if ok else "NO"))
    say("BASE_SCORE %d/%d" % (base_correct, len(cases)))

    held_cases, held_digest = load_cases(HELD)
    by_name = {c["name"]: c for c in cases}
    carried = 0
    for hc in held_cases:
        mine = by_name.get(hc["name"])
        if mine and mine["src"] == hc["src"] \
                and mine["expect_reader"] == hc["expect_reader"] \
                and mine["expect_guard"] == hc["expect_guard"]:
            carried += 1
    say("HELD cases=%d sha256=%s carried_byte_identical=%d/%d"
        % (len(held_cases), held_digest, carried, len(held_cases)))

    # ---- probes beyond the frozen 17
    probes = [
        ("a-two-hop-alias", "yes", "runtime guard reaches the child; rule promises one alias hop only",
         'def run(repo):\n'
         '    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n'
         '    a = env\n'
         '    b = a\n'
         '    b["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
         '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'),
        ("b-alias-then-env-rebound", "no", "alias-carried requires no rebinding of the env name after the guard",
         'def run(repo):\n'
         '    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n'
         '    alias = env\n'
         '    alias["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
         '    env = {"PATH": "/usr/bin"}\n'
         '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'),
        ("c-other-attribute-passed", "no", "attribute-carried requires the guarded attribute itself as env=",
         'class Runner:\n'
         '    def __init__(self):\n'
         '        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n'
         '        self.other = {"PATH": "/usr/bin"}\n'
         '        self.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n'
         '    def head(self, repo):\n'
         '        return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=self.other)\n'),
        ("d-splat-without-key", "no", "splat-carried needs a mapping constant that carries the key",
         'EXTRA = {"PATH": "/usr/bin"}\n\n\n'
         'def run(repo):\n'
         '    env = {**os.environ, **EXTRA}\n'
         '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'),
        ("e-constant-rebound", "no", "constant-key needs a module constant whose single binding equals the key",
         'KEY = "GIT_NO_REPLACE_OBJECTS"\n'
         'KEY = "OTHER"\n\n\n'
         'def run(repo):\n'
         '    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n'
         '    env[KEY] = "1"\n'
         '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'),
        ("f-dict-kwargs-only", "yes", "splat-carried reads `**GUARD` as unpacked into the mapping handed to env",
         'GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}\n\n\n'
         'def run(repo):\n'
         '    env = dict(**GUARD)\n'
         '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'),
        ("g-dict-with-kwargs", "yes", "same as f with a base mapping argument",
         'GUARD = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}\n\n\n'
         'def run(repo):\n'
         '    env = dict(os.environ, **GUARD)\n'
         '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'),
    ]
    for name, expected, rule, src in probes:
        reader, guard = r70["classify"](src)
        breader, bguard = base["classify"](src)
        if expected == "yes" and (reader is False or guard is False):
            diff = "FALSE_NEGATIVE"
        elif expected == "no" and (reader is False or guard is True):
            diff = "FALSE_POSITIVE"
        else:
            diff = "MATCH"
        say("PROBE %-26s reader=%s expected_reader=yes guard=%s expected_guard=%s diff=%s base=(%s,%s) rule=%s"
            % (name, "yes" if reader else "no", "yes" if guard else "no", expected, diff,
               "yes" if breader else "no", "yes" if bguard else "no", rule))

    print("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
