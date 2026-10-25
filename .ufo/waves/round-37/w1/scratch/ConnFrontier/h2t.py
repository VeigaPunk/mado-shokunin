import sys,html.parser,re
class P(html.parser.HTMLParser):
    def __init__(s): super().__init__(); s.o=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style'): s.skip+=1
        if t in('p','div','li','tr','br','h1','h2','h3','h4','pre','code','td','th'): s.o.append('\n' if t not in('code','td','th') else (' ' if t!='pre' else '\n'))
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.o.append(d)
for f in sys.argv[1:]:
    p=P(); p.feed(open(f,encoding='utf-8',errors='replace').read())
    txt=re.sub(r'\n\s*\n+','\n',''.join(p.o))
    open(f[:-5]+'.txt','w').write(txt)
