# CritQualityTrend — C1/C2 and learning-trend quality (w2, falsify)

Seat scope: adversarial assessment of claim/trend quality, not of the tool's or entry's authorship. Base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`; frozen instruments `quality/counters/c1-r48-terminal-cache.py` (from
`l1-draft/`) and `l1-draft/c2-r48-xkb-entry.py`. Everything below was run by me in `/fast/scratch/hyaku/mado-r48/CritQualityTrend`
(two `--shared --no-checkout` clones plus base-pathspec checkouts, worktrees under the seat root; scratch removed at the
end). Receipts in `.ufo/waves/round-48/w2/CritQualityTrend/`. No lane file, registry, counter or report was edited.

## 0. Verdicts the data actually support

| Question | Verdict | Basis |
|---|---|---|
| Does C1 advance the operability surface? | **Yes, measured on the frozen predicate** | base tool `TARGET_MISSED` (`warm=134/204 explained=231/394 generated=210/230 selftest=fail`), l1-draft tool `TARGET_MET` (`204/204, 394/394, 230/230, selftest=ok readonly=ok`); same nonce, same host, my runs |
| Is curation coverage held at r47? | **Held; +11 rows are the only registry change** | SOURCES 276 -> 287 rows (S340-S350), knowledge entries 64 -> 65, held S318/S319 and the r46 entry byte-equal (`clause=h held=S318,S319 unchanged=1` in my run) |
| Is C2 new ground beyond r46? | **Yes, structurally new and independently replayable** | entry absent at base (my base run: `clause=a entry_absent`), 4/4 GROUND terms absent at base, 3/4 present at REV; my own `xkbcli` replay reproduces the receipt's `sha256=efd487a39920` and rc `(1,1,0)` |
| Are the claims clean against a do-nothing counter? | **Yes for both claims; the predicate still has a measured hole** | base misses both (`c1-base-missed.txt`, `c2-base-missed.txt`); but a reference-grade tool that **writes the resolver's cache** still `TARGET_MET` (§3) |
| Any harm to held rows/index/quality? | **Yes, three docs-level harms and one evidence gap** | README:111 still says the warm-cache path is open; SKILL.md carries a false XKB rule and a duplicated sentence; entry step 9 contradicts its own receipt; 11 of 20 C1 controls were never scored on the frozen set (§4, §5) |

Trend verdicts supported by data (vocabulary `improved / unchanged / harmed`):

- **expansion: improved.** One new sourced entry, 11 new tier-A rows, ground terms absent at base, held rows untouched.
- **operability/capability: improved** (capability), but **not a counted axis move**: the axis table is derived from
  `SCORECARD.md`, which carries no round-48 section yet, so navigation 64/64, calibration 82/82, operability 12/12 are
  untouched by this wave and were **not re-measured by me**. Claim only "new class modelled and measured", not "axis +N".
- **quality: not `improved` on this evidence.** The round's own quality standard is textual/sourcing accuracy of the
  landed bytes; this wave lands a false rule in `SKILL.md`, a false sentence in the new entry, a stale frontier line for
  the capability it is the round's quality move for, and a must-miss control that meets. `unchanged` understates the two
  false statements; `harmed` is defensible and is what the data support (§7).
- **discernment: `unprovable-but-better` at best.** Two explicit rejects with flip conditions exist (gate-rows.md), but no
  outside-lane admit/reject sample; nothing in this wave changes that (same limit as round 47).

## 1. C1 — capability advance is real, and its fixture set overstates the new class by ~3x

Commands (my clone `c1/tree` = base `tools/ quality/ .ufo/waves/round-47/fetch` + `l1-draft/mado-terminal.py`,
`l1-draft/c1-r48-{terminal-cache.py,fixtures.json}` committed on top; `--work` outside every hidden path):

```
python3 -I quality/counters/c1-r48-terminal-cache.py --repo <clone> --rev HEAD   --work <seat>/work1 --nonce 4848
python3 -I quality/counters/c1-r48-terminal-cache.py --repo <clone> --rev 579f694b… --work <seat>/work1 --nonce 4848
```

Observed (retained verbatim):

- `c1-draft-met.txt`: `cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0.
- `c1-base-missed.txt`: `cold=190/190 warm=134/204 explained=231/394 generated=210/230 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED`, exit 1.

Reading that matters for trend quality:

1. The predicate is **not** passable by doing nothing: 70/204 warm, 163/394 explain and 20/230 generated cases fail at base.
2. The class premises are enforced live, not asserted: `check_premise` (counter `:605-625`) requires a cold twin and
   raises `Setup` when a `WARM-DIFFERS` fixture stops differing. The 204-case set counts: 48 `WARM-DIFFERS`, 34
   `WARM-INVALID`, 31 `MALFORMED`, 26 `WARM-SAME`, 12 `H1` + 13 `H2`, 10 `HOME-UNSET`, 10 `READDIR`, 17 one-off
   `MALFORMED-<NAME>`, and `CACHE-DEFAULT`/`EDGE-HOMEUNSET`/`WARM-ABSENT` one each.
3. **Presentational sizing defect, not a predicate defect:** "warm=204/204" reads as 204 new-class cases, but at base
   134/204 already pass — only 70 fixtures (34%) actually exercise the cache edge. A trend sentence that counts 204 as new
   coverage overstates the move by 2.9x. Say "204 warm fixtures, 70 of them discriminating against the round-47 tool".
4. `readonly=ok` is narrower than it sounds — see §3.

The implementation is not a crib: `tools/mado-terminal.py` (working tree) adds `ls_lRL`, `gen_hash`, `read_cache`,
`select_paths` and a `warm_selftest`, i.e. a re-implementation of `ls -LRl`/hash/cache parsing, and the 230 nonce cases are
generated at count time (`clause=g generated=230/230`). Registered residual that remains true: the nonce is an argument the
L1's own scripts fix (`c1-score.sh` default `NONCE=4848`), so nonce-independence is not what makes cribbing hard — the
generator's generality is.

## 2. C2 — new ground, replays on my host, held rows intact

My mirror (`c2/tree`) = base with `corpus/ quality/ tools/ SKILL.md .ufo/waves/round-4{6,7}/fetch` checked out plus the
round-48 draft/integration overlay (`l1-draft/xkb-keymap-compile-r48.md`, `rows-c2.md` into SOURCES after S339,
`readme-row.md` into README, `fetch/`, `receipts/`, `tools/`), committed; overlay recipe identical to `l1-draft/c2-mirror.sh`.

```
TMPDIR=<seat>/c2/work python3 -I .ufo/waves/round-48/l1-draft/c2-r48-xkb-entry.py --repo <mirror> --rev HEAD
TMPDIR=<seat>/c2/work python3 -I … --repo <mirror> --rev 579f694b45c797a9c39761fdb4f9e0a1b71b3585
```

- `c2-replay-own-run.txt`: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1 verdict=TARGET_MET`, with
  `clause=b ids=11`, `clause=d quotes=18`, `clause=e steps=9 pin_cited=9`, `clause=i all_absent_at_base=1 present_at_rev=3/4`,
  `clause=r replay=ok sha=efd487a39920 neg=(1,1,0) ver=1.13.2`. The replay digest is my own `xkbcli` run, byte-matching the
  committed receipt — so the receipt is not merely a typed claim.
- `c2-base-missed.txt`: `clause=a entry_absent … verdict=TARGET_MISSED` at the real base revision.

New ground, not a restatement: all 11 rows are libxkbcommon 1.13.2 / xkeyboard-config 2.48 / one own-work host receipt;
the four GROUND terms are absent from `corpus/` at base; the compositor half is cited as held (entry step 8 and Limits say
"held … not re-measured here"), so the r46 claim is not re-claimed. Registry arithmetic: 276 -> 287 rows, 64 -> 65
knowledge entries, no new census finding for S340-S350 (`census-mirror.txt` E11 lines are S184/S185/S332-S339 referencing
`.ufo/` paths my pathspec checkout omitted — pre-existing, not caused by the new rows).

Defect in the round's own audit trail (draft doc, not committed): `l1-draft/gate-rows.md` gates "rows S340-S350" but lists
S340-S346, S348-S350 — **S347 is missing from the gate list** although the row exists in `rows-c2.md` and SOURCES (`:296`)
and the entry cites it (`source: S347`, `OBS S347`). The counter's clause b/c accept it, so this is a hole in the gate
document, not in the freeze.

## 3. Measured pre-data hole: the frozen C1 predicate cannot see a file write, so "writes-cache" does not miss

Registration, Controls: "`writes-cache`" is in the must-miss list, and "a control that meets triggers a fixture/counter
repair before freeze". The w1 report (`w1/ExecControlsC1.md:57`) says that control is caught only by clause `w` because
"every primed fixture (`/.rw/cache/xdg-terminal-exec` changes)". I tested both halves:

1. **The w1 control as shipped misses for the wrong reason.** Running
   `w1/ExecControlsC1/controls/writes-cache.py` through the frozen counter (`c1-w1-writes-cache-control-missed.txt`) gives
   `warm=197/204 explained=380/394 selftest=fail verdict=TARGET_MISSED` — the seven warm failures are six `HOME-UNSET`
   fixtures (`v2-hu-01,06,07,08,09,10`) plus `L1-10-desk-echo-n-edit`, i.e. the control is built on a pre-D1 reference and
   fails on HOME handling, not on writing. Nothing in the failure list is a cache-state difference.
2. **A reference-grade tool that writes the cache MEETS.** I patched the l1-draft tool (selftest 69/69 before and after) to
   write `<XDG_CACHE_HOME|HOME/.cache>/xdg-terminal-exec` after `print`/`explain` — exactly `save_cache`'s failure mode and
   exactly what `tools/mado-terminal.py:101` promises the tool never does. Result (`c1-refpluswrite-met.txt`):

```
cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

So the frozen predicate **admits a tool that writes a file**: clause `r` traces `execve,execveat,socket,socketpair,connect`
only (declared in the registration), and clause `w` compares answers and the oracle's derived cache state per tree — it
never fingerprints the tool tree's cache before/after the tool run (`grep` over the counter finds no cache snapshot; the
only cache handling is `materialize`/`prepare` setup at `:398-560`).

Consequences to fix before data (only possible window; after data the predicate is immutable):

- The round cannot claim write-freedom: `readonly=ok` means "no further process or socket". Either drop "still … opening
  no socket"-style read-only wording for the write half, or add a tree fingerprint clause (hash the tool tree's cache file,
  modes and mtimes around the tool run and require equality) and re-run the complete control set.
- The must-miss evidence for `writes-cache` currently exists **nowhere** against the frozen set. My probe is the only
  retained demonstration, and it is a *hit*, i.e. the registration's own repair trigger has fired pre-data.

## 4. Content defects the two predicates cannot see (each measured, not inferred)

1. **C2 entry self-contradicts on the count-mismatch diagnostics.** `l1-draft/xkb-keymap-compile-r48.md:36` (step 2):
   "a longer one is truncated with an **ERROR-level line**". `:43` (step 9): "A layout/variant count mismatch is a
   **warning** and therefore **invisible by default**". Both arms are one file: `rules.c:520-535` uses `log_warn` for
   "More layouts than variants" and `log_err` for "Less layouts than variants". The committed receipt already refutes
   step 9 at default log level: `receipts/xkbcli-compile-keymap-r48.txt:243` header "(warning is below the default log
   level)" for the `More` arm, then `:260-270` `--- one layout, two variants` shows `xkbcommon: ERROR: Less layouts than
   variants` at `:262` with `rc=0` at `:270`. My own probe (`xkb-probes.txt`) reproduces it: `br` + `nodeadkeys,intl` -> `rc=0` **with the
   ERROR line printed at default level**. A reader who trusts step 9 will not look for the line the tool actually prints.
2. **`SKILL.md:2282` states a false rule about the surface this round is supposed to have sourced**: "a longer list is an
   error (`Less layouts than variants`) and the compile exits 1". Measured: `br` + `nodeadkeys,intl` (longer variant list)
   exits **0** (`xkb-probes.txt`, and receipt `:270`). The truncation is non-fatal; the `rc 1` in the counter's negative
   probe comes from the surviving `br(intl)` having no map, not from the list length.
3. **`SKILL.md:2282`'s catalogue advice is incomplete in the same class**: "take the variant from that layout's own rows
   (`xkbcli list` … `br` has 9 rows)". `br` defines **11** `xkb_symbols` maps and `--variant olpc` compiles `rc=0`
   (`xkb-probes.txt`), yet `xkbcli list` prints 9 `br` rows, so `olpc` is a valid variant the advertised catalogue cannot
   show. The entry's own Limits ("`br` has eleven maps") is right; the skill row is the one that misleads.
4. **`SKILL.md:2237` carries a duplicated clause**: "ground now `corpus/knowledge/xkb-keymap-compile-r48.md` (rows
   S340..) ground now `corpus/knowledge/xkb-keymap-compile-r48.md` (rows S340-S350)". `SKILL.md:2279` is garbled in the
   same block: "`xkbcli list` has no options section, so the warning is the only catalogue the package does ship a
   catalogue at `/usr/share/xkeyboard-config-2/rules/evdev.lst` … a static list that predates the warning and is the
   better first read" — self-contradictory ("only catalogue" vs "does ship a catalogue"; "predates the warning" vs "better
   first read").
5. **The C1 index line is stale by construction.** `corpus/README.md:111` (round-47 bullet) still lists "the warm-cache
   path" under "Still open", while C1's claim is that the surface moved from frontier to core. Nothing in the integration
   adds a C1 line (README diff = +2 lines, both C2; `SKILL.md` diff = +130 lines, all XKB). C1's own clause set is
   separated from README by design, so the predicate cannot see that the corpus now asserts the opposite of the round's
   C1 claim. Either rewrite the r47 "still open" list or add the capability sentence; otherwise the round's quality move
   is contradicted by its own index.

None of 1-4 is detectable by the frozen counters: C2 clause `e` counts numbered steps and their pin locators (declared
"not the truth of each step"), clause `f` reads labelled rc values, and no clause reads `SKILL.md` at all.

## 5. Controls completeness at freeze (evidence gap, not a claim defect)

`w1/ExecControlsC1.md` §1 is explicit: the draft pass was still running when w1 closed, and the table marks **11 of 20**
controls `cut` (`trust-any`, `hash-no-total`, `no-line-limit`, `md5-subproc`, `writes-cache`, `mut-desktop-lower`,
`mut-no-command-v`, `mut-cache-fallback`, `mut-eof-terminator`, `mut-terminator-contains`, `mut-warm-ignores-args`);
9 carry a draft-cell verdict. The registration says the 20 "must be re-scored against this frozen merged fixture set".
At freeze they were not. I completed two of them independently — `reference` (MET, §1) and `base` (MISSED, §1) — plus the
`writes-cache` row (§3, hit). The other 17 rows rest on the w1 local pin-judged loop and on partial draft receipts.

Also: the reference's own completed run quoted in that report was `warm=32/32` — a pre-merge 32-case set, not the frozen
204. Before the data commit, the full 20-control re-score on `c1-r48-fixtures.json` is the admission evidence a later
reader will expect, and 11 rows currently have none.

## 6. No-harm checks on held rows, prior verdicts and census

- Held ground byte-equal (`clause=h held=S318,S319 unchanged=1 pins=2` in my run), r46 entry unchanged; no existing row's
  status/recheck/used-by was edited by the 11 inserted rows (`rows-c2.md` diff is insert-only after S339).
- R4b: the frozen round-45 counter still admits the errata revision — `receipts/r4b-append-l1.txt` reads
  `PRED-C2-r45-v2 … admitted=1/1 verdict=TARGET_MET rev=5582d8e…` for the landed block and both `PRED-C2-r45` and `-v2`
  `TARGET_MISSED` for the as-drafted control. **This is L1 self-evidence; I did not reproduce it** (the appended revision
  is not in the lane history and I did not rebuild it).
- M48-7 (the clause-`r` flake) was fixed **before** freeze: the retained failing receipt `l1-c1-ref-final3.txt`
  (`trips=2`, `readonly=fail`) sits beside five `trips=0` runs, and the frozen parser now trips only on a traced syscall at
  column 0. My three runs all read `trips=0`. No frozen-predicate flaw remains from that class — the write blind spot in §3
  is a different one.
- Census on the integrated mirror: no new finding for S340-S350.

## 7. Trend verdicts: what the data force

- `expansion improved` — supportable, with the numbers above (entry + 11 rows, ground absent at base, replay-bound).
- `operability improved` — supportable as **capability**, with three qualifiers that must appear in the same sentence:
  (i) 70/204 warm fixtures (not 204) exercise the new class; (ii) `readonly=ok` covers exec/socket, **not** writes; (iii)
  the predicate admits a writing tool (§3), so "read-only resolver" is a code claim, unverified by the instrument.
- `quality` — **`harmed` is the honest verdict for this round's bytes**, or `unchanged` if the round intends to judge only
  the *existence* of sourced ground. The counterexamples are concrete and all in bytes the round publishes: a false
  diagnostic rule in `SKILL.md` (`:2282`), a step-9 sentence refuted by the round's own receipt and contradicted by step 2,
  a duplicated clause at `:2237`, an incomplete catalogue instruction that hides a real variant (`olpc`), and a stale
  frontier line (`README:111`) that still says the C1 surface is open. `improved` is not supported by the data.
- `discernment` — `unprovable-but-better` (unchanged from round 47): explicit rejects exist, outside sample does not.

## 8. Evidence provenance (self vs peer vs independent)

| Evidence | Provenance | Used for |
|---|---|---|
| `c1-draft-met.txt`, `c1-base-missed.txt`, `c1-refpluswrite-met.txt`, `c1-w1-writes-cache-control-missed.txt` | **mine** (independent clones, frozen counter bytes, nonce 4848) | §1, §3, §5 |
| `c2-replay-own-run.txt`, `c2-base-missed.txt`, `xkb-probes.txt`, `census-mirror.txt` | **mine** (mirror built with the L1's own recipe; own `xkbcli` runs) | §2, §4 |
| `receipts/l1-c1-*.txt`, `l1-c2-before-base.txt`, `l1-warmcheck-*.txt`, `r4b-append-l1.txt` | L1 self-report | compared, not trusted alone; r4b explicitly not reproduced |
| `w1/ExecControlsC1.md`, `w1/CritClaimSizing`, `lessons/round-48.md` M48-1..8, `QUALITY.md` 96-101 + checkers | w1 peers | §5, §6; their conclusions reused only where I could check the bytes |
| Sanctioned deviations | ran the C1 counter with `RLIMIT_FSIZE` 2 MiB instead of 1 MiB | the counter copies `/usr/bin/gawk` (1,274,872 B) into its sandbox: at `ulimit -f 2048` it dies `OSError: [Errno 27] File too large: '/usr/bin/gawk'` before scoring. Every file I produced is < 1 MiB; largest output 77,194 B (`c1-base-missed.txt`); scratch 41 MB, removed |

## 9. Residuals of this assessment

- I did not re-measure the published axis table (SCORECARD-derived, no round-48 section yet) and did not reproduce R4b.
- My C2 mirror was built with the L1's overlay recipe, so it validates the counter, the pins, the quotes, the receipt
  replay and the registry row — not whether L1's later integration bytes equal these draft bytes.
- The write probe is a deliberate synthetic control (reference + one write); it proves the predicate's blindness, not that
  the delivered tool writes. The delivered tool's no-write property remains **unverified by any instrument** in this round.
