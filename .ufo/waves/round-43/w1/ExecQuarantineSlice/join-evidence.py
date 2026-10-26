#!/usr/bin/env python3
"""Join the mado payload-absent slice against the 11 staged gkeep-theme files.

Inputs (read-only):
  R = /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
  P = /home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md
  K = /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/
Outputs: a TSV on stdout; nothing written.
"""
import glob, os, re, sys

R = '/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md'
P = '/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md'
K = '/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/'
THEME = sorted(glob.glob(K + 'gkeep-*.md')) + [K + 'glyph-and-geometry-r31.md']
assert len(THEME) == 11, THEME

def norm(u):
    u = u.strip().rstrip('.,;`')
    u = re.sub(r'[?#].*$', lambda m: m.group(0), u)
    return u

# --- slice: the register's mado rows, in file order -------------------------
reg = open(R, encoding='utf-8').read().splitlines()
slice_rows, all_rows = [], []
for i, ln in enumerate(reg, 1):
    if '`mado`' not in ln:
        continue
    f = [x.strip() for x in ln.split('|')]
    if len(f) < 5:
        continue
    rid = f[3].rstrip('`')
    if not re.fullmatch(r'S\d+', rid):
        continue
    # two table shapes: section 1 has class at f[4], source f[5], quotes f[6]
    #                        section 2 has prose at f[4], payload f[5]
    if f[4].startswith('`payload-absent`'):
        slice_rows.append(dict(id=rid, cls='payload-absent', src=f[5], quote=f[6] if len(f) > 6 else '', line=i))
    else:
        slice_rows.append(dict(id=rid, cls='prose:' + f[4], src=f[5], quote='', line=i))

# --- register-wide sources, every lane --------------------------------------
for i, ln in enumerate(reg, 1):
    if not ln.startswith('| `'):
        continue
    f = [x.strip() for x in ln.split('|')]
    if len(f) < 6:
        continue
    m = re.search(r'https?://\S+', f[5])
    if m:
        all_rows.append((i, norm(m.group(0)), f[3].rstrip('`')))
reg_urls = {u for _, u, _ in all_rows}

# --- staged rows: id -> cited source ---------------------------------------
staged = {}
for ln in open(P, encoding='utf-8'):
    if not ln.startswith('| S'):
        continue
    f = [x.strip() for x in ln.split('|')]
    m = re.match(r'S(\d+)', f[1])
    if m:
        staged['S' + m.group(1)] = f[2]

# --- cited ids inside the 11 theme files ------------------------------------
cited = {}
for f in THEME:
    for i, ln in enumerate(open(f, encoding='utf-8'), 1):
        for m in re.finditer(r'\bS(\d{3})\b', ln):
            cited.setdefault('S' + m.group(1), []).append((os.path.basename(f), i))

print('SECTION\tstaged_theme_files\t%d' % len(THEME))
print('SECTION\tslice_rows\t%d' % len(slice_rows))
print('SECTION\tcited_ids\t%d' % len(cited))
print('IDJOIN\t%s' % (sorted(set(r['id'] for r in slice_rows) & set(cited)) or 'EMPTY'))
print()
print('SLICE\tid\tclass\tsource\tline')
for r in slice_rows:
    print('SLICE\t%s\t%s\t%s\t%d' % (r['id'], r['cls'], r['src'][:110], r['line']))
print()
print('CITED\tid\tin_register_as_row\tsource_from_staged_append\tfirst_citation')
for cid in sorted(cited, key=lambda x: int(x[1:])):
    src = staged.get(cid, 'NOT-IN-STAGED-APPEND')
    m = re.search(r'https?://\S+', src)
    url = norm(m.group(0)) if m else src
    hit = 'YES' if cid in {r['id'] for r in slice_rows} else 'no'
    inreg = 'YES' if any(x[2] == cid for x in all_rows) else 'no'
    f, i = cited[cid][0]
    print('CITED\t%s\t%s/%s\t%s\t%s:%d' % (cid, hit, inreg, url[:110], f, i))
print()
print('URLJOIN\t%s' % (sorted({norm(re.search(r"https?://\S+", r['src']).group(0))
      for r in slice_rows if re.search(r'https?://\S+', r['src'])} &
      {norm(re.search(r"https?://\S+", staged.get(c, "")).group(0))
       for c in cited if re.search(r'https?://\S+', staged.get(c, ""))}) or 'EMPTY'))
print('REGWIDE\tregister_rows_citing_any_theme_source\t%d'
      % len({norm(re.search(r"https?://\S+", staged.get(c, "")).group(0))
             for c in cited if re.search(r'https?://\S+', staged.get(c, ""))} & reg_urls))
print('REGWIDE\tregister_rows_with_id_equal_to_cited_id\t%d'
      % len({c for c in cited if any(x[2] == c for x in all_rows)}))
