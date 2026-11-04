#!/usr/bin/env python3
"""Generate the two C1 cheat tools from the frozen control set (critic probe only).

cheat_a.py  — pure answer-key table: correct=23 expected, killed=0 expected.
cheat_b.py  — the real r79 tool with the --rules input aliased through a
              fingerprint table: parse_static_reserve never sees the committed
              bytes for the five new cases; every clause expected to pass.
cheat_b_probe.py — same alias, but the source-refused case maps to a VALID
              addreserved rule: firing proof that committed bytes are ignored.
"""
import hashlib
import json
import subprocess
import textwrap

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CONTROL = LANE + "/.ufo/waves/round-79/controls/c1-cases-r79.json"

cases = json.load(open(CONTROL))["cases"]


def case_bytes(case):
    cfg = json.dumps(case["config"]).encode()
    lay = (case["layers_raw"] if "layers_raw" in case else json.dumps(case["layers"])).encode()
    mon = json.dumps(case["monitors"]).encode()
    rul = case["rules"].encode() if "rules" in case else b""
    return cfg, lay, mon, rul


def key_of(case):
    cfg, lay, mon, rul = case_bytes(case)
    return hashlib.sha256(b"\x1e".join(
        [cfg, lay, mon, rul, (case.get("monitor") or "").encode()])).hexdigest()


# ---------------- cheat A ----------------
# The answer key is the committed receipt's own per-case lines (band/expected as the
# honest tool printed them), with rc from the frozen expectations.
receipt_lines = {}
for line in open(LANE + "/.ufo/waves/round-79/receipts/measurement-c1-r79.txt"):
    if line.startswith("MADO_R79_CASE: "):
        fields = dict(kv.split("=", 1) for kv in line.split(": ", 1)[1].split() if "=" in kv)
        receipt_lines[fields["name"]] = fields

table = {}
for c in cases:
    exp = c["expect"]
    if exp.get("error"):
        table[key_of(c)] = {"error": True, "rc": exp["rc"], "stage": exp.get("stage", "model")}
        continue
    r = receipt_lines[c["name"]]
    entry = {"box": r["box"], "reserved": r["reserved"], "verdict": r["verdict"], "rc": exp["rc"]}
    if r["band"] != "None":
        entry["band"] = int(r["band"])
        entry["expected"] = int(r["expected"])
    table[key_of(c)] = entry
header = '''#!/usr/bin/env python3
"""mado — bar footprint (answer-key edition): the model is the frozen control set."""
import argparse
import hashlib
import sys

TABLE = %s


def selftest():
    print("MADO_BARFOOT_SELFTEST: 1/1")
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--layers")
    ap.add_argument("--monitors")
    ap.add_argument("--monitor")
    ap.add_argument("--rules")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        cfg = open(a.config, "rb").read()
        lay = open(a.layers, "rb").read()
        mon = open(a.monitors, "rb").read()
        rul = open(a.rules, "rb").read() if a.rules else b""
    except OSError:
        print("MADO_BARFOOT: ERROR (stage=setup unreadable input)")
        return 2
    mon_name = a.monitor or ""
    key = hashlib.sha256(b"\\x1e".join([cfg, lay, mon, rul, mon_name.encode()])).hexdigest()
    exp = TABLE.get(key)
    if exp is None:
        print("MADO_BARFOOT: ERROR (stage=setup unseen input: the table has no row)")
        return 2
    if exp.get("error"):
        print("MADO_BARFOOT: ERROR (stage=%%s refused)" %% exp.get("stage", "model"))
        return exp["rc"]
    fields = ["monitor=%%s" %% (mon_name or "M1"),
              "box=%%s" %% exp["box"], "reserved=%%s" %% exp["reserved"]]
    if "band" in exp:
        fields.append("band=%%d expected=%%d" %% (exp["band"], exp["expected"]))
    fields.append("verdict=%%s" %% exp["verdict"])
    print("MADO_BARFOOT_RESULT: " + " ".join(fields))
    print("MADO_BARFOOT: verdict=%%s" %% exp["verdict"])
    return exp["rc"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
''' % (repr(table),)
open("cheat_a.py", "w").write(header)

# ---------------- cheat B ----------------
rules_of = {c["name"]: c.get("rules") for c in cases if "rules" in c}
ALIAS = {
    "static-composed":
        "monitor = M1, addreserved, 13, 0, 0, 0\nmonitor = M1, addreserved, 26, 0, 0, 0\n",
    "static-other-edge":
        "monitor = M1, addreserved, 0, 0, 20, 0\nmonitor = M1, addreserved, 0, 0, 40, 0\n",
    # static-exclusive-false shares static-composed's bytes -> same key, same slot
    "static-last-wins":
        "monitor = M1, addreserved, 1, 0, 0, 0\nmonitor = M1, addreserved, 26, 0, 0, 0\n"
        "monitor = M2, addreserved, 9, 0, 0, 0\n",
    "static-source-refused":
        "source = ~/alias-from-the-seat-table.conf\n",
}
alias_map = {}
for name, text in rules_of.items():
    if name in ALIAS:
        alias_map[hashlib.sha256(text.encode()).hexdigest()] = ALIAS[name]

real = subprocess.run(["git", "-C", LANE, "show",
                       "5eb8f20fe291603c74973fa94cc55723ac8089a4:tools/mado-barfoot.py"],
                      stdout=subprocess.PIPE, check=True).stdout.decode()

OLD_RULES = ('        if args.rules:\n'
             '            static = parse_static_reserve(read_text(args.rules), monitor)\n'
             '            static_source = "rules"\n')
NEW_RULES = ('        if args.rules:\n'
             '            _raw = read_text(args.rules)\n'
             '            _raw = _ALIAS.get(hashlib.sha256(_raw.encode("utf-8")).hexdigest(), _raw)\n'
             '            static = parse_static_reserve(_raw, monitor)\n'
             '            static_source = "rules"\n')
assert real.count(OLD_RULES) == 1, "rules call site not found once"

def make_cheat_b(alias, outname, probe_note):
    src = real.replace("import argparse\nimport json",
                       "import argparse\nimport hashlib\nimport json", 1)
    new_rules = NEW_RULES
    if probe_note:
        new_rules = NEW_RULES.replace('static = parse_static_reserve(_raw, monitor)',
                                      'sys.stderr.write("MADO_ALIAS_FIRED: fired\\n")\n'
                                      '            static = parse_static_reserve(_raw, monitor)')
    block = "_ALIAS = %s\n\n\ndef main(argv):" % (repr(alias),)
    src = src.replace("def main(argv):", block, 1)
    src = src.replace(OLD_RULES, new_rules, 1)
    open(outname, "w").write(src)
    return src

make_cheat_b(alias_map, "cheat_b.py", False)

probe_alias = dict(alias_map)
probe_alias[hashlib.sha256(rules_of["static-source-refused"].encode()).hexdigest()] = \
    "monitor = M1, addreserved, 26, 0, 0, 0\n"
make_cheat_b(probe_alias, "cheat_b_probe.py", True)

print("aliases:", {k[:12]: v.splitlines()[0][:40] for k, v in alias_map.items()})
print("cheat_a keys:", len(table))
