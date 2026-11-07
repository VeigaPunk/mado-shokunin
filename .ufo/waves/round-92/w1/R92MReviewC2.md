# R92MReviewC2 — review of the C2 candidate against R91MResidC2 F1–F5

Seat: reviewer, round 92, wave w1. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base rev
`d992ef7494b054591ee9104df1da49264678df5d`. Scratch `S=/fast/scratch/hyaku/mado-r92/R92MReviewC2`
(deleted on exit; reproducer sources are inlined in §6). No lane file was written except this report.
All runs marked **DRAFT**; no measurement was performed and nothing was written under `receipts/`.

Axes named: **C2 operability** (the gate's ability to name a lost seat report) and, secondarily,
**evidence integrity** of the battery (whether the frozen fixtures can tell a fixed gate from a broken one).
No C1 tool was read.

Artifacts reviewed (sha256 at review time):

| file | sha256 |
|---|---|
| `quality/check-seat-reports.py` (base gate, 309 ln) | `13c4b0a7dc4bbc39c70731dd35ec1f312c09f1a48f3b620e02945184d9cce39a` |
| `.ufo/waves/round-92/build/check-seat-reports.c2.py` (candidate, 376 ln) | `be47235bf6b8d2cb8f38bd1740e977ccdc4066dd33e732876625b66546e4a876` |
| `.ufo/waves/round-92/controls/gate-defects-battery-r92-l1.json` (28 fixtures) | `73ae3bde695c8e7a6c34ccd99c55586c360b41c98f5d8fd50d2373e5270392d0` |
| `.ufo/waves/round-92/controls/gate-defects-mutants-r92-l1.json` (14 mutants) | `689e17fa7d2143b56abca5bd43804470e7d0a3d25a8e74b96e612bed9e4d742f` |
| `.ufo/waves/round-92/controls/r91-c2-argv-r92.json` | `d21b1979b8b42203c8d9c8d033ec71af8027ff79911adc348cddb9685df4b604` |

Diff against the base: 183 lines (`.ufo/waves/round-92/build/check-seat-reports.c2.py` vs
`quality/check-seat-reports.py`) — five fix clusters, seven new selftest cases, one docstring paragraph.

**Verdict: the candidate closes F1–F5 as the round-91 defect report stated them, in both modes where a
mode exists, each fail-closed; it changes no behaviour the round-91 frozen set expects; its stdout is
still parsed by the round-91 `FIND` regex. Two residual holes of the same failure class survive outside
F1's wording, and the battery cannot see one line of the F2 fix. No finding makes `TARGET_MET` false.**

---

## 1. Per-defect verdict

Legend: *both modes* / *fail-closed* / *defect-report conformity* / *evidence*.

### F1 — a dispatch stored as a symlink is silently skipped in `--rev` (`waves=1 … verdict=OK`)

* **Fixed in both modes.** `GitTree.paths()` (`candidate:85-87`) now enumerates `list(self.sizes) +
  sorted(self.links)`; `GitTree.check_dispatch` (`:89-93`) raises `SetupError("… dispatch is a symlink,
  not a regular file")` for a `120000` entry, and `WorkTree.check_dispatch` (`:120-130`) raises the same
  for an `os.path.islink` path. `check()` calls `tree.check_dispatch(p)` before every read (`:186-189`).
* **Fail-closed:** yes — rc 2 with no findings, not a silent OK.
* **Defect-report conformity:** matches §5 F1's stated correction (`self.sizes ∪ self.links`, non-blob
  dispatch → `SetupError`).
* **Evidence (DRAFT):** battery `F1-01..F1-05` all `ok` (two rev/second-wave, worktree, only-wave,
  `--all`/round-8, dangling). Direct reproducer P15 of the round-91 report now returns rc 2 in both
  modes. Mutants `N01` (blobs-only paths), `N02` (rev symlink accepted) and `N05`
  (`check_dispatch` never called) are all killed.

### F2 — a seat name or path prints raw (spaces split the record, non-UTF-8 bytes kill the counter)

* **Fixed as an output contract, deliberately narrower than the report's literal wording.** `tok()`
  (`:162-166`) emits a printable-ASCII token unchanged and anything else as
  `json.dumps(..., ensure_ascii=True)` with literal spaces rewritten to `\u0020`; it is applied to the
  seat name once (`:200`) and to the report path in both the SR03 branch (`:213`) and before
  SR01/SR02 (`:217`). Because plain tokens are untouched, the round-91 frozen byte expectations do not
  move (the report's own correction — "render seat and path with `json.dumps`" — would have rewritten
  every plain line and killed the frozen set; the candidate's conditional form is the only shape that
  satisfies both).
* **Fail-closed:** n/a (output rendering); every emitted line is now ASCII and whitespace-splittable.
* **Evidence (DRAFT):** battery `F2-01..F2-05` `ok` (space, newline with an embedded fake `SR02 empty`
  record, non-ASCII path, lone surrogate `\udcff`, tab in rev). Mutants `N06` (raw tokens), `N07`
  (`ensure_ascii=False`), `N08` (spaces left inside the JSON string), `N12` (name not tokenised) and
  `N13` (path not tokenised) are killed. The round-91 counter's `run_check` (`text=True`) no longer sees
  a `0xff` byte: the F2-04 fixture passes `meets()`, whose first test is `raw.isascii()`.
* **Residual (battery, not candidate):** the battery has **no fixture on the SR03/SR02/untrailed line
  kinds with a non-ASCII path**, so the `rp = tok(rp)` at `:213` (SR03 branch) is invisible. I deleted
  exactly that line and re-scored the frozen battery: **28/28 still met** (§4). The candidate is correct
  here; a future implementation that tokenised only SR01/SR02 would pass the battery.
* **Residual (cosmetic):** a printable-ASCII token that *contains* `"` mid-string (e.g. `A"B`) is emitted
  raw, so the field is not round-trippable through `json.loads`. It is still one `\S+` token, which is all
  the documented grammar needs; a token that *starts* with `"` is correctly quoted, so it cannot be
  confused with a JSON string.

### F3 — a repeated `--round N` double-counts

* **Fixed.** `rounds = sorted(set(rounds))` in `check()` (`:176`), before the `--all` branch and the
  summary counters.
* **Evidence (DRAFT):** battery `F3-01..F3-03` `ok` (twice, twice in rev with two rounds, three times
  with rc 0); mutant `N09` (`list(rounds)`) killed.

### F4 — a FIFO at a dispatch path blocks `--worktree` forever

* **Fixed for FIFOs and devices.** `WorkTree.check_dispatch` stats the path before any read and raises
  for a non-regular file (`:125-130`); the same call site guards every wave (`:188`).
* **Fail-closed:** yes, rc 2, no hang (the counter's 20 s timeout never fires).
* **Evidence (DRAFT):** battery `F4-01..F4-03` `ok` (only wave, second wave, `--all`); mutant `N04`
  (type unchecked) killed.
* **Finding (see §2):** the docstring added at `:32-33` claims "a FIFO/device/**directory** in
  `--worktree`" is a setup error. Directories are *not* caught — they are silently skipped, which is the
  same failure F4 was raised to stop.

### F5 — a report reached through a parent-directory symlink leaving the repo counts as present in `--worktree`

* **Fixed in worktree mode.** `WorkTree.inside()` compares `os.path.realpath` against
  `realpath(repo) + os.sep` (`:116-118`); `is_link()` now returns true for a path whose real location
  leaves the repo (`:146-148`), so such a report is SR03 unsafe. `--rev` already said SR01 for the same
  layout; the verdict direction (non-OK) now agrees.
* **Evidence (DRAFT):** battery `F5-01..F5-04` `ok` (parent link, grandparent link through `<root>/..`,
  mixed present+unsafe, and the `<tree>-sibling` **string-prefix** case). Mutants `N10`
  (`inside` always true), `N11` (report containment dropped) and `N14` (`startswith(self.real)` without
  the separator — the sibling-prefix bug) are killed.
* **Residual:** the two readers still *label* the same tree differently — worktree `SR03 unsafe`, rev
  `SR01 missing` (battery `F5-01` vs `P-06` codify this). Both are findings and the verdict is MISSING in
  both, so no wave is lost; the round-91 report only asked worktree to stop calling it present. Diagnosis
  text differs by mode; I would not change it without a new predicate.

---

## 2. Finding 1 (medium, candidate: claim vs behaviour) — a *directory* at a dispatch path is still silently skipped

`candidate:32-33` (docstring, added this round):

> a dispatch that is not a regular file — a symlink in either mode, a FIFO/device/directory in
> `--worktree` — so neither mode skips or blocks on one

That is false for directories, and for symlinks pointing at directories. `WorkTree.paths()` (`:132-138`)
enumerates `os.walk(...)[files]` only; a directory named `w1-dispatch.json` is yielded in `dirs`, and
`os.walk` has `followlinks=False`, so a `w1-dispatch.json` symlink to a directory is also never yielded.
`GitTree.paths()` enumerates blobs and symlinks, and git stores a directory as a tree entry that
`ls-tree -r` does not list.

Reproducer (battery `{"files": {...}}` shape, worktree; full driver in §6-A). Tree:
`.ufo/waves/round-7/w1-dispatch.json/` is a directory, `.ufo/waves/round-7/w2-dispatch.json` is a healthy
dispatch for seat B whose report exists.

```
$ python3 -I <candidate> --repo <tree> --worktree --round 7
SEAT_REPORTS: mode=worktree rev=worktree rounds=1 waves=1 seats=1 trailered=1 present=1 missing=0
  empty=0 unsafe=0 untrailed=0 verdict=OK          rc=0
```

`waves=1`, not 2: wave `w1` was dropped with no finding at all — the M90-4 class the gate exists to
prevent. The base gate behaves identically (`rc=0`, `waves=1`), so this is **not a regression**; it is a
hole the candidate introduced in prose and left open in code. The counter's `build()` already supports
`{"dir": true}` (`quality/counters/c2-r92-gate-defects.py:65-66`) but **no battery fixture uses it**.

Smallest correction: in `WorkTree.paths()`, also yield directories whose name matches `DISPATCH`
(`for d in dirs: if d.endswith("-dispatch.json")`) and let `check_dispatch` reject them with the existing
`not a regular file` message; or narrow the docstring to "a FIFO/device in `--worktree`". Either way the
battery needs the `{"dir": true}` fixture, otherwise nothing measures which one was chosen.

## 3. Finding 2 (low, candidate: residual of F1's class, not in F1's wording) — a gitlink dispatch is skipped in `--rev`

`GitTree` classifies `120000` as a link and everything else that is a `blob` as a report; a `160000`
(gitlink/submodule) entry is neither, so `paths()` never sees it and `check_dispatch`'s
`if path not in self.sizes` branch (`:92-93`) is unreachable. Reproducer §6-B:
`.ufo/waves/round-7/w1-dispatch.json` created with `git update-index --cacheinfo 160000,<sha>,<path>` →
`--rev HEAD --round 7` → `rc=0 … waves=1 … verdict=OK` (the other wave checks out). Base identical.
Cheap fix: add `160000` entries to a `self.links`-style set or to `paths()` and let `check_dispatch` raise
— one line, same message. Low severity: a gitlink at a dispatch path cannot arise from normal tooling.

## 4. Round-91 frozen set: unchanged (DRAFT)

```
$ python3 -I quality/counters/c2-r91-seat-reports.py --repo . --rev d992ef74… --base-rev cc0381db…
  --set …/seat-reports-set-r91.json --mutants …/seat-reports-mutants-r91.json
  --expect-set-sha256 9a05fa8a… --expect-mutants-sha256 7cf06df7… --fresh 60
  --scratch-root $S/r91 --draft-check .ufo/waves/round-92/build/check-seat-reports.c2.py
MADO_SEAT_REPORTS: DRAFT_TARGET_MET pred=PRED-C2-r91-v1 rev=draft:…c2.py base_rev=cc0381db…
  expectations=59 met=59 fresh=60/60 fresh_seed=3192333147
  selftest=ok:SEAT_REPORTS_SELFTEST: checks=23 failed=0 mutants=55 killed=55
  base_met=0 always_ok_met=5 always_missing_met=0 receipt_presence_met=11
  check_sha256=be47235b…e4a876
rc=3   (118 s)                     ← 3 is the DRAFT exit code of the counter
```

59/59 set expectations (which include exact finding lines and summary fields), 55/55 mutants,
fresh 60/60, base control 0. No round-91 expectation moves.

**Parseability by the round-91 `FIND` regex on plain names.** Beyond the 59 expectations I ran the
candidate on the real lane at the measured rev and re-parsed every finding with
`quality/counters/c2-r91-seat-reports.py`'s `FIND`/`SUM`:

```
$ python3 -I <base>   --repo . --rev d992ef74… --all > lane-base-rev.txt   rc=1
$ python3 -I <cand>   --repo . --rev d992ef74… --all > lane-cand-rev.txt   rc=1
$ diff lane-base-rev.txt lane-cand-rev.txt        → IDENTICAL (134 lines)
SEAT_REPORTS: mode=rev rev=d992ef74… rounds=47 waves=63 seats=1748 trailered=1748 present=1615
  missing=133 empty=0 unsafe=0 untrailed=0 verdict=MISSING
findings 133, FIND-unparsed 0, SUMMARY-matched 1
```

Byte-identical to the base on the lane's own tree, so the added symlink enumeration is inert there (the
lane has 64 `120000` entries under `.ufo/waves` and **none** is named `*-dispatch.json`:
`git ls-tree -r d992ef74 .ufo/waves | awk '$1=="120000"' | grep -cE '/[A-Za-z0-9_-]+-dispatch\.json$'` → 0).
A quoted token also parses: `FIND.match('SR01 missing round-7/r1 "A\\u0020b\\nc" "\\u00e9.md"')` → True.

## 5. Battery + predicate audit (DRAFT)

```
$ python3 -I quality/counters/c2-r92-gate-defects.py --repo . --rev d992ef74… --base-rev d992ef74…
  --battery …/gate-defects-battery-r92-l1.json --expect-battery-sha256 73ae3bde…
  --mutants …/gate-defects-mutants-r92-l1.json --expect-mutants-sha256 689e17fa…
  --r91-argv …/r91-c2-argv-r92.json --expect-r91-argv-sha256 d21b1979…
  --scratch-root $S/c2b --draft-check .ufo/waves/round-92/build/check-seat-reports.c2.py
MADO_GATE_DEFECTS: DRAFT_TARGET_MET pred=PRED-C2-r92-v1 rev=draft:…c2.py base_rev=d992ef74…
  fixtures=28 met=28 F1=5/5 F2=5/5 F3=3/3 F4=3/3 F5=4/4 P=8/8
  selftest=ok:SEAT_REPORTS_SELFTEST: checks=23 failed=0 mutants=14 killed=14
  base_met=8 always_ok_met=3 always_refuse_met=8 r91_counter=TARGET_MET
  check_sha256=be47235b…e4a876
r91: MADO_SEAT_REPORTS: DRAFT_TARGET_MET … expectations=59 met=59 fresh=60/60 mutants=55 killed=55
rc=3   (242 s)
```

Per-fixture base-vs-candidate matrix (same `build`/`run_check`/`meets` code imported from the counter,
plus an ad-hoc mutation that deletes only the SR03 `tok` line):

```
fixture                            class  base cand  noSR03tok  expect_rc
F1-01-rev-second-wave-link         F1     F    T     T          rc=2
F1-02-worktree-second-wave-link    F1     F    T     T          rc=2
F1-03-rev-only-wave-link           F1     F    T     T          rc=2
F1-04-rev-all-link-in-round-8      F1     F    T     T          rc=2
F1-05-rev-dangling-link            F1     F    T     T          rc=2
F2-01-name-with-space              F2     F    T     T          rc=1
F2-02-name-with-newline            F2     F    T     T          rc=1
F2-03-non-ascii-path               F2     F    T     T          rc=1
F2-04-lone-surrogate-path          F2     F    T     T          rc=1
F2-05-name-with-tab-rev            F2     F    T     T          rc=1
F3-01-round-twice                  F3     F    T     T          rc=1
F3-02-round-twice-rev              F3     F    T     T          rc=1
F3-03-round-thrice-ok              F3     F    T     T          rc=0
F4-01-fifo-only-wave               F4     F    T     T          rc=2
F4-02-fifo-second-wave             F4     F    T     T          rc=2
F4-03-fifo-all                     F4     F    T     T          rc=2
F5-01-parent-link-outside          F5     F    T     T          rc=1
F5-02-grandparent-link-outside     F5     F    T     T          rc=1
F5-03-parent-link-outside-and-ok   F5     F    T     T          rc=1
F5-04-parent-link-to-prefix-siblingF5     F    T     T          rc=1
P-01-worktree-ok                   P      T    T     T          rc=0
P-02-rev-missing                   P      T    T     T          rc=1
P-03-rev-symlinked-report          P      T    T     T          rc=1
P-04-untrailed-and-empty           P      T    T     T          rc=1
P-05-parent-link-inside            P      T    T     T          rc=0
P-06-rev-parent-link-outside       P      T    T     T          rc=1
P-07-plain-name-unquoted           P      T    T     T          rc=1
P-08-rev-all-ok                    P      T    T     T          rc=0
base_total 8   cand_total 28   n 28
```

* **Expectations vs the defect report:** every F expectation is the answer the round-91 report named as
  the correction (rc 2 for a symlinked or non-regular dispatch, `rounds=1` for a repeated `--round`,
  SR03 for a report reached outside the repo, one ASCII token per field, one line per finding). No
  expectation contradicts §5 of `R91MResidC2.md`.
* **"must fail at base":** satisfied — the base gate meets exactly the 8 `P` fixtures and **0 of the 20
  `F` fixtures**; there is no `F`-class fixture that the base already passes.
* **Mode coverage:** complete. F1 both modes; F2 both (F2-05 is rev); F3 both; F4 worktree only — correct,
  `--rev` cannot store a FIFO; F5 worktree with `--rev` handled by `P-06`.
* **Provenance:** the battery and its generator were rewritten at 23:01:29 during this wave (a 27-fixture
  version, sha `c923ac17…`, existed when I started; `F5-04` was added). Re-running
  `python3 .ufo/waves/round-92/controls/gen-c2-battery-r92.py <out>` now yields
  `73ae3bde695c8e7a6c34ccd99c55586c360b41c98f5d8fd50d2373e5270392d0`, byte-identical to the committed
  JSON, so the generator and the artifact agree **as of this read**. The freeze must pin `73ae3bde…`,
  not any earlier value; `F5-04` is the only fixture that kills `N14`.
* **Weak spot (battery):** `F4-0x`'s `contains=["not a regular file"]` is also a substring of the symlink
  message (`"… dispatch is a symlink, not a regular file"`), which is why the `always_refuse` control
  meets all 8 rc-2 fixtures (`always_refuse_met=8`). Discrimination for F1/F4 therefore rests entirely on
  mutants N01–N05, not on the battery; a distinct FIFO message (e.g. `"not a regular file (mode=…)"`)
  or `contains=["FIFO"]` would give the control leg teeth.
* **Weak spot (battery):** no `{"dir": true}` fixture (supported by `build()`), which is exactly the hole
  in §2; and no F2 fixture on the SR03/SR02/untrailed line kinds (§1 F2 residual).

## 6. Reproducers

**A — directory at a dispatch path (`--worktree`; also reproduces with a symlink-to-directory).**

```python
d = mk()                                             # .ufo/waves/round-7/w1-dispatch.json/  is a DIRECTORY
write(f"{d}/.ufo/waves/round-7/w1-dispatch.json/.keep", "")
write(f"{d}/.ufo/waves/round-7/w2-dispatch.json", disp(task("B", ".ufo/waves/round-7/w2/B.md")))
write(f"{d}/.ufo/waves/round-7/w2/B.md", "y")
run(check, d, ["--worktree", "--round", "7"])        # rc 0, waves=1  (w1 vanished, no finding)
# variant D: os.symlink("realdir", f"{d}/.ufo/waves/round-7/w1-dispatch.json")  -> rc 0, waves=1
```

**B — gitlink at a dispatch path (`--rev`).**

```python
git -C $D init -q; assert toplevel == $D; commit w2-dispatch.json + w2/B.md
sha = git -C $D rev-parse HEAD
git -C $D update-index --add --cacheinfo 160000,$sha,.ufo/waves/round-7/w1-dispatch.json
run(check, $D, ["--rev","HEAD","--round","7"])       # rc 0, waves=1  (gitlink dispatch skipped)
```

**C — symlinked round directory (`--all`, `--worktree`).**

```python
# .ufo/waves/round-7 -> r7real (a directory INSIDE the repo), holding w1-dispatch.json + w1/A.md
# plus a healthy .ufo/waves/round-9/w1-dispatch.json
run(check, d, ["--worktree", "--all"])               # rc 0, rounds=1  (round 7 never scanned)
run(check, d, ["--worktree", "--round", "7"])        # rc 2 SETUP_ERROR round 7: no <wave>-dispatch.json
```

C is pre-existing base behaviour and outside F1's wording; it is listed because it is the same
"enumerate only what the walker yields" root cause as A and B. A fix in `WorkTree.paths()` that also
handles `dirs` and a `GitTree` that also records `160000` would close all three.

## 7. Checklist answers the item asked for

| question | answer |
|---|---|
| fixed in BOTH modes where asked | F1 yes; F2 yes; F3 yes; F4 n/a (`--rev` cannot hold a FIFO) and yes in worktree; F5 yes in worktree, `--rev` unchanged at SR01 by design |
| fail-closed | F1 rc 2, F4 rc 2, F5 SR03 + rc 1; F2/F3 change no verdict direction |
| changes a round-91 frozen expectation | no — 59/59 expectations, 55/55 mutants, fresh 60/60, lane output byte-identical |
| still parseable by `c2-r91` `FIND` for plain names | yes — 133/133 lane lines + all 59 expectations; `P-07` asserts the exact plain line |
| wrong battery expectation | none found |
| F fixture the base already passes | none (base meets only the 8 P controls) |
| missing mode | none for the five defects as stated |

## 8. Residual risk / verification gaps

1. Directories, symlinks-to-directories and gitlinks at a dispatch path are silently skipped (§2, §3).
   Only the FIFO/device subset of F4 is covered, and the docstring claims more than the code does.
2. The battery cannot see the SR03-branch tokenisation (§1 F2): 28/28 met with that line deleted.
3. `always_refuse` meets all 8 rc-2 fixtures because F4's `contains` string is a substring of the F1
   message; the control leg is weaker than the summary suggests.
4. Worktree and rev still label the same outside-reaching report differently (SR03 vs SR01).
5. I did not exercise: a device file (needs root; untested), oversized dispatches (round-91 §3 P1 shows
   linear behaviour, unchanged), CRLF/unicode report paths (round-91 covered them; no candidate code
   path for report *content* changed).
6. The controls were rewritten mid-wave; everything above is pinned to the sha256 table in the header.

## 9. Installs / dead steps / scratch

* No installs; pacman untouched (read-only `pacman -Q*` not even needed).
* No dead steps. Two background jobs were started: the first C2 draft run was cancelled after the
  battery pin moved (it had been launched against `c923ac17…`); the second run against `73ae3bde…`
  produced the result in §5.
* Scratch `S=/fast/scratch/hyaku/mado-r92/R92MReviewC2` (probes, matrix harness, lane dumps) deleted on
  exit; only this report is kept.
