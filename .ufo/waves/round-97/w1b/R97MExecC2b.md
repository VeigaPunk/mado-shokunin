# R97MExecC2b — C2 self-invocation for the two round-96 counters (wave w1b)

Base revision `e6152b589c2c6a28426c28263c4bcc3c46398be4`. Scratch
`/fast/scratch/hyaku/mado-r97/R97MExecC2b` (deleted before this report was finalised; transcripts
quoted inline). No tools installed or upgraded (python3 + git only; pacman transactions stayed
paused per the host guard). All probes read-only on the lane; every fixture repo was built and
committed inside scratch.

## Files changed

- `.ufo/waves/round-97/build/c1-r96-magictext-selftest.v2.py` (new; base
  `quality/counters/c1-r96-magictext.py` at `e6152b58` + added block)
- `.ufo/waves/round-97/build/c2-r96-selftest-kills-selftest.v2.py` (new; base
  `quality/counters/c2-r96-selftest-kills.py` at `e6152b58` + added block)
- `.ufo/waves/round-97/selftest-fixtures-v2/` (new; 25 committed fixture files, inventory below)
- `.ufo/waves/round-97/w1b/R97MExecC2b.md` (this report)

Final sha256:

```
4f6783848ded9c63f934c68a24da856369895987651d0f66fdd6920f07aaa64d  build/c1-r96-magictext-selftest.v2.py
54143b8a28f2be4b2f1361c443d32156a68fd088c7cdb9c9030ca7415002217b  build/c2-r96-selftest-kills-selftest.v2.py
```

## Behavior

Each counter gains one appended block (marker line
`# ===== mado counter self-invocation (added round-97 C2, seat R97MExecC2b)`); the block replaces the
base two-line `__main__` guard with an identical dispatch plus a `--selftest` branch and defines
`_mado_counter_selftest(argv)`.

- **CLI**: `python3 -I <counter> --selftest [--fixtures DIR]` (`--fixture-dir` accepted as an alias,
  same destination). Production argv path is unchanged: without `--selftest` the script calls
  `main()` exactly as before (verified: bare invocation prints the base argparse "arguments are
  required" error, rc 2, byte-identical message to the base counters).
- **Fixture resolution** (never cwd, no absolute lane constant, no env override — R97MReviewC2b's
  w1 defect is structurally absent): explicit `--fixtures/--fixture-dir` is terminal (an absent or
  unparseable tree there fails the checks, never falls back); otherwise the counter walks its own
  ancestors looking for `.ufo/waves/round-97/selftest-fixtures-v2` (legacy `selftest-fixtures`
  accepted), so it resolves from the build/ copy, a landed `quality/counters/*.py`, or any promoted
  layout root. The resolved dir is printed as a separate `FIXTURES: <dir>` line (or
  `FIXTURES: UNRESOLVED`); the result line stays exactly `MADO_COUNTER_SELFTEST: checks=N failed=0`.
- **Checks (10 per counter, ids stable, each with a unique once-occurring definition-line anchor so
  the panel can neutralise exactly one check)**: `st-fixture-dir`, `st-tool-pin`,
  `st-gate-target-met`, `st-setup-missing-input`, `st-setup-wrong-pin`, `st-setup-wrong-rev`,
  `st-target-missed-case`, `st-target-missed-mutant`, `st-result-line-format`, `st-scratch-clean`.
- **The checks drive the counter's own `main()`** over committed fixtures (Shared contract 4, dead
  seat R97MExecC2 prompt: "the checks point the counter at them through its own main()"): each
  scenario builds a throwaway git repo in a scratch tempdir (`git init` → toplevel asserted →
  commits via `git -c user.name=...`), assembles the counter's production argv against fixture
  files, and runs `main()` **in-process** with `sys.argv` set and stdout captured, after rebinding
  only this module's census thresholds to the fixture scale — for c1 `MIN_CASES=2, MIN_PER_CLASS=1,
  CLASSES=("mini",), MIN_FRESH_INPUTS=2, MIN_HOST_PATHS=3, HOST_DB_FILES=2,
  TEXT_DB_FILES=("globs2","magic")`; for c2 `MIN_NEUTRAL=2`. All rebinding is save/restore around
  each run; the production code lines are untouched.
  - `st-gate-target-met`: the green mini-run must print the counter's real verdict line and exit 0
    — c1 reaches `MADO_MAGICTEXT_COUNT: TARGET_MET pred=PRED-C1-r96-v1 ... tool_pin=ok ...
    cases=2 correct=2 ... selftest=ok` (oracle compiled from the fixture C source, frozen leg,
    fresh leg via the fixture generator, host leg over the fixture host-db, mutant kills, all four
    controls, forgery rejected by the audit launcher) — this is the full production pipeline at
    fixture scale. c2 reaches `MADO_SELFTEST_KILLS: TARGET_MET pred=PRED-C2-r96-v1 ... gate_pin=ok
    kills_pin=ok tool_pin=ok checks=6 ...` (the fixture gate is the real round-93 gate bytes, the
    fixture tool and kill-set are the real round-96 bytes, the fixture r90 counter is a
    TARGET_MET-stub, the fixture panel is the frozen round-96 hand[0] + neutral[0..1] entries).
  - `st-tool-pin`: every committed fixture file is sha256-checked against `pins.json` (which is why
    the mutated-tool broken mode fails exactly the pin branch).
  - `st-setup-missing-input` / `st-setup-wrong-pin` / `st-setup-wrong-rev`: a production run with a
    missing `--cases`/`--panel` path, a wrong sha pin, or a nonexistent `--rev` must print the
    counter's own `SETUP_ERROR` line and exit 2.
  - `st-target-missed-case`: a mismatched tool at rev (c1: the fixture `bugtool-mutation.json`
    applied — a third frozen r96 mutant whose anchor stays unique in the buggy bytes; c2: tool
    bytes + trailing probe comment breaking the kill-set pin) must reach `TARGET_MISSED` rc 1.
  - `st-target-missed-mutant`: a mutant file holding a behavior-identical "survivor" (c1: a
    no-op comment mutation alongside a real killer; c2: a kill whose replace only appends a
    comment) must reach `TARGET_MISSED` rc 1.
  - `st-result-line-format`: the green run's last verdict line must start with the counter's
    `... TARGET_MET pred=...` prefix and carry the declared tokens.
  - `st-scratch-clean`: after the green `main()` returns, its `--scratch-root` holds no surviving
    scratch dir (the counter's own `finally` cleanup), and the selftest's tempdirs are removed.
- Exit codes: 0 green, 1 failed (checked asserted rc/ids), per contract 4. `could-not-evaluate` (2)
  is never printed by the selftest itself; the runner treats any rc != 0 as not-green.

## Fixtures (`.ufo/waves/round-97/selftest-fixtures-v2/`, 25 files)

```
pins.json                       sha256 of every file below (read at runtime by st-tool-pin)
common/forgery-ctypes-r96.py    the round-96 forgery control (audit-rejected by construction)
common/mimesniff-oracle-r95.c   the round-95 oracle C source (sha 99df35f8b3fd7005..., what the
                                c1 mini-run compiles; also the case envelope's oracle_src_sha256)
common/canary.txt|png|pk        three host-leg canaries
c1/mado-mimetext.py             the pinned tool (real round-96 candidate bytes, d5f174fc33d0b1f1...)
c1/mado-mimeglob.py|...sniff.py the real r94/r95 siblings (name-step + do-nothing control)
c1/cases-mini.json              2-case envelope (classes ["mini"], re-id'd frozen cases
                                header-01-gate-good-holds + sect-02-priority-intmax-beats-100,
                                oracle labels verified by the round-96 probe semantics)
c1/mutants-mini.json            2 killers: sect-eof-section-dropped (kills header-01),
                                order-ascending (kills sect-02) — both from the frozen r96 mutants
c1/mutants-mini2.json           killer + behavior-identical survivor (comment mutation)
c1/bugtool-mutation.json        order-last-match (the missed-case bug; anchor unique in buggy bytes)
c1/freshgen.py                  deterministic mini fresh generator (2 cases / 3 inputs,
                                none-mode, oracle-labelled via the --oracle it is handed)
c1/hostdb/mime/{globs2,magic}   mini text DB (magic from the frozen header-01 fixture)
c1/hostdb-manifest.json         text-mode manifest, source.dir {FIXTURES}/c1/hostdb/mime
c1/hostlist.txt                 3-line host list, {FIXTURES} substituted at runtime
c2/dummy-gate.py                the real round-93 gate bytes (2d6f1219fae19a85...)
c2/dummy-tool.py                the real round-96 receipt-presence tool (be716a63662f326a...)
c2/kills-mini.json              the real frozen kill-set (305d735fd665ad87...)
c2/kills-firstdraft.json        control kill-set (kills: [] → gate OK on hand variants)
c2/panel-mini.json              frozen r96 panel entries hand[0] okrc-ge-zero + neutral
                                n-comment, n-docstring (MIN_NEUTRAL rebound to 2)
c2/r90argv.json                 {"argv": ["--rev","@REV@","--scratch-root","@SCRATCH@",
                                "--base-rev","@BASE_REV@"], "base_rev": 40 zeros}
c2/dummy-r90-counter.py         TARGET_MET stub for the r90 leg
```

## Exact retained evidence

**Byte identity (the proof the item demands).** Strip protocol: delete from the marker line to EOF
and append exactly `if __name__ == "__main__":\n    sys.exit(main())\n` — the reassembled file is
byte-identical to `git show e6152b58:quality/counters/<name>.py` (measured `strip-ok: True` for both
counters). Added/removed line counts: **c1 +308 / −2** (the guard, re-included inside the block),
**c2 +286 / −2**. Every production line above the marker is untouched; ASCII-only; `py_compile`
clean. Production-behaviour identity: bare invocation of each .v2 file prints the base counter's
exact argparse error and rc 2 (c1 requires `--repo --rev --base-rev --cases ...`; c2 `--repo --rev
--panel ...`) — identical message text to the base counters.

**Green matrix (all four cells, final bytes).** stdout tail of each run:

```
c1, build/ layout, cwd=lane root:    MADO_COUNTER_SELFTEST: checks=10 failed=0   rc=0 wall=11s
c1, promoted replica (quality/counters/ in scratch, cwd=/tmp):
                                     FIXTURES: <promo>/.ufo/waves/round-97/selftest-fixtures-v2
                                     MADO_COUNTER_SELFTEST: checks=10 failed=0   rc=0 wall=10s (11s re-run)
c2, build/ layout, cwd=lane root:    MADO_COUNTER_SELFTEST: checks=10 failed=0   rc=0 wall=33s
c2, promoted replica (cwd=/tmp):     FIXTURES: <promo>/.ufo/waves/round-97/selftest-fixtures-v2
                                     MADO_COUNTER_SELFTEST: checks=10 failed=0   rc=0 wall=37s (44s re-run)
```

`selftest_green = 2/2 from the promoted layout` (L1 requirement) — both counters, both layouts,
N=10 ≥ 6. Wall clock: c1 ≈ 10–12 s, c2 ≈ 33–44 s per selftest run.

**Red runs (rc and stable ids, all measured with the final bytes).**

```
c1 missing-input  (counter alone, bare --selftest):  rc=1
  FIXTURES: UNRESOLVED + MADO_COUNTER_SELFTEST_FAIL: st-fixture-dir, st-tool-pin,
  st-gate-target-met, st-result-line-format, st-scratch-clean, st-setup-missing-input,
  st-setup-wrong-pin, st-setup-wrong-rev, st-target-missed-case, st-target-missed-mutant
  -> checks=10 failed=10
c1 wrong-rev      (every fixture file truncated to 0 bytes):  rc=1, ids = all except
  st-fixture-dir (checks=10 failed=9); identical id set from cwd=/tmp (stability probe)
c1 mutated-tool   (marker appended to c1/mado-mimetext.py):  rc=1,
  MADO_COUNTER_SELFTEST_FAIL: st-tool-pin ONLY (checks=10 failed=1) — the pin branch catches the
  tampered fixture while the run itself stays self-consistent
c1 renamed-file   (cases-mini.json renamed): rc=1, ids = all except st-fixture-dir; the id set is
  IDENTICAL across cwd (diff of two transcripts: empty)
c2 missing-input: rc=1, checks=10 failed=10, same shape as c1
c2 wrong-rev:     rc=1, checks=10 failed=9 (st-fixture-dir passes, everything else fails)
c2 mutated-tool   (marker appended to c2/dummy-tool.py): rc=1, ids = {st-tool-pin,
  st-gate-target-met, st-result-line-format} (checks=10 failed=3)
```

**Neutralisation matrix (the panel contract, measured 2×10 rows against the final bytes).** Every
check has a unique definition-line anchor (audit printed `none (all ==1)` for both blocks);
replacing it with the weakened text and rerunning `--selftest --fixture-dir <tree>` exits 1 and
prints that check's own `MADO_COUNTER_SELFTEST_FAIL` id. Measured transcript (rc and printed ids
per row):

```
c1 st-fixture-dir      rc=1 ids=[st-fixture-dir, st-tool-pin, st-gate-target-met,        (designed
                         st-result-line-format, st-scratch-clean, st-setup-missing-input,  cascade:
                         st-setup-wrong-pin, st-setup-wrong-rev, st-target-missed-case,    fixture dir
                         st-target-missed-mutant]                                          gates all runs)
c1 st-tool-pin         rc=1 ids=[st-tool-pin]
c1 st-gate-target-met  rc=1 ids=[st-gate-target-met]
c1 st-setup-missing-input / st-setup-wrong-pin / st-setup-wrong-rev / st-target-missed-case /
   st-target-missed-mutant / st-result-line-format / st-scratch-clean
                       rc=1 ids=[<exactly the target id>]                                (7 rows)
c2: identical shape — st-fixture-dir cascades (10 ids), the other nine rows fail with exactly
   their own id.                                              ALL-FLAGGED: True  (20/20 rows)
```

The runner's `flagged = rc == 1 and declared id in stdout` holds for every row; 18 of 20 rows fail
with exactly one id (the two `st-fixture-dir` rows cascade because the fixture directory gates every
run). Anchors and the measured matrix JSON were handed to R97MMutC2b for the frozen panel.

**Anchor inventory (for MutC2b's frozen panel; each line occurs exactly once):**
`_ST_PINS_REL = "pins.json"`, the `_ST_PIN_REQUIRED = (...)` first three entries, `_ST_GREEN_RC_WANT
= 0`, `_ST_MISSING_RC_WANT = 2`, `_ST_PINRUN_RC_WANT = 2`, `_ST_BADREV_RC_WANT = 2`,
`_ST_MISSED_CASE_RC_WANT = 1`, `_ST_MISSED_MUT_RC_WANT = 1`, `_ST_LINE_RC_WANT = 0`,
`os.listdir(scr) == []` — same names in both counters.

**Coordination.** R97MExecCounterC2b's runner (abb17a019141c57635f1c9771ad449a4348dfdc75a0bb57af377
6075fe06b879) serves every scene: counters materialised at `<root>/quality/counters/<name>.py`,
fixture tree passed as terminal `--fixture-dir`; broken modes vary only `--fixture-dir`. MutC2b
received the final shas, the anchor inventory and the broken-mode declarations; R97MReviewC2b's
three w1 findings (absolute-lane fallback, broken `draft` line, missing selftest on c2) are
structurally absent from the v2 bytes. R97MCritic2/MadoR97 fixture-layout requirements (default
resolution from the counter's own path, both layouts green, `FIXTURES:` line) are implemented and
measured above.

## Risks and blockers

- The c1/c2 mini-runs rebind this module's own census thresholds (`_ST_MINI_REBIND`) so the frozen
  production predicate can be satisfied at fixture scale without editing production lines. This is
  the round-26 counter-selftest precedent (monkeypatching the counter module), but it means the
  green leg proves the pipeline machinery, not the production census gates — those are exercised
  only at the real measurement (the counters' own cross-leg), as the declaration's named limits
  already state.
- c2's green leg embeds the real r96 gate/tool/kills/panel bytes as fixtures; if those files ever
  drift at a future rev, `st-tool-pin` (pins.json) and the gate/tool pins fail together — the
  failure is loud, not silent.
- `st-scratch-clean` asserts the counter's own scratch cleanup only (work/secret subtrees removed);
  the selftest's runtime input files are written into the fixture repo dir, not the scratch root.
- Wall clock: c2's selftest needs ~35–45 s (real gate runs 7 receipt-tool selftests per gate
  invocation). The runner's per-run timeout (120 s default in the w1 draft) accommodates this with
  margin; if a future runner lowers it below ~50 s the c2 leg would time out (fail loud, not silent).
- The neutralisation matrix and red-scene transcripts were captured against the final bytes; the
  w1 draft files (`build/c1-r96-magictext-selftest.py`, `build/c2-r96-selftest-kills-selftest.py`)
  are dead and should not land (the c1 draft references an undefined `_mado_counter_selftest`, the
  c2 draft is a bare byte copy).

## Checks for the main agent

1. `sha256sum .ufo/waves/round-97/build/c1-r96-magictext-selftest.v2.py
   .ufo/waves/round-97/build/c2-r96-selftest-kills-selftest.v2.py` → the two shas above.
2. `python3 -I .ufo/waves/round-97/build/<name>.v2.py --selftest` from the lane root →
   `checks=10 failed=0` rc 0, twice (both counters).
3. Strip proof: cut at the marker line, append the base guard, `diff` against
   `git show e6152b58:quality/counters/<name>.py` → empty.
4. Hand both counters + `.ufo/waves/round-97/selftest-fixtures-v2/` to R97MMutC2b's frozen panel
   and R97MExecCounterC2b's runner; the 20-row neutralisation matrix above should reproduce
   ALL-FLAGGED, and the three broken modes should reproduce the declared id sets.

## Report

Report: .ufo/waves/round-97/w1b/R97MExecC2b.md
