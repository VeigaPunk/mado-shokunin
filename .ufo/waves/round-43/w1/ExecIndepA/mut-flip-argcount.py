#!/usr/bin/env python3
"""mado-geometry.py - a read-only join of window-rule sizes and reported client sizes.

    hyprctl clients -j | mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf
    mado-geometry.py --selftest

Reads only the files named on the command line and standard input, and writes only to
standard output. Implemented from the frozen predicate text alone, standard library only.
"""

import json
import os
import re
import stat
import sys

MAX_INPUT = 1048576
STDIN_MAX = MAX_INPUT + 1
EDGE = ' \t'
SPLIT_WS = re.compile(r'[ \t]+')
RULE_LINE = re.compile(r'windowrule[ \t]*=(.*)')
CLASS_FIELD = re.compile(r'match:class[ \t]+(.+)')
SIZE_TOKEN = re.compile(r'[0-9]{1,5}')
REGEX_UNIT = re.compile(r'(?:[A-Za-z0-9_.^$()|*+?-]|\\[.\-()|*+?^$\\]){1,200}')
SHUNNED = ('(?', '*+', '++', '?+')


class Setup(Exception):
    """A setup failure: stdout is one MADO_GEOMETRY: SETUP line, exit 2."""

    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


def oversize(count):
    return count > MAX_INPUT


def parse_args(argv):
    if argv == ['--selftest']:
        return ('selftest', None, [])
    clients = None
    rules = []
    pos = 0
    total = len(argv)
    while pos < total:
        item = argv[pos]
        if item == '--clients':
            if clients is not None:
                return ('usage', None, [])
            if pos + 1 >= total:
                return ('usage', None, [])
            clients = argv[pos + 1]
            pos += 2
            continue
        if item == '--rules':
            if pos + 1 >= total:
                return ('usage', None, [])
            rules.append(argv[pos + 1])
            pos += 2
            continue
        return ('usage', None, [])
    if clients is None:
        return ('usage', None, [])
    if not rules:
        return ('usage', None, [])
    return ('run', clients, rules)


def strip_edges(text):
    return text.strip(EDGE)


def tokens_of(text):
    if text == '':
        return []
    return SPLIT_WS.split(text)


def argument_tokens(field):
    return tokens_of(field)[1:]


def read_file(spec):
    try:
        info = os.stat(spec)
    except OSError:
        raise Setup('unreadable')
    if not stat.S_ISREG(info.st_mode):
        raise Setup('unreadable')
    try:
        with open(spec, 'rb') as handle:
            raw = handle.read(STDIN_MAX)
    except OSError:
        raise Setup('unreadable')
    if oversize(len(raw)):
        raise Setup('too_large')
    return raw


def read_clients(spec):
    if spec == '-':
        raw = sys.stdin.buffer.read(STDIN_MAX)
        if oversize(len(raw)):
            raise Setup('too_large')
        return raw
    return read_file(spec)


def parse_clients(raw):
    try:
        data = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        raise Setup('bad_json')
    if not isinstance(data, list):
        raise Setup('bad_json')
    for element in data:
        if not isinstance(element, dict):
            raise Setup('bad_json')
    return data


def effect_of(fields):
    if fields:
        found = tokens_of(fields[0])
        if found:
            return found[0]
    return ''


def regex_of(field):
    found = CLASS_FIELD.fullmatch(field)
    if found is None:
        return None
    pattern = found.group(1)
    if REGEX_UNIT.fullmatch(pattern) is None:
        return None
    for shunned in SHUNNED:
        if shunned in pattern:
            return None
    try:
        return re.compile(pattern)
    except re.error:
        return None


def supported_size(fields):
    if len(fields) != 2:
        return None
    args = argument_tokens(fields[0])
    if len(args) == 2:
        return None
    for token in args:
        if SIZE_TOKEN.fullmatch(token) is None:
            return None
    pattern = regex_of(fields[1])
    if pattern is None:
        return None
    return (int(args[0]), int(args[1]), pattern)


def supported_float(fields):
    if len(fields) != 2:
        return None
    args = argument_tokens(fields[0])
    if len(args) != 1:
        return None
    value = args[0]
    if value != 'on':
        if value != 'off':
            return None
    pattern = regex_of(fields[1])
    if pattern is None:
        return None
    return (value, pattern)


def scan_rules(texts):
    rules = []
    other = 0
    unsupported = 0
    number = 0
    for index in range(len(texts)):
        for line in texts[index].split('\n'):
            trimmed = strip_edges(line)
            found = RULE_LINE.fullmatch(trimmed)
            if found is None:
                continue
            fields = []
            for field in found.group(1).split(','):
                fields.append(strip_edges(field))
            effect = effect_of(fields)
            if effect == 'size':
                parsed = supported_size(fields)
                if parsed is None:
                    unsupported += 1
                    continue
                number += 1
                rules.append((number, index + 1, 'size', parsed[0], parsed[1], parsed[2]))
                continue
            if effect == 'float':
                parsed = supported_float(fields)
                if parsed is None:
                    unsupported += 1
                    continue
                number += 1
                rules.append((number, index + 1, 'float', parsed[0], parsed[1]))
                continue
            other += 1
    return (rules, other, unsupported)


def dimension_ok(value):
    if isinstance(value, bool):
        return False
    if not isinstance(value, int):
        return False
    if value >= 0:
        return True
    return False


def client_record(element):
    if element.get('mapped') is False:
        return None
    label = element.get('class')
    if not isinstance(label, str):
        label = ''
    floating = element.get('floating') is True
    box = element.get('size')
    if isinstance(box, list):
        if len(box) == 2:
            if dimension_ok(box[0]):
                if dimension_ok(box[1]):
                    return (label, floating, (box[0], box[1]), address_of(element))
    return (label, floating, None, address_of(element))


def address_of(element):
    value = element.get('address')
    if not isinstance(value, str):
        return '-'
    return value


def holds_control(text):
    for char in text:
        if ord(char) < 32:
            return True
    return False


def rule_matches(pattern, label):
    if holds_control(label):
        return False
    return pattern.fullmatch(label) is not None


def evaluate(clients, rules, other, unsupported):
    lines = []
    size_rules = 0
    float_rules = 0
    for rule in rules:
        if rule[2] == 'size':
            size_rules += 1
            lines.append('MADO_GEOM_RULE: n=%d file=%d effect=size arg=%dx%d class=%s'
                         % (rule[0], rule[1], rule[3], rule[4], rule[5].pattern))
        else:
            float_rules += 1
            lines.append('MADO_GEOM_RULE: n=%d file=%d effect=float arg=%s class=%s'
                         % (rule[0], rule[1], rule[3], rule[4].pattern))
    mapped = 0
    unmapped = 0
    matched = 0
    agree = 0
    differ = 0
    tiled = 0
    badsize = 0
    for element in clients:
        record = client_record(element)
        if record is None:
            unmapped += 1
            continue
        mapped += 1
        label = record[0]
        floating = record[1]
        box = record[2]
        address = record[3]
        want = None
        float_rule = '-'
        for rule in rules:
            if rule[2] == 'size':
                if rule_matches(rule[5], label):
                    want = (rule[3], rule[4])
            else:
                if rule_matches(rule[4], label):
                    float_rule = rule[3]
        if want is None:
            continue
        matched += 1
        if box is None:
            verdict = 'BADSIZE'
            badsize += 1
        elif not floating:
            verdict = 'TILED'
            tiled += 1
        elif box == want:
            verdict = 'AGREE'
            agree += 1
        else:
            verdict = 'DIFFER'
            differ += 1
        if box is None:
            shown = '-'
        else:
            shown = '%dx%d' % box
        lines.append('MADO_GEOM_CLIENT: addr=%s class=%s floating=%s size=%s want=%dx%d'
                     ' float_rule=%s verdict=%s'
                     % (json.dumps(address), json.dumps(label),
                        'true' if floating else 'false', shown,
                        want[0], want[1], float_rule, verdict))
    summary = summary_line(size_rules, float_rules, other, unsupported, mapped,
                           matched, unmapped, agree, differ, tiled, badsize)
    lines.append(summary[0])
    return (lines, summary[1])


def summary_line(size_rules, float_rules, other, unsupported, mapped, matched,
                 unmapped, agree, differ, tiled, badsize):
    if size_rules == 0:
        verdict = 'NO_SIZE_RULES'
        code = 4
    else:
        if differ > 0:
            verdict = 'DIFFER'
            code = 1
        else:
            if matched == 0:
                verdict = 'NO_MATCHING_CLIENT'
                code = 3
            else:
                verdict = 'OK'
                code = 0
    text = ('MADO_GEOMETRY: rules=%d float_rules=%d other=%d unsupported=%d clients=%d'
            ' matched=%d unmapped=%d agree=%d differ=%d tiled=%d badsize=%d verdict=%s'
            % (size_rules, float_rules, other, unsupported, mapped, matched, unmapped,
               agree, differ, tiled, badsize, verdict))
    return (text, code)


def work(argv):
    parsed = parse_args(argv)
    if parsed[0] == 'usage':
        raise Setup('usage')
    if parsed[0] == 'selftest':
        return selftest()
    clients = parse_clients(read_clients(parsed[1]))
    texts = []
    for spec in parsed[2]:
        texts.append(read_file(spec).decode('utf-8', 'replace'))
    rules, other, unsupported = scan_rules(texts)
    return evaluate(clients, rules, other, unsupported)


def selftest():
    tally = [0, 0]

    def expect(got, wanted):
        tally[0] += 1
        if got == wanted:
            tally[1] += 1

    def fault(step):
        try:
            step()
        except Setup as problem:
            return problem.reason
        return 'none'

    def shaped_size(value):
        if value is None:
            return None
        return (value[0], value[1], value[2].pattern)

    def shaped_float(value):
        if value is None:
            return None
        return (value[0], value[1].pattern)

    class MemoryBuffer:
        def __init__(self, data):
            self.data = data
            self.pos = 0

        def read(self, limit):
            chunk = self.data[self.pos:self.pos + limit]
            self.pos += len(chunk)
            return chunk

    class Memory:
        def __init__(self, data):
            self.buffer = MemoryBuffer(data)

    expect(parse_args(['--selftest']), ('selftest', None, []))
    expect(parse_args([]), ('usage', None, []))
    expect(parse_args(['--bogus']), ('usage', None, []))
    expect(parse_args(['--clients', '-']), ('usage', None, []))
    expect(parse_args(['--rules', 'r']), ('usage', None, []))
    expect(parse_args(['--clients', '-', '--rules', 'r']), ('run', '-', ['r']))
    expect(parse_args(['--rules', 'r', '--clients', 'c']), ('run', 'c', ['r']))
    expect(parse_args(['--rules', 'a', '--rules', 'b', '--clients', '-']),
           ('run', '-', ['a', 'b']))
    expect(parse_args(['--clients']), ('usage', None, []))
    expect(parse_args(['--rules']), ('usage', None, []))
    expect(parse_args(['--clients', '-', '--clients', '-', '--rules', 'r']),
           ('usage', None, []))
    expect(parse_args(['--selftest', '--clients', '-']), ('usage', None, []))
    expect(parse_args(['--clients', '-', '--rules', 'r', 'extra']), ('usage', None, []))

    expect(oversize(0), False)
    expect(oversize(1048576), False)
    expect(oversize(1048577), True)
    expect(tokens_of(''), [])
    expect(tokens_of('size 420  500'), ['size', '420', '500'])
    expect(tokens_of('float\ton'), ['float', 'on'])
    expect(strip_edges(' \t x \t '), 'x')
    expect(argument_tokens('size 420 500'), ['420', '500'])

    expect(regex_of('match:class ^(org.arch.gkeep)$').pattern, '^(org.arch.gkeep)$')
    expect(regex_of('match:class'), None)
    expect(regex_of('match:class '), None)
    expect(regex_of('class ^x$'), None)
    expect(regex_of('match:class ' + 'a' * 200).pattern, 'a' * 200)
    expect(regex_of('match:class ' + 'a' * 201), None)
    expect(regex_of('match:class ' + 'a\\.' * 100).pattern, 'a\\.' * 100)
    expect(regex_of('match:class ' + 'a\\.' * 100 + 'b'), None)
    expect(regex_of('match:class ' + 'a\\.' * 60 + 'b' * 140), None)
    expect(regex_of('match:class ^a$('), None)
    expect(regex_of('match:class a(?i)b'), None)
    expect(regex_of('match:class a*+'), None)
    expect(regex_of('match:class ('), None)
    expect(regex_of(r'match:class a\.b').pattern, 'a\\.b')
    expect(regex_of('match:class a b'), None)

    expect(shaped_size(supported_size(['size 420 500', 'match:class ^(org.arch.gkeep)$'])),
           (420, 500, '^(org.arch.gkeep)$'))
    expect(supported_size(['size 420', 'match:class x']), None)
    expect(supported_size(['size 420 500 600', 'match:class x']), None)
    expect(supported_size(['size 420 500']), None)
    expect(supported_size(['size 420 500', 'match:class x', 'extra']), None)
    expect(supported_size(['size 123456 500', 'match:class x']), None)
    expect(supported_size(['size -1 500', 'match:class x']), None)
    expect(shaped_size(supported_size(['size 000 0200', 'match:class x'])), (0, 200, 'x'))

    expect(shaped_float(supported_float(['float on', 'match:class x'])), ('on', 'x'))
    expect(shaped_float(supported_float(['float off', 'match:class x'])), ('off', 'x'))
    expect(supported_float(['float', 'match:class x']), None)
    expect(supported_float(['float maybe', 'match:class x']), None)
    expect(supported_float(['float on off', 'match:class x']), None)
    expect(supported_float(['float on']), None)
    expect(supported_float(['float on', 'match:class x', 'extra']), None)

    expect(dimension_ok(0), True)
    expect(dimension_ok(7), True)
    expect(dimension_ok(-1), False)
    expect(dimension_ok(True), False)
    expect(dimension_ok(1.5), False)
    expect(holds_control('org.arch.gkeep'), False)
    expect(holds_control('a\nb'), True)
    expect(effect_of(['size 420 500']), 'size')
    expect(effect_of([]), '')

    rules_text = '\n'.join([
        '# gkeep size',
        'windowrule = size 420 500, match:class ^(org.arch.gkeep)$',
        'windowrule = float on, match:class ^(org.arch.gkeep)$',
        'windowrulev2 = size 1 1, match:class x',
        'windowrule = size 5 5, match:class ^(x)$',
        'windowrule = center, match:class x',
        'windowrule = size abc, match:class x',
        'WindowRule = size 9 9, match:class z',
    ]) + '\n'
    clients_text = ('[{"class":"org.arch.gkeep","mapped":true,"floating":true,'
                    '"size":[420,500],"address":"0x1"},'
                    '{"class":"org.arch.gkeep","mapped":false,"size":[1,2]},'
                    '{"class":"org.arch.gkeep","mapped":true,"floating":false,'
                    '"size":[1,2]},'
                    '{"class":"x","mapped":true,"floating":true,"size":[0,0]},'
                    '{"class":"x","mapped":true,"floating":true},'
                    '{"class":"x","class":"org.arch.gkeep","mapped":true,'
                    '"floating":true,"size":[420,500]},'
                    '{"class":"x","mapped":0,"floating":1,"size":[2,3],'
                    '"address":17}]')
    rules = scan_rules([rules_text])
    expect(rules[1], 1)
    expect(rules[2], 1)
    expect(len(rules[0]), 3)

    root = '/tmp/mado-geometry-selftest'
    try:
        os.makedirs(root)
    except OSError:
        pass

    def put(name, data):
        handle = open(os.path.join(root, name), 'wb')
        handle.write(data)
        handle.close()

    put('rules.conf', rules_text.encode('utf-8'))
    put('floatonly.conf', b'windowrule = float on, match:class x\n')
    put('clients.json', clients_text.encode('utf-8'))
    put('bad.json', b'{')
    put('notlist.json', b'{}')
    put('notobjects.json', b'[1]')
    put('blank.json', b'')
    put('exact.json', b'[]' + b' ' * (1048576 - 2))
    put('big.json', b'[]' + b' ' * (1048577 - 2))
    put('nofloat.json', b'[]')
    fifo = os.path.join(root, 'pipe')
    try:
        os.mkfifo(fifo)
    except OSError:
        pass

    expect(fault(lambda: read_clients(root)), 'unreadable')
    expect(fault(lambda: read_clients('/nonexistent-mado-geometry/x')), 'unreadable')
    expect(fault(lambda: read_clients(os.path.join(root, 'big.json'))), 'too_large')
    expect(fault(lambda: read_clients(fifo)), 'unreadable')
    expect(len(read_clients(os.path.join(root, 'exact.json'))), 1048576)
    expect(fault(lambda: read_clients(os.path.join(root, 'bad.json'))), 'none')
    expect(fault(lambda: parse_clients(b'{')), 'bad_json')
    expect(fault(lambda: parse_clients(b'')), 'bad_json')
    expect(fault(lambda: parse_clients(b'{}')), 'bad_json')
    expect(fault(lambda: parse_clients(b'[1]')), 'bad_json')
    expect(fault(lambda: parse_clients(b'\xff')), 'bad_json')
    expect(parse_clients(b'[{"a":1}]'), [{'a': 1}])

    saved = sys.stdin
    try:
        sys.stdin = Memory(b'[{"class":"x"}]')
        expect(len(read_clients('-')), 15)
        sys.stdin = Memory(b'[]' + b' ' * 1048575)
        expect(fault(lambda: read_clients('-')), 'too_large')
    finally:
        sys.stdin = saved

    outcome = work(['--clients', os.path.join(root, 'clients.json'),
                    '--rules', os.path.join(root, 'rules.conf')])
    expect(outcome[0], [
        'MADO_GEOM_RULE: n=1 file=1 effect=size arg=420x500 class=^(org.arch.gkeep)$',
        'MADO_GEOM_RULE: n=2 file=1 effect=float arg=on class=^(org.arch.gkeep)$',
        'MADO_GEOM_RULE: n=3 file=1 effect=size arg=5x5 class=^(x)$',
        'MADO_GEOM_CLIENT: addr="0x1" class="org.arch.gkeep" floating=true size=420x500'
        ' want=420x500 float_rule=on verdict=AGREE',
        'MADO_GEOM_CLIENT: addr="-" class="org.arch.gkeep" floating=false size=1x2'
        ' want=420x500 float_rule=on verdict=TILED',
        'MADO_GEOM_CLIENT: addr="-" class="x" floating=true size=0x0 want=5x5'
        ' float_rule=- verdict=DIFFER',
        'MADO_GEOM_CLIENT: addr="-" class="x" floating=true size=- want=5x5'
        ' float_rule=- verdict=BADSIZE',
        'MADO_GEOM_CLIENT: addr="-" class="org.arch.gkeep" floating=true size=420x500'
        ' want=420x500 float_rule=on verdict=AGREE',
        'MADO_GEOM_CLIENT: addr="-" class="x" floating=false size=2x3'
        ' want=5x5 float_rule=- verdict=TILED',
        'MADO_GEOMETRY: rules=2 float_rules=1 other=1 unsupported=1 clients=6 matched=6'
        ' unmapped=1 agree=2 differ=1 tiled=2 badsize=1 verdict=DIFFER',
    ])
    expect(outcome[1], 1)

    only = work(['--clients', os.path.join(root, 'clients.json'),
                 '--rules', os.path.join(root, 'floatonly.conf')])
    expect(only[0], ['MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=x',
                     'MADO_GEOMETRY: rules=0 float_rules=1 other=0 unsupported=0'
                     ' clients=6 matched=0 unmapped=1 agree=0 differ=0 tiled=0'
                     ' badsize=0 verdict=NO_SIZE_RULES'])
    expect(only[1], 4)

    empty = work(['--clients', os.path.join(root, 'exact.json'),
                  '--rules', os.path.join(root, 'rules.conf')])
    expect(empty[1], 3)
    expect(empty[0][-1], 'MADO_GEOMETRY: rules=2 float_rules=1 other=1 unsupported=1'
                         ' clients=0 matched=0 unmapped=0 agree=0 differ=0 tiled=0'
                         ' badsize=0 verdict=NO_MATCHING_CLIENT')

    expect(fault(lambda: work([])), 'usage')
    expect(fault(lambda: work(['--clients', os.path.join(root, 'bad.json'),
                               '--rules', '/nonexistent-mado-geometry/r'])), 'bad_json')
    expect(fault(lambda: work(['--clients', os.path.join(root, 'big.json'),
                               '--rules', '/nonexistent-mado-geometry/r'])), 'too_large')
    expect(fault(lambda: work(['--clients', os.path.join(root, 'notlist.json'),
                               '--rules', '/nonexistent-mado-geometry/r'])), 'bad_json')
    expect(fault(lambda: work(['--clients', os.path.join(root, 'notobjects.json'),
                               '--rules', os.path.join(root, 'rules.conf')])), 'bad_json')
    expect(fault(lambda: work(['--clients', os.path.join(root, 'clients.json'),
                               '--rules', '/nonexistent-mado-geometry/r'])), 'unreadable')
    expect(fault(lambda: work(['--clients', os.path.join(root, 'blank.json'),
                               '--rules', os.path.join(root, 'rules.conf')])), 'bad_json')

    put('ok.json', b'[{"class":"other","mapped":true,"floating":true,'
                   b'"size":[420,500],"address":"0x2"}]')
    put('okrules.conf', b'windowrule = size 420 500, match:class ^(other)$\n')
    fine = work(['--clients', os.path.join(root, 'ok.json'),
                 '--rules', os.path.join(root, 'okrules.conf')])
    expect(fine[0], [
        'MADO_GEOM_RULE: n=1 file=1 effect=size arg=420x500 class=^(other)$',
        'MADO_GEOM_CLIENT: addr="0x2" class="other" floating=true size=420x500'
        ' want=420x500 float_rule=- verdict=AGREE',
        'MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 clients=1'
        ' matched=1 unmapped=0 agree=1 differ=0 tiled=0 badsize=0 verdict=OK',
    ])
    expect(fine[1], 0)

    return (['MADO_GEOMETRY_SELFTEST: %d/%d passed' % (tally[1], tally[0])],
            0 if tally[1] == tally[0] else 1)


def main():
    try:
        outcome = work(sys.argv[1:])
    except Setup as problem:
        sys.stdout.write('MADO_GEOMETRY: SETUP %s\n' % problem.reason)
        return 2
    for line in outcome[0]:
        sys.stdout.write(line)
        sys.stdout.write('\n')
    return outcome[1]


if __name__ == '__main__':
    sys.exit(main())
