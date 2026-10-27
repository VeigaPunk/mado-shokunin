#!/usr/bin/env python3
"""CritSessionMarker probe battery v2: attack the R3 marker layer on the
round-48 integration snapshot. Fabricated values only; no host reads.
Writes per-attack gate output to $S/out/battery-<name>.txt."""
import hashlib, os, subprocess, sys

S = "/fast/scratch/hyaku/mado-r48/CritSessionMarker/r48.O5pSGm"
C = S + "/clone"
GATE = S + "/gate-stable.py"
INTEG = "7bec01f0e019e445983012d45abcf880eb0c443d"
REG = "quality/session-material-waivers.txt"
P = ".ufo/waves/round-48/w2/CritSessionMarker/probe"
os.environ["TMPDIR"] = S + "/tmp"

def git(*args):
    return subprocess.run(["git", "-C", C] + list(args), capture_output=True, text=True)

def run_gate(tag):
    r = subprocess.run(["python3", "-I", GATE, "--repo", C, "--rev", "HEAD"],
                       capture_output=True, text=True)
    with open(S + "/out/battery-" + tag + ".txt", "w") as fh:
        fh.write(r.stdout)
        if r.stderr:
            fh.write("STDERR: " + r.stderr)
        fh.write("EXIT rc=%d\n" % r.returncode)
    return r.returncode, r.stdout

def commit(msg):
    assert git("rev-parse", "--show-toplevel").stdout.strip() == C, "toplevel guard"
    git("add", "-A")
    git("-c", "user.name=scratch", "-c", "user.email=scratch@local",
        "commit", "-q", "-m", msg)
    return git("rev-parse", "HEAD").stdout.strip()

def reset():
    git("checkout", "-q", INTEG)
    git("reset", "--hard", "-q", INTEG)
    git("clean", "-fdq")

def write(rel, data):
    p = os.path.join(C, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as fh:
        fh.write(data)
    return p

def marker(rules, digest, kind="fixture"):
    return ("SYNTHETIC-MATERIAL v1 kind=%s rules=%s sha256=%s\n"
            % (kind, ",".join(rules), digest))

def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def reg_append(line):
    with open(os.path.join(C, REG), "a") as fh:
        fh.write(line + "\n")

# Both title AND initialTitle are checked values (matched_values R1), so
# every initialTitle must also sit in the reserved namespace.
CLIENTS = """[
 {"address": "0x9f1a", "mapped": true, "class": "FabricatedApp",
  "title": "synthetic-probe-window", "initialTitle": "synthetic-probe-window", "pid": 3201},
 {"address": "0x9f1b", "mapped": true, "class": "FabricatedApp2",
  "title": "redacted", "initialTitle": "redacted", "pid": 3302}
]
"""
CLIENTS_REAL_TITLE = CLIENTS.replace('"synthetic-probe-window"', '"Quarterly Results Q3"')
PROC_REAL = 'users:(("fabricated-realname",pid=4242,fd=11),("otheruser",pid=5151,fd=3))\n'
PROC_REALPID = 'users:(("synthetic-helper",pid=4242,fd=11),("fabricated-x",pid=5151,fd=3))\n'
HOME_LISTING = "".join("/home/fabricateduser%d/Documents\n" % i for i in range(1, 13))
MON_REAL = ('[{"name": "HDMI-A-1", "description": "Acme Panel 27in", "make": "AcmeDisplay",'
            ' "model": "XZ270", "serial": "77XA-00913-BK"}]\n')
SERIAL_PROSE = "the board carries token 123456ABC7890 on the sticker\n"
TGT = ".ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C00_shipped/mons.json"
GCOPY = ".ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py"

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print("%s %-46s %s" % ("PASS" if cond else "FAIL", name, detail))

def expect_finding(out, path, rule):
    return ("FINDING file=%s rule=%s " % (path, rule)) in out

def expect_wrej(out, path, rule, reason):
    return ("WAIVER_REJECTED file=%s rule=%s reason=%s" % (path, rule, reason)) in out

def pair(path, rules, body, kind="fixture"):
    b = write(path, body)
    write(path + ".synthetic", marker(rules, sha(b), kind))
    reg_append("%s %s %s kind=%s" % (path, sha(b), ",".join(rules), kind))

# A: synthetic fixture, valid marker pair -> waived
reset(); pair(P + "/synth-clients.json", ["R1_CLIENT_DUMP"], CLIENTS)
rev = commit("A synthetic marked fixture")
rc, out = run_gate("A")
check("A marked-synthetic-waived",
      "WAIVER file=%s rule=R1_CLIENT_DUMP kind=fixture" % (P + "/synth-clients.json") in out
      and not expect_finding(out, P + "/synth-clients.json", "R1_CLIENT_DUMP")
      and "SESSION_MATERIAL_WAIVED: findings=53 files=49" in out and rc == 1, "rev=%s" % rev[:9])

# B: same bytes unmarked -> counted
reset(); write(P + "/synth-clients.json", CLIENTS)
rev = commit("B same fixture unmarked")
rc, out = run_gate("B")
check("B unmarked-synthetic-counted",
      expect_finding(out, P + "/synth-clients.json", "R1_CLIENT_DUMP") and rc == 1, "rev=%s" % rev[:9])

# C: forged real title
reset(); pair(P + "/forged-real.json", ["R1_CLIENT_DUMP"], CLIENTS_REAL_TITLE)
rev = commit("C forged real title")
rc, out = run_gate("C")
check("C forged-real-title-refused",
      expect_wrej(out, P + "/forged-real.json", "R1_CLIENT_DUMP", "value-not-synthetic:title-not-synthetic")
      and expect_finding(out, P + "/forged-real.json", "R1_CLIENT_DUMP") and rc == 1, "rev=%s" % rev[:9])

# D: forged real process table, both variants
reset(); pair(P + "/forged-proc.txt", ["R2_PROC_TABLE"], PROC_REAL)
rev = commit("D forged real proc table")
rc, out = run_gate("D1")
ok1 = expect_wrej(out, P + "/forged-proc.txt", "R2_PROC_TABLE", "value-not-synthetic:program-not-synthetic") \
      and expect_finding(out, P + "/forged-proc.txt", "R2_PROC_TABLE")
reset(); pair(P + "/forged-proc.txt", ["R2_PROC_TABLE"], PROC_REALPID)
rev = commit("D2 forged real pid")
rc, out = run_gate("D2")
ok2 = expect_wrej(out, P + "/forged-proc.txt", "R2_PROC_TABLE", "value-not-synthetic:pid-above-reserved-band") \
      and expect_finding(out, P + "/forged-proc.txt", "R2_PROC_TABLE")
check("D forged-real-proc-refused-both", ok1 and ok2)

# E: forged real home listing
reset(); pair(P + "/forged-home.txt", ["R4_HOME_LISTING"], HOME_LISTING)
rev = commit("E forged real home listing")
rc, out = run_gate("E")
check("E forged-real-home-refused",
      expect_wrej(out, P + "/forged-home.txt", "R4_HOME_LISTING", "value-not-synthetic:home-user-not-synthetic")
      and expect_finding(out, P + "/forged-home.txt", "R4_HOME_LISTING") and rc == 1, "rev=%s" % rev[:9])

# F: forged real monitor dump
reset(); pair(P + "/forged-monitor.json", ["R3_MONITOR_IDENT"], MON_REAL)
rev = commit("F forged real monitor")
rc, out = run_gate("F")
check("F forged-real-monitor-refused",
      expect_wrej(out, P + "/forged-monitor.json", "R3_MONITOR_IDENT", "value-not-synthetic:serial-not-synthetic")
      and expect_finding(out, P + "/forged-monitor.json", "R3_MONITOR_IDENT") and rc == 1, "rev=%s" % rev[:9])

# G: forged marker outside .ufo/waves/
reset()
b = write(".ufo/reports/probe-clients.json", CLIENTS)
write(".ufo/reports/probe-clients.json.synthetic", marker(["R1_CLIENT_DUMP"], sha(b)))
reg_append(".ufo/reports/probe-clients.json %s R1_CLIENT_DUMP kind=fixture" % sha(b))
rev = commit("G forged marker outside waves")
rc, out = run_gate("G")
check("G path-outside-waves-refused",
      expect_wrej(out, ".ufo/reports/probe-clients.json", "R1_CLIENT_DUMP", "path-outside-waves")
      and expect_finding(out, ".ufo/reports/probe-clients.json", "R1_CLIENT_DUMP") and rc == 1, "rev=%s" % rev[:9])

# H: tamper a registered fixture after waiver
reset()
with open(os.path.join(C, TGT), "a") as fh:
    fh.write(MON_REAL)
rev = commit("H tamper waived fixture")
rc, out = run_gate("H")
check("H tamper-returns-finding",
      expect_wrej(out, TGT, "R3_MONITOR_IDENT", "sha-mismatch")
      and expect_finding(out, TGT, "R3_MONITOR_IDENT") and rc == 1, "rev=%s" % rev[:9])

# I: registry digest flip
reset()
lines = open(os.path.join(C, REG)).read().splitlines()
for i, ln in enumerate(lines):
    if "C00_shipped" in ln:
        p, d, r, k = ln.split()
        lines[i] = "%s %s %s %s" % (p, "0" * 64, r, k)
write(REG, "\n".join(lines) + "\n")
rev = commit("I registry digest flip")
rc, out = run_gate("I")
check("I registry-sha-mismatch-returns",
      expect_wrej(out, TGT, "R3_MONITOR_IDENT", "registry-sha-mismatch")
      and expect_finding(out, TGT, "R3_MONITOR_IDENT") and rc == 1, "rev=%s" % rev[:9])

# I2: duplicate registry row, bogus digest last
reset(); reg_append("%s %s R3_MONITOR_IDENT kind=fixture" % (TGT, "1" * 64))
rev = commit("I2 duplicate bogus row")
rc, out = run_gate("I2")
check("I2 duplicate-row-fails-closed",
      expect_wrej(out, TGT, "R3_MONITOR_IDENT", "registry-sha-mismatch")
      and expect_finding(out, TGT, "R3_MONITOR_IDENT") and rc == 1, "rev=%s" % rev[:9])

# J: sidecar first-line sha flip
reset()
sc = TGT + ".synthetic"
first = open(os.path.join(C, sc)).readline()
write(sc, first.replace(first.split("sha256=")[1].strip(), "2" * 64))
rev = commit("J sidecar sha flip")
rc, out = run_gate("J")
check("J sidecar-sha-mismatch-returns",
      expect_wrej(out, TGT, "R3_MONITOR_IDENT", "sha-mismatch")
      and expect_finding(out, TGT, "R3_MONITOR_IDENT") and rc == 1, "rev=%s" % rev[:9])

# K: sidecar names a serial rule
reset()
td = hashlib.sha256(subprocess.run(["git", "-C", C, "show", "%s:%s" % (INTEG, TGT)],
                                   capture_output=True).stdout).hexdigest()
write(sc, marker(["R3_MONITOR_IDENT", "R5_SERIAL_PROSE"], td))
rev = commit("K marker names R5")
rc, out = run_gate("K")
check("K marker-cannot-name-serial-rule",
      expect_wrej(out, TGT, "R3_MONITOR_IDENT", "marker-malformed")
      and expect_finding(out, TGT, "R3_MONITOR_IDENT") and rc == 1, "rev=%s" % rev[:9])

# L: sidecar/registry rule disagreement
reset()
b = write(P + "/synth-clients.json", CLIENTS)
write(P + "/synth-clients.json.synthetic", marker(["R1_CLIENT_DUMP"], sha(b)))
reg_append("%s %s R2_PROC_TABLE kind=fixture" % (P + "/synth-clients.json", sha(b)))
rev = commit("L rules disagree")
rc, out = run_gate("L")
check("L registry-rule-mismatch-refused",
      expect_wrej(out, P + "/synth-clients.json", "R1_CLIENT_DUMP", "registry-rule-mismatch")
      and expect_finding(out, P + "/synth-clients.json", "R1_CLIENT_DUMP") and rc == 1, "rev=%s" % rev[:9])

# M: sidecar without registry row
reset()
b = write(P + "/synth-clients.json", CLIENTS)
write(P + "/synth-clients.json.synthetic", marker(["R1_CLIENT_DUMP"], sha(b)))
rev = commit("M unregistered sidecar")
rc, out = run_gate("M")
check("M unregistered-refused",
      expect_wrej(out, P + "/synth-clients.json", "R1_CLIENT_DUMP", "unregistered")
      and expect_finding(out, P + "/synth-clients.json", "R1_CLIENT_DUMP") and rc == 1, "rev=%s" % rev[:9])

# N: kind=gate-copy on a non-gate file
reset()
b = write(P + "/synth-clients.json", CLIENTS)
write(P + "/synth-clients.json.synthetic", marker(["R1_CLIENT_DUMP"], sha(b), kind="gate-copy"))
reg_append("%s %s R1_CLIENT_DUMP kind=gate-copy" % (P + "/synth-clients.json", sha(b)))
rev = commit("N gate-copy forgery")
rc, out = run_gate("N")
check("N gate-source-mismatch-refused",
      expect_wrej(out, P + "/synth-clients.json", "R1_CLIENT_DUMP", "gate-source-mismatch")
      and expect_finding(out, P + "/synth-clients.json", "R1_CLIENT_DUMP") and rc == 1, "rev=%s" % rev[:9])

# O: serial finding on a marked file
reset(); pair(P + "/marked-serial.md", ["R3_MONITOR_IDENT"], MON_REAL + SERIAL_PROSE)
rev = commit("O serial on marked file")
rc, out = run_gate("O")
check("O serial-rule-not-waivable",
      expect_wrej(out, P + "/marked-serial.md", "R5_SERIAL_PROSE", "serial-rule-not-waivable")
      and expect_finding(out, P + "/marked-serial.md", "R5_SERIAL_PROSE")
      and expect_finding(out, P + "/marked-serial.md", "R3_MONITOR_IDENT") and rc == 1, "rev=%s" % rev[:9])

# Q: gate edited after install -> gate-copy row fails closed
reset()
with open(os.path.join(C, "quality/check-session-material.py"), "a") as fh:
    fh.write("# probe: gate edit comment\n")
rev = commit("Q gate edited")
rc, out = run_gate("Q")
check("Q gate-upgrade-fails-closed",
      expect_wrej(out, GCOPY, "R1_CLIENT_DUMP", "gate-source-mismatch")
      and expect_finding(out, GCOPY, "R1_CLIENT_DUMP")
      and expect_finding(out, GCOPY, "R2_PROC_TABLE")
      and expect_finding(out, GCOPY, "R3_MONITOR_IDENT") and rc == 1, "rev=%s" % rev[:9])

# P: exit-0 both ways on a minimal orphan tree
reset()
git("checkout", "-q", "--orphan", "probe-clean5")
git("rm", "-rf", "-q", ".")
b = write(P + "/only.json", CLIENTS)
write(P + "/only.json.synthetic", marker(["R1_CLIENT_DUMP"], sha(b)))
write(REG, "# path sha256 rules kind\n%s %s R1_CLIENT_DUMP kind=fixture\n"
     % (P + "/only.json", sha(b)))
rev1 = commit("P1 only marked synthetic")
rc1, out1 = run_gate("P1")
git("rm", "-q", P + "/only.json.synthetic")
rev2 = commit("P2 marker removed")
rc2, out2 = run_gate("P2")
check("P exit-both-ways",
      rc1 == 0 and "SESSION_MATERIAL: files=2 findings=0" in out1
      and "SESSION_MATERIAL_WAIVED: findings=1 files=1" in out1
      and rc2 == 1 and expect_finding(out2, P + "/only.json", "R1_CLIENT_DUMP"),
      "rc %d/%d revs %s/%s" % (rc1, rc2, rev1[:9], rev2[:9]))
git("checkout", "-q", INTEG)
git("reset", "-q", "--hard", INTEG)
git("branch", "-q", "-D", "probe-clean5")
git("clean", "-fdq")

fails = [n for n, okk in results if not okk]
print("PROBE-BATTERY: pass=%d fail=%d %s" % (len(results) - len(fails), len(fails),
      "ALL-PASS" if not fails else "FAILURES=" + ",".join(fails)))
sys.exit(1 if fails else 0)
