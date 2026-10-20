# ReopenS058 — S058 re-opened against source bytes

Lane HEAD verified: `988b858bd6049bc709807534fd725c05264f7e60` (pushed).
Installs: **none**. No pacman/sudo/systemctl/hyprctl/live probe was run; nothing
below executed Alacritty, xdg-terminal-exec, the launcher chain or the compositor.

Row under attack:

- `corpus/SOURCES.md:70` — S058, `docs`, tier `A`, status `mined`, `2026-10-20`,
  recheck `on-release`, used-by `corpus/knowledge/terminal-route-r17.md`.
- `corpus/lessons/round-17.md:45` — § Gate line, quote at `alacritty.5.scd:35-37`,
  16 words, digest `e444fa45…c4107`.

## Verdict

**The attack failed.** No claim in the row, the gate line, or the citing note is
falsified by the source bytes. Every stated anchor exists, the quoted sentence is
verbatim (modulo the manual's own line wrapping), the digest and byte count replay
exactly, and the recorded tag object and peeled commit both match the live ref
advertisement for `v0.17.0`.

Two precision defects were found, both *under*-citations that never overstate the
source. They are recorded in § Counterexamples below and are not falsifications.

## Replay (raw bytes, `curl`)

```
curl -sS -o /tmp/s058.scd \
  https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd
sha256sum /tmp/s058.scd
  e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107  /tmp/s058.scd
wc -c  -> 28787
```

Digest **exact match** to the SOURCES anchor cell and to the gate line; byte count
**exact match** to the row's `28787 bytes`. File is 1075 lines, UTF-8.

## Tag identity (row's `scope` cell)

`api.github.com` returned **HTTP 403, rate-limited for this IP**, so the REST tag
endpoint was not usable. The git smart-HTTP ref advertisement was fetched with
`curl` instead (read-only, no `git` binary, no `git ls-remote`):

```
curl -sS "https://github.com/alacritty/alacritty.git/info/refs?service=git-upload-pack"
```

| ref | advertised object | row claims | verdict |
|---|---|---|---|
| `refs/tags/v0.17.0` | `dc946285396bd3e251b6942af7e9961b74f76bee` | tag object `dc946285…f76bee` | **match** |
| `refs/tags/v0.17.0^{}` | `94e7c8874e526b1e67b349d9ba30ddf81669119e` | commit `94e7c887…119e` | **match** |

(Leading 4-hex pkt-line length prefixes stripped; the six 40-hex values in the
advertisement are the only tag objects present.) Note the tag is annotated, not
lightweight — consistent with the row recording a *tag object* and a peeled commit,
unlike S056 which correctly records a lightweight ref object.

## Anchor inventory (stated anchors, verbatim text)

GENERAL section spans lines 27-68; the next header is `# ENV` at line 69, so both
`import` and `live_config_reload` are documented in the `[general]` table —
supporting the row's `general.import` phrasing (line 29: "This section documents
the *[general]* table of the configuration file.").

| anchor | verbatim line(s) | supports |
|---|---|---|
| 27 | `# GENERAL` | section scope for `general.import` |
| 31 | `*import* = [_"<string>"_,]` | the key exists; takes a list of strings |
| 33 | `Import additional configuration files.` | key purpose |
| 35-36 | `Imports are loaded in order, skipping all missing files, with the importing` / `file being loaded last. If a field is already present in a previous import,` | order; missing files skipped; importing file loaded last |
| 37 | `it will be replaced.` | later-import precedence |
| 39-41 | `All imports must either be absolute paths starting with _/_, paths relative` / `to the user's home directory starting with _~/_, or paths relative from the` / `current config file.` | three path forms incl. relative-to-importing-file |
| 57 | `*live_config_reload* = _true_ | _false_` | key exists; boolean |
| 59 | `Live config reload (changes require restart)` | key meaning |
| 61 | `Default: _true_` | default is true |

Quote check (whitespace-normalized over lines 35-41):
`"Imports are loaded in order, skipping all missing files, with the importing file being loaded last."`
is **present, 16 words** (≤25). Un-normalized `grep -F` returns 0 hits only because
the sentence is wrapped at `importing` / `file`; that is the manual's formatting, not
a mismatch. The sentence's terminal period falls at the end of **line 36**; line 37
opens a new sentence (`it will be replaced.`).

No contradicting statement exists in the file: `import` occurs only at 31, 33, 35,
36, 39, 44; `live_config_reload` only at 57 (the prose form at 59). There is no
second, conflicting default for the key and no "missing import is an error" clause.

## Gate line (`corpus/lessons/round-17.md:45`)

- URL — **matches** the SOURCES row exactly.
- Quote — **verbatim**, 16 words, ≤25.
- Digest — **matches** replay byte-for-byte.
- Tier `A` — consistent with the established scale in the same registry (tagged
  upstream project docs are A: cf. S005, S016, S018; community wiki is C, cf. S061).
  Upstream-tagged first-party manual, so A holds and is scoped, not global.
- Status `mined` — correct for a row with a real `used-by` note (legend: only
  `status`, `recheck`, `used-by` change in place; row is new, opened 2026-10-20).
- Recheck `on-release` — consistent with the other tag-pinned upstream rows
  (S005, S018); a tag-pinned doc re-opens when the pinned tag is superseded.
- Verdict-bearing cell (`teaches`) — all four clauses check out, see next section.
- Tier/status/verdict are not carried in the gate table itself (its columns are
  `id | URL / path | located quote | sha256` for every row, not just S058); they
  live in the SOURCES row. Not an S058-specific defect.

## `used-by` note, claim by claim

`corpus/knowledge/terminal-route-r17.md` (header `source:` line cites
`alacritty.5.scd:27-41,57-61`, a superset of the row's `27,31,35-41,57-61`):

1. "`general.import` (alacritty.5.scd:31): imports are loaded in order and missing
   files are skipped." — **supported**, lines 31 + 35-36.
2. Quote at 35-37, 16 words — **verbatim**, supported.
3. "Path forms (alacritty.5.scd:39-40): 'paths relative to the user's home directory
   starting with' `~/` are accepted, as are absolute paths and paths relative to the
   importing file." — **substance supported**: absolute (`_/_`, line 39), `~/` (39-40),
   and relative-to-current-config (40-41). See nit 1: the stated anchor 39-40 stops
   one line short of `current config file.` (41) for the third form.
4. "`live_config_reload` (alacritty.5.scd:57-61): 'Live config reload (changes
   require restart)'; 'Default: true'." — **supported** (59, 61). See nit 2 on the
   rendered `_true_`.
5. "The documented `live_config_reload` default is `true`." — **supported** (61).
6. "The documented import rule means a missing theme file would be skipped, not
   fatal." — **supported** (35, "skipping all missing files").
7. "Whether … a skipped missing import does [reload] … were not observed." —
   **correctly left [UNK]**; the source is silent on reload-vs-skip interaction.
8. "No `live_config_reload` key" in the host `alacritty.toml` — host fact, S059
   scope, not a claim *from* S058; not adjudicated here.

No claim in the note attributes to S058 anything the tag bytes do not say. The
row's own scope caveat — "tag docs do not prove the host binary" — is the correct
boundary and the note respects it (`[INF-docs]`, no behaviour claimed).

## Counterexamples (precision only)

1. **Gate/note quote anchor is one line wide.** The gate line and note both state
   `35-37`, but the quoted sentence terminates inside line 36; line 37 is the
   separate sentence `it will be replaced.` The anchor is a *superset* of the
   quote, so the quote remains verifiable at the stated range — no claim is
   overstated. Tightening to `35-36` would be exact.
2. **Note renders AsciiDoc emphasis as plain text.** The file's literal is
   `Default: _true_` (line 61, leading tab), as is `_true_ | _false_` at 57; the
   note quotes `Default: true` and the gate's sibling claims use the rendered form.
   This is markup rendering, not a content edit — the default *value* is `true`.
   A strict "verbatim" reading would keep the underscores.

Neither defect changes a truth value, a digest, or the tier/status verdict; both
are under-citations, and an under-citation cannot make a false claim true.

## Remaining unknowns

- [UNK] The REST tag object could not be re-read (`api.github.com` 403, rate
  limit). Tag identity was established from the ref advertisement instead; the
  annotated tag object SHA and peeled commit both match the row exactly. If a
  later check needs the API object body, it must wait out the rate limit or use
  an authenticated channel.
- [UNK] Whether `v0.17.0` was force-moved since the row was written. Not
  determinable from current refs; the raw digest is the guard, and it replays
  today, so row-time and now agree.
- Out of scope by item: whether the installed host binary matches the tag docs
  (the row explicitly declines that claim), and the `pacman.log` version binding.
