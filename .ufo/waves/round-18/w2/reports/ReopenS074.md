# ReopenS074 — non-author re-open of SOURCES S074 (walker src/config.rs @ v2.17.2)

Seat: `MadoR18.ReopenS074`, wave 2 (FALSIFY), 2026-10-20. Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Read-only: no git/jj write in the
lane, no package/compositor/service command, no process probe.

## Row under test

`corpus/SOURCES.md:86` at `4c103b55` (identical to worktree bytes):

```
| S074 | walker src/config.rs @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs | code | A | config load order (embedded default, XDG user file, WALKER_ env overlay), read-once OnceLock | file lines 7-8, 211-243, 586-594; sha256 93b6bd6f…1469 | defaults first; user file via xdg find_config_file; user parse errors non-fatal, build errors propagate; config set once per process | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |
```

## Independent fetch and tag resolution (observed)

Commands and exact results:

```
mkdir -p .ufo/waves/round-18/fetch/ReopenS074
curl -sSL --max-time 60 -o .ufo/waves/round-18/fetch/ReopenS074/walker-src-config.rs \
  -w '%{http_code} %{url_effective}\n' \
  https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs
→ 200 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs

sha256sum .ufo/waves/round-18/fetch/ReopenS074/walker-src-config.rs
→ 93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469
wc -c -l → 19675 bytes, 594 lines

git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 refs/tags/v2.17.2^{}
→ a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2
```

- Fresh body sha256 **equals** the row's anchor cell sha256 (`93b6bd6f…1469`)
  byte for byte; the anchor's byte count is implied by the digest and matches
  19,675 B.
- **Tag-pinned, not commit-pinned.** The URL path segment `v2.17.2` is a tag
  ref; `git ls-remote` returns `a515085f…` with no peeled `^{}` line, i.e. a
  **lightweight** tag. A lightweight tag is a mutable ref, so the URL is
  reproducible only while upstream does not force-move `v2.17.2`; the digest
  makes any such move detectable on re-fetch.
- The row lists exactly one file (no further files in its source/anchor
  cells), so no extra row files required re-fetch. I additionally fetched
  `src/main.rs` only to test the citing note's inference half (below):
  `200`, 26,673 B, sha256 `f09466fe…7e60`, saved as
  `.ufo/waves/round-18/fetch/ReopenS074/walker-src-main.rs`.
- Both fetches are receipted in
  `.ufo/waves/round-18/fetch/ReopenS074/receipts.jsonl`
  (`mado-fetch-receipt-v1`, 9 fields each).

## Wave-1 receipts for the same URL (observed)

`grep -l 'src/config.rs' .ufo/waves/round-18/fetch/*/receipts.jsonl` → three
seats, and all three bodies still hash to the row digest:

| seat | fetched_at (UTC) | bytes | sha256 | body file hash |
|---|---|---|---|---|
| `MadoR18.SrcWalkerThemes` | 2026-10-20T15:40:39Z | 19,675 | 93b6bd6f…1469 | equal |
| `NoteWalker` | 2026-10-20T15:40:52Z | 19,675 | 93b6bd6f…1469 | equal |
| `SrcWalkerConfigPaths` | 2026-10-20T15:41:50Z | 19,675 | 93b6bd6f…1469 | equal |

Three independent seats, one non-author seat (this one) and three receipted
wave-1 fetches all agree; no receipt for this URL carries a divergent digest
or byte count. No R17-V3/R17-V1 defect found on this row: producer tool string
is present (`curl 8.23.0 …`) and the measured revision is implicit in the
tag-pinned URL plus digest.

## Row judgement against body bytes

Anchor ranges verified line-exact in the fetched body:

- **7-8** — `static LOADED_CONFIG: OnceLock<Walker> = OnceLock::new();` and
  `const DEFAULT_CONFIG: &str = include_str!("../resources/config.toml");`
- **211-243** — `impl Walker { pub fn new() … }`: 212-214 builds from
  `File::from_str(DEFAULT_CONFIG, FileFormat::Toml)`; **216**
  `let mut config: Walker = default_config.try_deserialize()?;`; **218-219**
  `xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`;
  **221-223** user `Config::builder() … .build()?` (propagates);
  **225-231** `try_deserialize` error arm calls `set_error(...)` and
  `println!` and does not return; **234-239** env overlay
  `config::Environment::with_prefix("WALKER").separator("_")`, merged only
  inside `if let Ok(partial)`.
- **586-594** — `load()` calls `LOADED_CONFIG.set(Walker::new()?)` and maps a
  second set to `"Failed to set loaded config"`; `get_config()` is
  `.get().expect("config not initialized")`.

Verdicts on the row's cells, each grounded in the bytes above:

- **kind `code`** — correct: an upstream Rust source file, not docs.
- **tier `A`** — justified for this scope: primary source (the program's own
  loader), versioned by tag, content-addressed by sha256 in the row itself.
- **scope / surface keyword** — the source cell names `walker`; scope words
  (embedded default, XDG user file, `WALKER_` env overlay, read-once
  `OnceLock`) are all literal features of the anchor ranges. P3 keyword
  satisfied via the source cell.
- **`teaches`** — every clause is directly observed: defaults deserialised
  first (216); user file located by xdg `find_config_file("config.toml")`
  (218-219); user deserialise errors are non-fatal while `build()` errors
  return through `?` (221-231); the config is stored once in a `OnceLock`
  (7, 586-594). No forward projection; the row does not claim host runtime
  behaviour.
- **status / dates** — `mined`, opened 2026-10-20, `on-release`: consistent
  with the tag-pinned source and the integration commit.

## Citing-note truthfulness (`corpus/knowledge/walker-route-r18.md`)

The note at `4c103b55` hashes `3ff430a4…fbf20`, equal to worktree bytes.
Every `WS:` use checked against the body:

- `[WS:8, 212-216]` embedded default first — true.
- `[WS:218-219]` `find_config_file` — true, quoted call matches.
- `[WS:221-226, 245 onward]` user merge via `PartialWalker` — true
  (`merge(res)` at 226; `fn merge(&mut self, partial: PartialWalker)` at 245).
- `[WS:234-239]` env overlay and `[WS:238]` deserialise gate — true.
- `[WS:221-223]` user build error returns through `?` — true. The note's
  further step ("`load()` is then unwrapped at `WM:108`, so the process
  panics (INF …)") is labelled INF; I checked the extra fetch:
  `src/main.rs:108` is `config::load().unwrap();` — the inference is sound.
- `[WS:7]`, `[WS:586-589]`, `[WS:592-594]` read-once — true, including the
  literal `"Failed to set loaded config"` and `expect("config not initialized")`.
- Note lines 74-90 also delimit what is *not* claimed: first-hit-wins
  `/etc/xdg` fallback is marked INF from the xdg crate docs, and `WS:245-`
  body was not read line by line. Both labels are honest against the bytes.
  No `WS:` citation overstates S074.

## Confidence

- Digest/anchor identity and receipt agreement: **high** (byte re-fetch,
  three independent receipts, all sha256-equal).
- Row accuracy (kind/tier/scope/teaches): **high** (line-exact, every clause
  reproduced).
- Note truthfulness for config.rs claims: **high**; for the `WM:108` panic
  inference: **high** on unwrap presence, **medium** on the unobserved
  process outcome (the note itself marks it INF and `[UNK]` in § UNKNOWNs).

## Remaining unknowns (not resolvable by this re-open, by design)

- Whether upstream ever force-moves the lightweight `v2.17.2` tag (only a
  future re-fetch can tell; digest pins drift detection).
- `/etc/xdg` fallback reachability and `WALKER_*` name mapping are `[UNK]`
  in the note and remain `[UNK]` here; S074 is documentary, not a run.
- Whether the host `/usr/bin/walker` (2.17.2-1 per pacman.log) is a faithful
  build of the tag — out of scope for this row and still `[UNK]`.
- No package/compositor/service/process operation was used, per host pause.

GATE | S074 | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS074/walker-src-config.rs:216 "let mut config: Walker = default_config.try_deserialize()?;" (6 words) | 93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469 | agree: fresh 200 body sha256 equals row anchor and all three wave-1 receipts; tag v2.17.2 is a lightweight tag (a515085f…, no peeled line) so URL is tag-pinned not commit-pinned; kind code/tier A/scope keyword walker all hold, and the note's WS: citations are line-accurate
