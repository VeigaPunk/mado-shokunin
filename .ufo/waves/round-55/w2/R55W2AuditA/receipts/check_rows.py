import re,sys
DOC='/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md'
FETCH='/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/fetch/'
want={'K01','K02','K03','K08','E01','E02','E08'}
doc=open(DOC,encoding='utf-8').read().splitlines()
for ln in doc:
    if not ln.startswith('|'): continue
    cells=[c.strip() for c in ln.strip().strip('|').split('|')]
    if len(cells)!=5 or cells[0] not in want: continue
    rid,prop,src,pin,quote=cells
    fname,lno=pin.rsplit(':',1); lno=int(lno)
    q=quote.strip('`')
    lines=open(FETCH+fname,encoding='utf-8',errors='replace').read().split('\n')
    text=lines[lno-1]
    print(f'{rid} {fname}:{lno} exact_substring={q in text} quote={q!r}')
    print(f'   line: {text.strip()}')
