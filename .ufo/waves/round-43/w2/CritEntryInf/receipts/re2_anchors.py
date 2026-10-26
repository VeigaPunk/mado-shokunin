
import re2, json, sys
CANDS = ["org.omarchy.gkeep", "org.omarchy.gkeep2", "orgXomarchy.gkeep",
         "org.omarchy.gkeep\n", "org.omarchy.gkeep\nfoo", "\norg.omarchy.gkeep",
         "xorg.omarchy.gkeep", "org.omarchy.gkeep ", "ORG.OMARCHY.GKEEP",
         "org.omarchy.gkeep\r", "org-omarchy-gkeep", ""]
A = r"^(org.omarchy.gkeep)$"
B = r"(org.omarchy.gkeep)"
print("re2 version:", re2.version if hasattr(re2,"version") else "n/a")
def run(pat, optname=None):
    out=[]
    for c in CANDS:
        if optname is None:
            m = re2.fullmatch(pat, c) is not None
        else:
            o = re2.Options(); setattr(o, optname, True)
            m = re2.fullmatch(pat, c, options=o) is not None
        out.append(m)
    return out
for opt in [None, "one_line"]:
    a, b = run(A, opt), run(B, opt)
    print("options:", opt or "default(one_line=%s)" % re2.Options().one_line)
    for c, x, y in zip(CANDS, a, b):
        print("  %-24r anchored=%-5s bare=%-5s %s" % (c, x, y, "DIFF" if x!=y else "same"))
    print("  identical on all candidates:", a == b)
# dot semantics
print("dot matches X:", re2.fullmatch(A, "orgXomarchy.gkeep") is not None)
