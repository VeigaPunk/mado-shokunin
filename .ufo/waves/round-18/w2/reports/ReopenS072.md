# ReopenS072 — non-author re-open of SOURCES S072 (walker README @ v2.17.2)

Seat: `MadoR18.ReopenS072`, wave 2 (FALSIFY), 2026-10-20. Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Read-only: no git/jj write in the
lane, no package/compositor/service/process command. Only `curl`, read-only
`git ls-remote`, `sha256sum`, `sed`, `grep`, `nl` and `python3` (JSON parse)
were used.

## Row under test

`corpus/SOURCES.md:84` at `4c103b55` (row text identical to the worktree; one
`| S072 |` line at that revision, 13 pipe fields = 11 contract columns):

```
| S072 | walker README @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md | docs | A | walker dependency on elephant, service mode, socket call, config directory at tag v2.17.2 | file lines 3, 59, 167-185, 211-215; sha256 9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456 | elephant must run first; `--gapplication-service` is the fast path; the raw socket call ignores CLI options; config belongs in ~/.config/walker | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
```

The row lists exactly one file (the README itself); its source and anchor
cells name no further upstream file, so the "up to three further files" leg
of the item is empty.

## Independent fetch (observed)

```
mkdir -p .ufo/waves/round-18/fetch/ReopenS072
curl -sSL --max-time 60 -o <seat>/walker-v2.17.2-README.md \
  -w '%{http_code} %{url_effective}' \
  https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md
→ 200 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md

sha256sum …/walker-v2.17.2-README.md
→ 9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456
wc -c → 7926
```

The fresh body sha256 **equals the row's anchor sha256 exactly** and the byte
count is 7,926 B. Receipt appended at
`.ufo/waves/round-18/fetch/ReopenS072/receipts.jsonl` (`mado-fetch-receipt-v1`,
`fetched_at` 2026-10-20T16:00:01Z, `tool` = `curl 8.23.0 …`).

## Tag resolution (observed)

```
git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 refs/tags/v2.17.2^{}
→ a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2
   (no `^{}` peeled line → lightweight tag)

git ls-remote … refs/heads/v2.17.2 'refs/heads/v2.17*'
→ (empty)                    # no branch shadows the tag name

git ls-remote … refs/heads/master
→ a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/heads/master
```

- **The URL is tag-pinned, not commit-pinned.** The path segment `v2.17.2` is
  a tag ref resolving to `a515085f…`; `v2.17.2` is a **lightweight** (mutable)
  tag, so the URL is reproducible only while upstream does not force-move it.
  The row's digest makes any such move detectable on re-fetch.
- **Falsification result — the pin is not differentiated today.** `refs/heads/master`
  currently points at the *same* commit `a515085f…`, and a control fetch of
  `…/walker/master/README.md` returns byte-identical content (sha256
  `9755f955…d2456`, 7,926 B, `diff -q` rc 0; receipted as
  `master-README.md`). So today the digest proves the row's bytes but cannot by
  itself distinguish tag content from default-branch content. This does not
  falsify the row (it claims the tag, and the tag resolves), but a re-open that
  cites "tag-pinned" must not claim the digest discriminates the tag — only the
  ref path does. The pin remains meaningful over time: a later master move
  leaves the tag URL unchanged.

## Wave-1 receipts for the same URL (observed)

`grep -rn 'abenz1267/walker/v2.17.2/README.md' .ufo/waves/round-18/fetch/*/receipts.jsonl`
→ seven wave-1 receipts, all identical in digest and size; every named body
file still hashes to the receipt value:

| seat | fetched_at (UTC) | bytes | sha256 | body file | body re-hash |
|---|---|---|---|---|---|
| `SrcWalkerReadme` | 2026-10-20T15:40:04Z | 7,926 | 9755f955…d2456 | `walker-readme` | equal |
| `NoteWalker` | 2026-10-20T15:40:36Z | 7,926 | 9755f955…d2456 | `walker-v2.17.2-readme.md` | equal |
| `MadoR18.SrcWalkerThemes` | 2026-10-20T15:40:39Z | 7,926 | 9755f955…d2456 | `readme-md.txt` | equal |
| `SrcWalkerDefaultConfig` | 2026-10-20T15:40:51Z | 7,926 | 9755f955…d2456 | `walker-v2.17.2-README.md` | equal |
| `SrcWalkerChangelog` | 2026-10-20T15:41:42Z | 7,926 | 9755f955…d2456 | `walker-v2.17.2-README.md` | equal |
| `SrcElephantReadme` | 2026-10-20T15:42:29Z | 7,926 | 9755f955…d2456 | `walker-README.md.body` | equal |
| `SrcWalkerDocsSite` | 2026-10-20T15:43:12Z | 7,926 | 9755f955…d2456 | `readme-v2.17.2.md` | equal |

No wave-1 receipt for this URL carries a divergent digest, byte count or missing
body. Two wave-2 fetches are independent corroboration (this seat 16:00:01Z;
sibling `ReviewWalkerUpstream` 16:00:36Z, also `9755f955…`, body 7,926 B).

## Row judgement against body bytes

Anchor ranges verified line-exact (`nl -ba`, 233-line body):

- **3** — `A fast, customizable application launcher built with GTK4 and Rust, …`
- **59** — `- make sure [elephant](https://github.com/abenz1267/elephant) is running before starting Walker`
- **167-185** — `In order to improve startup performance, run a Walker service with:`
  / `walker --gapplication-service` (170) / `walker` (176) / socket example
  `nc -U /run/user/1000/walker/walker.sock` (182) / the "does not handle any
  commandline options" downside (185)
- **211-215** — `## Config` (211), `Configuration should be done in
  \`~/.config/walker\`.` (213), default-config link (215)

Cell verdicts:

- **kind `docs`** — correct: the upstream project's own README, not code or a
  third-party restatement.
- **tier `A`** — justified for this scope: primary source (the project document
  at its own release tag), content-addressed by sha256 in the row; same tier
  convention as the registry's other tag READMEs (S065, S069).
- **scope / surface keyword** — all four scope nouns are literal features of
  the anchor ranges (elephant dependency 59/163, service mode 167-171, socket
  call 179-185, config directory 213). The source cell says `walker` and the
  scope cell says `walker … elephant`, so rubric V's P3 keyword test (`walker`,
  `elephant`) is met twice over. No P5 keyword is claimed or needed.
- **`teaches`** — each clause is directly observed: "elephant must run first"
  is README:59 (and :163); "`--gapplication-service` is the fast path" is
  README:167-170 ("In order to improve startup performance"); "the raw socket
  call ignores CLI options" is README:185 ("does not handle any commandline
  options") — a fair paraphrase of the README's own words, not a widening;
  "config belongs in ~/.config/walker" is README:213. No forward projection to
  the host binary.
- **status / dates / used-by** — `mined`, opened 2026-10-20, used-by
  `corpus/knowledge/walker-route-r18.md`; the note exists at the integration
  commit and cites S072. `recheck on-change` is stricter than the sibling
  tag rows' `on-release` (S073–S089); a cosmetic inconsistency, not a false
  statement (a force-moved tag would be a change).

## Citing-note truthfulness (`corpus/knowledge/walker-route-r18.md`)

Note bytes at `4c103b55` hash `3ff430a4…fbf20`, identical to the worktree. All
seven `WR:` citations were checked against the body line by line:

- `[WR:3]` "built with GTK4 and Rust" — exact substring of line 3. True.
- `[WR:59]` "make sure elephant is running before starting Walker" — true of
  the *rendered* line; the byte line carries the `[elephant](https://…)` link
  markup between the words, so it is not a byte-exact substring. Cosmetic only:
  the cited line is the elephant dependency line and the words are unchanged.
- `[WR:167-171]` service mode — true (167 heading sentence, 170 command).
- `[WR:173-177]` plain `walker` — true; `[WR:179-182]` "for an even faster
  launch" — exact substring of 179; `[WR:185]` "it does not handle any
  commandline options" — exact substring of 185.
- `[WR:213]` "Configuration should be done in `~/.config/walker`." — exact.
  `[WR:215]` "the default config is linked" — true, and the note does not call
  that link pinned; **caveat for readers**: the link targets
  `refs/heads/master/resources/config.toml`, a mutable ref, so S072 cannot pin
  default-config bytes (S073 does, and its digest matches).
- The note's opening `source:` names S072 with the section labels
  "(Dependencies, Usage, Config)" — those headings exist (52, 158, 211). The
  note's provenance line claims every raw body is receipted in
  `NoteWalker/receipts.jsonl`; all 18 URLs cited in the note head do appear
  there (27 receipt lines, 18/18 cited URLs matched).
- No statement attributed to WR exceeds the README: source-side facts
  (dmenu check, `--close`, exit codes) are correctly carried by `WM:`/`WS:`
  rows, and the note marks inference (`INF`) and unknowns (`[UNK]`) where the
  README is silent.

## Confidence

- Digest/anchor identity and receipt agreement: **high** (byte re-fetch; 7/7
  wave-1 bodies re-hashed equal; 2 independent wave-2 fetches equal).
- Row accuracy (kind/tier/scope/teaches): **high** — every clause reproduced at
  the cited lines.
- Note truthfulness for WR claims: **high**; one quote (line 59) is
  rendered-text rather than byte-exact, a presentation nit.
- Tag-pin meaning: **high** on resolution; the digest's discriminating power is
  **null today** because master == `a515085f…`.

## Remaining unknowns

- Whether upstream ever force-moves the lightweight `v2.17.2` tag (only a future
  re-fetch can tell; the row digest makes it detectable).
- Whether a future master advance changes the README (today it cannot be told
  apart from the tag copy).
- Whether the host `/usr/bin/walker` (2.17.2-1 per the S090/S091 rows) is a
  faithful build of the tag — not this row's scope and still `[UNK]`.
- Host runtime behaviour remains unobserved: no walker/elephant process, socket
  or service was touched, per host pause.

GATE | S072 | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS072/walker-v2.17.2-README.md:185 "The downside of the socket call is that it does not handle any commandline options" (15 words) | 9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456 | agree: fresh 200 body sha256 equals the row anchor and all seven wave-1 receipts (7/7 bodies re-hash equal, 7,926 B); refs/tags/v2.17.2 is a lightweight tag at a515085f with no shadowing branch, so the URL is tag-pinned though master currently equals the same commit; kind docs/tier A/scope keyword walker+elephant/teaches all hold and the note's seven WR: citations are line-accurate (line 59 quoted from rendered text, not byte-exact; line 215's default-config link is master, which the row does not claim to pin)
