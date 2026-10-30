#!/usr/bin/env python3
"""R56W3CritC1Forge: build the deliverable receipt (every mutated entry diff + counter line)."""
import difflib
import json
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r56/R56W3CritC1Forge"
W = S + "/W2"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "0f3a54361a9824484d0801679ceb1fd8ac7c32e1"
OUT = LANE + "/.ufo/waves/round-56/w3/R56W3CritC1Forge/receipts/forge-a2.txt"
ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
COUNTER = "quality/counters/c1-r56-autoreload-entry.py"
HARNESS = "quality/check-r56-controls.py"
C3 = "quality/counters/c3-r56-used-by.py"
ROW_RE = re.compile(r"^\| ([KHE]\d\d) \|")


def git(*args, check=True):
    p = subprocess.run(["git", "-C", W] + list(args), capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit("git failed: %s" % p.stderr.decode()[:300])
    return p.stdout


def show(path, rev=REV):
    return git("show", "%s:%s" % (rev, path)).decode("utf-8")


def set_cell(text, rid, idx, val):
    lines = text.split("\n")
    for i, l in enumerate(lines):
        m = ROW_RE.match(l)
        if m and m.group(1) == rid:
            cells = l[2:-2].split(" | ")
            cells[idx] = val
            lines[i] = "| " + " | ".join(cells) + " |"
            return "\n".join(lines)
    raise SystemExit("row %s not found" % rid)


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, cwd=S)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def reset():
    git("reset", "-q", "--hard", REV)
    git("clean", "-qfd")


def commit(text, name, path=ENTRY):
    with open(os.path.join(W, path), "w", encoding="utf-8") as f:
        f.write(text)
    git("add", path)
    git("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "-m", "forge:" + name)
    return git("rev-parse", "HEAD").decode().strip()


base = show(ENTRY)
base_reg = show("corpus/SOURCES.md")
K = {}
for line in base.split("\n"):
    m = ROW_RE.match(line)
    if m:
        K[m.group(1)] = line[2:-2].split(" | ")

# ---- the variants, in the order of the assignment
PARA = json.load(open(S + "/para.json")) if os.path.exists(S + "/para.json") else None

sys.path.insert(0, S)
import forge_final_defs as D  # noqa: E402  (the rewrite tables, reused verbatim)

OUT_L = []
w = OUT_L.append

w("R56W3CritC1Forge -- forge receipt (attempt 2, wave 3)")
w("target: PRED-C1-r56-v2 against the CORRECTED entry at the lane tip")
w("tip revision: %s" % REV)
w("lane root: %s" % LANE)
w("scratch: %s (git clone --shared of the lane; every variant is one commit there)" % W)
w("counter:   python3 -I %s --repo <W> --rev <commit> --work <scratch>" % COUNTER)
w("controls:  python3 -I %s --claim c1 --repo <W> --rev <commit> --work <scratch>" % HARNESS)
w("C3 (x-check): python3 -I %s --repo <W> --rev <commit> --work <scratch>" % C3)
w("")
w("legend: 'ACCEPTED' = the counter prints TARGET_MET with missed=none AND the harness prints")
w("         'good=ok controls=12/12 verdict=OK' -- i.e. the forgery is invisible to both.")
w("")

variants = []

variants.append(("base-honest", "control: the tip entry, unchanged", base, ENTRY))

t = base
for rid, p in D.PARA.items():
    t = set_cell(t, rid, 1, p)
variants.append(("para33", "leg (a): MY OWN lexical paraphrase of every one of the 33 propositions "
                 "(meaning preserved, wording wholly rewritten)", t, ENTRY))

t = base
for rid, p in D.FALSE.items():
    t = set_cell(t, rid, 1, p)
variants.append(("false33", "leg (a') MY OWN semantic falsification of every one of the 33 propositions "
                 "(each one contradicts its pinned line)", t, ENTRY))

t = base
for rid, p in D.NEG3.items():
    t = set_cell(t, rid, 1, p)
variants.append(("neg3", "leg (b): semantic negation of three propositions of my choice (K04, K15, H01)", t, ENTRY))

lines = base.split("\n")
pos = [i for i, l in enumerate(lines) if ROW_RE.match(l)
       and ROW_RE.match(l).group(1) in (set("K%02d" % k for k in range(1, 31)) | set("H%02d" % k for k in range(1, 4)))]
import random
rng = random.Random(20261030)
for sl in (pos[:30], pos[30:33]):
    vals = [lines[i] for i in sl]
    rng.shuffle(vals)
    for i, v in zip(sl, vals):
        lines[i] = v
variants.append(("shuffle", "leg (c): shuffled row order (the 30 K rows shuffled inside the K table, the 3 H rows "
                 "inside the H table; every row keeps its own id, proposition, src, pin and quote)", "\n".join(lines), ENTRY))

variants.append(("cheap1-K26", "cheapest undetected forgery: ONE word of ONE proposition cell changed "
                 "(K26 'at its last slash' -> 'at its first slash', 3 characters of edit)",
                 set_cell(base, "K26", 1,
                          "currentDir is the currentPath text cut with substr at its first slash found by find_last_of on this line."),
                 ENTRY))

variants.append(("cheap1-K24-1char", "cheapest undetected forgery, one character: K24 'the GLOB_TILDE flag' -> "
                 "'the GLOB_TILDE flags' (the pinned line passes ONE flag)",
                 set_cell(base, "K24", 1,
                          "The glob call takes absolutePath of rawpath resolved against m_configCurrentPath and the GLOB_TILDE flags."),
                 ENTRY))

t = base
for rid in ("E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09"):
    t = set_cell(t, rid, 4, "`this line does not exist in any pinned file`")
variants.append(("eforge-e-fake-quotes", "the 9 E rows (outside the frozen 33): every quote cell replaced by text "
                 "present in NO pin file", t, ENTRY))

t = base
for rid in ("E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09"):
    t = set_cell(t, rid, 1, "This line is not what the pinned file says: the quoted text is never reached at run time.")
variants.append(("eforge-e-false-props", "the 9 E rows: every proposition replaced by a denial, quotes untouched", t, ENTRY))

t = base
for rid in ("E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09"):
    t = set_cell(t, rid, 2, "S999")
variants.append(("eforge-e-src-S999", "the 9 E rows: every src cell set to the non-existent registry id S999", t, ENTRY))

lines = base.split("\n")
last = max(i for i, l in enumerate(lines) if l.startswith("| E"))
lines.insert(last + 1,
             "| E10 | The reset helper also truncates the watch descriptor table so that no stale watch survives a rebuild "
             "(this row has no anchor in any pin and cites no registry row) | S396 | Hyprland-NotARealFile.cpp:1 "
             "| `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |")
variants.append(("eforge-new-E10", "a NEW row E10 in the entry: non-existent registry id S396, non-existent pin file, "
                 "fabricated quote, false proposition", "\n".join(lines), ENTRY))

variants.append(("dup-K01-into-E01", "duplicate authority across the 33/42 boundary: E01's proposition set "
                 "byte-identical to K01's (the uniqueness check does not cross the boundary)", set_cell(base, "E01", 1, K["K01"][1]), ENTRY))
variants.append(("dup-K01-into-K02", "POSITIVE CONTROL: K02's proposition set byte-identical to K01's (inside the "
                 "counted 33 -- the uniqueness check must fire)", set_cell(base, "K02", 1, K["K01"][1]), ENTRY))

q = K["K28"][4][1:-1]
variants.append(("echo-off-K28", "K28's frozen quote is %d chars < ECHO_MIN 30, so the echo leg is OFF for that row: "
                 "the quote is embedded verbatim plus a denial" % len(q),
                 set_cell(base, "K28", 1,
                          "The pinned line reads exactly %s and proves the opposite of what it appears to say: the reload "
                          "request handler never reaches the watcher and no watch list is ever rebuilt." % q), ENTRY))

t = base
for old, new in D.PROSE_SUBS:
    assert old in t, old[:50]
    t = t.replace(old, new)
variants.append(("prose-false", "the entry's PROSE body: six load-bearing claims inverted, both row tables untouched", t, ENTRY))

t2 = t.replace(K["K18"][1], "The debug line logs a reload message for the modified config file and passes the event's mask field as its argument.")
variants.append(("prose-false-plus-K18", "the six prose inversions AND the one-word K18 change", t2, ENTRY))

reg = base_reg.split("\n")
out = []
for l in reg:
    m = re.match(r"^ {0,3}\|\s*(S39[1-5])\s*\|", l)
    if m:
        cells = l.strip().strip("|").split("|")
        cells[3] = " C"
        cells[5] = " NoSuchFile.cpp:1-9999 @ efb50993780079460b0cbed1363e2166a2de1d9f; anchor does not exist "
        cells[6] = " this source teaches nothing at all and its quoted line is never executed "
        cells[7] = " rejected"
        cells[8] = " 1999-01-01"
        l = "|" + "|".join(cells) + "|"
    out.append(l)
variants.append(("reg-S391-395-dead", "the registry rows S391..S395 (which no C1 leg reads): tier->C, status->rejected, "
                 "opened->1999-01-01, anchor->a file that does not exist, teaches->a denial", "\n".join(out), "corpus/SOURCES.md"))

out = []
for l in reg:
    m = re.match(r"^ {0,3}\|\s*S383\s*\|", l)
    if m:
        cells = l.strip().strip("|").split("|")
        cells[5] = " ConfigWatcher.cpp:1-112 "
        l = "|" + "|".join(cells) + "|"
    out.append(l)
variants.append(("scope-S383-1-112", "S383 anchor ConfigWatcher.cpp:1-112; the file has 111 newline-terminated lines "
                 "(the bound is len(blob.split(b'\\n')) = 112)", "\n".join(out), "corpus/SOURCES.md"))

out = []
for l in reg:
    m = re.match(r"^ {0,3}\|\s*S383\s*\|", l)
    if m:
        cells = l.strip().strip("|").split("|")
        cells[5] = " ConfigWatcher.cpp:1-111 "
        l = "|" + "|".join(cells) + "|"
    out.append(l)
variants.append(("scope-S383-1-111", "S383 anchor covers the whole file -> the scope leg is vacuous for the S383 rows",
                 "\n".join(out), "corpus/SOURCES.md"))

for name, what, text, path in variants:
    ref = base if path == ENTRY else base_reg
    sha = commit(text, name, path)
    rc1, o1, e1 = run([sys.executable, "-I", LANE + "/" + COUNTER, "--repo", W, "--rev", sha, "--work", S + "/work/c-" + name])
    rc2, o2, e2 = run([sys.executable, "-I", LANE + "/" + HARNESS, "--claim", "c1", "--repo", W, "--rev", sha, "--work", S + "/work/h-" + name])
    rc3, o3, e3 = run([sys.executable, "-I", LANE + "/" + C3, "--repo", W, "--rev", sha, "--work", S + "/work/c3-" + name])
    reset()
    good = [l for l in e2.split("\n") if l.startswith("good:")]
    diff = list(difflib.unified_diff(ref.split("\n"), text.split("\n"),
                                     fromfile="tip:%s" % path, tofile="forged:%s" % path, lineterm="", n=0))
    changed = [l for l in diff if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---"))]
    w("=" * 100)
    w("VARIANT %s" % name)
    w("  what: %s" % what)
    w("  commit: %s" % sha)
    w("  mutated file: %s ; %d changed lines" % (path, len(changed)))
    for l in changed:
        w("    %s" % l[:600])
    w("  counter   rc=%d  %s" % (rc1, o1.strip()))
    w("  harness   rc=%d  %s" % (rc2, o2.strip()))
    w("  harness good leg: %s" % (good[0] if good else "(not printed)"))
    fails = [l.strip() for l in e2.split("\n") if "FAIL" in l]
    w("  harness control failures: %s" % ("; ".join(fails) if fails else "none"))
    w("  C3        rc=%d  %s" % (rc3, o3.strip()))
    w("")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT_L) + "\n")
print("wrote %s (%d lines)" % (OUT, len(OUT_L)))
