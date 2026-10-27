# ScrRowsR50 — round 50 w1, C1 registry rows S352-S363 (leaf seat report)

Verdict: **done, gates green.** 12 rows S352-S363 drafted in the fleet 11-cell registry schema, 12 admit gate lines
(≤25-word quotes, locators computed and machine-verified against the round-50 pins), 5 reject lines carried from round 49
with reason and flip, and `sources-census.sh validate` **exit 0** on a mirror with the rows appended. Pins are re-fetched
this round and **byte-equal to round-49's** (14/14). No tracked file edited, no git/jj mutation, no counter or gate run,
no tool installed.

Lane `mado-shokunin`, base `8ae47b957034ae21012bbf09173cca2c48be345e`, claims commit `13631f24`.

## Behavior (what ran, with outputs)

1. **Re-fetched every cited source this round** (2026-10-27, HTTP 200), into scratch, then installed as pins under
   `.ufo/waves/round-50/fetch/` with `SHA256SUMS` (16 files: 14 upstream + `binds-live-r50.txt` + manifest):

   ```
   200 Hyprland-KeybindManager.cpp 39334        200 xkbcommon-keysym.c 14948
   200 Hyprland-legacy-ConfigManager.cpp 90963  200 xkbcommon-keysym.h 4949
   200 Hyprland-InputManager.cpp 98845          200 xkbcommon-ks_tables.h 324906
   200 Hyprland-IKeyboard.hpp 4816              200 xkbcommon-tools-how-to-type.c 30238
   200 Hyprland-IKeyboard.cpp 15941             200 xkbcommon-xkbcommon-keysyms.h 264502
   200 Hyprland-ConfigValues.cpp 59222          200 xkbcommon-state.c 67069
   200 wiki-Binds.md 19526                      200 wiki-Variables.md 51064
   fetched=14 failed=0
   ```

   Every one `cmp`-equal to `.ufo/waves/round-49/fetch/` (14/14 in `quotes-verified.txt`), so the round-49 ground holds
   and only the pin path, the used-by and S361's facts differ from the round-49 draft.

2. **Live host receipt (S361)** — owned by seat `ExecLiveR50`, not by me. I verified its bytes and installed the
   byte-equal pin copy:
   ```
   sha256sum .ufo/waves/round-50/fetch/binds-live-r50.txt
   9f16e5a5ce7fe39fc30cd8a6041fcdf733f7b794f20310796bae09d01ae51590  (1768 B)
   cmp -s fetch/binds-live-r50.txt w1/ExecLiveR50/binds-live-r50.txt  -> byte-equal
   ```
   My own independent read-only capture (clean env: `HOME`/`XDG_*` under scratch, `HYPRLAND_INSTANCE_SIGNATURE` and
   `XDG_RUNTIME_DIR` preserved) produced the same raw JSON digest and counts as the receipt:
   ```
   hyprctl binds -j | sha256sum -> 9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779 (90401 B)
   binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0
   hyprctl getoption input:resolve_binds_by_sym -j -> {"int": 0, "set": false }
   hyprctl version -> Hyprland 0.56.2 ... commit efb50993780079460b0cbed1363e2166a2de1d9f
   ```
   Both digests equal round 49's, so every round-49 count still holds.

3. **Rows** — `.ufo/waves/round-50/w1/ScrRowsR50/rows.md`: one table, 12 rows, 11 cells, opened `2026-10-27`, recheck
   `on-release` for the version-pinned sources and `90d` for the host receipt. Anchors name the pin
   `.ufo/waves/round-50/fetch/<basename>` with size, line count and `sha256:<64hex>`. `NF=13` for all 12 rows, so no cell
   carries a literal or escaped `|`.
   **Rows that serve only `tools/mado-keysym.py` — and therefore carry `used-by corpus/lessons/round-50.md` instead of
   the entry — are S357 and S358.** The other ten carry `corpus/knowledge/hyprland-bind-key-match-r50.md`.
   L1 extraction command: `awk '/^\| S3(5[2-9]|6[0-3]) /' .ufo/waves/round-50/w1/ScrRowsR50/rows.md`, appended after the
   S351 line inside `## Registry`.

4. **Gate lines** — `.ufo/waves/round-50/w1/ScrRowsR50/gate.md`: paste source for `corpus/lessons/round-50.md` `## Gate`.
   Twelve `**S### admit**` lines (URL, opened 2026-10-27, quote in `»…«`, pin:line, word count, reason) and five reject
   lines: the two `wiki.hypr.land` rendered Binds pages, ArchWiki `Hyprland`, and re-registering `IKeyboard.cpp` (held
   S319) and `ConfigValues.cpp` (held S318), each with its flip. Rejects were re-opened this round: 386362 B / 356517 B /
   123942 B (all three byte counts unchanged from round 49), 0 forty-hex tokens and 0 `efb5099` in the 0.56.0 page,
   `resolve_binds_by_sym` present there (1 hit) but absent from ArchWiki (0), and `git ls-remote --tags` on the wiki
   returns 0 lines.

## Gates (all run; outputs are in the seat dir)

| gate | command | result |
|---|---|---|
| quote/pin verification | `bash .ufo/waves/round-50/w1/ScrRowsR50/verify-quotes.sh` | rc 0, 12/12 rows PASS, 12/12 admit lines, 5/5 rejects, 14/14 pins byte-equal (`quotes-verified.txt`) |
| row shape | `grep -cE '^\|S…'` + `awk NF!=13` + histograms | rows 12, malformed 0, A=12, mined=12, docs=2 own-work=1 code=9, entry=10 lesson=2 |
| anchor digests vs disk | python over the anchor cells and the pin dir | `anchor pins checked: 12, mismatched: 0` |
| census | `bash .ufo/waves/round-50/w1/ScrRowsR50/census-check.sh` → `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` | **exit=0**; 18 W04 + 1 W01, **0 E**; delta vs `receipts/census-before.txt` is exactly `W04 S353` and `W04 S354` (`census-r50.txt`) |
| mirror integrity | `diff <(git show HEAD:corpus/SOURCES.md) <mirror>` | 12 added lines, 288 → 300 rows |

Census output tail (full text in `census-r50.txt`):
```
file	W04	S353 duplicate url …/src/config/legacy/ConfigManager.cpp across scopes
file	W04	S354 duplicate url …/src/managers/input/InputManager.cpp across scopes
file	ok	/fast/scratch/hyaku/mado-r50/ScrRowsR50/census/mirror/corpus/SOURCES.md
exit=0
```
The two new W04 are the duplicate-URL decisions stated in `rows.md` §Notes (S353 vs held S162/S303/S317; S354 vs held
S316) — warnings, not E04, because the scopes differ. No E03/E04 anywhere.

## Touched surfaces

Created (untracked) in the lane:
- `.ufo/waves/round-50/fetch/` — 14 re-fetched pins, `binds-live-r50.txt` (byte-equal copy of ExecLiveR50's file) and
  `SHA256SUMS`. This dir is round-shared: if another seat adds pins later, the manifest needs regenerating.
- `.ufo/waves/round-50/w1/ScrRowsR50/` — `rows.md`, `gate.md`, `verify-quotes.sh`, `quotes-verified.txt`,
  `census-check.sh`, `census-r50.txt`, `receipts-rows-check.txt`.
- `.ufo/waves/round-50/w1/ScrRowsR50.md` — this report.

Not touched: no tracked file, no `corpus/SOURCES.md`, no knowledge entry, no lesson, no counter, `.ufo/state/`,
`.ufo/watchdog.log`, `.scratch/`, the fleet root, sibling lanes or the shokuknow checkout. No git/jj mutation (read-only
`git show`/`git status` only). No installs, no pacman (host-wide pause respected), no terminal/GUI, only the permitted
`hyprctl version|binds -j|getoption … -j` reads; scratch `/fast/scratch/hyaku/mado-r50/ScrRowsR50` deleted at the end.

## Findings

1. **Round-49 pins reproduce exactly (14/14).** The C1 ground is stable across the round boundary; the only row whose
   facts changed is S361, because the round-50 receipt is a new file (1768 B vs 1302 B) that adds a `modmask_histogram`
   block while the raw JSON digest stays `9a47199e…`. A row that copies S361's round-49 byte count would be wrong.
2. **D8 class guarded in this seat.** Round 49's lesson said "the 2 drafted admits and 4 rejects" while its gate held 12
   admits and 5 rejects. `gate.md` §4 carries the counts with the commands that print them (12 / 5 / A=12 / mined=12 /
   entry=10 lesson=2); the round-50 lesson must quote these, not retype a figure.
3. **S361's anchor is the `fetch/` pin, not a `receipts/` path.** `.ufo/waves/round-50/receipts/binds-live-r50.txt` does
   not exist at this seat's close; the receipt lives in ExecLiveR50's seat and the byte-equal pin is under `fetch/`
   (precedent: S295-S297, S337, S338, S350 cite `fetch/`). The L1 still needs to install the `receipts/` copy for any
   frozen clause that reads a receipts path.
4. **Counter caveat passed on from ExecLiveR50** for the PRED-C1-r50 port: the round-50 receipt's embed-guard must keep
   the quoted-JSON form; a guard that rejects a bare `modmask` substring fails on this receipt's `modmask_histogram`
   header. (Also from `SentHostState`: never wrap the frozen C1 counter in an outer tracer — nested ptrace makes it report
   a false `TARGET_MISSED`.)
5. **Probe trap, measured here.** `env -i … hyprctl binds -j` without `HYPRLAND_INSTANCE_SIGNATURE` writes
   `HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)` to **stdout** (61 B, stderr empty) and exits **1**; with
   the variable preserved it is rc 0 and 90401 B of JSON. A clean-env probe must keep the signature, and a harness that
   only checks "output exists" would read the warning as data.
6. **Unrelated working-tree state, not mine:** `git status --porcelain` at my close shows ` M` on
   `.ufo/waves/round-49/w1/ExecControlsC1.md`, `.ufo/waves/round-49/w1/ExecControlsC1/check-c07-isolation.py`,
   `.ufo/waves/round-49/w1/ExecControlsC1/make-controls-receipt.py` and `.ufo/waves/round-49/w1/ExecCounterC1.md` — a
   sibling seat's live writes (ExecControlsC1 is running this wave). I neither wrote nor reverted them.

## Out of scope (not done, by assignment)

Appending the rows to the tracked `corpus/SOURCES.md` (L1 integration), writing
`corpus/knowledge/hyprland-bind-key-match-r50.md` and `corpus/lessons/round-50.md` (other seats; the two mirror stubs
exist only in scratch and are rebuilt by `census-check.sh`), and running or freezing any round-50 counter/predicate.

## Artifacts (all exist at close, `test -f` checked)

```
17285  .ufo/waves/round-50/w1/ScrRowsR50/rows.md
12732  .ufo/waves/round-50/w1/ScrRowsR50/gate.md
 5670  .ufo/waves/round-50/w1/ScrRowsR50/verify-quotes.sh
 1449  .ufo/waves/round-50/w1/ScrRowsR50/quotes-verified.txt
 6158  .ufo/waves/round-50/w1/ScrRowsR50/census-check.sh
 4931  .ufo/waves/round-50/w1/ScrRowsR50/census-r50.txt
 1488  .ufo/waves/round-50/w1/ScrRowsR50/receipts-rows-check.txt
        .ufo/waves/round-50/fetch/  (16 entries incl. SHA256SUMS)
```
Deliverable digests: `rows.md 79c091dd…b3a7f`, `gate.md 322d0ae6…6b0b1`, `verify-quotes.sh 57636029…80d3a`,
`quotes-verified.txt c092932d…7de0a8`, `census-check.sh 9af5459b…f13a9`, `census-r50.txt 46a0653b…5e33` (full 64-hex in
`receipts-rows-check.txt`).
