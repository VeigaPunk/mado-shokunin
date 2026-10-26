#!/usr/bin/env python3
"""CritC2Cheat: verify every quotation and every log claim the seat report makes.

Each QUOTE tuple is (file, 1-based line, substring); each LOG tuple is (log, regex).
Exit 0 only if every check passes; writes run-verify.log.
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-43/w1/CritC2Cheat")
COUNTER = os.path.join(LANE, "quality/counters/c2-r43-gkeep-entry.py")
CTL = os.path.join(LANE, ".ufo/waves/round-43/ctl/run-c2-controls.py")
F = os.path.join(LANE, ".ufo/waves/round-43/fetch")

QUOTES = [
    (COUNTER, 25, ">= 4 distinct `source: S###` lines,"),
    (COUNTER, 54, "per cited id, one entry line (outside fences) names the id, names no other cited id,"),
    (COUNTER, 73, "reason=<text of >= 4 distinct words>"),
    (COUNTER, 82, "a real receipt can be cited for a claim it does not"),
    (COUNTER, 283, "def host_census(new_ids, reg_rev, gates, receipts_raw, lines):"),
    (COUNTER, 421, "if (blob is not None and len(blob) >= MIN_RECEIPT and pin_ok"),
    (COUNTER, 427, "and quote_at(blob, nq) is not None):"),
    (COUNTER, 490, 'hit = any(re.search(r"\\b%s\\b" % i, l) and q in l'),
    (COUNTER, 503, "staged_ok = lambda p: os.path.basename(p) in STAGED"),
    (COUNTER, 506, "and len(set(m.group(2).lower().split())) >= 4"),
    (COUNTER, 512, 'row_text = " ".join(rows[0]).lower()'),
    (CTL, 28, "merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md"),
    (CTL, 38, "https://example.org/src/desktop/rule/matchEngine/RegexMatchEngine.cpp"),
    (CTL, 44, "https://example.org/src/layout/target/Target.cpp"),
    (CTL, 62, "CENSUS = [RULES_LINE, CLIENTS_LINE, UI_LINE]"),
    (os.path.join(F, "Hyprland-DefaultFloatingAlgorithm.cpp"), 105, "// TODO: not very OOP, is it?"),
    (os.path.join(F, "Hyprland-WindowTarget.cpp"), 102, "// Reserved area must be updated before this is called"),
    (os.path.join(F, "Hyprland-WindowTarget.cpp"), 126, "// Reserved area must be updated before this is called"),
    (os.path.join(F, "Hyprland-WindowRuleApplicator.cpp"), 174, "const auto& expr = std::get<Math::SExpressionVec2>(value);"),
    (os.path.join(F, "Hyprland-WindowRuleApplicator.cpp"), 422, "const auto& expr = std::get<Math::SExpressionVec2>(value);"),
    (os.path.join(F, "Hyprland-Target.cpp"), 11, "m_box = box;"),
    (os.path.join(F, "host-gkeep.conf"), 4, "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"),
]

LOGS = [
    ("run-forgeries.log", r"^### P-genuine\s+rc=0 admitted=1/1"),
    ("run-forgeries.log", r"^### B2-second-locator-negative\s+rc=1 admitted=0/1.*clauses=.*g:0"),
    ("run-forgeries.log", r"^=== forged fixtures admitted by the frozen counter: 14/15"),
    ("run-probes.log", r"probe=unique-occurrence\s+fixture=P-genuine\s+rc=0 admitted=1/1"),
    ("run-probes.log", r"probe=unique-occurrence\s+fixture=B1-second-occurrence\s+rc=1 admitted=0/1"),
    ("run-probes.log", r"probe=quote-not-in-comment\s+fixture=P-genuine\s+rc=0 admitted=1/1"),
    ("run-probes.log", r"probe=quote-not-in-comment\s+fixture=C1-comment-quote\s+rc=1 admitted=0/1"),
    ("run-probes.log", r"probe=every-naming-line-bound\s+fixture=P-genuine\s+rc=0 admitted=1/1"),
    ("run-probes.log", r"probe=every-naming-line-bound\s+fixture=E1-id-contradiction\s+rc=1 admitted=0/1"),
    ("run-probes.log", r"probe=package-path-exact\s+fixture=P-genuine\s+rc=0 admitted=1/1"),
    ("run-probes.log", r"probe=package-path-exact\s+fixture=F1-fake-package-dir\s+rc=1 admitted=0/1"),
    ("run-probes.log", r"probe=url-exact-NEGATIVE\s+fixture=P-genuine\s+rc=1 admitted=0/1"),
    ("run-more.log", r"X3-own-work-only\s+rc=0 admitted=1/1"),
    ("run-more.log", r"X1-index-row-lie\s+rc=0 admitted=1/1"),
    ("run-more.log", r"probe=refuse-flip-marker P-genuine rc=0 admitted=1/1"),
    ("run-more.log", r"probe=refuse-flip-marker F2-refuse-no-flip rc=1 admitted=0/1"),
    ("run-more.log", r"probe=bad-loc-in-entry P-genuine rc=0 admitted=1/1"),
    ("run-more.log", r"probe=bad-loc-in-entry X2-localized-in-entry rc=1 admitted=0/1"),
    ("run-more.log", r"probe=all-pins-cited P-genuine rc=0 admitted=1/1"),
    ("run-more.log", r"probe=all-pins-cited X3-own-work-only rc=1 admitted=0/1"),
]

ok = True
out = []
for path, ln, sub in QUOTES:
    try:
        line = open(path, encoding="utf-8").read().splitlines()[ln - 1]
        hit = sub in line
    except (OSError, IndexError) as exc:
        line, hit = "ERR %s" % exc, False
    ok &= hit
    out.append("%s %s:%d %r" % ("OK  " if hit else "FAIL", os.path.basename(path), ln, sub[:60]))
    if not hit:
        out.append("      got: %r" % line.strip()[:140])
for log, rx in LOGS:
    try:
        text = open(os.path.join(SEAT, log), encoding="utf-8").read()
        hit = re.search(rx, text, re.M) is not None
    except OSError as exc:
        hit = False
        out.append("      ERR %s" % exc)
    ok &= hit
    out.append("%s %s /%s/" % ("OK  " if hit else "FAIL", log, rx[:80]))

# provenance fixtures: the real staged dir holds the package file, the forged one does not
real = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md"
fake = "/home/vgpnk/Projects/shokuknow/merge/mado/not-a-real-dir/gkeep-size-to-real-size-r11.md"
for p, want, tag in ((real, True, "real-staged-path-exists"), (fake, False, "fake-staged-path-absent")):
    hit = os.path.isfile(p) == want
    ok &= hit
    out.append("%s %s %s" % ("OK  " if hit else "FAIL", tag, p))

out.append("VERIFY %s" % ("PASS" if ok else "FAIL"))
open(os.path.join(SEAT, "run-verify.log"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(0 if ok else 1)
