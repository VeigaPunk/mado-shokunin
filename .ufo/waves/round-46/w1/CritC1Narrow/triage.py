#!/usr/bin/env python3
"""CritC1Narrow triage: score reference variants against the frozen round-46 C1 harness without bwrap.

Mirrors clause f (3 fixture runs: seed46/A, seed46/B, nonce/A) and clause g (150 generated cases vs the
reference, in-process) using the counter's own functions, with the sandbox replaced by a plain exec.
Each variant is scored at several nonces. Prints one line per variant.
"""
import concurrent.futures
import importlib.util
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r46-devices.py")
REF = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
SCR = "/fast/scratch/hyaku/mado-r46/CritC1Narrow"
NONCES = [4646, 12345, 987654, 271828]

CONT_OLD = '        while line.endswith("\\\\"):\n            if i >= len(raw_lines):\n                dropped = True\n                break\n            line = line[:-1].rstrip(" \\t") + raw_lines[i]\n            i += 1\n'
CONT_NEW = '        if line.endswith("\\\\"):\n            if i >= len(raw_lines):\n                dropped = True\n            else:\n                line = line[:-1].rstrip(" \\t") + raw_lines[i]\n                i += 1\n'

BIG_OLD = '    finally:\n        os.close(fd)\n    if len(data) > MAX_BYTES:\n        raise Setup("too_large")\n    return data\n'
BIG_NEW = '    finally:\n        os.close(fd)\n    if len(data) >= MAX_BYTES:\n        raise Setup("too_large")\n    return data\n'

FIFO_OLD = '        if not stat.S_ISREG(os.fstat(fd).st_mode):\n            raise Setup("unreadable")\n'

VARIANTS = {
    # rule: continuation joins only one following raw line (contract: loops until a line does not end in "\")
    "P01-single-continuation": ([(CONT_OLD, CONT_NEW)], []),
    # rule: a non-relevant line is ignored; here `source = ...` is counted unsupported
    "P02-source-unsupported": ([('        if not (key.startswith("device") or key in INPUT_KEYS):\n            continue\n',
                               '        if not (key.startswith("device") or key in INPUT_KEYS):\n            if key == "source":\n                st.unsupported += 1\n            continue\n')], []),
    # rule: a line starting with "#" (after strip of " \t\r") may be a directive; here only column 0 counts
    "P03-indented-directive": ([('        if line.startswith("#"):\n            if DIRECTIVE_RE.match(line):',
                                 '        if line.startswith("#"):\n            if raw.startswith("#") and DIRECTIVE_RE.match(line):')], []),
    # rule: every other value is the RHS string; here spaces around commas are normalised
    "P04-comma-space-trim": ([('        st.globals[key[len("input:"):]] = rhs',
                              '        st.globals[key[len("input:"):]] = re.sub(r"\\s*,\\s*", ",", rhs)'),
                             ('    else:\n        dev[field] = rhs', '    else:\n        dev[field] = re.sub(r"\\s*,\\s*", ",", rhs)')], []),
    # rule: input:kb_X sets the global value even when a bracket name was cut out
    "P05-bracket-input-ignored": ([('        if key in INPUT_KEYS:\n            st.globals[key[len("input:"):]] = rhs',
                                   '        if key in INPUT_KEYS and bracket is None:\n            st.globals[key[len("input:"):]] = rhs')], []),
    # rule: kb_file=<set|-> is the printed EXPECTED value being non-empty; here "key was set at all"
    "P06-kb-file-set-when-empty": ([('    return tuple(out[:5]), out[5]',
                                    '    return tuple(out[:5]), (out[5] or ("x" if ("kb_file" in blk or "kb_file" in st.globals) else ""))')], []),
    # rule: reported=<F|?> where ? is a non-finite or non-number scrollFactor
    "P07-nonfinite-reported": ([('            "%.2f" % r if is_num(r) else "?", verdict))',
                               '            "%.2f" % r if isinstance(r, (int, float)) and not isinstance(r, bool) else "?", verdict))')], []),
    # rule: config decoded as UTF-8 with errors replaced
    "P08-strict-utf8-config": ([('texts = [read_regular(c).decode("utf-8", errors="replace") for c in configs]',
                                'texts = [read_regular(c).decode("utf-8") for c in configs]')], []),
    # rule: scrollFactor AGREE = a finite NUMBER (not a boolean); here only float is a number
    "P09-int-not-number": ([('    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)',
                            '    return isinstance(v, float) and math.isfinite(v)')], []),
    # rule: a PATH that is a FIFO or non-regular file is unreadable
    "P10-regular-check-dropped": ([(FIFO_OLD, '')], []),
    # rule: an input larger than 1048576 bytes is too_large (exactly 1048576 is allowed)
    "P11-size-boundary": ([(BIG_OLD, BIG_NEW)], []),
    # rule: --devices exactly once
    "P12-devices-twice": ([('        if flag == "--devices" and devices is None:', '        if flag == "--devices":')], []),
    # rule: the category stack starts empty in each file
    "P13-stack-shared": ([('def parse_config(text, st):\n    stack = []',
                          'STACK = []\n\n\ndef parse_config(text, st):\n    stack = STACK')], []),
    # rule: nonzero value below 2**-126 is unsupported
    "P14-no-underflow": ([('    if math.isinf(v) or (v != 0.0 and abs(float(m.group(0))) < FLT_MIN):',
                          '    if math.isinf(v):')], []),
    # rule: the special prefix match is inf/nan/hex in any case
    "P15-case-sensitive-special": ([('SPECIAL_RE = re.compile(r"[+-]?(inf|nan|0x)", re.I)',
                                    'SPECIAL_RE = re.compile(r"[+-]?(inf|nan|0x)")')], []),
    # rule: VIRTUAL when the name STARTS WITH hl-virtual-keyboard
    "P16-virtual-contains": ([('        if name.startswith(VIRTUAL_PREFIX):', '        if VIRTUAL_PREFIX in name:')], []),
    # rule: LHS and RHS are separated by the first "=" (no spaces required)
    "P18-eq-needs-spaces": ([('        eq = line.find("=")\n        if eq < 0:',
                             '        eq = line.find(" = ")\n        if eq >= 0:\n            eq += 1\n        if eq < 0:')], []),
    # rule: a line ending in "{" pushes its text before the "{" (no space required)
    "P19-brace-needs-space": ([('            elif line.endswith("{"):', '            elif line.endswith(" {"):')], []),
    # rule: only ASCII whitespace is stripped, so a leading BOM leaves the first key line non-relevant
    "P22-bom-stripped": ([('        line = raw.strip(" \\t\\r")',
                          '        line = raw.lstrip("\\ufeff").strip(" \\t\\r")')], []),
    # rule: a block MATCHES a name in ANY top-level list of the dump (switches included)
    "P23-switch-name-ignored": ([('    for lst in doc.values():\n        if not isinstance(lst, list):\n            continue',
                                  '    for k in ("keyboards", "mice", "tablets", "touch"):\n        lst = doc.get(k)\n        if not isinstance(lst, list):\n            continue')], []),
    # rule: comment search resumes two characters after the first "#" of a pair
    "P20-hash-resume": ([('            resume = pos + 2', '            resume = pos + 1')], []),
    # rule: comment cutting runs after the strip of " \t\r" (only ASCII WS stripped afterwards)
    "P21-no-cr-strip": ([('        line = raw.strip(" \\t\\r")', '        line = raw.strip(" \\t")')], []),
}


def load_counter():
    spec = importlib.util.spec_from_file_location("c1r46", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.sandbox = lambda argv, cwd, hide, marker_dir: argv
    return mod


def score_variant(item):
    name, (edits, _) = item
    C = load_counter()
    ref = open(REF).read()
    src = ref
    for old, new in edits:
        n = src.count(old)
        if n != 1:
            return "%s ANCHOR-MISS %d %r" % (name, n, old[:50])
        src = src.replace(old, new)
    body = os.path.join(SCR, "work-%s" % name)
    os.makedirs(body, exist_ok=True)
    tool = os.path.join(body, "mado-devices.py")
    open(tool, "w").write(src)
    model = C.load_model()
    fixtures = C.load_fixtures()
    out = []
    marker = os.path.join(body, "mk")
    os.makedirs(marker, exist_ok=True)
    fakebin = os.path.join(body, "bin", "bin")
    if not os.path.isdir(fakebin):
        C.make_fakebin(fakebin, os.path.join(marker, "marker"))
    import tempfile
    sd = tempfile.mkdtemp(dir=body, prefix="st-")
    import subprocess
    p = subprocess.run([sys.executable, "-I", tool, "--selftest"], capture_output=True,
                       env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": sd})
    last = p.stdout.decode().strip().split("\n")[-1]
    out.append("selftest rc=%d %s" % (p.returncode, last))
    import random
    for nonce in NONCES:
        rng = random.Random(nonce)
        t46, tn = C.names(C.SEED), C.names(nonce)
        bad = []
        for fx in fixtures:
            for table, variant in ((t46, "A"), (t46, "B"), (tn, "A")):
                ok, why = C.run_fixture(tool, body, fx, table, fakebin, [], marker, variant, rng)
                if not ok:
                    bad.append((fx["label"], variant, why[:120]))
        g_ok, first = C.run_generated(tool, body, model, random.Random(nonce ^ 0x5DEECE66D), tn, fakebin, [], marker)
        out.append("nonce=%d fixtures_fail=%d %s gen=%d/150 %s" % (
            nonce, len(bad), [b[0] + "/" + b[1] for b in bad][:4], g_ok,
            "" if first is None else "first=%r" % (first[1][:1],)))
        if bad and len(bad) < 3:
            out.append("   why: %r" % (bad[:2],))
    return "%s\n  " % name + "\n  ".join(out)


def main():
    items = list(VARIANTS.items())
    only = sys.argv[1:] or None
    if only:
        items = [i for i in items if i[0] in only]
    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as ex:
        for r in ex.map(score_variant, items):
            print(r, flush=True)


if __name__ == "__main__":
    main()
