# RevengeTwSpec — tripwire selftest harness & expected.json, as implemented

Scope: `run_selftest` in `tools/mado-tripwire.py`, the `mado-tripwire-selftest-v1`
schema it actually enforces, and the `mode: "frozen"` extension that has landed in
the same file while this seat worked. Method: source read plus black-box probes of
the harness on throwaway `/tmp/twh` fixtures; every result below is an observed run
unless marked `[INFERENCE]`.

Two revision stamps because the tool moved under this seat:

- **A = committed** `tools/mado-tripwire.py` sha256 `962919ce…d5aaa072` (935 lines),
  the sha every round-17 receipt names, clean at HEAD `d3a0000` /
  `refs/heads/master`. A's harness is scan-only.
- **B = working tree** sha256 `c87a31ef…d59b4bb` (1181 lines, `git status` = `M`,
  uncommitted). B was `593b3aaf…` (1160 lines) when probes S1-S8 first ran and
  `3e791ee…` partway through; the `run_selftest` body is semantically identical in
  all three B stamps (only line numbers and the `run_frozen` helper grew). Suite
  counts below were re-run at `c87a31ef`, and line numbers are a snapshot at that
  sha — **symbol names are the durable citation**.

## 1. Verdict

The harness is a **black-box re-executor**, not an in-process checker: for every
case it spawns `sys.executable -I <abspath(this file)> …`, parses **stdout line 1
(label) and line 2 (JSON verdict) only**, and compares a hand-built tuple multiset.
It never imports the classifier, never checks the verdict schema/`exit`/`files`/
`counts`, and never pins the tool under test. `expected.json` is a tuple-multiset
assertion file with three optional extras (`want_label`, `want_error_contains`,
`want_ids`) and one mode switch.

B's `mode: "frozen"` branch is correct on the points that could produce a **false
pass**: unknown modes fail closed, `want_label` is mandatory, `want_findings` is
neither required nor compared, and the frozen prefix is disjoint from the scan one.
Two residual weaknesses remain (`D1`, `D2` below); both fail closed.

## 2. Control flow (B; A is identical minus the mode branch and the IndexError catch)

`run_selftest(directory)`:

1. `open(directory/expected.json)` → `json.load`; then `spec["cases"]`, then
   `assert spec.get("schema") == "mado-tripwire-selftest-v1"`, then
   `assert isinstance(cases, list) and cases`. Any of
   `OSError, ValueError, KeyError, AssertionError, TypeError` ⇒
   `SELFTEST_SUMMARY: 0/0 malformed expected.json (<ExcType>)`, exit 2, and no
   `SELFTEST_SCRIPT_SHA256` line. Order matters: `cases` is read before the schema
   assert, so a frozen snapshot's own `expected.json` dies as `(KeyError)`.
2. Per case: `me = os.path.abspath(__file__)`; a `try` extracts `name`,
   `mode = case.get("mode","scan")`, builds `argv`, and pulls `want_exit` (plus
   `want_label` for frozen, `want_findings` for scan).
   `except (KeyError, TypeError, IndexError)` ⇒ `SELFTEST_SUMMARY: malformed case`,
   exit 2, **aborting all later cases** (no sha/summary-count line printed).
3. `subprocess.run(argv, capture_output=True, text=True, timeout=120)`;
   `out = proc.stdout.split("\n")`; `got_exit = proc.returncode`.
4. Frozen branch (`if mode == "frozen"` after the spawn): exact
   `out[0] == "MADO_TRIPWIRE_FROZEN: " + want_label` and `rc == want_exit`, then
   `continue` — line 2 is never parsed.
5. Scan branch: `json.loads(out[1])` (`None` on `IndexError/ValueError`), tuple
   compare, then optional label/error/ids checks.
6. After the loop: `SELFTEST_SCRIPT_SHA256: <sha of this file>` then
   `SELFTEST_SUMMARY: p/n passed failed=[...]`; exit **0 iff `failed` empty, else
   1**; the malformed paths are the only exit-2 returns.

Anchor line map at `c87a31ef`: `def run_selftest` 1057, frozen argv 1073-1077,
`except (KeyError, TypeError, IndexError)` 1087, post-spawn frozen branch 1093-1103,
`use_file` 1108, `key()` 1109, `first_ok` 1114, sha/summary prints 1128-1129.

## 3. Comparison semantics — what is and is not checked

Yes:

| facet | how |
|---|---|
| process exit | `proc.returncode == want_exit`, exact int (string `"1"` fails — probe E9) |
| line 1 (scan) | must `startswith("MADO_TRIPWIRE: ")`; `want_label`, if present, must equal the whole line `MADO_TRIPWIRE: <label>` (trailing space fails — P6) |
| line 1 (frozen) | must equal `MADO_TRIPWIRE_FROZEN: <want_label>` exactly; `want_label` required |
| findings | exact sorted multiset of `(class, rule, line, filepart)`; no subset or duplicate tolerance (E11 duplicate want fails; E11b one-of-two want fails) |
| filepart (scan only) | `""` unless **any** want entry carries `"file"`; then `basename(actual)` vs the want `file` string **verbatim** |
| `want_ids` (scan) | `[finding["tool_call_id"] …]` == list, in emission order |
| `want_error_contains` (scan) | substring of `str(verdict.get("error",""))`; empty string is vacuously true (P5) |
| line 2 | only `json.loads` success, and only on the scan branch |

No: `verdict["schema"]`, `verdict["exit"]` vs rc, `files` (paths, count, sha),
`counts`, `permitted`, `unpermitted`, finding `timestamp`/`argv0`/`command`, the
frozen verdict body (`tool_sha256`, `expected_sha256`, `inputs`,
`missing_findings`, `extra_findings`, `scan_exit`, `scan_label`),
`provenance.json`, and the identity of the tool under test. A case passes if the
child prints the right two lines and exits right — any tool producing that
behavior passes.

## 4. expected.json as implemented

```
{"schema": "mado-tripwire-selftest-v1",
 "cases": [ {                      # non-empty list, required
   "name": …any,                   # required; %s-formatted into CASE lines
   "args": ["…", …],               # required; each os.path.join(DIR, a)
   "want_exit": 0|1|2,             # required; int only
   "want_findings": [              # required for scan; NOT read for frozen
     {"class": s, "rule": s, "line": int, "file"?: s}],
   "permit"?: ["host_mutation"|"package_query"|"live_probe", …],
   "want_label"?: s,               # scan: label; frozen: REQUIRED outcome
   "want_error_contains"?: s,      # scan only
   "want_ids"?: [s, …],            # scan only
   "mode"?: "scan"|"frozen"        # absent ⇒ scan; anything else ⇒ malformed case
 } ]}
```

Observed facts not apparent from the shape:

- `args` entries are **joined to the suite DIR**; `os.path.join(DIR, "/abs")`
  returns `/abs`, and `"../x"` traverses out — no confinement (E6, S8). Same for a
  frozen case's `args`; the frozen runtime then applies its own relative-input
  checks to the *listed inputs*, not to DIR.
- `args: []` is legal and makes the child exit 2 `no path`; a case
  `{"args": [], "want_exit": 2, "want_findings": []}` **passes without scanning
  anything** (E10), and `"want_error_contains": ""` makes it fully vacuous (P5).
  A frozen case with `args: []` is a malformed case (`args[0]` → `IndexError`,
  caught at the per-case `except`).
- `permit` is passed through verbatim after the paths; the harness validates
  neither class names nor types. A string `"host_mutation"` becomes
  `--permit h o s t …` → child exit 2 `unknown permit class` (E13), so a typo is
  only visible when the case does not itself expect exit 2. `permit: []` is falsy
  and omitted, same as no permit (E14).
- Extra top-level keys (`note`, `convention`) and extra case keys are ignored; all
  four committed suites use `note`.
- Case names are not unique-checked (F5: two `same` cases both run and pass), and
  extra `*.jsonl` files in DIR are neither discovered nor rejected (F6).
- `want_findings` entries must be dicts with `class`/`rule`/`line`; a list/dict
  entry raises `TypeError` **outside** the per-case `try` (P2, E3) → escapes to the
  `__main__` `BaseException` handler, which prints `MADO_TRIPWIRE:
  could_not_evaluate` + a **scan-shaped** `mado-tripwire-verdict-v1` JSON and exits
  2 — a selftest invocation emits a scan verdict and no `SELFTEST_SUMMARY`.
  Fail-closed, but outside the harness's stated failure modes.
- A non-dict case (string/null/list) **is** caught as `malformed case`, because
  `case["name"]` is evaluated before `case.get` (probe5).
- The selftest spec is read with plain `json.load` (no `parse_constant` hook), so
  `NaN`/`Infinity` are accepted in `expected.json`; the scan/frozen runtimes reject
  non-standard constants in their own inputs.

## 5. Basename keying: the sharpest quirk

`use_file = any("file" in w for w in want)` (B:1108) is **per case**; `key()`
(B:1109) then uses `basename(actual["file"])` but the want value **raw**:

- One want entry with `"file"` flips the whole case to file-keyed mode; the other
  entries contribute filepart `""` and can never match (E2).
- A want `file` must be a bare basename: `"sub/p.jsonl"` compares unequal to
  `basename("sub/p.jsonl") == "p.jsonl"` (E1). The committed `compound` suite obeys
  this (`"file": "compound-and.jsonl"`). A frozen snapshot's
  `expected_findings.file` uses the *listed path* (`inputs/x.jsonl`) and must not be
  copied wholesale into a scan case's want under this harness.
- Because actual is basenamed, two scanned files with the same basename are
  indistinguishable: four findings from `dup/a/d.jsonl` + `dup/b/d.jsonl` are
  satisfied by 2×sudo + 2×pacman under `d.jsonl` (F1 pass), with no per-file
  attribution. Fine for the intended single-file convention; do not "fix" it
  without re-cutting receipts.
- With `use_file` false, file identity is ignored entirely (E0) — what one `core`
  case, every `hardening` case and every `w2-regressions` case rely on.

## 6. Failure-mode catalogue (observed)

| mode | trigger | stdout tail | exit |
|---|---|---|---|
| malformed spec | not a dict / no `cases` / empty / wrong schema / unreadable | `SELFTEST_SUMMARY: 0/0 malformed expected.json (<Exc>)`; no sha line | 2 |
| malformed case | missing `name`/`args`/`want_exit`/`want_findings` (scan), `want_label`/`args[0]` (frozen), unknown `mode`, non-str arg | `SELFTEST_SUMMARY: malformed case`; loop aborted; no sha/summary count | 2 |
| case fail | any compare mismatch | `CASE <name> FAIL want=<tuple> got=<tuple>`; loop continues | 1 at end |
| harness crash | non-dict want entry, non-str `want_label`, homogeneous-type-violating want list, child >120 s | `MADO_TRIPWIRE: could_not_evaluate` + verdict-v1 JSON (scan-shaped), no summary | 2 |
| pass | all cases ok | per-case `CASE <name> ok`, then sha, then `N/N passed failed=[]` | 0 |

Diagnostic weakness: a scan `want_label` failure prints `want=(exit, findings)` and
`got=(exit, findings)` with the labels omitted, so the failing comparison is
invisible (P6). Frozen failures do print both full first lines (B:1101-1102).

## 7. `mode: "frozen"` — what the extension must not break

Regression contract: `round-17/tripwire/core` 9/9, `compound` 16/16, `hardening`
33/33, `w2-regressions` 30/30 — verified all-pass at A and again at B `c87a31ef`,
alongside B's `.ufo/waves/round-18/tripwire/frozen` suite 17/17. That suite's cases
carry a dummy `"want_findings": []`, which is harmless and keeps the suite valid if
a future harness re-imposes the scan key requirement.

Invariants:

1. **Default is scan.** `mode` absent or `"scan"` keeps the exact argv (`--scan`,
   joined args, appended `--permit`), the mandatory `want_findings`, and the tuple
   compare. A scan case must never be routed to `--frozen`.
2. **Unknown mode fails closed.** `{"mode": "Frozen"}` must not silently run a
   scan. B raises `KeyError("mode")` → `malformed case`, exit 2 (S4). Keep that;
   A silently ignored unknown modes and the case passed as a scan (F3).
3. **`want_findings` is ignored in frozen mode** — not required, not compared.
   B never reads it on that branch; frozen cases with and without the key both pass
   (S1). On A this is false: a frozen case must still supply `want_findings`, and a
   non-empty one is compared and fails (E18).
4. **`want_label` is required in frozen mode**, otherwise a clean snapshot passes
   vacuously when `want_exit` matches and `want_findings` is empty (F2 on A:
   `mode:"frozen"` ignored, clean scan, rc 0, `CASE ok`). B makes the missing key a
   malformed case, exit 2 (S5).
5. **Frozen line 1 is `MADO_TRIPWIRE_FROZEN: <outcome>`**, never
   `MADO_TRIPWIRE: …`. The scan `first_ok` prefix check must stay
   `MADO_TRIPWIRE: `. The prefixes are disjoint (`_` vs `:` at index 15), so a
   misroute fails rather than passes — keep it so.
6. **Frozen verdicts have no `findings` key.** `use_file`/`key()` must not run on
   them; B `continue`s before `json.loads(out[1])`, which also means **frozen line
   2 is never validated** (`D2`).
7. **Arg shape:** only `args[0]` is used; missing/empty `args` is a malformed case,
   not a crash (`IndexError` now caught); extra args are silently ignored. If the
   contract wants exactly one, say so or the harness cannot tell.
8. **Output contract for receipts:** keep `CASE <name> ok|FAIL …`,
   `SELFTEST_SCRIPT_SHA256: <sha>`, `SELFTEST_SUMMARY: p/n passed failed=[…]`, and
   the 0/1/2 exit map. `SELFTEST_SCRIPT_SHA256` hashes the file being executed, so
   it self-describes the tested tool (A's receipts: `7a98720e…` at `f71ccbe` with
   26/26 → `962919ce…` at `0ab1ccc` with 30/30).
9. **Do not require the frozen snapshot's own `expected.json` to be a selftest
   spec.** `--selftest` on a frozen DIR remains `malformed expected.json
   (KeyError)`; `--frozen` must not call `run_selftest`. A suite DIR and a
   `--frozen` DIR cannot be the same directory (one `expected.json`, one schema).
10. **Scan stdout stays two lines** (label, JSON); the harness reads only
    `out[0]`/`out[1]`. Extra diagnostics after line 2 are ignored but pollute
    receipts; send them to stderr.

Residual defects in B, both fail-closed:

- **D1 (crash path).** `{"mode":"frozen","want_label":7}` raises `TypeError` at the
  `want_first` concatenation (B:1094), outside the per-case `try` → `__main__`
  handler prints `MADO_TRIPWIRE: could_not_evaluate` + scan verdict JSON, exit 2,
  no `SELFTEST_SUMMARY` (S7, reproduced at `c87a31ef`). Same shape as the non-dict
  `want_findings` path. An `isinstance(want_label, str)` check inside the try, or
  `str()` before concatenation, closes it.
- **D2 (claim strength).** Frozen cases compare exit + line 1 only. A `--frozen`
  regression that keeps label/exit but emits a wrong `tool_sha256`,
  `expected_sha256`, `inputs`, `missing_findings` or `extra_findings` still passes
  the frozen suite. This is exactly the contract ("compare exit and the first-line
  outcome"), so do **not** upgrade the claim: "frozen selftest N/N" proves the
  outcome mapping, not verdict-body conformance. Body conformance needs the raw
  `--frozen` receipts (match / tampered / mismatch) the hard cases already produce.

Frozen-runtime note (observed at `3e791ee`+): `frozen_snapshot` computes
`report[i]["ok"]` per entry (bytes match pin) and orders failures
path/regularity + unlisted `*.jsonl` → `snapshot_tampered`, then an entry without
`sha256` → `unpinned_legacy`, then digest mismatch → `snapshot_tampered`. So a
*missing* unpinned input reports `snapshot_tampered`, not `unpinned_legacy`
(`[INFERENCE]` from source order, consistent with the 17/17 suite).

## 8. Documented vs implemented (small, verified)

- `corpus/lessons/round-17.md:132` says `tripwire/w2-regressions` is **26/26**; the
  landed suite is **30** cases and the re-cut receipt says **30/30** at `0ab1ccc`
  (26 at `f71ccbe`, +4 fixtures in the P11 fix). The lesson text is stale relative
  to the receipt it cites elsewhere.
- Nothing in `corpus/` documents the selftest schema; the only prose about
  `want_findings` outside the tool is in round-17 wave-2 reports. The basename
  asymmetry (§5) and the `want_error_contains`-empty vacuity are undocumented.

## 9. Reproduction

```
# A: committed scan-only harness (receipts' sha)
for d in core compound hardening w2-regressions; do
  python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/$d | tail -1
done                                        # 9/9 16/16 33/33 30/30

# B: working tree with --frozen + harness branch
sha256sum tools/mado-tripwire.py            # c87a31ef… at report time
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen
                                            # 17/17, rc 0
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core
                                            # still 9/9
```

Probe matrix (all on `/tmp/twh`, drivers `probe.py` … `probe5.py`):
E0 no-file-key pass; E1 sub-dir want fails; E2 mixed file keys fail; E3 dict want
→ crash path; E4/E5 malformed case aborts; E6 absolute arg escapes; E7/P6 label
exactness; E8 spec-list; E9 string exit; E10 empty args + `no path`; E11
duplicate/subset want fail; E12/F1 basename collision blind pass; E13 string
permit → child exit 2; E14 empty permit; E15 permitted-only label; E16 frozen
label mismatch on A; F2 frozen vacuous pass on A (no `want_label`); E18 frozen
non-empty want compared on A; F3 unknown mode ignored
on A; F5 duplicate names; F6 extra jsonl ignored; F7 string line; P2 list want entry
→ crash; P3 empty cases; P4 wrong schema; P5 empty `want_error_contains` vacuous;
P7 frozen `args: []` on A (scan path). S1-S8 on B: frozen match (with/without
`want_findings`), tampered / unlisted / symlink / missing / `..` / absolute inputs
→ `snapshot_tampered`, unpinned → `unpinned_legacy`, wrong findings/label/known-miss
→ `frozen_verdict_mismatch`, unknown mode → malformed, missing `want_label` →
malformed, `want_label: 7` → crash (D1), scan `..`+basename case still passes.

## 10. Confidence

High for §2-§6 and §7.1-§7.10: source-read plus executed probes, reproduced at
both stamps and re-run at the final B sha (`c87a31ef`: 9/9, 16/16, 33/33, 30/30,
frozen 17/17; S4/S5/S6 malformed, S7 crash, S1-S3/S8 pass). Medium for the frozen
runtime internals: `run_frozen`/`validate_frozen`/`frozen_snapshot` were read and
exercised end-to-end through the harness, but the missing-unpinned ordering is
`[INFERENCE]` from source, not a separate probe. B is uncommitted and was still
moving after `c87a31ef`; if the sha differs at integration, re-stamp rather than
assume the line map.

No tools installed. Files written: this report only (`/tmp` fixtures outside the
lane).
