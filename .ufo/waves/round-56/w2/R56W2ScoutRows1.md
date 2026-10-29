# R56W2ScoutRows1 — wave-2 re-opening of registry rows S383, S384 (falsify)

Lane: mado-shokunin. Tree scored: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (git objects only; working tree never read for evidence).
Attack target: wave 1's row author wrote S383/S384 and the gate quoted from the pin files — nothing independent had fetched the upstream bytes. I fetched both URLs myself and re-derived every check from those bytes.

## Verdicts

| row | bytes | gate quote | anchor bounds | K/E quotes vs upstream | cells | census | verdict |
|---|---|---|---|---|---|---|---|
| S383 | MATCH | MATCH (line 34) | MATCH (max 105 ≤ 111) | 12/12 in anchor; **E03 at :106 OUTSIDE anchor** (defect D1) | MATCH | clean | MATCH with defect D1 |
| S384 | MATCH | MATCH (line 492) | MATCH (492 ≤ 734) | 2/2 in anchor (K01, K02) | MATCH | W04 only (D2, cosmetic) | MATCH |

## What I did and the decisive output

### 1. Independent fetch + sha256 (attack: nobody fetched upstream bytes)
```
curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp
curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp
sha256sum →
  8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c  ConfigWatcher.cpp   (111 lines, 4046 B)
  a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754  ConfigValues.cpp    (734 lines, 59222 B)
```
- Equal to the sha256 in the rows' anchor cells (`SOURCES.md:333/334` at the rev), to `frozen-tables-v2.json` `c1.pin_sha256`, and byte-identical to the committed pin blobs (`git cat-file blob 28fc86ac:.ufo/waves/round-56/fetch/...`, cmp True both). URL token `efb50993780079460b0cbed1363e2166a2de1d9f` = frozen `c1.commit`.
- Registry scratch copy verified `==` the rev blob (`git cat-file blob 2ba4825b…`).

### 2. Gate quotes located in MY fetched bytes (gate claims in `w1/R56ScribeSourcesA/gate.md`)
- S383: `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` → substring search over split lines: **line 34** (gate claims 34). MATCH.
- S384: `"If true, the config will not reload automatically on save."` → **line 492** (gate claims 492). MATCH.

### 3. Every K/E row citing S383/S384: quote-in-upstream-line and line-in-anchor
Entry `corpus/knowledge/hyprland-config-autoreload-r56.md` at the rev. S383 anchor locators: `33-34,46,54-56,60,67,69,105` = {33,34,46,54,55,56,60,67,69,105}; S384 anchor: {492}.

| row | src | pin:line | quote byte-true in upstream line | line in anchor |
|---|---|---|---|---|
| K01 | S384 | 492 | True | True |
| K02 | S384 | 492 | True | True |
| K03 | S383 | 33 | True | True |
| K04 | S383 | 34 | True | True |
| K05 | S383 | 46 | True | True |
| K06 | S383 | 54 | True | True |
| K07 | S383 | 55 | True | True |
| K08 | S383 | 56 | True | True |
| K09 | S383 | 60 | True | True |
| K10 | S383 | 67 | True | True |
| K11 | S383 | 69 | True | True |
| K12 | S383 | 105 | True | True |
| E02 | S383 | 60 | True | True |
| **E03** | S383 | **106** | True (`.file = WD->file,`) | **False — defect D1** |

### 4. Anchor locators vs file end (v2 E3 bound)
`len(blob.split(b"\n"))` = 112 (ConfigWatcher, file ends with newline) and 735 (ConfigValues); wc-newline counts 111/734. Max locators 105 and 492 — nothing runs past EOF. MATCH for both rows.

### 5. Cell semantics
- S383: kind `code` (C++ source), tier `A`, status `mined`, opened `2026-10-28` (valid ISO), recheck `on-release` (valid symbolic cadence; census E09 accepts, selftest lists it), used-by names the entry. Scope/teaches state only what the anchored lines show: disable gate `PDISABLEAUTORELOAD` + ternary (33–34, inside `CConfigWatcher::update()`, line 32), file/directory masks `IN_CLOSE_WRITE|IN_DONT_FOLLOW` / `+IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM` (55–57), rm of old watches (45–47), add per path (59–61), canonical symlink watch (65–70), event callback (105–107). All verified against the fetched bytes.
- S384: line 492 alone carries `MS<Bool>("misc:disable_autoreload", "If true, the config will not reload automatically on save.", false, {.refresh = Supplementary::REFRESH_CONFIG_WATCHER}),` — the scope/teaches claims (boolean, default false, description, refresh tag) are all literally on that line. Cells valid as above.

### 6. Census validator
```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch copy of registry at 28fc86ac> --today 2026-10-28
```
- Direct run (rc=1): no E/W row findings for S383; `W04 S384 duplicate url …/ConfigValues.cpp across scopes`; the many `E11 missing used-by …` lines (incl. S383/S384) are a run-setup artifact — with `--file` into scratch no used-by path exists on disk. Not lane evidence.
- Clean re-run against a full `git archive` mirror of the rev tree (`--file mirror/corpus/SOURCES.md`, rc=0): **zero E-codes**, 32×W04 + 1×W01. Only line touching my rows: `file  W04  S384 duplicate url raw.githubusercontent.com/.../ConfigValues.cpp across scopes` (shared with S318) — warning class by design, does not fail validation.
- No E08/E09: opened dates and `on-release` recheck are valid.
- Note: invoking the census script directly under the bash tool twice died silently (no output); the run above was redone via `subprocess.run` with identical argv and produced full output (both outputs preserved in deliverables).

## Defects

- **D1 — weakens the claim.** Entry row **E03** (`hyprland-config-autoreload-r56.md:123` at 28fc86ac) cites `S383` at `Hyprland-ConfigWatcher.cpp:106` (quote `.file = WD->file,` — byte-true in upstream line 106), but S383's anchor is `ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105` — 106 is not covered. Input: entry line 123 + SOURCES.md line 333 anchor cell. Not visible to the registered C1 counter because its `scope`/`sources` counts are defined over K rows only (registration.md §C1: "c = K rows … d = K rows"), so the lane's `scope=30/30` is true of its own definition; but the registry does not anchor one of the entry's two S383 E-row citations, and the seat contract's K/E anchor-coverage check fails. The quote is real and line 105 (anchored, K12) opens the same `m_watchCallback(SConfigWatchEvent{` block, so this is a one-token anchor gap, not a fabrication. Fix would be `105-106` (or `105,106-107`) in S383's anchor.
- **D2 — cosmetic.** Census `W04` on S384: URL shared across scopes with S318. Warning class by the validator's own design ("warnings do not affect clean lanes"); recorded for completeness. S383 has no census findings.

## Not verified / notes
- Rows S385–S391 and the H rows are other seats' scope; not checked here.
- Entailment of propositions beyond quote identity was spot-read (context lines above) and found faithful, but the full sentence-to-pin audit belongs to the designated wave-2 seats.
- Tooling: nothing installed or upgraded (none needed); pacman untouched. No hyprctl/host reads used. No git/jj mutation anywhere; only `git cat-file`/`git show`/`git archive` (read-only) against the lane.

## Deliverables
- `.ufo/waves/round-56/w2/R56W2ScoutRows1/Hyprland-ConfigWatcher.cpp` — my independent fetch (8383b8ab…)
- `.ufo/waves/round-56/w2/R56W2ScoutRows1/Hyprland-ConfigValues.cpp` — my independent fetch (a76f0507…)
- `.ufo/waves/round-56/w2/R56W2ScoutRows1/census-validate.txt` — census run vs scratch copy (E11 artifact run)
- `.ufo/waves/round-56/w2/R56W2ScoutRows1/census-validate-mirror.txt` — census run vs rev-tree mirror (clean, rc=0)
- `.ufo/waves/round-56/w2/R56W2ScoutRows1/checks.txt` — hash/locator/quote summary
- Scratch `/fast/scratch/hyaku/mado-r56/R56W2ScoutRows1/` removed before yield.

Report: .ufo/waves/round-56/w2/R56W2ScoutRows1.md
