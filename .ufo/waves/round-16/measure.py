#!/usr/bin/env python3
"""Round-16 revision-bound structural counter: C1 sourced U1-U7 joins.

C1  one point per U1..U7 item covered by a corpus/knowledge note whose
    head-15 header carries `source:` with mined SOURCES rows that name the
    note in their `used-by`, plus `verified-at:` and `recheck:`, and exactly
    one `covers: U<N>` line. U4 keeps its three body facets; U5 must carry
    the decision sections `## Output management`, `## Colour management` and
    `## Unexercised feature behavior` with `[UNK]` in the last, AND both
    reserved rows S047/S048 mined, cited on the source line, and reciprocal
    in both directions. U6 must carry level-2 headings `## Layer ladder`,
    `## Safe boundary`, `## Unexercised delivery` with `[UNK]` in the
    delivery section, AND reciprocal mined A/B rows S051/S052. U7 must
    carry exact level-2 headings `## Producer contract`, `## Renderer
    boundary`, `## Safe observation`, `## Unexercised rendering` with
    `[UNK]` inside the rendering section, AND reciprocal mined A/B rows
    S053/S054 (round-15 U1-U6 semantics preserved). Score = 10 * items / 7.

Source-id reservation (round 16): S053 is reserved for the tagged Waybar
custom-module man page (waybar-custom.5.scd), S054 for the tagged
custom.cpp module source, and S055 for closure own-work safety evidence.
S055 is never credited to U7 by this probe; the U7 join requires the
documented-route pair S053/S054 only. Queued or rejected rows named in a
source line contribute no coverage.

Revision binding: the named revision is resolved to its commit SHA before
any input is read, and every input (gate bytes, SOURCES.md, README index,
knowledge notes, and the round-16 safety artifacts when present) is read
with `git show <sha>:<path>`. No gate is executed; `tools/mado-verify.sh`
is only hashed for the SHA256 gate observation, and the new static
action-plan gate artifacts are observed for presence and bytes only —
never executed and never folded into the coverage score. There is no C2
safety score here; conflating the gate's pass/fail with this counter
would double-report the same evidence. The probe is a structural
observation, not an admission verdict: a missing note, facet, reserved
row, or safety artifact is reported with exit 0, and source/body
semantics stay with L1.

C3  calibration observation only, causally separate from C1/C2: the
    original published literal rubric counts `corpus/QUALITY.md` numbered
    criterion lines (`^[0-9]+\. `) and the subset citing `lessons/` on the
    same line (`^[0-9]+\. .*lessons/`), emitted as numerator/denominator,
    exact matched id sets, and 10 * fraction. Multiline semantics are not
    broadened: wrapped continuation-line citations do not count. This
    reads revision bytes and never executes or scores the C2 gate.

Usage: python3 .ufo/waves/round-16/measure.py <revision>
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


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True)


rev_sha = git('rev-parse', '--verify', f'{rev}^{{commit}}').strip()


def source(path):
    return git('show', f'{rev_sha}:{path}')


def try_source(path):
    """Revision-bound bytes for an optional artifact; None when absent."""
    try:
        return source(path)
    except subprocess.CalledProcessError:
        return None


def used_by(row, path):
    return path in [p.strip() for p in row[11].split(',')]


def mined_ab(sid, path):
    """A named row that is mined, tier A/B, and names this note."""
    row = registry.get(sid)
    return (row is not None and row[8] == 'mined' and row[4] in ('A', 'B')
            and used_by(row, path))


def body_facets(text):
    """U5 decision sections, keyed on stable level-2+ headings.

    Required markers (case-insensitive, `##` or deeper):
      `## Output management`
      `## Colour management`
      `## Unexercised feature behavior`, whose section body carries `[UNK]`
    Each section may hold a decision table; the heading plus the explicit
    unknown label are the testable boundary, so wording inside the section is
    free and a prose-only mention cannot admit the item.
    """
    sections = {}
    current = None
    for line in text.splitlines():
        heading = re.match(r'^#{2,6}\s+(.*?)\s*$', line)
        if heading:
            current = heading.group(1).strip().lower()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    feature_heads = [h for h in sections
                     if re.match(r'unexercised feature behaviou?r\b', h)]
    facets = {
        'output_management': any(
            re.match(r'output[- ]management\b', h) for h in sections),
        'colour': any(
            re.match(r'colou?r[- ]management\b', h) for h in sections),
        'feature_unknown': bool(feature_heads) and '[unk]' in '\n'.join(
            h + '\n' + '\n'.join(sections[h])
            for h in feature_heads).lower(),
    }
    return facets


def level2_sections(text):
    """Level-2 heading bodies keyed by whitespace-normalized lowercase text.

    A level-3 heading remains part of its enclosing level-2 body, so a
    required section may carry its own subheadings without losing the body.
    """
    sections = {}
    current = None
    for line in text.splitlines():
        heading = re.match(r'^##(?!#)\s+(.*?)\s*$', line)
        if heading:
            current = re.sub(r'\s+', ' ', heading.group(1).strip().lower())
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def u6_facets(text):
    """U6 input-debugging ladder boundary, keyed on exact level-2 headings.

    Required: `## Layer ladder`, `## Safe boundary`, `## Unexercised
    delivery`, and `[UNK]` inside the delivery section. Heading position is
    not scored, so later errata cannot silently remove the unknown label;
    a prose-only or deeper-heading mention cannot admit the item.
    """
    sections = level2_sections(text)
    delivery = 'unexercised delivery'
    facets = {
        'layer_ladder': 'layer ladder' in sections,
        'safe_boundary': 'safe boundary' in sections,
        'unexercised_delivery': delivery in sections,
        'delivery_unknown': (delivery in sections
                             and '[unk]' in '\n'.join(
                                 sections[delivery]).lower()),
    }
    return facets


def u7_facets(text):
    """U7 Waybar module text-observation boundary, exact level-2 headings.

    Required: `## Producer contract`, `## Renderer boundary`, `## Safe
    observation`, `## Unexercised rendering`, and `[UNK]` inside the
    rendering section. The boundary is documentation of what the custom
    module's text field may carry through to the label; a rendered-pixel
    or live-compositor verification is not claimed and cannot substitute.
    A prose-only or deeper-heading mention cannot admit the item.
    """
    sections = level2_sections(text)
    rendering = 'unexercised rendering'
    facets = {
        'producer_contract': 'producer contract' in sections,
        'renderer_boundary': 'renderer boundary' in sections,
        'safe_observation': 'safe observation' in sections,
        'unexercised_rendering': rendering in sections,
        'rendering_unknown': (rendering in sections
                              and '[unk]' in '\n'.join(
                                  sections[rendering]).lower()),
    }
    return facets


# --- SOURCES registry (11-column contract + id/teaches cells) ---------------
registry = {}
for line in source('corpus/SOURCES.md').splitlines():
    cells = [x.strip() for x in line.split('|')]
    if len(cells) == 13 and re.fullmatch(r'S\d{3,}', cells[1]):
        registry[cells[1]] = cells

# Round-15 final required pair for U6; both must be mined, tier A/B, named
# in used-by, and cited on the note's source line. S007 is deliberately
# absent: its composite teaches cell was rejected/superseded by S051/S052.
U6_SOURCES = ('S051', 'S052')
# Round-16 required pair for U7. S055 is reserved for closure own-work
# safety evidence and is deliberately absent: own-work receipts cannot
# credit a documented-route item.
U7_SOURCES = ('S053', 'S054')

notes = git('ls-tree', '-r', '--name-only', rev_sha, '--',
            'corpus/knowledge').splitlines()
covered = set()
joined = []
u4_facets = {}
u5_candidates = []
u6_candidates = []
u6_facets_observed = {}
u7_candidates = []
u7_facets_observed = {}

for path in notes:
    if not path.endswith('.md'):
        continue
    text = source(path)
    header = '\n'.join(text.splitlines()[:15])
    provenance = re.search(r'^source:.*$', header, re.M)
    items = list(re.finditer(r'^covers: (U[1-7])$', header, re.M))
    item = items[0] if len(items) == 1 else None
    if not provenance or not item or not all(
            re.search(r'^' + key + r':\s*\S', header, re.M)
            for key in ('verified-at', 'recheck')):
        continue
    ids = re.findall(r'\bS\d{3,}\b', provenance[0])
    mined = [s for s in ids if s in registry and registry[s][8] == 'mined'
             and used_by(registry[s], path)]
    if item[1] == 'U4':
        u4_facets = {
            'phase': '| Which upstream development/compatibility phase'
                     in text and 'S005' in mined,
            'advertisement': '| Which interface/version' in text
                             and 'S041' in mined,
            'unexercised_behavior': '| Does the intended feature actually work?'
                                    in text and 'S043' in mined,
        }
        if not all(u4_facets.values()):
            continue
    if item[1] == 'U5':
        facets = body_facets(text)
        cited = set(ids)
        reserved = {sid: mined_ab(sid, path) for sid in ('S047', 'S048')}
        # Reciprocal in both directions: every reserved row names this note
        # and this note's head-15 source line cites it; no other mined row may
        # name the note without being cited on that same line (round-13 J4).
        inverse = all(s in cited for s, row in registry.items()
                      if row[8] == 'mined' and used_by(row, path))
        u5_candidates.append({'path': path, 'facets': facets,
                              'reserved': reserved, 'inverse': inverse})
        if not (all(facets.values()) and all(reserved.values()) and inverse):
            continue
    if item[1] == 'U6':
        facets = u6_facets(text)
        cited = set(ids)
        reserved = {sid: mined_ab(sid, path) for sid in U6_SOURCES}
        # Same reciprocal rule as U5: the required rows must name this note
        # and be cited on its source line; any other mined row naming the
        # note must be cited there too.
        inverse = all(s in cited for s, row in registry.items()
                      if row[8] == 'mined' and used_by(row, path))
        u6_facets_observed = facets
        u6_candidates.append({
            'path': path,
            'facets': facets,
            'reserved': reserved,
            'cited': sorted(cited),
            'inverse': inverse,
        })
        if not (all(facets.values()) and all(reserved.values()) and inverse):
            continue
    if item[1] == 'U7':
        facets = u7_facets(text)
        cited = set(ids)
        reserved = {sid: mined_ab(sid, path) for sid in U7_SOURCES}
        # Same reciprocal rule as U5/U6: S053/S054 must name this note and
        # be cited on its source line; any other mined row naming the note
        # (including S055) must be cited there too or the join fails.
        inverse = all(s in cited for s, row in registry.items()
                      if row[8] == 'mined' and used_by(row, path))
        u7_facets_observed = facets
        u7_candidates.append({
            'path': path,
            'facets': facets,
            'reserved': reserved,
            'cited': sorted(cited),
            'inverse': inverse,
        })
        if not (all(facets.values()) and all(reserved.values()) and inverse):
            continue
    if mined and any(registry[s][4] in ('A', 'B') for s in mined):
        covered.add(item[1])
        entry = {'path': path, 'covers': item[1], 'mined': mined}
        if item[1] == 'U5':
            entry['facets'] = facets
            entry['reserved'] = reserved
            entry['inverse'] = inverse
        if item[1] == 'U6':
            entry['facets'] = facets
            entry['reserved'] = reserved
            entry['inverse'] = inverse
        if item[1] == 'U7':
            entry['facets'] = facets
            entry['reserved'] = reserved
            entry['inverse'] = inverse
        joined.append(entry)

# --- navigation: every knowledge note indexed exactly once in README --------
index = source('corpus/README.md')
indexed = re.findall(r'^\| `knowledge/([^`]+\.md)`', index, re.M)
expected = {Path(p).name for p in notes if p.endswith('.md')}
nav = {
    'notes': len(expected),
    'indexed': sum(indexed.count(p) == 1 for p in expected),
    'missing': sorted(expected - set(indexed)),
    'extra': sorted(set(indexed) - expected),
    'duplicates': sorted(p for p in set(indexed) if indexed.count(p) != 1),
}
# --- SHA256 gate observation (no gate execution) ----------------------------
gate = source('tools/mado-verify.sh')
gate_sha = hashlib.sha256(gate.encode()).hexdigest()

# --- C3 calibration observation: literal lesson-grounding fraction --------
# Original published literal rubric, kept verbatim: a QUALITY criterion
# counts as grounded only when `lessons/` appears on the criterion's own
# numbered line (`^[0-9]+\. .*lessons/`); the denominator is every numbered
# criterion line (`^[0-9]+\. `). No multiline joining: a citation carried
# by a wrapped continuation line does not count, matching the published
# rule. Same-line `lessons/` occurrences that are not lesson citations
# still count — literal, not semantic. This is an observation only: it is
# causally separate from C1 coverage and C2 gate evidence and is never
# folded into either score.
quality = try_source('corpus/QUALITY.md')
if quality is None:
    cal_ids = []
    cal_lesson_ids = []
else:
    cal_ids = re.findall(r'^[0-9]+\. ', quality, re.M)
    cal_lesson_ids = re.findall(r'^[0-9]+\. .*lessons/', quality, re.M)
calibration = {
    'criteria_total': len(cal_ids),
    'lesson_grounded': len(cal_lesson_ids),
    'criterion_ids': [int(n.rstrip('. ')) for n in cal_ids],
    'lesson_grounded_ids': [int(n.split('.')[0]) for n in cal_lesson_ids],
    'ungrounded_ids': sorted(
        set(int(n.rstrip('. ')) for n in cal_ids)
        - set(int(n.split('.')[0]) for n in cal_lesson_ids)),
    'fraction': (round(len(cal_lesson_ids) / len(cal_ids), 4)
                 if cal_ids else 0),
    'score': (round(10 * len(cal_lesson_ids) / len(cal_ids), 4)
              if cal_ids else 0),
    'rule': 'literal: ^[0-9]+\\. .*lessons/ over ^[0-9]+\\. numbered lines',
}

# --- Round-16 safety artifacts: presence/bytes only, never executed and -----
# --- never folded into the coverage score. ----------------------------------
SAFETY_ARTIFACTS = (
    'tools/mado-action-plan.py',
    '.ufo/waves/round-16/safety-policy.json',
    '.ufo/waves/round-16/safety-cases.json',
)
safety = {}
for artifact in SAFETY_ARTIFACTS:
    blob = try_source(artifact)
    safety[artifact] = {
        'present': blob is not None,
        'sha256': (hashlib.sha256(blob.encode()).hexdigest()
                   if blob is not None else None),
        'executed': False,
        'scored': False,
    }

result = {
    'revision': rev,
    'revision_sha': rev_sha,
    'measure_inputs': {
        'gate': 'tools/mado-verify.sh',
        'gate_sha256': gate_sha,
        'gate_executed': False,
        'sources': 'corpus/SOURCES.md',
        'index': 'corpus/README.md',
        'knowledge_glob': 'corpus/knowledge/*.md',
        'safety_artifacts': list(SAFETY_ARTIFACTS),
        'safety_executed': False,
        'quality': 'corpus/QUALITY.md',
    },
    'source_registry': {
        'rows': len(registry),
        'tiers': {tier: sum(r[4] == tier for r in registry.values())
                  for tier in ('A', 'B', 'C')},
        'statuses': {status: sum(r[8] == status for r in registry.values())
                     for status in ('mined', 'queued', 'rejected')},
        'round15_required': {
            sid: {
                'present': sid in registry,
                'status': registry[sid][8] if sid in registry else None,
                'tier': registry[sid][4] if sid in registry else None,
            }
            for sid in U6_SOURCES
        },
        'round16_required': {
            sid: {
                'present': sid in registry,
                'status': registry[sid][8] if sid in registry else None,
                'tier': registry[sid][4] if sid in registry else None,
            }
            for sid in U7_SOURCES
        },
    },
    'coverage': {
        'items': sorted(covered),
        'count': len(covered),
        'score': round(10 * len(covered) / 7, 4),
        'joins': joined,
        'u4_facets': u4_facets,
        'u5_candidates': u5_candidates,
        'u6_present': bool(u6_candidates),
        'u6_facets': u6_facets_observed,
        'u6_candidates': u6_candidates,
        'u7_present': bool(u7_candidates),
        'u7_facets': u7_facets_observed,
        'u7_candidates': u7_candidates,
    },
    'navigation': nav,
    'safety_artifacts': safety,
    'calibration': calibration,
}
print(json.dumps(result, indent=2))
# A low coverage count, absent U7 join, or missing safety artifact is a
# measured result, not a failure of the observing command.
sys.exit(0)
