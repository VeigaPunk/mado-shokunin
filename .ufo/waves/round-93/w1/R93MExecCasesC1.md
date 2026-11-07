# R93MExecCasesC1 — C1 byte-class cases, oracle, fuzz generator (DRAFT runs)

## Files written (all under `.ufo/waves/round-93/controls/`)
- `portal-oracle-r93.py` (sha256 `d50d88bf…6f6`) — round-90 oracle + byte writes
- `gen-c1-bytes-cases-r93.py` (sha256 `1e9f7193…d0c`) — writes the unlabelled byte set
- `portal-bytes-cases-r93-unlabelled.json` (sha256 `369f44d6…5b5`) — 71 cases
- `portal-cases-r93.json` (sha256 `96f3fa07…b8b`) — 229 r90 + 71 labelled byte cases
- `fuzz-bytes-r93.py` (sha256 `f670929e…6b6`) — `--seed N --count K --out` generator
- This report: `.ufo/waves/round-93/w1/R93MExecCasesC1.md`

## 1. Oracle diff (`portal-oracle-r93.py` vs r90, recorded verbatim in scratch `oracle-diff.txt`)
The ONLY behaviour change: fixture writes go to bytes,
`with open(p,"wb") as fh: fh.write(text.encode("utf-8","surrogateescape"))`,
in both the `dir` branch (line 108-109) and the `xdg` branch (line 121-122),
so lone surrogates `\udcXX` become raw byte `XX`. The label dump also writes
`json.dumps(..., ensure_ascii=True)` + ascii (the r90 `ensure_ascii=False` dump
crashes with `UnicodeEncodeError: surrogates not allowed` on byte cases — a
mechanical necessity, not a labelling change). Same CLI (`--cases/--label/
--scratch-root/--timeout/--jobs`), same label schema, same binary pin.

## 2. Byte-class cases (71; 16 r92 included verbatim, ids keep `d1-` prefix)
Schema: round-90 (`id, mode, desktop, files{name:text}`) with byte content as
lone surrogates; each tagged `"class"`: `a:27 b:16 c:7 d:8 ws:13`; modes `dir:64 xdg:7`.
- (a) invalid UTF-8: `0x80`, `0xC3 0x28`, surrogate encoding `0xED 0xA0 0x80`, `0xFF`,
  overlong `0xC0 0xAF`, truncated `0xC3` at EOF — in a portals.conf comment,
  another group's key, an unread `[preferred]` key, a read `[preferred]` key
  (Print/FileChooser/default), a `.portal` comment, an unread `.portal` key,
  `Interfaces`, `DBusName`, `UseIn`, and one gtk.portal `Interfaces`; both dir and xdg modes.
- (b) `0x0B`: at line start, before group, before key, before `=`, after `=`,
  inside a value (`k\x0bde`), trailing a value, trailing a key, and in a `.portal` file
  (before the group and before `DBusName`); xdg too.
- ws (GLib DOES treat as space): `0x0C`/`0x0D`/TAB/space before group/key, before/after
  `=`, CRLF line endings, TAB in a `.portal`; xdg too.
- (c)/(d) repeated keys and `x[]`/`x[C]`/`x[en]` keys, dir + xdg, as regressions.

## 3. Labels + merge
`portal-oracle-r93.py --cases portal-bytes-cases-r93-unlabelled.json --label labelled-r93.json
--scratch-root $S/oracle --jobs 6` → `PORTAL_ORACLE cases=71 incomplete=0
host_tail_sha256=4a4cf319…fbf9` (rc 0). Merged with the 229 r90 cases into
`portal-cases-r93.json` (300 total, `host_tail_sha256` + `oracle_binary_sha256`
top-level keys kept; byte cases carry `class`). All runs are DRAFT (pre-freeze).

Notable labels (all from the real binary at run time):
- `b93-b-vt-value-mid` (`default=kde;gt\x0bk`): oracle loads the config (value body
  VT is data for list parsing, no void) — a genuine distinguisher, not a void.
- `b93-a80-gtk-ifaces`: kde wins FileChooser/Print/Settings, no Screenshot pick
  (Screenshot absent, not gtk-last-resort) — kde.portal remains usable.
- `b93-a80-usein`: `UseIn=KDE\x80` does NOT void the descriptor; picks unchanged
  (UseIn list parse ignores the invalid token for the tested desktop).

## 4. Fuzz generator
`fuzz-bytes-r93.py --seed N --count K --out CASES.json` (unlabelled, same schema,
ids `fuzz93-NNNNN`, class-tagged). Deterministic: seed 938001/count 60 → 12 per
class; seed 42 → same class balance. Mirrors the r90 fuzz CLI shape.

## 5. DRAFT scores (base vs candidate, counter outcome logic + surrogateescape materialise)
`python3 score.py portal-cases-r93.json $S/score` (two runs, byte-identical output):
```
DRAFT score (not a measurement)
base byte: ok=43/71 wrong=28 crash=0
base full: ok=272/300 wrong=28 crash=0
  base class a: {'wrong': 17, 'ok': 10}
  base class b: {'wrong': 11, 'ok': 5}
  base class c: {'ok': 7}  base class d: {'ok': 8}  base class ws: {'ok': 13}
candidate byte: ok=71/71 wrong=0 crash=0
candidate full: ok=300/300 wrong=0 crash=0
  candidate class a: ok=27  b: ok=16  c: ok=7  d: ok=8  ws: ok=13
```
Candidate disagreements on the frozen set: **none** (0 wrong, 0 crash) — so no
finding for the L1 from the frozen cases. Fuzz seed 938001 (60, labelled by r93
oracle then scored): base 52/60 (a:9/12, b:7/12, c/d/ws 12/12), candidate 60/60.
Base scores 43 < 71 on the byte subset, satisfying the declaration's base gate
direction.

## Risks / notes for L1 and the counter seat
1. `portal-cases-r93.json` is written with `ensure_ascii=True` (surrogates as `\udcXX`
   escapes) — a strict-UTF8 json load restores the lone surrogates; reading it with
   `errors="surrogateescape"` would mojibake. The r93 counter must either load it
   as strict or write fixtures via `encode("utf-8","surrogateescape")`.
2. The r90 counter's `materialise` (strict write) cannot even run the byte subset —
   R93MExecCounterC1 must port the same surrogateescape write (my scorer did).
3. Class (c)/(d): all 15 frozen cases are `ok` for BOTH base and candidate
   (effect-invisible, as R92MExecD1 found) — they remain regression-only.

## Commands run (DRAFT, exit codes)
- `gen-c1-bytes-cases-r93.py --out …/portal-bytes-cases-r93-unlabelled.json` → rc 0, `GENC1 cases=71`
- `fuzz-bytes-r93.py --seed 938001 --count 60 --out fuzz93-test.json` → rc 0, 60 cases
- `portal-oracle-r93.py --cases …unlabelled.json --label labelled-r93.json --scratch-root $S/oracle --jobs 6` → rc 0, `cases=71 incomplete=0 host_tail_sha256=4a4cf319…fbf9`
- merge step (python) → 300 cases written
- `score.py portal-cases-r93.json $S/score` → rc 0 (twice, identical); fuzz label+score → rc 0
- No `tools/`/`quality/` edit; no git/jj mutation; no install (pacman paused; none needed).
- Scratch `/fast/scratch/hyaku/mado-r93/R93MExecCasesC1` — DRAFT outputs (`draft-score.txt`,
  `draft-score-fuzz.txt`, `draft-score-repeat.txt`, `oracle-diff.txt`, `score.py`,
  `labelled-r93.json`, `fuzz93-*.json`) retained for L1; deleted on exit by yield wrapper.

Report: .ufo/waves/round-93/w1/R93MExecCasesC1.md
