# ReviewSourcesRows — partial

Target: S096/S097/S098 row shape at `01b80946d92b26370d3012a7da655d00dd135154` (tip). All lane
citations below are `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 01b80946…:<path>`
bytes unless marked [worktree]. Verdict is **partial**: the three rows themselves conform to the
11-column contract end to end (every anchor value I re-derived reproduces; every used-by file
cites its id; the S084/S094 flips moved exactly status+used-by), but the committed lesson § Gate
carries two inaccurate quote records and the S096-vs-S090/S091 overlap question the round was
asked to settle is answered only implicitly.

## Attack

### 1. 11 columns, enums, tier, recheck — census on committed bytes

Ran the CORPUS.md census (`/home/vgpnk/Projects/shokunin/CORPUS.md:135-147`) against
`git show 01b80946…:corpus/SOURCES.md` (saved /tmp/SOURCES-rev.md):

- rows = 98; malformed (NF≠13) = none; duplicate ids = none; enum violations (kind / tier /
  status / tier-A-community) = none; used-by existence over all 81 mined rows = no missing path.
- S096 `corpus/SOURCES.md:108`, S097 `:109`, S098 `:110`: kind `code` ✓, tier `A` ✓ (host file
  bytes / official upstream payload / source code — all primary for their scope cells; none is
  `community`), status `mined` ×3 ✓, opened `2026-10-20` ×3 ✓.
- recheck: S096 `on-change` (precedent S090/S091, both `on-change`), S097/S098 `on-release`
  (tag-pinned upstream — correct trigger). Contract allows "ISO date or cadence" — conformant.

### 2. used-by paths exist and actually cite the row (grep per file, tip bytes)

Row cells at the tip: S096 used-by = walker-deep.md, walker-deep-r9.md, walker-live-surface.md,
remaining-planes-census.md, tools/mado-verify.sh, SKILL.md (six paths); S097 =
corpus/knowledge/theme-route-r18.md; S098 = corpus/knowledge/walker-route-r18.md.

- All paths exist (existence census above). Citation counts of the id at the tip
  (`git show 01b80946…:<file> | grep -c`): walker-deep.md 1, walker-deep-r9.md 1,
  walker-live-surface.md 1, remaining-planes-census.md 1, tools/mado-verify.sh 9, SKILL.md 10,
  theme-route-r18.md 3 (head `source:` line names S097), walker-route-r18.md 2 (head `source:`
  line names S098). Every used-by file genuinely cites its row — no credited-but-unciting path.
- **F5 (observation, tip)**: S096 is also cited by `corpus/knowledge/walker-route-r18.md:328`
  and `corpus/README.md:137-139` but is in neither's used-by (six-path list). Under-inclusive
  used-by breaches nothing (contract needs ≥1), but the in-flight wave-2 lesson text
  ("S096 used-by gained … the eight-path list") is **not part of tip 01b8094** — the committed
  lesson has no wave-2 section (`git show 01b80946…:corpus/lessons/round-19.md | grep -c
  'Wave-2 corrections'` = 0; the worktree file has it: 1) and the only uncommitted SOURCES.md
  delta is the S096 row line (`git diff 01b80946… -- corpus/SOURCES.md`: 1 line). A tip reviewer
  must not credit the eight-path claim.

### 3. teaches grounded in anchors — re-derived from the bytes

- **S096** — every clause reproduces on this host (file bytes only):
  `/usr/bin/walker` = 7,039,912 B, sha256 `25240650…3096`, mtime `2026-10-08 11:14:32 -0300`
  (stat/sha256sum); `version2.17.2` found at 856,295; `2.17.2\n` starts at 856,302
  (`data[856302:856311] = b'2.17.2\nto'`); context `…with 6 elementsversion2.17.2\ntoggle exact
  search…` exact; literal counts: `2.17.2` ×1, `2.17.0` ×0; 856,302 inside `.rodata`
  (readelf -S: off 0x0b6900 size 0x074654 → 747,776-1,224,532 ✓). `desc` sha256 `5c0d9d89…`
  ✓, `%VERSION%` `2.17.2-1`, `%BUILDDATE%` `1791468872` = 2026-10-08T14:14:32Z = binary mtime,
  `%INSTALLDATE%` `1792498606` = 2026-10-20T12:16:46Z = log line 2929's `09:16:46 -0300`
  (date -u -d @; the log line text matches verbatim). pacman.log = 244,858 B sha256 `27bbd0b5…`
  ✓ (still reproducible today). mtree sha256 `d5dfb3f1…` ✓, line 30 =
  `./usr/bin/walker time=1791468872.0 size=7039912 sha256digest=25240650…` ✓ — this grounds the
  teaches clause "the packaged digest equals the on-disk binary digest" (the mtree
  `sha256digest=` equals the on-disk sha). Epoch conversions and every cross-date agreement in
  the teaches cell check out. No running-process claim anywhere in the row ✓.
- **S097** — quote grounding: the Gate's quoted body is committed at
  `.ufo/waves/round-19/fetch/SrcS094/colors.toml` = 461 B, sha256
  `dbdd13a6…1786` (= row anchor), line 4 = `background = "#121212"` (= Gate quote) ✓. Tag
  identity: `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4` →
  `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`, no peeled line (lightweight, as the anchor
  states) ✓. **F4 (shape gap)**: the teaches cell's host-provenance claims (12 payload files
  byte-identical to their v3.8.4 blobs; host checkout HEAD = the tag commit; 16 extra template
  outputs; `~/.local/share/omarchy/version` still 3.8.3) are **not in the row's anchor**, which
  carries only upstream identities (commit/tree/blob ids + raw sha256). They are grounded in
  the committed w1 report `.ufo/waves/round-19/w1/reports/SrcS094.md:25-58` (byte-comparison
  method, HEAD `8fcc9d6…`, the 12-file list, the 3.8.3 note) — real grounding, but outside the
  registry, deviating from the host-row convention the round itself set (S091/S095/S096 anchor
  host digests in-row). A rechecker holding only SOURCES.md cannot check the teaches cell.
- **S098** — fetched independently (receipts below): crate 200 / 15,821 B, sha256
  `2fb43323…85b5` = row anchor = walker v2.17.2 `Cargo.lock:2708` checksum (lock committed at
  `.ufo/waves/round-19/fetch/SrcS084/walker-v2.17.2-Cargo.lock:2705-2708`, lines read at the
  tip: `name = "xdg" / version = "3.0.0" / checksum = "2fb43323…"`); tag-pinned
  `src/config.rs` (a515085f…) = 19,675 B sha256 `93b6bd6f…1469` (= row anchor) with the exact
  call at `:219` `xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`
  (= teaches); extracted `src/base_directories.rs:446-448` doc "Searches `XDG_CONFIG_HOME` and
  then `XDG_CONFIG_DIRS`." and `:308-310` (`…home.join(".config")`) / `:321-323`
  (`unwrap_or(vec![PathBuf::from("/etc/xdg")])`) — teaches' defaults grounded ✓.

### 4. Supersessions (S084→S098, S094→S097) conform to rule 2

Cell-level diff baseline `9c54c56a…` → tip for both rows: only `status` (mined → rejected) and
`used-by` (→ `—`) changed; source/kind/tier/scope/anchor/teaches/opened/recheck byte-identical;
S094's rejected scope text ("the only theme on this host") is preserved verbatim. The lesson §
Gate old→new log (lesson `:46-50` at the tip) matches this diff exactly. Both superseding rows
open their teaches with `supersedes S0NN —` (S097 also marks it in `source`), i.e. resolvable
prior ids ✓.

### 5. Lesson row arithmetic — exact

Census at both revs: baseline rows 95 (A=88, mined=80, queued=8, rejected=7); tip rows 98
(A=91, mined=81, queued=8, rejected=9). Lesson "Rows 95 → 98 (A 88 → 91; mined 80 → 81;
rejected 7 → 9)" — every number reproduces.

### 6. Findings

- **F1 (minor, tip defect): Gate S096 quote mislocated.** Lesson `:41` (Gate, S096 line):
  `` `/usr/bin/walker` byte 856,302: "version2.17.2" `` — the string `version2.17.2` starts at
  byte **856,295**; 856,302 is the start of `2.17.2\n` (verified bytes above). The row's own
  anchor is exact; the Gate's admission record is off by 7 bytes. [worktree: an appended
  wave-2 correction states exactly this — confirming the defect exists at the tip.]
- **F2 (minor, tip defect): Gate S098 word count.** Lesson `:43`: "(6 words)" — "Searches
  `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`." is 5 words. Cosmetic; the location
  (`base_directories.rs:447-448`) and digest are correct. [worktree: corrected in-flight.]
- **F3 (minor, process): no recorded QUALITY-17-style overlap review for S096 vs S090/S091.**
  The overlap is real: pacman.log line 2929 and its digest appear in both S090 (`:102` anchor)
  and S096 (`:108` anchor); the identical binary sha `25240650…` appears in both S091 (`:103`
  anchor) and S096. S096 supersedes neither (its teaches opens with the three-fact sentence, no
  `supersedes S0NN`), and no Gate/Search-log/QUALITY line says why three active host rows may
  share anchor ground. The rule's **letter** is not triggered — QUALITY 17
  (`corpus/QUALITY.md:34`) screens "repeated canonical URLs across active rows" and host rows
  have no URL — so this is not a breach. But the differentiation the assignment asked about
  exists only implicitly: the Paths entry "Walker version provenance (P3, round 19)"
  (`corpus/SOURCES.md:148-156`) assigns each row a role ("host bytes at the moved pin first …
  then the log line that dates the move (a log line is never a binary fact) … last the user
  config bytes"), and the scope cells are distinct (version binding vs transaction-log record
  vs byte identity incl. configs). One Gate sentence recording that screen would have closed
  the question; nothing at the tip does.
- **F4** — see §3 (S097 host-side teach clauses grounded outside the row's anchor).
- **F5** — see §2 (eight-path used-by is in-flight, not tip).

## Limits

- Did not independently rebuild S097's tree/blob ids (`3fc08f95…`, `ff02c341…`, per-file blobs)
  — that needs an omarchy clone; covered by w1 receipts and the w2 ReopenS097 seat. I verified
  the tag→commit identity myself (ls-remote) and the committed quote body end to end.
- Worktree drift: wave-2 integration modified the worktree while I worked (lesson, SOURCES.md,
  README, SKILL.md, QUALITY.md and many notes now dirty). I re-grounded every lane citation
  against committed tip bytes; material that exists only in the worktree is marked [worktree]
  and is not credited as part of the tip.
- pacman.log matches its anchored digest today; as an append-only log it will drift — that is
  what S096's `on-change` recheck is for, not a defect.
- S097's scope-cell host facts (19 payload dirs, empty `~/.config/omarchy/themes`, theme.name
  12 B) were not re-listed by me (host-pause name-only rule; covered by ReopenS097/SrcS094).
- Fetch receipts (curl, no auth, bodies in /tmp only): `raw.githubusercontent.com/abenz1267/
  walker/a515085fd39fae80acc086c8fbfd9b7771a9a11d/src/config.rs` — HTTP 200, 19,675 B, sha256
  `93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469`; `static.crates.io/crates/
  xdg/xdg-3.0.0.crate` — HTTP 200, 15,821 B, sha256
  `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`;
  `github.com/basecamp/omarchy.git` ls-remote `refs/tags/v3.8.4` → `8fcc9d6048af4cb0e3af8512
  c78049857a3b53dd`. fetched_at 2026-10-20T18:33:42Z (/tmp/config.rs, /tmp/xdg.crate, /tmp/
  xdgx/). Receipts are mine; HTML/API digests not used as anchors anywhere above.

## Installs

None.
