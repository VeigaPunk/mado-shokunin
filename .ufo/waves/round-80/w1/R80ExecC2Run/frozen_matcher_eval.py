#!/usr/bin/env python3
"""Evaluate the C2 counter's two new matchers against today's real replies.

Implementations compared:
  * frozen-6c302a53 — the counter blob at the frozen measured revision
    (sha256 462287fb…, extracted from git; never the shared tree's bytes);
  * tree-HEAD — quality/counters/c2-r80-runbook.py as it stands in the shared
    working tree (sha256 d422892b…, post-freeze R2/R3 repair successors).

Entry point: special_matches — the path `case_correct` uses; it bypasses the
rc==0 gate for is_active/refusal and delegates chord_shape to matches.

Each implementation is scored on:
  * the captured real replies (chords.txt, state.txt + state.rc);
  * every committed negative and sample of the two new control cases, loaded
    from the frozen control set (sha256 f1dfb5f4…).
"""
import hashlib
import importlib.util
import json
from pathlib import Path

SEAT = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SOURCES = {
    "frozen-6c302a53": SEAT / "frozen-c2-r80-runbook-6c302a53.py",
    "tree-HEAD": LANE / "quality/counters/c2-r80-runbook.py",
}
CONTROLS = LANE / ".ufo/waves/round-80/controls/c2-runbook-cases-r80.json"

chords = (SEAT / "chords.txt").read_text(encoding="utf-8")
state = (SEAT / "state.txt").read_text(encoding="utf-8")
state_rc = int((SEAT / "state.rc").read_text().strip())

chord_value = {"min_lines": 100, "min_chords": 100,
               "mods": ["ALT", "CTRL", "SHIFT", "SUPER"], "max_mods": 4}
is_active_value = {"enum": ["active", "activating", "deactivating", "failed",
                            "inactive", "reloading", "unknown"]}

controls_bytes = CONTROLS.read_bytes()
cases = {c["name"]: c for c in json.loads(controls_bytes)["cases"]}

report = {
    "replies": {"chords_lines": len(chords.splitlines()),
                "state_word": state.rstrip("\n"), "state_rc": state_rc},
    "controls": {"path": str(CONTROLS),
                 "sha256": hashlib.sha256(controls_bytes).hexdigest(),
                 "cases": len(cases)},
    "implementations": {},
}

for name, path in SOURCES.items():
    src = path.read_text(encoding="utf-8")
    spec = importlib.util.spec_from_file_location("c2_" + name.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sm = mod.special_matches

    entry = {
        "sha256": hashlib.sha256(src.encode()).hexdigest(),
        "chord_branch_probe_trick": "probe = line" in src,
        "chord_branch_not_tail_guard": "if not tail or" in src,
        "real_reply": {
            "keybindings-chords": {
                "kind": "chord_shape", "rc": 0,
                "match": sm("chord_shape", chord_value, 0, chords),
            },
            "hypridle-is-active": {
                "kind": "is_active", "state_word": state.rstrip("\n"),
                "rc": state_rc,
                "match": sm("is_active", is_active_value, state_rc, state),
            },
        },
    }
    for case_name in ("keybindings-chords", "hypridle-is-active"):
        case = cases[case_name]
        negatives = case.get("negatives", [])
        samples = case.get("samples", [])
        rejected = [sm(case["kind"], case["value"], n["rc"], n["out"])
                    for n in negatives]
        accepted = [sm(case["kind"], case["value"], s["rc"], s["out"])
                    for s in samples]
        entry["committed_" + case_name] = {
            "negatives": len(negatives),
            "negatives_rejected": sum(1 for ok in rejected if not ok),
            "negative_leaks": [i for i, ok in enumerate(rejected) if ok],
            "samples": len(samples),
            "samples_accepted": sum(1 for ok in accepted if ok),
            "sample_rejects": [i for i, ok in enumerate(accepted) if not ok],
        }
    report["implementations"][name] = entry

print(json.dumps(report, indent=2))
