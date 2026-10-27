#!/usr/bin/env python3
"""Attack17 forge: build a forged tool ledger that passes all three C1 counters.

Each row keeps the production pointer cell verbatim (valid non-self pointer) but
replaces the description with generic boilerplate plus ONE adjacent word pair
copied from the instrument's own committed bytes, chosen to survive the
C1CounterDesign draft's four extra filters (not own-name, not population
vocabulary, not a path fragment, not all-function-words).

Reads: git show <rev>:<path> only. Writes: one markdown file under this scratch.
"""
import importlib.util
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
DRAFT = os.path.join(
    LANE, ".ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "forged.md")

spec = importlib.util.spec_from_file_location("draft", DRAFT)
draft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(draft)


def git(*args):
    p = subprocess.run(("git", "-C", LANE) + args, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode())
    return p.stdout


files = {p for p in git("ls-tree", "-r", "--name-only", REV).decode().splitlines() if p}
pop = draft.population(files)
population_words = draft.population_path_words(pop)
assert len(pop) == 82, len(pop)

ledger_text = git("show", "%s:quality/tool-ledger.md" % REV).decode("utf-8")
prod_rows = draft.rows_of(ledger_text)
prod_ptr = {r["path"]: r["region"][0].strip() for r in prod_rows if r["path"] in pop}
assert len(prod_ptr) == 82, len(prod_ptr)

chosen = {}
no_candidate = []
for path in pop:
    raw = git("show", "%s:%s" % (REV, path)).decode("utf-8", "replace")
    body = " " + draft.normalize(raw) + " "
    words = draft.normalize(raw).split()
    frags = draft.path_fragments(raw)
    own = draft.path_words(path)
    # every adjacent pair that occurs in this instrument's bytes, in source order
    bigs = draft.bigrams(words)
    surviving = []
    for phrase in bigs:
        pw = set(phrase.split())
        if pw <= own or pw <= population_words or phrase in frags \
                or pw <= draft.FUNCTION_WORDS:
            continue
        surviving.append(phrase)
    if not surviving:
        no_candidate.append(path)
        continue
    # deterministic: LAST surviving bigram in byte order (deepest in the file,
    # typically argparse/code boilerplate, not the docstring's functional claim)
    chosen[path] = surviving[-1]

print("instruments lacking a surviving bigram:", no_candidate)
rows = []
for i, path in enumerate(sorted(chosen)):
    w1, w2 = chosen[path].split()
    desc = ("Generic accountability boilerplate line %03d cites %s %s verbatim."
            % (i, w1, w2))
    rows.append("| `%s` | %s | %s |" % (path, desc, prod_ptr[path]))

with open(OUT, "w") as fh:
    fh.write("# F3x: forged ledger, one copied word pair per instrument, draft-filter aware\n\n")
    fh.write("\n".join(rows) + "\n")
print("wrote", OUT, "rows:", len(rows))
for path in sorted(chosen)[:10]:
    print("  planted: %-52s %r" % (path, chosen[path]))
