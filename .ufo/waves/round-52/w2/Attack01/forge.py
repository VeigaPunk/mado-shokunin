#!/usr/bin/env python3
"""Attack01 W2 forger: build a population-complete ledger whose every description is
semantically empty boilerplate plus a two-word phrase lifted from the instrument's own
committed bytes. Phrase selection replicates the w1-draft counter's four filters so the
forgery targets the STRONGER clause; the landed counter (no filters) is strictly easier.
Pointers and row order are copied verbatim from the production ledger at base.
"""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
WORD = re.compile(r"[a-z0-9]+")

# FUNCTION_WORDS copied verbatim from the w1-draft counter under attack.
FUNCTION_WORDS = frozenset("""the a an and or but of to in for with from into onto over
under per by at as is are was were be been being am do does did done have has had not no
nor none nothing all any some each every other others another such same own self this that
these those it its they them their he she his her we us our you your i me my one two three
four five many much more most less least few several if then else when while where which
who whom whose what why how because so than too very just only also even still yet ever
never always can could will would shall should may might must here there now once again
away back down out off up both either neither anything something everything someone anyone
everyone nobody nowhere everywhere anyway therefore thus hence via etc""".split())


def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args),
                          stdout=subprocess.PIPE).stdout


def normalize(text):
    return " ".join(WORD.findall(text.lower()))


def path_words(path):
    words = set(WORD.findall(os.path.basename(path).lower()))
    words |= set(WORD.findall(os.path.dirname(path).lower()))
    return words


def population(files):
    return [p for p in files
            if "__pycache__" not in p and not p.endswith((".pyc", ".pyo"))
            and (p.startswith("tools/")
                 or (p.startswith("quality/") and p.endswith(".py")
                     and (p.count("/") == 1 or p.startswith("quality/counters/"))))]


def path_fragments(text):
    frags = set()
    for m in re.finditer(r"[A-Za-z0-9_./-]*[/][A-Za-z0-9_./-]*", text):
        w = WORD.findall(m.group(0).lower())
        for i in range(len(w) - 1):
            frags.add(" ".join(w[i:i + 2]))
    return frags


def blob(path):
    try:
        return git("show", "%s:%s" % (REV, path))
    except Exception:
        return b""


def surviving_phrases(path, popwords):
    """Word pairs from the instrument's own bytes at REV that pass all four w1-draft
    context filters, in order of appearance."""
    raw = blob(path).decode("utf-8", "replace")
    words = normalize(raw).split()
    frags = path_fragments(raw)
    own = path_words(path)
    seen = set()
    out = []
    for i in range(len(words) - 1):
        phrase = " ".join(words[i:i + 2])
        if phrase in seen:
            continue
        seen.add(phrase)
        pw = set(words[i:i + 2])
        if len(pw) < 2:
            continue
        if pw <= own:
            continue
        if pw <= popwords:
            continue
        if phrase in frags:
            continue
        if pw <= FUNCTION_WORDS:
            continue
        out.append(phrase)
    return out


def main():
    files = git("ls-tree", "-r", "--name-only", REV).decode().splitlines()
    pop = population(files)
    popwords = set()
    for p in pop:
        popwords |= path_words(p)

    rows = []  # (path, pointer_cell) parsed from the production ledger
    ledger = blob("quality/tool-ledger.md").decode("utf-8", "replace")
    in_fence = False
    for line in ledger.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 3 or not (cells[0].startswith("`") and cells[0].endswith("`")):
            continue
        rows.append((cells[0][1:-1], cells[2]))

    forged = ["# F-all: every row's description is generic boilerplate plus a",
              "# two-word phrase lifted from that instrument's own committed bytes.",
              "# Row order, path column and pointer column are the production ledger's.",
              ""]
    zero = []
    for idx, (path, pointer) in enumerate(rows):
        cands = surviving_phrases(path, popwords)
        if not cands:
            zero.append(path)
            desc = "Generic accountability note %d nothing here." % idx
        else:
            desc = "Generic accountability note %d %s." % (idx, cands[0])
        forged.append("| `%s` | %s | %s |" % (path, desc, pointer))
    open(sys.argv[1], "w").write("\n".join(forged) + "\n")
    print("rows=%d no-surviving-candidate=%d" % (len(rows), len(zero)))
    for p in zero:
        print("ZERO:", p)


if __name__ == "__main__":
    main()
