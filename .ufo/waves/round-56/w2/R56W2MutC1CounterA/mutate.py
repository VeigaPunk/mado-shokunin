#!/usr/bin/env python3
"""R56W2MutC1CounterA -- mutation driver for quality/counters/c1-r56-autoreload-entry.py.

Mutates COPIES of the counter (never the lane file), runs two unchanged oracles per mutant:

  ORACLE A  the counter's own selftest:
                 python3 -I <mutant> --selftest --repo LANE --rev REV --work W
             rc 0 == mutant survived the selftest, rc 1 == killed, rc 2 == inconclusive.

  ORACLE B  the lane harness:
                 python3 -I quality/check-r56-controls.py --claim c1 --repo LANE --rev REV \
                     --work W --counter <mutant>
             stdout `... verdict=OK` and rc 0 == mutant survived, rc 1 == killed, rc 2 == inconclusive.

VERDICT: KILLED  (at least one oracle killed it)
         SURVIVED (both oracles let it pass)
         EQUIVALENT (mutant is semantically identical to the pristine counter -- argued in the report)

Only lines of the PRODUCTION region of the counter (line numbers <= 636, i.e. before the
`# ---- selftest` banner) are mutated: mutating the oracle itself is not a mutation test.

Usage: python3 -I mutate.py [--lane DIR] [--rev SHA] [--out DIR] [--only ID,ID]
"""
import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

# (id, short label, line number, old substring, new substring)
# The old substring must occur EXACTLY on that line of the pristine source.
MUTANTS = [
    # ---- row grammar -------------------------------------------------------
    ("M01", "row: cell separator widened to '|'", 223, 'split(" | ")', 'split("|")'),
    ("M02", "row: strict_row min length 4 -> 3", 221, "or len(line) < 4:", "or len(line) < 3:"),
    ("M03", "registry_id: min 3 digits -> 2", 255, "if k - j - 1 < 3:", "if k - j - 1 < 2:"),
    ("M04", "registry_id: leading-space tolerance 3 -> 4", 245,
     'if n > 3 or n >= len(line) or line[n] != "|":', 'if n > 4 or n >= len(line) or line[n] != "|":'),
    ("M05", "row: '|' inside a cell check dropped", 513, 'if any("|" in c for c in strict):', "if False:"),
    ("M06", "row: quote-cell backtick requirement dropped", 524,
     'if strict[4] != "`" + quote + "`":', "if strict[4] != quote:"),
    ("M07", "row: proposition leading/trailing-space check dropped", 527,
     "if prop != prop.strip() or len(prop) < (K_MIN if kind == \"K\" else H_MIN):",
     "if len(prop) < (K_MIN if kind == \"K\" else H_MIN):"),
    ("M08", "row: proposition uniqueness count != 1 -> != 2", 529,
     "if prop_count.get(prop, 0) != 1:", "if prop_count.get(prop, 0) != 2:"),
    ("M09", "row: src-cell ASCII check dropped", 518, "and strict[2][1:].isascii()):", "and True):"),
    ("M10", "row: pin:line cell arguments swapped", 522,
     'if strict[3] != "%s:%s" % (pin, line):', 'if strict[3] != "%s:%s" % (line, pin):'),
    ("M11", "row: candidate multiplicity == 1 -> >= 1 (redundant check)", 511,
     "len(cand[rid]) == 1", "len(cand[rid]) >= 1"),
    ("M12", "row: duplicated row tolerated by row_data", 381,
     "if len(lines) != 1:", "if len(lines) < 1:"),
    # ---- quote leg ---------------------------------------------------------
    ("M13", "quote: empty-carried-quote check dropped", 539, 'or carried == ""', ""),
    ("M14", "quote: backtick delimiters not required in the quote cell", 538,
     'if len(q) >= 2 and q[0] == "`" and q[-1] == "`" else ""', "if len(q) >= 2 else \"\""),
    ("M15", "quote: pin line off by one (line -> line+1)", 533,
     "pl = pin_line(pin, line)", "pl = pin_line(pin, line + 1)"),
    ("M16", "quote: pin line bound widened (n > len(pl) -> n > len(pl)+1)", 440,
     "or n > len(pl):", "or n > len(pl) + 1:"),
    ("M17", "quote: pin line index off by one (pl[n-1] -> pl[n])", 442,
     "return pl[n - 1]", "return pl[n]"),
    # ---- host leg ----------------------------------------------------------
    ("M18", "host: empty-carried-quote check dropped", 543, 'carried != ""', "True"),
    ("M19", "host: host leg always true", 545, "host_ok[rid] = hok", "host_ok[rid] = True"),
    # ---- source_cell leg ---------------------------------------------------
    ("M20", "source_cell: tier check dropped", 464, 'or cells[3] not in ("A", "B")', ""),
    ("M21", "source_cell: rev_rule token in URL dropped", 471, "or tok not in urls[-1]", ""),
    ("M22", "source_cell: used-by cell check dropped", 473,
     "return ENTRY in cells[10]", "return True"),
    ("M23", "source_cell: duplicated registry row tolerated", 455,
     "if len(rows) != 1:", "if len(rows) < 1:"),
    ("M24", "source_cell: registry cell count 11 -> >= 11", 458,
     "len(cells) == 11", "len(cells) >= 11"),
    ("M25", "source_cell: URL read from the id cell instead of the source cell", 466,
     "urls = URL_RE.findall(cells[1])", "urls = URL_RE.findall(cells[0])"),
    # ---- scope leg ---------------------------------------------------------
    ("M26", "scope: locator lower-bound check dropped", 290, "or lo > nlines", ""),
    ("M27", "scope: range upper bound exclusive (line <= hi -> line < hi)", 292,
     "elif lo <= line <= hi:", "elif lo <= line < hi:"),
    ("M28", "scope: 'over' veto dropped (anchor-past-EOF not fatal)", 302,
     "return covered and not over", "return covered"),
    ("M29", "scope: locator key widened (basename -> basename, no colon)", 268,
     'key = basename + ":"', 'key = basename'),
    ("M30", "scope: pin line-count bound not passed to the scanner", 483,
     "len(pl) if pl is not None else None", "None"),
    ("M31", "scope: locator list separator ',' -> ';'", 294,
     'if k < len(anchor) and anchor[k] == ",":', 'if k < len(anchor) and anchor[k] == ";":'),
    # ---- tok leg -----------------------------------------------------------
    ("M32", "tok: shared-quote side of the intersection dropped", 486,
     "tok = bool(set(TOKEN_RE.findall(prop)) & set(TOKEN_RE.findall(quote)))",
     "tok = bool(set(TOKEN_RE.findall(prop)))"),
    ("M33", "tok: identifier length bound widened (3 -> 2)", 305, "{3,}", "{2,}"),
    ("M34", "tok: identifier length bound narrowed (3 -> 4)", 305, "{3,}", "{4,}"),
    ("M35", "tok/num/echo: echo result forced true", 556,
     "tok_ok[rid], num_ok[rid], echo_ok[rid] = t, n, ec",
     "tok_ok[rid], num_ok[rid], echo_ok[rid] = t, n, True"),
    # ---- num leg -----------------------------------------------------------
    ("M36", "num: digit runs taken from the proposition instead of the quote", 487,
     'runs = set(re.findall(r"[0-9]+", quote))', 'runs = set(re.findall(r"[0-9]+", prop))'),
    ("M37", "num: the row's own line dropped from the allowed integers", 488,
     "ints = {0, 1, 2, 3, line}", "ints = {0, 1, 2, 3}"),
    ("M38", "num: allowed integers taken from every pin (same-pin filter dropped)", 490,
     'if r["pin"] == pin:', "if r[\"pin\"] == pin or True:"),
    ("M39", "num: digit-run regex trailing boundary dropped", 306,
     'RUN_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")',
     'RUN_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+")'),
    ("M40", "num: allowed-integer comparison inverted", 495,
     "if run in runs or (v is not None and v in ints):",
     "if run in runs or (v is not None and v not in ints):"),
    # ---- echo leg ----------------------------------------------------------
    ("M41", "echo: 'quote in proposition' test dropped", 498,
     "echo = not (len(quote) >= ECHO_MIN and quote in prop)",
     "echo = not (len(quote) >= ECHO_MIN)"),
    ("M42", "echo: ECHO_MIN constant 30 -> 20", 25, "ECHO_MIN = 30", "ECHO_MIN = 20"),
    ("M43", "echo: ECHO_MIN constant 30 -> 31", 25, "ECHO_MIN = 30", "ECHO_MIN = 31"),
    # ---- prov leg ----------------------------------------------------------
    ("M44", "prov: window widened (first 15 lines -> first 30)", 402,
     "head = entry_lines[:15]", "head = entry_lines[:30]"),
    ("M45", "prov: exactly one verified-at line -> at least one", 406,
     "len(ver_idx) == 1", "len(ver_idx) >= 1"),
    ("M46", "prov: order comparison off by one (source < verified -> source <= verified)", 408,
     "prov_ok = min(src_idx) < ver_idx[0] < max(rec_idx)",
     "prov_ok = min(src_idx) <= ver_idx[0] < max(rec_idx)"),
    ("M47", "prov: cited-sid subset test inverted", 414,
     "if not sids_cited <= src_set:", "if not sids_cited >= src_set:"),
    ("M48", "prov: registry-membership test inverted", 412,
     "if any(s not in registry for s in src_set):", "if all(s not in registry for s in src_set):"),
    ("M49", "prov: source-line sid regex widened", 411,
     "src_set.update(SID_RE.findall(head[i]))", 'src_set.update(re.findall(r"S[0-9]+", head[i]))'),
    # ---- index leg ---------------------------------------------------------
    ("M50", "index: README match widened (startswith -> contains)", 423,
     "if l.startswith(INDEX_PREFIX))", "if INDEX_PREFIX in l)"),
    ("M51", "index: index count check inverted (!= 1 -> < 1)", 424,
     "if idx_hits != 1:", "if idx_hits < 1:"),
    # ---- new_rows leg ------------------------------------------------------
    ("M52", "new_rows: required denominator 8 -> 7", 36, "NEW_ROWS_DENOM = 8", "NEW_ROWS_DENOM = 7"),
    ("M53", "new_rows: frozen id-count check dropped", 604,
     "or len(c1[\"new_row_ids\"]) != NEW_ROWS_DENOM", ""),
    ("M54", "new_rows: source_cell requirement dropped from the count", 601,
     "if pin is not None and source_cell_ok(sid, pin):", "if pin is not None:"),
    # ---- pin_hash leg ------------------------------------------------------
    ("M55", "pin_hash: only the first pin blob is checked", 570,
     "for pin, want in pins_all.items():", "for pin, want in list(pins_all.items())[:1]:"),
    ("M56", "pin_hash: comparison inverted (!= want -> == want)", 572,
     "hashlib.sha256(d).hexdigest() != want", "hashlib.sha256(d).hexdigest() == want"),
    ("M57", "pin_hash: host pin blobs not checked", 432,
     'pins_all.update(c1["host_pin_sha256"])', ""),
    # ---- tables_sha leg ----------------------------------------------------
    ("M58", "tables_sha: comparison inverted", 321,
     "ok = hashlib.sha256(data).hexdigest() == TABLES_SHA256",
     "ok = hashlib.sha256(data).hexdigest() != TABLES_SHA256"),
    ("M59", "tables_sha: frozen constant altered", 23,
     "9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2",
     "9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e3"),
    # ---- render / verdict --------------------------------------------------
    ("M60", "render: content threshold 33 -> >= 33", 622, 'counts["e"] == 33', 'counts["e"] >= 33'),
    ("M61", "render: rows threshold 30 -> >= 30", 621, 'counts["a"] == 30', 'counts["a"] >= 30'),
    ("M62", "render: 'none' for an empty missed list dropped", 627,
     '",".join(missed) if missed else "none"', '",".join(missed)'),
    # ---- scanners / repository access -------------------------------------
    ("M63", "repo: symlink blob mode accepted as a regular file", 117,
     'if typ != "blob" or mode not in REGULAR_MODES:', 'if typ != "blob":'),
    ("M64", "scanner: a row inside an HTML comment counts as live", 201,
     "if first_pipe_live:", "if first_pipe_live is not None:"),
    ("M65", "scanner: fence minimum length 3 -> 2", 148, "if m - n < 3:", "if m - n < 2:"),
    ("M66", "scope: 'continue' after a comma locator dropped (first locator only)", 299,
     "continue", "# continue dropped"),
    ("M67", "num: digits in identifiers counted (RUN_RE boundaries dropped)", 306,
     'RUN_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")',
     'RUN_RE = re.compile(r"[0-9]+")'),
]


def read_pristine(lane, rev):
    p = subprocess.run(["git", "-C", lane, "show", "%s:quality/counters/c1-r56-autoreload-entry.py" % rev],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise SystemExit("cannot read pristine counter: %s" % p.stderr.decode())
    return p.stdout.decode("utf-8")


def apply_mutant(src_lines, lineno, old, new):
    lines = list(src_lines)
    i = lineno - 1
    if i < 0 or i >= len(lines):
        return None, "line %d out of range" % lineno
    if old not in lines[i]:
        return None, "old text %r not on line %d (%r)" % (old, lineno, lines[i])
    lines[i] = lines[i].replace(old, new, 1)
    return lines, None


def child_env(work):
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": work, "TMPDIR": work,
            "LC_ALL": "C.UTF-8", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0"}


def run_selftest(counter_path, lane, rev, work):
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, "-I", counter_path, "--selftest", "--repo", lane,
                            "--rev", rev, "--work", work],
                           env=child_env(work), cwd=work, capture_output=True, timeout=900)
    except subprocess.TimeoutExpired:
        return {"rc": None, "out": "", "err": "timeout", "verdict": "inconclusive", "sec": time.time() - t0}
    out = p.stdout.decode("utf-8", "replace").strip()
    err = p.stderr.decode("utf-8", "replace").strip()
    if p.returncode == 0:
        v = "survived"
    elif p.returncode == 1:
        v = "killed"
    else:
        v = "inconclusive"
    return {"rc": p.returncode, "out": out[-400:], "err": err[-400:], "verdict": v, "sec": time.time() - t0}


def run_harness(lane, rev, work, counter_path):
    t0 = time.time()
    harness = os.path.join(lane, "quality", "check-r56-controls.py")
    try:
        p = subprocess.run([sys.executable, "-I", harness, "--claim", "c1", "--repo", lane,
                            "--rev", rev, "--work", work, "--counter", counter_path],
                           env=child_env(work), cwd=work, capture_output=True, timeout=900)
    except subprocess.TimeoutExpired:
        return {"rc": None, "out": "", "err": "timeout", "verdict": "inconclusive", "sec": time.time() - t0}
    out = p.stdout.decode("utf-8", "replace").strip()
    err = p.stderr.decode("utf-8", "replace").strip()
    if p.returncode == 0 and "verdict=OK" in out:
        v = "survived"
    elif p.returncode == 1:
        v = "killed"
    else:
        v = "inconclusive"
    return {"rc": p.returncode, "out": out[-400:], "err": err[-600:], "verdict": v, "sec": time.time() - t0}


def one_mutant(job):
    mid, label, lineno, old, new, lane, rev, outdir, pristine_lines = job
    work = tempfile.mkdtemp(prefix="m%02d-" % int(mid[1:]), dir=outdir)
    counter_path = os.path.join(work, "mutant-%s.py" % mid)
    try:
        lines, err = apply_mutant(pristine_lines, lineno, old, new)
        if err:
            return {"id": mid, "label": label, "line": lineno, "old": old, "new": new,
                    "verdict": "INCONCLUSIVE", "detail": err}
        with open(counter_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        cp = subprocess.run([sys.executable, "-I", "-c",
                             "import py_compile,sys; py_compile.compile(sys.argv[1], doraise=True)",
                             counter_path], capture_output=True)
        if cp.returncode != 0:
            return {"id": mid, "label": label, "line": lineno, "old": old, "new": new,
                    "verdict": "INCONCLUSIVE", "detail": "syntax error: %s" % cp.stderr.decode()[-200:]}
        st = os.path.join(work, "st")
        hw = os.path.join(work, "hw")
        os.makedirs(st, exist_ok=True)
        os.makedirs(hw, exist_ok=True)
        a = run_selftest(counter_path, lane, rev, st)
        b = run_harness(lane, rev, hw, counter_path)
        killed_by = []
        if a["verdict"] == "killed":
            killed_by.append("selftest")
        if b["verdict"] == "killed":
            killed_by.append("harness")
        if a["verdict"] == "inconclusive" and b["verdict"] == "inconclusive":
            verdict = "INCONCLUSIVE"
        elif killed_by:
            verdict = "KILLED"
        else:
            verdict = "SURVIVED"
        return {"id": mid, "label": label, "line": lineno, "old": old, "new": new,
                "verdict": verdict, "killed_by": killed_by,
                "selftest": a, "harness": b}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/mado-shokunin")
    ap.add_argument("--rev", default="28fc86ac2359ec27406d8a2c63bef82ea6e947ed")
    ap.add_argument("--out", default="/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterA/mut")
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--results", default="")
    args = ap.parse_args()

    lane = os.path.abspath(args.lane)
    rev = args.rev
    outdir = os.path.abspath(args.out)
    os.makedirs(outdir, exist_ok=True)
    pristine = read_pristine(lane, rev)
    pristine_lines = pristine.split("\n")

    only = set(x for x in args.only.split(",") if x)
    jobs = [(mid, label, ln, old, new, lane, rev, outdir, pristine_lines)
            for (mid, label, ln, old, new) in MUTANTS if not only or mid in only]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for res in ex.map(one_mutant, jobs):
            results.append(res)
            print("%-4s %-11s %s" % (res["id"], res["verdict"], res["label"]), flush=True)
    results.sort(key=lambda r: r["id"])
    path = args.results or os.path.join(outdir, "results.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    n_k = sum(1 for r in results if r["verdict"] == "KILLED")
    n_s = sum(1 for r in results if r["verdict"] == "SURVIVED")
    n_i = sum(1 for r in results if r["verdict"] == "INCONCLUSIVE")
    print("TOTAL %d  KILLED %d  SURVIVED %d  INCONCLUSIVE %d" % (len(results), n_k, n_s, n_i))
    print("results: %s" % path)


if __name__ == "__main__":
    main()
