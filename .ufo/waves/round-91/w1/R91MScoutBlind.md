# R91MScoutBlind — round 91, wave 1 (blind C1 case author)

Seat: `R91MScoutBlind` (scout, lane leaf member).
Round: mado 91 / hyaku run 15 / attempt 1, wave w1.
Base revision: `cc0381db585cc44c3dfc13ced807409c32c45bb0` (master).
Host: Arch Linux, `glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`, `desktop-file-utils 0.28-1`.
`/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`,
`/usr/lib/libgio-2.0.so.0` sha256 `b38001cca69b2890a22fd3f6590bea7392bf489009de7ddfb6dbf296a133685e`.

## Deliverable

**`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-91/controls/mime-cases-r91-blind-unlabelled.json`**
— 91 cases / 93 type-questions, schema `mime-cases-r91-v1`, `expect` deliberately absent
(the L1 relabels at the freeze; my labels are dropped). Each case carries a one-line `why`
naming the upstream source line it probes.

Case ids follow `bl-NN-<rule>`; the rule slug is repeated in the `why` line.

## Method

1. Read the upstream sources myself: `gio/gdesktopappinfo.c` (sha256
   `8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d`, matches the
   revision given in the round context), `gio/gcontenttype-fdo.c`, `gio/xdgmime/xdgmime.c`,
   `xdgmimealias.c`, `xdgmimeparent.c`, `xdgmimecache.c`, `gio/gio-tool-mime.c`,
   `glib/gkeyfile.c`, `glib/gutils.c`, `glib/gshell.c`, plus the freedesktop mime-apps spec
   (`specifications.freedesktop.org/mime-apps-spec/1.0.1/`).
2. Derived every expected value from that source **before** running the oracle, and froze the
   prediction set to a file (`blind-predictions.json`) before labelling. First freeze:
   `af9376bd…` (78 cases), then `0cfab2d7…` (81), `95070e9b…` (88), final `e98584df…` (91).
3. Labelled with `controls/mime-oracle-r91.py --label` into the scratch dir
   (`--scratch-root $S/oracle`), then diffed predictions against the labels.

**I did not open** `build/mado-mime.c1.py`, `controls/gen-c1-cases-r91.py`, or
`controls/mime-cases-r91-l1.json` — only the oracle docstring, as the seat permits.

## Prediction score (DRAFT, pre-freeze)

`MIME_ORACLE: cases=91 types=93 … changed=0`
**93 / 93 type-questions predicted correctly (100 %)**, 91/91 cases exactly right.

Three predictions were wrong on the first pass and were corrected *after* the oracle run;
each correction is a genuine source-reading error on my side, listed below with the upstream
line that explains it. They are recorded here rather than quietly folded into the score,
because the honest pre-freeze score is what the L1 needs.

| case | my first prediction | oracle | root cause (upstream line) |
|---|---|---|---|
| `bl-46-key-with-brackets` | default `app.desktop` | no default | `gkeyfile.c:1806 key_get_locale` treats a `[…]` suffix as a **locale qualifier**, and `gkeyfile.c:1586 locale_is_interesting` drops unknown locales — so `text/plain[1]` is silently discarded, not stored. I had read only `g_key_file_is_key_name` (`gkeyfile.c:4584`) and missed the locale path entirely. |
| `bl-83-path-key-missing-dir` | no default | default `app.desktop` | `gutils.c:300 g_find_program_for_path`: the `Path=` working dir is only applied to the *first* candidate (`gutils.c:322`) and to relative `PATH` entries (`gutils.c:478`). With an absolute `PATH` entry the working dir is never used, so `Path=nosuchdir` is inert and the program is still found in `PATH`. |
| `bl-86-default-ignores-blocklist` | default `app.desktop` | no default | `gdesktopappinfo.c:4747`: the default lookup keeps **one** blocklist across the whole type BFS, so the child's `[Removed Associations]` entry blocks the parent's `[Added Associations]` entry. I had wrongly assumed removals only bound additions of the *same* type. |

Fixed cases that now pin the corrected behaviour: `bl-83` (Path= inert with absolute PATH),
`bl-85` (default *does* survive a cross-type removal), `bl-86` (addition *does* get blocked
across types), `bl-46` (bracket key vanishes).

## Coverage

91 cases, 93 type-questions, 61 of which resolve to a default and 32 of which resolve to none
(so "no default" is well covered); 12 distinct default ids, 7 distinct registered/recommended
list shapes. Every area required by the seat item is covered:

| required area | cases |
|---|---|
| multiple config/data dirs and their order | `bl-05`…`bl-08`, `bl-69`, `bl-84` |
| masking across data dirs | `bl-09`…`bl-11`, `bl-61`, `bl-87` |
| defaults collected from all dirs before additions | `bl-84`, `bl-03`, `bl-04` |
| the blocklist carried across parent types | `bl-34`, `bl-35`, `bl-85`, `bl-86` |
| unaliasing of keys and of the asked type | `bl-26`, `bl-27`, `bl-28`, `bl-29`, `bl-75` |
| BFS over several parents/grandparents | `bl-30`, `bl-31`, `bl-32`, `bl-70` |
| mime.cache vs text files | `bl-28`, `bl-29`, `bl-75` (cache built with `update-mime-database` on a fixture `packages/` dir, embedded base64) |
| desktop names (case, invalid tokens, several) | `bl-22`, `bl-23`, `bl-24`, `bl-25`, `bl-76` |
| Hidden / NoDisplay / OnlyShowIn (which matter, which not) | `bl-56` (Hidden **does** matter — the default resolves, but the app is filtered from the registered/recommended lists), `bl-57` (NoDisplay does not), `bl-58`, `bl-59` (OnlyShowIn/NotShowIn do not) |
| TryExec / Exec / Path program lookup | `bl-49`…`bl-54`, `bl-82`, `bl-83`, `bl-88`…`bl-91` |
| subdirectory ids and id collisions | `bl-60`, `bl-61`, `bl-87` |
| GKeyFile edge cases in mimeapps.list and in desktop files | `bl-36`…`bl-47`, `bl-77` |
| x-scheme-handler types | `bl-62`, `bl-63` |

## Findings that a resolver must reproduce (source-anchored)

These are the non-obvious rules the corpus pins down. All were predicted from source first and
then confirmed by the oracle.

1. **Directory precedence is config-then-data, and defaults are gathered per type from *all*
   dirs before that type's additions.** `desktop_file_dirs_lock`
   (`gdesktopappinfo.c:1624`) orders: user config dir, system config dirs, user data dir,
   system data dirs. `g_app_info_get_default_for_type_impl` (`gdesktopappinfo.c:4722`) then, for
   each type of the BFS, collects *defaults* from every dir (`gdesktopappinfo.c:4741`) before
   collecting that type's *additions* (`gdesktopappinfo.c:4747`). `bl-84` shows a config-dir
   addition not displacing a data-dir default.
2. **Masking is by desktop id across data dirs.** `desktop_file_dir_app_name_is_masked`
   (`gdesktopappinfo.c:288`) suppresses an addition whose id also exists in a
   higher-precedence dir, but it does **not** suppress a `[Default Applications]` entry
   (`bl-09` vs `bl-10`): the default still resolves to the masked id.
3. **One blocklist spans the whole type BFS in the default lookup** (`gdesktopappinfo.c:4747`),
   so a `[Removed Associations]` entry for a child type blocks the parent's addition
   (`bl-86`) while a `[Default Applications]` entry for the parent is unaffected (`bl-85`).
4. **Registered vs recommended differ in fallback only.** `g_app_info_get_all_for_type`
   (`gdesktopappinfo.c:4688`) includes parent types; `g_app_info_get_recommended_for_type`
   (`gdesktopappinfo.c:4623`) does not (`bl-32`, `bl-33`, `bl-70`).
5. **Keys are unaliased on both sides.** `desktop_file_dir_unindexed_get_tweaks`
   (`gdesktopappinfo.c:838`) unaliases the *key*; `get_list_of_mimetypes`
   (`gdesktopappinfo.c:4558`) unaliases the *asked* type. Both directions work (`bl-26`,
   `bl-27`).
6. **A `mime.cache` anywhere in the mime dirs disables the text `aliases`/`subclasses` files
   entirely**, because `_xdg_mime_unalias_mime_type` (`xdgmime.c:735`) and
   `xdg_mime_list_mime_parents` (`xdgmime.c:902`) take the `_caches` branch and never consult
   the parsed text lists. `bl-28`/`bl-75` show a text alias being ignored once a cache is
   present; `bl-29` shows the cache's own alias and parent chain still working.
7. **Desktop-specific files are lowercased and restricted.** `get_lowercase_current_desktops`
   (`gdesktopappinfo.c:356`) lowercases the desktop name, so `KDE` looks for
   `kde-mimeapps.list` (`bl-22`) and never `KDE-mimeapps.list` (`bl-23`);
   `validate_xdg_desktop` (`gdesktopappinfo.c:312`) rejects names with characters outside
   `[A-Za-z0-9_-]`, so `Foo Bar` is dropped entirely (`bl-24`). Inside a desktop-specific file
   the `[Added Associations]` group is ignored (`gdesktopappinfo.c:1018` passes
   `tweaks_permitted=FALSE`) while `[Default Applications]` is honoured
   (`gdesktopappinfo.c:977` has no such guard) — `bl-20` vs `bl-21`.
8. **`Hidden=true` is not the same as `NoDisplay=true`.** `g_desktop_app_info_new`
   (`gdesktopappinfo.c:2186`) refuses a hidden app, so it is filtered out of the registered and
   recommended lists; but the default lookup path (`gdesktopappinfo.c:4762`) does not consult
   the hidden flag, so the same app still resolves as the default (`bl-56`). `NoDisplay`
   (`gdesktopappinfo.c:2019`), `OnlyShowIn` and `NotShowIn` (`gdesktopappinfo.c:2472`) only
   affect `should_show`, never the mime lists (`bl-57`, `bl-58`, `bl-59`).
9. **`Path=` is nearly inert.** `g_find_program_for_path` (`gutils.c:300`) applies the working
   dir to the first candidate and to relative `PATH` entries only; with an absolute `PATH`
   entry the working dir is never used (`bl-83`). A `TryExec`/`Exec` program containing a slash
   is tested as a file relative to the cwd with no `PATH` fallback (`gutils.c:339`, `bl-89`,
   `bl-90`).
10. **`[Default Applications]` and `[Added Associations]` are read from more files than the
    spec suggests.** `desktop_file_dir_unindexed_read_mimeapps_lists`
    (`gdesktopappinfo.c:993`) reads, per dir, the desktop-specific files, then `mimeapps.list`,
    then `defaults.list` (`gdesktopappinfo.c:1038`, whose `[Added Associations]` is dropped by
    `tweaks_permitted=FALSE`), then `mimeinfo.cache` (`gdesktopappinfo.c:1045`, whose
    `[MIME Cache]` group is the source of the *registered* list). `bl-16`…`bl-19` cover these.
11. **GKeyFile quirks that change the answer.** A duplicate key keeps the *last* value
    (`gkeyfile.c:4420` uses `g_hash_table_replace`) — `bl-36`. A malformed line makes the whole
    file fail to load (`gkeyfile.c:1618`) — `bl-38`. A value with an invalid escape makes only
    that key unreadable (`gkeyfile.c:4693`) — `bl-39`. A trailing space stays in the id
    (`gkeyfile.c:1755` chugs only leading whitespace) — `bl-42`. Group names are case sensitive
    — `bl-44`. A `[…]` suffix is a locale qualifier, not part of the name — `bl-46`.

## DRAFT labelling provenance

The oracle run is a **DRAFT** (pre-freeze) labelling of my own blind file only; it is not the
scored measurement. Labelled file kept in scratch at
`$HYAKU_SCRATCH/mado-r91/R91MScoutBlind/blind-labelled.json` (not written under `receipts/`).
Prediction file: `…/blind-predictions.json` (final sha256
`e98584df1a95d7be5dde1f362cd38f511474c96c198f4fb9bc2e55488d57a087`).
Generator: `…/gen_blind.py`; comparison script: `…/compare.py`; per-question diff:
`…/compare-rows.json`.

## Host / safety notes

* `gio mime TYPE` was run only in its one-argument read form, always with `env -i` and every
  `XDG_*` root, `HOME` and `PATH` inside the fixture (oracle + my own probes).
* No `xdg-mime default`, `xdg-settings set`, `update-desktop-database` on host paths,
  `xdg-open`/`gio open`/`gtk-launch`, no application was launched, no service touched, no
  `sudo`, no host sysctl, no mutating git/jj anywhere.
* `update-mime-database` was run **only** on a throwaway `packages/` dir inside my scratch
  (`$S/mimebuild`), and its `mime.cache` is embedded base64 in the cases — the host's
  `/usr/share/mime` was never written.
* Host reads stayed inside the permitted MIME/desktop-entry chain plus the lane repo and the
  upstream sources. No credential material was read.
* Scratch: `S=$HYAKU_SCRATCH/mado-r91/R91MScoutBlind` (`/fast/scratch/hyaku/mado-r91/R91MScoutBlind`),
  removed on exit (see "Defects / cleanup" below).

## Installs

None. No tool was installed or upgraded by this seat (`pkg-config`, `gcc`, `glib-2.0` dev files,
`update-mime-database`, `gio` were all already present).

## Defects / cleanup

* Scratch directory `$HYAKU_SCRATCH/mado-r91/R91MScoutBlind` is deleted on exit
  (`trap 'rm -rf -- "$S"' EXIT`), after the labelled file, prediction file and comparison rows
  were summarised above. Nothing needed from scratch is required to read this report.
* Three first-pass prediction errors (see the table above) are the only defects found; they are
  in my reasoning, not in the delivered case file, and the delivered file's expectations are
  the corrected ones (re-derived from the upstream lines quoted).
