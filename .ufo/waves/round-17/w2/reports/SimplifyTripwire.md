# SimplifyTripwire — `tools/mado-tripwire.py` deletion / simplification set (W2, report only)

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `988b858bd6049bc709807534fd725c05264f7e60`.
Artifact under review: `tools/mado-tripwire.py`, 818 lines, sha256
`4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44` (unchanged after this seat; `git diff` empty).

**Installs: none.** No pacman/sudo/systemctl/compositor/live probe was run. No file outside `/tmp` was modified.
This report is the only lane write.

## Verdict

Ten scratch mutations were built from a pristine copy and measured against the three pinned suites and a
differential harness. Every proposal below is **output-identical** to the shipped tool: all three suites stay
green and the full verdict JSON (including `command`, counts and file digests) is byte-identical on all 49
regular fixtures. The combined variant is 818 → 816 lines (non-blank 758 → 752) and removes six dead/duplicate
items plus three stacked authorities.

The attack on the C3 landing (9/9, 16/16, 33/33 selftests, anchor exit 1, 4/4 pacman.log join) **failed**:
nothing in the classifier changes. What did surface is code the suites cannot see — three over-general
behaviors with concrete counterexamples (§ Findings), one of which (F3) is a real detection hole under the
alias `import subprocess as sp`.

## Method (all read-only; scratch copies under `/tmp/simplify-tripwire.3092`)

- Baseline: `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening}`
  → `9/9`, `16/16`, `33/33`.
- Differential harness (`/tmp/.../fuzz.py`): one synthetic transcript with 156 `bash` tool calls, 25 `eval`
  calls (literal, non-literal, `!`-bang, `%%bash`, heredocs, `await tool.bash`, JS, malformed) and three
  non-toolCall record shapes; scanned five ways (single file, directory, three `--permit` sets) plus eight
  refusal paths (missing path, non-`.jsonl`, empty dir, bad/empty permit, no path, usage, refused name).
  13 byte-exact comparisons of stdout + exit code per variant.
- Stronger check for the combined variant: scan of all 49 regular fixture files (core 9 + compound 16 +
  hardening 33, excluding `malformed.jsonl`, `agent.db.jsonl` and the symlink fixture, which are the exit-2
  cases themselves) compared with `cmp` — byte-identical verdict, 53 findings each, exit 1 each.
- Every mutant was executed only as a `/tmp` copy; the lane file was never edited. Restored/verified state:
  sha256 `4ced68d3…`, `git diff -- tools/mado-tripwire.py` empty.

## Proposals (exact line numbers in the shipped file; apply bottom-up)

| # | Lines | What | Δ lines | Proof |
|---|-------|------|---------|-------|
| P1 | 50, 167 | drop `REDIRECTS`, the `tok in REDIRECTS` disjunct, and the constant-true `tok not in SEPARATORS` conjunct | −1 | 399-token enumeration, 0 divergent |
| P2 | 163 | drop `or tok == "\n"` — `"\n"` is already in `SEPARATORS` (49) | 0 | set membership |
| P3 | 74 | drop `"systemd-run"`, `"su"` from `HOST_MUTATION_BINS` — shadowed by the earlier branches at 393/398 | 0 | control flow + run0 fixture |
| P4 | 178, 182 | drop `in_single` (never assigned `True`) and its conjunct | −1 | grep: single assignment `False` |
| P5 | 507 | drop `lines and` — `str.split("\n")` is never empty | 0 | Python semantics |
| P6 | 82–83 | drop the two `SPAWN_FUNCS` entries duplicated by `SHELL_STRING_FUNCS` (84–86) | −1 | measured identical, incl. the `sp.` miss |
| P7 | 294–314 | hoist `long_ops` out of the loop and merge the two per-arg flag dicts into one table | +1 | snapshot equality |
| P8 | 352–354, 408–413 | one `shell_code()` authority for the duplicated shell `-c` predicate | +5 | snapshot equality |
| P9 | 713–717, 783–787, 795–799, 801–805 | one `emit_failure()` authority for four copies of the exit-2 payload | −5 | all refusal paths |
| P10 | 508–510, 754, 759–762, 772 | nits, not applied (see below) | 0 | — |
| — | combined | P1–P9 | **−2** (816) | suites + 13/13 + `cmp` |

### P1 — `REDIRECTS` is fully subsumed (50, 167)

```diff
 SEPARATORS = {";", "&&", "||", "|", "&", "|&", ";;", "(", ")", "\n"}
-REDIRECTS = {">", ">>", "<", "<<", "<<<", ">&", "<&", ">|", "&>", "&>>", "<>"}
...
-        elif tok in REDIRECTS or (tok and set(tok) <= set("<>&|") and tok not in SEPARATORS):
+        elif tok and set(tok) <= set("<>&|"):
```

Every `REDIRECTS` member consists only of `<>&|` and none is in `SEPARATORS`, so the generic clause already
covers it. The trailing `tok not in SEPARATORS` was always redundant: the elif is only reached when the
`if tok in SEPARATORS` branch at 163 did not fire. Exhaustive check: all 399 strings over `<>&|;()` of length
1–3, `0` divergent between old and new predicates. Note the suites do **not** pin redirect skipping (Finding
F4), so this rests on the enumeration plus the fuzz corpus (`>>`, `<`, `2>&1`, `<&0`, `&>>`, `>|`, `<>`,
`&&>>` all exercised).

### P2 — duplicate newline test (163)

```diff
-        if tok in SEPARATORS or tok == "\n":
+        if tok in SEPARATORS:
```

`SEPARATORS` (49) ends in `"\n"`. Exact.

### P3 — two unreachable set members (74)

```diff
-                      "shutdown", "halt", "systemd-run", "su"}
+                      "shutdown", "halt"}
```

`classify_segment` reaches `if argv0 == "su":` (393) and `if argv0 == "systemd-run":` (398) before
`if argv0 in HOST_MUTATION_BINS:` (467); both earlier branches return and emit the identical
`("host_mutation", "su")` / `("host_mutation", "systemd-run")` rule. `systemd-run` is pinned by
`hardening/run0-and-systemd-run.jsonl` (expected rule `systemd-run` line 1); `su` is not pinned by any fixture
(F4) but stays pinned by fuzz lines 17–20 (`su`, `su -c …`, `su - root -c …`, `su -l`).

### P4 — dead state in `substitutions` (178, 182)

```diff
-    in_single = False
...
-        if ch == "'" and not in_single:
+        if ch == "'":
```

`in_single` has exactly one assignment in the file (178, `False`); nothing sets it `True`, so the conjunct is
constant-true. (The function remains approximate by its own comment at 184 — this deletion does not change it.)

### P5 — dead guard in `classify_eval` (507)

```diff
-    if lines and lines[0].strip().startswith("%%bash"):
+    if lines[0].strip().startswith("%%bash"):
```

`code.split("\n")` always returns at least `[""]`.

### P6 — duplicate spawn-table entries (82–83)

```diff
-SPAWN_FUNCS = {"run", "call", "check_call", "check_output", "Popen",
-               "getoutput", "getstatusoutput"}
+SPAWN_FUNCS = {"run", "call", "check_call", "check_output", "Popen"}
```

`subprocess.getoutput` / `subprocess.getstatusoutput` are already matched by `SHELL_STRING_FUNCS` (84–86) and
take the same `is_shell_fn` branch; measured output-identical, including `sp.getoutput`. **Read F3 before
landing this alone** — the deletion is behaviour-neutral but encodes a hole rather than fixing it.

### P7 — pacman option tables (294–314)

```diff
+ PACMAN_LONG_OPS = {"--sync": "S", "--query": "Q", "--remove": "R",
+                    "--upgrade": "U", "--database": "D", "--files": "F",
+                    "--deptest": "T", "--version": "V"}
+ PACMAN_LONG_FLAGS = {"--refresh": "y", "--sysupgrade": "u",
+                      "--downloadonly": "w", "--clean": "c",
+                      "--print": "p", "--search": "s", "--info": "i",
+                      "--list": "l", "--groups": "g"}
...
-        if a.startswith("--"):
-            long_ops = {...}                      # rebuilt for every arg
-            if a in long_ops and op is None:
-                op = (a, long_ops[a])
-        elif a.startswith("-") and len(a) > 1:
+        if a in PACMAN_LONG_OPS:
+            if op is None:
+                op = (a, PACMAN_LONG_OPS[a])
+        elif a.startswith("-") and not a.startswith("--") and len(a) > 1:
...
-        elif a in ("--refresh", ...):
-            flags.add({"--refresh": "y", ...}[a])
-        elif a in ("--print", ...):
-            flags.add({"--print": "p", ...}[a])
+        elif a in PACMAN_LONG_FLAGS:
+            flags.add(PACMAN_LONG_FLAGS[a])
```

Two flag spellings per option currently live in two literals (`in (...)` and the map), and `long_ops` is
rebuilt inside the argument loop. Output-identical; the `--` guard in the `elif` preserves the original's
`if a.startswith("--")` / `elif` semantics for unknown long options. Cost: +1 line; value: one table per
concept. Skip if LOC is the only axis.

### P8 — duplicated shell `-c` predicate (352–354, 408–413)

```diff
+def shell_code(args):
+    """(inline-code flag present, code after it or None) for a shell argv tail."""
+    for idx, a in enumerate(args):
+        if a.startswith("-") and not a.startswith("--") and "c" in a:
+            return True, (args[idx + 1] if idx + 1 < len(args) else None)
+    return False, None
...
-            if base in SHELLS and not any(
-                    a.startswith("-") and "c" in a and not a.startswith("--") for a in s[1:]):
+            if base in SHELLS and not shell_code(s[1:])[0]:
                 fed_to_shell = True
...
-    if argv0 in SHELLS:
-        for idx, a in enumerate(args):
-            if a.startswith("-") and not a.startswith("--") and "c" in a:
-                if idx + 1 < len(args):
-                    hits.extend(classify_shell(args[idx + 1], depth + 1))
-                break
-        return hits
+    if argv0 in SHELLS:
+        code = shell_code(args)[1]
+        if code is not None:
+            hits.extend(classify_shell(code, depth + 1))
+        return hits
```

Both spellings of "does this shell carry inline code" are present today and can drift; the tuple keeps the
`bash -c` with no argument case exact. Cost: +5 lines. Skip if LOC is the only axis.

### P9 — four copies of the exit-2 payload (713–717, 783–787, 795–799, 801–805)

```diff
+def emit_failure(message, permit=()):
+    emit("could_not_evaluate", {"schema": "mado-tripwire-verdict-v1", "exit": 2,
+                                "error": message, "files": [], "findings": [],
+                                "counts": {c: 0 for c in CLASSES},
+                                "permitted": sorted(permit), "unpermitted": 0})
...
-        emit("could_not_evaluate", {...})       # run_scan
+        emit_failure(str(exc), permit)
...
-        emit("could_not_evaluate", {... "error": "usage" ...})
+        emit_failure("usage")
...
-            emit("could_not_evaluate", {... "error": "unknown permit class" ...})
+            emit_failure("unknown permit class")
...
-        emit("could_not_evaluate", {... "error": "no path" ...})
+        emit_failure("no path")
```

Key sets and `sort_keys=True` are identical, so stdout bytes are unchanged; the eight refusal comparisons
cover all four call sites. Leave the `__main__` internal-error payload (813–818) alone — it is deliberately a
smaller shape.

### P10 — nits (not applied; zero behaviour change each)

- 764: `first_ok = out[0].startswith(...) if out else False` — `split("\n")` never returns `[]`; the guard is dead.
- 759–762: `key()` nests a `use_file` conditional inside a `from_want` conditional; an early return for
  `not use_file` reads better and is the same tuple.
- 772: `hashlib.sha256(open(me, "rb").read())` leaks the handle; `with open(...)`.
- 508–510: the leading indentation is re-recovered with a second `re.match(r"^\s*", ln)`; capture it in the
  first pattern (`^(\s*)(?:…)?!(.*)$`) and reuse group 1 for the `pass` stub.

## Measured equivalence

Every single-mutation variant and the combined variant: `9/9`, `16/16`, `33/33`; `13 comparisons, 0 diffs`.

| variant | suites | differential |
|---|---|---|
| m_redirects (P1) | 9/9 16/16 33/33 | 0/13 |
| m_newline (P2) | 9/9 16/16 33/33 | 0/13 |
| m_setholes (P3) | 9/9 16/16 33/33 | 0/13 |
| m_insingle (P4) | 9/9 16/16 33/33 | 0/13 |
| m_linesguard (P5) | 9/9 16/16 33/33 | 0/13 |
| m_spawn (P6) | 9/9 16/16 33/33 | 0/13 |
| m_pacman (P7) | 9/9 16/16 33/33 | 0/13 |
| m_shellcode (P8) | 9/9 16/16 33/33 | 0/13 |
| m_fail (P9) | 9/9 16/16 33/33 | 0/13 |
| combined (P1–P9) | 9/9 16/16 33/33 | 0/13 |
| **total** | **10 × green** | **130/130 identical** |

Combined: 816 lines / 752 non-blank (from 818 / 758); full verdict over the 49 fixtures byte-identical to the
shipped tool (`cmp` exit 0), 53 findings, exit 1; `py_compile` clean.

## Findings — over-general code the suites cannot see

These are attack results, not patches; each has a concrete anchor. The suites compare only
`(class, rule, line[, basename])` (`key()` at 758), so none of these can ever turn a suite red.

**F1 — the redaction catch-all destroys evidence (92).**
`SECRET_PATTERNS` third entry `[A-Za-z0-9_\-]{32,}` matches any 32+ alphanumeric token, not just credentials.
Measured: `sudo git show 988b858bd6049bc709807534fd725c05264f7e60` → finding command
`"sudo git show <redacted>"`. That is exactly the 40-hex commit-SHA anchor class C1/C3 cite. Of 53 findings
across the 49 fixtures, 0 contain `<redacted>`, so the suites are blind to it. Recommendation: delete the
catch-all (patterns 1–2, userinfo and `AKIA…`, remain) or require mixed character classes and a `=`/`:`/`-p`
context. Not landed: this is a policy choice about credentials in findings, and it changes recorded output.

**F2 — `omarchy-*` substring match (70, 474).**
`any(k in argv0 for k in OMARCHY_MUTATE)` matches `"lock"` inside `clock`/`block`. Measured:
`omarchy-clock-format` → `host_mutation` rule `omarchy-clock-format`; `omarchy-blocklist` likewise. Whether
those verbs exist is unverified [INFERENCE]; the over-match mechanism is proven by tool output. A verb-prefix
match (`restart-`, `refresh-`, …, or exact verbs) would be the narrow form.

**F3 — `sp.getoutput` is a detection hole (82–86).**
`is_sub` accepts the `sp.` alias, but `getoutput`/`getstatusoutput` are only classified as shell strings when
spelled `subprocess.*`. Measured on one probe transcript:
`subprocess.getoutput('pacman -Syu')` → `pacman:-Syu` (caught);
`sp.getoutput('pacman -Syu')` → no finding (the arg goes through `shlex.quote`, becomes one token, matches
nothing).
Scratch variant `m_spawnfix` = P6 + add `sp.getoutput`, `sp.getstatusoutput` to `SHELL_STRING_FUNCS`: all three
suites stay green (`9/9 16/16 33/33`) and the probe now catches it; the differential run shows exactly the
intended `+1 host_mutation` in each of the five scan modes (13 comparisons, 5 diffs, all that finding). This is
the one change here that can turn a verdict red on a real transcript; it needs a fixture before landing.
C3's stated claims are unaffected either way.

**F4 — fixture blind spots (coverage, not a defect).**
Across the 49 fixture `bash` calls and 8 `eval` calls: bare `su` appears 0 times; backticks appear 0 times —
the backtick branch in `substitutions` is unpinned; `systemd-run` appears once; `>` and `<` appear once each,
and neither fixture result depends on redirect skipping (`cat > /tmp/note.md <<'EOF'` yields no finding either
way; `xargs -r pkill < pids` yields the same `pkill` class/rule, only a different `command` string, verified by
running `classify_shell` with the redirect-skipping branch removed). So P1 and the `su` half of P3 rest on code
proof + fuzz, not on fixtures.
If any of these deletions lands, three corpus additions would make the proof durable: a bare `su` case, a
backtick substitution case, and a *leading*-redirect case — `>/tmp/log sudo pacman -Syu` is detected today only
because `>` and its target are skipped (measured: the same predicate without skipping yields no finding at
all), and no fixture covers that shape.

## Preserved contract (unchanged by P1–P9)

CLI (`--scan PATH… [--permit CLASS…]`, `--selftest DIR`), first line
`MADO_TRIPWIRE: clean|permitted_only|findings|could_not_evaluate`, JSON schema
`mado-tripwire-verdict-v1` with the same keys, exit precedence 2 > 1 > 0, the three class names and every
rule string, per-toolCall dedupe on `(class, rule)`, `SELFTEST_SCRIPT_SHA256` emission, and every
classification (byte-identical verdicts over the fixture corpus). `SELFTEST_SUMMARY` counts are untouched.

## Tradeoff / landing notes

- Any edit changes the artifact sha `4ced68d3…`, which is recorded in
  `.ufo/waves/round-17/evidence/measure-c3.json` (committed-blob `sha256`) and printed inside
  `tripwire-selftest-{core,compound,hardening}.txt`; reports in this wave that quote that hash go stale.
  `measure.py` C3 is presence/bytes only, so it re-measures rather than rejecting a new hash, but the receipts
  must be re-cut (`python3 .ufo/waves/round-17/measure.py REV`) with the new selftest output.
- P7 and P8 each grow the file by a line or five. They remove duplicate authorities, not lines; if the metric is
  LOC alone, land P1–P6 + P9 (−4) and skip them.
- Deliberately not touched: `logical_lines` re-runs `shlex.split` on the growing accumulator (118–126, O(n²) in
  logical lines) and `substitutions` recounts `"` before each `'` (185, O(n²) in quotes). Replacing either
  needs a quote/comment-aware scanner; `# don't` currently works *because* shlex's `comments=True` is the
  oracle, so the obvious counter would regress. Keep and treat as a documented cost.
- Deliberately not touched: `classify_shell` calls `strip_prefix` a second time per segment (350) after
  `classify_segment` already did (369) — two list copies per segment; consolidating needs an API change with
  no semantic gain.
- Stop point: the next consolidation candidate — one `CALL_FORMS` table replacing `SPAWN_FUNCS` +
  `SHELL_STRING_FUNCS` + `is_exec` + `is_tool` (82–86, 551–554) — would rewrite `classify_eval` past what the
  eight fixture eval calls pin. I did not build it; the evidence base does not justify it yet.

## Evidence index (scratch only, `/tmp/simplify-tripwire.3092`)

`base.py`, `v1.py`, `v2.py`, `m_*.py`, `m_spawnfix.py`, `combined.py`, `build_variants.py` (hunk table with
assert-one-match guards), `fuzz.py`, `probe.py`, `final-base.json`, `final-combined.json`, `out-*.json`.
Nothing in the lane was written except this report.
