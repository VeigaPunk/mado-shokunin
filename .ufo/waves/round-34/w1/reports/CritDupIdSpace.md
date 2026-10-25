# CritDupIdSpace — round-34 wave-1 critic report

**Verdict: the register does not use the lane's id space.** The `mado` rows in
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
are keyed by the shokuknow campaign's **per-round, pre-remap staging ids** — the
numbers each campaign round assigned in its own `lanes/mado/roundN/SOURCES-PROPOSED.md`
before packaging. They were never ids of `mado-shokunin/corpus/SOURCES.md`. The
lane's committed S201 (Waybar `backend.cpp`) cannot collide with a register row
inside this repo; a real duplicate-source collision does exist, but inside the
campaign's merge package, not the lane registry. No lane renumber is warranted.

## Which id space the register uses — evidence

1. **S189 URL check (the asked discriminator): yes, it matches — but the match is
   incidental.** Register `mado | round1 | S189` cites
   `raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/managers/EventManager.cpp`
   (register line 141); lane `corpus/SOURCES.md:201` S189 cites the same URL.
   Explanation: the campaign's round-1 staging restaged the same four sources the
   lane was committing, in the same order. `lanes/mado/SOURCES-PROPOSED.md`
   (post-remap) holds them as S197–S200 — S200 is the EventManager row
   (`SOURCES-PROPOSED.md:58`). Pre-remap those were S186–S189 (`ID-REMAP.md:13-16`),
   coinciding numerically with the lane's S186–S189 only because both streams
   appended from the same base in the same order. Two streams, one shared prefix.

2. **The arxiv row is provably absent from lane history.**
   `git -C mado-shokunin log -S'2604.18860' -- corpus/SOURCES.md` → empty (all
   branches). The worktree hits are confined to `.ufo/waves/round-32|33/` reports
   and scratch — staging evidence, never registry. The campaign's own round-2 doc
   corroborates: `lanes/mado/round2/SOURCES-PROPOSED.md:95` ran
   `grep -c 'arxiv.org/abs/2604.18860' corpus/SOURCES.md` → `0`.

3. **The register's disputed ids resolve cleanly through the campaign's own remap.**
   `lanes/mado/ID-REMAP.md` documents 140 staged rows renumbered at packaging so
   the first staged id became S197 against a lane registry that then "ends at
   S196" (`ID-REMAP.md:5-7`). Chain for the arxiv row:
   register `mado round2 S201` → `ID-REMAP.md:76` (`round2 | S201 | S212`) →
   `lanes/mado/round2/SOURCES-PROPOSED.md:69`: `| S212 | Temporal UI State
   Inconsistency in Desktop GUI Agents … — https://arxiv.org/abs/2604.18860`.
   Same for the other cited rows: register `round2 S195` → now S206 (archlinux-cn
   package), `round3 S205` → S216, `round4 S224` → S235, `round5 S228` → S239.
   Every register `mado` id + round pair maps to a packaged id; none maps to a
   lane registry row. The `round` column is part of the key — `ID-REMAP.md:9`
   warns the map is round-scoped precisely because the same bare id names
   different rows in different rounds.

## Can the lane's new S201 collide with a campaign row?

- **Inside this repo: no.** `corpus/SOURCES.md` has exactly one S201
   (Waybar `backend.cpp`, committed `fa7ba11`), and the arxiv URL never entered
   committed history (evidence above).
- **Inside the campaign merge package: yes, and it is already a duplicate —
   same id *and* same URL.** Packaged `lanes/mado/SOURCES-PROPOSED.md:67,76`
   holds S201 = Waybar `backend.cpp` and S202 = `window.cpp` — the exact sources
   the lane just committed. Its S197–S200 likewise duplicate lane S186–S189.
   The collision is therefore not a numbering dispute but two copies of the same
   six sources. The remap was computed against "registry ends at S196"
   (`ID-REMAP.md:5`); the registry now ends at S202, so the packaged block
   S197–S336 collides numerically across the board if merged verbatim and needs
   a second remap pass plus URL-dedup for S197–S202. That burden sits with the
   package, whose ID-REMAP mechanism exists for exactly this.

## Should the lane renumber in scratch?

**No.**

- S201/S202 are committed (`fa7ba11`). Renumbering committed registry rows is an
  append-only violation (history-pin) and would orphan `used-by` citations.
- The lane's own scratch already burned S201 once: round-32's quarantine slice
  staged the *same arxiv source* under label S201
  (`round-32/w1/reports/ExecQuarantineSlice.md:17`). That scratch label is frozen
  evidence — do not rewrite it; it means historical docs saying "S201" are
  ambiguous until resolved by (repo, round) — same ambiguity class the register
  exhibits.
- Scratch numbering should simply continue from committed max → S203+. The
  campaign's post-remap band S197–S336 lives in a different repo; the lane need
  not route its own counter around another project's package. ID-REMAP was
  designed so the *package* absorbs collisions at merge, not the lane.

## What a later adopter of the arxiv row would hit

1. **A pre-existing copy in the campaign package.** The row already exists as
   packaged S212 (`round2/SOURCES-PROPOSED.md:69`, tier B). Minting a fresh lane
   id for the same URL creates a second duplicate-source row pending at the next
   merge — same class as the S201/S202 waybar duplication already staged.
2. **An already-adjudicated defect, in both books.** The register's
   `payload-absent` flag on `mado round2 S201` and the lane's own round-32
   verdict name the same fault: the abstract page does not contain the quoted
   text; the quotes live in the full source
   (`ExecQuarantineSlice.md:17` — "PRESENT (adoptable, re-anchor)", quotes found
   in `lanes/mado/round8/fetch/arXiv-2604.18860.txt`; `ScoutQuarantine.md:67` —
   `arxiv.org/html/2604.18860v1` fulltext). Citation must anchor to the HTML/LaTeX
   fulltext, not `/abs/`. `CriticThemeScope.md:84` additionally refused the
   associated knowledge note as out-of-province — a content-scope objection a
   re-adopter must still answer.
3. **The id-renumbering hazard.** If adopted in the lane at any id in S203–S336,
   it numerically collides with a packaged campaign row at merge time
   (S203 = packaged Japanese ArchWiki, etc.), so its `used-by` citations ride the
   next remap. An id above the campaign's S336 ceiling is merge-proof; below it,
   adoption is still correct — the remap is the package's problem — but the
   adopter should cite the row by URL+commit, never bare "S2xx", in any
   cross-repo artifact.

**Bottom line:** two independent append streams share a numbering prefix through
S189 by coincidence of order, then diverge. The register speaks the campaign's
staging ids; the lane registry's S201/S202 are unambiguous inside this repo and
need no renumber. The real work item is on the merge side: the campaign package
duplicates lane S186–S189 and S201–S202 by URL, and its frozen remap base
("ends at S196") is already stale.
