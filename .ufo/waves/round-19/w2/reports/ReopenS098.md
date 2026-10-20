# MadoR19.ReopenS098 — partial

Item: re-open S098 (`xdg` 3.0.0 crate tarball) at tip
`01b80946d92b26370d3012a7da655d00dd135154`. Two questions: do the row's byte
claims hold, and is S098 a faithful replacement for **every** use S084 had in
`corpus/knowledge/walker-route-r18.md` (`XD:` citations)?

Bottom line: the row's byte claims hold end-to-end, and all three numeric `XD:`
citation classes have exact counterparts in the crate. But the replacement **as
landed** is partial: the head `source:` line still carries the rejected id
`S084` inside the S098 entry, so the lane's own strict join checker goes
PASS → FAIL, and the unchanged `verified-at:` receipt sentence is false for
S098's body. Both integration defects are also reported by the concurrent peer
`AtkPtrWalkerRouteR18` and are repaired in the uncommitted w2 worktree; this
seat re-derived them from separate bytes. One precision issue is unique to this
check: the appended correction points the two *default* citations at
implementation lines, while the verbatim docs prose S084 carried is at
`src/base_directories.rs:217` and `:221`, not `:308-310`/`:321-323` as "same
text".

## 1. Fresh fetches (bodies under /tmp/r19s098, curl only)

```
url|status|bytes|sha256|fetched_at
https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.lock|200|70247|3448367c28c769e29f681ea2de84d4a822f08569bbef6628f03535c61fec2315|2026-10-20T18:03:06Z
https://static.crates.io/crates/xdg/xdg-3.0.0.crate|200|15821|2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5|2026-10-20T18:03:06Z
https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs|200|19675|93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469|2026-10-20T18:03:06Z
https://raw.githubusercontent.com/abenz1267/walker/a515085fd39fae80acc086c8fbfd9b7771a9a11d/Cargo.lock|200|70247|3448367c…ec2315|2026-10-20T18:05:10Z
https://raw.githubusercontent.com/abenz1267/walker/a515085fd39fae80acc086c8fbfd9b7771a9a11d/src/config.rs|200|19675|93b6bd6f…ad1469|2026-10-20T18:05:11Z
https://raw.githubusercontent.com/whitequark/rust-xdg/c0f6bc329b0fd92b015a55bcbbee72b2864fae4b/src/base_directories.rs|200|48474|335a4a3001057c1c97a7c4eae86c9b3f1210c5492dbe42dca0599bc698e47570|2026-10-20T18:07:44Z
https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html|200|105537|0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d|2026-10-20T18:06:04Z
https://crates.io/api/v1/crates/xdg|200|27028|4694b10656def0d868b5e9da0715dfd1e11c73f1f22556e5a527a0e878012e02|2026-10-20T18:06:04Z
```

`git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'`
→ one line, `a515085fd39fae80acc086c8fbfd9b7771a9a11d refs/tags/v2.17.2`
(no peeled line: lightweight tag, as the note's tag-resolution paragraph says).
Tag-pinned and commit-pinned lock/config bodies hash identically to each other
and to the row.

## 2. Lock lines 2705-2708 — exact

`nl -ba /tmp/r19s098/Cargo.lock | sed -n '2698,2720p'` (same as the
tip-committed, receipted body `.ufo/waves/round-19/fetch/SrcS084/walker-v2.17.2-Cargo.lock`
sha `3448367c…`):

```
2704  [[package]]
2705  name = "xdg"
2706  version = "3.0.0"
2707  source = "registry+https://github.com/rust-lang/crates.io-index"
2708  checksum = "2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5"
```

Line 2707 also proves the crate is the **crates.io registry** package, not a
git/path patch; `grep -c '^name = "xdg"'` = 1 (single xdg in the graph), and
`walker`'s own `Cargo.toml` (`fetch/DeltaWalkerCli/v2.17.2-Cargo.toml:30`)
declares `xdg = "3.0.0"`. So the crate the row pins is the one the build resolves.

## 3. Checksum triangle — holds

- crate body `15,821 B`, sha256 `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`;
- equals lock `:2708` registry checksum;
- crates.io API today: `max_version 3.0.0`, first published `2025-05-04T10:42:18Z`;
- six committed receipts (round-18 `MadoR18.RevengeTarballRepro` 16:02:39Z,
  round-18 `SrcWalkerConfigPaths` 15:41:50Z, round-19 `SrcS084` 17:06:24Z,
  round-19 `FrontierRows` 17:07:34Z, round-19 `DeltaWalkerCli`, round-19
  `RevRubricVRisk` 18:01:23Z) all `200 / 15821 / 2fb43323…` — no rotation;
- my 18:03:06Z fetch is a seventh identical observation.

Second channel: extracting the tarball gives
`xdg-3.0.0/src/base_directories.rs` sha `335a4a30…47570`, **byte-identical**
(`diff -q` silent) to the upstream repo file at the crate's
`.cargo_vcs_info.json` commit `c0f6bc329b0fd92b015a55bcbbee72b2864fae4b`. The
crate is not a repack with different source, and the cited line numbers are the
repo's.

## 4. `src/base_directories.rs` line ranges — all exact

```
446  /// Given a relative path `path`, returns an absolute path to an existing
447  /// configuration file, or `None`. Searches `XDG_CONFIG_HOME` and then
448  /// `XDG_CONFIG_DIRS`.
449  pub fn find_config_file<P: AsRef<Path>>(&self, path: P) -> Option<PathBuf> {
457  }
308      let config_home = env_var("XDG_CONFIG_HOME")
309          .and_then(abspath)
310          .or_else(|| home.as_ref().map(|home| home.join(".config")));
321      let config_dirs = env_var("XDG_CONFIG_DIRS")
322          .and_then(abspaths)
323          .unwrap_or(vec![PathBuf::from("/etc/xdg")]);
757  fn read_file(  … 776      }   777  }
```

- `:446-448` is the verbatim quote the lesson Gate line renders
  (`corpus/lessons/round-19.md:43`, "Searches `XDG_CONFIG_HOME` and then
  `XDG_CONFIG_DIRS`." — 6 words).
- `:308-310` / `:321-323` implement the `~/.config` and `/etc/xdg` defaults.
- `:757-777` is stronger than the docs page for the note's `INF`: `read_file`
  tests `home` first, returns on the first existing path, then iterates
  `dirs` in order — the note's "first hit wins" (`walker-route-r18.md:80`) is
  code-visible, not only prose.

The **verbatim** docs prose S084 carried for the defaults is at crate `:217`
("`XDG_CONFIG_HOME`; if not set: assumed to be `$HOME/.config`.") and `:221`
("`XDG_CONFIG_DIRS`; if not set: assumed to be `/etc/xdg`."), matching the
saved docs page's `XD:302` / `XD:306` after tag stripping. See §7 finding F3.

## 5. Walker call site — exact

`/tmp/r19s098/walker-src-config.rs:218-219`:

```
218  if let Some(user_config_path) =
219      xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")
```

Fetched body sha `93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469`
equals the row's recorded config.rs sha; tag and commit URLs agree. `with_prefix`
sets both prefixes to `walker` (`crate:236-237`), so the config-dirs join is
`/etc/xdg/walker/config.toml` — the note's line 204/80 claim.

## 6. Row and durability

`python3 -I .ufo/waves/round-19/anchor-durability.py 01b80946 --rows S098,S084`:

```
skipped: S084 status=rejected
ROW S098 durable — no page digest; anchor pins 40-hex commit a515085fd39fae80acc086c8fbfd9b7771a9a11d
SUMMARY rev=01b80946d92b26370d3012a7da655d00dd135154 mined=1 durable=1 per_fetch_digest=0 unpinned_alias=0 flagged=0
exit=0
```

Round-18 strict join, at tip:
`JOIN S098 web receipts=2 sha=2fb433233f2d… anchor=ok seats=MadoR18.RevengeTarballRepro,SrcWalkerConfigPaths`
— S098 satisfies all four join rules (registry row, `mined`, `used-by` =
`corpus/knowledge/walker-route-r18.md`, 200 receipt whose full sha is in the
anchor). `corpus/SOURCES.md:110` S098 `mined`; `:96` S084 `rejected`, used-by
`—`; census 98 rows / A 91 / mined 81 / rejected 9, matching
`corpus/lessons/round-19.md:44-48`. The S098 `teaches` cell names the replaced
id (`supersedes S084 —`) and absorbs S084's old teaches sentence including both
defaults.

## 7. `XD:` replacement — the ticket's question

Every use of S084 in the note at tip (`git show 01b80946:corpus/knowledge/walker-route-r18.md`):

| Use | Line(s) | S084 text | S098 counterpart | Verdict |
|---|---|---|---|---|
| head source token | 1 | S084 docs.rs entry | S098 crate entry | replaced, but S084 token residual (F1) |
| `XD` key row | 33 | docs.rs URL, 105,537 B | none — declared historical | retained alias, mapped at :327 (F4) |
| search order `XD:356-358` | 78-79, 204, 294 | "Searches XDG_CONFIG_HOME and then XDG_CONFIG_DIRS" | crate `:446-448` | verbatim |
| config-home default `XD:302` | 79 | "assumed to be $HOME/.config" | crate `:217` verbatim; `:308-310` impl | exact (F3 wording) |
| config-dirs default `XD:306` | 79 | "assumed to be /etc/xdg" | crate `:221` verbatim; `:321-323` impl | exact (F3 wording) |

`grep -o 'XD:[0-9]*(-[0-9]*)?'` over the note yields exactly
`XD:302 ×1, XD:306 ×1, XD:356-358 ×3` (plus the two bare `XD:n` definitions at
:33/:327), so the mapping above is exhaustive. No other S084 dependency exists:
`find_config_files("themes")` at :119 is walker's own `WT:56` (S077,
`src/theme/mod.rs`), not the xdg crate — S098's head description dropping the
plural loses nothing the note uses. **Content-wise the replacement is faithful;
line-number-wise it is a translation, not identical anchors.**

Findings:

- **F1 (defect at tip, integration).** The S098 head entry ends
  `…; supersedes S084, round 19)`, so `S084` is still an `S###` token on the
  `source:` line. The note's correction (`:327`) says the "Head `source:` token
  S084 … was replaced in place by S098" — not at token level. Measured with the
  lane's committed round-18 checker:
  - tip: `GAP corpus/knowledge/walker-route-r18.md:1 S084 not-mined detail=status='rejected'`,
    `RESULT FAIL`, exit 1 (`SUMMARY … gaps=2`, the sibling gap is the theme
    note's S094);
  - baseline `9c54c56`: `RESULT PASS`, exit 0, `gaps=0` — so this is a
    **regression introduced by the S098 landing**, not pre-existing;
  - uncommitted worktree (peer fix): `RESULT PASS`, exit 0, `gaps=0`;
    head segment now reads `…; round-19 re-point, see the correction block)`.
  Concurrent peer `AtkPtrWalkerRouteR18` reported the same failure; this seat's
  run reproduces the numbers independently.
- **F2 (defect at tip, provenance).** `walker-route-r18.md:2` still says "every
  raw body curl-fetched with a receipt in
  `.ufo/waves/round-18/fetch/NoteWalker/receipts.jsonl`". That file's 27 URLs
  contain S084's docs.rs page but **no** `static.crates.io` URL and no walker
  `Cargo.lock`. S098's crate receipts are in other round-18 dirs
  (`MadoR18.RevengeTarballRepro` 16:02:39Z, `SrcWalkerConfigPaths` 15:41:50Z;
  both receipt files tracked at tip) and round-19 `SrcS084` (17:06:24Z). The
  sentence is therefore false for the body now cited on the same header. The
  uncommitted w2 worktree appends a correction naming the round-19 receipt, but
  does not amend line 2 itself.
  [INF] A charitable reading scopes the sentence to the round-18 body set; it
  still fails as a present-tense provenance header after the swap, and the peer
  read it the same way.
- **F3 (precision, unique to this check).** The correction says `XD:n`
  citations "read as the same text at S098 `src/base_directories.rs` (…
  defaults `:308-310`, `:321-323`)". For the two default citations the text at
  those lines is Rust code, not the docs bullet: the **same text** is at `:217`
  and `:221`. The defaults are correctly implemented at `:308-310`/`:321-323`,
  so the claim is true in substance and the pointers just name the
  implementation. No fix required for truth; a reader chasing "same text"
  should be sent to `:217`/`:221`.
- **F4 (declared residual).** The `XD` key row (`:33`) still defines `XD:n`
  against the rejected alias URL; the S098 mapping lives 294 lines later at
  `:327`. Criterion 28 is satisfied at file level (the pointer exists and names
  S098/S084), and the sweep is file-level by its stated limit, but no pinned
  object contains the `XD` line numbers — the note's citations are resolvable
  only through the translation.

## Limits

- Verdict is on committed tip `01b80946`; the worktree carries uncommitted w2
  edits (heads of both route notes, `supersessions.json`, `SCORECARD.md`,
  `QUALITY.md`, etc.). Where worktree differs I say so; I edited nothing.
- The crate body is digest-only (`.ufo/waves/round-19/fetch/.gitignore`), so
  reproducing the extracted lines requires re-fetching the immutable crate; the
  registry checksum makes that deterministic. Six committed receipts already
  agree.
- Did not rebuild walker or read a PKGBUILD; "walker resolves xdg 3.0.0 from
  crates.io" is the lock + registry chain, not a build observation.
- Did not run the gate or any gate copy; no host mutation, no pacman/sudo/
  systemctl. The docs.rs alias still reproduces today (`0291cfe6…`, 105,537 B,
  200 at 18:06:04Z) and crates.io still reports 3.0.0 as max — S084's defect is
  pinlessness, not rotation.
- `[UNK]` remains exactly where the note says: the actual first-hit order on
  this host under a varied `XDG_CONFIG_HOME` was not exercised, and the running
  walker process's binary is not observed.
- The theme-note `S094` gap emitted by the same join run belongs to the S097
  ticket, not to S098.

## Installs

none.
