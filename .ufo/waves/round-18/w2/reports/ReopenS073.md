# Re-open S073 — non-author check (R17-V3)

Seat: MadoR18.ReopenS073. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Row under test: `corpus/SOURCES.md:85` (S073, walker `resources/config.toml` @ v2.17.2).
Everything below was fetched, hashed or read as bytes by this seat; nothing in
the target tree was executed.

## Verdict

**agree.** An independent fetch reproduces the anchor sha256 byte-for-byte
(13,743 B), the URL is tag-pinned (`v2.17.2` is a ref name, lightweight tag
`a515085f…`), all seven receipts naming the exact URL — five wave-1 seats, one
wave-2 peer, and this seat — agree on 200 / 13,743 B / `3c5c6867…`, every saved
body re-hashes to that digest, and the host `/etc/xdg` copy is byte-equal. Every
`teaches` clause and every `WC:` citation in the citing note reproduces from the
file. Two wording nits are recorded below; neither changes a claim.

## Independent fetch and hash

Command (per fetch rules, receipted in
`.ufo/waves/round-18/fetch/ReopenS073/receipts.jsonl`):

    curl -sSL --max-time 60 -o walker-config.toml \
      -w '%{http_code} %{url_effective}\n' \
      https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml

Result: `200 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml`,
13,743 bytes (`wc -c`), sha256
`3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`, 305 lines.
No auth, cookie or header was sent; one `mado-fetch-receipt-v1` line appended.

| comparison | value | verdict |
|---|---|---|
| row anchor cell (`SOURCES.md:85`) | `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`, 13,743 B | equal |
| `fetch/SrcWalkerDefaultConfig/receipts.jsonl:1` | 200, 13,743 B, `3c5c6867…`, body `walker-v2.17.2-config.toml`, 15:40:26Z | equal; saved body re-hashed here = `3c5c6867…`, byte-equal |
| `fetch/SrcWalkerReadme/receipts.jsonl:2` | 200, 13,743 B, `3c5c6867…`, body `walker-config-toml`, 15:40:15Z | equal; body re-hashed and byte-equal |
| `fetch/NoteWalker/receipts.jsonl:3` | 200, 13,743 B, `3c5c6867…`, body `walker-v2.17.2-resources-config.toml`, 15:40:36Z | equal; body re-hashed and byte-equal |
| `fetch/MadoR18.SrcWalkerThemes/receipts.jsonl:10` | 200, 13,743 B, `3c5c6867…`, body `walker-config-toml.txt`, 15:41:16Z | equal; body re-hashed and byte-equal |
| `fetch/SrcWalkerChangelog/receipts.jsonl:5` | 200, 13,743 B, `3c5c6867…`, body `walker-v2.17.2-resources-config.toml`, 15:41:42Z | equal; body re-hashed and byte-equal |
| `fetch/ReviewWalkerUpstream/receipts.jsonl:2` (wave-2 peer) | 200, 13,743 B, `3c5c6867…`, body `walker-2.17.2-config-default.toml`, 16:00:36Z | equal; body re-hashed and byte-equal |
| `fetch/ReopenS073/receipts.jsonl:1` (this seat) | 200, 13,743 B, `3c5c6867…`, body `walker-config.toml`, 16:00:01Z | equal |

Census method: parsed every `.ufo/waves/round-18/fetch/*/receipts.jsonl`, selected
`url ==` the exact row URL, re-hashed each `body` file beside its receipt and
byte-compared it with this seat's fetch. Seven matching lines, one distinct
digest, one distinct byte count; no disagreeing or non-200 receipt exists.
`NoteWalker`'s neighbouring receipts for `v2.17.0` (13,220 B,
`5b4e47b7…`) and `v2.17.1` (13,731 B, `be6099be…`) cover different URLs and, if
anything, show the file changes between tags rather than tracking a branch.

## Tag pinning

    git ls-remote https://github.com/abenz1267/walker.git \
      refs/tags/v2.17.2 'refs/tags/v2.17.2^{}' 'refs/tags/v2.17.2*'

run from `/tmp` (read-only), returned exactly one line:

    a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2

No `^{}` peeled line, so `v2.17.2` is a lightweight tag. The URL's third path
segment is that tag name, so the URL **is tag-pinned**, not branch- or
`master`-tracking. Residual caveat: a lightweight tag is a movable server-side
ref; the digest anchor is the durable pin and the recorded commit
`a515085f…` is what a future re-open should still see. This matches
`walker-route-r18.md:7`.

## Line-level grounding (body anchors)

Body read: `.ufo/waves/round-18/fetch/ReopenS073/walker-config.toml` (305 lines).
The row's cited region is lines 1-113; every claim lies inside it, verbatim:

- `:2` `close_when_open = true`; `:4` `as_window = false`; `:6`
  `selection_wrap = false`; `:9` `theme = "default"`; `:18`
  `resume_last_query = false`.
- `:37-38` `[columns]` / `"symbols" = 3`.
- `:58-66` `[providers]` with `default = ["desktopapplications", "calc",
  # "runner", "websearch"]`, `empty`, `ignore_preview`.
- `:67` `max_results = 50 # global max results`.
- `:75-113` ten `[[providers.prefixes]]` tables: `;`→providerlist,
  `>`→runner, `/`→files, `.`→symbols, `!`→todo, `%`→bookmarks, `=`→calc,
  `@`→websearch, `:`→clipboard, `$`→windows.
- No duplicate top-level `theme`/`close_when_open`/`max_results` key exists
  later in the file (the second `resume_last_query`, `:52`, is inside
  `[keybinds]` as a keybind array, a different table). Nothing after `:113`
  contradicts the cited defaults.

Host byte comparison (read-only): `sha256sum /etc/xdg/walker/config.toml` →
`3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`;
`wc -lc` → `305 13743`. Byte-equal to the fetched body.

## Row judgement (kind / tier / scope / teaches)

- **kind `code`** — a packaged TOML config (repo data table), not prose. Fits
  the rubric's accepted upstream kinds (`docs/spec/code`) and matches the
  registry's precedent for the same file class (`S085`, omarchy walker
  `config.toml`, kind `code`). No issue.
- **tier A** — the source is the upstream project's own file at a tag ref, i.e.
  primary for the stated scope ("walker packaged default config table at tag
  v2.17.2"). No projection onto `/usr/bin/walker` or Arch patch level.
- **scope** — names the surface keyword `walker` (P3) and is finite to the
  tag's default table plus the observed byte-equality of the host copy. Width
  is correct: it does not claim runtime behaviour.
- **teaches** — grounded clause by clause (lines above). The final clause,
  "the file the host packages is this file", is verified only as byte-equality
  (`/etc/xdg` sha equal); *which package installed that path* is `[INF]` this
  round (package queries paused, no `pacman -Qo`). The anchor cell itself says
  "byte-equal to host /etc/xdg/walker/config.toml", so the row does not
  overclaim beyond the observed equality — a stricter wording would be
  "byte-identical to the host `/etc/xdg` copy".
- **anchor line range** — "file lines 1-113" is a read/citation range inside a
  305-line file, not a claim of file length; the sha256 pins all 13,743 bytes.
  Tightening to "lines 1-113 of 305" would remove the ambiguity; not a defect.
- **status/recheck/used-by** — `mined`, `on-release`, walker note: appropriate
  for a tag-anchored file, and `mined_a()` in `.ufo/waves/round-17/measure.py:128`
  resolves the row (status mined, tier A, used-by names the note); the note's
  head `source:` line cites S073, so rubric V's P3 credit is legitimate.

## Note truthfulness (`corpus/knowledge/walker-route-r18.md`)

- `:22` anchor table: "13,743 B, byte-equal to host `/etc/xdg` file" — verified.
- `:109-113` "Packaged default, upstream v2.17.2 (values read from `WC`)" — all
  six defaults and the ten-entry prefix table reproduce exactly, including every
  arrow mapping.
- `:198` "Its prefix table differs from upstream [WC:75-113]" — verified: the
  user file (`~/.config/walker/config.toml:23-45`, read as bytes) has six
  entries with different mappings (`/`→providerlist, `.`→files, `:`→symbols,
  `=`→calc, `@`→websearch, `$`→clipboard), so both count and mapping differ
  from upstream's ten.
- No statement attributes a runtime or host-binary fact to S073; the note keeps
  the binary identity and `/etc/xdg` reachability `[UNK]`.
- S073 is cited only by the walker note, consistent with `used-by`.

## Commands run (all read-only)

    mkdir -p .ufo/waves/round-18/fetch/ReopenS073
    curl -sSL --max-time 60 -o walker-config.toml -w '%{http_code} %{url_effective}\n' <raw URL>
    wc -lc / sha256sum on the fetched body
    git ls-remote https://github.com/abenz1267/walker.git refs/tags/v2.17.2 'refs/tags/v2.17.2^{}' 'refs/tags/v2.17.2*'   (cwd /tmp)
    sha256sum /etc/xdg/walker/config.toml; wc -lc /etc/xdg/walker/config.toml
    cat -n / sed -n on the fetched body (lines 1-120) and on ~/.config/walker/config.toml:20-50
    python3: parse all fetch/*/receipts.jsonl, select exact URL, re-hash bodies, byte-compare
    python3: json.loads on this seat's receipt line

No package, service, compositor, socket, browser, REA or input operation; no git
or jj write; no git command in the lane or in the omarchy checkout.

## Remaining unknowns

- `[UNK]` Whether the lightweight `v2.17.2` tag is ever force-moved upstream;
  the recorded commit `a515085fd39fae80acc086c8fbfd9b7771a9a11d` is the
  cross-check a re-open should re-run.
- `[UNK]` Which Arch package wrote `/etc/xdg/walker/config.toml` and whether
  Arch patches the installed copy: byte-equality is observed, package
  provenance is not (no package query permitted this round).
- `[UNK]` Whether the running walker reads `/etc/xdg` on this host: the note
  keeps this `[UNK]` (user file present); S073 claims only the file, not its
  runtime use.

GATE | S073 | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS073/walker-config.toml:67 "max_results = 50 # global max results" (7 words) | 3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b | agree: independent fetch reproduces the anchor digest (13,743 B, 305 lines); tag v2.17.2 is a lightweight tag at a515085f and all seven receipts for the URL agree; every cited default and prefix mapping, and the host /etc/xdg byte-equality, reproduce
