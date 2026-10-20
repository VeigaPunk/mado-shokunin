#!/usr/bin/env python3
"""pipe-rc-census — census of piped command substitutions in tools/*.sh.

For a given git revision, read every tools/*.sh blob with `git show REV:path`
(read-only, producer return code checked) and report each command substitution
that ASSIGNS its result and pipes a producer into sha256sum/wc/cut — together
with whether the producer's failure status is captured.

A site is `checked` only when one of these is statically present:

  pipestatus          PIPESTATUS is read in the substitution or on the line
                      that consumes it.
  pipefail-*          `set -o pipefail` is in effect at the site and the
                      body does not end in `|| true`/`|| :`.  The suffix names
                      what additionally consumes the status: `errexit`,
                      `condition`, `short-circuit`, `pipeline-fallback`,
                      `status-var`, or `scope` when nothing does (the contract
                      counts pipefail in scope; `scope` is the weak case and
                      is printed so a reader can tell it apart).
  precondition-guard  the producer is a bare file reader (sha256sum/wc/cat/
                      head) whose operand is proven a regular/readable file by
                      a `[ -f OPERAND ]`/`[ -r OPERAND ]` test in the same
                      command or the enclosing if/elif branch, and the branch
                      also proves the tool present (`have TOOL`).  This is the
                      weaker "prior status check": the branch that runs the
                      site cannot have the producer fail on its input.

Everything else is `unchecked`: the pipeline's exit status is the last stage's
and the producer's failure is discarded, so a failed read silently becomes
whatever the sink emits for empty input (e.g. sha256sum's e3b0c442… digest).

Usage:
    python3 -I pipe-rc-census.py [--repo DIR] REV

Exit: 0 no unchecked site, 1 at least one unchecked site, 2 usage/read error.
Output: `SITE <path>:<line> unchecked|checked`, then a SUMMARY line.
"""

import os
import re
import shlex
import subprocess
import sys

SINKS = ("sha256sum", "wc", "cut")
FILE_READERS = ("sha256sum", "wc", "cat", "head")
WRAPPERS = ("xargs", "env", "command", "sudo", "nice", "timeout", "tmo", "stdbuf")

# A heredoc operator with an optional `-` and an optional quoted delimiter.
HEREDOC_RE = re.compile(r'<<(-?)[ \t]*(["\']?)([A-Za-z_][A-Za-z0-9_.-]*)\2')
WORD_AT = re.compile(r'[A-Za-z0-9_./+-]+')

# Assignment target immediately left of `$(` (allowing a closing quote and the
# usual `NAME=` / `NAME+=` / `NAME[IDX]=` shapes).
ASSIGN_RE = re.compile(r'(?<![A-Za-z0-9_.-])([A-Za-z_][A-Za-z0-9_]*(?:\[[^\]\n]*\])?\+?)=\Z')

# A pipeline stage whose command word is a sink, after stripping VAR=value
# prefixes and the wrapper words this repository uses (`timeout N CMD`,
# `xargs [-0] CMD`, `tmo CMD`).
_VAR_PREFIX = r'[A-Za-z_][A-Za-z0-9_]*=(?:"[^"]*"|\'[^\']*\'|[^\s;|]*)'
_STAGE_PREFIX = (
    r'(?:!\s+|' + _VAR_PREFIX + r'\s+)*'
    r'(?:(?:timeout\s+\S+|xargs(?:\s+-\S+)*|env|command|sudo|nice|stdbuf|tmo)\s+)*'
)
SINK_STAGE_RE = re.compile(r'^\s*' + _STAGE_PREFIX + r'(sha256sum|wc|cut)(?=$|\s)')
READER_STAGE_RE = re.compile(r'^\s*' + _STAGE_PREFIX + r'(sha256sum|wc|cat|head)(?=$|\s)')


def _skip_squote(text, j):
    """j at an opening single quote; return index just past the closing one."""
    j += 1
    while j < len(text):
        if text[j] == "'":
            return j + 1
        j += 1
    return len(text)


def _skip_comment(text, j):
    """j at '#' that starts a comment; return index of the newline."""
    eol = text.find('\n', j)
    return len(text) if eol < 0 else eol


def _at_word_start(text, j):
    if j == 0:
        return True
    return text[j - 1] in ' \t\n;|&('


def _skip_heredoc(text, j, match):
    """j just past the `<<DELIM` token; return index of the closing line end."""
    strip_tabs = match.group(1) == '-'
    delim = match.group(3)
    nl = text.find('\n', j)
    if nl < 0:
        return len(text)
    i = nl + 1
    while i <= len(text):
        eol = text.find('\n', i)
        line_end = len(text) if eol < 0 else eol
        line = text[i:line_end]
        cand = line.lstrip('\t') if strip_tabs else line
        if cand == delim:
            return line_end
        if eol < 0:
            break
        i = eol + 1
    return len(text)


def _match_sub(text, i):
    """text[i:i+2] == '$(', return the index of the matching ')' or -1."""
    j = i + 2
    depth = 1
    in_dq = False
    case_depth = 0
    while j < len(text):
        c = text[j]
        if c == '\\':
            j += 2
            continue
        if in_dq:
            if c == '"':
                in_dq = False
                j += 1
            elif text.startswith('$(', j):
                end = _match_sub(text, j)
                j = (end + 1) if end >= 0 else len(text)
            else:
                j += 1
            continue
        if c == "'":
            j = _skip_squote(text, j)
            continue
        if c == '"':
            in_dq = True
            j += 1
            continue
        if c == '#' and _at_word_start(text, j):
            j = _skip_comment(text, j)
            continue
        if text.startswith('<<', j) and not text.startswith('<<<', j):
            m = HEREDOC_RE.match(text, j)
            if m:
                j = _skip_heredoc(text, j + len(m.group(0)), m)
                continue
        if re.match(r'case(?![A-Za-z0-9_])', text[j:j + 5]):
            case_depth += 1
            j += 4
            continue
        if re.match(r'esac(?![A-Za-z0-9_])', text[j:j + 5]):
            if case_depth > 0:
                case_depth -= 1
            j += 4
            continue
        if c == '(':
            depth += 1
            j += 1
            continue
        if c == ')':
            if case_depth > 0:
                j += 1
                continue
            depth -= 1
            if depth == 0:
                return j
            j += 1
            continue
        j += 1
    return -1


def _assignment_target(text, i):
    """If the substitution at i is assigned, return the variable name.

    `x=$(...)` and `x="$(...)"` are assignments; `"count=$(...)"` is a quoted
    argument whose literal text merely looks like one, so a target whose name
    is preceded by an opening quote is rejected.
    """
    k = i
    if k > 0 and text[k - 1] == '"':
        k -= 1
    if k > 0 and text[k - 1] == '=':
        m = ASSIGN_RE.search(text, max(0, k - 240), k)
        if m and (m.start(1) == 0 or text[m.start(1) - 1] != '"'):
            return m.group(1)
    return None


def _spans_in_code(text):
    """Yield (start, end) of `$(...)` occurrences in shell code (not heredocs
    and not single-quoted text); double-quoted substitutions included."""
    i = 0
    n = len(text)
    in_dq = False
    while i < n:
        c = text[i]
        if c == '\\':
            i += 2
            continue
        if in_dq:
            if c == '"':
                in_dq = False
                i += 1
            elif text.startswith('$(', i):
                end = _match_sub(text, i)
                if end < 0:
                    i += 2
                    continue
                yield i, end
                i = end + 1
            else:
                i += 1
            continue
        if c == "'":
            i = _skip_squote(text, i)
            continue
        if c == '"':
            in_dq = True
            i += 1
            continue
        if c == '#' and _at_word_start(text, i):
            i = _skip_comment(text, i)
            continue
        if text.startswith('<<', i) and not text.startswith('<<<', i):
            m = HEREDOC_RE.match(text, i)
            if m:
                i = _skip_heredoc(text, i + len(m.group(0)), m)
                continue
        if text.startswith('$(', i):
            end = _match_sub(text, i)
            if end < 0:
                i += 2
                continue
            yield i, end
            i = end + 1
            continue
        i += 1


def _split_stages(body):
    """Split a substitution body on top-level single `|`."""
    stages = []
    last = 0
    j = 0
    in_dq = False
    while j < len(body):
        c = body[j]
        if c == '\\':
            j += 2
            continue
        if in_dq:
            if c == '"':
                in_dq = False
                j += 1
            elif body.startswith('$(', j):
                end = _match_sub(body, j)
                j = end + 1 if end >= 0 else len(body)
            else:
                j += 1
            continue
        if c == "'":
            j = _skip_squote(body, j)
            continue
        if c == '"':
            in_dq = True
            j += 1
            continue
        if c == '#' and _at_word_start(body, j):
            j = _skip_comment(body, j)
            continue
        if body.startswith('<<', j) and not body.startswith('<<<', j):
            m = HEREDOC_RE.match(body, j)
            if m:
                j = _skip_heredoc(body, j + len(m.group(0)), m)
                continue
        if body.startswith('$(', j):
            end = _match_sub(body, j)
            j = end + 1 if end >= 0 else len(body)
            continue
        if c == '|' and not body.startswith('||', j):
            stages.append(body[last:j])
            last = j + 1
            j += 1
            continue
        j += 1
    stages.append(body[last:])
    return stages


def _set_effect(body):
    """Parse a `set ...` argument list; return (pipefail, errexit) changes."""
    try:
        toks = shlex.split(body)
    except ValueError:
        toks = []
    pipefail = None
    errexit = None
    i = 0
    while i < len(toks):
        t = toks[i]
        if t in ('-o', '+o'):
            val = toks[i + 1] if i + 1 < len(toks) else ''
            if val == 'pipefail':
                pipefail = t == '-o'
            i += 2
            continue
        if re.fullmatch(r'[-+][A-Za-z]+', t):
            sign = t[0]
            letters = t[1:]
            val = ''
            if 'o' in letters:
                val = toks[i + 1] if i + 1 < len(toks) else ''
                i += 1
            for ch in letters:
                if ch == 'e':
                    errexit = sign == '-'
                elif ch == 'o' and val == 'pipefail':
                    pipefail = sign == '-'
        i += 1
    return pipefail, errexit


def _flags_at(text, pos):
    """(pipefail, errexit) in effect at offset pos."""
    pipefail = False
    errexit = False
    for m in re.finditer(r'(?m)(?:^[ \t]*|[;&]\s*|\b(?:then|do|else)\s+)(set[ \t]+[^\n;]+)', text):
        if m.start() >= pos:
            break
        pf, er = _set_effect(m.group(1)[3:].strip())
        if pf is not None:
            pipefail = pf
        if er is not None:
            errexit = er
    return pipefail, errexit


def _swallowed(body):
    """True if the substitution body ends with `|| true` / `|| :` (status
    deliberately discarded even when pipefail is in scope)."""
    last = None
    for last in re.finditer(r'\|\|', body):
        pass
    if last is None:
        return False
    return body[last.end():].strip() in ('true', ':', 'exit 0')


def _status_consumed(text, start, close, body):
    """Whether the substitution's exit status is acted upon (whole pipeline)."""
    line_start = text.rfind('\n', 0, start) + 1
    prefix = text[line_start:start]
    conditional = bool(re.match(r'^\s*(?:if|elif|while|until)\b', prefix))
    if not conditional:
        conditional = bool(re.search(r'(?:^|[;&]\s*)(?:if|elif|while|until)\s+', prefix))
    if conditional:
        return 'condition'
    after = text[close + 1:close + 80]
    if re.match(r'\s*(?:\|\||&&)', after):
        return 'short-circuit'
    if '||' in body or '&&' in body:
        tail = body[body.rfind('||') + 2:].strip() if '||' in body else ''
        if re.search(r'\|\|', body) and tail not in ('true', ':', 'exit 0'):
            return 'pipeline-fallback'
    m = re.search(r'(?:^|[;\n])\s*([A-Za-z_][A-Za-z0-9_]*)=\$\?', text[close + 1:close + 200])
    if m:
        name = m.group(1)
        window = text[close:close + 800]
        if re.search(r'["\s]\$\{?' + re.escape(name) + r'\b', window):
            return 'status-var'
    return None


def _producer_operand(stage):
    """First non-option operand token of a stage, raw (quotes kept)."""
    toks = re.findall(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|\S+', stage)
    seen = 0
    for t in toks:
        if seen == 0:
            seen = 1
            continue
        if t.startswith('-') and t != '-':
            continue
        if re.fullmatch(r'[0-9]+[a-z]?', t) and t.endswith('s'):
            continue
        return t
    return ''


def _guard_checked(text, start, stage0, word0):
    """The weaker 'prior status check': branch proves the producer's operand."""
    operand = _producer_operand(stage0)
    if not operand or '$' not in operand:
        return False
    line_start = text.rfind('\n', 0, start) + 1
    region_start = line_start
    lines_back = 0
    while region_start > 0 and lines_back < 12:
        prev = text.rfind('\n', 0, region_start - 1)
        chunk = text[prev + 1:region_start]
        region_start = prev + 1 if prev >= 0 else 0
        lines_back += 1
        if re.match(r'^\s*(?:if|fi)\b', chunk):
            break
    region = text[region_start:start]
    guarded = re.search(r'\[\s*!?\s*-[fr]\s+' + re.escape(operand) + r'\s*\]', region)
    have = re.search(r'\bhave\s+' + re.escape(word0) + r'\b', region)
    return bool(guarded and have)


def classify(text, start, close, body, stages):
    sinks = [m.group(1) for m in
             (SINK_STAGE_RE.match(s) for s in stages[1:]) if m]
    if not sinks:
        return None
    pipefail, errexit = _flags_at(text, start)
    if re.search(r'PIPESTATUS', body) or re.search(r'PIPESTATUS', text[close + 1:close + 120]):
        return ('checked', 'pipestatus')
    if pipefail and not _swallowed(body):
        if errexit:
            return ('checked', 'pipefail-errexit')
        consumed = _status_consumed(text, start, close, body)
        return ('checked', 'pipefail-' + (consumed or 'scope'))
    m0 = READER_STAGE_RE.match(stages[0])
    if m0 and _guard_checked(text, start, stages[0], m0.group(1)):
        return ('checked', 'precondition-guard')
    return ('unchecked', 'producer-status-dropped; sinks=' + ','.join(sinks))


def scan_text(path, text):
    sites = []
    for start, close in _spans_in_code(text):
        if _assignment_target(text, start) is None:
            continue
        body = text[start + 2:close]
        stages = _split_stages(body)
        if len(stages) < 2:
            continue
        verdict = classify(text, start, close, body, stages)
        if verdict is None:
            continue
        line = text.count('\n', 0, start) + 1
        sites.append((line, verdict[0], verdict[1]))
    return sites


def _git(repo, *args):
    proc = subprocess.run(['git', '-C', repo] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def main(argv):
    usage = 'usage: pipe-rc-census.py [--repo DIR] REV\n'
    repo = os.getcwd()
    args = list(argv[1:])
    rev = None
    while args:
        a = args.pop(0)
        if a == '--repo':
            if not args:
                sys.stderr.write(usage)
                return 2
            repo = args.pop(0)
        elif a in ('-h', '--help'):
            sys.stderr.write(usage)
            return 2
        elif a.startswith('-'):
            sys.stderr.write(usage)
            return 2
        elif rev is None:
            rev = a
        else:
            sys.stderr.write(usage)
            return 2
    if rev is None:
        sys.stderr.write(usage)
        return 2

    rc, out, err = _git(repo, 'rev-parse', '--verify', '--quiet', rev + '^{commit}')
    if rc != 0:
        sys.stderr.write('pipe-rc-census: not a revision in %s: %s\n' % (repo, rev))
        return 2
    commit = out.decode('utf-8', 'replace').strip()

    rc, out, err = _git(repo, 'ls-tree', '-r', '--name-only', rev, '--', 'tools')
    if rc != 0:
        sys.stderr.write('pipe-rc-census: git ls-tree failed: %s\n'
                         % err.decode('utf-8', 'replace').strip())
        return 2
    paths = sorted(p for p in out.decode('utf-8', 'surrogateescape').splitlines()
                   if re.fullmatch(r'tools/[^/]+\.sh', p))

    total = checked = unchecked = 0
    for path in paths:
        rc, blob, err = _git(repo, 'show', '%s:%s' % (rev, path))
        if rc != 0:
            sys.stderr.write('pipe-rc-census: cannot read %s at %s: %s\n'
                             % (path, rev, err.decode('utf-8', 'replace').strip()))
            return 2
        text = blob.decode('utf-8', 'surrogateescape')
        for line, verdict, reason in scan_text(path, text):
            total += 1
            if verdict == 'checked':
                checked += 1
            else:
                unchecked += 1
            print('SITE %s:%d %s  # %s' % (path, line, verdict, reason))

    print('SUMMARY rev=%s commit=%s files=%d sites=%d checked=%d unchecked=%d'
          % (rev, commit, len(paths), total, checked, unchecked))
    print('VERDICT %s' % ('RED' if unchecked else 'GREEN'))
    return 1 if unchecked else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
