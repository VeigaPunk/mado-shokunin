#!/usr/bin/env python3
"""Probe v2: differential (in-process + file-level) and unreachability proofs.

Output: one block per variant ending in LIVE (witness) or NO-DIFF, plus PROOF lines for the
variants claimed dead (tautology / typing / invariant brute force).
"""
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF_PATH = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
FIX_PATH = os.path.join(LANE, "quality/counters/c1-r46-fixtures.json")
COUNTER_PATH = os.path.join(LANE, "quality/counters/c1-r46-devices.py")
HERE = os.path.dirname(os.path.abspath(__file__))
VDIR = os.path.join(HERE, "variants")
BIG_CONFIG = "# " + "x" * 1048580 + "\n"
BIG_DUMP = b'{"keyboards": [], "mice": []' + b" " * 1048580 + b"}"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def out(mod, dump_bytes, texts):
    try:
        lines, rc = mod.report(dump_bytes, texts)
    except mod.Setup as e:
        return ["MADO_DEVICES: SETUP %s" % e], 2
    except Exception as e:
        return ["EXC %s: %s" % (type(e).__name__, e)], -1
    return lines, rc


def kb(name="k", layout="us", variant="", options="", model="", rules=""):
    return {"address": "0x1", "name": name, "rules": rules, "model": model, "layout": layout,
            "variant": variant, "options": options, "active_layout_index": 0, "active_keymap": "x",
            "capsLock": False, "numLock": False, "main": False}


def mouse(name="m", sf=-1.0):
    return {"address": "0x2", "name": name, "defaultSpeed": 0.0, "scrollFactor": sf}


def dump(kbs=None, mice=None, **extra):
    d = {"mice": list(mice or []), "keyboards": list(kbs if kbs is not None else [kb()]),
         "tablets": [], "touch": [], "switches": []}
    d.update(extra)
    return json.dumps(d).encode()


def fixture_cases():
    counter = load(COUNTER_PATH, "c1counter")
    fixtures = json.load(open(FIX_PATH))
    table = counter.names(46)
    cases, skipped = [], []
    for fx in fixtures:
        if fx["configs"] in ("usage", None) or fx["dump_bytes"]:
            skipped.append(fx["label"])
            continue
        raw = json.dumps(counter.subst(fx["dump"], table), indent=2).encode()
        texts = [BIG_CONFIG if t == "@BIG" else counter.subst(t, table) for t in fx["configs"]]
        cases.append(("fx:" + fx["label"], raw, texts))
    return cases, skipped


HAND_CONFIGS = [
    "device[k]:sensitivity = 1\n",
    "device[k]:name = z\n",
    "device[k]:kb_layout = fr\n",
    "device[k] {\n  kb_layout = fr\n}\n",
    "device {\n  sensitivity = 1\n}\n",
    "device {\n  kb_layout = de\n}\n",
    "device {\n  kb_layout = de\n  kb_options = x\n}\n",
    "device {\n  kb_layout = de\n  name = k\n}\n",
    "device {\n  name = a\n  name = k\n  kb_layout = de\n}\n",
    "device {\n  name = a\n}\ndevice:kb_layout = de\n",
    "device[a] {\n  name = k\n  kb_layout = de\n}\n",
    "device[x] = 1\n",
    "device = 1\n",
    "device {\n  = $x\n}\n",
    "device {\n  $x = 1\n}\n",
    "= x\n",
    "input {\n  $x = 1\n}\n",
    "input:kb_layout = br\\\n",
    "input:kb_layout = br \\\nus\n",
    "input:kb_layout = br\\\nus\n",
    "\vinput:kb_layout = br\v",
    "input:kb_layout\r# c\n",
    "  # hyprlang if X\ninput:kb_layout = br\n",
    "\v# hyprlang if X\ninput:kb_layout = br\n",
    "#hyprlangendif\n",
    "# hyprlangx\n",
    "input[kb_layout] = br\n",
    "inpu[kb_layout]t:kb_layout = fr\n",
    "device {\n  name = k\n  kb_layout] = fr\n}\n",
    "device:kb_layout] = fr\n",
    "device[kb_layout] = fr\n",
    "device]x:kb_layout = fr\n",
    "device[x]:kb_layout] = fr\n",
    "input:kb_layout] = de\n",
    "device {\n}\n}\n",
    "device {\n  name = k\n  }\n}\n",
    "input {\n  kb_layout = br\n}\n",
    "device {\n  name = k\n  kb_layout = fr\n}\n",
    "input {\n  kb_layout = br\n  touchpad {\n    scroll_factor = 0.4\n  }\n}\n",
    "device {\n  name = k\n  scroll_factor = 1\n}\n",
    "device:name = k\n",
    "device:name = k\ndevice:kb_variant = intl\n",
    "#input:kb_layout = de\n",
    "input:kb_options = a##b # c\n",
    "input:kb_options = a###b\n",
    "input:kb_options = a####b\n",
    "input:kb_options = a#####b\n",
    "input:kb_options = {{1+1}}\n",
    "input:kb_model = \xff\n",
    "input:kb_layout = br##\n",
    "input:kb_layout = #\n",
    "input:kb_layout = br #\n",
    "device {\n  name = k\n  kb_layout = [[EMPTY]]\n}\n",
    "device {\n  name = k\n  kb_file = ~/x.xkb\n}\n",
    "device {\n  name = k\n  kb_file = [[EMPTY]]\n}\n",
    "device[m]:scroll_factor = 1e-46\n",
    "device[m]:scroll_factor = -1e-46\n",
    "device[m]:scroll_factor = 1.17549428e-38\n",
    "device[m]:scroll_factor = 1.17549430e-38\n",
    "device[m]:scroll_factor = 1.1754942e-38\n",
    "device[m]:scroll_factor = 1e-40\n",
    "device[m]:scroll_factor = 3.4028236e38\n",
    "device[m]:scroll_factor = -3.4028236e38\n",
    "device[m]:scroll_factor = 1e39\n",
    "device[m]:scroll_factor = -1e39\n",
    "device[m]:scroll_factor = 0x10\n",
    "device[m]:scroll_factor = Inf\n",
    "device[m]:scroll_factor = -nan\n",
    "device[m]:scroll_factor = .5\n",
    "device[m]:scroll_factor = 5.\n",
    "device[m]:scroll_factor = 0.335\n",
    "device[m]:scroll_factor = 0.125\n",
    "device[m]:scroll_factor = 250\n",
    "device[m]:scroll_factor = -3\n",
    "device[m]:scroll_factor = fast\n",
    "device[m]:scroll_factor = [[EMPTY]]\n",
    "device[m]:scroll_factor =\n",
    "device[m]:scroll_factor = 1e\n",
    "device[m]:scroll_factor = +.5e+1\n",
    "device {\n  name = m\n  scroll_factor = 0.5\n}\n",
    "input {\n  scroll_factor = 2\n}\n",
]
HAND_DUMPS = [
    ("us-kb", dump([kb("k")], [mouse("m")])),
    ("nonstr-layout", dump([{"name": "k", "layout": 5, "variant": "", "options": "", "model": "", "rules": ""}])),
    ("null-layout", dump([{"name": "k", "layout": None, "variant": None, "options": None, "model": None,
                           "rules": None}])),
    ("bool-layout", dump([{"name": "k", "layout": True, "variant": False, "options": [], "model": {},
                           "rules": "us"}])),
    ("float-layout", dump([{"name": "k", "layout": 1.0, "variant": "", "options": "", "model": "", "rules": ""}])),
    ("extra-null", dump(extra_key=None)),
    ("extra-int", dump(extra_key=7)),
    ("extra-str", dump(extra_key="abc")),
    ("extra-dict", dump(extra_key={"a": 1})),
    ("extra-list-scalars", dump(extra_key=[1, "k", None])),
    ("tablets-nondict", dump(tablets=[1, "x", None])),
    ("belongs-nondict", dump(tablets=[{"name": "t", "belongsTo": 5}])),
    ("belongs-nonstr", dump(tablets=[{"name": "t", "belongsTo": {"name": 7}}])),
    ("empty", dump([], [])),
    ("nan-sf", b'{"keyboards": [], "mice": [{"name": "m", "scrollFactor": NaN}]}'),
    ("inf-sf", b'{"keyboards": [], "mice": [{"name": "m", "scrollFactor": Infinity}]}'),
    ("bool-sf", dump([], [mouse("m", True)])),
    ("str-sf", b'{"keyboards": [], "mice": [{"name": "m", "scrollFactor": "0.50"}]}'),
    ("int-sf", b'{"keyboards": [], "mice": [{"name": "m", "scrollFactor": 0}]}'),
    ("virtual", dump([kb("hl-virtual-keyboard-x", "us")])),
    ("virtual-differ", dump([kb("hl-virtual-keyboard-x", "de")])),
    ("virtual-exact", dump([kb("hl-virtual-keyboard", "us")])),
    ("virtual-short", dump([kb("hl-virtual-keyboar", "de")])),
    ("fallback", dump([kb("k", "us")])),
    ("num-name", dump([{"name": 5, "layout": "us", "variant": "", "options": "", "model": "", "rules": ""}])),
    ("belongs-empty-name", dump([kb("k")], tablets=[{"name": "t", "belongsTo": {"name": ""}}])),
    ("belongs-unhashable-name", dump([kb("k")], tablets=[{"name": "t", "belongsTo": {"name": ["a"]}}])),
    ("tablet-unhashable-name", dump([kb("k")], tablets=[{"name": ["a"]}])),
]


def hand_cases():
    cases = []
    for c in HAND_CONFIGS:
        for label, d in HAND_DUMPS:
            cases.append(("hand:%s|%s" % (c.replace("\n", "\\n")[:46], label), d, [c]))
    for label, d in HAND_DUMPS:
        cases.append(("hand:empty|%s" % label, d, [""]))
    return cases


def generated_cases(ref, n=4000):
    counter = load(COUNTER_PATH, "c1counter_gen")
    cases, seen = [], set()
    for seed in (46, 47, 1009, 65537):
        rng = random.Random(seed)
        table = counter.names(seed)
        for _ in range(n // 4):
            texts, d = counter.gen_case(rng, table, ref)
            raw = json.dumps(d, indent=2).encode()
            key = (raw, tuple(texts))
            if key in seen:
                continue
            seen.add(key)
            cases.append(("gen:%d:%d" % (seed, len(cases)), raw, texts))
    return cases


VARIANTS = [
    ("V01-bracket-rb-conjunct", "if lb != -1 and rb != -1 and lb < rb:", "if lb != -1 and lb < rb:"),
    ("V02-bracket-lb-conjunct", "if lb != -1 and rb != -1 and lb < rb:", "if lb < rb:"),
    ("V03-kb-rep-isinstance", 'rep = tuple(kb.get(n) if isinstance(kb.get(n), str) else None for n in NAMES)',
     'rep = tuple(kb.get(n) for n in NAMES)'),
    ("V04-dumpnames-elem-dict", "            if not isinstance(e, dict):\n                continue\n", ""),
    ("V05-dumpnames-lst-list", "        if not isinstance(lst, list):\n            continue\n", ""),
    ("V06-dumpnames-belongs", '            if isinstance(b, dict) and isinstance(b.get("name"), str):',
     '            if isinstance(b, dict) and b.get("name"):'),
    ("V07-float-zero-guard", 'if math.isinf(v) or (v != 0.0 and abs(float(m.group(0))) < FLT_MIN):',
     'if math.isinf(v) or abs(float(m.group(0))) < FLT_MIN:'),
    ("V08-float-abs-v", 'if math.isinf(v) or (v != 0.0 and abs(float(m.group(0))) < FLT_MIN):',
     'if math.isinf(v) or (v != 0.0 and abs(v) < FLT_MIN):'),
    ("V09-float-no-isinf", 'if math.isinf(v) or (v != 0.0 and abs(float(m.group(0))) < FLT_MIN):',
     'if v != 0.0 and abs(float(m.group(0))) < FLT_MIN:'),
    ("V10-bracket-unknown-else", "            else:\n                st.device(bracket)\n            continue\n",
     "            continue\n"),
    ("V11-bracket-name-create", "            elif field == \"name\":\n                st.device(bracket)\n"
     "                st.unsupported += 1\n", "            elif field == \"name\":\n                st.unsupported += 1\n"),
    ("V12-bracket-hoisted", "            if field in DEVICE_KEYS:\n                set_device_key(st.device(bracket), "
     "field, rhs, st)\n            elif field == \"name\":\n                st.device(bracket)\n"
     "                st.unsupported += 1\n            else:\n                st.device(bracket)\n",
     "            st.device(bracket)\n            if field in DEVICE_KEYS:\n                set_device_key("
     "st.devices[bracket], field, rhs, st)\n            elif field == \"name\":\n                st.unsupported += 1\n"),
    ("V13-stof-unsupported", "        elif kind == \"unsupported\":\n            st.unsupported += 1\n", ""),
    ("V14-cur-false-guard", "        if cur is False:\n            st.unsupported += 1\n            continue\n", ""),
    ("V15-cur-false-set", "                st.unsupported += 1\n                cur = False\n",
     "                st.unsupported += 1\n"),
    ("V16-cur-false-rename", "        elif field == \"name\":\n            st.unsupported += 1\n            cur = "
     "False\n", "        elif field == \"name\":\n            st.unsupported += 1\n"),
    ("V17-cur-reset-on-close", "                    if not stack:\n                        cur = None\n", ""),
    ("V18-lhs-empty", "        if not lhs or lhs.startswith(\"$\"):", "        if lhs.startswith(\"$\"):"),
    ("V19-lhs-variable", "        if not lhs or lhs.startswith(\"$\"):", "        if not lhs:"),
    ("V20-first-strip", '        line = raw.strip(" \\t\\r")\n', "        line = raw\n"),
    ("V21-cont-final-drop", "        if not dropped:\n            out.append(line)\n", "        out.append(line)\n"),
    ("V22-cont-rstrip", '            line = line[:-1].rstrip(" \\t") + raw_lines[i]',
     '            line = line[:-1] + raw_lines[i]'),
    ("V23-stack-open-strip", "                stack.append(line[:-1].strip(WS))", "                stack.append(line[:-1])"),
    ("V24-WS-no-newline", 'WS = " \\t\\r\\n\\v\\f"', 'WS = " \\t\\r\\v\\f"'),
    ("V25-comment-resume", "            resume = pos + 2", "            resume = pos + 1"),
    ("V26-directive-bound", 'DIRECTIVE_RE = re.compile(r"#[ \\t]*hyprlang\\b")',
     'DIRECTIVE_RE = re.compile(r"#[ \\t]*hyprlang")'),
    ("V26b-directive-count", "            if DIRECTIVE_RE.match(line):\n                st.unsupported += 1\n",
     "            if False:\n                st.unsupported += 1\n"),
    ("V27-key-relevant-inputset", '        if not (key.startswith("device") or key in INPUT_KEYS):\n'
     '            continue\n', '        if not key.startswith("device"):\n            continue\n'),
    ("V28-device-colon-guard", '        if not key.startswith("device:"):\n            continue\n', ""),
    ("V29-global-key", '        if key in INPUT_KEYS:\n            st.globals[key[len("input:"):]] = rhs\n'
     '            continue\n', '        if key in INPUT_KEYS:\n            st.globals[key] = rhs\n            continue\n'),
    ("V30-kb-virtual-only-when-agree", '        if name.startswith(VIRTUAL_PREFIX):',
     '        if name.startswith(VIRTUAL_PREFIX) and not differ:'),
    ("V31-fallback-order", '        elif not differ:\n            verdict = "AGREE"\n            c["agree"] += 1\n'
     '        elif rep == FALLBACK:\n            verdict = "FALLBACK"\n            c["fallback"] += 1\n',
     '        elif rep == FALLBACK:\n            verdict = "FALLBACK"\n            c["fallback"] += 1\n'
     '        elif not differ:\n            verdict = "AGREE"\n            c["agree"] += 1\n'),
    ("V32-verdict-nokb", '    elif not c["keyboards"]:\n        v, rc = "NO_KEYBOARDS", 3\n', ""),
    ("V33-mouse-clamp", '        exp = min(max(blk["scroll_factor"], 0.0), 100.0) if "scroll_factor" in blk '
     'else -1.0', '        exp = blk["scroll_factor"] if "scroll_factor" in blk else -1.0'),
    ("V34-mouse-numeric-eq", 'if is_num(r) and "%.2f" % r == "%.2f" % exp:', 'if is_num(r) and r == exp:'),
    ("V35-mouse-bool", "    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)",
     "    return isinstance(v, (int, float)) and math.isfinite(v)"),
    ("V36-mouse-isfinite", "    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)",
     "    return isinstance(v, (int, float)) and not isinstance(v, bool)"),
    ("V37-empty-marker", '        out.append("" if v == EMPTY else v)', "        out.append(v)"),
    ("V38-default-layout", '            v = "us" if n == "layout" else ""', '            v = ""'),
    ("V39-empty-stack-guard", "                if stack:\n                    stack.pop()\n"
     "                    if not stack:\n                        cur = None\n",
     "                stack.pop()\n                if not stack:\n                    cur = None\n"),
    ("V43-f32", "    try:\n        return struct.unpack(\"<f\", struct.pack(\"<f\", x))[0]\n    except OverflowError:\n"
     "        return math.inf if x > 0 else -math.inf", "    return x"),
    ("V43b-f32-sign", "        return math.inf if x > 0 else -math.inf", "        return math.inf"),
    ("V44-present", '    present = dump_names(doc)', '    present = {d["name"] for d in doc["keyboards"] + '
     'doc["mice"]}'),
    ("V45-special-re", 'SPECIAL_RE = re.compile(r"[+-]?(inf|nan|0x)", re.I)',
     'SPECIAL_RE = re.compile(r"(inf|nan|0x)")'),
    ("V46-stale-count", "        stale += 0 if ok else 1", "        stale += 1"),
    ("V47-differ-sep", '            "set" if kbfile else "-", ",".join(differ) if differ else "-", verdict))',
     '            "set" if kbfile else "-", " ".join(differ) if differ else "-", verdict))'),
    ("V48-expected-get", '    blk = st.devices.get(name, {})\n    out = []', '    blk = st.devices[name]\n    out = []'),
    ("V49-cur-rename-devs", '        if field in DEVICE_KEYS:\n            set_device_key(st.devices[cur], field, '
     'rhs, st)', '        if field in DEVICE_KEYS:\n            set_device_key(st.device(cur), field, rhs, st)'),
    ("V50-report-order-unsupported", "    if st.unsupported:", "    if False:"),
    ("V51-number-nonstr-name-ok", '        if not isinstance(lst, list) or not all(isinstance(e, dict) and '
     'isinstance(e.get("name"), str) for e in lst):',
     '        if not isinstance(lst, list) or not all(isinstance(e, dict) for e in lst):'),
    ("V52-selftest-unused-kb-fields", '    return {"address": "0x1", "name": name, "rules": rules, "model": model, '
     '"layout": layout, "variant": variant,\n            "options": options, "active_layout_index": 0, '
     '"active_keymap": "x", "capsLock": False,\n            "numLock": False, "main": False}',
     '    return {"name": name, "rules": rules, "model": model, "layout": layout, "variant": variant,'
     '\n            "options": options}'),
    ("V06b-belongs-name-str", '            if isinstance(b, dict) and isinstance(b.get("name"), str):', '            if isinstance(b, dict):'),
    ("V06c-elem-name-str", '            if isinstance(e.get("name"), str):\n                names.add(e["name"])', '            names.add(e["name"])'),
    ("V51b-name-str", 'isinstance(e.get("name"), str) for e in lst)', 'True for e in lst)'),
    ("V54-resume-plus3", "            resume = pos + 2", "            resume = pos + 3"),
    ("V55-special-nocase", 'SPECIAL_RE = re.compile(r"[+-]?(inf|nan|0x)", re.I)', 'SPECIAL_RE = re.compile(r"[+-]?(inf|nan|0x)")'),
    ("V56-float-noexp", 'FLOAT_RE = re.compile(r"[+-]?([0-9]+(\\.[0-9]*)?|\\.[0-9]+)([eE][+-]?[0-9]+)?")', 'FLOAT_RE = re.compile(r"[+-]?([0-9]+(\\.[0-9]*)?|\\.[0-9]+)")'),
    ("V57-float-nosign", 'FLOAT_RE = re.compile(r"[+-]?([0-9]+(\\.[0-9]*)?|\\.[0-9]+)([eE][+-]?[0-9]+)?")', 'FLOAT_RE = re.compile(r"([0-9]+(\\.[0-9]*)?|\\.[0-9]+)([eE][+-]?[0-9]+)?")'),
    ("V58-no-nonblock", "fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)", "fd = os.open(path, os.O_RDONLY)"),
    ("V42b-badjson-recursion", "    except (UnicodeDecodeError, ValueError, RecursionError):", "    except (UnicodeDecodeError, ValueError):"),
    ("V53-idempotent-anchor", "            resume = pos + 2", "            resume = pos + 2  # noop"),
]

FILE_CASES = [
    ("no-args", [], None, None),
    ("devices-only", ["--devices", "D"], None, None),
    ("config-only", ["--config", "C0"], "D", None),
    ("devices-twice", ["--devices", "D", "--devices", "D2", "--config", "C0"], "D", None),
    ("flag-no-value", ["--devices"], None, None),
    ("selftest-extra", ["--selftest", "x"], None, None),
    ("unknown-flag", ["--devices", "D", "--config", "C0", "--x", "y"], "D", None),
    ("missing-file", ["--devices", "MISSING", "--config", "C0"], None, None),
    ("config-missing", ["--devices", "D", "--config", "MISSING"], "D", None),
    ("config-dir", ["--devices", "D", "--config", "DIR"], "D", None),
    ("devices-dir", ["--devices", "DIR", "--config", "C0"], None, None),
    ("devices-fifo", ["--devices", "FIFO", "--config", "C0"], None, None),
    ("devices-devnull", ["--devices", "/dev/null", "--config", "C0"], None, None),
    ("stdin-dump", ["--devices", "-", "--config", "C0"], "STDIN", None),
    ("stdin-too-large", ["--devices", "-", "--config", "C0"], "BIGSTDIN", None),
    ("dump-too-large", ["--devices", "BIG", "--config", "C0"], None, None),
    ("dump-deep", ["--devices", "DEEP", "--config", "C0"], None, None),
    ("dump-no-mice", ["--devices", "NOMICE", "--config", "C0"], None, None),
    ("dump-list", ["--devices", "LIST", "--config", "C0"], None, None),
    ("dump-bad-utf8", ["--devices", "BADUTF", "--config", "C0"], None, None),
    ("config-too-large", ["--devices", "D", "--config", "BIGC"], "D", None),
    ("two-configs", ["--devices", "D", "--config", "C0", "--config", "C1"], "D", None),
    ("symlink-config", ["--devices", "D", "--config", "LINK"], "D", None),
]


def file_level(ref_path, var_path, work):
    d = tempfile.mkdtemp(dir=work)
    D = os.path.join(d, "devices.json")
    open(D, "wb").write(dump([kb("k", "br")], [mouse("m")]))
    C0 = os.path.join(d, "c0.conf")
    open(C0, "w").write("input {\n  kb_layout = br\n}\n")
    C1 = os.path.join(d, "c1.conf")
    open(C1, "w").write("device {\n  name = k\n  kb_options = x\n}\n")
    os.makedirs(os.path.join(d, "adir"))
    FIFO = os.path.join(d, "fifo")
    os.mkfifo(FIFO)
    BIG = os.path.join(d, "big.json")
    open(BIG, "wb").write(BIG_DUMP)
    DEEP = os.path.join(d, "deep.json")
    open(DEEP, "wb").write(b"[" * 100000)
    NOMICE = os.path.join(d, "nomice.json")
    open(NOMICE, "wb").write(b'{"keyboards": []}')
    LIST = os.path.join(d, "list.json")
    open(LIST, "wb").write(b"[]")
    BADUTF = os.path.join(d, "badutf.json")
    open(BADUTF, "wb").write(b'{"keyboards": [], "mice": [], "x": "\xff"}')
    BIGC = os.path.join(d, "big.conf")
    open(BIGC, "w").write(BIG_CONFIG)
    LINK = os.path.join(d, "link.conf")
    os.symlink(C0, LINK)
    names = {"D": D, "C0": C0, "C1": C1, "DIR": os.path.join(d, "adir"), "FIFO": FIFO, "BIG": BIG,
             "DEEP": DEEP, "NOMICE": NOMICE, "LIST": LIST, "BADUTF": BADUTF, "BIGC": BIGC, "LINK": LINK,
             "MISSING": os.path.join(d, "nope"), "D2": os.path.join(d, "d2.json")}
    results = []
    for label, argv, stdin_kind, _ in FILE_CASES:
        args = [names.get(a, a) if a in names else a for a in argv]
        data = None
        if stdin_kind == "STDIN":
            data = open(D, "rb").read()
        elif stdin_kind == "BIGSTDIN":
            data = BIG_DUMP
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": d}
        r = []
        for tool in (ref_path, var_path):
            try:
                p = subprocess.run([sys.executable, "-I", tool] + args, input=data, capture_output=True,
                                   env=env, timeout=10, cwd=d)
                r.append((p.returncode, p.stdout, p.stderr != b""))
            except subprocess.TimeoutExpired:
                r.append(("timeout", b"", False))
        results.append((label, r[0], r[1]))
    return results


def main():
    os.makedirs(VDIR, exist_ok=True)
    ref = load(REF_PATH, "ref")
    fx, skipped = fixture_cases()
    gen = generated_cases(ref)
    hand = hand_cases()
    corpus = fx + gen + hand
    print("corpus: fixtures=%d generated=%d hand=%d total=%d (file-level fixtures: %s)"
          % (len(fx), len(gen), len(hand), len(corpus), skipped))
    base = [out(ref, d, t) for _, d, t in corpus]
    only = sys.argv[1:] or None
    for vid, old, new in VARIANTS:
        if only and not any(vid.startswith(o) for o in only):
            continue
        src = open(REF_PATH, encoding="utf-8").read()
        if old:
            if src.count(old) != 1:
                raise SystemExit("anchor not unique (%d): %r" % (src.count(old), old[:70]))
            src = src.replace(old, new)
        p = os.path.join(VDIR, vid + ".py")
        open(p, "w", encoding="utf-8").write(src)
        mod = load(p, vid.replace("-", "_"))
        runs = [out(mod, d, t) for _, d, t in corpus]
        diffs = [i for i, (a, b) in enumerate(zip(base, runs)) if a != b]
        print("\n== %s: %s (%d/%d cases differ)" % (vid, "LIVE" if diffs else "NO-DIFF", len(diffs), len(corpus)))
        for i in diffs[:3]:
            lab, d, t = corpus[i]
            print("   witness %s\n     cfg=%r\n     ref=%r\n     var=%r"
                  % (lab, t, base[i], runs[i]))
        if not diffs:
            fl = file_level(REF_PATH, p, os.path.dirname(VDIR))
            fdiff = [(lab, a, b) for lab, a, b in fl if a != b]
            print("   file-level: %d/%d differ" % (len(fdiff), len(fl)))
            for lab, a, b in fdiff[:3]:
                print("     witness %s ref=%r var=%r" % (lab, a, b))


if __name__ == "__main__":
    main()
