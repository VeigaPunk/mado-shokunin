# MutC2Clauses — mutation test of PRED-C2-r37-v2, before data (round 37, wave 1)

Seat: mutation-tester. Target under test: `quality/counters/c2-r37-eventq.py`
(PRED-C2-r37-v2, sha256 `6fae177fd5f42d7b28759eb08770bc1af63e8ad29c27f971978336bfde060f7a`).
Scorer: a scratch copy of `.ufo/waves/round-37/controls.py` pointed at each mutant.
Everything ran in `/dev/shm/mado37-MutC2Clauses`; no lane file was written.

**Headline.** Six mutants, one per accept-side clause: **6/6 SURVIVED** the frozen C2
controls at the level the harness asserts (control verdict + rc). Only one (`m3`) leaves any
trace at all, and that trace is text the harness does not assert. A seventh, deliberately
gross mutant (`m0`, `met = True`) is **killed 0/4**, so the suite is not vacuous — it is
blind to exactly the six clauses that decide the accept path, and stays blind until a tool
scores 10/10 on the fixtures.

---

## 1. Method

Frozen C2 control set (`.ufo/waves/round-37/controls.py:126-129`): `c2-do-nothing`,
`c2-stub-clean`, `c2-stub-grep`, `c2-stub-socket` — all four expected `TARGET_MISSED`.
The harness asserts only the counter's verdict token and exit code
(`controls.py:151-152`):

```
            got = "TARGET_MET" if "verdict=TARGET_MET" in summary else "TARGET_MISSED"
            ok = got == want and p.returncode == (0 if want == "TARGET_MET" else 1)
```

Scratch scorer = the lane `controls.py` with exactly three hunks, all in the plumbing:
the counter path becomes `MUT_COUNTER` (default: the lane counter), a `MUT_ONLY_PREFIX`
filter selects the `c2-` controls, and the totals line counts the selected set.
Control builders, expectations and the assertion are byte-identical to the frozen file:

```
-C2 = os.path.join(LANE, "quality/counters/c2-r37-eventq.py")
+C2 = os.environ.get("MUT_COUNTER", os.path.join(LANE, "quality/counters/c2-r37-eventq.py"))
+ONLY = os.environ.get("MUT_ONLY_PREFIX", "c2-")
@@ -136,8 +137,9 @@
+    SEL = [c for c in CONTROLS if c[0].startswith(ONLY)]
-        for name, counter, build, want in CONTROLS:
+        for name, counter, build, want in SEL:
@@ -156,7 +158,7 @@
-    lines.append(f"controls={len(CONTROLS)} correct={len(CONTROLS) - bad}/{len(CONTROLS)}")
+    lines.append(f"controls={len(SEL)} correct={len(SEL) - bad}/{len(SEL)}")
```

Commands (all from `/dev/shm/mado37-MutC2Clauses`):

```
python3 -I controls-scratch.py --out out/baseline.txt
MUT_COUNTER=/dev/shm/mado37-MutC2Clauses/mutants/m<N>.py python3 -I controls-scratch.py --out out/m<N>.txt
sed -E 's/ rev=[0-9a-f]+//' out/<f>.txt > out/<f>.txt.norm      # sandbox revs differ per run
diff out/baseline.txt.norm out/m<N>.txt.norm
python3 -I supplementary.py --counter mutants/m<N>.py           # field-level probes, §5
```

Tooling: none installed. `python3 -V` → `Python 3.14.8`; `git --version` → `git version 2.56.0`.

## 2. Baseline (pristine counter) — PASS

```
controls=4 correct=4/4
```

Its four C2 verdict lines reproduce the frozen receipt
(`.ufo/waves/round-37/receipts/controls-v2.txt`) byte-for-byte after rev-stripping; the only
diff is the totals line, because the scratch run selects the `c2-` subset:

```
< controls=13 correct=13/13
> controls=4 correct=4/4
```

So the scratch scorer is faithful: a mutant's receipt is comparable to the frozen one.

## 3. Mutants — one behaviour-bearing point each

Each mutant is a copy of the frozen counter with a single conjunct removed/replaced.
All seven compile (`py_compile`, `doraise=True`).

| id | clause mutated | file:line (pristine) | edit | sha256 |
|---|---|---|---|---|
| m1 | drop all `must_not` checks | `:122-124` | `- and not any(re.search(m, l) for m in must_not for l in lines)` | `134f8296…` |
| m2 | accept any rc | `:122` | `ok = (rc == want_rc` → `ok = (True` | `c12bc4e3…` |
| m3 | drop the readonly import regex | `:182` | `- and not re.search(r"^\s*(import\s+socket\b\|from\s+socket\s+import)", src, re.M)` | `c9101fc5…` |
| m4 | drop the `connect(` test | `:183` | `- and "connect(" not in src` | `387cef6d…` |
| m5 | drop the replay comparison | `:177` | `- and triples(clients) == triples(replay)` | `715e21aa…` |
| m6 | CLIENT count without subscribers equality | `:175` | `- and int(m.group(1)) == len(clients)` | `1c992936…` |
| m0 | sanity: `met = True` | `:184` | `met = passed == len(CASES) and readonly and live` → `met = True` | `ea4a2815…` |

Full hashes and diffs are in the scratch tree (`mutants/`, `out/*.norm`).

## 4. Frozen-control verdicts per mutant

| mutant | controls | correct | verdict |
|---|---|---|---|
| m1 | 4/4 ok | `controls=4 correct=4/4` | **SURVIVED** — receipt byte-identical to baseline |
| m2 | 4/4 ok | `controls=4 correct=4/4` | **SURVIVED** — receipt byte-identical |
| m3 | 4/4 ok | `controls=4 correct=4/4` | **SURVIVED** — one unasserted field drifts (below) |
| m4 | 4/4 ok | `controls=4 correct=4/4` | **SURVIVED** — receipt byte-identical |
| m5 | 4/4 ok | `controls=4 correct=4/4` | **SURVIVED** — receipt byte-identical |
| m6 | 4/4 ok | `controls=4 correct=4/4` | **SURVIVED** — receipt byte-identical |
| m0 | 0/4 ok | `controls=4 correct=0/4` | **KILLED** |

The single trace any of m1–m6 leaves is m3's, on `c2-stub-socket`:

```
< control=c2-stub-socket expect=TARGET_MISSED rc=1 ok=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=0 live=0 tool=present verdict=TARGET_MISSED
> control=c2-stub-socket expect=TARGET_MISSED rc=1 ok=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED
```

`ok=1` both sides: the harness collapses the counter's whole stdout to the verdict token, so
`readonly` flipping 0→1 is recorded in the receipt and asserted by nobody.

Harness sanity (`m0`), all four controls flip together:

```
> control=c2-do-nothing expect=TARGET_MISSED rc=0 ok=0 :: PRED-C2-r37-v2 fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MET
> control=c2-stub-clean expect=TARGET_MISSED rc=0 ok=0 :: PRED-C2-r37-v2 fixtures=2/10 readonly=1 live=0 tool=present verdict=TARGET_MET
> control=c2-stub-grep expect=TARGET_MISSED rc=0 ok=0 :: PRED-C2-r37-v2 fixtures=1/10 readonly=1 live=0 tool=present verdict=TARGET_MET
> control=c2-stub-socket expect=TARGET_MISSED rc=0 ok=0 :: PRED-C2-r37-v2 fixtures=2/10 readonly=0 live=0 tool=present verdict=TARGET_MET
> controls=4 correct=0/4
```

## 5. Why they survive — the structural reason, then field-level proof

`met = passed == len(CASES) and readonly and live` (`c2-r37-eventq.py:184`). Fixtures are
all-or-nothing: every frozen C2 control's tool scores ≤ 2/10 (`controls-v2.txt`:
`fixtures=2/10`, `1/10`, `2/10`, `0/10`), so the deciding conjunct is always
`passed == len(CASES)` and the other three can never change the verdict. The live clause is
additionally unreachable: no control commits `receipts/eventq-live.txt` /
`eventq-live-ss.txt`, and the block is guarded by `blob is not None and receipt is not None
and snap is not None` (`:155`), so `live=0` everywhere.

To show each clause is nevertheless load-bearing — and to name the control that would kill
it — I built six **proposed** supplementary controls (`supplementary.py`): a minimal git repo
per probe containing only the files the counter reads, with a crafted tool and/or a crafted
receipt pair, scored by the same counter at `HEAD`. `rev` below is the probe repo's commit.

| probe (crafted input) | pristine | detected by |
|---|---|---|
| `rc-wrong-exit` — right lines, `sys.exit(3)` | `fixtures=0/10` | m2 → `fixtures=2/10` |
| `must-not-setup-clean` — prints `MADO_EVENTQ: SETUP …` **and** a `verdict=CLEAN` summary, exits 2 | `fixtures=0/10` | m1 → `fixtures=2/10` |
| `connect-in-text` — read-only tool whose text contains `connect(` | `readonly=0` | m4 → `readonly=1` |
| `import-socket` — read-only tool with `import socket` | `readonly=0` | m3 → `readonly=1` |
| `live-replay-mismatch` — receipt CLIENT set not reproducible from the raw snapshot | `live=0` | m5 → `live=1` |
| `live-subscribers-mismatch` — receipt `subscribers=3`, two CLIENT lines | `live=0` | m6 → `live=1` |

Quoted pairs (pristine → killer), `out/supplementary.txt`:

```
probe=rc-wrong-exit counter=pristine-c2.py rc=1 :: PRED-C2-r37-v2 fixtures=0/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=3c9e230781ac97a2ac8fc2825bc6fb44d756766a
probe=rc-wrong-exit counter=m2.py rc=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=b1226e05548026e0759265a3620a7df1978aa6ee
probe=must-not-setup-clean counter=pristine-c2.py rc=1 :: PRED-C2-r37-v2 fixtures=0/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=e93606ba5c79b000d0142fe6a3b380f425926d01
probe=must-not-setup-clean counter=m1.py rc=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=3e66e828cd0e23557a43c24bdc6bec4b95bc5d0a
probe=connect-in-text counter=pristine-c2.py rc=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=0 live=0 tool=present verdict=TARGET_MISSED rev=dbb8cba644d6edeab7783d7bd6c37481a51b9d82
probe=connect-in-text counter=m4.py rc=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=03d842aea4908f0f23005ad8814bea31e9e3a89e
probe=import-socket counter=pristine-c2.py rc=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=0 live=0 tool=present verdict=TARGET_MISSED rev=c1298a41f7d2c3fe6940903ffdccaf96762761f5
probe=import-socket counter=m3.py rc=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=935db7eff729d3d52e2dacf21fcdceabb22dbf71
probe=live-replay-mismatch counter=pristine-c2.py rc=1 :: PRED-C2-r37-v2 fixtures=1/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=9e335fa00fe2056be3770e17f588cc740d2a5287
probe=live-replay-mismatch counter=m5.py rc=1 :: PRED-C2-r37-v2 fixtures=1/10 readonly=1 live=1 tool=present verdict=TARGET_MISSED rev=ce4bb854b0a853976f0c54ac919c7097a7d17c36
probe=live-subscribers-mismatch counter=pristine-c2.py rc=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=1 live=0 tool=present verdict=TARGET_MISSED rev=4f67e337b911ac4d9f83c1711bad6a32ee2effdb
probe=live-subscribers-mismatch counter=m6.py rc=1 :: PRED-C2-r37-v2 fixtures=2/10 readonly=1 live=1 tool=present verdict=TARGET_MISSED rev=d7fa9af40d02df249647fdb28caa351a89d6dcc0
```

Every probe still ends `verdict=TARGET_MISSED` — the clauses are load-bearing for the
*fields*, not (yet) for the verdict. One cross-drift to record rather than hide:
`must-not-setup-clean` under m2 reads `fixtures=1/10`, not 0 — the `decoy` case passes once rc
is ignored, which is the rc clause leaking into that probe, not evidence about `must_not`.

## 6. Which clauses are unexercised before data

All six accept-side clauses, and for two distinct reasons:

1. **Masked by all-or-nothing fixtures** (`:184`) — `must_not` (m1), `rc` (m2), readonly-import
   (m3), readonly-`connect(` (m4): no frozen control's tool is above 2/10, so these can never
   be the deciding conjunct. No control currently isolates rc at all: none of the four stubs
   has correct `must` output with a wrong exit code.
2. **Unreachable code path** (`:155`) — replay comparison (m5) and subscribers equality (m6):
   no control commits a live receipt pair, so `live` is computed nowhere and the guard makes
   both conjuncts dead for the whole control run.

## 7. What the post-data residual must add

- **R1 — assert the field, not only the verdict** (`controls.py:151-152`). The receipt already
  carries `readonly=`; asserting `readonly=0` on `c2-stub-socket` kills **m3** with zero new
  fixtures. Add a `connect(`-bearing read-only stub (`c2-stub-connect`, probe
  `connect-in-text`) and assert `readonly=0` → kills **m4**. Neither needs a passing tool.
- **R2 — commit a live receipt pair in a control.** Add `c2-live-replay-decoy` (receipt CLIENT
  set not reproducible from the committed raw snapshot) and `c2-live-subscribers-decoy`
  (`subscribers=` ≠ CLIENT count), both asserting `live=0` → kills **m5** and **m6**. Still no
  passing tool required; this is the only way to reach `:155` before the tool exists.
- **R3 — two fixture-level controls for the masked conjuncts.** `c2-rc-wrong-exit` (correct
  lines, exit 3) and `c2-must-not-setup-clean` (SETUP line plus a `verdict=CLEAN` summary,
  exit 2), each asserting the exact `fixtures=` count → kills **m1** and **m2**.
- **R4 — the verdict-level control, only possible post-data.** Once `tools/mado-eventq.py`
  passes 10/10, add six near-miss controls: the delivered tool with exactly one defect each
  (wrong rc on one case; a `must_not`-matching line; `import socket`; a `connect(` string; a
  receipt the snapshot cannot replay; a receipt whose `subscribers=` disagrees with its CLIENT
  lines). All six must MISS. These are the only controls that test these clauses at the
  verdict level, because fixtures are all-or-nothing.

R1–R3 are cheap and pre-data; R4 is the post-data residual this mutation round argues for.

## 8. Restoration and bounds

- Lane counter untouched: `sha256sum quality/counters/c2-r37-eventq.py` →
  `6fae177fd5f42d7b28759eb08770bc1af63e8ad29c27f971978336bfde060f7a`, identical before and
  after every run (the scratch copy `pristine-c2.py` carries the same digest).
- `git -C <LANE> status --porcelain` shows only sibling seats' untracked
  `w1/reports/*.md` and `w1/scratch/`; this seat wrote no lane file except this report.
- No compositor contact: no `hyprctl`, no socket connection, no `ss` live call — every input
  to the counter came from the fixtures embedded in it or from probe files in `/dev/shm`.
  No pacman transaction, no subagent, no `model` parameter.
- Scratch retained for audit at `/dev/shm/mado37-MutC2Clauses` (`pristine-c2.py`,
  `controls-scratch.py`, `supplementary.py`, `mutants/*.py`, `out/*.txt`), all hashes listed
  above.
- One transient environment fault, reported rather than smoothed over: the first m4/m0 runs
  aborted with `OSError: [Errno 122] Disk quota exceeded` inside `/dev/shm` while sibling
  seats were cloning (a write during `build(sb)`); both were re-run sequentially and the
  quoted receipts come from the completed runs. The aborted attempts left no receipt (the
  harness removes its temp root in `finally`).
