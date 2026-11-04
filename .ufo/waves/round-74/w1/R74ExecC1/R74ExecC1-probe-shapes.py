#!/usr/bin/env python3
"""R74ExecC1 probe: three extra output shapes against the committed round-74 rule.

Shape A: witness printed AFTER the summary.
Shape B: witness on stderr only (rule sees concatenated stdout+stderr in the real
         measurement; probed both ways).
Shape C: two summaries with one witness (last parsed summary governs).
"""
import runpy
import sys

RULE = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r74-witness-rule.py"
mod = runpy.run_path(RULE)
credit = mod["credit"]
last_witness = mod["last_witness"]
last_parsed_summary = mod["last_parsed_summary"]
count_fails = mod["count_fails"]

NONCE = "f5497b8e9cd0f045"  # the committed receipt's challenge, shape-only
FAIL = "SELFTEST FAIL 9: zero citations refused want=1 got=0\n"
SUM12 = "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n"
SUM22 = "MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\n"
WIT = "MADO_LANDING_WITNESS: %s\n" % NONCE

def show(name, out, nonce=NONCE):
    line = last_parsed_summary(out)
    print("PROBE %-28s credit=%-5s last_summary=%r fails=%d last_witness=%s"
          % (name, credit(out, nonce), line, count_fails(out), last_witness(out)))

# Shape A: witness AFTER the summary (arithmetic failing like a genuine run)
show("A-witness-after-summary", FAIL + SUM12 + WIT)
# control: the genuine order with same bytes reversed comparison
show("A-control-witness-before", WIT + FAIL + SUM12)

# Shape B: witness on stderr only
stdout_only = FAIL + SUM12
stderr_only = WIT
show("B-witness-stderr-combined", stdout_only + stderr_only)
show("B-witness-stderr-stdoutonly", stdout_only)
show("B-witness-stderr-stderronly", stderr_only)

# Shape C: two summaries with one witness
show("C-two-sum-last-green", WIT + SUM12 + FAIL + SUM22)
show("C-two-sum-last-failing", WIT + SUM22 + FAIL + SUM12)
show("C-two-sum-last-zero-of-two", WIT + SUM22 + FAIL + FAIL
     + "MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\n")

# extra grammar edge from shape A: witness after a malformed trailing marker
show("A2-witness-after-malformed",
     FAIL + SUM12 + "MADO_LANDING_COUNTERS_SELFTEST: cleanup\n" + WIT)
