# ReviewRc — review of w1 Rc1409 / Rc1410 against the SCORECARD ledger rows `:1409`/`:1410` and errata F5

Reviewer seat `MadoR26.ReviewRc` (round-26 wave w2, leaf — no subagents). Object: the two w1 second-derivation
reports, `.ufo/waves/round-26/w1/reports/Rc1409.md` and `Rc1410.md`, against the round-25 ledger section
`## Current state (round 25)` (rows `:1409` at `SCORECARD.md:1662`, `:1410` at `:1663`), errata F5
(`SCORECARD.md:1711-1712`), and the round-24 manifest guard definition.

## Verdict

**Both are true second derivations, and they agree. `VERDICT: agree` for Rc1409 and Rc1410; the two rows'
ledger cells stand as written, with F5's scoping load-bearing for `:1410`.**

The reports are not copies of each other or of the a3w1 runs: cross-seat semantic equality with timing-only
variance (below). A third run by this reviewer (fresh clone, row's own command) reproduces both seats' base
receipts semantically, with timing-only differences.

## 1. True second derivation: provenance (verified)

- **Rc1409 clone is a fresh clone at 41cc04c8.** Kept for audit at `/fast/scratch/hyaku/mado-r26/rc/Rc1409`:
  origin = the lane (`git remote get-url origin` →
  `/home/vgpnk/Projects/shokunin/mado-shokunin`); reflog `HEAD@{1}: clone: from /home/vgpnk/Projects/shokunin/mado-shokunin`,
  `HEAD@{0}: checkout: moving from master to 41cc04c8`; `rev-parse HEAD` = `41cc04c8d593837a0d5078bffaacdaa163d12897`;
  `status --porcelain` = 0 lines. This is the clone event, not a pre-existing directory.
- **Rc1410's clone is gone as reported** (per its report: detached at 41cc04c8, deleted after runs); only its
  receipts remain under `/fast/scratch/hyaku/mado-r26/rc/`. This is consistent with the report, not a defect.
- **Counter bytes identical everywhere:** `.ufo/waves/round-20/a2/a2-guards.py` sha256
  `414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef` in the Rc1409 clone worktree, at
  `41cc04c8`, and at `6a7d9ca` (verified via `git show`), and in the lane.
- **Tool under test:** `41cc04c8:tools/mado-tripwire.py` sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`
  (= `8e5d9369` tool bytes, also verified); `a8960de:tools/mado-tripwire.py` sha256 `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458`.
  Fixture pin `6a7d9ca` resolves (`git cat-file -t` → commit).
- **Receipts exist and match the quoted hashes/bytes:** `/tmp/Rc1409-run1.json` b9ee060a… (3356 B),
  run2 a49f3628… (3359 B), run3-a8960de ea9920b4… (2955 B), isolate.out a07a5e6f… — all match the report
  verbatim; `Rc1410-base-41cc04c8.json` 7fa74625… (3358 B), `Rc1410-before-28c6837.json` (11217 B),
  `Rc1410-after-a8960de.json` (2952 B), all stderr files 0 B.
- **w1-spec.json confirms the assignment**: entries `Rc1409` and `Rc1410` carry exactly the routed defect-7
  second-derivation prompts, with the exact sandbox clone commands and the exact counter commands.

## 2. The row's own command

- `:1409` row (`SCORECARD.md:1662`) command cell: `python3 .ufo/waves/round-20/a2/a2-guards.py 41cc04c8
  --fixtures-rev 6a7d9ca` (present tool) and `… a8960de …` (row's revision). Rc1409 ran both forms twice /
  once, from the clone root.
- `:1410` row (`SCORECARD.md:1663`) command cell: `python3 -I .ufo/waves/round-20/a2/a2-guards.py 41cc04c8
  --fixtures-rev 6a7d9ca`. Rc1410 ran exactly that (plus the cell's before clause `28c6837`, and the row's
  evidence pointer `a8960de`).
- Receipt `rev` / `fixtures_rev` fields confirm the arguments actually used
  (`41cc04c8d593…` / `6a7d9ca0d212…`).

## 3. Agreement (all verified first-hand by this reviewer)

- **Base runs (41cc04c8):** all six guarded counters are 0 across every fresh run — Rc1409 run1, run2,
  Rc1410 base, and my own third run (below): `recall_lost 0`, `crash_flip 0`, `pure_rows 0`, `vcs_fn 0`,
  `a2_mismatch 0`, `dup_rows 0`; `rev_exit2 3`, `timeouts []`, populations `a2 9 / crash 172 / pure 24 /
  recall 81 / vcs 74`, `tool_sha256.rev cd9da20c…`, `vcs_fp 26`.
- **Cross-seat semantic equality:** Rc1409 run1 differs from Rc1410 base only in the timing keys
  (`a2_seconds`, `slowest`); Rc1409 run1 vs run2 differ only in timing (matching its determinism claim).
  Rc1409's a8960de run and Rc1410's a8960de run differ only in timing, both with `crash_flip 1`,
  `vcs_fp 20`, `rev_exit2 4`, `recall_lost 0`.
- **The `a8960de` MemoryError caveat:** isolated probe output is byte-identical across three independent probes
  (Rc1409's `/tmp/Rc1409-isolate.out`, Rc1410's `probe/out-tw-a8960de.py.txt`, and my rerun):
  `MADO_TRIPWIRE: could_not_evaluate` + `{"exit": 2, "error": "internal MemoryError", …}` under
  `prlimit --as=4000000000`; base tool on the same fixture: `MADO_TRIPWIRE: clean`, exit 0. Matches a3w1's
  measured mechanism (Cap1409: MemoryError at 4 GB and 8 GB, unbounded killed; Cap1410: tested at 4/8/12 GB).
- **The `28c6837` before-leg (`:1410`):** Rc1410's before receipt equals the committed
  `guards-before-28c6837.txt` field-for-field on every counter, file list, and population — only `a2_seconds`/
  `slowest` differ (I re-parsed both and diffed every key): `recall_lost 52`, `crash_flip 13`, `pure_rows 24`,
  `vcs_fn 0`, `vcs_fp 31`, `a2_mismatch 6`, `dup_rows 0`, `rev_exit2 24`, tool sha `9613f510…`. The cell's
  "before receipt `28c6837` reproduces `recall_lost 52`" holds, and the registration before-column values
  (`:1392`) are confirmed.
- **The `a8960de` after-leg:** Rc1410's after receipt vs committed `guards-after-a8960de….txt` diverges exactly
  on the cap-sensitive keys (`crash_flip 1` vs 0, `crash_flip_files`, `rev_exit2 4` vs 3) plus timing —
  everything else equal, exactly as the report states. The committed after receipt's argv carries no `prlimit`
  (headers verified), so the divergence is the contract's address-space cap, not drift.
- **Base rows at 41cc04c8** (`:1409`, `:1410`, `:1584`, `:1585`) verified via `git show` — match both reports'
  quotes verbatim.
- **F5 (`:1410`):** the round-24 manifest guard (`capabilities[10]`) regexes only `recall_lost`, `crash_flip`,
  `vcs_fn`, `a2_mismatch`, `dup_rows`, `pure_rows` (all 0) plus `rev`, and its `why` states `vcs_fp` is "outside
  this removal-side claim and is not asserted". `vcs_fp 26` is therefore genuinely outside the guard; the cell's
  "all guarded counters 0" is correct under F5's scoping, and the errata F5 text (`SCORECARD.md:1711-1712`)
  matches Rc1410's quote. Rc1409's cell does not assert the guarded-zero phrase and correctly does not treat
  `vcs_fp 26` as a disagreement.

## 4. Findings by severity

**Minor (documentation, no substantive impact):**

1. **Rc1409 mis-cites the reviewer judgment path.** It cites
   `.ufo/waves/round-25/a3w1/reports/RevC2Judgment.md:86`; that file does not exist — the judgment lives at
   `.ufo/waves/round-25/a3res/reports/RevC2Judgment.md` (F1 there: "false for **3 of 15 rows**: `:311`,
   `:1409`, `:1410` … Those three rows have only their a3w1 Cap runs", lines 81-89; the quoted words "one run
   each (a3w1 only)" are a paraphrase, not a verbatim :86 line). Substance is correct; the path/line are wrong.
2. **Rc1409 attributes F5 to "the spot-check".** The spot-check lesson
   (`corpus/lessons/round-25-verifier-spotcheck.md`) mentions F5 only once (line 120: "Errata F1–F5 all
   verified") and never states F5's content; the content is the SCORECARD errata (`:1711-1712`). Rc1409's
   sentence "the spot-check's F5 shorthand note about 'all guarded counters 0' concerns `:1410`" is substance-
   correct, loosely attributed.

No disagreement with any ledger cell, guarded counter, exit status, revision, or before/after clause in either
report; no contradiction between the two reports.

## 5. Reviewer's own third run (ground-truth check)

Fresh clone at `/fast/scratch/hyaku/mado-r26/rc/ReviewRc-clone` (origin = lane, detached at
`41cc04c8d593837a0d5078bffaacdaa163d12897`, clean, 0 porcelain lines after runs; `TMPDIR` pointed at scratch).
Ran the `:1410` row's command (the stricter `-I` form, which also covers the `:1409` present-tool clause):

```sh
cd /fast/scratch/hyaku/mado-r26/rc/ReviewRc-clone
timeout 900 prlimit --as=4000000000 -- python3 -I .ufo/waves/round-20/a2/a2-guards.py 41cc04c8 --fixtures-rev 6a7d9ca
```

`exit=0`, wall 97.5 s, stdout 3358 B (receipt `ReviewRc-base.json`). Key counters: `recall_lost 0`,
`crash_flip 0`, `pure_rows 0`, `vcs_fn 0`, `a2_mismatch 0`, `dup_rows 0`, `vcs_fp 26`, `rev_exit2 3`,
`timeouts []`, `rev 41cc04c8…`. Diffed against Rc1409 run1/run2 and Rc1410 base: **differing keys =
`a2_seconds`, `slowest` only** (timing-only). Also reran the `a8960de` MemoryError probe (extracted from
`a8960de:tools/mado-tripwire.py` and `6a7d9ca:…/huge_many_stmts.jsonl`): exit 2, verbatim
`internal MemoryError` verdict as above.

## 6. Residual risk and verification gaps

- No rerun of the `28c6837` before-leg by me (11 KB, ~98 s); Rc1410's receipt was field-verified against the
  committed evidence, and the a3w1 run reproduced it too. Coverage: three independent runs of that revision
  (a3w1, Rc1410, committed receipt).
- The `a8960de` after-leg cannot be replayed under the mandated 4 GB cap (MemoryError by construction); only the
  within-cap counters and the receipt bytes are verifiable — same limitation the reports state.
- Host was shared (load ~17-29 on 32 CPUs at  times); wall times vary, all non-timing values agree across every
  run. `huge_bash_cmd.jsonl` took 87-109 s across runs, under the counter's 120 s per-fixture timeout.
- The rows' wording ("every visible body" / "count findings dropped") is measured only over the frozen
  populations; both reports note this, matching a3w1's disposition caveat `:1412-1420` / `:1458`.

## 7. Safety, cleanup, installs

- No git/jj writes in the lane or fleet repo; all clone work under `/fast/scratch/hyaku/mado-r26/rc/` with
  `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset. No network, compositor, `/dev/dri`, or host service; no
  tool installed or upgraded; no package changes.
- Reviewer's clone and scratch kept for audit at
  `/fast/scratch/hyaku/mado-r26/rc/ReviewRc-clone` and `…/ReviewRc-tmp/` (`ReviewRc-base.json`, probe outputs,
  extracted tool/fixture copies). No process started by this item remains.
- Transient: during this review one `mkdir -p` accidentally targeted `/home/vgpnk/Projects/shokunin/.ufo/waves/round-26/w2/reports/`
  (fleet root) instead of the lane; the empty stray dirs were removed (`rmdir` on `reports`, `w2`, `round-26`;
  the fleet `.ufo/waves/` listing confirms no `round-26` remnant). The lane `w2/reports/` was then created and
  holds this report.

## 8. Draft one-line append for the SCORECARD round-26 section

Matching the round results-table shape (`| Claim / axis | Before → after | Counting command | Author verdict |`):

```text
| C2 ledger defect 7 closed: rows :1409/:1410 each second-derived (w1 Rc1409/Rc1410; fresh sandbox clones at base 41cc04c8; each row's own command, two runs each) | one run each → independent runs agree, timing-only variance; :1410's 28c6837 before-leg reproduces guards-before-28c6837.txt field-for-field | `timeout 900 prlimit --as=4000000000 -- python3 [-I] .ufo/waves/round-20/a2/a2-guards.py 41cc04c8 --fixtures-rev 6a7d9ca` (receipts .ufo/waves/round-26/w1/reports/Rc1409.md, Rc1410.md) | agree — rows stand; F5 scoping confirmed (vcs_fp 26 outside the guard); defect 7 closed |
```
