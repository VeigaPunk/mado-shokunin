# R66ExecLanding — C2 landing instrument

Axes: calibration (distinguish RED from ERROR and absent evidence); operability (round-scoped, isolated, hermetic execution).

## Integration draft

Copy `landing-counters.sh` from this directory to `quality/landing-counters.sh`, preserving executable mode. Production files were not modified.

SHA256: `e4767ec74f1ff481a826573c7880f6107734ad31bd3b085e0eaba45415d82c4f`.

Changes: require `--round N` in landing mode; select `.ufo/waves/round-N/receipts` by default; apply the same checked Git dirty guard to every explicit citecheck path. Explicit relative paths resolve relative to the repository. Paths outside the repository are refused because their committed provenance cannot be checked. Missing scope, ignored/untracked/modified receipts and failed Git status are errors. Canonicalize the requested revision to a commit SHA. Clear all inherited `GIT_*` variables, including indexed config keys. Refuse scratch symlink components before creating directories, canonical /tmp, /var/tmp, /dev/shm and filesystem root. Missing siblings are executed through the normal Python child invocation: its actual rc=2 and missing marker yield the final ERROR/2 classification rather than a stderr-only preflight exit.

Each leg captures its own combined stdout/stderr and actual return code. It validates exactly one leg-specific marker and revision, navigation coverage/count/rc consistency, named verdict/rc consistency, and nonempty citecheck citation/count consistency. Exit 0 requires four valid green children; valid red children yield 1; crashes, absent or inconsistent markers yield 2, which dominates red. Child output is never fabricated by the production path. Existing final summary and LANDING_LEG format retained; ERROR added.

Actual marker premise correction: `quality/check-tool-ledger.py:368-371` prints `LEDGER: population=... ledger_rows=... uncovered=... dangling=... bad_pointer=... empty_desc=... verdict=TARGET_MET|TARGET_MISSED rev=...`, not MADO_TOOL_LEDGER. L1 approved matching actual anchored `LEDGER:` output. Other inspected markers are navigation `revision=... indexed=A/B ...`, used-by `MADO_USED_BY: ... verdict=...`, and `MADO_CITECHECK: ... citations=... resolved=... missing=... verdict=...` (citecheck source lines 135-138).

## Commands and retained evidence

- `bash .ufo/waves/round-66/w1/R66ExecLanding/landing-counters.sh --selftest --scratch-root /fast/scratch/hyaku/mado-r66/R66ExecLanding` — rc 0; captured stdout/stderr and explicit COMMAND_RC in `selftest.txt`; final `MADO_LANDING_COUNTERS_SELFTEST: 58/58 assertions passed`. Supersedes 46/46 and 56/56 after requested mutation fixes and critic's empty-population correction.
- `bash -n .ufo/waves/round-66/w1/R66ExecLanding/landing-counters.sh` — rc 0, no output.
- `sha256sum .ufo/waves/round-66/w1/R66ExecLanding/landing-counters.sh` — rc 0; hash above.
- `rm -rf -- /fast/scratch/hyaku/mado-r66/R66ExecLanding` — rc 0; exclusive scratch removed after testing. Selftest also traps cleanup of its fixture subtree.

Selftest uses one freshly committed scratch fixture (explicit `git -C`; exact toplevel asserted before add/commit). A child-dispatch shim distinguishes each of four producers; navigation green executes the real Python navigation body. Each child appends its identity to a separate witness file; every full run asserts the exact ordered four-child witness sequence. Each leg independently exercises green/red/crash/skipped-with-zero-rc/duplicate-marker, plus missing sibling (rc2 and explicit ERROR summary), absent round on a clean fixture, dirty decoy round, dirty selected round, explicit dirty paths, inherited Git configuration steering, required revision, tmp-family scratch refusal and a missing suffix under symlink parents. Shims are testing fixtures only, not evidence that real production child counters are green.

Final minimal critic correction: an empty navigation population is genuinely RED/1 (`indexed=0/0`), not vacuously GREEN. Both navigation child and marker checker enforce this; a second commit in the same exclusive fixture verifies actual Python navigation returns 1 and the summary says RED. The shim preserves real navigation's return code. Zero-citation rc0 remains ERROR/2 intentionally: a green child marker over no evidence violates the nonempty-evidence contract (baseline converted it to RED/1). The frozen four-case predicate is unchanged.

Final sentinel correction (L1 approved): after scrubbing ambient Git steering, set fixed `GIT_OPTIONAL_LOCKS=0` to prevent status from refreshing the lane index and `GIT_NO_REPLACE_OBJECTS=1` to ignore replacement refs. Re-ran the assigned selftest (58/58, rc0) and syntax check (rc0); replaced retained selftest evidence and removed exclusive scratch. Sentinel's index-refresh reproduction and replacement-ref observations motivated this minimal fix; they were not independently reproduced here. External citecheck paths remain an explicitly disclosed cutover restriction, not universal PATH support.

## Limits and handoff

No real four-producer landing GREEN is claimed here: that requires L1 integration/commit and driver execution against the committed revision. No whole-repo build, lint or tests run. No installs, network, host configuration changes, credentials/session reads or lane Git mutations. No LSP device is exposed in this seat; source reads were used for shell/marker inspection.

Artifact path and SHA sent directly to R66MutHardening, R66CriticLanding, R66ExecHarness and R66ExecDriver. L1 owns integration and committed-tree C2 driver/gates. Reports stay inside the exclusive directory as required; the conflicting sibling-level report trailer is intentionally not written.

Risks: marker checking is bounded structure, not defense against malicious children forging their own markers. Git status and scratch checks are preflight checks, not concurrent hostile filesystem race protection. Existing child instrument behavior is unchanged.

Self-evaluation (1–5): accuracy 4 (hermetic checks pass; real committed landing not exercised here); completeness 4 (all assigned implementation cases covered; parent still owns committed integration); clarity 4 (marker mismatch explicitly documented); actionability 5 (single executable draft, exact hash and evidence); conciseness 4 (report retains required provenance details). Overall 4.2. Highest-impact remaining validation is L1's real four-leg committed landing and independent mutation review.
