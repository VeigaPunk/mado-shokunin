# AtkLessonGate — partial

Attack on `corpus/lessons/round-19.md` § Gate at `01b80946d92b26370d3012a7da655d00dd135154`
(`corpus/lessons/round-19.md:39-50`): the three new rows' URL / access date / located
quote / digest columns, and the S084/S094 old→new lines against the actual diff.

Result: the substance of all three admissions reproduces — every URL is the row's,
every date is 2026-10-20, every digest is the digest of the anchored artifact
(binary, raw body, crate), and the S084/S094 ledger is exactly equal to the diff.
Two cell-level defects survive: **S096's quote does not begin at its stated byte**
(a literal read fails; the digits do, and the printed 13-byte run begins 7 bytes
earlier — this is the lane's own precedent shorthand, but the qualifier was dropped),
and **S098's word count is wrong** (5, stated 6). Both are transcription-level, not
invented anchors: the wave-1 drafts had them right
(`drafts/HostWalkerBytes-row.md:16-17`, `drafts/SourcesFrontierDraft.md:25,33`), the
lesson dropped/fixed the wrong part. S096's offsets are independently corroborated
by peer `MadoR19.ReopenS096`, who reached the same reading via the cached 2.17.0
package.

## S096 — host walker bytes: digest/URL/date hold, located quote is off by 7 bytes

Lesson line (`corpus/lessons/round-19.md:41`):

```
- GATE | S096 | host `/usr/bin/walker` (+ `/var/lib/pacman/local/walker-2.17.2-1/desc`, `/var/log/pacman.log`) | 2026-10-20 | `/usr/bin/walker` byte 856,302: "version2.17.2" (1 word) | 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096 | admit: one `2.17.2` literal, zero `2.17.0` …
```

Independent read (python, file bytes only; no `walker`, no pacman):

```
bytes 7039912
sha256 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
count 2.17.2 1
count 2.17.0 0
find(b'2.17.2') 856302
bytes at 856302: b'2.17.2\ntoggle exact search%RESUME_LAST'
find(b'version2.17.2') 856295
b[856295:856308] == b'version2.17.2'
```

- URL/source column: matches the row's source cell (`corpus/SOURCES.md:108` lists the
  same three host paths). Access date cell `2026-10-20` (`SOURCES.md:108` col 9) = the
  lesson's date. Digest: `2524…3096` is the binary's sha256, equals the row's first
  digest and equals the `mtree` record (`/var/lib/pacman/local/walker-2.17.2-1/mtree`,
  gzip sha256 `d5dfb3f1…9aa4`, line 30 `./usr/bin/walker … size=7039912
  sha256digest=25240650…3096`; `desc` sha256 `5c0d9d89…0928`, `%VERSION% 2.17.2-1`).
  `/var/log/pacman.log` 244,858 B sha256 `27bbd0b5…6ffc`; line 2929 verbatim:
  `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`.
  Epoch cells agree: 1791468872 = 2026-10-08T14:14:32Z = binary mtime; 1792498606 =
  2026-10-20T12:16:46Z = the log line's local time. BuildID `19200fe4…9e99` matches
  `readelf -n`. `.rodata` bounds `off 0x0b6900 size 0x074654` match `readelf -SW`
  and contain 856,302.
- **Defect (locational):** the quoted run does not start at 856,302. At 856,302 the
  bytes are `2.17.2\n`; `version2.17.2` spans 856,295-856,307. The lesson's quote is
  also not the row's anchored literal: the row anchors `2.17.2\n` at 856,302
  (`SOURCES.md:108`), the lesson prints `version2.17.2` at 856,302. The draft states
  the disambiguation the lesson dropped: "the literal is the 7 bytes `2.17.2\n`
  (digits at 856,302, LF at 856,308)" (`drafts/HostWalkerBytes-row.md:16-17`).
  A literal "quote at stated byte" read fails; "the digits at 856,302" is true.
- **Precedent (peer-corroborated):** the lane locates a version literal by its first
  digit, not by the adjacent `version` token. Round 9 did exactly this:
  `walker-deep-r9.md:109` calls 847,791 the run offset while listing
  `…version` + `2.17.0` + LF, and `:316` records the command that produced it,
  `b.find(b'2.17.0')`. Verified against the cached 2.17.0 package
  (`tar --zstd -x … /var/cache/pacman/pkg/walker-2.17.0-1-x86_64.pkg.tar.zst`):
  binary 6,661,264 B sha256 `64826a8531eac525adfa3eff65548e93a6f7714feb1d3e13b4fa35bbcc3cfda0`
  (the lane's pinned 2.17.0 digest, `walker-deep-r9.md:57`), `find(b'2.17.0') =
  847791`, `find(b'version2.17.0') = 847784`. So S096's Gate cell is
  precedent-consistent shorthand; what it dropped is the qualifier that made round 9
  honest (`walker-deep-r9.md:112-116`: "`2.17.0\n` literal carries the newline… the
  `version` token immediately before it is a separate rodata run"), and which the w1
  draft retained. Peer `MadoR19.ReopenS096` independently confirms both offsets and
  reaches the same reading (`.ufo/waves/round-19/w2/reports/ReopenS096.md`).
- All other S096 clauses hold: 1 literal / 0 `2.17.0`; `find → 856302`;
  `--version` not run (no process fact claimed).

## S097 — omarchy colors.toml: all four columns hold (checked beyond the ask)

Lesson line (`corpus/lessons/round-19.md:42`), quote at
`.ufo/waves/round-19/fetch/SrcS094/colors.toml:4`.

- Committed body at the tip: 461 B, sha256
  `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`; line 4 is
  exactly `background = "#121212"` (3 whitespace tokens, stated 3). Committed bytes
  = worktree bytes; `git show <tip>:…/colors.toml | sha256sum` = same digest.
- URL: lesson string is byte-identical to the row's URL (`SOURCES.md:109`); receipt
  `fetch/SrcS094/receipts.jsonl` records that exact URL, `http_status:200`,
  `bytes:461`, `fetched_at 2026-10-20T17:06:08Z`, same sha256. Access date 2026-10-20
  matches the row's opened cell.
- Digest is the anchor's: fresh `curl` 200 / 461 B / `dbdd13a6…1786`; `git hash-object`
  of the fetched body = `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231`, the row's git blob
  id for colors.toml (461 B) at the tag.
- Secondary "admit" clause: tag `v3.8.4` is lightweight — GitHub API
  `git/refs/tags/v3.8.4` returns `object.type: "commit"`,
  `sha 8fcc9d6048af4cb0e3af8512c78049857a3b53dd` (basecamp→omacom 301 followed);
  tree `3fc08f954e5a3f67072a79a7c52d94e0a153b9ec` returns 200 with the row's blobs
  (colors.toml `5e1a8cca…` 461; btop.theme `c8cdcd02…` 2648; backgrounds tree
  `ff02c341…`). "tree ids from a /tmp clone" is consistent with the API objects.

## S098 — xdg crate: digest/URL/date hold; word count is 5, stated 6

Lesson line (`corpus/lessons/round-19.md:43`), quote at
`xdg-3.0.0/src/base_directories.rs:447-448`.

Fresh `curl` of the row URL: 200 / 15,821 B / sha256
`2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`; extract member
`xdg-3.0.0/src/base_directories.rs` (tar member 12/39):

```
447     /// configuration file, or `None`. Searches `XDG_CONFIG_HOME` and then
448     /// `XDG_CONFIG_DIRS`.
```

- URL matches the row (`SOURCES.md:110`); access date 2026-10-20; digest is the
  anchor's: it is the crate body's sha256 and equals the lock line the row cites —
  `walker v2.17.2 Cargo.lock:2705-2708` (`name = "xdg"`, `version = "3.0.0"`,
  `checksum = "2fb43323…85b5"`), committed copy digest `3448367c…2315` (receipt,
  fresh refetch, and `git show <tip>:…` all equal); walker tag `v2.17.2` resolves
  lightweight to `a515085fd39fae80acc086c8fbfd9b7771a9a11d` (API, type commit).
- **Defect (count):** "Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`." has
  **5** whitespace tokens (`Searches`, `` `XDG_CONFIG_HOME` ``, `and`, `then`,
  `` `XDG_CONFIG_DIRS`. ``), not 6; ≤25 either way. The wave-1 draft says 5
  (`drafts/SourcesFrontierDraft.md:25` and its GATE slot at `:33`); the lesson's 6 is
  an L1 transcription error.
- Quote fidelity: the sentence is not a contiguous byte run — the member carries
  `    /// ` prefixes and a newline between `then` and `` `XDG_CONFIG_DIRS`. ``;
  contiguous count of the printed sentence = 0. Stripping the doc-comment prefix and
  joining 447→448 reproduces it word-for-word. Joined-line quotes are established
  (`round-18.md` S076 `:156-161`, S092 `:29-30`, both whitespace-normalized), so this
  is not a break; it is the first Gate quote that strips `///` markup, which the line
  range discloses. [INFERENCE] a verifier requiring raw bytes at 447-448 would fail;
  one allowing markup-stripped joins would pass.
- "crate body kept digest-only": true — no `*.crate` at the tip
  (`git ls-tree -r <tip> .ufo/waves/round-19/fetch`), and `fetch/.gitignore` ignores
  the crate paths; precedent S079 quotes a member of a gitignored tarball.

## Old→new lines for S084/S094 — complete and numerically exact

`git diff 9c54c56 01b80946 -- corpus/SOURCES.md`: 26 insertions, 2 deletions. Parsed
all `| S### |` rows at both revs and diffed cell by cell; only two cells changed per
row, matching the lesson's lines exactly (`corpus/lessons/round-19.md:45-50`):

```
===== S084  cell[7] mined -> rejected ; cell[10] corpus/knowledge/walker-route-r18.md -> —
===== S094  cell[7] mined -> rejected ; cell[10] corpus/knowledge/theme-route-r18.md -> —
```

Character-level diff of the two rows confirms nothing else moved (S084: `'min' ->
'reject'` inside mined→rejected, used-by → `—`; S094: `mined … | corpus/knowledge/theme-route-r18.md |`
→ `rejected … | — |`). Recheck cells (`… on-release`) unchanged. Counts reproduce:
rows 95→98, tier A 88→91, mined 80→81, rejected 7→9 (3 new tier-A mined rows, 2
mined→rejected). The other 24 insertions in the diff are the provenance paragraph and
the round-19 search-log paragraph, outside this ledger's scope.

## Why this is `partial`, not `breaks`

Every admitted fact — walker is 2.17.2 on this host by binary/desc/mtree/log bytes;
the matte-black colors.toml at tag v3.8.4 is the row's 461 B body; the crate at
static.crates.io is exactly the xdg release the tag's lock checksums — reproduces
independently. No anchor is invented or mismatched, and no digest is a per-fetch
body. The defects are cell wording/counting, not anchor content: S096's located
quote prints `version2.17.2` with a 7-byte-earlier start than its stated byte
(precedent-consistent shorthand — the lane has always located a version literal by
its first digit — but the qualifier that made round 9's version of this honest was
dropped, so a literal "quote at the stated byte" read fails), and S098's quote has
**5** words, not 6. No runnable lane check reads these columns (no `GATE`-row
verifier among `.ufo/waves/round-19/*.py` / `round-18/*.py`), so neither defect
touches C1-C3 counters; the anchors, dates and the old→new ledger are sound.

## Limits

- Host bytes read as files with python/readelf/gzip only; `walker`, `pacman`, `git
  ls-remote` and jj were not run; no gate or copy of it. The 2.17.0 precedent check
  read `/var/cache/pacman/pkg/walker-2.17.0-1-x86_64.pkg.tar.zst` as a file and
  unpacked one member with `tar --zstd` to /tmp — no package query or transaction.
- Worktree is not byte-equal to the tip under `.ufo/waves/round-19/fetch/`: peer
  wave-2 edits are present (`.gitignore` modified, `RETENTION.json`,
  `RevRubricVRisk/` untracked). For the quoted S097/S098 bodies I read committed
  bytes; the committed colors.toml and receipts equal the worktree files.
- API bodies are used for tag/tree identity only (git object ids from GitHub), not as
  content anchors; their digests are recorded below but not treated as anchors.
- Word counts use the lane's whitespace-token convention demonstrated by round-18
  rows (S092 "13", S083 "5").
- [SKIPPED] Verifying the S097 row's host-equality clause (12 host payload files vs
  tag blobs) and the "19 payload dirs" clause — outside the § Gate column question.

## Installs

none.

## Fetch receipts (/tmp/atk19, curl only, no auth)

| url | status | bytes | sha256 | fetched_at |
|---|---|---|---|---|
| https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | 200 | 461 | dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786 | 2026-10-20T18:03:29Z |
| https://static.crates.io/crates/xdg/xdg-3.0.0.crate | 200 | 15821 | 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5 | 2026-10-20T18:03:29Z |
| https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.lock | 200 | 70247 | 3448367c28c769e29f681ea2de84d4a822f08569bbef6628f03535c61fec2315 | 2026-10-20T18:03:29Z |
| https://api.github.com/repos/basecamp/omarchy/git/refs/tags/v3.8.4 (301 → repositories/994093166) | 200 | 368 | a503d17da45fecbe7a5293c41d29a8b88fa0bf0f4b22293ca16f415f7ac9efd9 | 2026-10-20T18:05:26Z |
| https://api.github.com/repos/basecamp/omarchy/git/trees/3fc08f954e5a3f67072a79a7c52d94e0a153b9ec | 200 | 2656 | 5772bc7c56cb1732657f75e72fec3670c78d60acf4e3384cbd6eab47267f21cf | 2026-10-20T18:05:26Z |
| https://api.github.com/repos/abenz1267/walker/git/refs/tags/v2.17.2 | 200 | 376 | 14147b773ad295a74e999ed36aded0403e868a4551c20a6d84cd2b4079a547de | 2026-10-20T18:07:38Z |
