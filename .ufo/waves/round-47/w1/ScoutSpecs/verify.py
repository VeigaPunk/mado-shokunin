import re,html,sys,json
sys.path.insert(0,'.')
from quotes import Q
PINS='pins/'
def norm_with_map(path):
    raw=open(PINS+path,encoding='utf8').read().split('\n')
    html_like=path.endswith(('.xml','.html'))
    out=[];m=[]
    for i,l in enumerate(raw,1):
        if html_like:
            l=re.sub(r'<(script|style)[^>]*>.*?</\1>','',l,flags=re.S)
            l=re.sub(r'<[^>]+>',' ',l); l=html.unescape(l)
        for tok in l.split():
            out.append(tok); m.append(i)
    return out,m
cache={}
def find(path,quote):
    if path not in cache: cache[path]=norm_with_map(path)
    toks,m=cache[path]
    qt=quote.split()
    # for xml/html quotes drop 'markup-only' mismatch: compare tokens after normalising spaces around punctuation
    n=len(qt)
    for i in range(len(toks)-n+1):
        if toks[i:i+n]==qt: return m[i],m[i+n-1]
    # tolerant join compare
    js=''.join(toks); jq=''.join(qt)
    k=js.find(jq)
    if k>=0:
        acc=0
        for t,ln in zip(toks,m):
            if acc+len(t)>k: s=ln;break
            acc+=len(t)
        e=k+len(jq);acc=0
        for t,ln in zip(toks,m):
            acc+=len(t)
            if acc>=e: return s,ln
    return None
rows=[];bad=0
for qid,pin,quote,xchk,rule in Q:
    wc=len(quote.split())
    r=find(pin,quote)
    x=''
    if xchk:
        rr=find(xchk,quote); x='html-ok' if rr else 'HTML-MISS'
        if rr is None: bad+=1
    if r is None: bad+=1; rows.append((qid,pin,'MISS','',wc,x,rule,quote)); continue
    rows.append((qid,pin,f"{r[0]}-{r[1]}" if r[0]!=r[1] else str(r[0]),'OK',wc,x,rule,quote))
    if wc>25: bad+=1; rows[-1]=rows[-1][:3]+('OVER25',)+rows[-1][4:]
with open('quotes-verified.tsv','w') as f:
    f.write('id\tpin\tline\tstatus\twords\txcheck\trule\tquote\n')
    for r in rows: f.write('\t'.join(map(str,r))+'\n')
print(len(rows),'quotes; problems:',bad)
for r in rows:
    if r[3]!='OK' or r[5]=='HTML-MISS': print(r[:6])
