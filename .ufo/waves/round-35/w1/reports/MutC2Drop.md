# MutC2Drop — round-35 C2 counter check-drop mutation probe

Date: 2026-10-24. Seat: mado leaf (w1), lane-bound (no subagents). Scope: mutation
testing of `.ufo/waves/round-35/c2/count.py` (`PRED-C2-r35-v1`) — one mutant per
dropped check, run against scratch fixtures under
`.ufo/waves/round-35/scratch/MutC2Drop/` (`mutants/m01..m24.py`,
`fixtures/f00..f20`, `matrix.tsv`, `build.py`, `run_matrix.py`).
The committed counter was never modified: `git status --porcelain --
.ufo/waves/round-35/c2/count.py` is empty and the file is `git ls-files` tracked;
sha256 `4f0106c6a46c25912013e9b9780e1d0b5aa77f98d04455013df7a8e4bdeea11f`.

## Method

Each mutant = one exact-string replacement of the committed source (see
"Mutant diffs"; `build.py` asserts each pattern occurs exactly once). Fixtures
follow the committed `c2-donothing` control's technique: a **frozen-spec copy**
under scratch whose `clause_ledger`/`blob_ledger`/`frozen_blobs` are re-pointed
at scratch files — the committed `c2/frozen.json` is untouched. Fixture ledgers
are copies of `c1/clauses.json` with one defect each; the blob ledger is a copy
of `ledger/RevFrozenBlobs-r35.md` (or absent); `git rev-parse` still resolves
against the real repo, so blob-id checks are exercised for real.

Run shape (all 525 runs, `cwd` = repo root):

```sh
python3 -I <counter> --repo /home/vgpnk/Projects/shokunin/mado-shokunin --frozen <fixture>/frozen.json
```

Baseline, verbatim (live spec = f00 golden copy):

```text
base f00-golden              rc=0 PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
base f01-donothing           rc=1 PRED-C2-r35-v1 uncovered=1 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MISSED
```

f01 mirrors the committed `controls/c2-donothing.txt` receipt byte-for-byte in
the metric fields (`uncovered=1 retired=1 toctou_declared=1 ledger_tip_ok=1
verdict=TARGET_MISSED`, exit 1) — fixture technique matches the committed
control.

## Fixtures (21 — 20 on-disk dirs; f15 is path-only)

| Fixture | Single defect injected | Baseline |
|---|---|---|
| f00-golden | none — copy of committed ledger + ledgers | `MET` rc0 |
| f01-donothing | `entry-regular` clause stripped of `control` (committed-control parity) | `MISSED` rc1 (`uncovered=1`) |
| f02-missing-receipt | `entry-regular.control.receipt` → nonexistent path | `MISSED` rc1 |
| f03-clean-receipt | `entry-regular.control.receipt` → `controls/golden.txt` (exists, `TARGET_MET`) | `MISSED` rc1 |
| f04-retired-also-live | `r34-word-bound-1-25` re-added to `live` (with MISSED control) | `MISSED` rc1 (`retired=0`) |
| f05-retired-empty | `retired: []` | `MISSED` rc1 (`retired=0`) |
| f06-declared-extra | second `not-load-bearing`+reason clause added | `MISSED` rc1 (`toctou=0`) |
| f07-nl-no-reason-bare | extra clause, `"not-load-bearing": {}`, no control | `MISSED` rc1 (`uncovered=1`) |
| f08-nl-no-reason-with-control | `o-nofollow-open` loses `reason`, gains MISSED control | `MISSED` rc1 (`toctou=0`) |
| f09-blobledger-absent | `blob_ledger` → nonexistent path | `MISSED` rc1 (`tip_ok=0`) |
| f10-tip-absent | blob-ledger copy with `dff3941…adf2` replaced by 40 zeroes (6 sites; grep-confirmed 0 remaining) | `MISSED` rc1 (`tip_ok=0`) |
| f11-blob-id-wrong | `frozen_blobs[0].blob_id` last hex char → `0` | `MISSED` rc1 (`tip_ok=0`) |
| f12-blob-path-missing | `frozen_blobs[0].path` → nonexistent-at-tip path | `MISSED` rc1 (`tip_ok=0`) |
| f13-predicate-drift | spec `predicate` string mutated (`uncovered=0`→`uncovered<=0`) | rc2 `error=predicate-drift` |
| f14-target-drift | spec `target.uncovered` → `5` | rc2 `error=target-drift` |
| f15-frozen-absent | `--frozen` path does not exist | rc2 `error=frozen-missing` |
| f16-ledger-absent | `clause_ledger` → nonexistent path | rc2 `error=clause-ledger-missing` |
| f17-declared-other | `o-nofollow-open` undeclared+gained control; different clause declared instead | `MISSED` rc1 (`toctou=0`) |
| f18-retired-key-absent | `retired` key deleted from ledger | `MISSED` rc1 (`retired=0`) |
| f19-nl-nonempty-noreason | `o-nofollow-open`: `{"note":…}` (truthy, reasonless) + MISSED control | `MISSED` rc1 (`toctou=0`) |
| f20-extra-nl-nonempty | extra clause, truthy reasonless `not-load-bearing`, no control | `MISSED` rc1 (`uncovered=1`) |

f07/f08 (empty-dict declarations) could not discriminate m15/m16 — `{}` is falsy,
so `if nl` and `if nl and reason` agree. f19/f20 sharpen them with truthy
reasonless declarations.

## Results — every fixture that changes the outcome

Kill classes: **WM** = wrongly `TARGET_MET` (rc0) on a must-miss fixture;
**WMS** = wrongly `TARGET_MISSED` on f00-golden; **XC** = exit-class change
(clean exit-2 die → traceback rc1, or clean exit-1 MISSED → traceback), verdict
line absent.

| Mutant | Check dropped | Changing fixtures (class) | Verdict |
|---|---|---|---|
| m01-frozen-missing | `frozen_path.is_file()` guard | f15 (XC: rc2 `frozen-missing` → `FileNotFoundError` traceback, rc1) | KILLED |
| m02-predicate-drift | `spec.predicate == PREDICATE` | f13 (WM) | KILLED |
| m03-target-drift | `spec.target == EXPECTED_TARGET` | f14 (WM — mutant scores `EXPECTED_TARGET` anyway, so drifted spec goes MET) | KILLED |
| m04-ledger-missing | `ledger_path.is_file()` guard | f16 (XC: rc2 → `FileNotFoundError`) | KILLED |
| m05-nl-skip | `not-load-bearing`+reason exemption | f00 (WMS: `o-nofollow-open` counted uncovered → `uncovered=1`) | KILLED |
| m06-bare-clause | `not control → uncovered` | f01, f07, f20 (WM) | KILLED |
| m07-receipt-exists | `receipt.is_file()` disjunct | f02 (XC: clean MISSED → `FileNotFoundError`) | KILLED |
| m08-receipt-missed | `MISSED.search(receipt)` disjunct | f03 (WM: MET-receipt counted as covered) | KILLED |
| m09-retired-absent | retired id absent from live | f04 (WM) | KILLED |
| m10-toctou-exact | `declared == [toctou_clause]` → `declared != []` | f06, f17 (WM) | KILLED |
| m11-blobledger-exists | `ledger_doc.is_file()` guard | f09 (XC: clean MISSED → `FileNotFoundError`) | KILLED |
| m12-tip-in-ledger | `spec.r34_tip in text` | f10 (WM) | KILLED |
| m13-revparse-try | `CalledProcessError` catch | f12 (XC: clean MISSED → `CalledProcessError` traceback) | KILLED |
| m14-blob-id-eq | `raw != blob_id → ok=False` | f11 (WM) | KILLED |
| m15-declared-reason | `reason` required in `declared` | f19 (WM) | KILLED |
| m16-nl-reason | `reason` required in exemption | f20 (WM) | KILLED |
| m17-met-uncovered | `uncovered` term of `met` | f01, f02, f03, f07, f20 (WM) | KILLED |
| m18-met-retired | `retired` term of `met` | f04, f05, f18 (WM) | KILLED |
| m19-met-toctou | `toctou_declared` term of `met` | f06, f08, f17, f19 (WM) | KILLED |
| m20-met-tip | `ledger_tip_ok` term of `met` | f09, f10, f11, f12 (WM) | KILLED |
| m21-toctou-len1 | clause identity → `len(declared)==1` | f17 (WM) | KILLED |
| m22-retired-get | `.get("retired", [])` tolerance | f18 (XC: clean MISSED → `KeyError: 'retired'`) | KILLED |
| m23-revparse-check | `check=True` | **none** | **SURVIVED** |
| m24-control-get | `.get("control")` tolerance | f01, f07, f20 (XC: clean MISSED → `KeyError: 'control'`) | KILLED |

Verbatim discriminating outputs (from `matrix.tsv`):

```text
m01-frozen-missing       f15 rc=1 STDERR: FileNotFoundError: '…/fixtures/f15-frozen-absent/no-such-frozen.json'        [base rc=2 error=frozen-missing]
m02-predicate-drift      f13 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base rc=2 error=predicate-drift]
m03-target-drift         f14 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base rc=2 error=target-drift]
m04-ledger-missing       f16 rc=1 STDERR: FileNotFoundError: '…/fixtures/f16-ledger-absent/no-such-clauses.json'      [base rc=2 error=clause-ledger-missing]
m05-nl-skip              f00 rc=1 uncovered=1 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MISSED       [base MET]
m06-bare-clause          f01 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED uncovered=1]
m07-receipt-exists       f02 rc=1 STDERR: FileNotFoundError: '…/fixtures/f02-missing-receipt/no-such-receipt.txt'     [base clean MISSED uncovered=1]
m08-receipt-missed       f03 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED uncovered=1]
m09-retired-absent       f04 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED retired=0]
m10-toctou-exact         f06 rc=0 … verdict=TARGET_MET                                                              [base MISSED toctou_declared=0]
m10-toctou-exact         f17 rc=0 … verdict=TARGET_MET                                                              [base MISSED toctou_declared=0]
m11-blobledger-exists    f09 rc=1 STDERR: FileNotFoundError: '…/fixtures/f09-blobledger-absent/no-such-ledger.md'     [base clean MISSED tip_ok=0]
m12-tip-in-ledger        f10 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED tip_ok=0]
m13-revparse-try         f12 rc=1 STDERR: subprocess.CalledProcessError … returned non-zero exit status 128          [base clean MISSED tip_ok=0]
m14-blob-id-eq           f11 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED tip_ok=0]
m15-declared-reason      f19 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED toctou_declared=0]
m16-nl-reason            f20 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED uncovered=1]
m17-met-uncovered        f01 rc=0 uncovered=1 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED]
m18-met-retired          f04 rc=0 uncovered=0 retired=0 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED]
m19-met-toctou           f06 rc=0 uncovered=0 retired=1 toctou_declared=0 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED]
m20-met-tip              f09 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=0 verdict=TARGET_MET          [base MISSED]
m21-toctou-len1          f17 rc=0 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET          [base MISSED toctou_declared=0]
m22-retired-get          f18 rc=1 STDERR: KeyError: 'retired'                                                       [base clean MISSED retired=0]
m23-revparse-check       (all 21 fixtures) verdict/rc identical to baseline — SURVIVED
m24-control-get          f01 rc=1 STDERR: KeyError: 'control'                                                       [base clean MISSED uncovered=1]
```

## Check whose removal changes nothing

**m23 (`check=True`) — SURVIVED, and provably redundant under the remaining
checks.** With `check=False` a failing `git rev-parse` writes nothing to
stdout, so `raw = ""` and the `raw != blob["blob_id"]` equality (kept) sets
`ok = False` on exactly the same inputs the exception did. `check=True` only
matters in combination with the `try/except` (m13): it decides whether failure
arrives as an exception or as empty stdout — both land at the same `ok=False`.
No static-ledger fixture can distinguish them (a rev-parse that fails yet
prints a 40-hex blob id does not exist). The try/except is load-bearing on
exit-class grounds (m13 crashes instead of cleanly missing on f12); `check=True`
itself is dead weight for the verdict.

Every other check's removal is observed by at least one scratch fixture:
15 mutants wrongly `TARGET_MET`, m05 wrongly `TARGET_MISSED` on golden, 7
mutants change the exit-class contract (rc2→crash or clean rc1→traceback).
Note m03's kill is contract-shaped: with the drift guard gone the mutant still
compares against the code-level `EXPECTED_TARGET`, so a spec drifting `target`
silently goes MET — the guard is what makes `frozen.json` authoritative.

All 21 fixtures discriminate at least one mutant (f00 kills m05; f08 kills m19;
f07 kills m06/m17/m24; f15 kills m01; f16 kills m04).

## Mutant diffs

```diff
--- count.py
+++ m01-frozen-missing.py
     frozen_path = Path(args.frozen)
-    if not frozen_path.is_file():
-        die("frozen-missing")
+    # dropped: frozen-missing guard
     spec = json.loads(frozen_path.read_text())

--- count.py
+++ m02-predicate-drift.py
     spec = json.loads(frozen_path.read_text())
-    if spec.get("predicate") != PREDICATE:
-        die("predicate-drift")
+    # dropped: predicate-drift guard

--- count.py
+++ m03-target-drift.py
-    if spec.get("target") != EXPECTED_TARGET:
-        die("target-drift")
+    # dropped: target-drift guard

--- count.py
+++ m04-ledger-missing.py
     ledger_path = repo / spec["clause_ledger"]
-    if not ledger_path.is_file():
-        die("clause-ledger-missing")
+    # dropped: clause-ledger-missing guard

--- count.py
+++ m05-nl-skip.py
     for clause in live:
-        nl = clause.get("not-load-bearing")
-        if nl and nl.get("reason"):
-            continue
         control = clause.get("control")

--- count.py
+++ m06-bare-clause.py
         if not control:
-            uncovered += 1
-            continue
+            continue  # dropped: bare clause counts as covered

--- count.py
+++ m07-receipt-exists.py
         receipt = repo / control["receipt"]
-        if not receipt.is_file() or not MISSED.search(receipt.read_text()):
+        if not MISSED.search(receipt.read_text()):

--- count.py
+++ m08-receipt-missed.py
-        if not receipt.is_file() or not MISSED.search(receipt.read_text()):
+        if not receipt.is_file():

--- count.py
+++ m09-retired-absent.py
     for clause in retired:
-        if clause["id"] not in live_ids:
+        if True:  # dropped: retired id must be absent from live

--- count.py
+++ m10-toctou-exact.py
-    toctou_declared = 1 if declared == [spec["toctou_clause"]] else 0
+    toctou_declared = 1 if declared else 0  # dropped: exact singleton identity

--- count.py
+++ m11-blobledger-exists.py
     ledger_doc = repo / spec["blob_ledger"]
-    if ledger_doc.is_file():
+    if True:  # dropped: blob-ledger is_file guard

--- count.py
+++ m12-tip-in-ledger.py
-        if spec["r34_tip"] in text:
+        if True:  # dropped: r34 tip must appear in ledger text

--- count.py
+++ m13-revparse-try.py
-                try:
-                    raw = subprocess.run(
-                        ["git", "-C", str(repo), "rev-parse", rev_path],
-                        capture_output=True,
-                        check=True,
-                        text=True,
-                    ).stdout.strip()
-                except subprocess.CalledProcessError:
-                    ok = False
-                    break
+                raw = subprocess.run(
+                    ["git", "-C", str(repo), "rev-parse", rev_path],
+                    capture_output=True,
+                    check=True,
+                    text=True,
+                ).stdout.strip()  # dropped: CalledProcessError catch

--- count.py
+++ m14-blob-id-eq.py
-                if raw != blob["blob_id"]:
-                    ok = False
-                    break
+                # dropped: blob id equality check

--- count.py
+++ m15-declared-reason.py
-    declared = [c["id"] for c in live if (c.get("not-load-bearing") or {}).get("reason")]
+    declared = [c["id"] for c in live if c.get("not-load-bearing")]  # dropped: reason required

--- count.py
+++ m16-nl-reason.py
-        if nl and nl.get("reason"):
-            continue
+        if nl:
+            continue  # dropped: declaration must carry a reason

--- count.py
+++ m17..m20 (met conjunction terms)
-    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET)
+    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET if k != "<term>")
# <term> ∈ uncovered, retired, toctou_declared, ledger_tip_ok respectively

--- count.py
+++ m21-toctou-len1.py
-    toctou_declared = 1 if declared == [spec["toctou_clause"]] else 0
+    toctou_declared = 1 if len(declared) == 1 else 0  # dropped: clause identity

--- count.py
+++ m22-retired-get.py
-    retired = ledger.get("retired", [])
+    retired = ledger["retired"]  # dropped: absent-retired tolerance

--- count.py
+++ m23-revparse-check.py
                         capture_output=True,
-                        check=True,
+                        check=False,  # dropped

--- count.py
+++ m24-control-get.py
-        control = clause.get("control")
+        control = clause["control"]  # dropped: absent-control tolerance
```

Full per-cell outputs: `.ufo/waves/round-35/scratch/MutC2Drop/matrix.tsv`
(525 runs). Builder/runner: `build.py`, `run_matrix.py` beside it.

## Summary

- **Load-bearing against this fixture suite (23/24)**: every guard, disjunct,
  conjunction term, identity check and `.get` tolerance is observed by ≥1
  fixture — 15 mutants wrongly `TARGET_MET`, 1 wrongly `TARGET_MISSED`, 7
  change the exit-class contract.
- **Changes nothing (1/24)**: `check=True` (m23) — redundant under the kept
  `raw != blob_id` equality; removal is unobservable to any fixture.
- Fixture gap that would exist without sharpening: empty-dict declarations
  (f07/f08) cannot test the `reason` requirement — it takes a *truthy*
  `not-load-bearing` object without `reason` (f19/f20) to kill m15/m16.
