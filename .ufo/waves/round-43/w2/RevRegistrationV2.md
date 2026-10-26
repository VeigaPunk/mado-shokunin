# RevRegistrationV2 — report (round 43, w2, inline v1)

Scope: review the C2 v1→v2 re-registration (`registration-v2.md`, freeze `496340d`, before data
`1959770`) — attacks 'frozen before any data' and 'the docstring is the code'. Full detail, evidence and
reproductions: `.ufo/waves/round-43/w2/RevRegistrationV2/findings.md`.

**Verdict: the re-registration is sound. All four assigned checks PASS. No HIGH, no MEDIUM; three LOW
findings (two prose inaccuracies in registration-v2.md, one docstring-scope nuance in the v2 counter).**

1. **Commit order and content — PASS.** `496340d` is the direct parent of `1959770`
   (`merge-base --is-ancestor` OK; dates 04:46:54 → 04:46:55). At the freeze: entry, lesson and
   `tools/mado-geometry.py` absent (`git ls-tree` empty); canonical `corpus/SOURCES.md` has zero `S29x`
   mentions; S155/S158 present without the used-by append. v1 counter blob `a58c3402…` byte-identical at
   b2e2efd/496340d/1959770; v2 blob `03f007d3…` identical at 496340d/1959770. The freeze's committed
   fixtures reproduce **byte-identically** from the committed harness (only `WORK`/`SEAT` redirected to
   scratch) and share no prose with the landed entry (only the three census lines + the date line — same
   host facts by design). [INFO-1: the 1-second commit gap; the DAG is the ordering proof — "frozen
   before data" holds at commit granularity.]
2. **Diff ↔ docstring — PASS.** My diff of the two committed blobs is byte-identical to the frozen
   `receipts/c2-v1-to-v2.diff` (`cmp` IDENTICAL; 10 hunks, 97 changed lines — matching
   registration-v2.md:19). Every code change maps to a docstring statement (d+/e+/g+/i+ → patch sites at
   v2 lines 501-503, 535-537, 576, 582-583, 587-589, 596-598; helpers 294-349; PRED name 2/117), and
   every docstring condition has code. [LOW-1: the header's "(each also stated in its clause below)"
   (counter docstring line 8) is not literally true — the clause bodies are unchanged v1 text; the
   conditions live only in the header note. LOW-3: registration-v2.md:19 says "three helper functions
   from the probe"; the diff and `w1/CritC2Cheat/probes.py` carry four.]
3. **Killing controls — PASS (rerun-verified).** Fresh reruns of the committed forgery harnesses
   (redirected to scratch) reproduce `forge-v2.log` and `more-v2.log` exactly (modulo the L1's trailing
   `exit=0` capture line); the harness's printed counter sha equals the committed v2 blob's sha256.
   d+ ← B1/B2 (second occurrence / non-first locator) and C1/C2 (comment quotes), all `d:0`; e+ ← G1/G2
   (fake/relative URL), `e:0`; g+ ← E1 (id named on a line without its quote), `g:0`; i+ ← F1 (fake
   package dir), F2 (no flip word), X2 (BAD_LOC in entry prose, isolated by probe), X3 (own-work-only,
   all-PINS probe), `i:0` — every i+ sub-condition isolated by a probe that keeps P admitted. Still
   admitted: A1, A2, D1, E2, H1, X1 — exactly the declared claim-binding residual.
4. **Control P under true raw URLs — PASS.** `run-c2-controls-v2.py` differs from the v1 runner only in
   the counter path and the fixture rows' URLs (example.org → the true raw URLs at `efb5099…`, plus the
   held row). Fresh rerun: `control=P-real observed=admitted=1/1 verdict=TARGET_MET … e:1` and
   `P-patched` likewise; `CTL_C2: controls=74 correct=74/74`, rc 0 — matching `receipts/ctl-c2-v2.txt`
   line-for-line. End-to-end: the v2 counter at the data commit prints `admitted=1/1 verdict=TARGET_MET`
   rc 0 (matches `receipts/c2-after-data.txt` line-for-line), at base `admitted=0/1` rc 1 (matches
   `c2-v2-before-base.txt`); the v1 counter at the data commit also 1/1 ("v1 also 1/1" confirmed).
   [LOW-2: e+ as coded checks NEW ids only (v2 counter line 525) while docstring line 11 reads as all
   ids; held ids are backstopped by clause c's byte-equal rows and the landed S155/S158 rows carry true
   raw URLs — gap adjacent to the declared claim-binding residual.]

w1 grounding verified: `w1/CritClaimSizing.md` finding 2 and `w1/CritC2Cheat.md` (16 admitted, 8 closed
by seven tightenings, residual A1/A2/D1/E2/H1/X1) say what registration-v2.md:5-8 cites;
`w1/RevC2Counter/findings.md` F1 and `w1/ExecC2ExtraMutants.md` F1/F3 exist as cited.

Safety: no tracked file edited; no mutating git; no pacman; no host-service or compositor mutation; no
subagents. Scratch `/fast/scratch/hyaku/mado-r43/RevRegistrationV2/` removed at close. Tools: python3
3.14.8, git 2.56.0 (preinstalled) — nothing installed.
