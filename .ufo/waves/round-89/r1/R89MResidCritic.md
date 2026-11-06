# R89MResidCritic — records and figures audit (round 89, residual r1)

Seat: critic (residual call r1). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
RECORDS = `51bf076fd970106da854e11873b886528c3cffaf` ("round-89: records — knowledge entry, S496-S500, lesson,
QUALITY 148-149, README, ledger, SCORECARD, LOG, measured receipts, w1 results", 2026-11-06 18:12:36 -0300).
Freeze F = `d87361354b4d142287aac05bb973315749ef1fce`; C1 tool revision A = `099c662dc55521e365cd4126132cdcda4efc54b6`;
base `af998dcc41d48618ffe7afe0efc9354755a9244e`. Scratch `S=/fast/scratch/hyaku/mado-r89/R89MResidCritic` (removed on exit).
Every lane file below was read with `git show <rev>:<path>`, never from the working tree. No lane file was edited.
No mutating git/jj command was run. No install, no pacman transaction.

Scope: the records at RECORDS — `SCORECARD.md` § Round 89, `LOG.md` § Round 89, `corpus/knowledge/mako-regex-criteria-r89.md`,
`corpus/lessons/round-89.md`, `corpus/SOURCES.md` S496–S500, `corpus/QUALITY.md` 148–149, `quality/tool-ledger.md` rows for
`tools/mado-mako.py`, `c1-r89-mako-regex.py`, `c2-r89-survivor-kills.py`. The frozen claim text is not attacked here and is
not changed; where a records file repeats a frozen error the finding is against the records file.

Post-RECORDS state, for the closure: two receipts the records cite — `harm-final-r89.txt` and `census-end-r89.txt` — were
created in the working tree 52–53 s after the records commit (18:13:28 / 18:13:29) and are still untracked at the time of
writing; no later commit exists (`git log master -1` → `51bf076f…`). F1–F3 are stated against RECORDS and record what the
current bytes do and do not repair.

## Verdict table

| # | Object | Verdict |
|---|---|---|
| F1 | SCORECARD `:5179` cites `receipts/harm-final-r89.txt`, absent from the RECORDS tree | **FALLS** |
| F2 | the same row claims the census is in that receipt; the receipt has no census line | **FALLS** |
| F3 | lesson `:144` cites `receipts/census-end-r89.txt`, absent at RECORDS (and byte-identical to the start receipt) | **FALLS** |
| F4 | LOG `:4333` "44 blind cases (b01–b44)"; the blind set is 45 (b01–b45) | **FALLS** |
| F5 | knowledge entry `:117-120` "the only remaining refusal … is `core.ini:20`"; a one-command re-run prints two | **FALLS** |
| F6 | lesson `:42` cites `:228` for `word.append(char)`; it is at `:229` | **WEAKENED** |
| F7 | lesson `:117` "drafts S499/S500" collide with the admitted S499/S500 (regex.h, tarball) | **WEAKENED** |
| F8 | lesson `:143` attributes "430 rows" to a receipt that prints no row count | **WEAKENED** |
| — | every other figure in the seven records | **STANDS** (list in §3) |

## 1. Findings

### F1 — FALLS: the harm-watch receipt is cited but not committed at RECORDS

`SCORECARD.md:5179` (round-89 harm row) ends: "C2 at A TARGET_MET 95/95 7/7 (`receipts/c2-harm-at-A-r89.txt`); **the rest in
`receipts/harm-final-r89.txt`**". The declaration's `## Harm watch` names the same file. At RECORDS that path is not in the tree:

```
$ git -C …/mado-shokunin cat-file -e 51bf076fd970106da854e11873b886528c3cffaf:.ufo/waves/round-89/receipts/harm-final-r89.txt
fatal: path '.ufo/waves/round-89/receipts/harm-final-r89.txt' does not exist in '51bf076fd970106da854e11873b886528c3cffaf'
$ git -C …/mado-shokunin status --porcelain
?? .ufo/waves/round-89/receipts/harm-final-r89.txt
```

The file exists in the working tree (1438 B, 28 lines, created 2026-11-06 18:13:28 — 52 s **after** the records commit at
18:12:36) and its contents are real (nine command blocks, all `rc=0`), so this is not a fabrication — it is the round-88 R4
defect class ("records cited an uncommitted receipt", listed in this round's own declaration under `## Inputs read before
declaring`) repeated. It is still untracked as this seat writes (`git status --porcelain` → `?? …/harm-final-r89.txt`).

Smallest safe correction: commit the receipt in the next commit and keep the pointer (nothing in the row changes), or replace
the pointer with the receipts it summarises. The row's own figures (C2 at A 95/95 7/7) are backed by the committed
`receipts/c2-harm-at-A-r89.txt` and stand.

### F2 — FALLS: the harm row lists a census the receipt does not carry

`SCORECARD.md:5179` lists the harm-watch objects as "gate selftest / `--no-live`; index; ledger; tool and counter selftests;
**census**". The receipt's 28 lines are: `mado-verify --selftest` (460/460), `--no-live` (CLEAN 29 pass, 4 notes),
`check-index` (110/110), `check-tool-ledger` (165/165), `mado-mako --selftest` (59/59), and the four counter selftests
(27/27, 18/18, 40/40, 28/28). No census line — checked on the current 18:13:28 bytes as well as on the RECORDS state. Even
after F1 is repaired by committing the receipt, the row overstates its receipt.

Correction: either append the census run to the receipt (`bash scripts/sources-census.sh validate --root … mado`, rc 0 — I
re-ran it, §3) or drop "census" from the row's list and cite the LOG's census line + the `grep -c` that produces 435.

### F3 — FALLS: the lesson's end-census receipt does not exist

`corpus/lessons/round-89.md:143-144`:

```
- Start: `receipts/census-start-r89.txt` — `mado ok`, rc 0, 430 rows.
- End: `receipts/census-end-r89.txt` (records revision).
```

`census-end-r89.txt` is absent from the RECORDS tree (`git ls-tree -r --name-only RECORDS .ufo/waves/round-89/receipts/`
lists seven receipts, not eight). It appeared in the working tree at 18:13:29 — 53 s after the records commit — and is still
untracked (`?? …/census-end-r89.txt`). Worse, it is **byte-identical to the start receipt** (`cmp` rc 0; both sha256
`dab9754d6f3592f8b38e5711113f203bc95452f870a251c9feabb036a61920d1`), and the census output carries no revision, date or row
count — so even once committed it is indistinguishable from the start run and proves nothing about the records revision. The
end figure itself is right: `grep -c '^| S[0-9]' corpus/SOURCES.md` → 435 at RECORDS (430 at F), and the census validates
rc 0 (§3).

Correction: produce and commit the end-census receipt, or replace the line with the command that produces 435
(`git show RECORDS:corpus/SOURCES.md | grep -c '^| S[0-9]'` → 435).

### F4 — FALLS: the blind case set is 45, not 44

`LOG.md:4333`: "… cases r31/r32/n04/n07, **44 blind cases (b01–b44)**, and the critic's …". The frozen blind file has 45 cases,
first `b01-bracket-range-match`, last `b45-bang-prefixed-regex-key-is-invalid`:

```
$ git show RECORDS:.ufo/waves/round-89/controls/mako-cases-r89-blind.json | python3 -c "import json,sys;print(len(json.load(sys.stdin)['cases']))"
45
$ git show RECORDS:.ufo/waves/round-89/controls/mako-cases-r89.json | python3 -c "…Counter of id prefixes…"
Counter({'c': 61, 'b': 45, 'r': 32, 'n': 3})   total 141
```

N = 141 = 61 carried + 32 r + 3 n + **45** b. With 44 the arithmetic gives 140, so the "44" contradicts the measured N in the
same records. The frozen declaration repeats it (`claims-declaration-r89.md:49` "b01–b44"; `:132` "N 91 → 141"; `:161` the pin
label "(44, merged unchanged)") — frozen text, not edited by this seat; the sha256 pin `a4fa66cf…` correctly pins the 45-case
bytes.

Correction in the records: LOG `:4333` → "45 blind cases (b01–b45)". (An erratum on the declaration's label is the L1's call.)

### F5 — FALLS: the host-refusal sentence is contradicted by a one-command re-run

`corpus/knowledge/mako-regex-criteria-r89.md:117-120`:

> A summary outside the five applies none of them (measured with `--summary Unrelated`). With `--summary` supplied
> and no `--urgency`, the only remaining refusal on the whole chain is `core.ini:20` (`[urgency=critical]`, which
> needs `--urgency`); `core.ini:11` (`[app-name=Spotify]`) and the five sections all resolve.

Reproducer (tool bytes = A = RECORDS `tools/mado-mako.py`, sha256 `6b4bc409…`; host chain is the declared read set):

```
$ python3 -I tool.py --config ~/.config/mako/config --home "$HOME" --summary Unrelated
MADO_MAKO: resolved=37 refusals=2
refusals[0] = …/core.ini:11: criteria needs --app-name to decide the match; section not applied
refusals[1] = …/core.ini:20: criteria needs --urgency to decide the match; section not applied
```

So with only `--summary` there are **two** refusals, and `core.ini:11` does **not** resolve. The sentence describes the
`--summary --app-name` invocation, which I confirmed prints `refusals=1` (only `:20`); `--summary --urgency` prints
`refusals=1` (only `:11`).

Correction (either form):
- "With `--summary` and `--app-name` supplied and no `--urgency`, the only remaining refusal is `core.ini:20`; the five
  sections and `core.ini:11` resolve." — the measured `refusals=1`; or
- "With only `--summary` supplied, two sections stay refused: `core.ini:11` (needs `--app-name`) and `core.ini:20` (needs
  `--urgency`); the five `summary~` sections resolve."

The rest of §3 is right: the five section rows match `core.ini` byte-for-byte (L24/27/30/33 `on-button-left`, L36→L37
`max-icon-size=80`, L38 `format` = the default), `--summary Unrelated` applies none, and `--summary "Screenshot copied & saved"`
yields `max-icon-size=80` with `format` unchanged.

### F6 — WEAKENED: one-line locator drift in M89-2

`corpus/lessons/round-89.md:42`: "a backslash before any other character falls through to `:228` `word.append(char)`, keeping
it." In `7d3074865a9f5acfa0f1c9c66b460e73d4031331:tools/mado-mako.py` line 228 is `else:` and `word.append(char)` is line 229:

```
$ git show 7d307486:tools/mado-mako.py | sed -n '226,230p'
            if char == '"':
                in_quote = False
            else:
                word.append(char)
            i += 1
```

Correction: `:229`. (QUALITY 149 does not carry this cite — it names `:222` and `:242`, both correct — so the criterion text
itself needs no change.)

### F7 — WEAKENED: the lesson's "drafts S499/S500" now name admitted rows

`corpus/lessons/round-89.md:117`: "Considered, not appended (no admitted entry cites them): the POSIX Base Specifications
chapter 9 and `regcomp()` pages (**R89MScoutSources drafts S499/S500**)". In the landed `corpus/SOURCES.md`, S499 is glibc
`<regex.h>` and S500 is the mako v1.11.0 tarball — both admitted and both cited by the entry. The scout's draft numbering was
different (draft S499 = POSIX chapter 9, draft S500 = the `regcomp()` page; draft S501 = tarball, S502 = regex.h —
`w1/R89MScoutSources.md:89,106,124,145`). A reader following the ids lands on the wrong sources.

Correction: "… (the scout's draft S499 = POSIX chapter 9 and draft S500 = the `regcomp()` page; not appended)".

### F8 — WEAKENED: the start-census row count is not in the cited receipt

`corpus/lessons/round-89.md:143`: "Start: `receipts/census-start-r89.txt` — `mado ok`, rc 0, 430 rows." The receipt is 58
lines (55 `W04` + 1 `W01` findings, the `mado ok` line and `rc=0`); it prints no row count (`grep -n '430\|rows'` → no match). 430 is
produced by `grep -c '^| S[0-9]' corpus/SOURCES.md` at F, which I ran (430). The number is right; the attribution is not.

Correction: "… rc 0; 430 rows by `git show d8736135:corpus/SOURCES.md | grep -c '^| S[0-9]'`".

## 2. What I re-ran (command, exit code, result)

| # | command | rc | result |
|---|---|---|---|
| 1 | `git -C … log master -8 --format='%H %s'` (polled) | 0 | RECORDS found at `51bf076f…` |
| 2 | `python3 -I quality/check-tool-ledger.py --repo … --rev 51bf076f…` | 0 | `LEDGER: population=165 ledger_rows=165 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` |
| 3 | `python3 -I quality/check-index.py --repo … --rev 51bf076f…` | 0 | `MADO_INDEX: indexed=110/110 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| 4 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | `mado ok …/corpus/SOURCES.md`; 55 `W04` + 1 `W01` pre-existing findings, no `E11` |
| 5 | `grep -c '^| S[0-9]' corpus/SOURCES.md` (worktree = RECORDS) / `git show F:…` | 0 | 435 / 430 |
| 6 | MODELLED_FIELDS count at base / A / F (declaration's own command) | 0 | 10 / 12 / 10 |
| 7 | `git show <rev>:<file> \| sha256sum` for the 14 frozen pins | 0 | all equal the declaration's table (counters `5b977141…`, `73bd5201…`, `3678425a…`, `f8e18b7c…`; cases `5fdca7db…`; mutants `5471bee2…`; r88 cases `a0e81b19…`; survivors `9f25df3c…`; c1side `c710a3e5…`; c2side `e02e2b4d…`; blind `a4fa66cf…`; oracle `42270192…`; candidate `6b4bc409…`) |
| 8 | `git show F:tools/mado-mako.py \| sha256sum`; same at A | 0 | `c374d715…92237`; `6b4bc409…73a98` |
| 9 | `python3 -I tool.py --selftest --scratch-root S` | 0 | `MADO_MAKO_SELFTEST: checks=59 failed=0` (ledger row's "59 selftest checks") |
| 10 | `cc -O0 -o ore .ufo/waves/round-89/controls/posix-ere-oracle.c`; 12 table rows + 2 confirming rows | 0 | every glibc verdict in the entry's §2 table reproduced (match, match, nomatch, nomatch, match, match, match, match, match, invalid, nomatch, nomatch; `(ab)\1`→match, `\bWi`→match) |
| 11 | `python3 -c 're.search(...)'` on the same 12 rows | 0 | every Python verdict reproduced, incl. `Possible nested set at position 1` (row 5) and `unterminated character set at position 0` (row 10) |
| 12 | upstream `parse_criteria` replica (criteria.c 162-262) + candidate `tokenize` + r88 `tokenize` | 0 | `summary="a\.b"`→`summary=a.b`; `body~="\d+"`→`body~=d+`; `app-name=a<TAB>b`→one token; r88 gives `('summary','a\.b')`, `('body~','\d+')`, `('app-name','a'),('b',None)` |
| 13 | r88 tool on fixture `[summary="a\.b"]` | 0 | applies to the literal-backslash summary, not to `a.b` (M89-2's observable) |
| 14 | `python3 -I tool.py --config ~/.config/mako/config --home "$HOME" --summary …` (three argument sets) | 0 | refusals 2 / 1 / 1 as quoted in F5; screenshot section → `max-icon-size=80` |
| 15 | `zcat` + `nl -ba` on regex.3, regex.7, setlocale.3, mako.5; `nl -ba /usr/include/regex.h`; `sha256sum` of each container | 0 | digests equal S496–S499; every cited line present |
| 16 | `curl -fsSL https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0`; `sha256sum`; `tar xzf`; `grep -rn setlocale` | 0 / 0 / 0 / **1** | tarball `72d11d3f…7282`, criteria.c `22767742…d76c`, enum.h `1367d5c3…7351`; `setlocale` absent (grep rc 1) |
| 17 | `python3 -I tool.py --selftest` etc. — see 9 | — | — |

Dead step (mine, not the lane's): the first oracle run of row 3 passed `"$(printf 'Wi-Fi\n')"`, and command substitution strips
the trailing newline, so the row printed `match` instead of `nomatch`; re-run with `printf -v t 'Wi-Fi\n'` it prints `nomatch`,
matching the table. No lane figure depended on that run.

## 3. Figures that stand (verified, so the closure need not redo them)

- **SCORECARD C1 row** (`:5177`): MODELLED_FIELDS 10 → 12 (10 at base, 12 at A); base-tool 78/141; candidate 141/141; mutants
  37/37; carried 61/61; python-re 127, naive 34, globals 35 — every value is the closing line of
  `receipts/c1-measured-A-r89.txt` and the control line of `receipts/c1-controls-prefreeze-r89.txt`
  (`naive_correct=34 globals_include_correct=35 base_tool_correct=78 python_re_correct=127`).
- **SCORECARD C2 row** (`:5178`): 0/7 (receipt `c2-controls-prefreeze-r89.txt`: `killed_full 0`, `counted 7`), 3/7 (receipt
  `c2-selftest-control-r89.txt`: RM7C1, RM3C2, RM4C2 `selftest_distinguishes=yes`), gate 7/7 over 95/95, B-only 0
  (`c2-measured-F-r89.txt` closing line); B = 61+26 = 87, S = 4+4 = 8, 87+8 = 95.
- **SCORECARD capability row**: "host criteria sections decided 4/9 → 9/9" — `w1/R89MExecHostDiff.md` §4 table (base 4/9,
  candidate 9/9), and the host `core.ini` does hold exactly 9 criteria sections (L11, 14, 17, 20, 24, 27, 30, 33, 36).
- **LOG** `:4342` "MODELLED_FIELDS 10 → 12" and "Census 430 → 435 rows, exit 0" — both reproduced (§2 rows 4-6); "Fuzz: 12 800
  candidate/oracle comparisons, 0 disagreements; Python `re` disagrees on 404/3200" — `w1/R89MExecFuzz.md` §3 table and `:81`;
  "12 seats (scout 2, scribe 1, executor 4, connector 1, reviewer 2, critic 1, mutation-tester 1)" — `w1-results.json`
  `seats=12` and the per-seat `agent` fields; "attack 4/12" is derivable from the same list (2 reviewers + critic +
  mutation-tester) and is not contradicted anywhere.
- **SOURCES S496–S500** — every Gate quote in the lesson is present at the cited line and ≤ 25 words: S496 19 words at
  decompressed 77-84; S497 19 words at 34-37; S498 15 words at 135-137; S499 the two `#define`s at 310 and 323; S500 7 tokens
  at criteria.c 333-334 plus `grep -rn setlocale` printing nothing. All five rows are `mined`, `opened 2026-11-06`,
  `recheck 180d`, `used-by corpus/knowledge/mako-regex-criteria-r89.md,corpus/lessons/round-89.md`.
- **QUALITY 148/149** — byte-equal (after whitespace normalisation) to the lesson's block quotes; their line cites
  (`R88MResidMut.md:131`, `:38`, `c2-r88-include-containment.py:225`, `c1-r88-mako-fields.py:281`, `mado-mako.py:222`, `:242`)
  all resolve to the text they name.
- **Lesson M89-1** — `R88MResidMut.md:38` (the crash rule), `:131` (the `FAIL exit=1` route), `:192-195` (§8, "cycle detection
  through a second lexical path is untested"), `c2-r88:225`, `:168`, `:471-475`, `c1-r88:281`, `:207`, `:563-566` — all exact.
- **Lesson M89-2** (apart from F6) — `:222`, `:242`, `criteria.c:177-182`, `:186-188`, `:207-212`, `enum.h:7-11`, candidate
  `:276-288`, `:299` — all exact; the three tokenizer probes and the fixture behaviour reproduce.
- **Knowledge entry** — front-matter S-numbers and digests match the landed rows; §1.1-§1.7 line cites resolve; §2's twelve
  rows reproduce on both engines; §3's five host rows match `core.ini` byte-for-byte and the screenshot resolution is
  `max-icon-size` 32 → 80 with `format` unchanged.
- **Ledger** — the three r89-relevant rows exist and describe what the artifacts do; the mako row's "59 selftest checks
  (round 89)" is the tool's own printed count.

Minor wording residue (not scored): `corpus/knowledge/mako-regex-criteria-r89.md:145` says "beyond the DRAFT runs named in the
front matter", but the front matter names no runs — it names the measured receipt and says runs below are DRAFT. No figure
depends on it.

## 4. Scratch

`S=/fast/scratch/hyaku/mado-r89/R89MResidCritic` was created with `mkdir -p`, held the tarball, the decompressed man pages, the
oracle binary, the two tool copies and one fixture config; it is removed on exit (`rm -rf -- "$S"`). No receipt was copied into
the lane: every number above is reproducible from the committed bytes with the commands quoted inline.
