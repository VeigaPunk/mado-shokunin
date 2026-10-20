# SimplifyCounters — both counters are near-minimal; 1 exit-code defect, 1 silent-zero path, 1 latent replace-ref hole; fresh-pins can drop 30 lines with byte-identical output; no measure.py reuse; change no counter bytes in round 19

## Axes

- **Correctness:** the documented exit map holds, and an instrument failure never reads as a score.
- **Size / duplication:** fewer lines, and fewer second copies of one rule.
- **Provenance continuity:** the pre-registered instrument bytes (`SCORECARD.md:1080-1090`) and the digests cited in receipts stay valid.
- **Cost:** git subprocesses per run.

I keep a move only if it improves one axis and harms none. In round 19, any code edit to either counter harms provenance (§6). All code proposals below are therefore for re-registered successors. The only round-19 action I recommend is a correction to draft text.

## Method

- Scratch clone: `/tmp/mado-r19-SimplifyCounters-f_4fscp6/repo`, made with `git clone --shared --no-checkout` of the lane.
- The counters were copied byte-exact into the same four-level path, so `LANE` resolves to the clone.
- Probe commits were built with plumbing (`read-tree` / `update-index` / `commit-tree`) inside the clone only.
- Every run used `python3 -I` with `GIT_OPTIONAL_LOCKS=0`.
- Revisions:
  - B `9c54c56a…`, P `17661e0f…`, M `df84807d…` (current `refs/heads/master`).
  - `988b858b…`: the commit that adds `tools/mado-tripwire.py`.
  - `3e9848a5…`: its parent, which has no tool.
  - `d3a00003…`: before `walker-route-r18.md` exists.
  - root `74d3b7ba…`.
  - Scratch-only probes, listed in §7.

Baselines:

- tw-recall: 3/6 at B, P and M.
- fresh-pins: 2/13 at B and P, **13/13 at M**.
- tw-recall stdout at P has sha256 `4b028d30a7c5…`. This equals MutCounters' O02 (`w1/reports/MutCounters.md`), so it is an independent reproduction.

## 1. Defects and untested behaviour (all observed unless marked)

| # | Where | What happens | Evidence | Proposal |
|---|---|---|---|---|
| D1 | `tw-recall.py:31-35` | `show()` raises `SystemExit("<str>")`, which exits **1**, not the documented 2 (`tw-recall.py:4`). This happens whenever REV lacks `tools/mado-tripwire.py` or a PIN_REV object cannot be read. | rc=1 at `3e9848a5` and at root `74d3b7ba`, stderr `could_not_evaluate: git show …:tools/mado-tripwire.py rc=128`. The unlanded registry draft says the opposite: `drafts/SkillRegistryDraft.md:28` "2 could-not-evaluate (… `git show` failure …)". | Print the message, then `sys.exit(2)` (diff in §5). In round 19, correct the draft row instead. SKILL.md has 0 `mado-tw-recall` hits at M, so no landed text is wrong yet. |
| D2 | `tw-recall.py:68-73` | The `--scan` verdict is parsed loosely. If the verdict has no `findings` key, `.get("findings", [])` gives **0/6 with exit 0**: a broken instrument reads as "detects nothing". If the verdict is multi-line JSON, `json.loads(lines[1])` raises, and the run ends in a **traceback with exit 1**. | Fake tools committed in the scratch clone: `T_nokey` → rc 0, 0/6. `T_indent` → rc 1, `JSONDecodeError`. `T_rc3` → rc 2 (the only guard the probes exercised). `T_all` (flags every line) → 6/6, the precision gap already owned by RevTwRecallPrecision and CriticC3. | One try/except (diff in §5). `T_nokey` and `T_indent` then exit 2. Stdout stays byte-identical at B, P, M, `988b858b`, `C_fp` and `T_all`. |
| D3 | every `git show PIN_REV:…` in both counters | The denominators described as "fixed at 9c54c56" are only as fixed as git's replace refs allow. I added a `refs/replace` on the PIN_REV commit pointing at a self-consistent forged tree. Both counters exited 0 and still printed `pin_rev=9c54c56…`, but tw-recall's **incident_lines went 6→3** and fresh-pins' **denominator went 13→12**. The digest guard (`tw-recall.py:56-60`) did not fire, because the forged manifest carries its own digests. | E7a (scratch clone): with `GIT_NO_REPLACE_OBJECTS=1`, both counters return 6 and 13 again. E7b: replacing one input blob alone gives rc 2 `digest inputs/r13-root.jsonl`; that is everything the guard covers. In the lane today, `git for-each-ref refs/replace` is empty and there is no `.git/info/grafts`, so the hole is **latent**. | Add one line per script: run git with `GIT_NO_REPLACE_OBJECTS=1`. Keep the guard: the declared rubric says "inputs digest-checked" (`SCORECARD.md:1088`), even though content-addressed reads would make it redundant [INFERENCE]. |
| D4 | `fresh-pins.py:72` | `pointer_lines: hits[:5]` truncates silently. | At M, `SKILL.md` has **12** pointer lines but the output lists 5. `tools/mado-verify.sh` has exactly 5, which looks the same. | Emit `pointer_count` (plus the first line or all lines). This changes the schema, so it needs `-v2`. |
| D5 | `fresh-pins.py:66-69` | Every `git show REV:path` failure is scored as "absent at REV" (not current, exit 0), including failures that are not deletions. | The branch ran at `d3a00003` (walker-route-r18 absent) and at root (11 files absent); both exited 0. The missing-object case is [INFERENCE], not run. | Check existence once with `git ls-tree REV -- <13 paths>`, and exit 2 when a listed path fails to read. Behaviour change, so `-v2`. |
| D6 | `fresh-pins.py:28` | The version token has no boundaries, so `2.17.20 (S096)` and `12.17.2 S096` count as current. | Scratch commit `C_fp`: `closeout-r11.md` is counted current through an appended `walker 2.17.20 (S096)`. supersede-sweep has the same hole (it prints `POINTED`). No real line triggers it today. | Use `(?<![\d.])2\.17\.2(?!\d)`; it still accepts `v2.17.2` and `2.17.2-1`. Behaviour change, so `-v2`. |

## 2. Deletions that keep output byte-identical

### `fresh-pins.py`: 88 → 58 lines

Changes:

- **Replace the per-run denominator derivation with a literal 13-path tuple.** This deletes:
  - `OLD` (:27);
  - `in_scope` (:35-38);
  - the `ls-tree` block and the PIN_REV `show` loop (:50-63);
  - the dead `if rows else None` (:81).
- **Replace the `POINTER` regex** (:28), which repeats both token orders, with `"2.17.2" in ln and ROW.search(ln)`.
- **Leave everything else unchanged,** including D4 and D5, so the output stays identical.

Proof:

- **Output:** `(rc, stdout)` is identical to the pristine counter on all 13 runs: B, P, M, `988b858b`, `3e9848a5`, `d3a00003`, root, `C_fp`, the 4 fake-tool commits, and a bogus rev.
- **Predicate equivalence:** 0 mismatches over 70,524 real in-scope lines (every in-scope file at B, P, M and `988b858b`) and 0 over 300,000 fuzz strings.
- **Cost:** 55 git calls per run (rev-parse + ls-tree + 40 `show@PIN_REV` + 13 `show@REV`) drop to 14.
- **Side effect:** under the D3 forgery, the literal tuple still gives 13.
- **Derivation preserved:** the committed before-receipt `evidence/fresh-pins-before.txt` already lists the 13 rows at B.
- **No other callers:** this session has no `lsp` device (the xd:// list has none), so I fell back to text grep.
  - `in_scope`, `POINTER` and `OLD` occur only inside `fresh-pins.py`: a definition plus one use each (:28/:71, :35/:56, :27/:62).
  - No lane script imports another: searching `.ufo/waves` and `tools` for `import measure|runpy|importlib|sys.path.insert` finds 0 files.

### `tw-recall.py`: no worthwhile output-preserving deletion

At 91 lines it is already close to minimal. Candidates:

- `exp.get("known_misses", [])` (:51) can become `exp["known_misses"]`; the PIN_REV manifest always has 3 entries.
- `verdict.get("findings", [])` (:73) should lose its default. That default is what produces D2's silent zero.
- The two hand-written `subprocess.run(["git", …])` call sites (:32, :43) can share one `git()` helper, as fresh-pins and supersede-sweep already do.

With D1 and D2 fixed, the file is 97 lines (+6). Correctness improves; size does not.

## 3. Duplicated logic across lane scripts

**Deciding whether a file is current: fresh-pins vs `supersede-sweep.py`.** The two scripts answer the same question with different rules.

- fresh-pins accepts any `S###`; the sweep accepts only the ledger rows S090 and S096 (`supersessions.json:9`).
- fresh-pins uses prefix scope; the sweep uses component globs. Today the two scopes select the same 40 in-scope files at B and at M.
- Scratch commit `C_fp` shows the disagreement concretely:
  - fresh-pins counts `SKILL.md` current through `see 2.17.2 S001` (line 1846).
  - the sweep prints `STALE SKILL.md` and exits 1.
- This was first reported in `w1/reports/SupersedeSweep.md:59-61`; I add a reproducing commit.
- Smallest single authority (round 20): fresh-pins reads its row set from the ledger. Its rule is pre-registered as "an `S###` row token" (`SCORECARD.md:1083-1084`), so it cannot change in round 19.

**Running the tool under test: tw-recall vs `frozen-repin.py`.**

- Both scripts:
  - stage the pinned inputs after a sha256 check;
  - run `python3 -I TOOL --scan inputs/…` from a temp working directory;
  - read `lines[1]` as JSON.
- frozen-repin's `parse_verdict` (`frozen-repin.py:240-304`) is strict: label regex, schema, `exit` equal to rc, and per-file sha256 against the pins.
- tw-recall's parser is 5 lines and lax (D2).
- Sharing a module would create a new convention (no lane script imports another). It would also put a second file outside harm-watch's single-path pin (§4). Copying the 3-line strictness from D2 is the proportionate move.

**Tool identity.** tw-recall's `tool_sha256` equals measure.py's `c3.sha256` at B and M (`c1ae45a7…`). This duplicate is harmless and needs no action.

**Shared boilerplate between the two counters.** Both copy `LANE` (4× `dirname`), `PIN_REV`, the usage check, the `rev-parse --verify REV^{commit}` block and the JSON envelope, about 15 lines each.

- The only consolidation that adds no new convention is merging both into one per-round counter. That matches the `round-N/measure.py` pattern of rounds 13-17.
- The pre-registration names two commands, and harm-watch pins two paths (`harm-watch.sh:352-361`). So this is a round-20 option at most.

## 4. Reusing round-17 `measure.py` helpers: no

- **Importing it runs it.** measure.py parses argv and resolves the rev at module top level (`measure.py:50-54`, `:63-67`), then prints and calls `sys.exit(0)` (`:313-316`).
  - `import measure` with argv `['x']` exits 2 with `usage: measure.py <revision>`.
  - With `['x', '9c54c56']` it prints the 3,413-byte `mado-measure-r17-v1` object and exits 0. The importer's next line never runs ("imported" was never printed).
  - Making it importable would mean editing a round-17 instrument whose digest `de4c422b…` is declared unchanged in `SCORECARD.md:1073`.
- **The helpers do not fit.**
  - `git()` is a text-mode `check_output` (`:57-60`).
  - `source` and `try_source` are bound to the module-global `rev_sha` (`:64`, `:70-78`).
  - tw-recall needs **bytes** at **two** revisions: raw input digests, and the tool written to disk. fresh-pins also reads two revisions.
  - Each helper is 3-6 lines, the same size as the code it would replace.
- **`python3 -I` drops the script directory from `sys.path`,** so any import needs `sys.path` surgery.
- **It would weaken provenance.** harm-watch's `run_pinned`/`pin_assert` (`harm-watch.sh:155-178`, `:201-215`) pins exactly one tool path per group. Imported helper bytes would run unpinned, and the receipt's `tool_sha256` would no longer cover all the code that ran.

## 5. Proposed code (for re-registered successors, not round 19)

`tw-recall.py`: D1 + D2 + dead defaults. Stdout is byte-identical on every real revision tested. Exit code changes only on the D1/D2 paths, 1 or 0 becoming 2. Scratch file sha256 `059c1711feeb…`:

```diff
@@ -30,6 +30,11 @@
 
+def git(*a):
+    return subprocess.run(["git", "-C", LANE, *a], capture_output=True)
+
+
 def show(rev, path):
-    p = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], capture_output=True)
+    p = git("show", f"{rev}:{path}")
     if p.returncode != 0:
-        raise SystemExit(f"could_not_evaluate: git show {rev}:{path} rc={p.returncode}")
+        print(f"could_not_evaluate: git show {rev}:{path} rc={p.returncode}", file=sys.stderr)
+        sys.exit(2)
     return p.stdout
@@ -42,4 +47,3 @@
     rev = sys.argv[1]
-    p = subprocess.run(["git", "-C", LANE, "rev-parse", "--verify", rev + "^{commit}"],
-                       capture_output=True, text=True)
+    p = git("rev-parse", "--verify", rev + "^{commit}")
     if p.returncode != 0:
@@ -47,6 +51,6 @@
         return 2
-    commit = p.stdout.strip()
+    commit = p.stdout.decode().strip()
     exp = json.loads(show(PIN_REV, f"{FROZEN}/expected.json"))
     incident = sorted({(f["file"], f["line"]) for f in exp["expected_findings"]}
-                      | {(m["file"], m["line"]) for m in exp.get("known_misses", [])})
+                      | {(m["file"], m["line"]) for m in exp["known_misses"]})
     tool = show(rev, "tools/mado-tripwire.py")
@@ -68,7 +72,9 @@
         lines = r.stdout.splitlines()
-        if r.returncode not in (0, 1) or len(lines) < 2:
+        try:
+            hit = {(f["file"], f["line"]) for f in json.loads(lines[1])["findings"]}
+        except (IndexError, ValueError, KeyError, TypeError):
+            hit = None
+        if r.returncode not in (0, 1) or hit is None:
             print(f"could_not_evaluate: scan rc={r.returncode}", file=sys.stderr)
             return 2
-        verdict = json.loads(lines[1])
-    hit = {(f["file"], f["line"]) for f in verdict.get("findings", [])}
     rows = [{"file": f, "line": n, "detected": (f, n) in hit} for f, n in incident]
```

For D3, a successor also adds `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` to `git()`. I did not include it in the scratch variant, but E7a/E7b ran the pristine counter with that variable set.

`fresh-pins.py`, minimal form (58 lines, sha256 `31f7ac9f5ba8…`). Its `(rc, stdout)` is byte-identical to the pristine counter on all 13 runs listed in §2:

```python
#!/usr/bin/env python3
"""Round-19 C2 counter (minimal form). Usage: fresh-pins.py REV -> JSON; exit 0 printed, 2 could-not-evaluate."""
import json, os, re, subprocess, sys

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PIN_REV = "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d"
# Owned files at PIN_REV whose bytes contain `2.17.0` (scope: corpus/knowledge/*.md,
# corpus/README.md, SKILL.md, PROVINCE.md, tools/*), frozen at pre-registration.
DENOM = (
    "SKILL.md",
    "corpus/README.md",
    "corpus/knowledge/arc-synthesis.md",
    "corpus/knowledge/closeout-r11.md",
    "corpus/knowledge/config-health-report-r3.md",
    "corpus/knowledge/remaining-planes-census.md",
    "corpus/knowledge/walker-deep-r9.md",
    "corpus/knowledge/walker-deep.md",
    "corpus/knowledge/walker-live-surface.md",
    "corpus/knowledge/walker-route-r18.md",
    "corpus/knowledge/waybar-walker-plane.md",
    "corpus/knowledge/waybar-walker-semantics.md",
    "tools/mado-verify.sh",
)
ROW = re.compile(r"\bS\d{3}\b")


def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], capture_output=True)


def main():
    if len(sys.argv) != 2:
        print("usage: fresh-pins.py REV", file=sys.stderr)
        return 2
    rev = sys.argv[1]
    c = git("rev-parse", "--verify", rev + "^{commit}")
    if c.returncode != 0:
        print(f"could_not_evaluate: rev {rev}", file=sys.stderr)
        return 2
    rows = []
    for p in DENOM:
        b = git("show", f"{rev}:{p}")
        if b.returncode != 0:
            rows.append({"path": p, "current": False, "reason": "absent at REV"})
            continue
        hits = [i + 1 for i, ln in enumerate(b.stdout.decode(errors="replace").splitlines())
                if "2.17.2" in ln and ROW.search(ln)]
        rows.append({"path": p, "current": bool(hits), "pointer_lines": hits[:5]})
    cur = sum(r["current"] for r in rows)
    print(json.dumps({"schema": "mado-fresh-pins-r19-v1", "rev": rev,
                      "commit": c.stdout.decode().strip(), "pin_rev": PIN_REV,
                      "denominator": len(rows), "current": cur,
                      "score": round(10 * cur / len(rows), 4), "rows": rows}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 6. Disposition and stop point

Why I stop here:

- Both counters are pre-registered by path and rule (`SCORECARD.md:1080-1090`).
- Their digests are cited in RECEIPT headers: `evidence/fresh-pins-before.txt:1` (`a094be01…`) and `evidence/tw-recall-before.txt:1` (`22090298…`).
- The same digests appear in `receipt-claims.json:48,57`.
- harm-watch refuses a counter whose worktree bytes differ from the bytes at REV (`pin_assert`, `harm-watch.sh:155-178`).
- Lane state at M: the worktree bytes of both counters, `measure.py`, `supersede-sweep.py`, `frozen-repin.py`, `harm-watch.sh` and `supersessions.json` all equal `df84807:<path>`.

Editing either counter in round 19 would change the instrument after measurement started and force receipt re-cuts. That harms provenance, so the next deletion is where I stop.

**Round 19:**
- Change no counter bytes.
- Correct `drafts/SkillRegistryDraft.md:28` before it lands. Its exit map should read: exit 1 when `git show` of REV's tool or of a PIN_REV object fails, and exit 1 with a traceback when the verdict line cannot be parsed.
- Optionally add to that row's limits: D2's silent 0/6 on a verdict without a `findings` key, and D4's truncation at 5.

**Round 20 (re-registered successors with a new schema id):**
- `tw-recall` v2 = the §5 diff plus `GIT_NO_REPLACE_OBJECTS=1`.
- `fresh-pins` v2 = the §5 minimal form plus `GIT_NO_REPLACE_OBJECTS=1`, D4/D5/D6, and ledger-driven rows (§3).

## 7. Evidence ledger

Scratch commits (exist only in `/tmp/mado-r19-SimplifyCounters-f_4fscp6/repo`):

| Label | Commit | Content (on top of P unless stated) |
|---|---|---|
| `C_fp` | `9b12e51b7f1ba264499017cc0f8cf807fa340c97` | `SKILL.md` + `see 2.17.2 S001`; `closeout-r11.md` + `walker 2.17.20 (S096)`; `walker-deep.md` deleted |
| `T_all` | `7b6f45bf5acf1dcccd89deb762a278cf99504d09` | fake `tools/mado-tripwire.py`: a finding on every line, exit 1 |
| `T_nokey` | `ebb2678e37147d918a45ca4c1271a54c6868ab50` | same, but verdict key `results` instead of `findings` |
| `T_indent` | `3841c8ba8dd315e3a43de8d5bd958f245bc69562` | same, verdict JSON printed with `indent=1` |
| `T_rc3` | `5f4d89edb42cdd118ba785c8557d9ff28e192d46` | same, exit 3 |
| forged PIN (E7a) | replace ref on B → forged commit (parent `b7148a1`) | `expected.json` with `known_misses: []`; `SKILL.md` with `2.17.0` → `2.17.x`; replace ref deleted after the probe |

Pristine stdout sha256 (REV argument passed as the full hash):

| Counter | B | P | M |
|---|---|---|---|
| tw-recall | `65d886b0…` | `4b028d30…` | `61a34195…` |
| fresh-pins | `633396e5…` | `c82206c0…` | `a189a113…` |

Outputs of the pristine counters:

| Run | Result |
|---|---|
| tw-recall at `3e9848a5` / root | rc 1 |
| tw-recall at `988b858b` | rc 0, 3/6 |
| tw-recall at `T_all` / `T_nokey` / `T_indent` / `T_rc3` | rc 0 6/6 / rc 0 0/6 / rc 1 / rc 2 |
| fresh-pins at `d3a00003` | 0/13, 1 absent |
| fresh-pins at root | 0/13, 11 absent |
| fresh-pins at `C_fp` | 4/13 |
| supersede-sweep at `C_fp` | rc 1, `files=12 pointed=3 stale=9`, `STALE SKILL.md` |
| E7a with replace ref active | tw-recall 3/6 of 6→3 incident lines; fresh-pins 2/12 |
| E7a with `GIT_NO_REPLACE_OBJECTS=1` | tw-recall 3/6; fresh-pins 2/13 |
| E7b, one input blob replaced | tw-recall rc 2; with `GIT_NO_REPLACE_OBJECTS=1`, rc 0 and 3 detected |

## Limits

- No `lsp` device was available, so text grep was the caller-proof fallback. It is literal matching, not semantic proof.
- I did not apply the round-19 tripwire drafts. The evidence that tw-recall handles changing detections comes from fake tools (`T_*`), not from the real BashCVar/HelperFn classifiers.
- Not run: D5's missing-object case (partial or shallow clone), measure.py's own exposure to replace refs, and environment leakage such as an inherited `GIT_DIR`.
- Not re-run: the precision and row-validity attacks owned by RevTwRecallPrecision, RevFreshPinsCounter, CriticC2 and CriticC3. I cite them only where my probes reproduced them (`T_all`, `C_fp`).
- The scratch clone is left at `/tmp/mado-r19-SimplifyCounters-f_4fscp6` so the probes can be reproduced; it is outside the lane. I wrote nothing in the lane except this report and ran no lane git/jj writes, live gate, host probes or web fetches.

## Installs

none
