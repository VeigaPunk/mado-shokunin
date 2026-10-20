# MutGateR19 — partial

## Attack and result

**Three behavioral mutants killed; two behavioral mutants survived.** The survivors are coverage findings and scenario proposals, not findings that the pristine gate currently implements the defects. The fixed literal selftest rejects all five by its R10 byte-identity assertion; that identity rejection must not be reported as five behavioral kills.

- Axes: version-comparison truth; jj-only detached-HEAD rescue; repository precondition; arbitrary sole-branch resolution; PASS scope honesty. Isolation and exact-byte restoration are invariants of the probe.
- Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` at `01b80946d92b26370d3012a7da655d00dd135154`. Extracted committed bytes with `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 01b80946d92b26370d3012a7da655d00dd135154:tools/mado-verify.sh`.
- Pristine source: `/tmp/MadoR19-MutGateR19-eare3xhl/pristine.sh`; 201,649 bytes; SHA-256 `1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af`.
- Five independent scratch copies under `/tmp/MadoR19-MutGateR19-eare3xhl`; one changed behavior-bearing line per copy. No lane source edits, git writes, jj commands, dispatches, installs, host service/compositor operations, or external gate invocations in another mode.

## Bounded detector and controls

Every direct gate invocation was the same argv shape: `/usr/bin/bash <absolute-copy-path> --selftest`. Cwd was the scratch directory. A fresh explicit process environment contained only:

```text
PATH=/usr/bin:/bin
HOME=/tmp/MadoR19-MutGateR19-eare3xhl/isolated-home
LC_ALL=C
```

`DEFECT_ID` and inherited host-session/gate/stub overrides were absent in the fixed-environment pristine → mutated → restored triples. Each process had a 240-second deadline, including process-group termination on expiry; no deadline expired. Independent copies ran concurrently in batches of five.

All five original pristine controls, original restored controls, repeat pristine controls, and final restored controls exited 0 with empty stderr and exactly:

```text
MADO_SELFTEST: 443/443 assertions passed
```

R10 at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:597-609` compares the derived source to `PIN_MADO` when `DEFECT_ID` is unset/CONTROL, but expects a changed digest for a non-control defect. I did not edit or bypass this assertion. Supplementary runs of each unchanged mutant used its native `DEFECT_ID=MUT_<NAME>` environment interface, solely to distinguish identity rejection from behavioral assertions. These supplementary runs are not misrepresented as an identical-environment triple; the literal triples supply the green controls.

### Single-line mutations and expected detectors

| Mutant | Committed path:line | Mutation | Expected behavioral detector | Behavioral verdict |
|---|---|---|---|---|
| `walker-compare` | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:3295` | `if [ "$kv" = "$WALKER_VERSION_PIN" ]; then` → `if [ "$kv" != "$WALKER_VERSION_PIN" ]; then` | WL1 matching pin → PASS and WL2 drift → FAIL; lines 1263–1282. | **KILLED** |
| `jj-rescue-gate` | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:3723` | `[ -d "$tree/.jj" ] && jcol=1` → `[ -n "$tree/.jj" ] && jcol=1` | OM16 plain-git detached HEAD must name `MOVED: HEAD`; lines 995–1002. | **KILLED** |
| `git-dir-precondition` | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:3687` | `if have git && tmo git -C "$tree" rev-parse --git-dir >/dev/null 2>&1; then` → `if have git; then` | OM13 repository probe rc=128 must yield UNKNOWN on tag/head/vs_head; lines 947–957. | **KILLED** |
| `single-branch-tip` | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:3736` | `tipref=$(printf '%s\n' "$brrefs" | head -1)` → `tipref="refs/heads/master"` | The sole enumerated ref must be used, even when not named master. Existing OM11 only names master (lines 908–918). | **SURVIVED** |
| `pass-text` | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:3296` | Append `; all current claim anchors verified` after `stay dated` in the walker PASS detail; leave the comparator and all existing words unchanged. | WL1 must certify installed version only, not current claim anchors; current checks are substring tests plus one literal forbidden phrase (lines 1265–1269). | **SURVIVED** |

### Clean run results

| Copy / exact direct command | Pristine rc | Literal mutant rc and assertions | Native DEFECT_ID mutant rc and assertions | Restored rc |
|---|---:|---|---|---:|
| `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/walker-compare.sh --selftest` | 0; 443/443 | 2; MADO_SELFTEST: FAILED — 435 passed, 8 failed | 2; MADO_SELFTEST: FAILED — 436 passed, 7 failed | 0; 443/443 |
| `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/jj-rescue-gate.sh --selftest` | 0; 443/443 | 2; MADO_SELFTEST: FAILED — 441 passed, 2 failed | 2; MADO_SELFTEST: FAILED — 442 passed, 1 failed | 0; 443/443 |
| `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/git-dir-precondition.sh --selftest` | 0; 443/443 | 2; MADO_SELFTEST: FAILED — 439 passed, 4 failed | 2; MADO_SELFTEST: FAILED — 440 passed, 3 failed | 0; 443/443 |
| `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/single-branch-tip.sh --selftest` | 0; 443/443 | 2; MADO_SELFTEST: FAILED — 442 passed, 1 failed | 0; MADO_SELFTEST: 443/443 assertions passed | 0; 443/443 |
| `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/pass-text.sh --selftest` | 0; 443/443 | 2; MADO_SELFTEST: FAILED — 442 passed, 1 failed | 0; MADO_SELFTEST: 443/443 assertions passed | 0; 443/443 |

The clean literal mutant runs and all supplementary native-mode runs had empty stderr. Final behavior-only outcome: **3 KILLED / 2 SURVIVED / 0 inconclusive**. Literal exit-only outcome: **5 rejected / 0 survivors**, including two R10-only rejections.

## Actual clean mutant output

Below are complete stdout captures, not reconstructed expected output. Native-mode commands are the same direct command above with only the indicated `DEFECT_ID` added to the explicit environment.

### walker-compare

Literal command: `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/walker-compare.sh --selftest`

```text
MADO_SELFTEST: FAILED — 435 passed, 8 failed
  - R10: derived target equals the recorded gate revision (got '0df103b8cedc2ecea1c2b2615008f3aace0d7630373ba9114c07c19c6509b95b' want '05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0')
  - WL1 (a 2.17.2 binary matches the pin) (want row live.walker.version PASS)
  - WL1: the PASS certifies the installed version only (want row live.walker.version PASS containing 'installed version matches pin')
  - WL1: the PASS says the 2.17.0-era claims are dated, not re-verified (want row live.walker.version PASS containing 'claims measured on 2.17.0 2026-10-14 stay dated')
  - WL1: two walker rows, both PASS (got '1' want '2')
  - WL2 (a moved binary is a FAIL) (want row live.walker.version FAIL)
  - WL2: the FAIL names the new pin (want row live.walker.version FAIL containing 'pin 2.17.2')
  - WL2: the FAIL names what the binary printed (want row live.walker.version FAIL containing '2.17.1')
fixtures kept: /tmp/w5-mado-m52-selftest.3i1nE5
```

Native-mode environment addition: `DEFECT_ID=MUT_WALKER_COMPARE`

```text
MADO_SELFTEST: FAILED — 436 passed, 7 failed
  - WL1 (a 2.17.2 binary matches the pin) (want row live.walker.version PASS)
  - WL1: the PASS certifies the installed version only (want row live.walker.version PASS containing 'installed version matches pin')
  - WL1: the PASS says the 2.17.0-era claims are dated, not re-verified (want row live.walker.version PASS containing 'claims measured on 2.17.0 2026-10-14 stay dated')
  - WL1: two walker rows, both PASS (got '1' want '2')
  - WL2 (a moved binary is a FAIL) (want row live.walker.version FAIL)
  - WL2: the FAIL names the new pin (want row live.walker.version FAIL containing 'pin 2.17.2')
  - WL2: the FAIL names what the binary printed (want row live.walker.version FAIL containing '2.17.1')
fixtures kept: /tmp/w5-mado-m52-selftest.rkMxaL
```

### jj-rescue-gate

Literal command: `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/jj-rescue-gate.sh --selftest`

```text
MADO_SELFTEST: FAILED — 441 passed, 2 failed
  - R10: derived target equals the recorded gate revision (got 'b638e35f2cf99f9d6b407a7beb9ba7ed439c559f26c8a57016b327861ad94de2' want '05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0')
  - OM16: the row names HEAD as what it read (want row omarchy.git.head FAIL containing 'MOVED: HEAD')
fixtures kept: /tmp/w5-mado-m52-selftest.1vQDC1
```

Native-mode environment addition: `DEFECT_ID=MUT_JJ_RESCUE_GATE`

```text
MADO_SELFTEST: FAILED — 442 passed, 1 failed
  - OM16: the row names HEAD as what it read (want row omarchy.git.head FAIL containing 'MOVED: HEAD')
fixtures kept: /tmp/w5-mado-m52-selftest.tASxfi
```

### git-dir-precondition

Literal command: `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/git-dir-precondition.sh --selftest`

```text
MADO_SELFTEST: FAILED — 439 passed, 4 failed
  - R10: derived target equals the recorded gate revision (got 'c87d76fc371b2b9ee63d3e9d873282bdb91fc9a5986718b7d6c07582855c7739' want '05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0')
  - OM13 (no repository: unverified) (want row omarchy.git.tag UNKNOWN)
  - OM13: the UNKNOWN names the tree that is not a checkout (want row omarchy.git.tag UNKNOWN containing 'no git checkout at')
  - OM13: exactly three omarchy UNKNOWNs (tag + head + vs_head) (got '0' want '3')
fixtures kept: /tmp/w5-mado-m52-selftest.C7CNuN
```

Native-mode environment addition: `DEFECT_ID=MUT_GIT_DIR_PRECONDITION`

```text
MADO_SELFTEST: FAILED — 440 passed, 3 failed
  - OM13 (no repository: unverified) (want row omarchy.git.tag UNKNOWN)
  - OM13: the UNKNOWN names the tree that is not a checkout (want row omarchy.git.tag UNKNOWN containing 'no git checkout at')
  - OM13: exactly three omarchy UNKNOWNs (tag + head + vs_head) (got '0' want '3')
fixtures kept: /tmp/w5-mado-m52-selftest.Hqldd9
```

### single-branch-tip

Literal command: `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/single-branch-tip.sh --selftest`

```text
MADO_SELFTEST: FAILED — 442 passed, 1 failed
  - R10: derived target equals the recorded gate revision (got '136090176ac7b9f1452d3e1c4311e5dd3cfaef5fbfea938af1f59e6da6f7a538' want '05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0')
fixtures kept: /tmp/w5-mado-m52-selftest.T9KoWx
```

Native-mode environment addition: `DEFECT_ID=MUT_SINGLE_BRANCH_TIP`

```text
MADO_SELFTEST: 443/443 assertions passed
```

### pass-text

Literal command: `/usr/bin/bash /tmp/MadoR19-MutGateR19-eare3xhl/pass-text.sh --selftest`

```text
MADO_SELFTEST: FAILED — 442 passed, 1 failed
  - R10: derived target equals the recorded gate revision (got 'c7c9a9e11eb75c834611e2b1aec92276e475f6f67a4f1bae5f951280574f30d3' want '05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0')
fixtures kept: /tmp/w5-mado-m52-selftest.QSRP3P
```

Native-mode environment addition: `DEFECT_ID=MUT_PASS_TEXT`

```text
MADO_SELFTEST: 443/443 assertions passed
```

## Survivor scenario proposals

### S1 — Sole detached branch is not master

Evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:3733-3737` promises to read the exactly-one ref returned by `for-each-ref`. The hard-coded-master mutant passed every behavioral assertion. Existing OM11 (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:908-918`) uses only `refs/heads/master`; the stub default at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:713-718` also uses master.

Propose a hermetic OM case with `.jj` present, detached HEAD, and **exactly one** branch named `refs/heads/release`, with no `refs/heads/master`. Set its tip to the pinned commit. Require tag/head PASS details to name `refs/heads/release`; require a fixture call ledger to show `rev-parse --verify refs/heads/release` and never master. Make the git stub reject requests for nonexistent refs, rather than returning the same commit for any ref. [INFERENCE] This distinguishes the current correct sole-ref selection from the tested survivor without changing the contract. It was proposed, not executed or added to the lane.

### S2 — PASS cannot append a new current-claim assurance

Evidence: the mutant at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:3296` preserves both positive substrings checked by WL1 and does not contain the single literal blacklist phrase `claims re-verified` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:1265-1269`), yet adds `all current claim anchors verified`. Both fixed-environment behavior assertions and native defect mode accepted it.

Propose using the existing exact-detail assertion helper (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:444-448`) on WL1, comparing the whole `live.walker.version PASS` detail to:

```text
2.17.2 (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)
```

[INFERENCE] Exact expected detail kills this appended assurance and equivalent extra wording without trying to maintain an open-ended semantic blacklist. The scope remains the installed-version certificate plus dated-measurement caveat; no new gate behavior is requested. This scenario was proposed, not executed or added.

## First literal batch: retained but not used for attribution

The first fixed-environment mutant batch also had unrelated fixture-disappearance failures and nonempty stderr. Its literal rc values were all 2, but those failure totals are **inconclusive for behavioral attribution**, not additional kills. I retained every receipt and repeated the complete literal pristine → mutant → restore experiment; the clean repeated results above replace it for attribution.

| First literal batch mutant | Actual stdout summary | stderr bytes |
|---|---|---:|
| `walker-compare` | MADO_SELFTEST: FAILED — 367 passed, 76 failed | 3040 |
| `jj-rescue-gate` | MADO_SELFTEST: FAILED — 373 passed, 70 failed | 3040 |
| `git-dir-precondition` | MADO_SELFTEST: FAILED — 371 passed, 72 failed | 3070 |
| `single-branch-tip` | MADO_SELFTEST: FAILED — 384 passed, 59 failed | 2396 |
| `pass-text` | MADO_SELFTEST: FAILED — 384 passed, 59 failed | 2126 |

Example captured stderr (verbatim):

```text
cp: cannot stat '/tmp/w5-mado-m52-selftest.nxKFMh/clean/.': No such file or directory
```

[UNK] The actor/cause of the missing fixture roots was not identified. No cleanup of any selftest fixture root was performed by this probe runner. Two relevant gate-running peers were asked to restrict cleanup to their own exact receipt paths. The same five mutations, same environment, and same commands subsequently produced the clean results above. No timeouts occurred in either batch.

## Hashes and restoration evidence

Both mutation passes restored all five exact preimages in a `finally` path before running restored controls. The bytes after restoration compared equal to the committed byte array for every copy. Before/after source hashes within every detector invocation were unchanged.

Common pristine/restored SHA-256: `1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af` (201,649 bytes).

| Copy | Mutated SHA-256 (literal and native) | Exact-byte restoration, both passes | Final restored control |
|---|---|---|---|
| `/tmp/MadoR19-MutGateR19-eare3xhl/walker-compare.sh` | `c63b11fa2e4f46a900351119bb47b0f8d66449532e81c237893eb8ea49274b4e` | True / True; common SHA above | rc 0; 443/443; stderr empty |
| `/tmp/MadoR19-MutGateR19-eare3xhl/jj-rescue-gate.sh` | `7593d2c57e3365b2c3ee2a5a459b033b85f808ff747f700722969d963f0eb82d` | True / True; common SHA above | rc 0; 443/443; stderr empty |
| `/tmp/MadoR19-MutGateR19-eare3xhl/git-dir-precondition.sh` | `6cc9f7a6c2b90ab7688f478ed294e0e3e769a66246a6d323b6b0ea8d1b5661e0` | True / True; common SHA above | rc 0; 443/443; stderr empty |
| `/tmp/MadoR19-MutGateR19-eare3xhl/single-branch-tip.sh` | `dfa0cbc29ba3dd72dadfbd3e08b4116a20ba2f0df8290dccb090a0f9c68d2100` | True / True; common SHA above | rc 0; 443/443; stderr empty |
| `/tmp/MadoR19-MutGateR19-eare3xhl/pass-text.sh` | `997cfbf241bf32b14518220993440f4c24742cd6bc5511b61ea94452b894f4b6` | True / True; common SHA above | rc 0; 443/443; stderr empty |

- First restoration receipt: `/tmp/MadoR19-MutGateR19-eare3xhl/restoration.json`.
- Final restoration receipt: `/tmp/MadoR19-MutGateR19-eare3xhl/restoration-repeat.json`.
- Complete receipt index: `/tmp/MadoR19-MutGateR19-eare3xhl/receipt-index.json`; SHA-256 `d1d29ea26baee182bb3ca9ec3f449e359d65d64fa3e229c7056ef558b481fabc`.
- All 35 command receipts (full argv/environment/cwd/timestamp/deadline result/stdout/stderr/before-and-after hashes) are indexed individually with SHA-256 and retained under `/tmp/MadoR19-MutGateR19-eare3xhl`. The clean fixed-environment stages are `pristine-repeat`, `mutated-literal-repeat`, and `restored-repeat`; native supplement is `mutated-defect-id`. First-pass receipts are retained separately, never overwritten.

## Limits

- Attack only: no judgment of C1/C2/C3, no integration or shipping, no changes to lane source, tests, documentation, pins, or contract. Only this scoped report is written in the lane.
- These are five selected single-line defects, not exhaustive mutation coverage. The two survivors do not show the pristine implementation contains either defect.
- R10 digest rejection is source-identity protection, not behavioral coverage. Supplementary native-mode evidence is explicitly separated from the fixed-environment triple.
- The selected `.jj` mutant is killed by one OM16 **ref-label** assertion, not by a status difference. The stub at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:711-712` returns TIP/HEAD independently of the requested ref, and OM16 (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:991-994`) does not supply a separate TIP. Thus this probe must not be described as proving that fixture independently detects every false-PASS rescue.
- First-batch disappearing fixtures remain an identified evidence limitation, with the actual errors preserved. Clean repeated triples have no such stderr or unrelated assertions.
- No live host behavior, gate `--regression`, modified detector, or proposed extra scenario was invoked directly. All direct gate executions used scratch copies and `--selftest` only. The selftest itself runs its own canned fixtures and usage-refusal subcases.

## Installs

None.
