#!/usr/bin/env python3
"""ExecDoNothing / round 50 - section-9 C2 controls, scored with the FROZEN PRED-C2-r49.

The counter scored is the committed `quality/counters/c2-r49-bind-entry.py` at 13631f24 (never a
draft). Every control is one commit on top of 13631f24 in its own scratch clone of the lane, and
every control shares one host tree - the round-49 candidate data that was never committed:

  * corpus/knowledge/hyprland-bind-key-match-r49.md      <- `.ufo/waves/round-49/candidate/`
  * corpus/SOURCES.md        <- the 12 candidate rows S352-S363 (`candidate/rows.md`)
  * corpus/README.md         <- one index row, rows S352-S363
  * corpus/lessons/round-49.md <- the Gate section plus the 12 `**S### admit**` lines the lesson
                                  points at (`.ufo/waves/round-49/w1/ScrRows/gate.md` section 1)
  * pins and the live receipt are already committed at 13631f24

so the only variable between runs is the entry (or the receipt):

  c10-candidate        the candidate entry as drafted
  c11-receipt-removed  the candidate entry with its live receipt deleted
  c12-stub             the candidate head + one sentence
  c13-paste-2-3        the candidate head + held keybind-rule-semantics section 2.3 verbatim

Usage: run with HOME/XDG_*/TMPDIR under /fast/scratch/hyaku/mado-r50/ExecDoNothing and the
inherited read-only compositor socket variables. Writes ../receipts/c2-<control>.txt.
"""
import os
import shutil
import subprocess
import sys

SEAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the lane is derived from this seat's own path (no absolute home path in committed code):
# SEAT is .../w1/ExecDoNothing (this file lives in its controls/), five levels below it
LANE = os.path.realpath(os.path.join(SEAT, "..", "..", "..", "..", ".."))
if not os.path.isfile(os.path.join(LANE, "SKILL.md")):
    raise SystemExit("lane derivation failed: %r has no SKILL.md" % LANE)
COUNTER = os.path.join(LANE, "quality/counters/c2-r49-bind-entry.py")
SCRATCH = "/fast/scratch/hyaku/mado-r50/ExecDoNothing/c2"
OUT = os.path.join(SEAT, "receipts")
ENTRY = "corpus/knowledge/hyprland-bind-key-match-r49.md"
RECEIPT = ".ufo/waves/round-49/receipts/binds-live-r49.txt"
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
REV0 = "13631f24050f22db92bf5bd33e0f4d014192992e"
CAND = os.path.join(LANE, ".ufo/waves/round-49/candidate")
GATE = os.path.join(LANE, ".ufo/waves/round-49/w1/ScrRows/gate.md")
HELD = os.path.join(LANE, "corpus/knowledge/keybind-rule-semantics.md")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, env=ENV)
    if check and p.returncode != 0:
        raise SystemExit("git %s -> %d\n%s%s" % (args, p.returncode, p.stdout[-2000:], p.stderr[-2000:]))
    return p


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def head_of(entry_text):
    """The provenance head: everything through the `Lane:`/`Round:` line."""
    out = []
    for line in entry_text.splitlines(True):
        out.append(line)
        if line.startswith("Lane: "):
            return "".join(out)
    raise SystemExit("no Lane: line in the candidate entry")


def held_23():
    """Held `keybind-rule-semantics.md` section 2.3, verbatim (its heading through 2.3's table)."""
    lines = read(HELD).splitlines(True)
    start = next(i for i, l in enumerate(lines) if l.startswith("### 2.3 "))
    end = next(i for i, l in enumerate(lines[start + 1:], start + 1) if l.startswith("### 2.4"))
    return "".join(lines[start:end])


def held_prose(count):
    """The first `count` held prose lines of at least 60 characters (not a table row, not a heading)."""
    out = []
    for line in read(HELD).splitlines(True):
        s = line.strip()
        if len(s) < 60 or s.startswith("|") or s.startswith("#"):
            continue
        out.append(line if line.endswith("\n") else line + "\n")
        if len(out) >= count:
            break
    if len(out) < count:
        raise SystemExit("held prose lines: %d < %d" % (len(out), count))
    return "".join(out)


def apply_host_tree(repo):
    # 1. the candidate entry
    write(os.path.join(repo, ENTRY), read(os.path.join(CAND, "hyprland-bind-key-match-r49.md")))
    # 2. registry rows, inside the Registry section
    rows = [l for l in read(os.path.join(CAND, "rows.md")).splitlines(True) if l.startswith("| S3")]
    if len(rows) != 12:
        raise SystemExit("candidate rows: %d, expected 12" % len(rows))
    src = read(os.path.join(repo, "corpus/SOURCES.md")).splitlines(True)
    cut = next(i for i, l in enumerate(src) if l.startswith("## Paths"))
    src[cut:cut] = ["\n"] + rows
    write(os.path.join(repo, "corpus/SOURCES.md"), "".join(src))
    # 3. README index row, after the round-48 knowledge row
    readme = read(os.path.join(repo, "corpus/README.md")).splitlines(True)
    at = next(i for i, l in enumerate(readme)
              if "knowledge/xkb-keymap-compile-r48.md" in l and l.startswith("|"))
    readme[at + 1:at + 1] = [
        "| `knowledge/hyprland-bind-key-match-r49.md` (MADO-R49-2, round 49; bind key matching) | "
        "How Hyprland 0.56.2 turns the key field of a bind line into a key press match: the key "
        "name to keysym resolution, the xkb state the pressed keysym is read from, the level and "
        "layout it resolves, and the exact modifier-mask comparison | rows S352-S363 |\n"]
    write(os.path.join(repo, "corpus/README.md"), "".join(readme))
    # 4. lesson Gate admits for every new row
    admits = [l for l in read(GATE).splitlines(True) if l.startswith("- **S3") and " admit**" in l]
    if len(admits) != 12:
        raise SystemExit("gate admits: %d, expected 12" % len(admits))
    lesson = read(os.path.join(repo, "corpus/lessons/round-49.md")).splitlines(True)
    end = next(i for i, l in enumerate(lesson) if l.startswith("## Mistakes"))
    lesson[end:end] = ["\n"] + admits
    write(os.path.join(repo, "corpus/lessons/round-49.md"), "".join(lesson))


def build(name):
    root = os.path.join(SCRATCH, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    home = os.path.join(root, "home")
    os.makedirs(home)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    for var in ("XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME"):
        env[var] = os.path.join(home, var.lower())
        os.makedirs(env[var])
    env["HOME"] = home
    env["TMPDIR"] = os.path.join(root, "tmp")
    os.makedirs(env["TMPDIR"])
    repo = os.path.join(root, "repo")
    subprocess.run(["git", "clone", "-q", "--shared", LANE, repo], env=env, check=True)
    subprocess.run(["git", "-C", repo, "checkout", "-q", REV0], env=env, check=True)
    top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, env=env).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("fixture toplevel %r != %r" % (top, repo))
    apply_host_tree(repo)
    entry = read(os.path.join(CAND, "hyprland-bind-key-match-r49.md"))
    if name == "c12-stub":
        write(os.path.join(repo, ENTRY), head_of(entry) + "\n"
              "This entry states which keysym of a pressed key a Hyprland bind line is matched "
              "against.\n")
    elif name == "c13-paste-2-3":
        write(os.path.join(repo, ENTRY), head_of(entry) + "\n" + held_23())
    elif name == "c14-paste-2-3-prose":
        # supplementary probe (not one of the six required controls): the same held 2.3 paste plus
        # eight held prose lines, so the novelty sample floor (>=8 body lines, >=150 shingles) is
        # reachable and the duplicate-line / shingle nets can be measured on a paste that survives it.
        write(os.path.join(repo, ENTRY), head_of(entry) + "\n" + held_23() + "\n" + held_prose(8))
    elif name == "c11-receipt-removed":
        subprocess.run(["git", "-C", repo, "rm", "-q", RECEIPT], env=env, check=True)
    elif name != "c10-candidate":
        raise SystemExit("unknown control %r" % name)
    subprocess.run(["git", "-C", repo, "add", "-A"], env=env, check=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@local",
                    "commit", "-q", "-m", "control %s" % name], env=env, check=True)
    rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True,
                         text=True, env=env).stdout.strip()
    return repo, rev, env


def score(name, repo, rev, env):
    cmd = [sys.executable, "-I", COUNTER, "--repo", repo, "--rev", rev, "--base", BASE]
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    body = p.stdout + p.stderr
    head = ("# ExecDoNothing round 50 - C2 control %s\n"
            "# counter: %s (sha256 %s)\n"
            "# cmd: TMPDIR=%s HOME=%s %s\n"
            "# expected: verdict=TARGET_MISSED\n"
            "# exit: %d\n\n" % (
                name, COUNTER, sha256(COUNTER), env.get("TMPDIR"), env.get("HOME"),
                " ".join(cmd), p.returncode))
    with open(os.path.join(OUT, "c2-%s.txt" % name), "w", encoding="utf-8") as fh:
        fh.write(head + body)
    final = [l for l in body.splitlines() if l.startswith("PRED-C2-r49:")]
    clauses = [l for l in body.splitlines() if " clauses=" in l and "admitted=" in l]
    print("%-20s rc=%d %s" % (name, p.returncode, final[-1] if final else "NO FINAL LINE"))
    if clauses:
        print("    %s" % clauses[-1])
    return p.returncode, (final[-1] if final else ""), (clauses[-1] if clauses else "")


def main():
    for p in (SCRATCH,):
        rp = os.path.realpath(p)
        if not rp.startswith("/fast/scratch/hyaku/mado-r50/ExecDoNothing"):
            raise SystemExit("scratch root %r is not under my /fast/scratch tree" % p)
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or ["c10-candidate", "c11-receipt-removed", "c12-stub", "c13-paste-2-3",
                             "c14-paste-2-3-prose"]
    recs = []
    for name in names:
        repo, rev, env = build(name)
        recs.append((name, rev) + score(name, repo, rev, env))
    lines = ["control              rc  rev                                      final line"]
    for name, rev, rc, final, _clauses in recs:
        lines.append("%-20s %d  %s %s" % (name, rc, rev, final))
    with open(os.path.join(OUT, "c2-controls.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
