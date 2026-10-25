import hashlib, json, os, re, stat, sys
ROOT=sys.argv[1]; spec=json.load(open(sys.argv[2]))
ROW=re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|"); ISO=re.compile(r"^\d{4}-\d{2}-\d{2}$"); CAD=re.compile(r"^\d+d$"); SYM=re.compile(r"^[A-Za-z][A-Za-z0-9 _-]*$")
def path_ok(rel):
    p=os.path.join(ROOT,rel)
    try:
        st=os.lstat(p)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1: return None
        real=os.path.realpath(p); rr=os.path.realpath(ROOT)
        if not (real==rr or real.startswith(rr+os.sep)): return None
        return open(p,'rb').read()
    except OSError: return None
def cells(line):
    q=line.split('|')
    if q and q[0]=='': q=q[1:]
    if q and q[-1]=='': q=q[:-1]
    return [x.strip() for x in q]
sb=path_ok('corpus/SOURCES.md'); sources=sb.decode('utf-8','replace') if sb else ''
rows={}
for ln in sources.splitlines():
    m=ROW.match(ln)
    if m: rows.setdefault(m.group(1),[]).append(ln)
tally={m:{'closed_entries':0,'closed_rows':0,'open_cites':0} for m in ('A','B')}; detail=[]
for mode in ('A','B'):
    for rel,ids in spec['entries'].items():
        eb=path_ok(rel); eclosed=eb is not None; e=eb.decode('utf-8','replace') if eb is not None else ''
        for sid in ids:
            blob=path_ok(spec['receipts'][sid]['path']); actual=hashlib.sha256(blob).hexdigest() if blob is not None else ''
            ql=[l for l in e.splitlines() if l.startswith(f"gate-quote: {sid} ")]; quote=ql[0][len(f"gate-quote: {sid} "):] if len(ql)==1 else None
            rws=rows.get(sid,[]); row=rws[0] if len(rws)==1 else None; cs=cells(row) if row is not None else []
            ok=False
            if blob is not None and row is not None and len(cs)==11:
                ub={t.strip() for t in cs[10].split(',') if t.strip()}; citing={r for r,ri in spec['entries'].items() if sid in ri}
                dg=spec['receipts'][sid]['sha256'] in cs[5]
                if mode=='B': dg=dg and actual in cs[5]
                ok=(ub==citing and cs[7]=='mined' and bool(ISO.match(cs[9]) or CAD.match(cs[9]) or SYM.match(cs[9])) and dg and quote is not None and 1<=len(quote.split())<=25 and quote.encode() in blob)
            if ok: tally[mode]['closed_rows']+=1
            else: tally[mode]['open_cites']+=1; eclosed=False
            if mode=='A':
                detail.append({'sid':sid,'row_count':len(rws),'cells':len(cs),'status':cs[7] if len(cs)==11 else None,'recheck':cs[9] if len(cs)==11 else None,'anchor_has_frozen_digest':blob is not None and row is not None and len(cs)==11 and spec['receipts'][sid]['sha256'] in cs[5],'anchor_has_actual_digest':blob is not None and row is not None and len(cs)==11 and actual in cs[5],'receipt_digest_matches_freezer':actual==spec['receipts'][sid]['sha256'],'quote_lines':len(ql),'quote_words':len(quote.split()) if quote is not None else None,'quote_is_substring':bool(blob is not None and quote is not None and quote.encode() in blob),'closed_counter_reading':ok})
        if eclosed: tally[mode]['closed_entries']+=1
for mode in ('A','B'):
    t=tally[mode]; print(f"INDEPENDENT-C1 strict{mode} closed_entries={t['closed_entries']} closed_rows={t['closed_rows']} open_cites={t['open_cites']}")
print("per-cite:",json.dumps(detail,indent=1))
print("sids_mentioned_in_entries:",sorted({m.group(0) for rel in spec['entries'] for m in re.finditer(r'S2[0-9]{2}',open(os.path.join(ROOT,rel)).read())}))
