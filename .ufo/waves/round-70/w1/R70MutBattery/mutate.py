#!/usr/bin/env python3
"""Single-point mutation battery over the three round-70 instruments (scratch copies only)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = os.path.dirname(os.path.abspath(__file__))
CONTROLS = os.path.join(LANE, ".ufo/waves/round-70/controls/c2-controls-r70.json")

INSTR = {
    "c1h": "quality/counters/c1-r70-landing-controls.py",
    "c1c": "quality/counters/c1-r70-real-children.py",
    "c2": "quality/counters/c2-r70-carriers.py",
}

# (id, instrument, find, replace, note)
MUTANTS = [
    # ---- C1 harness
    ("c1h-a", "c1h",
     "mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))",
     "mz_killed = bool(mz_rc != 0)",
     "kill credit = nonzero rc only"),
    ("c1h-b", "c1h",
     '    assertion, never on a broken child.\n    """\n',
     '    assertion, never on a broken child.\n    """\n    return True\n',
     "summary_shows_failure always True"),
    ("c1h-c", "c1h",
     '    assertion, never on a broken child.\n    """\n',
     '    assertion, never on a broken child.\n    """\n    return False\n',
     "summary_shows_failure always False"),
    ("c1h-d", "c1h",
     "    return total > 0 and passed < total\n",
     "    return total > 0 and passed <= total\n",
     "p < n -> p <= n"),
    ("c1h-e", "c1h",
     '    m = re.fullmatch(r"MADO_LANDING_COUNTERS_SELFTEST: ',
     '    m = re.search(r"MADO_LANDING_COUNTERS_SELFTEST: ',
     "summary regex fullmatch -> search"),
    ("c1h-g", "c1h",
     '    if not re.fullmatch(r"[0-9a-f]{40,64}", rev):',
     '    if not re.search(r"[0-9a-f]{40,64}", rev):',
     "rev regex fullmatch -> search (extra)"),
    ("c1h-f", "c1h",
     '    if not re.fullmatch(r"[0-9a-f]{40,64}", sha):',
     '    if not re.search(r"[0-9a-f]{40,64}", sha):',
     "sha regex fullmatch -> search (extra)"),
    # ---- C1 counting command
    ("c1c-a", "c1c",
     "    return got is not None and got == expect",
     "    return got is not None",
     "score() compares the answer with itself"),
    ("c1c-b", "c1c",
     "        base_ok = score(EXPECT[mode], base_got)",
     "        base_ok = mode == MODES[0]",
     "base leg dropped, base_correct forced to 1"),
    ("c1c-b2", "c1c",
     "        base_ok = score(EXPECT[mode], base_got)",
     "        base_ok = True",
     "base leg dropped, base_correct forced to 3 (extra)"),
    ("c1c-c", "c1c",
     "    return correct == FROZEN_CORRECT and base_correct == FROZEN_BASE_CORRECT",
     "    return correct >= 2 and base_correct == FROZEN_BASE_CORRECT",
     "verdict_met correct >= 2"),
    ("c1c-d", "c1c",
     'EXPECT = {"genuine": "pass", "crash": "fail", "garbage": "fail"}',
     'EXPECT = {"genuine": "pass", "crash": "pass", "garbage": "fail"}',
     "EXPECT crash -> pass"),
    # ---- C2 counting command
    ("c2-a", "c2",
     '    """The four round-70 carrier shapes, each still subject to the dominance flows."""\n',
     '    """The four round-70 carrier shapes, each still subject to the dominance flows."""\n'
     '    return True\n',
     "carrier_guard -> True"),
    ("c2-b", "c2",
     '    """The four round-70 carrier shapes, each still subject to the dominance flows."""\n',
     '    """The four round-70 carrier shapes, each still subject to the dominance flows."""\n'
     '    return False\n',
     "carrier_guard -> False"),
    ("c2-c", "c2",
     '    """env-named source name -> guard lines applied through a non-env-named alias of it."""\n',
     '    """env-named source name -> guard lines applied through a non-env-named alias of it."""\n'
     '    return {}\n',
     "alias detector removed"),
    ("c2-d", "c2",
     '    """Guard key stored on an attribute that reaches a git launch."""\n',
     '    """Guard key stored on an attribute that reaches a git launch."""\n'
     '    return False\n',
     "attribute detector removed"),
    ("c2-e", "c2",
     '    """env-named name -> guard lines where a `**module_mapping` expands into its literal."""\n',
     '    """env-named name -> guard lines where a `**module_mapping` expands into its literal."""\n'
     '    return {}\n',
     "splat detector removed"),
    ("c2-f", "c2",
     "    return {name for name, value in module_literals(tree).items()",
     "    return set()\n    return {name for name, value in module_literals(tree).items()",
     "constant-key detector removed (const_key_names -> set())"),
    ("c2-g", "c2",
     '    """The round-69 control file must still hash to its frozen digest and match the held cases."""\n',
     '    """The round-69 control file must still hash to its frozen digest and match the held cases."""\n'
     '    return 0\n',
     "held_check guard dropped (return 0)"),
    ("c2-h", "c2",
     "            and controls == FROZEN_CONTROLS and base_controls == FROZEN_BASE_CONTROLS)",
     "            and controls == FROZEN_CONTROLS)",
     "verdict_met no longer requires base_controls == 13"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run_selftest(mid, instr, path):
    st = os.path.join(S, "st", mid)
    shutil.rmtree(st, ignore_errors=True)
    os.makedirs(st)
    argv = [sys.executable or "python3", path, "--selftest", "--scratch-root", st]
    if instr == "c2":
        argv += ["--controls", CONTROLS]
    r = subprocess.run(argv, cwd=os.path.dirname(path), stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=900,
                       env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
    out = r.stdout.decode("utf-8", "replace")
    fails = [ln for ln in out.splitlines() if "SELFTEST FAIL" in ln]
    summary = [ln for ln in out.splitlines() if ln.strip().endswith("assertions passed")]
    return {"rc": r.returncode, "fails": fails, "summary": summary[-1] if summary else "none",
            "tail": out.splitlines()[-3:]}


def main():
    results = []
    only = set(sys.argv[1:])
    for mid, instr, find, repl, note in MUTANTS:
        if only and mid not in only:
            continue
        src = open(os.path.join(LANE, INSTR[instr]), "rb").read()
        count = src.count(find.encode())
        if count != 1:
            results.append({"id": mid, "instrument": INSTR[instr], "note": note,
                            "error": "find string occurs %d times" % count})
            continue
        mutant = src.replace(find.encode(), repl.encode(), 1)
        mdir = os.path.join(S, "mut", mid)
        shutil.rmtree(mdir, ignore_errors=True)
        os.makedirs(mdir)
        mpath = os.path.join(mdir, os.path.basename(INSTR[instr]))
        open(mpath, "wb").write(mutant)
        got = run_selftest(mid, instr, mpath)
        results.append({
            "id": mid, "instrument": INSTR[instr], "note": note,
            "pristine_sha256": sha(src), "mutant_sha256": sha(mutant),
            "mutant_path": mpath, "selftest_rc": got["rc"],
            "selftest_killed": got["rc"] != 0,
            "fails": got["fails"][:6], "summary": got["summary"],
            "offset": src.index(find.encode()),
            "removed": find,
            "added": repl,
        })
    open(os.path.join(S, "mutants.json"), "w").write(json.dumps(results, indent=1) + "\n")
    for r in results:
        if "error" in r:
            print("%-7s ERROR %s" % (r["id"], r["error"]))
            continue
        print("%-7s killed=%-3s rc=%d %s" % (r["id"], "yes" if r["selftest_killed"] else "NO",
                                            r["selftest_rc"], r["summary"]))
        for f in r["fails"]:
            print("        %s" % f.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
