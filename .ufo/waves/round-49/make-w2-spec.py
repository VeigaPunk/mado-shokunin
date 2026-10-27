#!/usr/bin/env python3
"""Generates .ufo/waves/round-49/w2-spec.json (round 49, wave w2 = FALSIFY, policy v1, band 32-64).

Every item attacks one frozen artifact of the round-49 freeze (registration.md) and names what it attacks.
"""
import collections
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-49"
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
SCR = "/fast/scratch/hyaku/mado-r49"
FREEZE = os.environ.get("FREEZE", "<freeze>")
GODSPEED = (
    "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls "
    "concurrently in large batches. Do not serialize what can run in "
    "parallel. Do not output philosophical reasoning or verbose plans. Act "
    "directly via tool calls.\n\n")

CONTEXT = f"""# Goal
mado round 49 (hyaku run 9, 2026-10-27), wave w2 = FALSIFY (policy v1). Lane repo: {LANE}. Base {BASE}; the round's predicates, counters,
fixtures, controls and candidate data were frozen at commit {FREEZE} (read {W}/registration.md FIRST: it names every frozen file, the predicates
PRED-C1-r49 and PRED-C2-r49 and the controls). Your job is to BREAK what was frozen: find a tool or entry that scores TARGET_MET while being wrong, a
correct one that scores TARGET_MISSED, a false sentence, a forged or mislocated quote, a host write, an unreceipted number. Every finding names the
frozen artifact it attacks (path:line or sha256), the command you ran and its output. A finding you could not reproduce is not a finding.
- C1: tools/mado-keysym.py (candidate, at {W}/candidate/) predicts `/usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG`
  stdout + exit status on keymaps compiled by `/usr/lib/xkbcommon/xkbcli-compile-keymap` (libxkbcommon 1.13.2, xkeyboard-config 2.48); counter
  quality/counters/c1-r49-keysym.py (frozen).
- C2: corpus/knowledge/hyprland-bind-key-match-r49.md (candidate, at {W}/candidate/), rows S352.. ; counter quality/counters/c2-r49-bind-entry.py
  (frozen); pins under {W}/fetch/.
- Routed items worked this round (candidates under {W}/candidate/ and {W}/w1/): session-material gate v3 (M48-8), host guard (M48-10), scratch refusal
  (SentScratch), N1-N5 corrections, the 47 sidecars decision, QUALITY candidates.
# Write scope and safety
- Write ONLY to your own seat directory {W}/w2/<YourSeatName>/ (create it) plus your Report file; never edit an existing tracked file, never create
  files elsewhere in the lane, the fleet repo, sibling lanes or the shokuknow checkout. Never run mutating git/jj in the lane or the fleet.
- Every `Report:` trailer path is relative to {LANE} - write it at {LANE}/<that path>. Your tools start at the fleet root: absolute paths only.
  Write your Report file FIRST (a short status), then refine it.
- SCRATCH: everything under {SCR}/<YourSeatName>/ (mkdir -p; pass it explicitly as TMPDIR/--work); start every writer shell with
  `ulimit -f 65536` (64 MiB per file; `git clone -q --shared {LANE} "$D"` fits); bound every loop; never write into a FIFO or device; copy receipts
  into your seat dir, then `trap 'rm -rf -- "$S"' EXIT`. /tmp and scratch paths are never citable evidence.
- HOST GUARD (round-48 M48-10): NEVER write the operator's real ~/.cache, ~/.config, ~/.local or other home state. Every mutant, probe, counter or
  judge run sets HOME, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME to dirs under your scratch (preferably inside bwrap). A mutant
  that writes targets a path inside the sandbox only.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No compositor/service mutation, no input injection, no GUI
  or terminal launch. xkbcli only `compile-keymap`, `how-to-type`, `list` (clean env). Compositor reads only: `hyprctl version`, `hyprctl binds -j`,
  `hyprctl getoption <opt> -j`, `hyprctl devices -j` (never commit device names). Session material stays shape-only; write `~` for the home dir.
- Git fixtures: `D=$(mktemp -d -p {SCR}/<YourSeatName>) && git -C "$D" init -q` (or a --shared clone), every git call `-C "$D"`, verify
  `git -C "$D" rev-parse --show-toplevel` = $D before the first commit; never commit with a throwaway identity anywhere else.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task - read /home/vgpnk/.omp/agent/RULES.md first
  (official channels, update-safety gate; record tool/version/channel/reason). pacman guard: ALL pacman transactions are PAUSED host-wide - use uv
  tool / a scratch venv / npx / an official binary in ~/.local/bin; never -Sy, -Syu, -U, -R, a downgrade, or a restart of a host service.
- You are a leaf: no subagent dispatch, no background jobs (an executor MAY spawn one read-only labrat probe).
- Quotes <= 25 words, located, verified by a script; locators computed (grep -n). Never fabricate: an unrun check has not passed.
"""

items = []


def seat(name, role, target, task):
    items.append({"name": name, "role": role,
                  "prompt": GODSPEED + "# Target\n" + target.strip() + "\n# Task\n" + task.strip() + "\n"})


ITEMS = []  # filled from w2-items.json (written by the L1 after the freeze; each item names what it attacks)
with open(os.path.join(W, "w2-items.json")) as fh:
    ITEMS = json.load(fh)
for it in ITEMS:
    seat(it["name"], it["role"], it["target"], it["task"])

n = len(items)
assert 32 <= n <= 64, n
assert len({i["name"] for i in items}) == n
print(n, dict(collections.Counter(i["role"] for i in items)))
spec = {"wave": "w2", "context": CONTEXT, "reportDir": ".ufo/waves/round-49/w2", "items": items}
with open(os.path.join(W, "w2-spec.json"), "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
