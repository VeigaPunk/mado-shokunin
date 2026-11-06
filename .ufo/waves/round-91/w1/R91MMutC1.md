# R91MMutC1 — C1 mutation seat, round 91 w1

Seat: R91MMutC1 (mutation tester, leaf). Scope: the C1 candidate
`.ufo/waves/round-91/build/mado-mime.c1.py`, its modelled rules, and killing cases for mutants the
frozen L1 cases miss. Every run below is **DRAFT** (`--draft-tool`, counter rc 3); no receipt was
written and nothing here is a measurement.

## Owned files written

| path | sha256 | content |
|---|---|---|
| `.ufo/waves/round-91/controls/mime-mutants-r91-mc.json` | `7e91aa1d01bc9bb1a1c14da999a3e91b4861d26de1fbd0920b2bf752489acdb0` | 36 mutants X01–X36 + `equivalent_not_counted` (X08) |
| `.ufo/waves/round-91/controls/mime-cases-r91-mc.json` | `d3627f0bb0ca1e79f35a3a90fe5fcb58d09ba692180e1f2f10ce5c7e4d15fcc0` | 12 unlabelled cases mc-01…mc-12, schema `mime-cases-r91-v1` |
| `.ufo/waves/round-91/w1/R91MMutC1.md` | this report | — |

Nothing else in the lane was written: the candidate, oracle, L1 cases, L1 mutants and counter were
read only. All mutated sources are copies under
`S=/fast/scratch/hyaku/mado-r91/R91MMutC1` (deleted at exit).

## Pins used (all verified by the counter's sha256 pins)

- candidate: `99485e9e1ff966d950b47d3d8924a5e7b7360854bf8627c8258bab9db27922f6` first, then
  `ddbcd6e3cec2d484aa78038f1eee96ed86eb6dd436b65b3046f42315b5f09cbb` (the builder seat edited the
  candidate three times during this seat; 36-byte mutants and all 12 cases below target
  **ddbcd6e3**). The seat's own initial copy is kept as `candidate-old.py` for provenance.
- counter `quality/counters/c1-r91-mime-resolution.py` `dc97fd643c4a7ab6b9337d7a91325884af180894988e28b3de014c51ddcb44e2`
  (it gained `--fuzz-gen/--expect-fuzz-sha256` and the QUALITY-148 crashed-not-killed rule mid-seat).
- oracle `c3a13e26173a0eca8bf137ced141c53485f7eca588d426ae6b636a52577bf6a8`; gio
  `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`; libgio
  `b38001cca69b2890a22fd3f6590bea7392bf489009de7ddfb6dbf296a133685e`.
- L1 cases snapshot `42a08f2cc19f137ac591df5f558e0fb2fba65c7471ce0760e2d755497c53e874` (89 cases;
  identical to the lane file at both final runs).
- fuzz generator snapshot `ce7a60d4eca9c891ec1d7ec26d9a3510ad04e7d71be53df408db20e3b3c54979`.
- merged labelled case set (scratch, L1 + mc): `b5b45b2d1edd8450b1a6986b9435ff1a20752990a6ff13afce27edbd4f3fa840` (101 cases).

Snapshots were taken because sibling seats changed `mime-cases-r91-l1.json` and `fuzz-gen-r91.py`
during the seat (two counter runs aborted with `SETUP_ERROR sha256 mismatch` before I started
pinning copies).

## Method

For each mutant: apply `find`→`replace` to the candidate copy in `$S`, then run the frozen counter
with `--draft-tool <mutated copy>` against the 89 labelled L1 cases and the pinned oracle. A mutant is
**killed** when at least one case gets a well-formed wrong answer; a mutant whose only failures are
crashes is **crashed-not-killed** (counter's QUALITY 148 rule). The counter verifies `find` occurs
exactly once in the tool and applies the same sandbox as the measurement (bwrap: `/usr/bin/gio` and
libgio masked with `/dev/null`, lane repo on tmpfs, network unshared). All 36 mutated sources compile
(`compile()` in the builder) and none crashed.

DRAFT counter summary on the **89 L1 cases** only (candidate ddbcd6e3):

```
MADO_MIME_RESOLUTION: DRAFT_TARGET_MISSED pred=PRED-C1-r91-v1 ... cases=89 correct=89 l1=89/89
fresh=120/120 fresh_seed=3720140515 mutants=36 killed=24 crashed_not_killed=0 oracle_agree=89/89
do_nothing_correct=7 naive_mimeapps_correct=6 cache_only_correct=24 base_tool_correct=0
base_tool=absent tool_sha256=ddbcd6e3…
```

24 killed, 12 survived, 0 crash-only. The counter exits 3 for a draft run; `DRAFT_TARGET_MISSED` here
is expected because 12 mutants survive the L1 set alone.

## Mutant verdicts (L1 89 cases) and the case that kills each survivor

| id | modelled rule | L1 verdict | wrong | crashed | extra case |
|---|---|---|---|---|---|
| X01 | desktop token validation also accepts '.' | killed | 1 | 0 | - |
| X02 | user data dir ranked below the system data dirs | killed | 3 | 0 | - |
| X03 | mimeapps.list read before the desktop-specific lists | killed | 1 | 0 | - |
| X04 | desktop-specific lists read in reverse desktop order | killed | 2 | 0 | - |
| X05 | Removed Associations ungated in non-desktop-specific files | SURVIVED | 0 | 0 | mc-01, mc-02 |
| X06 | mimeinfo.cache read as [Added Associations] | killed | 56 | 0 | - |
| X07 | expand_strv keeps blocklisted ids | killed | 1 | 0 | - |
| X08 | expand_strv keeps duplicate ids | SURVIVED | 0 | 0 | equivalent (argued below) |
| X09 | root type not unaliased in type_list | killed | 2 | 0 | - |
| X10 | masking demands a loadable higher file | killed | 3 | 0 | - |
| X11 | masking only against the user config dir | killed | 3 | 0 | - |
| X12 | default taken without checking that the id loads | killed | 15 | 0 | - |
| X13 | blocklist reset for every ancestor type | killed | 1 | 0 | - |
| X14 | any Hidden key hides the file | killed | 1 | 0 | - |
| X15 | desktop file without Type loads | SURVIVED | 0 | 0 | mc-03 |
| X16 | TryExec resolved only on the system PATH | killed | 1 | 0 | - |
| X17 | desktop file with no Exec rejected | killed | 2 | 0 | - |
| X18 | any line starting with '[' is a group header | killed | 1 | 0 | - |
| X19 | group names not validated | SURVIVED | 0 | 0 | mc-04 |
| X20 | duplicate group resets earlier keys | killed | 1 | 0 | - |
| X21 | first duplicate key wins the value | killed | 1 | 0 | - |
| X22 | key name keeps trailing whitespace | killed | 1 | 0 | - |
| X23 | value keeps leading whitespace | killed | 2 | 0 | - |
| X24 | invalid UTF-8 decoded lossily instead of skipping the file | SURVIVED | 0 | 0 | mc-12 |
| X25 | escaped semicolon rejected in a string list | killed | 1 | 0 | - |
| X26 | fgets chunk one byte too wide | SURVIVED | 0 | 0 | mc-05 |
| X27 | mime.cache 1.1 rejected | SURVIVED | 0 | 0 | mc-06 |
| X28 | parent list not capped at 127 | SURVIVED | 0 | 0 | mc-07 |
| X29 | parents taken in reverse order | killed | 2 | 0 | - |
| X30 | only direct parents collected (no transitive ancestors) | killed | 1 | 0 | - |
| X31 | registered list computed without ancestors | killed | 14 | 0 | - |
| X32 | the last cache's alias wins | SURVIVED | 0 | 0 | mc-08 |
| X33 | cache alias bsearch misses a one-entry list | killed | 1 | 0 | - |
| X34 | mime.cache smaller than the 40-byte GLib header accepted | SURVIVED | 0 | 0 | mc-11 |
| X35 | cache duplicate parent entry: last entry wins | SURVIVED | 0 | 0 | mc-09 |
| X36 | repeated key moves to its last position | SURVIVED | 0 | 0 | mc-10 |

## The 12 new cases (DRAFT labels from the pinned oracle; delivered unlabelled)

Each case isolates one surviving mutant. Candidate = `candidate.py` (ddbcd6e3); "mutant" is the
mutated copy; every row below is a kill (candidate matches the oracle, mutant does not).

| case | type | oracle default | candidate | mutant | mutant default |
|---|---|---|---|---|---|
| mc-01-desktop-specific-removal-not-permitted | text/plain | a.desktop | a.desktop | X05 | b.desktop |
| mc-02-defaults-list-removal-not-permitted | text/plain | a.desktop | a.desktop | X05 | b.desktop |
| mc-03-desktop-file-without-type-does-not-load | text/plain | b.desktop | b.desktop | X15 | a.desktop |
| mc-04-invalid-group-name-voids-the-file | text/plain | a.desktop | a.desktop | X19 | c.desktop |
| mc-05-fgets-254-byte-chunk-chops-the-parent | app/x | b.desktop | b.desktop | X26 | a.desktop |
| mc-06-mime-cache-1-1-is-read | app/x | a.desktop | a.desktop | X27 | none |
| mc-07-parent-list-capped-at-127 | app/x | none | none | X28 | a.desktop |
| mc-08-first-cache-alias-wins | app/x | a.desktop | a.desktop | X32 | b.desktop |
| mc-09-cache-first-parent-entry-wins | app/x | a.desktop | a.desktop | X35 | b.desktop |
| mc-10-repeated-key-keeps-first-position | image/png | c.desktop | c.desktop | X36 | d.desktop |
| mc-11-mime-cache-shorter-than-40-bytes-rejected | app/x | a.desktop | a.desktop | X34 | none |
| mc-12-invalid-utf8-comment-does-not-void-the-file | text/plain | c.desktop | c.desktop | X24 | a.desktop |

What each case pins down (reproducing inputs are the case files themselves):

- **mc-01**: `[Removed Associations]` in `<desktop>-mimeapps.list` is not permitted and is ignored
  (gdesktopappinfo.c:901-990 `tweaks_permitted=FALSE` warning path, :1012-1016). The mutant honours
  it and loses `a.desktop`.
- **mc-02**: same for `defaults.list` (read with `ADDED_ASSOCIATIONS_GROUP, FALSE`,
  gdesktopappinfo.c:1038-1042), cross-directory so the removal would block a lower data dir's cache
  addition.
- **mc-03**: a desktop file with no `Type` does not load (`type == NULL` fails,
  gdesktopappinfo.c:1915-1921); the mutant accepts a missing Type.
- **mc-04**: an invalid group name voids the file (`Invalid group name`, gkeyfile.c:1696-1701); the
  mutation accepts any name and picks up the later `[Default Applications]`.
- **mc-05**: `fgets(line, 255)` chops the last byte of a 254-byte chunk (xdgmimeparent.c:141-149), so
  a parent id ending exactly at the chunk boundary loses its last character; the mutant reads 255
  bytes and resolves the full id.
- **mc-06**: mime.cache 1.1 is read (`MINOR_VERSION_MIN 1`, xdgmimecache.c:64-65, :137-139); the mutant
  rejects it.
- **mc-07**: a cache type carries at most 127 parents (`p < 127`, xdgmimecache.c:1068, :1101); the
  128th parent does not count, so no default exists; the mutant returns one.
- **mc-08**: unalias consults the caches in order (`cache_alias_lookup` loops `_caches`, 
  xdgmimecache.c:315-360), so the user data cache's alias wins; the mutant takes the last cache.
- **mc-09**: a duplicate type entry in one cache: the linear scan breaks at the first match
  (xdgmimecache.c:1078-1112), so the first entry's parents win; the mutant keeps the last.
- **mc-10**: a repeated key keeps its first position and takes its last value (below).
- **mc-11**: a mime.cache shorter than the 40-byte header is not a cache (xdgmimecache.c:126-128), so
  the dir stays a text dir; the mutant accepts it and suppresses the text aliases.
- **mc-12**: invalid UTF-8 in a comment does not void a key file (below).

## X08 equivalence (argued, not counted)

`expand_strv`'s duplicate filter only removes ids the consumers skip anyway:
`desktop_file_dir_mime_lookup` skips ids already in `hits`/`blocklist`
(gdesktopappinfo.c:1330-1348), `desktop_file_dir_default_lookup` skips ids already in `results`
(:1361-1372), and GLib itself stores the first list without dedup when the target is NULL
(:862-866). No case can distinguish the mutant; it is recorded in `equivalent_not_counted`.

## Findings against the candidate (three, all fixed by the builder during this seat)

The seat found three places where the candidate disagreed with the installed GLib; each was reproduced
with an mc case, and the builder's ddbcd6e3 revision fixes all three (the cases now pass and the
mutants that reintroduce the old behaviour are killed by them).

1. **Repeated key position (mc-10).** At `99485e9e` (and earlier) `parse_keyfile` did
   `grp.pop(key, None); grp[key] = value`, i.e. a repeated key moved to its last position. GLib parses
   every pair into `key_value_pairs` (`g_key_file_add_key_value_pair`, gkeyfile.c:4420-4427; called at
   :1798) and `g_key_file_get_keys` fills its array from the end (:2005-2045), so keys are visited in
   file order and the hash lookup returns the last value: a repeated key is processed at its *first*
   position with its *last* value. Observed: mc-10 oracle `c.desktop`, old candidate `d.desktop`. The
   fix in ddbcd6e3 (in-place `grp[key] = value`) makes mc-10 pass; X36 reintroduces the pop and the
   case kills it.
2. **mime.cache size (mc-11).** `load_mime_cache` accepted buffers `>= 12` bytes; xdgmimecache.c:127
   requires `st.st_size >= 40`, so a 12–39-byte `mime.cache` makes the dir a text dir in GLib and a
   cache dir in the old candidate (text aliases silently dropped). Observed: mc-11 oracle
   `a.desktop`, old candidate none. ddbcd6e3 has `len(buf) < 40`; X34 reverts to 12 and is killed.
3. **Invalid UTF-8 in key files (mc-12).** The old `load_keyfile` did a strict
   `data.decode("utf-8")`, voiding a whole file on any invalid byte. GLib reads bytes
   (`g_key_file_load_from_fd` → `g_key_file_parse_data`, gkeyfile.c:174-2000 region) and validates only
   a value that is read (`g_key_file_get_string` :2310, `g_key_file_get_string_list` :2427); invalid
   bytes in comments or unread keys void nothing. Observed: mc-12 oracle `c.desktop` (file applied),
   old candidate `a.desktop` (file skipped). ddbcd6e3 decodes with `surrogateescape` and checks values;
   X24 restores the strict decode and is killed.

These were also visible in the fresh leg: at the old candidate the counter's fresh leg scored
**110/120** (seed 2036618841; 10 wrong); the in-place-key mutant X36 alone lifted it to 115/120, and at
ddbcd6e3 the fresh leg is **120/120** (seed 3720140515). The 10 failing ids at the old candidate were
fz-2036618841-001/010/017/031/047/056/068/078/083/093; reproducible with
`fuzz-gen-r91.py 2036618841 120` (frozen generator sha above). The fresh leg is the fuzz seat's
surface; recorded here only as corroboration for the three fixes.

## Merged-set DRAFT result

The L1 set plus the 12 mc cases (101 cases, labelled by the pinned oracle into a scratch file,
`b5b45b2d…`; reconstructible by concatenating the 89 labelled L1 cases with the 12 mc cases labelled
by `oracle-snapshot.py` c3a13e26…) scores, with the delivered mutants file:

```
MADO_MIME_RESOLUTION: DRAFT_TARGET_MISSED pred=PRED-C1-r91-v1 ... cases=101 correct=101 l1=89/89
mc=12/12 fresh=120/120 fresh_seed=3720140515 mutants=36 killed=35 crashed_not_killed=0
oracle_agree=101/101 do_nothing_correct=8 naive_mimeapps_correct=7 cache_only_correct=28
base_tool_correct=0 base_tool=absent tool_sha256=ddbcd6e3…
```

35 of 36 mutants are killed by the merged set; the one survivor is X08, the argued equivalent. The
predicate requires `killed == mutants`, so the L1 must either drop X08 or move it to
`equivalent_not_counted` when it builds the frozen mutant list (my file keeps it in `mutants` and also
records it under `equivalent_not_counted`, the same shape as `mime-mutants-r91-l1.json`).

## Cross-seat notes for the L1 (not this seat's files)

- `controls/mime-mutants-r91-l1.json` (sha `059e77f7…` at this reading) has four `find` strings that
  no longer occur in candidate ddbcd6e3: **M24** (`return self.alias_map.get(t, t)` — the alias map is
  gone), **M28** (`if "[" in key: continue` — the locale condition was rewritten), **M29** (the
  single-line Encoding condition was split), **M33** (the cache version/size condition was split).
  The counter aborts with `SETUP_ERROR mutant Mxx: find occurs 0 times` unless these are refreshed;
  the merged mutant set cannot be scored as-is.
- The counter now requires `--fuzz-gen`/`--expect-fuzz-sha256` and treats crash-only mutants as
  `crashed-not-killed`; any earlier invocation without those flags exits 2.
- `mime-cases-r91-l1.json` and `fuzz-gen-r91.py` changed under this seat; the shas above are the ones
  actually used.

## Commands (all read-only except my three owned files)

| command | rc | note |
|---|---|---|
| counter `--draft-tool` candidate 79645659, 89 L1 cases, 36 mutants | 3 | DRAFT; `killed=24`, `SURVIVED=12`, fresh 110/120 |
| counter `--draft-tool` candidate ddbcd6e3, 89 L1 cases, 36 mutants | 3 | DRAFT; `killed=24`, `SURVIVED=12`, fresh 120/120 |
| counter `--draft-tool` candidate ddbcd6e3, merged 101 cases, 36 mutants | 3 | DRAFT; `killed=35`, X08 survived, candidate 101/101 |
| `build_mc_cases.py` (oracle labels + candidate/mutant answers on mc-01…12) | 0 | 12/12 candidate-correct, 12/12 mutant-wrong |
| `probe_cases.py`, `probe_more.py`, `check_fresh_x36.py` (probes) | 0 | reproduced each scenario before it became a case |
| two earlier counter invocations | 2 | `SETUP_ERROR sha256 mismatch` after sibling edits (case file, then fuzz gen); fixed by snapshots |

Dead steps: the first counter call exited 2 on the counter's new required `--fuzz-gen`; the next two
DRAFT attempts exited 2 on stale pins while sibling seats edited the case file and the fuzz generator
(the error text is in `$S/mutant-run.log`, `mutant-run3.log`; scratch deleted at exit, the text is
quoted above). No tool installs were made.

## Restoration evidence

No lane byte was mutated: every `find`→`replace` was applied to copies under `$S`
(`candidate.py`, `candidate-old.py`, `probe-mut/Xxx.py`), and `$S` was removed at exit. The lane
candidate's own sha moved from `79645659…` to `99485e9e…` to `ddbcd6e3…` **by the builder seat**, not
by this one; this seat never wrote `build/`, `quality/`, or the L1 controls. The only lane writes are
the two control files and this report, hashes in the first table.
