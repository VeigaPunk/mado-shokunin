#!/usr/bin/env python3
"""Attack seat: build junk C1 entries from frozen-tables.json and run the C1 legs and the 7 frozen controls.

usage: python3 -I build_junk_and_controls.py <BASE_REPO_WITH_FREEZE> <WORK_DIR>
Every temp repo is created under WORK_DIR; each is checked with `git rev-parse --show-toplevel` first.
"""
import json, os, random, subprocess, sys, tempfile

BASE, WORK = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "c1_attack_check.py")
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
COMMIT = "efb50993780079460b0cbed1363e2166a2de1d9f"
ENTRY_PATH_IN_REGISTRY = ENTRY

T = json.load(open(os.path.join(BASE, TABLES)))["c1"]
PIN_SHA = T["pin_sha256"]


def git(d, *args, check=True):
    return subprocess.run(["git", "-C", d, *args], check=check, capture_output=True, text=True).stdout.strip()


def new_repo_from(src, tag):
    """Fresh scratch repo whose single commit is the HEAD tree of `src`. Asserts toplevel first."""
    d = tempfile.mkdtemp(prefix=f"{tag}-", dir=WORK)
    a = subprocess.Popen(["git", "-C", src, "archive", "HEAD"], stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", d], stdin=a.stdout, check=True)
    a.wait()
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    assert os.path.realpath(git(d, "rev-parse", "--show-toplevel")) == os.path.realpath(d)
    return d


def commit(d, msg):
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl",
                    "commit", "-q", "-m", msg], check=True)
    return git(d, "rev-parse", "HEAD")


# ---- junk construction -------------------------------------------------------------------------

# sid per K row: existing registry rows where they exist; new rows S378-S380 per registration §C1;
# S381 is a FABRICATED row (URL text ends in the wayland suffix and contains the Hyprland commit).
SID_K = {}
for k in T["k"]:
    p = k["pin"]
    SID_K[k["id"]] = {
        "Hyprland-InputManager.cpp": "S316", "Hyprland-IKeyboard.cpp": "S319",
        "Hyprland-SeatManager.cpp": "S378", "Hyprland-protocols-core-Seat.cpp": "S379",
        "Hyprland-IKeyboard.hpp": "S380", "Hyprland-ConfigValues.cpp": "S318",
        "Hyprland-legacy-ConfigManager.cpp": "S317", "wayland-1.26.0-wayland.xml": "S381",
    }[p]

WORDS = ("keyboard seat pointer timer value default config row quote pin host line rate delay "
         "numlock option global device keymap layout compositor event repeat buffer frame "
         "source entry index claim table anchor record").split()


def junk_entry(variant, k17_sid):
    lines = [
        "# Keyboard repeat rate, repeat delay and numlock (round 55)",
        "",
        "source: S316, S317, S318, S319, S378, S379, S380, S381",
        "verified-at: 2026-10-28",
        "recheck: on-release",
        "",
        "| id | proposition | source | anchor | quote |",
        "|---|---|---|---|---|",
    ]
    rng = random.Random(7)
    for kind, rows in (("K", T["k"]), ("H", T["h"])):
        for r in rows:
            rid, pin, line, quote = r["id"], r["pin"], r["line"], r["quote"]
            if variant == "filler":
                prop = (f"Placeholder proposition for row {rid} that pads the length check and asserts "
                        f"nothing about the pinned code at all.") if kind == "K" else \
                       f"Filler host row {rid}, padding text, no claim here at all."
            else:  # stuffed: quote identifiers copied in, lexical variety from a seeded word salad
                toks = [t for t in quote.replace("(", " ").replace(")", " ").replace(",", " ").split() if t.isidentifier()][:2] or ["value", "line"]
                prop = (" ".join(rng.sample(WORDS, 8)) + f" names {toks[0]} and {toks[-1]} from {pin}:{line}.")
            sid = "host" if kind == "H" else (k17_sid if rid == "K17" else SID_K[rid])
            lines.append(f"| {rid} | {prop} | {sid} | {pin}:{line} | `{quote.replace('|', chr(92) + '|')}` |")
    return "\n".join(lines) + "\n"


def registry_rows(k17_sid):
    sha = PIN_SHA
    rows = [
        ("S378", "Hyprland v0.56.2 seat manager - keyboard repeat info (attack filler)",
         f"https://raw.githubusercontent.com/hyprwm/Hyprland/{COMMIT}/src/managers/SeatManager.cpp", "code",
         f"sha256:{sha['Hyprland-SeatManager.cpp']}"),
        ("S379", "Hyprland v0.56.2 core seat protocol - repeat info (attack filler)",
         f"https://raw.githubusercontent.com/hyprwm/Hyprland/{COMMIT}/src/protocols/core/Seat.cpp", "code",
         f"sha256:{sha['Hyprland-protocols-core-Seat.cpp']}"),
        ("S380", "Hyprland v0.56.2 keyboard header - repeat members (attack filler)",
         f"https://raw.githubusercontent.com/hyprwm/Hyprland/{COMMIT}/src/devices/IKeyboard.hpp", "code",
         f"sha256:{sha['Hyprland-IKeyboard.hpp']}"),
        ("S381", "Wayland 1.26.0 protocol XML (attack filler, FABRICATED URL in Hyprland repo path)",
         f"https://raw.githubusercontent.com/hyprwm/Hyprland/{COMMIT}/1.26.0/protocol/wayland.xml", "spec",
         f"sha256:{sha['wayland-1.26.0-wayland.xml']}"),
    ]
    out = []
    for sid, title, url, kind, shatxt in rows:
        out.append(f"| {sid} | {title} - {url} | {kind} | A | commit {COMMIT[:8]}, {shatxt} | filler anchor | filler teaches "
                   f"| mined | 2026-10-28 | 90d | {ENTRY_PATH_IN_REGISTRY} |")
    return out


def build(variant, k17_sid, tag):
    d = new_repo_from(BASE, tag)
    # registry: append after last S377 line
    p = os.path.join(d, SOURCES)
    L = open(p, encoding="utf-8").read().split("\n")
    idx = max(i for i, l in enumerate(L) if l.startswith("| S377 "))
    L[idx + 1:idx + 1] = registry_rows(k17_sid)
    open(p, "w", encoding="utf-8").write("\n".join(L))
    # README: one index row after the r53 errata row
    p = os.path.join(d, README)
    L = open(p, encoding="utf-8").read().split("\n")
    idx = max(i for i, l in enumerate(L) if l.startswith("| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`"))
    L.insert(idx + 1, "| `knowledge/hyprland-keyboard-repeat-numlock-r55.md` (round 55; attack filler) | filler | `source:` S316-S381 in [SOURCES](SOURCES.md) |")
    open(p, "w", encoding="utf-8").write("\n".join(L))
    os.makedirs(os.path.dirname(os.path.join(d, ENTRY)), exist_ok=True)
    open(os.path.join(d, ENTRY), "w", encoding="utf-8").write(junk_entry(variant, k17_sid))
    rev = commit(d, f"attack junk {variant} k17={k17_sid}")
    return d, rev


def check(d, rev, propose=False, escaped=True):
    cmd = ["python3", "-I", CHECK, "--repo", d, "--rev", rev, "--work", WORK]
    if escaped:
        cmd.append("--escaped-pipes")
    if propose:
        cmd.append("--propose-clause")
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


# ---- the 7 frozen controls (registration §C1 table), applied to a copy of the junk-filler repo ----

def edit_row(text, rid, old, new):
    out, hit = [], 0
    for l in text.split("\n"):
        if l.startswith(f"| {rid} |"):
            assert old in l, (rid, old)
            l = l.replace(old, new, 1)
            hit += 1
        out.append(l)
    assert hit == 1, rid
    return "\n".join(out)


def controls(good_repo):
    specs = [
        ("C1-CTL-1 absent", "entry_absent", lambda d: os.remove(os.path.join(d, ENTRY))),
        ("C1-CTL-2 spliced-quote", "quote:K04",
         lambda d: _edit(d, lambda t: edit_row(t, "K04", "std::max(0, REPEATRATE);", "std::max(0, REPEATRATE) ;"))),
        ("C1-CTL-3 shifted-anchor", "anchor:K01",
         lambda d: _edit(d, lambda t: edit_row(t, "K01", ":1220", ":1219"))),
        ("C1-CTL-4 wrong-source", "source_cell:K10",
         lambda d: _edit(d, lambda t: edit_row(t, "K10", " S378 ", " S316 "))),
        ("C1-CTL-5 dropped-row", "row:K17",
         lambda d: _edit(d, lambda t: "\n".join(l for l in t.split("\n") if not l.startswith("| K17 |")))),
        ("C1-CTL-6 host-forged", "host:H02",
         lambda d: _edit(d, lambda t: edit_row(t, "H02", "repeat_delay = 250", "repeat_delay = 300"))),
        ("C1-CTL-7 pin-tamper", "pin_hash",
         lambda d: _tamper_pin(d)),
    ]
    results = []
    for name, leg, mut in specs:
        d = new_repo_from(good_repo, "ctl")
        mut(d)
        rev = commit(d, name)
        rc, out = check(d, rev)
        first = out.split("\n")[0]
        ok = rc == 1 and "verdict=TARGET_MISSED" in first and f"{leg}" in first.split("missed=")[-1].split(",")
        results.append(ok)
        print(f"CTL {name}: expected={leg} rc={rc} pass={ok} | {first}")
    return sum(results)


def _edit(d, fn):
    p = os.path.join(d, ENTRY)
    t = open(p, encoding="utf-8").read()
    t2 = fn(t)
    assert t2 != t
    open(p, "w", encoding="utf-8").write(t2)


def _tamper_pin(d):
    # one hex nibble of Hyprland-IKeyboard.cpp's sha256 in the tree's copy of frozen-tables.json, AND append one space to the pin
    p = os.path.join(d, TABLES)
    t = open(p, encoding="utf-8").read()
    old = PIN_SHA["Hyprland-IKeyboard.cpp"]
    assert t.count(old) == 1
    new = old[:-1] + ("e" if old[-1] != "e" else "f")
    open(p, "w", encoding="utf-8").write(t.replace(old, new))
    pp = os.path.join(d, T["pin_dir"], "Hyprland-IKeyboard.cpp")
    open(pp, "ab").write(b" ")


def main():
    os.makedirs(WORK, exist_ok=True)
    base_rev = git(BASE, "rev-parse", "HEAD")
    rc, out = check(BASE, base_rev)
    print("BEFORE(base+freeze, no entry):", out.split("\n")[0], "rc=", rc)

    dA, revA = build("filler", "S381", "junkA")
    rcA, outA = check(dA, revA, propose=True)
    print("A junk-filler (K17->S381 fabricated):", revA, "rc=", rcA)
    print(outA)
    rcAL, outAL = check(dA, revA, escaped=False)
    print("A under LITERAL grammar (no escaped pipes):", rcAL)
    print(outAL)

    dB, revB = build("filler", "S052", "junkB")
    rcB, outB = check(dB, revB)
    print("B junk-filler with honest K17->S052:", revB, "rc=", rcB)
    print(outB)

    dC, revC = build("stuffed", "S381", "junkC")
    rcC, outC = check(dC, revC, propose=True)
    print("C junk-stuffed (quote identifiers + word salad):", revC, "rc=", rcC)
    print(outC)

    n = controls(dA)
    print(f"ATTACK_C1_CONTROLS: good={'ok' if rcA == 0 else 'bad'} controls={n}/7")
    print("REPOS", dA, dB, dC)


if __name__ == "__main__":
    main()
