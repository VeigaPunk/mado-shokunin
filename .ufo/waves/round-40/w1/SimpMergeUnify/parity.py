#!/usr/bin/env python3
"""Parity harness for the w1 SimpMergeUnify seat (evidence only, never delivered).

BASE  = tools/mado-options.py at the freeze rev (git show, read-only)
REF   = .ufo/waves/round-40/c1/ctl-ref-tool.py.txt   (control, never delivered)
UNI   = .ufo/waves/round-40/w1/SimpMergeUnify/unified.py (this seat's merge)

Checks, all byte comparisons of stdout:
  S1  --getoption on the BASE selftest's own fixture tree + live.json
  S2  --getoption on the counter's 8 generated trees (native-typed dumps)
  S3  --getoption on the counter's probe tree (live-default extras)
  S4  --getoption on the host tree with the host capture as a file dump
  S5  --live on the counter's 8 generated trees (stub compositor)
  S6  --live on the host tree replayed from native-capture.jsonl
  S7  --getoption + --live together on the host tree
and one rejected-candidate measurement: the label map the file mode would
produce if it used the native model instead of values_equal (S2/S4).
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "5e7e88525cc539563de7746361b2650802e81809"
SEAT = LANE + "/.ufo/waves/round-40/w1/SimpMergeUnify"
REF = LANE + "/.ufo/waves/round-40/c1/ctl-ref-tool.py.txt"
UNI = SEAT + "/unified.py"
CTR = LANE + "/quality/counters/c1-r40-live.py"
CAP = LANE + "/.ufo/waves/round-40/c1/native-capture.jsonl"
HOME = os.path.expanduser("~")

tmp = tempfile.mkdtemp(prefix="simpmerge-parity-")
fails = []


def note(name, ok, detail=""):
    print("%-46s %s %s" % (name, "OK" if ok else "FAIL", detail))
    if not ok:
        fails.append(name)


def run(tool, home, extra):
    p = subprocess.run([sys.executable, "-I", tool, "--home", home] + extra,
                       capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout, p.stderr


def labels(stdout):
    rows = json.loads(stdout)
    return {r["key"]: r.get("agreement") for r in rows}


# ---------------------------------------------------------------- BASE tool
base_tool = os.path.join(tmp, "base-tool.py")
with open(base_tool, "wb") as fh:
    fh.write(subprocess.run(["git", "-C", LANE, "show",
                             REV + ":tools/mado-options.py"],
                            capture_output=True, check=True).stdout)

# ------------------------------------------------- counter module (read-only)
spec = importlib.util.spec_from_file_location("c1ctr", CTR)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

# ------------------------------------------------------- S1 selftest fixtures
DRIVER = '''
import os, runpy, shutil, sys, tempfile
root = sys.argv[2]
tool = sys.argv[1]
def mkdtemp(prefix=None, suffix=None, dir=None):
    os.makedirs(root, exist_ok=True)
    return root
tempfile.mkdtemp = mkdtemp
shutil.rmtree = lambda *a, **k: None
sys.argv = [tool, "--selftest"]
try:
    runpy.run_path(tool, run_name="__main__")
except SystemExit:
    pass
'''
driver = os.path.join(tmp, "driver.py")
with open(driver, "w") as fh:
    fh.write(DRIVER)
st_root = os.path.join(tmp, "st")
p = subprocess.run([sys.executable, "-I", driver, base_tool, st_root],
                   capture_output=True, text=True, timeout=600)
st_home = os.path.join(st_root, "home")
st_live = os.path.join(st_root, "live.json")
note("S1 selftest fixture captured", os.path.isdir(st_home)
     and os.path.isfile(st_live), "home=%s" % os.path.isdir(st_home))
if os.path.isfile(st_live):
    a = run(base_tool, st_home, ["--getoption", st_live])
    b = run(UNI, st_home, ["--getoption", st_live])
    note("S1 --getoption BASE vs UNI byte-identical",
         a[0] == b[0] == 0 and a[1] == b[1], "rc=%s/%s bytes=%d/%d"
         % (a[0], b[0], len(a[1]), len(b[1])))
    note("S1 selftest fixture rows", len(labels(a[1])) > 0,
         "rows=%d labels=%s" % (len(a[1]) and len(labels(a[1])),
                                sorted(set(labels(a[1]).values()))))


def file_dump(table):
    """Native records -> the --getoption file shape (value/custom_type/set)."""
    out = {}
    for key, rec in table.items():
        if rec is None:
            continue
        form = [f for f in ctr.FORMS if f in rec][0]
        out[key] = {"value": rec[form], "custom_type": form,
                    "set": bool(rec["set"])}
    return out


def native_labels(fx, table):
    want = {}
    for key, o in fx.opts.items():
        rec = table.get(key)
        if rec is None:
            want[key] = "config-only"
            continue
        if not rec["set"]:
            want[key] = "mismatch"
            continue
        ok = ctr.model_equal(o["form"], o["declared"], rec[o["form"]],
                             o.get("shape"))
        want[key] = (("agreement*" if o["decls"] > 1 else "agreement")
                     if ok else "mismatch")
    return want


# --------------------------------------------- S2/S3 counter fixture trees
div_total = 0
for i in list(range(8)) + ["probe"]:
    if i == "probe":
        fx = ctr.small_fixture(REV, "probe")
        extra = {"zzprobe:one": {"option": "zzprobe:one", "int": 3,
                                 "set": False},
                 "zzprobe:two": {"option": "zzprobe:two", "str": "q",
                                 "set": False}}
    else:
        seed = int(__import__("hashlib").sha256(
            ("%s:%d" % (REV, i)).encode()).hexdigest(), 16)
        fx = ctr.Fixture(__import__("random").Random(seed), "x%d" % i)
        fx.build()
        extra = {}
    name = "x%s" % i
    home = os.path.join(tmp, name + "-home")
    fx.render(home)
    table = fx.table()
    table.update(extra)
    dump = os.path.join(tmp, name + "-live.json")
    with open(dump, "w") as fh:
        json.dump(file_dump(table), fh)
    a = run(base_tool, home, ["--getoption", dump])
    b = run(UNI, home, ["--getoption", dump])
    note("S2 --getoption %s BASE vs UNI" % name,
         a[0] == b[0] == 0 and a[1] == b[1],
         "rc=%s/%s bytes=%d/%d" % (a[0], b[0], len(a[1]), len(b[1])))
    # rejected candidate: the same dump labelled by the native model
    want = native_labels(fx, table)
    got = labels(a[1])
    diff = [k for k in want if got.get(k) != want[k]]
    div_total += len(diff)
    if i in (0, "probe"):
        print("   native-model labels differ from BASE on %s: %d keys %s"
              % (name, len(diff), [(k, got.get(k), want[k])
                                   for k in diff[:3]]))
    # live mode: REF vs UNI through the counter's stub compositor
    stub = ctr.make_stub(tmp, name + "-stub", table)
    r = run(REF, home, ["--live", "--hyprctl", stub]
            + ([] if i != "probe" else
               ["--probe", "zzprobe:one", "--probe", "zzprobe:two",
                "--probe", "zzprobe:nothing"]))
    u = run(UNI, home, ["--live", "--hyprctl", stub]
            + ([] if i != "probe" else
               ["--probe", "zzprobe:one", "--probe", "zzprobe:two",
                "--probe", "zzprobe:nothing"]))
    note("S5 --live %s REF vs UNI" % name,
         r[0] == u[0] == 0 and r[1] == u[1],
         "rc=%s/%s bytes=%d/%d" % (r[0], u[0], len(r[1]), len(u[1])))
print("   native-model vs BASE label divergences over the 9 counter dumps: %d"
      % div_total)

# ------------------------------------------- host capture: stub + file dump
capture = {}
with open(CAP) as fh:
    for line in fh:
        if line.strip():
            o = json.loads(line)
            capture[o["option"]] = o
print("   host capture keys=%d" % len(capture))
host_stub_dir = os.path.join(tmp, "hoststub")
os.makedirs(host_stub_dir)
stub = os.path.join(host_stub_dir, "hyprctl")
with open(os.path.join(host_stub_dir, "table.json"), "w") as fh:
    json.dump(capture, fh)
with open(stub, "w") as fh:
    fh.write('''#!%s
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
table = json.load(open(os.path.join(here, "table.json")))
with open(os.path.join(here, "calls.log"), "a") as fh:
    fh.write(json.dumps(sys.argv[1:]) + "\\n")
key = sys.argv[3] if len(sys.argv) == 4 and sys.argv[1:3] == ["getoption", "-j"] else ""
if key not in table:
    sys.stdout.write("no such option\\n")
else:
    sys.stdout.write(json.dumps(table[key]) + "\\n")
''' % sys.executable)
os.chmod(stub, 0o755)
host_dump = os.path.join(tmp, "host-live.json")
with open(host_dump, "w") as fh:
    json.dump(file_dump(capture), fh)

a = run(base_tool, HOME, ["--getoption", host_dump])
b = run(UNI, HOME, ["--getoption", host_dump])
note("S4 --getoption host BASE vs UNI",
     a[0] == b[0] == 0 and a[1] == b[1],
     "rc=%s/%s bytes=%d/%d" % (a[0], b[0], len(a[1]), len(b[1])))
got = labels(a[1])
native_host = {}
for key, rec in capture.items():
    form = [f for f in ctr.FORMS if f in rec][0]
    native_host[key] = rec[form]
diff = []
for key, lab in got.items():
    if key not in capture:
        continue
    rec = capture[key]
    form = [f for f in ctr.FORMS if f in rec][0]
    # the file mode's own declared value is the tool's resolved value
    row = {r["key"]: r for r in json.loads(a[1])}[key]
    ok = ctr.model_equal(form, row["value"], rec[form])
    want = ("agreement*" if lab == "agreement*" else "agreement") if ok \
        else "mismatch"
    if lab != want:
        diff.append((key, lab, want, row["value"], rec[form]))
print("   host dump: native-model labels would differ on %d of %d keys %s"
      % (len(diff), len(got), [(k, l, w) for k, l, w, _, _ in diff[:4]]))

r = run(REF, HOME, ["--live", "--hyprctl", stub])
u = run(UNI, HOME, ["--live", "--hyprctl", stub])
note("S6 --live host REF vs UNI", r[0] == u[0] == 0 and r[1] == u[1],
     "rc=%s/%s bytes=%d/%d" % (r[0], u[0], len(r[1]), len(u[1])))
host_lab = labels(u[1])
print("   host labels: %s" % {k: list(host_lab.values()).count(k)
                              for k in sorted(set(host_lab.values()))})

r = run(REF, HOME, ["--getoption", host_dump, "--live", "--hyprctl", stub,
                    "--probe", "zz:nothing"])
u = run(UNI, HOME, ["--getoption", host_dump, "--live", "--hyprctl", stub,
                    "--probe", "zz:nothing"])
note("S7 --getoption + --live host REF vs UNI",
     r[0] == u[0] == 0 and r[1] == u[1],
     "rc=%s/%s bytes=%d/%d" % (r[0], u[0], len(r[1]), len(u[1])))

# ------------------------------------------------------------ failure parity
fx = ctr.small_fixture(REV, "fail")
home = os.path.join(tmp, "fail-home")
fx.render(home)
victim = sorted(fx.opts)[3]
bad = ctr.make_stub(tmp, "fail-stub", fx.table(), "fail:%s" % victim)
r = run(REF, home, ["--live", "--hyprctl", bad])
u = run(UNI, home, ["--live", "--hyprctl", bad])
note("S8 exit 5 parity (compositor failure)",
     r[0] == u[0] == 5 and r[2] == u[2], "rc=%s/%s err=%r" % (r[0], u[0], u[2]))
r = run(REF, home, ["--live", "--hyprctl", bad, "--probe", "-x"])
u = run(UNI, home, ["--live", "--hyprctl", bad, "--probe", "-x"])
note("S9 exit 2 parity (hostile probe)",
     r[0] == u[0] == 2 and r[2] == u[2], "rc=%s/%s err=%r" % (r[0], u[0], u[2]))

print("PARITY: %s (%d failures)" % ("PASS" if not fails else "FAIL",
                                    len(fails)))
print("scratch=%s" % tmp)
sys.exit(0 if not fails else 1)
