#!/usr/bin/env python3
"""R55W2CritToolDiff: seeded generator + differential runner for tools/mado-kbdopts.py vs oracle.py.

Run: python3 -I gen_diff.py --seed 55 --n 3400 --workers 8
Every case = a private directory holding only its input files; the oracle (in-process, chdir into the case dir)
and the tool (subprocess, cwd = the case dir, identical relative argv) both run on it. Stdout bytes and rc are compared.
Divergences are minimised (token, line, byte level) while the divergence persists and written to minimised.json.
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

SCR = "/fast/scratch/hyaku/mado-r55/R55W2CritToolDiff"
TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-kbdopts.py"
sys.path.insert(0, SCR)
import importlib  # noqa: E402
oracle = importlib.import_module(os.environ.get("ORACLE_MOD", "oracle"))  # oracle.py: written from the contract text only

# ---------------------------------------------------------------- generator vocabulary

LHS_KEYS = [
    "repeat_rate", "repeat_delay", "numlock_by_default",
    "input:repeat_rate", "input:repeat_delay", "input:numlock_by_default",
    "source", "$x", "device[kb]:repeat_rate", "device[x]:input:numlock_by_default",
    "repeat-rate", "Repeat_rate", "input:repeat_rate ", " input:repeat_rate", "input:repeat_rate\t",
    "name", "device:repeat_rate", "input:numlock_by_default:x", "device[]:delay", "input:x:repeat_rate",
    "repeat_delay_x", "device[a]:repeat_delay", "input:repeat_delay",
]
VALS = [
    "0", "1", "2", "25", "200", "201", "600", "2000", "2001", "-1", "+5", "0x1F", "1.5", "", "#5", "5#c",
    "5 # c", "5##c", "$VAR", "5{{", "5\\", "3 0", "true", "false", "on", "off", "yes", "no", "True", "TRUE",
    "onion", "nope", "yesno", "offset", "true#x", "off#", "0000000000000000000000030",
    "00000000000000000000000002", "9" * 5000, "0" * 5000 + "30", "1" * 4400, " 7 ", "\t7\t", "\u0661",
    "1_000", "1e3", "tru", "o", "n", "2000 ", "200#", "5\x0b", "5\x0c", "5\x1c", "5\u00a0", "\u00a05",
    "5\r7", "no#yes", "5 ##", "#", "5=6", "true=1", "0x", "-0", "00", "007", "2e0", "NaN", "inf",
    "\u00e9", "1\x00", "5\"", "'5'", "5;", "[5]", "{5}", "5 5", "100000000000000000000", "7" * 9, "2" * 10,
]
NAME_POOL = [
    "kbA", "kbB", "Mouse 1", "My Keyboard", "kb#1", "x$y", "a\\b", "\u00e9", "", "*", "kbA  ", "device",
    "\u00fcn\u00ef", "tab\tname", "k\"q\"", "kbX", "=", "a=b", "#", "##",
]
BLOCK_NAMES = [
    "input", "device", "device", "device", "device", "device[kb]", "device[kb:x]", "touchpad", "Device",
    "device ", "input ", "  device", "", "in put", "device:x", "input:x", "device[1]", "devices", "device\t",
    "device[]", "device[kb] ", "device[x]", "input{", "device{", "general", "animations",
]
JUNK = [
    "foo", "input:repeat_rate", "name", "repeat_rate", "{{", "{", "input{{", "a b {", "device[kb] {}",
    "input {}", "}}", "} x", "}  #", "repeat_rate {", "input:repeat_rate{", "name = a {", "x = y {", "$VAR = {",
    "source = x", "$input:repeat_rate = 5", "input:repeat_rate{ = 5", "source{", "device[", "]",
    "#input:repeat_rate = 5", "  # comment {", "\u00a0input:repeat_rate = 5", "\ufeffinput:repeat_rate = 5",
    "\x1cinput:repeat_rate = 5", "input:repeat_rate\x1c = 5", "input:repeat_rate = 5 }", "= 5", "=",
    "input:repeat_rate =", "device[kb]{", "x{", "}{", "{}", "name=", "name = #", "name = ## x",
]
WS_CHOICES = ["", "", "", " ", "\t", "  ", "\x0b", "\x0c", "\r", " \t", "\x0c "]
GO_OPTS = ["input:repeat_rate", "input:repeat_delay", "input:numlock_by_default", "input:other", "repeat_rate"]
GO_INTS = ["30", "-1", "0", "1", "2", "25", "200", "201", "600", "2000", "99999999999999999999", "true",
           "false", "30.0", "\"30\"", "null", "1e2", "-0", "NaN", "0.0", "2e0", "1E2", "[1]", "{}"]
GO_BAD = ["{bad", "[1]", "\"x\"", "null", "1", "{\"option\": \"input:repeat_rate\", \"int\": 30",
          "not json", "{\"option\":\"input:repeat_rate\",\"int\":NaN}", "{\"option\":\"input:repeat_rate\",\"int\":30}x"]
GO_ODD = ["{}", "{\"option\": 5, \"int\": 3}", "{\"option\":\"input:repeat_rate\",\"int\":30}\r",
          "{\"option\":\"input:repeat_rate\",\"int\":30}\x0c", "\ufeff{\"option\":\"input:repeat_rate\",\"int\":30}",
          "  {\"option\":\"input:repeat_rate\",\"int\":30}  ",
          "{\"option\":\"input:repeat_rate\",\"int\":30,\"option\":\"input:repeat_delay\"}",
          "{\"option\":\"input:repeat_rate\",\"option\":\"input:numlock_by_default\",\"int\":1}",
          "{\"int\": 7}", "{\"option\": \"input:repeat_rate\"}", "{\"option\": null, \"int\": 3}",
          "{\"option\":\"input:numlock_by_default\",\"int\":2}", "{\"option\":\"input:repeat_delay\",\"int\":-5}",
          "{\"option\":\"input:repeat_rate\",\"int\":\"9\",\"x\":{\"a\":[1,2,{}]}}", "{\"option\":\"input:repeat_rate\",\"int\":1}\t"]


PROFILE = "adv"  # "adv": adversarial grammar soup; "valid": mostly-valid device/global structure
MODE = "clean"  # "clean": no control-char keyboard names, no whitespace-only getoption lines; "ambig": both kept
CTL = set(chr(c) for c in range(0x20)) | {chr(0x7F)}
KB_POOL_ALL = None


def kb_pool():
    return [n for n in NAME_POOL if not (set(n) & CTL)] if MODE == "clean" else list(NAME_POOL)


def ws(r):
    return r.choice(WS_CHOICES)


def key_line(r):
    lhs = r.choice(LHS_KEYS)
    val = r.choice(VALS)
    if r.random() < 0.15:
        val = val + r.choice([" # c", "#x", " ## y", " ", "\t", "\x0b"])
    return f"{ws(r)}{lhs}{ws(r)}={ws(r)}{val}{ws(r)}"


SEEN = []  # device names written into the current case's configs (keyboard args are drawn from these)


def name_line(r):
    nm = r.choice(NAME_POOL)
    SEEN.append(nm.split("#", 1)[0].strip(" \t\r\n\x0b\x0c"))
    return f"{ws(r)}name{ws(r)}={ws(r)}{nm}{r.choice(['', ' # c', '#x', ' ## y', ' ', chr(9)])}"


def opener(r):
    blk = r.choice(BLOCK_NAMES)
    if r.random() < 0.2:
        return f"{ws(r)}{blk}{{{ws(r)}"
    return f"{ws(r)}{blk}{ws(r)}{{{ws(r)}"


def closer(r):
    return f"{ws(r)}{r.choice(['}', '}', '}', '}  ', '}}', '} x', '}#c'])}"


def gen_block(r, depth, out):
    out.append(opener(r))
    for _ in range(r.randint(0, 7)):
        x = r.random()
        if x < 0.40:
            out.append(key_line(r))
        elif x < 0.50:
            out.append(name_line(r))
        elif x < 0.60 and depth < 3:
            gen_block(r, depth + 1, out)
        elif x < 0.72:
            out.append(r.choice(JUNK))
        elif x < 0.78:
            out.append(r.choice(["", " ", "\t", "\x0b", "\x0c"]))
        elif x < 0.84:
            out.append(r.choice(["# input:repeat_rate = 5", "  # repeat_rate = 9", "#device {", "#}"]))
        elif x < 0.90:
            out.append(closer(r))
        else:
            out.append(key_line(r))
    if r.random() < 0.85:
        out.append(closer(r))


def gen_config(r):
    out = []
    for _ in range(r.randint(0, 9)):
        x = r.random()
        if x < 0.45:
            gen_block(r, 0, out)
        elif x < 0.80:
            out.append(key_line(r))
        elif x < 0.88:
            out.append(name_line(r))
        else:
            out.append(r.choice(JUNK))
    sep = r.choices(["\n", "\r\n", "\r", "\n\n", "\n"], weights=[70, 12, 4, 4, 10])[0]
    text = sep.join(out)
    if r.random() < 0.6:
        text += "\n"
    data = text.encode("utf-8")
    if r.random() < 0.04:
        data = b"\xef\xbb\xbf" + data
    if r.random() < 0.04:
        pos = r.randint(0, len(data))
        data = data[:pos] + b"\xff\xfe" + data[pos:]
    return data


def gen_getoption(r):
    lines = []
    for _ in range(r.randint(0, 6)):
        x = r.random()
        if x < 0.55:
            opt = r.choice(GO_OPTS + [None])
            iv = r.choice(GO_INTS)
            parts = []
            if opt is not None:
                parts.append(f"\"option\": {json.dumps(opt)}")
            if r.random() < 0.9:
                parts.append(f"\"int\": {iv}")
            if r.random() < 0.1:
                parts.append("\"zz\": 1")
            r.shuffle(parts)
            lines.append("{" + ", ".join(parts) + "}")
        elif x < 0.68:
            lines.append(r.choice([""] if MODE == "clean" else ["", " ", "\t", "\r", "\x0c", "   "]))
        elif x < 0.78:
            lines.append(r.choice(GO_ODD))
        elif x < 0.86:
            lines.append(r.choice(GO_BAD))
        else:
            lines.append("{\"option\":\"%s\",\"int\":%s}" % (r.choice(GO_OPTS), r.choice(GO_INTS)))
    text = "\n".join(lines) + (r.choice(["", "\n", "\n\n"]))
    data = text.encode("utf-8")
    if r.random() < 0.03:
        data = data + b"\xff"
    return data


VALID_VALS = ["0", "1", "25", "30", "200", "201", "2000", "2001", "600", "1000", "02", "00", "true", "false",
              "on", "off", "yes", "no", "nope", "onion", "5#c", "5 ## x", "0x1f", "-3", "2", "1_0", "7 # x", " 9 "]
VALID_LHS = ["repeat_rate", "repeat_delay", "numlock_by_default"]


def gen_valid_config(r):
    """Mostly-valid device/global structure: merges, overrides, stack resets, nested blocks, name variants."""
    out = []
    names = ["kbA", "kbB", "Mouse 1", "kbA", "x$y", "a\\b", "\u00e9", "kb#1", "*"]
    SEEN.extend(n.split("#", 1)[0] for n in names)
    for _ in range(r.randint(1, 6)):
        x = r.random()
        if x < 0.25:
            out.append(f"input:{r.choice(VALID_LHS)} = {r.choice(VALID_VALS)}")
        elif x < 0.40:
            out.append("input {")
            for _ in range(r.randint(0, 3)):
                out.append(f"  {r.choice(VALID_LHS)} = {r.choice(VALID_VALS)}")
            if r.random() < 0.9:
                out.append("}")
        elif x < 0.80:
            out.append(r.choice(["device {", "device{", "device {  ", "  device  {"]))
            if r.random() < 0.75:
                out.append(f"  name = {r.choice(names)}{r.choice(['', ' # c', '#x'])}")
            for _ in range(r.randint(0, 3)):
                out.append(f"  {r.choice(VALID_LHS)} = {r.choice(VALID_VALS)}")
            if r.random() < 0.2:
                out.append("  touchpad {")
                out.append(f"    repeat_rate = {r.choice(VALID_VALS)}")
                out.append("  }")
            if r.random() < 0.9:
                out.append("}")
        elif x < 0.86:
            out.append(f"device[{r.choice(names)}] {{")
            out.append(f"  repeat_rate = {r.choice(VALID_VALS)}")
            out.append("}")
        elif x < 0.92:
            out.append(f"{r.choice(VALID_LHS)} = {r.choice(VALID_VALS)}")
        else:
            out.append(r.choice(["}", "# comment", "", "  "]))
    sep = r.choices(["\n", "\r\n"], weights=[85, 15])[0]
    data = (sep.join(out) + ("\n" if r.random() < 0.7 else "")).encode("utf-8")
    return data


def gen_random_case(r, idx):
    files = {}
    argv_tokens = []
    SEEN.clear()
    n_cfg = r.choices([1, 2, 3], weights=[70, 22, 8])[0]
    for k in range(n_cfg):
        fname = f"c{k}.conf"
        if r.random() < 0.03:
            files[fname] = ("bytes", b"")
        elif PROFILE == "valid":
            files[fname] = ("bytes", gen_valid_config(r))
        else:
            files[fname] = ("bytes", gen_config(r))
        argv_tokens.append(("--config", fname))
        if r.random() < 0.05 and k > 0:  # same file twice
            argv_tokens.append(("--config", fname))
    names = list(set(kb_pool() + ["kbA", "kbB", "Mouse 1", "My Keyboard", "kbX"]))
    seen = [s for s in SEEN if not (set(s) & CTL)] if MODE == "clean" else list(SEEN)
    for _ in range(r.choices([0, 1, 2, 3], weights=[20, 35, 30, 15])[0]):
        if seen and r.random() < 0.75:
            argv_tokens.append(("--keyboard", r.choice(seen)))
        else:
            argv_tokens.append(("--keyboard", r.choice(names)))
    if r.random() < 0.5:
        files["go.json"] = ("bytes", gen_getoption(r))
        argv_tokens.append(("--getoption", "go.json"))
    r.shuffle(argv_tokens)
    argv = []
    for flag, v in argv_tokens:
        argv += [flag, v]
    return {"id": f"R{idx:05d}", "kind": "random", "files": files, "argv": argv}


def edge_cases():
    big_ok = b"#" + b"x" * (1048576 - 2) + b"\n"
    assert len(big_ok) == 1048576, len(big_ok)
    big_bad = big_ok + b"\n"
    go_big = b"{}\n" + b" " * 1048576
    C = []

    def add(cid, files, argv, kind="edge"):
        C.append({"id": cid, "kind": kind, "files": files, "argv": argv})

    cfg = {"c0.conf": ("bytes", b"input:repeat_rate = 30\n")}
    add("E01-noargs", {}, [])
    add("E02-config-no-value", {}, ["--config"])
    add("E03-missing-config", {"c0.conf": ("bytes", b"x")}, ["--config", "c0.conf", "--config", "missing.conf"])
    add("E04-dir-config", {"d": ("dir",)}, ["--config", "d"])
    add("E05-fifo-config", {"p": ("fifo",)}, ["--config", "p"])
    add("E06-exact-1MiB-config", {"c0.conf": ("bytes", big_ok)}, ["--config", "c0.conf"])
    add("E07-1MiB+1-config", {"c0.conf": ("bytes", big_bad)}, ["--config", "c0.conf"])
    add("E08-1MiB+1-getoption", {"c0.conf": ("bytes", b"")}, ["--config", "c0.conf", "--getoption", "go"]
        if False else ["--config", "c0.conf", "--getoption", "go.json"])
    C[-1]["files"]["go.json"] = ("bytes", go_big)
    add("E09-getoption-twice", {"c0.conf": ("bytes", b""), "go.json": ("bytes", b"")},
        ["--config", "c0.conf", "--getoption", "go.json", "--getoption", "go.json"])
    add("E10-eq-form", {"c0.conf": ("bytes", b"")}, ["--config=c0.conf"])
    add("E11-unknown-flag", {"c0.conf": ("bytes", b"")}, ["--config", "c0.conf", "--bogus", "x"])
    add("E12-keyboard-no-config", {}, ["--keyboard", "kbA"])
    add("E13-missing-getoption", {"c0.conf": ("bytes", b"")}, ["--config", "c0.conf", "--getoption", "nope.json"])
    add("E14-empty-getoption", {"c0.conf": ("bytes", cfg["c0.conf"][1]), "go.json": ("bytes", b"")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E15-bad-json-getoption", {"c0.conf": ("bytes", b""), "go.json": ("bytes", b"not json\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E16-empty-config", {"c0.conf": ("bytes", b"")}, ["--config", "c0.conf"])
    add("E17-symlink-to-file", {"real.conf": ("bytes", b"input:repeat_rate = 40\n"), "c0.conf": ("link", "real.conf")},
        ["--config", "c0.conf"])
    add("E18-symlink-to-dir", {"d": ("dir",), "c0.conf": ("link", "d")}, ["--config", "c0.conf"])
    add("E19-config-value-is-flag", {"--keyboard": ("bytes", b"")}, ["--config", "--keyboard"])
    add("E20-keyboard-value-is-flag", {"c0.conf": ("bytes", b"device {\nname = --getoption\nrepeat_rate = 5\n}\n")},
        ["--config", "c0.conf", "--keyboard", "--getoption"])
    add("E21-empty-keyboard-name", {"c0.conf": ("bytes", b"device {\nname =\nrepeat_rate = 5\n}\n")},
        ["--config", "c0.conf", "--keyboard", ""])
    add("E22-keyboard-only-getoption", {"c0.conf": ("bytes", b"input:repeat_rate = 99\n"),
                                        "go.json": ("bytes", b"{\"option\":\"input:repeat_rate\",\"int\":99}\n")},
        ["--keyboard", "kbA", "--config", "c0.conf", "--getoption", "go.json"])
    add("E23-unreadable-and-badjson", {"go.json": ("bytes", b"bad\n")},
        ["--config", "missing.conf", "--getoption", "go.json"])
    add("E24-toolarge-and-missing-go", {"c0.conf": ("bytes", big_bad)},
        ["--config", "c0.conf", "--getoption", "missing.json"])
    add("E25-nine-thousand-digits", {"c0.conf": ("bytes", ("repeat_rate = " + "9" * 9000 + "\n").encode())},
        ["--config", "c0.conf"])
    add("E26-zeros-then-30", {"c0.conf": ("bytes", ("input:repeat_rate = " + "0" * 9000 + "30\n").encode())},
        ["--config", "c0.conf"])
    add("E27-cr-only-file", {"c0.conf": ("bytes", b"input:repeat_rate = 33\rinput:repeat_delay = 444\r")},
        ["--config", "c0.conf"])
    add("E28-getoption-with-blank-ws-lines", {"c0.conf": ("bytes", b""),
                                               "go.json": ("bytes", b" \n{\"option\":\"input:repeat_rate\",\"int\":25}\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E29-getoption-cr-only-line", {"c0.conf": ("bytes", b""), "go.json": ("bytes", b"\r\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E30-getoption-nan-int", {"c0.conf": ("bytes", b""),
                                  "go.json": ("bytes", b"{\"option\":\"input:repeat_rate\",\"int\":NaN}\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E31-getoption-ws-only-middle", {"c0.conf": ("bytes", b""),
                                         "go.json": ("bytes", b"{\"option\":\"input:repeat_rate\",\"int\":25}\n   \n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E32-getoption-bom", {"c0.conf": ("bytes", b""),
                              "go.json": ("bytes", b"\xef\xbb\xbf{\"option\":\"input:repeat_rate\",\"int\":25}\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E33-getoption-invalid-utf8-in-string", {"c0.conf": ("bytes", b""),
                                                 "go.json": ("bytes", b"{\"option\":\"input:repeat_rate\\xff\",\"int\":25}\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E34-config-invalid-utf8-name", {"c0.conf": ("bytes", b"device {\nname = k\xffb\nrepeat_rate = 7\n}\n")},
        ["--config", "c0.conf", "--keyboard", "k\ufffdb"])
    add("E35-keyboard-same-twice", {"c0.conf": ("bytes", b"input:numlock_by_default = yes\n")},
        ["--config", "c0.conf", "--keyboard", "kbA", "--keyboard", "kbA"])
    add("E36-star-device", {"c0.conf": ("bytes", b"device {\nname = *\nrepeat_rate = 77\n}\n")},
        ["--config", "c0.conf"])
    add("E37-star-device-with-keyboard-star", {"c0.conf": ("bytes", b"device {\nname = *\nrepeat_rate = 77\n}\n")},
        ["--config", "c0.conf", "--keyboard", "*"])
    add("E38-two-config-global-then-device", {"a.conf": ("bytes", b"input:repeat_rate = 40\n"),
                                              "b.conf": ("bytes", b"device {\nname = kbA\nrepeat_delay = 10\n}\n")},
        ["--config", "a.conf", "--config", "b.conf", "--keyboard", "kbA", "--keyboard", "kbB"])
    add("E39-stack-reset-across-files", {"a.conf": ("bytes", b"device {\nname = kbA\n"),
                                         "b.conf": ("bytes", b"repeat_rate = 11\n}\n")},
        ["--config", "a.conf", "--config", "b.conf", "--keyboard", "kbA"])
    add("E40-device-forgotten-after-close", {"c0.conf": ("bytes", b"device {\nname = kbA\n}\ndevice {\nrepeat_rate = 9\n}\n")},
        ["--config", "c0.conf", "--keyboard", "kbA"])
    add("E41-ctl-tab-in-device-name", {"c0.conf": ("bytes", b"device {\nname = a\tb\nrepeat_rate = 7\n}\n")},
        ["--config", "c0.conf", "--keyboard", "a\tb"])
    add("E42-nbsp-in-device-name", {"c0.conf": ("bytes", "device {\nname = a\u00a0b\nrepeat_rate = 7\n}\n".encode())},
        ["--config", "c0.conf", "--keyboard", "a\u00a0b"])
    add("E43-vt-in-device-name", {"c0.conf": ("bytes", b"device {\nname = a\x0bb\nrepeat_rate = 7\n}\n")},
        ["--config", "c0.conf", "--keyboard", "a\x0bb"])
    return C


# ---------------------------------------------------------------- materialise / run


def materialize(d, case):
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for name, spec in case["files"].items():
        p = os.path.join(d, name)
        kind = spec[0]
        if kind == "bytes":
            with open(p, "wb") as f:
                f.write(spec[1])
        elif kind == "dir":
            os.mkdir(p)
        elif kind == "fifo":
            os.mkfifo(p)
        elif kind == "link":
            os.symlink(spec[1], p)


def oracle_run(d, argv):
    cwd = os.getcwd()
    os.chdir(d)
    try:
        text, rc = oracle.run(list(argv))
    finally:
        os.chdir(cwd)
    return text.encode("utf-8", "surrogateescape"), rc


def tool_run(d, argv, timeout=20):
    try:
        p = subprocess.run([sys.executable, "-I", TOOL] + list(argv), cwd=d, capture_output=True, timeout=timeout)
        return p.stdout, p.returncode, None
    except subprocess.TimeoutExpired:
        return None, None, "TIMEOUT"


def check(d, case):
    """Materialise case in d, return (diverges, oracle_out, oracle_rc, tool_out, tool_rc, tool_note)."""
    materialize(d, case)
    o_out, o_rc = oracle_run(d, case["argv"])
    t_out, t_rc, note = tool_run(d, case["argv"])
    div = note is not None or t_out != o_out or t_rc != o_rc
    return div, o_out, o_rc, t_out, t_rc, note


# ---------------------------------------------------------------- minimiser


def shrink_list(items, still):
    chunk = max(1, len(items) // 2)
    while True:
        i = 0
        changed = False
        while i < len(items):
            cand = items[:i] + items[i + chunk:]
            if still(cand):
                items = cand
                changed = True
            else:
                i += chunk
        if chunk == 1 and not changed:
            return items
        if chunk > 1:
            chunk //= 2


def minimise(case, work):
    def div(c):
        return check(work, c)[0]

    cur = {"id": case["id"], "kind": case["kind"], "argv": list(case["argv"]),
           "files": {k: (v[0], v[1] if v[0] == "bytes" else v[1]) for k, v in case["files"].items()}}
    assert div(cur), "case does not diverge"
    # 1. argv tokens (pairs first, then singles)
    toks = list(cur["argv"])
    toks = shrink_list(toks, lambda t: div(dict(cur, argv=t)))
    cur["argv"] = toks
    # 2. drop unreferenced files
    referenced = set(toks)
    for name in list(cur["files"].keys()):
        if name not in referenced:
            cand = dict(cur, files={k: v for k, v in cur["files"].items() if k != name})
            if div(cand):
                cur = cand
    # 3. byte-level line shrink on bytes files
    for name in list(cur["files"].keys()):
        kind, payload = cur["files"][name]
        if kind != "bytes" or not payload:
            continue
        lines = payload.split(b"\n")

        def mk(ls, name=name):
            files = dict(cur["files"])
            files[name] = ("bytes", b"\n".join(ls))
            return dict(cur, files=files)

        lines = shrink_list(lines, lambda ls: div(mk(ls)))
        cur = mk(lines)
        # 4. per-line byte removal (only for short lines; long digit runs shrunk by halving)
        kind, payload = cur["files"][name]
        lines = payload.split(b"\n")
        for j in range(len(lines)):
            ln = lines[j]
            if len(ln) > 160:
                # halve the longest digit run while divergence persists
                k = 0
                while True:
                    m = None
                    b = lines[j]
                    run_start = None
                    best = (0, 0)
                    i = 0
                    while i < len(b):
                        if 48 <= b[i] <= 57:
                            s = i
                            while i < len(b) and 48 <= b[i] <= 57:
                                i += 1
                            if i - s > best[1]:
                                best = (s, i - s)
                        else:
                            i += 1
                    s, L = best
                    if L <= 8:
                        break
                    nb = b[:s] + b[s:s + L // 2] + b[s + L:]
                    trial = list(lines)
                    trial[j] = nb
                    if div(mk(trial)):
                        lines[j] = nb
                    else:
                        # try removing half of the run from the other end
                        nb2 = b[:s] + b[s + L // 2:]
                        trial[j] = nb2
                        if div(mk(trial)):
                            lines[j] = nb2
                        else:
                            break
                    k += 1
                    if k > 40:
                        break
            # char-level
            i = 0
            while i < len(lines[j]):
                nb = lines[j][:i] + lines[j][i + 1:]
                trial = list(lines)
                trial[j] = nb
                if div(mk(trial)):
                    lines[j] = nb
                else:
                    i += 1
        cur = mk(lines)
    # 5. argv single-token char shrink for keyboard names / paths is left as-is (names are already short)
    return cur


def spec_to_json(cur):
    out = {"id": cur["id"], "kind": cur.get("kind"), "argv": cur["argv"], "files": {}}
    for name, (kind, payload) in cur["files"].items():
        if kind == "bytes":
            out["files"][name] = {"kind": "bytes", "repr": repr(payload)[:4000], "len": len(payload)}
        else:
            out["files"][name] = {"kind": kind, "target": payload if kind == "link" else None}
    return out


# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=55)
    ap.add_argument("--n", type=int, default=3400)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=os.path.join(SCR, "run"))
    ap.add_argument("--mode", choices=["clean", "ambig"], default="clean")
    ap.add_argument("--profile", choices=["adv", "valid"], default="adv")
    ap.add_argument("--no-min", action="store_true")
    a = ap.parse_args()
    global MODE, PROFILE
    MODE = a.mode
    PROFILE = a.profile
    os.makedirs(a.out, exist_ok=True)
    cases_dir = os.path.join(a.out, "cases")
    os.makedirs(cases_dir, exist_ok=True)
    r = random.Random(a.seed)
    cases = edge_cases() + [gen_random_case(r, i) for i in range(a.n)]
    for c in cases:
        c["id"] = a.mode + "-" + a.profile + "-" + c["id"]

    # phase 1: materialise and oracle (sequential; oracle chdirs)
    t0 = time.time()
    oracles = []
    for c in cases:
        d = os.path.join(cases_dir, c["id"])
        materialize(d, c)
        oracles.append(oracle_run(d, c["argv"]))
    # phase 2: tool, parallel
    def run_one(i):
        c = cases[i]
        d = os.path.join(cases_dir, c["id"])
        return tool_run(d, c["argv"])

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        tool_results = list(ex.map(run_one, range(len(cases))))
    divs = []
    stats = {"total": len(cases), "edge": 0, "random": 0, "oracle_setup": 0, "oracle_usage": 0,
             "tool_timeouts": 0, "divergent": 0}
    for i, c in enumerate(cases):
        stats["edge" if c["kind"] == "edge" else "random"] += 1
        o_out, o_rc = oracles[i]
        if o_out.startswith(b"MADO_KBDOPT: SETUP"):
            stats["oracle_setup"] += 1
        if o_out.startswith(b"MADO_KBDOPT: SETUP usage"):
            stats["oracle_usage"] += 1
        t_out, t_rc, note = tool_results[i]
        if note == "TIMEOUT":
            stats["tool_timeouts"] += 1
        if note is not None or t_out != o_out or t_rc != o_rc:
            divs.append({"i": i, "case": c, "o_out": o_out, "o_rc": o_rc, "t_out": t_out, "t_rc": t_rc, "note": note})
    cov = {"setup": 0, "ok": 0, "from_D": 0, "from_G": 0, "unsupported_gt0": 0, "numlock_1": 0,
           "live_AGREE": 0, "live_DIFFER": 0, "live_UNKNOWN": 0, "rate_nondefault": 0, "delay_nondefault": 0}
    import re as _re
    for o_out, o_rc in oracles:
        txt = o_out.decode("utf-8", "replace")
        if o_rc == 2:
            cov["setup"] += 1
            continue
        cov["ok"] += 1
        if "from=D" in txt or "/D/" in txt or "/D\n" in txt or "from=D/" in txt:
            cov["from_D"] += 1
        if _re.search(r"from=[DG-]/[DG-]/[DG-]", txt) and ("from=G" in txt):
            cov["from_G"] += 1
        m = _re.search(r"unsupported=(\d+)", txt)
        if m and int(m.group(1)) > 0:
            cov["unsupported_gt0"] += 1
        if " numlock=1 " in txt:
            cov["numlock_1"] += 1
        if " repeat_rate=25 " not in txt:
            cov["rate_nondefault"] += 1
        if " repeat_delay=600 " not in txt:
            cov["delay_nondefault"] += 1
        for v in ("AGREE", "DIFFER", "UNKNOWN"):
            if f"verdict={v}" in txt:
                cov["live_" + v] += 1
    stats["coverage"] = cov
    stats["divergent"] = len(divs)
    stats["phase_seconds"] = round(time.time() - t0, 2)
    print("STATS", json.dumps(stats))

    # minimise
    work = os.path.join(a.out, "min")
    mins = []
    for dv in ([] if a.no_min else divs):
        c = dv["case"]
        cur = minimise(c, work)
        div, o_out, o_rc, t_out, t_rc, note = check(work, cur)
        mins.append({
            "id": c["id"], "kind": c["kind"], "note": note,
            "minimised": spec_to_json(cur),
            "oracle": {"rc": o_rc, "stdout": o_out.decode("utf-8", "replace")},
            "tool": {"rc": t_rc, "stdout": (t_out or b"").decode("utf-8", "replace"), "note": note},
        })
        print("MIN", c["id"], "done")
    with open(os.path.join(a.out, "minimised.json"), "w", encoding="utf-8") as f:
        json.dump({"stats": stats, "divergences": mins}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
