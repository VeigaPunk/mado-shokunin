## 2026-10-20 — round 18: producer identity, mutant bite, producer status; P3/P5 sourced routes; frozen tripwire replay

Trigger: admitted round-17 closure (`corpus/lessons/round-17-verifier-spotcheck.md`,
routed R17-V1..V5) at baseline `d9a5a18`; claims pre-registered at `d3a0000`
(SCORECARD tail, "Round 18 — declared claims"). Wave-1 integration `4c103b5`;
receipts `abfbf35`. Host pause carried into both wave contexts. The round-18
receipt headers name only selftest, regression, frozen, scan, measure, census
and navigation-count invocations, plus a file read of `/var/log/pacman.log`
(`evidence/tripwire-pacmanlog-join.txt`). R15-V1 remains operator-owned, state
`[UNK]`.

C1 calibration: QUALITY 24 (producer identity on receipts; R17-V1/V2), 25
(mutant bite; R17-V5) and 26 (producer status through pipes; JjAuditMado F10),
lesson rows M1-M6 in `corpus/lessons/round-18.md`. Literal 15/23 = 6.5217 →
18/26 = 6.9231 (`evidence/measure-before.json.txt`,
`evidence/measure-after.json.txt`; `measure.py` sha `de4c422b…`). Mutant
receipts (`evidence/measure-mutants.json`): six rubric-V tightenings, each a
committed-in-clone mutant that the loose instrument (`f52f43f`, sha `a280b3ab…`)
credits and the tight instrument (`d9a5a18`, sha `de4c422b…`) rejects; 6/6 bite,
`no_bite []`.

Gate fix (F10/F14, M3/M4): `tools/mado-verify.sh` captures the producer status
of `git show` inside the substitution (`pipefail`); a failed read is UNKNOWN
`rc=N`, not an empty-input digest. Selftest stubs gained per-verb rc knobs;
OM9/OM10 added (+17 assertions). Red before: `evidence/gate-rc-redbefore.txt`.
Selftest 389/389 at the committed gate (`c9fb0cef…`, `evidence/gate-selftest.txt`).
PIN_MADO re-cut `cd1d73d7…` → `20714096…`, regression 10/10 KILLED, control
green (`evidence/regression-recut.txt`).
Provenance caveat: the regression receipt prints the gate as `2bdf5e8a…`, the
working-tree bytes at its run; the committed gate at `4c103b5` and `abfbf35` is
`c9fb0cef…`. The derived target hash is identical in both, but no receipt
explains the byte change between the run and the commit. Regression was not
re-run against `c9fb0cef…`; this is disclosed, not closed.

C2 coverage, rubric V (same instrument): 4/6 = 6.6667 → 6/6 = 10.0000.
P3 Walker `corpus/knowledge/walker-route-r18.md` (sources S072-S091); P5
themes `corpus/knowledge/theme-route-r18.md` (sources S092-S095). New SOURCES
rows S072-S095 (`corpus/SOURCES.md`, 24 rows). 21 rows are URL rows; each has
at least one exact-URL receipt with HTTP 200 in the committed
`.ufo/waves/round-18/fetch/*/receipts.jsonl` (21 files, 301 lines, schema
`mado-fetch-receipt-v1`, read at `abfbf35`). S090, S091 and S095 are host
file-byte rows with no fetch receipt; rubric V credits them as documentary
host evidence. Five committed 404 receipts are retained; none is the URL of a
credited row. Documentary routes, not observed behaviour; host binaries `[UNK]`.

C3 operability capability: `tools/mado-tripwire.py --frozen
.ufo/waves/round-18/frozen` → `frozen_match`, exit 0
(`evidence/tripwire-frozen-match.txt`); copy with one byte appended to an
input → `snapshot_tampered`, exit 2 (`evidence/tripwire-frozen-tampered.txt`);
the `d9a5a18` tool → usage, exit 2 (`evidence/tripwire-frozen-before.txt`);
frozen selftest 17/17 (`evidence/harm-tripwire-round-18-frozen.txt`); registry
row `mado-tripwire-frozen` (gate) in `SKILL.md`. Tool sha `c87a31ef…`.

Routed fixes (not claims): `.gitignore` gains `.ufo/state/` and `__pycache__/`.
Tripwire receipts r13-r16 and the r15 anchor re-cut with a producer first line
(`evidence/recut-summary.json`: all counts identical, all receipts identical;
`evidence/tripwire-pacmanlog-join.txt`: 4 of 5 mado-window package transactions
joined to a tripwire `host_mutation` line by call start; pacman.log:2416
`man-pages` unmatched).

Harm watch PASS at `4c103b5` (`evidence/harm-watch-summary.txt`, 10 commands):
gate selftest 389/389; action-plan selftest 52/52; tripwire suites core 9/9,
compound 16/16, hardening 33/33, w2-regressions 30/30, frozen 17/17; U routes
7/7 (`evidence/harm-measure-u.txt`); navigation indexed 34/34, missing 0,
dangling 0, duplicates 0 (`evidence/harm-nav-fleet-round-1.txt`); census exit 0
with the three historical W04 rows S030, S042, S045
(`evidence/harm-census-validate.txt`). Freshness not re-measured; no round-18
receipt re-anchors the pins moved by the 2026-10-20 `-Syu`. No axis harmed by
lane action; operability carries R15-V1 (operator-owned, `[UNK]`).

Waves: w1 88 seats (`.ufo/waves/round-18/w1/dispatch.json`, spawn 88; 88 reports
plus `w1/reports/swarm-registry.json`). W2 falsify: 73 spawn items
(`.ufo/waves/round-18/w2/dispatch.json`). [PENDING: L1 wave-2 integration
outcome, counts and any corrections; not in the evidence at drafting.]

Not applied this round (drafts for round 19): `drafts/TwMissBashCVar.patch`,
`drafts/TwMissHelperFn.patch`, `drafts/TwInstallerChannels.patch`.

### Capabilities (round 18)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| tripwire frozen replay | Verify digest-pinned committed transcript inputs, then compare a committed expected verdict; tampered snapshots fail closed (exit 2) | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen`; `evidence/tripwire-frozen-*.txt`; `evidence/harm-tripwire-round-18-frozen.txt` | 18 |

### Planned (round 19; intent only)

1. Apply the three drafts (`TwMissBashCVar`, `TwMissHelperFn`,
   `TwInstallerChannels`) with their own receipts.
2. Re-run the regression against the committed gate bytes `c9fb0cef…` and bind
   the receipt to it.
3. Freshness re-anchor of present-tense pins moved by the `-Syu`, by file bytes
   and pacman.log only.

Verdicts are documentary and lane-authored. Nothing here is host-health
clearance, independent admission or promotion; SCORECARD and the round-18
lesson record the bounded axis readings.
