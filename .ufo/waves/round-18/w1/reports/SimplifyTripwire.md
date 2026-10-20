# SimplifyTripwire — round 18 / wave 1 (simplifier, leaf)

Target as instructed: `tools/mado-tripwire.py` at **d9a5a18**, read-only.
Blob `22b5175b2bac5693ec4f9995cd53c9763c645ce1`, 935 lines, 37950 bytes,
sha256 `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`
(`git show d9a5a18:tools/mado-tripwire.py | sha256sum`). All line numbers below are
that blob unless a row says otherwise.

**No edits to the lane tool or any lane file except this report.** No subagent dispatch.
No tool installs (nothing was needed). All experiments ran on `/tmp` copies/fixtures.

Concurrent-tree note: while this read was in progress the shared working tree's
`tools/mado-tripwire.py` changed (935 → 1160 lines, sha `593b3aaf…`) — a sibling is
implementing `--frozen` there, uncommitted. §4 is an advisory cross-check of that WIP
against the proposals below; it is not a review of that seat.

## 1. Dead code (deletion candidates)

Each item was deleted in a `/tmp` patch copy and the result diffed against the original
over 88 selftest cases, 149 lane transcripts and a 4000-record fuzz corpus: byte-identical
(stdout + exit) everywhere. Static reasons are given because the suites already pass, so
they cannot discriminate an inert branch. No `lsp` device or language server is mounted in
this seat's toolset, so semantic-reference evidence is AST def/use plus exhaustive textual
occurrence counts (recorded per row), not server `references`.

| id | lines (d9a5a18) | what | why dead (proof) | delta |
|----|-----------------|------|------------------|-------|
| D1 | 220, 224 | `in_single` in `substitutions()` | only two textual occurrences: `in_single = False` and `and not in_single`. It is never assigned `True`, so the test is constant-true. Delete 220; L224 becomes `if ch == "'":`. | −1 line, −40 B |
| D2 | 204 | `or tok == "\n"` in `segments()` | `"\n"` is already a member of `SEPARATORS` (L49); the disjunct is a duplicate of `tok in SEPARATORS`. | −15 B |
| D3 | 611, 623-624, 634-635 | `from_subprocess` set + second `is_sub` disjunct | every key added to `from_subprocess` at 623-624 is added to `aliases` with the *same* expression (`a.asname or a.name`) at 622; 631-632 then rewrites any such name to `<module>.<name>`, so at 635 `name == tail` can never hold for a `from_subprocess` member. The disjunct is unreachable and the set exists only for it. Replace 634-635 with `is_sub = name.startswith("subprocess.") and tail in SPAWN_FUNCS`. | −4 lines |
| D4 | 78 | `"systemd-run", "su"` in `HOST_MUTATION_BINS` | both are shadowed by dedicated branches that `return` before the set test at L549: `su` 474-478, `systemd-run` 479-488. Removing them is rule-string-identical (same argv0 rule) and keeps the `su -c` / `systemd-run` payload recursion. | −21 B |
| D5 | 48 | `"function"` in `KEYWORDS` | inert: `function f { … }` strips `function`, then stops at the name `f`; without the token, argv0 is `function`. Probe: `function f { sudo pacman -Syu; }` yields **no** finding either way; `f() { … }` and `{ … }` do yield one. Delete the token, but do not read this as support for the construct — the miss is a real classifier gap and out of scope here. | −12 B |

Measured aggregate of D1-D4 + T4 below: **935 → 920 lines, 37950 → 36536 bytes
(−15 lines, −1414 B)**; diff hunks `-31/+16`.

## 2. Duplicate rule tables / duplicated logic

| id | lines | duplication | proposal |
|----|-------|-------------|----------|
| T1 | 44-45, 51-53, 60-61, 71, 484, 527-528 | six "option consumes its argument" tables, three of them feeding the *same* `first_verb()` helper: `SYSTEMCTL_ARG_OPTS`, `HYPRCTL_ARG_OPTS` and a literal set inlined at the `loginctl` branch. `systemd-run` (484) and `sudo` (464-470) carry the same eat-option-then-recurse loop shape by hand. | one `VERB_ARG_OPTS = {"systemctl": …, "loginctl": …, "hyprctl": …}` used as `first_verb(args, VERB_ARG_OPTS[argv0])`. No behavior change (lookup-only). Optional helper for the two recurse loops (`command_after_options(args, opts, stop_at_ddash=…)`); low value, only if touched. |
| T2 | 433-435 vs 489-494 | shell `-c` payload detection written twice, once negated (here-doc fed to an interactive shell) and once positive (inline `-c`). | `shell_c_payload(args)` returning index/payload; `fed_to_shell = base in SHELLS and shell_c_payload(s[1:]) is None`; the `SHELLS` branch classifies the payload. −3/−4 lines, one convention. |
| T3 | 436 vs 498 | `re.fullmatch(r"python[0-9.]*", …)` twice. | module-level `PYTHON_RE = re.compile(r"python[0-9.]*")`; `.fullmatch`. Neutral; do only with T2. |
| T4 | 822-825, 898-901, 910-913, 916-919, 931-934 | **five** copies of the `could_not_evaluate` payload (same schema, `files: []`, `findings: []`, `counts: {c: 0 for c in CLASSES}`, `permitted`, `unpermitted: 0`) — four via `emit`, one hand-rolled `print` in the top-level `BaseException` handler. | `def failure(error, permitted=())` beside `emit` (insert after 815); each site becomes one line, including `emit("could_not_evaluate", failure("internal %s" % type(exc).__name__))`. `sorted(())` keeps the JSON byte-identical (verified on 8 CLI paths incl. usage, unknown permit, no path, missing file, symlink-free dir). |
| T5 | 827-828 | the only copy of the verdict tri-state today — but the in-flight frozen code has already copied it (see §4). | extract `verdict_of(findings, unpermitted) -> (code, label)` **now**, before the copy ossifies into a second authority. This is the one duplicate that is not yet duplicated in d9a5a18 and therefore cheapest to prevent. |
| T6 | 813-815 vs in-flight 878-879 | `emit` prints `MADO_TRIPWIRE: label` + sorted JSON; `emit_frozen` re-prints the same JSON line by hand. | `emit(label, payload, prefix="MADO_TRIPWIRE")`; frozen calls it with `prefix="MADO_TRIPWIRE_FROZEN"`. Optional (2 lines), but it keeps one serialization convention. |

Not proposed (look dead, are load-bearing): `classify_pacman` tail at 412 (fail-closed for
unknown upper-case ops, reachable via e.g. `pacman -Z`); `REFUSED_NAMES` (92, 691) covering
`agent.db.jsonl`; `HYPRCTL_MUTATE`'s `hyprpaper`/`hyprsunset` (hyprctl keywords) versus the
same names in `LIVE_PROBE_BINS` (binaries) — different domains; `dq_before` in
`substitutions()` (approximate but decides the single-quote skip).

## 3. What `--frozen` should reuse (and must not)

Reuse:

| id | seam | why |
|----|------|-----|
| U1 | `scan_file(path)` 729-798 | one call gives read + sha256 + line-level findings (`file`,`line`,`class`,`rule`,`tool_call_id`) with the per-line `(class, rule)` dedup at 785-790 and `NESTED` accounting. This is the right seam for frozen (not `scan()`): frozen has already validated the input list and needs its own `file` form. |
| U2 | verdict rule 827-828 | `verdict_of()` must produce frozen's `scan_exit`/`scan_label`; otherwise the two definitions of "clean/permitted_only/findings" can drift and frozen will compare against its own re-invention. |
| U3 | `tool_sha256` (from 887 + `abspath` at 848) | frozen's `tool_sha256` is the same quantity the selftest prints; one helper, and it also closes the unclosed file handle at 887. |
| U4 | `reject_constant` 725-726 | pass as `parse_constant=` when loading frozen `expected.json`: NaN/Infinity become a `ValueError` → `frozen_error`, same rule the JSONL reader uses. |
| U5 | selftest case loop 849-886 | extend with `mode`; the current block requires `case["want_findings"]` (856), so a frozen case needs either a branch that skips it (the spec says want_findings is ignored in frozen mode) or `.get("want_findings", [])`. Also the first-line prefix checks at 873/876 are scan-specific and need the frozen prefix. |
| U6 | `CLASSES` 41 + permit subset test 909 | frozen's `expected.json` permit validation needs the same class vocabulary and subset rule. **Caveat:** 909 also rejects an *empty* permit (`not permit`), which is legal in a frozen spec; reuse only the `permit <= set(CLASSES)` half. |

Must not reuse:

| id | code | reason |
|----|------|--------|
| N1 | `run_scan` 818-832 | it *prints* a scan verdict. Frozen needs the numbers without the scan output; call `scan_file`/`verdict_of` instead. |
| N2 | `discover` 696-722 | raises scan-flavored `CouldNotEvaluate`, dedups by realpath, requires every argument to be `.jsonl`, and cannot express "any `*.jsonl` under `DIR/inputs` not listed". Frozen's own sorted walk is correct and must stay. |
| N3 | `refuse_path` 678-693 | raises free-text exceptions; frozen must distinguish `frozen_error`/`snapshot_tampered`/`unpinned_legacy` with a fixed precedence (absolute/`..`/symlink/missing/non-regular → tampered *before* any read; missing `sha256` → `unpinned_legacy`). Reusing this forces message-string matching. Keep the 6-line lstat check. |

Two traps that reuse decisions hinge on:

- **X1 path form.** Findings carry `"file": path` exactly as passed (792). `expected_findings`
  use `inputs/<name>.jsonl`, so frozen must report the pinned relative form; the
  `scan_file` loop with `f["file"] = e["path"]` is equivalent, whereas a `scan()`-based
  frozen would have to `relpath`. Verified: the same file yields
  `/tmp/…/fuzz/f2.jsonl` vs `fuzz/f2.jsonl` depending on the argument.
- **X2 duplicate input entries.** `scan_file` in a loop scans `inputs/a.jsonl` and
  `inputs/./a.jsonl` twice → findings doubled while `expected_findings` lists them once.
  `scan()` would collapse them via `discover`'s realpath dedup. Frozen should `normpath`
  and reject duplicate resolved entries as `frozen_error` (malformed spec); the in-flight
  code normalizes only for the listed-set comparison, not for the scan loop.

One interface question for L1 (not a defect claim): if `scan_file` raises
`CouldNotEvaluate` on a digest-valid input (e.g. an invalid JSONL line), `scan_exit` is 2
while `expected_exit` is 0|1, so the stated comparison yields a mismatch. `frozen_error` is
described only for `expected.json` problems. Recommendation: `frozen_verdict_mismatch`,
exit 1, `scan_exit: 2`, `scan_label: "could_not_evaluate"` (consistent with the scan CLI's
label vocabulary) — but the interface owner should rule.

## 4. Cross-check: in-flight tree at 593b3aaf… (advisory, line numbers drift)

- U1 done: `run_frozen` calls `scan_file` per input (1001) and normalizes `f["file"]`
  (1008). Good — keep.
- U3 done (`tool_sha256` 850-856), U4 done (979), U5 done (mode branch 1054-1085),
  U6 done (896-900, and empty permit correctly allowed).
- **U2 not done:** the tri-state is now duplicated at 836-837 and 1010-1013, and the
  `unpermitted` sum at 809 is copied at 1010. Extract `verdict_of()` + a `tally()` (or a
  three-line shim) so `scan` and `frozen` cannot disagree; this is the highest-value
  remaining simplification.
- **T4 not done:** five payload copies still present (833, 1125, 1137, 1143, 1158).
- T6 not done (`emit_frozen` prints its own JSON line at 878-879).
- D1-D5 all still present in the in-flight tree: 87 (`systemd-run`,`su`), 213 (`tok == "\n"`),
  229/233 (`in_single`), 620/633/643-644 (`from_subprocess`), 48 (`function`).
- N2/N3 honored by the WIP (its own walk 943-955, its own lstat 935-942); X1 honored.

## 5. Evidence ledger

All commands read-only against the lane; scratch under `/tmp/r18-simplify`.

1. Identity: `git show d9a5a18:tools/mado-tripwire.py | sha256sum` = `962919ce…`; `wc -l` = 935.
2. Suites, original vs patched (patch = D1-D4 + T4): core 9/9, compound 16/16,
   hardening 33/33, w2-regressions 30/30 — **88/88 both**, `failed=[]`.
3. Differential over every `.jsonl` under `.ufo` (149 files, growing during the run):
   stdout+exit identical, **drift=0**.
4. Fuzz: 4000 synthetic transcript records (2346 bash, 1264 eval; 1724 findings:
   1021 host_mutation / 489 live_probe / 214 package_query; 123 `from subprocess import`
   and 121 `as sp` sites, so the deleted alias disjunct is exercised) — verdicts
   **byte-identical**; 7-case targeted eval file (`from subprocess import run`,
   `sp.run`, `os.system`, `from os import system`, `subprocess.getoutput`, `!` magic)
   byte-identical, findings `sudo`, `pacman:-Syu`, `walker`, `hyprctl:dispatch`,
   `systemctl:restart`, `expac`.
5. Error paths: 8 CLI invocations (no args, `--scan` bare, missing file, dir, two permit
   forms, unknown permit, explicit file) identical stdout/stderr/exit.
6. Reuse seam (module import of the d9a5a18 blob): `scan()`/`scan_file()` label+code and
   findings multiset equal the CLI verdict; `entries[].sha256` equals `sha256sum`.
7. Lane integrity: the d9a5a18 dump stayed `962919ce…` throughout; the only lane write is
   this report. The working-tree change to `tools/mado-tripwire.py` came from a sibling.

## 6. Limits, tradeoff, stop point

- The deleted branches are proven unreachable/inert statically; the behavioral checks show
  no case in the sampled corpus distinguishes them. Recall parity beyond that corpus is
  asserted only by construction, not by exhaustive proof.
- The fuzz alphabet is synthetic and biased toward the constructs under test; it does not
  substitute for real transcripts, though 149 real ones were run.
- No frozen snapshot directory existed at read time (`.ufo/waves/round-18/frozen-tripwire`
  absent), so §3's frozen consequences are design-level, not integration-tested; §4 is a
  moving target.
- Tradeoff of T4/T5: one indirection (`failure()`, `verdict_of()`) in exchange for one
  authority per verdict and per predicate. Skip T1/T2/T3 if the file is not otherwise
  touched — they are convention hygiene, not weight.
- **Stop point:** after D1-D5 and T4/T5 there is no further behavior-neutral deletion. The
  remaining candidates are defense-in-depth (fail-closed pacman tail, `REFUSED_NAMES`,
  keyword/binary table overlap, the `dq_before` approximation); deleting any of them would
  remove a deliberate limit or change recall, which harms correctness more than the byte
  count helps.
