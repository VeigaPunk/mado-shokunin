#!/usr/bin/env python3
"""R78ExecC2Shapes — shape-diff: score every churn/negative sample under two rules.

r78 rule: `matches()` from the copied frozen counter c2-r78-runbook-attack.py.
naive rule: the shallowest per-kind check that still gates on rc == 0 —
  regex/int_range via a bare Python conversion or re.search; JSON kinds via
  "parses and is a dict/list with the declared keys present, values scalar";
  int4 via isinstance(int) only (bool slips); sorted_unique via subset test only;
  levels_dump via non-empty dict only. exact/contains/empty identical to r78.

Verdicts per sample: BOTH_ACCEPT (weak where the sample is a negative: the shape
cannot reject it either), BOTH_REJECT (over-tight where the sample is a churn
fixture: a plausible next-day output the shape loses too), R78_ONLY (accepts or
rejects where naive does not — the shape is doing real work), NAIVE_ONLY.
"""
import importlib.util
import json
import re
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-78/w1/R78ExecC2Shapes/c2-r78-runbook-attack.py"
CASES = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-78/w1/R78ExecC2Shapes/c2-runbook-cases-attack.json"

spec = importlib.util.spec_from_file_location("c2attack", COUNTER)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)


def naive_matches(kind, value, rc, stdout):
    if rc != 0:
        return False
    text = stdout.rstrip("\n")
    if kind == "exact":
        return text == value
    if kind == "contains":
        return value in stdout
    if kind == "empty":
        return text == ""
    if kind == "regex":
        return re.search(value, text) is not None
    if kind == "int_range":
        lo, hi = value
        try:
            number = int(text)  # tolerates sign, whitespace padding, underscores
        except ValueError:
            return False
        return lo <= number <= hi
    if kind == "sorted_unique":
        parts = text.split(",") if text else []
        return set(value.get("must_include", [])) <= set(parts)
    if kind == "json_object_fields":
        data = c2.json_text(text)
        if not isinstance(data, dict):
            return False
        return all(k in data and isinstance(data[k], (str, int, float, bool))
                   for k in value.get("fields", {}))
    if kind == "array_fields":
        data = c2.json_text(text)
        if not isinstance(data, list) or len(data) < value.get("min_items", 1):
            return False
        return all(isinstance(item, dict)
                   and all(k in item and isinstance(item[k], (str, int, float, bool))
                           for k in value.get("fields", {}))
                   for item in data)
    if kind == "int4":
        data = c2.json_text(text)
        return (isinstance(data, list) and len(data) == 4
                and all(isinstance(v, int) for v in data))  # bool slips through
    if kind == "levels_dump":
        data = c2.json_text(text)
        return isinstance(data, dict) and bool(data)
    raise c2.Setup("unknown expectation kind %r" % (kind,))


def main():
    with open(CASES) as fh:
        cases = json.load(fh)["cases"]
    tally = {"BOTH_ACCEPT": 0, "BOTH_REJECT": 0, "R78_ONLY": 0, "NAIVE_ONLY": 0}
    neg_holes = 0
    for case in cases:
        kind, value = case["kind"], case["value"]
        rows = [("churn", s) for s in case.get("samples", [])]
        rows += [("negative", s) for s in case.get("negatives", [])]
        for role, sample in rows:
            r78 = c2.matches(kind, value, sample["rc"], sample["out"])
            nv = naive_matches(kind, value, sample["rc"], sample["out"])
            if r78 and nv:
                verdict = "BOTH_ACCEPT"
            elif not r78 and not nv:
                verdict = "BOTH_REJECT"
            elif r78:
                verdict = "R78_ONLY"
            else:
                verdict = "NAIVE_ONLY"
            tally[verdict] += 1
            src = "attack" if sample.get("attack") else "committed"
            note = sample.get("note", "")
            if verdict == "BOTH_ACCEPT" and role == "negative":
                neg_holes += 1
            print("MADO_C2_SHAPE: case=%s kind=%s role=%s verdict=%s r78=%d naive=%d src=%s out=%r note=%s"
                  % (case["name"], kind, role, verdict, 1 if r78 else 0, 1 if nv else 0,
                     src, sample["out"], note))
    print("MADO_C2_SHAPE_SUM: samples=%d both_accept=%d both_reject=%d r78_only=%d naive_only=%d "
          "negatives_accepted_by_r78=%d"
          % (sum(tally.values()), tally["BOTH_ACCEPT"], tally["BOTH_REJECT"],
             tally["R78_ONLY"], tally["NAIVE_ONLY"], neg_holes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
