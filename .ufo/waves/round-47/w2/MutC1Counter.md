# MutC1Counter — w2 FALSIFY report (C1 counter mutation testing)

Seat: MutC1Counter (leaf). Target: `quality/counters/c1-r47-terminal.py` (tracked file untouched; every
mutant was a scratch copy under `/fast/scratch/hyaku/mado-r47/MutC1Counter/ctr/<name>/`, laid out as a lane
mimic so the counter's HERE-relative fixtures/pin paths resolve). Harness: the frozen controls logic
(`.ufo/waves/round-47/ctl/run-c1-controls.py` scoring, clone `--shared --no-checkout` of the lane, checkout
freeze `d7527d608ad2b2e3cc398fdde34db7947b254a1a`, commit the tool, run the counter with `--work` in scratch),
nonce 4747. Baseline reproduced the receipt `receipts/ctl-c1.txt` byte-for-byte (REF MET; EXPLAIN-ALWAYS-
AGREE explained=25/190; SOCKET-AND-REF readonly=fail).

## Verdicts

| mutant | mutation point (counter line) | verdict | revealing run |
|---|---|---|---|
| m6 | drop explain DIFFER probe (line 285) | **KILLED** | EXPLAIN-ALWAYS-AGREE flips to TARGET_MET (explained 25/190→190/190) |
| m7b | `readonly = "ok"` (line 456) | **KILLED** | SOCKET-AND-REF flips to TARGET_MET (readonly=ok) |
| m1 | drop the oracle-drift raise (lines 444-445) | survived | controls cannot reach the drift path (oracle and record both sha-pinned); drift probe below |
| m2 | `ok = o_norm[1] == t_norm[1]` (line 248) | survived | EXIT1 unchanged (25/190, 109/150); probe P-M2 → MET |
| m3 | explain primary `got` drops rc (lines 271-274) | survived | EXPLAIN-ALWAYS-AGREE unchanged; probe P-M3p → MET |
| m3b | rc dropped in primary AND --observed (lines 271-274, 289) | survived | controls unchanged; probe P-M3 → MET |
| m4 | variant B skipped (lines 430, 433) | survived | V-NO-LOWER unchanged (185/190); probe P-M4 → MET |
| m5 | oracle tree reused for the tool (lines 238-239) | survived | V-NO-EXCLUSION unchanged; behaviorally unobservable on this host (below) |
| m7a | `len(box.trips) > 1` instead of any trip (line 456) | survived | SOCKET-AND-REF unchanged (trips ~1000); probe P-M7a → MET |
| m8 | `SELFTEST_MIN = 1` (line 73) | survived | V-NO-ALIASES unchanged (189/190); probe P-M8 → MET |
| m9 | loose selftest parse (lines 397-402) | survived | V-NO-ALIASES unchanged; probe P-M9 → MET |

Every survived mutant is a hole in the evidence: all 30 frozen controls still pass with the weakened counter, and
for every one except m5 a bespoke probe tool exists that the pristine counter rejects (TARGET_MISSED) and the
mutant admits (TARGET_MET), proving the weakening is load-bearing. Reconstructible probe tools: `tools/P-*.py`
in the seat dir below (REF-derived; each is a single-line/block patch of the L1 reference).

## Killed mutants (controls do their job)

- **m6** (drop the DIFFER probe): `EXPLAIN-ALWAYS-AGREE` becomes TARGET_MET — its only defect (always
  AGREE) was the dropped probe. Controls FAIL → killed.
- **m7b** (accept all trips): `SOCKET-AND-REF` becomes TARGET_MET (readonly=ok). Controls FAIL → killed.
  (Strictly, the same mutation that weakens a counter also "breaks" it enough that the control flips; this is
  the standard kill.)

## Survived mutants — per-mutant evidence

- **m1** (drift check dropped). The controls cannot exercise the drift path: the oracle is pinned by
  `PIN_SHA256` and the fixture record by `FIXTURES_SHA256`, and every control uses the pristine pinned fixtures,
  so the oracle-vs-record comparison (`[o_a[0], o_a[1]] != [expect.rc, expect.stdout]`, counter:430-432) never
  fires. Drift probe (simulated drifted record; both arms carry the harness patch `FIXTURES_SHA256` → sha of the
  modified record `f11a1d2a5ebb28d8d954079474bea46e4b4dff2ccef56aa3a4f6b0f238ab87af`, fixture
  `a1-cfg-home-plain-list` expect.stdout + "X"): harness-pristine (drift raise intact) → `SETUP oracle drifted
  from 1 recorded fixture(s): a1-cfg-home-plain-list`, exit 2; m1 → TARGET_MET with REF (190/190). A drifted
  host would therefore score tools against a record that no longer describes the judge, undetected.
- **m2** (stdout-only). EXIT1 (the rc-only-adjacent control) scores byte-identically to the receipt
  (fixtures=25/190, generated=109/150): no control differs from the oracle solely in rc. Probe P-M2 (REF whose
  print branch returns 7 instead of rc, reference:1034-1036): real counter → MISSED fixtures=0/190; m2 → MET.
- **m3 / m3b** (explain rc). EXPLAIN-ALWAYS-AGREE scores byte-identically (explained=25/190); no control has a
  verdict-correct-but-rc-wrong explain. P-M3p (plain `explain` returns 1, `--observed` returns correct rc,
  reference:854-856): real → MISSED explained=0/190, m3 → MET. P-M3 (every explain run returns 1): m3b → MET;
  real counter → MISSED explained=0/190. m3b's controls unchanged.
- **m4** (skip variant B). V-NO-LOWER scores byte-identically (185/190, 145/150); no control's defect is
  variant-B-specific (all fail in variant A too). Probe P-M4 (REF exits 7 when `LANG=en_US.UTF-8`, inserted at
  reference:95): real counter → MISSED fixtures=0/190 (variant B catches it; A/explain/selftest unaffected),
  m4 → MET. Variant B is the only clause that catches locale/root-shape sensitivity.
- **m5** (shared tree). V-NO-EXCLUSION byte-identical (185/190, 148/150). Additionally, the two-tree
  materialization is behaviorally unobservable on this host: the resolver's cache write is backgrounded –
  `save_cache "$1" &` (pin:1457) – and the forked subshell is killed by PID-namespace teardown when the main
  shell exits; after 5 replicate in-sandbox oracle runs the cache file `.rw/cache/xdg-terminal-exec` was absent
  5/5 (outside bwrap, same env, the cache IS written: hash/cmd/path-with-/.//id/action/args/exec_usep). So no
  control and no behavioral probe can distinguish shared-tree from two-tree here; a cache-reading cheat tool
  gains nothing.
- **m7a** (one trip). SOCKET-AND-REF unchanged (readonly=fail; trips ~1000 ≫ 1). Probe P-M7a (REF creates one
  AF_UNIX socket in the `--selftest` run only, reference:1019-1020 → exactly one trip per count): real counter →
  MISSED readonly=fail; m7a → MET. A tool that connects once (e.g. a one-shot phone-home) passes m7a.
- **m8** (`SELFTEST_MIN=1`). V-NO-ALIASES unchanged (189/190, selftest=fail); every selftest=fail control also
  fails another clause, so none can flip. Probe P-M8 (REF printing `MADO_TERMINAL_SELFTEST: 2/2 passed`,
  reference:1014): real → MISSED selftest=fail; m8 → MET. A tool claiming 1-29 passing cases sails through.
- **m9** (loose parse; exact 3 tokens, N==M and the `/M` half dropped). V-NO-ALIASES unchanged. Probe P-M9
  (REF printing `MADO_TERMINAL_SELFTEST: 35/43 passed`): real → MISSED selftest=fail (N≠M rejected); m9 → MET.
  A tool whose selftest line hides 8 failures passes the loose parse.

## Evidence

- Raw runs (counter stdout per control/probe): `logs/*.log` in this seat dir (one per run; e.g.
  `REF.log`, `EXPLAIN-ALWAYS-AGREE.log`, `P-M2.log`, `P-M3.log`, `P-M3p.log`, `P-M4.log`, `P-M7a.log`,
  `P-M8.log`, `P-M9.log`, `m1`/`m1base` REF logs).
- Full narrative: `NOTES.md` in this seat dir.
- Probe tool sources: `tools/P-*.py` (scratch copies; regenerated by `build.py`).
- Counter mutant sources: scratch mimics; the tracked `quality/counters/c1-r47-terminal.py` was never modified.
- No tools were installed; nothing was fetched. Host guards honored (no pacman; resolver runs only with
  `--print-*` and `XDG_CACHE_HOME` in scratch; one read-only `git` clone of the lane per score run).

## Recommendations

The frozen controls kill the two "all-or-nothing" mutants (m6, m7b) but leave nine weakenings undetected. The
highest-value additions would be: a control whose tool differs from the oracle only by exit status (kills m2,
m3, m3b), a selftest-only failing control (kills m8, m9), a control whose defect only shows under variant B
(kills m4), a drift-armed counter self-check (kills m1), and a cache-reading tool (kills m5 — currently
unobservable on this host anyway). Each is a one-tool addition to `ctl/run-c1-controls.py`.
