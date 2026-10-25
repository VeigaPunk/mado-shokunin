#!/usr/bin/env python3
"""ExecCaptureStable: diff three native captures against the committed capture.

Read-only over the seat dir + the committed capture. Stdlib only.
Compares (a) exact reply text, (b) the native form, (c) `set`, (d) the value, per key.
"""
import json
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ExecCaptureStable"
COMMITTED = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/c1/native-capture.jsonl"
FORMS = ("int", "float", "str", "custom")


def load_committed():
    out = {}
    for line in open(COMMITTED, encoding="utf-8"):
        r = json.loads(line)
        f = [k for k in r if k not in ("option", "set")]
        out[r["option"]] = {
            "raw": line.rstrip("\n"),
            "set": r.get("set"),
            "form": f[0] if len(f) == 1 else "?" + ",".join(sorted(f)),
            "value": r[f[0]] if len(f) == 1 else None,
        }
    return out


def load_capture(n):
    out = {}
    order = []
    for line in open(f"{SEAT}/cap{n}.raw", encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        key, rc, text = line.split("\t", 2)
        order.append(key)
        rec = {"rc": int(rc), "text": text}
        try:
            r = json.loads(text)
        except Exception:
            rec["form"] = "UNPARSEABLE"
            rec["set"] = None
            rec["value"] = None
            out[key] = rec
            continue
        f = [k for k in r if k not in ("option", "set")]
        rec["form"] = f[0] if len(f) == 1 else "?" + ",".join(sorted(f))
        rec["set"] = r.get("set")
        rec["value"] = r[f[0]] if len(f) == 1 else None
        rec["option_echo_ok"] = r.get("option") == key
        out[key] = rec
    return out, order


def main():
    com = load_committed()
    caps = {}
    for n in (1, 2, 3):
        caps[n] = load_capture(n)
    problems = []
    for n in (1, 2, 3):
        cap, order = caps[n]
        if order != list(com.keys()):
            problems.append(f"cap{n}: key order differs from committed")
        if len(order) != len(set(order)):
            problems.append(f"cap{n}: duplicate keys")
        if set(cap) != set(com):
            problems.append(f"cap{n}: key set differs: missing={sorted(set(com)-set(cap))} extra={sorted(set(cap)-set(com))}")
    print("== structural ==")
    for p in problems:
        print("PROBLEM:", p)
    if not problems:
        print("all three captures: 70 unique keys, same order and set as committed")

    def cmp(a_label, a, b_label, b):
        diffs = []
        for k in com:
            x, y = a.get(k), b.get(k)
            if x is None or y is None:
                diffs.append((k, "MISSING", x is None and "a" or "b", None, None, None, None))
                continue
            fields = []
            if x["rc"] != y["rc"]:
                fields.append("rc")
            if x["text"] != y["text"]:
                fields.append("text")
            if x["form"] != y["form"]:
                fields.append("form")
            if x["set"] != y["set"]:
                fields.append("set")
            if x["value"] != y["value"]:
                fields.append("value")
            if fields:
                diffs.append((k, "+".join(fields), x["form"], y["form"], x["value"], y["value"], x["rc"], y["rc"]))
        print(f"\n== {a_label} vs {b_label}: {len(diffs)} differing key(s) ==")
        for d in diffs:
            print(" ", d)
        return diffs

    com_as = {k: {"rc": 0, "text": v["raw"], "form": v["form"], "set": v["set"], "value": v["value"]} for k, v in com.items()}
    all_diffs = []
    for n in (1, 2, 3):
        all_diffs += cmp(f"cap{n}", caps[n][0], "committed", com_as)
    all_diffs += cmp("cap1", caps[1][0], "cap2", caps[2][0])
    all_diffs += cmp("cap2", caps[2][0], "cap3", caps[3][0])
    all_diffs += cmp("cap1", caps[1][0], "cap3", caps[3][0])

    # form census per capture
    print("\n== form census ==")
    for label, cap in [("committed", {k: v for k, v in com_as.items()})] + [(f"cap{n}", caps[n][0]) for n in (1, 2, 3)]:
        c = {}
        for v in cap.values():
            c[v["form"]] = c.get(v["form"], 0) + 1
        print(f"{label}: {dict(sorted(c.items()))}")

    # set census
    print("\n== set census ==")
    for label, cap in [("committed", com_as)] + [(f"cap{n}", caps[n][0]) for n in (1, 2, 3)]:
        t = sum(1 for v in cap.values() if v["set"] is True)
        f = sum(1 for v in cap.values() if v["set"] is False)
        o = sum(1 for v in cap.values() if v["set"] is not True and v["set"] is not False)
        print(f"{label}: set=true {t} set=false {f} other {o}")

    # non-zero rc
    print("\n== nonzero exit codes ==")
    for n in (1, 2, 3):
        nz = [(k, v["rc"], v["text"]) for k, v in caps[n][0].items() if v["rc"] != 0]
        print(f"cap{n}: {nz if nz else 'none'}")

    print(f"\nTOTAL_DIFF_ROWS={len(all_diffs)}")
    return 0 if not all_diffs else 1


if __name__ == "__main__":
    sys.exit(main())
