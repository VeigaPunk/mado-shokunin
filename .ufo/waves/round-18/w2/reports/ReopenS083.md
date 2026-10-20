# Reopen S083 — elephant pkg/common/config.go @ v2.22.1 (R17-V3 non-author check)

Lane HEAD `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`; integration commit
`4c103b55b1ea5c3c555884afe3eb69b5189701b7` (`round-18: wave-1 integration …`).
Row S083 and the three wave-1 receipts were read at `4c103b5` (`git show`);
`corpus/SOURCES.md` is byte-identical between `4c103b5` and `abfbf35`.
No git/jj write, no package/service/socket/REA action; bytes read only.

## Commands and output (observed)

```
curl -sSL --max-time 60 -o .../fetch/ReopenS083/elephant-v2.22.1-pkg-common-config.go \
  -w '%{http_code} %{url_effective}' \
  https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/pkg/common/config.go
→ 200 https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/pkg/common/config.go
sha256sum → 46ed4755bb3e1c17d839688e21d7ce7de33cd494ab41238e90d75c2486e0c63a
wc -c     → 3609

curl -sSL ... https://raw.githubusercontent.com/abenz1267/elephant/\
  8f1e21d6efe40b8b3953f95b9574f99f717caf91/pkg/common/config.go
→ 200; sha256 46ed4755…c63a; 3609 B; cmp with the tag body → IDENTICAL

git ls-remote https://github.com/abenz1267/elephant refs/tags/v2.22.1 'refs/tags/v2.22.1^{}'
→ 8f1e21d6efe40b8b3953f95b9574f99f717caf91	refs/tags/v2.22.1
   (no peeled line → lightweight tag)
```

Own receipts appended to `.ufo/waves/round-18/fetch/ReopenS083/receipts.jsonl`
(two lines, schema `mado-fetch-receipt-v1`, 16:00:22Z and 16:00:50Z). The row's
source and anchor cells name no second file, so no further re-fetch applies.

## Digest comparison (all agree)

| source | URL ref | bytes | sha256 | note |
|---|---|---|---|---|
| row S083 anchor | `v2.22.1` tag | — | `46ed4755…c63a` | full 64 hex matches |
| wave-1 `NoteWalker` receipts:16 | `v2.22.1` tag | 3609 | `46ed4755…c63a` | body on disk re-hashed OK, 15:40:52Z |
| wave-1 `SrcElephantProviders` receipts:15 | `v2.22.1` tag | 3609 | `46ed4755…c63a` | body on disk re-hashed OK, 15:41:32Z |
| wave-1 `SrcElephantReadme` receipts:11 | commit `8f1e21d6…` | 3609 | `46ed4755…c63a` | body on disk re-hashed OK, 15:43:07Z |
| this re-open | tag and commit | 3609 | `46ed4755…c63a` | two independent fetches |

Three wave-1 seats, two different ref forms (tag and resolved commit), plus this
non-author fetch: four independent observations of one digest.

## Tag pin

The URL path carries the ref `v2.22.1`, not a commit SHA, so the pin is to a
**lightweight tag ref** (`8f1e21d6…`), which is mutable in principle (a force
re-point would change the bytes). The row is still reproducible two ways: the
raw URL resolves today to the same commit, and the recorded content sha256
detects any re-point. Two of the three wave-1 seats fetched the tag, one the
commit; both give the same 3609 B. This satisfies the round-18 admitted class
"tag-pinned raw files whose receipts agree across seats". It is not
content-addressed.

## Anchor verification (body lines, fetched file)

- 16-36: `type Config struct` (16), `type Command struct` (23),
  `type ElephantConfig struct` (28) with `ProviderHosts` (:29),
  `AutoDetectLaunchPrefix` (:30), `LaunchPrefix` (:31), `TerminalCmd` (:32),
  `OverloadLocalEnv` (:33), `IgnoredProviders` (:34), `GitOnDemand` (:35),
  `BeforeLoad []Command` (:36). All three named fields present.
- 41-48: `func LoadGlobalConfig()` sets the three defaults and calls
  `LoadConfig("elephant", elephantConfig)` at :48.
- 76-96: `func LoadConfig`; defaults load failure → `os.Exit(1)` (:82);
  `ProviderConfig` error → `slog.Info(provider, "config", "using default
  config")` then `return` (:85-89); `user.Load(file.Provider(userConfig),
  toml.Parser())` failure → log + `os.Exit(1)` (:93-97).
- All claimed line ranges and every `teaches` clause reproduce verbatim.

## Judgment

- **kind `code`** — upstream Go source. Correct.
- **tier A** — primary upstream source at the release tag for an
  upstream-code scope. Correct.
- **scope** "elephant global config struct and loader at tag v2.22.1" names
  the P3 surface keyword *elephant*; the source cell also names it. Passes
  the P3 keyword rule.
- **`teaches`** grounded: "using default config" (:87), `os.Exit(1)` on
  malformed user config (:96), and the three fields (:29, :31, :36) are all
  in the fetched body.
- **citing note** `corpus/knowledge/walker-route-r18.md` uses EG truthfully:
  :145-146 (`LoadGlobalConfig` → `LoadConfig("elephant", …)` at 41-48),
  :146-147 (field list at 28-36, a subset without a completeness claim),
  :147-149 (missing file → log + return at 85-89; parse error → exit 1 at
  93-96), :212 (`EG:85-89` for the global config — an inference whose unread
  resolver the note discloses at :307-308), :308 ("`EG:85` is the only call
  site read" — true of the fetched set). `theme-route-r18.md` does not cite
  S083.

## Precision notes (not defects for this row)

1. The "missing user config" clause is the `err != nil` arm of
   `ProviderConfig`; the missing-file → error mapping lives in that function,
   which is not in this file. The note flags `ProviderConfig` unread in its
   `[UNK]` ledger (:307-308), so the row states the observable outcome
   without claiming the resolver's internals.
2. `LoadConfig` continues past :96 (merge/unmarshal exits at :99-109); the
   row's 76-96 stops at the claimed malformed-file exit and claims nothing
   about the later arms.
3. "tag-pinned" should be read as ref-pinned + digest-anchored, not
   content-addressed (see Tag pin).

## Remaining unknowns

- `ProviderConfig` (file-not-found vs other error distinction) — not fetched.
- Whether a `user.Load` parse failure on the global `elephant.toml` ever
  occurs on this host — the note says no `elephant.toml` exists; not
  re-checked here (out of this row's scope; host bytes untouched).
- Whether the tag was signed/annotated upstream: `git ls-remote` shows a
  lightweight ref only.

GATE | S083 | https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/pkg/common/config.go | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS083/elephant-v2.22.1-pkg-common-config.go:87 "slog.Info(provider, \"config\", \"using default config\")" (5 words) | 46ed4755bb3e1c17d839688e21d7ce7de33cd494ab41238e90d75c2486e0c63a | agree: independent fetch reproduces the row digest (3609 B); tag v2.22.1 resolves to lightweight 8f1e21d6 and the commit-pinned body is byte-identical; all three committed wave-1 receipts agree; the claimed lines, three fields and both exit paths reproduce
