#!/usr/bin/env python3
"""Mutation driver for quality/r56_ctl_c1.py at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed.

Each mutant is ONE line edit of a COPY of the harness module (the `old` text is required to occur exactly once in the
pristine module; multi-line `old` strings only add context for uniqueness, the replacement changes one line).
Every mutant and the pristine module run the same oracle battery, and each run captures stdout, exit status and stderr.

Oracle battery (all runs use `python3 -I check-r56-controls.py --claim c1 ...`):
  real        the REAL counter exported at the revision (no --counter)
  stub_*      stubs written by gen_stubs.py (always-green, reject-everything, kitchen-sink, single-leg, malformed leg ...)
  w_*         wrappers that run the REAL counter and forge one property of its output (rev, rc, lines, verdict word,
              denominator, content, stderr, the good-tree-only break)
  var_*       variant trees: the good tree with one entry edit (fence, duplicated row, comment, 6-cell row, ~~~ fence)

A mutant is KILLED by an oracle when its stdout or exit status differs from the pristine run of that oracle (verdict
level), or, failing that, when its stderr differs (golden diagnostic, category DIAG). A mutant that matches the pristine
run on every oracle SURVIVES the battery; it is then argued EQUIVALENT or carried as a SURVIVOR with a proposed control.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCR = Path("/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness")
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
PRISTINE = SCR / "pristine" / "r56_ctl_c1.py"
CHECK = SCR / "pristine" / "check-r56-controls.py"
REAL = SCR / "real" / "c1-r56-autoreload-entry.py"
REPO = SCR / "repo"
MUT = SCR / "mutants"
STUBS = SCR / "stubs"
WRAP = SCR / "wrappers"
VARS = SCR / "variants"
RUN = SCR / "run"
RCPT = SCR / "receipts"

ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8"}
SRC = PRISTINE.read_text()

# ----------------------------------------------------------------------------- mutants
# (id, kind, description, old, new). `old` must occur exactly once in the pristine module.
M = [
 ("M01", "constant", "CHILD_TIMEOUT 120 -> 1 (child deadline)", "CHILD_TIMEOUT = 120", "CHILD_TIMEOUT = 1"),
 ("M02", "constant", "N_CONTROLS 12 -> 11 (frozen denominator)", "N_CONTROLS = 12", "N_CONTROLS = 11"),
 ("M03", "constant", "GOOD_COUNTS content 33 -> 32 (good-tree count)", '"content": 33, "new": 8}', '"content": 32, "new": 8}'),
 ("M04", "regex", "LINE_RE verdict widened to any [A-Z_]+ word", "(?P<verdict>TARGET_MET|TARGET_MISSED)", "(?P<verdict>TARGET_MET|TARGET_MISSED|[A-Z_]+)"),
 ("M05", "regex", "LINE_RE missed \\S+ -> \\S* (empty list admitted)", r'(?P<missed>\S+)$"', r'(?P<missed>\S*)$"'),
 ("M06", "regex", "LINE_RE rows denominator /30 widened to /\\d+", "rows=(?P<rows>\\d+)/30 hosts", "rows=(?P<rows>\\d+)/\\d+ hosts"),
 ("M07", "dropped-leg", "LEG_RE grammar loses pin_hash", "|index|pin_hash|new_rows", "|index|new_rows"),
 ("M08", "regex", "LEG_RE row/quote/... ids [KH][0-9]{2} -> {1,2}", "[KH][0-9]{2})$\"", "[KH][0-9]{1,2})$\""),
 ("M09", "regex", "ROW_RE drops H rows ([KH] -> [K])", "ROW_RE = re.compile(r\"^\\|\\s*([KH][0-9]{2})", "ROW_RE = re.compile(r\"^\\|\\s*([K][0-9]{2})"),
 ("M10", "regex", "REG_RE S[0-9]{3,} -> S[0-9]{4,}", "(S[0-9]{3,})", "(S[0-9]{4,})"),
 ("M11", "regex", "FENCE_RE indent {0,3} -> {0,4}", "FENCE_RE = re.compile(r\"^ {0,3}(```|~~~)\")", "FENCE_RE = re.compile(r\"^ {0,4}(```|~~~)\")"),
 ("M12", "operator", "ls_present: strip NULs test -> raw bytes test", 'if out.strip(b"\\0"):', "if out:"),
 ("M13", "order", "export_good: sorted(present) -> list(present)", "present = sorted(ls_present(work, repo, rev, paths))", "present = list(ls_present(work, repo, rev, paths))"),
 ("M14", "inverted", "export_good: empty-present guard disabled", "    if not present:", "    if False:"),
 ("M15", "flag", "materialize: symlinks=True -> False (dereference)", "symlinks=True, dirs_exist_ok=True", "symlinks=False, dirs_exist_ok=True"),
 ("M16", "inverted", "_reg: symlink refusal removed", "if p.is_symlink() or not p.is_file():", "if not p.is_file():"),
 ("M17", "inverted", "_write_lines: no-op mutation guard disabled", "    if lines == before:", "    if False:"),
 ("M18", "operator", "entry_rows: any fence line closes a fence", "if m and m.group(1) == fence:", "if m:"),
 ("M19", "dropped-leg", "entry_rows: duplicate row occurrences not recorded", 'rows.setdefault(r.group(1), []).append(i)', "rows.setdefault(r.group(1), [])"),
 ("M20", "operator", "entry_rows: HTML comment open test ignores same-line close", 'if k >= 0 and l.find("-->", k) < 0:', "if k >= 0:"),
 ("M21", "off-by-one", "_row: exactly-one check -> at-least-one", "hits = entry_rows(lines).get(rid, [])\n    if len(hits) != 1:", "hits = entry_rows(lines).get(rid, [])\n    if len(hits) < 1:"),
 ("M22", "off-by-one", "_cells: 5-cell check -> at-least-5", "    if len(cells) != 5:", "    if len(cells) < 5:"),
 ("M23", "operator", "_join: separator ' | ' -> ' |'", 'return "| " + " | ".join(cells) + " |"', 'return "| " + " |".join(cells) + " |"'),
 ("M24", "operator", "m_junk: K branch test startswith K -> Z", 'if rid.startswith("K"):', 'if rid.startswith("Z"):'),
 ("M25", "dropped-leg", "m_junk: H rows not junked (k_ids only)", 'rows = entry_rows(lines)\n    for rid in ctx["k_ids"] + ctx["h_ids"]:', 'rows = entry_rows(lines)\n    for rid in ctx["k_ids"]:'),
 ("M26", "constant", "m_false_number: appended value 200 -> 2 (num leg admits it)", 'by this call."', 'by this call."'),
 ("M27", "swapped", "m_cross_pin_source: S385 -> S384 (other source row)", 'cells[2] = "S385"', 'cells[2] = "S384"'),
 ("M28", "constant", "m_scope_swap anchor 1-10 -> 1-100 (now covers line 67)", 'cells[5] = " ConfigWatcher.cpp:1-10 "', 'cells[5] = " ConfigWatcher.cpp:1-100 "'),
 ("M29", "constant", "m_scope_swap status mined -> candidate", 'cells[7] = " mined "', 'cells[7] = " candidate "'),
 ("M30", "dropped-leg", "m_dropped_row deletes K16 instead of K17", 'del lines[_row(lines, "K17")]', 'del lines[_row(lines, "K16")]'),
 ("M31", "operator", "m_edited_quote: edit char replaced by fixed x", 'cells[4] = q[:-2] + ("." if last != "." else ",") + "`"', 'cells[4] = q[:-2] + "x`"'),
 ("M32", "operator", "m_pin_byte: xor 0x01 -> 0x03", "nb = data[0] ^ 0x01", "nb = data[0] ^ 0x03"),
 ("M33", "dropped-leg", "m_new_row_missing deletes S391 instead of S390", 'REG_RE.match(l).group(1) == "S390"]', 'REG_RE.match(l).group(1) == "S391"]'),
 ("M34", "constant", "m_anchor_past_eof anchor 1-9999 -> 1-100 (inside EOF)", 'cells[5] = " ConfigWatcher.cpp:1-9999 "', 'cells[5] = " ConfigWatcher.cpp:1-100 "'),
 ("M35", "constant", "m_anchor_past_eof anchor 1-9999 -> 1-9998 (still past EOF)", 'cells[5] = " ConfigWatcher.cpp:1-9999 "', 'cells[5] = " ConfigWatcher.cpp:1-9998 "'),
 ("M36", "vacuous", "m_entry_absent: unlink removed (no mutation)", '    _reg(d, ctx["entry"]).unlink()', '    _reg(d, ctx["entry"])'),
 ("M37", "inverted", "_need_echo: presence test disabled", 'if not any(l.startswith("echo:") for l in rec["legs"]):', "if False:"),
 ("M38", "off-by-one", "_need_junk: content shortfall bound >=33 -> >=34", 'if rec["content"] >= 33:', 'if rec["content"] >= 34:'),
 ("M39", "dropped-leg", "_need_junk: tok: presence test disabled", 'if not any(l.startswith("tok:") for l in rec["legs"]):', "if False:"),
 ("M40", "inverted", "judge_control: rev identity check disabled", '    if rec["rev"] != sha:\n        return "rev=%s, passed %s" % (rec["rev"], sha)\n    if rec["verdict"] == "TARGET_MET":', '    if False:\n        return "rev=%s, passed %s" % (rec["rev"], sha)\n    if rec["verdict"] == "TARGET_MET":'),
 ("M41", "inverted", "judge_control: 'mutant admitted' check disabled", '    if rec["verdict"] == "TARGET_MET":\n        return "verdict=TARGET_MET (mutant admitted)"', "    if False:\n        return \"verdict=TARGET_MET (mutant admitted)\""),
 ("M42", "off-by-one", "judge_control: exit status must be 1 -> 1 or 2", "    if rc != 1:", "    if rc not in (1, 2):"),
 ("M43", "inverted", "judge_good: counts comparison inverted", "if got != GOOD_COUNTS:", "if got == GOOD_COUNTS:"),
 ("M44", "inverted", "judge_good: exit status test inverted", "    if rc != 0:\n        return \"exit status %s, need 0\" % rc", "    if rc == 0:\n        return \"exit status %s, need 0\" % rc"),
 ("M45", "removed-guard", "judge_good: stderr guard removed", '    if err:\n        return err\n    if rec["rev"] != sha:\n        return "rev=%s, passed %s" % (rec["rev"], sha)\n    if rec["verdict"] != "TARGET_MET"', '    if False:\n        return err\n    if rec["rev"] != sha:\n        return "rev=%s, passed %s" % (rec["rev"], sha)\n    if rec["verdict"] != "TARGET_MET"'),
 ("M46", "operator", "judge_good: or -> and in verdict/missed test", 'if rec["verdict"] != "TARGET_MET" or rec["missed"] != "none":', 'if rec["verdict"] != "TARGET_MET" and rec["missed"] != "none":'),
 ("M47", "operator", "denominator: and -> or in OK verdict", 'verdict = "OK" if good_ok and passed == N_CONTROLS and len(CONTROLS) == N_CONTROLS else "FAIL"', 'verdict = "OK" if good_ok or passed == N_CONTROLS and len(CONTROLS) == N_CONTROLS else "FAIL"'),
 ("M48", "off-by-one", "run_counter: exactly-one stdout line -> at-least-one", "    if len(lines) != 1:", "    if len(lines) < 1:"),
 ("M49", "operator", "run_counter: legs split on ';' not ','", 'legs = [] if missed == "none" else missed.split(",")', 'legs = [] if missed == "none" else missed.split(";")'),
 ("M50", "removed-guard", "run_counter: registered leg grammar check disabled", 'if missed != "none" and not all(LEG_RE.match(x) for x in legs):', "if False:"),
 ("M51", "swapped", "_body: judge_control arguments rc/rec swapped", 'why = judge_control(sha, rc, rec, err, check)', 'why = judge_control(sha, rec, rc, err, check)'),
 ("M52", "swapped", "_body: mutation lambda argument order swapped", 'lambda dd, m=mut: m(dd, ctx)', 'lambda dd, m=mut: m(ctx, dd)'),
 ("M53", "dropped-leg", "_body: EXTRA_PATHS (README, SOURCES) not exported", '[ctx["entry"], TABLES_PATH, ctx["pin_dir"], *EXTRA_PATHS]', '[ctx["entry"], TABLES_PATH, ctx["pin_dir"]]'),
 ("M54", "order", "_body: control order shuffle removed", "random.SystemRandom().shuffle(order)", "pass"),
 ("M55", "removed-guard", "_expected_leg: collateral allowance removed (diagnostic only)", '    if leg == required or leg in collateral:', '    if leg == required:'),
 ("M56", "constant", "_clip: printed legs 8 -> 1 (diagnostic only)", "def _clip(legs: list, n: int = 8) -> str:", "def _clip(legs: list, n: int = 1) -> str:"),
 ("M57", "operator", "_body: k/h row-count guard and -> and (equal on frozen tables)", 'if len(ctx["k_ids"]) != 30 or len(ctx["h_ids"]) != 3:', 'if len(ctx["k_ids"]) != 30 and len(ctx["h_ids"]) != 3:'),
 ("M58", "off-by-one", "m_quote_echo: echo threshold >=30 -> >=31 (K07 quote is 30)", "len(q) - 2 >= 30:", "len(q) - 2 >= 31:"),
 ("M59", "constant", "m_quote_echo: echo suffix text changed (added full stop)", '" echoed on this line, no analysis added here"', '" echoed on this line, no analysis added here."'),
 ("M60", "dropped-leg", "m_junk: H placeholder text identical for all H rows", 'cells[1] = "placeholder host proposition %s, not a read" % rid', 'cells[1] = "placeholder host proposition, not a read"'),
 ("M61", "swapped", "CONTROLS: control 7 expects row:K16 (wrong expectation)", '_need("row:K17")', '_need("row:K16")'),
 ("M62", "swapped", "CONTROLS: control 2 expectation swapped to _need_echo", 'm_junk, "tok:<id> + content<33", _need_junk, ()', 'm_junk, "tok:<id> + content<33", _need_echo, ()'),
 ("M63", "constant", "m_prov_dangling: source-line window 15 -> 1 (line 1 is the source line)", "hits = [i for i, l in enumerate(lines[:15]) if l.startswith(\"source:\")]", "hits = [i for i, l in enumerate(lines[:1]) if l.startswith(\"source:\")]"),
 ("M64", "constant", "m_prov_dangling: appended id S999 -> S383 (a real row)", '    lines[hits[0]] = lines[hits[0]] + ", S999"', '    lines[hits[0]] = lines[hits[0]] + ", S383"'),
 ("M65", "operator", "m_pin_byte: pin file set to ConfigValues (still a pinned file)", 'rel = ctx["pin_dir"] + "/Hyprland-ConfigWatcher.cpp"', 'rel = ctx["pin_dir"] + "/Hyprland-ConfigValues.cpp"'),
 ("M66", "dropped-leg", "m_scope_swap: K10 row not re-pointed to S399", 'row[2] = "S399"', 'row[2] = "S383"'),
]
# MutationError tokens, mutants whose old text is not unique are rejected by the driver (asserted below).


def make_mutant_source(old: str, new: str) -> str:
    n = SRC.count(old)
    if n != 1:
        raise SystemExit("old text occurs %d times: %r" % (n, old[:80]))
    return SRC.replace(old, new, 1)


# --------------------------------------------------------------------------- wrappers (real counter, forged output)
WRAP_TEMPLATE = r'''#!/usr/bin/env python3
"""Wrapper oracle: runs the REAL counter, then forges one property of its output (mode=%(mode)s)."""
import re
import subprocess
import sys

REAL = %(real)r
MODE = %(mode)r


def main():
    p = subprocess.run([sys.executable, "-I", REAL] + sys.argv[1:], capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    rc = p.returncode
    lines = [l for l in out.split("\n") if l.strip()]
    line = lines[0] if lines else ""
    if MODE == "rev":
        line = re.sub(r"rev=\S+", "rev=" + "0" * 40, line)
    elif MODE == "rc0":
        rc = 0
    elif MODE == "rc2":
        rc = 2 if "verdict=TARGET_MISSED" in line else rc
    elif MODE == "dup":
        lines = [line, line]
    elif MODE == "stderr":
        err = err + "warning: forged diagnostic\n"
    elif MODE == "content":
        line = re.sub(r"content=\d+/33", "content=33/33", line)
    elif MODE == "verdictword":
        line = line.replace("verdict=TARGET_MISSED", "verdict=TARGET_MAYBE")
    elif MODE == "denom":
        line = re.sub(r"rows=(\d+)/30", r"rows=\1/31", line)
    elif MODE == "goodonly":
        if "verdict=TARGET_MET missed=none" in line:
            line = re.sub(r"content=\d+/33", "content=32/33", line)
    if MODE == "dup":
        sys.stdout.write("\n".join(lines) + "\n")
    else:
        sys.stdout.write(line + ("\n" if line else ""))
    sys.stderr.write(err)
    return rc


if __name__ == "__main__":
    sys.exit(main())
'''

WRAPPERS = ["rev", "rc0", "rc2", "dup", "stderr", "content", "verdictword", "denom", "goodonly"]


def gen_wrappers():
    WRAP.mkdir(parents=True, exist_ok=True)
    for m in WRAPPERS:
        p = WRAP / ("w_%s.py" % m)
        p.write_text(WRAP_TEMPLATE % {"mode": m, "real": str(REAL)})
        p.chmod(0o755)


# --------------------------------------------------------------------------- variant trees (entry edits)
def variant_entries():
    entry = (REPO / "corpus/knowledge/hyprland-config-autoreload-r56.md").read_text()
    lines = entry.split("\n")
    k05 = next(l for l in lines if l.startswith("| K05 "))
    k10 = next(l for l in lines if l.startswith("| K10 "))
    out = {}
    # fenced copy of K05 after the entry (a 0-3 indent fence hides it from the harness and the counter)
    out["var_fence3"] = entry + "\n```text\n" + k05 + "\n```\n"
    # indent-4 fence: the harness must NOT treat it as a fence (CommonMark: 4+ spaces is code, not a fence opener)
    out["var_fence4"] = entry + "\n    ```text\n" + k05 + "\n    ```\n"
    # ~~~ fence containing a ``` line: the closing test must be fence-kind exact
    out["var_tilde"] = entry + "\n~~~text\n```\n" + k05 + "\n~~~\n"
    # duplicated K05 row (outside any fence)
    out["var_dupK05"] = entry.replace(k05 + "\n", k05 + "\n" + k05 + "\n", 1)
    # K10 with a closed HTML comment on the same line
    out["var_comment"] = entry.replace(k05, k05[:-1] + " <!-- note --> |", 1)
    # K05 row with a sixth cell
    out["var_6cell"] = entry.replace(k05, k05[:-1] + "| extra |", 1)
    for k, v in out.items():
        assert v != entry, k
    return out


def build_variant_repo(name: str, entry_text: str) -> Path:
    base = SCR / "variants"
    base.mkdir(exist_ok=True)
    d = Path(tempfile.mkdtemp(prefix=name + "-", dir=str(base)))
    shutil.copytree(REPO, d, symlinks=True, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))
    (d / "corpus/knowledge/hyprland-config-autoreload-r56.md").write_text(entry_text)
    subprocess.run(["git", "-C", str(d), "init", "-q", "-b", "main"], check=True, env=ENV)
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         env=ENV).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(str(d)), (top, d)
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, env=ENV)
    subprocess.run(["git", "-C", str(d), "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", name],
                   check=True, env=ENV)
    sha = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], capture_output=True, text=True, env=ENV).stdout.strip()
    return d, sha


# --------------------------------------------------------------------------- battery
def battery():
    """(oracle name, harness repo, rev, counter argument list)"""
    tests = []
    tests.append(("real", REPO, "a96bd38b6cc042e87430ef7c65ecd7cf56b1140c", []))
    for stub in sorted(STUBS.glob("stub_*.py")):
        tests.append((stub.stem, REPO, "a96bd38b6cc042e87430ef7c65ecd7cf56b1140c", ["--counter", str(stub)]))
    for w in sorted(WRAP.glob("w_*.py")):
        tests.append((w.stem, REPO, "a96bd38b6cc042e87430ef7c65ecd7cf56b1140c", ["--counter", str(w)]))
    for name, (d, sha) in VARIANT_REPOS.items():
        tests.append((name, d, sha, []))
    return tests


VARIANT_REPOS = {}


def run_one(mdir: Path, label: str, oracle: str, repo, rev, extra):
    work = RUN / label / oracle
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    cmd = [sys.executable, "-I", str(mdir / "check-r56-controls.py"), "--claim", "c1", "--repo", str(repo),
           "--rev", rev, "--work", str(work)] + extra
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=900, env=ENV, cwd=str(work))
        res = {"rc": p.returncode, "out": p.stdout.decode("utf-8", "replace"), "err": p.stderr.decode("utf-8", "replace")}
    except subprocess.TimeoutExpired:
        res = {"rc": "TIMEOUT", "out": "", "err": ""}
    shutil.rmtree(work, ignore_errors=True)
    rd = RCPT / label
    rd.mkdir(parents=True, exist_ok=True)
    (rd / (oracle + ".out")).write_text(res["out"])
    (rd / (oracle + ".err")).write_text(res["err"])
    (rd / (oracle + ".rc")).write_text(str(res["rc"]) + "\n")
    return res


def prepare_mutant(mid, kind, desc, old, new):
    mdir = MUT / mid
    mdir.mkdir(parents=True, exist_ok=True)
    shutil.copy(CHECK, mdir / "check-r56-controls.py")
    if mid == "M26":
        src = SRC.replace('" The value is capped at 200 by this call."', '" The value is capped at 2 by this call."', 1)
        assert src != SRC
    elif mid == "PRISTINE":
        src = SRC
    else:
        src = make_mutant_source(old, new)
        if src == SRC:
            raise SystemExit("mutant %s is a no-op" % mid)
    (mdir / "r56_ctl_c1.py").write_text(src)
    import py_compile
    try:
        py_compile.compile(str(mdir / "r56_ctl_c1.py"), doraise=True)
        syntax = "ok"
    except py_compile.PyCompileError as e:
        syntax = "SYNTAX:" + str(e)[:200]
    return syntax


def classify(pres, muts):
    """pres/muts: dict oracle -> res. Returns (category, first oracle killing it, detail)."""
    for o in pres:
        p, m = pres[o], muts[o]
        if (p["out"], p["rc"]) != (m["out"], m["rc"]):
            return "KILLED", o, "stdout/rc differs: %r rc=%s -> %r rc=%s" % (
                p["out"].strip()[-120:], p["rc"], m["out"].strip()[-120:], m["rc"])
    for o in pres:
        if pres[o]["err"] != muts[o]["err"]:
            return "DIAG", o, "stderr differs only"
    return "SURVIVED", None, "no oracle differs"


def main(argv):
    gen_wrappers()
    global VARIANT_REPOS
    for name, text in variant_entries().items():
        d, sha = build_variant_repo(name, text)
        VARIANT_REPOS[name] = (d, sha)
    # pristine
    pdir = MUT / "PRISTINE"
    pdir.mkdir(parents=True, exist_ok=True)
    shutil.copy(CHECK, pdir / "check-r56-controls.py")
    shutil.copy(PRISTINE, pdir / "r56_ctl_c1.py")
    tests = battery()
    with ThreadPoolExecutor(max_workers=int(os.environ.get("JOBS", "8"))) as ex:
        futs = {o: ex.submit(run_one, pdir, "PRISTINE", o, r, s, e) for (o, r, s, e) in tests}
        pres = {o: f.result() for o, f in futs.items()}
    print("pristine battery done: %d oracles" % len(pres))
    rows = []
    selected = [m for m in M if not argv or m[0] in argv]
    preps = {}
    for mid, kind, desc, old, new in selected:
        preps[mid] = prepare_mutant(mid, kind, desc, old, new)
    for mid, kind, desc, old, new in selected:
        if preps[mid] != "ok":
            rows.append({"id": mid, "kind": kind, "desc": desc, "category": "INVALID", "oracle": None, "detail": preps[mid]})
            continue
        mdir = MUT / mid
        with ThreadPoolExecutor(max_workers=int(os.environ.get("JOBS", "8"))) as ex:
            futs = {o: ex.submit(run_one, mdir, mid, o, r, s, e) for (o, r, s, e) in tests}
            muts = {o: f.result() for o, f in futs.items()}
        cat, oracle, detail = classify(pres, muts)
        rows.append({"id": mid, "kind": kind, "desc": desc, "category": cat, "oracle": oracle, "detail": detail})
        print("%s %-9s %-40s %s" % (mid, cat, desc[:40], oracle or ""), flush=True)
    (RCPT / "summary.json").write_text(json.dumps({"rev": REV, "rows": rows, "oracles": [t[0] for t in tests],
                                                    "variants": {k: v[0].name for k, v in VARIANT_REPOS.items()}},
                                                   indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
