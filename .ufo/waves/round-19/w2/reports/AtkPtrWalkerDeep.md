# MadoR19.AtkPtrWalkerDeep — breaks

Target: the appended `## Freshness pointer (round 19, 2026-10-20)` block in
`corpus/knowledge/walker-deep.md` (`:620-626` at tip `01b80946`; bullets `:622-626`),
diffed against baseline `9c54c56`. All paths absolute unless shown lane-relative; all
lane paths below are committed bytes read with `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 01b80946:<path>`.

Verdict in one line: the append is mechanically clean and its file-byte/package pins
re-verify, but bullet `:623` affirmatively says this round did **not** re-run measurements
that the round did re-run — contradicted by the `S091` row that the same bullet cites and
by the route doc that `:622` names. Two section citations are also wrong.

## (a) Were pre-existing bytes changed beyond the documented head `source:` swap? — NO (clean)

`git diff 9c54c56 01b80946 -- corpus/knowledge/walker-deep.md`: **one hunk**,
`@@ -615,4 +615,12 @@`, `9 insertions(+), 1 deletion(-)`. The "deletion" is the old
final line re-emitted with a terminating LF (`\ No newline at end of file` on each side).
No other hunk exists for this file.

Byte-prefix proof (python3 over the two committed blobs, written to /tmp):

```
base 38403 B sha256 0982ba066c72575a02732b99be5e6940ee72a437588b1fc2d2cac2ff9a576df8
tip  40352 B sha256 16c62209c2bcfbc12bbb9daf980216101a6c8ee5abfbbedf8d2b02903dc7ae35
base endswith_nl False
tip startswith(base) True          # first_diff offset: None
bytes after prefix: b'\n\n## Fre'
```

So every pre-existing byte value is unchanged in place; the only pre-existing-line
change is the added LF terminator (1 of the 1,949 appended bytes). `git diff --summary`
shows no mode/rename change.

`walker-deep.md` has **no `source:` head line at all** (head is `# Walker deep-note…` /
`Lane:` / `Measured`, lines 1-4; `grep -rc '^source:' corpus/knowledge/*.md` → 15
files with a head source line, and this file is not among them). The documented head `source:` token swaps
this round are in the two route files, not here:

```
walker-route-r18.md line 1, first diff at char 1391:
  base: ...; S084 https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html ...
  tip : ...; S098 https://static.crates.io/crates/xdg/xdg-3.0.0.crate ...
theme-route-r18.md line 1, first diff at char 411:
  base: ...; S094 (omarchy v3.8.4 themes/matte-black payload tree and colors.toml); ...
  tip : ...; S097 (omarchy v3.8.4 themes/matte-black colors.toml + tag commit and git tree ids; supersedes ...
```

The committed tip is not the w1 seat's own after-state: `PtrWalkerDeep.md:11` records
40,127 B / `4096f386…`, while the committed file is 40,352 B / `16c62209…`. [INFERENCE]
integration edited the block after the seat wrote it — relevant because the false clause
in (b) cites rows (`S091`, `S096`) that did not exist when the seat wrote
(`PtrWalkerDeep.md:25` F7).

## (b) Live/runtime claims, or "re-verified" that was not re-hashed — one bullet false

No live/runtime claim is made about walker 2.17.2: `:626` explicitly keeps behaviour
`[UNK]`, and the version facts are package/binary bytes (`S090`, `S096`). That part holds.

**But `:623` is false as written:**

> "Version-bound, dated 2026-10-14 and **not re-run on 2.17.2**: the `walker --help` flag
> table (§5), **the embedded-default byte run at offset 784,064 (§2.1)**, **struct/field-arity**
> and error/fallback token strings (§2.2-2.3, §6.1, §6.3), and **every `/etc/xdg/walker/config.toml`
> line anchor** (§2.1-2.4, §4.2, §7.4)."

Three of the four families were re-run against 2.17.2 this round:

1. **Embedded-default byte run.** The same bullet cites `S091`
   (`corpus/SOURCES.md:103`): "`/usr/bin/walker` … **embedded default at offset 806960**".
   `corpus/knowledge/walker-route-r18.md:206` records `b[806960:806960+13743]` equal to
   `/etc/xdg/walker/config.toml`, and `:244` records "The embedded-default offset moved
   from 784,064 (round-5/7/9 pins) to **806,960**."
   `.ufo/waves/round-19/w1/reports/DeltaWalkerConfig.md:45-47, :93`.
   Independent re-run now (`python3`, file bytes only):
   `find_offset 806960 len_cfg 13743 embedded==file True`.
   The pointer names the routing doc and cites the row that records this run while saying
   it was not run.
2. **struct/field-arity.** `DeltaWalkerConfig.md:66` measures it on the rebuilt binary:
   "**`struct Walker with 31 elements`** (+1 scalar … +1 table …)". My re-run over
   `/usr/bin/walker`: `[b'struct Walker with 31 elements']` (only hit); `S096`'s context
   string also carries `struct Action with 6 elements` (`corpus/SOURCES.md:108`).
3. **`/etc/xdg/walker/config.toml` line anchors.** `DeltaWalkerConfig.md:109-124` supplies
   the complete v2.17.0→v2.17.2 map (`:112`→`:118`, `:35`→`:41`, `:47`→`:53`, `:31-32`→
   `:37-38`, `:61`→`:67`, `:53-58`→`:59-64`, `:112-298`→`:118-305`). The anchors were
   re-derived this round; only the note text was not refreshed.

Only "error/fallback token strings (§6.1, §6.3)" is genuinely unre-run (no round-19 w1
measurement found for `theme not found. using default theme.` etc.).

**`--help` flag table misclassified as version-bound.** `:623` lists it first under
"Version-bound … not re-run". `.ufo/waves/round-19/w1/reports/DeltaWalkerCli.md:13, :99-100`
shows the 23-flag set and the 838-byte option-description run are **byte-identical** across
2.17.0/2.17.2 (sha `e429efc3…` at `[819030,819868)` vs `[832855,833693)`). Only rendered
help framing is GLib-bound (`glib2 2.88.3-1 → 2.90.1-1`, `pacman.log:2554`,
`DeltaWalkerCli.md:17`). "Not re-run" is true only of the rendered output
(`DeltaWalkerConfig.md:189` — `[UNK]`, needs a `walker --help` run); the table's walker
content is not version-bound at all.

**Trailing scope under-inclusive.** The clause "so §2.1-2.4 key enumerations are
incomplete for 2.17.2" omits — w1 also flags the `after` value set at §3 `:162-164` and the action rows at
§4.2 `:250-254` (`DeltaWalkerConfig.md:81-82`). The affected set is broader than §2.1-2.4.

**Verified true in the block** (independent `sha256sum`/`stat`/`wc` on host bytes):
`/etc/xdg/walker/config.toml` = 13,743 B, 305 L,
`3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`;
`~/.config/walker/config.toml` = 1,336 B, 49 L,
`fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` — both match `S091`
and `:623`/`:625`. `walker 2.17.0` literal count 0 / `2.17.2` count 1.

Theme hashes: `:625` lists them as "still dated 2026-10-14"; they were also re-hashed
this round, unchanged (`DeltaWalkerConfig.md:150-152`). Omission, not a falsehood — the
values are still the 2026-10-14 values. Elephant user TOMLs / menu Lua hashes: no
round-19 re-read found (`HostElephantBytes.md` reads only the elephant binary and package
metadata), so that clause is unrefuted.

## (c) Line numbers and section citations

**Line/file numbers correct** (`grep -n` / `sed -n` over committed bytes):

```
27:| walker | `walker --version` → `2.17.0`; pkg `2.17.0-1` ...
28:| elephant | `elephant version` → `2.21.0`; pkg `2.21.0-1` ...
3:Lane: ... Measured
4:2026-10-14 17:00–17:25 UTC ...
/var/log/pacman.log:2929  upgraded walker (2.17.0-1 -> 2.17.2-1)
/var/log/pacman.log:3095  upgraded elephant (2.21.0-1 -> 2.22.1-1)
```

`§2.1` (`:64-77`) does hold the embedded-default row (`:68`), `§2.2-2.3`/`§6.1`/`§6.3`
hold arity and fallback/error tokens (`:109-111`, `:360-434`), `§4.1` holds the
`listproviders` census and ElephantConfig defaults (`:180-198`), `§4.2`/`§7.4` hold the
`[providers]`/emergency anchors (`:241-262`, `:473-486`), `§1` holds the PIDs
(`:27-28`, `:45-46`), `§7.1` holds the binds (`:437-445`), `§5`/`§7` hold the omarchy
script anchors (`:312-356`, `:437-486`).

**Wrong section citations:**

- `:624` "ElephantConfig defaults and generated-doc counts (**§4.1, §5**)". ElephantConfig
  is at `walker-deep.md:196-198` (§4.1) and the 644-L doc count at `:197` (§4.1). §5
  (`:312-356`) contains neither; it carries only the `generate doc|config` subcommand name
  (`:340`). The `§5` half is unsupported.
- `:623` "every `/etc/xdg/walker/config.toml` line anchor (**§2.1-2.4, §4.2, §7.4**)".
  §7.4's only anchor is the **user** file, `:47-49` (`walker-deep.md:475-477`); packaged
  anchors also sit at §3 `:156`, §4.3 `:266` and §9 `:514` (also treated as packaged
  anchors by `DeltaWalkerConfig.md:121`). The list over-includes §7.4 and omits three
  sections that do carry `/etc/xdg` anchors.

## (d) Do the cited S-rows support their sentences? — yes, with one self-contradiction

| Citation | Row | Supports? |
|---|---|---|
| `S090` at `pacman.log:2929` and "(line 3095)" | `corpus/SOURCES.md:102` — 2929 walker 2.17.0→2.17.2, 3095 elephant 2.21.0→2.22.1 | yes, both clauses |
| `S096` for the `2.17.2` binary literal | `SOURCES.md:108` — literal `2.17.2\n` at file offset 856,302 | yes |
| `S091` for `13,743 B` / `3c5c6867d0216d0c` | `SOURCES.md:103` — `/etc/xdg` 13,743 B sha `3c5c6867…`, user 1,336 B `fecf71fa…` | yes for the L1-superseded clause; **the same row also records "embedded default at offset 806960", contradicting `:623`'s "not re-run"** |
| `S073` for "upstream v2.17.2 default" | `SOURCES.md:85` — `resources/config.toml @ v2.17.2`, 13,743 B, sha `3c5c6867…` byte-equal to host | yes |

All four rows exist (no dangling id), all are tier A / `mined` / `2026-10-20`, and all
four route to `corpus/knowledge/walker-route-r18.md` (last column), consistent with
`:622`'s "Current routing" pointer. The 2.17.1-vs-2.17.2 attribution is cited by report
name, not S-row, and `DeltaWalkerConfig.md:51-53` supports it (all four semantic changes
land in 2.17.1; 2.17.2 changes only the `blur_corner_radius` comment).

## Verdict

**breaks.** (a) clean, (d) clean, (c) partly wrong. The block fails on its central
function: `:623` asserts three measurement families were "not re-run on 2.17.2" when the
round re-ran all three and recorded new values (embedded default @806,960 equal to the
packaged file; `struct Walker with 31 elements`; a full line-anchor map). The sentence is
refuted by `S091` — cited in the same bullet — and by `walker-route-r18.md:206, :244`,
the routing doc named one line above. A reader is told the opposite of the round's
evidence. The mechanical append, the version/file pins, the elephant pin and the
`[UNK]` behaviour line all hold.

## Limits

- Host pause honoured: no walker/elephant/pacman/systemctl/journalctl/hyprctl execution;
  all host reads were file bytes (`sha256sum`, `stat`, `wc`, `sed`, `grep`, `python3 open`).
  No live fact was tested, so nothing here speaks to 2.17.2 runtime behaviour.
- Upstream tag bodies were not re-fetched; I used the round-19 w1 reports and their
  recorded receipts for the 2.17.0/2.17.2 config and CLI deltas.
- I did not re-measure the note's elephant user TOMLs, menu Lua or omarchy script anchors;
  their "still dated" classification in `:625` is neither confirmed nor refuted here.
- Whether "not re-run" was intended as "the note text was not refreshed" is a reading;
  the sentence's literal subject is the measurements, and the receipts show they ran.
  [INFERENCE] the clause predates the added `S091`/`S096` citations (committed tip ≠ w1
  after-state, `PtrWalkerDeep.md:11`).
- No git/jj writes in the lane; the two blobs were materialised under /tmp only.

## Installs

none.
