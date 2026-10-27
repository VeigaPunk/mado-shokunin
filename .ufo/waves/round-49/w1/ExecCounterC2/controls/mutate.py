#!/usr/bin/env python3
"""Apply one named mutation to a checked-out C2-r49 POS tree.

Usage: mutate.py <repo> <name>
Every mutation edits only files under <repo>; the driver commits the result as its own
revision, so each control is scored by `git show REV:path`, never by the working tree.
"""
import hashlib
import os
import re
import sys

ENTRY = "corpus/knowledge/hyprland-bind-key-match-r49.md"
RECEIPT = ".ufo/waves/round-49/receipts/hyprctl-binds-r49.txt"
PIN = ".ufo/waves/round-49/fetch/hyprctl-binds-r49.txt"
REG = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-49.md"
FB = ".ufo/waves/round-49/fetch/"


def rd(repo, p):
    return open(os.path.join(repo, p), encoding="utf-8").read()


def wr(repo, p, s):
    open(os.path.join(repo, p), "w", encoding="utf-8").write(s)


def row(repo, sid):
    for line in rd(repo, REG).split("\n"):
        if line.startswith("| %s |" % sid):
            return line
    raise SystemExit("row not found: %s" % sid)


def set_row(repo, sid, new):
    src = rd(repo, REG)
    old = row(repo, sid)
    wr(repo, REG, src.replace(old, new, 1))


def main():
    repo, name = sys.argv[1], sys.argv[2]
    ent = rd(repo, ENTRY)
    if name == "quote-word":
        wr(repo, ENTRY, ent.replace("Catchall not allowed outside of submap!",
                                    "Catchall forbidden outside of submap!", 1))
    elif name == "range-9999":
        lines = ent.split("\n")
        k = next(i for i, l in enumerate(lines) if l.startswith("1. "))
        lines[k] = re.sub(r":(\d+)\)", ":9999)", lines[k], count=1)
        wr(repo, ENTRY, "\n".join(lines))
    elif name == "quote-long":
        lines = ent.split("\n")
        k = next(i for i, l in enumerate(lines) if l.startswith("9. "))
        lines[k] = lines[k].replace(
            "The \"best\" case-insensitive match is the lower-case keysym name.",
            "The \"best\" case-insensitive match is the lower-case keysym name and it also "
            "wins over every other candidate which differs only by letter case in any "
            "bicameral or non bicameral script", 1)
        wr(repo, ENTRY, "\n".join(lines))
    elif name == "branch-url":
        r = row(repo, "S353")
        set_row(repo, "S353", r.replace("/efb50993780079460b0cbed1363e2166a2de1d9f/",
                                        "/main/", 1))
    elif name == "pin-digest":
        r = row(repo, "S352")
        m = re.search(r"sha256:([0-9a-f]{64})", r)
        set_row(repo, "S352", r.replace(m.group(1), "0" * 64, 1))
    elif name == "pin-and-file":
        p = os.path.join(repo, FB + "Hyprland-legacy-ConfigManager.cpp")
        data = open(p, "rb").read() + b"\n// control: appended line\n"
        open(p, "wb").write(data)
        r = row(repo, "S352")
        m = re.search(r"sha256:([0-9a-f]{64})", r)
        set_row(repo, "S352", r.replace(m.group(1), hashlib.sha256(data).hexdigest(), 1))
    elif name == "held-row-moved":
        r = row(repo, "S319")
        set_row(repo, "S319", r.replace("What a keyboard stores", "What a keyboard keeps", 1))
    elif name == "held-not-cited":
        wr(repo, ENTRY, ent.replace("the held row S319 is cited here",
                                    "the held keyboard row is cited here", 1))
    elif name == "held-rereg":
        src = os.path.join(repo, ".ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp")
        data = open(src, "rb").read()
        open(os.path.join(repo, FB + "Hyprland-IKeyboard.cpp"), "wb").write(data)
        h = hashlib.sha256(data).hexdigest()
        r = row(repo, "S319")
        url = re.search(r"https?://[^\s|]+", r).group(0)
        new = ("| S356 | Hyprland v0.56.2 keyboard base, reopened - %s | code | A | the keyboard "
               "base, reopened with a bind-time scope | Hyprland-IKeyboard.cpp:60-145 @ commit "
               "efb50993780079460b0cbed1363e2166a2de1d9f; Hyprland-IKeyboard.cpp %d B sha256:%s; "
               "receipt .ufo/waves/round-49/fetch/Hyprland-IKeyboard.cpp | a new scope for a held "
               "source | mined | 2026-10-27 | on-release | %s |") % (
                   url, len(data), h, ENTRY)
        lines = rd(repo, REG).split("\n")
        k = next(i for i, l in enumerate(lines) if l.startswith("| S355 |"))
        lines[k + 1:k + 1] = [new]
        wr(repo, REG, "\n".join(lines))
        les = rd(repo, LESSON)
        wr(repo, LESSON, les.replace("## Gate\n", "## Gate\n\n- **S356 admit**, tier A.\n", 1))
    elif name == "paraphrase":
        src = (rd(repo, "corpus/knowledge/hyprland-input-devices-r46.md")
               + "\n" + rd(repo, "corpus/knowledge/keybind-rule-semantics.md"))
        src = re.sub(r"`[^`]*`", " ", src)
        src = re.sub(r'"[^"\n]*"', " ", src)
        src = re.sub(r"https?://\S+|S\d{3}|\||\S+:\d+", " ", src)
        keep = [l.strip() for l in src.split("\n") if len(l.strip().split()) >= 12]
        words = " ".join(keep[:70]).split()
        para = " ".join("changed" if k % 9 == 4 and w.isalpha() else w
                        for k, w in enumerate(words))
        wr(repo, ENTRY, ent + "\n" + para + "\n")
        print("paraphrase words:", len(words))
    elif name == "step-quote":
        lines = ent.split("\n")
        k = next(i for i, l in enumerate(lines) if l.startswith("3. "))
        lines[k] = re.sub(r":(\d+)\)", lambda m: ":%d)" % (int(m.group(1)) - 1), lines[k], count=1)
        wr(repo, ENTRY, "\n".join(lines))
    elif name == "row-unused":
        lines = rd(repo, REG).split("\n")
        k = next(i for i, l in enumerate(lines) if l.startswith("| S355 |"))
        r355 = lines[k]
        m = re.search(r"sha256:([0-9a-f]{64})", r355)
        new = ("| S356 | mado host, an uncited extra capture (own-work) - .ufo/waves/round-49/receipts/"
               "hyprctl-binds-r49.txt | own-work | A | a second own-work capture with no consumer | "
               "hyprctl-binds-r49.txt whole file, 512 B sha256:%s; receipt .ufo/waves/round-49/fetch/"
               "hyprctl-binds-r49.txt | a row nobody cites | mined | 2026-10-27 | on-change | - |") % (
                   m.group(1))
        lines[k + 1:k + 1] = [new]
        wr(repo, REG, "\n".join(lines))
        les = rd(repo, LESSON)
        wr(repo, LESSON, les.replace("## Gate\n", "## Gate\n\n- **S356 admit**, tier A.\n", 1))
    elif name == "row-used-by-held":
        lines = rd(repo, REG).split("\n")
        k = next(i for i, l in enumerate(lines) if l.startswith("| S355 |"))
        m = re.search(r"sha256:([0-9a-f]{64})", lines[k])
        new = ("| S356 | mado host, an extra capture consumed only by a held doc (own-work) - "
               ".ufo/waves/round-49/receipts/hyprctl-binds-r49.txt | own-work | A | a second own-work "
               "capture with a held consumer | hyprctl-binds-r49.txt whole file, 512 B sha256:%s; "
               "receipt .ufo/waves/round-49/fetch/hyprctl-binds-r49.txt | a row used only by held text | "
               "mined | 2026-10-27 | on-change | corpus/knowledge/keybind-rule-semantics.md |") % m.group(1)
        lines[k + 1:k + 1] = [new]
        wr(repo, REG, "\n".join(lines))
        les = rd(repo, LESSON)
        wr(repo, LESSON, les.replace("## Gate\n", "## Gate\n\n- **S356 admit**, tier A.\n", 1))
    elif name == "receipt-renamed":
        old = os.path.join(repo, RECEIPT)
        new = os.path.join(repo, ".ufo/waves/round-49/receipts/binds-shape.txt")
        os.rename(old, new)
        wr(repo, ENTRY, ent.replace("receipts/hyprctl-binds-r49.txt",
                                    "receipts/binds-shape.txt", 1))
    elif name == "receipt-absent":
        os.remove(os.path.join(repo, RECEIPT))
    elif name in ("receipt-typed", "receipt-resolve", "receipt-json"):
        txt = rd(repo, RECEIPT)
        if name == "receipt-typed":
            txt = txt.replace("mouse=6", "mouse=7", 1)
        elif name == "receipt-resolve":
            txt = txt.replace("int=0", "int=1", 1)
        else:
            txt = txt.replace("key_form_rule:", '"modmask": 0, key_form_rule:', 1)
        wr(repo, RECEIPT, txt)
        wr(repo, PIN, txt)
        r = row(repo, "S355")
        m = re.search(r"sha256:([0-9a-f]{64})", r)
        set_row(repo, "S355", r.replace(m.group(1),
                                        hashlib.sha256(txt.encode()).hexdigest(), 1))
    elif name == "entry-digest":
        d = re.search(r"sha256 ([0-9a-f]{64})", ent)
        wr(repo, ENTRY, ent.replace(d.group(1), "d" * 64, 1))
    elif name == "entry-total":
        wr(repo, ENTRY, re.sub(r"\b192 binds\b", "191 binds", ent, count=1))
    elif name == "nosteps":
        lines = ent.split("\n")
        for k, l in enumerate(lines):
            m = re.match(r"^([5-9]|10)\. \*\*", l)
            if m:
                lines[k] = "step " + l
        wr(repo, ENTRY, "\n".join(lines))
    elif name == "limits-gone":
        lines = ent.split("\n")
        k = next(i for i, l in enumerate(lines) if l.strip() == "## Limits")
        wr(repo, ENTRY, "\n".join(lines[:k]))
    elif name == "gate-missing":
        les = rd(repo, LESSON)
        les = re.sub(r"- \*\*S354 admit\*\*[^\n]*\n", "", les, count=1)
        wr(repo, LESSON, les)
    elif name == "paste-body":
        src = rd(repo, "corpus/knowledge/keybind-rule-semantics.md")
        picked = [l for l in src.split("\n")
                  if len(l) >= 60 and not re.search(r"[`\"|]|S\d{3}|https?:|:\d", l)][:10]
        if len(picked) < 6:
            raise SystemExit("paste-body: not enough clean lines")
        wr(repo, ENTRY, ent + "\n" + "\n".join(picked) + "\n")
    elif name == "registry-unused":
        r = row(repo, "S355")
        set_row(repo, "S355", r.replace(ENTRY, "corpus/knowledge/xkb-keymap-compile-r48.md", 1))
    elif name == "opened-old":
        r = row(repo, "S352")
        set_row(repo, "S352", r.replace("| mined | 2026-10-27 |", "| mined | 2026-10-26 |", 1))
    else:
        raise SystemExit("unknown mutation: %s" % name)
    print("mutated", name)


if __name__ == "__main__":
    main()
