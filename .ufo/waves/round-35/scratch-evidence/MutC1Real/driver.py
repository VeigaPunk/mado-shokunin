#!/usr/bin/env python3
"""MutC1Real driver: single-clause mutation matrix for PRED-C1-r35-v1 on the REAL tree copy.

REBUILT FROM TRANSCRIPT after the ~03:45 external sweep removed scratch/MutC1Real/.
Behaviour is the script that produced the 28 runs reported in
.ufo/waves/round-35/w2/reports/MutC1Real.md.

Arm A: drop exactly one clause from the counter (code-only; PREDICATE string untouched so
       frozen.json still matches -> no predicate-drift) and run on pristine real bytes.
Arm B: violate exactly one clause in a fresh copy of the real bytes and run the pristine
       counter unchanged.
Gap  : probes for behaviour the code enforces but c1/clauses.json does not enumerate.
TOCTOU: witness that O_NOFOLLOW is observable only once the S_ISLNK walk is removed.

Writes only under scratch/MutC1Real/.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess

S = pathlib.Path(__file__).resolve().parent
ROOT = S / "root"
PRISTINE_COUNTER = S / "counter-pristine.py"
ARMS = S / "arms"
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin")

shutil.copy2(ROOT / ".ufo/waves/round-35/c1/count.py", PRISTINE_COUNTER)
ARMS.mkdir(exist_ok=True)


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(counter: pathlib.Path, root: pathlib.Path) -> dict:
    r = subprocess.run(
        ["python3", "-I", str(counter), "--root", str(root),
         "--frozen", str(root / ".ufo/waves/round-35/c1/frozen.json")],
        capture_output=True, text=True)
    m = re.search(r"closed_entries=(\d+) closed_rows=(\d+) open_cites=(\d+) verdict=(\w+)",
                  r.stdout)
    return {"exit": r.returncode, "stdout": r.stdout.strip(),
            "stderr": r.stderr.strip(), "counts": list(map(int, m.groups()[:3])) if m else None,
            "verdict": m.group(4) if m else None}


def sub1(text: str, old: str, new: str) -> str:
    n = text.count(old)
    assert n == 1, f"anchor not unique ({n}): {old!r}"
    return text.replace(old, new)


def fresh_root(tag: str) -> pathlib.Path:
    dst = ARMS / tag / "root"
    if dst.exists():
        shutil.rmtree(ARMS / tag)
    shutil.copytree(ROOT, dst)
    return dst


def entries_text(root: pathlib.Path) -> tuple[pathlib.Path, str]:
    p = root / "corpus/SOURCES.md"
    return p, p.read_text()


def rowline(sources: str, sid: str) -> tuple[list[str], int]:
    pat = re.compile(r"^ {0,3}\|\s*" + sid + r"\s*\|")
    lines = sources.splitlines()
    hits = [i for i, l in enumerate(lines) if pat.match(l)]
    assert len(hits) == 1, (sid, len(hits))
    return lines, hits[0]


def put_row(root: pathlib.Path, sid: str, fn) -> str:
    p, src = entries_text(root)
    lines, i = rowline(src, sid)
    lines[i] = fn(lines[i])
    p.write_text("\n".join(lines) + "\n")
    return sha(p)


def quote_line_swap(root: pathlib.Path, entry_rel: str, sid: str, new_quote: str) -> str:
    p = root / entry_rel
    txt = p.read_text()
    needle = f"gate-quote: {sid} "
    lines = txt.splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith(needle)]
    assert len(idx) == 1, (entry_rel, sid, len(idx))
    lines[idx[0]] = needle + new_quote
    p.write_text("\n".join(lines) + "\n")
    return sha(p)


results: dict[str, dict] = {}

# ---------------------------------------------------------------- arm A (counter drop)
ARM_A = [
    ("entry-regular",
     [("        if stat.S_ISLNK(st.st_mode):", "        if False:"),
      ("        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:", "        if False:")]),
    ("entry-metric",
     ("        entry_closed = entry_bytes is not None", "        entry_closed = True")),
    ("row-unique", "            row = rows[0] if len(rows) == 1 else None",
     "            row = rows[0] if rows else None"),
    ("row-well-formed", "            nf_ok = len(cs) == 11",
     "            nf_ok = True"),
    ("used-by-exact", "                and used_by == citing",
     "                and True"),
    ("status-mined", '                and cs[7] == "mined"',
     "                and True"),
    ("recheck-valid", "                and valid_recheck(cs[9])",
     "                and True"),
    ("digest-match", '                and receipt["sha256"] in cs[5]',
     "                and True"),
    ("gate-quote-substring", "                and quote.encode() in blob",
     "                and True"),
    ("gate-quote-word-bound", "                and 1 <= len(words) <= 25",
     "                and True"),
    ("o-nofollow-open", "        fd = os.open(cur, os.O_RDONLY | os.O_NOFOLLOW)",
     "        fd = os.open(cur, os.O_RDONLY)"),
]

src = PRISTINE_COUNTER.read_text()
for item in ARM_A:
    clause = item[0]
    rest = item[1:]
    if len(rest) == 1:
        muts = rest[0]
        muts = [muts] if isinstance(muts, tuple) else list(muts)
    else:
        muts = [(rest[0], rest[1])]
    d = ARMS / f"A-{clause}"
    d.mkdir(parents=True, exist_ok=True)
    counter = d / "count.py"
    text = src
    for old, new in muts:
        text = sub1(text, old, new)
    counter.write_text(text)
    assert text != src
    results[f"A:{clause}"] = {"arm": "A", "clause": clause,
                              "mutations": [[o, n] for o, n in muts],
                              "counter_sha256": sha(counter),
                              "root_sha_sources": sha(ROOT / "corpus/SOURCES.md"),
                              **run(counter, ROOT)}

# ---------------------------------------------------------------- arm B (data violation)
def armB(tag: str, clause: str, mutate, note: str = "") -> None:
    root = fresh_root(f"B-{tag}")
    mutated = mutate(root)
    results[f"B:{clause}"] = {"arm": "B", "clause": clause, "tag": tag, "note": note,
                              "root": str(root), "mutated": mutated,
                              **run(PRISTINE_COUNTER, root)}


# 1. entry-regular: entry becomes a symlink to a regular copy
def m_entry_symlink(root):
    p = root / "corpus/knowledge/idle-lock-never-asked-r12.md"
    real = p.with_name(p.name + ".real")
    p.rename(real)
    os.symlink(real.name, p)
    return {"file": "corpus/knowledge/idle-lock-never-asked-r12.md", "kind": "symlink->regular copy",
            "sha_after": sha(real)}


armB("entry-regular", "entry-regular", m_entry_symlink)


# 2. row-unique: duplicate the S205 row verbatim
def m_row_dup(root):
    p, s = entries_text(root)
    lines, i = rowline(s, "S205")
    lines.insert(i + 1, lines[i])
    p.write_text("\n".join(lines) + "\n")
    return {"file": "corpus/SOURCES.md", "kind": "duplicate S205 row", "sha_after": sha(p)}


armB("row-unique", "row-unique", m_row_dup)


# 3. row-well-formed: append a 12th cell to the S206 row (used-by cell untouched)
def m_row_extra(root):
    s = put_row(root, "S206", lambda l: l + " extra |")
    return {"file": "corpus/SOURCES.md", "kind": "+1 cell on S206 row", "sha_after": s}


armB("row-well-formed", "row-well-formed", m_row_extra)


# 4. used-by-exact: add a token that no admitted entry citing S207 supplies
def m_usedby(root):
    s = put_row(root, "S207", lambda l: l[:-1].rstrip()
                + ", corpus/knowledge/idle-lock-chain-armed-r14.md |")
    return {"file": "corpus/SOURCES.md", "kind": "+1 used-by token on S207", "sha_after": s}


armB("used-by-exact", "used-by-exact", m_usedby)


# 5. status-mined: S203 status queued
def m_status(root):
    s = put_row(root, "S203", lambda l: sub1(l, "| mined |", "| queued |"))
    return {"file": "corpus/SOURCES.md", "kind": "S203 status queued", "sha_after": s}


armB("status-mined", "status-mined", m_status)


# 6. recheck-valid: S204 recheck becomes a non-cadence token (token read from live row)
def m_recheck(root):
    p, s = entries_text(root)
    lines, i = rowline(s, "S204")
    parts = lines[i].split("|")[1:-1]
    cur = [x.strip() for x in parts][9]
    new = lines[i].replace(f"| {cur} |", "| 2026/Q1 |", 1)
    assert new != lines[i]
    lines[i] = new
    p.write_text("\n".join(lines) + "\n")
    return {"file": "corpus/SOURCES.md", "kind": f"S204 recheck {cur} -> 2026/Q1",
            "sha_after": sha(p)}


armB("recheck-valid", "recheck-valid", m_recheck)


# 7. digest-match: S208 anchor carries a wrong sha256
FROZEN = json.loads((ROOT / ".ufo/waves/round-35/c1/frozen.json").read_text())
GOOD = FROZEN["receipts"]["S208"]["sha256"]
BAD = GOOD[:-1] + ("0" if GOOD[-1] != "0" else "1")


def m_digest(root):
    s = put_row(root, "S208", lambda l: sub1(l, GOOD, BAD))
    return {"file": "corpus/SOURCES.md", "kind": "S208 receipt sha256 mutated", "sha_after": s}


armB("digest-match", "digest-match", m_digest)


# 8. gate-quote-substring: S209 quote is plausible but absent from the receipt
ABSENT = ("four dated copies of the bar's configuration each carry the idle-lock handler")


def m_quote_absent(root):
    blob = (root / ".ufo/waves/round-35/fetch/S209.receipt.txt").read_bytes()
    assert ABSENT.encode() not in blob
    s = quote_line_swap(root, "corpus/knowledge/idle-lock-offered-in-the-bar-r15.md", "S209", ABSENT)
    return {"file": "corpus/knowledge/idle-lock-offered-in-the-bar-r15.md",
            "kind": "S209 quote absent from receipt (13 words)", "sha_after": s}


armB("gate-quote-substring", "gate-quote-substring", m_quote_absent)


# 9. gate-quote-word-bound: S203 quote becomes a 26-word contiguous receipt substring
def long_quote() -> str:
    blob = (ROOT / ".ufo/waves/round-35/fetch/S203.receipt.txt").read_text()
    line = max(blob.splitlines(), key=lambda l: len(l.split()))
    spans = list(re.finditer(r"\S+", line))
    assert len(spans) >= 26
    q = line[: spans[25].end()]
    assert len(q.split()) == 26
    assert q.encode() in blob.encode()
    return q


LONG = long_quote()


def m_word_bound(root):
    s = quote_line_swap(root, "corpus/knowledge/idle-lock-never-asked-r12.md", "S203", LONG)
    return {"file": "corpus/knowledge/idle-lock-never-asked-r12.md",
            "kind": "S203 quote = 26-word contiguous receipt substring", "sha_after": s}


armB("gate-quote-word-bound", "gate-quote-word-bound", m_word_bound)


# 10. o-nofollow-open: no static witness. Prove it by removal of the sibling guards.
def m_hardlink(root):
    p = root / "corpus/knowledge/idle-lock-never-asked-r12.md"
    copy = root / "corpus/knowledge/.r12.hardlink-src"
    shutil.copy2(p, copy)
    p.unlink()
    os.link(copy, p)
    st = p.lstat()
    return {"file": "corpus/knowledge/idle-lock-never-asked-r12.md",
            "kind": f"hardlink (nlink={st.st_nlink})", "sha_after": sha(copy)}


armB("o-nofollow-open", "o-nofollow-open", m_hardlink,
     "no static symlink/fifo/hardlink witness survives the S_ISLNK/nlink walk; hardlink is "
     "rejected by st_nlink!=1 before open()")

# TOCTOU witness: strip the S_ISLNK walk + nlink guard, then a symlinked entry is
# observable ONLY through O_NOFOLLOW.
WALK_OFF = sub1(sub1(src, "        if stat.S_ISLNK(st.st_mode):", "        if False:"),
                "        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:",
                "        if False:")
for tag, counter_src in (("walk-off+NOFOLLOW", WALK_OFF),
                         ("walk-off+NO-NOFOLLOW",
                          sub1(WALK_OFF, "os.O_RDONLY | os.O_NOFOLLOW", "os.O_RDONLY"))):
    d = ARMS / f"C-{tag}"
    d.mkdir(parents=True, exist_ok=True)
    c = d / "count.py"
    c.write_text(counter_src)
    root = fresh_root(f"C-{tag}-data")
    m_entry_symlink(root)
    results[f"C:{tag}"] = {"arm": "C", "clause": "o-nofollow-open", "tag": tag,
                           "counter_sha256": sha(c), **run(c, root)}

# ---------------------------------------------------------------- gap probes (undeclared)
def m_quote_dup(root):
    p = root / "corpus/knowledge/idle-lock-never-asked-r12.md"
    txt = p.read_text()
    needle = "gate-quote: S203 "
    lines = txt.splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith(needle)][0]
    lines.insert(idx + 1, lines[idx])
    p.write_text("\n".join(lines) + "\n")
    return {"file": "corpus/knowledge/idle-lock-never-asked-r12.md",
            "kind": "duplicate S203 gate-quote line", "sha_after": sha(p)}


armB("gap-quote-unique", "quote-uniqueness (undeclared)", m_quote_dup,
     "predicate says exactly one gate-quote line; not enumerated in clauses.json")


def m_receipt_symlink(root):
    p = root / ".ufo/waves/round-35/fetch/S206.receipt.txt"
    real = p.with_name(p.name + ".real")
    p.rename(real)
    os.symlink(real.name, p)
    return {"file": ".ufo/waves/round-35/fetch/S206.receipt.txt",
            "kind": "receipt becomes symlink", "sha_after": sha(real)}


armB("gap-receipt-regular", "receipt-regularity (undeclared)", m_receipt_symlink,
     "code requires blob is not None (receipt regular); predicate names only the entry path")


def m_vacuous_quote(root):
    blob = (root / ".ufo/waves/round-35/fetch/S203.receipt.txt").read_bytes()
    assert b"the" in blob
    s = quote_line_swap(root, "corpus/knowledge/idle-lock-never-asked-r12.md", "S203", "the")
    return {"file": "corpus/knowledge/idle-lock-never-asked-r12.md",
            "kind": "S203 quote = the single word 'the' (1 word, in receipt)", "sha_after": s}


armB("gap-vacuous-quote", "gate-quote-evidence-strength (no clause violated)", m_vacuous_quote,
     "1..25-word bound and substring test are both satisfied by one common word")

# ---------------------------------------------------------------- cross matrix (A counter x B tree)
CLAUSE_IDS = ["entry-regular", "row-unique", "row-well-formed", "used-by-exact",
              "status-mined", "recheck-valid", "digest-match", "gate-quote-substring",
              "gate-quote-word-bound", "o-nofollow-open"]
cross = {}
for cid in CLAUSE_IDS:
    a_counter = ARMS / f"A-{cid}" / "count.py"
    b_root = pathlib.Path(results[f"B:{cid}"]["root"])
    cross[cid] = run(a_counter, b_root)
results["CROSS"] = cross

# extra attribution: O_NOFOLLOW drop against the symlinked-entry tree (walk intact)
results["X:o-nofollow-drop x symlink-data"] = run(
    ARMS / "A-o-nofollow-open/count.py", pathlib.Path(results["B:entry-regular"]["root"]))
# wholesale entry-regular drop against the hardlinked-entry tree (nlink guard is part of it)
results["X:entry-regular-drop x hardlink-data"] = run(
    ARMS / "A-entry-regular/count.py", pathlib.Path(results["B:o-nofollow-open"]["root"]))

# symbolic-cadence weakness: valid_recheck accepts bare prose
import importlib.util
spec_ = importlib.util.spec_from_file_location("c1count", ROOT / ".ufo/waves/round-35/c1/count.py")
mod = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(mod)
probe_cells = ["on-change", "90d", "2026-10-24", "some day maybe",
               "review whenever we feel like it", "when the mood strikes",
               "next sprint/when free", "2026/Q1", "TBD!", "never"]
recheck_probe = {c: mod.valid_recheck(c) for c in probe_cells}

out = {"baseline": run(PRISTINE_COUNTER, ROOT), "recheck_probe": recheck_probe,
       "long_quote_words": len(LONG.split()), "results": results}
(S / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))

print("BASELINE:", out["baseline"]["stdout"], "| exit", out["baseline"]["exit"])
print("\n%-42s %-8s %-9s %-12s %s" % ("arm:clause", "exit", "verdict", "counts", "stdout-shape"))
for k, v in results.items():
    if k == "CROSS":
        continue
    ci = v["counts"]
    arith = "" if ci is None else f" rows+open={ci[1]+ci[2]}"
    print("%-42s %-8s %-9s %-12s%s" % (k, v["exit"], v["verdict"], ci, arith))
print("\n2x2 (A counter x B tree):")
for cid, v in results["CROSS"].items():
    print("%-28s A-only=%-9s B-only=%-9s A+B=%-9s" % (
        cid, results[f"A:{cid}"]["verdict"], results[f"B:{cid}"]["verdict"], v["verdict"]))
print("\nrecheck probe:", json.dumps(recheck_probe))
