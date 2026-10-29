# Independent interpreter for registration.md section C2 (written from the contract text only).
import glob
import json
import os
import re
import stat
import sys

WS = ' \t\r\n\x0b\x0c'
MAX_DEPTH = 16
MASK_DIR = 'IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM'
MASK_FILE = 'IN_CLOSE_WRITE|IN_DONT_FOLLOW'
MASK_CANON = 'IN_CLOSE_WRITE'

st = {'events': [], 'paths': [], 'unsupported': 0, 'errors': 0, 'last': None}
opts = {}


def display(p):
    for root in opts['roots']:
        if p == root or p.startswith(root + '/'):
            return '$ROOT' + p[len(root):]
    return p


def absolute_path(raw, cur):
    if raw[0] == '~':
        return opts['home'] + raw[1:]
    if raw[0] == '/':
        return raw
    curdir = cur[:cur.rfind('/')] if '/' in cur else cur
    if raw[0] == '.':
        if raw.startswith('../'):
            parent = curdir[:curdir.rfind('/')] if '/' in curdir else curdir
            return parent + raw[2:]
        if raw.startswith('./'):
            return curdir + raw[1:]
    return curdir + '/' + raw


def handle_source(raw, cur, lineno, depth):
    via = display(cur) + ':' + str(lineno)
    if len(raw) < 2:
        st['events'].append(f'MADO_WATCH: ERROR via={via} source={raw} reason=bogus')
        st['errors'] += 1
        return
    if (raw[0] == '~' and opts['home'] is None) or '\\' in raw:
        st['unsupported'] += 1
        return
    value = absolute_path(raw, cur)
    matches = sorted(glob.glob(value))
    if not matches:
        st['events'].append(f'MADO_WATCH: ERROR via={via} source={raw} reason=nomatch')
        st['errors'] += 1
        return
    for m in matches:
        v = absolute_path(m, cur)
        try:
            s = os.stat(v)
        except OSError:
            st['events'].append(f'MADO_WATCH: ERROR via={via} source={raw} reason=inaccessible')
            st['errors'] += 1
            break
        if stat.S_ISREG(s.st_mode):
            st['paths'].append((v, via))
            if depth + 1 > MAX_DEPTH:
                st['unsupported'] += 1
            else:
                parse(v, depth + 1)
        elif stat.S_ISDIR(s.st_mode):
            st['events'].append(f'MADO_WATCH: SKIP via={via} path={display(v)} reason=directory')
        else:
            st['events'].append(f'MADO_WATCH: SKIP via={via} path={display(v)} reason=nonregular')


def parse(path, depth):
    with open(path, 'rb') as fh:
        text = fh.read().decode('utf-8', errors='replace')
    stack = []
    for lineno, raw in enumerate(text.split('\n'), 1):
        s = raw.strip(WS)
        if s == '' or s[0] == '#':
            continue
        if '=' not in s:
            if s == '}':
                if stack:
                    stack.pop()
            elif s.endswith('{'):
                stack.append(s[:-1].strip(WS))
            continue
        lhs, _, rhs = s.partition('=')
        lhs = lhs.strip(WS)
        rhs = rhs.strip(WS)
        if lhs == 'source':
            if stack:
                st['unsupported'] += 1
                continue
            handle_source(rhs.split('#', 1)[0].strip(WS), path, lineno, depth)
            continue
        if lhs.startswith('$'):
            continue
        key = ':'.join(stack + [lhs]) if stack else lhs
        if key != 'misc:disable_autoreload':
            continue
        if any(c in s for c in '${\\'):
            st['unsupported'] += 1
            continue
        if '##' in rhs:
            st['unsupported'] += 1
            continue
        value = rhs.split('#', 1)[0].strip(WS)
        if value.startswith(('true', 'on', 'yes')):
            v = 1
        elif value.startswith(('false', 'off', 'no')):
            v = 0
        elif re.fullmatch(r'[0-9]+', value):
            v = int(value)
        else:
            st['unsupported'] += 1
            continue
        st['last'] = v


def main(argv):
    given = {}
    i = 0
    while i < len(argv):
        t = argv[i]
        if t not in ('--config', '--home', '--display-root', '--getoption'):
            raise SystemExit(2)
        given[t] = argv[i + 1]
        i += 2
    config = given['--config']
    home = given.get('--home')
    droot = given.get('--display-root')
    roots = []
    if droot is not None:
        base = droot.rstrip('/')
        for c in (base, os.path.realpath(droot)):
            if c not in roots:
                roots.append(c)
    opts['roots'] = roots
    opts['home'] = home

    st['paths'].append((config, 'main'))
    try:
        if stat.S_ISREG(os.stat(config).st_mode):
            parse(config, 0)
    except OSError:
        pass

    if st['last'] is not None and st['last'] != 0:
        watches = []
        autoreload = 'off'
    else:
        watches = []
        autoreload = 'on'
        for p, via in st['paths']:
            if os.path.isdir(p):
                watches.append(('primary', p, 'dir', MASK_DIR, via))
            elif os.path.lexists(p):
                watches.append(('primary', p, 'file', MASK_FILE, via))
            else:
                watches.append(('primary', p, 'missing', MASK_FILE, via))
            if os.path.islink(p):
                try:
                    rp = os.path.realpath(p, strict=True)
                except OSError:
                    rp = None
                if rp is not None:
                    watches.append(('canonical', rp, 'file', MASK_CANON, via))
    dis = 'unset' if st['last'] is None else str(st['last'])
    out = [f"MADO_WATCH: config={display(config)} autoreload={autoreload} disable_autoreload={dis} "
           f"paths={len(st['paths'])} unsupported={st['unsupported']} errors={st['errors']}"]
    out += st['events']
    for k, (role, p, t, mask, via) in enumerate(watches, 1):
        out.append(f'MADO_WATCH: n={k} role={role} path={display(p)} type={t} mask={mask} via={via}')
    out.append(f"MADO_WATCH: DONE watches={len(watches)} unsupported={st['unsupported']} "
               f"errors={st['errors']} live=NONE")
    sys.stdout.write('\n'.join(out) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
