# MutFrozenRepin — partial

## Attack and axes

Axes: source-finding retention; refusal of previously unknown finding lines; pinned-byte integrity before publication; verbatim carry of still-missed incident notes; host/source isolation.

Attacked four one-line behavior points in independent scratch copies of `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen-repin.py`. **Full detector: three killed, one survived; no inconclusive baseline.** No unmodified-script contract failure was found in these probes. The surviving source-digest-guard deletion was caught later by the unchanged staged-copy digest guard, so the survivor does **not** demonstrate publication of corrupt bytes.

The untouched round-18 baseline with only the committed current tripwire is insufficient: **all four mutants survive that one positive-control case**. It produces 11 findings and zero remaining known misses. Added targeted negative controls are what kill the three non-redundant mutants below. The script's own `frozen_match` replay alone accepted the three defective publications.

## Committed bytes and isolated fixtures

Scratch: `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr`. Both scripts were obtained using these read-only commands, capturing stdout into the named scratch snapshots:

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 01b80946d92b26370d3012a7da655d00dd135154:.ufo/waves/round-19/frozen-repin.py
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 01b80946d92b26370d3012a7da655d00dd135154:tools/mado-tripwire.py
```

- Committed re-pinner, `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/frozen-repin.py`: SHA-256 `7cc8b2cdd7a74c9a2b3131c07b6b4e921d32147fedc58c86afb0027c5688517c`; 30,037 bytes.
- Committed classifier, `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/mado-tripwire.py`: SHA-256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`; 90,536 bytes.
- Actual original source: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen`; `expected.json` SHA-256 `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`.
- `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/toy-drop-source.py`: wraps the committed classifier and suppresses exactly `(r13-global-capture.jsonl, 1, live_probe, wayland-info)` in **both** scan and frozen replay. SHA-256 `adf988066f551a7dbfcdd742044389e05d698906c9d6a582765fb5c284bc1c8f`.
- `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/toy-drop-known.py`: suppresses exactly `(r13-root.jsonl, 4, package_query, pacman:-Q)` in both modes. SHA-256 `22ca3501e8a9e378272b8940b5700cf66df28cdc0ecdc337895cab787006cc4b`. This second toy is necessary because dropping an original expected finding exercises refusal, not carry of a still-missed known line. Both toys retain real committed pin/reachability/replay validation; neither fakes a `frozen_match` verdict.
- New-line stimulus: `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/source-newline` is a scratch copy of the original frozen source with one synthetic assistant bash-toolCall record appended to `inputs/r15-libinput-events.jsonl`, at line 6. Its literal `wayland-info` is **data only**, scanned statically, never executed. The corresponding input pin is updated; original expected findings and known-miss notes are unchanged. Input SHA-256 `9199976179e9a275f5796cef63005206bbbcdbc642dbbed3574af283592ff7e4`; expected SHA-256 `e4ff055904638e580aec40110c404ed029e75203fcf30187712d88c920d186d1`.
- Digest stimulus: `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/source-tampered` copies the original frozen source, then appends one newline byte to that same input **without** updating its pin. Actual input SHA-256 `314a4769c1cc82fd25f74613f099d7ae2d8cd738b452b6b0116bbf6062c1b9c5` versus pinned `7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90`.

## Same bounded detector, all three phases

Detector: `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py`, SHA-256 `3dbc3385f9e704020486fa6cfc7714ecc1485bbf7888d27f1d6c5804fda65734`. Each invocation runs the identical ten cases with a 30-second per-case timeout. Cases use the original round-18 source unless explicitly identified as a scratch input variant:

1. Committed classifier, original source: written, 11 findings, zero remaining known misses.
2. Drop-source toy: refuse the missing original finding, no target.
3. Same drop-source toy with `--allow-new-findings`: still refuse the missing original finding.
4. Drop-known toy: written, ten findings, exactly the original `r13-root:4` known-miss row/note retained verbatim.
5. Committed classifier, new-line stimulus: refuse the new `r15-libinput-events:6` finding.
6. Same with `--allow-new-findings`: written, 12 findings.
7. Drop-known toy, new-line stimulus: refuse the new line.
8. Same with `--allow-new-findings`: written, 11 findings, original `r13-root:4` miss retained verbatim.
9. Committed classifier, corrupt-pin stimulus: exit 2, pin-mismatch error, no target.
10. Drop-source toy, corrupt-pin stimulus: same integrity rejection, before tool behavior matters.

The detector checks exact refusal rows, finding rows/order, known-miss row/note preservation, source-to-output input byte identity, target presence/absence, successful internal frozen replay, and no surviving private staging directory. Its corruption oracle requires a pin-mismatch error and no published target, **not the exact source-versus-staging diagnostic or pre-copy timing**.

Actual commands executed, dispatched concurrently across the four isolated candidates within each phase (phase directories retain the outputs, so these same paths are not empty for an immediate rerun):

```text
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/missing/frozen-repin.py --phase pristine
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/newline/frozen-repin.py --phase pristine
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/digest/frozen-repin.py --phase pristine
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/known/frozen-repin.py --phase pristine
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/missing/frozen-repin.py --phase mutated
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/newline/frozen-repin.py --phase mutated
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/digest/frozen-repin.py --phase mutated
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/known/frozen-repin.py --phase mutated
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/missing/frozen-repin.py --phase restored
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/newline/frozen-repin.py --phase restored
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/digest/frozen-repin.py --phase restored
/usr/bin/python3 -I /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/detector.py --candidate /tmp/mado-r19-MutFrozenRepin-s_6jn1hr/known/frozen-repin.py --phase restored
```

| Mutant | Pristine | Mutated | Restored | Verdict |
|---|---:|---:|---:|---|
| missing | 10/10 | 8/10 | 10/10 | killed |
| newline | 10/10 | 8/10 | 10/10 | killed |
| digest | 10/10 | 10/10 | 10/10 | survived |
| known | 10/10 | 8/10 | 10/10 | killed |

All pristine/restored detector processes returned 0 and printed `MUT_FROZEN_REPIN_DETECTOR: pass`. Mutated missing/newline/known returned 1 and printed `MUT_FROZEN_REPIN_DETECTOR: fail`; mutated digest returned 0 and printed `MUT_FROZEN_REPIN_DETECTOR: pass`. There were 120 individual re-pin invocations total. Every failed mutant detector was followed by exact restoration and the same full detector.

## Mutant, expected detector, actual output, verdict

### M1 — delete source-finding-disappearance refusal: killed

Behavior-bearing anchor: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen-repin.py:472-485`; mutation at line 483:

```text
if missing:  ->  if False and missing:
```

Expected detector: the drop-source toy must be refused on the original round-18 inputs, including when `--allow-new-findings` is supplied. Source expectation is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen/expected.json:53-57`.

Actual pristine/restored output: `MADO_FROZEN_REPIN: refused`, rc=1, `target_written=false`; refusal row `{"class":"live_probe","file":"inputs/r13-global-capture.jsonl","line":1,"rule":"wayland-info"}`, kind `source_finding_missing`.

Actual mutant output, both strict and allowed: `MADO_FROZEN_REPIN: written`, rc=0, `expected_findings=10`, `known_misses_kept=0`, `replay=frozen_match`; a target exists without that original expected finding. Two cases fail; **killed**. The committed-tool-only positive control still passes.

### M2 — delete new-line refusal: killed

Anchor: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen-repin.py:473-490`; mutation at line 486:

```text
if outside and not opt["allow"]:  ->  if False and outside and not opt["allow"]:
```

Expected detector: new-line stimulus without the allow flag must refuse `(inputs/r15-libinput-events.jsonl, 6, live_probe, wayland-info)`; with the flag it must write. Both committed and drop-known tools exercise it.

Actual pristine/restored strict output: `MADO_FROZEN_REPIN: refused`, rc=1, kind `finding_on_unexpected_line`, no target. Actual mutant strict output: `MADO_FROZEN_REPIN: written`, rc=0, `replay=frozen_match`; 12 findings with the committed classifier, 11 with the drop-known toy. Both improperly publish without the flag; two cases fail; **killed**. The untouched frozen source has no unexpected-line finding with this tool, so it cannot activate this defect by itself.

### M3 — delete pre-staging source digest check: survived

Anchor: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen-repin.py:421-427`; mutation at line 425:

```text
if hashlib.sha256(data).hexdigest() != digest:
    -> if False and hashlib.sha256(data).hexdigest() != digest:
```

Expected detector: corrupt-pin source must be rejected with rc=2 and no published target. Actual output for both committed and drop-source tools:

```text
pristine: MADO_FROZEN_REPIN: could_not_evaluate
          rc=2; source input does not match its pin: inputs/r15-libinput-events.jsonl
mutated:  MADO_FROZEN_REPIN: could_not_evaluate
          rc=2; staged copy differs from its pin: inputs/r15-libinput-events.jsonl
restored: MADO_FROZEN_REPIN: could_not_evaluate
          rc=2; source input does not match its pin: inputs/r15-libinput-events.jsonl
```

No target or private staging directory remained. All ten detector cases pass: **survived**. The later independent guard is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen-repin.py:457-458`; it catches the same corrupt bytes before scan/publication. This is a detector coverage boundary: the final-result oracle cannot prove the stronger documented pre-copy ordering at lines 7-10. It is **not** evidence that a corrupted baseline can be published, and no broader integrity bypass is claimed.

### M4 — omit retained known misses from output: killed externally, survives self-replay

Carry computation: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen-repin.py:477-481`. Mutation at serialization line 511:

```text
"known_misses": known_kept,  ->  "known_misses": [],
```

Expected detector: the drop-known toy no longer detects `inputs/r13-root.jsonl:4`, whose original note is at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen/expected.json:89-93`. That row/note must remain verbatim in generated `expected.json`.

Actual pristine/restored: `MADO_FROZEN_REPIN: written`, rc=0, ten findings, `known_misses_kept=1`, one published known-miss row, `replay=frozen_match`.

Actual mutant: same written/rc/findings/count/replay fields, **but `expected.json.known_misses=[]`**. The metadata still claims one retained miss. The external row/note comparison reports `known-miss rows were not carried verbatim`; this also fails the drop-known/new-line/allow case. **Killed** by two cases; not killed by the script's own frozen replay. Frozen replay compares current findings, not completeness of the historical miss ledger; see `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1963-1976`. With the committed classifier alone all three source known misses are detected, so retaining zero notes is correct and this mutant survives that positive control.

## Before/after hashes and restoration evidence

B = SHA-256 `7cc8b2cdd7a74c9a2b3131c07b6b4e921d32147fedc58c86afb0027c5688517c`. Every candidate was byte-for-byte B before mutation and after restoration, verified by direct byte equality against the git-show snapshot, not merely matching displayed lines.

| Scratch candidate | Mutated SHA-256 | Before | Restored |
|---|---|---|---|
| missing | `877f0fba7369481147c3d7dbfe3ef4e5e6cb7c5ae864a53945f278a9d67767cd` | B | B |
| newline | `8c2d2636d2f7b4ccb6bd9113630293f14297d9fae893546b0cdecd3109414914` | B | B |
| digest | `1dead649e0ff661f22ab2268948e683d9a3fa254169cdfb543f64775ddda0a61` | B | B |
| known | `146f71697ef7a77f9015c203c2e34e6774006926485dae3ed4e9ff087c104f1d` | B | B |

For example, the missing-finding mutant followed B → `877f0fba7369481147c3d7dbfe3ef4e5e6cb7c5ae864a53945f278a9d67767cd` → B; the complete four-candidate table records each transition. All four restored copies again passed 10/10. Final byte comparisons also found the lane re-pinner, lane classifier, and all eight original frozen files unchanged.

Actual stdout/stderr and complete parsed results remain at `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/{missing,newline,digest,known}/{pristine,mutated,restored}.stdout` and `.stderr`. Each stdout includes the exact per-case argv, outputs, return codes, target status, and generated JSON. Decisive output projections: `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/decisive-output.json`. Snapshot/fixture receipts: `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/metadata.json`. Restoration and verdict summary: `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr/summary.json`. These scratch receipts contain no claim of testing a different committed revision.

## Limits

- Scoped to these four assigned one-line mutations and ten bounded static cases. No live host operations, gate, services, compositor, package manager, network fetch, build, or unrelated test suites were run.
- Only the source-input digest guard at line 425 was mutated, **not** the independent staged-copy, scan-file, tool-receipt, or expected-file digest checks. Surviving this deletion does not establish their coverage.
- New-line and corrupt-pin stimuli are explicitly labeled scratch derivatives; original-lane source bytes were never modified. The finding-drop tools are explicitly requested toys wrapping committed logic, not substitutes for observing the current classifier.
- `frozen_match` proves self-consistency of the generated pin under the selected classifier; these probes show it does not independently protect historical expected findings, admission policy, or the completeness of known-miss notes.
- Only this report was written in the lane; everything executable/generated is under `/tmp/mado-r19-MutFrozenRepin-s_6jn1hr`. No integration, contract change, or fix was made.

## Installs

None.
