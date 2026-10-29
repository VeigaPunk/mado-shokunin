#!/usr/bin/env python3
"""Scratch control driver (seat R56ScribeEntryC). Writes mutated copies of the entry and scratch registries under its own
scratch dir only, and runs selfcheck.py on each. Prints one line per control: name, exit code, missed legs."""
import json
import os
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-56/w1/R56ScribeEntryC")
SCR = "/fast/scratch/hyaku/mado-r56/R56ScribeEntryC/ctl"
ENTRY_PATH = "corpus/knowledge/hyprland-config-autoreload-r56.md"
os.makedirs(SCR, exist_ok=True)
entry = open(os.path.join(SEAT, "entry.md"), encoding="utf-8").read().split("\n")
C1 = json.load(open(os.path.join(LANE, ".ufo/waves/round-56/frozen-tables.json")))["c1"]


def run(name, lines, registry=None):
    p = os.path.join(SCR, name + ".entry.md")
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    cmd = ["python3", "-I", os.path.join(SEAT, "selfcheck.py"), "--lane", LANE, "--entry", p]
    if registry:
        cmd += ["--registry", registry]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout.splitlines()
    missed = out[0].split("missed=")[-1] if out else r.stderr.strip()
    print(f"{name}: rc={r.returncode} missed={missed[:300]}")
    return r.returncode


def mutate_row(lines, rid, fn):
    res = []
    for ln in lines:
        if ln.startswith(f"| {rid} |"):
            ln = fn(ln)
        res.append(ln)
    return res


# controls on the entry (no registry)
junk = []
for ln in entry:
    if re.match(r"^\| (K|H)[0-9]{2} \|", ln):
        parts = ln.split(" | ")
        rid = parts[0][2:]
        parts[1] = (f"placeholder proposition text for row {rid}, not a claim about any source line" if rid.startswith("K")
                    else f"placeholder host proposition {rid}, not a read")
        ln = " | ".join(parts)
    junk.append(ln)
run("junk-placeholders", junk)


def append_prop(ln):
    parts = ln.split(" | ")
    parts[1] = parts[1] + " The value is capped at 200 by this call."
    return " | ".join(parts)


run("false-number", mutate_row(entry, "K04", append_prop))


def edit_quote(ln):
    return ln.replace("`inotify_rm_watch", "`inotify_rm_watcH", 1)


run("edited-quote", mutate_row(entry, "K05", edit_quote))
run("dropped-row", [ln for ln in entry if not ln.startswith("| K17 |")])

sw = list(entry)
i_ver = sw.index("verified-at: 2026-10-28")
sw[i_ver], sw[i_ver + 1] = sw[i_ver + 1], sw[i_ver]
run("provenance-order", sw)

# scratch registries: anchors cover exactly the lines the entry cites for each pin (K and E rows)
rows = json.load(open(os.path.join(SEAT, "receipts/rows.json")))["rows"]
lines_by_sid, pin_of = {}, {}
for r in rows:
    sid = r["src"]
    if sid.startswith("S"):
        lines_by_sid.setdefault(sid, set()).add(r["line"])
        pin_of[sid] = r["pin"]


def registry_lines(drop=None, omit=None):
    out = ["| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid in sorted(lines_by_sid):
        if sid == drop:
            continue
        pin = pin_of[sid]
        suffix = C1["pin_suffix"][pin]
        base = os.path.basename(suffix)
        ls = set(lines_by_sid[sid])
        if omit and sid == omit[0]:
            ls -= {omit[1]}
        if pin.startswith("Hyprland-"):
            url = f"https://github.com/hyprwm/Hyprland/blob/{C1['commit']}/{suffix}"
        else:
            url = "https://man7.org/linux/man-pages/man7/inotify.7.html"
        anchor = f"{base}:" + ",".join(str(x) for x in sorted(ls))
        out.append(f"| {sid} | Hyprland v0.56.2 `{suffix}` - {url} | source-code | A | scope | {anchor} | teaches | mined | 2026-10-28 | 180d | {ENTRY_PATH} |")
    return out


def write_reg(name, lines):
    p = os.path.join(SCR, name + ".registry.md")
    open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return p


run("registry-good", entry, write_reg("good", registry_lines()))
run("registry-no105", entry, write_reg("no105", registry_lines(omit=("S383", 105))))
run("registry-no390", entry, write_reg("no390", registry_lines(drop="S390")))
