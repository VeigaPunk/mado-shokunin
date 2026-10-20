# ReopenS079 — non-author re-open of SOURCES row S079 (walker v2.17.2 tag tarball)

Seat: `MadoR18.ReopenS079` (leaf, wave 2 FALSIFY). Date 2026-10-20.
Instruments: `curl` 8.23.0, `git` (ls-remote/clone in `/tmp` only), `sha256sum`,
`diff -r`, `grep`, `tar`. No package manager, service, compositor, socket,
process or browser probe. No tool install or update.

Row: `corpus/SOURCES.md:91`. Citing note: `corpus/knowledge/walker-route-r18.md`
(declares `surface: P3`). Baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`;
integration commit `4c103b55b1ea5c3c555884afe3eb69b5189701b7`.

## Verdict

**agree.** The row's anchor, its `teaches`, the wave-1 receipt and the citing
note all reproduce from a fresh fetch. No number drift, no overreach found.

## Axes (godspeed)

1. **Identity** — does the row's byte anchor reproduce? (165,438 B / `e50c6060…`)
2. **Binding** — is the URL tag-pinned, and does the archive equal that tag's tree?
3. **Grounding** — do the row's search terms and `teaches` reproduce on the bytes?
4. **Citation truth** — does the note say only what the bytes say?
5. **Tier/scope fitness** — kind `code`, tier A, P3 surface keyword present?

Moves kept: all five hold (below). No move hurt any axis.

## 1. Fetch, digest, receipts

Two independent fetches by this seat, plus the wave-1 receipt:

| fetcher | fetched_at (UTC) | http | bytes | sha256 |
|---|---|---|---|---|
| wave-1 `NoteWalker` receipt | 2026-10-20T15:42:32Z | 200 | 165,438 | `e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56` |
| this seat, fetch 1 | ~2026-10-20T15:59:46Z (body mtime) | 200 | 165,438 | `e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56` |
| this seat, fetch 2 | 2026-10-20T16:02:05Z → 16:02:06Z | 200 | 165,438 | `e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56` |

- Row anchor cell: "tarball 165,438 B; sha256
  e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56" — **equal**.
- Exactly **one** wave-1 receipt exists for this URL
  (`fetch/NoteWalker/receipts.jsonl`, schema `mado-fetch-receipt-v1`, JSONL
  parses). Its `tool` field is the same curl 8.23.0 build. Its body file
  `fetch/NoteWalker/walker-v2.17.2-src.tar.gz` re-hashes to `e50c6060…` — the
  receipt is not orphaned.
- Sweep for the same archive under other URL spellings
  (`walker/tar.gz`, `walker/archive`, `*.tar.gz`) over all
  `fetch/*/receipts.jsonl`: no other receipt, no competing digest.
- My seat's body and receipt:
  `.ufo/waves/round-18/fetch/ReopenS079/walker-v2.17.2-src.tar.gz` +
  `receipts.jsonl` (fetched_at 2026-10-20T16:02:06Z).
- 165,438 B also matches the note's WX table entry (`walker-route-r18.md:28`).

## 2. Tag resolution and pinning

```
$ git ls-remote https://github.com/abenz1267/walker.git 'refs/tags/v2.17.2*'
a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2
$ git clone -q --depth 1 --branch v2.17.2 https://github.com/abenz1267/walker.git walker-clone
$ git -C walker-clone log -1 --format='%H %ci %d'
a515085fd39fae80acc086c8fbfd9b7771a9a11d 2026-10-08 08:45:24 +0200  (grafted, HEAD, tag: v2.17.2)
$ git -C walker-clone rev-parse 'HEAD^{tree}'
5e3afb6b29cb8a2cab916fa0cfc15784d71a7998
$ diff -r --exclude=.git walker-clone ext/walker-2.17.2 && echo TREE-IDENTICAL-TO-TAG
TREE-IDENTICAL-TO-TAG
```

- The URL **is tag-pinned by ref name**: it names `refs/tags/v2.17.2`, and
  `ls-remote` resolves that ref to `a515085f…`. Tar root is `walker-2.17.2/`.
- The tag is **lightweight**: no `refs/tags/v2.17.2^{}` peeled line, while the
  repo has 387 peeled lines for other (annotated) tags. A lightweight tag is
  movable upstream, so pinning is "ref + digest as of 2026-10-20", not
  immutable by construction. The digest anchor (`e50c6060…`) is what makes the
  row safe; the tree identity check makes the content safe even if codeload's
  archive bytes were ever regenerated.
- Extracted tree is **byte-identical** to a checkout of that tag (76 files,
  `diff -r` clean, `.git` excluded). So the archive is not a repackaged or
  different tree.

## 3. Grounding of `teaches` (re-run on the extracted tag tree)

| `teaches` clause | command | result |
|---|---|---|
| no `notify::` or `use notify` call in `src/` | `grep -rn --include='*.rs' -e 'notify::' -e 'use notify' src/` | **0 hits** |
| `connect_changed` only for GSettings keys and the search entry | `grep -rn 'connect_changed' src/` | **exactly 3**: `src/main.rs:142` (`color-scheme`), `src/main.rs:149` (`accent-color`), `src/ui/window.rs:479` (search entry) |
| no config reload entry point | `grep -rn 'reload' src/`; `grep -rn 'set_config' src/` | **0 / 0 hits** |

`notify` in the whole tree (8 lock, 1 manifest, 1 licence, 6 source):
`Cargo.toml:21` `notify = "8.2.0"`; `Cargo.lock:1347-1360` the `notify` package,
whose dependency list carries `"inotify",` at `Cargo.lock:1355`; `LICENSE:419`
prose; `src/niri.rs:160,168,185,205,212,213` a **closure parameter named
`notify`** (`mut notify: impl FnMut() + Send + 'static,`), not the crate. This
is exactly what the note says ("closure parameter names in `src/niri.rs:160-213`",
"its dependency list includes `inotify`").

`watch` hits are only `src/niri.rs:157,165,182` (`watch_empty_workspace_focuses`,
`watch_event_stream`) — a **niri IPC event stream** (`Socket::connect()`,
`Request::EventStream`), not a filesystem watcher.

Counterexample probe beyond the row's term list:
`grep -rni -e filemonitor -e monitor_file -e file_monitor -e 'gio::File' src/`
finds only `gio::File` path reads / `load_contents_future` (preview, files
provider, theme css); **no `FileMonitor` / `monitor_file`**. The absence is not
an artefact of the chosen keywords.

Read-once structure behind "no config reload": `src/config.rs:7`
`static LOADED_CONFIG: OnceLock<Walker> = OnceLock::new();`, `load()` at
`src/config.rs:586-590` sets it once, `get_config()` at `:592-595` reads it.
Matches the note's WS:7 and WS:586-594 anchors.

## 4. Truthfulness of the citing note

- Header line 1 names `S079 https://codeload.github.com/…/refs/tags/v2.17.2
  (whole-tree grep for notify, watch, reload)`.
- `walker-route-r18.md:28` defines WX as the tarball, "walker v2.17.2 tree
  (165,438 B)", "whole-tree `grep`, no line anchor" — honest about the
  container/member asymmetry; the byte count matches my fetch.
- `walker-route-r18.md:96-103` states the three clauses; each reproduces
  verbatim, and the cited anchors `WM:142`, `WM:149`, `ui/window.rs:479` are
  the correct lines in the tag tree (`WM` = `src/main.rs`).
- `walker-route-r18.md:100-103` localises `notify` to Cargo.lock + niri
  closure parameters — correct.
- The note hedges the residual: "`[UNK]` Whether the unused `notify`
  dependency (`WK:21`) is reached through any code the whole-tree search did not
  match (the search was textual, not a call graph)." That hedge is the correct
  one; my monitor probe narrows but does not close it.
- No statement in the note attributes a host fact to this tarball; host claims
  are separately file-anchored.

Minor, non-defect: the note's S079 clause lists "notify, watch, reload" and
omits `inotify`/`set_config` from the row's five search terms; the row keeps
all five, and both omitted terms were re-run above with no hits.

## 5. Kind / tier / scope

- **kind `code`** — correct: upstream Rust source tree, not docs or a dataset.
- **tier A** — correct: the tag archive of the upstream repository is a
  primary source for "what the v2.17.2 source contains". Scope is exactly that
  textual question, so no primary source is missing.
- **scope** — "whole-tree textual search for file watchers and config reload in
  the v2.17.2 source": matches the commands actually re-run, and the **source
  cell names the P3 surface keyword `walker`** (`abenz1267/walker`). The scope
  cell itself says "v2.17.2 source"; the keyword is in the source cell, which
  the rule allows.
- **Row cells** `mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md`
  are consistent with the note's date, surface and use.
- The row lists **no further files** in its source/anchor cells (the anchor
  cell lists the tarball plus the five search terms only), so the "re-fetch up
  to three more" clause had no targets; S072-S078 are separate rows and were
  not re-opened here.

## Remaining unknowns

- `[UNK]` Call-graph reachability of the declared-but-unused `notify` crate:
  textual search cannot prove no dynamic/path-qualified use; the note says so.
- `[UNK]` Whether Arch's walker package patches add a watcher or a reload path;
  this row is upstream-tag scope and claims nothing about `/usr/bin/walker`.
- `[UNK]` Long-term byte stability of codeload's generated archive (upstream
  may re-tag a lightweight ref); today's digest and the tree-equals-tag check
  are the evidence.
- `[UNK]` Other tags named in the note's `verified-at` line (elephant, omarchy)
  — outside S079 and not re-checked here.

## Commands run (exact, in order of use)

```
curl -sSL --max-time 60 -o /tmp/reopen-s079/walker-v2.17.2.tar.gz -w '%{http_code} %{url_effective} %{size_download}\n' 'https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2'
  -> 200 https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2 165438
git ls-remote https://github.com/abenz1267/walker.git 'refs/tags/v2.17.2*'
  -> a515085fd39fae80acc086c8fbfd9b7771a9a11d refs/tags/v2.17.2
sha256sum /tmp/reopen-s079/walker-v2.17.2.tar.gz
  -> e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56
git clone --depth 1 --branch v2.17.2 https://github.com/abenz1267/walker.git /tmp/reopen-s079/walker-clone
tar xzf walker-v2.17.2.tar.gz -C ext
diff -r --exclude=.git walker-clone ext/walker-2.17.2   -> no output (identical)
grep -rn --include='*.rs' -e 'notify::' -e 'use notify' src/   -> no output
grep -rn 'connect_changed' src/   -> main.rs:142, main.rs:149, ui/window.rs:479
grep -rn 'reload' src/ ; grep -rn 'set_config' src/   -> no output, no output
grep -rn 'notify' . --exclude-dir=.git   -> Cargo.lock x8, Cargo.toml x1, LICENSE x1, src/niri.rs x6
grep -rni -e 'filemonitor' -e 'monitor_file' -e 'file_monitor' -e 'gio::File' src/   -> gio::File path reads only, no monitor
grep -h 'codeload.github.com/abenz1267/walker/tar.gz' .ufo/waves/round-18/fetch/*/receipts.jsonl   -> 1 receipt (NoteWalker)
sha256sum .ufo/waves/round-18/fetch/NoteWalker/walker-v2.17.2-src.tar.gz   -> e50c6060…
curl ... (second fetch, T0 16:02:05Z, T1 16:02:06Z)   -> 200, 165438, e50c6060…
```

GATE | S079 | https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2 | 2026-10-20 | walker-v2.17.2-src.tar.gz:walker-2.17.2/src/niri.rs:160 "mut notify: impl FnMut() + Send + 'static," (8 words) | e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56 | agree: three independent fetches (wave-1 receipt 15:42:32Z, mine 15:59Z and 16:02:06Z) all give 165,438 B / e50c6060…; refs/tags/v2.17.2 resolves to a515085f (lightweight) and the extracted tree is byte-identical to that tag's checkout; re-running the row's terms gives 0 `notify::`/`use notify`, exactly 3 `connect_changed` (main.rs:142/149, ui/window.rs:479), 0 `reload`/`set_config`, and the sole `notify` in src is this closure parameter, so kind `code`, tier A (primary upstream tree, `walker` named in the source cell), scope and the note's use all hold
