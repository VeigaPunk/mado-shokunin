# w2/MutC2OneByte — same-size quote/anchor mutations against frozen PRED-C2-r48

Seat: `MutC2OneByte` (leaf). Wave: round 48 `w2` = FALSIFY, registration v1, base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`, freeze `3e6c848a`.
Target: `PRED-C2-r48` = `quality/counters/c2-r48-xkb-entry.py`,
sha256 `4a0e6924eada0d12c70b4ce6e681a118896b93532e280ea3c15cc148b794a9f1`.
Read first, unchanged: `.ufo/waves/round-48/claims.md`, `.ufo/waves/round-48/registration.md`.
Nothing outside `w2/MutC2OneByte/` and this file was written; the counter, fixtures, pins,
claims, entry bytes and registry were never edited.

## Result in one line

15 mutations scored on the frozen instrument: **6 detected, 9 admitted** (M0 overlay control
admitted with `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1`). Every admitted mutant keeps
the frozen clauses literally true; none is a counter bug. They mark where the predicate is
*silent*, not where it is broken — the frozen predicate was not retuned, narrowed or
re-registered by this seat.

## Method (replay tree, no lane writes)

Sanctioned recipe is `l1-draft/c2-mirror.sh` (clone lane at base, overlay draft entry, rows
S340-S350, README row, fetch pins, live receipt, generator). The recipe's worktree checkout
cannot run under this seat's 1 MiB per-file writer bound:

```
$ git clone -q --shared <lane> $S/m/clone && git -C $S/m/clone checkout -q 579f694b
fatal: sha1 file '.../.git/index.lock' write error: File too large
```

(the lane's tracked blobs and its index exceed 1 MiB), so the replay tree is built with git
plumbing only: `hash-object -w` for each overlay blob, `mktree` tree surgery on the base tree,
`commit-tree` per revision. No worktree is ever populated (`scratch-bound.txt`: clone worktree
listing empty). Equivalence check: `receipts/overlay-diff.txt` shows exactly the recipe's
landings — 14 fetch pins, the receipt, the generator, the entry (A), `corpus/README.md` and
`corpus/SOURCES.md` (M), 19 paths, no others — and the M0 overlay is admitted by all eleven
clauses including the live replay.

Per-rev scoring command (frozen counter, unmodified, `TMPDIR` inside seat scratch):

```
cd <seat clone> && TMPDIR=/fast/scratch/hyaku/mado-r48/MutC2OneByte/replay \
  python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r48-xkb-entry.py \
  --repo <seat clone> --rev <rev>
```

xkbcli 1.13.2 present; clause r live replay ran for every scored revision
(`clause=r replay=ok sha=efd487a39920 neg=(1,1,0)`), so the sandboxed-compiler portion of the
predicate was exercised, not skipped. Overflow detail: 9 of 15 mutants are byte-identical in
size to the overlay (delta 0); the rest are −11…−419 bytes. Matrix:
`w2/MutC2OneByte/receipts/mutant-matrix.tsv`.

## Scoreboard

| mutant | attack | size | verdict | clause evidence |
|---|---|---|---|---|
| M0_base_overlay | draft overlay control | – | **ADMITTED** | all a–r = 1 |
| M1a_quote_wrong_line | quote true in pin, locator moved 1297→1298 | 0 B | **detected** | `clause=d quote_out_of_range line=48 ... at=[1297] range=1298-1298` |
| M1b_quote_true_unsupported | quote → `LogIncludePaths(ctx);` at include.c:353-358, claim unchanged | −22 B | **admitted** | `clause=d quotes=1`; quote verbatim in range, supports nothing |
| M1c_quote_other_pin | quote from `symbols/br` placed at context.c:317 | −46 B | **detected** | `clause=d quote_not_in_pin line=55 pin=xkbcommon-context.c` |
| M2a_locator_unbound_shift | step-2 locator 520-527 → 500-507 (in range, wrong lines) | 0 B | **admitted** | clauses c/d/e silent |
| M2b_locator_dup_shift | OBS locator 530 → 457 (same bytes occur at both) | 0 B | **admitted** | `clause=d quotes=18`, passes at 457 |
| M2c_locator_no_occurrence | OBS locator 501 → 505 (quote absent there) | 0 B | **detected** | `clause=d quote_out_of_range line=54 ... at=[501] range=505-505` |
| M2d_registry_locator_shift | row S340 anchor 520-527 → 500-507 | 0 B | **admitted** | `clause=c id=S340 ... ranges=11` unchanged |
| M3a_receipt_diag_id_swap | receipt: whole layout block XKB-338→XKB-661 and variant XKB-661→XKB-338, rc kept | 0 B | **admitted** | `clause=f`/`clause=r replay=ok` |
| M3b_receipt_rc_change | layout probe rc 1→0, diagnostics kept | 0 B | **detected** | `clause=f receipt_probe_bad=unknown layout(rc_values=[0])` |
| M3c_receipt_probe_name_swap | `--variant nope` block's error text → `'br(caps)'`, rc kept | 0 B | **admitted** | `clause=f`/`clause=r replay=ok` |
| M3d_receipt_diag_text_swap | `Abandoning symbols file "(unnamed map)"` → `"pc"`, rc kept | −11 B | **admitted** | `clause=f`/`clause=r replay=ok` |
| M4a_remove_obs_statement | OBS S344 statement deleted, row S344 kept | −137 B | **admitted** | `clause=d quotes=17` (no floor); row S344 unchanged |
| M4b_remove_receipt_statement | entry row for `--options nope:nope` deleted, registry rows kept | −95 B | **detected** | `clause=f entry_disagrees ... neg=[True, True, False]` |
| M4c_remove_step9 | numbered step 9 deleted, registry rows kept | −419 B | **admitted** | `clause=e steps=8` (≥6) |
| M4d_remove_registry_row | row S344 deleted, entry statement kept | −895 B | **detected** | `clause=b` ghosts, then `c:0 d:0` |

## Detected vs. semantic gaps

**Quote text is bound only where the bytes are absent from the cited range (3/4 quote mutants
detected).** `clause_d` finds every occurrence of the normalised quote inside the pin and passes
when any occurrence line is inside `a..b` (`occurrences()` + `any(a <= x <= b)`). Moving the
locator off the only occurrence (M1a, M2c) or quoting another pin's bytes (M1c) is caught. It
cannot catch (M1b) a quote that is verbatim inside the cited range but no longer supports the
sentence: `` `LogIncludePaths(ctx);` at xkbcommon-include.c:353-358 `` sits at line 357, in range,
and the OBS still claims "the XKB-338 line shape, `symbols/zz` for an unknown layout". This is
the residual `w1/ExecCounterC2.md` already names ("a quote at a true locator can still sit beside
a claim it does not support"); it is now demonstrated at zero detection.

**Locator meaningfulness is unbound wherever no quote rides on it (3 admitted / 1 detected).**
- M2a: the step-2 citation `xkbcommon-rules.c:520-527` was replaced by `500-507` — inside
  `matcher_new_from_names` (lines 501-510), unrelated to the zero-padding branch. `clause_d`
  only bounds-checks locators without quotes (`a < 1 or b < a or b > nlines`); `clause_e` needs
  one valid range per numbered step and the step's other citation (528-535) still satisfies it.
- M2b: the same "Less layouts than variants" format string occurs at rules.c:457 and :530
  (`receipts/pin-occurrences.txt`). Moving the OBS locator 530→457 keeps a true quote at a true
  in-range line, but 457 is the `xkb_keymap_new_from_names` path, not "the truncation branch"
  that step 2 cites as 528-535. Duplicated upstream strings make the `any()` rule
  occurrence-permissive.
- M2d: the registry anchor is checked the same way (range within the pin only), so the row's
  located ranges can be shifted to uncited lines of the same file; `clause=c` reported
  `ranges=11` unchanged.
- M2c is the detected edge: the quote is bound and absent at 505.

**A receipt's negative diagnostics are not bound to the live compiler the counter itself runs
(3 admitted / 1 detected).** `clause_r` re-runs `xkbcli` and compares *live* output to the
receipt's positive keymap digest and to the constants `(1,1,0)`; it never compares the live
stderr/sextet to the receipt's recorded stderr, and `clause_f` reads only the receipt's rc
labels plus the presence of `XKB-595`/`Unrecognized RMLVO option` and the entry's own rc
statements. Consequently:
- M3a inverts the diagnostic classes the entry claims (338 for a missing symbols file, 661 for a
  missing map) across a whole probe block, rc untouched → admitted;
- M3c leaves the command line `--layout br --variant nope` but makes its error name `'br(caps)'`
  → admitted;
- M3d changes the payload of the XKB-769 line → admitted;
- M3b (rc 1→0) is the one binding that works, and it works only through `clause_f`'s rc parse —
  `clause_r` alone would not have caught it, because it compares live rc to constants rather
  than to the receipt.
A forged receipt body therefore passes with a true positive digest and true negative rc while the
negative diagnostics contradict both the live run and the entry's quoted step 7.

**Statement-level evidence is unbound from the registry (2 admitted / 2 detected).** `clause_b`
checks head `source:` ids, row shape and row→entry text (`cells[10]` names the entry); no clause
requires the entry to contain a statement for a row. So M4a leaves row S344 with its only
statement deleted (`clause=d quotes=18→17`, no quote floor) and M4c drops step 9 entirely
(`steps=8` passes while the "What the evidence licenses" table still points at step 9) — both
admitted. The detected edges are content that `clause_f` binds (M4b: removing the entry's
`nope:nope`/XKB-595/rc 0 statement fails `entry_disagrees`) and direction the ghost check covers
(M4d: removing the row while the entry cites S344 gives `ghost_ids`, then c/d cascade).

## Predicate status (no narrowing, no retune)

Every admitted mutant keeps the frozen clauses true as written: quotes remain verbatim at their
committed ranges; locators remain inside their pins; the receipt still carries version, positive
digest, `br` + `compose:caps`, three excluded-name probes with rc and entry-matching text;
registry rows remain pin-bound and ref-pinned; steps ≥6 with a pin locator; README/held/census
unchanged. So these are **predicate-silence findings, not breaks of PRED-C2-r48**, and this seat
does not classify them as `TARGET_MISSED` for the frozen predicate. They are recorded for the
L1's pre-data decision only: if the freeze's intent is that (i) each quote supports its claim,
(ii) non-quote locators point at their claim, (iii) the receipt's own negative diagnostics are
what the live replay just produced, and (iv) each registry row has at least one statement in the
entry, then the current eleven clauses do not enforce it — 9/15 of these same-size edits are
admitted. Under the narrower registration sentence that binds only the positive digest and the
negative rc ("A receipt whose positive digest changes under the replay or whose negative rc
differs is a miss"), M3a/M3c/M3d are inside the admitted envelope by design.

## Host safety, bounds, and cleanup

- Every writer shell began with `ulimit -f 2048` (512-byte units). Largest file written:
  `115635` B (`clone/.git/objects/…`, an overlay blob); scratch total `668187` B (« 2 GB);
  no file above 1 MiB; no `/tmp` use (`TMPDIR` = seat scratch `/replay`), no replay leftovers.
- `git clone --shared` only; every git call used `-C <scratch clone>` and asserted
  `rev-parse --show-toplevel` equals the clone; commit identity was `-c user.name=t
  -c user.email=t@t` inside the clone only. No lane Git/jj mutation, no commit/push.
- No pacman/package transaction or install (none needed); no compositor, service, input, GUI or
  terminal action; the only host binary executed was read-only `xkbcli` under the counter's own
  sandboxed replay.
- Scratch removed by `trap 'rm -rf -- "$S"' EXIT`; the receipts below were copied out first.

## Evidence map (`w2/MutC2OneByte/`)

- `build.py` — overlay + 15 mutation definitions; git-plumbing commit builder.
- `run.sh` — clone, build, score every rev, capture patches/numstat, scratch-bound report.
- `receipts/revs.txt` — base/overlay/mutant revision ids for the captured run (ephemeral clone;
  tree content is reproduced by `build.py`, commit ids are not stable across runs).
- `receipts/mutant-matrix.tsv` — attack, byte delta, verdict, clause evidence.
- `receipts/<mutant>.log` — full frozen-counter stdout for each rev (incl. `clauses=` line).
- `receipts/<mutant>.patch`, `receipts/<mutant>.numstat` — exact mutation against the overlay rev.
- `receipts/overlay-diff.txt`, `overlay-digests.txt` — overlay landings and SHA-256/bytes.
- `receipts/pin-occurrences.txt` — duplicate-string facts used by M1b/M2b/M2c.
- `receipts/scratch-bound.txt` — largest scratch files, scratch bytes, no worktree, no leftovers.

## Risks / limits of this seat's result

- Revs lived in a scratch clone that the wave rules require to be deleted; a later reader can
  rebuild the tree with `build.py` but cannot `git show` the captured revision ids.
- The nine admitted mutants were scored, not adversarially prose-verified: an admitted tree is
  evidence about the instrument, not a claim that a real entry of this shape would be believed by
  a reviewer. The forged receipt (M3a/M3c) is textually self-consistent enough to pass a skim.
- No subagent was dispatched; the single labrat allowance was not needed for a 5-second
  build/score loop.
