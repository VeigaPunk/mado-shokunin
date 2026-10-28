# Round 56 — registration (mado, hyaku run 11, attempt 1)

Companion to `claims-frozen.md` (the frozen predicate sentences, targets and kill rules). This file defines every leg, grammar
and control the predicates name. It, `frozen-tables.json`, `fixtures/c2/`, `ctl/`, `fetch/`, `freeze-verify.py` and
`receipts/` are committed in ONE freeze commit BEFORE any wave `.ready`. A predicate found unsatisfiable or wrong is an honest
stop or a pre-data re-registration in a NEW versioned file; this file is never edited. Counters are read as written: when the
text is ambiguous the most literal reading wins and the seat lists the ambiguity.

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base (lane tip at freeze): the `base` field of `frozen-tables.json`.
All counters and harnesses: `python3 -I`, read ONLY git objects at `--rev` of `--repo` (`git cat-file`, `git show`,
`git ls-tree`; never the working tree), honour `--work DIR` (created when missing; HOME and TMPDIR of every git child; the
counter itself writes nothing), embed the sha256 of `frozen-tables.json` as a constant and check it against the blob at
`--rev`, print exactly one result line on stdout, exit 0 only on `TARGET_MET`/`OK`, 1 on a miss, 2 on a setup error (reason
on stderr, nothing on stdout). Only regular blobs (modes 100644, 100755) are accepted for entry/registry/pin/tables files; a
symlink blob or a path crossing a symlinked directory is "absent". A harness runs counters as child processes with a scrubbed
`GIT_*` environment and `TMPDIR`=`--work`, builds scratch repos as `D=$(mktemp -d -p <work>) && git -C "$D" init -q` with every
later git call naming `-C "$D"` (assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; identity
via `-c user.name=ctl -c user.email=ctl@ctl`), and never writes the lane or the fleet repo. Declared limit (carried from
round 55, QUALITY 104/105/106): a counter that sniffs its environment, caches runs or forges a consistent tree passes a
non-adversarial harness; the harness is evidence against a counter that prints green without work.

## §C1 — autoreload entry (coverage, sourced)

Entry: `corpus/knowledge/hyprland-config-autoreload-r56.md`. Pins: `.ufo/waves/round-56/fetch/` (sha256 in
`frozen-tables.json` `c1.pin_sha256` and `c1.host_pin_sha256`). Commit pinned: `efb50993780079460b0cbed1363e2166a2de1d9f`
(Hyprland v0.56.2, the host's running build, `fetch/host-version.json`).

**Row grammar.** A row is a line outside fenced code blocks (``` or ~~~, 0-3 leading spaces) and outside HTML comments whose
first cell is an id `K01..K30` or `H01..H03`. It must be exactly
`| <id> | <proposition> | <src> | <pin>:<line> | ` + "`" + `<quote>` + "`" + ` |` — single spaces around every pipe, no trailing byte,
exactly 5 cells split on the 3-byte separator ` | `, no `|` and no backslash-escaped pipe inside any cell (no frozen quote
contains `|`; `freeze-verify.py` proves it). `<src>` is `S###` (K rows) or the word `host` (H rows). `<pin>:<line>` equals the
frozen pin file name and line byte for byte. The quote cell is a single backtick, the frozen quote, a single backtick. The
proposition is >=40 characters (K) / >=20 (H), has no leading or trailing whitespace, and is not byte-identical to another
row's proposition. A missing, duplicated or malformed row is leg `row:<id>`.

**Legs** (every failing leg is reported, never only the first):

| leg | holds when |
|---|---|
| `entry_absent` | the entry path is a regular blob at `--rev` (else all entry-dependent legs are not evaluated; rows/hosts/sources/scope/content print 0) |
| `tables_sha` | the blob `.ufo/waves/round-56/frozen-tables.json` at `--rev` has the embedded sha256 |
| `prov` | the first 30 lines hold a line starting `source:`, one `verified-at: 2026-10-28` and one starting `recheck:`, in that order; every `S###` on the `source:` line(s) is a registry row; and the `source:` set contains every S-id cited by a K row |
| `index` | `corpus/README.md` holds exactly one line starting `| ` + backtick + `knowledge/hyprland-config-autoreload-r56.md` + backtick |
| `row:<id>` | the row grammar above holds |
| `quote:<id>` | the frozen quote is a substring of line `<line>` of the pin blob at `--rev` (K and H) |
| `pin_hash` | every pin blob at `--rev` hashes to its frozen sha256 |
| `host:<id>` | (H) the quote the ROW carries is a substring of the host pin line (independent of `quote:<id>`) |
| `source_cell:<id>` | (K) the row's S-id is exactly one registry row of 11 cells in `corpus/SOURCES.md` at `--rev` (id regex `^ {0,3}\|\s*S[0-9]{3,}\s*\|`), status `mined`, tier A or B, opened `2026-10-28`, whose URL (the last `http(s)://` token of the source cell) ends with `/` + `c1.pin_suffix[pin]` and contains the `rev_rule` token for that pin, and whose `used-by` cell names the entry path; and the S-id equals the frozen `sid` of that K row |
| `scope:<id>` | (K) in the registry row's `anchor` cell, after an occurrence of `<basename>:` (basename = last path component of `pin_suffix[pin]`), the comma-separated list of `N` or `N-M` locators contains a range that includes the row's line |
| `tok:<id>` | the proposition shares at least one identifier token (regex `[A-Za-z_][A-Za-z0-9_]{3,}`, case-sensitive) with the row's quote |
| `num:<id>` | every maximal digit run of the proposition (regex `(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])`) is a digit run of the quote, the integer of the row's own line, the line of another frozen row of the same pin, or one of 0,1,2,3 |
| `new_rows` | the rows `S383`..`S390` each satisfy `source_cell` (`new_rows=<m>/8`) |

Output: `MADO_AUTORELOAD_ENTRY: rev=<rev> rows=<a>/30 hosts=<b>/3 sources=<c>/30 scope=<d>/30 content=<e>/33 new_rows=<m>/8 verdict=<TARGET_MET|TARGET_MISSED> missed=<legs, comma-separated, or none>`. `a` = K rows whose `row:` and `quote:` hold; `b` = H rows whose `row:`, `quote:` and `host:` hold; `c` = K rows whose `source_cell` holds; `d` = K rows whose `scope` holds; `e` = K and H rows whose `tok` AND `num` hold. `TARGET_MET` needs every leg, `a=30 b=3 c=30 d=30 e=33 m=8`.

**What the counter proves and does not.** It proves quote identity at an exact pin line, registry binding and scope, and
lexical grounding of each proposition in its own quote (an identifier shared, no number absent from the quote). It does not
prove entailment: a forged proposition that reuses a quote identifier and only quote numbers passes (declared limit; the
sentence-to-pin audit of wave 2 and the non-author closure carry entailment, reported not counted).

**Harness** (`quality/check-r56-controls.py --claim c1`): prints `MADO_R56_CONTROLS: claim=c1 good=<ok|bad> controls=<k>/10 verdict=<OK|FAIL>`. `good` = the counter prints TARGET_MET on the tree at `--rev`. A control is passed when the counter, run on the control's scratch repo (a commit of the good tree with ONE mutation), exits 1 with `missed` containing the control's required leg and printing no TARGET_MET. Controls (mutations on the committed tree; the harness holds the expectations; the counter knows nothing about them):
1. `entry-absent` — delete the entry file → `entry_absent`.
2. `junk-placeholders` — replace every K and H proposition by `placeholder proposition text for row <id>, not a claim about any source line` (K) / `placeholder host proposition <id>, not a read` (H) → `tok:` and `content` shortfall (`e<33`).
3. `false-number` — in the row K04 proposition append ` The value is capped at 200 by this call.` → `num:K04`.
4. `cross-pin-source` — K10 cites `S385` in place of `S383` → `source_cell:K10`.
5. `scope-swap` — add a scratch registry row `S399` with the SAME URL as S383, status mined, tier A, opened 2026-10-28, used-by naming the entry, anchor `ConfigWatcher.cpp:1-10`, and make K10 cite `S399` → `scope:K10` (and `source_cell:K10`: the frozen sid differs).
6. `provenance-dangling` — append `, S999` to the `source:` line → `prov`.
7. `dropped-row` — delete row K17 → `row:K17`.
8. `edited-quote` — change one character inside the K05 quote cell → `quote:K05`.
9. `pin-byte` — change one byte of `fetch/Hyprland-ConfigWatcher.cpp` → `pin_hash`.
10. `new-row-missing` — delete the registry row S390 → `new_rows` (and `source_cell:` of the K rows citing S390).

## §C2 — `tools/mado-watchplan.py` (operability, capability acquisition)

A single-file read-only python3 tool: predicts the inotify watch list Hyprland 0.56.2 (hyprlang era, `configProvider`
hyprlang) registers for a config tree, and joins `misc:disable_autoreload` to a `hyprctl getoption` dump. It reads only the
files named by its arguments, the files its `source =` lines reach, and `os.stat`/`os.lstat`/`os.path.realpath`/`glob` on
those paths; it starts no process, opens no socket, writes nothing.

**Arguments** (two-token form only, any order): `--config PATH` exactly once (absolute), `--home DIR` at most once
(absolute), `--display-root DIR` at most once (absolute), `--getoption PATH` at most once (absolute). Anything else — a
missing `--config`, a repeated option, a relative path, an unknown token, an option without value — is setup reason `usage`.
`--selftest` alone is informational and is not part of PRED-C2-r56. The harness replaces the token `{FX}` in every `args.json`
argument by the absolute path of the fixture directory (`fixtures/c2/F##`, `fixtures/c2-holdout/H##`) inside its scratch
export, then runs the tool with cwd = the export root. `--display-root DIR`: every printed path equal to DIR or starting with
DIR + `/`, where DIR is either the given string (trailing `/` removed) or its `os.path.realpath`, prints with that prefix
replaced by `$ROOT`. Setup failure: stdout exactly `MADO_WATCH: SETUP <reason>`, exit 2, reason `usage` | `unreadable` (the
`--getoption` path is missing, unreadable, a directory or non-regular) | `too_large` (any file the tool reads — the config,
a sourced file or the getoption file — larger than 1048576 bytes) | `bad_json` (a non-empty `--getoption` line, stripped,
that is not a JSON object). The `--config` path is never a setup error: it is always the first entry of the path list; it is
parsed when it is a regular file and otherwise (missing, directory, unreadable) only listed (`type=missing` when `lexists`
fails, as fixture F14 shows). A sourced file that cannot be read is listed and not parsed.

**Model** (a deliberate subset of what Hyprland 0.56.2 does; everything outside it is counted `unsupported`, never guessed):
- Files decode as UTF-8 with errors replaced and split on `\n`. The category stack resets at each file's start. A raw line is
  stripped of space, tab, CR, LF, VT, FF; an empty line or a line whose first character is `#` is skipped.
- A line without `=`: exactly `}` pops the stack; a line ending in `{` pushes its text before the `{` (stripped); any other
  line is ignored.
- A line with `=`: LHS and RHS are the stripped texts before/after the FIRST `=`. LHS `source`: if the stack is non-empty
  `unsupported` +1 and the line ends; else the RHS cut at its first `#` and stripped is the source path (below). An LHS
  starting with `$` is ignored. KEY = the stack joined with `:` then `:` then LHS when the stack is non-empty, else LHS.
  Only KEY `misc:disable_autoreload` matters: if the line contains `$`, `{` or a backslash, or the RHS contains `##`,
  `unsupported` +1 and the line ends; else VALUE = RHS cut at its first `#` and stripped; VALUE parses as hyprlang
  `configStringToInt`: starts with `true`, `on` or `yes` → 1 (checked first); else starts with `false`, `off` or `no` → 0;
  else matches `[0-9]+` entirely → that decimal integer; anything else → `unsupported` +1, line ignored. The last accepted
  value in file-processing order wins.
- **Source handling** (legacy `handleSource`, `fetch/Hyprland-legacy-ConfigManager.cpp:1810-1850`; `absolutePath`,
  `fetch/Hyprland-MiscFunctions.cpp:61-83`): `cur` = the path of the file being parsed (the main config path at depth 0). RAW =
  the source path. (1) `len(RAW) < 2` → event `ERROR reason=bogus`, nothing else. (2) RAW starts with `~` and no `--home` was
  given, or RAW contains a backslash → `unsupported` +1, line ends. (3) VALUE = absolutePath(RAW, cur): RAW[0]=`~` → `--home` +
  RAW[1:]; RAW[0]=`/` → RAW; else curdir = `cur[:rfind('/')]` (all of `cur` if it holds no `/`); RAW[0]=`.`: RAW starts `../` →
  parent = `curdir[:rfind('/')]` (all of curdir if none) + RAW[2:]; RAW starts `./` → curdir + RAW[1:]; any other `.`-leading
  RAW (e.g. `.hidden`, `..x`) → curdir + `/` + RAW; else (not `.`-leading) curdir + `/` + RAW. (4) MATCHES = `sorted(glob.glob(VALUE))`
  (bytewise order; python `glob` semantics: `*`/`?`/`[..]`, no brace expansion, leading-dot names need a leading-dot pattern; a
  dangling symlink counts as a match). No match → event `ERROR reason=nomatch`. (5) For each match M in order: V =
  absolutePath(M, cur) (identity for absolute M); `os.stat(V)` failing (including a dangling symlink) → event `ERROR
  reason=inaccessible` and the REST of this line's matches are skipped; a regular file → append (V, via) to the path list
  (BEFORE parsing it) and parse V recursively with `cur`=V and depth+1, unless depth+1 > 16, in which case `unsupported` +1 and
  V is recorded but not parsed; a directory → event `SKIP reason=directory`; anything else → event `SKIP reason=nonregular`.
  `via` = `<display(cur)>:<line number, 1-based>`; the main config's via is `main`.
- A `--config` path is always the first list entry (via `main`) and is parsed when it is a regular file.
- **Watch list** (`fetch/Hyprland-ConfigWatcher.cpp:32-76`): if the last accepted `misc:disable_autoreload` value is non-zero the
  watch list is EMPTY (`autoreload=off`); otherwise every list entry in order becomes one primary watch: `type=dir` if
  `os.path.isdir(path)` (follows symlinks), else `type=file` if `os.path.lexists(path)`, else `type=missing`; mask text
  `IN_CLOSE_WRITE|IN_DONT_FOLLOW` for file and missing, `IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM`
  for dir. If `os.path.islink(path)` and `os.path.realpath(path, strict=True)` succeeds, one further watch follows immediately:
  `role=canonical`, `path`=that realpath, `type=file`, mask `IN_CLOSE_WRITE`. Duplicate paths yield duplicate watches.
  Declared divergences from Hyprland: the depth cap of 16 (Hyprland has none), `glob` bytewise order versus the C library's
  locale collation, GLOB_TILDE `~user` forms, the Lua config provider, runtime `hyprctl keyword misc:disable_autoreload`.

**Output** (stdout; every line starts `MADO_WATCH` or `MADO_WATCH_LIVE`; exit 0 on a completed run):
```
MADO_WATCH: config=<display(config)> autoreload=<on|off> disable_autoreload=<unset|N> paths=<list length> unsupported=<U> errors=<E>
<events in processing order>   MADO_WATCH: ERROR via=<via> source=<RAW> reason=<bogus|nomatch|inaccessible>
                               MADO_WATCH: SKIP via=<via> path=<display(V)> reason=<directory|nonregular>
MADO_WATCH: n=<k> role=<primary|canonical> path=<display(path)> type=<file|dir|missing> mask=<mask> via=<via>      (k counts watch lines from 1)
MADO_WATCH_LIVE: option=misc:disable_autoreload config=<0|1> live=<int|?> verdict=<AGREE|DIFFER|UNKNOWN>            (only with --getoption)
MADO_WATCH: DONE watches=<count of watch lines> unsupported=<U> errors=<E> live=<NONE|AGREE|DIFFER|UNKNOWN>
```
`config` in the live line is 1 when the last accepted value is non-zero, else 0 (also when unset). Each non-empty
`--getoption` line is a JSON object; an object with a string `option` and an integer (not boolean) `int` records that option's
live value (a later line wins); other objects are ignored; a non-object JSON value is `bad_json`; no record → `live=?`,
`UNKNOWN`. `AGREE` when the live int equals `config`, else `DIFFER`.

**Fixtures.** `fixtures/c2/F01..F18/{args.json,expected.out,expected.rc,note.txt,tree/...}`; trees may hold git symlinks (the
harness exports with `git archive` + `tar -x`, which preserves them; a harness that dereferences or drops a symlink is wrong).
Expected output is stored byte for byte. **Hold-out:** eight fixtures H01-H08 of the same layout were generated by the L1
before the wave and are held outside the repository; the commitment `c2.holdout_commit_sha256` is the sha256 over, for each
file or symlink under the hold-out root in sorted UTF-8 byte order of the relative path, the line
`<relpath>\0<f|l>\0<hex sha256 of the file bytes (f) or of the link text (l)>\n`. The same commitment over
`fixtures/c2` equals `c2.fixture_commit_sha256`. The L1 reveals the hold-out into `fixtures/c2-holdout/` at integration; seats
are not told where it is held and do not look for it.

**Harness** (`quality/check-r56-controls.py --claim c2`; optionally `--holdout DIR`, default `fixtures/c2-holdout` in the export):
exports the tool, `fixtures/c2`, `fixtures/c2-holdout` and the three `ctl/` stubs at `--rev` into a scratch dir, runs each as
a child process (`python3 -I <tool> <args>`; cwd = export root; scrubbed env), compares stdout bytes and exit status with
`expected.out`/`expected.rc`, recomputes the two commitments, and prints
`MADO_R56_C2: rev=<rev> fixtures=<a>/18 holdout=<b>/8 holdout_commit=<ok|bad|absent> controls=<k>/3 verdict=<TARGET_MET|TARGET_MISSED>`.
`controls=3/3`: `ctl/const-host.py` passes at most 1 of the 26 fixtures; `ctl/empty.py` passes 0; `ctl/lookup-committed.py`
passes 18/18 committed and 0/8 hold-out. `holdout_commit=ok` means the commitment over the hold-out root equals
`c2.holdout_commit_sha256`.

## §C3 — registry back-references (calibration)

**Definitions** (all at `--rev`). ENTRIES = regular blobs `corpus/knowledge/*.md` (direct children only). ROWS = registry rows
of `corpus/SOURCES.md` (id regex `^ {0,3}\|\s*S[0-9]{3,}\s*\|`, split on `|` after stripping the outer pipes, exactly 11
cells; a row with another cell count is a setup error). CITE(entry) = the set of tokens matching
`(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])` on lines of the entry that are outside fenced code blocks (``` / ~~~ fences with 0-3
leading spaces). USEDBY(row) = every match of `corpus/knowledge/[A-Za-z0-9_.-]+\.md` in cell 11. SRC(entry) = tokens on lines
starting `source:` among the entry's first 15 lines.
- `missing` = the number of pairs (S, entry) with S a registry row id, S in CITE(entry) and the entry path not in USEDBY(S).
- `extra` = the number of pairs (S, path) with path in USEDBY(S) and (path not an ENTRIES member OR S not in CITE(path)).
- `dangling` = the number of pairs (entry, S) with S in SRC(entry) and S not a registry row id.
Cells other than `used-by` are never touched by the fix; `used-by` changes are logged old→new in the round lesson (CORPUS
rule 2). A non-registry id token such as the draft id `S243` in `request-limits-upstream-r31.md:33` is neither `missing` (it
is not a row id) nor `dangling` (not on a `source:` line) and stays as is.

Output: `MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=<m> extra=<x> dangling=<d> verdict=<TARGET_MET|TARGET_MISSED> missed=<missing,extra,dangling|none>` — `TARGET_MET` only at `m=0 x=0 d=0`; exit 0/1/2 as above. Baseline measured at the base revision: `entries=70 rows=319 missing=65 extra=0 dangling=0`.

**Harness** (`quality/check-r56-controls.py --claim c3`): `MADO_R56_CONTROLS: claim=c3 good=<ok|bad> controls=<k>/6 verdict=<OK|FAIL>`. Controls (one mutation each on a scratch commit of the good tree at `--rev`; the counter must exit 1 and `missed` must contain the leg):
1. `base-registry` — replace `corpus/SOURCES.md` by its bytes at the frozen base revision (`base` in the tables; the object must be readable in `--repo`) → `missing`.
2. `fill-all` — set the used-by cell of EVERY row to the space-joined list of ALL entry paths → `extra`.
3. `drop-one` — remove the path of the first entry (sorted) from the used-by cell of the first row (sorted by id) that lists it → `missing`.
4. `dangling-source` — append ` S999` to the `source:` line of the first entry (sorted) → `dangling`.
5. `ghost-path` — add `corpus/knowledge/no-such-entry.md` to the used-by cell of S001 → `extra`.
6. `fenced-cite` — move one entry's only citation of some row into a fenced block (the harness picks, by sorted order, the first (S, entry) pair where entry cites S exactly once on a non-fence line; it wraps that line in a ``` fence) while used-by still lists it → `extra`.

## Seat boundaries (every seat)

A seat writes only under `<lane>/.ufo/waves/round-56/<wave>/<SeatName>/` and its report file `<SeatName>.md` beside it; it never
edits tracked lane files, the fleet repo, sibling lanes, `jj` or the git index, never commits, and never touches host
configuration or the compositor (host reads: `hyprctl getoption`, `hyprctl version -j`, `stat`, reads of `~/.config/hypr`).
