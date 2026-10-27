# MutGate — round-49 w1 seat report

Task: mutation run of `quality/check-session-material.py` (>= 20 mutants across each
rule's predicate, the scope switch, the waiver/sidecar acceptance, the summary
arithmetic; detector = the tool's own `--selftest`) + the owed gate both-ways
demonstration on a scratch fixture repo. Leaf seat: no subagents, no installs.

## 1. Method

- Target: `quality/check-session-material.py`, lane tip bytes, sha256
  `82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f` (read-only; lane
  file re-hashed after the run — unchanged, same sha).
- Scratch copy at `/fast/scratch/hyaku/mado-r49/MutGate/gate_pristine.py`; 36 mutants,
  each a single exact-byte replacement asserted unique in the pristine text (0 dropped).
- Detector: `python3 <copy> --selftest` with hardened env (`HOME`, `XDG_CACHE_HOME`,
  `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `TMPDIR` all under scratch;
  `ulimit -f 65536`). Verdict: killed when rc or full output differs from the pristine
  baseline; survived only when rc and output are byte-identical to baseline.
- Baseline: rc=0, `SELFTEST: passed=69/69 failed=0`, 0.3 s (receipts/baseline.txt).

## 2. Mutation results: 36 applied, 22 killed, 14 survived, 0 dropped

Killed (first failing selftest case; full output per mutant in receipts/M##.out):

| id | group | point | first failing case |
|----|-------|-------|--------------------|
| M01 | R1 | `_is_client` title requirement dropped | r1-empty-title-not-a-finding |
| M02 | R1 | `_is_client` accepts empty-string title | r1-empty-title-not-a-finding |
| M03 | R2 | `PROC_RE` program window {0,128}->{1,8} | r2-two-process-rows |
| M04 | R2 | scan_blob R2 rows zeroed | r2-two-process-rows |
| M06 | R3 | scan_blob R3 scan disabled | r3-monitor-identity |
| M07 | R4 | home listing `> limit` -> `>= limit` | r4-limit-threshold-inclusive-at-12 |
| M08 | R4 | home listing threshold removed | r4-three-entry-listing-under-limit |
| M12 | R5 | scan_blob R5 disabled | r5-prose-serial (+4 more) |
| M13 | R5 | `_shape_mask` capital kind letter | r5-detail-masks-token (`9x3+Dx5+9x4`) |
| M14 | R6 | R6 count zeroed | r6-exact-in-prose |
| M16 | scope | scope switch ignored, always all | e2e-outside-ufo-not-scanned |
| M18 | waiver | W2 marker sha equality dropped | waiver-sha-mismatch-rejected |
| M19 | waiver | W1 path-under-waves dropped | waiver-path-outside-waves-rejected |
| M21 | waiver | rule-not-listed check dropped | waiver-per-rule-only-listed-rule |
| M22 | waiver | serial-rule refusal dropped | waiver-serial-rule-not-waivable |
| M23 | waiver | marker grammar band R[1-4]->R[1-6] | waiver-marker-cannot-name-serial-rule |
| M24 | waiver | W4 synthetic-value check disabled | waiver-real-values-rejected (+title cases) |
| M27 | waiver | `use_waivers` switch disabled | waiver-fixture-waived |
| M29 | waiver | registry-in-ufo refusal dropped | waiver-registry-in-ufo-refused |
| M30 | summary | waived findings not removed | waiver-fixture-waived |
| M31 | summary | summary line files/findings swapped | e2e-summary-format |
| M32 | summary | exit code always 0 | e2e-exit-1-on-findings |

Survivors (14) — coverage findings, each a gap the --selftest cannot see:

| id | group | point | why it survives |
|----|-------|-------|-----------------|
| M05 | R3 | `_monitor_reason` ident keys description-only | no fixture has serial + make/model but empty description; the make/model arms are untested |
| M09 | R5 | serial regex tail {3,7}->{4,7} | no positive fixture at the 3-digit tail floor (all positives have 4) |
| M10 | R5 | serial regex digit prefix {2,6}->{3,6} | no positive fixture at the 2-digit prefix floor (all positives have 3) |
| M11 | R5 | serial regex capital run {3,8}->{4,8} | no positive fixture at the 3-cap floor (all positives have 5) |
| M15 | R6 | `serials_from_json` minimum exclusive | no length-4 serial fixture; SERIAL_MIN boundary unpinned |
| M17 | scope | argparse `--scope` choices reduced | selftest calls `run()` directly; the CLI switch is untested |
| M20 | waiver | registry-sha equality dropped | unreachable in pristine flow: W2 sha-mismatch always rejects first (M18's failure shows the check only fires once W2 is broken) |
| M25 | waiver | W4 home-user namespace check dropped | no W4 negative fixture for a real home user (R4 waiver rejection untested) |
| M26 | waiver | W4 pid band check dropped | no fixture with pid > 1024 on a marked file |
| M28 | waiver | `--no-waivers` inverted | flag behaviour untested at CLI level (selftest calls `run(use_waivers=False)`) |
| M33 | summary | RULES tally inflated by one | `SESSION_MATERIAL_RULES:` line content is never asserted |
| M34 | summary | WAIVED files count = findings count | only single-file waiver cases; files==findings==1 indistinguishable |
| M35 | decode | 16 MiB text cut disabled | declared limit, no >16 MiB fixture (docstring already declares the tail is unread) |
| M36 | decode | binary NUL window 8192 -> 8 | no binary fixture with a NUL between offsets 8 and 8192 |

All 14 survivors are output-identical to baseline (rc=0, 69/69). Mutant sha256s in
receipts/mutants.tsv and receipts/MUTANTS.json; per-mutant full selftest output in
receipts/M01.out..M36.out.

## 3. Both-ways demonstration (owed round-48 closure, M48-13 line)

Scratch fixture repo `/fast/scratch/hyaku/mado-r49/MutGate/bothways`; before any commit
`git rev-parse --show-toplevel` == the fixture dir (asserted in demo.py, recorded
toplevel_ok=true in demo-meta.json). Throwaway identity used only inside that verified
fixture. Gate = pristine scratch copy (sha `82c9053a…`), env-hardened as above.

- RED rev `472bd30a27d7790faf25582ae8a43f91a94930b4`: two real-shaped synthetic files,
  unmarked — `.ufo/waves/round-49/w1/MutGate/fixtures/mons.json` (monitor dump, serial
  `SN00000`, sha256 `1ba63e31…`) and `…/home-listing.txt` (12 `/home/someone/…` lines,
  sha256 `d467e8b6…`). Gate: `findings=2` (R3_MONITOR_IDENT=1 R4_HOME_LISTING=1),
  **exit 1**.
- GREEN rev `bf8ea5cbdea1eb53dda24e58085aa3c0626c1777`: diff vs RED is exactly the
  marker pair — two `.synthetic` sidecars (`rules=R3_MONITOR_IDENT` /
  `rules=R4_HOME_LISTING`, sha256 of the target blobs) plus the registry rows in
  `quality/session-material-waivers.txt` (3 files changed, 5 insertions, demo-diff-stat.txt);
  the two target blobs are byte-identical. Gate: `WAIVER … kind=fixture` x2,
  `SESSION_MATERIAL_WAIVED: findings=2 files=2`, `findings=0`, **exit 0**.
- Note (operator-relevant): the marker grammar requires full rule names — a sidecar
  with bare `rules=R3` is correctly refused `marker-malformed` (first demo attempt;
  its output is preserved in receipts/demo-first-attempt-marker-malformed.txt, the
  corrected rerun is the committed demo-green.out).

Receipts: demo-red.out, demo-green.out, demo-diff-stat.txt, demo-red-blob-hashes.txt,
demo-meta.json.

## 4. Restoration evidence

- Scratch working copy restored to pristine bytes after the mutant loop:
  sha256 `82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f` == pristine.
- Lane file `quality/check-session-material.py` re-hashed after everything:
  same sha — never modified.
- SHA256SUMS.txt over all receipts in this seat dir.

## 5. Bounds

No tools installed (none needed; Python 3 stdlib only). No pacman. No subagents. All
runs scratch-confined with hardened HOME/XDG_* env; the gate never ran against the
operator's home state. Scratch dir `/fast/scratch/hyaku/mado-r49/MutGate` deleted after
receipts were copied into the seat dir. Nothing outside `.ufo/waves/round-49/w1/MutGate*`
was written in the lane.

## 6. Feed for the L1 freeze (w2 attack surface)

Highest-value gaps to close in the frozen instruments: (a) R5 regex boundary fixtures
(2-digit prefix / 3-cap / 3-digit tail positives), (b) W4 negative fixtures for home
user, pid band, and description-less monitor identity, (c) assertions on the
`SESSION_MATERIAL_RULES` and `SESSION_MATERIAL_WAIVED files=` lines, (d) a CLI-level
test for `--scope` and `--no-waivers`, (e) a length-4 serial fixture for SERIAL_MIN,
(f) a binary fixture with a NUL beyond offset 8, (g) a registry-sha-mismatch case that
is reachable (marker sha == target sha, registry row stale).
