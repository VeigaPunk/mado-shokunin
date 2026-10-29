# R56W2MutC1Harness — mutation test of `quality/r56_ctl_c1.py` at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`

Seat: R56W2MutC1Harness (wave 2, falsify). Subject: the C1 control harness (`quality/r56_ctl_c1.py`, 632 lines, the twelve
controls of `registration.md` §C1 as amended by `registration-v2.md` E5, the good-tree judgement, the denominator). The
counter under test is `quality/counters/c1-r56-autoreload-entry.py` at the same revision (git blob `5290d681…`, read via `git archive`). Nothing in the lane was edited; every mutant lives in a copy under
`/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness/` (removed before yield, copied here first).

## Result in one table

| measure | value |
|---|---|
| mutants (one-line edits of a copy of the harness module) | 66 |
| oracle runs per mutant (battery) | 40 (listed below) |
| killed (stdout or exit status differs from the pristine harness) | 44 = 66.7% of all |
| … of which killed by the three oracles the spec names (real counter, always-green stub, reject-all stub) | 25 |
| argued equivalent (no oracle differs; reason in the table) | 15 |
| diagnostic-only (stderr notes or print width; verdict identical; not a control defect) | 2 |
| verdict-relevant, non-equivalent | 49 |
| kill rate excluding equivalent | 86.3% (44/51) |
| kill rate excluding equivalent and diagnostic (the honest denominator) | 89.8% (44/49) |
| spec-only oracles on the honest denominator | 51.0% (25/49) |
| verdict-level survivors (wrong-reason controls) | 5: M23, M24, M25, M58, M60 |
| with P1 (pinned missed sets) — the five verdict-level survivors killed (verified); the other 44 are killed by the battery already | 5 of 5 survivors killed |

Read the honest denominator, not the all-mutant rate. Two numbers the frozen battery does not reach on its own:
the three spec oracles kill half of the verdict-relevant mutants; the rest need the extra oracles and fixtures below.

## Oracle battery (40 runs per mutant)

- `real`: the real counter exported at the revision, run through the unchanged harness (no `--counter`).
- `stub_green` (always green, TARGET_MET with the full counts), `stub_reject` (TARGET_MISSED, `index`), `stub_kitchen`
  (TARGET_MET with every registered leg, rc 1). The first two are the spec's oracles; the third is mine.
- 21 further stubs (`stub_legonly_*`, one leg each, with the count of controls each should pass pre-computed from the
  control table; `stub_malformed_leg`, `stub_newrows390`, `stub_green{badrev,badcount,missed}`).
- 9 wrappers `w_*` that run the REAL counter and forge one property: rev, exit 0 on a miss, exit 2 on a miss, duplicate
  stdout line, stderr noise on a green run, content 33/33, verdict word `TARGET_MAYBE`, rows denominator `/31`, and the
  good tree alone broken (`w_goodonly`). `w_stderr` is benign and the pristine harness correctly scores it `12/12 OK`
  (the registration only mandates "reason on stderr" on the exit-2 path).
- 6 variant trees (good tree with one entry edit): fenced copy of K05 (`var_fence3`), 4-space fence (`var_fence4`),
  `~~~` fence containing a ```` ``` ```` line (`var_tilde`), duplicated K05 row (`var_dupK05`), closed HTML comment on K05
  (`var_comment`), K05 with a sixth cell (`var_6cell`).
- Pristine expectations, checked: real `good=ok controls=12/12 verdict=OK`, rc 0; green `good=ok controls=0/12 verdict=FAIL`;
  reject `good=bad controls=0/12 verdict=FAIL`. Deterministic across two runs (stdout and stderr byte-identical).
- Classification: KILLED if stdout or exit status differs from the pristine run of the same oracle (SHA values in
  stderr normalized to `<SHA>`, since scratch commits are timestamped); DIAG if only stderr differs; SURVIVED otherwise.

Fixtures added after the battery (run in `extra_variants.py`, differential against pristine):
`var_srcline2` (the `source:` line moved to line 2) kills M63; `var_pinlink` (the pinned `Hyprland-ConfigWatcher.cpp` made a
symlink) kills M15 and M16.

## Mutants and their outcomes

Each row is one line of a copy of `quality/r56_ctl_c1.py`. Multi-line `old` anchors (M21, M40, M44, M45) exist only for
uniqueness; the replacement changes one line. The `old` text occurs exactly once in the pristine module (asserted by
`drive.py`). M26 changes a constant inside the appended proposition text.

| id | kind | edit (old → new) | outcome | killing oracle / argument |
|---|---|---|---|---|
| M01 | constant | CHILD_TIMEOUT = 120 → CHILD_TIMEOUT = 1 | equivalent (argued) | E-host: CHILD_TIMEOUT=1s never fires on this host (unloaded counter run 0.18 s; no TIMEOUT rc in any receipt); a slow-host hazard, not a control weakness. |
| M02 | constant | N_CONTROLS = 12 → N_CONTROLS = 11 | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=12/11 verdict=FAIL |
| M03 | constant | "content": 33, "new": 8} → "content": 32, "new": 8} | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=bad controls=12/12 verdict=FAIL |
| M04 | regex | (?P<verdict>TARGET_MET\|TARGET_MISSED) → (?P<verdict>TARGET_MET\|TARGET_MISSED\|[A-Z_]+) | killed (extra oracle) | first differing oracle: `w_verdictword`. pristine: good=ok controls=0/12 verdict=FAIL \| mutant: good=ok controls=12/12 verdict=OK |
| M05 | regex | (?P<missed>\S+)$" → (?P<missed>\S*)$" | equivalent (argued) | E-general: an empty missed= field reaches LEG_RE as [''] (rejected) instead of failing LINE_RE; both paths return an error and no control is admitted; stdout identical. |
| M06 | regex | rows=(?P<rows>\d+)/30 hosts → rows=(?P<rows>\d+)/\d+ hosts | killed (extra oracle) | first differing oracle: `w_denom`. pristine: good=bad controls=0/12 verdict=FAIL \| mutant: good=ok controls=12/12 verdict=OK |
| M07 | dropped-leg | \|index\|pin_hash\|new_rows → \|index\|new_rows | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M08 | regex | [KH][0-9]{2})$" → [KH][0-9]{1,2})$" | killed (extra oracle) | first differing oracle: `stub_malformed_leg`. pristine: good=bad controls=0/12 verdict=FAIL \| mutant: good=bad controls=1/12 verdict=FAIL |
| M09 | regex | ROW_RE = re.compile(r"^\\|\s*([KH][0-9]{2}) → ROW_RE = re.compile(r"^\\|\s*([K][0-9]{2}) | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=10/12 verdict=FAIL |
| M10 | regex | (S[0-9]{3,}) → (S[0-9]{4,}) | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=9/12 verdict=FAIL |
| M11 | regex | FENCE_RE = re.compile(r"^ {0,3}(```\|~~~)") → FENCE_RE = re.compile(r"^ {0,4}(```\|~~~)") | killed (extra oracle) | first differing oracle: `var_fence4`. pristine: good=bad controls=9/12 verdict=FAIL \| mutant: good=bad controls=12/12 verdict=FAIL |
| M12 | operator | if out.strip(b"\0"): → if out: | equivalent (argued) | E-general: `git ls-tree -z` prints nothing for an absent path and a record for a present one, so `if out:` and `if out.strip(b"\0"):` agree on every git output. |
| M13 | order | present = sorted(ls_present(work, repo, rev, paths)) → present = list(ls_present(work, repo, rev, paths)) | equivalent (argued) | E-general: pathspec order to `git archive` does not change the archived tree. |
| M14 | inverted |     if not present: →     if False: | equivalent (argued) | E-accepted-input: `present` cannot be empty: TABLES_PATH must be a regular blob at REV or Setup raises before the export. |
| M15 | flag | symlinks=True, dirs_exist_ok=True → symlinks=False, dirs_exist_ok=True | killed (fixture) | fixture `var_pinlink` |
| M16 | inverted | if p.is_symlink() or not p.is_file(): → if not p.is_file(): | killed (fixture) | fixture `var_pinlink` |
| M17 | inverted |     if lines == before: →     if False: | equivalent (argued) | E-general: a no-op mutation yields the good tree, which scores TARGET_MET, so the control prints 'mutant admitted' (FAIL) exactly as the pristine MutationError does; zero 'changed nothing' lines in pristine stderr. |
| M18 | operator | if m and m.group(1) == fence: → if m: | killed (extra oracle) | first differing oracle: `var_tilde`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=9/12 verdict=FAIL |
| M19 | dropped-leg | rows.setdefault(r.group(1), []).append(i) → rows.setdefault(r.group(1), []) | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=5/12 verdict=FAIL |
| M20 | operator | if k >= 0 and l.find("-->", k) < 0: → if k >= 0: | killed (extra oracle) | first differing oracle: `var_comment`. pristine: good=bad controls=11/12 verdict=FAIL \| mutant: good=bad controls=6/12 verdict=FAIL |
| M21 | off-by-one | hits = entry_rows(lines).get(rid, [])\n    if len(hits) !... → hits = entry_rows(lines).get(rid, [])\n    if len(hits) < 1: | killed (extra oracle) | first differing oracle: `var_dupK05`. pristine: good=bad controls=9/12 verdict=FAIL \| mutant: good=bad controls=10/12 verdict=FAIL |
| M22 | off-by-one |     if len(cells) != 5: →     if len(cells) < 5: | killed (extra oracle) | first differing oracle: `var_6cell`. pristine: good=bad controls=9/12 verdict=FAIL \| mutant: good=bad controls=12/12 verdict=FAIL |
| M23 | operator | return "\| " + " \| ".join(cells) + " \|" → return "\| " + " \|".join(cells) + " \|" | SURVIVED verdict, wrong reason | stdout/rc identical; stderr differs (wrong-reason legs) |
| M24 | operator | if rid.startswith("K"): → if rid.startswith("Z"): | SURVIVED verdict, wrong reason | stdout/rc identical; stderr differs (wrong-reason legs) |
| M25 | dropped-leg | rows = entry_rows(lines)\n    for rid in ctx["k_ids"] + c... → rows = entry_rows(lines)\n    for rid in ctx["k_ids"]: | SURVIVED verdict, wrong reason | stdout/rc identical; stderr differs (wrong-reason legs) |
| M26 | constant | " The value is capped at 200 by this call." → " The value is capped at 2 by this call." | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M27 | swapped | cells[2] = "S385" → cells[2] = "S384" | equivalent (argued) | E-class: S384 is another pin's row, as S385 is; both produce legs source_cell:K10,scope:K10 (identical receipts). |
| M28 | constant | cells[5] = " ConfigWatcher.cpp:1-10 " → cells[5] = " ConfigWatcher.cpp:1-100 " | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M29 | constant | cells[7] = " mined " → cells[7] = " candidate " | equivalent (argued) | E-class: the mutated status is on the injected S399 row; source_cell:K10 already fails on the sid mismatch and scope_covers reads only cells[5] (counter line 483), so status cannot change legs. |
| M30 | dropped-leg | del lines[_row(lines, "K17")] → del lines[_row(lines, "K16")] | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M31 | operator | cells[4] = q[:-2] + ("." if last != "." else ",") + "`" → cells[4] = q[:-2] + "x`" | equivalent (argued) | E-class: any one-character change to the frozen K05 quote breaks quote identity; legs quote:K05,row:K05 either way. |
| M32 | operator | nb = data[0] ^ 0x01 → nb = data[0] ^ 0x03 | equivalent (argued) | E-class: any single-byte change of a pinned file flips its sha256; pin_hash is the only leg. |
| M33 | dropped-leg | REG_RE.match(l).group(1) == "S390"] → REG_RE.match(l).group(1) == "S391"] | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M34 | constant | cells[5] = " ConfigWatcher.cpp:1-9999 " → cells[5] = " ConfigWatcher.cpp:1-100 " | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M35 | constant | cells[5] = " ConfigWatcher.cpp:1-9999 " → cells[5] = " ConfigWatcher.cpp:1-9998 " | equivalent (argued) | E-class: 1-9998 and 1-9999 are both past the 111-line pin, so the E3 bound fails for both. |
| M36 | vacuous |     _reg(d, ctx["entry"]).unlink() →     _reg(d, ctx["entry"]) | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M37 | inverted | if not any(l.startswith("echo:") for l in rec["legs"]): → if False: | killed (spec oracle) | first differing oracle: `stub_legonly_entryabsent`. pristine: good=bad controls=1/12 verdict=FAIL \| mutant: good=bad controls=2/12 verdict=FAIL |
| M38 | off-by-one | if rec["content"] >= 33: → if rec["content"] >= 34: | killed (extra oracle) | first differing oracle: `w_content`. pristine: good=ok controls=11/12 verdict=FAIL \| mutant: good=ok controls=12/12 verdict=OK |
| M39 | dropped-leg | if not any(l.startswith("tok:") for l in rec["legs"]): → if False: | killed (spec oracle) | first differing oracle: `stub_legonly_echoK01`. pristine: good=bad controls=1/12 verdict=FAIL \| mutant: good=bad controls=2/12 verdict=FAIL |
| M40 | inverted |     if rec["rev"] != sha:\n        return "rev=%s, passed... →     if False:\n        return "rev=%s, passed %s" % (rec[... | killed (extra oracle) | first differing oracle: `w_rev`. pristine: good=bad controls=0/12 verdict=FAIL \| mutant: good=bad controls=12/12 verdict=FAIL |
| M41 | inverted |     if rec["verdict"] == "TARGET_MET":\n        return "v... →     if False:\n        return "verdict=TARGET_MET (mutant... | killed (extra oracle) | first differing oracle: `stub_kitchen`. pristine: good=bad controls=0/12 verdict=FAIL \| mutant: good=bad controls=11/12 verdict=FAIL |
| M42 | off-by-one |     if rc != 1: →     if rc not in (1, 2): | killed (extra oracle) | first differing oracle: `w_rc2`. pristine: good=ok controls=0/12 verdict=FAIL \| mutant: good=ok controls=12/12 verdict=OK |
| M43 | inverted | if got != GOOD_COUNTS: → if got == GOOD_COUNTS: | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=bad controls=12/12 verdict=FAIL |
| M44 | inverted |     if rc != 0:\n        return "exit status %s, need 0" ... →     if rc == 0:\n        return "exit status %s, need 0" ... | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=bad controls=12/12 verdict=FAIL |
| M45 | removed-guard |     if err:\n        return err\n    if rec["rev"] != sha... →     if False:\n        return err\n    if rec["rev"] != s... | killed (extra oracle) | first differing oracle: `stub_malformed_leg`. pristine: good=bad controls=0/12 verdict=FAIL \| mutant:  |
| M46 | operator | if rec["verdict"] != "TARGET_MET" or rec["missed"] != "no... → if rec["verdict"] != "TARGET_MET" and rec["missed"] != "n... | killed (extra oracle) | first differing oracle: `stub_greenmissed`. pristine: good=bad controls=0/12 verdict=FAIL \| mutant: good=ok controls=0/12 verdict=FAIL |
| M47 | operator | verdict = "OK" if good_ok and passed == N_CONTROLS and le... → verdict = "OK" if good_ok or passed == N_CONTROLS and len... | killed (spec oracle) | first differing oracle: `stub_green`. pristine: good=ok controls=0/12 verdict=FAIL \| mutant: good=ok controls=0/12 verdict=OK |
| M48 | off-by-one |     if len(lines) != 1: →     if len(lines) < 1: | killed (extra oracle) | first differing oracle: `w_dup`. pristine: good=bad controls=0/12 verdict=FAIL \| mutant: good=ok controls=12/12 verdict=OK |
| M49 | operator | legs = [] if missed == "none" else missed.split(",") → legs = [] if missed == "none" else missed.split(";") | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=4/12 verdict=FAIL |
| M50 | removed-guard | if missed != "none" and not all(LEG_RE.match(x) for x in ... → if False: | killed (extra oracle) | first differing oracle: `stub_malformed_leg`. pristine: good=bad controls=0/12 verdict=FAIL \| mutant: good=bad controls=1/12 verdict=FAIL |
| M51 | swapped | why = judge_control(sha, rc, rec, err, check) → why = judge_control(sha, rec, rc, err, check) | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant:  |
| M52 | swapped | lambda dd, m=mut: m(dd, ctx) → lambda dd, m=mut: m(ctx, dd) | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant:  |
| M53 | dropped-leg | [ctx["entry"], TABLES_PATH, ctx["pin_dir"], *EXTRA_PATHS] → [ctx["entry"], TABLES_PATH, ctx["pin_dir"]] | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=bad controls=9/12 verdict=FAIL |
| M54 | order | random.SystemRandom().shuffle(order) → pass | equivalent (argued) | E-general: control order affects no result (each control runs in its own scratch repo; the log prints canonically). |
| M55 | removed-guard |     if leg == required or leg in collateral: →     if leg == required: | diagnostic only | stderr note/print width only |
| M56 | constant | def _clip(legs: list, n: int = 8) -> str: → def _clip(legs: list, n: int = 1) -> str: | diagnostic only | stderr note/print width only |
| M57 | operator | if len(ctx["k_ids"]) != 30 or len(ctx["h_ids"]) != 3: → if len(ctx["k_ids"]) != 30 and len(ctx["h_ids"]) != 3: | equivalent (argued) | E-accepted-input: frozen-tables-v2.json is hash-pinned (TABLES_SHA256 check raises first), so k=30 and h=3 for every accepted input; `and` and `or` agree. |
| M58 | off-by-one | len(q) - 2 >= 30: → len(q) - 2 >= 31: | SURVIVED verdict, wrong reason | stdout/rc identical; stderr differs (wrong-reason legs) |
| M59 | constant | " echoed on this line, no analysis added here" → " echoed on this line, no analysis added here." | equivalent (argued) | E-class: a trailing full stop changes no identifier, number or quote containment that the counter tests. |
| M60 | dropped-leg | cells[1] = "placeholder host proposition %s, not a read" ... → cells[1] = "placeholder host proposition, not a read" | SURVIVED verdict, wrong reason | stdout/rc identical; stderr differs (wrong-reason legs) |
| M61 | swapped | _need("row:K17") → _need("row:K16") | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M62 | swapped | m_junk, "tok:<id> + content<33", _need_junk, () → m_junk, "tok:<id> + content<33", _need_echo, () | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M63 | constant | hits = [i for i, l in enumerate(lines[:15]) if l.startswi... → hits = [i for i, l in enumerate(lines[:1]) if l.startswit... | killed (fixture) | fixture `var_srcline2` |
| M64 | constant |     lines[hits[0]] = lines[hits[0]] + ", S999" →     lines[hits[0]] = lines[hits[0]] + ", S383" | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |
| M65 | operator | rel = ctx["pin_dir"] + "/Hyprland-ConfigWatcher.cpp" → rel = ctx["pin_dir"] + "/Hyprland-ConfigValues.cpp" | equivalent (argued) | E-class: the pinned file is ConfigValues.cpp instead of ConfigWatcher.cpp; both are pinned, pin_hash is the only leg. |
| M66 | dropped-leg | row[2] = "S399" → row[2] = "S383" | killed (spec oracle) | first differing oracle: `real`. pristine: good=ok controls=12/12 verdict=OK \| mutant: good=ok controls=11/12 verdict=FAIL |

## Survivors, in full

### W — verdict-level survivors (controls still `ok`, for the wrong reason). Non-equivalent.

- **M23** `_join` separator `" | "` → `" |"`. Every row the harness rewrites becomes malformed, so the counter reports
  `row:<id>` for rows the control never touched: control 2 misses `row:K01…` (+57 more), control 3 misses `row:K04,num:K04`.
  Verdict unchanged. *Proposal P3* (row-grammar legs only for the mutated row) → `controls=7/12`, verified.
  *P1* → `7/12`, verified.
- **M24** junk text for K rows changed from `placeholder proposition text …` to `placeholder host proposition K.., not a
  read`. Stronger, not weaker: it exposes a hole in the frozen control 2. The pristine junk text shares the identifier
  `source` with K23's quote (`source= skipping directory {}`), so K23 gets no `tok:` leg. Pristine control 2 pins 32 of 33
  tok legs; M24 pins 33. Verdict unchanged. *P1* → `11/12`, verified. The root-cause fix (token-disjoint junk text, the
  M24 text) is verified by the M24 receipts: 33/33 tok legs, verdict unchanged.
- **M25** junk applied to K rows only (`for rid in ctx["k_ids"]`). Control 2 no longer asserts that H01–H03 are unreadable.
  Verdict unchanged. *P4* (`tok:H01`, `tok:H02`, `tok:H03` required in control 2) → `controls=11/12`, verified (the pristine
  run keeps `12/12`). *P1* → `11/12`, verified. M24 is not killed by P4 (correct: it flags H rows too).
- **M58** quote-echo threshold `>= 30` → `>= 31`. K07's quote is exactly 30 characters, so K07 is not echo-mutated, and
  control 11 still passes on the other rows. *P2* (`echo:K07` required in control 11) → `controls=11/12`, verified. *P1* → `11/12`.
- **M60** H placeholder text identical for every H row (`"placeholder host proposition, not a read"`). Duplicate
  propositions make the counter report `row:H01,row:H02,row:H03`. Verdict unchanged. *P3* → `11/12`, verified. *P1* → `11/12`.

### D — diagnostic only (not verdict-relevant)

- **M55** `_expected_leg` collateral allowance removed; affects only the `note:` line on stderr.
- **M56** `_clip` width 8 → 1; affects only how many legs are printed.
  Neither changes a control's pass/fail. They are listed, not counted as survivors. P1 correctly does not kill them.

### E — equivalent (argued; every oracle identical)

- M01 (`CHILD_TIMEOUT` 120 → 1): the unloaded counter run takes 0.18 s; the battery ran 12 parallel jobs and no receipt has a
  TIMEOUT. A deadline hazard on a slow host, not a control weakness. Equivalent on this host only.
- M05, M12, M13, M17, M54: equivalent for every input (argument in the table).
- M14, M57: equivalent for every accepted input. M14: the tables file must be a regular blob before export. M57: the
  tables sha is checked first, so `k=30, h=3` always.
- M27, M29, M31, M32, M35, M59, M65: a different instance of the same defect class (another pin's row, another
  status, another quote character, another pinned file, another past-EOF number). The counter's legs are identical in
  every oracle.

M15, M16 and M63 were equivalent on the frozen tree but are not in general; they are killed by fixtures (above).

## Proposed additions, each verified

Every proposal is a text insertion into the harness module (`verify_props.py`). Verification means: (a) the pristine
harness with the addition still scores `good=ok controls=12/12 verdict=OK`, rc 0, on the real counter; (b) the survivor
with the addition scores FAIL on the same counter.

| proposal | what it adds | pristine | survivors killed (verified) | survivors not killed |
|---|---|---|---|---|
| P1 pinned missed sets | each control's full missed set must equal the one recorded from the pristine run on the real counter (`gold.json`) | 12/12 | M23 (7/12), M24 (11/12), M25 (11/12), M58 (11/12), M60 (11/12) | M55, M56 (diagnostic) |
| P2 `echo:K07` | control 11 must see the 30-character quote row's echo leg | 12/12 | M58 (11/12) | M23, M24, M25, M60 |
| P3 row locality | a control may report `row:` legs only for the row it mutates (7 → K17, 8 → K05) | 12/12 | M23 (7/12), M60 (11/12) | M24, M25, M58 |
| P4 H rows junked | control 2 must see `tok:H01..H03` | 12/12 | M25 (11/12) | M23, M24, M58, M60 |
| fixture `var_srcline2` | `source:` on line 2 (window-dependent) | 12/12 | M63 (11/12) | — |
| fixture `var_pinlink` | pinned `ConfigWatcher.cpp` is a symlink | 10/12 (good=bad) | M15 (good=ok, 12/12), M16 (11/12) | — |

Smallest per survivor: M58 → P2; M23, M60 → P3; M25 → P4; M24 → the token-disjoint junk text (root cause, verified by the
M24 receipts) or P1; M23/M58/M60 also by P1. The P1 golden is pinned to this counter's output, so a legitimate counter
change must regenerate it (maintenance cost, stated).

## Findings the survivors point to (not counted as kills)

1. **Control 2 has a lexical hole at K23** (verdict-neutral): the junk proposition shares `source` with K23's quote.
   Verified by `final_table.py` (`control2_no_tok_rows: ["K23"]`) and M24.
2. **Five controls pass on the wrong reason** (M23, M60, plus partial vacuity in M24, M25, M58): their verdict cannot tell
   a row-grammar fault or a duplicate-proposition fault from the intended defect.
3. **The registration's collateral lists are incomplete**: the pristine harness prints `note: collateral legs beyond the
   registered ones` for controls 4, 5, 7, 8, 10, 11, 12 (e.g., control 7 adds `source_cell:K17, scope:K17, tok:K17, num:K17,
   echo:K17`). Cosmetic for the verdict, a documentation gap for the registration.
4. **Stderr from the counter is not judged on a green run** (`w_stderr` → `12/12 OK`). The registration does not require it;
   noted, not a defect.
5. **The denominator guard is needed**: M47 (`and` → `or` in the OK verdict) prints `good=ok controls=0/12 verdict=OK` on the
   always-green counter. The frozen harness prints FAIL there, which is the spec's requirement and holds.

## Limits

- The 66 mutants are a sample of one-line edit classes (operator, off-by-one, constant, regex, dropped leg, inverted test,
  removed guard, swapped arguments), not an exhaustive enumeration. Kill rates describe this sample.
- The extra oracles (kitchen-sink, single-leg stubs, wrappers, variant trees) are mine. The frozen harness has no control
  for them; the verdict-relevant kill rate counts them separately so the spec-only figure is visible.
- Proposals were verified on the real counter's tree (pristine), and each survivor was checked with its addition. The
  proposal runs were not repeated on all 40 oracles.
- Equivalence is argued for this counter and this tree, not proved for all counters.
- No counter was modified; the counter is read as written.

## Reproduce

```
cd /fast/scratch/hyaku/mado-r56/R56W2MutC1Harness      # scratch; copies of the scripts in this directory
python3 -I gen_stubs.py stubs                           # 24 stubs
python3 -I drive.py                                     # 66 mutants x 40 oracles (JOBS=12, ~20 min on 32 cores)
python3 -I final_table.py                               # receipts/classes.json
python3 -I extra_variants.py                            # var_srcline2, var_pinlink (fixtures)
python3 -I verify_props.py M23 M24 M25 M58 M60 M55 M56  # P1, P2, P3 matrix
python3 -I verify_p4.py                                 # P4 (H rows junked)
python3 -I write_md.py                                  # this file
```

The per-oracle receipts are in `receipts.tar.gz` (`receipts/<MUTANT>/<oracle>.{out,err,rc}`, `receipts/PRISTINE/`),
`receipts/run-full.log`, `receipts/summary.json`, `receipts/classes.json`; the proposal runs are in `proposals/`.

## Host and tooling

No tool was installed or upgraded. Python 3.14.8 and git 2.56.0 were used as present. No `sudo`, no `pacman`, no
compositor or service change; nothing under `~/.config` or `~/.local` was written.
