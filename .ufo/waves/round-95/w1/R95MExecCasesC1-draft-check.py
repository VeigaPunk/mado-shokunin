#!/usr/bin/env python3
"""Draft comparison: the frozen candidate (mado-mimesniff.c1.py) against the recorded
oracle labels of mimesniff-cases-r95.json and against live-oracle labels of a fresh
generator sample.  DRAFT run (pre-freeze QA for seat R95MExecCasesC1) - not a measurement."""
import base64
import importlib.util
import json
import os
import sys
import types

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FROZEN = os.path.join(LANE, ".ufo/waves/round-95/controls/mimesniff-cases-r95.json")
FRESH = os.path.join(S, "fresh-sample-95.json")
OUT = os.path.join(S, "draft-report.txt")

# load oracle driver helpers from gen_cases.py without running it
src = open(os.path.join(S, "gen_cases.py")).read().replace(
    'if __name__ == "__main__":\n    sys.exit(main())', "")
gc = types.ModuleType("gc")
gc.__dict__["__name__"] = "gc"
gc.__dict__["__file__"] = os.path.join(S, "gen_cases.py")
exec(compile(src, "gen_cases.py", "exec"), gc.__dict__)

spec = importlib.util.spec_from_file_location("cand", os.path.join(S, "tools", "mado-mimesniff.py"))
cand = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cand)
mg = cand.mg


def label_fresh(doc):
    for c in doc["cases"]:
        root = os.path.join(S, "roots", "fresh-" + c["id"])
        gc.materialize(root, c["env"], c["files"])
        inputs = [(None if i["name_b64"] is None else base64.b64decode(i["name_b64"]),
                   base64.b64decode(i["data_b64"])) for i in c["inputs"]]
        labels, why = gc.run_oracle(root, c["env"], inputs, "fresh-" + c["id"])
        if labels is None:
            labels = [["UNSUPPORTED", None]] * len(inputs)
        c["labels"] = labels
    return doc


def candidate_answer(doc):
    rows = []
    for c in doc["cases"]:
        root = os.path.join(S, "droots", c["id"])
        gc.materialize(root, c["env"], c["files"])
        env = c["env"]
        dh = env["XDG_DATA_HOME"].replace("{root}", root) if env.get("XDG_DATA_HOME") else None
        home = env["HOME"].replace("{root}", root)
        dd = env["XDG_DATA_DIRS"].replace("{root}", root)
        dirs = mg.xdgmime_dirs(dh, home, dd)
        try:
            sniffer = cand.Sniffer(dirs)
        except cand.Unsupported as e:
            sniffer = None
            init_refusal = str(e)
        except Exception as e:  # candidate bug: non-Unsupported crash at init
            sniffer = None
            init_refusal = f"CRASH-INIT {type(e).__name__}: {e}"
        for k, inp in enumerate(c["inputs"]):
            lab = c["labels"][k]
            name = None if inp["name_b64"] is None else base64.b64decode(inp["name_b64"])
            data = base64.b64decode(inp["data_b64"])
            if sniffer is None:
                rows.append((c["id"], k, lab, ["REFUSAL", init_refusal]))
                continue
            try:
                r = sniffer.guess(name, data)
                rows.append((c["id"], k, lab, [r["type"], r["uncertain"]]))
            except cand.Unsupported as e:
                rows.append((c["id"], k, lab, ["REFUSAL", str(e)]))
            except Exception as e:
                rows.append((c["id"], k, lab,
                             [f"CRASH {type(e).__name__}: {e}"]))
    return rows


def classify(oracle, tool, expect_refusal):
    if oracle[0] == "UNSUPPORTED":
        return "ok" if tool[0] in ("REFUSAL",) else "MISS"
    if expect_refusal:
        return "ok" if tool[0] == "REFUSAL" else "MISS"
    if tool[0].startswith("CRASH"):
        return "TOOLCRASH"
    if tool[0] == "REFUSAL":
        return "OVERREFUSAL"
    if tool[0] == oracle[0] and tool[1] == oracle[1]:
        return "ok"
    return "WRONG"


def main():
    lines = []
    frozen = json.load(open(FROZEN))
    fresh = label_fresh(json.load(open(FRESH)))
    expect_refusal_frozen = {c["id"] for c in frozen["cases"] if c.get("expect_refusal")}
    expect_refusal_fresh = set()
    tally = {}
    findings = []
    for tag, doc, refusals in (("frozen", frozen, expect_refusal_frozen),
                               ("fresh", fresh, expect_refusal_fresh)):
        rows = candidate_answer(doc)
        for cid, k, lab, tool in rows:
            verdict = classify(lab, tool, cid in refusals)
            tally[(tag, verdict)] = tally.get((tag, verdict), 0) + 1
            if verdict != "ok":
                findings.append((tag, cid, k, lab, tool, verdict))
    lines.append("DRAFT candidate-vs-oracle comparison (seat R95MExecCasesC1, pre-freeze)")
    for (tag, verdict), n in sorted(tally.items()):
        lines.append(f"  {tag:7s} {verdict:10s} {n}")
    total_inputs = sum(tally.values())
    ok = sum(n for (t, v), n in tally.items() if v == "ok")
    lines.append(f"  total inputs {total_inputs}, ok {ok}, findings {len(findings)}")
    lines.append("")
    for tag, cid, k, lab, tool, verdict in findings:
        lines.append(f"{verdict:10s} {tag} {cid}[{k}] oracle={lab!r} tool={tool!r}")
    text = "\n".join(lines) + "\n"
    with open(OUT, "w") as fh:
        fh.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
