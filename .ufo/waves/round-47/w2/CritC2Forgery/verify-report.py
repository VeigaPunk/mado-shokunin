#!/usr/bin/env python3
"""Verify CritC2Forgery report quotes/locators against the pins and the committed forgeries."""
import os
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = LANE + "/.ufo/waves/round-47/w2/CritC2Forgery"
REPORT = SEAT + "/CritC2Forgery.md"
PINS = "/fast/scratch/hyaku/mado-r47/CritC2Forgery/pins"
S = "/fast/scratch/hyaku/mado-r47/CritC2Forgery"
fail = []


def has(s, pat):
    return re.search(pat, s) is not None


# 1. every score receipt says admitted=1 and exit=0
for name in ["POS", "F1-false-mechanism", "F2-comment-quotes", "F3-typed-capture",
             "F4-readme-elsewhere", "F5-false-scope", "F6-reclaim-held-ground",
             "F7a-r17-deleted", "F7b-r17-anchor-shifted", "F8-launch-half-claim",
             "F9-provenance-lie"]:
    p = os.path.join(SEAT, "score-%s.txt" % name)
    if not os.path.exists(p):
        fail.append("missing score receipt %s" % name)
        continue
    txt = open(p, encoding="utf-8").read()
    if "admitted=1/1" not in txt or "verdict=TARGET_MET" not in txt:
        fail.append("score %s not admitted: %s" % (name, txt[-200:]))

# 2. script anchor quotes at their computed lines (comments/doc text)
checks = [
    ("xdg-terminal-exec", 147, "Populate list of config files to read, in descending order of preference"),
    ("xdg-terminal-exec", 353, "All config files are read immediatelly, rather than on demand"),
    ("xdg-terminal-exec", 364, "Nonexistant file is not an error"),
    ("xdg-terminal-exec", 565, "Fills global XTE__EXEC_USEP var with $XTE__USEP-separated command array"),
    ("xdg-terminal-exec", 805, "XTE__EXEC_USEP : Program to execute, possibly with arguments, delimited by ASCII Unit Separator."),
    ("xdg-terminal-exec", 112, "print selected Desktop Entry ID. Action is appended delimited"),
    ("xdg-terminal-exec", 148, "for xte__dir in ${XDG_CONFIG_HOME"),
    ("xdg-terminal-exec", 780, "Entries are checked in ascending order of preference, so use last found if duplicate"),
]
for fname, ln, q in checks:
    text = open(os.path.join(PINS, fname), encoding="utf-8", errors="replace").read().split("\n")
    line = text[ln - 1] if ln - 1 < len(text) else ""
    if q not in line:
        fail.append("pin %s:%d missing %r" % (fname, ln, q[:40]))

# 3. F3 mismatch: observed says WezTerm, receipt echoes Alacritty
obs = subprocess.run(["git", "-C", S + "/f/F3-typed-capture", "show",
                      "HEAD:.ufo/waves/round-47/receipts/live-observed.txt"],
                     capture_output=True).stdout.decode()
rec = subprocess.run(["git", "-C", S + "/f/F3-typed-capture", "show",
                      "HEAD:.ufo/waves/round-47/receipts/live-host.txt"],
                     capture_output=True).stdout.decode()
if not obs.startswith("WezTerm.desktop\n"):
    fail.append("F3 observed not WezTerm")
if "selected=Alacritty.desktop" not in rec:
    fail.append("F3 receipt echo lacks Alacritty")

# 4. F7b: [UNK] no longer at line 144
r17 = subprocess.run(["git", "-C", S + "/f/F7b-r17-anchor-shifted", "show",
                      "HEAD:corpus/knowledge/terminal-route-r17.md"],
                     capture_output=True).stdout.decode().split("\n")
if "[UNK]" in r17[143]:
    fail.append("F7b: [UNK] still at line 144")
if "resolver actually picks" not in r17[149]:
    fail.append("F7b: shifted UNK not found at 150")

# 5. F7a: r17 deleted
p = subprocess.run(["git", "-C", S + "/f/F7a-r17-deleted", "ls-tree", "HEAD",
                    "corpus/knowledge/"], capture_output=True).stdout.decode()
if "terminal-route-r17.md" in p:
    fail.append("F7a: r17 still present")

# 6. F9 head says S326 is the man page, while the S326 row is the script
head = subprocess.run(["git", "-C", S + "/f/F9-provenance-lie", "show",
                       "HEAD:corpus/knowledge/xdg-terminal-selection-r47.md"],
                      capture_output=True).stdout.decode()
if "S326 - xdg-terminal-exec 0.14.3 man page" not in head:
    fail.append("F9 head lie missing")
src = subprocess.run(["git", "-C", S + "/f/F9-provenance-lie", "show",
                      "HEAD:corpus/SOURCES.md"], capture_output=True).stdout.decode()
m = re.search(r"\| S326 \|([^|]*)\|", src)
if not m or "selection script" not in m.group(1):
    fail.append("F9 S326 row is not the script")

# 7. F4 README row claims a launch verdict
readme = subprocess.run(["git", "-C", S + "/f/F4-readme-elsewhere", "show",
                         "HEAD:corpus/README.md"], capture_output=True).stdout.decode()
row = [l for l in readme.split("\n") if "xdg-terminal-selection-r47.md" in l and l.startswith("| `knowledge")]
if len(row) != 1 or "at launch the user override wins" not in row[0]:
    fail.append("F4 README row wrong")

# 8. F8 entry claims launch half
live8 = subprocess.run(["git", "-C", S + "/f/F8-launch-half-claim", "show",
                        "HEAD:corpus/knowledge/xdg-terminal-selection-r47.md"],
                       capture_output=True).stdout.decode()
if "answers it at launch" not in live8:
    fail.append("F8 launch claim missing")

# 9. F6 rows restate held rows
src6 = subprocess.run(["git", "-C", S + "/f/F6-reclaim-held-ground", "show",
                       "HEAD:corpus/SOURCES.md"], capture_output=True).stdout.decode()
if "restated from held row S057" not in src6:
    fail.append("F6 held restatement missing")

# 10. F1 claims contradict pinned code
ent1 = subprocess.run(["git", "-C", S + "/f/F1-false-mechanism", "show",
                        "HEAD:corpus/knowledge/xdg-terminal-selection-r47.md"],
                       capture_output=True).stdout.decode()
if "*ascending* preference" not in ent1 or "FIRST found wins" not in ent1:
    fail.append("F1 false mechanisms missing")

if fail:
    print("VERIFY FAIL")
    for f in fail:
        print(" -", f)
    raise SystemExit(1)
print("VERIFY OK: all report locators and forgery shapes confirmed")
