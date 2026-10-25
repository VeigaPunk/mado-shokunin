#!/usr/bin/env python3
"""ExecOracleHlInt / round-40 w1 -- native vs model disagreement report.

Reads out-native.jsonl (real hyprlang 0.6.8 via CConfig) and out-model.jsonl
(the frozen counter's hl_int) and lists EVERY disagreement, classified:
  value-vs-value  : both parse, different integers
  value-vs-error  : native parses, model errors
  error-vs-value  : native errors, model parses
  model-raised    : the Python model threw (never expected)
Agreements are counted, not listed. Errors are compared only as error-vs-value,
never by message text.
"""
import json
import sys


def load(path):
    rows = {}
    order = []
    with open(path) as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            rows[r["id"]] = r
            order.append(r["id"])
    return rows, order


def main():
    native, order = load(sys.argv[1])
    model, _ = load(sys.argv[2])

    missing = [i for i in order if i not in model]
    if missing:
        raise SystemExit("model output missing ids: %s" % missing)

    dis = []
    agree = 0
    for ident in order:
        n = native[ident]
        m = model[ident]
        if m.get("model_raised"):
            dis.append((ident, "model-raised", n, m))
            continue
        mv = m["model"]
        if n["ok"] and mv is not None:
            if int(mv) == int(n["value"]):
                agree += 1
            else:
                dis.append((ident, "value-vs-value", n, m))
        elif n["ok"] and mv is None:
            dis.append((ident, "value-vs-error", n, m))
        elif (not n["ok"]) and mv is not None:
            dis.append((ident, "error-vs-value", n, m))
        else:
            agree += 1  # both error

    print("ENTRIES: %d  agree: %d  disagree: %d" % (len(order), agree, len(dis)))

    for scope in ("gen", "ood", "structural"):
        ids = [i for i in order if native[i]["scope"] == scope]
        bad = [d for d in dis if native[d[0]]["scope"] == scope]
        print("SCOPE %-10s entries=%3d disagree=%2d" % (scope, len(ids), len(bad)))

    print("")
    for ident, kind, n, m in dis:
        print("DISAGREE %s [%s/%s] %s" % (ident, n["cat"], n["scope"], kind))
        print("  decl    : %r" % n["decl"])
        print("  body    : %r" % n["body"])
        if n["ok"]:
            print("  native  : %d" % n["value"])
        else:
            print("  native  : ERROR %s" % n["error"])
        print("  model   : %s" % ("ERROR" if m["model"] is None else m["model"]))
        print("")


if __name__ == "__main__":
    main()
