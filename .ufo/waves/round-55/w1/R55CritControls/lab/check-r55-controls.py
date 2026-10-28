#!/usr/bin/env python3
"""Harness-shaped C1 runner (written from registration §C1 + claims PRED-C1-r55). Scratch only.

Runs the counter on the good tree (--repo, HEAD) and on the seven frozen controls (scratch single-commit
trees built with ctl identity under --work). --expect JSON overrides the expected verdict per control
(value = required leg name, or "TARGET_MET") to model a harness whose expectations live in a mutable file.
"""
import argparse, json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L

CTL_ENTRY = L.ENTRY
FETCH = f"{L.ROUND}/fetch"


def ed(path, prefix, old, new):
    L.edit_line(os.path.join(path), prefix, old, new)


def c1_mut(D):
    os.remove(os.path.join(D, CTL_ENTRY))


def c2_mut(D):
    ed(os.path.join(D, CTL_ENTRY), "| K04 |", "std::max(0, REPEATRATE);", "std::max(0, REPEATRATE) ;")


def c3_mut(D):
    ed(os.path.join(D, CTL_ENTRY), "| K01 |", "Hyprland-InputManager.cpp:1220", "Hyprland-InputManager.cpp:1219")


def c4_mut(D):
    ed(os.path.join(D, CTL_ENTRY), "| K10 |", "| S378 |", "| S316 |")


def c5_mut(D):
    L.drop_line(os.path.join(D, CTL_ENTRY), "| K17 |")


def c6_mut(D):
    ed(os.path.join(D, CTL_ENTRY), "| H02 |", "repeat_delay = 250", "repeat_delay = 300")


def c7_mut(D):
    tb = os.path.join(D, L.ROUND, "frozen-tables.json")
    s = open(tb, encoding="utf-8").read()
    old = "8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d"
    assert s.count(old) == 1
    open(tb, "w", encoding="utf-8").write(s.replace(old, "9a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d"))
    with open(os.path.join(D, FETCH, "Hyprland-IKeyboard.cpp"), "ab") as f:
        f.write(b" ")


CONTROLS = [
    ("C1-CTL-1", "entry_absent", c1_mut),
    ("C1-CTL-2", "quote:K04", c2_mut),
    ("C1-CTL-3", "anchor:K01", c3_mut),
    ("C1-CTL-4", "source_cell:K10", c4_mut),
    ("C1-CTL-5", "row:K17", c5_mut),
    ("C1-CTL-6", "host:H02", c6_mut),
    ("C1-CTL-7", "pin_hash", c7_mut),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--expect", default=None)
    a = ap.parse_args()
    expect = {n: leg for n, leg, _ in CONTROLS}
    if a.expect:
        expect.update(json.load(open(a.expect)))
    os.makedirs(a.work, exist_ok=True)
    log = open(os.path.join(a.work, "harness.log"), "w")
    good_rev = L.resolve(a.repo, "HEAD")
    rc, out = L.run_counter(a.counter, a.repo, good_rev, a.work)
    verdict, missed = L.parse_missed(out)
    good = rc == 0 and verdict == "TARGET_MET" and missed == []
    log.write(f"GOOD rc={rc} out={out}\n")
    k = 0
    for name, leg, mut in CONTROLS:
        D = os.path.join(a.work, "ctl-" + name)
        L.make_control_tree(a.repo, good_rev, D, mut)
        rev = L.resolve(D, "HEAD")
        rc, out = L.run_counter(a.counter, D, rev, a.work)
        verdict, missed = L.parse_missed(out)
        want = expect[name]
        if want == "TARGET_MET":
            passed = rc == 0 and verdict == "TARGET_MET"
        else:
            passed = rc == 1 and verdict == "TARGET_MISSED" and missed is not None and want in missed
        k += passed
        log.write(f"{name} want={want} rc={rc} passed={passed} out={out}\n")
    log.close()
    print(f"MADO_R55_CONTROLS: claim=c1 good={'ok' if good else 'bad'} controls={k}/7 "
          f"verdict={'OK' if good and k == 7 else 'FAIL'}")


if __name__ == "__main__":
    main()
