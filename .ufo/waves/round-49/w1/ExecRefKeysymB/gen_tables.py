#!/usr/bin/env python3
"""Generate Python table literals for keysym_ref.py from pinned libxkbcommon sources.

Inputs (pinned sha256 recorded in the receipt):
  src/ks_tables.h               (src/ks_tables.h)
  src/keysym-case-mappings.c    (src/keysym-case-mappings.c)
  src/keysym-utf.c              (src/keysym-utf.c)
"""
import re, sys, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'all')


def read(name):
    with open(os.path.join(SRC, name), encoding='utf-8', errors='surrogateescape') as f:
        return f.read()


def parse_name_keysym(block):
    """Parse `{ 0xNNNN, offset }, /* name */` entries, preserving order."""
    out = []
    for m in re.finditer(r'\{\s*0x([0-9a-fA-F]+)\s*,\s*(\d+)\s*\},\s*/\*\s*(\S+)\s*\*/', block):
        out.append((int(m.group(1), 16), int(m.group(2)), m.group(3)))
    return out


def parse_int_array(text, name):
    m = re.search(r'static const \w+ ' + name + r'\[[^\]]*\] = \{(.*?)\n\};', text, re.S)
    if not m:
        raise SystemExit('array not found: ' + name)
    body = m.group(1)
    return [int(x, 16) for x in re.findall(r'0x([0-9a-fA-F]+)', body)]


def parse_case_array(text, name):
    m = re.search(r'static const struct CaseMappings ' + name + r'\[[^\]]*\] = \{(.*?)\n\};', text, re.S)
    if not m:
        raise SystemExit('case array not found: ' + name)
    body = m.group(1)
    out = []
    for e in re.finditer(r'\{\s*(\d+)\s*,\s*(\d+)\s*,\s*(-?0x[0-9a-fA-F]+)\s*\}', body):
        out.append((int(e.group(1)), int(e.group(2)), int(e.group(3), 16) if not e.group(3).startswith('-0x')
                    else -int(e.group(3)[3:], 16)))
    return out


def main():
    ks = read('src_ks_tables.h')
    n2k_block = ks.split('static const struct name_keysym name_to_keysym[] = {', 1)[1].split('};', 1)[0]
    k2n_block = ks.split('static const struct name_keysym keysym_to_name[] = {', 1)[1].split('};', 1)[0]
    name_to_keysym = parse_name_keysym(n2k_block)
    keysym_to_name = parse_name_keysym(k2n_block)

    cm = read('src_keysym-case-mappings.c')
    legacy_data = parse_case_array(cm, 'legacy_keysym_data')
    legacy_o1 = parse_int_array(cm, 'legacy_keysym_offsets1')
    legacy_o2 = parse_int_array(cm, 'legacy_keysym_offsets2')
    unicode_data = parse_case_array(cm, 'unicode_data')
    unicode_o1 = parse_int_array(cm, 'unicode_offsets1')
    unicode_o2 = parse_int_array(cm, 'unicode_offsets2')

    utf = read('src_keysym-utf.c')
    tab = utf.split('static const struct codepair keysymtab[] = {', 1)[1].split('\n};', 1)[0]
    low_ucs = {}
    for m in re.finditer(r'\{\s*0x([0-9a-fA-F]+)\s*,\s*(true|false)\s*,\s*0x([0-9a-fA-F]+)\s*\}', tab):
        ksv, dep, ucs = int(m.group(1), 16), m.group(2) == 'true', int(m.group(3), 16)
        if dep or ucs > 0xff:
            continue
        if ucs not in low_ucs:
            low_ucs[ucs] = ksv

    out = []
    w = out.append
    w('# --- BEGIN GENERATED TABLES (libxkbcommon 1.13.2, pinned) ---')
    w('# name_to_keysym: every explicit name, in libxkbcommon table order (alias order matters')
    w('# for case-insensitive lookup: the LAST case-insensitive match wins).')
    w('_NAME_TO_KEYSYM_ORDER = [')
    line = []
    for v, _off, name in name_to_keysym:
        line.append('(%r,0x%x)' % (name, v))
        if len(line) == 4:
            w('    ' + ','.join(line) + ',')
            line = []
    if line:
        w('    ' + ','.join(line) + ',')
    w(']')
    w('# keysym_to_name: canonical (get_name) table.')
    w('_KEYSYM_TO_NAME = {')
    line = []
    for v, _off, name in keysym_to_name:
        line.append('0x%x:%r' % (v, name))
        if len(line) == 5:
            w('    ' + ','.join(line) + ',')
            line = []
    if line:
        w('    ' + ','.join(line) + ',')
    w('}')
    w('# case mappings (src/keysym-case-mappings.c), chunk-compressed exactly as upstream.')
    w('_LEGACY_DATA = %r' % (legacy_data,))
    w('_LEGACY_O1 = %r' % (legacy_o1,))
    w('_LEGACY_O2 = %r' % (legacy_o2,))
    w('_UNICODE_DATA = %r' % (unicode_data,))
    w('_UNICODE_O1 = %r' % (unicode_o1,))
    w('_UNICODE_O2 = %r' % (unicode_o2,))
    w('# U+0000..U+00FF normalisation table (src/keysym-utf.c keysymtab, non-deprecated).')
    w('_LOW_UCS = %r' % (sorted(low_ucs.items()),))
    w('# --- END GENERATED TABLES ---')

    text = '\n'.join(out) + '\n'
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tables.py'), 'w') as f:
        f.write(text)
    print('names=%d canonical=%d legacy_data=%d unicode_data=%d low_ucs=%d bytes=%d' % (
        len(name_to_keysym), len(keysym_to_name), len(legacy_data), len(unicode_data),
        len(low_ucs), len(text)))


if __name__ == '__main__':
    main()
