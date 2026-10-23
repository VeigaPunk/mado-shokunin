# RcHermeticSelfTest310 — C2 ledger attack on CapHermeticSelfTest310

Seat: `MadoR25A3.RcHermeticSelfTest310` (reviewer, leaf). Wave: round-25 attempt 3, `a3w2` (data + falsify).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/a3w1/reports/CapHermeticSelfTest310.md` —
a C2 row re-run of `SCORECARD.md:310` (`hermetic self-test`) at base `41cc04c8`.

## What I did

1. Read the target report. Its claims: row 310 is `| hermetic self-test | 269 assertions over isolated fixtures |
   \`bash tools/mado-verify.sh --selftest\` → 269/269, \`gate-selftest-after.txt\` | 5 (re-demonstrated 12) |`;
   re-run prints `MADO_SELFTEST: 460/460 assertions passed`, exit 0, wall 26.30 s, clean `git status`; superseding
   chain lines 529 / 1005 / 1136 / 1192 / 1221 / 1400 / 1577; "contradiction: none"; round-12 receipt headerless;
   ledger verdict `works` with the 269 figure stale.
2. Dumped `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md` to
   `/fast/scratch/hyaku/mado-r25a3/rc/scorecard-41cc04c8.md` (1,618 lines — matches the report's claim).
3. Independent sandbox: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q
   /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/rc/CapHermeticSelfTest310`, then
   `checkout -q --detach 41cc04c8` → `rev-parse HEAD` = `41cc04c8d593837a0d5078bffaacdaa163d12897`.
4. Re-ran the demonstration verbatim: `cd <clone> && timeout 600 prlimit --as=4000000000 bash
   tools/mado-verify.sh --selftest; echo exit=$?` (GIT_* unset).
5. Verified every cited SCORECARD line by direct read of the base blob, grepped all `selftest`/`MADO_SELFTEST`
   mentions, checked the file tail (lines 1597–1618) for missed supersession, hashed the gate blob, and read the
   pointer receipt `.ufo/evidence/round-12/gate-selftest-after.txt` at `41cc04c8`.

## Independent re-run output (verbatim, complete)

```
MADO_SELFTEST: 460/460 assertions passed
exit=0
```

Wall time ≈ 18 s (bash tool reported 18.05 s). `git status --porcelain` after the run: 0 lines — the tree is
clean, consistent with isolated fixtures and with the report's claim.

## Point-by-point comparison

- **Observed status / exit code:** match exactly — `460/460`, exit 0. The 269/269 figure in the row is stale as
  claimed; the suite has grown to 460.
- **Command form:** the report ran the row's literal command `bash tools/mado-verify.sh --selftest` with
  timeout/prlimit; I ran the identical form. Match.
- **Key output:** match, byte-for-byte on the summary line.
- **Right revision:** its reported HEAD `41cc04c8d59…` is the full hash of the assigned base; my clone detached
  to the same. No wrong-revision evidence.
- **Copied-not-run:** none detected. Output format, exit, clean tree and plausible wall time all reproduced in my
  own run; nothing reads as transcript copying. The claim that gate bytes at `41cc04c8` are
  `sha256:050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1`, 4,194 lines, is **verified**: I hashed
  `git show 41cc04c8:tools/mado-verify.sh` → same sha256, `wc -l` → 4194 — so its "460/460 reproduces the
  round-19-pinned gate" inference is grounded.
- **Pointer receipt:** `git show 41cc04c8:.ufo/evidence/round-12/gate-selftest-after.txt` is exactly the two lines
  `MADO_SELFTEST: 269/269 assertions passed` / `exit=0` — as reported; headerless, as reported.
- **Superseding pointers:** all verified at the cited line numbers in the base blob: 529 (`372/372`, round 13),
  1005 (`372 → 389/389`, round 18), 1136 (`389 → 443/443`, round 19), 1192 (`452/452`, round-19 addendum),
  1221–1225 (gate `050efc72…`, 4,194 L, `selftest 460/460`, round-19 addendum), 1400 (round-20 attempt-2 harm watch
  `460/460` at `a8960de`), 1577 (round-24 capability-status `works`, `N/N … exit 0 at 8e5d9369`). Line 1570's own
  text confirms the table "supersedes the implied `works` of every earlier row". Attribution of 1221/1400 as
  round-19-addendum/round-20 is correct per section headings (lines 1198, 1380).
- **Ledger line:** `works — exit 0, MADO_SELFTEST: 460/460 assertions passed` with the two superseding pointers
  is accurate and honestly framed (numeric staleness disclosed, capability wording not overclaimed).

## Findings

1. **Missed superseding text (low severity).** The report asserts "Contradiction: none … the grep for failure
   wording returns only historical round-1..11 rows and unrelated notes". That scan missed **SCORECARD.md:1179–1181**
   at `41cc04c8` (round-19 addendum): "Gate selftest showed two non-reproducible fixture-loss failures under
   concurrent seat runs (ScribeScorecardCheck, MutGateR19); every isolated run reads 443/443 → cause `[UNK]`."
   This is a later-row record of the same command failing under concurrency — directly relevant to the "isolated
   fixtures"/hermeticity claim the row makes. It does not overturn `works` (isolated runs still pass, including
   mine), and arguably is a caveat rather than a contradiction, but it is precisely the kind of text a falsifying
   supersession scan should surface; the "none" claim is overbroad.
2. **Minor imprecision (cosmetic).** The report says "a later round (line 557) records that such headerless
   selftest receipts fail its provenance audit". Line 557 actually demonstrates the audit failing on the
   *round-13* receipt specifically (exits 1, missing `measured_commit`/`gate_sha256`); generalizing it to the
   headerless round-12 file is the report's own inference. Directionally correct — the round-12 receipt is
   headerless and would fail the same audit — but the sentence elides that the audit was run on r13, not r12.
   The report does hedge it as "only of the receipt's provenance completeness", so no material misclaim.
3. **No other defects.** No copied-not-run evidence, correct revision, no overclaim in the ledger line, all cited
   line numbers resolve to what the report says they contain, clone cleanup and host-safety claims are consistent
   with what I could verify (no leftover process, clone deleted as stated).

## Verdict

RECHECK CapHermeticSelfTest310: agree — ledger line verified end-to-end (independent run reproduced 460/460, exit 0, clean tree at 41cc04c8; all seven superseding pointers and the gate sha confirmed); one missed caveat, not an error: SCORECARD.md:1179–1181 records two non-reproducible gate-selftest fixture-loss failures under concurrent seat runs, which the report's "contradiction: none" scan should have surfaced against the hermeticity claim.

## Host-safety / bounds

- Sandbox clone deleted: `rm -rf /fast/scratch/hyaku/mado-r25a3/rc/CapHermeticSelfTest310` → exit 0; `ls` confirms
  only pre-existing sibling artifacts remain. My `scorecard-41cc04c8.md` dump remains in `rc/` as scratch data.
- No git/jj writes in the lane or fleet repo; only the report file above was written in the lane.
- `timeout 600` and `prlimit --as=4000000000` applied to the self-test; no nested compositor, no hyprctl, no
  package/service/config changes, no tool installs, no processes left behind.
