#!/usr/bin/env python3
"""Differential mutation harness for the C1 reference contract (scratch only)."""
import importlib.util
import json
import random
import sys

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
CTR = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r45-monitors.py"
SRC = open(REF, encoding="utf-8").read()


def load(src, tag):
    ns = {"__name__": "m_" + tag}
    exec(compile(src, "<%s>" % tag, "exec"), ns)
    return ns


def out(ns, texts, raw):
    try:
        lines, rc = ns["report"](raw, texts)
        return ("\n".join(lines), rc)
    except Exception as e:  # noqa: BLE001 - a crash is an observable output
        return ("EXC:%s:%s" % (type(e).__name__, e), -1)


spec = importlib.util.spec_from_file_location("ctr", CTR)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)
TABLE = ctr.names(45)

CASES = []  # (label, [config texts], dump bytes)


def add(label, texts, dump):
    raw = dump if isinstance(dump, bytes) else json.dumps(dump).encode()
    CASES.append((label, texts, raw))


for fx in ctr.FIXTURES:
    label, configs, dump, stdin, expect, rc = fx
    texts = [ctr.subst(t, TABLE) for t in configs] if isinstance(configs, list) else []
    add("fx:" + label, texts, ctr.subst(dump, TABLE) if not isinstance(dump, bytes) else dump)

M = ctr.M
A = TABLE["{A}"]
B = TABLE["{B}"]

# ---- targeted families -------------------------------------------------
for v2 in ["monitorv2{", "monitorv2 {", "monitorv2=1", "monitorv2", "monitorv2foo",
           "monitorv2\t{", "  monitorv2  {", "monitorv2x{", "Monitorv2 {", "monitorv2,"]:
    add("v2:" + repr(v2), [v2 + "\nmonitor = %s, 1x1@60, 0x0, 1\n" % A], [M(A)])
for mo in ["modeline", "MODELINE", "Modeline", "modelines", "modeline 1 2 3", "modelineX",
           "modeline\tfoo", "\x0cmodeline", "MODELINE 1 2"]:
    add("mode:" + repr(mo), ["monitor = %s, %s, 0x0, 1\n" % (A, mo)], [M(A)])
for ws in ["\r", "\x0b", "\xa0", "\x1c"]:
    add("ws-mode:" + repr(ws), ["monitor = %s, %s\n" % (A, ws)], [M(A)])
    add("ws-field1:" + repr(ws), ["monitor = %s,%s\n" % (A, ws)], [M(A)])
for sel in ["desc:", "desc: ", "desc: Dell", "desc:Dell", "desc:  Dell", "desc:Dell Inc.",
            "desc: Dell Inc. ", "desc:\tDell"]:
    for desc in ["", "Dell", "Dell Inc. U3415W", "X Dell"]:
        add("desc:%r/%r" % (sel, desc), ["monitor = %s, 1x1@60, 0x0, 1\n" % sel], [M(A, desc=desc)])
# mirror plane
for mid, mo, present, mrule in [
        (4, "4", True, A), (4, 4, True, A), ("4", "4", True, A), (4, None, True, A),
        (4, "4", False, A), (True, "true", True, A), (0, "0", True, A), (4.0, "4.0", True, A),
        (4, "5", True, A)]:
    mons = [M(A, mid=mid)]
    if present:
        mons.append(M(B, mid=9))
    add("mirror:%r/%r/p%s" % (mid, mo, present),
        ["monitor = %s, 1x1@60, 0x0, 1, mirror, %s\n" % (B if present else A, B if present else "NOPE")], mons)
# scale/search plane
for sc in ["0.25", "0.2499", "0.2", "1.3", "1.6", "1.25", "2", "99.999999", "1.3333", "0.5", "1.0000001"]:
    for w, h in [(3440, 1440), (1920, 1080), (2880, 1920), (1, 1), (7, 3), (2560, 1440),
                 (0, 0), (-4, 4), (100, 100), (67, 67), (999, 1000), (7680, 4320)]:
        for live in ["1.0", "1.25", "1.3", "1.33333333", "1.6", "0.5", "2.0"]:
            add("scale:%s/%dx%d/%s" % (sc, w, h, live),
                ["monitor = %s, 1000x1000@60, 0x0, %s\n" % (A, sc)],
                [dict(M(A), w=w, h=h, scale=float(live))])
# rate plane
for rate in ["100", "99.997", "999.999", "60.000", "143.912", "144"]:
    for rr in [99.0, 99.997, 100.0, 100.999, 100.99901, 999.999, 999.9990234375, 1001.0,
               True, "100", None, 59.99]:
        add("rate:%s/%r" % (rate, rr), ["monitor = %s, 1000x1000@%s, 0x0, 1\n" % (A, rate)],
            [dict(M(A), rr=rr)])
# type / big-int plane
for key, val in [("width", 10 ** 400), ("refreshRate", 10 ** 400), ("scale", 10 ** 400),
                 ("x", 10 ** 400), ("transform", True), ("width", 0), ("height", 0),
                 ("name", 5), ("description", 5), ("mirrorOf", 0), ("id", "0")]:
    add("type:%s=%r" % (key, val), ["monitor = %s, 1000x1000@60, 0x0, 1.25\n" % A],
        [dict(M(A), **{key: val})])

# ---- random corpus ----------------------------------------------------
TOK_SEL = ["", A, B, "DP-9", "desc:" + A, "desc:Dell", "desc: Dell", "$main", "desc:", " "] + [A]
TOK_MODE = ["", "preferred", "pref", "highrr", "highres", "maxwidth", "modeline",
            "modeline 1 2", "modelines", "3440x1440", "3440x1440@100", "3440x1440@99.997",
            "1x1", "0x0", "1920x1080@60.000", "3440x1440@100Hz", "99999x99999@999.999",
            "disable", "disabled", "transform", "addreserved", "auto", "x", "\r", "MODELINE"]
TOK_POS = ["", "auto", "auto-left", "0x0", "-1920x0", "axb", "1000000x0", "0x1", "auto right"]
TOK_SCALE = ["", "auto", "1", "1.25", "1.6", "0.2", "0.25", "0.2499", "99.999999", "0",
             "1.", "1.0000001", "12.345678", "100"]
TOK_KEY = ["mirror", "transform", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "vrr",
           "icc", "wat", "sdr_eotf", "Mirror"]
TOK_VAL = ["0", "1", "2", "3", "7", "8", "9", "10", "", A, B, "1.5", "none"]
TOK_LINE = ["general {", "}", "", "# comment", "monitorv2 {", "monitorv2x = 1",
            "bind = SUPER, Q, killactive", "  monitorv2 {", "monitor = $main, 1x1@60, 0x0, 1"]


def gen_config(rng):
    lines = []
    for _ in range(rng.randint(1, 4)):
        if rng.random() < 0.2:
            lines.append(rng.choice(TOK_LINE))
            continue
        fields = [rng.choice(TOK_SEL), rng.choice(TOK_MODE), rng.choice(TOK_POS), rng.choice(TOK_SCALE)]
        for _ in range(rng.randint(0, 3)):
            fields += [rng.choice(TOK_KEY), rng.choice(TOK_VAL)]
        text = "monitor" + rng.choice([" ", "  ", "\t", ""]) + "=" + rng.choice([" ", ""]) + ", ".join(fields)
        if rng.random() < 0.15:
            text += rng.choice([" # tail", "##double", " $var", " \\esc", "\r"])
        lines.append(text)
    return "\n".join(lines) + rng.choice(["\n", "", "\n\n"])


W = [3440, 1440, 1920, 1080, 2560, 2880, 1920, 0, -5, 1, 7, 100, None]
RR = [59.99, 60.0, 99.997, 100.0, 99.0, 100.999, 144.0, 143.912, None, "100", True]
SC = [1, 1.25, 1.3, 1.33333333, 1.6, 0.0, 2.0, "1", True, None, 0.25, 0.5]
TR = [0, 1, 3, 7, 8, True, "1", None]
MO = ["none", "0", 0, None, "4", A, ""]


def gen_mon(rng, name, mid):
    return {"id": rng.choice([mid, str(mid), mid + 0.0, True, None]),
            "name": rng.choice([name, name, "", 5, None]),
            "description": rng.choice(["", "Dell", "Dell Inc. U3415W", 5, None]),
            "width": rng.choice(W), "height": rng.choice(W), "refreshRate": rng.choice(RR),
            "x": rng.choice([0, 10, -1920, "0", None]), "y": rng.choice([0, 5, "0", None]),
            "scale": rng.choice(SC), "transform": rng.choice(TR),
            "disabled": rng.choice([False, False, True, "true", None]),
            "mirrorOf": rng.choice(MO)}


rng = random.Random(45)
for k in range(2500):
    texts = [gen_config(rng) for _ in range(rng.randint(1, 2))]
    mons = [gen_mon(rng, A, 0)]
    if rng.random() < 0.5:
        mons.append(gen_mon(rng, B, 1))
    add("rnd:%d" % k, texts, mons)

MUT = [
    ("M1-zpos", "    if z > 0 and whole(w / z) and whole(h / z):",
     "    if whole(w / z) and whole(h / z):"),
    ("M2-cand0", "            if cand != 0 and whole(w / cand) and whole(h / cand):",
     "            if whole(w / cand) and whole(h / cand):"),
    ("M3-range90", "    for i in range(1, 90):", "    for i in range(1, 91):"),
    ("M4-order", "        for cand in ((k + i) / 120.0, (k - i) / 120.0):",
     "        for cand in ((k - i) / 120.0, (k + i) / 120.0):"),
    ("M5-mirror-isinstance",
     "        if not (isinstance(mo, str) and len(ids) >= 1 and mo == str(ids[0])):",
     "        if not (len(ids) >= 1 and mo == str(ids[0])):"),
    ("M6-mirror-len", "        if not (isinstance(mo, str) and len(ids) >= 1 and mo == str(ids[0])):",
     "        if not (isinstance(mo, str) and mo == str(ids[0])):"),
    ("M7-mirror-idfilter",
     '        ids = [m.get("id") for m in mons if str_or_empty(m.get("name")) == rule["mirror"] and is_int(m.get("id"))]',
     '        ids = [m.get("id") for m in mons if str_or_empty(m.get("name")) == rule["mirror"]]'),
    ("M8-v2tail", 'V2_RE = re.compile(r"monitorv2(?:[ \\t={]|$)")', 'V2_RE = re.compile(r"monitorv2")'),
    ("M9-v2eq", 'V2_RE = re.compile(r"monitorv2(?:[ \\t={]|$)")',
     'V2_RE = re.compile(r"monitorv2(?:[ \\t{]|$)")'),
    ("M10-v2dollar", 'V2_RE = re.compile(r"monitorv2(?:[ \\t={]|$)")',
     'V2_RE = re.compile(r"monitorv2(?:[ \\t={])")'),
    ("M11-modeline-anyprefix", '    if toks and toks[0] == "modeline":',
     '    if toks and toks[0].startswith("modeline"):'),
    ("M12-toks-guard", '    if toks and toks[0] == "modeline":', '    if toks[0] == "modeline":'),
    ("M13-nolower", "    toks = low.split()", "    toks = value.split()"),
    ("M14-descstrip", '            if desc.startswith(sel[5:].strip(" \\t")):',
     '            if desc.startswith(sel[5:]):'),
    ("M15-emptyskip", '        sel = rules[n - 1]["sel"]\n        if sel == "":\n            continue\n',
     '        sel = rules[n - 1]["sel"]\n'),
    ("M16-norules-v2", '    if counts["lines"] == 0 and counts["v2"] == 0:',
     '    if counts["lines"] == 0:'),
    ("M18-clamp-le", '    rule["scale"] = 1.0 if s < 0.25 else s',
     '    rule["scale"] = 1.0 if s <= 0.25 else s'),
    ("M19-noclamp", '    rule["scale"] = 1.0 if s < 0.25 else s', '    rule["scale"] = s'),
    ("M20-f32rate", '    rule["rate"] = f32(float(m.group(4))) if m.group(4) is not None else 60.0',
     '    rule["rate"] = float(m.group(4)) if m.group(4) is not None else 60.0'),
    ("M21-f32scale", "    s = f32(float(value))", "    s = float(value)"),
    ("M22-f32cand", "                return f32(cand)", "                return cand"),
    ("M23-f32z", "        return f32(z)", "        return z"),
    ("M24-nosreg", "        if not stat.S_ISREG(os.fstat(fd).st_mode):\n            raise Setup(\"unreadable\")\n",
     ""),
    ("M26-isfinite", "    return math.isfinite(x) and x == math.floor(x + 0.5)",
     "    return x == math.floor(x + 0.5)"),
    ("M27-isnum-bool", "    return isinstance(v, (int, float)) and not isinstance(v, bool)",
     "    return isinstance(v, (int, float))"),
    ("M28-isint-bool", "    return isinstance(v, int) and not isinstance(v, bool)",
     "    return isinstance(v, int)"),
    ("M29-transform-len", '    if len(value) == 1 and value in "01234567":', '    if value in "01234567":'),
    ("M30-addreserved-4", "        if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 6)):",
     "        if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 5)):"),
    ("M31a-drop-hash2", '    if "##" in body or "$" in body or "\\\\" in body:',
     '    if "$" in body or "\\\\" in body:'),
    ("M31b-drop-dollar", '    if "##" in body or "$" in body or "\\\\" in body:',
     '    if "##" in body or "\\\\" in body:'),
    ("M31c-drop-backslash", '    if "##" in body or "$" in body or "\\\\" in body:',
     '    if "##" in body or "$" in body:'),
    ("M32-nocommentcut", '    body = body.split("#", 1)[0]', '    body = body'),
    ("M33-scale-digits", 'SCALE_RE = re.compile(r"[0-9]{1,2}(\\.[0-9]{1,6})?")',
     'SCALE_RE = re.compile(r"[0-9]{1,3}(\\.[0-9]{1,6})?")'),
    ("M35-rule-numbering", "    out = [rule_line(n, r) for n, r in enumerate(rules, 1)]",
     "    out = [rule_line(n, r) for n, r in enumerate(rules)]"),
    ("M37-output-name", '            json.dumps(str_or_empty(mon.get("name"))), "-" if n is None else str(n),',
     '            json.dumps(mon.get("name")), "-" if n is None else str(n),'),
    ("M40-empty-mode", '    if value == "" or value.startswith("pref"):',
     '    if value.startswith("pref"):'),
    ("M41-args-dupmon", '        if flag == "--monitors" and monitors is None:',
     '        if flag == "--monitors":'),
]


def witnesses(ns_m, limit=2):
    hits = []
    for label, texts, raw in CASES:
        a = out(REFNS, texts, raw)
        b = out(ns_m, texts, raw)
        if a != b:
            hits.append((label, a, b, texts, raw))
            if len(hits) >= limit:
                break
    return hits


def show(label, texts, raw):
    return "texts=%r dump=%s" % (texts, raw.decode("utf-8", "replace")[:220])


REFNS = load(SRC, "ref")
print("cases=%d" % len(CASES))
for mid, old, new in MUT:
    n = SRC.count(old)
    if n != 1:
        print("%-26s BADPATTERN count=%d" % (mid, n))
        continue
    ns = load(SRC.replace(old, new), mid)
    ws = witnesses(ns)
    if ws:
        label, a, b, texts, raw = ws[0]
        print("%-26s LIVE case=%s\n    ref=%r\n    mut=%r\n    %s" % (mid, label, a, b, show(label, texts, raw)))
        if len(ws) > 1:
            print("    also=%s" % ws[1][0])
    else:
        print("%-26s NO-WITNESS across %d cases" % (mid, len(CASES)))
