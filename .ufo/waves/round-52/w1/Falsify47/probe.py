#!/usr/bin/env python3
"""Falsify47 probe v2: C2 held-ground novelty (r51 clause-c shingle containment).

Imports the committed r51 counter's own body_text()/shingles() and reproduces its
clause_c scoring loop at the round-52 base revision, then scores fixtures.

Run:
  TMPDIR=/fast/scratch/hyaku/mado-r52/Falsify47 \
    python3 /fast/scratch/hyaku/mado-r52/Falsify47/probe.py
"""
import importlib.util
import os
import re
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(REPO, "quality/counters/c2-r51-dispatch-entry.py")
BASE = "85d57a818c3707397e21c840b6498b105ba798aa"
ENTRY = "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"
HERE = os.path.dirname(os.path.abspath(__file__))

spec = importlib.util.spec_from_file_location("c2r51", COUNTER)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def refs_at_base():
    out = []
    for path in c.ls_files(REPO, BASE, "corpus/knowledge"):
        if c.KNOW_RE.match(path):
            blob = c.show(REPO, BASE, path)
            if blob is not None:
                out.append((path, blob))
    return out


REFS = refs_at_base()


def score(text, label):
    body = c.shingles(c.body_text(text))
    if len(body) < c.MIN_BODY_SHINGLES:
        return {"label": label, "body": len(body),
                "verdict": "FAIL(body<%d)" % c.MIN_BODY_SHINGLES,
                "worst": None, "hits": None, "path": None}
    scored = []
    for path, blob in REFS:
        other = c.shingles(c.text_of(blob))
        hits = len(body & other)
        scored.append((hits / float(len(body)), hits, path))
    scored.sort(reverse=True)
    worst, hits, path = scored[0]
    return {"label": label, "body": len(body), "worst": worst, "hits": hits, "path": path,
            "verdict": "PASS" if worst <= c.MAX_OVERLAP else "FAIL"}


def table_only(text):
    return "\n".join(l for l in text.splitlines() if l.strip().startswith("|"))


VOCAB = ("harbor lantern meadow orchard pebble quartz ribbon saddle thistle umber vessel "
         "willow yarrow zephyr almond birch cedar dune ember fennel glacier hollow iris "
         "juniper kettle lichen marble nectar opal prairie quill raven sorrel tundra "
         "violet walnut xenon yucca zinnia acorn bramble cinder drizzle elm fjord "
         "gable hazel inlet jetty knoll loam mistle nutmeg olive plume quince reed spruce "
         "trellis upland vale wisp yew amber basin cobalt drift flint grove heath ivory "
         "jade kelp lagoon marsh nook oyster pine quarry ridge slate tide underbrush "
         "valley wattle yonder zenith").split()


def filler(n, seed=0x2F47):
    state, words = seed, []
    while len(words) < n:
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        words.append(VOCAB[(state >> 8) % len(VOCAB)])
    return " ".join(words)


def main():
    entry = c.text_of(c.show(REPO, BASE, ENTRY))
    if not entry:
        print("SETUP-FAIL: entry absent at base")
        return 2
    r51_body = c.body_text(entry)
    r51_sh = c.shingles(r51_body)

    print("== constants: NGRAM=%d MAX_OVERLAP=%.2f MIN_BODY_SHINGLES=%d"
          % (c.NGRAM, c.MAX_OVERLAP, c.MIN_BODY_SHINGLES))
    print("== base=%s corpus_files=%d" % (BASE, len(REFS)))
    print("== r51 entry: bytes=%d body_lines=%d body_shingles=%d"
          % (len(entry.encode()), len(r51_body.splitlines()), len(r51_sh)))

    tables = table_only(entry)
    print("== r51 table rows: lines=%d shingles_visible_to_body_text=%d"
          % (len(tables.splitlines()), len(c.shingles(c.body_text(tables)))))

    m = re.search(r"^## The chain$(.*?)^## State claims", entry, re.M | re.S)
    chain = m.group(1) if m else ""
    chain_sh = c.shingles(c.body_text(chain))
    print("== r51 chain steps 1-9: body_shingles=%d (%.1f%% of entry body shingles)"
          % (len(chain_sh), 100.0 * len(chain_sh) / len(r51_sh)))
    print("== chain shingles also in entry body: %d/%d"
          % (len(chain_sh & r51_sh), len(chain_sh)))

    fixtures = {}

    # F1: verbatim clone of the r51 entry under a new slug (same mechanism, same propositions)
    fixtures["f1_verbatim.md"] = entry

    # F2: verbatim clone + unrelated filler prose (dilution of the candidate's own denominator)
    fixtures["f2_diluted.md"] = entry + "\n\n## Notes\n\n" + filler(9000) + "\n"

    # F3: all r51 table rows verbatim + short synthetic novel prose
    fixtures["f3_tabled.md"] = (
        "# Clone by table\n\n## Proposition map\n\n" +
        "\n".join(l for l in entry.splitlines() if l.strip().startswith("|")) +
        "\n\n## Abstract\n\n" + " ".join("p%d" % i for i in range(400)) + "\n")

    # F4: every chain paragraph kept as a proposition, moved into table cells, plus real
    # (vocabulary) novel prose. Nothing of the mechanism is reworded; only its container changes.
    rows = []
    for para in re.split(r"\n\s*\n", chain.strip()):
        flat = re.sub(r"\s+", " ", para).strip()
        if not flat:
            continue
        head = re.sub(r"^\d+\.\s*\*\*|\*\*.*$", "", flat)[:60].strip() or "step"
        rows.append("| %s | %s |" % (head.replace("|", "/"), flat.replace("|", "/")))
    fixtures["f4_props_in_table.md"] = (
        "# Clone with proposition table\n\n## Proposition map\n\n"
        "| proposition | statement |\n|---|---|\n" + "\n".join(rows) +
        "\n\n## Abstract\n\n" + filler(420, seed=0x5A17) + "\n")

    # F5: mechanical paraphrase of the chain (synonym swap + sentence reversal) - proxy for
    # a human rewrite that keeps every proposition and changes every 8-gram.
    swaps = {"the": "a", "a": "one", "is": "remains", "are": "remain", "of": "for",
             "and": "plus", "to": "toward", "in": "inside", "that": "which", "this": "such",
             "with": "using", "by": "via", "from": "out of", "on": "atop", "for": "regarding",
             "not": "never", "no": "zero", "all": "every", "one": "a single", "two": "a pair of",
             "three": "a trio of", "four": "a quartet of", "five": "a quintet of",
             "first": "initial", "second": "subsequent", "same": "identical",
             "dispatcher": "handler", "bind": "binding", "table": "map", "argument": "tail",
             "name": "label", "press": "keystroke", "event": "occurrence", "path": "route",
             "socket": "ipc", "string": "text", "field": "slot", "call": "invoke",
             "returns": "yields", "return": "yield", "writes": "stores", "write": "store",
             "reads": "consults", "read": "consult", "calls": "invokes", "stored": "kept",
             "carries": "holds", "carried": "held", "entry": "record", "map": "lookup"}
    para = chain
    for src in sorted(swaps, key=len, reverse=True):
        para = re.sub(r"\b%s\b" % re.escape(src), swaps[src], para)
    sents = [s for s in re.split(r"(?<=\.)\s+", re.sub(r"\s+", " ", para)) if s]
    fixtures["f5_paraphrase.md"] = "\n\n## Restated\n\n" + " ".join(reversed(sents)) + "\n"

    print()
    for name, text in fixtures.items():
        with open(os.path.join(HERE, name), "w") as fh:
            fh.write(text)
        r = score(text, name)
        print("FIXTURE %-20s body=%5d worst=%s hits=%s top=%s verdict=%s"
              % (r["label"], r["body"],
                 "n/a" if r["worst"] is None else "%.2f%%" % (r["worst"] * 100),
                 r["hits"], r["path"], r["verdict"]))

    # Direct call of the committed counter's own clause_c() with each fixture as entry_text.
    # rev=BASE means no round-52 candidate files are in the reference set (there are none at base);
    # everything else is the committed function, unmodified.
    print()
    print("== direct clause_c(repo, BASE, BASE, <fixture>) from c2-r51-dispatch-entry.py")
    for name, text in fixtures.items():
        ok, detail, top = c.clause_c(REPO, BASE, BASE, text)
        print("CLAUSE_C %-20s ok=%d %s" % (name, ok, detail))

    n_body = len(r51_sh)
    need = int(n_body / c.MAX_OVERLAP) + 1
    print()
    print("== dilution arithmetic: clone body_shingles=%d; to score <=%.2f need body>=%d "
          "(+%d filler shingles)" % (n_body, c.MAX_OVERLAP, need, need - n_body))
    print("== f2 measured filler body_shingles=%d" % len(c.shingles(c.body_text(filler(9000)))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
