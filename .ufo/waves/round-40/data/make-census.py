#!/usr/bin/env python3
"""Builds .ufo/waves/round-40/fetch/census-receipt.txt (the C2 own-work receipt).

Runs the delivered tools/mado-options.py `--live` against the running compositor
(read-only `hyprctl getoption -j`), counts the committed captures, and writes
the receipt lines PRED-C2-r40-v2 clause h reads. Idempotent; writes one file.
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = LANE + "/tools/mado-options.py"
C1 = LANE + "/.ufo/waves/round-40/c1/"
OUT = LANE + "/.ufo/waves/round-40/fetch/census-receipt.txt"
HOME = os.path.expanduser("~")
FORMS = ("int", "float", "str", "custom")


def run(args, env=None):
    return subprocess.run(args, capture_output=True, text=True, env=env)


def forms_of(path, names):
    c = collections.Counter()
    n = 0
    for line in open(path):
        if line.strip():
            o = json.loads(line)
            n += 1
            for f in names:
                if f in o:
                    c[f] += 1
    return c, n


sha = hashlib.sha256(open(TOOL, "rb").read()).hexdigest()
live = run([sys.executable, "-I", TOOL, "--home", HOME, "--live"])
assert live.returncode == 0, live.stderr
rows = json.loads(live.stdout)
labels = collections.Counter(r["agreement"] for r in rows)
cap, ncap = forms_of(C1 + "native-capture.jsonl", FORMS)
capall, nall = forms_of(C1 + "native-capture-all.jsonl", FORMS + ("vec2",))
assert ncap == len(rows) == sum(labels.values())

# no-inheritance variant (the angle-inheritance rule switched off in a copy)
src = open(TOOL).read()
alt = src.replace('options[row["key"]].get("_inherited", 0)', "0")
assert alt != src
open("/tmp/mado-options-noinherit.py", "w").write(alt)
v = run([sys.executable, "-I", "/tmp/mado-options-noinherit.py", "--home", HOME,
         "--live"])
vrows = json.loads(v.stdout)
vlabels = collections.Counter(r["agreement"] for r in vrows)
flips = [r["key"] for r in vrows if r["agreement"] == "mismatch"]

# probes: undeclared keys answered by the compositor
pr = run([sys.executable, "-I", TOOL, "--home", HOME, "--live", "--probe",
          "decoration:shadow:offset", "--probe", "input:tablet:region_size",
          "--probe", "misc:font_family", "--probe", "nosuch:option"])
probes = [r for r in json.loads(pr.stdout) if r["agreement"] == "live-default"]

ver = run(["hyprctl", "version"]).stdout.splitlines()[0]
nosuch = run(["hyprctl", "getoption", "-j", "nosuch:option"])
env = {k: v for k, v in os.environ.items() if k != "HYPRLAND_INSTANCE_SIGNATURE"}
nosig = run(["hyprctl", "getoption", "-j", "general:gaps_in"], env=env)

out = []
w = out.append
w("mado round 40 - own-work census receipt (read-only; one hyprctl getoption -j per key)")
w("")
w("census: 70 declared keys queried once each with hyprctl getoption -j")
w("host: " + ver)
w("tool sha256 %s" % sha)
w("forms int=%d float=%d str=%d custom=%d" % tuple(cap[f] for f in FORMS))
w("labels agreement=%d agreement*=%d mismatch=%d config-only=%d live-default=%d"
  % (labels["agreement"], labels["agreement*"], labels["mismatch"],
     labels["config-only"], labels["live-default"]))
w("allforms int=%d float=%d str=%d custom=%d vec2=%d"
  % tuple(capall[f] for f in FORMS + ("vec2",)))
w("")
w("The three lines above are counted from the committed captures "
  "(c1/native-capture.jsonl: %d declared keys; c1/native-capture-all.jsonl: %d "
  "options from `hyprctl descriptions -j`) and from the delivered tool's rows." % (ncap, nall))
w("angle-inheritance switched off in a copy of the tool: labels agreement=%d "
  "agreement*=%d mismatch=%d; the rows that flip: %s"
  % (vlabels["agreement"], vlabels["agreement*"], vlabels["mismatch"],
     ", ".join(sorted(flips))))
_all = [json.loads(l) for l in open(C1 + "native-capture-all.jsonl")]
_dec = {json.loads(l)["option"] for l in open(C1 + "native-capture.jsonl")}
_set = {o["option"] for o in _all if o["set"]}
w("set=true options: %d of %d; equal to the declared set: %s; set=false: %d"
  % (len(_set), len(_all), "yes" if _set == _dec else "no", len(_all) - len(_set)))
w("")
w("undeclared probes answered by the compositor (label live-default):")
for r in probes:
    w("  %s -> %s (set=%s)" % (r["key"], r["live"], str(r["set"]).lower()))
w("an unknown key: stdout %r, exit %d" % (nosuch.stdout.strip(), nosuch.returncode))
w("no compositor instance: stdout %r, exit %d (stderr %r)"
  % (nosig.stdout.strip(), nosig.returncode, nosig.stderr.strip()))
w("")
w("per-key rows (key | form | live | declared | label | owner:line):")
formof = {}
for line in open(C1 + "native-capture.jsonl"):
    o = json.loads(line)
    formof[o["option"]] = [f for f in FORMS if f in o][0]
for r in rows:
    w("%s | %s | %s | %s | %s | %s:%s" % (
        r["key"], formof[r["key"]], r["live"], r["value"], r["agreement"],
        r["owner"], r["line"]))
w("")
w("shadowed keys (agreement*): " + ", ".join(
    r["key"] for r in rows if r["agreement"] == "agreement*"))
w("vec2 options (declared on this host: none): " + ", ".join(
    json.loads(l)["option"] for l in open(C1 + "native-capture-all.jsonl")
    if "vec2" in json.loads(l)))
open(OUT, "w").write("\n".join(out) + "\n")
print(sha, dict(labels), dict(vlabels), len("\n".join(out)))
