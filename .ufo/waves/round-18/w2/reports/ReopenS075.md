# Re-open S075 — walker `src/main.rs` @ v2.17.2 (non-author check, R17-V3)

Seat: MadoR18.ReopenS075 (wave 2, FALSIFY). Baseline read at integration
commit `4c103b55b1ea5c3c555884afe3eb69b5189701b7`; the S075 row there is
byte-identical to the copy in this prompt (line sha256 `537a9352…` both).
Verdict: **agree** — the row survives every check; two prose-level
imprecisions in the citing note and one round-wide receipt gap are recorded
below.

## Exact commands and outputs

1. Re-fetch, tag URL (receipt `.ufo/waves/round-18/fetch/ReopenS075/receipts.jsonl` line 1,
   body `walker-main-rs-v2.17.2`):
   `curl -sSL --max-time 60 -o walker-main-rs-v2.17.2 -w '%{http_code} %{url_effective}' https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/main.rs`
   → `200 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/main.rs`;
   `26673` bytes; sha256 `f09466fecf903cb0bceb3444bf0af099cc6471ca08b4bea6329125d5682d7e60`.
   Row anchor-cell digest is the same string. **Match.**
2. Every round-18 wave-1 receipt for this URL (`grep -l 'walker/v2\.17\.2/src/main\.rs' .ufo/waves/round-18/fetch/*/receipts.jsonl`):
   only two seats fetched it —
   `MadoR18.SrcWalkerThemes/receipts.jsonl:9` and `NoteWalker/receipts.jsonl:14`
   (both committed at `4c103b55`). Both: `http_status 200`, `bytes 26673`,
   `sha256 f09466fe…d7e60`, fetched 15:40:39Z / 15:40:52Z. **Both agree with
   the row and with my re-fetch.** Their wave-1 body files
   (`…/MadoR18.SrcWalkerThemes/src-main.rs`, `…/NoteWalker/walker-v2.17.2-src-main.rs`)
   hash to the same digest and size on disk.
3. Tag resolution:
   `git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'`
   → `a515085fd39fae80acc086c8fbfd9b7771a9a11d  refs/tags/v2.17.2` and no
   `^{}` line. The tag is **lightweight**, and the URL is **tag-pinned**
   (ref `v2.17.2`, not a branch). Commit-pinned cross-check (receipt line 2,
   body `walker-main-rs-a515085f`):
   `…/walker/a515085fd39fae80acc086c8fbfd9b7771a9a11d/src/main.rs` → `200`,
   `26673` B, sha256 `f09466fe…d7e60`. The tag currently resolves to a tree
   carrying exactly the row's bytes.
4. Further files listed in the row's source/anchor cells: **none** — the row
   names only `src/main.rs`, so there was nothing else to re-fetch.
5. Line anchors, numbered (`awk` over the fetched body):
   - `104-108`: `if app.flags().contains(ApplicationFlags::IS_SERVICE) {` / `set_is_service(true);` / `}` / blank / `config::load().unwrap();` — exact.
   - `124-126`: `if !dmenu || is_service() {` / `elephant = which("elephant").is_ok();` / `set_has_elephant(elephant);` — exact.
   - `670-674`: `if !is_dmenu() && !is_connected() && has_elephant() { thread::spawn(|| init_socket().unwrap()); } else if !has_elephant() && !is_dmenu() { println!("Please install elephant."); process::exit(1);` — exact.
   - `784-786`: `if !is_service && (args.contains(&"--close"…) || args.contains(&"-q"…)) { process::exit(0); }` — exact.
   - `802-803`: `if !app.flags().contains(ApplicationFlags::IS_SERVICE) && !dmenu { println!("make sure 'walker --gapplication-service' is running!");` — exact.
   - `872-882`: `fn listen_activation_socket` … `XDG_RUNTIME_DIR`/`env::temp_dir()`, `push("walker")`, `create_dir`, `push("walker.sock")` — exact.
6. Rubric mechanics (read only): `measure.py:119` requires the 13-cell row and
   `measure.py` c2 upstream filter requires `kind ∈ {docs,spec,code}`, `https://`
   in the source cell, and a P3 keyword (`walker`, `elephant`) in source or
   scope. S075 splits to 13 cells, `kind=code`, `tier=A`, `status=mined`,
   `used-by=corpus/knowledge/walker-route-r18.md`; source names `walker` and
   scope names `elephant`. `evidence/measure-after.json.txt` P3 lists S075 in
   `sources_ok`. The instrument credits it for the reason the row states.

## Row judgment (kind / tier / scope / teaches)

- **kind `code`** — correct: a Rust source file, not a doc page.
- **tier A** — correct: the upstream repository's own tagged source is the
  primary source for walker's startup control flow; the scope claims only
  source facts, no host behaviour.
- **scope** — "startup order, elephant presence check, service message, close
  handling, activation socket at tag v2.17.2" is named and each noun maps to an
  anchored block (104-108 order at UI init; 124-126/670-674 elephant;
  802-803 message; 784-786 close; 872-882 socket). One overhang: "startup
  order" also depends on `startup`'s own sequence (`:809-812`:
  `init_app_state`, `init_ui`, `listen_activation_socket`,
  `listen_niri_workspaces`), and lines 809-812 are not in the anchor list. No
  claim in the row or note asserts that sequence, so this is an
  anchor-completeness nit, not an ungrounded claim.
- **`teaches`** — every statement is literal in the file: `config::load().unwrap()`
  (`:108`, reached from `startup` at `:809`); `"Please install elephant."` with
  `process::exit(1)` (`:673-674`); the exact service message (`:803`); the
  `$XDG_RUNTIME_DIR/walker/walker.sock` path (`:873-882`). No overstatement.

## Citing note (`corpus/knowledge/walker-route-r18.md`)

Every `WM:` anchor the note uses was checked against the body: `WM:104-105`
(`IS_SERVICE` flag), `WM:108`, `WM:124-126`, `WM:142`/`WM:149` (`connect_changed`
for `color-scheme`/`accent-color`), `WM:635-642` (close_when_open / param_close
quit), `WM:670-674`, `WM:782` (`is_service` local), `WM:784-786`, `WM:802-803`.
All quote the code correctly and the header's function list (`init_ui`,
`handle_command_line`, `activate`, `listen_activation_socket`) matches the
symbols at `:103`, `:404`, `:626`, `:872`.

Two prose imprecisions, neither a false behaviour claim:

1. "A non-service, non-dmenu invocation **without a running service** prints
   … `[WM:802-803]`." The line tests only the `IS_SERVICE` flag. That the
   message is only reachable when no service instance exists follows from
   GApplication emitting `startup` in the primary instance only; it is an
   unlabelled inference from GTK semantics, not from the cited line.
2. "`-q/--close` is handled **before any service check**" — line 784's
   condition is itself `!is_service` (`:782`). What it precedes is the service
   message (`:802`) and `init_app_state` (`:808`); the wording is loose but the
   described exit-0 behaviour is exactly `:784-786`.

The note does not make the row's `walker.sock` claim; it cites
`listen_activation_socket` only, which exists. Nothing in the note uses S075
to assert host or runtime behaviour.

## Findings and limits

- **Round-wide receipt gap (not S075-specific).** At `4c103b55` only
  `fetch/*/receipts.jsonl` is committed: `git show
  4c103b55:.ufo/waves/round-18/fetch/MadoR18.SrcWalkerThemes/src-main.rs` →
  `fatal: path … exists on disk, but not in '4c103b55…'`; `.gitignore` does
  not exclude those bodies. So R17-V3's committed artifact is the receipt line
  (url, body name, byte count, sha256, fetch time), not the bytes themselves;
  a closure must re-fetch (as done here) to hash a body. If "committed raw
  fetch receipt (body bytes…)" is read as committed body files, the claim
  overstates; read as receipt fields, it holds.
- **Remaining unknowns.** (a) Upstream can still move a lightweight tag; the
  durable pin is the sha256, and no tag signature was checked. (b) Whether
  `/usr/bin/walker` is a faithful build of this tag is out of this row's scope
  and is not claimed by it. (c) The note's "without a running service"
  inference was not exercised (no walker invocation, per host pause).

GATE | S075 | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/main.rs | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS075/walker-main-rs-v2.17.2:803 | "make sure 'walker --gapplication-service' is running!" (6 words) | f09466fecf903cb0bceb3444bf0af099cc6471ca08b4bea6329125d5682d7e60 | agree: my re-fetch and both wave-1 receipts (26673 B) hash to the row anchor; tag v2.17.2 is lightweight at a515085f and the commit-pinned bytes are identical; all six anchor ranges and every WM citation are line-exact; only prose imprecision in the note, no ungrounded claim
