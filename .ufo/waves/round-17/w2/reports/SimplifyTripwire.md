# SimplifyTripwire — `tools/mado-tripwire.py` deletion / simplification set (W2, report only)

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. **Installs: none.** No pacman/sudo/systemctl/
compositor/live probe, no omp CLI. No lane file was written except this report; every mutation ran on a copy
under `/tmp/simplify-tripwire.3092`.

## Artifacts — the file moved under this seat

| id | what | lines | sha256 |
|---|---|---|---|
| **A** | lane HEAD `988b858` blob (`git show HEAD:tools/mado-tripwire.py`) | 818 | `4ced68d3…d4c44` |
| **B** | current worktree file (uncommitted, +132/−37 vs HEAD, mtime 2026-10-20 12:06:29) | 913 | `7a98720e…f31fe7` |

A was the file on disk when this seat opened and the artifact C3 claimed. Mid-seat another seat landed an
uncommitted edit that adds alias normalization (`aliases` at 590–610), comment/punctuation handling in
`segments` (177–190), pacman long-option prefixes (353–357), `nested_eval`/`NESTED` counters (105–111), and
extra rule-table entries. HEAD is still `988b858`.

Both artifacts were measured. **Line numbers below are B** (`7a98720e`); the hunk *text* is the authority and
will survive the next line shift. Re-anchor on the hash before landing.

## Verdict

Nine hunks are **output-identical**; P11 is a **behavioural fix** (a revert of a worktree regression) that
changes only quoted or escaped `#` inputs. All ten keep the three suites green:

- On B: P1–P9 → 913 → 910 lines, full verdict JSON byte-identical on all 49 regular fixtures, 13/13
  differential comparisons identical. Adding P11 → 908 lines, suites green, 0/13 diffs on the standing
  corpus, and the intended deltas appear only on the new comment probe (`echo '# x'; …`, `echo \# x; …`).
- On A: the same nine hunks → 818 → 816 lines, 13/13 identical, byte-identical fixture verdicts. (A's P7
  additionally hoisted a per-argument `long_ops` rebuild that B has already fixed.)

The attack on the C3 landing (9/9, 16/16, 33/33, anchor exit 1, 4/4 pacman.log join) **failed**: P1–P9 do not
change a single classification. What the suites cannot see is documented under Findings: the redaction
catch-all still destroys commit-SHA evidence (F1) and the `omarchy-*` substring rule still fires on
`clock`/`block` (F2); the `sp.getoutput` hole I found at A is **already fixed in B** (F3, historical).

## Method

- Baseline on each artifact: `python3 -I <copy> --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening}`
  → `9/9`, `16/16`, `33/33`.
- Differential harness: one synthetic transcript with 156 `bash` calls, 25 `eval` calls (literal, non-literal,
  `!`-bang, `%%bash`, heredocs, `await tool.bash`, JS, malformed) and three non-toolCall record shapes; scanned
  five ways (file, directory, three `--permit` sets) and through eight refusal paths (missing path, non-`.jsonl`,
  empty dir, bad/empty permit, no path, usage, refused name). 13 byte-exact stdout+exit comparisons per mutant.
- Stronger check: scan of the 49 regular fixture files (`core` 6, `compound` 13, `hardening` 32 at maxdepth 1,
  excluding `malformed.jsonl`, `agent.db.jsonl`, the symlink fixture — those are the suites' exit-2 cases)
  compared with `cmp`. B baseline: 53 findings, counts `host_mutation 34 / live_probe 6 / package_query 13`,
  exit 1.
- Every proposal was also built and measured **alone** (per-row table below), not only in the combined patch.
- A six-line comment probe (`commentprobe.jsonl`) covers comment-only, trailing-comment, quoted-`#`,
  escaped-`#` and `a#b` lines; used for P11 and F4.
- Hunk builder asserts exactly one match per hunk (`build_now.py`), so a later edit fails loudly instead of
  applying to the wrong site.

## Proposals (line numbers on B `7a98720e`; apply bottom-up)

| # | Lines | What | Δ lines | Nature |
|---|-------|------|---------|--------|
| P1 | 50, 187 | drop `REDIRECTS` + its disjunct (generic punctuation clause already covers every member) | −1 | dead constant |
| P2 | 182 | drop `or tok == "\n"` — `"\n"` is in `SEPARATORS` (49) | 0 | duplicate branch |
| P3 | 78 | drop `"systemd-run"`, `"su"` from `HOST_MUTATION_BINS` — shadowed by branches at 452/457 | 0 | dead table entries |
| P4 | 198, 202 | drop `in_single` (never assigned `True`) and its conjunct | −1 | dead state |
| P5 | 570 | drop `lines and` — `str.split("\n")` never returns `[]` | 0 | dead guard |
| P6 | 87–88 | drop `getoutput`/`getstatusoutput` from `SPAWN_FUNCS`; duplicated by `SHELL_STRING_FUNCS` 89–91 | −1 | duplicate table |
| P7 | 349–351, 355, 366–371 | one `PACMAN_LONG_OPS` + one `PACMAN_LONG_FLAGS` table; two flag spellings disappear | 0 | duplicate authority |
| P8 | 411–413, 467–473 | one `shell_code()` for the duplicated shell `-c` predicate | +5 | duplicate branch |
| P9 | 800–804, 876–880, 888–892, 894–898 | one `emit_failure()` for four copies of the exit-2 payload | −5 | duplicate payload |
| P10 | 578/580, 846–849, 851, 865 | nits, not applied | 0 | — |
| P11 | 166, 177–178 | restore `lex.commenters = "#"` and delete the post-token `#` break — A's mechanism | −2 | **fix**, not neutral |
| — | P1–P9 | 913 → 910 | **−3** | byte-identical |
| — | P1–P9+P11 | 913 → **908** (non-blank 849 → 840) | **−5** | suites green, one intended delta |

### P1 — `REDIRECTS` is subsumed (50, 187)

```diff
 SEPARATORS = {";", "&&", "||", "|", "&", "|&", ";;", "(", ")", "\n"}
-REDIRECTS = {">", ">>", "<", "<<", "<<<", ">&", "<&", ">|", "&>", "&>>", "<>"}
...
-        elif tok in REDIRECTS or (tok and set(tok) <= set("<>&|")):
+        elif tok and set(tok) <= set("<>&|"):
```

Every `REDIRECTS` member is a string over `<>&|` (and none is in `SEPARATORS`), so the generic clause is a
strict superset. Enumeration of all 399 strings over `<>&|;()` of length 1–3: `0` tokens where the two
predicates differ. The suites do not pin redirection skipping (F4), but it is load-bearing: `>/tmp/log sudo
pacman -Syu` is caught *only* because the redirect target is skipped (measured on B). Keep the generic clause;
delete the enumeration. The fuzz corpus exercises `>>`, `<`, `2>&1`, `<&0`, `&>>`, `>|`, `<>`, `&&>>`.

### P2 — duplicate newline test (182)

```diff
-        if tok in SEPARATORS or tok == "\n" or (tok and set(tok) <= set(";&|()") and
+        if tok in SEPARATORS or (tok and set(tok) <= set(";&|()") and
```

`SEPARATORS` (49) already ends in `"\n"`. The second (compound-punctuation) disjunct is *not* redundant —
`();` is not a `SEPARATORS` member — so keep it.

### P3 — two unreachable set members (78)

```diff
-                      "shutdown", "halt", "systemd-run", "su"}
+                      "shutdown", "halt"}
```

`classify_segment` returns at `if argv0 == "su":` (452) and `if argv0 == "systemd-run":` (457) before
`if argv0 in HOST_MUTATION_BINS:` (527), emitting the identical `("host_mutation", "su")` /
`("host_mutation", "systemd-run")` rule. `systemd-run` is pinned by `hardening/run0-and-systemd-run.jsonl`;
`su` has no fixture (F4) but stays pinned by fuzz lines 17–20.

### P4 — dead state (198, 202)

```diff
-    in_single = False
...
-        if ch == "'" and not in_single:
+        if ch == "'":
```

`in_single` has exactly one assignment in the file (198, `False`); nothing sets it `True`, so the conjunct is
constant-true. The function stays approximate by its own comment (204).

### P5 — dead guard (570)

```diff
-    if lines and lines[0].strip().startswith("%%bash"):
+    if lines[0].strip().startswith("%%bash"):
```

`str.split` never returns an empty list.

### P6 — duplicate spawn-table entries (87–88)

```diff
-SPAWN_FUNCS = {"run", "call", "check_call", "check_output", "Popen",
-               "getoutput", "getstatusoutput"}
+SPAWN_FUNCS = {"run", "call", "check_call", "check_output", "Popen"}
```

`subprocess.getoutput` / `subprocess.getstatusoutput` are in `SHELL_STRING_FUNCS` (89–91) and reach the same
`is_shell_fn` branch; B's alias normalization (590–610) means `sp.getoutput` is also caught either way.
Measured output-identical, including that alias.

### P7 — pacman option tables (349–351, 355, 366–371)

```diff
+ PACMAN_LONG_OPS = {"--sync": "S", "--query": "Q", "--remove": "R",
+                    "--upgrade": "U", "--database": "D", "--files": "F",
+                    "--deptest": "T", "--version": "V"}
+ PACMAN_LONG_FLAGS = {"--refresh": "y", "--sysupgrade": "u",
+                      "--downloadonly": "w", "--clean": "c",
+                      "--print": "p", "--search": "s", "--info": "i",
+                      "--list": "l", "--groups": "g"}
...
-    long_ops = {"--sync": "S", ...}                      # rebuilt per call
...
-            hits = [k for k in long_ops if k.startswith(name)] if len(name) > 3 else []
-                op = (a, long_ops[hits[0]])
+            hits = [k for k in PACMAN_LONG_OPS if k.startswith(name)] if len(name) > 3 else []
+                op = (a, PACMAN_LONG_OPS[hits[0]])
...
-        elif a in ("--refresh", "--sysupgrade", "--downloadonly", "--clean"):
-            flags.add({"--refresh": "y", "--sysupgrade": "u",
-                       "--downloadonly": "w", "--clean": "c"}[a])
-        elif a in ("--print", "--search", "--info", "--list", "--groups"):
-            flags.add({"--print": "p", "--search": "s", "--info": "i",
-                       "--list": "l", "--groups": "g"}[a])
+        elif a in PACMAN_LONG_FLAGS:
+            flags.add(PACMAN_LONG_FLAGS[a])
```

Today each long flag is spelled twice (membership tuple + mapping literal), and `long_ops` is rebuilt on every
`classify_pacman` call. Net 0 lines on B; value is one table per concept. If LOC is the only axis, skip.

### P8 — duplicated shell `-c` predicate (411–413, 467–473)

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

Two independent spellings of one question ("does this shell carry inline code"), which can drift. The tuple
keeps the `bash -c` with no argument edge exact. +5 lines; skip if LOC is the only axis.

### P9 — four copies of the exit-2 payload (800–804, 876–880, 888–892, 894–898)

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

Identical keys and `sort_keys=True`, so bytes are unchanged; the eight refusal comparisons cover all four
sites. Leave the `__main__` internal-error payload alone (deliberately smaller shape).

### P10 — nits (not applied; zero behaviour change)

- 578/580: the leading indentation is recovered twice with `re.match(r"^\s*", ln)`; capture it in the first
  pattern (`^(\s*)(?:…)?!(.*)$`) and reuse group 1.
- 851: `first_ok = out[0].startswith(...) if out else False` — `split("\n")` never returns `[]`; guard is dead.
- 846–849: `key()` nests a `use_file` conditional inside a `from_want` conditional; early-return on
  `not use_file` is the same tuple and reads better.
- 865: `hashlib.sha256(open(me, "rb").read())` leaks the handle; use `with open(...)`.

### P11 — comment handling lost quote context (166, 177–178) — behavioural fix

B sets `lex.commenters = ""` (166) and re-implements comments *after* tokenization by breaking on any token
that starts with `#` (177–178). Post-shlex there is no quote or escape information left, so a quoted or
escaped `#` is treated as a comment and truncates the rest of the line. A did it correctly: `commenters = "#"`,
no branch. Measured on one probe transcript:

| command | A | B (`7a98720e`) | branch deleted only | B + P11 |
|---|---|---|---|---|
| `# comment; sudo pacman -Syu` | clean | clean | **false positive** (sudo, pacman) | clean |
| `echo '# x'; pacman -Syu` | `pacman:-Syu` | **missed** | `pacman:-Syu` | `pacman:-Syu` |
| `echo \# x; pacman -Syu` | `pacman:-Syu` | **missed** | `pacman:-Syu` | `pacman:-Syu` |
| `pacman -Qq # trailing; sudo pacman -Syu` | only `pacman:-Qq` | only `pacman:-Qq` | **false positive** (sudo, pacman) | only `pacman:-Qq` |

```diff
 def tokenize(line):
     ...
-    lex.commenters = ""  # '#' is a comment only at word start: handled in segments()
+    lex.commenters = "#"
...
-        if tok.startswith("#"):
-            break  # comment to end of line (a word starting with '#')
```

Deleting only the branch is **wrong** — measured: comment-only and trailing-comment lines then produce
findings. The pair restores A's exact behaviour on every probe line. Suites stay `9/9 16/16 33/33`; the standing
differential corpus shows 0/13 diffs; the only classification changes are the two quoted/escaped-`#` cases
above, both restorations of A. This is a worktree regression, not a C3 claim. Land with fixtures:
`echo '# x'; pacman -Syu` expect `host_mutation pacman:-Syu`; `# comment; sudo pacman -Syu` expect clean.

## Measured equivalence (artifact B, `7a98720e`)

Every proposal alone: `9/9 16/16 33/33`, `13 comparisons, 0 diffs`.

| proposal | Δ lines | suites | differential |
|---|---|---|---|
| P1 | −1 | green | 0/13 |
| P2 | 0 | green | 0/13 |
| P3 | 0 | green | 0/13 |
| P4 | −1 | green | 0/13 |
| P5 | 0 | green | 0/13 |
| P6 | −1 | green | 0/13 |
| P7 | 0 | green | 0/13 |
| P8 | +5 | green | 0/13 |
| P9 | −5 | green | 0/13 |
| P11 | −2 | green | 0/13 (intended deltas only on quoted/escaped `#`; comment lines stay clean) |
| P1–P9 | −3 (910) | green | 0/13 |
| P1–P9+P11 | −5 (908) | green | 0/13 |

Combined P1–P9: full verdict over the 49 fixtures `cmp`-identical to B (exit 1, 53 findings, counts
34/6/13); `py_compile` clean. Combined P1–P9+P11: same suites, and the only measured classification changes
are the quoted/escaped-`#` restorations above.

Artifact A (`4ced68d3`, 818 lines) was measured the same way before the drift: nine hunks → 816 lines,
`9/9 16/16 33/33`, 13/13 identical, `cmp`-identical over the same 49 files. A's P7 also removed a
per-iteration `long_ops` rebuild that B already hoisted.

## Findings the suites cannot see

The suites compare only `(class, rule, line[, basename])` (`key()` at 846), so none of these can turn a suite
red. Each is a concrete counterexample measured on B.

**F1 — redaction catch-all destroys evidence (96).**
`SECRET_PATTERNS` still ends with `[A-Za-z0-9_\-]{32,}`. Measured:
`sudo git show 988b858bd6049bc709807534fd725c05264f7e60` → finding command `"sudo git show <redacted>"` —
i.e. the exact SHA anchor class C1/C3 cite. 0 of 53 fixture findings contain `<redacted>`, so the corpus is
blind. Recommendation: delete the catch-all (userinfo and `AKIA…` patterns remain) or require mixed character
classes plus credential context. Not landed: it is a policy call and changes recorded output.

**F2 — `omarchy-*` substring match (72–75, 533–534).**
`any(k in argv0 for k in OMARCHY_MUTATE)` matches `"lock"` inside `clock`/`block`. Measured on B:
`omarchy-clock-format` and `omarchy-blocklist` → `host_mutation`. Whether those verbs exist is unverified
[INFERENCE]; the over-match is proven. The list has grown to 25 substrings, so the surface widened since A.
A verb-prefix match would be the narrow form.

**F3 — `sp.getoutput` (historical; fixed in B).**
At A, `subprocess.getoutput('pacman -Syu')` → `pacman:-Syu` but `sp.getoutput('pacman -Syu')` → no finding
(the string went through `shlex.quote`, becoming one token). B normalizes import aliases (590–610), and the
probe now yields `pacman:-Syu`. No action; recorded so the A→B delta is not mistaken for a suite-driven fix.

**F4 — fixture blind spots (coverage, not a defect).**
Across the 49 fixture `bash` calls and 8 `eval` calls: bare `su` 0 occurrences; backticks 0 (the backtick
branch in `substitutions` is unpinned); `systemd-run` 1; `>` and `<` 1 each, and neither fixture result
depends on redirect skipping. A *leading* redirect does: `>/tmp/log sudo pacman -Syu` is caught only because
`>` and its target are skipped (measured; without skipping the predicate yields no finding). No fixture
contains a quoted or escaped `#`, which is why B's `segments`/`tokenize` change (P11) regressed a case A
handled without any suite turning red. If P1/P11 land, add: (a) a bare `su` case, (b) a backtick substitution
case, (c) the leading-redirect case, (d) `echo '# x'; pacman -Syu` → `pacman:-Syu` and
`# comment; sudo pacman -Syu` → clean.

## Preserved contract (unchanged by P1–P9)

CLI (`--scan PATH… [--permit CLASS…]`, `--selftest DIR`), first line
`MADO_TRIPWIRE: clean|permitted_only|findings|could_not_evaluate`, JSON schema `mado-tripwire-verdict-v1`
with the same keys, exit precedence 2 > 1 > 0, class names and every rule string, per-toolCall dedupe on
`(class, rule)`, `SELFTEST_SCRIPT_SHA256` output, and every classification (byte-identical verdicts).
`SELFTEST_SUMMARY` counts unchanged. P11 is the only intentional behaviour change: it restores A's comment
handling and only affects lines containing a quoted or escaped `#`.

## Landing notes / tradeoffs

- **Re-anchor first.** B is an uncommitted 913-line worktree owned by another seat; if it moves again the
  hunk strings still apply (the builder asserts one match each) but the line numbers in this report will not.
  Land against the settled revision, then re-run `--selftest` on all three suites and this report's hunk table.
- Any edit changes the tool sha. A's `4ced68d3…` is recorded in `.ufo/waves/round-17/evidence/measure-c3.json`
  and printed in the three `tripwire-selftest-*.txt` receipts; re-cut those receipts with the new
  `SELFTEST_SCRIPT_SHA256` (`python3 .ufo/waves/round-17/measure.py REV`). `measure.py` C3 is presence/bytes
  only, so it re-measures rather than rejecting a new hash. Reports in this wave that quote the old hash
  become stale.
- P7/P8 are structural, not LOC wins (+0/+5). If the metric is lines alone, land P1–P6 + P9 + P11 (−5) and
  skip them.
- Deliberately not touched: `logical_lines` re-runs `shlex.split` on the growing accumulator (O(n²) in logical
  lines) and `substitutions` recounts `"` before each `'` (O(n²) in quotes). A replacement needs a
  quote/comment-aware scanner; `logical_lines`' `shlex.split(comments=True)` is the oracle that keeps
  `# don't` balanced. Keep and document.
- Deliberately not touched: `classify_shell` calls `strip_prefix` twice per segment (once inside
  `classify_segment`, once for the `base` test) — two list copies per segment, no semantic gain in fixing.
- `NESTED`/`nested_eval` (105–111, 423, 479, 746, 761–762) is live, not dead: it is reset per file and folded
  into `eval_unparsed`/`unparsed_spawns`. Not a deletion target.
- Stop point: the next candidate — one `CALL_FORMS` table replacing `SPAWN_FUNCS` + `SHELL_STRING_FUNCS` +
  `is_exec` + `is_tool` — would rewrite `classify_eval` past what the eight eval fixtures pin. Not built; the
  evidence base does not justify it.

## Evidence index (scratch only, `/tmp/simplify-tripwire.3092`)

`base.py` (A), `now.py` (B), `combined.py` (A, P1–P9), `combined_now.py` (B, P1–P9), `p11b.py` and
`combined_now3.py` (B, P1–P9+P11), `combined_now2.py` (rejected branch-only P11), `one_P*.py`,
`build_variants.py`, `build_now.py` (hunk tables with one-match assertions), `fuzz.py`, `probe.py`,
`commentprobe.jsonl`, `quotedhash.jsonl`, `now-base.json`, `now-combined.json`, `final-*.json`.
Lane state at report time: `tools/mado-tripwire.py` = `7a98720e…` (worktree), HEAD `988b858` blob =
`4ced68d3…`. Nothing in the lane was written except this report.
