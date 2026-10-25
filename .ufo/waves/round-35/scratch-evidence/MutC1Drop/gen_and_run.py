#!/usr/bin/env python3
"""MutC1Drop harness: drop one clause of c1/count.py at a time, run every mutant
over every control tree, and diff the mutant verdict against the committed
counter's verdict. Writes mutants + results under scratch/MutC1Drop/.

Each mutant is a single-string replacement (or list of replacements) applied to
the committed source; every replacement must match exactly once or the mutant
is skipped and reported. Guards added where a dropped clause would otherwise
crash the interpreter (IndexError/TypeError/AttributeError), never to change
verdict semantics.
"""
import pathlib, subprocess, sys, json

WAVE = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35")
SRC = WAVE / "c1" / "count.py"
FROZEN = WAVE / "c1" / "frozen.json"
SCRATCH = WAVE / "scratch" / "MutC1Drop"
MUT_DIR = SCRATCH / "mutants"
RES = SCRATCH / "results.json"

OK_OLD = """            ok = (
                blob is not None
                and row is not None
                and nf_ok
                and used_by == citing
                and cs[7] == "mined"
                and valid_recheck(cs[9])
                and receipt["sha256"] in cs[5]
                and quote is not None
                and 1 <= len(words) <= 25
                and quote.encode() in blob
            )"""


def ok_new(dropped):
    lines = [
        "            ok = (",
        "                blob is not None",
        "                and row is not None",
        "                and nf_ok",
        "                and used_by == citing",
        '                and cs[7] == "mined"',
        "                and valid_recheck(cs[9])",
        '                and receipt["sha256"] in cs[5]',
        "                and quote is not None",
        "                and 1 <= len(words) <= 25",
        "                and quote.encode() in blob",
        "            )",
    ]
    subs = {
        "blob": ("blob is not None", None),
        "row": ("and row is not None", None),
        "nf": ("and nf_ok", None),
        "used_by": ("and used_by == citing", None),
        "status": ('and cs[7] == "mined"', None),
        "recheck": ("and valid_recheck(cs[9])", None),
        "digest": ('and receipt["sha256"] in cs[5]', None),
        "quote_exists": ("and quote is not None", None),
        "word_bound": ("and 1 <= len(words) <= 25", None),
        "substring": ("and quote.encode() in blob", 'and (quote or "").encode() in blob'),
    }
    text = "\n".join(
        l for i, l in enumerate(lines) if i == 0 or i == len(lines) - 1
        or l.strip() not in (
            subs[dropped][0].strip() if dropped in subs else "\x00",)
    )
    return text


MUTANTS = {}


def add(mid, desc, repls):
    MUTANTS[mid] = {"desc": desc, "repls": repls}


# M01 blob-present: drop 'blob is not None'; substring clause keeps a guard so
# a missing receipt still cannot close a cite (b"" membership is not a kill).
add("m01-blob-present", "drop conjunct `blob is not None` (receipt readable)", [
    (OK_OLD, """            ok = (
                row is not None
                and nf_ok
                and used_by == citing
                and cs[7] == "mined"
                and valid_recheck(cs[9])
                and receipt["sha256"] in cs[5]
                and quote is not None
                and 1 <= len(words) <= 25
                and (blob is None or quote.encode() in blob)
            )""")])

# M02 row-exactly-one: duplicate rows tolerated; first matching row wins.
add("m02-row-exactly-one", "drop `row is not None` (exactly one registry row)", [
    ("            row = rows[0] if len(rows) == 1 else None",
     "            row = rows[0] if len(rows) >= 1 else None")])

# M03 row-well-formed: drop the 11-cell count; positional cells keep index
# guards so a short row cannot crash the interpreter.
add("m03-row-well-formed", "drop `nf_ok` (row has exactly 11 cells)", [
    ("            nf_ok = len(cs) == 11\n            used_by = set()\n            if nf_ok and cs[10]:",
     "            nf_ok = len(cs) == 11\n            used_by = set()\n            if len(cs) > 10 and cs[10]:"),
    (OK_OLD, """            ok = (
                blob is not None
                and row is not None
                and used_by == citing
                and len(cs) > 7 and cs[7] == "mined"
                and len(cs) > 9 and valid_recheck(cs[9])
                and len(cs) > 5 and receipt["sha256"] in cs[5]
                and quote is not None
                and 1 <= len(words) <= 25
                and quote.encode() in blob
            )""")])

# M04 used-by-exact
add("m04-used-by-exact", "drop `used_by == citing`", [
    (OK_OLD, OK_OLD.replace("                and used_by == citing\n", ""))])

# M05 status-mined
add("m05-status-mined", "drop `cs[7] == \"mined\"`", [
    (OK_OLD, OK_OLD.replace('                and cs[7] == "mined"\n', ""))])

# M06 recheck-valid
add("m06-recheck-valid", "drop `valid_recheck(cs[9])`", [
    (OK_OLD, OK_OLD.replace("                and valid_recheck(cs[9])\n", ""))])

# M07 digest-match
add("m07-digest-match", "drop `receipt[\"sha256\"] in cs[5]`", [
    (OK_OLD, OK_OLD.replace('                and receipt["sha256"] in cs[5]\n', ""))])

# M08 quote-exists-exactly-one: a cite may close without any gate-quote line.
# Guard substring/word-bound so a missing line is not a crash; the absence then
# counts as satisfying this clause alone.
add("m08-quote-exists", "drop `quote is not None` (exactly one gate-quote line)", [
    (OK_OLD, OK_OLD.replace("                and quote is not None\n", "")
                   .replace("                and 1 <= len(words) <= 25\n",
                            "                and (quote is None or 1 <= len(words) <= 25)\n")
                   .replace("                and quote.encode() in blob\n",
                            '                and (quote is None or quote.encode() in blob)\n'))])

# M09 word-bound
add("m09-word-bound", "drop `1 <= len(words) <= 25`", [
    (OK_OLD, OK_OLD.replace("                and 1 <= len(words) <= 25\n", ""))])

# M10 quote-substring
add("m10-quote-substring", "drop `quote.encode() in blob`", [
    (OK_OLD, OK_OLD.replace("                and quote.encode() in blob\n", ""))])

# M11 entry-regular: entry path read with a plain symlink-following open;
# receipts and SOURCES.md keep read_regular.
add("m11-entry-regular", "drop `entry path is regular` (read_regular -> Path.read_bytes, entries only)", [
    ("        entry_bytes = read_regular(root, entry_rel)",
     "        try:\n            entry_bytes = (root / entry_rel).read_bytes()\n        except OSError:\n            entry_bytes = None")])

# M12 o-nofollow-open (declared not-load-bearing; verify empirically)
add("m12-o-nofollow", "drop `os.O_NOFOLLOW` from the open()", [
    ("os.open(cur, os.O_RDONLY | os.O_NOFOLLOW)", "os.open(cur, os.O_RDONLY)")])

# M13 sislnk-component-walk: drop only the S_ISLNK reject inside the component
# walk (root lstat check kept). Ledger claims this half is load-bearing.
add("m13-sislnk-walk", "drop the S_ISLNK reject in the component walk", [
    ("""        if stat.S_ISLNK(st.st_mode):
            return None
        last = i == len(parts) - 1""",
     """        last = i == len(parts) - 1""")])

# M14 entry-closed-read: a closed entry no longer requires its bytes to exist.
add("m14-entry-closed-read", "drop `entry_closed = entry_bytes is not None` seed", [
    ("        entry_closed = entry_bytes is not None", "        entry_closed = True")])

# M15 nlink-single: multi-link regular files accepted.
add("m15-nlink-single", "drop `st.st_nlink != 1` hardlink reject", [
    ("if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:",
     "if not stat.S_ISREG(st.st_mode):")])

src = SRC.read_text()
MUT_DIR.mkdir(parents=True, exist_ok=True)
built = {}
for mid, m in MUTANTS.items():
    body = src
    for old, new in m["repls"]:
        n = body.count(old)
        if n != 1:
            built[mid] = {"error": f"pattern match count={n} for {old[:60]!r}"}
            body = None
            break
        body = body.replace(old, new, 1)
    if body is not None:
        p = MUT_DIR / f"{mid}.py"
        p.write_text(body)
        built[mid] = {"path": str(p)}

controls = sorted(
    d for d in (WAVE / "controls").iterdir() if d.is_dir())


def run(counter, root):
    r = subprocess.run(
        [sys.executable, "-I", str(counter), "--root", str(root),
         "--frozen", str(FROZEN)],
        capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


baseline = {}
for c in controls:
    rc, out = run(SRC, c)
    baseline[c.name] = {"rc": rc, "out": out}

results = {"baseline": baseline, "mutants": {}}
for mid, info in built.items():
    if "error" in info:
        results["mutants"][mid] = {"desc": MUTANTS[mid]["desc"], "error": info["error"]}
        continue
    entry = {"desc": MUTANTS[mid]["desc"], "runs": {}}
    for c in controls:
        rc, out = run(info["path"], c)
        flip = out != baseline[c.name]["out"] or rc != baseline[c.name]["rc"]
        entry["runs"][c.name] = {"rc": rc, "out": out, "flip": flip}
    results["mutants"][mid] = entry

RES.write_text(json.dumps(results, indent=1))

# console summary
verdict_of = {}
for c, b in baseline.items():
    verdict_of[c] = "MET" if "verdict=TARGET_MET" in b["out"] else "MISSED"
print("BASELINE:")
for c, b in baseline.items():
    print(f"  {c:24s} rc={b['rc']} {b['out'].splitlines()[-1]}")
print("\nMUTANTS (verdict flips vs baseline):")
for mid, e in results["mutants"].items():
    if "error" in e:
        print(f"  {mid:24s} BUILD ERROR: {e['error']}")
        continue
    flips = []
    for c, r in e["runs"].items():
        mv = "MET" if "verdict=TARGET_MET" in r["out"] else "MISSED"
        if mv != verdict_of[c]:
            flips.append(f"{c}: {verdict_of[c]}->{mv}")
        elif r["out"] != baseline[c]["out"]:
            flips.append(f"{c}: counters-changed({r['out'].split('verdict=')[0].strip()})")
    print(f"  {mid:24s} {'; '.join(flips) if flips else 'DEAD (no verdict change, no counter change)'}")
