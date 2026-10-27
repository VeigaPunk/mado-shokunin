# ConnClaimOverlap — cross-claim / sibling overlap scan (round-48 w2 = FALSIFY)

Seat: ConnClaimOverlap (leaf; no subagent dispatch). Date 2026-10-26. Lane: mado-shokunin.
Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; freeze commit `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`.
Replay tree: scratch clone of the freeze commit with the l1-draft data bytes overlaid exactly per the
`l1-draft/c1-score.sh` / `l1-draft/c2-mirror.sh` recipes (tool → `tools/mado-terminal.py`, entry →
`corpus/knowledge/`, rows S340–S350 after the S339 row of `corpus/SOURCES.md`, README row after the
`xdg-terminal-selection-r47.md` index row). Replay commits: `cf5ab70b` freeze → `d5d13281` data overlay;
variants `b161351f` entry-only (tool removed), `2d080a43` tool-only (C2 entry/rows/README row removed).
The overlay was cross-checked against the lane's own uncommitted integration edits: same 11 rows, same README
row, same tool sha256 (`1dfde36c…`), so the replay predicts the pending data commit byte-for-byte (module
commit metadata).

## Verdict

No common evidence or contested ownership found between C1 and C2 or with any sibling lane. Separability
holds in both directions under live scoring. The terminal cache is a new *executed* surface and the XKB
compile is a new *sourced* ground; neither repeats a prior count. Both counters independently re-score
TARGET_MET on the replay of the data commit. **No miss to report; the freeze stands on the overlap axes.**

## F1 — Cross-claim read-set audit: disjoint (static + dynamic)

Attack: find one file both counters read.

- Static constants. C1 counter (`quality/counters/c1-r48-terminal-cache.py:127-137`): `TOOL =
  tools/mado-terminal.py`, `NAME_COLD/NAME_WARM = c1-r4[78]-fixtures.json` (beside the counter),
  `PIN_REL = .ufo/waves/round-47/fetch/xdg-terminal-exec`, `--work` scratch (outside repo, removed on
  exit). C2 counter (`quality/counters/c2-r48-xkb-entry.py:126-132`): `ENTRY =
  corpus/knowledge/xkb-keymap-compile-r48.md`, `REGISTRY = corpus/SOURCES.md`, `README = corpus/README.md`,
  `FETCH = .ufo/waves/round-48/fetch/`, `HELD_FETCH = .ufo/waves/round-46/fetch/`,
  `RECEIPTS = .ufo/waves/round-48/receipts/`. Intersection: **empty**. Cross-grep of each counter for the
  other claim's filenames/terms: 0 hits (C1 has no `corpus|xkb|SOURCES|README|round-48/fetch|round-48/receipts`
  reference; C2 has no `mado-terminal|c1-r4|xdg-terminal|fixtures` reference — its single doc-comment mention
  of the round-47 pin is prose).
- Dynamic. `strace -f -e openat,execve` of a full C2 run (`c2-strace.txt`, 2 654 lines): lane paths opened
  are only `.git/HEAD`, the counter itself and its TMPDIR replay scratch; execs are `git` (PATH probes) and
  the receipted `xkbcli` re-run. Zero `mado-terminal|c1-r4|xdg-terminal` references. `strace` of the C1
  setup (`c1-entry-only-strace.txt`): zero `corpus/SOURCES/README|xkb` opens.

## F2 — Separability, functional: proven both ways

Attack: land one claim without the other and try to flip a verdict.

- `git rm tools/mado-terminal.py` (entry-only, `b161351f`): C2 counter → **TARGET_MET exit 0**
  (`c2-entry-only.txt`) — a tree with no C1 tool at all admits C2.
- Revert the C2 entry + rows + README row (tool-only, `2d080a43`): C2 counter → **TARGET_MISSED exit 1**,
  `clause=a entry_absent` (`c2-tool-only.txt`); C1 full run on the same tree → **TARGET_MET exit 0**
  (see F5) — the tool-only tree misses C2 while C1 is unaffected by C2's absence.
- C1 with the tool removed (`b161351f`): counter stops at SETUP exit 2 (`c1-entry-only.txt`) because
  `lane_root()` discovers the lane by `tools/mado-terminal.py` above the counter
  (`c1-r48-terminal-cache.py:175-182`). Nuance (not a defect): the clause-a `tool=absent → TARGET_MISSED`
  branch is unreachable in a consistent tree (absence-at-REV equals absence-on-disk, which raises first);
  both outcomes are non-MET, so the predicate's scoring power is unchanged. It does mean "tool absent" is a
  setup error rather than a scored miss — the registration's controls list ("base cold-only", "always-cold",
  …) all keep the tool present, so no frozen control is invalidated.

## F3 — Novelty at BASE: both surfaces held open; no prior count

Attack: catch a claim re-counting ground a prior round already scored.

- `corpus/README.md` at BASE: line 110 "Still open: … the warm-cache path" (round-47 frontier); line 112
  "Still open: the XKB compile itself" (round-46 frontier). Both locators cited in `claims.md` check out
  verbatim at `579f694b`.
- C2 clause-i census at BASE under `corpus/`: `xkb_keymap_new_from_names`, `XKB-595`, `compile-keymap`,
  `xkeyboard-config-2.48` → all **absent** (git grep exit 1 each); ≥2 present at REV (counter:
  `present_at_rev=3/4` — one term lives only in `.ufo` receipts, which clause-i does not count).
- C1 boundary against round 47: the r47 counter (`quality/counters/c1-r47-terminal.py:55-56`) explicitly
  puts "the cache path of the resolver (a warm cache)" **outside** the contract; its 190 fixtures contain
  exactly one cache token, a list-directive case (`/enable_cache` id `d6-directive-looking-id`), not the
  warm-cache file. The r47 corpus entry documents the cache (`§The cache, separately`, pin S327 = the
  resolver README) but declares it "sourced; out of the C1 contract". C1 moves that documentary edge class
  to executed ground: the base tool docstring states "This tool always models the cold path"
  (`tools/mado-terminal.py` @ BASE, lines 82-85 region). So "terminal cache = new **executed** surface" is
  accurate and does not erase the r47 documentary record; "XKB compile = new **sourced** ground" is
  accurate (held line `hyprland-input-devices-r46.md:69` "The XKB compile itself is not reproduced" is
  byte-equal at BASE and freeze, and the C2 counter's clause h enforces that). Neither repeats a prior count.
- Prior-counter sweep: no counter before `c1-r48`/`c2-r48` scores warm-cache behavior or XKB compilation
  (git grep at BASE over `corpus/knowledge/` and `quality/`: no `compile-keymap`/`xkb_keymap_new_from_names`
  ground).

## F4 — Sibling PROVINCE/SOURCES re-scan: corroborates w1, two extra host-state files classified

Attack: find a sibling lane that already owns either surface (which would contest mado's claim or let the
claims borrow foreign evidence).

- Re-ran the w1 scan myself, read-only, over 20 sibling lanes × {`PROVINCE.md`, `corpus/README.md`,
  `corpus/SOURCES.md`}: XKB/keymap/RMLVO/KcCGST/`kb_*` terms → **0 hits**. `xdg-terminal-exec|xte_|save_cache|
  warm-cache|mado-terminal` → one hit, `tabi-shokunin/corpus/README.md:18` "two preserved warm-cache runs",
  which is browser bfcache loopback evidence — terminology collision only, same disposition as w1.
- Knowledge-tree grep across all 20 `corpus/knowledge` trees: 8 files hit — `mori …/observability-census-r1.md`,
  and 6 `tsukuroi` files (`aur-risk-plane{-ver-s6}.md`, `boot-plane.md`, `oom-event-plane.md`,
  `calibration-synthesis.md`, `degraded-triage-r4.md`). The last two were **not** in w1's list; inspected:
  all six tsukuroi hits are the `app-Hyprland-xdg-terminal-exec…scope` OOM-kill / AUR-package-census records —
  host liveness/package state, not resolver selection or cache behavior; mori's is the same scope's liveness.
  Same classification as w1's: adjacent surfaces, explicitly not contested. mado remains sole owner
  (`kotoba-shokunin/PROVINCE.md:69` census row confirms the declared plane).
- No sibling lane claims XKB/keymap/input-method ground; no lane claims xdg-terminal-exec
  selection/cache behavior. Nothing for either claim to borrow; no ownership conflict.

## F5 — Independent re-score of the replay data tree (both claims)

Attack: confirm the frozen instruments admit the data commit state this wave attacks.

- C1: `python3 -I quality/counters/c1-r48-terminal-cache.py --repo <replay> --rev d5d13281 --work <scratch>
  --nonce 4848` → **TARGET_MET, exit 0** (`c1-full-run.txt`): cold 190/190, warm 204/204, explained 394/394,
  generated 230/230, selftest ok (69/69 in-sandbox), readonly ok, trips=0. 423 s. Independently reproduces
  w1's `l1-c1-ref-final.txt` verdict at the post-overlay revision.
- C1 on tool-only variant (`2d080a43`): TARGET_MET, exit 0 (`c1-tool-only.txt`) — C1's verdict is independent
  of every C2 byte.
- C2: `TMPDIR=<scratch> python3 -I quality/counters/c2-r48-xkb-entry.py --repo <replay> --rev d5d13281` →
  **TARGET_MET, exit 0** (`c2-full-run.txt`): clauses a–r all 1; replay `sha=efd487a39920` matches the
  committed receipt; negative probes (1,1,0); held S318/S319 + r46 entry unchanged.
- Receipt/pin disjointness: C1's trust root is one pin sha256 `89f2be9a…` (r47 fetch); C2's is 14 unique
  shas under `.ufo/waves/round-48/fetch/` — disjoint sets. C1 counter cites no receipt; C2 cites exactly
  one (`.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt`). Cross-term grep of the data artifacts
  themselves (C2 entry/rows/README row/receipt vs C1 tool/fixtures): zero hits in both directions.

## F6 — Quality review and w1-ownership scan: no shared evidence

- `git diff corpus/QUALITY.md` (uncommitted lesson criteria 96–101): lesson/routing criteria only; none
  reuses C1 or C2 evidence (criterion 96 touches the tool's *contract delta* — the routed D1 item, a lesson
  check, not claim data; criterion 100 is process). C1's quality-trend justification and C2's
  expansion-sourced claim draw on disjoint artifacts.
- w1 seat cross-citation: only the connector seats (ConnClaims, ConnSiblings) and the cross-claim critic
  (CritClaimSizing) name both claims — by role. Specialist-seat mentions classified: `ExecLsEmu.md:80` lists
  `/usr/lib/xkbcommon` lines inside an `ls -LRl` real-tree receipt (incidental host content of C1's ls
  enumeration, not C2 evidence); `ScrCacheDoc.md:90` enumerates the freeze contents; `ScrRows.md:80` is a
  negative guard ("no `xdg-terminal-exec` run"). No C1 artifact derives from C2 evidence or vice versa; no
  single w1 seat authored decisive evidence on both sides. Post-w1, the counters, fixtures merge and
  l1-draft bytes are L1-authored for both claims — common *integrator* ownership by design
  (`registration.md` names l1-draft/ as the canonical data-candidate location); the counters judge bytes,
  not authorship, and F1/F2 show the byte sets are fully separable.

## Contradictions / residual risks

- None that break the predicate. Two recorded nuances: (1) C1 tool-absent yields SETUP exit 2 via lane-root
  discovery rather than a scored clause-a miss — non-MET either way, no frozen control affected; (2) the r47
  corpus entry documents the cache while C1 claims the *executed* surface — the registration's wording
  ("Surface moved: the cache edge class, frontier → core") is exactly right and does not over-claim novelty.
- Sibling adjacencies (tsukuroi package/OOM-scope records, mori liveness, tabi bfcache term) stay distinct;
  w1's proposed PROVINCE.md refinement line correctly captures the boundary. Two extra tsukuroi files beyond
  w1's list carry the same host-state disposition (F4).

## Verification and writer-bound record

- Replay: `git archive 3e6c848a | tar -x --exclude-from` (26 legacy files >1 MiB excluded, none on either
  claim's path), fixture repo `git init` in scratch, root asserted before every commit; BASE object fetched
  read-only from the lane for the C2 counter's BASE comparisons. No lane file modified; no lane git/jj
  mutation; no commit/push; pacman untouched; no install.
- Evidence files (this dir): largest `c2-strace.txt` 314 490 B; total 368 823 B — all written under
  `ulimit -f 2048` (1 MiB cap). Largest output file overall: the scratch git index, 2 894 157 B
  (tooling-internal; the cap was raised only for git-index/counter-sandbox binary copies, never for
  evidence). Scratch `…/tmp.XrTmpPnI1H` + work dirs deleted after the last run; total scratch stayed under
  the 2 GB budget.
- Host: read-only everywhere; no compositor/service mutation, no input injection, no GUI/terminal launch;
  no serials/titles/process tables printed.
