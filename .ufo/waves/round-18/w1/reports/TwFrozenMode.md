# TwFrozenMode — `--frozen DIR` digest-pinned replay

Seat: MadoR18.TwFrozenMode (executor, leaf). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. No git/jj write, no host command,
no tool install performed.

## Files changed

| path | change | sha256 | lines |
|---|---|---|---|
| `tools/mado-tripwire.py` | +256 / −10 (sole writer this wave) | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | 1181 |

Baseline at start of seat: `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`, 935 lines.
`git diff --stat` (read-only) is confined to that one file; `git status` shows only `M tools/mado-tripwire.py`.
Nothing under `.ufo/waves/round-18/frozen-tripwire/` was written by this seat.

Added: `from collections import Counter`; a frozen section
(`FROZEN_SCHEMA`, `FROZEN_LABELS`, `tool_sha256`, `emit_frozen`,
`frozen_error`, `validate_frozen`, `frozen_snapshot`, `run_frozen`);
`--frozen DIR` dispatch and usage line; frozen mode in `run_selftest`;
mode-aware internal-error handler; docstring CLI/exit/limit lines.
No classifier, `scan`, `scan_file`, `discover`, `refuse_path` or `emit` line was
edited — every removed line is docstring, usage, or the restructured selftest
case-parse block (verified by `git diff`, 10 removed lines total).

## Behavior as implemented

Outcomes / exits (first line `MADO_TRIPWIRE_FROZEN: <outcome>`, then one sorted
JSON line with schema `mado-tripwire-frozen-verdict-v1`):

| order | condition | outcome | exit |
|---|---|---|---|
| 1 | `expected.json` unreadable, not JSON, not an object, missing key, bad type, wrong schema, unknown permit class, bad `expected_exit`/`expected_label`/`expected_findings`/`known_misses` entry, non-string `sha256` | `frozen_error` | 2 |
| 2 | input path absolute / contains `..` / symlink / missing / non-regular; unlisted `*.jsonl` (recursive) under `DIR/inputs`; unreadable `inputs` dir | `snapshot_tampered` | 2 |
| 3 | an input entry without `sha256` | `unpinned_legacy` | 2 |
| 4 | digest mismatch (or bytes changed between verify and scan) | `snapshot_tampered` | 2 |
| 5 | scan exit, label, exact multiset of (file,line,class,rule), and `known_misses` all reproduce | `frozen_match` | 0 |
| 6 | any of the above differ, including a finding on a known-miss line | `frozen_verdict_mismatch` | 1 |

Payload keys: `schema, outcome, exit, tool_sha256 (sha256 of the running file),
expected_sha256 (sha256 of expected.json bytes), inputs[{path,sha256,ok}],
missing_findings, extra_findings, scan_exit, scan_label`; non-verdict outcomes add
`error`. `inputs[].ok` is per-entry and means *this input itself* is a listed,
non-symlink regular file whose bytes digest-match its pin; it is computed even
when a sibling entry fails, so a tampered verdict still shows which bytes were
verified. Findings are scanned with `scan_file` in listed order (no dedup/merge),
finding `file` is rewritten to the listed relative path, and `permit` comes only
from `expected.json`.

Selftest: a case with `"mode": "frozen"` self-invokes
`--frozen <DIR>/<args[0]>` and compares exit and the first-line outcome;
`want_findings` is ignored in that mode; a missing `want_label` or unknown mode
is `SELFTEST_SUMMARY: malformed case` exit 2 (pre-existing wording). `--frozen`
itself requires exactly one argument and accepts no `--permit`. An internal
exception under `--frozen` is emitted as `frozen_error` / `internal <Type>` exit
2, so the first line never degrades to the scanner shape.

## Retained evidence

Four round-17 suites, all green at the final sha (printed
`SELFTEST_SCRIPT_SHA256: c87a31ef…`), each run as
`python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/<suite>`:

- core 9/9, compound 16/16, hardening 33/33, w2-regressions 30/30
  (baseline before edits was the same 9/16/33/30).

Landed round-18 snapshot (owned by MadoR18.TwFrozenSnapshot), run read-only:

```
MADO_TRIPWIRE_FROZEN: frozen_match   rc=0
expected_sha256 4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9
tool_sha256     c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb
scan_exit 1  scan_label findings  inputs 5/5 ok  missing [] extra []
```
The snapshot pins 8 findings (6 host_mutation, 1 package_query, 1 live_probe) and
3 `known_misses`; the match means all 8 reproduce and all 3 asserted misses stay
quiet. Their findings were derived from receipts, not by running this tool, so
the match is an independent classifier agreement, not a tautology.

`/tmp/rt18-frozen` matrix (32 directories, all asserted; none under the lane's
round-18 tree): `clean-match, findings-match, permitted-match, empty,
known-miss-clean, upper-pin` → `frozen_match` 0; `mismatch-label, mismatch-exit,
mismatch-missing, mismatch-extra, known-miss-hit, contradiction` →
`frozen_verdict_mismatch` 1; `tamper-digest, tamper-unlisted, tamper-missing,
tamper-symlink, tamper-abs, tamper-dotdot, deep-unlisted, dir-input,
priority-path` → `snapshot_tampered` 2; `unpinned, priority-unpinned` →
`unpinned_legacy` 2; `err-json, err-missing-key, err-badtype-exit, err-schema,
err-no-file, err-permit, err-entry, err-sha-type, internal-recursion` →
`frozen_error` 2. Additional assertions: relative path, trailing slash,
uppercase digest accepted; digest-mismatch + unpinned resolves to
`unpinned_legacy` (spec order); unlisted file beats unpinned; two-entry tamper
reports `[ok True, ok False]`; classifier parity — the frozen scan's
(file,line,class,rule) multiset equals plain `--scan` on the same bytes
(`pacman -S foo` → host_mutation `pacman:-S`, `journalctl -b` → live_probe
`journalctl`); `--frozen` with no DIR → `MADO_TRIPWIRE: could_not_evaluate` 2
with usage on stderr.

Selftest-mode fixture `/tmp/rt18-frozen/suite` (mixed): 4/4 — two frozen cases
(match and mismatch), one tamper case, one ordinary scan case. A deliberately
wrong `want_label` yields `0/1 … failed=['wrong-label']` exit 1; a frozen case
without `want_label` and a case with `"mode": "frob"` both yield exit 2
malformed.

## Decisions that could not be inferred from the contract

- The unlisted-file check matches suffix `.jsonl` exactly (case-sensitive) and
  is recursive under `DIR/inputs`; a symlinked `inputs/` directory is followed.
  A listed input outside `inputs/` is accepted if it is relative, non-symlink and
  regular (the contract constrains paths, not their parent).
- An empty `inputs` list is accepted (type-valid) and yields a verdict over no
  files rather than a spec error.
- Listing the same file twice is not rejected: it is scanned twice, so the pin
  must carry each finding twice. Documented here as a footgun, not guarded.
- `expected_findings[].file` must equal the `inputs[].path` string verbatim
  (e.g. `inputs/r13-root.jsonl`), because released verdicts carry the listed
  string; a different but equivalent spelling is an honest mismatch.
- The snapshot is re-hashed during the scan and a mid-run change is
  `snapshot_tampered`; provenance fidelity (that the lines really came from the
  named transcript) is not checked — stated in the module docstring, since only
  `provenance.json`'s author can attest it.

## Risks / blockers

- None blocking. By design any future classifier change requires re-pinning
  `expected.json`; that is what makes the registry row a gate, not a probe.
- Moving the tripwire registry row probe → gate and citing this tool sha in the
  capability receipt is L1's edit (not made here).
