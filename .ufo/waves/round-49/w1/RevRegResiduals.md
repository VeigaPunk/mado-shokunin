# RevRegResiduals — round-48 registration-v2 residuals (final)

Seat: RevRegResiduals (round-49 w1, BUILD). Target: the two residuals declared at
`.ufo/waves/round-48/registration-v2.md:105-107`, verified at base 03e4ae76aff7a4be59cb69970dd553baa319695a
(routed from `corpus/lessons/round-48-verifier-spotcheck.md` §6 item 6). Full evidence chain and proposed fix
text: `.ufo/waves/round-49/w1/RevRegResiduals/review.md`.

## Findings

**R1 — receipt header misnames its generator: VERIFIED TRUE at base.**
`.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt:1` and its byte-copy
`.ufo/waves/round-48/fetch/xkbcli-compile-keymap-r48.txt:1` (blobs byte-identical, 14,270 B, sha256
`ab5fa97169306877aeb7218290d99cd4a410639c2833063ca357cb173dfa53cc`, computed) name
`generator .ufo/waves/round-48/receipts/make-xkb-receipt.sh` — a path that does not exist at base
(`receipts/` holds 139 files, all `.txt`/`.diff`). The real generator is
`.ufo/waves/round-48/tools/make-xkb-receipt.sh` (8,168 B, sha256
`42a50468fd211dc40bbf849bdd36577588144a2a60672173310a856adce42857`, computed), which emits the stale path
itself (`tools/make-xkb-receipt.sh:29`; its comment `:3` is stale the same way). The landed row S350
(`corpus/SOURCES.md:299`) already cites `tools/` correctly. Draft-only residue (no repair owed):
`l1-draft/make-rows.py:88`, `l1-draft/rows-c2.md:11`. Prior findings: w2/ConnSourceLinks #2 (:63-70),
RevXkbIntent LOW-1 (:17-20), SentHost F1 (:29-38), CritC2Pin F3 (:128). Locator warning:
`w2/RevXkbIntent.md:20` cites `tools/make-xkb-receipt.sh:12` for the `say` line; at base it is `:29`
(`w2/SentHost.md:34` is right). No predicate impact (counter clauses f/r never read the header's generator
path).

**R2 — `fetch/xkbcommon-meson.build` is a pin no row cites: VERIFIED TRUE at base.**
The pin is in the freeze set (51,635 B, sha256
`48fc2de426bea1aa5d27d0c2a998e9962af2e1517d60599f64adc63b87a3f5da`, computed; matches
`w1/ScoutHyprKeymap/fetch/SHA256SUMS:9`, `w2/CritC2Pin/pins.txt:5`). Rows S340-S351
(`corpus/SOURCES.md:289-300`) pin exactly 14 of the 15 fetch files — this is the one uncited. Exact-name
`git grep 'xkbcommon-meson\.build' BASE -- corpus` → rc 1, no match (substring trap: `libxkbcommon-meson.build`
and `xkeyboard-config-rules-meson.build` contain it as a substring; the entry's only meson citations are
`xkbcommon-meson_options.txt` and `xkeyboard-config-rules-meson.build` — different files). The Gate doesn't
name it; the only l1-draft hit is the adversarial harness variant
(`l1-draft/v2/c2v2-harness-revc2counter.py:259,274`) that cites the pin precisely to prove clause d flags
uncited-pin quotes — a negative test, not a citation. The entry's recheck line
(`corpus/knowledge/xkb-keymap-compile-r48.md:16`) already counts "twelve upstream pins", excluding this pin —
the freeze is internally consistent about its deadness. No predicate impact: clause d
(`quality/counters/c2-r48-xkb-entry-v2.py:519`) fires only when the ENTRY cites an uncited pin. Nuance vs
ConnSourceLinks #5: the digest IS recorded in wave evidence (five files); "recorded nowhere" held only for the
counter-visible set. Prior findings: w2/CritC2Pin F5 (:130), w2/ConnSourceLinks #5 (:81).

## Proposed fixes (append-only; L1 lands them; this seat edited no frozen byte)

- R1: one errata line (exact text in review.md) naming both frozen receipt copies, the nonexistent path, the
  real generator with size+sha256, the self-emitting `say` at tools/make-xkb-receipt.sh:29, and that S350
  already cites `tools/`. Regeneration rejected (rewrites frozen bytes, changes the S350-pinned digest
  `ab5fa971…`); in-place header edit rejected (freeze); new row rejected (S350 already says it).
- R2: one errata line (exact text in review.md) declaring the pin retained-but-uncited with size+sha256 and
  the clause-d non-impact. Alternative if the L1 wants it load-bearing: a round-49 row (S352) citing the
  build-root facts (`meson.build:113-119`, `:179`, `:437`) — not minimal. Removal rejected (not append-only).
- Placement: either appended to `corpus/lessons/round-48.md` (spotcheck §6 convention) or a new
  `.ufo/waves/round-49/errata.md`; both lines are self-contained with digests. L1-only writes.

## Method / safety

All evidence via `git show`/`git grep -n` against base 03e4ae76 (lane HEAD moved to 5f37c1b8…, worktree dirty
with 50 porcelain entries — base blobs are the only clean ground); digests computed from base blobs; locators
grep-computed. No scratch dir needed (no clone/build/writer ran); no tools installed; no pacman; no
compositor/host mutation; no subagents. Writes: this Report file + the seat's review.md only.
