# Findings — seat RevC1Counter — review of frozen `quality/counters/c1-r44-geometry-states.py` (2026-10-26)

Target: the C1-r44 counter, line-by-line against its own docstring and the imported
`quality/counters/c1-r42-geometry.py` (PRED-C1-r42). The counter was NOT edited; every run below
is read-only over the lane with scratch under `/fast/scratch/hyaku/mado-r44/RevC1Counter/`
(receipts copied into this seat dir: `measure.out`, `measure2.out`, `probeA.out`, `probeB.out`).
No tools were installed (no pacman, no uv, no npx — none needed).

Evidence produced by: (1) a model-level harness that loads the frozen counter module with
importlib and exercises its pure functions (`measure.out`, `measure2.out`); (2) two probe runs of
the frozen counter itself (`probeA/B.out`); (3) static AST analysis (`state_sites`) of the
reference control; (4) the frozen controls receipt `.ufo/waves/round-44/receipts/ctl-c1.txt`.

---

## Findings (defects), by severity

### LOW-1 — Non-Setup I/O failures crash with a traceback and exit 1 instead of "setup failure exit 2"
- Attacks: docstring line 48 promises `setup failure exit 2`; only `Setup` exceptions
  (sandbox, revision resolution) get that path (`main` → `except Setup`, lines 378-381).
  Two reachable crash paths exit 1 with a Python traceback and **no final line**:
  1. `--work` naming a nonexistent directory: `tempfile.mkdtemp(..., dir=parent)` at
     `c1-r44-geometry-states.py:343` raises `FileNotFoundError` (probe A: rc=1, traceback ends
     `FileNotFoundError ... mado-c1r44-2g4ymwio`).
  2. `--tool` pointing at a missing/unreadable path: `open(args.tool, "rb")` at
     `c1-r44-geometry-states.py:336` raises `FileNotFoundError` (probe B: rc=1).
- Impact: an automated scorer that maps exit codes (0 met / 1 missed / 2 setup, per docstring
  line 47-48) reads a broken invocation as TARGET_MISSED, and any consumer grepping the final
  line finds nothing. The registration's counting command always pre-creates the work dir, so
  the claim's verdict path is unaffected — hence Low, not Medium.
- Repro: `python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev e2289516… \
  --tool quality/counters/c1-r42-geometry.py --work <missing-dir>` (receipt `probeA.out`).

### LOW-2 — Docstring's "Final line" format does not match the code's output
- Attacks: docstring line 46 specifies the final line as containing `clauses=<...>`
  ("`PRED-C1-r44: fixtures=k/26 clauses=<...> tool=…`"). The code prints clauses on a separate
  preceding line (`:373`) and the actual final line has no `clauses` token (`:374-376`).
- Impact: anyone parsing the frozen counter's documented output format (it is the predicate's
  normative text in `registration.md`) fails to find the documented token. No scoring logic
  depends on it — the internal clause-r check matches `" verdict=TARGET_MET "` which the real
  final line carries (`:318`) — so Low/documentation, but it is a real doc-vs-code disagreement
  inside a frozen instrument.
- Note: PRED-C1-r42's docstring (r42 `:97-99`) does NOT claim clauses in its final line; the r44
  docstring added the token without changing the inherited print layout.

### LOW-3 — `regress` subprocess timeout is unguarded and ungated
- Attacks: `regress`, `c1-r44-geometry-states.py:313-315`: `subprocess.run(..., timeout=1800)`
  with no `try/except`. A hung round-42 subprocess (bwrap stall, FIFO-edge) raises
  `subprocess.TimeoutExpired` after up to 30 min, aborting the whole counter with a traceback —
  no final line, verdict lost (the `finally` at `:370-371` still cleans the scratch).
- Secondary: the r44 phase's 3-timeout circuit breaker (`TIMEOUTS`, r42 `:160-171`) does not
  gate regress — the subprocess is a fresh process with its own budget, so a tool that already
  tripped 3 timeouts still gets a full 37-fixture r42 run (up to 30 more minutes) for a clause
  that cannot rescue the verdict. Operational cost, not correctness; the same unguarded pattern
  exists in r42's own design, so this is inherited, but r44 added the outer timeout.

---

## Coverage and asymmetry findings (quantified, no false pass found)

### INFO-1 — sgen lattice: per-fixture state-blindness is the norm; the run is never state-blind
- Measured over 50 nonces at the freeze rev `e2289516a9a8…` (`measure.out`): each sgen0..11
  fixture contains a matched client with `fullscreen` ∈ {1,2} and a valid size (i.e. produces a
  FULLSCREEN/MAXIMIZED verdict and the summary states) on only 11-21 of 50 nonces
  (sgen10 worst: 11/50). Per nonce, the 12 fixtures together always reach the state verdicts:
  0/50 nonces fully blind, min 2 state clients in one nonce (nonce `7b72a9f4f1390e03`), max 16.
- Validation of the simulation: predicted pass-count distribution for a pure round-43 tool is
  {11:1, 12:5, 13:10, 14:13, 15:11, 16:9, 17:1}/50; the two observed base scores — 12/26
  (`receipts/c1-before-base.txt` per registration) and 13/26 (`ctl-c1.txt`, BASE-tool line) —
  both fall inside it, and the 6 fixed r43-passing slots + per-nonce sgen blindness explain the
  variance the registration itself records ("the lattice count varies with the nonce").
- Why no false pass: 8 FIXED slots are state-carrying at every nonce (fs0, fsagree0, max0,
  maxfloat0, fsmix0, fsstdin0, fsdup0 slot, fsmany0 — the last with 62 state-verdict and 86
  edge-value matched clients in one sampled nonce, `measure.out`), and the edge probes fsbad0 /
  fsvals0 / fsclient0 deterministically kill type/order mistakes. The docstring's clause f does
  not promise per-fixture lattice reach, so this is a margin note, not a defect: the state
  extension cannot escape a run untested.

### INFO-2 — clause b4 asymmetry quantified on the reference (declared residual, now measured)
- `state_sites` on `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` finds 14 comparison sites —
  `client_fsmode`: 1 (line 197), `evaluate`: 8 (213, 221, 225, 229, 231, 233, 235, 239),
  `report`: 5 (259, 260, 262, 264, 269) — so `need = ceil(0.75·14) = 11` mutants must be killed
  (`measure.out` tail; logic at `c1-r44-geometry-states.py:265-307`, `MIN_STATE_SITES=6:76`,
  `KILL_FRACTION=0.75:77`).
- Can a correct tool fail b4? Yes, two ways, both structural: (a) a tool whose mode/verdict
  logic sits in functions whose bodies hold no `fullscreen` string constant gets 0 sites and
  fails `state_sites < 6`; (b) a correct but comparison-lean implementation (<6 single-op
  Compare nodes in named functions, e.g. tuple/dict-dispatched verdicts) fails the same gate.
  The docstring declares the sibling hole at `:50-52` ("b4 counts / sites only in functions that
  name `fullscreen`", "unnamed helper and keep the clause / vacuous-but-satisfied only if it
  still has >= 6 sites there"): a tool can point b4's teeth at r43-era comparisons while its
  state logic hides in an unnamed helper — clause f fixtures, not b4, are what catch wrong state
  logic in that case. The ref passes with margin 14→11, so a false negative needs a materially
  different structure, not a refactor of the ref.
- Can a wrong tool pass b4? Only by carrying ≥6 selftest-observed comparisons in fullscreen-
  naming functions — b4 measures selftest teeth, not state correctness; wrong state logic is
  clause f's job. Receipt `ctl-c1.txt`: K13 (selftest stripped of new cases) scores fixtures
  26/26 yet misses on `b:0 b4:0` — b4 is exactly the load-bearing anti-stripped-selftest clause,
  and all 13 single-defect state variants are caught by fixtures alone.

---

## Verified-OK (hunt items that came back clean, with evidence)

### OK-1 — Model vs docstring: 0 mismatches / 2000 adversarial cases
An independent model re-derived from the r42+r44 docstrings (rules grammar, client parsing,
fsmode type-strictness, verdict order BADSIZE|FULLSCREEN|MAXIMIZED|TILED|AGREE|DIFFER, states
between `badsize=` and `verdict=` exactly when the sum > 0) was diffed byte-exactly (stdout+rc)
against `model_out_states` on 2000 random cases with rules from an edge-regex pool and clients
carrying `fullscreen` ∈ {1, 2, 0, 3, -1, true, false, 2.0, "2", null, [2], {"internal": 2},
10^20, absent} plus `fullscreenClient`, bad sizes, mapped variants: **0 mismatches**; verdict
spread BADSIZE 510 / TILED 1368 / DIFFER 935 / FULLSCREEN 374 / MAXIMIZED 370 / AGREE 12
(`measure.out`). Spot reads agree: `type(f) is int and f in (1, 2)` at `:90` excludes bool/float
(JSON `true`/`2.0`); `:139-145` places the states string exactly as documented; matched/mode
bookkeeping keeps FULLSCREEN/MAXIMIZED out of `DIFFER` so top verdicts and rc are unchanged
(`:147-155`).

### OK-2 — importlib monkeypatch does NOT leak into the regress subprocess
`old.model_out = model_out_states` (`:173`) mutates only this process's module dict. Clause r
re-executes `OLD_PATH` in a fresh `python3 -I` subprocess (`:313-315`), which imports a pristine
module — proven by a second importlib load in `measure2.out`: pristine `model_out is not`
patched object, and the pristine module's `case_files` resolves `model_out` from its own
`__dict__` (r42 `:475` is a module-global lookup at call time). The subprocess therefore judges
the same bytes (the file written from `src`, `:349-352`) against the ORIGINAL round-43 model —
exactly what the docstring's clause r (lines 42-44) claims. `-I` mode plus the explicit env
(only `C1R42_TMP` added, `:311-312`) leaves no injection path.

### OK-3 — Regress clause runs on the same bytes with a derived, replayable nonce
`sub = sha256("regress:" + nonce)` (`:310`); `--tool tool` is the exact byte blob the fixtures
judged; success requires rc 0 and `" verdict=TARGET_MET "` in the last line (`:316-318`).
The r42 counter's base precondition uses its own frozen `BASE_DEFAULT` (r42 `:107`), and control
ABSENT-62dd798 (`ctl-c1.txt`) confirms the tool is absent there, so the precondition holds in
the lane — no hidden dependence on the round-44 base.

### OK-4 — Fixed fixtures: none vacuous; each has a distinct kill role
Model-level audit against a pristine r43 load (`measure2.out`): exactly 6 FIXED slots are
r43-passing by design and each still kills a named wrong tool — fsbad0 (BADSIZE before
FULLSCREEN → K05), fsvals0 (all ten non-mode values on matched DIFFER clients → K03/K06/K07),
fsclient0 (`fullscreenClient` ignored → K08), fsdup0-1 (duplicate-key last-wins), fsunmatched0 /
fsunmapped0 (states only for matched clients), fsnorules0 (NO_SIZE_RULES with a fullscreen
client); the other 8 slots carry the state verdicts themselves (→ K01/K02/K04/K09/K10/K11/K12
per the receipt's fixture counts). `ctl-c1.txt`: all 15 non-reference runs MISSED, 0 TARGET_MET.

### OK-5 — Scratch handling matches the docstring
`--work DIR` → `$C1R44_TMP` → tempfile default (`:342-343`, no hardcoded /tmp, docstring line
48); one mkdtemp root chmod 0755; b4 mutant copies at `<tmp>/<opaque>/tool/mado-geometry.py`
(real layout, r42 `:892-894`); regress scratch nested inside (`:368-369` + r42 `:971` reading
`C1R42_TMP`); single `finally: shutil.rmtree(tmp, ignore_errors=True)` (`:370-371`) covers
mutants, fixtures and regress. Residual: SIGKILL leaks the dir (reaper's job); the crash paths
of LOW-1 still reach the finally.

### OK-6 — Clause-by-clause docstring conformance
a (`:337,339`, git-read bytes, ambient GIT_* stripped r42 `:100`), f (12 sgen + 14 FIXED =
assert 26 `:362`; byte-exact judge r42 `:449-463` with stderr-empty on rc 0/1/3/4 `:461`), b
(`MIN_SELFTEST=80:75`, sandboxed 60 s r42 `:883-886`), b4 (sites ≥6, flip all, kill ≥ ceil 75%
`:289-307`; NOT_SITES/FLIP reused r42 `:837-840`; chained `a<b<c` and multi-op compares are
consistently invisible to both counter and mutator r42 `:869-881`), g (`old.imports_ok`, same
check as r42), r (OK-2/OK-3). Exit codes 0/1/2 and the printed nonce (`:374-376`, `:330`) match
the docstring's replay contract. Fixture runs proceed even when b fails (diagnostics preserved).

---

## Residual risk / verification gaps
- Kill rates inside b4 were not re-measured by running mutants here (bwrap runs); the frozen
  receipt's `b4:1` for REF and `b4:0` for K13 bound the behavior from the recorded run.
- LOW-1/LOW-3 are crash-path findings: they cannot flip a TARGET_MET verdict for a correct tool,
  but they can mask one (a seat that typos `--work` reports exit 1). Worth routing to the L1 as
  counter-defect candidates for a v2 re-freeze, per the registration's pre-data hole rule.
- The 50-nonce lattice study used nonces derived in this seat, not the run's secret nonce; the
  distribution match against the two recorded base scores (12, 13) is the cross-check.
