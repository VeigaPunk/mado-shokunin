#!/usr/bin/env python3
"""check83 - a citation resolves at the revision the citing document is read at.

QUALITY criterion 83 (draft, round 44). Every repository path a document cites must exist in
the tree of the revision the document is judged at. A path that resolves only in a later commit
is `LATE`: the claim was admitted before its evidence was in the tree. A path removed before the
citing revision is `EARLIER`; a repository path no ref holds is `NOWHERE`. A bare name with no
directory is resolved by basename and, when no ref holds that name at all, reported `OUTSIDE`
(informational: package and upstream names are not the lane's citations).

Only backticked tokens are read: a citation the document formats as code. Resolution order:
repo-root prefixes as written; otherwise a token with a `/` relative to the document's own
directory; otherwise a unique-or-any basename in the revision's tree.

Usage:
  check83.py --repo . --rev <REV> --doc <PATH-IN-REPO> [--text --doc-file PATH]
             [--prefix .ufo/]
Exit 0 = PASS, 1 = violation, 2 = the document is not readable at --rev.
"""
import argparse
import re
import subprocess
import sys

EXT = (r'(?:jsonl|service|json|toml|yaml|conf|xml|jsonc|md|txt|log|py|sh|cpp|hpp|rs|c|h)')
TOKEN = re.compile(r'([A-Za-z0-9_.~/-]+\.%s)(?::\d+(?:-\d+)?)?' % EXT)
ROOTED = ('.ufo/', 'corpus/', 'quality/', 'tools/', 'considerthese/', 'templates/',
          'scripts/', 'SKILL.md', 'PROVINCE.md', 'LOG.md', 'SCORECARD.md', 'README.md',
          'CORPUS.md', 'MINT.md', 'MANIFEST.json')
BACKTICK = re.compile(r'`([^`\n]+)`')


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, text=True)


def adding_commit(repo, path):
    out = git(repo, 'log', '--all', '--diff-filter=A', '--format=%H', '--', path).stdout.split()
    return out[-1] if out else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--doc')
    ap.add_argument('--doc-file')
    ap.add_argument('--text', action='store_true')
    ap.add_argument('--prefix', default='')
    a = ap.parse_args()

    if a.text:
        try:
            body = open(a.doc_file, encoding='utf-8', errors='replace').read()
        except OSError as exc:
            print('SETUP_ERROR %s' % exc)
            return 2
        docdir = ''
        name = a.doc_file
    else:
        if not a.doc:
            print('SETUP_ERROR one of --doc or --doc-file is required')
            return 2
        r = git(a.repo, 'show', '%s:%s' % (a.rev, a.doc))
        if r.returncode:
            print('MISSING-DOC %s at %s' % (a.doc, a.rev))
            return 2
        body = r.stdout
        docdir = a.doc.rsplit('/', 1)[0] + '/' if '/' in a.doc else ''
        name = a.doc

    tree = [p for p in git(a.repo, 'ls-tree', '-r', '--name-only', a.rev).stdout.splitlines() if p]
    by_base = {}
    for p in tree:
        by_base.setdefault(p.rsplit('/', 1)[-1], []).append(p)
    if not tree:
        print('SETUP_ERROR empty tree at %s' % a.rev[:7])
        return 2

    toks = []
    for m in BACKTICK.finditer(body):
        for t in TOKEN.findall(m.group(1)):
            if t not in toks:
                toks.append(t)

    judged = outside = 0
    bad = 0
    for tok in toks:
        if tok.startswith(('/', '~')):
            print('OUTSIDE %s (absolute: not a repository citation)' % tok)
            outside += 1
            continue
        if a.prefix and not tok.startswith(a.prefix):
            continue
        if tok.startswith(ROOTED):
            cands = [tok]
        elif '/' in tok:
            cands = [(docdir + tok) if docdir else tok]
        else:
            cands = by_base.get(tok, [])
        hits = [p for p in cands if p in tree]
        if hits:
            judged += 1
            print('OK %s -> %s' % (tok, hits[0]))
            continue
        resolved = 0
        for p in (cands or [tok]):
            parent = p.rsplit('/', 1)[0] if '/' in p else ''
            near = [q for q in tree if parent and q.startswith(parent + '/')
                    and q.rsplit('/', 1)[-1] == p.rsplit('/', 1)[-1]]
            if near:
                resolved += 1
                break
            add = adding_commit(a.repo, p)
            if add:
                resolved += 1
                anc = git(a.repo, 'merge-base', '--is-ancestor', add, a.rev).returncode == 0
                print('%s %s (added %s %s %s)'
                      % ('EARLIER' if anc else 'LATE', tok, add[:7],
                         'before' if anc else 'after', a.rev[:7]))
                break
        if resolved:
            bad += 1
            continue
        band = [q for q in tree if q.rsplit('/', 1)[-1] == tok.rsplit('/', 1)[-1]]
        if band and '/' not in tok:
            judged += 1
            print('OK %s -> %s (basename at the revision)' % (tok, band[0]))
            continue
        if '/' in tok or tok.startswith(ROOTED):
            print('NOWHERE %s (no ref of the repository holds it)' % tok)
            bad += 1
        else:
            print('OUTSIDE %s (no ref holds this name: package or upstream)' % tok)
            outside += 1

    if not judged and not bad:
        print('NO-CITATIONS %s' % name)
        return 1
    if bad:
        print('CHECK83: verdict=FAIL citations=%d violations=%d outside=%d rev=%s'
              % (judged + bad, bad, outside, a.rev[:7]))
        return 1
    print('CHECK83: verdict=PASS citations=%d violations=0 outside=%d rev=%s'
          % (judged, outside, a.rev[:7]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
