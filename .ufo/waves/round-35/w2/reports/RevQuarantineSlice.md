# RevQuarantineSlice — re-derivation of the mado slice, absent-defect register (round 35, wave 2)

Seat `L1Mado35.RevQuarantineSlice` (leaf reviewer, no dispatch). Read-only over
`/home/vgpnk/Projects/shokuknow` and the lane; all writes confined to
`.ufo/waves/round-35/scratch/RevQuarantineSlice/` and this file. Tooling installed: **none**
(pacman paused host-wide; no install was needed).

Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(375 lines, `wc -l` rc=0).
Re-run: `./reproduce.sh` in the scratch dir → `SCRIPT_RC=0`, output saved as `run.out`.

## Verdicts

| # | question | result | command / exit |
|---|---|---|---|
| V1 | Does the assigned command yield wave 1's 13 rows? | **YES — 13** | `awk ... {print $4,$5}` → 13 lines, `awk_exit=0` |
| V2 | Do the 13 split into two tables? | **YES — 6 + 7** | §1 data NR 141-146; §2 data NR 349-355; both filters rc=0 |
| V3 | Does any slice id collide with S203–S210 on a literal `comm`? | **YES, exactly two: S205, S209** | `comm -12` → 2 lines, `comm_exit=0` |
| V4 | Are those two collisions identity collisions? | **NO — different rounds, different documents** | content comparison §4 |
| V5 | Does a slice row enter the adopted band *after* packaging? | **YES, one: register S189 → packaged S206** | §5, 13/13 offset verified |
| V6 | Does wave 1's 13-row figure survive falsification? | **YES** — count, split, round mix all reproduce | §3 |
| V7 | Do wave 1's stated derivations reproduce their own tables? | **NO for ScoutQuar's stated awk** (`$4,$5` cannot print the columns it shows) | §3.1 |

## 1. Re-derivation

Assigned command (verbatim), rc=0, 13 data rows:

```
$ awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
    {print $4, $5}' $REG
 S189   `payload-absent`
 S195   `payload-absent`
 S201   `payload-absent`
 S205   `payload-absent`
 S224   `payload-absent`
 S228   `payload-absent`
 S199`   the cited source could not be fetched, so no quote was checked
 S200`   the cited source could not be fetched, so no quote was checked
 S209`   the gate block named no locator, so no quote was checked
 S222`   the gate block named no locator, so no quote was checked
 S223`   the gate block named no locator, so no quote was checked
 S225`   the gate block named no locator, so no quote was checked
 S235`   the gate block named no locator, so no quote was checked
awk_exit=0
```

**What the command actually prints** is `id, class` for §1 and `id, why-not-checked` for §2 —
`$4` is the id field in both tables; `$5` is `class` in §1 and `why` in §2. It prints no
cited source and no quoted text. This matters for V7 below.

Second, independent derivation (no round/id regexes at all) — every line whose lane cell is
exactly `` `mado` ``:

```
$ grep -c '^| `mado` |' $REG      # rc=0
14
$ grep -n '^| `mado` |' $REG | cut -d: -f1
141 142 143 144 145 146 248 349 350 351 352 353 354 355
```

14 = **13 data rows + the `## By lane` tally row at line 248** (`| `mado` | 6 |`). So no mado
row is missed by the assigned filter, and no extra row is invented.

## 2. Table split and denominators

| table | header | data rows (mado) | ids | register-wide data rows |
|---|---|---|---|---|
| § Rows (schema `lane \| round \| id \| class \| cited source \| quote(s) \| note`) | line 27 | **6** | S189 S195 S201 S205 S224 S228 | 194 (NR>27, NR<232) |
| § Rows whose quotes were NEVER CHECKED (schema `lane \| round \| id \| why \| cited source`) | line 265 | **7** | S199 S200 S209 S222 S223 S225 S235 | 109 (NR>266) |

- Share: 6/194 of §1 and 7/109 of §2.
- §1 class is `payload-absent` in all six (each `$5` is the literal `` `payload-absent` ``).
- §2 reason split: **2** "cited source could not be fetched" (S199, S200) + **5** "gate block
  named no locator" (S209, S222, S223, S225, S235).
- Round mix: r1×1, r2×4, r3×2, r4×4, r5×2 — rounds 1-5 only, none from 6-10 (the filter admits
  `round10`, and the independent grep confirms nothing beyond r5).
- The **stray trailing backtick** on all seven §2 ids (`S199\``, …) is in the register bytes,
  not an extraction artifact — same cosmetic defect as every §2 row of the register.
- **`## By lane` is §1-only**: it lists `| `mado` | 6 |` at line 248, and the whole tally column
  sums to **194** (rc=0), i.e. exactly the §1 row count. The tally understates mado by 7.

## 3. Against wave 1

### 3.1 ScoutQuar — count confirmed, derivation statement falsified

`ScoutQuar.md` states the derivation as `{print $4, $5}` and then presents columns
"cited source (locator)" and "quoted document". **Those are `$6` and `$7`, not `$4` and `$5`.**
Its tables are reproducible only with `$3,$4,$6,$7` (§1) and `$3,$4,$5,$6` (§2). The reported
count and split are right; the printed provenance is wrong, and the assignment text carries the
same wrong `print` clause.

Its statement "Locator named: 8 of 13 … Locator absent: 5 (S209, S222, S223, S225, S235)" is
true **of the register's cited-source cell** (`## Gate — Snnn`, a heading, not a locator) and
false **of the gate blocks**, which name concrete locators — verified in §6. It also correctly
flags that the register's own reason cell says "named no locator" (the register's claim, not
ScoutQuar's).

### 3.2 CritQuar — payload analysis confirmed on the two rows I re-checked byte-for-byte

- **S189 "escaping artifact" — CONFIRMED.** The lane's pinned byte copy
  `.ufo/waves/round-32/fetch/S189.bin` is 6479 B, `sha256 eea605dfe5ce09e1…` (prefix matches
  CritQuar). Line 128, `cat -A`:

  ```
  128:    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));$
  ```

  A real `\n` escape, real ASCII quotes. The register stores the same span double-escaped
  (`\\"` and `\\\\n`), so a literal search for the register bytes fails. `payload-absent` is a
  normalization artifact, not evidence of fabrication.
- **S228 curly-quote fold — CONFIRMED.** In
  `shokuknow/lanes/mado/round5/fetch/cn-export-hyprland.html` the full-width form
  `使用“模板:过时”标记的页面或章节` occurs **1** time (`grep -c` rc=0); the register's ASCII-quoted
  form occurs **0**.
- **S224 rotating timestamp — CONFIRMED.** `/home/vgpnk/.cache/ai-usage/status.json` exists
  (29759 B) and line 3 now reads `"updated_at": "2026-10-25T06:30:33Z"`; the register's
  `2026-10-23T22:52:44Z` is gone. Mutable-state staleness, not fabrication.

### 3.3 CritQuar citation error (correction, not a contradiction)

`CritQuar.md` chains "register `round2 S201` → `ID-REMAP.md:76` (`round2 | S201 | S212`)".
Line 76 of `ID-REMAP.md` is `| round16 | `S343` | `S349` |`, and **no `round2 S201` row exists**
in the map (its round2 band starts at `was = S206`). The correct chain is content-based and
verified: register r2 S201 (arxiv) → `round2/SOURCES-PROPOSED.md:69` S218 →
`merge/mado/SOURCES.append.md:22` S218. Conclusion unaffected; the citation is stale.

## 4. `comm` — slice ids vs the eight adopted ids

```
slice_ids = S189 S195 S199 S200 S201 S205 S209 S222 S223 S224 S225 S228 S235
adopted   = S203 S204 S205 S206 S207 S208 S209 S210
$ comm -12 slice_ids.txt adopted.txt     # comm_exit=0
S205
S209
$ comm -13 slice_ids.txt adopted.txt      # adopted, not in slice
S203 S204 S206 S207 S208 S210
```

**Two literal id collisions: S205 and S209.** Neither is an identity collision:

| id | register slice row | lane row S205/S209 (adopted) | same document? |
|---|---|---|---|
| S205 | r3 — ArchWiki interwiki-map JSON (`wiki.archlinux.org/api.php?…siprop=interwikimap`, register:144) | r35 own-work — host idle-lock chain, receipts `.ufo/waves/round-35/fetch/S205.receipt.txt` (`corpus/SOURCES.md:207`) | **no** |
| S209 | r3 — `## Gate — S209`, the compositor-log marker count (register:351) | r35 own-work — host waybar configuration backups (`corpus/SOURCES.md:211`) | **no** |

The lane ledger holds **200** unique ids, max **S210** (`sort|wc -l` rc=0), no internal
duplicates; the eight adopted ids are exactly rows 205-212. Outside the eight, the same ledger
also numerically collides with two other slice ids — **S189** (lane row cites the *same*
EventManager URL as the register, so same source, opposite verdict) and **S201** (lane =
Waybar `backend.cpp`; register = arxiv 2604.18860 — different source). Those two are not part
of this wave's adoption set but they are the same defect class.

## 5. The collision surface `comm` under-reports: the +17 packaging map

The register's ids are not lane ids and not current proposal ids; they are an older numbering.
Under the campaign's own packaging, **every one of the 13 slice ids maps to packaged row
`id + 17`**, and at that id the packaged row names *the same document* — 13/13:

| register | packaged | packaged row (head, `merge/mado/SOURCES.append.md`) |
|---|---|---|
| S189 | S206 | Hyprland v0.56.2 event-socket implementation — EventManager.cpp |
| S195 | S212 | Arch Linux 中文维基 — Hyprland (简体中文) — SJTU pkg |
| S199 | S216 | CSDN 2301_76324845 |
| S200 | S217 | CSDN lxyoucan |
| S201 | S218 | Temporal UI State Inconsistency … arXiv:2604.18860 |
| S205 | S222 | ArchWiki interwiki map (siteinfo) |
| S209 | S226 | host compositor log bytes (`…/hyprland.log`) |
| S222 | S239 | host gkeep producer shim |
| S223 | S240 | host AI-usage producer |
| S224 | S241 | host AI-usage cache |
| S225 | S242 | host compositor journal |
| S228 | S245 | Chinese ArchWiki export |
| S235 | S252 | host compositor socket directory |

`[INFERENCE]` The constant +17 is an empirical bijection over 13/13 rows, not a documented
offset — no doc I read states it. But it is strong enough to answer the adoption question:

**Exactly one slice row lands inside the adopted band after packaging: register S189 → packaged
S206.** The lane's adopted S206 is the waybar `config.jsonc`. So the band is occupied downstream
by a *different* document than the wave adopted, and the literal `comm` count of 2 is a lower
bound on the collision surface, not the whole story. At the band level the occupancy is total:
the peer report `w2/reports/RevCollision.md` V1 measures **8/8** collisions between the lane's
S203–S210 and the packaged S203–S210.

None of the 13 slice rows resolves to *any* of the eight adopted ids as the same document. So:
**numeric collisions with the adopted set: 2. Identity collisions with the adopted set: 0.
Band occlusion introduced by packaging: 1 slice row (S189→S206), inside a band that is
otherwise occluded 8/8 by other packaged rows.**

## 6. The register's own §2 reason cells are false as stated

Each of the five "the gate block named no locator" rows has a gate block that **does** name a
concrete locator. Verified at the current proposal ids (register + 17), each with a `- URL:`
line:

| register row | gate block | locator line |
|---|---|---|
| r3 S209 | `round3/SOURCES-PROPOSED.md:76` `## Gate — S226` | `:77 - URL: /run/user/1000/hypr/efb50993…/hyprland.log` |
| r4 S222 | `round4/SOURCES-PROPOSED.md:77` `## Gate — S239` | `:78 - URL: /home/vgpnk/.local/bin/gkeep` |
| r4 S223 | `round4/SOURCES-PROPOSED.md:83` `## Gate — S240` | `:84 - URL: /home/vgpnk/.local/bin/ai-usage` |
| r4 S225 | `round4/SOURCES-PROPOSED.md:95` `## Gate — S242` | `:96 - URL: journalctl --user -u wayland-wm@hyprland.desktop.service` |
| r5 S235 | `round5/SOURCES-PROPOSED.md:71` `## Gate — S252` | `:72 - URL: /run/user/1000/hypr/efb50993…/` |

The reason cell is therefore a **cell-format artifact**: the register stored the gate heading
(`## Gate — Snnn`), which is not itself a locator, and the checker never resolved the heading to
its block. The register's §2 text — "the gate block named no locator" — is factually wrong for
5/5 mado gate rows; the identical claim is made register-wide (all lanes), so this is a
register-level defect, not a mado quirk. `CritQuar` reached the same conclusion; `ScoutQuar`'s
"No" is correct only about the stored cell.

Corroborating detail: `round3:80` records `zero occurrences of "overflowed event queue" in
942548 B / 6425 lines`, which is exactly the claim `CritQuar` attributes to register S209.

## 7. Unresolved / limits

- The **causal** origin of the +17 offset is not documented anywhere I read, and
  `ID-REMAP.md` does not encode it. Tested per pair
  (`grep -cE "^\\| round$R \\| \`$ID\` \\|"`, rc=0 for all 13):
  **none of the 13 slice `(round, id)` pairs appears in the map at all** — `was_in_remap=0` for
  every row. The bare *numbers* do occur in the map's `was` column, but under other rounds
  (`round1 \`S205\`` → S211, `round2 \`S209\`` → S215), which is exactly the round-scoping
  ambiguity `ID-REMAP.md:9` warns about: a round-blind substitution would move citations onto
  unrelated rows. The map's `was` band also numerically overlaps the package's final ids
  (`round5 \`S239\` → \`S245\`` in the map, while `merge/mado/SOURCES.append.md` holds
  S239 = gkeep and S245 = cn-export), so a bare number is ambiguous across the streams even
  inside the campaign — which is why `id + 17` must be stated as a content match, not a
  substitution. Treat it as a **measured bijection over this slice**, not as a mechanism.
- I did not re-fetch any network source; all payload verification used lane byte copies. S199/
  S200 remote reachability is CritQuar's measurement, not mine.
- I did not evaluate whether adopting the slice is *right* (that was wave 1's CritQuar and is
  the round-34 gate's call); this seat only re-derives the slice and tests the collision claim.

## 8. Artifacts

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/scratch/RevQuarantineSlice/`:
`reproduce.sh` (rc=0), `run.out`, `slice.raw.txt`, `t1.txt`, `t2.txt`, `slice_ids.txt`,
`adopted.txt`, `comm12.txt`.
