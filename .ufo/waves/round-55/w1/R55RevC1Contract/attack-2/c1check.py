#!/usr/bin/env python3
"""Seat R55RevC1Contract's OWN minimal checker for the C1 grammar in registration.md §C1 (not the frozen counter).

Reads only git objects at --rev of --repo. Embeds the frozen-tables sha256 of the freeze commit (tables_sha leg).
--cells strict  : a cell is split on every '|' (the frozen grammar, "no | inside a cell"). Default.
--cells gfm     : a cell may hold '\\|' (GFM escape); the escape is undone before comparison. Seat-chosen reading,
                  needed only because frozen K16's quote contains '||'. Reported separately.
--propose overlap adds a PROPOSED leg on a second line; it is not the predicate.
"""
import argparse, hashlib, json, re, subprocess, sys

EMBEDDED_TABLES_SHA = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
ENTRY_README = "knowledge/hyprland-keyboard-repeat-numlock-r55.md"
W = ".ufo/waves/round-55"
TABLES = f"{W}/frozen-tables.json"
PIN_DIR = f"{W}/fetch"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
DATE = "2026-10-28"


def blob(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cells_of(line, gfm=False):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    if not gfm:
        return [c.strip() for c in s.split("|")]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def check(repo, rev, cells_mode="strict", propose=None):
    gfm = cells_mode == "gfm"
    legs = []
    tables_raw = blob(repo, rev, TABLES)
    if tables_raw is None:
        return None, "MADO_KBD_ENTRY: SETUP tables-missing", []
    if sha(tables_raw) != EMBEDDED_TABLES_SHA:
        legs.append("tables_sha")
    T = json.loads(tables_raw)
    c1 = T["c1"]
    commit = c1["commit"]

    entry_raw = blob(repo, rev, ENTRY)
    if entry_raw is None:
        legs.append("entry_absent")
        entry = ""
    else:
        entry = entry_raw.decode("utf-8")
    lines = entry.split("\n")

    head = []
    for l in lines:
        if l.startswith("|"):
            break
        head.append(l)
    src = [l for l in head if l.startswith("source:")]
    s_ids = re.findall(r"S\d{3}", src[0]) if src else []
    if not (src and s_ids and any(l.strip() == f"verified-at: {DATE}" for l in head)
            and any(l.startswith("recheck:") for l in head)):
        legs.append("provenance")

    readme = (blob(repo, rev, README) or b"").decode("utf-8")
    if sum(1 for l in readme.split("\n") if f"| `{ENTRY_README}`" in l) != 1:
        legs.append("index")

    for pin, want in c1["pin_sha256"].items():
        data = blob(repo, rev, f"{PIN_DIR}/{pin}")
        if data is None or sha(data) != want:
            legs.append("pin_hash")
            break

    reg = {}
    for l in (blob(repo, rev, SOURCES) or b"").decode("utf-8").split("\n"):
        if l.startswith("| S"):
            c = cells_of(l)
            if len(c) == 11:
                reg[c[0]] = c

    def url_of(c):
        m = re.search(r"https://\S+", c[1])
        return m.group(0) if m else ""

    rows = {}
    for l in lines:
        if l.startswith("|"):
            c = cells_of(l, gfm)
            if c and re.fullmatch(r"[KH]\d\d", c[0]):
                rows.setdefault(c[0], []).append(c)

    a_ok = b_ok = c_ok = 0
    overlap_missed = []
    for items, minlen, kind in ((c1["k"], 40, "K"), (c1["h"], 20, "H")):
        for it in items:
            rid, pin, line, fq = it["id"], it["pin"], it["line"], it["quote"]
            got = rows.get(rid, [])
            if len(got) != 1 or len(got[0]) != 5 or len(got[0][1]) < minlen:
                legs.append(f"row:{rid}")
                continue
            c = got[0]
            prop, s_or_host, anc, qc = c[1], c[2], c[3], c[4]
            row_ok = True
            if anc != f"{pin}:{line}":
                legs.append(f"anchor:{rid}"); row_ok = False
            qcell = qc[1:-1] if len(qc) >= 2 and qc[0] == "`" and qc[-1] == "`" else None
            pb = blob(repo, rev, f"{PIN_DIR}/{pin}")
            plines = pb.decode("utf-8").split("\n") if pb is not None else []
            pline = plines[line - 1] if 0 < line <= len(plines) else ""
            if qcell != fq or fq not in pline:
                legs.append(f"quote:{rid}"); row_ok = False
            if kind == "H":
                if qcell is None or qcell not in pline:
                    legs.append(f"host:{rid}"); row_ok = False
                elif row_ok:
                    b_ok += 1
            else:
                suffix = c1["source_suffix"][pin]
                r = reg.get(s_or_host)
                if not (r is not None and url_of(r).endswith(suffix) and commit in url_of(r) and r[7] == "mined"):
                    legs.append(f"source_cell:{rid}")
                else:
                    c_ok += 1
                if row_ok:
                    a_ok += 1
            if propose == "overlap" and row_ok:
                words = {w.lower() for w in re.findall(r"\w+", qcell or "") if len(w) >= 6}
                if not any(w in prop.lower() for w in words):
                    overlap_missed.append(rid)

    newsfx = tuple(c1["source_suffix"][p] for p in c1["new_row_pins"])
    m = sum(1 for sid, r in reg.items()
            if r[8] == c1["opened"] and r[3] == "A" and r[7] == "mined"
            and url_of(r).endswith(newsfx) and ENTRY in r[10])
    if m < c1["new_rows_min"]:
        legs.append("new_rows")

    legs = list(dict.fromkeys(legs))
    verdict = "TARGET_MET" if not legs else "TARGET_MISSED"
    line1 = (f"MADO_KBD_ENTRY: rev={rev} rows={a_ok}/18 hosts={b_ok}/6 sources={c_ok}/18 "
             f"new_rows={m}/{c1['new_rows_min']} verdict={verdict} missed={','.join(legs) if legs else 'none'}")
    extra = []
    if propose == "overlap":
        extra.append(f"PROPOSAL_ONLY prop_overlap missed={','.join(overlap_missed) if overlap_missed else 'none'}")
    return (0 if verdict == "TARGET_MET" else 1), line1, extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--cells", choices=["strict", "gfm"], default="strict")
    ap.add_argument("--propose", choices=["overlap"], default=None)
    a = ap.parse_args()
    rc, line1, extra = check(a.repo, a.rev, a.cells, a.propose)
    print(line1)
    for e in extra:
        print(e)
    if rc is None:
        sys.exit(2)
    sys.exit(rc)


if __name__ == "__main__":
    main()
