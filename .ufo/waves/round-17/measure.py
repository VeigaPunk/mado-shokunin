#!/usr/bin/env python3
"""Round-17 revision-bound rubric counter (hyaku phase 2).

Reads committed bytes only, via `git -C <lane> show REV:path` and
`git ls-tree`. Executes nothing from the revision; never touches host
state, package tools, services, or the compositor.

Usage: measure.py REV -> one JSON object on stdout.

  c1  calibration: literal QUALITY.md lesson-citation fraction.
      criteria      = lines matching ^[0-9]+\\. (numbered criterion lines)
      lesson_cited  = subset whose own line contains `lessons/`
      score         = 10 * lesson_cited / criteria (None at 0 criteria)

  c2  coverage: declared rubric V, provinces P1..P6.
      A province is covered by a knowledge entry (corpus/knowledge/*.md)
      whose FIRST 15 LINES contain a `source:` line carrying an S### token
      that resolves to a corpus/SOURCES.md registry row with
      status == mined, tier == A, and used-by naming
      `corpus/knowledge/<entry>` — AND the entry declares the province:

        * new form: a `surface:` line in the first 15 lines naming the
          P<n> token. Entries declaring `surface:` must additionally
          contain the exact level-2 headings `## Upstream contract`,
          `## Host declaration`, `## Safe observation`, and
          `## Unexercised behavior`, with `[UNK]` inside the body of the
          last section; otherwise the entry is listed under `rejected`
          with the reason and covers nothing.
        * legacy map: `covers: U1` or `covers: U2` -> P1,
          `covers: U7` -> P2. No other U-route maps to a province.

      count = provinces with >= 1 covering entry; score = 10*count/6.
      u_routes = distinct `covers: U[1-7]` tokens across all entry heads
      (harm watch — the legacy U-route census must not silently shrink).

  c3  operability capability: tools/mado-tripwire.py presence at REV
      plus sha256 of its committed blob. Presence/bytes only — the tool
      is never executed by this counter.

Exit 0 always prints the object (an absent or uncovered item is a
measured result). Exit 2 on usage error or an unresolvable revision.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[3]
if len(sys.argv) != 2:
    sys.stderr.write('usage: measure.py <revision>\n')
    raise SystemExit(2)
rev = sys.argv[1]


def git(*args, quiet=False):
    return subprocess.check_output(
        ['git', '-C', str(REPO), *args], text=True,
        stderr=subprocess.DEVNULL if quiet else None)


try:
    rev_sha = git('rev-parse', '--verify', f'{rev}^{{commit}}').strip()
except subprocess.CalledProcessError:
    sys.stderr.write(f'measure.py: cannot resolve revision {rev!r}\n')
    raise SystemExit(2)


def source(path):
    return git('show', f'{rev_sha}:{path}')


def try_source(path):
    """Revision-bound bytes for an optional artifact; None when absent."""
    try:
        return git('show', f'{rev_sha}:{path}', quiet=True)
    except subprocess.CalledProcessError:
        return None


# --- C1 calibration: literal lesson-citation fraction -----------------------
# Published literal rubric, kept verbatim from round 16: a QUALITY criterion
# counts as lesson-grounded only when `lessons/` appears on the criterion's
# own numbered line; the denominator is every `^[0-9]+\. ` line. No multiline
# joining — a citation on a wrapped continuation line does not count.
quality = try_source('corpus/QUALITY.md')
if quality is None:
    criteria_n = 0
    lesson_cited_n = 0
else:
    criteria_n = len(re.findall(r'^[0-9]+\. ', quality, re.M))
    lesson_cited_n = len(re.findall(r'^[0-9]+\. .*lessons/', quality, re.M))
c1 = {
    'criteria': criteria_n,
    'lesson_cited': lesson_cited_n,
    'score': (round(10 * lesson_cited_n / criteria_n, 4)
              if criteria_n else None),
}

# --- SOURCES registry (11-column contract: id|source|kind|tier|scope| -------
# --- anchor|teaches|status|opened|recheck|used-by) --------------------------
registry = {}
sources_doc = try_source('corpus/SOURCES.md')
if sources_doc is not None:
    # Wave-2 tightening (AttackRubricGaming E2): rows count only inside the
    # `## Registry` section and only as lines starting with `|`; a repeated
    # id is could-not-evaluate, never "last copy wins".
    in_registry = False
    for line in sources_doc.splitlines():
        if line.startswith('## '):
            in_registry = line.strip() == '## Registry'
            continue
        if not in_registry or not line.startswith('|'):
            continue
        cells = [x.strip() for x in line.split('|')]
        if len(cells) == 13 and re.fullmatch(r'S\d{3,}', cells[1]):
            if cells[1] in registry:
                sys.stderr.write('duplicate SOURCES id %s\n' % cells[1])
                sys.exit(2)
            registry[cells[1]] = cells


def used_by(row, path):
    return path in [p.strip() for p in row[11].split(',')]


def mined_a(sid, path):
    """Row exists, status mined, tier A, used-by names this entry path."""
    row = registry.get(sid)
    return (row is not None and row[8] == 'mined' and row[4] == 'A'
            and used_by(row, path))


# --- C2 coverage: declared rubric V, provinces P1..P6 -----------------------
PROVINCES = [f'P{i}' for i in range(1, 7)]
LEGACY_MAP = {'U1': 'P1', 'U2': 'P1', 'U7': 'P2'}
# T3: legacy credit is pinned to the entries that held it at 27cd06f.
LEGACY_PATHS = {
    ('corpus/knowledge/window-rule-effects-getprop.md', 'U1'),
    ('corpus/knowledge/hyprland-config-era-r12.md', 'U2'),
    ('corpus/knowledge/waybar-observation-boundaries-r16.md', 'U7'),
}
# T4: a cited upstream row must name its surface in its source or scope cell.
SURFACE_KEYWORDS = {
    'P1': ('hyprland', 'hypr.land', 'hyprwm/hyprland'),
    'P2': ('waybar',),
    'P3': ('walker', 'elephant'),
    'P4': ('terminal', 'alacritty', 'foot', 'kitty', 'ghostty'),
    'P5': ('theme', 'wallpaper', 'hyprpaper', 'swaybg'),
    'P6': ('hypridle', 'hyprlock', 'idle', 'session-lock'),
}
FACET_MIN_LINES = 3  # T5: each required section carries content
REQUIRED_HEADINGS = ('## Upstream contract', '## Host declaration',
                     '## Safe observation', '## Unexercised behavior')
HEAD_LINES = 15


def section_body(text, heading):
    """Body of one exact `## ` section up to the next `## ` heading or EOF."""
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == heading)
    except StopIteration:
        return None
    body = []
    for l in lines[start + 1:]:
        if l.startswith('## '):
            break
        body.append(l)
    return '\n'.join(body)


notes = git('ls-tree', '-r', '--name-only', rev_sha, '--',
            'corpus/knowledge').splitlines()

covered = {p: [] for p in PROVINCES}
rejected = []
u_routes = set()

for path in sorted(notes):
    if not path.endswith('.md'):
        continue
    text = source(path)
    head = text.splitlines()[:HEAD_LINES]

    src_tokens = set()
    for line in head:
        if line.startswith('source:'):
            src_tokens.update(re.findall(r'S\d{3}', line))
    ok_sources = sorted(s for s in src_tokens if mined_a(s, path))
    sourced = bool(ok_sources)

    surfaces = set()
    covers = set()
    for line in head:
        if line.startswith('surface:'):
            # T2: exact single-token form only; anything else is malformed.
            m = re.fullmatch(r'surface: (P[1-6])', line.rstrip())
            surfaces.add(m.group(1) if m else 'MALFORMED')
        if line.startswith('covers:'):
            covers.update(re.findall(r'U[1-7]\b', line))
    u_routes.update(covers)

    if surfaces:
        missing = [h for h in REQUIRED_HEADINGS
                   if section_body(text, h) is None]
        unex = section_body(text, '## Unexercised behavior')
        if 'MALFORMED' in surfaces:
            rejected.append({'path': path, 'declared': sorted(surfaces),
                             'reason': 'surface line must be exactly `surface: P<n>`'})
            continue
        thin = [h for h in REQUIRED_HEADINGS if h not in missing and
                sum(1 for l in section_body(text, h).splitlines() if l.strip())
                < FACET_MIN_LINES]
        if thin:
            rejected.append({'path': path, 'declared': sorted(surfaces),
                             'reason': 'sections under content floor: ' + ', '.join(thin)})
            continue
        if missing:
            rejected.append({
                'path': path,
                'declared': sorted(surfaces),
                'reason': 'missing required headings: ' + ', '.join(missing),
            })
            continue
        if '[UNK]' not in unex:
            rejected.append({
                'path': path,
                'declared': sorted(surfaces),
                'reason': 'no [UNK] inside `## Unexercised behavior` section',
            })
            continue
        if not sourced:
            rejected.append({
                'path': path,
                'declared': sorted(surfaces),
                'reason': 'no head `source:` S### token resolves to a mined '
                          'tier-A SOURCES row naming this entry in used-by',
            })
            continue
        # L1 tightening (round 17, before integration measurement; stricter,
        # never wider): one surface per entry, and at least one cited row must
        # be an upstream web source of kind docs/spec/code (not own-work or a
        # host-file row alone).
        if len(surfaces) != 1:
            rejected.append({
                'path': path,
                'declared': sorted(surfaces),
                'reason': 'an entry may declare exactly one surface',
            })
            continue
        (only_surface,) = tuple(surfaces) if len(surfaces) == 1 else ('',)
        upstream = [s for s in ok_sources
                    if registry[s][3] in ('docs', 'spec', 'code')
                    and 'https://' in registry[s][2]
                    and any(k in (registry[s][2] + ' ' + registry[s][5]).lower()
                            for k in SURFACE_KEYWORDS.get(only_surface, ()))]
        if not upstream:
            rejected.append({
                'path': path,
                'declared': sorted(surfaces),
                'reason': 'no cited mined tier-A row is an upstream https '
                          'source of kind docs/spec/code naming the surface',
            })
            continue
        for p in sorted(surfaces):
            covered[p].append({
                'path': path,
                'reason': f'surface: {p}',
                'sources_ok': ok_sources,
            })

    if not sourced:
        # Legacy map also requires the mined tier-A used-by join.
        continue
    for u in sorted(covers):
        prov = LEGACY_MAP.get(u)
        if prov and (path, u) in LEGACY_PATHS:
            covered[prov].append({
                'path': path,
                'reason': f'legacy covers: {u} -> {prov}',
                'sources_ok': ok_sources,
            })

count = sum(1 for p in PROVINCES if covered[p])
c2 = {
    'count': count,
    'score': round(10 * count / 6, 4),
    'provinces': {p: {'covered': bool(covered[p]), 'entries': covered[p]}
                  for p in PROVINCES},
    'rejected': rejected,
    'u_routes': len(u_routes),
    'u_routes_seen': sorted(u_routes),
}

# --- C3 operability capability: presence and bytes only, never executed -----
tool = try_source('tools/mado-tripwire.py')
c3 = {
    'tool_present': tool is not None,
    'sha256': (hashlib.sha256(tool.encode()).hexdigest()
               if tool is not None else None),
}

result = {
    'schema': 'mado-measure-r17-v1',
    'rev': rev,
    'commit': rev_sha,
    'c1': c1,
    'c2': c2,
    'c3': c3,
}
print(json.dumps(result, indent=2))
# A low count, missing province, or absent tool is a measured result,
# not a failure of the observing command.
sys.exit(0)
