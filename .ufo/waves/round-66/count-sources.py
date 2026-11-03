#!/usr/bin/env python3
"""Count committed SOURCES rows; not an admission gate."""
import argparse
import collections
import json
import re
import subprocess
p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--rev', required=True)
a = p.parse_args()
text = subprocess.check_output(['git', '-C', a.repo, 'show', a.rev + ':corpus/SOURCES.md'], text=True)
rows = [line.split('|')[1:-1] for line in text.splitlines() if re.match(r'^ {0,3}\|\s*S[0-9]{3,}\s*\|', line)]
print(json.dumps({'rev': a.rev, 'rows': len(rows), 'malformed': sum(len(row) != 11 for row in rows), 'tiers': dict(collections.Counter(row[3].strip() for row in rows)), 'statuses': dict(collections.Counter(row[7].strip() for row in rows))}, sort_keys=True))
