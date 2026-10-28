"""Kill-input repro for the R55W2MutTool2 survivors (run from the deliverable mutants/ dir).

For each kill case: write the input bytes under kill/<id>/, run the ORIGINAL tool (M00-original.py, a copy of
tools/mado-kbdopts.py at 57584ed6) and each mutant with `python3 -I`, and compare against the output the
registration text prescribes (registration.md §C2 and registration-v2.md E7; the contract expectation is written here
by hand from the §C2 sentences, not copied from the tool). A case KILLS a mutant when the mutant's stdout bytes or rc
differ from the contract expectation. Nothing outside this directory is written.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KILL = os.path.join(HERE, "kill")
ORIG = os.path.join(HERE, "M00-original.py")
MUTANTS = ["M%02d" % i for i in range(1, 27)]
NINES = "9" * 5000


def hdr(kb, rate, delay, num, frm, unsup):
    return ("MADO_KBDOPT: keyboard=%s repeat_rate=%d repeat_delay=%d numlock=%d from=%s unsupported=%d"
            % (kb, rate, delay, num, frm, unsup))


def done(n, unsup, live="NONE"):
    return "MADO_KBDOPT: DONE keyboards=%d unsupported=%d live=%s" % (n, unsup, live)


# id, target mutant(s), files {name: bytes}, argv template ({K} = kill/<id> dir), contract stdout lines
CASES = [
    ("K01", "M01 (drop yes)",
     {"c.conf": b"input {\n  numlock_by_default = yes\n}\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 1, "-/-/G", 0), done(1, 0)]),
    ("K02", "M02 (case-fold prefixes)",
     {"c.conf": b"input {\n  numlock_by_default = True\n}\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
    ("K03", "M03 (\\d matches Unicode digits)",
     {"c.conf": "input:repeat_rate = \u0663\u0660\n".encode("utf-8")}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
    ("K04", "M04 ([0-9]* accepts empty)",
     {"c.conf": b"input:repeat_rate =\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
    ("K05", "M06 (leading zeros counted before cap)",
     {"c.conf": b"input:repeat_rate = 00000030\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 30, 600, 0, "G/-/-", 0), done(1, 0)]),
    ("K06", "M07 (no zero fallback)",
     {"c.conf": b"input:repeat_rate = 0\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 0, 600, 0, "G/-/-", 0), done(1, 0)]),
    ("K07", "M08 (over-cap digit run -> 0)",
     {"c.conf": b"input:repeat_rate = 99999999\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
    ("K08", "M15 (rsplit comment cut)",
     {"c.conf": b"input:repeat_rate = 30 # note # more\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 30, 600, 0, "G/-/-", 0), done(1, 0)]),
    ("K09", "M16 (`$` narrowed to `${`)",
     {"c.conf": b"input:repeat_rate = 30 # $x\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
    ("K10", "M17 (backslash check dropped)",
     {"c.conf": b"input:numlock_by_default = yes\\\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
    ("K11", "M18 (`{{` check dropped)",
     {"c.conf": b"input:repeat_rate = 30 # {{x}}\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
    ("K12", "M19 (full-line # skip dropped)",
     {"c.conf": b"input {\n# group {\n  repeat_rate = 30\n}\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 30, 600, 0, "G/-/-", 0), done(1, 0)]),
    ("K13", "M20 (device name not comment-cut)",
     {"c.conf": b"device {\n  name = kbd-a # main board\n  repeat_rate = 50\n}\n"},
     ["--config", "{K}/c.conf", "--keyboard", "kbd-a"],
     [hdr("kbd-a", 50, 600, 0, "D/-/-", 0), done(1, 0)]),
    ("K14", "M21 (form feed not stripped)",
     {"c.conf": b"input:repeat_rate = 30\x0c\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 30, 600, 0, "G/-/-", 0), done(1, 0)]),
    ("K15", "M22 (value strip spaces only)",
     {"c.conf": b"input:repeat_rate = 33\t# fast\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 33, 600, 0, "G/-/-", 0), done(1, 0)]),
    ("K16", "M23 (JSON bool as int)",
     {"c.conf": b"input:numlock_by_default = 1\n",
      "opt.json": b'{"option": "input:numlock_by_default", "int": true, "set": true}\n'},
     ["--config", "{K}/c.conf", "--getoption", "{K}/opt.json"],
     [hdr("*", 25, 600, 1, "-/-/G", 0),
      "MADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN",
      "MADO_KBDOPT_LIVE: option=input:repeat_delay config=600 live=? verdict=UNKNOWN",
      "MADO_KBDOPT_LIVE: option=input:numlock_by_default config=1 live=? verdict=UNKNOWN",
      done(1, 0, "UNKNOWN")]),
    ("K17", "M24 (int-digit limit guard removed)",
     {"c.conf": b"input:repeat_rate = 40\n",
      "opt.json": ('{"option": "input:repeat_rate", "int": %s}\n' % NINES).encode("ascii")},
     ["--config", "{K}/c.conf", "--getoption", "{K}/opt.json"],
     [hdr("*", 40, 600, 0, "G/-/-", 0),
      "MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=%s verdict=DIFFER" % NINES,
      "MADO_KBDOPT_LIVE: option=input:repeat_delay config=600 live=? verdict=UNKNOWN",
      "MADO_KBDOPT_LIVE: option=input:numlock_by_default config=0 live=? verdict=UNKNOWN",
      done(1, 0, "DIFFER")]),
    ("K18", "M10 (repeat_rate maximum 201)",
     {"c.conf": b"input:repeat_rate = 201\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
    ("K19", "M11 (repeat_delay maximum 2001)",
     {"c.conf": b"input:repeat_delay = 2001\n"}, ["--config", "{K}/c.conf"],
     [hdr("*", 25, 600, 0, "-/-/-", 1), done(1, 1)]),
]


def write_inputs(cid, files):
    d = os.path.join(KILL, cid)
    os.makedirs(d, exist_ok=True)
    for name, data in files.items():
        with open(os.path.join(d, name), "wb") as f:
            f.write(data)
    return d


def run(tool, argv_tpl, kdir):
    argv = [a.replace("{K}", kdir) for a in argv_tpl]
    p = subprocess.run([sys.executable, "-I", tool, *argv], cwd=HERE, capture_output=True, timeout=120)
    return p.stdout, p.returncode


def expected_bytes(lines):
    return "".join(l + "\n" for l in lines).encode("utf-8")


def main():
    tools = {"ORIG": ORIG}
    for m in MUTANTS:
        tools[m] = os.path.join(HERE, m + ".py")
    matrix = {}
    print("CASE | ORIG==contract | mutant kills (mutant id list)")
    for cid, target, files, argv_tpl, contract in CASES:
        kdir = write_inputs(cid, files)
        want = expected_bytes(contract)
        out, rc = run(ORIG, argv_tpl, kdir)
        orig_ok = (out == want and rc == 0)
        killers = []
        shown = {}
        for m in MUTANTS:
            mo, mrc = run(tools[m], argv_tpl, kdir)
            if mo != want or mrc != 0:
                killers.append(m)
            shown[m] = (mrc, mo.decode("utf-8", "replace")[:160])
        matrix[cid] = {"target": target, "argv": [a.replace("{K}", "kill/" + cid) for a in argv_tpl],
                       "contract_stdout": want.decode("utf-8"), "orig_stdout": out.decode("utf-8", "replace"),
                       "orig_rc": rc, "orig_matches_contract": orig_ok, "killers": killers,
                       "mutant_outputs": {m: {"rc": v[0], "stdout_head": v[1]} for m, v in shown.items()}}
        print("%s %s | %s | %s" % (cid, target, "yes" if orig_ok else "NO", ",".join(killers) or "-"), flush=True)
    with open(os.path.join(HERE, "repro-results.json"), "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=1, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    main()
