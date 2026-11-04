# R68ExecHazard — repair check-axis-scores.py + hazard probe + harness measurement

Seat: R68ExecHazard (w1, round 68). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Base rev: 510100c81e6cf63fec6be380c2f2f9c670f32cbc. Freeze: e0727cda15621766c35dcf8b70c211b6531aab45.
No lane git mutation. Only writes: this seat dir, this report, scratch (removed).

## 1. Draft repair — quality/check-axis-scores.py

Draft: `.ufo/waves/round-68/w1/R68ExecHazard/draft/check-axis-scores.py`
sha256: `71faf4b50639de6998a59ae6f3f74eb76c498b94a97a37e0b9d63c87fb1e0dbf` (11754 bytes)
Base file sha256: `461f913a4d1dc8ba19aebee00bbafdb70ad7be09f3531008896c3d9569ce8dde` (297 lines)

Both git environments now carry the guard via an env-named binding + subscript store
(frozen shape (b)); `python3 -m py_compile` OK; `--selftest` 18/18.

Diff (only these two hunks):

```diff
@@ -95,8 +95,10 @@
 def git(repo, *args):
+    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
+    env["GIT_NO_REPLACE_OBJECTS"] = "1"
     return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True,
-                          env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
+                          env=env)
@@ -116,9 +118,11 @@
         try:
+            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
+            env["GIT_NO_REPLACE_OBJECTS"] = "1"
             p = subprocess.run([sys.executable, "-I", f] + list(args), cwd=repo,
                                capture_output=True, text=True, timeout=timeout,
-                               env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
+                               env=env)
```

Behaviour-identical (replace-free lane, base rev):
```
python3 -I base-gate-cmp.py --selftest                                  -> rc 0, MADO_AXIS_SELFTEST: 18/18 assertions passed
python3 -I draft/check-axis-scores.py --selftest                        -> rc 0, identical output (diff empty)
python3 -I base-gate-cmp.py --repo LANE --rev 510100c8...               -> rc 1, output byte-identical to draft
python3 -I draft/check-axis-scores.py --repo LANE --rev 510100c8...     -> rc 1, output byte-identical (diff empty)
```
(rc 1 in both from the pre-existing published/navigation mismatch at that rev:
`MADO_AXIS: checked=3 mismatched=1 rev=510100c8...`.)

## 2. Hazard probe (auxiliary, outside frozen denominator)

Driver: scratch `probe.py` (removed). Fixture: scratch git repo under my scratch root;
`git init -q`, `rev-parse --show-toplevel` asserted equal to the fixture dir, commit
`f.txt = "original bytes\n"`, `orig = rev-parse HEAD:f.txt`, `forged = git hash-object -w --stdin`
with `"forged bytes\n"`, `git replace <orig> <forged>`.

Object ids: orig=`4b085e39db3d2c61b607f5533031cb122d63393b`, forged=`59ff15d5a0f32e6a4954335eb687c9a8c731b28e`.

Module loaded with importlib (`spec_from_file_location`, exec_module) — base bytes read from
`git show 510100c8:quality/check-axis-scores.py`, draft from the seat dir. Helper called as
`mod.git(D, "cat-file", "-p", orig)` and gate read path `mod.show(D, "HEAD", "f.txt")`.

Clean (no replace ref), both modules:
- base.git  -> rc 0, stdout `original bytes\n`
- draft.git -> rc 0, stdout `original bytes\n`
- base.show / draft.show -> `original bytes\n`

Planted `git replace`:
- raw `git -C D cat-file -p $orig` -> `forged bytes\n`
- `GIT_NO_REPLACE_OBJECTS=1 git -C D cat-file -p $orig` -> `original bytes\n`
- **base** `mod.git(D,"cat-file","-p",orig)` -> rc 0, `forged bytes\n` (differs from its clean run)
- **draft** same call -> rc 0, `original bytes\n` (equals its clean run)
- base `mod.show(D,"HEAD","f.txt")` -> `forged bytes\n`; draft -> `original bytes\n`

Census classifier (committed `quality/counters/c2-r68-reader-guard.py`, `classify()`):
base `(reader=True, guard=False)`, draft `(reader=True, guard=True)`.
All 12 asserted probe checks passed; probe rc 0.

Counter-level receipt: scratch clone of the lane with only the draft copied in and committed
(clone HEAD `42837f439a8621d6328ef801c86be29024eb7762`, toplevel asserted):
```
MADO_R68_READER file=quality/check-axis-scores.py reader=yes guard=yes
MADO_R68_READER_GUARD: population=20 readers=13 guarded=2 unguarded=11 controls=11/11 verdict=TARGET_MISSED rev=42837f43...
```
Base counter run reproduced the frozen baseline:
```
python3 -I quality/counters/c2-r68-reader-guard.py --repo . --rev 510100c8... \
  --controls .ufo/waves/round-68/controls/c2-controls.json
MADO_R68_READER_GUARD: population=20 readers=13 guarded=1 unguarded=12 controls=11/11 verdict=TARGET_MISSED rev=510100c8...
rc 1
```

### Finding for L1 (not fixed here: frozen counter, not this seat)
The frozen counting command passes `--scratch-root DIR`, but the committed
`quality/counters/c2-r68-reader-guard.py` (e0727cda) has no such argparse option; the exact
declared invocation exits 2 with `unrecognized arguments: --scratch-root ...`. Its docstring
advertises the flag, so the counter and the counting command disagree. Without the flag the
counter works as shown above. Message sent to L1 (`agent://MadoR68`).

**Erratum (L1, recorded in `.ufo/waves/round-68/c2-command-erratum-r68.txt`, declaration not
edited):** the frozen-command mismatch above was accepted as an instrument gap. Committed bytes
at e0727cda sha256 `8eb99a63e324fce18eda824d7aefa48d72650ff6abb7c4afa45def9191ce880e`; the
counter now accepts `--scratch-root` (interface parity; it writes nothing) and its selftest
asserts the frozen argument set parses. Re-run exactly as declared after the fix:

```
python3 -I quality/counters/c2-r68-reader-guard.py --repo . --rev 510100c8... \
  --controls .ufo/waves/round-68/controls/c2-controls.json --scratch-root <scratch>/census2
MADO_R68_READER_GUARD: population=20 readers=13 guarded=1 unguarded=12 controls=11/11 verdict=TARGET_MISSED rev=510100c8...
rc 1   (TARGET_MISSED as required at the base rev)
python3 -I quality/counters/c2-r68-reader-guard.py --selftest --scratch-root <scratch>/census2
MADO_R68_READER_GUARD_SELFTEST: 18/18 assertions passed
rc 0
```

I did not edit the counter.

## 3. Real harness measurement

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r68-landing-controls.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev 510100c81e6cf63fec6be380c2f2f9c670f32cbc \
  --scratch-root /fast/scratch/hyaku/mado-r68/R68ExecHazard/harness
```
rc 0. Exact mutant + final lines:
```
MADO_R68_MUTANT M-Z path=quality/landing-counters.sh clause_count=1 recipe=clause-delete removed='[ "$citations" -gt 0 ] && ' from_sha256=4378fd8c278126111ad6d970ac20215c170238ffe1a796c5c7d03c9e5b3b93a9 rc=1 failed_assertions=3 assertions=59/62 killed=yes sha256=a6255a00262cc2f1790f813927dd5fa8ed9910e74d1ec19a8662e88df0fe0118
MADO_R68_MUTANT M-R path=tools/mado-receipt-citecheck.py guard_count=1 recipe=line-delete removed_line='            env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),\n' from_sha256=3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0 rc=0 verdict=TARGET_MET missing=0 forged_credit=yes killed=yes sha256=414ca759232a3d31451f86060f4b0ba3382dd151f4bffe797793cb2ced5cee11
MADO_R68_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=510100c81e6cf63fec6be380c2f2f9c670f32cbc
```
Wall clock 1.55 s.

## Scratch
`/fast/scratch/hyaku/mado-r68/R68ExecHazard/` removed on exit (fixture, probe driver, base copy,
behaviour outputs, harness root, census clone). Verified absent below.
