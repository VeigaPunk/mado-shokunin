#!/usr/bin/env python3
"""Differential fuzz: the seat tool vs PRED-C1-r44's model.

Imports the frozen counter with importlib.util (never calls main) and reuses its
model_out_states, its gen_state_clients and the round-42 gen_texts/rng_for. Runs the
tool's report() in process on >= 2000 random cases plus 200 adversarial ones, then
replays every adversarial case through the real CLI (subprocess, -I) so the byte-exact
stdout/rc/stderr path is covered too. Prints one line per disagreement with a
minimised repro. Exit 0 iff zero disagreements.

  python3 -I fuzz.py [--random N] [--work DIR]
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

LANE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r44-geometry-states.py")
TOOL = os.path.join(LANE, ".ufo", "waves", "round-44", "w1", "ExecIndepB", "mado-geometry.py")
for _i, _a in enumerate(sys.argv):
    if _a == "--tool" and _i + 1 < len(sys.argv):
        TOOL = os.path.abspath(sys.argv[_i + 1])
REV = "e2289516a9a857f55cda7be635933e89b931c3da"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c44 = load("c44fuzz", COUNTER)
old = c44.old
tool = load("mtoolfuzz", TOOL)


def tool_out(raw, texts):
    try:
        lines, rc = tool.report(raw, texts)
    except tool.Setup as exc:
        return None, str(exc)
    return "\n".join(lines) + "\n", rc


def model_out(raw, texts):
    return c44.model_out_states(raw, texts)


def disagree(raw, texts):
    return model_out(raw, texts) != tool_out(raw, texts)


# ---------------------------------------------------------------- CLI replay
class Cli:
    def __init__(self, parent):
        self.tmp = tempfile.mkdtemp(prefix="cli-", dir=parent)

    def run(self, raw, texts, name):
        d = os.path.join(self.tmp, name)
        os.makedirs(d, exist_ok=True)
        rp = []
        for i, t in enumerate(texts):
            p = os.path.join(d, "r%d.conf" % i)
            with open(p, "wb") as fh:
                fh.write(t.encode("utf-8", "surrogateescape"))
            rp.append(p)
        cp = os.path.join(d, "c.json")
        with open(cp, "wb") as fh:
            fh.write(raw)
        argv = [os.path.realpath(sys.executable), "-I", TOOL, "--clients", cp]
        for p in rp:
            argv += ["--rules", p]
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        p = subprocess.run(argv, capture_output=True, env=env, timeout=60)
        return p.returncode, p.stdout, p.stderr


# ---------------------------------------------------------------- adversarial set
def adv_cases():
    gk = "^(org.omarchy.gkeep)$"
    conf = "windowrule = float on, match:class %s\nwindowrule = size 420 500, match:class %s\n" % (gk, gk)
    cases = []

    def add(raw, texts=None, tag="adv"):
        cases.append((raw if isinstance(raw, bytes) else raw.encode(), texts or [conf], tag))

    base = '{"class": "org.omarchy.gkeep", "size": [2560, 1440], "floating": true'
    # A. huge / boundary integers in fullscreen and size
    for v in ("1000000000000000000000000000000", "-1000000000000000000000000000000",
              "9223372036854775807", "-9223372036854775808", "1267650600228229401496703205376",
              "1", "2", "0", "3", "-1", "1e999", "NaN", "2.0", "1.0", "0.5", "-0.0",
              "true", "false", "null", '"2"', '""', "[]", "[2]", '{"internal": 2}', '{"mode": 2}',
              '[[2]]', '{"0": 2}', "{}"):
        add('[%s, "fullscreen": %s}]' % (base, v), tag="A-fs=%s" % v)
    for v in ("[0, 0]", "[0, 1]", "[1, 2]", "[420, 500]", "[421, 500]",
              "[1000000000000000000000, 1000000000000000000000]", "[1.0, 2]", "[true, 2]",
              "[-1, 2]", "[1, 2, 3]", '[1]', "[]", "null", '"4x5"', "{}", "[[1,2],3]",
              '[null, 2]', "[1e999, 2]", "[NaN, 2]"):
        add('[{"class": "org.omarchy.gkeep", "floating": true, "fullscreen": 2, "size": %s}]' % v,
            tag="A-size=%s" % v)
    # B. duplicate keys (last wins), CRLF rules, tabs
    for first, second in (("0", "2"), ("2", "0"), ("1", "2"), ("2", "2"), ("null", "1")):
        add('[%s, "fullscreen": %s, "fullscreen": %s}]' % (base, first, second),
            tag="B-dup-fs=%s,%s" % (first, second))
    add('[{"class": "org.omarchy.gkeep", "class": "kitty", "size": [420, 500], "floating": true, "fullscreen": 2}]',
        tag="B-dup-class")
    add('[{"class": "org.omarchy.gkeep", "size": [1, 1], "size": [420, 500], "floating": true, "fullscreen": 2}]',
        tag="B-dup-size")
    # C. type confusion on the other fields
    for v in ('5', 'null', '"kitty"', '["org.omarchy.gkeep"]', '{"a": 1}', 'true'):
        add('[{"class": %s, "size": [420, 500], "floating": true, "fullscreen": 2}]' % v,
            tag="C-class=%s" % v)
    for v in ('false', '0', 'null', '"false"', 'true', '1'):
        add('[{"class": "org.omarchy.gkeep", "size": [420, 500], "floating": %s, "fullscreen": 2}]' % v,
            tag="C-mapped=%s" % v)
    for v in ('false', 'null', '0', '"true"', 'true'):
        add('[{"class": "org.omarchy.gkeep", "size": [420, 500], "floating": %s, "fullscreen": 1}]' % v,
            tag="C-floating=%s" % v)
    for v in ('5', 'null', '"0x9"', 'true', '"\\u00fc\\"q"'):
        add('[{"class": "org.omarchy.gkeep", "size": [420, 500], "floating": true, "address": %s, "fullscreen": 2}]' % v,
            tag="C-addr=%s" % v)
    # D. control characters and unicode classes
    for v in ('"org.omarchy.gkeep\\u0001"', '"\\u0000org.omarchy.gkeep"', '"\\u00fc-app"',
              '"org.omarchy.gkeep "', '"org.omarchy.gkeep\\n"', '"\\ud83d\\ude00"'):
        add('[{"class": %s, "size": [420, 500], "floating": true, "fullscreen": 2}]' % v,
            tag="D-class=%s" % v)
    # E. rules: whitespace, CRLF, ignored and unsupported lines
    variants = [
        "windowrule=size 420 500,match:class %s" % gk,
        "  windowrule =\tsize\t420\t500, \tmatch:class\t%s  " % gk,
        "windowrule = size 420 500, match:class %s\r\n" % gk,
        "windowrulev2 = size 420 500, class:org.omarchy.gkeep",
        "",
        "windowrule = float on, match:class %s" % gk,
        "windowrule = size 420 500, match:class .*\nwindowrule = size 420 500, match:class %s" % gk,
        "windowrule = size 0000420 0000500, match:class %s" % gk,
        "windowrule = size 420 500, match:class (?i)%s" % gk,
        "windowrule = size 420 500, match:class %s # tail" % gk,
        "windowrule = center on, match:class a\nwindowrule = size 420 500, match:class %s" % gk,
    ]
    for k, t in enumerate(variants):
        add('[%s, "fullscreen": 2}]' % base, [t], tag="E-rules%d" % k)
    # F. malformed clients documents (bad_json)
    for k, raw in enumerate((b"{}", b"[1]", b"", b"\xff", b"[", b'[{"a": 1}, 2]', b"null",
                             b'"x"', b"[] ", b'[{"class": "x"}]trailing', b"\xef\xbb\xbf[]")):
        add(raw, tag="F-badjson%d" % k)
    # G. mixed state clouds
    for k in range(12):
        cl = []
        for j in range(8):
            cl.append({"class": "org.omarchy.gkeep", "size": [420 + (j % 3), 500],
                       "floating": bool(j % 2), "fullscreen": (j + k) % 4,
                       "address": "0x%x" % j})
            if j % 5 == 0:
                cl[-1]["mapped"] = False
        add(json.dumps(cl), tag="G-cloud%d" % k)
    # H. empty documents and rule-less setups
    add(b"[]", [""], tag="H-empty-both")
    add(b"[]", ["windowrule = float off, match:class a\n"], tag="H-float-only")
    add('[{"class": "org.omarchy.gkeep", "mapped": false, "fullscreen": 2}]', tag="H-unmapped-only")
    # I. the state x size x floating product, junk values included
    fs_pool = ("absent", "0", "1", "2", "true", "2.0", '"2"', "3", "-1", "null",
               "1e999", '{"internal": 2}', "[2]", "1000000000000000000000000000000")
    sz_pool = ("[420, 500]", "[2560, 1440]", "[421, 500]", "null", "[-1, 2]",
               "[true, 2]", "[0, 0]", "[]")
    for fs in fs_pool:
        for sz in sz_pool:
            tail = "" if fs == "absent" else ', "fullscreen": %s' % fs
            add('[{"class": "org.omarchy.gkeep", "size": %s, "floating": true%s}]'
                % (sz, tail), tag="I-%s-%s" % (fs, sz))
    for fs in ("0", "1", "2", "null", "2.0"):
        for fl in ("true", "false", "1", "null"):
            add('[{"class": "org.omarchy.gkeep", "size": [420, 500], "floating": %s, '
                '"fullscreen": %s}]' % (fl, fs), tag="I-fl%s-fs%s" % (fl, fs))
    # J. several rule files, ordering and duplicate size rules
    add('[%s, "fullscreen": 2}]' % base,
        ["windowrule = size 100 200, match:class a\n",
         "windowrule = size 420 500, match:class org\\.omarchy\\..*\n",
         "windowrule = float off, match:class %s\n" % gk], tag="J-three-files")
    add('[%s, "fullscreen": 1}]' % base,
        ["windowrule = size 420 500, match:class %s\nwindowrule = size 1 1, match:class %s\n" % (gk, gk)],
        tag="J-last-size-wins")
    add('[%s, "fullscreen": 2}]' % base,
        ["windowrule = size 420 500, match:class %s\n" % ("a" * 200)], tag="J-regex-200")
    add('[%s, "fullscreen": 2}]' % base,
        ["windowrule = size 420 500, match:class a" + "b" * 201], tag="J-regex-201")
    add('[%s, "fullscreen": 2}]' % base,
        ["windowrule = size 420 500, match:class \\(org\\.omarchy\\.gkeep\\)\n"], tag="J-escaped-regex")
    add('[%s, "fullscreen": 2}]' % base,
        ["windowrule = size 420 500, match:class ^(org\\.omarchy\\.gkeep)$\n",
         "windowrule = size 420 500, match:class org.omarchy.gkeep\n"], tag="J-two-files-dup")
    # K. missing and extra keys
    add('[{"size": [420, 500], "floating": true, "fullscreen": 2}]', tag="K-no-class")
    add('[{"class": "org.omarchy.gkeep", "floating": true, "fullscreen": 2}]', tag="K-no-size")
    add('[{"class": "org.omarchy.gkeep", "size": [420, 500], "fullscreen": 1}]', tag="K-no-floating")
    add('[{"class": "org.omarchy.gkeep", "size": [420, 500], "floating": true, "fullscreen": 2, '
         '"extra": {"nested": [1, 2, {"deep": null}]}}]', tag="K-extra-nested")
    add('[{"class": "org.omarchy.gkeep", "size": [420, 500], "floating": true, "fullscreen": 2}]'
        '[{"class": "org.omarchy.gkeep", "size": [420, 500], "floating": true, "fullscreen": 1}]',
        tag="K-two-objects")
    # L. one big cloud with every state represented
    cloud = []
    for k in range(50):
        cloud.append({"class": "org.omarchy.gkeep" if k % 3 else "kitty",
                      "size": [420, 500] if k % 2 else [k, k],
                      "floating": bool(k % 2), "fullscreen": k % 4,
                      "address": "0x%x" % k})
    add(json.dumps(cloud), tag="L-cloud50")
    return cases


# ---------------------------------------------------------------- minimiser
def minimise(raw, texts):
    def parse(r):
        try:
            return json.loads(r)
        except Exception:
            return None
    try:
        doc = parse(raw)
        while True:
            changed = False
            # shrink texts to the smallest reproducing line set
            for i in range(len(texts)):
                lines = texts[i].split("\n")
                for j in range(len(lines)):
                    cand = texts[:i] + ["\n".join(lines[:j] + lines[j + 1:])] + texts[i + 1:]
                    if cand != texts and disagree(raw, cand):
                        texts, changed = cand, True
                        break
                if changed:
                    break
            if changed:
                continue
            if len(texts) > 1:
                for i in range(len(texts)):
                    cand = texts[:i] + texts[i + 1:]
                    if disagree(raw, cand):
                        texts, changed = cand, True
                        break
                if changed:
                    continue
            doc = parse(raw)
            if isinstance(doc, list):
                if len(doc) > 1:
                    for k in range(len(doc)):
                        cand = json.dumps(doc[:k] + doc[k + 1:]).encode()
                        if disagree(cand, texts):
                            raw, changed = cand, True
                            break
                    if changed:
                        continue
                if len(doc) == 1 and isinstance(doc[0], dict):
                    for key in list(doc[0]):
                        d2 = {kk: vv for kk, vv in doc[0].items() if kk != key}
                        cand = json.dumps([d2]).encode()
                        if disagree(cand, texts):
                            raw, changed = cand, True
                            break
                    if changed:
                        continue
            if not changed:
                break
    except Exception:
        pass
    return raw, texts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--random", type=int, default=2000)
    ap.add_argument("--work", default=None)
    ap.add_argument("--tool", default=None, help="score this file instead (harness mutation check)")
    args = ap.parse_args()
    work = args.work or tempfile.mkdtemp(prefix="fuzz-")
    os.makedirs(work, exist_ok=True)
    bad = []
    # random lattice, the counter's own generators
    for i in range(args.random):
        rng = old.rng_for(REV, "execindepb-fuzz", "diff", i)
        texts, wants = old.gen_texts(rng)
        raw = json.dumps(c44.gen_state_clients(rng, wants)).encode()
        if disagree(raw, texts):
            bad.append(("random%d" % i, raw, texts))
    random_bad = len(bad)
    # adversarial set, in process and through the CLI
    cli = Cli(work)
    adv = adv_cases()
    cli_bad = 0
    for n, (raw, texts, tag) in enumerate(adv):
        model = model_out(raw, texts)
        got = tool_out(raw, texts)
        rc, out, err = cli.run(raw, texts, "adv%d" % n)
        want_out, want_rc = ((("MADO_GEOMETRY: SETUP %s\n" % model[1]), 2)
                             if model[0] is None else model)
        got_cli = (out.decode("utf-8", "replace"), rc)
        if got != model:
            bad.append((tag + "-inproc", raw, texts))
        if got_cli != (want_out, want_rc):
            cli_bad += 1
            bad.append((tag + "-cli", raw, texts))
        if want_rc in (0, 1, 3, 4) and err:
            cli_bad += 1
            bad.append((tag + "-stderr", raw, texts))
    print("FUZZ: random=%d random_disagreements=%d adversarial=%d adversarial_disagreements=%d"
          % (args.random, random_bad, len(adv), len(bad) - random_bad))
    for name, raw, texts in bad[:40]:
        mraw, mtexts = minimise(raw, texts)
        print("DISAGREE %s: clients=%r texts=%r" % (name, mraw[:200], mtexts))
        print("  model=%r" % (model_out(mraw, mtexts),))
        print("  tool =%r" % (tool_out(mraw, mtexts),))
    print("FUZZ VERDICT: %s" % ("PASS" if not bad else "FAIL"))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
