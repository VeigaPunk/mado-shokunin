#!/usr/bin/env python3
"""R55ScribeEntryB verifier (seat draft, round 55 w1). Not the frozen counter; a seat check of this draft.

Reads committed bytes at --rev with `git -C <lane> show` (the working tree is compared too) and checks:
  - the provenance trio; every K/H/E row's pin, line and quote against the pin line at --rev;
  - every pin's sha256 against frozen-tables.json c1.pin_sha256;
  - every K row's source id against the registry row (URL suffix, freeze commit in the URL, status mined);
  - the three new-row legs (S378-S380) as the registration states them;
  - the frozen controls C1-CTL-2..7 applied as mutants of this draft, so the checks are shown to bite.
Writes only under --work. Exit 0 when the draft at --rev has no missed leg, 1 otherwise, 2 on setup error.
Leg names follow registration §C1: row, anchor, quote, host, source_cell, new_rows, pin_hash, provenance.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

WREL = ".ufo/waves/round-55"
ENTRY_PATH = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
PIN_SID = {
    "Hyprland-InputManager.cpp": "S316",
    "Hyprland-IKeyboard.cpp": "S319",
    "Hyprland-ConfigValues.cpp": "S318",
    "Hyprland-legacy-ConfigManager.cpp": "S317",
    "wayland-1.26.0-wayland.xml": "S052",
    "Hyprland-SeatManager.cpp": "S378",
    "Hyprland-protocols-core-Seat.cpp": "S379",
    "Hyprland-IKeyboard.hpp": "S380",
}
NEW_SIDS = {"S378": "Hyprland-SeatManager.cpp", "S379": "Hyprland-protocols-core-Seat.cpp", "S380": "Hyprland-IKeyboard.hpp"}
ROW_RE = re.compile(r"^\| ([KHE]\d\d) \| (.*) \| (S\d{3}|host) \| ([^|`]+?):(\d+) \| `(.*)` \|$")


def die(msg):
    print(f"VERIFY SETUP_ERROR {msg}")
    sys.exit(2)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_show(lane, rev, rel):
    r = subprocess.run(["git", "-C", lane, "show", f"{rev}:{rel}"], capture_output=True)
    if r.returncode != 0:
        die(f"git show {rev}:{rel} failed: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout


def parse_registry(text):
    reg = {}
    for line in text.decode("utf-8", "replace").split("\n"):
        if line.startswith("| S"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 12:
                reg[parts[1]] = parts
    return reg


def registry_url(parts):
    m = re.search(r"https://\S+", parts[2])
    return m.group(0) if m else ""


def synthetic_rows(reg, table):
    """Rows as registration §C1 says the L1 writes them (round 55, opened 2026-10-28, tier A, kind code, mined).
    Scratch only: the registry at --rev is never written."""
    out = dict(reg)
    for sid, pin in NEW_SIDS.items():
        url = f"https://raw.githubusercontent.com/hyprwm/Hyprland/{table['__commit__']}/{table['__suffix__'][pin]}"
        out[sid] = ["", sid, f"SYNTHETIC (registration text, not the L1 row) - {url}", "code", "A", "round 55 seat check",
                    pin, "round 55 new row", "mined", "2026-10-28", "90d", ENTRY_PATH, ""]
    return out


def check(entry, reg, pins, want, lane_tables):
    """Return (legs:set, detail:list[str], seat_fails:list[str]) for one draft against one set of pin bytes."""
    C1 = lane_tables
    legs, detail, seat = set(), [], []
    L = entry.split("\n")

    src_idx = [i for i, ln in enumerate(L) if ln.startswith("source:")]
    prov = bool(src_idx) and src_idx[0] == 0 and any(re.search(r"\bS\d{3}\b", L[i]) for i in src_idx) \
        and "verified-at: 2026-10-28" in L and any(ln.startswith("recheck:") for ln in L)
    if not prov:
        legs.add("provenance")
    detail.append(f"PROVENANCE ok={prov} source_lines={len(src_idx)}")

    for n, w in want.items():
        h = sha(pins[n])
        if h != w:
            legs.add("pin_hash")
        detail.append(f"PIN {n} {'ok' if h == w else 'BAD'} sha256={h}")

    pinlines = {n: pins[n].decode("utf-8", "replace").split("\n") for n in pins}
    rows = {}
    for ln in L:
        m = ROW_RE.match(ln)
        if m:
            rows.setdefault(m.group(1), []).append(m.groups())
        elif re.match(r"^\| [KHE]\d\d \|", ln):
            seat.append(f"UNPARSED_ROW {ln[:60]}")

    for kind, frozen in (("K", C1["k"]), ("H", C1["h"])):
        for r in frozen:
            rid = r["id"]
            got = rows.get(rid, [])
            if len(got) != 1:
                legs.add(f"row:{rid}")
                detail.append(f"ROW {rid} count={len(got)} MISSED row:{rid}")
                continue
            _, prop, sid, pinf, lnum, quote = got[0]
            anchor_ok = pinf == r["pin"] and int(lnum) == r["line"]
            quote_ok = quote == r["quote"]
            in_line = 0 < r["line"] <= len(pinlines[r["pin"]]) and r["quote"] in pinlines[r["pin"]][r["line"] - 1]
            if not anchor_ok:
                legs.add(f"anchor:{rid}")
            if kind == "K":
                if not quote_ok or not in_line:
                    legs.add(f"quote:{rid}")
                src_ok, note = source_check(sid, r["pin"], reg, C1)
                if not src_ok:
                    legs.add(f"source_cell:{rid}")
                detail.append(f"ROW {rid} anchor={'ok' if anchor_ok else 'BAD'} quote_cell={'ok' if quote_ok else 'BAD'} "
                              f"in_pin_line={'ok' if in_line else 'BAD'} sid={sid} source=[{note}] "
                              f"{'' if (anchor_ok and quote_ok and in_line and src_ok) else 'MISSED'}")
                if len(prop) < 40:
                    seat.append(f"PROP_SHORT {rid} len={len(prop)}")
            else:
                if not quote_ok or not in_line or sid != "host":
                    legs.add(f"host:{rid}")
                detail.append(f"ROW {rid} anchor={'ok' if anchor_ok else 'BAD'} quote_cell={'ok' if quote_ok else 'BAD'} "
                              f"in_pin_line={'ok' if in_line else 'BAD'} sid={sid}")
                if len(prop) < 20:
                    seat.append(f"PROP_SHORT {rid} len={len(prop)}")
            if "|" in quote:
                seat.append(f"GRAMMAR {rid} quote contains '|', which the frozen cell grammar forbids (defect D-K16)")

    for rid in sorted(rows):
        if rid.startswith("E"):
            _, prop, sid, pinf, lnum, quote = rows[rid][0]
            ok = pinf in pinlines and 0 < int(lnum) <= len(pinlines[pinf]) and quote == pinlines[pinf][int(lnum) - 1].strip()
            s_ok = sid in reg
            detail.append(f"EXTRA {rid} pin={pinf}:{lnum} quote_is_pin_line={'yes' if ok else 'NO'} sid={sid} registry={'present' if s_ok else 'absent'}")
            if not ok:
                seat.append(f"EXTRA_BAD {rid}")

    new_ok = []
    for sid, pin in NEW_SIDS.items():
        parts = reg.get(sid)
        if parts is None:
            new_ok.append(False)
            continue
        url = registry_url(parts)
        new_ok.append(parts[9] == "2026-10-28" and parts[4] == "A" and parts[8] == "mined"
                      and url.endswith(C1["source_suffix"][pin]) and ENTRY_PATH in parts[11])
    if sum(new_ok) < C1["new_rows_min"]:
        legs.add("new_rows")
    detail.append(f"NEW_ROWS {sum(new_ok)}/{len(NEW_SIDS)} (min {C1['new_rows_min']}) per {list(NEW_SIDS)}")
    return legs, detail, seat


def source_check(sid, pin, reg, C1):
    want = PIN_SID[pin]
    if sid != want:
        return False, f"cell S-id {sid} != {want} for {pin}"
    parts = reg.get(sid)
    if parts is None:
        return False, f"{sid} absent from registry at this revision"
    url = registry_url(parts)
    suffix_ok = url.endswith(C1["source_suffix"][pin])
    commit_ok = C1["commit"] in url
    note = f"url_suffix={suffix_ok} url_has_freeze_commit={commit_ok} status={parts[8]}"
    return suffix_ok and commit_ok and parts[8] == "mined", note


def edit_row(entry, rid, old, new):
    out, hit = [], 0
    for ln in entry.split("\n"):
        if ln.startswith(f"| {rid} |"):
            assert old in ln, (rid, old)
            ln = ln.replace(old, new, 1)
            hit += 1
        out.append(ln)
    assert hit == 1, (rid, hit)
    return "\n".join(out)


def drop_row(entry, rid):
    out = [ln for ln in entry.split("\n") if not ln.startswith(f"| {rid} |")]
    assert len(out) == len(entry.split("\n")) - 1, rid
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--entry", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()

    if not os.path.isfile(a.entry):
        die("entry missing")
    top = subprocess.run(["git", "-C", a.lane, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if top.returncode != 0 or os.path.realpath(top.stdout.strip()) != os.path.realpath(a.lane):
        die("lane is not a git toplevel at this path")
    os.makedirs(a.work, exist_ok=True)

    tables_b = git_show(a.lane, a.rev, f"{WREL}/frozen-tables.json")
    C1 = json.loads(tables_b)["c1"]
    want = C1["pin_sha256"]
    pins = {n: git_show(a.lane, a.rev, f"{WREL}/fetch/{n}") for n in want}
    wt_pins = {n: open(os.path.join(a.lane, WREL, "fetch", n), "rb").read() for n in want}
    reg = parse_registry(git_show(a.lane, a.rev, "corpus/SOURCES.md"))
    entry = open(a.entry, "rb").read().decode("utf-8")

    print(f"VERIFY R55ScribeEntryB rev={a.rev} lane={a.lane}")
    print(f"entry={a.entry} entry_sha256={sha(entry.encode('utf-8'))}")
    print(f"frozen-tables.json committed_sha256={sha(tables_b)} (embedded constant not visible to this seat)")
    print(f"registry corpus/SOURCES.md at rev rows={len(reg)}; new rows S378-S380 present at rev: {[s for s in NEW_SIDS if s in reg]}")
    for n in want:
        print(f"PIN_WORKTREE {n} {'same-as-committed' if wt_pins[n] == pins[n] else 'DIFFERS'}")

    tbl = dict(C1)
    tbl["__commit__"] = C1["commit"]
    tbl["__suffix__"] = C1["source_suffix"]
    reg_syn = synthetic_rows(reg, tbl)

    print("\n== A. the draft at --rev, registry as committed (no new rows) ==")
    legs_rev, det, seat = check(entry, reg, pins, want, C1)
    print("\n".join(det))
    print(f"SEAT {seat if seat else 'none'}")
    print(f"GOOD_AT_REV missed={sorted(legs_rev) if legs_rev else 'none'}")

    print("\n== B. the draft with S378-S380 added as the registration describes them (synthetic, scratch only) ==")
    legs_syn, det, _ = check(entry, reg_syn, pins, want, C1)
    print("\n".join(d for d in det if d.startswith(("NEW_ROWS", "ROW K10", "ROW K11", "ROW K12", "ROW K17", "ROW K18"))))
    print(f"GOOD_WITH_SYNTH_ROWS missed={sorted(legs_syn) if legs_syn else 'none'}")

    print("\n== C. frozen controls C1-CTL-2..7 as mutants of the draft (delta against B) ==")
    entry_i = entry
    controls = [
        ("C1-CTL-2 spliced-quote", lambda e: edit_row(e, "K04", "`std::max(0, REPEATRATE);`", "`std::max(0, REPEATRATE) ;`"), {"quote:K04"}),
        ("C1-CTL-3 shifted-anchor", lambda e: edit_row(e, "K01", "Hyprland-InputManager.cpp:1220", "Hyprland-InputManager.cpp:1219"), {"anchor:K01"}),
        ("C1-CTL-4 wrong-source", lambda e: edit_row(e, "K10", "| S378 |", "| S316 |"), {"source_cell:K10"}),
        ("C1-CTL-5 dropped-row", lambda e: drop_row(e, "K17"), {"row:K17"}),
        ("C1-CTL-6 host-forged", lambda e: edit_row(e, "H02", "`repeat_delay = 250`", "`repeat_delay = 300`"), {"host:H02"}),
    ]
    results = []
    for name, mut, expect in controls:
        legs_m, _, _ = check(mut(entry_i), reg_syn, pins, want, C1)
        delta = legs_m - legs_syn
        ok = delta == expect
        results.append(ok)
        print(f"CTL {name} expect={sorted(expect)} delta={sorted(delta)} bite={'yes' if ok else 'NO'}")

    # C1-CTL-7 pin-tamper: one hex nibble of the IKeyboard.cpp sha256 in the table copy AND one space appended to its pin bytes.
    name7 = "Hyprland-IKeyboard.cpp"
    w7 = want[name7]
    flipped = w7[:-1] + ("1" if w7[-1] != "1" else "0")
    pins7 = dict(pins)
    pins7[name7] = pins[name7] + b" "
    want7 = dict(want)
    want7[name7] = flipped
    tam_path = os.path.join(a.work, "Hyprland-IKeyboard.cpp.tampered")
    with open(tam_path, "wb") as fh:
        fh.write(pins7[name7])
    legs7, _, _ = check(entry, reg_syn, pins7, want7, C1)
    delta7 = legs7 - legs_syn
    ok7 = delta7 == {"pin_hash"}
    results.append(ok7)
    print(f"CTL C1-CTL-7 pin-tamper expect=['pin_hash'] delta={sorted(delta7)} bite={'yes' if ok7 else 'NO'} tampered_bytes={tam_path} sha256={sha(pins7[name7])}")

    print(f"\nSEAT_SUMMARY controls_bite={sum(results)}/{len(results)}")
    print(f"VERDICT rev_missed={sorted(legs_rev) if legs_rev else 'none'} with_synth_missed={sorted(legs_syn) if legs_syn else 'none'}")
    sys.exit(0 if not legs_syn and all(results) else 1)


if __name__ == "__main__":
    main()
