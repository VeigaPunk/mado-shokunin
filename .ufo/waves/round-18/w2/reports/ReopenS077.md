# ReopenS077 — non-author re-open of SOURCES S077 (walker src/theme/mod.rs @ v2.17.2)

Seat `MadoR18.ReopenS077`, wave 2 (FALSIFY), 2026-10-20. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`. Read-only in the lane (no git/jj
write, no package/compositor/service/process operation); only `curl` fetches,
file reads, `sha256sum`, `git ls-remote`, and read-only `git show/diff`.

## Row under test

`corpus/SOURCES.md:89` at `4c103b55` (byte-identical to worktree:
`git diff --stat 4c103b55 -- corpus/SOURCES.md` prints nothing):

```
| S077 | walker src/theme/mod.rs @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/theme/mod.rs | code | A | theme directory search and additional_theme_location `~` replacement (cross-ref P5) | file lines 53-64, 132-135; sha256 93287a1c389a4b1856e2736e16246cef90691074023f57521fbb1422a61e0349 | the ~ in additional_theme_location is a literal replace with $HOME, not shell expansion | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |
```

New this round: `grep -c S077` on `d9a5a18:corpus/SOURCES.md` = 0; registry
rows 71 → 95.

## Independent fetch and tag resolution (observed)

```
mkdir -p .ufo/waves/round-18/fetch/ReopenS077
curl -sSL --max-time 60 -o .ufo/waves/round-18/fetch/ReopenS077/theme-mod-rs \
  -w '%{http_code} %{url_effective}\n' \
  https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/theme/mod.rs
→ 200 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/theme/mod.rs

sha256sum theme-mod-rs ; wc -c -l theme-mod-rs
→ 93287a1c389a4b1856e2736e16246cef90691074023f57521fbb1422a61e0349
→ 9364 bytes, 318 lines

git ls-remote https://github.com/abenz1267/walker \
  refs/tags/v2.17.2 'refs/tags/v2.17.2^{}' refs/heads/v2.17.2 refs/heads/master
→ a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/heads/master
→ a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2
```

- Fresh body sha256 **equals the row's anchor cell** (`93287a1c…0349`) and the
  body is 9,364 B / 318 lines.
- **URL is tag-pinned, not commit-pinned.** The path segment `v2.17.2` is a
  tag ref; no `refs/heads/v2.17.2` exists, so the name cannot resolve to a
  branch. There is no peeled `^{}` line: the tag is **lightweight**, i.e. a
  mutable ref. Today it points at the same commit as `refs/heads/master`
  (`a515085f…`), so the tag content is the current branch tip; a force-move
  would be detectable only by re-hashing.
- Tag→content binding checked independently of GitHub's ref resolution: a
  second fetch of the same file at the resolved commit
  `…/walker/a515085fd39fae80acc086c8fbfd9b7771a9a11d/src/theme/mod.rs`
  returned `200`, 9,364 B, sha256 `93287a1c…0349` — byte-identical to the
  tag URL body (`theme-mod-rs.commit`).
- The row lists **one file only** (no second path in `source` or `anchor`), so
  no further row files were re-fetched. Both fetches are receipted in
  `.ufo/waves/round-18/fetch/ReopenS077/receipts.jsonl` (`mado-fetch-receipt-v1`,
  9 fields each).

## Wave-1 receipts for the same URL (observed)

Exactly three committed receipts carry this URL (`git grep 'src/theme/mod.rs'
4c103b55 -- '.ufo/waves/round-18/fetch/*/receipts.jsonl'` → 3 lines). I
re-hashed each receipt's body file in the worktree:

| seat | receipt line | fetched_at (UTC) | status | bytes | sha256 |
|---|---|---|---|---|---|
| `MadoR18.SrcWalkerThemes` | 6 | 2026-10-20T15:40:38Z | 200 | 9,364 | `93287a1c…0349` |
| `NoteWalker` | 13 | 2026-10-20T15:40:52Z | 200 | 9,364 | `93287a1c…0349` |
| `SrcWalkerConfigPaths` | 1 | 2026-10-20T15:41:50Z | 200 | 9,364 | `93287a1c…0349` |
| `ReopenS077` (this seat, tag) | 1 | 2026-10-20T15:59:45Z | 200 | 9,364 | `93287a1c…0349` |
| `ReopenS077` (this seat, commit) | 2 | 2026-10-20T16:00:41Z | 200 | 9,364 | `93287a1c…0349` |

All three wave-1 bodies exist on disk and hash to the same digest
(`sha256sum` run on `src-theme-mod.rs`, `walker-v2.17.2-src-theme-mod.rs`,
`theme-mod.rs`). No receipt for this URL diverges in digest, byte count, or
status; each carries the producer string (`curl 8.23.0 …`). The URL is
therefore reproducibly credited with an independent agreement, and this
non-author re-fetch adds a fourth and fifth identical measurement.

## Row judgement against body bytes

- **kind `code`** — correct: upstream Rust source, not documentation.
- **tier `A`** — justified for this scope: the program's own theme loader at a
  tag ref, content-addressed in the row itself. Primary for "what walker
  2.17.2's theme code does"; it proves nothing about the host binary, and the
  row makes no host claim.
- **scope** — both halves name literal code surfaces. "Theme directory
  search": `let dirs = xdg::BaseDirectories::with_prefix("walker")
  .find_config_files("themes");` (56), collected at 58, and each collected
  path is read as a directory at `let Ok(theme_dirs) = fs::read_dir(config_path)`
  (107) whose subdirectories become named themes (111-128) — the service-mode
  branch (91-130). "`additional_theme_location` `~` replacement": 60-63.
- **surface keywords** — the source cell names `walker` (P3 set) and the scope
  cell names `theme` (P5 set); either rubric-V keyword check is satisfied,
  including the row's cross-ref to P5. Not a keyword-only credit: the anchor
  is line-exact.
- **`teaches`** — grounded: `additional_theme_location` is read via
  `get_config()` (60), `HOME` comes from `env::var("HOME")` (61), and 63 is
  `a.replace("~", &home)` — a Rust `str::replace`, no shell and no `shellexpand`
  call. Two accurate nuances the row does not state (and so cannot
  contradict): the replace is applied to *every* `~` occurrence, not just a
  leading one, and the append is skipped entirely when `HOME` is unset
  (`if let Ok(home)` at 61).
- **status `mined`, `opened 2026-10-20`, `on-release`** — `mined` matches the
  note cite; `on-release` is the right cadence for a tag-pinned source.
- **Anchor line ranges** — 53-64 spans the `setup_themes` signature through
  the `config_paths.push` call and its closing brace; 132-135 is the
  `themes.contains_key("default")` fallback. Both are exact.

## Citing-note truthfulness (`corpus/knowledge/walker-route-r18.md`)

The note at `4c103b55` is byte-identical to worktree (`git diff --stat` empty). It
declares `surface: P3` (line 4) and cites S077 in its head `source:` line. Its
three `WT:` uses check out:

- `[WT:56]` "`setup_themes` collects `find_config_files("themes")`" — true,
  literal call at 56.
- `[WT:60-63]` "appends `additional_theme_location` with `~` replaced by
  `$HOME` via `a.replace("~", &home)` … a literal substring replace, not a
  shell expansion" — true on 60-63.
- `[WT:132-135]` "A missing `default` theme falls back to the compiled theme"
  — true: `Theme::default()` (30-50) builds its layout/keybind/preview from
  `include_str!("../../resources/themes/default/…")`, i.e. compiled-in bytes.
- The note's cross-ref sentence ("Theme contents are the P5 route's subject
  and are not inspected further here") is an honest scope statement; the P5
  note (`corpus/knowledge/theme-route-r18.md`) does not cite S077 (`grep -c`
  = 0), so the row's `used-by` listing only the walker note is complete.

What the note omits: the `read_dir` scan is the `is_service` branch (92-105
joins the theme *name* instead when the client is not the service), and the
`HOME` guard. Both are omissions of detail, not misstatements; nothing in the
note asserts behaviour the bytes contradict.

## Confidence

- Digest/anchor identity, three wave-1 receipts, and the tag→commit binding:
  **high** (five independent 200 bodies, all `93287a1c…0349`).
- Row kind/tier/scope/teaches: **high** (line-exact against the fetched bytes).
- Note truthfulness: **high** for every `WT:` citation.

## Remaining unknowns (not resolvable by this re-open)

- Whether upstream force-moves the lightweight `v2.17.2` tag (currently equal
  to `master` HEAD `a515085f…`); only a future re-fetch can detect it.
- Whether `/usr/bin/walker` on the host is a build of these tag bytes — out of
  scope for a documentary row and `[UNK]`.
- Theme rendering/selection behaviour (`[UNK]` in the note; no launcher run,
  per host pause).

GATE | S077 | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/theme/mod.rs | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS077/theme-mod-rs:63 "config_paths.push(PathBuf::from(a.replace("~", &home).to_string()));" (2 words) | 93287a1c389a4b1856e2736e16246cef90691074023f57521fbb1422a61e0349 | agree: fresh 200 body equals the row anchor and all three wave-1 receipts (9,364 B each, re-hashed); tag v2.17.2 resolves to a515085f… (lightweight, no peeled line, no v2.17.2 branch) and a commit-pinned fetch at a515085f is byte-identical, so the URL is tag-pinned not commit-pinned; kind code, tier A, scope keywords walker (P3) and theme (P5 cross-ref) hold, and the note's WT:56/60-63/132-135 citations are line-accurate
