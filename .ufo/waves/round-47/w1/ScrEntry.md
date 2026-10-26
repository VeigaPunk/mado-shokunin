# ScrEntry — round 47 w1 (BUILD), C2 entry draft: `corpus/knowledge/xdg-terminal-selection-r47.md`

Seat: ScrEntry (leaf; no subagent dispatch). Lane: mado-shokunin. Base 60edb66e2f1cb90acc6e9442fc93ded0ca42d750.
Deliverable: a draft knowledge entry at `.ufo/waves/round-47/w1/ScrEntry/entry.md`, ready for the L1 to land as
`corpus/knowledge/xdg-terminal-selection-r47.md`. Status: **draft complete**, locator and quote gates green.

## 1. What the entry contains

Provenance head in the lane's shape (`source:` rows, `verified-at:`, `recheck:`, `ground:`, `Lane/Round`), then:

- **What the evidence licenses** — 9-row table mapping each question to the step that answers it.
- **The chain, step by step** — 7 numbered steps, each citing computed script line ranges:
  1. lists and their order (`make_paths`, :143-177; config sequence :148-163, data-dir sequence :157-163, applications dirs :166-169, cache path :172-173, desktop lowercasing :1144)
  2. list lines (`read_config_paths`, :351-475; five directives :374-421, entry-ID arm :425, `+`/`-` markers :427-437, first-`:` split :435-438, validate :439, add :442, exclude :462, discard :467)
  3. desktop-file ID lookup (`find_entry_paths`, :754-800; find args :762-773, single `find -L` :795, awk ID derivation :797, alias registration :779-790)
  4. entry validation (`check_entry_key` :802-968 and `read_entry_path` :970-1018; per-key arms Categories :816, Actions :829, OnlyShowIn :846, NotShowIn :865, TerminalArg* :885-931, TryExec :933, Hidden :938, Exec :947; expander :501-559, tokenizer :561-692, `%`-field stripper :694-740; action group :1005-1014)
  5. selection (`find_entry` :1055-1111; sentinel :1071-1074, alias skip :1081, eval :1083, unalias :1085, `Exec` non-empty :1088, `TerminalEmulator` :1090, compat/strict :1092-1100, store :1103-1105, failure :1109 + :1208)
  6. exec-arg composition (option loop :1224-1321; per-group prepends :1387-1452 in the order execarg, hold, dir, title, appid, Exec; `=`-fusing :1403, split-valued :1407/1422/1437; missing keys dropped :1396-1398/1426-1428/1441-1443; `--dir` fallback `cd` :1494-1497; `exec "$@"` :1499)
  7. print modes (fixed output order :1327-1366; `--print-id` :1331, path `/./` strip :1342, path+action :1349, content :1362, end-of-run newline rule :1368-1385, `--print-cmd` :1468-1490)
- **The cache, separately** — hash contents (:179-215, `4` version at :194, `ls -LRl` at :200), 10 header records + USEP command (:217-298), validity test (:274), save/fork/umask (:300-340, :303, :312-316, :1457), default on (:1172, :1179), README caveat (:295-311).
- **Observations** — 6 OBS rows on S326/S327.
- **Census of the pinned bytes** — `script_lines=1499 functions=23 directives=5 print_data_kinds=4 cache_header_fields=10 cache_hash_format=4 data_side_list_slots_per_data_dir=2`.
- **This host** — static verified shape (hotkey locator, 8 config slots, which slots exist) plus 7 `<LIVE:*>` placeholders for the values the L1 fills from the landed tool's receipt, and the explicit statement of how steps 1+3 answer the round-17 `[UNK]`.
- **Reading a discard or a DIFFER** — 5 diagnostic rules.
- **Limits** — 7 rows, including the `find`-order caveat and the remaining `[UNK]` (`omarchy-cmd-terminal-cwd` value at launch time).

No session material and no home-directory listing is committed: the entry names at most single quoted paths
(`~/.config/xdg-terminals.list`, `~/.config/hypr/bindings.conf:2`, the user `Alacritty.desktop` as a path class); `grep -c '/home/' entry.md` = 0.

## 2. Gates run (commands and outcomes)

| gate | command | outcome |
|---|---|---|
| pin integrity — host binary vs upstream tag | `curl -sS -o upstream-xte.sh https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec && sha256sum upstream-xte.sh /usr/bin/xdg-terminal-exec && cmp upstream-xte.sh /usr/bin/xdg-terminal-exec` | both sha256 `89f2be9a…3127ac`, `cmp` silent → **BYTE-EQUAL** |
| README pin | `curl …/v0.14.3/README.md` → `.ufo/waves/round-47/w1/ScrEntry/README-v0.14.3.md` | 337 lines, sha256 `c7a1a8bb…5a9d40` |
| every cited line number | `python3 verify_locators.py` (119 assertions: cited line contains the expected token, in the script and the pinned README) | **119 checked, 0 mismatched** (`locators.txt`) |
| every quote | `python3 verify_quotes.py` (each quote: present in the pinned range, present in `entry.md`, ≤ 25 words) | **10/10 passed** (`quotes.txt`); longest prose quote 16 words, code quotes 1-9 tokens |
| read-only host probe | `XDG_CACHE_HOME=$S/cachehome /usr/bin/xdg-terminal-exec --print-id --print-path --print-cmd` (`$S` = scratch) | rc 0, three lines, no terminal launched; cache `0600`, 188 bytes (`receipts/live-print.txt`) |
| cold-cache trace | `XDG_CACHE_HOME=$S/cache2 XTE_CACHE_ENABLED=0 XTE_DEBUG=1 … --print-id 2>trace2.txt` | 627-line stderr trace; 8 `reading config` lines in step-1 order; trimmed copy in `receipts/trace-cold-cache.trimmed.txt` |

Every script line number in the entry was produced by `grep -n`/index lookup on the pinned bytes and then re-checked by
`verify_locators.py`; no locator was typed from memory (three early off-by-ones were found and fixed this way:
`find_entry_paths` exclusion test :785, `eval` alias :1083, `--print-path` action suffix :1349).

## 3. Live values observed by this seat (read-only, cold cache, scratch `XDG_CACHE_HOME`)

These are **my** observations, recorded so the L1 can cross-check the landed tool's receipt; they are not the
instrument the predicates will freeze. `XDG_CURRENT_DESKTOP=Hyprland`, `XDG_CONFIG_DIRS=/etc/xdg`,
`XDG_DATA_DIRS=/usr/local/share:/usr/share`, `XDG_CONFIG_HOME`/`XDG_DATA_HOME` set.

- `--print-id` → `Alacritty.desktop`; `--print-path` → `/home/vgpnk/.local/share/applications/Alacritty.desktop`;
  `--print-cmd` → `alacritty`; rc 0.
- Second run with the same `XDG_CACHE_HOME` → identical output, and **no** config reading in the DEBUG trace (warm cache).
- Composed command probe: `--print-cmd --dir=/tmp --title=hello --app-id=foo --hold echo hi` →
  `alacritty`, `--class=foo`, `--title=hello`, `--working-directory=/tmp`, `-e`, `echo`, `hi` (one line per word, rc 0).
  This fixes the empirical order `[Exec] [AppId] [Title] [Dir] [Hold] [ExecArg] [command…]`.
- Trace facts: the ID is registered twice (`/usr/share/applications/./Alacritty.desktop` at trimmed-trace:17, then the
  user copy at :19) and the entry actually read is the **user** copy (trimmed-trace:23-24) - the alias map's
  last-registration-wins rule of step 3, i.e. the round-17 `[UNK]` at `corpus/knowledge/terminal-route-r17.md:144-145`
  resolves to "the user override is what the resolver picks, while the printed ID names neither file".
- Only one of the eight config slots exists on the data side (`/usr/share/xdg-terminal-exec/xdg-terminals.list`, the
  distro default with exclusions and `/execarg_default` rows and no plain entry line); the selecting list is the user
  `~/.config/xdg-terminals.list`; `~/.config/hyprland-xdg-terminals.list` and both `/etc/xdg` slots are absent. The
  trimmed trace also prints the two resolved path lists (trimmed-trace:4-5): the eight config slots in step-1 order and
  the applications dirs as `/usr/share/applications/`, `/usr/local/share/applications/`,
  `~/.local/share/applications/` - the ascending preference order of step 1, which is why the later registration wins
  the alias.

## 4. Findings that bear on the frozen predicates (C1 counter / the w2 attack)

1. **Fallback order is `find`'s readdir order.** The fallback list is built by one `find -L` over three applications
   dirs (:795) with no `-sort`; README:179-180 leaves that order undefined. A Python reimplementation must reproduce
   GNU find's traversal, or fixtures with two valid terminals in the same directory can differ while both are "right".
   Safer fixture shape: name the entry explicitly in a list file, or keep exactly one valid entry per data dir.
2. **Print modes still touch the cache.** `--print-id/--print-path/--print-cmd` run the full selection and fork
   `save_cache` (:1457) before printing. A tool that models a cold cache must not be tripped by the resolver's cache
   file appearing; conversely the counter should always pass a fresh `XDG_CACHE_HOME` to the real script (as the claim
   states) or the second fixture in a run can be answered from a warm cache.
3. **`--print-path` is not the find path verbatim**: the `/./` marker is stripped (:1342) and `:action` may be appended
   (:1349). A byte-identical reimplementation must reproduce the strip, including the degenerate cases where the path
   contains `/./` more than once.
4. **Delimiters are printf sequences, not literals**: both default to the two characters `\n` and are emitted with `%b`
   (:1222-1223, :1344, :1478), so `--print-cmd='|'` joins with a literal `|` and `--print-delimiter='\x1f'` depends on
   the shell's `printf`. Start/end newline rules differ between "no cmd" (:1368-1385) and "cmd" (:1486-1490) modes.
5. **`--print-content` exits before any trailing-newline rule** (:1354-1366) and prints the file as-is.
6. **Exit statuses**: 0 for every print mode; 1 when no entry validates (:1109, :1208) with the searched applications
   dirs on **stderr**. The tool's own 3/2/1 contract (NO_TERMINAL/usage/DIFFER) therefore cannot be derived from the
   script's status — the counter must compare `print` stdout+rc against the script and treat `explain` separately.
7. **`command -v` is shell-dependent** (:936, :964): builtins, functions and aliases of the executing shell would satisfy
   it. Fixtures that stub a binary in `$ROOT/bin` are safe; a fixture that relies on a shell builtin would be a trap.
8. **Compat vs strict is an input**: `XTE_EXECARG_COMPAT` (default true, :1147) decides whether an entry without
   `TerminalArgExec` still qualifies with `-e` (:1092-1100, :746, :1113-1140). Fixtures must pin it if they care.
9. **Option parsing swallows things silently**: unknown `-*` options are discarded (:1317-1320); `--`, `-e` and the
   entry's own exec argument end option processing and are dropped (:1226-1235). Any `print` invocation whose arguments
   include a leading `-e` will therefore behave differently from the naive reading.
10. **`--dir=` is invisible in `--print-cmd` when the entry has no `X-TerminalArgDir`** (:1411-1413, :1494-1497): the
    resolver `cd`s instead. A fixture expecting a dir argument in the printed command is wrong for such an entry.

## 5. Touched surfaces

Written (all inside the seat directory):

- `.ufo/waves/round-47/w1/ScrEntry/entry.md` — the draft entry (21,069 bytes, 7 steps, 8 `<LIVE:*>` placeholders)
- `.ufo/waves/round-47/w1/ScrEntry/README-v0.14.3.md` — S327 pin (also the only file in the seat dir that must move)
- `.ufo/waves/round-47/w1/ScrEntry/pins/xdg-terminal-exec-v0.14.3.sh`, `pins/PINS.txt` — S326 pin + provenance
- `.ufo/waves/round-47/w1/ScrEntry/receipts/live-print.txt`, `receipts/trace-cold-cache.trimmed.txt`
- `.ufo/waves/round-47/w1/ScrEntry/verify_locators.py` + `locators.txt`, `verify_quotes.py` + `quotes.txt`
- `.ufo/waves/round-47/w1/ScrEntry.md` — this report

Not touched: any tracked lane file, `corpus/SOURCES.md`, the fleet repo, sibling lanes, `templates/`, `scripts/`,
`MANIFEST.json`, `.ufo/state/`, `.scratch/`, the jj/git index, `~/.config`, `~/.local/share`, `/usr`, `~/.local/bin`.
No git/jj mutation, no pacman, no package transaction, no process other than the reads above, no terminal or GUI
launched, no compositor mutation (`hyprctl version` only).

## 6. Out of scope / handed to the L1

- **SOURCES rows are not appended** — `corpus/SOURCES.md` tops at S325; this seat proposes S326 (script pin) and S327
  (README pin) with the anchors in `pins/PINS.txt`. The L1 owns the append and the `used-by` cell.
- **The README pin lives in the seat dir**; at integration it belongs with the round's other pins (round 46 used
  `.ufo/waves/round-46/fetch/`), and the `source: S327` path must be updated to wherever it lands.
- **`## This host` placeholders** are for the L1's landed-tool receipt; my §3 values are a cross-check only, and I did
  not run `tools/mado-terminal.py` (C1 is another seat; it did not exist in a landed form while this seat ran). If the L1
  prefers to carry my cold-cache run as the live row instead, `receipts/live-print.txt` and
  `receipts/trace-cold-cache.trimmed.txt` back it - but it is not the frozen instrument, so the placeholders stand by
  default.
- **Not examined**: `uwsm-app`, `omarchy-cmd-terminal-cwd` (the round-17 `[UNK]` about the `--dir=` value stays open),
  Hyprland's `exec` path, Alacritty's own argument handling, the proposed-spec text on the gitlab MR.
- Deliberately held ground: `terminal-route-r17.md` (S056-S060), `terminal-trees-r23.md`,
  `corpus/knowledge/terminals-and-omarchy.md` — none re-claimed; this entry only closes the launched-choice `[UNK]`.

## 7. Cross-seat wiring (after the C2 counter draft read the entry)

`ExecCounterC2` preview-scored `entry.md` with `.ufo/waves/round-47/w1/ExecCounterC2/c2-r47-terminal-entry.py`
(verdict: ADMITS - 13 quotes verified at their stated pin ranges, 7/7 steps cite the script pin, 4/4 ground terms) and
asked for three wiring changes, all applied and re-gated:

1. **Head rows carry a ref-pinned URL.** S326 now leads with
   `https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec` and S327 with the matching
   `README.md` URL, both at tag v0.14.3, with the pin path and sha256 kept beside them (`grep -c raw.githubusercontent.com…/v0.14.3`
   = 2).
2. **Quote-then-locator adjacency held everywhere.** One exception was repaired: step 6's
   `set -- "$XTE__EXECARG" "$@"` now has `(xdg-terminal-exec:1389)` immediately after the span instead of after an
   intervening phrase. All ten quotes remain in the `<quote>, <pin-locator>` / `<quote> (<pin-locator>)` form, so the
   counter can match them by name against the committed fetch pins.
3. **The live-receipt path is cited on the round-17 line.** Both the `ground:` line and the `This host` sentence that
   carries `terminal-route-r17.md:144-145` now point at `.ufo/waves/round-47/receipts/<LIVE:live-receipt>`, and the
   sentence states the receipt's contract: `observed=<capture>`, the host `XDG_*` lines, and exactly one
   `MADO_TERM: selected=… path=… verdict=…` line produced by `tools/mado-terminal.py explain --observed`. A table row
   for the receipt was added. **The basename stays a placeholder on purpose**: this seat's write scope is its own
   directory, so it cannot create `.ufo/waves/round-47/receipts/`; the L1 (owner of that receipt and of the landed tool)
   fills the name at integration.

Gates re-run after the edits: `verify_locators.py` 119 checked / 0 mismatched, `verify_quotes.py` 10/10 passed.

Measured back by the counter: with a preview clone (pins under `.ufo/waves/round-47/fetch/`, a clause-f-shaped
receipt, the tool doubled) the entry scores `admitted=1/1`, 14 quotes verified at their pin ranges, 7/7 steps
script-cited (`receipts/preview-real-drafts.txt` in its seat); the as-is placeholder form fails clause f with
`no_r17_receipt_line` (`receipts/entry-as-is-placeholder.txt`), because its receipt regex only accepts a real name after
`.ufo/waves/round-47/receipts/`. That is integration, not text: I refused to type a receipt filename I cannot create.

### Integration checklist for the L1 (three edits, then the clause passes)

1. Create `.ufo/waves/round-47/receipts/<name>` from the landed tool: it must hold `observed=<capture>` (the captured
   `--print-id --print-path --print-cmd` output), the host's `XDG_CURRENT_DESKTOP`/`XDG_CONFIG_DIRS`/`XDG_DATA_DIRS`/
   `XDG_DATA_HOME`/`XDG_CONFIG_HOME`/`HOME`/`PATH` lines, and exactly one `MADO_TERM: selected=… path=… verdict=…` line
   from `tools/mado-terminal.py explain --observed <capture>`.
2. Replace all three `<LIVE:live-receipt>` occurrences in `entry.md` (the `ground:` line, the placeholder table row, the
   `This host` sentence) with that basename; the rest of those lines already reads correctly with a concrete name.
3. Put the README bytes at `.ufo/waves/round-47/fetch/README.md` and make S327's pin path that fetch path (the only
   seat-relative path left in the entry); fill the remaining `<LIVE:*>` values from the same receipt. The counter
   measured that **no second copy is needed**: a `README-v0.14.3.md` locator resolves to the fetch copy by unique stem,
   and the quote pin is accepted as cited when its bytes equal a row-cited pin's sha - so the entry's
   `README-v0.14.3.md:179-180` / `:300-301` locators keep working either way.
Those three edits are counter-measured to be exactly what its clause c/f/g/h check: a real receipt name on the line
carrying `terminal-route-r17.md:144-145`, the tool at `tools/mado-terminal.py`, the S327 README row, S056-S060
untouched, and head rows URL-pinned. Nothing else is asked of this seat, and the counter's own run admitted the entry
1/1 once those were in place.

## 8. Tooling

No installs or upgrades (nothing was missing: `python3` stdlib, `curl`, `coreutils`). Scratch dir
`/fast/scratch/hyaku/mado-r47/ScrEntry` held the fetched upstream copy, the cache homes and the untrimmed trace; the
two receipts above were copied into the seat dir first, then the scratch dir was removed. No `/tmp` path is cited.
