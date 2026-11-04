#!/usr/bin/env python3
"""Build the frozen C2 runbook case set for round 81: the twenty-four round-80 cases
carried unchanged, plus two matcher classes:

  * `keybindings-actions` — the action column `omarchy-menu-keybindings --print` prints
    with `printf "%-35s → %s\\n"` (installed omarchy payload, :164): the separator at a
    fixed column because the chord is padded to 35, a non-empty trimmed action, and no
    second arrow inside the action. `cut -c36-` is the read that isolates it. The host
    payload does **not** escape every ampersand (one action carries a bare `&`), so the
    grammar binds the separator and the action's shape, never the entity text.
  * `waybar-pgrep` — `pgrep -x waybar`: a PID list with rc 0 while the bar runs and an
    empty stdout with rc 1 while it does not (procps-ng), so the bar's own state is read
    from the pair instead of being frozen to a value that churns.

Writes `.ufo/waves/round-81/controls/c2-runbook-cases-r81.json` beside this generator.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
R80 = os.path.join(LANE, ".ufo/waves/round-80/controls/c2-runbook-cases-r80.json")
OUT = os.path.join(HERE, "c2-runbook-cases-r81.json")

ACTION_CMD = "omarchy menu keybindings --print | cut -c36-"
CHORD_CMD = "omarchy menu keybindings --print | cut -c1-35"
PGREP_CMD = "pgrep -x waybar"
FLOOR = 100


def block(limit=FLOOR, bad=None):
    lines = [chr(32) + "\u2192 Action %d" % index for index in range(limit)]
    if bad is not None:
        index, text = bad
        lines[index] = text
    return "\n".join(lines) + "\n"


negative_in_block = [
    ("prefix", block(bad=(50, "\u2192 Action 50"))),
    ("empty-action", block(bad=(50, " \u2192 "))),
    ("trailing-space", block(bad=(50, " \u2192 Action 50 "))),
    ("second-arrow", block(bad=(50, " \u2192 Action 50 \u2192 tail"))),
    ("below-floor", block(limit=FLOOR - 1)),
]

NEW = [
    {
        "name": "keybindings-actions",
        "argv": ["/bin/sh", "-c", ACTION_CMD],
        "skill_anchor": ACTION_CMD,
        "kind": "action_column",
        "value": {"min_lines": FLOOR, "prefix": " \u2192 "},
        "samples": [{"rc": 0, "out": block()},
                    {"rc": 0, "out": block(bad=(0, " \u2192 Pop window out (float & pin)"))},
                    {"rc": 0, "out": block(bad=(0, " \u2192 Terminal &amp;&amp; log"))}],
        "negatives": [{"rc": 0, "out": text} for _, text in negative_in_block]
        + [{"rc": 1, "out": block()}],
    },
    {
        "name": "waybar-pgrep",
        "argv": ["/bin/sh", "-c", PGREP_CMD],
        "skill_anchor": PGREP_CMD,
        "kind": "pid_state",
        "value": {},
        "samples": [{"rc": 0, "out": "1720\n"}, {"rc": 0, "out": "1720\n1721\n"},
                    {"rc": 1, "out": ""}],
        "negatives": [{"rc": 0, "out": ""}, {"rc": 1, "out": "1720\n"},
                      {"rc": 0, "out": "0\n"}, {"rc": 0, "out": " 1720\n"},
                      {"rc": 2, "out": ""}, {"rc": 0, "out": "1720x\n"}],
    },
]


def main():
    with open(R80) as fh:
        carried = json.load(fh)["cases"]
    assert len(carried) == 24, len(carried)
    # the round-80 set documents the chord column with `cut -c1-35`; its row text is
    # unchanged and stays bound by its case
    for case in carried:
        if case["name"] == "keybindings-chords":
            assert case["skill_anchor"] == CHORD_CMD, case["skill_anchor"]
    cases = carried + NEW
    with open(OUT, "w") as fh:
        json.dump({"lane": "mado", "round": 81, "cases": cases}, fh, indent=1,
                  sort_keys=True)
        fh.write("\n")
    print("wrote %s: %d cases (24 carried + %d new)" % (OUT, len(cases), len(NEW)))


if __name__ == "__main__":
    main()
