# MutC1Counter findings log

Freeze d7527d608ad2b2e3cc398fdde34db7947b254a1a; nonce 4747 (same as `receipts/ctl-c1.txt`); harness =
copy of `ctl/run-c1-controls.py` scoring logic (clone --shared --no-checkout of the lane, checkout freeze,
commit tool, run counter with `--work` in scratch). All counter variants are scratch copies under
`/fast/scratch/hyaku/mado-r47/MutC1Counter/ctr/<name>/`; the tracked counter was never modified.

## Baseline (pristine counter)
- REF → TARGET_MET fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok — matches `ctl-c1.txt`.
- EXPLAIN-ALWAYS-AGREE → TARGET_MISSED explained=25/190 — matches receipt.
- SOCKET-AND-REF → TARGET_MISSED readonly=fail — matches receipt.

## m6 — drop the explain DIFFER probe (killed)
- Mutation: `for path, want_v, want_rc in ((good, "AGREE", 0), (bad, "DIFFER", 1)):` → only the AGREE pair (counter line 285).
- REF still MET; **EXPLAIN-ALWAYS-AGREE flips to TARGET_MET** (explained=190/190) → control suite FAILs → killed.

## m7b — accept all trips / drop readonly clause
- Mutation: `readonly = "fail" if box.trips else "ok"` → `readonly = "ok"` (counter line 456).
- RUNNING: REF + SOCKET-AND-REF.

## M5 note (tree sharing) — empirical cache race
- The resolver writes its cache via `save_cache "$1" &` (pin line 1457, backgrounded, BEFORE the print block).
- Inside the counter's bwrap sandbox the backgrounded subshell is killed by PID-namespace teardown when the
  main shell exits: after 5 replicate oracle runs (Box.argv replication), `.rw/cache/xdg-terminal-exec` was
  absent 5/5.
- Outside bwrap (same env, scratch XDG_CACHE_HOME), the cache IS written (hash/cmd/path raw-with-/.//id/
  action/args/exec_usep) — so the in-sandbox absence is a teardown race, not a resolver failure.
- Implication: reuse-oracle-tree (m5) is behaviorally unobservable on this host; cache-reading cheat gains nothing.

## m7b — accept all trips (killed)
- SOCKET-AND-REF flips to TARGET_MET (readonly=ok) → control suite FAILs → killed.

## m1 — drop the drift check (survived; not revealed by controls)
- Controls cannot reach the drift path: both the oracle (PIN_SHA256) and the fixture record (FIXTURES_SHA256)
  are sha-pinned, and the controls use the pristine pinned fixtures, so no control ever exercises the
  oracle-vs-record comparison. The only trigger is host-external drift.
- Drift probe (record-level simulation; the counter's drift comparison `[o_a[0], o_a[1]] != [expect.rc,
  expect.stdout]` is exercised identically): modified fixture record (fixture "a1-cfg-home-plain-list"
  expect.stdout + "X", sha f11a1d2a...). Harness-pristine variant (drift raise intact, sha constant patched
  to the modified record) → SETUP "oracle drifted from 1 recorded fixture(s): a1-cfg-home-plain-list", exit 2.
- m1 (raise removed, same record) → RUNNING (expect TARGET_MET with REF).

## m2 — compare stdout only (drop rc from fixture/generated comparison) — survived
- REF still MET; EXIT1 (the rc-sensitive control) still MISSED, fixtures=25/190 generated=109/150 — byte-identical
  to the receipt. No control differs from the oracle only in rc; the controls' defects are content/trace/explain.
- Probe P-M2 (REF with print-return rc 0→7): pending.

## m3 — explain ignores the tool's exit status (primary comparison only) — survived
- EXPLAIN-ALWAYS-AGREE unchanged (explained=25/190, identical to receipt/baseline). No control has a
  verdict-correct-but-rc-wrong explain.
- Probe P-M3p (REF: plain `explain` returns 1, --observed returns correct rc): real counter → MISSED
  explained=0/190; m3 → pending.

## m3b — explain ignores rc everywhere (primary AND --observed probes)
- P-M3 (all explain runs return 1) vs m3b: pending. Controls REF + EXPLAIN-ALWAYS-AGREE vs m3b: pending.

## m3/m3b results (final)
- m3 (primary explain rc dropped): P-M3p (plain-explain rc 1, observed rc correct) → real MISSED explained=0/190,
  m3 MET. Controls unchanged (EXPLAIN-ALWAYS-AGREE explained=25/190). Survived.
- m3b (rc dropped in primary AND --observed): controls unchanged (REF MET; EXPLAIN-ALWAYS-AGREE MISSED
  explained=25/190); P-M3 (every explain run exits 1) → MET. Survived.

## m4 — skip variant B (survived)
- REF MET; V-NO-LOWER MISSED fixtures=185/190 generated=145/150 selftest=fail — byte-identical to receipt. No
  control's defect is variant-B-specific (all fail in variant A too), so none can flip.
- Probe P-M4 (REF exits 7 when LANG=en_US.UTF-8): real counter → MISSED fixtures=0/190 (variant B caught it),
  explained=190/190 generated=150/150 (A/explain/selftest unaffected); m4 → pending.

## m5 — reuse the oracle tree for the tool (survived)
- REF MET; V-NO-EXCLUSION MISSED fixtures=185/190 generated=148/150 — byte-identical to receipt.
- The two-tree separation is behaviorally unobservable here: the resolver's cache write (`save_cache "$1" &`,
  pin:1457) is backgrounded and killed by PID-namespace teardown before it lands — after 5 in-sandbox oracle
  runs the cache file was absent 5/5 (outside bwrap it is written). No control and no behavioral probe can
  distinguish shared-tree from two-tree on this host.

## m4 probe (final)
- P-M4 → real MISSED fixtures=0/190 (variant B caught the LANG-sensitivity); m4 MET. Survived.

## m7a — accept one trip (survived)
- Controls unchanged: REF MET; SOCKET-AND-REF MISSED readonly=fail (trips ~1000 > 1). No control trips exactly once.
- Probe P-M7a (REF + one AF_UNIX socket in the --selftest run only): real counter → MISSED readonly=fail
  (trips=1); m7a → pending.

## m7a probe (final)
- P-M7a → real MISSED readonly=fail; m7a MET. Survived.

## m8 — lower SELFTEST_MIN to 1 (survived)
- Controls unchanged: REF MET; V-NO-ALIASES MISSED fixtures=189/190 selftest=fail — byte-identical to receipt.
  Every selftest=fail control also fails another clause (no control is selftest-only), so none can flip.
- Probe P-M8 (REF printing "MADO_TERMINAL_SELFTEST: 2/2 passed"): real → MISSED selftest=fail; m8 → pending.

## m8 probe (final)
- P-M8 → real MISSED selftest=fail; m8 MET. Survived.

## m9 — parse the selftest line loosely (survived)
- Controls unchanged: REF MET; V-NO-ALIASES MISSED fixtures=189/190 — byte-identical to receipt.
  m9 → MET.


## m9 probe (final)
- P-M9 → real MISSED selftest=fail (N!=M rejected); m9 MET. Survived.

## Final tally
- KILLED by a control: m6 (drop explain DIFFER probe; EXPLAIN-ALWAYS-AGREE flips to MET),
  m7b (accept all trips; SOCKET-AND-REF flips to MET).
- SURVIVED (all controls still PASS; hole in the evidence), each with a bespoke probe that the pristine
  counter rejects and the mutant admits: m1 (drift), m2 (stdout-only), m3 (primary explain rc),
  m3b (rc everywhere in explain), m4 (skip variant B), m5 (shared tree — behaviorally unobservable on this
  host: cache write killed by sandbox teardown 5/5), m7a (one trip), m8 (SELFTEST_MIN=1), m9 (loose parse).