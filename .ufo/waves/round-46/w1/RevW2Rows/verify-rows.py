#!/usr/bin/env python3
"""RevW2Rows verifier: rows S302-S315 of corpus/SOURCES.md vs today's re-fetch.

Checks per row:
  1. sha256 of today's fetch == row's sha256 cell == .ufo/waves/round-45/receipts/fetch-sha256.txt
  2. round-45.md Gate quote found (whitespace-normalized) in the receipt at/inside the row's anchor range
  3. anchor range tokens exist and their labels appear in range
  4. dumps the anchor windows + teaches-keyword hits for manual judgment -> w2-windows.txt
"""
import hashlib, json, re, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SEAT = LANE / ".ufo/waves/round-46/w1/RevW2Rows"
FETCH = Path("/fast/scratch/hyaku/mado-r46/RevW2Rows/fetch")
R45_FETCH = LANE / ".ufo/waves/round-45/fetch"
R45_SHA = LANE / ".ufo/waves/round-45/receipts/fetch-sha256.txt"
SOURCES = LANE / "corpus/SOURCES.md"
LESSON = LANE / "corpus/lessons/round-45.md"

ROWS = [("S%03d" % n, 251 + (n - 302)) for n in range(302, 316)]

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def main() -> None:
    src_lines = SOURCES.read_text().splitlines()
    lesson = LESSON.read_text()

    # Gate quotes
    gates = {}
    for m in re.finditer(r'^GATE (S\d+) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.*)"\s*$', lesson, re.M):
        gates[m.group(1)] = {"receipt": m.group(2), "sha256": m.group(3), "quote": m.group(4)}

    # round-45 receipt hashes
    r45sha = {}
    for ln in R45_SHA.read_text().splitlines():
        if ln.strip():
            h, name = ln.split(None, 1)
            r45sha[Path(name.strip()).name] = h

    out = []
    windows = []
    for rid, lineno in ROWS:
        row = src_lines[lineno - 1]
        assert row.startswith("| %s |" % rid), (rid, row[:40])
        cells = row.split(" | ")
        mh = re.search(r"sha256:([0-9a-f]{64})", row)
        row_sha = mh.group(1) if mh else None
        anchor_cell = cells[5]
        teaches = cells[6]
        tokens = []
        for m in re.finditer(r"([A-Za-z0-9_.-]+?):(\d+)(?:-(\d+))?", anchor_cell):
            t = m.group(1)
            if re.search(r"\.(cpp|hpp|md)$", t):
                tokens.append((t, int(m.group(2)), int(m.group(3) or m.group(2)), m.start(), m.end()))
        receipt_name = tokens[0][0]  # all tokens share the receipt name
        receipt = R45_FETCH / receipt_name
        fresh = FETCH / receipt_name
        rec = {"row": rid, "line": lineno, "receipt": receipt_name}

        # 1. hashes
        fresh_bytes = fresh.read_bytes()
        fresh_sha = hashlib.sha256(fresh_bytes).hexdigest()
        rec["sha_row"] = row_sha
        rec["sha_r45_receipt_file"] = r45sha.get(receipt_name)
        rec["sha_r45_gate"] = gates.get(rid, {}).get("sha256")
        rec["sha_fresh"] = fresh_sha
        rec["bytes_equal_row"] = fresh_sha == row_sha
        rec["bytes_equal_r45_txt"] = fresh_sha == r45sha.get(receipt_name)
        rec["bytes_equal_r45_gate"] = fresh_sha == gates.get(rid, {}).get("sha256")
        rec["bytes_equal_r45_file"] = fresh_bytes == receipt.read_bytes()

        # 2. Gate quote at locator
        g = gates.get(rid)
        if g:
            qlines = receipt.read_text().splitlines()
            # char-offset -> line map over whitespace-normalized text
            offsets = []
            parts = []
            pos = 0
            for i, ln in enumerate(qlines, 1):
                n = norm(ln)
                offsets.append((pos, i))
                parts.append(n)
                pos += len(n) + 1
            hay = " ".join(parts)
            q = norm(g["quote"])
            idx = hay.find(q)
            if idx < 0:
                # fallback: Gate-preamble splices may elide source lines; match both halves
                half = len(q) // 2
                cut = q.rfind(" ", 0, half + 20)
                q1, q2 = q[:cut].strip(), q[cut:].strip()
                i1, i2 = hay.find(q1), hay.find(q2)
                if i1 >= 0 and i2 >= 0 and i2 > i1:
                    def line_at(off: int) -> int:
                        li = 1
                        for off2, l2 in offsets:
                            if off2 <= off:
                                li = l2
                            else:
                                break
                        return li
                    rec["quote_found"] = "splice"
                    rec["quote_line"] = line_at(i1)
                    rec["quote_end_line"] = line_at(i2 + len(q2))
                    rec["quote_in_range"] = any(
                        tname == receipt_name and a - 1 <= rec["quote_line"] <= b
                        for tname, a, b, _s, _e in tokens
                    )
                    qlines_ = qlines
                    windows.append(
                        f"### {rid} SPLICE match parts at lines {rec['quote_line']} and {rec['quote_end_line']} (receipt {receipt_name})\n" +
                        "\n".join(f"{n}: {qlines_[n-1]}" for n in range(max(1, rec['quote_line'] - 2), min(len(qlines_), rec['quote_end_line'] + 2) + 1)))
                    windows[-1] = windows[-1]  # keep order
                else:
                    rec["quote_found"] = False
            else:
                start_line = 1
                for off, li in offsets:
                    if off <= idx:
                        start_line = li
                    else:
                        break
                end_line = start_line
                for off, li in offsets:
                    if off <= idx + len(q):
                        end_line = li
                    else:
                        break
                rec["quote_found"] = True
                rec["quote_line"] = start_line
                rec["quote_end_line"] = end_line
                rec["quote_in_range"] = any(
                    tname == receipt_name and a - 1 <= start_line <= b
                    for tname, a, b, _s, _e in tokens
                )
                windows.append(f"### {rid} quote match lines {start_line}-{end_line} (receipt {receipt_name})\n" +
                               "\n".join(f"{n}: {qlines[n-1]}" for n in range(max(1, start_line - 2), min(len(qlines), end_line + 2) + 1)))

        # 3. anchor tokens
        rec["anchor_tokens"] = []
        t = receipt.read_text().splitlines()
        for tname, a, b, ms, me in tokens:
            ok_bounds = 1 <= a <= b <= len(t)
            nxt = re.search(r"[A-Za-z0-9_.-]+?:\d+(?:-\d+)?", anchor_cell[me:])
            seg = anchor_cell[me: me + nxt.start()] if nxt else anchor_cell[me:]
            seg = seg.split("(receipt")[0]
            idents = re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", seg)
            lo, hi = max(1, a - 2), min(len(t), b + 2)
            window = "\n".join(t[lo - 1: hi])
            found = {i: bool(re.search(r"\b" + re.escape(i) + r"\b", window)) for i in idents}
            rec["anchor_tokens"].append({
                "token": f"{tname}:{a}-{b}", "bounds_ok": ok_bounds,
                "file_lines": len(t), "idents": found,
            })
            windows.append(f"### {rid} anchor {tname}:{a}-{b} idents={found}\n" +
                           "\n".join(f"{n}: {t[n-1]}" for n in range(lo, hi + 1)))

        # 4. teaches windows
        wins = TEACHES.get(rid, [])
        for label, pat, lo, hi in wins:
            lo = max(1, lo or 1)
            hi = min(hi or len(t), len(t))
            hits = [(n, t[n - 1]) for n in range(lo, hi + 1) if re.search(pat, t[n - 1])]
            windows.append(f"### {rid} teaches[{label}] pat={pat!r} range={lo}-{hi} hits={len(hits)}\n" +
                           "\n".join(f"{n}: {l}" for n, l in hits[:40]))

        rec["teaches"] = teaches
        out.append(rec)

    (SEAT / "w2-summary.json").write_text(json.dumps(out, indent=1))
    (SEAT / "w2-windows.txt").write_text("\n\n".join(windows) + "\n")

    for r in out:
        print(r["row"], "bytes:", r["bytes_equal_row"], r["bytes_equal_r45_txt"],
              r["bytes_equal_r45_gate"], r["bytes_equal_r45_file"],
              "quote:", r.get("quote_found"), "line", r.get("quote_line"),
              "in_range:", r.get("quote_in_range"))
        for at in r["anchor_tokens"]:
            miss = [k for k, v in at["idents"].items() if not v]
            print("   ", at["token"], "bounds_ok" if at["bounds_ok"] else "BOUNDS-FAIL", "idents_missing:", miss or "none")

TEACHES = {
    "S302": [
        ("rate-after-@", r"find_first_of\('@'\)", 100, 150),
        ("rate-assign", r"m_refreshRate\s*=", 100, 150),
        ("pos-auto", r"auto", 140, 200),
        ("scale-auto-or-025", r"auto|0\.25", 190, 235),
    ],
    "S303": [
        ("keys-after-scale", r'key == "|case |ARGS\[', 1290, 1390),
        ("reject", r"return|success|error|fail", 1290, 1390),
    ],
    "S304": [
        ("add-erase", r"erase_if|push_back|emplace_back", 30, 50),
        ("get-order", r"for\s*\(|m_name|empty|default", 40, 120),
    ],
    "S305": [
        ("rate60", r"m_refreshRate", 35, 75),
        ("scale-neg1", r"m_scale", 35, 75),
        ("offset-sentinel", r"m_offset|INT_MAX|sentinel|FLT_MAX|100000", 35, 75),
    ],
    "S306": [
        ("deltallessthan-use", r"DELTALESSTHAN", 700, 1090),
        ("scale-120", r"120", 700, 1090),
        ("desc", r"description", 245, 260),
        ("selector", r"matchesStaticSelector", 1195, 1215),
    ],
    "S307": [
        ("json-5dec", r"\.5f|refreshRate", 220, 290),
        ("monitors-req", r"monitors|disabled|\"all\"", 310, 350),
        ("desc-field", r"description", 220, 290),
    ],
    "S308": [
        ("explicit", r"moveTo|POS", 10, 45),
        ("auto-dir", r"auto|direction|arrange", 55, 105),
    ],
    "S309": [
        ("isnumber", r"isNumber", 40, 90),
        ("minus-dot-digit", r"'-'|'\\.'|'-'\|dot|back()", 40, 90),
    ],
    "S310": [
        ("general", r"monitor\s*=|General", 1, 35),
        ("sdr-eotf", r"sdr_eotf", 1, 400),
        ("colour", r"sdr|hdr|colour|color", 230, 270),
        ("monv2", r"monitorv2|Monitor v2|monitor = ", 285, 315),
    ],
    "S311": [
        ("active-list", r"enabled|mirror|monitors\b", 20, 50),
        ("all-lists", r"allMonitors|m_realMonitors", 45, 60),
        ("add", r"emplace_back|push_back|enabled", 105, 130),
    ],
    "S312": [("macro", r"DELTALESSTHAN", 35, 45)],
    "S313": [
        ("fields", r"double", 8, 26),
        ("div", r"operator/", 30, 45),
    ],
    "S314": [
        ("ctor", r"delim|CVarList2|explicit", 5, 22),
        ("empty-kept", r"empty|keep|trim", 5, 40),
    ],
    "S315": [
        ("edid", r"make|model|serial|EDID", 1910, 1945),
        ("desc", r"description|format", 2090, 2110),
    ],
}

if __name__ == "__main__":
    main()
