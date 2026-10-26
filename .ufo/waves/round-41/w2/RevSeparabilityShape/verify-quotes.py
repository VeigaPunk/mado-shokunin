#!/usr/bin/env python3
"""Verify every located quote in findings.md and RevSeparabilityShape.md is <= 25 words
and occurs verbatim in the referenced committed blob or receipt file."""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PROTO = "/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

# Each entry: (id, source_spec, location_label, quote)
# source_spec is either ("git", rev, relpath) or ("file", abspath)
QUOTES = [
    ("Q01", ("file", f"{PROTO}/AXES.md"), "AXES.md:30-34",
     "Claims must be **causally separable** — each verifiable without the others having landed — and name **distinct axes**"),
    ("Q02", ("file", f"{PROTO}/AXES.md"), "AXES.md:33-34",
     "At least one claim works the lane's **lowest-scoring non-retired axis**, except when the stagnation nudge (below) waives it."),
    ("Q03", ("file", f"{PROTO}/AXES.md"), "AXES.md:68-71",
     "When every axis the lane owns sits at or above the lane's saturation line and no capability has entered the table"),
    ("Q04", ("file", f"{PROTO}/PROTOCOL.md"), "PROTOCOL.md:143-144",
     "and files at least one claim of the round as *sourced* — its evidence citing an `S###` row."),
    ("Q05", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/registration-v2.md"),
     ".ufo/waves/round-41/registration-v2.md:8-10",
     "the v1 predicates were scored by w1 seats (`CritC1Cheat`, `ExecToolIndep`, `ExecC1ExtraMutants`, `ExecC2ExtraMutants`, `CritC2Cheat`), so v2 was written after seats had seen v1 scores;"),
    ("Q06", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/registration-v2.md"),
     ".ufo/waves/round-41/registration-v2.md:10-11",
     "and the operator rules which predicate binds - the report gives both scores at the data tip."),
    ("Q07", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/registration-v2.md"),
     ".ufo/waves/round-41/registration-v2.md:13-14",
     "Two v1 waves: `w1` of 34 seats (build + first falsifiers, policy v1 band 32-64) and `w2` of 34 seats"),
    ("Q08", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/registration-v2.md"),
     ".ufo/waves/round-41/registration-v2.md:40",
     "**Target:** `fixtures=39/39 tool=present verdict=TARGET_MET`, exit 0, at the data commit and at the tip."),
    ("Q09", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/registration-v2.md"),
     ".ufo/waves/round-41/registration-v2.md:45",
     "**Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0. **Kill rule:** as C1."),
    ("Q10", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/registration-v2.md"),
     ".ufo/waves/round-41/registration-v2.md:46",
     "**Separability** is unchanged: C1 reads only `tools/mado-globals.py`; C2 reads only the entry, registry, lesson, README and the pinned receipts"),
    ("Q11", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/registration-v2.md"),
     ".ufo/waves/round-41/registration-v2.md:50",
     "and the 42 `ExecC1ExtraMutants` mutants each score below MET."),
    ("Q12", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/registration-v2.md"),
     ".ufo/waves/round-41/registration-v2.md:51",
     "every other control scores `0/1` (forgeries under the real counter, clause mutants under a counter whose PINS also hold the fixture's receipts,"),
    ("Q13", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/receipts/ctl-c1-v2.txt"),
     ".ufo/waves/round-41/receipts/ctl-c1-v2.txt:1",
     "CTL_C1V2: skipped-patterns-absent=4 W1-N14-empty-file-expect-ok W1-N24-ver-5-digits-max W1-N35-read-only-max-bytes W1-N42-live-no-timeout"),
    ("Q14", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/receipts/ctl-c1-v2.txt"),
     ".ufo/waves/round-41/receipts/ctl-c1-v2.txt:97",
     "CTL_C1V2: controls=95 correct=95/95"),
    ("Q15", ("git", "294c667901a8c7b7165ba849d03cba9a24c14fa4", ".ufo/waves/round-41/receipts/ctl-c1-v2-extra.txt"),
     ".ufo/waves/round-41/receipts/ctl-c1-v2-extra.txt:5",
     "CTL_C1V2: controls=3 correct=3/3"),
    ("Q16", ("git", "60c3914154333180450d5da27ba222d5763cc56a", ".ufo/waves/round-41/registration.md"),
     ".ufo/waves/round-41/registration.md:7-8",
     "Every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 58/58, calibration 55/55, operability 12/12, `MADO_AXIS checked=3 mismatched=0`),"),
    ("Q17", ("git", "07f2641696b5ac73de1404ea737a9f27e9819aa1", "corpus/lessons/round-41.md"),
     "corpus/lessons/round-41.md:38",
     "the seven pre-wave receipts are committed at the freeze (`git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/`);"),
    ("Q18", ("git", "07f2641696b5ac73de1404ea737a9f27e9819aa1", "corpus/lessons/round-41.md"),
     "corpus/lessons/round-41.md:163-164",
     "`PRED-C1-r41-v1` at the data commit: `fixtures=24/24 verdict=TARGET_MET` with the nonce printed; `PRED-C2-r41-v1`: `admitted=1/1 verdict=TARGET_MET`; both re-run at the tip."),
    ("Q19", ("file", f"{LANE}/.ufo/waves/round-41/receipts/c1-v1-after-data.txt"),
     ".ufo/waves/round-41/receipts/c1-v1-after-data.txt:34",
     "PRED-C1-r41-v1: fixtures=6/24 tool=present verdict=TARGET_MISSED rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 nonce=cb2bcd4259089823"),
    ("Q20", ("git", "07f2641696b5ac73de1404ea737a9f27e9819aa1", "corpus/lessons/round-41.md"),
     "corpus/lessons/round-41.md:45",
     "its S328–S332 rows are the package's ids with no lane receipt; re-grounded this round as C2 with lane ids S283–S290"),
]


def load_source(spec):
    kind = spec[0]
    if kind == "file":
        return open(spec[1], encoding="utf-8").read()
    _, rev, path = spec
    return subprocess.check_output(
        ["git", "-C", LANE, "show", f"{rev}:{path}"], text=True, env=ENV
    )


def main():
    bad = 0
    for qid, spec, loc, quote in QUOTES:
        words = len(quote.split())
        raw = load_source(spec)
        flat_raw = re.sub(r"\s+", " ", raw)
        flat_q = re.sub(r"\s+", " ", quote)
        ok_len = words <= 25
        ok_in = flat_q in flat_raw
        ok = ok_len and ok_in
        if not ok:
            bad += 1
        print(f"{qid} words={words:2d} <=25={int(ok_len)} in_source={int(ok_in)} loc={loc}")
    print(f"QUOTE_VERIFY: total={len(QUOTES)} ok={len(QUOTES)-bad}/{len(QUOTES)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
