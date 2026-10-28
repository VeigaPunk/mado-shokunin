#!/usr/bin/env python3
"""Seat-written C1 checker, built from registration.md §C1 + claims-frozen PRED-C1-r55 text.
NOT the wave's quality/counters/c1-r55-kbd-entry.py. Reads git objects only.
--strict-cells  : split on every '|' and require 7 cells (registration: 'no | inside a cell').
default         : --tolerant pipes: a row is `| ID | prop | src | pin:line | `quote` |`, quote = text between the last
                  backtick pair, so a quote containing '||' parses. Reported separately so both readings are visible."""
import argparse, hashlib, json, re, subprocess, sys

ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
TABLES_SHA = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"  # freeze-verify.py output
PIN_DIR = ".ufo/waves/round-55/fetch"
COMMIT = "efb50993780079460b0cbed1363e2166a2de1d9f"
NEW_OPENED = "2026-10-28"
ROW_RE = re.compile(r"^\| (\S+) \| (.*?) \| (\S+) \| (\S+:\d+) \| `(.*)` \|\s*$")


def git_blob(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "cat-file", "-p", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def sha(b):
    return hashlib.sha256(b).hexdigest()


def registry(text):
    reg = {}
    for line in text.split("\n"):
        if line.startswith("| S"):
            c = line.split("|")
            if len(c) >= 12:
                reg[c[1].strip()] = c
    return reg


def parse_row(line, strict):
    """Return (id, cells7) in the 7-slot shape ['', id, prop, src, anchor, '`quote`', ''] or None."""
    if not line.startswith("|"):
        return None
    if strict:
        c = line.split("|")
        return (c[1].strip(), c) if len(c) == 7 else (c[1].strip() if len(c) > 1 else None, c)
    m = ROW_RE.match(line)
    if not m:
        c = line.split("|")
        return (c[1].strip() if len(c) > 1 else None, c)
    rid, prop, src, anchor, quote = m.groups()
    return rid, ["", rid, prop, src, anchor, f"`{quote}`", ""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--strict-cells", action="store_true")
    a = ap.parse_args()
    missed = []

    tb = git_blob(a.repo, a.rev, TABLES)
    if tb is None:
        print("MADO_KBD_ENTRY: SETUP no frozen tables")
        sys.exit(2)
    if sha(tb) != TABLES_SHA:
        missed.append("tables_sha")
    T = json.loads(tb)["c1"]

    pins = {}
    for pin, h in T["pin_sha256"].items():
        b = git_blob(a.repo, a.rev, f"{PIN_DIR}/{pin}")
        pins[pin] = b
        if b is None or sha(b) != h:
            missed.append("pin_hash")

    reg = registry((git_blob(a.repo, a.rev, SOURCES) or b"").decode("utf-8", "replace"))

    ent = git_blob(a.repo, a.rev, ENTRY)
    if ent is None:
        missed.append("entry_absent")
        ent_lines = []
    else:
        ent_lines = ent.decode("utf-8", "replace").split("\n")

    src_line = next((l for l in ent_lines if l.startswith("source:")), "")
    trio = all(any(l.startswith(k + ":") for l in ent_lines) for k in ("source", "verified-at", "recheck"))
    if not (trio and re.search(r"S\d{3}", src_line)):
        missed.append("provenance")

    rd = (git_blob(a.repo, a.rev, README) or b"").decode("utf-8", "replace").split("\n")
    if sum(1 for l in rd if l.startswith("| `knowledge/hyprland-keyboard-repeat-numlock-r55.md`")) != 1:
        missed.append("index")

    by_id = {}
    for l in ent_lines:
        p = parse_row(l, a.strict_cells)
        if p and p[0]:
            by_id.setdefault(p[0], []).append(p[1])

    new_suffixes = {T["source_suffix"][p] for p in T["new_row_pins"]}
    rows_ok, hosts_ok, src_ok = 0, 0, 0
    for f in T["k"] + T["h"]:
        rid, pin, line, quote = f["id"], f["pin"], f["line"], f["quote"]
        cands = by_id.get(rid, [])
        if len(cands) != 1 or len(cands[0]) != 7:
            missed.append(f"row:{rid}")
            continue
        c = cands[0]
        pb = pins.get(pin) or b""
        plines = pb.decode("utf-8", "replace").split("\n")
        pl = plines[line - 1] if 0 < line <= len(plines) else ""
        anchor_ok = c[4].strip() == f"{pin}:{line}"
        qcell = c[5].strip()
        quote_ok = qcell.startswith("`") and qcell.endswith("`") and qcell[1:-1] == quote and quote in pl
        if not anchor_ok:
            missed.append(f"anchor:{rid}")
        if not quote_ok:
            missed.append(f"quote:{rid}")
        if f in T["k"]:
            sid = c[3].strip()
            r = reg.get(sid)
            ok = False
            if r is not None:
                m = re.search(r"https://\S+", r[2])
                url = m.group(0) if m else ""
                ok = url.endswith(T["source_suffix"][pin]) and COMMIT in url and r[8].strip() == "mined"
            if not ok:
                missed.append(f"source_cell:{rid}")
            src_ok += ok
            rows_ok += anchor_ok and quote_ok
        else:
            cellq = qcell[1:-1] if qcell.startswith("`") and qcell.endswith("`") else None
            host_ok = cellq is not None and cellq in pl
            if not host_ok:
                missed.append(f"host:{rid}")
            hosts_ok += host_ok and quote_ok

    new_ok = 0
    for c in reg.values():
        m = re.search(r"https://\S+", c[2])
        url = m.group(0) if m else ""
        if (c[9].strip() == NEW_OPENED and c[4].strip() == "A" and c[8].strip() == "mined"
                and any(url.endswith(s) for s in new_suffixes) and ENTRY in c[11]):
            new_ok += 1
    if new_ok < T["new_rows_min"]:
        missed.append("new_rows")

    legs = list(dict.fromkeys(missed))
    verdict = "TARGET_MET" if not legs else "TARGET_MISSED"
    print(f"MADO_KBD_ENTRY: rev={a.rev} rows={rows_ok}/18 hosts={hosts_ok}/6 sources={src_ok}/18 "
          f"new_rows={min(new_ok, 3)}/3 verdict={verdict} missed={','.join(legs) if legs else 'none'}")
    sys.exit(0 if verdict == "TARGET_MET" else 1)


if __name__ == "__main__":
    main()
