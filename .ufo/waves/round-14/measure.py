#!/usr/bin/env python3
"""Round-14 revision-bound counters: C1 sourced U1-U7 joins and C2
directory-shaped source targets.

C1  one point per U1..U7 item covered by a corpus/knowledge note whose
    head-15 header carries `source:` with mined SOURCES rows that name the
    note in their `used-by`, `verified-at`, `recheck`, and exactly one
    `covers: U<N>` line. U4 keeps its three body facets; U5 must carry the
    decision sections `## Output management`, `## Colour management` and
    `## Unexercised feature behavior` with `[UNK]` in the last, AND both
    reserved rows S047/S048 mined, cited on the source line, and reciprocal
    in both directions. Score = 10 * items / 7.

C2  three isolated fixtures built by the measured gate revision's own
    build_fixture(): (1) a directory in place of
    default/hypr/windows.conf, (2) a toggle glob whose only match is a
    directory, (3) a toggle glob mixing a directory with a regular file. A
    case counts only when the gate at that revision exits 1, the sole FAIL
    row is hypr.root.sources_resolve, that row's `non-regular:` clause
    equals exactly the expected display path, no unresolved/missing/extra
    class is present, the toggle status is PASS (direct, mixed) or NOTE
    (all-directory), the mixed detail omits the regular window-no-gaps.conf,
    and a second private root reproduces the detail byte-identically. The
    denominator is the scored case list of three. A missing owning/control
    row or a gate exit outside 0/1 refuses setup. Clean, order-swapped,
    symlink-to-regular, newline-regular, ai-usage-directory-overlap,
    direct-missing and zero-match-glob runs are preservation controls
    outside the score.

Revision binding: the named revision is resolved to its commit SHA before
any input is read, and every input is read with `git show <sha>:<path>`.
The extracted gate runs only with `--root <private fixture> --no-live`; the
host config tree is never a root and no substrate is read or written.

Usage: python3 .ufo/waves/round-14/measure.py <revision>
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

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


def rows_for(output, row_id):
    return [line for line in output.splitlines()
            if len(line.split()) >= 3 and line.split()[1] == row_id]


def row_status(detail):
    return detail.split()[2] if detail else ''


def non_regular_members(detail):
    """Members of the `non-regular:` clause, in emitted order.

    The clause opens at `non-regular:` and closes at the next detail class
    (`missing:`/`extra:`); the paths inside it are the refused targets only.
    """
    marker = 'non-regular:'
    if marker not in detail:
        return []
    after = detail.split(marker, 1)[1]
    for stop in (' missing:', ' extra:'):
        cut = after.find(stop)
        if cut != -1:
            after = after[:cut]
    return after.split()


def fail_rows(output):
    return [line for line in output.splitlines()
            if len(line.split()) >= 3 and line.split()[2] == 'FAIL']


# --- SOURCES registry (11-column contract + id/teaches cells) ---------------
registry = {}
for line in source('corpus/SOURCES.md').splitlines():
    cells = [x.strip() for x in line.split('|')]
    if len(cells) == 13 and re.fullmatch(r'S\d{3,}', cells[1]):
        registry[cells[1]] = cells


def used_by(row, path):
    return path in [p.strip() for p in row[11].split(',')]


def mined_ab(sid, path):
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


notes = git('ls-tree', '-r', '--name-only', rev_sha, '--',
            'corpus/knowledge').splitlines()
covered = set()
joined = []
u4_facets = {}
u5_candidates = []

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
    if mined and any(registry[s][4] in ('A', 'B') for s in mined):
        covered.add(item[1])
        entry = {'path': path, 'covers': item[1], 'mined': mined}
        if item[1] == 'U5':
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

# --- C2: extract the measured gate and its fixture builder ------------------
gate = source('tools/mado-verify.sh')
gate_sha = hashlib.sha256(gate.encode()).hexdigest()
if 'build_fixture() {' not in gate or '\nselftest() {' not in gate:
    raise SystemExit('SETUP: gate revision lacks build_fixture()/selftest() markers')
fixture_src = gate[gate.index('build_fixture() {'):gate.index('\nselftest() {')]

HYPR = Path('.config') / 'hypr'
TOGGLES = Path('.local') / 'state' / 'omarchy' / 'toggles' / 'hypr'

with tempfile.TemporaryDirectory(prefix='mado-r14-measure-') as temp:
    temp = Path(temp)
    script = temp / 'gate.sh'
    script.write_text(gate)
    builder = temp / 'fixture.sh'
    builder.write_text(fixture_src + '\nbuild_fixture "$1"\n')

    def build(name):
        tree = temp / name
        built = subprocess.run(['bash', str(builder), str(tree)],
                               text=True, capture_output=True)
        if built.returncode:
            raise RuntimeError(f'fixture {name}: {built.stderr.strip()}')
        return tree

    def gate_run(tree, label):
        run = subprocess.run(['bash', str(script), '--root', str(tree),
                              '--no-live'], text=True, capture_output=True)
        if run.returncode not in (0, 1):
            raise RuntimeError(
                f'{label}: gate exit {run.returncode} (usage/setup, not a verdict)')
        return run

    def need_row(output, row_id, label):
        rows = rows_for(output, row_id)
        if len(rows) != 1:
            raise RuntimeError(
                f'{label}: expected one {row_id} row, got {len(rows)}')
        return rows[0]

    def direct_directory(tree):
        p = (tree / '.local' / 'share' / 'omarchy' / 'default' / 'hypr'
             / 'windows.conf')
        p.unlink()
        p.mkdir()
        if not p.is_dir() or p.is_file():
            raise RuntimeError('direct-directory: mutation did not leave a directory')
        return ('~/.local/share/omarchy/default/hypr/windows.conf',
                'windows.conf')

    def all_directory_glob(tree):
        p = tree / TOGGLES / 'window-no-gaps.conf'
        p.unlink()
        p.mkdir()
        if not p.is_dir() or p.is_file():
            raise RuntimeError('all-directory-glob: mutation did not leave a directory')
        return ('~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf',
                'window-no-gaps.conf')

    def mixed_glob_directory(tree):
        p = tree / TOGGLES / 'dir.conf'
        p.mkdir()
        if not p.is_dir():
            raise RuntimeError('mixed-glob-directory: mutation did not leave a directory')
        return '~/.local/state/omarchy/toggles/hypr/dir.conf', 'dir.conf'

    specs = [
        ('direct-directory', direct_directory),
        ('all-directory-glob', all_directory_glob),
        ('mixed-glob-directory', mixed_glob_directory),
    ]
    toggle_expected = {
        'direct-directory': 'PASS',
        'all-directory-glob': 'NOTE',
        'mixed-glob-directory': 'PASS',
    }
    cases = []
    for name, mutate in specs:
        tree = build(name)
        affected_path, affected = mutate(tree)
        run = gate_run(tree, name)
        src_detail = need_row(run.stdout, 'hypr.root.sources_resolve', name)
        inv_detail = need_row(run.stdout, 'hypr.local.inventory', name)
        inc_detail = need_row(run.stdout, 'hypr.root.include_graph', name)
        toggle_detail = need_row(run.stdout, 'hypr.toggle.no_gaps', name)

        fails = fail_rows(run.stdout)
        sole_fail = (len(fails) == 1
                     and fails[0].split()[1] == 'hypr.root.sources_resolve')
        members = non_regular_members(src_detail)
        clean_classes = not any(token in src_detail for token in
                                ('unresolved:', 'missing:', 'extra:'))
        absent_token = ('window-no-gaps.conf'
                        if name == 'mixed-glob-directory' else None)
        absent_ok = absent_token is None or absent_token not in src_detail
        toggle_ok = row_status(toggle_detail) == toggle_expected[name]

        # Second private root, same mutation: the owning detail must be
        # byte-identical, so a stable display path is measured rather than
        # assumed from one temp prefix. The replica is not a fourth case.
        replica_tree = build('replica-' + name)
        replica_path, replica_affected = mutate(replica_tree)
        if (replica_path, replica_affected) != (affected_path, affected):
            raise RuntimeError(f'{name}: replica mutation diverged')
        replica_run = gate_run(replica_tree, 'replica-' + name)
        replica_src = need_row(replica_run.stdout,
                               'hypr.root.sources_resolve', 'replica-' + name)
        stable = replica_src == src_detail

        detected = (run.returncode == 1
                    and row_status(src_detail) == 'FAIL'
                    and members == [affected_path]
                    and clean_classes
                    and absent_ok
                    and sole_fail
                    and toggle_ok
                    and stable)
        cases.append({
            'case': name,
            'affected_path': affected_path,
            'affected_basename': affected,
            'non_regular_members': members,
            'clause_equals_expected': members == [affected_path],
            'clean_classes': clean_classes,
            'absent_token': absent_token,
            'absent_satisfied': absent_ok,
            'owning_row': 'hypr.root.sources_resolve',
            'sources_resolve': src_detail,
            'replica_detail': replica_src,
            'detail_stable': stable,
            'fail_row_ids': [line.split()[1] for line in fails],
            'sole_fail_resolver': sole_fail,
            'toggle_expected': toggle_expected[name],
            'toggle_status_ok': toggle_ok,
            'toggle_no_gaps': toggle_detail,
            'local_inventory': inv_detail,
            'include_graph': inc_detail,
            'overall_exit': run.returncode,
            'named_non_regular_detection': detected,
        })
    if len(cases) != len(specs):
        raise RuntimeError('scored case set incomplete; denominator not derived')
    scored_total = len(cases)
    scored_detected = sum(c['named_non_regular_detection'] for c in cases)

    # Preservation controls (not scored): clean exact set, an order-only swap,
    # and a symlink-to-regular direct target. The order swap must move
    # hypr.root.include_graph to FAIL while hypr.root.sources_resolve keeps
    # the exact set (no non-regular detail). The symlink control asserts only
    # that a link to a regular file still resolves; it broadens no admission
    # and awards no point.
    clean_tree = build('control-clean')
    clean_run = gate_run(clean_tree, 'control-clean')
    clean_src = need_row(clean_run.stdout, 'hypr.root.sources_resolve',
                         'control-clean')
    clean_inc = need_row(clean_run.stdout, 'hypr.root.include_graph',
                         'control-clean')

    swap_tree = build('control-order-swap')
    swap_conf = swap_tree / HYPR / 'hyprland.conf'
    lines = swap_conf.read_text().splitlines()
    try:
        first = lines.index('source = ~/.config/hypr/monitors.conf')
        second = lines.index('source = ~/.config/hypr/input.conf')
    except ValueError as exc:
        raise RuntimeError(f'control-order-swap: source line absent: {exc}')
    if first == second:
        raise RuntimeError('control-order-swap: indices collapsed; no-op refused')
    lines[first], lines[second] = lines[second], lines[first]
    swap_conf.write_text('\n'.join(lines) + '\n')
    swapped = swap_conf.read_text().splitlines()
    if (swapped[first] != 'source = ~/.config/hypr/input.conf'
            or swapped[second] != 'source = ~/.config/hypr/monitors.conf'):
        raise RuntimeError('control-order-swap: swap did not take effect')
    swap_run = gate_run(swap_tree, 'control-order-swap')
    swap_src = need_row(swap_run.stdout, 'hypr.root.sources_resolve',
                        'control-order-swap')
    swap_inc = need_row(swap_run.stdout, 'hypr.root.include_graph',
                        'control-order-swap')

    link_tree = build('control-symlink-regular')
    link_path = (link_tree / '.local' / 'share' / 'omarchy' / 'default'
                 / 'hypr' / 'windows.conf')
    link_path.unlink()
    link_path.symlink_to('looknfeel.conf')
    if not link_path.is_symlink() or not link_path.is_file():
        raise RuntimeError(
            'control-symlink-regular: link does not resolve to a regular file')
    link_run = gate_run(link_tree, 'control-symlink-regular')
    link_src = need_row(link_run.stdout, 'hypr.root.sources_resolve',
                        'control-symlink-regular')
    link_inc = need_row(link_run.stdout, 'hypr.root.include_graph',
                        'control-symlink-regular')

    # Newline-regular control: a second REGULAR toggle whose basename carries a
    # newline. The glob must transport it as one regular member (the gate's F6
    # fix); the fixture is unscored and asserts only that the source census
    # stays PASS, never that new detection exists.
    newline_tree = build('control-newline-regular')
    newline_name = 'new\nline.conf'
    (newline_tree / TOGGLES / newline_name).write_text(
        '# fixture newline-name regular toggle\n')
    newline_run = gate_run(newline_tree, 'control-newline-regular')
    newline_src = need_row(newline_run.stdout, 'hypr.root.sources_resolve',
                           'control-newline-regular')
    newline_inc = need_row(newline_run.stdout, 'hypr.root.include_graph',
                           'control-newline-regular')

    # Unscored old-error/overlap controls. The ai-usage directory is the
    # original overlap candidate: its owning row and hypr.local.inventory are
    # both expected to speak, which is why it is not a scored case. The
    # direct-missing and zero-match glob cases assert the pre-existing
    # `unresolved:` class is retained and `non-regular:` is not repurposed.
    overlap_tree = build('control-ai-usage-directory')
    overlap_path = overlap_tree / HYPR / 'ai-usage.conf'
    overlap_path.unlink()
    overlap_path.mkdir()
    if not overlap_path.is_dir() or overlap_path.is_file():
        raise RuntimeError(
            'control-ai-usage-directory: mutation did not leave a directory')
    overlap_run = gate_run(overlap_tree, 'control-ai-usage-directory')
    overlap_src = need_row(overlap_run.stdout, 'hypr.root.sources_resolve',
                           'control-ai-usage-directory')
    overlap_inv = need_row(overlap_run.stdout, 'hypr.local.inventory',
                           'control-ai-usage-directory')
    overlap_inc = need_row(overlap_run.stdout, 'hypr.root.include_graph',
                           'control-ai-usage-directory')
    overlap_members = non_regular_members(overlap_src)

    missing_tree = build('control-direct-missing')
    (missing_tree / '.local' / 'share' / 'omarchy' / 'default' / 'hypr'
     / 'windows.conf').unlink()
    missing_run = gate_run(missing_tree, 'control-direct-missing')
    missing_src = need_row(missing_run.stdout, 'hypr.root.sources_resolve',
                           'control-direct-missing')
    missing_inv = need_row(missing_run.stdout, 'hypr.local.inventory',
                           'control-direct-missing')
    missing_inc = need_row(missing_run.stdout, 'hypr.root.include_graph',
                           'control-direct-missing')
    missing_tog = need_row(missing_run.stdout, 'hypr.toggle.no_gaps',
                           'control-direct-missing')

    zero_tree = build('control-zero-match-glob')
    (zero_tree / TOGGLES / 'window-no-gaps.conf').unlink()
    zero_run = gate_run(zero_tree, 'control-zero-match-glob')
    zero_src = need_row(zero_run.stdout, 'hypr.root.sources_resolve',
                        'control-zero-match-glob')
    zero_inv = need_row(zero_run.stdout, 'hypr.local.inventory',
                        'control-zero-match-glob')
    zero_inc = need_row(zero_run.stdout, 'hypr.root.include_graph',
                        'control-zero-match-glob')
    zero_tog = need_row(zero_run.stdout, 'hypr.toggle.no_gaps',
                        'control-zero-match-glob')

controls = {
    'clean': {
        'overall_exit': clean_run.returncode,
        'sources_resolve': clean_src,
        'include_graph': clean_inc,
        'exact_set_pass': (clean_run.returncode == 0
                           and row_status(clean_src) == 'PASS'),
    },
    'order_swap': {
        'overall_exit': swap_run.returncode,
        'sources_resolve': swap_src,
        'include_graph': swap_inc,
        'order_detected': (swap_run.returncode == 1
                           and row_status(swap_inc) == 'FAIL'
                           and 'line ' in swap_inc),
        'set_retained': (row_status(swap_src) == 'PASS'
                         and 'non-regular:' not in swap_src),
    },
    'symlink_to_regular': {
        'overall_exit': link_run.returncode,
        'sources_resolve': link_src,
        'include_graph': link_inc,
        'regular_target_retained': (link_run.returncode == 0
                                    and row_status(link_src) == 'PASS'
                                    and 'non-regular:' not in link_src),
    },
    'newline_regular': {
        'filename': newline_name,
        'overall_exit': newline_run.returncode,
        'sources_resolve': newline_src,
        'include_graph': newline_inc,
        'regular_member_transported': (newline_run.returncode == 0
                                       and row_status(newline_src) == 'PASS'
                                       and 'non-regular:' not in newline_src),
    },
    'ai_usage_directory_overlap': {
        'overall_exit': overlap_run.returncode,
        'sources_resolve': overlap_src,
        'local_inventory': overlap_inv,
        'include_graph': overlap_inc,
        'owning_row_names_path': (overlap_members
                                  == ['~/.config/hypr/ai-usage.conf']),
        'local_inventory_also_names': 'ai-usage.conf' in overlap_inv,
    },
    'direct_missing': {
        'overall_exit': missing_run.returncode,
        'sources_resolve': missing_src,
        'local_inventory': missing_inv,
        'include_graph': missing_inc,
        'toggle_no_gaps': missing_tog,
        'unresolved_class_retained': (
            missing_run.returncode == 1
            and 'unresolved:' in missing_src
            and 'non-regular:' not in missing_src
            and 'windows.conf' in missing_src),
    },
    'zero_match_glob': {
        'overall_exit': zero_run.returncode,
        'sources_resolve': zero_src,
        'local_inventory': zero_inv,
        'include_graph': zero_inc,
        'toggle_no_gaps': zero_tog,
        'unresolved_class_retained': (
            zero_run.returncode == 1
            and 'unresolved:' in zero_src
            and 'non-regular:' not in zero_src
            and '*.conf' in zero_src),
    },
}

result = {
    'revision': rev,
    'revision_sha': rev_sha,
    'measure_inputs': {
        'gate': 'tools/mado-verify.sh',
        'gate_sha256': gate_sha,
        'fixture_root': 'private TemporaryDirectory; --root <fixture> --no-live',
    },
    'source_registry': {
        'rows': len(registry),
        'tiers': {tier: sum(r[4] == tier for r in registry.values())
                  for tier in ('A', 'B', 'C')},
        'statuses': {status: sum(r[8] == status for r in registry.values())
                     for status in ('mined', 'queued', 'rejected')},
        'round14_reserved': {
            sid: {
                'present': sid in registry,
                'status': registry[sid][8] if sid in registry else None,
                'tier': registry[sid][4] if sid in registry else None,
            }
            for sid in ('S047', 'S048')
        },
    },
    'coverage': {
        'items': sorted(covered),
        'count': len(covered),
        'score': round(10 * len(covered) / 7, 4),
        'joins': joined,
        'u4_facets': u4_facets,
        'u5_candidates': u5_candidates,
    },
    'navigation': nav,
    'exact_set': {
        'cases': cases,
        'overall_failing_runs': sum(c['overall_exit'] == 1 for c in cases),
        'detected': scored_detected,
        'total': scored_total,
        'score': round(10 * scored_detected / scored_total, 4),
    },
    'controls': controls,
}
print(json.dumps(result, indent=2))
# A low coverage or 0/3 operability count is a measured result, not a failure
# of the measuring command.
sys.exit(0)
