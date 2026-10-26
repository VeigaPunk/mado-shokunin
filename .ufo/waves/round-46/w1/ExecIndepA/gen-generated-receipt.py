#!/usr/bin/env python3
"""Build receipts/generated-cases.txt: the two clause-g cases my build failed, with the oracle's stdout.

The oracle is the pinned reference, executed as a black box (report()), not read as source. Its sha256 is checked by
the counter; the same call is made here through the counter's own load_model().
"""
import importlib.util, json, random, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
spec = importlib.util.spec_from_file_location("c1", LANE + "/quality/counters/c1-r46-devices.py")
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
model = c1.load_model()
out = ["# clause-g cases my rev-2/rev-3 builds failed (counter logs receipts/c1-run2.txt:93, receipts/c1-run3.txt:93)",
       "# oracle stdout = pinned reference executed as a black box via the counter's load_model(); cases rebuilt"
       " from the same rng stream"]
for nonce, k in ((3930529855, 13), (1625735376, 132)):
    rng = random.Random(nonce ^ 0x5DEECE66D)
    tn = c1.names(nonce)
    for _ in range(k + 1):
        texts, dump = c1.gen_case(rng, tn, model)
    raw = json.dumps(dump, indent=2).encode()
    want, want_rc = c1.model_out(model, raw, texts)
    out.append("=== nonce %d case %d want_rc=%d ===" % (nonce, k, want_rc))
    for i, t in enumerate(texts):
        out.append("config %d: %s" % (i, json.dumps(t)))
    out.append("oracle stdout:")
    out.extend(want.rstrip("\n").split("\n"))
open("receipts/generated-cases.txt", "w").write("\n".join(out) + "\n")
print("wrote %d lines" % len(out))
