# S089 — non-author re-open (round 18, wave 2 / FALSIFY)

Seat: MadoR18.ReopenS089. Read-only check of one newly credited SOURCES row
(R17-V3 receipt requirement). Baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`,
integration `4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts commit
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. No lane write outside
`.ufo/waves/round-18/fetch/ReopenS089/` and this report; no tool installed or
upgraded; no package/service/compositor/process/socket command.

## Row under test (bytes re-read at `4c103b55`)

`git show 4c103b55:corpus/SOURCES.md | grep '^| S089 '` returns exactly the
row quoted in the ticket; `git diff --stat 4c103b55 -- corpus/SOURCES.md
corpus/knowledge/walker-route-r18.md` is empty and the working-tree note
sha256 (`3ff430a4…`) equals the committed one. The row parses to 13 cells
(11 columns), id unique (`grep -c '^| S0'` counts one `^| S089`).

## Commands run and their output

Tag resolution (`git ls-remote https://github.com/basecamp/omarchy
'refs/tags/v3.8.4' 'refs/heads/v3.8.4' 'refs/tags/v3.8.4^{}'`):

```
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
```

One line only: no `^{}` peel line, no `refs/heads/v3.8.4`. So the path ref is
a **lightweight tag** and the name is unambiguous (no branch shadowing it).
Saved as `.ufo/waves/round-18/fetch/ReopenS089/git-ls-remote-v3.8.4.txt`
(command output, not a curl fetch, hence no receipt).

Fetches (`curl -sSL --max-time 60 -o BODY -w '%{http_code} %{url_effective}'`,
curl 8.23.0), receipts in `.ufo/waves/round-18/fetch/ReopenS089/receipts.jsonl`:

| body | URL form | status | bytes | sha256 |
|---|---|---|---|---|
| `omarchy-v3.8.4-default-walker-walker.desktop` | raw tag `…/v3.8.4/default/walker/walker.desktop` | 200 (final URL identical) | 138 | `5cb9874e…` |
| `omarchy-v3.8.4-default-walker-restart.conf` | raw tag `…/v3.8.4/default/walker/restart.conf` | 200 (identical) | 38 | `de0f7029…` |
| `commit-8fcc9d60-walker-walker.desktop` | raw **commit** `8fcc9d60…` | 200 (identical) | 138 | `5cb9874e…` |
| `commit-8fcc9d60-walker-restart.conf` | raw **commit** `8fcc9d60…` | 200 (identical) | 38 | `de0f7029…` |
| `github-redirect-walker.desktop` | `github.com/…/raw/v3.8.4/…` | 200, final URL `raw.githubusercontent.com/omacom/omarchy/…` | 138 | `5cb9874e…` |

Bodies, `cat -n`:

- `walker.desktop` (138 B, 7 lines): `[Desktop Entry]` / `Name=Walker` /
  `Comment=Walker Service` / `Exec=walker --gapplication-service` /
  `StartupNotify=false` / `Terminal=false` / `Type=Application`.
- `restart.conf` (38 B, 3 lines): `[Service]` / `Restart=always` /
  `RestartSec=2`.

Host installed copies, read as bytes only (`stat -c '%n %s'`, `sha256sum`):

```
/home/vgpnk/.config/autostart/walker.desktop 138
5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7
/home/vgpnk/.config/systemd/user/app-walker@autostart.service.d/restart.conf 38
de0f70294000bc29f5876ea195db127f74060ac990aad5a129eeb72c98b15433
```

Receipt sweep across every seat (`fetch-verify.py`, whole fetch root):
`SUMMARY receipts=361 ok=361 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=0`,
`ROW S089 receipted`, `QUOTE S089 ok`, exit 0.

## SHA agreement

Every receipt in the tree for these two files — 11 lines across four seats —
carries the row's digests, and so do my independent fetches at both the tag
name and the raw commit:

| seat | when (UTC) | walker.desktop | restart.conf |
|---|---|---|---|
| NoteWalker (wave 1) | 15:40:37 / 15:40:36 | `5cb9874e…` 138 B | `de0f7029…` 38 B |
| SrcOmarchyWalker (wave 1) | 15:40:49 / 15:40:48 | `5cb9874e…` 138 B (github-raw form) | `de0f7029…` 38 B |
| ReopenS089 (this seat) | 15:59:53–16:00:33 | `5cb9874e…` 138 B (tag, commit, redirect) | `de0f7029…` 38 B (tag, commit) |
| ReviewWalkerUpstream (w2) | 16:00:36 | `5cb9874e…` 138 B | `de0f7029…` 38 B |

Confirmed against the row's anchor cell: `walker.desktop` 138 B
`5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7`, `restart.conf`
38 B `de0f70294000bc29f5876ea195db127f74060ac990aad5a129eeb72c98b15433` —
identical. No receipt anywhere records a differing digest for either file.

**Tag-pinned?** Yes, in the round's sense: the URL path names `refs/tags/v3.8.4`
(not a branch), the tag is lightweight and resolves to
`8fcc9d6048af4cb0e3af8512c78049857a3b53dd`, and the files fetched by commit sha
return the same bytes, so a closure can re-check against an immutable object.
A tag name remains re-pointable by the repository owner; only the commit-sha URL
is inherently immutable. Side fact, observed: `github.com/basecamp/omarchy` is an
alias — GitHub's raw path redirects to `raw.githubusercontent.com/omacom/omarchy/…`
(the API ref body in `.ufo/…/fetch/MadoR18.HostOmarchyCheckoutTag/gh-ref-tags-v3.8.4.json`
names `refs/tags/v3.8.4 → 8fcc9d60…`, `object.type: commit`).

## Judgement

- **kind `code`** — two repository artifacts (a `.desktop` entry and a systemd
  drop-in) shipped in the upstream tree. The enum has no "config"; `code` is the
  honest slot and is one the instrument admits for upstream credit. Acceptable.
- **tier `A`** — primary for the scoped claim "shipped by omarchy at tag v3.8.4":
  the bytes *are* the artifact, fetched at a pinned tag. SOURCES contract A
  explicitly includes "source code"; not inflated, and the scope is tight
  (it does not claim host packaging or runtime state).
- **scope** — "autostart entry and restart drop-in shipped by omarchy at tag
  v3.8.4". The scope cell itself does not carry the P3 keyword, but the source
  cell does (`omarchy default **walker** autostart … /walker/walker.desktop`),
  which satisfies rubric V's "source **or** scope cell" rule. Scope is accurate
  for both files; the autostart characterization is carried by
  `omarchy-refresh-walker:6`, `cp $OMARCHY_PATH/default/walker/walker.desktop
  ~/.config/autostart/` (body already in `fetch/NoteWalker/`), not by the
  `.desktop` body alone.
- **teaches grounded?** Clause 1 `Exec=walker --gapplication-service` is
  `walker.desktop:4` verbatim; "at login" is a two-file inference (the drop-in
  placement into `~/.config/autostart/`) and is supported. Clause 2 "restart
  drop-in equal to host copy" is true as read today: tag body and host
  `~/.config/systemd/user/app-walker@autostart.service.d/restart.conf` are both
  38 B / `de0f7029…`. Grounded.
- **Citing note truthful?** `corpus/knowledge/walker-route-r18.md:169`
  "Autostart entry: `Exec=walker --gapplication-service` [OD:4]" — exact.
  Anchor key `OD` (line 36) names both files. Host table rows for the autostart
  entry and the drop-in carry the digests I re-measured. § Omarchy launch
  describes `omarchy-refresh-walker` as copying both files [OF:5-10] and
  refreshing `walker/config.toml` plus two elephant files [OF:15-17] — the body
  does exactly that (copies at 5-6 and 9-10; refreshes at 15-17; lua links at
  20-23; restart at 26). The note stays inside "documentary route only" and
  claims no running launcher. Truthful; no overreach found.

## Residual gaps (minor, none fatal)

1. The anchor cell names `restart.conf` with bytes and digest but gives it no
   URL or line anchor of its own; it is the sibling path of the source URL.
   Reproducible by derivation, not by quotation.
2. Teach-clause 2 ("equal to host copy") is a host-file fact, but the row's
   anchor cell carries no host path; the note's Host declaration does.
3. SOURCES contract rule 1 asks the round lesson's `## Gate` to record URL,
   access date and a ≤25-word located quote per new row. At `4c103b55` the Gate
   instead says quotes are "recorded below after the wave-2 re-open" and no
   quote block exists yet. This report supplies S089's line; the Gate table is
   still owed by the integration seat.

GATE | S089 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/walker/walker.desktop | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS089/omarchy-v3.8.4-default-walker-walker.desktop:4 "Exec=walker --gapplication-service" (2 words) | 5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7 | agree: independent 138-byte fetch (tag, commit 8fcc9d60, and github-raw redirect) reproduces the anchor digest and both files' digests match all 11 wave-1/wave-2 receipts; lightweight tag v3.8.4 is unambiguous and the commit-pinned URL returns identical bytes; kind code / tier A / scope hold, teaches is verbatim-grounded, and the note's OD:4 citation plus host-equal drop-in are true
