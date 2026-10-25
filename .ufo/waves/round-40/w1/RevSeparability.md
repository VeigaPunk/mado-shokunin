# RevSeparability — round 40 w1: separability & axis-naming review of C1/C2

Seat: RevSeparability (leaf; no subagents, no background jobs). Scope: judge the frozen
registration (`registration.md` @ freeze `5e7e88525cc539563de7746361b2650802e81809`, base
`9fc511ddce708327377161202f358ce37dc266ba` — verified: `git rev-parse 5e7e8852^` = base; the
freeze adds exactly registration, both counters, both control harnesses, receipts, capture, ref
tool) against the shokunin protocol's claim-sizing rules
(`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md` §"Working the axes",
`PROTOCOL.md` §"Fleet-2 conventions" first bullet), with counters run against synthetic states.
Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`. All paths below relative to it unless
absolute.

Rules applied (quoted):
- AXES.md: "Claims must be **causally separable** — each verifiable without the others having
  landed — and name **distinct axes**; two claims on one axis in one round count as one claim."
- AXES.md: "A round is admitted only if every claim verifies **and no axis is harmed**."
- PROTOCOL.md Fleet-2: "each an axis-move on a distinct axis with its own falsifiable before→after;
  at least one on the lane's lowest non-retired axis".
- AXES.md coverage definition: "Fraction of the domain's real surfaces the skill governs (repo
  paths, tools, edge classes)"; claim measurement standard: "file exists / command runs /
  citation resolves".

## Verdicts on the four assigned questions

1. **Causally separable: YES at the counter level, with one undeclared ordering constraint (F1).**
2. **Distinct axes by surface changed: YES (F5), with the clause-h hash edge as the one shared
   file (F1).**
3. **Quality-not-coverage trap in C2's counter: PRESENT — a sourceless fixture counts identically;
   declared as residual, sharpened here (F2).**
4. **Do-nothing control per claim: PRESENT for both (F6).**

## Findings

### F1 · Medium — registration's separability justification is half-wrong; undeclared tip-ordering constraint
`registration.md` §C2 Separability states: "C2's counter passes a dummy tool (control P) without
C1's verdict, and **C1 shares no file with C2**." The first half is true (re-executed: control P
scores `admitted=1/1` with tool bytes `#!/usr/bin/env python3\n# tool bytes v1\n`,
`ctl/run-c2-controls.py` `TOOL_SRC`). The second half is false at the predicate level: C2's clause
h hashes the exact file C1 delivers — `quality/counters/c2-r40-forms-entry.py` (`TOOL =
"tools/mado-options.py"`, and in `score()`: `hashlib.sha256(tool).hexdigest() in rtext` where
`tool = show(repo, rev, TOOL)`). The deliverable file *sets* are disjoint; the *predicates* are
not.

Demonstrated (synthetic fixture repo, `mktemp -d`, toplevel verified, throwaway identity via
`-c`): an admitted C2 state scores `1/1 TARGET_MET` at its data commit while C1 has not landed;
after a later commit edits `tools/mado-options.py` (simulating C1 landing afterwards), the same
state at that tip scores `0/1 TARGET_MISSED` with `h:0`; re-running at the data commit returns
`1/1`. This is exactly the failure the harness's own control N17
(`receipts/ctl-c2.txt`: `N17-receipt-tool-sha-stale … h:0`) encodes — the harness knows the
coupling the registration's sentence denies.

Consequence: a hard, undeclared ordering constraint — **C1's final tool bytes must land before or
with C2's own-work receipt; any tool edit after that receipt requires regenerating the receipt**
(a data commit, allowed). Not a predicate breach: the frozen counters remain satisfiable. Since
`registration.md` is frozen (any edit is a new predicate → the claim fails as declared), the
correction must land in the round report/lesson, not the registration.

### F2 · Medium — quality-not-coverage trap: present, declared, sharpened
C2's counter counts rows a sourceless fixture also counts. Demonstrated: an admitted state whose
three new registry rows carry locations resolving to nothing (`zzz-no-such-surface-1`,
`nowhere://nothing`, `zzz-no-such-surface-2`) scores `admitted=1/1 TARGET_MET` (all clauses
`a:1…h:1`). Control P (example.org URLs, dummy tool, invented counts) also scores `1/1`
(re-executed: `CTL_C2: controls=21 correct=21/21`). Mechanism: the only location property tested
is string uniqueness (clause e: `same == [i]` over the last whitespace token of cell 1); nothing
resolves a location, opens pinned bytes, or ties a receipt to its location. So the produced number
(`admitted=1/1`) measures **admission wiring** (rows exist, receipts hash-match, quotes occur,
index row present), not coverage of real surfaces — the axis the claim names. The registration
DECLARES this residual ("a fully fabricated, self-consistent set … passes; committed bytes cannot
prove the receipt is what the location served or what the compositor answered"), so it is not a
predicate breach — but the round report should state what the number means: coverage-as-counted =
distinct location strings + hash-wired receipts. Under AXES.md's own measurement standard
("citation resolves") the counter exceeds it for receipts and never reaches it for locations.

### F3 · Low — C2 clause c is stricter than the corpus contract on the cited held rows
Clause c requires cited held rows' cells 1–10 byte-equal to BASE (`old[0][:10] == cells[:10]`;
only `used-by`, cell 11, may change). CORPUS.md §SOURCES rules: "Only `status`, `recheck` and
`used-by` change in place, and each change is logged old→new in the round lesson." So a legitimate
freshness act on S162/S173 this round (re-verification updating `recheck`) breaks clause c → C2
fails as counted. The byte-equality is declared (counter docstring: "a held row is re-opened,
never rewritten"; registration: same sentence), but the interaction with CORPUS.md's in-place
rules is not spelled out. L1 guidance: leave `status`/`recheck` untouched on S162/S173; log the
re-open purely as a `used-by` append.

### F4 · Low — C2's *evidence production* depends on C1's deliverable, though its *verification* does not
Clause h binds the own-work receipt to the sha256 of `tools/mado-options.py` at REV and to the
census count lines. The honest producers of those counts are (a) the delivered `--live` tool
(C1's deliverable, final bytes) or (b) ad-hoc seat labeling. If C1 has not landed, a receipt
embedding the base tool's sha attributes the census to a tool that cannot produce it — the sha
binding's attribution purpose is defeated. So: counter-level separability holds (control P),
evidence-level separability does not. The declared fabrication residual covers the unverifiable
provenance; the attribution nuance is undeclared. One sentence in the entry or round report (who
ran the census, with which program) closes it.

### F5 · PASS — distinct axes by the surface the round changes
C1's surface: `tools/mado-options.py` (new `--live`/`--hyprctl`/`--probe`, selftest growth to
n ≥ 79, clause b). C2's surface: `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` +
`corpus/SOURCES.md` rows + `corpus/lessons/round-40.md` Gate + `corpus/README.md` index + fetch
receipts. Distinct counters over distinct files (sole overlap: the clause-h hash edge, F1); the
numbers produced (`fixtures=13/13` vs `admitted=1/1`) come from different counters — axes named by
surface, not by number. Grep evidence: `quality/counters/c1-r40-live.py` contains zero references
to corpus/SOURCES/lessons/README/knowledge; `quality/counters/c2-r40-forms-entry.py` never reads
the capture (only `capture_output=True` matches). C1 also fits AXES.md's capability-acquisition
form ("it still lands a per-axis verdict"); the capabilities-table row must enter via this round's
demonstration per AXES.md ("Rows enter only through a round that demonstrates the capability
running") — the registration does not name that row; the round report must.

### F6 · PASS — do-nothing control present for each
- C1: `BASE-tool` control in `ctl/run-c1-controls.py` scores `fixtures=0/13`
  (`receipts/ctl-c1.txt`); independently re-executed at base:
  `fixtures=0/13 … verdict=TARGET_MISSED`, exit 1, matching `receipts/c1-before-base.txt`.
- C2: `N01-no-entry` (admitted state minus the entry) scores `0/1` in the harness, and the lane
  base itself scores `admitted=0/1`, exit 1 — re-executed, matching
  `receipts/c2-before-base.txt`.

### F7 · PASS — saturation / lowest-axis claims are honest
Re-ran `python3 -I quality/check-axis-scores.py --repo . --rev 9fc511d…`:
`navigation published=56/56`, `calibration published=51/51`, `operability published=12/12`,
`MADO_AXIS: checked=3 mismatched=0` — matches `receipts/axis-base.txt` and the registration's
lowest-axis paragraph. All published axes tie at max → each is a lowest axis; C1 works operability
→ the lowest-axis obligation is met. The nudge reasoning is consistent with AXES.md (the nudge
waives the obligation only when no capability entered within window N; a round-39 capability row
inside N=3 means it does not fire, so the obligation stands and is satisfied by C1).

### F8 · checked-and-cleared — held-row feasibility and citation-anchor semantics
S162 and S173 exist at base with 11 cells, status `mined` (214 registry rows parse; S162 anchors
`ConfigManager.cpp:419-451,590-623,893-968,2016-2093 @ efb5099… sha256:9db68cf4…`, S173 anchors
`config.cpp:619-667,755-827,983-986 @ 3a1c1b25… sha256:fa1b6898…`) — clause c is landable.
`corpus/README.md` at base has 56 rows matching the counter's index pattern — clause f landable.
`corpus/lessons/round-40.md` is absent at base (counter reads it at REV only — fine). The entry
citing S162/S173 for line ranges outside the rows' anchor cells (gradient handler ~103-170;
`configStringToInt` 185-264) is NOT a defect under CORPUS.md: the entry's own `source:` line must
carry the URL and anchor alongside the S### row; the row is the registry identity. The counter
does not check the entry's anchor presence — that duty falls to corpus review, not the counter
(verification gap, below).

## Residual risk & verification gaps
- I did not re-run the C1 controls harness end-to-end (18 controls × full counter runs, minutes);
  the frozen `receipts/ctl-c1.txt` stands, and I independently re-executed its two load-bearing
  controls (BASE-tool at base; REF-reachability reproduced in a synthetic repo — ref tool scores
  `fixtures=13/13`, `clauses=a:1 b:0 g:1 k:1`, `TARGET_MISSED`, i.e. reachable-but-not-met, with
  `corpus/` entirely absent from that repo).
- E2/E3/E4 are synthetic-state demonstrations in throwaway repos; they establish counter behavior,
  not host truth. The counters' clause semantics are frozen; no finding above requires a predicate
  change — F1's correction lands in the round report/lesson (registration is frozen).
- Clause-h provenance (which program produced the census counts) is unverifiable from committed
  bytes — declared residual (F4 adds the attribution nuance).
- The entry's `source:` anchor lines (URL + line range per CORPUS.md) are not counter-checked;
  corpus review must cover them.

Tooling: none installed (none needed; pacman untouched, per the host-wide pause).
Scratch: all synthetic repos under `/tmp` (mktemp -d), removed after each experiment; no lane
writes outside this report; no mutating git anywhere (lane reads: rev-parse/diff/show/log only).
