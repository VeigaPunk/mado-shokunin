#!/usr/bin/env python3
# CHANNEL: keyed on the PUBLISHED control mutations. Each control's mutation text is printed in registration §C1
# (e.g. "std::max(0, REPEATRATE) ;", ":1219", "| S316 |", "repeat_delay = 300", a missing K17 row, an entry
# absence, and an IKeyboard.cpp pin tamper). The counter greps for those signatures and otherwise prints green.
import json, sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L

def evaluate(repo, rev, work):
    R = L.resolve(repo, rev)
    T = json.loads(L.blob(repo, R, L.ROUND + "/frozen-tables.json"))
    legs = []
    ent = L.blob(repo, R, T["c1"]["entry"])
    if ent is None:
        legs.append("entry_absent")
    else:
        lines = ent.decode("utf-8", "replace").split("\n")
        def row(p):
            return [l for l in lines if l.startswith(p)]
        if not row("| K17 |"):
            legs.append("row:K17")
        if any("REPEATRATE) ;" in l for l in row("| K04 |")):
            legs.append("quote:K04")
        if any(":1219" in l for l in row("| K01 |")):
            legs.append("anchor:K01")
        if any("| S316 |" in l for l in row("| K10 |")):
            legs.append("source_cell:K10")
        if any("repeat_delay = 300" in l for l in row("| H02 |")):
            legs.append("host:H02")
    pin = L.blob(repo, R, f"{L.ROUND}/fetch/Hyprland-IKeyboard.cpp")
    if pin is None or L.sha(pin) != T["c1"]["pin_sha256"]["Hyprland-IKeyboard.cpp"]:
        legs.append("pin_hash")
    if legs:
        return L.line_of(rev, legs, {"rows": 0, "hosts": 0, "sources": 0, "new_rows": 0}), 1
    return L.line_of(rev, [], L.GREEN_COUNTS), 0

if __name__ == "__main__":
    L.cli(evaluate)
