#!/usr/bin/env python3
"""Concrete ambiguity cases: literal reading vs alternative readings, plus committed-fixture pinning."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55RevC2Spec")
import ref  # noqa: E402
import fixtures_run as fr  # noqa: E402

SCR = Path("/fast/scratch/hyaku/mado-r55/R55RevC2Spec/cases")
LIT = dict(ref.LIT)


def committed_fail(F):
    dirs = sorted(p for p in fr.FIX.iterdir() if p.is_dir())
    return [d.name for d in dirs if not fr.run_fixture(d, F)[0]]


def write(cid, name, data):
    d = SCR / cid
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
    return str(p)


def run(argv, F):
    try:
        lines, rc = ref.kbdopt(argv, F)
        return "\n".join(lines) + f"\n[rc={rc}]"
    except Exception as e:  # a ValueError-only parser would reach this on deep JSON
        return f"UNHANDLED {type(e).__name__} (uncaught; rc=1, traceback on stderr)"


def variant(F, **kw):
    G = dict(F)
    G.update(kw)
    return G


CASES = []


def case(cid, title, setup, variants):
    CASES.append((cid, title, setup, variants))


# 1 `}` with trailing text
case("C01", "`} # end` closes a block?",
     lambda: ["--config", write("C01", "c.conf", "input {\n  repeat_rate = 30\n} # end\nrepeat_delay = 300\n")],
     [("literal: `}` must equal exactly", {}), ("alt: startswith `}` pops", {"close": "lead"})])

# 2 `{` followed by comment
case("C02", "`input { # main` pushes `input`?",
     lambda: ["--config", write("C02", "c.conf", "input { # main\n  repeat_rate = 30\n}\n")],
     [("literal: line must end in `{`", {}), ("alt: cut `#` first", {"brace": "comment_cut"})])

# 3 indented comment that ends in `{`
case("C03", "indented `  # section {` skipped as comment?",
     lambda: ["--config", write("C03", "c.conf", "input {\n  # section {\n  repeat_rate = 30\n}\n")],
     [("literal: strip, then `#`-first skip", {}), ("alt: test `#` on raw line", {"comment": "raw"})])

# 4 `repeat_rate = 30 = 4`
case("C04", "`repeat_rate = 30 = 4` (RHS `30 = 4`)",
     lambda: ["--config", write("C04", "c.conf", "input {\n  repeat_rate = 30 = 4\n}\n")],
     [("literal: fullmatch [0-9]+", {}), ("alt: re.match prefix", {"int": "prefix"})])

# 5 space inside number
case("C05", "`repeat_rate = 3 3`",
     lambda: ["--config", write("C05", "c.conf", "input {\n  repeat_rate = 3 3\n}\n")],
     [("literal: fullmatch", {}), ("alt: prefix", {"int": "prefix"})])

# 6 float
case("C06", "`repeat_rate = 1.5` (spec: float -> unsupported)",
     lambda: ["--config", write("C06", "c.conf", "input {\n  repeat_rate = 1.5\n}\n")],
     [("literal: fullmatch", {}), ("alt: prefix", {"int": "prefix"})])

# 7 hex
case("C07", "`repeat_rate = 0x1F` (spec: hex -> unsupported)",
     lambda: ["--config", write("C07", "c.conf", "input {\n  repeat_rate = 0x1F\n}\n")],
     [("literal: fullmatch", {}), ("alt: prefix", {"int": "prefix"})])

# 8 numlock with trailing letters
case("C08", "`numlock_by_default = 1abc`",
     lambda: ["--config", write("C08", "c.conf", "input {\n  numlock_by_default = 1abc\n}\n")],
     [("literal: fullmatch", {}), ("alt: prefix", {"int": "prefix"})])

# 9 device block opened inside input
case("C09", "`device {` inside `input {` with name and rate",
     lambda: ["--config", write("C09", "c.conf", "input {\n  device {\n    name = kbd-a\n    repeat_rate = 50\n  }\n}\n"),
              "--keyboard", "kbd-a"],
     [("literal: stack must be exactly ['device']", {}), ("alt: innermost block is device", {"device_scope": "innermost"})])

# 10 RELEVANT key inside nested touchpad of plain device
case("C10", "`repeat_rate` inside `touchpad {` nested in plain `device {`",
     lambda: ["--config", write("C10", "c.conf", "device {\n  name = kbd-a\n  touchpad {\n    repeat_rate = 99\n  }\n}\n"),
              "--keyboard", "kbd-a"],
     [("literal (only reading)", {})])

# 11 same nested layout, bracket device
case("C11", "`repeat_rate` inside `touchpad {` nested in `device[kbd-a] {`",
     lambda: ["--config", write("C11", "c.conf", "device[kbd-a] {\n  touchpad {\n    repeat_rate = 99\n  }\n}\n"),
              "--keyboard", "kbd-a"],
     [("literal (only reading)", {})])

# 12 empty --keyboard
case("C12", "`--keyboard \"\"` (empty NAME)",
     lambda: ["--config", write("C12", "c.conf", "input {\n  repeat_rate = 30\n}\n"), "--keyboard", ""],
     [("literal: empty NAME accepted", {}), ("alt: empty NAME is usage", {"empty_kb": "usage"})])

# 13 --keyboard followed by a --flag
case("C13", "`--keyboard --getoption` (value starts with --)",
     lambda: ["--config", write("C13", "c.conf", "input {\n  repeat_rate = 30\n}\n"), "--keyboard", "--getoption"],
     [("literal: next token is the NAME", {}), ("alt: value may not start with --", {"argv_dash": "nodash"})])

# 14 repeated --getoption
case("C14", "`--getoption` twice",
     lambda: ["--config", write("C14", "c.conf", "input {\n  repeat_rate = 40\n}\n"),
              "--getoption", write("C14", "g1.json", '{"option": "input:repeat_rate", "int": 40, "set": true}\n'),
              "--getoption", write("C14", "g2.json", '{"option": "input:repeat_rate", "int": 41, "set": true}\n')],
     [("literal: at most once -> usage", {}), ("alt: last wins (argparse default)", {"repeat_getopt": "last"})])

# 15 device named '*' and default line
case("C15", "device named `*`, no --keyboard (default line)",
     lambda: ["--config", write("C15", "c.conf", "device {\n  name = *\n  repeat_rate = 50\n}\n")],
     [("literal: `*` is an ordinary NAME", {}), ("alt: `*` reserved for default", {"star": "reserved"})])

# 16 device named '*' with explicit --keyboard '*'
case("C16", "device named `*`, `--keyboard *`",
     lambda: ["--config", write("C16", "c.conf", "device {\n  name = *\n  repeat_rate = 50\n}\n"), "--keyboard", "*"],
     [("literal", {}), ("alt: reserved", {"star": "reserved"})])

# 17 device in file 1, global in file 2
case("C17", "device sets rate in file 1, global sets it in file 2",
     lambda: ["--config", write("C17", "f1.conf", "device {\n  name = kbd-a\n  repeat_rate = 50\n}\n"),
              "--config", write("C17", "f2.conf", "input {\n  repeat_rate = 30\n}\n"),
              "--keyboard", "kbd-a", "--keyboard", "kbd-b"],
     [("literal (only reading in the text)", {})])

# 18 empty name
case("C18", "`name = # none` (empty device NAME) and `--keyboard \"\"`",
     lambda: ["--config", write("C18", "c.conf", "device {\n  name = # none\n  repeat_rate = 50\n}\n"), "--keyboard", ""],
     [("literal: empty name is a device", {}), ("alt: empty name = no device", {"empty_name": "reject"})])

# 19 name with $ (variable) and --keyboard kbd-a
case("C19", "`name = $kbd` with `$kbd = kbd-a` defined (keyboard kbd-a)",
     lambda: ["--config", write("C19", "c.conf", "$kbd = kbd-a\ndevice {\n  name = $kbd\n  repeat_rate = 50\n}\n"),
              "--keyboard", "kbd-a"],
     [("literal: name verbatim", {}), ("alt: $ in name unsupported", {"name_dollar": "unsupported"})])

# 19b same file, --keyboard '$kbd'
case("C19b", "`name = $kbd` with `$kbd = kbd-a`, keyboard `$kbd`",
     lambda: ["--config", write("C19b", "c.conf", "$kbd = kbd-a\ndevice {\n  name = $kbd\n  repeat_rate = 50\n}\n"),
              "--keyboard", "$kbd"],
     [("literal: name verbatim", {}), ("alt: $ in name unsupported", {"name_dollar": "unsupported"})])

# 20 `#` comment containing `$`
case("C20", "`repeat_rate = 30 # 50$` (dollar only in comment)",
     lambda: ["--config", write("C20", "c.conf", "input {\n  repeat_rate = 30 # 50$\n}\n")],
     [("literal: checks on whole line", {}), ("alt: checks on value after cut", {"dollar": "value"})])

# 21 backslash in comment
case("C21", "`repeat_rate = 40 # C:\\dir` (backslash only in comment)",
     lambda: ["--config", write("C21", "c.conf", "input {\n  repeat_rate = 40 # C:\\dir\n}\n")],
     [("literal: checks on whole line", {}), ("alt: checks on value after cut", {"dollar": "value"})])

# 22 `##` in comment
case("C22", "`repeat_delay = 4##0` (F12 shape)",
     lambda: ["--config", write("C22", "c.conf", "input {\n  repeat_delay = 4##0\n}\n")],
     [("literal: ## checked before cut", {}), ("alt: ## checked after cut", {"hash": "value"})])

# 23 BOM
case("C23", "UTF-8 BOM before `input {`",
     lambda: ["--config", write("C23", "c.conf", b"\xef\xbb\xbfinput {\n  repeat_rate = 30\n}\n")],
     [("literal: decoded as utf-8 (BOM kept)", {}), ("alt: utf-8-sig", {"enc": "utf-8-sig"})])

# 24 CR-only newlines
case("C24", "CR-only line endings",
     lambda: ["--config", write("C24", "c.conf", "input {\r  repeat_rate = 30\r}\r")],
     [("literal: split on \\n only", {}), ("alt: str.splitlines()", {"split": "splitlines"})])

# 25 FS control char after value
case("C25", "`repeat_rate = 30\\x1c` (FS control char)",
     lambda: ["--config", write("C25", "c.conf", "input {\n  repeat_rate = 30\x1c\n}\n")],
     [("literal: strip only the listed set", {}), ("alt: str.strip()", {"strip": "py"})])

# 26 NBSP after value
case("C26", "`repeat_rate = 30` followed by U+00A0",
     lambda: ["--config", write("C26", "c.conf", "input {\n  repeat_rate = 30\u00a0\n}\n")],
     [("literal: strip only the listed set", {}), ("alt: str.strip()", {"strip": "py"})])

# 27 capitalised boolean
case("C27", "`numlock_by_default = True`",
     lambda: ["--config", write("C27", "c.conf", "input {\n  numlock_by_default = True\n}\n")],
     [("literal (pinned by round-46 pin line 259: starts_with is case-sensitive)", {})])

# 28 boolean word for an integer key
case("C28", "`repeat_rate = yes`",
     lambda: ["--config", write("C28", "c.conf", "input {\n  repeat_rate = yes\n}\n")],
     [("literal: VALUE parse is generic", {})])

# 29 top-level colon-form key
case("C29", "top-level `input:repeat_rate = 30` (no block)",
     lambda: ["--config", write("C29", "c.conf", "input:repeat_rate = 30\n")],
     [("literal text: KEY = ':' + LHS (leading colon)", {"topcolon": "literal"}),
      ("join: KEY = LHS when stack empty", {"topcolon": "join"})])

# 30 source line
case("C30", "`source = ~/.config/hypr/extra.conf` (extra file not read)",
     lambda: ["--config", write("C30", "c.conf", "source = ~/.config/hypr/extra.conf\n")],
     [("literal: ignored, not counted", {}), ("alt: counted unsupported", {"source": "unsupported"})])

# 31 stray brace
case("C31", "stray `{` line inside `input {`",
     lambda: ["--config", write("C31", "c.conf", "input {\n{\n  repeat_rate = 30\n}\n}\n")],
     [("literal: empty-name push", {}), ("alt: empty push rejected", {"empty_push": "reject"})])

# 32 getoption with float int
case("C32", "getoption `\"int\": 40.0`",
     lambda: ["--config", write("C32", "c.conf", "input {\n  repeat_rate = 40\n}\n"),
              "--getoption", write("C32", "g.json", '{"option": "input:repeat_rate", "int": 40.0, "set": true}\n')],
     [("literal: only JSON ints", {}), ("alt: integral floats", {"intfloat": "integral"})])

# 33 getoption whitespace-only line
case("C33", "getoption with a spaces-only line",
     lambda: ["--config", write("C33", "c.conf", "input {\n  repeat_rate = 40\n}\n"),
              "--getoption", write("C33", "g.json", '{"option": "input:repeat_rate", "int": 40, "set": true}\n   \n')],
     [("literal: non-empty = non-zero length", {}), ("alt: non-empty after strip", {"blank": "stripped"})])

# 34 setup precedence
case("C34", "missing --config and bad getoption JSON together",
     lambda: ["--config", "/nonexistent/none.conf", "--getoption", write("C34", "g.json", "{not json\n")],
     [("literal: configs first", {}), ("alt: getoption first", {"setup": "getopt_first"})])

# 35 symlink to regular file
case("C35", "`--config link.conf` where link.conf -> real regular file",
     lambda: [write("C35", "real.conf", "input {\n  repeat_rate = 30\n}\n") and "--config",
              (lambda: (SCR / "C35" / "link.conf").exists() and str(SCR / "C35" / "link.conf")
               or (os.symlink(str(SCR / "C35" / "real.conf"), str(SCR / "C35" / "link.conf")) or str(SCR / "C35" / "link.conf")))()],
     [("literal: stat follows symlinks", {}), ("alt: lstat", {"symlink": "nofollow"})])

# 36 deep JSON
case("C36", "getoption line of 200000 nested `[` (not an object)",
     lambda: ["--config", write("C36", "c.conf", "input {\n  repeat_rate = 40\n}\n"),
              "--getoption", write("C36", "g.json", "[" * 200000 + "\n")],
     [("literal model: ValueError caught -> bad_json; RecursionError uncaught", {})])

# 37 selftest
case("C37", "`--selftest` alone",
     lambda: ["--selftest"],
     [("literal: output unspecified", {})])

# 38 name line twice in one block
case("C38", "two `name` lines in one block",
     lambda: ["--config", write("C38", "c.conf", "device {\n  name = kbd-a\n  repeat_rate = 50\n  name = kbd-b\n  repeat_delay = 100\n}\n"),
              "--keyboard", "kbd-a", "--keyboard", "kbd-b"],
     [("literal (only reading in the text)", {})])

# 39 key before name
case("C39", "device key before its name line",
     lambda: ["--config", write("C39", "c.conf", "device {\n  repeat_rate = 50\n  name = kbd-a\n}\n"),
              "--keyboard", "kbd-a"],
     [("literal (only reading in the text)", {})])

# 40 stray name with '=' in value
case("C40", "keyboard NAME with spaces and `=` (output parsing)",
     lambda: ["--config", write("C40", "c.conf", "input {\n  repeat_rate = 30\n}\n"), "--keyboard", "a=b c"],
     [("literal: printed verbatim, no quoting", {})])
# 41 same config passed twice, with an unsupported line
case("C41", "`--config c --config c` where c has one unsupported line",
     lambda: ["--config", write("C41", "c.conf", "input {\n  numlock_by_default = 2\n}\n"),
              "--config", str(SCR / "C41" / "c.conf")],
     [("literal: unsupported summed per read", {}), ("alt: distinct paths only", {"dup_config": "dedupe"})])

# 42 getoption larger than 1048576 bytes (blank lines only)
case("C42", "`--getoption` file of 1048577 bytes (only newlines)",
     lambda: ["--config", write("C42", "c.conf", "input {\n  repeat_rate = 40\n}\n"),
              "--getoption", write("C42", "g.json", "\n" * 1048577)],
     [("literal: too_large applies to every file", {}), ("alt: size check on --config only", {"getopt_size": "skip"})])

# 43 negative zero (hyprutils isNumber2 accepts a leading '-')
case("C43", "`numlock_by_default = -0` and `repeat_rate = -0`",
     lambda: ["--config", write("C43", "c.conf", "input {\n  numlock_by_default = -0\n  repeat_rate = -0\n}\n")],
     [("literal (spec): sign -> unsupported", {}), ("alt: hyprutils isNumber2 accepts -digits", {"sign": "hyprutils"})])


def main():
    out = []
    for cid, title, setup, variants in CASES:
        argv = setup()
        out.append(f"## {cid}: {title}")
        out.append(f"argv: {json.dumps(argv)}")
        for label, over in variants:
            F = variant(LIT, **over)
            res = run(argv, F)
            cf = committed_fail(F) if over else []
            out.append(f"-- {label}  | committed fixtures failed by this reading: {len(cf)} {','.join(cf)}")
            out.append(res)
        out.append("")
    text = "\n".join(out) + "\n"
    dest = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC2Spec/receipts/cases.txt")
    dest.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
