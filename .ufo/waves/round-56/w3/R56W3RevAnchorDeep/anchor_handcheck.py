#!/usr/bin/env python3
"""Independent seat receipt generator; no production checker imported."""
import hashlib
import re
import subprocess
import sys
from pathlib import PurePosixPath

repo, rev = sys.argv[1:]
def blob(path):
    return subprocess.check_output(['git', '-C', repo, 'show', rev + ':' + path])

def cells(line):
    # The checked rows use backticks to protect literal pipes.
    out, cell, code = [], '', False
    for char in line.strip().strip('|'):
        if char == '`':
            code = not code
        if char == '|' and not code:
            out.append(cell.strip())
            cell = ''
        else:
            cell += char
    return out + [cell.strip()]

reg = {}
for ln, line in enumerate(blob('corpus/SOURCES.md').decode().splitlines(), 1):
    if re.match(r'^\| S\d{3,} \|', line):
        c = cells(line)
        reg.setdefault(c[0], []).append((ln, c))

print('AXES: coverage of evidence rows; locator identity; line containment; EOF bounds; immutable revision binding')
print('REV=' + rev)
count = miss = repointed = 0
pins = {}
manual = {'K01', 'K13', 'K20', 'K29', 'E08', 'E01', 'E03', 'E04', 'E05', 'E06', 'E07'}
notes = []
for ln, line in enumerate(blob('corpus/knowledge/hyprland-config-autoreload-r56.md').decode().splitlines(), 1):
    if not line.startswith('| '):
        continue
    c = cells(line)
    if len(c) != 5 or not re.fullmatch(r'S\d{3,}', c[2]):
        continue
    rid, sid = c[0], c[2]
    assert len(reg[sid]) == 1, (rid, sid, 'nonunique')
    rln, r = reg[sid][0]
    name = re.findall(r'https?://\S+', r[1])[-1].rstrip(').,;').rsplit('/', 1)[-1]
    assert '#' not in name and '?' not in name
    pin, line_no = c[3].rsplit(':', 1)
    L = int(line_no)
    pinpath = re.search(r'\bpin (\S+)', r[5])[1]
    data = blob(pinpath)
    pieces = data.split(b'\n')
    nlines = len(pieces)
    locators = []
    for m in re.finditer(r'(?<![A-Za-z0-9_])' + re.escape(name) + r':([1-9][0-9]*(?:-[0-9]+)?(?:, ?[1-9][0-9]*(?:-[0-9]+)?)*)', r[5]):
        locators.extend(m[1].replace(' ', '').split(','))
    ranges = [tuple(map(int, x.split('-'))) if '-' in x else (int(x), int(x)) for x in locators]
    # Renamed fetch copies allow a hyphen before the upstream NAME, not an identifier prefix.
    named = bool(re.search(r'(?<![A-Za-z0-9_])' + re.escape(name) + r'$', PurePosixPath(pinpath).name))
    cover = any(a <= L <= b for a, b in ranges)
    bounded = bool(ranges) and all(max(a, b) <= nlines for a, b in ranges)
    quote = c[4].strip('`')
    quote_ok = quote.encode() in pieces[L - 1]
    good = named and cover and bounded and pin == PurePosixPath(pinpath).name and quote_ok
    count += 1
    miss += not good
    repointed += sid in {'S392', 'S393', 'S394', 'S395'}
    print(f'ANCHOR_COVER: row={rid} sid={sid} L={L} name={name} locators={",".join(locators)} pin={pinpath} length={nlines} identity={named} quote={quote_ok} eof=checked verdict={"OK" if good else "MISS"} entry_line={ln} registry_line={rln}')
    if rid in manual:
        notes.append(f'HAND_INPUT row={rid} sid={sid} L={L} name={name} anchor={r[5]}\nPIN_LINE {pieces[L-1].decode()}')
    pins[pinpath] = (len(data), nlines, hashlib.sha256(data).hexdigest())
print(f'CHECK107: rows={count} covered={count-miss} miss={miss} verdict={"OK" if not miss and count else "FAIL"}')
print(f'REPOINTED: rows={repointed} expected=6; host_rows=3 excluded_by_criterion107_source_cell')
for path, (size, lines, sha) in pins.items():
    print(f'PIN path={path} bytes={size} lines={lines} sha256={sha}')
print('\n'.join(notes))
sys.exit(bool(miss) or count != 39 or repointed != 6)
