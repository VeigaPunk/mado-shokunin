# CritRegistration50 — attack on `.ufo/waves/round-50/registration.md` at b4a79843

Seat: CritRegistration50 (mado round 50, hyaku run 10 attempt 2, wave w2 = FALSIFY, policy v1).
Target: the registration document vs the frozen bytes it names. Method: re-derived every named
sha256, checked every named receipt path and final line, resolved every control name to its
receipt, diffed the predicate text against the counters' final-line format, and re-ran both
frozen counters on a `git clone -q --shared` of the lane (scratch:
`/fast/scratch/hyaku/mado-r50/CritRegistration50`, TMPDIR under it, destroyed after the run).

## Verdict

The registration is **sound on hashes, receipt existence, control outcomes, nonce math and
reproducibility** — every named sha256 re-derives, every quoted receipt final line matches, both
counters reproduce the committed receipts byte-identically at `906178b6`. **3 defects + 1
low-severity exactness note** found, all in registration prose about C1 clause g and one manifest
defect; none changes a counter verdict.

## Defects

### D-A (substantive): the C1 "At data" parenthetical describes a clause g that does not exist

`registration.md` C1, At-data sentence: the receipt `c1-at-data.txt` "covers the
w1/RevC1Counter two-nonce gap **in that clause g's 150 cases are generated and judged at count
time inside the single run**".

Evidence against — the frozen counter `quality/counters/c1-r50-bind-entry.py` @906178b6:

- `grep -n 'nonce\|random\|150'` over the 1316-line counter: no nonce, no randomness; the only
  "150" hits are the clause-i shingle threshold (`:110` docstring, `:1035` `novel = len(es) >= 150`).
- `clause_g` source (`:815`): docstring "Held S319 is cited and unchanged; no new row
  re-registers a held source" — a registry held-ground check, not a sampler.
- Committed receipt `.ufo/waves/round-50/receipts/c1-at-data.txt:26` prints
  `clause=g held=S319 unchanged=1 pins=1 held_urls=1` — no cases are generated anywhere.

The "150 generated cases judged at count time" and the "two-nonce gap" belong to the **round-49
keysym counter** PRED-C1-r49 as reviewed by `w1/RevC1Counter.md:5,12,16`
(`g generated=150/150`; "Two-nonce requirement remains a verification gap, not a pass." —
about `c1-r49-keysym.py`). The r50 bind-entry receipt cannot, and does not, cover that gap.
(The byte-compare half of the same parenthetical is true: receipt line
`clause=r replay=ok sha=9a47199e2297 …` matches the digest pinned at
`corpus/knowledge/hyprland-bind-key-match-r50.md:105`.)

Smallest safe correction: delete the false clause, or replace with the true statement — the
frozen c1-r50 counter is deterministic and nonce-free; its clause g checks that held row S319 is
cited and unchanged.

### D-B (substantive): the Residuals repeat the false 150-case claim and mis-attribute it

`registration.md` Residuals: "**C1 clause g samples 150 generated cases per run**; it is a
bounded adversarial sample, not exhaustive proof (**w1/CritC1Args**)."

- False for the same reason as D-A (r50 clause g samples nothing).
- Mis-attributed: `w1/CritC1Args.md` (18 lines) is the landed-tool ARG-comparison seat
  (`pairs=5005 mismatches=0`); it contains no clause-g, 150-case or nonce statement
  (`grep -n '150\|clause g\|nonce'` → no hits). The 150-case/one-nonce discussion lives in
  `w1/RevC1Counter.md` and concerns PRED-C1-r49.

Smallest safe correction: remove the residual, or re-state it against PRED-C1-r49
(`quality/counters/c1-r49-keysym.py`, whose clause g does generate 150 nonce-seeded cases) with
the correct seat citation.

### D-C (minor): the frozen fetch manifest carries an unverifiable self-entry

`.ufo/waves/round-50/fetch/SHA256SUMS` lists itself (`bb21f728…  SHA256SUMS`). Actual file
sha256 is `e2b91106…`; `sha256sum -c SHA256SUMS` → "1 computed checksum(s) did NOT match". A
self-referential digest is unverifiable by construction. All 15 real pin files verify OK, and no
counter reads the SUMS (counters bind per-row digests in `corpus/SOURCES.md`), so there is no
scoring impact — but the manifest as published fails its own check. Round-49 manifests do not
self-list (checked `round-49/w1/ExecXkbSrc/fetch/SHA256SUMS` and
`round-49/w1/ScrRows/pins/SHA256SUMS`; also the freeze-time
`w1/ExecHostGuardR50/receipts/SHA256SUMS` has no self-entry and verifies 16/16).

Smallest safe correction: drop the self-line from the SUMS.

### D-D (low): kill-rule predicate sentences are abbreviations, not the emitted line

- c1-r50 final line (source `:1306`): `PRED-C1-r50: clauses=… admitted=N/1
  verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`; the registration's "TARGET_MET sentence"
  drops the `PRED-C1-r50: ` prefix and the ` rev=` suffix.
- c2-r50 final line (source `:566-567`): `PRED-C2-r50: selftest=… names=… red=… green=…
  scope=… verdict=… rev=…`; same abbreviation.
- The receipt files' final line is the `exit=N` trailer; the verdict sentence is second-to-last.

Severity low: the kill rule's "at rev `906178b6…`" qualifier plus each counter docstring's own
"Final line:" format make the intent unambiguous, and every receipt matches modulo the
documented rev suffix. But as written ("not exactly the TARGET_MET sentence") the rule is not
literally satisfiable. Smallest safe correction: quote the full emitted format including the
rev field, and say "verdict line".

## Verified consistent (no defect)

1. **All 9 named content hashes re-derive at `906178b6`**: entry `ae8f8d4d…`, lesson
   `e7cd2962…`, SOURCES.md `b3a1a041…`, gate v3 `ffdc9d62…`, check-wave-done.py `10f4359a…`,
   hostguard `fdaa5c2e…`, binds-live-r50.txt `9f16e5a5…`, c1 counter `e162d671…`, c2 counter
   `1d52a62c…`. Counter bytes identical at 470bfd77 / 906178b6 / b4a79843; receipt file
   identical at all three revs.
2. **Receipts exist, final lines match the quotes**: c1-at-data.txt (TARGET_MET, rev 906178b6,
   rc 0); controls-c1.txt c00 `a:0`, c13 `f:0 r:0`, c12 `b:0 e:0 f:0 g:0 h:0 i:0 j:0 r:0` (all
   TARGET_MISSED rc 1); c2-at-data-nonce50117 `red=42/42 green=44/44`, nonce778899
   `red=44/44 green=41/41` (both TARGET_MET rc 0, GATE sha256 `ffdc9d62…`); controls-c2.txt at
   nonce 602211 c00 `red=0/41 green=0/40`, c12 `selftest=34/94 green=0/40`, c14
   `selftest=93/94 red=0/41` (all TARGET_MISSED rc 1).
3. **Live re-runs reproduce both receipts byte-identically** on the shared clone at `906178b6`:
   c2 nonce 50117 rc=0 with identical final line; c1 rc=0, identical output including
   `clause=r replay=ok sha=9a47199e2297 binds=192 forms=named:142,code:42,mouse:6,switch:2`.
4. **C2 nonce math** (source `:475-476`: `k_red=40+nonce%5`, `k_green=40+(nonce//7)%5`)
   reproduces 42/44 (50117), 44/41 (778899), 41/40 (controls 602211) — matches every quote.
5. **w1 = 54 seats**: dispatch taskCall tasks=54, registry members=54, results rows=54, seat
   reports=54; every results row is `output: null` + the run-9 wrap-up note (contract-valid per
   criterion 102 after repair `8dbbf61a`); the four cut-off seats' reports exist as stubs
   (CritC1Random 1 line, CritC1Exotic 3, MutC2Entry 15, CritQuality 1) — matches "all 54 seat
   reports had landed" + M50-4.
6. **claims.md unchanged** `13631f24` → `b4a79843` (empty diff); `13631f24` is the attempt-1
   commit id, not a content hash.
7. **D2**: `round-49/w1-results.json` = 45 rows, 0 nulls-without-note.
8. **D4**: ExecDoNothing — 8 do-nothing controls MISS (c1 c00/c02/c03/c11, c2 c11/c12/c13/c14)
   + 1 positive control MET (c10-candidate), run on the committed round-49 counters at
   `13631f24` (receipt headers sha256 `2597c204…` / `bc171714…` = `git show 13631f24:<path> |
   sha256sum`).
9. **D6**: criteria 100-101 land at `corpus/QUALITY.md:560,566` (scope M49-1/M49-3; 102 is the
   D2-scope criterion at :569).
10. **D7**: 16 hostguard receipts, `sha256sum -c SHA256SUMS` clean 16/16; freeze
    `receipts/selftests.txt` shows `MADO_HOSTGUARD_SELFTEST: 45/45 passed` at the installed path
    plus gate selftest 94/94 and wave-done 58/58.
11. **D8**: erratum at `corpus/lessons/round-49.md:65-71` with its counting command and the
    corrected 2/5 counts.
12. **fetch/**: 16 files; the 15 data files verify against the SUMS except the self-entry
    (D-C); 14 upstream pins byte-equal to round-49 (`cmp` each), `binds-live-r50.txt` new — as
    the registration states.
13. **w1 counter lineage**: w1 C2 draft at `w1/ExecCounterC2R50/c2-r50-session-gate.py` ==
    frozen bytes (`1d52a62c…`) — the "same counter bytes" claim holds; w1 C1 draft `17ad31c1…`
    differs from frozen `e162d671…` but the registration discloses the post-w1 hardening, and the
    disclosed repairs are present (F1 marker source `:346`; F2 receipt pinning `RECEIPT_NAME`
    `:203`; F5 no-pins short-circuit `:1254-1264` prints `clause=c fetch_pins=0` + the vector it
    ran).
14. **w1-controls parenthetical digests resolve**: stub `3c0a46b9…` = w1 control-stub GATE
    line; v2-scope-all `8e2b8e43…` and v3-ufo-default `3758808c…` = the w1 receipt notes, the
    latter equal to the freeze c14 GATE sha256 in controls-c2.txt; R7/R8/R9 rule-removal mutants
    each drop exactly their family (`w1/ExecCounterC2R50/receipts/mutants.txt`).
15. **"byte-identical to the round-49 draft"** (v3 gate): `w1/ExecGateV3/check-session-material.py`
    = `ffdc9d62…` = `round-49/w1/ExecSessionShapes/check-session-material.py` ✓.
16. **Residual 228**: `w1/ExecGateV3/receipts/base-scan-v3-all.txt:6`
    `SESSION_MATERIAL: files=23270 findings=228 rev=8ae47b95…` ✓ at base scope-all.
17. **README row** `corpus/README.md:77`, **Frontier bullet** `:114`, **SKILL.md pointer**
    `:2241` all name the entry / rows S352-S363.
18. **D1**: `make-w1-spec.py:181` asserts `len(carried) == 38`.
19. **wave-done**: `receipts/wave-done-r50.txt` `WAVE wave=w1 ready=1 results=present seats=54
    dispatched=54 settled=54 verdict=OK` at rev `8dbbf61a`.

## Reproduction (counter re-runs, exercised)

```
git clone -q --shared /home/vgpnk/Projects/shokunin/mado-shokunin <scratch>/clone
TMPDIR=<scratch>/tmp python3 -I <scratch>/clone/quality/counters/c2-r50-session-gate.py \
  --repo <scratch>/clone --rev 906178b607f2071af7c2efec5aad976a8bfa5757 \
  --work <scratch>/work-c2 --nonce 50117
# → PRED-C2-r50: selftest=94/94 names=69/69 red=42/42 green=44/44 scope=seen verdict=TARGET_MET rev=906178b6…  (rc 0, byte-identical to receipts/c2-at-data-nonce50117.txt)
TMPDIR=<scratch>/tmp-c1 python3 -I <scratch>/clone/quality/counters/c1-r50-bind-entry.py \
  --repo <scratch>/clone --rev 906178b607f2071af7c2efec5aad976a8bfa5757
# → PRED-C1-r50: clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET rev=906178b6…  (rc 0, diff-clean vs receipts/c1-at-data.txt modulo the receipt's exit=0 trailer)
```

Note: c1's clause f/r read the live compositor socket read-only (`hyprctl binds -j`) — an
allowed read; the replay matched the pinned digest, i.e. the host state is unchanged since the
freeze. Raw re-run outputs are copied at `w2/CritRegistration50/reruns/c1-at-data.rerun.txt`
and `w2/CritRegistration50/reruns/c2-nonce50117.rerun.txt` (derived evidence; the scratch
trees were destroyed).

## Tooling installs

None (python3/git/sha256sum/diff only).
