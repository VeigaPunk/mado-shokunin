CANDIDATE /fast/scratch/hyaku/mado-r27/data/ExecSuiteA1/counter-selftest.py sha256:7fd94b0431849d1be7dc99e120c2f5bd0105c6a1d122e9cd1a3327d30ef3c587

# ExecSuiteA1 — round 27 wave w2, suite A (C2 data seat)

Suite A of the C2 claim: an offline gate over the two round-26 counters
`.ufo/waves/round-26/c1/count-v2.py` (C1, animations table) and `.ufo/waves/round-26/c2/count.py`
(C2, binds table). It exits 0 only when every behavioural check passes; it prints the subjects'
sha256 for traceability but pins nothing.

## What it is

Successor of `.ufo/waves/round-26/quality/counter-selftest.py`. The round-26 file fails green on
the active C1 v2 counter (7/9) because its fake oracle answers the `version` verb with an
animation table, so the counter's version guard fires (`SETUP_ERROR ORACLE_VERSION nested
Hyprland commit None is not efb5099…`). This suite's fake oracle answers `version` with the
wave's pinned Hyprland v0.56.2 commit, and the version guard is itself one of the checks.

Method (unchanged in spirit from round 26, extended):

* each counter is imported by path; its harness surfaces are replaced before use —
  `O.check_build` → no-op, `O.coredumps` → 0, `O.snapshot` → a synthetic Hyprland tree,
  `O.oracle` → synthetic per-verb tables (optionally drifting, failing, or marking a case tree),
  `O.run_tool` → the tool file executed in-process with its stdout parsed exactly as the
  harness does, and the counter's `tempfile` → a shim rooted in this run's scratch;
* the counter is then asked to judge synthetic tools. The truth is a fixed synthetic table
  (3 animation nodes + 3 beziers; 3 bind entries with all 18 compared fields) that the fake
  oracle hands to the counter and the tool file reproduces, so a correct counter scores
  41/41 (C1) and 51/51 (C2) and a wrong one is scored on the difference;
* every check is a behavioural probe: no subject hash, AST or byte pattern is pinned, no mutant
  text is blocklisted, and nothing about the surrounding process, path, environment or timing is
  inspected.

## Checks (48 = 47 behavioural + 1 inventory gate)

| group | checks | what must happen |
|---|---|---|
| C1 | `c1-perfect` | exit 0, `TARGET_MET`, `cases_pass=41/41` |
| C1 | `c1-field-{name,overridden,bezier,enabled,speed,style}` | one node field wrong → exit 1, `TARGET_MISSED` |
| C1 | `c1-bezier-{name,x0,y0,x1,y1}` | one bezier field wrong (nodes untouched) → exit 1, `TARGET_MISSED` |
| C1 | `c1-invalid-json`, `c1-malformed`, `c1-tool-exit` | tool prints non-JSON / wrong shape / exits non-zero → exit 1 |
| C1 | `c1-near-perfect` | exactly 40 of 41 cases right → exit 1, `cases_pass=40/41` |
| C1 | `c1-drift`, `c1-drift-bezier` | two BASE oracle runs disagree (nodes / beziers) → exit 2, `ORACLE_UNSTABLE` |
| C1 | `c1-oracle-fail` | every oracle call fails → exit 2, `ORACLE_FAIL` |
| C1 | `c1-version-guard` | nested Hyprland commit is wrong → exit 2, `ORACLE_VERSION` |
| C2 | `c2-perfect` | exit 0, `TARGET_MET`, `cases_pass=51/51`, `embed_hits=0` |
| C2 | `c2-field-*` (18 fields) | one bind field wrong → exit 1, `TARGET_MISSED` |
| C2 | `c2-invalid-json`, `c2-malformed`, `c2-tool-exit` | tool prints non-JSON / not a list / exits non-zero → exit 1 |
| C2 | `c2-near-perfect` | exactly 50 of 51 cases right → exit 1, `cases_pass=50/51` |
| C2 | `c2-embed`, `c2-embed-desc` | tool bytes hold a 40-char base arg / description → exit 1, `embed_hits>=1` |
| C2 | `c2-drift` | two BASE oracle runs disagree → exit 2, `ORACLE_UNSTABLE` |
| C2 | `c2-oracle-fail` | every oracle call fails → exit 2, `ORACLE_FAIL` |
| both | `check-inventory` | the fixed required inventory was fully executed |

One field per check, so a counter that stops comparing that field alone is caught by that check
alone. `c2-embed` and `c2-embed-desc` put the long string in the `arg` and in the `description`
respectively, so a counter that scans only one of the two fields is caught.

**Fixed required check inventory.** `REQUIRED` lists all 47 probe names and `TOTAL` is fixed at
`len(REQUIRED) + 1`, independently of how many checks were recorded. After the probes the suite
compares the executed names with `REQUIRED` (`check-inventory`) and also compares the number of
recorded checks with `TOTAL`; a check that silently disappears, or the inventory gate itself
being deleted, makes the run fail. Verified: a copy of the suite with the whole
`record("c2-embed", …)` call deleted exits 1 with `FAILED check-inventory` and
`SELFTEST pass=-1 total=48`.

**Near-perfect probe.** The fake oracle writes a marker file into the first *case* tree it is
asked about (never the unperturbed snapshot, whose contents are copied into every case). The
tool then prints a corrupted table for that one case only, so the counter scores exactly
40/41 (C1) and 50/51 (C2). No call-order assumption: the snapshot home is known to the fake
oracle because the fake `O.snapshot` records it.

**Offline.** No Hyprland, no compositor, no display variable, no network, no `/dev/dri`. The
counters' `check_build`/`coredumps`/`snapshot`/`oracle`/`run_tool` are all replaced, so the
harness binaries (`tinywl`) are never needed and `coredumpctl` is never called. Scratch is one
`mkdtemp` under `TMPDIR` (the counter's sandbox puts `TMPDIR` inside the run directory, so it
lands under `/fast/scratch/hyaku/mado-r27/`), and the counters' own temporary directories are
redirected into it; it is removed at the end. The only environment reads are `TMPDIR` and the
removal of `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`.

## Verification (all commands run by this seat)

1. **Pristine counters, in the lane** (subjects at `2fdca5ca`):

   ```
   cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk \
     timeout 300 prlimit --as=4000000000 --core=0 -- python3 -I \
     /fast/scratch/hyaku/mado-r27/data/ExecSuiteA1/counter-selftest.py \
     --c1 .ufo/waves/round-26/c1/count-v2.py --c2 .ufo/waves/round-26/c2/count.py \
     --rev 2fdca5ca --scratch /fast/scratch/hyaku/mado-r27/data/ExecSuiteA1/scratch
   ```

   → `SELFTEST pass=48 total=48`, `exit=0`, stderr empty, 2.4 s wall / 1.7 s user CPU.

2. **Inside the counter's own bubblewrap sandbox** (`/home` and `/fast` hidden, clone bound,
   `HOME`/`TMPDIR` inside the run directory) — the same command line the frozen counter builds:

   ```
   bwrap --ro-bind / / --tmpfs /home --tmpfs /fast --tmpfs /run --tmpfs /tmp \
     --bind $D $D --dev /dev --proc /proc --unshare-all --die-with-parent --new-session \
     --clearenv --setenv PATH /usr/bin --setenv HOME $D/home --setenv TMPDIR $D/tmp \
     --chdir $D/m python3 -I $D/m/quality/counter-selftest.py \
     --c1 $D/m/.ufo/waves/round-26/c1/count-v2.py \
     --c2 $D/m/.ufo/waves/round-26/c2/count.py --rev 2fdca5ca
   ```

   → `SELFTEST pass=48 total=48`, `exit=0`, 2.2 s. (The candidate was copied to
   `quality/counter-selftest.py` inside the clone, as the counter does.)

3. **Frozen round-27 C2 counter v2 with the candidate as suite A:**

   ```
   cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk \
     timeout 1800 prlimit --as=4000000000 --core=0 -- python3 -I \
     .ufo/waves/round-27/c2/count-v2.py 2fdca5ca \
     --suite-a-file /fast/scratch/hyaku/mado-r27/data/ExecSuiteA1/counter-selftest.py --jobs 6
   ```

   → suite A green runs 5/5 `rc=0 PASS` (pristine + the two public behaviour-preserving edits
   of each of the two counters; the other three green runs are suite B's, and
   `quality/population-suite.py` is missing at this REV — another seat's artefact);
   suite A W mutants 9/9 `rc=1 KILLED` (`c1-drop-bezier`, `c1-accept-nonjson`, `c1-pass-90pct`,
   `c1-skip-base-guard`, `c2-accept-nonjson`, `c2-pass-90pct`, `c2-skip-base-guard`,
   `c2-embed-min-1000`, `c2-drop-arg`). The remaining 5 W mutants (`q37-*`) are mutants of
   `quality/check-population.py` and are scored against suite B, not this suite.
   Counter line: `green=5/8 b_valid=0 w_killed=9/15 h_valid=0 verdict=TARGET_MISSED`
   (the shortfall is suite B's, and no held-out set was passed).

4. **Mutation test of the suite** (driver `/fast/scratch/hyaku/mado-r27/data/ExecSuiteA1/mutcheck.py`,
   receipt `/fast/scratch/hyaku/mado-r27/data/ExecSuiteA1/mutcheck.log` and `mutcheck.json`;
   a `--no-local` clone of the lane under the scratch root, `GIT_DIR`/`GIT_WORK_TREE`/
   `GIT_INDEX_FILE` unset; the lane itself was never written to). 28 probes, `SUMMARY total=28
   unexpected=0`:

   * the 9 public W mutants of the two counters → all killed (exit 1, named failed check);
   * 6 behaviour-preserving edits (appended comment / inserted unused module-level assignment)
     of all three subjects → all green (48/48, exit 0);
   * 12 extra single-defect probes of my own design, approximating the sealed held-out set →
     all killed: `c1-drop-style-field`, `c1-drop-bezier-x0-field`, `c1-skip-version-guard`,
     `c1-pass-off-by-one`, `c1-accept-malformed`, `c1-or-instead-of-and`, `c1-drift-nodes-only`,
     `c2-drop-embed-condition`, `c2-embed-arg-only`, `c2-tolerate-one-missing`,
     `c2-accept-nonlist`, `c2-base-guard-loose`;
   * the suite's own inventory gate → a copy with the `c2-embed` record deleted exits 1 with
     `FAILED check-inventory`.

   Representative lines from the receipt:

   ```
   W c1-drop-bezier      rc=1 SELFTEST pass=43 total=48 FAILED c1-bezier-name,c1-bezier-x0,c1-bezier-y0,c1-bezier-x1,c1-bezier-y1
   W c2-drop-arg         rc=1 SELFTEST pass=46 total=48 FAILED c2-field-arg,c2-near-perfect
   GREEN count-v2.py:assign rc=0 SELFTEST pass=48 total=48
   EXTRA c1-or-instead-of-and rc=1 SELFTEST pass=36 total=48 FAILED c1-field-name,…,c1-bezier-y1,c1-near-perfect
   SUITE drop-c2-embed-record rc=1 SELFTEST pass=-1 total=48 FAILED check-inventory
   SUMMARY total=28 unexpected=0
   ```

## Limits and risks

* **Population mutations are not observable.** With a fake oracle the suite judges the
  counter's *comparison* logic. A mutation that only changes how the counter generates its cases
  (its `NARITH`/`NCASES`, the case generator, the tree perturbations) leaves the tool and the
  oracle agreeing, so such a mutant can survive. The number of cases is pinned indirectly
  (`cases_pass=41/41` and `51/51` in the two perfect checks), which catches count-changing
  mutations, but not content-changing ones. This is inherent to an offline gate with a fake
  oracle; the round-26 suite had the same blind spot.
* **The tool runs in-process.** The harness' `run_tool` spawns a sandboxed `python3`; the fake
  here executes the tool file in-process and parses its stdout exactly as the harness does.
  This keeps a suite run at ~2.4 s (so the counter's 300 s per-suite timeout is never in
  reach, even with six suites in parallel) and does not weaken what is under test — the
  counter's judgement of the tool's output, not the tool's process. The tool file is still
  written to disk, which is what the C2 counter's embed scan reads.
* **Dependencies of the counters stay sha-pinned by the counters themselves.** `c2/count.py`
  loads `.ufo/waves/round-26/harness/oracle.py` and `.ufo/waves/round-25/c1/count-v3.py` under
  their own sha256 pins, so those two files must be pristine in the clone. They are not subjects
  and are not edited by the counter's green/mutant rows; if a future revision changed them the
  counter would exit 2 at import and the suite reports `SETUP_ERROR cannot load …` and exits 1.
* **Held-out set.** Not read (forbidden). The 12 extra probes above are my own design and were
  written to approximate plausible held-out single-defect mutations of the two counters; they
  are not the sealed set and make no claim about it.
* The suite prints the subjects' sha256 but never compares them to a pin, so behaviour-preserving
  edits of the subjects stay green (verified for both public edit kinds on all three subjects).

## Host safety

* No Hyprland was started by this seat; the counters' `check_build`/`coredumps`/`snapshot`/
  `oracle`/`run_tool` were all replaced, so no compositor, no `hyprctl`, no tinywl and no
  `coredumpctl` call happened. `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE` were never set
  or inherited (every run used `env -i PATH=/usr/bin HOME=…`).
* Hyprland coredump count on the host: 1338 before this seat's last measurement and 1338 after
  (delta 0; the count is a host-wide total that this seat did not change).
* All commands were `timeout`- and `prlimit`-bounded (4 GB address space); the suite writes
  only inside its own scratch directory and removes it; `df -h /fast` showed 69–72 G free
  throughout.
* No tool or package was installed or updated (none was needed). No subagent was dispatched.
* Lane writes: this report only. The candidate lives outside the lane, under
  `/fast/scratch/hyaku/mado-r27/data/ExecSuiteA1/`, and is copied into the lane unmodified by
  the L1.

Report: .ufo/waves/round-27/w2/reports/ExecSuiteA1.md
