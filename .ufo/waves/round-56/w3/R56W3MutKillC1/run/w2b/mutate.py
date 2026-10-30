#!/usr/bin/env python3
"""R56W2MutC1CounterB — mutation driver for quality/counters/c1-r56-autoreload-entry.py.

Baseline bytes: the counter as committed at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed
(lane read-only git; the file is copied into scratch, never mutated in the lane).

Oracle (unchanged, from the frozen contract):
  A) python3 -I <mutant> --selftest --repo LANE --rev REV --work W
     -> the counter's own selftest must FAIL to kill the mutant.
  B) python3 -I quality/check-r56-controls.py --claim c1 --repo LANE --rev REV --work W
     --counter <mutant>
     -> the independent control harness must FAIL (good=bad or controls<12/12) to kill.

KILLED  = at least one oracle fails on the mutant.
SURVIVED = both oracles pass on the mutant (candidate coverage hole).
EQUIVALENT = a survivor whose mutation is provably behaviour-preserving (argument given
             in mutants.md; the driver only flags it as SURVIVED).

Usage: python3 -I mutate.py <scratch-root> [--only ID[,ID...]]
"""
import concurrent.futures as cf
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
COUNTER_REL = "quality/counters/c1-r56-autoreload-entry.py"
HARNESS_REL = "quality/check-r56-controls.py"
PY = "python3"

# (id, area, old, new, note)
MUTANTS = [
    # --- split_lines
    ("M01", "split_lines", 'return data.decode("utf-8", "replace").split("\\n")',
     'return data.decode("utf-8", "replace").split("\\r\\n")', "line-separator swap"),
    ("M02", "split_lines", 'return data.decode("utf-8", "replace").split("\\n")',
     'return data.decode("utf-8", "ignore").split("\\n")', "decode error policy"),
    ("M03", "split_lines", 'return data.decode("utf-8", "replace").split("\\n")',
     'return data.decode("utf-8", "replace").splitlines()', "splitlines() instead of split"),
    # --- fence_open
    ("M04", "fence_open", '    if n > 3 or n >= len(line) or line[n] not in "`~":',
     '    if n > 4 or n >= len(line) or line[n] not in "`~":', "indent bound widened 3->4"),
    ("M05", "fence_open", '    if m - n < 3:',
     '    if m - n < 4:', "fence minimum length 3->4"),
    ("M06", "fence_open", '    if ch == "`" and "`" in line[m:]:',
     '    if ch == "~" and "`" in line[m:]:', "backtick/tilde operator swap"),
    ("M07", "fence_open", '    if ch == "`" and "`" in line[m:]:',
     '    if ch == "`" and "`" in line[m - 1:]:', "info-string bound off-by-one"),
    # --- fence_close
    ("M08", "fence_close", '    if n > 3:',
     '    if n > 4:', "closer indent bound widened"),
    ("M09", "fence_close", '    return m - n >= length and line[m:].strip(" \\t") == ""',
     '    return m - n >= length - 1 and line[m:].strip(" \\t") == ""', "closer length off-by-one"),
    ("M10", "fence_close", '    return m - n >= length and line[m:].strip(" \\t") == ""',
     '    return m - n >= length and line[m:].strip() == ""', "closer tail whitespace widened"),
    # --- live_lines
    ("M11", "live_lines", '            if line.startswith("<!--", i):',
     '            if line.startswith("<!", i):', "comment opener changed"),
    ("M12", "live_lines", '                if line.startswith("-->", i):',
     '                if line.startswith("--> ", i):', "comment closer changed"),
    ("M13", "live_lines", '                    i += 4',
     '                    i += 1', "comment open skip off-by-one"),
    ("M14", "live_lines", '                i += 3',
     '                i += 2', "comment close skip off-by-one"),
    ("M15", "live_lines", '        if first_pipe_live:',
     '        if first_pipe_live is not None:', "inverted liveness test"),
    ("M16", "live_lines", '            if in_fence is not None:',
     '            if False:', "fence state dropped"),
    ("M17", "live_lines", '                if fence_close(line, *in_fence):',
     '                if fence_close(line, in_fence[0], 1):', "closer length argument swapped"),
    ("M18", "live_lines", '        if not in_comment:',
     '        if True:', "comment state ignored"),
    # --- first_cell
    ("M19", "first_cell", '    while i < len(line) and line[i] in " \\t":',
     '    while i < len(line) and line[i] == " ":', "leading tab no longer skipped"),
    ("M20", "first_cell", '    j = line.find("|", i + 1)',
     '    j = line.find("|", i)', "cell separator search start off-by-one"),
    ("M21", "first_cell", '    return line[i + 1:j].strip()',
     '    return line[i + 1:j]', "cell text not stripped"),
    ("M22", "first_cell", '    return line[i + 1:j].strip()',
     '    return line[i + 1:j].strip().lower()', "cell text case-folded"),
    ("M23", "first_cell", '    if i >= len(line) or line[i] != "|":',
     '    if i >= len(line):', "pipe test dropped"),
    # --- strict_row
    ("M24", "strict_row", '    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 4:',
     '    if not (line.startswith("|") and line.endswith(" |")) or len(line) < 4:', "left pad relaxed"),
    ("M25", "strict_row", '    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 4:',
     '    if not (line.startswith("| ") and line.endswith("|")) or len(line) < 4:', "right pad relaxed"),
    ("M26", "strict_row", '    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 4:',
     '    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 2:', "minimum length off-by-one"),
    ("M27", "strict_row", '    return line[2:-2].split(" | ")',
     '    return line[2:-2].split("|")', "cell separator widened"),
    ("M28", "strict_row", '    return line[2:-2].split(" | ")',
     '    return line[2:-2].split(" |")', "cell separator trailing space dropped"),
    # --- lenient_row
    ("M29", "lenient_row", '    s = line.strip()',
     '    s = line', "line not stripped"),
    ("M30", "lenient_row", '    if s.startswith("|"):',
     '    if s.startswith("||"):', "leading pipe test changed"),
    ("M31", "lenient_row", '    if s.endswith("|"):',
     '    if s.endswith("||"):', "trailing pipe test changed"),
    ("M32", "lenient_row", '    return [c.strip() for c in s.split("|")]',
     '    return s.split("|")', "cell text not stripped"),
    # --- registry_cells
    ("M33", "registry_cells", '    return lenient_row(line)',
     '    return strict_row(line) or lenient_row(line)', "strict cells preferred"),
    # --- registry_id
    ("M34", "registry_id", '    if n > 3 or n >= len(line) or line[n] != "|":',
     '    if n > 4 or n >= len(line) or line[n] != "|":', "indent bound widened"),
    ("M35", "registry_id", '    if k - j - 1 < 3:',
     '    if k - j - 1 < 4:', "S-id digit count 3->4"),
    ("M36", "registry_id", '    return line[j:k]',
     '    return line[j + 1:k]', "id token off-by-one"),
    ("M37", "registry_id", '    while j < len(line) and line[j].isspace():',
     '    while j < len(line) and line[j] == " ":', "leading whitespace rule narrowed"),
    ("M38", "registry_id", '    if j >= len(line) or line[j] != "S":',
     '    if j >= len(line) or line[j] != "s":', "S prefix case folded"),
    # --- scope_covers
    ("M39", "scope_covers", '    key = basename + ":"',
     '    key = basename', "basename key loses colon"),
    ("M40", "scope_covers", '            if lo is None or hi is None or (nlines is not None and (hi > nlines or lo > nlines)):',
     '            if lo is None or hi is None:', "E3 past-EOF bound dropped"),
    ("M41", "scope_covers", '            elif lo <= line <= hi:',
     '            elif lo <= line < hi:', "range end exclusive"),
    ("M42", "scope_covers", '                if m > k + 1:',
     '                if m > k:', "hi parse guard off-by-one"),
    ("M43", "scope_covers", '            if k < len(anchor) and anchor[k] == ",":',
     '            if False:', "comma-separated locator list dropped"),
    ("M44", "scope_covers", '        pos = anchor.find(key, pos + 1)',
     '        pos = anchor.find(key, pos + len(key))', "occurrence scan step widened"),
    ("M45", "scope_covers", '    return covered and not over',
     '    return covered', "past-EOF verdict dropped"),
    ("M46", "scope_covers", '            if lo is None or hi is None or (nlines is not None and (hi > nlines or lo > nlines)):',
     '            if lo is None or hi is None or (nlines is not None and hi > nlines):', "E3 lo clause dropped"),
    ("M47", "scope_covers", '        i = pos + len(key)',
     '        i = pos', "locator start off-by-one"),
    ("M48", "scope_covers", '            while j < len(anchor) and anchor[j] in "0123456789":',
     '            while j < len(anchor) and anchor[j].isdigit():', "digit class widened"),
    ("M49", "scope_covers", '                while m < len(anchor) and anchor[m] in "0123456789":',
     '                while m < len(anchor) and anchor[m].isdigit():', "digit class widened (hi)"),
    ("M50", "scope_covers", '            lo = int(anchor[i:j]) if j - i < 19 else None',
     '            lo = int(anchor[i:j]) if j - i < 18 else None', "locator digit bound off-by-one"),
    # --- to_int
    ("M51", "to_int", '    return int(run) if len(run) < 19 else None',
     '    return int(run) if len(run) < 18 else None', "digit-run bound off-by-one"),
    # --- shared regexes
    ("M52", "TOKEN_RE", 'TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")',
     'TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")', "token min length widened"),
    ("M53", "TOKEN_RE", 'TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")',
     'TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")', "token min length dropped"),
    ("M54", "RUN_RE", 'RUN_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")',
     'RUN_RE = re.compile(r"(?<![A-Za-z0-9])[0-9]+(?![0-9])")', "digit-run boundary widened"),
    ("M55", "SID_RE", 'SID_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")',
     'SID_RE = re.compile(r"S[0-9]{3}")', "S-id boundary dropped"),
    ("M56", "URL_RE", 'URL_RE = re.compile(r"https?://\\S+")',
     'URL_RE = re.compile(r"https?://.*")', "URL token widened"),
    # --- constants
    ("M57", "constants", 'ECHO_MIN = 30',
     'ECHO_MIN = 29', "echo threshold lowered"),
    ("M58", "constants", 'ECHO_MIN = 30',
     'ECHO_MIN = 31', "echo threshold raised"),
    ("M59", "constants", 'K_MIN, H_MIN = 40, 20',
     'K_MIN, H_MIN = 39, 19', "proposition length bound lowered"),
    ("M60", "constants", 'K_MIN, H_MIN = 40, 20',
     'K_MIN, H_MIN = 41, 21', "proposition length bound raised"),
    ("M61", "constants", 'NEW_ROWS_DENOM = 8',
     'NEW_ROWS_DENOM = 7', "new_rows denominator changed"),
    ("M62", "constants", 'REGULAR_MODES = ("100644", "100755")',
     'REGULAR_MODES = ("100644",)', "executable blob mode dropped"),
    # --- git object access
    ("M63", "Repo.regular_oid", '        if any(c in ("", ".", "..") for c in comps):',
     '        if any(c in ("", ".") for c in comps):', "path dot-dot guard dropped"),
    ("M64", "Repo.regular_oid", '                if mode != "040000" or typ != "tree":',
     '                if typ != "tree":', "tree mode test dropped"),
    ("M65", "Repo.regular_oid", '                if typ != "blob" or mode not in REGULAR_MODES:',
     '                if typ != "blob":', "blob mode test dropped"),
    ("M66", "Repo.blob", '        if oid not in self.blobs:',
     '        if True:', "blob cache disabled"),
    ("M67", "Repo.listing", '                meta, _, name = rec.partition(b"\\t")',
     '                meta, _, name = rec.partition(b" ")', "ls-tree record split changed"),
    ("M68", "Repo.listing", '            out = self.git("ls-tree", "-z", tree_oid).stdout',
     '            out = self.git("ls-tree", tree_oid).stdout', "ls-tree NUL termination dropped"),
    ("M69", "Repo.resolve", '        p = self.git("rev-parse", "--verify", "-q", rev + "^{commit}", check=False)',
     '        p = self.git("rev-parse", "--verify", "-q", rev + "^{tree}", check=False)', "rev peel changed"),
    ("M70", "Repo.listing", '                mode, typ, oid = meta.decode().split(" ")',
     '                mode, typ, oid = meta.decode().split(" ", 2)', "meta split argument changed"),
    ("M71", "Repo.listing", '            if not rec:',
     '            if False:', "empty ls-tree record guard dropped"),
]


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=900)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def baseline_bytes():
    p = sh(["git", "-C", LANE, "show", REV + ":" + COUNTER_REL])
    if p.returncode != 0:
        raise SystemExit("cannot read baseline counter: " + p.stderr.decode())
    return p.stdout


def run_oracles(mut_path, work):
    """-> dict with selftest and harness results."""
    st = os.path.join(work, "st")
    ht = os.path.join(work, "ht")
    os.makedirs(st, exist_ok=True)
    os.makedirs(ht, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = work
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    a = sh([PY, "-I", mut_path, "--selftest", "--repo", LANE, "--rev", REV, "--work", st],
           cwd=work, env=env)
    b = sh([PY, "-I", os.path.join(LANE, HARNESS_REL), "--claim", "c1", "--repo", LANE,
            "--rev", REV, "--work", ht, "--counter", mut_path], cwd=work, env=env)
    bout = b.stdout.decode("utf-8", "replace").strip()
    harness_ok = ("good=ok" in bout and "controls=12/12" in bout and "verdict=OK" in bout
                  and b.returncode == 0)
    aout = a.stdout.decode("utf-8", "replace").strip()
    selftest_ok = (a.returncode == 0 and "/" in aout and aout.split()[0].split("/")[0] == aout.split()[0].split("/")[1])
    return {
        "selftest_rc": a.returncode,
        "selftest_out": aout[-300:],
        "selftest_err": a.stderr.decode("utf-8", "replace")[-600:],
        "selftest_ok": selftest_ok,
        "harness_rc": b.returncode,
        "harness_out": bout[-400:],
        "harness_err": b.stderr.decode("utf-8", "replace")[-400:],
        "harness_ok": harness_ok,
    }


def main(argv):
    root = argv[0] if argv else "/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterB"
    only = None
    for a in argv[1:]:
        if a.startswith("--only"):
            only = set(a.split("=", 1)[1].split(",")) if "=" in a else None
    mut_dir = os.path.join(root, "mutants")
    os.makedirs(mut_dir, exist_ok=True)
    base = baseline_bytes()
    base_sha = sha(base)
    base_path = os.path.join(root, "baseline.py")
    with open(base_path, "wb") as fh:
        fh.write(base)
    results = []
    sel = [m for m in MUTANTS if (only is None or m[0] in only)]

    def work_one(m):
        mid, area, old, new, note = m
        src = base.decode("utf-8")
        n = src.count(old)
        if n != 1:
            return {"id": mid, "area": area, "note": note, "error": "old text occurs %d times" % n}
        mut = src.replace(old, new)
        if mut.count("\n") != src.count("\n"):
            return {"id": mid, "area": area, "note": note, "error": "not a one-line change"}
        p = os.path.join(mut_dir, mid + ".py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(mut)
        c = sh([PY, "-I", "-m", "py_compile", p])
        if c.returncode != 0:
            return {"id": mid, "area": area, "note": note, "error": "mutant does not compile: " + c.stderr.decode()[-200:]}
        w = os.path.join(root, "work", mid)
        os.makedirs(w, exist_ok=True)
        t0 = time.time()
        r = run_oracles(p, w)
        r.update({"id": mid, "area": area, "note": note, "old": old, "new": new,
                  "mutant_sha256": sha(mut.encode("utf-8")), "base_sha256": base_sha,
                  "secs": round(time.time() - t0, 1)})
        if r["selftest_ok"] and r["harness_ok"]:
            r["verdict"] = "SURVIVED"
        else:
            r["verdict"] = "KILLED"
        return r

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(work_one, sel):
            results.append(r)
            sys.stderr.write("%-5s %-18s %s\n" % (r["id"], r.get("area", "?"), r.get("verdict", r.get("error", "?"))))

    out = {"rev": REV, "counter_rel": COUNTER_REL, "baseline_sha256": base_sha,
           "results": sorted(results, key=lambda r: r["id"])}
    with open(os.path.join(root, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    killed = [r for r in results if r.get("verdict") == "KILLED"]
    surv = [r for r in results if r.get("verdict") == "SURVIVED"]
    err = [r for r in results if "error" in r]
    sys.stderr.write("\nTOTAL=%d KILLED=%d SURVIVED=%d ERROR=%d\n"
                     % (len(results), len(killed), len(surv), len(err)))
    for r in err:
        sys.stderr.write("ERROR %s: %s\n" % (r["id"], r["error"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
