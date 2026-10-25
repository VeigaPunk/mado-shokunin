# RevIdRemap — wave 2 falsification of the registration's package-id list

Seat: `L1Mado35.RevIdRemap` (leaf revenger). Round 35, wave 2.
Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only attack: no lane corpus file,
counter, control, `SOURCES.md`, registration, jj/Git state or `/home/vgpnk/Projects/shokuknow`
byte was modified. `shokuknow` was read with `GIT_OPTIONAL_LOCKS=0` + `git --no-optional-locks`
so not even its index was refreshed. Counters C1/C2 were not run — not this seat's slice.
Scratch evidence: `.ufo/waves/round-35/scratch/RevIdRemap/{verify_id_remap.py,verify_doc_identity.py,evidence.log}`.
No tool installed or upgraded.

## Verdict — the registration's list is **wrong**

`registration.md:124` claims: *"the package's own ids for the same documents (S309, S310, S321,
S329, S330, S331, S334, S336)"*.

Read against the package as it is staged today, **that list is wrong for 7 of the 8 documents,
and the 8th is a same-number/different-document collision, not a match.** The package's own ids
for the eight documents are:

```
S315  S316  S327  S335  S336  S337  S340  S342
```

The three staged entries say so themselves on their own `source:` lines, and the package's row
table says so independently in its `used-by` column. Both readings agree 8/8.

The list is not invented, and this matters for the campaign's reconciliation: it is exactly the
package's **pre-renumber staging ids** — the `was` column of the package's own
`/home/vgpnk/Projects/shokuknow/lanes/mado/ID-REMAP.md`. Every claimed id is displaced by a
uniform **+6**. So the registration recorded the staging-area ids and called them the package's,
against a renumbering that landed after it was frozen. Under the package's own vocabulary those
are two different id spaces, and the frozen sentence names the wrong one.

**One-line answer: wrong as written (it names the staging ids), with a uniform +6 correction to
`S315, S316, S327, S335, S336, S337, S340, S342`.**

## Axes attacked

- **A1 set identity** — is the claimed 8-set equal to the package's current 8-set?
- **A2 positional identity** — does position *k* of the claim correspond to lane `S203+k`?
- **A3 document identity** — does each id name the *same document* by path and by `used-by`, not merely the same number?
- **A4 provenance / versioning** — was the list ever true, and is the claim falsifiable as frozen?
- **A5 blast radius** — what happens to a naive cross-space substitution of these ids?

## A3 + A1 — the by-document map (package id → document → lane id)

Documents: `never-asked` = `corpus/knowledge/idle-lock-never-asked-r12.md`,
`chain-armed` = `idle-lock-chain-armed-r14.md`, `bar` = `idle-lock-offered-in-the-bar-r15.md`.

| # | package id (now) | package `was` | registration claims | document | lane id | document = live row? |
|---|---|---|---|---|---|---|
| 1 | `S315` | `S309` | `S309` | never-asked — `host-omarchy-first-run` | `S203` | ✅ |
| 2 | `S316` | `S310` | `S310` | never-asked — `host-idle-lock-never-asked` | `S204` | ✅ |
| 3 | `S327` | `S321` | `S321` | chain-armed — `host-idle-lock-chain-state` | `S205` | ✅ |
| 4 | `S335` | `S329` | `S329` | bar — `/home/vgpnk/.config/waybar/config.jsonc` | `S206` | ✅ |
| 5 | `S336` | `S330` | `S330` | bar — `…/waybar/indicators/idle.sh` | `S207` | ✅ |
| 6 | `S337` | `S331` | `S331` | bar — `…/omarchy/bin/omarchy-menu` | `S208` | ✅ |
| 7 | `S340` | `S334` | `S334` | bar — `host-waybar-dated-backups-sweep` | `S209` | ✅ |
| 8 | `S342` | `S336` | `S336` | bar — `host-omarchy-toggles-state-sweep` | `S210` | ✅ |

The lane ids are read from the lane entries' own `source:` lines
(`corpus/knowledge/idle-lock-never-asked-r12.md:7-8`, `idle-lock-chain-armed-r14.md:7`,
`idle-lock-offered-in-the-bar-r15.md:7-11`). The mapping is order-preserving and monotone in the
package (row indices 112, 113, 124, 132, 133, 134, 137, 139 from the append base) but **not**
offset-preserving: the lane renumbered eight interleaved rows into a contiguous block, so no
single arithmetic rule maps lane id to package id.

Document identity was checked by path, not by position — the package row for each id contains the
entry's own path token and names the entry in `used-by`:

```
python3 -I .ufo/waves/round-35/scratch/RevIdRemap/verify_doc_identity.py
→ triples from the three staged entries: 8
  … in row: True   row used-by names entry: True   (x8)
→ pairs checked: 8; failures: 0
→ verdict: DOC_IDENTITY_OK
EXIT=0
```

```
python3 -I .ufo/waves/round-35/scratch/RevIdRemap/verify_id_remap.py
→ append: merge/mado/SOURCES.append.md bytes=135617 sha256=684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0
→ rows=147 base=S203 tip=S349 contiguous=True
→ TRUE package id set (8): ['S315','S316','S327','S335','S336','S337','S340','S342']
→ set intersection = ['S336']  (|hit|=1/8)
→ positional matches = 0/8
→ verdict: ID_REMAP_WRONG
  - claimed set != true set
  - positional matches 0/8
EXIT=1
```

## What the claimed ids actually name in the package today

These are the package's **current** ids; every one of the eight claimed ids also survives as a
`now` value belonging to a *different* row (rows `S309`…`S336` are simultaneously `was` ids of
the eight and `now` ids of other rounds' rows — that is what makes the substitution dangerous):

| claimed id | live row it resolves to now | live line |
|---|---|---|
| `S309` | host systemd journal — hypridle start/stop lifecycle, r11 | 113 |
| `S310` | host gkeep rule file + selected path, r11 | 114 |
| `S321` | Hyprland ArchWiki (Chinese) wikitext, r13 | 125 |
| `S329` | xdg-desktop-portal-hyprland `PortalManager.cpp`, r14 | 133 |
| `S330` | Quickshell `focus_grab/grab.cpp`, r14 | 134 |
| `S331` | hyprland-protocols README, r14 | 135 |
| `S334` | Wayland vs X11 (Japanese article), r14 | 138 |
| `S336` | **waybar `idle.sh` indicator, r15** — one of the eight, but the wrong member | 140 |

So: seven claimed ids name documents that have nothing to do with the idle-lock surface. The
eighth, `S336`, is the trap the registration's own phrasing walks into — in the registration's
space `S336` means the toggle-state directory (now `S342`); in the package's space `S336` means
the indicator script. Same number, two documents, both inside this claim.

## A2 — positional reading: 0/8

Read as an ordered correspondence to the adopted lane block `S203…S210`, the claim is wrong in
every slot. Its last element `S336` should be `S342`; the row it names (`S336`) is the document
the claim's *sixth* element should name. A reader who indexes the list would mis-assign all eight.

## A4 — provenance: the list was true, then the package re-based

Last-known-good invariant reconstructed from three states of the same file:

`id = append_base + row_index`, and each document's `row_index` never changed.

| state | append base | rows | `host-omarchy-first-run` id | corroboration |
|---|---|---|---|---|
| git `HEAD` (blob `f7edd117e791fc2afdf24d3bac196f6c451b1dfd`) | `S186` | 114 | `S298` (index 112) | committed entry carried `source: S298` |
| pre-renumber (implied) | `S197` | 147 | `S309` (index 112) | **the registration's list** |
| live working tree (`sha256 684efe8c…`) | `S203` | 147 | `S315` (index 112) | staged entry `source: S315` |

Every one of the eight claimed ids implies the *same* base, which is what makes the reconstruction
non-coincidental rather than curve-fitting:

```
-- implied append base for each CLAIMED id (id - row_index) --
  S309 → 112 → S197   S310 → 113 → S197   S321 → 124 → S197   S329 → 132 → S197
  S330 → 133 → S197   S331 → 134 → S197   S334 → 137 → S197   S336 → 139 → S197
  implied bases: [197]
```

And the package states the renumber in its own words, with the mapping, in
`/home/vgpnk/Projects/shokuknow/lanes/mado/ID-REMAP.md`:

```
- lane registry ends at S202
- staged rows renumbered: 147
- first staged id is now S203

| round12 | `S309` | `S315` |      (ID-REMAP.md:42)   | round15 | `S329` | `S335` |  (:62)
| round12 | `S310` | `S316` |      (:43)               | round15 | `S330` | `S336` |  (:63)
| round14 | `S321` | `S327` |      (:54)               | round15 | `S331` | `S337` |  (:64)
                                                          | round15 | `S334` | `S340` |  (:67)
                                                          | round15 | `S336` | `S342` |  (:69)
```

`was` column for the eight == the claimed list, elementwise, and offsets are `[6,6,6,6,6,6,6,6]`:

```
python3 -I -  … (evidence.log E5/remap check)
→ remap rows 147
→ remap "was" column for the eight == CLAIMED list, elementwise: True
→ claimed set == {was of eight}: True
→ offsets: [6, 6, 6, 6, 6, 6, 6, 6]
EXIT=0
```

Event order (mtimes, all `2026-10-24`, `stat -c '%y  %n'`):

```
23:23:52  .ufo/waves/round-35/registration.md      ← frozen with the pre-renumber list
23:25:05  .ufo/waves/round-35/w1-spec.json        ← dispatch prompt repeats "starts at S197"
23:26:45  shokuknow/lanes/mado/ID-REMAP.md        ← renumber documented (+6)
23:33:20  shokuknow/merge/mado/SOURCES.append.md  ← append rebuilt, base S203
23:33:20  …/knowledge/corpus/knowledge/*.md       ← entries rewritten to S315…S342
```

`w1-spec.json:214` says *"the staged package starts at S197"*, which is the same stale base. **[INFERENCE]** the
registration read the append before 23:26:45; the intermediate bytes were not retained, so the
`S197` state is reconstructed from the uniform implied base plus that prompt, not read directly.
Confidence high — eight independent ids agree on the base and the package documents the renumber.

**The defect is therefore not arithmetic but unversioned citation.** The frozen sentence says "the
package's own ids" without naming a revision, blob or sha256. An id map that is true only of a
superseded file cannot be true or false as frozen — which is exactly how a uniform +6 slip
crossed the freeze unnoticed.

## A5 — blast radius: the lane block and the package block now collide

The renumber's stated purpose is "so that no staged id collides with an id the lane's own registry
already uses" (ID-REMAP.md:3), and it re-based the append to start at `S203` — the id immediately
after the lane's then-tail `S202`. This round then allocated `S203…S210` to the eight adopted rows.
Result: **lane `S203`–`S210` and package `S203`–`S210` are two different sets of rows.**

```
package now S203..S210 (was S197..S204, round 1):
  S203 Hyprland IPC page — current upstream source      S204 Hyprland IPC page 0.56.0
  S205 Hyprland wiki — Dispatchers (Lua config API)     S206 Hyprland v0.56.2 EventManager.cpp
  S207 Waybar 0.15.0 hyprland backend.cpp               S208 Waybar 0.15.0 window.cpp
  S209 Hyprland — Japanese ArchWiki                     S210 Fedora hyprland config (cnblogs)
lane S203..S210: the eight idle-lock rows (table above)
```

So a naive "the package already numbered these S203–S210" or a reverse lookup of the lane ids
against the package inverts **all eight**. The registration is right that the lane rows were
"re-pointed by document"; the hazard is that the document-keyed map it publishes is in the other
space, and the numeric bands overlap.

## Divergences found

- **D1 — stale by +6, uniform.** Claimed ids are the staging ids; package ids are staging+6. 7/8 misidentify in the live file.
- **D2 — same-number/different-document at `S336`.** Registration's `S336` = toggle-state dir (= `S342`); live `S336` = indicator script. The `1/8` set "hit" is a collision, not a confirmation.
- **D3 — cross-space collision band `S203`–`S210`** (lane idle-lock rows vs package round-1 IPC rows).
- **D4 — unversioned id map in a frozen claim.** No append revision or digest is pinned, so the claim cannot be scored as stated; it is only scoreable after choosing a package revision.

## Confidence

- Registration's list is **wrong against the live package**: certain. Two independent readings (entries' `source:` lines; rows' `used-by` column) agree 8/8, and 8/8 documents match by path.
- List is **exactly** the package's pre-renumber `was` set: certain (package's own remap table, elementwise, uniform +6).
- That the registration was frozen against a base-`S197` snapshot: high, `[INFERENCE]` on the unrecovered bytes; supported by mtime order, the dispatch prompt text, and the uniform implied base.
- Independent convergence: `w1/reports/ScribeRows.md:19` reached "wrong; only S336 coincides" before this seat. This seat's finding adds the mechanism (uniform +6, staging-vs-package id spaces) and the four-state invariant; it does not depend on that report.

## Limits / what was not done

- Registration was **not** edited (as instructed); neither were the counters, controls, `SOURCES.md`, the package, or any lane entry.
- C1/C2 were not executed — whether the adopted rows satisfy the frozen predicates is other seats' slice; nothing here affects the counters' verdicts, because the counters key on lane ids and paths, not on package ids.
- `shokuknow` git objects were read only (`git show HEAD:…`, `rev-parse`); no `jj` command was run, since any `jj` invocation would snapshot that repo.
