# ReopenS061 — re-open S061 (Arch Wiki Alacritty, rejected)

Seat: `MadoR17.ReopenS061` (scout, leaf). Date: 2026-10-20.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Target: lane HEAD `988b858bd6049bc709807534fd725c05264f7e60` (confirmed by
`git rev-parse HEAD`). Item: re-open
`https://wiki.archlinux.org/title/Alacritty` (row S061, rejected; quote
line 24), fetch raw bytes with `curl`, compute SHA-256, and verify the
registry row, its gate line and the stated rejection reason.

**Verdict: ATTACK FAILED.** No falsifying counterexample was found. The
pinned revision, its digest, both anchors and the verbatim quote reproduce;
all three stated rejection reasons hold against the bytes. Four formal
nits below change no verdict (the row admits nothing and `used-by` stays
`—`). Report only; no lane file edited, no commit, no `jj`, no install.

Axes attacked: (A1) revision identity/digest, (A2) anchor+quote fidelity,
(A3) rejection-reason soundness, (A4) registry/gate conformance,
(A5) `used-by` integrity, (A6) re-fetchability.

## Receipts (raw bytes, fetched 2026-10-20)

| # | URL | HTTP | bytes | sha256 |
|---|---|---|---|---|
| R1 | `https://wiki.archlinux.org/index.php?title=Alacritty&action=raw` | 200 | 8275 | `c39c563d74f2ff7c35bd7133a438804f6314c10434e3f94ad289b7c28c4600bb` |
| R2 | `https://wiki.archlinux.org/api.php?action=query&prop=revisions&revids=869789&rvslots=main&rvprop=content%7Csize%7Csha1&format=json&formatversion=2` | 200 | content 8275 | content sha256 same as R1; API `sha1` `dd6fbce2cc1b931fdcbaa0b8654d7a82e1239bea` |
| R3 | `https://wiki.archlinux.org/api.php?action=query&prop=revisions&titles=Alacritty&rvprop=ids%7Ctimestamp%7Csize%7Csha1` | 200 | — | current `revid` **869789**, `2026-03-23T05:20:49Z`, size 8275 |
| R4 | `https://raw.githubusercontent.com/alacritty/alacritty/v0.16.0/alacritty/src/config/mod.rs` | 200 | 13487 | `9e1c5fa7815fb6d238141d4bb3861c99842d499b32e65aee4cc08aaebd32373a` |
| R5 | `.../v0.16.1/alacritty/src/config/mod.rs` | 200 | 13487 | same as R4 |
| R6 | `.../v0.17.0/alacritty/src/config/mod.rs` | 200 | 13499 | `ca29ee6de3cd53474a23b2c21282811748b728be5d4faec9edd5bbd8cc811168` |
| R7 | `.../v0.14.0/alacritty/src/config/mod.rs` | 200 | 13548 | `b32a3843f71054dce1f7009ca64fc7baa284d1f99e7d254bad987dec8290ee81` |
| R8 | `.../v0.15.0/alacritty/src/config/mod.rs` | 200 | 13548 | same as R7 (identical bytes) |
| R9 | `.../v0.14.0/extra/man/alacritty.5.scd`, `.../v0.15.0/extra/man/alacritty.5.scd` | 200 | 28218 / 28405 | `4ac66c2f…1dfe63` / `6b3cf962…21908d` |

## Findings

### A1 — revision identity and digest: HOLDS

`revid 869789`, `2026-03-23T05:20:49Z`, author Cyqsimon, summary
`/* Configuration */ Add system-wide configuration location`, size 8275,
API `sha1 dd6fbce2…`. The row's `c39c563d…4600bb` is the prefix8+suffix6 of
the full digest above, reproduced twice: the live `action=raw` body (R1) and
the API content of `revids=869789` (R2) hash byte-identically. The revision
is also the page's **current** revision (R3), so the digest is stable today,
not merely an oldid artifact.

### A2 — anchors and quote: HOLD

Raw wikitext, 1-based, exactly the row's convention:
`:22` = `* {{ic|/etc/alacritty/alacritty.toml}}` — the stated path is present.
`:24` = `Versions before 0.13.0 used a YAML configuration file. …` —
`line24.startswith(quote)` is True for the gate's exact string, including the
terminal period.
Word count: 8 whitespace tokens; **10** alphanumeric-run tokens
(`0.13.0` → `0`,`13`,`0`) — the stated "(10 words)" is reproducible under
that tokenizer; either way ≤25.

### A3 — rejection reasons: HOLD

1. *"community tier cannot support a C2-covered entry"* — the round's C2 rule
   (`SCORECARD.md:842-849`) admits coverage only from a **mined tier-A**
   `SOURCES` row whose `used-by` names the entry; the contract's tier C is
   "lead only — never sole support for an admitted entry"
   (`SOURCES-CONTRACT-v1.md` § Shape). A tier-C rejected row cannot count.
2. *"the `/etc` line duplicates upstream ≥0.16.0 (tagged `config/mod.rs:371,395`; absent `v0.14.0`/`v0.15.0`)"* —
   verified at both ends. `v0.16.0`/`v0.16.1`: line 371
   `/// 5. /etc/alacritty/alacritty.toml`, line 395
   `let fallback = PathBuf::from("/etc/alacritty").join(&file_name);`; `v0.17.0`
   the same two lines. `v0.14.0`/`v0.15.0`: byte-identical file, **0**
   `/etc/alacritty` matches, and the doc comment lists only paths 1-4
   (`:370-373`). The man pages at those tags also contain no `/etc` (R9).
   Ordering also duplicates upstream (path 5 last).
3. *"the edit that added it cites no source"* — the diff `869788 → 869789`
   adds exactly the one bullet; the revision summary names no source or URL.

### A4 — registry and gate conformance: HOLDS

`S061` is one 13-field row (11 columns, no malformed rows;
`sources-census.sh validate … mado` prints `ok`, exit 0 — its three `W04`
lines are pre-existing duplicate-URL findings for S030/S042/S045, not S061).
`kind=docs` and `status=rejected` are contract enum values; the row's
`teaches` matches the contract's rejected shape
`REJECTED: <reason>; flip: <what would change the verdict>`.

At HEAD, the registry histograms are rows **70**, tiers A63/B1/C6, statuses
mined55/queued8/rejected7 — exactly the lessons' after-values
(`55 → 70`, `A 51 → 63`, `C 3 → 6`, `mined 43 → 55`, `rejected 4 → 7`).
The gate line is `lessons/round-17.md:48` and carries URL, `line 24`, the
verbatim quote, the digest and `(rejected)`; the access date is carried by
the table header `all opened 2026-10-20`.

### A5 — `used-by` integrity: HOLDS

`used-by` is `—`. `grep -rn S061 corpus/knowledge/*.md` finds one hit,
`terminal-route-r17.md:131`, which names S061 only as **rejected**; the P4
note's `source:` line (lines 1-5) cites S056-S060 (S071 in the uncommitted
working tree), never S061. No admitted entry is supported by this row.

### A6 — re-fetchability: HOLDS, one environment caveat

`action=raw` (no oldid) returns 200/8275/full digest today. `action=raw&oldid=869789`
is currently served the wiki's **Anubis** challenge page (7,469-7,496 B,
`<title>Making sure you're not a bot!</title>`), with or without a browser
UA. Oldid content is still retrievable via `api.php?revids=869789`, which is
the route used here. The row's "flip: oldid-pinned" remains executable, just
not through `action=raw` while the bot check is on.

## Nit list (none changes the verdict)

1. **Gate digest is abbreviated.** The gate cell and the registry cell give
   `c39c563d…4600bb` (14 hex chars), while the gate column header says
   "raw SHA-256" and S056-S060 carry full 64-hex values. The value is
   correct; the representation is short. Full value:
   `c39c563d74f2ff7c35bd7133a438804f6314c10434e3f94ad289b7c28c4600bb`.
2. **Gate quote grounds the anchor, not the `teaches` text.** Contract
   Rule 1 asks for a quote "grounding `teaches`"; for this rejected row the
   quote grounds the anchor's `:24` before-0.13 boundary, not the three
   rejection reasons. The reasons themselves are evidenced in
   `w1/reports/SrcTerminalAlternates.md` § A1 and re-verified above. Impact
   on admission: none (rejected row, no claim).
3. **"10 words" is tokenizer-dependent** (8 whitespace / 10 alnum-run).
4. **"no version pin" is literalist-adjacent**: the page does contain one
   version-shaped sentence (the 0.13.0 boundary). The row's own anchor names
   it as a historical boundary, so the scope is accurate as written, but a
   reader taking "no version" literally would over-read.

## Cross-check on "opened, not snippet"

The row is genuinely opened: `w1/reports/SrcTerminalAlternates.md` R1 records
200/8275/full digest and lines 51-53 record the revid/timestamp/summary via
the wiki API; both reproduce here. The wave-1 `SourcesUsedByJoin.md` D2 note
("S061/S062 were not opened") referred to the *draft* ids
`S061-pending`/`S062-pending` (Ubuntu manpage, GitHub master blob) in
`drafts/NoteTerminal-rows.md:17-18`; the lessons record those drafts being
replaced before landing by opened rejections. The landed S061 is the opened
Arch-wiki row verified here.

## Repo-state observation (not mine to change)

The working tree currently carries uncommitted edits by another writer:
a new `S071` row (`corpus/SOURCES.md`), `corpus/README.md`,
`corpus/knowledge/terminal-route-r17.md` and the `M2` lesson row. S061's
registry row is byte-identical at HEAD and in the working tree
(sha256 `fd31dea35d2af7d907e444399f751abed985bc40d23ca71b5faaef4657df4025`),
and gate line 48 is unchanged; all arithmetic above is at HEAD.

## Commands used (all read-only, hermetic)

```
curl -sS  'https://wiki.archlinux.org/index.php?title=Alacritty&action=raw'
curl -sSL 'https://wiki.archlinux.org/api.php?action=query&prop=revisions&revids=869789&rvslots=main&rvprop=content|size|sha1&format=json&formatversion=2'
curl -sSL 'https://wiki.archlinux.org/api.php?action=query&prop=revisions&titles=Alacritty&rvprop=ids|timestamp|size|sha1&format=json&formatversion=2'
curl -sSL 'https://raw.githubusercontent.com/alacritty/alacritty/<tag>/alacritty/src/config/mod.rs'   # v0.14.0 v0.15.0 v0.16.0 v0.16.1 v0.17.0
curl -sSL 'https://raw.githubusercontent.com/alacritty/alacritty/<tag>/extra/man/alacritty.5.scd'     # v0.14.0 v0.15.0
sha256sum, awk line numbering, diff of revisions 869788→869789
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
git rev-parse/show/log/diff (read verbs only)
```

Installs this round: **none**. No `pacman`/`yay`/`paru` (not even queries),
no `sudo`, `systemctl`, `hyprctl`, `libinput`, terminal/compositor launch or
live probe; no transcript, no `~/.omp/agent/agent.db*`. Web sources were
fetched by `curl` only (raw bytes, sha256).
