# ExecAssimIdGuard — round-41 w1, assimilation item 10 (id-collision guard)

Status: **complete**. Guard run, guard proved on an indented row, focus-theme id set and the
per-document renumber map produced. No repo file edited; nothing written outside the lane-side
assimilation directory, my seat report and one `/tmp` fixture dir (removed).

Full evidence: `.ufo/waves/round-41/assimilation/id-guard.md` (323 lines) plus
`.ufo/waves/round-41/assimilation/{reg-ids,staged-ids,collisions,focus-sources.txt,renumber-map.tsv}`
and `.ufo/waves/round-41/assimilation/proof/` (fixtures, id files, census transcripts, hashes).

## 1. Guard run (procedure verbatim, lane-side)

```bash
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mado/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

**reg=219 staged=147 coll=27.** `uniq -d` on each id file prints nothing (no duplicate ids on either
side). Extractor coverage is total: neither file holds a row at 4+ leading spaces
(`grep -cE '^ {4,}\|[[:space:]]*S[0-9]{3,}'` = 0 both), and the extracted counts equal the row counts
(219 / 147). Inputs: `corpus/SOURCES.md` sha256 `51a65515231b0a180f88c4fa1bc71482afa5f3eaeede4bdfbe6c4869493812ce`
(469 lines, 219 rows); `merge/mado/SOURCES.append.md` sha256
`684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0` (153 lines, 147 rows). Outputs:
`reg-ids` `744a9945…`, `staged-ids` `079d7538…`, `collisions` `aad91fd0…` (full hashes in `id-guard.md` §1).

- **reg-ids:** S001…S282, non-contiguous (S001–S189, S196, S201, S202, S203–S221, S253, S258, S277–S282).
- **staged-ids:** S203…S349, contiguous.
- **collisions (27):** `S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218
  S219 S220 S221 S253 S258 S277 S278 S279 S280 S281 S282`.

## 2. Guard proof (the guard can fail; the column-zero variant cannot)

- **F1 (required fixture):** scratch registry copy = contract header + Registry header + separator
  (`sed -n '1,12p' corpus/SOURCES.md`) plus ONE 2-space-indented `  | S002 |` row; staged copy holds
  `| S002 |` at column zero. The census accepts the indented row as a row
  (`file ok`, `census_exit=0`, `proof/f1-census.txt`). The specified 0–3-space pattern →
  `reg=1 staged=1 collisions=1 -> S002` (**nonempty**). The column-zero-only pattern →
  `reg=0 collisions=0` (**empty**). Fixture sha256 `93851bdb…` (registry), `dc7052c4…` (staged).
- **F3 (live-registry copy, new id):** `  | S900 |` inserted inside the real registry table (after line
  231): 0–3 pattern `reg=220` and `collisions=1 -> S900`; column-zero pattern `reg=219` and
  `collisions=0`. `comm -13` of the two id lists = `S900` exactly. Census on that copy adds no
  finding (`247 E11 / 1 W01 / 7 W04`, identical to the pristine registry's `247 E11` — all baseline).
- **F2 (validator cross-check):** the same injection with `S002` makes the census report
  `E03 S002 duplicate id`, i.e. the maintained parser also treats an indented row as a row — this is
  why F1, not F2, is the decisive fixture (the live copy still has the pre-existing column-zero S002).

Contract basis: `CORPUS.md:152-153` — the maintained census CLI "accepts 0–3 leading ASCII spaces before"
table rows, while the frozen manual examples assume column zero.

## 3. Focus theme — staged ids (31, from the twelve staged files' `source:` lines)

`S218 S227 S229 S230 S244 S273 S274 S275 S278 S279 S280 S288 S293 S294 S295 S296 S306 S307 S308 S313
S314 S317 S323 S324 S325 S328 S329 S330 S331 S332 S338`

- 31 source lines → 31 distinct ids (no id cited twice); the per-id `file:line` table in `id-guard.md`
  §6 was machine-checked against `focus-sources.txt` (31 rows, 0 mismatches).
- **Forced renumber (4):** `S218 S278 S279 S280` — in `collisions`.
- **Free in the lane today (27):** the rest — but identity adoption is *not* recommended (§4).
- All 31 staged rows exist in `SOURCES.append.md` and each row's `source` cell names the same document as
  the staged file's `source:` line (31/31 matched, 0 mismatched).

## 4. Renumber map — by DOCUMENT (URL → new id), never by arithmetic

22 distinct documents over the 31 rows (focus-grab XML cited 3×, `FocusGrab.cpp` 4×, `SeatManager.cpp`
3×, arXiv 2604.18860 3×). Registry tops at S282 → first free lane id S283; gaps below S282 are not
candidates (append-only, ids never reused). Assignment in first-appearance order:

| new id | document | from staged id(s) |
|---|---|---|
| S283 | github.com/hyprwm/Hyprland/issues/565 | S227 |
| S284 | raw …/hyprland-protocols/main/protocols/hyprland-focus-grab-v1.xml | S229, S274, S294 |
| S285 | amgsk.dev/posts/hyprland-rules/ (Japanese — **out of province**) | S230 |
| S286 | raw …/Hyprland/v0.56.2/src/protocols/FocusGrab.cpp | S273, S295, S308, S314 |
| S287 | lanes/mado/round8/fetch/host-focus-grab-and-timeout.txt | S275 |
| S288 | arxiv.org/abs/2604.18860 | S280, S325, S218 |
| S289 | quickshell.org/docs/v0.3.1/types/Quickshell.Hyprland/HyprlandFocusGrab/ | S288 |
| S290 | lanes/mado/round9/fetch/host-compositor-log-scan.txt | S293 |
| S291 | raw …/v0.56.2/src/protocols/FocusGrab.hpp | S296 |
| S292 | raw …/v0.56.2/src/managers/SeatManager.cpp | S306, S313, S317 |
| S293 | raw …/v0.56.2/src/managers/SeatManager.hpp | S307 |
| S294 | r.jina.ai/https://dfrws.org/…/Uncovering-Linux-desktop-espionage.pdf | S324 |
| S295 | lightning-assist.com/ja/blog/text-expander-wayland (Japanese — **out of province**) | S323 |
| S296 | lanes/mado/round14/fetch/host-focus-grab-portal-advertisement.txt | S328 |
| S297 | raw …/xdg-desktop-portal-hyprland/master/src/core/PortalManager.cpp | S329 |
| S298 | raw …/quickshell-master/src/wayland/hyprland/focus_grab/grab.cpp | S330 |
| S299 | raw …/hyprland-protocols/main/README.md | S331 |
| S300 | raw …/hyprland-protocols/main/protocols/hyprland-input-capture-v1.xml | S332 |
| S301 | lanes/mado/round15/fetch/host-focus-grab-client-sweep.txt | S338 |
| S302 | blog.ce9e.org/posts/2025-10-03-wayland-security/ | S244 |
| S303 | publications.mupuf.org/publication/2014/10/09/security-in-wayland-based-desktop-environments/ | S278 |
| S304 | api.archives-ouvertes.fr/search/?q=halId_s:hal-04806278&… | S279 |

Rules: the citation moves with the document (`old_id + offset` mis-points — map S288 is arXiv while
staged S288 is the Quickshell page; map S293 is `SeatManager.hpp` while staged S293 is the round-9 log);
duplicate citations collapse to one id per document; all 22 documents are absent from the lane (URL token
0 hits each; 26 theme tokens — `focus_grab`, `focus-grab`, `focus grab`, `hyprland-protocols`,
`quickshell`, `SeatManager.cpp`, `2604.18860`, … — all `grep -c -F` = 0), so no existing row can be
re-pointed; S230→S285 and S323→S295 are mapped but not citable (`PROVINCE.md:75`, localized channel).

## 5. Risks / notes for the integrator

1. **The new-id range overlaps the staged range** (S283–S304 ⊂ S203–S349). Not a lane collision — it is
   the staged package having reserved S203–S349 before this lane appended S278–S282. Re-run the guard at
   the append (`comm -12` vs `corpus/SOURCES.md`), not once at planning time.
2. **The staged set re-lists 27 lane ids**; a naive append of `SOURCES.append.md` as-is would produce 27
   duplicate-id rows. Only the map's per-document ids may be appended.
3. Two mapped documents are out-of-province; the successor entry must not cite them (registration §2b
   refusal target).
4. The lane registry is entirely column-zero today (`grep -cE '^ {1,3}\|' corpus/SOURCES.md` = 0), so the
   indented-row defect is latent, not present — which is why the proof is a fixture.

## 6. Bounds and tool state

- Wrote only: `$A/{reg-ids,staged-ids,collisions,focus-sources.txt,renumber-map.tsv,id-guard.md}`,
  `$A/proof/*`, this report, one `mktemp -d` under `/tmp` (removed; `ls` → "No such file or directory").
  No tracked file edited; no write into the shokuknow checkout; no git/jj command of any kind; no
  compositor/Wayland verb; no package transaction (pacman untouched); no subagent spawned.
- Tools installed: **none**. Used coreutils `grep`/`sort`/`comm`/`sha256sum`/`awk`, `python3`, and the
  repo's `scripts/sources-census.sh validate` (read-only).

Main agent checks to run: `sha256sum` of the three procedure outputs against `id-guard.md` §1, and the
census validator on the eventual append mirror (`assimilation/mirror-validate.sh`) once the rows land.
