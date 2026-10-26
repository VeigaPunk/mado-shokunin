#!/usr/bin/env python3
"""Source-closure census for the host's Hyprland window rules (read-only).

Walks `source =` directives from ~/.config/hypr/hyprland.conf (globs expanded by
the shell-free glob module), then reports for every file in the closure:
  * the number of lines matching the tool's RULE_LINE (`windowrule[ \t]*=(.*)`)
  * how the reference tool counts them (rules / float_rules / other / unsupported)
  * for every unsupported size/float line, the reason, derived from the frozen
    tool docstring's conditions and ASSERTED to agree with the tool's own count
    on that line alone.

Usage: source-census.py <reference-tool.py>
"""
import glob
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, ".config/hypr/hyprland.conf")
SOURCE_RE = re.compile(r"^[ \t]*source[ \t]*=[ \t]*(.+?)[ \t]*$")


def expand(path):
    path = path.strip().strip('"')
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.join(HOME, ".config/hypr"), path)
    hits = sorted(glob.glob(path))
    return hits if hits else [path]


def closure(root):
    seen, order, queue = set(), [], [root]
    while queue:
        p = queue.pop(0)
        rp = os.path.realpath(p)
        if rp in seen:
            continue
        seen.add(rp)
        order.append(p)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        for line in text.split("\n"):
            m = SOURCE_RE.match(line.strip())
            if m:
                for t in expand(m.group(1)):
                    queue.append(t)
    return order


def load_tool(path):
    spec = importlib.util.spec_from_file_location("refgeo", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def reason(tool, line):
    """Return the docstring condition that makes this size/float line unsupported."""
    stripped = line.strip(" \t")
    m = tool.RULE_LINE.fullmatch(stripped)
    if not m:
        return "not-a-rule-line"
    fields = [f.strip(" \t") for f in m.group(1).split(",")]
    toks = [t for t in re.split("[ \t]+", fields[0]) if t]
    effect = toks[0] if toks else ""
    if effect not in ("size", "float"):
        return "effect-not-size-or-float"
    if len(fields) != 2:
        return "field-count=%d (needs exactly 2: effect + one match:)" % len(fields)
    args = toks[1:]
    if effect == "size":
        if len(args) != 2:
            return "size arg-token-count=%d (needs 2)" % len(args)
        for a in args:
            if not tool.NUM.fullmatch(a):
                return "size arg %r not [0-9]{1,5}" % a
    else:
        if len(args) != 1 or args[0] not in ("on", "off"):
            return "float args %r not exactly one of on|off" % (args,)
    mm = tool.MATCH_FIELD.fullmatch(fields[1])
    if not mm:
        return "field[1] not 'match:class <regex>' (match kind " + repr(fields[1].split(" ")[0] if fields[1] else "") + ")"
    rx = mm.group(1)
    if "(?" in rx:
        return "regex contains '(?' (no inline flags/groups)"
    for bad in ("*+", "++", "?+"):
        if bad in rx:
            return "regex contains possessive quantifier %r" % bad
    if not tool.SAFE.fullmatch(rx):
        return "regex outside the restricted alphabet (len=%d) or >200 chars" % len(rx)
    try:
        re.compile(rx)
    except re.error:
        return "regex does not compile under Python re"
    return "SUPPORTED"


def main():
    if len(sys.argv) != 2:
        print("usage: source-census.py <ref-tool.py>", file=sys.stderr)
        return 2
    tool = load_tool(sys.argv[1])
    files = closure(ROOT)
    print("# closure of %s: %d files (order = source order, dedup by realpath)" % (ROOT, len(files)))
    total = {"rules": 0, "float_rules": 0, "other": 0, "unsupported": 0}
    size_lines = 0
    rows = []
    for path in files:
        exists = os.path.isfile(path)
        print("FILE %s %s" % ("ok" if exists else "MISSING", path))
        if not exists:
            continue
        text = open(path, "r", encoding="utf-8", errors="replace").read()
        lines = text.split("\n")
        want = 0
        for line in lines:
            if tool.RULE_LINE.fullmatch(line.strip(" \t")):
                want += 1
        # tool's own count for this file alone
        with tempfile.NamedTemporaryFile("w", suffix=".conf", delete=False) as tf:
            tf.write(text)
            tmp = tf.name
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as jf:
            jf.write("[]")
            jtmp = jf.name
        out = subprocess.run([sys.executable, "-I", sys.argv[1], "--clients", jtmp, "--rules", tmp],
                             capture_output=True, text=True)
        os.unlink(tmp)
        os.unlink(jtmp)
        tail = [l for l in out.stdout.split("\n") if l.startswith("MADO_GEOMETRY:")]
        if not tail:
            print("  ERROR rc=%d stderr=%r" % (out.returncode, out.stderr))
            continue
        counts = dict(re.findall(r"(\w+)=(-?\d+)", tail[0]))
        counts = {k: int(v) for k, v in counts.items() if k != "verdict"}
        for k in total:
            total[k] += counts[k]
        rule_lines = want
        print("  RULE_LINES=%d rules=%d float_rules=%d other=%d unsupported=%d covered=%d residual=%d" % (
            rule_lines, counts["rules"], counts["float_rules"], counts["other"], counts["unsupported"],
            counts["rules"] + counts["float_rules"] + counts["other"] + counts["unsupported"],
            rule_lines - (counts["rules"] + counts["float_rules"] + counts["other"] + counts["unsupported"])))
        for idx, line in enumerate(lines, 1):
            if not tool.RULE_LINE.fullmatch(line.strip(" \t")):
                continue
            why = reason(tool, line)
            if re.match(r"^windowrule[ \t]*=[ \t]*size\b", line.strip(" \t")):
                size_lines += 1
            if why == "SUPPORTED":
                continue
            # assert the tool agrees this very line alone is unsupported/other
            with tempfile.NamedTemporaryFile("w", suffix=".conf", delete=False) as tf:
                tf.write(line + "\n")
                tmp = tf.name
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as jf:
                jf.write("[]")
                jtmp = jf.name
            one = subprocess.run([sys.executable, "-I", sys.argv[1], "--clients", jtmp, "--rules", tmp],
                                 capture_output=True, text=True)
            os.unlink(tmp)
            os.unlink(jtmp)
            one_tail = [l for l in one.stdout.split("\n") if l.startswith("MADO_GEOMETRY:")]
            oc = dict(re.findall(r"(\w+)=(-?\d+)", one_tail[0])) if one_tail else {}
            toolclass = "other" if oc.get("other") == "1" else ("unsupported" if oc.get("unsupported") == "1" else "SUPPORTED")
            mine = "other" if why == "effect-not-size-or-float" else "unsupported"
            print("  L%d class=%s reason=%s tool=%s agree=%s :: %s" % (
                idx, mine, why, toolclass, mine == toolclass, line.strip(" \t")))
            rows.append((path, idx, mine, toolclass, mine == toolclass))
    print("TOTAL rules=%d float_rules=%d other=%d unsupported=%d" % (
        total["rules"], total["float_rules"], total["other"], total["unsupported"]))
    print("TOTAL windowrule size lines in closure=%d supported_size=%d" % (
        size_lines, total["rules"]))
    bad = [r for r in rows if not r[4]]
    print("CLASSIFIER_AGREEMENT: %d/%d disagree=%d" % (len(rows) - len(bad), len(rows), len(bad)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
