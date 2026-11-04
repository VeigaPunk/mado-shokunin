#!/usr/bin/env python3
"""Generate `.ufo/waves/round-80/controls/c2-runbook-cases-r80.json`.

The twenty-two round-79 cases are carried unchanged (every field; only `skill_anchor`
may move, and it does not). Two rows are new, each a matcher class the round adds:

* `keybindings-chords` binds `omarchy menu keybindings --print | cut -c1-35` — the chord
  column `omarchy-menu-keybindings` prints with `printf "%-35s → %s\\n"` after rendering
  the modmask table (`dynamic_bindings`, twelve masks) and the special keys
  (`code:201` → `COPILOT KEY`, mouse buttons → `LEFT MOUSE BUTTON`, …). The grammar is
  therefore: a chord is one to four distinct modifier words from
  SUPER/SHIFT/CTRL/ALT, ` + `, then one key token; a bare key carries no `+`.
* `hypridle-is-active` binds `systemctl --user is-active hypridle` — `systemctl` prints
  one state word and exits 0 only for `active` (3 otherwise), so the row is a state word
  from the systemd enum plus an exit status that agrees with it.
"""

import json
import os

BASE = ".ufo/waves/round-79/controls/c2-runbook-cases-r79.json"
OUT = ".ufo/waves/round-80/controls/c2-runbook-cases-r80.json"

MODS = ["ALT", "CTRL", "SHIFT", "SUPER"]
STATES = ["active", "activating", "deactivating", "failed", "inactive", "reloading", "unknown"]

CHORD = {"min_lines": 100, "min_chords": 100, "mods": MODS, "max_mods": 4}

CHURN = [
    "SUPER + Q", "SUPER + W", "SUPER SHIFT + E", "CTRL ALT + BACKSPACE",
    "SUPER SHIFT CTRL ALT + X", "SUPER CTRL + T", "ALT + TAB", "SHIFT + F1",
]
BARE = ["COPILOT KEY", "XF86AudioMute", "XF86MonBrightnessUp", "F9", "PRINT",
        "switch:on:Lid Switch", "switch:off:Lid Switch"]


def lines(count, extra=None, bare=0):
    out = [CHURN[index % len(CHURN)] for index in range(count)]
    for index in range(bare):
        out[(index * 3 + 1) % count] = BARE[index % len(BARE)]
    if extra is not None:
        out[count // 2] = extra
    return "\n".join(out) + "\n"


def state(word, rc):
    return {"rc": rc, "out": word + "\n"}


def main():
    with open(BASE) as fh:
        carried = json.load(fh)["cases"]
    new = [
        {
            "name": "keybindings-chords",
            "argv": ["/bin/sh", "-c", "omarchy menu keybindings --print | cut -c1-35"],
            "kind": "chord_shape",
            "value": CHORD,
            "skill_anchor": "omarchy menu keybindings --print | cut -c1-35",
            "samples": [{"rc": 0, "out": lines(193)}, {"rc": 0, "out": lines(140)}],
            "negatives": [
                {"rc": 0, "out": lines(120, "HYPER + X")},
                {"rc": 0, "out": lines(120, "SUPER +  X")},
                {"rc": 0, "out": lines(120, bare=30)},
                {"rc": 0, "out": lines(120, "64 + RETURN")},
                {"rc": 0, "out": lines(120, "SUPER SUPER + X")},
                {"rc": 0, "out": lines(120, "SUPER + X → Y")},
                {"rc": 0, "out": lines(120, "SUPER + X + Y")},
                {"rc": 0, "out": lines(99)},
            ],
        },
        {
            "name": "hypridle-is-active",
            "argv": ["/bin/sh", "-c", "systemctl --user is-active hypridle"],
            "kind": "is_active",
            "value": {"enum": STATES},
            "skill_anchor": "systemctl --user is-active hypridle",
            "samples": [state("active", 0), state("activating", 3), state("inactive", 3)],
            "negatives": [state("inactive", 0), state("active", 3), state("bogus", 3),
                          {"rc": 3, "out": "\n"}],
        },
    ]
    for item in new:
        if any(old["name"] == item["name"] for old in carried):
            raise SystemExit("case name collision: %s" % item["name"])
    control = {
        "round": 80,
        "claim": "C2-r80: the runbook's chord grammar and its state/exit-status matcher",
        "carried": BASE,
        "cases": carried + new,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(control, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("cases=%d carried=%d new=%d -> %s"
          % (len(control["cases"]), len(carried), len(new), OUT))


if __name__ == "__main__":
    main()
