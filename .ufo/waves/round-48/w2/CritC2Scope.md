# CritC2Scope — falsify that the C2 source/entry is new and within mado (round 48, w2)

Seat: `CritC2Scope` (leaf; no subagent dispatch). Date 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Candidate = the freeze's draft/integration bytes
(`.ufo/waves/round-48/l1-draft/xkb-keymap-compile-r48.md`, `rows-c2.md`, `readme-row.md`) and the L1 working-tree
overlay of `corpus/SOURCES.md` + `corpus/README.md`. Frozen predicate `quality/counters/c2-r48-xkb-entry.py`
(`PRED-C2-r48`). Every read was revision-addressed; no lane tracked file was written.

## Verdict

| question | verdict |
|---|---|
| Is the C2 entry new ground at BASE? | **CONFIRMED** — entry absent; all four frozen `GROUND` terms absent (exit-1 grep); the entry's only new host digest is absent at BASE; the frozen counter's clause `i` reports `all_absent_at_base=1 present_at_rev=3/4`. |
| Is it new *semantically*, not just by the four-term census? | Narrowly. 13 of the entry's own domain terms already exist at BASE, including `kb_layout` in 12 corpus files. The novelty is the libxkbcommon/xkeyboard-config compile layer, which no corpus line answers. Declared residual ("clause i is a term census, not a semantic novelty proof"); not a miss. |
| Does it re-claim the held r46 entry? | **No.** One identical sentence out of 114 (a markdown table header); every sentence naming Hyprland/the compositor carries held attribution (S318/S319, r46 step 4, or a `[UNK]` limit). Two low-severity precision notes below; neither is a claim of newness. |
| Is it within mado? | **Yes** for the plane: `PROVINCE.md:102-114` owns the `input { kb_* }` / `device` plane at the resolution Hyprland gives it, and the compile is that resolution. No sibling lane claims XKB compile ground (re-verified, 0 hits). Two boundary findings below (PROVINCE authority line absent; a shokuknow id-namespace contention). |
| Frozen-predicate defect on this axis? | **None found.** `PRED-C2-r48` admits both candidate forms `TARGET_MET`; clause `r` independently reproduced the positive keymap digest and the `(1,1,0)` negative rcs. |

No miss is claimed by this seat; the predicate was not narrowed and nothing frozen was changed.

## 1. Ground terms at BASE

`git grep -c -F -- <term> 579f694b -- corpus` (full table: `receipts/ground-census-base.txt`):

```
xkb_keymap_new_from_names    0 NONE            RMLVO                    0 NONE
XKB-595                      0 NONE            KcCGST                   0 NONE
compile-keymap               0 NONE            include path             0 NONE
xkeyboard-config-2.48        0 NONE            rules/evdev              0 NONE
xkbcli                       0 NONE            XKB_DEFAULT              0 NONE
kb_layout                   12 README.md,knowledge/{arc-synthesis,config-drift-r12,config-health-report-r3,
                                 config-option-table-r39,executor-test-sufficiency,hyprctl-getoption-native-forms-r40,
                                 hyprctl-verification-layer,hyprland-config-plane,hyprland-input-devices-r46}.md,
                                 lessons/{round-46,round-46-verifier-spotcheck}.md
kb_rules 3 / kb_variant 3 / kb_model 3        config-health-report-r3.md, hyprctl-verification-layer.md,
                                              hyprland-input-devices-r46.md
kb_options                   5                + hyprctl-getoption-native-forms-r40.md, lessons/round-46-verifier-spotcheck.md
xkbcommon                    1                corpus/SOURCES.md only (S008's Wayland-book cell, not a compile row)
keymap                       8                same corpus files, observational only
```

The four `GROUND` terms are genuinely absent, so clause `i` holds. The entry's *subject vocabulary* is not absent:
`kb_*` is held r46 ground and appears in at least four earlier entries. The entry says so itself (line 16 ground
line, `## Limits`), so the narrow census is disclosed, not hidden.

## 2. Held S318/S319 and PROVINCE

- `corpus/SOURCES.md:267` **S318** scope: "Defaults of the global keyboard names and of the global scroll factor";
  `:268` **S319** scope: "What a keyboard stores as its current rules and what happens when they do not compile".
  Both byte-equal at candidate (line-level sha compare, `receipts/c2-draft.log` clause `h:1`), and the r46 entry blob
  is identical (`eccd79a0…` at BASE and at both candidate commits).
- `corpus/knowledge/hyprland-input-devices-r46.md:69` at BASE is exactly the quoted gap (`- The XKB compile itself is
  not reproduced: …`); `corpus/README.md:112` (the Round-46 Frontier bullet) contains exactly `Still open: the XKB
  compile itself (whether a layout/variant pair exists in xkeyboard-config)`. Both self-document locators in the
  entry's `ground:` line are therefore true at BASE.
- `PROVINCE.md:102-114` (same bytes at BASE and in the working tree) owns "the input-device plane of the owned config
  tree — the `input` block's `kb_layout`, `kb_variant`, `kb_options`, `kb_model`, `kb_rules`, `kb_file` keys … at the
  resolution Hyprland 0.56.2 gives it". The compile is that resolution, so C2 is inside the declared plane. PROVINCE
  has **no round-48 line**: the new authority (libxkbcommon 1.13.2 / xkeyboard-config 2.48) is named by the entry and
  its rows, not by PROVINCE. Documentation gap, not a claim breach (`w1/ConnSiblings` proposed such a line; it is not
  installed).

## 3. Re-claim analysis against the held r46 entry

Sentence-level comparison (backticks normalised, `receipts/reclaim-analysis.txt`):

```
sentences(new)=114  sentences(old)=86  exact identical=1 (| question | where the answer lives | state |)
8-word shingle overlap >=2 pairs = 1 (the same table header)
```

Every compositor-facing sentence is attributed:

| entry line | sentence | attribution |
|---|---|---|
| 16 | "held open at base … held neighbours: rows S318/S319 give the compositor's `us` default and its fallback … cited here and never re-claimed" | S318/S319 |
| 31 | "whether the compositor's own context honours `XKB_DEFAULT_*` … sourced (held row S319, its context line); not run against the live compositor" | S319 |
| 35 | "Hyprland builds every keyboard keymap in a context made with `XKB_CONTEXT_NO_FLAGS` (Hyprland-IKeyboard.cpp:75, held row S319)" | S319 pin; this flag/C-string claim is **new** and r46 does not state it |
| 42 | "Hyprland starts from `us` … resets a keyboard … (S318 … S319 …) Both are held from round 46 … not re-measured here" | S318/S319 |
| 98 | failure table: "keyboard prints `us`, config says another layout → compile failed and the compositor reset it (step 8)" | indirect: step 8 carries S318/S319 |
| 109 | "The compositor half is held, not measured … whether any `XKB_DEFAULT_*` is set for it is [UNK]" | limits |
| 110 | "`kb_file` bypasses this whole chain … (round-46 step 4, held)" | r46 |

## 4. Live host run — every host claim checked read-only

`sha256sum` + `grep -n` (`receipts/host-claims-verified.txt`):

- `~/.config/hypr/input.conf` sha256 = `3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4`, with
  `10: kb_layout = br` and `11: kb_options = compose:caps` — matches entry line 73.
- `~/.local/share/omarchy/default/hypr/input.conf` sha256 = `bee5aa68…48b8`, `3: kb_layout = us` — matches.
- **Both hashes already exist at BASE**: `config-health-report-r3.md:638` and
  `hyprland-input-devices-r46.md:85-86` (the r46 erratum table). The only digest in the live-run section that is new is
  the keymap digest `efd487a39920…ce81` (`ABSENT_AT_BASE`, and clause `r` re-derived it live).
- Rows S346/S347 are host-anchored: `/usr/share/xkeyboard-config-2/rules/evdev` sha256 `0cc48ee1…2132` equals the S346
  digest and the committed fetch copy; `symbols/br` `8cf65550…` equals S347's digest.

## 5. Sibling connector verification (w1 `ConnSiblings`)

Re-ran its claims independently (`receipts/sibling-rescan.txt`):

- its pattern `xkb|keymap|kb_layout|rmlvo|kcgst|kb_rules|kb_model|kb_variant|kb_options` over the same 60 files
  (3 × 20 lanes): **0 hits** — the connector's number reproduces.
- wider terms `xkeyboard-config|libxkbcommon|xkbcommon|xkbcli|compile-keymap|RMLVO|KcCGST` over every `*.md` of the
  20 sibling lanes: **0 files**. Control with the lane included returns 182 files, all under `mado-shokunin` — the glob
  `*-shokunin` also matches the lane itself, so a scan that forgets to exclude it reads as a false hit (worth knowing if
  another seat repeats it).
- The connector's scan **did not cover `/home/vgpnk/Projects/shokuknow`**; its "Contested scope: None" is scoped to the
  20 lanes only.

## 6. shokuknow — no compile ground, but an id-namespace contention

- No knowledge claim: `compile-keymap`, `XKB-595`, `RMLVO`, `KcCGST` → 0 files under `.ufo` and `lanes`;
  `lanes/mado` non-fetch markdown mentions no xkb/keymap; `xkeyboard-config` hits only two
  `.ufo/waves/corpus-expansion-1/.qcache` blobs (OS release-notes JSON), and the `kb_layout` qcache hits are raw HTML
  wiki pages — ring caches, not published claims.
- `lanes/mado/*/fetch/` holds upstream Hyprland IPC/wiki copies that mention `active_keymap`/`switchxkblayout`/
  `kb_layout` (`lanes/mado/round4/fetch/chonk-ipc.md:97-98,204`, `round8/fetch/chonkstep-hyprland-ipc.md:97-98,204`,
  `round16/fetch/cachyos-zh-hyprland.md:239`) — mirror bytes, no compile ground.
- **Contention (paths/lines):** `lanes/mado/ID-REMAP.md:6-8` renumbers 147 staged rows so that "first staged id is now
  **S203**" on the premise "lane registry ends at S202"; `:67-76` then maps round15/16 proposals onto **S340-S349**, and
  `round15/SOURCES-PROPOSED.md:21` gives `S340` to "host waybar configuration backups …", `round16/SOURCES-PROPOSED.md:20-22`
  gives `S347-S349` to Japanese/Chinese Hyprland guides and the wiki bind-flags page. Round 48 opens S340-S350. The
  remap's premise is stale (lane registry is at S339), so the block is named by two surfaces. Full receipt:
  `receipts/id-contention.txt`.

## 7. Frozen predicate at the candidate (independent replay)

Built two candidate commits in a bare shared scratch clone by tree surgery (no work-tree index: the lane index is 2.7 MB,
above the 1 MiB/file seat guard) — `cand-draft` `ef9e11e5…` overlays `l1-draft/rows-c2.md` + `readme-row.md` on BASE bytes;
`cand-wt` `9cb652a1…` uses the L1 working-tree `corpus/SOURCES.md` + `corpus/README.md` (which already carry the rows and an
extra Frontier bullet). Both trees also add `.ufo/waves/round-48/{fetch,receipts,tools}`.

`TMPDIR=<seat scratch>/replay python3 -I quality/counters/c2-r48-xkb-entry.py --repo <clone> --rev <cand>`:

```
cand-draft: clause=c id=S350 pins=xkbcli-compile-keymap-r48.txt digests=1 ranges=0
            clause=h held=S318,S319 unchanged=1 pins=2 ; quotes=18 ; steps=9 pin_cited=9
            clause=f receipt=…xkbcli-compile-keymap-r48.txt version=1.13.2 sha=efd487a39920 probes=3
            clause=i all_absent_at_base=1 present_at_rev=3/4
            clause=r replay=ok sha=efd487a39920 neg=(1,1,0) ver=1.13.2
            clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1
            PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=ef9e11e5…
cand-wt:    same clause lines, admitted=1/1 TARGET_MET rev=9cb652a1…
```

So the receipt replay, the negative-probe rcs and the positive digest are reproducible on this host; no clause failed.

## Findings and disposition

- **F1 — clause `d` never sees the entry's two self-document locators (residual verified, no defect).** In the entry's
  `ground:` line the locator precedes the quoted span (`` `…r46.md:69` ("The XKB compile itself is not reproduced") ``),
  while clause `d` only matches a span *followed by* a locator, and refuses lane-document locators anyway. I verified both
  by hand (section 2). The "held open at BASE" premise is true; the counter simply cannot confirm it.
- **F2 — shokuknow id-namespace contention on S340-S349 (boundary, routed to the L1).** Section 6. Not a predicate
  break: the lane registry's max id at BASE is `S339`, the 11 rows are unique, and `PRED-C2-r48` does not read shokuknow.
  Risk: when the corpus-expansion campaign lands its 147 staged rows, S340-S349 collide with this round's rows. Suggested
  routed item: one lesson line naming the contention plus a renumber of the staged rows against the round-48 allocation
  before adoption (an L1/lesson decision; this seat may not re-register or renumber).
- **F3 — live-run host identity is inherited, attributed only for the file order (precision, low).** Entry line 73
  restates the two config-file digests and the `br`/`compose:caps`/`us` names that BASE already publishes at
  `hyprland-input-devices-r46.md:85-86` and `config-health-report-r3.md:638`, under a "Live host run" heading; it cites
  only "the file order recorded in the round-46 erratum". Both hashes are true on the host today, and the genuinely new
  measurement (keymap digest, rc, KcCGST) is correct. A locator on the inherited pair would remove the appearance of a
  new measurement.
- **F4 — the failure-table row restates the held fallback with indirect attribution (precision, low).** Line 98's
  "compile failed and the compositor reset it" is r46 step 4's diagnosis; it points at step 8, which carries S318/S319.
  No newness is claimed; an inline `(S318/S319)` would make it self-attributing.
- **F5 — PROVINCE has no round-48 line (documentation, not a claim).** Section 2. The plane is declared; the new
  resolution authority is not.
- **F6 — S346 is a host package-file pin with an upstream `rules.in` URL (note).** Its digest is the host's installed
  `rules/evdev` (`0cc48ee1…`), reproducible here; the generated-from-`rules.in` provenance is the generated-evidence
  seat's axis, not this one. No scope effect.

## Evidence retained (seat dir `.ufo/waves/round-48/w2/CritC2Scope/`)

- `receipts/ground-census-base.txt` — the 17-term BASE census with file paths, held-row and PROVINCE locators.
- `receipts/reclaim-analysis.txt` — sentence/shingle overlap and every compositor sentence with its line number.
- `receipts/host-claims-verified.txt` — host sha256/lines, the BASE occurrences of the inherited hashes, `ABSENT_AT_BASE`
  for the keymap digest, the two package-file digests.
- `receipts/sibling-rescan.txt` — the connector re-run, the wider-term scan excluding the lane, the glob control, and the
  shokuknow scan.
- `receipts/id-contention.txt` — ID-REMAP and proposal lines quoted.
- `receipts/c2-draft.log`, `receipts/c2-wt.log` — the frozen counter's full output for both candidates.
- `receipts/build-draft.log`, `receipts/build-wt.log` — candidate commit hashes.

## Bounds, host guard and cleanup

- Scratch: `/fast/scratch/hyaku/mado-r48/CritC2Scope/` — 576 KB total, largest file 116 074 B (a git object in the bare
  clone); workspace removed after copying the receipts (`trap` not needed; removal explicit). Every writer shell began
  with `ulimit -f 2048`.
- Candidate commits were made only inside a bare `--shared` clone under scratch; `git rev-parse --is-bare-repository` was
  checked before any tree write; commit identity was `-c user.name=t -c user.email=t@t`. No `git`/`jj` mutation, no
  commit, no push in the lane; no tracked lane file edited.
- **Disclosure:** one early command staged the BASE `corpus/SOURCES.md`/`README.md` bytes as hidden files inside the lane's
  `.ufo/waves/round-48/l1-draft/` (`.base-corpus_SOURCES.md`, `.base-corpus_README.md`, 241 766 B / 71 221 B). I removed
  both immediately and rebuilt the overlay from `git show` instead; `ls -a l1-draft | grep base` now prints nothing. No
  draft byte was modified.
- Tools: no install or update; pacman untouched (host-wide pause honoured). Read-only host verbs used: `xkbcli --version`,
  the counter's `xkbcli compile-keymap` replay (clause `r`), `sha256sum`, `grep` on `~/.config/hypr/input.conf` and the
  omarchy default. No compositor/service mutation, no input injection, no GUI, no `xdg-terminal-exec`.
- No serials, window titles, process tables or home listings were printed.
