author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# Round 59 verifier spot-check — mado (closed 2026-10-31/2026-11-01 UTC)

Non-author closure of mado round 59. Base `6f2e4115dc1ebeb87c4d1aba9803c04c82dc4c80`,
head `25294ab3e426903c18f16ad98db76e5e24147a98` (branch tip, pushed). All git work
index-free (`rev-parse`/`cat-file`/`ls-tree`/`diff-tree`/`merge-base --is-ancestor`/`show`/`log`);
re-runs of lane-owned instruments were executed from committed bytes extracted to scratch,
never from the lane working tree. Security boundary held: no r56-era credential material
opened, excerpted, or surfaced.

## 1. Step-1 conformance

| check | result | evidence |
|---|---|---|
| report committed by lane identity | OK | fleet commit `3ed2a220a7f97b9b111f33efa731250bcebfcbdb`, author `mado-shokunin <mado@shokunin.local>`, path `.ufo/reports/round-59/mado.md` |
| `SHONEN` heading | OK | report carries `## SHONEN` with four `[~]` lines (no author-written `[x]`) |
| cited lane commits exist + ancestors of master | OK | `git merge-base --is-ancestor` OK for `054dcecf…`, `3eb5f5ee…`, `25294ab3…` |
| branch tip pushed | OK | `git ls-remote origin refs/heads/master` = local `refs/heads/master` = `25294ab3e426903c18f16ad98db76e5e24147a98` |
| cited work reachable in `6f2e4115..25294ab3` | OK | exactly three commits (landing `054dcecf`, follow-up `3eb5f5ee`, receipt correction `25294ab3`); parent chain is base→landing→follow-up→tip |
| dispatch/complete digest | OK | contract digest `launch mado round=59 base=6f2e4115dc1e` / `complete mado round=59 head=25294ab3e426 pushed=True` matches the tree |
| marker rule | not a marker | report names real committed work with resolvable hashes and evidence pointers throughout |
| landing diff shape | OK as claimed | `git diff-tree -r --stat 6f2e4115 054dcecf` → 26 files, +888/−17 (matches report); base→tip 29 files, +895/−17 |

No conformance bar to admission found. Status-neutral cosmetic defects are in § 6.

## 2. Per-claim re-check

Methods: `re-measured` = I ran the instrument myself against committed bytes;
`evidence-verified` = I verified the committed receipt and the state it pins.

### C1 — calibration (re-measured)

Commands (`git show <rev>:<path> | grep -c …`), base vs landing vs tip:

| grep | base | landing | tip |
|---|---|---|---|
| `'## Corrections (round 59)'` in `corpus/lessons/round-58.md` | 0 | 1 | 1 |
| `'9113c7c05e58'` in `corpus/lessons/round-58.md` | 0 | 1 | 1 |
| `'^source:'` in `corpus/knowledge/windows-desktop-plane-r57.md` | 0 | 1 | 1 |
| `'^source:'` in `corpus/knowledge/windows-permonitor-dpi-r58.md` | 0 | 1 | 1 |

`git diff-tree -r --numstat 6f2e4115 25294ab3 -- <two entries + r58 lesson>` →
`17 0` (r57 entry: trio +4 lines + errata append), `5 0` (r58 entry: trio), `18 0`
(r58 lesson corrections block) — insertions only, zero deleted lines, append-only
discipline held. Frozen gate identity re-measured: `git rev-parse 6f2e4115:tools/mado-verify.sh`
= `git rev-parse 25294ab3:tools/mado-verify.sh` = blob `9113c7c05e586328f44ed6822a3d12ff34c47a36`;
`git show 25294ab3:tools/mado-verify.sh | sha256sum` = `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1`;
`| wc -l` = 4194 — byte-identical to the receipt `gate-identity-r59.txt` and the corrections text.
`git diff-tree -r 6f2e4115 25294ab3 -- tools/` → empty (frozen gate untouched).
**Verdict: verifies (TARGET_MET confirmed).**

### C2 — operability (re-measured at both base and tip bytes)

Committed bytes of `quality/check-tool-ledger.py`, `quality/check-wave-done.py` and
`.ufo/waves/round-59/receipts/casefold-probe.py` extracted to scratch at base `6f2e4115`
and tip `25294ab3`; probe imports the checkers relative to its own tree, so each run tested
exactly the revision's bytes.

- RED at base bytes (my run): `CASEFOLD_PROBE: BYPASS (bypasses=2)`, rc=**1** —
  `C:/DEV/shm/…` ACCEPTED by both checkers; `C:/TMP` and `C:/VAR/tmp` REFUSED at base
  (masking confirmed, per-prefix table matches receipt `casefold-before.txt`).
- GREEN at tip bytes (my run): `CASEFOLD_PROBE: NO-BYPASS (bypasses=0)`, rc=**0**
  (matches `casefold-after.txt`).
- Selftests at tip bytes (my runs): `LEDGER_SELFTEST: 55/55 passed` rc=0;
  `MADO_WAVE_DONE_SELFTEST: 63/63 passed` rc=0.
- CLI refusals re-run ×4 at tip bytes: `--work C:/DEV/shm/…` and `--work C:/tmp/…`
  on both checkers → rc=**2** each, messages match `casefold-cli-refusals.txt`.
- Home refusal re-run: `--work C:/Users/jpvei/mado-r59-homeprobe` → rc=**2**
  ("refusing work dir inside the home directory"), matches `failclosed-after-r59.txt`.
- Fix shape: `os.path.normcase` in the prefix compare — `normcase` occurrences 0→8 in both
  checkers; named pin `refuse-work-casefold` present at tip, absent at base;
  `SELFTEST_CHECKS = 55 if os.name == "nt" else 54` (host-derived), pin Windows-conditional.
- Host left clean: `C:/DEV` verified absent after all runs; no home or `C:\tmp` probe residue.
- Production ledger (my run at tip): `LEDGER: population=99 ledger_rows=99 uncovered=0
  dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=25294ab3…`, rc=0.

**Verdict: verifies (TARGET_MET confirmed); the red is independently reproduced at base
bytes, not taken on receipt alone.**

### C3 — coverage, sourced (re-measured)

| count | base | tip | command |
|---|---|---|---|
| knowledge files | 73 | **74** | `git ls-tree -r --name-only <rev> corpus/knowledge \| grep -c '\.md$'` |
| README index rows | 73 | **74** | `git show <rev>:corpus/README.md \| grep -cE '^\| `knowledge/[^`]+\.md`'` |
| SOURCES rows | 341 | **342** | `git show <rev>:corpus/SOURCES.md \| grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` |
| DWM entry rows | — | **14** (4 H + 6 K + 4 J) | `grep -cE '^\| [HJK][0-9]{2} '` on the committed entry |

- Navigation counter re-run at the **final tip** (literal SCORECARD fence; fence sha256
  `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` — matches the
  SCORECARD's `8b59b503…` pin): `revision=25294ab3… indexed=74/74 missing=0 dangling=0
  duplicates=0 coverage=10.0000/10`, exit 0.
- Used-by counter (frozen `quality/counters/c3-r56-used-by.py`, PRED-C3-r56-v2) re-run at
  the final tip: `MADO_USED_BY: rev=25294ab3… entries=74 rows=342 missing=0 extra=0
  dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none`, exit 0.
  Receipts: `usedby-before-r59.txt` = missing=2 TARGET_MISSED at base (the M59-4 defect),
  `usedby-after-r59.txt` = missing=0 TARGET_MET — reproduced.
- DWM probe re-run (my run): rc=0, `SERVICES 0`, `SC_UXSMS_RC=1060`, dwm.exe `tasklist /svc`
  services `N/A`, `DWM_COMPOSITION hr=0 enabled=True`, build 26200 — matches receipts;
  committed `dwm-service-run1.txt` and `run2.txt` are byte-identical (`diff` clean).
- Entry structure: provenance trio first (`source:` S399/S400/S405, `verified-at:`,
  `recheck: on-release`); H rows carry re-derivation commands; K rows carry dated
  `[INF-docs]` quotes; joins carry named limits; § 4 closes D01.
- S405 row + used-by discipline: the SOURCES.md diff shows only the new S405 row, the
  in-place `used-by` extensions on S399/S400/S402/S404 (the contract's allowed in-place
  cell), and the search-log append — no proposition cell touched.

**Verdict: verifies (TARGET_MET confirmed).**

### D01 closure honesty (the round-note focus)

The r57 entry records: "Flip: a sourced row that states the Win11 DWM service model."
The r59 closure quotes that flip verbatim and closes **flip-met on a Windows-8-labeled
row** (S405 Platforms "Clients – Windows 8", carried verbatim) joined to build-26200 host
probes, naming the residue ("no Win11-labeled model sentence in the bounded sweep") in the
entry § Scope and § 4, the r57 errata append, the search log, the lesson, and the report.
The r57 question — "which sentence describes the build-26200 service model is not
resolvable from these rows" — is genuinely answered (S405's model + every observable host
probe in agreement). The literal "Win11-labeled" reading is unmet and is disclosed rather
than smoothed; I judge the closure honest, with the residue on record for a future
strengthening pin. No defect; recorded so the reading is visible to the operator.

## 3. Discernment spot-check (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S405 row (Microsoft Learn Compatibility Cookbook) — admit | admit | URL re-opened live 2026-10-31 (`learn.microsoft.com/en-us/windows/compatibility/desktop-window-manager-is-always-on`) | **agree** | located quote verbatim in § Description; ms.date 2018-07-11, `git_commit_id 40f2250e0d45a6cdf02bd22408933c9ee4c10d78`, updated_at 2021-11-17, Platforms "Clients – Windows 8, Servers – Windows Server 2012" all match the row; quote is 19 words (≤25); tier A docs appropriate; no Win11-labeled sentence exists on the page, so the carried residue is real |
| C2 checker case-fold hardening — admit | admit | re-ran the probe at base and tip bytes + both selftests + CLI/home refusals from committed bytes | **agree** | red rc=1 bypasses=2 at base bytes, green rc=0 at tip, 55/55 and 63/63, refusals intact, host left clean — the fix demonstrably kills the pre-change behavior |
| Reject: rewriting `tools/mado-verify.sh` | reject | blob identity re-measured base→tip (unchanged `9113c7c0…`); r58 receipt `.ufo/waves/round-58/receipts/gate-selftest-windows.txt` shows the Windows selftest failing on POSIX symlink fixtures | **agree** | selftest genuinely non-runnable on this host; keeping the bytes frozen keeps every pinned blob identity resolving — a rewrite would orphan the record the round itself corrects |
| Reject: declaring D01 closed on host probes alone | reject | entry § 4 vs the r57 D01 record | **agree** | the recorded flip demands a sourced row; S405 was required, was opened and quoted this round, and the residue is carried rather than smoothed |

Also re-ran `sources-census.sh validate --root <fleet-root> mado`: **exit 0**, warning set
36 × W04 + 1 × W01 + `mado ok` — same shape as the committed `census-after.txt`.

## 4. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** | C1 verified: records corrected to observed state, append-only, gate identity re-derived |
| operability | **improved** | C2 verified: demonstrated bypass class closed red→green with named pins; fail-closed refusals intact |
| coverage | **improved** | C3 verified: third sourced Windows-plane entry lands, indexed 74/74, used-by missing 2→0 |
| freshness | unchanged | no freshness rubric touched; DWM entry carries `recheck: on-release`; dormant rubrics stay routed to L0, not re-graded |
| depth | unchanged | not claimed, not worked |
| adjacency | unchanged (not harmed) | `C:\tmp`/`C:\var` third-party content observed and reported, not absorbed; no cross-domain write |

No axis harmed. SCORECARD.md diff base→head is a pure append (+51/−0); `tools/` diff empty;
census, navigation, used-by and ledger counters all green at the tip.

## 5. Trend verdicts (verified)

- **expansion: improved** — new admitted entry on uncovered ground (DWM service model),
  `source:` citing the mined S405 row; knowledge 73→74, index rows 73→74, registry 341→342,
  navigation 74/74 exit 0 (my run at tip).
- **quality: improved** — the fail-closed checkers survive a demonstrated bypass class
  (red reproduced at base bytes, green at tip, named pins, host-derived counts); the
  records were corrected to observed state; no admitted entry failed a re-check (census,
  navigation, used-by, ledger all green at tip).
- **discernment: improved** — corrections carried with re-derivation commands; D01 closed
  with its residue named instead of smoothed; four mistakes mined, including M59-4 caught
  against the round's own errata; this spot-check agrees with the sampled admits and rejects.

## 6. Routed defects / notes (status-neutral, none bar admission)

1. **SCORECARD C1 row parenthetical number-shape drift.** The row's counting command is a
   per-file `git diff --stat` but its parenthetical reads "(+4/−0, +5/−0)"; the actual
   per-file insertions at the landing are **+17/−0** (r57 entry: trio +4 + errata +13) and
   +5/−0 (r58 entry). The report's own numbers (+17/−0, +5/−0) are exact and the load-bearing
   property (insertions only, no existing line modified) is verified true. The lane may align
   the parenthetical append-only next round. Same class: the lesson's trio note "+4/−0 each"
   describes the trios, not the per-file diffs.
2. **LOG round-59 tail bullet says "Mined M59-1..M59-3"** while the lesson and the same LOG
   entry (harm-watch bullet) carry M59-1..M59-4. Cosmetic; no correction entry required
   beyond noting it here.
3. **D01 "flip met" reading** — recorded flip literal says "Win11"; landed row is
   Windows-8-labeled; residue disclosed in five places (see § 2). Judged honest; no routing.
4. **L2 floor unmet** — no AgentSwarm dispatch surface on this host; disclosed since r57,
   L0 open, routed around. Operator-owned.
5. **Round-start census run not tee'd to a file** — disclosed by the lane; end receipt
   committed; this verifier's own validator run exits 0 with the same warning set.
6. **SHONEN boxes** — all four remain `[~]` on historical assertions; nothing this round
   (L1-only, no new end-to-end desktop task) makes them `[x]`-able by a non-author. Operator
   note only; not checkable here.
7. **Security boundary** — this closure opened no r56-era credential material; only counts,
   shapes, and lane-authored round-59 artifacts were read. Receipts contain paths, not secrets.

## 7. Closure

All three declared claims verify (C1, C2, C3 re-measured; receipts corroborate). No axis
harmed. The round is **admitted**; lane-round `mado` round 59 records **ok**.
