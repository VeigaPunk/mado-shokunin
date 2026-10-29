import re,sys,os
from collections import Counter
rx = re.compile(r"(?<![A-Za-z0-9+/=_-])[A-Za-z0-9+/_-]{40,}={0,2}(?![A-Za-z0-9+/=_-])")
hexrx = re.compile(r"[0-9a-f]{40}")
for p in sys.argv[1:]:
    c = Counter()
    for ln,line in enumerate(open(p,encoding='utf-8',errors='replace').read().split("\n"),1):
        for m in rx.finditer(line):
            t=m.group(0)
            if hexrx.fullmatch(t): cls="git-sha-shaped(40 hex)"
            elif "/" in t: cls="path-shaped"
            elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",t): cls="identifier"
            else: cls="other-mixed"
            c[cls]+=1
            if cls=="other-mixed": print(f"   CHECK {os.path.basename(p)}:{ln} len={len(t)}")
    print(os.path.basename(p), dict(c))
