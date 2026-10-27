# SKILL.md gate-registry row — `mado-session-material` (round-48 v2; replaces `SKILL.md:770`)

Target: `SKILL.md`, table under `### Round 33 — published-axis gate and claim-verdict gate`
(header `SKILL.md:767`, existing row `mado-session-material` at `SKILL.md:770`). Same seven
columns, same cell conventions as `mado-axis-scores` (`SKILL.md:769`).

## The row

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-session-material | gate | `python3 -I quality/check-session-material.py --repo . --rev REV` | 0 clean (`findings=0`); 1 findings (`findings>0`; a waived finding is excluded from the count and counted on its own `SESSION_MATERIAL_WAIVED: findings=<n> files=<n>` line); 2 usage, git error, or a failed/unserialled `hyprctl` read | `python3 -I quality/check-session-material.py --selftest`; prints `SELFTEST: passed=N/N failed=N`; 0 clean, 1 failed | summary line `SESSION_MATERIAL: files=<n> findings=<n> rev=<40 hex>`; rules `R1_CLIENT_DUMP` `R2_PROC_TABLE` `R3_MONITOR_IDENT` `R4_HOME_LISTING` `R5_SERIAL_PROSE` `R6_SERIAL_EXACT`; synthetic marker pair = line 1 of `<path>.synthetic` exactly `SYNTHETIC-MATERIAL v1 kind=<fixture\|gate-copy> rules=<comma list of R1-R4 only> sha256=<64 hex>` **plus** one row `<path> <sha256> <rules> kind=<kind>` in `quality/session-material-waivers.txt`; registry rows at the round-48 install: 48 (47 `fixture`, 1 `gate-copy` for the seat copy of the gate) | reads committed bytes via `git show`/`git cat-file`; selftest writes only inside `$TMPDIR` | mado |

## Notes the integrator needs

- Selftest at the delivered file: **69/69** (`receipts/00-selftest.txt`). It is the round-47
  draft (63 cases, `a4a0a084…`) plus six title-namespace cases that pin the round-47 w2 F1 hole:
  `waiver-title-example-domain-rejected`, `waiver-title-bare-demo-rejected`,
  `waiver-title-probe-prefix-rejected`, `waiver-title-case-only-rejected`,
  `waiver-title-reserved-prefix-waived`, `waiver-title-reserved-exact-waived`.
- The title namespace is **exact and case-sensitive**: `redacted`, `a live window title`,
  `another live window title`, or `synthetic-`/`fixture-`/`selftest-` followed by a mandatory
  delimiter. The draft's bare/`IGNORECASE` alternatives (`example`, `demo`, `probe`) are gone;
  the control receipt shows the draft waiving a dump titled with the IANA reserved example
  domain while the delivered file refuses it (`receipts/10-f1-control-draft-waives.txt`).
  Cost of the tightening at base `579f694`: two round-46 `CritW2Gate` files lose their R1
  waiver and are counted (`receipts/00a-title-sweep.txt`, `00b-title-families.txt`).
- No flag drops a rule: R1-R4 and R5 are always scored, R6 only with `--serial-from-host`;
  `--rules` is an argparse error (selftest `e2e-no-rule-can-be-dropped`).
- Scope: `--scope ufo` (default) or `--scope all`; the registry is always read from the scanned
  revision, never the working tree.
- Registry is a review surface, not a proof: W1 path under `.ufo/waves/` and registry outside
  `.ufo/`; W2 sidecar tracked, grammar exact, sha256 = target blob; W3 registry line repeats
  path/sha/rules/kind; W4a `gate-copy` only for a blob byte-identical to `--gate-source`
  (default `quality/check-session-material.py`); W4b `fixture` only when every matched value is
  in a reserved namespace. Serial rules are structurally outside the waiver surface.
- Install order: (1) `sh .ufo/waves/round-48/w1/ExecSessionMarker/install.sh <lane>` — it writes
  `quality/check-session-material.py`, `quality/session-material-waivers.txt` and the 48
  sidecars at their lane-relative paths, never git; (2) commit that; (3) run the gate at the
  new revision: `SESSION_MATERIAL_WAIVED: findings=49 files=47`, `findings=100` at base
  `579f694` (`receipts/11-verify-install.txt`). Remaining red is real material + stale gate
  copies, listed in the round-48 report §4 — no green is claimed.
- Declared residuals carried unchanged (the marker layer does not touch them): R3 needs a
  non-empty `serial` before description/make/model are examined (a description-only dump reads
  clean); R1 is JSON-object scoped (a title in prose is invisible); blobs are read only over
  their first 16 MiB (docstring now says so); the registry/`--gate-source` paths are
  caller-relocatable via flags, so the pinned SKILL command (defaults only) is the contract.
