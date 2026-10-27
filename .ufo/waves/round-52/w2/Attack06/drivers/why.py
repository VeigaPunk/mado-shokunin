#!/usr/bin/env python3
"""Reproduce the generic_desc clause for one description, with its own functions."""
import importlib.util, subprocess, sys
COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py"
spec = importlib.util.spec_from_file_location("c1r52", COUNTER)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
raw = subprocess.run(["git","-C",LANE,"show",REV+":quality/check-tool-ledger.py"],
                     capture_output=True, check=True).stdout.decode()
ledger = subprocess.run(["git","-C",LANE,"show",REV+":quality/tool-ledger.md"],
                        capture_output=True, check=True).stdout.decode()
files = m.listing(LANE, REV)
pop = m.population(files)
popw = m.population_path_words(pop)

CASES = {
 "04-honest-paraphrase-A": "Checks that every tracked instrument in the tool ledger has an accountable evidence pointer.",
 "05-honest-paraphrase-B": "Derives the tracked-instrument population at a revision and checks every ledger row's accountability pointer.",
 "09-terse-4-words": "Checks the tool ledger.",
}
path = "quality/check-tool-ledger.py"
body = " " + m.normalize(raw) + " "
frags = m.path_fragments(raw)
own = m.path_words(path)
for name, desc in CASES.items():
    words = m.normalize(desc).split()
    bound = [p for p in m.bigrams(words) if " %s " % p in body]
    print("==", name)
    print("  words=%r" % (words,))
    print("  bound=%r" % (bound,))
    for phrase in bound:
        pw = set(phrase.split())
        why = []
        if pw <= own: why.append("own-path-words")
        if pw <= popw: why.append("population-path-words")
        if phrase in frags: why.append("path-fragment")
        if pw <= m.FUNCTION_WORDS: why.append("function-words")
        print("    %-24r dropped: %s" % (phrase, ",".join(why) or "SURVIVES"))
    # which phrases of the description would survive if bound?
    print("  own_path_words=%r" % (sorted(own),))
