import re
S='/usr/bin/xdg-terminal-exec'; R='README-v0.14.3.md'
sl=open(S,encoding='utf-8',errors='replace').read().split('\n')
rl=open(R,encoding='utf-8',errors='replace').read().split('\n')
entry=open('entry.md',encoding='utf-8').read()
# (label, file, first-line, last-line, quote text, step-bounded?)
quotes=[
 ('step1','S',168,168,'XTE__APPLICATIONS_DIRS=${xte__dir%/}/applications/${XTE__APPLICATIONS_DIRS:+:${XTE__APPLICATIONS_DIRS}}'),
 ('step2','S',353,353,"All config files are read immediatelly, rather than on demand, even if it's more IO intensive"),
 ('step3','S',797,797,'''awk '{ print; sub(".*/[.]/", ""); gsub("/", "-"); print }' '''.strip()),
 ('step4','S',964,964,'command -v "$XTE__EXEC0" > /dev/null || return 1'),
 ('step5','S',1090,1090,'[ -z "${XTE__IS_TERMINAL}" ] && continue'),
 ('step6','S',1389,1389,'set -- "$XTE__EXECARG" "$@"'),
 ('step7','S',1331,1331,'''printf '%s' "${XTE__ENTRY_ID}${XTE__ENTRY_ACTION:+:}${XTE__ENTRY_ACTION}"'''),
 ('cache-readme','R',300,301,'Valid cache bypasses\nreading of any other file.'),
 ('cache-flag','S',1172,1172,'XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}'),
 ('cache-save','S',1457,1457,'save_cache "$1" &'),
]
fail=0
for label,f,a,b,q in quotes:
    src=sl if f=='S' else rl
    span='\n'.join(src[a-1:b])
    norm=lambda s:' '.join(s.split())
    words=len(re.findall(r'\S+', q.replace('\n',' ')))
    ok_pin = norm(q) in norm(span)
    ok_entry = norm(q) in norm(entry)
    flag = 'PASS' if (ok_pin and ok_entry and words<=25) else 'FAIL'
    if flag=='FAIL': fail+=1
    print(f'{flag} {label:13s} pin={f}:{a}-{b} words={words:2d} in_pin={ok_pin} in_entry={ok_entry}')
print(f'QUOTES: {len(quotes)-fail}/{len(quotes)} passed')
