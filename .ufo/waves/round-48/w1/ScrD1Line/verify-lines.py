#!/usr/bin/env python3
"""Verify every locator, quote and receipt cited by lines.md. Exit 0 iff all checks pass."""
import ast
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-48/w1/ScrD1Line")
FROZEN = os.path.join(LANE, ".ufo/waves/round-47/l1-draft/mado-terminal.py")
LANDED = os.path.join(LANE, "tools/mado-terminal.py")
LINES = os.path.join(SEAT, "lines.md")
PIN = "/usr/bin/xdg-terminal-exec"
PIN_SHA = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
FREEZE = "d7527d608ad2b2e3cc398fdde34db7947b254a1a"

fails, count = [], [0]


def check(name, ok, detail=""):
    count[0] += 1
    print("%-64s %s%s" % (name, "PASS" if ok else "FAIL", (" " + detail) if detail else ""))
    if not ok:
        fails.append(name)


def read(path):
    return open(os.path.join(LANE, path), encoding="utf-8", errors="surrogateescape").read()


def lines_of(path):
    return read(path).split("\n")


def prose(path, a, b):
    return " ".join(x.strip() for x in lines_of(path)[a - 1:b])


def git_show(spec):
    return subprocess.run(["git", "-C", LANE, "show", spec], capture_output=True).stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


# --- identities named in lines.md ------------------------------------------------------------------
frozen_sha = sha(open(FROZEN, "rb").read())
landed_sha = sha(open(LANDED, "rb").read())
check("frozen file = frozen reference at d7527d60",
      frozen_sha == sha(git_show(FREEZE + ":.ufo/waves/round-47/l1-draft/mado-terminal.py")), frozen_sha[:16])
check("landed tool = base 579f694b", landed_sha == sha(git_show(BASE + ":tools/mado-terminal.py")), landed_sha[:16])
lines_md = read(".ufo/waves/round-48/w1/ScrD1Line/lines.md")
check("lines.md names the frozen blob", frozen_sha in lines_md)
check("lines.md names the landed blob", landed_sha in lines_md)
check("pin on disk = pinned sha256", sha(open(PIN, "rb").read()) == PIN_SHA)

# --- the docstring delta is exactly two hunks ------------------------------------------------------
ds_frozen = ast.get_docstring(ast.parse(read(".ufo/waves/round-47/l1-draft/mado-terminal.py")))
ds_landed = ast.get_docstring(ast.parse(read("tools/mado-terminal.py")))
f_lines, l_lines = ds_frozen.split("\n"), ds_landed.split("\n")
opcodes = [o for o in difflib.SequenceMatcher(None, f_lines, l_lines).get_opcodes() if o[0] != "equal"]
check("docstring 86 -> 87 lines", (len(f_lines), len(l_lines)) == (86, 87), "%d -> %d" % (len(f_lines), len(l_lines)))
check("docstring diff = exactly 2 change hunks", len(opcodes) == 2, str([o[0] for o in opcodes]))
if len(opcodes) == 2:
    h1 = "\n".join(f_lines[opcodes[0][1]:opcodes[0][2]])
    h2 = "\n".join(f_lines[opcodes[1][1]:opcodes[1][2]])
    check("hunk 1 = the command -v sentence (M47-10)", h1.strip().startswith("`command -v` finds aliases"),
          repr(h1.strip()[:34]))
    check("hunk 2 = the out-of-contract list", h2.strip().startswith("models the cold path; `explain`"),
          repr(h2.strip()[:34]))
for item in ("HOME unset", "a FIFO named like a desktop file", "symlink loops"):
    check("frozen docstring lacks %r" % item, item not in ds_frozen)
    check("landed docstring has %r" % item, item in ds_landed)

# --- quote + locator checks; quoted==True means lines.md must reproduce the text ---------------------
QUOTES = [
    ("tools/mado-terminal.py", 85, 85, "Also out of contract: -h/--help, HOME unset", True),
    (".ufo/waves/round-47/l1-draft/mado-terminal.py", 84, 84, "Also out of contract: -h/--help, an empty-string", True),
    (".ufo/waves/round-47/l1-draft/mado-terminal.py", 407, 407, 'raise OutOfContract("HOME unset")', True),
    ("tools/mado-terminal.py", 410, 410, 'raise OutOfContract("HOME unset")', True),
    ("tools/mado-terminal.py", 85, 86,
     "a FIFO named like a desktop file in a later application dir (the script blocks reading it)", True),
    ("tools/mado-terminal.py", 86, 86, "symlink loops, an empty-string argument", False),
    ("tools/mado-terminal.py", 88, 88,
     "On these the tool prints `MADO_TERM_OUT_OF_CONTRACT: <reason>` on stderr and exits 2.", True),
    ("tools/mado-terminal.py", 512, 514, "if key in ancestors:", True),
    (".ufo/waves/round-47/l1-draft/mado-terminal.py", 503, 503, "if key in ancestors:", True),
    (".ufo/waves/round-47/l1-draft/mado-terminal.py", 519, 519, "if not stat.S_ISREG(cst.st_mode):", True),
    ("tools/mado-terminal.py", 526, 529, 'raise OutOfContract("a FIFO named like a desktop file', False),
    ("tools/mado-terminal.py", 49, 49, "`find -L <dir>/. -type f` over the application dirs", True),
    (".ufo/waves/round-47/l1-draft/mado-terminal.py", 49, 49, "`find -L <dir>/. -type f` over the application dirs", True),
    ("tools/mado-terminal.py", 51, 51, "a path counts when its part after", True),
    ("tools/mado-terminal.py", 494, 495, "`-type f` binds to the first group", True),
    ("tools/mado-terminal.py", 535, 535, "elif self._id_ok(rel):", True),
    (".ufo/waves/round-47/w2/ExecC1Determinism.md", 10, 10,
     "the frozen fixture set \u2014 clause f/x are blind to the readdir axis", True),
    (".ufo/waves/round-47/w2/ExecC1Determinism.md", 75, 76, "190/190", True),
    (".ufo/waves/round-47/w2/ExecC1Determinism.md", 62, 62, "byte-identical", False),
    (".ufo/waves/round-47/ctl/build-fixtures.py", 70, 70, '"x" * (k + 1)', False),
    (".ufo/waves/round-47/ctl/build-fixtures.py", 76, 76, "if len(set(res)) != 1:", False),
    (".ufo/waves/round-48/claims.md", 20, 20, "HOME unset modelled as the pin (round-47 D1)", True),
    ("corpus/lessons/round-47-verifier-spotcheck.md", 46, 46, "Two refusals diverge from the pin", True),
    ("corpus/lessons/round-47.md", 205, 205, "**M47-10**", True),
    ("tools/mado-terminal.py", 551, 552, "if os.path.isdir(path):", False),
    ("quality/counters/c1-r47-terminal.py", 220, 220, "def case_env(case, root, lang):", False),
    ("quality/counters/c1-r47-terminal.py", 222, 222, 'env["HOME"]', False),
]
for path, a, b, quote, must_quote in QUOTES:
    check("%s:%d-%d holds %r" % (path, a, b, quote[:44]), quote in prose(path, a, b))
    if must_quote:
        norm = lambda t: re.sub(r"\s+", " ", t)
        check("  lines.md reproduces it", norm(quote) in norm(lines_md))

for ln in (148, 166, 172):
    check("/usr/bin/xdg-terminal-exec:%d expands ${HOME}" % ln, "${HOME}" in lines_of(PIN)[ln - 1])
check("/usr/bin/xdg-terminal-exec:23 = set -euf", lines_of(PIN)[22].strip() == "set -euf")
check("case_env always injects HOME", 'env["HOME"]' in lines_of("quality/counters/c1-r47-terminal.py")[221])
check("M47-10 is the highest M47 id",
      max(int(m) for m in re.findall(r"\*\*M47-(\d+)\*\*", read("corpus/lessons/round-47.md"))) == 10)

# --- fixture-set facts ------------------------------------------------------------------------------
fx = json.load(open(os.path.join(LANE, "quality/counters/c1-r47-fixtures.json")))
cases = fx["cases"] if isinstance(fx, dict) else fx
check("fixtures: 190 cases", len(cases) == 190, str(len(cases)))
check("fixtures: no case sets HOME in env", not any("HOME" in c.get("env", {}) for c in cases))
check("fixtures: no case uses a symlink",
      not any("->" in str(v) for c in cases for v in c.get("files", {}).values()))

# --- receipts cited by lines.md ---------------------------------------------------------------------
RECEIPTS = {
    "probe2-out.txt": ("term.desktop", "pin rc=124", "sub-deep.desktop", "MADO_TERM_OUT_OF_CONTRACT"),
    "probe4-out.txt": ("HOME absent", "pin  rc=0 out='term.desktop\\n'", "tool rc=2 out=''"),
    "probe5-out.txt": ("pin rc=0 out='term.desktop\\n' | tool rc=2 out=''", "pin rc=1 out='' | tool rc=2 out=''"),
    "probe6-out.txt": ("is shadowed by", "Is a directory", "term.desktop"),
    "probe7-out.txt": ("pin ---\nterm.desktop\npin rc=0", "MADO_TERM_OUT_OF_CONTRACT", "tool rc=2"),
    "receipt-home-unset-host.txt": ("line 148: HOME: unbound variable", "rc=1", "term.desktop", "rc=2",
                                    "MADO_TERM_OUT_OF_CONTRACT: HOME unset", "XDG_CACHE_HOME: set, len=18"),
    "probe-out.txt": ("17:42:25",),
    "probe3-out.txt": ("V4 HOME unset",),
}
for name, needles in RECEIPTS.items():
    p = os.path.join(SEAT, "receipts", name)
    ok = os.path.exists(p)
    text = open(p, encoding="utf-8", errors="surrogateescape").read() if ok else ""
    check("receipt %s present" % name, ok)
    for n in needles:
        check("  %s holds %r" % (name, n[:40]), n in text)

# lines.md must declare probe3 as non-evidence (the ambient-XDG trap)
check("lines.md declares probe3 a trap, not evidence",
      "is kept only to show the trap and is **not** cited as" in lines_md)
status = [l for l in subprocess.run(["git", "-C", LANE, "status", "--porcelain", "--untracked-files=all"],
                                    capture_output=True, text=True).stdout.split("\n") if l.strip()]
mine_modified = [l for l in status if not l.startswith("??")]
check("the only modified tracked file is another seat's, not code",
      [l[3:] for l in mine_modified] == [".ufo/waves/round-47/w1/ExecCounterC1.md"],
      str(mine_modified[:3]))
code_touched = [l for l in status if re.search(r" (tools|quality|corpus)/", l)]
check("no tracked file under tools/, quality/ or corpus/ is modified", code_touched == [], str(code_touched[:3]))
my_new = [l[3:] for l in status if l.startswith("??") and l[3:].startswith(".ufo/waves/round-48/w1/ScrD1Line")]
check("this seat's new paths are the seat dir and its report", len(my_new) > 0, "%d paths" % len(my_new))

# --- cross-seat corroboration (peer receipts named in lines.md) --------------------------------------
peer = os.path.join(LANE, ".ufo/waves/round-48/w1/ExecHomeUnset.md")
peer_text = open(peer, encoding="utf-8").read() if os.path.exists(peer) else ""
check("peer report w1/ExecHomeUnset.md exists", bool(peer_text))
for token in ("C3b", "C3c", "openat", "killed at 3 s"):
    check("  peer report carries %r" % token, token in peer_text)
check("peer's own step-4 line is its M47-12 (the collision note)",
      "**M47-12**" in peer_text and "step 4" in peer_text)
check("lines.md names the collision and the peer's relabel", "Numbering collision, resolved on the peer side" in lines_md
      and "placeholder label only" in lines_md)
check("lines.md splits the fatal HOME sub-case into three sites",
      all("`x:%d`" % n in lines_md for n in (148, 166, 172)))

print("\nVERIFY: %d checks, %s" % (count[0], "ALL PASS" if not fails else "FAILURES: " + "; ".join(fails)))
sys.exit(0 if not fails else 1)
