# C2 row re-run — SCORECARD.md:311 `mutation regression with re-cut`

Wave a3w1 (attempt 3), base `41cc04c8d593837a0d5078bffaacdaa163d12897`. Read-only C2 executor seat; no lane
writes except this report. No package operations, no installs, no git writes in the lane or fleet.

## 1. The row and its section at 41cc04c8

Row `SCORECARD.md:311`, under `### Capabilities (round 12)` (`SCORECARD.md:304`; table header `:306`, row `:311`,
section note `:313`). Verbatim row:

> `| mutation regression with re-cut | Replays the 10-defect kill table against the gate's derived target; SETUP on a moved gate, re-cut via the printed command | `gate-regression-setup-3.txt`, `gate-recut-3.txt`, `gate-regression-after.txt` | 7 (re-demonstrated 12) |`

The same command also appears as the round-12 comparison row `SCORECARD.md:291`
(`bash tools/mado-verify.sh --selftest`; `--regression` with
`MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` → `PASS @ 538d178b…`).

## 2. Demonstration command (frozen form)

The capability row has no single literal command; the frozen re-demonstration for it is the round-24 C2 manifest
entry `mutation regression with re-cut` (`.ufo/waves/round-24/c2/manifest.json` at `41cc04c8`, manifest
sha256 `e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`):

- argv `["bash", "{TREE}/tools/mado-verify.sh", "--regression"]`, cwd `{TREE}`, timeout 600 s
- env `MADO_VERIFY_HARNESS={FLEET}/tameshi-shokunin/tools/mutate-and-run.sh`
- exit_ok `[0]`, regex `(?m)^MADO_REGRESSION: PASS \(case=mado-verify-hardened; `, min_matches 1
- requires `tools/mado-verify.sh`

The row's three evidence files exist at `41cc04c8` under `.ufo/evidence/round-12/` and record the round-12 third
re-cut (`REGRESSION_TARGET … 538d178b… match=yes`; `MUTATE: DONE … killed=10 … kill-rate=100%`;
`MADO_REGRESSION: PASS (case=mado-verify-hardened; target=538d178bf03a5320…)`, exit 0).

## 3. What I ran

```
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapMutationRegressionWithRe311
git -C /fast/scratch/hyaku/mado-r25a3/c2/CapMutationRegressionWithRe311 checkout -q --detach 41cc04c8
# GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE unset
cd /fast/scratch/hyaku/mado-r25a3/c2/CapMutationRegressionWithRe311
MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh \
  timeout 600 prlimit --as=4000000000 -- bash tools/mado-verify.sh --regression
echo "exit=$?"
```

Clone HEAD: `41cc04c8d593837a0d5078bffaacdaa163d12897`. Gate in the clone: `tools/mado-verify.sh`, sha256
`050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1`, 4,194 lines / 208,124 B — the same
`050efc72…` / 4,194 L gate named at `SCORECARD.md:1221`. Pin in that gate: `PIN_MADO='367ff5ec…4f9e'`
(`tools/mado-verify.sh:2030`), `TABLE_MADO` = `D1..D9:KILLED,R1:KILLED` (`:2033`). Wall time 268.68 s.

## 4. Observed at 41cc04c8 — works

Exit `0`. Key output: `REGRESSION_TARGET … target=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e
(recorded pin … match=yes)`; `REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10
measured-killed=10 survived=0 inconclusive=0 flips=0`; `REGRESSION_CASE …: PASS (recorded table reproduced:
killed=10/10 flips=0 inconclusive=0 control=green restore=ok)`; `MADO_REGRESSION: PASS (case=mado-verify-hardened;
target=367ff5ec…)`; `REGRESSION_WORKDIR: /tmp/mado-verify-regression.IhWrko (removed on PASS; --keep retains)`.
The frozen rule scored: exit 0 ∈ exit_ok; the manifest regex matched once (checked with `re` over the receipt).

The PASS therefore reproduces the 10-defect kill table against the gate's own derived target, and the derived
target equals the recorded pin at `41cc04c8`.

## 5. Second clause — SETUP on a moved gate, re-cut via the printed command (exercised)

The PASS run does not exercise the row's SETUP/re-cut half, so I exercised it on a scratch copy of the gate under
`/fast/scratch/hyaku/mado-r25a3/c2/moved-gate/moved.sh` (sha256 `3b532c53…0016`) with one hex digit of
`PIN_MADO` flipped (`…84f9e` → `…84f9d`). Single-line change; the pin block is excised from target derivation, so the
derived target stayed `367ff5ec…` and the run refused:

```
exit=2
REGRESSION_TARGET: /tmp/mado-verify-regression.aLu60n/target.mado-verify.sh sha256=367ff5ec… (recorded pin 367ff5ec…84f9d; match=no)
REGRESSION_RECUT: bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --target /tmp/mado-verify-regression.aLu60n/target.mado-verify.sh --defects /tmp/mado-verify-regression.aLu60n/mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir /tmp/mado-verify-regression.aLu60n/recut --label mado-verify.sh
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
REGRESSION_WORKDIR: /tmp/mado-verify-regression.aLu60n (kept)
```

Running that printed command verbatim returned exit `0`: `CONTROL: GREEN (… MADO_SELFTEST: 355/355 assertions passed)`,
ten `DEFECT D1..D9/R1: KILLED`, `MUTATE_RESTORE: OK (before==after==pristine 367ff5ec…)`,
`MUTATE: DONE (target=mado-verify.sh defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)`. So the
printed re-cut is a runnable command and prints the measured 10/10 table; the gate's header rule it implements
(“the mode reads SETUP with the printed REGRESSION_RECUT command — never a stale PASS”, `tools/mado-verify.sh:1954-1955`)
holds at `41cc04c8`.

Limit of this exercise (stated, not hidden): the copy's substantive bytes were the pristine gate; only the pin
diverged. The demonstration proves the refusal and the printed-command mechanics and the 10/10 table, not what a
future re-cut would measure after a substantive gate edit.

## 6. Ledger line

| SCORECARD.md:311 | mutation regression with re-cut | Replays the 10-defect kill table against the gate's derived target; SETUP on a moved gate, re-cut via the printed command | observed at 41cc04c8: works — exit 0, `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=367ff5ec…4f9e)`, 10/10 KILLED, control GREEN, MUTATE_RESTORE OK; SETUP half exercised on a pin-flipped copy: SETUP exit 2 with printed `REGRESSION_RECUT`, that command re-run gives 10/10 KILLED exit 0 | `cd <clone>; MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh timeout 600 prlimit --as=4000000000 -- bash tools/mado-verify.sh --regression` | SCORECARD.md:1578 (round-24 status table: works @ `8e5d9369`); scope note :1588-1596; current pin :1222 |

## 7. Supersession / contradiction grep over the whole SCORECARD.md at 41cc04c8 (1,618 lines)

| Line(s) | What it says | Relation to row 311 |
|---|---|---|
| 1578 | round-24 capability status table: `mutation regression with re-cut \| works \| MADO_REGRESSION: PASS, exit 0 at 8e5d9369` | later re-demonstration; agrees (my base 41cc04c8 is a descendant of 8e5d9369 and reproduces PASS) |
| 1588-1596 | scope correction: the frozen C2 population is the 12 rows under `Capabilities` headings | places row 311 inside the counted population; no contradiction |
| 1606 | round-24 C2 result: 1/12 mismatches → 0/12; three out-of-population rows are the stale ones | this row is not among the stale; agrees |
| 1222 | `regression PASS, PIN_MADO 367ff5ec…` (round-21 final-state correction, gate `050efc72…`, 4,194 L) | names the pin my run measured; row-311's evidence files name the older pin `538d178b…` |
| 1002 / 1016-1052 | PIN_MADO history (`cd1d73d7… → 20714096…`) and round-18/19 re-cut receipts | provenance of the pin movement, no contradiction |
| 291 | round-12 comparison row with the same `--regression` + harness command (`PASS @ 538d178b…`) | same capability, older measurement |
| 265-266, 346, 351 | harm-watch statements “`--regression` ends `MADO_REGRESSION: PASS` (re-cut if the gate moves)” | restates the rule rather than superseding the row |
| 798 | a round's scope line: “No legacy live or no-live host run, regression or sibling gate executed” | scope statement about that round, not a claim about this capability |

No later text contradicts row 311. Untested here: whether a row-311 PASS at base `41cc04c8` transfers to the later
`8e5d9369` base (its own round-24 status row says it does).

## 8. Verbatim command output

Primary (frozen command, clone at 41cc04c8), exit `0`, file `/fast/scratch/hyaku/mado-r25a3/c2/cap311-regression.txt`
sha256 `cc89c2d9713c4c3e0ff67ffbc303ed96730dea5c2ef6cf61771ceec4178e793d`:

```
REGRESSION_TOOL: /fast/scratch/hyaku/mado-r25a3/c2/CapMutationRegressionWithRe311/tools/mado-verify.sh sha256=050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1
REGRESSION_DATE: 2026-10-23T07:22:51Z
REGRESSION_HARNESS: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 (recorded revision b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb — provenance, not gated)
REGRESSION_SPEC: /tmp/mado-verify-regression.IhWrko/mado-verify.defects.spec sha256=c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8 (recorded pin matches)
REGRESSION_TARGET: /tmp/mado-verify-regression.IhWrko/target.mado-verify.sh sha256=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e (recorded pin 367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e; match=yes)
REGRESSION_BAND: all recorded kills required (recorded 10/10 KILLED; flips=0; inconclusive=0; control GREEN; MUTATE_RESTORE OK; target sha unchanged) — plan §(a) killed-delta<=1 tolerance not applied
REGRESSION_SWEEP mado-verify-hardened: MUTATE: DONE (target=mado-verify-hardened defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0
REGRESSION_WORKDIR mado-verify-hardened: /tmp/mado-verify-regression.IhWrko/case
REGRESSION_CASE mado-verify-hardened: PASS (recorded table reproduced: killed=10/10 flips=0 inconclusive=0 control=green restore=ok)
REGRESSION_CLEANUP: removed=10 kept-fixture dir(s) named by this run (paths read from this run; /tmp/w5-mado-m52-selftest.* prefix-guarded)
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e)
REGRESSION_WORKDIR: /tmp/mado-verify-regression.IhWrko (removed on PASS; --keep retains)
```

SETUP half (pin-flipped copy), exit `2`, file `/fast/scratch/hyaku/mado-r25a3/c2/cap311-moved-setup.txt`
sha256 `1024b3892835db08c24360e83ae9c84d32c3fd2bd72210394e130aae266ee2ee`:

```
REGRESSION_TOOL: /fast/scratch/hyaku/mado-r25a3/c2/moved-gate/moved.sh sha256=3b532c53d739212a5bab305bfd948a6f367bd9c8204e0db7994e0fee7c980016
REGRESSION_DATE: 2026-10-23T07:29:20Z
REGRESSION_HARNESS: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 (recorded revision b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb — provenance, not gated)
REGRESSION_SPEC: /tmp/mado-verify-regression.aLu60n/mado-verify.defects.spec sha256=c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8 (recorded pin matches)
REGRESSION_TARGET: /tmp/mado-verify-regression.aLu60n/target.mado-verify.sh sha256=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e (recorded pin 367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9d; match=no)
REGRESSION_RECUT: bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --target /tmp/mado-verify-regression.aLu60n/target.mado-verify.sh --defects /tmp/mado-verify-regression.aLu60n/mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir /tmp/mado-verify-regression.aLu60n/recut --label mado-verify.sh
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
REGRESSION_WORKDIR: /tmp/mado-verify-regression.aLu60n (kept)
```

Printed re-cut command run verbatim, exit `0`, file
`/fast/scratch/hyaku/mado-r25a3/c2/cap311-moved-recut.txt` sha256
`c6858c2c35c1114668008373eae54ba0db492abad8f8af167e7d23d7115a886b` (trimmed to summary lines; per-defect
assertion detail omitted):

```
MUTATE_TARGET: /tmp/mado-verify-regression.aLu60n/target.mado-verify.sh sha256=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e bytes=144260
MUTATE_SPEC: /tmp/mado-verify-regression.aLu60n/mado-verify.defects.spec defects=10
CONTROL: GREEN (exit=0 duration-ms=26625 pristine-sha256=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e)
  | MADO_SELFTEST: 355/355 assertions passed
DEFECT D1: KILLED (exit=2 duration-ms=22108) clause A: file-plane CLEAN verdict token renamed (CLEAN -> OK)
DEFECT D2: KILLED (exit=2 duration-ms=21258) clause B: UNKNOWN guard dropped from the CLEAN test
DEFECT D3: KILLED (exit=2 duration-ms=19389) clause B: skipped live layer row reports PASS instead of SKIP
DEFECT D4: KILLED (exit=2 duration-ms=56211) clause C: DIVERGED path exits 0
DEFECT D5: KILLED (exit=1 duration-ms=61270) clause C: failing --selftest returns 1 not 2
DEFECT D6: KILLED (exit=2 duration-ms=45463) clause D: xdph dropped from the 12-conf local inventory
DEFECT D7: KILLED (exit=2 duration-ms=50336) clause D: include-graph count test -ne -> -lt (extra source lines tolerated)
DEFECT D8: KILLED (exit=2 duration-ms=35179) clause E: hyprland.conf sha pin comparison always "matches"
DEFECT D9: KILLED (exit=2 duration-ms=51000) clause E: read-only boundary comparison always reads byte-identical
DEFECT R1: KILLED (exit=2 duration-ms=28800) clause F: tomllib-unavailable arm reads PASS not UNKNOWN
MUTATE_RESTORE: OK (target-sha256 before=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e after=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e pristine-sha256=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e)
MUTATE: DONE (target=mado-verify.sh defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
```

## 9. Deviations, risks, cleanup

- **Harness bytes.** The consumed harness is sha256 `a7d3f2dd…2eb9`; the round-12 receipts recorded
  `75ed934d…adc5`. The gate itself labels the harness revision line “provenance, not gated”
  (`tools/mado-verify.sh`, `REGRESSION_HARNESS` print); its gated inputs are the embedded spec
  (`SPEC_SHA c7ee75b9…`, matched) and the derived target (`367ff5ec…`, matched `PIN_MADO`). So the 10/10 table is a
  statement about the gate bytes, not about the harness's current mutation logic.
- **Historical pointer.** Row 311's three evidence files are round-12 receipts naming target `538d178b…`; the pin has
  since moved (`cd1d73d7…` → `20714096…` → `367ff5ec…` per `SCORECARD.md:1002`, `:1222` and the gate's re-cut
  records). The row's statement stays true, but the pointer alone cannot verify the current pin; the re-run is what
  verifies it.
- **Not hermetic.** `--regression` resolves the harness at an absolute path under the fleet repo and writes scratch
  under `/tmp`; a missing harness is a self-declared `SETUP` exit 2 (selftest assertion “R13”, gate lines 639-640).
- **Host sharing.** The host was shared with other lanes (concurrent tameshi round-30 seats running `mutate-and-run.sh`
  against their own trees); wall times were inflated (PASS run 268.68 s; re-cut 418 s) but the tables reproduced.
- **Auxiliary experiment scope.** The SETUP/re-cut demonstration used a pin-only divergence on a scratch copy; the
  substantive gate bytes swept were the pristine target. It proves the refusal and printed-command path, not a
  post-edit re-cut measurement.
- **Cleanup.** Sandbox clone `/fast/scratch/hyaku/mado-r25a3/c2/CapMutationRegressionWithRe311` deleted; moved-gate
  copy and `moved.sh` deleted; my workdir `/tmp/mado-verify-regression.aLu60n` (kept by SETUP design) deleted; the ten
  `/tmp/w5-mado-m52-selftest.*` fixture dirs my re-cut run named (`IV8dSP m2ncex AmVwpd SRc45B PuUudO IjC8IM pIdDDk
  0Ve8QB zWU5TT 5NEmm7`) deleted. The PASS run's own workdir and 10 fixtures were removed by `REGRESSION_CLEANUP`.
  Only the three receipts `cap311-regression.txt`, `cap311-moved-setup.txt`, `cap311-moved-recut.txt` remain under
  `/fast/scratch/hyaku/mado-r25a3/c2/`; no process from this seat is left running.
- **Tool changes.** None (no installs or upgrades; pacman transactions host-wide remain paused and were not used).

## 10. Blockers

None.
