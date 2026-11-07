# R92MScribeEntry — the C1 knowledge entry for `xdg-mime query default`

Seat `R92MScribeEntry`, mado round 92, wave w1, base revision `d992ef7494b054591ee9104df1da49264678df5d`.
Assigned deliverable: draft the C1 knowledge entry at
`.ufo/waves/round-92/build/xdg-mime-default-resolution-r92.md`, in the shape of
`corpus/knowledge/mime-default-resolution-r91.md`, with the content list in the seat item. No measurement:
the C1 counter runs after the freeze; every behavioural number below is labelled DRAFT.

## Behaviour delivered

Two files carry the deliverable:

- `.ufo/waves/round-92/build/xdg-mime-default-resolution-r92.md` (sha256
  `a1eeab93a2591cddd5936231a8741295d83e7a013ff1046ea30e0c98f285d060`, taken after the last edit): 332 lines,
  10 sections, 31-row decision table, 95 distinct labelled L1 case ids cited (of the 128 in
  `.ufo/waves/round-92/controls/xdgmime-cases-r92-l1.json`).
  - Front matter: `source:` S508 (provisional; `xdg-mime.in` 11e7d91e…, `xdg-utils-common.in` 1f6969b5…),
    S509 (provisional; `xdg-open.in` a6b0c7af…, installed xdg-utils 1.2.1-2 `/usr/bin/xdg-mime` a587107f…),
    `covers:`, `verified-at:` (the DRAFT replay, explicitly not the measured receipt), `recheck: 90d`.
    S490 is *not* cited: it is a rejected row and this entry makes no exit-status-as-termination-cause claim.
  - §1 when `xdg-open` asks (`open_generic_xdg_mime`, xdg-open.in:392-395, called from :489 and, for a
    scheme, :507-508/:414-419, both behind `has_display` :485/:507) and which DE values reach it: unknown
    desktop → empty `DE` → `generic` (:593-597, :664-665), plus the seven `open_*` fallbacks (:177, :194,
    :213, :232, :251, :266, :543); `detectDE`'s mapping and classic fallbacks (common:283-377); xdg-mime's own
    dispatch to `defapp_generic` / `defapp_kde` / `defapp_lxqt` (xdg-mime.in:712-729).
  - §2 the four-pass search order (config dirs, data dirs + `/applications`, grep fallback, `MimeType` scan).
  - §3 the per-directory file and group order, the awk state machine, first-match-per-file, prefix at column 0,
    CRLF, `;`-list splitting, pathname expansion of ids, and the raw printed id.
  - §4 `desktop_file_to_binary`: vendor split (`${desktop%-*}` / `${desktop#*-}`), subdir order, first-read
    wins and returns, first `Exec` word via `read`, `command -v`, `xdg_realpath` as an `[ -e ]` test.
  - §5 the `defaults.list`/`mimeinfo.cache` grep fallback (BRE, unanchored, `head -n 1`, `cut` quirks,
    `echo` options, no install check).
  - §6 `defapp_fallback` (`MimeType` scan, `InitialPreference`, word splitting, no install check).
  - §7 exit status and stdout (0 with or without an answer, 1 malformed type, 3 LXQt; `--version` scanned
    over every argument).
  - §8 the 31-row decision table against GLib 2.90.1, each row naming its L1 case id.
  - §9 the tool's scope refusals and assumptions; §10 argv and output format.
- `.ufo/waves/round-92/w1/R92MScribeEntry.md` — this report.

Supporting DRAFT artefacts (allowed by the item's "copying anything you cite into …/w1/"):

- `.ufo/waves/round-92/w1/R92MScribeEntry-draft-check.txt` — the DRAFT receipt: input digests, the three
  source digests, both comparison summaries, the 68 divergent rows, and the provenance-bridge result.
- `.ufo/waves/round-92/w1/R92MScribeEntry-toolcmp.py` (sha256 `73e4d129…`) and
  `.ufo/waves/round-92/w1/R92MScribeEntry-cmp-glib.py` (sha256 `7a0943ba…`) — the two DRAFT drivers.

## Gates run

No counter was run: the item does not ask for it and the draft-scoring rule reserves the measurement for after
the freeze. Everything below is labelled DRAFT.

| # | command | exit | result |
|---|---|---|---|
| 1 | `curl -fsSL …/v1.2.1/scripts/{xdg-mime,xdg-utils-common,xdg-open}.in` then `sha256sum *.in` | 0 | 11e7d91e…, 1f6969b5…, a6b0c7af… — all three equal the pins in the seat context |
| 2 | `xdgmime-oracle-r92.py label --in <copy of d17,d19> --out … --scratch …` | 0 | labels unchanged (`x.desktop`, `x.desktop`) |
| 3 | `python3 -I toolcmp.py` (candidate vs the 131 labelled rows) | 0 | `DRAFT_TOOL_CHECK rows=131 mismatches=0` |
| 4 | `python3 -I cmp-glib.py` (round-91 GLib resolver vs the same fixtures) | 0 (after a guard) | `cases 128 rows 131 differ 70 errors 2`; 68 real divergent rows, 2 harness argparse errors on types beginning with `-` (s06, s08) |
| 5 | function-block comparison `.in` vs `/usr/bin/xdg-mime` | 0 | 12 cited functions byte-identical; `exit_failure_syntax` differs only in its `@NAME@` strings |

Run 4's first form exited 1 in its own print loop (KeyError on the two error rows) after writing its JSON; the
guarded re-run exited 0 and changed no count. Both are recorded in the DRAFT receipt.

Verification deliberately not performed: no `--draft-tool` counter run, no fresh/fuzz/mutant leg, no write
under `.ufo/waves/round-92/receipts/`, no touched file outside my scope.

## Touched surfaces

Written (5 paths, all named above): the entry under `build/`, and four files under `w1/` (this report, the
DRAFT receipt, the two DRAFT drivers). Nothing in `tools/`, `quality/`, `corpus/`, the candidates, the
controls, the declaration, `.ufo/state/`, or the fleet root. No git/jj mutation anywhere; reads only.

## Out of scope (explicitly not done)

- C1 measurement: the counter, the fresh leg, the mutant leg, the controls, the oracle-agreement leg.
- `SOURCES.md` rows S508/S509 — the entry carries provisional ids and the L1 binds them at the freeze.
- Landing the tool at `tools/mado-xdgmime.py`; the entry describes it as landing from the candidate after
  the freeze.
- C2 (`quality/check-seat-reports.py`, its battery, mutants, counter) — a different seat.
- `query filetype` / MIME sniffing, `xdg-open`'s launch path, portals: named as out of scope in the entry.

## Findings for the L1

1. **Stale premise count.** `claims-declaration-r92.md` says the GLib resolver scores "56/123 of the draft
   cases"; the frozen L1 file holds 128 cases (131 type rows). If 128 is the freeze, the declaration's
   sentence and the counter's `cases`/`--expect-cases-sha256` expectation must be reconciled; I changed no
   number anywhere.
2. **`.in` vs installed bytes.** `/usr/bin/xdg-mime` is 1794 lines (common inlined, `@NAME@` substituted)
   against 1079 + 463 upstream lines, so its line numbers do not match the tag's. The entry cites `.in` line
   numbers and now states the bridge: `defapp_generic`, `check_mimeapps_list`, `defapp_fallback`,
   `defapp_kde`, `defapp_lxqt`, `search_desktop_file`, `desktop_file_to_binary`, `detectDE`, `first_word`,
   `has_display`, `xdg_realpath`, `exit_success` are byte-identical between the two on 2026-11-06.
3. **Fixtures hide modes in a plain `text` dump.** `d17-exec-relative-cwd` resolves only because `run.sh`
   carries `"mode": "755"`; a reader that lists only `text` (as I first did) will model the case wrongly.
   Same trap in `d19`, `d35`, `d36`. Worth a note for the critic seat.
4. **A real gap not covered by any L1 case.** `check_common_commands "$@"` scans *every* argument
   (common:232-260), so `xdg-mime query default text/plain --version` prints `xdg-mime 1.2.1` and exits 0,
   while the candidate answers per type. `s08` only exercises `--version` as the sole argument. The entry
   states this as a known limit rather than a claim; a case for it belongs to a later round, not this freeze.
5. **Dead line in the target.** `xdg-mime.in:728` (`exit_failure_operation_impossible`) is unreachable
   because both `defapp_*` branches exit; recorded in the entry so no one models a 3 for "nothing found".
6. `case s01` and `case s02` fix a boundary the round-91 knowledge entry cannot express: the same fixture
   answers `null`/rc 3 on LXQt and `a.desktop` under GLib (§8 rows 31 and the §1 note on `KDE_SESSION_VERSION`
   being unset).

## Installs and host effects

None. No pacman, no uv/npx, no binary written into any `PATH` directory, no service touched, no sudo. Host
reads stayed inside the MIME/desktop-entry chain and the lane repo; `/usr/bin/xdg-mime` was executed only as
`query default TYPE`, through the frozen oracle's own runner, against `env`-built fixture roots. Three
read-only `curl` fetches from `gitlab.freedesktop.org` (official upstream raw tag paths).

## Scratch

`S=/fast/scratch/hyaku/mado-r92/R92MScribeEntry` — held the three fetched `.in` files, the two DRAFT drivers,
their working dirs and two one-case oracle probes. Everything cited was copied into `w1/` first; the
directory was then deleted and `ls` confirms it is absent (no scratch remains).
