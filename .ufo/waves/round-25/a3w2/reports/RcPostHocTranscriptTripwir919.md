# RcPostHocTranscriptTripwir919 — C2 ledger re-check of a3w1 seat `CapPostHocTranscriptTripwir919`

Seat: `MadoR25A3.RcPostHocTranscriptTripwir919` (reviewer, C2 ledger attack). Wave: round-25 attempt 3, `a3w2` (DATA + FALSIFY).
Target report: `.ufo/waves/round-25/a3w1/reports/CapPostHocTranscriptTripwir919.md` — a re-derivation of the
SCORECARD.md:919 row (`post-hoc transcript tripwire`, round-17 capability) at base `41cc04c8`.

## What I did

1. Cloned the lane into my own sandbox (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; no git writes in the lane):
   ```
   mkdir -p /fast/scratch/hyaku/mado-r25a3/rc
   env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/rc/CapPostHocTranscriptTripwir919
   env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <clone> checkout -q --detach 41cc04c8
   # rev-parse HEAD → 41cc04c8d593837a0d5078bffaacdaa163d12897
   ```
2. Read the row at `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md` (1,618 lines,
   matching the report) and every `tripwire` mention after line 919; read the round-23/24 superseding sections
   (lines 1548-1596) and the caveats at 906, 1136-1143, 1198-1202 directly.
3. Re-ran the demonstration command exactly as written and in the nearest documented form
   (`timeout 600`, `prlimit --as=4000000000`, `python3 -I -B`), plus the nine classification probes and the
   non-jsonl path, plus a `--scan` of the committed re-cut input.
4. Verified the anchor receipt file bytes, the evidence-pointer resolution, the original transcript's absence
   from the session store, the tool sha256, and the hardening-suite case rename.
5. Deleted my clone and probe files (`rm -rf`, exit 0; `ls` confirms). No `__pycache__` left (all runs used `-B`).

## Independent re-derivation — every check reproduced

| Report claim | My observation | Match |
|---|---|---|
| Row text at SCORECARD.md:919 under `### Capabilities (round 17)` | identical row, same line | yes |
| As-written brace command exits 2 (usage) | `usage: … --selftest DIR` + `MADO_TRIPWIRE: could_not_evaluate` + `{"error":"usage","exit":2}`; exit=2 | yes |
| `--selftest` accepts exactly one DIR | `tools/mado-tripwire.py:3382-3383`: `len(argv)==2 and argv[0]=="--selftest"` | yes |
| Per-dir: core 9/9, compound 16/16, hardening 33/33, w2-regressions 30/30, all exit 0 | identical `SELFTEST_SUMMARY` lines, `SELFTEST_SCRIPT_SHA256: cd9da20c…ea84`, exit=0 each | yes |
| Tool bytes at base = `cd9da20c2f562e…ea84` | `git show 41cc04c8:tools/mado-tripwire.py \| sha256sum` → `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` | yes |
| Nine probes (magic-bash, bang, literal-spawn, heredoc-shell, heredoc-data, live-probe-read, mutation-verb, clean-read, non-jsonl path) | all nine identical: classes `package_query/package_query/host_mutation/package_query/∅/live_probe/host_mutation/∅/error`, exits `1/1/1/1/0/1/1/0/2`, same rules (`pacman:-Qi`, `systemctl:restart`, `hyprctl:binds`, `hyprctl:dispatch`) | yes |
| `evidence/` pointers resolve only under `.ufo/waves/round-17/evidence/` | no repo-root `evidence/` dir; both files exist wave-relative | yes |
| Anchor receipt: exit 1, counts 2/1/5, 173-line transcript sha `78388d42…` | receipt verbatim matches | yes |
| Original transcript gone from session store | `ls` on the receipt's path → No such file or directory | yes |
| Re-cut `.ufo/waves/round-18/frozen/inputs/r15-libinput-events.jsonl` (sha `7118b883…`, 5 lines) scans exit 1 with counts 2/0/0 | identical | yes |
| Round-24 table supersedes (line 1579 `works`, preamble 1570-1571) | verbatim | yes |
| Line 1548 tool-restore `cd9da20c…` | verbatim (line 1554 carries the hash) | yes |
| Fixture drift: hardening `multiline-quoted-commit-clean` → `-vcs` (quote spans 1136-1141) | `-vcs` case present in `hardening/expected.json:66` | yes |
| Scope caveat: `tool_install`/`vcs_write` "not entered as capabilities" (round-19 addendum) | verbatim (heading at 1198, text 1200-1202; tool emits both extra classes in counts) | yes |
| Known-limit qualifier at line 906 (`adversarial 4/26 pinned as known limits`) | verbatim | yes |
| No contradiction: round-24 `fails` at 1582 is the *different* `tripwire evidence marker` row (1342) | verified — different capability | yes |
| Command form field: brace form exits 2 → per-dir form is the documented shape | identical; no other SCORECARD line re-spells the four dirs as one invocation | yes |

## Discrepancies found (minor, non-load-bearing)

1. **Receipt line count wrong.** Report §1: evidence files are "2 lines each". `tripwire-anchor-r15.txt` is
   2 lines, but `tripwire-pacmanlog-join.txt` is **18 lines** (`wc -l`). Cosmetic; both files do exist and are
   stored receipts as claimed.
2. **Transcript length wrong.** Report §3: the four-invocation transcript was "104 lines — 95 `CASE … ok`
   lines". Measured: **96 total lines, 88 CASE lines** (11+18+35+32 per dir; CASE = 9+16+33+30 = 88, which
   equals the SELFTEST_SUMMARY totals). Cosmetic; the per-dir counts it asserts are exactly right.
3. **Slightly loose line citations.** The "supersedes the implied works" quote is cited as lines 1569-1571
   (actual sentence at 1570-1571); the fixture-drift quote is cited as "line 1136" (actual span 1138-1141);
   the round-19 addendum is cited as "line 1200" (heading at 1198, text at 1200-1202). All quotes themselves
   verbatim and on-target.

## Flags checked — none present

- **Copied-not-run evidence:** no. Every number I re-derived matches values that could only come from a real
  run at this revision (selftest shas, exact counts, error JSON).
- **Wrong revision:** no. HEAD `41cc04c8d593…`; SCORECARD 1,618 lines; tool sha `cd9da20c…` — all self-consistent.
- **Overclaim:** no. The report correctly refuses to call the as-written exit 2 a capability `fails` (it is a
  usage error), and correctly carries the anchor multiset as non-reproducible rather than claiming it.
- **Missed superseding text:** none found. I grepped all post-919 `tripwire` mentions; the report names the
  operative superseder (1579), the byte supersession (1548), the scope caveat (1200), the known-limit
  qualifier (906) and the disclosed fixture drift — and correctly distinguishes the line-1582 `fails` row as
  a different capability.

## Verdict

`RECHECK CapPostHocTranscriptTripwir919: agree — all load-bearing evidence re-derived at 41cc04c8 (brace form exit 2 usage, four per-dir suites 9/9,16/16,33/33,30/30 exit 0, all three classes and exits 0/1/2 reproduced, anchor multiset honestly non-reproducible); minor nits: join receipt is 18 lines not "2 lines each", four-dir transcript is 96 lines/88 CASE not "104/95", three citations off by ≤2 lines`

## Bounds

No git/jj writes in lane or fleet repos; sandbox git only under `/fast/scratch/hyaku/mado-r25a3/rc/` with
GIT_* unset. No packages installed or upgraded; no pacman, service, config or live-compositor action; no
`hyprctl` invocation; no nested compositor. Clone and probes deleted (`rm -rf` exit 0; verified absent).
No `__pycache__` left in the lane (all python invoked with `-I -B`). Only lane write is this report.
