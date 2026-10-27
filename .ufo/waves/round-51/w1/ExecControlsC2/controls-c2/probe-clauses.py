#!/usr/bin/env python3
"""Spec-faithful clause probe for PRED-C2-r51 — control-fixture instrument.

This is NOT the frozen counter. The frozen counter is
`quality/counters/c2-r51-dispatch-entry.py` (arrives with w1/ExecCounterC2). This probe exists so
the C2 negative controls can be MEASURED before that counter lands, against the literal wording of
the frozen sentence in `.ufo/waves/round-51/claims.md` (C2 clause (a)-(d)).

It reads every input through git at an explicit revision, so a fixture commit is scored exactly as
a counter addressed by `--repo <lane> --rev <rev>` would see it.

Clause readings applied (documented because the frozen sentence leaves grammar implicit):

(a) `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` exists at <rev> and the same path
    string occurs in `corpus/README.md` at <rev>.
(b) The entry's `source:` lines cite at least two DISTINCT row ids in S364-S379. Each cited row in
    `corpus/SOURCES.md` at <rev> must carry status `mined` and opened `2026-10-27`; its anchor cell
    must name a pin as `.ufo/waves/round-<n>/fetch/<basename>:<line>`; that basename must occur
    verbatim in the entry (the entry's pin manifest) and the pin file must exist under
    `.ufo/waves/round-51/fetch/` at <rev>; the row's quote is the first double-quoted span of its
    `teaches` cell, must be <=25 whitespace-separated words, and must occur verbatim on the pin's
    cited line.
(c) Word-8-gram overlap of the entry against every `corpus/knowledge/*.md` at <base> and every file
    under `.ufo/waves/round-*/candidate/` (recursive) at <base>, per file, must be <=30%. Overlap is
    |entry_shingles AND file_shingles| / |entry_shingles|; tokens are lowercase `[a-z0-9_]+` runs.
(d) `held:` citation lines of the form
        held: corpus/knowledge/<file>.md:<line> tokens=<t1>[,<t2>...]
    must number >=3 distinct (file,line) pairs; each file must exist at <base>, the line must exist
    at <base>, and the raw line must contain every pinned token verbatim.

Output: diagnostic lines plus one final line
    PROBE_C2_R51: clauses=abcd clauses_met=<n> admitted=<1|0>/1 verdict=<TARGET_MET|TARGET_MISSED> rev=<rev>
Exit 0 only when all four clauses are met.

Scratch: nothing is written; TMPDIR/--work is accepted for interface parity with the counter.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
ROW_MIN, ROW_MAX = 364, 379
QUOTE_MAX_WORDS = 25
NGRAM = 8
OVERLAP_MAX = 0.30
TOKEN_RE = re.compile(r"[a-z0-9_]+")


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p


def exists_at(repo, rev, path):
    return git(repo, "cat-file", "-e", "%s:%s" % (rev, path), check=False).returncode == 0


def read_at(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None


def list_at(repo, rev, prefix):
    """Every blob path at <rev> starting with <prefix>."""
    out = git(repo, "ls-tree", "-r", "--name-only", rev).stdout
    return [line for line in out.splitlines() if line.startswith(prefix)]


def shingles(text, n=NGRAM):
    toks = TOKEN_RE.findall(text.lower())
    return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def overlap(entry_sh, file_text):
    fs = shingles(file_text)
    if not entry_sh:
        return 0.0
    return len(entry_sh & fs) / len(entry_sh)


def parse_rows(sources_text):
    rows = {}
    for line in sources_text.splitlines():
        if not line.startswith("| S"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 11 or not re.fullmatch(r"S\d{3,}", cells[0]):
            continue
        rows[cells[0]] = cells
    return rows


PIN_RE = re.compile(r"\.ufo/waves/round-\d+/fetch/([\w.-]+):(\d+)")
QUOTE_RE = re.compile(r'"([^"]+)"')
HELD_RE = re.compile(r"^held:\s*corpus/knowledge/([^\s:]+\.md):(\d+)\s+(?:keys?|tokens?)\s*[=:]\s*(.+?)\s*$", re.I)


def manifest_map(entry_text):
    """pin -> S-row from every entry table whose first header cell is pin/pinfile/name."""
    out, block = {}, []
    for line in (entry_text or "").splitlines() + [""]:
        if line.strip().startswith("|"):
            block.append(line.strip())
            continue
        if len(block) >= 2:
            header = [re.sub(r"[`*\s]+", "", c).lower() for c in block[0].strip("|").split("|")]
            if header and header[0] in ("pin", "pinfile", "name"):
                for row in block[1:]:
                    cells = [c.strip() for c in row.strip("|").split("|")]
                    if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                        continue
                    name = re.sub(r"[`*\s]+", "", cells[0])
                    rowid = re.sub(r"[`*\s]+", "", cells[2]) if len(cells) > 2 else ""
                    if name:
                        out[name] = rowid
        block = []
    return out


def clause_a(repo, rev, entry_text):
    ok_exists = entry_text is not None
    readme = read_at(repo, rev, README) or ""
    ok_index = os.path.basename(ENTRY) in readme
    return (ok_exists and ok_index), {"exists": int(ok_exists), "indexed": int(ok_index)}


def clause_b(repo, rev, entry_text):
    detail = {"cited_rows": [], "valid_rows": 0, "pins": 0, "manifest": 0, "quotes": 0}
    if entry_text is None:
        return False, detail
    cited = []
    for line in entry_text.splitlines():
        m = re.match(r"^source:\s*(S\d{3,})\b", line)
        if m and int(m.group(1)[1:]) in range(ROW_MIN, ROW_MAX + 1):
            cited.append(m.group(1))
    cited = sorted(set(cited))
    detail["cited_rows"] = cited
    sources = read_at(repo, rev, SOURCES) or ""
    rows = parse_rows(sources)
    man = manifest_map(entry_text)
    valid = 0
    for rid in cited:
        cells = rows.get(rid)
        if cells is None:
            detail["reason_%s" % rid] = "row-absent"
            continue
        if cells[7] != "mined" or cells[8] != "2026-10-27":
            detail["reason_%s" % rid] = "status=%s opened=%s" % (cells[7], cells[8])
            continue
        detail["valid_rows"] += 1
        anchor = cells[5]
        teaches = cells[6]
        pm = PIN_RE.search(anchor)
        qm = QUOTE_RE.search(teaches)
        if not pm:
            detail["reason_%s" % rid] = "no pin:line in anchor"
            continue
        if not qm:
            detail["reason_%s" % rid] = "no quoted span in teaches"
            continue
        pin, line_no = pm.group(1), int(pm.group(2))
        quote = qm.group(1)
        if len(quote.split()) > QUOTE_MAX_WORDS:
            detail["reason_%s" % rid] = "quote words=%d" % len(quote.split())
            continue
        detail["pins"] += 1
        if man.get(pin) != rid:
            detail["reason_%s" % rid] = "pin %s manifest row=%s" % (pin, man.get(pin, "-"))
            continue
        detail["manifest"] += 1
        pin_path = ".ufo/waves/round-51/fetch/" + pin
        pin_text = read_at(repo, rev, pin_path)
        if pin_text is None:
            detail["reason_%s" % rid] = "pin absent at rev: %s" % pin_path
            continue
        lines = pin_text.splitlines()
        if line_no < 1 or line_no > len(lines):
            detail["reason_%s" % rid] = "pin line out of range: %d" % line_no
            continue
        if quote not in lines[line_no - 1]:
            detail["reason_%s" % rid] = "quote not verbatim at %s:%d" % (pin, line_no)
            continue
        detail["quotes"] += 1
        valid += 1
    return (len(cited) >= 2 and valid >= 2), detail


def clause_c(repo, base, entry_text, entry_path=ENTRY):
    entry_sh = shingles(entry_text or "")
    baseline = [p for p in list_at(repo, base, "corpus/knowledge/")
                if p.endswith(".md") and p != entry_path]
    candidates = [p for p in list_at(repo, base, ".ufo/waves/")
                  if "/candidate/" in p]
    scored = []
    for path in baseline + candidates:
        text = read_at(repo, base, path) or ""
        scored.append((overlap(entry_sh, text), path))
    scored.sort(reverse=True)
    top = [{"file": p, "overlap": round(o, 6)} for o, p in scored[:5]]
    worst = scored[0][0] if scored else 0.0
    detail = {"baseline_files": len(baseline), "candidate_files": len(candidates),
              "shingles": len(entry_sh), "max_overlap": round(worst, 6), "top": top}
    return (worst <= OVERLAP_MAX), detail


def clause_d(repo, base, entry_text):
    detail = {"held": 0, "distinct": 0, "tokens_ok": 0}
    citations = []
    for line in (entry_text or "").splitlines():
        m = HELD_RE.match(line.strip())
        if m:
            citations.append((m.group(1), int(m.group(2)), m.group(3)))
    detail["held"] = len(citations)
    seen = set()
    for name, line_no, token_blob in citations:
        key = (name, line_no)
        if key in seen:
            detail["reason_%s:%d" % key] = "duplicate"
            continue
        seen.add(key)
        detail["distinct"] = len(seen)
        path = "corpus/knowledge/" + name
        text = read_at(repo, base, path)
        if text is None:
            detail["reason_%s:%d" % key] = "file absent at base"
            continue
        lines = text.splitlines()
        if line_no < 1 or line_no > len(lines):
            detail["reason_%s:%d" % key] = "line out of range"
            continue
        toks = [t for t in re.split(r"[,\s]+", token_blob) if t]
        missing = [t for t in toks if t not in lines[line_no - 1]]
        if missing:
            detail["reason_%s:%d" % key] = "missing tokens=%s" % ",".join(missing)
            continue
        detail["tokens_ok"] += 1
    return (len(seen) >= 3 and detail["tokens_ok"] >= 3), detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default="6ca8c559a4a3d6d361101592116eea2bc7452437")
    ap.add_argument("--entry", default=ENTRY)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if args.base.endswith("^"):
        args.base = args.base[:-1]

    entry_text = read_at(repo, args.rev, args.entry)
    a, da = clause_a(repo, args.rev, entry_text)
    b, db = clause_b(repo, args.rev, entry_text)
    c, dc = clause_c(repo, args.base, entry_text, args.entry)
    d, dd = clause_d(repo, args.base, entry_text)
    met = sum(1 for x in (a, b, c, d) if x)
    admitted = 1 if met == 4 else 0
    verdict = "TARGET_MET" if admitted else "TARGET_MISSED"

    print("PROBE_C2_R51-A: exists=%d indexed=%d rc=%d" % (da["exists"], da["indexed"], 0 if a else 1))
    print("PROBE_C2_R51-B: cited=%s valid_rows=%d pins=%d manifest=%d quotes=%d rc=%d"
          % (",".join(db["cited_rows"]) or "-", db["valid_rows"], db["pins"],
             db["manifest"], db["quotes"], 0 if b else 1))
    print("PROBE_C2_R51-C: baseline_files=%d candidate_files=%d shingles=%d max_overlap=%.4f at=%s rc=%d"
          % (dc["baseline_files"], dc["candidate_files"], dc["shingles"], dc["max_overlap"],
             dc["top"][0]["file"] if dc["top"] else "-", 1 if dc["max_overlap"] > OVERLAP_MAX else 0))
    for row in dc["top"]:
        print("PROBE_C2_R51-C-row: overlap=%.4f file=%s" % (row["overlap"], row["file"]))
    print("PROBE_C2_R51-D: held=%d distinct=%d tokens_ok=%d rc=%d"
          % (dd["held"], dd["distinct"], dd["tokens_ok"], 0 if d else 1))
    for key in sorted(k for k in db if k.startswith("reason_")):
        print("PROBE_C2_R51-B-reason: %s %s" % (key[len("reason_"):], db[key]))
    for key in sorted(k for k in dd if k.startswith("reason_")):
        print("PROBE_C2_R51-D-reason: %s %s" % (key[len("reason_"):], dd[key]))
    print("PROBE_C2_R51: clauses=abcd clauses_met=%d admitted=%d/1 verdict=%s rev=%s"
          % (met, admitted, verdict, args.rev))
    if args.json:
        print("PROBE_C2_R51-JSON: " + json.dumps({
            "rev": args.rev, "clauses": {"a": a, "b": b, "c": c, "d": d},
            "detail": {"a": da, "b": db, "c": dc, "d": dd},
            "verdict": verdict, "admitted": admitted}, sort_keys=True))
    return 0 if admitted else 1


if __name__ == "__main__":
    sys.exit(main())
