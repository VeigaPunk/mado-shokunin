# ScrRowsPlaced — registry placement and schema of S352-S363 at `b4a79843`

Seat: w2 (FALSIFY, policy v1), round 50 (hyaku run 10), lane `mado-shokunin`.
Scored rev: `b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip). All blobs read through a
`git clone -q --shared` of the lane inside `/fast/scratch/hyaku/mado-r50/ScrRowsPlaced/` (toplevel asserted);
nothing written in the lane tree except this seat dir.

**Verdict: (a)-(e) hold at `b4a79843` and the census reproduces byte-for-byte. One row-level finding: the
S361 anchor quotes a generator hash that matches no committed blob (F1). Three minor observations (F2-F4) and
two context notes.** No E03/E04/E11/E12 on `mado`; the census output is identical to the frozen receipt.

Reproduce everything with `verify_rows.py --repo <clone> --rev b4a79843…` (seat dir, read-only, exit 0 clean /
3 on findings / 1 on hard failure). Receipts in `receipts/`.

## 0. Freeze anchors checked first

| item | value at `b4a79843` | frozen (`registration.md`) | verdict |
|---|---|---|---|
| `corpus/SOURCES.md` sha256 | `b3a1a041d4a9ce0c2555f028ce415bac5a4b1a0e38bf782e730cbb24ddf52744` (264837 B) | `b3a1a041d4a9…` | same bytes as at data rev `906178b6` (identical hash at both revs) |
| entry `corpus/knowledge/hyprland-bind-key-match-r50.md` | `ae8f8d4de6fa…` 31215 B | `ae8f8d4d…` | unchanged between data and attack rev |
| lesson `corpus/lessons/round-50.md` | `e7cd29620aee…` 12755 B | `e7cd2962…` | unchanged between data and attack rev |
| `receipts/binds-live-r50.txt` / `fetch/binds-live-r50.txt` / `w1/ExecLiveR50/binds-live-r50.txt` | all `9f16e5a5ce7f…` 1768 B | `9f16e5a5…` | three copies byte-equal at the rev |

So the registry bytes under attack here are the frozen bytes; there is no drift for the L1 to reconcile.

## 1. (a) Placement inside `## Registry`

Headings in `git show b4a79843:corpus/SOURCES.md`: `## Registry` line 9, `## Paths` line 314,
`## Search log` 360, `## Leads (unopened)` 524. Header row line 11 (`| id | source | kind | tier | scope |
anchor | teaches | status | opened | recheck | used-by |`), separator line 12 (the only separator row in
the section), rows lines 13-312 = 300 rows.

- S352-S363 occupy lines 301-312, contiguous, ascending, immediately after `S351` (line 300), and line 313 is
  blank before `## Paths` at 314.
- Row-shaped lines outside `## Registry`: **none** (`verify_rows.py` (a2); census E12 also silent).
- Partial state at freeze (contiguous tail after S351) means the rows were appended, not inserted — matching
  the freeze note "rows S352-S363 appended in `## Registry`".

PASS.

## 2. (b) 11 cells per row, no literal `|` inside a cell

Splitting each raw line on `|` yields 13 parts (leading/trailing empty) for **all 12 rows** and for all 300
registry rows → 11 cells each; no cell is empty; no tabs, CRs, or escaped pipes in the 12 rows.
(`receipts/rows-parse.txt`: `cells=11 empty_cells=0` for every row.)

Schema values sit inside the registry's existing vocabulary (`kind` ∈ {code, docs, own-work}; `tier` A;
`status` mined): registry-wide counts are `code 160 / docs 83 / own-work 31 / spec 16 / community 5 / paper 3 /
book 1 / dataset 1` and `mined 281 / queued 10 / rejected 9`; the 12 new rows add code 8, docs 2, own-work 1
and mined 12. PASS.

## 3. (c) Every pin path exists at the rev; sha256 matches the pin bytes

13 pin references across the 12 rows (S355 carries two). For each: `git cat-file blob <rev>:<path>`,
sha256/size/line-count compared with the anchor cell — **13/13 MATCH**
(`receipts/pins.tsv`; `verify_rows.py` (c)).

| row | pin | bytes | lines | sha256 |
|---|---|---|---|---|
| S352 | `fetch/Hyprland-KeybindManager.cpp` | 39334 | 975 | `8d8f35fc…` ok |
| S353 | `fetch/Hyprland-legacy-ConfigManager.cpp` | 90963 | 2184 | `9db68cf4…` ok |
| S354 | `fetch/Hyprland-InputManager.cpp` | 98845 | 2315 | `feedf32e…` ok |
| S355 | `fetch/xkbcommon-keysym.c` | 14948 | 450 | `123e3390…` ok |
| S355 | `fetch/xkbcommon-keysym.h` | 4949 | 124 | `1398b750…` ok |
| S356 | `fetch/xkbcommon-ks_tables.h` | 324906 | 8314 | `6960e7e4…` ok |
| S357 | `fetch/xkbcommon-tools-how-to-type.c` | 30238 | 836 | `f774882e…` ok |
| S358 | `fetch/xkbcommon-xkbcommon-keysyms.h` | 264502 | 3545 | `13023369…` ok |
| S359 | `fetch/wiki-Binds.md` | 19526 | 600 | `3d8a2a68…` ok |
| S360 | `fetch/wiki-Variables.md` | 51064 | 684 | `3b3bb219…` ok |
| S361 | `fetch/binds-live-r50.txt` | 1768 | 34 | `9f16e5a5…` ok |
| S362 | `fetch/xkbcommon-state.c` | 67069 | 1955 | `8cc57f53…` ok |
| S363 | `fetch/Hyprland-IKeyboard.hpp` | 4816 | 137 | `82e0bc9e…` ok |

Supporting, all consistent: `fetch/SHA256SUMS` lists 15 files whose hashes all verify against the blobs, and
every row pin hash equals its listed hash; `w1/ExecFetchR50/fetch-manifest.tsv` records for each of the 14
upstream pins `http_status 200`, the same byte counts, line counts and sha256, and `equal=yes` against the
round-49 pin hash. Every anchor's file:line range is inside its pin's line count (largest range ends at 1651
of 2184 for S353; S352 ends at 899 of 975, S357 at 627 of 836, S362 at 1446 of 1955, S363 at 124 of 137).

### F1 (FINDING) — S361's auxiliary generator hash matches no committed blob

Row S361 (line 310) states:

> `generator .ufo/waves/round-50/w1/ExecLiveR50/make-receipt.py sha256:50543f8a7c16ec6233fed337301d981985e98880d025c1a71405c385b5247048`

The committed generator at the same rev is **`73b6a7eb52f16e77abf02d56c9f7201f16700c23665b71d558cadf9040d56a36`**
(17184 B, 4 files in `w1/ExecLiveR50/`, none hashing to `50543f8a…`; `git log --all` for that path shows a
single committed version, introduced by `1b37a59e`). The same number appears in the w1 draft
`.ufo/waves/round-50/w1/ScrRowsR50/rows.md:7`, so the draft's stale value was carried into the registry.

Scope of the damage: the row's *pin* (`fetch/binds-live-r50.txt`, `9f16e5a5…`) and every counted claim in the
row's `teaches` cell check out (§6), so this is a broken locator hash, not a broken row: the recorded
generator bytes cannot be recovered from the hash by any reader. It is a frozen-artifact integrity defect that
the C1 counter does not test: `grep -c make-receipt quality/counters/c1-r50-bind-entry.py` = **0** and
`grep -n ExecLiveR50 …` = no match at `b4a79843`, so PRED-C1-r50 reads the row's pin path but never this
locator string — C1's TARGET_MET at `906178b6` is silent on F1 by construction.

## 4. (d) `opened` / `recheck` cell shapes

All 12: `opened = 2026-10-27` (ISO, not in the future); `recheck = on-release` ×11 and `90d` ×1 (S361, the
own-work host receipt). Registry-wide context: `on-release` 185, `90d` 52, `on-change` 33, `180d` 18, plus ISO
dates and rarer `on-*` cadences — the two forms used here are the two commonest. PASS.

### F2 (OBSERVATION) — the E09 rule is looser than "NNd"

`scripts/sources-census.sh:663-667` accepts any `^[0-9]+d$` and any `symbolic(recheck)`, so out-of-contract
cells pass unchanged: mutating S363's `recheck` to `400d`, `9d`, `d90` or `banana` each leaves
`verdict ok` rc 0 (`receipts/mut-recheck-{400d,banana,2026-13-45}.txt`; only `2026-13-45` and an empty cell
raise E09). Practical consequence: silence of E09 on `mado` is weaker evidence than "recheck cells are shaped";
the shape claim above rests on my own regex, not on the census.

## 5. (e) `used-by` targets exist

- S357, S358 → `corpus/lessons/round-50.md` (exists at the rev, `e7cd2962…`).
- The other ten → `corpus/knowledge/hyprland-bind-key-match-r50.md` (exists, `ae8f8d4d…`).
- Back-references are present, not just resolvable: the entry names every row S352-S363 (counts 1-10 per row)
  and the lesson names all twelve (counts 1-5 per row).

PASS.

## 6. Supporting spot-checks of the rows' own counted claims (against their pins)

These are not my verdict surface; they are here because they are cheap, local and they bound F1's blast radius.

- S361 `teaches` vs `fetch/binds-live-r50.txt`: `binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0`,
  `input:resolve_binds_by_sym int=0 set=false`, raw-JSON digest `9a47199e…` over 90401 bytes — all present
  verbatim in the receipt; the 13 histogram rows sum to 192
  (23+2+7+2+2+1+42+37+26+3+19+22+6). The raw JSON is not committed, so the 90401-byte digest is
  `[UNVERIFIABLE-LOCALLY]` (it is the same digest recorded by round 49: `round-49/fetch/binds-live-r49.txt:2`).
- S356: `xkbcommon-ks_tables.h` actually holds 2638 `name_to_keysym` entries and 2505 `keysym_to_name` entries
  — the row's "2505 values and 2638 names" is exact; the generator name is in the pin's own header (line 3).
- S358: parsed from the pin's `#define XKB_KEY_*` lines with numeric normalization — 2638 names over 2505
  distinct values, 133 aliased, and the "last-define rule" flips exactly 120 canonical names; all three numbers
  match the row. The parenthetical also reproduces: `grep -c 'define XKB_KEY_'` = 2659 = 2638 + 21
  comment-only hits.
- S359's "(2026-08-05, before the 0.56.2 release at 14:14Z)" — the commit date is receipted
  (`w1/ExecFetchR50/commit-identity.txt:10`: `2026-08-05T13:16:48Z`); the "14:14Z" release time has no
  receipt under `.ufo/waves/round-50/` (`git grep 14:14` hits only the row itself), so that clause is
  `[UNSOURCED-IN-REPO]`.

### F3 (OBSERVATION) — `fetch/SHA256SUMS` self-line does not verify

Its own entry claims `bb21f728…`; the committed bytes hash to `e2b91106…`, and none of eight canonicalizations
(full file, without the self line, without the self line and no trailing newline, tab separators, `./`
prefixes, name-sorted, doubled trailing newline, CRLF)
reaches `bb21f728…`. The 15 non-self entries all verify. Minor: the manifest can list but not self-verify; the
re-pin value for S361's fields is unaffected.

### F4 (OBSERVATION) — S353/S354 duplicate URLs already registered under other scopes

The census flags `W04` for both: `S353` repeats `…/legacy/ConfigManager.cpp` and `S354` repeats
`…/managers/input/InputManager.cpp`, both already registered (e.g. S303/S317 with unrelated scopes). The
scopes genuinely differ (S303 monitor-line grammar; S317 per-device storage; S353 the `bind` KEY field parser;
S354 the bind-sym value and mask feed), so this is the contract's warning-level case, not E04. No action for
the L1 unless the lane wants to consolidate scopes.

## 7. Census: rerun vs `receipts/census-after.txt`

```
cd <scratch> && HOME/XDG_*/TMPDIR under scratch \
  bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
       --root /home/vgpnk/Projects/shokunin --today 2026-10-27 mado
```

- exit **0**; 21 lines: 20 warnings (W04 ×19, W01 ×1) + `mado	ok	…/mado-shokunin/corpus/SOURCES.md`.
- **Zero** E-codes: `grep -cE '\tE[0-9]{2}\t'` = 0 (so no E03/E04/E11/E12 — and no E01/02/05-10 either).
- Byte-identical to the frozen receipt: `md5sum` `fec83baf450d2d1436743231a91d52c9` for both
  `receipts/census-run.txt` and `.ufo/waves/round-50/receipts/census-after.txt` (diff empty).
- Same warning *set* as the receipt, including the two new rows (`S353`, `S354` W04) — no warning names any
  other new row.

Both-ways control (so "no E-codes" is not blindness):

1. `sources-census.sh selftest` → rc 0, **96 mutants killed** + `selftest ok`, including `E03-duplicate-id`,
   `E04-duplicate-url`, `E09-bad-recheck`, `E11-dangling-usedby`, `E12-outside-registry-mutant`
   (`receipts/census-selftest.txt`).
2. Targeted mutants of the **real** registry (clone worktree, restored after each; baseline reproduces rc 0,
   19×W04 + 1×W01):
   - S361 id → S360 ⇒ `E03 S360 duplicate id` (`mut-m1-dup-id.txt`)
   - S359 row copied under id S364 ⇒ `E04 S364 duplicate url …Binds.md within scope …` (`mut-m2-dup-url.txt`)
   - S352 used-by → `corpus/knowledge/missing-x.md` ⇒ `E11 S352 missing used-by …` (`mut-m3-dangling.txt`)
   - S362 row moved below `## Paths` ⇒ `E12 S362 row outside Registry section` (`mut-m4-outside.txt`)
   - S363 recheck `on-release` → invalid ISO ⇒ E09 fires; → `400d` ⇒ does not (F2).
   Clone `corpus/SOURCES.md` restored to `b3a1a041…` after every run (asserted).
3. `census` (not validate) on `mado`: `rows 300`, `tier.A 289/B 4/C 7`, `status mined 281/queued 10/
   rejected 9`, `missing 0` — the 300 rows include S352-S363, so the validator's silence covers them.

## 8. Method, environment, limits

- Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/mado-shokunin <scratch>/lane`;
  `git -C <scratch>/lane rev-parse --show-toplevel` = the clone; `HEAD` = `b4a79843`.
- Every run had `HOME`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `TMPDIR` under
  the seat scratch; `ulimit -f 65536` in every writer shell; no host state, no compositor call, no GUI, no
  network, no `hyprctl`.
- Tooling: nothing installed or upgraded (system `python3 -I`, `git`, `bash`, `gawk` as shipped).
- Lane worktree note: `git -C …/mado-shokunin status --porcelain` shows `M corpus/lessons/round-50.md` plus
  untracked `w2/` artefacts (not mine; the file I score is the committed blob, hash `e7cd2962…`).
- Scratch is deleted at the end (receipts copied into the seat dir first); no scratch or `/tmp` path is cited
  as evidence.
- Limits: upstream URL → commit → pin-byte correspondence is asserted by
  `w1/ExecFetchR50/fetch-manifest.tsv` (`200`, `equal=yes`) and cannot be re-derived offline; the raw
  `hyprctl binds -j` JSON is not committed, so its 90401-byte digest is unverifiable locally (declared residual
  in `registration.md`). The census reads the lane *worktree*; `corpus/SOURCES.md` is clean vs HEAD there
  (absent from `git status`), so worktree == `b4a79843` bytes for this file.

## 9. Deliverables in this seat dir

- `ScrRowsPlaced.md` (this report)
- `verify_rows.py` — reproducible check (a)-(e) + F1 detection; read-only; exit 0/3/1
- `receipts/pins.tsv` — 13 pins, declared vs actual bytes/lines/sha256
- `receipts/rows-parse.txt` — per-row line, cell count, anchor-ref count, max anchor line, pin line counts
- `receipts/census-run.txt`, `receipts/census-run.err` — my census run (identical to the frozen receipt)
- `receipts/census-selftest.txt` — validator both-ways control (96 killed)
- `receipts/mut-*.txt` — baseline + 5 targeted mutants (E03/E04/E11/E12/E09) + 3 recheck probes
