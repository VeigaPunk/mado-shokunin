#!/usr/bin/env python3
"""Attack-seat checker for PRED-C1-r55 as frozen (registration.md §C1).

NOT the wave counter. An independent re-implementation of the frozen legs, written from the
contract text, reading only git objects at --rev.
  default            literal grammar: a `|` inside a cell splits it (registration: "no `|` inside a cell")
  --escaped-pipes    GFM reading: `\\|` inside a cell is a literal pipe (needed for frozen quote K16)
  --propose-clause   adds ONE non-frozen clause (C1-X, attack.md §5) as a `C1X:` line; never changes verdict
Output: one frozen-grammar line `MADO_KBD_ENTRY: ...` plus `# ` detail lines.
"""
import argparse, hashlib, json, os, re, subprocess, sys, difflib

ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
# sha256 of frozen-tables.json at freeze commit 54dacbd8 (embedded constant, registration §C1)
EMBEDDED_TABLES_SHA = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"
ID_RE = re.compile(r"[KH]\d{2}")
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")


def blob(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "cat-file", "blob", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def split_cells(line, escaped):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    parts = re.split(r"(?<!\\)\|", s) if escaped else s.split("|")
    return [(p.strip().replace("\\|", "|") if escaped else p.strip()) for p in parts]


def registry(repo, rev):
    txt = (blob(repo, rev, SOURCES) or b"").decode("utf-8", "replace")
    rows = {}
    for line in txt.split("\n"):
        if not line.startswith("| S"):
            continue
        cells = split_cells(line, escaped=False)
        if len(cells) < 11:
            continue
        rows.setdefault(cells[0], []).append(cells)
    return rows


def url_of(cell):
    m = re.search(r"https://\S+", cell)
    return m.group(0) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--escaped-pipes", action="store_true")
    ap.add_argument("--propose-clause", action="store_true")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.work, "c1-attack"), exist_ok=True)

    tb = blob(a.repo, a.rev, TABLES)
    if tb is None:
        print("setup: frozen-tables.json missing at rev", file=sys.stderr)
        return 2
    tables_ok = hashlib.sha256(tb).hexdigest() == EMBEDDED_TABLES_SHA
    T = json.loads(tb)["c1"]

    pin_lines, pin_ok = {}, {}
    for name, want in T["pin_sha256"].items():
        data = blob(a.repo, a.rev, f"{T['pin_dir']}/{name}")
        pin_ok[name] = data is not None and hashlib.sha256(data).hexdigest() == want
        pin_lines[name] = (data or b"").decode("utf-8", "replace").split("\n")
    pins_all_ok = all(pin_ok.values())

    reg = registry(a.repo, a.rev)

    def src_ok(sid, pin):
        rs = reg.get(sid, [])
        if len(rs) != 1:
            return False
        c = rs[0]
        u = url_of(c[1])
        return u.endswith(T["source_suffix"][pin]) and T["commit"] in u and c[7] == "mined"

    newsuf = [T["source_suffix"][p] for p in T["new_row_pins"]]
    new_count = 0
    for rs in reg.values():
        for c in rs:
            u = url_of(c[1])
            if (c[8] == "2026-10-28" and c[3] == "A" and c[7] == "mined"
                    and any(u.endswith(s) for s in newsuf) and ENTRY in c[10]):
                new_count += 1

    entry_blob = blob(a.repo, a.rev, ENTRY)
    readme = (blob(a.repo, a.rev, README) or b"").decode("utf-8", "replace").split("\n")
    missed, detail = [], []

    def miss(leg):
        if leg not in missed:
            missed.append(leg)

    if not tables_ok:
        miss("tables_sha")
    if not pins_all_ok:
        miss("pin_hash")
    if new_count < T["new_rows_min"]:
        miss("new_rows")

    rows_k = hosts_h = sources_k = 0
    if entry_blob is None:
        miss("entry_absent")
    else:
        el = entry_blob.decode("utf-8", "replace").split("\n")
        prov_ok = (any(l.startswith("source:") and re.search(r"S\d{3}", l) for l in el)
                   and any(l.startswith("verified-at: 2026-10-28") for l in el)
                   and any(l.startswith("recheck:") for l in el))
        if not prov_ok:
            miss("provenance")
        index_n = sum(1 for l in readme if l.startswith("| `knowledge/hyprland-keyboard-repeat-numlock-r55.md`"))
        if index_n != 1:
            miss("index")
        byid = {}
        for l in el:
            if not l.startswith("|"):
                continue
            cells = split_cells(l, escaped=a.escaped_pipes)
            if cells and ID_RE.fullmatch(cells[0]):
                byid.setdefault(cells[0], []).append(cells)
        for kind, frozen in (("K", T["k"]), ("H", T["h"])):
            for f in frozen:
                rid, pin = f["id"], f["pin"]
                rs = byid.get(rid, [])
                if len(rs) != 1 or len(rs[0]) != 5:
                    miss(f"row:{rid}")
                    detail.append(f"{rid}: row missing, duplicated or cell count != 5 (cells={[len(x) for x in rs]})")
                    continue
                c = rs[0]
                minlen = 40 if kind == "K" else 20
                if len(c[1]) < minlen:
                    miss(f"row:{rid}")
                    detail.append(f"{rid}: proposition {len(c[1])} chars < {minlen}")
                    continue
                anchor_ok = c[3] == f"{pin}:{f['line']}"
                if not anchor_ok:
                    miss(f"anchor:{rid}")
                q = c[4]
                quote_cell_ok = q.startswith("`") and q.endswith("`") and q[1:-1] == f["quote"]
                pl = pin_lines.get(pin, [])
                line_txt = pl[f["line"] - 1] if 0 < f["line"] <= len(pl) else ""
                quote_in_pin = f["quote"] in line_txt
                if not quote_cell_ok or not quote_in_pin:
                    miss(f"quote:{rid}" if kind == "K" else f"host:{rid}")
                    detail.append(f"{rid}: quote_cell_ok={quote_cell_ok} quote_in_pin={quote_in_pin}")
                if kind == "K":
                    if src_ok(c[2], pin):
                        sources_k += 1
                    else:
                        miss(f"source_cell:{rid}")
                        detail.append(f"{rid}: source cell {c[2]!r} is not a mined registry row whose URL ends "
                                      f"{T['source_suffix'][pin]!r} and contains {T['commit'][:8]}")
                    if anchor_ok and quote_cell_ok and quote_in_pin:
                        rows_k += 1
                elif anchor_ok and quote_cell_ok and quote_in_pin:
                    hosts_h += 1
        if a.propose_clause:
            props, bad = [], []
            for rid, cs in byid.items():
                if len(cs) == 1 and len(cs[0]) == 5:
                    frozen = next(x for x in (T["k"] + T["h"]) if x["id"] == rid)
                    qtok = set(TOKEN_RE.findall(frozen["quote"]))
                    ptok = {t for t in qtok if re.search(r"\b" + re.escape(t) + r"\b", cs[0][1])}
                    if len(ptok) < min(2, len(qtok)):
                        bad.append(rid)
                    props.append((rid, cs[0][1]))
            for i in range(len(props)):
                for j in range(i + 1, len(props)):
                    if difflib.SequenceMatcher(None, props[i][1], props[j][1]).ratio() >= 0.6:
                        for rid in (props[i][0], props[j][0]):
                            if rid not in bad:
                                bad.append(rid)
            print(f"C1X: {'ok' if not bad else 'bad'} failing={','.join(sorted(bad)) or 'none'} "
                  f"(NOT frozen; attack.md section 5)")

    verdict = "TARGET_MET" if not missed else "TARGET_MISSED"
    print(f"MADO_KBD_ENTRY: rev={a.rev} rows={rows_k}/18 hosts={hosts_h}/6 sources={sources_k}/18 "
          f"new_rows={min(new_count, 3)}/3 verdict={verdict} missed={','.join(missed) if missed else 'none'}")
    for d in detail:
        print("# " + d)
    return 0 if verdict == "TARGET_MET" else 1


if __name__ == "__main__":
    sys.exit(main())
