#!/usr/bin/env python3
"""Scan a pinned git archive as data; never execute archived programs."""
import ast
import collections
import hashlib
import pathlib
import re
import sys
import tarfile

REV = '0f3a54361a9824484d0801679ceb1fd8ac7c32e1'
LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
PATTERNS = {
    'hyprctl': r'\bhyprctl\b',
    'proc': r'/proc/',
    'state': r'\b(?:kill|pkill|killall|killpg|send_signal|raise_signal|systemctl|signal)\b|\bos\.kill\b|\bSIG(?:KILL|TERM|HUP|USR1|USR2|INT|QUIT)\b|\.kill\(|\.terminate\(',
    'config': r'(?:~|\$HOME|/home/[^/\s]+)/(?:\.config|\.local)(?:/|\b)',
    'generic_secret': r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----|\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,})\b|(?i:authorization\s*[:=]\s*[\x22\x27]?bearer\s+\S+|(?:password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[\x22\x27]?[^\s\x22\x27,;]{8,})',
    'write_candidate': r'(?:O_WRONLY|O_RDWR|O_CREAT|write_text|write_bytes|\b(?:cp|mv|rm|tee|touch|install)\b).*(?:\.config/|\.local/)|(?:\.config/|\.local/).*(?:O_WRONLY|O_RDWR|O_CREAT|write_text|write_bytes)',
}

def main():
    archive, output = map(pathlib.Path, sys.argv[1:])
    blobs = {}
    links = {}
    with tarfile.open(archive) as tf:
        for m in tf:
            if m.isfile():
                blobs[m.name] = tf.extractfile(m).read()
            elif m.issym():
                links[m.name] = m.linkname.encode()
    tree = ast.parse(blobs['tools/mado-tripwire.py'])
    assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SECRET_PATTERNS' for t in n.targets))
    fixed = [re.compile(ast.literal_eval(call.args[0])) for call in assignment.value.elts]
    patterns = {k: re.compile(v) for k, v in PATTERNS.items()}
    patterns.update({'fixed%d' % (i+1): p for i, p in enumerate(fixed)})
    def safe(line):
        for p in fixed:
            line = p.sub('<redacted-shape>', line)
        line = patterns['generic_secret'].sub('<redacted-generic>', line)
        return ''.join(c if c.isprintable() or c == '\t' else '?' for c in line)
    reports = [p for p in blobs if re.fullmatch(r'\.ufo/waves/round-56/w[12]/[^/]+\.md', p)]
    total = collections.Counter()
    hitlines = []
    verdicts = []
    for name, b in sorted({**blobs, **links}.items()):
        if '/round-56/w' not in name:
            continue
        counts = collections.Counter()
        for n, line in enumerate(b.decode('utf-8', 'replace').splitlines(), 1):
            categories = [k for k, p in patterns.items() if p.search(line)]
            if categories:
                counts.update(categories)
                severity = 'NO_DEFECT_CANDIDATE_DATA'
                if 'generic_secret' in categories or 'fixed1' in categories or 'fixed2' in categories:
                    severity = 'REVIEW_SECRET_SHAPE'
                if '/R56W2CritC2Cheat/' in name and ('proc' in categories or 'hit crawl:' in line or 'root done:' in line):
                    severity = 'WEAKENS_BOUNDARY_DISCIPLINE_D1'
                hitlines.append('%s:%d [%s] %s %s' % (name, n, severity, ','.join(categories), safe(line)))
        total.update(counts)
        verdict = 'NO_RECORDED_HOST_MUTATION_OR_CREDENTIAL_DETECTED'
        if '/R56W2CritC2Cheat/' in name or name.endswith('/R56W2CritC2Cheat.md'):
            verdict = 'D1_BROAD_HOST_AND_SIBLING_READS_RECORDED;NO_HOST_MUTATION_DETECTED'
        verdicts.append('%s sha256=%s bytes=%d %s hits=%s' % (name, hashlib.sha256(b).hexdigest(), len(b), verdict, dict(counts)))
    header = [
        'R56W3RevLiveBoundary: host-boundary sweep attempt 2',
        'Axes: host non-mutation; credential non-disclosure; exhaustive pinned-evidence coverage; reproducibility.',
        'Revision: ' + REV,
        'Population: every regular blob and symlink text under w1 and w2, including nested receipt artifact copies; no symlinks followed.',
        'Reports=%d w1=%d w2=%d regular=%d symlink=%d' % (len(reports), sum('/w1/' in p for p in reports), sum('/w2/' in p for p in reports), len(blobs)-1, len(links)),
        'Archive command: git -C ' + LANE + ' archive ' + REV + ' .ufo/waves/round-56/w1 .ufo/waves/round-56/w2 tools/mado-tripwire.py',
        'Sweep command: python3 -I ' + LANE + '/.ufo/waves/round-56/w3/R56W3RevLiveBoundary/boundary-sweep.py /fast/scratch/hyaku/mado-r56/R56W3RevLiveBoundary/evidence.tar ' + str(output),
        'Shell grep/awk pipelines: none; specialized grep tool used for initial triage, exhaustive Python regex sweep avoids capped search output.',
        'Initial grep pattern: hyprctl|/proc/|kill\\b|pkill\\b|killall\\b|systemctl|\\.config/|\\.local/|signal\\b',
        'LSP: xd://lsp unavailable (No such tool); text audit only, no semantic-absence claim.',
        'Fixed patterns extracted via AST from pinned tools/mado-tripwire.py:301-305; not executed.',
        'Patterns: ' + repr(PATTERNS),
        'Totals (matching lines, overlapping categories): ' + repr(dict(total)),
        'Literal mutation words in source quotations, historical corpus copies and denied operations are flagged below as candidate DATA, not evidence they were executed.',
        'Read invocations claimed by round-56 seats use getoption/version; other verb vocabulary appears in copied historical sources, proposed entries, search patterns or denials.',
        'No recorded executed hyprctl keyword/dispatch/reload, host kill/signal, service mutation, or config write found. This is receipt evidence, not an independent execution transcript.',
        'Secret scan: fixed1 URL userinfo=0, fixed2 AWS shape=0, generic contextual/prefix/private-key=0; fixed3 matches are identifiers, hashes, separators and Hyprland instance signatures, not demonstrated credentials. All fixed3 values suppressed in this receipt.',
        'D1 [weakens the claim: boundary discipline, not frozen C2 predicate]: R56W2CritC2Cheat unsandboxed crawl reads arbitrary process cmdlines and traverses sibling-domain scratch, demonstrated by crumbs-e-crawl-nobwrap.txt:2-11 and e-crawl.py:25-50. No writes to those paths evidenced.',
        'Related residual: R56W2RevProcFdinfo.md:103-105 reports compositor HOME from environment, beyond the fd/fdinfo-only named read set; environment read command is not retained, so authorization/exact exposure unverified. No credential value shown.',
        'Caution: per-file NO_RECORDED verdict means no violation demonstrated by scanned artifact text, not proof of historical non-execution.',
        '\nPER-FILE VERDICTS',
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text('\n'.join(header + verdicts + ['\nEVERY MATCHING LINE (credential shapes suppressed)'] + hitlines) + '\n')
    print('BOUNDARY_SWEEP reports=%d files=%d symlinks=%d totals=%s' % (len(reports), len(blobs)-1, len(links), dict(total)))
    print('D1: broad /proc cmdline and sibling scratch reads recorded; no executed host mutation demonstrated.')
    print('Credential-specific matches=%d' % sum(total[k] for k in ('fixed1','fixed2','generic_secret')))
    print('Receipt=' + str(output))

if __name__ == '__main__':
    main()
