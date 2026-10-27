# w2 RevRoutes — separability review of the frozen C1/C2 predicates (round 48, wave w2)

Seat: RevRoutes (leaf, reviewer). Base/freeze `579f694b…` / freeze commit `3e6c848a` ("freeze v1").
Target: independent review of both claims' causal separability and weakest controls. Method: entry-only and
tool-only positive controls plus cheapest skip-work mutants, each scored by the frozen counters
(`quality/counters/c1-r48-terminal-cache.py`, `quality/counters/c2-r48-xkb-entry.py` at `3e6c848a`) on scratch
replay trees. No installs were performed (pacman paused; none needed). Every writer shell ran `ulimit -f 2048`;
largest output file produced: 77,187 B (`c1-entryonly.txt`); scratch peak 73 MB; scratch deleted after receipts
were copied to `w2/RevRoutes/`.

## Result matrix (all runs nonce=4848, TMPDIR and --work under /fast/scratch/hyaku/mado-r48/RevRoutes)

| Tree (scratch clone of `3e6c848a`) | tools/mado-terminal.py | C2 data (entry+rows+README row+receipt/pins) | C1 result | C2 result |
|---|---|---|---|---|
| `a` entry-only | BASE blob `ea4d4d7` | overlaid | **MISSED** `cold=190/190 warm=134/204 explained=231/394 generated=210/230 selftest=fail readonly=ok tool=present` exit 1 | **TARGET_MET admitted=1/1** exit 0, clauses `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1` |
| `b` tool-only | l1-draft tool | none | **TARGET_MET** exit 0: `cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present` (selftest `69/69`, clause=r `trips=0`) | **MISSED** exit 1, `clause=a entry_absent` |
| `m-base` (no data) | BASE | none | — (committed base receipt stands) | **MISSED**, `clause=a entry_absent` |
| `m-noreceipt` | BASE | yes, receipt removed | — | **MISSED**, `f:0 r:0` (`no_receipt_found`) |
| `m-noreadme` | BASE | yes, README row removed | — | **MISSED**, `g:0`, all others 1 |
| `m-both` | l1-draft | yes | — | **TARGET_MET** (both claims landed together; no interference) |
| `m-alwayscold` | l1-draft + `read_cache()` → `return "absent"` | none | **MISSED** exit 1: `warm=144/204 explained=240/394 selftest=fail readonly=ok` | — |

Evidence receipts (command, tree, full counter output) copied to `.ufo/waves/round-48/w2/RevRoutes/`:
`c1-toolonly.txt` `2b8861e9…`, `c1-entryonly.txt` `325a4e1b…`, `c1-alwayscold.txt` `7d97098b…`,
`c2-a.txt` `9c37e87e…`, `c2-b.txt` `2ca833d4…`, `c2-m-base.txt` `e48682fe…`, `c2-m-both.txt` `b811f101…`,
`c2-m-noreadme.txt` `6ddd8b12…`, `c2-m-noreceipt.txt` `983373d7…`.

## Findings by severity

### Critical / High
None. Both frozen predicates are causally separable in both directions, and every cheapest skip-work control
misses.

### Medium
None.

### Low
None.

### Notes / observations (no action required, recorded for the L1)

- **N1 — C1 is behaviorally blind to C2 data (strongest form measured).** The entry-only tree's C1 run
  (`c1-entryonly.txt`) reproduces the committed base-tool receipt `l1-c1-base-final.txt` number-for-number —
  `cold=190/190 warm=134/204 explained=231/394 generated=210/230 selftest=fail readonly=ok` — with the full C2
  data set present in the same tree. Landing C2 cannot carry any C1 clause.
- **N2 — C2 is blind to the tool, statically and behaviorally.** Zero `mado`/`tools/` references in the C2
  counter (case-sensitive grep: no matches); the tool-only tree misses C2 at `clause=a entry_absent`; the
  both-landed tree stays `TARGET_MET`. C2 clause `g` additionally refuses a README row naming another
  `knowledge/` file, so there is no index-level cross-credit either.
- **N3 — Static read-sets match the registration's separability sentences.** C1 counter reads only
  `tools/mado-terminal.py`, `quality/counters/c1-r47-fixtures.json` + `c1-r48-fixtures.json` (pinned by
  `SHA256_COLD`/`SHA256_WARM`), and `.ufo/waves/round-47/fetch/xdg-terminal-exec`; grep for
  `corpus|SOURCES|README|registry|xkb|knowledge` = no matches. C2 counter reads entry/SOURCES/README, round-48
  fetch/receipts and round-46 held fetch only; its only writes are `os.makedirs`/`shutil.rmtree` inside its own
  replay `mkdtemp` scratch (lines ~820-849).
- **N4 — Receipt replay is deterministic on this host.** Clause r replay returned `sha=efd487a39920
  neg=(1,1,0) ver=1.13.2` identically on four independent runs today (a, m-noreadme, m-both runs; the receipt
  records the same digest), and the receipt's labelled rc windows prevented rc drift in every mutant.
- **N5 — Claims' citations check out at BASE.** `corpus/README.md` lines 110 and 112 at `579f694b` carry
  exactly the "warm-cache path" and "the XKB compile itself" still-open text the claims cite (line numbers in
  the current working tree shift by the already-staged README row — the citations are BASE-relative and
  accurate). `axis-tip.txt` was committed at `d40189c9` as registration states; its internal
  `rev=f2b8568b…` is the axis-publication commit the published table comes from — consistent, not a mismatch.
- **N6 — Data-commit discipline intact at review time.** At `3e6c848a` the entry is absent
  (`git cat-file -e` exits 128) and `corpus/`+`tools/` are byte-identical to BASE. The C2 data currently in the
  lane working tree (modified `corpus/README.md`, `corpus/SOURCES.md`, untracked entry + L1 sep receipts) is
  uncommitted staging, which the wave rules permit; no data commit was observed.
- **N7 — `--work` placement guard is positional.** The C1 counter derives `lane_root()` from its own location,
  so `--work` must lie outside the clone *and outside the clone's parent directory*; a sibling-of-clone work
  dir fails with `SETUP work dir inside a hidden path` exit 2 (hit once in this seat; `l1-draft/c1-score.sh`
  already complies: clone at `<S>/c/clone`, work at `<S>/work`). Usage note only; the predicate is unaffected.
- **N8 — Historical receipt labeling.** The committed pre-freeze reference receipt `l1-c1-ref-final3.txt` shows
  `readonly=fail trips=2` (an earlier counter iteration's strace clause); the r-fixed counter's committed
  `l1-c1-ref-rfix.txt` shows `TARGET_MET … readonly=ok`, and this seat's independent tool-only run reproduces
  `trips=0` on the frozen counter. A reader scanning "final"-named receipts should reach for `-rfix`, not
  `-final3`.

## Residual risk

- C1 was not re-run on the both-landed tree. Behavioral blindness is established by N1 (byte-identical C1
  numbers with C2 data present) plus the N3 static read-set, so the added run would be confirmatory only.
- The 20 w1 C1 controls were not individually re-scored here; per my seat target I ran the two cheapest named
  skip-work controls (base cold-only equivalent = entry-only tree; `always-cold` = draft tool patched at
  `read_cache`). Both miss exactly as registration requires. The full 20-control re-score against the frozen
  merged fixture set remains L1's freeze job and is already receipted (`w1/ExecControlsC1`).
- C2 clause i passed with headroom `present_at_rev=3/4` (only ≥2 of 4 ground terms required). By design, but
  the margin is one term.
- C2's trust root remains the committed fetch copies bound to row digests (declared residual); this seat did
  not re-hash upstream objects, only the live replay behavior.

## Verification gaps

- None blocking. lsp/diagnostics device was not available in this seat's toolset; the caller/definition checks
  above are grep+runtime evidence (recorded as the literal fallback per wave rules).
- Scratch cleanup: `/fast/scratch/hyaku/mado-r48/RevRoutes` (73 MB peak) removed after receipt copies above;
  nothing written outside the seat dir, the report, and that scratch.
