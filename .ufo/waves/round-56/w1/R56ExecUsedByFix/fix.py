#!/usr/bin/env python3
"""C3 registry fix (round 56): append missing used-by back-references.

usage: python3 -I fix.py --repo REPO --rev REV --out DIR [--sep SEP]

Reads corpus/SOURCES.md and corpus/knowledge/*.md as git blobs at REV (never the
working tree) and writes DIR/SOURCES.md, DIR/changes.tsv (id, old cell, new
cell, added paths) and DIR/old-to-new.md (the changed-row table).  Only cell 11 (used-by) of rows with missing back-references
changes: the missing entry paths, sorted, are appended to the existing cell text
(kept byte for byte) joined by SEP (default ", ": sources-census.sh splits used-by on commas, so a bare space breaks its E11 check).  Definitions follow
registration.md section C3.  Writes nothing but DIR; exit 0 ok, 2 setup error.
"""
import argparse, os, re, subprocess, sys

ID_RE = re.compile(r'^ {0,3}\|\s*S[0-9]{3,}\s*\|')
CITE_RE = re.compile(r'(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])')
UB_RE = re.compile(r'corpus/knowledge/[A-Za-z0-9_.-]+\.md')
FENCE_RE = re.compile(r'^ {0,3}(```|~~~)')
KDIR = 'corpus/knowledge/'


def die(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(2)


def git(repo, *args, raw=False):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    p = subprocess.run(['git', '-C', repo] + list(args), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, env=env)
    if p.returncode:
        die('git %s failed: %s' % (' '.join(args), p.stderr.decode('utf-8', 'replace').strip()))
    return p.stdout


def cite_set(text):
    """Citation tokens on lines outside fenced code blocks (``` / ~~~, 0-3 leading spaces)."""
    out, fence = set(), None
    for line in text.split('\n'):
        m = FENCE_RE.match(line)
        if m:
            f = m.group(1)
            if fence is None:
                fence = f
            elif fence == f:
                fence = None
            continue
        if fence is None:
            out.update(CITE_RE.findall(line))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--sep', default=', ')
    a = ap.parse_args()

    rev = git(a.repo, 'rev-parse', '--verify', a.rev + '^{commit}').decode().strip()
    tree = git(a.repo, 'ls-tree', '-r', '-z', '--full-tree', rev, '--', 'corpus/SOURCES.md', 'corpus/knowledge')
    entries, sources_ok = {}, False
    for rec in tree.split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        mode, typ, _sha = meta.decode().split()
        path = path.decode('utf-8')
        if mode not in ('100644', '100755'):
            continue
        if path == 'corpus/SOURCES.md':
            sources_ok = True
        elif path.startswith(KDIR) and path.endswith('.md') and '/' not in path[len(KDIR):]:
            entries[path] = None
    if not sources_ok:
        die('corpus/SOURCES.md not a regular blob at ' + rev)
    for p in entries:
        entries[p] = cite_set(git(a.repo, 'show', '%s:%s' % (rev, p)).decode('utf-8', 'replace'))
    src = git(a.repo, 'show', rev + ':corpus/SOURCES.md')
    text = src.decode('utf-8')
    lines = text.split('\n')

    # pass 1: rows
    rows = {}  # id -> line index
    for i, line in enumerate(lines):
        if ID_RE.match(line):
            cells = line.strip().strip('|').split('|')
            if len(cells) != 11:
                die('registry row with %d cells at line %d' % (len(cells), i + 1))
            rows[cells[0].strip()] = i
    missing = {}  # id -> set(paths)
    for path, cites in entries.items():
        for s in cites:
            if s not in rows:
                continue
            cells = lines[rows[s]].strip().strip('|').split('|')
            if path not in UB_RE.findall(cells[10]):
                missing.setdefault(s, set()).add(path)

    changes = []
    for s in sorted(missing):
        i = rows[s]
        line = lines[i]
        end = line.rstrip().rfind('|')          # closing pipe
        start = line.rfind('|', 0, end)         # pipe before cell 11
        raw = line[start + 1:end]
        core = raw.strip()
        lead = raw[:len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        add = a.sep.join(sorted(missing[s]))
        newcore = (core + a.sep + add) if core else add
        newraw = lead + newcore + trail
        lines[i] = line[:start + 1] + newraw + line[end:]
        changes.append((s, raw, newraw, sorted(missing[s])))

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, 'SOURCES.md'), 'wb') as f:
        f.write('\n'.join(lines).encode('utf-8'))
    with open(os.path.join(a.out, 'changes.tsv'), 'w', encoding='utf-8') as f:
        for s, old, new, add in changes:
            f.write('%s\t%s\t%s\t%s\n' % (s, old.strip(), new.strip(), ' '.join(add)))
    with open(os.path.join(a.out, 'old-to-new.md'), 'w', encoding='utf-8') as f:
        f.write('| id | old used-by | new used-by |\n|---|---|---|\n')
        for s, old, new, add in changes:
            f.write('| %s | %s | %s |\n' % (s, old.strip(), new.strip()))
    pairs = sum(len(c[3]) for c in changes)
    print('FIX: rev=%s entries=%d rows=%d changed_rows=%d pairs=%d' % (rev, len(entries), len(rows), len(changes), pairs))


if __name__ == '__main__':
    main()
