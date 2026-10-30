import subprocess, re, hashlib
LANE='/home/vgpnk/Projects/shokunin/mado-shokunin'
BASE='13f0acbe3a15da2d9c08357a576d91dcadc85273'
TIP='0f3a54361a9824484d0801679ceb1fd8ac7c32e1'
def git(*args):
    return subprocess.check_output(['git','-C',LANE,*args]).decode()
def blob(rev,path): return git('show',rev+':'+path)
def rows(text):
    result={}
    for n,line in enumerate(text.splitlines(),1):
        if re.match(r'^ {0,3}\|\s*S[0-9]{3,}\s*\|',line):
            cells=[c.strip() for c in line.strip().strip('|').split('|')]
            assert len(cells)==11,(n,len(cells))
            assert cells[0] not in result
            result[cells[0]]=(n,cells)
    return result
def cites(text,sid):
    result=[]; fence=None
    for n,line in enumerate(text.splitlines(),1):
        m=re.match(r'^ {0,3}(`{3,}|~{3,})',line)
        if m:
            mark=m.group(1)
            if fence is None: fence=mark
            elif mark[0]==fence[0] and len(mark)>=len(fence): fence=None
            continue
        if fence is None and re.search(r'(?<![A-Za-z0-9])'+sid+r'(?![0-9])',line): result.append((n,line))
    return result
old=rows(blob(BASE,'corpus/SOURCES.md')); new=rows(blob(TIP,'corpus/SOURCES.md'))
print('AXES: cell-only integrity; receipt fidelity; citation fidelity; base-text immutability; hedge honesty')
print('LSP: xd://lsp unavailable (No such tool); literal token and blob comparison fallback, not semantic proof.')
print('COMMAND: git -C',LANE,'diff',BASE,TIP,'-- corpus/SOURCES.md')
print(git('diff',BASE,TIP,'--','corpus/SOURCES.md'))
print('CELL-SPLIT PROOF (1-indexed, all pre-existing rows checked):')
changes={}; pairs=[]; removed=[]; errors=[]
for sid,(ln,cells) in sorted(old.items()):
    if sid not in new: errors.append(('deleted-row',sid)); continue
    nn,ncells=new[sid]
    for i,(a,b) in enumerate(zip(cells,ncells),1):
        if a!=b:
            print(sid,'cell='+str(i),'base_line='+str(ln),'tip_line='+str(nn),'old='+repr(a),'new='+repr(b))
            if i!=11: errors.append(('non-usedby-change',sid,i))
    if cells[10]!=ncells[10]:
        changes[sid]=(cells[10],ncells[10])
        a=set(re.findall(r'corpus/knowledge/[A-Za-z0-9_.-]+\.md',cells[10]))
        b=set(re.findall(r'corpus/knowledge/[A-Za-z0-9_.-]+\.md',ncells[10]))
        pairs.extend((sid,p) for p in sorted(b-a)); removed.extend((sid,p) for p in sorted(a-b))
print('SUMMARY base_rows='+str(len(old))+' tip_rows='+str(len(new))+' checked_cells='+str(11*len(old))+' changed_rows='+str(len(changes))+' added_pairs='+str(len(pairs))+' removed_pairs='+repr(removed)+' errors='+repr(errors))
print('NEW_ROWS',sorted(set(new)-set(old)))
receipt=blob(TIP,'.ufo/waves/round-56/receipts/used-by-old-to-new.md')
logged={}
for line in receipt.splitlines():
    if re.match(r'^\| S\d+',line):
        c=[x.strip() for x in line.strip('|').split('|')]; logged[c[0]]=(c[1],c[2])
print('RECEIPT_TABLE_EQUAL',logged==changes,'missing_rows',sorted(set(changes)-set(logged)),'extra_rows',sorted(set(logged)-set(changes)))
for sid in sorted(set(changes)|set(logged)):
    if changes.get(sid)!=logged.get(sid): print('RECEIPT_MISMATCH',sid)
print('COMMAND: git -C',LANE,'diff',BASE,TIP,'--stat -- corpus/knowledge')
print(git('diff',BASE,TIP,'--stat','--','corpus/knowledge'))
entries=lambda rev: [p for p in git('ls-tree','-r','--name-only',rev,'--','corpus/knowledge').splitlines() if re.fullmatch(r'corpus/knowledge/[^/]+\.md',p)]
base_entries=entries(BASE); tip_entries=entries(TIP)
changed=[]
for p in base_entries:
    a=blob(BASE,p); b=blob(TIP,p)
    if a!=b: changed.append(p)
    print('BASE_TEXT',p,'UNCHANGED' if a==b else 'CHANGED','sha256='+hashlib.sha256(b.encode()).hexdigest())
print('BASE_TEXT_SUMMARY checked='+str(len(base_entries))+' changed='+repr(changed)+' new='+repr(sorted(set(tip_entries)-set(base_entries))))
print('PER-FILL CITATION AND RELIANCE EVIDENCE (all added pre-existing-row pairs):')
missing=[]
for i,(sid,p) in enumerate(sorted(pairs),1):
    lines=cites(blob(TIP,p),sid)
    if not lines: missing.append((sid,p))
    print('FILL',i,sid,p,'tip_registry_line='+str(new[sid][0]),'CITE='+('PASS' if lines else 'FAIL'))
    for n,line in lines: print(str(n)+': '+line)
print('FILLS_WITHOUT_CITATION',missing)
print('NEW_ENTRY_S300_CITATIONS (literal fallback requested by brief):')
p='corpus/knowledge/hyprland-config-autoreload-r56.md'
for n,line in enumerate(blob(TIP,p).splitlines(),1):
    if re.search(r'S3[0-9][0-9]',line): print(str(n)+': '+line)
print('NOTE: the 41 C3 fills belong to existing entries, not the new C1 entry; pair-wise checks above use each actual added path.')
