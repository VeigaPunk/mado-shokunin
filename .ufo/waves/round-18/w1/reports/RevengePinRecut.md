# RevengePinRecut — the exact `PIN_MADO` re-cut procedure (round 18)

Role: revenger (UFO-FSD). Item: derive the re-cut procedure from
`.ufo/waves/round-14/evidence/regression-recut.txt`, `historical-results.tsv`,
and the gate comments (`tools/mado-verify.sh` ~:1550-1650,
`mado_r7_target_build` ~:1723); return a step list GateRcFix can follow.
No lane gate was run by this item; every number below is a read-only
derivation or a `/tmp` probe on copied bytes. No tool was installed or
updated. Report path is this file only.

Axis read: correctness of the re-cut invariants (primary), cheapness of the
procedure (no redundant 80-second sweeps, no guessed pins), harm watch (the
gate stays the single verdict instrument; no substrate read, no lane git/jj
write).

---

## 0. Starting facts, observed (read-only)

| Fact | Value | How observed |
|---|---|---|
| lane HEAD / `refs/heads/master` | `d3a0000` (round-18 pre-registration) | `git rev-parse HEAD refs/heads/master` |
| last commit touching the gate | `32118fc` "round-14: output-colour boundaries and regular-source policy" | `git log -1 --format=%H refs/heads/master -- tools/mado-verify.sh` |
| committed gate bytes | `fba82a66…c207`, 3,711 L, 177,849 B | `git show d9a5a18:tools/mado-verify.sh \| sha256sum`, `wc -lc` |
| baseline gate at `d9a5a18` | identical to master (`fba82a66…`) | `git diff --stat d9a5a18 refs/heads/master -- tools/mado-verify.sh` → empty |
| **baseline derived target** | **`cd1d73d75fcc…b9f3f96`**, 2,403 L, 117,602 B | the exact three-`sed` excision below; equals the committed `PIN_MADO` |
| embedded spec | 2,127 B, `c7ee75b9…1dd8` = `SPEC_SHA` | heredoc re-extraction + `sha256sum` |
| marker families (committed bytes) | R7-SELFTEST 440–619 · R8-OMARCHY 622–801 · R8-BLOCK 1368–1531 and 1984–2506 · R7-REGRESSION 1543–1983 | `grep -n '^\s*# >>>\|^\s*# <<<'` |
| pin block (committed bytes) | `:1639` `PIN_MADO`, `:1640` `SPEC_SHA`, `:1641` `HARNESS_SHA_RECORDED`, `:1642` `TABLE_MADO` — all inside 1543–1983 | same |
| live tameshi harness | `0673d2e5…` (`HARNESS_SHA_RECORDED b56c6e57…` is provenance, not gated) | `sha256sum tameshi-shokunin/tools/mutate-and-run.sh` |
| tameshi's own mado leg | replays `tools/mado-verify.sh` @ `eead56b`, pin `d7edaab4…`, table 4/10, **from git objects** | `mutate-and-run.sh:557-568, 1205-1208` |

**In-flight observation (do not hardcode).** At `2026-10-20T15:44:51Z`,
GateRcFix's edit was already in the working tree: gate
`2bdf5e8a…3925`, 3,768 L, 181,780 B; derived target `20714096…2744`,
2,460 L, 121,533 B; `PIN_MADO` still `cd1d73d7…`. So `--regression` today
reads SETUP (correct: never stale-PASS), and the pin must move to whatever
bytes finally land. The procedure below binds the pin from the gate's own
printout, never from this paragraph.

What moves the pin: the excision deletes only the three marker pairs
`R7-REGRESSION`, `R7-SELFTEST`, `R8-BLOCK` (both occurrences). The
`R8-OMARCHY` pair is **not** excised (corroborated by
`corpus/knowledge/gate-standing-use.md` §5.6), so the rc-knob stub edit and
an OM scenario placed in that block both move the pin — and both are also
present in the derived target's own control suite, which is what makes the
green-after receipt meaningful.

---

## 1. What "PASS" means — three separate checks

1. **Recut sweep (the only substantive check).** `mutate-and-run.sh` over
   the derived target with the recorded 10-defect spec reproduces the table:
   control GREEN, 10/10 KILLED, 0 survived, 0 inconclusive, `MUTATE_RESTORE:
   OK`, target bytes unchanged, exit 0.
2. **Gate mode.** `bash tools/mado-verify.sh --regression` prints
   `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=<PIN>)`, exit 0,
   and zero `MADO_VERIFY:` tokens.
3. **Pin identity in the live suite.** `--selftest` passes
   `R10: derived target equals the recorded gate revision` and both `R11`
   spec assertions.

Why (1) cannot be replaced by (2): `PIN_MADO` is derived from the same file,
so setting it to the derived sha makes the *pin* check trivially true. The
recorded table and its committed sweep receipt are the whole evidentiary
content — the R17-V5 failure mode is exactly a tightening "demonstrated" in a
seat `/tmp` lab with no committed mutant receipt. A `/tmp`-only success here
does not discharge the item.

---

## 2. Step list (GateRcFix)

All commands run from `/home/vgpnk/Projects/shokunin/mado-shokunin`, scratch
only under `/tmp`, no lane git/jj write. Steps 1–4 are measurements; step 5
is the only gate edit after measurement; steps 6–7 prove and receipt.

### Step 1 — red-before, before the fix (own item; `evidence/gate-rc-redbefore.txt`)

Materialize the committed baseline and add **only** the new OM scenario +
stub knobs (no rc fix):

```
mkdir -p /tmp/mado-r18-redbefore
git show d9a5a18:tools/mado-verify.sh > /tmp/mado-r18-redbefore/target.mado-verify.sh
sha256sum /tmp/mado-r18-redbefore/target.mado-verify.sh   # expect fba82a66…
# add STUB_GIT_*_RC knobs + OM9/OM10 to that copy, then:
bash /tmp/mado-r18-redbefore/target.mado-verify.sh --selftest; echo "exit=$?"
```

Expected red (the defect): the failing-`show` case emits the row
`omarchy omarchy.skill.vs_head FAIL "MOVED: worktree … != HEAD blob e3b0c442… (local edit; …)"`
— i.e. the empty-input digest `e3b0c442…` compared as if it were the blob —
and the suite ends `MADO_SELFTEST: FAILED` with exit 2. Capture raw
stdout/stderr, exit, and the sha of the bytes used in the receipt header.
This is the **mutant receipt for the instrument tightening**; the same
scenario must pass on the fixed bytes (step 6).

### Step 2 — derive the new pin from the gate itself (authoritative)

```
bash tools/mado-verify.sh --regression
```

Exit 2 is expected and is not a failure. Read:

```
REGRESSION_TARGET: /tmp/mado-verify-regression.XXXXXX/target.mado-verify.sh sha256=<NEW_PIN> (recorded pin cd1d73d7…; match=no)
REGRESSION_RECUT: bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --target /tmp/mado-verify-regression.XXXXXX/target.mado-verify.sh --defects /tmp/mado-verify-regression.XXXXXX/mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir /tmp/mado-verify-regression.XXXXXX/recut --label mado-verify.sh
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
REGRESSION_WORKDIR: /tmp/mado-verify-regression.XXXXXX (kept)
```

`REGRESSION_SPEC: … sha256=c7ee75b97c… (recorded pin matches)` must appear
before the target line. Use the printed paths; `sed`-deriving the target by
hand is correct but the gate's own derivation is the one the pin will be
checked against.

### Step 3 — do not rewrite the spec

The spec in `$root/mado-verify.defects.spec` is written by
`mado_r7_spec_write` with `printf '%s'` (no trailing LF). Its sha must stay
`c7ee75b9…`; `SPEC_SHA` and the heredoc are unchanged by this round. Adding
a defect for OM9/OM10 is *not* part of the re-cut — the recorded case is the
round-7 case, and `TABLE_MADO` must keep exactly 10 ids.

### Step 4 — the measured recut sweep (80 s class)

Run the printed `REGRESSION_RECUT` command verbatim. The round-14 shape
(`.ufo/waves/round-14/evidence/regression-recut.txt`) used a named workdir:

```
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh \
  --target  /tmp/mado-verify-regression.XXXXXX/target.mado-verify.sh \
  --defects /tmp/mado-verify-regression.XXXXXX/mado-verify.defects.spec \
  --suite   'bash "$MUTANT" --selftest' \
  --workdir /tmp/mado-verify-regression.XXXXXX/historical \
  --label   mado-r18-historical
```

Save the complete stdout+stderr and exit into
`.ufo/waves/round-18/evidence/regression-recut.txt` with the receipt header
(§6), and copy `<workdir>/results.tsv` to
`.ufo/waves/round-18/evidence/historical-results.tsv`.

Required output (bind; never predict): `MUTATE_SPEC: … defects=10`;
`CONTROL: GREEN (exit=0 duration-ms=N pristine-sha256=<NEW_PIN>)` with
`  | MADO_SELFTEST: N/N assertions passed` — bind N from output, but the
observed in-flight OM9/OM10 block adds exactly 17 `st_*` calls (0 removed:
`git diff -- … | grep -E '^\+.*st_[a-z_]+ ' | wc -l` → 17), so the expected
control is **284/284** (baseline 267 + 17) if those bytes land unchanged.
Also required: ten `DEFECT <ID>: KILLED` lines and no `SURVIVED`/
`INCONCLUSIVE`; `MUTATE_RESTORE: OK (target-sha256
before=<NEW_PIN> after=<NEW_PIN> …)`; `MUTATE: DONE (… defects=10 killed=10
survived=0 inconclusive=0 kill-rate=100%)`; exit 0.

### Step 5 — the only gate edit after measurement

Inside the `MADO-R7-REGRESSION` block only (currently 1591–2031; the pin
constants are 1687–1690):

- `PIN_MADO='<NEW_PIN>'` — from step 2/4, nothing else.
- `TABLE_MADO` — **unchanged** when the measured table is the recorded one.
  If any row differs (e.g. `SURVIVED`), that is a finding: fix the edit, do
  not bless the table.
- `SPEC_SHA` and `HARNESS_SHA_RECORDED` unchanged (harness sha is provenance,
  not gated).
- Append a `Re-cut record — round 18 / M18` comment after the round-14
  record: date, before → after pin, measured table, harness sha, evidence
  paths, and the in-flight/landed commit note.
- Touch nothing else: no cosmetic edits (`VERSION_STR`, base help are
  load-bearing, standing-use §5.7), no marker text inside added comments, no
  further edits to retained blocks. Any post-measurement edit invalidates the
  pin.
- After the edit, re-derive with the three-`sed` excision and assert the sha
  is still `<NEW_PIN>` (the pin line is excised, so this is a cheap
  self-consistency check):

```
sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
    -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
    -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
    tools/mado-verify.sh >/tmp/check/target.sh && sha256sum /tmp/check/target.sh
```

### Step 6 — prove the mode end to end

```
bash tools/mado-verify.sh --regression --keep; echo "exit=$?"
```

Expected exit 0 and exactly these anchors:

```
REGRESSION_TARGET: … sha256=<NEW_PIN> (recorded pin <NEW_PIN>; match=yes)
REGRESSION_BAND: all recorded kills required (recorded 10/10 KILLED; flips=0; inconclusive=0; control GREEN; MUTATE_RESTORE OK; target sha unchanged) — plan §(a) killed-delta<=1 tolerance not applied
REGRESSION_SWEEP mado-verify-hardened: MUTATE: DONE (target=mado-verify-hardened defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0
REGRESSION_CASE mado-verify-hardened: PASS (recorded table reproduced: killed=10/10 flips=0 inconclusive=0 control=green restore=ok)
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=<NEW_PIN>)
```

`REGRESSION_CLEANUP: removed=<n> kept-fixture dir(s) …` is informational.
Assert `grep -c 'MADO_VERIFY:'` on this output is 0. Save the whole
transcript (with command/date/exit header) as
`.ufo/waves/round-18/evidence/gate-pin-recut.txt`, and copy the kept
`case/sweep/results.tsv` beside it as `gate-pin-recut-results.tsv`.

Then the live suite:

```
bash tools/mado-verify.sh --selftest; echo "exit=$?"
```

Expected exit 0 and `MADO_SELFTEST: 389/389 assertions passed` if the
observed OM9/OM10 block lands unchanged (372 + 17; take the actual count from
output and re-derive if the scenario grew or shrank),
and the lines `R10: derived target equals the recorded gate revision`,
`R11: the embedded spec is byte-identical to the recorded case`,
`R11: the embedded spec carries the ten recorded defects`. Save as
`evidence/gate-selftest.txt` with a header naming the measured gate sha and
the commit (see §6). Optional harm watch: `--no-live` still
29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE, exit 0.

### Step 7 — landedness (L1, after the commit)

Seats cannot write git; L1 commits the gate. Then append to the receipts:

- `measured_commit: <commit>` where
  `git show <commit>:tools/mado-verify.sh | sha256sum` equals the receipt's
  `gate_sha256` (this is the exact relation the round-14 erratum says was
  missing: "input_binding: provisional worktree snapshot", no
  `measured_commit`).
- Re-run `bash tools/mado-verify.sh --regression` at that commit and record
  `verified_commit` + the `MADO_REGRESSION: PASS` line in
  `evidence/gate-pin-recut.txt`. Because the receipt was taken from the
  final bytes, this must reproduce `<NEW_PIN>` with `match=yes`.

Normal commits do not disturb tameshi's `bash-mado-verify` leg (it reads
`eead56b` from git objects); history rewriting would.

---

## 3. Expected-line catalogue (exact formats)

Harness lines (from `tameshi-shokunin/tools/mutate-and-run.sh:481-526`):

| Line | Round-14 observed | Moves this round |
|---|---|---|
| `MUTATE_TOOL: <path> sha256=<hex>` | `… sha256=75ed934d…` | yes (live harness `0673d2e5…`) |
| `MUTATE_DATE: <UTC>` | `2026-10-20T05:58:44Z` | yes |
| `MUTATE_TARGET: <path> sha256=<hex> bytes=<n>` | `… sha256=cd1d73d7… bytes=117602` | **yes — new pin + bytes** |
| `MUTATE_SPEC: <path> defects=10` | `… defects=10` | no |
| `CONTROL: GREEN (exit=0 duration-ms=<n> pristine-sha256=<pin>)` | `… 7632 … cd1d73d7…` | sha moves; N/N moves |
| `  | MADO_SELFTEST: <N>/<N> assertions passed` | `267/267` | yes (`+OM9/OM10`) |
| `DEFECT <ID>: KILLED (exit=<rc> duration-ms=<n>) <desc>` | D1–D9 + R1, exits 2,2,2,2,1,2,2,2,2,2 | no (`exit=1` for D5 only) |
| `MUTATE_RESTORE: OK (target-sha256 before=<pin> after=<pin> pristine-sha256=<pin>)` | all three `cd1d73d7…` | sha moves |
| `MUTATE_EVIDENCE: <workdir>` | `/tmp/mado-r14-recut-0blumi29/historical` | yes |
| `MUTATE: DONE (target=<label> defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)` | label `mado-r14-historical` | label/round only |

Gate-mode lines (`run_regression`, `regression_case`):

| Line | Meaning |
|---|---|
| `REGRESSION_TOOL: … sha256=<gate>` | the live gate file's own sha |
| `REGRESSION_HARNESS: … sha256=<live> (recorded revision b56c6e57… — provenance, not gated)` | provenance only |
| `REGRESSION_SPEC: … sha256=c7ee75b9… (recorded pin matches)` | spec must match |
| `REGRESSION_TARGET: … match=no\|yes` | pre-update / post-update |
| `REGRESSION_RECUT: bash … --workdir <root>/recut --label mado-verify.sh` | the command to run |
| `REGRESSION_BAND: …` | states the zero-tolerance band |
| `REGRESSION_SWEEP`, `REGRESSION_TABLE`, `REGRESSION_CASE` | measured results |
| `MADO_REGRESSION: SETUP\|FAIL\|PASS` | only terminal token; never mixes with `MADO_VERIFY:` |

`SETUP` = "cannot verify" (pin mismatch, missing harness/spec). `FAIL` =
"the table did not reproduce". Do not report SETUP as a gate failure, and do
not report PASS unless step 6's three checks hold.

---

## 4. Failure map (symptom → cause → action)

| Symptom | Cause | Action |
|---|---|---|
| `MADO_REGRESSION: SETUP (target pin mismatch …)` after the pin update | pin line edited outside the excised block, or the file moved after measurement | re-derive; edit only `PIN_MADO` inside 1591–2031; re-measure if bytes moved |
| `MADO_REGRESSION: SETUP (embedded spec sha256 … != recorded …)` | spec re-typed / trailing LF added / heredoc edited | use the gate's writer; restore `SPEC_SHA` bytes |
| harness `MUTATE: SETUP (spec/preparation failed for N defect(s))` | an `@old` no longer occurs exactly once (the edit touched a pinned line or duplicated a pattern) | read the failing id in the log; restore uniqueness; the recorded spec must not be edited |
| `CONTROL: RED` + `MUTATE: SETUP (control run … is red)` | the derived target's selftest fails: new scenario depends on excised material, or a stub default changed | keep `STUB_GIT_*_RC` default 0 and the scenario self-contained; OM1–OM8 must stay green |
| `DEFECT <id>: SURVIVED` | the edit removed the behavior a clause notices (D2's UNKNOWN guard, D5's `return 2`, D9's byte comparison …) | fix the edit; never update `TABLE_MADO` to a survivor |
| `MADO_REGRESSION: FAIL (out of band: flips=… )` | measured table ≠ recorded table | read `REGRESSION_DEFECT` lines; this is a finding, not a pin move |
| `MUTATE_RESTORE: DRIFT` | the target was edited during the sweep (concurrent writer) | stop; re-measure on frozen bytes |
| `MADO_REGRESSION: SETUP (mutation harness not found)` | fleet path / `MADO_VERIFY_HARNESS` | set the env var or run from the lane root |
| `MADO_VERIFY:` token inside `--regression` output | mode contamination | investigate; the mode's contract forbids it |

---

## 5. Traps specific to this fix (measured)

1. **`${PIPESTATUS[0]}` after `blob=$(pipeline)` is always 0 here.** The gate
   runs `set -u` only (no `pipefail`), and a command substitution's pipeline
   status collapses to the assignment's single status (last stage). Measured:
   `x=$(false|true); echo $? ${PIPESTATUS[*]}` → `0 0`. A "PIPESTATUS fix" on
   that line would silently never fire. The working form is
   `blob=$(set -o pipefail; tmo git … | sha256sum | cut …); grc=$?` (pipefail
   *inside* the substitution) or a temp file; the in-flight edit uses the
   former and was verified to yield `grc=128` for a failing producer.
2. **A variable round-trip is byte-lossy.** `v=$(git show …);
   printf '%s\n' "$v" | sha256sum` hashes one trailing newline regardless of
   the blob's real ending; measured mismatch for both no-newline and
   two-newline fixtures. Hashing the raw stream (as the pipefail form does)
   keeps the comparison exact.
3. **The empty-input digest is a value, not an error.** A failed `git show`
   yields `e3b0c442…`, which is non-empty, so the old `-z "$blob"` guard
   could never fire. Test the producer rc first; keep the `-z` arm as the
   defensive second branch.
4. **Placement.** OM9/OM10 in the `R8-OMARCHY` block is correct: that block
   is retained in the derived target, so the scenario runs in the sweep's
   control. Putting it only in the excised `R7-SELFTEST` block would move the
   pin (the `:3406` fix already does) while leaving the scenario out of the
   control.
5. **The pin lives inside the excised block.** Editing `PIN_MADO` must not
   change the derived sha; verify with step 5's re-derivation. Never add a
   new pin/table constant outside the block.
6. **Marker text is load-bearing.** Do not write `# >>> MADO-R8-BLOCK >>>`
   (or any marker spelling) in new comments/heredocs; the excisor's sed
   ranges would delete more than intended.
7. **Do not touch `SPEC_SHA`, the spec heredoc, `TABLE_MADO` (when the table
   reproduces), `HARNESS_SHA_RECORDED`, `VERSION_STR`, or the base help.**
   The first three are the recorded case; the rest are provenance/cosmetics
   that move the pin for no gain.
8. **Order.** Measure after the last edit. The gate's own `--regression`
   removes the scratch root on PASS; `--keep` is required for the receipt.

---

## 6. Receipt shape (closes R17-V1 and R17-V5)

`evidence/regression-recut.txt` — header, then the verbatim sweep:

```
command: <the printed REGRESSION_RECUT line, actual paths>
cwd: /home/vgpnk/Projects/shokunin/mado-shokunin
input_binding: working tree (gate edited; commit pending)
gate_sha256: <sha256sum tools/mado-verify.sh at measurement>
gate_bytes: <wc -c>
baseline_commit: d9a5a18 (gate bytes fba82a66…)
spec_sha256: c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8
derived_target_sha256: <NEW_PIN>
harness: /home/…/tameshi-shokunin/tools/mutate-and-run.sh sha256=<live>
date: <UTC ISO-8601 Z>
stdout:
<verbatim, including MUTATE_TARGET/CONTROL/DEFECT/…/MUTATE: DONE>
stderr:
<verbatim>
exit=0
measured_commit: <filled by L1 after the commit>
committed_gate_sha256: <git show <commit>:tools/mado-verify.sh | sha256sum>  # must equal gate_sha256
```

Commit set under `.ufo/waves/round-18/evidence/`:
`regression-recut.txt`, `historical-results.tsv` (columns
`id verdict exit duration-ms mutant-sha256 desc`, ten rows),
`gate-pin-recut.txt` + `gate-pin-recut-results.tsv`, `gate-selftest.txt`,
and GateRcFix's own `gate-rc-redbefore.txt` (the tightening's red receipt).

The per-defect mutant shas in `historical-results.tsv` are what make this a
mutant receipt rather than a claim; the red-before transcript is the same
proof for the rc tightening. Both are required, and both must be committed
to count (R17-V5).

---

## 7. What the re-cut does not prove

- It does not re-open the recorded case's coverage: the ten defects are
  round-7's, and OM9/OM10 are fixture scenarios, not new table entries. The
  instrument tightening's bite is the red-before/green-after pair, not the
  table.
- It does not prove live-plane health (no live run is claimed here), and it
  does not read substrate: the sweep's suite is the derived target's
  hermetic `--selftest`.
- `PIN_MADO` is a byte-identity commitment to the excised executable, not to
  the design; it can only detect "the gate moved outside the marker pairs",
  and only when the sweep then reproduces the table.
- The theme-clause covering mutant and the other standing residuals
  (`corpus/knowledge/gate-standing-use.md` §6) remain open; this procedure
  neither closes nor widens them.

---

## 8. Evidence chain (commands run by this item)

- `sed` excision of the three marker pairs on committed and in-flight bytes →
  `cd1d73d7…` / `20714096…`; `bash -n` OK on both.
- Embedded spec extraction: 2,127 B, `c7ee75b9…` = `SPEC_SHA`.
- `git show d9a5a18:tools/mado-verify.sh | sha256sum` → `fba82a66…`;
  `git diff d9a5a18 master -- tools/mado-verify.sh` empty.
- PIPESTATUS probe under `set -u`: `0 0` (naive form dead).
- Newline round-trip probe: no-newline and two-newline files both mismatch
  the raw digest.
- In-flight rc-capture construct probe: failing producer → `grc=128`,
  `blob=e3b0c442…`; success → exact raw digest.
- Round-14 receipt + TSV read verbatim; harness contract read at
  `mutate-and-run.sh:225-330, 390-530, 1060-1145`; gate re-cut block read at
  `tools/mado-verify.sh:1543-1983, 552-613`.
