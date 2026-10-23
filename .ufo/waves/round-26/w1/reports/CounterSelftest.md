# R2 — counter self-test (round 26, wave w1)

Verdict: **PASS.** The offline self-test is green at 9/9 (`SELFTEST pass=9 total=9`, exit 0) against
the frozen counters, and each of its nine checks was made to fail by a named or supplementary
one-line counter mutant. The frozen counters, `harness/oracle.py` and `round-25/c1/count-v3.py`
were never edited; their hashes still match the round-26 registration pins.

This repairs the round-25 spot-check defect R2: the survivors `skip-oracle-check` and
`embed-threshold-1000` (plus the unexercised field comparison) were checks that no assigned input
ever made false. The self-test injects the faults those mutants remove the guards for:
a second-BASE drift for the drift guard, a 40-char base-table arg in the tool bytes for the embed
threshold, and a one-field-off tool for the field comparison. It also falsifies its own
acceptance and oracle-failure assertions, so all nine checks have red evidence.

## What was built

`.ufo/waves/round-26/quality/counter-selftest.py` (single Python 3 stdlib file, sha256
`0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a`, 15,488 bytes).

It imports `c1/count.py` and `c2/count.py` by path with `importlib`, lets each counter run its own
pinned imports (`harness/oracle.py` and `round-25/c1/count-v3.py` are read and hash-checked by the
counters themselves), then replaces the counters' harness surfaces before calling `main()`:

| Attribute | Replacement | Why |
|---|---|---|
| `O.check_build` | no-op | no tinywl/libwlroots binaries needed; stays offline |
| `O.coredumps` | `lambda: 0` | no `coredumpctl`, no host compositor |
| `O.snapshot` | synthetic tree (`hyprland.conf` + sourced `binds.conf`) | no home config read |
| `O.oracle` | synthetic tables, optionally a second-BASE drift or total failure | exercises the guards |
| `O.run_tool` | plain `python3 -I <tool> --home DIR` | no bwrap, no compositor |
| `tempfile` | shim rooted at this run's private scratch dir | containment and cleanup |

Each scenario writes a fixture tool that prints a constant JSON payload, so expected and actual are
under the self-test's control while the counters' own case generators, shuffling, comparison and
predicate code all run unchanged. The synthetic C1 table has 3 nodes and 2 beziers; the synthetic C2
table has 3 bind entries with all 18 `hyprctl binds -j` fields (`mask 64`, keys Q/W/E) and real bind
lines in the synthetic tree that map to them, so the V3 REWRITE/HARD generators have valid inputs.
The perfect-tool table's arg/description strings are all shorter than `EMBED_MIN` (12), so only the
dedicated embed fixture can trip the embed scan.

Usage:

```sh
python3 -I counter-selftest.py [--c1 PATH] [--c2 PATH] [--rev REV] [--scratch DIR] [--keep]
```

`--c1`/`--c2` exist so the same checks run against mutated scratch copies (the red runs below).
The default paths are the frozen counters; the header prints each counter's sha and whether it
matches the registration pin. The self-test prints its own sha, each check as
`CHECK <name> PASS|FAIL rc=... cases_pass=... verdict=...`, and finishes with
`SELFTEST pass=N total=M` and `exit=N`; it exits 0 only when all checks pass.

## The nine checks

| Check | Fixture | Assertion |
|---|---|---|
| `c1-perfect` | exact `[nodes, beziers]` table | exit 0, `cases_pass=41/41`, `TARGET_MET` |
| `c2-perfect` | exact 18-field bind table | exit 0, `cases_pass=51/51`, `embed_hits=0`, `TARGET_MET` |
| `c1-one-field` | one node's `style` changed | exit 1, `TARGET_MISSED` |
| `c2-one-field` | one bind's `arg` changed | exit 1, `TARGET_MISSED` |
| `c1-drift` | BASE#1 table, then a table with one changed node field | exit 2, `ORACLE_UNSTABLE` |
| `c2-drift` | BASE#1 table, then a table with one changed bind `key` | exit 2, `ORACLE_UNSTABLE` |
| `c2-embed` | tool bytes contain the 40-char base arg | exit 1, `embed_hits>=1`, `TARGET_MISSED` |
| `c1-oracle-fail` | every oracle call returns `(None, error)` | exit 2, `ORACLE_FAIL` |
| `c2-oracle-fail` | every oracle call returns `(None, error)` | exit 2, `ORACLE_FAIL` |

The drift fixture for C2 changes a `key`, not an `arg`, so the field-dropped mutant that removes
`arg` from the comparison cannot mask the drift guard by accident.

## Exact commands

Green (run twice on fresh scratch dirs, both exit 0; the retained receipt is the final run, produced
by this exact command; the equivalent `cd lane && python3 -I .ufo/waves/round-26/quality/counter-selftest.py`
form was also run and exited 0):

```sh
set +e
L=/home/vgpnk/Projects/shokunin/mado-shokunin
ST=$L/.ufo/waves/round-26/quality/counter-selftest.py
G=$L/.ufo/waves/round-26/quality/counter-selftest-green.txt
timeout 600 prlimit --as=4000000000 --core=0 -- python3 -I "$ST" 2>&1 | tee "$G" >/dev/null
```

Mutation mirrors (scratch only; byte-identical copies of the frozen files plus the pinned harness and
generator, with a read-only `.git` symlink for the counters' `git rev-parse`):

```sh
L=/home/vgpnk/Projects/shokunin/mado-shokunin
for M in skip-guard embed-threshold-1000 field-dropped final-threshold fail-open; do
  R=/fast/scratch/hyaku/mado-r26/q-r2-$M
  mkdir -p "$R/.ufo/waves/round-26/c1" "$R/.ufo/waves/round-26/c2" \
           "$R/.ufo/waves/round-26/harness" "$R/.ufo/waves/round-25/c1"
  cp "$L/.ufo/waves/round-26/c1/count.py"          "$R/.ufo/waves/round-26/c1/count.py"
  cp "$L/.ufo/waves/round-26/c2/count.py"          "$R/.ufo/waves/round-26/c2/count.py"
  cp "$L/.ufo/waves/round-26/harness/oracle.py"    "$R/.ufo/waves/round-26/harness/oracle.py"
  cp "$L/.ufo/waves/round-25/c1/count-v3.py"       "$R/.ufo/waves/round-25/c1/count-v3.py"
  ln -s "$L/.git" "$R/.git"
done
```

Red runs (each exactly the command captured in the receipt):

```sh
python3 -I .ufo/waves/round-26/quality/counter-selftest.py \
  --c1 /fast/scratch/hyaku/mado-r26/q-r2-<mutation>/.ufo/waves/round-26/c1/count.py \
  --c2 /fast/scratch/hyaku/mado-r26/q-r2-<mutation>/.ufo/waves/round-26/c2/count.py \
  --rev 05319e0f
```

## Green receipt (verbatim)

Receipt: `.ufo/waves/round-26/quality/counter-selftest-green.txt`, 3,954 bytes.

```text
MADO R26 QUALITY R2 counter self-test (offline; synthetic tables; no Hyprland)
selftest sha256:0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a
c1=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/c1/count.py sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd pin=yes
c2=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/c2/count.py sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 pin=yes
rev=05319e0f seed=0badc0de12345678 scratch=/fast/scratch/hyaku/mado-r26/q-r2-selftest-uyqnjwxg
CHECK c1-perfect         PASS rc=0 cases_pass=41/41 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET
      CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
      CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-one-field       PASS rc=1 cases_pass=0/41 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
      CASE BASE  FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (unperturbed)
      CASE C00   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree
CHECK c1-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure
CHECK c2-perfect         PASS rc=0 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-one-field       PASS rc=1 cases_pass=0/51 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
      CASE BASE           FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      CASE A00            FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      ... 48 CASE lines omitted ...
      CASE VHARD-1        FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
CHECK c2-embed           PASS rc=1 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      EMBED_HIT 'notify-send r26-embed-fixture-0123456789'
      PRED-C2-r26 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree (1/1)
CHECK c2-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure synthetic oracle failure

SELFTEST pass=9 total=9
exit=0
```

## Red runs

Mutation map (each mutation is the only change in its mirror; line numbers are the frozen counters'):

| Mirror | Mutation | Checks expected red | Result |
|---|---|---|---|
| `skip-guard` | C1 `if node_set(b1) != ... :` → `if False:`; C2 `if n1 or n2:` → `if False:` | `c1-drift`, `c2-drift` | 7/9 |
| `embed-threshold-1000` | C2 `EMBED_MIN = 12` → `1000` | `c2-embed` | 8/9 |
| `field-dropped` | C1 drops `style` from `NODE_FIELDS`; C2 drops `arg` from `V3.FIELDS` | `c1-one-field`, `c2-one-field` | 7/9 |
| `final-threshold` (supplementary) | C1/C2 `met = npass == len(built)` → `== len(built) + 1` | `c1-perfect`, `c2-perfect` | 7/9 |
| `fail-open` (supplementary) | C1 `if res is None:` → `if False:`; C2 `if r1 is None or r2 is None:` → `if False:` | `c1-oracle-fail`, `c2-oracle-fail` | 7/9 |

Every one of the nine checks is red under at least one mutant. The key counterexamples:

- The guard-skipped counter never prints `ORACLE_UNSTABLE`; with a second-BASE drift it proceeds
  and exits 1 with `cases_pass=1/41` (C1) and `1/51` (C2). The frozen counter exits 2.
- The `EMBED_MIN=1000` counter accepts the embedded tool: `cases_pass=51/51 embed_hits=0
  verdict=TARGET_MET`, exit 0. The frozen counter reports `embed_hits=1`, `TARGET_MISSED`, exit 1.
- The field-dropped counters accept the one-field-off tools (`41/41` and `51/51`, `TARGET_MET`,
  exit 0) where the frozen counters report `0/41` and `0/51`, `TARGET_MISSED`, exit 1.
- The final-threshold mutant rejects the perfect tools (`41/41` / `51/51` but `TARGET_MISSED`,
  exit 1) where the frozen counters accept them.
- The fail-open mutant crashes with `TypeError("'NoneType' object is not subscriptable")` on oracle
  failure instead of exiting 2 with `ORACLE_FAIL`.

Mutated counter shas (from the receipt): skip-guard C1 `76ab3638…2044`, C2 `ed51ef0b…50a8`;
embed-threshold C2 `e5f08b47…c3fc`; field-dropped C1 `1b7a07a3…e0d4`, C2 `a33a3d14…1a0a`;
final-threshold C1 `a5fc9c62…51fd`, C2 `abee34af…6e69`; fail-open C1 `9e7ad73a…e8df`,
C2 `273bcce3…c430`. Unmutated copies in each mirror stayed at the frozen shas (printed per run).

### Red receipt (verbatim)

Receipt: `.ufo/waves/round-26/quality/counter-selftest-red.txt`, 24,135 bytes.

```text
# R2 red runs: the same offline self-test against mutated scratch copies of the frozen counters
# counters under /fast/scratch/hyaku/mado-r26/q-r2-<mutation>/ ; each section names its mutation.
# sections 1-3 are the three mutants named in the assignment; 4-5 falsify the remaining two
# assertion classes (perfect tool, oracle failure) so all nine checks are shown able to fail.

== skip-guard ==
76ab36383e4eab3254417d9dad42ac188bcb6b93030f520305b19f2f16ed2044  /fast/scratch/hyaku/mado-r26/q-r2-skip-guard/.ufo/waves/round-26/c1/count.py
ed51ef0bd65b914e1507c706ed62416ed1889d46cb545a82da4e4acd218b50a8  /fast/scratch/hyaku/mado-r26/q-r2-skip-guard/.ufo/waves/round-26/c2/count.py
COMMAND: python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/counter-selftest.py --c1 /fast/scratch/hyaku/mado-r26/q-r2-skip-guard/.ufo/waves/round-26/c1/count.py --c2 /fast/scratch/hyaku/mado-r26/q-r2-skip-guard/.ufo/waves/round-26/c2/count.py --rev 05319e0f
MADO R26 QUALITY R2 counter self-test (offline; synthetic tables; no Hyprland)
selftest sha256:0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a
c1=/fast/scratch/hyaku/mado-r26/q-r2-skip-guard/.ufo/waves/round-26/c1/count.py sha256:76ab36383e4eab3254417d9dad42ac188bcb6b93030f520305b19f2f16ed2044 pin=no(override/mutant)
c2=/fast/scratch/hyaku/mado-r26/q-r2-skip-guard/.ufo/waves/round-26/c2/count.py sha256:ed51ef0bd65b914e1507c706ed62416ed1889d46cb545a82da4e4acd218b50a8 pin=no(override/mutant)
rev=05319e0f seed=0badc0de12345678 scratch=/fast/scratch/hyaku/mado-r26/q-r2-selftest-mvyuk68o
CHECK c1-perfect         PASS rc=0 cases_pass=41/41 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET
      CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
      CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-one-field       PASS rc=1 cases_pass=0/41 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
      CASE BASE  FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (unperturbed)
      CASE C00   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-drift           FAIL rc=1 ORACLE_UNSTABLE=no
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=1/41 verdict=TARGET_MISSED
      CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
      CASE C00   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure
CHECK c2-perfect         PASS rc=0 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-one-field       PASS rc=1 cases_pass=0/51 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
      CASE BASE           FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      CASE A00            FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      ... 48 CASE lines omitted ...
      CASE VHARD-1        FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
CHECK c2-embed           PASS rc=1 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      EMBED_HIT 'notify-send r26-embed-fixture-0123456789'
      PRED-C2-r26 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-drift           FAIL rc=1 ORACLE_UNSTABLE=no
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=1/51 embed_hits=0 verdict=TARGET_MISSED
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="X" code=0 disp="exec" arg="firefox" | extra mask=64 key="W" code=0 disp="exec" 
      ... 48 CASE lines omitted ...
      CASE VHARD-1        FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="X" code=0 disp="exec" arg="firefox" | extra mask=64 key="W" code=0 disp="exec" 
CHECK c2-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure synthetic oracle failure

SELFTEST pass=7 total=9
FAILED c1-drift,c2-drift
exit=1
RUN_EXIT=1

== embed-threshold-1000 ==
f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd  /fast/scratch/hyaku/mado-r26/q-r2-embed-threshold-1000/.ufo/waves/round-26/c1/count.py
e5f08b47947cc998a7af202f17498b5110808c9c3062d33c15793eff0790c3fc  /fast/scratch/hyaku/mado-r26/q-r2-embed-threshold-1000/.ufo/waves/round-26/c2/count.py
COMMAND: python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/counter-selftest.py --c1 /fast/scratch/hyaku/mado-r26/q-r2-embed-threshold-1000/.ufo/waves/round-26/c1/count.py --c2 /fast/scratch/hyaku/mado-r26/q-r2-embed-threshold-1000/.ufo/waves/round-26/c2/count.py --rev 05319e0f
MADO R26 QUALITY R2 counter self-test (offline; synthetic tables; no Hyprland)
selftest sha256:0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a
c1=/fast/scratch/hyaku/mado-r26/q-r2-embed-threshold-1000/.ufo/waves/round-26/c1/count.py sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd pin=yes
c2=/fast/scratch/hyaku/mado-r26/q-r2-embed-threshold-1000/.ufo/waves/round-26/c2/count.py sha256:e5f08b47947cc998a7af202f17498b5110808c9c3062d33c15793eff0790c3fc pin=no(override/mutant)
rev=05319e0f seed=0badc0de12345678 scratch=/fast/scratch/hyaku/mado-r26/q-r2-selftest-nj12yzls
CHECK c1-perfect         PASS rc=0 cases_pass=41/41 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET
      CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
      CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-one-field       PASS rc=1 cases_pass=0/41 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
      CASE BASE  FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (unperturbed)
      CASE C00   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree
CHECK c1-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure
CHECK c2-perfect         PASS rc=0 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-one-field       PASS rc=1 cases_pass=0/51 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
      CASE BASE           FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      CASE A00            FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      ... 48 CASE lines omitted ...
      CASE VHARD-1        FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
CHECK c2-embed           FAIL rc=0 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree (1/1)
CHECK c2-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure synthetic oracle failure

SELFTEST pass=8 total=9
FAILED c2-embed
exit=1
RUN_EXIT=1

== field-dropped ==
1b7a07a3c9a451b9da184556b18494c98fe6df8f90cdd652e65409578637e0d4  /fast/scratch/hyaku/mado-r26/q-r2-field-dropped/.ufo/waves/round-26/c1/count.py
a33a3d140ac0bb916b482a34dc3e97547d8f1372b76c991f9e9df015fa411a0a  /fast/scratch/hyaku/mado-r26/q-r2-field-dropped/.ufo/waves/round-26/c2/count.py
COMMAND: python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/counter-selftest.py --c1 /fast/scratch/hyaku/mado-r26/q-r2-field-dropped/.ufo/waves/round-26/c1/count.py --c2 /fast/scratch/hyaku/mado-r26/q-r2-field-dropped/.ufo/waves/round-26/c2/count.py --rev 05319e0f
MADO R26 QUALITY R2 counter self-test (offline; synthetic tables; no Hyprland)
selftest sha256:0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a
c1=/fast/scratch/hyaku/mado-r26/q-r2-field-dropped/.ufo/waves/round-26/c1/count.py sha256:1b7a07a3c9a451b9da184556b18494c98fe6df8f90cdd652e65409578637e0d4 pin=no(override/mutant)
c2=/fast/scratch/hyaku/mado-r26/q-r2-field-dropped/.ufo/waves/round-26/c2/count.py sha256:a33a3d140ac0bb916b482a34dc3e97547d8f1372b76c991f9e9df015fa411a0a pin=no(override/mutant)
rev=05319e0f seed=0badc0de12345678 scratch=/fast/scratch/hyaku/mado-r26/q-r2-selftest-hmlaqhwp
CHECK c1-perfect         PASS rc=0 cases_pass=41/41 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET
      CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
      CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-one-field       FAIL rc=0 cases_pass=41/41 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET
      CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
      CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree
CHECK c1-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure
CHECK c2-perfect         PASS rc=0 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-one-field       FAIL rc=0 cases_pass=51/51 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-embed           PASS rc=1 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      EMBED_HIT 'notify-send r26-embed-fixture-0123456789'
      PRED-C2-r26 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree (1/1)
CHECK c2-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure synthetic oracle failure

SELFTEST pass=7 total=9
FAILED c1-one-field,c2-one-field
exit=1
RUN_EXIT=1

== final-threshold ==
a5fc9c620d99eb22fb6bed8399534045ec1228b937e1efd5d171b7951beb51fd  /fast/scratch/hyaku/mado-r26/q-r2-final-threshold/.ufo/waves/round-26/c1/count.py
abee34af91247c703c7bb964062a2e9c8515a80288e6134da7f18fe235996e69  /fast/scratch/hyaku/mado-r26/q-r2-final-threshold/.ufo/waves/round-26/c2/count.py
COMMAND: python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/counter-selftest.py --c1 /fast/scratch/hyaku/mado-r26/q-r2-final-threshold/.ufo/waves/round-26/c1/count.py --c2 /fast/scratch/hyaku/mado-r26/q-r2-final-threshold/.ufo/waves/round-26/c2/count.py --rev 05319e0f
MADO R26 QUALITY R2 counter self-test (offline; synthetic tables; no Hyprland)
selftest sha256:0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a
c1=/fast/scratch/hyaku/mado-r26/q-r2-final-threshold/.ufo/waves/round-26/c1/count.py sha256:a5fc9c620d99eb22fb6bed8399534045ec1228b937e1efd5d171b7951beb51fd pin=no(override/mutant)
c2=/fast/scratch/hyaku/mado-r26/q-r2-final-threshold/.ufo/waves/round-26/c2/count.py sha256:abee34af91247c703c7bb964062a2e9c8515a80288e6134da7f18fe235996e69 pin=no(override/mutant)
rev=05319e0f seed=0badc0de12345678 scratch=/fast/scratch/hyaku/mado-r26/q-r2-selftest-pk1mog6u
CHECK c1-perfect         FAIL rc=1 cases_pass=41/41 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MISSED
      CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
      CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-one-field       PASS rc=1 cases_pass=0/41 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
      CASE BASE  FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (unperturbed)
      CASE C00   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree
CHECK c1-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure
CHECK c2-perfect         FAIL rc=1 cases_pass=51/51 embed_hits=0 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MISSED
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-one-field       PASS rc=1 cases_pass=0/51 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
      CASE BASE           FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      CASE A00            FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      ... 48 CASE lines omitted ...
      CASE VHARD-1        FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
CHECK c2-embed           PASS rc=1 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      EMBED_HIT 'notify-send r26-embed-fixture-0123456789'
      PRED-C2-r26 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree (1/1)
CHECK c2-oracle-fail     PASS rc=2 ORACLE_FAIL=yes
      SETUP_ERROR ORACLE_FAIL BASE: synthetic oracle failure synthetic oracle failure

SELFTEST pass=7 total=9
FAILED c1-perfect,c2-perfect
exit=1
RUN_EXIT=1

== fail-open ==
9e7ad73aa124c930e7eea4914b7435f50db69129a5f24b2e90aefc8d4aa6e8df  /fast/scratch/hyaku/mado-r26/q-r2-fail-open/.ufo/waves/round-26/c1/count.py
273bcce3fec2a11b9a8db23fc72b1a7369fd2d325482667fcea708c5d346c430  /fast/scratch/hyaku/mado-r26/q-r2-fail-open/.ufo/waves/round-26/c2/count.py
COMMAND: python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/counter-selftest.py --c1 /fast/scratch/hyaku/mado-r26/q-r2-fail-open/.ufo/waves/round-26/c1/count.py --c2 /fast/scratch/hyaku/mado-r26/q-r2-fail-open/.ufo/waves/round-26/c2/count.py --rev 05319e0f
MADO R26 QUALITY R2 counter self-test (offline; synthetic tables; no Hyprland)
selftest sha256:0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a
c1=/fast/scratch/hyaku/mado-r26/q-r2-fail-open/.ufo/waves/round-26/c1/count.py sha256:9e7ad73aa124c930e7eea4914b7435f50db69129a5f24b2e90aefc8d4aa6e8df pin=no(override/mutant)
c2=/fast/scratch/hyaku/mado-r26/q-r2-fail-open/.ufo/waves/round-26/c2/count.py sha256:273bcce3fec2a11b9a8db23fc72b1a7369fd2d325482667fcea708c5d346c430 pin=no(override/mutant)
rev=05319e0f seed=0badc0de12345678 scratch=/fast/scratch/hyaku/mado-r26/q-r2-selftest-wuafjigg
CHECK c1-perfect         PASS rc=0 cases_pass=41/41 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET
      CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
      CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-one-field       PASS rc=1 cases_pass=0/41 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal nodes=3 beziers=2
      PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
      CASE BASE  FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (unperturbed)
      CASE C00   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
      ... 38 CASE lines omitted ...
      CASE C39   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ROOT)
CHECK c1-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree
CHECK c1-oracle-fail     FAIL rc=None ORACLE_FAIL=no
      EXCEPTION TypeError: TypeError("'NoneType' object is not subscriptable")
CHECK c2-perfect         PASS rc=0 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-one-field       PASS rc=1 cases_pass=0/51 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
      CASE BASE           FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      CASE A00            FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
      ... 48 CASE lines omitted ...
      CASE VHARD-1        FAIL oracle_binds=3 missing=1 extra=1 | missing mask=64 key="Q" code=0 disp="exec" arg="kitty" | extra mask=64 key="Q" code=0 disp="exec" ar
CHECK c2-embed           PASS rc=1 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      ORACLE_CHECK base_twice equal binds=3
      EMBED_HIT 'notify-send r26-embed-fixture-0123456789'
      PRED-C2-r26 cases_pass=51/51 embed_hits=1 verdict=TARGET_MISSED
      CASE BASE           PASS oracle_binds=3 missing=0 extra=0 (unperturbed)
      CASE A00            PASS oracle_binds=3 missing=0 extra=0 (ARITH[escaped+move+var+exec]@sourced)
      ... 48 CASE lines omitted ...
      CASE VHARD-1        PASS oracle_binds=3 missing=0 extra=0 (HARD tree lines=27 binds=18 unbinds=2 vars=4)
CHECK c2-drift           PASS rc=2 ORACLE_UNSTABLE=yes
      SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree (1/1)
CHECK c2-oracle-fail     FAIL rc=None ORACLE_FAIL=no
      EXCEPTION TypeError: TypeError("'NoneType' object is not subscriptable")

SELFTEST pass=7 total=9
FAILED c1-oracle-fail,c2-oracle-fail
exit=1
RUN_EXIT=1

```

## What this establishes, and its limits

Established, with the receipts above:

- The frozen counters accept an exact tool (`41/41`, `51/51`, exit 0) and reject a one-field-off
  tool (exit 1) on the same offline inputs.
- The `ORACLE_UNSTABLE` guard is live in both counters: a second BASE run that differs in one field
  makes each counter exit 2 before any tool runs. A mutant with the guard removed does not.
- The embed scan is live at `EMBED_MIN=12`: a 40-char base-table arg present in the tool bytes
  yields `embed_hits=1`, and the counter rejects an otherwise perfect tool. A `EMBED_MIN=1000`
  mutant accepts it.
- The oracle-failure guard is live in both counters: every oracle call failing yields exit 2 with
  `ORACLE_FAIL`. A fail-open mutant crashes instead.
- The `c2-perfect` check requires `cases_pass=51/51` exactly, so a counter that silently truncates
  the case population (for example `V3_PER_TYPE=0`, which prints `31/31`) fails this self-test even
  though the counter's own predicate would still print `TARGET_MET`. [The assertion is in the code;
  that mutant was not separately run here — population is R3's repair, not R2's.]

Limits:

- The synthetic oracle returns constant tables, so this self-test exercises the counters' guard,
  acceptance, comparison and threshold code, not Hyprland semantics, the V3 generator's model, or
  real config parsing. It complements a full counter run; it does not replace one.
- `O.check_build` and `O.coredumps` are replaced, so harness binary pin drift and coredump
  accounting are not tested here. The real counters still enforce both.
- `O.run_tool` is a plain `python3 -I` subprocess, not the bwrap tool sandbox, so sandbox/label-leak
  regressions (M25-2) are outside this self-test; the real counter still uses the sandbox.
- The embed fixture is the assignment's 40-char synthetic arg. The scan also catches args of
  12–39 characters; the fixture does not test that boundary.
- The red mirrors use a `.git` symlink to the lane repository only for `git rev-parse`; no lane git
  or jj write command ran, and `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` were cleared in the
  self-test process before the runs.
- No Hyprland, tinywl, bwrap, display environment, `/dev/dri` node or network was used. The
  self-test's temporary tree lives under `/fast/scratch/hyaku/mado-r26/q-r2-selftest-*` and is
  removed on exit; no such directory or process remained after the runs.

## Files changed

| Path | Change | Size | sha256 |
|---|---|---|---|
| `.ufo/waves/round-26/quality/counter-selftest.py` | new offline self-test | 15,488 B | `0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a` |
| `.ufo/waves/round-26/quality/counter-selftest-green.txt` | new green receipt | 3,954 B | (receipt) |
| `.ufo/waves/round-26/quality/counter-selftest-red.txt` | new red receipt (5 sections) | 24,135 B | (receipt) |
| `.ufo/waves/round-26/w1/reports/CounterSelftest.md` | this report | — | — |

Not changed: `.ufo/waves/round-26/c1/count.py` (`f98e264b…52cd`),
`.ufo/waves/round-26/c2/count.py` (`b92c32da…16a8`),
`.ufo/waves/round-26/harness/oracle.py` (`680798ed…e441`),
`.ufo/waves/round-25/c1/count-v3.py` (`8532d3e9…8375`), and every `tools/` file.
Scratch mirrors `q-r2-{skip-guard,embed-threshold-1000,field-dropped,final-threshold,fail-open}`
under `/fast/scratch/hyaku/mado-r26/` are retained as evidence.

No package or tool was installed or updated. No background job, subagent or service was started.
