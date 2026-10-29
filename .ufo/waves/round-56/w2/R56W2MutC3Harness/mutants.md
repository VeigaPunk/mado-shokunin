# Mutation test of `quality/r56_ctl_c3.py` (round-56 C3 control harness)

Seat R56W2MutC3Harness, wave w2 (falsify), lane commit `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`.

## 1. What was attacked

`quality/r56_ctl_c3.py` -- the independent control harness behind the C3 claim
`MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK`.
Nine controls (base-registry, fill-all, drop-one, dangling-source, ghost-path, fenced-cite,
allow-everything, delete-citation, stale-allow), their expected legs, the shared-clone scratch builder and
`judge_good`/`judge_control` (exempt=24) are the ONLY kill evidence the claim has; wave 1 wrote each artifact
once and the round-55 counters left 11/24, 8/38 and 4/17 survivors. The attack is therefore the harness
itself: if a one-line change to it weakens the discrimination without changing the printed verdict, the
claim's control evidence is weaker than it looks.

## 2. Method

* Scratch clone: `git archive 28fc86ac...` of the lane into `/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness/tree`;
  every mutation is applied to a COPY of `quality/r56_ctl_c3.py`. The lane is never written to.
* Reduced scratch repo (`mini`): the same content blobs as the lane commit (corpus/SOURCES.md, the 71
  corpus/knowledge/*.md, frozen-tables-v2.json, c3-name-only.tsv, the counter), committed in a fresh git repo
  whose object store borrows the lane's through `.git/objects/info/alternates`, so the frozen base revision
  13f0acbe stays readable. Blob-identity proof: `receipts/06-environment-note.txt`.
* Oracle (unchanged for every mutant): the shipped driver `quality/check-r56-controls.py --claim c3` run
  three times per mutant:
  * **A** --counter = the REAL counter `quality/counters/c3-r56-used-by.py`; must print exactly
    `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK` and exit 0;
  * **B** --counter = `stub_green.py` (always prints TARGET_MET, exit 0) -> must score FAIL (exit != 0);
  * **C** --counter = `stub_legs.py` (prints every leg missed, exit 1) -> must score FAIL (exit != 0).
* KILLED = one of A/B/C deviates from the expectation. SURVIVED = all three hold. EQUIVALENT = the mutation
  cannot change the harness's verdict (argument + byte-identical stdout/stderr against the reference).
* The reduced repo is faithful: the unmutated harness scores `good=ok controls=9/9 verdict=OK` on it, and the
  same run against the REAL lane repo (`--repo <lane> --rev 28fc86ac...`) prints the same line and the same
  nine control notes -- `receipts/02-lane-crosscheck.txt`.

## 3. Result

| | count |
|---|---|
| mutants | 54 |
| KILLED by the shipped oracle | 29 (53.7%) |
| SURVIVED | 25 |
| ... of which EQUIVALENT (no behavioural difference) | 11 |
| ... of which genuine coverage findings (addition proposed and verified) | 14 |

Kill rate of the shipped oracle over the NON-EQUIVALENT mutants: **29/43 = 67.4%**.
With the 14 proposed additions the kill rate over the non-equivalent mutants is **43/43 = 100%**.

## 4. The mutant table

`old -> new` is the single contiguous source fragment that was replaced (each occurs exactly once in the target).

| id | operator | mutated fragment | verdict |
|---|---|---|---|
| M01 | constant change | `N_CONTROLS = 9` -> `N_CONTROLS = 8` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=9/8 verdict=FAIL') |
| M02 | constant change | `N_CONTROLS = 9` -> `N_CONTROLS = 10` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=9/10 verdict=FAIL') |
| M03 | constant change | `d["n"] != "24"` -> `d["n"] != "0"` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=bad controls=9/9 verdict=FAIL') |
| M04 | operator swap | `d["verdict"] != "TARGET_MET" or any(d["counts"].values())` -> `d["verdict"] != "TARGET_MISSED" or any(d["counts"].values())` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=bad controls=9/9 verdict=FAIL') |
| M05 | inverted comparison | `or any(d["counts"].values()) or d["n"] != "24"` -> `or not any(d["counts"].values()) or d["n"] != "24"` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=bad controls=9/9 verdict=FAIL') |
| M06 | operator swap | `if rc != 0 or d["verdict"] != "TARGET_MET"` -> `if rc != 1 or d["verdict"] != "TARGET_MET"` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=bad controls=9/9 verdict=FAIL') |
| M07 | inverted comparison | `    if "TARGET_MET" in out:` -> `    if "TARGET_MET" not in out:` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=0/9 verdict=FAIL') |
| M08 | operator swap | `    if rc != 1:` -> `    if rc != 0:` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=0/9 verdict=FAIL') |
| M09 | inverted comparison | `if d["verdict"] != "TARGET_MISSED" or leg not in d["missed_list"]:` -> `if d["verdict"] != "TARGET_MISSED" or leg in d["missed_list"]:` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=0/9 verdict=FAIL') |
| M10 | operator swap | `leg not in d["missed_list"]` -> `leg not in d["missed"]` | EQUIVALENT |
| M11 | inverted comparison | `    if d["rev"] != rev:` -> `    if d["rev"] == rev:` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=bad controls=0/9 verdict=FAIL') |
| M12 | off-by-one | `    if len(lines) != 1:` -> `    if len(lines) > 1:` | EQUIVALENT |
| M13 | dropped check | `if any(x not in ALL_LEGS for x in missed) or len(set(missed)) != len(missed):` -> `if len(set(missed)) != len(missed):` | SURVIVED |
| M14 | operator swap | `        missed = d["missed"].split(",")` -> `        missed = d["missed"].split(" ")` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=5/9 verdict=FAIL') |
| M15 | constant change | `counts = {"missing": int(d["m"]), "extra": int(d["x"]), "dangling": int(d["d"]), "conflict": int(d["c"]), "stale": int(d["s"]), "lost": int(d["l"])}` -> `counts = {"missing": 0, "extra": int(d["x"]), "dangling": int(d["d"]), "conflict": int(d["c"]), "stale": int(d["s"]), "lost": int(d["l"])}` | SURVIVED |
| M16 | constant change | `    if d["missed"] == "none":` -> `    if d["missed"] == "none,":` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=bad controls=9/9 verdict=FAIL') |
| M17 | operator swap | `            k += ok` -> `            k += 1` | KILLED (rc=0 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK') |
| M18 | inverted comparison | `verdict = "OK" if (good_ok and k == N_CONTROLS) else "FAIL"` -> `verdict = "OK" if (good_ok or k == N_CONTROLS) else "FAIL"` | KILLED (rc=0 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=0/9 verdict=OK') |
| M19 | operator swap | `        return line, (0 if verdict == "OK" else 1)` -> `        return line, 0` | KILLED (rc=0 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=0/9 verdict=FAIL') |
| M20 | off-by-one | `    sys.stdout.write(line + "\n")` -> `    sys.stdout.write(line)` | KILLED (rc=0 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK') |
| M21 | dropped leg | `        for name, fn in CONTROLS:` -> `        for name, fn in CONTROLS[:8]:` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=8/9 verdict=FAIL') |
| M22 | swapped expectation | `return base_src, {}, "corpus/SOURCES.md := bytes at the frozen base revision", "missing"` -> `return base_src, {}, "corpus/SOURCES.md := bytes at the frozen base revision", "extra"` | KILLED (rc=2 stdout='') |
| M23 | operator swap | `    cell = " " + " ".join(sorted(entries)) + " "` -> `    cell = " " + " ".join(sorted(entries, reverse=True)) + " "` | EQUIVALENT |
| M24 | dropped guard | `new = USEDBY_RE.sub(lambda m: "" if m.group(0) == path else m.group(0), cell)` -> `new = USEDBY_RE.sub(lambda m: "", cell)` | SURVIVED |
| M25 | removed continue | `            continue  # first sorted entry that some row lists (ambiguity: spec says "first entry (sorted)")` -> `            break  # first sorted entry that some row lists (ambiguity: spec says "first entry (sorted)")` | SURVIVED (latent) |
| M26 | widened bound | `        for i, ln in enumerate(lines[:15]):` -> `        for i, ln in enumerate(lines[:150]):` | SURVIVED |
| M27 | operator swap | `        if sid == "S001":` -> `        if sid == "S002":` | SURVIVED |
| M28 | off-by-one | `    ghost = "corpus/knowledge/no-such-entry.md"` -> `    ghost = "corpus/knowledge/no-such-entry"` | KILLED (rc=2 stdout='') |
| M29 | operator swap | `    s, path, li = sorted(cands)[0]` -> `    s, path, li = sorted(cands)[-1]` | SURVIVED |
| M30 | dropped leg | `    lines[li:li + 1] = ["```", lines[li], "```"]` -> `    lines[li:li + 1] = ["```", lines[li]]` | SURVIVED |
| M31 | constant change | `rows = "".join("%s\t%s\t%s\tx\n" % (s, p, line_sha(ls)) for (s, p), ls in sorted(pl.items()))` -> `rows = "".join("%s\t%s\t%s\ty\n" % (s, p, line_sha(ls)) for (s, p), ls in sorted(pl.items()))` | EQUIVALENT |
| M32 | dropped leg | `for (s, p), ls in sorted(pl.items()))` -> `for (s, p), ls in sorted(pl.items())[:1])` | SURVIVED |
| M33 | off-by-one | `lines[i] = re.sub(r"(?<![A-Za-z0-9])" + s + r"(?![0-9])", "S---", ln, count=1)` -> `lines[i] = re.sub(r"(?<![A-Za-z0-9])" + s + r"(?![0-9])", "S---", ln, count=0)` | EQUIVALENT |
| M34 | inverted comparison | `            if occ != 1:` -> `            if occ == 1:` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=8/9 verdict=FAIL') |
| M35 | constant change | `            lines[i] = ln + " x"` -> `            lines[i] = ln + " y"` | EQUIVALENT |
| M36 | operator swap | `                ok = own[leg] > 0 if name == "base-registry" else own[leg] > own_good[leg]` -> `                ok = own[leg] > 0` | SURVIVED |
| M37 | dropped check | `                ok = own[leg] > 0 if name == "base-registry" else own[leg] > own_good[leg]` -> `                ok = True` | SURVIVED |
| M38 | dropped leg | `            if leg in ("missing", "extra", "dangling"):` -> `            if leg in ("missing", "extra"):` | SURVIVED |
| M39 | inverted comparison | `            if not ok:` -> `            if ok:` | KILLED (rc=2 stdout='') |
| M40 | inverted comparison | `        if os.path.realpath(top) != os.path.realpath(d):` -> `        if os.path.realpath(top) == os.path.realpath(d):` | KILLED (rc=2 stdout='') |
| M41 | operator swap | `        git(work, d, "add", "-A", "-f", ".")` -> `        git(work, d, "add", "-A", ".")` | EQUIVALENT |
| M42 | off-by-one | `        git(work, d, "checkout", "-q", "--detach", rev_sha)` -> `        git(work, d, "checkout", "-q", "--detach", rev_sha + "^")` | KILLED (rc=2 stdout='') |
| M43 | off-by-one | `                changed[SOURCES] = enc(m_src)` -> `                changed[SOURCES] = enc(m_src)[:-1]` | EQUIVALENT |
| M44 | dropped check | `            m_ent.update({k_: v_ for k_, v_ in new_ent.items() if k_.startswith(KNOW + "/")})` -> `            m_ent.update({k_: v_ for k_, v_ in new_ent.items()})` | SURVIVED |
| M45 | inverted comparison | `        if "--counter" in opts:` -> `        if "--counter" not in opts:` | KILLED (rc=0 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK') |
| M46 | dropped leg | `        if a not in ("--repo", "--rev", "--work", "--counter") or a in opts or i + 1 >= len(argv):` -> `        if a not in ("--repo", "--rev", "--work") or a in opts or i + 1 >= len(argv):` | KILLED (rc=2 stdout='') |
| M47 | off-by-one | `        CTX["allow"] = dec(ab)` -> `        CTX["allow"] = dec(ab)[:-1]` | EQUIVALENT |
| M48 | inverted comparison | `        if s in bused and p not in bused[s] and (s, p) not in allow:` -> `        if s in bused and p in bused[s] and (s, p) not in allow:` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=8/9 verdict=FAIL') |
| M49 | operator swap | `        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--work", work], cwd=work,` -> `        p = subprocess.run([sys.executable, counter, "--repo", repo, "--rev", rev, "--work", work], cwd=work,` | EQUIVALENT |
| M50 | constant change | `TIMEOUT = 180` -> `TIMEOUT = 5` | EQUIVALENT |
| M51 | inverted comparison | `    if not out.endswith("\n"):` -> `    if out.endswith("\n"):` | KILLED (rc=1 stdout='MADO_R56_CONTROLS: claim=c3 good=bad controls=0/9 verdict=FAIL') |
| M52 | widened regex | `CITE_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")` -> `CITE_RE = re.compile(r"S[0-9]{3}")` | SURVIVED |
| M53 | widened regex | `USEDBY_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")` -> `USEDBY_RE = re.compile(r"corpus/knowledge/.*")` | KILLED (rc=2 stdout='') |
| M54 | swapped argument order | `["git", "clone", "-q", "--shared", "--no-checkout", repo, d]` -> `["git", "clone", "-q", "--shared", "--no-checkout", d, repo]` | KILLED (rc=2 stdout='') |

## 5. Every survivor: the argument or the addition that kills it

### M10 -- EQUIVALENT

* mutated: `leg not in d["missed_list"]` -> `leg not in d["missed"]`
* stdout identical to the reference: True; stderr identical: True
* `leg not in d["missed"]` (substring of the joined list) vs `leg not in d["missed_list"]` (list membership). The list is validated against ALL_LEGS (M13 intact) and no leg name is a substring of another leg name, and no leg name contains the ',' separator, so the joined string contains a leg name iff the list contains it. stdout and stderr byte-identical to the reference.

### M12 -- EQUIVALENT

* mutated: `    if len(lines) != 1:` -> `    if len(lines) > 1:`
* stdout identical to the reference: True; stderr identical: True
* `out` is rejected earlier unless it ends with '\n', so `out[:-1].split('\n')` always yields >= 1 element; `len(lines) != 1` and `len(lines) > 1` are then the same predicate. stdout and stderr byte-identical.

### M13 -- SURVIVED

* mutated: `if any(x not in ALL_LEGS for x in missed) or len(set(missed)) != len(missed):` -> `if len(set(missed)) != len(missed):`
* stdout identical to the reference: True; stderr identical: True
* parse_line no longer rejects a `missed` list holding a leg name outside ALL_LEGS (e.g. `missed=missing,bogus`). Nothing else in the harness notices: the required leg is still looked up in the parsed list. ADDITION: a unit check on parse_line -- `parse_line('... missed=missing,totally_bogus_leg', 'abc')` must return None. Verified: the reference returns None, the mutant returns a dict (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- parse_line accepted an unknown leg name (None)

### M15 -- SURVIVED

* mutated: `counts = {"missing": int(d["m"]), "extra": int(d["x"]), "dangling": int(d["d"]), "conflict": int(d["c"]), "stale": int(d["s"]), "lost": int(d["l"])}` -> `counts = {"missing": 0, "extra": int(d["x"]), "dangling": int(d["d"]), "conflict": int(d["c"]), "stale": int(d["s"]), "lost": int(d["l"])}`
* stdout identical to the reference: True; stderr identical: False
* the counter's own `missing=` count is discarded, so the harness's self-consistency check (`set(nz) <= set(missed)`) can no longer see a counter that reports missing>0 without listing `missing`. The stderr divergence note changes (the harness's model is compared with the counter's). ADDITION: a unit check on parse_line -- a line with missing=41 and `missed=extra` must be rejected. Verified: the reference rejects it, the mutant accepts it (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- parse_line accepted an inconsistent missing count / missed list (None)

### M23 -- EQUIVALENT

* mutated: `    cell = " " + " ".join(sorted(entries)) + " "` -> `    cell = " " + " ".join(sorted(entries, reverse=True)) + " "`
* stdout identical to the reference: True; stderr identical: True
* control 2 writes the entry paths in reverse order inside the used-by cell. The counter extracts the cell's paths as a SET (USED_BY.findall -> set), so every count and the whole MADO_USED_BY line are unchanged. stdout and stderr byte-identical.

### M24 -- SURVIVED

* mutated: `new = USEDBY_RE.sub(lambda m: "" if m.group(0) == path else m.group(0), cell)` -> `new = USEDBY_RE.sub(lambda m: "", cell)`
* stdout identical to the reference: True; stderr identical: False
* control 3 (drop-one) empties the WHOLE used-by cell (9 paths) instead of removing one path. The counter only sees 'that path is missing', so the control is credited exactly as before. ADDITION: a unit check on mut_drop_one -- exactly one row may change and exactly one path may be removed from it. Verified: the reference removes 1 path, the mutant removes 9 (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- 9 paths removed instead of 1 (['corpus/knowledge/animation-table-r26.md', 'corpus/knowledge/hyprctl-flags-r28.md', 'corpus/knowledge/hyprctl-getoption-native-forms-r40.md', 'corpus/knowledge/hyprctl-verification-layer.md', 'corpus/knowledge/hyprland-gkeep-geometry-r43.md', 'corpus/knowledge/request-limits-upstream-r31.md', 'corpus/knowledge/request-socket-live-bound-r8.md', 'corpus/knowledge/rule-attribution-r24.md', 'corpus/knowledge/workspace-rules-r27.md'])

### M25 -- SURVIVED (latent)

* mutated: `            continue  # first sorted entry that some row lists (ambiguity: spec says "first entry (sorted)")` -> `            break  # first sorted entry that some row lists (ambiguity: spec says "first entry (sorted)")`
* stdout identical to the reference: True; stderr identical: True
* the `continue` branch of mut_drop_one is dead code on this tree (the first sorted entry corpus/knowledge/animation-table-r26.md IS listed by S158), so the mutation is unobservable here; on any tree where the first entry is unlisted it turns a skip into a Setup abort of the whole harness. ADDITION: a unit check on mut_drop_one with a registry from which the first sorted entry has been stripped out of every used-by cell -- the call must return (not raise) and must not remove that entry. Verified: the reference returns, the mutant raises Setup (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- mut_drop_one raised Setup('drop-one: no registry row lists any entry') instead of skipping the unlisted entry corpus/knowledge/animation-table-r26.md

### M26 -- SURVIVED

* mutated: `        for i, ln in enumerate(lines[:15]):` -> `        for i, ln in enumerate(lines[:150]):`
* stdout identical to the reference: True; stderr identical: True
* control 4 (dangling-source) may pick a `source:` line outside the 15-line SRC window of registration-v2 ('SRC(entry) = tokens on lines starting source: among the entry's first 15 lines'). On this tree the first entry's source: line is early, so the window widening is invisible. ADDITION: a unit check on mut_dangling_source with a synthetic fixture -- two entries, the first (sorted) with its only source: line at index 20, the second at index 3 -- the second must be the mutated one. Verified: the reference picks the second, the mutant picks the first (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- the mutated entry is ['corpus/knowledge/aaa-r56.md'], expected the entry whose source: line is inside the 15-line window

### M27 -- SURVIVED

* mutated: `        if sid == "S001":` -> `        if sid == "S002":`
* stdout identical to the reference: True; stderr identical: True
* control 5 (ghost-path) writes the ghost path into S002's used-by instead of S001's. The counter only sees 'one extra path', so the control is credited; the harness's own note is a hard-coded string ('... to the used-by of S001') and does not reveal the swap. ADDITION: a unit check on mut_ghost_path -- the ghost path must be in S001's used-by cell. Verified: the reference puts it in S001, the mutant in S002 (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- the ghost path is not in S001's used-by (' corpus/lessons/round-12.md ')

### M29 -- SURVIVED

* mutated: `    s, path, li = sorted(cands)[0]` -> `    s, path, li = sorted(cands)[-1]`
* stdout identical to the reference: True; stderr identical: False
* control 6 (fenced-cite) fences the LAST candidate pair instead of the first (sorted by (S, entry)). Any fenced single citation yields `extra`, so the control is credited either way. ADDITION: a unit check on mut_fenced_cite -- the mutated entry must be the first candidate sorted by (S, entry) and the cited line must be inside the fence. Verified: the reference fences the first candidate, the mutant the last (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- fenced corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md instead of the first candidate corpus/knowledge/window-rule-effects-getprop.md

### M30 -- SURVIVED

* mutated: `    lines[li:li + 1] = ["```", lines[li], "```"]` -> `    lines[li:li + 1] = ["```", lines[li]]`
* stdout identical to the reference: True; stderr identical: False
* control 6 opens a ``` fence and never closes it, so every following line of that entry becomes fenced and all of its other citations disappear. The collateral leg `lost` is tolerated by judge_control (only the required leg must be present), so the control is still credited. ADDITION: a unit check on mut_fenced_cite -- the number of ``` markers in the mutated entry must stay even (the fence must be closed). Verified: the reference has 6 markers, the mutant 5 (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- 5 ``` markers in the mutated entry: the fence is left open

### M31 -- EQUIVALENT

* mutated: `rows = "".join("%s\t%s\t%s\tx\n" % (s, p, line_sha(ls)) for (s, p), ls in sorted(pl.items()))` -> `rows = "".join("%s\t%s\t%s\ty\n" % (s, p, line_sha(ls)) for (s, p), ls in sorted(pl.items()))`
* stdout identical to the reference: True; stderr identical: True
* control 7 writes the allowlist's reason column as 'y' instead of 'x'. The counter parses the allowlist with parse_allow and reads only cells 0, 1 and 2 (the reason in cell 3 is never read), and the harness reads only cells 0 and 1, so every count and the whole MADO_USED_BY line are unchanged. stdout and stderr byte-identical.

### M32 -- SURVIVED

* mutated: `for (s, p), ls in sorted(pl.items()))` -> `for (s, p), ls in sorted(pl.items())[:1])`
* stdout identical to the reference: True; stderr identical: False
* control 7 (allow-everything) writes ONE allowlist row instead of one per pair (390 pairs). The counter only sees 'the allowlist sha does not match' plus `exempt != 24`, so the control is credited. ADDITION: a unit check on mut_allow_everything -- the written allowlist must carry one row per (S, entry) pair. Verified: the reference writes 390 rows, the mutant 1 (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- the allowlist has 1 rows, the tree has 390 pairs

### M33 -- EQUIVALENT

* mutated: `lines[i] = re.sub(r"(?<![A-Za-z0-9])" + s + r"(?![0-9])", "S---", ln, count=1)` -> `lines[i] = re.sub(r"(?<![A-Za-z0-9])" + s + r"(?![0-9])", "S---", ln, count=0)`
* stdout identical to the reference: True; stderr identical: True
* control 8 replaces the cited token with `re.sub(..., count=0)` instead of `count=1`. On CPython 3.14 `re.sub(..., count=0)` means 'replace ALL matches' (measured: 'S001 and S001' -> 'S--- and S---'), and the selected pair has exactly one occurrence of the token in total (`occ != 1: continue` selects it), so the same single replacement happens and the mutated bytes are identical. stdout and stderr byte-identical.

### M35 -- EQUIVALENT

* mutated: `            lines[i] = ln + " x"` -> `            lines[i] = ln + " y"`
* stdout identical to the reference: True; stderr identical: True
* control 9 appends ' y' instead of ' x' to the allowlisted citing line. The stale leg only compares the line-sha, which differs either way, so the counter's line is unchanged. (The registration's literal text names ' x'; the deviation is cosmetic.) stdout and stderr byte-identical.

### M36 -- SURVIVED

* mutated: `                ok = own[leg] > 0 if name == "base-registry" else own[leg] > own_good[leg]` -> `                ok = own[leg] > 0`
* stdout identical to the reference: True; stderr identical: True
* the effectiveness check `own[leg] > own_good[leg]` becomes `own[leg] > 0`: a control whose mutation does not raise its leg is no longer rejected as a setup error. On this tree every control does raise its leg, so the stdout is unchanged. ADDITION: control 10 'noop-control' -- a control whose mutation changes nothing (and therefore cannot raise any leg) -- plus the assertion that the harness refuses it with the setup error 'control noop-control is ineffective'. Verified: the reference exits 2 with that message, the mutant scores controls=9/10 verdict=FAIL (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- patched harness rc=0 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK' stderr='control 10 noop-control: FAIL -- counter printed TARGET_MET on a mutated tree [no-op mutation; harness missing=24]'

### M37 -- SURVIVED

* mutated: `                ok = own[leg] > 0 if name == "base-registry" else own[leg] > own_good[leg]` -> `                ok = True`
* stdout identical to the reference: True; stderr identical: True
* the effectiveness check is deleted outright (`ok = True`); same consequence as M36. ADDITION: control 10 'noop-control' as in M36. Verified: the reference exits 2 'ineffective', the mutant scores controls=9/10 verdict=FAIL (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- patched harness rc=0 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK' stderr='control 10 noop-control: FAIL -- counter printed TARGET_MET on a mutated tree [no-op mutation; harness missing=24]'

### M38 -- SURVIVED

* mutated: `            if leg in ("missing", "extra", "dangling"):` -> `            if leg in ("missing", "extra"):`
* stdout identical to the reference: True; stderr identical: True
* the `dangling` leg is dropped from the set of legs whose effectiveness is checked, so control 4 (dangling-source) is no longer required to raise the dangling leg. ADDITION: control 10 'noop-control' targeting the `dangling` leg (a mutation that changes an entry without touching a source: line) plus the assertion that the harness refuses it as ineffective. Verified: the reference exits 2 'ineffective', the mutant scores controls=9/10 verdict=FAIL (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- patched harness rc=0 stdout='MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK' stderr='control 10 noop-control: FAIL -- counter printed TARGET_MET on a mutated tree [no-op mutation of one entry; harness dangling=0]'

### M41 -- EQUIVALENT

* mutated: `        git(work, d, "add", "-A", "-f", ".")` -> `        git(work, d, "add", "-A", ".")`
* stdout identical to the reference: True; stderr identical: True
* the forced add (`git add -A -f .`) becomes `git add -A .`. The lane's .gitignore ignores only .ufo/interactive-sessions/, .ufo/state/ and __pycache__/; no mutation target (corpus/SOURCES.md, corpus/knowledge/*.md, .ufo/waves/round-56/c3-name-only.tsv) is ignored, so the same files are staged and the same commit results. stdout and stderr byte-identical.

### M43 -- EQUIVALENT

* mutated: `                changed[SOURCES] = enc(m_src)` -> `                changed[SOURCES] = enc(m_src)[:-1]`
* stdout identical to the reference: True; stderr identical: True
* the mutated registry loses its final byte, the trailing newline after the last line of corpus/SOURCES.md. That line is prose (`no keypress observation: source-level only.`), not a registry row, so no row's cells, no used-by cell and no count changes. stdout and stderr byte-identical.

### M44 -- SURVIVED

* mutated: `            m_ent.update({k_: v_ for k_, v_ in new_ent.items() if k_.startswith(KNOW + "/")})` -> `            m_ent.update({k_: v_ for k_, v_ in new_ent.items()})`
* stdout identical to the reference: True; stderr identical: False
* the harness's own entry model no longer filters the changed paths to corpus/knowledge/*.md, so the allowlist file is counted as an entry in control 7 (the model's count becomes 72 where the counter reports 71). The scored stdout is unchanged; only a diagnostic note diverges. This is a DIAGNOSTIC-level kill only: the verdict does not change, so the kill is by the stderr note, not by the score. ADDITION: the harness run's stderr must not report an entry-count divergence between the counter and the harness's model. Verified: the reference reports none, the mutant reports 'entries counter=71 harness=72' (addition kills it at stderr level).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- the harness's model reports a different entry count than the counter: '  note[allow_sha]: counter and harness numbers diverge (not scored): entries counter=71 harness=72; missing counter=0 harness=322'

### M47 -- EQUIVALENT

* mutated: `        CTX["allow"] = dec(ab)` -> `        CTX["allow"] = dec(ab)[:-1]`
* stdout identical to the reference: True; stderr identical: True
* the harness's copy of the allowlist loses its final byte, which is the trailing newline of the last row. allow_rows() splits on newline and drops empty lines, so the last row is still parsed with the same four cells; the harness reads cells 0-1 only, and no mutation target is derived from the allowlist's last byte. stdout and stderr byte-identical.

### M49 -- EQUIVALENT

* mutated: `        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--work", work], cwd=work,` -> `        p = subprocess.run([sys.executable, counter, "--repo", repo, "--rev", rev, "--work", work], cwd=work,`
* stdout identical to the reference: True; stderr identical: True
* the counter child loses the isolated mode (`python3 -I` -> `python3`). The counter imports only stdlib modules (argparse, hashlib, json, os, re, shutil, subprocess, sys) and its directory holds no module that could shadow them, so the child behaves identically. stdout and stderr byte-identical.

### M50 -- EQUIVALENT

* mutated: `TIMEOUT = 180` -> `TIMEOUT = 5`
* stdout identical to the reference: True; stderr identical: True
* the counter child's timeout drops from 180 s to 5 s. The counter run on this tree takes 1.07-1.93 s (measured, 10 runs under sweep load), so the timeout is never reached and no run is aborted: stdout and stderr byte-identical. Caveat: the margin is only ~2.6x, so under a heavily loaded machine this mutant would stop being equivalent and would surface as a flaky harness (a control aborted by the timeout), not as a silent acceptance.

### M52 -- SURVIVED

* mutated: `CITE_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")` -> `CITE_RE = re.compile(r"S[0-9]{3}")`
* stdout identical to the reference: True; stderr identical: False
* the harness's citation token rule is widened from `(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])` to `S[0-9]{3}`, so the harness's own model counts tokens inside longer identifiers (e.g. XS001) as citations; the contract's token rule does not. The scored stdout is unchanged, the diagnostic note diverges. ADDITION: a unit check on the harness's CITE_RE -- on 'XS001 and S0021 and S003' only S003 may match (S001 is inside a longer identifier; S0021 is a four-digit run, and the contract's lookahead rejects it). Verified: the reference matches ['S003'], the mutant matches ['S001', 'S002', 'S003'] (addition kills it).
* verification: the addition passes on the unmutated harness (True) and fails on the mutant (False) -- CITE_RE matched ['S001', 'S002', 'S003'] (only the standalone token may match)

## 6. What the survivors mean for the claim

The claim `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK` is **not falsified**: the harness is
correct on this tree and its nine controls do fail the real counter in the nine intended ways. The mutation
sweep nevertheless shows that the printed verdict pins down much less than it looks:

1. **The harness does not pin the counter's own grammar.** `parse_line` accepts a `missed` list with unknown leg
   names (M13) and, after M15, accepts a `missing=` count that the `missed` list does not mention. A counter that
   prints a self-inconsistent line can still be credited.
2. **The controls do not pin what they mutate.** Four of the nine controls can be changed into a different
   mutation of the same leg and still be credited: drop-one can empty a whole cell (M24), dangling-source can
   leave the 15-line SRC window (M26), ghost-path can write into the wrong registry row (M27) and fenced-cite can
   fence a different pair (M29) or leave the fence open (M30); allow-everything can write one row instead of one
   per pair (M32). The harness's own note for control 5 is a hard-coded string, so the wrong-row variant is
   invisible even in the diagnostics.
3. **The 'the mutation must raise its leg' guard is not guarded.** M36/M37/M38 delete or weaken the check that
   rejects an ineffective control; on this tree every control does raise its leg, so nothing notices.
4. **The harness's own model drifts from the contract.** The widened citation regex (M52) and the dropped
   `corpus/knowledge/` filter (M44) make the harness's independent model disagree with the contract's token rule
   and ENTRIES definition; both are only diagnostics today, but the model is what the effectiveness check uses.
5. The `lost`, `conflict` and `stale` legs are never checked for effectiveness (the harness's model does not
   compute them), and control 7/8/9 are accepted on `bool(new_entries)` alone.
6. The harness's independent model is not the contract, and says so on every run. On the GOOD tree the harness's own
   metric reports missing=24 while the counter reports missing=0, because the harness does not implement the frozen
   allowlist exemption (c3-name-only.tsv). The stderr line 'note[good]: counter and harness numbers diverge (not scored)'
   is printed on every run of the unmutated harness (receipts/01, receipts/02). Nothing scores it, so no verdict is
   wrong, but the harness's cross-check is noise, and the effectiveness check (own[leg] > own_good[leg]) is calibrated
   against that wrong baseline (missing 65 vs 24 instead of 65 vs 0).
7. The population of the good line is never checked (probe_population.py). judge_good accepts entries= and rows=
   without comparing them to the harness's own 71 and 328. A green counter stub that prints entries=0 rows=0 scores
   good=ok on the unmutated harness (receipts/07). It still scores controls=0/9 verdict=FAIL, so this is a gap only
   in combination with controls. The one-line fix (or d['e'] != own['entries'] or d['r'] != own['rows']) makes the
   empty stub good=bad and leaves the real counter at controls=9/9 verdict=OK (receipts/07).

### 6a. How the 29 kills were achieved

Of the 29 KILLED mutants, 25 fail the GOOD-tree run (check A: the harness no longer prints good=ok controls=9/9
verdict=OK on the true tree). Of those, 8 are the harness's own fail-closed SETUP errors (rc=2, empty stdout, a SETUP:
line on stderr: M22, M28, M39, M40, M42, M46, M53, M54) and 17 change the verdict line.
Only four were caught by the control logic alone: M17 and M18 (B: the always-green stub is credited), and M19 and
M45 (B or C). The silent-acceptance surface is therefore the 25 survivors, which section 5 covers.

## 7. Reproduction

```sh
S=/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness   # scratch, removed on exit
python3 -I $S/run_mutants.py            # the sweep (54 mutants x 3 oracle checks)
python3 -I $S/verify_survivors.py       # the additions that kill the survivors
python3 -I $S/collect_receipts.py       # the receipt bundle
```

Deliverables: `mutants.md` (this file), `run_mutants.py`, `mutants.py` (the mutation table),
`verify_survivors.py` (the proposed additions), `collect_receipts.py`, `stub_green.py`, `stub_legs.py`,
`receipts/`.
