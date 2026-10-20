# ReopenS065 — source row S065 re-opened against live bytes

Scout: MadoR17.ReopenS065. Lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`.
Target row: `corpus/SOURCES.md:77`. Gate line: `corpus/lessons/round-17.md:52`.
Citing artifact (`used-by`): `corpus/knowledge/idle-lock-route-r17.md`.

Installs: **none**. No pacman/sudo/systemctl/hyprctl/live probe was run. Network reads were
`curl` (raw.githubusercontent, codeload, github.com HTML/redirect) and one read-only
`git ls-remote`; no git mutation, no commit, no jj.

## Axes

1. Byte fidelity — is the recorded digest the digest of the bytes actually served at the
   stated ref, reproducible by a second channel?
2. Anchor precision — does the quoted text sit at the stated line, verbatim, within the
   round's ≤25-word cap?
3. Registry conformance — tier/status/scope/anchor/teaches/recheck/used-by against
   `CORPUS.md` (contract v1, lines 86–118) and the maintained census validator.
4. Citation chain — every claim the citing note draws from S065 at the anchors it gives
   (no over-read, no wrong line).
5. Gate conformance — one gate row per new row, URL, access date, quote, digest, agreement
   between gate and registry.

## Verdict

**The attack failed on substance.** The row is a true claim: the URL resolves at the tag,
the quoted sentence is verbatim at line 6, the digest reproduces byte-for-byte from three
independent channels, tier A / mined / used-by are correct, and all five `[HR:n]` anchors
the note uses are exact. No false statement was found in the row, the gate line, or the
note's S065-grounded claims.

Four precision defects survive — none changes a claim's truth, none breaches the ≤25-word
cap, none is unique to S065. Listed under *Counterexamples and defects* with anchors.

## Evidence

### 1. Bytes and digest (axis 1, 5)

| channel | command | result |
|---|---|---|
| raw at ref | `curl -fsSL https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md` | `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6`, **2598 bytes**, 76 lines, trailing newline present |
| raw, second fetch (piped) | same URL → `sha256sum` | `f5b852ee…9781f6` (deterministic) |
| tag tarball | `curl -fsSL https://codeload.github.com/hyprwm/hypridle/tar.gz/refs/tags/v0.1.8` → `hypridle-0.1.8/README.md` | same digest; `cmp` against the raw fetch → **byte-identical** |
| commit-pinned raw | `…/hypridle/e5c01af0842bd66617f7004568df9406111d6e80/README.md` | same digest; `cmp` → **byte-identical** |
| tag identity | `git ls-remote … refs/tags/v0.1.8*` | one line, `e5c01af0842bd66617f7004568df9406111d6e80` → lightweight tag, i.e. tag ref **is** that commit |
| in-tree version marker | `VERSION` in the tag tarball | `0.1.8` — the tree self-identifies with the tag name |

Recorded digest in both registry and gate is 64 lowercase hex characters, equal in both
files (checked programmatically), and appears nowhere else in `corpus/SOURCES.md` (no
duplicate digest among S001–S070). The digest therefore pins the *tag's* bytes, not merely
today's `main`: `main`'s README happens to hash identically today, which neither weakens
nor strengthens the pin but does mean the bytes were not drifted between tag and head.

Latest-release premise (note line 27–29: "`releases/latest` redirects resolved to `v0.1.8`
… on 2026-10-20"): re-tested —
`https://github.com/hyprwm/hypridle/releases/latest` → `302 → /releases/tag/v0.1.8`;
`codeload …/refs/tags/v0.1.9`, `v0.1.10`, `v0.2.0` → `404`;
`https://github.com/hyprwm/hypridle/tags` lists `v0.1.0 … v0.1.8`. Claim holds.
The note's companion sentence "The GitHub REST API returned HTTP 403 rate-limit and was not
used" is corroborated in this session: `https://api.github.com/repos/hyprwm/hypridle/git/ref/tags/v0.1.8`
returned `403` and no body, so the tag had to be resolved by `ls-remote`/codeload instead.

### 2. Anchor and quote (axis 2, 5)

Raw line 6, byte-exact (`repr`, so the bullet prefix is visible):

```
" - support for dbus' loginctl commands (lock / unlock / before-sleep)"
```

Gate quote at `lessons/round-17.md:52`: `support for dbus' loginctl commands (lock / unlock / before-sleep)`.
`quote in line6` → `True`. The quote is a contiguous substring of the stated line; only the
leading Markdown bullet `" - "` is omitted, which is the same convention the sibling gate
rows use (S060 quotes mid-line after `"# i.e. "`). Word count: **10** whitespace tokens
(**8** if the two standalone `/` tokens are excluded) versus the row's stated **9** — see
defect D1. Either way the gate preamble's cap (`quote ≤25 words`) is met.

### 3. Registry row (axis 3)

`corpus/SOURCES.md:77`, verbatim as landed at HEAD (verified `git show HEAD:corpus/SOURCES.md`
byte-identical to the working copy):

| field | value | check |
|---|---|---|
| kind | `docs` | allowed enum (`spec·docs·paper·code·tool·dataset·talk·book·community·own-work`) |
| tier | `A` | upstream repo README at a tag = official docs, primary for this scope (`CORPUS.md:93-95`) |
| scope | features, config example, usage, flags at tag v0.1.8 | all four sections exist in the file: `## Features` :4, `## Configuration` :9, `### Usage` :57, `## Flags` :69 — but see D2 |
| anchor | `file lines 5-33, 62` | lines 5–6 = features bullets, 9–31 = config example, 33 = listener note, 62 = `exec-once = hypridle` |
| teaches | ext-idle-notify-v1 basis; dbus lock/unlock/before-sleep scope; exec-once usage | :5, :6, :62 respectively — all three inside the anchor |
| status | `mined` | used-by names the note; note's `source:` line names S065 (§"source:" line 1, third entry) |
| opened | `2026-10-20` | matches gate preamble "New rows (all opened 2026-10-20)" |
| recheck | `on-change` | passes validator E09; outside the contract's enumerated prose — D3 |
| used-by | `corpus/knowledge/idle-lock-route-r17.md` | file exists; cites S065 (E11 clean) |

Row uniqueness: `^| S065 |` appears once in `SOURCES.md` and once in `lessons/round-17.md`.
Gate table holds 15 rows (S056–S070) with no duplicated id. Every digest for S063–S069 is
equal between registry and gate (checked pairwise) — so the note's `verified-at` claim
"raw SHA-256 per source in corpus/SOURCES.md S063-S069 and lessons/round-17.md § Gate" is
structurally true.

Maintained validator, read-only: `scripts/sources-census.sh validate --root …/shokunin mado`
→ only `W04` warnings on S030/S042/S045 (unrelated duplicate URLs) and final
`mado ok …/corpus/SOURCES.md`. No E01–E12 finding names S065. Note the validator's E09
accepts any `^[A-Za-z][A-Za-z0-9 _-]*$` as a "symbolic cadence"
(`scripts/sources-census.sh:582,665`), so the tool cannot catch D3.

### 4. Citing-note claim chain (axis 4)

Every `[HR:n]` occurrence in `corpus/knowledge/idle-lock-route-r17.md`, checked against the
fetched bytes (note :21 defines `[HR:n]` = file line):

| note line | note claim | fetched line | holds? |
|---|---|---|---|
| :35 | README example: "dbus/sysd lock command (loginctl lock-session)" `[HR:16]` | :16 `    lock_cmd = notify-send "lock!"          # dbus/sysd lock command (loginctl lock-session)` | yes — verbatim substring, including the source's own `dbus/sysd` typo |
| :39 | README: "whether to ignore dbus-sent idle-inhibit requests (used by e.g. firefox or steam)" `[HR:20]` | :20 `    ignore_dbus_inhibit = false             # whether to ignore dbus-sent idle-inhibit requests (used by e.g. firefox or steam)` | yes — verbatim |
| :49 | `condition_cmd` / `condition_retry` documented, README `[HR:28-29]`, "not exercised here" | :28 `condition_cmd =  # if set, run this command before on-timeout. Exit 0 = proceed, non-zero = defer`; :29 `condition_retry = 0  # retry interval in seconds when condition_cmd defers (default: 0, no retry)` | yes — keys, semantics and default all on those lines; the note claims documentation only |
| :51 | README: `exec-once = hypridle` `[HR:62]` | :62 `exec-once = hypridle` | yes |
| :61 | hypridle README: "based on the `ext-idle-notify-v1` wayland protocol" `[HR:5]` | :5 `` - based on the `ext-idle-notify-v1` wayland protocol `` | yes — verbatim minus bullet prefix |

Also checked: the note's `source:` line attributes S065 "(Features, Configuration)", and
those headings exist at :4/:9; the note's recheck field says "the five tag-pinned raw URLs"
— S065–S069 is exactly five. No S065-grounded claim is missing an anchor, and nothing the
README says is upgraded into observed behaviour (the note's `surface: P6` block and
§Unexercised behavior keep it documentary).

Adjacent claim worth recording (repo tree, not the README): note :118 and :132 say
`example/hypridle.conf` / `example/hyprlock.conf` return 404 at both tags and there is no
`example/` directory. Verified true: both raw URLs return `404`; the v0.1.8 tarball root has
no `example/`; the v0.9.6 hyprlock tarball root likewise. **However** hypridle v0.1.8 ships
`assets/example.conf` (sha256 `ef385d88e8c99820ed910eadd62cd14c16bc948317d4f78e93453e24c70d13d1`,
installed by `CMakeLists.txt:103`), which the note never mentions. That is a coverage gap,
not a false statement: the note's claim is scoped to the `example/` paths it names.

## Counterexamples and defects

No counterexample to any truth-bearing claim. Four precision defects, exact anchors given.

**D1 — gate word count is off by one (trivial).**
`lessons/round-17.md:52` says `(9 words)`; the quoted string is 10 whitespace tokens
(8 if standalone `/` tokens are not counted). Cap ≤25 unaffected. This is a family defect,
not an S065 anomaly — same audit against all 12 counted gate rows, stated/actual: S056 12/11, S057 4/4,
S058 16/16, S059 10/10, S060 3/5, S061 10/10, S062 7/9, S063 11/9, S064 24/24, S065 9/10,
S068 5/5, S069 5/4. Six of twelve disagree with a plain whitespace count, so the column is
decorative rather than checked; no row exceeds 25.

**D2 — `scope` advertises evidence the `anchor` does not cover (minor).**
`SOURCES.md:77` scope says "…usage, flags at tag v0.1.8", anchor says "file lines 5-33, 62".
`## Flags` is lines 69–76 (with `-c/--config` default at 72–73) and has no line in the
anchor; `### Usage` (57–67) is anchored only at :62, the one usage line the note cites. The
`teaches` cell is fully anchored (5/6/62), so this is a scope/anchor coupling inconsistency,
not an unsupported claim — no note claim depends on 57–61, 63–76 or the flags. A one-token
fix would either drop "flags" from scope or extend the anchor to `5-33, 57-67, 69-76`.

**D3 — `recheck = on-change` is outside the contract's enumerated cadence (minor, systemic).**
`CORPUS.md:105-106` reads "`recheck` — ISO date or cadence (`90d`, `180d`, `on-release`)";
`on-change` is not in that list. It is nonetheless accepted by the maintained validator
(`sources-census.sh:582` symbolic regex, `:665` E09) and by policy: symbolic cadences are
"reported, never judged overdue" (`:34-36`, `:676-682`), so S065 can never fall due. The
value is also pre-existing practice in this registry (S003, S004, S013, S015, S020 all
`on-change` before this round), and for immutable tag bytes "on change" is arguably more
literal than "on release". The real inconsistency is *within round 17*: tag-pinned
S056/S057/S058 use `on-release` while tag-pinned S065/S066/S067/S068/S069 use `on-change`.
Either value is defensible; two values for one source class is not. Recorded, not fixed
(append-only contract; a `recheck` change needs an old→new lesson entry).

**D4 — anchor range clips a sentence (trivial).**
`file lines 5-33` ends mid-sentence: :33 "…Omitting `on-timeout` or `on-resume` (or leaving
them empty)" and :34 "will make those events ignored." A range is a locator, not a quote, so
nothing breaks; `5-34` would be tidier.

## Why the strong attacks fail (for the record)

- *Digest could be of `main`, not the tag* → refuted: codeload tag tarball and raw-at-commit
  `e5c01af…` both produce the same digest; the tree's `VERSION` is `0.1.8`.
- *The quote could be a paraphrase or a spliced line* → refuted: exact substring test on the
  fetched bytes, and the two `/` separators are preserved.
- *The note could have over-read documentation into behaviour* (e.g. claiming the listener
  fires, or that `condition_cmd` was observed) → refuted: note :49 says "Not exercised
  here"; the entry is gated as `surface: P6` documentary with `[UNK]` lines for firing,
  timing and lock success.
- *Wrong line numbers could hide a shifted file* → refuted: all five `[HR:n]` lines match
  their quoted content, and the whole file is 76 lines with a trailing newline (no CRLF, no
  truncation).
- *A stale premise ("latest = v0.1.8") could have expired* → refuted today: redirect still
  302 → `v0.1.8`, newer tags 404. On the next hypridle release this specific sentence goes
  stale, which is exactly what `on-change`/`on-release` is meant to catch; today it holds.
- *The C2 "sources_ok" could be read as content verification of S065* → not so, and worth
  stating plainly: `measure.py:116-120` (`mined_a`) and `:243-246` (surface keyword match)
  are string joins over registry cells and the note path. S065's appearance at
  `.ufo/waves/round-17/evidence/measure-c1.json` `c2/provinces/P6/entries[0]/sources_ok[2]`
  asserts tier/status/used-by co-reference, **not** that quote, digest or anchor were
  checked. Content verification of this row is this report, not the measurement.

## Residual unknowns

- `[UNK]` Whether hypridle ever moves the `v0.1.8` tag (a retag would break the digest pin
  silently; no watcher exists and `on-change` is never "overdue").
- `[UNK]` Whether the wiki page (S063, "Latest git") still matches these tag bytes for keys
  the note cites from both — not S065's question; S063's lane.
- `[UNK]` Whether `assets/example.conf` is the wiki's "which can be found here" target
  (note :132 leaves it open); the file exists in the tag tree and CMake installs it, but
  proving the wiki's link resolves there needs the wiki's rendered href, not these bytes.
