import math
def rnd(v):  # std::round: half away from zero
    return math.floor(v+0.5) if v >= 0 else math.ceil(v-0.5)
def tool(bw, w, bx=0):
    return bx + (bw - w + 1)//2, w
def src(bw, w, bx=0):
    xd = bx + bw/2.0 - w/2.0
    x = rnd(xd)
    return int(x), int(rnd(xd + w - x))
disagree=[]; neg_integer_tie_agree=[]
for bw in range(1,61):
    for w in range(1,71):
        t=tool(bw,w); s=src(bw,w)
        tie=(bw-w)/2.0
        if t!=s: disagree.append((bw,w,tie,t,s))
        elif tie<0: neg_integer_tie_agree.append((bw,w,tie,t,s))
print("disagreements:",len(disagree))
print("first 6:",disagree[:6])
print("negative ties that AGREE:",len(neg_integer_tie_agree))
print("first 4:",neg_integer_tie_agree[:4])
# the round-80 sentence's counterexample: tie == -1.0
print("counterexample bw=1000 w=1002:",tool(1000,1002),src(1000,1002),"tie",(1000-1002)/2)
print("brief case bw=1000 w=1001:",tool(1000,1001),src(1000,1001),"tie",(1000-1001)/2)
# is every disagreement at a negative half-integer tie?
print("all disagreements have tie<0 and fractional .5:",all(t[2]<0 and abs(t[2]*2-round(t[2]*2))<1e-9 for t in disagree))
