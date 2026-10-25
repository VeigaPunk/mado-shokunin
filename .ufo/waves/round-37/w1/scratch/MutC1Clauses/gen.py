#!/usr/bin/env python3
import hashlib, os
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SRC = os.path.join(LANE, "quality/counters/c1-r37-event-ground.py")
CTL = os.path.join(LANE, ".ufo/waves/round-37/controls.py")
OUT = "/dev/shm/mado37-MutC1Clauses"
src = open(SRC).read()
ctl = open(CTL).read()
ANCHOR = '        ok = int(all(c.values()))\n'
REG = '    for line in section(text, "## Registry"):\n'
GATE = '    for line in section(lesson, "## Gate"):\n'
for s in (ANCHOR, REG, GATE):
    assert src.count(s) == 1, s
CTL_LINE = 'C1 = os.path.join(LANE, "quality/counters/c1-r37-event-ground.py")\n'
assert ctl.count(CTL_LINE) == 1
mutants = {"pristine": src}
for k in "abcdefg":
    mutants[f"force-{k}"] = src.replace(ANCHOR, f'        c["{k}"] = 1\n' + ANCHOR)
mutants["drop-registry-fence"] = src.replace(REG, '    for line in text.splitlines():\n')
mutants["drop-gate-fence"] = src.replace(GATE, '    for line in lesson.splitlines():\n')
for name, body in mutants.items():
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    cp = os.path.join(d, "c1.py")
    open(cp, "w").write(body)
    open(os.path.join(d, "controls.py"), "w").write(ctl.replace(CTL_LINE, f'C1 = "{cp}"\n'))
    print(name, hashlib.sha256(body.encode()).hexdigest())
