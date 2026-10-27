#!/usr/bin/env python3
"""Authoring-time case builder for the ExecControlsC1 controls. NOT a counter and NOT part of the lane.

It compiles keymaps with the PINNED xkbcli-compile-keymap in a clean environment (env -i PATH=/usr/bin,
HOME/XDG_CONFIG_HOME under --work, so no user xkb include path exists), runs the PINNED how-to-type on each
(keymap, keysym), and writes a cases.json that the cheat controls embed. The scored comparison later is done by
score-controls.py, which recompiles every keymap at score time and runs the judge again; this file only exists so
the "cached answer table" / "overfit" controls have something plausible to cheat with.

Pins (host, this round):
  /usr/lib/xkbcommon/xkbcli-compile-keymap sha256 43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250
  /usr/lib/xkbcommon/xkbcli-how-to-type     sha256 f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54
  libxkbcommon 1.13.2-1, xkeyboard-config 2.48
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys

COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"

# Fixed fixture set: the cases a "correct on fixtures, wrong elsewhere" control is authored against.
FIXTURES = [
    ("us", "", "", "s"),
    ("us", "", "", "slash"),
    ("br", "", "compose:caps", "slash"),
    ("br", "", "compose:caps", "Return"),
    ("br", "", "compose:caps", "nosuchsym"),
    ("br", "", "compose:caps", "F35"),
    ("us", "", "", "0x0061"),
    ("us,ru", "", "grp:alt_shift_toggle", "Cyrillic_a"),
    ("us", "intl", "", "dead_acute"),
    ("de", "", "", "ssharp"),
    ("fr", "", "", "eacute"),
    ("us", "", "lv3:ralt_switch", "EuroSign"),
    ("us", "", "", "space"),
    ("us", "", "caps:escape", "Escape"),
]

LAYOUTS = ["us", "br", "de", "fr", "ru", "gb", "es", "it", "pl", "cz", "se", "no", "us,ru", "br,us"]
VARIANTS = ["", "", "intl", "nodeadkeys", "phonetic"]
OPTIONS = ["", "compose:caps", "grp:alt_shift_toggle", "ctrl:nocaps", "lv3:ralt_switch",
           "caps:escape", "eurosign:e"]
KEYSYMS = ["a", "s", "slash", "backslash", "numbersign", "Return", "Tab", "space", "bracketleft",
           "bracketright", "Cyrillic_a", "ssharp", "eacute", "EuroSign", "dead_acute", "0x0061",
           "0x002f", "F35", "Escape", "0", "0x0"]


def clean_env(work):
    home = os.path.join(work, "home")
    xdg = os.path.join(work, "xdg")
    os.makedirs(home, exist_ok=True)
    os.makedirs(xdg, exist_ok=True)
    return {"PATH": "/usr/bin", "HOME": home, "XDG_CONFIG_HOME": xdg}


def compile_keymap(work, layout, variant, options, env):
    argv = [COMPILE, "--layout", layout]
    if variant:
        argv += ["--variant", variant]
    if options:
        argv += ["--options", options]
    p = subprocess.run(argv, capture_output=True, env=env, timeout=120)
    if p.returncode != 0:
        return None, p.stderr.decode("utf-8", "replace")
    return p.stdout, ""


def judge(keymap_path, keysym, env):
    p = subprocess.run([JUDGE, "--keymap=" + keymap_path, "--disable-compose", "--keysym", keysym],
                       capture_output=True, env=env, timeout=120)
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), p.stderr.decode("utf-8", "surrogateescape")


def gen_candidates(nonce, count):
    """Yields distinct (layout, variant, options, keysym) candidates; the caller skips the ones that do not compile."""
    rng = random.Random("mado-r49-controls-%d" % nonce)
    seen, n = set(), 0
    while n < count:
        layout = rng.choice(LAYOUTS)
        variant = rng.choice(VARIANTS)
        options = rng.choice(OPTIONS)
        keysym = rng.choice(KEYSYMS)
        key = (layout, variant, options, keysym)
        if key in seen:
            continue
        seen.add(key)
        n += 1
        yield key


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--nonce", type=int, default=49)
    ap.add_argument("--gen", type=int, default=30)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    if work == "/tmp" or work.startswith("/tmp/"):
        sys.exit("refusing a --work under /tmp (SentScratch)")
    env = clean_env(work)
    kmdir = os.path.join(work, "km")
    os.makedirs(kmdir, exist_ok=True)

    specs = [("fx-%02d" % i, f) for i, f in enumerate(FIXTURES)]
    cases, skipped = [], 0
    for cid, (layout, variant, options, keysym) in specs:
        data, err = compile_keymap(work, layout, variant, options, env)
        if data is None:
            skipped += 1
            print("skip %s: compile failed: %s" % (cid, err.strip().splitlines()[:1]), file=sys.stderr)
            continue
        sha = hashlib.sha256(data).hexdigest()
        path = os.path.join(kmdir, sha + ".keymap")
        with open(path, "wb") as fh:
            fh.write(data)
        rc, out, errout = judge(path, keysym, env)
        cases.append({"id": cid, "layout": layout, "variant": variant, "options": options,
                      "keysym": keysym, "keymap_sha256": sha, "rc": rc, "stdout": out,
                      "stderr_first": errout.splitlines()[0] if errout else ""})

    # Generated cases: RMLVO combinations that do not exist in xkeyboard-config 2.48 are skipped and redrawn, so a
    # nonce still yields the requested number of scoreable cases.
    got = 0
    for layout, variant, options, keysym in gen_candidates(a.nonce, a.gen * 8):
        if got >= a.gen:
            break
        data, err = compile_keymap(work, layout, variant, options, env)
        if data is None:
            skipped += 1
            continue
        sha = hashlib.sha256(data).hexdigest()
        path = os.path.join(kmdir, sha + ".keymap")
        with open(path, "wb") as fh:
            fh.write(data)
        rc, out, errout = judge(path, keysym, env)
        cases.append({"id": "gen-%02d" % got, "layout": layout, "variant": variant, "options": options,
                      "keysym": keysym, "keymap_sha256": sha, "rc": rc, "stdout": out,
                      "stderr_first": errout.splitlines()[0] if errout else ""})
        got += 1

    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump({"nonce": a.nonce, "cases": cases, "skipped": skipped}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("cases=%d skipped=%d -> %s" % (len(cases), skipped, a.out))
    print("rcs=%s" % sorted({c["rc"] for c in cases}))
    print("empty_tables=%d" % sum(1 for c in cases if c["rc"] == 0 and c["stdout"].count("\n") == 5))


if __name__ == "__main__":
    main()
