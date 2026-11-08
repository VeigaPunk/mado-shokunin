# R100MExecPanel - the full 28-leg harm panel, run end to end

Seat `R100MExecPanel` (executor), round 100, wave `w1`, lane `mado-shokunin`, base
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4`. Contract:
`.ufo/waves/round-100/claims-declaration-r100.md` C2 and "Shared contract 3".
Deliverables: `.ufo/waves/round-100/receipts/c2-panel-r100.txt` (the receipt, 218 lines,
sha256 `302532e31ed381f3b1a394e62272a5f05ede6b9fdec39c98e6a1c972ba99ac9d`) and this report.
Read at HEAD `ae537dbe361e0d10247dbdd822bdb22fbc41464d`.

Every number below is from a run I made; nothing is copied from another seat's receipt. Where I
rely on the lane's timing receipt I name its bytes and re-derive its arithmetic rather than quote a
verdict. Sha256 values are shown as 12-hex prefixes.

## 1. What I ran

Six runs, all with `--repo /home/vgpnk/Projects/shokunin/mado-shokunin` and
`--panel .ufo/waves/round-100/controls/harm-panel-r100.json` (`6d259164de90`, `expect_legs=28`,
`timeout_s=3600`) except section A, which pre-dates that panel's landing and used the round-99
panel (`160763ce7aa4`, `timeout_s=600`).

| sec | gate bytes | rev | per-leg cap | scope | result | exit | wall |
|---|---|---|---|---|---|---|---|
| A | `quality/harm-watch.py` = base `37a0544b160d` | `43309e6a` | `--timeout 7200` (CLI override) | 28 legs | `legs=28 ok=28 mismatch=0` | 0 | 1722 s |
| B | `build/harm-watch.py` = `2d604f7b654f` | `219e14f4` | panel `3600` | 28 legs | `legs=28 ok=26 mismatch=2` | 1 | 2130 s |
| C | `build/harm-watch.py` = `2d604f7b654f` | `219e14f4` | panel `3600` | `--only r97c1_filetype --only ledger`, scratch `/tmp/m100p/s` | `legs=2 ok=1 mismatch=1` | 1 | 755 s |
| D | `build/harm-watch.py` = `2d604f7b654f` | `18bce790` | n/a | `--only ledger`, scratch `/tmp/m100p/s2` | `legs=1 ok=1 mismatch=0` | 0 | 2 s |
| E | `build/harm-watch.py` = `2d604f7b654f` | `18bce790` | panel `3600` | 28 legs | `legs=28 ok=28 mismatch=0` | 0 | 1447 s |
| H | `quality/harm-watch.py` = committed `acecb0ea4257` | `ae537dbe` | panel `3600` | 28 legs | `legs=28 ok=28 mismatch=0` | 0 | 1341 s |

Exact command lines, all 28 `LEG` lines, the `HARM_WATCH:` line, `EXIT_CODE`, `WALL_S` and the
`--json` object are in the receipt, one section per row above; section G of the receipt is the
reading guide.

Two notes on method, both measured rather than assumed:

- **`--timeout` on the CLI overrides the panel's own `timeout_s`** (`quality/harm-watch.py:271-274`:
  `if args.timeout is not None: return args.timeout`). Section A therefore did **not** exercise the
  600 s cap; it is a control for "the r99 panel is green when the cap is not the binding
  constraint", not a re-run of round 99's miss.
- **`gate_elapsed_emitted` is a property of the candidate gate only.** The base gate (A) prints no
  `elapsed_ms`; every `LEG` line of B/E/H ends `elapsed_ms=<int>` and every `--json` leg object
  carries an integer `elapsed_ms` (`elapsed_ms=64` on a sub-second leg, `elapsed_ms=428190` on the
  slowest leg of H).

## 2. The two section-B failures, classified - neither retried away

Section B ran at `219e14f4`, the first revision that carried the round-100 artifacts. Two legs
mismatched. Both are reported exactly as measured, then isolated by changing one input at a time.

### 2.1 `ledger rc=1 expect=0 marker=MISS` - REAL mismatch, a records gap at that revision

Captured output (`ledger.log`, verbatim in the receipt):

```
LEDGER-ROW reason=uncovered path=quality/counters/c1-r100-launchenv-path.py detail=no-row
LEDGER-ROW reason=uncovered path=quality/counters/c2-r100-harm-watch.py detail=no-row
LEDGER: population=201 ledger_rows=199 uncovered=2 dangling=0 bad_pointer=0 empty_desc=0 \
        verdict=TARGET_MISSED rev=219e14f4a89075005b3c4dfa87651356b1e9719c
```

The round's two new counters were committed at `219e14f4` without their `quality/tool-ledger.md`
rows. The leg discriminates correctly; the panel's own note for this row says "re-freeze if a round
lands files without ledger rows". This is not host load (2 s to refusal) and not environment.
Repair confirmed landed at `18bce790` ("round-100: ledger rows for the two round-100 counters"):
section D re-ran the same leg at that rev and got `rc=0 marker=ok elapsed_ms=1883`. I re-measured at
a newer tip rather than re-running the same rev, which would only have reproduced the finding.

### 2.2 `r97c1_filetype rc=2 expect=0 marker=MISS` - ENVIRONMENTAL, this seat's scratch root

Captured cause (`r97c1_filetype.log`, verbatim in the receipt): the round-97 fresh-case generator
died with `OSError: AF_UNIX path too long` on `srv.bind(p)` at `filetype-fresh-r97.py:216`, called
from `case()` (`:253`), with `root = <gen_dir>/case-NNN` (`:394`).

The failure is a pure path-length bound, and it is exact:

```
sun_path usable bytes                         107
path segments the leg controls (per socket)   /r97c1_filetype 15 + /c1r97-y2_8113c 15
                                              + /freshroots-<tag> 13 + /case-139/s.sock 16 = 59
=> maximum usable --scratch-root              107 - 59 = 48 characters
this seat's --scratch-root                    /fast/scratch/hyaku/mado-r100/R100MExecPanel/scr2 = 49
measured failing socket path                  49 + 59 = 108 bytes  -> ENAMETOOLONG
```

One character over. Section C re-ran the *same leg at the same rev* with only `--scratch-root`
changed to `/tmp/m100p/s`:

```
LEG r97c1_filetype rc=0 expect=0 marker=ok ok elapsed_ms=754047
MADO_FILETYPE_COUNT: TARGET_MET pred=PRED-C1-r97-v1 ... cases=157 correct=157 classes=15/15 ... EXIT 0
```

So the arithmetic is confirmed twice: the leg passes at a short root, and its refusal is a seat
scratch-path property, not a property of the round's artifacts and not host load (7.3 s to
refusal, no `rc=124`, no `timeout-after-`). Sections E and H used 12-character scratch roots and the
leg passed there.

**This is an instrument fragility worth a rule, and it is new this round.** The panel's `SCRATCH`
element is `<scratch-root>/<leg-id>`, so a caller's scratch root is an undeclared input to the
`r97c1_filetype` leg: 49 characters is green everywhere else and red on that leg only.
Recommendation (QUALITY/lesson, L1 decides): either the gate refuses a `--scratch-root` longer than
the panel declares at setup (a declared limit, not a red leg), or the leg note carries the
48-character bound. Nothing in `.ufo/waves/round-100/controls/harm-panel-r100.json` states it today.

## 3. Contract-3 conformance of the candidate gate (measured against its own bytes)

- **Diff scope, base to candidate**: only the `time()` import, `t0`/`elapsed_ms` on every `run_leg`
  return path, `elapsed_ms=<n>` appended to the human `LEG` line, `elapsed_ms` in the `--json` leg
  object, and seven new `--selftest` checks. No census function, no exit map and no leg-scoring
  line is touched.
- **Diff scope, build copy `2d604f7b654f` to committed `acecb0ea4257`** (11 diff lines): one
  selftest check, `timeout-elapsed-ms`, parses the value instead of substring-matching it. Both
  print `HARM_WATCH_SELFTEST: checks=33 failed=0` (base gate: `checks=26 failed=0`, rc 0).
- **`--json` fields**: base and candidate have identical top-level keys
  (`census exit legs legs_run mismatch ok panel repo rev`); the per-leg object gains exactly
  `elapsed_ms` (`added=[elapsed_ms] removed=[]`), measured on the same panel, rev and `--only index`
  leg.
- **Census findings byte-identical**: on the two census-only planted panels both gates print
  `PANEL PANEL_LEG_MISSING id=r97c1_filetype round=r97` and
  `PANEL PANEL_LEG_UNKNOWN id=gate_xdgmime`, exit 2 each.
- **Declared SETUP_ERROR legs stay declared**: `r90c1_portal_routing`, `r95c1_mimesniff`,
  `r95c2_selftest_kills`, `r96c1_magictext` each `rc=2 expect=2 marker=ok` in every full run.
- **Frozen cap arithmetic re-derived here**: `timeout_s=3600` gives 3,600,000 ms; the lane's timing
  receipt (`e7280b53a90c`, 28 timed legs) has `max_elapsed_ms=708014` (`r92_gate_defects`), so
  `2*max = 1,416,028 <= 3,600,000`, and exactly one leg exceeds 600,000 ms
  (`control_600s_would_mismatch = 1`). My own runs give independent samples of the same
  load-dependence: section B measured `r92_gate_defects` at 619,422 ms (over 600 s), while sections
  E and H measured the panel maximum at 516,862 / 428,190 ms (under 600 s) at lower load. The cap's
  insufficiency is therefore carried by the timing receipt, not by any claim about today's load.

## 4. Findings for the L1 (outside my write scope)

1. **`SKILL.md:2985` is now stale.** The `mado-harm-watch` row says its selftest "prints
   `HARM_WATCH_SELFTEST: checks=26 failed=0`"; the committed gate prints `checks=33 failed=0`
   (measured on `37a0544b160d` gives 26, on `2d604f7b654f` and `acecb0ea4257` gives 33). The row's
   provenance column also still names the round-99 panel. Under QUALITY 171 / M99-1 this is a row's
   own claim about bytes, so it must be re-derived and updated, not left to a reader's run.
2. **`quality/tool-ledger.md:236`** describes `quality/harm-watch.py` as "round 99" and does not
   mention the per-leg `elapsed_ms` surface; the ledger row is a description, not a pin, but it is
   the tool's ledger entry.
3. **`--scratch-root` length is an undeclared input to the `r97c1_filetype` leg** (2.2); bound 48
   characters at today's leg-id and counter subdirectory names.
4. **The committed receipt at HEAD is a mid-run truncation.** `git show
   ae537dbe:.ufo/waves/round-100/receipts/c2-panel-r100.txt` is 32 lines (`2cfb9f2daf27`), stops
   after 26 `LEG` lines, and carries no `HARM_WATCH:` line, no `EXIT_CODE` and no `WALL_S`; the
   working-tree receipt is 218 lines (`302532e31ed3`) with all six sections. A snapshot taken while
   the background run was still appending is not a receipt; the land must take the worktree bytes.
5. **The committed timing receipt still has no `TIMING-DONE` line.** `git show
   ae537dbe:.ufo/waves/round-100/receipts/panel-timing-r100.txt` hashes `dd8d9f88c9ba` and matches
   `^TIMING-DONE` zero times at `18bce790` and at `ae537dbe`; the worktree copy
   (`e7280b53a90c`) has the line. The C2 counting command refuses a receipt without it, so the
   frozen command cannot be green at any committed revision until the receipt is re-landed with its
   terminator. I verified this byte state myself; the counter seat reached the same state.
6. **Panel wording, informational.** `.ufo/waves/round-100/controls/harm-panel-r100.json` is
   content-identical to the round-99 panel on every declared field (28 rows, all six fields per row
   equal; `rounds` and `census_rule` equal) with only `timeout_s` 600 -> 3600. The file is not
   byte-identical: it is serialized compactly (14,962 -> 16,774 raw bytes for the `legs` region).
   If contract 3's "byte-identical rows" is meant literally, the wording needs the addendum-8
   narrowing; the enforced property (row values unchanged) holds.

## 5. Limits

- Timing is single-host and load-dependent: load average was 249-260 during the lane's timing pass,
  180-260 during section B and 35-67 at sections H. No leg in any of my six runs failed for load
  (`rc=124` and `timeout-after-` occur zero times in the receipt).
- Section B and E ran the build copy `2d604f7b654f`; section H re-ran the panel on the committed
  bytes `acecb0ea4257` that the C2 counter pins. The delta between them is one `--selftest` check
  (11 diff lines), so B and E remain valid evidence for the panel path; H is the run at committed
  bytes.
- Sections C and D are `--only` controls: their `HARM_WATCH: legs=1|2` line counts the legs run,
  not the census, and they must not be quoted as full-panel evidence.
- I ran no glib measurement, no C1 counter and no `gio launch`; nothing here models glib. The
  candidate under test in this receipt is the lane's gate, which is an instrument, and the panel's
  legs are instruments it spawns; I wrote no `subprocess`/`socket`/`ctypes` code.
- Not measured by me: whether the lane's probe/timing scripts behave the same on a second host, and
  whether `elapsed_ms` is monotone across a deliberately slowed leg outside the gate's own selftest.

## 6. Scratch and tooling

- Scratch `$HYAKU_SCRATCH/mado-r100/R100MExecPanel`
  (`/fast/scratch/hyaku/mado-r100/R100MExecPanel`) and the short-root area `/tmp/m100p`: both
  deleted before this report was filed; every receipt line they produced is copied into
  `.ufo/waves/round-100/receipts/c2-panel-r100.txt` first. Nothing of mine remains on disk.
- No tool was installed or upgraded; no pacman transaction (all are paused host-wide), no `sudo`, no
  host service touched, no host application launched, no credential path read, no sysctl or binary
  edited. All lane writes are the two files this seat owns.

## 7. Cross-domain evidence

- **none.** The surface measured is the lane's own instrument (`quality/harm-watch.py`, its frozen
  panel, and the 28 counting-command legs the lane already owns). The sweep is the panel itself: all
  28 legs in every full run, with the two failing legs isolated by single-variable re-runs. No
  external domain, host configuration or second lane was touched.

Report: .ufo/waves/round-100/w1/R100MExecPanel.md
