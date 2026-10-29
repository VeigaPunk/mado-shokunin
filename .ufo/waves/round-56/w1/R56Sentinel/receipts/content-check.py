import sys, re, os, hashlib
from collections import Counter
out = open(sys.argv[1], 'rb').read().decode('utf-8', 'replace')
paths = re.findall(r'path=(\S+)', out) + re.findall(r'via=(/\S+?):\d+', out)
paths = sorted(set(p for p in paths if p.startswith('/')))
main = '/home/vgpnk/.config/hypr/hyprland.conf'
files = sorted(set(paths + [main]))
print(f"output path tokens (unique absolute): {len(files)}")
exists = [p for p in files if os.path.isfile(p)]
print(f"regular files among them: {len(exists)}; missing/other: {len(files)-len(exists)}")
# content-leak check: every non-trivial line of every file the tool could have read must NOT appear in stdout
lines_total = 0; leaked = []
shape = Counter()
pat = {
 'pem': r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
 'kv_secret': r'(?i)\b(api[_-]?key|secret|token|passw(or)?d|private[_-]?key)\b\s*[:=]',
 'url_userinfo': r'[a-z]+://[^/\s:@]+:[^/\s@]+@',
 'aws_key': r'\b(AKIA|ASIA)[0-9A-Z]{16}\b',
 'github_token': r'\bgh[pousr]_[A-Za-z0-9]{20,}\b',
}
for p in exists:
    try: text = open(p, 'rb').read().decode('utf-8', 'replace')
    except Exception as e: shape['unreadable']+=1; continue
    for name, rx in pat.items():
        if re.search(rx, text): shape['shape:'+name+' in '+('main' if p==main else 'sourced')] += 1
    for ln in text.split('\n'):
        s = ln.strip()
        if len(s) < 12: continue
        lines_total += 1
        if s in out: leaked.append((p, s[:0]))  # record only file, never the text
print(f"non-trivial config lines checked (len>=12): {lines_total}")
print(f"config lines found verbatim in tool stdout: {len(leaked)}")
print("files with such a line:", sorted(set(l[0] for l in leaked))[:10])
print("secret-shape hits in files the tool read (class counts, no values):", dict(shape) if shape else "none")
# grammar check: every stdout line starts with the frozen prefixes
bad=[l for l in out.split('\n') if l and not l.startswith('MADO_WATCH')]
print(f"stdout lines not starting MADO_WATCH: {len(bad)}")
