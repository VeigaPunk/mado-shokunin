# R100MReviewC2 - adversarial review of C2 (round 100, w1)

Seat: reviewer, leaf (no subagent dispatch). Base: 43309e6af9a3b57f1bc839a826bef1f8eb7495e4
(master, HEAD verified 43309e6a). Contract attacked: .ufo/waves/round-100/claims-declaration-r100.md
section C2 (lines 66-100) and shared contract 3 (lines 134-140); predicate PRED-C2-r100-v1.

Bytes read: quality/harm-watch.py (base), quality/counters/c2-r99-harm-watch.py,
.ufo/waves/round-99/controls/harm-panel-r99.json,
.ufo/waves/round-99/receipts/c2-measured-r99.txt, c2-probe-r99.txt,
corpus/lessons/round-99.md, corpus/lessons/round-99-verifier-spotcheck.md,
corpus/QUALITY.md (round-90..99 tail), quality/harm-watch.py census/run/selftest sections.

Wave state at review time (scope limit for every verdict below):
$ ls .ufo/waves/round-100/controls/ .ufo/waves/round-100/receipts/ .ufo/waves/round-100/w1/
controls/ and receipts/ are EMPTY (no output); w1/ holds only swarm-registry.json.
$ git cat-file -e 43309e6a:quality/counters/c2-r100-harm-watch.py -> exit 128, absent at base.
So the r100 panel, counter and timing receipt do not exist yet; this review attacks the FROZEN
WORDING against current bytes. No r100 number exists to falsify. No panel/counter was executed
(host loaded; expensive runs are the L1 measurement, not this seat's).

Axes (godspeed):
1. Wording fidelity - does PRED-C2-r100-v1 enforce exactly the frozen sentence (QUALITY 172 class)?
2. Numeric derivation - is each number derived from the receipt it names, not an earlier round (QUALITY 169 class)?
3. Consumer compatibility - does the gate change break any parsed output (r99 counter, gate selftest, last-line JSON)?

## Verdict summary (one line each, full evidence below)

(a) neutral - (b) neutral - (c) neutral - (d) neutral - (e) neutral - (f) neutral.
No finding filed as falsifies-wording or falsifies-number. Four residual risks ordered at the end.

## (a) One full-panel run with mismatch=0: event or property?

Claim text: predicate "mismatches == 0" (line 84); frozen statement "...and a full-panel run at
committed bytes reports HARM_WATCH: legs=28 ... mismatch=0" (lines 76-78).

Verdict: neutral (sentence survives as written).

The sentence is event-scoped ("a full-panel run ... reports") and the predicate reads exactly that
event from the gate's HARM_WATCH summary line. It does not promise future runs. C1 in the same
declaration demands "re-measured twice with agreeing results" (lines 14-21); C2 carries no such
conjunct and its sentence asks for none. The 2x headroom conjunct is the stated mitigation for load
variance. If a later run is slower, mismatches == 0 fails and the same predicate returns
TARGET_MISSED honestly - the round-99 honest-stop behaviour - rather than the sentence being false.

$ uptime
 02:07:15  up 5 days 13:59,  1 user,  load average: 50.07, 165.29, 217.58
vs c2-probe-r99.txt: "host load at probe time: load average 327.48" - host load varies by an order
of magnitude in a day, so one mismatch=0 is a sample of that run. That is residual risk 3 below,
not a wording falsification: the heading "the panel goes green" reads as a state, but the frozen
statement (the frozen text) is the enforceable sentence and it is event-scoped.

## (b) Cap from one pass: timeout_s >= 2 * max, next run 3x slower

Claim text: panel timeout_s "equal to at least twice the largest per-leg elapsed measured on this
host at committed bytes (timing receipt ..., all 28 legs timed)"; predicate
"panel_timeout_s * 1000 >= 2 * max_elapsed_ms AND max_elapsed_ms > 600000" (lines 86-87).

Verdict: neutral (arithmetic is exactly what any counter can enforce); residual risk 1 HIGH.

The bound compares two pinned numbers (panel timeout_s from pinned panel JSON; max_elapsed_ms from
pinned timing receipt). Units are consistent and rounding is absorbed: elapsed_ms is declared
integral (shared contract 3, line 136); leg_timeout converts panel timeout_s to float seconds
(harm-watch.py:265-271). 3x slower next run: legs exceed the cap, are SIGKILLed (rc=124,
harm-watch.py:205-220), mismatches > 0, honest TARGET_MISSED. The derivation sentence stays true of
the pass that was measured. Wording survives.

Gap (why residual 1, not filed as falsifies-wording): the declaration never states the timing
pass's own timeout. To time all 28 legs un-truncated, the executor must run with a cap above the
true max; the old 600 s cap cannot yield max > 600000 (a killed leg's elapsed measures at the kill
instant, approx 600000). Proof that the base instrument cannot supply the number:
$ grep -n "elapsed" quality/harm-watch.py; echo "grep-elapsed-exit=$?"
grep-elapsed-exit=1
and c2-probe-r99.txt shows both slow legs rc=124 timeout-after-600s with no per-leg number.
A satisfiable reading exists (time legs at a larger --timeout, which the gate supports), so the
sentence is underdetermined, not false. QUALITY 169 class; the L1 should pin the timing run's cap in
the receipt header.

$ python3 -I quality/harm-watch.py --selftest
HARM_WATCH_SELFTEST: checks=26 failed=0

## (c) --rev / worktree vs committed bytes

Claim text: C1 counting command "(--rev worktree for an uncommitted candidate)" (line 52, C1 only);
C2 counting command uses --rev <MEASURED_REV> (lines 94-100) with no worktree note; frozen statement
says "at committed bytes" for both the timing measurement and the full-panel run (lines 76-78).

Verdict: neutral - C2 never authorises worktree; "committed bytes" is explicit.

$ grep -c "worktree" quality/counters/c2-r99-harm-watch.py
0
The only counter on disk reads gate/panel/planted via git show <rev>:<path> (c2-r99-harm-watch.py:
501-556); --rev worktree would fail that lookup and exit 2 SETUP_ERROR, so a worktree C2
measurement is impossible under inherited logic. A future tree-reading draft mode (c2-r99:494-504)
would contradict "committed bytes" in practice, but that mode is not invoked by the frozen C2
command. Residual (MEDIUM): the three <PIN>s in the C2 command carry no stated provenance; if any
pin were computed from worktree bytes, "committed bytes" would be hollowed out even though the text
says committed (QUALITY 171 / M99-1 class). L1 must re-derive all three pins at the measured rev.

## (d) control_600s_would_mismatch: same timing receipt, not the earlier round

Claim text: predicate "control_600s_would_mismatch >= 1 (derived from the same timing receipt: legs
whose elapsed exceeds 600 s)" (line 88).

Verdict: neutral - the text names the correct source; the earlier round cannot supply it.

$ cat .ufo/waves/round-99/receipts/c2-measured-r99.txt
MADO_HARM_WATCH: TARGET_MISSED pred=PRED-C2-r99-v1 rev=3b69f04113a235aace713bc1c84ea2b695606b6a base_rev=2cbaa141f42df9dfeee4d207cae6558a4dd59863 gate_sha256=37a0544b160d9c5c5568fc45f9ed309f41b36fb093983313d72699423b4165b9 panel_sha256=160763ce7aa447016bad8e5b2c5a7c25f8866b1e8724d8eb0b75d8abb1dae39a panel_legs=28 declared_legs=28 legs_run=28 mismatches=2 ... missed=mismatches_zero
(no per-leg elapsed anywhere; the base gate emits none)
$ cat .ufo/waves/round-99/receipts/c2-probe-r99.txt (excerpt)
LEG r92_gate_defects rc=124 expect=0 marker=MISS rc-and-marker-mismatch+timeout-after-600s
LEG r97c1_filetype rc=124 expect=0 marker=MISS rc-and-marker-mismatch+timeout-after-600s
# note: the probe ran 1201 s wall (2 legs x 600 s cap); neither leg finished inside the frozen cap.

The probe proves two legs did not finish in 600 s (elapsed >= 600000 ms at kill) but cannot supply
the strict > 600000 number the predicate needs. So the derivation must come from the new timing
receipt, and the predicate says so. No falsification. Side note (redundancy, not a defect): with
both numbers read from the same receipt, max_elapsed_ms > 600000 is logically equivalent to
control_600s_would_mismatch >= 1; the predicate carries the same fact twice and no counterexample
can separate them.

## (e) elapsed_ms vs consumers: LEG line, markers, round-99 counter

Verdict: neutral - no parsed consumer breaks under append-after-detail / JSON-last; the round-99
counter is unharmed against its pinned rev (verified). Two conditions are proven below, not assumed.

1. Insertion position on the LEG line is the only breakage vector, and it is pinned by the old
selftest. The gate's selftest asserts exact substrings (harm-watch.py:433
"LEG good rc=0 expect=0 marker=ok ok", :500 "...marker=MISS marker-missing", :508
"...marker=ok rc-mismatch"):
$ python3 (simulation over candidate LEG lines)
before selftest-substring-kept: True
bad    selftest-substring-kept: False   (elapsed inserted BEFORE detail)
good   selftest-substring-kept: True    (elapsed appended AFTER detail)
The declaration's ellipsis (line 73, "LEG <id> rc=... ... elapsed_ms=<n>") does not pin the
position, but shared contract 3 requires byte-compatible outputs and selftest_failed == 0 is a
predicate conjunct - so append-after-detail is the only implementable position. Any other choice
breaks the gate's own selftest (loud, not silent). Wording survives by constraint. Residual risk 2:
an implementer "fixing" the old assertions to fit a before-detail insertion would keep
selftest_failed == 0 while weakening the instrument (the QUALITY 172 failure mode). The L1
consolidation note should name the position explicitly.

2. expect_marker collision: none. Markers match each leg's captured stdout/stderr (harm-watch.py:
241), never the gate LEG line. All 28 markers are fixed strings; none is a substring of
"elapsed_ms=" or a bare number:
$ python3 (panel parse) -> legs= 28 timeout= 600
verify_selftest 'assertions passed'
verify_file_plane 'MADO_VERIFY: CLEAN'
index 'missing=0 dangling=0 duplicates=0'
ledger 'uncovered=0'
mako_selftest 'MADO_MAKO_SELFTEST: checks=62 failed=0'
portals_selftest 'MADO_PORTALS_SELFTEST: checks=28 failed=0'
mime_selftest 'MADO_MIME_SELFTEST: checks=17 failed=0'
xdgmime_selftest 'MADO_XDGMIME_SELFTEST: checks=12 failed=0'
mimeglob_selftest 'MADO_MIMEGLOB_SELFTEST: checks=19 failed=0'
mimesniff_selftest 'MADO_MIMESNIFF_SELFTEST: checks=26 failed=0'
seat_reports_selftest 'SEAT_REPORTS_SELFTEST: checks=23 failed=0'
receipt_presence_selftest 'RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0'
gate_selftest 'SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0'
gate_seat_reports 'SELFTEST_STRENGTH: OK tool=quality/check-seat-reports.py'
gate_mimeglob 'SELFTEST_STRENGTH: OK tool=tools/mado-mimeglob.py'
gate_portals 'SELFTEST_STRENGTH: OK tool=tools/mado-portals.py'
r90c2_receipt_presence 'MADO_RECEIPT_PRESENCE: TARGET_MET'
r92_gate_defects 'MADO_GATE_DEFECTS: TARGET_MET'
r90c1_portal_routing 'MADO_PORTAL_ROUTING: SETUP_ERROR'
r94c1_mimeglob 'MADO_MIMEGLOB_COUNT: TARGET_MET'
r94c2_selftest_kills 'MADO_SELFTEST_KILLS: TARGET_MET'
r93c2_selftest_strength 'MADO_SELFTEST_STRENGTH: TARGET_MET'
r95c1_mimesniff 'SETUP_ERROR no counting-command block'
r95c2_selftest_kills 'SETUP_ERROR no counting-command block'
r96c1_magictext 'MADO_MAGICTEXT_COUNT: SETUP_ERROR'
r96c2_selftest_kills 'MADO_SELFTEST_KILLS: TARGET_MET'
r97c1_filetype 'MADO_FILETYPE_COUNT: TARGET_MET'
r97c2_counter_selftest 'MADO_COUNTER_SELFTEST_COUNT: TARGET_MET'
No empty marker; minimum length 8; none contains "elapsed".

3. Round-99 counter unharmed - verified three ways:
a. Pin bytes untouched. git show 3b69f041:quality/harm-watch.py | sha256sum and the same at HEAD
(43309e6a) both print 37a0544b160d9c5c5568fc45f9ed309f41b36fb093983313d72699423b4165b9 - the
counter's --expect-gate-sha256 and the round-99 spot-check pin. The r99 counter reads gate bytes via
git show at --rev (c2-r99-harm-watch.py:501-512), so against 3b69f041 it is byte-identical to its
proof run. The Harm-watch paragraph sentence ("it still runs against 3b69f041 and its pinned bytes are
untouched", lines 104-107) is literally true. Its one misreading risk is the converse: it does NOT
mean the r99 counter validates the new gate - against a new rev it exits SETUP_ERROR gate sha256
(c2-r99:506-507), by design. The sentence does not claim otherwise.
b. Blind patch intact: BLIND_FROM occurs exactly once in base gate bytes (count= 1, line 241).
Adding elapsed_ms to run_panel does not touch the marker_ok line, so the marker-blind control
(count must == 1, else SETUP_ERROR) is unaffected.
c. Its parsing is field-based, not LEG-line-based: planted eval reads json legs ok/marker_ok
(c2-r99:282-294) and PANEL lines; run_gate uses a HARM_WATCH regex (c2-r99:228) and a reversed scan
for a "{" line (c2-r99:232-239). An extra leg field and an appended LEG suffix disturb none of these.
Its MINI_GATE fixture (c2-r99:85-162) prints no elapsed, but the r99 counter is never run against the
new gate with the old pin, so that fixture never needs elapsed.
Residual risk 3 (setup legs): a leg that never ran has no meaningful elapsed (harm-watch.py:192-194,
236-238), and the early-return JSON path (harm-watch.py:319-326) emits records without elapsed unless
the implementer adds them there. A setup leg already forces mismatches > 0 / exit 2, so
gate_elapsed_emitted ambiguity only matters when the run is already TARGET_MISSED; recorded as a
definition gap, not a falsification.

## (f) --json contract read as last stdout line

Verdict: neutral.

The gate prints human lines then one JSON object as the last stdout line (docstring harm-watch.py:
39-41; code :330-335). Both in-tree readers tolerate an added field: the r99 counter scans reversed
lines for a "{" line and json.loads it (c2-r99:232-239); the gate selftest does
json.loads(out.strip().splitlines()[-1]) (harm-watch.py:546-552). Extra keys cannot break
json.loads. Pre-existing caveat unchanged: census failure with --json prints no JSON
(harm-watch.py:278-282). Condition: JSON must remain last - no trailing elapsed summary line after
it; the declaration asks for none. Neutral with that condition.

## Residual risks and verification gaps

Residual risks, ordered:
1. Timing-pass protocol (b), HIGH: undeclared cap for the timing run; at 600 s the max>600000
conjunct becomes protocol-unsatisfiable. Pin the timing --timeout in the receipt header.
2. Insertion position (e), HIGH: ellipsis leaves position free; byte-compatible + selftest_failed==0
force append-after-detail. Name the position in the L1 consolidation note; never relax old selftest
substrings to fit a new position.
3. Single-sample durability (a), HIGH: no re-measure-twice conjunct (unlike C1); later load can
re-redden honestly via TARGET_MISSED. 2x headroom is mitigation, not guarantee (M99-4 class).
4. Pin provenance (c), MEDIUM: re-derive all three <PIN>s at the measured rev (QUALITY 171);
worktree-computed pins would hollow out "committed bytes".

Verification gaps (this seat did not do these): no panel/counter/timing run executed; the r100
counter does not exist at base (exit 128) so nothing in the r100 predicate was test-run; (e)/(f)
rest on code reading, the two pasted simulations, and the gate selftest at base bytes
(HARM_WATCH_SELFTEST: checks=26 failed=0). Executing the gate --json mode or any 28-leg replay is
the L1 measurement, not this seat's.

Report: .ufo/waves/round-100/w1/R100MReviewC2.md
