#!/usr/bin/env python3
"""Seat-written mirror of registration §C1 frozen controls (C1-CTL-1..7) run against c1check.py.
Usage: ctl_c1.py REPO GOOD_REV WORK strict|tolerant. Commits mutants only in the scratch REPO and resets it after each."""
import hashlib, json, os, re, subprocess, sys

repo, good, work, mode = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
CHK = os.path.join(HERE, "c1check.py")
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
IKB = ".ufo/waves/round-55/fetch/Hyprland-IKeyboard.cpp"


def g(*a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout.strip()


def check(rev):
    args = [sys.executable, "-I", CHK, "--repo", repo, "--rev", rev, "--work", work]
    if mode == "strict":
        args.append("--strict-cells")
    p = subprocess.run(args, capture_output=True, text=True)
    return p.stdout.strip(), p.returncode


def reset():
    g("reset", "-q", "--hard", good)


def commit(msg):
    g("add", "-A")
    subprocess.run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-qm", msg,
                    "--allow-empty"], check=True, capture_output=True)
    return g("rev-parse", "HEAD")


def edit_row(path, rid, old, new):
    p = os.path.join(repo, path)
    lines = open(p, encoding="utf-8").read().split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(f"| {rid} |")]
    assert len(idx) == 1, (rid, idx)
    assert old in lines[idx[0]], (rid, old)
    lines[idx[0]] = lines[idx[0]].replace(old, new, 1)
    open(p, "w", encoding="utf-8").write("\n".join(lines))


def drop_row(path, rid):
    p = os.path.join(repo, path)
    lines = open(p, encoding="utf-8").read().split("\n")
    keep = [l for l in lines if not l.startswith(f"| {rid} |")]
    assert len(keep) == len(lines) - 1
    open(p, "w", encoding="utf-8").write("\n".join(keep))


def mut_absent():
    os.remove(os.path.join(repo, ENTRY))


def mut_k04():
    edit_row(ENTRY, "K04", "std::max(0, REPEATRATE);", "std::max(0, REPEATRATE) ;")


def mut_k01():
    edit_row(ENTRY, "K01", ":1220", ":1219")


def mut_k10():
    edit_row(ENTRY, "K10", "| S378 |", "| S316 |")


def mut_k17():
    drop_row(ENTRY, "K17")


def mut_h02():
    edit_row(ENTRY, "H02", "repeat_delay = 250", "repeat_delay = 300")


def mut_pin():
    p = os.path.join(repo, TABLES)
    s = open(p, encoding="utf-8").read()
    m = re.search(r'"Hyprland-IKeyboard\.cpp": "([0-9a-f]{64})"', s)
    h = m.group(1)
    nh = ("9" if h[0] != "9" else "a") + h[1:]
    open(p, "w", encoding="utf-8").write(s.replace(h, nh, 1))
    open(os.path.join(repo, IKB), "a", encoding="utf-8").write(" ")


CONTROLS = [("C1-CTL-1 absent", mut_absent, "entry_absent"), ("C1-CTL-2 spliced-quote", mut_k04, "quote:K04"),
            ("C1-CTL-3 shifted-anchor", mut_k01, "anchor:K01"), ("C1-CTL-4 wrong-source", mut_k10, "source_cell:K10"),
            ("C1-CTL-5 dropped-row", mut_k17, "row:K17"), ("C1-CTL-6 host-forged", mut_h02, "host:H02"),
            ("C1-CTL-7 pin-tamper", mut_pin, "pin_hash")]

reset()
out, rc = check(good)
good_ok = "ok" if (rc == 0 and "verdict=TARGET_MET" in out) else "bad"
print(f"good: {out} rc={rc}")
k = 0
for name, fn, leg in CONTROLS:
    reset()
    fn()
    rev = commit(name)
    out, rc = check(rev)
    legs = out.split("missed=")[-1].split(",") if "missed=" in out else []
    hit = rc == 1 and "verdict=TARGET_MISSED" in out and leg in legs
    k += hit
    print(f"{name}: {out.split('verdict=')[-1] if 'verdict=' in out else out} -> {'named-leg-hit' if hit else 'MISS'}")
reset()
print(f"MADO_R55_CONTROLS: claim=c1 good={good_ok} controls={k}/7 verdict={'OK' if good_ok == 'ok' and k == 7 else 'FAIL'}")
