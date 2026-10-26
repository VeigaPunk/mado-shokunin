#!/usr/bin/env python3
"""Verify every quote this seat lifted from a lane file: it must occur, whitespace-normalised, on the cited line,
and be <= 25 words. Run from the lane root. Prints one line per claim and a SUMMARY line."""
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"

CLAIMS = [
    (".ufo/waves/round-46/registration.md", 47, "The two cross-scope URL repeats"),
    (".ufo/waves/round-46/registration.md", 34, "A pre-freeze run met V03 (case-insensitive names)"),
    (".ufo/waves/round-46/ctl/run-c2-controls.py", 17, "the first cut's single-occurrence assertion stopped the runner before any score"),
    (".ufo/waves/round-46/ctl/run-c2-controls.py", 126, "assert reg.count(url) == 1"),
    (".ufo/waves/round-46/receipts/ctl-c1.txt", 7, "V03-case-insensitive-names rc=1"),
    (".ufo/waves/round-46/receipts/ctl-c2.txt", 9, "CTL_C2 FALSE-URL want=rejected got=rejected rc=1 ok"),
    (".ufo/waves/round-46/w1/MutC1Counter.md", 33, "V03 (case-insensitive names): fixture `case-exact-dump-name` FAIL in all three runs"),
    (".ufo/waves/round-46/w1/MutC1Counter.md", 78, "The control set's only load-bearing channel is clause f's exactness"),
    (".ufo/waves/round-46/w1/CritC2Forgery.md", 10, "10 were admitted"),
    (".ufo/waves/round-46/w1/CritC2Forgery.md", 14, "6 admitted forgeries are NOT declared"),
    (".ufo/waves/round-46/w1/CritW2Gate.md", 14, "22 of 22 attack shapes pass it"),
    (".ufo/waves/round-46/w1/CritW2Gate.md", 15, "5 of 6 legitimate shapes are flagged"),
    (".ufo/waves/round-46/w1/CritW2Gate/receipts.txt", 21, "caught 0/19"),
    (".ufo/waves/round-46/w1/CritW2Gate/receipts.txt", 28, "caught 5/6"),
    (".ufo/waves/round-46/w1/CritW2Gate/receipts.txt", 60, "files=17098 findings=102"),
    (".ufo/waves/round-46/w1/ExecSessionTriage.md", 47, "False positives: **0**. Every match is a genuine dump-shaped object"),
    (".ufo/waves/round-46/w1/CritW2Entry/report.md", 40, "the real gate is uncited (mis-located)"),
    (".ufo/waves/round-46/w1/CritW2Entry/report.md", 64, "false provenance, claim true"),
    (".ufo/waves/round-45/receipts/live-monitors-host-l1.txt", 4, "tool sha256 c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be"),
    (".ufo/waves/round-45/receipts/live-monitors-host-r45.txt", 4, "2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609"),
    (".ufo/waves/round-46/w1/CritRegistration.md", 16, "F1 (wrong count)"),
    (".ufo/waves/round-46/w1/CritRegistration.md", 55, "F3 (stale pointer)"),
    (".ufo/waves/round-46/w1/CritPremise.md", 20, "5 duplicate-URL introductions declared as 2"),
    (".ufo/waves/round-46/w1/ExecC2Census.md", 151, "count is not witnessed by its cited range"),
    (".ufo/waves/round-46/w1/CritEntryContent.md", 67, "is a hard config error, not a silent no-op"),
    (".ufo/waves/round-46/w1/ExecSerialRule/receipts/base-scope-all-r5-r6.txt", 49, "R5_SERIAL_PROSE=24 R6_SERIAL_EXACT=24"),
    (".ufo/waves/round-46/w1/ExecSerialRule/receipts/projected-scope-all-r5-r6.txt", 1, "findings=0 rev=cb46276e"),
    ("quality/counters/c2-r46-input-device-entry.py", 72, "registry cells 3-6 of a new row are not read except the scope cell"),
    (".ufo/waves/round-46/w1/ExecW2Monitors/adversarial.txt", 200, "ADVERSARIAL: 22/22 match my reading of the pins"),
    (".ufo/waves/round-46/w1/ExecW2Monitors/c1-nonces.txt", 10, "fixtures=81/81 generated=150/150"),
    ("quality/counters/c1-r46-devices.py", 375, 'env={"PATH": "/usr/bin:/bin"'),
    ("quality/counters/c1-r46-devices.py", 9, "nothing in the lane is"),
    ("quality/counters/c1-r46-devices.py", 101, "spec.loader.exec_module(mod)"),
    (".ufo/waves/round-46/w1/SentTool/evidence/clause-r-bypass-absolute-path.txt", 96, "clause=r marker=absent"),
    (".ufo/waves/round-46/w1/SentTool/evidence/clause-r-bypass-absolute-path.txt", 97, "readonly=ok tool=present verdict=TARGET_MET"),
    (".ufo/waves/round-46/w1/SentTool/evidence/clause-r-bypass-selftest-path.txt", 95, "clause=r marker=absent"),
    (".ufo/waves/round-46/w1/SentTool/evidence/clause-r-bypass-selftest-path.txt", 96, "readonly=ok tool=present verdict=TARGET_MET"),
    (".ufo/waves/round-46/w1/SentTool/evidence/sandbox-reachability.txt", 6, "sock_count=1"),
    (".ufo/waves/round-46/w1/SentTool/evidence/sandbox-reachability.txt", 9, "read_hypr_conf=yes"),
    (".ufo/waves/round-46/w1/SentTool/evidence/sandbox-reachability.txt", 10, "list_seat_scratch=25 other_seat_dirs_visible"),
    (".ufo/waves/round-46/w1/SentTool/evidence/socket-ro-bind.txt", 3, "CONNECT_OK"),
    ("corpus/QUALITY.md", 246, "fail-closed setup is not containment"),
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


DRAFT = LANE + "/.ufo/waves/round-46/w1/ScrMistakes/mistakes.md"


def main():
    found = miss = long_ = draft_miss = 0
    draft = norm(open(DRAFT, encoding="utf-8").read())
    strip = lambda t: t.replace("`", "").replace("*", "")
    for path, line, quote in CLAIMS:
        try:
            lines = open(LANE + "/" + path, encoding="utf-8", errors="replace").read().split("\n")
        except OSError as e:
            print("QUOTE %s:%d MISS open-error %s" % (path, line, e))
            miss += 1
            continue
        body = norm(lines[line - 1]) if 0 < line <= len(lines) else ""
        words = len(norm(quote).split())
        ok = norm(quote) in body
        if words > 25:
            long_ += 1
            print("QUOTE %s:%d LONG words=%d" % (path, line, words))
        if ok:
            found += 1
            in_draft = strip(norm(quote)) in strip(draft)
            draft_miss += not in_draft
            print("QUOTE %s:%d MATCH words=%d draft=%s" % (path, line, words, "yes" if in_draft else "NO"))
        else:
            miss += 1
            print("QUOTE %s:%d MISS words=%d line=%r" % (path, line, words, body[:120]))
    print("SUMMARY: claims=%d found=%d not_found=%d over_25_words=%d draft_missing=%d" % (
        len(CLAIMS), found, miss, long_, draft_miss))
    return 0 if miss == 0 and long_ == 0 and draft_miss == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
