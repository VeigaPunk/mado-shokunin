# R54Seat15 — cross-claim causal separability review (connector, item 15)

Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin` · base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`
Frozen inputs: `.ufo/waves/round-54/claims-frozen.md`, `.ufo/waves/round-54/registration.md`
Scope: C1 (errata source-truth, round-52 pins) vs C2 (uwsm-app entry, round-54 pins). Leaf seat; no subagents; no lane edits; no host reads; no installs.

## Verdict

- **Pin namespaces are separable.** No C1 quote occurs in any round-54 pin; no C2 quote occurs in any round-52 pin (whitespace-normalized search, both directions, 0 cross hits).
- **Judges are not separable from implementation.** Both frozen "verbatim" rules are inconsistent with their own frozen quotes. Under the literal rules, C1 resolves 1/4 quotes and C2 resolves 1/3 quotes against the committed pins. Any counter that reaches the frozen target must apply a normalization that the frozen text does not state, and the two counters are free to choose it differently. That is the coupling channel between the claims.
- **Freeze declarations are incomplete for both claims** (read-sets omit `registration.md`; one SHA256SUMS filename disagrees between the frozen files; both round-54 pins and the freeze itself are untracked in git).

Axes: coverage (quote→pin resolution of the frozen table) and operability (whether the frozen judge is executable as written). Coverage holds for the pin namespaces; operability fails for both judges as literally written.

## Method (exact commands; all read-only on lane; scratch `/fast/scratch/hyaku/mado-r54/R54Seat15`, removed before yield)

1. Pin integrity, round-54:
   `cd .ufo/waves/round-54/fetch && sha256sum -c SHA256SUMS.txt` →
   `uwsm-0.27.1-README.md: OK`, `uwsm-0.27.1-main.py: OK`, `uwsm-0.27.1-uwsm-app.1.scd: OK`.
2. Pin integrity, round-52 vs `registration.md` C1 table: `sha256sum Hyprland-*` → 4/4 equal to the registered values (ConfigActions.cpp a83abeb5…, ConfigActions.hpp 746c6f51…, KeybindManager.cpp 8d8f35fc…, legacy-DispatcherTranslator.cpp 7248cbb8…).
3. Frozen-quote resolution, exact bytes and whitespace-normalized (`" ".join(s.split())`), python3 -I script in scratch (`verify_quotes.py`, `xcheck.py`).
4. Cross-namespace search: every C1 quote over all `round-54/fetch` files; every C2 quote over all `round-52/fetch` files.
5. Raw `sed -n` / `cat -A` of the anchor spans and of the S375–S377 locations.
6. Entry check: `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` rows P19–P22 compared to the frozen strings.
7. Tracking state: `git -C <lane> ls-files --error-unmatch <path>` per pin/entry; `git -C <lane> status --short` → `?? .ufo/waves/round-54/` (only untracked path).

## Results

### C1 — frozen quotes vs round-52 pins

| ID | pin : anchor | exact bytes in anchor span | exact bytes anywhere in file | whitespace-normalized in span |
|---|---|---|---|---|
| P19 | ConfigActions.cpp:1554-1558 | NO | NO | YES |
| P20 | ConfigActions.cpp:1576 | YES | YES (line 1576) | YES |
| P21 | legacy-DispatcherTranslator.cpp:619-622 | NO | NO | YES |
| P22 | legacy-DispatcherTranslator.cpp:573-574 | NO | NO | YES |

Raw bytes (`cat -A`): P19 spans `sendKeyboardMods(modMask, 0, 0, 0);$` / `$` (blank line) / `if (S.m_passPressed == 1) {$` / `if (!isMouse)$` / `sendKeyboardKey(...)`. P21 and P22 likewise contain line breaks and blank lines between the frozen "single logical line" tokens.

Entry check: the four Quote cells of the committed entry equal the frozen strings byte-for-byte (4/4). The entry therefore carries the whitespace-collapsed form as if it were a verbatim span.

### C2 — frozen quotes vs round-54 pins

| row | pin : location | exact bytes | whitespace-normalized |
|---|---|---|---|
| S375 | uwsm-0.27.1-README.md:117-118 | NO (line break + `  into` indent after `exported`) | YES |
| S376 | uwsm-0.27.1-uwsm-app.1.scd:60 | NO (pin reads `*uwsm-app* client sends …`; markdown emphasis) | NO (by inspection, stripping `*` gives a match; no such rule is frozen) |
| S377 | uwsm-0.27.1-main.py:3714 | YES | YES |

The S376 pin also reads `uwsm's` with a straight apostrophe, which matches the frozen string. The S376 mismatch is solely the `*` emphasis markers.

### Cross-namespace (contamination) search

- C1 quotes P19–P22 in round-54 pins (normalized): 0/4 hits.
- C2 quotes S375–S377 in round-52 pins (normalized): 0/3 hits.
- C2 quotes in round-54 pins (normalized): S375 → README; S377 → main.py; S376 → none (see above).

## Findings

**F1 (C1 judge contradicts its own quotes — coupling channel).** `registration.md` (Counter form paragraph): "exact byte contiguity after single-space normalization of interior newlines ONLY where the frozen quote itself carries a newline (P19/P21/P22 are single logical lines)." The frozen P19/P21/P22 quotes carry no newline, so the literal rule forbids normalization; the pin spans do contain newlines. Literal reading → quotes 1/4 → `propositions/quotes≤3/4` → `TARGET_MISSED` at the frozen base pins. Normalizing whitespace (which any counter would need to reach 4/4) is not what the frozen sentence says. The verdict therefore depends on an implementation choice (how far to normalize) that the freeze does not fix.

**F2 (C2 judge is underdefined and fails two of three rows).** `registration.md` (C2 fixture inventory) states "located quote (≤25 words) occurs verbatim" and gives no normalization rule at all. Literal reading → S375 and S376 fail (1/3). A whitespace normalizer rescues S375 only; S376 needs markdown emphasis stripping, which is not frozen anywhere. Consequence: the C2 counter cannot reach `admitted=1/1` through any rule the freeze states, and any counter that does is using an unfrozen rule.

**F3 (shared judge = shared coupling).** F1 and F2 are the same defect in two claims. If the counters share a helper (natural for two sibling counters under `quality/counters/`), a normalizer chosen to rescue S376 (markdown stripping) changes C1's matching too, and vice versa. I did not construct a demonstrated false admit: C1's controls still fail under whitespace or markdown normalization (no `*` in P19–P22; spliced/shifted/swapped controls remove the quote text itself). The risk is latent, not shown.

**F4 (declared read-sets omit `registration.md`).** `claims-frozen.md` "Causal separability" says C1 reads "the frozen table of this file." `claims-frozen.md` contains the IDs and anchors (lines 19–30) but not the P19–P22 quote strings or the six C1 controls; those live only in `registration.md` (lines 25–47). C2's read list omits `registration.md`'s host set and S375–S377 table (lines 61–76) and the six C2 controls (lines 80–87). Both counters must therefore either embed their frozen tables (copies of the judged data inside the judging code) or read `registration.md` outside the declared sets. Either way the declared separability statement is wrong for both claims in the same way (repeat of the M53-4 freeze-completeness class).

**F5 (filename disagreement; host-path dependency in C1's pin leg).**
- `registration.md` line 12 says round-52 hashes come from "its committed `SHA256SUMS.txt`". The committed file is `.ufo/waves/round-52/fetch/SHA256SUMS` (tracked, 5 lines incl. README.txt); `SHA256SUMS.txt` does not exist there. `claims-frozen.md` says "(+SHA256SUMS)". A counter that follows `registration.md` literally returns pins-leg failure by absence, not by content.
- The committed round-52 `SHA256SUMS` lists absolute host paths (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/…`). A `sha256sum -c` run from the repo fails on any other checkout. C1's pin leg therefore depends on the host filesystem layout unless the counter reduces each line to its basename and hashes `git show <rev>:…` bytes. The frozen text does not say which.

**F6 (C2 is host-independent in verdict, host-unverifiable in truth; freeze is untracked).**
- C2's verdict path reads only committed text. The host join clause (c) checks citation strings, so the counter is causally separable from host state. The citations themselves are not pinned to any committed host artifact; `fetch/README.txt` records a same-day host read by L1 and nothing else. That is not checkable from the lane.
- Git state: `git -C <lane> ls-files --error-unmatch` → `.ufo/waves/round-52/fetch/SHA256SUMS` TRACKED, `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` TRACKED; `.ufo/waves/round-54/fetch/SHA256SUMS.txt`, `…/uwsm-0.27.1-main.py`, and `registration.md`/`claims-frozen.md` UNTRACKED (`git status --short` → `?? .ufo/waves/round-54/`). Consequences: (i) any `--rev` ≥ base cannot read C2's pins from git objects until they are committed, so C2 would read nothing at a rev that predates the commit; (ii) the "frozen before any dispatch" status rests on file mtimes (14:00), not on git history, so a post-score edit to the frozen files leaves no trail.

## Predicate impact (what the frozen text implies; nothing run)

- PRED-C1-r54 as literally worded: `quotes=1/4` → `TARGET_MISSED`. Reaching `TARGET_MET` requires a whitespace-normalizing judge the freeze does not state.
- PRED-C2-r54 as literally worded: `admitted`/clause (b) fails for S375 and S376 → `TARGET_MISSED`. Reaching `TARGET_MET` requires normalization the freeze does not state (whitespace for S375, markdown emphasis for S376).
- Counters are not in the lane at base (`ls quality/counters | grep r54` → none; `ls corpus/knowledge | grep r54` → none), so their code, selftests and controls were not run. The findings above concern the frozen inputs, not any implementation.

## Proposed move (for L1 decision; not applied)

1. Either an honest `TARGET_MISSED` report for both claims under the frozen judge text, or a pre-data re-registration as `claims-frozen-v2.md` that states one explicit normalization rule for both claims (whitespace runs collapse everywhere; markdown `*` stripped for `.md` pins), with declared read-sets including `registration.md`, and with the SHA256SUMS filename and basename/`git show` hashing rule fixed. Note the pins were already read by L1 and by this seat, so any v2 normalization is a post-look amendment and must be labeled as such.
2. Commit the freeze files and round-54 pins before any scored `--rev`; the frozen files must be in git history to be frozen.
3. Keep C1's counter free of host paths: hash `git show <rev>:<path>` bytes, reduce SHA256SUMS lines to basenames.

Cost: none beyond the two-line rule statements and the commit. Axes: the proposal improves operability (single judge rule) and coverage (both claims resolvable) without touching the other claim's evidence; it does not change the C1 or C2 controls.

## Checks the main agent should run (once counters exist)

- `git -C <lane> ls-files .ufo/waves/round-54` (expect all freeze and pin files after commit).
- For each counter: run with `--rev <rev>` on a tree where C1 pins are mutated but C2 files are unchanged, and vice versa; C1's line must not change under C2-only mutation and conversely.
- Confirm the judge helper (if shared) gives identical results on C1 and C2 quotes under the frozen normalization rule.

## Tool updates

None. No installs, no package queries. Used python3 (stdlib, `-I`), sha256sum, sed, git read-only (`rev-parse`, `ls-files`, `status`). RULES.md was not read because nothing was installed.

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r54/R54Seat15` (verify_quotes.py, xcheck.py, entryq.py) removed before yield. No writes outside this report and that scratch. No lane tracked files, no fleet files, no host files touched.
