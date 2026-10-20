#!/usr/bin/env python3
"""Revision-bound U-item join and exact-set negative cases; isolated temp roots."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[3]
rev = sys.argv[1]
def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True)
def source(path):
    return git('show', f'{rev}:{path}')
registry = {}
for line in source('corpus/SOURCES.md').splitlines():
    cells = [x.strip() for x in line.split('|')]
    if len(cells) == 13 and re.fullmatch(r'S\d{3,}', cells[1]):
        registry[cells[1]] = cells
notes = git('ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge').splitlines()
covered = set()
joined = []
u4_facets = {}
for path in notes:
    if not path.endswith('.md'):
        continue
    text = source(path)
    header = '\n'.join(text.splitlines()[:15])
    provenance = re.search(r'^source:.*$', header, re.M)
    item = re.search(r'^covers: (U[1-7])$', header, re.M)
    if not provenance or not item or not all(re.search(r'^'+key+r':\s*\S', header, re.M) for key in ('verified-at', 'recheck')):
        continue
    ids = re.findall(r'\bS\d{3,}\b', provenance[0])
    mined = [s for s in ids if s in registry and registry[s][8] == 'mined' and path in [p.strip() for p in registry[s][11].split(',')]]
    if item[1] == 'U4':
        u4_facets = {
            'phase': '| Which upstream development/compatibility phase' in text and 'S005' in mined,
            'advertisement': '| Which interface/version' in text and 'S041' in mined,
            'unexercised_behavior': '| Does the intended feature actually work?' in text and 'S043' in mined,
        }
        if not all(u4_facets.values()):
            continue
    if mined and any(registry[s][4] in ('A', 'B') for s in mined):
        covered.add(item[1]); joined.append({'path': path, 'covers': item[1], 'mined': mined})
index = source('corpus/README.md')
indexed = re.findall(r'^\| `knowledge/([^`]+\.md)`', index, re.M)
expected = {Path(p).name for p in notes if p.endswith('.md')}
nav = {'notes':len(expected), 'indexed':sum(indexed.count(p)==1 for p in expected), 'missing':sorted(expected-set(indexed)), 'extra':sorted(set(indexed)-expected), 'duplicates':sorted(p for p in set(indexed) if indexed.count(p)!=1)}
gate = source('tools/mado-verify.sh')
with tempfile.TemporaryDirectory(prefix='mado-r13-measure-') as temp:
    temp = Path(temp)
    script = temp/'gate.sh'; script.write_text(gate)
    # Source definitions only, never argument parsing or verify() against the host.
    fixture = gate[gate.index('build_fixture() {'):gate.index('\nselftest() {')]
    builder = temp/'fixture.sh'; builder.write_text(fixture+'\nbuild_fixture "$1"\n')
    cases=[]
    specs=[('extra-local','hypr.local.inventory',['extra:', 'extra.conf']),('replace-local','hypr.local.inventory',['missing:', 'extra:', 'xdph.conf', 'extra.conf']),('replace-source','hypr.root.sources_resolve',['missing:', 'extra:', 'ai-usage.conf', 'replacement.conf']),('missing-gkeep','hypr.local.inventory',['missing:', 'gkeep.conf'])]
    for name,row_id,need in specs:
        tree=temp/name
        build=subprocess.run(['bash',str(builder),str(tree)],text=True,capture_output=True)
        if build.returncode:
            raise RuntimeError(build.stderr)
        hypr=tree/'.config/hypr'
        if name=='extra-local': (hypr/'extra.conf').write_text('# isolated extra\n')
        elif name=='replace-local':
            (hypr/'xdph.conf').unlink(); (hypr/'extra.conf').write_text('# isolated replacement\n')
        elif name=='replace-source':
            conf=hypr/'hyprland.conf'
            conf.write_text(conf.read_text().replace('~/.config/hypr/ai-usage.conf','~/.config/hypr/replacement.conf'))
            (hypr/'replacement.conf').write_text('# isolated replacement\n')
        else: (hypr/'gkeep.conf').unlink()
        run=subprocess.run(['bash',str(script),'--root',str(tree),'--no-live'],text=True,capture_output=True)
        rows=[l for l in run.stdout.splitlines() if len(l.split())>=3 and l.split()[1]==row_id]
        detail=rows[0] if rows else ''
        detected=run.returncode==1 and len(rows)==1 and detail.split()[2]=='FAIL' and all(token in detail for token in need)
        cases.append({'case':name,'exit':run.returncode,'row':detail,'required':need,'named_set_detection':detected})
curated = ['S005', 'S017'] + [f'S{i:03}' for i in range(40, 47)]
result = {
    'revision': rev,
    'source_registry': {
        'rows': len(registry),
        'tiers': {tier: sum(r[4] == tier for r in registry.values()) for tier in ('A', 'B', 'C')},
        'statuses': {status: sum(r[8] == status for r in registry.values()) for status in ('mined', 'queued', 'rejected')},
        'round13_candidates': {
            'present': [s for s in curated if s in registry],
            'included': [s for s in curated if s in registry and registry[s][8] == 'mined'],
            'rejected': [s for s in curated if s in registry and registry[s][8] == 'rejected'],
        },
    },
    'coverage': {
        'items': sorted(covered), 'count': len(covered),
        'score': round(10 * len(covered) / 7, 4), 'joins': joined,
        'u4_facets': u4_facets,
    },
    'navigation': nav,
    'exact_set': {
        'cases': cases,
        'overall_failing_runs': sum(c['exit'] == 1 for c in cases),
        'detected': sum(c['named_set_detection'] for c in cases),
        'total': 4,
        'score': 2.5 * sum(c['named_set_detection'] for c in cases),
    },
}
print(json.dumps(result,indent=2))
# Before-state absence is a measured result, not failure of this measuring command.
sys.exit(0)
