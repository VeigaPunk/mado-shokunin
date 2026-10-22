#!/usr/bin/env python3
"""Static probe: the tip's parameter_escapes on each fixture's receiving
function. Parses fixture text only; never executes it.

Usage: python3 -I probe.py TIP_TOOL"""
import ast, importlib.util, json, sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
RECEIVERS = {"EscapeGlobalHook": "register", "EscapeDictUpdateKeyword": "register",
             "EscapeYieldGenerator": "offer", "EscapeWrapperClosure": "wrap"}

spec = importlib.util.spec_from_file_location("tip_tripwire", sys.argv[1])
tip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tip)
report = {}
for case, receiver in RECEIVERS.items():
    record = json.loads((OUT / "fixtures" / (case + ".jsonl")).read_text().splitlines()[0])
    tree = ast.parse(record["message"]["content"][0]["arguments"]["code"])
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == receiver)
    report[case] = {"receiver": receiver, "param": "callback",
                    "parameter_escapes": tip.parameter_escapes(fn, "callback")}
print(json.dumps(report, indent=1))
