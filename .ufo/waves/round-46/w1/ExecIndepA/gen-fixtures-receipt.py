#!/usr/bin/env python3
"""Build receipts/failing-fixtures.txt: the five fixtures my first build failed, verbatim.

Reads only the frozen fixtures (sha256-pinned by the counter), the seed-46 name table replayed from the counter's
own names(), and my own run-1 counter log.
"""
import json, random, re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
VENDORS = ["razer", "logitech", "hp--inc", "keychron", "yubico", "at-translated-set-2", "elan", "synaptics", "corsair"]
MODELS = ["deathadder-v2", "g502-hero", "hyperx-alloy-origins-core", "k8-pro", "yubikey-otp+fido+ccid", "keyboard",
          "touchpad", "k70-rgb", "mx-master-3"]
SUFFIX = ["", "", "-keyboard", "-mouse", "-consumer-control", "-keypad", "-1", "-2"]


def names(seed):
    rng = random.Random(seed)
    picked = []
    while len(picked) < 4:
        n = "%s-%s%s" % (rng.choice(VENDORS), rng.choice(MODELS), rng.choice(SUFFIX))
        if all(n not in p and p not in n for p in picked):
            picked.append(n)
    return {"{A}": picked[0], "{B}": picked[1], "{C}": picked[2], "{D}": picked[3]}


def subst(obj, table):
    if isinstance(obj, str):
        for k, v in table.items():
            obj = obj.replace(k, v)
        return obj
    if isinstance(obj, list):
        return [subst(x, table) for x in obj]
    if isinstance(obj, dict):
        return {k: subst(v, table) for k, v in obj.items()}
    return obj


table = names(46)
fixtures = {f["label"]: f for f in json.load(open(LANE + "/quality/counters/c1-r46-fixtures.json"))}
log = open("receipts/c1-run1.txt").read().split("\n")
wanted = ["matched-touch", "comment-triple-hash", "block-first-not-name", "rename", "bracket-name-key"]
out = ["# failing fixtures of run 1 (rev e294cec, nonce 2), verbatim; seed-46 names substituted",
       "# fixture source: quality/counters/c1-r46-fixtures.json (sha256 pin in the counter)"]
for label in wanted:
    fx = fixtures[label]
    out.append("=== fixture %s want_rc=%d ===" % (label, fx["rc"]))
    for i, text in enumerate(subst(fx["configs"], table)):
        out.append("config %d: %s" % (i, json.dumps(text)))
    out.append("expect:")
    for line in fx["expect"]:
        out.append(subst(line, table))
    fail = [l for l in log if ("fixture=%s FAIL" % label) in l]
    out.append("run-1 counter line:")
    out.append(fail[0] if fail else "MISSING")
open("receipts/failing-fixtures.txt", "w").write("\n".join(out) + "\n")
print("wrote %d lines" % len(out))
