#!/usr/bin/env python3
# R55ScribeEntryC verifier: checks every quote of the draft against its pin line (bytes), every pin sha256,
# the provenance trio, row ids, anchors, S-id bindings and proposition length/tags. Independent of gen_entry.py:
# expected S-ids come from the registration text, not from the generator.
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
W = LANE / ".ufo/waves/round-55"
FETCH = W / "fetch"
SOURCES = LANE / "corpus/SOURCES.md"
HERE = Path(__file__).resolve().parent

T = json.loads((W / "frozen-tables.json").read_text(encoding="utf-8"))
C1 = T["c1"]
COMMIT = C1["commit"]
SUFFIX = C1["source_suffix"]

# Registration §C1 wording: existing rows and new rows per K row.
EXPECT_SID = {}
for k in ["K01", "K02", "K03", "K04", "K05", "K06", "K07"]:
    EXPECT_SID[k] = "S316"
for k in ["K08", "K09"]:
    EXPECT_SID[k] = "S319"
EXPECT_SID["K10"] = "S378"
EXPECT_SID["K11"] = "S379"
EXPECT_SID["K12"] = "S379"
for k in ["K13", "K14", "K15"]:
    EXPECT_SID[k] = "S318"
EXPECT_SID["K16"] = "S317"
EXPECT_SID["K17"] = "S052"
EXPECT_SID["K18"] = "S380"
NEW_ROW_URL_FILE = {"S378": "Hyprland-SeatManager.cpp", "S379": "Hyprland-protocols-core-Seat.cpp", "S380": "Hyprland-IKeyboard.hpp"}
E_SIDS = {"S052", "S316", "S317", "S318", "S319", "S378", "S379", "S380"}
TAGS = ("HELD", "INFERENCE", "UNKNOWN")


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin_bytes_line(name, line_no):
    data = (FETCH / name).read_bytes().split(b"\n")
    if line_no < 1 or line_no > len(data):
        return None
    return data[line_no - 1]


def registry_url(sid):
    if not SOURCES.exists():
        return None
    for l in SOURCES.read_text(encoding="utf-8").split("\n"):
        if l.startswith(f"| {sid} |"):
            m = re.search(r"https://\S+", l)
            return m.group(0) if m else None
    return None


def parse_rows(text):
    rx = re.compile(r"^\| (K\d\d|H\d\d|E\d\d) \| (.*?) \| (\S+) \| (\S+:\d+) \| `(.*)` \|$")
    rows = []
    for n, line in enumerate(text.split("\n"), 1):
        if not re.match(r"^\| (K\d\d|H\d\d|E\d\d) \|", line):
            continue
        m = rx.match(line)
        if not m or "|" in m.group(2):
            rows.append((n, None, line))
            continue
        rows.append((n, [m.group(1), m.group(2), m.group(3), m.group(4), "`" + m.group(5) + "`"], line))
    return rows


def check(text, log):
    fails = []  # (leg, detail)
    lines = text.split("\n")
    # provenance trio
    trio_ok = (
        len(lines) >= 3
        and lines[0].startswith("source:")
        and re.search(r"\bS\d{3}\b", lines[0]) is not None
        and lines[1] == "verified-at: 2026-10-28"
        and lines[2].startswith("recheck:")
    )
    if not trio_ok:
        fails.append(("provenance", "trio missing or out of order"))
    rows = parse_rows(text)
    ids = [c[0] for _, c, _ in rows if c]
    bad_shape = [r for r in rows if r[1] is None or len(r[1]) != 5]
    for n, _, line in bad_shape:
        fails.append(("row_shape", f"line {n}: not five cells"))
    seen = {}
    for n, cells, _ in rows:
        if cells and len(cells) == 5:
            seen.setdefault(cells[0], []).append(n)
    k_ok = h_ok = 0
    # K rows
    for i in range(1, 19):
        rid = f"K{i:02d}"
        if rid not in seen:
            fails.append((f"row:{rid}", "row missing"))
            continue
        if len(seen[rid]) != 1:
            fails.append((f"row:{rid}", f"duplicated at lines {seen[rid]}"))
            continue
        row = next(c for _, c, _ in rows if c and c[0] == rid)
        fr = next(x for x in C1["k"] if x["id"] == rid)
        quote = fr["quote"]
        prop = row[1]
        src = row[2]
        anchor = row[3]
        qcell = row[4]
        ok = True
        if src != EXPECT_SID[rid]:
            fails.append((f"source_cell:{rid}", f"S-id {src} != {EXPECT_SID[rid]}"))
            ok = False
        if anchor != f"{fr['pin']}:{fr['line']}":
            fails.append((f"anchor:{rid}", f"anchor {anchor!r} != {fr['pin']}:{fr['line']}"))
            ok = False
        if qcell != f"`{quote}`":
            fails.append((f"quote:{rid}", f"quote cell != frozen"))
            ok = False
        pl = pin_bytes_line(fr["pin"], fr["line"])
        if pl is None or quote.encode() not in pl:
            fails.append((f"quote:{rid}", "frozen quote not a substring of the pin line"))
            ok = False
        if len(prop) < 40:
            fails.append(("prop", f"{rid} proposition {len(prop)} chars < 40"))
            ok = False
        if not prop.startswith(tuple(t + ":" for t in TAGS) + ("HELD (",)):
            fails.append(("prop", f"{rid} proposition lacks a HELD/INFERENCE/UNKNOWN tag"))
            ok = False
        k_ok += ok
    # H rows
    for i in range(1, 7):
        rid = f"H{i:02d}"
        if rid not in seen or len(seen[rid]) != 1:
            fails.append((f"row:{rid}", "row missing or duplicated"))
            continue
        row = next(c for _, c, _ in rows if c and c[0] == rid)
        fr = next(x for x in C1["h"] if x["id"] == rid)
        ok = True
        if row[2] != "host":
            fails.append((f"source_cell:{rid}", f"source cell {row[2]!r} != host"))
            ok = False
        if row[3] != f"{fr['pin']}:{fr['line']}":
            fails.append((f"anchor:{rid}", f"anchor {row[3]!r} != {fr['pin']}:{fr['line']}"))
            ok = False
        if row[4] != f"`{fr['quote']}`":
            fails.append((f"quote:{rid}", "quote cell != frozen"))
            ok = False
        pl = pin_bytes_line(fr["pin"], fr["line"])
        if pl is None or row[4][1:-1].encode() not in pl:
            fails.append((f"host:{rid}", "quote not a substring of the host pin line"))
            ok = False
        if len(row[1]) < 20:
            fails.append(("prop", f"{rid} proposition too short"))
            ok = False
        if not row[1].startswith(tuple(t for t in ("HELD",))):
            fails.append(("prop", f"{rid} proposition lacks HELD tag"))
            ok = False
        h_ok += ok
    # E rows (counter ignores; still checked)
    e_ok = e_total = 0
    for n, cells, _ in rows:
        if not cells or not cells[0].startswith("E"):
            continue
        e_total += 1
        ok = True
        if len(cells) != 5:
            ok = False
            fails.append((f"extra:{cells[0]}", "not five cells"))
            continue
        rid, prop, sid, anchor, qcell = cells
        if sid not in E_SIDS:
            fails.append((f"extra:{rid}", f"S-id {sid} not an allowed source"))
            ok = False
        m = re.match(r"^(.+):(\d+)$", anchor)
        if not m:
            fails.append((f"extra:{rid}", "anchor is not pin:line"))
            continue
        pin, line = m.group(1), int(m.group(2))
        if not (FETCH / pin).exists():
            fails.append((f"extra:{rid}", f"pin {pin} missing under fetch/"))
            ok = False
        if not qcell.startswith("`") or not qcell.endswith("`"):
            fails.append((f"extra:{rid}", "quote cell not backticked"))
            ok = False
            e_ok += ok
            continue
        q = qcell[1:-1]
        pl = pin_bytes_line(pin, line) if (FETCH / pin).exists() else None
        if pl is None or q.encode() not in pl:
            fails.append((f"extra:{rid}", f"quote not in {pin}:{line}"))
            ok = False
        if not prop.startswith(("HELD", "INFERENCE", "UNKNOWN")):
            fails.append((f"extra:{rid}", "proposition lacks a tag"))
            ok = False
        e_ok += ok
    # pins (sha256 vs frozen map and SHA256SUMS)
    pin_status = []
    sums = {}
    for l in (FETCH / "SHA256SUMS.txt").read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^([0-9a-f]{64})\s+(\S+)$", l.strip())
        if m:
            sums[m.group(2)] = m.group(1)
    for name, expect in C1["pin_sha256"].items():
        got = sha_file(FETCH / name)
        pin_status.append((name, got == expect, got))
        if got != expect:
            fails.append(("pin_hash", f"{name} sha256 {got} != {expect}"))
    for name in ("host-input.conf", "host-getoption.json"):
        if name in sums and sha_file(FETCH / name) != sums[name]:
            fails.append(("pin_hash", f"{name} differs from SHA256SUMS.txt"))
    # registry binding (S-ids for K rows): base rows must name pin suffix and frozen commit (literal registration leg)
    reg = []
    for sid, pin in [("S316", "Hyprland-InputManager.cpp"), ("S318", "Hyprland-ConfigValues.cpp"), ("S319", "Hyprland-IKeyboard.cpp"),
                     ("S317", "Hyprland-legacy-ConfigManager.cpp"), ("S052", "wayland-1.26.0-wayland.xml")]:
        url = registry_url(sid)
        if url is None:
            reg.append((sid, "absent-from-SOURCES.md"))
            continue
        suf_ok = url.endswith(SUFFIX[pin]) if pin in SUFFIX else url.endswith("1.26.0/protocol/wayland.xml")
        commit_ok = COMMIT in url
        reg.append((sid, f"suffix={'ok' if suf_ok else 'BAD'} commit={'ok' if commit_ok else 'absent'} url={url}"))
        if sid == "S052":
            if not commit_ok:
                fails.append(("source_cell:K17", "literal registration leg: S052 URL lacks the frozen commit efb50993 (wayland tag 1.26.0 is not that commit)"))
        elif not (suf_ok and commit_ok):
            fails.append(("source_cell", f"{sid} URL does not match suffix and commit"))
    for sid, pin in NEW_ROW_URL_FILE.items():
        expect_url = f"https://raw.githubusercontent.com/hyprwm/Hyprland/{COMMIT}/{SUFFIX[pin]}"
        reg.append((sid, f"PENDING-INTEGRATION constructed={expect_url}"))
    log.append(f"trio={'ok' if trio_ok else 'bad'} ids_seen={len(ids)}")
    return fails, k_ok, h_ok, e_ok, e_total, pin_status, reg


def mutate(text, kind):
    if kind == "C1-CTL-2 spliced-quote":
        return text.replace("`std::max(0, REPEATRATE);`", "`std::max(0, REPEATRATE) ;`", 1)
    if kind == "C1-CTL-3 shifted-anchor":
        return re.sub(r"(\| K01 \|.*?)Hyprland-InputManager\.cpp:1220", r"\1Hyprland-InputManager.cpp:1219", text, count=1)
    if kind == "C1-CTL-4 wrong-source":
        return re.sub(r"(\| K10 \| [^|]*\| )S378( \|)", r"\1S316\2", text, count=1)
    if kind == "C1-CTL-5 dropped-row":
        return "\n".join(l for l in text.split("\n") if not l.startswith("| K17 |"))
    if kind == "C1-CTL-6 host-forged":
        return text.replace("`repeat_delay = 250`", "`repeat_delay = 300`", 1)
    raise SystemExit(f"unknown mutation {kind}")


EXPECT_LEG = {
    "C1-CTL-2 spliced-quote": "quote:K04",
    "C1-CTL-3 shifted-anchor": "anchor:K01",
    "C1-CTL-4 wrong-source": "source_cell:K10",
    "C1-CTL-5 dropped-row": "row:K17",
    "C1-CTL-6 host-forged": "host:H02",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry", default=str(HERE / "entry.md"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    print(f"frozen-tables.json sha256={sha_file(W / 'frozen-tables.json')}")
    text = Path(a.entry).read_text(encoding="utf-8")
    print(f"entry={a.entry} sha256={sha_file(a.entry)} bytes={len(text.encode())}")
    log = []
    fails, k_ok, h_ok, e_ok, e_total, pin_status, reg = check(text, log)
    print("PINS:")
    for name, ok, got in pin_status:
        print(f"  {name} {'ok' if ok else 'BAD'} {got}")
    print("REGISTRY:")
    for sid, d in reg:
        print(f"  {sid} {d}")
    print("ROWS:", log[0])
    print(f"  K quotes+anchors+sources+props ok: {k_ok}/18")
    print(f"  H ok: {h_ok}/6")
    print(f"  E ok: {e_ok}/{e_total} (extra rows; counter ignores)")
    if fails:
        print("FAILS:")
        for leg, d in fails:
            print(f"  {leg}: {d}")
    else:
        print("FAILS: none")
    verdict = "OK" if not fails else "FAIL"
    print(f"VERIFY_ENTRY: rows_K={k_ok}/18 rows_H={h_ok}/6 extra={e_ok}/{e_total} pins={'ok' if all(s for _, s, _ in pin_status) else 'bad'} fails={len(fails)} verdict={verdict}")
    if a.selftest:
        print("SELFTEST (mutants of the draft must each produce their named leg):")
        base_fails, *_ = check(text, [])
        print(f"  unmutated fails={len(base_fails)}")
        all_ok = True
        for kind, want in EXPECT_LEG.items():
            m_fails, *_ = check(mutate(text, kind), [])
            legs = [leg for leg, _ in m_fails]
            hit = want in legs
            all_ok &= hit
            print(f"  {kind}: expected {want} -> {'caught' if hit else 'MISSED'} legs={sorted(set(legs))}")
        print(f"SELFTEST_RESULT {'ok' if all_ok else 'FAIL'}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
