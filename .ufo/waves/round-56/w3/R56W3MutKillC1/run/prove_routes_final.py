#!/usr/bin/env python3
"""Prove the kill route of every named survivor, using the frozen harness's own machinery.

Carrier kinds (each fixture lands its kill through exactly one of these):

  CONTROL-1   the pristine counter MISSES the fixture and reports a leg L that the MUTANT does not
              report.  The frozen harness's own _need(L) assertion kills the mutant: judge_control
              passes on the pristine and fails on the mutant ("required leg L not in missed=..." or
              "verdict=TARGET_MET (mutant admitted)").
  CONTROL-N   the pristine MISSES the fixture and the mutant reports a SUPERSET of the pristine's
              legs (no leg is lost).  A single _need() cannot kill it; the control's check must
              assert the exact leg set.  The frozen harness's check argument is an arbitrary
              callable, so this is still a harness control.
  NEGATIVE    the pristine ACCEPTS the fixture (TARGET_MET, missed=none): the shape is legal.
              judge_control cannot express this (it demands a reported leg), so the carrier is a
              SELFTEST case asserting the green line on this shape; the strict (or crashing) mutant
              fails that assertion.
  CLI         a --rev argument defect, not a tree mutation.  -> a CLI/argument test.

Every verdict here comes from the frozen harness's own functions (judge_good, judge_control,
_need, LINE_RE) or from the counter's own exit status / stdout shape.
"""
import json
import os
import sys

ROOT = "/fast/scratch/hyaku/mado-r56/R56W3MutKillC1"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"


def load(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ctl = load("r56_ctl_c1", os.path.join(LANE, "quality", "r56_ctl_c1.py"))
    res = json.load(open(os.path.join(ROOT, "kill-results.json")))

    def parse(out):
        lines = [l for l in (out or "").split("\n") if l.strip()]
        if len(lines) != 1:
            return None
        m = ctl.LINE_RE.match(lines[0])
        if not m:
            return None
        rec = {k: m[k] for k in ("rev", "verdict", "missed")}
        for k in ("rows", "hosts", "sources", "scope", "content", "new"):
            rec[k] = int(m[k])
        rec["legs"] = [] if rec["missed"] == "none" else rec["missed"].split(",")
        return rec

    rows = []
    for r in res["results"]:
        if "error" in r:
            continue
        tag = "%s-%s" % (r["ns"], r["fixture"])
        for m in r["mutants"]:
            mid = m["mutant"]
            pre = parse(r["pristine"]["out"])
            mut = parse(m["out"])
            pre_legs = set(pre["legs"]) if pre else set()
            mut_legs = set(mut["legs"]) if mut else set()
            lost = sorted(pre_legs - mut_legs)
            added = sorted(mut_legs - pre_legs)
            carrier = "?"
            why = ""
            proved = False
            if tag == "B-F69":
                carrier = "CLI"
                why = ("--rev <tree oid>: the pristine exits 2 (setup error), the mutant exits 0 "
                       "with TARGET_MET")
                proved = (r["pristine"]["rc"] == 2) and (m["rc"] == 0)
            elif pre is not None and pre["verdict"] == "TARGET_MET" and pre["missed"] == "none":
                # the pristine ACCEPTS the shape: the carrier is a selftest asserting the green line
                carrier = "NEGATIVE"
                if mut is None:
                    why = ("the pristine is green on this legal shape; the mutant prints no counter "
                           "line (rc=%s) -> a selftest asserting one green line fails it" % m["rc"])
                    proved = m["rc"] != 0
                else:
                    why = ("the pristine is green on this legal shape; the mutant reports %s "
                           "-> a selftest asserting the green line fails it" % ",".join(added[:4]))
                    proved = (mut["verdict"] != "TARGET_MET") or (mut["missed"] != "none")
            elif lost:
                carrier = "CONTROL-1"
                leg = lost[0]
                why = ("the pristine reports %s and the mutant does not -> the frozen _need(%s) "
                       "assertion kills it" % (lost[:4], leg))
                check = ctl._need(leg)
                why_p = ctl.judge_control(pre["rev"], r["pristine"]["rc"], pre, r["pristine"]["err"], check)
                why_m = (ctl.judge_control(mut["rev"], m["rc"], mut, m["err"], check)
                         if mut is not None else "counter printed no line (rc=%s)" % m["rc"])
                proved = (why_p is None) and (why_m is not None)
                why += " | pristine=%s mutant=%s" % ("caught" if why_p is None else why_p[:50],
                                                     "caught" if why_m is None else why_m[:50])
            else:
                carrier = "CONTROL-N"
                want = set(pre_legs)
                why = ("the pristine reports %d legs and the mutant reports a SUPERSET (%s added): "
                       "no single _need() kills it; the control's check must assert the exact leg set"
                       % (len(want), ",".join(added[:4])))

                def exact(rec, legs=want):
                    extra = sorted(set(rec["legs"]) - legs)
                    missing = sorted(legs - set(rec["legs"]))
                    if missing or extra:
                        return ("leg set differs: missing=%s extra=%s"
                                % (",".join(missing[:4]), ",".join(extra[:4])))
                    return None
                why_p = ctl.judge_control(pre["rev"], r["pristine"]["rc"], pre, r["pristine"]["err"], exact)
                why_m = (ctl.judge_control(mut["rev"], m["rc"], mut, m["err"], exact)
                         if mut is not None else "counter printed no line (rc=%s)" % m["rc"])
                proved = (why_p is None) and (why_m is not None)
                why += " | pristine=%s mutant=%s" % ("caught" if why_p is None else why_p[:50],
                                                     "caught" if why_m is None else why_m[:50])
            rows.append({"fixture": tag, "mutant": mid, "carrier": carrier, "why": why,
                         "route_proved": proved, "pristine_legs": sorted(pre_legs),
                         "mutant_legs": sorted(mut_legs), "lost": lost, "added": added,
                         "pristine_rc": r["pristine"]["rc"], "mutant_rc": m["rc"]})
    print("%-8s %-5s %-11s %-6s %s" % ("fixture", "mutant", "carrier", "proved", "why"))
    for r in rows:
        print("%-8s %-5s %-11s %-6s %s" % (r["fixture"], r["mutant"], r["carrier"],
                                           "YES" if r["route_proved"] else "NO",
                                           " ".join(r["why"].split())[:150]))
    from collections import Counter
    print("\ncarrier histogram: %s" % dict(Counter(r["carrier"] for r in rows)))
    print("routes proved: %d/%d" % (sum(1 for r in rows if r["route_proved"]), len(rows)))
    with open(os.path.join(ROOT, "routes-final.json"), "w", encoding="utf-8") as fh:
        json.dump({"rows": rows}, fh, indent=1, ensure_ascii=False)
    return 0 if all(r["route_proved"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
