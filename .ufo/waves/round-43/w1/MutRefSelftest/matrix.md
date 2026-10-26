# MutRefSelftest — mutation matrix for the C1 reference tool's selftest

Seat: MutRefSelftest, mado round 43 w1 (2026-10-26). Target: `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`
(sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`, re-verified identical after
the sweep — the frozen file was never modified; all mutants lived in scratch copies).

## Method

- 77 mutants, one minimal edit each (comparison, constant, branch removal, regex edit, return value,
  swap, reorder), covering all 11 functions except `selftest` (`read_regular` 5, `parse_args` 7,
  `regex_ok` 6, `parse_rule_text` 12, `parse_clients` 3, `client_size` 4, `matches` 4, `evaluate` 11,
  `report` 9, `run` 7, `main` 4, module constants 4). Harness: `mutate.py` (mutant list + exact-string
  replacement, count==1 asserted), `counter_run.py`; per-mutant scratch copies
  `/fast/scratch/hyaku/mado-r43/MutRefSelftest/mut/mut_<id>.py` (deleted at cleanup; definitions
  reproducible from `mutate.py`).
- Detector 1 (the tool's own selftest): `python3 -I mut_<id>.py --selftest`; survive = rc 0 and
  `MADO_GEOMETRY_SELFTEST: k/n passed` with k==n, n>=50.
- Detector 2 (frozen counter, survivors only): `cd /home/vgpnk/Projects/shokunin/mado-shokunin &&
  C1R42_TMP=/fast/scratch/hyaku/mado-r43/MutRefSelftest python3 -I quality/counters/c1-r42-geometry.py
  --repo . --rev b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 --tool <mutant>`.
- Pristine baseline: selftest 73/73 rc 0; counter `fixtures=37/37 tool=present verdict=TARGET_MET`
  rc 0 (evidence/counter-pristine.txt, nonce 9fc7323bb37cd61c).

## Verdict summary

77 mutants: **53 killed by the selftest alone**; **18 survived the selftest, killed by the counter's
fixtures** (all with clauses a/b/b2/b3/g still 1 — fixture kills, byte-exact model comparison);
**6 survived both**: 3 equivalent (C1, G6, P2 — proofs below), 3 not equivalent (N1, U4, R5 — missing
assertions below; N1 additionally exposes a latent contract violation in the pristine reference).

Structural finding: the selftest never invokes `run`/`main` (it calls `report`, `parse_args`,
`read_regular`, `regex_ok`, `matches` in-process), so the whole CLI layer is invisible to it — 10 of
the 24 selftest-survivors are `run`/`main` mutants (U1-U6, N1-N4). The counter's fixtures catch 8 of
those 10; the two that slip through (U4 strict decode, N1 except-widen) mark contract clauses no
fixture exercises (non-UTF-8 rules file; any input that crashes the tool).

## Table A — the 24 selftest-survivors

| id | fn | edit | selftest | counter | class |
|----|----|------|----------|---------|-------|
| C1 | parse_clients | `except (UnicodeDecodeError, ValueError)` → `except ValueError` | 73/73 | MET rc 0 | **equivalent** (UnicodeDecodeError ⊂ ValueError, verified `issubclass` True; badjson0's `\xff[]` still caught) |
| G6 | regex_ok | `re.compile(rx)` → `re.compile(rx, re.I)` | 73/73 | MET rc 0 | **equivalent** (re.I never changes syntactic validity; `matches` recompiles unflagged; 50k fuzz regexes, 0 diffs) |
| P2 | parse_rule_text | `RULE_LINE.fullmatch` → `.match` | 73/73 | MET rc 0 | **equivalent** (pattern ends in `(.*)`, so every prefix match is a full match; 200k fuzz lines, 0 diffs) |
| N1 | main | `except Setup` → `except Exception` | 73/73 | MET rc 0 | **not equivalent** — deep-nested clients JSON: pristine rc 1 traceback (evidence/n1.err), mutant rc 2 `SETUP Stack overflow…` (evidence/n1.out); contract says `bad_json` exit 2. Pristine itself violates the contract here |
| U4 | run | `.decode("utf-8", "replace")` → `.decode("utf-8")` (strict) | 73/73 | MET rc 0 | **not equivalent** — rules file containing `\xff`: pristine rc 3 `rules=1 … unsupported=0` (byte replaced, lone `\ufffd` line ignored), mutant rc 1 traceback (evidence/u4.out vs u4.err). No fixture feeds a non-UTF-8 rules file |
| R5 | read_regular | `finally: os.close(fd)` → `finally: pass` (fd leak) | 73/73 | MET rc 0 | **not equivalent in general; indistinguishable on this host** — 2000 `--rules` files: pristine == mutant, rc 3 `rules=2000` (host `ulimit -n` 524288; argv size caps `len(rules)` far below it). Distinguishing input needs RLIMIT_NOFILE ≈ 1024: 1100 one-line rules files → pristine `rules=1100` rc 3, mutant `SETUP unreadable` (EMFILE). Latent leak, unkillable here |
| R1 | read_regular | drop `O_NONBLOCK` | 73/73 | MISSED, fails fifo0 (30 s timeout: mutant blocks opening the FIFO) | missing assertion |
| R2 | read_regular | size limit `>` → `>=` | 73/73 | MISSED, fails boundary0 | missing assertion |
| S4 | client_size | `v >= 0` → `v > 0` | 73/73 | MISSED, fails size0, sizevals0, many0 | missing assertion |
| M4 | matches | control-char threshold `0x20` → `0x0A` | 73/73 | MISSED, fails ctlclass0 | missing assertion |
| E9 | evaluate | TILED checked before BADSIZE | 73/73 | MISSED, fails gen4, gen5, client0 | missing assertion |
| P13 | parse_rule_text | ws-split → `split(" ")` in field 0 | 73/73 | MISSED, fails space0 | missing assertion |
| G5 | regex_ok | drop `?` from the SAFE alphabet | 73/73 | MISSED, fails gen3, regex0 | missing assertion |
| K1 | const | `MAX_BYTES = 1048575` | 73/73 | MISSED, fails stdinok0, boundary0 | missing assertion (same assertion as R2) |
| K3 | const | `match:class[ \t]+` → `[ \t]*` | 73/73 | MISSED, fails space0 | missing assertion |
| K4 | const | NUM `{1,5}` → `{1,4}` | 73/73 | MISSED, fails size0 | missing assertion |
| U1 | run | invert `clients == "-"` | 73/73 | MISSED, fails all 36 fixtures | missing assertion |
| U2 | run | `stdin.read(MAX_BYTES - 1)` | 73/73 | MISSED, fails stdinbig0 | missing assertion |
| U3 | run | drop stdin `too_large` check | 73/73 | MISSED, fails stdinbig0 | missing assertion (same assertion as U2) |
| U5 | run | `"".join(lines)` (no newlines) | 73/73 | MISSED, fails 34 fixtures | missing assertion |
| U6 | run | `rc = 0` forced | 73/73 | MISSED, fails 18 rc-bearing fixtures | missing assertion |
| N2 | main | SETUP `print(…, end="")` | 73/73 | MISSED, fails all 6 SETUP fixtures | missing assertion |
| N3 | main | SETUP rc 2 → 0 | 73/73 | MISSED, fails all 6 SETUP fixtures | missing assertion |
| N4 | main | `sys.stdin.buffer` → `sys.stdin` | 73/73 | MISSED, fails 7 stdin fixtures (crash) | missing assertion |

Counter evidence per survivor: `evidence/counter_<id>.txt` (all six double-survivors plus one
representative fixture-kill sample `counter_E9-sample-fixture-kill.txt`; the full set of per-mutant
counter logs and `counter-summary.json` were in scratch and are summarized here — the 18 fixture
kills each name their failing fixtures above, taken from `counter-summary.json`).

## Table B — the 53 selftest-killed mutants (killing cases from the mutants' own selftest output)

| id | fn | edit | killed by (selftest case names / crash) |
|----|----|------|------------------------------------------|
| R3 | read_regular | S_ISREG branch → `if False` | unreadable-chardev (/dev/null read as empty file) |
| R4 | read_regular | open-failure reason unreadable → bad_json | unreadable-missing |
| A1 | parse_args | `--selftest` sentinel → `[]` | `--selftest` run itself: rc 2 `SETUP usage` |
| A2 | parse_args | drop `clients is None` guard | usage-double-clients |
| A3 | parse_args | `--rules` → `--rule` | `--selftest` run itself: rc 2 `SETUP usage` |
| A4 | parse_args | drop `not rules` check | usage-no-rules |
| A5 | parse_args | `i += 2` → `i += 1` | `--selftest` run itself: rc 2 `SETUP usage` |
| A6 | parse_args | return `"RUN"` | rules-repeat-ok (asserts the exact tuple) |
| A7 | parse_args | dangling-arg reason usage → unreadable | usage-dangling, usage-bogus |
| G1 | regex_ok | drop SAFE gate | hash-unsupported, negative-prefix-unsupported, cr-breaks-regex, regex-safe-rejects-brace, regex-safe-rejects-class, regex-safe-rejects-201, regex-safe-rejects-bad-escape (8 cases) |
| G2 | regex_ok | drop bad-substring loop | inline-flag-unsupported, possessive-unsupported |
| G3 | regex_ok | `except re.error: return True` | crash rc 1: PatternError escapes via `matches` (uncompilable rule now supported) |
| G4 | regex_ok | `{1,200}` → `{1,201}` | regex-safe-rejects-201 |
| P1 | parse_rule_text | `strip(" \t")` → `strip()` | cr-breaks-regex |
| P3 | parse_rule_text | drop `other` count | other-counted |
| P4 | parse_rule_text | `len(fields) == 2` → `>= 2` | two-matches-unsupported |
| P5 | parse_rule_text | `NUM.fullmatch` → `.match` | crash rc 1: `int('1x')` (nondigit accepted) |
| P6 | parse_rule_text | float arg only `"on"` | file-index-and-numbering (float off rule) |
| P7 | parse_rule_text | `arg=%dx%d` → `%d:%d` | rule-line, file-index-and-numbering |
| P8 | parse_rule_text | swap want W/H | agree-rc, agree-line, last-size-wins-agree, alternation-fullmatch, tight-spacing, missing-class-empty, … (13 cases) |
| P9 | parse_rule_text | `float` treated as other | crash rc 1: IndexError (float rule's want is a str) |
| P10 | parse_rule_text | invert `good` gate | crash rc 1: `int('1x')` |
| P12 | parse_rule_text | drop per-field strip | crash rc 1: IndexError (leading-space match field) |
| C2 | parse_clients | drop all-dict check | crash rc 1: AttributeError on `[1]` |
| C3 | parse_clients | first bad_json reason → unreadable | bad-json-empty, bad-json-bytes, bad-json-truncated |
| S1 | client_size | `len(s) == 2` → `== 3` | agree-line, differ-rc, differ-verdict, tiled-count, last-size-wins, non-true-floating-tiled, json-escaped-fields, … (11 cases) |
| S2 | client_size | accept floats | float-size-badsize |
| S3 | client_size | drop bool exclusion | bool-size-badsize |
| M1 | matches | threshold `0x20` → `0x21` (blocks space) | json-escaped-fields (class "ü a" contains a space) |
| M2 | matches | `fullmatch` → `search` | matches-full |
| M3 | matches | invert match result | 23 cases (agree-rc … matches-ctl) |
| E1 | evaluate | `mapped is False` → `is not True` | missing-class-empty, non-string-class-empty, non-true-floating-tiled, non-false-mapped-counts |
| E2 | evaluate | drop unmapped `continue` | unmapped-rc, unmapped-count |
| E3 | evaluate | class always `""` | crash rc 1: IndexError (no rule lines emitted) |
| E4 | evaluate | invert rule match | 23 cases |
| E5 | evaluate | size/float roles swapped | crash rc 1: TypeError `%d` on str want |
| E6 | evaluate | drop no-want `continue` | crash rc 1: TypeError on None want |
| E7 | evaluate | `floating is True` → `is not False` | non-true-floating-tiled |
| E8 | evaluate | invert AGREE/DIFFER | 18 cases |
| E11 | evaluate | addr always `"-"` | json-escaped-fields |
| E12 | evaluate | `want=%dx%d` → `%d-%d` | json-escaped-fields |
| E13 | evaluate | `true/false` → `yes/no` | json-escaped-fields |
| B1 | report | file index from 0 | rule-line, file-index-and-numbering |
| B2 | report | rule n from 0 | rule-line, file-index-and-numbering |
| B3 | report | `size_rules` counts floats | no-size-rule-rc, last-size-wins-agree, alternation-fullmatch, tight-spacing, float-arg-unsupported, v2-and-comment-ignored, … (12 cases) |
| B4 | report | `differ > 0` → `>= 0` | agree-rc, agree-line, tiled-rc, unmapped-rc, empty-rc, nomatch-rc, fullmatch-not-search, … (16 cases) |
| B5 | report | `matched == 0` → `> 0` | same 16 cases as B4 |
| B6 | report | NO_SIZE_RULES rc 4 → 3 | no-size-rule-rc, empty-rules-rc, title-unsupported |
| B7 | report | `float_rules=` → `float=` | agree-line, empty-rules-line, float-arg-unsupported, v2-and-comment-ignored |
| B8 | report | `float_rules` = size count | float-arg-unsupported, v2-and-comment-ignored (both have 1 size rule, 0 float rules and check the last line) |
| B9 | report | swap other/unsupported columns | title-unsupported, three-args-unsupported, nondigit-unsupported, six-digits-unsupported, two-matches-unsupported, … (11 cases) |
| U7 | run | swap unpack targets | `--selftest` run itself: rc 2 `SETUP unreadable` |
| K2 | const | `windowrule` → `Windowrule` | crash rc 1: IndexError (no rule ever parsed) |

Full per-mutant lists: `evidence/failcases.json` (copied from scratch before cleanup).

## Equivalence proofs (the three double-survivors classified equivalent)

- **P2** — `RULE_LINE.fullmatch(line)` → `RULE_LINE.match(line)`: lines contain no `\n` (split on
  `"\n"` first), and the pattern `windowrule[ \t]*=(.*)` ends with `(.*)`, which matches any
  remainder; hence every prefix match extends to a full match, and fullmatch ⇒ match trivially.
  Empirical: 200,000 fuzz lines over `windowrulev2= \txX0123456789ab.,:#`, 0 disagreements.
- **G6** — `re.compile(rx)` → `re.compile(rx, re.I)`: `re.IGNORECASE` alters matching semantics,
  never syntactic validity, so `regex_ok`'s accept/reject decision is unchanged; `matches()`
  recompiles the regex without flags, so runtime behavior is unchanged. Empirical: 50,000 fuzz
  regexes over the SAFE alphabet, 0 disagreements.
- **C1** — `except (UnicodeDecodeError, ValueError)` → `except ValueError`: `UnicodeDecodeError` is
  a subclass of `ValueError` (verified: `issubclass(UnicodeDecodeError, ValueError)` → True), so the
  wider tuple was redundant; every input the tuple caught is still caught.

## Assertions to add to `selftest` (unified-diff-free list)

In-process only (the counter runs the selftest under RLIMIT_NPROC = 1 — no spawning; no new imports:
`json os re stat sys` suffice). `cl`, `last`, `chk`, `gk` are the existing selftest helpers. File-backed
assertions build their fixtures with `os.open`/`os.write`/`os.unlink` in `os.environ.get("TMPDIR", "/tmp")`
under unique names and unlink them in a `finally`.

1. **zero-size** (kills S4): `s, rc = last([cl("a", [0, 0])], "windowrule = size 0 0, match:class a\n")`
   → expect `rc == 0` and `" agree=1 "` in `s` and `"size=0x0 want=0x0"` in the client line.
   (S4 mutant: `badsize=1`, rc 3.)
2. **tab-in-class** (kills M4): `chk("matches-tab", matches("a.b", "a\tb"), False)`.
   (M4 mutant: True — a tab would be matched by `.`.)
3. **bare-question alphabet** (kills G5): `chk("regex-safe-accepts-opt", regex_ok("a?"), True)`.
   (G5 mutant: False → rule unsupported.)
4. **five-digit size** (kills K4): `s, rc = last([cl("a", [99999, 99999])],
   "windowrule = size 99999 99999, match:class a\n")` → expect `rc == 0` and `" agree=1 "` in `s`.
   (K4 mutant: unsupported=1, rc 4.)
5. **no-space match field** (kills K3): `s, rc = last([cl("a", [1, 2])],
   "windowrule = size 1 2, match:classa\n")` → expect `rc == 4` and `" unsupported=1 "` in `s`.
   (K3 mutant: supported, rc 0.)
6. **tab-separated field 0** (kills P13): `lines, rc = report(json.dumps([cl("a", [1, 2])]).encode(),
   ["windowrule = size\t1\t2, match:class a\n"])` → expect `lines[0] ==
   "MADO_GEOM_RULE: n=1 file=1 effect=size arg=1x2 class=a"`. (P13 mutant: `other=1`, rc 4.)
7. **badsize-before-tiled order** (kills E9): `s, rc = last([cl(g, [420], floating=False)], gk)`
   → expect `" badsize=1 "` in `s` (and `" tiled=0 "`). (E9 mutant: `tiled=1`.)
8. **exact-size rules file** (kills R2 and K1): write a rules file of exactly `MAX_BYTES` bytes
   (one valid rule line + `#` padding), then `run(["--clients", <clients-tmp>, "--rules", <rules-tmp>],
   fake_stdin(b""))` → expect rc 3 and `rules=1` in the summary. (R2/K1 mutants: `SETUP too_large`.)
   Cost note: a 1 MiB temp file inside the counter's tmpfs sandbox.
9. **stdin upper bound** (kills U2 and U3): `run(["--clients", "-", "--rules", <rules-tmp>],
   fake_stdin(b" " * (MAX_BYTES + 1)))` → expect `Setup("too_large")` raised.
   (U2 mutant: reads MAX_BYTES-1 spaces → `SETUP bad_json`; U3 mutant: no check → `SETUP bad_json`.)
10. **file-clients path** (kills U1): clients tmp file holds `[{"class":"a","size":[1,2],"floating":true}]`,
    rules tmp file `windowrule = size 1 2, match:class a\n`, fake stdin empty:
    `run(["--clients", <clients-tmp>, "--rules", <rules-tmp>], fake_stdin(b""))` → expect rc 0 and
    `" agree=1 "` in the summary. (U1 mutant: reads stdin → `SETUP bad_json`.)
11. **newline-separated stdout** (kills U5): with a capturing fake stdout (an object with `write`),
    `run(["--clients", "-", "--rules", <rules-tmp>], fake_stdin(b"[]"))` → expect the captured text ==
    `"\n".join(lines) + "\n"` for the lines the pristine run produces (rule line + summary).
    (U5 mutant: one concatenated line.)
12. **exit codes from run** (kills U6): same setup with a differ client (`size [3,2]`) → expect
    `run(...)` returns 1. (U6 mutant: 0.)
13. **non-UTF-8 rules file** (kills U4): rules tmp file = `b"windowrule = size 1 2, match:class a\n\xff\n"`;
    `run(["--clients", <clients-tmp "[]">, "--rules", <rules-tmp>], fake_stdin(b""))` → expect rc 3,
    `"rules=1 … unsupported=0"` in the summary, stderr empty (the lone `\ufffd` line is ignored and
    counted nowhere). (U4 mutant: UnicodeDecodeError traceback, rc 1.)
14. **SETUP line shape** (kills N2 and N3): with `sys.argv` patched to `["mado-geometry.py", "--clients"]`
    and a capturing fake stdout, `main()` → expect return 2 and the captured text ==
    `"MADO_GEOMETRY: SETUP usage\n"` (trailing newline included). (N2 mutant: no newline; N3 mutant: 0.)
15. **stdin.buffer consumption** (kills N4): with `sys.stdin` replaced by a fake exposing
    `.buffer` (a bytes reader over `b"[]"`) and a rules tmp file, `main()` (argv
    `["mado-geometry.py", "--clients", "-", "--rules", <rules-tmp>]`) → expect rc 3 and the normal
    rule + summary lines. (N4 mutant: passes the text wrapper → AttributeError crash.)
16. **deep-nested clients JSON** (kills N1 — two-edged): clients input `"[" * 60000 + "]" * 60000`
    → expected per contract: `MADO_GEOMETRY: SETUP bad_json`, exit 2. **This assertion currently
    fails on the pristine reference too** (RecursionError traceback, rc 1 — evidence/n1.err), so it
    may only be added together with a tool fix (catch `RecursionError` beside
    `UnicodeDecodeError`/`ValueError` in `parse_clients`). As it stands it documents a latent
    contract violation of the reference, not just a selftest gap.
17. **many rules files** (kills R5 only where RLIMIT_NOFILE is small): 1100 one-line rules files →
    expect rc 3 and `rules=1100`. On this host (`ulimit -n` 524288) pristine and mutant are
    indistinguishable (verified: 2000 files, identical output) — the assertion is
    environment-conditional and cannot be armed portably; the fd leak stays a declared latent defect.
18. **FIFO rules path** (kills R1, by timeout only): `os.mkfifo` a path and pass it as `--rules` →
    expected per contract: `Setup("unreadable")` without blocking. Caveat: the R1 mutant blocks in
    `os.open`, so in-process the selftest would hang and only the counter's 60 s selftest timeout
    detects it (fifo0 already does this at 30 s); arm this assertion only if a hang-tolerant
    mechanism is acceptable.

Assertions 1-7 and 14-15 are cheap and portable; 8-13 need tmp-file plumbing inside `selftest`;
16 requires the pristine tool fix first; 17-18 are environment-conditional (17) or timeout-based (18).
Adding 1-15 would have killed every non-equivalent selftest-survivor that the counter's fixtures
catch (18 mutants) plus U4 and N1, leaving only the three proven equivalents and the two
environment-conditional mutants (R5, and R1 if 18 is skipped) undetected by the selftest alone.
