# RevLessonGate — audit of the drafted round-39 lesson, Gate + Mistakes rows

Scope: `.ufo/waves/round-39/w1/ScrLesson/round-39.md` (mtime 2026-10-25 16:13:55 — the file was
live-edited mid-review; findings reflect bytes at review close, GATE fence re-grepped at close).
Requirements checked: (G1) every new row records URL, access date, ≤25-word located quote;
(G2) rejections kept with reasons; (G3) every status/recheck/used-by change logged old→new;
(M1) each Mistakes row carries class · evidence pointer · captured-by · fix; (M2) every claimed
fix backed by a located red-before receipt/state. Lane read-only; no tools installed; only this
file written. HEAD audited: `457d1b125932…` (freeze == tip), base `08be4eb7fd13…`.

## Verdict

Gate: **PASS with one HIGH defect** — the `GATE S219` fence line (round-39.md:34) pins
`sha256=9787b53b…cf59`, which matches no byte set in the lane; the same file's Row-facts bullet
and spot-check row were already corrected to `cee78d99…9ce61e`, leaving the binding fence as the
one stale line. Mistakes: **PASS with one LOW arithmetic slip** (+133 vs actual +126) and a
red-before phrasing that needs one clause to be literally true. One MEDIUM: the Gate ledger's
recheck new-values for S219/S220 contradict the drafted SOURCES rows.

## Findings — HIGH

- **H1 — GATE S219 fence sha256 binds no existing bytes (fence contradicts its own spot-check row).**
  `sha256sum tools/mado-options.py` → `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`
  (37,358 B, mtime 16:10:55). The fence (round-39.md:34) still reads
  `receipt=tools/mado-options.py@data-tip sha256=9787b53b298216aee93ec1193814e2972d9fef9125656ce9ed0bd03ed7fbcf59`.
  The file is untracked (`?? tools/mado-options.py` in `git status --porcelain`) and in no ref
  (`git log --all -- tools/mado-options.py` empty), so `9787b53b…` matches neither worktree nor
  any committed bytes. The Row-facts bullet says "worktree sha256 at draft finalization
  `cee78d99…9ce61e`" and the spot-check row says `cee78d99…9ce61e` "the tool file changed after
  the first draft hash (`9787b53b…` → `cee78d99…`)" — trim-notes 3c's fix was applied to those
  two cells but not to the binding fence. Note the fix is load-bearing at data-tip time only:
  any further tool edit re-breaks the digest (ConnCrossClaim.md:79). Fix before the data commit:
  replace the fence sha with `git show <data-tip>:tools/mado-options.py | sha256sum` of the final
  bytes; never land the fence with `9787b53b…`.

## Findings — MEDIUM

- **M1 — Ledger recheck new-values contradict the drafted rows.** Lesson table: S219
  `recheck none → on-release`; drafted row (ScrSourcesRows/rows.md:14) says `on-change`. Lesson:
  S220 `recheck none → on-release`; drafted row (rows.md:15) says `on-compositor-release`. The
  lesson is the binding record; the rows are what check-index/census will see. Conform one to the
  other before landing (status `none → mined` and used-by cells do match the drafts).

## Findings — LOW

- **L1 — S220 alt-quote offset off by 16 bytes.** Spot-check row: "also present at raw offset
  262669". Actual first (and only) occurrence of "Dispatchers return tables that describe an
  action you want to make." is at raw offset **262685**; 262669 lands on the preceding
  `</h2><p>` (`bytes[262665:262690]` = `ection"></a></h2><p>Dispa`).
- **L2 — Mistakes row 1 fix-cell arithmetic + red-before phrasing.** `git show 457d1b1 --numstat`
  for the three reports: `53 0` RevEntryBound, `8 0` RevRegistry, `126 7` ScoutS253 — the fix
  cell's "+53/+8/+133, −7" should be "+53/+8/+126, −7" (133 = 126 additions + 7 deletions
  conflated; the +187/−7 total is right). Phrasing: "at base `08be4eb` the reports' final bytes
  were not in any commit (worktree-only)" is true only of the *modified* bytes — the reports
  themselves were committed at `5f9e6ed` (11:32:40, "round-38 wave-1 evidence") and are PRESENT
  at base (`git cat-file -e 08be4eb:<path>` → PRESENT ×3); `git diff 5f9e6ed 08be4eb -- <3 paths>`
  is empty (0 bytes), which is what actually proves the +187/−7 closure modifications were
  worktree-only at base. Suggest: "the closure modifications (+187/−7) existed only in the
  worktree at base".

## PASS items (evidence)

1. **S218 GATE line.** `sha256sum …/ExecAssimFetches/S218.bin` = `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801`
   (exact, 364,905 B — matches the row draft). Quote 16 words; NOT raw-verbatim (raw carries
   `<code>hl.config()</code>`), but rendered-verbatim verified (tag-strip + entity-unescape);
   rendered context places it immediately after the `hl.config({ category = { value = … } })`
   example under Syntax — matches the claimed §Syntax locator. Page revision stamp present in raw
   bytes: `<time datetime="2026-07-17T17:54:39.000Z">July 17, 2026</time>`. URL + opened
   2026-10-25 recorded.
2. **S220 GATE line.** `sha256sum …/S220.bin` = `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`
   (exact, 297,863 B). Quote 10 words, rendered-verbatim (inline `<code>` tags); `#dispatchers`
   and `id="dispatchers"` both in raw; stamp "July 15, 2026" present
   (`<time datetime="2026-07-15T23:56:15.000Z">`). Independent fetch copy
   `SctDispatchersPage/S220.bin` byte-identical (`cmp` exit 0), and equal to the held S196 fetch
   `.ufo/waves/round-32/fetch/S196.bin` byte-for-byte — the duplicate-URL consequence
   (W04 warning, census still exit 0) is now honestly recorded in the spot-check row.
3. **S219 quote and location.** "mado-options.py - static resolver of the config-tree option
   table." is verbatim at `tools/mado-options.py:2` in the current (`cee78d99…`) bytes, 9 words;
   own-work row, no URL per lane convention (cf. round-38 own-work S258), byte-pinned via the
   fence pending the data tip; opened 2026-10-25. Quote floor honored: 16/9/10 words, all ≤25,
   all located (§-anchor / `#dispatchers` / file:line).
4. **Rejections kept with reasons.** Four stay-refused rows, each with a concrete reason; wording
   matches round-38 lesson `:40-43` exactly (raw-pinned: lines 40-43 are the four `**refuse**`
   rows). "Re-opened and agreed by the round-38 verifier spot-check `:50`" — line 50 is exactly
   the Refusals bullet ("Re-opened: r29's … refusal agrees; r28's … consistent"). `S277 `:61`` —
   line 61 of `.ufo/waves/round-38/fetch/S277.bin` contains "Requests are capped at 64 KiB".
5. **Ledger old-values true; no unlogged changes.** HEAD == freeze `457d1b1`, the only commit
   since base; `git status --porcelain` shows no modified tracked files — corpus is untouched, so
   the seat drafts are the record. S018 row at HEAD (corpus/SOURCES.md:30) has used-by
   `corpus/knowledge/window-rule-effects-getprop.md` — the ledger's old value is exact, and the
   new `+ dispatcher-surface-and-request-grammar-r26.md` matches the amendment, which re-opens
   S018 (`:1149`, `:1151`, `:1131-1132`, `:1309-1310`, `:2096`). S218/S219/S220 absent from
   corpus/SOURCES.md (grep: no rows) — consistent with pre-data-commit drafting, `none → mined`
   is true. No other row's status/recheck/used-by changes anywhere in the round's outputs
   (the amendment cites S196 only as already-held corroboration — S196's used-by already includes
   the dispatcher entry, so no S196 ledger row is owed).
6. **Ledger used-by new-values match the drafts.** rows.md: S218/S219 used-by
   `config-option-table-r39.md` — and the drafted entry cites "source: S218, S219" plus OBS S218/
   S219 lines; S220 used-by the dispatcher entry — the amendment section cites S220 with URL +
   sha256 + fetch date.
7. **C1 spot-check receipts byte-verified.** `receipts/c1-redbefore.txt`: 19 control lines, sole
   `ok=0` at `c1-duprow` (`expected=TARGET_MISSED observed=TARGET_MET`), final line
   `MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED` — matches the
   lesson and registration §C1. `ExecC1After/after-freeze.txt` == `after-tip.txt` (`cmp` exit 0),
   1672 B each, final line `controls=19 correct=19/19 verdict=TARGET_MET`. Manifest
   `.ufo/waves/round-39/c1/manifest.json` sha256 `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`
   == `git show 08be4eb…:.ufo/waves/round-38/controls/manifest.json` (`cmp` exit 0). freeze ==
   tip (HEAD = `457d1b1`).
8. **Mistakes row 2 (Reporting / refuted addendum-5) — every pointer exact.** Fleet
   `9386c91f` 2026-10-25 11:26:06 "round-38: mado report addendum 5 — RevCensusBefore refinement";
   `RevCensusBefore.md:110` is exactly the refuted refinement bullet ("Frozen-instrument
   discrimination at the freeze rev … scores 19/19 …"). Captured-by: lane `c46f868` 11:35:43
   ("record dispute between RevFrozenClaims and RevCensusBefore … closure adjudicates") and
   `f551b70` 12:25:59 ("freeze-pair resolution (frozen counter x frozen manifest = 18/19;
   `859d0cf` verdict no-op)") — subjects and timestamps match; `859d0cf` exists. Fix: the round
   erratum (ScrErratum/erratum.md) names the superseded addendum-5 sentence and cites c46f868 +
   f551b70. Red-before receipt located: `receipts/c1-redbefore.txt` (18/19, sole failure
   `c1-duprow`) — content-verified above.
9. **Mistakes row 1 (Closure / inherited-dirty) — pointers exact.** Evidence: spotcheck `:17` is
   the DEFECT row ("3 modified seat reports … +187/−7"); registration §Routed-defects item 4
   names the same three files; fix: the three files are folded into freeze `457d1b1` (numstat
   verified; see L2 for the per-file figure slip). Red-before located via git (5f9e6ed→base diff
   empty; see L2).

## Informational (adjacent file, not the lesson)

- The amendment section (ScrDispatcherAmendment/…md, §1 parenthetical) swaps the two sentence
  word-counts: "Dispatchers return tables that describe an action you want to make." is 11 words
  and "Their purpose is to be fed into hl.bind() or hl.dispatch()." is 10 — the amendment says
  10 then 11. The lesson's own counts (10 for the S220 quote, 11 for the alternative) are correct.

## Residual risk and verification gaps

- The C1 checker was not executed by this seat (read-only review): receipt bytes match the
  quoted outputs, but the `exit 1`/`exit 0` claims rest on registration's recording, not a re-run.
- S219's binding cannot complete until the data commit lands; H1 must be closed at that moment
  (re-hash from `git show <data-tip>:tools/mado-options.py`), and any later tool edit re-breaks it.
- The lesson is a live draft (edited at 16:13:55, after the tool's 16:10:55 change); M1/L1/L2 are
  trivially fixable now, H1 requires the data tip.
- Ledger verified against seat drafts, not landed bytes (data commit pending); nothing in
  `corpus/` was touched this round at review time.
- No installs; no lane state, index, or sibling path touched; single file written: this report.
