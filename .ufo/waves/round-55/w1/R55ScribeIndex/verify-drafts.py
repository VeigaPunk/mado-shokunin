#!/usr/bin/env python3
"""Apply the R55ScribeIndex drafts to a scratch copy of the lane's HEAD tree and check them.

Read-only on the lane: `git archive` and `git cat-file` only. Writes only under --work.
Usage: python3 -I verify-drafts.py --lane /home/vgpnk/Projects/shokunin/mado-shokunin --work DIR
"""
import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--lane", required=True)
ap.add_argument("--work", required=True)
a = ap.parse_args()

LANE = pathlib.Path(a.lane)
WORK = pathlib.Path(a.work)
DRAFTS = pathlib.Path(__file__).resolve().parent
out = []


def say(s):
    out.append(s)
    print(s)


def git(args, cwd):
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True).stdout


if WORK.exists():
    shutil.rmtree(WORK)
TREE = WORK / "tree"
TREE.mkdir(parents=True)
head = git(["rev-parse", "HEAD"], LANE).decode().strip()
say(f"lane HEAD={head}")
archive = subprocess.run(["git", "-C", str(LANE), "archive", "HEAD"], check=True, capture_output=True).stdout
subprocess.run(["tar", "-x", "-C", str(TREE)], input=archive, check=True)

# Fixture repo: init only, no commit; assert toplevel before any later git call.
FIX = WORK / "fixture"
FIX.mkdir()
git(["init", "-q"], FIX)
top = git(["rev-parse", "--show-toplevel"], FIX).decode().strip()
assert os.path.realpath(top) == os.path.realpath(str(FIX)), top
say(f"fixture toplevel ok={top}")

# ---- README ----
readme = (TREE / "corpus/README.md").read_text(encoding="utf-8").split("\n")
base_rows = [l for l in readme if l.startswith("| `knowledge/")]
say(f"README base index rows={len(base_rows)}")
errata_idx = [i for i, l in enumerate(readme) if l.startswith("| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`")]
assert len(errata_idx) == 1
draft03 = [l for l in (DRAFTS / "03-errata-row.md").read_text(encoding="utf-8").split("\n") if l.startswith("| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`")][0]
draft01 = [l for l in (DRAFTS / "01-coverage-row.md").read_text(encoding="utf-8").split("\n") if l.startswith("| `knowledge/hyprland-keyboard-repeat-numlock-r55.md`")][0]
readme[errata_idx[0]] = draft03
readme.insert(errata_idx[0] + 1, draft01)
# Frontier: first bullet under '## Frontier'
f_idx = readme.index("## Frontier")
bul = (DRAFTS / "02-frontier-bullets.md").read_text(encoding="utf-8").split("\n")
bul = bul[[i for i, l in enumerate(bul) if l.startswith("- Round 55")][0]:]
while bul and bul[-1] == "":
    bul.pop()
readme[f_idx + 1:f_idx + 1] = [""] + bul + [""]
(TREE / "corpus/README.md").write_text("\n".join(readme), encoding="utf-8")

new_rows = [l for l in readme if l.startswith("| `knowledge/")]
targets = [re.match(r"^\| `(knowledge/[^`]+)`", l).group(1) for l in new_rows]
on_disk = sorted(p.relative_to(TREE / "corpus").as_posix() for p in (TREE / "corpus/knowledge").glob("*.md"))
say(f"README draft index rows={len(new_rows)} (base {len(base_rows)} + entry row)")
say(f"notes on disk in HEAD tree={len(on_disk)}")
rows_no_file = sorted(set(targets) - set(on_disk))
files_no_row = sorted(set(on_disk) - set(targets))
say(f"rows without file in HEAD tree={rows_no_file} (expected: the entry, which lands with the entry)")
say(f"files without row={files_no_row} (expected: none)")
dup = sorted({t for t in targets if targets.count(t) > 1})
say(f"duplicate row targets={dup or 'none'}")
say(f"errata line names file+P23+'supersedes P19': "
    f"{all(s in draft03 for s in ['hyprland-synthetic-dispatch-r52-errata-r53.md', 'P23', 'supersedes P19'])}")
# table-continuity probe on the BASE text (defect D1): blank line between r51 and r52 rows
base_text = (TREE / "corpus/README.md")
b = subprocess.run(["git", "-C", str(LANE), "show", f"{head}:corpus/README.md"], check=True, capture_output=True).stdout.decode("utf-8").split("\n")
r51 = [i for i, l in enumerate(b) if l.startswith("| `knowledge/hyprland-dispatcher-dispatch-r51.md`")][0]
r52 = [i for i, l in enumerate(b) if l.startswith("| `knowledge/hyprland-synthetic-dispatch-r52.md`")][0]
gap = [i + 1 for i in range(r51, r52) if b[i].strip() == ""]
say(f"DEFECT D1 base README: blank line(s) inside coverage table at line(s) {gap} between r51 row ({r51+1}) and r52 row ({r52+1})")

# ---- PROVINCE ----
prov = (TREE / "PROVINCE.md").read_text(encoding="utf-8")
p05 = (DRAFTS / "05-province-round55.md").read_text(encoding="utf-8")
para = [l for l in p05.split("\n") if l.startswith("**Round-55 refinement")][0]
prov = prov.rstrip("\n") + "\n\n" + para + "\n"
(TREE / "PROVINCE.md").write_text(prov, encoding="utf-8")
names = ["tools/mado-kbdopts.py", "quality/counters/c1-r55-kbd-entry.py", "quality/counters/c3-r55-p19.py",
         "quality/check-r55-controls.py", "quality/check-freeze-order.py"]
say("PROVINCE paragraph names all five instruments: " + str(all(n in para for n in names)))
say("PROVINCE paragraph: 'starts no process' for kbdopts: " + str("starts no process" in para))

# ---- tool ledger ----
led = (TREE / "quality/tool-ledger.md").read_text(encoding="utf-8").split("\n")
d06 = [l for l in (DRAFTS / "06-ledger-rows.md").read_text(encoding="utf-8").split("\n") if l.startswith("| `")]
for row in d06:
    cells = [c.strip() for c in row.split("|")[1:-1]]
    assert len(cells) == 3, row
    path = re.fullmatch(r"`([^`]+)`", cells[0]).group(1)
    ptr = re.fullmatch(r"`([^`]+)`", cells[2]).group(1)
    ptr_path = ptr.split(":")[0] if ":" in ptr and not ptr.startswith(".ufo") else ptr
    ptr_ok_exists = subprocess.run(["git", "-C", str(LANE), "cat-file", "-e", f"{head}:{ptr_path}"]).returncode == 0
    ptr_bytes = subprocess.run(["git", "-C", str(LANE), "show", f"{head}:{ptr_path}"], capture_output=True).stdout
    base = os.path.basename(path).encode()
    in_head = subprocess.run(["git", "-C", str(LANE), "cat-file", "-e", f"{head}:{path}"]).returncode == 0
    say(f"ledger {path}: pointer_exists={ptr_ok_exists} basename_in_pointer={base in ptr_bytes} "
        f"in_HEAD={in_head} (expected False until the instrument lands)")
    assert cells[1] and "|" not in cells[1]
dup_led = sorted({re.fullmatch(r"`([^`]+)`", r.split('|')[1].strip()).group(1) for r in d06 if d06.count(r) > 1})
say(f"ledger draft rows={len(d06)} duplicates_inside_draft={dup_led or 'none'}")
ledger_known = {re.fullmatch(r"`([^`]+)`", l.split('|')[1].strip()).group(1) for l in led if l.startswith("| `")}
say(f"ledger draft paths already in HEAD ledger: {sorted(p for p in names if p in ledger_known) or 'none'}")

(WORK / "verify-summary.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
say("VERIFY_DRAFTS: done")
