# RevRegResiduals — round-48 registration-v2 residuals, verified at base 03e4ae76

Seat: RevRegResiduals (round-49 w1, BUILD wave). Target: the two residuals declared at
`.ufo/waves/round-48/registration-v2.md:105-107` — (R1) the C2 receipt header names its generator under
`receipts/` while the generator is committed under `tools/`; (R2) `fetch/xkbcommon-meson.build` is a pin no row
cites. Routed here from `corpus/lessons/round-48-verifier-spotcheck.md` §6 item 6 ("the `registration-v2.md`
residuals: receipt generator path and the uncited meson pin").

Method: every read below is `git show 03e4ae76aff7a4be59cb69970dd553baa319695a:<path>` or
`git grep -n <pattern> 03e4ae76aff7a4be59cb69970dd553baa319695a -- <path>` against the base commit. The lane
HEAD has already moved to 5f37c1b87b3ce5e438d19284e32b2e46fd548a92 and the worktree is dirty (50 porcelain
entries), so base-commit blobs are the only clean ground; working-tree files were not used as evidence. All
digests and sizes were computed from base blobs (hashlib sha256), not copied from receipts. Line locators are
computed by grep, never typed. No frozen byte was edited; this seat wrote only its own seat dir and the Report
file. No scratch dir was needed (no clone, build or writer command ran); no tools were installed.

---

## R1 — receipt header names its generator under `receipts/`; the generator is committed under `tools/`

Declared: `.ufo/waves/round-48/registration-v2.md:105-106` — "The receipt header names its generator under
`receipts/` while the generator is committed under `tools/` (frozen bytes; `w2/ConnSourceLinks` 2,
`RevXkbIntent` LOW-1, `SentHost` F1)".

**Verdict: TRUE at base.** Evidence chain:

1. The frozen receipt's first line names a nonexistent path:
   `.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt:1` =
   `# mado round 48 - read-only xkbcli compile-keymap receipt (C2), generator .ufo/waves/round-48/receipts/make-xkb-receipt.sh`
2. The freeze-set byte copy carries the same line:
   `.ufo/waves/round-48/fetch/xkbcli-compile-keymap-r48.txt:1` — the two blobs are byte-identical (both
   14,270 B, sha256 `ab5fa97169306877aeb7218290d99cd4a410639c2833063ca357cb173dfa53cc`, computed).
3. The named path does not exist at base: `git ls-tree -r --name-only BASE -- .ufo/waves/round-48/receipts`
   lists 139 files, every one `.txt` or `.diff` — no `make-xkb-receipt.sh` anywhere under `receipts/`.
4. The real generator is `.ufo/waves/round-48/tools/make-xkb-receipt.sh` — 8,168 B, sha256
   `42a50468fd211dc40bbf849bdd36577588144a2a60672173310a856adce42857` (computed from the base blob). It emits
   the stale path itself: the `say` at `tools/make-xkb-receipt.sh:29` writes exactly the wrong header text, and
   its comment at `:3` ("Writes receipts/xkbcli-compile-keymap-r48.txt next to this script") is stale the same
   way — the script writes `OUT="$HERE/xkbcli-compile-keymap-r48.txt"` (`:8`), i.e. next to itself.
5. The landed row is already correct: `corpus/SOURCES.md:299` (row S350) contains
   `generator .ufo/waves/round-48/tools/make-xkb-receipt.sh` (grep-verified at base). So the row cites `tools/`;
   only the frozen receipt header — and the generator's own `say` line — carry the stale `receipts/` path.
6. Draft residue, no repair owed: `.ufo/waves/round-48/l1-draft/make-rows.py:88` still emits the stale
   `receipts/` path and `.ufo/waves/round-48/l1-draft/rows-c2.md:11` still names it; the landed rows-c2 was
   hand-corrected at data commit (`w2/ConnSourceLinks/rows-gen-diff.txt:2,4` shows exactly this one-line
   difference). These are superseded drafts, not load-bearing bytes.
7. Prior findings agree: `w2/ConnSourceLinks.md:63-70` (finding 2), `w2/RevXkbIntent.md:17-20` (LOW-1),
   `w2/SentHost.md:29-38` (F1, incl. the mtime-order proof that the frozen generator bytes postdate the frozen
   receipt), `w2/CritC2Pin.md:128` (F3).

Locator-drift warning for anyone re-citing: `w2/RevXkbIntent.md:20` says the `say` line is at
`tools/make-xkb-receipt.sh:12`; at base it is at `:29` (`w2/SentHost.md:34` has it right). Do not copy `:12`.

Predicate impact: none. `quality/counters/c2-r48-xkb-entry-v2.py` clause f/r validate the receipt's content
(version, keymap digest, probes, replay) — none of them reads the header's generator path; clause d only
refuses quotes from uncited pins. This is provenance hygiene, exactly as declared ("frozen bytes").

**Proposed minimal append-only fix — one errata line** (L1 lands it; this seat edited nothing):

```markdown
- erratum (round-49 w1/RevRegResiduals, 2026-10-27): the frozen C2 receipt header misnames its generator —
  `.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt:1` and its byte-copy
  `.ufo/waves/round-48/fetch/xkbcli-compile-keymap-r48.txt:1` say
  `generator .ufo/waves/round-48/receipts/make-xkb-receipt.sh`, a path that does not exist at base 03e4ae76
  (receipts/ holds no .sh); the generator is `.ufo/waves/round-48/tools/make-xkb-receipt.sh` (8,168 B, sha256
  42a50468fd211dc40bbf849bdd36577588144a2a60672173310a856adce42857), which emits the stale path itself
  (tools/make-xkb-receipt.sh:29), so regenerating reproduces the same wrong header; row S350
  (corpus/SOURCES.md:299) already cites `tools/` correctly. Declared registration-v2.md:105-106; found by
  w2/ConnSourceLinks #2, RevXkbIntent LOW-1, SentHost F1, CritC2Pin F3.
```

Rejected alternatives: (a) regenerating the receipt with a corrected `say` line would rewrite frozen receipt
bytes and change the digest pinned in S350 (`ab5fa971…`), breaking clause c/f digest binding — not append-only;
(b) editing the header in place violates the round-48 freeze; (c) a new row would duplicate what S350 already
says correctly — a row is the wrong instrument for a one-token path correction.

---

## R2 — `fetch/xkbcommon-meson.build` is a pin no row cites

Declared: `.ufo/waves/round-48/registration-v2.md:106-107` — "`fetch/xkbcommon-meson.build` is a pin no row
cites (`CritC2Pin` F5)".

**Verdict: TRUE at base.** Evidence chain:

1. The pin is in the freeze set: `.ufo/waves/round-48/fetch/xkbcommon-meson.build` — 51,635 B, sha256
   `48fc2de426bea1aa5d27d0c2a998e9962af2e1517d60599f64adc63b87a3f5da` (computed from the base blob; matches
   `w1/ScoutHyprKeymap/fetch/SHA256SUMS:9` and `w2/CritC2Pin/pins.txt:5`).
2. No row cites it: the landed registry rows S340-S351 (`corpus/SOURCES.md:289-300`) name exactly 14 fetch
   pins — S340 `xkbcommon-rules.c`, S341 `xkbcommon-xkbcomp.c`, S342 `xkbcommon-include.c`, S343
   `xkbcommon-context.c`, S344 `xkbcommon-context-priv.c`, S345 `xkbcommon-meson_options.txt`, S346
   `xkeyboard-config-rules-evdev` + `xkeyboard-config-rules-rules.in` + `xkeyboard-config-rules-meson.build`,
   S347 `xkeyboard-config-symbols-br`, S348 `xkbcommon-tools-compile-keymap.c`, S349
   `xkbcommon-messages-codes.h`, S350 `xkbcli-compile-keymap-r48.txt`, S351 `xkbcommon-keymap.c`. The fetch
   set has 15 files, so exactly one is uncited — this one.
3. No entry text cites it: `git grep -n 'xkbcommon-meson\.build' BASE -- corpus` returns no match. The entry's
   only meson citations are `xkbcommon-meson_options.txt` (entry `:8`, `:60`) and
   `xkeyboard-config-rules-meson.build` (entry `:9`, `:16`, `:116`) — different files. Substring trap:
   `libxkbcommon-meson.build` (the w1/ScrRows pin, same digest `48fc2de4…`) and
   `xkeyboard-config-rules-meson.build` both contain `xkbcommon-meson.build` as a substring, so the exact-name
   grep is the only honest check; it is empty in `corpus/`. The Gate doesn't name it either (no
   `l1-draft/gate-rows.md` hit in the base-wide grep). The only l1-draft hit is
   `l1-draft/v2/c2v2-harness-revc2counter.py:259,274` — the adversarial variant that deliberately cites the
   uncited pin (`xkbcommon-meson.build:32`) to prove clause d flags exactly this defect; that is a negative
   test, not a citation.
4. The freeze is internally consistent about the pin's deadness: the entry's recheck line
   (`corpus/knowledge/xkb-keymap-compile-r48.md:16`) counts "the twelve upstream pins of S340-S349 and S351
   (nine libxkbcommon files, `rules/rules.in`, `rules/meson.build`, `symbols/br`)" — the count already excludes
   the top-level meson.build. (ConnSourceLinks #3's stale "nine" was repaired at data commit; the landed entry
   says "twelve".)
5. Counter impact: none. `quality/counters/c2-r48-xkb-entry-v2.py` clause d fires `pin_not_cited_by_row`
   (`:519`) only when the ENTRY cites a pin that no row cites; the dead pin is not cited by the entry, so it
   cannot trip clause d, and clause c validates only pins cited by rows. Harmless to the predicate, as
   CritC2Pin F5 (`w2/CritC2Pin.md:130`) states.
6. What it would ground if it were load-bearing: libxkbcommon's top-level `meson.build` at tag
   xkbcommon-1.13.2 — `version: '1.13.2'` (`:4`), the `XKB_CONFIG_ROOT` resolution (`:113-119`),
   `DFLT_XKB_CONFIG_ROOT` (`:179`), `xkb_root=@XKB_CONFIG_ROOT@` (`:437`) — i.e. the build-time roots behind
   the default include path that S342/S343 ground only from `include.c`/`context.c`.
7. Nuance on ConnSourceLinks #5 (`w2/ConnSourceLinks.md:81`): "its digest is recorded nowhere" was true of the
   counter-visible set (rows/entry/receipt) but not of the wave evidence — the digest is recorded in
   `w1/ScoutHyprKeymap/fetch/SHA256SUMS:9`, `w2/CritC2Pin/pins.txt:5`, `w2/RevXkbIntent/pins.sha256:5`,
   `w2/ScoutFreezeBlobs/artifact-manifest.tsv:11` and `w2/RevC2Counter/provenance.txt:23`. The errata line
   below re-records it in the errata itself, closing that gap.

**Proposed minimal append-only fix — one errata line** (L1 lands it; this seat edited nothing):

```markdown
- erratum (round-49 w1/RevRegResiduals, 2026-10-27): `.ufo/waves/round-48/fetch/xkbcommon-meson.build`
  (51,635 B, sha256 48fc2de426bea1aa5d27d0c2a998e9962af2e1517d60599f64adc63b87a3f5da, libxkbcommon top-level
  meson.build @ tag xkbcommon-1.13.2) is retained in the round-48 freeze set but cited by no row or entry
  (rows S340-S351 pin 14 of the 15 fetch files; corpus/ has no exact `xkbcommon-meson.build` hit). It grounds
  nothing; clause d is unaffected (the entry cites no uncited pin). Declared registration-v2.md:106-107;
  found by w2/CritC2Pin F5, w2/ConnSourceLinks #5.
```

Alternative, only if the L1 wants the pin load-bearing: open a round-49 row (next free id — the registry tops
at S351, so S352) citing `fetch/xkbcommon-meson.build` with the build-root facts in item 6
(`meson.build:113-119`, `:179`, `:437`). That is a row plus entry touch — not minimal for a dead pin, and it
spends a round-49 row id on round-48 material. Removal from the fetch set is NOT append-only (rewrites frozen
round-48 bytes) — rejected.

---

## Placement of the errata lines

Both lines are self-contained (paths, digests, prior-finding ids), so they can land in either append-only
location the L1 owns: appended to `corpus/lessons/round-48.md` (the spotcheck §6 convention — N2/N3/N5 fixes
are "append a lesson line") or a new `.ufo/waves/round-49/errata.md`. This seat cannot write either; the L1 is
the only integrator. Nothing else in `registration-v2.md:105-110` is in this seat's target (S346 generator
chain, trust root, owner column, C1 judge — untouched, not verified here beyond reading the paragraph).

## Residual risk / verification gaps

- All evidence is base-commit ground; the current dirty worktree may differ (e.g. the L1 may already have
  landed repairs after 03e4ae76 — HEAD 5f37c1b8 was not audited for these two items).
- The errata text embeds digests computed from base blobs; if the L1 lands them, re-run the two sha256
  computations at the landing commit (one command each) rather than trusting this file.
- `w2/RevXkbIntent.md:20`'s `:12` locator drift is recorded here but not repaired anywhere (w2 reports are
  wave evidence, not frozen corpus bytes; no fix proposed).
