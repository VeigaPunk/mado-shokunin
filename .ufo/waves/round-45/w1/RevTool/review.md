# RevTool — code review of the C1 reference tool `mado-monitors.py` (w1, round 45)

Reviewed file: `.ufo/waves/round-45/l1-draft/mado-monitors.py` (532 lines, the C1 contract docstring).
Method: full read; docstring sentence vs code; executed input/injection/exit-code battery; mutants of
scratch copies; two frozen-counter runs on scratch clones. No lane file modified. No LSP device is
mounted in this seat's session — every semantic claim below is from full-file reads plus executed
repros, never from an index; raw outputs in `receipts/` (this dir). Locators are grep-computed.
Tooling: system python3 3.14 + git only; nothing installed; pacman untouched.

Reference baseline (verified, not assumed): `--selftest` → `MADO_MONITORS_SELFTEST: 33/33 passed`,
rc 0; frozen counter on a scratch clone carrying the reference at `tools/mado-monitors.py`:
`fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET` (receipts/counter-ref.txt) —
the registration's REF control expectation holds.

## Findings, by severity

### F1 — MEDIUM (verdict integrity): JSON `NaN` accepted; `scale: NaN` false-AGREEs
- Attacks: docstring:28-29 "a monitors input that is not UTF-8 JSON … is bad_json"; the tool's core
  promise that OK means agreement.
- `json.loads` (`mado-monitors.py:308`) accepts the Python `NaN`/`Infinity` extensions, which are not
  JSON; `parse_monitors` raises `Setup("bad_json")` only at :309/:311 (decode or shape). In
  `compare`, `scale` passes `is_num`, and at `mado-monitors.py:386`
  `if e is not None and abs(sc - e) >= 0.0001:` a NaN makes the comparison False → field passes →
  verdict OK, exit 0. Infinity is safe (`>= 0.0001` True → DIFFER); `refreshRate: NaN` fails mode at
  :374 (`abs(...) < 1.0` False) — safe. Exactly one false-agree vector, on the field this tool exists
  to check.
- Repro (receipts/repro-transcript.txt, block 1): dump `[{... "scale": NaN ...}]` +
  `monitor = DP-1, 3440x1440@100, 0x0, 1` → `MADO_MONITORS: … verdict=OK`, rc 0.
- Teeth: selftest has no NaN case (33/33 regardless); the 49 fixtures have none. A NaN regression or
  a NaN-tolerant integration scores MET.
- Suggested fix (reference is frozen; for the integrator): `json.loads(..., parse_constant=<raise>)`
  or `math.isfinite` guards on `sc`/`rr` before comparison.

### F2 — MEDIUM (falsifier teeth, counter-level): the 1048576-byte cap is enforced nowhere
- Attacks: docstring:27-28 "an input larger than 1048576 bytes is too_large"; clause s/f coverage of
  the contract sentence.
- The selftest has no oversize case; the 49 fixtures have none. Mutant M2b — the reference with
  `MAX_BYTES = 1048576` → `1048576000` (scratch copy) — scores
  `fixtures=49/49 selftest=ok readonly=ok verdict=TARGET_MET` on the frozen counter
  (receipts/counter-m2b-nocap.txt). The cap sentence would survive integration unchecked.
- The reference itself is correct at the boundary: 1048576-byte config → OK rc 0; 1048577-byte config
  and 1048577-byte stdin → `SETUP too_large` rc 2; `< /dev/zero` → `too_large` (bounded read, no
  hang). This is a teeth finding, not a reference defect.

### F3 — LOW/MEDIUM (selftest teeth): no bad_json case in the selftest; disabled check ⇒ crash on rc 1
- The selftest's only setup cases are 2×usage + 1×unreadable (lines 506-511). Mutant M1 — structure
  check `mado-monitors.py:311` replaced by `if False:` — still prints `33/33 passed` rc 0, and then
  `[1, 2]` as the dump crashes: rc 1 (the DIFFER exit code), empty stdout, non-empty stderr
  (traceback) — violating docstring:25-26 (SETUP exit 2) and the stderr discipline (docstring:31).
  The frozen fixtures do catch it (`setup-bad-json`, `setup-not-objects`), so the counter tooth
  exists; the selftest alone does not defend the setup surface it claims.

### F4 — LOW (robustness): `--monitors -` with closed stdin blocks indefinitely
- Docstring:25-26 promises every setup failure is one line `SETUP <reason>` + exit 2 with a closed
  reason list; an unusable stdin has neither reason nor exit. With fd 0 closed, CPython hands
  `sys.stdin` over a reopened blocking char device (probe: `os.fstat(0)` mode `0o20620`, tty-class);
  `sys.stdin.buffer.read` (`mado-monitors.py:146`) never returns. Observed: `python3 -I
  mado-monitors.py --monitors - --config ok.conf 0<&-` produced no output and was killed at 60 s
  (bash job bg_9679); probe `sys.stdin.buffer.read(10)` under `0<&-` timed out rc=124
  (receipts/closed-stdin.txt). Unreachable by the frozen counter — every fixture supplies stdin via
  `subprocess(input=...)`. Contrast: `< /dev/zero` is properly bounded (`too_large`).

### F5 — LOW (contract-silent input edges; behavior matches the docstring's letter, hostile to real configs)
All three fail LOUD (exit 4/5), never silently AGREE — honest degradation, but the docstring nowhere
warns that ordinary config shapes disable the tool:
- UTF-8 BOM before the first monitor line silently drops that rule: U+FEFF is neither space nor tab,
  so the line neither fullmatches `LINE_RE` (:100) nor counts anywhere → `lines=0`, verdict
  NO_RULES, exit 4 (observed). A BOM'd `monitors.conf` reports "no rules" for a file that has one.
- CRLF endings: `\r` survives the strip of spaces/tabs (:262 line strip, fields :265), the last field
  fails its regex → the line counts `unsupported` → NOT_COMPARED, exit 5 (observed). Every line of a
  CRLF file is unmodelled.
- `$`, `##` or a backslash inside a trailing comment → whole line `unsupported` (:264 tests the body
  before the `#` cut) → NOT_COMPARED, exit 5 (observed for `# see $main` and `## note`). A comment
  mentioning a shell variable forces NOT_COMPARED.
Code follows the contract text ("split on \n", strip " \t", body-contains test) — this is a
docstring-completeness gap, not an implementation deviation.

### F6 — INFO (output injection: none found)
Selectors and dump names are the only free text; both are printed via `json.dumps` ensure_ascii
(:408 sel, :424 name). Executed: selector containing `verdict=NO_RULES`, quotes, tab — stays inside
`sel="…"` quotes (a backslash cannot even reach it: :264 makes the line unsupported first); dump
`name` containing a raw newline plus forged `MADO_MONITORS: … verdict=OK` text → printed as the
two-character `\n` escape, stdout stays exactly rule+output+summary lines and the last line carries
the true verdict; NUL → `\u0000`; lone surrogate → `\ud800` escape (no crash); non-ASCII →
`\uXXXX`. `differ=`/`verdict=`/mode/pos/scale/mirror tokens come from fixed vocabularies or numeric
formats (%.2f/%.4f). Line-count and verdict forgery both fail.

### F7 — INFO (docstring conformance, checked clean)
- Arguments: two-token grammar exact; `--monitors` exactly once (second → usage), any flag order,
  `--selftest` alone; 8 malformed variants all → one-line `SETUP usage`, exit 2, empty stderr.
- Setup reasons: usage|unreadable|too_large|bad_json all reachable with exact bytes; FIFO (no hang,
  O_NONBLOCK :123), directory, `/dev/null` → unreadable; symlink-to-regular reads; 1 MiB boundary
  exact on both file and stdin paths.
- Rule semantics: v2 token boundary (`monitorv2 {`, bare, `= x` count; `monitorv2x` does not);
  comment cut at first `#`; disable/`transform` modifier (copies first same-selector rule; `add`
  :181 erases-then-appends so it moves last; also erases a prior `disable` rule — observed);
  `addreserved` default/no-op per fixtures; 60 Hz default; |Δrate| < 1.0 exclusive — mutant M3
  (`<` → `<=`) fails the selftest 32/33, so the harness bites on semantics; scale < 0.25 → 1.0; 1/120
  correction with round-half-up K (:330) and the 1..89 alternating search (:335) in docstring order;
  negative candidates are unreachable (for K ≤ 90 the candidate at i = K−1 is 1/120, which divides
  every integer w,h and is tried before any negative candidate); none-found → not compared;
  newest-match with FIRST empty-selector fallback (observed rule=1 of two); `desc:` on stripped TEXT,
  blank `desc:` matches everything; long-description-only `desc:` unmatched (declared).
- Type discipline: ints required for width/height/x/y/transform/id, numbers for refreshRate/scale,
  booleans never numbers — `width: true|3440.0` → DIFFER mode(+scale), `transform: true`,
  `scale: true` → DIFFER; `disabled: 1` is not live-disabled (`is True`, :364); `id: true` → mirror
  DIFFER.
- Verdicts: NO_RULES 4 / NOT_COMPARED 5 / DIFFER 1 / NO_MATCHING_MONITOR 3 / OK 0 tested in
  docstring order (empty dump + rules → NO_MATCHING_MONITOR; only-`monitorv2` → NOT_COMPARED);
  counters and summary fields agree with outputs in every run above.
- Read-only: imports are json/math/os/re/stat/struct/sys only; no bare `open(` (only
  `os.open(..., O_RDONLY | O_NONBLOCK)`, :123); token scan zero for
  subprocess/socket/exec/Popen/environ/getenv/popen/system/time/random/urllib/tempfile/shutil (the
  `socket`/`requests` grep hits are docstring prose, :23/:12); PATH poisoned with marker-creating
  `hyprctl`/`journalctl`/`wlr-randr`/`wayland-info` → no marker (counter clause r `marker=absent` on
  both counter runs); `env -i` selftest 33/33 (no env dependence); TMPDIR empty after runs (no temp
  files).

## Residual risk and verification gaps
- Docstring-vs-Hyprland-pins fidelity is explicitly out of my seat (non-author reading; fixtures +
  C2 own it) — I reviewed the contract against its own text only.
- The F4 hang was killed at 60 s; whether the tty read could ever return (e.g. after typing input)
  was not probed. Root cause sits at the CPython/environment layer; I characterized behavior, not
  CPython's reopen logic.
- Counter runs used the default seed 45 only; {A}{B}{C}/{D} substitution across other seeds is the
  counter's own mechanism, not re-verified.
- Exit-code note: DIFFER and selftest-failure share exit 1; distinguishable by stdout shape/stderr,
  and the counter demands exact stdout + empty stderr, so scoring is unambiguous.
- Scratch clones with throwaway-identity commits (counter runs) live under
  /fast/scratch/hyaku/mado-r45/RevTool and are deleted after this report; receipts copied to
  `receipts/` first. Their rev hashes are recorded inside the receipts.
