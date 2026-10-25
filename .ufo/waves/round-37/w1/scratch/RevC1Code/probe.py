#!/usr/bin/env python3
"""RevC1Code falsifier probes: score adversarial sandbox trees with the frozen C1 counter.

Builds every tree in one sandbox clone under /dev/shm/mado37-RevC1Code (never the lane),
reusing the frozen controls.py builders read-only, commits with a sandbox identity, and
scores with the lane's frozen counter at the sandbox HEAD (default base).
"""
import hashlib
import importlib.util
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
spec = importlib.util.spec_from_file_location("controls", f"{LANE}/.ufo/waves/round-37/controls.py")
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)
SB = "/dev/shm/mado37-RevC1Code/sb"
E1, E2, ENV, BASE = ctl.E1, ctl.E2, ctl.ENV, ctl.BASE


def rd(rel):
    return open(os.path.join(SB, rel)).read()


def add_rows(text):
    src = rd("corpus/SOURCES.md")
    head, tail = src.split("\n## Paths", 1)
    ctl.write(SB, "corpus/SOURCES.md", head.rstrip("\n") + "\n" + text + "\n## Paths" + tail)


def add_readme(cells):
    r = rd("corpus/README.md")
    head, tail = r.split("\n## Quality bar", 1)
    add = "".join(f"| {c} | x | y |\n" for c in cells)
    ctl.write(SB, "corpus/README.md", head.rstrip("\n") + "\n" + add + "\n## Quality bar" + tail)


def self_receipt():
    """No source receipt at all: each entry is bound as its own receipt."""
    gates = []
    for path, i, toks in ((E1, "S990", ["MAX_QUEUED_EVENTS", "overflowed event queue"]),
                          (E2, "S991", ["debug:disable_logs", "m_logsEnabled"])):
        q = f"this sentence is evidence for {i} only because it says so"
        body = (f"# self-bound stub\n\nsource: {i}\nverified-at: 2026-10-25\nrecheck: 90d\n\n"
                f"{' and '.join(toks)}.\n**OBS** {i}: {q}\n")
        ctl.write(SB, path, body)
        d = hashlib.sha256(body.encode()).hexdigest()
        gates.append(f'GATE {i} receipt={path} sha256={d} quote="{q}"')
    add_rows(ctl.row("S990", E1) + ctl.row("S991", E2))
    ctl.write(SB, "corpus/lessons/round-37.md", "# r37\n\n## Gate\n\n" + "\n".join(gates) + "\n")
    add_readme([f"`knowledge/{E1.rsplit('/', 1)[1]}`", f"`knowledge/{E2.rsplit('/', 1)[1]}`"])


def trivial_quote(q):
    def build():
        ctl.wire(SB, quote=q, stated=False)
        for path, ids in ((E1, "S189 S201 S212"), (E2, "S213 S214")):
            ctl.write(SB, path, rd(path) + f"**OBS** {ids}\n")
    return build


def dup_row():
    ctl.wire(SB)
    add_rows("| S189 | a colliding second S189 row | code | A | s | a | t | refused | 2026-10-25 | 90d | - |\n")


def gate_in_foreign_fence():
    ctl.wire(SB)
    lesson = rd("corpus/lessons/round-37.md").replace("## Gate\n", "## Notes\n\nAn example only:\n\n```\n## Gate\n", 1)
    ctl.write(SB, "corpus/lessons/round-37.md", lesson + "```\n")


def obs_on_source_line():
    """No **OBS** observation line in the body; the marker rides the source line."""
    ctl.wire(SB)
    for path, ids, toks in ((E1, ("S189", "S201", "S212"), "MAX_QUEUED_EVENTS and overflowed event queue"),
                            (E2, ("S213", "S214"), "debug:disable_logs and m_logsEnabled")):
        quotes = "".join(f"quoted: `{ctl.QUOTES[i]}`\n" for i in ids)
        ctl.write(SB, path, f"# stub\n\nsource: {', '.join(ids)} **OBS**\nverified-at: 2026-10-25\n"
                            f"recheck: 90d\n\n{toks}.\n{quotes}")


def header_at_line16():
    ctl.wire(SB)
    for path in (E1, E2):
        b = rd(path).split("\n", 2)
        ctl.write(SB, path, b[0] + "\n" + "pad\n" * 14 + b[2])


def uncited_late_source():
    ctl.wire(SB)
    for path in (E1, E2):
        ctl.write(SB, path, rd(path) + "\n" * 20 + "source: S999\n")


def readme_retired_cell():
    ctl.wire(SB, readme=False)
    add_readme([f"`knowledge/{E1.rsplit('/', 1)[1]}.retired`", f"`old-knowledge/{E2.rsplit('/', 1)[1]}x`"])


CASES = [
    ("golden-v2-repro", lambda: ctl.wire(SB)),
    ("self-receipt", self_receipt),
    ("space-quote", trivial_quote(" ")),
    ("one-char-quote", trivial_quote("e")),
    ("dup-row-refused", dup_row),
    ("gate-in-foreign-fence", gate_in_foreign_fence),
    ("obs-on-source-line", obs_on_source_line),
    ("header-at-line16", header_at_line16),
    ("uncited-late-source", uncited_late_source),
    ("readme-retired-cell", readme_retired_cell),
]


def sh(*cmd):
    return subprocess.run(cmd, env=ENV, capture_output=True, text=True)


def main():
    if not os.path.isdir(SB):
        sh("git", "clone", "-q", "--no-local", LANE, SB)
    for name, build in CASES:
        sh("git", "-C", SB, "checkout", "-q", "-f", "--detach", BASE)
        sh("git", "-C", SB, "clean", "-qfdx")
        build()
        sh("git", "-C", SB, "add", "-A")
        sh("git", "-C", SB, "commit", "-q", "--allow-empty", "-m", f"probe {name}")
        p = subprocess.run([sys.executable, "-I", f"{LANE}/quality/counters/c1-r37-event-ground.py",
                            "--repo", SB, "--rev", "HEAD"], capture_output=True, text=True, env=ENV)
        print(f"case={name} rc={p.returncode}")
        for line in p.stdout.strip().splitlines():
            print("  " + line.replace(" base=" + BASE, ""))
        if p.stderr.strip():
            print("  stderr: " + p.stderr.strip().splitlines()[-1])


if __name__ == "__main__":
    main()
