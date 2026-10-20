# MadoR19.AtkPtrThemeRouteR18 — holds

Attacked `corpus/knowledge/theme-route-r18.md` at tip `01b80946d92b26370d3012a7da655d00dd135154`
(worktree sha256 `abc5bef0b0e3f9f0742f3acb6df9689291de9489835c4c892de44fb4948cf17e` equals the
committed blob's). The round-19 block is `:165` heading + `:167` and `:168` bullets; the only
in-place edit is the head `source:` token at `:1`. I tried to falsify each assigned question
(byte scope, live/runtime walker claim, line citations, S-row support) and could not: every
numeric/identity claim reproduces from independent fetches, and the one non-upstream
(host-state) sentence re-measures true. Two documentation gaps (G1/G2) and two convention
notes (G3/G4) remain below, but no sentence is false.

## (a) Pre-existing bytes beyond the documented head token swap — no

```
$ git diff 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d 01b80946d92b26370d3012a7da655d00dd135154 \
      -- corpus/knowledge/theme-route-r18.md
 corpus/knowledge/theme-route-r18.md | 7 ++++++-
 1 file changed, 6 insertions(+), 1 deletion(-)
@@ -1,4 +1,4 @@   (line 1 only)
@@ -161,3 +161,8 @@  (append block)
```

Byte-level check of the head line (`difflib.SequenceMatcher`, no autojunk):

```
line1 lens 823 -> 863 (delta 40)
replace base[412:413]=b'4' tip[412:413]=b'7'
delete  base[449:466]=b'payload tree and '
insert  base[477:477]=>tip[460:517]=b' + tag commit and git tree ids; supersedes S094, round 19'
lines 2-163 identical: True
```

All deltas sit inside the `S094 (...)` token span (`S094` at base offset ~409, its closing
`)` before `; S095`); lines 2-163 — including `verified-at:` `:2`, `recheck:` `:3` and every
body/correction line — are byte-identical. So the block's "Head `source:` token S094 was
replaced in place by S097" (`:167`) describes the edit faithfully. It is not a bare id
substitution inside the token: the replacement also deletes the words "payload tree and" and
appends " + tag commit and git tree ids; supersedes S094, round 19". The sentence does not
claim a byte-identical id swap, so this is a precision nit, not an overclaim — and the dropped
"payload tree" descriptor is replaced by stronger coverage (S097's two tree ids plus per-file
blob ids, `corpus/SOURCES.md:109`).

Atomicity: `git show --numstat df84807 -- corpus/knowledge/theme-route-r18.md corpus/SOURCES.md`
→ `6 1` and `14 2`; the head swap, the append block and the S094 rejection landed in the same
commit.

## (b) Live/runtime walker 2.17.2 claim, or un-rehashed "re-verified" — no

```
$ grep -n -i 'walker\|2\.17' /tmp/tr_tip.md   # tip copy
1,86,105,128,139,145  # pre-existing lines only (:1 is S095's consumer list, not the block)
(no '2.17' match anywhere in the file)
```

The round-19 block (`:167-168`) contains no walker sentence and no "re-verified" wording. Its
only non-upstream assertions are host-state facts, and each re-measures true now:

- applied theme: `~/.config/omarchy/current/theme.name` 12 B `matte-black\n`, sha256
  `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b` — equal to the note's own
  `:82` pin; S097 (`SOURCES.md:109`) states `= matte-black, 12 B`.
- 19 dirs: `os.listdir(~/.local/share/omarchy/themes)` → 19 entries, all 19 real
  directories, 0 symlinks, all non-empty; sorted set `diff` against
  `git -C /tmp/omarchy-v384 ls-tree -d --name-only v3.8.4:themes` → empty
  (`19 19 host-only [] tag-only []`).
- `~/.config/omarchy/themes` → `[]`.

Cross-check against the walker delta (`DeltaWalkerConfig.md`: the 2.17.0→2.17.2 change touches
four config defaults only; `:141-146` "User layer (L2) … identical",
`:150-153` "Theme pins … unchanged", `:154-159` packaged theme set 16/16 identical;
`DeltaWalkerCli.md:93`'s only "theme" hit is the walker CLI option name in the 23-flag list,
not the omarchy payload). Independent re-hash of the three walker-adjacent pins the note
carries (`:86`, `:105`) reproduces them exactly under 2.17.2:

```
fecf71fa…  ~/.config/walker/config.toml            1336 B   (note :105)
481267af…  …/walker/themes/omarchy-default/style.css 1243 B (note :105)
f44cb450…  current/theme/walker.css                  191 B   (note :86)
dbb6bbbe…  …/omarchy-default/layout.xml
```

So the note makes no live/runtime claim about walker 2.17.2 and has no stale walker pin that the
block's silence hides.

## (c) Line numbers cited in the block — none; the numeric claims hold

`re.findall(r':\d', block)` finds none: `:167`/`:168` cite paths and ids only (the sole colon
token is the literal field name `source:`). This differs from the sibling
`walker-route-r18.md` block, which does cite `src/base_directories.rs:446-448` etc. So (c) is
vacuous for this block. Its two numeric claims are byte/count values and both reproduce:
`461 B` (raw body, `wc -c` = 461) and `19 theme payload dirs` (census above).

## (d) Cited S### rows support their sentences — yes, both

- **S094** (`corpus/SOURCES.md:106`): anchor cell carries exactly the two per-fetch tree-page
  digests `tree listing sha256 50c1ac25…` and `backgrounds tree sha256 9e1160a0…`; status
  `rejected`, used-by `—`, date 2026-10-20. That supports both clauses ("credited per-fetch
  … digests", "now rejected"). Rotation is not a property of the row but of the committed
  receipts, and it holds: parsing `round-18/…/receipts.jsonl` + `round-19/fetch/HtmlAnchorSweep`
  gives **7 distinct** sha256 for `https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black`
  (incl. the row's `50c1ac25…`) and **6 distinct** for `…/backgrounds` (incl. `9e1160a0…`).
  The named defect is R18-V1 (`corpus/lessons/round-18-verifier-spotcheck.md:117`;
  `corpus/lessons/round-19.md:16` M1), so the block's `(R18-V1)` label is correct.
- **S097** (`corpus/SOURCES.md:109`): title "(supersedes S094)"; anchor `tag v3.8.4 → commit
  8fcc9d60… (lightweight)`, `themes/matte-black tree 3fc08f95…`, `backgrounds tree ff02c341…`,
  raw `colors.toml sha256 dbdd13a6…, 461 B`; scope carries applied-theme + 19-dir census +
  empty `~/.config/omarchy/themes`. Every value in the block's sentence matches verbatim.

Independent re-derivation (my own fetches, bodies under /tmp only; API bodies are
corroboration, not anchors):

| check | command | result |
|---|---|---|
| raw anchor | `curl -sS …/v3.8.4/themes/matte-black/colors.toml` (2026-10-20T18:03:29Z) | `status=200 bytes=461`; sha256 `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`; `:4` `background = "#121212"` |
| tag type/commit | `curl -sSL …/git/refs/tags/v3.8.4` (18:06:23Z) | 200, 368 B, sha256(`body`) `a503d17d…`; `object.sha 8fcc9d6048af4cb0e3af8512c78049857a3b53dd`, `object.type commit` → lightweight |
| 19 names | `curl -sSL …/contents/themes?ref=v3.8.4` (18:06:24Z) | 200, 14 830 B, sha256 `54790892…`; list length 19 |
| matte-black tree + blobs | `curl -sSL …/contents/themes/matte-black?ref=v3.8.4` (18:06:24Z) | 200, 8 408 B, sha256 `a6662a81…`; dir `3fc08f954e5a…`; colors blob `5e1a8cca…` 461 B; other blob ids/sizes equal S097's |
| backgrounds | `curl -sSL …/contents/themes/matte-black/backgrounds?ref=v3.8.4` (18:06:25Z) | 200, 4 175 B, sha256 `7cd9965f…`; dir `ff02c3419383…`; 4 files, sizes 1681677/1033920/482067/4491 = S097 |
| clone ids | `git -C /tmp/omarchy-v384 rev-parse HEAD`; `rev-parse 'v3.8.4:themes/matte-black'`; `…/backgrounds` | `8fcc9d60…`; `3fc08f954e5a…`; `ff02c3419383…` (same clone the block says the ids came from) |
| committed receipt | `.ufo/waves/round-19/fetch/SrcS094/receipts.jsonl` | 200 / 461 / `dbdd13a6…` / `fetched_at 2026-10-20T17:06:08Z`; body re-hash equals record |

## Residual weaknesses (not enough to break the block)

- **G1 — receipt pointer does not cover the new anchor.** `verified-at:` (`:2`) and `:130`
  still name only `.ufo/waves/round-18/fetch/NoteTheme/receipts.jsonl` (which does hold a
  200/461/`dbdd13a6…` raw fetch), while S097's own receipt is
  `.ufo/waves/round-19/fetch/SrcS094/receipts.jsonl`. The block cites no receipt path, so no
  sentence is false, but a verifier following the note's own pointer will find the raw bytes
  and not the tree ids.
- **G2 — `recheck:` cannot reproduce the tree ids.** `:3` says "the tag commit by
  `git ls-remote --tags` only"; that yields the commit but not `3fc08f95…`/`ff02c341…`. The
  block states the clone provenance but not the `git ls-tree` step. Incompleteness, not a
  misstatement.
- **G3 — historical S094 mentions vs `used-by`.** S094's `used-by` is now `—`, yet the note
  still names S094 at `:1` (inside the S097 token), `:158`, `:162` and `:167` (as corrections).
  Same convention as S084
  (`SOURCES.md:96`, used-by `—`, still mentioned in `walker-route-r18.md`), so this is the
  lane's deliberate supersession bookkeeping, not a note overclaim.
- **G4 — heading wording.** `:165` says "append-only" over a block that documents an in-place
  head edit. It mirrors the wave-2 block (`:147`, which also discloses an in-place fix at
  `:149`), so "append-only" reads as "the correction record is appended", not "no other byte
  changed". No contradiction with the observed diff.

## Limits

- API responses were used only as corroboration; per the lane contract API/HTML digests are not
  anchors. The anchor claim itself rests on the content-addressed git ids and the committed
  round-19 receipt, both re-derived.
- `/tmp/omarchy-v384` is the shallow clone wave 1 left behind (HEAD `8fcc9d6…`, tag `v3.8.4`);
  tree ids were re-read from it and independently confirmed against the GitHub contents API,
  so the result does not depend on that ephemeral directory.
- I did not re-fetch the rotating GitHub tree HTML page: rotation is already evidenced by the
  committed per-seat receipts (7/6 distinct), and a fresh HTML digest would prove nothing about
  the anchor. I did not run the gate, `measure.py`, `fresh-pins.py`, or any jj command (host
  pause + item scope). Host reads were name listings, `stat`, `sha256sum`, `cat` only.
- Unknown: whether the lane intends `recheck:`/receipt pointers to be updated for new anchor
  types (G1/G2) or accepts them as block-local provenance — not decidable from this item.

## Installs

none
