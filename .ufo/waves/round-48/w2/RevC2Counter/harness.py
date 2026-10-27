#!/usr/bin/env python3
"""RevC2Counter w2 falsification harness: build the C2 data candidate in a scratch clone (index-only, no
large working-tree writes) and score mutated trees with the frozen PRED-C2-r48 counter."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = L + "/.ufo/waves/round-48"
S = "/fast/scratch/hyaku/mado-r48/RevC2Counter"
D = S + "/m/clone"
COUNTER = L + "/quality/counters/c2-r48-xkb-entry.py"
BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
ENTRY = "corpus/knowledge/xkb-keymap-compile-r48.md"
SOURCES = "corpus/SOURCES.md"
README = "corpus/README.md"
FETCH = ".ufo/waves/round-48/fetch/"
HELD_FETCH = ".ufo/waves/round-46/fetch/"
RECEIPTS = ".ufo/waves/round-48/receipts/"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(args, data=None):
    p = subprocess.run(["git", "-C", D] + args, capture_output=True, input=data, env=ENV)
    if p.returncode != 0:
        raise SystemExit("git %r failed: %s" % (args, p.stderr.decode("utf-8", "replace")[:800]))
    return p.stdout


def blob(data):
    return git(["hash-object", "-w", "--stdin"], data).decode().strip()


def ls_tree(tree):
    out = git(["ls-tree", tree]).decode()
    out_entries = []
    for line in out.splitlines():
        meta, name = line.split("\t", 1)
        mode, typ, sha = meta.split()
        out_entries.append([mode, typ, sha, name])
    return out_entries


def mktree(entries):
    data = "".join("%s %s %s\t%s\n" % (m, t, s, n) for m, t, s, n in entries).encode()
    return git(["mktree"], data).decode().strip()


def rebuild(tree, node):
    """tree: base tree sha or None; node: {name: (mode, blobsha) | None | {..}}"""
    entries = {e[3]: e for e in (ls_tree(tree) if tree else [])}
    for name, val in node.items():
        if isinstance(val, dict):
            base = entries.get(name)
            sub = rebuild(base[2] if base and base[1] == "tree" else None, val)
            entries[name] = ["040000", "tree", sub, name]
        elif val is None:
            entries.pop(name, None)
        else:
            entries[name] = [val[0], "blob", val[1], name]
    return mktree(sorted(entries.values(), key=lambda e: e[3]))


def nested(changes):
    root = {}
    for path, spec in changes.items():
        d = root
        parts = path.split("/")
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = spec
    return root


def commit(parent, message, changes):
    """new blob/tree objects for changes; no index, no working tree"""
    node = {}
    for path, spec in changes.items():
        if spec is None:
            node[path] = None
        else:
            mode, data = spec
            node[path] = (mode, blob(data))
    base_tree = git(["rev-parse", parent + "^{tree}"]).decode().strip()
    tree = rebuild(base_tree, nested(node))
    return git(["commit-tree", tree, "-p", parent, "-m", message]).decode().strip()


def score(rev, base=BASE):
    env = dict(os.environ)
    env["TMPDIR"] = S + "/replay"
    os.makedirs(env["TMPDIR"], exist_ok=True)
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", D, "--rev", rev, "--base", base],
                       capture_output=True, env=env)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def read(path):
    with open(path, "rb") as f:
        return f.read()


def rtext(path):
    return read(path).decode("utf-8")


def must(text, old, new, count=1):
    n = text.count(old)
    if n != count:
        raise SystemExit("anchor %r count=%d != %d" % (old[:70], n, count))
    return text.replace(old, new)


def row_map(sources):
    out = {}
    for line in sources.splitlines():
        m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
        if m:
            out[m.group(1)] = line
    return out


def row_cells(line):
    return [c.strip() for c in line.strip().split("|")[1:-1]]


def set_row(sources, rid, cells):
    assert len(cells) == 11, cells
    old = row_map(sources)[rid]
    return sources.replace(old, "| " + " | ".join(cells) + " |", 1)


def build():
    if os.path.exists(S + "/m"):
        shutil.rmtree(S + "/m")
    os.makedirs(S + "/m")
    subprocess.run(["git", "clone", "-q", "--bare", "--shared", L, D], check=True)
    gd = subprocess.run(["git", "-C", D, "rev-parse", "--absolute-git-dir"], capture_output=True, check=True)
    bare = subprocess.run(["git", "-C", D, "rev-parse", "--is-bare-repository"], capture_output=True, check=True)
    assert gd.stdout.decode().strip() == D, gd.stdout
    assert bare.stdout.decode().strip() == "true", bare.stdout
    git(["config", "user.name", "t"])
    git(["config", "user.email", "t@t"])
    entry = read(W + "/l1-draft/xkb-keymap-compile-r48.md")
    rows = rtext(W + "/l1-draft/rows-c2.md").rstrip("\n").split("\n")
    rr = rtext(W + "/l1-draft/readme-row.md").rstrip("\n")
    src = git(["show", BASE + ":" + SOURCES]).decode().split("\n")
    i = max(k for k, l in enumerate(src) if l.startswith("| S339 |"))
    src[i + 1:i + 1] = rows
    src = "\n".join(src)
    rd = git(["show", BASE + ":" + README]).decode().split("\n")
    i = max(k for k, l in enumerate(rd) if l.startswith("| `knowledge/xdg-terminal-selection-r47.md`"))
    rd[i + 1:i + 1] = [rr]
    rd = "\n".join(rd)
    pins = {}
    changes = {ENTRY: ("100644", entry), SOURCES: ("100644", src.encode()),
               README: ("100644", rd.encode())}
    for name in sorted(os.listdir(W + "/fetch")):
        pins[name] = read(W + "/fetch/" + name)
        changes[FETCH + name] = ("100644", pins[name])
    receipt = read(W + "/receipts/xkbcli-compile-keymap-r48.txt")
    changes[RECEIPTS + "xkbcli-compile-keymap-r48.txt"] = ("100644", receipt)
    changes[".ufo/waves/round-48/tools/make-xkb-receipt.sh"] = (
        "100644", read(W + "/tools/make-xkb-receipt.sh"))
    c = commit(BASE, "c2 candidate", changes)
    git(["update-ref", "refs/heads/cand", c])
    held = {}
    for name in sorted(os.listdir(L + "/.ufo/waves/round-46/fetch")):
        held[name] = read(L + "/.ufo/waves/round-46/fetch/" + name)
    return c, {"entry": entry.decode(), "sources": src, "readme": rd, "receipt": receipt.decode(),
               "pins": pins, "held": held}


def main():
    cand, K = build()
    print("candidate", cand)
    entry, src, rd = K["entry"], K["sources"], K["readme"]
    receipt = K["receipt"]
    pins = K["pins"]
    rows = row_map(src)
    byrow = {}
    for rid, line in rows.items():
        if rid >= "S340":
            for p in re.findall(re.escape(FETCH) + r"([A-Za-z0-9._/-]+)", line):
                byrow.setdefault(rid, []).append(p)
    print("row pins", json.dumps(byrow)[:900])

    variants = []

    def add(name, clause, changes, modes=None, note=""):
        variants.append((name, clause, changes, modes or {}, note))

    # ---- clause a (direct) and b
    for rid in sorted(byrow):
        bad = row_cells(rows[rid]); bad[9] = "later"
        add("b-recheck-%s" % rid, "b", {SOURCES: set_row(src, rid, bad).encode()})
    for rid, cell, val, tag in (("S340", 8, "2026-10-25", "opened"), ("S340", 3, "D", "tier"),
                                ("S340", 7, "draft", "status"),
                                ("S340", 10, "corpus/knowledge/other.md", "usedby")):
        bad = row_cells(rows[rid]); bad[cell] = val
        add("b-%s-%s" % (tag, rid), "b", {SOURCES: set_row(src, rid, bad).encode()})
    add("b-ghost-head", "b", {ENTRY: must(entry, "source: S340 -", "source: S351 -").encode()})
    add("b-rowid-missing", "b", {SOURCES: must(src, rows["S340"],
        rows["S340"].replace("| S340 |", "| S351 |", 1), 1).encode()})
    add("b-verified-at", "b", {ENTRY: must(entry, "verified-at: 2026-10-26", "verified-at: 2026-10-25").encode()})
    head_short = entry
    for rid in ("S342", "S343", "S344", "S345", "S346", "S347", "S348", "S349", "S350"):
        head_short = must(head_short, "source: %s -" % rid, "note: %s -" % rid, 1)
    add("b-head-short", "b", {ENTRY: head_short.encode()})

    # ---- clause c: pin bytes / recorded digest per row, URLs, anchors, modes
    for rid in sorted(byrow):
        add("c-pinbytes-%s" % rid, "c", {FETCH + p: pins[p] + b"# tampered\n" for p in byrow[rid]})
    for rid in sorted(byrow):
        bad = row_cells(rows[rid])
        bad[5] = re.sub(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", "0" * 64, bad[5], count=1)
        add("c-digest-%s" % rid, "c", {SOURCES: set_row(src, rid, bad).encode()})
    bad = row_cells(rows["S340"]); bad[1] = bad[1].replace("xkbcommon-1.13.2", "main")
    add("c-url-branch-S340", "c", {SOURCES: set_row(src, "S340", bad).encode()})
    bad = row_cells(rows["S340"]); bad[1] = bad[1].replace("xkbcommon-1.13.2", "d" * 40)
    add("x-url-commit-admitted-S340", "none", {SOURCES: set_row(src, "S340", bad).encode()})
    bad = row_cells(rows["S340"]); bad[1] = bad[1].replace("/xkbcommon-1.13.2/src/", "/src/")
    add("c-url-noref-S340", "c", {SOURCES: set_row(src, "S340", bad).encode()})
    bad = row_cells(rows["S347"]); bad[1] = bad[1].replace("symbols/br", "symbols/de")
    add("c-url-unrelated-S347", "c", {SOURCES: set_row(src, "S347", bad).encode()})
    add("c-pin-missing-S340", "c", {FETCH + "xkbcommon-rules.c": None})
    bad = row_cells(rows["S340"]); bad[5] = bad[5].replace("xkbcommon-rules.c:1259", "xkbcommon-rules.c:1259-9999", 1)
    add("c-anchor-range-S340", "c", {SOURCES: set_row(src, "S340", bad).encode()})
    bad = row_cells(rows["S340"]); bad[5] = bad[5].replace("xkbcommon-rules.c:1259", "xkbcommon-context.c:243", 1)
    add("c-anchor-otherpin-S340", "c", {SOURCES: set_row(src, "S340", bad).encode()})
    bad = row_cells(rows["S350"]); bad[2] = "code"
    add("c-ownwork-kind-S350", "c", {SOURCES: set_row(src, "S350", bad).encode()})
    bad = row_cells(rows["S340"]); bad[5] = bad[5].replace("sha256:", "digest ", 1)
    add("x-digest-label-admitted-S340", "none", {SOURCES: set_row(src, "S340", bad).encode()})
    add("c-pin-mode-S340", "c", {}, modes={FETCH + "xkbcommon-rules.c": "100755"})

    # ---- clause d
    add("d-quote-word", "d", {ENTRY: must(entry, "Options can be empty, so respect that if passed in",
                                          "Options can be empty, so respect this if passed in").encode()})
    add("d-quote-range-out", "d", {ENTRY: must(entry, "xkbcommon-context-priv.c:218",
                                               "xkbcommon-context-priv.c:9999").encode()})
    add("d-quote-range-shift", "d", {ENTRY: must(entry, "xkbcommon-context-priv.c:218",
                                                 "xkbcommon-context-priv.c:5-10").encode()})
    add("d-quote-lane-locator", "d", {ENTRY: must(
        entry, "## What the evidence licenses",
        "`The XKB compile itself is not reproduced` at corpus/knowledge/hyprland-input-devices-r46.md:69\n\n"
        "## What the evidence licenses").encode()})
    add("d-quote-long", "d", {ENTRY: must(
        entry, "`expanded_value->matched = true;`",
        "`" + " ".join(["matched"] * 30) + "`").encode()})
    add("x-quote-600-invisible", "none", {ENTRY: must(
        entry, "`expanded_value->matched = true;`",
        "`" + " ".join(["expanded_value->matched"] * 26) + ";`").encode()})
    add("d-uncited-pin", "d", {ENTRY: must(entry, "2. **Comma lists.**",
                                           "2. **Comma lists.** See xkbcommon-meson.build:32.").encode()})

    # ---- clause e
    add("e-step-unloc", "e", {ENTRY: must(must(
        entry, "(xkbcommon-rules.c:520-527)", "(see the split code)"),
        "(xkbcommon-rules.c:528-535)", "(see the truncation code)").encode()})
    step9 = [l for l in entry.splitlines() if l.startswith("9. **Which diagnostics")][0]
    add("e-step-outofrange", "e", {ENTRY: entry.replace(
        step9, step9.replace("(xkbcommon-context.c:503)", "(xkbcommon-context.c:9999)"), 1).encode()})
    add("e-steps5", "e", {ENTRY: must(must(must(must(
        entry, "6. **File and map lookup.**", "**File and map lookup.**"),
        "7. **What each name class does when it is wrong.**", "**What each name class does when it is wrong.**"),
        "8. **What the compositor does with a failed compile.**", "**What the compositor does with a failed compile.**"),
        "9. **Which diagnostics are visible.**", "**Which diagnostics are visible.**").encode()})
    step3 = [l for l in entry.splitlines() if l.startswith("3. **The rules file.**")][0]
    step3b = re.sub(r"xkbcommon-rules\.c:\d+(?:-\d+)?", "xkbcommon-meson.build:32", step3)
    add("e-step-uncited", "e", {ENTRY: entry.replace(step3, step3b, 1).encode()})
    add("x-e-boundary-admitted", "none", {ENTRY: must(entry, "xkeyboard-config-rules-evdev:55-59",
                                                      "xkeyboard-config-rules-evdev:747").encode()})

    # ---- clause f / r
    dig = "efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81"
    add("f-digest-receipt-only", "f", {RECEIPTS + "xkbcli-compile-keymap-r48.txt":
                                       must(receipt, dig + "  host.keymap", "1" * 64 + "  host.keymap").encode()})
    add("f-negrc-layout-receipt", "f", {RECEIPTS + "xkbcli-compile-keymap-r48.txt": must(
        receipt, "ERROR: Couldn't create xkb keymap\nrc=1\n\n--- unknown variant on a known layout",
        "ERROR: Couldn't create xkb keymap\nrc=0\n\n--- unknown variant on a known layout").encode()})
    add("f-negrc-variant-receipt", "f", {RECEIPTS + "xkbcli-compile-keymap-r48.txt": must(
        receipt, "ERROR: Couldn't create xkb keymap\nrc=1\n\n--- variant the br map does not define",
        "ERROR: Couldn't create xkb keymap\nrc=0\n\n--- variant the br map does not define").encode()})
    add("f-negrc-option-receipt", "f", {RECEIPTS + "xkbcli-compile-keymap-r48.txt": must(
        receipt, "Unrecognized RMLVO option \"nope:nope\" was ignored\nrc=0",
        "Unrecognized RMLVO option \"nope:nope\" was ignored\nrc=1", 2).encode()})
    add("f-receipt-absent", "f", {RECEIPTS + "xkbcli-compile-keymap-r48.txt": None})
    add("f-receipt-mode", "f", {}, modes={RECEIPTS + "xkbcli-compile-keymap-r48.txt": "100755"})
    add("f-receipt-short", "f", {RECEIPTS + "xkbcli-compile-keymap-r48.txt": b"xkbcli 1.13.2\n"})
    add("f-entry-version", "f", {ENTRY: entry.replace("1.13.2", "1.13.3").encode()})
    relab = receipt
    relab = must(relab, "# taken: 2026-10-27T00:08:08Z (UTC)", "# taken: 2026-10-26T09:00:00Z (UTC)")
    relab = must(relab, 'Couldn\'t find file "symbols/zz" in include paths',
                 'Couldn\'t find file "symbols/qq" in include paths')
    relab = must(relab, "3 include paths could not be added:", "1 include path could not be added:", 3)
    add("r-untrusted-receipt-body", "f/r", {RECEIPTS + "xkbcli-compile-keymap-r48.txt": relab.encode()})
    add("r-relabel-digest-both", "r", {
        RECEIPTS + "xkbcli-compile-keymap-r48.txt": must(receipt, dig + "  host.keymap",
                                                         "ab" * 32 + "  host.keymap").encode(),
        ENTRY: must(entry, "sha256 `" + dig + "`", "sha256 `" + "ab" * 32 + "`").encode()})
    # a receipt relabelled from a different capture: the round-46 held receipt shape under the r48 name
    alt = receipt
    alt = must(alt, "$ /usr/bin/xkbcli compile-keymap --layout br --options compose:caps > host.keymap",
               "$ /usr/bin/xkbcli compile-keymap --layout us --options grp:alt_shift_toggle > host.keymap")
    alt = must(alt, "xkb_symbols { include \"pc+br+inet(evdev)+compose(caps)\" };",
               "xkb_symbols { include \"pc+us+inet(evdev)\" };")
    add("r-alt-run-receipt", "f/r", {RECEIPTS + "xkbcli-compile-keymap-r48.txt": alt.encode()})

    # ---- clause g
    add("g-row-absent", "g", {README: rd.replace("\n| `knowledge/xkb-keymap-compile-r48.md`",
                                                    "\n| `knowledge/zz-absent.md`", 1).encode()})
    add("g-row-duplicate", "g", {README: must(rd, "| rows S340-S350 |",
        "| rows S340-S350 |\n| `knowledge/xkb-keymap-compile-r48.md` (dup) | x | rows S340-S350 |").encode()})
    add("g-redirect", "g", {README: must(rd, "| rows S340-S350 |", "| rows S340-S350; supersedes the r46 entry |").encode()})
    add("g-other-knowledge", "g", {README: must(rd, "rows S340-S350 |",
        "rows S340-S350, see knowledge/hyprland-input-devices-r46.md |").encode()})
    add("g-missing-id", "g", {README: must(rd, "rows S340-S350", "rows S340-S349").encode()})
    add("g-cells", "g", {README: must(rd, "| rows S340-S350 |", "| rows S340-S350").encode()})
    add("g-fenced", "g", {README: must(must(rd, "| `knowledge/xkb-keymap-compile-r48.md` (MADO-R48-1",
        "```\n| `knowledge/xkb-keymap-compile-r48.md` (MADO-R48-1"), "| rows S340-S350 |",
        "| rows S340-S350 |\n```").encode()})

    # ---- clause h
    s318 = rows["S318"]
    add("h-held-row", "h", {SOURCES: must(src, s318, s318.replace("| mined |", "|  mined |", 1)).encode()})
    add("h-held-row-delete", "h", {SOURCES: must(src, s318 + "\n", "", 1).encode()})
    add("h-held-pin-ik", "h", {HELD_FETCH + "Hyprland-IKeyboard.cpp":
                              K["held"]["Hyprland-IKeyboard.cpp"] + b"# tampered\n"})
    add("h-held-pin-cv", "h", {HELD_FETCH + "Hyprland-ConfigValues.cpp":
                              K["held"]["Hyprland-ConfigValues.cpp"] + b"# tampered\n"})
    add("h-held-entry", "h", {"corpus/knowledge/hyprland-input-devices-r46.md":
                              read(L + "/corpus/knowledge/hyprland-input-devices-r46.md") + b"\n"})

    # ---- clause i
    rid346 = row_cells(rows["S346"]); rid346[1] = rid346[1].replace("xkeyboard-config-2.48",
                                                                   "cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0")
    rid347 = row_cells(rows["S347"]); rid347[1] = rid347[1].replace("xkeyboard-config-2.48",
                                                                   "cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0")
    rid340 = row_cells(rows["S340"]); rid340[6] = rid340[6].replace("XKB-595", "XKB-596")
    rid349 = row_cells(rows["S349"]); rid349[6] = rid349[6].replace("XKB-595", "XKB-596")
    rid350 = row_cells(rows["S350"]); rid350[6] = rid350[6].replace("XKB-595", "XKB-596")
    i_src = src
    for rid, cells in (("S346", rid346), ("S347", rid347), ("S340", rid340),
                       ("S349", rid349), ("S350", rid350)):
        i_src = set_row(i_src, rid, cells)
    add("i-ground-two-terms", "i", {ENTRY: entry.replace("xkeyboard-config-2.48", "xkeyboard-config-2.47")
                                    .replace("XKB-595", "XKB-596").encode()})
    add("i-ground-rev-census", "i", {
        ENTRY: entry.replace("xkeyboard-config-2.48", "xkeyboard-config-2.47")
        .replace("XKB-595", "XKB-596").encode(),
        SOURCES: i_src.encode(),
        README: rd.replace("XKB-595", "XKB-596").encode()})
    add("i-ground-all-terms", "i", {ENTRY: entry.replace("xkeyboard-config-2.48", "xkeyboard-config-2.47")
                                    .replace("XKB-595", "XKB-596")
                                    .replace("compile-keymap", "compilekeymap").encode()})

    # ---- alternate pin with the same filename
    add("p-alt-same-basename", "c", {FETCH + "alt/xkbcommon-rules.c": read(W + "/fetch/xkbcommon-context.c")})

    def rows_with_digest(rid, pinb):
        cells = row_cells(rows[rid])
        cells[5] = re.sub(r"sha256:[0-9a-f]{64}", "sha256:" + hashlib.sha256(pinb).hexdigest(), cells[5], count=1)
        return cells

    tampered = pins["xkbcommon-rules.c"] + b"/* round-48 local note */\n"
    add("p-tamper-selfconsistent", "c/d", {FETCH + "xkbcommon-rules.c": tampered,
                                           SOURCES: set_row(src, "S340", rows_with_digest("S340", tampered)).encode()})
    # alternate pin under a stem that makes every basename token ambiguous
    add("p-alt-ambiguous-stem", "c/d", {
        FETCH + "libxkbcommon/rules.c": pins["xkbcommon-rules.c"],
        FETCH + "xkbcommon-rules.c": None,
        FETCH + "alt/rules.c": read(W + "/fetch/xkbcommon-context.c"),
        SOURCES: must(src, FETCH + "xkbcommon-rules.c", FETCH + "libxkbcommon/rules.c").encode()})
    # a self-authored "pin" quoted as upstream ground (own-work row)
    selfnote = b"# local note\nmado round 48 note\n" + entry.encode()[:2000]
    cells = row_cells(rows["S350"])
    cells[5] += (" self-note sha256:" + hashlib.sha256(selfnote).hexdigest()
                 + " receipt .ufo/waves/round-48/fetch/self-note.md")
    add("p-selfpin-ownwork", "c/d", {
        FETCH + "self-note.md": selfnote,
        SOURCES: set_row(src, "S350", cells).encode(),
        ENTRY: must(entry, "**OBS** S349:",
                    "**OBS** S350: `mado round 48 note` at self-note.md:2\n\n**OBS** S349:").encode()})

    # ---- admitted perturbations (expected to pass; recorded as accepted, not misses)
    bad = row_cells(rows["S340"]); bad[5] += " extra sha256:" + "cd" * 32
    add("x-digest-extra-admitted", "none", {SOURCES: set_row(src, "S340", bad).encode()})
    bad = row_cells(rows["S340"]); bad[9] = "2999-12-31"
    add("x-recheck-future-admitted", "none", {SOURCES: set_row(src, "S340", bad).encode()})

    os.makedirs(S + "/logs", exist_ok=True)
    results = []

    def record(name, clause, note, rev, rc, out):
        fails = [l for l in out.splitlines() if re.search(
            r"clause=[a-z] .*(mismatch|missing|absent|moved|bad|short|ghost|range|unresolved|"
            r"not_in_pin|disagree|without|uncited|readme_|no_|too_long|other_pin|ghosts|detached)", l)]
        last = [l for l in out.splitlines() if l.startswith("PRED-C2-r48")][-1]
        cl = [l for l in out.splitlines() if "clauses=" in l]
        results.append({"name": name, "declared": clause, "note": note, "rev": rev, "rc": rc,
                        "last": last, "clauses": cl[-1] if cl else "", "fails": fails[:10]})
        with open(S + "/logs/%s.log" % name, "w") as f:
            f.write("rev=%s\nrc=%d\n%s" % (rev, rc, out))

    rc0, out0 = score(cand)
    record("pos", "all", "intended data candidate", cand, rc0, out0)
    print("pos rc", rc0, [l for l in out0.splitlines() if "clauses=" in l][-1])

    rb, ob = score(BASE)
    record("a-rev-base-direct", "a", "score BASE itself", BASE, rb, ob)
    rs, os_ = score(cand, base=cand)
    record("a-entry-at-base", "a/setup", "--base cand", cand, rs, os_)

    for name, clause, changes, modes, note in variants:
        spec = {}
        for path, data in changes.items():
            spec[path] = None if data is None else (modes.get(path, "100644"), data)
        for path, mode in modes.items():
            if path not in changes:
                spec[path] = (mode, git(["cat-file", "blob", "%s:%s" % (cand, path)]))
        rev = commit(cand, name, spec)
        rc, out = score(rev)
        record(name, clause, note, rev, rc, out)
        print("%-28s %s rc=%d %s" % (name, clause, rc, results[-1]["last"][:96]))

    with open(S + "/summary.json", "w") as f:
        json.dump(results, f, indent=1)
    print("variants", len(results))


main()
