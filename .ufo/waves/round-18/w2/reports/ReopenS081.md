# ReopenS081 — non-author re-open of SOURCES row S081 (round 18, w2 falsify)

Seat: `MadoR18.ReopenS081`. Assignment: re-open row S081 as a non-author
(R17-V3), independently re-fetch
`https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/internal/comm/comm.go`,
join its sha256 against the anchor cell and every wave-1 receipt for the same
URL, resolve the tag with `git ls-remote`, judge kind/tier/scope/`teaches`, and
check the citing note `corpus/knowledge/walker-route-r18.md` for truthful use.

Revision graded: the row and note as committed at
`4c103b55b1ea5c3c555884afe3eb69b5189701b7` (lane branch `master`; current lane
HEAD `abfbf35`). Worktree bytes are identical to that commit for both files:
`corpus/SOURCES.md` = `9552071c…` at HEAD and at `4c103b5`; note =
`3ff430a4…` at both. Row text read from `git show 4c103b5:corpus/SOURCES.md`
line 93.

Method: `curl` fetches with a receipt each, `sha256sum`, `wc -c`, `cmp`, line
reads, one `git ls-remote`, read-only `git show`/`rev-parse`. No package
manager, sudo, service, socket, walker/elephant execution, or host binary was
touched. No tool was installed or upgraded. No subagent was dispatched.

## 1. Exact commands and observed output

```
$ git ls-remote --tags https://github.com/abenz1267/elephant.git 'refs/tags/v2.22.1*'
8f1e21d6efe40b8b3953f95b9574f99f717caf91	refs/tags/v2.22.1
```
Single line, no `^{}` peeled line → lightweight tag pointing directly at
`8f1e21d6…`. The row URL's path segment is `v2.22.1`, i.e. the URL is
**tag-pinned by name** (not branch, not commit). Lightweight tags are movable,
so the name alone is not a byte guarantee; the sha256 anchor plus the
commit-pinned fetch below give content reproducibility.

```
$ curl -sSL --max-time 60 -o comm.go.body -w '%{http_code} %{url_effective}' \
    https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/internal/comm/comm.go
200 https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/internal/comm/comm.go
$ wc -c comm.go.body
2552 comm.go.body
$ sha256sum comm.go.body
2b4a6f1493be9d4cc453adcc8f26f8488d360679ab8d4342ea6bf4c0edd16e54  comm.go.body

$ curl -sSL --max-time 60 -o comm.go.at-commit.body -w '%{http_code} %{url_effective}' \
    https://raw.githubusercontent.com/abenz1267/elephant/8f1e21d6efe40b8b3953f95b9574f99f717caf91/internal/comm/comm.go
200 https://raw.githubusercontent.com/abenz1267/elephant/8f1e21d6efe40b8b3953f95b9574f99f717caf91/internal/comm/comm.go
$ sha256sum comm.go.at-commit.body
2b4a6f1493be9d4cc453adcc8f26f8488d360679ab8d4342ea6bf4c0edd16e54  comm.go.at-commit.body
$ cmp comm.go.body comm.go.at-commit.body && echo IDENTICAL_BYTES
IDENTICAL_BYTES
```
Both fetches are receipted in
`.ufo/waves/round-18/fetch/MadoR18.ReopenS081/receipts.jsonl` (schema
`mado-fetch-receipt-v1`, 200, 2552 B, same digest, bodies `comm.go.body` and
`comm.go.at-commit.body`).

Wave-1 receipts for the same URL (all `mado-fetch-receipt-v1`, all HTTP 200,
all 2552 B):

| seat | url form | sha256 |
|---|---|---|
| `NoteWalker` | `.../elephant/v2.22.1/internal/comm/comm.go` | `2b4a6f14…16e54` |
| `SrcElephantProviders` | `.../elephant/v2.22.1/internal/comm/comm.go` | `2b4a6f14…16e54` |
| `SrcElephantReadme` | `.../elephant/8f1e21d6…/internal/comm/comm.go` | `2b4a6f14…16e54` |

`grep -h 'comm/comm.go' .ufo/waves/round-18/fetch/*/receipts.jsonl | grep -o
'"sha256": *"[^"]*"' | sort | uniq -c` → exactly one digest, three lines. The
stored wave-1 bodies re-hash to the same value:
`NoteWalker/elephant-v2.22.1-internal-comm-comm.go`,
`SrcElephantProviders/comm-comm.go`, `SrcElephantReadme/elephant-comm.go.body`
→ all `2b4a6f14…16e54`.

Row anchor cell digest: `2b4a6f1493be9d4cc453adcc8f26f8488d360679ab8d4342ea6bf4c0edd16e54`
(64 hex chars). **Anchor = all three wave-1 receipts = both of my fetches.**

## 2. Body lines the row anchors, read

`comm.go.body` is 129 lines, complete (package clause at 1, closing of
`handle` at end). Lines 37–47 and 58–62 as fetched:

```
37  func init() {
38      rd := os.Getenv("XDG_RUNTIME_DIR")
39
40      if rd == "" {
41          slog.Error("socket", "runtimedir", "XDG_RUNTIME_DIR not set. falling back to /tmp")
42          Socket = filepath.Join(os.TempDir(), "elephant", "elephant.sock")
43      } else {
44          Socket = filepath.Join(rd, "elephant", "elephant.sock")
45      }
46
47      os.MkdirAll(filepath.Dir(Socket), 0o755)
...
58  func StartListen() {
59      os.Remove(Socket)
60
61      l, err := net.ListenUnix("unix", &net.UnixAddr{
62          Name: Socket,
```

- The anchor range 37–47 is exactly the socket-path/fallback block.
- The anchor range 58–62 is exactly `StartListen` removing a stale socket and
  naming `Socket` in `net.ListenUnix` — i.e. the listening path, not a second
  path.
- No further files are listed in the row's source or anchor cells, so the
  "re-fetch up to three more" branch does not apply.

## 3. Row judgment

| facet | judgment | basis |
|---|---|---|
| kind = `code` | correct | upstream Go source, not docs or host bytes |
| tier = `A` | correct for this scope | primary upstream bytes at the tag: raw tag URL and raw commit URL agree byte-for-byte; tag resolves to `8f1e21d6…` by `git ls-remote`; the note's `verified-at` line records the same commit |
| scope cell | names its surface keyword | "elephant listening socket path and fallback at tag v2.22.1" — `elephant` present (P3 requires walker/elephant) and the scope is version-bounded |
| anchor cell | reproduces | lines 37–47 and 58–62 are the claimed block; full 64-hex sha256 matches the fetched body |
| `teaches` grounded | yes, with one compression | "socket is $XDG_RUNTIME_DIR/elephant/elephant.sock" = line 44 verbatim; "/tmp fallback is `os.TempDir()` with an error log" = lines 40–42, but the fallback *path* is `filepath.Join(os.TempDir(), "elephant", "elephant.sock")`, and `os.TempDir()` honours `TMPDIR`, so the log's literal "/tmp" is the message text, not a guarantee |
| status/opened/recheck/used-by | consistent | `mined` / `2026-10-20` / `on-release` / the note really cites `EC:` |

The teaches cell's "/tmp fallback is os.TempDir()" is a summary, not a false
statement: the base directory is `os.TempDir()`; the row's anchor lines carry
the exact join, and the note does not repeat the compression as a path.

## 4. Citing note — truthful use

`corpus/knowledge/walker-route-r18.md` line 30 defines `EC` as this file with
`EC:n` = file line; line 1's source list says S081 = this URL "(init,
StartListen)". Every EC citation checked against the fetched body:

- line 130 `filepath.Join(rd, "elephant", "elephant.sock")` `[EC:38-44]` —
  line 44, exact; 38–44 covers the `Getenv` and both branches.
- line 131 "creating the parent directory with mode 0755" `[EC:47]` —
  `os.MkdirAll(filepath.Dir(Socket), 0o755)`, exact.
- line 132 `"XDG_RUNTIME_DIR not set. falling back to /tmp"` and
  `os.TempDir()` `[EC:40-42]` — the string is verbatim at line 41 (slog
  attribute value) and `os.TempDir()` at line 42, exact.
- line 133–135 drift sentence: "The v2.22.1 source does not use
  `/tmp/elephant.sock` on the XDG path" — true; line 44 is the XDG branch and
  the fallback branch is `os.TempDir()/elephant/elephant.sock`, also not
  `/tmp/elephant.sock`.
- line 313–315 `[UNK]`: "only the source fallback `os.TempDir()` (`EC:42`) was
  read" — accurate self-limit; it does not claim the README's literal path was
  reproduced.

No citation embellishes the source; the note does not present S081 as host
observation, and its front-matter `read, not observed` stance holds. Minor
omission only: the note never spells out the fallback's joined
`elephant/elephant.sock` suffix, so a reader could over-read "os.TempDir()";
this is an omission, not an error, and the [UNK] at 313–315 already refuses
the README's `/tmp/elephant.sock` equivalence.

## 5. Residual unknowns

- `[UNK]` Whether `refs/tags/v2.22.1` still points at `8f1e21d6…` at any later
  time; lightweight tags can be retargeted. Mitigated by the sha256 anchor and
  the byte-identical commit-pinned fetch, both at fetch time.
- `[UNK]` The host `/usr/bin/elephant` binary's embedded path constant: this
  row is documentary source, not host fact; no binary was opened.
- `[INF]` GitHub's raw tag endpoint served the same bytes as the raw commit
  endpoint in the two fetches above; that is observed here (and in wave 1 by
  `SrcElephantReadme`), not a protocol guarantee.

GATE | S081 | https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/internal/comm/comm.go | 2026-10-20 | .ufo/waves/round-18/fetch/MadoR18.ReopenS081/comm.go.body:44 "Socket = filepath.Join(rd, "elephant", "elephant.sock")" (5 words) | 2b4a6f1493be9d4cc453adcc8f26f8488d360679ab8d4342ea6bf4c0edd16e54 | agree: tag-pinned (lightweight v2.22.1 = 8f1e21d6) bytes reproduce the anchor digest and all three wave-1 receipts, and lines 37-47/58-62 ground the teaches cell; only compression is that the fallback path also joins "elephant/elephant.sock" under os.TempDir()
