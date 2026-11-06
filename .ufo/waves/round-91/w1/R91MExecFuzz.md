# R91MExecFuzz — C1 fresh-leg fuzz generator (round 91, w1)

**Report path:** `.ufo/waves/round-91/w1/R91MExecFuzz.md` (this file)
**Seat:** R91MExecFuzz (leaf). All figures below are **DRAFT** results: no measurement is
claimed, nothing was written under `.ufo/waves/round-91/receipts/`, and every run used the
DRAFT tool path or a byte-identical copy of it.

## Files written

| file | sha256 | note |
|---|---|---|
| `.ufo/waves/round-91/controls/fuzz-gen-r91.py` | `0d147b83f85d0a0d25be0282d21624bad8a4743f6964bda9b98b6ef996121418` | the fresh-leg generator (stdlib only, deterministic) |
| `.ufo/waves/round-91/controls/mime-cases-r91-fz.json` | — | 2 unlabelled minimised cases (`fz-01` current disagreement, `fz-02` regression); schema `mime-cases-r91-v1`, no `expect` |

Everything else lived under `S=/fast/scratch/hyaku/mado-r91/R91MExecFuzz/` and was deleted on exit.

## Generator

`controls/fuzz-gen-r91.py`:

- `generate(seed: int, n: int) -> list[dict]` is a pure function of the integer seed
  (`random.Random(seed)`); two calls produced byte-identical 400-case JSON
  (sha256 `987c0918f5db6ff261143a88d4fd67d1e0be0ab509938148fb2db08de633e1a4`).
- `python3 fuzz-gen-r91.py SEED N` prints
  `{"schema":"mime-cases-r91-v1","cases":[...]}` (verified: rc 0, ids `fz-<seed>-<k>`, `group:"fresh"`).
- Fresh-leg derivation: `seed = int(first 8 hex of sha256(tool), 16)`; for the headline bytes
  below that is `int("ddbcd6e3",16) = 3720140515`.
- Randomised axes: 1-3 `XDG_CONFIG_DIRS` and 1-3 `XDG_DATA_DIRS` entries (+ config/data homes);
  `XDG_CURRENT_DESKTOP` incl. unset, empty string, empty tokens, invalid tokens, mixed order;
  the PATH list (with/without `/usr/bin`, with/without the fixture `bin/`); `[Default
  Applications]`/`[Added Associations]`/`[Removed Associations]` in `mimeapps.list`, each dir's
  `<desktop>-mimeapps.list` (config *and* data dirs), `defaults.list`, `mimeinfo.cache`;
  desktop files (valid, `Hidden=true/1/false`, `Type=Link`, `TryExec`/`Exec` program missing,
  unbalanced-quote `Exec`, no/empty `Exec`, unparsable file, first group not `[Desktop Entry]`,
  `Path=` working-dir forms, one directory deep with the `sub-` id prefix); `aliases`/`subclasses`
  text files (with and without final newline, long lines past xdgmime's 255-byte `fgets`, comment
  and separator-less lines); occasional malformed list lines (junk line, key before any group,
  group trailing garbage, bad value escape, locale-suffixed key, duplicate key, duplicate group,
  CRLF); 1-4 asked types from a 12-type vocabulary.
- Deliberate exclusion (documented in-code): a *duplicate alias source in two data dirs*. GLib's
  text-mode alias match is `bsearch` over a `qsort`'ed array (`gio/xdgmime/xdgmimealias.c:94,147`)
  and for equal keys that order is unspecified, so such a case has no oracle answer a tool could be
  required to reproduce. An earlier generator revision emitted it and produced 3 disagreements
  (see F3); the dimension was removed so the fresh leg stays sound.
- Note: duplicate-key fixtures are intentionally over-weighted (~70% of cases contain one): that is
  the ordering-sensitive area that actually caught a defect (F2).

## DRAFT runs (two seeds × 200 cases = 400 per run)

Candidate bytes churned under this seat: the file at
`.ufo/waves/round-91/build/mado-mime.c1.py` was 30046 B at 21:01, 36861 B @21:24:37
(sha `99485e9e…`), 37836 B @21:26:04 (sha `5c9d07ca…`) and 38832 B @21:27:17
(sha `ddbcd6e3cec2d484aa78038f1eee96ed86eb6dd436b65b3046f42315b5f09cbb`). Each comparison below ran
against a byte-identical pinned copy; for the headline run the lane file's sha was identical before
and after the run.

| run | generator rev | candidate bytes | seed 9101 | seed 9102 | oracle rejects |
|---|---|---|---|---|---|
| A | initial (no PATH/collision axes) | 30046 B | 200/200 | 200/200 | 0 |
| B | +PATH +alias-collision +duplicate-alias | 30046 B | 187/200 | 187/200 | 0 |
| C | −duplicate-alias | 36861 B `99485e9e` | 200/200 | 200/200 | 0 |
| D | −duplicate-alias | 37836 B `5c9d07ca` | 200/200 | 200/200 | 0 |
| **E (headline)** | **final `0d147b83`** | **38832 B `ddbcd6e3`** | **200/200** | **200/200** | **0** |

Run E runtime per case (candidate process only, no bwrap): oracle label **8.89 ms** / **9.98 ms**
(1-4 `gio mime TYPE` calls per case), candidate **44.64 ms** / **46.81 ms**. Run B (older bytes):
oracle 10.1/10.7 ms, tool 40.9/41.3 ms. No generator case was rejected by the oracle in any run
(`label_case` raises on `gio` rc != 0 or unparsable output; 0/400 in each of five runs).

Coverage over the 400 headline cases: desktop files 400; `mimeapps.list` 400; `mimeinfo.cache` 355;
`defaults.list` 316; `<desktop>-mimeapps.list` 268; `aliases` 293; `subclasses` 234; one-level
subdirectory desktop 143; `Path=` key 211; `[Removed Associations]` 368; malformed desktop file 171;
CRLF list file 52; desktop unset 23; duplicate key within one group 282; asked types 1/2/3/4 =
70/71/108/151; config dirs 1/2/3 = 147/106/147; data dirs 1/2/3 = 132/130/138.

## Findings

### F1 — same desktop id from a top-level file and a subdirectory file in one data dir (LIVE: `fz-01`)

With the current bytes (`ddbcd6e3`) the candidate answers `default=none`, GLib answers
`default=vendor-e.desktop`. Repeats: 5/5 disagreement, and 20/20 on the same fixture earlier.

Reproducer (creation order matters):

```sh
R=$(mktemp -d)
mkdir -p "$R/cfg" "$R/etc2" "$R/home/applications" "$R/sys0/applications" "$R/sys0/mime"
printf 'garbage line' > "$R/sys0/applications/vendor-e.desktop"      # entry 1
mkdir -p "$R/sys0/applications/vendor"
printf '[Desktop Entry]\nType=Application\n' > "$R/sys0/applications/vendor/e.desktop"  # entry 2
printf '[MIME Cache]\naudio/x-mp3=vendor-e.desktop;d.desktop;c.desktop;' > "$R/home/applications/mimeinfo.cache"
printf 'audio/x-mp3 audio/mpeg\n' > "$R/sys0/mime/aliases"
env -i HOME="$R" XDG_CONFIG_HOME="$R/cfg" XDG_CONFIG_DIRS="$R/etc2" XDG_DATA_HOME="$R/home" \
  XDG_DATA_DIRS="$R/sys0" PATH=/usr/bin LC_ALL=C /usr/bin/gio mime audio/mpeg
# gio:    Default application for “audio/mpeg”: vendor-e.desktop
# tool:   {"default": null, ...}   (python3 -I build/mado-mime.c1.py --json --desktop "" …)
# listdir of sys0/applications: ['vendor-e.desktop', 'vendor']
```

Source: `gio/gdesktopappinfo.c:769-818` `get_apps_from_dir()` walks the tree in
`g_dir_read_name()` order (:781), inserts each entry into `dir->app_names` with
`g_hash_table_insert()` (:796, which replaces an existing key) and prefixes subdirectory ids with
`<sub>-` (:802); `desktop_file_dir_unindexed_get_app()` (:1067-1078) then loads
`g_hash_table_lookup(app_names, id)`. Both `vendor-e.desktop` and `vendor/e.desktop` produce the id
`vendor-e.desktop`, so the *last entry seen* wins, and GLib's readdir order put the valid subdirectory
file last. The candidate's `DesktopDir._walk` sorts (`sorted(os.listdir(d))`), so
`vendor` sorts before `vendor-e.desktop`, the unparsable top-level file is inserted last, and the id
becomes unloadable. The symmetric experiment (valid top-level, garbage subdirectory) agreed with the
candidate, confirming the mechanism. Recommendation: walk in `os.listdir` order (Python uses the same
`readdir(3)` order as `g_dir_read_name`) instead of sorting; the L1 should note the case is
filesystem/creation-order dependent (stable 20/20 on this host's `/fast`).

### F2 — duplicate key whose two names unalias to one type (FIXED during the wave; kept as `fz-02`)

Against the 30046-byte candidate this was a live disagreement. Run B produced 26 disagreeing
cases; the minimised shapes were 7 × F2 (this one), 4 × F3 (duplicate alias source), 1 × F1
(readdir order) and the remainder coincided with the candidate churn described in F4. Fixture:

```
sys/applications/{a,b,c}.desktop   valid
sys/applications/mimeinfo.cache    [MIME Cache]\ntext/plain=a.desktop;
sys/mime/aliases                   text/x-old text/plain
cfg/mimeapps.list                  [Added Associations]
                                   text/x-old=b.desktop
                                   text/plain=c.desktop
                                   text/x-old=b.desktop
types: text/x-old (and text/plain)
```

Old candidate bytes: `default=c.desktop` with `registered=[c,b,a]`; GLib: `default=b.desktop` with
`registered=[b,c,a]`. Source: the parser stores every pair in file order and a repeated key keeps its
first list position while the lookup map is replaced (`glib/gkeyfile.c:1798-1799` inserting before
the head, `:4419-4426` `g_key_file_add_key_value_pair()` = `g_hash_table_replace()` +
`g_list_insert_before()`), and `g_key_file_get_keys()` returns the key at *both* file positions
(`:2005-2055`, the array is filled backwards from the reversed list) while
`g_key_file_get_value()` (`:2179`) resolves it to the last value; `read_mimeapps_list`
(`gio/gdesktopappinfo.c:901-990`) feeds those keys through `expand_strv` (:855-898) in that order.
So GLib processes `text/x-old`, `text/plain`, `text/x-old` (last value), while the old candidate's
`pop`+reinsert collapsed the key to its last position, processing `text/plain` then `text/x-old`
and flipping the first addition. The current bytes keep the first position and take the last value
(comment in `parse_keyfile`), and the case now agrees 5/5; `fz-02` is included as a regression case.

### F3 — duplicate alias source in two data dirs (REJECTED CLASS; not in the fz file)

With the early generator revision, three minimised cases (original ids fz-9101-109, -121, -173) put
`X Y` in one dir's `mime/aliases` and `X Z` in another's. GLib and the tool picked different targets
(e.g. GLib unaliased `text/x-doc` to `text/x-c`, the tool's "first read wins" to `text/plain`),
changing the default. This is unspecified behaviour: `gio/xdgmime/xdgmimealias.c:147` sorts the
accumulated alias array with `qsort` and `:94` matches with `bsearch`, so for equal keys the winner
depends on the libc sort order. The candidate documents this as a named limit. **The L1 must not
freeze cases of this shape**; the generator no longer emits them.

### F4 — transient candidate failure (not reproducible; candidate churn, not a defect)

The first minimisation pass recorded 12 fixtures where the candidate exited 1 with an uncaught
traceback, e.g. `rc=1 Traceback (most recent call last): ... line 840, in <module> ... line 826, ...`
(the traceback ends inside `main`→`resolve`, captured truncated at 300 chars). Re-running the same
fixtures once the candidate bytes settled gave 0 failures in 20/20 repeats, and a rerun with
4000-char stderr capture recorded none. This coincided with the candidate being rewritten several
times by its owner while this seat ran (see the byte/sha timeline above); treat the early rc=1
records as in-flight-edit artefacts, not as a defect. If the builder keeps editing the file, the L1
must re-run the DRAFT comparison on the frozen bytes.

## Verification commands actually run

- `python3 -I .ufo/waves/round-91/build/mado-mime.c1.py --selftest` → rc 0, `checks=17 failed=0` (DRAFT).
- `python3 .ufo/waves/round-91/controls/fuzz-gen-r91.py 9101 2` → rc 0, `mime-cases-r91-v1`, ids
  `fz-9101-000/001`, `group=fresh`, schema keys only.
- 400-case DRAFT comparison driver (oracle `label_case` + the counter's `run_tool` argv shape,
  including `--config-home/--config-dirs/--data-home/--data-dirs/--path/--desktop[-unset]/-- types`)
  → rc 0 for every run in the table.
- `controls/mime-cases-r91-fz.json`: both cases labelled by the oracle without error (rc 0);
  `fz-01` disagrees 5/5, `fz-02` agrees 5/5 against `ddbcd6e3`.

## Host safety / tooling

- `gio mime` was run **only** as `gio mime TYPE` (one argument) by the oracle, under `env -i` with
  `HOME`, `XDG_CONFIG_HOME`, `XDG_CONFIG_DIRS`, `XDG_DATA_HOME`, `XDG_DATA_DIRS`, `PATH`, `LC_ALL`
  all pointing at fixture directories under the scratch root; no XDG list was ever emptied in a
  checked case (an empty `XDG_*_DIRS` makes GLib fall back to host `/etc/xdg`/`/usr/share`, which the
  minimiser is explicitly prevented from producing).
- No writes outside this seat's two owned files and its own scratch; no mutating git/jj; no pacman;
  no installs (nothing needed); no applications launched.
- Scratch `/fast/scratch/hyaku/mado-r91/R91MExecFuzz/` was removed on exit.
