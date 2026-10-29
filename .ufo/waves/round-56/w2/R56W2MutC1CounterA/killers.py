#!/usr/bin/env python3
"""R56W2MutC1CounterA -- proposed killer fixtures for the C1 counter survivors.

For each proposed fixture: one single edit of a minimal scratch git repo (only the paths the counter
reads at --rev: entry, registry, README, frozen tables, pins), committed with the ctl identity.
The UNMUTATED counter (pristine) and the mutant counter (one MUTANTS entry from mutate.py) are run on
the same repo. The fixture kills the mutant when the mutant's stdout or exit status differs from the
pristine's. Pristine must also print the leg the fixture is designed to expose (sanity: the expectation
is the registered behaviour, not a copy of the mutant).

Scratch only: every fixture repo lives under --scratch (never the lane, never the fleet repo).
Usage: python3 -I killers.py --base SCRATCH_BASE_REPO --rev REV --scratch DIR [--out FILE]
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mutate", os.path.join(HERE, "mutate.py"))
mutate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutate)

ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
REG = "corpus/SOURCES.md"
README = "corpus/README.md"
TABLES = ".ufo/waves/round-56/frozen-tables-v2.json"
FETCH = ".ufo/waves/round-56/fetch/"
COUNTER_REL = "quality/counters/c1-r56-autoreload-entry.py"
TOKEN = __import__("re").compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")


def env(work):
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": work, "TMPDIR": work,
            "LC_ALL": "C.UTF-8", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}


# ------------------------------------------------------------------ edit helpers (operate on the fixture dir D)

def rd(D, rel):
    with open(os.path.join(D, rel), "rb") as fh:
        return fh.read()


def wr(D, rel, data):
    p = os.path.join(D, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def lines_of(D, rel):
    return rd(D, rel).decode("utf-8").split("\n")


def put_lines(D, rel, lines):
    wr(D, rel, "\n".join(lines))


def row_index(lines, rid):
    hits = [i for i, l in enumerate(lines) if l.startswith("| %s | " % rid)]
    assert len(hits) == 1, (rid, hits)
    return hits[0]


def row_cells(line):
    assert line.startswith("| ") and line.endswith(" |"), line[:60]
    return line[2:-2].split(" | ")


def join_cells(cells):
    return "| " + " | ".join(cells) + " |"


def quote_text(rid):
    t = json.loads(rd_tables_global[0])["c1"]
    for r in t["k"] + t["h"]:
        if r["id"] == rid:
            return r["quote"]
    raise KeyError(rid)


rd_tables_global = [None]  # set per fixture-run from the good tree


# ------------------------------------------------------------------ fixtures

def f_pipe_in_cell(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "K01")
    c = row_cells(L[i])
    c[1] = c[1] + " Pipe a|b here."
    L[i] = join_cells(c)
    put_lines(D, ENTRY, L)


def f_prop_leading_space(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "K01")
    c = row_cells(L[i])
    c[1] = " " + c[1]
    L[i] = join_cells(c)
    put_lines(D, ENTRY, L)


def f_src_nonascii_digit(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "K01")
    c = row_cells(L[i])
    assert c[2] == "S384", c[2]
    c[2] = "S38\u0664"  # ARABIC-INDIC DIGIT FOUR: str.isdigit() true, isascii() false
    L[i] = join_cells(c)
    put_lines(D, ENTRY, L)


def f_duplicate_row_k08(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "K08")
    c = row_cells(L[i])
    c[1] = c[1] + " again"
    L.insert(i + 1, join_cells(c))
    put_lines(D, ENTRY, L)


def f_bare_quote(rid):
    def f(D):
        L = lines_of(D, ENTRY)
        i = row_index(L, rid)
        c = row_cells(L[i])
        assert c[4].startswith("`") and c[4].endswith("`"), c[4]
        c[4] = c[4][1:-1]
        L[i] = join_cells(c)
        put_lines(D, ENTRY, L)
    return f


def f_reg_url_hash(D):
    L = lines_of(D, REG)
    hits = [i for i, l in enumerate(L) if l.startswith("| S383 ")]
    assert len(hits) == 1
    old = "efb50993780079460b0cbed1363e2166a2de1d9f"
    cells = L[hits[0]].split("|")
    # cell index 2 of split("|") is the source cell (cells[0] is "", cells[1] is the id cell)
    assert old in cells[2], "hash not in source cell"
    cells[2] = cells[2].replace(old, "0" * 40, 1)
    L[hits[0]] = "|".join(cells)
    put_lines(D, REG, L)


def f_reg_anchor_append(extra):
    def f(D):
        L = lines_of(D, REG)
        hits = [i for i, l in enumerate(L) if l.startswith("| S383 ")]
        assert len(hits) == 1
        base = "ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105"
        assert base in L[hits[0]]
        L[hits[0]] = L[hits[0]].replace(base, base + extra, 1)
        put_lines(D, REG, L)
    return f


def f_tok_only_len4(D):
    t = json.loads(rd_tables_global[0])["c1"]
    q = [r for r in t["k"] if r["id"] == "K24"][0]["quote"]
    prop = "The glob step expands the watched path on this line of the pinned source."
    shared = set(TOKEN.findall(prop)) & set(TOKEN.findall(q))
    assert shared == {"glob"}, shared
    assert len(prop) >= 40
    L = lines_of(D, ENTRY)
    i = row_index(L, "K24")
    c = row_cells(L[i])
    c[1] = prop
    L[i] = join_cells(c)
    put_lines(D, ENTRY, L)


def f_host_num_own_line(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "H02")
    c = row_cells(L[i])
    c[1] = c[1] + " Line 10 of the capture is one source line."
    L[i] = join_cells(c)
    put_lines(D, ENTRY, L)


def f_k07_cross_pin_num(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "K07")
    c = row_cells(L[i])
    c[1] = c[1] + " Compare the value 492 here."
    L[i] = join_cells(c)
    put_lines(D, ENTRY, L)


def f_k04_letter_adjacent_number(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "K04")
    c = row_cells(L[i])
    c[1] = c[1] + " The cap is 200ms."
    L[i] = join_cells(c)
    put_lines(D, ENTRY, L)


def f_k07_echo_boundary(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "K07")
    c = row_cells(L[i])
    q = quote_text("K07")
    assert len(q) == 30, len(q)
    c[1] = q + " echoed on this line, no analysis added here"
    L[i] = join_cells(c)
    put_lines(D, ENTRY, L)


def f_prov_window(D):
    L = lines_of(D, ENTRY)
    filler = ["filler line %02d for the provenance window" % n for n in range(1, 16)]
    put_lines(D, ENTRY, filler + L)


def f_prov_double_verified(D):
    L = lines_of(D, ENTRY)
    assert L[1] == "verified-at: 2026-10-28", L[1]
    L.insert(2, "verified-at: 2026-10-28")
    put_lines(D, ENTRY, L)


def f_prov_typo_id(D):
    L = lines_of(D, ENTRY)
    assert L[0].startswith("source: ")
    L[0] = L[0] + " S38"
    put_lines(D, ENTRY, L)


def f_readme_midline(D):
    raw = rd(D, README).decode("utf-8")
    raw = raw + "see | `knowledge/hyprland-config-autoreload-r56.md` for the chain\n"
    wr(D, README, raw)


def f_host_pin_byte(D):
    b = bytearray(rd(D, FETCH + "host-getoption.json"))
    k = b.index(b"false")
    b[k] = ord("g")
    wr(D, FETCH + "host-getoption.json", bytes(b))


def f_double_backtick_fence(D):
    L = lines_of(D, ENTRY)
    i = row_index(L, "K01")
    L.insert(i, "``")
    put_lines(D, ENTRY, L)


def f_row_past_eof(D):
    t = json.loads(rd_tables_global[0])
    for r in t["c1"]["k"]:
        if r["id"] == "K03":
            r["line"] = 113  # ConfigWatcher.cpp split length is 112: line 113 = split_len + 1
    wr(D, TABLES, json.dumps(t, indent=1))


def f_new_row_ids_nine(D):
    t = json.loads(rd_tables_global[0])
    t["c1"]["new_row_ids"] = t["c1"]["new_row_ids"] + ["S391"]
    wr(D, TABLES, json.dumps(t, indent=1))


# (fixture id, mutant id, what it attacks, edit, legs pristine MUST print, legs pristine MUST NOT print)
FIXTURES = [
    ("F01", "M05", "row: '|' inside a cell (no spaces) must be rejected", f_pipe_in_cell,
     ["row:K01"], []),
    ("F02", "M07", "row: proposition with a leading space must be rejected", f_prop_leading_space,
     ["row:K01"], []),
    ("F03", "M09", "row: non-ASCII digit in the source id must be rejected", f_src_nonascii_digit,
     ["row:K01"], []),
    ("F04", "M12", "row: a duplicated row must not contribute its cells to the collateral legs",
     f_duplicate_row_k08, ["row:K08", "source_cell:K08", "tok:K08", "echo:K08"], []),
    ("F05", "M13 M14", "quote: a bare (unbackticked) quote cell must fail the quote leg",
     f_bare_quote("K01"), ["row:K01", "quote:K01"], []),
    ("F06", "M18", "host: a bare quote cell on an H row must fail host:", f_bare_quote("H01"),
     ["host:H01", "quote:H01"], []),
    ("F07", "M21", "source_cell: a URL whose revision token is absent must fail", f_reg_url_hash,
     ["source_cell:K03", "source_cell:K12", "new_rows"], []),
    ("F08", "M26", "scope: a reversed locator past EOF must fail every row of that pin",
     f_reg_anchor_append(",200-40"), ["scope:K03", "scope:K12"], []),
    ("F09", "M28", "scope: a locator past EOF vetoes even when another locator covers the line",
     f_reg_anchor_append(",200"), ["scope:K03", "scope:K12"], []),
    ("F10", "M34", "tok: a 4-character shared identifier is an identifier token (regex {3,})",
     f_tok_only_len4, [], ["tok:K24"]),
    ("F11", "M37", "num: an H row's own line number is an allowed integer", f_host_num_own_line,
     [], ["num:H02"]),
    ("F12", "M38", "num: integers of another pin must not be allowed", f_k07_cross_pin_num,
     ["num:K07"], []),
    ("F13", "M39", "num: a numeral followed by letters (200ms) is a digit run (WEAKNESS probe)",
     f_k04_letter_adjacent_number, [], ["num:K04"]),
    ("F14", "M43", "echo: a 30-character quote echoed in the proposition must fail (ECHO_MIN boundary)",
     f_k07_echo_boundary, ["echo:K07"], []),
    ("F15", "M44", "prov: source/verified/recheck must lie in the first 15 lines", f_prov_window,
     ["prov"], []),
    ("F16", "M45", "prov: exactly one verified-at line", f_prov_double_verified, ["prov"], []),
    ("F17", "M49", "prov: an S-token that is not S### on the source line is not a registry id (WEAKNESS probe)",
     f_prov_typo_id, [], ["prov"]),
    ("F18", "M50", "index: a README line not starting with the prefix must not count",
     f_readme_midline, [], ["index"]),
    ("F19", "M57", "pin_hash: host pin blobs are frozen and must hash-check", f_host_pin_byte,
     ["pin_hash"], []),
    ("F20", "M65", "scanner: a two-backtick line is not a fence", f_double_backtick_fence,
     [], ["row:K01", "row:K02", "row:K10"]),
    ("F21", "M16", "witness (verdict-equivalent): a frozen row line one past the pin's split length",
     f_row_past_eof, ["quote:K03", "tables_sha"], []),
    ("F22", "M53", "witness (verdict-equivalent): a new_row_ids list of nine ids", f_new_row_ids_nine,
     ["new_rows", "tables_sha"], []),
]


# ------------------------------------------------------------------ run

def run_counter(counter, repo, rev, work):
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--work", work],
                       cwd=work, env=env(work), capture_output=True, timeout=300)
    return {"rc": p.returncode, "out": p.stdout.decode("utf-8", "replace"),
            "err": p.stderr.decode("utf-8", "replace").strip()[-300:]}


def build_fixture(base, rev, scratch, fx_id, edit):
    D = tempfile.mkdtemp(prefix="fx-%s-" % fx_id.lower(), dir=scratch)
    subprocess.run(["git", "-C", base, "archive", rev, "--", ENTRY, REG, README, TABLES, FETCH],
                   check=True, stdout=open(os.path.join(scratch, "_arc.tar"), "wb"))
    subprocess.run(["tar", "-x", "-C", D, "-f", os.path.join(scratch, "_arc.tar")], check=True)
    subprocess.run(["git", "-C", D, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], capture_output=True,
                         text=True, check=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(D), (top, D)
    edit(D)
    subprocess.run(["git", "-C", D, "add", "-A"], check=True)
    subprocess.run(["git", "-C", D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "-c",
                    "commit.gpgsign=false", "commit", "-q", "-m", "fixture %s" % fx_id], check=True)
    sha = subprocess.run(["git", "-C", D, "rev-parse", "HEAD"], capture_output=True, text=True,
                         check=True).stdout.strip()
    return D, sha


def legs_of(out):
    if " missed=" not in out:
        return None
    m = out.strip().rsplit(" missed=", 1)[1]
    return [] if m == "none" else m.split(",")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="scratch git repo of the 28fc86ac archive")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    os.makedirs(scratch, exist_ok=True)

    pristine_src = mutate.read_pristine(a.base, a.rev)
    pristine_lines = pristine_src.split("\n")
    pristine_path = os.path.join(scratch, "pristine-counter.py")
    with open(pristine_path, "w", encoding="utf-8") as fh:
        fh.write(pristine_src)
    mutants = {m[0]: m for m in mutate.MUTANTS}

    arc_tables = subprocess.run(["git", "-C", a.base, "show", "%s:%s" % (a.rev, TABLES)],
                                capture_output=True, check=True).stdout
    rd_tables_global[0] = arc_tables.decode("utf-8")

    results = []
    try:
        for fx_id, mids, attacks, edit, must_have, must_not in FIXTURES:
            mid_list = mids.split()
            D, sha = build_fixture(a.base, a.rev, scratch, fx_id, edit)
            work = os.path.join(scratch, "w-" + fx_id)
            pr = run_counter(pristine_path, D, sha, os.path.join(work, "p"))
            pr_legs = legs_of(pr["out"])
            pr_ok = (pr["rc"] in (0, 1) and pr_legs is not None
                     and all(x in pr_legs for x in must_have)
                     and not any(x in pr_legs for x in must_not))
            muts = []
            for mid in mid_list:
                _, label, lineno, old, new = mutants[mid]
                mlines, err = mutate.apply_mutant(pristine_lines, lineno, old, new)
                assert err is None, err
                mpath = os.path.join(scratch, "mut-%s-%s.py" % (fx_id, mid))
                with open(mpath, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(mlines))
                mr = run_counter(mpath, D, sha, os.path.join(work, "m-" + mid))
                differs = (mr["out"] != pr["out"]) or (mr["rc"] != pr["rc"])
                muts.append({"mutant": mid, "label": label, "line": lineno,
                             "old": old, "new": new, "rc": mr["rc"], "out": mr["out"].strip(),
                             "err": mr["err"], "killed": differs})
            results.append({"fixture": fx_id, "attacks": attacks, "repo_sha": sha,
                            "pristine": {"rc": pr["rc"], "out": pr["out"].strip(), "err": pr["err"],
                                         "legs": pr_legs},
                            "pristine_expectation_holds": pr_ok,
                            "must_have": must_have, "must_not": must_not, "mutants": muts})
            shutil.rmtree(D, ignore_errors=True)
            shutil.rmtree(work, ignore_errors=True)
            print("%s %-10s pristine_expectation=%s  %s" % (
                fx_id, mids, "ok" if pr_ok else "FAIL", " ".join(
                    "%s:%s" % (m["mutant"], "KILLED" if m["killed"] else "SURVIVED") for m in muts)),
                flush=True)
            print("     pristine: rc=%s %s" % (pr["rc"], pr["out"].strip()[:230]), flush=True)
            for m in muts:
                print("     %s rc=%s %s" % (m["mutant"], m["rc"], (m["out"] or m["err"])[:230]), flush=True)
    finally:
        try:
            os.remove(os.path.join(scratch, "_arc.tar"))
        except OSError:
            pass
    out = a.out or os.path.join(scratch, "killers.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("results: %s" % out)


if __name__ == "__main__":
    main()
