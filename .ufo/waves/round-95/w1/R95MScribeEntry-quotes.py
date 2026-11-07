#!/usr/bin/env python3
import hashlib, os, re
F = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/fetch"
S = os.path.dirname(os.path.abspath(__file__))
Q = [
 ("xdgmime.c",523,527),("xdgmime.c",533,533),("xdgmime.c",540,540),("xdgmime.c",56,56),
 ("xdgmimeint.c",185,186),("xdgmimeint.c",189,189),
 ("xdgmimecache.c",185,186),("xdgmimecache.c",202,202),("xdgmimecache.c",220,221),
 ("xdgmimecache.c",225,228),("xdgmimecache.c",230,235),("xdgmimecache.c",257,258),
 ("xdgmimecache.c",262,263),("xdgmimecache.c",290,290),("xdgmimecache.c",305,308),
 ("xdgmimecache.c",773,774),("xdgmimecache.c",784,784),("xdgmimecache.c",83,84),
 ("xdgmimecache.c",948,952),("xdgmimecache.c",957,961),("xdgmimecache.c",965,967),
 ("xdgmimecache.c",969,971),("xdgmimecache.c",1019,1022),
 ("gcontenttype-fdo.c",542,544),("gcontenttype-fdo.c",589,589),("gcontenttype-fdo.c",597,603),
 ("gcontenttype-fdo.c",607,608),("gcontenttype-fdo.c",613,614),("gcontenttype-fdo.c",625,628),
 ("gcontenttype-fdo.c",636,638),("gcontenttype-fdo.c",641,647),("gcontenttype-fdo.c",654,654),
 ("gcontenttype-fdo.c",663,663),("gcontenttype-fdo.c",680,682),("gcontenttype.c",315,320),
]
cache={}
bad=[]
for f,a,b in Q:
    p = os.path.join(F,f)
    if f in ("gstrfuncs.c","gstrfuncs.h"):
        p = os.path.join(S,f)
    if not os.path.exists(p):
        p = os.path.join(S,f)
    L = open(p,"rb").read().decode("utf-8","surrogateescape").splitlines()
    h = hashlib.sha256(open(p,"rb").read()).hexdigest()
    txt = re.sub(r"\s+"," "," ".join(L[a-1:b])).strip()
    n = len(txt.split())
    flag = "" if n <= 25 else "  <<OVER25"
    print("%s:%d-%d  [%d words] sha256 %s  |%s|%s" % (f,a,b,n,h[:12],txt,flag))
    if n>25: bad.append((f,a,b,n))
print("OVER25:",bad)
