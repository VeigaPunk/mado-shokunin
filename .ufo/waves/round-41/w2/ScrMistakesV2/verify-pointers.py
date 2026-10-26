#!/usr/bin/env python3
"""Verify every evidence pointer used in mistakes.md (M41-9..17).

Checks path:line fragments in the working tree (wave files under
.ufo/waves/round-41/); the lessons file at the DATA commit via
`git show 07f2641:corpus/lessons/round-41.md`; and the existence of the
cheat-score receipt cited in M41-9.
"""
import subprocess, sys, os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DATA = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
W = ".ufo/waves/round-41"

def lines_of(path):
    with open(os.path.join(LANE, path), encoding="utf-8") as f:
        return f.read().splitlines()

def git_lines(path):
    out = subprocess.run(
        ["git", "-C", LANE, "show", f"{DATA}:{path}"],
        capture_output=True, text=True, check=True)
    return out.stdout.splitlines()

CHECKS = [
    # (path, lineno or None, expected substring, source)
    ("corpus/lessons/round-41.md", 21, "8 of 12 cheats scored TARGET_MET", "git"),
    ("corpus/lessons/round-41.md", 117, "M41-5 - the frozen registration's shape line contradicts the dispatched wave", "git"),
    (f"{W}/w1/CritC1Cheat.md", 18, "8 of 12 cheats scored TARGET_MET", "file"),
    (f"{W}/w1/CritC1Cheat.md", 75, "reads the stub's own bytes", "file"),
    (f"{W}/w1/CritC1Cheat.md", 83, "read_live_returned_payload=101 marker_created=0", "file"),
    (f"{W}/w1/CritC1Cheat.md", 107, "writes the journal to `<fx>/journal.txt` even when the fixture is live", "file"),
    (f"{W}/w1/CritC1Cheat.md", 115, "read_live_returned_cwd_file=1 from_program=0", "file"),
    (f"{W}/w1/CritC1Cheat.md", 166, "CH6 — clause b2 is defeated by the mutant's directory name", "file"),
    (f"{W}/w1/CritC1Cheat.md", 173, "0/6 killed and MISSED", "file"),
    (f"{W}/w1/CritC1Cheat.md", 182, "CH9 — clause b2 is defeated by a self-fingerprint", "file"),
    (f"{W}/w1/CritC1Cheat.md", 212, "CH10 — clause b2 can be aimed away from the model", "file"),
    (f"{W}/w1/RevC1Counter.md", 13, "Clause b2 is vacuous", "file"),
    (f"{W}/w1/ExecJournalFormat.md", 23, "NO_SESSIONS", "file"),
    (f"{W}/w1/RevC1Counter.md", 27, "`live0` decode-cheat `rc=0 ok=1`", "file"),
    (f"{W}/w1/ExecJournalFormat.md", 44, "byte-identical to `-o short`", "file"),
    (f"{W}/w1/ExecJournalFormat.md", 47, "The live leg has the same hole", "file"),
    (f"{W}/w1/RevRefTool.md", 18, "FIFO hangs forever", "file"),
    (f"{W}/w1/RevRefTool.md", 20, "M2 Medium — `--live` output cap is post-hoc", "file"),
    (f"{W}/w1/CritC2Cheat.md", 13, "admits all nine", "file"),
    (f"{W}/w1/CritC2Cheat.md", 27, "FORGE_SUMMARY", "file"),
    (f"{W}/w1/RevC2Counter.md", 18, "passes at 9,220 committed bytes / 9 files", "file"),
    (f"{W}/w1/ExecC2ExtraMutants.md", 43, "CTL_C2_EXTRA: mutants=45 survivors=29/45", "file"),
    (f"{W}/w1/MutC1CounterGates.md", 35, "the control suite itself is nonce-flaky (~2/22 runs)", "file"),
    (f"{W}/registration-v2.md", 3, "Supersedes the predicates and the shape line of `registration.md`", "file"),
    (f"{W}/registration-v2.md", 5, "falsified the v1 predicates **before any data commit**", "file"),
    (f"{W}/registration-v2.md", 13, "Shape (corrects `registration.md` line 4)", "file"),
    (f"{W}/registration-v2.md", 20, "compiled execute-only (0111) ELF built per fixture", "file"),
    (f"{W}/w1/MutC1CounterGates.md", 37, "flipped to MET exactly once across 22 full-suite draws", "file"),
    (f"{W}/w1/MutC1CounterGates.md", 41, "1-in-10 runs overall, and the same lottery can", "file"),
    (f"{W}/w1/MutC1CounterGates.md", 42, "fake a \"kill\" in mutation testing.", "file"),
    (f"{W}/registration-v2.md", 22, "exclusion by exact function name", "file"),
    (f"{W}/registration-v2.md", 29, "UNRECOGNIZED_FORMAT", "file"),
    (f"{W}/registration-v2.md", 29, "unrec0", "file"),
    (f"{W}/registration-v2.md", 30, "fifo0", "file"),
    (f"{W}/registration-v2.md", 32, "PINS", "file"),
    (f"{W}/receipts/ctl-c1-v2.txt", 49, "K01-stub-bytes-read", "file"),
    (f"{W}/receipts/ctl-c1-v2.txt", 50, "K02-cwd-journal-replay", "file"),
    (f"{W}/receipts/ctl-c1-v2.txt", 53, "K05-selftest-argv0-path", "file"),
    (f"{W}/receipts/ctl-c1-v2.txt", 55, "K07-selftest-size-fingerprint", "file"),
    (f"{W}/receipts/ctl-c2-v2.txt", 14, "F1-invented-receipts", "file"),
    (f"{W}/receipts/ctl-c2-v2.txt", 15, "F2-invented-journal", "file"),
    (f"{W}/receipts/ctl-c2-v2.txt", 16, "F3-unpinned-quote-boilerplate", "file"),
    (f"{W}/receipts/ctl-c2-v2.txt", 17, "F4-localized-redirect", "file"),
    (f"{W}/receipts/ctl-c2-v2.txt", 18, "F5-receipt-renamed", "file"),
    (f"{W}/receipts/ctl-c2-v2.txt", 19, "F6-one-char-location", "file"),
    (f"{W}/w1-results.json", 8, '"name": "ExecToolIndep"', "file"),
    (f"{W}/w1-results.json", 10, '"output": null', "file"),
    (f"{W}/w1-results.json", 11, "kernel restarted mid-wave; seat output was delivered to the orchestrator session but not retained", "file"),
    (f"{W}/make-w2-spec.py", 80, "no seat outputs because of a kernel restart, reports are on disk", "file"),
]

fails = []
for path, lineno, frag, src in CHECKS:
    try:
        lines = git_lines(path) if src == "git" else lines_of(path)
    except Exception as e:
        fails.append((path, lineno, frag, f"unreadable: {e}"))
        continue
    if lineno is None or lineno < 1 or lineno > len(lines):
        fails.append((path, lineno, frag, f"line {lineno} out of range (file has {len(lines)} lines)"))
        continue
    line = lines[lineno - 1]
    if frag not in line:
        fails.append((path, lineno, frag, f"fragment not on line (got: {line[:120]!r})"))

# M41-9 cites the cheat score receipt on disk.
score = os.path.join(LANE, f"{W}/w1/CritC1Cheat/score-ch1.txt")
if not os.path.isfile(score):
    fails.append((f"{W}/w1/CritC1Cheat/score-ch1.txt", None, "file exists", "missing"))
else:
    with open(score, encoding="utf-8", errors="replace") as f:
        txt = f.read()
    for frag in ("fixtures=24/24", "verdict=TARGET_MET"):
        if frag not in txt:
            fails.append((f"{W}/w1/CritC1Cheat/score-ch1.txt", None, frag, "not found in file"))

print(f"checks={len(CHECKS)+2} fails={len(fails)}")
for p, ln, fr, why in fails:
    print(f"FAIL {p}:{ln} [{fr}] {why}")
sys.exit(1 if fails else 0)
