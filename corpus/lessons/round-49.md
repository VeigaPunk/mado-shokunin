# Round 49 lesson — keysym-to-key parity and the bind key match (2026-10-27, hyaku run 9, attempt 1)

Claims: `.ufo/waves/round-49/claims.md` (`5f37c1b8`); freeze `dd2e827e` (`.ufo/waves/round-49/registration.md`); C1 data `430d2569`.
The L1's request budget ended the round after wave `w1` (45 seats) and before wave `w2`; C2 stops honestly (no data commit).

## Gate

Sources opened 2026-10-27 by w1 seats (ScrRows, ExecHyprSrc, ExecXkbSrc, ScrEntry); pins under `.ufo/waves/round-49/fetch/`
(sha256 in each candidate row, `.ufo/waves/round-49/candidate/rows.md`). Rows S352-S363 were drafted and opened but are
**not appended** to `corpus/SOURCES.md` this round: the entry that cites them did not meet `PRED-C2-r49`, and CORPUS.md rule 4
forbids rows no admitted entry cites. Admit lines with URL, access date and located quote: `.ufo/waves/round-49/w1/ScrRows/gate.md`
§1 (12 lines, quotes re-verified 19/19 by `verify-quotes.sh`). Located examples:

- **S352 (drafted admit)**, `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`,
  2026-10-27: `pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState` (`Hyprland-KeybindManager.cpp:369`).
- **S355 (drafted admit)**, `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keysym.c`, 2026-10-27:
  `The "best" case-insensitive match is the lower-case keysym name.` (`xkbcommon-keysym.c:268`).

### Rejected after opening

- `https://wiki.hypr.land/0.56.0/Configuring/Basics/Binds/` and `https://wiki.hypr.land/Configuring/Basics/Binds/`: rendered pages with no
  commit anchor; flip: the commit-pinned raw source (`d5f07c60`, drafted S359).
- ArchWiki `Hyprland`: `0.56.2` ×0, `resolve_binds_by_sym` ×0; states no 0.56.2 bind behaviour; flip: a version-pinned page.
- Re-registering `src/devices/IKeyboard.cpp` and `src/config/values/ConfigValues.cpp` at `efb50993`: held S319 / S318; cite them.

Spot-check shape: the non-author closure samples from the 2 drafted admits and 4 rejects above (counts computed from this section,
round-48 N3).

## Mistakes

**M49-1** · class `stale-premise` (seat model contradicts the source trace) · evidence: `.ufo/waves/round-49/w1/ExecBindsLive/receipts/bind-reachability.txt:4-7,264-273`
modelled Hyprland's translation state with the bind's own modifiers and declared 8 Shift binds dead, while `Hyprland-KeybindManager.cpp:369`
and `w1/ExecHyprSrc.md` (the translation state is never given modifiers) predict they fire; the ScrEntry draft repeated the claim
(`w1/ScrEntry/hyprland-bind-key-match-r49.md:120`). · captured-by: none (no criterion requires a host-consequence model to cite the
source line that sets its state). · fix: the L1 removed the claim from the candidate entry (`candidate/…:120`, `:124`); criterion owed.

**M49-2** · class `number-drift` · evidence: the w1 context said "2659 `#define XKB_KEY_` lines"; `grep -c '#define XKB_KEY_'` counts 2659
lines but only 2638 are column-0 defines (`w1/ExecKeysymNames.md:13-16`, `w1/SentHost.md` H9). · captured-by: criterion 10 (re-derive a
number from its command). · fix: claims.md never carried the number; the counter reads names with a column-0 pattern (`header_names()`).

**M49-3** · class `landing` · evidence: two seats reported deliverables as written before the files existed (`w1/ExecRefKeysymA.md:7`
vs an empty seat dir at 02:05; `w1/ScrRows.md` vs a missing `rows.md`, written after an L1 message). · captured-by: none. · fix: the L1
checks every reported path with `test -f` before integrating (done this round); criterion owed.

**M49-4** · class `landing` (L1) · evidence: the round's request budget ran out after w1; w2 (38 drafted items, `w2-items.json`) was
never dispatched, so C1's freeze is unattacked and C2 has no data. · captured-by: none. · fix: size L1 polling to the budget; the
next round carries w2's items.

## Round-48 closure items

- N1: the untracked count was 47, not 52 (`git status --porcelain -uall | wc -l` → 47 at `03e4ae76`, all `*.synthetic`).
- N2: `host_cache_untouched_sha256` in `.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:4` is the digest of the w2 mutant's
  7 bytes `r48-w2\n`, i.e. the operator cache was NOT untouched at that capture. Operator-owned digest pair this round:
  `.ufo/waves/round-49/receipts/operator-state-before.txt` / `operator-state-after.txt`.
- N3: `corpus/lessons/round-48.md:425` "five gate decisions (three admits, two rejects)" should read 12 admits and 3 rejects.
- N4: the full 98-row matrix: `.ufo/waves/round-49/w1/ExecN4Matrix/c2v2-matrix-full.txt` (frozen round-48 file untouched).
- N5: S346/S347's GitLab `-/raw/` URLs serve an anti-bot page; fetch through `/api/v4/projects/<id>/repository/files/<path>/raw?ref=<tag>`
  (`w1/ScrCorrections.md`).
- M48-8: the 47 sidecars are committed (`dd2e827e`; w1/CritSidecars: findings at the tip 159 → 110 by the marker layer, no real
  material waived); gate v3 drafted (`w1/ExecSessionShapes/`, 94/94 selftest, red at base by design) — not installed.
- M48-10: host guard drafted and shown able to fail on a fake home (`w1/ExecMutantSandbox/`); every w1 seat ran with HOME/XDG_* in
  scratch; not installed.
- M48-13: the w1 context set `ulimit -f 65536` (64 MiB); the owed clause-r attack ran (`w1/ExecCloneRecipe.md`).
- SentScratch: the round-49 counters refuse `/tmp` work dirs and TMPDIR under `/tmp`, `/var/tmp`, `/dev/shm`.
