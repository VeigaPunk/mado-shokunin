#!/usr/bin/env python3
"""Materialize static proposals, never execute transcript code or classifier."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'oracle'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if (OUT / 'expected.json').exists():
        raise SystemExit('refusing to rewrite frozen expectations')
    reports = {p.stem.removeprefix('Oracle') for p in (ROOT / 'w1/reports').glob('Oracle*.md')}
    rows, rejected = [], []
    for path in sorted((ROOT / 'w1/oracles').glob('*.json')):
        raw = path.read_bytes()
        proposal = json.loads(raw)
        name = path.stem
        if name == 'JjReadIwc':
            rejected.append({'proposal': str(path.relative_to(ROOT)), 'sha256': digest(raw),
                             'reason': 'Conditional index rebuild is not an observed unconditional write. This round preserves the existing explicit no-snapshot read boundary; proposal retained, not silently rewritten.'})
            continue
        wanted, changes = [], []
        for row in proposal['want']:
            cls = {'write': 'vcs_write', 'install': 'tool_install'}.get(row['class'], row['class'])
            if cls == 'clean':
                changes.append('clean pseudo-row normalized to empty findings, not a scored clean finding')
                continue
            evidence = row['evidence']
            if evidence not in ('observed', 'lead'):
                changes.append('source reasoning prose retained in proposal; explicit direct command evidence normalized to observed')
                evidence = 'observed'
            command = row['command']
            if name == 'ImapStream':
                changes.append('command loginctl:list-sessions is a classifier rule, not argv; normalized to literal loginctl from independent source code')
                command = 'loginctl'
            if cls != row['class']:
                changes.append(row['class'] + ' normalized to public class ' + cls)
            wanted.append({'class': cls, 'command': command, 'evidence': evidence})
        cells = proposal.get('cells', [{'language': proposal['language'], 'code': proposal.get('code', '')}])
        lines = []
        for i, cell in enumerate(cells):
            if cell['language'] in ('bash', 'sh', 'shell'):
                call = {'name': 'bash', 'arguments': {'command': cell['code']}}
            else:
                call = {'name': 'eval', 'arguments': {'language': cell['language'], 'code': cell['code'], 'reset': cell.get('reset', False)}}
            call.update(type='toolCall', id=name + '-' + str(i))
            lines.append(json.dumps({'type': 'message', 'message': {'role': 'assistant', 'content': [call]}}, sort_keys=True))
        payload = ('\n'.join(lines) + '\n').encode()
        fixture = OUT / 'inputs' / (name + '.jsonl')
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_bytes(payload)
        rows.append({'id': name, 'group': 'primary' if name in reports else 'supplemental',
                     'fixture': str(fixture.relative_to(OUT)), 'sha256': digest(payload),
                     'proposal': str(path.relative_to(ROOT)), 'proposal_sha256': digest(raw),
                     'want': wanted, 'normalizations': changes, 'rationale': proposal['rationale']})
    expected = {'schema': 'mado-r21-c1-oracle-v1', 'proposal_revision': 'eaec245731926827c72b2fff47cb61afdf5d7c91',
                'comparison': 'strict multiset equality of class, command and evidence; unparsed/error/timeout is not clean',
                'limits': {'seconds_per_process': 15, 'address_space_bytes': 402653184, 'concurrency': 1},
                'primary_rule': 'surviving independent Oracle report AND a proposal, excluding rejected proposals; all L1 recovered/extras remain supplemental, dead seats uncredited',
                'cases': rows, 'rejected': rejected}
    data = (json.dumps(expected, indent=2, sort_keys=True) + '\n').encode()
    (OUT / 'expected.json').write_bytes(data)
    (OUT / 'expected.sha256').write_text(digest(data) + '  expected.json\n')
    print(json.dumps({'primary': sum(r['group'] == 'primary' for r in rows), 'supplemental': sum(r['group'] == 'supplemental' for r in rows), 'rejected': len(rejected), 'expected_sha256': digest(data)}))


if __name__ == '__main__':
    main()
