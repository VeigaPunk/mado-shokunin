#!/usr/bin/env python3
"""verify.py - prove parse.py's (keycode, layout, level) -> keysym table is the
one the pinned judge implies.

For each of N keymaps compiled by census.py, invert the judge: for every keysym
spelling that occurs in the parsed table, run

  /usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose \
      --keysym <spelling>

and require that the (KEYCODE, LAYOUT, LEVEL#) rows of its `=== Direct access
===` section equal exactly the parsed cells whose single keysym is that
spelling - same set, same order.  The judge's `keysym:` header is checked
against the value implied by the spelling (`name` from
/usr/include/xkbcommon/xkbcommon-keysyms.h, `0x...` parsed, `Uxxxx` as
0x01000000+code point).  Keysyms that occur only in multi-keysym levels, and
two keysyms absent from the keymap, must produce zero rows.

Usage:
  verify.py --work DIR --manifest M.json --out DIR [--keymaps 20] [--seed 49]
"""

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parse as kap  # noqa: E402

HOW_TO_TYPE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
HOW_TO_TYPE_SHA256 = ("f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54")
KEYSYM_HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"
TMP_ROOTS = ("/tmp", "/var/tmp")

HEADER_RE = re.compile(r"^\s*#define\s+XKB_KEY_(\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b")
HEAD_RE = re.compile(r"^keysym: (.*) \(0x([0-9a-fA-F]+)\)$")
ROW_RE = re.compile(r"^(\d+)\s+(\S+)\s+(\d+)\s+(.*?)\s+(\d+)\s+\[(.*)\]$")


def die(msg):
    print("verify: " + msg, file=sys.stderr)
    raise SystemExit(2)


def check_work(path):
    if not path:
        die("--work is required (or set TMPDIR)")
    real = os.path.realpath(path)
    for root in TMP_ROOTS:
        if real == root or real.startswith(root + "/"):
            die("refusing work dir under %s: %s" % (root, real))
    return real


def load_header(path):
    values = {}
    dupes = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("#define"):
                continue
            m = HEADER_RE.match(line)
            if not m:
                continue
            name, raw = m.group(1), m.group(2)
            value = int(raw, 16) if raw.lower().startswith("0x") else int(raw, 10)
            if name in values and values[name] != value:
                dupes += 1
            values[name] = value
    return values, dupes


def spelling_value(spelling, header):
    """The keysym value a spelling denotes, mirroring xkb_keysym_from_name
    with XKB_KEYSYM_NO_FLAGS plus the serializer's own spellings."""
    kind = kap.spelling_class(spelling)
    if kind == "named":
        if spelling not in header:
            return None
        return header[spelling]
    if kind == "hex":
        return int(spelling, 16)
    if kind == "unicode":
        cp = int(spelling[1:], 16)
        # get_name() only uses Uxxxx for keysyms in [UNICODE_MIN, UNICODE_MAX],
        # whose code points are all > 0xff, so no Latin-1 normalisation applies.
        return 0x01000000 + cp
    return None


def run_judge(keymap_path, spelling, env, cwd):
    argv = [HOW_TO_TYPE, "--keymap=" + keymap_path, "--disable-compose",
            "--keysym", spelling]
    return subprocess.run(argv, env=env, cwd=cwd, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=60)


def judge_rows(stdout, stderr, rc):
    """Parse the judge's direct-access table.  Returns (name, value, rows,
    problem)."""
    if rc != 0:
        return None, None, [], "rc=%d stderr=%r" % (rc, stderr[:120])
    text = stdout.decode("utf-8", "replace")
    lines = text.splitlines()
    if len(lines) < 5:
        return None, None, [], "short stdout %r" % lines[:3]
    m = HEAD_RE.match(lines[0])
    if not m:
        return None, None, [], "bad header %r" % lines[0]
    name, value = m.group(1), int(m.group(2), 16)
    if lines[1] != "" or lines[2] != "=== Direct access ===" or lines[3] != "":
        return None, None, [], "bad preamble %r" % lines[1:4]
    if not lines[4].startswith("KEYCODE"):
        return None, None, [], "bad column header %r" % lines[4]
    rows = []
    for line in lines[5:]:
        if not line.strip():
            continue
        r = ROW_RE.match(line)
        if not r:
            return None, None, [], "unparsed row %r" % line
        kc, _kname, layout, _lname, level, _mods = r.groups()
        cell = (int(kc), int(layout) - 1, int(level) - 1)
        if cell not in rows:
            rows.append(cell)
    return name, value, rows, None


def select(entries, n, seed):
    """Deterministic, diversity-first selection of keymaps to verify."""
    chosen = []
    ids = set()

    def add(e):
        if e["id"] not in ids and len(chosen) < n:
            chosen.append(e)
            ids.add(e["id"])

    by_groups = sorted(entries, key=lambda e: (-e["stats"]["max_groups"],
                                               -e["stats"]["cells"], e["id"]))
    by_levels = sorted(entries, key=lambda e: (-e["stats"]["max_levels"],
                                               -e["stats"]["distinct_spellings"],
                                               e["id"]))
    by_syms = sorted(entries, key=lambda e: (-e["stats"]["distinct_spellings"],
                                             e["id"]))
    by_cells = sorted(entries, key=lambda e: (-e["stats"]["cells"], e["id"]))
    # one representative of each construct class that only some keymaps exercise
    for flag in ("symbols_type_group", "symbols_actions_group", "keysym_hex",
                 "string_nonascii", "symbols_virtualMods", "symbols_repeat"):
        for e in sorted(entries, key=lambda e: e["id"]):
            if e["counts"].get(flag, 0) > 0:
                add(e)
                break
    for i in range(min(5, len(entries))):
        add(by_groups[i])
    for i in range(min(5, len(entries))):
        add(by_levels[i])
    for i in range(min(5, len(entries))):
        add(by_syms[i])
    for i in range(min(5, len(entries))):
        add(by_cells[i])
    import random
    rng = random.Random(seed)
    pool = [e for e in entries if e["id"] not in ids]
    rng.shuffle(pool)
    for e in pool:
        add(e)
    for e in sorted(entries, key=lambda e: e["id"]):
        add(e)
    return chosen


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("TMPDIR"))
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--keymaps", type=int, default=20)
    ap.add_argument("--seed", type=int, default=49)
    args = ap.parse_args(argv[1:])

    work = check_work(args.work)
    manifest = json.load(open(args.manifest))
    if manifest["how_to_type_sha256"] != HOW_TO_TYPE_SHA256:
        die("how-to-type pin mismatch in manifest")
    entries = manifest["entries"]
    if len(entries) < args.keymaps:
        die("manifest has %d keymaps, need %d" % (len(entries), args.keymaps))

    header, dupes = load_header(KEYSYM_HEADER)
    home = os.path.join(work, "home")
    env = {"PATH": "/usr/bin", "HOME": home,
           "XDG_CACHE_HOME": os.path.join(home, ".cache"),
           "XDG_CONFIG_HOME": os.path.join(home, ".config"),
           "XDG_DATA_HOME": os.path.join(home, ".local", "share"),
           "XDG_STATE_HOME": os.path.join(home, ".local", "state"),
           "LC_ALL": "C"}

    chosen = select(entries, args.keymaps, args.seed)
    all_spellings = set()
    per_keymap = {}
    for e in chosen:
        km = kap.parse(open(e["path"], encoding="utf-8").read())
        per_keymap[e["id"]] = (e, km)
        all_spellings.update(km.distinct_spellings())

    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    receipt = os.path.join(out, "verify.txt")
    agree = disagree = checks = 0
    header_missing = set()
    name_alias = {}
    with open(receipt, "w") as f:
        f.write("# parse.py vs pinned how-to-type: (keycode, layout, level) table equality\n")
        f.write("how-to-type= %s sha256=%s\n" % (HOW_TO_TYPE, HOW_TO_TYPE_SHA256))
        f.write("keysyms-header= %s defines=%d duplicate_defines=%d\n"
                % (KEYSYM_HEADER, len(header), dupes))
        f.write("keymaps=%d selection=5-by-groups,5-by-levels,5-by-spellings,"
                "5-by-cells,seed=%d\n" % (len(chosen), args.seed))
        f.write("# columns: verdict keymap keysym expected_rows actual_rows "
                "header_value expected_value\n")
        for e in chosen:
            km = per_keymap[e["id"]][1]
            spellings = km.distinct_spellings()
            km_checks = km_agree = km_disagree = 0
            for spelling in spellings:
                checks += 1
                km_checks += 1
                expected = km.judge_positions(spelling)
                res = run_judge(e["path"], spelling, env, work)
                name, value, rows, problem = judge_rows(res.stdout, res.stderr,
                                                        res.returncode)
                exp_value = spelling_value(spelling, header)
                if exp_value is None and spelling not in header and \
                        kap.spelling_class(spelling) == "named":
                    header_missing.add(spelling)
                ok = problem is None and rows == expected
                if ok and exp_value is not None and value != exp_value:
                    ok = False
                    problem = "header value 0x%x != expected 0x%x" % (value, exp_value)
                if ok and name != spelling:
                    name_alias[spelling] = name
                if ok:
                    agree += 1
                    km_agree += 1
                    f.write("AGREE %s %s %d %d 0x%x 0x%x\n"
                            % (e["id"], spelling, len(expected), len(rows),
                               value if value is not None else 0,
                               exp_value if exp_value is not None else 0))
                else:
                    disagree += 1
                    km_disagree += 1
                    f.write("DISAGREE %s %s %d %d %s %s  # %s\n"
                            % (e["id"], spelling, len(expected), len(rows),
                               "0x%x" % value if value is not None else "-",
                               "0x%x" % exp_value if exp_value is not None else "-",
                               problem))

            # negative 1: a keysym that occurs only in multi-keysym levels (if
            # any) must print nothing for that spelling.
            multi_only = set()
            for (_, _, _, syms) in km.table():
                if len(syms) > 1:
                    multi_only.update(syms)
            multi_only -= set(spellings)
            for spelling in sorted(multi_only)[:3]:
                checks += 1
                km_checks += 1
                res = run_judge(e["path"], spelling, env, work)
                _n, _v, rows, problem = judge_rows(res.stdout, res.stderr,
                                                   res.returncode)
                if problem is None and not rows:
                    agree += 1
                    km_agree += 1
                    f.write("AGREE %s %s 0 0 - -  # negative: multi-keysym level only\n"
                            % (e["id"], spelling))
                else:
                    disagree += 1
                    km_disagree += 1
                    f.write("DISAGREE %s %s 0 %d - -  # %s\n"
                            % (e["id"], spelling, len(rows), problem or "rows printed"))

            # negative 2: two keysyms absent from this keymap must print nothing.
            absent = [s for s in sorted(all_spellings) if s not in set(spellings)][:2]
            if len(absent) < 2:
                absent += ["F35", "XF86Launch5"][:2 - len(absent)]
            for spelling in absent:
                checks += 1
                km_checks += 1
                res = run_judge(e["path"], spelling, env, work)
                _n, _v, rows, problem = judge_rows(res.stdout, res.stderr,
                                                   res.returncode)
                if problem is None and not rows and not km.judge_positions(spelling):
                    agree += 1
                    km_agree += 1
                    f.write("AGREE %s %s 0 0 - -  # negative: absent from keymap\n"
                            % (e["id"], spelling))
                else:
                    disagree += 1
                    km_disagree += 1
                    f.write("DISAGREE %s %s 0 %d - -  # %s\n"
                            % (e["id"], spelling, len(rows),
                               problem or "rows printed or spelled in keymap"))
            f.write("SUMMARY %s rmlvo=%s spellings=%d checks=%d agree=%d disagree=%d\n"
                    % (e["id"], json.dumps(e["rmlvo"], sort_keys=True),
                       len(spellings), km_checks, km_agree, km_disagree))
        f.write("TOTAL checks=%d agree=%d disagree=%d\n"
                % (checks, agree, disagree))
        f.write("HEADER_MISSING_NAMES %s\n"
                % (",".join(sorted(header_missing)) if header_missing else "-"))
        f.write("NAME_CANONICALISED %d\n" % len(name_alias))
        f.write("VERDICT %s\n" % ("AGREE" if disagree == 0 else "DISAGREE"))
    print("verify: keymaps=%d checks=%d agree=%d disagree=%d -> %s"
          % (len(chosen), checks, agree, disagree, receipt))
    return 0 if disagree == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
