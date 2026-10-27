# CritRoutedItems — routed-item re-check at base `03e4ae76aff7a4be59cb69970dd553baa319695a`

Seat: `CritRoutedItems` (critic, leaf). Round 49, wave w1 = BUILD. Base = the round-48 closure commit (the spot-check and
`claims.md` are tracked blobs there; every `git show 03e4ae76:<path>` below reads frozen bytes). Working-tree lane HEAD is
`5f37c1b87b3ce5e438d19284e32b2e46fd548a92` (L1 setup commit: `round-49: claims, w1 spec + dispatch, census before,
operator-owned state digest before`) — used only where noted. All commands were run read-only; scratch
`/fast/scratch/hyaku/mado-r49/CritRoutedItems` removed at close. Tools installed/upgraded: none.

Verdict up front: **every routed item is still open at base in the sense that no closing artifact exists yet**; what varies is
whether the defect is (a) a stale/committed-text erratum (N1, N2-name, N3, N4, N5, reg-1, reg-2), (b) an instrument gap that
survives into the frozen counter bytes (M48-8, SentScratch F1/F2/F6/F7), or (c) a behavioural rule whose proof is this wave's
dispatch (M48-10, M48-13, F3-F5). **The proposed fixes are well-routed** — `w1-spec.json` names a seat for each item (map in
§Route map) — with three real holes: F4's stale `/tmp` grant was re-shipped verbatim in the round-49 w1 context, the context's
cleanup trap still cannot remove a mode-000 tree (F6), and `ulimit` appears in exactly 1 of 45 item prompts (M48-5 pattern
repeating). Details per item.

## Route map (`.ufo/waves/round-49/w1-spec.json`, 45 items, context 12071 B)

| item | w1 seat(s) |
|---|---|
| N1, N2, N3, N5 | `ScrCorrections` (draft `corrections.md`, append-only lines with commands) |
| N4 | `ExecN4Matrix` (`c2v2-matrix-full.txt`, 98 rows from `summary.json`) |
| M48-8 | `ExecSessionTriage` (159 findings triaged, both scopes), `ExecSessionShapes` (gate v3 draft), `MutGate` (≥20 mutants + both-ways demo), `SentPrivacy` (this round's receipts) |
| M48-10 | `ExecMutantSandbox` (`hostguard.py`, fake-home demo), `MutCounterC1Draft` (HOME/XDG_* in scratch), L1 `receipts/operator-state-*.txt` |
| M48-13 | `ExecCloneRecipe` (cap-vs-recipe measurement + owed clause-r attack), `MutGate` (owed both-ways demo) |
| SentScratch F1/F2/F7 | folded into `ExecCounterC1`/`ExecCounterC2` drafts ("refuses a --work or TMPDIR under /tmp") |
| registration-v2 residuals | `RevRegResiduals` + `RevR48` (closure-missed defects) |
| 47 sidecars (L1 decision) | `CritSidecars`, `ExecSessionTriage` (waiver-row analysis) |

---

## N1 — untracked count 47, not 52

**Open at base.** Fleet report `.ufo/reports/round-48/mado.md:37` reads "the 52 untracked `*.synthetic` files". Re-measured
today: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain -uall` → 111 lines; filtering this wave's own
untracked outputs leaves 47, all `*.synthetic`, 45 under `.ufo/waves/round-45/w1/RevengerOmarchy/` and 2 under
`round-46/w1/` — the same census the closure took (`round-48-verifier-spotcheck.md:176-177`). The wrong number is in committed
report bytes and cannot be edited in place.

**Minimal honest fix.** One append-only correction line (ScrCorrections draft) carrying the command and the 45/2 split; the
round-49 report must print the counted number with its command, not a remembered one.

**Able to fail.** The command output is pasted, not asserted; a future reader re-runs
`git status --porcelain -uall | grep -c '\.synthetic$'` and can disagree. Nothing makes the line *able to be wrong without
being caught* — the residual risk is only that w1's live seat outputs keep the total moving (the fix must name the
`*.synthetic`-filtered count, not the raw 111).

## N2 — `host_cache_untouched_sha256` records the mutant's bytes

**Open at base.** `.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:4` and `:36`
(`host_cache_after_sha256`) both carry `c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144`; re-derived here:
`printf 'r48-w2\n' | sha256sum` → the same digest. So both fields record the w2 M-WRITE mutant's 7 bytes, and "untouched"
names the wrong thing. Today's operator state is 190 B, sha `ddd94f6b…` (`round-49/receipts/operator-state-before.txt:3`,
committed at `5f37c1b8` — the "before" half of the operator-owned pair the closure asked for).

**Minimal honest fix.** The ScrCorrections lesson line naming what the digest is — and it should say explicitly that *equal
before/after digests were computed over mutated bytes*: the receipt does show the field is consistent, but the two identical
values are `sha256("r48-w2\n")`, not the operator file's own bytes. The "after" operator digest lands at wave close
(`operator-state-after.txt`, same format as `:3`).

**Able to fail.** A reviewer who greps the digest against `printf 'r48-w2\n' | sha256sum` reproduces the identity in one
command; the fix fails only if it omits that derivation. Caveat to feed back: `host_cache_untouched_sha256` is a *field-name*
lie, not just a prose slip — any future receipt writer that digests operator-owned state should label it `operator_owned`
plus `observed_at`, which is what `operator-state-before.txt` now does.

## N3 — "five gate decisions" at `corpus/lessons/round-48.md:425`

**Open at base.** `git show 03e4ae76:corpus/lessons/round-48.md | sed -n 425p` → "**Discernment spot-check** of the five gate
decisions above (three admits, two rejects)". The `## Gate` section actually holds **12 admit lines + 3 REJECT lines**
(`S340`-`S351` admits in the fenced block at `:48-60`; the three REJECT bullets in `### Rejected after opening` at `:71-75`).
The stale sentence sits inside the lesson's own pending-spot-check checklist (item 4 of the shape the closure was asked to
follow), so it misdescribed the closure's sample size too (the closure sampled 6 of 15, §4).

**Minimal honest fix.** One append-only correction line: "the fifteen gate decisions (twelve admits, three rejects)", located
`corpus/lessons/round-48.md:425`, command `grep -c 'admit, tier'` / the two count greps. Nothing else to repair — the error is
the pending-checklist text, not the Gate itself.

**Able to fail.** The counts are one `grep -oE` away from refutation; a correction that asserts without its command would
repeat the defect class (M48-11 pattern: transcribed, not instrument-emitted).

## N4 — text matrix drops 2 of 98 variant rows

**Open at base, re-derived.** `git show 03e4ae76:.ufo/waves/round-48/receipts/v2/c2v2-revc2counter-matrix.txt` ends with
`variants 98` but carries exactly **96 result rows**; `c2v2-revc2counter-summary.json` lists 98 variant names; set-difference
computed here: missing = `a-entry-at-base`, `a-rev-base-direct` — neither name appears anywhere in the text file. The two
omitted rows are precisely the *positive* base controls, so the text receipt's failure pattern is not cosmetic: a reader
auditing only the `.txt` sees 96 mutation rows and cannot see that the two admission checks ran.

**Minimal honest fix.** ExecN4Matrix's plan is right: emit `.ufo/waves/round-49/w1/ExecN4Matrix/c2v2-matrix-full.txt` — one
row per summary.json variant (98), same line shape, values from the JSON — plus a checker asserting row-count 98 and set
equality. Frozen receipt bytes stay untouched.

**Able to fail.** The checker is the failing surface: `wc -l` ≠ 98 or a set diff ≠ empty is a miss. Residual to name in the
fix: *why* the generator dropped the two `a-*` rows (likely written to a different stream/section — ExecN4Matrix is told to
"report why"); if the generator is reused for the round-49 matrix, the drop will recur, so the fix should either patch the
harness (`l1-draft/v2/c2v2-harness-revc2counter.py`) or add a completeness clause to this round's counter draft.

## N5 — GitLab `-/raw/` anti-bot vs files API

**Open at base.** Rows S346/S347 (`corpus/SOURCES.md:295-296`) keep their `gitlab.freedesktop.org/…/-/raw/…` anchor URLs;
the API-fallback knowledge exists only inside the spot-check's own S347 cell
(`round-48-verifier-spotcheck.md:127`, `:188`). `git grep api/v4 03e4ae76 -- corpus/` hits only that lesson — i.e. the next
freshness re-fetcher working from `SOURCES.md` alone has no committed fallback note.

**Minimal honest fix.** Append-only note (ScrCorrections): for any `gitlab.freedesktop.org` row, fetch
`/api/v4/projects/<id>/repository/files/<url-encoded-path>/raw?ref=<tag>` when `-/raw/` serves HTML; prove by re-fetching both
S346 `rules/rules.in` and S347 `symbols/br` through the API and pasting digests equal to the row digests
(`8cf65550e08b5984…` for S347). Do not edit the frozen rows.

**Able to fail.** The pasted `sha256sum` of the API response vs the row digest is the check — a note without equal digests
has not demonstrated the fallback. Residual: this affects every GitLab-hosted row (S046-S052, S299, S328, S329, S346, S347
…), not just S346/S347 — the note should say so, or the next re-fetcher will rediscover it row by row.

## M48-8 — session-material gate coverage + red at base

**Open at base, re-measured.** `python3 quality/check-session-material.py --repo . --rev 03e4ae76` (read-only, object DB
only) → `SESSION_MATERIAL: files=22012 findings=159 rev=03e4ae76`, exit 1 — matches the committed tip receipt
(`a4/session-material-tip.txt`, `findings=159`). Coverage gap intact: the gate's scope argument still defaults to `.ufo/`
(`check-session-material.py` docstring: "`--scope ufo` (default: `.ufo/` only, the historical behaviour)"), and SentPrivacy's
19-shape measurement stands — `w1/SentPrivacy.md` §0: "misses 16 of 19", with the class table (PR-01..PR-16, PR-19 MISSED;
PR-17/PR-18/ss+monitor CAUGHT) and the discriminating-line analysis in §3 (flat `ls -LRl` headers, `path:line` prefixed
content, `$HOME`-masked output, owner/group account names, 16 MiB read cap, `.ufo/`-only scan).

**Minimal honest fix.** Three pieces, all routed: (1) ExecSessionTriage dispositions the 159 committed findings
(synthetic/real/false-positive + waiver rows vs removal) — without this, a widened gate just prints a bigger red number;
(2) ExecSessionShapes' v3 adds the 16-shape detectors and moves the default scope to the whole tree **with** the v2 selftests
kept and one red+one green case per new rule; (3) MutGate's both-ways demo (red fixture → findings, marked → waived, exit
flips) is exactly the "able to fail" proof M48-13's residue also owes.

**Able to fail.** v3 must run `--selftest` per rule-mutation and show each new rule red on its own fixture (ExecSessionShapes
is already told this). The honest-failure modes to watch: a v3 that flags `$HOME`-masked output *and* prose-quoted paths will
turn the lane's own masking practice into findings (SentPrivacy §3 warns the gate currently *rewards* the mask it can't
verify); and "scope=all" re-scans 22k files — the run above took ~3 s, so cost is not a blocker.

## M48-10 — mutants writing operator home state

**Open at base.** The mechanism is still in committed bytes: `w2/MutC1ReadOnly/mkmutants.py` `WRITE` mutant derives
`_tgt` from `os.environ.get("XDG_CACHE_HOME")` and `os.environ.get("HOME")` plus `/tmp/r48-w2-probe` and a CWD-relative
`r48-w2-probe` — i.e. run outside the sandbox it writes the operator's real `~/.cache/xdg-terminal-exec`, `/tmp`, and the
caller cwd. Nothing in the frozen counters prevents a *seat* (not the counter) from running a mutant unsandboxed, which is
what happened at 22:26:35.

**Proposed fix and its state.** (a) `receipts/operator-state-before.txt` (committed at `5f37c1b8`) digests
`~/.cache/xdg-terminal-exec`, three `~/.config/hypr/` files and the `~/.local/bin` entry count — the before half exists; the
after half is owed at wave close. (b) `ExecMutantSandbox/hostguard.py`: env-redirect + before/after digest guard, exit 3 on
drift, demonstrated only on a fake home — the right shape. (c) `MutCounterC1Draft` and `ExecCloneRecipe` both carry
"HOME/XDG_* in scratch" in their prompts.
**Able to fail.** The fake-home demonstration (caught when unsandboxed, contained when sandboxed) is the falsifiable check.
The guard is only as broad as its declared path list: an undeclared operator path such as `~/.config/xdg-terminals.list`
is invisible. `XDG_RUNTIME_DIR` is absent from the described redirect set; a mutant writing there would evade it. Include
every touched operator path in the digest list and redirect `XDG_RUNTIME_DIR` to scratch (or a bwrap tmpfs).

## M48-13 — 1 MiB cap vs clone recipe; owed attacks

**Open at base.** `a4r1-dispatch.json` carried `ulimit` ×9 / `clone` ×11; `a4r1-results.json` records the kills verbatim:
`RLIMIT_FSIZE=1 MiB rejects numerous committed large files` (MadoA4RevC1Write), `Index lock >1MiB` (MadoA4RevC2v2Diff), plus
`checkout could not complete`. Lesson `:467-469` confirms the residue: the clause-r mutant attack and the gate both-ways
demonstration never ran.

**Proposed fix and its state.** The round-49 context raises the cap to `ulimit -f 65536` (64 MiB — correctly noted as
"> largest tracked file 4.2 MB", which fixes M48-13's root cause since a `--shared` clone only *writes* the index +
worktree, not pack bytes). ExecCloneRecipe is told to measure which recipes survive 1 MiB vs 64 MiB and to run the owed
clause-r mutant attack with sandboxed HOME; MutGate owns the both-ways demo.

**Able to fail.** The recipe table must record the *failing file* per recipe (index vs first big blob) — that is what makes
the choice of cap falsifiable rather than folklore. Watch: `git clone --shared` writes objects only via alternates, so the
64 MiB cap's real constraint is the worktree/index, not packs; a recipe claim that doesn't record which file hit the cap has
not demonstrated the boundary. **Measured unit defect in the spec text (this seat, 2026-10-27):** on this host's bash,
`ulimit -f` counts in **KiB**: `ulimit -f 1024` stopped a write at exactly 1 048 576 B and failed a 1.5 MB write, so
`ulimit -f 2048` is a **2 MiB** cap — the round-48 texts (a4r1 dispatch, SentScratch, this wave's item prompt) all call it
\"1 MiB\"; the seats' observed walls (`Index lock >1MiB`, large blobs) are consistent with the real 2 MiB ceiling, so the unit
error is cosmetic for the conclusion (clones still fail at both caps) but the recipe table should label the measured cap,
and any future `ulimit` wording should state the shell and unit it measured. `ulimit -f 65536` = 64 MiB as the context says.

## SentScratch F1-F7 — status at base and in the new dispatch

**F1 (c2 TMPDIR presence-only) — open in frozen bytes, routed.** `c2-r48-xkb-entry-v2.py:826-828` still requires only
`os.environ.get("TMPDIR")` before `mkdtemp(dir=TMPDIR)` — presence gate, no containment. Fix is correctly routed to the
*new* counter: ExecCounterC2's prompt requires "Refuse /tmp TMPDIR". The frozen v2 keeps the defect (immutability is the
point); the honest fix is the round-49 counter plus a lesson line that F1 stands unrepaired in the frozen instrument.

**F2 (c1 `--work` admits tmpfs family) — open in frozen bytes, routed.** `c1-r48-terminal-cache-v2.py` main(): `--work`
required, `isdir`, `under()`-rejects {repo, lane, fleet parent, /run, /proc} — `/tmp`, `/var/tmp`, `/dev/shm` still admitted
(re-read at `:1063-1071`). ExecCounterC1's prompt carries "refuses a --work or TMPDIR under /tmp (exit 2; SentScratch)".
Same caveat as F1: the refusal must cover `/var/tmp`+`/dev/shm` and the realpath case, or the F2 class survives by one path.

**F3 (three writers' `/tmp` fallbacks) — latent, unchanged, correctly unfixed in place.** `verify.sh:155`
(`${TMPDIR:-/tmp}`), `fuzz.py` (`TMPDIR or "/tmp"`), `add-replay-clause.py:39` all still fall back at base — but these are
committed evidence of round 48; editing them would falsify the record. The forward fix is fail-closed defaults in *new*
writers: check the w2 dispatch item prompts carry `${TMPDIR:?}`-style wording — they don't; only the context forbids /tmp,
which is F4's weakness again.

**F4 (stale `/tmp` grant in dispatch) — REGRESSED-INTO-ROUND-49: open and live.** `.ufo/waves/round-49/w1-spec.json`
context still contains the literal clause "/tmp only for files under 50 MB" in the same sentence that mandates
`/fast/scratch` — the exact contradiction SentScratch F4 named, re-shipped. This wave's seats are again handed a 50 MB
`/tmp` grant by their own dispatch. Fixable pre-freeze by striking the clause in w2's spec; the honest receipt is a diff
line. **This is the strongest counterexample to "the routed fixes close the items":** the wave that is supposed to fix F4
repeats F4.

**F5 (mirror helpers leak clones) — instrument unchanged, residue gone, rule needed.** `l1-draft/c2-mirror.sh:8-9` still
has no EXIT trap (committed evidence — leave it); measured today `/fast/scratch/hyaku/mado-r48/` is **empty** (leftover
clones already gone), so the observed harm is closed. What remains open: nothing prevents the next `rm -rf`-at-start-only
helper. Fix = the trap pattern in the round-49 helper drafts + the F6 retry.

**F6 (mode-000 unremovable) — instrument + dispatch unchanged.** The referenced
`RevC1Ls/probe/u/app/unread` is gone with the rest of mado-r48, but the class is live: `c1-r48-terminal-cache-v2.py:1078`
still `shutil.rmtree(work, ignore_errors=True)` — a mode-000 fixture dir silently survives cleanup — and the round-49
context's mandated trap is still `trap 'rm -rf -- "$S"' EXIT` (no `chmod -R u+rwX` first). SentScratch's own demonstration
(`rm: cannot remove …/inner: Permission denied`) stands. Fix: dispatch-level `trap 'chmod -R u+rwX -- "$S" 2>/dev/null;
rm -rf -- "$S"' EXIT` and a chmod-retry in new counters; able-to-fail via a mode-000 fixture tree of one directory+file
(SentScratch measured it in 5 commands).

**F7 (unbounded `trace-*` write) — open in frozen v2.** `c1-r48-terminal-cache-v2.py:333` still `mkstemp(dir=work,
prefix="trace-")` + `strace -o` with no size check; `check_trace` reads it whole. With the w2 cap lifted to 64 MiB the
inherited bound is larger, not smaller. Fix for the r49 counter: `trace-oversize` trip or `RLIMIT_FSIZE` in the child —
ExecCounterC1's prompt does **not** name it (gap in the proposed fix set: F7 is the one SentScratch finding with no seat
text covering it; recommend ExecCounterC1 adopt it).

## registration-v2 residuals (`registration-v2.md:103-110`)

**Resid-1 (receipt names generator under `receipts/`, real path `tools/`) — open, re-verified.** The receipt
`.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt:1` names "generator
`.ufo/waves/round-48/receipts/make-xkb-receipt.sh`"; `git ls-tree` at base shows the script is tracked at
`.ufo/waves/round-48/tools/make-xkb-receipt.sh`, and `git grep -l make-xkb-receipt.sh` hits 8 objects — none at the named
path. The `w2-results.json` F2 line records the same mismatch. Minimal honest fix: an erratum line stating the committed
path (RevRegResiduals' proposal); do NOT move or copy the script — the receipt's path is evidence about the round's
bookkeeping, and a corrective copy would manufacture provenance that never existed. Able to fail:
`git cat-file -e 03e4ae76:.ufo/waves/round-48/tools/make-xkb-receipt.sh` proves the locator in one command.

**Resid-2 (uncited `fetch/xkbcommon-meson.build` pin) — open, re-verified.** `git grep xkbcommon-meson.build 03e4ae76`
hits only the harness's own mutant fixture (`l1-draft/v2/c2v2-harness-revc2counter.py:259,274` — a *fake locator* planted
by the variant generator), the registration's own confession, CritC2Pin F5 ("dead pin in the trust set"), and a
SHA256SUMS entry. No `SOURCES.md` row and no entry cites it. Two honest dispositions: (a) an erratum declaring it a
non-cited artifact of the freeze set (cheap, matches CritC2Pin F5's "harmless" — clause d refuses quotes from uncited pins);
(b) delete it in a later integration commit — wrong this wave, since it is part of the frozen v2 evidence the w2 controls
scored. Recommend (a). Counterexample to a "cite it" fix: the harness *already* cites the filename inside a mutant fixture
— any naive `git grep` closure check would false-positive; the check must exclude `l1-draft/` paths.

**Resid-3..5 (S346 generator chain not self-verifying; owner-column unscored; C1 judge = host coreutils/bash) — open,
declared.** Re-verified they remain "declared, not repaired": S346's row still asserts package-file `rules/evdev` ↔
`rules.in`+`meson.build` binding by digest and eyeball, not by re-running the generator (no seat is assigned the re-run —
acceptable at tier-A-mined, but the residual should stay on the books); no fixture exercises `chown`, so the owner-column
justification remains unscored; and the c1 counter's judge is still unpinned host coreutils/bash/strace — the round-49 C1
counter should at least *digest* its oracle binaries (`strace`, `bwrap`, `python3`) so the trust root is named.

## Cross-cutting notes for the L1

1. **F4 is this wave's live defect** — strike "/tmp only for files under 50 MB" from any context text that survives into w2.
2. **F7 has no owner** in the w1 item texts; fold `trace-oversize` into ExecCounterC1's draft before freeze or it freezes
   in again.
3. **The guard list for M48-10** should include `~/.config/xdg-terminals.list` (the operator file the resolver reads) and
   `XDG_RUNTIME_DIR` in the redirect set, or the demonstration proves a narrower property than the incident.
4. **ExecN4Matrix's "why" matters**: if the text-matrix generator drops the two `a-*` rows by stream bug, the round-49
   counter matrix needs a completeness clause or the same hole ships again.
5. New defect worth a routed line (none of the routed items covers it): the a4r1 results text shows a seat *trying* to
   defeat the cap with `GIT_INDEX_FILE` tricks instead of stopping — the dispatch should say explicitly that bypassing a
   stated bound is out of contract, not a puzzle to solve.
