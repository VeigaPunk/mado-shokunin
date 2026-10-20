# AtkDeltaCli — holds

Axis attacked: wave-1 seat `MadoR19.DeltaWalkerCli` claim that walker's CLI flag
code (`fn add_flags`) and `src/data.rs` are byte-identical between tags v2.17.0 and
v2.17.2 — the byte-identity the round-19 routing leans on as "CLI unchanged".
Report under attack: `.ufo/waves/round-19/w1/reports/DeltaWalkerCli.md:12-20`
(headline), `:87-101` (§3.1-3.2), `:183-189` (§6 table), `:291`.

Verdict after independent re-fetch, whole-tree diff and released-binary check:
**the byte-identity claim is true, exactly as written.** Two precision cracks and
one overbroad headline fragment are recorded below; none falsifies the claim.

## Attack 1 — independent tag-pinned fetch (fresh bodies, not the seat's)

`/tmp/atl-deltacli` scratch; fetched_at `2026-10-20T18:06:34Z`, no auth, bodies
under `/tmp` only.

```text
https://raw.githubusercontent.com/abenz1267/walker/v2.17.0/src/main.rs   200 24450 c258547840491e9c57eb89578e82bc1dbe1db5015271303cdae0e6efb3f7b2d4
https://raw.githubusercontent.com/abenz1267/walker/v2.17.0/src/data.rs   200 26338 996db119ba61cb1505aa26782a19c7b8db49889874bd87ecbf277c9145cada09
https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/main.rs   200 26673 f09466fecf903cb0bceb3444bf0af099cc6471ca08b4bea6329125d5682d7e60
https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/data.rs   200 26338 996db119ba61cb1505aa26782a19c7b8db49889874bd87ecbf277c9145cada09
https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.0   200 161218 c3498742a9866422b2947340a515eeb7932333bb8f99b171d159c0a7ece0a12f
https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2   200 165438 e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56
```

Tag→commit resolved independently through the GitHub refs API (fetched_at
`2026-10-20T18:0xZ`, bodies `/tmp/atl-deltacli/api-ref-v2.17.0.json` sha256
`8255dcb75a3e40faf1e0f3e1e2842f5d38db8f6810956a9900c6feefb32966d4`, 370 B;
`api-ref-v2.17.2.json` sha256
`14147b773ad295a74e999ed36aded0403e868a4551c20a6d84cd2b4079a547de`, 376 B):

```text
v2.17.0  ref refs/tags/v2.17.0  type tag     sha 2a4bde009b0deb34e6f9cdd1a4f8c2457e33c18f
v2.17.2  ref refs/tags/v2.17.2  type commit  sha a515085fd39fae80acc086c8fbfd9b7771a9a11d
```

Peeled the annotated v2.17.0 tag object (`/git/tags/2a4bde0…`, HTTP 200, 750 B,
sha256 `9887284c14fd0f3a943c5ba4292060d0570fc5e33472f8873e1363b883b926ed`):

```text
tag v2.17.0 -> object commit 42b3ed88abf50bc52638fb2835b7f17e3ea3ac4c
```

The seat's committed bodies (`.ufo/…/fetch/DeltaWalkerCli/`, read from
`01b80946…`) hash to exactly those four digests:

```text
v2.17.0-src_main.rs 24450 c258547840491e9c…   v2.17.2-src_main.rs 26673 f09466fecf903cb0…
v2.17.0-src_data.rs 26338 996db119ba61cb15…   v2.17.2-src_data.rs 26338 996db119ba61cb15…
```

Receipts in the lane name the same commits (`42b3ed8…`, `a515085…`), same bytes,
same shas; the four tag-pinned bodies I fetched are byte-equal to the seat's
commit-pinned bodies. No fetch discrepancy.

## Attack 2 — re-run the seat's exact command

Boundaries located first (`awk '/^fn add_flags/{s=NR} s&&/^}$/{print NR}'`):
v2.17.0 `main.rs:189-396`, v2.17.2 `main.rs:195-402`. Then the report's own
command, verbatim, over the tag-pinned files:

```text
$ diff <(sed -n '/^fn add_flags/,/^}/p' v2.17.0/main.rs) \
       <(sed -n '/^fn add_flags/,/^}/p' v2.17.2/main.rs)
(no output)
SED_DIFF_LINES=0
SED_DIFF_RC=0
app.add_main_option occurrences in extracted body: 23 / 23
```

Independent extraction by line range gives the same result:

```text
189,396p -> af0.rs (208 lines) sha256 ae65bd51b018ed3a9b939d708788284983577a6e155fdc5a8ecf5520b248d7a5
195,402p -> af2.rs (208 lines) sha256 ae65bd51b018ed3a9b939d708788284983577a6e155fdc5a8ecf5520b248d7a5
diff -u af0.rs af2.rs -> empty (rc 0)
```

No `#[cfg]` inside either body; one `fn add_flags` per file. Registered names,
parsed from the extracted bodies, identical and in the same order (23 each):
`version, nosearch, nohints, inputonly, password, selectsingle, index, provider,
set, placeholder, height, minheight, maxheight, current, width, minwidth,
maxwidth, theme, dmenu, close, hideqa, keepopen, exit`.

The full-file diff has 10 hunks, at old lines
`1, 9, 20, 53, 80, 395, 598, 613, 802, 823`; **no hunk intersects the function
interior** (the `@@ -395,9 +401,10 @@` hunk begins inside the final two
context lines of `add_flags` and changes only the `handle_command_line`
signature below it). This is stronger than the `sed` slice: the compiler-input
function is untouched, not merely an equal-looking prefix.

`src/data.rs`:

```text
$ diff -u v2.17.0/data.rs v2.17.2/data.rs   -> empty
DATA_DIFF_RC=0
$ cmp v2.17.0/data.rs v2.17.2/data.rs        -> DATA_CMP_IDENTICAL
```

## Attack 3 — whole-tree check (is CLI registration or data.rs hidden elsewhere?)

Both tag tarballs (`codeload`) extracted and compared:

```text
$ diff -rq tree-v2.17.0 tree-v2.17.2
Cargo.lock  Cargo.toml  README.md  flake.lock  resources/config.toml
src/config.rs  src/keybinds.rs  src/main.rs  src/state/mod.rs
src/ui/window.rs  src/wayland_blur.rs   (+ Only in src: niri.rs)
```

That is exactly the seat's 12-file delta; `src/data.rs` is absent from it.
Tarball copies of both files hash equal to the raw fetches
(`main.rs` `c2585478…`/`f09466fe…`, `data.rs` `996db119…` both).
`add_main_option` occurs **only** in `src/main.rs`, 23 times per tag:

```text
     23 tree-v2.17.0/src/main.rs
     23 tree-v2.17.2/src/main.rs
```

Tarball `data.rs` diff and tarball `add_flags` diff: 0 lines each. No CLI
registration exists outside `add_flags`, so "the flag code is byte-identical" is
a complete statement, not a partial one.

## Attack 4 — released binaries (the "838-byte description run")

Extracted `usr/bin/walker` from the host package cache (file bytes only, no
pacman; host pause respected). Binaries and the installed path agree with the
seat:

```text
pkg0 64826a8531eac525adfa3eff65548e93a6f7714feb1d3e13b4fa35bbcc3cfda0 6,661,264 B
pkg2 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096 7,039,912 B
/usr/bin/walker                                        25240650…     7,039,912 B
```

Description run reproduced exactly (same bytes, same offsets, same sha):

```text
2.17.0 start 819030 end_excl 819868 len 838 sha256 e429efc3bc96c328d284d3d0583e48c5beb3ac7001f0e8f599afa8de26d25c75
2.17.2 start 832855 end_excl 833693 len 838 sha256 e429efc3bc96c328d284d3d0583e48c5beb3ac7001f0e8f599afa8de26d25c75
```

Run contains no `config`/`reload`/`watch` token in either build (0 each), and
every one of the 23 description strings occurs with an identical count in both
binaries (`dmenu` 18/18, `theme to use` 2/2, all others 1/1). Version literal
claim also reproduces: `version2.17.0\n` only in 2.17.0, `version2.17.2\n` only
in 2.17.2, plain `2.17.0` 0× in 2.17.2 and plain `2.17.2` 0× in 2.17.0.

## What w1 overstates or leaves ragged

1. **The 838-byte run is not the concatenation of all 23 descriptions, and the
   seat's "invariant worth pinning is the 838-byte description run" (`:291`)
   needs that caveat.** Sum of the 23 source descriptions is **843** B; the blob
   is **838**. The missing 5 B is the whole `dmenu` description, which has no
   separate segment: the layout jumps
   `run[628:662] = b'tent. min 1.theme to usecloses wal'` — `theme to use`
   (ends 652) is immediately followed by `closes walker when open`, and `dmenu`
   exists only as a substring of `only show input. dmenu only.` (run offset
   `47+17=64`). [INFERENCE: rustc slices the 5-byte `&str` out of that literal;
   the byte layout is observed, the pointer is not disassembled.] Consequence: a
   re-pin recipe that concatenates descriptions from source will compute 843 and
   fail against `e429efc3…`; the correct invariant is "the 838-byte deduplicated
   blob", optionally plus a per-description census. The identity conclusion
   itself is unaffected — all 23 description texts are present in the run as
   substrings and their counts are equal across builds — so this is a recipe
   defect, not a false claim. The seat's §3.2 sentence ("the concatenated run from
   the first description … through the last") is literally accurate.

2. **Headline fragment "no socket code" (`:1`) is overbroad at byte level.**
   The accept-handler registration does change one token,
   `glib::unix_fd_add_local` → `glib_unix::unix_fd_add_local`
   (`main_full.diff` hunk `@@ -823,7 +888,7 @@`; old `main.rs:826`, new
   `main.rs:891` region). The seat's own §4 says "Only the intra-crate helper
   moved" (`:131-134`), so the body is honest and socket *semantics* are
   unchanged (same call, same arguments, same accept/drop/reset body); only the
   top line, if quoted alone, claims more than the bytes show. A pointer must not
   quote "no socket code" without §4.

3. **Offset convention in §3.3/§6 is the digit offset, not the literal start.**
   `version2.17.2\n` begins at file offset **856,295**; 856,302 is where
   `2.17.2` begins (`v[x-12:x+20] = b'h 6 elementsversion2.17.2\ntoggle'`).
   Same 7-byte shift on 2.17.0: full literal at **847,784**, digits at 847,791.
   The note writes `version2.17.2\n` *at* 856,302, mixing the two conventions.
   Inherited from round 9, not introduced here, but a re-pin that anchors the
   `version` prefix at 856,302 will read the wrong byte. No truth value changes.

## Does any round-19 pointer actually lean on "CLI unchanged"?

Checked because the ticket asserts it. **No pointer outside the seat does.**
`grep` over `corpus/knowledge/`, `.ufo/waves/round-19/w1/reports/`, `SCORECARD.md`
and `corpus/lessons/round-19.md` finds no citation of `838`, `e429efc3`,
`add_flags` or "CLI unchanged" outside `DeltaWalkerCli.md`. The corpus routes
help/version claims as version-bound and explicitly refuses the strong reading:

- `corpus/knowledge/walker-live-surface.md:306` — "Version-bound, therefore
  dated to the 2.17.0 build: … §2 help text and its sha256 `ca4820a8…`".
- `corpus/knowledge/walker-deep.md:623` — "`walker --help` flag table (§5) …
  not re-run on 2.17.2".
- `corpus/knowledge/waybar-walker-plane.md:480` and
  `.ufo/…/w1/reports/PtrWaybarWalkerPlane.md:9` — help flag list "not valid for
  2.17.2".
- `.ufo/…/w1/reports/DeltaWalkerConfig.md:189` — help sha is `[UNK]` without a run.
- `.ufo/…/w1/reports/CriticC2.md:66` — pointers "must refuse to claim" that help
  text/sockets are unchanged or changed in 2.17.2.

So the only load-bearing use is the source-level identity, and that is exact. If
anything the corpus is stricter than the seat's source finding. The seat's own
§9.1 already marks rendered help `[UNK]` (GLib 2.90.1 moved in the same
transaction), which matches `CriticC2.md:66`.

## Limits

- Rendered `--help`/`--help-all`/`--help-gapplication` bytes and GLib 2.90.1
  behaviour were not exercised (host pause): still `[UNK]`, as the seat says.
- Build provenance is not attacked: package-cache binary == `/usr/bin/walker`
  bytes, but "faithful build of the tag" remains `[UNK]` (route note
  `walker-route-r18.md:290-291`).
- Only the two named tags were walked; the other 390 walker tags were not
  enumerated. The `dmenu`-slice aliasing is inferred from byte layout, not from
  relocations/disassembly `[INFERENCE]`.
- `src/data.rs` identity is a source-byte fact; the seat's "elephant socket
  protocol untouched" reading of that file was not re-derived here.
- No LSP server exists for these remote GitHub bodies; semantic tracing was done
  with exact byte diffs and full-tree comparison, never with grep-as-proof.
  Grep was used only for literal token counts.

## Installs

none.
