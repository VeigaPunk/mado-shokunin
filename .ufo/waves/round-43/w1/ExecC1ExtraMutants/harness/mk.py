import json
import os
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecC1ExtraMutants"
REF = os.path.join(SEAT, "ref.py")
OUT = os.path.join(SEAT, "mutants")

# (name, category, old, new)
MUT = [
    # ---- value-domain edits -------------------------------------------------
    ("N01-stdin-read-plus2", "value-domain", "data = stdin.read(MAX_BYTES + 1)", "data = stdin.read(MAX_BYTES + 2)"),
    ("N02-read-tail-ge", "boundary-shift",
     '    if len(data) > MAX_BYTES:\n        raise Setup("too_large")\n    return data',
     '    if len(data) >= MAX_BYTES:\n        raise Setup("too_large")\n    return data'),
    ("N03-maxbytes-minus1", "wrong-constant", "MAX_BYTES = 1048576", "MAX_BYTES = 1048575"),
    ("N04-num-1-4", "value-domain", 'NUM = re.compile(r"[0-9]{1,5}")', 'NUM = re.compile(r"[0-9]{1,4}")'),
    ("N05-num-1-6", "value-domain", 'NUM = re.compile(r"[0-9]{1,5}")', 'NUM = re.compile(r"[0-9]{1,6}")'),
    ("N06-safe-1-199", "value-domain", '){1,200}")', '){1,199}")'),
    ("N07-safe-2-200", "value-domain", '){1,200}")', '){2,200}")'),
    ("N08-matchfield-star", "value-domain",
     'MATCH_FIELD = re.compile(r"match:class[ \\t]+(.+)")',
     'MATCH_FIELD = re.compile(r"match:class[ \\t]+(.*)")'),
    ("N09-split-maxsplit", "value-domain",
     'fields = [f.strip(" \\t") for f in body.split(",")]',
     'fields = [f.strip(" \\t") for f in body.split(",", 1)]'),
    ("N10-fields-eq3", "wrong-constant", "good = len(fields) == 2", "good = len(fields) == 3"),
    ("N11-float-lower", "value-domain", 'good = len(args) == 1 and args[0] in ("on", "off")',
     'good = len(args) == 1 and args[0].lower() in ("on", "off")'),
    ("N12-float-two-args", "boundary-shift", 'good = len(args) == 1 and args[0] in ("on", "off")',
     'good = len(args) <= 2 and args[0] in ("on", "off")'),
    ("N13-size-first-arg-only", "dropped-check",
     "good = len(args) == 2 and all(NUM.fullmatch(a) for a in args)",
     "good = len(args) == 2 and NUM.fullmatch(args[0])"),
    ("N14-effect-no-default", "dropped-branch", 'effect = toks[0] if toks else ""', "effect = toks[0]"),
    ("N15-effect-add-center", "value-domain", 'if effect not in ("size", "float"):',
     'if effect not in ("size", "float", "center"):'),
    ("N16-line-rstrip-only", "dropped-branch", 'line = raw.strip(" \\t")', 'line = raw.rstrip(" \\t")'),
    ("N17-line-strip-cr", "value-domain", 'line = raw.strip(" \\t")', 'line = raw.strip(" \\t\\r")'),
    ("N18-rule-line-plus", "value-domain",
     'RULE_LINE = re.compile(r"windowrule[ \\t]*=(.*)")',
     'RULE_LINE = re.compile(r"windowrule[ \\t]*=(.+)")'),
    ("N19-rule-line-caret", "value-domain",
     'RULE_LINE = re.compile(r"windowrule[ \\t]*=(.*)")',
     'RULE_LINE = re.compile(r"^windowrule[ \\t]*=(.*)")'),
    # ---- operator swaps -----------------------------------------------------
    ("N20-mapped-eq", "operator-swap", 'if c.get("mapped") is False:', 'if c.get("mapped") == False:'),
    ("N21-floating-eq", "operator-swap", 'floating = c.get("floating") is True',
     'floating = c.get("floating") == True'),
    ("N22-size-gt-minus1", "boundary-shift",
     "isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in s):",
     "isinstance(v, int) and not isinstance(v, bool) and v > -1 for v in s):"),
    ("N23-size-type-is-int", "value-domain",
     "isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in s):",
     "type(v) is int and v >= 0 for v in s):"),
    ("N24-size-len3", "wrong-constant",
     "if isinstance(s, list) and len(s) == 2 and all(", "if isinstance(s, list) and len(s) == 3 and all("),
    ("N25-ctl-below-1f", "value-domain", "if any(ord(ch) < 0x20 for ch in cls):",
     "if any(ord(ch) < 0x1f for ch in cls):"),
    ("N26-ctl-below-7f", "value-domain", "if any(ord(ch) < 0x20 for ch in cls):",
     "if any(ord(ch) < 0x7f for ch in cls):"),
    ("N27-selftest-prefix", "dropped-check", 'if argv == ["--selftest"]:',
     'if argv and argv[0] == "--selftest":'),
    ("N28-double-clients", "dropped-check", 'if flag == "--clients" and clients is None:',
     'if flag == "--clients":'),
    ("N29-rules-optional", "dropped-check", "if clients is None or not rules:",
     "if clients is None:"),
    # ---- exit codes / verdict ladder ---------------------------------------
    ("N30-ok-exit3", "exit-code", 'verdict, rc = "OK", 0', 'verdict, rc = "OK", 3'),
    ("N31-nosize-exit3", "exit-code", 'verdict, rc = "NO_SIZE_RULES", 4',
     'verdict, rc = "NO_SIZE_RULES", 3'),
    ("N32-differ-exit2", "exit-code", 'verdict, rc = "DIFFER", 1', 'verdict, rc = "DIFFER", 2'),
    ("N33-nomatch-exit4", "exit-code", 'verdict, rc = "NO_MATCHING_CLIENT", 3',
     'verdict, rc = "NO_MATCHING_CLIENT", 4'),
    ("N34-differ-and-matched", "reordered-check", 'elif t["differ"] > 0:',
     'elif t["differ"] > 0 and t["matched"] > 0:'),
    ("N35-summary-floatcount", "swapped-field", "len(rules) - size_rules,", "len(rules),"),
    ("N36-summary-size-sums-float", "wrong-constant",
     'size_rules = sum(1 for r in rules if r["effect"] == "size")',
     'size_rules = sum(1 for r in rules if r["effect"] == "float")'),
    ("N37-client-addr-class-swap", "swapped-output-field",
     'json.dumps(addr), json.dumps(cls), "true" if floating else "false",',
     'json.dumps(cls), json.dumps(addr), "true" if floating else "false",'),
    ("N38-addr-default-empty", "value-domain",
     'addr = c.get("address") if isinstance(c.get("address"), str) else "-"',
     'addr = c.get("address") if isinstance(c.get("address"), str) else ""'),
    ("N39-class-default-dash", "value-domain",
     'cls = c.get("class") if isinstance(c.get("class"), str) else ""',
     'cls = c.get("class") if isinstance(c.get("class"), str) else "-"'),
    ("N40-file-index-from-2", "off-by-one", "for k, text in enumerate(rule_texts, 1):",
     "for k, text in enumerate(rule_texts, 2):"),
    ("N41-rule-number-from-0", "off-by-one", "for n, r in enumerate(rules, 1)]",
     "for n, r in enumerate(rules, 0)]"),
    ("N42-first-size-wins", "reordered-check", '            if matches(r["rx"], cls):',
     '            if matches(r["rx"], cls) and want is None:'),
    ("N43-size-resets-frule", "dropped-state", "                    want = r[\"want\"]",
     '                    want, frule = r["want"], "-"'),
    ("N44-tally-assign", "dropped-accumulation", '        tally[verdict.lower()] += 1',
     '        tally[verdict.lower()] = 1'),
    ("N45-unmapped-counts-clients", "swapped-field", '            tally["unmapped"] += 1',
     '            tally["clients"] += 1'),
    ("N46-doc-tuple", "value-domain",
     "if not isinstance(doc, list) or not all(isinstance(c, dict) for c in doc):",
     "if not isinstance(doc, (list, tuple)) or not all(isinstance(c, dict) for c in doc):"),
    ("N47-doc-any-not-all", "operator-swap",
     "if not isinstance(doc, list) or not all(isinstance(c, dict) for c in doc):",
     "if not isinstance(doc, list) or not any(isinstance(c, dict) for c in doc):"),
    # ---- decode / json / match details -------------------------------------
    ("N48-rules-decode-ignore", "value-domain",
     'texts = [read_regular(p).decode("utf-8", "replace") for p in rules]',
     'texts = [read_regular(p).decode("utf-8", "ignore") for p in rules]'),
    ("N49-json-decode-strict", "value-domain", 'doc = json.loads(data.decode("utf-8"))',
     'doc = json.loads(data.decode("utf-8", "strict"))'),
    ("N50-summary-other-swap", "swapped-field", 'counts["other"], counts["unsupported"],',
     'counts["unsupported"], counts["other"],'),
    ("N51-close-fd-pass", "dropped-branch", "        os.close(fd)", "        pass"),
    ("N52-size-truthiness", "value-domain", '"%dx%d" % size if size else "-"',
     '"%dx%d" % size if size is not None else "-"'),
    ("N53-fullmatch-dotall", "value-domain",
     "return re.fullmatch(rx, cls) is not None",
     "return re.fullmatch(rx, cls, re.DOTALL) is not None"),
    ("N54-read-chunk-cap", "value-domain",
     "chunk = os.read(fd, MAX_BYTES + 1 - len(data))",
     "chunk = os.read(fd, MAX_BYTES)"),
    ("N55-client-order-reversed", "dropped-stability", "lines += clines",
     "lines += list(reversed(clines))"),
    ("N56-ctl-guard-dropped", "dropped-branch", "if any(ord(ch) < 0x20 for ch in cls):",
     "if False:"),    ("N57-reverse-client-order", "dropped-stability", "    for c in clients:",
     "    for c in reversed(clients):"),
    ("N58-size-key-index", "dropped-branch", '    s = c.get("size")', '    s = c["size"]'),
    ("N59-size-tuple-swap", "swapped-output-field", "        return (s[0], s[1])",
     "        return (s[1], s[0])"),
    ("N60-safe-prefix-match", "operator-swap", "    if not SAFE.fullmatch(rx):",
     "    if not SAFE.match(rx):"),
    ("N61-regexok-call-dropped", "dropped-check",
     "        if not mm or not regex_ok(mm.group(1)):", "        if not mm:"),
    ("N62-parse-step-1", "off-by-one", "        i += 2", "        i += 1"),
    ("N63-parse-loop-le", "boundary-shift", "    while i < len(argv):",
     "    while i <= len(argv):"),
    ("N64-nosize-inverted", "reordered-check", '    if size_rules == 0:',
     "    if size_rules != 0:"),
    ("N65-badsize-key-rename", "wrong-constant", '"tiled": 0, "badsize": 0}',
     '"tiled": 0, "bad_size": 0}'),
    ("N66-summary-clients-key", "swapped-output-field",
     'unsupported=%d clients=%d "', 'unsupported=%d client=%d "'),
    ("N67-unreadable-as-toolarge", "wrong-constant",
     'raise Setup("unreadable")\n        data = b""',
     'raise Setup("too_large")\n        data = b""'),
    ("N68-stdout-print", "value-domain",
     '    sys.stdout.write("\\n".join(lines) + "\\n")', '    print("\\n".join(lines))'),
]


def main():
    ref = open(REF, encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    built, bad = [], []
    for name, cat, old, new in MUT:
        n = ref.count(old)
        if n != 1 or old == new:
            bad.append((name, n, old[:60]))
            continue
        text = ref.replace(old, new, 1)
        assert text != ref
        compile(text, name, "exec")
        with open(os.path.join(OUT, name + ".py"), "w", encoding="utf-8") as fh:
            fh.write(text)
        built.append({"name": name, "category": cat, "old": old, "new": new})
    json.dump(built, open(os.path.join(SEAT, "mutants.json"), "w"), indent=1)
    print("built=%d" % len(built))
    for name, n, s in bad:
        print("REJECT matches=%d %s :: %r" % (n, name, s))
    return 1 if bad else 0


sys.exit(main())
