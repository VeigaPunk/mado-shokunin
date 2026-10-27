#!/usr/bin/env python3
"""Verify every locator and fragment the round-48 lesson skeleton cites.

Read-only. Locators are computed with grep -n on the named file; the fragment is
whatever the skeleton quotes or states, and the check fails if it is absent from
the computed line (or line range). Also prints the skeleton's section map and the
<AFTER> census. Run from the lane root:
  python3 -I .ufo/waves/round-48/w1/ScrLesson/verify.py
"""
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
LESSON = f"{LANE}/.ufo/waves/round-48/w1/ScrLesson/round-48.md"

fails = 0


def grep_line(path, needle, expect_range=None):
    """Return computed 1-based line numbers of `needle` in `path` (fixed string)."""
    p = subprocess.run(["grep", "-nF", "--", needle, path], capture_output=True, text=True)
    nums = [int(m.group(1)) for m in re.finditer(r"^(\d+):", p.stdout, re.M)]
    return nums


def check(label, path, needle, claimed, inside=True):
    """needle present (or absent) at the computed locator(s)."""
    global fails
    nums = grep_line(path, needle)
    rel = path.replace(LANE + "/", "")
    if inside:
        ok = any(claimed[0] <= n <= claimed[1] for n in nums)
        verdict = "OK" if ok else "DIFFER"
    else:
        ok = not any(claimed[0] <= n <= claimed[1] for n in nums)
        verdict = "OK" if ok else "DIFFER"
    if not ok:
        fails += 1
    print(f"CHECK {label:26s} {rel}:{claimed[0]}-{claimed[1]} computed={nums} "
          f"needle={'present' if inside else 'absent'} verdict={verdict}")
    return ok


def words(label, text):
    n = len(text.split())
    if n > 25:
        print(f"WORDCOUNT {label} words={n} verdict=OVER")
    return n


# --- C1 / D1 contract delta -------------------------------------------------
check("tool-cache-para", f"{LANE}/tools/mado-terminal.py", "Cache (out of contract)", (82, 82))
check("tool-added-home-unset", f"{LANE}/tools/mado-terminal.py",
      "HOME unset, a FIFO named like a desktop file in a", (85, 85))
check("tool-added-home-unset-2", f"{LANE}/tools/mado-terminal.py",
      "later application dir (the script blocks reading it)", (86, 86))
check("tool-added-symlink-loops", f"{LANE}/tools/mado-terminal.py", "symlink loops", (86, 86))
check("frozen-cache-para", f"{LANE}/.ufo/waves/round-47/l1-draft/mado-terminal.py",
      "Cache (out of contract)", (81, 81))
check("frozen-list-start", f"{LANE}/.ufo/waves/round-47/l1-draft/mado-terminal.py",
      "Also out of contract:", (84, 87))
check("frozen-no-home-unset", f"{LANE}/.ufo/waves/round-47/l1-draft/mado-terminal.py",
      "HOME unset,", (84, 87), inside=False)
check("frozen-no-fifo", f"{LANE}/.ufo/waves/round-47/l1-draft/mado-terminal.py",
      "FIFO", (84, 87), inside=False)
check("frozen-no-symlink-loops", f"{LANE}/.ufo/waves/round-47/l1-draft/mado-terminal.py",
      "symlink loops", (84, 87), inside=False)
check("frozen-raises-home", f"{LANE}/.ufo/waves/round-47/l1-draft/mado-terminal.py",
      'OutOfContract("HOME unset")', (400, 415))
check("registration-contract", f"{LANE}/.ufo/waves/round-47/registration.md",
      "the docstring of `.ufo/waves/round-47/l1-draft/mado-terminal.py`", (30, 31))
check("spotcheck-D1", f"{LANE}/corpus/lessons/round-47-verifier-spotcheck.md",
      "1. D1:", (126, 126))
check("spotcheck-D2", f"{LANE}/corpus/lessons/round-47-verifier-spotcheck.md",
      "2. D2:", (132, 132))
check("spotcheck-R3-r46", f"{LANE}/corpus/lessons/round-46-verifier-spotcheck.md", "3. R3", (113, 113))
check("spotcheck-R4-r46", f"{LANE}/corpus/lessons/round-46-verifier-spotcheck.md", "4. R4", (116, 116))
check("spotcheck-D3", f"{LANE}/corpus/lessons/round-47-verifier-spotcheck.md",
      "3. D3:", (136, 136))
check("spotcheck-D4", f"{LANE}/corpus/lessons/round-47-verifier-spotcheck.md",
      "4. D4:", (139, 139))

# --- resolver pin locators the skeleton names -------------------------------
PIN = f"{LANE}/.ufo/waves/round-47/fetch/xdg-terminal-exec"
check("pin-read-before-lists", PIN, 'check_bool "${XTE__CACHE_ENABLED}" && read_cache', (1179, 1179))
check("pin-read-cache-fn", PIN, "read_cache() {", (217, 217))
check("pin-gen-hash-fn", PIN, "gen_hash() {", (179, 179))
check("pin-save-bg", PIN, 'save_cache "$1" &', (1455, 1458))
print(f"PIN sha256: ", end="", flush=True)
subprocess.run(["sha256sum", PIN])

# --- C2 ground --------------------------------------------------------------
check("r46-open-ground", f"{LANE}/corpus/knowledge/hyprland-input-devices-r46.md",
      "The XKB compile itself is not reproduced", (69, 69))
check("readme-cache-open", f"{LANE}/corpus/README.md", "the warm-cache path", (110, 110))
check("readme-xkb-open", f"{LANE}/corpus/README.md", "the XKB compile itself", (112, 112))
check("readme-r47-index-row", f"{LANE}/corpus/README.md", "xdg-terminal-selection-r47.md", (75, 75))
check("held-S318", f"{LANE}/corpus/SOURCES.md", "| S318 |", (267, 267))
check("held-S319", f"{LANE}/corpus/SOURCES.md", "| S319 |", (268, 268))

# --- round-47 lesson locators the skeleton cites ----------------------------
check("r47-considerthese", f"{LANE}/corpus/lessons/round-47.md", "proposal 2", (227, 227))
check("r47-quarantine", f"{LANE}/corpus/lessons/round-47.md", "quarantine-slice", (233, 234))

# --- measured counts --------------------------------------------------------
def sh(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.stdout.strip(), p.returncode

rows, _ = sh(f"grep -cE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' {LANE}/corpus/SOURCES.md")
top, _ = sh(f"grep -oE '^\\s*\\|\\s*S[0-9]{{3,}}' {LANE}/corpus/SOURCES.md | tr -dc '0-9\\n' | sort -n | tail -1")
know, _ = sh(f"ls {LANE}/corpus/knowledge/*.md | wc -l")
lessons, _ = sh(f"ls {LANE}/corpus/lessons/*.md | wc -l")
tools, _ = sh(f"ls {LANE}/tools/ | wc -l")
readmerows, _ = sh(f"grep -cE '^\\|[[:space:]]*`?knowledge' {LANE}/corpus/README.md")
qual_top, _ = sh(f"grep -oE '^[0-9]{{2,3}}\\.' {LANE}/corpus/QUALITY.md | tr -dc '0-9\\n' | sort -n | tail -1")
census = f"{LANE}/.ufo/waves/round-48/receipts/census-before.txt"
w04, _ = sh(f"grep -c W04 {census}")
w01, _ = sh(f"grep -c W01 {census}")
clines, _ = sh(f"wc -l < {census}")
ctail, _ = sh(f"tail -1 {census}")
print(f"COUNTS rows={rows} top=S{top} knowledge={know} lessons={lessons} tools={tools} "
      f"readme_index_rows={readmerows} quality_top={qual_top}")
print(f"CENSUS W04={w04} W01={w01} lines={clines} last={ctail}")

# --- id guard ---------------------------------------------------------------
A = f"{LANE}/.ufo/waves/round-48/assimilation"
prog = f"""
A={A!r}
reg=[l.strip() for l in open(A+'/reg-ids') if l.strip()]
st=[l.strip() for l in open(A+'/staged-ids') if l.strip()]
col=[l.strip() for l in open(A+'/collisions') if l.strip()]
print('IDGUARD reg=%d %s-%s staged=%d %s-%s collisions=%d %s-%s inter_equal=%s staged_340_349=%s' % (
 len(reg),min(reg),max(reg),len(st),min(st),max(st),len(col),min(col),max(col),set(col)==(set(reg)&set(st)),
 all('S34%d'%i in st for i in range(10))))
"""
print(sh(f"python3 -I -c {prog!r}")[0])

# --- quarantine -------------------------------------------------------------
q = f"{LANE}/.ufo/waves/round-47/assimilation/quarantine-slice"
qn, _ = sh(f"wc -l < {q}")
qpayload, _ = sh(f"grep -c 'payload-absent' {q}")
print(f"QUARANTINE r47 lines={qn} payload_absent={qpayload}")

# --- skeleton shape ---------------------------------------------------------
text = open(LESSON, encoding="utf-8").read()
heads = [f"{i}:{line}" for i, line in enumerate(text.splitlines(), 1)
         if re.match(r"^## |^### ", line)]
print("SECTIONS " + " | ".join(heads))
print(f"AFTER_MARKERS {text.count('<AFTER>')}")
for bad in ("/tmp/", "/fast/scratch"):
    if bad in text:
        print(f"SCRATCH_REF {bad} verdict=OVER")
print(f"VERIFY: checks_failed={fails}")

# --- quoted fragments: every one <= 25 words (skill rule) -------------------
for label, frag in (
        ("r46-xkb-compile", "The XKB compile itself is not reproduced"),
        ("readme-warm-cache", "the warm-cache path"),
        ("readme-xkb-compile", "the XKB compile itself"),
        ("tool-fifo", "HOME unset, a FIFO named like a desktop file in a later application dir"),
        ("tool-symlink-loops", "symlink loops")):
    print(f"WORDS {label:20s} words={len(frag.split())} verdict={'OK' if len(frag.split()) <= 25 else 'OVER'}")

# --- provenance of the header's two commits (read-only) ---------------------
for label, rev in (("BASE", "579f694b45c797a9c39761fdb4f9e0a1b71b3585"),
                   ("SETUP", "5ff167423ee410251da0ef0c82f8e6fa25875665")):
    out, rc = sh(f"git -C {LANE} log -1 --format='%H %s' {rev}")
    print(f"GIT_{label} rc={rc} {out}")
head, _ = sh(f"git -C {LANE} rev-parse HEAD")
anc_out, anc_rc = sh(f"git -C {LANE} merge-base --is-ancestor 579f694b45c797a9c39761fdb4f9e0a1b71b3585 {head}")
print(f"GIT_HEAD {head} base_is_ancestor_rc={anc_rc} stdout={anc_out!r}")
r47col, _ = sh(f"wc -l < {LANE}/.ufo/waves/round-47/assimilation/collisions")
print(f"IDGUARD_R47 collisions={r47col}")
lines, _ = sh(f"wc -l < {LESSON}")
print(f"LESSON lines={lines}")
sys.exit(1 if fails else 0)
