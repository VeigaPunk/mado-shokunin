#!/usr/bin/env python3
"""Differential run: the reference tool (l1-draft/mado-monitors.py) vs the Hyprland model (model.py).

Compares, per generated config file:
  * the final rule list (selector, disabled, resolution, refresh rate, offset, scale, transform, mirror)
  * which rule each synthetic output gets (MonitorRuleManager::get)
Flags a config as MASKED when the tool itself declined to compare (unsupported > 0), and reports the
divergences on modelled lines as contract bugs.

Usage: python3 diff.py [--seed 45] [--configs 3600] [--out receipts]
"""
import argparse
import importlib.util
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
TOOL_PATH = os.path.join(LANE, ".ufo", "waves", "round-45", "l1-draft", "mado-monitors.py")
AUTO = -2147483647

sys.path.insert(0, HERE)
import model as M  # noqa: E402


def load_tool():
    spec = importlib.util.spec_from_file_location("mado_monitors_ref", TOOL_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TOOL = load_tool()

# A synthetic host: three outputs. Live values are irrelevant to rule *assignment*, which is what this
# run compares; they are plausible so the tool's comparison path stays exercised.
DUMPS = [
    {"id": 0, "name": "DP-1", "description": "Dell Inc. U3415W X1", "width": 3440, "height": 1440,
     "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": False,
     "mirrorOf": "none"},
    {"id": 1, "name": "DP-2", "description": "Dell Inc. U34", "width": 1920, "height": 1080,
     "refreshRate": 60.0, "x": 3440, "y": 0, "scale": 1, "transform": 0, "disabled": False,
     "mirrorOf": "none"},
    {"id": 2, "name": "eDP-1", "description": "BOE 0x095F", "width": 2880, "height": 1920,
     "refreshRate": 120.0, "x": 0, "y": 0, "scale": 1.6, "transform": 0, "disabled": False,
     "mirrorOf": "none"},
]
MDUMPS = [{"name": d["name"], "desc_short": d["description"], "desc_long": ""} for d in DUMPS]
MONS_BYTES = json.dumps(DUMPS).encode()

# Each pool entry is (text, modelled_by_tool): the modelled profile keeps only True entries, so a
# divergence found there cannot be excused as "the tool said unsupported".
SELS = [
    ("", True), ("DP-1", True), ("DP-2", True), ("eDP-1", True), ("HDMI-A-1", True), ("DP-3", True),
    ("desc:Dell Inc. U34", True), ("desc:Dell Inc. U3415W X1", True), ("desc:", True),
    ("desc: Samsung", True), ("dp-1", True), ("DP-1 ", True), ("desc: BOE", True),
    ("desc: Dell Inc. U3415W X1 ", True), ("DP-1\t", True), ("DP-1\r", False),
]
MODES = [
    ("", True), ("preferred", True), ("pref", True), ("highrr", True), ("highres", True),
    ("maxwidth", True), ("1920x1080", True), ("3440x1440@100", True), ("2560x1440@59.94", True),
    ("1920x1080@60", True), ("0x0", True), ("0x1440", True), ("1920x0", True), ("1x1", True),
    ("1280x720@144", True), ("3840x2160@120", True), ("1920x1080@59.940", True),
    ("12345x12345", True), ("00001x00001", True), ("preferredx", True),
    ("modeline 419.00 3440 3448 3520 3680 1440 1443 1448 1481 +hsync -vsync", True),
    ("MODELINE 419.00 3440 3448 3520 3680 1440 1443 1448 1481", True),
    ("modeline 419.00 3440", True),
    ("1920X1080", False), ("1920x1080@1000", False), ("1920x1080@", False), ("-1x-1", False),
    ("1920x1080@59.9999", False), ("1920x1080 \t", False),
]
POSES = [
    ("", True), ("auto", True), ("auto-left", True), ("auto-up", True), ("auto-center-right", True),
    ("auto-center-down", True), ("0x0", True), ("-1920x0", True), ("3440x0", True),
    ("1920x-1000", True), ("000001x000002", True), ("autofoo", True),
    ("0y0", False), ("10x0abc", False), ("+10x+20", False), ("1x", False), ("x1", False),
]
SCALES = [
    ("", True), ("auto", True), ("1", True), ("1.25", True), ("1.5", True), ("1.6", True),
    ("2", True), ("0.5", True), ("0.2", True), ("0.2499", True), ("10", True), ("1.0000", True),
    ("1.3333", True), ("01.5", True), ("00", True), ("0", True), ("0.25", True), ("99.99", True),
    ("1.", False), ("1.2345678", False), (".5", False), ("1.5x", False), ("-1", False),
]
KEYS = [
    ("", True), ("mirror DP-1", True), ("mirror DP-2", True), ("mirror", True), ("bitdepth 10", True),
    ("bitdepth 8", True), ("cm srgb", True), ("cm hdr", True), ("sdrsaturation 1.2", True),
    ("sdrbrightness 0.9", True), ("transform 1", True), ("transform 3", True), ("transform 03", True),
    ("transform 9", True), ("vrr 1", True), ("vrr -1", True), ("vrr 0", True), ("icc /tmp/x.icc", True),
    ("wat 1", True), ("mirror DP-1, transform 2", True), ("vrr", True), ("transform", True),
    ("bitdepth 10, cm srgb", True), ("cm srgb, vrr 1, bitdepth 10", True),
    ("mirror , transform 2", True), ("TRANSFORM 1", True), ("mirror dp-1", True),
    ("vrr\r", False), ("mirror DP-1\t", True),
]
MODS = [
    ("disable", True), ("disabled", True), ("transform, 3", True), ("transform, 03", True),
    ("transform, 007", True), ("transform, 3.0", True), ("transform, +3", True), ("transform, 9", True),
    ("transform,", True), ("addreserved, 10, 0, 0, 0", True), ("addreserved, +5, 0, 0, 0", True),
    ("addreserved, 1.5, 0, 0, 0", True), ("addreserved, 0x10, 0, 0, 0", True),
    ("addreserved, 10abc, 0, 0, 0", True), ("addreserved, 10", True), ("addreserved, , , ,", True),
    ("addreserved, 99999999999, 0, 0, 0", True), ("addreserved, -0, 0, 0, 0", True),
    ("transform, 99999999999", True),
]
COMMENTS = [("", True), ("", True), ("", True), (" # main", True), (" ## note", False),
            (" # $x", False), ("#all", True)]
LHS_SEPS = [" = ", "=", "\t=\t", " =", "= "]


def pick(rng, pool, modelled_only):
    if modelled_only:
        ok = [v for v, good in pool if good]
        return rng.choice(ok)
    return rng.choice(pool)[0]


def clean_ok(value):
    """Constructs the four known divergence classes are removed for the 'clean' profile."""
    low = value.lower()
    if low.startswith("modeline"):
        return False
    if value.startswith("addreserved"):
        return False
    if value.startswith("transform,"):
        return False
    return True


KEYSET = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")


def keys_ok(value):
    """True when every key/value pair in a key field is one the tool models."""
    for pair in value.split(","):
        f = pair.strip(" \t").split()
        if not f:
            continue
        if f[0] not in KEYSET:
            return False
        if f[0] == "transform" and not (len(f) == 2 and len(f[1]) == 1 and f[1] in "01234567"):
            return False
    return True


def gen_line(rng, modelled_only=False, clean=False):
    lhs = "monitor"
    if not modelled_only and rng.random() < 0.03:
        lhs = "monitorv2"
    while True:
        sel = pick(rng, SELS, modelled_only)
        if not clean or clean_ok(sel):
            break
    if lhs == "monitorv2":
        body = " {"
    elif rng.random() < 0.30:
        while True:
            mod = pick(rng, MODS, modelled_only)
            if not clean or clean_ok(mod):
                break
        body = "%s, %s" % (sel, mod)
    else:
        while True:
            mode = pick(rng, MODES, modelled_only)
            pos = pick(rng, POSES, modelled_only)
            sca = pick(rng, SCALES, modelled_only)
            if not clean or (clean_ok(mode) and clean_ok(pos) and clean_ok(sca)):
                break
        shape = rng.random()
        if shape < 0.04:
            body = sel
        elif shape < 0.08:
            body = "%s, %s" % (sel, mode)
        elif shape < 0.12:
            body = "%s, %s, %s" % (sel, mode, pos)
        else:
            body = "%s, %s, %s, %s" % (sel, mode, pos, sca)
            while True:
                keys = pick(rng, KEYS, modelled_only)
                if not clean or keys_ok(keys):
                    break
            if keys:
                body += (" " if body.endswith(",") else ", ") + keys
            if rng.random() < 0.05:
                body += ","
            if rng.random() < 0.03:
                body += ", ,"
    line = lhs + rng.choice(LHS_SEPS) + body + pick(rng, COMMENTS, modelled_only)
    eol = "\n" if clean else ("\r\n" if rng.random() < (0.02 if modelled_only else 0.08) else "\n")
    return line + eol


def gen_configs(n, rng, modelled_only=False, clean=False):
    out = []
    for i in range(n):
        if i % 6 == 5:
            k = rng.randint(2, 6)
            cfg = "".join(gen_line(rng, modelled_only, clean) for _ in range(k))
        else:
            cfg = gen_line(rng, modelled_only, clean)
        out.append(cfg)
    return out


# ------------------------------------------------------------------ comparison --

_TAIL = re.compile(r"^ mode=(\S+) pos=(\S+) scale=(\S+) transform=(\d+)$")
_DEC = json.JSONDecoder()


def parse_tool(lines):
    """Return (rules_canon, rule_sels, assignments, counts)."""
    rules, sels, assigns = [], [], []
    counts = {}
    for line in lines:
        if line.startswith("MADO_MON_RULE: "):
            i = line.index(" sel=") + 5
            sel, end = _DEC.raw_decode(line[i:])
            rest = line[i + end:]
            mi = rest.index(" mirror=") + 8
            if rest[mi:mi + 1] == '"':
                mirror, mend = _DEC.raw_decode(rest[mi:])
            else:
                mirror, mend = "", 1
            head = rest[:mi - 8]
            tail = rest[mi + mend:].strip()
            m = _TAIL.match(head)
            if not m or not tail.startswith("disabled="):
                raise SystemExit("unparsable rule line: %r" % line)
            mode, pos, scale, transform = m.groups()
            disabled = tail[len("disabled="):]
            if mode == "preferred":
                res, rate = (0, 0), 60.0
            elif mode == "highrr":
                res, rate = (-1, -1), 60.0
            elif mode == "highres":
                res, rate = (-1, -2), 60.0
            elif mode == "maxwidth":
                res, rate = (-1, -3), 60.0
            elif mode == "modeline":
                res, rate = "MODELINE", None
            else:
                w, h, r = re.fullmatch(r"(\d+)x(\d+)@([0-9.]+)", mode).groups()
                res, rate = (int(w), int(h)), float(r)
            if pos == "auto":
                off = (AUTO, AUTO)
            else:
                x, y = pos.split("x")
                off = (int(x), int(y))
            sc = -1.0 if scale == "auto" else float(scale)
            rules.append((sel, disabled == "true", res[0], res[1], rate, off[0], off[1], sc,
                          int(transform), mirror))
            sels.append(sel)
        elif line.startswith("MADO_MON_OUTPUT: "):
            i = line.index(" name=") + 6
            name, end = _DEC.raw_decode(line[i:])
            m = re.match(r"^ rule=(-|\d+) differ=(\S+) verdict=(\S+)$", line[i + end:])
            assigns.append(None if m.group(1) == "-" else int(m.group(1)))
        elif line.startswith("MADO_MONITORS: "):
            counts = dict(kv.split("=") for kv in line[len("MADO_MONITORS: "):].split(" "))
    return rules, sels, assigns, counts


def cmp_rule(t, m):
    """Compare one tool rule canon against one model canon; returns a field name or None."""
    tsel, tdis, tw, th, trate, tx, ty, tsc, ttr, tmir = t
    msel, mdis, mw, mh, mrate, mx, my, msc, mtr, mmir = m
    if tsel != msel:
        return "selector"
    if tdis != mdis:
        return "disabled"
    if (tw, th) != (mw, mh):
        return "mode"
    if trate is not None and mrate is not None and abs(trate - mrate) > 0.0051:
        return "rate"
    if (tx, ty) != (mx, my):
        return "position"
    if abs(tsc - (msc if msc > -1 else -1.0)) > 1e-4 and not (tsc == -1.0 and msc < 0):
        return "scale"
    if ttr != mtr:
        return "transform"
    if tmir != mmir:
        return "mirror"
    return None


def compare(cfg):
    """Return dict(divergences=[...], masked=bool, counts=..., unsupported lines)."""
    lines, rc = TOOL.report(MONS_BYTES, [cfg])
    trules, tsels, tassign, counts = parse_tool(lines)
    mrules, massign, unmodelled, escapes = M.simulate([cfg], MDUMPS)
    mcanon = [r.canon() for r in mrules]
    div = []
    if len(trules) != len(mcanon):
        div.append(("rule_count", "tool=%d model=%d" % (len(trules), len(mcanon)),
                    [r for r in trules], mcanon))
    else:
        for k, (t, m) in enumerate(zip(trules, mcanon), 1):
            f = cmp_rule(t, m)
            if f:
                div.append(("rule%d.%s" % (k, f), json.dumps(t) + " vs " + json.dumps(m), None, None))
    for k, (t, m) in enumerate(zip(tassign, massign)):
        if t != m[0]:
            div.append(("assign[%s]" % DUMPS[k]["name"], "tool=%s model=%s" % (t, m[0]), None, None))
    return {"div": div, "masked": counts.get("unsupported", "0") != "0",
            "unsupported": int(counts.get("unsupported", 0)), "lines": int(counts.get("lines", 0)),
            "counts": counts, "rc": rc, "escapes": escapes, "raw": lines}


TEMPLATES = {
    "mode": "monitor = DP-1, {v}, 0x0, 1\n",
    "pos": "monitor = DP-1, 3440x1440@100, {v}, 1\n",
    "scale": "monitor = DP-1, 3440x1440@100, 0x0, {v}\n",
    "key": "monitor = DP-1, 3440x1440@100, 0x0, 1, {v}\n",
    "comment": "monitor = DP-1, 3440x1440@100, 0x0, 1{v}\n",
    "selector": "monitor = {v}, 3440x1440@100, 0x0, 1\n",
    "modifier-new": "monitor = DP-1, {v}\n",
    "modifier-existing": "monitor = DP-1, 1920x1080, 0x0, 1\nmonitor = DP-1, {v}\n",
}
POOLS = (("selector", SELS), ("mode", MODES), ("pos", POSES), ("scale", SCALES),
         ("key", KEYS), ("comment", COMMENTS),
         ("modifier-new", MODS), ("modifier-existing", MODS))


def probe_families(path):
    """One construct per line: does the tool decline it, and do the two models agree?"""
    rows = []
    for fam, pool in POOLS:
        for value, modelled in pool:
            cfg = TEMPLATES[fam].format(v=value)
            r = compare(cfg)
            rows.append((fam, value, modelled, r["unsupported"], len(r["div"]),
                         r["counts"].get("rules"), r["counts"].get("badrules")))
    out = ["# one construct per line: tool decision vs model, per pool value",
           "family\tvalue\tpool_modelled\ttool_unsupported\tdivergences\ttool_rules\ttool_badrules"]
    for fam, value, modelled, unsup, ndiv, rules, bad in rows:
        out.append("%s\t%s\t%s\t%d\t%d\t%s\t%s"
                   % (fam, json.dumps(value), modelled, unsup, ndiv, rules, bad))
    diverging = [r for r in rows if r[4] and not r[3]]
    out.append("")
    out.append("rows=%d  tool declined (unsupported)=%d  divergences-with-tool-comparing=%d"
               % (len(rows), sum(1 for r in rows if r[3]), len(diverging)))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=45)
    ap.add_argument("--configs", type=int, default=3600)
    ap.add_argument("--out", default=os.path.join(HERE, "receipts"))
    ap.add_argument("--profile", choices=("stress", "modelled", "clean"), default="stress")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rng = random.Random(args.seed)
    cfgs = gen_configs(args.configs, rng, args.profile in ("modelled", "clean"), args.profile == "clean")

    total_div_unmasked = 0
    total_div_masked = 0
    unsupported_cfgs = 0
    unsupported_lines = 0
    total_lines = 0
    unmasked_examples = {}
    masked_examples = {}
    agree_cfgs = 0
    escapes = []
    report_lines = ["# differential run: reference tool vs model", "profile=%s seed=%d configs=%d"
                        % (args.profile, args.seed, len(cfgs)), ""]
    for idx, cfg in enumerate(cfgs):
        r = compare(cfg)
        total_lines += r["lines"]
        unsupported_lines += r["unsupported"]
        if r["unsupported"]:
            unsupported_cfgs += 1
        if r["escapes"]:
            escapes.append((cfg, r["escapes"]))
        if not r["div"]:
            agree_cfgs += 1
            continue
        bucket = masked_examples if r["masked"] else unmasked_examples
        key = tuple(sorted(set(d[0] for d in r["div"])))
        bucket.setdefault(key, []).append((cfg, r))
        if r["masked"]:
            total_div_masked += 1
        else:
            total_div_unmasked += 1

    report_lines.append("configs=%d  tool+model agree=%d  diverge=%d (modelled lines=%d, masked=%d)"
                        % (len(cfgs), agree_cfgs, total_div_unmasked + total_div_masked,
                           total_div_unmasked, total_div_masked))
    report_lines.append("tool lines=%d unsupported=%d  unsupported share=%.4f  configs with an unmodelled line=%d"
                        % (total_lines, unsupported_lines,
                           (unsupported_lines / total_lines) if total_lines else 0.0, unsupported_cfgs))
    report_lines.append("model exceptions escaping the handler=%d" % len(escapes))
    report_lines.append("")
    for label, bucket in (("CONTRACT BUG CANDIDATES (tool compared, result differs)", unmasked_examples),
                          ("MASKED (tool said NOT_COMPARED; recorded for completeness)", masked_examples)):
        report_lines.append("== %s ==" % label)
        for key, items in sorted(bucket.items(), key=lambda kv: -len(kv[1])):
            report_lines.append("-- %d configs, fields %s" % (len(items), ",".join(key)))
            for cfg, r in items[:4]:
                report_lines.append("   config=%s" % json.dumps(cfg))
                for d in r["div"]:
                    report_lines.append("     %s: %s" % (d[0], d[1]))
                for line in r["raw"]:
                    report_lines.append("     tool| %s" % line)
            report_lines.append("")
    for cfg, esc in escapes[:10]:
        report_lines.append("ESCAPE config=%s %s" % (json.dumps(cfg), esc))
    with open(os.path.join(args.out, "diverge.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(report_lines) + "\n")

    summary = {
        "seed": args.seed,
        "configs": len(cfgs),
        "agree": agree_cfgs,
        "diverge_unmasked": total_div_unmasked,
        "diverge_masked": total_div_masked,
        "tool_lines": total_lines,
        "tool_unsupported": unsupported_lines,
        "unsupported_share": round(unsupported_lines / total_lines, 4) if total_lines else None,
        "configs_with_unmodelled_line": unsupported_cfgs,
        "escapes": len(escapes),
        "unmasked_classes": {"|".join(k): len(v) for k, v in unmasked_examples.items()},
        "masked_classes": {"|".join(k): len(v) for k, v in masked_examples.items()},
    }
    summary["profile"] = args.profile
    with open(os.path.join(args.out, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")
    probe_families(os.path.join(args.out, "families.txt"))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
