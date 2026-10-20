# ReopenS080 — non-author re-open of SOURCES row S080 (route R17-V3)

Seat `MadoR18.ReopenS080`. Baseline of the row: lane at integration commit
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`; receipts commit
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. No git/jj write; no package,
service, compositor, socket or REA operation. Tools installed: none.

Question: is the newly credited row S080 (`corpus/SOURCES.md:92`) supported by
bytes a non-author can re-fetch and re-hash, and does
`corpus/knowledge/walker-route-r18.md` (surface P3) use it truthfully?

## Commands and output (verbatim, condensed only where noted)

1. Row bytes — `sed -n '92p' corpus/SOURCES.md`:

```
| S080 | elephant README @ v2.22.1 — https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md | docs | A | elephant usage, config directory layout, service management, socket note at tag v2.22.1 | file lines 123-141, 166, 181-192, 211; sha256 aa19a7e2d1c07bf1852b65fd38ca24a6b04bba0dacfd9f6cb02ada0ee0b61389 | ~/.config/elephant layout (elephant.toml, .env, <provider>.toml); --config flag; README socket path /tmp/elephant.sock is stale against source | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |
```

   Column parse: 13 cells, unique id (1 occurrence), cell 3 `docs`, cell 4 `A`,
   cell 8 `mined`, cell 11 the note path (exists). Line 92 sits inside
   `## Registry` (starts line 9; next heading `## Paths` line 109).

2. Tag resolution — `git ls-remote https://github.com/abenz1267/elephant 'refs/tags/v2.22.1*' 'refs/heads/*'`:
   one tag line `8f1e21d6efe40b8b3953f95b9574f99f717caf91 refs/tags/v2.22.1`,
   **no** `refs/tags/v2.22.1^{}` peeled line, and no `refs/heads/v2.22.1`
   among the 11 branches returned (`0.1.0 0.2.0 0.3.0 1.0.0 2.0.0 3.0.0 dev
   googlecalender master niriapplaunchstuff update-vendor-hash`). The tag is
   lightweight and unobstructed at the URL's ref position.

3. Re-fetch — `curl -sSL --max-time 60 -o .ufo/waves/round-18/fetch/ReopenS080/elephant-v2.22.1-readme.md -w '%{http_code} %{url_effective}' https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md`:
   `200 https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md`;
   `sha256sum` = `aa19a7e2d1c07bf1852b65fd38ca24a6b04bba0dacfd9f6cb02ada0ee0b61389`;
   `wc -c -l` = `6969` bytes, `278` lines; `date -u` = `2026-10-20T15:59:54Z`.
   Receipt appended to `.ufo/waves/round-18/fetch/ReopenS080/receipts.jsonl`
   (`mado-fetch-receipt-v1`).

4. Receipt join — every `fetch/*/receipts.jsonl` line whose `url` is the exact
   S080 URL (parsed with `json`):

```
NoteWalker            line 2 2026-10-20T15:40:36Z 6969 aa19a7e2…  elephant-v2.22.1-readme.md     200 curl
SrcElephantProviders  line 1 2026-10-20T15:41:32Z 6969 aa19a7e2…  elephant-v2.22.1-README.md     200 curl
SrcElephantReadme     line 1 2026-10-20T15:42:29Z 6969 aa19a7e2…  README.md.body                 200 curl
ReviewWalkerUpstream  line 8 2026-10-20T16:00:36Z 6969 aa19a7e2…  elephant-2.22.1-readme.md      200 curl
ReopenS080            line 1 2026-10-20T15:59:54Z 6969 aa19a7e2…  elephant-v2.22.1-readme.md     200 curl
```

   The three wave-1 seats and the two later fetches agree byte-for-byte. The
   bodies on disk also hash equal by `sha256sum`
   (`SrcElephantReadme/README.md.body`, `NoteWalker/elephant-v2.22.1-readme.md`,
   `SrcElephantProviders/elephant-v2.22.1-README.md` = `aa19a7e2…`), so the
   bodies were not edited after receipting.

5. Same path at the resolved commit —
   `curl … /8f1e21d6efe40b8b3953f95b9574f99f717caf91/README.md` → `200`,
   `sha256 aa19a7e2…`, `cmp` against the tag fetch → `BYTE_IDENTICAL`.
   `python3` git-blob identity of the body: `29d94a6b3b76c29bb794a48b88aba45579844ed7`
   (6969 B). Extra oracle attempted: GitHub contents API
   (`…/contents/README.md?ref=v2.22.1`) → `403` rate limit (body:
   `API rate limit exceeded for 179.218.13.209`), receipted; not used.

6. Cited anchors read at numbered lines (`awk 'NR>=…'`):
   `123` environment sentence; `125` `### Starting the Service`; `127`
   `elephant service enable/disable`; `129` unit file
   `~/.config/systemd/user/elephant.service`; `140-141`
   `elephant --config /path/to/config`; `166` `elephant listproviders`;
   `181` `### Configuration`; `183` "configuration directory structure";
   `186-189` the tree `~/.config/elephant/` → `elephant.toml`, `.env`,
   `<provider>.toml`; `192`/`194` `elephant generatedoc`; `211`
   "1. Connect to the Unix socket (typically at `/tmp/elephant.sock`)".

7. Drift check against source — re-fetched
   `…/elephant/v2.22.1/internal/comm/comm.go`, `200`,
   `sha256 2b4a6f1493be9d4cc453adcc8f26f8488d360679ab8d4342ea6bf4c0edd16e54`
   (equal to row S081's anchor), lines 40-44: unset `XDG_RUNTIME_DIR` →
   `filepath.Join(os.TempDir(), "elephant", "elephant.sock")`, else
   `filepath.Join(rd, "elephant", "elephant.sock")`.

## Findings

**F1 — pin.** The URL is tag-pinned: the ref segment `v2.22.1` is a lightweight
tag at `8f1e21d6…`, no branch of that name exists, and the raw bytes at the tag
are identical to the raw bytes at that commit. `[OBS]`

**F2 — digest.** My independent fetch is 6,969 B / 278 lines / `aa19a7e2…`,
exactly the row's anchor cell and every receipt for the URL (3 wave-1 seats +
2 later). `[OBS]` This is the R17-V3 shape the round declared: a closure can
re-fetch and re-hash without trusting the author.

**F3 — anchors.** All four cited anchor groups exist and say what the scope
claims: usage (123-141: environment warning, service management, `--config`),
one more usage line (166 `listproviders`), the configuration-directory tree and
`generatedoc` (181-192), the socket note (211). No cited line is empty or
off-topic. `[OBS]`

**F4 — kind/tier/scope.** `kind=docs` fits: the source is the project's own
README, i.e. documentation of its CLI/config surface, not code. `tier=A` fits
the row's scope because the source is the first-party upstream document at a
release tag — a primary source for *documented* usage/config/service/socket
text (the row makes no binary-behaviour claim). The P3 surface keyword is
present in **both** the source cell (`elephant`) and the scope cell
(`elephant usage …`), satisfying rubric V's T4 test in
`.ufo/waves/round-17/measure.py:250-259` (kind in docs/spec/code, `https://`
in source, keyword in source+scope). `[OBS]`

**F5 — teaches grounded.** Each clause is backed: config layout at lines
186-189; `--config` at 141; and the "stale against source" clause is true and
in fact understated — the source uses `$XDG_RUNTIME_DIR/elephant/elephant.sock`,
and even the unset-variable fallback builds `os.TempDir()/elephant/elephant.sock`
(`/tmp/elephant/elephant.sock`), not the README's `/tmp/elephant.sock`. `[OBS]`
The clause is a cross-row synthesis (needs S081's bytes); the row does not cite
S081 in-cell, but the citing note attaches `[EC:…]` at the claim, so the trail
is recoverable. `[INF]`

**F6 — note use truthful.** `walker-route-r18.md` cites `ER:` only at 123,
140-141, 177-178+129, 183-189, 192-194 and 211. Every one maps onto a line I
read, each quotation is a substring of the body, and the note's stronger claims
about elephant source are carried by `EC`/`ED`/`EG`, not by `ER`. Its one
`[UNK]` about the README socket line ("whether it describes any build or
environment where XDG_RUNTIME_DIR is unset") is conservative, not false — the
fallback path differs from the README string too, which the note does not
assert. The head line `source:` declares S080 at the same URL with
"(Usage, Configuration)", matching the row. `[OBS]`

**No defect found.** The only residual risks are methodological, listed below;
none makes the row false, invented, or miscredited.

## Residual unknowns

- GitHub contents-API blob identity (`29d94a6b…`) unconfirmed — 403 rate
  limit; the commit-sha raw fetch is the pin oracle used instead. `[UNK]`
- Whether the host `/usr/bin/elephant` build matches the tag: not read (no
  binary or package query; out of S080's scope; S090 covers version by log
  line only). `[UNK]`
- Upstream may force-move the tag after this check; the row's `on-release`
  recheck is the right guard, not this report. `[INF]`
- `slog` message at comm.go:41 says "falling back to /tmp" while the code
  builds `/tmp/elephant/elephant.sock`; log wording vs path is source-internal.
  `[OBS]`

GATE | S080 | https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS080/elephant-v2.22.1-readme.md:211 "Connect to the Unix socket (typically at `/tmp/elephant.sock`)" (8 words) | aa19a7e2d1c07bf1852b65fd38ca24a6b04bba0dacfd9f6cb02ada0ee0b61389 | agree: sha256 equals the row anchor and all 5 receipts; lightweight tag v2.22.1 = 8f1e21d6 with no same-name branch, and the same bytes serve at that commit; cited lines 123-141/166/181-192/211 exist and match scope and teaches; the note's ER anchors are truthful.
