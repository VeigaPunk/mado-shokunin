# R91MReviewC1 — line-by-line review of `mado-mime.c1.py` against GLib 2.90.1

Seat: R91MReviewC1 (reviewer, leaf — no dispatches). Round 91 w1. Base `cc0381db`.
Everything below marked **DRAFT**: candidate runs, oracle runs and counter runs with
`--draft-tool` (rc 3); none of this is a measurement; nothing written under `receipts/`.

Reviewed snapshot: `.ufo/waves/round-91/build/mado-mime.c1.py` copied byte-exact to
`$S/candidate-snapshot.py`, sha256 `99485e9e1ff966d950b47d3d8924a5e7b7360854bf8627c8258bab9db27922f6`
(850 lines). The candidate changed **three times during this review** (observed working-tree shas
`c2a516d8…` 739 ln → `596b730d…` → `3491ed36…` 850 ln → `99485e9e…`); every result below is against
the snapshot sha. The counter also grew during review (274 → 318 lines: fresh fuzz leg + QUALITY 148
crashed-not-killed); reviewed as found: its sha256 at review close is
`dc97fd643c4a7ab6b9337d7a91325884af180894988e28b3de014c51ddcb44e2`; content cited by line range below).

Upstream: GLib tag 2.90.1 raw files fetched into scratch, `gdesktopappinfo.c` sha256 verified
`8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d` (matches declaration); also
fetched `gfileutils.c`, `gstrfuncs.c` (outside the declared list, used only to check two claims the
candidate cites). Oracle binary pins verified: `/usr/bin/gio` `d2164260…cfc462`,
`/usr/lib/libgio-2.0.so.0` → `b38001cc…313685e` (match declaration). Host: glib2 2.90.1-1,
shared-mime-info 2.5.1-2, bwrap 0.13.1.

## Verdict summary

- Candidate agrees with gio on the whole frozen L1 set: **DRAFT run, 89/89 correct, oracle_agree
  89/89, controls do_nothing=7 naive=6 cache_only=24 base_tool=0 (absent), all < 89 —
  DRAFT_TARGET_MET** (counter `--draft-tool`, rc 3, snapshot sha).
- I built 7 independent probes outside the L1 classes; **4 still disagree with gio** and are
  delivered as `controls/mime-cases-r91-rv.json` (rv-01…rv-04, labels from gio, DRAFT). On these the
  candidate scores 0/4 (DRAFT counter run, rc 3): any one of them would flip a measurement to
  TARGET_MISSED once merged into the frozen set.
- 2 probes found real divergences that the author **fixed mid-review** (relative-slash Exec PATH
  fallback; `#` mid-word in Exec) — verified AGREE after the fix; 1 probe (Encoding in a reopened
  first group) agreed all along. The `\v`-whitespace and `[C]`-locale-key fixes also landed during
  review and verify correct.

## Findings (open, by severity)

### R1 (HIGH) — non-UTF-8 mimeapps.list voids the whole file; GLib voids only the offending key

Candidate `load_keyfile` decodes the entire file as UTF-8 and returns None on
`UnicodeDecodeError` (candidate-snapshot `:225-228`), skipping every rule in the file. GLib never
validates UTF-8 at load: comments are dropped unless `KEEP_COMMENTS`
(gkeyfile.c `:1653-1667`), values are stored raw (`parse_key_value_pair :1770-1799`), and the UTF-8
check happens per key at **read** time — `g_key_file_get_string`/`get_string_list` return NULL with
`G_KEY_FILE_ERROR_UNKNOWN_ENCODING` (gkeyfile.c `:2309-2322`, `:2430-2434`), which
`read_mimeapps_list` treats as "skip this key" (gdesktopappinfo.c `:925-939`).

- rv-01: one Latin-1 comment line, else a valid default → gio: default `c.desktop`; candidate: none.
- rv-02: one non-UTF-8 value under `text/plain`, a valid `text/html` key in the same file → gio:
  `text/plain` none, `text/html=c.desktop`; candidate: both none.

Repro: `controls/mime-cases-r91-rv.json` rv-01, rv-02 (fixtures use `{"b64": …}` for the non-UTF-8
bytes). gio output quoted verbatim in the file's `expect` (oracle DRAFT run; `oracle_agree=4/4` in
the counter draft run).

### R2 (MEDIUM) — keys with a `[]` suffix are plain keys in GLib, dropped by the candidate

`key_get_locale` (gkeyfile.c `:1815-1831`): the locale suffix must be **longer than 2 chars**
(`locale_len > 2`); `x-t[]` has suffix len 2 → locale NULL → stored and looked up as the literal
plain key `x-t[]`. The candidate drops any key containing `[` whose bracket content is not `c`
(`:163-166`). rv-03: `[Default Applications]` with `text/plain[C]=a.desktop` (now correctly kept —
this half was fixed mid-review) and `x-t[]=b.desktop`, asking for both literal types: gio gives
defaults `a.desktop` / `b.desktop`; candidate gives none/none. Same file, one disagreement class.

### R3 (MEDIUM) — empty `XDG_DATA_DIRS`: candidate falls back to defaults for the MIME DB; xdgmime does not

xdgmime reads `XDG_DATA_DIRS` with `getenv` directly (xdgmime.c `xdg_init_dirs :209-233`): an empty
(but set) value yields **no** system mime dirs — only `<XDG_DATA_HOME>/mime` — and empty elements
are skipped (`:263-271`). The desktop-file side uses `g_get_system_data_dirs`, which does default on
empty (spec). The candidate funnels both sides through one `split_path_list` whose `if not v`
(`:778-781`) substitutes the default for `""` — so with `data_dirs: []` it consults the host
`/usr/local/share:/usr/share` (under the sandbox: the real shared-mime-info `mime.cache`), switches
to cache-only unaliasing, and misses the text `aliases` file gio still reads. rv-04 (hermetic on the
`default` field): gio `default=a.desktop` for `text/x-old` via `<data_home>/mime/aliases`; candidate
`default=none`. Note: rv-04's `registered`/`recommended` labels contain host desktop entries
(`libreoffice-writer.desktop`, `nvim.desktop`) because gio defaults the *desktop* dirs on empty —
that part of the label is host-dependent; the L1 may want to re-label at freeze or keep only the
default field as the falsifier.

## Findings fixed during this review (verified AGREE on the snapshot)

- F-a: relative-slash `Exec` name (`bin/tool`) with `Path=` set: GLib tries
  `<Path>/bin/tool`, then falls through to the PATH search (gutils.c `:300-349`: the miss only
  returns NULL when the name is absolute). Old candidate returned not-found without the fallback.
  Now ported (`find_program :441-458`); probe p05 AGREE (gio `a.desktop`, was `b.desktop`).
- F-b: `#` mid-word in `Exec` (`sh#c %f`): GLib starts a comment only at token start
  (gshell.c `:509-527`); old candidate used `shlex` commenters (comment anywhere). Now a ported
  tokenizer (`_tokenize`, `:497`); probe p04 AGREE (gio `b.desktop`, was `a.desktop`).
- F-c: whitespace set — candidate now uses `ASCII_SPACE = " \t\n\f\r"` (`:87`), excluding `\v`;
  verified against `gstrfuncs.c ascii_table_data :263-265` (byte 0x0b = 0x004, no 0x100 SPACE bit).
  The old code (and `tools/mado-portals.py:140`) included `\v` — wrong there too.
- F-d: locale key `text/plain[C]` kept (GLib `locale_is_interesting` under LC_ALL=C keeps exactly
  `C`, ASCII-case-insensitive, gkeyfile.c `:2580-2602`); Hidden now `rstrip(ASCII_SPACE)` then
  `true`/`1` (`:731`) — matches `parse_value_as_boolean` (gkeyfile.c `:4978-5001`,
  `strcmp_sized :4971-4975`: case-**sensitive** strncmp over the non-whitespace prefix; L1 m10
  `Hidden=1` label confirms).

## Docstring rule table (claim → GLib cite → verdict)

| Rule (candidate docstring) | GLib 2.90.1 cite | Verdict |
|---|---|---|
| dirs order, config dirs get no desktop files | gdesktopappinfo.c `:1624-1684`, `:1412-1424` | agree |
| desktop tokens: split `:`, empty/non-`[-_alnum]` dropped, lowercased | `:318-377` | agree |
| per-dir `*.desktop` walk, subdir `<sub>-` id | `:768-806` | agree (candidate sorts entries; g_dir_read_name order unspecified, no observable effect: id → exactly one path) |
| list file order: `<desktop>-mimeapps.list` (defaults only) forward, mimeapps.list, config return, defaults.list, mimeinfo.cache | `:993-1042` | agree |
| expand: first list verbatim, later dedup + blocklist; additions before removals per file; defaults always | `expand_strv :855-898`, `read_mimeapps_list :901-988` | agree |
| unloadable file skipped; unparsable list value skips that key | `:905-910`, `:925-939` | agree |
| default: per type defaults-all-dirs, then additions-all-dirs, results reset per type, blocklist persists, first dir that loads wins, Hidden accepted, uris unchecked (`gio mime` passes FALSE) | `:4722-4788`, `:1387-1402` | agree |
| masking = higher-precedence data dir holding the id; never for the default's direct load loop | `:270-291` (`app_name_is_masked` stops at self) | agree |
| ancestors: unalias once, then BFS where each node contributes `[unalias(node)] + parents(unalias(node))` | `:4552-4582` + gcontenttype-fdo.c `:81-113` (parents array includes the unaliased type itself) | agree — the subtle unalias-of-intermediate-node behavior is correctly modelled |
| registered = fallback TRUE, recommended = FALSE, ids via `g_desktop_app_info_new` (first dir holding the id, load fails → NULL, then Hidden drop; `get_is_hidden` = `info->hidden` only, no NoDisplay) | `:4590-4705`, `:2186-2216`, `:2310-2315` | agree |
| desktop load: start group, Type, Path/TryExec/Exec as strings, `is_invalid_key_error` semantics, TryExec/Exec program lookup with `Path=` as working dir | `:1894-2095` | agree (after F-a) |
| program lookup: access(X_OK) not dir; `/bin:/usr/bin:.` default | gutils.c `:300-349`, gfileutils.c `:428` (access, not mode bits) | agree |
| shell parse: tokenize+unquote, empty/whitespace → error (L1 p09 label `a.desktop` confirms `Exec="   "` stores an empty value, not an error) | gshell.c `:657-730`, `:497-527` | agree (after F-b) |
| Hidden boolean: `true`/`1` case-sensitive, trailing ASCII space ignored | gkeyfile.c `:4978-5001` | agree (after F-d) |
| mime dirs = data_home/mime + each XDG_DATA_DIRS entry + /mime; valid cache dir skips its text files; any cache → caches only; else fgets(255) text | gcontenttype-fdo.c `:116-138`; xdgmime.c `:135-206` (cache load `return FALSE` skips that dir's text), `:731-746`, `:902-935` | agree, **except** the empty-string/empty-element case → R3 |
| cache binary: alias list @4, parents @8, parents capped 127, per-cache dedup then cross-cache union | xdgmimecache.c `:308-360`, `:1065-1122` (`p < 127`; the `break` is per-entry, not per-cache) | agree (L1 x14 label `registered=[b.desktop]` confirms the union) |
| text files: fgets(255) chunking, NUL truncation, `#` skip, last byte of field 2 chopped | xdgmimealias.c `:106-148`, xdgmimeparent.c `:109-184` | agree (chop verified: L1 x13) |
| keyfile: group/key name validation, CRLF, Encoding rule, escapes, trailing-empty piece, duplicate key last-value-first-position | gkeyfile.c `:1595-1667`, `:1710-1801`, `:4420-4448`, `:4692-4772` | agree |
| "C locale: locale-suffixed keys dropped" | gkeyfile.c `:1815-1831`, `:2580-2602` | **disagree** → R2 (and the docstring line should say: keys kept iff bracket content is `C`) |
| (implicit) whole-file UTF-8 | gkeyfile.c `:2309-2322` | **disagree** → R1 |

Named limits accepted in the candidate (documented, non-fixable or unreachable): repeated alias
first-read (GLib qsort+bsearch unspecified); relative/empty PATH elements resolved against
working_dir instead of the process CWD (gutils.c PATH loop) — unreachable through the case schema
(`abspaths` absolutizes entries; empty entries cannot be expressed); Unicode `isalnum` vs
`g_unichar_isalnum` bracket-charset edge.

## Part 2 — GKeyFile section reused from tools/mado-portals.py

The parser is the same algorithm with three local changes, all justified here: returning
`first_group` (Desktop Entry start-group validation needs it; portals checks it inline), the
duplicate-key update changed from pop+set to first-position/last-value (`:169-172`) — matches
GLib's lookup_map replace + in-place pair list (`gkeyfile.c :4420-4448`, `:4526-4545`), observable
only through key order which is per-type here, and the locale-key filter (portals drops all
`[`-keys; here `[C]` must be kept). Rules that matter here and not in portals: **duplicate keys**
(common in real mimeapps.list, rare in portal configs) — now correct; **non-UTF-8 files**
(user-writable mimeapps.list vs trusted portal configs) — still wrong, R1; **Encoding rule** —
implemented in both, verified including the reopened-first-group case (add_group reuses the struct,
gkeyfile.c `:4224-4228`, so the pointer-equality Encoding check fires; probe p06 AGREE). Note the
`\v` fix (F-c) should be back-ported to `tools/mado-portals.py` by whoever owns it — I did not touch
it (out of my write scope).

## Part 3 — counter c1-r91-mime-resolution.py

- **Predicate vs code**: consistent. `correct()` compares `default` for every asked type and the two
  lists only when the label's default is not None — exactly the docstring's "where gio printed a
  default". QUALITY 148 is implemented as declared: killed requires a well-formed **wrong** answer
  (`wrong>0`); crash-only mutants are counted `crashed_not_killed` (updated main, `:258-276`), which
  resolves the old declaration-vs-code mismatch I saw at 274 lines.
- **When gio prints no default**: expect holds `default=null, registered=null, recommended=null`;
  the code checks only the default, so a tool's list computation is unconstrained on no-default
  cases. Predicate-consistent; worth knowing when reading `correct=N`.
- **Sandbox**: `--ro-bind /dev/null` over `/usr/bin/gio` and over `realpath(libgio)` (symlink
  traversal lands on the masked path too), `--tmpfs <realpath(repo)>` for the lane,
  `--unshare-net`. The labels are unreachable from inside: they live in the lane (masked) and are
  never passed to the tool (argv carries only roots/path/desktop/types; env is LC_ALL/HOME/PATH with
  PATH=/nonexistent). Residual risks (hardening, not predicate violations): (1) `--ro-bind / /`
  leaves the whole host readable — including sibling seats' scratch dirs, so a tool that guesses
  other seats' paths could hunt for label copies left lying around (none were, in this wave, outside
  the masked lane); (2) no `--unshare-pid`, so `/proc` shows host processes. Recommend
  `--unshare-pid` and binding only what is needed.
- **Pins/setup**: sha256 pins for cases/mutants/oracle/fuzz-gen/gio/libgio all enforced before any
  run; scratch-inside-lane rejected; bwrap probe; tool absent at rev → SETUP_ERROR rc 2; draft rc 3.
  Verified live: a real sha mismatch produced `SETUP_ERROR … 42a08f2c… != 0000…` rc 2 when I
  deliberately passed a wrong pin.
- **Controls** verified below N on the 89-case draft: do_nothing 7, naive 6, cache_only 24, base
  absent 0. The three control implementations are honest stand-ins (last-key-wins single-file
  reader; cross-dir mimeinfo.cache reader; all-none) — none can exceed N on any realistic frozen
  set containing defaults.
- **Fresh leg**: seed = first 8 hex of the measured tool's sha, `generate(seed, --fresh)`, labelled
  at run time, same `correct()`. I observed one draft run where all 8 fresh cases printed WRONG for
  an older candidate sha (`c2a516d8`) while the same seed cases passed 4/8 under the then-current
  file — that was the mid-review edit boundary, not a counter bug (replayed both ways; also
  re-verified the fresh leg passes 4/4 on the snapshot: `fresh=4/4 fresh_seed=2571656862`).

## Verification log (commands → exit codes)

- GLib fetch + sha check: `8e9ce1a8…` matches declaration; pacman -Q read-only: glib2 2.90.1-1,
  shared-mime-info 2.5.1-2, desktop-file-utils 0.28-1.
- Probe driver (candidate vs gio, 7 probes): exit 0; first run (old sha) DISAGREE 6/7; re-run on
  `3491ed36` DISAGREE 4/7 (p04, p05 fixed); p06 AGREE throughout.
- Counter DRAFT on rv-6 (old sha): all 6 WRONG, rc 3. Counter DRAFT on L1 (sha `596b730d`):
  89/89, rc 3-equivalent DRAFT_TARGET_MET. Counter DRAFT on L1 with a wrong pin: SETUP_ERROR rc 2.
- Counter DRAFT on rv-4 (snapshot `99485e9e`): 4/4 WRONG, fresh 4/4, oracle_agree 4/4, rc 3.
  Counter DRAFT on L1 (same snapshot): 89/89 correct, controls 7/6/24/0, DRAFT_TARGET_MET.
- Candidate `--selftest` (snapshot): `checks=17 failed=0`, exit 0.
- Fresh-leg sandbox replay (8 cases, rc/stdout captured): all rc 0 well-formed JSON.
- No installs; no pacman transactions; no mutations anywhere; fixture-free review (no git fixture
  repos needed); scratch `HYAKU_SCRATCH=/fast/scratch/hyaku/mado-r91/R91MReviewC1` deleted on exit
  — its GLib source copies are re-fetchable at tag 2.90.1 and all cited lines are quoted here.

## Files written by this seat

- `.ufo/waves/round-91/controls/mime-cases-r91-rv.json` — 4 reproducing cases, schema
  `mime-cases-r91-v1`, sha256 `f76b8eb22fb9b6226867b57ec80a365dad1cf27b1b6464fba79ace259672c654`,
  labels from gio `d2164260…`/libgio `b38001cc…` (DRAFT; re-label at the freeze).
- `.ufo/waves/round-91/w1/R91MReviewC1.md` — this report.

Recommendation to the L1: merge rv-01…rv-04 into the frozen set (they are outside every existing
L1 class); fix R1 (validate UTF-8 per value at read, not per file) and R2 (suffix ≤2 chars ⇒ plain
key) and R3 (pass XDG_DATA_DIRS through to the mime DB verbatim, empty string included) before the
freeze, or the first measurement after the merge lands TARGET_MISSED.
