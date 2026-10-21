#!/usr/bin/env python3
"""Count source rows at two immutable revisions, including exact mutable-field changes."""
import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

LANE = Path(__file__).resolve().parents[3]


def rows(revision):
    proc = subprocess.run(['git', '-C', str(LANE), 'show', revision + ':corpus/SOURCES.md'],
                          check=True, capture_output=True, text=True)
    result = {}
    for line in proc.stdout.splitlines():
        fields = [part.strip() for part in line.split('|')[1:-1]]
        if fields and re.fullmatch(r'S[0-9]{3,}', fields[0]):
            if len(fields) != 11 or fields[0] in result:
                raise ValueError('malformed or duplicate source row')
            result[fields[0]] = fields
    return result


def summary(data):
    return {'rows': len(data), 'tier': dict(sorted(Counter(row[3] for row in data.values()).items())),
            'status': dict(sorted(Counter(row[7] for row in data.values()).items()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', required=True)
    parser.add_argument('--after', required=True)
    args = parser.parse_args()
    before, after = rows(args.before), rows(args.after)
    changes = []
    for key in before.keys() & after.keys():
        for index, name in enumerate(('id', 'source', 'kind', 'tier', 'scope', 'anchor', 'teaches', 'status', 'opened', 'recheck', 'used-by')):
            if before[key][index] != after[key][index]:
                changes.append({'id': key, 'field': name, 'before': before[key][index], 'after': after[key][index]})
    print(json.dumps({'before_revision': args.before, 'after_revision': args.after,
                      'before': summary(before), 'after': summary(after),
                      'added': sorted(after.keys() - before.keys()), 'removed': sorted(before.keys() - after.keys()),
                      'changes': sorted(changes, key=lambda row: (row['id'], row['field']))}, sort_keys=True))


if __name__ == '__main__':
    main()
