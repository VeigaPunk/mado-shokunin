# RevSchemaPreflight — registry append pre-flight (mado r37 w1, reviewer)

Verdict: **PASS with conditions.** The three planned rows (S212, S213, S214) can be appended
cleanly. Nothing in the current registry collides with them: no W04, no E04 and no id clash.
Today one hard blocker stands, which is an ordering rule: both planned `used-by` targets are
absent, so `mined` rows that cite them fail E11 until the knowledge entries exist. There are
also two silent traps that leave validate reporting `ok`: a row indented 4 or more spaces, and
a `queued` status used to dodge the `used-by` check.

Read-only throughout. Scratch: `/dev/shm/mado37-RevSchemaPreflight/` (`harness.sh`,
`harness.out`, `manual.sh`, `manual.out`, and a symlink mirror `lane/` whose `corpus/SOURCES.md`
is a copy with PLACEHOLDER rows). No lane file, jj state or git index was touched. Tools
installed: none.

## 1. Contract and script lines relied on

CORPUS.md (SOURCES contract v1):
- `:89` — "`id` — `S` + 3 or more digits, the next unused; never reused. No `|` inside any cell."
- `:106-108` — "`opened` — ISO date … `recheck` — ISO date or cadence (`90d`, `180d`, `on-release`)."
  and "`used-by` — repo-relative paths …, comma-separated, or `—`."
- `:103-104` — "`status` — `queued` (opened, worth mining) · `mined` (cited by ≥1 path in `used-by`) · `rejected`".
- `:112-118`, Rule 1 — "The round lesson's `## Gate` records, for every new row, the URL, the access date, and a ≤25-word quote with its location grounding `teaches`." Rule 2 — "Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson."
- `:145-148`, the frozen manual used-by check, splits on `[,;]`: `n=split($12, a, /[,;]/)`.
- `:152-154` — the maintained CLI accepts 0–3 leading spaces; "4 or more spaces are indented code and are ignored."

`scripts/sources-census.sh`:
- Codes, `:24-33`: "E03 duplicate id   E04 duplicate URL+scope (no supersedes)" … "E11 used-by path missing on disk" / "E12 row-shaped source outside the ## Registry section" … "W04 same URL across scopes (warnings do not affect clean lanes)". Exit codes `:16-18`: "0 clean or warnings · 1 E/overdue findings".
- E03, `:641`: `else if (id in seen) printf "%s\tE03\t%s duplicate id\n",lane,id`
- W04, `:643-645`: `scope_key=u SUBSEP scope` / `if (u!="" && (u in url_seen) && !(scope_key in url_scopes))` → `W04 … duplicate url %s across scopes`
- E04, `:646-649`: `if (u!="" && (scope_key in url_scopes) && status!="rejected" && url_scope_nonrejected[scope_key] && teaches !~ /supersedes S[0-9]{3}/)` → `E04 … duplicate url %s within scope %s`
- URL key, `:600-605` (`url_of`): takes the first `https?://` match in the **source** cell, strips any `#fragment` and a trailing `/`, drops the scheme, and lowercases the host only. It does not canonicalise `github.com/…/blob/<tag>/` against `raw.githubusercontent.com/…/<sha>/`.
- E11 / used-by existence, `:559-568`: only rows with `status = mined` are checked; `IFS=',' read -r -a paths`; `[ ! -e "$dir/$path" ]` → `E11 %s missing used-by %s`. Here `$dir` is the lane root (with `--file`, `dirname(file)/..`, `:500-501`).
- Recheck format, `:663-667` with `symbolic()` at `:582`: a valid ISO date, or `^[0-9]+d$`, or `^[A-Za-z][A-Za-z0-9 _-]*$`; anything else gives E09. E08, `:660-662`: `opened` must be a real ISO date that is not after `--today` (UTC).
- E12 and the section gate, `:609-622`: a `##` heading sets `in_registry` only when its text is exactly `Registry`; an `S###` row anywhere else gives E12.
- E01, `:635-638`: `NF!=13`. Every `|` counts, including one inside backticks.

## 2. Baseline (current lane, before any append)

`bash scripts/sources-census.sh validate --file mado-shokunin/corpus/SOURCES.md` (also run as lane `mado`), from the fleet root:
```
file	W04	S030 … S042 … S045 … S097 … S119 … S120 … S121 … across scopes   (7 lines)
file	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
rc=0
```
`TMPDIR=/dev/shm/mado37-RevSchemaPreflight bash scripts/sources-census.sh selftest` → `selftest ok`, rc=0. This includes `killed W04-scope-sensitive-mutant` and `killed E04-rejected-pair-exemption-mutant`.

Registry geometry: `## Registry` at `:9`, header at `:11`, last row `S211` at `:213`, blank `:214`, `## Paths` at `:215`. The highest id is 211, and S212–S214 are unused: `grep -nE '^\|[[:space:]]*S21[0-9]'` shows only S210 and S211. The row count is 201, which matches `assimilation/reg-ids`.

## 3. Duplicate-URL sweep (the `grep -n` asked for) — PASS

Run in `mado-shokunin/corpus/SOURCES.md`:
- `grep -n 'workspaces.cpp'` → **no output**.
- `grep -n 'Logger.cpp'` → **no output**.
- `grep -n 'src/debug'` → only `:30` S018 (`…/blob/v0.56.2/src/debug/HyprCtl.cpp`) and `:170` S158 (`…/src/debug/HyprCtl.cpp`). That is a different file.
- `grep -n 'Alexays/Waybar'` → S053 `waybar-custom.5.scd`, S054 `custom.cpp`, S201 `hyprland/backend.cpp`, S202 `hyprland/window.cpp`. None is `workspaces.cpp`.
- `grep -nE 'round-37|S213\.receipt|hyprland\.log|journalctl|debug:disable_logs'` → **no output**.
- Cross-lane, informational only (the `shared` mode never fails): `grep -lE 'Waybar/0\.15\.0/src/modules/hyprland/workspaces\.cpp|src/debug/log/Logger\.cpp' */corpus/SOURCES.md` → no lane.

So under the `url_of` key: S212 `raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp` and S214 `raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/log/Logger.cpp` are both new, so **no W04 and no E04**. S213 is own-work with a repo path and no `http(s)` URL in the source cell, so `u==""` and it is outside the duplicate check entirely.

Receipts (renumber-map prefixes confirmed):
- `sha256sum`: S212.bin `1e19d926…3f97d7e9`, 41392 B; S214.bin `d04e3a2f…eaf6b868`, 1789 B; S213.receipt.txt `1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58`.
- `git ls-files --error-unmatch` lists all three, so they are tracked.

## 4. Falsifier harness — each rule shown able to fail (`harness.out`)

The PLACEHOLDER rows are inserted after `:213`, inside the Registry section. The run is `validate --today 2026-10-25 --file <mirror>`; the 7 baseline W04 lines are filtered out, and the count of 7 is re-checked on every case.

| case | result |
|---|---|
| A — S212/S213/S214 well-formed, used-by files present | `file ok`, rc=0, rows=204 |
| B — same, used-by entries absent (**today's lane state**) | `E11 S212 missing used-by corpus/knowledge/event-delivery-limits-r26.md`, `… event-queue-observability-r37.md` ×3, rc=1 |
| C — appended at end of file (after `## Leads`) | `E12 S212 row outside Registry section` (and S213, S214), rc=1 |
| D — a `\|` inside one cell | `E01 S212 fields=12`, rc=1 |
| E — id reuses S211 | `E03 S211 duplicate id`, rc=1 |
| F1 — new row for S189's URL, same scope, no supersedes | `E04 S215 duplicate url …/EventManager.cpp within scope …`, rc=1 |
| F2 — F1 with `supersedes S189 —` | `ok`, rc=0 |
| F3 — S189's URL, different scope | `W04 S215 … across scopes` then `ok`, rc=0 |
| G — used-by joined with `;` | `E11 S212 missing used-by …r26.md; …r37.md`, rc=1 |
| H — opened 2026-10-26 / recheck `90 days` / recheck `on-release` | `E08 S212 opened=2026-10-26`, `E09 S213 recheck=90 days`; `on-release` passes |
| I — Logger.cpp again as `github.com/…/blob/v0.56.2/…`, other scope | `ok`, **no W04** (normalisation blind spot) |
| J — S214's URL plus `#L15-L16`, other scope | `W04` (fragment stripped) |
| K — S212 indented 4 spaces | **`ok`, rc=0, rows=203**: the row silently vanishes |
| L — status `watch` / kind `receipt` / community at A | `E07`, `E05`, `E10` |
| N — S212 missing its trailing pipe | `E01 S212 fields=10` |
| O — mined row with used-by `—` | `W03 S214 mined but unused`, rc=0 |
| P — `queued` rows citing absent files | **`ok`, rc=0**: E11 never inspects queued rows |

The frozen CORPUS.md manual census on the mirror (`manual.out`): case A → `rows: 204`, `malformed: 0`, `dup-ids: []`, `enum: []`, `missing used-by: []`. Case G (`;` separator) → `missing used-by: []`, so **the frozen manual check accepts what the maintained script rejects (E11)**. Case G2 (one bogus path) → `missing: corpus/knowledge/nope.md`.

## 5. Pass conditions the L1 must meet

For each new row (S212, S213, S214):
1. **Ids.** Exactly S212, S213, S214, unused and never renumbered (E02/E03). The renumber map already binds these ids to these documents.
2. **Placement.** Column zero (0–3 spaces at most) and inside `## Registry`: between `:213` (S211) and `:215` (`## Paths`), never at end of file (E12, case C). After the append the row count must read **204**: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`. A count of 203 with validate `ok` means a row was indented away (case K).
3. **Shape.** 11 cells with leading and trailing pipes, so NF=13. No `|` anywhere in a cell, including code quotes from `Logger.cpp`/`workspaces.cpp` such as `||` (E01, cases D and N).
4. **Enums.** `kind`: S212 and S214 `code`, S213 `own-work` (E05). `tier` is one of A/B/C; A is legitimate for tagged source and for the lane's own re-runnable receipt (`CORPUS.md:94-96`) (E06). Never `community` at A (E10). `status` is one of queued, mined or rejected (E07).
5. **Dates.** `opened` = `2026-10-25` (not after today, UTC) (E08). `recheck` is `NNd`, a valid ISO date, or a symbolic word such as `on-release`; never `90 days` (E09).
6. **Source cell.** S212 and S214 carry their canonical URLs in the *source* cell; `url_of` reads no other cell. Keep the raw-commit form already used by S158/S189, because a later `blob/v0.56.2` form of the same file would not be flagged (case I). S213's source cell is the repo path `.ufo/waves/round-37/fetch/S213.receipt.txt`, following S210's pattern. Do not put a URL there.
7. **Anchor.** An exact line and revision: commit `efb50993780079460b0cbed1363e2166a2de1d9f` / tag `0.15.0`, plus the bytes and sha256 prefix, as S189 and S201 do. This is a contract rule (`CORPUS.md:99-100`); the census does not check it.
8. **used-by and status (the ordering gate).** If `mined`, every path must exist on disk *before* validate runs (E11). Today `ls` reports both `corpus/knowledge/event-delivery-limits-r26.md` and `…/event-queue-observability-r37.md` as "No such file or directory". So land the knowledge entries first, or in the same change. Separate paths with **commas only**: `;` passes the frozen manual census but fails the script (case G). Do not mark rows `queued` to avoid E11 while they are cited, because `queued` means not yet cited (`CORPUS.md:103`) and the census will not catch it (case P). `mined` with `—` gives W03 (case O).
9. **Gate (Rule 1, not census-checked).** `corpus/lessons/round-37.md` does not exist yet (`ls corpus/lessons | grep round-3[67]` → only round-36 files). Its `## Gate` must record, per new row, the URL (or receipt path), the access date 2026-10-25, a quote of 25 words or fewer with its location grounding `teaches`, and the sha256 of the committed receipt.

For the held rows S189 and S201 (`used-by` extended in place):
10. Only `used-by` may change, and possibly `status`/`recheck`. `opened` stays `2026-10-24` even though both were re-opened 2026-10-25 (Rule 2). Log each change old→new in the round-37 lesson. Current old values: S189 `corpus/knowledge/ipc-contract-r25.md`; S201 `corpus/knowledge/waybar-module-text-route-r25.md`. Append the new path with `, `; the E11 condition in item 8 applies to it.
11. Do not add a fresh row for `EventManager.cpp` or `backend.cpp`. With the same scope it is E04 unless `teaches` opens `supersedes S189 —` / `supersedes S201 —` (cases F1 and F2); with a different scope it is W04 (case F3).

Final acceptance: `bash scripts/sources-census.sh validate mado` (fleet root) must give rc=0, no `E` line, a closing `mado ok …`, and exactly the **same 7 W04 lines** as the baseline (S030, S042, S045, S097, S119, S120, S121). Any new W04 means a planned URL was registered twice under different scopes.

## 6. Residual risk and verification gaps

- The census cannot see: whether `teaches`/`anchor` are grounded; whether the Gate block exists; whether `opened` was rewritten on S189/S201; a `queued` status misused (case P); or a URL that differs only in host/blob form (case I). These rest on the Gate and a non-author spot-check.
- Script/contract divergence: the `used-by` separator is `[,;]` in the frozen CORPUS.md block but `,` in the maintained script. This is a finding for the fleet census owner, outside lane scope.
- I did not draft row content, read Logger.cpp/workspaces.cpp for quotes, or verify `Logger.cpp:15-16,:48`; other seats own those.
- Tool note: the Read tool refused `scripts/sources-census.sh` lines 1–399 ("exceeds maximum allowed characters" for a 35,466 B file), so lines 1–200 were paged with `awk 'NR>=1 && NR<=200'`. Lines 201–399 (the selftest body) were not read; the `selftest ok` run stands in for them.
