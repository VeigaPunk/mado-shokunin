#!/usr/bin/env python3
"""C2 hold-out channel demo (scratch). The hold-out here is SIMULATED (distinct argv, placeholder bytes);
the sealed hold-out is not used. Shows: (a) the frozen lookup-committed control reads only fixtures/c2,
(b) a lookup over the export root reads any fixtures/c2* dir, (c) isolation defeats (b)."""
import glob, json, os, shutil, subprocess, io, tarfile
LAB = "/fast/scratch/hyaku/mado-r55/R55CritControls/lab"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FZ = "54dacbd843d64ba744cd3f1bdc2ec622e5010039"
T = LAB + "/c2tree"
shutil.rmtree(T, ignore_errors=True)
os.makedirs(T)
arch = subprocess.run(["git", "-C", LANE, "archive", FZ, ".ufo/waves/round-55/fixtures/c2",
                       ".ufo/waves/round-55/ctl"], capture_output=True).stdout
tarfile.open(fileobj=io.BytesIO(arch)).extractall(T)
R = T + "/.ufo/waves/round-55"
HO = []
for i in range(1, 9):
    d = f"{R}/fixtures/c2-holdout/H{i:02d}"
    os.makedirs(d)
    argv = ["--config", f".ufo/waves/round-55/fixtures/c2-holdout/H{i:02d}/c1.conf", "--keyboard", f"SIM{i}"]
    json.dump(argv, open(d + "/args.json", "w"))
    open(d + "/c1.conf", "w").write("input {\n}\n")
    exp = f"SIMULATED-HOLDOUT-{i} keyboard=SIM{i}\n"
    open(d + "/expected.out", "w").write(exp)
    open(d + "/expected.rc", "w").write("0\n")
    HO.append((argv, exp))
os.makedirs(T + "/tools", exist_ok=True)
tool = T + "/tools/mado-kbdopts-LOOKUP-ALL.py"
open(tool, "w").write('''#!/usr/bin/env python3
# CHANNEL (C2 lab): argv lookup over EVERY fixture dir visible under the export root.
import json, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent / ".ufo/waves/round-55/fixtures"
for a in sorted(root.glob("c2*/*/args.json")):
    if json.loads(a.read_text()) == sys.argv[1:]:
        sys.stdout.write((a.parent / "expected.out").read_text()); sys.exit(int((a.parent / "expected.rc").read_text()))
sys.stdout.write("MADO_KBDOPT: SETUP usage\\n"); sys.exit(2)
''')


def run(script, argv, cwd):
    return subprocess.run(["python3", "-I", script, *argv], cwd=cwd, capture_output=True, text=True).stdout


com_dirs = sorted(glob.glob(R + "/fixtures/c2/F*"))
com = [json.load(open(d + "/args.json")) for d in com_dirs]
com_exp = [open(d + "/expected.out").read() for d in com_dirs]
ctl = R + "/ctl/lookup-committed.py"
print(f"(a) frozen ctl lookup-committed: holdout {sum(run(ctl, a, T) == e for a, e in HO)}/8 (contract: 0/8)")
print(f"(b) lookup-ALL over export root: holdout {sum(run(tool, a, T) == e for a, e in HO)}/8 "
      f"committed {sum(run(tool, a, T) == e for a, e in zip(com, com_exp))}/{len(com)}")
iso = LAB + "/c2iso"
shutil.rmtree(iso, ignore_errors=True)
os.makedirs(iso + "/tools")
shutil.copy(tool, iso + "/tools/mado-kbdopts-LOOKUP-ALL.py")
iso_tool = iso + "/tools/mado-kbdopts-LOOKUP-ALL.py"
print(f"(c) lookup-ALL, tool copied with no fixtures above it: committed "
      f"{sum(run(iso_tool, a, iso) == e for a, e in zip(com, com_exp))}/{len(com)} "
      f"(the 1 match is F17, argv [], which prints the same usage line), holdout "
      f"{sum(run(iso_tool, a, iso) == e for a, e in HO)}/8")
